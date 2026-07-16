---
title: TiDB 8.5.7 リリースノート
summary: TiDB 8.5.7 の機能、互換性の変更、改善、およびバグ修正について説明します。
---

# TiDB 8.5.7 リリースノート

リリース日: 2026年7月9日

TiDB version: 8.5.7

クイックアクセス: [Quick start](https://docs.pingcap.com/tidb/v8.5/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v8.5/production-deployment-using-tiup)

## 機能 {#features}

### パフォーマンス {#performance}

* 読み取り負荷分散を改善するために、CPU を考慮したホットリージョンのスケジューリングをサポート [#5718](https://github.com/tikv/pd/issues/5718) [#19373](https://github.com/tikv/tikv/issues/19373) @[lhy1024](https://github.com/lhy1024)

    以前のバージョンでは、hot Region scheduler は主にクエリレートとバイトスループットに基づいて読み取りホットスポットを分散していました。一部のワークロードでは、QPS とバイトスループットが均衡しているように見えても、TiKV の CPU 使用率は依然として不均一なままです。たとえば、クエリごとの CPU コストが大きく異なる場合や、TiKV ノードごとに性能特性が異なる場合が該当します。

    v8.5.7 以降、TiKV は store heartbeat 内で hot Regions の読み取り CPU 使用率を報告し、PD は読み取り hot Region のスケジューリングにおいて CPU 使用率をスケジューリングの次元として利用できるようになりました。この仕組みにより、PD は CPU ベースの読み取りホットスポットを識別し、TiKV ストア間でより正確に分散できます。

    さらに、PD には CPU 関連のホットスポット統計と scheduler 制御が追加されました。これには、[hot store statistics](https://docs.pingcap.com/tidb/v8.5/pd-control#hot-read--write--store--history-start_time-end_time-key-value) の `cpu-read-rate` フィールドと、[`min-hot-cpu-rate` および `cpu-rate-rank-step-ratio`](https://docs.pingcap.com/tidb/v8.5/pd-control#scheduler-config-balance-hot-region-scheduler) の scheduler 設定が含まれます。

    詳細は、[documentation](https://docs.pingcap.com/tidb/v8.5/troubleshoot-hot-spot-issues#cpu-aware-hot-region-scheduling-for-read-hotspots) を参照してください。

### 信頼性 {#reliability}

* 単一ユーザーが 1 つの TiDB インスタンス上で確立できる接続数の制限をサポート [#59203](https://github.com/pingcap/tidb/issues/59203) @[joccau](https://github.com/joccau)

    v8.5.7 以降、`max_user_connections` システム変数を使用して、単一ユーザーが単一の TiDB サーバーインスタンスに対して確立できる最大接続数を制限できます。これにより、1 人のユーザーによる過剰な [token](https://docs.pingcap.com/tidb/v8.5/tidb-configuration-file#token-limit) 消費によって、他のユーザーからのリクエストへの応答が遅延する状況を防ぐのに役立ちます。

    さらに、`CREATE USER` および `ALTER USER` 文で `WITH MAX_USER_CONNECTIONS N` を使用して、対応するユーザーが確立できる最大接続数を制限できます。

    詳細は、[documentation](https://docs.pingcap.com/tidb/v8.5/system-variables#max_user_connections-new-in-v857) を参照してください。

### SQL {#sql}

* インデックスのストレージ使用量と DML メンテナンスのオーバーヘッドを削減するために、部分インデックスをサポート [#62664](https://github.com/pingcap/tidb/issues/62664) [#62761](https://github.com/pingcap/tidb/issues/62761) [#62758](https://github.com/pingcap/tidb/issues/62758) [#63447](https://github.com/pingcap/tidb/issues/63447) [#64344](https://github.com/pingcap/tidb/issues/64344) @[YangKeao](https://github.com/YangKeao) @[winoros](https://github.com/winoros) @[wjhuang2016](https://github.com/wjhuang2016)

    v8.5.7 以降、TiDB は部分インデックスをサポートします。これは、インデックスの `WHERE` 句で定義された述語を満たす行だけをインデックス化するものです。部分インデックスは、`CREATE INDEX ... WHERE ...`、`ALTER TABLE ... ADD INDEX ... WHERE ...`、または `CREATE TABLE` 内のインデックス定義を使用して作成できます。

    部分インデックスは、特定の条件に基づく行のサブセットを頻繁にクエリする場合や、特定の条件下でのみ適用される一意制約が必要な場合に有用です。述語に一致しない行はインデックスに書き込まれないため、部分インデックスはインデックスのストレージ使用量を削減し、`INSERT`、`UPDATE`、`DELETE` 操作時のインデックス保守オーバーヘッドを低減できます。

    部分インデックスを効果的に使用するには、一般的なクエリのフィルターに一致する述語を定義してください。TiDB は、クエリ述語が部分インデックスの述語に一致するか、それを含意する場合にのみ部分インデックスを選択します。現在、部分インデックスの述語では、基本的な比較演算子（`=`, `!=`, `<`, `<=`, `>`, `>=`）、`IS NULL`、`IS NOT NULL`、および定数値を使用した `IN` 述語をサポートしています。

    詳細は、[documentation](https://docs.pingcap.com/tidb/v8.5/sql-statement-create-index#partial-indexes) を参照してください。

### 可観測性 {#observability}

* TiDB Dashboard の Top SQL ページで、TiKV のネットワークトラフィックおよび論理 I/O メトリクスの収集と表示をサポート [#62916](https://github.com/pingcap/tidb/issues/62916) @[yibin87](https://github.com/yibin87)

    以前のバージョンでは、TiDB Dashboard は CPU 関連メトリクスのみに基づいて Top SQL クエリを識別していたため、複雑なシナリオではネットワークやストレージアクセスに関連するパフォーマンスボトルネックを特定することが困難でした。

    v8.5.7 以降、Top SQL の設定で **TiKV Network IO collection (multi-dimensional)** を有効にすると、TiKV ノードの `Network Bytes` や `Logical IO Bytes` などのメトリクスを確認できます。また、`By Query`、`By Table`、`By DB`、`By Region` など複数の次元でこれらのメトリクスを分析できるため、リソースのホットスポットをより包括的に特定できます。

    詳細は、[documentation](https://docs.pingcap.com/tidb/v8.5/top-sql) を参照してください。

### データ移行 {#data-migration}

* DM が、静的な 1 対 1 のスキーマ/テーブルルーティングにおける外部キー因果関係をサポート [#12350](https://github.com/pingcap/tiflow/issues/12350) @[OliverS929](https://github.com/OliverS929)

    v8.5.7 以降、DM は `foreign_key_checks=1` かつ `syncer.worker-count > 1` の場合に、静的な 1 対 1 のスキーマ/テーブルルーティングにおける外部キー因果関係をサポートします。

    レプリケーションタスクを開始する前に、ターゲットスキーマと外部キー定義をダウンストリームデータベースに作成しておく必要があります。この機能は、多対一または shard-merge ルーティング、レプリケーション中の動的な外部キー DDL、`syncer.compact` や `syncer.multiple-rows` のように DML 文の境界を変更するオプション、またはレプリケーション中に主キーや一意キーの値を変更する safe-mode の `UPDATE` 文をサポートしません。外部キー因果関係が有効な場合、DM は `worker-count`、`case-sensitive`、route ルール、block-allow-list ルール、binlog filter ルール、または `foreign_key_checks` を変更するホット設定更新をサポートしません。これらの設定を変更するには、タスクを停止し、設定を更新してから、タスクを再起動してください。

    詳細は、[documentation](https://docs.pingcap.com/tidb/v8.5/dm-compatibility-catalog#foreign-key-cascade-operations) を参照してください。

* TiCDC がテーブルルーティングをサポート [#4655](https://github.com/pingcap/ticdc/issues/4655) [#4941](https://github.com/pingcap/ticdc/issues/4941) [#4702](https://github.com/pingcap/ticdc/issues/4702) @[3AceShowHand](https://github.com/3AceShowHand)

    v8.5.7 以降、[new TiCDC architecture](https://docs.pingcap.com/tidb/v8.5/ticdc-architecture) はテーブルルーティングをサポートします。changefeed の `sink.dispatchers` 設定で `target-schema` と `target-table` を使用して、アップストリームテーブルを指定したダウンストリームデータベース名またはテーブル名にマッピングできます。

    この機能は、ダウンストリームのデータベース名やテーブル名の命名規則がアップストリームと異なる場合や、複数のソースデータベースを同じターゲットデータベースにレプリケートしつつ、ターゲットテーブル名の一意性を保つ必要がある場合に有用です。テーブルルーティングにより、ダウンストリームシステムに対して安定した期待どおりのターゲットデータベース名およびテーブル名を提供できます。

    この機能は new TiCDC architecture にのみ適用されます。詳細は、[documentation](https://docs.pingcap.com/tidb/v8.5/ticdc-table-routing) を参照してください。

## 互換性の変更 {#compatibility-changes}

v8.5.6 で新規にデプロイされた TiDB クラスター（つまり、以前のバージョンからアップグレードされたものではない v8.5.6 クラスター）の場合、v8.5.7 にスムーズにアップグレードできます。v8.5.7 の変更の大部分は通常のアップグレードに対して安全ですが、このリリースにはいくつかの動作変更、MySQL 互換性の変更、システム変数の更新、設定パラメーターの更新、および非推奨機能も含まれています。アップグレード前に、このセクションを必ず注意深く確認してください。

### 動作変更 {#behavior-changes}

* TiKV は、無効であることが確認された `max_ts` 更新を、従来のようにログに記録するだけでなく、デフォルトで拒否するようになりました。この変更により、TiKV の panic を引き起こすことなく無効なタイムスタンプ更新を防止し、安全性が向上します。従来のログ記録のみの動作を維持するには、[`storage.max-ts.action-on-invalid-update`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#action-on-invalid-update-new-in-v857) を `log` に設定してください [#19755](https://github.com/tikv/tikv/issues/19755) @[ekexium](https://github.com/ekexium)
* v8.5.7 以降、TiDB はデフォルトで [optimizer fix control `52869`](https://docs.pingcap.com/tidb/v8.5/optimizer-fix-controls#52869-new-in-v810) を有効にします。この変更により、代替インデックスが存在する場合に optimizer が `IndexMerge` を自動的に考慮できるようになり、一部のケースでクエリプランが変わる可能性があります。[#26764](https://github.com/pingcap/tidb/issues/26764) @[time-and-fate](https://github.com/time-and-fate)

### MySQL 互換性 {#mysql-compatibility}

* MySQL 8.0 との互換性向上のため、派生テーブルに対する `LATERAL` 構文の解析をサポート。これには、カンマ結合、`CROSS JOIN LATERAL`、`INNER JOIN LATERAL` が含まれます

    現在、TiDB は [the `LATERAL` derived table syntax](https://docs.pingcap.com/tidb/v8.5/lateral-derived-tables) の解析のみをサポートしており、この構文を使用するクエリの実行はサポートしていません。このようなクエリを実行しようとすると、TiDB はエラーを返します。この機能の完全な実行サポートの進捗は issue [#40328](https://github.com/pingcap/tidb/issues/40328) で確認できます。

* MySQL 互換性向上のため、`CREATE USER` および `ALTER USER` で `WITH MAX_USER_CONNECTIONS N` をサポート。TiDB はさらに `mysql.user` に `max_user_connections` カラムを追加し、`max_user_connections` システム変数を使用して、ユーザーが TiDB サーバーインスタンスに対して確立できる最大接続数を制御できるようにしました。

### システム変数 {#system-variables}

| Variable name | Change type | Description |
|--------|------------------------------|------|
| [`tidb_enable_telemetry`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_enable_telemetry-new-in-v402) | Deprecated | v8.5.7 以降、TiDB はこのシステム変数と telemetry 機能を非推奨とします。この変数は互換性のためにのみ保持されており、今後の使用は推奨されません。|
| [`tidb_auto_analyze_concurrency`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_auto_analyze_concurrency-new-in-v840) | Modified | 統計情報収集タスクを高速化し、自動 analyze の効率を向上させるため、デフォルト値を `1` から `3` に変更します。クラスターが以前のバージョンからアップグレードされた場合、この変数の値はアップグレード後も変更されません。|
| [`tidb_auto_build_stats_concurrency`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_auto_build_stats_concurrency-new-in-v650) | Modified | auto `ANALYZE` のデフォルト性能を向上させるため、デフォルト値を `1` から `2` に変更します。クラスターが以前のバージョンからアップグレードされた場合、この変数の値はアップグレード後も変更されません。|
| [`tidb_sysproc_scan_concurrency`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_sysproc_scan_concurrency-new-in-v650) | Modified | TiDB が内部 SQL 文を実行する際のスキャン操作を高速化するため、デフォルト値を `1` から `4` に変更します。クラスターが以前のバージョンからアップグレードされた場合、この変数の値はアップグレード後も変更されません。|
| [`max_user_connections`](https://docs.pingcap.com/tidb/v8.5/system-variables#max_user_connections-new-in-v857) | Newly added | ユーザーが TiDB サーバーインスタンスに対して確立できる最大接続数を制御します。デフォルト値は `0` で、制限なしを意味します。この変数の値が `max_connections` を超える場合、TiDB は `max_connections` を実効上限として使用します。|
| [`performance_schema_session_connect_attrs_size`](https://docs.pingcap.com/tidb/v8.5/system-variables#performance_schema_session_connect_attrs_size-new-in-v857) | Newly added | 各セッションの接続属性の合計最大サイズを制御します。デフォルト値は `4096` バイトです。サイズがこの上限を超えると、TiDB は超過分の属性を切り詰め、切り詰められたバイト数を示すために `_truncated` を追加します。|
| [`tidb_enable_batch_query_region`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_enable_batch_query_region-new-in-v857) | Newly added | TiDB が `QueryRegion` gRPC stream を介して Region 情報のポイントクエリを PD に対してバッチ送信するかどうかを制御します。デフォルト値は `OFF` です。有効にすると、一部のシナリオで PD に送信されるリクエスト数を減らし、PD leader の CPU オーバーヘッドを低減できます。|
| [`tidb_enable_cache_prepare_stmt`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_enable_cache_prepare_stmt-new-in-v857) | Newly added | `Prepare` 文の結果をキャッシュするかどうかを制御します。デフォルト値は `OFF` です。現在、この変数は実験的であり、本番環境での使用は推奨されません。|
| [`tidb_enable_strict_not_null_check`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_enable_strict_not_null_check-new-in-v857) | Newly added | `INSERT` 文が `NOT NULL` カラムに `NULL` 値を明示的に書き込む際に、TiDB が厳密な検証を行うかどうかを制御します。デフォルト値は `ON` です。アプリケーションが、暗黙のデフォルト値を書き込む以前の寛容な動作に依存している場合は、アップグレード互換性リスクを低減するために、この変数を一時的に `OFF` に設定できます。|
| [`tidb_opt_enable_alternative_logical_plans`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_opt_enable_alternative_logical_plans-new-in-v857) | Newly added | 相関サブクエリの decorrelation シナリオにおいて、optimizer が decorrelate しない論理候補プランも追加で構築するかどうかを制御します。デフォルト値は `OFF` です。|
| [`tidb_opt_partial_ordered_index_for_topn`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_opt_partial_ordered_index_for_topn-new-in-v857) | Newly added | クエリに `ORDER BY ... LIMIT` が含まれる場合に、optimizer がインデックスの部分的な順序性を利用して TopN 計算を最適化できるかどうかを制御します。デフォルト値は `DISABLE` で、この最適化が無効であることを意味します。|

### 設定パラメーター {#configuration-parameters}

| Configuration file or component | Configuration parameter | Change type | Description |
| -------- | -------- | -------- | -------- |
| TiDB | [`enable-telemetry`](https://docs.pingcap.com/tidb/v8.5/tidb-configuration-file#enable-telemetry-new-in-v402) | Deprecated | v8.5.7 以降、TiDB はこの設定項目と telemetry 機能を非推奨とします。この項目は互換性のためにのみ保持されており、今後の使用は推奨されません。|
| TiKV | [`backup.gcp-v2-enable`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#backupgcp-v2-enable-new-in-v857) | Newly added | TiKV が GCS のフルバックアップおよびリストアに `gcp_v2` 外部ストレージバックエンドを使用するかどうかを制御します。デフォルト値は `true` です。有効時は TiKV は `gcp_v2` を使用し、無効時は従来の GCS 実装を使用します。|
| TiKV | [`log-backup.gcp-v2-enable`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#log-backupgcp-v2-enable-new-in-v857) | Newly added | TiKV が GCS のログバックアップに `gcp_v2` 外部ストレージバックエンドを使用するかどうかを制御します。デフォルト値は `true` です。有効時は TiKV は `gcp_v2` を使用し、無効時は従来の GCS 実装を使用します。|
| TiKV | [`resource-control.admission-max-delayed-count`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#admission-max-delayed-count-new-in-v857) | Newly added | TiKV が admission control の遅延キュー内に保持できる同時リクエスト数（読み取りと書き込みの合計）の最大値を指定します。デフォルト値は `10000` です。無制限の同時遅延を許可するには、この値を `0` に設定します。|
| TiKV | [`resource-control.baseline-burst-pct`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#baseline-burst-pct-new-in-v857) | Newly added | TiKV がリソースグループをベースライン超過と見なす前に許容する、そのリソースグループの過去の RU ベースラインに対する余裕率の割合を指定します。デフォルト値は `20.0` です。|
| TiKV | [`resource-control.bg-compaction-pressure-threshold`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#bg-compaction-pressure-threshold-new-in-v857) | Newly added | バックグラウンド書き込み I/O スロットリングを開始するしきい値を、`storage.flow-control.soft-pending-compaction-bytes-limit` に対する割合として指定します。デフォルト値は `70.0` です。|
| TiKV | [`resource-control.bg-cpu-throttle-threshold`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#bg-cpu-throttle-threshold-new-in-v857) | Newly added | バックグラウンドタスクのスロットリングを開始する CPU 使用率のしきい値（パーセンテージ）を指定します。デフォルト値は `60.0` です。|
| TiKV | [`resource-control.bg-write-io-ceiling`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#bg-write-io-ceiling-new-in-v857) | Newly added | compaction pressure が `bg-compaction-pressure-threshold` 未満の場合に、バックグラウンドタスクに許可される最大書き込み I/O レートを指定します。デフォルト値は `"100GB"` です。|
| TiKV | [`resource-control.bg-write-io-floor`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#bg-write-io-floor-new-in-v857) | Newly added | compaction pressure が最大の場合でもバックグラウンドタスクに保証される最小書き込み I/O レートを指定します。デフォルト値は `"10MB"` です。|
| TiKV | [`resource-control.enable-fair-scheduling`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#enable-fair-scheduling-new-in-v857) | Newly added | 読み取りリクエストに対して、RU ベースの 2 段階フェアスケジューリングを有効にするかどうかを制御します。デフォルト値は `false` です。|
| TiKV | [`resource-control.enable-read-admission-control`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#enable-read-admission-control-new-in-v857) | Newly added | 読み取りリクエストに対する admission control を有効にするかどうかを制御します。デフォルト値は `false` です。|
| TiKV | [`resource-control.enable-write-admission-control`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#enable-write-admission-control-new-in-v857) | Newly added | 書き込みリクエストに対する admission control を有効にするかどうかを制御します。デフォルト値は `false` です。|
| TiKV | [`resource-control.fg-cpu-throttle-threshold`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#fg-cpu-throttle-threshold-new-in-v857) | Newly added | フォアグラウンドトラフィック保護が完全に有効化される CPU 使用率のしきい値（パーセンテージ）を指定します。デフォルト値は `70.0` です。このしきい値は `bg-cpu-throttle-threshold` より大きくなければなりません。|
| TiKV | [`resource-control.historical-usage-window-mins`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#historical-usage-window-mins-new-in-v857) | Newly added | TiKV がリソースグループごとの過去の RU ベースラインを計算するために使用する、分単位のスライディング時間ウィンドウのサイズを指定します。デフォルト値は `15` で、変更を有効にするには TiKV の再起動が必要です。|
| TiKV | [`resource-metering.enable-network-io-collection`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#resource-meteringenable-network-io-collection-new-in-v857) | Newly added | Top SQL 向けに、CPU データに加えて TiKV がネットワークトラフィックおよび論理 I/O 情報を収集するかどうかを制御します。デフォルト値は `false` です。|
| TiKV | [`storage.max-ts.action-on-invalid-update`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#action-on-invalid-update-new-in-v857) | Newly added | TiKV が無効な `max-ts` 更新リクエストをどのように処理するかを決定します。デフォルト値は `"error"` で、TiKV が無効な `max-ts` 更新リクエストを検出したときにエラーを返し、そのリクエストの処理を停止することを意味します。|
| TiKV | [`storage.max-ts.cache-sync-interval`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#cache-sync-interval-new-in-v857) | Newly added | TiKV がローカルの PD TSO キャッシュを更新する間隔を制御します。デフォルト値は `"15s"` です。|
| TiKV | [`storage.max-ts.max-drift`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#max-drift-new-in-v857) | Newly added | 読み取りまたは書き込みリクエストのタイムスタンプが、TiKV にキャッシュされた PD TSO を超過できる最大時間を指定します。デフォルト値は `"60s"` です。|
| TiCDC | [`sink.dispatchers`](https://docs.pingcap.com/tidb/v8.5/ticdc-changefeed-config#dispatchers) | Updated | changefeed のダウンストリームが MQ sink の場合、`dispatchers` を使用して event dispatcher を設定できます。v8.5.7 以降、[new TiCDC architecture](https://docs.pingcap.com/tidb/v8.5/ticdc-architecture) を使用している場合は、`dispatchers` を使用して [table routing](https://docs.pingcap.com/tidb/v8.5/ticdc-table-routing) も設定できます。|

### コンパイラバージョン {#compiler-versions}

* TiDB の Go コンパイラバージョンを go1.25.8 から go1.25.10 にアップグレードし、TiDB のパフォーマンスを向上させました。TiDB 開発者の場合は、スムーズにコンパイルできるよう Go コンパイラバージョンをアップグレードしてください。 
* TiKV の Rust コンパイラバージョンを nightly-2023-12-28 から nightly-2025-02-28 にアップグレードし、TiKV のパフォーマンスを向上させました。TiKV 開発者の場合は、スムーズにコンパイルできるよう Rust コンパイラバージョンをアップグレードしてください。

## 非推奨機能 {#deprecated-features}

* v8.5.7 以降、TiDB および TiDB Dashboard の [telemetry](https://docs.pingcap.com/tidb/v8.5/telemetry) 機能は非推奨です。

## 削除された機能 {#removed-features}

* TiDB v8.5.7 以降、TiDB Lightning は Web インターフェースをサポートしなくなりました。[#67697](https://github.com/pingcap/tidb/issues/67697) @[D3Hunter](https://github.com/D3Hunter)

    TiDB Lightning でデータをインポートするには、TiDB Lightning のコマンドラインツールを使用してください。インポートタスクには [`tidb-lightning`](https://docs.pingcap.com/tidb/v8.5/tidb-lightning-command-line-full#tidb-lightning)、チェックポイントおよびトラブルシューティング操作には [`tidb-lightning-ctl`](https://docs.pingcap.com/tidb/v8.5/tidb-lightning-command-line-full#tidb-lightning-ctl) を使用します。

    新しいデータインポートのワークロードでは、[`IMPORT INTO`](https://docs.pingcap.com/tidb/v8.5/sql-statement-import-into) 文も使用できます。

    この変更がワークフローに影響する場合は、[#67697](https://github.com/pingcap/tidb/issues/67697) にコメントしてください。
## 改善点 {#improvements}

+ TiDB

    - `OR` 条件および `IN` 条件を含む `ORDER BY ... LIMIT` クエリのパフォーマンスを改善しました。オプティマイザーが `IndexMerge` をより効果的に選択できるようになり、`IndexMerge` 内の `IN` 条件パスに対するマージソートもサポートしました。これにより、`Limit` を部分パスへプッシュダウンでき、不要な行読み取りと I/O オーバーヘッドを削減できます。[#65712](https://github.com/pingcap/tidb/issues/65712) @[time-and-fate](https://github.com/time-and-fate)
    - スロークエリログにクライアント接続属性を記録し、`INFORMATION_SCHEMA.SLOW_QUERY` および `INFORMATION_SCHEMA.CLUSTER_SLOW_QUERY` から問い合わせ可能にすることで、スロークエリの可観測性を向上しました。`performance_schema_session_connect_attrs_size` で属性の切り詰めを制御し、切り詰められたバイト数は `_truncated` に記録されます。[#66616](https://github.com/pingcap/tidb/issues/66616) @[jiong-nba](https://github.com/jiong-nba)
    - 単一行の `INSERT` 文に対して TiDB が厳格な `NOT NULL` チェックを適用するかどうかを制御するシステム変数 `tidb_enable_strict_not_null_check` を追加しました。これにより、従来の非厳格な動作に依存するワークロードにおけるアップグレードリスクを低減できます。[#68108](https://github.com/pingcap/tidb/issues/68108) @[xhebox](https://github.com/xhebox)
    - runaway query watch 処理のパフォーマンスと安定性を改善しました。これには、TiDB インスタンス間でのより信頼性の高い watch 同期と、より効率的なバックグラウンドでのフラッシュおよび同期が含まれます。[#65746](https://github.com/pingcap/tidb/issues/65746) @[JmPotato](https://github.com/JmPotato)
    - TiDB が PD に対してバッチ化された Region クエリを使用するかどうかを制御するグローバルシステム変数 `tidb_enable_batch_query_region` を追加しました。これにより Region 情報取得の効率が向上します。この変数はデフォルトで無効です。[#58439](https://github.com/pingcap/tidb/issues/58439) [#8690](https://github.com/tikv/pd/issues/8690) @[JmPotato](https://github.com/JmPotato)
    - 多数のインデックスを持つテーブルに対するクエリのオプティマイザーパフォーマンスを改善しました。コスト見積もりの前に無関係なインデックスを枝刈りすることで、クエリ計画時間を短縮し、不要な全範囲の範囲外見積もりを回避します。[#63856](https://github.com/pingcap/tidb/issues/63856) @[terry1purcell](https://github.com/terry1purcell) @[qw4990](https://github.com/qw4990)
    - Blackbox exporter ダッシュボードの **Ping Latency** パネルを強化し、`max_over_time` アラートルールを使用した `Max Ping Latency` メトリクスを追加しました。この変更により、ダッシュボードの可視化が TiDB のアラートロジックと一致し、レイテンシーのピークスパイクの特定やアラート発火の確認が容易になります。[#1071](https://github.com/pingcap/monitoring/issues/1071) @[yibin87](https://github.com/yibin87)
    - 一致するプレフィックスインデックス上の `ORDER BY ... LIMIT/OFFSET` クエリに対して、部分順序付きインデックス最適化をサポートしました。`tidb_opt_partial_ordered_index_for_topn` を `COST` に設定すると、TiDB はインデックスの部分順序を利用して全表スキャンを減らし、`TOPN` クエリのパフォーマンスを向上できます。[#63280](https://github.com/pingcap/tidb/issues/63280) [#65813](https://github.com/pingcap/tidb/issues/65813) [#66338](https://github.com/pingcap/tidb/issues/66338) @[elsa0520](https://github.com/elsa0520) @[xzhangxian1008](https://github.com/xzhangxian1008) @[winoros](https://github.com/winoros)
    - Stream Aggregate を使用する高カーディナリティの `GROUP BY` クエリについて、メモリ追跡における CPU オーバーヘッドを削減し、パフォーマンスを最適化しました。[#68475](https://github.com/pingcap/tidb/issues/68475) @[guo-shaoge](https://github.com/guo-shaoge)
    - ローカルインデックスを持つ高分割テーブル上の `IndexLookUp` クエリにおけるコプロセッサーリクエストのバーストを緩和し、クエリの安定性を向上させ、性能スパイクを低減しました。[#67545](https://github.com/pingcap/tidb/issues/67545) @[gengliqi](https://github.com/gengliqi)
    - 実行時の不要な式バッファ割り当てを削減することで、`INSERT ... ON DUPLICATE KEY UPDATE` 文の CPU およびメモリ使用量を最適化しました。[#65003](https://github.com/pingcap/tidb/issues/65003) @[windtalker](https://github.com/windtalker)
    - 範囲構築時の CPU およびメモリオーバーヘッドを削減することで、大きな `IN` リストを含む文のクエリ計画パフォーマンスを最適化しました。[#67756](https://github.com/pingcap/tidb/issues/67756) @[winoros](https://github.com/winoros)
    - `tidb_auto_build_stats_concurrency` と `tidb_sysproc_scan_concurrency` のデフォルト値を手動 `ANALYZE` と揃えることで、自動 `ANALYZE` のデフォルトパフォーマンスと一貫性を改善しました。[#67195](https://github.com/pingcap/tidb/issues/67195) @[0xTars](https://github.com/0xTars)
    - サブクエリの decorrelation に対する代替論理プラン最適化を有効にするシステム変数 `tidb_opt_enable_alternative_logical_plans` を追加しました。[#66676](https://github.com/pingcap/tidb/issues/66676) @[AilinKid](https://github.com/AilinKid)
    - 同一セッション内で繰り返し使用されるプリペアドステートメントをキャッシュし、リクエストごとに prepare を行うワークロードの CPU オーバーヘッドを削減するシステム変数 `tidb_enable_cache_prepare_stmt` を追加しました。[#67815](https://github.com/pingcap/tidb/issues/67815) @[guo-shaoge](https://github.com/guo-shaoge)
    - join reorder を改善し、TiDB が join グループ間の projection を処理できるようにしました。これにより不要な Cartesian join を減らし、より多くのクエリで `LEADING` ヒントが有効になります。[#50229](https://github.com/pingcap/tidb/issues/50229) @[Reminiscent](https://github.com/Reminiscent)
    - `LEADING((a, b), (c, d))` のように、より複雑な join 順序を指定するために、`LEADING` オプティマイザーヒントでネストした括弧をサポートしました。[#63253](https://github.com/pingcap/tidb/issues/63253) @[guo-shaoge](https://github.com/guo-shaoge)
    - 推定 probe 行数が全スキャンに近い場合に非効率な index join を選択しないよう join プラン選択を改善し、一部の `HASHAGG` + join シナリオでクエリパフォーマンスを向上しました。[#67610](https://github.com/pingcap/tidb/issues/67610) @[qw4990](https://github.com/qw4990)
    - ネストした `OR` 条件を含むクエリについて、より効率的な `IndexMerge` プランを有効にし、冗長なグローバルフィルターを削除して `LIMIT` をプッシュダウンできるようにすることで、クエリパフォーマンスを改善しました。[#65822](https://github.com/pingcap/tidb/issues/65822) @[time-and-fate](https://github.com/time-and-fate)
    - すべて、データベース単位、またはテーブル単位のスコープについて、保留中のオプティマイザー統計 delta を永続化する `FLUSH STATS_DELTA` 文をサポートしました。[#65668](https://github.com/pingcap/tidb/issues/65668) @[0xPoe](https://github.com/0xPoe)
    - 代替インデックスが存在する場合に `IndexMerge` を考慮するためのオプティマイザー fix control をデフォルトで有効にし、より多くの適用可能なクエリで TiDB が `IndexMerge` プランを選択できるようにして、クエリ最適化を改善しました。[#26764](https://github.com/pingcap/tidb/issues/26764) @[time-and-fate](https://github.com/time-and-fate)
    - `set_var` および `resource_group` ヒントを使用するプリペアドクエリと非プリペアドクエリのキャッシュをサポートし、ヒント付きクエリのプランキャッシュヒット率を向上しました。[#60920](https://github.com/pingcap/tidb/issues/60920) @[qw4990](https://github.com/qw4990)
    - `IndexMerge` を使用する `ORDER BY ... LIMIT` および `ORDER BY ... TOPN` クエリを最適化し、可能な場合は `Limit` または `TopN` を個々の部分パスにプッシュダウンすることで、一部のクエリプランにおける不要なスキャンとソートを削減しました。[#68773](https://github.com/pingcap/tidb/issues/68773) @[time-and-fate](https://github.com/time-and-fate)
    - 新規に bootstrap されたクラスターにおける `ANALYZE` パフォーマンスを改善するため、`mysql.stats_*` システムテーブルに clustered primary key を使用するようにしました。[#66751](https://github.com/pingcap/tidb/issues/66751) @[0xPoe](https://github.com/0xPoe)
    - `COM_PING` リクエストに対してエラーを返すことで、プロキシやロードバランサーが TiDB サーバーのシャットダウンを検知し、新しい接続の送信を停止できるようにして、graceful shutdown 処理を改善しました。[#58007](https://github.com/pingcap/tidb/issues/58007) @[dveeden](https://github.com/dveeden)
    - 多数の生成カラムを持つテーブルに対する `INSERT` 文を高速化し、ワイドテーブルワークロードのパフォーマンスを大幅に向上しました。[#67916](https://github.com/pingcap/tidb/issues/67916) @[bb7133](https://github.com/bb7133)
    - TiDB Dashboard の Slow Query ページでセッション接続属性を表示できるようにしました。オプションのリストカラムと専用の詳細タブを含み、このフィールドを提供しない以前の TiDB バージョンとの互換性も維持します。[#1899](https://github.com/pingcap/tidb-dashboard/issues/1899) @[yibin87](https://github.com/yibin87)
    - 非 TiDB リクエストに対して厳密な max-ts チェックを適用することで、トランザクションタイムスタンプ検証を改善し、外部コンポーネントが将来のタイムスタンプを誤って使用するリスクを低減しました。[#68799](https://github.com/pingcap/tidb/issues/68799) @[ekexium](https://github.com/ekexium)
    - 自動コミットの楽観的トランザクションを最適化し、初回実行時のロック解決をスキップすることで、高競合シナリオでのレイテンシーを削減しました。[#58675](https://github.com/pingcap/tidb/issues/58675) @[ekexium](https://github.com/ekexium)

+ TiKV

    - 動的 resource group 分離を追加し、履歴上の RU ベースラインを超えたグループからのリクエストの優先度を下げることで、継続的なワークロードをトラフィックスパイクから保護します。さらに、高 CPU 負荷時にはベースライン超過リクエストを遅延または拒否することも可能です。新しい `resource-control` 設定オプションはデフォルトで無効です。[#19607](https://github.com/tikv/tikv/issues/19607) @[mittalrishabh](https://github.com/mittalrishabh)
    - すべての TiKV バックグラウンド resource group に対してグローバル rate limiter を使用し、関連するバックグラウンド resource-control メトリクスを `resource_group` ラベルなしで集約するようにしました。これに伴い、影響を受けるダッシュボードとアラートの更新が必要です。[#19497](https://github.com/tikv/tikv/issues/19497) @[mittalrishabh](https://github.com/mittalrishabh)
    - キューが満杯のときに高優先度リクエストが低優先度の待機タスクを追い出せるようにし、TiKV 統一読み取りプールのスケジューリング公平性を改善しました。これにより、テナント間およびバックグラウンドトラフィック間でより公平なリソース割り当てを実現します。[#19386](https://github.com/tikv/tikv/issues/19386) @[mittalrishabh](https://github.com/mittalrishabh)
    - apply log 処理中に、PITR でリストアされた `Put` および `Delete` の write CF レコードへ物理 import トランザクションソースを付与するようにし、TiCDC が PITR で import されたデータを無視できるようにしました。[#19669](https://github.com/tikv/tikv/issues/19669) @[YuJuncen](https://github.com/YuJuncen)
    - ディスク I/O ハングを検出した TiKV ノードが自動的に fail-fast で終了するようにし、応答しないストアからのリカバリを高速化しました。[#19626](https://github.com/tikv/tikv/issues/19626) @[hbisheng](https://github.com/hbisheng)
    - TiKV 8.5 向けに脆弱なサードパーティ依存関係をアップグレードし、必要な互換性修正を upstream と整合させることで、TiKV の安定性とセキュリティを向上しました。[#19713](https://github.com/tikv/tikv/issues/19713) @[LykxSassinator](https://github.com/LykxSassinator)
    - truncate key 式を使用するクエリで、より正確な結果を返すために、TiKV で rank ベースの limit 処理をサポートしました。[#19388](https://github.com/tikv/tikv/issues/19388) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - デフォルトの split しきい値を緩和し、split key 選択および CPU フォールバック判断の可観測性を追加することで、TiKV の負荷ベース Region 分割を改善しました。これにより、運用者はホット Region をより効果的に処理できます。[#18932](https://github.com/tikv/tikv/issues/18932) @[lhy1024](https://github.com/lhy1024)

+ PD

    - PD のメンテナンス用エンドポイントと `pd-ctl` コマンドを追加し、TiKV のメンテナンスタスクを直列化できるようにしました。これにより、一度に 1 つのメンテナンスタスクのみを有効にして Raft クォーラム喪失を防ぎます。[#9477](https://github.com/tikv/pd/issues/9477) @[SerjKol80](https://github.com/SerjKol80) @[HaoW30](https://github.com/HaoW30)
    - Region 分割後の予期しないスケジューリングを避けるため、PD で split scatter をデフォルトで無効にしました。引き続き `schedule.split-scatter-schedule-limit` を正の値に設定することで有効化できます。[#10592](https://github.com/tikv/pd/issues/10592) @[lhy1024](https://github.com/lhy1024)
    - unsafe recovery の empty-region プラン生成を最適化し、多数の Region とギャップを持つ大規模クラスターでパフォーマンスを向上し、タイムアウトリスクを低減しました。[#10638](https://github.com/tikv/pd/issues/10638) @[Connor1996](https://github.com/Connor1996)
    - PD のトランザクション継続時間メトリクスを改善し、本番環境のレイテンシー分布をより適切に反映できるようにして、ダッシュボードとアラートでの可観測性を向上しました。[#10705](https://github.com/tikv/pd/issues/10705) @[bufferflies](https://github.com/bufferflies)

+ TiFlash

    - TiKV ノードのスケールイン後に繰り返し出力される無効な接続ログを減らすため、TiFlash の不要な gRPC 接続を削除しました。[#9806](https://github.com/pingcap/tiflash/issues/9806) @[gengliqi](https://github.com/gengliqi)

+ Tools

    + Backup & Restore (BR)

        - BR で Workload Identity Federation を使用して Google Cloud Storage のバックアップバケットへアクセスできるようにしました。[#19442](https://github.com/tikv/tikv/issues/19442) @[Leavrth](https://github.com/Leavrth)
        - 必要なデータベーススキーマ情報のみを読み込むことで、BR のバックアップおよびリストアがオンライン DDL に与える影響を緩和し、スキーマ再読み込みのオーバーヘッドと DDL ブロック時間を削減しました。[#64833](https://github.com/pingcap/tidb/issues/64833) @[YuJuncen](https://github.com/YuJuncen)
        - PITR でリストアされた write CF エントリを物理 import トランザクションとしてマークすることで、TiCDC が PITR で import されたデータを無視できるようにし、PITR と TiCDC の互換性を向上しました。[#68660](https://github.com/pingcap/tidb/issues/68660) @[YuJuncen](https://github.com/YuJuncen)
        - BR が同時に PD へ送信する Region スキャンリクエスト数を制限する `--region-scan-concurrency` パラメーターを追加し、多数の Region スキャンが発行される場合のリストア安定性を向上しました。[#66821](https://github.com/pingcap/tidb/issues/66821) @[Leavrth](https://github.com/Leavrth)

    + TiCDC

        - TiCDC event store の書き込みパスと iterator パスを最適化し、メモリ割り当てを削減してイベント処理パフォーマンスを向上しました。[#4928](https://github.com/pingcap/ticdc/issues/4928) @[lidezhu](https://github.com/lidezhu)
        - DDL 取得における TiCDC の `tidb_ddl_history` への依存を削除し、`tidb_ddl_job` に依存することで高速なテーブル作成をサポートしました。[#2272](https://github.com/pingcap/ticdc/issues/2272) @[wlwilliamx](https://github.com/wlwilliamx)
        - TiCDC のホットパスを最適化し、高スループットシナリオでの CPU オーバーヘッドを削減してレプリケーション性能を向上しました。[#5107](https://github.com/pingcap/ticdc/issues/5107) @[lidezhu](https://github.com/lidezhu)
        - redo checkpoint および resolved timestamp のメトリクスを追加し、TiCDC redo log 進行状況の可観測性を向上しました。[#5264](https://github.com/pingcap/ticdc/issues/5264) @[wk989898](https://github.com/wk989898)
        - 多数の TiCDC Changefeed が warning 状態に入った際の etcd への高負荷を、変更のないランタイム状態の不要な永続化を避けることで緩和しました。[#5268](https://github.com/pingcap/ticdc/issues/5268) @[wk989898](https://github.com/wk989898)
        - Changefeed Error Details Grafana パネルにエラー発生時刻を表示することで TiCDC の監視を強化し、運用者が changefeed 障害をより効率的に診断できるようにしました。[#5085](https://github.com/pingcap/ticdc/issues/5085) @[wlwilliamx](https://github.com/wlwilliamx)
        - 各 checker 実行でグループごとの merge operator を最大 8 個に制限することで、TiCDC の増分スキャンにおける CPU スパイクを緩和しました。[#5047](https://github.com/pingcap/ticdc/issues/5047) @[hongyunyan](https://github.com/hongyunyan)
        - cloud storage sink に対する TiCDC のスケジューリング応答性とコールバックの正確性を改善しました。flush 完了を待つ代わりに、DML イベントが書き込みパイプラインに入った時点で受理を通知することで、checkpoint の意味論を変えずに wake レイテンシーを削減します。[#4269](https://github.com/pingcap/ticdc/issues/4269) @[3AceShowHand](https://github.com/3AceShowHand)
        - sink 初期化が遅い場合に、changefeed 間で発生する TiCDC bootstrap のヘッドオブラインブロッキングを削減し、changefeed 作成およびリカバリのスループットを向上しました。[#5139](https://github.com/pingcap/ticdc/issues/5139) @[hongyunyan](https://github.com/hongyunyan)
        - 一時的な producer 送信失敗をデフォルトで再試行することで、TiCDC Kafka sink の安定性を向上しました。[#1920](https://github.com/pingcap/ticdc/issues/1920) @[3AceShowHand](https://github.com/3AceShowHand)
        - `max-retry` Kafka sink URI パラメーターを追加し、一時的な Kafka producer 送信失敗に対する上限付き再試行をデフォルトで有効にして、TiCDC Kafka sink の安定性を向上しました。[#12655](https://github.com/pingcap/tiflow/issues/12655) @[3AceShowHand](https://github.com/3AceShowHand)
        - TiCDC cloud storage sink にローカル spool を追加し、受理したエンコード済み DML を外部ストレージへ flush する前にローカルで一時保持することで、オブジェクトストレージが遅い場合のメモリ圧力を軽減し、安定性を向上しました。[#3745](https://github.com/pingcap/ticdc/issues/3745) @[3AceShowHand](https://github.com/3AceShowHand)
        - partial index の DDL 文のレプリケーションをサポートしました。[#3698](https://github.com/pingcap/ticdc/issues/3698) @[YangKeao](https://github.com/YangKeao)
        - TiCDC blackhole sink のメトリクスを追加し、changefeed レプリケーションおよび DDL 処理の可観測性を向上しました。[#5362](https://github.com/pingcap/ticdc/issues/5362) @[wk989898](https://github.com/wk989898)
        - resolved-ts が多いワークロード、特に小さなバッチにおいて、CPU 使用量とメモリ割り当てを削減するよう TiCDC log puller のパフォーマンスを最適化しました。[#4697](https://github.com/pingcap/ticdc/issues/4697) @[asddongmen](https://github.com/asddongmen)
        - TiCDC MySQL sink の競合検出を最適化し、レプリケーション性能を向上しました。[#4582](https://github.com/pingcap/ticdc/issues/4582) @[wk989898](https://github.com/wk989898)
        - TiCDC の resolve lock の可観測性を改善し、同じ Region に対する重複した resolve 試行を回避することで、不要なロック解決作業を削減し、新しいメトリクスとダッシュボードによってトラブルシューティングを容易にしました。[#5016](https://github.com/pingcap/ticdc/issues/5016) @[lidezhu](https://github.com/lidezhu)
        - TiCDC Grafana ダッシュボードに Changefeed Operation History パネルを追加し、create、update、pause、resume、delete など、最近のユーザー起因の changefeed 操作を調査しやすくしました。[#5087](https://github.com/pingcap/ticdc/issues/5087) @[wlwilliamx](https://github.com/wlwilliamx)
        - `WHERE` 句を含む `CREATE TABLE`、`CREATE INDEX`、`ALTER TABLE ... ADD INDEX` を含め、partial index を使用する DDL 文の解析とレプリケーションをサポートしました。[#12503](https://github.com/pingcap/tiflow/issues/12503) @[YangKeao](https://github.com/YangKeao)
        - MySQL sink のテーブルルーティングをサポートし、ルーティングされた changefeed がターゲットのスキーマ名およびテーブル名に対して DDL と DML を適用できるようにしました。[#4818](https://github.com/pingcap/ticdc/issues/4818) @[3AceShowHand](https://github.com/3AceShowHand)
        - warning または failed 状態の changefeed のエラー情報を表示する TiCDC メトリクスを追加し、ログではなく監視を通じて問題を診断しやすくしました。[#4498](https://github.com/pingcap/ticdc/issues/4498) @[wk989898](https://github.com/wk989898)

    + TiDB Lightning

        - TiDB `IMPORT INTO` で `FORMAT` が指定されていない場合に、ファイル名からファイル形式を自動検出できるようにし、CSV、SQL、Parquet ファイルのデータインポートを簡素化しました。[#59540](https://github.com/pingcap/tidb/issues/59540) @[JQWong7](https://github.com/JQWong7)

## バグ修正 {#bug-fixes}

+ TiDB

    - クエリ実行中でも切断済みクライアント接続を TiDB が速やかに閉じず、文の終了まで接続が `SHOW PROCESSLIST` に残り続ける問題を修正しました。[#57531](https://github.com/pingcap/tidb/issues/57531) @[Defined2014](https://github.com/Defined2014)
    - `RegionNotFound` エラー後も古い Region キャッシュエントリが使われ続け、再試行の繰り返し、Region 再読み込みの遅延、追加のクロス AZ トラフィックを引き起こす可能性がある問題を修正しました。[#1892](https://github.com/tikv/client-go/issues/1892) [#69197](https://github.com/pingcap/tidb/issues/69197) @[ekexium](https://github.com/ekexium)
    - 定数文字列引数を持つベクトル化 `ILIKE` の評価時に発生する可能性があるクラッシュを修正しました。[#67001](https://github.com/pingcap/tidb/issues/67001) @[zanmato1984](https://github.com/zanmato1984)
    - 負の値を符号なし数値カラムへ代入したり、整数値を `SET` カラムへ代入したりする際に、point `UPDATE` 文が通常の `UPDATE` 文と異なる代入変換セマンティクスを使用し、不整合な結果、範囲外エラー、または MySQL 互換性の問題を引き起こす可能性がある問題を修正しました。[#63455](https://github.com/pingcap/tidb/issues/63455) [#67534](https://github.com/pingcap/tidb/issues/67534) @[fzzf678](https://github.com/fzzf678)
    - まれなケースで、クエリの並行実行中に TiDB が `SIGSEGV` でクラッシュする可能性がある問題を修正しました。[#66391](https://github.com/pingcap/tidb/issues/66391) @[bb7133](https://github.com/bb7133)
    - 大文字小文字の異なるユーザー変数を使用するクエリで、最適でない実行プランが生成され、インデックス範囲スキャンを使用できない場合がある問題を修正しました。[#66339](https://github.com/pingcap/tidb/issues/66339) @[qw4990](https://github.com/qw4990)
    - 複数セッションが同時にグローバルバインディングにヒットした際に、TiDB がメモリ不足になり、グローバルバインディングキャッシュが破損する可能性がある問題を修正しました。[#68015](https://github.com/pingcap/tidb/issues/68015) @[qw4990](https://github.com/qw4990)
    - `NULL` 値に敏感な条件を伴う outer join を使用するクエリで、TiDB が誤った結果を返す可能性がある問題を修正しました。この問題は、オプティマイザーが outer join を inner join に簡略化できるかどうかを誤って判断することが原因で発生します。影響を受けるシナリオには、`OR`、`IS NULL`、`COALESCE()`、`NULLIF()`、`CAST()`、`IN (NULL, ...)` などの述語や式を含む `WHERE` 句、および派生テーブルや `UNION ALL` を含む outer join クエリが含まれます。この問題により、誤った結果、欠落行、空結果、または `NULL` 値を含む予期しない行が発生する可能性があります。[#58793](https://github.com/pingcap/tidb/issues/58793) [#59162](https://github.com/pingcap/tidb/issues/59162) [#60080](https://github.com/pingcap/tidb/issues/60080) [#60081](https://github.com/pingcap/tidb/issues/60081) [#60370](https://github.com/pingcap/tidb/issues/60370) [#61327](https://github.com/pingcap/tidb/issues/61327) [#66824](https://github.com/pingcap/tidb/issues/66824) [#66825](https://github.com/pingcap/tidb/issues/66825) [#67330](https://github.com/pingcap/tidb/issues/67330) [#67373](https://github.com/pingcap/tidb/issues/67373) @[winoros](https://github.com/winoros)
    - null-reject チェックがパラメーター値に依存しない場合に、outer join 上のプリペアドステートメントがプリペアドプランキャッシュをスキップする可能性がある問題を修正しました。[#67048](https://github.com/pingcap/tidb/issues/67048) @[winoros](https://github.com/winoros)
    - 全範囲インデックススキャンのクエリ計画時に、非同期インデックスヒストグラム読み込みに関する不要な警告を TiDB が記録する可能性がある問題を修正しました。[#64791](https://github.com/pingcap/tidb/issues/64791) @[terry1purcell](https://github.com/terry1purcell)
    - 同期統計読み込みがタイムアウトして pseudo または部分統計へフォールバックした際に生成されたプランが、必要な統計が読み込まれた後もキャッシュされ再利用される可能性がある問題を修正しました。[#66585](https://github.com/pingcap/tidb/issues/66585) @[winoros](https://github.com/winoros)
    - outer join に対して TiDB が誤った join 順序を生成し、誤ったクエリ結果を返す可能性がある問題を修正しました。[#63887](https://github.com/pingcap/tidb/issues/63887) @[guo-shaoge](https://github.com/guo-shaoge)
    - outer join を含む一部のクエリで、TiDB が最適でない join 順序を選択し、効率の低い実行プランにつながる可能性がある問題を修正しました。[#67774](https://github.com/pingcap/tidb/issues/67774) @[AilinKid](https://github.com/AilinKid)
    - `mysql.global_variables` に対応する行が存在しない場合、アップグレード中に `tidb_ignore_inlist_plan_digest` が予期せずリセットされる可能性がある問題を修正しました。[#68136](https://github.com/pingcap/tidb/issues/68136) @[qw4990](https://github.com/qw4990)
    - `ORDER BY` と `LIMIT` を含むクエリの最適化時に、`IndexFullScan` コストの過小評価により TiDB が非効率な `MergeJoin` プランを選択し、クエリパフォーマンスが低下する可能性がある問題を修正しました。[#67595](https://github.com/pingcap/tidb/issues/67595) @[qw4990](https://github.com/qw4990)
    - 重複した式を持つ式インデックスを使用するクエリで、TiDB が誤った隠し生成カラムを解決するため、`Unexpected missing column` エラーが返される可能性がある問題を修正しました。[#67552](https://github.com/pingcap/tidb/issues/67552) @[AilinKid](https://github.com/AilinKid)
    - `KILL QUERY` またはキャンセル後に `ANALYZE` が速やかに停止せず、analyze ジョブがハングする可能性がある問題を修正しました。[#65818](https://github.com/pingcap/tidb/issues/65818) @[hawkingrei](https://github.com/hawkingrei)
    - v7.6 より前のバージョンからクラスターをアップグレードした後、`tidb_analyze_distsql_scan_concurrency` が既存の `tidb_distsql_scan_concurrency` 設定から初期化されないため、手動 `ANALYZE` が遅くなる可能性がある問題を修正しました。[#65423](https://github.com/pingcap/tidb/issues/65423) @[winoros](https://github.com/winoros)
    - 一部の非相関 `IN` サブクエリを TiDB が相関実行プランへ変換できず、index lookup を使用できなくなり、効率の低いクエリプランにつながる可能性がある問題を修正しました。[#66320](https://github.com/pingcap/tidb/issues/66320) @[terry1purcell](https://github.com/terry1purcell)
    - インデックス付き文字列カラムに対して `CAST(... AS BINARY)` を使用するクエリで、インデックス範囲スキャンではなくインデックス全スキャンが使用される可能性がある問題を修正しました。[#67899](https://github.com/pingcap/tidb/issues/67899) @[terry1purcell](https://github.com/terry1purcell)
    - `JSON` などスキップされるカラム型に依存する、インデックス付き stored generated column に対して `ANALYZE TABLE` を実行した際に発生する可能性がある panic を修正しました。[#66359](https://github.com/pingcap/tidb/issues/66359) [#66918](https://github.com/pingcap/tidb/issues/66918) @[xhebox](https://github.com/xhebox)
    - outer join を含むクエリに対して TiDB が誤った join 順序を生成し、誤ったクエリ結果につながる可能性がある問題を修正しました。[#67290](https://github.com/pingcap/tidb/issues/67290) @[guo-shaoge](https://github.com/guo-shaoge)
    - セッション `time_zone` が UTC より進んでいる場合に、`SHOW ANALYZE STATUS` が負の `Remaining_seconds` 値を表示する問題を修正しました。[#67230](https://github.com/pingcap/tidb/issues/67230) @[0xPoe](https://github.com/0xPoe)
    - パーティションテーブルに対する `ANALYZE`（auto-analyze を含む）中に、`fatal error: concurrent map read and map write` を報告して TiDB サーバーがクラッシュする可能性がある問題を修正しました。[#68457](https://github.com/pingcap/tidb/issues/68457) @[mjonss](https://github.com/mjonss)
    - partial index が外部キーの強制に誤って使用され、親行に対する delete または update 時に一致する子行を見逃して孤立行が残る可能性がある問題を修正しました。[#68587](https://github.com/pingcap/tidb/issues/68587) @[YangKeao](https://github.com/YangKeao)
    - 生成カラムを持たないテーブルに対する `INSERT` 文で性能退行が発生し、一般的なワークロードのスループットが低下する問題を修正しました。[#68129](https://github.com/pingcap/tidb/issues/68129) @[bb7133](https://github.com/bb7133)
    - `utf8mb4_0900_bin` カラムと `BLOB` カラムを結合する際に、`CONCAT_WS()` がバイナリ結果ではなく `ERROR 3854` エラーを返す問題を修正しました。[#68845](https://github.com/pingcap/tidb/issues/68845) @[tiancaiamao](https://github.com/tiancaiamao)
    - 接続監視のオーバーヘッドにより、自動コミットの `INSERT`、`UPDATE`、`DELETE` 文で性能退行が発生する問題を修正しました。[#68633](https://github.com/pingcap/tidb/issues/68633) @[King-Dylan](https://github.com/King-Dylan)
    - `new_collation_enabled` が無効な場合に、混在した大文字小文字のスキーマ名に対する `GRANT` および `REVOKE` が失敗したり、重複した権限行を作成したり、既存の権限行に一致しなかったりする問題を修正しました。修正後は、このような混在ケースの識別子は同じ権限レコードにマッピングされます。[#66867](https://github.com/pingcap/tidb/issues/66867) [#68406](https://github.com/pingcap/tidb/issues/68406) @[expxiaoli](https://github.com/expxiaoli)
    - クライアント切断後に、自動コミットの書き込み文が速やかに中断されない可能性がある問題を修正しました。[#68236](https://github.com/pingcap/tidb/issues/68236) @[King-Dylan](https://github.com/King-Dylan)
    - 非 TiDB のトランザクション関連リクエストが将来タイムスタンプ検証を誤って通過し、`ScanLock`、backup range、`CheckTxnStatus`、`Cleanup`、`CheckSecondaryLocks` で一貫しない動作を引き起こす可能性がある問題を修正しました。[#19656](https://github.com/tikv/tikv/issues/19656) @[ekexium](https://github.com/ekexium)
    - `tidb_foreign_key_check_in_shared_lock` が有効な場合に、悲観的トランザクションでの外部キー cascade update が `use Op::SharedLock to prewrite on a shared lock` で失敗する可能性がある問題を修正しました。[#68133](https://github.com/pingcap/tidb/issues/68133) @[wfxr](https://github.com/wfxr)

+ TiKV

    - Region 数が多い場合に、resolved_ts モジュールが過剰なメモリを消費する問題を修正しました。[#19535](https://github.com/tikv/tikv/issues/19535) @[glorv](https://github.com/glorv)
    - MVCC read-aware compaction が有効な場合に、長時間実行された compaction ラウンドの直後に TiKV が次の compaction ラウンドを即座に開始し、負荷ベース compaction のための統計収集が不十分になる問題を修正しました。[#19362](https://github.com/tikv/tikv/issues/19362) @[mittalrishabh](https://github.com/mittalrishabh)
    - raft-engine 使用時に、安定したワークロードでも TiKV のメモリ使用量が時間とともに増加する問題を修正しました。[#19544](https://github.com/tikv/tikv/issues/19544) @[LykxSassinator](https://github.com/LykxSassinator)
    - TiKV in-memory engine から Region を手動で退避させると、Region が `Evicting` 状態のままになり、自動的に再ロードされなくなる問題を修正しました。[#19584](https://github.com/tikv/tikv/issues/19584) @[overvenus](https://github.com/overvenus)
    - ストアが複数の gRPC raft 接続を使用している場合に、raft メッセージキューで TiKV が過剰なメモリを消費する問題を修正しました。[#19542](https://github.com/tikv/tikv/issues/19542) @[glorv](https://github.com/glorv)
    - TiKV で中断された CPU profiling リクエストにより profiling が active 状態のままになり、その後の profiling リクエストが `Already in CPU Profiling` で失敗する問題を修正しました。[#19703](https://github.com/tikv/tikv/issues/19703) @[hujiatao0](https://github.com/hujiatao0)
    - エントリ永続化後も TiKV が Raft ログ内に過剰なメモリを保持し、レプリカで異常に高いメモリ使用量を引き起こす可能性がある問題を修正しました。[#19593](https://github.com/tikv/tikv/issues/19593) @[LykxSassinator](https://github.com/LykxSassinator)
    - PD から削除済み tombstone store のアドレス解決時に、TiKV が無限再試行ループに入り、`invalid store ID ..., not found` エラーを繰り返し記録する可能性がある問題を修正しました。[#17875](https://github.com/tikv/tikv/issues/17875) @[LykxSassinator](https://github.com/LykxSassinator)
    - 長時間のアップロード中にアクセストークンの有効期限が近い場合、TiKV の GCS バックアップが失敗する可能性がある問題を修正しました。[#19659](https://github.com/tikv/tikv/issues/19659) @[RidRisR](https://github.com/RidRisR)
    - 通常トラフィック時に TiKV の `apply_msg_len` メトリクスにデータポイントがなく、apply メッセージ長分布の監視に影響する問題を修正しました。[#18800](https://github.com/tikv/tikv/issues/18800) @[squalfof](https://github.com/squalfof)
    - split 直後に PD が Region をマージした際、TiKV が Region heartbeat で誤った pending peer 情報を報告することにより発生する可能性がある panic を修正しました。[#17992](https://github.com/tikv/tikv/issues/17992) @[hbisheng](https://github.com/hbisheng)
    - TiKV In-Memory Engine のデバッグ API `/debug/ime/cached_regions` にアクセスできない問題を修正しました。[#19546](https://github.com/tikv/tikv/issues/19546) @[glorv](https://github.com/glorv)
    - TiKV の `server.grpc_memory_pool_quota` 設定を動的に変更できない問題を修正しました。[#19104](https://github.com/tikv/tikv/issues/19104) @[glorv](https://github.com/glorv)
    - オンライントラフィックが CPU リソースの大半を使用している場合に TiKV がバックグラウンドトラフィックをスロットリングせず、高負荷時にオンラインリクエストのレイテンシーが増加する可能性がある問題を修正しました。[#19401](https://github.com/tikv/tikv/issues/19401) @[mittalrishabh](https://github.com/mittalrishabh)

+ PD

    - 高並行時に token bucket が過剰なトークンを蓄積し、PD の resource control rate limiting が弱くなる可能性がある問題を修正しました。[#10744](https://github.com/tikv/pd/issues/10744) @[YuhaoZhang00](https://github.com/YuhaoZhang00)
    - token bucket 通知タイマーのリセット時に発生する resource group client controller の goroutine リークを修正しました。[#9745](https://github.com/tikv/pd/issues/9745) @[lhy1024](https://github.com/lhy1024)
    - 設定された RU fill rate が実際の RU 消費量より大幅に高い場合に、resource group への SQL リクエストで約 1 秒のレイテンシースパイクが発生する問題を修正しました。[#10251](https://github.com/tikv/pd/issues/10251) @[JmPotato](https://github.com/JmPotato)
    - 配置ルールで要求される最高分離レベルが満たされていない場合でも、PD の affinity scheduling が Region を適切にレプリケート済みと見なしてしまい、誤ったレプリカ配置判断につながる可能性がある問題を修正しました。[#10149](https://github.com/tikv/pd/issues/10149) @[HunDunDM](https://github.com/HunDunDM)
    - Region heartbeat breakdown メトリクスがホストの monotonic clock の一時的な逆行に遭遇した際に、`counter cannot decrease in value` エラーを引き起こす可能性がある PD の panic を修正しました。[#10901](https://github.com/tikv/pd/issues/10901) @[JmPotato](https://github.com/JmPotato)
    - affinity group が設定されていない場合に、PD が affinity checker operator limit メトリクスを誤って報告する問題を修正しました。[#10687](https://github.com/tikv/pd/issues/10687) @[lhy1024](https://github.com/lhy1024)
    - `PD-Allow-Follower-Handle: true` ヘッダーが明示的に設定されない限り、PD Follower がローカルで同期済みの Region キャッシュから読み取り専用 Region HTTP API を提供できない問題を修正しました。[#10681](https://github.com/tikv/pd/issues/10681) @[okJiang](https://github.com/okJiang)
    - PD leader が Region sync 応答を送信できなかったり、シャットダウン中に sync stream を閉じたりした場合に、PD follower が Region 更新を受信しなくなる可能性がある問題を修正しました。[#10684](https://github.com/tikv/pd/issues/10684) @[okJiang](https://github.com/okJiang)
    - PD leader が更新送信に失敗して stream をメモリから削除した後、PD follower が古い stream を待ち続ける可能性がある Region syncer の問題を修正しました。[#10666](https://github.com/tikv/pd/issues/10666) @[okJiang](https://github.com/okJiang)
    - flow のみの Region heartbeat 更新後も、PD が冗長な subtree update タスクをスケジュールし続け、大規模クラスターでメモリ圧力を増加させる可能性がある問題を修正しました。[#10722](https://github.com/tikv/pd/issues/10722) @[JmPotato](https://github.com/JmPotato)

+ Tools

    + Backup & Restore (BR)

        - `--check-requirements=false` を指定しても BR restore がバージョン互換性チェックに失敗し続け、明示的にバージョンチェックを無効化しているにもかかわらず restore を続行できない問題を修正しました。[#67402](https://github.com/pingcap/tidb/issues/67402) @[RidRisR](https://github.com/RidRisR)
        - ロックファイルがストレージルートにある場合に、S3 互換ストレージで BR `log truncate` が失敗する可能性がある問題を修正しました。[#65897](https://github.com/pingcap/tidb/issues/65897) @[YuJuncen](https://github.com/YuJuncen)
        - 複数バージョンにまたがる多数の `mDB:*` メタキーをバックアップが含む場合に、BR point-in-time restore がメタデータ復元中にメモリ不足になる可能性がある問題を修正しました。[#67196](https://github.com/pingcap/tidb/issues/67196) @[vldmit](https://github.com/vldmit)
        - AWS FIPS endpoint mode が有効な場合に、BR がカスタム AWS S3 endpoint へアクセスできない可能性がある問題を修正しました。[#68966](https://github.com/pingcap/tidb/issues/68966) @[v01dstar](https://github.com/v01dstar)
        - ターゲットクラスターのカラム数が異なる場合に、snapshot restore 中に BR が `mysql.user` テーブルを物理的にリストアしてしまい、論理 restore にフォールバックせず新しいテーブルスキーマを上書きする可能性がある問題を修正しました。[#68861](https://github.com/pingcap/tidb/issues/68861) @[Leavrth](https://github.com/Leavrth)
        - `br operator base64ify` が生成された storage backend で S3 Object Lock 状態を保持しない問題を修正しました。[#68551](https://github.com/pingcap/tidb/issues/68551) @[YuJuncen](https://github.com/YuJuncen)
        - TiKV が flush subscription リクエストに応答しない場合に、BR log backup の checkpoint 進行が停止する可能性がある問題を修正しました。[#68411](https://github.com/pingcap/tidb/issues/68411) @[Leavrth](https://github.com/Leavrth)
        - テーブルフィルター付きの BR point-in-time restore で、同じデータベースから複数回テーブルをリストアすると、重複したデータベースが作成されたり、ターゲットデータベースが予期せず変更されたりする可能性がある問題を修正しました。[#68908](https://github.com/pingcap/tidb/issues/68908) @[Leavrth](https://github.com/Leavrth)
        - 現在の最後の Region ID および leader store ID に関する BR log backup メトリクスが `/metrics` エンドポイントに存在しない問題を修正しました。[#62839](https://github.com/pingcap/tidb/issues/62839) @[YuJuncen](https://github.com/YuJuncen)
        - 書き込み負荷が高い状況で、multipart upload が 10000 パート制限を超えるため、S3 への BR log backup が停止する可能性がある問題を修正しました。[#19162](https://github.com/tikv/tikv/issues/19162) @[vldmit](https://github.com/vldmit)
        - 新しい BR バージョンで作成されたバックアップを古い restore ツールで復元する際に、`merge_option` 属性など認識できないバックアップメタデータを BR が黙って失う問題を修正しました。現在は requirement チェック時に互換性の問題を報告します。[#67016](https://github.com/pingcap/tidb/issues/67016) @[JoyC-dev](https://github.com/JoyC-dev)
        - truncate または migration 読み込み失敗時に、BR log backup が外部バックアップディレクトリをリークしたり、古い read lock を残したりする可能性がある問題を修正しました。[#67819](https://github.com/pingcap/tidb/issues/67819) @[RidRisR](https://github.com/RidRisR)
        - 認証情報が設定済みプレフィックスにスコープされている場合に、BR の S3 権限チェックが失敗し、backup または restore タスクが開始前に失敗する可能性がある問題を修正しました。[#68583](https://github.com/pingcap/tidb/issues/68583) @[YuJuncen](https://github.com/YuJuncen)
        - log backup を有効にした失敗済み restore の checkpoint から restore を再開する際に、BR が PiTR blocklist を書き込まない可能性がある問題を修正しました。[#68171](https://github.com/pingcap/tidb/issues/68171) @[Leavrth](https://github.com/Leavrth)
        - 32768 を超える Region を初期化する際に、BR log backup タスクの起動がハングする問題を修正しました。[#19615](https://github.com/tikv/tikv/issues/19615) @[YuJuncen](https://github.com/YuJuncen)
        - システムテーブルを論理 restore する際に `Transaction is too large` エラーで BR restore が失敗する可能性がある問題を修正し、トランザクションメモリクォータを調整する `--txn-total-size-limit` パラメーターを追加しました。[#66806](https://github.com/pingcap/tidb/issues/66806) @[Leavrth](https://github.com/Leavrth)

    + TiCDC

        - TiCDC Grafana ダッシュボードでパネルが重なって表示され、セクション順序が正しくない問題を修正しました。[#4508](https://github.com/pingcap/ticdc/issues/4508) @[lidezhu](https://github.com/lidezhu)
        - event iterator の作成または最初の読み取りに失敗した際に、TiCDC が実際のエラーを報告せず、イベントスキャン失敗の根本原因が隠れてしまう問題を修正しました。[#5005](https://github.com/pingcap/ticdc/issues/5005) @[lidezhu](https://github.com/lidezhu)
        - DDL イベントまたは checkpoint の送信失敗時に再試行が発生すると、TiCDC Kafka changefeed が Kafka クライアントインスタンスをリークし、メモリ使用量が増え続ける可能性がある問題を修正しました。[#12666](https://github.com/pingcap/tiflow/issues/12666) @[3AceShowHand](https://github.com/3AceShowHand)
        - old value が欠落した insert-like prewrite lock をスキャンする際に、TiCDC の増分スキャンが過剰な CPU を使用し、checkpoint の進行が遅くなる問題を修正しました。[#19565](https://github.com/tikv/tikv/issues/19565) @[zier-one](https://github.com/zier-one)
        - dispatcher リセット後に TiCDC が checkpoint より前のデータをスキャンし、event store で panic を引き起こす可能性がある問題を修正しました。[#4492](https://github.com/pingcap/ticdc/issues/4492) @[lidezhu](https://github.com/lidezhu)
        - コンポーネント初期化に失敗した際に、TiCDC が接続、storage handle、またはバックグラウンド goroutine をリークする可能性がある問題を修正しました。[#4516](https://github.com/pingcap/ticdc/issues/4516) @[wk989898](https://github.com/wk989898)
        - event processing pipeline のデッドロックにより、利用可能なメモリクォータが 0 の場合に TiCDC changefeed が停止する可能性がある問題を修正しました。[#4899](https://github.com/pingcap/ticdc/issues/4899) @[lidezhu](https://github.com/lidezhu)
        - 以前の close リクエストの処理中に後続の changefeed remove リクエストが到着した場合、TiCDC が downstream の remove-only cleanup をスキップする可能性がある問題を修正しました。[#4825](https://github.com/pingcap/ticdc/issues/4825) @[hongyunyan](https://github.com/hongyunyan)
        - `tidb_cdc.ddl_ts_v1` が存在せず、downstream が標準外の missing-table エラーコードを返す場合に、TiCDC の MySQL 互換 sink が停止する問題を修正しました。[#5003](https://github.com/pingcap/ticdc/issues/5003) @[hongyunyan](https://github.com/hongyunyan)
        - Kafka sink の初期化失敗時または sink クローズ時に、TiCDC が Kafka クライアント接続およびバックグラウンドリソースをリークする可能性がある問題を修正しました。[#12572](https://github.com/pingcap/tiflow/issues/12572) @[wlwilliamx](https://github.com/wlwilliamx)
        - 多数のアクティブテーブルをレプリケートする際に、TiCDC の resolved-ts lag と CPU 使用率が周期的に増加する問題を修正しました。[#4887](https://github.com/pingcap/ticdc/issues/4887) @[lidezhu](https://github.com/lidezhu)
        - ローカル EventService が dispatcher を削除し、collector がそれをローカルで再登録した後に、TiCDC レプリケーションが停止する可能性がある問題を修正しました。[#5088](https://github.com/pingcap/ticdc/issues/5088) @[lidezhu](https://github.com/lidezhu)
        - TiCDC が Pulsar sink を初期化し、producer 初期化に失敗した際に発生する可能性がある panic を修正しました。[#4937](https://github.com/pingcap/ticdc/issues/4937) @[wk989898](https://github.com/wk989898)
        - パス削除後も TiCDC が不正確なメモリアカウンティングを保持し、dynstream で誤った pause または release フィードバックを引き起こす問題を修正しました。[#4644](https://github.com/pingcap/ticdc/issues/4644) @[asddongmen](https://github.com/asddongmen)
        - graceful `SIGTERM` シャットダウン中に TiCDC がコード 1 で終了する問題を修正しました。[#4563](https://github.com/pingcap/ticdc/issues/4563) @[pingyu](https://github.com/pingyu)
        - redo 設定が正しく初期化されないため、TiCDC が redo log sink の起動に失敗する可能性がある問題を修正しました。[#4512](https://github.com/pingcap/ticdc/issues/4512) @[3AceShowHand](https://github.com/3AceShowHand)
        - `CURRENT_TIMESTAMP` など時間関連のデフォルト値を持つカラムに対して TiCDC が redo DDL イベントを適用する際に発生する可能性がある panic を修正しました。[#4699](https://github.com/pingcap/ticdc/issues/4699) @[wk989898](https://github.com/wk989898)
        - 複数の TiCDC クラスターが同じ PD/etcd を共有し、それらの cluster ID がプレフィックス関係にある場合に、再起動後に TiCDC が別クラスターの changefeed を読み込む可能性がある問題を修正しました。[#4756](https://github.com/pingcap/ticdc/issues/4756) @[wk989898](https://github.com/wk989898)
        - bootstrap および failover 中の TiCDC redo readiness における data race を修正し、failover タスクが `DATA RACE` 警告を報告する可能性がある問題を解消しました。[#4402](https://github.com/pingcap/ticdc/issues/4402) @[3AceShowHand](https://github.com/3AceShowHand)
        - ソースデータベース名が指定されていない場合に、TiCDC がクロスデータベースの `RENAME TABLE` 操作をレプリケートできない問題を修正しました。[#4424](https://github.com/pingcap/ticdc/issues/4424) @[lidezhu](https://github.com/lidezhu)
        - log puller が一時的な gRPC `EOF` エラーに遭遇した際に、TiCDC changefeed が失敗または停止する可能性がある問題を修正しました。[#4880](https://github.com/pingcap/ticdc/issues/4880) @[lidezhu](https://github.com/lidezhu)
        - 非常に多数のテーブルをレプリケートする際に、TiCDC changefeed の初期化が遅くなり、maintainer レイテンシーが高くなる問題を修正しました。[#4951](https://github.com/pingcap/ticdc/issues/4951) @[hongyunyan](https://github.com/hongyunyan)
        - 存在しない changefeed を問い合わせた際に、TiCDC CLI がエラーを返さない問題を修正しました。[#4648](https://github.com/pingcap/ticdc/issues/4648) @[wk989898](https://github.com/wk989898)
        - TiCDC の `unsafe/service_gc_safepoint` API 呼び出しが、予期せず PD クライアントを閉じてしまう問題を修正しました。[#4638](https://github.com/pingcap/ticdc/issues/4638) @[wk989898](https://github.com/wk989898)
        - bootstrap 失敗後に TiCDC が maintainer bootstrap を再試行する際に発生する可能性がある panic を修正し、changefeed がクラッシュする代わりに元のエラーを報告するようにしました。[#4509](https://github.com/pingcap/ticdc/issues/4509) @[wk989898](https://github.com/wk989898)
        - ステイルロック解決中に TiCDC が shared lock を未解決のまま残す可能性があり、nextgen デプロイメントで shared-lock 互換性に影響する問題を修正しました。[#5206](https://github.com/pingcap/ticdc/issues/5206) @[wfxr](https://github.com/wfxr)
        - 削除済みの dispatcher を TiCDC が予期せず再スケジュールする可能性がある問題を修正しました。[#4874](https://github.com/pingcap/ticdc/issues/4874) @[wlwilliamx](https://github.com/wlwilliamx)
        - 再作成された dispatcher が古い checkpoint から開始した場合に、再起動後の TiCDC でデータレプリケーションギャップが残る可能性がある問題を修正しました。[#3846](https://github.com/pingcap/ticdc/issues/3846) @[hongyunyan](https://github.com/hongyunyan)
        - coordinator メッセージ処理中に TiCDC がハングして応答しなくなる可能性がある問題を修正しました。[#4440](https://github.com/pingcap/ticdc/issues/4440) @[wk989898](https://github.com/wk989898)
        - リクエストコンテキストがキャンセルされた後も、TiCDC の create、pause、remove changefeed 操作が長時間ハングしたり停止したままになったりする可能性がある問題を修正しました。[#4417](https://github.com/pingcap/ticdc/issues/4417) @[wk989898](https://github.com/wk989898)
        - log pulling 中に TiCDC が fast Region error または replication worker shutdown を処理する際に発生する可能性がある panic を修正しました。[#4472](https://github.com/pingcap/ticdc/issues/4472) @[lidezhu](https://github.com/lidezhu)
        - 頻繁な DDL を伴う syncpoint 有効ワークロードで、重複する block status リクエストの処理に TiCDC が過剰な時間を費やし、maintainer slow log や barrier 処理遅延を引き起こす問題を修正しました。[#4957](https://github.com/pingcap/ticdc/issues/4957) @[hongyunyan](https://github.com/hongyunyan)
        - etcd クラスターのメンバーシップ変更後に、TiCDC `cli changefeed list` が異なるクラスターの changefeed を表示する可能性がある問題を修正しました。[#5137](https://github.com/pingcap/ticdc/issues/5137) @[wk989898](https://github.com/wk989898)
        - シャットダウン中にタスクが送信または再スケジュールされた際に、TiCDC のスレッドプールのシャットダウンがハングする可能性がある問題を修正しました。[#4640](https://github.com/pingcap/ticdc/issues/4640) @[wk989898](https://github.com/wk989898)
        - dispatcher の `WAITING` ステータスが maintainer によって一時的に無視された場合に、`CREATE TABLE ... LIKE ...` などの一部の DDL で TiCDC が barrier を進める前に約 5 秒待機する問題を修正しました。[#4810](https://github.com/pingcap/ticdc/issues/4810) @[zier-one](https://github.com/zier-one)
        - 多数の changefeed を一時停止して再開した後に、TiCDC の changefeed のラグが増加し CPU 使用率が高くなる問題を修正しました。[#4653](https://github.com/pingcap/ticdc/issues/4653) @[lidezhu](https://github.com/lidezhu)
        - ソーステーブルのスキーマが明示的に指定されていない場合に、TiCDC がデータベース間の `CREATE TABLE ... LIKE` ステートメントをレプリケートできない問題を修正しました。[#5025](https://github.com/pingcap/ticdc/issues/5025) @[lidezhu](https://github.com/lidezhu)
        - ビュー定義で修飾されていないソーステーブル名が使用されている場合に、TiCDC がスキーマ間の `CREATE VIEW` ステートメントを誤ってレプリケートし、下流のレプリケーションが失敗したりビューが誤ったテーブルを参照したりする可能性がある問題を修正しました。[#5026](https://github.com/pingcap/ticdc/issues/5026) @[lidezhu](https://github.com/lidezhu)
        - PD ノードのスケールインまたはスケールアウト後に TiCDC が誤った etcd エンドポイントを使用し、削除された PD メンバーが繰り返し追加し直される問題を修正しました。[#12368](https://github.com/pingcap/tiflow/issues/12368) @[wk989898](https://github.com/wk989898)
        - 無効なグローバル checkpoint がコミットされた際に、TiCDC の redo dispatcher が `Initializing` 状態のままスタックし、redo メタデータの進行が停止する可能性がある問題を修正しました。[#4703](https://github.com/pingcap/ticdc/issues/4703) @[hongyunyan](https://github.com/hongyunyan)
        - 非常に多数のテーブルを処理する際に、TiCDC の changefeed の初期化が遅くなる問題を修正しました。[#5014](https://github.com/pingcap/ticdc/issues/5014) @[lidezhu](https://github.com/lidezhu)
        - 最後の changefeed が削除された後に、TiCDC が PD にクラスターレベルの stale なサービス GC safepoint を残し、上流の GC の進行をブロックする可能性がある問題を修正しました。[#4610](https://github.com/pingcap/ticdc/issues/4610) @[hongyunyan](https://github.com/hongyunyan)
        - `MultipleTableInfos` が空でない場合に、TiCDC が複数テーブルの DDL イベントのデコードに失敗したり、誤って処理したりする可能性がある問題を修正しました。[#4415](https://github.com/pingcap/ticdc/issues/4415) @[asddongmen](https://github.com/asddongmen)
        - `EXCHANGE PARTITION` DDL ステートメントをレプリケートする際に、エスケープされたバッククォートを含むパーティション名を TiCDC が破損させる問題を修正しました。[#4450](https://github.com/pingcap/ticdc/issues/4450) @[lidezhu](https://github.com/lidezhu)
        - サブスクリプションの checkpoint 更新が同時に行われる際に、TiCDC が event store で順序が乱れた checkpoint 更新を生成し、レプリケーション進行状況の追跡に不整合が生じる可能性がある問題を修正しました。[#4992](https://github.com/pingcap/ticdc/issues/4992) @[lidezhu](https://github.com/lidezhu)
        - EventCollector がまだメッセージを受信している場合に、TiCDC がシャットダウン中にデッドロックし、クリーンアップをブロックする可能性がある問題を修正しました。[#4434](https://github.com/pingcap/ticdc/issues/4434) @[wk989898](https://github.com/wk989898)
        - 匿名の `ADD INDEX` DDL ステートメントをレプリケートする際、特に再試行時や `CREATE TABLE LIKE` のレプリケーション時に、TiCDC が下流で不整合なインデックス名を生成する可能性がある問題を修正しました。[#2327](https://github.com/pingcap/ticdc/issues/2327) @[wk989898](https://github.com/wk989898)
        - 接続 watchdog の中断後に TiCDC が stale な CDC 接続を保持し続け、接続のクリーンアップが遅延して、sink のメモリが一杯になったときに changefeed のレプリケーションがスタックする問題を修正しました。[#19610](https://github.com/tikv/tikv/issues/19610) @[wk989898](https://github.com/wk989898)
        - stale な遅延削除 tombstone が原因で、TiCDC で再登録された capture がオンラインに復帰した後に再び削除される可能性がある問題を修正しました。[#4695](https://github.com/pingcap/ticdc/issues/4695) @[hongyunyan](https://github.com/hongyunyan)

    + Dumpling

        - `--output-filename-template` に条件ブロックの外で単独の `{{.Index}}` が含まれていない状態で `--rows/-r` または `--filesize/-F` を使用した場合に、Dumpling が chunk ファイルを上書きし、不完全なダンプ結果を生成する可能性がある問題を修正しました。[#68611](https://github.com/pingcap/tidb/issues/68611) @[D3Hunter](https://github.com/D3Hunter)
