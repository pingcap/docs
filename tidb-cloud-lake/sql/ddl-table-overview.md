---
title: Table
---

This page provides a comprehensive overview of table operations in Databend, organized by functionality for easy reference.

## Table Creation

| Command | Description |
|---------|-------------|
| [CREATE TABLE](10-ddl-create-table.md) | Creates a new table with specified columns and options |
| [CREATE TABLE ... LIKE](10-ddl-create-table.md#create-table--like) | Creates a table with the same column definitions as an existing one |
| [CREATE TABLE ... AS](10-ddl-create-table.md#create-table--as) | Creates a table and inserts data based on the results of a SELECT query |
| [CREATE TRANSIENT TABLE](10-ddl-create-transient-table.md) | Creates a table without Time Travel support |
| [CREATE EXTERNAL TABLE](10-ddl-create-table-external-location.md) | Creates a table with data stored in a specified external location |
| [ATTACH TABLE](92-attach-table.md) | Creates a table by associating it with an existing table |

## Table Modification

| Command | Description |
|---------|-------------|
| [ALTER TABLE](90-alter-table.md) | Modifies table columns, comments, Fuse options, external connections, or swaps metadata with another table |
| [RENAME TABLE](30-ddl-rename-table.md) | Changes the name of a table |

## Table Information

| Command | Description |
|---------|-------------|
| [DESCRIBE TABLE](50-describe-table.md) / [SHOW FIELDS](show-fields.md) | Shows information about the columns in a given table |
| [SHOW FULL COLUMNS](show-full-columns.md) | Retrieves comprehensive details about the columns in a given table |
| [SHOW CREATE TABLE](show-create-table.md) | Shows the CREATE TABLE statement that creates the named table |
| [SHOW TABLES](show-tables.md) | Lists the tables in the current or a specified database |
| [SHOW TABLE STATUS](show-table-status.md) | Shows the status of the tables in a database |
| [SHOW DROP TABLES](show-drop-tables.md) | Lists the dropped tables in the current or a specified database |

## Table Deletion & Recovery

| Command | Description | Recovery Option |
|---------|-------------|----------------|
| [TRUNCATE TABLE](40-ddl-truncate-table.md) | Removes all data from a table while preserving the table's schema | [FLASHBACK TABLE](70-flashback-table.md) |
| [DROP TABLE](20-ddl-drop-table.md) | Deletes a table | [UNDROP TABLE](21-ddl-undrop-table.md) |
| [VACUUM TABLE](91-vacuum-table.md) | Permanently removes historical data files of a table (Enterprise Edition) | Not recoverable |
| [VACUUM DROP TABLE](91-vacuum-drop-table.md) | Permanently removes data files of dropped tables (Enterprise Edition) | Not recoverable |

## Table Optimization

| Command | Description |
|---------|-------------|
| [OPTIMIZE TABLE](60-optimize-table.md) | Compacts or purges historical data to save storage space and enhance query performance |
| [SET CLUSTER KEY](../06-clusterkey/dml-set-cluster-key.md) | Configures a cluster key to enhance query performance for large tables |

:::note
Table optimization is an advanced operation. Please carefully read the documentation before proceeding to avoid potential data loss.
:::
