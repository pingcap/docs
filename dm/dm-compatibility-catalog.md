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

| Data source | Compatibility level | Note |
| - | - | - |
| MySQL ≤ 5.5 | Not tested | |
| MySQL 5.6 | GA | |
| MySQL 5.7 | GA | |
| MySQL 8.0 | GA | Does not support binlog transaction compression [Transaction_payload_event](https://dev.mysql.com/doc/refman/8.0/en/binary-log-transaction-compression.html). |
| MySQL 8.1 ~ 8.3 | Not tested | |
| MySQL 8.4 | Incompatible | For more information, see [DM Issue #11020](https://github.com/pingcap/tiflow/issues/11020). |
| MySQL 9.x | Not tested | |
| MariaDB < 10.1.2 | Incompatible | Incompatible with binlog of the time type. |
| MariaDB 10.1.2 ~ 10.5.10 | Experimental | |
| MariaDB > 10.5.10 | Not tested | Expected to work in most cases after bypassing the [precheck](/dm/dm-precheck.md). See [MariaDB notes](#mariadb-notes). |

### Incompatibility with foreign key CASCADE operations

- DM creates foreign key **constraints** on the target, but they are not enforced while applying transactions because DM sets the session variable [`foreign_key_checks=OFF`](/system-variables.md#foreign_key_checks).
- DM does **not** support `ON DELETE CASCADE` or `ON UPDATE CASCADE` behavior by default, and enabling `foreign_key_checks` via a DM task session variable is not recommended. If your workload relies on cascades, **do not assume** that cascade effects will be replicated.

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
