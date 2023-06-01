---
title: Miscellaneous Functions
summary: Learn about miscellaneous functions in TiDB.
---

# その他の機能 {#miscellaneous-functions}

TiDB は、 MySQL 5.7で利用可能なほとんどの[<a href="https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html">さまざまな関数</a>](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html)をサポートします。

## サポートされている関数 {#supported-functions}

| 名前                                                                                                                                                                                                                            | 説明                                     |
| :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------- |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_any-value">`ANY_VALUE()`</a>](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_any-value)                | `ONLY_FULL_GROUP_BY`値拒否の抑制             |
| [<a href="https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_bin-to-uuid">`BIN_TO_UUID()`</a>](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_bin-to-uuid)          | UUIDをバイナリ形式からテキスト形式に変換します              |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_default">`DEFAULT()`</a>](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_default)                      | テーブル列のデフォルト値を返します。                     |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_inet-aton">`INET_ATON()`</a>](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_inet-aton)                | IPアドレスの数値を返します                         |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_inet-ntoa">`INET_NTOA()`</a>](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_inet-ntoa)                | IPアドレスを数値から返す                          |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_inet6-aton">`INET6_ATON()`</a>](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_inet6-aton)             | IPv6アドレスの数値を返します。                      |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_inet6-ntoa">`INET6_NTOA()`</a>](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_inet6-ntoa)             | IPv6アドレスを数値から返します。                     |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_is-ipv4">`IS_IPV4()`</a>](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_is-ipv4)                      | 引数がIPv4アドレスかどうか                        |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_is-ipv4-compat">`IS_IPV4_COMPAT()`</a>](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_is-ipv4-compat) | 引数がIPv4互換アドレスかどうか                      |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_is-ipv4-mapped">`IS_IPV4_MAPPED()`</a>](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_is-ipv4-mapped) | 引数がIPv4マップされたアドレスかどうか                  |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_is-ipv6">`IS_IPV6()`</a>](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_is-ipv6)                      | 引数がIPv6アドレスかどうか                        |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_name-const">`NAME_CONST()`</a>](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_name-const)             | 列名の変更に使用できます                           |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_sleep">`SLEEP()`</a>](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_sleep)                            | 数秒間スリープします                             |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_uuid">`UUID()`</a>](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_uuid)                               | Universal Unique Identifier (UUID) を返す |
| [<a href="https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_uuid-to-bin">`UUID_TO_BIN()`</a>](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_uuid-to-bin)          | UUIDをテキスト形式からバイナリ形式に変換します              |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_values">`VALUES()`</a>](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_values)                         | INSERT 中に使用される値を定義します。                 |

## サポートされていない関数 {#unsupported-functions}

| 名前                                                                                                                                                                                                                               | 説明                                                                                                                                                          |
| :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_uuid-short">`UUID_SHORT()`</a>](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_uuid-short)                | TiDB [<a href="https://github.com/pingcap/tidb/issues/4620">TiDB #4620</a>](https://github.com/pingcap/tidb/issues/4620)に存在しない特定の前提条件を考慮して、一意の UUID を提供します。 |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_master-pos-wait">`MASTER_WAIT_POS()`</a>](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_master-pos-wait) | MySQLレプリケーションに関連する                                                                                                                                          |
