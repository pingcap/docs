---
title: CREATE VIEW
summary: クエリに基づいて新しいビューを作成します。Logical View は物理データを保存せず、論理ビューにアクセスすると、処理を完了するために SQL をサブクエリ形式に変換します。
---

# CREATE VIEW

クエリに基づいて新しいビューを作成します。Logical View は物理データを保存せず、論理ビューにアクセスすると、処理を完了するために SQL をサブクエリ形式に変換します。

たとえば、次のような Logical View を作成したとします。

```sql
CREATE VIEW view_t1 AS SELECT a, b FROM t1;
```

そして、次のようなクエリを実行するとします。

```sql
SELECT a FROM view_t1;
```

その結果は、次のクエリと同じです。

```sql
SELECT a FROM (SELECT a, b FROM t1);
```

そのため、ビューが依存しているテーブルを削除すると、元のテーブルが存在しないというエラーが発生します。この場合は、古いビューを削除し、必要な新しいビューを再作成する必要があることがあります。

## 構文 {#syntax}

```sql
CREATE [ OR REPLACE ] VIEW [ IF NOT EXISTS ] [ db. ]view_name [ (<column>, ...) ] AS SELECT query
```

## アクセス制御の要件 {#access-control-requirements}

ビューにアクセスするには、ユーザーはビュー自体に対する SELECT 権限のみが必要です。

ビューの基になるテーブルに対して個別の権限は必要ありません。この仕組みにより、アクセス制御が簡素化され、データセキュリティが向上します。

## 例 {#examples}

```sql
CREATE VIEW tmp_view(c1, c2) AS SELECT number % 3 AS a, avg(number) FROM numbers(1000) GROUP BY a ORDER BY a;

SELECT * FROM tmp_view;
+------+-------+
| c1   | c2    |
+------+-------+
|    0 | 499.5 |
|    1 | 499.0 |
|    2 | 500.0 |
+------+-------+
```