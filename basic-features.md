---
title: TiDB Basic Features
summary: Learn about the basic features of TiDB.
aliases: ['/docs/dev/basic-features/']
---

# TiDB Features

The following table provides an overview of the feature development history of TiDB. Note that features under active development may change before final release.

| Data types, functions, and operators                                                  | Development | 4.0 | 3.1 | 3.0 | 2.1 |
|--------------------------------------------------------------------------------------|:-----:|:---:|:---:|:---:|:---:|
| [Numeric types](/data-type-numeric.md)                                               | Y     | Y   | Y   | Y   | Y   |
| [Date and time types](/data-type-date-and-time.md)                                   | Y     | Y   | Y   | Y   | Y   |
| [String types](/data-type-string.md)                                                 | Y     | Y   | Y   | Y   | Y   |
| [JSON type](/data-type-json.md)                                                      | Experimental | Experimental | Experimental | Experimental | Experimental |
| [Control flow functions](/functions-and-operators/control-flow-functions.md)         | Y     | Y   | Y   | Y   | Y   |
| [String functions](/functions-and-operators/string-functions.md)                     | Y     | Y   | Y   | Y   | Y   |
| [Numeric functions and operators](/functions-and-operators/numeric-functions-and-operators.md) | Y     | Y   | Y   | Y   | Y   |
| [Date and time functions](/functions-and-operators/date-and-time-functions.md)       | Y     | Y   | Y   | Y   | Y   |
| [Bit functions and operators](/functions-and-operators/bit-functions-and-operators.md) | Y     | Y   | Y   | Y   | Y   |
| [Cast functions and operators](/functions-and-operators/cast-functions-and-operators.md) | Y     | Y   | Y   | Y   | Y   |
| [Encryption and compression functions](/functions-and-operators/encryption-and-compression-functions.md) | Y     | Y   | Y   | Y   | Y   |
| [Information functions](/functions-and-operators/information-functions.md)           | Y     | Y   | Y   | Y   | Y   |
| [JSON functions](/functions-and-operators/json-functions.md)                         | Experimental | Experimental | Experimental | Experimental | Experimental |
| [Aggregation functions](/functions-and-operators/aggregate-group-by-functions.md)    | Y     | Y   | Y   | Y   | Y   |
| [Window functions](/functions-and-operators/window-functions.md)                     | Y     | Y   | Y   | Y   | Y   |
| [Miscellaneous functions](/functions-and-operators/miscellaneous-functions.md)       | Y     | Y   | Y   | Y   | Y   |
| [Operators](/functions-and-operators/operators.md)                                   | Y     | Y   | Y   | Y   | Y   |
| [**Character sets**](/character-set-and-collation.md)                                | **Development** | **4.0** | **3.1** | **3.0** | **2.1** |
| `utf8`                                                                               | Y     | Y   | Y   | Y   | Y   |
| `utf8mb4`                                                                            | Y     | Y   | Y   | Y   | Y   |
| `ascii` [^1]                                                                         | Y     | Y   | Y   | Y   | Y   |
| `latin1`                                                                             | Y     | Y   | Y   | Y   | Y   |
| `binary`                                                                             | Y     | Y   | Y   | Y   | Y   |
| [**Collations**](/character-set-and-collation.md)                                    | **Development** | **4.0** | **3.1** | **3.0** | **2.1** |
| `utf8_bin`                                                                           | Y     | Y   | Y   | Y   | Y   |
| `utf8_general_ci`                                                                    | Experimental | Experimental | N   | N   | N   |
| `utf8_unicode_ci`                                                                    | Experimental | Experimental | N   | N   | N   |
| `utf8mb4_bin`                                                                        | Y     | Y   | Y   | Y   | Y   |
| `utf8mb4_general_ci`                                                                 | Experimental     | Experimental   | N   | N   | N  |
| `utf8mb4_unicode_ci`                                                                 | Experimental     | Experimental   | N   | N   | N  |
| `ascii_bin`                                                                          | Y     | Y   | Y   | Y   | Y   |
| `latin1_bin`                                                                         | Y     | Y   | Y   | Y   | Y   |
| `binary`                                                                             | Y     | Y   | Y   | Y   | Y   |
| **Indexing and constraints**                                                         | **Development** | **4.0** | **3.1** | **3.0** | **2.1** |
| [Expression indexes](/sql-statements/sql-statement-create-index.md#expression-index) | Experimental | Experimental | N   | N   | N   |
| [Columnar storage (TiFlash)](/tiflash/tiflash-overview.md)                           | Y     | Y   | Y   | N   | N   |
| [RocksDB engine](/storage-engine/rocksdb-overview.md)                                | Y     | Y   | Y   | Y   | Y   |
| [Titan plugin](/storage-engine/titan-overview.md)                                    | Y     | Y   | Experimental | Experimental | Experimental |
| [Invisible indexes](/sql-statements/sql-statement-add-index.md)                      | Y     | N   | N   | N   | N   |
| [Composite `PRIMARY KEY`](/constraints.md)                                           | Y     | Y   | Y   | Y   | Y   |
| [Unique indexes](/constraints.md)                                                    | Y     | Y   | Y   | Y   | Y   |
| [Clustered index on integer `PRIMARY KEY`](/constraints.md)                          | Y     | Y   | Y   | Y   | Y   |
| [Clustered index on composite or non-integer key](/constraints.md)                   | Experimental | N | N | N | N  |
| **SQL statements** [^2]                                                              | **Development** | **4.0** | **3.1** | **3.0** | **2.1** |
| Basic `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `REPLACE`                              | Y     | Y   | Y   | Y   | Y   |
| `INSERT ON DUPLICATE KEY UPDATE`                                                     | Y     | Y   | Y   | Y   | Y   |
| `LOAD DATA INFILE`                                                                   | Y     | Y   | Y   | Y   | Y   |
| `SELECT INTO OUTFILE`                                                                | Y     | Y   | N   | N   | N   |
| `INNER JOIN`, `LEFT\|RIGHT [OUTER] JOIN`                                             | Y     | Y   | Y   | Y   | Y   |
| `UNION`, `UNION ALL`                                                                 | Y     | Y   | Y   | Y   | Y   |
| `GROUP BY`, `ORDER BY`                                                               | Y     | Y   | Y   | Y   | Y   |
| `START TRANSACTION`, `COMMIT`, `ROLLBACK`                                            | Y     | Y   | Y   | Y   | Y   |
| [`EXPLAIN`](/sql-statements/sql-statement-explain.md)                                | Y     | Y   | Y   | Y   | Y   |
| [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)                | Y     | Y   | Y   | Y   | Y   |
| **Advanced SQL Features**                                                            | **Development** | **4.0** | **3.1** | **3.0** | **2.1** |
| Prepared statement cache                                                             | Y     | Experimental   | N   | N   | N   |
| [SQL plan management (SPM)](/sql-plan-management.md)                                 | Y     | Y   | N   | N   | N   |
| [Coprocessor cache](/coprocessor-cache.md)                                           | Y     | Experimental | N | N | N |
| [Placement rules](/configure-placement-rules.md)                                     | Y     | Experimental | N   | N   | N   |
| [Follower reads](/follower-read.md)                                                  | Y     | Y   | Y   | N   | N   |
| [Read historical data (tidb_snapshot)](/read-historical-data.md)                     | Y     | Y   | Y   | Y   | Y   |
| [Optimizer hints](/optimizer-hints.md)                                               | Y     | Y   | Y   | Y   | Y   |
| **Data definition language (DDL)**                                                   | **Development** | **4.0** | **3.1** | **3.0** | **2.1** |
| Basic `CREATE`, `DROP`, `ALTER`, `RENAME`, `TRUNCATE`                                | Y     | Y   | Y   | Y   | Y   |
| [Generated columns](/generated-columns.md)                                           | Experimental | Experimental | Experimental | Experimental | Experimental |
| [Views](/views.md)                                                                   | Y     | Y   | Y   | Y   | N   |
| [Sequences](/sql-statements/sql-statement-create-sequence.md)                        | Y     | Y   | N   | N   | N   |
| [Auto increment](/auto-increment.md)                                                 | Y     | Y   | Y   | Y   | Y   |
| [Auto random](/auto-random.md)                                                       | Y     | Y   | N   | N   | N   |
| DDL algorithm assertions                                                             | Y     | Y   | N   | N   | N   |
| Multi schema change: add column(s)                                                   | Y     | N   | N   | N   | N   |
| **Transactions**                                                                     | **Development** | **4.0** | **3.1** | **3.0** | **2.1** |
| Async commit                                                                         | Y     | N   | N   | N   | N   |
| Large transactions (10GB)                                                            | Y     | Y   | N   | N   | N   |
| [Pessimistic transactions](/pessimistic-transaction.md)                              | Y     | Y   | Y   | Y   | Experimental |
| [Optimistic transactions](/optimistic-transaction.md)                                | Y     | Y   | Y   | Y   | Y   |
| [Repeatable-read isolation (snapshot isolation)](/transaction-isolation-levels.md)   | Y     | Y   | Y   | Y   | Y   |
| [Read-committed isolation](/transaction-isolation-levels.md)                         | Y     | Y   | N   | N   | N   |
| **Partitioning**                                                                     | **Development** | **4.0** | **3.1** | **3.0** | **2.1** |
| [Range partitioning](/partitioned-table.md)                                          | Y     | Y   | Y   | Y   | N   |
| [Hash partitioning](/partitioned-table.md)                                           | Y     | Y   | Y   | Y   | N   |
| **Statistics**                                                                       | **Development** | **4.0** | **3.1** | **3.0** | **2.1** |
| [CMSketch](/statistics.md)                                                           | Deprecated | Y   | Y   | Y   | Y   |
| [Histograms](/statistics.md)                                                         | Y     | Y   | Y   | Y   | Y   |
| [Extended statistics (multiple columns)](/statistics.md)                             | Experimental | N   | N   | N   | N   |
| **Security**                                                                         | **Development** | **4.0** | **3.1** | **3.0** | **2.1** |
| [Transparent layer security (TLS)](/enable-tls-between-clients-and-servers.md)       | Y     | Y   | Y   | Y   | Y   |
| [Encryption at rest (TDE)](/encryption-at-rest.md)                                   | Y     | Y   | N   | N   | N   |
| [Role-based authentication (RBAC)](/role-based-access-control.md)                    | Y     | Y   | Y   | Y   | N   |
| [Certificate-based authentication](/certificate-authentication.md)                   | Y     | Y   | Y   | Y   | N   |
| Support for MySQL 8.0 clients                                                        | Y     | Y   | N   | N   | N   |
| [MySQL compatible `GRANT` system](/privilege-management.md)                          | Y     | Y   | Y   | Y   | Y   |
| Auditing                                                                             | Y     | Y   | Y   | Y   | Y   |
| **Data import and export**                                                           | **Development** | **4.0** | **3.1** | **3.0** | **2.1** |
| [Fast Importer (TiDB Lightning)](/tidb-lightning/tidb-lightning-overview.md)         | Y     | Y   | Y   | Y   | Y   |
| [mydumper logical dumper](/mydumper-overview.md)                                     | Deprecated | Deprecated | Y   | Y   | Y   |
| [Dumpling logical dumper](/dumpling-overview.md)                                     | Y     | Y   | N   | N   | N   |
| [Transactional `LOAD DATA`](/sql-statements/sql-statement-load-data.md)              | Y     | N   | N   | N   | N   |
| [Database migration toolkit (DM)](/migration-overview.md)                            | Y     | Y   | Y   | Y   | Y   |
| [TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md)                                  | Deprecated | Deprecated | Y | Y | Y |
| [Change data capture (CDC)](/ticdc/ticdc-overview.md)                                | Y     | Y   | N   | N   | N   |
| **Management, observability and tools**                                              | **Development** | **4.0** | **3.1** | **3.0** | **2.1** |
| [TiDB Dashboard](/dashboard/dashboard-intro.md)                                      | Y     | Y   | N   | N   | N   |
| [SQL diagnostics](/information-schema/information-schema-sql-diagnostics.md)         | Experimental | Experimental | N   | N   | N   |
| [Information schema](/information-schema/information-schema.md)                      | Y     | Y   | Y   | Y   | Y   |
| [Metrics schema](/metrics-schema.md)                                                 | Y     | Y   | N   | N   | N   |
| [Statements summary tables](/statement-summary-tables.md)                            | Y     | Y   | N   | N   | N   |
| [Slow query log](/identify-slow-queries.md)                                          | Y     | Y   | Y   | Y   | Y   |
| [TiUP deployment](/tiup/tiup-overview.md)                                            | Y     | Y   | N   | N   | N   |
| [Ansible deployment](/online-deployment-using-ansible.md)                            | Deprecated | Deprecated | Y   | Y   | Y   |
| [Kubernetes operator](https://docs.pingcap.com/tidb-in-kubernetes/)                  | Y     | Y   | Y   | Y   | Y   |
| [Built-in physical backup](/br/backup-and-restore-use-cases.md)                      | Y     | Y   | N   | N   | N   |
| Point in time recovery (PITR)                                                        | Planned | N | N   | N   | N   |

[^1]: TiDB incorrectly treats latin1 as a subset of utf8. See [TiDB #18955](https://github.com/pingcap/tidb/issues/18955) for more details.
[^2]: See [Statement Reference](/sql-statements/sql-statement-select.md) for a full list of SQL statements supported.
