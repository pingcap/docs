---
title: Timeouts in TiDB
summary: TiDB のタイムアウトとエラーのトラブルシューティングの解決策について学習します。
---

# TiDBのタイムアウト {#timeouts-in-tidb}

このドキュメントでは、エラーのトラブルシューティングに役立つ TiDB のさまざまなタイムアウトについて説明します。

## GCタイムアウト {#gc-timeout}

TiDBのトランザクション実装では、MVCC（Multiple Version Concurrency Control）メカニズムが採用されています。新しく書き込まれたデータが古いデータを上書きする場合、古いデータは置き換えられず、新しく書き込まれたデータと一緒に保持されます。バージョンはタイムスタンプによって区別されます。TiDBは、定期的なガベージコレクション（GC）メカニズムを使用して、不要になった古いデータをクリーンアップします。

-   TiDB バージョン v4.0 より前のバージョンの場合:

    デフォルトでは、各MVCCバージョン（整合性スナップショット）は10分間保持されます。読み取りに10分以上かかるトランザクションにはエラー`GC life time is shorter than transaction duration`が返されます。

-   TiDB v4.0 以降のバージョンの場合:

    24時間を超えない実行中のトランザクションの場合、トランザクション実行中はガベージコレクション（GC）がブロックされます。エラー`GC life time is shorter than transaction duration`は発生しません。

一時的に読み取り時間を長くする必要がある場合は、MVCC バージョンの保持時間を長くすることができます。

-   v5.0 より前の TiDB バージョンの場合: TiDB の`mysql.tidb`テーブルの`tikv_gc_life_time`調整します。
-   TiDB v5.0 以降のバージョンの場合: システム変数[`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50)調整します。

システム変数の設定は、グローバルかつ即座に反映されます。値を増やすと、既存のすべてのスナップショットの有効期間が延長され、値を減らすと、すべてのスナップショットの有効期間が即座に短縮されます。MVCCのバージョンが多すぎると、TiDBクラスタのパフォーマンスに影響します。そのため、この変数は適切なタイミングで以前の設定に戻す必要があります。

<CustomContent platform="tidb">

> **ヒント：**
>
> 具体的には、 Dumplingが TiDB (1 TB 未満) からデータをエクスポートする際に、TiDB のバージョンが v4.0.0 以降であり、 Dumpling がTiDB クラスターの PD アドレスと[`INFORMATION_SCHEMA.CLUSTER_INFO`](/information-schema/information-schema-cluster-info.md)テーブルにアクセスできる場合、 Dumpling は自動的に GC セーフ ポイントを調整し、元のクラスターに影響を与えずに GC をブロックします。
>
> ただし、次のいずれかのシナリオでは、 Dumpling はGC 時間を自動的に調整できません。
>
> -   データサイズが非常に大きい（1TB以上）。
> -   Dumpling はPD に直接接続できません。たとえば、 TiDB クラスターはTiDB Cloud上、またはDumplingとは分離された Kubernetes 上にあります。
>
> このようなシナリオでは、エクスポート プロセス中の GC によるエクスポートの失敗を回避するために、事前に GC 時間を手動で延長する必要があります。
>
> 詳細は[TiDB GC時間を手動で設定する](/dumpling-overview.md#manually-set-the-tidb-gc-time)参照。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **ヒント：**
>
> 具体的には、 Dumplingが TiDB (1 TB 未満) からデータをエクスポートするときに、TiDB のバージョンが v4.0.0 以上であり、 Dumpling がTiDB クラスターの PD アドレスにアクセスできる場合、 Dumpling は元のクラスターに影響を与えずに GC 時間を自動的に延長します。
>
> ただし、次のいずれかのシナリオでは、 Dumpling はGC 時間を自動的に調整できません。
>
> -   データサイズが非常に大きい（1TB以上）。
> -   Dumpling はPD に直接接続できません。たとえば、 TiDB クラスターはTiDB Cloud上、またはDumplingとは分離された Kubernetes 上にあります。
>
> このようなシナリオでは、エクスポート プロセス中の GC によるエクスポートの失敗を回避するために、事前に GC 時間を手動で延長する必要があります。
>
> 詳細は[TiDB GC時間を手動で設定する](https://docs.pingcap.com/tidb/stable/dumpling-overview#manually-set-the-tidb-gc-time)参照。

</CustomContent>

GC の詳細については、 [GCの概要](/garbage-collection-overview.md)参照してください。

## トランザクションタイムアウト {#transaction-timeout}

トランザクションが開始されたものの、コミットもロールバックもされないシナリオでは、ロックの長時間保持を防ぐために、よりきめ細かな制御と短いタイムアウトが必要になる場合があります。このような場合は、 [`tidb_idle_transaction_timeout`](/system-variables.md#tidb_idle_transaction_timeout-new-in-v760) （TiDB v7.6.0で導入）を使用して、ユーザーセッション内のトランザクションのアイドルタイムアウトを制御できます。

GCは実行中のトランザクションには影響しません。ただし、実行可能な悲観的トランザクションの数には上限があり、トランザクションのタイムアウトとトランザクションで使用されるメモリにも制限があります。トランザクションタイムアウトは、TiDBプロファイルのカテゴリ`[performance]`で`max-txn-ttl`ずつ変更できます。デフォルトでは`60`分です。

`INSERT INTO t10 SELECT * FROM t1`ような SQL 文は GC の影響を受けませんが、 `max-txn-ttl`超えるとタイムアウトによりロールバックされます。

## SQL実行タイムアウト {#sql-execution-timeout}

TiDB `max_execution_time`は、単一のSQL文の実行時間を制限するシステム変数（デフォルトでは`max_execution_time` 、 `0` 、制限なしを意味します）も用意されています。現在、このシステム変数は読み取り専用SQL文にのみ適用されます。5の単位は`ms`ですが、実際の精度はミリ秒単位ではなく`100ms`単位です。

## JDBCクエリタイムアウト {#jdbc-query-timeout}

<CustomContent platform="tidb">

v6.1.0 以降、 [`enable-global-kill`](/tidb-configuration-file.md#enable-global-kill-new-in-v610)構成項目がデフォルト値`true`に設定されている場合、MySQL JDBC によって提供される`setQueryTimeout()`メソッドを使用してクエリ タイムアウトを制御できます。

> **注記：**
>
> TiDBのバージョンがv6.1.0より前の場合、または[`enable-global-kill`](/tidb-configuration-file.md#enable-global-kill-new-in-v610) `false`に設定されている場合、 `setQueryTimeout()` TiDBでは機能しません。これは、クライアントがクエリタイムアウトを検出すると、データベースに`KILL`コマンドを送信するためです。ただし、TiDBサービスは負荷分散されているため、間違ったTiDBノードで接続が切断されるのを防ぐため、 `KILL`コマンドは実行されません。このような場合は、 `max_execution_time`使用してクエリタイムアウトを制御できます。

</CustomContent>

<CustomContent platform="tidb-cloud">

v6.1.0 以降、 [`enable-global-kill`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file/#enable-global-kill-new-in-v610)構成項目がデフォルト値`true`に設定されている場合、MySQL JDBC によって提供される`setQueryTimeout()`メソッドを使用してクエリ タイムアウトを制御できます。

> **注記：**
>
> TiDBのバージョンがv6.1.0より前の場合、または[`enable-global-kill`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file/#enable-global-kill-new-in-v610) `false`に設定されている場合、 `setQueryTimeout()` TiDBでは機能しません。これは、クライアントがクエリタイムアウトを検出すると、データベースに`KILL`コマンドを送信するためです。ただし、TiDBサービスは負荷分散されているため、間違ったTiDBノードで接続が切断されるのを防ぐため、 `KILL`コマンドは実行されません。このような場合は、 `max_execution_time`使用してクエリタイムアウトを制御できます。

</CustomContent>

TiDB は、次の MySQL 互換のタイムアウト制御パラメータを提供します。

-   **wait_timeout は**、 Javaアプリケーションへの接続における非対話型アイドルタイムアウトを制御します。TiDB v5.4以降では、デフォルト値は`wait_timeout`で、これは`28800`秒（8時間）です。TiDB v5.4より前のバージョンでは、デフォルト値は`0`で、これはタイムアウトが無制限であることを意味します。
-   **interactive_timeout は**、 Javaアプリケーションへの接続における対話型アイドルタイムアウトを制御します。デフォルトの値は`8 hours`です。
-   **max_execution_time は**、接続におけるSQL実行のタイムアウトを制御します。これは読み取り専用SQL文にのみ有効です。デフォルトの値は`0`で、接続が無限にビジー状態になることを許可します。つまり、SQL文は無限に長い時間実行されます。

しかし、実際の本番環境では、アイドル接続とSQL文の無期限実行は、データベースとアプリケーションの両方に悪影響を及ぼします。アプリケーションの接続文字列でこれらの2つのセッションレベル変数を設定することで、アイドル接続とSQL文の無期限実行を回避できます。例えば、次のように設定します。

-   `sessionVariables=wait_timeout=3600` （1時間）
-   `sessionVariables=max_execution_time=300000` （5分）

## ヘルプが必要ですか? {#need-help}

<CustomContent platform="tidb">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、あるいは[サポートチケットを送信する](/support.md)についてコミュニティに質問してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、あるいは[サポートチケットを送信する](https://tidb.support.pingcap.com/)についてコミュニティに質問してください。

</CustomContent>
