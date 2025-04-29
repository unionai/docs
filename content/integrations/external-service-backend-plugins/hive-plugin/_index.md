---
title: Hive
weight: 1
variants: +flyte -serverless -byoc -byok
sidebar_expanded: false
---

# Hive

Flyte backend can be connected with various hive services. Once enabled it can allow you to query a hive service (e.g. Qubole) and retrieve typed schema (optionally).
This section will provide how to use the Hive Query Plugin using flytekit python

## Installation

To use the flytekit hive plugin simply run the following:

```shell
$ pip install flytekitplugins-hive
```

## No Need of a dockerfile

This plugin is purely a spec. Since SQL is completely portable there is no need to build a Docker container.

