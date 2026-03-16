---
title: QUERY_HISTORY
sidebar_position: 7
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.687"/>

Retrieves query execution logs for analysis and monitoring purposes.

## Syntax

```sql
QUERY_HISTORY
    [ BY WAREHOUSE <warehouse_name> ]
    [ FROM '<timestamp>' ]
    [ TO '<timestamp>' ]
    [ LIMIT <unsigned_integer> ]
```

| Parameter      | Description                                                                                                                              |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `BY WAREHOUSE` | Optional. Filters logs to a specific warehouse. Empty names raise an error.                                                              |
| `FROM`         | Optional. Start timestamp for the query range. Format: `YYYY-MM-DD HH:MM:SS` (UTC or explicit timezone). Defaults to 1 hour before `TO`. |
| `TO`           | Optional. End timestamp for the query range. Format: `YYYY-MM-DD HH:MM:SS` (UTC or explicit timezone). Defaults to current time.         |
| `LIMIT`        | Optional. Maximum number of records to return. Defaults to `10`. Must be a positive integer.                                             |

## Output Columns

The result includes columns such as:

| Column       | Description                           |
| ------------ | ------------------------------------- |
| `query_id`   | Unique identifier for the query       |
| `query_text` | The SQL statement executed            |
| `scan_bytes` | Amount of data scanned                |
| ...          | Additional query metrics and metadata |

## Examples

Get recent query history for a specific warehouse:

```sql
QUERY_HISTORY
    BY WAREHOUSE etl_wh
    FROM '2023-08-20 00:00:00'
    TO '2023-08-20 06:00:00'
    LIMIT 200;
```

Get the last 10 queries across all warehouses:

```sql
QUERY_HISTORY;
```

Get query history with a custom limit:

```sql
QUERY_HISTORY LIMIT 50;
```
