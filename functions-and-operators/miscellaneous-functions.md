---
title: Miscellaneous Functions
summary: Learn about miscellaneous functions in TiDB.
---

# その他の機能 {#miscellaneous-functions}

TiDBは、MySQL5.7で利用可能な[その他の関数](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html)のほとんどをサポートしMySQL 5.7。

## サポートされている関数 {#supported-functions}

| 名前                                                                                                                 | 説明                              |
| :----------------------------------------------------------------------------------------------------------------- | :------------------------------ |
| [`ANY_VALUE()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_any-value)           | `ONLY_FULL_GROUP_BY`の値の拒否を抑制します |
| [`BIN_TO_UUID()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_bin-to-uuid)       | UUIDをバイナリ形式からテキスト形式に変換する        |
| [`DEFAULT()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_default)               | テーブル列のデフォルト値を返します               |
| [`INET_ATON()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_inet-aton)           | IPアドレスの数値を返します                  |
| [`INET_NTOA()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_inet-ntoa)           | 数値からIPアドレスを返す                   |
| [`INET6_ATON()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_inet6-aton)         | IPv6アドレスの数値を返します                |
| [`INET6_NTOA()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_inet6-ntoa)         | 数値からIPv6アドレスを返す                 |
| [`IS_IPV4()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_is-ipv4)               | 引数がIPv4アドレスかどうか                 |
| [`IS_IPV4_COMPAT()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_is-ipv4-compat) | 引数がIPv4互換アドレスかどうか               |
| [`IS_IPV4_MAPPED()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_is-ipv4-mapped) | 引数がIPv4にマップされたアドレスかどうか          |
| [`IS_IPV6()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_is-ipv6)               | 引数がIPv6アドレスかどうか                 |
| [`NAME_CONST()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_name-const)         | 列名の名前を変更するために使用できます             |
| [`SLEEP()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_sleep)                   | 数秒間寝る                           |
| [`UUID()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_uuid)                     | ユニバーサル一意識別子（UUID）を返す            |
| [`UUID_TO_BIN()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_uuid-to-bin)       | UUIDをテキスト形式からバイナリ形式に変換する        |
| [`VALUES()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_values)                 | INSERT中に使用される値を定義します            |

## サポートされていない関数 {#unsupported-functions}

| 名前                                                                                                                   | 説明                                                                                        |
| :------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------- |
| [`GET_LOCK()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_get-lock)               | 名前付きロックを取得する[TiDB＃10929](https://github.com/pingcap/tidb/issues/14994)                    |
| [`RELEASE_LOCK()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_release-lock)       | 名前付きロックを解放します[TiDB＃10929](https://github.com/pingcap/tidb/issues/14994)                   |
| [`UUID_SHORT()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_uuid-short)           | TiDB1に存在しない特定の仮定を前提として一意のUUIDを提供し[TiDB＃4620](https://github.com/pingcap/tidb/issues/4620) |
| [`MASTER_WAIT_POS()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_master-pos-wait) | MySQLレプリケーションに関連します                                                                       |
