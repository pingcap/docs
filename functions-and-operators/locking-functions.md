---
title: Locking Functions
summary: Learn about user-level locking functions in TiDB.
---

# ロック機能 {#locking-functions}

TiDBは、MySQL5.7で利用可能なユーザーレベル[ロック機能](https://dev.mysql.com/doc/refman/5.7/en/locking-functions.html)のほとんどをサポートします。

## サポートされている機能 {#supported-functions}

| 名前                                                                                                                 | 説明                                                                                    |
| :----------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------ |
| [`GET_LOCK(lockName, timeout)`](https://dev.mysql.com/doc/refman/5.7/en/locking-functions.html#function_get-lock)  | アドバイザリーロックを取得します。 `lockName`パラメーターは64文字を超えてはなりません。タイムアウトする前に最大`timeout`秒間待機し、障害を返します。 |
| [`RELEASE_LOCK(lockName)`](https://dev.mysql.com/doc/refman/5.7/en/locking-functions.html#function_release-lock)   | 以前に取得したロックを解放します。 `lockName`パラメーターは64文字を超えてはなりません。                                    |
| [`RELEASE_ALL_LOCKS()`](https://dev.mysql.com/doc/refman/5.7/en/locking-functions.html#function_release-all-locks) | 現在のセッションによって保持されているすべてのロックを解放します。                                                     |

## MySQLの互換性 {#mysql-compatibility}

-   TiDBで許可されている最小タイムアウトは1秒で、最大タイムアウトは1時間（3600秒）です。これは、0秒と無制限のタイムアウト（ `timeout=-1` ）の両方が許可されているMySQLとは異なります。 TiDBは、範囲外の値を最も近い許可された値に自動的に変換し、 `timeout=-1`秒に変換します。
-   TiDBは、ユーザーレベルのロックによって引き起こされたデッドロックを自動的に検出しません。デッドロックされたセッションは、最大1時間後にタイムアウトしますが、影響を受けるセッションの1つで`KILL`を使用して手動で解決することもできます。また、常に同じ順序でユーザーレベルのロックを取得することにより、デッドロックを防ぐことができます。
-   ロックは、クラスタのすべてのTiDBサーバーで有効になります。これは、ロックが単一のサーバーに対してローカルであるMySQLクラスターおよびグループレプリケーションとは異なります。

## サポートされていない機能 {#unsupported-functions}

-   `IS_FREE_LOCK()`
-   `IS_USED_LOCK()`
