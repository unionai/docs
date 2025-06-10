---
title: Debugging with interactive tasks
weight: 11
variants: +flyte +serverless +byoc +selfmanaged
---

# Debugging with interactive tasks

With interactive tasks you can inspect and debug live task code directly in the UI in an embedded Visual Studio Code IDE.

## Enabling interactive tasks in your code

To enable interactive tasks, you need to:

* Include `flytekitplugins-flyteinteractive` as a dependency
* Use the `@vscode` decorator on the tasks you want to make interactive.

The `@vscode` decorator, when applied, converts a task into a Visual Studio Code
server during runtime.  This process overrides the standard execution of the
task’s function body, initiating a command to start a Visual Studio Code server
instead.

<!-- TODO: Remove mention of flytesnacks and flytekit -->

> [!NOTE] No need for ingress or port forwarding
> The {{< key product_name >}} interactive tasks feature is an adaptation of the open-source
> [FlyteInteractive plugin](https://docs.flyte.org/en/latest/flytesnacks/examples/flyteinteractive_plugin/index.html).
> It improves on the open-source version by removing the need for ingress
> configuration or port forwarding, providing a more seamless debugging
> experience.

## Basic example

The following example demonstrates interactive tasks in a simple workflow.

### requirements.txt

This `requirements.txt` file is used by all the examples in this section:

```text
flytekit
flytekitplugins-flyteinteractive
```

{{< variant byoc selfmanaged flyte >}}
{{< markdown >}}

### example.py

```python
"""{{< key product_name >}} workflow example of interactive tasks (@vscode)"""

import {{< key kit_import >}}
from flytekitplugins.flyteinteractive import vscode

image = {{< key kit_as >}}.ImageSpec(
    registry="<my-image-registry>",
    name="interactive-tasks-example",
    base_image="ghcr.io/flyteorg/flytekit:py3.11-latest",
    requirements="requirements.txt"
)

@{{< key kit_as >}}.task(container_image=image)
@vscode
def say_hello(name: str) -> str:
    s = f"Hello, {name}!"
    return s

@{{< key kit_as >}}.workflow
def wf(name: str = "world") -> str:
    greeting = say_hello(name=name)
    return greeting
```

{{< /markdown >}}
{{< /variant >}}
{{< variant serverless >}}
{{< markdown >}}

### example.py

```python
"""{{< key product_name >}} workflow example of interactive tasks (@vscode)"""

import {{< key kit_import >}}
from flytekitplugins.flyteinteractive import vscode

image = {{< key kit_as >}}.ImageSpec(
    builder="union",
    name="interactive-tasks-example",
    requirements="requirements.txt"
)

@{{< key kit_as >}}.task(container_image=image)
@vscode
def say_hello(name: str) -> str:
    s = f"Hello, {name}!"
    return s

@{{< key kit_as >}}.workflow
def wf(name: str = "world") -> str:
    greeting = say_hello(name=name)
    return greeting
```

{{< /markdown >}}
{{< /variant >}}

{{< variant byoc selfmanaged flyte >}}
{{< markdown >}}

## Register and run the workflow

To register the code to a project on {{< key product_name >}} and run the workflow, follow the
directions in [Running your code](../development-cycle/running-your-code)

{{< /markdown >}}
{{< /variant >}}
{{< variant serverless >}}
{{< markdown >}}

## Register and run the workflow

To register the code to a project on {{< key product_name >}} as usual and run the workflow.

{{< /markdown >}}
{{< /variant >}}

## Access the IDE

1. Select the first task in the workflow page (in this example the task is called `say_hello`).
   The task info pane will appear on the right side of the page.
2. Wait until the task is in the **Running** state and the **VSCode (User)** link appears.
3. Click the **VSCode (User)** link.

![VSCode link](../../_static/images/user-guide/development-cycle/debugging-with-interactive-tasks/vscode-link.png)

## Inspect the task code

Once the IDE opens, you will be able to see your task code in the editor.

![Inspect code](../../_static/images/user-guide/development-cycle/debugging-with-interactive-tasks/inspect-code.png)

## Interactive debugging

To run the task in VSCode, click the _Run and debug_ symbol on the left rail of the IDE and select the **Interactive Debugging** configuration.

![Interactive debugging](../../_static/images/user-guide/development-cycle/debugging-with-interactive-tasks/interactive-debugging.png)

Click the **Play** button beside the configuration drop-down to run the task.
This will run your task with inputs from the previous task. To inspect intermediate states, set breakpoints in the Python code and use the debugger for tracing.

> [!NOTE] No task output written to {{< key product_name >}} storage
> It’s important to note that during the debugging phase the task runs entirely within VSCode and does not write the output to {{< key product_name >}} storage.

## Update your code

You can edit your code in the VSCode environment and run the task again to see the changes.
Note, however, that the changes will not be automatically persisted anywhere.
You will have to manually copy and paste the changes back to your local environment.

## Resume task

After you finish debugging, you can resume your task with updated code by executing the **Resume Task** configuration.
This will terminate the code server, run the task with inputs from the previous task, and write the output to {{< key product_name >}} storage.

> [!NOTE] Remember to persist your code
> Remember to persist your code (for example, by checking it into GitHub) before resuming the task, since you will lose the connection to the VSCode server afterwards.

![Resume task](../../_static/images/user-guide/development-cycle/debugging-with-interactive-tasks/resume-task.png)

## Auxiliary Python files

You will notice that aside from your code, there are some additional files in the VSCode file explorer that have been automatically generated by the system:

### flyteinteractive_interactive_entrypoint.py

The `flyteinteractive_interactive_entrypoint.py` script implements the **Interactive Debugging** action that we used above:

![Interactive entrypoint](../../_static/images/user-guide/development-cycle/debugging-with-interactive-tasks/flyteinteractive-interactive-entrypoint-py.png)

### flyteinteractive_resume_task.py

The `flyteinteractive_resume_task.py` script implements the **Resume Task** action that we used above:

![Resume task](../../_static/images/user-guide/development-cycle/debugging-with-interactive-tasks/flyteinteractive-resume-task-py.png)

### launch.json

The `launch.json` file in the `.vscode` directory configures the **Interactive Debugging** and **Resume Task** actions.

![launch.json](../../_static/images/user-guide/development-cycle/debugging-with-interactive-tasks/launch-json.png)

## Integrated terminal

In addition to using the convenience functions defined by the auxiliary files, you can also run your Python code script directly from the integrated terminal using `python <script_name>.py` (in this example, `python hello.py`).

![Interactive terminal](../../_static/images/user-guide/development-cycle/debugging-with-interactive-tasks/interactive-terminal.png)

## Install extensions

As with local VSCode, you can install a variety of extensions to assist development.
Available extensions differ from official VSCode for legal reasons and are hosted on the [Open VSX Registry](https://open-vsx.org/).

Python and Jupyter extensions are installed by default.
Additional extensions can be added by defining a configuration object and passing it to the `@vscode` decorator, as shown below:

{{< variant byoc selfmanaged flyte >}}
{{< markdown >}}

### example-extensions.py

```python
"""{{< key product_name >}} workflow example of interactive tasks (@vscode) with extensions"""

import {{< key kit_import >}}
from flytekitplugins.flyteinteractive import COPILOT_EXTENSION, VscodeConfig, vscode

image = {{< key kit_as >}}.ImageSpec(
    registry="<my-image-registry>",
    name="interactive-tasks-example",
    base_image="ghcr.io/flyteorg/flytekit:py3.11-latest",
    requirements="requirements.txt"
)

config = VscodeConfig()
config.add_extensions(COPILOT_EXTENSION) # Use predefined URL
config.add_extensions(
    "https://open-vsx.org/api/vscodevim/vim/1.27.0/file/vscodevim.vim-1.27.0.vsix"
) # Copy raw URL from Open VSX

@{{< key kit_as >}}.task(container_image=image)
@vscode(config=config)
def say_hello(name: str) -> str:
    s = f"Hello, {name}!"
    return s

@{{< key kit_as >}}.workflow
def wf(name: str = "world") -> str:
    greeting = say_hello(name=name)
    return greeting
```

{{< /markdown >}}
{{< /variant >}}
{{< variant serverless >}}
{{< markdown >}}

### example-extensions.py

```python
"""{{< key product_name >}} workflow example of interactive tasks (@vscode) with extensions"""

import {{< key kit_import >}}
from flytekitplugins.flyteinteractive import COPILOT_EXTENSION, VscodeConfig, vscode

image = {{< key kit_as >}}.ImageSpec(
    builder="union",
    name="interactive-tasks-example",
    requirements="requirements.txt"
)

config = VscodeConfig()
config.add_extensions(COPILOT_EXTENSION) # Use predefined URL
config.add_extensions(
    "https://open-vsx.org/api/vscodevim/vim/1.27.0/file/vscodevim.vim-1.27.0.vsix"
) # Copy raw URL from Open VSX

@{{< key kit_as >}}.task(container_image=image)
@vscode(config=config)
def say_hello(name: str) -> str:
    s = f"Hello, {name}!"
    return s

@{{< key kit_as >}}.workflow
def wf(name: str = "world") -> str:
    greeting = say_hello(name=name)
    return greeting
```

{{< /markdown >}}
{{< /variant >}}

## Manage resources

To manage resources, the VSCode server is terminated after a period of idleness (no active HTTP connections).
Idleness is monitored via a heartbeat file.

The `max_idle_seconds` parameter can be used to set the maximum number of seconds the VSCode server can be idle before it is terminated.

{{< variant byoc selfmanaged flyte >}}
{{< markdown >}}

### example-manage-resources.py

```python
"""{{< key product_name >}} workflow example of interactive tasks (@vscode) with max_idle_seconds"""

import {{< key kit_import >}}
from flytekitplugins.flyteinteractive import vscode

image = {{< key kit_as >}}.ImageSpec(
    registry="<my-image-registry>",
    name="interactive-tasks-example",
    base_image="ghcr.io/flyteorg/flytekit:py3.11-latest",
    requirements="requirements.txt"
)

@{{< key kit_as >}}.task(container_image=image)
@vscode(max_idle_seconds=60000)
def say_hello(name: str) -> str:
   s = f"Hello, {name}!"
   return s

@{{< key kit_as >}}.workflow
def wf(name: str = "world") -> str:
    greeting = say_hello(name=name)
    return greeting
```

{{< /markdown >}}
{{< /variant >}}
{{< variant serverless >}}
{{< markdown >}}

### example-manage-resources.py

```python
"""{{< key product_name >}} workflow example of interactive tasks (@vscode) with max_idle_seconds"""

import {{< key kit_import >}}
from flytekitplugins.flyteinteractive import vscode

image = {{< key kit_as >}}.ImageSpec(
    builder="union",
    name="interactive-tasks-example",
    requirements="requirements.txt"
)

@{{< key kit_as >}}.task(container_image=image)
@vscode(max_idle_seconds=60000)
def say_hello(name: str) -> str:
    s = f"Hello, {name}!"
    return s

@{{< key kit_as >}}.workflow
def wf(name: str = "world") -> str:
    greeting = say_hello(name=name)
    return greeting
```

{{< /markdown >}}
{{< /variant >}}

## Pre and post hooks

Interactive tasks also allow the registration of functions to be executed both before and after VSCode starts.
This can be used for tasks requiring setup or cleanup.


{{< variant flyte byoc selfmanaged >}}
{{< markdown >}}

### example-pre-post-hooks.py

```python
"""{{< key product_name >}} workflow example of interactive tasks (@vscode) with pre and post hooks"""

import {{< key kit_import >}}
from flytekitplugins.flyteinteractive import vscode

image = {{< key kit_as >}}.ImageSpec(
    registry="<my-image-registry>",
    name="interactive-tasks-example",
    base_image="ghcr.io/flyteorg/flytekit:py3.11-latest",
    requirements="requirements.txt"
)

def set_up_proxy():
    print("set up")

def push_code():
    print("push code")

@{{< key kit_as >}}.task(container_image=image)
@vscode(pre_execute=set_up_proxy, post_execute=push_code)
def say_hello(name: str) -> str:
    s = f"Hello, {name}!"
    return s

@{{< key kit_as >}}.workflow
def wf(name: str = "world") -> str:
    greeting = say_hello(name=name)
    return greeting
```

{{< /markdown >}}
{{< /variant >}}
{{< variant serverless >}}
{{< markdown >}}

### example-pre-post-hooks.py

```python
"""{{< key product_name >}} workflow example of interactive tasks (@vscode) with pre and post hooks"""

import {{< key kit_import >}}
from flytekitplugins.flyteinteractive import vscode

image = {{< key kit_as >}}.ImageSpec(
    builder="union",
    name="interactive-tasks-example",
    requirements="requirements.txt"
)

def set_up_proxy():
print("set up")

def push_code():
print("push code")

@{{< key kit_as >}}.task(container_image=image)
@vscode(pre_execute=set_up_proxy, post_execute=push_code)
def say_hello(name: str) -> str:
    s = f"Hello, {name}!"
    return s

@{{< key kit_as >}}.workflow
def wf(name: str = "world") -> str:
    greeting = say_hello(name=name)
    return greeting
```

{{< /markdown >}}
{{< /variant >}}

## Only initiate VSCode on task failure

The system can also be set to only initiate VSCode _after a task failure_, preventing task termination and thus enabling inspection.
This is done by setting the `run_task_first` parameter to `True`.



{{< variant byoc selfmanaged flyte >}}
{{< markdown >}}

### example-run-task-first.py

```python
"""{{< key product_name >}} workflow example of interactive tasks (@vscode) with run_task_first"""

import {{< key kit_import >}}
from flytekitplugins.flyteinteractive import vscode

image = {{< key kit_as >}}.ImageSpec(
    registry="<my-image-registry>",
    name="interactive-tasks-example",
    base_image="ghcr.io/flyteorg/flytekit:py3.11-latest",
    requirements="requirements.txt"
)

@{{< key kit_as >}}.task(container_image=image)
@vscode(run_task_first=True)
def say_hello(name: str) -> str:
    s = f"Hello, {name}!"
    return s

@{{< key kit_as >}}.workflow
def wf(name: str = "world") -> str:
    greeting = say_hello(name=name)
    return greeting
```

{{< /markdown >}}
{{< /variant >}}
{{< variant serverless >}}
{{< markdown >}}

### example-run-task-first.py

```python
"""{{< key product_name >}} workflow example of interactive tasks (@vscode) with run_task_first"""

import {{< key kit_import >}}
from flytekitplugins.flyteinteractive import vscode

image = {{< key kit_as >}}.ImageSpec(
    builder="union",
    name="interactive-tasks-example",
    requirements="requirements.txt"
)

@{{< key kit_as >}}.task(container_image=image)
@vscode(run_task_first=True)
def say_hello(name: str) -> str:
    s = f"Hello, {name}!"
    return s

@{{< key kit_as >}}.workflow
def wf(name: str = "world") -> str:
    greeting = say_hello(name=name)
    return greeting
```

{{< /markdown >}}
{{< /variant >}}

## Debugging execution issues

The inspection of task and workflow execution provides log links to debug things further.

Using `--details` flag you can view node executions with log links.

```shell
└── n1 - FAILED - 2021-06-30 08:51:07.3111846 +0000 UTC - 2021-06-30 08:51:17.192852 +0000 UTC
    └── Attempt :0
        └── Task - FAILED - 2021-06-30 08:51:07.3111846 +0000 UTC - 2021-06-30 08:51:17.192852 +0000 UTC
        └── Logs :
            └── Name :Kubernetes Logs (User)
            └── URI :http://localhost:30082/#/log/flytectldemo-development/f3a5a4034960f4aa1a09-n1-0/pod?namespace=flytectldemo-development
```

Additionally, you can check the pods launched in `\<project>-\<domain>` namespace

```shell
$ kubectl get pods -n <project>-<domain>
```

The launched pods will have a prefix of execution name along with suffix of `nodeId`:

```shell
NAME                        READY   STATUS             RESTARTS   AGE
f65009af77f284e50959-n0-0   0/1     ErrImagePull       0          18h
```

For example, above we see that the `STATUS` indicates an issue with pulling the image.
