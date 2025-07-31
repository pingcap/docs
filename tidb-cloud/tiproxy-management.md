---
title: Manage TiProxy
summary: Learn about how to manage TiProxy.
---

# Manage TiProxy

## Enable TiProxy

You can enable TiProxy for either a new cluster or an existing cluster.

### Decide TiProxy instance size and number

TiProxy size and number depend on both the QPS and network bandwidth of your cluster. Network bandwidth is the sum of the client request and TiDB response bandwidth.

The maximum QPS and network bandwidth of each TiProxy size are listed below.

| size | max QPS | max network bandwidth |
| :-| :-|
| small | 30K | 93 MiB/s |
| large | 120K | 312 MiB/s |

The optional TiProxy instance numbers are 2, 3, 6, 9, 12, 15, 18, 21, and 24. The default two small-sized TiProxy instances can provide 60K QPS and 92 MiB/s network bandwidth. We recommend you to reserve 20% QPS to prevent high latency.

For example, if the cluster's maximum QPS is 100K and the maximum network bandwidth is 100MiB/s, then the size and number of TiProxy instances mainly depend on the QPS. We recommend selecting six small-sized TiProxy instances.

For more details of TiProxy performance, see [TiProxy Performance Test](/tiproxy/tiproxy-performance-test.md).

### Enable TiProxy for a new cluster

To enable TiProxy when creating a new cluster, click the TiProxy toggle and choose the TiProxy size and number.

![Enable TiProxy](/media/tidb-cloud/tiproxy-enable-tiproxy.png)

### Enable TiProxy for an existing cluster

To enable TiProxy for an existing cluster, perform the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project, and then click the name of your target cluster to go to its overview page.
2. In the left navigation pane, click **Monitoring > Nodes**.
3. Click **Modify** in the upper-right corner. The **Modify Cluster** page is displayed.
4. On the **Modify Cluster** page, click the TiProxy toggle and choose the TiProxy size and number.

![Enable TiProxy](/media/tidb-cloud/tiproxy-enable-tiproxy.png)

> **Note**
>
> Enabling TiProxy will make TiDB rolling restart, which causes connections to disconnect. Besides, creating new connections may hang for at most 30 seconds. Make sure you enable TiProxy in the maintenance window.

### Limitations

- The TiDB instance number in the TiDB node group must be at least two
- The TiDB instance size must be at least 4 vCPU
- The TiProxy instance quota of a tenant is 10

## Disable TiProxy

To disable TiProxy, perform the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project, and then click the name of your target cluster to go to its overview page.
2. In the left navigation pane, click **Monitoring > Nodes**.
3. Click **Modify** in the upper-right corner. The **Modify Cluster** page is displayed.
4. On the **Modify Cluster** page, click the TiProxy toggle to disable TiProxy.

![Disable TiProxy](/media/tidb-cloud/tiproxy-disable-tiproxy.png)

> **Note**
>
> Disabling TiProxy will cause connections to disconnect. Besides, creating new connections may hang for at most 10 seconds. Make sure you enable TiProxy in the maintenance window.

## View TiProxy

### View TiProxy topology

To disable TiProxy, perform the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project, and then click the name of your target cluster to go to its overview page.
2. In the left navigation pane, click **Monitoring > Nodes**.
3. In the **Node Map** page, TiProxy topology is displayed in the **TiDB** panel.

![TiProxy Topology](/media/tidb-cloud/tiproxy-topology.png)

### View TiProxy metrics

To view TiProxy metrics, perform the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project, and then click the name of your target cluster to go to its overview page.
2. In the left navigation pane, click **Monitoring > Metrics**.
3. On the **Metrics** page, click **Server** tab and scroll down to TiProxy-related metrics.

The metrics include:

- TiProxy CPU Usage. It indicates the CPU usage statistics of each TiProxy node. The upper limit is 100%. If the maximum CPU usage exceeds 80%, scaling out TiProxy is recommended.
- TiProxy Connections. It indicates the connection number on each TiProxy node.
- TiProxy Throughput. It indicates the transferred bytes per second on each TiProxy node. If the maximum throughput reaches the maximum network bandwidth, scaling out TiProxy is recommended. To learn about the maximum network bandwidth, see [Decide TiProxy instance size and number](#decide-tiproxy-instance-size-and-number).
- TiProxy Sessions Migration Reasons. It indicates the number of session migrations that happened every minute and the reason for them. For example, when TiDB scales in and TiProxy migrates session to other TiDB instances, the reason should be `status`. For more migration reasons, see [TiProxy Monitoring Metrics](/tiproxy/tiproxy-grafana.md#balance).

### View Tiproxy bills

To view TiProxy bills, perform the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com), switch to your target organization using the combo box in the upper-left corner.
2. In the left navigation pane, click **Billing**. On the **Billing** page, the **Bills** tab is displayed by default.
3. In the **Summary by Service** session, TiProxy node cost is displayed under **TiDB Dedicated**, while TiProxy data transfer cost is included in **Data Transfer > Same Region**.

![TiProxy Billing](/media/tidb-cloud/tiproxy-billing.png)

## Modify TiProxy

To scale TiProxy, perform the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project, and then click the name of your target cluster to go to its overview page.
2. In the left navigation pane, click **Monitoring > Nodes**.
3. Click **Modify** in the upper-right corner. The **Modify Cluster** page is displayed.
4. On the **Modify Cluster** page, modify the TiProxy number.

![Modify TiProxy](/media/tidb-cloud/tiproxy-enable-tiproxy.png)

> **Note**
>
> - Modifying TiProxy size is not supported and it's recommended to modify TiProxy number. If you really need to modify TiProxy size, you need to disable TiProxy and enable TiProxy again to choose a different size.
> - Scaling in TiProxy will cause connections to disconnect. Make sure you scale in TiProxy in the maintenance window.

## Manage TiProxy in TiDB node groups

When you have multiple TiDB node groups, each TiDB node group has its dedicated TiProxy group and TiProxy will route to the TiDB instances in the same TiDB node group to isolate computing resources. You can enable, disable, or modify TiProxy in each TiDB node group respectively. However, the TiProxy size in all the TiDB node groups must be the same.
