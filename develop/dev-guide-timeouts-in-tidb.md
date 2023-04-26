---
title: Timeouts in TiDB
summary: Learn about timeouts in TiDB, and solutions for troubleshooting errors.
---

# TiDB のタイムアウト {#timeouts-in-tidb}

このドキュメントでは、エラーのトラブルシューティングに役立つように、TiDB のさまざまなタイムアウトについて説明します。

## GC タイムアウト {#gc-timeout}

TiDB のトランザクション実装は、MVCC (Multiple Version Concurrency Control) メカニズムを使用します。新しく書き込まれたデータが古いデータを上書きする場合、古いデータは置き換えられず、新しく書き込まれたデータと一緒に保持されます。バージョンはタイムスタンプによって区別されます。 TiDB は、定期的なガベージ コレクション (GC) のメカニズムを使用して、不要になった古いデータをクリーンアップします。

デフォルトでは、各 MVCC バージョン (整合性スナップショット) は 10 分間保持されます。読み取りに 10 分以上かかるトランザクションは、エラー`GC life time is shorter than transaction duration`を受け取ります。

たとえば、フル バックアップに**Mydumper を**使用している場合 ( <strong>Mydumper は</strong>一貫性のあるスナップショットをバックアップする場合)、より長い読み取り時間が必要な場合は、TiDB の`mysql.tidb`テーブルの値`tikv_gc_life_time`を調整して、MVCC バージョンの保持時間を長くすることができます。 `tikv_gc_life_time`グローバルかつ即時に有効になることに注意してください。値を大きくすると、既存のすべてのスナップショットの寿命が長くなり、値を小さくすると、すべてのスナップショットの寿命がすぐに短くなります。 MVCC のバージョンが多すぎると、TiKV の処理効率に影響します。そのため、 <strong>Mydumper</strong>で完全バックアップを行った後、 `tikv_gc_life_time`以前の設定に戻す必要があります。

GC の詳細については、 [GC の概要](/garbage-collection-overview.md)を参照してください。

## トランザクションのタイムアウト {#transaction-timeout}

GC は進行中のトランザクションには影響しません。ただし、実行できる悲観的トランザクションの数には上限があり、トランザクション タイムアウトの制限とトランザクションが使用するメモリの制限があります。トランザクション タイムアウトは、TiDB プロファイルの`[performance]`カテゴリで`max-txn-ttl`ずつ変更できます。デフォルトでは`60`分です。

`INSERT INTO t10 SELECT * FROM t1`などの SQL ステートメントは GC の影響を受けませんが、 `max-txn-ttl`超えるとタイムアウトによりロールバックされます。

## SQL 実行タイムアウト {#sql-execution-timeout}

TiDB は、単一の SQL ステートメントの実行時間を制限するためのシステム変数 (デフォルトでは`max_execution_time` 、 `0`で、制限がないことを示します) も提供します。 `max_execution_time`現在、 `SELECT`のステートメントだけでなく、すべてのタイプのステートメントに対して有効です。単位は`ms`ですが、実際の精度はミリ秒レベルではなく`100ms`レベルです。

## JDBC クエリのタイムアウト {#jdbc-query-timeout}

MySQL JDBC のクエリ タイムアウト設定の`setQueryTimeout()` TiDB では機能しませ***ん***。これは、クライアントがタイムアウトを検出すると、データベースに`KILL`コマンドを送信するためです。ただし、tidb-server は負荷分散されており、間違った tidb-server での接続の終了を避けるために、この`KILL`コマンドを実行しません。クエリのタイムアウト効果を確認するには、 `MAX_EXECUTION_TIME`を使用する必要があります。

TiDB は、次の MySQL 互換のタイムアウト制御パラメーターを提供します。

-   **wait_timeout**は、 Javaアプリケーションへの接続の非対話型アイドル タイムアウトを制御します。 TiDB v5.4 以降、デフォルト値の`wait_timeout`は`28800`秒、つまり 8 時間です。 v5.4 より前のバージョンの TiDB の場合、デフォルト値は`0`です。これは、タイムアウトが無制限であることを意味します。
-   **interactive_timeout**は、 Javaアプリケーションへの接続の対話型アイドル タイムアウトを制御します。デフォルトの値は`8 hours`です。
-   **max_execution_time**は、接続での SQL 実行のタイムアウトを制御します。デフォルトの値は`0`で、これにより接続は無限にビジー状態になります。つまり、SQL ステートメントは無限に長時間実行されます。

ただし、実際の本番環境では、アイドル状態の接続と無期限に実行される SQL ステートメントは、データベースとアプリケーションの両方に悪影響を及ぼします。アプリケーションの接続文字列でこれら 2 つのセッション レベルの変数を構成することにより、アイドル状態の接続と無期限に SQL ステートメントを実行することを回避できます。たとえば、次のように設定します。

-   `sessionVariables=wait_timeout=3600` (1時間)
-   `sessionVariables=max_execution_time=300000` (5 分)
