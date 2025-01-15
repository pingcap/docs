---
title: Configure TiDB for Optimal Performance
summary: 主要な設定を構成し、エッジケースに対処することで、TiDB のパフォーマンスを最適化する方法を学習します。
---

## 最適なパフォーマンスを得るための TiDB の設定 {#configure-tidb-for-optimal-performance}

このガイドでは、TiDB のパフォーマンスを最適化する方法について説明します。

-   一般的なワークロードのベスト プラクティス。
-   困難なパフォーマンス シナリオを処理するための戦略。

> **注記：**
>
> このガイドの最適化手法は、TiDB で最適なパフォーマンスを実現するのに役立ちます。ただし、パフォーマンスのチューニングには複数の要素のバランスを取る必要があることが多く、単一のソリューションですべてのパフォーマンス ニーズに対応できるわけではありません。このガイドの一部の手法では、実験的機能を使用しており、その旨が示されています。これらの最適化によりパフォーマンスが大幅に向上する可能性がありますが、本番環境には適さない可能性があり、実装前に慎重に評価する必要があります。

## 概要 {#overview}

TiDB を最高のパフォーマンスに最適化するには、さまざまな設定を慎重に調整する必要があります。多くの場合、最適なパフォーマンスを実現するには、デフォルト値を超えて構成を調整する必要があります。

デフォルト設定では、パフォーマンスよりも安定性が優先されます。パフォーマンスを最大化するには、より積極的な構成や、場合によっては実験的機能を使用する必要がある場合があります。これらの推奨事項は、本番の展開経験とパフォーマンス最適化の調査に基づいています。

このガイドでは、デフォルト以外の設定について、その利点や潜在的なトレードオフなどを含めて説明します。この情報を使用して、ワークロード要件に合わせて TiDB 設定を最適化してください。

## 一般的なワークロードのキー設定 {#key-settings-for-common-workloads}

TiDB のパフォーマンスを最適化するために、次の設定が一般的に使用されます。

-   [SQL 準備実行プラン キャッシュ](/sql-prepared-plan-cache.md)や[準備されていないプラン キャッシュ](/sql-non-prepared-plan-cache.md)などの実行プラン キャッシュを強化します。
-   [オプティマイザー修正コントロール](/optimizer-fix-controls.md)使用して TiDB オプティマイザーの動作を最適化します。
-   [タイタン](/storage-engine/titan-overview.md)storageエンジンをより積極的に使用します。

これらの設定により、多くのワークロードのパフォーマンスが大幅に向上します。ただし、他の最適化と同様に、本番に展開する前に、ご使用の環境で徹底的にテストしてください。

### システム変数 {#system-variables}

推奨設定を適用するには、次の SQL コマンドを実行します。

```sql
SET GLOBAL tidb_session_plan_cache_size=200; 
SET GLOBAL tidb_enable_non_prepared_plan_cache=on;
SET GLOBAL tidb_ignore_prepared_cache_close_stmt=on;
SET GLOBAL tidb_stats_load_sync_wait=2000;
SET GLOBAL tidb_enable_inl_join_inner_multi_pattern=on;
SET GLOBAL tidb_opt_derive_topn=on;
SET GLOBAL tidb_runtime_filter_mode=LOCAL;
SET GLOBAL tidb_opt_enable_mpp_shared_cte_execution=on;
SET GLOBAL tidb_rc_read_check_ts=on;
SET GLOBAL tidb_guarantee_linearizability=off;
SET GLOBAL pd_enable_follower_handle_region=on;
SET GLOBAL tidb_opt_fix_control = '44262:ON,44389:ON,44823:10000,44830:ON,44855:ON,52869:ON';
```

次の表は、特定のシステム変数の構成の影響を示しています。

| システム変数                                                                                                                  | 説明                                                                                                         | 注記                                                                            |
| ----------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| [`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-new-in-v710)                         | キャッシュできるプランの最大数をデフォルトの`100`から`200`に増やします。これにより、プリペアドステートメントパターンが多数あるワークロードのパフォーマンスが向上します。                  | この値を増やすと、セッション プラン キャッシュのメモリ使用量が増加する可能性があります。                                 |
| [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache)                       | [準備されていないプラン キャッシュ](/sql-non-prepared-plan-cache.md)機能を有効にすると、準備されたステートメントを使用しないアプリケーションのコンパイル コストが削減されます。 | 該当なし                                                                          |
| [`tidb_ignore_prepared_cache_close_stmt`](/system-variables.md#tidb_ignore_prepared_cache_close_stmt-new-in-v600)       | 準備されたステートメントを使用するが、実行ごとにプランを閉じるアプリケーションのプランをキャッシュします。                                                      | 該当なし                                                                          |
| [`tidb_stats_load_sync_wait`](/system-variables.md#tidb_stats_load_sync_wait-new-in-v540)                               | 統計を同期的にロードするためのタイムアウトを、デフォルトの 100 ミリ秒から 2 秒に増やします。これにより、クエリのコンパイル前に TiDB が必要な統計をロードするようになります。              | この値を大きくすると、クエリのコンパイル前の同期待機時間が長くなります。                                          |
| [`tidb_enable_inl_join_inner_multi_pattern`](/system-variables.md#tidb_enable_inl_join_inner_multi_pattern-new-in-v700) | 内部テーブルに`Selection`または`Projection`演算子がある場合に、インデックス結合のサポートを有効にします。                                           | 該当なし                                                                          |
| [`tidb_opt_derive_topn`](/system-variables.md#tidb_opt_derive_topn-new-in-v700)                                         | [ウィンドウ関数から TopN または Limit を導出する](/derive-topn-from-window.md)の最適化ルールを有効にします。                               | これは`ROW_NUMBER()`ウィンドウ関数に制限されます。                                              |
| [`tidb_runtime_filter_mode`](/system-variables.md#tidb_runtime_filter_mode-new-in-v720)                                 | ハッシュ結合の効率を向上させるには、ローカル モードで[ランタイムフィルター](/runtime-filter.md#runtime-filter-mode)有効にします。                     | この変数は v7.2.0 で導入され、安全のためデフォルトでは無効になっています。                                     |
| [`tidb_opt_enable_mpp_shared_cte_execution`](/system-variables.md#tidb_opt_enable_mpp_shared_cte_execution-new-in-v720) | TiFlashへの非再帰的な[共通テーブル式 (CTE)](/sql-statements/sql-statement-with.md)プッシュダウンを有効にします。                        | これは実験的機能です。                                                                   |
| [`tidb_rc_read_check_ts`](/system-variables.md#tidb_rc_read_check_ts-new-in-v600)                                       | 読み取りコミット分離レベルの場合、この変数を有効にすると、グローバル タイムスタンプの取得にかかるレイテンシーとコストが回避され、トランザクション レベルの読み取りレイテンシーが最適化されます。          | この機能は、繰り返し読み取り分離レベルと互換性がありません。                                                |
| [`tidb_guarantee_linearizability`](/system-variables.md#tidb_guarantee_linearizability-new-in-v50)                      | PDサーバーからのコミット タイムスタンプの取得をスキップすることでパフォーマンスが向上します。                                                           | これにより、パフォーマンスを優先して線形化可能性が犠牲になります。因果一貫性のみが保証されます。厳密な線形化可能性を必要とするシナリオには適していません。 |
| [`pd_enable_follower_handle_region`](/system-variables.md#pd_enable_follower_handle_region-new-in-v760)                 | PDFollower機能を有効にして、PD フォロワーがリージョン要求を処理できるようにします。これにより、すべての PD サーバーに負荷が均等に分散され、PD リーダーの CPU 負荷が軽減されます。      | これは実験的機能です。非本番環境でテストしてください。                                                   |
| [`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-new-in-v653-and-v710)                                | 高度なクエリ最適化戦略を有効にして、追加の最適化ルールとヒューリスティックを通じてパフォーマンスを向上させます。                                                   | パフォーマンスの向上はワークロードによって異なるため、ご使用の環境で徹底的にテストしてください。                              |

追加の最適化を可能にするオプティマイザー制御構成について次に説明します。

-   [`44262:ON`](/optimizer-fix-controls.md#44262-new-in-v653-and-v720) : [グローバル統計](/statistics.md#collect-statistics-of-partitioned-tables-in-dynamic-pruning-mode)つが不足している場合は、 [動的プルーニングモード](/partitioned-table.md#dynamic-pruning-mode)使用してパーティションテーブルにアクセスします。
-   [`44389:ON`](/optimizer-fix-controls.md#44389-new-in-v653-and-v720) : `c = 10 and (a = 'xx' or (a = 'kk' and b = 1))`などのフィルターの場合は、 `IndexRangeScan`のより包括的なスキャン範囲を構築します。
-   [`44823:10000`](/optimizer-fix-controls.md#44823-new-in-v730) :メモリを節約するために、プラン キャッシュはこの変数で指定された数を超えるパラメータを持つクエリをキャッシュしません。プラン キャッシュ パラメータの制限を`200`から`10000`に増やして、長いインリストを持つクエリでプラン キャッシュを使用できるようにします。
-   [`44830:ON`](/optimizer-fix-controls.md#44830-new-in-v657-and-v730) : プラン キャッシュは、物理的な最適化中に生成された`PointGet`の演算子を使用して実行プランをキャッシュできます。
-   [`44855:ON`](/optimizer-fix-controls.md#44855-new-in-v654-and-v730) : `IndexJoin`演算子の`Probe`側に`Selection`演算子が含まれている場合、オプティマイザーは`IndexJoin`選択します。
-   [`52869:ON`](/optimizer-fix-controls.md#52869-new-in-v810) : オプティマイザがクエリ プランに対して単一インデックス スキャン メソッド (フル テーブル スキャン以外) を選択できる場合、オプティマイザはインデックス マージを自動的に選択します。

### TiKV 構成 {#tikv-configurations}

TiKV 構成ファイルに次の構成項目を追加します。

```toml
[server]
concurrent-send-snap-limit = 64
concurrent-recv-snap-limit = 64
snap-io-max-bytes-per-sec = "400MiB"

[rocksdb.titan]
enabled = true
[rocksdb.defaultcf.titan]
min-blob-size = "1KB"
blob-file-compression = "zstd"

[storage.flow-control]
l0-files-threshold = 60
```

| コンフィグレーション項目                                                                                                                                                                                                                                                                         | 説明                                                                                                             | 注記                                                                                                                                        |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| [`concurrent-send-snap-limit`](/tikv-configuration-file.md#concurrent-send-snap-limit) [`concurrent-recv-snap-limit`](/tikv-configuration-file.md#concurrent-recv-snap-limit) [`snap-io-max-bytes-per-sec`](/tikv-configuration-file.md#snap-io-max-bytes-per-sec)                   | TiKV スケーリング操作中に同時スナップショット転送と I/O 帯域幅の制限を設定します。制限を高くすると、データ移行が高速化され、スケーリング時間が短縮されます。                            | これらの制限を調整すると、スケーリング速度とオンライン トランザクションのパフォーマンスのトレードオフに影響します。                                                                                |
| [`rocksdb.titan`](/tikv-configuration-file.md#rocksdbtitan) [`rocksdb.defaultcf.titan`](/tikv-configuration-file.md#rocksdbdefaultcftitan) [`min-blob-size`](/tikv-configuration-file.md#min-blob-size) [`blob-file-compression`](/tikv-configuration-file.md#blob-file-compression) | Titanstorageエンジンを有効にして、書き込み増幅を減らし、ディスク I/O ボトルネックを軽減します。RocksDB の圧縮が書き込みワークロードに対応できず、保留中の圧縮バイトが蓄積される場合に特に便利です。 | 書き込み増幅が主なボトルネックになっている場合は、これを有効にします。トレードオフには次のものが含まれます。1. 主キー範囲スキャンに対する潜在的なパフォーマンスへの影響。2. スペース増幅の増加 (最悪の場合、最大 2 倍)。3. BLOB キャッシュの追加メモリ使用量。 |
| [`storage.flow-control.l0-files-threshold`](/tikv-configuration-file.md#l0-files-threshold)                                                                                                                                                                                          | kvDB L0 ファイルの数に基づいて、書き込みフロー制御がトリガーされるタイミングを制御します。しきい値を増やすと、書き込みワークロードが高いときに書き込みが停止する回数が減少します。                  | しきい値を高くすると、多くの L0 ファイルが存在する場合に、より積極的な圧縮が行われる可能性があります。                                                                                     |

### TiFlash構成 {#tiflash-configurations}

TiFlash構成ファイルに次の構成項目を追加します。

```toml
[raftstore-proxy.server]
snap-io-max-bytes-per-sec = "300MiB"
```

| コンフィグレーション項目                                                                         | 説明                                                                             | 注記                                                                                |
| ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ | --------------------------------------------------------------------------------- |
| [`snap-io-max-bytes-per-sec`](/tikv-configuration-file.md#snap-io-max-bytes-per-sec) | TiKV からTiFlashへのデータ複製の最大許容ディスク帯域幅を制御します。制限を高くすると、初期データの読み込みとキャッチアップ複製が高速化されます。 | 帯域幅の消費量が多いと、オンライン トランザクションのパフォーマンスに影響する可能性があります。レプリケーション速度とシステムの安定性のバランスをとってください。 |

## ベンチマーク {#benchmark}

このセクションでは、デフォルト設定 (ベースライン) と、前述の[一般的な負荷のキー設定](#key-settings-for-common-workloads)に基づいて最適化された設定のパフォーマンスを比較します。

### 大きなレコード値に対するYCSBのワークロード {#ycsb-workloads-on-large-record-value}

#### テスト環境 {#test-environment}

テスト環境は次のとおりです。

-   3 台の TiDB サーバー (16 コア、64 GiB)
-   3 台の TiKV サーバー (16 コア、64 GiB)
-   TiDB バージョン: v8.1.0
-   作業量: [go-ycsb ワークロード](https://github.com/pingcap/go-ycsb/blob/master/workloads/workloada)

#### パフォーマンス比較 {#performance-comparison}

次の表は、ベースライン設定と最適化設定間のスループット (1 秒あたりの操作数) を比較したものです。

| アイテム     | ベースライン（OPS） | 最適化（OPS） | 改善       |
| -------- | ----------- | -------- | -------- |
| データを読み込む | 2858.5      | 5074.3   | +77.59%  |
| 作業負荷     | 2243.0      | 12804.3  | +470.86% |

#### パフォーマンス分析 {#performance-analysis}

Titan は v7.6.0 以降ではデフォルトで有効になっており、TiDB v8.1.0 の Titan のデフォルト`min-blob-size`は`32KiB`です。ベースライン構成では、データが RocksDB に保存されるようにレコード サイズ`31KiB`を使用します。一方、キー設定構成では、 `min-blob-size`を`1KiB`に設定して、データが Titan に保存されるようにします。

主要な設定で確認されたパフォーマンスの向上は、主に Titan の RocksDB 圧縮を削減する機能によるものです。次の図に示されています。

-   ベースライン: RocksDB 圧縮の合計スループットは 1 GiB/秒を超え、ピーク時には 3 GiB/秒を超えます。
-   主要な設定: RocksDB 圧縮のピーク スループットは 100 MiB/s 未満に維持されます。

この圧縮オーバーヘッドの大幅な削減は、主要な設定構成で確認される全体的なスループットの向上に貢献します。

![Titan RocksDB compaction:](/media/performance/titan-rocksdb-compactions.png)

#### テストの作業負荷 {#test-workload}

次の`go-ycsb load`のコマンドはデータをロードします。

```bash
go-ycsb load mysql -P /ycsb/workloads/workloada -p {host} -p mysql.port={port} -p threadcount=100 -p recordcount=5000000 -p operationcount=5000000 -p workload=core -p requestdistribution=uniform -pfieldcount=31 -p fieldlength=1024
```

次の`go-ycsb run`のコマンドはワークロードを実行します。

```bash
go-ycsb run mysql -P /ycsb/workloads/workloada -p {host} -p mysql.port={port} -p mysql.db=test -p threadcount=100 -p recordcount=5000000 -p operationcount=5000000 -p workload=core -prequestdistribution=uniform -p fieldcount=31 -p fieldlength=1024
```

## エッジケースと最適化 {#edge-cases-and-optimizations}

このセクションでは、基本的な最適化を超えたターゲット調整が必要な特定のシナリオに合わせて TiDB を最適化する方法を説明します。特定のユースケースに合わせて TiDB を調整する方法を学習します。

### エッジケースを特定する {#identify-edge-cases}

エッジケースを識別するには、次の手順を実行します。

1.  クエリ パターンとワークロードの特性を分析します。
2.  システム メトリックを監視してパフォーマンスのボトルネックを特定します。
3.  特定の問題についてアプリケーション チームからフィードバックを収集します。

### よくあるエッジケース {#common-edge-cases}

以下に、一般的なエッジ ケースをいくつか示します。

-   頻度の高い小さなクエリに対する TSO 待機時間が長い
-   さまざまなワークロードに適した最大チャンクサイズを選択する
-   読み取り負荷の高いワークロード向けにコプロセッサ キャッシュを調整する
-   ワークロード特性に合わせてチャンクサイズを最適化する
-   さまざまなワークロードに合わせてトランザクション モードと DML タイプを最適化する
-   TiKVプッシュダウンで`GROUP BY`と`DISTINCT`操作を最適化する
-   バッチ操作中の統計収集を最適化する
-   異なるインスタンスタイプに合わせてスレッドプール設定を最適化する

次のセクションでは、それぞれのケースの処理方法について説明します。シナリオごとに異なるパラメータを調整するか、特定の TiDB 機能を使用する必要があります。

> **注記：**
>
> これらの最適化は、ユースケースやデータ パターンによって効果が異なる可能性があるため、慎重に適用し、徹底的にテストしてください。

### 頻度の高い小さなクエリに対する TSO 待機時間が長い {#high-tso-wait-for-high-frequency-small-queries}

#### トラブルシューティング {#troubleshooting}

ワークロードに、タイムスタンプを頻繁に要求する小規模なトランザクションやクエリが頻繁に含まれる場合、TSO (Timestamp Oracle) がパフォーマンスのボトルネックになる可能性があります。TSO 待機時間がシステムに影響を与えているかどうかを確認するには、 [**パフォーマンスの概要 &gt; SQL 実行時間の概要**](/grafana-performance-overview-dashboard.md#sql-execute-time-overview)パネルを確認します。TSO 待機時間が SQL 実行時間の大部分を占める場合は、次の最適化を検討してください。

-   厳密な一貫性を必要としない読み取り操作には、低精度 TSO (有効[`tidb_low_resolution_tso`](/system-variables.md#tidb_low_resolution_tso) ) を使用します。詳細については、 [解決策1: 低精度TSOを使用する](#solution-1-low-precision-tso)参照してください。
-   [`tidb_enable_batch_dml`](/system-variables.md#tidb_enable_batch_dml)有効にすると、バッチ操作の TSO 要求が削減されます。

#### 解決策1: 低精度TSO {#solution-1-low-precision-tso}

低精度TSO機能（ [`tidb_low_resolution_tso`](/system-variables.md#tidb_low_resolution_tso) ）を有効にすると、TSO待機時間を短縮できます。この機能を有効にすると、TiDBはキャッシュされたタイムスタンプを使用してデータを読み取るため、潜在的に古い読み取りを犠牲にしてTSO待機時間を短縮できます。

この最適化は、次のシナリオで特に効果的です。

-   多少の古さが許容される、読み取り中心のワークロード。
-   絶対的な一貫性よりもクエリのレイテンシーを減らすことの方が重要なシナリオ。
-   最新のコミット状態から数秒遅れた読み取りを許容できるアプリケーション。

利点とトレードオフ:

-   キャッシュされた TSO を使用して古い読み取りを有効にすることでクエリのレイテンシーを短縮し、新しいタイムスタンプを要求する必要性を排除します。
-   パフォーマンスとデータの一貫性のバランスをとる: この機能は、古い読み取りが許容されるシナリオにのみ適しています。厳密なデータの一貫性が必要な場合には、この機能を使用することはお勧めしません。

この最適化を有効にするには:

```sql
SET GLOBAL tidb_low_resolution_tso=ON;
```

### 読み取り負荷の高いワークロード向けにコプロセッサ キャッシュを調整する {#tune-coprocessor-cache-for-read-heavy-workloads}

[コプロセッサキャッシュ](/coprocessor-cache.md)最適化することで、読み取り負荷の高いワークロードのクエリ パフォーマンスを向上させることができます。このキャッシュにはコプロセッサ要求の結果が格納され、頻繁にアクセスされるデータの繰り返し計算が削減されます。キャッシュ パフォーマンスを最適化するには、次の手順を実行します。

1.  [コプロセッサーキャッシュ](/coprocessor-cache.md#view-the-grafana-monitoring-panel)で説明したメトリックを使用してキャッシュヒット率を監視します。
2.  キャッシュ サイズを増やすと、より大きなワーキング セットのヒット率が向上します。
3.  クエリ パターンに基づいて許可しきい値を調整します。

読み取り負荷の高いワークロードに推奨される設定を以下に示します。

```toml
[tikv-client.copr-cache]
capacity-mb = 4096
admission-max-ranges = 5000
admission-max-result-mb = 10
admission-min-process-ms = 0
```

### ワークロード特性に合わせてチャンクサイズを最適化する {#optimize-chunk-size-for-workload-characteristics}

[`tidb_max_chunk_size`](/system-variables.md#tidb_max_chunk_size)システム変数は、実行プロセス中のチャンク内の最大行数を設定します。ワークロードに基づいてこの値を調整すると、パフォーマンスが向上します。

-   大規模な同時実行性と小規模なトランザクションを伴う OLTP ワークロードの場合:

    -   `128`行から`256`行の間の値を設定します (デフォルト値は`1024`です)。
    -   これにより、メモリ使用量が削減され、制限クエリが高速化されます。
    -   使用例: ポイント クエリ、小範囲スキャン。

    ```sql
    SET GLOBAL tidb_max_chunk_size = 128;
    ```

-   複雑なクエリと大規模な結果セットを含む OLAP または分析ワークロードの場合:

    -   `1024`から`4096`行の間で値を設定します。
    -   これにより、大量のデータをスキャンする際のスループットが向上します。
    -   使用例: 集計、大規模テーブルスキャン。

    ```sql
    SET GLOBAL tidb_max_chunk_size = 4096;
    ```

### さまざまなワークロードに合わせてトランザクション モードと DML タイプを最適化する {#optimize-transaction-mode-and-dml-type-for-different-workloads}

TiDB は、さまざまなワークロード パターンのパフォーマンスを最適化するために、さまざまなトランザクション モードと DML 実行タイプを提供します。

#### トランザクションモード {#transaction-modes}

[`tidb_txn_mode`](/system-variables.md#tidb_txn_mode)システム変数を使用してトランザクション モードを設定できます。

-   [悲観的なトランザクションモード](/pessimistic-transaction.md) (デフォルト):

    -   書き込み競合が発生する可能性のある一般的なワークロードに適しています。
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

バルク DML 実行モードを使用するには、 `tidb_dml_type`を`"bulk"`に設定します。このモードでは、競合なしでバルク データのロードが最適化され、大規模な書き込み操作中のメモリ使用量が削減されます。このモードを使用する前に、次の点を確認してください。

-   自動コミットが有効になっています。
-   [`pessimistic-auto-commit`](/tidb-configuration-file.md#pessimistic-auto-commit-new-in-v600)構成項目は`false`に設定されています。

```sql
SET SESSION tidb_dml_type = "bulk";
```

### TiKV プッシュダウンを使用して<code>GROUP BY</code>および<code>DISTINCT</code>操作を最適化する {#optimize-code-group-by-code-and-code-distinct-code-operations-with-tikv-pushdown}

TiDB は集計操作を TiKV にプッシュダウンして、データ転送と処理のオーバーヘッドを削減します。パフォーマンスの向上は、データの特性によって異なります。

#### 使用シナリオ {#usage-scenarios}

-   **理想的なシナリオ**（高いパフォーマンス向上）:
    -   異なる値がほとんど含まれない列 (NDV が低い)。
    -   頻繁に重複する値を含むデータ。
    -   例: ステータス列、カテゴリ コード、日付部分。

-   **理想的でないシナリオ**（潜在的なパフォーマンス低下）:
    -   ほとんどが一意の値を含む列 (高い NDV)。
    -   一意の識別子またはタイムスタンプ。
    -   例: ユーザー ID、トランザクション ID。

#### コンフィグレーション {#configuration}

セッションレベルまたはグローバルレベルでプッシュダウンの最適化を有効にします。

```sql
-- Enable regular aggregation pushdown
SET GLOBAL tidb_opt_agg_push_down = ON;

-- Enable distinct aggregation pushdown
SET GLOBAL tidb_opt_distinct_agg_push_down = ON;
```

### バッチ操作中の統計収集を最適化する {#optimize-statistics-collection-during-batch-operations}

統計収集を管理することで、クエリの最適化を維持しながらバッチ操作中のパフォーマンスを最適化できます。このセクションでは、このプロセスを効果的に管理する方法について説明します。

#### auto analyzeを無効にする場合 {#when-to-disable-auto-analyze}

次のシナリオでは、システム変数[`tidb_enable_auto_analyze`](/system-variables.md#tidb_enable_auto_analyze-new-in-v610)を`OFF`に設定することでauto analyzeを無効にすることができます。

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

### さまざまなインスタンスタイプに合わせてスレッドプール設定を最適化する {#optimize-thread-pool-settings-for-different-instance-types}

TiKV のパフォーマンスを向上させるには、インスタンスの CPU リソースに基づいてスレッド プールを構成します。次のガイドラインは、これらの設定を最適化するのに役立ちます。

-   8 ～ 16 個のコアを持つインスタンスの場合、通常はデフォルト設定で十分です。

-   32 個以上のコアを持つインスタンスの場合は、リソースの使用率を向上させるためにプール サイズを増やします。次のように設定を調整します。

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
