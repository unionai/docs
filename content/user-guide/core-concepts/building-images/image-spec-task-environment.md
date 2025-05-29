---
title: Local image building
weight: 1
variants: +flyte -serverless +byoc +selfmanaged
---

# Local image building

With {{< key product_name >}}, every task in a workflow runs within its own dedicated container.
Since a container requires a container image to run, every task in {{< key product_name >}} must have a container image associated with it.
You can specify the container image to be used by a task by defining an `ImageSpec` object and passing it to the `container_image` parameter of the `@{{< key kit_as >}}.task` decorator.
When you register the workflow, the container image is built locally and pushed to the container registry that you specify.
When the workflow is executed, the container image is pulled from that registry and used to run the task.

> [!NOTE]
> See the [ImageSpec API documentation]() for full documentation of `ImageSpec` class parameters and methods.
<!-- TODO: Add link to API -->

To illustrate the process, we will walk through an example.

## Project structure

```shell
├── requirements.txt
└── workflows
    ├── __init__.py
    └── imagespec-simple-example.py
```

### requirements.txt

```shell
union
pandas
```

### imagespec-simple-example.py

```python
import typing
import pandas as pd
import {{< key kit_import >}}

image_spec = union.ImageSpec(
    registry="ghcr.io/<my-github-org>",
    name="simple-example-image",
    base_image="ghcr.io/flyteorg/flytekit:py3.11-latest",
    requirements="requirements.txt"
)

@{{< key kit_as >}}.task(container_image=image_spec)
def get_pandas_dataframe() -> typing.Tuple[pd.DataFrame, pd.Series]:
    df = pd.read_csv("https://storage.googleapis.com/download.tensorflow.org/data/heart.csv")
    print(df.head())
    return df[["age", "thalach", "trestbps", "chol", "oldpeak"]], df.pop("target")

@{{< key kit_as >}}.workflow()
def wf() -> typing.Tuple[pd.DataFrame, pd.Series]:
    return get_pandas_dataframe()
```

## Install and configure `{{< key cli >}}` and Docker

To install Docker, see [Setting up container image handling](../../../getting-started/local-setup#install-docker-and-get-access-to-a-container-registry).
To configure `{{< key cli >}}` to connect to your {{< key product_name >}} instance, see [Getting started](../../../getting-started/_index).

## Set up an image registry

You will need an image registry where the container image can be stored and pulled by {{< key product_name >}} when the task is executed.
You can use any image registry that you have access to, including public registries like Docker Hub or GitHub Container Registry.
Alternatively, you can use a registry that is part of your organization's infrastructure such as AWS Elastic Container Registry (ECR) or Google Artifact Registry (GAR).

The registry that you choose must be one that is accessible to the {{< key product_name >}} instance where the workflow will be executed.
Additionally, you will need to ensure that the specific image, once pushed to the registry, is itself publicly accessible.

In this example, we use GitHub's `ghcr.io` container registry.
See [Working with the Container registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry) for more information.

{{< variant byoc selfmanaged serverless >}}
{{< markdown >}}

* For an example using Amazon ECR see [ImageSpec with ECR](./image-spec-with-ecr).
* For an example using Google Artifact Registry see [ImageSpec with GAR](./image-spec-with-gar).
* For an example using Azure Container Registry see [ImageSpec with ACR](./image-spec-with-acr).

{{< /markdown >}}
{{< /variant >}}

## Authenticate to the registry

You will need to set up your local Docker client to authenticate with GHCR. This is needed for `{{< key cli >}}` CLI to be able to push the image built according to the `ImageSpec` to GHCR.

Follow the directions [Working with the Container registry > Authenticating to the Container registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry#authenticating-to-the-container-registry).

## Set up your project and domain on {{< key product_name >}}

You will need to set up a project on your {{< key product_name >}} instance to which you can register your workflow.
See [Setting up the project](../../../development-cycle/setting-up-a-project).

## Understand the requirements

The `requirements.txt` file contains the `{{< key kit >}}` package and the `pandas` package, both of which are needed by the task.

## Set up a virtual Python environment

Set up a virtual Python environment and install the dependencies defined in the `requirements.txt` file.
Assuming you are in the local project root, run `pip install -r requirements.txt`.

## Run the workflow locally

You can now run the workflow locally.
In the project root directory, run: `{{< key cli >}} run workflows/imagespec-simple-example.py wf`.
See [Running your code](../../../development-cycle/running-your-code) for more details.

> [!NOTE]
> When you run the workflow in your local Python environment, the image is not built or pushed (in fact, no container image is used at all).

## Register the workflow

To register the workflow to {{< key product_name >}}, in the local project root, run:

```shell
$ {{< key cli >}} register workflows/imagespec-simple-example.py
```

`{{< key cli >}}` will build the container image and push it to the registry that you specified in the `ImageSpec` object.
It will then register the workflow to {{< key product_name >}}.

To see the registered workflow, go to the UI and navigate to the project and domain that you created above.

## Ensure that the image is publicly accessible

If you are using the `ghcr.io` image registry, you must switch the visibility of your container image to Public before you can run your workflow on {{< key product_name >}}.
See [Configuring a package's access control and visibility](https://docs.github.com/en/packages/learn-github-packages/configuring-a-packages-access-control-and-visibility#about-inheritance-of-access-permissions-and-visibility).

## Run the workflow on {{< key product_name >}}

Assuming your image is publicly accessible, you can now run the workflow on {{< key product_name >}} by clicking **Launch Workflow**.

> [!WARNING] Make sure your image is accessible
> If you try to run a workflow that uses a private container image or an image that is inaccessible for some other reason, the system will return an error:
>
> ```
> ... Failed to pull image ...
> ... Error: ErrImagePull
> ... Back-off pulling image ...
> ... Error: ImagePullBackOff
> ```

## Multi-image workflows

You can also specify different images per task within the same workflow.
This is particularly useful if some tasks in your workflow have a different set of dependencies where most of the other tasks can use another image.

In this example we specify two tasks: one that uses CPUs and another that uses GPUs.
For the former task, we use the default image that ships with {{< key kit >}} while for the latter task, we specify a pre-built image that enables distributed training with the Kubeflow Pytorch integration.

```python
import numpy as np
import torch.nn as nn

@task(
    requests=Resources(cpu="2", mem="16Gi"),
    container_image="ghcr.io/flyteorg/flytekit:py3.9-latest",
)
def get_data() -> Tuple[np.ndarray, np.ndarray]:
    ...  # get dataset as numpy ndarrays


@task(
    requests=Resources(cpu="4", gpu="1", mem="16Gi"),
    container_image="ghcr.io/flyteorg/flytecookbook:kfpytorch-latest",
)
def train_model(features: np.ndarray, target: np.ndarray) -> nn.Module:
    ...  # train a model using gpus
```
