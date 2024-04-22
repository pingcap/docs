---
title: CLIENT_ERRORS_SUMMARY_GLOBAL
summary: 表`CLIENT_ERRORS_SUMMARY_GLOBAL`は、TiDBサーバーに接続するクライアントに返されたSQLエラーと警告の概要を示します。エラーには不正なSQLステートメントやゼロ除算エラーなどが含まれます。クライアントエラーはMySQLサーバープロトコル経由で返され、アプリケーションは適切なアクションを実行することが期待されます。要約されたカウントは`FLUSH CLIENT_ERRORS_SUMMARY`でリセットできます。サマリーは各TiDBサーバーに対してローカルであり、メモリ内にのみ保持されます。 TiDBサーバーが再起動すると、サマリーは失われます。
---

# CLIENT_ERRORS_SUMMARY_GLOBAL {#client-errors-summary-global}

表`CLIENT_ERRORS_SUMMARY_GLOBAL`は、TiDBサーバーに接続するクライアントに返されたすべての SQL エラーと警告の全体的な概要を示しています。これらには次のものが含まれます。

-   不正な形式の SQL ステートメント。
-   ゼロ除算エラー。
-   範囲外の重複キー値を挿入しようとしました。
-   許可エラー。
-   テーブルが存在しません。

クライアント エラーは MySQLサーバープロトコル経由でクライアントに返され、アプリケーションは適切なアクションを実行することが期待されます。表`INFORMATION_SCHEMA.CLIENT_ERRORS_SUMMARY_GLOBAL`は高レベルの概要を示しており、アプリケーションが TiDBサーバーから返されたエラーを正しく処理 (またはログ記録) していないシナリオに役立ちます。

要約されたカウントはステートメント`FLUSH CLIENT_ERRORS_SUMMARY`でリセットできます。概要は各 TiDBサーバーに対してローカルであり、メモリ内にのみ保持されます。 TiDBサーバーが再起動すると、サマリーは失われます。

```sql
USE INFORMATION_SCHEMA;
DESC CLIENT_ERRORS_SUMMARY_GLOBAL;
```

出力は次のとおりです。

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

フィールドの説明:

-   `ERROR_NUMBER` : 返された MySQL 互換のエラー番号。
-   `ERROR_MESSAGE` : エラー番号と一致するエラー メッセージ (プリペアドステートメント形式)。
-   `ERROR_COUNT` : このエラーが返された回数。
-   `WARNING_COUNT` : この警告が返された回数。
-   `FIRST_SEEN` : このエラー (または警告) が初めて送信されたとき。
-   `LAST_SEEN` : このエラー (または警告) が最後に送信された時刻。

次の例は、ローカル TiDBサーバーに接続するときに生成される警告を示しています。 `FLUSH CLIENT_ERRORS_SUMMARY`を実行するとサマリーがリセットされます。

```sql
SELECT 0/0;
SELECT * FROM CLIENT_ERRORS_SUMMARY_GLOBAL;
FLUSH CLIENT_ERRORS_SUMMARY;
SELECT * FROM CLIENT_ERRORS_SUMMARY_GLOBAL;
```

出力は次のとおりです。

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
