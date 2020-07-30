---
title: Cluster Topology Configuration
summary: Learn to configure cluster topology to maximize the capacity for disaster recovery.
aliases: ['/docs/dev/location-awareness/','/docs/dev/how-to/deploy/geographic-redundancy/location-awareness/']
---

# Cluster Topology Configuration

## Overview

PD schedules according to the topology of the TiKV cluster to maximize the TiKV's capability for disaster recovery. We recommend that TiKV nodes should be physically dispersed as much as possible. For example, TiKV nodes can be distributed in different racks or even different data zones. According to the topology information of TiKV, the PD scheduler will automatically schedule in the background to isolate the replicas of the Region as much as possible, thereby maximizing the data disaster tolerance.

Before you begin, see [Deploy TiDB Using TiDB Ansible (Recommended)](/online-deployment-using-ansible.md) and [Deploy TiDB Using Docker](/test-deployment-using-docker.md).

## TiKV reports the topological information

TiKV reports the topological information to PD according to the startup parameter or configuration of TiKV.

Assuming that the topology has three structures: zone > rack > host, use labels to specify the following information:

Startup parameter:

```
tikv-server --labels zone=<zone>,rack=<rack>,host=<host>
```

Configuration:

``` toml
[server]
labels = "zone=<zone>,rack=<rack>,host=<host>"
```

## PD understands the TiKV topology

PD gets the topology of TiKV cluster through the PD configuration.

``` toml
[replication]
max-replicas = 3
location-labels = ["zone", "rack", "host"]
```

After the PD cluster is initialized, you need to use the pd-ctl tool to make online changes:

{{< copyable "shell-regular" >}}

```bash
pd-ctl config set location-labels zone,rack,host
```

`location-labels` needs to correspond to the TiKV `labels` name so that PD can understand that the `labels` represents the TiKV topology.

> **Note:**
>
> You must configure `location-labels` for PD and `labels` for TiKV at the same time for `labels` to take effect.

## PD restricts the TiKV topology

With configuring `location-labels` first, we can further enhance the topological isolation requirements of TiKV clusters through the `isolation-level`. Suppose we divide the cluster topology into three layers through `location-labels` according to the above instructions: zone -> rack -> host, and configure the `isolation-level` as follows.

{{< copyable "" >}}

```toml
[replication]
isolation-level = "zone"
```

After the PD cluster is initialized, you need to use the pd-ctl tool to make online changes:

{{< copyable "shell-regular" >}}

```bash
pd-ctl config set isolation-level zone
```

`isolation-level` needs to correspond to one of the `location-labels` name so that PD can understand that this label represents the TiKV topology.

> **Note:**
>
> `isolation-level` is empty by default, that is, there is no mandatory isolation level restriction. To set it, you must first configure the PD's `location-labels` parameter, and ensure that the value of `isolation-level` must be one of `location-labels`.

## PD schedules based on the TiKV topology

PD makes optimal scheduling according to the topological information. You just need to care about what kind of topology can achieve the desired effect.

If you use 3 replicas and hope that the TiDB cluster is always highly available even when a data zone goes down, you need at least 4 data zones.

Assume that you have 4 data zones, each zone has 2 racks, and each rack has 2 hosts. You can start 2 TiKV instances on each host:

```
# zone=z1
tikv-server --labels zone=z1,rack=r1,host=h1
tikv-server --labels zone=z1,rack=r1,host=h2
tikv-server --labels zone=z1,rack=r2,host=h1
tikv-server --labels zone=z1,rack=r2,host=h2

# zone=z2
tikv-server --labels zone=z2,rack=r1,host=h1
tikv-server --labels zone=z2,rack=r1,host=h2
tikv-server --labels zone=z2,rack=r2,host=h1
tikv-server --labels zone=z2,rack=r2,host=h2

# zone=z3
tikv-server --labels zone=z3,rack=r1,host=h1
tikv-server --labels zone=z3,rack=r1,host=h2
tikv-server --labels zone=z3,rack=r2,host=h1
tikv-server --labels zone=z3,rack=r2,host=h2

# zone=z4
tikv-server --labels zone=z4,rack=r1,host=h1
tikv-server --labels zone=z4,rack=r1,host=h2
tikv-server --labels zone=z4,rack=r2,host=h1
tikv-server --labels zone=z4,rack=r2,host=h2
```

In other words, 16 TiKV instances are distributed across 4 data zones, 8 racks and 16 machines.

In this case, PD will schedule different replicas of each datum to different data zones.

- If one of the data zones goes down, the high availability of the TiDB cluster is not affected.
- If the data zone cannot recover within a period of time, PD will remove the replica from this data zone.

To sum up, PD maximizes the disaster recovery of the cluster according to the current topology. Therefore, if you want to reach a certain level of disaster recovery, deploy many machines in different sites according to the topology. The number of machines must be more than the number of `max-replicas`.

However, with setting `isolation-level` to `"zone"`, PD will strictly ensure that each replica will isolated from each other at the zone level, even if guaranteeing this will not meet the number requirement of `max-replicas`. For example, there are three data zones z1/z2/z3 in the TiKV cluster. Under the requirement of 3 replicas, PD will dispatch the three replicas of the same Region to these three data zones. If there is a power outage in the z1 and it cannot be recovered after a period of time, PD will think that the region replica on z1 is no longer available, but because the `isolation-level` is set to `"zone"`, PD needs to strictly guarantee different region replicas will not fall on the same data zone. Because both z2 and z3 already have copies, PD will not perform any scheduling under the minimum isolation level limit of `isolation-level`, even if there are only two copies at this moment.

Similarly, when `isolation-level` is `"rack"`, the minimum isolation level will be different racks in the same data zone. Under this configuration, the isolation at the zone level will be guaranteed first if it can be. When the isolation at the zone level cannot be promised, PD will consider to avoid scheduling replicas to be in the same zone with the same rack, and so on.