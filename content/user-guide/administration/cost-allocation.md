---
title: Cost allocation
weight: 2
variants: -flyte -serverless +byoc +selfmanaged
---

# Cost allocation

Cost allocation allows you to track costs and resource utilization for your task and workflow executions.

It provides the following breakdowns by project, domain, workflow/task name, and execution ID:

* **Total Cost**: An estimate of the total cost. Total cost is composed of estimated costs of each container's allocated memory, CPU, and GPU, plus that container's proportion of unused compute resources on nodes it occupies.
* **Allocated Memory**: The aggregate allocated memory (gigabyte-hours) across all containers in the selection. Allocated memory is calculated as max(requested memory, used memory).
* **Memory Utilization**: The aggregate used memory divided by the aggregate allocated memory across all containers in the selection.
* **Allocated CPU**: The aggregate allocated CPU (core-hours) across all containers in the selection. Allocated memory is calculated as max(requested CPU, used CPU).
* **CPU Utilization**: The aggregate used CPU divided by the aggregate allocated CPU across all containers in the selection.
* **Allocated GPU**: The aggregate allocated GPU (GPU-hours) across all containers in the selection (allocated GPU equals requested GPU).
* **GPU SM Occupancy**: The weighted average SM occupancy (a measure of GPU usage efficiency) across all GPU containers in the selection.

Additionally, it provides a stacked bar chart of the cost over time grouped by workflow/task name.
The height of each bar is the sum of costs across each 15-minute interval.

## Suggested Usage

Cost allocation is designed to show where costs are being incurred and to highlight opportunities for cost reduction through right-sizing resource requests. All tables are sorted in descending order of total cost, so users can scan across the rows to quickly identify expensive workloads with low memory, CPU, or GPU utilization. Steps can then be taken to reduce the resource requests for particular workflows. {{< key product_name >}}'s task-level monitoring functionality can be used to view granular resource usage for individual tasks, making this exercise straightforward.

## Accessing Cost Data

Cost data is accessed by selecting the **Cost** button in the top right of the {{< key product_name >}} interface:

![Cost link](../../_static/images/user-guide/administration/cost-allocation/cost-link.png)

The **Cost** view displays three top level tabs: **Workload Costs**, **Compute Costs**, and **Invoices**.

### Workload Costs

This tab provides a detailed breakdown of workflow/task costs and resource utilization, allowing you to filter by project, domain, workflow/task name, and execution ID.
It offers views showing total cost, allocated memory, memory utilization, allocated CPU, CPU utilization, allocated GPU, and average GPU SM occupancy.
Additionally, the time series shows total cost per Workflow/Task in a stacked bar format with 15-minute bars.

![Workload costs 1](../../_static/images/user-guide/administration/cost-allocation/workload-costs-1.png)

![Workload costs 2](../../_static/images/user-guide/administration/cost-allocation/workload-costs-2.png)

### Compute Costs

This tab provides a summary of the cluster's overall compute costs.
It includes information on total cost of worker nodes, total uptime by node type, and total cost by node type.

![Compute costs](../../_static/images/user-guide/administration/cost-allocation/compute-costs.png)

### Invoices

This tab displays the total cost of running workflows and tasks in your {{< key product_name >}} installation broken out by invoice.

![Invoices](../../_static/images/user-guide/administration/cost-allocation/invoices.png)

## Data collection and cost calculation

The system collects container-level usage metrics, such as resource allocation and usage, node scaling information, and compute node pricing data from each cloud provider.
These metrics are then processed to calculate the cost of each workflow execution and individual task.

## Total cost calculation

 The total cost per workflow or task execution is the sum of allocated cost and overhead cost:

  * **Allocated Cost**: Cost directly attributable to your workflow's resource usage (memory, CPU, and GPU).
    This is calculated based on the resources requested or consumed (whichever is higher) by the containers running your workloads.

  * **Overhead Cost**: Cost associated with the underlying cluster infrastructure that cannot be directly allocated to specific workflows or tasks.
    This is calculated by proportionally, assigning a share of the unallocated node costs to each entity based on its consumption of allocated resources.

## Allocated cost calculation

The cost of CPU, memory, and GPU resources is calculated using the following approach:

* **Resource consumption**: For CPU and Memory, the system determines the maximum of requested and used resources for each container.
GPU consumption is determined by a container’s allocated GPU resources.
Resource consumption is measured every 15 seconds.

* **Node-level cost**: Hourly costs for CPU, memory, and GPU are calculated using a statistical model based on a regression of node types on their resource specs.
These hourly costs are converted to a 15-second cost for consistency with the data collection interval.
For node costs, the total hourly cost of each node type is used.

* **Allocation to Entities**: The resource costs from each container are then allocated to the corresponding workflow or task execution.

## Overhead Cost Calculation

Overhead costs represent the portion of the cluster's infrastructure cost not directly attributable to individual workflows or tasks.
These costs are proportionally allocated to workflows/tasks and applications based on their use of allocated resources. Specifically:

* The total allocated cost per node is calculated by summing the allocated costs (memory, CPU, and GPU) for all entities running on that node.

* The overhead cost per node is the difference between the total node cost and the total allocated cost on that node.

* The overhead cost is then proportionally allocated to each entity running on that node according to its share of the total allocated cost on that node.

## Limitations

The system currently assumes that all nodes in the cluster are using on-demand pricing.
Therefore, cost will be overestimated for spot and reserved instances, as well as special pricing arrangements with cloud providers.

Overhead cost allocation is an approximation and might not perfectly reflect the true distribution of overhead costs.
In particular, overhead costs are only evaluated within the scope of a single 15-second scrape interval.
This means that the system can still fail to allocate costs to nodes which are left running after a given execution completes.

{{< key product_name >}} services and fees such as platform fees are not reflected in the dashboards.
Cost is scoped to nodes that have been used in running executions.
The accuracy of cost allocation depends on the accuracy of the underlying resource metrics as well as per-node pricing information.

This feature limits lookback to 60 days and allows picking any time range within the past 60 days to assess cost.

## Future Enhancements

Future enhancements may include:

* Longer lookback period (i.e. 90 days)
* Customizable pricing per node type
* Data export
* Per-task cost allocation granularity

If you have an idea for what you and your business would like to see, please reach out to the {{< key product_name >}} team.
