---
title: Compatibility of TiDB Lightning and IMPORT INTO with TiCDC and Log Backup
summary: Learn about compatibility of IMPORT INTO and TiDB Lightning with log backup and TiCDC.
---

# Compatibility of TiDB Lightning and IMPORT INTO with TiCDC and Log Backup

This document describes TiDB Lightning and `IMPORT INTO` compatibility with [log backup](/br/br-pitr-guide.md), [TiCDC](/ticdc/ticdc-overview.md), as well as some special usage scenarios.

## `IMPORT INTO` vs. TiDB Lightning

[`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) currently integrates with the physical import mode of TiDB Lightning, but there are some differences. See [`IMPORT INTO` vs. TiDB Lightning](/tidb-lightning/import-into-vs-tidb-lightning.md) for details.

## Compatibility with log backup and TiCDC

- TiDB Lightning [logical import mode](/tidb-lightning/tidb-lightning-logical-import-mode.md) is compatible with log backup and TiCDC.

- TiDB Lightning [physical import mode](/tidb-lightning/tidb-lightning-physical-import-mode.md) is not compatible with log backup and TiCDC. The reason is that physical import mode directly ingests the encoded KV pairs of the source data to TiKV, and TiKV will not generate the corresponding change log during this process. Without this part of the change log, the relevant data cannot be backed up and cannot be replicated by TiCDC.

- `IMPORT INTO` is not compatible with log backup and TiCDC. The reason is that `IMPORT INTO` also ingests the encoded KV pairs of the source data directly to TiKV.

## Scenarios for TiDB Lightning logical import mode

If the performance of TiDB Lightning logical import can meet the performance requirements of the application and the application requires TiDB Lightning imported tables to be backed up or replicated downstream using TiCDC, it is recommended to use TiDB Lightning logical import mode.

## Scenarios for TiDB Lightning physical import mode

This section describes how to use TiDB Lightning together with [log backup](/br/br-pitr-guide.md) and [TiCDC](/ticdc/ticdc-overview.md).

If the performance of TiDB Lightning logical imports does not meet the performance requirements, you have touse TiDB Lightning physical import mode, and the tables need to be backed up or replicated downstream using TiCDC, then the following scenarios are recommended.

### Used with log backup

You can perform in different scenarios as follows:

- Scenario 1: tables in physical import mode do not need to be backed up

    In this scenario, if [PITR](/br/br-log-architecture.md#process-of-pitr) is enabled, the compatibility check will report an error after starting TiDB Lightning. If you are sure that these tables do not need to be backed up or backed up by [log backup](/br/br-pitr-guide.md), you can change the [TiDB Lightning configuration file](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task) in the `Lightning.check-requirements` parameter to `false` and restart the import task.

- Scenario 2: after the physical import is finished, there will be no new DML operations on the table

    This scenario does not involve incremental data writes, so it is sufficient to perform a table-level snapshot backup of the table after completing the data import in TiDB Lightning physical import mode, as described in [Back up a table](/br/br-snapshot-manual.md#back-up-a-table).

    During data recovery, the snapshot data of the table is restored. See [Restore a table](/br/br-snapshot-manual.md#restore-a-table) for the procedure.

- Scenario 3: after the physical import is finished, perform new DML operations to the table (not supported)

    In this scenario, you can only choose either [full snapshot backup](/br/br-snapshot-guide.md) or [log backup](/br/br-pitr-guide.md) for the backup operation of this table. You cannot back up and restore the full snapshot data and log backup data of this table.

### Used with TiCDC

This scenario is not compatible in the short term, because TiCDC can hardly keep up with the write speed of TiDB Lightning physical import mode, which might result in increasing cluster replication latency.

You can perform in different scenarios as follows:

- Scenario 1: the table does not need to be replicated downstream by TiCDC.

    In this scenario, if TiCDC changefeed is enabled, the compatibility check will report an error after starting TiDB Lightning. If you are sure that these tables do not need to be replicated by TiCDC, you can change the `Lightning.check-requirements` parameter in the [TiDB Lightning configuration file](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task) to `false` and then restart the import task.

- Scenario 2: the table needs to be replicated downstream by TiCDC.

    In this scenario, if TiCDC changefeed is enabled, the compatibility check will report an error after starting TiDB Lightning. You need to change the `Lightning.check-requirements` parameter in the [TiDB Lightning configuration file](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task) in the upstream TiDB cluster to `false` and then restart the import task.

    After the import task for the upstream TiDB cluster is finished, use TiDB Lightning to import a copy of the same data in the downstream TiDB cluster. If you have databases such as Redshift and Snowflake in the downstream, you can have these databases read CSV or Parquet files from a cloud storage service and write them to the database.

## Scenarios for `IMPORT INTO`

This section describes how to use `IMPORT INTO` together with [log backup](/br/br-pitr-guide.md) and [TiCDC](/ticdc/ticdc-overview.md).

### Used with log backup

You can perform in different scenarios as follows:

- Scenario 1: tables do not need to be backed up

    In this scenario, if [PITR](/br/br-log-architecture.md#process-of-pitr) is enabled, the compatibility check will report an error after you submit the `IMPORT INTO` SQL. If you are sure that these tables do not need to be backed up or backed up by [log backups](/br/br-pitr-guide.md), you can include `DISABLE_PRECHECK` (introduced in v8.0.0) in [`WithOptions`](/sql-statements/sql-statement-import-into.md#withoptions) of that SQL, and then resubmit it, so that the data import task ignores the compatibility check, and imports the data directly.

- Scenario 2: after the import is finished, there will be no new DML operations on the table

    This scenario does not involve incremental data writes, so it is sufficient to perform a table-level snapshot backup of the table after completing the data import, as described in [Back up a table](/br/br-snapshot-manual.md#back-up-a-table).

    During data recovery, the snapshot data of the table is restored. See [Restore a table](/br/br-snapshot-manual.md#restore-a-table) for the procedure.

- Scenario 3: after the import is finished, perform new DML operations to the table (not supported)

    In this scenario, you can only choose either [full snapshot backup](/br/br-snapshot-guide.md) or [log backup](/br/br-pitr-guide.md) for the backup operation of this table. You cannot back up and restore the full snapshot data and log backup data of this table.

### Used with TiCDC

You can perform in different scenarios as follows:

- Scenario 1: the table does not need to be replicated downstream by TiCDC.

    In this scenario, the compatibility check will report an error after you submit the `IMPORT INTO` SQL because TiCDC changefeed is enabled. If you are sure that these tables do not need to be replicated by TiCDC, you can include `DISABLE_PRECHECK` (introduced in v8.0.0) in [`WithOptions`](/sql-statements/sql-statement-import-into.md#withoptions) of that SQL, and then resubmit it, so that the data import task ignores the compatibility check, and imports the data directly.

- Scenario 2: the table needs to be replicated downstream by TiCDC.

    In this scenario, if TiCDC changefeed is enabled, the compatibility check will report an error after starting TiDB Lightning. you can include `DISABLE_PRECHECK` (introduced in v8.0.0) in [`WithOptions`](/sql-statements/sql-statement-import-into.md#withoptions) of that SQL, and then resubmit it, so that the data import task ignores the compatibility check, and imports the data directly.

    After the import task for the upstream TiDB cluster is finished, use TiDB Lightning to import a copy of the same data in the downstream TiDB cluster. If you have databases such as Redshift and Snowflake in the downstream, you can have these databases read CSV or Parquet files from a cloud storage service and write them to the database.
