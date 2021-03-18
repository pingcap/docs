---
title: tiup update
---

# tiup update

The `tiup update` command is used to update the installed components or itself.

## Syntax

```sh
tiup update [component1][:version] [component2..N] [flags]
```

- `[component1]`: the name of the component to update.
- `[version]`: the version to update. If omitted, it means updating to the latest stable version of the component.
- `[component2...N]`: specifies updating multiple components or versions. If no component is specified, which means `[component1][:version] [component2..N]` is empty, you need to use the `--all` or the `--self` option together.

The update operation does not delete the old version. You can still specify using the old version during execution.

## Options

### --all

If no component is specified, this option must be specified.

- Data type: `BOOLEAN`
- Default: `false`

### --force

If the version of the specified component is already installed, the update operation is skipped by default. Specifying this option forcibly updates the installed version.

- Data type: `BOOLEAN`
- Default: `false`

### --nightly

Updates the specified components to the nightly version. The command using this option is equivalent to the `tiup update <component>:nightly` command.

- Data type: `BOOLEAN`
- Default: `false`

### --self

Updates TiUP itself.

- Data type: `BOOLEAN`
- Default: `false`

## Outputs

- If updates successfully, output `Updated successfully!`.
- If target version does not exist, the `Error: version %s not supported by component %s` error is reported.