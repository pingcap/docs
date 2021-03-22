---
title: tiup status
---

# tiup status

The `tiup status` command is used to view the operation information of the components after you run the components using the `tiup [flags] <component> [args...]` command.

> **Note:**
>
> You can only query the information of the following components:
>
> - Components that are still in operation
> - Components that run through the tag specified by `tiup -T/--tag`

## Syntax

```sh
tiup status [flags]
```

## Option

None

## Output

A table consisting of the following fields:

- `Name`: The tag name specified by `-T/--tag`. If not specified, it is a random string.
- `Component`: The operating components.
- `PID`: The corresponding process ID of the operating components.
- `Status`: The status of the operating components.
- `Created Time`: The starting time of the components.
- `Directory`: The data directory of the components.
- `Binary`: The binary file path of the components.
- `Args`: The starting arguments of the operating components.
