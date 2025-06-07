---
title: Viewing logs
weight: 6
variants: +flyte +serverless +byoc +selfmanaged
---

# Viewing logs

In the [Execution view](../workflows/viewing-workflow-executions), selecting a task from the list in the **Nodes** tab will open the task details in the right panel.

{{< variant flyte >}}

{{< markdown >}}

Within that panel, in the **Execution** tab,  you will find the stack trace associated with that node:

![Task logs link](/_static/images/user-guide/core-concepts/tasks/viewing-logs/viewing_logs_flyte.png)

Also, if you configure the Kubernetes dashboard, the Flyte console will display a link to the specific Pod logs.

{{< /markdown >}}
{{< /variant >}}

{{< variant byoc serverless >}}

{{< markdown >}}

Within that panel, in the **Execution** tab, under **Logs**, you will find a link labeled **Task Logs**.

![Task logs link](../../../_static/images/user-guide/core-concepts/tasks/viewing-logs/task-logs-link.png)

This leads to the **Execution logs tab** of the **Execution details page**:

![Execution logs](../../../_static/images/user-guide/core-concepts/tasks/viewing-logs/execution-logs.png)

The execution logs provide a live view into the standard output of the task execution.

For example, any `print` statements in the tasks Python code will be displayed here.

## Kubernetes cluster logs

On the left side of the page you can also see the Kubernetes cluster logs for the task execution:

![Kubernetes cluster logs](../../../_static/images/user-guide/core-concepts/tasks/viewing-logs/k8s-cluster-logs.png)

## Other tabs

Alongside the **Execution logs** tab in the **Execution details page**, you will also find the **Execution resources** and **Inputs & Outputs** tabs.

{{< /markdown >}}
{{< /variant >}}

## Cloud provider logs

In addition to the **Task Logs** link, you will also see a link to your cloud provider's logs (**Cloudwatch Logs** for AWS, **Stackdriver Logs** for GCP, and **Azure Logs** for Azure):

{{< variant byoc selfmanaged flyte >}}

{{< markdown >}}

![Cloud provider logs link](../../../_static/images/user-guide/core-concepts/tasks/viewing-logs/cloud-provider-logs-link.png)

Assuming you are logged into your cloud provider account with the appropriate permissions, this link will take you to the logs specific to the container in which this particular task execution is running.

{{< /markdown >}}
{{< /variant >}}