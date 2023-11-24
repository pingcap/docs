---
title: Miscellaneous Functions
summary: Learn about miscellaneous functions in TiDB.
---

# その他の機能 {#miscellaneous-functions}

TiDB は、 MySQL 5.7で利用可能なほとんどの[さまざまな関数](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html)をサポートします。

## サポートされている関数 {#supported-functions}

| 名前                                                                                                                 | 説明                                                                                                                                                                   |
| :----------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`ANY_VALUE()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_any-value)           | `ONLY_FULL_GROUP_BY`値拒否の抑制                                                                                                                                           |
| [`BIN_TO_UUID()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_bin-to-uuid)       | UUIDをバイナリ形式からテキスト形式に変換します                                                                                                                                            |
| [`DEFAULT()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_default)               | テーブル列のデフォルト値を返します。                                                                                                                                                   |
| [`INET_ATON()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_inet-aton)           | IPアドレスの数値を返します                                                                                                                                                       |
| [`INET_NTOA()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_inet-ntoa)           | IPアドレスを数値から返す                                                                                                                                                        |
| [`INET6_ATON()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_inet6-aton)         | IPv6アドレスの数値を返します。                                                                                                                                                    |
| [`INET6_NTOA()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_inet6-ntoa)         | IPv6アドレスを数値から返します。                                                                                                                                                   |
| [`IS_IPV4()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_is-ipv4)               | 引数がIPv4アドレスかどうか                                                                                                                                                      |
| [`IS_IPV4_COMPAT()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_is-ipv4-compat) | 引数がIPv4互換アドレスかどうか                                                                                                                                                    |
| [`IS_IPV4_MAPPED()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_is-ipv4-mapped) | 引数がIPv4マップされたアドレスかどうか                                                                                                                                                |
| [`IS_IPV6()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_is-ipv6)               | 引数がIPv6アドレスかどうか                                                                                                                                                      |
| [`NAME_CONST()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_name-const)         | 列名の変更に使用できます                                                                                                                                                         |
| [`SLEEP()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_sleep)                   | 数秒間スリープします。 [TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)クラスターの場合、 `SLEEP()`関数には最大スリープ時間 300 秒しかサポートできないという制限があることに注意してください。 |
| [`UUID()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_uuid)                     | Universal Unique Identifier (UUID) を返す                                                                                                                               |
| [`UUID_TO_BIN()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_uuid-to-bin)       | UUIDをテキスト形式からバイナリ形式に変換します                                                                                                                                            |
| [`VALUES()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_values)                 | INSERT 中に使用される値を定義します。                                                                                                                                               |

## サポートされていない関数 {#unsupported-functions}

| 名前                                                                                                                   | 説明                                                                                                |
| :------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------ |
| [`UUID_SHORT()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_uuid-short)           | TiDB [TiDB #4620](https://github.com/pingcap/tidb/issues/4620)に存在しない特定の前提条件を考慮して、一意の UUID を提供します。 |
| [`MASTER_WAIT_POS()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_master-pos-wait) | MySQLレプリケーションに関連する                                                                                |
