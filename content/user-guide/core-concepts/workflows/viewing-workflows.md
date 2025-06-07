---
title: Viewing workflows
weight: 7
variants: +flyte +serverless +byoc +selfmanaged
---

# Viewing workflows

## Workflows list

The workflows list shows all workflows in the current project and domain:

![Workflows list](../../../_static/images/user-guide/core-concepts/workflows/viewing-workflows/workflows-list.png)

You can search the list by name and filter for only those that are archived.
To archive a workflow, select the archive icon ![Archive icon](../../../_static/images/user-guide/core-concepts/workflows/viewing-workflows/archive-icon.png).

Each entry in the list provides some basic information about the workflow:

* **Last execution time**:
The time of the most recent execution of this workflow.
* **Last 10 executions**:
The status of the last 10 executions of this workflow.
* **Inputs**:
The input type for the workflow.
* **Outputs**:
The output type for the workflow.
* **Description**:
 The description of the workflow.

Select an entry on the list to go to that [specific workflow](#workflow-view).

## Workflow view

The workflow view provides details about a specific workflow.

![Workflow view](../../../_static/images/user-guide/core-concepts/workflows/viewing-workflows/workflow-view.png)

This view provides:
* A list of recent workflow versions:
  Selecting a version will take you to the [workflow version list](#workflow-versions-list).
* A list of recent executions:
  Selecting an execution will take you to the [execution view](./viewing-workflow-executions).

### Workflow versions list

The workflow versions list shows the  a list of all versions of this workflow along with a graph view of the workflow structure:

![Workflow version list](../../../_static/images/user-guide/core-concepts/workflows/viewing-workflows/workflow-versions-list.png)

### Workflow and task descriptions

{{< key product_name >}} enables the use of docstrings to document your code. Docstrings are stored in the control plane and displayed on the UI for each workflow or task.