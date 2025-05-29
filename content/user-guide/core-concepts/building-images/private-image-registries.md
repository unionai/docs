---
title: Private image registries
weight: 3
variants: +flyte +serverless +byoc +selfmanaged
---

# Private image registries

The images used by your {{< key product_name >}} tasks must be stored in a container registry from which {{< key product_name >}} will pull it when it spins up the container for a task execution.
The key constraint here is that the registry, and the image itself, must be read-accessible to your {{< key product_name >}} cluster, in order for the image pull to succeed.

{{< variant serverless byoc selfmanaged >}}
{{< markdown >}}

So far, we have discussed two options:

* Using the built-in {{< key product_name >}} [Cloud image builder]() (by specifying the `ImageSpec` parameter `builder="union"`) which pushes the image to the {{< key product_name >}} internal container registry.
  * Since the registry is built into {{< key product_name >}}, it is automatically accessible to your {{< key product_name >}} cluster.
* Building your image on your local machine (by specifying the `ImageSpec` parameter `builder="default"`) and pushing the image to  a public registry (like the GitHub Packages registry) (by specifying the `ImageSpec` parameter `registry`).
  * In this case the image is accessible to your {{< key product_name >}} cluster because it is public.

If you want to keep your images private, clearly the public registry option will not work.
The internal {{< key product_name >}} registry is private, so that is an option is you are concerned only with keeping your images non-public.

However, there may be cases where you want to keep your images both *private*, and *in you own registry*.
In that case, you will need to set up your {{< key product_name >}} cluster with the correct credentials to be able to pull the images from that private registry.

{{< /markdown >}}
{{< /variant >}}

{{< variant flyte >}}
{{< markdown >}}

We have discussed building your image on your local machine (by specifying the `ImageSpec` parameter `builder="default"`) and pushing the image to a public registry (like the GitHub Packages registry) (by specifying the `ImageSpec` parameter `registry`). In this case the image is accessible to your {{< key product_name >}} cluster because it is public.

However, if you want to **keep your images private**, clearly the public registry option will not work.
You will need to set up your {{< key product_name >}} cluster with the correct credentials to be able to pull the images from a private registry.


You can use different private container registries to host your images, such as AWS ECR, Docker Hub, GitLab Container Registry, and GitHub Container Registry.

To pull private images, ensure that you have the command line tools and login information associated with the registry.

## Create a secret

First create a secret that contains all the credentials needed to log into the registry.

## Configure `imagePullSecrets`

Then, you’ll need to specify an `imagePullSecrets` configuration to pull a private image using one of two methods below.

### Service Account

You can use the default or new service account for this option:

1. Add your `imagePullSecrets` configuration to the service account.

2. Use this service account to log into the private registry and pull the image.

3. When you create a task/workflow execution this service account should be specified.

### Custom Pod Template

This option uses a custom pod template to create a pod.
This template is automatically added to every pod that Flyte creates.

1. Add your `imagePullSecrets` configuration to the custom pod template.

2. Update FlytePropeller about the pod created in the previous step.

3. FlytePropeller adds `imagePullSecrets`, along with other customization for the pod, to the `PodSpec`, which should look similar to this manifest.

The pods with their keys can log in and access the images in the private registry. Once you set up the token to authenticate with the private registry, you can pull images from them.

{{< /markdown >}}
{{< /variant >}}
