---
title: FUSE_TIME_TRAVEL_SIZE
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.684"/>

Calculates the storage size of historical data (for Time Travel) for tables.

## Syntax

```sql
-- Calculate historical data size for all tables in all databases
SELECT ...
FROM fuse_time_travel_size();

-- Calculate historical data size for all tables in a specified database
SELECT ...
FROM fuse_time_travel_size('<database_name>');

-- Calculate historical data size for a specified table in a specified database
SELECT ...
FROM fuse_time_travel_size('<database_name>', '<table_name>');
```

## Output

The function returns a result set with the following columns:

| Column                           | Description                                                                                           |
|----------------------------------|-------------------------------------------------------------------------------------------------------|
| `database_name`                  | The name of the database where the table is located.                                                  |
| `table_name`                     | The name of the table.                                                                                |
| `is_dropped`                     | Indicates whether the table has been dropped (`true` for dropped tables, `false` otherwise).          |
| `time_travel_size`               | The total storage size of historical data (for Time Travel) for the table, in bytes.                  |
| `latest_snapshot_size`           | The storage size of the latest snapshot of the table, in bytes.                                       |
| `data_retention_period_in_hours` | The retention period for Time Travel data in hours (`NULL` means using the default retention policy). |
| `error`                          | Any error encountered while retrieving the storage size (`NULL` if no errors occurred).               |

## Examples

This example calculates the historical data for all tables in the `default` database:

```sql
SELECT * FROM fuse_time_travel_size('default')

┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ database_name │ table_name │ is_dropped │ time_travel_size │ latest_snapshot_size │ data_retention_period_in_hours │       error      │
├───────────────┼────────────┼────────────┼──────────────────┼──────────────────────┼────────────────────────────────┼──────────────────┤
│ default       │ books      │ true       │             2810 │                 1490 │                           NULL │ NULL             │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
