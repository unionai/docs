---
title: Platform architecture
weight: 1
variants: -flyte -serverless +byoc -selfmanaged
---

# Platform architecture

The {{< key product_name >}} architecture consists of two virtual private clouds, referred to as planes—the control plane and the data plane.

![](../_static/images/user-guide/platform-architecture/union-architecture.png)

## Control plane

The control plane:
  * Runs within the {{< key product_name >}} AWS account.
  * Provides the user interface through which users can access authentication, authorization, observation, and management functions.
  * Is responsible for placing executions onto data plane clusters and performing other cluster control and management functions.

## Data plane

{{< variant byoc >}}
{{< markdown >}}
All your workflow and task executions are performed in the data plane, which runs within your AWS or GCP account. The data plane's clusters are provisioned and managed by the control plane through a resident Union operator with minimal required permissions.
{{< /markdown >}}
{{< /variant >}}

{{< key product_name >}} operates one control plane for each supported region, which supports all data planes within that region. You can choose the region in which to locate your data plane. Currently, {{< key product_name >}} supports the `us-west`, `us-east`, `eu-west`, and `eu-central` regions, and more are being added.

### Data plane nodes

{{< variant byoc >}}
{{< markdown >}}

Once the data plane is deployed in your AWS or GCP account, there are different kinds of nodes with different responsibilities running in your cluster. In {{< key product_name >}}, we distinguish between default nodes and worker nodes.

Default nodes guarantee the basic operation of the data plane and are always running. Example services that run on these nodes include autoscaling (worker nodes), monitoring services, union operator, and many more.

Worker nodes are responsible for executing your workloads. You have full control over the configuration of your [worker nodes](./data-plane-setup/configuring-your-data-plane#worker-node-groups).

When worker nodes are not in use, they automatically scale down to the configured minimum. (The default is zero.)

{{< /markdown >}}
{{< /variant >}}
{{< variant selfmanaged >}}
{{< markdown >}}

Worker nodes are responsible for executing your workloads. You have full control over the configuration of your worker nodes. When worker nodes are not in use, they automatically scale down to the configured minimum.

{{< /markdown >}}
{{< /variant >}}

## {{< key product_name >}} operator

The {{< key product_name >}} hybrid architecture lets you maintain ultimate ownership and control of your data and compute infrastructure while enabling {{< key product_name >}} to handle the details of managing that infrastructure.

Management of the data plane is mediated by a dedicated operator (the {{< key product_name >}} operator) resident on that plane.
This operator is designed to perform its functions with only the very minimum set of required permissions.
It allows the control plane to spin up and down clusters and provides {{< key product_name >}}'s support engineers with access to system-level logs and the ability to apply changes as per customer requests.
It _does not_ provide direct access to secrets or data.

In addition, communication is always initiated by the {{< key product_name >}} operator in the data plane toward the {{< key product_name >}} control plane, not the other way around.
This further enhances the security of your data plane.

{{< key product_name >}} is SOC-2 Type 2 certified. A copy of the audit report is available upon request.

## Registry data

Registry data is composed of:

* Names of workflows, tasks, launch plans, and artifacts
* Input and output types for workflows and tasks
* Execution status, start time, end time, and duration of workflows and tasks
* Version information for workflows, tasks, launchplans, and artifacts
* Artifact definitions

This type of data is stored in the control plane and is used to manage the execution of your workflows.
This does not include any workflow or task code, nor any data that is processed by your workflows or tasks.

## Execution data

Execution data is composed of::

* Event data
* Workflow inputs
* Workflow outputs
* Data passed between tasks (task inputs and outputs)

This data is divided into two categories: *raw data* and *literal data*.

### Raw data

Raw data is composed of:

* Files and directories
* Dataframes
* Models
* Python-pickled types

These are passed by reference between tasks and are always stored in an object store in your data plane.
This type of data is read by (and may be temporarily cached) by the control plane as needed, but is never stored there.

### Literal data

* Primitive execution inputs (int, string... etc.)
* JSON-serializable dataclasses

These are passed by value, not by reference, and may be stored in the {{< key product_name >}} control plane.

## Data privacy

If you are concerned with maintaining strict data privacy, be sure not to pass private information in literal form between tasks.

