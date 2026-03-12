---
title: WITH CONSUME
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.469"/>

Consumes data from a stream within a SELECT query.

See also: [WITH Stream Hints](with-stream-hints.md)

## Syntax

```sql
SELECT ...
FROM <stream_name> WITH CONSUME [ AS <alias> ]
[ WHERE <conditions> ]
```

:::note
As long as the query executes successfully, the WITH CONSUME clause will consume all data captured by the stream, even if only a portion of it is queried using a WHERE condition.
:::

## Examples

Suppose we have a stream named 's' that has captured the following data:

```sql
SELECT * FROM s;

┌────────────────────────────────────────────────────────────────────────────────────────────────┐
│        a        │   change$action  │              change$row_id             │ change$is_update │
├─────────────────┼──────────────────┼────────────────────────────────────────┼──────────────────┤
│               3 │ INSERT           │ 4942372d864147e98188f3b486ec18d2000000 │ false            │
│               1 │ DELETE           │ 3df95ad8552e4967a704e1c7209d3dff000000 │ false            │
└────────────────────────────────────────────────────────────────────────────────────────────────┘
```

If we now query the stream using `WITH CONSUME`, we would get the following result:

```sql
SELECT
  a
FROM
  s WITH CONSUME AS ss
WHERE
  ss.change$action = 'INSERT';

┌─────────────────┐
│        a        │
├─────────────────┤
│               3 │
└─────────────────┘
```

The stream is now empty because the query above has consumed all of the data present in the stream. 

```sql
-- empty results
SELECT * FROM s;
```