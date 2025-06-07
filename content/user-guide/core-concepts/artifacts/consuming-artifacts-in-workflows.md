---
title: Consuming artifacts in workflows
weight: 3
variants: -flyte +serverless +byoc +selfmanaged
---

# Consuming artifacts in workflows

## Defining a workflow that consumes an artifact

You can define a workflow that consumes an artifact by defining a query and passing it as an input to the consuming workflow.

The following code defines a query, `data_query`, that searches across all versions of `BasicArtifact` that match the partition values. This query binds parameters to the workflow's `key1` and `time_partition` inputs and returns the most recent version of the artifact.

{{< variant byoc selfmanaged flyte >}}
{{< markdown >}}
> [!NOTE]
> To use the example code on this page, you will need to add your `registry` to the `pandas_image` ImageSpec block.
{{< /markdown >}}
{{< /variant >}}

```python
# query.py

from datetime import datetime

import pandas as pd
import {{< key kit_import >}}
from flytekit.core.artifact import Inputs

pandas_image = {{< key kit_as >}}.ImageSpec(
    packages=["pandas==2.2.2"]
)

BasicArtifact = {{< key kit_as >}}.Artifact(
    name="my_basic_artifact"
)


@{{< key kit_as >}}.task(container_image=pandas_image)
def t1(key1: str, dt: datetime, data: pd.DataFrame):
    print(f"key1: {key1}")
    print(f"Date: {dt}")
    print(f"Data retrieved from query: {data}")


data_query = BasicArtifact.query(
    time_partition=Inputs.dt,
    key1=Inputs.key1,
)


@{{< key kit_as >}}.workflow
def query_wf(
    key1: str,
    dt: datetime,
    data: pd.DataFrame = data_query
):
    t1(key1=key1, dt=dt, data=data)
```
<!-- TODO :emphasize-lines: 23-26,35 -->

You can also directly reference a particular artifact version in a query using the `get()` method:

```python
data = BasicArtifact.get(<organization>/<domain>/BasicArtifact@<artifact-version>)
```

> [!NOTE]
> For a full list of Artifact class methods, see the [Artifact API documentation]().
<!-- TODO: Add link to API -->

## Launching a workflow that consumes an artifact

To launch a workflow that consumes an artifact as one of its inputs, navigate to the workflow in the UI and click **Launch Workflow**:

![Launch workflow UI with artifact query](../../../_static/images/user-guide/core-concepts/artifacts/consuming-artifacts-in-workflows/launch-workflow-artifact-query.png)

In the `query_wf` example, the workflow takes three inputs: `key1`, `dt`, and a `BasicArtifact` artifact query. In order to create the workflow execution, you would enter values for `key1` and `dt` and click **Launch**. The artifacts service will supply the latest version of the `BasicData` artifact that meets the partition query criteria.

You can also override the artifact query from the launch form by clicking **Override**, directly supplying the input that the artifact references (in this case, a blob store URI), and clicking **Launch**:

![Launch workflow UI with artifact query override](../../../_static/images/user-guide/core-concepts/artifacts/consuming-artifacts-in-workflows/launch-workflow-artifact-query-override.png)