---
title: Compatibility Catalog of TiDB Data Migration
summary: This document describes the compatibility of TiDB Data Migration (DM) with upstream and downstream databases.
---

# Compatibility Catalog of TiDB Data Migration

DM supports migrating data from different sources to TiDB clusters. Based on the data source type, DM has four compatibility levels:

- **Generally available (GA)**: The application scenario has been verified and passed GA testing.
- **Experimental**: Common application scenarios have been verified, but coverage is limited or involves only a small number of users. Occasional issues are possible, so you need to verify compatibility in your specific scenario.
- **Not tested**: DM aims to be compatible with the MySQL protocol and binlog. However, not all MySQL forks or versions are included in the DM test matrix. If a fork or version uses MySQL-compatible protocols and binlog formats, it is expected to work, but you must verify compatibility in your own environment before use.
- **Incompatible**: DM has known blocking issues, so production use is not recommended.

## Data sources

| Data source              | Compatibility level | Note |
| ------------------------ | ------------------- | ---- |
| MySQL ≤ 5.5              | Not tested          |      |
| MySQL 5.6                | GA                  |      |
| MySQL 5.7                | GA                  |      |
| MySQL 8.0                | GA                  | Does not support [binlog transaction compression (`Transaction_payload_event`)](https://dev.mysql.com/doc/refman/8.0/en/binary-log-transaction-compression.html). |
| MySQL 8.1 ~ 8.3          | Not tested          | Does not support [binlog transaction compression (`Transaction_payload_event`)](https://dev.mysql.com/doc/refman/8.0/en/binary-log-transaction-compression.html). |
| MySQL 8.4                | Experimental (supported starting from TiDB v8.5.6) | Does not support [binlog transaction compression (`Transaction_payload_event`)](https://dev.mysql.com/doc/refman/8.4/en/binary-log-transaction-compression.html). |
| MySQL 9.x                | Not tested          |      |
| MariaDB < 10.1.2         | Incompatible        | Incompatible with binlog of the time type. |
| MariaDB 10.1.2 ~ 10.5.10 | Experimental        |      |
| MariaDB > 10.5.10        | Not tested          | Expected to work in most cases after bypassing the [precheck](/dm/dm-precheck.md). See [MariaDB notes](#mariadb-notes). |

### Foreign key `CASCADE` operations

> **Warning:**
>
> This feature is experimental. It is not recommended that you use it in the production environment. It might be changed or removed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tiflow/issues) on GitHub.

Starting from v8.5.6, DM provides **experimental** support for replicating tables that use foreign key constraints. This support includes the following improvements:

- **Safe mode**: during safe mode execution, DM sets `foreign_key_checks=0` for each batch and skips the redundant `DELETE` step for `UPDATE` statements that do not modify primary key or unique key values. This prevents `REPLACE INTO` (which internally performs `DELETE` + `INSERT`) from triggering unintended `ON DELETE CASCADE` effects on child rows. For more information, see [DM safe mode](/dm/dm-safe-mode.md#foreign-key-handling-new-in-v856).
- **Multi-worker causality**: when `worker-count > 1`, DM reads foreign key relationships from the downstream schema at task start and injects causality keys. This ensures that DML operations on parent rows complete before operations on dependent child rows, preserving binlog order across workers.

The following limitations apply to foreign key replication:

- In safe mode, DM does not support `UPDATE` statements that modify primary key or unique key values. The task is paused with the error `safe-mode update with foreign_key_checks=1 and PK/UK changes is not supported`. To replicate such statements, set `safe-mode: false`.
- When `foreign_key_checks=1`, DM does not support DDL statements that create, modify, or drop foreign key constraints during replication.
- Table routing is not supported when `worker-count > 1`. If you use table routing with tables that include foreign keys, set `worker-count` to `1`.
- The block-allow list must include all ancestor tables in the foreign key dependency chain. If ancestor tables are filtered out, the task is paused with an error during incremental replication.
- Foreign key metadata must be consistent between the source and downstream. If inconsistencies are detected, run `binlog-schema update --from-target` to resynchronize metadata.
- `ON UPDATE CASCADE` is not correctly replicated in safe mode when an `UPDATE` modifies primary key or unique key values. DM rewrites such statements as `DELETE` + `REPLACE`, which triggers `ON DELETE` actions instead of `ON UPDATE` actions. In this case, DM rejects the statement and pauses the task. `UPDATE` statements that do not modify key values are replicated correctly.

In versions earlier than v8.5.6, DM creates foreign key constraints in the downstream but does not enforce them because it sets the session variable [`foreign_key_checks=OFF`](/system-variables.md#foreign_key_checks). As a result, cascading operations are not replicated to the downstream.

### MariaDB notes

- For MariaDB **10.5.11 and later**, the DM **precheck fails** due to privilege name changes (for example, `BINLOG MONITOR`, `REPLICATION SLAVE ADMIN`, `REPLICATION MASTER ADMIN`). The error appears as `[code=26005] fail to check synchronization configuration` in the replication privilege, dump privilege, and dump connection number checkers.
- You can **bypass the precheck** by adding `ignore-checking-items: ["all"]` in the DM task. See [DM precheck](/dm/dm-precheck.md) for details.

## Target databases

> **Warning:**
>
> DM v5.3.0 is not recommended. Enabling GTID replication without relay log in DM v5.3.0 might cause data replication to fail, although the probability is low.

| Target database | Compatibility level | DM version |
| - | - | - |
| TiDB 8.x | GA | ≥ 5.3.1 |
| TiDB 7.x | GA | ≥ 5.3.1 |
| TiDB 6.x | GA | ≥ 5.3.1 |
| TiDB 5.4 | GA | ≥ 5.3.1 |
| TiDB 5.3 | GA | ≥ 5.3.1 |
| TiDB 5.2 | GA | ≥ 2.0.7, recommended: 5.4 |
| TiDB 5.1 | GA | ≥ 2.0.4, recommended: 5.4 |
| TiDB 5.0 | GA | ≥ 2.0.4, recommended: 5.4 |
| TiDB 4.x | GA | ≥ 2.0.1, recommended: 2.0.7 |
| TiDB 3.x | GA | ≥ 2.0.1, recommended: 2.0.7 |
| MySQL | Experimental | |
| MariaDB | Experimental | |
