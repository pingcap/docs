---
title: tiup cluster replay
summary: The `tiup cluster replay` command allows you to retry failed cluster operations and skip successfully performed steps. Use `tiup cluster replay <audit-id>` to retry the command with the specified audit ID. View audit IDs with `tiup cluster audit` command. The output is the result of the specified audit ID.
---

# tiup cluster replay

When you perform a cluster operation such as upgrade or restart, the operation might fail due to cluster environment issues. If you re-perform the operation, you need to perform all the steps from the very beginning. If the cluster is large, re-performing these steps will take a long time. In this case, you can use the `tiup cluster replay` command to retry the failed commands and skip the successfully performed steps.

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
