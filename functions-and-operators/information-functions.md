---
title: Information Functions
summary: Learn about the information functions.
---

# 情報機能 {#information-functions}

TiDB は、 MySQL 5.7で利用可能な[情報関数](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html)のほとんどをサポートしています。

## 対応関数 {#supported-functions}

| 名前                                                                                                                                       | 説明                                         |
| :--------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------- |
| [`BENCHMARK()`](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_benchmark)                                   | ループで式を実行する                                 |
| [`CONNECTION_ID()`](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_connection-id)                           | 接続の接続 ID (スレッド ID) を返す                     |
| [`CURRENT_USER()` 、 <code>CURRENT_USER</code>](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_current-user) | 認証されたユーザー名とホスト名を返す                         |
| [`DATABASE()`](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_database)                                     | デフォルト (現在の) データベース名を返す                     |
| [`FOUND_ROWS()`](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_found-rows)                                 | `SELECT`と`LIMIT`句の場合、 `LIMIT`句がない場合に返される行数 |
| [`LAST_INSERT_ID()`](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_last-insert-id)                         | 最後の`INSERT`の`AUTOINCREMENT`列の値を返します        |
| [`ROW_COUNT()`](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_row-count)                                   | 影響を受けた行数                                   |
| [`SCHEMA()`](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_schema)                                         | `DATABASE()`の同義語                           |
| [`SESSION_USER()`](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_session-user)                             | `USER()`の同義語                               |
| [`SYSTEM_USER()`](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_system-user)                               | `USER()`の同義語                               |
| [`USER()`](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_user)                                             | クライアントから提供されたユーザー名とホスト名を返す                 |
| [`VERSION()`](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_version)                                       | MySQLサーバーのバージョンを示す文字列を返します                 |

## サポートされていない関数 {#unsupported-functions}

-   `CHARSET()`
-   `COERCIBILITY()`
-   `COLLATION()`
