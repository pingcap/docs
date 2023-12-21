---
title: TiDB 7.6.0 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 7.6.0.
---

# TiDB 7.6.0 Release Notes

Release date: xx xx, 202x

TiDB version: 7.6.0

Quick access: [Quick start](https://docs.pingcap.com/tidb/v7.6/quick-start-with-tidb) | [Installation packages](https://www.pingcap.com/download/?version=v7.6.0#version-list)

7.6.0 introduces the following key features and improvements:

## Feature details

### Scalability

* Feature summary [#issue-number](issue-link) @[pr-auorthor-id](author-link)

    Feature descriptions (including what the feature is, why it is valuable for users, and how to use this feature generally)

    For more information, see [documentation](doc-link).

### Performance

* Feature summary [#issue-number](issue-link) @[pr-auorthor-id](author-link)

    Feature descriptions (including what the feature is, why it is valuable for users, and how to use this feature generally)

    For more information, see [documentation](doc-link).

### Reliability

* Feature summary [#issue-number](issue-link) @[pr-auorthor-id](author-link)

    Feature descriptions (including what the feature is, why it is valuable for users, and how to use this feature generally)

    For more information, see [documentation](doc-link).

### SQL

* Feature summary [#issue-number](issue-link) @[pr-auorthor-id](author-link)

    Feature descriptions (including what the feature is, why it is valuable for users, and how to use this feature generally)

    For more information, see [documentation](doc-link).

### DB operations

* Feature summary [#issue-number](issue-link) @[pr-auorthor-id](author-link)

    Feature descriptions (including what the feature is, why it is valuable for users, and how to use this feature generally)

    For more information, see [documentation](doc-link).

### Observability

* Feature summary [#issue-number](issue-link) @[pr-auorthor-id](author-link)

    Feature descriptions (including what the feature is, why it is valuable for users, and how to use this feature generally)

    For more information, see [documentation](doc-link).

### Data migration

* TiCDC supports replicating DDL statements in bi-directional replication mode [#10301](https://github.com/pingcap/tiflow/issues/10301) @[asddongmen](https://github.com/asddongmen)

    Starting from v7.6.0 TiCDC supports replication of DDL statements with bi-directional replication configured. Previously, replicating DDL statements was not supported by TiCDC, so users of TiCDC's bi-directional replication had to apply DDL statements to both TiDB clusters separately. With this feature, TiCDC allows for a cluster to be assigned the primary BDR role, and for DDL statements at that cluster to be replicated to the downstream cluster.

    For more information, see [documentation](/ticdc/ticdc-bidirectional-replication.md).

* TiCDC supports querying the downstream synchronization status of a changefeed [#10289](https://github.com/pingcap/tiflow/issues/10289) @[hongyunyan](https://github.com/hongyunyan)

    Starting from v7.6.0 TiCDC introduces a new API to support querying the downstream synchronization status of a changefeed. With this API, users can query a TiCDC changefeed about its synchronization status. This allows users to determine whether the upstream information received by TiCDC has been synchronized to the downstream system successfully.

    For more information, see [documentation](/ticdc/ticdc-open-api-v2.md).

* TiCDC adds support for two character delimmeters with CSV output protocol [#9969](https://github.com/pingcap/tiflow/issues/9969) @[zhangjinpeng1987](https://github.com/zhangjinpeng1987)

    Starting from v7.6.0 TiCDC allows the CSV output protocol delimiters to specified as 1 or 2 characters long. With this change, users can configure TiCDC to generate file output using 2 character delimeters (such as `||` or `$^`) to separate fields in the output.

    For more information, see [documentation](/ticdc/ticdc-csv.md).

## Compatibility changes

> **Note:**
>
> This section provides compatibility changes you need to know when you upgrade from v7.5.0 to the current version (v7.6.0). If you are upgrading from v7.4.0 or earlier versions to the current version, you might also need to check the compatibility changes introduced in intermediate versions.

### Behavior changes

### System variables

| Variable name | Change type | Description |
|--------|------------------------------|------|
| [`tidb_idle_transaction_timeout`](/system-variables.md#tidb_idle_transaction_timeout-new-in-v760) | Newly added | Controls the idle timeout for transactions in a user session. When a user session is in a transactional state and remains idle for a duration exceeding the value of this variable, TiDB will terminate the session. The default value `0` means unlimited. |
| [`tidb_txn_entry_size_limit`](/system-variables.md#tidb_txn_entry_size_limit-new-in-v760) | Newly added | Dynamically modifies the TiDB configuration item [`performance.txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v50). It limits the size of a single row of data in TiDB. The default value of this variable is `0`, which means that TiDB uses the value of the configuration item `txn-entry-size-limit` by default. When this variable is set to a non-zero value, `txn-entry-size-limit` is also set to the same value. |

### Configuration file parameters

| Configuration file | Configuration parameter | Change type | Description |
| -------- | -------- | -------- | -------- |
| TiKV | [`raftstore.periodic-full-compact-start-times`](/tikv-configuration-file.md#periodic-full-compact-start-times-new-in-v760) | Newly added | Sets the specific times that TiKV initiates periodic full compaction. The default value `[]` means periodic full compaction is disabled by default. |
| TiKV | [`raftstore.periodic-full-compact-start-max-cpu`](/tikv-configuration-file.md#periodic-full-compact-start-max-cpu-new-in-v760) | Newly added | Limits the maximum CPU usage rate for TiKV periodic full compaction. The default value is `0.1`. |

### System tables

- Add a new system table [`INFORMATION_SCHEMA.KEYWORDS`](/information-schema/information-schema-keywords.md) to display the information of all keywords supported by TiDB. **tw@Oreoxmt**

## Deprecated features

## Improvements

+ TiDB

    - When a non-binary collation is set and the query condition includes `LIKE`, the optimizer generates an `IndexRangeScan` to improve the execution efficiency [#48181](https://github.com/pingcap/tidb/issues/48181) @[time-and-fate](https://github.com/time-and-fate)

## Bug fixes

## Contributors
