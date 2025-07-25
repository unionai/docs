---
title: Serving a Model from a Workflow With FastAPI
weight: 2
variants: -flyte +serverless +byoc +selfmanaged
---

# Serving a Model from a Workflow With FastAPI

In this section, we create a {{< key product_name >}} app to serve a scikit-learn model created by a {{< key product_name >}} workflow
using `FastAPI`.

## Example app

In this example, we first use a {{< key product_name >}} workflow to train a model and output it as a {{< key product_name >}} `Artifact`.
We then use a {{< key product_name >}} app to serve the model using `FastAPI`.

In a local directory, create the following files:

```shell
├── app.py
├── main.py
└── train_wf.py
```

## App configuration

In the code below, we declare the resources, runtime image, and FastAPI app that
exposes a `/predict` endpoint.

```python
"""A {{< key product_name >}} app that uses FastAPI to serve model created by a {{< key product_name >}} workflow."""

import os
import {{< key kit_import >}}
import joblib
from fastapi import FastAPI

SklearnModel = union.Artifact(name="sklearn-model")

# The `ImageSpec` for the container that will run the `App`, where `union-runtime`
# must be declared as a dependency. In addition to any other dependencies needed
# by the app code. Set the environment variable `REGISTRY` to be the URI for your
# container registry. If you are using `ghcr.io` as your registry, make sure the
# image is public.
image_spec = union.ImageSpec(
    name="union-serve-sklearn-fastapi",
    packages=["union-runtime>=0.1.10", "scikit-learn==1.5.2", "joblib==1.5.1", "fastapi[standard]"],
    registry=os.getenv("REGISTRY"),
)

ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    model_file = os.getenv("SKLEARN_MODEL")
    ml_models["model"] = joblib.load(model_file)
    yield

app = FastAPI(lifespan=lifespan)

# The `App` declaration, which uses the `ImageSpec` declared above.
# Your core logic of the app resides in the files declared in the `include`
# parameter, in this case, `main.py`. Input artifacts are declared in the
# `inputs` parameter
fast_api_app = union.app.App(
    name="simple-fastapi-sklearn",
    inputs=[
        union.app.Input(
            value=SklearnModel.query(),
            download=True,
            env_var="SKLEARN_MODEL",
        )
    ],
    container_image=image_spec,
    framework_app=app,
    limits=union.Resources(cpu="1", mem="1Gi"),
    port=8082,
)

@app.get("/predict")
async def predict(x: float, y: float) -> float:
    result = ml_models["model"]([[x, y]])
    return {"result": result}

```

Note that the Artifact is provided as an `Input` to the App definition. With `download=True`,
the model is downloaded to the container's working directory. The full local path to the
model is set to `SKLEARN_MODEL` by the runtime.

During startup, the FastAPI app loads the model using the `SKLEARN_MODEL` environment
variable. Then it serves an endpoint at `/predict` that takes two float inputs and
returns a float result.


## Training workflow

The training workflow trains a random forest regression and saves it to a {{< key product_name >}}
`Artifact`.

```python
"""A {{< key product_name >}} workflow that trains a model."""

import os
from pathlib import Path
from typing import Annotated

import joblib
from sklearn.datasets import make_regression
from sklearn.ensemble import RandomForestRegressor

import {{< key kit_import >}}

# Declare the `Artifact`.
SklearnModel = union.Artifact(name="sklearn-model")

# The `ImageSpec` for the container that runs the tasks.
# Set the environment variable `REGISTRY` to be the URI for your container registry.
# If you are using `ghcr.io` as your registry, make sure the image is public.
image_spec = union.ImageSpec(
    packages=["scikit-learn==1.5.2", "joblib==1.5.1"],
    registry=os.getenv("REGISTRY"),
)

# The `task` that trains a `RandomForestRegressor` model.
@{{< key kit_as >}}.task(
    limits=union.Resources(cpu="2", mem="2Gi"),
    container_image=image_spec,
)
def train_model() -> Annotated[union.FlyteFile, SklearnModel]:
    """Train a RandomForestRegressor model and save it as a file."""
    X, y = make_regression(n_features=2, random_state=42)
    working_dir = Path(union.current_context().working_directory)
    model_file = working_dir / "model.joblib"

    rf = RandomForestRegressor().fit(X, y)
    joblib.dump(rf, model_file)
    return model_file
```

## Run the example

To run this example you will need to register and run the workflow first:

```shell
$ {{< key cli >}} run --remote train_wf.py train_model
```


This task trains a `RandomForestRegressor`, saves it to a file, and uploads it to
a {{< key product_name >}} `Artifact`. This artifact is retrieved by the FastAPI app for
serving the model.

![scikit-learn Artifact](../../../_static/images/user-guide/core-concepts/serving/fastapi-sklearn/sklearn-artifact.png)

Once the workflow has completed, you can deploy the app:

```shell
$ {{< key cli >}} deploy apps app.py simple-fastapi-sklearn
```


The output displays the console URL and endpoint for the FastAPI App:

```shell
✨ Deploying Application: simple-fastapi-sklearn
🔎 Console URL: https://<union-host-url>/org/...
[Status] Pending: OutOfDate: The Configuration is still working to reflect the latest desired
specification.
[Status] Pending: IngressNotConfigured: Ingress has not yet been reconciled.
[Status] Pending: Uninitialized: Waiting for load balancer to be ready
[Status] Started: Service is ready

🚀 Deployed Endpoint: https://<unique-subhost>.apps.<union-host-url>
```


You can see the Swagger docs of the FastAPI endpoint, by going to `/docs`:

![scikit-learn FastAPI App](../../../_static/images/user-guide/core-concepts/serving/fastapi-sklearn/sklearn-fastapi.png)
