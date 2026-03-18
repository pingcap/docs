---
title: Data Lifecycle in TiDB Cloud Lake
summary: Databend supports familiar Data Definition Language (DDL) and Data Manipulation Language (DML) commands, making it easy for you to manage your database. Whether you're organizing, storing, querying, modifying, or deleting data, Databend follows the same industry standards you're accustomed to.
---
Databend supports familiar Data Definition Language (DDL) and Data Manipulation Language (DML) commands, making it easy for you to manage your database. Whether you're organizing, storing, querying, modifying, or deleting data, Databend follows the same industry standards you're accustomed to.

## Databend Objects

Databend supports the following objects to create and modify them:

- Database
- Table
- External Table
- Stream
- View
- Index
- Stage
- File Format
- Connection
- User Defined Function (UDF)
- External Function
- User
- Role
- Grants
- Warehouse
- Task

## Organizing Data

Arrange your data in databases and tables.

Key Commands:

- [`CREATE DATABASE`](/tidb-cloud-lake/sql/create-database.md): To create a new database.
- [`ALTER DATABASE`](/tidb-cloud-lake/sql/rename-database.md): To modify an existing database.
- [`CREATE TABLE`](/tidb-cloud-lake/sql/create-table.md): To create a new table.
- [`ALTER TABLE`](/tidb-cloud-lake/sql/alter-table.md): To modify an existing table.

## Storing Data

Directly add data to your tables. Databend also allows importing data from external files into its tables.

Key Commands:

- [`INSERT`](/tidb-cloud-lake/sql/insert.md): To add data to a table.
- [`COPY INTO <table>`](/tidb-cloud-lake/sql/copy-into-table.md): To bring in data from an external file.

## Querying Data

After your data is in the tables, use `SELECT` to look at and analyze it.

Key Command:

- [`SELECT`](/tidb-cloud-lake/sql/select.md): To get data from a table.

## Working with Data

Once your data is in Databend, you can update, replace, merge, or delete it as needed.

Key Commands:

- [`UPDATE`](/tidb-cloud-lake/sql/update.md): To change data in a table.
- [`REPLACE`](/tidb-cloud-lake/sql/replace.md): To replace existing data.
- [`MERGE`](/tidb-cloud-lake/sql/merge.md): To seamlessly insert, update, and delete by comparing data between main and source tables or subqueries.
- [`DELETE`](/tidb-cloud-lake/sql/delete.md): To remove data from a table.

## Removing Data

Databend allows you to delete specific data or entire tables and databases.

Key Commands:

- [`TRUNCATE TABLE`](/tidb-cloud-lake/sql/truncate-table.md): To clear a table without deleting its structure.
- [`DROP TABLE`](/tidb-cloud-lake/sql/drop-table.md): To remove a table.
- [`DROP DATABASE`](/tidb-cloud-lake/sql/drop-database.md): To delete a database.
