---
title: CLIENT_ERRORS_SUMMARY_BY_HOST
summary: Learn about the `CLIENT_ERRORS_SUMMARY_BY_HOST` information_schema table.
---

# CLIENT_ERRORS_SUMMARY_BY_HOST {#client-errors-summary-by-host}

表`CLIENT_ERRORS_SUMMARY_BY_HOST`は、TiDBサーバーに接続するクライアントに返されたSQLエラーと警告の要約を示しています。これらには以下が含まれます：

-   不正な形式のSQLステートメント。
-   ゼロ除算エラー。
-   範囲外または重複するキー値を挿入しようとしました。
-   許可エラー。
-   存在しないテーブル。

これらのエラーは、MySQLサーバープロトコルを介してクライアントに返されます。このプロトコルでは、アプリケーションが適切なアクションを実行することが期待されます。 `information_schema` 。 `CLIENT_ERRORS_SUMMARY_BY_HOST`表は、アプリケーションがTiDBサーバーから返されたエラーを正しく処理（またはログ記録）していないシナリオでエラーを検査するための便利な方法を提供します。

`CLIENT_ERRORS_SUMMARY_BY_HOST`はリモートホストごとにエラーを要約するため、1つのアプリケーションサーバーが他のサーバーよりも多くのエラーを生成しているシナリオを診断するのに役立ちます。考えられるシナリオは次のとおりです。

-   古いMySQLクライアントライブラリ。
-   古いアプリケーション（新しい展開を展開するときにこのサーバーが失われた可能性があります）。
-   ユーザー権限の「ホスト」部分の誤った使用。
-   より多くのタイムアウトまたは切断された接続を生成する信頼性の低いネットワーク接続。

要約されたカウントは、ステートメント`FLUSH CLIENT_ERRORS_SUMMARY`を使用してリセットできます。要約は各TiDBサーバーに対してローカルであり、メモリにのみ保持されます。 TiDBサーバーが再起動すると、要約は失われます。

{{< copyable "" >}}

```sql
USE information_schema;
DESC CLIENT_ERRORS_SUMMARY_BY_HOST;
```

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

フィールドの説明：

-   `HOST` ：クライアントのリモートホスト。
-   `ERROR_NUMBER` ：返されたMySQL互換のエラー番号。
-   `ERROR_MESSAGE` ：エラー番号と一致するエラーメッセージ（プリペアドステートメント形式）。
-   `ERROR_COUNT` ：このエラーがクライアントホストに返された回数。
-   `WARNING_COUNT` ：この警告がクライアントホストに返された回数。
-   `FIRST_SEEN` ：このエラー（または警告）がクライアントホストから初めて発生したとき。
-   `LAST_SEEN` ：このエラー（または警告）がクライアントホストから発生した最新の時刻。

次の例は、クライアントがローカルTiDBサーバーに接続したときに生成される警告を示しています。要約は`FLUSH CLIENT_ERRORS_SUMMARY`を実行した後にリセットされます：

{{< copyable "" >}}

```sql
SELECT 0/0;
SELECT * FROM CLIENT_ERRORS_SUMMARY_BY_HOST;
FLUSH CLIENT_ERRORS_SUMMARY;
SELECT * FROM CLIENT_ERRORS_SUMMARY_BY_HOST;
```

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
