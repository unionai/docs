---
title: Actors
weight: 4
variants: -flyte +serverless +byoc +selfmanaged
sidebar_expanded: false
---

# Actors

Actors allow you to reuse a container and environment between tasks, avoiding the cost of starting a new container for each task. This can be useful when you have a task that requires a lot of setup or has a long startup time.

To create an actor, instantiate the [`ActorEnvironment`](../../../api-reference/union-sdk/packages/union.actor#unionactoractorenvironment) class, then add the instance as a decorator to the task that requires that environment.

### `ActorEnvironment` parameters

{{< variant serverless >}}
{{< markdown >}}
* **container_image:** The container image to use for the task. This container must have the `{{< key kit >}}` python package installed. Defaults to `cr.union.ai/union/unionai:py3.11-latest`.
{{< /markdown >}}
{{< /variant >}}
{{< variant byoc selfmanaged flyte >}}
{{< markdown >}}
* **container_image:** The container image to use for the task. This container must have the `{{< key kit >}}` python package installed, so this must be updated from the default (i.e. `cr.flyte.org/flyteorg/flytekit:py3.11-latest`).
{{< /markdown >}}
{{< /variant >}}
* **environment:** Environment variables as key, value pairs in a Python dictionary.
* **limits:** Compute resource limits.
* **replica_count:** The number of workers to provision that are able to accept tasks.
* **requests:** Compute resource requests per task.
* **secret_requests:** Keys (ideally descriptive) that can identify the secrets supplied at runtime. For more information, see [Managing secrets](../../development-cycle/managing-secrets).
* **ttl_seconds:** How long to keep the Actor alive while no tasks are being run.

The following example shows how to create a basic `ActorEnvironment` and use it for one task:

{{< variant serverless >}}
{{< markdown >}}

```python
# hello_world.py

import {{< key kit_import >}}


actor = {{< key kit_as >}}.ActorEnvironment(
    name="my-actor",
    replica_count=1,
    ttl_seconds=30,
    requests={{< key kit_as >}}.Resources(
        cpu="2",
        mem="300Mi",
    ),
)


@actor.task
def say_hello() -> str:
    return "hello"


@{{< key kit_as >}}.workflow
def wf():
    say_hello()
```

{{< /markdown >}}
{{< /variant >}}
{{< variant byoc selfmanaged flyte >}}
{{< markdown >}}

```python
# hello_world.py

import os

import {{< key kit_import >}}

image = {{< key kit_as >}}.ImageSpec(
    registry=os.environ.get("DOCKER_REGISTRY", None),
    packages=["union"],
)

actor = {{< key kit_as >}}.ActorEnvironment(
    name="my-actor",
    replica_count=1,
    ttl_seconds=30,
    requests={{< key kit_as >}}.Resources(
        cpu="2",
        mem="300Mi",
    ),
    container_image=image,
)


@actor.task
def say_hello() -> str:
    return "hello"


@{{< key kit_as >}}.workflow
def wf():
    say_hello()
```

{{< /markdown >}}
{{< /variant >}}

You can learn more about the trade-offs between actors and regular tasks, as well as the efficiency gains you can expect [here](actors-and-regular-tasks).

## Caching on Actor Replicas

The `@actor_cache` decorator provides a powerful mechanism to cache the results of Python callables on individual actor replicas. This is particularly beneficial for workflows involving repetitive tasks, such as data preprocessing, model loading, or initialization of shared resources, where caching can minimize redundant operations and improve overall efficiency. Once a callable is cached on a replica, subsequent tasks that use the same actor can access the cached result, significantly improving performance and efficiency.

### When to Use `@actor_cache`

- **Shared Initialization Costs:**
  For expensive, shared initialization processes that multiple tasks rely on.

- **Repetitive Task Execution:**
  When tasks repeatedly require the same resource or computation on the same actor replica.

- **Complex Object Caching:**
  Use custom Python objects as keys to define unique cache entries.


Below is a simplified example showcasing the use of `@actor_cache` for caching repetitive tasks. This dummy example demonstrates caching model that is loaded by the `load_model` task.

{{< variant serverless >}}
{{< markdown >}}

```python
# caching_basic.py

from time import sleep

import {{< key kit_import >}}


actor = {{< key kit_as >}}.ActorEnvironment(
    name="my-actor",
    replica_count=1,
)


@{{< key kit_as >}}.actor_cache
def load_model(state: int) -> callable:
    sleep(4)  # simulate model loading
    return lambda value: state + value


@actor.task
def evaluate(value: int, state: int) -> int:
    model = load_model(state=state)
    return model(value)


@{{< key kit_as >}}.workflow
def wf(init_value: int = 1, state: int = 3) -> int:
    out = evaluate(value=init_value, state=state)
    out = evaluate(value=out, state=state)
    out = evaluate(value=out, state=state)
    out = evaluate(value=out, state=state)
    return out
```

{{< /markdown >}}
{{< /variant >}}
{{< variant byoc selfmanaged flyte >}}
{{< markdown >}}

```python
# caching_basic.py

from time import sleep
import os

import {{< key kit_import >}}

image = {{< key kit_as >}}.ImageSpec(
    registry=os.environ.get("DOCKER_REGISTRY", None),
    packages=["union"],
)

actor = {{< key kit_as >}}.ActorEnvironment(
    name="my-actor",
    container_image=image,
    replica_count=1,
)


@{{< key kit_as >}}.actor_cache
def load_model(state: int) -> callable:
    sleep(4)  # simulate model loading
    return lambda value: state + value


@actor.task
def evaluate(value: int, state: int) -> int:
    model = load_model(state=state)
    return model(value)


@{{< key kit_as >}}.workflow
def wf(init_value: int = 1, state: int = 3) -> int:
    out = evaluate(value=init_value, state=state)
    out = evaluate(value=out, state=state)
    out = evaluate(value=out, state=state)
    out = evaluate(value=out, state=state)
    return out
```

> [!NOTE]
> In order to get the `@actor_cache` functionality, you must pin `{{< key kit >}}` to at least `0.1.121`.

{{< /markdown >}}
{{< /variant >}}

![Actor caching example 1](../../../_static/images/user-guide/core-concepts/actors/caching/actor-cache-example-1.png)

You can see that the first call of `evaluate` took considerable time as it involves allocating a node for the task, creating a container, and loading the model. The subsequent calls of `evaluate` execute in a fraction of the time.

You can see examples of more advanced actor usage [here](actor-examples).
