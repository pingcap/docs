---
title: REFRESH VIRTUAL COLUMN
sidebar_position: 3
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.832"/>

import EEFeature from '@site/src/components/EEFeature';

<EEFeature featureName='VIRTUAL COLUMN'/>

The `REFRESH VIRTUAL COLUMN` command in Databend is used to explicitly trigger the creation of virtual columns for existing tables. While Databend automatically manages virtual columns for new data, there are specific scenarios where manual refreshing is necessary to take full advantage of this feature.

Virtual columns are enabled by default starting from v1.2.832.

## When to Use `REFRESH VIRTUAL COLUMN`

- **Existing Tables Before Feature Enablement:** If you have tables containing `VARIANT` data that were created *before* the virtual column feature was enabled (or before upgrading to a version with automatic virtual column creation), you need to refresh the virtual columns to enable query acceleration. Databend will not automatically create virtual columns for data that already exists in these tables.

## Syntax

```sql
REFRESH VIRTUAL COLUMN FOR <table>
```

## Examples

This example refreshes virtual columns for a table named 'test':

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

REFRESH VIRTUAL COLUMN FOR test;

SHOW VIRTUAL COLUMNS WHERE table = 'test' AND database = 'default';
╭───────────────────────────────────────────────────────────────────────────────────────────────────╮
│ database │  table │ source_column │ virtual_column_id │ virtual_column_name │ virtual_column_type │
│  String  │ String │     String    │       UInt32      │        String       │        String       │
├──────────┼────────┼───────────────┼───────────────────┼─────────────────────┼─────────────────────┤
│ default  │ test   │ val           │        3000000000 │ ['id']              │ UInt64              │
│ default  │ test   │ val           │        3000000001 │ ['name']            │ String              │
╰───────────────────────────────────────────────────────────────────────────────────────────────────╯
```
