---
title: Customizing task resources
weight: 1
variants: +flyte +serverless +byoc +selfmanaged
---

# Customizing task resources

When defining a task function, you can specify resource requirements for the pod that runs the task.
{{< key product_name >}} will take this into account to ensure that the task pod is scheduled to run on a Kubernetes node that meets the specified resource profile.

Resources are specified in the `@{{< key kit_as >}}.task` decorator. Here is an example:

```python
from flytekit.extras.accelerators import A100

@{{< key kit_as >}}.task(
    requests=Resources(mem="120Gi", cpu="44", ephemeral_storage="100Gi"),
    limits=Resources(mem="200Gi", cpu="100", gpu="12", ephemeral_storage="200Gi"),
    accelerator=GPUAccelerator("nvidia-tesla-a100")
)
def my_task()
    ...
```

There are three separate resource-related settings:

* `requests`
* `limits`
* `accelerator`

## The `requests` and `limits` settings

The `requests` and `limits` settings each takes a [`Resource`]() object, which itself has five possible attributes:
<!-- TODO: Add link to API -->

* `cpu`: Number of CPU cores (in whole numbers or millicores (`m`)).
* `gpu`: Number of GPU cores (in whole numbers or millicores (`m`)).
* `mem`: Main memory (in `Mi`, `Gi`, etc.).
* `ephemeral_storage`: Ephemeral storage (in `Mi`, `Gi` etc.).

Note that CPU and GPU allocations can be specified either as whole numbers or in millicores (`m`). For example, `cpu="2500m"` means two and a half CPU cores and `gpu="3000m"`, meaning three GPU cores.

{{< variant byoc selfmanaged >}}
{{< markdown >}}

The type of ephemeral storage used depends on the node type and configuration you request from the {{< key product_name >}} team. By default, all nodes will use network-attached storage for ephemeral storage. However, if a node type has attached NVMe SSD storage, you can request that the {{< key product_name >}} team configure your cluster to use the attached NVMe as ephemeral storage for that node type.

{{< /markdown >}}
{{< /variant >}}

The `requests` setting tells the system that the task requires _at least_ the resources specified and therefore the pod running this task should be scheduled only on a node that meets or exceeds the resource profile specified.

The `limits` setting serves as a hard upper bound on the resource profile of nodes to be scheduled to run the task.
The task will not be scheduled on a node that exceeds the resource profile specified (in any of the specified attributes).

> [!NOTE] GPUs take only `limits`
> GPUs should only be specified in the `limits` section of the task decorator:
>   * You should specify GPU requirements only in `limits`, not in `requests`, because Kubernetes will use the `limits` value as the `requests` value anyway.
>   * You _can_ specify GPU in both `limits` and `requests` but the two values must be equal.
>   * You cannot specify GPU `requests` without specifying `limits`.

## The `accelerator` setting

{{< variant serverless >}}
{{< markdown >}}

The `accelerator` setting further specifies the *type* of GPU required for the task.

{{< /markdown >}}
{{< /variant >}}
{{< variant byoc selfmanaged flyte >}}
{{< markdown >}}

The `accelerator` setting further specifies the *type* of specialized hardware required for the task.
This may be a GPU, a specific variation of a GPU, a fractional GPU, or a different hardware device, such as a TPU.

{{< /markdown >}}
{{< /variant >}}

See [Accelerators](./accelerators) for more information.

## Execution defaults and resource quotas

The execution defaults and resource quotas can be found on the right sidebar of the Dashboard.
They can be edited by selecting the gear icon:

![](../../../../_static/images/user-guide/core-concepts/tasks/task-hardware-environment/customizing-task-resources/execution-defaults-gear.png)

This will open a dialog:

![](../../../../_static/images/user-guide/core-concepts/tasks/task-hardware-environment/customizing-task-resources/execution-defaults-dialog.png)

> [!NOTE]
> An ephemeral storage default value of zero means that the task pod will consume storage on the node as needed.
> This makes it possible for a pod to get evicted if a node doesn't have enough storage. If your tasks are built to rely on
> ephemeral storage, we recommend being explicit with the ephemeral storage you request to avoid pod eviction.

{{< variant byoc selfmanaged >}}
{{< markdown >}}

## Task resource validation

If you attempt to execute a workflow with unsatisfiable resource requests, the execution will fail immediately rather than being allowed to queue forever.

To remedy such a failure, you should make sure that the appropriate node types are:

* Physically available in your cluster, meaning you have arranged with the {{< key product_name >}} team to include them when [configuring your data plane](../../../../deployment/configuring-your-data-plane).
* Specified in the task decorator (via the `requests`, `limits`, `accelerator`, or other parameters).

Go to the **Resources > Compute** dashboard to find the available node types and their resource profiles.

To make changes to your cluster configuration, go to the [{{< key product_name >}} Support Portal](https://get.support.union.ai/servicedesk/customer/portal/1/group/6/create/30).

{{< /markdown >}}
{{< /variant >}}
{{< variant serverless >}}
{{< markdown >}}

## Task resource validation

If you attempt to execute a workflow with unsatisfiable resource requests, the execution will fail immediately rather than being allowed to queue forever.

To remedy such a failure, you should make sure that the appropriate node types are specified in the task decorator (via the `requests`, `limits`, `accelerator`, or other parameters).

{{< /markdown >}}
{{< /variant >}}

## The `with_overrides` method

When `requests`, `limits`, or `accelerator` are specified in the `@{{< key kit_as >}}.task` decorator, they apply every time that a task is invoked from a workflow.
In some cases, you may wish to change the resources specified from one invocation to another.
To do that, use the [`with_overrides` method](../../../../api-reference/flytekit-sdk/packages/flytekit.core.node#with_overrides) of the task function.

For example:

```python
@{{< key kit_as >}}.task
def my_task(ff: FlyteFile):
    ...

@{{< key kit_as >}}.workflow
def my_workflow():
    my_task(ff=smallFile)
    my_task(ff=bigFile).with_overrides(requests=Resources(mem="120Gi", cpu="10"))
```
