---
title: Cache a Huggingface Model as an Artifact
weight: 3
variants: -flyte +serverless +byoc +selfmanaged
---

# Cache a HuggingFace Model as an Artifact

The [`union cache model-from-hf`](../../../api-reference/union-cli#model-from-hf) command allows you to automatically download and cache models from HuggingFace Hub as Union Artifacts. This is particularly useful for serving large language models (LLMs) and other AI models efficiently in production environments.

## Why Cache Models from HuggingFace?

Caching models from HuggingFace Hub as Union Artifacts provides several key benefits:

- **Faster model downloads**: Once cached, models load much faster since they're stored in Union's optimized blob storage.
- **Stream model weights into GPU memory**: Union's [`SGLangApp`](../../../api-reference/union-sdk/packages/union.app.llm#unionappllmsglangapp) and [`VLLMApp`](../../../api-reference/union-sdk/packages/union.app.llm#unionappllmvllmapp) classes also allow you to load model weights
  directly into GPU memory instead of downloading the weights to disk first, then loading to GPU memory.
- **Reliability**: Eliminates dependency on HuggingFace Hub availability during model serving.
- **Cost Efficiency**: Reduces repeated downloads and bandwidth costs from HuggingFace Hub.
- **Version Control**: Each cached model gets a unique artifact ID for reproducible deployments.
- **Sharding Support**: Large models can be automatically sharded for distributed inference.
- **Streaming**: Models can be streamed directly from blob storage to GPU memory.

## Prerequisites

Before using the `union cache model-from-hf` command, you need to set up authentication:

1. **Create a HuggingFace API Token**:
   - Go to [HuggingFace Settings](https://huggingface.co/settings/tokens)
   - Create a new token with read access
   - Store it as a Union secret:
   ```bash
   union create secret --name HUGGINGFACE_TOKEN
   ```

2. **Create a Union API Key** (optional):
   ```bash
   union create api-key admin --name MY_API_KEY
   union create secret --name MY_API_KEY
   ```

If you don't want to create a Union API key, Union tenants typically ship with
a `EAGER_API_KEY` secret, which is an internally-provision Union API key that
you can use for the purpose of caching HuggingFace models.

## Basic Example: Cache a Model As-Is

The simplest way to cache a model is to download it directly from HuggingFace without any modifications:

```bash
union cache model-from-hf Qwen/Qwen2.5-0.5B-Instruct \
    --hf-token-key HUGGINGFACE_TOKEN \
    --union-api-key EAGER_API_KEY \
    --artifact-name qwen2-5-0-5b-instruct \
    --cpu 2 \
    --mem 8Gi \
    --ephemeral-storage 10Gi
```

Let's break down each flag in the command:

- `Qwen/Qwen2.5-0.5B-Instruct`: The HuggingFace model repository
- `--hf-token-key HUGGINGFACE_TOKEN`: Union secret containing your HuggingFace API token
- `--union-api-key EAGER_API_KEY`: Union secret with admin permissions
- `--artifact-name qwen2-5-0-5b-instruct`: Custom name for the cached artifact.
  If not provided, the model repository name is lower-cased and `.` characters are
  replaced with `-`.
- `--cpu 2`: CPU resources for downloading the caching
- `--mem 8Gi`: Memory resources for downloading and caching
- `--ephemeral-storage 10Gi`: Temporary storage for the download process

When you run the command, you'll see outputs like this:

```
🔄 Started background process to cache model from Hugging Face repo Qwen/Qwen2.5-0.5B-Instruct.
 Check the console for status at
https://acme.union.ai/console/projects/flytesnacks/domains/development/executions/a5nr2
g79xb9rtnzczqtp
```

You can then visit the URL to see the model caching workflow on the Union UI.

If you provide the `--wait` flag to the `union cache model-from-hf` command,
the command will wait for the model to be cached and then output additional
information:

```
Cached model at:
/tmp/flyte-axk70dc8/sandbox/local_flytekit/50b27158c2bb42efef8e60622a4d2b6d/model_snapshot
Model Artifact ID:
flyte://av0.2/acme/flytesnacks/development/qwen2-5-0-5b-instruct@322a60c7ba4df41621be528a053f3b1a

To deploy this model run:
union deploy model --project None --domain development
flyte://av0.2/acme/flytesnacks/development/qwen2-5-0-5b-instruct@322a60c7ba4df41621be528a053f3b1a
```

## Using Cached Models in Applications

Once you have cached a model, you can use it in your Union serving apps:

### VLLM App Example

```python
import os
from union import Artifact, Resources
from union.app.llm import VLLMApp
from flytekit.extras.accelerators import L4

# Use the cached model artifact
Model = Artifact(name="qwen2-5-0-5b-instruct")

vllm_app = VLLMApp(
    name="vllm-app-3",
    requests=Resources(cpu="12", mem="24Gi", gpu="1"),
    accelerator=L4,
    model=Model.query(),  # Query the cached artifact
    model_id="qwen2",
    scaledown_after=300,
    stream_model=True,
    port=8084,
)
```

### SGLang App Example

```python
import os
from union import Artifact, Resources
from union.app.llm import SGLangApp
from flytekit.extras.accelerators import L4

# Use the cached model artifact
Model = Artifact(name="qwen2-5-0-5b-instruct")

sglang_app = SGLangApp(
    name="sglang-app-3",
    requests=Resources(cpu="12", mem="24Gi", gpu="1"),
    accelerator=L4,
    model=Model.query(),  # Query the cached artifact
    model_id="qwen2",
    scaledown_after=300,
    stream_model=True,
    port=8000,
)
```


## Advanced Example: Sharding a Model with the vLLM Engine

For large models that require distributed inference, you can use the `--shard-config` option to automatically shard the model using the [vLLM](https://docs.vllm.ai/en/latest/) inference engine.

### Create a Shard Configuration File

Create a YAML file (e.g., `shard_config.yaml`) with the sharding parameters:

```yaml
engine: vllm
args:
  model: unsloth/Llama-3.3-70B-Instruct
  tensor_parallel_size: 4
  gpu_memory_utilization: 0.9
  extra_args:
    max_model_len: 16384
```

The `shard_config.yaml` file is a YAML file that should conform to the
[`remote.ShardConfig`](../../../api-reference/union-sdk/packages/union.remote#unionremoteshardconfig)
dataclass, where the `args` field contains configuration that's forwarded to the
underlying inference engine. Currently, only the `vLLM` engine is supported for sharding, so
the `args` field should conform to the [`remote.VLLMShardArgs`](../../../api-reference/union-sdk/packages/union.remote#unionremotevllmshardargs) dataclass.

### Cache the Sharded Model

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
    --domain development
```

Let's break down each input to the command:

- `unsloth/Llama-3.3-70B-Instruct`: The HuggingFace model repository to download from
- `--hf-token-key HUGGINGFACE_TOKEN`: References a Union secret containing your HuggingFace API token for authentication
- `--union-api-key EAGER_API_KEY`: References a Union secret containing API key with admin permissions
- `--artifact-name llama-3-3-70b-instruct-sharded`: Custom name for the cached model artifact
- `--cpu 36`: Allocates 36 CPU cores for the download and sharding process
- `--gpu 4`: Allocates 4 GPUs for model sharding
- `--mem 300Gi`: Allocates 300GB of memory for the process
- `--ephemeral-storage 300Gi`: Allocates 300GB of temporary storage for downloading
- `--accelerator nvidia-l40s`: Specifies NVIDIA L40S GPUs
- `--shard-config shard_config.yaml`: Points to the YAML file containing sharding configuration
- `--project flytesnacks`: The Union project to store the artifact in
- `--domain development`: The domain within the project (defaults to "development")

The large resource allocations (CPU, GPU, memory, storage) are necessary due to the size of the 70B parameter model
being loaded into memory and sharded into the 4 GPUs that will be used for inference.


## Configuring the appropriate compute resources

The `union cache model-from-hf` command exposes five flags to configure the
compute resources used for caching the model.

- `--cpu`: Number of CPU cores to use for the caching process
- `--gpu`: Number of GPUs to use for the caching process
- `--mem`: Amount of memory to use for the caching process
- `--ephemeral-storage`: Amount of temporary storage to use for the caching process
- `--accelerator`: The accelerator to use for the caching process

### When caching models as-is

When caching models as-is, the important flag to consider is `--ephemeral-storage`,
since the model weights are downloaded to disk and then directly serialized into
Union's data storage as an Artifact. For example, if you're caching a 1GB model,
you should allocate at least 1GB of ephemeral storage.

### When caching sharded models

When sharding models, it's important to know ahead of time what accelerator and
how many you need to provision at inference time. Therefore, it's critical that
the compute-related flags that you pass into `union cache model-from-hf` the
compute resources specified by the serving app that is consuming the cached model.

The page for [deploying optimized LLM endpoints with SGlang and vLLM](./deploy-optimized-llm-endpoints) provides a guide for setting up the correct
configurations for the model caching step and the downstream inference app.
