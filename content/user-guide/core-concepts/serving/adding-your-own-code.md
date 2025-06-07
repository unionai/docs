---
title: Adding your own code
weight: 1
variants: -flyte +serverless +byoc +selfmanaged
---

# Adding your own code

In the introductory section we saw how to define and deploy a simple Streamlit app.
The app deployed was the default hello world Streamlit example app.
In this section, we will expand on this by adding our own custom code to the app.

## Example app

We will initialize the app in `app.py` as before, but now we will add two files containing our own code, `main.py` and `utils.py`.

In a local directory, create the following files:

```shell
├── app.py
├── main.py
└── utils.py
```

## App declaration

The file `app.py` contains the app declaration:

```python
"""A {{< key product_name >}} app with custom code"""

import os
import {{< key kit_import >}}

# The `ImageSpec` for the container that will run the `App`.
# `union-runtime` must be declared as a dependency,
# in addition to any other dependencies needed by the app code.
# Set the environment variable `REGISTRY` to be the URI for your container registry.
# If you are using `ghcr.io` as your registry, make sure the image is public.
image = union.ImageSpec(
    name="streamlit-app",
    packages=["streamlit==1.41.1", "union-runtime>=0.1.10", "pandas==2.2.3", "numpy==2.2.3"],
    registry=os.getenv("REGISTRY"),
)

# The `App` declaration.
# Uses the `ImageSpec` declared above.
# Your core logic of the app resides in the files declared
# in the `include` parameter, in this case, `main.py` and `utils.py`.
app = union.app.App(
    name="streamlit-custom-code",
    container_image=image,
    args="streamlit run main.py --server.port 8080",
    port=8080,
    include=["main.py", "utils.py"],
    limits=union.Resources(cpu="1", mem="1Gi"),
)
```


Compared to the first example we have added one more parameter:

* `include`: A list of files to be added to the container at deployment time, containing the custom code that defines the specific functionality of your app.

## Custom code

In this example we include two files containing custom logic: `main.py` and `utils.py`.

The file `main.py` contains the bulk of our custom code:

```python
"""Streamlit App that plots data"""
import streamlit as st
from utils import generate_data

all_columns = ["Apples", "Orange", "Pineapple"]
with st.container(border=True):
    columns = st.multiselect("Columns", all_columns, default=all_columns)

all_data = st.cache_data(generate_data)(columns=all_columns, seed=101)

data = all_data[columns]

tab1, tab2 = st.tabs(["Chart", "Dataframe"])
tab1.line_chart(data, height=250)
tab2.dataframe(data, height=250, use_container_width=True)
```


The file `utils.py` contains a supporting data generating function that is imported into the file above

```python
"""Function to generate sample data."""
import numpy as np
import pandas as pd


def generate_data(columns: list[str], seed: int = 42):
    rng = np.random.default_rng(seed)
    data = pd.DataFrame(rng.random(size=(20, len(columns))), columns=columns)
    return data
```

## Deploy the app

Deploy the app with:

```shell
$ {{< key cli >}} deploy apps app.py streamlit-custom-code
```


The output displays the console URL and endpoint for the Streamlit app:

```shell
✨ Deploying Application: streamlit-custom-code
🔎 Console URL:
https://<union-host-url>/org/...
[Status] Pending: OutOfDate: The Configuration is still working to reflect the latest desired
specification.
[Status] Started: Service is ready

🚀 Deployed Endpoint: https://<unique-subhost>.apps.<union-host-url>
```


Navigate to the endpoint to see the Streamlit App!

![Streamlit App](../../../_static/images/user-guide/core-concepts/serving/custom-code-streamlit.png)

## App deployment with included files

When a new app is deployed for the first time (i.e., there is no app registered with the specified `name`),
a container is spun up using the specified `container_image` and the files specified in `include` are
copied into the container. The `args` is the then executed in the container, starting the app.

If you alter the `include` code you need to re-deploy your app.
When `{{< key cli >}} deploy apps` is called using an app name that corresponds to an already existing app,
the app code is updated in the container and the app is restarted.

You can iterate on your app easily by changing your `include` code and re-deploying.

Because there is a slight performance penalty involved in copying the `include` files into the container,
you may wish to consolidate you code directly into custom-built image once you have successfully iterated to production quality.
