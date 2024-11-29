---
title: CLIENT_ERRORS_SUMMARY_BY_HOST
summary: CLIENT_ERRORS_SUMMARY_BY_HOST` INFORMATION_SCHEMA テーブルについて学習します。
---

# ホスト別のクライアントエラー要約 {#client-errors-summary-by-host}

表`CLIENT_ERRORS_SUMMARY_BY_HOST`は、TiDBサーバーに接続するクライアントに返された SQL エラーと警告の概要を示しています。これには次のものが含まれます。

-   不正な SQL ステートメント。
-   ゼロ除算エラー。
-   範囲外または重複したキー値を挿入しようとしました。
-   権限エラー。
-   存在しないテーブル。

これらのエラーは MySQLサーバープロトコルを介してクライアントに返され、アプリケーションは適切なアクションを実行することが期待されます。1 `INFORMATION_SCHEMA.CLIENT_ERRORS_SUMMARY_BY_HOST`表は、アプリケーションが TiDBサーバーから返されたエラーを正しく処理 (またはログに記録) していないシナリオでエラーを検査するための便利な方法を提供します。

`CLIENT_ERRORS_SUMMARY_BY_HOST`リモート ホストごとにエラーを要約するため、1 つのアプリケーションサーバーが他のサーバーよりも多くのエラーを生成しているシナリオを診断するのに役立ちます。考えられるシナリオは次のとおりです。

-   時代遅れの MySQL クライアント ライブラリ。
-   古いアプリケーション (新しいデプロイメントを展開するときにこのサーバーが見逃された可能性があります)。
-   ユーザー権限の「ホスト」部分の使用方法が間違っています。
-   信頼性の低いネットワーク接続により、タイムアウトや接続切断がさらに発生します。

要約されたカウントは、ステートメント`FLUSH CLIENT_ERRORS_SUMMARY`を使用してリセットできます。要約は各 TiDBサーバーにローカルであり、メモリ内にのみ保持されます。要約は、TiDBサーバーを再起動すると失われます。

```sql
USE INFORMATION_SCHEMA;
DESC CLIENT_ERRORS_SUMMARY_BY_HOST;
```

出力は次のようになります。

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

-   `HOST` : クライアントのリモート ホスト。
-   `ERROR_NUMBER` : 返された MySQL 互換エラー番号。
-   `ERROR_MESSAGE` : エラー番号と一致するエラー メッセージ (プリペアドステートメント形式)。
-   `ERROR_COUNT` : このエラーがクライアント ホストに返された回数。
-   `WARNING_COUNT` : この警告がクライアント ホストに返された回数。
-   `FIRST_SEEN` : このエラー (または警告) がクライアント ホストから初めて確認されました。
-   `LAST_SEEN` : このエラー (または警告) がクライアント ホストから最後に確認された時刻。

次の例は、クライアントがローカル TiDBサーバーに接続したときに生成される警告を示しています。 `FLUSH CLIENT_ERRORS_SUMMARY`実行すると、サマリーがリセットされます。

```sql
SELECT 0/0;
SELECT * FROM CLIENT_ERRORS_SUMMARY_BY_HOST;
FLUSH CLIENT_ERRORS_SUMMARY;
SELECT * FROM CLIENT_ERRORS_SUMMARY_BY_HOST;
```

出力は次のようになります。

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
