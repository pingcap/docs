---
title: 数据类型
summary: "{{{ .lake }}} 将数据存储在强类型列中。本页概述支持的数据类型、自动/显式转换的工作方式，以及 NULL 或默认值的处理行为。"
---

# 数据类型

{{{ .lake }}} 将数据存储在强类型列中。本页概述支持的数据类型、自动/显式转换的工作方式，以及 NULL 或默认值的处理行为。

## 基础类型 {#foundational-types}

| 数据类型                                   | 别名      | 存储 / 精度                    | 最小值                   | 最大值                         |
|--------------------------------------------|------------|-----------------------------------|--------------------------|--------------------------------|
| [BOOLEAN](/tidb-cloud-lake/sql/boolean.md)                      | BOOL       | 1 字节                            | –                        | –                              |
| [BINARY](/tidb-cloud-lake/sql/binary.md)                        | VARBINARY  | 可变                          | –                        | –                              |
| [VARCHAR](/tidb-cloud-lake/sql/string.md)                       | STRING     | 可变                          | –                        | –                              |
| [TINYINT](/tidb-cloud-lake/sql/numeric.md#integer-data-types)   | INT8       | 1 字节                            | -128                     | 127                            |
| [SMALLINT](/tidb-cloud-lake/sql/numeric.md#integer-data-types)  | INT16      | 2 字节                           | -32768                   | 32767                          |
| [INT](/tidb-cloud-lake/sql/numeric.md#integer-data-types)       | INT32      | 4 字节                           | -2147483648              | 2147483647                     |
| [BIGINT](/tidb-cloud-lake/sql/numeric.md#integer-data-types)    | INT64      | 8 字节                           | -9223372036854775808     | 9223372036854775807            |
| [FLOAT](/tidb-cloud-lake/sql/numeric.md#floating-point-data-types) | –        | 4 字节 (Float32)                | -3.40e38                 | 3.40e38                        |
| [DOUBLE](/tidb-cloud-lake/sql/numeric.md#floating-point-data-types) | –       | 8 字节 (Float64)                | -1.79e308                | 1.79e308                       |
| [DECIMAL](/tidb-cloud-lake/sql/decimal.md)                      | –          | 16/32 字节 (精度 ≤38/76)    | `-(10^P-1)/10^S`         | `(10^P-1)/10^S`                |

## 日期和时间类型 {#date-time-types}

| 数据类型                 | 别名     | 精度 / 说明                           |
|---------------------------|-----------|--------------------------------------|
| [DATE](/tidb-cloud-lake/sql/datetime.md)       | –         | 天级精度                        |
| [TIMESTAMP](/tidb-cloud-lake/sql/datetime.md)  | DATETIME  | 微秒，按会话时区输出 |
| [TIMESTAMP_TZ](/tidb-cloud-lake/sql/datetime.md) | –       | 微秒 + 存储偏移          |
| [INTERVAL](/tidb-cloud-lake/sql/interval.md)   | –         | 微秒，支持负时间跨度 |

## 结构化与半结构化类型 {#structured-semi-structured-types}

| 数据类型             | 示例                                | 说明 |
|-----------------------|----------------------------------------|-------------|
| [ARRAY](/tidb-cloud-lake/sql/array.md)     | `[1, 2, 3]`                            | 具有相同内部类型的有序值列表。 |
| [TUPLE](/tidb-cloud-lake/sql/tuple.md)     | `('2023-02-14','Valentine's Day')`     | 具有已声明元素类型的定长有序列表。 |
| [MAP](/tidb-cloud-lake/sql/map.md)         | `{'a': 1, 'b': 2}`                     | 键值集合（内部表示为键类型和值类型的元组）。 |
| [VARIANT](/tidb-cloud-lake/sql/variant.md) | `[1, {"name":"datalake"}]`             | 类似 JSON 的容器，可混合原语、数组和对象。 |
| [BITMAP](/tidb-cloud-lake/sql/bitmap.md)   | `<bitmap binary>`                      | 针对成员关系和集合运算优化的压缩位图。 |

## 领域特定类型 {#domain-specific-types}

| 数据类型                           | 说明 |
|------------------------------------|-------------|
| [VECTOR](/tidb-cloud-lake/sql/vector.md)                | 用于相似度搜索 / ML 工作负载的 Float32 向量嵌入。 |
| [GEOMETRY](/tidb-cloud-lake/sql/geospatial.md) / GEOGRAPHY | 以 WKB/EWKB 格式存储的空间对象。 |

## 类型转换与转换规则 {#casting-and-conversion}

### 显式类型转换 {#explicit-casting}

- `CAST(expr AS TYPE)` 使用 ANSI 语法，在转换无效时会失败。
- `expr::TYPE` 是 PostgreSQL 风格的简写。
- `TRY_CAST(expr AS TYPE)` 在转换失败时返回 NULL，而不是抛出错误。

### 隐式类型转换（Coercion） {#implicit-casting-coercion}

{{{ .lake }}} 会在定义明确的场景下执行自动转换：

1. 整数型会向上提升为 `INT64`。例如：`UInt8 -> INT64`。
2. 数值类型在必要时会向上提升为 `FLOAT64`。
3. 如果表达式中出现 NULL，任意类型 `T` 都可以变为 `Nullable(T)`。
4. 所有类型都可以向上提升为 `VARIANT`。
5. 复杂类型按元素进行强制转换（当 `T -> U` 时，`Array<T> -> Array<U>`；元组和映射同理）。

当目标列为 `NOT NULL` 时，如果数据中可能包含 NULL，请显式转换为 `Nullable<T>` 或使用 `TRY_CAST`。

```sql
SELECT CONCAT('1', col);      -- safe (strings)
SELECT CONCAT(1, col);        -- may fail if `col` can't coerce to number
```

## NULL 处理与默认值 {#null-handling-and-defaults}

除非声明为 `NOT NULL`，否则列允许 NULL 值。当在 INSERT 时省略 `NOT NULL` 列，{{{ .lake }}} 会写入该类型对应的默认值：

| 类型类别            | 默认值 |
|--------------------------|---------|
| 整数型                  | `0`     |
| 浮点型           | `0.0`   |
| 字符串 / 二进制          | 空字符串 / 空二进制 |
| 日期                     | `1970-01-01` |
| 时间戳                | `1970-01-01 00:00:00` |
| 布尔型                  | `FALSE` |

示例：

```sql
CREATE TABLE test (
    id   INT64,
    name STRING NOT NULL,
    age  INT32
);

INSERT INTO test (id, name, age) VALUES (2, 'Alice', NULL);  -- allowed
INSERT INTO test (id, name) VALUES (1, 'John');              -- age becomes NULL
INSERT INTO test (id, age) VALUES (3, 45);                   -- name uses default ''
```

你可以随时使用 `DESC test` 或 `SHOW CREATE TABLE test` 查看列的默认值和可空性。