---
title: Database
---

This page provides a comprehensive overview of database operations in Databend, organized by functionality for easy reference.

## Database Creation & Management

| Command | Description |
|---------|-------------|
| [CREATE DATABASE](ddl-create-database.md) | Creates a new database |
| [ALTER DATABASE](ddl-alter-database.md) | Modifies a database |
| [DROP DATABASE](ddl-drop-database.md) | Removes a database |
| [USE DATABASE](ddl-use-database.md) | Sets the current working database |
| [UNDROP DATABASE](undrop-database.md) | Recovers a dropped database |

## Database Information

| Command | Description |
|---------|-------------|
| [SHOW DATABASES](show-databases.md) | Lists all databases |
| [SHOW CREATE DATABASE](show-create-database.md) | Shows the CREATE DATABASE statement for a database |
| [SHOW DROP DATABASES](show-drop-databases.md) | Lists dropped databases that can be recovered |

:::note
Database operations are foundational for organizing your data in Databend. Make sure you have appropriate privileges before executing these commands.
:::