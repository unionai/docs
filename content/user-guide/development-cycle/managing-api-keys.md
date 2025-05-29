---
title: Managing API keys
weight: 15
variants: -flyte +serverless +byoc +selfmanaged
---

# Managing API keys

You need to create an API key to allow external systems to run compute
on {{< key product_name >}}, e.g. a GitHub action that registers or runs workflows.

## Creating an API key

To create an API key, run the following with the {{< key cli_name >}} CLI with any name.

```shell
$ {{< key cli >}} create api-key admin --name my-custom-name

Client ID: my-custom-name
The following API key will only be shown once. Be sure to keep it safe!
Configure your headless CLI by setting the following environment variable:

export {{< key env_prefix >}}_API_KEY="<SECRET>"
```

Store the `<SECRET>` in a secure location. For `git` development, make sure to not check in the `<SECRET>` into your repository.
Within a GitHub action, you can use [Github Secrets](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions) to store the secret.

For this example, copy the following workflow into a file called `hello.py`:

```python
import {{< key kit_import >}}

@{{< key kit_as >}}.task
def welcome(name: str) -> str:
    return f"Welcome to {{< key product_name >}}! {name}"

@{{< key kit_as >}}.workflow
def main(name: str) -> str:
    return welcome(name=name)
```

You can run this workflow from any machine by setting the `{{< key env_prefix >}}_API_KEY`
environment variable:

```shell
$ export {{< key env_prefix >}}_API_KEY="<SECRET>"
$ {{< key cli >}} run --remote hello.py main --name "{{< key product_name >}}"
```

## Listing and deleting applications

You can list all your application by running:

```shell
$ {{< key cli >}} get api-key admin
```

```shell
┏━━━━━━━━━━━━━━━━┓
┃ client_id      ┃
┡━━━━━━━━━━━━━━━━┩
│ my-custom-name │
└────────────────┘
```

The `client_id` contains your custom application name and a prefix that contains your
username.

Finally, you can delete your application by running:

```shell
$ {{< key cli >}} delete api-key admin --name my-custom-name
```
