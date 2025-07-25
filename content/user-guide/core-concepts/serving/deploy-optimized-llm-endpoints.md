---
title: Deploy Optimized LLM Endpoints with vLLM and SGLang
weight: 5
variants: -flyte +serverless +byoc +selfmanaged
---

# Deploy Optimized LLM Endpoints with vLLM and SGLang

This guide shows you how to deploy high-performance LLM endpoints using SGLang
and vLLM. It also shows how to use Union's optimized serving images that are
designed to reduce cold start times and provide efficient model serving
capabilities.

For information on how to cache models from HuggingFace Hub as Union Artifacts,
see the [Cache a HuggingFace Model as an Artifact](cache-huggingface-model.md) guide.

## Overview

Union provides two specialized app classes for serving high-performance LLM endpoints:

- **[`SGLangApp`](../../../api-reference/union-sdk/packages/union.app.llm#unionappllmsglangapp)**: uses [SGLang](https://docs.sglang.ai/), a fast serving framework for large language models and vision language models.
- **[`VLLMApp`](../../../api-reference/union-sdk/packages/union.app.llm#unionappllmvllmapp)**: uses [vLLM](https://docs.vllm.ai/en/latest/), a fast and easy-to-use library for LLM inference and serving.

By default, both classes provide:

- **Reduced cold start times** through optimized image loading.
- **Fast model loading** by streaming model weights directly from blob storage to GPU memory.
- **Distributed inference** with options for shared memory and tensor parallelism.

You can also serve models with other frameworks like [FastAPI](./serving-a-model.md), but doing so would require more
effort to achieve high performance, whereas vLLM and SGLang provide highly performant LLM endpoints out of the box.

## Basic Example: Deploy a Non-Sharded Model

### Deploy with vLLM

Assuming that you have followed the guide to [cache models from huggingface](cache-huggingface-model.md)
and have a model artifact named `qwen2-5-0-5b-instruct`, you can deploy a simple LLM endpoint with the following code:

```python
# vllm_app.py

import union
from union.app.llm import VLLMApp
from flytekit.extras.accelerators import L4

# Reference the cached model artifact
Model = union.Artifact(name="qwen2-5-0-5b-instruct")

# Deploy with default image
vllm_app = VLLMApp(
    name="vllm-app",
    requests=union.Resources(cpu="12", mem="24Gi", gpu="1"),
    accelerator=L4,
    model=Model.query(),  # Query the cached artifact
    model_id="qwen2",
    scaledown_after=300,
    stream_model=True,  # Enable streaming for faster loading
    port=8084,
    requires_auth=False,
)
```

To use the optimized image, use the `OPTIMIZED_VLLM_IMAGE` variable:

```python
from union.app.llm import OPTIMIZED_VLLM_IMAGE

vllm_app = VLLMApp(
    name="vllm-app",
    container_image=OPTIMIZED_VLLM_IMAGE,
    ...
)
```

Here we're using a single L4 GPU to serve the model and specifying `stream_model=True`
to stream the model weights directly to GPU memory.

Deploy the app:

```bash
union deploy apps vllm_app.py vllm-app
```

### Deploy with SGLang

```python
# sglang_app.py

import union
from union.app.llm import SGLangApp
from flytekit.extras.accelerators import L4

# Reference the cached model artifact
Model = union.Artifact(name="qwen2-5-0-5b-instruct")

# Deploy with default image
sglang_app = SGLangApp(
    name="sglang-app",
    requests=union.Resources(cpu="12", mem="24Gi", gpu="1"),
    accelerator=L4,
    model=Model.query(),  # Query the cached artifact
    model_id="qwen2",
    scaledown_after=300,
    stream_model=True,  # Enable streaming for faster loading
    port=8000,
    requires_auth=False,
)
```

To use the optimized image, use the `OPTIMIZED_SGLANG_IMAGE` variable:

```python
from union.app.llm import OPTIMIZED_SGLANG_IMAGE

sglang_app = SGLangApp(
    name="sglang-app",
    container_image=OPTIMIZED_SGLANG_IMAGE,
    ...
)
```

Deploy the app:

```bash
union deploy apps sglang_app.py sglang-app
```

## Custom Image Example: Deploy with Your Own Image

If you need more control over the serving environment, you can define a custom `ImageSpec`.
For vLLM apps, that would look like this:

```python
import union
from union.app.llm import VLLMApp
from flytekit.extras.accelerators import L4

# Reference the cached model artifact
Model = union.Artifact(name="qwen2-5-0-5b-instruct")

# Define custom optimized image
image = union.ImageSpec(
    name="vllm-serving-custom",
    builder="union",
    apt_packages=["build-essential"],
    packages=["union[vllm]>=0.1.189"],
    env={
        "NCCL_DEBUG": "INFO",
        "CUDA_LAUNCH_BLOCKING": "1",
    },
)

# Deploy with custom image
vllm_app = VLLMApp(
    name="vllm-app-custom",
    container_image=image,
    ...
)
```

And for SGLang apps, it would look like this:

```python
# sglang_app.py

import union
from union.app.llm import SGLangApp
from flytekit.extras.accelerators import L4

# Reference the cached model artifact
Model = union.Artifact(name="qwen2-5-0-5b-instruct")

# Define custom optimized image
image = union.ImageSpec(
    name="sglang-serving-custom",
    builder="union",
    python_version="3.12",
    apt_packages=["build-essential"],
    packages=["union[sglang]>=0.1.189"],
)

# Deploy with custom image
sglang_app = SGLangApp(
    name="sglang-app-custom",
    container_image=image,
    ...
)
```

This allows you to control the exact package versions in the image, but at the
cost of increased cold start times. This is because the Union images are optimized
with [Nydus](https://github.com/dragonflyoss/nydus), which reduces the cold start
time by streaming container image layers. This allows the container to start before
the image is fully downloaded.

## Advanced Example: Deploy a Sharded Model

For large models that require distributed inference, deploy using a sharded model artifact:

### Cache a Sharded Model

First, cache a large model with sharding (see [Cache a HuggingFace Model as an Artifact](./cache-huggingface-model#advanced-example-sharding-a-model-with-the-vllm-engine) for details).
First create a shard configuration file:

```yaml
# shard_config.yaml
engine: vllm
args:
  model: unsloth/Llama-3.3-70B-Instruct
  tensor_parallel_size: 4
  gpu_memory_utilization: 0.9
  extra_args:
    max_model_len: 16384
```

Then cache the model:

```bash
union cache model-from-hf unsloth/Llama-3.3-70B-Instruct \
    --hf-token-key HUGGINGFACE_TOKEN \
    --union-api-key EAGER_API_KEY \
    --artifact-name llama-3-3-70b-instruct-sharded \
    --cpu 36 \
    --gpu 4 \
    --mem 300Gi \
    --ephemeral-storage 300Gi \
    --accelerator nvidia-l40s \
    --shard-config shard_config.yaml \
    --project flytesnacks \
    --domain development \
    --wait
```

### Deploy with VLLMApp

Once the model is cached, you can deploy it to a vLLM app:

```python
# vllm_app_sharded.py

from flytekit.extras.accelerators import L40S
from union import Artifact, Resources
from union.app.llm import VLLMApp

# Reference the sharded model artifact
LLMArtifact = Artifact(name="llama-3-3-70b-instruct-sharded")

# Deploy sharded model with optimized configuration
vllm_app = VLLMApp(
    name="vllm-app-sharded",
    requests=Resources(
        cpu="36",
        mem="300Gi",
        gpu="4",
        ephemeral_storage="300Gi",
    ),
    accelerator=L40S,
    model=LLMArtifact.query(),
    model_id="llama3",

    # Additional arguments to pass into the vLLM engine:
    # see https://docs.vllm.ai/en/stable/serving/engine_args.html
    # or run `vllm serve --help` to see all available arguments
    extra_args=[
        "--tensor-parallel-size", "4",
        "--gpu-memory-utilization", "0.8",
        "--max-model-len", "4096",
        "--max-num-seqs", "256",
        "--enforce-eager",
    ],
    env={
        "NCCL_DEBUG": "INFO",
        "CUDA_LAUNCH_BLOCKING": "1",
        "VLLM_SKIP_P2P_CHECK": "1",
    },
    shared_memory=True,  # Enable shared memory for multi-GPU
    scaledown_after=300,
    stream_model=True,
    port=8084,
    requires_auth=False,
)
```

Then deploy the app:

```bash
union deploy apps vllm_app_sharded.py vllm-app-sharded-optimized
```

### Deploy with SGLangApp

You can also deploy the sharded model to a SGLang app:

```python
import os
from flytekit.extras.accelerators import GPUAccelerator
from union import Artifact, Resources
from union.app.llm import SGLangApp

# Reference the sharded model artifact
LLMArtifact = Artifact(name="llama-3-3-70b-instruct-sharded")

# Deploy sharded model with SGLang
sglang_app = SGLangApp(
    name="sglang-app-sharded",
    requests=Resources(
        cpu="36",
        mem="300Gi",
        gpu="4",
        ephemeral_storage="300Gi",
    ),
    accelerator=GPUAccelerator("nvidia-l40s"),
    model=LLMArtifact.query(),
    model_id="llama3",

    # Additional arguments to pass into the SGLang engine:
    # See https://docs.sglang.ai/backend/server_arguments.html for details.
    extra_args=[
        "--tensor-parallel-size", "4",
        "--mem-fraction-static", "0.8",
    ],
    env={
        "NCCL_DEBUG": "INFO",
        "CUDA_LAUNCH_BLOCKING": "1",
    },
    shared_memory=True,
    scaledown_after=300,
    stream_model=True,
    port=8084,
    requires_auth=False,
)
```

Then deploy the app:

```bash
union deploy apps sglang_app_sharded.py sglang-app-sharded-optimized
```

## Authentication via API Key

To secure your `SGLangApp`s and `VLLMApp`s with API key authentication, you can
specify a secret in the `extra_args` parameter. First, create a secret:

```bash
union secrets create --name AUTH_SECRET
```

Add the secret value to the input field and save the secret.

Then, add the secret to the `extra_args` parameter. For SGLang, do the following:

```python
from union import Secret

sglang_app = SGLangApp(
    name="sglang-app",
    ...,
    # Disable Union's platform-level authentication so you can access the
    # endpoint in the public internet
    requires_auth=False,
    secrets=[Secret(key="AUTH_SECRET", env_var="AUTH_SECRET")],
    extra_args=[
        ...,
        "--api-key", "$AUTH_SECRET",  # Use the secret in the extra_args
    ],
)
```

And similarly for vLLM, do the following:

```python
from union import Secret

vllm_app = VLLMApp(
    name="vllm-app",
    ...,
    # Disable Union's platform-level authentication so you can access the
    # endpoint in the public internet
    requires_auth=False,
    secrets=[Secret(key="AUTH_SECRET", env_var="AUTH_SECRET")],
    extra_args=[
        ...,
        "--api-key", "$AUTH_SECRET",  # Use the secret in the extra_args
    ],
)
```

## Performance Tuning

You can refer to the corresponding documentation for vLLM and SGLang for more
information on how to tune the performance of your app.

- **vLLM**: see the [optimization and tuning](https://docs.vllm.ai/en/latest/configuration/optimization.html) and [engine arguments](https://docs.vllm.ai/en/latest/configuration/engine_args.html) pages to learn about how to tune the performance of your app. You can also look at the [distributed inference and serving](https://docs.vllm.ai/en/latest/serving/distributed_serving.html) page to learn more about distributed inference.
- **SGLang**: see the [environment variables](https://docs.sglang.ai/references/environment_variables.html#performance-tuning) and [server arguments](https://docs.sglang.ai/backend/server_arguments.html) pages to learn about all of the available serving
options in SGLang.
