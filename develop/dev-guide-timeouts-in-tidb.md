---
title: Timeouts in TiDB
summary: Learn about timeouts in TiDB, and solutions for troubleshooting errors.
---

# TiDBのタイムアウト {#timeouts-in-tidb}

このドキュメントでは、エラーのトラブルシューティングに役立つTiDBのさまざまなタイムアウトについて説明します。

## GCタイムアウト {#gc-timeout}

TiDBのトランザクション実装は、MVCC（Multiple Version Concurrency Control）メカニズムを使用します。新しく書き込まれたデータが古いデータを上書きする場合、古いデータは置き換えられませんが、新しく書き込まれたデータと一緒に保持されます。バージョンはタイムスタンプによって区別されます。 TiDBは、定期的なガベージコレクション（GC）のメカニズムを使用して、不要になった古いデータをクリーンアップします。

デフォルトでは、各MVCCバージョン（整合性スナップショット）は10分間保持されます。読み取りに10分以上かかるトランザクションは、エラー`GC life time is shorter than transaction duration`を受け取ります。

読み取り時間を長くする必要がある場合、たとえば、フルバックアップに**Mydumper**を使用している場合（ <strong>Mydumper</strong>は一貫性のあるスナップショットをバックアップします）、TiDBの`mysql.tidb`テーブルの`tikv_gc_life_time`の値を調整して、MVCCバージョンの保持時間を増やすことができます。 `tikv_gc_life_time`はグローバルかつ即座に有効になることに注意してください。値を大きくすると、既存のすべてのスナップショットの寿命が長くなり、値を小さくすると、すべてのスナップショットの寿命がすぐに短くなります。 MVCCのバージョンが多すぎると、TiKVの処理効率に影響します。したがって、 <strong>Mydumper</strong>を使用して完全バックアップを実行した後、 `tikv_gc_life_time`を以前の設定に戻す必要があります。

GCの詳細については、 [GCの概要](/garbage-collection-overview.md)を参照してください。

## トランザクションタイムアウト {#transaction-timeout}

GCは進行中のトランザクションには影響しません。ただし、実行できるペシミスティックトランザクションの数には上限があり、トランザクションタイムアウトの制限と、トランザクションで使用されるメモリの制限があります。 TiDBプロファイルの`[performance]`カテゴリでトランザクションタイムアウトを`max-txn-ttl`ずつ変更できます。デフォルトでは`60`分です。

`INSERT INTO t10 SELECT * FROM t1`などのSQLステートメントはGCの影響を受けませんが、 `max-txn-ttl`を超えた後のタイムアウトのためにロールバックされます。

## SQL実行タイムアウト {#sql-execution-timeout}

TiDBは、単一のSQLステートメントの実行時間を制限するためのシステム変数（デフォルトでは`max_execution_time` 、制限なしを示す）も提供し`0` 。 `max_execution_time`は現在、 `SELECT`のステートメントだけでなく、すべてのタイプのステートメントに対して有効です。単位は`ms`ですが、実際の精度はミリ秒レベルではなく`100ms`レベルです。

## JDBCクエリタイムアウト {#jdbc-query-timeout}

MySQL JDBCの`setQueryTimeout()`のクエリタイムアウト設定は、TiDBでは機能し***ません***。これは、クライアントがタイムアウトを検出すると、データベースに`KILL`コマンドを送信するためです。ただし、tidb-serverは負荷分散されており、間違ったtidb-serverでの接続の終了を回避するために、この`KILL`コマンドは実行されません。クエリタイムアウトの影響を確認するには、 `MAX_EXECUTION_TIME`を使用する必要があります。

TiDBは、次のMySQL互換のタイムアウト制御パラメーターを提供します。

-   **wait_timeout**は、Javaアプリケーションへの接続の非対話型アイドルタイムアウトを制御します。値はデフォルトで`0`であり、接続を無期限にアイドル状態にすることができます。
-   **Interactive_timeout**は、Javaアプリケーションへの接続のインタラクティブアイドルタイムアウトを制御します。デフォルト値は`8 hours`です。
-   **max_execution_time**は、接続でのSQL実行のタイムアウトを制御します。デフォルトの値は`0`です。これにより、接続が無限にビジーになります。つまり、SQLステートメントが無限に長時間実行されます。

ただし、実際の実稼働環境では、アイドル状態の接続と無期限に実行されるSQLステートメントは、データベースとアプリケーションの両方に悪影響を及ぼします。アプリケーションの接続文字列でこれらの2つのセッションレベル変数を構成することにより、アイドル状態の接続やSQLステートメントの無期限の実行を回避できます。たとえば、次のように設定します。

-   `sessionVariables=wait_timeout=3600` （1時間）
-   `sessionVariables=max_execution_time=300000` （5分）
