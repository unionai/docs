---
title: Enabling AWS resources
weight: 9
variants: -flyte -serverless +byoc -selfmanaged
sidebar_expanded: true
---

# Enabling AWS resources

Components of your {{< key product_name >}} data plane will need to connect to and communicate with other resources in your cloud environment such as [AWS S3 storage](./enabling-aws-s3), [AWS Elastic Container Registry](./enabling-aws-ecr), and so forth.

> [!NOTE] Secret management
> We strongly recommend using the [{{< key product_name >}} secrets manager](../../user-guide/development-cycle/managing-secrets) to manage secrets rather than AWS Secrets Manager. If your organization must use AWS Secrets Manager, however, see [Enabling AWS Secrets Manager](./enabling-aws-secrets-manager).

As much as possible, access to the resources you need will be pre-configured by the {{< key product_name >}} team when they set up your data plane.
For example, if you want your task code to have access to a specific S3 bucket or database, this can be pre-configured.
**You just have to inform the team of your specific requirements before the setup process begins**.

As your projects evolve, your needs may change.
You can always contact the {{< key product_name >}} team for help enabling additional resources as required.

**There are also some cases where you may want to configure things on your own.**
**Below we give a general overview of these self-configuration options.**
**The sub-pages of this section give examples for specific resources.**

## Types of access

Broadly speaking, there are two categories of access that you are likely to have to deal with:

* **Infrastructure access**:
  Enabling access to a resource for your data plane infrastructure.
  The most common case occurs when you are using [AWS Elastic Container Registry (ECR)](./enabling-aws-ecr) for your task container images, and it resides in an AWS account other than the one containing your data plane.
  In that case, some configuration is required to enable the {{< key product_name >}} operator on your data plane to pull images from the registry when registering your workflows and tasks.
  **If you are using an ECR instance within the same AWS account as your data plane, then access is enabled by default and no further configuration is needed.**
* **Task code access**:
  Enabling access to a resource for your task code.
  For example, your task code might need to access [AWS S3 storage](./enabling-aws-s3) or [AWS Secrets Manager](./enabling-aws-secrets-manager) at runtime.
  This involves granting permission to roles that are attached to the Kubernetes cluster within which your task code runs.

## Infrastructure-level access

The only infrastructure-level access issue you are likely to encounter is around access to an AWS Elastic Container Registry (ECR) _in an AWS account other than the one in which your data plane resides_.

**If your task container images are stored in an AWS Elastic Container Registry in the same AWS account as your data plane, then access is already enabled. You do not have to do anything.**

If your task container images reside in an ECR instance in **another AWS account** you will need configure that ECR instance to allow access from your data plane.
See [Enabling AWS ECR](./enabling-aws-ecr) for details.

## Task code access

When your task code runs, it executes within a pod in the Kubernetes cluster in your data plane.
To enable your task code to access cloud resources you must grant the appropriate permissions to a role that is attached to the Kubernetes cluster.

There are two main options for setting this up:

* **Project-domain-scoped access**: With this arrangement, you define the permissions you want to grant to your task code, and those permissions are applied only to specific project-domain pairs.
* **Global access**: With this arrangement, you define the permissions you want to grant to your task code, and those permissions are then applied to code in all your projects and domains.

Global access is recommended for most use cases since it is simpler, but if you have a compelling reason to restrict access, then the project-domain-scoped access is available, at the cost of some additional complexity in setup.

> [!NOTE] Relationship with RBAC
> The permissions being discussed here are attached to a project and domain.
> This is independent of the permissions granted to users and machine applications through {{< key product_name >}}'s role-based access control (see [User management](../../user-guide/administration/user-management)).
> But, the two types of permissions are related.
>
> For example, for a user (or machine application) to have read access to an S3 bucket, two things are required:
>
> * The user (or machine application) must have **execute** permission for the project and domain where the code that does the reading resides.
> * The project and domain must have read permission for the S3 bucket.

## Background

As you know, your workflows and tasks run in a Kubernetes cluster within your data plane.
Within that cluster, the Kubernetes pods allocated to run your task code are organized as follows:

* The set of task pods is partitioned into namespaces where each namespace corresponds to a project-domain pair.
* All workflows running in a given project and domain are run on pods within that namespace.
  For example, code in the `development` domain of project `foo` runs in the namespace `foo-development` while code in the `staging` domain of project `bar` runs in the namespace `bar-staging`, and so forth.
* By default, all project-domain namespaces are bound to a common IAM role which we will refer to as `<UserFlyteRole>`.
  Its actual name differs from organization to organization. **The actual name will have the form `<YourOrgPrefix>-userflyterole`**.
* The role `<UserFlyteRole>` has an attached policy called `userflyterole`.
  This policy contains all the permissions granted to your task code when your data plane was set up.
  If you requested permissions for resources specific to your organization at set up time, they will have been added here.

> [!NOTE] `<UserFlyteRole>` vs `userflyterole`
> The entity that we refer to here as `<UserFlyteRole>` is an IAM role.
> As mentioned the actual name of this role in your system will be of the form `<YourOrgPrefix>-userflyterole.`
>
> By default, this role has an attached IAM policy called `userflyterole`.
> This is the literal name used in all AWS-based data planes.
>
> **Be aware of the difference and don't get these two things confused!**

> [!NOTE] `<UserFlyteRole>`vs `<AdminFlyteRole>`
> In addition to the task pods, your cluster also contains pods that run {{< key product_name >}} services, which are used to manage tasks and to connect your cluster to the control plane.
> These pods are bound to a different default role, `<AdminFlyteRole>` (again, its actual name differs from organization to organization).
> The separation of this role from `<UserFlyteRole>` serves to provide isolation between {{< key product_name >}} administrative logic and your workflow logic.
>
> **You should not alter any settings associated with `<AdminFlyteRole>`**.

## Enabling access

To enable your task code to access a resource:

* [**Create a custom policy**](#creating-a-custom-policy) that grants the appropriate permissions for your resource.
  This is the step where you define exactly which permissions you want to grant (read-only, read/write, list, etc.).
  The name of this policy is yours to determine.
  Here we will refer to it as `<CustomPolicy>`.

You can then choose whether to enable **global access** or **project-domain-scoped access**:

* [**To enable global access** ](#setting-up-global-access) to the resource, you simply attach `<CustomPolicy>` to the existing `<UserFlyteRole>`.
* [**To enable project-domain-scoped access**](#setting-up-project-domain-scoped-access) to your resource:
  * Create your own custom role (let's refer to it `<CustomRole>`)
  * Attach `<CustomPolicy>` to `<CustomRole>`.
  * Also, attach the policy called `userflyterole` to `<CustomRole>` (this will ensure that `<CustomRole>` has all the default permissions needed to allow tasks to run).
  * Attach `<CustomRole>` to the desired project-domain namespace.

![](../../_static/images/user-guide/integrations/enabling-aws-resources/union-roles.png)

### Creating a custom policy

Regardless of which route you take (global vs project-domain-scoped) the first step is to create a policy that grants the desired permissions to your resource.

To create a new policy:

* Go to **IAM > Access management > Policies**.
* Select **Create policy**.
* Go through the sections of the visual editor to define the permissions you wish to grant.
  * Alternatively, you can paste a JSON definition directly into the JSON editor.
  * The details of what permissions to grant depend on the resource in question and the access you wish to grant.
    Specific examples are covered in [Enabling AWS S3](./enabling-aws-s3) and [Enabling AWS Secrets Manager](./enabling-aws-secrets-manager).
* Proceed through the steps of the wizard, give your policy a name (which we will call `<CustomPolicy>`), and select **Create policy**.
* Record the name and ARN of your policy.
  Here we will refer to the ARN is `<CustomPolicyArn>`.

### Setting up global access

To set up global access, you must bind the `<CustomPolicy>` that you created above to the role `<UserFlyteRole>`.

> [!NOTE]
> As mentioned above, the actual name of `<UserFlyteRole>` has the form:
>
> **`<YourOrgPrefix>-userflyterole`**
>
> You should be able to find the role by searching in your AWS IAM console for roles with names that follow that pattern.

* Go to **IAM > Access management > Roles**.
* Find `<UserFlyteRole>` and select the checkbox beside it.
* In the **Add Permissions** drop-down menu, select **Attach Policies**.
* In the displayed list find `<CustomPolicy>` and select its checkbox, then select **Add permissions**.

> [!NOTE]
> Alternatively, you can perform the binding from the command line like this:
>
> ```shell
> $ aws iam attach-role-policy \
>  --policy-arn <CustomPolicyArn> \
>  --role-name <UserFlyteRole>
> ```
>
> Notice that in this case, you have to use `<CustomPolicyArn>` here instead of `<CustomPolicy>`.

**At this point, all task code in your organization will have access to the cloud resource as defined by your custom policy.**

### Setting up project-domain-scoped access

To set up project-domain-scoped access, you do this:

In AWS:

* Create the IAM role, `<CustomRole>`.
* Add the `userflyterole` policy to `<CustomRole>`.
* Add `<CustomPolicy>` to `<CustomRole>`.

In {{< key product_name >}} (using `uctl`):

* Bind `<CustomRole>` to the project-domain pair desired.

### Create the IAM role

1. Sign in to the AWS Management Console as an administrator of your account, and open the IAM console.
2. In the navigation pane, choose **Roles** and then choose **Create role**.
3. Choose the **Web identity** role type.
4. In the **Identity provider** dropdown select `oidc.eks.<Suffix>.`Record this name.
5. Choose `sts.amazonaws.com` as the **Audience** and select **Next**.
6. On the **Add permissions** page, search for the `userflyterole` policy and check the box beside it and select **Next**.
7. Enter a name and description for this role.
8. Under **Step 1: Select trusted entities**, click edit and _replace_ the `Condition` block with the following, where `oidc.eks.<Suffix>` is the value from step 4, and `<Project>`, and `<Domain>` are the {{< key product_name >}} project and domain pairs you want to set custom permissions for. Repeat for each project-domain pair.

```json
"Condition": {
    "StringEquals": {
        "oidc.eks.<Suffix>:sub": [
            "system:serviceaccount:<Project>-<Domain1>:default",
            "system:serviceaccount:<Project>-<Domain2>:default"
        ]
    }
}
```

9. Add additional permissions as needed, following [these steps](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_manage-attach-detach.html).
10. Select **Create role**.
11. In the **Summary** section of the new role's details pane, note the ARN value.

### Configure the cluster to use the new IAM role

Repeat the following steps for each project-domain pair:

1.  Create a file named `cluster_resource_attributes.yaml` with the following contents:

```yaml
attributes:
defaultUserRoleValue: <ARN from step 11 above>
domain: <domain>
project: <project>
```

2.  Run the following command to override the IAM role used for {{< key product_name >}} Tasks in this Project-Domain:

```shell
$ uctl update cluster-resource-attribute --attrFile cluster_resource_attributes.yaml
```

3.  You can verify the overrides by running:

```shell
$ uctl get cluster-resource-attribute -p <project> -d <domain>
```

**At this point, only code in your chosen project-domain pairs will have access to the cloud resource as defined by your custom policy.**
