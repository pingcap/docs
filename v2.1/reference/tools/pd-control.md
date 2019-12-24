---
title: PD Control User Guide
summary: Use PD Control to obtain the state information of a cluster and tune a cluster.
category: reference
---

# PD Control User Guide

As a command line tool of PD, PD Control obtains the state information of the cluster and tunes the cluster.

## Compile from source code

1. [Go](https://golang.org/) Version 1.9 or later
2. In the root directory of the [PD project](https://github.com/pingcap/pd), use the `make` command to compile and generate `bin/pd-ctl`

> **Note:**
>
> Generally, you don't need to compile source code as the PD Control tool already exists in the released Binary or Docker. However, dev users can refer to the above instruction for compiling source code.

## Download TiDB installation package

If you want to download the latest version of `pd-ctl`, directly download the TiDB package, because `pd-ctl` is included in the TiDB package.

| Package download link | OS | Architecture | SHA256 checksum |
|:---|:---|:---|:---|
| `http://download.pingcap.org/tidb-{version}-linux-amd64.tar.gz` (pd-ctl) | Linux | amd64 | `http://download.pingcap.org/tidb-{version}-linux-amd64.sha256` |

> **Note:**
>
> `{version}` indicates the version number of TiDB. For example, if `{version}` is `v2.1.18`, the package download link is `http://download.pingcap.org/tidb-v2.1.18-linux-amd64.tar.gz`. You can also download the latest unpublished version by replacing `{version}` with `latest`.

## Usage

Single-command mode:

```bash
./pd-ctl store -d -u http://127.0.0.1:2379
```

Interactive mode:

```bash
./pd-ctl -u http://127.0.0.1:2379
```

Use environment variables:

```bash
export PD_ADDR=http://127.0.0.1:2379
./pd-ctl
```

Use TLS to encrypt:

```bash
./pd-ctl -u https://127.0.0.1:2379 --cacert="path/to/ca" --cert="path/to/cert" --key="path/to/key"
```

## Command line flags

### --cacert

+ Specifies the path to the certificate file of the trusted CA in PEM format
+ Default: ""

### --cert

+ Specifies the path to the certificate of SSL in PEM format
+ Default: ""

### \-\-detach,-d

+ Uses the single command line mode (not entering readline)
+ Default: false

### --key

+ Specifies the path to the certificate key file of SSL in PEM format, which is the private key of the certificate specified by `--cert`
+ Default: ""

### \-\-pd,-u

+ Specifies the PD address
+ Default address: `http://127.0.0.1:2379`
+ Environment variable: `PD_ADDR`

### --version,-V

+ Prints the version information and exit
+ Default: false

## Command

### `cluster`

Use this command to view the basic information of the cluster.

Usage:

```bash
>> cluster                                     // To show the cluster information
{
  "id": 6493707687106161130,
  "max_peer_count": 3
}
```

### `config [show | set <option> <value>]`

Use this command to view or modify the configuration information.

Usage:

```bash
>> config show                                // Display the config information of the scheduler
{
  "max-snapshot-count": 3,
  "max-pending-peer-count": 16,
  "max-merge-region-size": 50,
  "max-merge-region-keys": 200000,
  "split-merge-interval": "1h",
  "patrol-region-interval": "100ms",
  "max-store-down-time": "1h0m0s",
  "leader-schedule-limit": 4,
  "region-schedule-limit": 4,
  "replica-schedule-limit":8,
  "merge-schedule-limit": 8,
  "tolerant-size-ratio": 5,
  "low-space-ratio": 0.8,
  "high-space-ratio": 0.6,
  "disable-raft-learner": "false",
  "disable-remove-down-replica": "false",
  "disable-replace-offline-replica": "false",
  "disable-make-up-replica": "false",
  "disable-remove-extra-replica": "false",
  "disable-location-replacement": "false",
  "disable-namespace-relocation": "false",
  "schedulers-v2": [
    {
      "type": "balance-region",
      "args": null
    },
    {
      "type": "balance-leader",
      "args": null
    },
    {
      "type": "hot-region",
      "args": null
    }
  ]
}
>> config show all                            // Display all config information
>> config show namespace ts1                  // Display the config information of the namespace named ts1
{
  "leader-schedule-limit": 4,
  "region-schedule-limit": 4,
  "replica-schedule-limit": 8,
  "max-replicas": 3,
}
>> config show replication                    // Display the config information of replication
{
  "max-replicas": 3,
  "location-labels": ""
}
>> config show cluster-version                // Display the current version of the cluster, which is the current minimum version of TiKV nodes in the cluster and does not correspond to the binary version.
"2.0.0"
```

+ `max-snapshot-count` controls the maximum number of snapshots that a single store receives or sends out at the same time. The scheduler is restricted by this configuration to avoid taking up normal application resources. When you need to improve the speed of adding replicas or balancing, increase this value.

    ```bash
    >> config set max-snapshot-count 16  // Set the maximum number of snapshots to 16
    ```

+ `max-pending-peer-count` controls the maximum number of pending peers in a single store. The scheduler is restricted by this configuration to avoid producing a large number of Regions without the latest log in some nodes. When you need to improve the speed of adding replicas or balancing, increase this value. Setting it to 0 indicates no limit.

    ```bash
    >> config set max-pending-peer-count 64  // Set the maximum number of pending peers to 64
    ```

- `max-merge-region-size` controls the upper limit on the size of Region Merge (the unit is M). When `regionSize` exceeds the specified value, PD does not merge it with the adjacent Region. Setting it to 0 indicates disabling Region Merge.

    ```bash
    >> config set max-merge-region-size 16 // Set the upper limit on the size of Region Merge to 16M
    ```

- `max-merge-region-keys` controls the upper limit on the key count of Region Merge. When `regionKeyCount` exceeds the specified value, PD does not merge it with the adjacent Region.

    ```bash
    >> config set max-merge-region-keys 50000 // Set the the upper limit on keyCount to 50000
    ```

- `split-merge-interval` controls the interval between the `split` and `merge` operations on a same Region. This means the newly split Region won't be merged within a period of time.

    ```bash
    >> config set split-merge-interval 24h  // Set the interval between `split` and `merge` to one day
    ```

- `patrol-region-interval` controls the execution frequency that `replicaChecker` checks the health status of Regions. A shorter interval indicates a higher execution frequency. Generally, you do not need to adjust it.

    ```bash
    >> config set patrol-region-interval 10ms // Set the execution frequency of replicaChecker to 10ms
    ```

- `max-store-down-time` controls the time that PD decides the disconnected store cannot be restored if exceeded. If PD does not receive heartbeats from a store within the specified period of time, PD adds replicas in other nodes.

    ```bash
    >> config set max-store-down-time 30m  // Set the time within which PD receives no heartbeats and after which PD starts to add replicas to 30 minutes
    ```

- `leader-schedule-limit` controls the number of tasks scheduling the leader at the same time. This value affects the speed of leader balance. A larger value means a higher speed and setting the value to 0 closes the scheduling. Usually the leader scheduling has a small load, and you can increase the value in need.

    ```bash
    >> config set leader-schedule-limit 4         // 4 tasks of leader scheduling at the same time at most
    ```

- `region-schedule-limit` controls the number of tasks scheduling the Region at the same time. This value affects the speed of Region balance. A larger value means a higher speed and setting the value to 0 closes the scheduling. Usually the Region scheduling has a large load, so do not set a too large value.

    ```bash
    >> config set region-schedule-limit 2         // 2 tasks of Region scheduling at the same time at most
    ```

- `replica-schedule-limit` controls the number of tasks scheduling the replica at the same time. This value affects the scheduling speed when the node is down or removed. A larger value means a higher speed and setting the value to 0 closes the scheduling. Usually the replica scheduling has a large load, so do not set a too large value.

    ```bash
    >> config set replica-schedule-limit 4        // 4 tasks of replica scheduling at the same time at most
    ```

- `merge-schedule-limit` controls the number of Region Merge scheduling tasks. Setting the value to 0 closes Region Merge. Usually the Merge scheduling has a large load, so do not set a too large value.

    ```bash
    >> config set merge-schedule-limit 16       // 16 tasks of Merge scheduling at the same time at most
    ```

The configuration above is global. You can also tune the configuration by configuring different namespaces. The global configuration is used if the corresponding configuration of the namespace is not set.

> **Note:**
>
> The configuration of the namespace only supports editing `leader-schedule-limit`, `region-schedule-limit`, `replica-schedule-limit` and `max-replicas`.

```bash
>> config set namespace ts1 leader-schedule-limit 4 // 4 tasks of leader scheduling at the same time at most for the namespace named ts1
>> config set namespace ts2 region-schedule-limit 2 // 2 tasks of region scheduling at the same time at most for the namespace named ts2
```

- `tolerant-size-ratio` controls the size of the balance buffer area. When the score difference between the leader or Region of the two stores is less than specified multiple times of the Region size, it is considered in balance by PD.

    ```bash
    >> config set tolerant-size-ratio 20        // Set the size of the buffer area to about 20 times of the average regionSize
    ```

- `low-space-ratio` controls the threshold value that is considered as insufficient store space. When the ratio of the space occupied by the node exceeds the specified value, PD tries to avoid migrating data to the corresponding node as much as possible. At the same time, PD mainly schedules the remaining space to avoid using up the disk space of the corresponding node.

    ```bash
    config set low-space-ratio 0.9              // Set the threshold value of insufficient space to 0.9
    ```

- `high-space-ratio` controls the threshold value that is considered as sufficient store space. When the ratio of the space occupied by the node is less than the specified value, PD ignores the remaining space and mainly schedules the actual data volume.

    ```bash
    config set high-space-ratio 0.5             // Set the threshold value of sufficient space to 0.5
    ```

- `disable-raft-learner` is used to disable Raft learner. By default, PD uses Raft learner when adding replicas to reduce the risk of unavailability due to downtime or network failure.

    ```bash
    config set disable-raft-learner true        // Disable Raft learner
    ```

- `cluster-version` is the version of the cluster, which is used to enable or disable some features and to deal with the compatibility issues. By default, it is the minimum version of all normally running TiKV nodes in the cluster. You can set it manually only when you need to roll it back to an earlier version.

    ```bash
    config set cluster-version 1.0.8              // Set the version of the cluster to 1.0.8
    ```

- `disable-remove-down-replica` is used to disable the feature of automatically deleting DownReplica. When you set it to `true`, PD does not automatically clean up the downtime replicas.

- `disable-replace-offline-replica` is used to disable the feature of migrating OfflineReplica. When you set it to `true`, PD does not migrate the offline replicas.

- `disable-make-up-replica` is used to disable the feature of making up replicas. When you set it to `true`, PD does not adding replicas for Regions without sufficient replicas.

- `disable-remove-extra-replica` is used to disable the feature of removing extra replicas. When you set it to `true`, PD does not remove extra replicas for Regions with redundant replicas.

- `disable-location-replacement` is used to disable the isolation level check. When you set it to `true`, PD does not improve the isolation level of Region replicas by scheduling.

- `disable-namespace-relocation` is used to disable Region relocation to the store of its namespace. When you set it to `true`, PD does not move Regions to stores where they belong to.

### `config delete namespace <name> [<option>]`

Use this command to delete the configuration of namespace.

Usage:

After you configure the namespace, if you want it to continue to use global configuration, delete the configuration information of the namespace using the following command:

```bash
>> config delete namespace ts1                      // Delete the configuration of the namespace named ts1
```

If you want to use global configuration only for a certain configuration of the namespace, use the following command:

```bash
>> config delete namespace region-schedule-limit ts2 // Delete the region-schedule-limit configuration of the namespace named ts2
```

### `health`

Use this command to view the health information of the cluster.

Usage:

```bash
>> health                                // Display the health information
[
  {
    "name": "pd",
    "member_id": 13195394291058371180,
    "client_urls": [
      "http://127.0.0.1:2379"
      ......
    ],
    "health": true
  }
  ......
]
```

### `hot [read | write | store]`

Use this command to view the hot spot information of the cluster.

Usage:

```bash
>> hot read                             // Display hot spot for the read operation
>> hot write                            // Display hot spot for the write operation
>> hot store                            // Display hot spot for all the read and write operations
```

### `label [store <name> <value>]`

Use this command to view the label information of the cluster.

Usage:

```bash
>> label                                // Display all labels
>> label store zone cn                  // Display all stores including the "zone":"cn" label
```

### `member [delete | leader_priority | leader [show | resign | transfer <member_name>]]`

Use this command to view the PD members, remove a specified member, or configure the priority of leader.

Usage:

```bash
>> member                               // Display the information of all members
{
  "members": [......],
  "leader": {......},
  "etcd_leader": {......},
}
>> member delete name pd2               // Delete "pd2"
Success!
>> member delete id 1319539429105371180 // Delete a node using id
Success!
>> member leader show                   // Display the leader information
{
  "name": "pd",
  "addr": "http://192.168.199.229:2379",
  "id": 9724873857558226554
}
>> member leader resign // Move leader away from the current member
......
>> member leader transfer pd3 // Migrate leader to a specified member
......
```

### `operator [show | add | remove]`

Use this command to view and control the scheduling operation, split a Region, or merge Regions.

Usage:

```bash
>> operator show                                        // Display all operators
>> operator show admin                                  // Display all admin operators
>> operator show leader                                 // Display all leader operators
>> operator show region                                 // Display all Region operators
>> operator add add-peer 1 2                            // Add a replica of Region 1 on store 2
>> operator add remove-peer 1 2                         // Remove a replica of Region 1 on store 2
>> operator add transfer-leader 1 2                     // Schedule the leader of Region 1 to store 2
>> operator add transfer-region 1 2 3 4                 // Schedule Region 1 to stores 2,3,4
>> operator add transfer-peer 1 2 3                     // Schedule the replica of Region 1 on store 2 to store 3
>> operator add merge-region 1 2                        // Merge Region 1 with Region 2
>> operator add split-region 1 --policy=approximate     // Split Region 1 into two Regions in halves, based on approximately estimated value
>> operator add split-region 1 --policy=scan            // Split Region 1 into two Regions in halves, based on accurate scan value
>> operator remove 1                                    // Remove the scheduling operation of Region 1
```

The splitting of Regions starts from the position as close as possible to the middle. You can locate this position using two strategies, namely "scan" and "approximate". The difference between them is that the former determines the middle key by scanning the Region, and the latter obtains the approximate position by checking the statistics recorded in the SST file. Generally, the former is more accurate, while the latter consumes less I/O and can be completed faster.

### `ping`

Use this command to view the time that `ping` PD takes.

Usage:

```bash
>> ping
time: 43.12698ms
```

### `region <region_id> [--jq="<query string>"]`

Use this command to view the region information. For a jq formatted output, see [jq-formatted-json-output-usage](#jq-formatted-json-output-usage).

Usage:

```bash
>> region                               //　Display the information of all regions
{
  "count": 1,
  "regions": [......]
}

>> region 2                             // Display the information of the region with the id of 2
{
  "region": {
      "id": 2,
      ......
  }
  "leader": {
      ......
  }
}
```

### `region key [--format=raw|encode] <key>`

Use this command to query the region that a specific key resides in. It supports the raw and encoding formats. And you need to use single quotes around the key when it is in the encoding format.

Raw format usage (default):

```bash
>> region key abc
{
  "region": {
    "id": 2,
    ......
  }
}
```

Encoding format usage:

```bash
>> region key --format=encode 't\200\000\000\000\000\000\000\377\035_r\200\000\000\000\000\377\017U\320\000\000\000\000\000\372'
{
  "region": {
    "id": 2,
    ......
  }
}
```

### `region sibling <region_id>`

Use this command to check the adjacent Regions of a specific Region.

Usage:

```bash
>> region sibling 2
{
  "count": 2,
  "regions": [......],
}
```

### `region store <store_id>`

Use this command to list all Regions of a specific store.

Usage:

```bash
>> region store 2
{
  "count": 10,
  "regions": [......],
}
```

### `region topread [limit]`

Use this command to list Regions with top read flow. The default value of the limit is 16.

Usage:

```bash
>> region topread
{
  "count": 16,
  "regions": [......],
}
```

### `region topwrite [limit]`

Use this command to list Regions with top write flow. The default value of the limit is 16.

Usage:

```bash
>> region topwrite
{
  "count": 16,
  "regions": [......],
}
```

### `region topconfver [limit]`

Use this command to list Regions with top conf version. The default value of the limit is 16.

Usage:

```bash
>> region topconfver
{
  "count": 16,
  "regions": [......],
}
```

### `region topversion [limit]`

Use this command to list Regions with top version. The default value of the limit is 16.

Usage:

```bash
>> region topversion
{
  "count": 16,
  "regions": [......],
}
```

### `region topsize [limit]`

Use this command to list Regions with top approximate size. The default value of the limit is 16.

Usage:

```bash
>> region topsize
{
   "count": 16,
   "regions": [......],
}

```

### `region check [miss-peer | extra-peer | down-peer | pending-peer | incorrect-ns]`

Use this command to check the Regions in abnormal conditions.

Description of various types:

- miss-peer: the Region without enough replicas
- extra-peer: the Region with extra replicas
- down-peer: the Region in which some replicas are Down
- pending-peer：the Region in which some replicas are Pending
- incorrect-ns：the Region in which some replicas deviate from the namespace constraints

Usage:

```bash
>> region check miss-peer
{
  "count": 2,
  "regions": [......],
}
```

### `scheduler [show | add | remove]`

Use this command to view and control the scheduling strategy.

Usage:

```bash
>> scheduler show                             // Display all schedulers
>> scheduler add grant-leader-scheduler 1     // Schedule all the leaders of the regions on store 1 to store 1
>> scheduler add evict-leader-scheduler 1     // Move all the region leaders on store 1 out
>> scheduler add shuffle-leader-scheduler     // Randomly exchange the leader on different stores
>> scheduler add shuffle-region-scheduler     // Randomly scheduling the regions on different stores
>> scheduler remove grant-leader-scheduler-1  // Remove the corresponding scheduler
```

### `store [delete | label | weight] <store_id>  [--jq="<query string>"]`

Use this command to view the store information or remove a specified store. For a jq formatted output, see [jq-formatted-json-output-usage](#jq-formatted-json-output-usage).

Usage:

```bash
>> store                        // Display information of all stores
{
  "count": 3,
  "stores": [...]
}
>> store 1                      // Get the store with the store id of 1
  ......
>> store delete 1               // Delete the store with the store id of 1
  ......
>> store label 1 zone cn        // Set the value of the label with the "zone" key to "cn" for the store with the store id of 1
>> store weight 1 5 10          // Set the leader weight to 5 and region weight to 10 for the store with the store id of 1
```

### `table_ns [create | add | remove | set_store | rm_store | set_meta | rm_meta]`

Use this command to view the namespace information of the table.

Usage:

```bash
>> table_ns add ts1 1            // Add the table with the table id of 1 to the namespace named ts1
>> table_ns create ts1           // Add the namespace named ts1
>> table_ns remove ts1 1         // Remove the table with the table id of 1 from the namespace named ts1
>> table_ns rm_meta ts1          // Remove the metadata from the namespace named ts1
>> table_ns rm_store 1 ts1       // Remove the table with the store id of 1 from the namespace named ts1
>> table_ns set_meta ts1         // Add the metadata to namespace named ts1
>> table_ns set_store 1 ts1      // Add the table with the store id of 1 to the namespace named ts1
```

### `tso`

Use this command to parse the physical and logical time of TSO.

Usage:

```bash
>> tso 395181938313123110        // Parse TSO
system:  2017-10-09 05:50:59 +0800 CST
logic:  120102
```

## Jq formatted JSON output usage

### Simplify the output of `store`

```bash
» store --jq=".stores[].store | { id, address, state_name}"
{"id":1,"address":"127.0.0.1:20161","state_name":"Up"}
{"id":30,"address":"127.0.0.1:20162","state_name":"Up"}
...
```

### Query the remaining space of the node

```bash
» store --jq=".stores[] | {id: .store.id, available: .status.available}"
{"id":1,"available":"10 GiB"}
{"id":30,"available":"10 GiB"}
...
```

### Query the distribution status of the Region replicas

```bash
» region --jq=".regions[] | {id: .id, peer_stores: [.peers[].store_id]}"
{"id":2,"peer_stores":[1,30,31]}
{"id":4,"peer_stores":[1,31,34]}
...
```

### Filter Regions according to the number of replicas

For example, to filter out all Regions whose number of replicas is not 3:

```bash
» region --jq=".regions[] | {id: .id, peer_stores: [.peers[].store_id] | select(length != 3)}"
{"id":12,"peer_stores":[30,32]}
{"id":2,"peer_stores":[1,30,31,32]}
```

### Filter Regions according to the store ID of replicas

For example, to filter out all Regions that have a replica on store30:

```bash
» region --jq=".regions[] | {id: .id, peer_stores: [.peers[].store_id] | select(any(.==30))}"
{"id":6,"peer_stores":[1,30,31]}
{"id":22,"peer_stores":[1,30,32]}
...
```

You can also find out all Regions that have a replica on store30 or store31 in the same way:

```bash
» region --jq=".regions[] | {id: .id, peer_stores: [.peers[].store_id] | select(any(.==(30,31)))}"
{"id":16,"peer_stores":[1,30,34]}
{"id":28,"peer_stores":[1,30,32]}
{"id":12,"peer_stores":[30,32]}
...
```

### Look for relevant Regions when restoring data

For example, when [store1, store30, store31] is unavailable at its downtime, you can find all Regions whose Down replicas are more than normal replicas:

```bash
» region --jq=".regions[] | {id: .id, peer_stores: [.peers[].store_id] | select(length as $total | map(if .==(1,30,31) then . else empty end) | length>=$total-length) }"
{"id":2,"peer_stores":[1,30,31,32]}
{"id":12,"peer_stores":[30,32]}
{"id":14,"peer_stores":[1,30,32]}
...
```

Or when [store1, store30, store31] fails to start, you can find Regions where the data can be manually removed safely on store1. In this way, you can filter out all Regions that have a replica on store1 but don't have other DownPeers:

```bash
» region --jq=".regions[] | {id: .id, peer_stores: [.peers[].store_id] | select(length>1 and any(.==1) and all(.!=(30,31)))}"
{"id":24,"peer_stores":[1,32,33]}
```

When [store30, store31] is down, find out all Regions that can be safely processed by creating the `remove-peer` Operator, that is, Regions with one and only DownPeer:

```bash
» region --jq=".regions[] | {id: .id, remove_peer: [.peers[].store_id] | select(length>1) | map(if .==(30,31) then . else empty end) | select(length==1)}"
{"id":12,"remove_peer":[30]}
{"id":4,"remove_peer":[31]}
{"id":22,"remove_peer":[30]}
...
```
