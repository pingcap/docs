---
title: TiDB 7.3.0 Release Notes
summary: TiDB 7.3.0 の新機能、互換性の変更、改善点、バグ修正について説明します。
---

# TiDB 7.3.0 リリースノート {#tidb-7-3-0-release-notes}

発売日：2023年8月14日

TiDB バージョン: 7.3.0

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v7.3/quick-start-with-tidb)

7.3.0では、以下の主要な機能が導入されています。さらに、7.3.0には、TiDBサーバーとTiFlashにおけるクエリの安定性を向上させるための一連の機能強化（セクション[機能の詳細](#feature-details)で説明）も含まれています。これらの機能強化は、ユーザーに直接影響するものではなく、雑多な性質のものであるため、以下の表には含まれていません。

<table><thead><tr><th>カテゴリ</th><th>特徴</th><th>説明</th></tr></thead><tbody><tr><td>スケーラビリティとパフォーマンス</td><td>TiDB Lightning は<a href="https://docs.pingcap.com/tidb/v7.3/partitioned-raft-kv">Partitioned Raft KV</a>をサポートします (実験的)</td><td> TiDB Lightning は、アーキテクチャの近い将来の GA の一部として、新しい Partitioned Raft KVアーキテクチャをサポートするようになりました。</td></tr><tr><td rowspan="2">信頼性と可用性</td><td><a href="https://docs.pingcap.com/tidb/v7.3/tidb-lightning-physical-import-mode-usage#conflict-detection">データのインポート時に自動競合検出と解決を追加する</a></td><td>TiDB Lightning物理インポートモードは、新しいバージョンの競合検出をサポートします。このモードでは、競合が発生した場合に、競合データを置換（ <code>replace</code> ）または無視（ <code>ignore</code> ）するセマンティクスが実装されています。競合データを自動的に処理するとともに、競合解決のパフォーマンスを向上させます。</td></tr><tr><td><a href="https://docs.pingcap.com/tidb/v7.3/tidb-resource-control#query-watch-parameters">暴走クエリの手動管理</a>（実験的）</td><td>クエリの実行時間は予想以上に長くなる場合があります。リソースグループの新しいウォッチリストを使用すると、クエリをより効率的に管理し、優先順位を下げたり、強制終了したりすることができます。この機能により、オペレーターはSQLテキスト、SQLダイジェスト、またはプランダイジェストでターゲットクエリをマークし、リソースグループレベルでクエリを処理できるようになります。これにより、予期せぬ大規模なクエリがクラスターに及ぼす潜在的な影響をより詳細に制御できるようになります。</td></tr><tr><td> SQL</td><td><a href="https://docs.pingcap.com/tidb/v7.3/optimizer-hints">クエリプランナーにオプティマイザーヒントを追加することで、クエリの安定性に対するオペレータ制御を強化します。</a></td><td>追加されたヒント: <code>NO_INDEX_JOIN()</code> 、 <code>NO_MERGE_JOIN()</code> 、 <code>NO_INDEX_MERGE_JOIN()</code> 、 <code>NO_HASH_JOIN()</code> 、 <code>NO_INDEX_HASH_JOIN()</code></td></tr><tr><td> DB操作と可観測性</td><td><a href="https://docs.pingcap.com/tidb/v7.3/sql-statement-show-analyze-status">統計収集タスクの進行状況を表示する</a></td><td><code>SHOW ANALYZE STATUS</code>ステートメントまたは<code>mysql.analyze_jobs</code>システム テーブルを使用して、 <code>ANALYZE</code>タスクの進行状況を表示できるようになりました。</td></tr></tbody></table>

## 機能の詳細 {#feature-details}

### パフォーマンス {#performance}

-   TiFlashはレプリカ選択戦略[＃44106](https://github.com/pingcap/tidb/issues/44106) @ [徐淮嶼](https://github.com/XuHuaiyu)をサポートします

    v7.3.0より前のバージョンでは、 TiFlashはデータスキャンとMPP計算に全ノードのレプリカを使用してパフォーマンスを最大化していました。v7.3.0以降、 TiFlashはレプリカ選択戦略を導入し、 [`tiflash_replica_read`](/system-variables.md#tiflash_replica_read-new-in-v730)システム変数を使用して設定できるようになりました。この戦略は、ノードの[ゾーン属性](/schedule-replicas-by-topology-labels.md#optional-configure-labels-for-tidb)に基づいて特定のレプリカを選択し、データスキャンとMPP計算を行う特定のノードをスケジュールすることをサポートします。

    複数のデータセンターに展開されたクラスターで、各データセンターに完全なTiFlashデータレプリカが存在する場合、この戦略を設定して、現在のデータセンターのTiFlashレプリカのみを選択できます。これにより、データスキャンとMPP計算は現在のデータセンター内のTiFlashノードでのみ実行されるため、データセンター間での過剰なネットワークデータ転送を回避できます。

    詳細については[ドキュメント](/system-variables.md#tiflash_replica_read-new-in-v730)参照してください。

-   TiFlashはノード[＃40220](https://github.com/pingcap/tidb/issues/40220) @ [エルサ0520](https://github.com/elsa0520)内でランタイムフィルターをサポートします。

    ランタイムフィルターは、クエリプランニングフェーズで生成される**動的述語**です。テーブル結合プロセスにおいて、これらの動的述語は結合条件を満たさない行を効果的に除外することで、スキャン時間とネットワークオーバーヘッドを削減し、テーブル結合の効率を向上させます。TiFlashはv7.3.0以降、ノード内でランタイムフィルターをサポートし、分析クエリの全体的なパフォーマンスを向上させます。一部のTPC-DSワークロードでは、パフォーマンスが10%～50%向上する可能性があります。

    この機能はバージョン7.3.0ではデフォルトで無効になっています。この機能を有効にするには、システム変数[`tidb_runtime_filter_mode`](/system-variables.md#tidb_runtime_filter_mode-new-in-v720)を`LOCAL`に設定してください。

    詳細については[ドキュメント](/runtime-filter.md)参照してください。

-   TiFlash は共通テーブル式 (CTE) の実行をサポートしています (実験的) [＃43333](https://github.com/pingcap/tidb/issues/43333) @ [ウィノロス](https://github.com/winoros)

    v7.3.0より前のバージョンでは、 TiFlashのMPPエンジンはデフォルトでCTEを含むクエリを実行できません。MPPフレームワーク内で最高の実行パフォーマンスを実現するには、システム変数[`tidb_opt_force_inline_cte`](/system-variables.md#tidb_opt_force_inline_cte-new-in-v630)使用してCTEのインライン化を強制する必要があります。

    v7.3.0以降、TiFlashのMPPエンジンは、CTEを含むクエリをインライン化せずに実行することをサポートし、MPPフレームワーク内で最適なクエリ実行を実現します。TPC-DSベンチマークテストでは、この機能により、CTEをインライン化した場合と比較して、CTEを含むクエリの全体的なクエリ実行速度が20%向上することが示されました。

    この機能は実験的であり、デフォルトでは無効になっています。システム変数[`tidb_opt_enable_mpp_shared_cte_execution`](/system-variables.md#tidb_opt_enable_mpp_shared_cte_execution-new-in-v720)によって制御されます。

### 信頼性 {#reliability}

-   新しいオプティマイザヒント[＃45520](https://github.com/pingcap/tidb/issues/45520) @ [qw4990](https://github.com/qw4990)を追加

    v7.3.0 では、TiDB に、テーブル間の結合方法を制御するためのいくつかの新しいオプティマイザー ヒントが導入されています。

    -   [`NO_MERGE_JOIN()`](/optimizer-hints.md#no_merge_joint1_name--tl_name-)マージ結合以外の結合方法を選択します。
    -   [`NO_INDEX_JOIN()`](/optimizer-hints.md#no_index_joint1_name--tl_name-)インデックス ネスト ループ結合以外の結合方法を選択します。
    -   [`NO_INDEX_MERGE_JOIN()`](/optimizer-hints.md#no_index_merge_joint1_name--tl_name-)インデックス ネスト ループ マージ結合以外の結合方法を選択します。
    -   [`NO_HASH_JOIN()`](/optimizer-hints.md#no_hash_joint1_name--tl_name-)ハッシュ結合以外の結合方法を選択します。
    -   [`NO_INDEX_HASH_JOIN()`](/optimizer-hints.md#no_index_hash_joint1_name--tl_name-) [インデックスネストループハッシュ結合](/optimizer-hints.md#inl_hash_join)以外の結合方法を選択します。

    詳細については[ドキュメント](/optimizer-hints.md)参照してください。

-   予想以上にリソースを使用するクエリを手動でマークする（実験的） [＃43691](https://github.com/pingcap/tidb/issues/43691) @ [コナー1996](https://github.com/Connor1996) @ [キャビンフィーバーB](https://github.com/CabinfeverB)

    v7.2.0では、TiDBは想定以上にリソースを使用するクエリ（ランナウェイクエリ）を自動的にダウングレードまたはキャンセルすることで、ランナウェイクエリを自動的に管理します。しかし、実際にはルールだけではすべてのケースに対応できません。そこで、TiDB v7.3.0では、ランナウェイクエリを手動でマークする機能が導入されました。新しいコマンド[`QUERY WATCH`](/sql-statements/sql-statement-query-watch.md)を使用すると、SQLテキスト、SQLダイジェスト、または実行プランに基づいてランナウェイクエリをマークし、マークされたランナウェイクエリをダウングレードまたはキャンセルできます。

    この機能は、データベースで突発的なパフォーマンス問題が発生した場合に効果的な介入方法を提供します。クエリに起因するパフォーマンス問題の場合、根本原因を特定する前に、全体的なパフォーマンスへの影響を迅速に軽減し、システムのサービス品質を向上させることができます。

    詳細については[ドキュメント](/tidb-resource-control-runaway-queries.md#query-watch-parameters)参照してください。

### SQL {#sql}

-   リストとリスト列のパーティションテーブルは、デフォルトのパーティション[＃20679](https://github.com/pingcap/tidb/issues/20679) @ [ミョンス](https://github.com/mjonss) @ [bb7133](https://github.com/bb7133)をサポートします。

    バージョン7.3.0より前のバージョンでは、 `INSERT`文を使用してリストまたはリスト列パーティションテーブルにデータを挿入する場合、データは表に指定されたパーティション条件を満たしている必要があります。挿入するデータがこれらの条件のいずれかを満たしていない場合、文の実行は失敗するか、条件を満たしていないデータは無視されます。

    バージョン7.3.0以降、リストおよびリスト列パーティションテーブルはデフォルトパーティションをサポートします。デフォルトパーティションの作成後、挿入するデータがパーティション条件を満たさない場合、そのデータはデフォルトパーティションに書き込まれます。この機能により、リストおよびList COLUMNS パーティショニングのユーザビリティが向上し、パーティション条件を満たさないデータによって`INSERT`のステートメントの実行が失敗したり、データが無視されたりするのを回避できます。

    この機能はMySQL構文に対するTiDBの拡張であることに注意してください。デフォルトパーティションを持つパーティションテーブルの場合、テーブル内のデータはMySQLに直接複製できません。

    詳細については[ドキュメント](/partitioned-table.md#list-partitioning)参照してください。

### 可観測性 {#observability}

-   統計情報[＃44033](https://github.com/pingcap/tidb/issues/44033) @ [ホーキングレイ](https://github.com/hawkingrei)収集の進行状況を表示します

    大規模なテーブルの統計収集には、多くの場合、長い時間がかかります。以前のバージョンでは、統計収集の進行状況を確認できず、完了時間を予測できませんでした。TiDB v7.3.0では、統計収集の進行状況を表示する機能が導入されました。システムテーブル`mysql.analyze_jobs`または`SHOW ANALYZE STATUS`使用して、全体のワークロード、現在の進行状況、および各サブタスクの推定完了時間を表示できます。大規模データのインポートやSQLパフォーマンスの最適化などのシナリオにおいて、この機能はタスク全体の進行状況を把握し、ユーザーエクスペリエンスを向上させるのに役立ちます。

    詳細については[ドキュメント](/sql-statements/sql-statement-show-analyze-status.md)参照してください。

-   Plan Replayerは履歴統計[＃45038](https://github.com/pingcap/tidb/issues/45038) @ [時間と運命](https://github.com/time-and-fate)エクスポートをサポートします

    バージョン7.3.0以降、新たに追加された[`dump with stats as of timestamp`](/sql-plan-replayer.md)句を使用することで、Plan Replayerを使用して、特定のSQL関連オブジェクトの特定の時点における統計情報をエクスポートできます。実行プランの問題の診断において、履歴統計情報を正確に取得することで、問題が発生した時点で実行プランがどのように生成されたかをより正確に分析できます。これにより、問題の根本原因を特定し、実行プランの問題の診断効率を大幅に向上させることができます。

    詳細については[ドキュメント](/sql-plan-replayer.md)参照してください。

### データ移行 {#data-migration}

-   TiDB Lightning は、競合データ検出および処理戦略[＃41629](https://github.com/pingcap/tidb/issues/41629) @ [ランス6716](https://github.com/lance6716)の新しいバージョンを導入します

    以前のバージョンでは、 TiDB Lightning は論理インポートモードと物理インポートモードで異なる競合検出および処理方法を使用していましたが、設定が複雑で、ユーザーにとって理解しにくいものでした。また、物理インポートモードでは、 `replace`または`ignore`戦略を使用して競合を処理できませんでした。v7.3.0 以降、 TiDB Lightning は論理インポートモードと物理インポートモードの両方に統一された競合検出および処理戦略を導入します。競合が発生した場合、競合するデータをエラーとして報告する ( `error` )、置き換える ( `replace` )、または無視する ( `ignore` ) ことを選択できます。指定した数の競合レコードを処理した後にタスクが中断されて終了するなど、競合レコードの数を制限することもできます。さらに、システムはトラブルシューティングのために競合データを記録できます。

    競合の多いインポートデータの場合、パフォーマンス向上のため、新しいバージョンの競合検出および処理戦略を使用することをお勧めします。ラボ環境では、新しいバージョンの戦略により、競合検出および処理のパフォーマンスが旧バージョンと比較して最大3倍向上しました。このパフォーマンス値は参考値です。実際のパフォーマンスは、設定、テーブル構造、競合データの割合によって異なる場合があります。なお、新しいバージョンと旧バージョンの競合検出および処理戦略を同時に使用することはできません。旧バージョンの競合検出および処理戦略は、将来的に廃止される予定です。

    詳細については[ドキュメント](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#conflict-detection)参照してください。

-   TiDB Lightning はPartitioned Raft KV (実験的) [＃14916](https://github.com/tikv/tikv/issues/14916) @ [GMHDBJD](https://github.com/GMHDBJD)をサポートします

    TiDB Lightning は、Partitioned Raft KV をサポートするようになりました。この機能により、 TiDB Lightningのデータインポートパフォーマンスが向上します。

-   TiDB Lightningは、より多くの診断ログを印刷することでトラブルシューティングを強化するための新しいパラメータ`enable-diagnose-log`を導入しました[＃45497](https://github.com/pingcap/tidb/issues/45497) @ [D3ハンター](https://github.com/D3Hunter)

    デフォルトではこの機能は無効になっており、 TiDB Lightning は`lightning/main`を含むログのみを出力。有効にすると、 TiDB Lightning は`client-go`と`tidb`に関連する問題の診断に役立つように、すべてのパッケージ（ `client-go`と`tidb`を含む）のログを出力。

    詳細については[ドキュメント](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-global)参照してください。

## 互換性の変更 {#compatibility-changes}

> **注記：**
>
> このセクションでは、v7.2.0から最新バージョン（v7.3.0）にアップグレードする際に知っておくべき互換性の変更点について説明します。v7.1.0以前のバージョンから最新バージョンにアップグレードする場合は、中間バージョンで導入された互換性の変更点も確認する必要があるかもしれません。

### 行動の変化 {#behavior-changes}

-   TiDB

    -   MPP は、 TiFlashエンジンが提供する分散コンピューティング フレームワークで、ノード間でのデータ交換を可能にし、高性能で高スループットの SQL アルゴリズムを提供します。他のプロトコルと比較して、 MPP プロトコルはより成熟しており、より優れたタスクおよびリソース管理を提供できます。 v7.3.0 以降、 TiDB が計算タスクをTiFlashにプッシュする場合、オプティマイザーはデフォルトで MPP プロトコルを使用する実行プランのみを生成します。 [`tidb_allow_mpp`](/system-variables.md#tidb_allow_mpp-new-in-v50) `OFF`に設定すると、 TiDB をアップグレードした後にクエリーがエラーを返す可能性があります。アップグレード前に`tidb_allow_mpp`の値を確認し、 `ON`に設定することをお勧めします。 コスト見積もりに基づいて実行プランを生成するためにオプティマイザーが Cop、BatchCop、および MPP プロトコルのいずれかを選択する必要がある場合は、 [`tidb_allow_tiflash_cop`](/system-variables.md#tidb_allow_tiflash_cop-new-in-v730)変数を`ON`に設定できます。

-   バックアップと復元 (BR)

    -   BRは、完全なデータ復元を実行する前に、空のクラスタのチェックを追加します。デフォルトでは、空でないクラスタへのデータの復元は許可されません。強制的に復元する場合は、 `--filter`オプションを使用して、復元先のテーブル名を指定できます。

-   TiDB Lightning

    -   `tikv-importer.on-duplicate`は非推奨となり、 [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)に置き換えられました。
    -   `max-error`パラメータは、 TiDB Lightningが移行タスクを停止するまでに許容できる致命的ではないエラーの最大数を制御しますが、インポートデータの競合を制限しなくなりました。3 [`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)のパラメータは、許容できる競合レコードの最大数を制御するようになりました。

-   TiCDC

    -   Kafka シンクが Avro プロトコルを使用する場合、 `force-replicate`パラメータが`true`に設定されると、TiCDC は変更フィードを作成するときにエラーを報告します。
    -   `delete-only-output-handle-key-columns`と`force-replicate`パラメータの間に互換性がないため、両方のパラメータを有効にすると、TiCDC は変更フィードを作成するときにエラーを報告します。
    -   出力プロトコルがオープン プロトコルの場合、 `UPDATE`イベントは変更された列のみを出力します。

### システム変数 {#system-variables}

| 変数名                                                                                                                     | タイプを変更   | 説明                                                                          |
| ----------------------------------------------------------------------------------------------------------------------- | -------- | --------------------------------------------------------------------------- |
| [`tidb_opt_enable_mpp_shared_cte_execution`](/system-variables.md#tidb_opt_enable_mpp_shared_cte_execution-new-in-v720) | 修正済み     | このシステム変数はバージョン7.3.0以降で有効になります。TiFlash MPPで非再帰共通テーブル式（CTE）を実行できるかどうかを制御します。  |
| [`tidb_allow_tiflash_cop`](/system-variables.md#tidb_allow_tiflash_cop-new-in-v730)                                     | 新しく追加された | このシステム変数は、TiDB が計算タスクをTiFlashにプッシュダウンするときに実行プランを生成するためのプロトコルを選択するために使用されます。 |
| [`tidb_lock_unchanged_keys`](/system-variables.md#tidb_lock_unchanged_keys-new-in-v711-and-v730)                        | 新しく追加された | この変数は、特定のシナリオにおいて、トランザクションに関係しているが変更されていないキーをロックするかどうかを制御するために使用されます。       |
| [`tidb_opt_enable_non_eval_scalar_subquery`](/system-variables.md#tidb_opt_enable_non_eval_scalar_subquery-new-in-v730) | 新しく追加された | `EXPLAIN`ステートメントが最適化段階で展開できる定数サブクエリの実行を無効にするかどうかを制御します。                     |
| [`tidb_skip_missing_partition_stats`](/system-variables.md#tidb_skip_missing_partition_stats-new-in-v730)               | 新しく追加された | この変数は、パーティション統計が欠落している場合のグローバル統計の生成を制御します。                                  |
| [`tiflash_replica_read`](/system-variables.md#tiflash_replica_read-new-in-v730)                                         | 新しく追加された | クエリにTiFlashエンジンが必要な場合にTiFlashレプリカを選択する戦略を制御します。                             |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーションパラメータ                                                                                                                                 | タイプを変更   | 説明                                                                                                                                                                                                                                                                                                                                          |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB           | [`enable-32bits-connection-id`](/tidb-configuration-file.md#enable-32bits-connection-id-new-in-v730)                                            | 新しく追加された | 32 ビット接続 ID 機能を有効にするかどうかを制御します。                                                                                                                                                                                                                                                                                                             |
| TiDB           | [`in-mem-slow-query-recent-num`](/tidb-configuration-file.md#in-mem-slow-query-recent-num-new-in-v730)                                          | 新しく追加された | メモリにキャッシュされる最近使用された低速クエリの数を制御します。                                                                                                                                                                                                                                                                                                           |
| TiDB           | [`in-mem-slow-query-topn-num`](/tidb-configuration-file.md#in-mem-slow-query-topn-num-new-in-v730)                                              | 新しく追加された | メモリにキャッシュされる最も遅いクエリの数を制御します。                                                                                                                                                                                                                                                                                                                |
| TiKV           | [`coprocessor.region-bucket-size`](/tikv-configuration-file.md#region-bucket-size-new-in-v610)                                                  | 修正済み     | デフォルト値を`96MiB`から`50MiB`に変更します。                                                                                                                                                                                                                                                                                                              |
| TiKV           | [`raft-engine.format-version`](/tikv-configuration-file.md#format-version-new-in-v630)                                                          | 修正済み     | Partitioned Raft KV ( `storage.engine="partitioned-raft-kv"` )を使用する場合、リボンフィルターが使用されます。そのため、TiKVはデフォルト値を`2`から`5`に変更します。                                                                                                                                                                                                                      |
| TiKV           | [`raftdb.max-total-wal-size`](/tikv-configuration-file.md#max-total-wal-size-1)                                                                 | 修正済み     | Partitioned Raft KV ( `storage.engine="partitioned-raft-kv"` ) を使用する場合、TiKVはWALの書き込みをスキップします。そのため、TiKVはデフォルト値を`"4GB"`から`1`に変更し、WALを無効にします。                                                                                                                                                                                                  |
| TiKV           | [`rocksdb.[defaultcf|writecf|lockcf].compaction-guard-min-output-file-size`](/tikv-configuration-file.md#compaction-guard-min-output-file-size) | 修正済み     | 大容量データの書き込み時に圧縮速度が書き込み速度に追いつかない問題を解決するために、デフォルト値を`"1MB"`から`"8MB"`に変更します。                                                                                                                                                                                                                                                                    |
| TiKV           | [`rocksdb.[defaultcf|writecf|lockcf].format-version`](/tikv-configuration-file.md#format-version-new-in-v620)                                   | 修正済み     | Partitioned Raft KV ( `storage.engine="partitioned-raft-kv"` )を使用する場合、リボンフィルターが使用されます。そのため、TiKVはデフォルト値を`2`から`5`に変更します。                                                                                                                                                                                                                      |
| TiKV           | [`rocksdb.lockcf.write-buffer-size`](/tikv-configuration-file.md#write-buffer-size)                                                             | 修正済み     | Partitioned Raft KV（ `storage.engine="partitioned-raft-kv"` ）を使用する場合、lockcfでの圧縮を高速化するために、TiKVはデフォルト値を`"32MB"`から`"4MB"`に変更します。                                                                                                                                                                                                               |
| TiKV           | [`rocksdb.max-total-wal-size`](/tikv-configuration-file.md#max-total-wal-size)                                                                  | 修正済み     | Partitioned Raft KV ( `storage.engine="partitioned-raft-kv"` ) を使用する場合、TiKVはWALの書き込みをスキップします。そのため、TiKVはデフォルト値を`"4GB"`から`1`に変更し、WALを無効にします。                                                                                                                                                                                                  |
| TiKV           | [`rocksdb.stats-dump-period`](/tikv-configuration-file.md#stats-dump-period)                                                                    | 修正済み     | Partitioned Raft KV（ `storage.engine="partitioned-raft-kv"` ）を使用する場合、冗長ログ出力を無効にするには、デフォルト値を`"10m"`から`"0"`に変更します。                                                                                                                                                                                                                            |
| TiKV           | [`rocksdb.write-buffer-limit`](/tikv-configuration-file.md#write-buffer-limit-new-in-v660)                                                      | 修正済み     | memtablesのメモリオーバーヘッドを削減するため、 `storage.engine="raft-kv"`場合、TiKVはデフォルト値をマシンのメモリの25%から`0` （無制限を意味する）に変更します。Partitioned Raft KV（ `storage.engine="partitioned-raft-kv"` ）を使用する場合、TiKVはデフォルト値をマシンのメモリの25%から20%に変更します。                                                                                                                            |
| TiKV           | [`storage.block-cache.capacity`](/tikv-configuration-file.md#capacity)                                                                          | 修正済み     | Partitioned Raft KV（ `storage.engine="partitioned-raft-kv"` ）を使用する場合、memtablesのメモリオーバーヘッドを補うために、TiKVはデフォルト値をシステムメモリ全体のサイズの45%から30%に変更します。                                                                                                                                                                                                   |
| TiFlash        | [`storage.format_version`](/tiflash/tiflash-configuration.md)                                                                                   | 修正済み     | 小さなファイルを結合することで物理ファイル数を削減する新しいDTFileフォーマット`format_version = 5`を導入します。このフォーマットは実験的であり、デフォルトでは有効になっていないことに注意してください。                                                                                                                                                                                                                           |
| TiDB Lightning | `tikv-importer.incremental-import`                                                                                                              | 削除済み     | TiDB Lightning の並列インポートパラメータ。増分インポートパラメータと間違えられる可能性があったため、このパラメータの名前は`tikv-importer.parallel-import`に変更されました。ユーザーが古いパラメータ名を渡した場合、自動的に新しいパラメータ名に変換されます。                                                                                                                                                                                      |
| TiDB Lightning | `tikv-importer.on-duplicate`                                                                                                                    | 非推奨      | 論理インポートモードで競合するレコードを挿入しようとした際に実行するアクションを制御します。v7.3.0以降、このパラメータは[`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)に置き換えられます。                                                                                                                                                                         |
| TiDB Lightning | [`conflict.max-record-rows`](/tidb-lightning/tidb-lightning-configuration.md)                                                                   | 新しく追加された | 競合データを処理する戦略の新バージョン。1 `conflict_records`の最大行数を制御します。デフォルト値は100です。                                                                                                                                                                                                                                                                           |
| TiDB Lightning | [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md)                                                                          | 新しく追加された | 競合データの処理戦略の新バージョン。以下のオプションが含まれます：&quot;&quot;（TiDB Lightning は競合データを検出・処理しません）、 `error` （インポートされたデータで主キーまたは一意キーの競合が検出された場合、インポートを終了しエラーを報告します）、 `replace` （主キーまたは一意キーの競合を含むデータが検出された場合、新しいデータは保持され、古いデータは上書きされます）、 `ignore` （主キーまたは一意キーの競合を含むデータが検出された場合、古いデータは保持され、新しいデータは無視されます）。デフォルト値は &quot;&quot; で、 TiDB Lightning は競合データを検出・処理しません。 |
| TiDB Lightning | [`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md)                                                                         | 新しく追加された | 競合データの上限を制御します。1 `conflict.strategy="error"`場合、デフォルト値は`0`です。5 または`conflict.strategy="replace"` `conflict.strategy="ignore"`場合、maxint として設定できます。                                                                                                                                                                                             |
| TiDB Lightning | [`enable-diagnose-logs`](/tidb-lightning/tidb-lightning-configuration.md)                                                                       | 新しく追加された | 診断ログを有効にするかどうかを制御します。デフォルト値は`false`で、インポートに関連するログのみが出力され、他の依存コンポーネントのログは出力されません。 `true`に設定すると、インポートプロセスと他の依存コンポーネントの両方のログが出力され、診断に使用できるGRPCデバッグが有効になります。                                                                                                                                                                                    |
| TiDB Lightning | [`tikv-importer.parallel-import`](/tidb-lightning/tidb-lightning-configuration.md)                                                              | 新しく追加された | TiDB Lightning の並列インポートパラメータ。増分インポートパラメータと誤認され、誤用される可能性のある既存のパラメータ`tikv-importer.incremental-import`置き換えます。                                                                                                                                                                                                                                 |
| BR             | `azblob.encryption-scope`                                                                                                                       | 新しく追加された | BR は、Azure Blob Storage の暗号化スコープ サポートを提供します。                                                                                                                                                                                                                                                                                                |
| BR             | `azblob.encryption-key`                                                                                                                         | 新しく追加された | BR は、Azure Blob Storage の暗号化キー サポートを提供します。                                                                                                                                                                                                                                                                                                  |
| TiCDC          | [`large-message-handle-option`](/ticdc/ticdc-sink-to-kafka.md#handle-messages-that-exceed-the-kafka-topic-limit)                                | 新しく追加された | デフォルトでは空です。つまり、メッセージサイズがKafkaトピックの制限を超えると、変更フィードは失敗します。この設定を`"handle-key-only"`に設定すると、メッセージがサイズ制限を超えた場合、メッセージサイズを縮小するためにハンドルキーのみが送信されます。縮小されたメッセージでも制限を超える場合、変更フィードは失敗します。                                                                                                                                                                  |
| TiCDC          | [`sink.csv.binary-encoding-method`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)                                      | 新しく追加された | バイナリデータのエンコード方式。1 または`'base64'` `'hex'`指定できます。デフォルト値は`'base64'`です。                                                                                                                                                                                                                                                                          |

### システムテーブル {#system-tables}

-   内部タイマーのメタデータを保存するための新しいシステム テーブル`mysql.tidb_timers`を追加します。

## 非推奨の機能 {#deprecated-features}

-   TiDB

    -   統計の[`Fast Analyze`](/system-variables.md#tidb_enable_fast_analyze)機能 (実験的) は、v7.5.0 で廃止される予定です。
    -   統計の[増分コレクション](https://docs.pingcap.com/tidb/v7.3/statistics#incremental-collection)機能は、v7.5.0 で廃止されます。

## 改善点 {#improvements}

-   TiDB

    -   最適化フェーズ[＃22076](https://github.com/pingcap/tidb/issues/22076) @ [ウィノロス](https://github.com/winoros)で`EXPLAIN`文がサブクエリを事前に実行するかどうかを制御するための新しいシステム変数[`tidb_opt_enable_non_eval_scalar_subquery`](/system-variables.md#tidb_opt_enable_non_eval_scalar_subquery-new-in-v730)導入します。
    -   [グローバルキル](/tidb-configuration-file.md#enable-global-kill-new-in-v610)有効になっている場合、 <kbd>Control+C</kbd> [＃8854](https://github.com/pingcap/tidb/issues/8854) @ [ピンギュ](https://github.com/pingyu)を押すことで現在のセッションを終了できます。
    -   `IS_FREE_LOCK()`と`IS_USED_LOCK()`ロック関数[＃44493](https://github.com/pingcap/tidb/issues/44493) @ [ドヴェーデン](https://github.com/dveeden)をサポート
    -   ディスク[＃45125](https://github.com/pingcap/tidb/issues/45125)からダンプされたチャンクを読み込む際のパフォーマンスを最適化します[ヤンケオ](https://github.com/YangKeao)
    -   オプティマイザ修正コントロール[＃44855](https://github.com/pingcap/tidb/issues/44855) @ [時間と運命](https://github.com/time-and-fate)を使用して、インデックス結合の内部テーブルの過大評価の問題を最適化します。

-   TiKV

    -   `Max gap of safe-ts`と`Min safe ts region`メトリックを追加し、 `tikv-ctl get-region-read-progress`コマンドを導入して、resolved-tsと安全な ts の状態をより適切に観察および診断します[＃15082](https://github.com/tikv/tikv/issues/15082) @ [エキシウム](https://github.com/ekexium)

-   PD

    -   Swaggerサーバーが有効になっていない場合に、デフォルトで Swagger API をブロックする機能をサポート[＃6786](https://github.com/tikv/pd/issues/6786) @ [バッファフライ](https://github.com/bufferflies)
    -   etcd [＃6554](https://github.com/tikv/pd/issues/6554) [＃6442](https://github.com/tikv/pd/issues/6442) @ [lhy1024](https://github.com/lhy1024)の高可用性を向上させる
    -   `GetRegions`リクエスト[＃6835](https://github.com/tikv/pd/issues/6835) @ [lhy1024](https://github.com/lhy1024)のメモリ消費を削減

-   TiFlash

    -   物理ファイルの数を減らすために新しい DTFile 形式バージョン[`storage.format_version = 5`](/tiflash/tiflash-configuration.md)をサポートします (実験的) [＃7595](https://github.com/pingcap/tiflash/issues/7595) @ [ホンユニャン](https://github.com/hongyunyan)

-   ツール

    -   バックアップと復元 (BR)

        -   BRを使用して Azure Blob Storage にデータをバックアップする場合、サーバー側暗号化の暗号化スコープまたは暗号化キーのいずれかを指定できます[＃45025](https://github.com/pingcap/tidb/issues/45025) @ [リーヴルス](https://github.com/Leavrth)

    -   TiCDC

        -   オープンプロトコル出力のメッセージサイズを最適化して、 `UPDATE`イベント[＃9336](https://github.com/pingcap/tiflow/issues/9336) @ [3エースショーハンド](https://github.com/3AceShowHand)を送信するときに更新された列の値のみが含まれるようにします。
        -   ストレージシンクは、HEX形式のデータの16進エンコードをサポートするようになり、AWS DMS形式仕様[＃9373](https://github.com/pingcap/tiflow/issues/9373) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)と互換性があります。
        -   Kafka Sink は、メッセージが大きすぎる場合に[ハンドルキーデータのみを送信する](/ticdc/ticdc-sink-to-kafka.md#handle-messages-that-exceed-the-kafka-topic-limit)サポートし、メッセージのサイズを[＃9382](https://github.com/pingcap/tiflow/issues/9382) @ [3エースショーハンド](https://github.com/3AceShowHand)に縮小します。

## バグ修正 {#bug-fixes}

-   TiDB

    -   MySQLカーソルフェッチプロトコル使用時に、結果セットのメモリ消費量が`tidb_mem_quota_query`上限を超え、TiDBのメモリオーバーフローが発生する問題を修正しました。修正後、TiDBは結果セットを自動的にディスクに書き込み、メモリを解放します[＃43233](https://github.com/pingcap/tidb/issues/43233) @ [ヤンケオ](https://github.com/YangKeao)
    -   データ競合[＃45561](https://github.com/pingcap/tidb/issues/45561) @ [ゲンリキ](https://github.com/gengliqi)によって引き起こされる TiDBpanic問題を修正しました
    -   `indexMerge`のクエリが[＃45279](https://github.com/pingcap/tidb/issues/45279) @ [xzhangxian1008](https://github.com/xzhangxian1008)で強制終了されたときに発生するハングアップの問題を修正しました
    -   `tidb_enable_parallel_apply`有効になっている場合、MPP モードでのクエリ結果が正しくない問題を修正[＃45299](https://github.com/pingcap/tidb/issues/45299) @ [ウィンドトーカー](https://github.com/windtalker)
    -   PD時間[＃44822](https://github.com/pingcap/tidb/issues/44822) @ [ジグアン](https://github.com/zyguan)に突然の変化があったときに`resolve lock`ハングする可能性がある問題を修正しました
    -   GC ロック解決ステップで一部の悲観的ロック[＃45134](https://github.com/pingcap/tidb/issues/45134) @ [ミョンケミンタ](https://github.com/MyonKeminta)が見逃される可能性がある問題を修正しました
    -   `ORDER BY`のクエリが動的プルーニングモード[＃45007](https://github.com/pingcap/tidb/issues/45007) @ [定義2014](https://github.com/Defined2014)で誤った結果を返す問題を修正しました
    -   `DEFAULT`列目の値[＃45136](https://github.com/pingcap/tidb/issues/45136) @ [定義2014](https://github.com/Defined2014)と同じ列に`AUTO_INCREMENT`指定できる問題を修正しました
    -   システムテーブル`INFORMATION_SCHEMA.TIKV_REGION_STATUS`をクエリすると、場合によっては誤った結果が返される問題を修正しました[＃45531](https://github.com/pingcap/tidb/issues/45531) @ [定義2014](https://github.com/Defined2014)
    -   一部のケースでパーティションテーブルのプルーニングが不正確になる問題を修正[＃42273](https://github.com/pingcap/tidb/issues/42273) @ [ジフハウス](https://github.com/jiyfhust)
    -   パーティションテーブル[＃42435](https://github.com/pingcap/tidb/issues/42435) @ [L-メープル](https://github.com/L-maple)のパーティションを切り捨てるときにグローバルインデックスがクリアされない問題を修正しました
    -   1つのTiDBノード[＃45022](https://github.com/pingcap/tidb/issues/45022) @ [lcwangchao](https://github.com/lcwangchao)で障害が発生した後、他のTiDBノードがTTLタスクを引き継がない問題を修正しました
    -   TTLが[＃45510](https://github.com/pingcap/tidb/issues/45510) @ [lcwangchao](https://github.com/lcwangchao)で実行されているときのメモリリークの問題を修正しました
    -   パーティションテーブル[＃44966](https://github.com/pingcap/tidb/issues/44966) @ [リーリンハイ](https://github.com/lilinghai)にデータを挿入する際の不正確なエラーメッセージの問題を修正しました
    -   `INFORMATION_SCHEMA.TIFLASH_REPLICA`テーブル[＃7795](https://github.com/pingcap/tiflash/issues/7795) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)の読み取り権限の問題を修正しました
    -   間違ったパーティションテーブル名[＃44967](https://github.com/pingcap/tidb/issues/44967) @ [リバー2000i](https://github.com/River2000i)を使用するとエラーが発生する問題を修正
    -   `tidb_enable_dist_task`が有効になっている場合にインデックスの作成が停止する問題を修正[＃44440](https://github.com/pingcap/tidb/issues/44440) @ [接線](https://github.com/tangenta)
    -   BR [＃44716](https://github.com/pingcap/tidb/issues/44716) @ [天菜まお](https://github.com/tiancaiamao)を使用して`AUTO_ID_CACHE=1`テーブルを復元するときに発生する`duplicate entry`エラーを修正します
    -   `TRUNCATE TABLE`実行に費やされた時間が`ADMIN SHOW DDL JOBS` [＃44785](https://github.com/pingcap/tidb/issues/44785) @ [接線](https://github.com/tangenta)に表示されるタスク実行時間と一致しない問題を修正しました
    -   メタデータの読み取りに 1 つの DDL リース[＃45176](https://github.com/pingcap/tidb/issues/45176) @ [ジムララ](https://github.com/zimulala)よりも長い時間がかかる場合に TiDB のアップグレードが停止する問題を修正しました
    -   文中の`n`負の数[＃44786](https://github.com/pingcap/tidb/issues/44786) @ [xhebox](https://github.com/xhebox)の場合に文`SELECT CAST(n AS CHAR)`のクエリ結果が正しくない問題を修正しました
    -   `tidb_opt_agg_push_down`有効になっている場合にクエリが誤った結果を返す可能性がある問題を修正[＃44795](https://github.com/pingcap/tidb/issues/44795) @ [アイリンキッド](https://github.com/AilinKid)
    -   `current_date()`のクエリがプラン キャッシュ[＃45086](https://github.com/pingcap/tidb/issues/45086) @ [qw4990](https://github.com/qw4990)を使用した場合に誤った結果が発生する問題を修正しました

-   TiKV

    -   GC 中にデータを読み取ると、まれに TiKVpanicが発生する可能性がある問題を修正[＃15109](https://github.com/tikv/tikv/issues/15109) @ [ミョンケミンタ](https://github.com/MyonKeminta)

-   PD

    -   PDを再起動すると、 `default`リソースグループが[＃6787](https://github.com/tikv/pd/issues/6787) @ [栄光](https://github.com/glorv)で再初期化される可能性がある問題を修正しました。
    -   etcd がすでに起動しているがクライアントがまだ接続していない場合、クライアントを呼び出すと PD がpanic[＃6860](https://github.com/tikv/pd/issues/6860) @ [HuSharp](https://github.com/HuSharp)になる可能性がある問題を修正しました。
    -   リージョンの`health-check`出力が、リージョンID [＃6560](https://github.com/tikv/pd/issues/6560) @ [Jmポテト](https://github.com/JmPotato)をクエリして返されるリージョン情報と一致しない問題を修正しました。
    -   `unsafe recovery`で不合格になった学習者のピアが`auto-detect`モード[＃6690](https://github.com/tikv/pd/issues/6690) @ [v01dスター](https://github.com/v01dstar)で無視される問題を修正
    -   配置ルールがルール[＃6662](https://github.com/tikv/pd/issues/6662) @ [rleungx](https://github.com/rleungx)を満たさないTiFlash学習者を選択する問題を修正しました
    -   ルールチェッカーがピア[＃6559](https://github.com/tikv/pd/issues/6559) @ [ノルーシュ](https://github.com/nolouch)を選択した場合に、不健全なピアを削除できない問題を修正しました

-   TiFlash

    -   デッドロック[＃7758](https://github.com/pingcap/tiflash/issues/7758) @ [ホンユニャン](https://github.com/hongyunyan)によりTiFlash がパーティション テーブルを正常に複製できない問題を修正しました
    -   `INFORMATION_SCHEMA.TIFLASH_REPLICA`システムテーブルにユーザーがアクセス権限を持たないテーブルが含まれている問題を修正[＃7795](https://github.com/pingcap/tiflash/issues/7795) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)
    -   同じ MPP タスク内に複数の HashAgg 演算子がある場合、MPP タスクのコンパイルに非常に長い時間がかかり、クエリのパフォーマンスに重大な影響を与える可能性がある問題を修正しました[＃7810](https://github.com/pingcap/tiflash/issues/7810) @ [シーライズ](https://github.com/SeaRise)

-   ツール

    -   TiCDC

        -   PD [＃9294](https://github.com/pingcap/tiflow/issues/9294) @ [アズドンメン](https://github.com/asddongmen)が一時的に利用できないために変更フィードが失敗する問題を修正しました
        -   一部の TiCDC ノードがネットワークから分離されているときに発生する可能性のあるデータの不整合の問題を修正[＃9344](https://github.com/pingcap/tiflow/issues/9344) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)
        -   Kafka Sink がエラーに遭遇すると、changefeed の進行[＃9309](https://github.com/pingcap/tiflow/issues/9309) @ [ヒック](https://github.com/hicqu)が無期限にブロックされる可能性がある問題を修正しました。
        -   TiCDC ノードのステータスが[＃9354](https://github.com/pingcap/tiflow/issues/9354) @ [スドジ](https://github.com/sdojjy)に変化したときに発生する可能性のあるpanic問題を修正しました。
        -   デフォルトの`ENUM`値[＃9259](https://github.com/pingcap/tiflow/issues/9259) @ [3エースショーハンド](https://github.com/3AceShowHand)のエンコードエラーを修正しました

    -   TiDB Lightning

        -   TiDB Lightning がインポートを完了した後にチェックサムを実行すると SSL エラー[＃45462](https://github.com/pingcap/tidb/issues/45462) @ [D3ハンター](https://github.com/D3Hunter)が発生する可能性がある問題を修正しました
        -   論理インポートモードで、インポート中に下流のテーブルを削除すると、 TiDB Lightningメタデータが時間[＃44614](https://github.com/pingcap/tidb/issues/44614) @ [dsdashun](https://github.com/dsdashun)で更新されない可能性がある問題を修正しました。

## 寄稿者 {#contributors}

TiDB コミュニティからの以下の貢献者に感謝いたします。

-   [charleszheng44](https://github.com/charleszheng44)
-   [ディサム](https://github.com/dhysum)
-   [ハイユクス](https://github.com/haiyux)
-   [ジャンファ](https://github.com/Jiang-Hua)
-   [ジル](https://github.com/Jille)
-   [ジフハウス](https://github.com/jiyfhust)
-   [krishnaduttPanchagnula](https://github.com/krishnaduttPanchagnula)
-   [L-メープル](https://github.com/L-maple)
-   [ピンアンドビー](https://github.com/pingandb)
-   [テストウィル](https://github.com/testwill)
-   [ティソンクン](https://github.com/tisonkun)
-   [xuyifangreeneyes](https://github.com/xuyifangreeneyes)
-   [ヤムチナ](https://github.com/yumchina)
