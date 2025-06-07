---
title: Running your workflow
weight: 5
variants: +flyte +serverless +byoc +selfmanaged
---

# Running your workflow

## Python virtual environment

The first step is to ensure that your `uv.lock` file is properly generated from your `pyproject.toml` file and that your local Python virtual environment is properly set up.

Using `uv`, you can install the dependencies with the command:

```shell
$ uv sync
```

You can then activate the virtual environment with:

```shell
$ source .venv/bin/activate
```

> [!NOTE] `activate` vs `uv run`
> When running the `{{< key cli >}}` CLI within your local project you must run it in the virtual
> environment _associated with_ that project.
> This differs from our earlier usage of the tool when
> [we installed `{{< key cli >}}` globally](./local-setup#install-the--cli--cli) in order to
> [set up its configuration](./local-setup#configure-the-connection-to-your--product_full--instance).
>
> To run `{{< key cli >}}` within your project's virtual environment using `uv`,
> you can prefix it use the `uv run` command. For example:
>
> `uv run {{< key cli >}} ...`
>
> Alternatively, you can activate the virtual environment with `source .venv/bin/activate` and then
> run the `{{< key cli >}}` command directly.
>
> In our examples we assume that you are doing the latter.

## Run the code locally

Because tasks and workflows are defined as regular Python functions, they can be executed in your local Python environment.

You can run the workflow locally with the command [`{{< key cli >}} run <FILE> <WORKFLOW>`](../../api-reference/union-cli#union-cli-commands):

```shell
$ {{< key cli >}} run hello_world.py hello_world_wf
```

You should see output like this:

```shell
Running Execution on local.
Hello, world!
```

You can also pass in parameters to the workflow (assuming they declared in the workflow function):

```shell
$ {{< key cli >}} run hello_world.py hello_world_wf --name="everybody"
```

You should see output like this:

```shell
Running Execution on local.
Hello, everybody!
```

## Running remotely on {{< key product_name >}} in the cloud

Running you code in your local Python environment is useful for testing and debugging.

But to run them at scale, you will need to deploy them (or as we say, "register" them) on to your {{< key product_name >}} instance in the cloud.

When task and workflow code is registered:

* The `@{{< key kit_as >}}.task` function is loaded into a container defined by the `ImageSpec` object specified in the `container_image` parameter of the decorator.
* The `@{{< key kit_as >}}.workflow` function is compiled into a directed acyclic graph that controls the running of the tasks invoked within it.

To run the workflow on {{< key product_name >}} in the cloud, use the [`--remote` option](../../api-reference/union-cli#union-cli-commands) and the

```shell
$ {{< key cli >}} run --remote --project my-project --domain development hello_world.py hello_world_wf
```

The output displays a URL that links to the workflow execution in the UI:

{{< variant serverless >}}
{{< markdown >}}

```shell
👍 Build submitted!
⏳ Waiting for build to finish at: https://serverless.union.ai/org/...
✅ Build completed in 0:01:57!

[✔] Go to https://serverless.union.ai/org/... to see execution in the UI.
```

{{< /markdown >}}
{{< /variant >}}

{{< variant byoc selfmanaged flyte >}}
{{< markdown >}}

```shell
👍 Build submitted!
⏳ Waiting for build to finish at: https://<union-host-url>/org/...
✅ Build completed in 0:01:57!

[✔] Go to https://<union-host-url>/org/... to see execution in the UI.
```

{{< /markdown >}}
{{< /variant >}}

Click the link to see the execution in the UI.

## Register the workflow without running

Above we used the `{{< key cli >}} run --remote` to register and immediately run a workflow on {{< key product_name >}}.

This is useful for quick testing, but for more complex workflows you may want to register the workflow first and then run it from the {{< key product_name >}} interface.

To do this, you can use the `{{< key cli >}} register` command to register the workflow code with {{< key product_name >}}.

The form of the command is:

```shell
$ {{< key cli >}} register [<options>] <path-to-source-directory>
```

in our case, from within the `getting-started` directory, you would do:

```shell
$ {{< key cli >}} register --project my-project --domain development .
```

This registers all code in the current directory to {{< key product_name >}} but does not immediately run anything.
You should see the following output (or similar) in your terminal:

```shell
Running {{< key cli >}} register from /Users/my-user/scratch/my-project with images ImageConfig(default*image=Image(name='default', fqn='cr.flyte.org/flyteorg/flytekit', tag='py3.12-1.14.6', digest=None), images=[Image(name='default', fqn='cr.flyte.org/flyteorg/flytekit', tag='py3.12-1.14.6', digest=None)]) and image destination folder /root on 1 package(s) ('/Users/my-user/scratch/my-project',)
Registering against demo.hosted.unionai.cloud
Detected Root /Users/my-user/my-project, using this to create deployable package...
Loading packages ['my-project'] under source root /Users/my-user/my-project
No output path provided, using a temporary directory at /var/folders/vn/72xlcb5d5jbbb3kk_q71sqww0000gn/T/tmphdu9wf6* instead
Computed version is sSFSdBXwUmM98sYv930bSQ
Image say-hello-image:lIpeqcBrlB8DlBq0NEMR3g found. Skip building.
Serializing and registering 3 flyte entities
[✔] Task: my-project.hello_world.say_hello
[✔] Workflow: my-project.hello_world.hello_world_wf
[✔] Launch Plan: my-project.hello_world.hello_world_wf
Successfully registered 3 entities
```

## Run the workflow from the {{< key product_name >}} interface

To run the workflow, you need to go to the {{< key product_name >}} interface:

1. Navigate to the {{< key product_name >}} dashboard.
2. In the left sidebar, click **Workflows**.
3. Search for your workflow, then select the workflow from the search results.
4. On the workflow page, click **Launch Workflow**.
5. In the "Create New Execution" dialog, you can change the workflow version, launch plan, and inputs (if present). Click "Advanced options" to change the security context, labels, annotations, max parallelism, override the interruptible flag, and overwrite cached inputs.
6. To execute the workflow, click **Launch**. You should see the workflow status change to "Running", then "Succeeded" as the execution progresses.

To view the workflow execution graph, click the **Graph** tab above the running workflow.

## View the workflow execution on {{< key product_name >}}

When you view the workflow execution graph, you will see the following:

![Graph](../../_static/images/user-guide/getting-started/running-your-workflow/graph.png)

Above the graph, there is metadata that describes the workflow execution, such as the
duration and the workflow version. Next, click on the `evaluate_model` node to open up a
sidebar that contains additional information about the task:

![Sidebar](../../_static/images/user-guide/getting-started/running-your-workflow/sidebar.png)
