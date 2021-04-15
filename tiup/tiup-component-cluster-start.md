---
title: tiup cluster start
---

# tiup cluster start

The `tiup cluster start` command is used to start all services or some services of the specified cluster.

## Syntax

```shell
tiup cluster start <cluster-name> [flags]
```

`<cluster-name>` is the name of the cluster to operate on. If you forget the cluster name, check it with the [cluster list](/tiup/tiup-component-cluster-list.md) command.

## Options

### -N, --node

- Specifies the nodes to be started. If not specified, all nodes are started. The value of this option is a comma-separated list of node IDs. The node ID is the first column of the [cluster status](/tiup/tiup-component-cluster-display.md) table.
- Data type: `STRING`
- Default: `[]`. If this option is not specified in the command, all nodes are started.

> **Note:**
>
> If the `-R, --role` option is specified at the same time, then the services in their intersection are started.

### -R, --role

- Specifies the roles to be started. If not specified, all roles are started. The value of this option is a comma-separated list of node roles. The role is the second column of the [cluster status](/tiup/tiup-component-cluster-display.md) table.
- Data type: `STRING`
- Default: `[]`.  If this option is not specified in the command, all roles are started.

> **Note:**
>
> If the `-N, --node` option is specified at the same time, the services in their intersection are started.

### -h, --help

- Prints the help information.
- Data type: `BOOLEAN`
- This option is disabled by default with the `false` value. To enable this option, add this option to the command, and either pass the `true` value or do not pass any value.

## Output

The log of starting the service.
