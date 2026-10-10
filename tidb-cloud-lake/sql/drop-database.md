---
title: DROP DATABASE
summary: データベースを削除します。
---

# DROP DATABASE

データベースを削除します。

関連情報: [UNDROP DATABASE](/tidb-cloud-lake/sql/undrop-database.md)

## 構文 {#syntax}

```sql
DROP { DATABASE | SCHEMA } [ IF EXISTS ] <database_name>
```

`DROP SCHEMA` は `DROP DATABASE` の同義語です。

## 例 {#examples}

この例では、`orders_2024` という名前のデータベースを作成してから削除します。

```sql
root@localhost:8000/default> CREATE DATABASE orders_2024;

CREATE DATABASE orders_2024

0 row written in 0.014 sec. Processed 0 row, 0 B (0 row/s, 0 B/s)

root@localhost:8000/default> DROP DATABASE orders_2024;

DROP DATABASE orders_2024

0 row written in 0.012 sec. Processed 0 row, 0 B (0 row/s, 0 B/s)
```