---
title: Data handling
weight: 5
variants: +flyte -serverless -byoc -selfmanaged
---

# Data handling

In Flyte, data is categorized into metadata and raw data to optimize data handling and improve performance and security.

* **Metadata**: Small values, like integers and strings, are treated as “stack parameters” (passed by value).
  This metadata is globally accessible to Flyte components (FlytePropeller, FlyteAdmin, and other running pods/jobs).
  Each entry is limited to 10MB and is passed directly between tasks.
  On top of that, metadata allows in-memory computations for branches, partial outputs, and composition of multiple outputs as input for other tasks.

* **Raw data**: Larger data, such as files and dataframes, are treated as “heap parameters” (passed by reference).
  Flyte stores raw data in an object store (e.g., S3), uploading it on first use and passing only a reference thereafter.
  Tasks can then access this data via Flyte’s automated download or streaming, enabling efficient access to large datasets without needing to transfer full copies.

*Source code reference for auto-offloading value sizes limitation*:

Flyte’s data separation avoids bottlenecks and security risks:

* **Metadata** remains within Flyte’s control plane, making it accessible through the UI or CLI.

* **Raw data** is accessible only by tasks, stored securely in an external blob store, preventing Flyte’s control plane from directly handling large data files.

Moreover, a unique property of this separation is that all meta values are read by FlytePropeller engine and available on the UI or CLI from the control plane.

## Example

Consider a basic Flyte task:

```python
@{{< key kit_as >}}.task
def my_task(m: int, n: str, o: FlyteFile) -> pd.DataFrame:
   ...
```

In this task, `m`, `n`, and `o` are inputs: `m (int)` and `n (str)` are simple types, while `o` is a large, arbitrarily sized file.
Flyte treats each differently:

* **Metadata**: Small values like `m` and `n` are inlined within Flyte’s metadata and passed directly between tasks.

* **Raw data**: Objects like `o` and the output `pd.DataFrame` are offloaded to an object store (e.g., S3), with only references retained in metadata.

Flytekit TypeTransformers make it possible to use complex objects as if they are available locally, just like persistent filehandles.
However, the Flyte backend only deals with the references.

## Raw data path

Every task can read/write its own data files. If `FlyteFile` or any natively supported type like `pandas.DataFrame` is used, Flyte will automatically offload and download data from the configured object-store paths.
These paths are completely customizable per launch plan or execution.

The default **raw output path** (prefix in an object store like S3/GCS) can be configured during registration as shown in `flytectl register` files.
The argument `--outputLocationPrefix` allows us to set the destination directory for all the raw data produced.
Flyte will create randomized folders in this path to store the data.

To override the **raw output path* (prefix in an object store like S3/GCS),
you can specify an alternate location when invoking a Flyte execution in the launch form in the UI.

In the local demo cluster, the default raw output path is configured to be the root of the local bucket.
Hence Flyte will write all the raw data (reference types like blob, file, df/schema/parquet, etc.) under a path defined by the execution.

## `LiteralType` and `Literal`

### Serialization time

When a task is declared with inputs and outputs, Flyte extracts the interface of the task and converts it to an internal representation called a TypedInterface.
For each variable, a corresponding `LiteralType` is created.

For example, consider the following Python function interface:

```python
@{{< key kit_as >}}.task
def my_task(a: int, b: str) -> FlyteFile:
    """
    Description of my function

    :param a: My input integer
    :param b: My input string
    :return: My output file
    """
```

It is transformed the following:

```python
  interface {
  inputs {
    variables {
      key: "a"
      value {
        type {
          simple: INTEGER
        }
        description: "My input Integer"
      }
    }
    variables {
      key: "b"
      value {
        type {
          simple: STRING
        }
        description: "My input string"
      }
    }
  }
  outputs {
    variables {
      key: "o0"
      value {
        type {
          blob {
          }
        }
        description: "My output File"
      }
    }
  }
}
```

### Runtime

At runtime, data passes through Flyte using `Literal` where the values are set.
For files, the corresponding `Literal` is called `LiteralBlob (Blob)` which is a binary large object.
Many different objects can be mapped to the underlying `Blob` or `Struct` types.
For example, an image is a `Blob`, a `pandas.DataFrame` is a `Blob `of type `parquet`, etc.

## Data movement

Flyte is primarily a dataflow engine.
It enables movement of data and provides an abstraction to enable movement of data between different languages.

One implementation of Flyte is the current workflow engine.

The workflow engine is responsible for moving data from a previous task to the next task.
As explained previously, Flyte only deals with metadata and not the actual raw data.
The illustration below explains how data flows from engine to the task and how that is transferred between tasks.
The medium to transfer the data can change, and will change in the future.
We could use fast metadata stores to speed up data movement or exploit locality.

### Between FlytePropeller and tasks

![Flyte data movement](../_static/images/architecture/data-handling/flyte-data-movement.png)

### Between tasks

![Flyte data transfer](../_static/images/architecture/data-handling/flyte-data-transfer.png)

### Practical example

Let’s consider a simple example where we have some tasks that needs to operate huge dataframes.

The first task reads a file from the object store, shuffles the data, saves to local disk, and passes the path to the next task:

```python
@{{< key kit_as >}}.task()
def task_read_and_shuffle_file(input_file: FlyteFile) -> FlyteFile:
    """
    Reads the input file as a DataFrame, shuffles the rows, and writes the shuffled DataFrame to a new file.
    """
    input_file.download()
    df = pd.read_csv(input_file.path)

    # Shuffle the DataFrame rows
    shuffled_df = df.sample(frac=1).reset_index(drop=True)

    output_file_path = "data_shuffle.csv"
    shuffled_df.to_csv(output_file_path, index=False)

    return FlyteFile(output_file_path)
```

The second task reads the file from the previous task, removes a column, saves to local disk, and returns the path:

```python
@{{< key kit_as >}}.task()
def task_remove_column(input_file: FlyteFile, column_name: str) -> FlyteFile:
    """
    Reads the input file as a DataFrame, removes a specified column, and outputs it as a new file.
    """
    input_file.download()
    df = pd.read_csv(input_file.path)

    # remove column
    if column_name in df.columns:
        df = df.drop(columns=[column_name])

    output_file_path = "data_finished.csv"
    df.to_csv(output_file_path, index=False)

    return FlyteFile(output_file_path)
```

And here is the workflow:

```python
@{{< key kit_as >}}.workflow
def wf() -> FlyteFile:
    existed_file = FlyteFile("s3://custom-bucket/data.csv")
    shuffled_file = task_read_and_shuffle_file(input_file=existed_file)
    result_file = task_remove_column(input_file=shuffled_file, column_name="County")
    return result_file
```

This example shows how to access an existing file in a MinIO bucket from the Flyte local demo cluster and pass it between tasks with FlyteFile.
When a workflow outputs a local file as a FlyteFile, Flyte automatically uploads it to MinIO and provides an S3 URL for downstream tasks, no manual uploads needed.

### Bringing in your own datastores for raw data

Flytekit has a pluggable data persistence layer.
This is driven by protocol.
For example, it is theoretically possible to use S3 `s3://` for metadata and GCS `gcs://` for raw data.
It is also possible to create your own protocol `my_fs://`, to change how data is stored and accessed.
But for metadata, the data should be accessible to Flyte control plane.

Data persistence is also pluggable. By default, it supports all major blob stores and uses an interface defined in Flytestdlib.

### Deleting raw data in your own datastores

Flyte does not offer a direct function to delete raw data stored in external datastores like S3 or GCS.
However, you can manage deletion by configuring a lifecycle policy within your datastore service.

If caching is enabled in your Flyte task, ensure that the `max-cache-age` is set to be shorter than the lifecycle policy in your datastore to prevent potential data inconsistency issues.