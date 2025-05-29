---
title: ImageSpec with GAR
weight: 3
variants: +flyte -serverless +byoc +selfmanaged
---

# ImageSpec with GAR

In this section we explain how to set up and use Google Artifact Registry (GAR) to build and deploy task container images using `ImageSpec`.


{{< variant byoc selfmanaged >}}
{{< markdown >}}

## Prerequisites

If you are using GAR in the same Google Cloud Platform (GCP) project as your {{< key product_name >}} data plane, then you do not need to configure anything.
Access to GAR in the same project is enabled by default.

If you want to store your task container images in a GAR repository in a GCP project _other than the one that holds your data plane_, you must enable the node pool of your data plane to access that GAR.
See [Enable Google Artifact Registry](../../../integrations/enabling-gcp-resources/enabling-google-artifact-registry) for details.

{{< /markdown >}}
{{< /variant >}}

## Set up the image repository

Unlike GitHub Container Registry, GAR does not allow you to simply push an arbitrarily named image to the registry.
Instead, you must first create a repository in the GAR instance and then push the image to that repository.

> [!NOTE] Registry, repository, and image
> In GAR terminology the **registry** is the top-level storage service. The registry holds a collection of **repositories**.
> Each repository in turn holds some number of images, and each specific image name can have different versions.
>
> Note that this differs from the arrangement in AWS ECR where the repository name and image name are essentially the same.
>
> When you push an image to GAR, you are actually pushing it to an image name within a repository within that registry.
> Strictly speaking, the term *image* refers to a specific *image version* within that repository.

This means that you have to decide on the name of your repository and create it, before registering your workflow. You can, however, decide on the image name later, when you push the image to the repository. We will assume the following:

* The GAR instance you will be using has the base URL `us-east1-docker.pkg.dev/my-union-dataplane/my-registry/`.
* Your repository will be called `my-image-repository`.
* Your image will be called `simple-example-image`.

{{< variant byoc selfmanaged >}}
{{< markdown >}}

In the GCP console, within your {{< key product_name >}} data plane project, go to **Artifact Registry**. You should see a list of repositories. The existing ones are used internally by {{< key product_name >}}. For your own work you should create a new one. Click **Create Repository**:

{{< /markdown >}}
{{< /variant >}}
{{< variant flyte >}}
{{< markdown >}}

In the GCP console, within the same project as your Flyte installation, go to **Artifact Registry**. Create a new one by clicking **Create Repository**:

{{< /markdown >}}
{{< /variant >}}

![](/_static/images/user-guide/core-concepts/tasks/task-software-environment/imagespec-with-gar/gar-create-repository-1.png)

On the **Create repository** page,

* Enter the name of the repository. In this example it would be `my-image-repository`.
* Select **Docker** for the artifact type.

{{< variant byoc selfmanaged >}}
{{< markdown >}}

* Select the region. If you want to access the GAR without further configuration, make sure this the same region as your {{< key product_name >}} data plane.

{{< /markdown >}}
{{< /variant >}}
{{< variant flyte>}}
{{< markdown >}}

* Select the region. If you want to access the GAR without further configuration, make sure this the same region as your Flyte cluster.

{{< /markdown >}}
{{< /variant >}}

* Click **Create**:

![](/_static/images/user-guide/core-concepts/tasks/task-software-environment/imagespec-with-gar/gar-create-repository-2.png)

Your GAR repository is now created.

## Authenticate to the registry

You will need to set up your local Docker client to authenticate with GAR. This is needed for `{{< key cli >}}` to be able to push the image built according to the `ImageSpec` to GAR.

Directions can be found in the GAR console interface. Click on **Setup Instructions**:

![](/_static/images/user-guide/core-concepts/tasks/task-software-environment/imagespec-with-gar/gar-setup-instructions.png)

The directions are also reproduced below. (We show the directions for the `us-east1` region. You may need to adjust the command accordingly):

> [!NOTE] Setup Instructions
> Follow the steps below to configure your client to push and pull packages using this repository.
> You can also [view more detailed instructions here](https://cloud.google.com/artifact-registry/docs/docker/authentication?authuser=1).
> For more information about working with artifacts in this repository, see the [documentation](https://cloud.google.com/artifact-registry/docs/docker?authuser=1).
>
> **Initialize gcloud**
>
> The [Google Cloud SDK](https://cloud.google.com/sdk/docs/?authuser=1) is used to generate an access token when authenticating with Artifact Registry.
> Make sure that it is installed and initialized with [Application Default Credentials](https://cloud.google.com/sdk/gcloud/reference/auth/application-default/login?authuser=1) before proceeding.
>
> **Configure Docker**
>
> Run the following command to configure `gcloud` as the credential helper for the Artifact Registry domain associated with this repository's location:
>
> ```shell
> $ gcloud auth configure-docker us-east1-docker.pkg.dev
> ```

## Register your workflow to {{< key product_name >}}

You can now register tasks with `ImageSpec` declarations that reference this repository.

For example, to use the example GAR repository shown here, we would alter the Python code in the [previous section](.), to have the following `ImageSpec` declaration:

```python
image_spec = union.ImageSpec(
    registry="us-east1-docker.pkg.dev/my-union-dataplane/my-registry/my-image-repository",
    name="simple-example-image",
    base_image="ghcr.io/flyteorg/flytekit:py3.11-latest",
    requirements="image-requirements.txt"
)
```
