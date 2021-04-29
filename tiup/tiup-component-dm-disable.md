---
title: tiup dm disable
---

# tiup dm disable

The `tiup dm disable` command is used to disable the auto-enabling after restarting the machine where the cluster service is located. This command executes the `systemctl disable <service>` on the specified node to disable the auto-enabling of the service.

## Syntax

```shell
tiup dm disable <cluster-name> [flags]
```

`<cluster-name>`: the cluster whose auto-enabling service is to be disabled.

## Options

### -N, --node

- Specifies the nodes whose service auto-enabling is to be disabled. The value of this option is a comma-separated list of node IDs. You can get the node IDs from the first column of the cluster status table returned by the [`tiup-component-dm-display`](/tiup/tiup-component-dm-display.md) command.
- Data type: `STRINGS`
- If this option is not specified in the command, the auto-enabling of all nodes is disabled by default.

> **Note:**
>
> If the `-R, --role` option is specified at the same time, the auto-enabling of services in their intersection is disabled.

### -R, --role

- Specifies the roles whose service auto-enabling is to be disabled. The value of this option is a comma-separated list of node roles. You can get the roles of nodes from the second column of the cluster status table returned by the [`tiup-component-dm-display`](/tiup/tiup-component-dm-display.md) command.
- Data type: `STRINGS`
- If this option is not specified in the command, the auto-enabling of all roles is disabled by default.

> **Note:**
>
> If the `-N, --node` option is specified at the same time, the auto-enabling of services in their intersection is disabled.

### -h, --help

Prints the help information.

## Output

The execution log of the tiup-dm.