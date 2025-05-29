---
title: Task resource validation
weight: 17
variants: +flyte +serverless +byoc +selfmanaged
---

# Task resource validation

In {{< key product_name >}}, when you attempt to execute a workflow with unsatisfiable resource requests, we fail the execution immediately rather than allowing it to queue forever.

We intercept execution creation requests in executions service to validate that their resource requirements can be met and fast-fail if not. A failed validation returns a message similar to

```text
Request failed with status code 400 rpc error: code = InvalidArgument desc = no node satisfies task 'workflows.fotd.fotd_directory' resource requests
```
