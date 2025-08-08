---
title: mysql.tidb_mdl_view
summary: mysql` スキーマの `tidb_mdl_view` テーブルについて学習します。
---

# <code>mysql.tidb_mdl_view</code> {#code-mysql-tidb-mdl-view-code}

この表には[メタデータロック](/metadata-lock.md)ビューに関する情報が表示されます。

```sql
DESC mysql.tidb_mdl_view;
```

出力は次のようになります。

    +-------------+-----------------+------+------+---------+-------+
    | Field       | Type            | Null | Key  | Default | Extra |
    +-------------+-----------------+------+------+---------+-------+
    | job_id      | bigint          | NO   | PRI  | NULL    |       |
    | db_name     | longtext        | YES  |      | NULL    |       |
    | table_name  | longtext        | YES  |      | NULL    |       |
    | query       | longtext        | YES  |      | NULL    |       |
    | session_id  | bigint unsigned | YES  |      | NULL    |       |
    | start_time  | timestamp(6)    | YES  |      | NULL    |       |
    | SQL_DIGESTS | varchar(5)      | YES  |      | NULL    |       |
    +-------------+-----------------+------+------+---------+-------+
    7 rows in set (0.00 sec)

## フィールド {#fields}

-   `job_id` : ジョブの識別子。
-   `db_name` : データベース名。
-   `table_name` : テーブル名。
-   `query` : クエリ。
-   `session_id` : セッションの識別子。
-   `start_time` : 開始時刻。この列は以前のバージョンでは`TxnStart`呼ばれていました。
-   `SQL_DIGESTS` : SQL ステートメントのダイジェスト。
