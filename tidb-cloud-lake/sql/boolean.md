---
title: Boolean
description: Basic logical data type.
sidebar_position: 1
---

## Overview

`BOOLEAN` (alias `BOOL`) represents `TRUE` or `FALSE` and always uses one byte of storage. Numeric and string inputs automatically coerce to boolean values when possible.

| Input Type | Converts to TRUE | Converts to FALSE | Notes |
|------------|-----------------|-------------------|-------|
| Numeric    | Any non-zero     | 0                 | Negative numbers convert to TRUE. |
| String     | `TRUE`           | `FALSE`           | Case-insensitive; other text fails to cast. |

## Examples

```sql
SELECT
  0::BOOLEAN            AS zero_is_false,
  42::BOOLEAN           AS nonzero_is_true,
  'True'::BOOLEAN       AS string_true,
  'false'::BOOLEAN      AS string_false;
```

Result:
```
┌───────────────┬──────────────────┬───────────────┬────────────────┐
│ zero_is_false │ nonzero_is_true  │ string_true   │ string_false   │
├───────────────┼──────────────────┼───────────────┼────────────────┤
│ false         │ true             │ true          │ false          │
└───────────────┴──────────────────┴───────────────┴────────────────┘
```

```sql
-- Casting unsupported text raises an error.
SELECT 'yes'::BOOLEAN;
```

Result:
```
ERROR 1105 (HY000): QueryFailed: [1006]cannot parse to type `BOOLEAN` while evaluating function `to_boolean('yes')` in expr `CAST('yes' AS Boolean)`
```
