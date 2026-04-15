---
title: TiProxy Load Balancing Policies
summary: Introduce the load balancing policies in TiProxy and their applicable scenarios.
---

# TiProxy Load Balancing Policies

TiProxy v1.0.0 only supports status-based and connection count-based load balancing policies for TiDB servers. Starting from v1.1.0, TiProxy introduces five additional load balancing policies: label-based, health-based, memory-based, CPU-based, and location-based.

By default, TiProxy applies these policies with the following priorities:

1. Status-based load balancing: when a TiDB server is shutting down, TiProxy migrates connections from that TiDB server to an online TiDB server.
2. Label-based load balancing: TiProxy prioritizes routing requests to TiDB servers that share the same label as the TiProxy instance, enabling resource isolation at the computing layer.
3. Health-based load balancing: when the health of a TiDB server is abnormal, TiProxy migrates connections from that TiDB server to a healthy TiDB server.
4. Memory-based load balancing: when a TiDB server is at risk of running out of memory (OOM), TiProxy migrates connections from that TiDB server to a TiDB server with lower memory usage.
5. CPU-based load balancing: when the CPU usage of a TiDB server is much higher than that of other TiDB servers, TiProxy migrates connections from that TiDB server to a TiDB server with lower CPU usage.
6. Location-based load balancing: TiProxy prioritizes routing requests to the TiDB server geographically closest to TiProxy.
7. Connection count-based load balancing: when the connection count of a TiDB server is much higher than that of other TiDB servers, TiProxy migrates connections from that TiDB server to a TiDB server with fewer connections.

To adjust the priorities of load balancing policies, see [Configure load balancing policies](#configure-load-balancing-policies).

## Status-based load balancing

TiProxy periodically checks whether a TiDB server is offline or shutting down using the SQL port and status port.

## Label-based load balancing

Label-based load balancing prioritizes routing connections to TiDB servers that share the same label as TiProxy, enabling resource isolation at the computing layer. This policy is disabled by default and should only be enabled when your workload requires computing resource isolation.

To enable label-based load balancing, you need to:

- Specify the matching label name through [`balance.label-name`](/tiproxy/tiproxy-configuration.md#label-name).
- Configure the [`labels`](/tiproxy/tiproxy-configuration.md#labels) configuration item in TiProxy.
- Configure the [`labels`](/tidb-configuration-file.md#labels) configuration item in TiDB servers.

After configuration, TiProxy uses the label name specified in `balance.label-name` to route connections to TiDB servers with matching label values.

Consider an application that handles both transaction and BI workloads. To prevent these workloads from interfering with each other, configure your cluster as follows:

1. Set [`balance.label-name`](/tiproxy/tiproxy-configuration.md#label-name) to `"app"` in TiProxy, indicating that TiDB servers will be matched by the label name `"app"`, and connections will be routed to TiDB servers with matching label values.
2. Deploy at least two TiProxy instances. Configure the TiProxy instance used for transaction business with [`labels`](/tiproxy/tiproxy-configuration.md#labels) as `{"app"="Order"}`, and the instance used for BI business with [`labels`](/tiproxy/tiproxy-configuration.md#labels) as `{"app"="BI"}`.
3. If high availability of TiProxy is required, deploy at least four TiProxy instances, and configure different virtual IP addresses for different businesses. For example, configure two TiProxy instances used for transaction business with virtual IP `10.0.1.10/24`, and two TiProxy instances used for BI business with virtual IP `10.0.1.20/24`.
4. Divide TiDB instances into two groups, adding `"app"="Order"` and `"app"="BI"` to their respective [`labels`](/tidb-configuration-file.md#labels) configuration items.
5. Optional: For storage layer isolation, configure [Placement Rules](/configure-placement-rules.md) or [Resource Control](/tidb-resource-control-ru-groups.md).
6. Direct transaction and BI clients to connect to their respective virtual IP addresses.

<img src="https://docs-download.pingcap.com/media/images/docs/tiproxy/tiproxy-balance-label-v2.png" alt="Label-based Load Balancing" width="600" />

Example configuration for this topology:

```yaml
component_versions:
  tiproxy: "v1.1.0"

server_configs:
  tiproxy:
    balance.label-name: "app"
  tidb:
    graceful-wait-before-shutdown: 30

tiproxy_servers:
  - host: tiproxy-host-1
    config:
      labels: {"app": "Order"}
      ha.virtual-ip: "10.0.1.10/24"
      ha.interface: "eth0"
  - host: tiproxy-host-2
    config:
      labels: {"app": "Order"}
      ha.virtual-ip: "10.0.1.10/24"
      ha.interface: "eth0"
  - host: tiproxy-host-3
    config:
      labels: {"app": "BI"}
      ha.virtual-ip: "10.0.1.20/24"
      ha.interface: "eth0"
  - host: tiproxy-host-4
    config:
      labels: {"app": "BI"}
      ha.virtual-ip: "10.0.1.20/24"
      ha.interface: "eth0"

tidb_servers:
  - host: tidb-host-1
    config:
      labels: {"app": "Order"}
  - host: tidb-host-2
    config:
      labels: {"app": "Order"}
  - host: tidb-host-3
    config:
      labels: {"app": "BI"}
  - host: tidb-host-4
    config:
      labels: {"app": "BI"}

tikv_servers:
  - host: tikv-host-1
  - host: tikv-host-2
  - host: tikv-host-3

pd_servers:
  - host: pd-host-1
  - host: pd-host-2
  - host: pd-host-3
```

## Health-based load balancing

TiProxy determines the health of a TiDB server by querying its error count. When the health of a TiDB server is abnormal while others are normal, TiProxy migrates connections from that server to a healthy TiDB server, achieving automatic failover.

This policy is suitable for the following scenarios:

- A TiDB server frequently fails to send requests to TiKV, causing frequent SQL execution failures.
- A TiDB server frequently fails to send requests to PD, causing frequent SQL execution failures.

## Memory-based load balancing

TiProxy queries the memory usage of TiDB servers. When the memory usage of a TiDB server is rapidly increasing or reaching a high level, TiProxy migrates connections from that server to a TiDB server with lower memory usage, preventing unnecessary connection termination due to OOM. TiProxy does not guarantee identical memory usage across TiDB servers. This policy only takes effect when a TiDB server is at risk of OOM.

When a TiDB server is at risk of OOM, TiProxy attempts to migrate all connections from it. Usually, if OOM is caused by runaway queries, ongoing runaway queries will not be migrated to another TiDB server for re-execution, because these connections can only be migrated after the transaction is complete.

This policy has the following limitations:

- If the memory usage of a TiDB server grows too quickly and reaches OOM within 30 seconds, TiProxy might not be able to detect the OOM risk in time, potentially leading to connection termination.
- TiProxy aims to maintain client connections without termination, not to reduce the memory usage of TiDB servers to avoid OOM. Therefore, TiDB servers might still encounter OOM.
- This policy applies only to TiDB server v8.0.0 and later versions. For earlier versions of TiDB servers, this policy does not take effect.

## CPU-based load balancing

TiProxy queries the CPU usage of TiDB servers and migrates connections from a TiDB server with high CPU usage to a server with lower usage, reducing overall query latency. TiProxy does not guarantee identical CPU usage across TiDB servers but ensures that the CPU usage differences are minimized.

This policy is suitable for the following scenarios:

- When background tasks (such as `ANALYZE`) consume a significant amount of CPU resources, the TiDB servers executing these tasks have higher CPU usage.
- When workloads on different connections vary greatly, even if the connection count on each TiDB server is similar, the CPU usage might differ significantly.
- When TiDB servers in the cluster have different CPU resource configurations, even with balanced connection counts, the actual CPU usage might be imbalanced.

## Location-based load balancing

TiProxy prioritizes routing connections to geographically closer TiDB servers based on the locations of TiProxy and TiDB servers.

This policy is suitable for the following scenarios:

- When a TiDB cluster is deployed across availability zones in the cloud, to reduce cross-availability zone traffic costs between TiProxy and TiDB servers, TiProxy prioritizes routing requests to TiDB servers in the same availability zone.
- When a TiDB cluster is deployed across data centers, to reduce network latency between TiProxy and TiDB servers, TiProxy prioritizes routing requests to TiDB servers in the same data center.

By default, this policy has a lower priority than health-based, memory-based, and CPU-based load balancing policies. You can increase its priority by setting [`policy`](/tiproxy/tiproxy-configuration.md#policy) to `location`. To maintain availability and performance, it is recommended to ensure that at least three TiDB servers are in the same location.

TiProxy determines the locations of itself and TiDB servers based on the `zone` label. You need to set the following configuration items:

- In the [`labels`](/tidb-configuration-file.md#labels) configuration item of the TiDB server, set `zone` to the current availability zone. For configuration details, see [Configure labels for TiDB](/schedule-replicas-by-topology-labels.md#optional-configure-labels-for-tidb).
- In the [`labels`](/tiproxy/tiproxy-configuration.md#labels) configuration item of TiProxy, set `zone` to the current availability zone.

For clusters deployed using TiDB Operator, see [High availability of data](https://docs.pingcap.com/tidb-in-kubernetes/stable/configure-a-tidb-cluster#high-availability-of-data).

The following is an example of a cluster configuration:

```yaml
component_versions:
  tiproxy: "v1.1.0"
server_configs:
  tidb:
    graceful-wait-before-shutdown: 30
tiproxy_servers:
  - host: tiproxy-host-1
    config:
      labels:
        zone: east
  - host: tiproxy-host-2
    config:
      labels:
        zone: west
tidb_servers:
  - host: tidb-host-1
    config:
      labels:
        zone: east
  - host: tidb-host-2
    config:
      labels:
        zone: west
tikv_servers:
  - host: tikv-host-1
  - host: tikv-host-2
  - host: tikv-host-3
pd_servers:
  - host: pd-host-1
  - host: pd-host-2
  - host: pd-host-3
```

In the preceding configuration, the TiProxy instance on `tiproxy-host-1` prioritizes routing requests to the TiDB server on `tidb-host-1` because `tiproxy-host-1` has the same `zone` configuration as `tidb-host-1`. Similarly, the TiProxy instance on `tiproxy-host-2` prioritizes routing requests to the TiDB server on `tidb-host-2`.

## Connection count-based load balancing

TiProxy migrates connections from a TiDB server with more connections to a server with fewer connections. This policy is not configurable and has the lowest priority.

Typically, TiProxy identifies the load on TiDB servers based on CPU usage. This policy usually takes effect in the following scenarios:

- When the TiDB cluster is just starting up, the CPU usage of all TiDB servers is close to 0. In this case, this policy prevents imbalanced load during startup.
- When the [CPU-based load balancing](#cpu-based-load-balancing) is not enabled, this policy ensures load balancing.

## Configure load balancing policies

TiProxy lets you configure the combination and priority of load balancing policies through the [`policy`](/tiproxy/tiproxy-configuration.md#policy) configuration item.

- `resource`: the resource priority policy performs load balancing based on the following priority order: status, label, health, memory, CPU, location, and connection count.
- `location`: the location priority policy performs load balancing based on the following priority order: status, label, location, health, memory, CPU, and connection count.
- `connection`: the minimum connection count policy performs load balancing based on the following priority order: status, label, and connection count.

## More resources

For more information about the load balancing policies of TiProxy, see the [design document](https://github.com/pingcap/tiproxy/blob/main/docs/design/2024-02-01-multi-factor-based-balance.md).
