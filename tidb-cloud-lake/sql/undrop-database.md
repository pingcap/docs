---
title: UNDROP DATABASE
summary: 削除されたデータベースの最新バージョンを復元します。これは {{{ .lake }}} の Time Travel 機能を利用しており、削除されたオブジェクトを復元できるのは保持期間内のみです（デフォルトは 24 時間）。
---

# UNDROP DATABASE

削除されたデータベースの最新バージョンを復元します。これは {{{ .lake }}} の Time Travel 機能を利用しており、削除されたオブジェクトを復元できるのは保持期間内のみです（デフォルトは 24 時間）。

**See also:**

- [DROP DATABASE](/tidb-cloud-lake/sql/drop-database.md)
- [SHOW DROP DATABASES](/tidb-cloud-lake/sql/show-drop-databases.md)

## 構文 {#syntax}

```sql
UNDROP DATABASE <database_name>
```

- 同じ名前のデータベースがすでに存在する場合は、エラーが返されます。

    ```sql title='Examples:'
    root@localhost:8000/default> CREATE DATABASE doc;
    processed in (0.030 sec)

    root@localhost:8000/default> DROP DATABASE doc;
    processed in (0.028 sec)

    root@localhost:8000/default> CREATE DATABASE doc;
    processed in (0.028 sec)

    root@localhost:8000/default> UNDROP DATABASE doc;
    error: APIError: QueryFailed: [2301]Database 'doc' already exists
    ```

- データベースを UNDROP しても、元のロールへの所有権は自動的には復元されません。UNDROP 後は、以前のロールまたは別のロールに対して所有権を手動で付与する必要があります。それまでは、そのデータベースにアクセスできるのは `account-admin` ロールのみです。

    ```sql title='Examples:'
    GRANT OWNERSHIP on doc.* to ROLE writer;
    ```

## 例 {#examples}

この例では、`orders_2024` という名前のデータベースを作成し、削除してから復元します。

```sql
root@localhost:8000/default> CREATE DATABASE orders_2024;

CREATE DATABASE orders_2024

0 row written in 0.014 sec. Processed 0 row, 0 B (0 row/s, 0 B/s)

root@localhost:8000/default> DROP DATABASE orders_2024;

DROP DATABASE orders_2024

0 row written in 0.012 sec. Processed 0 row, 0 B (0 row/s, 0 B/s)

root@localhost:8000/default> UNDROP DATABASE orders_2024;

UNDROP DATABASE orders_2024

0 row read in 0.011 sec. Processed 0 row, 0 B (0 row/s, 0 B/s)
```