---
title: CLIENT_ERRORS_SUMMARY_GLOBAL
summary: Learn about the `CLIENT_ERRORS_SUMMARY_GLOBAL` information_schema table.
---

# CLIENT_ERRORS_SUMMARY_GLOBAL {#client-errors-summary-global}

表`CLIENT_ERRORS_SUMMARY_GLOBAL`は、TiDBサーバーに接続するクライアントに返されたすべてのSQLエラーと警告のグローバルな要約を示しています。これらには以下が含まれます：

-   不正な形式のSQLステートメント。
-   ゼロ除算エラー。
-   範囲外の重複キー値を挿入しようとしました。
-   許可エラー。
-   テーブルが存在しません。

クライアントエラーは、MySQLサーバープロトコルを介してクライアントに返されます。このプロトコルでは、アプリケーションが適切なアクションを実行することが期待されます。 `information_schema` 。 `CLIENT_ERRORS_SUMMARY_GLOBAL`表は、概要を示しており、アプリケーションがTiDBサーバーから返されたエラーを正しく処理（またはログ記録）していないシナリオで役立ちます。

要約されたカウントは、ステートメント`FLUSH CLIENT_ERRORS_SUMMARY`でリセットできます。要約は各TiDBサーバーに対してローカルであり、メモリにのみ保持されます。 TiDBサーバーが再起動すると、要約は失われます。

{{< copyable "" >}}

```sql
USE information_schema;
DESC CLIENT_ERRORS_SUMMARY_GLOBAL;
```

```sql
+---------------+---------------+------+------+---------+-------+
| Field         | Type          | Null | Key  | Default | Extra |
+---------------+---------------+------+------+---------+-------+
| ERROR_NUMBER  | bigint(64)    | NO   |      | NULL    |       |
| ERROR_MESSAGE | varchar(1024) | NO   |      | NULL    |       |
| ERROR_COUNT   | bigint(64)    | NO   |      | NULL    |       |
| WARNING_COUNT | bigint(64)    | NO   |      | NULL    |       |
| FIRST_SEEN    | timestamp     | YES  |      | NULL    |       |
| LAST_SEEN     | timestamp     | YES  |      | NULL    |       |
+---------------+---------------+------+------+---------+-------+
6 rows in set (0.00 sec)
```

フィールドの説明：

-   `ERROR_NUMBER` ：返されたMySQL互換のエラー番号。
-   `ERROR_MESSAGE` ：エラー番号と一致するエラーメッセージ（プリペアドステートメント形式）。
-   `ERROR_COUNT` ：このエラーが返された回数。
-   `WARNING_COUNT` ：この警告が返された回数。
-   `FIRST_SEEN` ：このエラー（または警告）が初めて送信されたとき。
-   `LAST_SEEN` ：このエラー（または警告）が送信された最新の時刻。

次の例は、ローカルTiDBサーバーに接続するときに生成される警告を示しています。要約は`FLUSH CLIENT_ERRORS_SUMMARY`を実行した後にリセットされます：

{{< copyable "" >}}

```sql
SELECT 0/0;
SELECT * FROM CLIENT_ERRORS_SUMMARY_GLOBAL;
FLUSH CLIENT_ERRORS_SUMMARY;
SELECT * FROM CLIENT_ERRORS_SUMMARY_GLOBAL;
```

```sql
+-----+
| 0/0 |
+-----+
| NULL |
+-----+
1 row in set, 1 warning (0.00 sec)

+--------------+---------------+-------------+---------------+---------------------+---------------------+
| ERROR_NUMBER | ERROR_MESSAGE | ERROR_COUNT | WARNING_COUNT | FIRST_SEEN          | LAST_SEEN           |
+--------------+---------------+-------------+---------------+---------------------+---------------------+
|         1365 | Division by 0 |           0 |             1 | 2021-03-18 13:10:51 | 2021-03-18 13:10:51 |
+--------------+---------------+-------------+---------------+---------------------+---------------------+
1 row in set (0.00 sec)

Query OK, 0 rows affected (0.00 sec)

Empty set (0.00 sec)
```
