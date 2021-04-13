---
title: tiup dm prune
---

# tiup dm prune

When [scaling in the cluster](/tiup/tiup-component-dm-scale-in.md), a small amount of meta-information in etcd is not cleaned up, and usually causes no problem. If you really need to clean the meta-information up, you can manually execute the `tiup cluster prune` command.

## Syntax

```shell
tiup dm prune <cluster-name> [flags]
```

## Option

### -h, --help

- Prints the help information.
- Data type: `BOOLEAN`
- Default: false

## Output

The log of the cleanup process.
