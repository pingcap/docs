---
title: Manage TiProxy
summary: Learn about how to manage TiProxy.
---

# Manage TiProxy

## Enable TiProxy

You can enable TiProxy for either a new cluster or an existing cluster in any TiDB node group.

### Decide TiProxy instance size and number

TiProxy size and number depend on both the QPS and network bandwidth of your cluster. Network bandwidth is the sum of the client request and TiDB response bandwidth.

The maximum QPS and network bandwidth of each TiProxy size are listed below.

| size | max QPS | max network bandwidth |
| :-| :-|
| small | 30K | 93 MiB/s |
| large | 120K | 312 MiB/s |

The optional TiProxy sizes are `small` and `large`. The optional TiProxy instance numbers are 2, 3, 6, 9, 12, 15, 18, 21, and 24. The default two small-sized TiProxy instances can provide 60K QPS and 186 MiB/s network bandwidth. It is recommended that you reserve 20% of the QPS to prevent high latency.

For example, if your cluster's maximum QPS is 100K and the maximum network bandwidth is 100 MiB/s, the size and number of TiProxy instances mainly depend on the QPS. In this case, you can select six small-sized TiProxy instances.

### Enable TiProxy for a new cluster

To enable TiProxy when creating a new cluster, click the TiProxy toggle and choose the TiProxy size and number.

![Enable TiProxy](/media/tidb-cloud/tiproxy-enable-tiproxy.png)

### Enable TiProxy for an existing cluster

To enable TiProxy for an existing cluster, perform the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project, and then click the name of your target cluster to go to its overview page.
2. Click **...** in the upper-right corner, and click **Modify** in the drop-down menu. The **Modify Cluster** page is displayed.
3. On the **Modify Cluster** page, click the TiProxy toggle and choose the TiProxy size and number.

![Enable TiProxy](/media/tidb-cloud/tiproxy-enable-tiproxy.png)

> **Note**
>
> Enabling TiProxy will cause a rolling restart of TiDB in this TiDB node group, which causes connections to disconnect. In addition, creating new connections might hang for up to 30 seconds. Make sure that you enable TiProxy in the maintenance window.

### Limitations and quotas

- The TiDB instance number in a TiDB node group must be at least two
- The TiDB instance size must be at least 4 vCPU
- The default maximum TiProxy instance number of an organization is 10, see [Limitations and Quotas](/tidb-cloud/limitations-and-quotas.md)
- The TiDB cluster version should be v6.5.0 or higher

## Disable TiProxy

To disable TiProxy, perform the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project, and then click the name of your target cluster to go to its overview page.
2. Click **...** in the upper-right corner, and click **Modify** in the drop-down menu. The **Modify Cluster** page is displayed.
4. On the **Modify Cluster** page, click the TiProxy toggle to disable TiProxy.

![Disable TiProxy](/media/tidb-cloud/tiproxy-disable-tiproxy.png)

> **Note**
>
> Disabling TiProxy will cause connections to disconnect. In addition, creating new connections might hang for up to 10 seconds. Make sure that you disable TiProxy in the maintenance window.

## View TiProxy

### View TiProxy topology

To view the TiProxy topology, perform the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project, and then click the name of your target cluster to go to its overview page.
2. In the left navigation pane, click **Monitoring > Nodes**. The **Node Map** page is displayed.
3. In the **Node Map** page, TiProxy topology is displayed in the **TiDB** panel.

![TiProxy Topology](/media/tidb-cloud/tiproxy-topology.png)

### View TiProxy metrics

To view TiProxy metrics, perform the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project, and then click the name of your target cluster to go to its overview page.
2. In the left navigation pane, click **Monitoring > Metrics**. The **Metrics** page is displayed.
3. On the **Metrics** page, click **Server** tab and scroll down to TiProxy-related metrics. To view TiProxy metrics in one TiDB node group, click **TiDB Node Group View** tab, select your TiDB node group, and scroll down to TiProxy-related metrics.

The metrics include:

- TiProxy CPU Usage: The CPU usage statistics of each TiProxy node. The upper limit is 100%. If the maximum CPU usage exceeds 80%, it is recommended that you scale out TiProxy.
- TiProxy Connections: The connection number on each TiProxy node.
- TiProxy Throughput: The transferred bytes per second on each TiProxy node. If the maximum throughput reaches the maximum network bandwidth, it is recommended that you scale out TiProxy. To learn about the maximum network bandwidth, see [Decide TiProxy instance size and number](#decide-tiproxy-instance-size-and-number).
- TiProxy Sessions Migration Reasons: The number of session migrations that happen every minute and the reason for them. For example, when TiDB scales in and TiProxy migrates sessions to other TiDB instances, the reason is `status`. For more migration reasons, see [TiProxy Monitoring Metrics](/tiproxy/tiproxy-grafana.md#balance).

### View TiProxy bills

To view TiProxy bills, perform the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com), switch to your target organization using the combo box in the upper-left corner.
2. In the left navigation pane, click **Billing**. On the **Billing** page, the **Bills** tab is displayed by default.
3. In the **Summary by Service** section, TiProxy node cost is displayed under **TiDB Dedicated**, while TiProxy data transfer cost is included in **Data Transfer > Same Region**.

![TiProxy Billing](/media/tidb-cloud/tiproxy-billing.png)

## Modify TiProxy

To scale-in or scale-out TiProxy, perform the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project, and then click the name of your target cluster to go to its overview page.
2. Click **...** in the upper-right corner, and click **Modify** in the drop-down menu. The **Modify Cluster** page is displayed.
3. On the **Modify Cluster** page, modify the TiProxy number.

![Modify TiProxy](/media/tidb-cloud/tiproxy-enable-tiproxy.png)

> **Note**
>
> - Modifying the TiProxy size is not supported. It is recommended that you modify the TiProxy number. If you must modify the TiProxy size, you need to disable TiProxy in all the TiDB node groups and then enable it again to choose a different size.
> - Scaling in TiProxy will cause connections to disconnect. Make sure you scale in TiProxy in the maintenance window.

## Manage TiProxy in TiDB node groups

When you have multiple TiDB node groups, each TiDB node group has its dedicated TiProxy group. TiProxy will route traffic to the TiDB instances in the same TiDB node group to isolate computing resources. You can enable, disable, or modify TiProxy in each TiDB node group. However, the TiProxy size in all the TiDB node groups must be the same.
