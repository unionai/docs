---
title: Managing secrets
weight: 14
variants: -flyte +serverless +byoc +selfmanaged
---

# Managing secrets

You can use secrets to interact with external services.

## Creating secrets

### Creating a secret on the command line

To create a secret, use the `{{< key cli >}} create secret` command:

```shell
$ {{< key cli >}} create secret --project my_project --domain my_domain my_secret
```

You'll be prompted to enter a secret value in the terminal:

```
Enter secret value: ...
```

### Creating a secret from a file

To create a secret from a file, run the following command:

```shell
$ {{< key cli >}} create secret --project my_project --domain my_domain my_file_secret -f /path/to/file
```

## Listing secrets

You can list existing secrets with the `{{< key cli >}} get secret` command:

```shell
$ {{< key cli >}} get secret --project my_project --domain my_domain
```

## Using secrets in workflow code

Note that secrets are stored per project/domain pair.
A workflow can only access secrets created within its own project and domain.

### Using a secret created on the command line

To use a secret created on the command line, see the example code below. To run the example code:

1. [Create a secret on the command line](#creating-a-secret-on-the-command-line) with the key `my_secret`.
2. Copy the following example code to a new file and save it as `using_secrets.py`.
3. Run the script with `{{< key cli >}} run --remote using_secrets.py main`.


```python
import {{< key kit_import >}}

@{{< key kit_as >}}.task(secret_requests=[union.Secret(key="my_secret")])
def t1():
    secret_value = union.current_context().secrets.get(key="my_secret")
    # do something with the secret. For example, communication with an external API.
    ...
```

> [!WARNING]
> Do not return secret values from tasks, as this will expose secrets to the control plane.

With `env_var`, you can automatically load the secret into the environment. This is useful
with libraries that expect the secret to have a specific name:

```python
import {{< key kit_import >}}

@{{< key kit_as >}}.task(secret_requests=[union.Secret(key="my_union_api_key", env_var="{{< key env_prefix >}}_API_KEY")])
def t1():
    # Authenticates the remote with {{< key env_prefix >}}_API_KEY
    remote = union.{{< key kit_remote >}}(default_project="{{< key default_project >}}", default_domain="development")
```

### Using a secret created from a file

To use a secret created from a file in your workflow code, you must mount it as a file. To run the example code below:

1. [Create a secret from a file](#creating-a-secret-from-a-file) with the key `my_secret`.
2. Copy the example code below to a new file and save it as `using_secrets_file.py`.
4. Run the script with `{{< key cli >}} run --remote using_secrets_file.py main`.


```python
import {{< key kit_import >}}

@{{< key kit_as >}}.task(
    secret_requests=[
        {{< key kit_as >}}.Secret(key="my_file_secret", mount_requirement={{< key kit_as >}}.Secret.MountType.FILE),
    ]
)
def t1():
    path_to_secret_file = union.current_context().secrets.get_secrets_file("my_file_secret")
    with open(path_to_secret_file, "r") as f:
        secret_value = f.read()
    # do something with the secret. For example, communication with an external API.
    ...
```

> [!WARNING]
> Do not return secret values from tasks, as this will expose secrets to the control plane.


> [!NOTE]
> The `get_secrets_file` method takes the secret key and returns the path to the secret file.

## Updating secrets

To update a secret, run the `{{< key cli >}} update secret` command. You will be prompted to enter a new value:

```shell
$ {{< key cli >}} update secret --project my_project --domain my_domain my_secret
```

## Deleting secrets

To delete a secret, use the `{{< key cli >}} delete secret` command:

```shell
$ {{< key cli >}} delete secret --project my_project --domain my_domain my_secret
```
