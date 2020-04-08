---
title: Tune TiFlash Performance
summary: Learn how to tune the performance of TiFlash.
category: reference
---

# Tune TiFlash Performance

This document introduces how to tune the performance of TiFlash, including planning machine resources, tuning TiDB parameters, and setting the size of TiKV Regions.

## Plan resources

If you want to save machine resources and have no requirement on isolation, you can use the method that combines the deployment of both TiKV and TiFlash. It is recommended that you save enough resources for TiKV and TiFlash respectively, and do not share disks.

## Tune TiDB parameters

1. For the TiDB node dedicated to OLAP/TiFlash, it is recommended that you increase the value of the [`tidb_distsql_scan_concurrency`](/reference/configuration/tidb-server/tidb-specific-variables.md#tidb_distsql_scan_concurrency) configuration item for this node to `80`:

    {{< copyable "sql" >}}

    ```sql
    set @@tidb_distsql_scan_concurrency = 80;
    ```

2. Enable the optimization for TiDB Operator such as the aggregate pushdown of `JOIN` or `UNION`:

    {{< copyable "sql" >}}

    ```sql
    set @@tidb_opt_agg_push_down = 1;
    ```

## Configure the size of TiKV Regions

The number and size of Regions might have some impact on TiFlash performance. Too many small Regions might bring down TiFlash performance by several times.

For user scenarios that focus on analysis and query, it is recommended that you set the Region size to 192MB, and enable the Region Merge feature to ensure that small Regions generated during operation are automatically merged.

This section introduces how to set Region size and enable Region Merge for TiDB clusters that are deployed in different ways.

### For clusters deployed using TiDB Ansible

For clusters deployed using TiDB Ansible, use the following methods to set Region size and enable Region Merge:

+ To modify the Region size, add the following configuration in the `roles/tikv/vars/default.yml` file and then restart the cluster.

    {{< copyable "" >}}

    ```yaml
    coprocessor:
    region-max-size: "288MiB"
    region-split-size: "192MiB"
    region-max-keys:  2880000
    region-split-keys:  1920000
    ```

+ To enable Region Merge, add the following configuration in the `roles/pd/vars/default.yml` file. You can also execute the `config set <config-name>` command in pd-ctl to enable this feature.

    {{< copyable "" >}}

    ```yaml
    schedule:
    max-merge-region-size: 20 # Merges Regions smaller that 20 MB.
    max-merge-region-keys: 200000 # Merges Regions with less than 20,000 keys.
    split-merge-interval: "1h"
    merge-schedule-limit: 8 # Controls the speed of merge. Setting this value to 0 will disable Region Merge.
    ```

### For clusters deployed not using TiDB Ansible

For TiDB clusters deployed not using TiDB Ansible, use the following methods to set Region size and enable Region Merge:

+ To modify the Region size, add the following configuration in the `tikv.toml` file and then restart the cluster.

    {{< copyable "" >}}

    ```toml
    [coprocessor]
    region-max-size = "288MiB"
    region-split-size = "192MiB"
    region-max-keys = 2880000
    region-split-keys = 1920000
    ```

+ To enable Region Merge, add the following configuration in the `pd.toml` file:

    {{< copyable "" >}}

    ```toml
    [schedule]
    max-merge-region-size = 20
    max-merge-region-keys = 200000
    split-merge-interval = "1h"
    merge-schedule-limit = 8
    ```

    You can also execute the `config set <config-name>` command in pd-ctl to enable Region Merge.
