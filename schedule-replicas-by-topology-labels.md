---
title: Schedule Replicas by Topology Labels
aliases: ['/docs/dev/location-awareness/','/docs/dev/how-to/deploy/geographic-redundancy/location-awareness/','/tidb/dev/location-awareness']
---

# Schedule Replicas by Topology Labels

To improve the high availability and disaster tolerance of TiDB clusters, it is recommended that TiKV nodes are physically distributed as much as possible. For example, TiKV nodes can be distributed on different racks or even in different data centers. According to the topology information of TiKV, the PD scheduler automatically performs scheduling at the background to isolate the replicas of Regions as much as possible, thereby maximizing the capability for disaster recovery.

To make this mechanism effective, you need to report the topology information of the cluster, especially the TiKV location, to PD for proper configuration during deployment. Before you begin, see [Deploy TiDB Using TiUP](/production-deployment-using-tiup.md).

## Configure `labels` based on the cluster topology

### Set the `labels` configuration of TiKV

TiKV supports binding some attributes through command-line flags or configuration files in the form of key-value pairs. The attribute is called a `label`. TiKV reports its labels to PD so we can mark the TiKV location.

Assume that the topology has three structures: zone > rack > host, use these labels to set the TiKV location.

Command-line flags:

{{< copyable "" >}}

```
tikv-server --labels zone=<zone>,rack=<rack>,host=<host>
```

Configuration files:

{{< copyable "" >}}

```toml
[server]
labels = "zone=<zone>,rack=<rack>,host=<host>"
```

### Set the `location-labels` configuration of PD

According to the previous description, labels can be any key-value pairs used to describe TiKV attributes, but PD can not distinguish the location-marking labels and the structure among them. Therefore, you need to set some configuration to understand the TiKV node topology.

Set the PD configuration `location-labels` through the PD configuration files.

{{< copyable "" >}}

```toml
[replication]
location-labels = ["zone", "rack", "host"]
```

If PD cluster is already initialized, you need to use the pd-ctl tool to make online changes:

{{< copyable "shell-regular" >}}

```bash
pd-ctl config set location-labels zone,rack,host
```

The `location-labels` configuration is an array of strings, and each item corresponds to the key of TiKV `labels`. The sequence of each key represents the layer relationship among different labels.

> **Note:**
>
> You must configure `location-labels` for PD and `labels` for TiKV at the same time for `labels` to take effect. Otherwise, PD does not schedule according to the topology.

### Set the `isolation-level` configuration of PD

Under the premise of configuring `location-labels`, you can further strengthen the topological isolation requirements for TiKV clusters through the `isolation-level` configuration. 

Assume that the topology is divided into three structures through `location-labels` according to the above instructions: zone > rack > host, and the `isolation-level` is configured as follows:

{{< copyable "" >}}

```toml
[replication]
isolation-level = "zone"
```

If PD cluster is already initialized, you need to use the pd-ctl tool to make online changes:

{{< copyable "shell-regular" >}}

```bash
pd-ctl config set isolation-level zone
```

The `location-level` configuration is an array of strings, which needs to correspond to a key of `location-labels`. This parameter limits the minimum and mandatory isolation level requirements for TiKV topology clusters.

> **Note:**
>
> `isolation-level` is empty by default, which means there is no mandatory isolation level restriction. To set it, you need to configure the `location-labels` of PD, and ensure that the value of `isolation-level` must be one of `location-labels`.

### Use TiDB Ansible to deploy a cluster

You can directly set location related configuration in the `inventory.ini` file when using TiDB Ansible to deploy a cluster. `tidb-ansible` generates the corresponding TiKV and PD configuration files during deployment.

The following example defines a double-level topology of `zone/host`. The TiKV of the cluster is distributed in three zones, with two hosts in each zone. z1 is deployed with two TiKV instances per host, and z2 and z3 are deployed with 1 instance per host.

```
[tikv_servers]
# z1
tikv-1 labels="zone=z1,host=h1"
tikv-2 labels="zone=z1,host=h1"
tikv-3 labels="zone=z1,host=h2"
tikv-4 labels="zone=z1,host=h2"
# z2
tikv-5 labels="zone=z2,host=h1"
tikv-6 labels="zone=z2,host=h2"
# z3
tikv-7 labels="zone=z3,host=h1"
tikv-8 labels="zone=z3,host=h2"

[pd_servers:vars]
location_labels = ["zone", "host"]
```

## PD schedules based on topology label

PD schedules replicas according to the label level to make sure that different replicas of the same data are distributed as much as possible.

Take the topology in the previous section as an example.

Assume that the number of cluster replicas is 3 (`max-replicas=3`). As there are 3 zones in total, PD keeps the 3 replicas of each Region placed in z1/z2/z3, so that the TiDB cluster is still available when any data center fails,

Assume that the number of cluster replicas is 5 (`max-replicas=5`). As there are only 3 zones in total, PD can not guarantee the isolation of each replica at this level. At this time, the PD scheduler adjusts to ensure isolation at the host level. In other words, multiple copies of a Region might be distributed in the same zone, but will not be distributed on the same host.

Under the premise of the 5-replica configuration, if z3 occurs an overall failure or isolation, and can not be restored in a period (controlled by `max-store-down-time`), PD will make up the 5 replicas through scheduling. At this time, only 3 hosts are available, so host level isolation can not be guaranteed. Therefore, multiple copies might be distributed to the same host. But if the value `isolation-level` is set to `zone` instead of empty, this specifies the minimum physical isolation requirements for Region replicas. That is to say, PD ensures that replicas of the same Region are scattered in different zones. Even if following this isolation restriction does not meet the multiple replica requirements of `max-replicas`, PD will not perform corresponding scheduling. 

For example, there are three data centers z1, z2 and z3 in the TiKV cluster. Under the three-replica setting, PD distributes the three replicas of the same Region to these three data centers respectively. At this time, if the entire data center z1 encounters a power outage and cannot be recovered in a period, the PD will consider that the Region copy on z1 is no longer available. But because the `isolation-level` is set to `zone`, PD needs to strictly ensure that different Region replicas will not fall into the same zone. At this time, as both z2 and z3 already have replicas, PD does not perform any scheduling under the restriction of the minimum mandatory isolation level, even if there are only two replicas.

Similarly, when `isolation-level` is set to `rack`, the minimum isolation level is different racks in the same data center. Under this setting, if isolation can be guaranteed at the zone level, it will be guaranteed first. Only when the zone level isolation can not be completed, will the scheduling in the same zone and the same rack be considered to avoid.

In summary, PD maximizes the disaster recovery of the cluster according to the current topology. Therefore, if you want to achieve a certain level of disaster recovery, deploy more machines on different sites according to the topology than the number of `max-replicas`. Also, TiDB provides mandatory isolation level settings such as `isolation-level` to control the topological isolation level according to the scenario more flexibly.
