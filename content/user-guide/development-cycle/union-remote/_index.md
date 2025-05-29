---
title: UnionRemote
weight: 21
variants: -flyte +serverless +byoc +selfmanaged
sidebar_expanded: false
---

# {{< key kit_remote >}}

The `{{< key kit_remote >}}` Python API supports functionality similar to that of the {{< key cli_name >}} CLI, enabling you to manage {{< key product_name >}} workflows, tasks, launch plans and artifacts from within your Python code.

> [!NOTE]
> The primary use case of `{{< key kit_remote >}}` is to automate the deployment of {{< key product_name >}} entities. As such, it is intended for use within scripts *external* to actual {{< key product_name >}} workflow and task code, for example CI/CD pipeline scripts.
>
> In other words: _Do not use `{{< key kit_remote >}}` within task code._

## Creating a `{{< key kit_remote >}}` object

Ensure that you have the {{<key kit_name >}} SDK installed, import the `{{< key kit_remote >}}` class and create the object like this:

```python
from {{< key cli >}} import {{< key kit_remote >}}

remote = {{< key kit_remote >}}()
```

By default, when created with a no-argument constructor, `{{< key kit_remote >}}` will use the prevailing configuration in the local environment to connect to {{< key product_name >}}, that is, the same configuration as would be used by the {{< key cli_name >}} CLI in that environment (see [{{< key cli_name >}} CLI configuration search path](../../../api-reference/union-cli#-key-cli--cli-configuration-search-path)).

In the default case, as with the {{< key cli_name >}} CLI, all operations will be applied to the default project, `{{< key default_project >}}` and default domain, `development`.

{{< variant byoc selfmanaged flyte >}}
{{< markdown >}}

Alternatively, you can initialize `{{< key kit_remote >}}` by explicitly specifying a `flytekit.configuration.Config` object with connection information to a {{< key product_name >}} instance, a project, and a domain. Additionall, the constructor supports specifying a file upload location (equivalent to a default raw data prefix):

```python
from {{< key cli >}} import {{< key kit_remote >}}
from flytekit.configuration import Config

remote = {{< key kit_remote >}}(
    config=Config.for_endpoint(endpoint="union.example.com"),
    default_project="my-project",
    default_domain="my-domain",
    data_upload_location="<s3|gs|abs>://my-bucket/my-prefix",
)
```

Here we use the `Config.for_endpoint` method to specify the URL to connect to.
There are number of other ways to configure the `Config` object.
In general, you have all the same options as you would when specifying a connection for the {{< key cli_name >}} CLI using a `config.yaml` file.

### Authenticating using a client secret

In some cases, you may be running a script with `{{< key kit_remote >}}` in a CI/CD pipeline or via SSH, where you don't have access to a browser for the default authentication flow. In such scenarios, you can use the [client secret](../../development-cycle/authentication#3-clientsecret-best-for-cicd-and-automation) authentication method to establish a connection to {{< key product_name >}}. After [creating an API key](../managing-api-keys), you can initialize `{{< key kit_remote >}}` as follows:

```python
from {{< key cli >}} import {{< key kit_remote >}}
from flytekit.configuration import Config, PlatformConfig

remote = {{< key kit_remote >}}(
        config=Config(
            platform=PlatformConfig(
                endpoint="union.example.com",
                insecure=False,
                client_id="<your-client-id>",  # this is the api-key name
                client_credentials_secret="<your-client-secret>",  # this is the api-key
                auth_mode="client_credentials",
            )
        ),
    )
```


For details see [the API docs for `flytekit.configuration.Config`](../../../api-reference/flytekit-sdk/packages/flytekit.configuration#flytekitconfigurationconfig)

{{< /markdown >}}
{{< /variant >}}
{{< variant serverless >}}
{{< markdown >}}

Alternatively, you can initialize `{{< key kit_remote >}}` by explicitly specifying a project, and a domain:

```python
from {{< key cli >}} import {{< key kit_remote >}}

remote = {{< key kit_remote >}}(
    default_project="my-project",
    default_domain="my-domain",
)
```

{{< /markdown >}}
{{< /variant >}}

