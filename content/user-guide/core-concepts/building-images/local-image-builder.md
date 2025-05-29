---
title: Local image builder
weight: 3
variants: +flyte +serverless +byoc +selfmanaged
---

# Local image builder

When `builder="default"` is specified, {{< key product_name >}} will build the image locally on your machine with `docker` and push it to the registry you specify in the `registry` parameter.
From there it will be pulled and installed in the task container when it spins up.

### Local container engine

To enable local image building you must have an [OCI-compatible](https://opencontainers.org/) container engine, like [Docker](https://docs.docker.com/get-docker/), installed and running locally.
Other options include [Podman](https://podman.io/), [LXD](https://linuxcontainers.org/lxd/introduction/), or [Containerd](https://containerd.io/).

### Accessibility of the container registry and image

When building images locally you will need to specify the URL of the registry in the `registry` parameter of the `ImageSpec`.

The registry you specify must be accessible both to your local machine and to your {{< key product_name >}} cluster:

* Your local machine must be able to *push* the image it builds to the registry.
  * This usually requires authenticating your local docker to the registry by doing a `docker login`. See the example below.
* Your {{< key product_name >}} cluster must be able to *pull* the image from the registry when it spins up a task that uses that image.
  * The most common option here is use a public registry and make the image publicly available. See the example below.

A common choice is to use the GitHub Container Registry (GHCR) that comes as part of your GitHub account.
For more information, see [Working with the Container registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry).

You will still need to set up your local Docker client to authenticate to the registry in order for `{{< key cli >}}` to be able to push the built image.

Follow the directions in [Working with the Container registry > Authenticating to the Container registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry#authenticating-to-the-container-registry).

You may use another container registry if you prefer,
such as [Docker Hub](https://hub.docker.com/),
[Amazon Elastic Container Registry (ECR)](../integrations/enabling-aws-resources/enabling-aws-ecr),
or [Google Artifact Registry (GAR)](../integrations/enabling-gcp-resources/enabling-google-artifact-registry).


### Make your image accessible to {{< key product_name >}}

In addition to making sure your registry is accessible from your local machine, you will need to ensure that the specific image, once pushed to the registry, is itself publicly accessible.

> [!NOTE] Make your image public
> Note that in the case of our example registry (GHCR), making the image public can only be done once the image _has been_ pushed.
> This means that you will need to register your workflow first, then make the image public and then run the workflow from the {{< key product_name >}} UI.
> If you try to run the workflow before making the image public (for example by doing a `{{< key cli >}} run` which both registers and runs immediately)
> the workflow execution will fail with an `ImagePullBackOff `error.

In the GitHub Container Registry, switch the visibility of your container image to Public. For more information, see [Configuring a package's access control and visibility](https://docs.github.com/en/packages/learn-github-packages/configuring-a-packages-access-control-and-visibility#about-inheritance-of-access-permissions-and-visibility).

At this point, you can run the workflow from the {{< key product_name >}} interface.
