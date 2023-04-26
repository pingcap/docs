---
title: CLIENT_ERRORS_SUMMARY_BY_USER
summary: Learn about the `CLIENT_ERRORS_SUMMARY_BY_USER` INFORMATION_SCHEMA table.
---

# CLIENT_ERRORS_SUMMARY_BY_USER {#client-errors-summary-by-user}

表`CLIENT_ERRORS_SUMMARY_BY_USER`は、TiDBサーバーに接続するクライアントに返された SQL エラーと警告の概要を示しています。これらには以下が含まれます：

-   不正な SQL ステートメント。
-   ゼロ エラーによる除算。
-   範囲外または重複するキー値を挿入しようとしています。
-   許可エラー。
-   存在しないテーブル。

クライアント エラーは、MySQLサーバープロトコルを介してクライアントに返され、そこでアプリケーションは適切なアクションを実行することが期待されます。 `INFORMATION_SCHEMA.CLIENT_ERRORS_SUMMARY_BY_USER`テーブルは、アプリケーションが TiDBサーバーによって返されたエラーを正しく処理 (またはログ記録) していないシナリオでエラーを検査するための便利な方法を提供します。

`CLIENT_ERRORS_SUMMARY_BY_USER`ユーザーごとにエラーを要約するため、あるユーザーサーバーが他のサーバーよりも多くのエラーを生成しているシナリオを診断するのに役立ちます。考えられるシナリオは次のとおりです。

-   許可エラー。
-   テーブルまたはリレーショナル オブジェクトがありません。
-   SQL 構文が正しくないか、アプリケーションと TiDB のバージョンの間に互換性がない。

集計されたカウントは、ステートメント`FLUSH CLIENT_ERRORS_SUMMARY`でリセットできます。要約は各 TiDBサーバーにローカルであり、メモリにのみ保持されます。 TiDBサーバーが再起動すると、サマリーは失われます。

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
-   `ERROR_MESSAGE` : エラー番号に一致するエラー メッセージ (プリペアドステートメント形式)。
-   `ERROR_COUNT` : このエラーがユーザーに返された回数。
-   `WARNING_COUNT` : この警告がユーザーに返された回数。
-   `FIRST_SEEN` : このエラー (または警告) が初めてユーザーに送信された時刻。
-   `LAST_SEEN` : このエラー (または警告) がユーザーに最後に送信された時刻。

次の例は、クライアントがローカル TiDBサーバーに接続するときに生成される警告を示しています。サマリーは`FLUSH CLIENT_ERRORS_SUMMARY`を実行した後にリセットされます:

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
