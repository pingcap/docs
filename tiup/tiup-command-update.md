---
title: tiup update
---

# tiup update

The `tiup update` command is used to upgrade the installed components or itself.

## Syntax

```sh
tiup update [component1][:version] [component2..N] [flags]
```

- `[component1]`: The name of the component to be upgraded.
- `[version]`: The version to be uninstalled. If omitted, it means upgrading to the latest stable version of the component.
- `[component2...N]`: Specifies upgrading multiple components or versions. If no component is specified, which means `[component1][:version] [component2..N]` is empty, you need to use the `--all` or the `--self` option together.

The upgrade operation does not delete the old version. You can still specify using the old version during execution.

## Options

### --all

If no component is specified, this option must be specified.

- Data type: `BOOLEAN`
- Default: `false`

### --force

If the version of the specified component is already installed, the upgrade operation is skipped by default. Specifying this option forcibly upgrades the installed version.

- Data type: `BOOLEAN`
- Default: `false`

### --nightly

Upgrades the specified components to the nightly version. The command using this option is equivalent to `tiup update <component>:nightly`.

- Data type: `BOOLEAN`
- Default: `false`

### --self

Updates TiUP itself.

- Data type: `BOOLEAN`
- Default: `false`

## Outputs

- If updates successfully, output `Updated successfully!`.
- If target version does not exist, the `Error: version %s not supported by component %s` error is reported.