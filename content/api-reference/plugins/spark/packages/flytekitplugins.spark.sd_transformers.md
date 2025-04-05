---
title: flytekitplugins.spark.sd_transformers
version: 0.0.0+develop
variants: +flyte +byoc +byok +serverless
layout: py_api
---

# flytekitplugins.spark.sd_transformers

## Directory

### Classes

| Class | Description |
|-|-|
| [`ParquetToSparkDecodingHandler`](.././flytekitplugins.spark.sd_transformers#flytekitpluginssparksd_transformersparquettosparkdecodinghandler) | Helper class that provides a standard way to create an ABC using. |
| [`SparkDataFrameRenderer`](.././flytekitplugins.spark.sd_transformers#flytekitpluginssparksd_transformerssparkdataframerenderer) | Render a Spark dataframe schema as an HTML table. |
| [`SparkToParquetEncodingHandler`](.././flytekitplugins.spark.sd_transformers#flytekitpluginssparksd_transformerssparktoparquetencodinghandler) | Helper class that provides a standard way to create an ABC using. |

### Variables

| Property | Type | Description |
|-|-|-|
| `PARQUET` | `str` |  |

## flytekitplugins.spark.sd_transformers.ParquetToSparkDecodingHandler

Helper class that provides a standard way to create an ABC using
inheritance.


```python
def ParquetToSparkDecodingHandler()
```
Extend this abstract class, implement the decode function, and register your concrete class with the
StructuredDatasetTransformerEngine class in order for the core flytekit type engine to handle
dataframe libraries. This is the decoder interface, meaning it is used when there is a Flyte Literal value,
and we have to get a Python value out of it. For the other way, see the StructuredDatasetEncoder



### Methods

| Method | Description |
|-|-|
| [`decode()`](#decode) | This is code that will be called by the dataset transformer engine to ultimately translate from a Flyte Literal. |


#### decode()

```python
def decode(
    ctx: flytekit.core.context_manager.FlyteContext,
    flyte_value: flytekit.models.literals.StructuredDataset,
    current_task_metadata: flytekit.models.literals.StructuredDatasetMetadata,
) -> n: This function can either return an instance of the dataframe that this decoder handles, or an iterator
```
This is code that will be called by the dataset transformer engine to ultimately translate from a Flyte Literal
value into a Python instance.



| Parameter | Type |
|-|-|
| `ctx` | `flytekit.core.context_manager.FlyteContext` |
| `flyte_value` | `flytekit.models.literals.StructuredDataset` |
| `current_task_metadata` | `flytekit.models.literals.StructuredDatasetMetadata` |

### Properties

| Property | Type | Description |
|-|-|-|
| `protocol` |  |  |
| `python_type` |  |  |
| `supported_format` |  |  |

## flytekitplugins.spark.sd_transformers.SparkDataFrameRenderer

Render a Spark dataframe schema as an HTML table.


### Methods

| Method | Description |
|-|-|
| [`to_html()`](#to_html) |  |


#### to_html()

```python
def to_html(
    df: pyspark.sql.dataframe.DataFrame,
) -> str
```
| Parameter | Type |
|-|-|
| `df` | `pyspark.sql.dataframe.DataFrame` |

## flytekitplugins.spark.sd_transformers.SparkToParquetEncodingHandler

Helper class that provides a standard way to create an ABC using
inheritance.


```python
def SparkToParquetEncodingHandler()
```
Extend this abstract class, implement the encode function, and register your concrete class with the
StructuredDatasetTransformerEngine class in order for the core flytekit type engine to handle
dataframe libraries. This is the encoding interface, meaning it is used when there is a Python value that the
flytekit type engine is trying to convert into a Flyte Literal. For the other way, see
the StructuredDatasetEncoder



### Methods

| Method | Description |
|-|-|
| [`encode()`](#encode) | Even if the user code returns a plain dataframe instance, the dataset transformer engine will wrap the. |


#### encode()

```python
def encode(
    ctx: flytekit.core.context_manager.FlyteContext,
    structured_dataset: flytekit.types.structured.structured_dataset.StructuredDataset,
    structured_dataset_type: flytekit.models.types.StructuredDatasetType,
) -> n: This function should return a StructuredDataset literal object. Do not confuse this with the
```
Even if the user code returns a plain dataframe instance, the dataset transformer engine will wrap the
incoming dataframe with defaults set for that dataframe
type. This simplifies this function's interface as a lot of data that could be specified by the user using
the
# TODO: Do we need to add a flag to indicate if it was wrapped by the transformer or by the user?



| Parameter | Type |
|-|-|
| `ctx` | `flytekit.core.context_manager.FlyteContext` |
| `structured_dataset` | `flytekit.types.structured.structured_dataset.StructuredDataset` |
| `structured_dataset_type` | `flytekit.models.types.StructuredDatasetType` |

### Properties

| Property | Type | Description |
|-|-|-|
| `protocol` |  |  |
| `python_type` |  |  |
| `supported_format` |  |  |

