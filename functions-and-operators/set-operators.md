---
title: Set Operations
summary: Learn the supported set operations in TiDB.
---

# セット操作 {#set-operations}

TiDB は、UNION、EXCEPT、および INTERSECT 演算子を使用した 3 つのセット操作をサポートしています。セットの最小単位は[`SELECT`ステートメント](/sql-statements/sql-statement-select.md)です。

## UNION 演算子 {#union-operator}

数学では、2 つのセット A と B の結合は、A または B にあるすべての要素で構成されます。たとえば、次のようになります。

```sql
SELECT 1 UNION SELECT 2;
+---+
| 1 |
+---+
| 2 |
| 1 |
+---+
2 rows in set (0.00 sec)
```

TiDB は、 `UNION DISTINCT`と`UNION ALL`演算子の両方をサポートしています。 `UNION DISTINCT`結果セットから重複レコードを削除しますが、 `UNION ALL`重複を含むすべてのレコードを保持します。 TiDB ではデフォルトで`UNION DISTINCT`が使用されます。

```sql
CREATE TABLE t1 (a int);
CREATE TABLE t2 (a int);
INSERT INTO t1 VALUES (1),(2);
INSERT INTO t2 VALUES (1),(3);
```

`UNION DISTINCT`と`UNION ALL`クエリの例は、それぞれ次のとおりです。

```sql
SELECT * FROM t1 UNION DISTINCT SELECT * FROM t2;
+---+
| a |
+---+
| 1 |
| 2 |
| 3 |
+---+
3 rows in set (0.00 sec)

SELECT * FROM t1 UNION ALL SELECT * FROM t2;
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
SELECT * FROM t1 EXCEPT SELECT * FROM t2;
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
SELECT * FROM t1 INTERSECT SELECT * FROM t2;
+---+
| a |
+---+
| 1 |
+---+
1 rows in set (0.00 sec)
```

`INTERSECT ALL`演算子はまだサポートされていません。 INTERSECT 演算子は、EXCEPT および UNION 演算子よりも優先されます。

```sql
SELECT * FROM t1 UNION ALL SELECT * FROM t1 INTERSECT SELECT * FROM t2;
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
(SELECT * FROM t1 UNION ALL SELECT * FROM t1) INTERSECT SELECT * FROM t2;
+---+
| a |
+---+
| 1 |
+---+
1 rows in set (0.00 sec)
```

## <code>ORDER BY</code>と<code>LIMIT</code>を使用する {#use-code-order-by-code-and-code-limit-code}

TiDB は、集合操作での[`ORDER BY`](/media/sqlgram/OrderByOptional.png)または[`LIMIT`](/media/sqlgram/LimitClause.png)句の使用をサポートしています。これら 2 つの句は、ステートメント全体の最後にある必要があります。

```sql
(SELECT * FROM t1 UNION ALL SELECT * FROM t1 INTERSECT SELECT * FROM t2) ORDER BY a LIMIT 2;
+---+
| a |
+---+
| 1 |
| 1 |
+---+
2 rows in set (0.00 sec)
```
