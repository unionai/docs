---
title: Authentication
weight: 1
variants: -flyte -serverless +byoc +selfmanaged
---

# Authentication

Authentication is required to interact with {{< key product_name >}} using the command-line interface (CLI). The authentication method depends on whether you are working on a local or remote machine. This guide walks you through different authentication mechanisms and helps you choose the best one for your use case.

Before diving into authentication, ensure you have installed the {{< key cli_name >}} CLI. See [Local Setup](../getting-started/local-setup) for details.

## Authentication Methods

{{< key cli_name >}} CLI supports three authentication mechanisms:

| Authentication Method | Works on Local? | Works on Remote? | Use Case                                                        |
|-----------------------|-----------------|------------------|-----------------------------------------------------------------|
| PKCE (default)        | ✅ Yes          | ❌ No            | Best on local machines with a browser.                          |
| DeviceFlow            | ✅ Yes          | ✅ Yes           | Best on remote machines without a browser, like an ssh session. |
| ClientSecret          | ✅ Yes          | ✅ Yes           | Best for CI/CD or automation.                                   |

> [!NOTE]
> If you used `{{< key cli >}} create login --host <union-host-url>`, this used PKCE by default.

## 1. PKCE (Proof Key of Code Exchange)

PKCE is the default authentication method. When you run a {{< key cli_name >}} CLI command, it opens a browser window for authentication.

Authentication Flow:
- Run a {{< key cli_name >}} CLI command.
- You are redirected to your default browser and log in.

Example Configuration:
```yaml
admin:
  endpoint: https://<YourOrg>.hosted.unionai.cloud
  insecure: false
  authType: Pkce
logger:
  show-source: true
  level: 0
```

> [!NOTE]
> PKCE requires a local browser, making it unsuitable for using the {{< key cli_name >}} CLI on remote machines within an ssh session.

## 2. DeviceFlow (Best for Remote Machines)

If you are working with the {{< key cli_name >}} CLI on a remote machine without a browser, use DeviceFlow. This method provides a URL that you can open in your local browser.

Authentication Flow:
- Run a {{< key cli_name >}} CLI command.
- The CLI returns a URL.
- Open the URL in your local browser and log in.

Example Configuration:
```
admin:
  endpoint: dns:///<YourOrg>.hosted.unionai.cloud
  insecure: false
  authType: DeviceFlow
logger:
  show-source: true
  level: 0
```
> [!NOTE]
> During authentication, {{< key product_name >}} attempts to store an authentication token on the keyring service of the operating system. If you are authenticating from within an SSH session on a Linux based machine, there may not be a keyring service by default. If you find that browser based authentication is required every time you run or register your workflows, you may need to `run pip install keyring` or `pip install keyrings.alt` to install a keyring service on your machine.

## 3. ClientSecret (Best for CI/CD and Automation)

The ClientSecret method is a headless authentication option, ideal for automation and CI/CD pipelines.

Steps to Set Up ClientSecret Authentication:

1. Create an API Key:
    ```
    $ {{< key cli >}} create api-key admin --name my-custom-name
    ```
    The output provides a Client ID and API Key. Store the API Key securely, as it will not be shown again.

2. Set the Environment Variable:
    ```
    export {{< key env_prefix >}}_API_KEY="<SECRET>"
    ```
   With this environment variable set, `{{< key cli >}}` and `uctl` commands do not require a configuration yaml to be referenced.

> [!NOTE]
> Never commit API keys to version control. Use environment variables or a secure vault.

## Managing Authentication Configuration

By default, the {{< key cli_name >}} CLI looks for configuration files in `~/.{{< key product >}}/config.yaml`. You can override this by:

- Setting the `{{< key config_env >}}` environment variable:
    ```
    export {{< key config_env >}}=~/.my-config-location/my-config.yaml
    ```

- Using the `--config` flag:
    ```
    $ {{< key cli >}} --config ~/.my-config-location/my-config.yaml run my_script.py my_workflow
    ```

## Troubleshooting Authentication Issues

{{< variant byoc selfmanaged serverless >}}
{{< markdown >}}
- Old configuration files causing conflicts? Remove the deprecated directory from `~/.unionai/`.
{{< /markdown >}}
{{< /variant >}}

- Need to switch authentication methods? Update `~/.{{< key product >}}/config.yaml` or use a different config file.

- Getting prompted for login every time? If using DeviceFlow on Linux, install a `keyring` service (`pip install keyring keyrings.alt`).