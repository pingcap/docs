---
title: TiDB Basic Features
summary: Learn about the basic features of TiDB.
aliases: ['/docs/stable/basic-features/','/docs/v4.0/basic-features/']
---

# TiDB Basic Features

This document introduces the basic features of TiDB.

## Data types

- Numeric types: `BIT`, `BOOL|BOOLEAN`, `SMALLINT`, `MEDIUMINT`, `INT|INTEGER`, `BIGINT`, `FLOAT`, `DOUBLE`, `DECIMAL`.

- Date and time types: `DATE`, `TIME`, `DATETIME`, `TIMESTAMP`, `YEAR`.

- String types: `CHAR`, `VARCHAR`, `TEXT`, `TINYTEXT`, `MEDIUMTEXT`, `LONGTEXT`, `BINARY`, `VARBINARY`, `BLOB`, `TINYBLOB`, `MEDIUMBLOB`, `LONGBLOB`, `ENUM`, `SET`.

- The `JSON` type.

## Operators

- Arithmetic operators, bit operators, comparison operators, logical operators, date and time operators, and so on.

## Character sets and collations

- Character sets: `UTF8`, `UTF8MB4`, `BINARY`, `ASCII`, `LATIN1`.

- Collations: `UTF8MB4_GENERAL_CI`, `UTF8MB4_GENERAL_BIN`, `UTF8_GENERAL_CI`, `UTF8_GENERAL_BIN`, `BINARY`.

## Functions

- Control flow functions, string functions, date and time functions, bit functions, data type conversion functions, data encryption and decryption functions, compression and decompression functions, information functions, JSON functions, aggregation functions, window functions, and so on.

## SQL statements

<<<<<<< HEAD
- Fully supports standard Data Definition Language (DDL) statements, such as `CREATE`, `DROP`, `ALTER`, `RENAME`, `TRUNCATE`, and so on.

- Fully supports standard Data Manipulation Language (DML) statements, such as `INSERT`, `REPLACE`, `SELECT`, subqueries, `UPDATE`, `LOAD DATA`, and so on.

- Fully supports standard transactional and locking statements, such as `START TRANSACTION`, `COMMIT`, `ROLLBACK`, `SET TRANSACTION`, and so on.

- Fully supports standard database administration statements, such as `SHOW`, `SET`, and so on.

- Fully supports standard utility statements, such as `DESCRIBE`, `EXPLAIN`, `USE`, and so on.

- Fully supports the `GROUP BY` and `ORDER BY` clauses.

- Fully supports the standard `LEFT OUTER JOIN` and `RIGHT OUTER JOIN` SQL statements.

- Fully supports the standard SQL table and column aliases.

## Partitioning

- Supports Range partitioning
- Supports Hash partitioning

## Views

- Supports general views

## Constraints

- Supports non-empty constraints
- Supports primary key constraints
- Supports unique constraints

## Security

- Supports privilege management based on RBAC (role-based access control)
- Supports password management
- Supports communication and data encryption
- Supports IP allowlist
- Supports audit

## Tools

- Supports fast backup
- Supports data migration from MySQL to TiDB using tools
- Supports deploying and maintaining TiDB using tools
=======
| SQL statements [^2]                                      | 6.1 | 6.0 | 5.4          |   5.3    |   5.2    |   5.1    |   5.0    |   4.0    |
| ------------------------------------------------------------ | :--: | :--: | ------------ | :----------: | :----------: | :----------: | :----------: | :----------: |
| Basic `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `REPLACE`     | Y | Y  | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| `INSERT ON DUPLICATE KEY UPDATE`                             | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| `LOAD DATA INFILE`                                           | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| `SELECT INTO OUTFILE`                                        | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| `INNER JOIN`, `LEFT\|RIGHT [OUTER] JOIN`                     | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| `UNION`, `UNION ALL`                                         | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [`EXCEPT` and `INTERSECT` operators](/functions-and-operators/set-operators.md) | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      N       |
| `GROUP BY`, `ORDER BY`                                       | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Window Functions](/functions-and-operators/window-functions.md) | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Common Table Expressions (CTE)](/sql-statements/sql-statement-with.md)| Y | Y  | Y            |      Y       |      Y       |      Y       |      N       |      N       |
| `START TRANSACTION`, `COMMIT`, `ROLLBACK`                    | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [`EXPLAIN`](/sql-statements/sql-statement-explain.md)        | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [User-defined variables](/user-defined-variables.md)         | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |
| [`BATCH [ON COLUMN] LIMIT INTEGER DELETE`](/sql-statements/sql-statement-batch.md) | Y | N | N | N | N | N | N | N |

## Advanced SQL features

| Advanced SQL features                                    | 6.1 | 6.0 | 5.4          |   5.3    |   5.2    |   5.1    |   5.0   |   4.0    |
| ------------------------------------------------------------ | :--: | :--: | ------------ | :----------: | :----------: | :----------: | :----------: | :----------: |
| [Prepared statement cache](/sql-prepared-plan-cache.md)       | Y | Y | Y            |      Y       | Experimental | Experimental | Experimental | Experimental |
| [SQL plan management (SPM)](/sql-plan-management.md)         | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Coprocessor cache](/coprocessor-cache.md)                   | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       | Experimental |
| [Stale Read](/stale-read.md)                                 | Y | Y | Y            |      Y       |      Y       |      Y       |      N       |      N       |
| [Follower reads](/follower-read.md)                          | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Read historical data (tidb_snapshot)](/read-historical-data.md) | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Optimizer hints](/optimizer-hints.md)                       | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [MPP Execution Engine](/explain-mpp.md)                       | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      N       |
| [Index Merge](/explain-index-merge.md)                  | Y | Y | Y            | Experimental | Experimental | Experimental | Experimental | Experimental |
| [Placement Rules in SQL](/placement-rules-in-sql.md)         | Y | Y | Experimental | Experimental |      N       |      N       |      N       |      N       |

## Data definition language (DDL)

| Data definition language (DDL)                           | 6.1 | 6.0 | 5.4          |   5.3    |   5.2    |   5.1    |   5.0    |   4.0    |
| ------------------------------------------------------------ | :--: | :--: | ------------ | :----------: | :----------: | :----------: | :----------: | :----------: |
| Basic `CREATE`, `DROP`, `ALTER`, `RENAME`, `TRUNCATE`        | Y | Y  | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Generated columns](/generated-columns.md)                  | Experimental | Experimental| Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |
| [Views](/views.md)                                           | Y | Y  | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Sequences](/sql-statements/sql-statement-create-sequence.md) | Y | Y  | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Auto increment](/auto-increment.md)                         | Y | Y  | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Auto random](/auto-random.md)                               | Y | Y  | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [DDL algorithm assertions](/sql-statements/sql-statement-alter-table.md) | Y | Y  | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Multi-schema change: add columns](/system-variables.md#tidb_enable_change_multi_schema)                           | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |
| [Change column type](/sql-statements/sql-statement-modify-column.md) | Y | Y  | Y            |      Y       |      Y       |      Y       |      N       |      N       |
| [Temporary tables](/temporary-tables.md)                    | Y | Y   | Y            |      Y       |      N       |      N       |      N       |      N       |

## Transactions

| Transactions                                             | 6.1 | 6.0 | 5.4  | 5.3 | 5.2 | 5.1 | 5.0 | 4.0 |
| ------------------------------------------------------------ | :--: | :-----| ---- | :-----: | :-----: | :-----: | :-----: | :-----: |
| [Async commit](/system-variables.md#tidb_enable_async_commit-new-in-v50) | Y | Y | Y    |    Y    |    Y    |    Y    |    Y    |    N    |
| [1PC](/system-variables.md#tidb_enable_1pc-new-in-v50)       | Y | Y | Y    |    Y    |    Y    |    Y    |    Y    |    N    |
| [Large transactions (10GB)](/transaction-overview.md#transaction-size-limit) | Y | Y | Y    |    Y    |    Y    |    Y    |    Y    |    Y    |
| [Pessimistic transactions](/pessimistic-transaction.md)      | Y | Y | Y    |    Y    |    Y    |    Y    |    Y    |    Y    |
| [Optimistic transactions](/optimistic-transaction.md)        | Y | Y | Y    |    Y    |    Y    |    Y    |    Y    |    Y    |
| [Repeatable-read isolation (snapshot isolation)](/transaction-isolation-levels.md) | Y | Y | Y    |    Y    |    Y    |    Y    |    Y    |    Y    |
| [Read-committed isolation](/transaction-isolation-levels.md) | Y | Y | Y    |    Y    |    Y    |    Y    |    Y    |    Y    |

## Partitioning

| Partitioning                                             | 6.1 | 6.0| 5.4          |   5.3    |   5.2    |   5.1    |   5.0    | 4.0 |
| ------------------------------------------------------------ | :--: | :--: | ------------ | :----------: | :----------: | :----------: | :----------: | :-----: |
| [Range partitioning](/partitioned-table.md)                  | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |    Y    |
| [Hash partitioning](/partitioned-table.md)                   | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |    Y    |
| [List partitioning](/partitioned-table.md)                   | Y | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |    N    |
| [List COLUMNS partitioning](/partitioned-table.md)           | Y | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |    N    |
| [`EXCHANGE PARTITION`](/partitioned-table.md)                | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |    N    |
| [Dynamic Pruning](/partitioned-table.md#dynamic-pruning-mode) | Y | Experimental | Experimental | Experimental | Experimental | Experimental |      N       |    N    |

## Statistics

| Statistics                                               | 6.1 | 6.0 | 5.4          |   5.3    |   5.2    |   5.1   |   5.0    |   4.0    |
| ------------------------------------------------------------ | :--: | :--: | ------------ | :----------: | :----------: | :----------: | :----------: | :----------: |
| [CMSketch](/statistics.md)                                   | Disabled by default | Disabled by default | Disabled by default | Disabled by default | Y | Y | Y |      Y       |
| [Histograms](/statistics.md)                                 | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| Extended statistics (multiple columns)     | Experimental | Experimental| Experimental | Experimental | Experimental | Experimental | Experimental |      N       |
| [Statistics feedback](/statistics.md#automatic-update)       | Deprecated | Deprecated | Deprecated   | Experimental | Experimental | Experimental | Experimental | Experimental |
| [Automatically update statistics](/statistics.md#automatic-update) | Y | Y | Y | Y | Y | Y | Y | Y |
| [Fast Analyze](/system-variables.md#tidb_enable_fast_analyze) | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |
| [Dynamic pruning](/partitioned-table.md#dynamic-pruning-mode) | Y | Experimental | Experimental | Experimental | Experimental | Experimental | N | N |

## Security

| Security                                                 | 6.1 | 6.0 | 5.4  | 5.3 | 5.2 | 5.1 | 5.0 | 4.0 |
| ------------------------------------------------------------ | :--: | :--: | ---- | :-----: | :-----: | :-----: | :-----: | :-----: |
| [Transparent layer security (TLS)](/enable-tls-between-clients-and-servers.md) | Y | Y | Y    |    Y    |    Y    |    Y    |    Y    |    Y    |
| [Encryption at rest (TDE)](/encryption-at-rest.md)           | Y | Y | Y    |    Y    |    Y    |    Y    |    Y    |    Y    |
| [Role-based authentication (RBAC)](/role-based-access-control.md) | Y | Y | Y    |    Y    |    Y    |    Y    |    Y    |    Y    |
| [Certificate-based authentication](/certificate-authentication.md) | Y | Y | Y    |    Y    |    Y    |    Y    |    Y    |    Y    |
| `caching_sha2_password` authentication                       | Y | Y | Y    |    Y    |    Y    |    N    |    N    |    N    |
| [MySQL compatible `GRANT` system](/privilege-management.md)  | Y | Y | Y    |    Y    |    Y    |    Y    |    Y    |    Y    |
| [Dynamic Privileges](/privilege-management.md#dynamic-privileges) | Y | Y | Y    |    Y    |    Y    |    Y    |    N    |    N    |
| [Security Enhanced Mode](/system-variables.md#tidb_enable_enhanced_security) | Y | Y | Y    |    Y    |    Y    |    Y    |    N    |    N    |
| [Redacted Log Files](/log-redaction.md)                      | Y | Y | Y    |    Y    |    Y    |    Y    |    Y    |    N    |

## Data import and export

| Data import and export                                                                               | 6.1 | 6.0 | 5.4  | 5.3      | 5.2      | 5.1      | 5.0      | 4.0      |
|----------------------------------------------------------------------------------------------------------| :--: | :--: |:------------:|:------------:|:------------:|:------------:|:------------:|:------------:|
| [Fast Importer (TiDB Lightning)](/tidb-lightning/tidb-lightning-overview.md)                             | Y | Y  | Y           | Y            | Y            | Y            | Y            | Y            |
| mydumper logical dumper                                                                                  | Deprecated | Deprecated | Deprecated | Deprecated   | Deprecated   | Deprecated   | Deprecated   | Deprecated   |
| [Dumpling logical dumper](/dumpling-overview.md)                                                         | Y | Y | Y           | Y            | Y            | Y            | Y            | Y            |
| [Transactional `LOAD DATA`](/sql-statements/sql-statement-load-data.md)                                 | Y | Y  | Y           | Y            | Y            | Y            | Y            | N [^3]       |
| [Database migration toolkit (DM)](/migration-overview.md)                                               | Y | Y  | Y           | Y            | Y            | Y            | Y            | Y            |
| [TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md)                                                     | Y | Y  | Y   | Y    | Y    | Y    | Y    | Y    |
| [Change data capture (CDC)](/ticdc/ticdc-overview.md)                                                   | Y | Y  | Y           | Y            | Y            | Y            | Y            | Y            |

## Management, observability, and tools

| Management, observability, and tools                     | 6.1 | 6.0 | 5.4          |   5.3    |   5.2    |   5.1    |   5.0    |   4.0    |
| ------------------------------------------------------------ | :--: | :--: | ------------ | :----------: | :----------: | :----------: | :----------: | :----------: |
| [TiDB Dashboard UI](/dashboard/dashboard-intro.md)              | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [TiDB Dashboard Continuous Profiling](/dashboard/continuous-profiling.md)   | Y | Y | Experimental | Experimental |      N       |      N       |      N       |      N       |
| [TiDB Dashboard Top SQL](/dashboard/top-sql.md)                             | Y | Y | Experimental |      N       |      N       |      N       |      N       |      N       |
| [TiDB Dashboard SQL Diagnostics](/information-schema/information-schema-sql-diagnostics.md) | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |
| [Information schema](/information-schema/information-schema.md) | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Metrics schema](/metrics-schema.md)                        | Y | Y  | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Statements summary tables](/statement-summary-tables.md)    | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Slow query log](/identify-slow-queries.md)                 | Y | Y  | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [TiUP deployment](/tiup/tiup-overview.md)                   | Y | Y  | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| Ansible deployment                                           | N | N | N            |      N       |      N       |      N       |      N       |  Deprecated  |
| [Kubernetes operator](https://docs.pingcap.com/tidb-in-kubernetes/) | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Built-in physical backup](/br/backup-and-restore-use-cases.md) | Y | Y | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Global Kill](/sql-statements/sql-statement-kill.md)       | Y | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |
| [Lock View](/information-schema/information-schema-data-lock-waits.md) | Y | Y | Y            |      Y       |      Y       | Experimental | Experimental | Experimental |
| [`SHOW CONFIG`](/sql-statements/sql-statement-show-config.md) | Y | Y | Y | Y | Y | Y | Y | Y |
| [`SET CONFIG`](/dynamic-config.md)                           | Y | Experimental| Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |
| [DM WebUI](/dm/dm-webui-guide.md) | Experimental | Experimental | N | N | N | N | N | N |

[^1]: TiDB incorrectly treats latin1 as a subset of utf8. See [TiDB #18955](https://github.com/pingcap/tidb/issues/18955) for more details.

[^2]: See [Statement Reference](/sql-statements/sql-statement-select.md) for a full list of SQL statements supported.

[^3]: For TiDB v4.0, the `LOAD DATA` transaction does not guarantee atomicity.
>>>>>>> b8b52cc17 (correct experimental information in docs (#9803))
