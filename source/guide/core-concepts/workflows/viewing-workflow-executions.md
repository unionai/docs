# Viewing workflow executions in the UI

The **Execution list** shows all executions in a project and domain combination.
An execution represents a single run of all or part of a workflow (including subworkflows and individual tasks).

This is the default view when you select a project and domain from the [**Projects list**](./index).
You can also access it from the **Executions** link in the left navigation.

![Execution list](/_static/images/execution-list.png)

## Domain Settings

This section displays any domain-level settings that have been configured for this project-domain combination. They are:

* Security Context
* Labels
* Annotations
* Raw output data config
* Max parallelism

## All Executions in the Project

For each execution in this project and domain you can see the following:

* **Start time**: Select to view the [individual execution](#execution-view).
* **Workflow/Task**: The [individual workflow](./viewing-workflows) or [individual task](../tasks/viewing-tasks) that ran in this execution.
* **Version**: The version of the workflow or task that ran in this execution.
* **Launch Plan**: The [Launch Plan](../launch-plans/viewing-launch-plans) that was used to launch this execution.
* **Schedule**: The schedule that was used to launch this execution (if any).
* **Execution ID**: The ID of the execution.
* **Status**: The status of the execution. One of **QUEUED**, **RUNNING**, **SUCCEEDED**, **FAILED** or **UNKNOWN**.
* **Duration**: The duration of the execution.

## Execution view

The execution view appears when you launch a workflow or task or select an already completed execution.

An execution represents a single run of all or part of a workflow (including subworkflows and individual tasks).

![](/_static/images/execution-view.png)

:::{note}
An execution usually represents the run of an entire workflow.
But, because workflows are composed of tasks (and sometimes subworkflows) and Union caches the outputs of those independently of the workflows in which they participate, it sometimes makes sense to execute a task or subworkflow independently.
:::

The execution view provides a lot of detailed information about the execution:

In the top bar:

![](/_static/images/execution-view-topbar.png)

* **Breadcrumb** showing:
  * **Project**:
  Select the drop down to choose a different project.
  * **Domain**:
  Select the drop down to choose a different project.
  * **Type of entity (workflow or task)**:
  Select the drop down to switch entity types (executions and launch plans are the other two possibilities).
  * **Workflow or task name**:
  Select the drop down to see the current version or select a different one.
  * **ID of this specific execution**:
  Select the drop down choose a different one.
* **Status badge**:
One of **QUEUED**, **RUNNING**, **SUCCEEDED**, **FAILED** or **UNKNOWN**.
* **View Inputs & Outputs** link.
* **Relaunch** button.

Below the top bar, details on the execution (domain, cluster, time, etc.) are displayed:

![](/_static/images/execution-view-info.png)

And below that, three tabs provide access to the **Nodes**, **Graph**, and **Timeline** views:

## Nodes

The default tab within the execution view is the **Nodes** tab.
It shows a list of the Flyte nodes that make up this execution (A node in Flyte is either a task or a (sub-)workflow):

![](/_static/images/execution-view-nodes.png)

Selecting an item in the list opens the right panel showing more details of that specific node:

![](/_static/images/execution-view-right-panel.png)

Within the right panel, we can see

* **Node ID**: _n0_
* **Task name**: _workflows.diffuse.start_process_
* **Success status**: _SUCCEEDED_
* **Caching status**: _Caching was disabled for this execution_
* **Type**: _Python Task_
* **Rerun** button

Below that, you have the tabs **Executions**, **Inputs**, **Outputs**, and **Task**.

### Executions

This tab gives you details on the execution of this particular node.

![](/_static/images/execution-view-right-panel-executions.png)

{@@ if byoc @@}
#### Task level monitoring

You can access the [task-level monitoring](../tasks/task-hardware-environment/task-level-monitoring) information by selecting **View Utilization**.

#### Logs

You can access logs by clicking the text under **Logs**.
In AWS-based systems this will say **CloudWatch Logs**.
In GCP-based system this will say **StackDriver Logs**. See [Logging](../tasks/viewing-logs).
{@@ endif @@}

### Inputs

This tab displays the input to this node.:

![](/_static/images/execution-view-right-panel-inputs.png)

### Outputs

This tab displays the output of this node:

![](/_static/images/execution-view-right-panel-outputs.png)

### Task

If this node is Task (as opposed to a subworkflow) this tab displays the Task definition:

![](/_static/images/execution-view-right-panel-task.png)

## Graph

The Graph tab displays a visual representation of the execution as a directed acyclic graph:

![](/_static/images/execution-view-graph.png)

## Timeline

The Timeline tab displays a visualization showing the timing of each task in the execution:

![](/_static/images/execution-view-timeline.png)
