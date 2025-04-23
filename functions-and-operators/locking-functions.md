---
title: Locking Functions
summary: TiDB のユーザー レベルのロック関数について学習します。
---

# ロック機能 {#locking-functions}

TiDB は、MySQL 8.0 で利用可能なユーザー レベル[ロック関数](https://dev.mysql.com/doc/refman/8.0/en/locking-functions.html)のほとんどをサポートしています。

## サポートされている関数 {#supported-functions}

| 名前                                                                                                                 | 説明                                                                                   |
| :----------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------- |
| [`GET_LOCK(lockName, timeout)`](https://dev.mysql.com/doc/refman/8.0/en/locking-functions.html#function_get-lock)  | アドバイザリロックを取得します。パラメータ`lockName`は64文字以内でなければなりません。タイムアウトするまで最大`timeout`秒間待機し、失敗を返します。 |
| [`IS_FREE_LOCK(lockName)`](https://dev.mysql.com/doc/refman/8.0/en/locking-functions.html#function_is-free-lock)   | ロックが空いているかどうかを確認します。                                                                 |
| [`IS_USED_LOCK(lockName)`](https://dev.mysql.com/doc/refman/8.0/en/locking-functions.html#function_is-used-lock)   | ロックが使用中かどうかを確認します。使用中の場合、対応する接続IDを返します。                                              |
| [`RELEASE_ALL_LOCKS()`](https://dev.mysql.com/doc/refman/8.0/en/locking-functions.html#function_release-all-locks) | 現在のセッションによって保持されているすべてのロックを解除します。                                                    |
| [`RELEASE_LOCK(lockName)`](https://dev.mysql.com/doc/refman/8.0/en/locking-functions.html#function_release-lock)   | 以前に取得したロックを解除します。1 `lockName`パラメータは64文字以内でなければなりません。                                 |

## MySQLの互換性 {#mysql-compatibility}

-   TiDB で許可される最小タイムアウトは 1 秒、最大タイムアウトは 1 時間 (3600 秒) です。これは、0 秒と無制限 ( `timeout=-1` ) の両方のタイムアウトが許可されている MySQL とは異なります。TiDB は範囲外の値を最も近い許容値に自動的に変換し、 `timeout=-1`は 3600 秒に変換されます。
-   TiDBは、ユーザーレベルロックによるデッドロックを自動的に検出しません。デッドロックが発生したセッションは最大1時間後にタイムアウトしますが、影響を受けたセッションのいずれかで[`KILL`](/sql-statements/sql-statement-kill.md)使用することで手動で解決することもできます。また、ユーザーレベルロックを常に同じ順序で取得することで、デッドロックを防ぐこともできます。
-   ロックはクラスタ内のすべてのTiDBサーバーで有効になります。これは、ロックが単一のサーバーにローカルであるMySQL クラスタやグループレプリケーションとは異なります。
-   `IS_USED_LOCK()` 、別のセッションから呼び出され、ロックを保持しているプロセスの ID を返すことができない場合は`1`返します。
