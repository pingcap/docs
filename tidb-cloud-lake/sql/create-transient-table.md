---
title: CREATE TRANSIENT TABLE
sidebar_position: 1
---

Creates a table without storing its historical data for Time Travel.

Transient tables are used to hold transitory data that does not require a data protection or recovery mechanism. Dataebend does not hold historical data for a transient table so you will not be able to query from a previous version of the transient table with the Time Travel feature, for example, the [AT](./../../20-query-syntax/03-query-at.md) clause in the SELECT statement will not work for transient tables. Please note that you can still [drop](./20-ddl-drop-table.md) and [undrop](./21-ddl-undrop-table.md) a transient table.

:::caution
Concurrent modifications (including write operations) on transient tables may cause data corruption, making the data unreadable. This defect is being addressed. Until fixed, please avoid concurrent modifications on transient tables.
:::

## Syntax

```sql
CREATE [ OR REPLACE ] TRANSIENT TABLE 
       [ IF NOT EXISTS ] 
       [ <database_name>. ]<table_name>
       ...
```

The omitted parts follow the syntax of [CREATE TABLE](10-ddl-create-table.md).

## Examples

This examples creates a transient table named `visits`:

```sql
CREATE TRANSIENT TABLE visits (
  visitor_id BIGINT
);
```