---
title: Migrating from Kubeflow to Flyte
weight: 19
variants: +flyte -serverless -byoc -selfmanaged
---

# Migrating from Kubeflow to Flyte

Kubeflow Pipelines served its purpose, but it's time to level up. Flyte offers a more robust, scalable, and developer-friendly experience for orchestrating machine learning and data workflows. Whether you're tired of wrestling with pipeline definitions or looking for stronger type safety and seamless data passing, this guide will help you transition smoothly—and confidently—from Kubeflow Pipelines to Flyte Workflows.

For this migration guide, we will use this example kubeflow pipeline to walk you through the following. 

{{< download "/docs/flyte/code/example_kubeflow_pipeline.py" "example_kubeflow_pipeline.py" >}}

## Components vs Tasks

In Kubeflow, a component is a set of code used to modularize your pipeline. It should perform one step inside a data/ML pipeline, such as data, preprocessing, model training, etc. In the Flyte domain, this concept is called a Flyte Task. In this chapter, we will convert KFP components to Flyte tasks.

Let’s have a look at the first component in this pipeline called `fetch_dataset`:

```python
@kfp.dsl.component
def fetch_dataset(
          dataset, data_dir, lakefs_endpoint = "https://example.com"
      ):
          import logging
          import os
          import subprocess
          from pathlib import Path

          # LOGS
          logging.basicConfig(level=logging.INFO)

          # Assertions to help users
          assert os.getenv("AWS_ACCESS_KEY_ID") is not None, logging.info(
              "There is no AWS Key set in environment"
          )
          assert os.getenv("AWS_SECRET_ACCESS_KEY") is not None, logging.info(
              "There is no AWS Secret set in environment"
          )

          # Constants
          DOWNLOAD_DIR = data_dir
          DATASET = dataset

          loc = Path(data_dir)
          allfiles = [i for i in loc.rglob("**/*")]

          # Check for persistent version file
          if len(allfiles)>1:
              logging.info("Data exists in target dir, skipping download.")
              logging.info(f"Downloaded data folder structure: {os.listdir(DOWNLOAD_DIR)}")
              logging.info(
                  "If there is no data in your directories, check to make sure that you have the right credentials, then delete the directories that were created and have no data in them."
              )
              logging.info("Good luck and have fun modeling!")
          else:
              # Download data if not already there
              logging.info(f"No local data found. Getting data from {lakefs_endpoint}")
              command = (
                  f"aws s3 cp {DATASET} {DOWNLOAD_DIR} --debug --recursive --endpoint {lakefs_endpoint}"
              )
              subprocess.run(
                  command,
                  stdout=None,
                  universal_newlines=True,
                  shell=True,
                  check=True,
                  stderr=subprocess.STDOUT,
              )
              logging.info(f"Downloaded data folder structure: {os.listdir(DOWNLOAD_DIR)}")
          return
```

As you can see, the purpose of this component is to download a dataset from an S3 compatible object store. In Flyte, there is no need to author such tasks, since Flyte has features included called [Flytefile, Flytedirectory](https://www.union.ai/docs/flyte/user-guide/data-input-output/flyte-file-and-flyte-directory/), which is abstracting the upload/download of files and directories.

Lets have a look at the second component `train_conv_model:`

```python
def train_conv_model(pvc_alias: str) -> Dict[str, dict]:
    # Import all the libraries
    import datetime
    import json
    import logging
    import os
    from pathlib import Path
    from typing import Dict
    import tensorflow as tf
    from tensorflow.keras.callbacks import History
    from tensorflow.keras.preprocessing.image import ImageDataGenerator
    DATA = Path().home() / f"{pvc_alias}/"

    # Set directories on volume
    TRAINING_DIR = f"{DATA}/train"
    TEST_DIR = f"{DATA}/test"

    # Make logging visible in Panel
    logging.basicConfig(level=logging.INFO)

    # Instantiate data loaders
    train = tf.keras.utils.image_dataset_from_directory(
        TRAINING_DIR, image_size=(150, 150), color_mode="rgb"
    )
    test = tf.keras.utils.image_dataset_from_directory(
        TEST_DIR, image_size=(150, 150), color_mode="rgb"
    )
    logging.info("Data Generators built")

    # Define Model Architecture
    model = tf.keras.models.Sequential(
        [
            tf.keras.layers.Rescaling(1.0 / 255, input_shape=(150, 150, 3)),
            tf.keras.layers.Conv2D(filters=64, activation="relu", kernel_size=3),
            tf.keras.layers.MaxPool2D(pool_size=2, strides=2),
            tf.keras.layers.Conv2D(filters=32, activation="relu", kernel_size=3),
            tf.keras.layers.MaxPool2D(pool_size=2, strides=2),
            tf.keras.layers.Conv2D(filters=16, activation="relu", kernel_size=3),
            tf.keras.layers.MaxPool2D(pool_size=2, strides=2),
            tf.keras.layers.Conv2D(filters=128, activation="relu", kernel_size=3),
            tf.keras.layers.MaxPool2D(pool_size=2, strides=2),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(units=512, activation="relu"),
            tf.keras.layers.Dense(units=20, activation="softmax"),
        ]
    )

    model.compile(
        optimizer="adam",
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=["accuracy"],
    )

    logging.info(model.summary())
    
    # Add experiment tracking code here

    # Create History object for metrics logging
    history = History()

    # Fit Model
    hist = model.fit(train, validation_data=test, epochs=5, callbacks=[history])

    logging.info(hist.history)

    MODEL_DIR = "shire-clothing"

    version = 2
    export_path = os.path.join(os.sep, "data", MODEL_DIR, str(version), str(version))

    # Save model Binary
    tf.keras.models.save_model(
        model,
        export_path,
        overwrite=True,
        include_optimizer=True,
        save_format=None,
        signatures=None,
        options=None,
    )

    # Return information from model for next stage in pipeline
    return json.dumps({"path": export_path, "metrics": hist.history})
```

Looks like a regular model training step using tensorflow. Lets walk through the steps on migrating this Kubeflow component to a Flyte task.

### Set up task decorator

The first thing you want to do is installing the python Flyte sdk called `flytekit` in your local Python environment. Having that in place, we can swap the kfp decorator with a Flyte task decorator. This is how the `train_conv_model` task definition would look like: 

```python
from flytekit import workflow, task, FlyteDirectory, FlyteFile
from dataclasses import dataclass

@dataclass
class DemoModel:
    file: FlyteFile
    metrics: dict

@task
def train_conv_model(dataset: FlyteDirectory = "s3://my/datadir") -> DemoModel:
		# Import all the libraries
    # ...

    dataset.download() # explicitly triggers remote dir download
    
    TRAINING_DIR = f"{dataset}/train"
    TEST_DIR = f"{dataset}/test"
    # same model training logic
    # ...
    tf.keras.models.save_model(
        model,
        export_path,
        overwrite=True,
        include_optimizer=True,
        save_format=None,
        signatures=None,
        options=None,
    )
    return DemoModel(file=FlyteFile(path=export_path), metrics=hist.history)
```

At first you can see the I/O definition of the python function changed to make this a Flyte task. Tasks have strongly typed inputs and outputs, which are validated at registration time. This helps to catch bugs early and ensures that the data passing through tasks and workflows is compatible with the explicitly stated types.

By specifying the dataset input as a `FlyteDirectory` and adjusting the logic of `train_conv_model` just a little we integrated the downloading aspect of first component already.


> 💡
`dataset.download()`: Certain read / list operations on `FlyteFile` and `FlyteDirectory` (e.g. `pd.read_parquet()` / `os.listdir()`) automatically trigger the actual download in the task. If none of these operations are being used, we can always manually trigger the download via `.download()`.


Lastly, the cleanest and most maintainable way to return multiple outputs from a Flyte task is by using Python `dataclasses`. This approach makes it incredibly convenient for downstream tasks and workflows to consume and work with the results.

Check out these [docs](https://www.union.ai/docs/flyte/user-guide/core-concepts/tasks/) to dive deeper into tasks.  If you're looking to scale and parallelize task executions across a collection of inputs, Map tasks are essential reading.

### Passing Data

Passing around data is definitely one of the limiting factors in Kubeflow since only Python-native data types are supported and the syntax to achieve this is not intuitive for most Python developers. The only way of passing around more complex datatypes in bigger sizes is to mount persistent volumes to each component like to be seen in the example pipeline:

```python
train_model_r1 = (
        train_model_op1("/data/")
        .add_pvolumes({"/data/": dsl.PipelineVolume(pvc=PERSISTENT_VOLUME_CLAIM_NAME)})
)
```

This ends up in a lot of boilerplate code and developers have to constantly think of the file structure in that volume.

Good news! In Flyte, developers simply do not have to care about passing data at all. You just return data from one task to next like you would do in a regular python function:

```python
@task
def get_data() -> pd.DataFrame:
    df = pd.DataFrame({"a":[1,2,3]})
    return df

@task
def print_data(df:pd.DataFrame):
    print(df)

@workflow
def wf():
    df = get_data()
    print_data(df=df)
```

Flyte automatically serializes and deserializes task input/outputs while offloading the actual data to the associated object storage - goodbye volumes!

> ☝️
This only applies to remote execution on a Flyte cluster. When running a Flyte workflow locally (yes, that is possible), all data remains in memory.


### Dependency Management

When going for anything more advanced than writing a hello world pipeline, we want to make use of all the amazing libraries in the python ecoystem. In the `train_conv_model` component in our example, we are gonna use `tensorflow` to train a model. Build your container images in kubeflow with all the necessary dependencies can be a tedious and time consuming process.

```python
train_model_op1 = comp.func_to_container_op(
    train_conv_model,
    base_image="https://example.com/tensorflow:latest",
    packages_to_install=["pillow", "scipy"],
)
```

You would need to build and start a container build process in some other system to provide a base image and specify the required packages to install at runtime. This might be the reason why Data Scientists are often reluctant to hear the term “Container Orchestration”. It typically implies setting up a container build tool out of the box, wasting compute resources on dependencies installations over and over again on runtime, and manually adjusting the base_image (e.g. version changes) on every iteration.

In Flyte instead, you just specify your required dependencies and everything else is taken care of. Introducing [ImageSpec](https://www.union.ai/docs/flyte/user-guide/development-cycle/image-spec/):

```python
from flytekit import workflow, task, FlyteDirectory, ImageSpec, FlyteFile
# ...
container_image = ImageSpec(
    name="my-demo-image",
    registry="ghcr.io/fiedlernr9",
    packages=["tensorflow", "pillow", "scipy"],
)

@task(container_image=container_image)
def train_conv_model(dataset: FlyteDirectory = "s3://my/datadir") -> DemoModel:
				...
```

When running this remotely, ImageSpec will build the container image for you, push it to the specified registry and assign it to the task executed on a Flyte cluster. On subsequent runs, ImageSpec will check if a container image with that specific configuration already exists and reuse that for your task executions. As a result, ImageSpec guarantees to never build the same image twice and developers dont have to care about container image tags. 

> ☝️
Again, this applies for remote executions! To run locally, just install the dependencies in your local Python environment.

With ImageSpec you can also specify custom base images, `requirements.txt`, environment variables, apt packages, CUDA environments, and much more. Check out these [docs](https://www.union.ai/docs/flyte/api-reference/flytekit-sdk/packages/flytekit.image_spec.image_spec/#flytekitimage_specimage_specimagespec) for all the available options. 

### Environment Settings

With dependencies covered, we are almost there! When building ML workflows, controlling the execution environment is key to ensuring reproducibility, efficiency, and security. Whether it's setting environment variables, defining resource limits, or mounting secrets, customizing the environment allows you to fine-tune how your components or tasks run. 

Looking at our example, this is how it's done in Kubeflow:

```python
train_model_r1 = (
        train_model_op1("/data/")
        .add_pvolumes({"/data/": dsl.PipelineVolume(pvc=PERSISTENT_VOLUME_CLAIM_NAME)})
        .set_cpu_limit('2000m')
        .set_memory_limit('2Gi')
        .set_retry(2)
        .after(fetch_data_r)
    )
```

In Flyte, all these configurations are to be made on the task decorator level - no need for another wrapper!

```python
from flytekit import workflow, task, FlyteDirectory, ImageSpec, FlyteFile, Resources

@task(container_image=container_image, requests=Resources(cpu=2), limits=Resources(mem="2Gi"), retries=2)
def train_conv_model(dataset: FlyteDirectory) -> DemoModel:
```

Check out these [docs](https://www.union.ai/docs/flyte/api-reference/flytekit-sdk/packages/flytekit.core.task/#task) to learn how to configure caching, environment variables, secrets, timeouts and more for Flyte tasks!

## Pipelines vs Workflows

A Kubeflow pipeline organizes components into a computational directed acyclic graph (DAG), establishing how they run and interact based on their dependencies. The same applies for Flyte Workflows and Tasks.

Lets see how this looks for our `workshop_pipeline` example pipeline:

```python
@dsl.pipeline(name=PIPELINE_NAME, description="fetch data, train model, save model to MR, serve model")
def workshop_pipeline():
    fetch_data_r = (
        fetch_data_op("s3://kfp-intro-bywater/cleaned-empties/", "/data/")
        .add_env_variable(
            k8s_client_helper.env_from_secret(
                "AWS_ACCESS_KEY_ID", "kfp-intro-lakefs", "AWS_ACCESS_KEY_ID"
            )
        )
        .add_env_variable(
            k8s_client_helper.env_from_secret(
                "AWS_SECRET_ACCESS_KEY", "kfp-intro-lakefs", "AWS_SECRET_ACCESS_KEY"
            )
        )
        .add_env_variable(
            k8s_client_helper.env_from_secret("AUTH_TOKEN", "kfp-intro-rat", "AUTH_TOKEN")
        )
        .add_pvolumes({"/data/": dsl.PipelineVolume(pvc=PERSISTENT_VOLUME_CLAIM_NAME)})
    )

    train_model_r1 = (
        train_model_op1("/data/")
        .add_pvolumes({"/data/": dsl.PipelineVolume(pvc=PERSISTENT_VOLUME_CLAIM_NAME)})
        .set_cpu_limit('2000m')
        .set_memory_limit('2Gi')
        .set_retry(2)
        .after(fetch_data_r)
    )
```

Quite a lot of code to chain two components together right? Let me show you how this would look like in our optimised Flyte workflow:

```python
@workflow
def wf(
    dataset_dir: FlyteDirectory = "s3://my-demo-bucket/flower_photos",
) -> DemoModel:
    return train_conv_model(dataset=dataset_dir)
```

Just like Flyte tasks, Flyte workflows are strongly typed and defined as standard Python functions, annotated with a workflow decorator. Within a workflow, tasks are composed by chaining them together much like you would do in a typical Python `main` function. By clearly connecting task outputs to subsequent inputs, Flyte automatically constructs the underlying DAG at registration time and manages all data passing between tasks. 

For more advanced use cases, you sometimes want to nest workflow in each other or dynamically fan out workflows or tasks. Check out these [docs](https://www.union.ai/docs/flyte/user-guide/core-concepts/workflows/) and learn how to use other types of workflows like subworkflows or dynamic workflows.

### Run your DAG

Finally, let’s compare how Kubeflow and Flyte handle the execution of DAGs both locally and remotely. With Kubeflow, there is no built-in way to run pipelines locally. Executing a pipeline on a Kubeflow cluster typically requires a significant amount of boilerplate: initializing a client, creating an experiment, compiling and zipping the pipeline code, and uploading it for execution. In fact, the `run_pipeline` function in our example spans nearly 50 lines of code just to handle this process.

In contrast, Flyte abstracts away the complexity of deploying workflows. Developers can begin by running their pipelines locally as standard Python code, without needing to worry about the underlying orchestration. This makes iteration faster and significantly lowers the barrier to getting started.

The most convenient way of executing a workflow locally is to use the pyflyte cli commands:
`pyflyte run example_flyte_workflow.py wf --dataset_dir s3://my-demo-bucket/flower_photos`

In this example we are executing the Flyte entitiy `wf` in the `example_flyte_workflow.py` file. There is also the possibility to execute singular tasks - just switch `wf` with a task name to achieve that.

Okay but executing locally is the easy part right? How do I execute this specific workflow on a Flyte Cluster?

`pyflyte run -—remote example_flyte_workflow.py wf --dataset_dir s3://my-demo-bucket/flower_photos` 

Adding the —remote flag is all you need!

Check out these [docs](https://www.union.ai/docs/flyte/api-reference/pyflyte-cli/#hahahugoshortcode4s16hbhb-cli-configuration-search-path) to learn all about pyflyte cli command and how to further interact with your Flyte cluster.

> 🎉
Congrats on finishing this migration guide. Please reach out to the Union team if you have any further questions on migrating Kubeflow pipelines to Flyte workflows.


Take a look at the Flyte workflow shown below — it mirrors the same logic as the original Kubeflow pipeline, but with some clear advantages:

- It's significantly more **pythonic**, making it easier for developers to read, understand, and extend.
- The code is about **one-third the size** of the Kubeflow version.
- We've introduced **container image build tooling** to streamline deployments.
- By leveraging **FlyteDirectories**, we reduced the number of tasks from two to one — simplifying the overall structure.
- …and much more!

{{< download "/docs/flyte/code/example_flyte_workflow.py" "example_flyte_workflow.py" >}}
