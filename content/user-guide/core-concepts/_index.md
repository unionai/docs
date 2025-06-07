---
title: Core concepts
weight: 4
sidebar_expanded: true
variants: +flyte +serverless +byoc +selfmanaged
sidebar_expanded: true
---

# Core concepts

{{< key product_name >}} is a platform for building and orchestrating the execution of interconnected software processes across machines in a computer cluster.
In {{< key product_name >}} terminology, the software processes are called *tasks* and the overall organization of connections between tasks is called a *workflow*.
The tasks in a workflow are connected to each other by their inputs and outputs. The output of one task becomes the input of another.

More precisely, a workflow in {{< key product_name >}} is a *directed acyclic graph (DAG)* of *nodes* where each node is a unit of execution and the edges between nodes represent the flow of data between them.
The most common type of node is a task node (which encapsulates a task), though there are also workflow nodes (which encapsulate subworkflows) and branch nodes.
In most contexts we just say that a workflow is a DAG of tasks.

You define tasks and workflows in Python using the {{< key kit_name >}} SDK. The {{< key kit_name >}} SDK provides a set of decorators and classes that allow you to define tasks and workflows in a way that is easy to understand and work with.
Once defined, tasks and workflows are deployed to your {{< key product_name >}} instance (we say they are *registered* to the instance), where they are compiled into a form that can be executed on your {{< key product_name >}} cluster.

In addition to tasks and workflows, another important concept in {{< key product_name >}} is the [*launch plan*](./launch-plans).
A launch plan is like a template that can be used to define the inputs to a workflow.
Triggering a launch plan will launch its associated workflow with the specified parameters.

## Defining tasks and workflows

Using the {{< key kit_name >}} SDK, tasks and workflows are defined as Python functions using the `@{{< key kit_as >}}.task` and `@{{< key kit_as >}}.workflow` decorators, respectively:

```python
import {{< key kit_import >}}

@{{< key kit_as >}}.task
def task_1(a: int, b: int, c: int) -> int:
    return a + b + c

@{{< key kit_as >}}.task
def task_2(m: int, n: int) -> int:
    return m * n

@{{< key kit_as >}}.task
def task_3(x: int, y: int) -> int:
    return x - y

@{{< key kit_as >}}.workflow
def my_workflow(a: int, b: int, c: int, m: int, n: int) -> int:
    x = task_1(a=a, b=b, c=c)
    y = task_2(m=m, n=n)
    return task_3(x=x, y=y)
```

Here we see three tasks defined using the `@{{< key kit_as >}}.task` decorator and a workflow defined using the `@{{< key kit_as >}}.workflow` decorator.
The workflow calls `task_1` and `task_2` and passes the results to `task_3` before finally outputting the result of `task_3`.

When the workflow is registered, {{< key product_name >}} compiles the workflow into a directed acyclic graph (DAG) based on the input/output dependencies between the tasks.
The DAG is then used to execute the tasks in the correct order, taking advantage of any parallelism that is possible.
For example, the workflow above results in the following DAG:

![Workflow DAG](../../_static/images/user-guide/core-concepts/workflow-dag.png)

### Type annotation is required

One important difference between {{< key product_name >}} and generic Python is that in {{< key product_name >}} all inputs and outputs *must be type annotated*.
This is because tasks are strongly typed, meaning that the types of the inputs and outputs are validated at deployment time.

See [Tasks are strongly typed](./tasks#tasks-are-strongly-typed) for more details.

### Workflows *are not* full Python functions

The definition of a workflow must be a valid Python function, so it can be run locally as a normal Python function during development,
but only *a subset of Python syntax is allowed*, because it must also be compiled into a DAG that is deployed and executed on {{< key product_name >}}.

*Technically then, the language of a workflow function is a domain-specific language (DSL) that is a subset of Python.*

See [Workflows](./workflows) for more details.

## Registering tasks and workflows

### Registering on the command line with `{{< key cli >}}` or `{{< key ctl >}}`

In most cases, workflows and tasks (and possibly other things, such as launch plans) are defined in your project code and registered as a bundle using `{{< key cli >}}` or `{{< key ctl >}}` For example:

```shell
$ {{< key cli >}} register ./workflows --project my_project --domain development
```

Tasks can also be registered individually, but it is more common to register alongside the workflow that uses them.

See [Running your code](../development-cycle/running-your-code).

### Registering in Python with `{{< key kit_remote >}}`

As with all {{< key product_name >}} command line actions, you can also perform registration of workflows and tasks programmatically with [`{{< key kit_remote >}}`](), specifically, [`{{< key kit_remote >}}.register_script`](),
[`{{< key kit_remote >}}.register_workflow`](), and
[`{{< key kit_remote >}}.register_task`]().
<!-- TODO: Add link to API -->

## Results of registration

When the code above is registered to {{< key product_name >}}, it results in the creation of five objects:

* The tasks `workflows.my_example.task_1`, `workflows.my_example.task_2`, and `workflows.my_example.task_3` (see [Task fundamentals](./tasks) for more details).
* The workflow `workflows.my_example.my_workflow`.
* The default launch plan `workflows.my_example.my_workflow` (see [Launch plans](./launch-plans) for more details).

Notice that the task and workflow names are derived from the path, file name and function name of the Python code that defines them: `<folder>.<file>.<function>`.
The default launch plan for a workflow always has the same name as its workflow.

## Changing tasks and workflows

Tasks and workflows are changed by altering their definition in code and re-registering.
When a task or workflow with the same project, domain, and name as a preexisting one is re-registered, a new version of that entity is created.

## Inspecting tasks and workflows

### Inspecting workflows in the UI

Select **Workflows** in the sidebar to display a list of all the registered workflows in the project and domain.
You can search the workflows by name.

Click on a workflow in the list to see the **workflow view**.
The sections in this view are as follows:

* **Recent Workflow Versions**: A list of recent versions of this workflow.
  Select a version to see the **Workflow version view**.
  This view shows the DAG and a list of all version of the task.
  You can switch between versions with the radio buttons.

* **All Executions in the Workflow**: A list of all executions of this workflow.
  Click on an execution to go to the [Execution view](./workflows/viewing-workflow-executions).

* **Launch Workflow button**: In the top right of the workflow view, you can click the **Launch Workflow** button to run the workflow with the default inputs.

### Inspecting tasks in the UI

Select **Tasks** in the sidebar to display a list of all the registered tasks in the project and domain.
You can search the launch plans by name.
To filter for only those that are archived, check the **Show Only Archived Tasks** box.

Click on a task in the list to see the task view
The sections in the task view are as follows:

* **Inputs & Outputs**: The name and type of each input and output for the latest version of this task.

* **Recent Task Versions**: A list of recent versions of this task.
  Select a version to see the **Task version view**:
  This view shows the task details and a list of all version of the task.
  You can switch between versions with the radio buttons.
  See [Tasks](./tasks) for more information.

* **All Executions in the Task**: A list of all executions of this task.
  Click on an execution to go to the execution view.

* **Launch Task button**: In the top right of the task view, you can click the **Launch Task** button to run the task with the default inputs.

### Inspecting workflows on the command line with `{{< key ctl >}}`

To view all tasks within a project and domain:

```shell
$ {{< key ctl >}} get workflows \
       --project <project-id> \
       --domain <domain>
```

To view a specific workflow:

```shell
$ {{< key ctl >}} get workflow \
       --project <project-id> \
       --domain <domain> \
       <workflow-name>
       <workflow-version>
```

See [{{< key ctl_name >}} CLI](../../api-reference/uctl-cli) for more details.

### Inspecting tasks on the command line with `{{< key ctl >}}`

To view all tasks within a project and domain:

```shell
$ {{< key ctl >}} get tasks \
       --project <project-id> \
       --domain <domain>
```

To view a specific task:

```shell
$ {{< key ctl >}} get task \
       --project <project-id> \
       --domain <domain> \
       <task-name>
       <task-version>
```

See [{{< key ctl_name >}} CLI](../../api-reference/uctl-cli) for more details.

### Inspecting tasks and workflows in Python with `{{< key kit_remote >}}`

Use the method [`{{< key kit_remote >}}.fetch_workflow`]() or [`{{< key kit_remote >}}.client.get_workflow`]() to get a workflow.
See [`{{< key kit_remote >}}`]() for more options and details.

Use the method [`{{< key kit_remote >}}.fetch_task`]() or [`{{< key kit_remote >}}.client.get_task`]() to get a task.
See [`{{< key kit_remote >}}`]() for more options and details.
<!-- TODO: Add links to API -->

## Running tasks and workflows

### Running a task or workflow in the UI

To run a workflow in the UI, click the **Launch Workflow** button in the workflow view.

You can also run individual tasks in the UI by clicking the **Launch Task** button in the task view.

### Running a task or workflow locally on the command line with `{{< key cli >}}` or `python`

You can execute a {{< key product_name >}} workflow or task locally simply by calling it just like any regular Python function.
For example, you can add the following to the above code:

```python
if __name__ == "__main__":
    my_workflow(a=1, b=2, c=3, m=4, n=5)
```

If the file is saved as `my_example.py`, you can run it locally using the following command:

```shell
$ python my_example.py
```

Alternatively, you can run the task locally with the `{{< key cli >}}` command line tool:

To run it locally, you can use the following `{{< key cli >}} run` command:

```shell
$ {{< key cli >}} run my_example.py my_workflow --a 1 --b 2 --c 3 --m 4 --n 5
```

This has the advantage of allowing you to specify the input values as command line arguments.
For more details on running workflows and tasks, see [Development cycle](../development-cycle).

### Running a task or workflow remotely on the command line with `{{< key cli >}}`

To run a workflow remotely on your {{< key product_name >}} installation, use the following command (this assumes that you have your [{{<key config_env >}} set up correctly](../development-cycle/setting-up-a-project)):

```shell
$  {{< key cli >}} run --remote my_example.py my_workflow --a 1 --b 2 --c 3 --m 4 --n 5
```

### Running a task or workflow remotely in Python with `{{< key kit_remote >}}`

To run a workflow or task remotely in Python, use the method [`{{< key kit_remote >}}.execute`](). See [`{{< key kit_remote >}}`]() for more options and details.

<!-- TODO: Add links to API -->
