---
title: STREAM_STATUS
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.225"/>

Provides information about the status of a specified stream, yielding a single-column result (`has_data`) that can take on values of `true` or `false`: 

- `true`: Indicates that the stream **might contain** change data capture records.
- `false`: Indicates that the stream currently does not contain any change data capture records.

:::note
The presence of a `true` in the result (`has_data`) does **not** ensure the definite existence of change data capture records. Other operations, such as performing a table compact operation, could also lead to a `true` value even when there are no actual change data capture records.
:::

:::note
When using `STREAM_STATUS` in tasks, you must include the database name when referencing the stream (e.g., `STREAM_STATUS('mydb.stream_name')`).
:::

## Syntax

```sql
SELECT * FROM STREAM_STATUS('<database_name>.<stream_name>');
-- OR
SELECT * FROM STREAM_STATUS('<stream_name>');  -- Uses current database
```

## Examples

```sql
-- Create a table 't' with a column 'c'
CREATE TABLE t (c int);

-- Create a stream 's' on the table 't'
CREATE STREAM s ON TABLE t;

-- Check the initial status of the stream 's'
SELECT * FROM STREAM_STATUS('s');

-- The result should be 'false' indicating no change data capture records initially
┌──────────┐
│ has_data │
├──────────┤
│ false    │
└──────────┘

-- Insert a value into the table 't'
INSERT INTO t VALUES (1);

-- Check the updated status of the stream 's' after the insertion
SELECT * FROM STREAM_STATUS('s');

-- The result should now be 'true' indicating the presence of change data capture records
┌──────────┐
│ has_data │
├──────────┤
│ true     │
└──────────┘

-- Example with database name specified
SELECT * FROM STREAM_STATUS('mydb.s');
```
