---
title: TiDB 7.3.0 Release Notes
summary: TiDB 7.3.0 の新機能、互換性の変更点、改善点、およびバグ修正についてご確認ください。
---

# TiDB 7.3.0 リリースノート {#tidb-7-3-0-release-notes}

発売日：2023年8月14日

TiDB バージョン: 7.3.0

クイックアクセス: [クイックスタート](https://docs-archive.pingcap.com/tidb/v7.3/quick-start-with-tidb)

7.3.0では、以下の主要機能が導入されています。さらに、7.3.0には、TiDBサーバーおよびTiFlashにおけるクエリの安定性を向上させるための一連の機能強化（[機能の詳細](#feature-details)セクションで説明）も含まれています。これらの機能強化は、より細かなものであり、ユーザーに直接影響を与えるものではないため、以下の表には含まれていません。

<table><thead><tr><th>カテゴリ</th><th>特徴</th><th>説明</th></tr></thead><tbody><tr><td>拡張性とパフォーマンス</td><td>TiDB Lightningは<a href="https://docs-archive.pingcap.com/tidb/v7.3/partitioned-raft-kv">パーティション化されたRaft KV</a>をサポートしています（実験的）。</td><td> TiDB Lightningは、アーキテクチャの近々の一般提供開始の一環として、新しいパーティション化されたRaft KVアーキテクチャをサポートするようになりました。</td></tr><tr><td rowspan="2">信頼性と可用性</td><td><a href="https://docs-archive.pingcap.com/tidb/v7.3/tidb-lightning-physical-import-mode-usage#conflict-detection">データインポート時に自動的な競合検出と解決機能を追加する</a></td><td>TiDB Lightningの物理インポートモードでは、競合検出の新しいバージョンがサポートされています。このバージョンでは、競合が発生した場合に、競合データを置換（ <code>replace</code> ）または無視（ <code>ignore</code> ）するセマンティクスが実装されています。競合データを自動的に処理し、競合解決のパフォーマンスを向上させます。</td></tr><tr><td> <a href="https://docs-archive.pingcap.com/tidb/v7.3/tidb-resource-control#query-watch-parameters">暴走クエリの手動管理</a>（実験的）</td><td>クエリの実行に予想以上に時間がかかる場合があります。新しいリソース グループの監視リストを使用すると、クエリをより効果的に管理し、優先順位を下げたり、強制終了したりできます。この機能により、オペレーターは対象のクエリを正確な SQL テキスト、SQL ダイジェスト、またはプラン ダイジェストでマークし、リソース グループ レベルでクエリを処理できるため、予期しない大規模なクエリがクラスターに及ぼす潜在的な影響をより詳細に制御できます。</td></tr><tr><td> SQL</td><td><a href="https://docs-archive.pingcap.com/tidb/v7.3/optimizer-hints">クエリプランナーにオプティマイザヒントを追加することで、クエリの安定性に対するオペレーターの制御を強化します。</a></td><td>追加されたヒント: <code>NO_INDEX_JOIN()</code> 、 <code>NO_MERGE_JOIN()</code> 、 <code>NO_INDEX_MERGE_JOIN()</code> 、 <code>NO_HASH_JOIN()</code> 、 <code>NO_INDEX_HASH_JOIN()</code></td></tr><tr><td>データベースの運用と可観測性</td><td><a href="https://docs-archive.pingcap.com/tidb/v7.3/sql-statement-show-analyze-status">統計収集タスクの進捗状況を表示します。</a></td><td> <code>SHOW ANALYZE STATUS</code>ステートメントまたは<code>mysql.analyze_jobs</code>システム テーブルを使用して、 <code>ANALYZE</code>タスクの進行状況を表示することをサポートします。</td></tr></tbody></table>

## 機能の詳細 {#feature-details}

### パフォーマンス {#performance}

-   TiFlashはレプリカ選択戦略をサポートしています [#44106](https://github.com/pingcap/tidb/issues/44106) @[XuHuaiyu](https://github.com/XuHuaiyu)

    バージョン 7.3.0 より前のTiFlashでは、パフォーマンスを最大化するために、すべてのノードのレプリカを使用してデータ スキャンと MPP 計算を行っていました。バージョン 7.3.0 以降では、 TiFlash はレプリカ選択戦略を導入し、システム変数[`tiflash_replica_read`](/system-variables.md#tiflash_replica_read-new-in-v730)を使用して設定できるようになりました。この戦略では、ノードの[ゾーン属性](/schedule-replicas-by-topology-labels.md#optional-configure-labels-for-tidb)に基づいて特定のレプリカを選択し、データ スキャンと MPP 計算のために特定のノードをスケジュールすることができます。

    複数のデータセンターに展開され、各データセンターに完全なTiFlashデータレプリカが存在するクラスターの場合、この戦略を設定して、現在のデータセンターのTiFlashレプリカのみを選択することができます。これにより、データスキャンとMPP計算は現在のデータセンター内のTiFlashノードでのみ実行されるため、データセンター間での過剰なネットワークデータ転送を回避できます。

    詳細については、 [ドキュメント](/system-variables.md#tiflash_replica_read-new-in-v730)を参照してください。

-   TiFlash はノード内のランタイム フィルターをサポート [#40220](https://github.com/pingcap/tidb/issues/40220) @[elsa0520](https://github.com/elsa0520)

    ランタイムフィルタは、クエリプランニングフェーズ中に生成される**動的な述語**です。テーブル結合処理において、これらの動的な述語は結合条件を満たさない行を効果的にフィルタリングし、スキャン時間とネットワークオーバーヘッドを削減し、テーブル結合の効率を向上させます。TiFlashはv7.3.0以降、ノード内でランタイムフィルタをサポートし、分析クエリの全体的なパフォーマンスを向上させています。一部のTPC-DSワークロードでは、パフォーマンスが10%から50%向上する可能性があります。

    この機能はv7.3.0ではデフォルトで無効になっています。この機能を有効にするには、システム変数[`tidb_runtime_filter_mode`](/system-variables.md#tidb_runtime_filter_mode-new-in-v720) `LOCAL`に設定してください。

    詳細については、[ドキュメント](/runtime-filter.md)を参照してください。

-   TiFlashは共通テーブル式（CTE）の実行をサポートします（実験的） [#43333](https://github.com/pingcap/tidb/issues/43333) @[winoros](https://github.com/winoros)

    バージョン7.3.0より前のTiFlashのMPPエンジンは、デフォルトではCTEを含むクエリを実行できません。MPPフレームワーク内で最高の実行パフォーマンスを実現するには、システム変数[`tidb_opt_force_inline_cte`](/system-variables.md#tidb_opt_force_inline_cte-new-in-v630)を使用してCTEのインライン化を強制する必要があります。

    バージョン7.3.0以降、TiFlashのMPPエンジンは、CTEをインライン化せずにクエリを実行できるようになり、MPPフレームワーク内での最適なクエリ実行が可能になりました。TPC-DSベンチマークテストでは、CTEをインライン化する場合と比較して、この機能によりCTEを含むクエリの全体的な実行速度が20%向上することが確認されています。

    この機能は実験的であり、デフォルトでは無効になっています。システム変数[`tidb_opt_enable_mpp_shared_cte_execution`](/system-variables.md#tidb_opt_enable_mpp_shared_cte_execution-new-in-v720)によって制御されます。

### 信頼性 {#reliability}

-   新しいオプティマイザヒントを追加 [#45520](https://github.com/pingcap/tidb/issues/45520) @[qw4990](https://github.com/qw4990)

    TiDB v7.3.0では、テーブル間の結合方法を制御するための新しいオプティマイザヒントがいくつか導入されています。これには以下が含まれます。

    -   [`NO_MERGE_JOIN()`](/optimizer-hints.md#no_merge_joint1_name--tl_name-)は、マージ結合以外の結合方法を選択します。
    -   [`NO_INDEX_JOIN()`](/optimizer-hints.md#no_index_joint1_name--tl_name-)は、インデックスネストループ結合以外の結合方法を選択します。
    -   [`NO_INDEX_MERGE_JOIN()`](/optimizer-hints.md#no_index_merge_joint1_name--tl_name-)は、インデックスネストループマージ結合以外の結合方法を選択します。
    -   [`NO_HASH_JOIN()`](/optimizer-hints.md#no_hash_joint1_name--tl_name-)は、ハッシュ結合以外の結合方法を選択します。
    -   [`NO_INDEX_HASH_JOIN()`](/optimizer-hints.md#no_index_hash_joint1_name--tl_name-)は[インデックスネストループハッシュ結合](/optimizer-hints.md#inl_hash_join)以外の結合方法を選択します。

    詳細については、[ドキュメント](/optimizer-hints.md)を参照してください。

-   予想以上にリソースを使用するクエリを手動でマークする (実験的) [#43691](https://github.com/pingcap/tidb/issues/43691) @[Connor1996](https://github.com/Connor1996) @[CabinfeverB](https://github.com/CabinfeverB)

    TiDB v7.2.0では、想定以上のリソースを使用するクエリ（暴走クエリ）を自動的にダウングレードまたはキャンセルすることで、TiDBが自動的に管理します。しかし、実際の運用では、ルールだけではすべてのケースに対応できません。そこで、TiDB v7.3.0では、暴走クエリを手動でマークする機能が導入されました。新しいコマンド[`QUERY WATCH`](/sql-statements/sql-statement-query-watch.md)を使用すると、SQLテキスト、SQLダイジェスト、または実行プランに基づいて暴走クエリをマークでき、マークされた暴走クエリをダウングレードまたはキャンセルできます。

    この機能は、データベースにおける突発的なパフォーマンス問題に対する効果的な介入手段を提供します。クエリによって引き起こされるパフォーマンス問題の場合、根本原因を特定する前に、この機能によって全体的なパフォーマンスへの影響を迅速に軽減し、システムサービスの品質を向上させることができます。

    詳細については、 [ドキュメント](/tidb-resource-control-runaway-queries.md#query-watch-parameters)を参照してください。

### SQL {#sql}

-   リストとリスト列のパーティションテーブルはデフォルトのパーティションをサポートします [#20679](https://github.com/pingcap/tidb/issues/20679) @[mjonss](https://github.com/mjonss)@[bb7133](https://github.com/bb7133)

    バージョン 7.3.0 より前では、 `INSERT`ステートメントを使用してリストまたはリスト COLUMNSパーティションテーブルにデータを挿入する場合、データはテーブルの指定されたパーティション条件を満たす必要があります。挿入するデータがこれらの条件のいずれにも満たない場合、ステートメントの実行が失敗するか、条件を満たさないデータは無視されます。

    バージョン7.3.0以降、ListおよびList COLUMNSパーティションテーブルはデフォルトパーティションをサポートします。デフォルトパーティションが作成された後、挿入するデータがパーティション条件を満たさない場合、そのデータはデフォルトパーティションに書き込まれます。この機能により、ListおよびList COLUMNS パーティショニングの使いやすさが向上し、 `INSERT`ステートメントの実行失敗や、パーティション条件を満たさないデータによるデータの無視を防ぐことができます。

    この機能は、MySQL構文に対するTiDBの拡張機能であることに注意してください。デフォルトのパーティションを持つパーティションテーブルの場合、テーブル内のデータをMySQLに直接レプリケートすることはできません。

    詳細については、[ドキュメント](/partitioned-table.md#list-partitioning)を参照してください。

### 可観測性 {#observability}

-   統計収集の進行状況を表示 [#44033](https://github.com/pingcap/tidb/issues/44033) @[hawkingrei](https://github.com/hawkingrei)

    大規模テーブルの統計情報を収集するには、多くの場合、長い時間がかかります。以前のバージョンでは、統計情報の収集の進行状況を確認できなかったため、完了時間を予測できませんでした。TiDB v7.3.0 では、統計情報の収集の進行状況を表示する機能が導入されました。システムテーブル`mysql.analyze_jobs`または`SHOW ANALYZE STATUS`を使用して、各サブタスクの全体的なワークロード、現在の進行状況、および推定完了時間を確認できます。大規模なデータインポートや SQL パフォーマンス最適化などのシナリオでは、この機能によりタスク全体の進行状況を把握しやすくなり、ユーザーエクスペリエンスが向上します。

    詳細については、 [ドキュメント](/sql-statements/sql-statement-show-analyze-status.md)を参照してください。

-   Plan Replayer は履歴統計のエクスポートをサポート [#45038](https://github.com/pingcap/tidb/issues/45038) @[time-and-fate](https://github.com/time-and-fate)

    バージョン7.3.0以降、 [`dump with stats as of timestamp`](/sql-plan-replayer.md)が新たに追加されたため、Plan Replayerを使用して、指定した時点におけるSQL関連オブジェクトの統計情報をエクスポートできます。実行プランの問題を診断する際に、履歴統計情報を正確に取得することで、問題発生時に実行プランがどのように生成されたかをより詳細に分析できます。これにより、問題の根本原因を特定しやすくなり、実行プランの問題診断の効率が大幅に向上します。

    詳細については、[ドキュメント](/sql-plan-replayer.md)を参照してください。

### データ移行 {#data-migration}

-   TiDB Lightning で競合データ検出および処理戦略の新バージョンが導入されました [#41629](https://github.com/pingcap/tidb/issues/41629) @[lance6716](https://github.com/lance6716)

    以前のバージョンでは、 TiDB Lightning は論理インポート モードと物理インポート モードに対して異なる競合検出および処理方法を使用しており、設定が複雑でユーザーが理解しにくいものでした。さらに、物理インポート モードでは`replace`または`ignore`戦略を使用して競合を処理することができませんでした。v7.3.0 以降、 TiDB Lightning は論理インポート モードと物理インポート モードの両方に対して統一された競合検出および処理戦略を導入しました。競合が発生した場合、競合するデータをエラーとして報告 ( `error` )、置換 ( `replace` )、または無視 ( `ignore` ) するかを選択できます。競合レコードの数を制限することもでき、たとえば、指定した数の競合レコードを処理した後、タスクが中断されて終了します。さらに、このシステムはトラブルシューティングのために矛盾するデータを記録することもできます。

    競合が多数含まれるインポートデータの場合、パフォーマンス向上のため、競合検出および処理戦略の新しいバージョンを使用することをお勧めします。ラボ環境では、新しいバージョンの戦略は、競合検出および処理のパフォーマンスを旧バージョンよりも最大3倍高速化できます。このパフォーマンス値は参考値です。実際のパフォーマンスは、構成、テーブル構造、および競合データの割合によって異なる場合があります。なお、競合戦略の新バージョンと旧バージョンは同時に使用できません。旧バージョンの競合検出および処理戦略は、将来的に廃止される予定です。

    詳細については、 [ドキュメント](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#conflict-detection)を参照してください。

-   TiDB Lightning がパーティション化されたRaft KV をサポート (実験的) [#14916](https://github.com/tikv/tikv/issues/14916) @[GMHDBJD](https://github.com/GMHDBJD)

    TiDB Lightningがパーティション化されたRaft KVをサポートするようになりました。この機能により、TiDB Lightningのデータインポートパフォーマンスが向上します。

-   TiDB Lightning は、より多くの診断ログを出力することでトラブルシューティングを強化する新しいパラメータ`enable-diagnose-log`を導入しました [#45497](https://github.com/pingcap/tidb/issues/45497) @[D3Hunter](https://github.com/D3Hunter)

    デフォルトでは、この機能は無効になっており、 TiDB Lightning は`lightning/main`を含むログのみを出力。有効にすると、 TiDB Lightning は`client-go`および`tidb`に関連する問題の診断に役立つように、すべてのパッケージ`client-go`および`tidb`を含む) のログを出力します。

    詳細については、 [ドキュメント](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-global)を参照してください。

## 互換性の変更 {#compatibility-changes}

> **注記：**
>
> このセクションでは、バージョン7.2.0から最新バージョン（7.3.0）にアップグレードする際に知っておくべき互換性の変更点について説明します。バージョン7.1.0以前のバージョンから最新バージョンにアップグレードする場合は、中間バージョンで導入された互換性の変更点も確認する必要があるかもしれません。

### 動作の変更 {#behavior-changes}

-   TiDB

    -   MPP はTiFlashエンジンが提供する分散コンピューティング フレームワークであり、ノード間でのデータ交換を可能にし、高性能かつ高スループットの SQL アルゴリズムを提供します。他のプロトコルと比較して、MPP プロトコルはより成熟しており、より優れたタスクおよびリソース管理を提供できます。v7.3.0 以降、TiDB が計算タスクをTiFlashにプッシュする場合、オプティマイザはデフォルトで MPP プロトコルを使用した実行プランのみを生成します。tidb_allow_mpp が`OFF`に設定されている場合、TiDB をアップグレードした後にクエリでエラーが発生する可能性があります。 [`tidb_allow_mpp`](/system-variables.md#tidb_allow_mpp-new-in-v50)前に`tidb_allow_mpp`の値を確認し、 `ON`に設定することをお勧めします。コスト見積もりに基づいて実行プランを生成するために、オプティマイザがCop、BatchCop、およびMPPプロトコルのいずれかを選択する必要がある場合は、 [`tidb_allow_tiflash_cop`](/system-variables.md#tidb_allow_tiflash_cop-new-in-v730)変数を`ON`に設定できます。

-   Backup & Restore (BR)

    -   BR は、完全なデータ復元を実行する前に、空のクラスタのチェックを追加します。デフォルトでは、空でないクラスタへのデータ復元は許可されていません。復元を強制する場合は、 `--filter`オプションを使用して、データを復元する対応するテーブル名を指定できます。

-   TiDB Lightning

    -   `tikv-importer.on-duplicate`は非推奨となり、 [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)に置き換えられました。
    -   TiDB Lightning が移行タスクを停止する前に許容できる非致命的なエラーの最大数を制御する`max-error`パラメータは、インポートデータの競合を制限しなくなりました。代わりに、 [`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)パラメータが、許容できる競合レコードの最大数を制御するようになりました。

-   TiCDC

    -   KafkaシンクがAvroプロトコルを使用している場合、 `force-replicate`パラメータが`true`に設定されている場合、TiCDCはchangefeedを作成する際にエラーを報告します。
    -   `delete-only-output-handle-key-columns`と`force-replicate`パラメータ間に互換性がないため、両方のパラメータが有効になっている場合、TiCDC は変更フィードを作成する際にエラーを報告します。
    -   出力プロトコルがオープンプロトコルの場合、 `UPDATE`イベントは変更された列のみを出力します。

### システム変数 {#system-variables}

| 変数名                                                                                                                     | 変更の種類  | 説明                                                                           |
| ----------------------------------------------------------------------------------------------------------------------- | -------- | ---------------------------------------------------------------------------- |
| [`tidb_opt_enable_mpp_shared_cte_execution`](/system-variables.md#tidb_opt_enable_mpp_shared_cte_execution-new-in-v720) | 変更     | このシステム変数はバージョン7.3.0以降で有効になります。TiFlash MPPで非再帰的な共通テーブル式（CTE）を実行できるかどうかを制御します。 |
| [`tidb_allow_tiflash_cop`](/system-variables.md#tidb_allow_tiflash_cop-new-in-v730)                                     | 新しく追加された | このシステム変数は、TiDBが計算タスクをTiFlashにプッシュダウンする際に、実行プランを生成するためのプロトコルを選択するために使用されます。   |
| [`tidb_lock_unchanged_keys`](/system-variables.md#tidb_lock_unchanged_keys-new-in-v711-and-v730)                        | 新しく追加された | この変数は、特定のシナリオにおいて、トランザクションに関与しているものの、変更されていないキーをロックするかどうかを制御するために使用されます。     |
| [`tidb_opt_enable_non_eval_scalar_subquery`](/system-variables.md#tidb_opt_enable_non_eval_scalar_subquery-new-in-v730) | 新しく追加された | `EXPLAIN`ステートメントが、最適化段階で展開可能な定数サブクエリの実行を無効にするかどうかを制御します。                     |
| [`tidb_skip_missing_partition_stats`](/system-variables.md#tidb_skip_missing_partition_stats-new-in-v730)               | 新しく追加された | この変数は、パーティション統計情報が欠落している場合にグローバル統計情報を生成するかどうかを制御します。                         |
| [`tiflash_replica_read`](/system-variables.md#tiflash_replica_read-new-in-v730)                                         | 新しく追加された | クエリがTiFlashエンジンを必要とする場合に、 TiFlashレプリカを選択する戦略を制御します。                          |

### コンフィグレーションファイルパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーションパラメータ                                                                                                                                 | 変更の種類  | 説明                                                                                                                                                                                                                                                                                                                                                          |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB           | [`enable-32bits-connection-id`](/tidb-configuration-file.md#enable-32bits-connection-id-new-in-v730)                                            | 新しく追加された | 32ビット接続ID機能を有効にするかどうかを制御します。                                                                                                                                                                                                                                                                                                                                |
| TiDB           | [`in-mem-slow-query-recent-num`](/tidb-configuration-file.md#in-mem-slow-query-recent-num-new-in-v730)                                          | 新しく追加された | メモリにキャッシュされる、最近使用された低速クエリの数を制御します。                                                                                                                                                                                                                                                                                                                          |
| TiDB           | [`in-mem-slow-query-topn-num`](/tidb-configuration-file.md#in-mem-slow-query-topn-num-new-in-v730)                                              | 新しく追加された | メモリにキャッシュされる最も遅いクエリの数を制御します。                                                                                                                                                                                                                                                                                                                                |
| TiKV           | [`coprocessor.region-bucket-size`](/tikv-configuration-file.md#region-bucket-size-new-in-v610)                                                  | 変更     | デフォルト値を`96MiB`から`50MiB`に変更します。                                                                                                                                                                                                                                                                                                                              |
| TiKV           | [`raft-engine.format-version`](/tikv-configuration-file.md#format-version-new-in-v630)                                                          | 変更     | パーティション化されたRaft KV ( `storage.engine="partitioned-raft-kv"` ) を使用する場合、リボンフィルタが使用されます。そのため、TiKV はデフォルト値を`2`から`5`に変更します。                                                                                                                                                                                                                                      |
| TiKV           | [`raftdb.max-total-wal-size`](/tikv-configuration-file.md#max-total-wal-size-1)                                                                 | 変更     | パーティション化されたRaft KV ( `storage.engine="partitioned-raft-kv"` ) を使用する場合、TiKV は WAL の書き込みをスキップします。そのため、TiKV はデフォルト値を`"4GB"`から`1`に変更し、WAL が無効になるようにします。                                                                                                                                                                                                         |
| TiKV           | [`rocksdb.[defaultcf|writecf|lockcf].compaction-guard-min-output-file-size`](/tikv-configuration-file.md#compaction-guard-min-output-file-size) | 変更     | デフォルト値を`"1MB"`から`"8MB"`に変更し、大容量データ書き込み時に圧縮速度が書き込み速度に追いつかない問題を解決します。                                                                                                                                                                                                                                                                                         |
| TiKV           | [`rocksdb.[defaultcf|writecf|lockcf].format-version`](/tikv-configuration-file.md#format-version-new-in-v620)                                   | 変更     | パーティション化されたRaft KV ( `storage.engine="partitioned-raft-kv"` ) を使用する場合、リボンフィルタが使用されます。そのため、TiKV はデフォルト値を`2`から`5`に変更します。                                                                                                                                                                                                                                      |
| TiKV           | [`rocksdb.lockcf.write-buffer-size`](/tikv-configuration-file.md#write-buffer-size)                                                             | 変更     | パーティション化されたRaft KV ( `storage.engine="partitioned-raft-kv"` ) を使用する場合、lockcf の圧縮を高速化するために、TiKV はデフォルト値を`"32MB"`から`"4MB"`に変更します。                                                                                                                                                                                                                             |
| TiKV           | [`rocksdb.max-total-wal-size`](/tikv-configuration-file.md#max-total-wal-size)                                                                  | 変更     | パーティション化されたRaft KV ( `storage.engine="partitioned-raft-kv"` ) を使用する場合、TiKV は WAL の書き込みをスキップします。そのため、TiKV はデフォルト値を`"4GB"`から`1`に変更し、WAL が無効になるようにします。                                                                                                                                                                                                         |
| TiKV           | [`rocksdb.stats-dump-period`](/tikv-configuration-file.md#stats-dump-period)                                                                    | 変更     | パーティション化されたRaft KV ( `storage.engine="partitioned-raft-kv"` ) を使用する場合、冗長なログ印刷を無効にするには、デフォルト値を`"10m"`から`"0"`に変更します。                                                                                                                                                                                                                                          |
| TiKV           | [`rocksdb.write-buffer-limit`](/tikv-configuration-file.md#write-buffer-limit-new-in-v660)                                                      | 変更     | memtable のメモリオーバーヘッドを削減するため、 `storage.engine="raft-kv"`の場合、TiKV はデフォルト値をマシンのメモリの 25% から`0`に変更します。これは制限がないことを意味します。パーティション化されたRaft KV ( `storage.engine="partitioned-raft-kv"` ) を使用する場合、TiKV はデフォルト値をマシンのメモリの 25% から 20% に変更します。                                                                                                                            |
| TiKV           | [`storage.block-cache.capacity`](/tikv-configuration-file.md#capacity)                                                                          | 変更     | パーティション化されたRaft KV ( `storage.engine="partitioned-raft-kv"` ) を使用する場合、memtable のメモリオーバーヘッドを補償するために、TiKV はデフォルト値をシステムメモリ全体のサイズの 45% から 30% に変更します。                                                                                                                                                                                                           |
| TiFlash        | [`storage.format_version`](/tiflash/tiflash-configuration.md)                                                                                   | 変更     | より小さなファイルをマージすることで物理ファイルの数を削減する新しいDTFileフォーマット`format_version = 5`を導入します。このフォーマットは実験的であり、デフォルトでは有効になっていません。                                                                                                                                                                                                                                                 |
| TiDB Lightning | `tikv-importer.incremental-import`                                                                                                              | 削除済み     | TiDB Lightning の並列インポート パラメータ。増分インポート パラメータと混同されやすいため、このパラメータは`tikv-importer.parallel-import`に名称変更されました。ユーザーが古いパラメータ名を渡した場合、自動的に新しいパラメータ名に変換されます。                                                                                                                                                                                                           |
| TiDB Lightning | `tikv-importer.on-duplicate`                                                                                                                    | 非推奨      | 論理インポートモードで競合するレコードを挿入しようとしたときに実行するアクションを制御します。v7.3.0 以降、このパラメーターは[`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)に置き換えられました。                                                                                                                                                                                     |
| TiDB Lightning | [`conflict.max-record-rows`](/tidb-lightning/tidb-lightning-configuration.md)                                                                   | 新しく追加された | 競合するデータを処理するための新しい戦略です。 `conflict_records`テーブルの最大行数を制御します。デフォルト値は 100 です。                                                                                                                                                                                                                                                                                   |
| TiDB Lightning | [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md)                                                                          | 新しく追加された | 競合するデータを処理するための新しい戦略。次のオプションが含まれます: &quot;&quot; (TiDB Lightning は競合するデータを検出して処理しません)、 `error` (インポートされたデータで主キーまたは一意キーの競合が検出された場合、インポートを終了してエラーを報告します)、 `replace` (競合する主キーまたは一意キーを持つデータに遭遇した場合、新しいデータが保持され、古いデータが上書きされます)、 `ignore` (競合する主キーまたは一意キーを持つデータに遭遇した場合、古いデータが保持され、新しいデータは無視されます)。デフォルト値は &quot;&quot; です。つまり、 TiDB Lightning は競合するデータを検出して処理しません。 |
| TiDB Lightning | [`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md)                                                                         | 新しく追加された | 競合するデータの上限を制御します。 `conflict.strategy="error"`の場合、デフォルト値は`0`です。 `conflict.strategy="replace"`または`conflict.strategy="ignore"`の場合、maxint として設定できます。                                                                                                                                                                                                            |
| TiDB Lightning | [`enable-diagnose-logs`](/tidb-lightning/tidb-lightning-configuration.md)                                                                       | 新しく追加された | 診断ログを有効にするかどうかを制御します。デフォルト値は`false`で、インポートに関連するログのみが出力され、他の依存コンポーネントのログは出力されません。これを`true`に設定すると、インポートプロセスと他の依存コンポーネントの両方のログが出力され、GRPC デバッグが有効になり、診断に使用できます。                                                                                                                                                                                                 |
| TiDB Lightning | [`tikv-importer.parallel-import`](/tidb-lightning/tidb-lightning-configuration.md)                                                              | 新しく追加された | TiDB Lightning の並列インポート パラメータです。既存の`tikv-importer.incremental-import`パラメータに代わるもので、既存のパラメータは増分インポート パラメータと誤解されて誤用される可能性がありました。                                                                                                                                                                                                                               |
| BR             | `azblob.encryption-scope`                                                                                                                       | 新しく追加された | BRはAzure Blob Storageの暗号化スコープをサポートします。                                                                                                                                                                                                                                                                                                                      |
| BR             | `azblob.encryption-key`                                                                                                                         | 新しく追加された | BRはAzure Blob Storageの暗号化キーをサポートします。                                                                                                                                                                                                                                                                                                                        |
| TiCDC          | [`large-message-handle-option`](/ticdc/ticdc-sink-to-kafka.md#handle-messages-that-exceed-the-kafka-topic-limit)                                | 新しく追加された | デフォルトでは空になっています。つまり、メッセージサイズが Kafka トピックの制限を超えると、changefeed は失敗します。この設定を`"handle-key-only"`に設定すると、メッセージがサイズ制限を超えた場合、ハンドルキーのみが送信され、メッセージサイズが縮小されます。縮小されたメッセージでも制限を超える場合は、changefeed は失敗します。                                                                                                                                                                  |
| TiCDC          | [`sink.csv.binary-encoding-method`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)                                      | 新しく追加された | バイナリデータのエンコード方式。 `'base64'`または`'hex'`を指定できます。デフォルト値は`'base64'`です。                                                                                                                                                                                                                                                                                           |

### システムテーブル {#system-tables}

-   内部タイマーのメタデータを格納するための新しいシステムテーブル`mysql.tidb_timers`を追加します。

## 非推奨機能 {#deprecated-features}

-   TiDB

    -   統計情報用の[`Fast Analyze`](/system-variables.md#tidb_enable_fast_analyze)機能（実験的）は、バージョン7.5.0で廃止されます。
    -   統計の[増分収集](https://docs-archive.pingcap.com/tidb/v7.3/statistics#incremental-collection)機能は v7.5.0 で非推奨になります。

## 改善点 {#improvements}

-   TiDB

    -   `EXPLAIN`ステートメントが最適化フェーズ中にサブクエリを事前に実行するかどうかを制御するための新しいシステム変数[`tidb_opt_enable_non_eval_scalar_subquery`](/system-variables.md#tidb_opt_enable_non_eval_scalar_subquery-new-in-v730)を導入します [#22076](https://github.com/pingcap/tidb/issues/22076) @[winoros](https://github.com/winoros)
    -   [グローバルキル](/tidb-configuration-file.md#enable-global-kill-new-in-v610)が有効な場合、 <kbd>Ctrl+C</kbd>を押すと現在のセッションを終了できます [#8854](https://github.com/pingcap/tidb/issues/8854) @[pingyu](https://github.com/pingyu)
    -   `IS_FREE_LOCK()`および`IS_USED_LOCK()`のロック関数をサポートする [#44493](https://github.com/pingcap/tidb/issues/44493) @[dveeden](https://github.com/dveeden)
    -   ディスクからダンプされたチャンクを読み取るパフォーマンスを最適化 [#45125](https://github.com/pingcap/tidb/issues/45125) @[YangKeao](https://github.com/YangKeao)
    -   Optimizer Fix Controls を使用してインデックス結合の内部テーブルの過大評価問題を最適化する [#44855](https://github.com/pingcap/tidb/issues/44855) @[time-and-fate](https://github.com/time-and-fate)

-   TiKV

    -   `Max gap of safe-ts`および`Min safe ts region`メトリックを追加し、 `tikv-ctl get-region-read-progress`コマンドを導入して、 resolved-tsおよび safe-ts の状態をより適切に監視および診断します [#15082](https://github.com/tikv/tikv/issues/15082) @[ekexium](https://github.com/ekexium)

-   PD

    -   Swaggerサーバーが有効になっていない場合、デフォルトで Swagger API のブロックをサポート [#6786](https://github.com/tikv/pd/issues/6786) @[bufferflies](https://github.com/bufferflies)
    -   etcdの高可用性を向上させる[#6554](https://github.com/tikv/pd/issues/6554) [#6442](https://github.com/tikv/pd/issues/6442) @[lhy1024](https://github.com/lhy1024)
    -   `GetRegions`リクエストのメモリ消費量を削減する [#6835](https://github.com/tikv/pd/issues/6835) @[lhy1024](https://github.com/lhy1024)

-   TiFlash

    -   新しい DTFile フォーマット バージョン[`storage.format_version = 5`](/tiflash/tiflash-configuration.md)をサポートして物理ファイルの数を削減します (実験的) [#7595](https://github.com/pingcap/tiflash/issues/7595) @[hongyunyan](https://github.com/hongyunyan)

-   ツール

    -   Backup & Restore (BR)

        -   BRを使用して Azure Blob Storage にデータをバックアップする場合、サーバー側暗号化の暗号化スコープまたは暗号化キーを指定できます [#45025](https://github.com/pingcap/tidb/issues/45025) @[Leavrth](https://github.com/Leavrth)

    -   TiCDC

        -   `UPDATE`イベント送信時に更新された列値のみが含まれるように、Open Protocol 出力のメッセージ サイズを最適化します [#9336](https://github.com/pingcap/tiflow/issues/9336) @[3AceShowHand](https://github.com/3AceShowHand)ハンド
        -   Storage Sink が HEX 形式のデータの 16 進数エンコーディングをサポートするようになり、AWS DMS フォーマット仕様との互換性が確保されました [#9373](https://github.com/pingcap/tiflow/issues/9373) @[CharlesCheung96](https://github.com/CharlesCheung96)
        -   Kafka Sink は、メッセージが大きすぎる場合に[ハンドルキーデータのみを送信する](/ticdc/ticdc-sink-to-kafka.md#handle-messages-that-exceed-the-kafka-topic-limit)をサポートし、メッセージのサイズを削減します [#9382](https://github.com/pingcap/tiflow/issues/9382) @[3AceShowHand](https://github.com/3AceShowHand)

## バグ修正 {#bug-fixes}

-   TiDB

    -   MySQL Cursor Fetch プロトコルを使用した場合に、結果セットのメモリ消費量が`tidb_mem_quota_query`制限を超え、TiDB のメモリ不足が発生する問題を修正しました。修正後、TiDB は自動的に結果セットをディスクに書き込み、メモリを解放します。 [#43233](https://github.com/pingcap/tidb/issues/43233) @[YangKeao](https://github.com/YangKeao)
    -   データ競合によって引き起こされる TiDBpanic問題を修正 [#45561](https://github.com/pingcap/tidb/issues/45561) @[gengliqi](https://github.com/gengliqi)
    -   `indexMerge`を含むクエリが強制終了されたときに発生するハングアップ問題を修正 [#45279](https://github.com/pingcap/tidb/issues/45279) @[xzhangxian1008](https://github.com/xzhangxian1008)
    -   `tidb_enable_parallel_apply`が有効な場合、MPP モードでのクエリ結果が正しくない問題を修正 [#45299](https://github.com/pingcap/tidb/issues/45299) @[windtalker](https://github.com/windtalker)
    -   `resolve lock` PD時間の急激な変化時にハングアップする可能性がある問題を修正 [#44822](https://github.com/pingcap/tidb/issues/44822) @[zyguan](https://github.com/zyguan)
    -   GC Resolve Locks ステップで一部の悲観的ロックが見落とされる可能性がある問題を修正 [#45134](https://github.com/pingcap/tidb/issues/45134) @[MyonKeminta](https://github.com/MyonKeminta)
    -   `ORDER BY`を含むクエリが動的プルーニングモードで誤った結果を返す問題を修正 [#45007](https://github.com/pingcap/tidb/issues/45007) @[Defined2014](https://github.com/Defined2014)
    -   `AUTO_INCREMENT`が`DEFAULT`列の値と同じ列に指定できてしまう問題を修正しました [#45136](https://github.com/pingcap/tidb/issues/45136) @[Defined2014](https://github.com/Defined2014)
    -   システムテーブル`INFORMATION_SCHEMA.TIKV_REGION_STATUS`をクエリした際に、場合によっては誤った結果が返される問題を修正しました [#45531](https://github.com/pingcap/tidb/issues/45531) @[Defined2014](https://github.com/Defined2014)
    -   一部のケースでパーティションテーブルのプルーニングが正しく行われない問題を修正 [#42273](https://github.com/pingcap/tidb/issues/42273) @[jiyfhust](https://github.com/jiyfhust)
    -   パーティションテーブルのパーティションを切り捨てる際にグローバルインデックスがクリアされない問題を修正 [#42435](https://github.com/pingcap/tidb/issues/42435) @[L-maple](https://github.com/L-maple)
    -   TiDBノードの障害発生後、他のTiDBノードがTTLタスクを引き継がない問題を修正 [#45022](https://github.com/pingcap/tidb/issues/45022) @[lcwangchao](https://github.com/lcwangchao)
    -   TTL実行時のメモリリーク問題を修正 [#45510](https://github.com/pingcap/tidb/issues/45510) @[lcwangchao](https://github.com/lcwangchao)
    -   パーティションテーブルにデータを挿入する際の不正確なエラーメッセージの問題を修正 [#44966](https://github.com/pingcap/tidb/issues/44966) @[lilinghai](https://github.com/lilinghai)
    -   `INFORMATION_SCHEMA.TIFLASH_REPLICA`テーブルの読み取り権限の問題を修正 [#7795](https://github.com/pingcap/tiflash/issues/7795) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    -   パーティションテーブル名が間違っている場合にエラーが発生する問題を修正 [#44967](https://github.com/pingcap/tidb/issues/44967) @[River2000i](https://github.com/River2000i)
    -   `tidb_enable_dist_task`が有効になっている場合にインデックス作成が停止する問題を修正 [#44440](https://github.com/pingcap/tidb/issues/44440) @[tangenta](https://github.com/tangenta)
    -   BR を使用して `duplicate entry` を含むテーブルを復元する際に発生する `AUTO_ID_CACHE=1` エラーを修正します。 [#44716](https://github.com/pingcap/tidb/issues/44716) @[tiancaiamao](https://github.com/tiancaiamao)
    -   `TRUNCATE TABLE`の実行に要した時間が`ADMIN SHOW DDL JOBS`に表示されるタスク実行時間と一致しない問題を修正しました。 [#44785](https://github.com/pingcap/tidb/issues/44785) @[tangenta](https://github.com/tangenta)
    -   TiDBのアップグレード時にメタデータの読み取りに1つのDDLリースよりも時間がかかると、アップグレードが停止する問題を修正しました [#45176](https://github.com/pingcap/tidb/issues/45176) @[zimulala](https://github.com/zimulala)
    -   `SELECT CAST(n AS CHAR)`ステートメント内の`n`が負の数の場合、クエリ結果が正しくない問題を修正しました [#44786](https://github.com/pingcap/tidb/issues/44786) @[xhebox](https://github.com/xhebox)
    -   `tidb_opt_agg_push_down`が有効になっている場合にクエリが間違った結果を返す可能性がある問題を修正 [#44795](https://github.com/pingcap/tidb/issues/44795) @[AilinKid](https://github.com/AilinKid)
    -   `current_date()`を含むクエリがプランキャッシュを使用した場合に発生する誤った結果の問題を修正します [#45086](https://github.com/pingcap/tidb/issues/45086) @[qw4990](https://github.com/qw4990)

-   TiKV

    -   GC中にデータを読み取ると、まれにTiKVpanicが発生する可能性がある問題を修正しました [#15109](https://github.com/tikv/tikv/issues/15109) @[MyonKeminta](https://github.com/MyonKeminta)

-   PD

    -   PD の再起動によって`default`リソース グループが再初期化される可能性がある問題を修正 [#6787](https://github.com/tikv/pd/issues/6787) @[glorv](https://github.com/glorv)
    -   etcdが既に起動しているがクライアントがまだ接続していない場合に、クライアントを呼び出すとPDがpanicを起こす可能性がある問題を修正しました [#6860](https://github.com/tikv/pd/issues/6860) @[HuSharp](https://github.com/HuSharp)
    -   リージョンの出力 `health-check` が、リージョン ID を照会して返されるリージョン情報と一致しない問題を修正します。 [#6560](https://github.com/tikv/pd/issues/6560) @[JmPotato](https://github.com/JmPotato)
    -   `unsafe recovery`で失敗したラーナーピアが`auto-detect`モードでは無視される問題を修正 [#6690](https://github.com/tikv/pd/issues/6690) @[v01dstar](https://github.com/v01dstar)
    -   配置ルールがルールを満たしていないTiFlashラーナーを選択してしまう問題を修正します [#6662](https://github.com/tikv/pd/issues/6662) @[rleungx](https://github.com/rleungx)
    -   ルールチェッカーがピアを選択する際に、不健全なピアを削除できない問題を修正 [#6559](https://github.com/tikv/pd/issues/6559) @[nolouch](https://github.com/nolouch)

-   TiFlash

    -   TiFlashがデッドロックのためにパーティション化されたテーブルを正常に複製できない問題を修正 [#7758](https://github.com/pingcap/tiflash/issues/7758) @[hongyunyan](https://github.com/hongyunyan)
    -   `INFORMATION_SCHEMA.TIFLASH_REPLICA`システム テーブルにユーザーがアクセスする権限を持たないテーブルが含まれる問題を修正 [#7795](https://github.com/pingcap/tiflash/issues/7795) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    -   同じ MPP タスク内に複数の HashAgg 演算子が存在する場合、MPP タスクのコンパイルに非常に長い時間がかかり、クエリのパフォーマンスに深刻な影響を与える問題を修正しました [#7810](https://github.com/pingcap/tiflash/issues/7810) @[SeaRise](https://github.com/SeaRise)

-   ツール

    -   TiCDC

        -   PD が一時的に利用できないために changefeeds が失敗する問題を修正しました [#9294](https://github.com/pingcap/tiflow/issues/9294) @[asddongmen](https://github.com/asddongmen)
        -   TiCDCノードの一部がネットワークから隔離された場合に発生する可能性のあるデータ不整合の問題を修正します [#9344](https://github.com/pingcap/tiflow/issues/9344) @[CharlesCheung96](https://github.com/CharlesCheung96)
        -   Kafka Sinkでエラーが発生した場合、changefeedの進行が永久にブロックされる可能性がある問題を修正しました [#9309](https://github.com/pingcap/tiflow/issues/9309) @[hicqu](https://github.com/hicqu)
        -   TiCDCノードの状態変化時に発生する可能性のあるpanic問題を修正 [#9354](https://github.com/pingcap/tiflow/issues/9354) @[sdojjy](https://github.com/sdojjy)
        -   デフォルトの`ENUM`値のエンコード エラーを修正 [#9259](https://github.com/pingcap/tiflow/issues/9259) @[3AceShowHand](https://github.com/3AceShowHand)

    -   TiDB Lightning

        -   TiDB Lightning のインポート完了後にチェックサムを実行すると SSL エラーが発生する可能性がある問題を修正しました [#45462](https://github.com/pingcap/tidb/issues/45462) @[D3Hunter](https://github.com/D3Hunter)
        -   論理インポートモードで、インポート中に下流のテーブルを削除すると、 TiDB Lightningメタデータがタイムリーに更新されない可能性がある問題を修正しました [#44614](https://github.com/pingcap/tidb/issues/44614) @[dsdashun](https://github.com/dsdashun)

## 貢献者 {#contributors}

TiDBコミュニティの以下の貢献者の皆様に感謝申し上げます。

-   [charleszheng44](https://github.com/charleszheng44)
-   [dhysum](https://github.com/dhysum)
-   [haiyux](https://github.com/haiyux)
-   [Jiang-Hua](https://github.com/Jiang-Hua)
-   [Jille](https://github.com/Jille)
-   [jiyfhust](https://github.com/jiyfhust)
-   [krishnaduttPanchagnula](https://github.com/krishnaduttPanchagnula)
-   [L-maple](https://github.com/L-maple)
-   [pingandb](https://github.com/pingandb)
-   [testwill](https://github.com/testwill)
-   [tisonkun](https://github.com/tisonkun)
-   [xuyifangreeneyes](https://github.com/xuyifangreeneyes)
-   [yumchina](https://github.com/yumchina)
