---
title: tiup mirror modify
---

# tiup mirror modify

The `tiup mirror modify` command is used to modify published components. Only authorized component owners can modify components, and only modify their own published components. For the component publishing method, refer to the [`publish` command](/tiup/tiup-command-mirror-publish.md).

## Syntax

```shell
tiup mirror modify <component>[:version] [flags]
```

Each parameter is explained as follows:

- `<component>`: the component name
- `[version]`: the version you want to modify. If not specified, the entire component is modified.

## Options

### -k, --key

- Specifies the location of the private key used for signing the `{component}.json` files.
- Data type: `STRING`
- Default: "${TIUP_HOME}/keys/private.json"

### --yank

Mark the specified component or version as unavailable.

- After marking the component as unavailable, the component cannot be seen in the  `tiup list`, nor can the new version of the component be installed.
- After marking the component as unavailable, the version cannot be seen in the `tiup list <component>`, nor can this version be installed.
- Data type: `BOOLEAN`
- Default: false

### --hide

- Specifies whether the component is hidden. If it is a hidden component, it can be seen in the result list of `tiup list -all`, but not in that of `tiup list`.
- Data type: `STRING`
- Default: NULL

> **Note:**
>
> This option can only be applied to the component, not to the version of the component.

### --standalone

- Controls whether the component can run standalone. This option is currently **NOT available**.
- Data type: `BOOLEAN`
- Default: false

> **Note:**
>
> This option can only be applied to the component, not to the version of the component.

## Outputs

- If the command is executed successfully, there is no output.
- If the component owner is not authorized to modify the target component:
    - If the mirror is a remote mirror, TiUP reports the error `Error: The server refused, make sure you have access to this component`.
    - If the mirror is a local mirror, TiUP reports the error `Error: the signature is not correct`.