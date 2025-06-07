---
title: Setting up a production project
weight: 5
variants: +flyte +serverless +byoc +selfmanaged
---

# Setting up a production project

In {{< key product_name >}}, your work is organized in a hierarchy with the following structure:

{{< variant serverless >}}
{{< markdown >}}

* **Account**: Your account on {{< key product_name >}}, tied to your GitHub identity.
* **Domains**: Within your account there are three domains, `development`, `staging`, and `production`, used to organize your code during the development process.
* **Projects**: Orthogonal to domains, projects are used to organize your code into logical groups. You can create as many projects as you need.

A given workflow will reside in a specific project. For example, let's say `my_workflow` is a workflow in `my_project`.

When you start working on `my_workflow` you would typically register it in the project-domain `my_project/development`.

As you work on successive iterations of the workflow you might promote `my_workflow` to `my_project/staging` and eventually  `my_project/production`.

Promotion is done simply by [re-registering the workflow to the new project-domain](./running-your-code).

{{< /markdown >}}
{{< /variant >}}
{{< variant byoc selfmanaged flyte >}}
{{< markdown >}}

* **Organization**: Your {{< key product_name >}} instance, accessible at a specific URL like `{{< key product >}}.my-company.com`.
* **Domains** Within an organization there are (typically) three domains, `development`, `staging`, and `production`, used to organize your code during the development process.
You can configure a custom set of domains to suit your needs during [onboarding](../../deployment/configuring-your-data-plane).
* **Projects**: Orthogonal to domains, projects are used to organize your code into logical groups. You can create as many projects as you need.

A given workflow will reside in a specific project. For example, let's say `my_workflow` is a workflow in `my_project`.

When you start work on `my_workflow` you would typically register it in the project-domain `my_project/development`.

As you work on successive iterations of the workflow you might promote `my_workflow` to `my_project/staging` and eventually `my_project/production`.

Promotion is done simply by [re-registering the workflow to the new project-domain](./running-your-code).

{{< /markdown >}}
{{< /variant >}}

## Terminology

In everyday use, the term "project" is often used to refer to not just the {{< key product_name >}} entity that holds a set of workflows,
but also to the local directory in which you are developing those workflows, and to the GitHub (or other SCM) repository that you are using to store the same workflow code.

To avoid confusion, in this guide we will stick to the following naming conventions:

* **{{< key product_name >}} project**: The entity in your {{< key product_name >}} instance that holds a set of workflows, as described above. Often referred to simply as a **project**.
* **Local project**: The local directory (usually the working directory of a GitHub repository) in which you are developing workflows.

## Create a {{< key product_name >}} project

{{< variant flyte >}}
{{< markdown >}}

Ensure that you have [`flytectl` CLI installed](../getting-started/local-setup#install-flytectl-to-set-up-a-local-cluster) and the connection to your Flyte cluster [properly configured](../getting-started/local-setup#configure-the-connection-to-your-flyte-instance).
Now, create a new project on your Flyte cluster:

```shell
$ flytectl create project \
      --id "my-project" \
      --labels "my-label=my-project" \
      --description "My Flyte project" \
      --name "My project"
```

{{< /markdown >}}
{{< /variant >}}
{{< variant serverless byoc selfmanaged >}}
{{< markdown >}}

You can create a new project in the {{< key product_name >}} UI by clicking on the project breadcrumb at the top left and selecting **All projects**:

![Select all projects](../../_static/images/user-guide/development-cycle/setting-up-a-project/select-all-projects.png)

This will take you to the **Projects list**:

![Projects list](../../_static/images/user-guide/development-cycle/setting-up-a-project/projects-list.png)

Click on the **New Project** button and fill in the details for your new project.

You now have a project on {{< key product_name >}} into which you can register your workflows.
The next step is to set up a local workflow directory.

{{< /markdown >}}
{{< /variant >}}

## Creating a local production project directory using `{{< key cli >}} init`

Earlier, in the [Getting started](../getting-started/_index) section we used `{{< key cli >}} init`
to create a new local project based on the `{{< key product>}}-simple`.

Here, we will do the same, but use the `{{< key product>}}-production` template. Perform the following command:

```shell
$ {{< key cli >}} init --template union-production my-project
```

## Directory structure

In the `basic-example` directory you’ll see the following file structure:

```shell
├── LICENSE
├── README.md
├── docs
│   └── docs.md
├── pyproject.toml
├── src
│   ├── core
│   │   ├── __init__.py
│   │   └── core.py
│   ├── orchestration
│   │   ├── __init__.py
│   │   └── orchestration.py
│   ├── tasks
│   │   ├── __init__.py
│   │   └── say_hello.py
│   └── workflows
│       ├── __init__.py
│       └── hello_world.py
└── uv.lock
```

You can create your own conventions and file structure for your production projects, but this tempkate provides a good starting point.

However, the separate `workflows` subdirectory and the contained `__init__.py` file are significant.
We will discuss them when we cover the [registration process](./running-your-code).
