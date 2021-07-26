---
title: Data Types
summary: Learn about the data types supported in TiDB.
aliases: ['/docs/dev/data-type-overview/','/docs/dev/reference/sql/data-types/overview/']
---

# Data Types

TiDB supports all the data types in MySQL except the `SPATIAL` type.  This includes all the [numeric types](/data-type-numeric.md), [string types](/data-type-string.md), [date & time types](/data-type-date-and-time.md), and [the JSON type](/data-type-json.md).

The definitions used for datatypes are specified as `T(M[, D])`. Where by:

- `T` indicates the specific data type.
- `M` indicates the maximum display width for integer types. For floating-point and fixed-point types, `M` is the total number of digits that can be stored (the precision). For string types, `M` is the maximum length. The maximum permissible value of M depends on the data type.
- `D` applies to floating-point and fixed-point types and indicates the number of digits following the decimal point (the scale).
- `fsp` applies to the `TIME`, `DATETIME`, and `TIMESTAMP` types and represents the fractional seconds precision. The `fsp` value, if given, must be in the range 0 to 6. A value of 0 signifies that there is no fractional part. If omitted, the default precision is 0.
