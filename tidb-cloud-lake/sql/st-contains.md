---
title: ST_CONTAINS
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.564"/>

Returns TRUE if the second GEOMETRY object is completely inside the first GEOMETRY object.

## Syntax

```sql
ST_CONTAINS(<geometry1>, <geometry2>)
```

## Arguments

| Arguments     | Description                                                                                  |
|---------------|----------------------------------------------------------------------------------------------|
| `<geometry1>` | The argument must be an expression of type GEOMETRY object that is not a GeometryCollection. |
| `<geometry2>` | The argument must be an expression of type GEOMETRY object that is not a GeometryCollection. |

:::note
- The function reports an error if the two input GEOMETRY objects have different SRIDs.
:::

## Return Type

Boolean.

## Examples

```sql
SELECT ST_CONTAINS(TO_GEOMETRY('POLYGON((-2 0, 0 2, 2 0, -2 0))'), TO_GEOMETRY('POLYGON((-1 0, 0 1, 1 0, -1 0))')) AS contains

┌──────────┐
│ contains │
├──────────┤
│ true     │
└──────────┘

SELECT ST_CONTAINS(TO_GEOMETRY('POLYGON((-2 0, 0 2, 2 0, -2 0))'), TO_GEOMETRY('LINESTRING(-1 1, 0 2, 1 1)')) AS contains

┌──────────┐
│ contains │
├──────────┤
│ false    │
└──────────┘

SELECT ST_CONTAINS(TO_GEOMETRY('POLYGON((-2 0, 0 2, 2 0, -2 0))'), TO_GEOMETRY('LINESTRING(-2 0, 0 0, 0 1)')) AS contains

┌──────────┐
│ contains │
├──────────┤
│ true     │
└──────────┘

```
