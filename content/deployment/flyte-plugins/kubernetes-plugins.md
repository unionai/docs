---
title: Kubernetes plugins
weight: 1
variants: +flyte -serverless -byoc -selfmanaged
---

# Kubernetes Plugins

This guide will help you configure the Flyte plugins that provision resources on Kubernetes.
The steps are defined in terms of the Helm chart you used to install Flyte.

## Install the Kubernetes operator

Select the integration you need and follow the steps to install the corresponding Kubernetes operator:

{{< dropdown title="PyTorch/TensorFlow/MPI" icon=arrow_forward >}}
{{< markdown >}}

1. Install the [Kubeflow training-operator](https://github.com/kubeflow/training-operator?tab=readme-ov-file#stable-release) (stable release):

```bash

  kubectl apply -k "github.com/kubeflow/training-operator/manifests/overlays/standalone?ref=v1.7.0"
```
**Optional: Using a gang scheduler**

To address potential issues with worker pods of distributed training jobs being scheduled at different times due to resource constraints, you can opt for a gang scheduler. This ensures that all worker pods are scheduled simultaneously, reducing the likelihood of job failures caused by timeout errors.

To enable gang scheduling for the ``training-operator``:

a. Select a second scheduler from
[Kubernetes scheduler plugins with co-scheduling](https://www.kubeflow.org/docs/components/training/user-guides/job-scheduling/#running-jobs-with-gang-scheduling)
or [Apache YuniKorn](https://yunikorn.apache.org/docs/next/user_guide/workloads/run_tf/).

b. Configure a Flyte ``PodTemplate`` to use the gang scheduler for your Tasks:

**K8s scheduler plugins with co-scheduling**

```yaml

template:
  spec:
    schedulerName: "scheduler-plugins-scheduler"
```
**Apache Yunikorn**

```yaml

template:
  metadata:
    annotations:
      yunikorn.apache.org/task-group-name: ""
      yunikorn.apache.org/task-groups: ""
      yunikorn.apache.org/schedulingPolicyParameters: ""
```
You can set the scheduler name in the Pod template passed to the ``@task`` decorator. However, to prevent the two different schedulers from competing for resources, we recommend setting the scheduler name in the pod template in the ``flyte`` namespace which is applied to all tasks. Non distributed training tasks can be scheduled by the
gang scheduler as well.

{{< /markdown >}}
{{< /dropdown >}}

{{< dropdown title="Ray" icon=arrow_forward >}}
{{< markdown >}}

To add the Kuberay Helm repo, run the following command:

```bash

helm repo add kuberay https://ray-project.github.io/kuberay-helm/
```
To install the Kuberay operator, run the following command:

```bash

helm install kuberay-operator kuberay/kuberay-operator --namespace ray-system --version 1.1.0 --create-namespace
```

{{< /markdown >}}
{{< /dropdown >}}

{{< dropdown title="Spark" icon=arrow_forward >}}
{{< markdown >}}

To add the Spark Helm repository, run the following commands:

```bash

helm repo add spark-operator https://kubeflow.github.io/spark-operator
```
    To install the Spark operator, run the following command:

```bash

helm install spark-operator spark-operator/spark-operator --namespace spark-operator --create-namespace
```

{{< /markdown >}}
{{< /dropdown >}}

{{< dropdown title="Dask" icon=arrow_forward >}}
{{< markdown >}}

To add the Dask Helm repository, run the following command:

```bash

helm repo add dask https://helm.dask.org
```
To install the Dask operator, run the following command:

```bash

helm install dask-operator dask/dask-kubernetes-operator --namespace dask-operator --create-namespace
```
{{< /markdown >}}
{{< /dropdown >}}

{{< dropdown title="Volcano-Scheduled PodTask" icon=arrow_forward >}}
{{< markdown >}}

PodTasks in Flyte can be scheduled using the Volcano scheduler, which offers queue-based features such as multi-tenant resource management, task prioritization, and resource preemption. These features enhance scheduling efficiency and improve overall cluster utilization in shared environments.

To enable Volcano-scheduled PodTasks in Flyte, follow these steps:

1. Install Volcano in your cluster by following the [instructions in the volcano repository](https://github.com/volcano-sh/volcano).

2. Configure a Flyte PodTemplate to use the Volcano scheduler for your PodTasks:
  
```yaml

template:
  spec:
    schedulerName: "volcano"
```


{{< /markdown >}}
{{< /dropdown >}}

## Specify plugin configuration

{{< dropdown title="Pytorch" icon=arrow_forward >}}
{{< markdown >}}

### flyte-binary

Create a file named ``values-override.yaml`` and add the following config to it:

```yaml

configuration:
  inline:
    tasks:
      task-plugins:
        enabled-plugins:
          - container
          - sidecar
          - k8s-array
          - pytorch
        default-for-task-types:
          - container: container
          - container_array: k8s-array
          - pytorch: pytorch
```
### flyte-core

Create a file named ``values-override.yaml`` and add the following config to it:

```yaml
configmap:
  enabled_plugins:
    tasks:
      task-plugins:
        enabled-plugins:
          - container
          - sidecar
          - k8s-array
          - pytorch
        default-for-task-types:
          container: container
          sidecar: sidecar
          container_array: k8s-array
          pytorch: pytorch
```
{{< /markdown >}}
{{< /dropdown >}}

{{< dropdown title="Tensorflow" icon=arrow_forward >}}
{{< markdown >}}

### flyte-binary

Create a file named ``values-override.yaml`` and add the following config to it:

```yaml

configuration:
  inline:
    tasks:
      task-plugins:
        enabled-plugins:
          - container
          - sidecar
          - k8s-array
          - tensorflow
        default-for-task-types:
          - container: container
          - container_array: k8s-array
          - tensorflow: tensorflow
```
### flyte-core

Create a file named ``values-override.yaml`` and add the following config to it:

```yaml

configmap:
  enabled_plugins:
    tasks:
      task-plugins:
        enabled-plugins:
          - container
          - sidecar
          - k8s-array
          - tensorflow
        default-for-task-types:
          container: container
          sidecar: sidecar
          container_array: k8s-array
          tensorflow: tensorflow
```
{{< /markdown >}}
{{< /dropdown >}}

{{< dropdown title="MPI" icon=arrow_forward >}}
{{< markdown >}}

### flyte-binary

Create a file named ``values-override.yaml`` and add the following config to it:

```yaml

configuration:
  inline:
    tasks:
      task-plugins:
        enabled-plugins:
          - container
          - sidecar
          - k8s-array
          - mpi
        default-for-task-types:
          - container: container
          - container_array: k8s-array
          - mpi: mpi
```
#### flyte-core

Create a file named ``values-override.yaml`` and add the following config to it:

```yaml

configmap:
  enabled_plugins:
    tasks:
      task-plugins:
        enabled-plugins:
          - container
          - sidecar
          - k8s-array
          - mpi
        default-for-task-types:
          container: container
          sidecar: sidecar
          container_array: k8s-array
          mpi: mpi
```

{{< /markdown >}}
{{< /dropdown >}}

{{< dropdown title="Ray" icon=arrow_forward >}}
{{< markdown >}}

### flyte-binary

Create a file named ``values-override.yaml`` and add the following config to it:

```yaml

configuration:
  inline:
    tasks:
      task-plugins:
        enabled-plugins:
          - container
          - sidecar
          - k8s-array
          - ray
        default-for-task-types:
          - container: container
          - container_array: k8s-array
          - ray: ray
    plugins:
      ray:
      // Shutdown Ray cluster after 1 hour of inactivity
        ttlSecondsAfterFinished: 3600
```
### flyte-core

Create a file named ``values-override.yaml`` and add the following config to it:

```yaml

configmap:
  enabled_plugins:
    tasks:
      task-plugins:
        enabled-plugins:
          - container
          - sidecar
          - k8s-array
          - ray
        default-for-task-types:
          container: container
          sidecar: sidecar
          container_array: k8s-array
          ray: ray
    plugins:
      ray:
        // Shutdown Ray cluster after 1 hour of inactivity
        ttlSecondsAfterFinished: 3600
```
{{< /markdown >}}
{{< /dropdown >}}

{{< dropdown title="Spark" icon=arrow_forward >}}
{{< markdown >}}

## flyte-binary on AWS

Create a file named ``values-override.yaml`` and add the following config to it:

```yaml

configuration:
  inline:
    tasks:
      task-plugins:
        enabled-plugins:
          - container
          - sidecar
          - k8s-array
          - spark
        default-for-task-types:
          - container: container
          - container_array: k8s-array
          - spark: spark
    cluster_resources:
      - production:
        - defaultIamRole:
            value: <FLYTE_IAM_USER_ARN>
      - staging:
        - defaultIamRole:
            value: <FLYTE_IAM_USER_ARN>
      - development:
        - defaultIamRole:
            value: <FLYTE_IAM_USER_ARN>
    plugins:
      spark:
      # Edit the Spark configuration as you see fit
        spark-config-default:
          - spark.driver.cores: "1"
          - spark.hadoop.fs.s3a.aws.credentials.provider: "com.amazonaws.auth.DefaultAWSCredentialsProviderChain"
          - spark.kubernetes.allocation.batch.size: "50"
          - spark.hadoop.fs.s3a.acl.default: "BucketOwnerFullControl"
          - spark.hadoop.fs.s3n.impl: "org.apache.hadoop.fs.s3a.S3AFileSystem"
          - spark.hadoop.fs.AbstractFileSystem.s3n.impl: "org.apache.hadoop.fs.s3a.S3A"
          - spark.hadoop.fs.s3.impl: "org.apache.hadoop.fs.s3a.S3AFileSystem"
          - spark.hadoop.fs.AbstractFileSystem.s3.impl: "org.apache.hadoop.fs.s3a.S3A"
          - spark.hadoop.fs.s3a.impl: "org.apache.hadoop.fs.s3a.S3AFileSystem"
          - spark.hadoop.fs.AbstractFileSystem.s3a.impl: "org.apache.hadoop.fs.s3a.S3A"
          - spark.network.timeout: 600s
          - spark.executorEnv.KUBERNETES_REQUEST_TIMEOUT: 100000
          - spark.executor.heartbeatInterval: 60s
  clusterResourceTemplates:
  inline:
    #This section automates the creation of the project-domain namespaces
    - key: aa_namespace
      value: |
        apiVersion: v1
        kind: Namespace
        metadata:
          name: {{ namespace }}
        spec:
          finalizers:
          - kubernetes
    # This block performs the automated annotation of KSAs across all project-domain namespaces
    - key: ab_service_account
      value: |
        apiVersion: v1
        kind: ServiceAccount
        metadata:
          name: default
          namespace: '{{ namespace }}'
          annotations:
            eks.amazonaws.com/role-arn: '{{ defaultIamRole }}'
    - key: ac_spark_role
      value: |
        apiVersion: rbac.authorization.k8s.io/v1
        kind: Role
        metadata:
          name: spark-role
          namespace: "{{ namespace }}"
        rules:
        - apiGroups: ["*"]
          resources:
          - pods
          verbs:
          - '*'
        - apiGroups: ["*"]
          resources:
          - services
          verbs:
          - '*'
        - apiGroups: ["*"]
          resources:
          - configmaps
          verbs:
          - '*'
        - apiGroups: ["*"]
          resources:
          - persistentvolumeclaims
          verbs:
          - "*"
    - key: ad_spark_service_account
      value: |
        apiVersion: v1
        kind: ServiceAccount
        metadata:
          name: spark
          namespace: "{{ namespace }}"
          annotations:
            eks.amazonaws.com/role-arn: '{{ defaultIamRole }}'
    - key: ae_spark_role_binding
      value: |
        apiVersion: rbac.authorization.k8s.io/v1
        kind: RoleBinding
        metadata:
          name: spark-role-binding
          namespace: "{{ namespace }}"
        roleRef:
          apiGroup: rbac.authorization.k8s.io
          kind: Role
          name: spark-role
        subjects:
          - kind: ServiceAccount
            name: spark
            namespace: "{{ namespace }}"
```
2. (Optional) The Spark operator supports Kubernetes ResourceQuota enforcement. If you plan to use it, set [per-Task resource requests](https://docs.flyte.org/en/latest/user_guide/productionizing/customizing_task_resources.html#customizing-task-resources)that fit into the quota for each project-namespace. A Task without resource requests or limits will be rejected by the K8s scheduler as described [in the Kubernetes docs](https://kubernetes.io/docs/concepts/policy/resource-quotas/).
The following is a sample configuration you can add to your Helm chart values, adjusting the resources to match your needs:

```yaml

customData:
  - production:
      - projectQuotaCpu:
          value: "5"
      - projectQuotaMemory:
          value: "4000Mi"
  - staging:
      - projectQuotaCpu:
          value: "2"
      - projectQuotaMemory:
          value: "3000Mi"
  - development:
      - projectQuotaCpu:
          value: "4"
      - projectQuotaMemory:
          value: "3000Mi"
```
Plus an additional Cluster Resource template to automate the creation of the ``ResourceQuota``:

```yaml

templates:
  - key: ab_project_resource_quota
    value: |
      apiVersion: v1
      kind: ResourceQuota
      metadata:
        name: project-quota
        namespace: {{ namespace }}
      spec:
        hard:
          limits.cpu: {{ projectQuotaCpu }}
          limits.memory: {{ projectQuotaMemory }}
```
## flyte-binary on GCP

> Check out the [reference implementation for GCP](https://github.com/unionai-oss/deploy-flyte/blob/main/environments/gcp/flyte-core/README.md)for information on how all the Flyte prerequisites are configured.

Create a file named ``values-override.yaml`` and add the following config to it:

```yaml

configuration:
  inline:
    tasks:
      task-plugins:
        enabled-plugins:
          - container
          - sidecar
          - k8s-array
          - spark
        default-for-task-types:
          - container: container
          - container_array: k8s-array
          - spark: spark
    cluster_resources:
      - production:
        - gsa:
            value: <GoogleServiceAccount-EMAIL>
      - staging:
        - gsa:
            value: <GoogleServiceAccount-EMAIL>
      - development:
        - gsa:
            value: <GoogleServiceAccount-EMAIL>
    plugins:
      spark:
      # Edit the Spark configuration as you see fit
        spark-config-default:
          - spark.eventLog.enabled: "true"
          - spark.eventLog.dir: "{{ .Values.userSettings.bucketName }}/spark-events"
          - spark.driver.cores: "1"
          - spark.executorEnv.HTTP2_DISABLE: "true"
          - spark.hadoop.fs.AbstractFileSystem.gs.impl: com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS
          - spark.kubernetes.allocation.batch.size: "50"
          - spark.kubernetes.driverEnv.HTTP2_DISABLE: "true"
          - spark.network.timeout: 600s
          - spark.executorEnv.KUBERNETES_REQUEST_TIMEOUT: 100000
          - spark.executor.heartbeatInterval: 60s

clusterResourceTemplates:
  inline:
    #This section automates the creation of the project-domain namespaces
    - key: aa_namespace
      value: |
        apiVersion: v1
        kind: Namespace
        metadata:
          name: {{ namespace }}
        spec:
          finalizers:
          - kubernetes
    # This block performs the automated annotation of KSAs across all project-domain namespaces
    - key: ab_service_account
      value: |
        apiVersion: v1
        kind: ServiceAccount
        metadata:
          name: default
          namespace: '{{ namespace }}'
          annotations:
            iam.gke.io/gcp-service-account: {{ gsa }}
    - key: ac_spark_role
      value: |
        apiVersion: rbac.authorization.k8s.io/v1
        kind: Role
        metadata:
          name: spark-role
          namespace: "{{ namespace }}"
        rules:
        - apiGroups: ["*"]
          resources:
          - pods
          verbs:
          - '*'
        - apiGroups: ["*"]
          resources:
          - services
          verbs:
          - '*'
        - apiGroups: ["*"]
          resources:
          - configmaps
          verbs:
          - '*'
        - apiGroups: ["*"]
          resources:
          - persistentvolumeclaims
          verbs:
          - "*"
    - key: ad_spark_service_account
      value: |
        apiVersion: v1
        kind: ServiceAccount
        metadata:
          name: spark
          namespace: "{{ namespace }}"
          annotations:
            iam.gke.io/gcp-service-account: {{ gsa }}
    - key: ae_spark_role_binding
      value: |
        apiVersion: rbac.authorization.k8s.io/v1
        kind: RoleBinding
        metadata:
          name: spark-role-binding
          namespace: "{{ namespace }}"
        roleRef:
          apiGroup: rbac.authorization.k8s.io
          kind: Role
          name: spark-role
        subjects:
          - kind: ServiceAccount
            name: spark
            namespace: "{{ namespace }}"
```

## flyte-core on AWS

Create a file named ``values-override.yaml`` and add the following config to it:

```yaml

configmap:
  enabled_plugins:
    tasks:
      task-plugins:
        enabled-plugins:
          - container
          - sidecar
          - k8s-array
          - spark
        default-for-task-types:
          container: container
          sidecar: sidecar
          container_array: k8s-array
          spark: spark
cluster_resource_manager:
  enabled: true
  standalone_deploy: false
  # -- Resource templates that should be applied
  templates:
    # -- Template for namespaces resources
    - key: aa_namespace
      value: |
        apiVersion: v1
        kind: Namespace
        metadata:
          name: {{ namespace }}
        spec:
          finalizers:
          - kubernetes
    - key: ac_spark_role
      value: |
        apiVersion: rbac.authorization.k8s.io/v1beta1
        kind: Role
        metadata:
          name: spark-role
          namespace: {{ namespace }}
        rules:
        - apiGroups: ["*"]
          resources:
          - pods
          verbs:
          - '*'
        - apiGroups: ["*"]
          resources:
          - services
          verbs:
          - '*'
        - apiGroups: ["*"]
          resources:
          - configmaps
          verbs:
          - '*'
        - apiGroups: ["*"]
          resources:
          - persistentvolumeclaims
          verbs:
          - "*"

    - key: ad_spark_service_account
      value: |
        apiVersion: v1
        kind: ServiceAccount
        metadata:
          name: spark
          namespace: {{ namespace }}

    - key: ae_spark_role_binding
      value: |
        apiVersion: rbac.authorization.k8s.io/v1beta1
        kind: RoleBinding
        metadata:
          name: spark-role-binding
          namespace: {{ namespace }}
        roleRef:
          apiGroup: rbac.authorization.k8s.io
          kind: Role
          name: spark-role
        subjects:
        - kind: ServiceAccount
          name: spark
          namespace: {{ namespace }}

sparkoperator:
  enabled: true
  plugin_config:
    plugins:
      spark:
        # Edit the Spark configuration as you see fit
        spark-config-default:
          - spark.driver.cores: "1"
          - spark.hadoop.fs.s3a.aws.credentials.provider: "com.amazonaws.auth.DefaultAWSCredentialsProviderChain"
          - spark.kubernetes.allocation.batch.size: "50"
          - spark.hadoop.fs.s3a.acl.default: "BucketOwnerFullControl"
          - spark.hadoop.fs.s3n.impl: "org.apache.hadoop.fs.s3a.S3AFileSystem"
          - spark.hadoop.fs.AbstractFileSystem.s3n.impl: "org.apache.hadoop.fs.s3a.S3A"
          - spark.hadoop.fs.s3.impl: "org.apache.hadoop.fs.s3a.S3AFileSystem"
          - spark.hadoop.fs.AbstractFileSystem.s3.impl: "org.apache.hadoop.fs.s3a.S3A"
          - spark.hadoop.fs.s3a.impl: "org.apache.hadoop.fs.s3a.S3AFileSystem"
          - spark.hadoop.fs.AbstractFileSystem.s3a.impl: "org.apache.hadoop.fs.s3a.S3A"
          - spark.network.timeout: 600s
          - spark.executorEnv.KUBERNETES_REQUEST_TIMEOUT: 100000
          - spark.executor.heartbeatInterval: 60s
```
## flyte-core on GCP

>  Check out the [reference implementation for GCP](https://github.com/unionai-oss/deploy-flyte/blob/main/environments/gcp/flyte-core/README.md) for guidance on how all the Flyte prerequisites are configured.

Create a file named ``values-override.yaml`` and add the following config to it:

```yaml

enabled_plugins:
  tasks:
    task-plugins:
      enabled-plugins:
        - container
        - sidecar
        - k8s-array
        - spark
      default-for-task-types:
        container: container
        sidecar: sidecar
        container_array: k8s-array
        spark: spark
cluster_resource_manager:
  enabled: true
  standalone_deploy: false
  config:
    cluster_resources:
      customData:
      - production:
          - gsa:
          #This is the GSA that the Task Pods will use to access GCP resources.
              value: "<GoogleServiceAccount-email>"
      - staging:
          - gsa:
              value: "<GoogleServiceAccount-email>"
      - development:
          - gsa:
              value: "<GoogleServiceAccount-email>"
  templates:
    # -- Template for namespaces resources
    - key: aa_namespace
      value: |
        apiVersion: v1
        kind: Namespace
        metadata:
          name: {{ namespace }}
        spec:
          finalizers:
          - kubernetes
    # -- Patch default service account
    - key: aab_default_service_account
      value: |
        apiVersion: v1
        kind: ServiceAccount
        metadata:
          name: default
          namespace: {{ namespace }}
          annotations:
            # Annotation needed for GCP Workload Identity to function
            # https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity
            iam.gke.io/gcp-service-account: {{ gsa }}
    - key: ac_spark_role
      value: |
        apiVersion: rbac.authorization.k8s.io/v1
        kind: Role
        metadata:
          name: spark-role
          namespace: "{{ namespace }}"
        rules:
        - apiGroups: ["*"]
          resources:
          - pods
          verbs:
          - '*'
        - apiGroups: ["*"]
          resources:
          - services
          verbs:
          - '*'
        - apiGroups: ["*"]
          resources:
          - configmaps
          verbs:
          - '*'
        - apiGroups: ["*"]
          resources:
          - persistentvolumeclaims
          verbs:
          - "*"
    #While the Spark Helm chart creates a spark ServiceAccount, this template creates one
    # on each project-domain namespace and annotates it with the GSA
    #You should always run workflows with the Spark service account (eg pyflyte run --remote --service-account=spark ...)
    - key: ad_spark_service_account
      value: |
        apiVersion: v1
        kind: ServiceAccount
        metadata:
          name: spark
          namespace: "{{ namespace }}"
          annotations:
            iam.gke.io/gcp-service-account: {{ gsa }}
    - key: ae_spark_role_binding
      value: |
        apiVersion: rbac.authorization.k8s.io/v1
        kind: RoleBinding
        metadata:
          name: spark-role-binding
          namespace: "{{ namespace }}"
        roleRef:
          apiGroup: rbac.authorization.k8s.io
          kind: Role
          name: spark-role
        subjects:
          - kind: ServiceAccount
            name: spark
            namespace: "{{ namespace }}"
sparkoperator:
enabled: true
plugins:
  spark:
    spark-config-default:
      - spark.eventLog.enabled: "true"
      - spark.eventLog.dir: "{{ .Values.userSettings.bucketName }}/spark-events"
      - spark.driver.cores: "1"
      - spark.executorEnv.HTTP2_DISABLE: "true"
      - spark.hadoop.fs.AbstractFileSystem.gs.impl: com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS
      - spark.kubernetes.allocation.batch.size: "50"
      - spark.kubernetes.driverEnv.HTTP2_DISABLE: "true"
      - spark.network.timeout: 600s
      - spark.executorEnv.KUBERNETES_REQUEST_TIMEOUT: 100000
      - spark.executor.heartbeatInterval: 60s
```
## flyte-sandbox

If you installed the [flyte-sandbox](https://github.com/flyteorg/flyte/tree/master/charts/flyte-sandbox) Helm chart to a K8s cluster, follow this section to configure the Spark plugin.
Note that none of this configuration applies to the demo cluster that you spin up with ``flytectl demo start``.

1. Create a file named ``values-override.yaml`` and add the following config to it:

> Within the flyte-binary block, the value of ``inline.storage.signedURL.stowConfigOverride.endpoint`` should be set to the corresponding node Hostname/IP on the MinIO pod if you are deploying on a Kubernetes cluster.

```yaml

flyte-binary:
  nameOverride: flyte-sandbox
  enabled: true
  configuration:
    database:
      host: '{{ printf "%s-postgresql" .Release.Name | trunc 63 | trimSuffix "-" }}'
      password: postgres
    storage:
      metadataContainer: my-s3-bucket
      userDataContainer: my-s3-bucket
      provider: s3
      providerConfig:
        s3:
          disableSSL: true
          v2Signing: true
          endpoint: http://{{ printf "%s-minio" .Release.Name | trunc 63 | trimSuffix "-" }}.{{ .Release.Namespace }}:9000
          authType: accesskey
          accessKey: minio
          secretKey: miniostorage
    logging:
      level: 5
      plugins:
        kubernetes:
          enabled: true
          templateUri: |-
            http://localhost:30080/kubernetes-dashboard/#/log/{{.namespace }}/{{ .podName }}/pod?namespace={{ .namespace }}
    inline:
      task_resources:
        defaults:
          cpu: 500m
          ephemeralStorage: 0
          gpu: 0
          memory: 1Gi
        limits:
          cpu: 0
          ephemeralStorage: 0
          gpu: 0
          memory: 0
      storage:
        signedURL:
          stowConfigOverride:
            endpoint: http://localhost:30002
      plugins:
        k8s:
          default-env-vars:
            - FLYTE_AWS_ENDPOINT: http://{{ printf "%s-minio" .Release.Name | trunc 63 | trimSuffix "-" }}.{{ .Release.Namespace }}:9000
            - FLYTE_AWS_ACCESS_KEY_ID: minio
            - FLYTE_AWS_SECRET_ACCESS_KEY: miniostorage
        spark:
          spark-config-default:
            - spark.driver.cores: "1"
            - spark.hadoop.fs.s3a.aws.credentials.provider: "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider"
            - spark.hadoop.fs.s3a.endpoint: http://{{ printf "%s-minio" .Release.Name | trunc 63 | trimSuffix "-" }}.{{ .Release.Namespace }}:9000
            - spark.hadoop.fs.s3a.access.key: "minio"
            - spark.hadoop.fs.s3a.secret.key: "miniostorage"
            - spark.hadoop.fs.s3a.path.style.access: "true"
            - spark.kubernetes.allocation.batch.size: "50"
            - spark.hadoop.fs.s3a.acl.default: "BucketOwnerFullControl"
            - spark.hadoop.fs.s3n.impl: "org.apache.hadoop.fs.s3a.S3AFileSystem"
            - spark.hadoop.fs.AbstractFileSystem.s3n.impl: "org.apache.hadoop.fs.s3a.S3A"
            - spark.hadoop.fs.s3.impl: "org.apache.hadoop.fs.s3a.S3AFileSystem"
            - spark.hadoop.fs.AbstractFileSystem.s3.impl: "org.apache.hadoop.fs.s3a.S3A"
            - spark.hadoop.fs.s3a.impl: "org.apache.hadoop.fs.s3a.S3AFileSystem"
            - spark.hadoop.fs.AbstractFileSystem.s3a.impl: "org.apache.hadoop.fs.s3a.S3A"
    inlineConfigMap: '{{ include "flyte-sandbox.configuration.inlineConfigMap" . }}'
  clusterResourceTemplates:
    inlineConfigMap: '{{ include "flyte-sandbox.clusterResourceTemplates.inlineConfigMap" . }}'
  deployment:
    image:
      repository: flyte-binary
      tag: sandbox
      pullPolicy: Never
    waitForDB:
      image:
        repository: bitnami/postgresql
        tag: sandbox
        pullPolicy: Never
  rbac:
    # This is strictly NOT RECOMMENDED in production clusters, and is only for use
    # within local Flyte sandboxes.
    # When using cluster resource templates to create additional namespaced roles,
    # Flyte is required to have a superset of those permissions. To simplify
    # experimenting with new backend plugins that require additional roles be created
    # with cluster resource templates (e.g. Spark), we add the following:
    extraRules:
      - apiGroups:
        - '*'
        resources:
        - '*'
        verbs:
        - '*'
  enabled_plugins:
    tasks:
      task-plugins:
        enabled-plugins:
          - container
          - sidecar
          - k8s-array
          - connector-service
          - spark
        default-for-task-types:
          container: container
          sidecar: sidecar
          container_array: k8s-array
          spark: spark
```
{{< /markdown >}}
{{< /dropdown >}}


{{< dropdown title="Dask" icon=arrow_forward >}}
{{< markdown >}}

## flyte-binary

Create a file named ``values-override.yaml`` and add the following config to it:

```yaml

tasks:
task-plugins:
  enabled-plugins:
    - container
    - sidecar
    - dask
  default-for-task-types:
    - container: container
    - dask: dask
```
## flyte-core

Create a file named ``values-override.yaml`` and add the following config to it:

```yaml

configmap:
  enabled_plugins:
    tasks:
      task-plugins:
        enabled-plugins:
          - container
          - sidecar
          - k8s-array
          - dask
        default-for-task-types:
          container: container
          sidecar: sidecar
          container_array: k8s-array
          dask: dask
```
{{< /markdown >}}
{{< /dropdown >}}


{{< dropdown title="Volcano-Scheduled PodTask" icon=arrow_forward >}}
{{< markdown >}}

### flyte-binary

Create a file named ``values-override.yaml`` and add the following config to it:

```yaml

configuration:
  inline:
    plugins:
      k8s:
        enable-create-pod-group-for-pod: true
```
### flyte-core

Create a file named ``values-override.yaml`` and add the following config to it:

```yaml

configmap:
  k8s:
    plugins:
      k8s:
        enable-create-pod-group-for-pod: true
```

{{< /markdown >}}
{{< /dropdown >}}

## Upgrade the deployment

```bash
helm upgrade <RELEASE_NAME> flyteorg/<HELM_CHART> -n <YOUR_NAMESPACE> --values values-override.yaml

```

Replace ``<RELEASE_NAME>`` with the name of your release (e.g., ``flyte-backend``),
``<YOUR_NAMESPACE>`` with the name of your namespace (e.g., ``flyte``) and `<HELM_CHART>` with `flyte-binary`, `flyte-core ` or `flyte-sandbox`.


Wait for the upgrade to complete. You can check the status of the deployment pods by running the following command:

```bash
kubectl get pods -n flyte
```

Once all the components are up and running, go to the examples section to learn more about how to use Flyte backend plugins.
