---
title: Information Functions
summary: Learn about the information functions.
---

# 情報機能 {#information-functions}

TiDB は、 MySQL 5.7で利用可能なほとんどの[<a href="https://dev.mysql.com/doc/refman/5.7/en/information-functions.html">情報関数</a>](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html)をサポートします。

## サポートされている関数 {#supported-functions}

| 名前                                                                                                                                                                                                                                   | 説明                                            |
| :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------- |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_benchmark">`BENCHMARK()`</a>](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_benchmark)                           | ループ内で式を実行する                                   |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_connection-id">`CONNECTION_ID()`</a>](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_connection-id)               | 接続の接続 ID (スレッド ID) を返します。                     |
| `CURRENT_RESOURCE_GROUP()`                                                                                                                                                                                                           | 現在のセッションがバインドされているリソース グループの名前を返します。          |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_current-user">`CURRENT_USER()` 、 `CURRENT_USER`</a>](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_current-user) | 認証されたユーザー名とホスト名を返します。                         |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_database">`DATABASE()`</a>](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_database)                              | デフォルト (現在の) データベース名を返します。                     |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_found-rows">`FOUND_ROWS()`</a>](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_found-rows)                        | `SELECT`に`LIMIT`句がある場合、 `LIMIT`句がない場合に返される行の数 |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_last-insert-id">`LAST_INSERT_ID()`</a>](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_last-insert-id)            | 最後の`INSERT`の列の`AUTOINCREMENT`列の値を返します。        |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_row-count">`ROW_COUNT()`</a>](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_row-count)                           | 影響を受ける行の数                                     |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_schema">`SCHEMA()`</a>](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_schema)                                    | `DATABASE()`の同義語                              |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_session-user">`SESSION_USER()`</a>](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_session-user)                  | `USER()`の同義語                                  |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_system-user">`SYSTEM_USER()`</a>](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_system-user)                     | `USER()`の同義語                                  |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_user">`USER()`</a>](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_user)                                          | クライアントから提供されたユーザー名とホスト名を返します。                 |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_version">`VERSION()`</a>](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_version)                                 | MySQLサーバーのバージョンを示す文字列を返します。                   |

## サポートされていない関数 {#unsupported-functions}

-   `CHARSET()`
-   `COERCIBILITY()`
-   `COLLATION()`
