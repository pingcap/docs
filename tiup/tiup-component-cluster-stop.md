---
title: tiup cluster stop
summary: The "tiup cluster stop" command is used to stop all or some services of a specified cluster. If the core services are stopped, the cluster cannot provide services anymore. The command syntax is "tiup cluster stop <cluster-name> [flags]". Options include -N/--node to specify nodes to be stopped, -R/--role to specify roles of nodes to be stopped, and -h/--help to print help information. The output is the log of stopping the service.
---

# tiup cluster stop

The `tiup cluster stop` command is used to stop all services or some services of the specified cluster.

> **Note:**
>
> If the core services of a cluster are stopped, the cluster cannot provide services anymore.

## Syntax

```shell
tiup cluster stop <cluster-name> [flags]
```

`<cluster-name>` is the name of the cluster to operate on. If you forget the cluster name, you can check it using the [`tiup cluster list`](/tiup/tiup-component-cluster-list.md) command.

## Options

### -N, --node

- Specifies the nodes to be stopped. The value of this option is a comma-separated list of node IDs. You can get the node IDs from the first column of the [cluster status table](/tiup/tiup-component-cluster-display.md) returned by the `tiup cluster display` command.
- Data type: `STRINGS`
- If this option is not specified in the command, the command stops all the nodes by default.

> **Note:**
>
> If the `-R, --role` option is specified at the same time, only the service nodes that match both the specifications of `-N, --node` and `-R, --role` are stopped.

### -R, --role

- Specifies the roles of nodes to be stopped. The value of this option is a comma-separated list of the roles of the nodes. You can get the roles of the nodes from the second column of the [cluster status table](/tiup/tiup-component-cluster-display.md) returned by the `tiup cluster display` command.
- Data type: `STRINGS`
- If this option is not specified in the command, the command stops all the roles by default.

> **Note:**
>
> If the `-N, --node` option is specified at the same time, only the service nodes that match both the specifications of `-N, --node` and `-R, --role` are stopped.

### -h, --help

- Prints the help information.
- Data type: `BOOLEAN`
- This option is disabled by default with the `false` value. To enable this option, add this option to the command, and either pass the `true` value or do not pass any value.

## Output

The log of stopping the service.

## See also

- [TiUP Common Operations](/maintain-tidb-using-tiup.md)