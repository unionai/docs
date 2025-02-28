# Cost allocation

The Cost allocation feature allows you to track and analyze the cost of your Union workflows and individual tasks.
It provides cost breakdowns categorized by:

* **Total Cost**: An estimate of the total cost per workflow or task execution, accounting for both allocated cost and overhead cost:

  * **Allocated Cost**: Cost directly attributable to your workflow's resource usage (CPU, memory, and GPU).
    This is calculated based on the resources requested or consumed (whichever is higher) by the containers running your workloads.

  * **Overhead Cost**: Cost associated with the underlying cluster infrastructure that cannot be directly allocated to specific workflows or tasks.
    This is calculated by proportionally assigning a share of the unallocated node costs to each entity based on its consumption of allocated resources.

## Data collection and cost calculation

The system collects usage metrics, such as container resource consumption, node scaling information, and cloud resource pricing data.
These metrics are then processed to calculate the cost of each workflow execution and individual task.

## Resource cost calculation

The cost of CPU, memory, and GPU resources is calculated using the following approach:

* **Resource consumption**: For CPU and Memory, the system determines the maximum of requested and used resources for each pod.
  GPU consumption is determined by a pod’s allocated GPU resources.
  Resource consumption is measured every 15 seconds.

* **Node-level cost**: Hourly costs for CPU, memory, and GPU are calculated using a statistical model based on a regression of node types on their resource specs.
  These hourly costs are converted to a 15-second cost for consistency with the data collection interval.
  For node costs, the total hourly cost of each node type is used.

* **Allocation to Entities**: The resource costs from each pod are then allocated to the corresponding workflow or task using labeled metrics that link pods to the relevant entity.

## Overhead Cost Calculation:

Overhead costs represent the portion of the cluster's infrastructure cost not directly attributable to individual workflows or tasks.
These costs are proportionally allocated to workflows/tasks and applications based on their use of allocated resources. Specifically:

* The total allocated cost per node is calculated by summing the allocated costs (memory, CPU, and GPU) for all entities running on that node.

* The overhead cost per node is the difference between the total node cost and the total allocated cost on that node.

* The overhead cost is then proportionally allocated to each entity running on that node according to its share of the total allocated cost on that node.

## Accessing Cost Data

Cost data is accessed by selecting the **Cost** button in the top right of the Union interface:

![Cost link](/_static/images/user-guide/administration/cost-allocation/cost-link.png)

The **Cost** view displays three top level tabs: **Workload Costs**, **Compute Costs**, and **Invoices**.

### Workload Costs

This tab provides a detailed breakdown of workflow and task costs, allowing you to filter by domain, project, workflow name, and execution ID.
It offers views showing total cost, memory cost, CPU cost, GPU cost, and overhead cost.
Bar charts visualize costs by domain, project, workflow/task and task execution; tables summarize cost by domain and resource type, project and resource type, workflow/task and resource type, and workflow/task execution and resource type.

![Workload costs 1](/_static/images/user-guide/administration/cost-allocation/workload-costs-1.png)

![Workload costs 2](/_static/images/user-guide/administration/cost-allocation/workload-costs-2.png)

### Compute Costs

This tab provides a summary of the cluster's overall compute costs.
It includes information on total cost of worker nodes, total uptime by node type, and total cost by node type.

![Compute costs](/_static/images/user-guide/administration/cost-allocation/compute-costs.png)

### Invoices

This tab displays the total cost of running workflows and tasks in your Union installation broken out by invoice.

![Invoices](/_static/images/user-guide/administration/cost-allocation/invoices.png)

## Limitations

The system currently assumes that all nodes in the cluster are using on-demand pricing.
Therefore, cost will be overestimated for spot and reserved instances, as well as special pricing arrangements with cloud providers.

Overhead cost allocation is an approximation and might not perfectly reflect the true distribution of overhead costs.
In particular, overhead costs are only evaluated within the scope of a single 15-second scrape interval.
This means that the system can still fail to allocate costs to nodes which are left running after a given execution completes.

Union services and fees such as platform fees are not reflected in the dashboards.
Cost is scoped to nodes that have been used in running executions.
The accuracy of cost allocation depends on the accuracy of the underlying Kubernetes and cost metrics.

This feature limits lookback to 3 days and allows picking any time range within the past 3 days to assess cost.

## Future Enhancements

Future enhancements may include:

* Customizable pricing per node type
* Data export
* Support for additional resource types (such as App Serving, Workspaces, and Actors)
* Enhanced visualization and reporting capabilities
* Cost optimization suggestions
* Longer lookback horizon

If you have an idea for what you and your business would like to see, reach out to your Union representative via Slack.
