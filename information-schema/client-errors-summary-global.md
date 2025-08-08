---
title: CLIENT_ERRORS_SUMMARY_GLOBAL
summary: CLIENT_ERRORS_SUMMARY_GLOBAL` INFORMATION_SCHEMA テーブルについて学習します。
---

# クライアントエラー概要グローバル {#client-errors-summary-global}

表`CLIENT_ERRORS_SUMMARY_GLOBAL` 、TiDBサーバーに接続したクライアントに返されたすべてのSQLエラーと警告のグローバルサマリーを示しています。これには以下が含まれます。

-   不正な SQL ステートメント。
-   ゼロ除算エラー。
-   範囲外の重複キー値を挿入しようとしました。
-   権限エラー。
-   テーブルが存在しません。

クライアントエラーはMySQLサーバープロトコルを介してクライアントに返され、アプリケーションは適切なアクションを実行することが期待されます。表`INFORMATION_SCHEMA.CLIENT_ERRORS_SUMMARY_GLOBAL`は概要を示しており、アプリケーションがTiDBサーバーから返されたエラーを適切に処理（またはログに記録）していないシナリオで役立ちます。

集計されたカウントは、ステートメント`FLUSH CLIENT_ERRORS_SUMMARY`でリセットできます。集計は各 TiDBサーバーにローカルであり、メモリ内にのみ保持されます。TiDBサーバーが再起動すると、集計は失われます。

```sql
USE INFORMATION_SCHEMA;
DESC CLIENT_ERRORS_SUMMARY_GLOBAL;
```

出力は次のようになります。

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

-   `ERROR_NUMBER` : 返された MySQL 互換エラー番号。
-   `ERROR_MESSAGE` : エラー番号に一致するエラー メッセージ (プリペアドステートメント形式)。
-   `ERROR_COUNT` : このエラーが返された回数。
-   `WARNING_COUNT` : この警告が返された回数。
-   `FIRST_SEEN` : このエラー (または警告) が最初に送信されたとき。
-   `LAST_SEEN` : このエラー (または警告) が最後に送信された時刻。

以下の例は、ローカルTiDBサーバーへの接続時に生成される警告を示しています。1 `FLUSH CLIENT_ERRORS_SUMMARY`実行するとサマリーがリセットされます。

```sql
SELECT 0/0;
SELECT * FROM CLIENT_ERRORS_SUMMARY_GLOBAL;
FLUSH CLIENT_ERRORS_SUMMARY;
SELECT * FROM CLIENT_ERRORS_SUMMARY_GLOBAL;
```

出力は次のようになります。

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
