---
title: tiup dm upgrade
summary: The `tiup dm upgrade` command upgrades a specified cluster to a specific version. It requires the cluster name and target version as parameters. The `--offline` option allows for offline upgrades, and the `-h, --help` option prints help information. The output is a log of the service upgrade process.
---

# tiup dm upgrade

The `tiup dm upgrade` command is used to upgrade a specified cluster to a specific version.

## Syntax

```shell
tiup dm upgrade <cluster-name> <version> [flags]
```

- `<cluster-name>` is the name of the cluster to be operated on. If you forget the cluster name, you can check it using the [`tiup dm list`](/tiup/tiup-component-dm-list.md) command.
- `<version>` is the target version to be upgraded to, such as `v8.1.0`. Currently, only upgrading to a later version is allowed, and upgrading to an earlier version is not allowed, which means the downgrade is not allowed. Upgrading to a nightly version is not allowed either.

## Options

### --offline

- Declares that the current cluster is offline. When this option is specified, TiUP DM only replaces the binary files of the cluster components in place without restarting the service.

### -h, --help

- Prints the help information.
- Data type: `BOOLEAN`
- This option is disabled by default with the `false` value. To enable this option, add this option to the command, and either pass the `true` value or do not pass any value.

## Output

Log of the service upgrade process.

[<< Back to the previous page - TiUP DM command list](/tiup/tiup-component-dm.md#command-list)
