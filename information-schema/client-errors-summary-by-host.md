---
title: CLIENT_ERRORS_SUMMARY_BY_HOST
summary: Learn about the `CLIENT_ERRORS_SUMMARY_BY_HOST` INFORMATION_SCHEMA table.
---

# CLIENT_ERRORS_SUMMARY_BY_HOST {#client-errors-summary-by-host}

表`CLIENT_ERRORS_SUMMARY_BY_HOST`は、TiDBサーバーに接続するクライアントに返される SQL エラーと警告の概要を示しています。これらには次のものが含まれます。

-   不正な形式の SQL ステートメント。
-   ゼロ除算エラー。
-   範囲外または重複したキー値を挿入しようとしました。
-   許可エラー。
-   存在しないテーブル。

これらのエラーは MySQLサーバープロトコル経由でクライアントに返され、アプリケーションは適切なアクションを実行することが期待されます。表`INFORMATION_SCHEMA.CLIENT_ERRORS_SUMMARY_BY_HOST`は、アプリケーションが TiDBサーバーから返されたエラーを正しく処理 (またはログ記録) していないシナリオでエラーを検査する便利な方法を提供します。

`CLIENT_ERRORS_SUMMARY_BY_HOST`リモート ホストごとにエラーを要約するため、あるアプリケーションサーバーが他のサーバーよりも多くのエラーを生成しているシナリオを診断するのに役立ちます。考えられるシナリオは次のとおりです。

-   古い MySQL クライアント ライブラリ。
-   古いアプリケーション (新しい展開をロールアウトするときにこのサーバーが見つからなかった可能性があります)。
-   ユーザー権限の「ホスト」部分の誤った使用。
-   ネットワーク接続の信頼性が低いため、タイムアウトや接続の切断が増加します。

要約されたカウントは、ステートメント`FLUSH CLIENT_ERRORS_SUMMARY`を使用してリセットできます。概要は各 TiDBサーバーに対してローカルであり、メモリ内にのみ保持されます。 TiDBサーバーが再起動すると、サマリーは失われます。

```sql
USE INFORMATION_SCHEMA;
DESC CLIENT_ERRORS_SUMMARY_BY_HOST;
```

出力は次のとおりです。

```sql
+---------------+---------------+------+------+---------+-------+
| Field         | Type          | Null | Key  | Default | Extra |
+---------------+---------------+------+------+---------+-------+
| HOST          | varchar(255)  | NO   |      | NULL    |       |
| ERROR_NUMBER  | bigint(64)    | NO   |      | NULL    |       |
| ERROR_MESSAGE | varchar(1024) | NO   |      | NULL    |       |
| ERROR_COUNT   | bigint(64)    | NO   |      | NULL    |       |
| WARNING_COUNT | bigint(64)    | NO   |      | NULL    |       |
| FIRST_SEEN    | timestamp     | YES  |      | NULL    |       |
| LAST_SEEN     | timestamp     | YES  |      | NULL    |       |
+---------------+---------------+------+------+---------+-------+
7 rows in set (0.00 sec)
```

フィールドの説明:

-   `HOST` : クライアントのリモートホスト。
-   `ERROR_NUMBER` : 返された MySQL 互換のエラー番号。
-   `ERROR_MESSAGE` : エラー番号と一致するエラー メッセージ (プリペアドステートメント形式)。
-   `ERROR_COUNT` : このエラーがクライアント ホストに返された回数。
-   `WARNING_COUNT` : この警告がクライアント ホストに返された回数。
-   `FIRST_SEEN` : このエラー (または警告) がクライアント ホストから初めて確認されたとき。
-   `LAST_SEEN` : このエラー (または警告) がクライアント ホストから最後に確認された時刻。

次の例は、クライアントがローカル TiDBサーバーに接続するときに生成される警告を示しています。 `FLUSH CLIENT_ERRORS_SUMMARY`を実行するとサマリーがリセットされます。

```sql
SELECT 0/0;
SELECT * FROM CLIENT_ERRORS_SUMMARY_BY_HOST;
FLUSH CLIENT_ERRORS_SUMMARY;
SELECT * FROM CLIENT_ERRORS_SUMMARY_BY_HOST;
```

出力は次のとおりです。

```sql
+-----+
| 0/0 |
+-----+
| NULL |
+-----+
1 row in set, 1 warning (0.00 sec)

+-----------+--------------+---------------+-------------+---------------+---------------------+---------------------+
| HOST      | ERROR_NUMBER | ERROR_MESSAGE | ERROR_COUNT | WARNING_COUNT | FIRST_SEEN          | LAST_SEEN           |
+-----------+--------------+---------------+-------------+---------------+---------------------+---------------------+
| 127.0.0.1 |         1365 | Division by 0 |           0 |             1 | 2021-03-18 12:51:54 | 2021-03-18 12:51:54 |
+-----------+--------------+---------------+-------------+---------------+---------------------+---------------------+
1 row in set (0.00 sec)

Query OK, 0 rows affected (0.00 sec)

Empty set (0.00 sec)
```
