---
title: DM-worker Introduction
summary: Learn the features of DM-worker.
---

# DM-worker Introduction

DM-worker is a component of TiDB Data Migration (DM) that executes tasks and subtasks assigned by DM-master. For a full and incremental migration, it dumps data from one MySQL-compatible source instance and loads the dumped data into the target TiDB cluster. It then reads the source binlog as a replication client, transforms and filters events, and applies them to the target. DM-master queries DM-worker for the status of sources and subtasks.

## Key concepts

- If a worker instance goes offline, DM-master can automatically reschedule its tasks to another available worker to resume the data replication. Note that this does not apply during a full export/import phase.
- A single DM-worker process connects to **one** upstream source database instance at a time. To migrate from multiple sources, such as when merging sharded tables, you must run multiple DM-worker processes.

> **Note:**
>
> A DM-worker is a MySQL-compatible binlog client, not a standby database replica server. It reads and replays data from a MySQL-compatible source to a TiDB target. To replicate data from a source TiDB cluster, use [TiCDC](/ticdc/ticdc-overview.md).

## DM-worker processing units

Depending on its task mode, a DM-worker subtask runs the dump, load, and binlog replication processing units. DM-worker can also run an optional relay log processing unit for its bound source.

### Relay log

Relay log is optional and disabled by default. When enabled, DM-worker stores upstream binlog events on the local disk before the binlog replication processing unit reads them. Enable relay log if a long-running full migration or a blocked task might outlast upstream binlog retention period, or if multiple tasks for the same source need to share a single binlog stream. Relay logging consumes disk, I/O, and CPU resources, and can increase replication latency. For configuration and operational details, see [DM relay log](/dm/relay-log.md).

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

> **Note:**
>
> - If you migrate from a managed MySQL service (such as Amazon RDS, Aurora, ApsaraDB RDS for MySQL, Azure Database for MySQL, or Google Cloud SQL) where `FLUSH TABLES WITH READ LOCK` (FTWRL) is not permitted, also grant the `LOCK TABLES` privilege. With the default `consistency=auto` setting, DM falls back to `LOCK TABLES` when FTWRL is unavailable.
>
>     ```sql
>     GRANT LOCK TABLES ON db1.* TO 'your_user'@'your_wildcard_of_host';
>     ```
>
> - If you also need to migrate the data from other databases into TiDB, make sure the same privileges are granted to the user of the respective databases.

#### MySQL and MariaDB (before MariaDB 10.5.2)

For MySQL, and for MariaDB versions earlier than 10.5.2, the user must have the following privileges:

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

For a full data export from MariaDB earlier than 10.5.2, also grant `PROCESS` so that the dump unit can query InnoDB metadata:

```sql
GRANT PROCESS ON *.* TO 'your_user'@'your_wildcard_of_host';
```

#### MariaDB 10.5.2 to 10.5.8

Starting from [MariaDB 10.5.2](https://mariadb.com/docs/release-notes/community-server/old-releases/10.5/10.5.2), the `REPLICATION CLIENT` privilege is renamed to `BINLOG MONITOR`, and several replication statements use new privileges created by splitting `SUPER`. For MariaDB 10.5.2 to 10.5.8, the user must have the following privileges:

| Privilege | Scope | Description |
|:---|:---|:---|
| `SELECT` | Tables | Required for full data export. |
| `PROCESS` | Global | Required for InnoDB metadata queries during full data export. |
| `RELOAD` | Global | Required for `FLUSH TABLES WITH READ LOCK`. |
| `BINLOG MONITOR` | Global | Renamed from `REPLICATION CLIENT`; allows monitoring the binlog. |
| `REPLICATION SLAVE` | Global | Allows reading binlog events. |
| `REPLICATION SLAVE ADMIN` | Global | Allows managing replication status (for example, `SHOW SLAVE STATUS`). |
| `REPLICATION MASTER ADMIN`| Global | Allows monitoring the master (for example, `SHOW SLAVE HOSTS`). |

To grant these privileges, execute the following statement:

```sql
GRANT PROCESS, RELOAD, BINLOG MONITOR, REPLICATION SLAVE, REPLICATION SLAVE ADMIN, REPLICATION MASTER ADMIN ON *.* TO 'your_user'@'your_wildcard_of_host';
GRANT SELECT ON `db1`.* TO 'your_user'@'your_wildcard_of_host';
```

#### MariaDB 10.5.9 or later

Starting from [MariaDB 10.5.9](https://mariadb.com/docs/release-notes/community-server/old-releases/10.5/10.5.9), `SHOW SLAVE STATUS` and `SHOW REPLICA STATUS` require the `REPLICA MONITOR` privilege. MariaDB displays this privilege as `SLAVE MONITOR` in `SHOW GRANTS`. Grant the privileges listed for MariaDB 10.5.2 to 10.5.8 plus `REPLICA MONITOR`:

```sql
GRANT PROCESS, RELOAD, BINLOG MONITOR, REPLICATION SLAVE, REPLICATION SLAVE ADMIN, REPLICATION MASTER ADMIN, REPLICA MONITOR ON *.* TO 'your_user'@'your_wildcard_of_host';
GRANT SELECT ON `db1`.* TO 'your_user'@'your_wildcard_of_host';
```

> **Note:**
>
> Because MariaDB reports these privileges differently from MySQL, `dmctl check-task` might report privilege errors even when the account has the required privileges.
>
> For DM v8.5.6, if the precheck returns `[code=26005] fail to check synchronization configuration` for the replication privilege, dump privilege, or dump connection number check, add only the following items to the task configuration file:
>
> ```yaml
> ignore-checking-items:
>   - replication_privilege
>   - dump_privilege
>   - conn_number
> ```
>
> This workaround skips only the three checks affected by the MariaDB privilege parser. Before using it, manually verify the corresponding privileges and connection limit. For more information, see [DM precheck](/dm/dm-precheck.md).

> **Note:**
>
> On some older MariaDB releases, `PROCESS` is not sufficient for the dump unit to query InnoDB metadata. With DM v8.5.6, this behavior occurs when the dump unit queries `INNODB_TABLESPACES_SCRUBBING` on MariaDB 10.4.34, or `INNODB_TABLESPACES_ENCRYPTION` on MariaDB 10.5.1 and 10.5.2. In the same smoke tests, MariaDB 10.5.9, 10.6.13, and 10.11.16 complete without `SUPER`.
>
> If the dump unit returns the following error, grant `SUPER`. Because `SUPER` is a broad privilege, grant it only when this exact error occurs and your security policy permits it.
>
> ```
> Error 1227 (42000): Access denied; you need (at least one of) the SUPER privilege(s) for this operation
> ```

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

The following table lists the minimal privileges required by each processing unit for MySQL and for MariaDB versions earlier than 10.5.2. For MariaDB 10.5.2 and later, refer to the privilege tables in the preceding section.

| Processing unit | Minimal upstream (MySQL/MariaDB) privilege | Minimal downstream (TiDB) privilege | Minimal system privilege |
|:----|:--------------------|:------------|:----|
| Relay log | `REPLICATION SLAVE` (reads the binlog)<br/>`REPLICATION CLIENT` (`SHOW MASTER STATUS`, `SHOW SLAVE STATUS`) | NULL | Read/Write local files |
| Dump | `SELECT`<br/>`RELOAD` (`FLUSH TABLES WITH READ LOCK`)<br/>`PROCESS` (MariaDB only, for InnoDB metadata queries) | NULL | Write local files |
| Load | NULL | `SELECT` (Query the checkpoint history)<br/>`CREATE` (creates a database/table)<br/>`DELETE` (deletes checkpoint)<br/>`INSERT` (Inserts the Dump data) | Read/Write local files |
| Binlog replication | `REPLICATION SLAVE` (reads the binlog)<br/>`REPLICATION CLIENT` (`SHOW MASTER STATUS`, `SHOW SLAVE STATUS`) | `SELECT` (shows the index and column)<br/>`INSERT` (DML)<br/>`UPDATE` (DML)<br/>`DELETE` (DML)<br/>`CREATE` (creates a database/table)<br/>`DROP` (drops databases/tables)<br/>`ALTER` (alters a table)<br/>`INDEX` (creates/drops an index)| Read/Write local files |
