---
title: CLIENT_ERRORS_SUMMARY_BY_USER
summary: CLIENT_ERRORS_SUMMARY_BY_USER` INFORMATION_SCHEMA テーブルについて学習します。
---

# クライアントエラー概要（ユーザー別） {#client-errors-summary-by-user}

表`CLIENT_ERRORS_SUMMARY_BY_USER` 、TiDBサーバーに接続したクライアントに返されたSQLエラーと警告の概要を示しています。これには以下が含まれます。

-   不正な SQL ステートメント。
-   ゼロ除算エラー。
-   範囲外または重複したキー値を挿入しようとしました。
-   権限エラー。
-   存在しないテーブル。

クライアントエラーはMySQLサーバープロトコルを介してクライアントに返され、アプリケーションは適切なアクションを実行することが期待されます。1 `INFORMATION_SCHEMA.CLIENT_ERRORS_SUMMARY_BY_USER`表は、アプリケーションがTiDBサーバーから返されたエラーを適切に処理（またはログに記録）していないシナリオにおいて、エラーを検査するための便利な方法を提供します。

`CLIENT_ERRORS_SUMMARY_BY_USER`ユーザーごとにエラーを要約するため、あるユーザーサーバーが他のサーバーよりも多くのエラーを生成しているシナリオを診断するのに役立ちます。考えられるシナリオには以下が含まれます。

-   権限エラー。
-   テーブルまたはリレーショナル オブジェクトが見つかりません。
-   SQL 構文が正しくないか、アプリケーションと TiDB のバージョン間に互換性がありません。

集計されたカウントは、ステートメント`FLUSH CLIENT_ERRORS_SUMMARY`でリセットできます。集計は各 TiDBサーバーにローカルであり、メモリ内にのみ保持されます。TiDBサーバーが再起動すると、集計は失われます。

```sql
USE INFORMATION_SCHEMA;
DESC CLIENT_ERRORS_SUMMARY_BY_USER;
```

出力は次のようになります。

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
-   `ERROR_NUMBER` : 返された MySQL 互換エラー番号。
-   `ERROR_MESSAGE` : エラー番号に一致するエラー メッセージ (プリペアドステートメント形式)。
-   `ERROR_COUNT` : このエラーがユーザーに返された回数。
-   `WARNING_COUNT` : この警告がユーザーに返された回数。
-   `FIRST_SEEN` : このエラー (または警告) がユーザーに初めて送信されたとき。
-   `LAST_SEEN` : このエラー (または警告) がユーザーに最後に送信された時刻。

以下の例は、クライアントがローカルTiDBサーバーに接続する際に生成される警告を示しています。1 `FLUSH CLIENT_ERRORS_SUMMARY`実行するとサマリーはリセットされます。

```sql
SELECT 0/0;
SELECT * FROM CLIENT_ERRORS_SUMMARY_BY_USER;
FLUSH CLIENT_ERRORS_SUMMARY;
SELECT * FROM CLIENT_ERRORS_SUMMARY_BY_USER;
```

出力は次のようになります。

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
