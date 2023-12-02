---
title: CLIENT_ERRORS_SUMMARY_BY_USER
summary: Learn about the `CLIENT_ERRORS_SUMMARY_BY_USER` INFORMATION_SCHEMA table.
---

# CLIENT_ERRORS_SUMMARY_BY_USER {#client-errors-summary-by-user}

表`CLIENT_ERRORS_SUMMARY_BY_USER`は、TiDBサーバーに接続するクライアントに返される SQL エラーと警告の概要を示しています。これらには次のものが含まれます。

-   不正な形式の SQL ステートメント。
-   ゼロ除算エラー。
-   範囲外または重複したキー値を挿入しようとしました。
-   許可エラー。
-   存在しないテーブル。

クライアント エラーは MySQLサーバープロトコル経由でクライアントに返され、アプリケーションは適切なアクションを実行することが期待されます。表`INFORMATION_SCHEMA.CLIENT_ERRORS_SUMMARY_BY_USER`は、アプリケーションが TiDBサーバーから返されたエラーを正しく処理 (またはログ記録) していないシナリオでエラーを検査するための便利な方法を提供します。

`CLIENT_ERRORS_SUMMARY_BY_USER`ユーザーごとにエラーを要約するため、あるユーザーサーバーが他のサーバーよりも多くのエラーを生成しているシナリオを診断するのに役立ちます。考えられるシナリオは次のとおりです。

-   許可エラー。
-   テーブルまたはリレーショナル オブジェクトが欠落しています。
-   SQL 構文が間違っているか、アプリケーションと TiDB のバージョンとの間に互換性がない。

要約されたカウントはステートメント`FLUSH CLIENT_ERRORS_SUMMARY`でリセットできます。概要は各 TiDBサーバーに対してローカルであり、メモリ内にのみ保持されます。 TiDBサーバーが再起動すると、サマリーは失われます。

```sql
USE INFORMATION_SCHEMA;
DESC CLIENT_ERRORS_SUMMARY_BY_USER;
```

出力は次のとおりです。

```sql
+---------------+---------------+------+------+---------+-------+
| Field         | Type          | Null | Key  | Default | Extra |
+---------------+---------------+------+------+---------+-------+
| USER          | varchar(64)   | NO   |      | NULL    |       |
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

-   `USER` : 認証されたユーザー。
-   `ERROR_NUMBER` : 返された MySQL 互換のエラー番号。
-   `ERROR_MESSAGE` : エラー番号と一致するエラー メッセージ (プリペアドステートメント形式)。
-   `ERROR_COUNT` : このエラーがユーザーに返された回数。
-   `WARNING_COUNT` : この警告がユーザーに返された回数。
-   `FIRST_SEEN` : このエラー (または警告) が初めてユーザーに送信されたとき。
-   `LAST_SEEN` : このエラー (または警告) がユーザーに送信された最新の時刻。

次の例は、クライアントがローカル TiDBサーバーに接続するときに生成される警告を示しています。 `FLUSH CLIENT_ERRORS_SUMMARY`を実行するとサマリーがリセットされます。

```sql
SELECT 0/0;
SELECT * FROM CLIENT_ERRORS_SUMMARY_BY_USER;
FLUSH CLIENT_ERRORS_SUMMARY;
SELECT * FROM CLIENT_ERRORS_SUMMARY_BY_USER;
```

出力は次のとおりです。

```sql
+-----+
| 0/0 |
+-----+
| NULL |
+-----+
1 row in set, 1 warning (0.00 sec)

+------+--------------+---------------+-------------+---------------+---------------------+---------------------+
| USER | ERROR_NUMBER | ERROR_MESSAGE | ERROR_COUNT | WARNING_COUNT | FIRST_SEEN          | LAST_SEEN           |
+------+--------------+---------------+-------------+---------------+---------------------+---------------------+
| root |         1365 | Division by 0 |           0 |             1 | 2021-03-18 13:05:36 | 2021-03-18 13:05:36 |
+------+--------------+---------------+-------------+---------------+---------------------+---------------------+
1 row in set (0.00 sec)

Query OK, 0 rows affected (0.00 sec)

Empty set (0.00 sec)
```
