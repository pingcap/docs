---
title: Compatibility Catalog of TiDB Data Migration
summary: This document describes the compatibility between DM versions and upstream/downstream databases.
---

# Compatibility Catalog of TiDB Data Migration

DM supports migrating data from different sources to TiDB clusters. Based on the data source type, DM has four compatibility levels:

- **Generally available (GA)**: The application scenario has been verified and passed GA testing.
- **Experimental**: The common application scenarios have been verified, but coverage is limited or involves only a small number of users. Occasional issues are possible, and the verification using your specific scenario is highly recommended.
- **Not tested**: DM aims for MySQL protocol and binlog compatibility, but not all MySQL forks/versions are part of DM test matrix. However, if the forks/versions protocols and binlog formats are MySQL-compatible, these are expected to work. You must verify in your environment before use.
- **Incompatible**: DM has known blocking issues and production use is not recommended.

## Data sources

| Data source | Compatibility level | Remarks |
| - | - | - |
| MySQL ≤ 5.5 | Not tested | |
| MySQL 5.6 | GA | |
| MySQL 5.7 | GA | |
| MySQL 8.0 | GA | Does not support binlog transaction compression [Transaction_payload_event](https://dev.mysql.com/doc/refman/8.0/en/binary-log-transaction-compression.html) |
| MariaDB < 10.1.2 | Incompatible | Incompatible with binlog of the time type |
| MariaDB 10.1.2 ~ 10.5.10 | Experimental | |
| **MariaDB > 10.5.10** | Not tested | **Should work for most cases** after bypassing precheck. See [MariaDB notes](#mariadb-notes). |

### DM is incompatible with Foreign keys CASCADE operations

- DM creates foreign key **constraints** on the target, but they are not enforced while applying transactions because the DM sets the session variable [`foreign_key_checks=OFF`](/system-variables.md#foreign_key_checks).
- DM does **not** honor `ON DELETE/UPDATE CASCADE` behavior by default and it is not recommended to enable `foreign_key_checks` via DM task session variable. If your workload relies on cascades, **do not assume** cascade effects will be replicated.

### MariaDB notes

- For MariaDB **10.5.11 and later**, DM **precheck will fail** due to privilege name changes and return:  
  `[code=26005] fail to check synchronization configuration`  
  with errors in the replication and dump privilege checkers (e.g., mentions of `BINLOG MONITOR`, `REPLICATION SLAVE ADMIN`, `REPLICATION MASTER ADMIN`).
- You can **bypass precheck** by adding  
  `ignore-checking-items: ["all"]` in the DM task. See [DM precheck](/dm/dm-precheck.md) for details.

## Target databases

> **Warning:**  
> DM v5.3.0 is not recommended. If you enabled GTID replication without relay log in DM v5.3.0, data replication can fail with low probability.

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