---
title: PD Control User Guide
category: tools
---

# PD Control User Guide

As a command line tool of PD, PD Control obtains the state information of the cluster and tunes the cluster.

## Source code compiling

1. [Go](https://golang.org/) Version 1.7 or later
2. In the PD root directory, use the `make` command to compile and generate `bin/pd-ctl`

> **Note:** Generally, you don't need to compile source code as the PD Control tool already exists in the released Binary or Docker. However, dev users can refer to the above instruction for compiling source code.

## Usage

Single-command mode:

    ./pd-ctl store -d -u http://127.0.0.1:2379

Interactive mode:

    ./pd-ctl -u http://127.0.0.1:2379

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

### \-\-pd,-u

+ PD address
+ Default address: http://127.0.0.1:2379
+ Enviroment variable: PD_ADDR

### \-\-detach,-d

+ Use single command line mode (not entering readline)
+ Default: false

### --cacert

+ Specify the path to the certificate file of the trusted CA in PEM format
+ Default: ""

### --cert

+ Specify the path to the certificate of SSL in PEM format
+ Default: ""

### --key

+ Specify the path to the certificate key file of SSL in PEM format, which is the private key of the certificate specified by `--cert`
+ Default: ""

### --version,-V

+ Print the version information and exit
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

### `config [show | set \<option\> \<value\>]`

Use this command to view or modify the configuration information.

Usage:

```bash
>> config show                                //　Display the config information of the scheduler
{
  "max-snapshot-count": 3,
  "max-pending-peer-count": 16,
  "max-store-down-time": "1h0m0s",
  "leader-schedule-limit": 64,
  "region-schedule-limit": 16,
  "replica-schedule-limit": 24,
  "tolerant-size-ratio": 2.5,
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
  "leader-schedule-limit": 64,
  "region-schedule-limit": 16,
  "replica-schedule-limit": 24,
  "max-replicas": 3,
}
>> config show replication                    // Display the config information of replication
{
  "max-replicas": 3,
  "location-labels": ""
}
```

- `leader-schedule-limit` controls the number of tasks scheduling the leader at the same time. This value affects the speed of leader balance. A larger value means a higher speed and setting the value to 0 closes the scheduling. Usually the leader scheduling has a small load, and you can increase the value in need.
    
    ```bash
    >> config set leader-schedule-limit 4         // 4 tasks of leader scheduling at the same time at most
    ```

- `region-schedule-limit` controls the number of tasks scheduling the region at the same time. This value affects the speed of region balance. A larger value means a higher speed and setting the value to 0 closes the scheduling. Usually the region scheduling has a large load, so do not set a too large value.
    
    ```bash
    >> config set region-schedule-limit 2         // 2 tasks of region scheduling at the same time at most
    ```

- `replica-schedule-limit` controls the number of tasks scheduling the replica at the same time. This value affects the scheduling speed when the node is down or removed. A larger value means a higher speed and setting the value to 0 closes the scheduling. Usually the replica scheduling has a large load, so do not set a too large value.

    ```bash
    >> config set replica-schedule-limit 4        // 4 tasks of replica scheduling at the same time at most
    ```

The configuration above is global. You can also tune the configuration by configuring different namespaces. The global configuration is used if the corresponding configuration of the namespace is not set.

> **Note:** The configuration of the namespace only supports editing `leader-schedule-limit`, `region-schedule-limit`, `replica-schedule-limit` and `max-replicas`.

    ```bash
    >> config set namespace ts1 leader-schedule-limit 4 // 4 tasks of leader scheduling at the same time at most for the namespace named ts1
    >> config set namespace ts2 region-schedule-limit 2 // 2 tasks of region scheduling at the same time at most for the namespace named ts2
    ```

### `config delete namespace \<name\> [\<option\>]`

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
{"health": "true"}
```

### `hot [read | write | store]`

Use this command to view the hot spot information of the cluster.

Usage:

```bash
>> hot read                             // Display hot spot for the read operation
>> hot write                            // Display hot spot for the write operation
>> hot store                            // Display hot spot for all the read and write operations
```

### `label [store]`

Use this command to view the label information of the cluster.

Usage:

```bash
>> label                                // Display all labels
>> label store zone cn                  // Display all stores including the "zone":"cn" label
```

### `member [leader | delete]`

Use this command to view the PD members or remove a specified member.

Usage:

```bash
>> member                               // Display the information of all members
{
  "members": [......]
}
>> member leader show                   // Display the information of the leader
{
  "name": "pd",
  "addr": "http://192.168.199.229:2379",
  "id": 9724873857558226554
}
>> member delete name pd2               // Delete "pd2"
Success!
>> member delete id 1319539429105371180 // Delete a node using id
Success!
```

### `operator [show | add | remove]`

Use this command to view and control the scheduling operation.

Usage:

```bash
>> operator show                            // Display all operators
>> operator show admin                      // Display all admin operators
>> operator show leader                     // Display all leader operators
>> operator show region                     // Display all region operators
>> operator add add-peer 1 2                // Add a replica of region 1 on store 2
>> operator remove remove-peer 1 2          // Remove a replica of region 1 on store 2
>> operator add transfer-leader 1 2         // Schedule the leader of region 1 to store 2
>> operator add transfer-region 1 2 3 4     // Schedule region 1 to store 2,3,4
>> operator add transfer-peer 1 2 3         // Schedule the replica of region 1 on store 2 to store 3
>> operator remove 1                        // Remove the scheduling operation of region 1
```

### `ping`

Use this command to view the time that `ping` PD takes.

Usage:

```bash
>> ping
time: 43.12698ms
```

### `region \<region_id\> [--jq="<query string>"]`

Use this command to view the region information. For a jq formatted output, see [jq-formatted-json-output-usage] (#jq-formatted-json-output-usage).

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

### `region key [--format=raw|pb|proto|protobuf] \<key\>`

Use this command to query the region that a specific key resides in. It supports the raw and protobuf formats.

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

Protobuf format usage:

```bash
>> region key --format=pb t\200\000\000\000\000\000\000\377\035_r\200\000\000\000\000\377\017U\320\000\000\000\000\000\372
{
  "region": {
    "id": 2,
    ......
  }
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

### `store [delete | label | weight] \<store_id\>  [--jq="<query string>"]`

Use this command to view the store information or remove a specified store. For a jq formatted output, see [jq-formatted-json-output-usage] (#jq-formatted-json-output-usage).

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

## Jq formatted json output usage

### Simplify the output of `store`

```bash
» store --jq=".stores[].store | { id, address, state_name}"
{"id":1,"address":"127.0.0.1:20161","state_name":"Up"}
{"id":30,"address":"127.0.0.1:20162","state_name":"Up"}
...
```

### Query the remaining space of the node

```bash
» store --jq=".stores[] | {id: .store.id, avaiable: .status.available}"
{"id":1,"avaiable":"10 GiB"}
{"id":30,"avaiable":"10 GiB"}
...
```

### Query the distribution status of the Region copies

```bash
» region --jq=".regions[] | {id: .id, peer_stores: [.peers[].store_id]}"
{"id":2,"peer_stores":[1,30,31]}
{"id":4,"peer_stores":[1,31,34]}
...
```

### Filter Regions according to the number of copies

For example, to filter out all Regions whose number of copies is not 3:

```bash
» region --jq=".regions[] | {id: .id, peer_stores: [.peers[].store_id] | select(length != 3)}"
{"id":12,"peer_stores":[30,32]}
{"id":2,"peer_stores":[1,30,31,32]}
```

### Filter Regions according to the store ID of copies

For example,to filter out all Regions that have a replica on store30:

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

For example, when [store1, store30, store31] is unavailable at its downtime, you can find all Regions whose Down copies are more than normal copies:

```bash
» region --jq=".regions[] | {id: .id, peer_stores: [.peers[].store_id] | select(length as $total | map(if .==(1,30,31) then . else empty end) | length>=$total-length) }"
{"id":2,"peer_stores":[1,30,31,32]}
{"id":12,"peer_stores":[30,32]}
{"id":14,"peer_stores":[1,30,32]}
...
```

Or when [store1, store30, store31] fails to start, you can find Regions that can manually remove data without risks on store1. In this way, you can filter out all Regions that have a replica on store1 but don't have other DownPeers:

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
