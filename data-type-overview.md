---
title: Data Types
summary: 了解 TiDB 支持的数据类型。
---

# Data Types

TiDB 支持所有 MySQL 中的数据类型，除了 `SPATIAL` 类型。这包括所有的 [numeric types](/data-type-numeric.md)、[string types](/data-type-string.md)、[date & time types](/data-type-date-and-time.md) 和 [the JSON type](/data-type-json.md)。

数据类型的定义格式为 `T(M[, D])`，其中：

- `T` 表示具体的数据类型。
- `M` 表示整数类型的最大显示宽度。对于浮点型和定点型，`M` 表示可存储的总位数（精度）。对于字符串类型，`M` 表示最大长度。M 的最大允许值取决于数据类型。

<CustomContent platform="tidb">

> **Warning:**
>
> 从 v8.5.0 版本开始，整数显示宽度已被弃用（[`deprecate-integer-display-length`](/tidb-configuration-file.md#deprecate-integer-display-length) 默认为 `true`）。不建议为整数类型指定显示宽度。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **Warning:**
>
> 从 v8.5.0 版本开始，整数显示宽度已被弃用。不建议为整数类型指定显示宽度。

</CustomContent>

- `D` 适用于浮点型和定点型，表示小数点后面的位数（即小数位数）。
- `fsp` 适用于 `TIME`、`DATETIME` 和 `TIMESTAMP` 类型，表示小数秒的精度。如果给定，`fsp` 的值必须在 0 到 6 之间。值为 0 表示没有小数部分。如果省略，默认精度为 0。