---
title: The TiDB System Database
category: user guide
---

The TiDB System Database is similar to MySQL, which contains tables that store information required by the server as it runs.

### Grant System Tables

These system tables contain grant information about user accounts and the privileges held by them:

- `user`: user accounts, global privileges, and other non-privilege columns
- `db`: database-level privileges
- `tables_priv`: table-level privileges
- `columns_priv`: column-level privileges

### Server-Side Help System Tables

Currently, the `help_topic` is NULL.

### Statistics System Tables

- `stats_buckets`: the buckets of statistics information
- `stats_histograms`: the histograms of statistics information
- `stats_meta`: the meta information of tables, such as the total number of rows and modifications

### GC Worker System Tables

- `gc_delete_range`

### Miscellaneous System Tables

- `GLOBAL_VARIABLES`: global system variable tables
- `tidb`: to record the version information when TiDB executes `bootstrap`
