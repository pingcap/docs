---
title: Best Practices for Handling Millions of Tables in SaaS Multi-Tenant Scenarios
summary: SaaS (Software as a Service) マルチテナント シナリオ、特に単一クラスター内のテーブル数が 100 万を超える環境における TiDB のベスト プラクティスを学習します。
aliases: ['/ja/tidb/stable/saas-best-practices/']
---

# SaaS マルチテナントシナリオで数百万のテーブルを処理するためのベストプラクティス {#best-practices-for-handling-millions-of-tables-in-saas-multi-tenant-scenarios}

このドキュメントでは、SaaS（Software as a Service）マルチテナント環境、特に**単一クラスター内のテーブル数が100万を超える**シナリオにおけるTiDBのベストプラクティスを紹介します。適切な構成と選択を行うことで、SaaSシナリオにおいてTiDBを効率的かつ安定的に実行し、リソース消費とコストを削減できます。

> **注記：**
>
> TiDB v8.5.0 以降のバージョンを使用することをお勧めします。

これらのベスト プラクティスの実際のケース スタディについては、ブログ投稿[300万テーブルへの拡張: TiDB が Atlassian Forge の SaaS プラットフォームを支える仕組み](https://www.pingcap.com/blog/scaling-3-million-tables-how-tidb-powers-atlassian-forge-saas-platform/)を参照してください。

## TiDB ハードウェア推奨事項 {#tidb-hardware-recommendations}

大容量メモリを搭載したTiDBインスタンスの使用をお勧めします。例:

-   100 万個のテーブルの場合は、32 GiB 以上のメモリを使用します。
-   300 万のテーブルの場合は、64 GiB 以上のメモリを使用します。

大容量メモリ搭載のTiDBインスタンスは、Infoschema、 統計、および実行プランキャッシュに多くのキャッシュスペースを割り当てるため、キャッシュヒット率が向上し、ビジネスパフォーマンスが向上します。また、大容量メモリは、TiDB GCによるパフォーマンス変動や安定性の問題を軽減します。

TiKV および PD に推奨されるハードウェア構成は次のとおりです。

-   TiKV: 8 個の vCPU と 32 GiB 以上のメモリ。
-   PD: 8 個の CPU と 16 GiB 以上のメモリ。

## リージョンの数を制御する {#control-the-number-of-regions}

多数のテーブル (たとえば、100,000 個以上) を作成する必要がある場合は、TiDB 構成項目[`split-table`](/tidb-configuration-file.md#split-table)を`false`に設定してリージョンの数を減らし、TiKV のメモリ負荷を軽減することをお勧めします。

## キャッシュを構成する {#configure-caches}

-   TiDB v8.4.0 以降、TiDB は SQL 実行中に、SQL ステートメントに関連するテーブル情報をオンデマンドで Infoschema キャッシュにロードします。

    -   TiDB ダッシュボードの**「スキーマ ロード」**パネルの下にある**「Infoschema v2 キャッシュ サイズ」**サブパネルと**「Infoschema v2 キャッシュ操作」**サブパネルを観察することで、Infoschema キャッシュのサイズとヒット率を監視できます。
    -   システム変数[`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-new-in-v800)使用すると、ビジネスニーズに合わせて Infoschema キャッシュのメモリ制限を調整できます。Infoschema キャッシュのサイズは、SQL 実行に関係するテーブルの数に比例します。実際のテストでは、100 万テーブル（各テーブルに 4 つの列、1 つの主キー、1 つのインデックス）のメタデータを完全にキャッシュするには、約 2.4 GiB のメモリが必要です。

-   TiDB は、SQL 実行中に、SQL ステートメントに関係するテーブル統計をオンデマンドで統計キャッシュに読み込みます。

    -   TiDB ダッシュボードの**「統計とプラン管理」**パネルの**「統計キャッシュ コスト**」サブパネルと**「統計キャッシュ OPS」**サブパネルを観察することで、統計キャッシュのサイズとヒット率を監視できます。
    -   システム変数[`tidb_stats_cache_mem_quota`](/system-variables.md#tidb_stats_cache_mem_quota-new-in-v610)を使用することで、ビジネスニーズに合わせて統計キャッシュのメモリ制限を調整できます。実際のテストでは、100,000 個のテーブルに対して単純な SQL（演算子`IndexRangeScan`を使用）を実行すると、統計キャッシュで約 3.96 GiB のメモリが消費されます。

## 統計を収集する {#collect-statistics}

-   TiDB v8.4.0以降、TiDBはTiDBクラスター内で同時に実行できる自動分析操作の数を制御するためのシステム変数[`tidb_auto_analyze_concurrency`](/system-variables.md#tidb_auto_analyze_concurrency-new-in-v840)を導入しました。複数テーブルを扱うシナリオでは、必要に応じてこの同時実行数を増やすことで、自動分析のスループットを向上させることができます。同時実行数の値を増やすと、スループットとTiDBオーナーノードのCPU使用率は直線的に増加します。実際のテストでは、同時実行数を16に設定することで、1分以内に320個のテーブル（各テーブルは10,000行、4列、1つのインデックスを持つ）の自動分析を実行でき、TiDBオーナーノードのCPUコアを1つ消費しました。
-   システム変数[`tidb_auto_build_stats_concurrency`](/system-variables.md#tidb_auto_build_stats_concurrency-new-in-v650)と[`tidb_build_sampling_stats_concurrency`](/system-variables.md#tidb_build_sampling_stats_concurrency-new-in-v750)は、TiDB統計情報の構築における同時実行性を制御します。シナリオに応じて調整できます。
    -   パーティション化されたテーブルが多数あるシナリオでは、 `tidb_auto_build_stats_concurrency`の値を増やすことを優先します。
    -   列数が多いシナリオでは、 `tidb_build_sampling_stats_concurrency`の値を増やすことを優先します。
-   過剰なリソース使用を避けるため、 `tidb_auto_analyze_concurrency` 、 `tidb_auto_build_stats_concurrency` 、 `tidb_build_sampling_stats_concurrency`の積が TiDB CPU コアの数を超えないようにしてください。

## システムテーブルを効率的にクエリする {#query-system-tables-efficiently}

システムテーブルをクエリする際は、大量の無関係なデータのスキャンを回避するために、 `TABLE_SCHEMA` 、 `TABLE_NAME` 、 `TIDB_TABLE_ID`などのフィルターを追加することをお勧めします。これにより、クエリ速度が向上し、リソース消費が削減されます。

たとえば、300 万のテーブルがあるシナリオでは次のようになります。

-   次の SQL ステートメントを実行すると、約 8 GiB のメモリが消費されます。

    ```sql
    SELECT COUNT(*) FROM information_schema.tables;
    ```

-   次の SQL ステートメントの実行には約 20 分かかります。

    ```sql
    SELECT COUNT(*) FROM information_schema.views;
    ```

前述の SQL ステートメントに適切なフィルター条件を追加することで、メモリ消費量は無視できるほどになり、クエリ時間は数ミリ秒に短縮されます。

## 接続集中型のシナリオを処理する {#handle-connection-intensive-scenarios}

SaaSマルチテナントシナリオでは、通常、各ユーザーはTiDBに接続して自身のテナント（データベース）内のデータを操作します。多数の接続をサポートするには、次の点に留意してください。

-   より多くの同時リクエストをサポートするには、TiDB 構成項目[`token-limit`](/tidb-configuration-file.md#token-limit) (デフォルトでは`1000` ) を増やします。
-   TiDBのメモリ使用量は接続数にほぼ比例します。実際のテストでは、アイドル接続が20万件あると、TiDBのメモリ使用量が約30GiB増加しました。実際の接続数に基づいて、TiDBのメモリ仕様を増やすことをお勧めします。
-   `PREPARED`ステートメントを使用する場合、各接続はセッションレベルのプリペアドプランキャッシュを維持します。3 `DEALLOCATE`ステートメントが長時間実行されない場合、キャッシュに過剰なプランが蓄積され、メモリ使用量が増加する可能性があります。実際のテストでは、 `IndexRangeScan`含む 400,000 の実行プランで約 5 GiB のメモリが消費されました。これに応じてメモリ仕様を増やすことをお勧めします。

## 古いものを使用するには、慎重に読んでください {#use-stale-read-carefully}

[ステイル読み取り](/stale-read.md)使用すると、古いスキーマバージョンによって過去のスキーマがフルロードされ、パフォーマンスに重大な影響を与える可能性があります。この問題を軽減するには、 [`tidb_schema_version_cache_limit`](/system-variables.md#tidb_schema_version_cache_limit-new-in-v740)の値を（例えば`255`に）増やしてください。

## BRバックアップと復元を最適化 {#optimize-br-backup-and-restore}

-   数百万のテーブルを含むフルバックアップを復元する場合は、大容量メモリを搭載したBRインスタンスの使用をお勧めします。例:
    -   100 万個のテーブルの場合は、32 GiB 以上のメモリを備えたBRインスタンスを使用します。
    -   300 万のテーブルの場合は、64 GiB 以上のメモリを備えたBRインスタンスを使用します。
-   BRログバックアップとスナップショットリストアは追加のTiKVメモリを消費します。32GiB以上のメモリを搭載したTiKVインスタンスの使用をお勧めします。
-   ログの復元速度を向上させるには、必要に応じてBR構成[`pitr-batch-count`と`pitr-concurrency`](/br/br-pitr-manual.md#restore-to-a-specified-point-in-time-pitr)を調整します。

## TiDB Lightningでデータをインポートする {#import-data-with-tidb-lightning}

[TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)を使用して数百万のテーブルをインポートする場合は、次の推奨事項に従ってください。

-   大きなテーブル (100 GiB 以上) の場合は、 TiDB Lightning [物理インポートモード](/tidb-lightning/tidb-lightning-physical-import-mode.md)を使用します。
-   小さなテーブル (通常は多数) の場合は、 TiDB Lightning [論理インポートモード](/tidb-lightning/tidb-lightning-logical-import-mode.md)を使用します。
