---
title: SHOW STREAMS
sidebar_position: 2
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.460"/>

import EEFeature from '@site/src/components/EEFeature';

<EEFeature featureName='STREAM'/>

Lists the streams associated with a specific database.

## Syntax

```sql
SHOW [ FULL ] STREAMS 
     [ { FROM | IN } <database_name> ]  
     [ LIKE '<pattern>' | WHERE <expr> ]
```

| Parameter | Description                                                                                  |
|-----------|----------------------------------------------------------------------------------------------|
| FULL      | Lists the results with additional information. See [Examples](#examples) for more details.   |
| FROM / IN | Specifies a database. If omitted, the command returns the results from the current database. |
| LIKE      | Filters the stream names using case-sensitive pattern matching with the `%` wildcard.        |
| WHERE     | Filters the stream names using an expression in the WHERE clause.                            |

## Examples

This example shows streams belonging to the current database:

```sql
SHOW STREAMS;

┌──────────────────────────────────────────────────────────┐
│ Streams_in_default │        table_on       │     mode    │
├────────────────────┼───────────────────────┼─────────────┤
│ order_changes      │ default.orders        │ append_only │
│ s_append_only      │ default.t_append_only │ append_only │
│ s_standard         │ default.t_standard    │ standard    │
└──────────────────────────────────────────────────────────┘
```

This example shows detailed information about streams in the current database:

```sql
SHOW FULL STREAMS;

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│         created_on         │      name     │ database │ catalog │        table_on       │       owner      │ comment │     mode    │ invalid_reason │
├────────────────────────────┼───────────────┼──────────┼─────────┼───────────────────────┼──────────────────┼─────────┼─────────────┼────────────────┤
│ 2024-05-12 14:28:33.886271 │ order_changes │ default  │ default │ default.orders        │ NULL             │         │ append_only │                │
│ 2024-05-12 14:35:05.992050 │ s_append_only │ default  │ default │ default.t_append_only │ NULL             │         │ append_only │                │
│ 2024-05-12 14:35:05.981121 │ s_standard    │ default  │ default │ default.t_standard    │ NULL             │         │ standard    │                │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```