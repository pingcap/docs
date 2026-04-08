---
title: DM-worker Introduction
summary: Learn the features of DM-worker.
aliases: ['/docs/tidb-data-migration/dev/dm-worker-intro/']
---

# DM-worker Introduction

DM-worker is a component of TiDB Data Migration (DM) that executes tasks to dump and replicate data from MySQL/MariaDB to TiDB.

## Key Concepts

- A DM-worker can perform a full export of data from the MySQL source and then transition to reading the MySQL binlog for continuous, incremental replication.
- The DM-worker is the execution engine for tasks and subtasks received from the DM-master. It dumps data from one MySQL source instance, acts as a replication client reading the binlog events, performs data transformation and filtering, stores data in a local relay log, applies data to the downstream target TiDB, and reports the status back to the DM-master.
- If a worker instance goes offline, DM-master can automatically reschedule its tasks to another available worker to resume the data replication. Note that this does not apply during a full export/import phase.
- A single DM-worker process connects to **one** upstream source database at a time. To migrate from multiple sources, such as when merging sharded tables, you must run multiple DM-worker processes.

> **Note:**
>
> A DM-worker is a MySQL binlog client, not a standby database replica server. It reads and replays data from a MySQL source to a TiDB target. To replicate data from a source TiDB cluster, use [TiCDC](/ticdc/ticdc-overview.md).

## DM-worker processing units

A DM-worker task contains multiple logic units, including relay log, the dump processing unit, the load processing unit, and binlog replication.

### Relay log

The relay log persistently stores the binlog data from the upstream MySQL/MariaDB and provides the feature of accessing binlog events for the binlog replication.

Its rationale and features are similar to the relay log of MySQL. For details, see [MySQL Relay Log](https://dev.mysql.com/doc/refman/8.0/en/replica-logs-relaylog.html).

### Dump processing unit

The dump processing unit dumps the full data from the upstream MySQL/MariaDB to the local disk.

### Load processing unit

The load processing unit reads the dumped files of the dump processing unit and then loads these files to the downstream TiDB.

### Binlog replication/sync processing unit

Binlog replication/sync processing unit reads the binlog events of the upstream MySQL/MariaDB or the binlog events of the relay log, transforms these events to SQL statements, and then applies these statements to the downstream TiDB.

## Privileges required by DM-worker

This section describes the upstream and downstream database users' privileges required by DM-worker, and the user privileges required by the respective processing unit.

### Upstream database user privileges

The required privileges for the upstream database user depend on the database flavor (MySQL/MariaDB) and version.

#### MySQL and MariaDB version before 10.5

For MySQL and MariaDB versions before 10.5, the user must have the following privileges:

| Privilege | Scope |
|:----|:----|
| `SELECT` | Tables |
| `RELOAD` | Global |
| `REPLICATION SLAVE` | Global |
| `REPLICATION CLIENT` | Global |

To grant these privileges, execute the following statement:

```sql
GRANT RELOAD, REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'your_user'@'your_wildcard_of_host';
GRANT SELECT ON `db1`.* TO 'your_user'@'your_wildcard_of_host';
```

#### MariaDB version 10.5 or higher

Starting from [MariaDB 10.5](https://mariadb.com/docs/release-notes/community-server/old-releases/mariadb-10-5-series/what-is-mariadb-105), the `REPLICATION CLIENT` privilege was renamed and split into more granular privileges. The user must have the following privileges:

| Privilege | Scope | Description |
|:---|:---|:---|
| `SELECT` | Tables | Required for full data export. |
| `RELOAD` | Global | Required for `FLUSH TABLES WITH READ LOCK`. |
| `BINLOG MONITOR` | Global | Renamed from `REPLICATION CLIENT`; allows monitoring the binlog. |
| `REPLICATION SLAVE` | Global | Allows reading binlog events. |
| `REPLICATION SLAVE ADMIN` | Global | Allows managing replication status (for example, `SHOW SLAVE STATUS`). |
| `REPLICATION MASTER ADMIN`| Global | Allows monitoring the master (for example, `SHOW SLAVE HOSTS`). |

To grant these privileges, execute the following statement:

```sql
GRANT RELOAD, BINLOG MONITOR, REPLICATION SLAVE, REPLICATION SLAVE ADMIN, REPLICATION MASTER ADMIN ON *.* TO 'your_user'@'your_wildcard_of_host';
GRANT SELECT ON db1.* TO 'your_user'@'your_wildcard_of_host';
```

> **Note:**
>
> Due to changes in MariaDB 10.5+, DM's automated pre-check (`check-task`) might fail with privilege errors because the checks were designed for MySQL's privilege system.
>
> If the pre-check fails even with the correct privileges granted, you can use the following workaround in your task configuration file to bypass the check:
>
> ```yaml
> ignore-checking-items: ["all"]
> ```
>
> This option bypasses all pre-checks, so it is crucial to verify that all prerequisites are met before skipping.

If you also need to migrate the data from other databases into TiDB, make sure the same privileges are granted to the user of the respective databases.

### Downstream database user privileges

The downstream database (TiDB) user must have the following privileges:

| Privilege | Scope |
|:----|:----|
| `SELECT` | Tables |
| `INSERT` | Tables |
| `UPDATE` | Tables |
| `DELETE` | Tables |
| `CREATE` | Databases, tables |
| `DROP` | Databases, tables |
| `ALTER` | Tables |
| `INDEX` | Tables |

Execute the following `GRANT` statement for the databases or tables that you need to migrate:

```sql
GRANT SELECT,INSERT,UPDATE,DELETE,CREATE,DROP,ALTER,INDEX ON db.table TO 'your_user'@'your_wildcard_of_host';
GRANT ALL ON dm_meta.* TO 'your_user'@'your_wildcard_of_host';
```

### Minimal privilege required by each processing unit

The following table lists the minimal privileges required by each processing unit for **MySQL and MariaDB < 10.5**. For MariaDB 10.5 and later, refer to the privilege table in the preceding section.

| Processing unit | Minimal upstream (MySQL/MariaDB) privilege | Minimal downstream (TiDB) privilege | Minimal system privilege |
|:----|:--------------------|:------------|:----|
| Relay log | `REPLICATION SLAVE` (reads the binlog)<br/>`REPLICATION CLIENT` (`SHOW MASTER STATUS`, `SHOW SLAVE STATUS`) | NULL | Read/Write local files |
| Dump | `SELECT`<br/>`RELOAD` (`FLUSH TABLES WITH READ LOCK`) | NULL | Write local files |
| Load | NULL | `SELECT` (Query the checkpoint history)<br/>`CREATE` (creates a database/table)<br/>`DELETE` (deletes checkpoint)<br/>`INSERT` (Inserts the Dump data) | Read/Write local files |
| Binlog replication | `REPLICATION SLAVE` (reads the binlog)<br/>`REPLICATION CLIENT` (`SHOW MASTER STATUS`, `SHOW SLAVE STATUS`) | `SELECT` (shows the index and column)<br/>`INSERT` (DML)<br/>`UPDATE` (DML)<br/>`DELETE` (DML)<br/>`CREATE` (creates a database/table)<br/>`DROP` (drops databases/tables)<br/>`ALTER` (alters a table)<br/>`INDEX` (creates/drops an index)| Read/Write local files |
