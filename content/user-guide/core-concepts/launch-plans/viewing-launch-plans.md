---
title: Viewing launch plans
weight: 2
variants: +flyte +serverless +byoc +selfmanaged
---

# Viewing launch plans

## Viewing launch plans in the UI

Select **Launch Plans** in the sidebar to display a list of all the registered launch plans in the project and domain:

![Launch plans list](../../../_static/images/user-guide/core-concepts/launch-plans/viewing-launch-plans/launch-plans-list.png)

You can search the launch plans by name and filter for only those that are archived.

The columns in the launch plans table are defined as follows:

* **Name**: The name of the launch plan. Click to inspect a specific launch plan in detail.
* **Triggers**:
  * If the launch plan is active, a green **Active** badge is shown. When a launch plan is active, any attached schedule will be in effect and the launch plan will be invoked according to that schedule.
  * Shows whether the launch plan has a [trigger](./reactive-workflows). To filter for only those launch plans with a trigger, check the **Has Triggers** box in the top right.
* **Last Execution**: The last execution timestamp of this launch plan, irrespective of how the last execution was invoked (by schedule, by trigger, or manually).
* **Last 10 Executions**: A visual representation of the last 10 executions of this launch plan, irrespective of how these executions were invoked (by schedule, by trigger, or manually).

Select an entry on the list to go to that specific launch plan:

![Launch plan view](../../../_static/images/user-guide/core-concepts/launch-plans/viewing-launch-plans/launch-plan-view.png)

Here you can see:
* **Launch Plan Detail (Latest Version)**:
  * **Expected Inputs**: The input and output types for the launch plan.
  * **Fixed Inputs**: If the launch plan includes predefined input values, they are shown here.
* **Launch Plan Versions**: A list of all versions of this launch plan.
* **All executions in the Launch Plan**: A list of all executions of this launch plan.

In the top right you can see if this launch plan is active (and if it is, which version, specifically, is active). There is also a control for changing the active version or deactivating the launch plan entirely.
See [Activating and deactivating](./activating-and-deactivating) for more details.

{{< variant byoc selfmanaged flyte >}}
{{< markdown >}}

## Viewing launch plans on the command line with `uctl`

To view all launch plans within a project and domain:

```shell
$ uctl get launchplans \
       --project <project-id> \
       --domain <domain>
```


To view a specific launch plan:

```shell
$ uctl get launchplan \
       --project <project-id> \
       --domain <domain> \
       <launch-plan-name>
```


See the [Uctl CLI](../../../api-reference/uctl-cli) for more details.

{{< /markdown >}}
{{< /variant >}}

## Viewing launch plans in Python with `{{< key kit_remote >}}`

Use the method `{{< key kit_remote >}}.client.list_launch_plans_paginated` to get the list of launch plans.

<!-- TODO need to add and link to full UnionRemote documentation to Union docs -- current UnionRemote page does not document all launch plan methods. -->
