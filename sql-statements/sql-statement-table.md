---
title: TABLE | TiDB SQL Statement Reference
summary: An overview of the usage of TABLE for the TiDB database.
---

# テーブル {#table}

集計や複雑なフィルタリングが必要ない場合は、 `SELECT * FROM`の代わりに`TABLE`のステートメントを使用できます。

## あらすじ {#synopsis}

```ebnf+diagram
TableStmt ::=
    "TABLE" Table ( "ORDER BY" Column )? ( "LIMIT" NUM )?
```

## 例 {#examples}

{{< copyable "" >}}

```sql
CREATE TABLE t1(id INT PRIMARY KEY);
```

```sql
Query OK, 0 rows affected (0.31 sec)
```

{{< copyable "" >}}

```sql
INSERT INTO t1 VALUES (1),(2),(3);
```

```sql
Query OK, 3 rows affected (0.06 sec)
Records: 3  Duplicates: 0  Warnings: 0
```

{{< copyable "" >}}

```sql
TABLE t1;
```

```sql
+----+
| id |
+----+
|  1 |
|  2 |
|  3 |
+----+
3 rows in set (0.01 sec)
```

{{< copyable "" >}}

```sql
TABLE t1 ORDER BY id DESC;
```

```sql
+----+
| id |
+----+
|  3 |
|  2 |
|  1 |
+----+
3 rows in set (0.01 sec)
```

{{< copyable "" >}}

```sql
TABLE t1 LIMIT 1;
```

```sql
+----+
| id |
+----+
|  1 |
+----+
1 row in set (0.01 sec)
```

## MySQLの互換性 {#mysql-compatibility}

`TABLE`ステートメントはMySQL8.0.19で導入されました。

## も参照してください {#see-also}

-   [選択する](/sql-statements/sql-statement-select.md)
-   [MySQLのTABLEステートメント](https://dev.mysql.com/doc/refman/8.0/en/table.html)
