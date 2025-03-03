# Launching tasks

From the [task view](./viewing-tasks.md#task-view) (accessed, for example, by selecting a task in the [**Tasks** list](./viewing-tasks.md#tasks-list)) you can select **Launch Task** in the top right:

This opens the **New Execution** dialog for tasks:

![](/_static/images/user-guide/core-concepts/tasks/launching-tasks/new-execution-dialog.png)

The settings are similar to those for workflows. At the top you can select:

* The specific version of this task that you want to launch.

Along the left side the following sections are available:

* **Inputs**: The input parameters of the task function appear here as fields to be filled in.
* **Settings**:
  * **Execution name**: A custom name for this execution. If not specified, a name will be generated.
  * **Overwrite cached outputs**: A boolean. If set to `True`, this execution will overwrite any previously-computed cached outputs.
  * **Raw output data config**: Remote path prefix to store raw output data.
    By default, workflow output will be written to the built-in metadata storage.
    Alternatively, you can specify a custom location for output at the organization, project-domain, or individual execution levels.
    This field is for specifying this setting at the workflow execution level.
    If this field is filled in it overrides any settings at higher levels.
    The parameter is expected to be a URL to a writable resource (for example, `http://s3.amazonaws.com/my-bucket/`).
    {@# TODO: Add link to raw data documentation #@}
  * **Max parallelism**: Number of workflow nodes that can be executed in parallel. If not specified, project/domain defaults are used. If 0 then no limit is applied.
  * **Force interruptible**: A three valued setting for overriding the interruptible setting of the workflow for this particular execution.
    If not set, the workflow's interruptible setting is used.
    If set and **enabled** then `interruptible=True` is used for this execution.
    If set and **disabled** then `interruptible=False` is used for this execution.
    {@# TODO: Add link to interruptible documentation #@}
{@@ if byoc or byok or flyte @@}
  * **Service account**: The service account to use for this execution. If not specified, the default is used.
{@@ endif @@}
* **Environment variables**: Environment variables that will be available to tasks in this workflow execution.
* **Labels**: Labels to apply to the execution resource.
* **Notifications**: Notifications configured for this workflow execution.
{@# TODO: Add link to notifications documentation #@}
{@@ if byoc or byok or flyte @@}
* **Debug**: The workflow execution details for debugging purposes.
{@@ endif @@}

Select **Launch** to launch the task execution. This will take you to the [Execution view](../workflows/viewing-workflow-executions.md).
