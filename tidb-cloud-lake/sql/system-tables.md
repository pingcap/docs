---
title: System Tables
summary: Databend provides a set of system tables that contain metadata about your Databend deployment, databases, tables, queries, and system performance. These tables are read-only and are automatically updated by the system.
---

# System Tables

Databend provides a set of system tables that contain metadata about your Databend deployment, databases, tables, queries, and system performance. These tables are read-only and are automatically updated by the system.

System tables are organized in the `system` schema and can be queried using standard SQL. They provide valuable information for monitoring, troubleshooting, and understanding your Databend environment.

## Available System Tables

### Database & Table Metadata

| Table                                                             | Description                                                                                       |
|-------------------------------------------------------------------|---------------------------------------------------------------------------------------------------|
| [system.tables](/tidb-cloud-lake/sql/system-tables.md)                                 | Provides metadata information for all tables including properties, creation time, size, and more. |
| [system.tables_with_history](/tidb-cloud-lake/sql/system-tables-with-history.md)       | Provides historical metadata information for tables, including dropped tables.                    |
| [system.databases](/tidb-cloud-lake/sql/system-databases.md)                           | Contains information about all databases in the system.                                           |
| [system.views](/tidb-cloud-lake/sql/system-views.md)                                   | Contains information about all views in the system.                                               |
| [system.databases_with_history](/tidb-cloud-lake/sql/system-databases-with-history.md) | Contains historical information about databases, including dropped databases.                     |
| [system.columns](/tidb-cloud-lake/sql/system-columns.md)                               | Provides information about columns in all tables.                                                 |
| [system.indexes](/tidb-cloud-lake/sql/system-indexes.md)                               | Contains information about table indexes.                                                         |
| [system.virtual_columns](/tidb-cloud-lake/sql/system-virtual-columns.md)               | Lists virtual columns available in the system.                                                    |

### Query & Performance

| Table | Description |
|-------|-------------|
| [system.query_log](/tidb-cloud-lake/sql/system-query-log.md) | Contains information about executed queries, including performance metrics. |
| [system.metrics](/tidb-cloud-lake/sql/system-metrics.md) | Contains information about system metric events. |
| [system.query_cache](/tidb-cloud-lake/sql/system-query-cache.md) | Provides information about the query cache. |
| [system.locks](/tidb-cloud-lake/sql/system-locks.md) | Contains information about acquired locks in the system. |

### Functions & Settings

| Table | Description |
|-------|-------------|
| [system.functions](/tidb-cloud-lake/sql/system-functions.md) | Lists all available built-in functions. |
| [system.table_functions](/tidb-cloud-lake/sql/system-table-functions.md) | Lists all available table functions. |
| [system.user_functions](/tidb-cloud-lake/sql/system-user-functions.md) | Contains information about user-defined functions. |
| [system.settings](/tidb-cloud-lake/sql/system-settings.md) | Contains information about system settings. |
| [system.configs](/tidb-cloud-lake/sql/system-configs.md) | Contains configuration information for the Databend deployment. |

### System Information

| Table | Description |
|-------|-------------|
| [system.build_options](/tidb-cloud-lake/sql/system-build-options.md) | Contains information about build options used to compile Databend. |
| [system.clusters](/tidb-cloud-lake/sql/system-clusters.md) | Contains information about clusters in the system. |
| [system.contributors](/tidb-cloud-lake/sql/system-contributors.md) | Lists contributors to the Databend project. |
| [system.credits](/tidb-cloud-lake/sql/system-credits.md) | Contains information about third-party libraries used in Databend. |
| [system.caches](/tidb-cloud-lake/sql/system-caches.md) | Provides information about system caches. |

### Utility Tables

| Table | Description |
|-------|-------------|
| [system.numbers](/tidb-cloud-lake/sql/system-numbers.md) | A table containing a single column with integers starting from 0, useful for generating test data. |
| [system.streams](/tidb-cloud-lake/sql/system-streams.md) | Contains information about streams in the system. |
| [system.temp_tables](/tidb-cloud-lake/sql/system-temporary-tables.md) | Contains information about temporary tables. |
| [system.temp_files](/tidb-cloud-lake/sql/system-temp-files.md) | Contains information about temporary files. |
