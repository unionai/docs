---
title: Customizing resources
weight: 7
variants: +flyte -serverless -byoc -selfmanaged
---

# Customizing project, domain, and workflow resources with flytectl

For critical projects and workflows, you can use the `flytectl update task-resource-attribute` command to configure
settings for task, cluster, and workflow execution resources, set matching executions to execute on specific clusters, set execution queue attributes, and [other attributes](https://github.com/flyteorg/flyte/blob/95baed556f5844e6a494507c3aa5a03fe6d42fbb/flyteidl/protos/flyteidl/admin/matchable_resource.proto#L15)
that differ from the default values set for your global Flyte installation. These customizable settings are created, updated, and deleted via the API and stored in the FlyteAdmin database.

In code, these settings are sometimes called `matchable attributes` or `matchable resources`, because we use a hierarchy for matching the customizations to applicable Flyte inventory and executions.

## Configuring existing resources

### About the resource hierarchy

Many platform specifications set in the FlyteAdmin config are applied to every project and domain. Although these values are customizable as part of your helm installation, they are still applied to every user project and domain combination.

You can choose to customize these settings along increasing levels of specificity with Flyte:

- Domain
- Project and Domain
- Project, Domain, and Workflow name
- Project, Domain, Workflow name and LaunchPlan name

See :ref:`control-plane` to understand projects and domains.
The following section will show you how to configure the settings along
these dimensions.

### Task resources

As a system administrator you may want to define default task resource requests and limits across your Flyte deployment. This can be set globally in the FlyteAdmin [config](https://github.com/flyteorg/flyte/blob/95baed556f5844e6a494507c3aa5a03fe6d42fbb/charts/flyte-core/values.yaml#L786-L795)
under `task_resource_defaults`.

**Default** values get injected as the task requests and limits when a task definition omits a specific resource.

**Limit** values are only used as validation. Neither a task request nor limit can exceed the limit for a resource type.

#### Configuring task resources

Available resources for configuration include:

- CPU
- GPU
- Memory
- [Ephemeral Storage](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#local-ephemeral-storage)

In the absence of a customization, the global
default values in `task_resource_defaults` are used.

The customized values from the database are assigned at execution, rather than registration time.

### Customizing task resource configuration


To customize resources for project-domain attributes using `flytectl`, define a ``tra.yaml`` file with your customizations:


```yaml
project: flyteexamples
domain: development
defaults:
    cpu: "1"
    memory: 150Mi
limits:
    cpu: "2"
    memory: 450Mi
```
Update the task resource attributes for a project-domain combination:

```bash
flytectl update task-resource-attribute --attrFile tra.yaml
```
> Refer to the :ref:`docs <flytectl:flytectl_update_task-resource-attribute>` to learn more about the command and its supported flag(s).

To fetch and verify the individual project-domain attributes:

```bash
    flytectl get task-resource-attribute -p flyteexamples -d development
```

You can view all custom task-resource-attributes by visiting
``protocol://<host/api/v1/matchable_attributes?resource_type=0>`` and substitute
the protocol and host appropriately.

### Cluster resources


Cluster resources are how you configure Kubernetes namespace attributes that are applied at execution time.
This includes per-namespace resource quota, patching the default service account with a bounded IAM role, or attaching `imagePullSecrets` to the default service account for accessing a private container registry

#### Configuring cluster resources

The format of all these parameters are free-form key-value pairs used for populating the Kubernetes object templates consumed by the cluster resource controller. The cluster resource controller ensures these fully rendered object templates are applied as Kubernetes resources for each execution namespace.

The keys represent templatized variables in the
[cluster resource template](https://github.com/flyteorg/flyte/blob/95baed556f5844e6a494507c3aa5a03fe6d42fbb/charts/flyte-core/values.yaml#L1035-L1056)
and the values are what you want to see filled in.

In the absence of custom customized values, your Flyte installation will use ``customData`` from the FlyteAdmin config
as the per-domain defaults. Flyte specifies these defaults by domain and applies them to every project-domain namespace combination.

#### Customizing cluster resource configuration

The cluster resource template values can be specified on domain, and project-and-domain.
Since Flyte execution namespaces are never on a per-workflow or a launch plan basis, specifying a workflow or launch plan level customization is non-actionable.
This is a departure from the usual hierarchy for customizable resources.

Define an attributes file, ``cra.yaml``:

```yaml

domain: development
project: flyteexamples
attributes:
    projectQuotaCpu: "1000"
    projectQuotaMemory: 5Ti
```
To ensure that the customizations reflect in the Kubernetes namespace
``flyteexamples-development`` (that is, the namespace has a resource quota of
1000 CPU cores and 5TB of memory) when the admin fills in cluster resource
templates:

```bash
flytectl update cluster-resource-attribute --attrFile cra.yaml
```

To fetch and verify the individual project-domain attributes:

```bash
flytectl get cluster-resource-attribute -p flyteexamples -d development
```
Flyte uses these updated values to fill the template fields for the
``flyteexamples-development`` namespace.

For other namespaces, the
[platform defaults](https://github.com/flyteorg/flyte/blob/95baed556f5844e6a494507c3aa5a03fe6d42fbb/charts/flyte-core/values.yaml#L1035-L1056)
apply.


> The template values, for example, ``projectQuotaCpu`` or ``projectQuotaMemory`` are free-form strings. Ensure that they match the template placeholders in your values file (e.g. [values-eks.yaml](https://github.com/flyteorg/flyte/blob/95baed556f5844e6a494507c3aa5a03fe6d42fbb/charts/flyte-core/values-eks.yaml#L357-L379)) for your changes to take effect and custom values to be substituted.

You can view all custom cluster-resource-attributes by visiting ``protocol://<host/api/v1/matchable_attributes?resource_type=1>``
and substitute the protocol and host appropriately.

### Workflow execution configuration


Although many execution-time parameters can be overridden at execution time itself, it is helpful to set defaults on a per-project or per-workflow basis. This config includes
annotations and labels in the [Workflow execution config](https://github.com/flyteorg/flyte/blob/95baed556f5844e6a494507c3aa5a03fe6d42fbb/flyteidl/gen/pb_python/flyteidl/admin/matchable_resource_pb2.pyi#L15-L24).
- `max_parallelism`: Limits maximum number of nodes that can be evaluated for an individual workflow in parallel
- [security context](https://github.com/flyteorg/flyte/blob/95baed556f5844e6a494507c3aa5a03fe6d42fbb/flyteidl/protos/flyteidl/core/security.proto#L118): configures the pod identity and auth credentials for task pods at execution time
- `raw_output_data_config`: where offloaded user data is stored
- `interruptible`: whether to use [spot instances](https://docs.flyte.org/en/user_guide/productionizing/spot_instances.html)
- `overwrite_cache`: Allows for all cached values of a workflow and its tasks to be overwritten for a single execution.
- `envs`: Custom environment variables to apply for task pods brought up during execution

#### Customizing workflow execution configuration

These can be defined at two levels of project-domain or project-domain-workflow:

```bash
flytectl update workflow-execution-config
```

#### Execution cluster label

This matchable attribute allows forcing a matching execution to consistently execute on a specific Kubernetes cluster for multi-cluster Flyte deployment set-up. In lieu of an explicit customization, cluster assignment is random.

For setting up a multi-cluster environment, follow [the guide](https://www.union.ai/docs/flyte/deployment/flyte-deployment/multicluster/)

#### Customizing execution cluster label configuration


Define an attributes file in `ec.yaml`:

```yaml
value: mycluster
domain: development
project: flyteexamples
```
Ensure that admin places executions in the flyteexamples project and development domain onto ``mycluster``:

```bash
flytectl update execution-cluster-label --attrFile ec.yaml
```

To fetch and verify the individual project-domain attributes:

```bash
flytectl get execution-cluster-label -p flyteexamples -d development
```

You can view all custom execution cluster attributes by visiting
``protocol://<host/api/v1/matchable_attributes?resource_type=3>`` and substitute
the protocol and host appropriately.

### Execution queues

Execution queues are defined in [FlyteAdmin configuration](https://github.com/flyteorg/flyte/blob/95baed556f5844e6a494507c3aa5a03fe6d42fbb/flyteadmin/flyteadmin_config.yaml#L138-L148).
These are used for execution placement for constructs like AWS Batch.

The **attributes** associated with an execution queue must match the **tags**
for workflow executions. The tags associated with configurable resources are
stored in the admin database.

#### Customizing execution queue configuration


```bash
flytectl update execution-queue-attribute
```

You can view existing attributes for which tags can be assigned by visiting
``protocol://<host>/api/v1/matchable_attributes?resource_type=2`` and substitute
the protocol and host appropriately.

## Adding new customizable resources


As a quick refresher, custom resources allow you to manage configurations for specific combinations of user projects, domains and workflows that customize default values.
Examples of such resources include execution clusters, task resource defaults, and more.


In a multi-cluster setup, an example one could think of is setting routing rules to send certain workflows to specific clusters, which demands setting up custom resources.

Here's how you could go about building a customizable priority designation.


**Example**

Let's say you want to inject a default priority annotation for your workflows.
Perhaps you start off with a model where everything has a default priority but soon you realize it makes sense that workflows in your production domain should take higher priority than those in your development domain.

Now, one of your user teams requires critical workflows to have a higher priority than other production workflows.

Here's how you could do that.

**Flyte IDL**


Introduce a new [matchable resource](https://github.com/flyteorg/flyte/blob/95baed556f5844e6a494507c3aa5a03fe6d42fbb/flyteidl/protos/flyteidl/admin/matchable_resource.proto#L15) that includes a unique enum value and proto message definition.

For example:

```

   enum MatchableResource {
     ...
     WORKFLOW_PRIORITY = 10;
   }

   message WorkflowPriorityAttribute {
     int priority = 1;
   }

   message MatchingAttributes {
     oneof target {
       ...
       WorkflowPriorityAttribute WorkflowPriority = 11;
     }
   }
```

See the changes in this `file <https://github.com/flyteorg/flyteidl/commit/b1767697705621a3fddcb332617a5304beba5bec#diff-d3c1945436aba8f7a76755d75d18e671>`__ for an example of what is required.


**FlyteAdmin**


Once your IDL changes are released, update the logic of FlyteAdmin to `fetch <https://github.com/flyteorg/flyteadmin/commit/60b4c876ea105d4c79e3cad7d56fde6b9c208bcd#diff-510e72225172f518850fe582149ff320R122-R128>`__ your new matchable priority resource and use it while creating executions or in relevant use cases.

For example:

```

   resource, err := s.resourceManager.GetResource(ctx, managerInterfaces.ResourceRequest{
       Domain:       domain,
       Project:      project, // optional
       Workflow:     workflow, // optional, must include project when specifying workflow
       LaunchPlan:   launchPlan, // optional, must include project + workflow when specifying launch plan
       ResourceType: admin.MatchableResource_WORKFLOW_PRIORITY,
   })

   if err != nil {
       return err
   }

   if resource != nil && resource.Attributes != nil && resource.Attributes.GetWorkflowPriority() != nil {
        priorityValue := resource.Attributes.GetWorkflowPriority().GetPriority()
        // do something with the priority here
   }
```

**Flytekit**

For convenience, add a FlyteCTL wrapper to update the new attributes. Refer to [this PR](https://github.com/flyteorg/flytectl/pull/65) for the entire set of changes required.

That's it! You now have a new matchable attribute to configure as the needs of your users evolve.
