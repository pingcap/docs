---
title: Configure TiDB for Optimal Performance
summary: 主要な設定を構成し、特殊なケースに対処することで、TiDBのパフォーマンスを最適化する方法を学びましょう。
---

# TiDBを最適なパフォーマンスに構成する {#configure-tidb-for-optimal-performance}

このガイドでは、TiDBのパフォーマンスを最適化する方法について説明します。具体的には、以下の内容が含まれます。

-   一般的なワークロードに対するベストプラクティス。
-   困難なパフォーマンス状況に対処するための戦略。

> **注記：**
>
> このガイドで紹介する最適化手法は、TiDB の最適なパフォーマンスを実現するのに役立ちます。ただし、パフォーマンスの調整には複数の要素のバランスを取る必要があり、すべてのパフォーマンスニーズに対応できる単一のソリューションは存在しません。このガイドで紹介する手法の中には、実験的機能を使用するものがあり、それらはその旨が明記されています。これらの最適化によってパフォーマンスを大幅に向上させることは可能ですが、本番環境には適さない場合があり、実装前に慎重な評価が必要です。

## 概要 {#overview}

TiDBのパフォーマンスを最適化するには、さまざまな設定を慎重に調整する必要があります。多くの場合、最適なパフォーマンスを実現するには、デフォルト値以外の設定変更が必要となります。

デフォルト設定では、パフォーマンスよりも安定性が優先されます。パフォーマンスを最大限に引き出すには、より積極的な設定や、場合によっては実験的機能を使用する必要があるかもしれません。これらの推奨事項は、本番での導入経験とパフォーマンス最適化に関する研究に基づいています。

このガイドでは、デフォルト以外の設定について、それぞれの利点と潜在的なトレードオフを含めて説明します。この情報を活用して、ワークロードの要件に合わせてTiDBの設定を最適化してください。

## 一般的なワークロードの主要設定 {#key-settings-for-common-workloads}

TiDBのパフォーマンスを最適化するために、一般的に以下の設定が使用されます。

-   [SQL準備済み実行プランキャッシュ](/sql-prepared-plan-cache.md)などの実行プランキャッシュ[準備されていないプランキャッシュ](/sql-non-prepared-plan-cache.md)強化します[インスタンスレベルの実行プランキャッシュ](/system-variables.md#tidb_enable_instance_plan_cache-new-in-v840)
-   [オプティマイザー修正コントロール](/optimizer-fix-controls.md)を使用して TiDB オプティマイザの動作を最適化します。
-   storageエンジン[タイタン](/storage-engine/titan-overview.md)をより積極的に活用する。
-   書き込み負荷の高いワークロード下でも最適かつ安定したパフォーマンスを確保するために、TiKVの圧縮およびフロー制御の設定を微調整します。

これらの設定は、多くのワークロードのパフォーマンスを大幅に向上させることができます。ただし、他の最適化と同様に、本番に展開する前に、必ずご自身の環境で十分にテストしてください。

### システム変数 {#system-variables}

推奨設定を適用するには、以下のSQLコマンドを実行してください。

```sql
SET GLOBAL tidb_enable_instance_plan_cache=on;
SET GLOBAL tidb_instance_plan_cache_max_size=2GiB;
SET GLOBAL tidb_enable_non_prepared_plan_cache=on;
SET GLOBAL tidb_ignore_prepared_cache_close_stmt=on;
SET GLOBAL tidb_analyze_column_options='ALL';
SET GLOBAL tidb_stats_load_sync_wait=2000;
SET GLOBAL tidb_opt_limit_push_down_threshold=10000;
SET GLOBAL tidb_opt_derive_topn=on;
SET GLOBAL tidb_runtime_filter_mode=LOCAL;
SET GLOBAL tidb_opt_enable_mpp_shared_cte_execution=on;
SET GLOBAL tidb_rc_read_check_ts=on;
SET GLOBAL tidb_guarantee_linearizability=off;
SET GLOBAL pd_enable_follower_handle_region=on;
SET GLOBAL tidb_opt_fix_control = '44262:ON,44389:ON,44823:10000,44830:ON,44855:ON,52869:ON';
```

以下の表は、特定のシステム変数構成が及ぼす影響を概説したものです。

| システム変数                                                                                                                                                                                                          | 説明                                                                                                              | 注記                                                                                      |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| [`tidb_enable_instance_plan_cache`](/system-variables.md#tidb_enable_instance_plan_cache-new-in-v840)と[`tidb_instance_plan_cache_max_size`](/system-variables.md#tidb_instance_plan_cache_max_size-new-in-v840) | セッションレベルのキャッシュではなく、インスタンスレベルのプランキャッシュを使用してください。これにより、接続数が多いワークロードや、プリペアドステートメントの使用頻度が高いワークロードのパフォーマンスが大幅に向上します。 | これは実験的機能です。まずは非本番環境でテストし、プランキャッシュサイズが増加するにつれてメモリ使用量を監視してください。                           |
| [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache)                                                                                                               | プリペアドステートメントを使用しないアプリケーションのコンパイルコストを削減するには、 [準備されていないプランキャッシュ](/sql-non-prepared-plan-cache.md)機能を有効にしてください。    | 該当なし                                                                                    |
| [`tidb_ignore_prepared_cache_close_stmt`](/system-variables.md#tidb_ignore_prepared_cache_close_stmt-new-in-v600)                                                                                               | プリペアドステートメントを使用するアプリケーション向けに、実行後にプランを閉じるキャッシュプランを作成します。                                                         | 該当なし                                                                                    |
| [`tidb_analyze_column_options`](/system-variables.md#tidb_analyze_column_options-new-in-v830)                                                                                                                   | 列統計情報の欠落による最適とは言えない実行計画を回避するため、すべての列の統計情報を収集してください。                                                             | 該当なし                                                                                    |
| [`tidb_stats_load_sync_wait`](/system-variables.md#tidb_stats_load_sync_wait-new-in-v540)                                                                                                                       | 統計情報の同期読み込みのタイムアウト時間を、デフォルトの100ミリ秒から2秒に延長します。これにより、TiDBはクエリコンパイル前に必要な統計情報を確実に読み込むことができます。                       | この値を大きくすると、クエリコンパイル前の同期待機時間が長くなります。                                                     |
| [`tidb_opt_limit_push_down_threshold`](/system-variables.md#tidb_opt_limit_push_down_threshold)                                                                                                                 | `Limit`または`TopN`オペレーターをTiKVにプッシュダウンするかどうかを決定するしきい値を引き上げます。                                                      | 複数のインデックスオプションが存在する場合、この変数を増やすと、オプティマイザは`ORDER BY`と`Limit`演算子を最適化できるインデックスを優先するようになります。 |
| [`tidb_opt_derive_topn`](/system-variables.md#tidb_opt_derive_topn-new-in-v700)                                                                                                                                 | 最適化ルール[ウィンドウ関数からTopNまたはLimitを導出する](/derive-topn-from-window.md)を有効にします。                                         | これは`ROW_NUMBER()`ウィンドウ機能に限定されます。                                                        |
| [`tidb_runtime_filter_mode`](/system-variables.md#tidb_runtime_filter_mode-new-in-v720)                                                                                                                         | ハッシュ結合の効率を向上させるには、ローカルモードで[ランタイムフィルタ](/runtime-filter.md#runtime-filter-mode)有効にしてください。                         | この変数はバージョン7.2.0で導入され、安全上の理由からデフォルトでは無効になっています。                                          |
| [`tidb_opt_enable_mpp_shared_cte_execution`](/system-variables.md#tidb_opt_enable_mpp_shared_cte_execution-new-in-v720)                                                                                         | TiFlashへの非再帰的な[共通テーブル式（CTE）](/sql-statements/sql-statement-with.md)プッシュダウンを有効にします。                              | これは実験的機能です。                                                                             |
| [`tidb_rc_read_check_ts`](/system-variables.md#tidb_rc_read_check_ts-new-in-v600)                                                                                                                               | 読み取りコミット分離レベルの場合、この変数を有効にすると、グローバルタイムスタンプを取得する際のレイテンシーとコストが回避され、トランザクションレベルの読み取りレイテンシーが最適化されます。                 | この機能は、リピータブルリード分離レベルとは互換性がありません。                                                        |
| [`tidb_guarantee_linearizability`](/system-variables.md#tidb_guarantee_linearizability-new-in-v50)                                                                                                              | PDサーバーからのコミットタイムスタンプの取得をスキップすることでパフォーマンスを向上させます。                                                                | これは、線形化可能性を犠牲にしてパフォーマンスを優先するものです。因果的一貫性のみが保証されます。厳密な線形化可能性が求められるシナリオには適していません。          |
| [`pd_enable_follower_handle_region`](/system-variables.md#pd_enable_follower_handle_region-new-in-v760)                                                                                                         | PDFollower機能を有効にすると、PDフォロワーがリージョン要求を処理できるようになります。これにより、すべてのPDサーバーに負荷が均等に分散され、PDリーダーのCPU負荷が軽減されます。               | 該当なし                                                                                    |
| [`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-new-in-v653-and-v710)                                                                                                                        | 高度なクエリ最適化戦略を有効にすることで、追加の最適化ルールとヒューリスティックを通じてパフォーマンスを向上させることができます。                                               | ワークロードによってパフォーマンスの向上度合いが異なるため、ご使用の環境で十分にテストを行ってください。                                    |

以下では、追加の最適化を可能にするオプティマイザ制御構成について説明します。

-   [`44262:ON`](/optimizer-fix-controls.md#44262-new-in-v653-and-v720) : [グローバル統計](/statistics.md#collect-statistics-of-partitioned-tables-in-dynamic-pruning-mode)が欠落している場合は、 [動的プルーニングモード](/partitioned-table.md#dynamic-pruning-mode)使用してパーティションテーブルにアクセスします。
-   [`44389:ON`](/optimizer-fix-controls.md#44389-new-in-v653-and-v720) : `c = 10 and (a = 'xx' or (a = 'kk' and b = 1))`のようなフィルターの場合、 `IndexRangeScan`のより包括的なスキャン範囲を作成します。
-   [`44823:10000`](/optimizer-fix-controls.md#44823-new-in-v730) ：メモリを節約するため、プランキャッシュは、この変数で指定された数を超えるパラメータを持つクエリをキャッシュしません。長いインリストを持つクエリでもプランキャッシュを使用できるようにするには、プランキャッシュのパラメータ制限を`200`から`10000`に増やしてください。
-   [`44830:ON`](/optimizer-fix-controls.md#44830-new-in-v657-and-v730) : プランキャッシュは、物理最適化中に生成された`PointGet`演算子を含む実行プランをキャッシュすることを許可します。
-   [`44855:ON`](/optimizer-fix-controls.md#44855-new-in-v654-and-v730) : `IndexJoin`演算子の`Probe`側に`Selection`演算子が含まれている場合、オプティマイザは`IndexJoin`選択します。
-   [`52869:ON`](/optimizer-fix-controls.md#52869-new-in-v810) : オプティマイザがクエリ プランに対して (フル テーブル スキャン以外の) 単一のインデックス スキャン メソッドを選択できる場合、オプティマイザは自動的にインデックス マージを選択します。

### TiKV構成 {#tikv-configurations}

TiKV設定ファイルに以下の設定項目を追加してください。

```toml
[server]
concurrent-send-snap-limit = 64
concurrent-recv-snap-limit = 64
snap-io-max-bytes-per-sec = "400MiB"

[rocksdb]
max-manifest-file-size = "256MiB"
[rocksdb.titan]
enabled = true
[rocksdb.defaultcf.titan]
min-blob-size = "1KB"
blob-file-compression = "zstd"

[storage]
scheduler-pending-write-threshold = "512MiB"
[storage.flow-control]
l0-files-threshold = 50
soft-pending-compaction-bytes-limit = "512GiB"

[rocksdb.writecf]
level0-slowdown-writes-trigger = 20
soft-pending-compaction-bytes-limit = "192GiB"
[rocksdb.defaultcf]
level0-slowdown-writes-trigger = 20
soft-pending-compaction-bytes-limit = "192GiB"
[rocksdb.lockcf]
level0-slowdown-writes-trigger = 20
soft-pending-compaction-bytes-limit = "192GiB"
```

| コンフィグレーションアイテム                                                                                                                                                                                                                                                                       | 説明                                                                                                                                                                           | 注記                                                                                                                                                                       |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [`concurrent-send-snap-limit`](/tikv-configuration-file.md#concurrent-send-snap-limit) [`concurrent-recv-snap-limit`](/tikv-configuration-file.md#concurrent-recv-snap-limit) [`snap-io-max-bytes-per-sec`](/tikv-configuration-file.md#snap-io-max-bytes-per-sec)                   | TiKVのスケーリング操作中に、同時スナップショット転送量とI/O帯域幅の制限を設定します。制限値を高く設定すると、データ移行が高速化され、スケーリング時間が短縮されます。                                                                                       | これらの制限を調整すると、スケーリング速度とオンライン取引パフォーマンスのトレードオフに影響します。                                                                                                                       |
| [`rocksdb.max-manifest-file-size`](/tikv-configuration-file.md#max-manifest-file-size)                                                                                                                                                                                               | RocksDB マニフェストファイルの最大サイズを設定します。このファイルには、SST ファイルとデータベースの状態変更に関するメタデータが記録されます。このサイズを大きくすると、マニフェストファイルの書き換え頻度が減り、フォアグラウンド書き込みパフォーマンスへの影響を最小限に抑えることができます。                       | デフォルト値は`128MiB`です。SSTファイルが多数存在する環境（例えば、数十万個）では、マニフェストファイルの書き換えが頻繁に行われると、書き込みパフォーマンスが低下する可能性があります。このパラメータを`256MiB`以上の値に調整することで、最適なパフォーマンスを維持できます。                         |
| [`rocksdb.titan`](/tikv-configuration-file.md#rocksdbtitan) [`rocksdb.defaultcf.titan`](/tikv-configuration-file.md#rocksdbdefaultcftitan) [`min-blob-size`](/tikv-configuration-file.md#min-blob-size) [`blob-file-compression`](/tikv-configuration-file.md#blob-file-compression) | Titanstorageエンジンを有効にすることで、書き込み増幅を低減し、ディスクI/Oのボトルネックを緩和できます。特に、RocksDBの圧縮処理が書き込みワークロードに追いつかず、圧縮待ちバイトが蓄積される場合に有効です。                                                            | 書き込み増幅が主なボトルネックである場合に有効にします。トレードオフは以下のとおりです。<ul><li>プライマリキー範囲スキャンにおけるパフォーマンスへの影響の可能性。</li><li>空間増幅率の向上（最悪の場合、最大2倍）。</li><li>ブロブキャッシュのための追加メモリ使用量。</li></ul>              |
| [`storage.scheduler-pending-write-threshold`](/tikv-configuration-file.md#scheduler-pending-write-threshold)                                                                                                                                                                         | TiKVスケジューラで書き込みキューの最大サイズを設定します。保留中の書き込みタスクの合計サイズがこのしきい値を超えると、TiKVは新規書き込み要求に対してエラーコード`Server Is Busy`を返します。                                                                   | デフォルト値は`100MiB`です。書き込み同時実行数が多い場合や、一時的な書き込みスパイクが発生する場合は、このしきい値を上げる（例えば`512MiB`にする）ことで負荷に対応できます。ただし、書き込みキューが継続的に蓄積され、このしきい値を超える場合は、根本的なパフォーマンスの問題が発生している可能性があり、さらに調査が必要です。 |
| [`storage.flow-control.l0-files-threshold`](/tikv-configuration-file.md#l0-files-threshold)                                                                                                                                                                                          | kvDB L0ファイルの数に基づいて、書き込みフロー制御がトリガーされるタイミングを制御します。しきい値を上げると、書き込み負荷が高い場合の書き込み停止が減少します。                                                                                          | しきい値を高く設定すると、L0ファイルが多数存在する場合に、より積極的な圧縮処理が行われる可能性があります。                                                                                                                   |
| [`storage.flow-control.soft-pending-compaction-bytes-limit`](/tikv-configuration-file.md#soft-pending-compaction-bytes-limit)                                                                                                                                                        | 書き込みフロー制御を管理するために、保留中の圧縮バイトのしきい値を制御します。ソフトリミットを設定すると、部分的な書き込み拒否が発生します。                                                                                                       | デフォルトのソフトリミットは`192GiB`です。書き込み負荷の高いシナリオでは、圧縮処理が追いつかない場合、保留中の圧縮バイトが蓄積され、フロー制御がトリガーされる可能性があります。リミットを調整することでバッファ領域を増やすことができますが、蓄積が続く場合は、さらなる調査が必要な根本的な問題があることを示しています。        |
| [`rocksdb.(defaultcf|writecf|lockcf).level0-slowdown-writes-trigger`](/tikv-configuration-file.md#level0-slowdown-writes-trigger)と[`rocksdb.(defaultcf|writecf|lockcf).soft-pending-compaction-bytes-limit`](/tikv-configuration-file.md#soft-pending-compaction-bytes-limit-1)      | `level0-slowdown-writes-trigger`と`soft-pending-compaction-bytes-limit`デフォルト値に手動で設定する必要があります。こうすることで、フロー制御パラメータの影響を受けなくなります。さらに、Rocksdbパラメータを設定して、デフォルトパラメータと同じ圧縮効率を維持してください。 | 詳細については、 [第18708号](https://github.com/tikv/tikv/issues/18708)参照してください。                                                                                                   |

前述の表に示されている圧縮およびフロー制御構成の調整は、以下の仕様を持つインスタンスへの TiKV デプロイメントに合わせて調整されていることに注意してください。

-   CPU: 32コア
-   メモリ: 128 GiB
-   ストレージ: 5 TiB EBS
-   ディスクスループット：1 GiB/秒

#### 書き込み負荷の高いワークロードに対する推奨構成調整 {#recommended-configuration-adjustments-for-write-intensive-workloads}

書き込み負荷の高いワークロードにおける TiKV のパフォーマンスと安定性を最適化するには、インスタンスのハードウェア仕様に基づいて、特定の圧縮およびフロー制御パラメータを調整することをお勧めします。例:

-   [`rocksdb.rate-bytes-per-sec`](/tikv-configuration-file.md#rate-bytes-per-sec) : 通常はデフォルト値を使用します。圧縮 I/O がディスク帯域幅のかなりの割合を消費していることに気づいた場合は、レートをディスクの最大スループットの約 60% に制限することを検討してください。これにより、圧縮作業のバランスが取れ、ディスクが飽和状態にならないようになります。たとえば、 **1 GiB/s**の定格のディスクでは、これを約`600MiB`に設定します。

-   [`storage.flow-control.soft-pending-compaction-bytes-limit`](/tikv-configuration-file.md#soft-pending-compaction-bytes-limit-1)と[`storage.flow-control.hard-pending-compaction-bytes-limit`](/tikv-configuration-file.md#hard-pending-compaction-bytes-limit-1) ：これらの制限を、利用可能なディスク容量に比例して増やします（例えば、それぞれ1 TiBと2 TiB）。これにより、圧縮処理のためのバッファが増えます。

これらの設定は、リソースの効率的な利用を確保し、書き込み負荷がピークに達した際の潜在的なボトルネックを最小限に抑えるのに役立ちます。

> **注記：**
>
> TiKVは、システムの安定性を確保するために、スケジューラレイヤーでフロー制御を実装しています。保留中の圧縮バイト数や書き込みキューサイズなどの重要なしきい値を超えると、TiKVは書き込み要求を拒否し、ServerIsBusyエラーを返します。このエラーは、バックグラウンドの圧縮プロセスがフォアグラウンドの書き込み操作の現在の速度に追いつけないことを示しています。フロー制御が有効になると、通常、レイテンシーの急増とクエリスループットの低下（QPSの低下）が発生します。これらのパフォーマンス低下を防ぐには、包括的なキャパシティプランニングと、圧縮パラメータおよびstorage設定の適切な構成が不可欠です。

### TiFlash -学習者向け設定 {#tiflash-learner-configurations}

TiFlash-learner 設定ファイルに以下の設定項目を追加してください。

```toml
[server]
snap-io-max-bytes-per-sec = "300MiB"
```

| コンフィグレーションアイテム                                                                       | 説明                                                                                             | 注記                                                                             |
| ------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| [`snap-io-max-bytes-per-sec`](/tikv-configuration-file.md#snap-io-max-bytes-per-sec) | TiKVからTiFlashへのデータレプリケーションにおける、最大許容ディスク帯域幅を制御します。制限値を高く設定すると、初期データロードとキャッチアップレプリケーションが高速化されます。 | 帯域幅の消費量が増加すると、オンライン取引のパフォーマンスに影響が出る可能性があります。レプリケーション速度とシステム安定性のバランスを取ることが重要です。 |

## ベンチマーク {#benchmark}

このセクションでは、デフォルト設定（ベースライン）と前述の[一般的な負荷に対する主要な設定](#key-settings-for-common-workloads)に基づいて最適化された設定のパフォーマンスを比較します。

### 1000個のテーブルに対するSysbenchワークロード {#sysbench-workloads-on-1000-tables}

#### テスト環境 {#test-environment}

テスト環境は以下のとおりです。

-   TiDBサーバー3台（16コア、64GiB）
-   TiKVサーバー3台（16コア、64GiB）
-   TiDBバージョン：v8.4.0
-   作業負荷: [sysbench oltp_read_only](https://github.com/akopytov/sysbench/blob/master/src/lua/oltp_read_only.lua)

#### 性能比較 {#performance-comparison}

以下の表は、ベースライン設定と最適化設定におけるスループット、レイテンシー、およびプランキャッシュヒット率を比較したものです。

| メトリック                 | ベースライン | 最適化済み   | 改善      |
| --------------------- | ------ | ------- | ------- |
| QPS                   | 89,100 | 100,128 | +12.38% |
| 平均レイテンシー（ミリ秒）         | 35.87  | 31.92   | -11.01% |
| P95レイテンシー（ms）         | 58.92  | 51.02   | -13.41% |
| プランキャッシュヒット率（％）       | 56.89% | 87.51%  | +53.82% |
| キャッシュメモリ使用量（MiB）を計画する | 95.3   | 70.2    | -26.34% |

#### 主なメリット {#key-benefits}

インスタンスプランキャッシュは、ベースライン構成と比較して大幅なパフォーマンス向上を実現しています。

-   ヒット率の向上：53.82%増加（56.89%から87.51%へ）。
-   メモリ使用量の削減：26.34%減少（95.3 MiBから70.2 MiBへ）。
-   パフォーマンスの向上：

    -   QPSは12.38%増加する。
    -   平均レイテンシーは11.01%減少します。
    -   P95のレイテンシーは13.41%減少する。

#### 仕組み {#how-it-works}

インスタンスプランキャッシュは、以下のメカニズムを通じてパフォーマンスを向上させます。

-   メモリ内の`SELECT`ステートメントの実行プランをキャッシュします。
-   同じ TiDB インスタンス上のすべての接続 (最大 200) 間で、キャッシュされたプランを共有します。
-   1,000個のテーブルにわたって、最大5,000 `SELECT`ステートメントのプランを効率的に保存できます。
-   キャッシュミスは主に`BEGIN`と`COMMIT`ステートメントの場合にのみ発生します。

#### 実生活におけるメリット {#real-world-benefits}

シンプルなsysbench `oltp_read_only`クエリ（プランあたり14KB）を使用したベンチマークではわずかな改善しか見られませんが、実際のアプリケーションではより大きな効果が期待できます。

-   複雑なクエリは最大20倍高速に実行できます。
-   セッションレベルのプランキャッシュと比較して、メモリ使用量がより効率的です。

インスタンスプランキャッシュは、特に以下のようなシステムに効果的です。

-   列数の多い大きな表。
-   複雑なSQLクエリ。
-   同時接続数が多い。
-   多様なクエリパターン。

#### メモリ効率 {#memory-efficiency}

インスタンスプランキャッシュは、セッションレベルのプランキャッシュよりもメモリ効率が優れています。その理由は次のとおりです。

-   プランはすべての接続で共有されます
-   各セッションごとに計画を複製する必要はありません
-   より高いヒット率を維持しながら、メモリ利用効率を向上させる。

複数の接続と複雑なクエリが発生するシナリオでは、セッションレベルのプランキャッシュでは同等のヒット率を達成するために相当量のメモリが必要となるため、インスタンスプランキャッシュの方が効率的な選択肢となります。

![Instance plan cache: Queries Using Plan Cache OPS](/media/performance/instance-plan-cache.png)

#### テストワークロード {#test-workload}

以下の`sysbench oltp_read_only prepare`コマンドでデータが読み込まれます。

```bash
sysbench oltp_read_only prepare --mysql-host={host} --mysql-port={port} --mysql-user=root --db-driver=mysql --mysql-db=test --threads=100 --time=900 --report-interval=10 --tables=1000 --table-size=10000
```

以下の`sysbench oltp_read_only run`コマンドでワークロードが実行されます。

```bash
sysbench oltp_read_only run --mysql-host={host} --mysql-port={port} --mysql-user=root --db-driver=mysql --mysql-db=test --threads=200 --time=900 --report-interval=10 --tables=1000 --table-size=10000
```

詳細については、 [Sysbenchを使用してTiDBをテストする方法](/benchmark/benchmark-tidb-using-sysbench.md)参照してください。

### YCSBの大規模レコード値に関するワークロード {#ycsb-workloads-on-large-record-value}

#### テスト環境 {#test-environment}

テスト環境は以下のとおりです。

-   TiDBサーバー3台（16コア、64GiB）
-   TiKVサーバー3台（16コア、64GiB）
-   TiDBバージョン：v8.4.0
-   作業負荷: [go-ycsbワークロード](https://github.com/pingcap/go-ycsb/blob/master/workloads/workloada)

#### 性能比較 {#performance-comparison}

以下の表は、基準設定と最適化設定におけるスループット（1秒あたりの処理回数）を比較したものです。

| アイテム      | ベースライン（OPS） | 最適化済み（OPS） | 改善       |
| --------- | ----------- | ---------- | -------- |
| データをロードする | 2858.5      | 5074.3     | +77.59%  |
| 作業負荷      | 2243.0      | 12804.3    | +470.86% |

#### パフォーマンス分析 {#performance-analysis}

バージョン7.6.0以降、Titanはデフォルトで有効になっています。TiDB v8.4.0では、Titanのデフォルト値は`min-blob-size`ですが、現在は`32KiB`なっています。ベースライン構成では、レコードサイズを`31KiB`に設定することで、データがRocksDBに保存されるようにしています。一方、キー設定構成では、 `min-blob-size` ～ `1KiB`に設定すると、データがTitanに保存されます。

主要設定で確認されたパフォーマンスの向上は、主にTitanがRocksDBの圧縮を削減する能力によるものです。以下の図に示すように、

-   ベースライン：RocksDBの圧縮処理の総スループットは1 GiB/sを超え、ピーク時には3 GiB/sを超える。
-   主な設定：RocksDBの圧縮処理のピークスループットは100 MiB/sを下回っています。

この圧縮処理オーバーヘッドの大幅な削減は、主要設定構成で見られる全体的なスループットの向上に貢献しています。

![Titan RocksDB compaction:](/media/performance/titan-rocksdb-compactions.png)

#### テストワークロード {#test-workload}

以下のコマンド`go-ycsb load`データが読み込まれます。

```bash
go-ycsb load mysql -P /ycsb/workloads/workloada -p {host} -p mysql.port={port} -p threadcount=100 -p recordcount=5000000 -p operationcount=5000000 -p workload=core -p requestdistribution=uniform -pfieldcount=31 -p fieldlength=1024
```

以下の`go-ycsb run`コマンドでワークロードが実行されます。

```bash
go-ycsb run mysql -P /ycsb/workloads/workloada -p {host} -p mysql.port={port} -p mysql.db=test -p threadcount=100 -p recordcount=5000000 -p operationcount=5000000 -p workload=core -prequestdistribution=uniform -p fieldcount=31 -p fieldlength=1024
```

## エッジケースと最適化 {#edge-cases-and-optimizations}

このセクションでは、基本的な最適化を超えた、より的を絞った調整が必要な特定のシナリオに合わせてTiDBを最適化する方法を説明します。特定のユースケースに合わせてTiDBを調整する方法を習得できます。

### エッジケースを特定する {#identify-edge-cases}

例外的なケースを特定するには、以下の手順を実行してください。

1.  クエリパターンとワークロード特性を分析する。
2.  システム指標を監視して、パフォーマンスのボトルネックを特定します。
3.  アプリケーション開発チームから、具体的な問題点に関するフィードバックを収集する。

### 一般的なエッジケース {#common-edge-cases}

以下に、よくある例外的なケースをいくつか挙げます。

-   高頻度の小さなクエリに対して、TSOは高い待機時間を設ける。
-   さまざまなワークロードに適した最大チャンクサイズを選択してください。
-   読み込み負荷の高いワークロード向けにコプロセッサキャッシュを調整する
-   ワークロード特性に合わせてチャンクサイズを最適化
-   さまざまなワークロードに合わせてトランザクションモードとDMLタイプを最適化する
-   TiKVプッシュダウンによる`GROUP BY`および`DISTINCT`オペレーションの最適化
-   インメモリエンジンを使用してMVCCバージョンの蓄積を軽減する
-   バッチ処理中の統計情報収集を最適化する
-   インスタンスの種類ごとにスレッドプールの設定を最適化する

以下のセクションでは、これらの各ケースへの対処方法について説明します。それぞれのシナリオに応じて、異なるパラメータを調整したり、特定のTiDB機能を使用したりする必要があります。

> **注記：**
>
> これらの最適化は、使用状況やデータパターンによって効果が異なる可能性があるため、慎重に適用し、徹底的にテストしてください。

### 高頻度の小さなクエリに対して、TSOは高い待機時間を設ける。 {#high-tso-wait-for-high-frequency-small-queries}

#### トラブルシューティング {#troubleshooting}

ワークロードに頻繁に発生する小規模なトランザクションや、タイムスタンプを頻繁に要求するクエリが含まれる場合、 [TSO（タイムスタンプオラクル）](/glossary.md#timestamp-oracle-tso)パフォーマンスのボトルネックになる可能性があります。TSO の待機時間がシステムに影響を与えているかどうかを確認するには、 [**パフォーマンス概要 &gt; SQL実行時間概要**](/grafana-performance-overview-dashboard.md#sql-execute-time-overview)パネルを確認してください。TSO の待機時間が SQL 実行時間の大部分を占める場合は、次の最適化を検討してください。

-   厳密な一貫性を必要としない読み取り操作には、低精度TSO（ [`tidb_low_resolution_tso`](/system-variables.md#tidb_low_resolution_tso)を有効にする）を使用します。詳細については、 [解決策1：低精度TSOを使用する](#solution-1-low-precision-tso)参照してください。
-   可能な場合は、小さな取引をまとめて大きな取引にします。詳細については、 [解決策2：TSO要求の並列モード](#solution-2-parallel-mode-for-tso-requests)参照してください。

#### 解決策1：低精度TSO {#solution-1-low-precision-tso}

低精度TSO機能（ [`tidb_low_resolution_tso`](/system-variables.md#tidb_low_resolution_tso) ）を有効にすることで、TSOの待ち時間を短縮できます。この機能を有効にすると、TiDBはキャッシュされたタイムスタンプを使用してデータを読み取り、TSOの待ち時間を短縮しますが、その代償として古いデータを読み取る可能性があります。

この最適化は、特に以下のシナリオで効果を発揮します。

-   読み込み負荷の高いワークロードで、多少の古さは許容範囲内。
-   クエリのレイテンシーを削減することが、絶対的な一貫性よりも重要なシナリオ。
-   最新のコミット状態から数秒遅れた読み取りを許容できるアプリケーション。

メリットとデメリット：

-   キャッシュされたTSOを使用して古いデータの読み取りを有効にすることで、クエリのレイテンシーを削減し、新しいタイムスタンプを要求する必要性をなくします。
-   パフォーマンスとデータの一貫性のバランスを取る：この機能は、古い読み取りデータが許容されるシナリオにのみ適しています。厳密なデータの一貫性が求められる場合には、使用を推奨しません。

この最適化を有効にするには：

```sql
SET GLOBAL tidb_low_resolution_tso=ON;
```

#### 解決策2：TSO要求の並列モード {#solution-2-parallel-mode-for-tso-requests}

システム変数[`tidb_tso_client_rpc_mode`](/system-variables.md#tidb_tso_client_rpc_mode-new-in-v840)は、TiDBがPDにTSO RPCリクエストを送信するモードを切り替えます。デフォルト値は`DEFAULT`です。以下の条件を満たす場合、パフォーマンス向上の可能性を考慮して、この変数を`PARALLEL`または`PARALLEL-FAST`に切り替えることを検討してください。

-   TSOの待機時間は、SQLクエリの総実行時間の大部分を占める。
-   PDにおけるTSOの割り当ては、まだボトルネックに達していません。
-   PDノードとTiDBノードは十分なCPUリソースを備えています。
-   TiDBとPD間のネットワークレイテンシーは、PDがTSOを割り当てるのにかかる時間よりもかなり長い（つまり、TSO RPCの実行時間の大部分はネットワークレイテンシーによるものである）。
    -   TSO RPCリクエストの所要時間を取得するには、Grafana TiDBダッシュボードのPDクライアントセクションにある**PD TSO RPC所要時間**パネルを確認してください。
    -   PD TSO割り当ての期間を確認するには、Grafana PDダッシュボードのTiDBセクションにある**PDサーバーTSOハンドル期間**パネルを確認してください。
-   TiDBとPD間のTSO RPCリクエストの増加（ `PARALLEL`の場合は2倍、 `PARALLEL-FAST`の場合は4倍）によって生じる追加のネットワークトラフィックは許容範囲内です。

並列モードを切り替えるには、次のコマンドを実行してください。

```sql
-- Use the PARALLEL mode
SET GLOBAL tidb_tso_client_rpc_mode=PARALLEL;

-- Use the PARALLEL-FAST mode
SET GLOBAL tidb_tso_client_rpc_mode=PARALLEL-FAST;
```

### 読み込み負荷の高いワークロード向けにコプロセッサキャッシュを調整する {#tune-coprocessor-cache-for-read-heavy-workloads}

[コプロセッサキャッシュ](/coprocessor-cache.md)キャッシュを最適化することで、読み取り負荷の高いワークロードのクエリ パフォーマンスを向上させることができます。このキャッシュにはコプロセッサのリクエスト結果が格納され、頻繁にアクセスされるデータの繰り返し計算が削減されます。キャッシュのパフォーマンスを最適化するには、次の手順を実行します。

1.  [コプロセッサーキャッシュ](/coprocessor-cache.md#view-the-grafana-monitoring-panel)で説明した指標を使用してキャッシュヒット率を監視します。
2.  キャッシュサイズを増やすことで、より大きなワーキングセットにおけるヒット率を向上させることができます。
3.  クエリパターンに基づいて、承認基準値を調整する。

以下に、読み込み負荷の高いワークロード向けに推奨される設定例をいくつか示します。

```toml
[tikv-client.copr-cache]
capacity-mb = 4096
admission-max-ranges = 5000
admission-max-result-mb = 10
admission-min-process-ms = 0
```

### ワークロード特性に合わせてチャンクサイズを最適化 {#optimize-chunk-size-for-workload-characteristics}

システム変数[`tidb_max_chunk_size`](/system-variables.md#tidb_max_chunk_size)は、実行プロセス中にチャンク内の最大行数を設定します。ワークロードに応じてこの値を調整することで、パフォーマンスを向上させることができます。

-   同時実行数が多くトランザクション数が少ないOLTPワークロードの場合：

    -   値を`128`から`256`行の間で設定してください（デフォルト値は`1024`です）。
    -   これによりメモリ使用量が削減され、制限クエリの処理速度が向上します。
    -   使用例：ポイントクエリ、小範囲スキャン。

    ```sql
    SET GLOBAL tidb_max_chunk_size = 128;
    ```

-   複雑なクエリと大規模な結果セットを伴うOLAPまたは分析ワークロードの場合：

    -   値を`1024`から`4096`行の間で設定してください。
    -   これにより、大量のデータをスキャンする際のスループットが向上します。
    -   使用例：集計処理、大規模テーブルのスキャン。

    ```sql
    SET GLOBAL tidb_max_chunk_size = 4096;
    ```

### さまざまなワークロードに合わせてトランザクションモードとDMLタイプを最適化する {#optimize-transaction-mode-and-dml-type-for-different-workloads}

TiDBは、さまざまなワークロードパターンに合わせてパフォーマンスを最適化するために、複数のトランザクションモードとDML実行タイプを提供します。

#### トランザクションモード {#transaction-modes}

トランザクションモードは、システム変数[`tidb_txn_mode`](/system-variables.md#tidb_txn_mode)を使用して設定できます。

-   [悲観的な取引モード](/pessimistic-transaction.md) （デフォルト）：

    -   書き込み競合が発生する可能性のある一般的なワークロードに適しています。
    -   より強力な一貫性保証を提供します。

    ```sql
    SET SESSION tidb_txn_mode = "pessimistic";
    ```

-   [楽観的な取引モード](/optimistic-transaction.md) :

    -   書き込み競合が最小限のワークロードに適しています。
    -   複数明細の取引におけるパフォーマンスが向上しました。
    -   例： `BEGIN; INSERT...; INSERT...; COMMIT;` .

    ```sql
    SET SESSION tidb_txn_mode = "optimistic";
    ```

#### DMLタイプ {#dml-types}

バージョン8.0.0で導入されたシステム変数[`tidb_dml_type`](/system-variables.md#tidb_dml_type-new-in-v800)を使用して、DMLステートメントの実行モードを制御できます。

バルクDML実行モードを使用するには、 `tidb_dml_type` ～ `"bulk"`に設定します。このモードでは、競合のないバルクデータロードが最適化され、大規模な書き込み操作中のメモリ使用量が削減されます。このモードを使用する前に、以下の点を確認してください。

-   [`autocommit`](/system-variables.md#autocommit)が有効です。
-   [`pessimistic-auto-commit`](/tidb-configuration-file.md#pessimistic-auto-commit-new-in-v600)設定項目は`false`に設定されています。

```sql
SET SESSION tidb_dml_type = "bulk";
```

### TiKVプッシュダウンを使用して<code>GROUP BY</code>および<code>DISTINCT</code>操作を最適化します {#optimize-code-group-by-code-and-code-distinct-code-operations-with-tikv-pushdown}

TiDBは集計処理をTiKVにプッシュダウンすることで、データ転送と処理のオーバーヘッドを削減します。パフォーマンスの向上度合いは、データの特性によって異なります。

#### 使用シナリオ {#usage-scenarios}

-   **理想的なシナリオ**（高いパフォーマンス向上）：
    -   異なる値が少ない列（NDVが低い）。
    -   重複値が頻繁に含まれるデータ。
    -   例：ステータス列、カテゴリコード、日付部分。

-   **理想的でないシナリオ**（潜在的なパフォーマンス低下）：
    -   ほとんどが一意の値を含む列（NDVが高い）。
    -   固有の識別子またはタイムスタンプ。
    -   例：ユーザーID、トランザクションID。

#### コンフィグレーション {#configuration}

セッションレベルまたはグローバルレベルでプッシュダウン最適化を有効にする：

```sql
-- Enable regular aggregation pushdown
SET GLOBAL tidb_opt_agg_push_down = ON;

-- Enable distinct aggregation pushdown
SET GLOBAL tidb_opt_distinct_agg_push_down = ON;
```

### インメモリエンジンを使用してMVCCバージョンの蓄積を軽減する {#mitigate-mvcc-version-accumulation-using-in-memory-engine}

MVCC のバージョンが多すぎると、特に読み書き頻度の高い領域や、ガベージコレクションと圧縮の問題により、パフォーマンスのボトルネックが発生する可能性があります。この問題を軽減するには、v8.5.0 で導入されたバージョン[TiKV MVCC インメモリエンジン (IME)](/tikv-in-memory-engine.md)使用できます。これを有効にするには、TiKV 設定ファイルに次の設定を追加してください。

> **注記：**
>
> インメモリエンジンは、過剰なMVCCバージョンの影響を軽減するのに役立ちますが、メモリ使用量が増加する可能性があります。この機能を有効にした後は、システムを監視してください。

```toml
[in-memory-engine]
enable = true
```

### バッチ処理中の統計情報収集を最適化する {#optimize-statistics-collection-during-batch-operations}

統計情報の収集を管理することで、クエリの最適化を維持しながら、バッチ処理中のパフォーマンスを向上させることができます。このセクションでは、このプロセスを効果的に管理する方法について説明します。

#### auto analyzeを無効にするタイミング {#when-to-disable-auto-analyze}

以下のシナリオでは、システム変数[`tidb_enable_auto_analyze`](/system-variables.md#tidb_enable_auto_analyze-new-in-v610) `OFF`に設定することでauto analyzeを無効にできます。

-   大量のデータインポート時。
-   一括更新処理中。
-   時間制約のあるバッチ処理向け。
-   統計情報の収集タイミングを完全に制御する必要がある場合。

#### ベストプラクティス {#best-practices}

-   バッチ処理の前に：

    ```sql
    -- Disable auto analyze
    SET GLOBAL tidb_enable_auto_analyze = OFF;
    ```

-   バッチ処理後：

    ```sql
    -- Manually collect statistics
    ANALYZE TABLE your_table;

    -- Re-enable auto analyze
    SET GLOBAL tidb_enable_auto_analyze = ON;
    ```

### インスタンスの種類ごとにスレッドプールの設定を最適化する {#optimize-thread-pool-settings-for-different-instance-types}

TiKVのパフォーマンスを向上させるには、インスタンスのCPUリソースに基づいてスレッドプールを設定してください。以下のガイドラインは、これらの設定を最適化するのに役立ちます。

-   8～16コアのインスタンスの場合、デフォルト設定で通常は十分です。

-   32コア以上のインスタンスでは、リソース利用効率を向上させるためにプールサイズを増やしてください。設定は以下のように調整してください。

    ```toml
    [server]
    # Increase gRPC thread pool 
    grpc-concurrency = 10

    [raftstore]
    # Optimize for write-intensive workloads
    apply-pool-size = 4
    store-pool-size = 4
    store-io-pool-size = 2
    ```
