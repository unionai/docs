---
title: Task-level monitoring
weight: 5
variants: -flyte +serverless +byoc +selfmanaged
---

# Task-level monitoring

In the [Execution view](../../workflows/viewing-workflow-executions), selecting a task within the list will open the right panel.
In that panel, you will find the **View Utilization** button:

![View Utilization](../../../../_static/images/user-guide/core-concepts/tasks/task-hardware-environment/task-level-monitoring/execution-view-right-panel-executions-view-util.png)

Clicking this will take you to the **task-level monitoring** page:

![Task-level monitoring](../../../../_static/images/user-guide/core-concepts/tasks/task-hardware-environment/task-level-monitoring/task-level-monitoring.png)

## Execution Resources

This tab displays details about the resources used by this specific task.
As an example, let's say that the definition of this task in your Python code has the following task decorator:

```python
@{{< key kit_as >}}.task(
   requests=Resources(cpu="44", mem="120Gi"),
   limits=Resources(cpu="44", mem="120Gi")
)
```

These parameters are reflected in the displayed **Memory Quota** and **CPU Cores Quota** charts as explained below:

### Memory Quota

![Memory Quota](../../../../_static/images/user-guide/core-concepts/tasks/task-hardware-environment/task-level-monitoring/task-level-monitoring-memory-quota.png)

This chart shows the memory consumption of the task.

* **Limit** refers to the value of the `limits.mem` parameter (the `mem` parameter within the `Resources` object assigned to `limits`)
* **Allocated** refers to the maximum of the value of the `requests.mem` parameter (the `mem` parameter within the `Resources` object assigned to `requests`) the amount of memory actually used by the task.
* **Used** refers to the actual memory used by the task.

This chart displays the ratio of memory used over memory requested, as a percentage.
Since the memory used can sometimes exceed the memory requested, this percentage may exceed 100.

### CPU Cores Quota

![CPU Cores Quota](../../../../_static/images/user-guide/core-concepts/tasks/task-hardware-environment/task-level-monitoring/task-level-monitoring-cpu-cores-quota.png)

This chart displays the number of CPU cores being used.

* **Limit** refers to the value of the `limits.cpu` parameter (the `cpu` parameter within the `Resources` object assigned to `limits`)
* **Allocated** refers to the value of the `requests.cpu` parameter (the `cpu` parameter within the `Resources` object assigned to `requests`)
* **Used** refers to the actual number of CPUs used by the task.

### GPU Memory Utilization

![GPU Memory Utilization](../../../../_static/images/user-guide/core-concepts/tasks/task-hardware-environment/task-level-monitoring/task-level-monitoring-gpu-memory-utilization.png)

This chart displays the amount of GPU memory used for each GPU.

### GPU Utilization

![GPU Utilization](../../../../_static/images/user-guide/core-concepts/tasks/task-hardware-environment/task-level-monitoring/task-level-monitoring-gpu-utilization.png)

This chart displays the GPU core utilization as a percentage of the GPUs allocated (the `requests.gpu` parameter).

## Execution Logs (Preview)

![Execution Logs (Preview)](../../../../_static/images/user-guide/core-concepts/tasks/task-hardware-environment/task-level-monitoring/task-level-monitoring-execution-logs.png)

This tab is a preview feature that displays the `stdout` (the standard output) of the container running the task.
Currently, it only shows content while the task is actually running.

## Map Tasks

When the task you want to monitor is a **map task**, accessing the utilization data is a bit different.
Here is the task execution view of map task. Open the drop-down to reveal each subtask within the map task:

![](../../../../_static/images/user-guide/core-concepts/tasks/task-hardware-environment/task-level-monitoring/map-task-1.png)

Drill down by clicking on one of the subtasks:

![](../../../../_static/images/user-guide/core-concepts/tasks/task-hardware-environment/task-level-monitoring/map-task-2.png)

This will bring you to the individual subtask information panel, where the **View Utilization** button for the subtask can be found:

![](../../../../_static/images/user-guide/core-concepts/tasks/task-hardware-environment/task-level-monitoring/map-task-3.png)

Clicking on View Utilization will take you to the task-level monitoring page for the subtask, which will have the same structure and features as the task-level monitoring page for a standard task (see above).
