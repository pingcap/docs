---
title: View
---

This page provides a comprehensive overview of view operations in Databend, organized by functionality for easy reference.

## View Management

| Command | Description |
|---------|-------------|
| [CREATE VIEW](ddl-create-view.md) | Creates a new view based on a query |
| [ALTER VIEW](ddl-alter-view.md) | Modifies an existing view |
| [DROP VIEW](ddl-drop-view.md) | Removes a view |

## View Information

| Command | Description |
|---------|-------------|
| [DESC VIEW](desc-view.md) | Shows detailed information about a view |
| [SHOW VIEWS](show-views.md) | Lists all views in the current or specified database |

:::note
Views in Databend are named queries stored in the database that can be referenced like tables. They provide a way to simplify complex queries and control access to underlying data.
:::