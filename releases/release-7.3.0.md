---
title: TiDB 7.3.0 Release Notes
summary: TiDB 7.3.0 の新機能、互換性の変更、改善、バグ修正について説明します。
---

# TiDB 7.3.0 リリースノート {#tidb-7-3-0-release-notes}

発売日: 2023年8月14日

TiDB バージョン: 7.3.0

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v7.3/quick-start-with-tidb)

7.3.0 では、次の主要な機能が導入されています。さらに、7.3.0 には、TiDBサーバーとTiFlashのクエリ安定性を強化する一連の機能強化 (セクション[機能の詳細](#feature-details)で説明) も含まれています。これらの機能強化は、本質的に雑多であり、ユーザーに直接関係するものではないため、次の表には含まれていません。

<table><thead><tr><th>カテゴリ</th><th>特徴</th><th>説明</th></tr></thead><tbody><tr><td>スケーラビリティとパフォーマンス</td><td>TiDB Lightning は<a href="https://docs.pingcap.com/tidb/v7.3/partitioned-raft-kv">Partitioned Raft KV</a>をサポートします (実験的)</td><td> TiDB Lightning は、アーキテクチャの近い将来の GA の一環として、新しい Partitioned Raft KVアーキテクチャをサポートするようになりました。</td></tr><tr><td rowspan="2">信頼性と可用性</td><td><a href="https://docs.pingcap.com/tidb/v7.3/tidb-lightning-physical-import-mode-usage#conflict-detection">データのインポート時に自動競合検出と解決を追加する</a></td><td>TiDB Lightning物理インポート モードは、競合検出の新しいバージョンをサポートしており、競合が発生した場合に競合データを置き換える ( <code>replace</code> ) か無視する ( <code>ignore</code> ) というセマンティクスを実装しています。競合データを自動的に処理しながら、競合解決のパフォーマンスを向上させます。</td></tr><tr><td><a href="https://docs.pingcap.com/tidb/v7.3/tidb-resource-control#query-watch-parameters">暴走クエリの手動管理</a>（実験的）</td><td>クエリには予想よりも時間がかかる場合があります。リソース グループの新しいウォッチ リストを使用すると、クエリをより効率的に管理し、優先順位を下げるか、強制終了することができます。オペレーターが正確な SQL テキスト、SQL ダイジェスト、またはプラン ダイジェストでターゲット クエリをマークし、リソース グループ レベルでクエリを処理できるこの機能により、予期しない大規模なクエリがクラスターに及ぼす潜在的な影響をより詳細に制御できます。</td></tr><tr><td>構文</td><td><a href="https://docs.pingcap.com/tidb/v7.3/optimizer-hints">クエリプランナーにオプティマイザヒントを追加することで、クエリの安定性に対するオペレータの制御を強化します。</a></td><td>追加されたヒント: <code>NO_INDEX_JOIN()</code> 、 <code>NO_MERGE_JOIN()</code> 、 <code>NO_INDEX_MERGE_JOIN()</code> 、 <code>NO_HASH_JOIN()</code> 、 <code>NO_INDEX_HASH_JOIN()</code></td></tr><tr><td> DB 操作と可観測性</td><td><a href="https://docs.pingcap.com/tidb/v7.3/sql-statement-show-analyze-status">統計収集タスクの進行状況を表示する</a></td><td><code>SHOW ANALYZE STATUS</code>ステートメントまたは<code>mysql.analyze_jobs</code>システム テーブルを使用して、 <code>ANALYZE</code>タスクの進行状況を表示できるようになりました。</td></tr></tbody></table>

## 機能の詳細 {#feature-details}

### パフォーマンス {#performance}

-   TiFlashはレプリカ選択戦略[＃44106](https://github.com/pingcap/tidb/issues/44106) @ [徐懐玉](https://github.com/XuHuaiyu)をサポートします

    v7.3.0 より前のバージョンでは、 TiFlash はパフォーマンスを最大化するために、データ スキャンと MPP 計算にすべてのノードのレプリカを使用していました。v7.3.0 以降では、 TiFlash にレプリカ選択戦略が導入され、 [`tiflash_replica_read`](/system-variables.md#tiflash_replica_read-new-in-v730)システム変数を使用して構成できるようになりました。この戦略では、 [ゾーン属性](/schedule-replicas-by-topology-labels.md#optional-configure-labels-for-tidb)のノードに基づいて特定のレプリカを選択し、データ スキャンと MPP 計算のために特定のノードをスケジュールすることがサポートされています。

    複数のデータ センターに展開され、各データ センターに完全なTiFlashデータ レプリカがあるクラスターの場合、現在のデータ センターからのみTiFlashレプリカを選択するようにこの戦略を構成できます。つまり、データ スキャンと MPP 計算は現在のデータ センターのTiFlashノードでのみ実行されるため、データ センター間での過剰なネットワーク データ転送を回避できます。

    詳細については[ドキュメント](/system-variables.md#tiflash_replica_read-new-in-v730)参照してください。

-   TiFlashはノード[#40220](https://github.com/pingcap/tidb/issues/40220) @ [エルサ0520](https://github.com/elsa0520)内でランタイムフィルターをサポートします。

    ランタイム フィルターは、クエリ プランニング フェーズで生成される**動的述語**です。テーブル結合のプロセスでは、これらの動的述語によって結合条件を満たさない行を効果的にフィルター処理できるため、スキャン時間とネットワーク オーバーヘッドが削減され、テーブル結合の効率が向上します。v7.3.0 以降、 TiFlash はノード内でランタイム フィルターをサポートし、分析クエリの全体的なパフォーマンスが向上します。一部の TPC-DS ワークロードでは、パフォーマンスが 10% ～ 50% 向上します。

    この機能は、v7.3.0 ではデフォルトで無効になっています。この機能を有効にするには、システム変数[`tidb_runtime_filter_mode`](/system-variables.md#tidb_runtime_filter_mode-new-in-v720)を`LOCAL`に設定します。

    詳細については[ドキュメント](/runtime-filter.md)参照してください。

-   TiFlash は共通テーブル式 (CTE) の実行をサポートしています (実験的) [#43333](https://github.com/pingcap/tidb/issues/43333) @ [ウィノロス](https://github.com/winoros)

    v7.3.0 より前では、 TiFlashの MPP エンジンは、デフォルトで CTE を含むクエリを実行できません。MPP フレームワーク内で最高の実行パフォーマンスを実現するには、システム変数[`tidb_opt_force_inline_cte`](/system-variables.md#tidb_opt_force_inline_cte-new-in-v630)使用して CTE のインライン化を強制する必要があります。

    v7.3.0 以降、TiFlash の MPP エンジンは、CTE をインライン化せずにクエリを実行することをサポートし、MPP フレームワーク内で最適なクエリ実行を可能にします。TPC-DS ベンチマーク テストでは、この機能により、CTE をインライン化する場合と比較して、CTE を含むクエリの全体的なクエリ実行速度が 20% 向上することが示されました。

    この機能は実験的であり、デフォルトでは無効になっています。これはシステム変数[`tidb_opt_enable_mpp_shared_cte_execution`](/system-variables.md#tidb_opt_enable_mpp_shared_cte_execution-new-in-v720)によって制御されます。

### 信頼性 {#reliability}

-   新しいオプティマイザヒント[＃45520](https://github.com/pingcap/tidb/issues/45520) @ [qw4990](https://github.com/qw4990)を追加

    v7.3.0 では、TiDB はテーブル間の結合方法を制御するためのいくつかの新しいオプティマイザーヒントを導入しています。

    -   [`NO_MERGE_JOIN()`](/optimizer-hints.md#no_merge_joint1_name--tl_name-)マージ結合以外の結合方法を選択します。
    -   [`NO_INDEX_JOIN()`](/optimizer-hints.md#no_index_joint1_name--tl_name-)インデックス ネスト ループ結合以外の結合方法を選択します。
    -   [`NO_INDEX_MERGE_JOIN()`](/optimizer-hints.md#no_index_merge_joint1_name--tl_name-)インデックス ネスト ループ マージ結合以外の結合方法を選択します。
    -   [`NO_HASH_JOIN()`](/optimizer-hints.md#no_hash_joint1_name--tl_name-)ハッシュ結合以外の結合方法を選択します。
    -   [`NO_INDEX_HASH_JOIN()`](/optimizer-hints.md#no_index_hash_joint1_name--tl_name-) [インデックスネストループハッシュ結合](/optimizer-hints.md#inl_hash_join)以外の結合方法を選択します。

    詳細については[ドキュメント](/optimizer-hints.md)参照してください。

-   予想以上にリソースを使用するクエリを手動でマークする (実験的) [＃43691](https://github.com/pingcap/tidb/issues/43691) @ [コナー1996](https://github.com/Connor1996) @ [キャビンフィーバーB](https://github.com/CabinfeverB)

    v7.2.0 では、TiDB は、予想以上にリソースを使用するクエリ (ランナウェイ クエリ) を自動的にダウングレードまたはキャンセルすることで、ランナウェイ クエリを自動的に管理します。実際には、ルールだけではすべてのケースをカバーできません。そのため、TiDB v7.3.0 では、ランナウェイ クエリを手動でマークする機能が導入されています。新しいコマンド[`QUERY WATCH`](/sql-statements/sql-statement-query-watch.md)を使用すると、SQL テキスト、SQL ダイジェスト、または実行プランに基づいてランナウェイ クエリをマークし、マークされたランナウェイ クエリをダウングレードまたはキャンセルできます。

    この機能は、データベースで突然発生するパフォーマンスの問題に対して効果的な介入方法を提供します。クエリによって発生するパフォーマンスの問題の場合、根本原因を特定する前に、この機能によって全体的なパフォーマンスへの影響を迅速に軽減し、システム サービスの品質を向上させることができます。

    詳細については[ドキュメント](/tidb-resource-control.md#query-watch-parameters)参照してください。

### 構文 {#sql}

-   リストとリスト列のパーティションテーブルは、デフォルトのパーティション[＃20679](https://github.com/pingcap/tidb/issues/20679) @ [ミョンス](https://github.com/mjonss) @ [bb7133](https://github.com/bb7133)をサポートします。

    v7.3.0 より前では、 `INSERT`ステートメントを使用してリストまたはリスト COLUMNSパーティションテーブルにデータを挿入する場合、データはテーブルの指定されたパーティション条件を満たす必要があります。挿入するデータがこれらの条件のいずれも満たさない場合、ステートメントの実行は失敗するか、または非準拠のデータは無視されます。

    v7.3.0 以降、List および List COLUMNS パーティション テーブルは、デフォルト パーティションをサポートします。デフォルト パーティションの作成後、挿入するデータがパーティション条件を満たさない場合、そのデータはデフォルト パーティションに書き込まれます。この機能により、List およびList COLUMNS パーティショニングの使いやすさが向上し、 `INSERT`ステートメントの実行失敗や、パーティション条件を満たさないデータによるデータの無視を回避できます。

    この機能は、MySQL 構文に対する TiDB 拡張であることに注意してください。デフォルト パーティションを持つパーティションテーブルの場合、テーブル内のデータを MySQL に直接複製することはできません。

    詳細については[ドキュメント](/partitioned-table.md#list-partitioning)参照してください。

### 可観測性 {#observability}

-   統計収集の進行状況を表示する[＃44033](https://github.com/pingcap/tidb/issues/44033) @ [ホーキングレイ](https://github.com/hawkingrei)

    大規模なテーブルの統計の収集には、多くの場合、長い時間がかかります。以前のバージョンでは、統計の収集の進行状況を確認できなかったため、完了時間を予測できませんでした。TiDB v7.3.0 では、統計の収集の進行状況を表示する機能が導入されています。システム テーブル`mysql.analyze_jobs`または`SHOW ANALYZE STATUS`使用して、サブタスクごとに全体的なワークロード、現在の進行状況、および推定完了時間を表示できます。大規模なデータのインポートや SQL パフォーマンスの最適化などのシナリオでは、この機能により、タスク全体の進行状況を把握し、ユーザー エクスペリエンスを向上させることができます。

    詳細については[ドキュメント](/sql-statements/sql-statement-show-analyze-status.md)参照してください。

-   Plan Replayerは履歴統計[＃45038](https://github.com/pingcap/tidb/issues/45038) @ [時間と運命](https://github.com/time-and-fate)のエクスポートをサポートします

    v7.3.0 以降では、新しく追加された[`dump with stats as of timestamp`](/sql-plan-replayer.md)句により、Plan Replayer を使用して、特定の時点での指定された SQL 関連オブジェクトの統計をエクスポートできます。実行プランの問題の診断中に、履歴統計を正確に取得すると、問題が発生した時点で実行プランがどのように生成されたかをより正確に分析するのに役立ちます。これにより、問題の根本原因を特定し、実行プランの問題の診断の効率を大幅に向上させることができます。

    詳細については[ドキュメント](/sql-plan-replayer.md)参照してください。

### データ移行 {#data-migration}

-   TiDB Lightning は、競合データ検出および処理戦略[＃41629](https://github.com/pingcap/tidb/issues/41629) @ [ランス6716](https://github.com/lance6716)の新しいバージョンを導入します

    以前のバージョンでは、 TiDB Lightning は論理インポート モードと物理インポート モードに対して異なる競合検出および処理方法を使用していましたが、設定が複雑で、ユーザーにとって理解しにくいものでした。また、物理インポート モードでは、 `replace`または`ignore`戦略を使用して競合を処理できません。v7.3.0 以降、 TiDB Lightning は論理インポート モードと物理インポート モードの両方に対して統合された競合検出および処理戦略を導入しています。競合が発生した場合、エラーを報告する ( `error` )、競合データを置き換える ( `replace` )、または無視する ( `ignore` ) ことを選択できます。競合レコードの数を制限できます。たとえば、指定された数の競合レコードを処理した後にタスクを中断して終了するなどです。さらに、システムはトラブルシューティングのために競合データを記録できます。

    競合の多いインポート データの場合、パフォーマンスを向上させるために、新しいバージョンの競合検出および処理戦略を使用することをお勧めします。ラボ環境では、新しいバージョンの戦略により、競合検出および処理のパフォーマンスが古いバージョンよりも最大 3 倍高速化されます。このパフォーマンス値は参考値です。実際のパフォーマンスは、構成、テーブル構造、競合データの割合によって異なる場合があります。新しいバージョンと古いバージョンの競合戦略を同時に使用することはできません。古い競合検出および処理戦略は、将来廃止される予定です。

    詳細については[ドキュメント](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#conflict-detection)参照してください。

-   TiDB Lightning はPartitioned Raft KV (実験的) [＃14916](https://github.com/tikv/tikv/issues/14916) @ [GMHDBJD](https://github.com/GMHDBJD)をサポートします

    TiDB Lightning は、パーティション化されたRaft KV をサポートするようになりました。この機能により、 TiDB Lightningのデータ インポート パフォーマンスが向上します。

-   TiDB Lightning、より多くの診断ログを印刷することでトラブルシューティングを強化する新しいパラメータ`enable-diagnose-log`が導入されました[＃45497](https://github.com/pingcap/tidb/issues/45497) @ [D3ハンター](https://github.com/D3Hunter)

    デフォルトでは、この機能は無効になっており、 TiDB Lightning は`lightning/main`含むログのみを出力。有効にすると、 TiDB Lightning はすべてのパッケージ ( `client-go`と`tidb`を含む) のログを出力、 `client-go`と`tidb`に関連する問題の診断に役立ちます。

    詳細については[ドキュメント](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-global)参照してください。

## 互換性の変更 {#compatibility-changes}

> **注記：**
>
> このセクションでは、v7.2.0 から現在のバージョン (v7.3.0) にアップグレードするときに知っておく必要のある互換性の変更について説明します。v7.1.0 以前のバージョンから現在のバージョンにアップグレードする場合は、中間バージョンで導入された互換性の変更も確認する必要がある可能性があります。

### 行動の変化 {#behavior-changes}

-   ティビ

    -   MPP は、 TiFlashエンジンによって提供される分散コンピューティング フレームワークであり、ノード間のデータ交換を可能にし、高性能で高スループットの SQL アルゴリズムを提供します。他のプロトコルと比較して、MPP プロトコルはより成熟しており、より優れたタスクおよびリソース管理を提供できます。v7.3.0 以降では、 TiDB が計算タスクをTiFlashにプッシュする場合、オプティマイザーはデフォルトで MPP プロトコルを使用して実行プランのみを生成します。 [`tidb_allow_mpp`](/system-variables.md#tidb_allow_mpp-new-in-v50) `OFF`に設定すると、TiDB をアップグレードした後にクエリがエラーを返す可能性があります。アップグレード前に`tidb_allow_mpp`の値を確認し、 `ON`に設定することをお勧めします。コスト見積もりに基づいて実行プランを生成するためにオプティマイザーが Cop、BatchCop、および MPP プロトコルのいずれかを選択する必要がある場合は、 [`tidb_allow_tiflash_cop`](/system-variables.md#tidb_allow_tiflash_cop-new-in-v730)変数を`ON`に設定できます。

-   バックアップと復元 (BR)

    -   BR は、完全なデータ復元を実行する前に、空のクラスター チェックを追加します。デフォルトでは、空でないクラスターへのデータの復元は許可されません。復元を強制する場合は、 `--filter`オプションを使用して、データを復元する対応するテーブル名を指定できます。

-   TiDB Lightning

    -   `tikv-importer.on-duplicate`非推奨となり、 [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)に置き換えられました。
    -   移行タスクを停止する前にTiDB Lightning が許容できる致命的でないエラーの最大数を制御する`max-error`パラメータは、インポート データの競合を制限しなくなりました。3 [`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)は、許容できる競合レコードの最大数を制御するようになりました。

-   ティCDC

    -   Kafka シンクが Avro プロトコルを使用する場合、 `force-replicate`パラメータが`true`に設定されると、TiCDC は変更フィードを作成するときにエラーを報告します。
    -   `delete-only-output-handle-key-columns`と`force-replicate`パラメータの間に互換性がないため、両方のパラメータが有効になっていると、TiCDC は変更フィードを作成するときにエラーを報告します。
    -   出力プロトコルがオープン プロトコルの場合、 `UPDATE`イベントは変更された列のみを出力します。

### システム変数 {#system-variables}

| 変数名                                                                                                                     | タイプを変更   | 説明                                                                              |
| ----------------------------------------------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------- |
| [`tidb_opt_enable_mpp_shared_cte_execution`](/system-variables.md#tidb_opt_enable_mpp_shared_cte_execution-new-in-v720) | 修正済み     | このシステム変数は、v7.3.0 以降で有効になります。これは、非再帰共通テーブル式 (CTE) をTiFlash MPP で実行できるかどうかを制御します。 |
| [`tidb_allow_tiflash_cop`](/system-variables.md#tidb_allow_tiflash_cop-new-in-v730)                                     | 新しく追加された | このシステム変数は、TiDB が計算タスクをTiFlashにプッシュダウンするときに実行プランを生成するためのプロトコルを選択するために使用されます。     |
| [`tidb_lock_unchanged_keys`](/system-variables.md#tidb_lock_unchanged_keys-new-in-v711-and-v730)                        | 新しく追加された | この変数は、特定のシナリオで、トランザクションに関係しているが変更されていないキーをロックするかどうかを制御するために使用されます。              |
| [`tidb_opt_enable_non_eval_scalar_subquery`](/system-variables.md#tidb_opt_enable_non_eval_scalar_subquery-new-in-v730) | 新しく追加された | `EXPLAIN`ステートメントが、最適化段階で展開できる定数サブクエリの実行を無効にするかどうかを制御します。                        |
| [`tidb_skip_missing_partition_stats`](/system-variables.md#tidb_skip_missing_partition_stats-new-in-v730)               | 新しく追加された | この変数は、パーティション統計が欠落している場合の GlobalStats の生成を制御します。                                |
| [`tiflash_replica_read`](/system-variables.md#tiflash_replica_read-new-in-v730)                                         | 新しく追加された | クエリにTiFlashエンジンが必要な場合にTiFlashレプリカを選択する戦略を制御します。                                 |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーションパラメータ                                                                                                                                 | タイプを変更   | 説明                                                                                                                                                                                                                                                                                                                                                                  |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ティビ            | [`enable-32bits-connection-id`](/tidb-configuration-file.md#enable-32bits-connection-id-new-in-v730)                                            | 新しく追加された | 32 ビット接続 ID 機能を有効にするかどうかを制御します。                                                                                                                                                                                                                                                                                                                                     |
| ティビ            | [`in-mem-slow-query-recent-num`](/tidb-configuration-file.md#in-mem-slow-query-recent-num-new-in-v730)                                          | 新しく追加された | メモリにキャッシュされる最近使用された低速クエリの数を制御します。                                                                                                                                                                                                                                                                                                                                   |
| ティビ            | [`in-mem-slow-query-topn-num`](/tidb-configuration-file.md#in-mem-slow-query-topn-num-new-in-v730)                                              | 新しく追加された | メモリにキャッシュされる最も遅いクエリの数を制御します。                                                                                                                                                                                                                                                                                                                                        |
| ティクヴ           | [`coprocessor.region-bucket-size`](/tikv-configuration-file.md#region-bucket-size-new-in-v610)                                                  | 修正済み     | デフォルト値を`96MiB`から`50MiB`に変更します。                                                                                                                                                                                                                                                                                                                                      |
| ティクヴ           | [`raft-engine.format-version`](/tikv-configuration-file.md#format-version-new-in-v630)                                                          | 修正済み     | Partitioned Raft KV（ `storage.engine="partitioned-raft-kv"` ）を使用する場合、リボンフィルタが使用されます。そのため、TiKVはデフォルト値を`2`から`5`に変更します。                                                                                                                                                                                                                                                |
| ティクヴ           | [`raftdb.max-total-wal-size`](/tikv-configuration-file.md#max-total-wal-size-1)                                                                 | 修正済み     | Partitioned Raft KV（ `storage.engine="partitioned-raft-kv"` ）を使用する場合、TiKVはWALの書き込みをスキップします。そのため、TiKVはデフォルト値を`"4GB"`から`1`に変更し、WALが無効であることを意味します。                                                                                                                                                                                                                     |
| ティクヴ           | [`rocksdb.[defaultcf|writecf|lockcf].compaction-guard-min-output-file-size`](/tikv-configuration-file.md#compaction-guard-min-output-file-size) | 修正済み     | 大容量データの書き込み時に圧縮速度が書き込み速度に追いつかない問題を解決するために、デフォルト値を`"1MB"`から`"8MB"`に変更します。                                                                                                                                                                                                                                                                                            |
| ティクヴ           | [`rocksdb.[defaultcf|writecf|lockcf].format-version`](/tikv-configuration-file.md#format-version-new-in-v620)                                   | 修正済み     | Partitioned Raft KV（ `storage.engine="partitioned-raft-kv"` ）を使用する場合、リボンフィルタが使用されます。そのため、TiKVはデフォルト値を`2`から`5`に変更します。                                                                                                                                                                                                                                                |
| ティクヴ           | [`rocksdb.lockcf.write-buffer-size`](/tikv-configuration-file.md#write-buffer-size)                                                             | 修正済み     | Partitioned Raft KV（ `storage.engine="partitioned-raft-kv"` ）を使用する場合、lockcfでの圧縮を高速化するために、TiKVはデフォルト値を`"32MB"`から`"4MB"`に変更します。                                                                                                                                                                                                                                       |
| ティクヴ           | [`rocksdb.max-total-wal-size`](/tikv-configuration-file.md#max-total-wal-size)                                                                  | 修正済み     | Partitioned Raft KV（ `storage.engine="partitioned-raft-kv"` ）を使用する場合、TiKVはWALの書き込みをスキップします。そのため、TiKVはデフォルト値を`"4GB"`から`1`に変更し、WALが無効であることを意味します。                                                                                                                                                                                                                     |
| ティクヴ           | [`rocksdb.stats-dump-period`](/tikv-configuration-file.md#stats-dump-period)                                                                    | 修正済み     | Partitioned Raft KV（ `storage.engine="partitioned-raft-kv"` ）を使用する場合、冗長ログ出力を無効にするには、デフォルト値を`"10m"`から`"0"`に変更します。                                                                                                                                                                                                                                                    |
| ティクヴ           | [`rocksdb.write-buffer-limit`](/tikv-configuration-file.md#write-buffer-limit-new-in-v660)                                                      | 修正済み     | memtablesのメモリオーバーヘッドを削減するために、 `storage.engine="raft-kv"`場合、TiKVはデフォルト値をマシンのメモリの25%から無制限を意味する`0`に変更します。Partitioned Raft KV（ `storage.engine="partitioned-raft-kv"` ）を使用する場合、TiKVはデフォルト値をマシンのメモリの25%から20%に変更します。                                                                                                                                                      |
| ティクヴ           | [`storage.block-cache.capacity`](/tikv-configuration-file.md#capacity)                                                                          | 修正済み     | パーティション化されたRaft KV（ `storage.engine="partitioned-raft-kv"` ）を使用する場合、memtablesのメモリオーバーヘッドを補うために、TiKVはデフォルト値をシステムメモリ全体のサイズの45％から30％に変更します。                                                                                                                                                                                                                            |
| TiFlash        | [`storage.format_version`](/tiflash/tiflash-configuration.md)                                                                                   | 修正済み     | 小さなファイルを結合して物理ファイルの数を減らすために、新しい DTFile 形式`format_version = 5`を導入します。この形式は実験的であり、デフォルトでは有効になっていないことに注意してください。                                                                                                                                                                                                                                                        |
| TiDB Lightning | `tikv-importer.incremental-import`                                                                                                              | 削除されました  | TiDB Lightning並列インポート パラメータ。増分インポート パラメータと間違われる可能性が高かったため、このパラメータの名前は`tikv-importer.parallel-import`に変更されました。ユーザーが古いパラメータ名を渡すと、自動的に新しいパラメータ名に変換されます。                                                                                                                                                                                                                |
| TiDB Lightning | `tikv-importer.on-duplicate`                                                                                                                    | 非推奨      | 論理インポート モードで競合するレコードを挿入しようとしたときに実行するアクションを制御します。v7.3.0 以降では、このパラメーターは[`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)に置き換えられます。                                                                                                                                                                                           |
| TiDB Lightning | [`conflict.max-record-rows`](/tidb-lightning/tidb-lightning-configuration.md)                                                                   | 新しく追加された | 競合するデータを処理する戦略の新しいバージョン。1 `conflict_records`のテーブル内の行の最大数を制御します。デフォルト値は 100 です。                                                                                                                                                                                                                                                                                      |
| TiDB Lightning | [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md)                                                                          | 新しく追加された | 競合するデータを処理する戦略の新しいバージョン。次のオプションが含まれます: &quot;&quot; (TiDB Lightning は競合するデータを検出および処理しません)、 `error` (インポートされたデータで主キーまたは一意キーの競合が検出された場合は、インポートを終了してエラーを報告します)、 `replace` (競合する主キーまたは一意キーを持つデータが検出された場合、新しいデータは保持され、古いデータは上書きされます)、 `ignore` (競合する主キーまたは一意キーを持つデータが検出された場合、古いデータは保持され、新しいデータは無視されます)。デフォルト値は &quot;&quot; です。つまり、 TiDB Lightning は競合するデータを検出および処理しません。 |
| TiDB Lightning | [`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md)                                                                         | 新しく追加された | 競合データの上限を制御します。 `conflict.strategy="error"`場合、デフォルト値は`0`です。 `conflict.strategy="replace"`または`conflict.strategy="ignore"`の場合、maxint として設定できます。                                                                                                                                                                                                                       |
| TiDB Lightning | [`enable-diagnose-logs`](/tidb-lightning/tidb-lightning-configuration.md)                                                                       | 新しく追加された | 診断ログを有効にするかどうかを制御します。デフォルト値は`false`で、インポートに関連するログのみが出力され、他の依存コンポーネントのログは出力されません。 `true`に設定すると、インポートプロセスと他の依存コンポーネントの両方のログが出力され、診断に使用できる GRPC デバッグが有効になります。                                                                                                                                                                                                          |
| TiDB Lightning | [`tikv-importer.parallel-import`](/tidb-lightning/tidb-lightning-configuration.md)                                                              | 新しく追加された | TiDB Lightning並列インポート パラメータ。増分インポート パラメータと間違えられ、誤用される可能性のある既存の`tikv-importer.incremental-import`パラメータを置き換えます。                                                                                                                                                                                                                                                       |
| BR             | `azblob.encryption-scope`                                                                                                                       | 新しく追加された | BR は、Azure Blob Storage の暗号化スコープ サポートを提供します。                                                                                                                                                                                                                                                                                                                        |
| BR             | `azblob.encryption-key`                                                                                                                         | 新しく追加された | BR は、Azure Blob Storage の暗号化キー サポートを提供します。                                                                                                                                                                                                                                                                                                                          |
| ティCDC          | [`large-message-handle-option`](/ticdc/ticdc-sink-to-kafka.md#handle-messages-that-exceed-the-kafka-topic-limit)                                | 新しく追加された | デフォルトでは空です。つまり、メッセージ サイズが Kafka トピックの制限を超えると、changefeed は失敗します。この構成が`"handle-key-only"`に設定されている場合、メッセージがサイズ制限を超えると、メッセージ サイズを縮小するためにハンドル キーのみが送信されます。縮小されたメッセージでも制限を超えると、changefeed は失敗します。                                                                                                                                                                         |
| ティCDC          | [`sink.csv.binary-encoding-method`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)                                      | 新しく追加された | バイナリ データのエンコード方法。 `'base64'`または`'hex'`を指定できます。デフォルト値は`'base64'`です。                                                                                                                                                                                                                                                                                                  |

### システムテーブル {#system-tables}

-   内部タイマーのメタデータを保存するための新しいシステム テーブル`mysql.tidb_timers`を追加します。

## 廃止された機能 {#deprecated-features}

-   ティビ

    -   統計の[`Fast Analyze`](/system-variables.md#tidb_enable_fast_analyze)機能 (実験的) は、v7.5.0 で廃止される予定です。
    -   統計の[増分コレクション](https://docs.pingcap.com/tidb/v7.3/statistics#incremental-collection)機能は、v7.5.0 で廃止されます。

## 改善点 {#improvements}

-   ティビ

    -   最適化フェーズ[＃22076](https://github.com/pingcap/tidb/issues/22076) @ [ウィノロス](https://github.com/winoros)中に`EXPLAIN`ステートメントがサブクエリを事前に実行するかどうかを制御するための新しいシステム変数[`tidb_opt_enable_non_eval_scalar_subquery`](/system-variables.md#tidb_opt_enable_non_eval_scalar_subquery-new-in-v730)を導入します。
    -   [グローバルキル](/tidb-configuration-file.md#enable-global-kill-new-in-v610)が有効になっている場合、 <kbd>Control+C</kbd> [＃8854](https://github.com/pingcap/tidb/issues/8854) @ [ピンギュ](https://github.com/pingyu)を押すことで現在のセッションを終了できます。
    -   `IS_FREE_LOCK()`と`IS_USED_LOCK()`ロック関数[＃44493](https://github.com/pingcap/tidb/issues/44493) @ [ドヴェーデン](https://github.com/dveeden)をサポート
    -   ディスク[＃45125](https://github.com/pingcap/tidb/issues/45125) @ [ヤンケオ](https://github.com/YangKeao)からダンプされたチャンクの読み取りパフォーマンスを最適化します。
    -   オプティマイザ修正コントロール[＃44855](https://github.com/pingcap/tidb/issues/44855) @ [時間と運命](https://github.com/time-and-fate)を使用して、インデックス結合の内部テーブルの過大評価の問題を最適化します。

-   ティクヴ

    -   `Max gap of safe-ts`と`Min safe ts region`メトリックを追加し、 `tikv-ctl get-region-read-progress`コマンドを導入して、resolved-tsと安全な ts の状態をより適切に観察および診断します[＃15082](https://github.com/tikv/tikv/issues/15082) @ [エキシウム](https://github.com/ekexium)

-   PD

    -   Swaggerサーバーが有効になっていない場合に、デフォルトで Swagger API をブロックするサポート[＃6786](https://github.com/tikv/pd/issues/6786) @ [バッファフライ](https://github.com/bufferflies)
    -   etcd [＃6554](https://github.com/tikv/pd/issues/6554) [＃6442](https://github.com/tikv/pd/issues/6442) @ [翻訳者](https://github.com/lhy1024)の高可用性を向上させる
    -   `GetRegions`リクエスト[＃6835](https://github.com/tikv/pd/issues/6835) @ [翻訳者](https://github.com/lhy1024)のメモリ消費を削減

-   TiFlash

    -   物理ファイルの数を減らすために新しい DTFile 形式バージョン[`storage.format_version = 5`](/tiflash/tiflash-configuration.md)をサポートします (実験的) [＃7595](https://github.com/pingcap/tiflash/issues/7595) @ [ホンユンヤン](https://github.com/hongyunyan)

-   ツール

    -   バックアップと復元 (BR)

        -   BRを使用して Azure Blob Storage にデータをバックアップする場合、サーバー側暗号化の暗号化スコープまたは暗号化キーのいずれかを指定できます[＃45025](https://github.com/pingcap/tidb/issues/45025) @ [リーヴルス](https://github.com/Leavrth)

    -   ティCDC

        -   オープンプロトコル出力のメッセージサイズを最適化して、 `UPDATE`イベント[＃9336](https://github.com/pingcap/tiflow/issues/9336) @ [3エースショーハンド](https://github.com/3AceShowHand)を送信するときに更新された列の値のみが含まれるようにします。
        -   ストレージシンクは、HEX 形式のデータの 16 進エンコードをサポートするようになり、AWS DMS 形式仕様[＃9373](https://github.com/pingcap/tiflow/issues/9373) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)と互換性があります。
        -   Kafka Sinkは、メッセージが大きすぎる場合に[ハンドルキーデータのみ送信](/ticdc/ticdc-sink-to-kafka.md#handle-messages-that-exceed-the-kafka-topic-limit)サポートし、メッセージのサイズを[＃9382](https://github.com/pingcap/tiflow/issues/9382) @ [3エースショーハンド](https://github.com/3AceShowHand)に縮小します。

## バグ修正 {#bug-fixes}

-   ティビ

    -   MySQL カーソルフェッチプロトコルを使用すると、結果セットのメモリ消費が`tidb_mem_quota_query`制限を超え、TiDB OOM が発生する可能性がある問題を修正しました。修正後、TiDB は結果セットを自動的にディスクに書き込み、メモリを解放します[＃43233](https://github.com/pingcap/tidb/issues/43233) @ [ヤンケオ](https://github.com/YangKeao)
    -   データ競合[＃45561](https://github.com/pingcap/tidb/issues/45561) @ [ゲンリキ](https://github.com/gengliqi)によって発生する TiDBpanic問題を修正
    -   `indexMerge`のクエリが[＃45279](https://github.com/pingcap/tidb/issues/45279) @ [翻訳者](https://github.com/xzhangxian1008)で強制終了されたときに発生するハングアップの問題を修正しました
    -   `tidb_enable_parallel_apply`が有効になっている場合に MPP モードでクエリ結果が正しくない問題を修正[＃45299](https://github.com/pingcap/tidb/issues/45299) @ [風の話し手](https://github.com/windtalker)
    -   PD時間[＃44822](https://github.com/pingcap/tidb/issues/44822) @ [ジグアン](https://github.com/zyguan)に突然の変化があった場合に`resolve lock`ハングする可能性がある問題を修正
    -   GC ロック解決ステップで一部の悲観的ロックが見逃される可能性がある問題を修正[＃45134](https://github.com/pingcap/tidb/issues/45134) @ [ミョンケミンタ](https://github.com/MyonKeminta)
    -   `ORDER BY`のクエリが動的プルーニングモード[＃45007](https://github.com/pingcap/tidb/issues/45007) @ [定義2014](https://github.com/Defined2014)で誤った結果を返す問題を修正しました
    -   `DEFAULT`列目の値[＃45136](https://github.com/pingcap/tidb/issues/45136) @ [定義2014](https://github.com/Defined2014)と同じ列に`AUTO_INCREMENT`指定できる問題を修正しました
    -   システムテーブル`INFORMATION_SCHEMA.TIKV_REGION_STATUS`をクエリすると、場合によっては誤った結果が返される問題を修正しました[＃45531](https://github.com/pingcap/tidb/issues/45531) @ [定義2014](https://github.com/Defined2014)
    -   一部のケースでパーティションテーブルのプルーニングが不正確になる問題を修正[＃42273](https://github.com/pingcap/tidb/issues/42273) @ [ジフハウス](https://github.com/jiyfhust)
    -   パーティションテーブル[＃42435](https://github.com/pingcap/tidb/issues/42435) @ [L-メープル](https://github.com/L-maple)のパーティションを切り捨てるときにグローバルインデックスがクリアされない問題を修正しました。
    -   1 つの TiDB ノード[＃45022](https://github.com/pingcap/tidb/issues/45022) @ [lcwangchao](https://github.com/lcwangchao)で障害が発生した後、他の TiDB ノードが TTL タスクを引き継がない問題を修正しました。
    -   TTLが[＃45510](https://github.com/pingcap/tidb/issues/45510) @ [lcwangchao](https://github.com/lcwangchao)で実行されているときのメモリリークの問題を修正
    -   パーティションテーブル[＃44966](https://github.com/pingcap/tidb/issues/44966) @ [リリンハイ](https://github.com/lilinghai)にデータを挿入する際の不正確なエラーメッセージの問題を修正
    -   `INFORMATION_SCHEMA.TIFLASH_REPLICA`テーブル[＃7795](https://github.com/pingcap/tiflash/issues/7795) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)の読み取り権限の問題を修正
    -   間違ったパーティションテーブル名[＃44967](https://github.com/pingcap/tidb/issues/44967) @ [リバー2000i](https://github.com/River2000i)を使用するとエラーが発生する問題を修正
    -   `tidb_enable_dist_task`が有効になっている場合にインデックスの作成が停止する問題を修正[＃44440](https://github.com/pingcap/tidb/issues/44440) @ [タンジェンタ](https://github.com/tangenta)
    -   BR [＃44716](https://github.com/pingcap/tidb/issues/44716) @ [天菜まお](https://github.com/tiancaiamao)使用して`AUTO_ID_CACHE=1`テーブルを復元するときに発生する`duplicate entry`エラーを修正します。
    -   `TRUNCATE TABLE`実行に費やされた時間が`ADMIN SHOW DDL JOBS` [＃44785](https://github.com/pingcap/tidb/issues/44785) @ [タンジェンタ](https://github.com/tangenta)に表示されるタスク実行時間と一致しない問題を修正しました
    -   メタデータの読み取りに 1 つの DDL リース[＃45176](https://github.com/pingcap/tidb/issues/45176) @ [ジムララ](https://github.com/zimulala)よりも長い時間がかかる場合に TiDB のアップグレードが停止する問題を修正しました。
    -   ステートメント内の`n`負の数[＃44786](https://github.com/pingcap/tidb/issues/44786) @ [xhebox](https://github.com/xhebox)の場合、ステートメント`SELECT CAST(n AS CHAR)`のクエリ結果が正しくない問題を修正しました。
    -   `tidb_opt_agg_push_down`が有効になっている場合にクエリが誤った結果を返す可能性がある問題を修正[＃44795](https://github.com/pingcap/tidb/issues/44795) @ [アイリンキッド](https://github.com/AilinKid)
    -   `current_date()`のクエリがプラン キャッシュ[＃45086](https://github.com/pingcap/tidb/issues/45086) @ [qw4990](https://github.com/qw4990)を使用した場合に誤った結果が発生する問題を修正しました。

-   ティクヴ

    -   GC 中にデータを読み取ると、まれに TiKVpanicが発生する可能性がある問題を修正[＃15109](https://github.com/tikv/tikv/issues/15109) @ [ミョンケミンタ](https://github.com/MyonKeminta)

-   PD

    -   PD を再起動すると`default`リソース グループが[＃6787](https://github.com/tikv/pd/issues/6787) @ [栄光](https://github.com/glorv)で再初期化される可能性がある問題を修正しました。
    -   etcd がすでに起動しているがクライアントがまだ接続していない場合、クライアントを呼び出すと PD がpanicになる可能性がある問題を修正しました[＃6860](https://github.com/tikv/pd/issues/6860) @ [ヒューシャープ](https://github.com/HuSharp)
    -   リージョンの`health-check`出力が、リージョンID [＃6560](https://github.com/tikv/pd/issues/6560) @ [じゃがいも](https://github.com/JmPotato)をクエリして返されるリージョン情報と一致しない問題を修正しました。
    -   `unsafe recovery`で不合格になった学習者のピアが`auto-detect`モード[＃6690](https://github.com/tikv/pd/issues/6690) @ [v01dスター](https://github.com/v01dstar)で無視される問題を修正
    -   配置ルールがルール[＃6662](https://github.com/tikv/pd/issues/6662) @ [rleungx](https://github.com/rleungx)を満たさないTiFlash学習者を選択する問題を修正しました
    -   ルール チェッカーがピア[＃6559](https://github.com/tikv/pd/issues/6559) @ [ノルーシュ](https://github.com/nolouch)を選択した場合に、不健全なピアを削除できない問題を修正しました。

-   TiFlash

    -   デッドロック[＃7758](https://github.com/pingcap/tiflash/issues/7758) @ [ホンユンヤン](https://github.com/hongyunyan)によりTiFlash がパーティション テーブルを正常に複製できない問題を修正
    -   `INFORMATION_SCHEMA.TIFLASH_REPLICA`システム テーブルに、ユーザーがアクセスする権限を持たないテーブルが含まれている問題を修正[＃7795](https://github.com/pingcap/tiflash/issues/7795) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)
    -   同じ MPP タスク内に複数の HashAgg 演算子がある場合、MPP タスクのコンパイルに非常に長い時間がかかり、クエリのパフォーマンスに重大な影響を与える可能性がある問題を修正しました[＃7810](https://github.com/pingcap/tiflash/issues/7810) @ [シーライズ](https://github.com/SeaRise)

-   ツール

    -   ティCDC

        -   PD [＃9294](https://github.com/pingcap/tiflow/issues/9294) @ [アズドンメン](https://github.com/asddongmen)が一時的に利用できないために変更フィードが失敗する問題を修正しました
        -   一部の TiCDC ノードがネットワークから分離されている場合に発生する可能性のあるデータの不整合の問題を修正[＃9344](https://github.com/pingcap/tiflow/issues/9344) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)
        -   Kafka Sink がエラーに遭遇すると、changefeed の進行が無期限にブロックされる可能性がある問題を修正しました[＃9309](https://github.com/pingcap/tiflow/issues/9309) @ [ヒック](https://github.com/hicqu)
        -   TiCDC ノードのステータスが[＃9354](https://github.com/pingcap/tiflow/issues/9354) @ [スドジ](https://github.com/sdojjy)に変化したときに発生する可能性のあるpanic問題を修正しました。
        -   デフォルトの`ENUM`値[＃9259](https://github.com/pingcap/tiflow/issues/9259) @ [3エースショーハンド](https://github.com/3AceShowHand)のエンコード エラーを修正

    -   TiDB Lightning

        -   TiDB Lightning がインポートを完了した後にチェックサムを実行すると SSL エラーが発生する可能性がある問題を修正[＃45462](https://github.com/pingcap/tidb/issues/45462) @ [D3ハンター](https://github.com/D3Hunter)
        -   論理インポート モードで、インポート中に下流のテーブルを削除すると、 TiDB Lightningメタデータが時間[＃44614](https://github.com/pingcap/tidb/issues/44614) @ [ダシュン](https://github.com/dsdashun)で更新されない可能性がある問題を修正しました。

## 寄稿者 {#contributors}

TiDB コミュニティの以下の貢献者に感謝いたします。

-   [チャールズ・ジェン44](https://github.com/charleszheng44)
-   [ディサム](https://github.com/dhysum)
-   [ハイユクス](https://github.com/haiyux)
-   [江華](https://github.com/Jiang-Hua)
-   [ジル](https://github.com/Jille)
-   [ジフハウス](https://github.com/jiyfhust)
-   [krishnaduttパンチャグヌラ](https://github.com/krishnaduttPanchagnula)
-   [L-メープル](https://github.com/L-maple)
-   [ピンとb](https://github.com/pingandb)
-   [テストウィル](https://github.com/testwill)
-   [ティソンクン](https://github.com/tisonkun)
-   [翻訳者](https://github.com/xuyifangreeneyes)
-   [ヤムチャイナ](https://github.com/yumchina)
