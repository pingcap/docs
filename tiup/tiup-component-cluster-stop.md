---
title: tiup cluster stop
---

# tiup cluster stop

The `tiup cluster stop` command is used to stop all services or some services of the specified cluster.

> **Note:**
> 
> If the core services of a cluster are stopped, the cluster cannot provide services anymore.

## Syntax

```sh
tiup cluster stop <cluster-name> [flags]
```

``<cluster-name>` is the name of the cluster to operate on. If you forget the cluster name, check it in [tiup cluster list](/tiup/tiup-component-cluster-list.md).

## Options

### -N, --node

Specifies the IDs of the nodes to stop, splitting by commas for multiple nodes. The node IDs are in the first column of the [tiup cluster display](/tiup/tiup-component-cluster-display.md) table.
Data type: `STRING`
Default: []. If this option is not specified in the command, the command stops all the nodes.

> **Note:**
> 
> If `-R, --role` is also specified, only the services in the intersection of the specified nodes and roles are stopped.

### -R, --role strings

Specifies the roles to stop, splitting by commas for multiple roles. The roles are in the second column of the [tiup cluster display](/tiup/tiup-component-cluster-display.md) table.
Data type: `STRING`
Default: []. If this option is not specified in the command, the command stops all the roles.

> **Note:**
> 
> If `-N, --node` is also specified, only the services in the intersection of the specified nodes and roles are stopped.

### -h, --help

- Prints the help information.
- Data type: `BOOLEAN`
- This option is disabled by default with the `false` value. To enable this option, add this option to the command, and either pass the `true` value or do not pass any value.

## Output

The output contains the stopping logs.
