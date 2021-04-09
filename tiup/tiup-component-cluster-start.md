<<<<<<< Updated upstream
---
title: tiup cluster start
---
=======
--
title: tiup cluster start
--
>>>>>>> Stashed changes

# tiup cluster start

The `tiup cluster start` command is used to start all services or some services of the specified cluster.

## Syntax

```sh
tiup cluster start <cluster-name> [flags]
```

<<<<<<< Updated upstream
``<cluster-name>` is the name of the cluster to operate on. If you forget the cluster name, check it in [tiup cluster list](/tiup/tiup-component-cluster-list.md).

## Options

### -N, --node

Specifies the IDs of the nodes to start, splitting by commas if starting multiple nodes. The node IDs are in the first column of the [tiup cluster display](/tiup/tiup-component-cluster-display.md) table.
Data type: `STRING`
Default: []. If this option is not specified in the command, the command starts all the nodes.

> **Note:**
> 
> If `-R, --role` is also specified, only the services in the intersection of the specified nodes and roles will be started.

### -R, --role strings

Specifies the roles to be started, splitting by commas if starting multiple roles. The roles are in the second column of the [tiup cluster display](/tiup/tiup-component-cluster-display.md) table.
Data type: `STRING`
Default: []. If this option is not specified in the command, the command starts all the roles.

> **Note:**
> 
> If `-N, --node` is also specified, only the services in the intersection of the specified nodes and roles will be started.

### -h, --help

- Prints the help information.
- Data type: `BOOLEAN`
- This option is disabled by default with the `false` value. To enable this option, add this option to the command, and either pass the `true` value or do not pass any value.

## Output

The output contains the starting logs.
=======
``<cluster-name>` is the name of the cluster to be operated on. If you forget the cluster name, check it in [tiup cluster list](/tiup/tiup-component-cluster-list.md).

## Options

### -N, --node (strings, default is [] for all nodes)

Specifies the nodes to start, or all nodes if not specified. The value of this option is a comma-separated list of node IDs, with the node IDs being the first column of the [cluster status](/tiup/tiup-component-cluster-display.md) table.

> **Note:**
> 
> If `-R, --role` is also specified, then the services in their intersection will be started.

### -R, --role strings (strings, default [], means all roles)

Specify the roles to be started, or all roles if not specified. The value of this option is a comma-separated list of node roles, with the roles being the second column of the [cluster status](/tiup/tiup-component-cluster-display.md) table.

> **Note:**
> 
> If `-N, --node` is also specified, then the services in their intersection will be started.

### -h, --help (boolean, default false)

Output help information.

## Output

Start log.
>>>>>>> Stashed changes
