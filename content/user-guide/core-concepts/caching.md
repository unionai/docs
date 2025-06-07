---
title: Caching
weight: 8
variants: +flyte +serverless +byoc +selfmanaged
---

# Caching

{{< key product_name >}} allows you to cache the output of nodes ([tasks](./tasks), [subworkflows, and sub-launch plans](./workflows/subworkflows-and-sub-launch-plans)) to make subsequent executions faster.

Caching is useful when many executions of identical code with the same input may occur.

Here's a video with a brief explanation and demo, focused on task caching:

{{< youtube WNkThCp-gqo >}}

{{< variant flyte >}}

{{< markdown >}}
## Inputs caching

In Flyte, input caching allows tasks to automatically cache the input data required for execution. This feature is particularly useful in scenarios where tasks may need to be re-executed, such as during retries due to failures or when manually triggered by users. By caching input data, Flyte optimizes workflow performance and resource usage, preventing unnecessary recomputation of task inputs.

## Outputs caching

Output caching in Flyte allows users to cache the results of tasks to avoid redundant computations. This feature is especially valuable for tasks that perform expensive or time-consuming operations where the results are unlikely to change frequently.
{{< /markdown >}}

{{< /variant >}}

> [!NOTE]
> * Caching is available and individiually enablable for all nodes *within* a workflow directed acyclic graph (DAG).
> * Nodes in this sense include tasks, subworkflows (workflows called directly within another workflow), and sub-launch plans (launch plans called within a workflow).
> * Caching is *not available* for top-level workflows or launch plans (that is, those invoked from UI or CLI).
> * By default, caching is *disabled* on all tasks, subworkflows and sub-launch plans, to avoid unintended consequences when caching executions with side effects. It must be explcitly enabled on any node where caching is desired.

## Enabling and configuring caching

Caching can be enabled by setting the `cache` parameter of the `@{{< key kit_as >}}.task` (for tasks) decorator or `with_overrides` method (for subworkflows or sub-launch plans) to a `Cache` object. The parameters of the `Cache` object are used to configure the caching behavior.
For example:

```python
import {{< key kit_import >}}

# Define a task and enable caching for it

@{{< key kit_as >}}.task(cache={{< key kit_as >}}.Cache(version="1.0", serialize=True, ignored_inputs=["a"]))
def sum(a: int, b: int, c: int) -> int:
    return a + b + c

# Define a workflow to be used as a subworkflow

@{{< key kit_as >}}.workflow
def child*wf(a: int, b: int, c: int) -> list[int]:
    return [
        sum(a=a, b=b, c=c)
        for _ in range(5)
    ]

# Define a launch plan to be used as a sub-launch plan

child_lp = {{< key kit_as >}}.LaunchPlan.get_or_create(child_wf)

# Define a parent workflow that uses the subworkflow

@{{< key kit_as >}}.workflow
def parent_wf_with_subwf(input: int = 0):
    return [
        # Enable caching on the subworkflow
        child_wf(a=input, b=3, c=4).with_overrides(cache={{< key kit_as >}}.Cache(version="1.0", serialize=True, ignored_inputs=["a"]))
        for i in [1, 2, 3]
    ]

# Define a parent workflow that uses the sub-launch plan

@{{< key kit_as >}}.workflow
def parent_wf_with_sublp(input: int = 0):
    return [
        child_lp(a=input, b=1, c=2).with_overrides(cache={{< key kit_as >}}.Cache(version="1.0", serialize=True, ignored_inputs=["a"]))
        for i in [1, 2, 3]
    ]
```

In the above example, caching is enabled at multiple levels:

* At the task level, in the `@{{< key kit_as >}}.task` decorator of the task `sum`.
* At the workflow level, in the `with_overrides` method of the invocation of the workflow `child_wf`.
* At the launch plan level, in the `with_overrides` method of the invocation of the launch plan `child_lp`.

In each case, the result of the execution is cached and reused in subsequent executions.
Here the reuse is demonstrated by calling the `child_wf` and `child_lp` workflows multiple times with the same inputs.
Additionally, if the same node is invoked again with the same inputs (excluding input "a", as it is ignored for purposes of versioning)
the cached result is returned immediately instead of re-executing the process.
This applies even if the cached node is invoked externally through the UI or CLI.

## The `Cache` object

The [Cache]() object takes the following parameters:
<!-- TODO: Add link to API -->

{{< variant byoc serverless >}}

{{< markdown >}}
* `version` (`Optional[str]`): Part of the cache key.
  A change to this parameter from one invocation to the next will invalidate the cache.
  This allows you to explicitly indicate when a change has been made to the node that should invalidate any existing cached results.
  Note that this is not the only change that will invalidate the cache (see below).
  Also, note that you can manually trigger cache invalidation per execution using the [`overwrite-cache` flag](#the-overwrite-cache-flag).

  If not set, the version will be generated based on the specified cache policies.
  When using `cache=True`, [as shown below](#enabling-caching-with-the-default-configuration), the [default cache policy](#default-cache-policy) generates the version.
{{< /markdown >}}
{{< /variant >}}

{{< variant flyte >}}
{{< markdown >}}

* `version` (`Optional[str]`): Part of the cache key. Changing this version number tells Flyte to ignore previous cached results and run the task again if the task’s function has changed. This allows you to explicitly indicate when a change has been made to the task that should invalidate any existing cached results. Note that this is not the only change that will invalidate the cache (see below). Also, note that you can manually trigger cache invalidation per execution using the `overwrite-cache` flag.

{{< /markdown >}}
{{< /variant >}}
* `serialize` (`bool`): Enables or disables [cache serialization](#cache-serialization).
  When enabled, {{< key product_name >}} ensures that a single instance of the node is run before any other instances that would otherwise run concurrently.
  This allows the initial instance to cache its result and lets the later instances reuse the resulting cached outputs.
  If not set, cache serialization is disabled.

* `ignored_inputs` (`Union[Tuple[str, ...], str]`): Input variables that should not be included when calculating the hash for the cache.
  If not set, no inputs are ignored.

{{< variant byoc serverless >}}

{{< markdown >}}
* `policies` (`Optional[Union[List[CachePolicy], CachePolicy]]`): A list of [CachePolicy]() objects used for automatic version generation.
  If no `version` is specified and one or more polices are specified then these policies automatically generate the version.
  Policies are applied in the order they are specified to produce the final `version`.
  If no `version` is specified and no policies are specified then the [default cache policy](#default-cache-policy) generates the version.
  When using `cache=True`, [as shown below](#enabling-caching-with-the-default-configuration), the [default cache policy](#default-cache-policy) generates the version.
{{< /markdown >}}

{{< /variant >}}

{{< variant flyte >}}

{{< markdown >}}

* `policies` (`Optional[Union[List[CachePolicy], CachePolicy]]`): A list of cache policies to generate the version hash.


{{< /markdown >}}

{{< /variant >}}
* `salt` (`str`): A [salt](<https://en.wikipedia.org/wiki/salt_(cryptography)>) used in the hash generation. A salt is a random value that is combined with the input values before hashing.

{{< variant byoc serverless >}}

{{< markdown >}}
## Enabling caching with the default configuration

Instead of specifying a `Cache` object, a simpler way to enable caching is to set `cache=True` in the `@{{< key kit_as >}}.task` decorator (for tasks) or the `with_overrides` method (for subworkflows and sub-launch plans).

When `cache=True` is set, caching is enabled with the following configuration:

* `version` is automatically generated by the [default cache policy](#).
* `serialize` is set to `False`.
* `ignored_inputs` is not set. No parameters are ignored.

You can convert the example above to use the default configuration throughout by changing each instance of `cache={{< key kit_as >}}.Cache(...)` to `cache=True`. For example, the task `sum` would now be:

```python
@{{< key kit_as >}}.task(cache=True)
def sum(a: int, b: int, c: int) -> int:
    return a + b + c
```

## Automatic version generation

Automatic version generation is useful when you want to generate the version based on the function body of the task, or other criteria.

You can enable automatic version generation by specifying `cache=Cache(...)` with one or more `CachePolicy` classes in the `policies` parameter of the `Cache` object (and by not specifying an explicit `version` parameter), like this:

```python
@{{< key kit_as >}}.task(cache=Cache(policies=[CacheFunctionBody()]))
def sum(a: int, b: int, c: int) -> int:
    return a + b + c
```

Alternatively, you can just use the default configuration by specify use `cache=True`. In this case the default cache policy is used to generate the version.

## Default cache policy

Automatic version generation using the default cache policy is used

* if you set `cache=True`, or
* if you set `cache=Cache(...)` but do not specify an explicit `version` or `policies` parameters within the `Cache` object.

The default cache policy is `{{< key kit_as >}}.cache.CacheFunctionBody`.
This policy generates a version by hashing the text of the function body of the task.
This means that if the code in the function body changes, the version changes, and the cache is invalidated. Note that `CacheFunctionBody` does not recursively check for changes in functions or classes referenced in the function body.

{{< /markdown >}}

{{< /variant >}}

## The `overwrite-cache` flag

When launching the execution of a workflow, launch plan or task, you can use the `overwrite-cache` flag to invalidate the cache and force re-execution.

### Overwrite cache on the command line

The `overwrite-cache` flag can be used from the command line with the `{{< key cli >}} run` command. For example:

```shell
$ {{< key cli >}} run --remote --overwrite-cache example.py wf
```

### Overwrite cache in the UI

You can also trigger cache invalidation when launching an execution from the UI by checking **Override**, in the launch dialog:

![Overwrite cache flag in the UI](../../_static/images/user-guide/core-concepts/caching/overwrite-cached-outputs.png)

### Overwrite cache programmatically

When using `{{< key kit_remote >}}`, you can use the `overwrite_cache` parameter in the [`{{< key kit_remote >}}.execute`]() method:
<!-- TODO: Add link to API -->

{{< variant flyte >}}
{{< markdown >}}
```python
from flytekit.configuration import Config
from flytekit.remote import {{< key kit_remote >}}

remote = {{< key kit_remote >}}(
    config=Config.auto(),
    default_project="{{< key default_project >}}",
    default_domain="development"
)

wf = remote.fetch_workflow(name="workflows.example.wf")
execution = remote.execute(wf, inputs={"name": "Kermit"}, overwrite_cache=True)
```
{{< /markdown >}}
{{< /variant >}}
{{< variant byoc selfmanaged >}}
{{< markdown >}}
```python
from flytekit.configuration import Config
from union.remote import {{< key kit_remote >}}

remote = {{< key kit_remote >}}(
    config=Config.auto(),
    default_project="{{< key default_project >}}",
    default_domain="development"
)

wf = remote.fetch_workflow(name="workflows.example.wf")
execution = remote.execute(wf, inputs={"name": "Kermit"}, overwrite_cache=True)
```
{{< /markdown >}}
{{< /variant >}}
{{< variant serverless >}}
{{< markdown >}}
```python
from union.remote import {{< key kit_remote >}}

remote = {{< key kit_remote >}}()

wf = remote.fetch_workflow(name="workflows.example.wf")
execution = remote.execute(wf, inputs={"name": "Kermit"}, overwrite_cache=True)
```
{{< /markdown >}}
{{< /variant >}}

## How caching works

When a node (with caching enabled) completes on {{< key product_name >}}, a **key-value entry** is created in the **caching table**. The **value** of the entry is the output.
The **key** is composed of:

* **Project:** A task run under one project cannot use the cached task execution from another project which would cause inadvertent results between project teams that could result in data corruption.
* **Domain:** To separate test, staging, and production data, task executions are not shared across these environments.
{{< variant byoc serverless >}}
{{< markdown >}}
* **Cache Version:** The cache version is either explicitly set using the `version` parameter in the `Cache` object or automatically set by a cache policy (see [Automatic version generation](#automatic-version-generation)).
  If the version changes (either explicitly or automatically), the cache entry is invalidated.

{{< /markdown >}}
{{< /variant >}}

{{< variant flyte >}}
{{< markdown >}}

* **Cache version**: When task functionality changes, you can change the cache_version of the task. Flyte will know not to use older cached task executions and create a new cache entry on the subsequent execution.

{{< /markdown >}}
{{< /variant >}}

* **Node signature:** The cache is specific to the signature associated with the execution.
  The signature comprises the name, input parameter names/types, and the output parameter name/type of the node.
  If the signature changes, the cache entry is invalidated.
* **Input values:** A well-formed {{< key product_name >}} node always produces deterministic outputs.
  This means that, given a set of input values, every execution should have identical outputs.
  When an execution is cached, the input values are part of the cache key.
  If a node is run with a new set of inputs, a new cache entry is created for the combination of that particular entity with those particular inputs.

The result is that within a given project and domain, a cache entry is created for each distinct combination of name, signature, cache version, and input set for every node that has caching enabled.
If the same node with the same input values is encountered again, the cached output is used instead of running the process again.

### Explicit cache version

When a change to code is made that should invalidate the cache for that node, you can explicitly indicate this by incrementing the `version` parameter value.
For a task example, see below. (For workflows and launch plans, the parameter would be specified in the `with_overrides` method.)

```python
@{{< key kit_as >}}.task(cache={{< key kit_as >}}.Cache(version="1.1"))
def t(n: int) -> int:
    return n \* n + 1
```

Here the `version` parameter has been bumped from `1.0`to `1.1`, invalidating of the existing cache.
The next time the task is called it will be executed and the result re-cached under an updated key.
However, if you change the version back to `1.0`, you will get a "cache hit" again and skip the execution of the task code.

If used, the `version` parameter must be explicitly changed in order to invalidate the cache.

{{< variant byoc serverless >}}
{{< markdown >}}

If not used, then a cache policy may be specified to generate the version, or you can rely on the default cache policy.

{{< /markdown >}}
{{< /variant >}}

Not every Git revision of a node will necessarily invalidate the cache.
A change in Git SHA does not necessarily correlate to a change in functionality.
You can refine your code without invalidating the cache as long as you explicitly use, and don't change, the `version` parameter (or the signature, see below) of the node.

The idea behind this is to decouple syntactic sugar (for example, changed documentation or renamed variables) from changes to logic that can affect the process's result.
When you use Git (or any version control system), you have a new version per code change.
Since the behavior of most nodes in a Git repository will remain unchanged, you don't want their cached outputs to be lost.

When a node's behavior does change though, you can bump `version` to invalidate the cache entry and make the system recompute the outputs.

### Node signature

If you modify the signature of a node by adding, removing, or editing input parameters or output return types, {{< key product_name >}} invalidates the cache entries for that node.
During the next execution, {{< key product_name >}} executes the process again and caches the outputs as new values stored under an updated key.

{{< variant byoc selfmanaged flyte >}}
{{< markdown >}}

### Caching when running locally

The description above applies to caching when executing a node remotely on your {{< key product_name >}} cluster.
Caching is also available [when running on a local cluster](../development-cycle/running-in-a-local-cluster).

When running locally the caching mechanism is the same except that the cache key does not include **project** or **domain** (since there are none).
The cache key is composed only of **cache version**, **signature**, and **inputs**.
The results of local executions are stored under `~/.flyte/local-cache/`.

Similar to the remote case, a local cache entry for a node will be invalidated if either the `cache_version` or the signature is modified.
In addition, the local cache can also be emptied by running

```shell
$ {{< key cli >}} local-cache clear
```

This removes the contents of the `~/.flyte/local-cache/` directory.

{{< /markdown >}}
{{< /variant >}}

## Cache serialization

Cache serialization means only executing a single instance of a unique cacheable task (determined by the `cache_version` parameter and task signature) at a time.
Using this mechanism, {{< key product_name >}} ensures that during multiple concurrent executions of a task only a single instance is evaluated, and all others wait until completion and reuse the resulting cached outputs.

Ensuring serialized evaluation requires a small degree of overhead to coordinate executions using a lightweight artifact reservation system.
Therefore, this should be viewed as an extension to rather than a replacement for non-serialized cacheable tasks.
It is particularly well fit for long-running or otherwise computationally expensive tasks executed in scenarios similar to the following examples:

* Periodically scheduled workflow where a single task evaluation duration may span multiple scheduled executions.
* Running a commonly shared task within different workflows (which receive the same inputs).

### Enabling cache serialization

Task cache serializing is disabled by default to avoid unexpected behavior for task executions.
To enable, set `serialize=True` in the `@{{< key kit_as >}}.task` decorator.
The cache key definitions follow the same rules as non-serialized cache tasks.

```python
@{{< key kit_as >}}.task(cache={{< key kit_as >}}.Cache(version="1.1", serialize=True))
def t(n: int) -> int:
return n \* n
```

In the above example calling `t(n=2)` multiple times concurrently (even in different executions or workflows) will only execute the multiplication operation once.
Concurrently evaluated tasks will wait for completion of the first instance before reusing the cached results and subsequent evaluations will instantly reuse existing cache results.

### How does cache serialization work?

The cache serialization paradigm introduces a new artifact reservation system. Executions with cache serialization enabled use this reservation system to acquire an artifact reservation, indicating that they are actively evaluating a node, and release the reservation once the execution is completed.
{{< key product_name >}} uses a clock-skew algorithm to define reservation timeouts. Therefore, executions are required to periodically extend the reservation during their run.

The first execution of a serializable node will successfully acquire the artifact reservation.
Execution will be performed as usual and upon completion, the results are written to the cache, and the reservation is released.
Concurrently executed node instances (those that would otherwise run in parallel with the initial execution) will observe an active reservation, in which case these instances will wait until the next reevaluation and perform another check.
Once the initial execution completes, they will reuse the cached results as will any subsequent instances of the same node.

{{< key product_name >}} handles execution failures using a timeout on the reservation.
If the execution currently holding the reservation fails to extend it before it times out, another execution may acquire the reservation and begin processing.

## Caching of offloaded objects

In some cases, the default behavior displayed by {{< key product_name >}}’s caching feature might not match the user's intuition.
For example, this code makes use of pandas dataframes:

```python
@{{< key kit_as >}}.task
def foo(a: int, b: str) -> pandas.DataFrame:
    df = pandas.DataFrame(...)
    ...
    return df

@{{< key kit_as >}}.task(cache=True)
def bar(df: pandas.DataFrame) -> int:
    ...

@{{< key kit_as >}}.workflow
def wf(a: int, b: str):
    df = foo(a=a, b=b)
    v = bar(df=df)
```

If run twice with the same inputs, one would expect that `bar` would trigger a cache hit, but that’s not the case because of the way dataframes are represented in {{< key product_name >}}.

However, {{< key product_name >}} provides a new way to control the caching behavior of literals.
This is done via a `typing.Annotated` call on the node signature.
For example, in order to cache the result of calls to `bar`, you can rewrite the code above like this:

```python
def hash_pandas_dataframe(df: pandas.DataFrame) -> str:
    return str(pandas.util.hash_pandas_object(df))

@{{< key kit_as >}}.task
def foo_1(a: int, b: str) -> Annotated[pandas.DataFrame, HashMethod(hash_pandas_dataframe)]:
    df = pandas.DataFrame(...)
    ...
    return df

@{{< key kit_as >}}.task(cache=True)
def bar_1(df: pandas.DataFrame) -> int:
    ...

@{{< key kit_as >}}.workflow
def wf_1(a: int, b: str):
    df = foo(a=a, b=b)
    v = bar(df=df)
```

Note how the output of the task `foo` is annotated with an object of type `HashMethod`.
Essentially, it represents a function that produces a hash that is used as part of the cache key calculation in calling the task `bar`.

### How does caching of offloaded objects work?

Recall how input values are taken into account to derive a cache key.
This is done by turning the literal representation into a string and using that string as part of the cache key.
In the case of dataframes annotated with `HashMethod`, we use the hash as the representation of the literal.
In other words, the literal hash is used in the cache key.
This feature also works in local execution.

Here’s a complete example of the feature:

```python
def hash_pandas_dataframe(df: pandas.DataFrame) -> str:
    return str(pandas.util.hash_pandas_object(df))

@{{< key kit_as >}}.task
def uncached_data_reading_task() -> Annotated[pandas.DataFrame, HashMethod(hash_pandas_dataframe)]:
    return pandas.DataFrame({"column_1": [1, 2, 3]})

@{{< key kit_as >}}.task(cache=True)
def cached_data_processing_task(df: pandas.DataFrame) -> pandas.DataFrame:
    time.sleep(1)
    return df \* 2

@{{< key kit_as >}}.task
def compare_dataframes(df1: pandas.DataFrame, df2: pandas.DataFrame):
    assert df1.equals(df2)

@{{< key kit_as >}}.workflow
def cached_dataframe_wf():
    raw_data = uncached_data_reading_task()

    # Execute `cached_data_processing_task` twice, but force those
    # two executions to happen serially to demonstrate how the second run
    # hits the cache.
    t1_node = create_node(cached_data_processing_task, df=raw_data)
    t2_node = create_node(cached_data_processing_task, df=raw_data)
    t1_node >> t2_node

    # Confirm that the dataframes actually match
    compare_dataframes(df1=t1_node.o0, df2=t2_node.o0)

if **name** == "**main**":
    df1 = cached_dataframe_wf()
    stickioesprint(f"Running cached_dataframe_wf once : {df1}")
```
