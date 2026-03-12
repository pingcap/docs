---
title: SHOW VIRTUAL COLUMNS
sidebar_position: 4
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.832"/>

import EEFeature from '@site/src/components/EEFeature';

<EEFeature featureName='VIRTUAL COLUMN'/>

Shows the created virtual columns in the system. Equivalent to `SELECT * FROM system.virtual_columns`.

Virtual columns are enabled by default starting from v1.2.832.

See also: [system.virtual_columns](../../../00-sql-reference/31-system-tables/system-virtual-columns.md)

## Preferred Syntax

Use the command in its simplest, most useful form to inspect a specific table or list all virtual columns:

```sql
SHOW VIRTUAL COLUMNS [WHERE table = '<table_name>' AND database = '<database_name>']
```

## Example

```sql
CREATE TABLE test(id int, val variant);

INSERT INTO
  test
VALUES
  (
    1,
    '{"id":1,"name":"databend"}'
  ),
  (
    2,
    '{"id":2,"name":"databricks"}'
  );

SHOW VIRTUAL COLUMNS WHERE table = 'test' AND database = 'default';
╭───────────────────────────────────────────────────────────────────────────────────────────────────╮
│ database │  table │ source_column │ virtual_column_id │ virtual_column_name │ virtual_column_type │
│  String  │ String │     String    │       UInt32      │        String       │        String       │
├──────────┼────────┼───────────────┼───────────────────┼─────────────────────┼─────────────────────┤
│ default  │ test   │ val           │        3000000000 │ ['id']              │ UInt64              │
│ default  │ test   │ val           │        3000000001 │ ['name']            │ String              │
╰───────────────────────────────────────────────────────────────────────────────────────────────────╯
```
