---
title: Set Operations
summary: Learn the supported set operations in TiDB.
---

# セット操作 {#set-operations}

TiDBは、UNION、EXCEPT、およびINTERSECT演算子を使用した3つの集合演算をサポートしています。セットの最小単位は[`SELECT`ステートメント](/sql-statements/sql-statement-select.md)です。

## UNIONオペレーター {#union-operator}

数学では、2つのセットAとBの和集合は、AまたはBにあるすべての要素で構成されます。次に例を示します。

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

TiDBは、 `UNION DISTINCT`つと`UNION ALL`のオペレーターの両方をサポートします。 `UNION DISTINCT`は結果セットから重複レコードを削除し、 `UNION ALL`は重複を含むすべてのレコードを保持します。 TiDBではデフォルトで`UNION DISTINCT`が使用されます。

{{< copyable "" >}}

```sql
create table t1 (a int);
create table t2 (a int);
insert into t1 values (1),(2);
insert into t2 values (1),(3);
```

`UNION DISTINCT`クエリと`UNION ALL`クエリの例は、それぞれ次のとおりです。

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

## EXCEPT演算子 {#except-operator}

AとBが2つのセットである場合、EXCEPTは、AにはあるがBにはない要素で構成されるAとBの差分セットを返します。

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

## INTERSECT演算子 {#intersect-operator}

数学では、2つのセットAとBの共通部分は、AとBの両方にあるすべての要素で構成され、他の要素は含まれません。

```sql
select * from t1 intersect select * from t2;
+---+
| a |
+---+
| 1 |
+---+
1 rows in set (0.00 sec)
```

`INTERSECT ALL`演算子はまだサポートされていません。 INTERSECT演算子は、EXCEPTおよびUNION演算子よりも優先されます。

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

TiDBは、括弧を使用して集合演算の優先順位を指定することをサポートしています。括弧内の式が最初に処理されます。

```sql
(select * from t1 union all select * from t1) intersect select * from t2;
+---+
| a |
+---+
| 1 |
+---+
1 rows in set (0.00 sec)
```

## <code>Order By</code>と<code>Limit</code>を使用する {#use-code-order-by-code-and-code-limit-code}

TiDBは、セット操作での[`ORDER BY`](/media/sqlgram/OrderByOptional.png)つまたは[`LIMIT`](/media/sqlgram/LimitClause.png)の句の使用をサポートしています。これらの2つの句は、ステートメント全体の最後にある必要があります。

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
