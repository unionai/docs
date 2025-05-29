---
title: Environment variables
weight: 5
variants: +flyte -serverless +byoc +selfmanaged
---

# Environment variables

The `environment` parameter lets you specify the values of any variables that you want to be present within the task container execution environment.
For example:

```python
@{{< key kit_as >}}.task(environment={"MY_ENV_VAR": "my_value"})
def my_task() -> str:
    return os.environ["MY_ENV_VAR"]
```