---
title: Array
description: Array of defined data type.
sidebar_position: 8
---

## Overview

`ARRAY(T)` stores variable-length collections whose elements all share the type `T`. Define the element type when creating a table and use array functions to read or transform the values.

:::note
Databend arrays are 1-based. `arr[1]` returns the first element and `arr[n]` the last.
:::

## Examples

```sql
CREATE TABLE array_samples (arr ARRAY(INT64));

INSERT INTO array_samples VALUES ([1, 2, 3]), ([10, 20]);

SELECT
  arr,
  arr[1]   AS first_elem,
  arr[2]   AS second_elem
FROM array_samples;
```

Result:
```
┌────────────┬────────────┬──────────────┐
│ arr        │ first_elem │ second_elem │
├────────────┼────────────┼──────────────┤
│ [1,2,3]    │          1 │            2 │
│ [10,20]    │         10 │           20 │
└────────────┴────────────┴──────────────┘
```

```sql
-- Index 0 always returns NULL because arrays are 1-based.
SELECT arr[0] AS zeroth_elem FROM array_samples;
```

Result:
```
┌─────────────┐
│ zeroth_elem │
├─────────────┤
│ NULL        │
│ NULL        │
└─────────────┘
```
