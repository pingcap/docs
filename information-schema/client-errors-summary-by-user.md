---
title: CLIENT_ERRORS_SUMMARY_BY_USER
summary: Learn about the `CLIENT_ERRORS_SUMMARY_BY_USER` information_schema table.
---

# CLIENT_ERRORS_SUMMARY_BY_USER {#client-errors-summary-by-user}

表`CLIENT_ERRORS_SUMMARY_BY_USER`は、TiDBサーバーに接続するクライアントに返されたSQLエラーと警告の要約を示しています。これらには以下が含まれます：

-   不正な形式のSQLステートメント。
-   ゼロ除算。
-   範囲外または重複するキー値を挿入しようとしました。
-   権限エラー。
-   存在しないテーブル。

クライアントエラーは、MySQLサーバープロトコルを介してクライアントに返されます。このプロトコルでは、アプリケーションが適切なアクションを実行することが期待されます。 `information_schema` 。 `CLIENT_ERRORS_SUMMARY_BY_USER`表は、アプリケーションがTiDBサーバーから返されたエラーを正しく処理（またはログ記録）していないシナリオでエラーを検査するための便利な方法を提供します。

`CLIENT_ERRORS_SUMMARY_BY_USER`はユーザーごとにエラーを要約するため、1つのユーザーサーバーが他のサーバーよりも多くのエラーを生成しているシナリオを診断するのに役立ちます。考えられるシナリオは次のとおりです。

-   権限エラー。
-   欠落しているテーブル、またはリレーショナルオブジェクト。
-   正しくないSQL構文、またはアプリケーションとTiDBのバージョン間の非互換性。

要約されたカウントは、ステートメント`FLUSH CLIENT_ERRORS_SUMMARY`でリセットできます。要約は各TiDBサーバーに対してローカルであり、メモリにのみ保持されます。 TiDBサーバーを再起動すると、要約は失われます。

{{< copyable "" >}}

```sql
USE information_schema;
DESC CLIENT_ERRORS_SUMMARY_BY_USER;
```

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

フィールドの説明：

-   `USER` ：認証されたユーザー。
-   `ERROR_NUMBER` ：返されたMySQL互換のエラー番号。
-   `ERROR_MESSAGE` ：エラー番号と一致するエラーメッセージ（プリペアドステートメント形式）。
-   `ERROR_COUNT` ：このエラーがユーザーに返された回数。
-   `WARNING_COUNT` ：この警告がユーザーに返された回数。
-   `FIRST_SEEN` ：このエラー（または警告）がユーザーに初めて送信されたとき。
-   `LAST_SEEN` ：このエラー（または警告）がユーザーに送信された最新の時刻。

次の例は、クライアントがローカルTiDBサーバーに接続したときに生成される警告を示しています。要約は`FLUSH CLIENT_ERRORS_SUMMARY`を実行した後にリセットされます：

{{< copyable "" >}}

```sql
SELECT 0/0;
SELECT * FROM CLIENT_ERRORS_SUMMARY_BY_USER;
FLUSH CLIENT_ERRORS_SUMMARY;
SELECT * FROM CLIENT_ERRORS_SUMMARY_BY_USER;
```

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
