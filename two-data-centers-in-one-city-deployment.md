---
title: Two Data Centers in One City Deployment
summary: Learn the deployment solution to two data centers in one city.
aliases: ['/tidb/dev/synchronous-replication']
---

# Two Data Centers in One City Deployment with DR Auto-Sync Mode

This document introduces the deployment mode for two data centers (DC) in one city, including the architecture, configuration, methods to enable this delpoyment mode, and ways to use the replicas in this mode.

In an on-premises environment, TiDB usually adopts the multi-data-center deployment mode to ensure high availability and disaster recovery capability. The multi-data-center deployment mode includes a variety of deployment modes, such as three data centers in two cities and three data centers in one city. This document introduces the deployment mode of two data centers in one city. With lower cost, TiDB can also meet the requirements of high availability and disaster recovery. The deployment mode adopts Data Replication Auto Synchronous mode, or DR Auto-Sync mode.

Under the mode of two data centers in one city, the distance between the two data centers is within 50 kilometers. They are usually located in the same city or two adjacent cities (such as Beijing and Langfang in Hebei province). The network latency between the data centers is lower than 1.5 milliseconds and the bandwidth is higher than 10 Gbps.

## Architecture

This section takes the example of a city where two data centers IDC1 and IDC2 are located separately in the east and west.

The architecture of the cluster deployment is as follows:

- The TiDB cluster is deployed to two DCs in one city: the primary IDC1 in the east, and the DR IDC2 in the west.
- The cluster has 4 replicas, 2 Voter replicas in IDC1, 1 Voter replicas and 1 Learner replicas in IDC2. For the TiKV component, each rack has a proper label.
- The Raft protocol is adopted to ensure consistency and high availability of data, which is transparent to users.

![2-DC-in-1-city architecture](/media/two-dc-replication-1.png)

This deployment solution defines three status to control and label the replication status of the cluster, which restricts the replication mode of TiKV. The replication mode of the cluster can automatically and adaptively switch between the three status. For details, see [Status switch](#status-switch).

- **sync**: Synchronous replication mode. In this mode, at least one replica in DR data center synchronizes with the replica in the primary data center. Raft algorithm ensures that each log is replicated to DR based on the label.
- **async**: Asynchronous replication mode. In this mode, DR data center is not fully synchronized with the primary data center. Raft algorithm follows the majority protocol to replicate logs.
- **sync-recover**: Synchronous recovery mode. In this mode, DR is not fully synchronized with the primary data center. Raft gradually switches to label replication mode and then reports the label information to PD.

## Configuration

### Example

The following `tiup topology.yaml` yaml file example is a classic topology configuration for the two data centers in one city deployment mode:

```
# # Global variables are applied to all deployments and used as the default value of
# # the deployments if a specific deployment value is missing.
global:
  user: "tidb"
  ssh_port: 22
  deploy_dir: "/data/tidb_cluster/tidb-deploy"
  data_dir: "/data/tidb_cluster/tidb-data"

server_configs:
  pd:
    replication.location-labels:  ["zone","rack","host"]

pd_servers:
  - host: 10.63.10.10
    name: "pd-10"
  - host: 10.63.10.11
    name: "pd-11"
  - host: 10.63.10.12
    name: "pd-12"


tidb_servers:
  - host: 10.63.10.10
  - host: 10.63.10.11
  - host: 10.63.10.12


tikv_servers:
  - host: 10.63.10.30
    config:
      server.labels: { zone: "east", rack: "east-1", host: "30" }
  - host: 10.63.10.31
    config:
      server.labels: { zone: "east", rack: "east-2", host: "31" }
  - host: 10.63.10.32
    config:
      server.labels: { zone: "west", rack: "west-1", host: "32" }
  - host: 10.63.10.33
    config:
      server.labels: { zone: "west", rack: "west-2", host: "33" }


monitoring_servers:
  - host: 10.63.10.60

grafana_servers:
  - host: 10.63.10.60

alertmanager_servers:
  - host: 10.63.10.60
```

### Placement Rules

To deploy based on the planned cluster topology, you need to use [Placement Rules](/configure-placement-rules.md) to determine the locations of the cluster replicas. If 4 replica and 2 Voter replica is at the primary center and 1 Voter replica and 1 Learner replica is at the DR center, you can use the placement rules to configure the replicas as follows:

```
cat rule.json
[
  {
    "group_id": "pd",
    "id": "zone-east",
    "start_key": "",
    "end_key": "",
    "role": "voter",
    "count": 2,
    "label_constraints": [
      {
        "key": "zone",
        "op": "in",
        "values": [
          "east"
        ]
      }
    ],
    "location_labels": [
      "zone",
      "rack",
      "host",
    ]
  },
  {
    "group_id": "pd",
    "id": "zone-west",
    "start_key": "",
    "end_key": "",
    "role": "voter",
    "count": 1,
    "label_constraints": [
      {
        "key": "zone",
        "op": "in",
        "values": [
          "west"
        ]
      }
    ],
    "location_labels": [
      "zone",
      "rack",
      "host"
    ]
  },
  {
    "group_id": "pd",
    "id": "zone-west",
    "start_key": "",
    "end_key": "",
    "role": "learner",
    "count": 1,
    "label_constraints": [
      {
        "key": "zone",
        "op": "in",
        "values": [
          "west"
        ]
      }
    ],
    "location_labels": [
      "zone",
      "rack",
      "host"
    ]
  }
]
```

### Enable the DR Auto-Sync mode

The replication mode is controlled by PD. You can configure it in the PD configuration file when deploying a cluster as follows:

{{< copyable "" >}}

```toml
[replication-mode]
replication-mode = "dr-auto-sync"
[replication-mode.dr-auto-sync]
label-key = "zone"
primary = "east"
dr = "west"
primary-replicas = 2
dr-replicas = 1
wait-store-timeout = "1m"
wait-sync-timeout = "1m"
```

In the configuration above:

+ `replication-mode` is the replication mode to be enabled. In the above example, it is set to `dr-auto-sync`. By default, majority protocol is followed.
+ `label-key` is used to distinguish different data centers and needs to be matched with placement rules. In this example, the primary data center is "east" and the DR data center is "west".
+ `primary-replicas` ia the number of Voter replicas in the primary data center.
+ `dr-replicas` is the number of Voter replicas in the DR data center.
+ `wait-store-timeout` is the waiting time for switching to asynchronous replication mode when network isolation or failure occurs. If the time of network failure exceeds the waiting time, asynchronous replication mode is enabled. The default waiting time is 60 seconds.

To check the current replication state of the cluster, use the following API:

{{< copyable "shell-regular" >}}

```bash
curl http://pd_ip:pd_port/pd/api/v1/replication_mode/status
```

{{< copyable "shell-regular" >}}

```bash
{
  "mode": "dr-auto-sync",
  "dr-auto-sync": {
    "label-key": "zone",
    "state": "sync"
  }
}
```

#### Status Switch

The replication mode for clusters can automatically and adaptively switch between three status:

- When the clusters are normal, the synchronous replication mode is enabled to maximize the data integrity of the disaster recovery data center.
- When network fails or the disaster recovery data center breaks down, after a pre-set protective interval, the cluster enables asynchronous replication mode to ensure the availability of transactions.
- When network reconnects or the disaster recovery data center restores, the TiKV node joins the cluster again and gradually replicates the data. Finally, the cluster switches to synchronous replication mode.

The details for status switch is as follows:

1. **Initialization**: When the cluster is in the initialization process, the synchronous replication mode is enabled. PD sends information to TiKV and all TiKV nodes strictly follow the requirements of the synchronous replication mode to work.

2. **Switch from sync to async**: PD regularly check the heartbeat information of TiKV to judge if TiKV peers fail to work or disconnect. If the number of failed peers exceeds the number of replicas of the primary data center and the DR data center `primary-replicas` and `dr-replicas`, the synchronous replication mode fails to work and it is necessary to switch the status. When the failure or disconnect time exceeds the time set by `wait-store-timeout`, PD switches the status of the cluster to async mode. Then PD sends the status of async to all the TiKV nodes and the replication mode for TiKV switches from two-center replication to native Raft majority.

3. **Switch from async to sync**: PD regularly check the heartbeat information of TiKV to judge if TiKV peers reconnect. If  the number of failed peers is less than the number of replicas of the primary data center and the DR data center `primary-replicas` and `dr-replicas`, the synchronous replication mode can be enabled again. PD switches the status of the cluster to sync-recover and sends this status to all the TiKV nodes. All Regions of TiKV gradually switch to two-data-center synchronous replication mode and then report the heartbeat information to PD. PD records the status of Regions of TiKV and calculte the recovery progress. When all Regions of TiKV finish the switching, PD switches the replication mode to synchronous status.

### Disaster recovery

This section introduces the disaster recovery solution of the two data centers in one city deployment.

When a disaster occurs to a cluster in the synchronous replication mode, you can perform data recovery with `RPO = 0`:

- If the primary data center fails and most of the Voter replicas are lost, and complete data exists in the DR data center, the data can be recovered from the DR data center. At this time, manual intervention is required with professional tools (you can contact TiDB team for recovery).

- If the DR center fails and a few Voter replicas are lost, the cluster can automatically switch to asynchronous replication mode. to solve the problem.

When a disaster occurs to a cluster that is not in the synchronous replication mode and you cannot perform data recovery with `RPO = 0`:

- If most of the  Voter replicas are lost, manual intervention is required with professional tools (you can contact TiDB team for recovery).
