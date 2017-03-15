# Multi-site Deployment

## Overview

PD schedules according to the topology of TiKV cluster, maximizing TiKV's ability of disaster recovery.

Before reading this chapter, you are recommended to read [Binary Deployment (Recommended)](./binary-deployment.md) and [Docker Deployment](./docker-deployment.md).

## TiKV reports the topological information

TiKV reports the topological information to PD through the startup parameter or configuration of TiKV.

Assume that the topology has three structures: zone > rack > host, the following information can be specified through labels.

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

PD understands the topology of TiKV cluster through PD configuration.

``` toml
[replication]
max-replicas = 3
location-labels = ["zone", "rack", "host"]
```

`location-labels` needs to corresponse to the name of `labels` of TiKV. Only in this way can PD know that these `labels` represent the TiKV topology.

## PD schedules based on the TiKV topology

PD makes optimal schedulings according to the topological information that we have provided. We just need to care about what kind of topology can achieve the desired effect.

Assume that we use three replicas and hope that everything still works well when a data zone hangs up. In this case, we need at least four data zones.
(Theoretically, three data zones are feasible but the current implementation is not guaranteed.)

Assume that we have four data zones, each zone has two racks and each rack has two hosts.
We can start two TiKV instances on each host:

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
If one of the data zones hangs up, everything still works well.
If the data zone couldn't recover within a period of time, PD will remove the replica of this data zone.
If there are only three (or two) data zones, we cannot guarantee that everything would work well when a data zone hangs up. However, it is ensured that everything is fine when a site hangs up.

In a word, PD maximized the disaster recovery of the cluster according to the current topology. Therefore, if we want to reach to a certain level of disaster recovery, we need to deploy many machines in different sites according to the topology. The number of machines should be more than the one of `max-replicas`.
