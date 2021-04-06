---
title: tiup cluster prune
---

# tiup cluster prune

When [scaling in the cluster](/tiup/tiup-component-cluster-scale-in.md), for some components, the service is not immediately stopped and the data is deleted, but you need to wait for the data scheduling to complete and then manually execute the `tiup cluster prune` command to clean up.

## Syntax

```shell
tiup cluster prune <cluster-name> [flags]
```

## Option

### -h, --help

- Prints the help information.
- Data type: `BOOLEAN`
- Default: false

## Output

The log of the cleanup process.