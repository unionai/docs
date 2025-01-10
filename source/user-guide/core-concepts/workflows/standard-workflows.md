# Standard workflows

A standard workflow is defined by a Python function decorated with the `@workflow` decorator.
The function is written in a domain specific language (DSL) that is a subset of Python syntax that describes directed acyclic graph (DAG) that is deployed and executed on Union.
The syntax of a standard workflow definition can only include the following:

* Calls to functions decorated with `@task` and assignment of variables to the returned values.
* Calls to other functions decorated with `@workflow` and assignment of variables to the returned values (see [Subworkflows](./subworkflows-and-sub-launch-plans.md)).
* Calls to [`LaunchPlan` objects](../launch-plans/index.md) (see [When to use sub-launch plans](./subworkflows-and-sub-launch-plans.md#when-to-use-sub-launch-plans))
* Calls to functions decorated with `@dynamic` and assignment of variables to the returned values (see [Dynamic workflows](./dynamic-workflows.md)).
* Calls to functions decorated with `@eager` and assignment of variables to the returned values (see [Eager workflows](./eager-workflows.md)).
* The special [`conditional` construct](#conditional-construct).
* Statements using the [chaining operator `>>`](#chaining-operator).

## Evaluation of a standard workflow

{@@ if byoc @@}
When a standard workflow is [run locally in a Python environment](../../development-cycle/running-your-code.md#running-a-script-in-local-python-with-union-run) it is executed as a normal Python function.
However, when it is registered to Union, the top level `@workflow`-decorated function is evaluated as follows:
{@@ elif serverless @@}
When a standard workflow is run locally in a Python environment it is executed as a normal Python function.
However, when it is registered to Union, the top level `@workflow`-decorated function is evaluated as follows:
{@@ endif @@}

* Inputs to the workflow are materialized as lazily-evaluated promises which are propagated to downstream tasks and subworkflows.
* All values returned by calls to functions decorated with `@task` , `@dynamic`and `@eager` are also materialized as lazily-evaluated promises.

The resulting structure is used to construct the Directed Acyclic Graph (DAG) and deploy the required containers to the cluster.
The actual evaluation of these promises occurs when the tasks (or dynamic or eager workflows) are executed in their respective containers.

## Conditional construct

Because standard workflows cannot directly include Python `if` statements, a special `conditional` construct is provided that allows you to define conditional logic in a workflow.
For details, see [Conditionals](https://docs.flyte.org/en/latest/user_guide/advanced_composition/conditionals.html).

## Chaining operator

When Union builds the DAG for a standard workflow, it uses the passing of values from one task to another to determine the dependency relationships between tasks.

There may be cases where you want to define a dependency between two tasks that is not based on the output of one task being passed as an input to another.

In that case, you can use the chaining operator `>>` to define the dependencies between tasks.

For details, see [Chaining Flyte entities](https://docs.flyte.org/en/latest/user_guide/advanced_composition/chaining_flyte_entities.html).

## Workflow decorator parameters

The `@workflow` decorator can take the following parameters:

* `failure_policy`: Use the options in [`flytekit.WorkflowFailurePolicy`](https://docs.flyte.org/en/latest/api/flytekit/generated/flytekit.WorkflowFailurePolicy.html#flytekit.WorkflowFailurePolicy).

{@@ if byoc @@}
* `interruptible`: Indicates if tasks launched from this workflow are interruptible by default. See [Interruptible instances](../tasks/task-hardware-environment/interruptible-instances.md).
{@@ endif @@}

* `on_failure`: Invoke this workflow or task on failure. The workflow specified must have the same parameter signature as the current workflow, with an additional parameter called `error`.

* `docs`: A description entity for the workflow.
