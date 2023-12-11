---
title: Migrate Data from MariaDB to TiDB
summary: Learn how to migrate data from MariaDB to TiDB.
---

# Migrate Data from MariaDB to TiDB

This document describes how to migrate data from a MariaDB Server installation to a TiDB Cluster.

## Prerequisites

- [Install Dumpling and TiDB Lightning](/migration-tools.md).
- Setup [DM](/dm/dm-overview.md)
- Make sure you have the required privileges on the MariaDB server that are required for Dumpling to export data.

Choose the right migration strategy:

The first strategy is a [_Dump and Restore_](#dump-and-restore). This works will all versions of MariaDB. The drawback of this strategy is that it needs more downtime.

The second strategy is to [_Replicate data_](#replicate-data) from MariaDB to TiDB with DM (Data Migration). TiDB Data Migration (DM) doesn't support all versions of MariaDB. The list of supported versions is listed on the [DM Compatibility Catalog](/dm/dm-compatibility-catalog.md#compatibility-catalog-of-tidb-data-migration).

Besides these two strategies there might be other strategies available specifically to your situation. For example you might use the functionality of your ORM to re-deploy and migrate your data or you might be able to modify your application to write and read from both MariaDB and TiDB while the migration is ongoing.

Note that only the first two strategies are discussed here.

## Check Compatibility

TiDB is made to be [compatible with MySQL](/mysql-compatibility.md) and MySQL and MariaDB have a lot of functionality in common. However there might be MariaDB specific features that might not be compatible with TiDB that you should be aware of before migrating. 

Besides checking the items in this section we suggest that you also check the [Compatibility & Differences](https://mariadb.com/kb/en/compatibility-differences/) in the MariaDB documentation.

### Authentication

The [security compatibility](/security-compatibility-with-mysql.md) page lists which authentication methods are supported by TiDB. There are a few authentication method's in MariaDB that are not supported in TiDB. This means that you might have to create a new password hash for the account or take other measures that are authentication method specific.

To check what authentication methods are used you can run the following statement:

```sql
SELECT
  plugin,
  COUNT(*)
FROM
  mysql.user
GROUP BY
  plugin;
```

```
+-----------------------+----------+
| plugin                | COUNT(*) |
+-----------------------+----------+
| mysql_native_password |       11 |
+-----------------------+----------+
1 row in set (0.002 sec)
```

### System versioned tables

[System versioned tables](https://mariadb.com/kb/en/system-versioned-tables/) are not supported by TiDB. However, TiDB does support [`AS OF TIMESTAMP`](/as-of-timestamp.md) which may replace some of the use cases of system versioned tables.

You can check for affected tables with the following statement

```sql
SELECT
  TABLE_SCHEMA,
  TABLE_NAME
FROM
  information_schema.tables
WHERE
  TABLE_TYPE='SYSTEM VERSIONED';
```

```
+--------------+------------+
| TABLE_SCHEMA | TABLE_NAME |
+--------------+------------+
| test         | t          |
+--------------+------------+
1 row in set (0.005 sec)
```

To remove system versioning use the `ALTER TABLE` statement:

```
MariaDB [test]> ALTER TABLE t DROP SYSTEM VERSIONING;
Query OK, 0 rows affected (0.071 sec)
Records: 0  Duplicates: 0  Warnings: 0
```

### Sequences

Both MariaDB and TiDB support [`CREATE SEQUENCE`](/sql-statements/sql-statement-create-sequence.md). However this is currently not supported by DM. It is recommended to not create, modify or remove sequences during the migration and to test this specifically after migration.

To check if you're using sequences, run the following statement.

```sql
SELECT
  TABLE_SCHEMA,
  TABLE_NAME
FROM
  information_schema.tables
WHERE
  TABLE_TYPE='SEQUENCE';
```

```
+--------------+------------+
| TABLE_SCHEMA | TABLE_NAME |
+--------------+------------+
| test         | s1         |
+--------------+------------+
1 row in set (0.016 sec)
```

### Storage engines

MariaDB offers storage engines for local data like `InnoDB`, `MyISAM` and `Aria`. While the data format isn't directly supported by TiDB migrating these works fine. However there are also engines that place data outside of the server like the `CONNECT` storage engine and `Spider`. While you can migrate the data of these kinds of tables to TiDB, TiDB doesn't provide the functionality to store data external to the TiDB cluster.

To see what storage engines you're using you can run the following statement:

```sql
SELECT
  ENGINE,
  COUNT(*)
FROM
  information_schema.tables
GROUP BY
  ENGINE;
```

```
+--------------------+----------+
| ENGINE             | COUNT(*) |
+--------------------+----------+
| NULL               |      101 |
| Aria               |       38 |
| CSV                |        2 |
| InnoDB             |        6 |
| MEMORY             |       67 |
| MyISAM             |        1 |
| PERFORMANCE_SCHEMA |       81 |
+--------------------+----------+
7 rows in set (0.009 sec)
```

### Syntax

MariaDB supports the `RETURNING` keyword for `DELETE`, `INSERT` and `REPLACE` statements. TiDB doesn't support this. You might want to look into your application and query logging to see if you're affected by this.

### Data types

MariaDB supports some datatypes that TiDB doesn't support like `UUID`, `INET4` and `INET6`.

To check for these datatypes you can run the following statement

```sql
SELECT
  TABLE_SCHEMA,
  TABLE_NAME,
  COLUMN_NAME,
  DATA_TYPE
FROM
  information_schema.columns
WHERE
  DATA_TYPE IN('INET4','INET6','UUID');
```

```
+--------------+------------+-------------+-----------+
| TABLE_SCHEMA | TABLE_NAME | COLUMN_NAME | DATA_TYPE |
+--------------+------------+-------------+-----------+
| test         | u1         | u           | uuid      |
| test         | u1         | i4          | inet4     |
| test         | u1         | i6          | inet6     |
+--------------+------------+-------------+-----------+
3 rows in set (0.026 sec)

```

### Character set and collation

TiDB doesn't support the `latin1_swedish_ci` collation that is often used in MariaDB.

To see what collations TiDB supports you can run this statement on TiDB:

```sql
SHOW COLLATION;
```

```
+--------------------+---------+-----+---------+----------+---------+
| Collation          | Charset | Id  | Default | Compiled | Sortlen |
+--------------------+---------+-----+---------+----------+---------+
| ascii_bin          | ascii   |  65 | Yes     | Yes      |       1 |
| binary             | binary  |  63 | Yes     | Yes      |       1 |
| gbk_bin            | gbk     |  87 |         | Yes      |       1 |
| gbk_chinese_ci     | gbk     |  28 | Yes     | Yes      |       1 |
| latin1_bin         | latin1  |  47 | Yes     | Yes      |       1 |
| utf8_bin           | utf8    |  83 | Yes     | Yes      |       1 |
| utf8_general_ci    | utf8    |  33 |         | Yes      |       1 |
| utf8_unicode_ci    | utf8    | 192 |         | Yes      |       1 |
| utf8mb4_0900_ai_ci | utf8mb4 | 255 |         | Yes      |       1 |
| utf8mb4_0900_bin   | utf8mb4 | 309 |         | Yes      |       1 |
| utf8mb4_bin        | utf8mb4 |  46 | Yes     | Yes      |       1 |
| utf8mb4_general_ci | utf8mb4 |  45 |         | Yes      |       1 |
| utf8mb4_unicode_ci | utf8mb4 | 224 |         | Yes      |       1 |
+--------------------+---------+-----+---------+----------+---------+
13 rows in set (0.0012 sec)
```

To check what collations the columns of your current tables are using you can use this statement:

```sql
SELECT
  TABLE_SCHEMA,
  COLLATION_NAME,
  COUNT(*)
FROM
  information_schema.columns
GROUP BY
  TABLE_SCHEMA, COLLATION_NAME
ORDER BY
  COLLATION_NAME;
```

```
+--------------------+--------------------+----------+
| TABLE_SCHEMA       | COLLATION_NAME     | COUNT(*) |
+--------------------+--------------------+----------+
| sys                | NULL               |      562 |
| test               | NULL               |       14 |
| mysql              | NULL               |       84 |
| performance_schema | NULL               |      892 |
| information_schema | NULL               |      421 |
| mysql              | latin1_swedish_ci  |       34 |
| performance_schema | utf8mb3_bin        |       38 |
| mysql              | utf8mb3_bin        |       61 |
| sys                | utf8mb3_bin        |       40 |
| information_schema | utf8mb3_general_ci |      375 |
| performance_schema | utf8mb3_general_ci |      244 |
| sys                | utf8mb3_general_ci |      386 |
| mysql              | utf8mb3_general_ci |       67 |
| mysql              | utf8mb4_bin        |        8 |
+--------------------+--------------------+----------+
14 rows in set (0.045 sec)
```

See also [Character Set and Collation](/character-set-and-collation.md)

## Dump and Restore

This method would assume you would take your application offline, then migrate the data and then re-configure your application to use the migrated data.

It is strongly recommended to first do this on a test or development instance of your application before doing it in production. This is both to check for possible compatibility issues as to get insight into how much time this would take.

### D1. Stop your application

Take your application offline. This ensures there are no modifications made to the data in MariaDB during or after the migration.

### D2. Dump the data

For this the first step is to dump data in MariaDB with the `tiup dumpling` command.

```
tiup dumpling --port 3306 --host 127.0.0.1 --user root --password secret -F 256MB  -o /data/backup
```

### D3. Restore the data

For this step we will use the `tiup tidb-lightning` command. Please see [Get Started with TiDB Lightning](/get-started-with-tidb-lightning.md) for how to configure TiDB Lightning and how to run it.

### D4. User accounts and permissions

See [Users and grants](#users-and-grants) below for how to migrate your users and permissions.

### D5. Reconfigure your application

Here you would change the application configuration so that it now connects to the TiDB server.

### D6. Cleanup

Once you have verified that the migration is succesful you can make a final backup of the data in MariaDB and stop the server. This also means you can stop and remove the DM cluster.

## Replicate data

To use Data Migration (DM) we need to deploy a set of DM services either with  [TiUP Cluster](/dm/deploy-a-dm-cluster-using-tiup.md) or with [TiDB Operator](/tidb-operator-overview.md). After this we will use `dmctl` to configure the DM services.

### R1. Prepare

Make sure that binlogs are enabled on MariaDB and that the `binlog_format` is set to `ROW`. It is also recommended to set `binlog_annotate_row_events=OFF` and `log_bin_compress=OFF`.

You will also need an account with the `SUPER` permission or with the `BINLOG MONITOR` and `REPLICATION MASTER ADMIN` permissions. This account also needs read permission for the schemas you're going to migrate.

If you're not using an account with the `SUPER` permission then you might have to add the following to the DM configuration as TiDB doesn't yet know how to check for MariaDB specific permissions.

```
ignore-checking-items: ["replication_privilege"]
```

### R2. Replication

Note that it is not required to first copy the initial data as you would do with MariaDB to MariaDB replication, DM will do this for you.

Please follow the [Quick Start Guide for TiDB Data Migration](/dm/quick-start-with-dm.md) to replicate your data from MariaDB to TiDB.

### R3. User accounts and permissions

See [Users and grants](#users-and-grants) below for how to migrate your users and permissions.

### R4. Testing

Once your data is replicated you can run read-only queries on it to validate it. Please see the section below about [Testing your application](#testing-your-application) for more details on this.

### R5. Switchover

First stop your application. Then monitor the replication delay, which should go to 0 seconds. Then you can change the configuration of your application so that it connects to TiDB and start it again.

To check for replication delay run [`query-status <taskname>`](/dm/dm-query-status.md#detailed-query-result) via `dmctl` and check for `"synced: true"` in the `subTaskStatus`.

### R6. Cleanup

Once you have verified that the migration is succesful you can make a final backup of the data in MariaDB and stop the server. This also means you can stop and remove the DM cluster.

## Users and grants

You can use [`pt-show-grants`](https://docs.percona.com/percona-toolkit/pt-show-grants.html), which is part of the Percona Toolkit to export users and grants from MariaDB and load these into TiDB.

## Testing your application

While it is possible to use generic tools like `sysbench` that you could use for testing it is highly recommended to test something that's specific to your application. You could for example run a copy of your application against a TiDB cluster with a temporary copy of your data. 

This makes sure your application compatibility and performance with TiDB is tested. Please monitor the log files of your application and TiDB to see if there are any warnings that might need to be addressed. This also makes sure that the database driver that your application is using (for example MySQL Connector/J for Java based applications) is tested. You might want to use an application like JMeter to put some load on your application if needed.

## Validation

You can use [sync-diff-inspector](/sync-diff-inspector/sync-diff-inspector-overview.md) to validate if the data in MariaDB and TiDB are identical.
