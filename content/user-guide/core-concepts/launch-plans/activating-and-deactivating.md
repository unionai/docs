---
title: Activating and deactivating
weight: 5
variants: +flyte +serverless +byoc +selfmanaged
---

# Activating and deactivating

You can set an active/inactive status on launch plans. Specifically:

* Among the versions of a given launch plan (as defined by name), at most one can be set to active.
  All others are inactive.

* If a launch plan version that has a schedule attached is activated, then its schedule also becomes active and its workflow will be invoked automatically according to that schedule.

* When a launch plan version with a schedule is inactive, its schedule is inactive and will not be used to invoke its workflow.

Launch plans that do not have schedules attached can also have an active version.
For such non-scheduled launch plans, this status serves as a flag that can be used to distinguish one version from among the others.
It can, for example, be used by management logic to determine which version of a launch plan to use for new invocations.

Upon registration of a new launch plan, the first version is automatically inactive.
If it has a schedule attached, the schedule is also inactive.
Once activated, a launch plan version remains active even as new, later, versions are registered.

A launch plan version with a schedule attached can be activated through either the UI, `uctl`, or [`{{< key kit_remote >}}`](../../../user-guide/development-cycle/union-remote).

## Activating and deactivating a launch plan in the UI

To activate a launch plan, go to the launch plan view and click **Add active launch plan** in the top right corner of the screen:

![Activate schedule](../../../_static/images/user-guide/core-concepts/launch-plans/activating-and-deactivating/add-active-launch-plan.png)

A modal will appear that lets you select which launch plan version to activate:

![Activate schedule](../../../_static/images/user-guide/core-concepts/launch-plans/activating-and-deactivating/update-active-launch-plan-dialog.png)

This modal will contain all versions of the launch plan that have an attached schedule.
Note that at most one version (and therefore at most one schedule) of a launch plan can be active at any given time.

Selecting the launch plan version and clicking **Update** activates the launch plan version and schedule.
The launch plan version and schedule are now activated. The launch plan will be triggered according to the schedule going forward.

> [!WARNING]
> Non-scheduled launch plans cannot be activated via the UI.
> The UI does not support activating launch plans that do not have schedules attached.
> You can activate them with `uctl` or `{{< key kit_remote >}}`.

To deactivate a launch plan, navigate to a launch plan with an active schedule, click the **...** icon in the top-right corner of the screen beside **Active launch plan**, and click “Deactivate”.

![Deactivate schedule](../../../_static/images/user-guide/core-concepts/launch-plans/activating-and-deactivating/deactivate-launch-plan.png)

A confirmation modal will appear, allowing you to deactivate the launch plan and its schedule.

> [!WARNING]
> Non-scheduled launch plans cannot be deactivated via the UI.
> The UI does not support deactivating launch plans that do not have schedules attached.
> You can deactivate them with `uctl` or `{{< key kit_remote >}}`.

{{< variant byoc selfmanaged flyte >}}
{{< markdown >}}

## Activating and deactivating a launch plan on the command line with `uctl`

To activate a launch plan version with `uctl`, execute the following command:

```shell
$ uctl update launchplan \
       --activate \
       --project <project-id> \
       --domain <domain> \
       <launch-plan-name> \
       --version <launch-plan-version>
```


To deactivate a launch plan version with `uctl`, execute the following command:

```shell
$ uctl update launchplan \
       --deactivate \
       --project <project-id> \
       --domain <domain> \
       <launch-plan-name> \
       --version <launch-plan-version>
```


See [Uctl CLI](../../../api-reference/uctl-cli) for more details.

{{< /markdown >}}
{{< /variant >}}

<!-- TODO: Adjust Remote code or serverless vs everything else -->
## Activating and deactivating a launch plan in Python with `{{< key kit_remote >}}`

To activate a launch plan using version `{{< key kit_remote >}}`:

```python
from union.remote import {{< key kit_remote >}}
from flytekit.configuration import Config

remote = {{< key kit_remote >}}(config=Config.auto(), default_project=<project-id>, default_domain=<domain>)
launch_plan = remote.fetch_launch_plan(ame=<launch-plan-name>, version=<launch-plan-version>).id
remote.client.update_launch_plan(launch_plan.id, "ACTIVE")
```

To deactivate a launch plan version using `{{< key kit_remote >}}`:

```python
from union.remote import {{< key kit_remote >}}
from flytekit.remote import Config

remote = {{< key kit_remote >}}(config=Config.auto(), default_project=<project-id>, default_domain=<domain>)
launch_plan = remote.fetch_launch_plan(ame=<launch-plan-name>, version=<launch-plan-version>)
remote.client.update_launch_plan(launch_plan.id, "INACTIVE")
```

<!-- TODO need to add and link to full UnionRemote documentation to Union docs -- current UnionRemote page does not document all launch plan methods. -->
