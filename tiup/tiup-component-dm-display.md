---
title: tiup dm display
---

# tiup dm display

If you want to check the operational status of each component in a cluster, it is inefficient to log in to each machine one by one. Therefore, tiup-dm provides the `tiup dm display` command to do this job efficiently.

## Syntax

```shell
tiup dm display <cluster-name> [flags]
```

`<cluster-name>` is the name of the cluster to operate on. If you forget the cluster name, check it in [tiup cluster list](/tiup/tiup-component-cluster-list.md).

## Options

### -N, --node

Specifies the IDs of the nodes to query, splitting by commas for multiple nodes. The node IDs are in the first column of the [tiup cluster display](/tiup/tiup-component-cluster-display.md) table.
Data type: `STRING`
Default: []. If this option is not specified in the command, the command queries all the nodes.

> **Note:**
> 
> If `-R, --role` is also specified, only the services in the intersection of the specified nodes and roles will be queried.

### -R, --role strings

Specifies the roles to be queried, splitting by commas for multiple roles. The roles are in the second column of the [tiup cluster display](/tiup/tiup-component-cluster-display.md) table.
Data type: `STRING`
Default: []. If this option is not specified in the command, the command queries all the roles.

> **Note:**
> 
> If `-N, --node` is also specified, only the services in the intersection of the specified nodes and roles will be queried.

### -h, --help

- Prints the help information.
- Data type: `BOOLEAN`
- This option is disabled by default with the `false` value. To enable this option, add this option to the command, and either pass the `true` value or do not pass any value.

## Output

- Cluster name
- Cluster version
- SSH client type
- A table containing the following fields:
    - `ID`: Node ID, consisting of IP:PORT.
    - `Role`: the service role deployed on the node (for example, TiDB or TiKV).
    - `Host`: IP address of the machine corresponding to the node.
    - `Ports`: the port number used by the service.
    - `OS/Arch`: the operating system and machine architecture of the node.
    - `Status`: the current status of the services on the node.
    - `Data Dir`: the data directory of the service. `-` means that there is no data directory.
    - `Deploy Dir`: the deployment directory of the service.
