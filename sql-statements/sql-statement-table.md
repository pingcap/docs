---
title: TABLE | TiDB SQL Statement Reference
summary: テーブルステートメントは、集計や複雑なフィルタリングが不要な場合に使用されます。`SELECT * FROM`の代わりに`TABLE`ステートメントを使用できます。MySQL 8.0.19で導入されたこのステートメントは、テーブルの作成、データの挿入、データの表示、および並べ替えを行うことができます。これにより、データベースの操作がより簡単になります。
---

# テーブル {#table}

集計や複雑なフィルタリングが必要ない場合は、 `SELECT * FROM`の代わりに`TABLE`ステートメントを使用できます。

## あらすじ {#synopsis}

```ebnf+diagram
TableStmt ::=
    "TABLE" Table ( "ORDER BY" Column )? ( "LIMIT" NUM )?
```

## 例 {#examples}

テーブル`t1`を作成します。

```sql
CREATE TABLE t1(id INT PRIMARY KEY);
```

`t1`にデータを挿入します。

```sql
INSERT INTO t1 VALUES (1),(2),(3);
```

表`t1`のデータをビュー。

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

`t1`クエリし、結果を`id`フィールドで降順に並べ替えます。

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

`t1`の最初のレコードをクエリします。

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

`TABLE`ステートメントは MySQL 8.0.19 で導入されました。

## こちらも参照 {#see-also}

-   [`SELECT`](/sql-statements/sql-statement-select.md)
-   [MySQL の`TABLE`ステートメント](https://dev.mysql.com/doc/refman/8.0/en/table.html)
