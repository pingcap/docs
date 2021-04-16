---
title: tiup dm upgrade
---

# tiup dm upgrade

The `tiup dm upgrade` command is used to upgrade a specified cluster to a specific version.

## Syntax 

```shell
tiup dm upgrade <cluster-name> <version> [flags]
```

- `<cluster-name>` is the name of the cluster to be operated on. If you forget the cluster name, you can use the `[tiup dm list](/tiup/tiup-component-dm-list.md)` command to check it.
- `<version>` is the target version to be upgraded to. Currently, only upgrading to a later version is allowed, and upgrading to an earlier version is not allowed, which means the downgrade is not allowed. Upgrading to a nightly version is not allowed either.

## Options

### -h, --help

- Prints the help information.
- Data type: `BOOLEAN`
- This option is disabled by default with the `false` value. To enable this option, add this option to the command, and either pass the `true` value or do not pass any value.

## Output

Log of the service upgrade process.
