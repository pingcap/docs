---
title: Locking Functions
summary: Learn about user-level locking functions in TiDB.
---

# ロック機能 {#locking-functions}

TiDB は、 MySQL 5.7で利用可能なユーザーレベル[ロック関数](https://dev.mysql.com/doc/refman/5.7/en/locking-functions.html)のほとんどをサポートします。

## サポートされている関数 {#supported-functions}

| 名前                                                                                                                 | 説明                                                                                       |
| :----------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------- |
| [`GET_LOCK(lockName, timeout)`](https://dev.mysql.com/doc/refman/8.0/en/locking-functions.html#function_get-lock)  | アドバイザリーロックを取得します。 `lockName`パラメータは 64 文字以内である必要があります。タイムアウトになるまで最大`timeout`秒待機し、失敗を返します。 |
| [`IS_FREE_LOCK(lockName)`](https://dev.mysql.com/doc/refman/8.0/en/locking-functions.html#function_is-free-lock)   | ロックが空いているかどうかを確認します。                                                                     |
| [`IS_USED_LOCK(lockName)`](https://dev.mysql.com/doc/refman/8.0/en/locking-functions.html#function_is-used-lock)   | ロックが使用されているかどうかを確認します。 true の場合、対応する接続​​ ID を返します。                                       |
| [`RELEASE_ALL_LOCKS()`](https://dev.mysql.com/doc/refman/8.0/en/locking-functions.html#function_release-all-locks) | 現在のセッションによって保持されているすべてのロックを解放します。                                                        |
| [`RELEASE_LOCK(lockName)`](https://dev.mysql.com/doc/refman/8.0/en/locking-functions.html#function_release-lock)   | 以前に取得したロックを解放します。 `lockName`パラメータは 64 文字以内である必要があります。                                    |

## MySQLの互換性 {#mysql-compatibility}

-   TiDB で許可される最小タイムアウトは 1 秒、最大タイムアウトは 1 時間 (3600 秒) です。これは、0 秒と無制限のタイムアウト ( `timeout=-1` ) の両方が許可される MySQL とは異なります。 TiDB は範囲外の値を最も近い許可値に自動的に変換し、 `timeout=-1`秒を 3600 秒に変換します。
-   TiDB は、ユーザーレベルのロックによって引き起こされるデッドロックを自動的に検出しません。デッドロックされたセッションは最大 1 時間後にタイムアウトしますが、影響を受けるセッションの 1 つで`KILL`を使用して手動で解決することもできます。ユーザーレベルのロックを常に同じ順序で取得することで、デッドロックを防ぐこともできます。
-   ロックはクラスター内のすべての TiDB サーバーで有効になります。これは、ロックが単一サーバーに対してローカルである MySQL クラスタやグループ レプリケーションとは異なります。
-   別のセッションから呼び出され、ロックを保持しているプロセスの ID を返せない場合、 `IS_USED_LOCK()` `1`を返します。
