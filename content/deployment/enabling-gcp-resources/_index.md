---
title: Enabling GCP resources
weight: 10
variants: -flyte -serverless +byoc -selfmanaged
sidebar_expanded: true
---

# Enabling GCP resources

Components of your {{< key product_name >}} data plane will need to connect to and communicate with other resources in your cloud environment such as [Cloud Storage](./enabling-google-cloud-storage), [Artifact Registry](./enabling-google-artifact-registry), [BigQuery](./enabling-bigquery), and so forth.

> [!NOTE] Secret management
> We strongly recommend using the [{{< key product_name >}} secrets manager](../../user-guide/development-cycle/managing-secrets) to manage secrets rather than Google Secret Manager. If your organization must use Google Secret Manager, however, see [Enabling Google Secret Manager](./enabling-google-secret-manager).

As much as possible, access to the resources you need will be pre-configured by the {{< key product_name >}} team when they set up your data plane.
For example, if you want your task code to have access to a specific Cloud Storage bucket or BigQuery, this can be pre-configured.
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
  The most common case occurs when you are using Artifact Registry for your task container images and it resides in a project other than the one containing your data plane.
  In that case, some configuration is required to enable the {{< key product_name >}} operator on your data plane to pull images from the registry when registering your workflows and tasks.
  **If you are using an Artifact Registry instance within the same project as your data plane, then access is enabled by default and no further configuration is needed.**
* **Task code access**:
  Enabling access to a resource for your task code.
  For example, your task code might need to access Cloud Storage or Secret Manager at runtime.
  This involves granting permission to a Google Service Account (GSA) that is attached to the Kubernetes cluster within which your task code runs.

## Infrastructure-level access

The only infrastructure-level access issue you are likely to encounter is around access to an Artifact Registry _in a GCP project other than the one in which your data plane resides_.

**If your task container images are stored in an Artifact Registry in the same GCP project as your data plane, then access is already enabled. You do not have to do anything.**

If your task container images reside in an Artifact Registry instance in **another GCP project** you will need to configure that instance to allow access from your data plane.
See Enabling Artifact Registry for details.

## Task code access

When your task code runs, it executes within a pod in the Kubernetes cluster in your data plane.
To enable your task code to access cloud resources you must grant the appropriate permissions to the Google Service Account (GSA) attached to the Kubernetes cluster.

There are two main options for setting this up:

* **Domain-scoped access**: With this arrangement, you define the permissions you want to grant to your task code, and those permissions are applied only to a specific domain.
* **Global access**: With this arrangement, you define the permissions you want to grant to your task code, and those permissions are then applied to code in all your projects and domains.

> [!NOTE] GCP only supports scoping by domain
> In AWS-based data planes, scoping by both project _and_ domain is supported.
> However, due to intrinsic architectural constraints, GCP-based data planes only support scoping by domain.

Global access is recommended for most use cases since it is simpler, but if you have a compelling reason to restrict access, then the project-domain-scoped access is available, at the cost of some additional complexity in setup.

> [!NOTE] Relationship with RBAC
> The permissions being discussed here are attached to a domain.
> This is independent of the permissions granted to users and machine applications through {{< key product_name >}}'s role-based access control (see [User management](../../user-guide/administration/user-management)).
> But, the two types of permissions are related.
>
> For example, for a user (or machine application) to have read access to a Cloud Storage bucket, two things are required:
>
> * The user (or machine application) must have **execute** permission for the project and domain where the code that does the reading resides.
> * The domain must have read permission for the Cloud Storage bucket.

## Domain-scoped access

**Because of the way that GCP works internally, domain-scoped access can only be configured by the {{< key product_name >}} team.**

Please work directly with the {{< key product_name >}} team if you have requirements that involve domain-scoped access to cloud resources.

If you need to add or change domain-scoped access after your data plane has been set up, you should also contact the team.

## Globally-scoped access

You can manage the configuration of globally-scoped access to GCP resources yourself without involving the {{< key product_name >}} team.

In a GCP-based {{< key product_name >}} data plane, globally-scoped access to resources is mediated by a single Google Service Account (GSA) that is configured as part of the data plane setup.
We refer to it as `<UserFlyteGSA>`.

`<UserFlyteGSA>` is bound to all the pods in your data plane's Kubernetes cluster that run your Flyte code.

To enable access to a resource in GCP you grant `<UserFlyteGSA>`access to that resource and assign it a role that includes the permissions that you want your code to have.

> [!NOTE] `<UserFlyteGSA>`
> Here we refer to the default global-access GSA as`<UserFlyteGSA>`because the precise name differs across installations.
> This GSA is identified by name and email of the following form:
>
> * Name: `<OrgName>-userflyterol-<Suffix>`
> * Email: `<OrgName>-userflyterol-<Suffix>@<OrgName>-gcp-dataplane.iam.gserviceaccount.com`

> [!NOTE] Google Service Account (GSA)
> We use the term Google Service Account (GSA) to refer to the accounts that are managed in the GCP console under **IAM & Admin > Service Accounts**.
> This is to distinguish them from Kubernetes Service Accounts (KSAs).
> KSAs are a distinct type of service account managed _within_ the Kubernetes cluster. You will not normally encounter these at the data plane level.

## Find the actual name of `<UserFlyteGSA>`

In this section we refer to the default global-access GSA as`<UserFlyteGSA>`because the precise name differs across installations. The actual name and email of this GSA have the following forms:

* Name: `<OrgName>-userflyterol-<Suffix>`
* Email: `<OrgName>-userflyterol-<Suffix>@<OrgName>-gcp-dataplane.iam.gserviceaccount.com`

**You will need to have the email identifier of this role on hand when you enable access to resources for your task code.**

To find the actual name of this GSA do the following:

* In the GCP data plane project, go to **IAM & Admin > Service accounts**.
* In the list of service account, find the one whose name and email match the pattern above. For example:

![](../../_static/images/user-guide/integrations/enabling-gcp-resources/user-flyte-gsa.png)

* Copy this name to document in an editor.
  You will need it later to configure each specific resource.
