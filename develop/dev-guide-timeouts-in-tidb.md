---
title: Timeouts in TiDB
summary: TiDB のタイムアウトとエラーのトラブルシューティングの解決策について学習します。
---

# TiDB のタイムアウト {#timeouts-in-tidb}

このドキュメントでは、エラーのトラブルシューティングに役立つ TiDB のさまざまなタイムアウトについて説明します。

## GCタイムアウト {#gc-timeout}

TiDB のトランザクション実装では、MVCC (Multiple Version Concurrency Control) メカニズムが使用されます。新しく書き込まれたデータが古いデータを上書きする場合、古いデータは置き換えられず、新しく書き込まれたデータと一緒に保持されます。バージョンはタイムスタンプによって区別されます。TiDB は、定期的なガベージ コレクション (GC) のメカニズムを使用して、不要になった古いデータをクリーンアップします。

-   TiDB バージョン v4.0 より前のバージョンの場合:

    デフォルトでは、各 MVCC バージョン (一貫性スナップショット) は 10 分間保持されます。読み取りに 10 分以上かかるトランザクションにはエラー`GC life time is shorter than transaction duration`が返されます。

-   TiDB v4.0 以降のバージョンの場合:

    実行時間が 24 時間を超えないトランザクションの場合、トランザクションの実行中はガベージコレクション(GC) がブロックされます。エラー`GC life time is shorter than transaction duration`は発生しません。

一時的に読み取り時間を長くする必要がある場合は、MVCC バージョンの保持時間を長くすることができます。

-   v5.0 より前の TiDB バージョンの場合: TiDB の`mysql.tidb`のテーブルの`tikv_gc_life_time`を調整します。
-   TiDB v5.0 以降のバージョンの場合: システム変数[`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50)を調整します。

システム変数の設定は、グローバルかつ即時に有効になることに注意してください。値を増やすと、既存のすべてのスナップショットの有効期間が長くなり、値を減らすと、すべてのスナップショットの有効期間が即時に短くなります。MVCC バージョンが多すぎると、TiDB クラスターのパフォーマンスに影響します。そのため、この変数を適時に以前の設定に戻す必要があります。

<CustomContent platform="tidb">

> **ヒント：**
>
> 具体的には、 Dumpling がTiDB (1 TB 未満) からデータをエクスポートしているときに、TiDB のバージョンが v4.0.0 以降であり、 Dumpling がTiDB クラスターの PD アドレスと[`INFORMATION_SCHEMA.CLUSTER_INFO`](/information-schema/information-schema-cluster-info.md)テーブルにアクセスできる場合、 Dumpling はGC セーフ ポイントを自動的に調整して、元のクラスターに影響を与えずに GC をブロックします。
>
> ただし、次のいずれかのシナリオでは、 Dumpling はGC 時間を自動的に調整できません。
>
> -   データサイズが非常に大きい（1TB以上）。
> -   Dumpling はPD に直接接続できません。たとえば、 TiDB クラスターはTiDB Cloud上にあるか、 Dumplingから分離された Kubernetes 上にあります。
>
> このようなシナリオでは、エクスポート プロセス中の GC によるエクスポートの失敗を回避するために、事前に GC 時間を手動で延長する必要があります。
>
> 詳細については[TiDB GC時間を手動で設定する](/dumpling-overview.md#manually-set-the-tidb-gc-time)参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **ヒント：**
>
> 具体的には、 Dumpling がTiDB (1 TB 未満) からデータをエクスポートしているときに、TiDB のバージョンが v4.0.0 以上であり、 Dumpling がTiDB クラスターの PD アドレスにアクセスできる場合、 Dumpling は元のクラスターに影響を与えずに GC 時間を自動的に延長します。
>
> ただし、次のいずれかのシナリオでは、 Dumpling はGC 時間を自動的に調整できません。
>
> -   データサイズが非常に大きい（1TB以上）。
> -   Dumpling はPD に直接接続できません。たとえば、 TiDB クラスターはTiDB Cloud上にあるか、 Dumplingから分離された Kubernetes 上にあります。
>
> このようなシナリオでは、エクスポート プロセス中の GC によるエクスポートの失敗を回避するために、事前に GC 時間を手動で延長する必要があります。
>
> 詳細については[TiDB GC時間を手動で設定する](https://docs.pingcap.com/tidb/stable/dumpling-overview#manually-set-the-tidb-gc-time)参照してください。

</CustomContent>

GC の詳細については、 [GC の概要](/garbage-collection-overview.md)参照してください。

## トランザクションタイムアウト {#transaction-timeout}

トランザクションが開始されてもコミットもロールバックもされないシナリオでは、ロックの保持が長時間続くのを防ぐために、よりきめ細かい制御と短いタイムアウトが必要になる場合があります。この場合、 [`tidb_idle_transaction_timeout`](/system-variables.md#tidb_idle_transaction_timeout-new-in-v760) (TiDB v7.6.0 で導入) を使用して、ユーザー セッション内のトランザクションのアイドル タイムアウトを制御できます。

GC は進行中のトランザクションには影響しません。ただし、実行できる悲観的トランザクションの数には上限があり、トランザクション タイムアウトの制限とトランザクションで使用されるメモリの制限があります。トランザクション タイムアウトは、TiDB プロファイルの`[performance]`カテゴリで`max-txn-ttl`ずつ変更できます (デフォルトでは`60`分)。

`INSERT INTO t10 SELECT * FROM t1`のような SQL 文は GC の影響を受けませんが、 `max-txn-ttl`超えるとタイムアウトによりロールバックされます。

## SQL実行タイムアウト {#sql-execution-timeout}

TiDB には、単一の SQL ステートメントの実行時間を制限するためのシステム変数 (デフォルトでは`max_execution_time` 、 `0` 、制限なしを示します) も用意されています。現在、システム変数は読み取り専用 SQL ステートメントにのみ有効です。 `max_execution_time`の単位は`ms`ですが、実際の精度はミリ秒レベルではなく`100ms`レベルです。

## JDBC クエリ タイムアウト {#jdbc-query-timeout}

MySQL JDBC のクエリ タイムアウト設定`setQueryTimeout()`は、TiDB では機能し***ません***。これは、クライアントがタイムアウトを検出すると、データベースに`KILL`コマンドを送信するためです。ただし、tidb サーバーは負荷分散されており、間違った tidb サーバーでの接続の終了を回避するために、この`KILL`コマンドは実行されません。クエリ タイムアウトの効果を確認するには、 `MAX_EXECUTION_TIME`使用する必要があります。

TiDB は、次の MySQL 互換のタイムアウト制御パラメータを提供します。

-   **wait_timeout は**、 Javaアプリケーションへの接続の非対話型アイドル タイムアウトを制御します。TiDB v5.4 以降、デフォルト値`wait_timeout`は`28800`秒 (8 時間) です。v5.4 より前のバージョンの TiDB の場合、デフォルト値は`0`で、タイムアウトは無制限であることを意味します。
-   **interactive_timeout は**、 Javaアプリケーションへの接続のインタラクティブなアイドル タイムアウトを制御します。デフォルトの値は`8 hours`です。
-   **max_execution_time は**、接続での SQL 実行のタイムアウトを制御します。読み取り専用 SQL ステートメントにのみ有効です。値はデフォルトで`0`設定されており、接続が無限にビジー状態になることを許可します。つまり、SQL ステートメントが無限に長い時間実行されます。

ただし、実際の本番環境では、アイドル接続と SQL ステートメントの無期限実行は、データベースとアプリケーションの両方に悪影響を及ぼします。アプリケーションの接続文字列でこれら 2 つのセッション レベルの変数を構成することで、アイドル接続と SQL ステートメントの無期限実行を回避できます。たとえば、次のように設定します。

-   `sessionVariables=wait_timeout=3600` (1時間)
-   `sessionVariables=max_execution_time=300000` (5分)

## ヘルプが必要ですか? {#need-help}

<CustomContent platform="tidb">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、または[サポートチケットを送信する](/support.md)についてコミュニティに質問してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、または[サポートチケットを送信する](https://tidb.support.pingcap.com/)についてコミュニティに質問してください。

</CustomContent>
