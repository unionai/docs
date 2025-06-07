---
title: Multi-cluster
weight: 3
variants: +flyte -serverless -byoc -selfmanaged
---

# Multi-cluster

The multi-cluster deployment described in this section assumes that you have deployed the `flyte-core` helm chart, which runs the individual flyte components separately.
This is needed because in a multi-cluster setup, the execution engine (`flytepropeller`) is deployed to multiple k8s clusters; hence it wouldn't work with the `flyte-binary` helm chart, since it deploys all flyte services as one single binary.

> [!NOTE]
> Union.ai offers simplified support for multi-cluster and multi-cloud.
> [Learn more]({{< docs_home byoc >}}/deployment/multi-cluster#multi-cluster-and-multi-cloud) or [book a demo](https://union.ai/demo).

## Scaling Beyond Kubernetes

As described in the [Architecture Overview](https://docs.flyte.org/en/latest/concepts/architecture.html), the Flyte control plane (`flyteadmin`) sends workflows off to the Data Plane (`flytepropeller`) for execution.
The data plane fulfills these workflows by launching pods in Kubernetes.

The case for multiple Kubernetes clusters may arise due to security constraints, cost-effectiveness or a need to scale out computing resources.

To address this, you can deploy Flyte's data plane to multiple Kubernetes clusters.
The control plane (`flyteadmin`) can be configured to submit workflows to these individual data planes.
Additionally, Flyte provides the mechanisms for administrators to retain control on the workflow placement logic while enabling users to reap the benefits using simple abstractions like `projects` and `domains`.

### Prerequisites

To make sure that your multi-cluster deployment is able to scale and process requests successfully, the following environment-specific requirements should be met:

1. An IAM Policy that defines the permissions needed for Flyte. A minimum set of permissions include:

   ```json
   "Action": [
      "s3:DeleteObject*",
      "s3:GetObject*",
      "s3:ListBucket",
      "s3:PutObject*"
   ],
   "Resource": [
      "arn:aws:s3:::<your-S3-bucket>*",
      "arn:aws:s3:::<your-S3-bucket>*/*"
   ],
   ```

2. Two IAM Roles configured: one for the control plane components, and another for the data plane where the worker Pods and `flytepropeller` run.
   Use the recommended security strategy for the cloud provider you're running on.
   For example, IRSA for EKS environments or Workload Identity Federation for GCP.

3.  Mapping between the `default` Service Account in each `project-domain` namespace and the assumed role in your cloud environment.
    By default, every Pod created for a Task execution, uses the `default` Service Account in their respective namespace.
    In your cluster, you'll have as many namespaces as `project` and `domain` combinations you may have.

### Data Plane Deployment

This guide assumes that you have two Kubernetes clusters and that you can access them all with `kubectl`.

Let's call these clusters `dataplane1` and `dataplane2`. In this section, you'll prepare the first cluster only.

1. Add the `flyteorg` Helm repo:

   ```shell
   $ helm repo add flyteorg https://flyteorg.github.io/flyte
   $ helm repo update
   ```

2. Get the `flyte-core` Helm chart:

   ```shell
   $ helm fetch --untar --untardir . flyteorg/flyte-core
   $ cd flyte-core
   ```

3. Open the `values-dataplane.yaml` file and add the following contents:

   ```yaml
   configmap:
     admin:
       admin:
         endpoint: <your-Ingress-FQDN>:443 #indicate the URL you're using to connect to Flyte
         insecure: false #enables secure communication over SSL. Requires a signed certificate
      catalog:
        catalog-cache:
          endpoint: <your-datacatalog-address>
          insecure: false
   ```

   This step is needed so the `flytepropeller` instance in the data plane cluster is able to send notifications back to the `flyteadmin` service in the control plane.

   The `catalog` service runs in the control plane and is used when caching is enabled.
   Note that `catalog` is not exposed via the ingress by default and does not have its own authentication mechanism.
   The `catalog` service in the control plane cluster can, for instance, be made available to the `flytepropeller` services in the data plane clusters with an internal load balancer service.
   See [GKE documentation](https://cloud.google.com/kubernetes-engine/docs/how-to/internal-load-balancing#create>) or
   [AWS Load Balancer Controller](https://kubernetes-sigs.github.io/aws-load-balancer-controller/latest/guide/service/nlb) if the clusters use the same VPC network.

4. Install the Flyte data plane Helm chart. Use the same base `values` file you used to deploy the control plane:

   **AWS**

   ```bash

   $ helm install flyte-core-data flyteorg/flyte-core -n flyte \
          --values values-eks.yaml --values values-dataplane.yaml \
          --create-namespace
   ```

   **GCP**

   ```bash
   $ helm install flyte-core-data -n flyte flyteorg/flyte-core  \
          --values values-gcp.yaml \
          --values values-dataplane.yaml \
          --create-namespace flyte
   ```

## Control Plane configuration

For `flyteadmin` to access and create Kubernetes resources in one or more Flyte data plane clusters, it needs credentials to each cluster.
Flyte makes use of Kubernetes Service Accounts to enable every control plane cluster to perform authenticated requests to the Kubernetes API Server in the data plane cluster.
The default behavior is that the Helm chart creates a [ServiceAccount](https://github.com/flyteorg/flyte/blob/master/charts/flyte-core/templates/admin/rbac.yaml#L4)in each data plane cluster.
In order to verify requests, the Kubernetes API Server expects a [signed bearer token](https://kubernetes.io/docs/reference/access-authn-authz/authentication/#service-account-tokens) attached to the Service Account.
Starting with Kubernetes 1.24, the bearer token has to be generated manually.

1. Use the following manifest to create a long-lived bearer token for the `flyteadmin` Service Account in your data plane cluster:

   ```shell
   $ kubectl apply -f - <<EOF
     apiVersion: v1
     kind: Secret
     metadata:
        name: dataplane1-token
        namespace: flyte
        annotations:
           kubernetes.io/service-account.name: flyteadmin
     type: kubernetes.io/service-account-token
     EOF
   ```

2. Create a new file named `secrets.yaml` that looks like:

   ```yaml
      apiVersion: v1
      kind: Secret
      metadata:
        name: cluster-credentials
        namespace: flyte
      type: Opaque
      data:
   ```

   > [!NOTE]
   > The credentials have two parts (`CA cert` and `bearer token`).

3. Copy the bearer token of the first data plane cluster's secret to your clipboard using the following command:

   ```shell
   $ kubectl get secret -n flyte dataplane1-token \
             -o jsonpath='{.data.token}' | pbcopy
   ```

4. Go to `secrets.yaml` and add a new entry under `stringData` with the data plane cluster token:

   ```yaml
      apiVersion: v1
      kind: Secret
      metadata:
        name: cluster-credentials
        namespace: flyte
      type: Opaque
      data:
        dataplane_1_token: <your-dataplane1-token>
   ```
5. Obtain the corresponding certificate:

   ```shell
   $ kubectl get secret -n flyte dataplane1-token \
             -o jsonpath='{.data.ca\.crt}' | pbcopy
   ```

6. Add another entry in your `secrets.yaml` file for the certificate:

   ```yaml
   apiVersion: v1
   kind: Secret
   metadata:
      name: cluster-credentials
      namespace: flyte
   type: Opaque
   data:
      dataplane_1_token: <your-dataplane1-token>
      dataplane_1_cacert: <your-dataplane1-token-certificate>
   ```

7. Connect to your control plane cluster and create the `cluster-credentials` secret:

   ```shell
   $ kubectl apply -f secrets.yaml
   ```

8. Create a file named `values-override.yaml` and add the following config to it:

   ```yaml
   flyteadmin:
     additionalVolumes:
     - name: cluster-credentials
       secret:
         secretName: cluster-credentials
     additionalVolumeMounts:
     - name: cluster-credentials
       mountPath: /var/run/credentials
     initContainerClusterSyncAdditionalVolumeMounts:
     - name: cluster-credentials
       mountPath: /etc/credentials
   configmap:
     clusters:
      labelClusterMap:
        label1:
        - id: dataplane_1
          weight: 1
      clusterConfigs:
      - name: "dataplane_1"
        endpoint: https://<your-dataplane1-kubeapi-endpoint>:443
        enabled: true
        auth:
           type: "file_path"
           tokenPath: "/var/run/credentials/dataplane_1_token"
           certPath: "/var/run/credentials/dataplane_1_cacert"
   ```

   > [!NOTE]
   > Typically, you can obtain your Kubernetes API endpoint URL using `kubectl cluster-info`

   In this configuration, `label1` and `label2` are just labels that we will use later in the process to configure mappings that enable workflow executions matching those labels, to be scheduled on one or multiple clusters depending on the weight (e.g. `label1` on `dataplane_1`). The `weight` is the priority of a specific cluster, relative to the other clusters under the `labelClusterMap` entry. The total sum of weights under a particular label has to be `1`.

9. Add the data plane IAM Role as the `defaultIamRole` in your Helm values file. [See AWS example](https://github.com/flyteorg/flyte/blob/97a79c030555eaefa3e27383d9b933ba1fdc1140/charts/flyte-core/values-eks.yaml#L351-L365)

10. Update the control plane Helm release:

    This step will disable `flytepropeller` in the control plane cluster, leaving no possibility of running workflows there. If you require the control plane to run workflows, edit the `values-controlplane.yaml` file and set `flytepropeller.enabled` to `true` and add one additional cluster config for the control plane cluster itself:

    ```yaml
    configmap:
       clusters:
          clusterConfigs:
          - name: "dataplane_1"
             ...
          - name: "controlplane"
             enabled: true
             inCluster: true  # Use in-cluster credentials
    ```
    Then, complete the `helm upgrade` operation.

    **AWS**

    ```shell
    $ helm upgrade flyte-core flyteorg/flyte-core \
           --values values-eks-controlplane.yaml --values values-override.yaml \
           --values values-eks.yaml -n flyte
    ```

    **GCP**

    ```shell
    $ helm upgrade flyte -n flyte flyteorg/flyte-core values.yaml \
           --values values-gcp.yaml \
           --values values-controlplane.yaml \
           --values values-override.yaml
    ```

11. Verify that all Pods in the `flyte` namespace are `Running`:

    ```shell
    $ kubectl get pods -n flyte
    ```

    Example output:

    ```shell
    NAME                             READY   STATUS    RESTARTS   AGE
    datacatalog-86f6b9bf64-bp2cj     1/1     Running   0          23h
    datacatalog-86f6b9bf64-fjzcp     1/1     Running   0          23h
    flyteadmin-84f666b6f5-7g65j      1/1     Running   0          23h
    flyteadmin-84f666b6f5-sqfwv      1/1     Running   0          23h
    flyteconsole-cdcb48b56-5qzlb     1/1     Running   0          23h
    flyteconsole-cdcb48b56-zj75l     1/1     Running   0          23h
    flytescheduler-947ccbd6-r8kg5    1/1     Running   0          23h
    syncresources-6d8794bbcb-754wn   1/1     Running   0          23h
    ```

## Configure Execution Cluster Labels

The next step is to configure project-domain or workflow labels to schedule on a specific Kubernetes cluster.

### Project-domain execution labels

1. Create an `ecl.yaml` file with the following contents:

   ```yaml
   domain: development
   project: project1
   value: label1
   ```

   > [!NOTE]
   > Change `domain` and `project` according to your environment.  The `value` has to match with the entry under `labelClusterMap` in the `values-override.yaml` file.

2. Repeat step 1 for every project-domain mapping you need to configure, creating a YAML file for each one.

3. Update the execution cluster label of the project and domain:

   ```shell
   $ flytectl update execution-cluster-label --attrFile ecl.yaml
   ```

   Example output:

   ```shell
   Updated attributes from team1 project and domain development
   ```

4. Execute a workflow indicating project and domain:

   ```shell
   $ pyflyte run --remote --project team1 --domain development example.py  training_workflow \                                                          ✔ ╱ docs-development-env 
             --hyperparameters '{"C": 0.1}'
   ```

### Configure a Specific Workflow mapping

1. Create a `workflow-ecl.yaml` file with the following example contents:

   ```yaml
   domain: development
   project: project1
   workflow: example.training_workflow
   value: project1
   ```

2. Update execution cluster label of the project and domain

   ```shell
   $ flytectl update execution-cluster-label \
              -p project1 -d development \
              example.training_workflow \
              --attrFile workflow-ecl.yaml
   ```

3. Execute a workflow indicating project and domain:

   ```shell
   $ pyflyte run --remote --project team1 --domain development example.py  training_workflow \                                                          ✔ ╱ docs-development-env 
             --hyperparameters '{"C": 0.1}'
   ```

Congratulations!
With this, the execution of workflows belonging to a specific
project-domain or a single specific workflow will be scheduled on the target label
cluster.

## Day 2 Operations

### Add another Kubernetes cluster

The process can be repeated for additional clusters.

1. Provision the new cluster and add it to the permissions structure (IAM, etc.).

2. Install the data plane Helm chart following the steps in the [Data plane deployment](#data-plane-deployment) section.

3. Follow steps 1-3 in the [control plane configuration](#control-plane-configuration) to generate and populate a new section in your `secrets.yaml` file.
   For example:

   ```yaml
   apiVersion: v1
   kind: Secret
   metadata:
     name: cluster-credentials
     namespace: flyte
   type: Opaque
   data:
     dataplane_1_token: <your-dataplane1-token>
     dataplane_1_cacert: <your-dataplane1-token-certificate>
     dataplane_2_token: <your-dataplane2-token>
     dataplane_2_cacert:  <your-dataplane2-token-certificate>
   ```

4. Connect to the control plane cluster and update the `cluster-credentials` Secret:

   ```bash
   kubect apply -f secrets.yaml
   ```

5. Go to your `values-override.yaml` file and add the information of the new cluster.
   Adding a new label is not entirely needed.
   Nevertheless, in the following example a new label is created to illustrate Flyte's capability to schedule workloads on different clusters in response to user-defined mappings of `project`, `domain` and `label`:

   ```yaml
   ... #all the above content remains the same
      configmap:
      clusters:
      labelClusterMap:
         label1:
         - id: dataplane_1
            weight: 1
         label2:
         - id: dataplane_2
            weight: 1
      clusterConfigs:
      - name: "dataplane_1"
         endpoint: https://<DATAPLANE-1-K8S-API-ENDPOINT>.com:443
         enabled: true
         auth:
            type: "file_path"
            tokenPath: "/var/run/credentials/dataplane_1_token"
            certPath: "/var/run/credentials/dataplane_1_cacert"
      - name: "dataplane_2"
         endpoint: https://<DATAPLANE-1-K8S-API-ENDPOINT>:443
         enabled: true
         auth:
            type: "file_path"
            tokenPath: "/var/run/credentials/dataplane_2_token"
            certPath: "/var/run/credentials/dataplane_2_cacert"
   ```

6. Update the Helm release in the control plane cluster:

   ```shell
   $ helm upgrade flyte-core-control flyteorg/flyte-core  -n flyte --values values-controlplane.yaml --values values-eks.yaml --values values-override.yaml
   ```

7. Create a new execution cluster labels file with the following sample content:

   ```yaml
   domain: production
   project: team1
   value: label2
   ```

8. Update the cluster execution labels for the project:

   ```shell
   $ flytectl update execution-cluster-label --attrFile ecl-production.yaml
   ```

9. Finally, submit a workflow execution that matches the label of the new cluster:

   ```shell
   $ pyflyte run --remote --project team1 --domain production example.py \
         training_workflow --hyperparameters '{"C": 0.1}'
   ```

10. A successful execution should be visible on the UI, confirming it ran in the new cluster:

![](../../_static/images/deployment/multicluster-execution.png)
