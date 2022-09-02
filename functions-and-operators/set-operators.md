---
title: Set Operations
summary: Learn the supported set operations in TiDB.
---

# セット操作 {#set-operations}

TiDB は、UNION、EXCEPT、および INTERSECT 演算子を使用した 3 つのセット操作をサポートしています。セットの最小単位は[`SELECT`ステートメント](/sql-statements/sql-statement-select.md)です。

## UNION 演算子 {#union-operator}

数学では、2 つのセット A と B の結合は、A または B にあるすべての要素で構成されます。たとえば、次のようになります。

```sql
select 1 union select 2;
+---+
| 1 |
+---+
| 2 |
| 1 |
+---+
2 rows in set (0.00 sec)
```

TiDB は、 `UNION DISTINCT`演算子と`UNION ALL`演算子の両方をサポートしています。 `UNION DISTINCT`は結果セットから重複レコードを削除しますが、 `UNION ALL`は重複を含むすべてのレコードを保持します。 TiDB ではデフォルトで`UNION DISTINCT`が使用されます。

{{< copyable "" >}}

```sql
create table t1 (a int);
create table t2 (a int);
insert into t1 values (1),(2);
insert into t2 values (1),(3);
```

`UNION DISTINCT`と`UNION ALL`のクエリの例は、それぞれ次のとおりです。

```sql
select * from t1 union distinct select * from t2;
+---+
| a |
+---+
| 1 |
| 2 |
| 3 |
+---+
3 rows in set (0.00 sec)
select * from t1 union all select * from t2;
+---+
| a |
+---+
| 1 |
| 2 |
| 1 |
| 3 |
+---+
4 rows in set (0.00 sec)
```

## EXCEPT 演算子 {#except-operator}

A と B が 2 つのセットである場合、EXCEPT は、A には含まれるが B には含まれない要素で構成される A と B の差分セットを返します。

```sql
select * from t1 except select * from t2;
+---+
| a |
+---+
| 2 |
+---+
1 rows in set (0.00 sec)
```

`EXCEPT ALL`演算子はまだサポートされていません。

## INTERSECT 演算子 {#intersect-operator}

数学では、2 つのセット A と B の交点は、A と B の両方にあるすべての要素で構成され、他の要素は含まれません。

```sql
select * from t1 intersect select * from t2;
+---+
| a |
+---+
| 1 |
+---+
1 rows in set (0.00 sec)
```

`INTERSECT ALL`演算子はまだサポートされていません。 INTERSECT 演算子は、EXCEPT および UNION 演算子よりも優先されます。

```sql
select * from t1 union all select * from t1 intersect select * from t2;
+---+
| a |
+---+
| 1 |
| 1 |
| 2 |
+---+
3 rows in set (0.00 sec)
```

## 括弧 {#parentheses}

TiDB は、集合操作の優先順位を指定するための括弧の使用をサポートしています。括弧内の式が最初に処理されます。

```sql
(select * from t1 union all select * from t1) intersect select * from t2;
+---+
| a |
+---+
| 1 |
+---+
1 rows in set (0.00 sec)
```

## 並べ<code>Order By</code>と<code>Limit</code>を使用する {#use-code-order-by-code-and-code-limit-code}

TiDB は、集合操作での[`ORDER BY`](/media/sqlgram/OrderByOptional.png)つまたは[`LIMIT`](/media/sqlgram/LimitClause.png)の句の使用をサポートしています。これら 2 つの句は、ステートメント全体の最後にある必要があります。

```sql
(select * from t1 union all select * from t1 intersect select * from t2) order by a limit 2;
+---+
| a |
+---+
| 1 |
| 1 |
+---+
2 rows in set (0.00 sec)
```
