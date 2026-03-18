---
title: Table
---

This page provides a comprehensive overview of table operations in Databend, organized by functionality for easy reference.

## Table Creation

| Command | Description |
|---------|-------------|
| [CREATE TABLE](/tidb-cloud-lake/sql/create-table.md) | Creates a new table with specified columns and options |
| [CREATE TABLE ... LIKE](/tidb-cloud-lake/sql/create-table.md#create-table--like) | Creates a table with the same column definitions as an existing one |
| [CREATE TABLE ... AS](/tidb-cloud-lake/sql/create-table.md#create-table--as) | Creates a table and inserts data based on the results of a SELECT query |
| [CREATE TRANSIENT TABLE](/tidb-cloud-lake/sql/create-transient-table.md) | Creates a table without Time Travel support |
| [CREATE EXTERNAL TABLE](/tidb-cloud-lake/sql/create-external-table.md) | Creates a table with data stored in a specified external location |
| [ATTACH TABLE](/tidb-cloud-lake/sql/attach-table.md) | Creates a table by associating it with an existing table |

## Table Modification

| Command | Description |
|---------|-------------|
| [ALTER TABLE](/tidb-cloud-lake/sql/alter-table.md) | Modifies table columns, comments, Fuse options, external connections, or swaps metadata with another table |
| [RENAME TABLE](/tidb-cloud-lake/sql/rename-table.md) | Changes the name of a table |

## Table Information

| Command | Description |
|---------|-------------|
| [DESCRIBE TABLE](/tidb-cloud-lake/sql/describe-table.md) / [SHOW FIELDS](/tidb-cloud-lake/sql/show-fields.md) | Shows information about the columns in a given table |
| [SHOW FULL COLUMNS](/tidb-cloud-lake/sql/show-columns.md) | Retrieves comprehensive details about the columns in a given table |
| [SHOW CREATE TABLE](/tidb-cloud-lake/sql/show-create-table.md) | Shows the CREATE TABLE statement that creates the named table |
| [SHOW TABLES](/tidb-cloud-lake/sql/show-tables.md) | Lists the tables in the current or a specified database |
| [SHOW TABLE STATUS](/tidb-cloud-lake/sql/show-table-status.md) | Shows the status of the tables in a database |
| [SHOW DROP TABLES](/tidb-cloud-lake/sql/show-drop-tables.md) | Lists the dropped tables in the current or a specified database |

## Table Deletion & Recovery

| Command | Description | Recovery Option |
|---------|-------------|----------------|
| [TRUNCATE TABLE](/tidb-cloud-lake/sql/truncate-table.md) | Removes all data from a table while preserving the table's schema | [FLASHBACK TABLE](/tidb-cloud-lake/sql/flashback-table.md) |
| [DROP TABLE](/tidb-cloud-lake/sql/drop-table.md) | Deletes a table | [UNDROP TABLE](/tidb-cloud-lake/sql/undrop-table.md) |
| [VACUUM TABLE](/tidb-cloud-lake/sql/vacuum-table.md) | Permanently removes historical data files of a table (Enterprise Edition) | Not recoverable |
| [VACUUM DROP TABLE](/tidb-cloud-lake/sql/vacuum-drop-table.md) | Permanently removes data files of dropped tables (Enterprise Edition) | Not recoverable |

## Table Optimization

| Command | Description |
|---------|-------------|
| [OPTIMIZE TABLE](/tidb-cloud-lake/sql/optimize-table.md) | Compacts or purges historical data to save storage space and enhance query performance |
| [SET CLUSTER KEY](/tidb-cloud-lake/sql/set-cluster-key.md) | Configures a cluster key to enhance query performance for large tables |

> **Note:**
>
> Table optimization is an advanced operation. Please carefully read the documentation before proceeding to avoid potential data loss.
