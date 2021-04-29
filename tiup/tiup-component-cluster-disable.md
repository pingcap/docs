---
title: tiup cluster disable
---

# tiup cluster disable

The `tiup cluster disable` command is used to disable the auto-enabling after restarting the machine where the cluster service is located. This command executes the `systemctl disable <service>` on the specified node to disable the auto-enabling of the service.

## Syntax

```shell
tiup cluster disable <cluster-name> [flags]
```

`<cluster-name>`: the cluster whose auto-enabling service is to be disabled.

## Options

### -N, --node

- Specifies the nodes whose auto-enabling service is to be disabled. The value of this option is a comma-separated list of node IDs. The node ID is the first column of the cluster status table returned by the [`tiup cluster display`](/tiup/tiup-component-cluster-display.md) command.
- Data type: `STRINGS`
- If this option is not specified in the command, the auto-enabling of all nodes is disabled by default.

> **Note:**
>
> If the `-R, --role` option is specified at the same time, the auto-enabling of services in their intersection is disabled.

### -R, --role

- Specifies the roles whose auto-enabling service is to be disabled. The value of this option is a comma-separated list of node roles. The role is the second column of the cluster status table returned by the [`tiup cluster display`](/tiup/tiup-component-cluster-display.md) command.
- Data type: `STRINGS`
- If this option is not specified in the command, the auto-enabling of all roles is disabled by default.

> **Note:**
>
> If the `-N, --node` option is specified at the same time, the auto-enabling of services in their intersection is disabled.

### -h, --help

- Prints the help information.
- Data type: `BOOLEAN`
- This option is disabled by default and its default value is `false`. To enable this option, you can add this option to the command, and pass the `true` value or do not pass any value.

## Output

The execution log of the tiup-cluster.
