---
title: Information Functions
summary: Learn about the information functions.
---

# 情報機能 {#information-functions}

TiDB は、 MySQL 5.7で利用可能なほとんどの[情報関数](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html)をサポートします。

## TiDB がサポートする MySQL関数 {#tidb-supported-mysql-functions}

| 名前                                                                                                                            | 説明                                            |
| :---------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------- |
| [`BENCHMARK()`](https://dev.mysql.com/doc/refman/8.0/en/information-functions.html#function_benchmark)                        | ループ内で式を実行する                                   |
| [`CONNECTION_ID()`](https://dev.mysql.com/doc/refman/8.0/en/information-functions.html#function_connection-id)                | 接続の接続 ID (スレッド ID) を返します。                     |
| [`CURRENT_USER()` 、 `CURRENT_USER`](https://dev.mysql.com/doc/refman/8.0/en/information-functions.html#function_current-user) | 認証されたユーザー名とホスト名を返します。                         |
| [`DATABASE()`](https://dev.mysql.com/doc/refman/8.0/en/information-functions.html#function_database)                          | デフォルト (現在の) データベース名を返します。                     |
| [`FOUND_ROWS()`](https://dev.mysql.com/doc/refman/8.0/en/information-functions.html#function_found-rows)                      | `SELECT`に`LIMIT`句がある場合、 `LIMIT`句がない場合に返される行の数 |
| [`LAST_INSERT_ID()`](https://dev.mysql.com/doc/refman/8.0/en/information-functions.html#function_last-insert-id)              | 最後の`INSERT`の列の`AUTOINCREMENT`列の値を返します。        |
| [`ROW_COUNT()`](https://dev.mysql.com/doc/refman/8.0/en/information-functions.html#function_row-count)                        | 影響を受ける行の数                                     |
| [`SCHEMA()`](https://dev.mysql.com/doc/refman/8.0/en/information-functions.html#function_schema)                              | `DATABASE()`の同義語                              |
| [`SESSION_USER()`](https://dev.mysql.com/doc/refman/8.0/en/information-functions.html#function_session-user)                  | `USER()`の同義語                                  |
| [`SYSTEM_USER()`](https://dev.mysql.com/doc/refman/8.0/en/information-functions.html#function_system-user)                    | `USER()`の同義語                                  |
| [`USER()`](https://dev.mysql.com/doc/refman/8.0/en/information-functions.html#function_user)                                  | クライアントから提供されたユーザー名とホスト名を返します。                 |
| [`VERSION()`](https://dev.mysql.com/doc/refman/8.0/en/information-functions.html#function_version)                            | MySQLサーバーのバージョンを示す文字列を返します。                   |

## TiDB 固有の関数 {#tidb-specific-functions}

次の関数は TiDB でのみサポートされており、MySQL には同等の関数はありません。

| 名前                                                                                              | 説明                                   |
| :---------------------------------------------------------------------------------------------- | :----------------------------------- |
| [`CURRENT_RESOURCE_GROUP()`](/functions-and-operators/tidb-functions.md#current_resource_group) | 現在のセッションがバインドされているリソース グループの名前を返します。 |

## サポートされていない関数 {#unsupported-functions}

-   `CHARSET()`
-   `COERCIBILITY()`
-   `COLLATION()`
