---
title: TO_GEOGRAPHY
title_includes: TRY_TO_GEOGRAPHY
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.431"/>

Parses an input and returns a value of type GEOGRAPHY.

`TRY_TO_GEOGRAPHY` returns a NULL value if an error occurs during parsing.

## Syntax

```sql
TO_GEOGRAPHY(<string>)
TO_GEOGRAPHY(<binary>)
TO_GEOGRAPHY(<variant>)
TRY_TO_GEOGRAPHY(<string>)
TRY_TO_GEOGRAPHY(<binary>)
TRY_TO_GEOGRAPHY(<variant>)
```

## Arguments

| Arguments   | Description                                                             |
|-------------|-------------------------------------------------------------------------|
| `<string>`  | The argument must be a string expression in WKT or EWKT format.         |
| `<binary>`  | The argument must be a binary expression in WKB or EWKB format.         |
| `<variant>` | The argument must be a JSON OBJECT in GeoJSON format.                   |

:::note
Only SRID 4326 is supported for GEOGRAPHY inputs.
:::

## Return Type

Geography.

## Examples

```sql
SELECT
  ST_ASWKT(
    TO_GEOGRAPHY(
      'POINT(1 2)'
    )
  ) AS pipeline_geography;

┌────────────────────┐
│ pipeline_geography │
├────────────────────┤
│ POINT(1 2)         │
└────────────────────┘

SELECT
  ST_ASWKT(
    TO_GEOGRAPHY(
      FROM_HEX('0101000000000000000000F03F0000000000000040')
    )
  ) AS pipeline_geography;

┌────────────────────┐
│ pipeline_geography │
├────────────────────┤
│ POINT(1 2)         │
└────────────────────┘

SELECT
  ST_ASWKT(
    TO_GEOGRAPHY(
      PARSE_JSON('{"type":"Point","coordinates":[1,2]}')
    )
  ) AS pipeline_geography;

┌────────────────────┐
│ pipeline_geography │
├────────────────────┤
│ POINT(1 2)         │
└────────────────────┘
```
