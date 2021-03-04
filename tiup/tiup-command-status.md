---
title: tiup status
---

# tiup status

The command `tiup status` is used to view the running information of the components. After running the components with the command `tiup [flags] <component> [args...]`, you can view the running information of the components.

> **Note:**
>
> You can only query the information of the following components:
>
> - Running components
> - Components that run through the tag specified by `tiup -T/--tag`

## Syntax

```sh
tiup status [flags]
```

## Option

None

## Output

A table consisting of the following fields:

- Name: the tag name specified by `-T/--tag`. If not specified, it is a random string.
- Component: running components
- PID: corresponding process ID
- Status: running status of components
- Created Time: start time
- Directory: data directory
- Binary: binary file path
- Args: startup parameters