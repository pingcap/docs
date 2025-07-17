---
title: Cast Functions and Operators
summary: 了解转换函数和操作符。
---

# Cast Functions and Operators

Cast 函数和操作符可以实现值从一种数据类型到另一种数据类型的转换。 TiDB 支持所有在 MySQL 8.0 中可用的 [cast 函数和操作符](https://dev.mysql.com/doc/refman/8.0/en/cast-functions.html)。

| 名称                                     | 描述                      |
| ---------------------------------------- | -------------------------- |
| [`BINARY`](#binary) | 将字符串转换为二进制字符串 |
| [`CAST()`](#cast) | 将值转换为特定类型   |
| [`CONVERT()`](#convert) | 将值转换为特定类型   |

> **注意：**
>
> TiDB 和 MySQL 在执行 `SELECT CAST(MeN AS CHAR)`（或其等价形式 `SELECT CONVERT(MeM, CHAR)`）时显示的结果不一致，其中 `MeN` 表示以科学计数法表示的双精度浮点数。 MySQL 在 `-15 <= N <= 14` 时显示完整的数值，在 `N < -15` 或 `N > 14` 时显示科学计数法。而 TiDB 始终显示完整的数值。例如，MySQL 显示 `SELECT CAST(3.1415e15 AS CHAR)` 的结果为 `3.1415e15`，而 TiDB 显示的结果为 `3141500000000000`。

## BINARY

[`BINARY`](https://dev.mysql.com/doc/refman/8.0/en/cast-functions.html#operator_binary) 操作符自 MySQL 8.0.27 版本起已被弃用。建议在 TiDB 和 MySQL 中使用 `CAST(... AS BINARY)` 代替。

## CAST

[`CAST(<expression> AS <type> [ARRAY])`](https://dev.mysql.com/doc/refman/8.0/en/cast-functions.html#function_cast) 函数用于将表达式转换为特定类型。

该函数也用于创建 [多值索引](/sql-statements/sql-statement-create-index.md#multi-valued-indexes)。

支持的类型如下：

| 类型                 | 描述      | 是否可用于多值索引                      |
|----------------------|-----------|----------------------------------------|
| `BINARY(n)`          | 二进制字符串 | 否                                     |
| `CHAR(n)`            | 字符串     | 是，但仅在指定长度时有效               |
| `DATE`               | 日期       | 是                                     |
| `DATETIME(fsp)`      | 日期/时间，`fsp` 为可选 | 是                                |
| `DECIMAL(n, m)`      | 十进制数，`n` 和 `m` 为可选，默认为 `10` 和 `0` | 否   |
| `DOUBLE`             | 双精度浮点数 | 否                                    |
| `FLOAT(n)`           | 浮点数，`n` 为可选，范围在 `0` 到 `53` 之间 | 否 |
| `JSON`               | JSON       | 否                                     |
| `REAL`               | 浮点数     | 是                                    |
| `SIGNED [INTEGER]`   | 有符号整数 | 是                                    |
| `TIME(fsp)`          | 时间       | 是                                     |
| `UNSIGNED [INTEGER]` | 无符号整数 | 是                                    |
| `VECTOR`             | 向量       | 否                                     |
| `YEAR`               | 年份       | 否                                     |

示例：

以下语句将十六进制字面量的二进制字符串转换为 `CHAR`。

```sql
SELECT CAST(0x54694442 AS CHAR);
```

```sql
+--------------------------+
| CAST(0x54694442 AS CHAR) |
+--------------------------+
| TiDB                     |
+--------------------------+
1 行，耗时 0.0002 秒
```

以下语句将从 JSON 列中提取的 `a` 属性的值转换为无符号数组。注意，转换为数组仅作为多值索引定义的一部分被支持。

```sql
CREATE TABLE t (
    id INT PRIMARY KEY,
    j JSON,
    INDEX idx_a ((CAST(j->'$.a' AS UNSIGNED ARRAY)))
);
INSERT INTO t VALUES (1, JSON_OBJECT('a',JSON_ARRAY(1,2,3)));
INSERT INTO t VALUES (2, JSON_OBJECT('a',JSON_ARRAY(4,5,6)));
INSERT INTO t VALUES (3, JSON_OBJECT('a',JSON_ARRAY(7,8,9)));
ANALYZE TABLE t;
```

```sql
 EXPLAIN SELECT * FROM t WHERE 1 MEMBER OF(j->'$.a')\G
*************************** 1. 行 ***************************
           id: IndexMerge_10
      estRows: 2.00
         task: root
访问对象: 
操作符信息: type: union
*************************** 2. 行 ***************************
           id: ├─IndexRangeScan_8(Build)
      estRows: 2.00
         task: cop[tikv]
访问对象: table:t, index:idx_a(cast(json_extract(`j`, _utf8mb4'$.a') as unsigned array))
操作符信息: range:[1,1], keep order:false, stats:partial[j:unInitialized]
*************************** 3. 行 ***************************
           id: └─TableRowIDScan_9(Probe)
      estRows: 2.00
         task: cop[tikv]
访问对象: table:t
操作符信息: keep order:false, stats:partial[j:unInitialized]
3 行，耗时 0.00 秒
```

## CONVERT

[`CONVERT()`](https://dev.mysql.com/doc/refman/8.0/en/cast-functions.html#function_convert) 函数用于在 [字符集](/character-set-and-collation.md) 之间进行转换。

示例：

```sql
SELECT CONVERT(0x616263 USING utf8mb4);
```

```sql
+---------------------------------+
| CONVERT(0x616263 USING utf8mb4) |
+---------------------------------+
| abc                             |
+---------------------------------+
1 行，耗时 0.0004 秒
```

## MySQL 兼容性

- TiDB 不支持对 `SPATIAL` 类型的 cast 操作。更多信息请参见 [#6347](https://github.com/pingcap/tidb/issues/6347)。
- TiDB 不支持 `CAST()` 中的 `AT TIME ZONE`。更多信息请参见 [#51742](https://github.com/pingcap/tidb/issues/51742)。
- `CAST(24 AS YEAR)` 在 TiDB 中返回 2 位数字，在 MySQL 中返回 4 位数字。更多信息请参见 [#29629](https://github.com/pingcap/tidb/issues/29629)。