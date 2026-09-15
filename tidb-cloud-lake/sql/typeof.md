---
title: TYPEOF
summary: TYPEOF 函数用于返回数据类型的名称。
---

# TYPEOF

TYPEOF 函数用于返回数据类型的名称。

## 语法 {#syntax}

```sql
TYPEOF( <expr> )
```

## 参数 {#arguments}

| 参数 | 描述 |
| ----------- | ----------- |
| `<expr>` | 任意表达式。<br /> 这可以是列名、另一个函数的结果，或数学运算。 |

## 返回类型 {#return-type}

字符串

## 示例 {#examples}

```sql
SELECT typeof(1::INT);
+------------------+
| typeof(1::Int32) |
+------------------+
| INT              |
+------------------+
```