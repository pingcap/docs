---
title: TiProxy Load Balancing Policies
summary: Introduces TiProxy load balancing policies and their applicable scenarios.
---

# TiProxy Load Balancing Policies

In TiProxy v1.0.0, TiProxy supports only load balancing policies based on TiDB server status and connection count. Starting from v1.1.0, TiProxy adds five new load balancing policies: based on labels, health, memory, CPU, and location.

With the default configuration, these policies are prioritized from highest to lowest as follows:

1. Label-based load balancing: preferentially routes connection requests to TiDB servers that have the same labels as the TiProxy instance itself, to achieve resource isolation for the compute layer.
2. Status-based load balancing: when a TiDB server cannot provide service normally or is shutting down, TiProxy migrates connections from that TiDB server to online TiDB servers.
3. Health-based load balancing: when a TiDB server has abnormal health, TiProxy migrates connections from that TiDB server to TiDB servers with normal health.
4. Memory-based load balancing: when a TiDB server has an Out of Memory (OOM) risk, TiProxy migrates connections from that TiDB server to TiDB servers with lower memory usage.
5. CPU-based load balancing: when a TiDB server's CPU usage is much higher than that of other TiDB servers, TiProxy migrates connections from that TiDB server to TiDB servers with lower CPU usage.
6. Location-based load balancing: preferentially routes requests to TiDB servers that are geographically closer to TiProxy.
7. Connection-count-based load balancing: when a TiDB server has far more connections than other TiDB servers, TiProxy migrates connections from that TiDB server to TiDB servers with fewer connections.

To adjust the priority of load balancing policies, see [Load balancing policy configuration](#负载均衡策略配置).

## Label-based load balancing

Label-based load balancing preferentially routes connections to TiDB servers that have the same labels as TiProxy itself, thereby achieving resource isolation for the compute layer. This policy is disabled by default and needs to be enabled only when your business requires compute-layer resource isolation.

To enable label-based load balancing, you need to:

- Use [`balance.label-name`](/tiproxy/tiproxy-configuration.md#label-name) to specify the label name used for matching
- Configure the TiProxy configuration item [`labels`](/tiproxy/tiproxy-configuration.md#labels)
- Configure the TiDB server configuration item [`labels`](/tidb-configuration-file.md#labels)

After the configuration is complete, TiProxy looks up the corresponding configuration according to the label name specified by `balance.label-name` and routes connections to TiDB servers with the same label value.

For example, if your application includes two types of workloads, transaction and BI, to avoid mutual interference, you can configure the cluster as follows:

1. Configure [`balance.label-name`](/tiproxy/tiproxy-configuration.md#label-name) on TiProxy as `"app"`, which means TiDB servers are matched by the label name `"app"`, and connections are routed to TiDB servers with the same label value.
2. Configure at least two TiProxy instances. For TiProxy instances used for transaction workloads, configure [`labels`](/tiproxy/tiproxy-configuration.md#labels) as `{"app"="Order"}`. For instances used for BI workloads, configure [`labels`](/tiproxy/tiproxy-configuration.md#labels) as `{"app"="BI"}`.
3. If you also need high availability for TiProxy, configure at least four TiProxy instances, and configure different virtual IPs for instances serving different workloads. For example, configure the two TiProxy instances for transaction workloads with virtual IP `10.0.1.10/24`, and configure the two TiProxy instances for BI workloads with virtual IP `10.0.1.20/24`.
4. Divide TiDB instances into two groups, and add `"app"="Order"` and `"app"="BI"` respectively to the [`labels`](/tidb-configuration-file.md#labels) configuration item.
5. If you also need to isolate resources at the storage layer, you can configure [Placement Rules](/configure-placement-rules.md) or [Resource Control](/tidb-resource-control-ru-groups.md).
6. Clients for transaction and BI workloads connect to the two virtual IP addresses respectively.

<img src="https://docs-download.pingcap.com/media/images/docs-cn/tiproxy/tiproxy-balance-label-v2.png" alt="Label-based load balancing" width="600" />

The configuration example for the preceding topology is as follows:

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

## Status-based load balancing

TiProxy periodically checks through the SQL port and status port whether a TiDB server can provide service normally, including whether it has been stopped or is shutting down.

## Health-based load balancing

TiProxy queries the error count of TiDB servers to determine their health. When one TiDB server has abnormal health while other TiDB servers are normal, TiProxy migrates the connections of that TiDB server to other TiDB servers to implement automatic failover.

This policy applies to the following scenarios:

- A TiDB server frequently fails to send requests to TiKV, causing frequent SQL execution failures.
- A TiDB server frequently fails to send requests to PD, causing frequent SQL execution failures.

## Memory-based load balancing

TiProxy queries the memory usage of TiDB servers. When a TiDB server's memory usage rises rapidly or its usage is very high, TiProxy migrates that TiDB server's connections to other TiDB servers to avoid unnecessary connection interruptions caused by OOM. TiProxy does not guarantee that the memory usage of all TiDB servers stays close. This policy takes effect only when a TiDB server has an OOM risk.

When a TiDB server has an OOM risk, TiProxy tries to migrate all connections from that TiDB server. In most cases, if the OOM is caused by a Runaway Query, because a connection can be migrated only after the transaction ends, the running Runaway Query is not migrated to another TiDB server for re-execution.

This policy has the following limitations:

- If a TiDB server's memory usage grows too quickly and OOM occurs within 30 seconds, TiProxy might not be able to determine the OOM risk in time, so connections might still be interrupted.
- TiProxy aims to keep client connections from being interrupted, rather than reducing TiDB server memory usage to avoid OOM, so OOM can still occur on the TiDB server.
- Only TiDB server v8.0.0 and later versions are supported. This policy does not take effect when earlier versions of TiDB server are used.

## CPU-based load balancing

TiProxy queries the CPU usage of TiDB servers and migrates connections from TiDB servers with higher CPU usage to TiDB servers with lower CPU usage, reducing overall query latency. TiProxy does not guarantee that the CPU usage of all TiDB servers is exactly the same. It only ensures that the difference in CPU usage is not too large.

This policy applies to the following scenarios:

- When background tasks such as Analyze consume many CPU resources, the TiDB server executing the background tasks has higher CPU usage.
- When workloads differ greatly across different connections, even if the connection counts on TiDB servers are similar, CPU usage can differ significantly.
- When TiDB servers in the cluster have different CPU resource configurations, actual CPU usage can still be unbalanced even if connection counts are balanced.

## Location-based load balancing

Based on the geographic locations of itself and TiDB servers, TiProxy preferentially routes connections to TiDB servers that are closer to TiProxy.

This policy applies to the following scenarios:

- When a TiDB cluster is deployed across availability zones in the cloud, to reduce cross-availability-zone traffic costs between TiProxy and TiDB servers, TiProxy preferentially routes requests to TiDB servers in the same availability zone.
- When a TiDB cluster is deployed across datacenters, to reduce network latency between TiProxy and TiDB servers, TiProxy preferentially routes requests to TiDB servers in the same datacenter.

By default, the priority of this policy is lower than that of health-, memory-, and CPU-based load balancing policies. You can increase its priority by setting [`policy`](/tiproxy/tiproxy-configuration.md#policy) to `location`, but it is recommended to ensure that there are at least three TiDB servers in the same geographic location to guarantee availability and performance.

TiProxy determines the geographic locations of itself and TiDB servers based on their `zone` labels. You need to set the following configuration items:

- In the TiDB server [`labels`](/tidb-configuration-file.md#labels) configuration item, set `zone` to the current availability zone. For the configuration method, see [Set TiDB `labels`](/schedule-replicas-by-topology-labels.md#设置-tidb-的-labels可选).
- In the TiProxy [`labels`](/tiproxy/tiproxy-configuration.md#labels) configuration item, set `zone` to the current availability zone.

If the cluster is deployed using TiDB Operator, see [High availability of data](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/configure-a-tidb-cluster#数据的高可用) for configuration.

The following is an example of cluster configuration:

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

In the preceding configuration, `tiproxy-host-1` and `tidb-host-1` have the same `zone` configuration, so the TiProxy on `tiproxy-host-1` preferentially routes requests to the TiDB server on `tidb-host-1`. Similarly, the TiProxy on `tiproxy-host-2` preferentially routes requests to the TiDB server on `tidb-host-2`.

## Connection-count-based load balancing

TiProxy migrates connections from TiDB servers with more connections to TiDB servers with fewer connections. This policy has the lowest priority.

TiProxy usually identifies the load of TiDB servers based on CPU usage. This policy usually takes effect in the following scenarios:

- When the TiDB cluster has just started and the CPU usage of all TiDB servers is close to 0, this policy prevents load imbalance during startup.
- When [CPU-based load balancing](#基于-cpu-的负载均衡) is not enabled, use this policy to ensure load balancing.

## Load balancing policy configuration

TiProxy supports configuring the combination and priority of the preceding load balancing policies through the [`policy`](/tiproxy/tiproxy-configuration.md#policy) configuration item.

- `resource`: resource-priority policy. The priority order is load balancing based on labels, status, health, memory, CPU, location, and connection count.
- `location`: location-priority policy. The priority order is load balancing based on labels, status, location, health, memory, CPU, and connection count.
- `connection`: minimum-connection-count policy. The priority order is load balancing based on labels, status, and connection count.

For more load balancing configuration items, see [`balance`](/tiproxy/tiproxy-configuration.md#balance).

## Resources

For more detailed information about TiProxy load balancing policies, see the [design document](https://github.com/pingcap/tiproxy/blob/main/docs/design/2024-02-01-multi-factor-based-balance.md).