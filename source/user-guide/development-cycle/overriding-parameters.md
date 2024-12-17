# Overriding parameters

Every task execution in Union occurs within a parameter context that defines various aspects of the [task parameters](../core-concepts/tasks/task-hardware-environment) and [software environment](../core-concepts/tasks/task-software-environment).

The parameter settings for a given execution are defined by a cascading set of configurations starting at the global level and proceeding through the project, workflow definition, task definition, and task invocation levels, with each level potentially overriding settings from the previous level.

In this section we will explain the parameters involved and how they are inherited and overridden.

To begin, let's take a look at which parameters we are talking about.

## Execution settings and resource quotas

The parameters that are inherited and (potentially) overridden are the *execution settings and resource quotas* that govern the hardware and software environment within which a task is executed. They are:

* `accelerator`: Specify [accelerators](../core-concepts/tasks/task-hardware-environment/accelerators).
* `cache_serialize`: Enable [cache serialization](../core-concepts/caching).
* `cache_version`: Specify the [cache version](../core-concepts/caching).
* `cache`: Enable [caching](../core-concepts/caching).
* `container_image`: Specify a [container image](../core-concepts/tasks/task-software-environment/imagespec).
* `interruptible`: Specify whether the task is [interruptible](../core-concepts/tasks/task-hardware-environment/interruptible-instances).
* `limits`: Specify [resource limits](../core-concepts/tasks/task-hardware-environment/customizing-task-resources).
* `name`: Give a specific name to this task execution. This will appear in the workflow flowchart in the UI (see [below](#using-with_overrides-with-name-and-node_name).
* `node_name`: Give a specific name to the DAG node for this task. This will appear in the workflow flowchart in the UI (see [below](#using-with_overrides-with-name-and-node_name)).
* `requests`: Specify [resource requests](../core-concepts/tasks/task-hardware-environment/customizing-task-resources).
* `retries`: Specify the [number of times to retry this task](../core-concepts/tasks/task-parameters.md#retries).
* `task_config`: Specify a [task config](../core-concepts/tasks/task-parameters.md#task_config).
* `timeout`: Specify the [task timeout](../core-concepts/tasks/task-parameters.md#timeout).*



level, the configuration, the workflow definition, the task definition and the task invocation


the task definition, the workflow definition, and the

The `with_overrides` method allows you to specify parameter overrides on [tasks](../core-concepts/tasks/index),
[subworkflows, and sub-launch plans](../core-concepts/workflows/subworkflows-and-sub-launch-plans) at execution time.
This is useful when you want to change the behavior of a task, subworkflow, or sub-launch plan without modifying the original definition.

## Task parameters

When calling a task, you can specify the following parameters in `with_overrides`:

* `accelerator`: Specify [accelerators](../core-concepts/tasks/task-hardware-environment/accelerators).
* `cache_serialize`: Enable [cache serialization](../core-concepts/caching).
* `cache_version`: Specify the [cache version](../core-concepts/caching).
* `cache`: Enable [caching](../core-concepts/caching).
* `container_image`: Specify a [container image](../core-concepts/tasks/task-software-environment/imagespec).
* `interruptible`: Specify whether the task is [interruptible](../core-concepts/tasks/task-hardware-environment/interruptible-instances).
* `limits`: Specify [resource limits](../core-concepts/tasks/task-hardware-environment/customizing-task-resources).
* `name`: Give a specific name to this task execution. This will appear in the workflow flowchart in the UI (see [below](#using-with_overrides-with-name-and-node_name).
* `node_name`: Give a specific name to the DAG node for this task. This will appear in the workflow flowchart in the UI (see [below](#using-with_overrides-with-name-and-node_name)).
* `requests`: Specify [resource requests](../core-concepts/tasks/task-hardware-environment/customizing-task-resources).
* `retries`: Specify the [number of times to retry this task](../core-concepts/tasks/task-parameters.md#retries).
* `task_config`: Specify a [task config](../core-concepts/tasks/task-parameters.md#task_config).
* `timeout`: Specify the [task timeout](../core-concepts/tasks/task-parameters.md#timeout).

For example, if you have a task that does not have caching enabled, you can use `with_overrides` to enable caching at execution time as follows:

```python
my_task(a=1, b=2, c=3).with_overrides(cache=True)
```

### Using `with_overrides` with `name` and `node_name`

Using `with_overrides` with `name` on a task is a particularly useful feature.
For example, you can use `with_overrides(name="my_task")` to give a specific name to a task execution, which will appear in the UI.
The name specified can be chosen or generated at invocation time without modifying the task definition.

```python
@workflow
def wf() -> int:
    my_task(a=1, b=1, c=1).with_overrides(name="my_task_1")
    my_task(a=2, b=2, c=2).with_overrides(name="my_task_2", node_name="my_node_2")
    return my_task(a=1, b=1, c=1)
```

The above code would produce the following workflow display in the UI:

![Overriding name](/_static/images/user-guide/development-cycle/overriding-parameters/override-name.png)

There is also a related parameter called `node_name` that can be used to give a specific name to the DAG node for this task.
The DAG node name is usually autogenerated as `n0`, `n1`, `n2`, etc. It appears in the `node` column of the workflow table.
Overriding `node_name` results in the autogenerated name being replaced by the specified name:

![Overriding node name](/_static/images/user-guide/development-cycle/overriding-parameters/override-node-name.png)

Note that the `node_name` was specified as `my_node_2` in the code but appears as `my_node_2` in the UI. This is to the fact that Kubernetes node names cannot contain underscores. Union automatically alters the name to be Kubernetes-compliant.

## Subworkflow and sub-launch plan parameters

When calling a workflow or launch plan from within a high-level workflow
(in other words, when invoking a subworkflow or sub-launch plan),
you can specify the following parameters in `with_overrides`:

* `cache_serialize`: Enable [cache serialization](../core-concepts/caching).
* `cache_version`: Specify the [cache version](../core-concepts/caching).
* `cache`: Enable [caching](../core-concepts/caching).
