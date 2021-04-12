---
title: tiup mirror merge
---

# tiup mirror merge

The `tiup mirror merge` command is used to merge one or more mirrors to the current mirror.

To execute this command, you need to meet the following conditions:

-The owner IDs of all components of the target mirror must exist in the current mirror.
-The user's `${TIUP_HOME}/keys` directory has all the private keys corresponding to the above owner ID in the current mirror (you can use the command [`tiup mirror set`](/tiup/tiup-command-mirror-set.md) to switch the current mirror to the mirror that is currently authorized to modify).

## Syntax

```shell
tiup mirror merge <mirror-dir-1> [mirror-dir-N] [flags]
```

- `<mirror-dir-1>`: the first mirror to be merged into the current mirror
- `[mirror-dir-N]`: the Nth mirror to be merged into the current mirror

## Option

None

## Outputs

- If the command is executed successfully, there is no output.
- If the current mirror is missing the component owner of the target mirror, or `${TIUP_HOME}/keys` is missing the administrator's private key, TiUP reports the `Error: missing owner keys for owner %s on component %s` error.