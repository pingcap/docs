---
title: Miscellaneous Functions
summary: Learn about miscellaneous functions in TiDB.
---

# その他の機能 {#miscellaneous-functions}

TiDB は、 MySQL 5.7で利用可能な[その他の関数](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html)のほとんどをサポートしています。

## 対応関数 {#supported-functions}

| 名前                                                                                                                 | 説明                                     |
| :----------------------------------------------------------------------------------------------------------------- | :------------------------------------- |
| [`ANY_VALUE()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_any-value)           | `ONLY_FULL_GROUP_BY`値の拒否を抑制            |
| [`BIN_TO_UUID()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_bin-to-uuid)       | UUID をバイナリ形式からテキスト形式に変換する              |
| [`DEFAULT()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_default)               | テーブル列のデフォルト値を返します                      |
| [`INET_ATON()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_inet-aton)           | IP アドレスの数値を返す                          |
| [`INET_NTOA()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_inet-ntoa)           | 数値から IP アドレスを返す                        |
| [`INET6_ATON()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_inet6-aton)         | IPv6 アドレスの数値を返す                        |
| [`INET6_NTOA()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_inet6-ntoa)         | 数値からIPv6アドレスを返す                        |
| [`IS_IPV4()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_is-ipv4)               | 引数が IPv4 アドレスかどうか                      |
| [`IS_IPV4_COMPAT()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_is-ipv4-compat) | 引数が IPv4 互換アドレスかどうか                    |
| [`IS_IPV4_MAPPED()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_is-ipv4-mapped) | 引数が IPv4 マップ アドレスかどうか                  |
| [`IS_IPV6()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_is-ipv6)               | 引数が IPv6 アドレスかどうか                      |
| [`NAME_CONST()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_name-const)         | 列名の名前変更に使用できます                         |
| [`SLEEP()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_sleep)                   | 数秒間スリープする                              |
| [`UUID()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_uuid)                     | Universal Unique Identifier (UUID) を返す |
| [`UUID_TO_BIN()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_uuid-to-bin)       | UUID をテキスト形式からバイナリ形式に変換する              |
| [`VALUES()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_values)                 | INSERT 中に使用される値を定義します                  |

## サポートされていない関数 {#unsupported-functions}

| 名前                                                                                                                   | 説明                                                                                              |
| :------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------- |
| [`UUID_SHORT()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_uuid-short)           | TiDB [TiDB #4620](https://github.com/pingcap/tidb/issues/4620)に存在しない特定の仮定を考慮して、一意の UUID を提供します。 |
| [`MASTER_WAIT_POS()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_master-pos-wait) | MySQL レプリケーションに関連                                                                               |
