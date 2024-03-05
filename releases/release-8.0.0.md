---
title: TiDB 8.0.0 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 8.0.0.
---

# TiDB 8.0.0 Release Notes

Release date: xx xx, 2024

TiDB version: 8.0.0

Quick access: [Quick start](https://docs.pingcap.com/tidb/v8.0/quick-start-with-tidb) | [Installation packages](https://www.pingcap.com/download/?version=v8.0.0#version-list)

8.0.0 introduces the following key features and improvements:

<table>
<thead>
  <tr>
    <th>Category</th>
    <th>Feature/Enhancement</th>
    <th>Description</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td rowspan="4">Scalability and Performance</td>
    <td>Disaggregation of PD to improve scale (experimental) **tw@qiancai** <!--1553, 1558--></td>
    <td>PD (Placement Driver) has a lot of critical modules for the running of TiDB. Each module's resource consumption can increase as certain workloads scale, meaning they can each interfere with other functions in PD, ultimately impacting quality of service of the cluster.
By separating PD modules into separately-deployable services, their blast radii are massively mitigated as the cluster scales. Much larger clusters with much larger workloads are possible with this architecture.</td>
  </tr>
  <tr>
    <td>Pipelined DML for much larger transactions (experimental) **tw@Oreoxmt** <!--1694--></td>
    <td>Large batch DML jobs like huge cleanup jobs, joins, or aggregations can consume tons of memory and were previously limited at very large scales. Pipelined DML is a new feature meant for supporting large batch DML with transaction guarantees more efficiently and mitigating out-of-memory risks. When used for data loading, this is distinct from import, load, and restore operations. </td>
  </tr>
  <tr>
    <td>Acceleration of cluster snapshot restore speed **tw@qiancai** <!--1681--></td>
    <td>An optimization to involve all TiKV nodes in the preparation step for cluster restores was introduced to leverage scale such that restore speeds for a cluster are much faster for larger sets of data on larger clusters. Real world tests exhibit restore acceleration of ~300% in slower cases.</td>
  </tr>
  <tr>
    <td>Enhanced stability of massive number of tables **tw@hfxsd** <!--16408--></td>
    <td>SaaS companies using TiDB as the system of record for their multi-tenant applications require storing many tables. Prior to this release, so table counts on the order of a million or more were possible but were likely to degrade experience.
Several enhancements were made in this version to mitigate that:

  - New information schema caching system that includes a lazy-loading LRU cache for table metadata and more memory-efficient handling of schema version changes.
  - Priority queue for auto-analyze, making auto-analyze less rigid and more stable across more tables</td>
  </tr>
  <tr>
    <td rowspan="1">DB Operations and Observability</td>
    <td>Index usage view **tw@Oreoxmt** <!--1400--></td>
    <td>TiDB adds a new system table for viewing the usage statistics of indexes, ultimately helping users to evaluate the importance (or lack thereof) of all indexes.</td>
    </td>
  </tr>
  <tr>
    <td rowspan="3">Data Migration</td>
    <td>TiCDC supports replicating DDL statements in bi-directional replication (BDR) mode (GA)</td>
    <td>With this feature, TiCDC allows for a cluster to be assigned the PRIMARY BDR role, and enables the replication of DDL statements from that cluster to the downstream cluster</td>
    </td>
  </tr>
  <tr>
    <td>TiCDC adds support for Simple Protocol</td>
    <td>TiCDC introduces support for a new protocol, the Simple Protocol. This new protocol includes support for in-band schema tracking capabilities.</td>
  </tr>
  <tr>
    <td>TiCDC adds support for Debezium format Protocol</td>
    <td>TiCDC can now publish replication events to a Kafka sink using a protocol that generates Debezium style messages.</td>
  </tr>
</tbody>
</table>

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

* PITR supports Amazon S3 Object Lock [#51184](https://github.com/pingcap/tidb/issues/51184) @[RidRisR](https://github.com/RidRisR) **tw@lilin90** <!--1604-->

    Amazon S3 Object Lock can help prevent backup data from being accidentally or intentionally deleted during a specified retention period, enhancing the security and integrity of data. Starting from v6.3.0, BR supports Amazon S3 Object Lock in snapshot backups, adding an additional layer of security for full backups. Starting from v8.0.0, PITR also supports Amazon S3 Object Lock. Whether full backups or log data backups, the Object Lock feature ensures a more reliable data protection, further strengthening the security of data backup and recovery and meeting regulatory requirements.

    For more information, see [documentation](/br/backup-and-restore-storages.md#other-features-supported-by-the-storage-service).

* Feature summary [#issue-number](issue-link) @[pr-auorthor-id](author-link)

    Feature descriptions (including what the feature is, why it is valuable for users, and how to use this feature generally)

    For more information, see [documentation](doc-link).

### Observability

* Feature summary [#issue-number](issue-link) @[pr-auorthor-id](author-link)

    Feature descriptions (including what the feature is, why it is valuable for users, and how to use this feature generally)

    For more information, see [documentation](doc-link).

### Data migration

* TiCDC supports replicating DDL statements in bi-directional replication (BDR) mode (GA) [#10301](https://github.com/pingcap/tiflow/issues/10301) @[asddongmen](https://github.com/asddongmen)

    General Availability since v8.0.0, TiCDC supports replication of DDL statements with bi-directional replication configured. Previously, replicating DDL statements was not supported by TiCDC, so users of TiCDC's bi-directional replication had to apply DDL statements to both TiDB clusters separately. With this feature, TiCDC allows for a cluster to be assigned the PRIMARY BDR role, and enables the replication of DDL statements from that cluster to the downstream cluster.

    For more information, see [documentation](https://docs.pingcap.com/tidb/v8.0/ticdc-bidirectional-replication).

* TiCDC adds support for Simple Protocol [#9898](https://github.com/pingcap/tiflow/issues/9898) @[3AceShowHand](https://github.com/3AceShowHand)

    TiCDC introduces support for a new protocol, the Simple protocol. This new protocol includes support for in-band schema tracking capabilities.

    For more information, see [documentation](/ticdc/ticdc-simple-protocol.md).

* TiCDC adds support for Debezium format Protocol [#1799](https://github.com/pingcap/tiflow/issues/1799) @[breezewish](https://github.com/breezewish)

    TiCDC can now publish replication events to a Kafka sink using a protocol that generates event messages using a Debezium style format. This helps to simplify the migration from MySQL to TiDB for users who are currently using Debezium to pull data from MySQL for downstream processing.

    For more information, see [documentation](/ticdc/ticdc-debezium.md).

## Compatibility changes

> **Note:**
>
> This section provides compatibility changes you need to know when you upgrade from v7.6.0 to the current version (v8.0.0). If you are upgrading from v7.5.0 or earlier versions to the current version, you might also need to check the compatibility changes introduced in intermediate versions.

### Behavior changes

### System variables

| Variable name | Change type | Description |
|--------|------------------------------|------|
|        |                              |      |

### Configuration file parameters

| Configuration file | Configuration parameter | Change type | Description |
| -------- | -------- | -------- | -------- |
|          |          |          |          |

## Deprecated features

- Starting from v8.0.0, the [`tidb_disable_txn_auto_retry`](/system-variables.md#tidb_disable_txn_auto_retry) system variable is deprecated, and TiDB no longer supports automatic retries of optimistic transactions. As an alternative, when encountering optimistic transaction conflicts, you can capture the error and retry transactions in your application, or use the [Pessimistic transaction mode](/pessimistic-transaction.md) instead. **tw@lilin90** <!--1671-->

## Improvements

## Bug fixes

## Contributors