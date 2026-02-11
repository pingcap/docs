---
title: Configure TiDB for Optimal Performance
summary: 主要な設定を構成し、エッジケースに対処して、TiDB のパフォーマンスを最適化する方法を学習します。
---

# 最適なパフォーマンスを得るための TiDB の設定 {#configure-tidb-for-optimal-performance}

このガイドでは、次の内容を含め、TiDB のパフォーマンスを最適化する方法について説明します。

-   一般的なワークロードのベスト プラクティス。
-   困難なパフォーマンス シナリオを処理するための戦略。

> **注記：**
>
> このガイドで紹介する最適化手法は、TiDB で最適なパフォーマンスを実現するのに役立ちます。ただし、パフォーマンスチューニングでは複数の要素のバランスを取る必要がある場合が多く、単一のソリューションですべてのパフォーマンスニーズに対応できるものはありません。このガイドの一部の手法では実験的機能を使用しており、その旨が明記されています。これらの最適化はパフォーマンスを大幅に向上させる可能性がありますが、本番環境には適さない可能性があり、実装前に慎重な評価が必要です。

## 概要 {#overview}

TiDBを最高のパフォーマンスに最適化するには、様々な設定を慎重に調整する必要があります。多くの場合、最適なパフォーマンスを実現するには、デフォルト値を超えて設定を調整する必要があります。

デフォルト設定では、パフォーマンスよりも安定性が優先されます。パフォーマンスを最大限に高めるには、より積極的な設定や、場合によっては実験的機能の使用が必要になる場合があります。これらの推奨事項は、本番での導入経験とパフォーマンス最適化に関する調査に基づいています。

このガイドでは、デフォルト以外の設定について、そのメリットと潜在的なトレードオフを含めて説明します。この情報を活用して、ワークロード要件に合わせてTiDB設定を最適化してください。

## 一般的なワークロードの主な設定 {#key-settings-for-common-workloads}

TiDB のパフォーマンスを最適化するために、次の設定が一般的に使用されます。

-   [SQL 準備済み実行プランキャッシュ](/sql-prepared-plan-cache.md) 、 [準備されていないプランキャッシュ](/sql-non-prepared-plan-cache.md) 、 [インスタンスレベルの実行プランキャッシュ](/system-variables.md#tidb_enable_instance_plan_cache-new-in-v840)などの実行プラン キャッシュを強化します。
-   [オプティマイザー修正コントロール](/optimizer-fix-controls.md)を使用して TiDB オプティマイザーの動作を最適化します。
-   [タイタン](/storage-engine/titan-overview.md)storageエンジンをより積極的に使用します。
-   TiKV の圧縮とフロー制御の構成を微調整して、書き込み集中型のワークロードで最適かつ安定したパフォーマンスを確保します。

これらの設定は、多くのワークロードのパフォーマンスを大幅に向上させることができます。ただし、他の最適化と同様に、本番に導入する前に、必ずご自身の環境で十分にテストしてください。

### システム変数 {#system-variables}

推奨設定を適用するには、次の SQL コマンドを実行します。

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

次の表は、特定のシステム変数の構成の影響の概要を示しています。

| システム変数                                                                                                                                                                                                          | 説明                                                                                                           | 注記                                                                                         |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ |
| [`tidb_enable_instance_plan_cache`](/system-variables.md#tidb_enable_instance_plan_cache-new-in-v840)と[`tidb_instance_plan_cache_max_size`](/system-variables.md#tidb_instance_plan_cache_max_size-new-in-v840) | セッションレベルのキャッシュではなく、インスタンスレベルのプランキャッシュを使用します。これにより、接続数が多いワークロードや、プリペアドステートメントの使用頻度が高いワークロードのパフォーマンスが大幅に向上します。 | これは実験的機能です。まずは非本番環境でテストし、プランキャッシュのサイズが増加するにつれてメモリ使用量がどのように変化するかを監視してください。                  |
| [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache)                                                                                                               | [準備されていないプランキャッシュ](/sql-non-prepared-plan-cache.md)機能を有効にすると、準備されたステートメントを使用しないアプリケーションのコンパイル コストが削減されます。    | 該当なし                                                                                       |
| [`tidb_ignore_prepared_cache_close_stmt`](/system-variables.md#tidb_ignore_prepared_cache_close_stmt-new-in-v600)                                                                                               | 準備されたステートメントを使用するが、実行ごとにプランを閉じるアプリケーションのプランをキャッシュします。                                                        | 該当なし                                                                                       |
| [`tidb_analyze_column_options`](/system-variables.md#tidb_analyze_column_options-new-in-v830)                                                                                                                   | 列統計の欠落による最適でない実行プランを回避するために、すべての列の統計を収集します。                                                                  | 該当なし                                                                                       |
| [`tidb_stats_load_sync_wait`](/system-variables.md#tidb_stats_load_sync_wait-new-in-v540)                                                                                                                       | 統計情報の同期ロードのタイムアウトを、デフォルトの100ミリ秒から2秒に増やします。これにより、TiDBはクエリのコンパイル前に必要な統計情報をロードできるようになります。                       | この値を大きくすると、クエリのコンパイル前の同期待機時間が長くなります。                                                       |
| [`tidb_opt_limit_push_down_threshold`](/system-variables.md#tidb_opt_limit_push_down_threshold)                                                                                                                 | `Limit`または`TopN`演算子を TiKV にプッシュするかどうかを決定するしきい値を増やします。                                                        | 複数のインデックス オプションが存在する場合、この変数を増やすと、オプティマイザーは`ORDER BY`と`Limit`の演算子を最適化できるインデックスを優先するようになります。 |
| [`tidb_opt_derive_topn`](/system-variables.md#tidb_opt_derive_topn-new-in-v700)                                                                                                                                 | [ウィンドウ関数からTopNまたはLimitを導出する](/derive-topn-from-window.md)の最適化ルールを有効にします。                                     | これは`ROW_NUMBER()`ウィンドウ関数に制限されます。                                                           |
| [`tidb_runtime_filter_mode`](/system-variables.md#tidb_runtime_filter_mode-new-in-v720)                                                                                                                         | ハッシュ結合の効率を向上させるには、ローカル モードで[ランタイムフィルター](/runtime-filter.md#runtime-filter-mode)有効にします。                       | この変数はバージョン 7.2.0 で導入され、安全のためデフォルトでは無効になっています。                                              |
| [`tidb_opt_enable_mpp_shared_cte_execution`](/system-variables.md#tidb_opt_enable_mpp_shared_cte_execution-new-in-v720)                                                                                         | TiFlashへの非再帰的な[共通テーブル式（CTE）](/sql-statements/sql-statement-with.md)プッシュダウンを有効にします。                           | これは実験的機能です。                                                                                |
| [`tidb_rc_read_check_ts`](/system-variables.md#tidb_rc_read_check_ts-new-in-v600)                                                                                                                               | 読み取りコミット分離レベルの場合、この変数を有効にすると、グローバル タイムスタンプの取得のレイテンシーとコストが回避され、トランザクション レベルの読み取りレイテンシーが最適化されます。               | この機能は、繰り返し可能読み取り分離レベルと互換性がありません。                                                           |
| [`tidb_guarantee_linearizability`](/system-variables.md#tidb_guarantee_linearizability-new-in-v50)                                                                                                              | PDサーバーからのコミット タイムスタンプの取得をスキップすることでパフォーマンスが向上します。                                                             | これにより、パフォーマンスを優先して線形化可能性が犠牲になります。因果一貫性のみが保証されます。厳密な線形化可能性が求められるシナリオには適していません。              |
| [`pd_enable_follower_handle_region`](/system-variables.md#pd_enable_follower_handle_region-new-in-v760)                                                                                                         | PDFollower機能を有効にすると、PDフォロワーがリージョンリクエストを処理できるようになります。これにより、すべてのPDサーバー間で負荷が均等に分散され、PDリーダーのCPU負荷が軽減されます。        | 該当なし                                                                                       |
| [`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-new-in-v653-and-v710)                                                                                                                        | 高度なクエリ最適化戦略を有効にして、追加の最適化ルールとヒューリスティックを通じてパフォーマンスを向上させます。                                                     | パフォーマンスの向上はワークロードによって異なるため、ご使用の環境で徹底的にテストしてください。                                           |

追加の最適化を可能にするオプティマイザー制御構成について次に説明します。

-   [`44262:ON`](/optimizer-fix-controls.md#44262-new-in-v653-and-v720) : [グローバルスタッツ](/statistics.md#collect-statistics-of-partitioned-tables-in-dynamic-pruning-mode)が欠落している場合は、 [動的プルーニングモード](/partitioned-table.md#dynamic-pruning-mode)使用してパーティションテーブルにアクセスします。
-   [`44389:ON`](/optimizer-fix-controls.md#44389-new-in-v653-and-v720) : `c = 10 and (a = 'xx' or (a = 'kk' and b = 1))`などのフィルターの場合は、 `IndexRangeScan`のより包括的なスキャン範囲を構築します。
-   [`44823:10000`](/optimizer-fix-controls.md#44823-new-in-v730) :メモリを節約するため、プランキャッシュはこの変数で指定された数を超えるパラメータを持つクエリをキャッシュしません。プランキャッシュのパラメータ制限を`200`から`10000`に増やすと、長い入力リストを持つクエリでもプランキャッシュを利用できるようになります。
-   [`44830:ON`](/optimizer-fix-controls.md#44830-new-in-v657-and-v730) : プラン キャッシュは、物理的な最適化中に生成された`PointGet`演算子を使用して実行プランをキャッシュできます。
-   [`44855:ON`](/optimizer-fix-controls.md#44855-new-in-v654-and-v730) : `IndexJoin`演算子の`Probe`側に`Selection`演算子が含まれている場合、オプティマイザーは`IndexJoin`選択します。
-   [`52869:ON`](/optimizer-fix-controls.md#52869-new-in-v810) : オプティマイザがクエリ プランに対して単一インデックス スキャン方式 (フル テーブル スキャン以外) を選択できる場合、オプティマイザはインデックス マージを自動的に選択します。

### TiKV構成 {#tikv-configurations}

TiKV 構成ファイルに次の構成項目を追加します。

```toml
[server]
concurrent-send-snap-limit = 64
concurrent-recv-snap-limit = 64
snap-io-max-bytes-per-sec = "400MiB"

[pessimistic-txn]
in-memory-peer-size-limit = "32MiB"
in-memory-instance-size-limit = "512MiB"

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

| コンフィグレーション項目                                                                                                                                                                                                                                                                         | 説明                                                                                                                                                                         | 注記                                                                                                                                                                                  |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`concurrent-send-snap-limit`](/tikv-configuration-file.md#concurrent-send-snap-limit) [`concurrent-recv-snap-limit`](/tikv-configuration-file.md#concurrent-recv-snap-limit) [`snap-io-max-bytes-per-sec`](/tikv-configuration-file.md#snap-io-max-bytes-per-sec)                   | TiKVスケーリング操作中の同時スナップショット転送とI/O帯域幅の制限を設定します。制限値を上げると、データ移行が高速化され、スケーリング時間が短縮されます。                                                                                           | これらの制限を調整すると、スケーリング速度とオンライン トランザクションのパフォーマンスのトレードオフに影響します。                                                                                                                          |
| [`in-memory-peer-size-limit`](/tikv-configuration-file.md#in-memory-peer-size-limit-new-in-v840)と[`in-memory-instance-size-limit`](/tikv-configuration-file.md#in-memory-instance-size-limit-new-in-v840)                                                                            | リージョンおよびTiKVインスタンスレベルで、悲観的ロックキャッシュのメモリ割り当てを制御します。ロックをメモリに保存することで、ディスクI/Oが削減され、トランザクションパフォーマンスが向上します。                                                                       | メモリ使用量を注意深く監視してください。制限値を上げるとパフォーマンスは向上しますが、メモリ消費量も増加します。                                                                                                                            |
| [`rocksdb.max-manifest-file-size`](/tikv-configuration-file.md#max-manifest-file-size)                                                                                                                                                                                               | RocksDBマニフェストファイルの最大サイズを設定します。このファイルは、SSTファイルとデータベースの状態変更に関するメタデータを記録します。このサイズを大きくすると、マニフェストファイルの書き換え頻度が減り、フォアグラウンド書き込みパフォーマンスへの影響を最小限に抑えることができます。                         | デフォルト値は`128MiB`です。SST ファイルが多数（例えば数十万）ある環境では、マニフェストの書き換えが頻繁に発生すると書き込みパフォーマンスが低下する可能性があります。このパラメータを`256MiB`以上に調整すると、最適なパフォーマンスを維持できます。                                                |
| [`rocksdb.titan`](/tikv-configuration-file.md#rocksdbtitan) [`rocksdb.defaultcf.titan`](/tikv-configuration-file.md#rocksdbdefaultcftitan) [`min-blob-size`](/tikv-configuration-file.md#min-blob-size) [`blob-file-compression`](/tikv-configuration-file.md#blob-file-compression) | Titanstorageエンジンを有効にすることで、書き込み増幅を減らし、ディスクI/Oボトルネックを緩和します。RocksDBの圧縮が書き込みワークロードに対応できず、保留中の圧縮バイトが蓄積される場合に特に役立ちます。                                                            | ライトアンプリフィケーションが主なボトルネックになっている場合は、これを有効にしてください。トレードオフには以下のものがあります。<ul><li>主キー範囲スキャンに潜在的なパフォーマンスの影響が及ぶ可能性があります。</li><li>空間増幅の増加（最悪の場合最大 2 倍）。</li><li> BLOB キャッシュの追加メモリ使用量。</li></ul> |
| [`storage.scheduler-pending-write-threshold`](/tikv-configuration-file.md#scheduler-pending-write-threshold)                                                                                                                                                                         | TiKVスケジューラの書き込みキューの最大サイズを設定します。保留中の書き込みタスクの合計サイズがこのしきい値を超えると、TiKVは新しい書き込み要求に対してエラー`Server Is Busy`を返します。                                                                   | デフォルト値は`100MiB`です。書き込み同時実行数が多い場合や、書き込みが一時的に急増するシナリオでは、このしきい値を大きく（例えば`512MiB`に）することで負荷に対応しやすくなります。ただし、書き込みキューが蓄積し続け、このしきい値を継続的に超える場合は、根本的なパフォーマンスの問題を示している可能性があり、さらなる調査が必要です。        |
| [`storage.flow-control.l0-files-threshold`](/tikv-configuration-file.md#l0-files-threshold)                                                                                                                                                                                          | kvDB L0ファイルの数に基づいて、書き込みフロー制御のトリガータイミングを制御します。しきい値を上げると、書き込みワークロードが高い場合の書き込みストールが減少します。                                                                                     | しきい値を高くすると、多くの L0 ファイルが存在する場合により積極的な圧縮が行われる可能性があります。                                                                                                                                |
| [`storage.flow-control.soft-pending-compaction-bytes-limit`](/tikv-configuration-file.md#soft-pending-compaction-bytes-limit)                                                                                                                                                        | 書き込みフロー制御を管理するために、保留中の圧縮バイト数のしきい値を制御します。ソフトリミットは部分的な書き込み拒否をトリガーします。                                                                                                        | デフォルトのソフトリミットは`192GiB`です。書き込み負荷の高いシナリオでは、コンパクションプロセスが追いつかず、保留中のコンパクションバイトが蓄積され、フロー制御がトリガーされる可能性があります。リミットを調整することでバッファスペースを増やすことができますが、継続的に蓄積されている場合は、根本的な問題が示唆されており、さらなる調査が必要です。    |
| [`rocksdb.(defaultcf|writecf|lockcf).level0-slowdown-writes-trigger`](/tikv-configuration-file.md#level0-slowdown-writes-trigger)と[`rocksdb.(defaultcf|writecf|lockcf).soft-pending-compaction-bytes-limit`](/tikv-configuration-file.md#soft-pending-compaction-bytes-limit-1)      | `level0-slowdown-writes-trigger`と`soft-pending-compaction-bytes-limit`手動でデフォルト値に戻す必要があります。これにより、フロー制御パラメータの影響を受けなくなります。さらに、Rocksdbパラメータをデフォルトパラメータと同じ圧縮効率を維持するように設定してください。 | 詳細については[問題 18708](https://github.com/tikv/tikv/issues/18708)参照してください。                                                                                                               |

上の表で概説した圧縮およびフロー制御の構成調整は、次の仕様のインスタンス上の TiKV デプロイメントに合わせて調整されていることに注意してください。

-   CPU: 32コア
-   メモリ: 128 GiB
-   ストレージ: 5 TiB EBS
-   ディスクスループット: 1 GiB/秒

#### 書き込み集中型のワークロードに推奨される構成調整 {#recommended-configuration-adjustments-for-write-intensive-workloads}

書き込み集中型のワークロードにおける TiKV のパフォーマンスと安定性を最適化するには、インスタンスのハードウェア仕様に基づいて、特定のコンパクションおよびフロー制御パラメータを調整することをお勧めします。例:

-   [`rocksdb.rate-bytes-per-sec`](/tikv-configuration-file.md#rate-bytes-per-sec) : 通常はデフォルト値を使用します。コンパクションI/Oがディスク帯域幅の大部分を消費していることに気付いた場合は、ディスクの最大スループットの約60%にレートを制限することを検討してください。これにより、コンパクション作業のバランスが取れ、ディスクが飽和状態になるのを防ぐことができます。例えば、 **1 GiB/s**のディスクでは、この値を約`600MiB`に設定します。

-   [`storage.flow-control.soft-pending-compaction-bytes-limit`](/tikv-configuration-file.md#soft-pending-compaction-bytes-limit-1)および[`storage.flow-control.hard-pending-compaction-bytes-limit`](/tikv-configuration-file.md#hard-pending-compaction-bytes-limit-1) : 使用可能なディスク容量に比例してこれらの制限を増やし (たとえば、それぞれ 1 TiB と 2 TiB)、圧縮プロセス用のバッファを増やします。

これらの設定は、効率的なリソース使用を保証し、ピーク時の書き込み負荷時に潜在的なボトルネックを最小限に抑えるのに役立ちます。

> **注記：**
>
> TiKVは、システムの安定性を確保するために、スケジューラレイヤーでフロー制御を実装しています。保留中の圧縮バイト数や書き込みキューサイズなどの重要なしきい値を超えると、TiKVは書き込み要求を拒否し、ServerIsBusyエラーを返します。このエラーは、バックグラウンドの圧縮プロセスがフォアグラウンドの書き込み操作の現在の速度に追いつけないことを示します。フロー制御を有効にすると、通常、レイテンシーとクエリスループットの低下（QPSの低下）が発生します。こうしたパフォーマンスの低下を防ぐには、包括的なキャパシティプランニングに加え、圧縮パラメータとstorage設定を適切に構成することが不可欠です。

### TiFlash-学習者構成 {#tiflash-learner-configurations}

TiFlash-learner 構成ファイルに次の構成項目を追加します。

```toml
[server]
snap-io-max-bytes-per-sec = "300MiB"
```

| コンフィグレーション項目                                                                         | 説明                                                                                           | 注記                                                                               |
| ------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| [`snap-io-max-bytes-per-sec`](/tikv-configuration-file.md#snap-io-max-bytes-per-sec) | TiKVからTiFlashへのデータレプリケーションにおける最大許容ディスク帯域幅を制御します。上限を高く設定すると、初期データロードとキャッチアップレプリケーションが高速化されます。 | 帯域幅の消費量が多いと、オンライントランザクションのパフォーマンスに影響する可能性があります。レプリケーション速度とシステムの安定性のバランスをとってください。 |

## ベンチマーク {#benchmark}

このセクションでは、デフォルト設定 (ベースライン) と、前述の[一般的な負荷のキー設定](#key-settings-for-common-workloads)に基づいて最適化された設定のパフォーマンスを比較します。

### 1000 個のテーブルに対する Sysbench ワークロード {#sysbench-workloads-on-1000-tables}

#### テスト環境 {#test-environment}

テスト環境は次のとおりです。

-   3 台の TiDB サーバー (16 コア、64 GiB)
-   3 台の TiKV サーバー (16 コア、64 GiB)
-   TiDB バージョン: v8.4.0
-   ワークロード: [sysbench oltp_read_only](https://github.com/akopytov/sysbench/blob/master/src/lua/oltp_read_only.lua)

#### パフォーマンス比較 {#performance-comparison}

次の表は、ベースライン設定と最適化設定の間のスループット、レイテンシー、およびプラン キャッシュ ヒット率を比較しています。

| メトリック                 | ベースライン | 最適化     | 改善      |
| --------------------- | ------ | ------- | ------- |
| QPS                   | 89,100 | 100,128 | +12.38% |
| 平均レイテンシー（ミリ秒）         | 35.87  | 31.92   | -11.01% |
| P95レイテンシー(ミリ秒)        | 58.92  | 51.02   | -13.41% |
| プランキャッシュヒット率（％）       | 56.89% | 87.51%  | +53.82% |
| プランのキャッシュメモリ使用量 (MiB) | 95.3   | 70.2    | -26.34% |

#### 主なメリット {#key-benefits}

インスタンス プラン キャッシュは、ベースライン構成に比べてパフォーマンスが大幅に向上します。

-   ヒット率の向上：53.82% 増加（56.89% から 87.51% に増加）。
-   メモリ使用量の削減: 26.34% 減少 (95.3 MiB から 70.2 MiB)。
-   パフォーマンスの向上:

    -   QPS は 12.38% 増加します。
    -   平均レイテンシーは 11.01% 減少します。
    -   P95レイテンシーは13.41% 減少します。

#### 仕組み {#how-it-works}

インスタンス プラン キャッシュは、次のメカニズムを通じてパフォーマンスを向上させます。

-   `SELECT`ステートメントの実行プランをメモリにキャッシュします。
-   同じ TiDB インスタンス上のすべての接続 (最大 200) にわたってキャッシュされたプランを共有します。
-   1,000 個のテーブルにわたって最大 5,000 `SELECT`ステートメントのプランを効率的に保存できます。
-   キャッシュ ミスは主に`BEGIN`および`COMMIT`ステートメントでのみ発生します。

#### 現実世界のメリット {#real-world-benefits}

単純な sysbench `oltp_read_only`クエリ (プランあたり 14 KB) を使用したベンチマークではわずかな改善が見られますが、実際のアプリケーションではさらに大きなメリットが期待できます。

-   複雑なクエリは最大 20 倍高速に実行できます。
-   セッション レベルのプラン キャッシュと比較して、メモリの使用効率が向上します。

インスタンス プラン キャッシュは、次のようなシステムに特に効果的です。

-   多くの列を持つ大きなテーブル。
-   複雑な SQL クエリ。
-   同時接続数が多い。
-   多様なクエリパターン。

#### メモリ効率 {#memory-efficiency}

インスタンス プラン キャッシュは、次の理由により、セッション レベルのプラン キャッシュよりもメモリ効率が優れています。

-   プランはすべての接続で共有されます
-   各セッションごとに計画を重複させる必要はありません
-   高いヒット率を維持しながらメモリをより効率的に利用

複数の接続と複雑なクエリがあるシナリオでは、セッション レベルのプラン キャッシュでは同様のヒット率を達成するために大幅に多くのメモリが必要になるため、インスタンス プラン キャッシュの方が効率的な選択肢になります。

![Instance plan cache: Queries Using Plan Cache OPS](/media/performance/instance-plan-cache.png)

#### テストのワークロード {#test-workload}

次の`sysbench oltp_read_only prepare`コマンドはデータをロードします。

```bash
sysbench oltp_read_only prepare --mysql-host={host} --mysql-port={port} --mysql-user=root --db-driver=mysql --mysql-db=test --threads=100 --time=900 --report-interval=10 --tables=1000 --table-size=10000
```

次の`sysbench oltp_read_only run`コマンドはワークロードを実行します。

```bash
sysbench oltp_read_only run --mysql-host={host} --mysql-port={port} --mysql-user=root --db-driver=mysql --mysql-db=test --threads=200 --time=900 --report-interval=10 --tables=1000 --table-size=10000
```

詳細については[Sysbenchを使用してTiDBをテストする方法](/benchmark/benchmark-tidb-using-sysbench.md)参照してください。

### 大きなレコード値に対するYCSBワークロード {#ycsb-workloads-on-large-record-value}

#### テスト環境 {#test-environment}

テスト環境は次のとおりです。

-   3 台の TiDB サーバー (16 コア、64 GiB)
-   3 台の TiKV サーバー (16 コア、64 GiB)
-   TiDB バージョン: v8.4.0
-   ワークロード: [go-ycsb ワークロード](https://github.com/pingcap/go-ycsb/blob/master/workloads/workloada)

#### パフォーマンス比較 {#performance-comparison}

次の表は、ベースライン設定と最適化された設定間のスループット (1 秒あたりの操作数) を比較したものです。

| アイテム     | ベースライン（OPS） | 最適化（OPS） | 改善       |
| -------- | ----------- | -------- | -------- |
| データを読み込む | 2858.5      | 5074.3   | +77.59%  |
| ワークロード   | 2243.0      | 12804.3  | +470.86% |

#### パフォーマンス分析 {#performance-analysis}

v7.6.0以降、Titanはデフォルトで有効になっています。TiDB v8.4.0では、Titanのデフォルト値は`min-blob-size`ですが、 `32KiB`設定されています。ベースライン構成では、データがRocksDBに保存されるように、レコードサイズを`31KiB`に設定しています。一方、キー設定構成では、 `min-blob-size`を`1KiB`に設定することで、データがTitanに保存されます。

主要な設定で確認されたパフォーマンスの向上は、主にTitanがRocksDBの圧縮を削減する能力によるものです。以下の図に示されています。

-   ベースライン: RocksDB 圧縮の合計スループットは 1 GiB/s を超え、ピーク時には 3 GiB/s を超えます。
-   主な設定: RocksDB 圧縮のピーク スループットは 100 MiB/s 未満のままです。

この圧縮オーバーヘッドの大幅な削減は、主要な設定構成で確認される全体的なスループットの向上に貢献します。

![Titan RocksDB compaction:](/media/performance/titan-rocksdb-compactions.png)

#### テストのワークロード {#test-workload}

次の`go-ycsb load`コマンドはデータをロードします。

```bash
go-ycsb load mysql -P /ycsb/workloads/workloada -p {host} -p mysql.port={port} -p threadcount=100 -p recordcount=5000000 -p operationcount=5000000 -p workload=core -p requestdistribution=uniform -pfieldcount=31 -p fieldlength=1024
```

次の`go-ycsb run`コマンドはワークロードを実行します。

```bash
go-ycsb run mysql -P /ycsb/workloads/workloada -p {host} -p mysql.port={port} -p mysql.db=test -p threadcount=100 -p recordcount=5000000 -p operationcount=5000000 -p workload=core -prequestdistribution=uniform -p fieldcount=31 -p fieldlength=1024
```

## エッジケースと最適化 {#edge-cases-and-optimizations}

このセクションでは、基本的な最適化を超えた具体的な調整が必要な特定のシナリオ向けにTiDBを最適化する方法を説明します。特定のユースケースに合わせてTiDBをチューニングする方法を習得します。

### エッジケースを特定する {#identify-edge-cases}

エッジケースを識別するには、次の手順を実行します。

1.  クエリ パターンとワークロードの特性を分析します。
2.  システム メトリックを監視してパフォーマンスのボトルネックを特定します。
3.  特定の問題についてアプリケーション チームからフィードバックを収集します。

### 一般的なエッジケース {#common-edge-cases}

以下に、一般的なエッジ ケースをいくつか示します。

-   高頻度の小さなクエリに対する TSO 待機時間が長い
-   さまざまなワークロードに適した最大チャンクサイズを選択する
-   読み取り負荷の高いワークロード向けにコプロセッサ キャッシュを調整する
-   ワークロード特性に合わせてチャンクサイズを最適化する
-   さまざまなワークロードに合わせてトランザクション モードと DML タイプを最適化します
-   TiKVプッシュダウンで`GROUP BY`と`DISTINCT`操作を最適化する
-   インメモリエンジンを使用して MVCC バージョンの蓄積を軽減する
-   バッチ操作中の統計収集を最適化
-   さまざまなインスタンスタイプに合わせてスレッドプールの設定を最適化する

以下のセクションでは、それぞれのケースへの対処方法について説明します。シナリオごとに異なるパラメータを調整するか、特定のTiDB機能を使用する必要があります。

> **注記：**
>
> これらの最適化の効果はユースケースやデータ パターンによって異なる可能性があるため、慎重に適用し、徹底的にテストしてください。

### 高頻度の小さなクエリに対する TSO 待機時間が長い {#high-tso-wait-for-high-frequency-small-queries}

#### トラブルシューティング {#troubleshooting}

ワークロードに頻繁に発生する小規模なトランザクションや、タイムスタンプを頻繁に要求するクエリが含まれる場合、 [TSO (タイムスタンプ オラクル)](/glossary.md#timestamp-oracle-tso)パフォーマンスのボトルネックになる可能性があります。TSO 待機時間がシステムに影響を与えているかどうかを確認するには、 [**パフォーマンスの概要 &gt; SQL実行時間の概要**](/grafana-performance-overview-dashboard.md#sql-execute-time-overview)パネルを確認してください。TSO 待機時間が SQL 実行時間の大部分を占めている場合は、以下の最適化を検討してください。

-   厳密な一貫性を必要としない読み取り操作には、低精度TSO（有効[`tidb_low_resolution_tso`](/system-variables.md#tidb_low_resolution_tso) ）を使用します。詳細については、 [解決策1: 低精度TSOを使用する](#solution-1-low-precision-tso)参照してください。
-   可能な場合は、小規模な取引を大規模な取引に統合してください。詳細については、 [ソリューション2: TSOリクエストの並列モード](#solution-2-parallel-mode-for-tso-requests)参照してください。

#### 解決策1：低精度TSO {#solution-1-low-precision-tso}

低精度TSO機能（ [`tidb_low_resolution_tso`](/system-variables.md#tidb_low_resolution_tso) ）を有効にすると、TSOの待機時間を短縮できます。この機能を有効にすると、TiDBはキャッシュされたタイムスタンプを使用してデータを読み取るため、TSOの待機時間が短縮されますが、その代償として、古い読み取りが発生する可能性があります。

この最適化は、次のシナリオで特に効果的です。

-   多少の古さが許容される、読み取り中心のワークロード。
-   絶対的な一貫性よりもクエリのレイテンシーを減らすことの方が重要なシナリオ。
-   最後にコミットされた状態から数秒遅れた読み取りを許容できるアプリケーション。

利点とトレードオフ:

-   キャッシュされた TSO を使用して古い読み取りを有効にすることでクエリのレイテンシーを短縮し、新しいタイムスタンプを要求する必要性を排除します。
-   パフォーマンスとデータ整合性のバランスをとる：この機能は、古い読み取りが許容されるシナリオにのみ適しています。厳密なデータ整合性が求められる場合は使用しないことをお勧めします。

この最適化を有効にするには:

```sql
SET GLOBAL tidb_low_resolution_tso=ON;
```

#### ソリューション2: TSOリクエストの並列モード {#solution-2-parallel-mode-for-tso-requests}

システム変数[`tidb_tso_client_rpc_mode`](/system-variables.md#tidb_tso_client_rpc_mode-new-in-v840)は、TiDB が PD に TSO RPC リクエストを送信するモードを切り替えます。デフォルト値は`DEFAULT`です。以下の条件を満たす場合は、パフォーマンス向上のためにこの変数を`PARALLEL`または`PARALLEL-FAST`に切り替えることを検討してください。

-   TSO 待機時間は、SQL クエリの合計実行時間の大部分を占めます。
-   PD における TSO 割り当てはボトルネックに達していません。
-   PD ノードと TiDB ノードには十分な CPU リソースがあります。
-   TiDB と PD 間のネットワークレイテンシーは、PD が TSO を割り当てるのにかかる時間よりも大幅に長くなります (つまり、ネットワークレイテンシーが TSO RPC 期間の大部分を占めます)。
    -   TSO RPC 要求の期間を取得するには、Grafana TiDB ダッシュボードの PD クライアント セクションにある**PD TSO RPC 期間**パネルを確認します。
    -   PD TSO 割り当ての期間を取得するには、Grafana PD ダッシュボードの TiDB セクションにある**PDサーバーTSO ハンドル期間**パネルを確認します。
-   TiDB と PD 間の TSO RPC 要求の増加 ( `PARALLEL`の場合は 2 回、 `PARALLEL-FAST`の場合は 4 回) によって発生する追加のネットワーク トラフィックは許容されます。

パラレルモードを切り替えるには、次のコマンドを実行します。

```sql
-- Use the PARALLEL mode
SET GLOBAL tidb_tso_client_rpc_mode=PARALLEL;

-- Use the PARALLEL-FAST mode
SET GLOBAL tidb_tso_client_rpc_mode=PARALLEL-FAST;
```

### 読み取り負荷の高いワークロード向けにコプロセッサ キャッシュを調整する {#tune-coprocessor-cache-for-read-heavy-workloads}

[コプロセッサキャッシュ](/coprocessor-cache.md)を最適化することで、読み取り負荷の高いワークロードのクエリパフォーマンスを向上させることができます。このキャッシュはコプロセッサリクエストの結果を保存し、頻繁にアクセスされるデータの繰り返し計算を削減します。キャッシュパフォーマンスを最適化するには、次の手順を実行します。

1.  [コプロセッサーキャッシュ](/coprocessor-cache.md#view-the-grafana-monitoring-panel)で説明したメトリックを使用してキャッシュヒット率を監視します。
2.  キャッシュ サイズを増やすと、より大きなワーキング セットのヒット率が向上します。
3.  クエリ パターンに基づいて許可しきい値を調整します。

以下に、読み取り負荷の高いワークロードに推奨される設定をいくつか示します。

```toml
[tikv-client.copr-cache]
capacity-mb = 4096
admission-max-ranges = 5000
admission-max-result-mb = 10
admission-min-process-ms = 0
```

### ワークロード特性に合わせてチャンクサイズを最適化する {#optimize-chunk-size-for-workload-characteristics}

システム変数[`tidb_max_chunk_size`](/system-variables.md#tidb_max_chunk_size)は、実行プロセス中のチャンク内の最大行数を設定します。ワークロードに応じてこの値を調整することで、パフォーマンスを向上させることができます。

-   大規模な同時実行性と小規模なトランザクションを備えた OLTP ワークロードの場合:

    -   `128`から`256`行の間の値を設定します (デフォルト値は`1024`です)。
    -   これにより、メモリ使用量が削減され、制限クエリが高速化されます。
    -   使用例: ポイント クエリ、小範囲スキャン。

    ```sql
    SET GLOBAL tidb_max_chunk_size = 128;
    ```

-   複雑なクエリと大規模な結果セットを含む OLAP または分析ワークロードの場合:

    -   `1024`から`4096`行の間の値を設定します。
    -   これにより、大量のデータをスキャンする際のスループットが向上します。
    -   使用例: 集計、大規模テーブルスキャン。

    ```sql
    SET GLOBAL tidb_max_chunk_size = 4096;
    ```

### さまざまなワークロードに合わせてトランザクション モードと DML タイプを最適化します {#optimize-transaction-mode-and-dml-type-for-different-workloads}

TiDB は、さまざまなワークロード パターンのパフォーマンスを最適化するために、さまざまなトランザクション モードと DML 実行タイプを提供します。

#### トランザクションモード {#transaction-modes}

[`tidb_txn_mode`](/system-variables.md#tidb_txn_mode)システム変数を使用してトランザクション モードを設定できます。

-   [悲観的なトランザクションモード](/pessimistic-transaction.md) （デフォルト）:

    -   書き込み競合の可能性がある一般的なワークロードに適しています。
    -   より強力な一貫性保証を提供します。

    ```sql
    SET SESSION tidb_txn_mode = "pessimistic";
    ```

-   [楽観的トランザクションモード](/optimistic-transaction.md) :

    -   書き込み競合が最小限のワークロードに適しています。
    -   複数ステートメントのトランザクションのパフォーマンスが向上します。
    -   例: `BEGIN; INSERT...; INSERT...; COMMIT;` .

    ```sql
    SET SESSION tidb_txn_mode = "optimistic";
    ```

#### DMLタイプ {#dml-types}

バージョン 8.0.0 で導入された[`tidb_dml_type`](/system-variables.md#tidb_dml_type-new-in-v800)システム変数を使用して、DML ステートメントの実行モードを制御できます。

バルクDML実行モードを使用するには、 `tidb_dml_type`を`"bulk"`に設定します。このモードは、競合を発生させることなくバルクデータのロードを最適化し、大規模な書き込み操作時のメモリ使用量を削減します。このモードを使用する前に、以下の点を確認してください。

-   [`autocommit`](/system-variables.md#autocommit)が有効です。
-   [`pessimistic-auto-commit`](/tidb-configuration-file.md#pessimistic-auto-commit-new-in-v600)構成項目は`false`に設定されています。

```sql
SET SESSION tidb_dml_type = "bulk";
```

### TiKVプッシュダウンを使用して<code>GROUP BY</code>および<code>DISTINCT</code>操作を最適化する {#optimize-code-group-by-code-and-code-distinct-code-operations-with-tikv-pushdown}

TiDBは集計操作をTiKVにプッシュダウンすることで、データ転送と処理のオーバーヘッドを削減します。パフォーマンスの向上はデータの特性によって異なります。

#### 使用シナリオ {#usage-scenarios}

-   **理想的なシナリオ**（パフォーマンスの大幅な向上）:
    -   異なる値がほとんど含まれない列 (NDV が低い)。
    -   頻繁に重複する値が含まれるデータ。
    -   例: ステータス列、カテゴリ コード、日付部分。

-   **理想的でないシナリオ**（潜在的なパフォーマンス低下）:
    -   ほとんどが一意の値を含む列 (高い NDV)。
    -   一意の識別子またはタイムスタンプ。
    -   例: ユーザー ID、トランザクション ID。

#### コンフィグレーション {#configuration}

セッション レベルまたはグローバル レベルでプッシュダウンの最適化を有効にします。

```sql
-- Enable regular aggregation pushdown
SET GLOBAL tidb_opt_agg_push_down = ON;

-- Enable distinct aggregation pushdown
SET GLOBAL tidb_opt_distinct_agg_push_down = ON;
```

### インメモリエンジンを使用して MVCC バージョンの蓄積を軽減する {#mitigate-mvcc-version-accumulation-using-in-memory-engine}

MVCCのバージョンが多すぎると、特に読み取り/書き込みが多い領域やガベージコレクションおよびコンパクションの問題により、パフォーマンスのボトルネックが発生する可能性があります。この問題を軽減するには、v8.5.0で導入されたバージョン[TiKV MVCC インメモリエンジン (IME)](/tikv-in-memory-engine.md)使用できます。これを有効にするには、TiKV設定ファイルに以下の設定を追加してください。

> **注記：**
>
> インメモリエンジンは、過剰なMVCCバージョンの影響を軽減するのに役立ちますが、メモリ使用量が増加する可能性があります。この機能を有効にした後は、システムを監視してください。

```toml
[in-memory-engine]
enable = true
```

### バッチ操作中の統計収集を最適化 {#optimize-statistics-collection-during-batch-operations}

統計収集を管理することで、クエリの最適化を維持しながらバッチ操作中のパフォーマンスを最適化できます。このセクションでは、このプロセスを効果的に管理する方法について説明します。

#### auto analyzeを無効にする場合 {#when-to-disable-auto-analyze}

次のシナリオでは、 [`tidb_enable_auto_analyze`](/system-variables.md#tidb_enable_auto_analyze-new-in-v610)システム変数を`OFF`に設定することでauto analyzeを無効にすることができます。

-   大規模なデータのインポート中。
-   一括更新操作中。
-   時間に敏感なバッチ処理用。
-   統計収集のタイミングを完全に制御する必要がある場合。

#### ベストプラクティス {#best-practices}

-   バッチ操作の前:

    ```sql
    -- Disable auto analyze
    SET GLOBAL tidb_enable_auto_analyze = OFF;
    ```

-   バッチ操作後:

    ```sql
    -- Manually collect statistics
    ANALYZE TABLE your_table;

    -- Re-enable auto analyze
    SET GLOBAL tidb_enable_auto_analyze = ON;
    ```

### さまざまなインスタンスタイプに合わせてスレッドプールの設定を最適化する {#optimize-thread-pool-settings-for-different-instance-types}

TiKV のパフォーマンスを向上させるには、インスタンスの CPU リソースに基づいてスレッドプールを設定します。以下のガイドラインは、これらの設定を最適化するのに役立ちます。

-   8 ～ 16 個のコアを持つインスタンスの場合、通常はデフォルト設定で十分です。

-   32コア以上のインスタンスの場合、リソース利用率を向上させるためにプールサイズを大きくしてください。設定は次のように調整してください。

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
