---
title: CREATE TRANSIENT TABLE
summary: Creates a table without storing its historical data for Time Travel.
---

# CREATE TRANSIENT TABLE

Creates a table without storing its historical data for Time Travel.

Transient tables are used to hold transitory data that does not require a data protection or recovery mechanism. Dataebend does not hold historical data for a transient table so you will not be able to query from a previous version of the transient table with the Time Travel feature, for example, the [AT](/tidb-cloud-lake/sql/at.md) clause in the SELECT statement will not work for transient tables. Please note that you can still [drop](/tidb-cloud-lake/sql/drop-table.md) and [undrop](/tidb-cloud-lake/sql/undrop-table.md) a transient table.

> **Note:**
>
> Concurrent modifications (including write operations) on transient tables may cause data corruption, making the data unreadable. This defect is being addressed. Until fixed, please avoid concurrent modifications on transient tables.

## Syntax

```sql
CREATE [ OR REPLACE ] TRANSIENT TABLE
       [ IF NOT EXISTS ]
       [ <database_name>. ]<table_name>
       ...
```

The omitted parts follow the syntax of [CREATE TABLE](/tidb-cloud-lake/sql/create-table.md).

## Examples

This examples creates a transient table named `visits`:

```sql
CREATE TRANSIENT TABLE visits (
  visitor_id BIGINT
);
```
