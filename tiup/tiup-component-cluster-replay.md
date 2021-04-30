---
title: tiup cluster replay
---

# tiup cluster replay

When you perform operations such as upgrading or restarting the cluster, the operation might accidentally fail due to environmental reasons. If you restart the operation, you need to perform all the steps from the beginning. If the cluster is large, it takes a long time. In this case, you can use the `tiup cluster replay` command to retry the failed commands and skip the steps that already succeeded.

## Syntax

```shell
tiup cluster replay <audit-id> [flags]
```

- `<audit-id>`: the `audit-id` of the command to be retried. You can view the historical commands and their `audit-id`s using the [`tiup cluster audit`](/tiup/tiup-component-cluster-audit.md) command.

## Option

### -h, --help

Prints the help information.

## Output

The output of the command corresponding to `<audit-id>`.
