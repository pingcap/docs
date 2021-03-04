---
title: tiup clean
---

# tiup clean

The command `tiup clean` is used to clean the data generated during component operation.

## Syntax

```sh
tiup clean [name] [flags]
```

The value of `[name]` is the `Name` field output by [status command](/tiup/tiup-command-status.md). If you omit the `[name]`, it must be used with `--all`.

## Option

### --all

- Data type: Boolean
- Default: false

Clean all running records.

## Output

```
Clean instance of `%s`, directory: %s
```