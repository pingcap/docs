---
title: tiup cluster scale-in
---

# tiup cluster scale-in

The `tiup cluster scale-in` command is used to scale down the cluster, which takes the services of the specified nodes offline, removes the specified nodes from the cluster, and deletes the remaining files from those nodes.

Because the TiKV, TiFlash and TiDB Binlog components are taken to offline asynchronously (the removal needs to be executed by the API first) and the stopping process takes a long time (the command needs to keep checking whether the specified nodes have been successfully stopped), the `tiup cluster scale-in` command handles the TiKV, TiFlash and TiDB Binlog components particularly as follows:

- For TiKV, TiFlash and TiDB Binlog components, the `tiup cluster scale-in` command makes the following operations:

  - Exit tiup-cluster directly after it is stopped by the API without waiting for the entire stopping process to be completed.
  - Execute the `tiup cluster display` command to check the status of the nodes being scaled down and wait for the status to change to `Tombstone`.
  - Execute the `tiup cluster prune` command to clean up the nodes in the `Tombstone` status, which performs the following operations:

        - Stop the services of the nodes that have been taken offline.
        - Clean up the data files of the nodes that have been taken offline.
        - Update the cluster topology and remove the nodes that have been taken offline.

- For other components, the `tiup cluster scale-in` command makes the following operations:

  - To take the PD nodes offline, the command uses the API to remove the specified PD nodes from the cluster (this process is fast), stops the services of the specified PD nodes, and then cleans up the data files of the specified PD nodes.
  - To take other components offline, the command stops the nodes and cleans up the related data files directly.

## Syntax

```sh
tiup cluster scale-in <cluster-name> [flags]
```

`<cluster-name>` is the name of the cluster to be scaled down. If you forget the cluster name, check the name in [tiup cluster list](/tiup/tiup-component-cluster-list.md).

## Options

### -N, --node

- Specifies the nodes to be scaled down, split by commas if scaling multiple nodes.
- Data type: `STRING`
- There is no default value. This option is mandatory and the value must be not null.

### --force

- Controls whether to forcibly remove the specified nodes from the cluster. In some cases, it is possible that the host of the node to be scaled down is down, making it impossible to connect to the node via SSH for operations, so you can forcibly remove the node from the cluster using the `-force` option.
- Data type: `BOOLEAN`
- Default: false. If this option is not specified in the command, the specified nodes are not forcibly removed.

> **Note:**
>
> Because the forced removal of a TiKV node does not wait for data to be scheduled, removing more than one serving TiKV node is in the risk of data loss.

### --transfer-timeout

- When a PD or TiKV node is to be scaled down, the leader role of the node will be migrated to other nodes first. Because the migration process takes some time, you can set the maximum waiting time (in seconds) by configuring `-transfer-timeout`. After the timeout, the `tiup cluster scale-in` command skips waiting and starts the scaling down directly.
- Data type: `UINT`
- If this option is not specified in the command, the default waiting time of leader migration is `300` seconds.

> **Note:**
>
> If a PD or TiKV node is scaled down directly without waiting for the leader role migration to be completed, the service performance may jitter.

### -h, --help

- Shows the help information in the output.
- Data type: `BOOLEAN`
- Default: false

## Output

Shows the logs of the scaling down process.
