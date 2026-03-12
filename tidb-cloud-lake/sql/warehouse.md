---
title: Warehouse
sidebar_position: 0
---

Warehouse-related SQL commands for Databend Cloud.

## General Rules

- **Warehouse naming**: 3–63 characters, `A-Z`, `a-z`, `0-9`, and `-` only.
- **Strings and identifiers**: Bare identifiers may omit quotes when they contain no spaces; otherwise enclose with single quotes. Grammar allows keywords or numeric/boolean literals as names, but runtime validation still applies.
- **Numeric parameters**: `nullable_unsigned_number` / `nullable_signed_number` accept integers or `NULL`. Supplying `NULL` resets the value (for example, `AUTO_SUSPEND = NULL` equals `0`).
- **Time parameters**: `QUERY_HISTORY` uses `YYYY-MM-DD HH:MM:SS` (UTC or explicit timezone). Missing fractional seconds are interpreted as whole seconds.
- **Boolean parameters**: Only `TRUE`/`FALSE` are accepted.
- **`WITH` keyword**: May appear before the entire option list or ahead of each option. Options are whitespace-separated; commas are not part of the grammar.

## Warehouse Management

Tags are key-value pairs that help categorize and organize warehouses, similar to AWS resource tags. They are commonly used for:

- **Cost allocation**: Track warehouse costs by team, project, or cost center
- **Environment identification**: Mark warehouses as dev, staging, or production
- **Team ownership**: Identify which team owns or manages a warehouse
- **Custom metadata**: Add any arbitrary metadata for organizational purposes

Tag keys and values are arbitrary strings (enclosed in quotes if they contain spaces or special characters). Tags can be:

- Added at warehouse creation time using `WITH TAG (key = 'value', ...)`
- Updated or added later using `ALTER WAREHOUSE ... SET TAG key = 'value'`
- Removed using `ALTER WAREHOUSE ... UNSET TAG key`

Tags are returned in API responses and visible through `SHOW WAREHOUSES`.

**Tag Limits:**

- Maximum 10 tags per warehouse
- Tag name (key) maximum length: 128 characters
- Tag value maximum length: 256 characters

## Supported Statements

| Statement          | Purpose                      | Notes                                                      |
| ------------------ | ---------------------------- | ---------------------------------------------------------- |
| `CREATE WAREHOUSE` | Create a warehouse           | Supports `IF NOT EXISTS` and option list                   |
| `ALTER WAREHOUSE`  | Suspend/resume/mutate/rename | `SUSPEND`/`RESUME`, `SET <options>`, or `RENAME TO <name>` |
| `DROP WAREHOUSE`   | Delete a warehouse           | Optional `IF EXISTS`                                       |
| `USE WAREHOUSE`    | Bind the current session     | Validates existence only                                   |
| `SHOW WAREHOUSES`  | List warehouses              | Optional `LIKE` filter                                     |
| `QUERY_HISTORY`    | Inspect query logs           | Filter by warehouse, time range, limit                     |

## Warehouse Management

| Command                                 | Description                                       |
| --------------------------------------- | ------------------------------------------------- |
| [CREATE WAREHOUSE](create-warehouse.md) | Creates a new warehouse                           |
| [USE WAREHOUSE](use-warehouse.md)       | Sets the current warehouse for the session        |
| [SHOW WAREHOUSES](show-warehouses.md)   | Lists all warehouses with optional filtering      |
| [ALTER WAREHOUSE](alter-warehouse.md)   | Suspends, resumes, or modifies warehouse settings |
| [DROP WAREHOUSE](drop-warehouse.md)     | Removes a warehouse                               |
| [QUERY_HISTORY](query-history.md)       | Inspects query logs for a warehouse               |

:::note
A warehouse represents compute resources used to run queries in Databend Cloud.
:::
