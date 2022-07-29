---
title: Information Functions
summary: Learn about the information functions.
---

# 情報機能 {#information-functions}

TiDBは、MySQL5.7で利用可能な[情報関数](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html)のほとんどをサポートしMySQL 5.7。

## サポートされている関数 {#supported-functions}

| 名前                                                                                                                                       | 説明                                            |
| :--------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------- |
| [`BENCHMARK()`](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_benchmark)                                   | ループで式を実行する                                    |
| [`CONNECTION_ID()`](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_connection-id)                           | 接続の接続ID（スレッドID）を返します                          |
| [`CURRENT_USER()` 、 <code>CURRENT_USER</code>](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_current-user) | 認証されたユーザー名とホスト名を返します                          |
| [`DATABASE()`](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_database)                                     | デフォルトの（現在の）データベース名を返します                       |
| [`FOUND_ROWS()`](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_found-rows)                                 | `SELECT`と`LIMIT`の句の場合、 `LIMIT`の句がない場合に返される行の数 |
| [`LAST_INSERT_ID()`](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_last-insert-id)                         | 最後の`INSERT`の`AUTOINCREMENT`列の値を返します           |
| [`ROW_COUNT()`](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_row-count)                                   | 影響を受ける行数                                      |
| [`SCHEMA()`](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_schema)                                         | `DATABASE()`の同義語                              |
| [`SESSION_USER()`](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_session-user)                             | `USER()`の同義語                                  |
| [`SYSTEM_USER()`](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_system-user)                               | `USER()`の同義語                                  |
| [`USER()`](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_user)                                             | クライアントから提供されたユーザー名とホスト名を返します                  |
| [`VERSION()`](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_version)                                       | MySQLサーバーのバージョンを示す文字列を返します                    |

## サポートされていない関数 {#unsupported-functions}

-   `CHARSET()`
-   `COERCIBILITY()`
-   `COLLATION()`
