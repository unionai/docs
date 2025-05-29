---
title: ImageSpec with ACR
weight: 4
variants: +flyte -serverless +byoc +selfmanaged
---

# ImageSpec with ACR

In this section we explain how to use [Azure Container Registry (ACR)](https://azure.microsoft.com/en-us/products/container-registry) to build and deploy task container images using `ImageSpec`.

Before proceeding, make sure that you have [enabled Azure Container Registry](../../../integrations/enabling-azure-resources/enabling-azure-container-registry) for you {{< key product_name >}} installation.

## Authenticate to the registry

Authenticate with the container registry

```bash
az login
az acr login --name <acrName>
```

Refer to [Individual login with Microsoft Entra ID](https://learn.microsoft.com/en-us/azure/container-registry/container-registry-authentication?tabs=azure-cli#individual-login-with-microsoft-entra-id) in the Azure documentation for additional details.

## Register your workflow to {{< key product_name >}}

You can now register tasks with `ImageSpec` declarations that reference this repository.

For example, to use an existing ACR repository, we would alter the Python code in the [previous section](.), to have the following `ImageSpec` declaration:

```python
image_spec = union.ImageSpec(
    registry="<AZURE_CONTAINER_REGISTRY_NAME>.azurecr.io",
    name="my-repository/simple-example-image",
    base_image="ghcr.io/flyteorg/flytekit:py3.11-latest",
    requirements="image-requirements.txt"
)
```

