---
title: Airflow Provider
weight: 1
variants: +flyte -serverless -byoc -selfmanaged
sidebar_expanded: false
---

# Airflow Provider

The `airflow-provider-flyte` package provides an operator, a sensor, and a hook that integrates Flyte into Apache Airflow.
`FlyteOperator` is helpful to trigger a task/workflow in Flyte and `FlyteSensor` enables monitoring a Flyte execution status for completion.

The primary use case of this provider is to **scale Airflow for machine learning tasks using Flyte**.
With the Flyte Airflow provider, you can construct your ETL pipelines in Airflow and machine learning pipelines in Flyte
and use the provider to trigger machine learning or Flyte pipelines from within Airflow.

## Installation

```shell
$ pip install airflow-provider-flyte
```

All the configuration options for the provider are available in the provider repo's [README](https://github.com/flyteorg/airflow-provider-flyte#readme).


