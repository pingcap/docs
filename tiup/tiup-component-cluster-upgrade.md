---
title: tiup cluster upgrade
summary: The tiup cluster upgrade command is used to upgrade a specified cluster to a specific version. It requires the cluster name and target version as input. Options include --force to ignore errors and start the cluster, --transfer-timeout to set maximum wait time for node migration, --ignore-config-check to skip configuration check, and --offline to replace binary files without restarting the cluster. The output is the log of the upgrading progress.
---

# tiup cluster upgrade

The `tiup cluster upgrade` command is used to upgrade the specified cluster to a specific version.

## Syntax

```shell
tiup cluster upgrade <cluster-name> <version> [flags]
```

- `<cluster-name>`: the cluster name to operate on. If you forget the cluster name, you can check it with the [cluster list](/tiup/tiup-component-cluster-list.md) command.
- `<version>`: the target version to upgrade to, such as `v8.2.0`. Currently, it is only allowed to upgrade to a version higher than the current cluster, that is, no downgrade is allowed. It is also not allowed to upgrade to the nightly version.

## Options

### --force

- To upgrade the cluster, you need to ensure that the cluster is currently started. In some cases, you might want to upgrade when the cluster is not started. At this time, you can use `--force` to ignore the error during the upgrade, forcibly replace the binary file and start the cluster.
- Data type: `BOOLEAN`
- Default: false

> **Note:**
>
> Forcing an upgrade of the cluster that is providing services might result in service unavailability. Unstarted clusters are started automatically after a successful upgrade.

### --transfer-timeout

- When upgrading PD or TiKV, the leader of the upgraded node is migrated to other nodes first. The migration process takes some time, and you can set the maximum wait time (in seconds) by the `-transfer-timeout` option. After the timeout, the wait is skipped and the service is upgraded directly.
- Data type: `uint`
- Default: 600

> **Note:**
>
> If the wait is skipped and the service is upgraded directly, the service performance might jitter.

### --ignore-config-check

- After the binary is updated, a configuration check is performed on the TiDB, TiKV and PD components using `<binary> --config-check <config-file>`. `<binary>` is the path to the newly deployed binary and `<config-file>` is the configuration file generated based on the user configuration. To skip this check, you can use the `--ignore-config-check` option.
- Data type: `BOOLEAN`
- Default: false

### --ignore-version-check

- Before upgrading, TiUP checks whether the target version is greater than or equal to the current version. To skip this check, you can use the `--ignore-version-check` option.
- Data type: `BOOLEAN`
- This option is disabled by default with the `false` value. To enable this option, add this option to the command, and either pass the `true` value or do not pass any value.

### --offline

- Declares that the current cluster is not running. When this option is specified, TiUP does not evict the service leader to another node or restart the service, but only replaces the binary files of the cluster components.
- Data type: `BOOLEAN`
- This option is disabled by default with the `false` value. To enable this option, add this option to the command, and either pass the `true` value or do not pass any value.

### --pd-version

- Specifies the version of PD. If this option is set, the version of PD will no longer be consistent with the cluster version.
- Data type: `STRINGS`
- If this option is not set, the version of PD remains consistent with the cluster version.

### --tikv-version

- Specifies the version of TiKV. If this option is set, the version of TiKV will no longer be consistent with the cluster version.
- Data type: `STRINGS`
- If this option is not set, the version of TiKV remains consistent with the cluster version.

### --tikv-cdc-version

- Specifies the version of TiKV CDC. If this option is set, the version of TiKV CDC will no longer be consistent with the cluster version.
- Data type: `STRINGS`
- If this option is not set, the version of TiKV CDC remains consistent with the cluster version.

### --tiflash-version

- Specifies the version of TiFlash. If this option is set, the version of TiFlash will no longer be consistent with the cluster version.
- Data type: `STRINGS`
- If this option is not set, the version of TiFlash remains consistent with the cluster version.

### --cdc-version

- Specifies the version of TiCDC. If this option is set, the version of TiCDC will no longer be consistent with the cluster version.
- Data type: `STRINGS`
- If this option is not set, the version of TiCDC remains consistent with the cluster version.

### --tiproxy-version

- Specifies the version of TiProxy. If this option is set, the version of TiProxy will no longer be consistent with the cluster version.
- Data type: `STRINGS`
- If this option is not set, the version of TiProxy remains consistent with the cluster version.

### --tidb-dashboard-version

- Specifies the version of TiDB Dashboard. If this option is set, the version of TiDB Dashboard will no longer be consistent with the cluster version.
- Data type: `STRINGS`
- If this option is not set, the version of TiDB Dashboard remains consistent with the cluster version.

### --alertmanager-version

- Specifies the version of alert manager. If this option is set, the version of alert manager will no longer be consistent with the cluster version.
- Data type: `STRINGS`
- If this option is not set, the version of alert manager remains consistent with the cluster version.

### --blackbox-exporter-version

- Specifies the version of Blackbox Exporter. If this option is set, the version of Blackbox Exporter will no longer be consistent with the cluster version.
- Data type: `STRINGS`
- If this option is not set, the version of Blackbox Exporter remains consistent with the cluster version.

### --node-exporter-version

- Specifies the version of Node Exporter. If this option is set, the version of Node Exporter will no longer be consistent with the cluster version.
- Data type: `STRINGS`
- If this option is not set, the version of Node Exporter remains consistent with the cluster version.

### -h, --help

- Prints the help information.
- Data type: `BOOLEAN`
- This option is disabled by default with the `false` value. To enable this option, add this option to the command, and either pass the `true` value or do not pass any value.

### ---pre-upgrade-script

> **Warning:**
>
> This option is experimental and is not recommended for production deployments.

- Runs a script before the upgrade.
- Data type: `STRINGS`
- This option specifies the path of a script to be run on the node that is to be upgraded.

### ---post-upgrade-script

> **Warning:**
>
> This option is experimental and is not recommended for production deployments.

- Runs a script after the upgrade.
- Data type: `STRINGS`
- This option specifies the path of a script to be run after the upgrade of a node. This script will be executed on the upgraded node itself.

## Output

The log of the upgrading progress.

[<< Back to the previous page - TiUP Cluster command list](/tiup/tiup-component-cluster.md#command-list)
