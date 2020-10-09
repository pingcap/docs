---
title: TiDB Dashboard Metrics Relation Map
summary: Learn TiDB Dashboard metrics relation map.
---

# TiDB Dashboard Metrics Relation Map

TiDB Dashboard metrics relation map is a feature introduced in v4.0.7. With this feature, the monitoring data of each internal process's duration in a TiDB cluster is drawn into relation maps. The aim is to help you quickly learn the time consumption of each process and their relations.

## Access map

Log into TiDB Dashboard, click **Cluster Diagnostics** on the left navigation menu, and you can see the page of generating the metrics relation map.

![Metrics relation map homepage](/media/dashboard/dashboard-metrics-relation-home.png)

After setting **Range Start Time** and **Range Duration**, click the **Generate Metrics Relation** button and you will enter the page of metrics relation map.

## Learn map

The following image is an example of the metrics relation map. This map illustrates the proportion of each monitoring metric's duration to the whole execution duration in a TiDB cluster within 5 minutes after 2020-07-29 16:36:00. The map also illustrates the relations of each monitoring metric.

![Metrics relation map example](/media/dashboard/dashboard-metrics-relation-example.png)

For example, the following monitoring map of the `tidb_execute` node indicates:

+ The total duration of the `tidb_execute` monitoring metric is 19306.46 seconds, which accounts for 89.4% of the total query duration.
+ The duration of `tidb_execute` node itself is 9070.18 seconds, which accounts for 42% of the total query duration.
+ Hover your mouse over the box area and you can see the detailed information of the metric's note, including the total duration, the average duration, and the average P99 duration.

![tidb_execute node example](/media/dashboard/dashboard-metrics-relation-node-example.png)

### Node information

Each box area represents a monitoring metric and provides the following information:

* The name of the monitoring metric
* The total duration of the monitoring metric
* The proportion of the metric's total duration to the total query duration.

*The total duration of the metric node* = *the duration of the metric node itself* + *the duration of its child nodes*. Therefore, the metric map of some nodes displays the proportion of the nodes' duration to the total duration, such as the map of `tidb_execute`.

![tidb_execute node example1](/media/dashboard/dashboard-metrics-relation-node-example1.png)

* `tidb_execute` is the name of the monitoring metric, which represents the execution duration of a SQL query in the TiDB execution engine.
* `19306.46s` represents that total duration of the `tidb_execute` metric is 19306.46 seconds. `89.40%` represents that 19306.46 seconds account for 89.40% of the total time consumed for all SQL queries (including user SQL queries and TiDB's internal SQL queries). The total query duration is the total duration of `tidb_query`.
* `9070.18s` represents that the total execution duration of the `tidb_execute` node itself is 9070.18 seconds, and the rest is the time consumed by its child nodes. `42.00%` represents that 9070.18 seconds account for 42.00% of the total execution duration of all queries.

Hover your mouse over the box area and you can see more details of the `tidb_execute` metric node:

![tidb_execute node example2](/media/dashboard/dashboard-metrics-relation-node-example2.png)

The text information displayed in the image above is the note of the metric node, including the total duration, the total times, the average duration, and the average duration P99, P90, and P80.

### The parent-child relations between nodes

This section takes the example of the `tidb_execute` metric node to introduce the metric's child nodes.

![tidb_execute node relation example1](/media/dashboard/dashboard-metrics-relation-relation-example1.png)

From the map above, you can see the two child nodes of `tidb_execute`:

* `pd_start_tso_wait`: The total duration of waiting for the transaction's `start_tso`, which is 300.66 seconds.
* `tidb_txn_cmd`: The total duration of TiDB executing the relevant commands, which is 9935.62 seconds.

In addition, `tidb_execute` also has a dotted arrow pointing to `tidb_cop` box area, which indicates as follows:

`tidb_execute` includes the duration of the `tidb_cop` metric, but cop requests might be executed concurrently. For example, the `execute` duration of performing `join` queries on two tables is 60 seconds, duration which table scan requests are concurrently executed on the joined two tables. If the execution durations of cop requests are respectively 40 seconds and 30 seconds, the total duration of cop requests are 70 seconds. However, the `execute` duration is only 60 seconds. Therefore, if the duration of a parent node does not completely include the duration of a child node, the dotted arrow is used to point to the child node.

> **Note:**
>
> When a node have a dotted arrow pointing to its child node, the duration of this node itself is inaccurate. For example, in the `tidb_execute` node, the duration of the node itself is 9070.18 seconds (`9070.18 = 19306.46 - 300.66 - 9935.62`). In this equation, the duration of the `tidb_cop` child node is not calculated into the duration of `tidb_execute`'s child nodes. But in fact, this is not true. 9070.18 seconds, the duration of `tidb_execute` itself, includes a part of the `tidb_cop` duration, and the duration of this part cannot be determined.

### `tidb_kv_request` and its parent nodes

![tidb_execute node relation example2](/media/dashboard/dashboard-metrics-relation-relation-example2.png)

`tidb_cop` and `tidb_txn_cmd.get`, the parent nodes of `tidb_kv_request`, both have dotted arrows pointing to `tidb_kv_request`, which indicates as follows:

* The duration of `tidb_cop` includes a part of `tidb_kv_request`'s duration.
* The duration of `tidb_txn_cmd.get` also includes a part of `tidb_kv_request`'s duration.

However, it is impossible to determine how much duration of `tidb_kv_request` is included in `tidb_cop`.

* `tidb_kv_request.Get`: The duration of TiDB sending the `Get` type key-value requests.
* `tidb_kv_request.Cop`: The duration of TiDB sending the `Cop` type key-value requests.

The relation between `tidb_kv_request` and the `tidb_kv_request.Get` and `tidb_kv_request.Cop` nodes that point to it is not the parent-child inclusive type, but the component type. The name prefix of the child node is the name of the parent node plus `.xxx`, which is the child class of the parent node. It is appropriate to understand this case in the following way:

The total duration of TiDB sending key-value requests is 14745.07 seconds, during which the key-value requests for the `Get` and `Cop` types respectively consume 9798.02 seconds and 4946.46 seconds.
