---
title: Context Functions
---

This page provides reference information for the context-related functions in Databend. These functions return information about the current session, database, or system context.

## Session Information Functions

| Function | Description | Example |
|----------|-------------|--------|
| [CONNECTION_ID](connection-id.md) | Returns the connection ID for the current connection | `CONNECTION_ID()` → `42` |
| [CURRENT_USER](current-user.md) | Returns the user name and host for the current connection | `CURRENT_USER()` → `'root'@'%'` |
| [LAST_QUERY_ID](last-query-id.md) | Returns the query ID of the last executed query | `LAST_QUERY_ID()` → `'01890a5d-ac96-7cc6-8128-01d71ab8b93e'` |

## Database Context Functions

| Function | Description | Example |
|----------|-------------|--------|
| [CURRENT_CATALOG](current-catalog.md) | Returns the name of the current catalog | `CURRENT_CATALOG()` → `'default'` |
| [DATABASE](database.md) | Returns the name of the current database | `DATABASE()` → `'default'` |

## System Information Functions

| Function | Description | Example |
|----------|-------------|--------|
| [VERSION](version.md) | Returns the current version of Databend | `VERSION()` → `'DatabendQuery v1.2.252-nightly-193ed56304'` |
