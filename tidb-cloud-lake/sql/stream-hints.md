---
title: WITH Stream Hints
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.670"/>

Specifies various stream configuration options using hints to control how the stream is processed.

See also: [WITH CONSUME](with-consume.md)

## Syntax

```sql
SELECT ...
FROM <stream_name> WITH (<hint1> = <value1>[, <hint2> = <value2>, ...])
```

The following lists the available hints, including their descriptions and recommended usage for optimizing stream processing:

| Hint             | Description                                                                                                                                                                               |
|------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `CONSUME`        | Specifies whether this query will consume the stream. Defaults to `False`.                                                                                                                |
| `MAX_BATCH_SIZE` | Defines the maximum number of rows per batch processed from the stream.<br/>- If not specified, all rows from the stream are processed.<br/>- Changing `MAX_BATCH_SIZE` for the same stream within a transaction is not allowed and will result in an error.<br/>- For streams with a large backlog of changes, such as when a stream hasn’t been consumed for a long time, setting `MAX_BATCH_SIZE` or using a smaller value is *not* recommended, as it may reduce capture efficiency. |

## Examples

Before the demonstration, let's create a table, define a stream on it, and insert two rows of data.

```sql
CREATE TABLE t1(a int);
CREATE STREAM s ON TABLE t1;
INSERT INTO t1 values(1);
INSERT INTO t1 values(2);
```

The following demonstrates how the `MAX_BATCH_SIZE` hint affects the number of rows processed per batch when querying a stream. With `MAX_BATCH_SIZE` set to 1, each batch contains a single row, while setting it to 2 processes both rows in a single batch.

```sql
SELECT * FROM s WITH (CONSUME = FALSE, MAX_BATCH_SIZE = 1);

-[ RECORD 1 ]-----------------------------------
               a: 1
   change$action: INSERT
change$is_update: false
   change$row_id: de75bebeeb6b4a54bfe05d4d14c83757000000

SELECT * FROM s WITH (CONSUME = FALSE, MAX_BATCH_SIZE = 2);

┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│        a        │ change$action │ change$is_update │              change$row_id             │
├─────────────────┼───────────────┼──────────────────┼────────────────────────────────────────┤
│               2 │ INSERT        │ false            │ d2c02e411db84d269dc9f6e32d8444bc000000 │
│               1 │ INSERT        │ false            │ de75bebeeb6b4a54bfe05d4d14c83757000000 │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
```

The following shows how the `CONSUME` hint operates when querying a stream. With `CONSUME = TRUE` and ` MAX_BATCH_SIZE = 1`, each query consumes one row from the stream.

```sql
SELECT * FROM s WITH (CONSUME = TRUE, MAX_BATCH_SIZE = 1);

-[ RECORD 1 ]-----------------------------------
               a: 1
   change$action: INSERT
change$is_update: false
   change$row_id: de75bebeeb6b4a54bfe05d4d14c83757000000

SELECT * FROM s WITH (CONSUME = TRUE, MAX_BATCH_SIZE = 1);

-[ RECORD 1 ]-----------------------------------
               a: 2
   change$action: INSERT
change$is_update: false
   change$row_id: d2c02e411db84d269dc9f6e32d8444bc000000
```