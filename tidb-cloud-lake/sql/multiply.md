---
title: MULTIPLY
summary: MULTIPLY 函数对两个数字执行乘法运算。它等价于使用 `*` 运算符。
---

# MULTIPLY

MULTIPLY 函数对两个数字执行乘法运算。它等价于使用 `*` 运算符。

## 语法 {#syntax}

```sql
MULTIPLY(x, y)
-- Or using the operator syntax
x * y
```

## 参数 {#arguments}

| 参数 | 描述 |
|-----------|-------------|
| x, y      | 要相乘的数值表达式。 |

## 返回类型 {#return-type}

根据输入参数，返回具有适当数据类型的数值。

## 示例 {#examples}

```sql
-- Using the function syntax
SELECT MULTIPLY(5, 3);
+----------------+
| MULTIPLY(5, 3) |
+----------------+
|             15 |
+----------------+

-- Using the operator syntax
SELECT 5 * 3;
+-------+
| 5 * 3 |
+-------+
|    15 |
+-------+

-- With decimal numbers
SELECT MULTIPLY(2.5, 4);
+------------------+
| MULTIPLY(2.5, 4) |
+------------------+
|             10.0 |
+------------------+

-- With column references
SELECT number, MULTIPLY(number, 10) AS multiplied
FROM numbers(5);
+--------+------------+
| number | multiplied |
+--------+------------+
|      0 |          0 |
|      1 |         10 |
|      2 |         20 |
|      3 |         30 |
|      4 |         40 |
+--------+------------+
```

## 另请参阅 {#see-also}

- [PLUS](/tidb-cloud-lake/sql/plus.md) / [ADD](/tidb-cloud-lake/sql/add.md)
- [MINUS](/tidb-cloud-lake/sql/minus.md) / [SUBTRACT](/tidb-cloud-lake/sql/subtract.md)
- [DIV](/tidb-cloud-lake/sql/div.md)