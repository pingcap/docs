---
title: Scaling a TiDB Cluster
category: deployment
---

# Scaling a TiDB Cluster

## Overview

The capacity of a TiDB cluster can be incresead or reduced without affecting online services.

The following part shows you how to add or delete PD, TiKV or TiDB nodes.

About pd-ctl usage, please refer to [pd-control](./pd-control.md).

## PD

Assume we have three PD servers with the following details:

|Name|ClientUrls|PeerUrls|
|----|----------|--------|
|pd1|http://host1:2379|http://host1:2380|
|pd2|http://host2:2379|http://host2:2380|
|pd3|http://host3:2379|http://host3:2380|

Get the information about the existing PD nodes through pd-ctl:

```bash
./pd-ctl -u http://host1:2379
>> member
```

### Add a node dynamically

Add a new PD server to the current PD cluster by using the parameter `join`.
To add `pd4`, you just need to specify the client url of any PD server in the PD cluster in the parameter `--join`, like:

```bash
./bin/pd-server --name=pd4 \
                --client-urls="http://host4:2379" \
                --peer-urls="http://host4:2380" \
                --join="http://host1:2379"
```

### Delete a node dynamically

Delete `pd4` through pd-ctl:

```bash
./pd-ctl -u http://host1:2379
>> member delete pd4
```

### Migrate a node dynamically
If you want to migrate a node to a new machine, you need to, first of all, add a node on the new machine and then delete the node on the old machine.
As you can just migrate one node at a time, if you want to migrate multiple nodes, you need to repeat the above steps until you have migrated all nodes. After completing each step, you can verify the process by checking the information of all nodes.

## TiKV

Get the information about the existing TiKV nodes through pd-ctl:

```bash
./pd-ctl -u http://host1:2379
>> store
```

### Add a node dynamically

It is very easy to add a new TiKV server dynamically. You just need to start a TiKV server on the new machine.
The newly started TiKV server will automatically register in the existing PD of the cluster. To reduce the pressure of the existing TiKV servers, PD loads balance automatically, which means PD gradually migrates some data to the new TiKV server.

## Delete a node dynamically

To delete (make it offline) a TiKV server safely, you need to inform PD in advance. After that, PD is able to migrate the data on this TiKV server to other TiKV servers, ensuring that data have enough replicas.

Assume that you need to delete the TiKV server with a store id 1, you can complete this through pd-ctl:

```bash
./pd-ctl -u http://host1:2379
>> store delete 1
```

Then you can check the state of this TiKV:

```bash
./pd-ctl -u http://host1:2379
>> store 1
{
  "stores": {
    "id": 1,
    "state": 1,
  }
}
```

You can verify the state of this store through the following information:
- `state=0`: this store is in service
- `state=1`: this store is in the process of offline, but the store is still in service
- `state=2`: this store has completed the process of offline and there are no data on it, so the instance can be shut down

## Migrate a node dynamically

To migrate TiKV servers to a new machine, you also need to add nodes on the new machine and then make all nodes on the old machine offline.
In the process of migration, you can add all machines in the new cluster to the existing cluster, then make old nodes offline one by one.
To verify whether a node has been made offline, you can check the state information of the node in process. After verifying, you can make the next node offline.

### TiDB

TiDB is a stateless server, which means it can be added or deleted directly.
It should be noted that if you deploy a proxy (such as HAProxy) in front of TiDB, you need to update the proxy configuration and reload it.
