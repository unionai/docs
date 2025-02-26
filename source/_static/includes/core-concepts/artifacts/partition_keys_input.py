from datetime import datetime

import pandas as pd
from typing_extensions import Annotated
import union
from flytekit.core.artifact import Inputs, Granularity

pandas_image = union.ImageSpec(
    packages=["pandas==2.2.2"]
)

BasicArtifact = union.Artifact(
    name="my_basic_artifact",
    time_partitioned=True,
    time_partition_granularity=Granularity.HOUR,
    partition_keys=["key1"]
)


@union.task(container_image=pandas_image)
def t1(
    key1: str, dt: datetime
) -> Annotated[pd.DataFrame, BasicArtifact(key1=Inputs.key1)]:
    df = pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
    return BasicArtifact.create_from(
        df,
        time_partition=dt,
        key1=key1
    )


@union.workflow
def wf(dt: datetime, val: str):
    t1(key1=val, dt=dt)
