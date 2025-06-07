---
title: Viewing tasks
weight: 5
variants: +flyte +serverless +byoc +selfmanaged
---

# Viewing tasks

## Tasks list

Selecting **Tasks** in the sidebar displays a list of all the registered tasks:

![Tasks list](../../../_static/images/user-guide/core-concepts/tasks/viewing-tasks/tasks-list.png)

You can search the tasks by name and filter for only those that are archived.

Each task in the list displays some basic information about the task:

* **Inputs**: The input type for the task.
* **Outputs**: The output type for the task.
* **Description**: A description of the task.

Select an entry on the list to go to that [specific task](#task-view).

## Task view

Selecting an individual task from the [task list](#tasks-list) will take you to the task view:

![Task view](../../../_static/images/user-guide/core-concepts/tasks/viewing-tasks/task-view.png)

Here you can see:

* **Inputs & Outputs**: The input and output types for the task.
* Recent task versions. Selecting one of these takes you to the [task version view](#task-versions-list)
* Recent executions of this task. Selecting one of these takes you to the [execution view](../workflows/viewing-workflow-executions).

### Task versions list

The task versions list give you detailed information about a specific version of a task:

![Task versions list](../../../_static/images/user-guide/core-concepts/tasks/viewing-tasks/task-versions-list.png)

* **Image**: The Docker image used to run this task.
* **Env Vars**: The environment variables used by this task.
* **Commands**: The JSON object defining this task.

At the bottom is a list of all versions of the task with the current one selected.