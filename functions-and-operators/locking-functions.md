---
title: Locking Functions
summary: Learn about user-level locking functions in TiDB.
---

# ロック機能 {#locking-functions}

TiDB は、 MySQL 5.7で利用可能なユーザーレベル[ロック関数](https://dev.mysql.com/doc/refman/5.7/en/locking-functions.html)のほとんどをサポートしています。

## 対応関数 {#supported-functions}

| 名前                                                                                                                 | 説明                                                                                     |
| :----------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------- |
| [`GET_LOCK(lockName, timeout)`](https://dev.mysql.com/doc/refman/5.7/en/locking-functions.html#function_get-lock)  | アドバイザリ ロックを取得します。 `lockName`パラメーターは 64 文字を超えてはなりません。タイムアウトするまで最大`timeout`秒待機し、失敗を返します。 |
| [`RELEASE_LOCK(lockName)`](https://dev.mysql.com/doc/refman/5.7/en/locking-functions.html#function_release-lock)   | 以前に取得したロックを解放します。 `lockName`パラメーターは 64 文字を超えてはなりません。                                   |
| [`RELEASE_ALL_LOCKS()`](https://dev.mysql.com/doc/refman/5.7/en/locking-functions.html#function_release-all-locks) | 現在のセッションが保持しているすべてのロックを解放します。                                                          |

## MySQL の互換性 {#mysql-compatibility}

-   TiDB で許可される最小タイムアウトは 1 秒で、最大タイムアウトは 1 時間 (3600 秒) です。これは、0 秒と無制限のタイムアウト ( `timeout=-1` ) の両方が許可されている MySQL とは異なります。 TiDB は、範囲外の値を最も近い許容値に自動的に変換し、 `timeout=-1`を 3600 秒に変換します。
-   TiDB は、ユーザーレベルのロックによって引き起こされたデッドロックを自動的に検出しません。デッドロックされたセッションは最大 1 時間後にタイムアウトしますが、影響を受けるセッションの 1 つで`KILL`を使用して手動で解決することもできます。ユーザーレベルのロックを常に同じ順序で取得することで、デッドロックを防ぐこともできます。
-   ロックは、クラスター内のすべての TiDB サーバーで有効になります。これは、ロックが単一のサーバーに対してローカルである MySQL クラスタおよびグループ レプリケーションとは異なります。

## サポートされていない関数 {#unsupported-functions}

-   `IS_FREE_LOCK()`
-   `IS_USED_LOCK()`
