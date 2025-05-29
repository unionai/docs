---
title: ImageSpec with ECR
weight: 2
variants: +flyte -serverless +byoc +selfmanaged
---

# ImageSpec with ECR

In this section we explain how to set up and use AWS Elastic Container Registry (ECR) to build and deploy task container images using `ImageSpec`.

{{< variant byoc selfmanaged >}}
{{< markdown >}}

## Prerequisites

If you are using ECR in the same AWS account as your {{< key product_name >}} data plane, then you do not need to configure anything. Access to ECR in the same account is enabled by default.

If you want to store your task container images in an ECR instance in an AWS account _other than the one that holds your data plane_, then you will have to configure that ECR instance to permit access from your data plane. See [Enable AWS ECR](../../../integrations/enabling-aws-resources/enabling-aws-ecr) for details.

{{< /markdown >}}
{{< /variant >}}

## Set up the image repository

Unlike GitHub Container Registry, ECR does not allow you to simply push an arbitrarily named image to the registry. Instead, you must first create a repository in the ECR instance and then push the image to that repository.

> [!NOTE] Registry, repository, and image
> In ECR terminology the **registry** is the top-level storage service. The registry holds a collection of **repositories**.
> Each repository corresponds to a named image and holds all versions of that image.
>
> When you push an image to a registry, you are actually pushing it to a repository within that registry.
> Strictly speaking, the term *image* refers to a specific *image version* within that repository.

This means that you have to decide on the name of your image and create a repository by that name first, before registering your workflow. We will assume the following:

* The ECR instance you will be using has the base URL `123456789012.dkr.ecr.us-east-1.amazonaws.com`.

* Your image will be called `simple-example-image`.

In the AWS console, go to **Amazon ECR > Repositories** and find the correct ECR registry

{{< variant byoc selfmanaged >}}
{{< markdown >}}

If you are in the same account as your {{< key product_name >}} data plane you should go directly to the ECR registry that was set up for you by {{< key product_name >}}. If there are multiple ECR registries present, consult with your {{< key product_name >}} administrator to find out which one to use.

{{< /markdown >}}
{{< /variant >}}

Under **Create a Repository**, click **Get Started**:

![](/_static/images/user-guide/core-concepts/tasks/task-software-environment/imagespec-with-ecr/create-repository-1.png)

On the **Create repository** page:

* Select **Private** for the repository visibility, assuming you want to make it private. You can, alternatively, select **Public**, but in most cases, the main reason for using ECR is to keep your images private.

* Enter the name of the repository:

![](/_static/images/user-guide/core-concepts/tasks/task-software-environment/imagespec-with-ecr/create-repository-2.png)

and then scroll down to click **Create repository**:

![](/_static/images/user-guide/core-concepts/tasks/task-software-environment/imagespec-with-ecr/create-repository-3.png)

Your repository is now created.

## Authenticate to the registry

You will need to set up your local Docker client to authenticate with ECR. This is needed for `{{< key cli >}}` to be able to push the image built according to the `ImageSpec` to ECR.

To do this, you will need to [install the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html), use it to run the `aws ecr get-login-password` command to get the appropriate password, then perform a `docker login` with that password.

See [Private registry authentication](https://docs.aws.amazon.com/AmazonECR/latest/userguide/registry_auth.html) for details.

## Register your workflow to {{< key product_name >}}

You can register tasks with `ImageSpec` declarations that reference this repository.

For example, to use the example repository shown here, we would alter the Python code in the [previous section](.), to have the following `ImageSpec` declaration:

```python
image_spec = union.ImageSpec(
    registry="123456789012.dkr.ecr.us-eas-1.amazonaws.com",
    name="simple-example-image",
    base_image="ghcr.io/flyteorg/flytekit:py3.11-latest",
    requirements="image-requirements.txt"
)
```
