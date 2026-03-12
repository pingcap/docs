---
title: Data Lifecycle in Databend
sidebar_label: Data Lifecycle
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

- [`CREATE DATABASE`](/sql/sql-commands/ddl/database/ddl-create-database): To create a new database.
- [`ALTER DATABASE`](/sql/sql-commands/ddl/database/ddl-alter-database): To modify an existing database.
- [`CREATE TABLE`](/sql/sql-commands/ddl/table/ddl-create-table): To create a new table.
- [`ALTER TABLE`](/sql/sql-commands/ddl/table/alter-table): To modify an existing table.

## Storing Data

Directly add data to your tables. Databend also allows importing data from external files into its tables.

Key Commands:

- [`INSERT`](/sql/sql-commands/dml/dml-insert): To add data to a table.
- [`COPY INTO <table>`](/sql/sql-commands/dml/dml-copy-into-table): To bring in data from an external file.

## Querying Data

After your data is in the tables, use `SELECT` to look at and analyze it.

Key Command:

- [`SELECT`](/sql/sql-commands/query-syntax/query-select): To get data from a table.

## Working with Data

Once your data is in Databend, you can update, replace, merge, or delete it as needed.

Key Commands:

- [`UPDATE`](/sql/sql-commands/dml/dml-update): To change data in a table.
- [`REPLACE`](/sql/sql-commands/dml/dml-replace): To replace existing data.
- [`MERGE`](/sql/sql-commands/dml/dml-merge): To seamlessly insert, update, and delete by comparing data between main and source tables or subqueries.
- [`DELETE`](/sql/sql-commands/dml/dml-delete-from): To remove data from a table.

## Removing Data

Databend allows you to delete specific data or entire tables and databases.

Key Commands:

- [`TRUNCATE TABLE`](/sql/sql-commands/ddl/table/ddl-truncate-table): To clear a table without deleting its structure.
- [`DROP TABLE`](/sql/sql-commands/ddl/table/ddl-drop-table): To remove a table.
- [`DROP DATABASE`](/sql/sql-commands/ddl/database/ddl-drop-database): To delete a database.
