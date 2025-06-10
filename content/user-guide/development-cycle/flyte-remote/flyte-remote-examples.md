---
title: FlyteRemote examples
weight: 1
variants: +flyte -serverless -byoc -selfmanaged
---

# {{< key kit_remote >}} examples

## Registering and running a workflow

In the following example we register and run a workflow and retrieve its output:

```shell
├── remote.py
└── workflow
    ├── __init__.py
    └── example.py
```

The workflow code that will be registered and run on {{< key product_name >}} resides in the `workflow` directory and consists of an empty `__init__.py` file and the workflow and task code in `example.py`:

```python
import os
import {{< key kit_import >}}

@{{< key kit_as >}}.task()
def create_file(message: str) -> {{< key kit_as >}}.FlyteFile:
    with open("data.txt", "w") as f:
        f.write(message)
    return {{< key kit_as >}}.FlyteFile(path="data.txt")

@{{< key kit_as >}}.workflow
def my_workflow(message: str) -> {{< key kit_as >}}.FlyteFile:
    f = create_file(message)
    return f
```

The file `remote.py` contains the `{{< key kit_remote >}}` logic. It is not part of the workflow code, and is meant to be run on your local machine.

```python
import {{< key kit_import >}}
from workflow.example import my_workflow


def run_workflow():
    remote = {{<key kit_as>}}.{{< key kit_remote >}}()
    remote.fast_register_workflow(entity=my_workflow)
    execution = remote.execute(
        entity=my_workflow,
        inputs={"message": "Hello, world!"},
        wait=True)
    output = execution.outputs["o0"]
    print(output)
    with open(output, "r") as f:
        read_lines = f.readlines()
    print(read_lines)
```


The `my_workflow` workflow and the `create_file` task is registered and run.
Once the workflow completes, the output is passed back to the `run_workflow` function and printed out.

The output is also be available via the UI, in the **Outputs** tab of the `create_file` task details view:

![Outputs](../../../_static/images/user-guide/development-cycle/union-remote/outputs.png)

The steps above demonstrates the simplest way of registering and running a workflow with `{{< key kit_remote >}}`.
For more options and details see [API reference > {{< key kit_remote >}} > Entrypoint]().
<!-- TODO: Add link to API -->

## Fetching outputs

By default, `{{< key kit_remote >}}.execute` is non-blocking, but you can also pass in `wait=True` to make it synchronously wait for the task or workflow to complete, as we did above.

You can print out the {{< key product_name >}} console URL corresponding to your execution with:

```python
print(f"Execution url: {remote.generate_console_url(execution)}")
```

And you can synchronize the state of the execution object with the remote state with the `sync()` method:

```python
synced_execution = remote.sync(execution)
print(synced_execution.inputs)  # print out the inputs
```

You can also wait for the execution after you’ve launched it and access the outputs:

```shell
completed_execution = remote.wait(execution)
print(completed_execution.outputs)  # print out the outputs
```

## Terminating all running executions for a workflow

This example shows how to terminate all running executions in a given workflow name.

```python
import {{< key kit_import >}}
from dataclasses import dataclass
import json
from flytekit.configuration import Config
from flytekit.models.core.execution import NodeExecutionPhase

@dataclass
class Execution:
    name: str
    link: str

SOME_LARGE_LIMIT = 5000
PHASE = NodeExecutionPhase.RUNNING
WF_NAME = "your_workflow_name"
EXECUTIONS_TO_IGNORE = ["some_execution_name_to_ignore"]
PROJECT = "your_project"
DOMAIN = "production"
ENDPOINT = "union.example.com"

remote = {{<key kit_as>}}.{{< key kit_remote >}}(
    config=Config.for_endpoint(endpoint=ENDPOINT),
    default_project=PROJECT,
    default_domain=DOMAIN,
)

executions_of_interest = []

executions = remote.recent_executions(limit=SOME_LARGE_LIMIT)

for e in executions:
    if e.closure.phase == PHASE:
        if e.spec.launch_plan.name == WF_NAME:
            if e.id.name not in EXECUTIONS_TO_IGNORE:
                execution_on_interest = Execution(name=e.id.name, link=f"https://{ENDPOINT}/console/projects/{PROJECT}/domains/{DOMAIN}/executions/{e.id.name}")
                executions_of_interest.append(execution_on_interest)
                remote.terminate(e, cause="Terminated manually via script.")


with open('terminated_executions.json', 'w') as f:
    json.dump([{'name': e.name, 'link': e.link} for e in executions_of_interest], f, indent=2)

print(f"Terminated {len(executions_of_interest)} executions.")
```

## Rerunning all failed executions of a workflow

This example shows how to identify all failed executions from a given workflow since a certain time, and re-run them with the same inputs and a pinned workflow version.

```python
import datetime
import pytz
import {{< key kit_import >}}
from flytekit.models.core.execution import NodeExecutionPhase

SOME_LARGE_LIMIT = 5000
WF_NAME = "your_workflow_name"
PROJECT = "your_project"
DOMAIN = "production"
ENDPOINT = "union.example.com"
VERSION = "your_target_workflow_version"

remote = {{<key kit_as>}}.{{< key kit_remote >}}(
    config=Config.for_endpoint(endpoint=ENDPOINT),
    default_project=PROJECT,
    default_domain=DOMAIN,
)

executions = remote.recent_executions(limit=SOME_LARGE_LIMIT)

failures = [
    NodeExecutionPhase.FAILED,
    NodeExecutionPhase.ABORTED,
    NodeExecutionPhase.FAILING,
]

# time of the last successful execution
date = datetime.datetime(2024, 10, 30, tzinfo=pytz.UTC)

# filter executions by name
filtered = [execution for execution in executions if execution.spec.launch_plan.name == WF_NAME]

# filter executions by phase
failed = [execution for execution in filtered if execution.closure.phase in failures]

# filter executions by time
windowed = [execution for execution in failed if execution.closure.started_at > date]

# get inputs for each execution
inputs = [remote.sync(execution).inputs for execution in windowed]

# get new workflow version entity
workflow = remote.fetch_workflow(name=WF_NAME, version=VERSION)

# execute new workflow for each failed previous execution
[remote.execute(workflow, inputs=X) for X in inputs]
```

## Filtering for executions using a `Filter`

This example shows how to use a `Filter` to only query for the executions you want.

```python
from flytekit.models import filters
import {{< key kit_import >}}

WF_NAME = "your_workflow_name"
LP_NAME = "your_launchplan_name"
PROJECT = "your_project"
DOMAIN = "production"
ENDPOINT = "union.example.com"

remote = {{<key kit_as>}}.{{< key kit_remote >}}.for_endpoint(ENDPOINT)

# Only query executions from your project
project_filter = filters.Filter.from_python_std(f"eq(workflow.name,{WF_NAME})")
project_executions = remote.recent_executions(project=PROJECT, domain=DOMAIN, filters=[project_filter])

# Query for the latest execution that succeeded and was between 8 and 16 minutes
latest_success = remote.recent_executions(
    limit=1,
    filters=[
        filters.Equal("launch_plan.name", LP_NAME),
        filters.Equal("phase", "SUCCEEDED"),
        filters.GreaterThan("duration", 8 * 60),
        filters.LessThan("duration", 16 * 60),
    ],
)
```

## Launch task via FlyteRemote with a new version

```python
import {{< key kit_import >}}
from flytekit.remote import FlyteRemote
from flytekit.configuration import Config, SerializationSettings

# {{< key kit_remote >}} object is the main entrypoint to API
remote = {{<key kit_as>}}.{{< key kit_remote >}}(
    config=Config.for_endpoint(endpoint="flyte.example.net"),
    default_project="flytesnacks",
    default_domain="development",
)

# Get Task
task = remote.fetch_task(name="workflows.example.generate_normal_df", version="v1")

task = remote.register_task(
    entity=flyte_task,
    serialization_settings=SerializationSettings(image_config=None),
    version="v2",
)

# Run Task
execution = remote.execute(
     task, inputs={"n": 200, "mean": 0.0, "sigma": 1.0}, execution_name="task-execution", wait=True
)

# Or use execution_name_prefix to avoid repeated execution names
execution = remote.execute(
     task, inputs={"n": 200, "mean": 0.0, "sigma": 1.0}, execution_name_prefix="flyte", wait=True
)

# Inspecting execution
# The 'inputs' and 'outputs' correspond to the task execution.
input_keys = execution.inputs.keys()
output_keys = execution.outputs.keys()
```

## Launch workflow via {{< key kit_remote >}}

Workflows can be executed with UnionRemote because under the hood it fetches and triggers a default launch plan.

```python
import {{< key kit_import >}}
from flytekit.configuration import Config

# UnionRemote object is the main entrypoint to API
remote = {{<key kit_as>}}.{{< key kit_remote >}}(
    config=Config.for_endpoint(endpoint="flyte.example.net"),
    default_project="flytesnacks",
    default_domain="development",
)

# Fetch workflow
workflow = remote.fetch_workflow(name="workflows.example.wf", version="v1")

# Execute
execution = remote.execute(
    workflow, inputs={"mean": 1}, execution_name="workflow-execution", wait=True
)

# Or use execution_name_prefix to avoid repeated execution names
execution = remote.execute(
    workflow, inputs={"mean": 1}, execution_name_prefix="flyte", wait=True
)
```

## Launch launchplan via {{< key kit_remote >}}

A launch plan can be launched via {{< key kit_remote >}} programmatically.

```python
import {{< key kit_import >}}
from flytekit.configuration import Config

# UnionRemote object is the main entrypoint to API
remote = {{<key kit_as>}}.{{< key kit_remote >}}(
    config=Config.for_endpoint(endpoint="flyte.example.net"),
    default_project="flytesnacks",
    default_domain="development",
)

# Fetch launch plan
lp = remote.fetch_launch_plan(
    name="workflows.example.wf", version="v1", project="flytesnacks", domain="development"
)

# Execute
execution = remote.execute(
    lp, inputs={"mean": 1}, execution_name="lp-execution", wait=True
)

# Or use execution_name_prefix to avoid repeated execution names
execution = remote.execute(
    lp, inputs={"mean": 1}, execution_name_prefix="flyte", wait=True
)
```

## Inspecting executions

With {{< key kit_remote >}}, you can fetch the inputs and outputs of executions and inspect them.

```python
import {{< key kit_import >}}
from flytekit.configuration import Config

# UnionRemote object is the main entrypoint to API
remote = {{<key kit_as>}}.{{< key kit_remote >}}(
    config=Config.for_endpoint(endpoint="flyte.example.net"),
    default_project="flytesnacks",
    default_domain="development",
)

execution = remote.fetch_execution(
    name="fb22e306a0d91e1c6000", project="flytesnacks", domain="development"
)

input_keys = execution.inputs.keys()
output_keys = execution.outputs.keys()

# The inputs and outputs correspond to the top-level execution or the workflow itself.
# To fetch a specific output, say, a model file:
model_file = execution.outputs["model_file"]
with open(model_file) as f:
    ...

# You can use UnionRemote.sync() to sync the entity object's state with the remote state during the execution run.
synced_execution = remote.sync(execution, sync_nodes=True)
node_keys = synced_execution.node_executions.keys()

# node_executions will fetch all the underlying node executions recursively.
# To fetch output of a specific node execution:
node_execution_output = synced_execution.node_executions["n1"].outputs["model_file"]
