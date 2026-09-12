---
title: GROUPING
summary: 返回一个位掩码，用于指示哪些 `GROUP BY` 表达式未包含在当前分组集中。位从右到左分配，最右侧参数对应最低有效位；如果对应表达式包含在生成当前结果行的分组集的分组条件中，则该位为 0，否则为 1。
---

# GROUPING

返回一个位掩码，用于指示哪些 `GROUP BY` 表达式未包含在当前分组集中。位从右到左分配，最右侧参数对应最低有效位；如果对应表达式包含在生成当前结果行的分组集的分组条件中，则该位为 0，否则为 1。

## 语法 {#syntax}

```sql
GROUPING ( expr [, expr, ...] )
```

> **注意：**
>
> `GROUPING` 只能与 `GROUPING SETS`、`ROLLUP` 或 `CUBE` 一起使用，并且其参数必须在 grouping sets 列表中。

## 参数 {#arguments}

分组集项。

## 返回类型 {#return-type}

UInt32。

## 示例 {#examples}

```sql
select a, b, grouping(a), grouping(b), grouping(a,b), grouping(b,a) from t group by grouping sets ((a,b),(a),(b), ()) ;
+------+------+-------------+-------------+----------------+----------------+
| a    | b    | grouping(a) | grouping(b) | grouping(a, b) | grouping(b, a) |
+------+------+-------------+-------------+----------------+----------------+
| NULL | A    |           1 |           0 |              2 |              1 |
| a    | NULL |           0 |           1 |              1 |              2 |
| b    | A    |           0 |           0 |              0 |              0 |
| NULL | NULL |           1 |           1 |              3 |              3 |
| a    | A    |           0 |           0 |              0 |              0 |
| b    | B    |           0 |           0 |              0 |              0 |
| b    | NULL |           0 |           1 |              1 |              2 |
| a    | B    |           0 |           0 |              0 |              0 |
| NULL | B    |           1 |           0 |              2 |              1 |
+------+------+-------------+-------------+----------------+----------------+
```