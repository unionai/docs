---
title: Getting started
weight: 3
sidebar_expanded: true
variants: +flyte +serverless +byoc +selfmanaged
---

# Getting started

This section gives you a quick introduction to writing and running {{< key product_name >}} workflows.

{{< variant serverless >}}
{{< markdown >}}

## Sign up for {{< key product_name >}} Serverless

First, sign up for {{< key product_name >}} Serverless:
{{< /markdown >}}

{{< button-link text="Create an account" target="https://signup.union.ai/" variant="warning" >}}

{{< markdown >}}
Once you've received confirmation that your sign-up succeeded, navigate to
the UI at [serverless.union.ai](https://serverless.union.ai).

To get started, try selecting the default project, called `{{< key default_project >}}`, from the list of projects.
This will take you to `{{< key default_project >}}` project dashboard:

![{{< key product_name >}} UI](../../_static/images/quick-start/serverless-dashboard.png)

## Run your first workflow

Run your first workflow on a {{< key product_name >}} Workspace.
{{< /markdown >}}

{{< dropdown title="Start workspace" icon=arrow_forward >}}
{{< markdown >}}

Select **Workspaces** in the left navigation bar.

Start the default workspace by clicking on the `default` workspace item.

![Start workspace](../../_static/images/quick-start/serverless-workspace-start.png))
{{< /markdown >}}
{{< /dropdown >}}

{{< dropdown title="Open workspace" icon=arrow_forward >}}
{{< markdown >}}

When the `Status` is `Active` on the `default` workspace, you can click on it
again to open the workspace.

_It will take a few moments to load the VSCode interface._

![Open workspace](../../_static/images/quick-start/serverless-workspace-open.png)
:::)

{{< /markdown >}}
{{< /dropdown >}}

{{< dropdown title="Complete walkthrough" icon=arrow_forward >}}
{{< markdown >}}

Once the workspace is open, you should see a VSCode interface in your browser.

![Workspace VSCode](../../_static/images/quick-start/serverless-workspace-vscode.png)

In the walkthrough, you'll learn how to:

1. 🤖 Train a model
2. 🔀 Parallelize model training
3. 📘 Iterate on a Jupyter Notebook

{{< /markdown >}}
{{< /dropdown >}}

{{< dropdown title="Stop workspace" icon=arrow_forward >}}
{{< markdown >}}


The workspace will terminate after 20 minutes of idle time, but you can also
stop it manually on the Workspaces page.

![Open workspace](../../_static/images/quick-start/serverless-workspace-stop.png)

{{< /markdown >}}
{{< /dropdown >}}

{{< markdown class="top-margin" >}}

🎉 Congratulations! You've just run your first workflow on {{< key product_name >}}.

{{< /markdown >}}
{{< /variant >}}

{{< variant byoc selfmanaged >}}
{{< markdown >}}

## Gather your credentials

After your administrator has onboarded you to {{< key product_name >}} (see [Deployment](../../deployment)), you should have the following at hand:

- Your {{< key product_name >}} credentials.
- The URL of your {{< key product_name >}} instance. We will refer to this as `<union-host-url>` below.

## Log into {{< key product_name >}}

Navigate to the UI at `<union-host-url>` and log in with your credentials.
Once you have logged in you should see the {{< key product_name >}} UI.

To get started, try selecting the default project, called `{{< key default_project >}}`, from the list of projects.
This will take you to `{{< key default_project >}}` project dashboard:

![{{< key product_name >}} UI](../../_static/images/quick-start/byoc-dashboard.png)

This dashboard gives you an overview of the workflows and tasks in your project.
Since you are just starting out, it will be empty.
To build and deploy your first workflow, the first step is to [set up your local environment](./local-setup).

{{< /markdown >}}
{{< /variant >}}
{{< variant flyte >}}
{{< markdown >}}

## Try Flyte in your browser

You can try Flyte in your browser without any setup simply by [signing up for **Union.ai Serverless**](https://signup.union.ai/).

[Union.ai Serverless is a fully-hosted version of Flyte]({{< docs_home serverless >}}) with additional features.

## Try Flyte on your local machine

You can also install Flyte's SDK (called `flytekit`) and a local Flyte cluster to run workflows on your local machine.

To get started, follow the instructions on the next page, [Local setup](./local-setup).

{{< /markdown >}}
{{< /variant >}}
