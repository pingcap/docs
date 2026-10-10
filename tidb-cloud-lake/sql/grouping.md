---
title: GROUPING
summary: 現在の grouping set に含まれていない `GROUP BY` 式を示すビットマスクを返します。ビットは右端の引数が最下位ビットに対応するように割り当てられます。各ビットは、現在の結果行を生成した grouping set のグループ化条件に対応する式が含まれている場合は 0、含まれていない場合は 1 です。
---

# GROUPING

現在の grouping set に含まれていない `GROUP BY` 式を示すビットマスクを返します。ビットは右端の引数が最下位ビットに対応するように割り当てられます。各ビットは、現在の結果行を生成した grouping set のグループ化条件に対応する式が含まれている場合は 0、含まれていない場合は 1 です。

## 構文 {#syntax}

```sql
GROUPING ( expr [, expr, ...] )
```

> **Note:**
>
> `GROUPING` は `GROUPING SETS`、`ROLLUP`、または `CUBE` と組み合わせてのみ使用でき、引数は grouping sets のリスト内に含まれている必要があります。

## 引数 {#arguments}

Grouping sets の項目です。

## 戻り値の型 {#return-type}

UInt32。

## 例 {#examples}

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