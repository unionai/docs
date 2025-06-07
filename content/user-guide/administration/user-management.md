---
title: User management
weight: 3
variants: -flyte -serverless +byoc +selfmanaged
---

# User management

{{< key product_name >}} comes with role-based access control management out of the box.
The system is based on the following concepts:

* **Action**: An action that can be performed by a **user** or **application**.
For example, `register_flyte_inventory` is the action of registering tasks and workflows.
* **Role**: A set of **actions**.
The system includes built-in roles out of the box (see below) and also enabled administrators to define custom roles.
* **Policy**: A set of bindings between a **role** and an **organization**, **project, domain or project-domain** pair.
* **User** or **application**: An actor to which **policies** can be assigned.
Through the assigned policies, the user or application acquires permission to perform the specified **actions** on the designated resources.
A user is a person, registered and identified by **email address**.
An application is an automated process (a bot, service, or other type of program), registered and identified by **application ID**.
* **Organization**: A set of projects associated with a company, department, or other organization.
* **Project**: A set of associated workflows, tasks, launch plans, and other {{< key product_name >}} entities.
* **Domain**: Categories representing the standard environments used in the development process: **development**, **staging**, and **production**.
* **Project-domain pair**: The set of projects is divided orthogonally by the three **domains**.
The result is a set of project-domain pairs.
For example: `{{< key default_project >}}/development`, `{{< key default_project >}}/staging`, and `{{< key default_project >}}/production`.

## Actions

The following is the full list of actions available in the {{< key product_name >}} system:

* `administer_project`: Permission to archive and update a project and manage customizable resources.
* `manage_permissions`: Permission to manage user and machine applications and their policy assignments.
* `create_flyte_executions`: Permission to launch new flyte executions.
* `register_flyte_inventory`: Permission to register workflows, tasks, and launch plans.
* `view_flyte_executions`: Permission to view historical flyte execution data.
* `view_flyte_inventory`: Permission to view registered workflows, tasks, and launch plans.

## Built-in policies

{{< key product_name >}} ships with three built-in policies: **Admin**, **Contributor**, and **Viewer**.

* An **Admin** has permission to perform all actions (`administer_project`, `manage_permissions`, `create_flyte_executions`, `register_flyte_inventory`, `view_flyte_executions`, `view_flyte_inventory`) across the organization (in all projects and domains).
In other words:
  * Invite users and assign roles.
  * View the **Monitoring** and **Billing** dashboards.
  * Do everything a **Contributor** can do.
* A **Contributor** has permission to perform the actions `create_flyte_executions`, `register_flyte_inventory`, `view_flyte_executions`, and `view_flyte_inventory`across the organization (in all projects and domains). In other words:
  * Register and execute workflows, tasks and launch plans.
  * Do everything a **Viewer** can do.
* A **Viewer** has permission to perform the actions `view_flyte_executions` and `view_flyte_inventory`across the organization (in all projects and domains).
In other words:
  * View workflows, tasks, launch plans, and executions.

## Multiple policies

Users and applications are assigned to zero or more policies.
A user or application with no policies will have no permissions but will not be [removed](#removing-a-user).
For example, in the case of users, they will still appear on the [list of users](#managing-users-and-assigning-policies).
A user or application with multiple policies will have the logical union of the permission sets of those policies.

> [!NOTE]
> The default roles that come out of the box are hierarchical.
> The **Admin** permission set is a superset of the **Contributor** permission set and the **Contributor** permission set is a superset of **Viewer** permission set.
> This means, for example, that if you make a user an **Admin**, then additionally assigning them **Contributor** or **Viewer** will make no difference.
> But this is only the case due to how these particular roles are defined.
> In general, it is possible to create roles where assigning multiple ones is meaningful.

## Custom roles and policies

It is possible to create new custom roles and policies.
Custom roles and policies can, for example, be used to mix and match permissions at the organization, project, or domain level.

Roles and policies are created using the [`uctl` CLI](../../api-reference/uctl-cli) (not the [{{< key cli_name >}} CLI](../../api-reference/union-cli)).
Make sure you have the [`uctl` CLI installed and configured to point to your {{< key product_name >}} instance](../../api-reference/uctl-cli).

### Create a role

Create a role spec file `my_role.yaml` that defines a set of actions:

```yaml
:name: my_role.yaml

name: Workflow Runner
actions:
- view_flyte_inventory
- view_flyte_executions
- create_flyte_executions
```


Create the role from the command line:

```shell
$ uctl create role --roleFile my_role.yaml
```

### Create a policy

Create a policy spec file `my_policy.yaml` that binds roles to project/domain pairs.
Here we create a policy that binds the **Contributor** role to `{{< key default_project >}}/development` and binds the **Workflow Runner** role (defined above) to `{{< key default_project >}}/production`:

```yaml
:name: my_policy.yaml

name: Workflow Developer Policy
bindings:
- role: Workflow Runner
  resource:
    project: {{< key default_project >}}
    domain: production
- role: contributor # Boilerplate system role
  resource:
    project: {{< key default_project >}}
    domain: development
```


Create the policy from the command line:

```shell
$ uctl create policy --policyFile my_policy.yaml
```


Any user or application to which this policy is assigned will be granted **Contributor** permissions to `{{< key default_project >}}/development` while being granted (the more restrictive) **Workflow Runner** permission to `{{< key default_project >}}/production`.

### Assign the policy to a user

Once the policy is created you can assign it to a user using the **User Management** interface in the UI (see [Changing assigned policies](#changing-assigned-policies) below) or using the command line:

```shell
$ uctl append identityassignments \
       --user "bob@contoso.com" \
       --policy "Workflow Developer Policy"
```


Similarly, you can assign the policy to an application through the command line (there is currently no facility to assign policies to applications in the UI):

```shell
$ uctl append identityassignments \
       --application "contoso-operator" \
       --policy "Workflow Developer Policy"
```

## Initial onboarding

The initial {{< key product_name >}} onboarding process will set up your organization with at least one **Admin** user who will have permission to invite teammates and manage their roles.

## Managing users and assigning policies

To add and remove users and to assign and unassign roles, you have to be an **Admin**.
As an **Admin** you should see a **Users** icon at the top-right of the UI:

![](../../_static/images/user-guide/administration/user-management/users-button.png)

Select this icon to display the **User Management** dialog displays the list of users:

![](../../_static/images/user-guide/administration/user-management/user-management.png "medium")

Each user is listed with their assigned policies. You can search the list and filter by policy.

### Adding a user

To add a new user, select **ADD USER**.

In the **Add User** dialog, fill in the name and email of the new user and select the policies to assign, then select either **SUBMIT** or **SUBMIT AND ADD ANOTHER USER**:

![](../../_static/images/user-guide/administration/user-management/add-user.png "medium")

The new user should expect to see an email invite from Okta after they have been added through this dialog.
They should accept the invite and set up a password. At that point, they will be able to access the {{< key product_name >}} UI.

### Changing assigned policies

To change a user's assigned policies, go to the **User Management** dialog and select the user. The **Edit User** dialog will appear:

![](../../_static/images/user-guide/administration/user-management/edit-user.png "medium")

To adjust the assigned policies, simply toggle the appropriate buttons and select **SUBMIT**.

### Removing a user

To remove a user, in the **Edit User** dialog (above), select **REMOVE USER**.
