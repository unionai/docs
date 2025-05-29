---
title: Jupyter notebooks
weight: 20
variants: +flyte +serverless +byoc +selfmanaged
---

# Jupyter notebooks

{{< key product_name >}} supports the development, running, and debugging of tasks and workflows in an interactive Jupyter notebook environment, which accelerates the iteration speed when building data- or machine learning-driven applications.

## Write your workflows and tasks in cells

When building tasks and workflows in a notebook, you write the code in cells as you normally would.

From those cells you can run the code locally (i.e., in the notebook itself, not on {{< key product_name >}}) by clikcing the run button, as you would in any notebook.

## Enable the notebook to register workflows to {{< key product_name >}}

To enable the tasks and workflows in your notebok to be easily registered and run on your {{< key product_name >}} instance, you needdto set up an _interactive_ {{<key kit_remote >}} object and then use to to invoke the remote executions:

First, in a cell, create an interactive {{<key kit_remote >}}  object:

```python
from flytekit.configuration import Config
from flytekit.remote import FlyteRemote

remote = {{<key kit_remote>}}(
    config=Config.auto(),
    default_project="default",
    default_domain="development",
    interactive_mode_enabled=True,
)
```

The `interactive_mode_enabled` flag must be set to `True` when running in a Jupyter notebook environment, enabling interactive registration and execution of workflows.

Next, set up the execution invocation in another cell:

```python
execution = remote.execute(my_task, inputs={"name": "Joe"})
execution = remote.execute(my_wf, inputs={"name": "Anne"})
```

The interactive {{< key kit_remote >}} client re-registers an entity whenever it’s redefined in the notebook, including when you re-execute a cell containing the entity definition, even if the entity remains unchanged. This behavior facilitates iterative development and debugging of tasks and workflows in a Jupyter notebook.