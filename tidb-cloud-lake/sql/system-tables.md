---
title: System Tables
---

# System Tables

Databend provides a set of system tables that contain metadata about your Databend deployment, databases, tables, queries, and system performance. These tables are read-only and are automatically updated by the system.

System tables are organized in the `system` schema and can be queried using standard SQL. They provide valuable information for monitoring, troubleshooting, and understanding your Databend environment.

## Available System Tables

### Database & Table Metadata

| Table                                                             | Description                                                                                       |
|-------------------------------------------------------------------|---------------------------------------------------------------------------------------------------|
| [system.tables](system-tables.md)                                 | Provides metadata information for all tables including properties, creation time, size, and more. |
| [system.tables_with_history](system-tables-with-history.md)       | Provides historical metadata information for tables, including dropped tables.                    |
| [system.databases](system-databases.md)                           | Contains information about all databases in the system.                                           |
| [system.views](system-views.md)                                   | Contains information about all views in the system.                                               |
| [system.databases_with_history](system-databases-with-history.md) | Contains historical information about databases, including dropped databases.                     |
| [system.columns](system-columns.md)                               | Provides information about columns in all tables.                                                 |
| [system.indexes](system-indexes.md)                               | Contains information about table indexes.                                                         |
| [system.virtual_columns](system-virtual-columns.md)               | Lists virtual columns available in the system.                                                    |

### Query & Performance

| Table | Description |
|-------|-------------|
| [system.query_log](system-query-log.md) | Contains information about executed queries, including performance metrics. |
| [system.metrics](system-metrics.md) | Contains information about system metric events. |
| [system.query_cache](system-query-cache.md) | Provides information about the query cache. |
| [system.locks](system-locks.md) | Contains information about acquired locks in the system. |

### Functions & Settings

| Table | Description |
|-------|-------------|
| [system.functions](system-functions.md) | Lists all available built-in functions. |
| [system.table_functions](system-table-functions.md) | Lists all available table functions. |
| [system.user_functions](system-user-functions.md) | Contains information about user-defined functions. |
| [system.settings](system-settings.md) | Contains information about system settings. |
| [system.configs](system-configs.md) | Contains configuration information for the Databend deployment. |

### System Information

| Table | Description |
|-------|-------------|
| [system.build_options](system-build-options.md) | Contains information about build options used to compile Databend. |
| [system.clusters](system-clusters.md) | Contains information about clusters in the system. |
| [system.contributors](system-contributors.md) | Lists contributors to the Databend project. |
| [system.credits](system-credits.md) | Contains information about third-party libraries used in Databend. |
| [system.caches](system-caches.md) | Provides information about system caches. |

### Utility Tables

| Table | Description |
|-------|-------------|
| [system.numbers](system-numbers.md) | A table containing a single column with integers starting from 0, useful for generating test data. |
| [system.streams](system-streams.md) | Contains information about streams in the system. |
| [system.temp_tables](system-temp-tables.md) | Contains information about temporary tables. |
| [system.temp_files](system-temp-files.md) | Contains information about temporary files. |
