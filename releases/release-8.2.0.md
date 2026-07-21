---
title: TiDB 8.2.0 Release Notes
summary: TiDB 8.2.0 の新機能、互換性の変更点、改善点、およびバグ修正についてご確認ください。
---

# TiDB 8.2.0 リリースノート {#tidb-8-2-0-release-notes}

発売日：2024年7月11日

TiDB バージョン: 8.2.0

クイックアクセス: [クイックスタート](https://docs-archive.pingcap.com/tidb/v8.2/quick-start-with-tidb)

バージョン8.2.0では、以下の主要な機能と改善点が導入されています。

<table><thead><tr><th>カテゴリ</th><th>機能／改善点</th><th>説明</th></tr></thead><tbody><tr><td rowspan="3">信頼性と可用性</td><td><a href="https://docs-archive.pingcap.com/tidb/v8.2/tiproxy-load-balance">TiProxyは複数のロードバランシングポリシーをサポートしています。</a></td><td> TiDB v8.2.0では、TiProxyはステータス、接続数、健全性、メモリ、CPU、ロケーションなど、さまざまな要素に基づいてTiDBノードを評価し、ランク付けします。 <code>policy</code>構成項目で指定された負荷分散ポリシーに従って、TiProxyはデータベース操作を実行する最適なTiDBノードを動的に選択します。これにより、リソース使用率全体が最適化され、クラスタのパフォーマンスが向上し、スループットが増加します。</td></tr><tr><td> <a href="https://docs-archive.pingcap.com/tidb/v8.2/system-variables#tidb_enable_parallel_hashagg_spill-new-in-v800">TiDB の並列 HashAgg アルゴリズムはディスク スピル (GA) をサポートします</a></td><td>HashAgg は、同じフィールド値を持つ行を効率的に集計するために TiDB で広く使用されている集計演算子です。TiDB v8.0.0 では、処理速度をさらに向上させる実験的機能として parallel HashAgg が導入されました。メモリリソースが不足している場合、parallel HashAgg は一時的にソートされたデータをディスクに書き出すことで、過剰なメモリ使用による潜在的な OOM リスクを回避します。これにより、ノードの安定性を維持しながらクエリ パフォーマンスが向上します。v8.2.0 では、この機能が一般提供 (GA) となり、デフォルトで有効になっているため、 <code>tidb_executor_concurrency</code>を使用して parallel HashAgg の同時実行性を安全に構成できます。</td></tr><tr><td> <a href="https://docs-archive.pingcap.com/tidb/v8.2/tidb-configuration-file#stats-load-concurrency-new-in-v540">統計情報の読み込み効率を最大10倍向上</a></td><td>SaaSやPaaSサービスなど、テーブルとパーティションの数が多いクラスタでは、統計情報のロード効率を改善することで、TiDBインスタンスの起動速度低下の問題を解決し、統計情報の動的ロードの成功率を高めることができます。この改善により、統計情報のロード失敗によるパフォーマンス低下が軽減され、クラスタの安定性が向上します。</td></tr><tr><td rowspan="1">データベースの運用と可観測性</td><td><a href="https://docs-archive.pingcap.com/tidb/v8.2/tidb-resource-control#bind-resource-groups">リソースグループの切り替えに対する特権制御を導入する</a></td><td>リソース制御は広く利用されているため、リソースグループの切り替えに関する権限制御は、データベースユーザーによるリソースの不正使用を防ぎ、管理者によるリソース使用全体の保護を強化し、クラスタの安定性を向上させることができる。</td></tr></tbody></table>

## 機能の詳細 {#feature-details}

### パフォーマンス {#performance}

-   TiKVへの以下のJSON関数のプッシュダウンをサポート [#50601](https://github.com/pingcap/tidb/issues/50601) @[dbsid](https://github.com/dbsid)

    -   `JSON_ARRAY_APPEND()`
    -   `JSON_MERGE_PATCH()`
    -   `JSON_REPLACE()`

    詳細については、 [ドキュメント](/functions-and-operators/expressions-pushed-down.md)を参照してください。

-   TiDB は並列ソートをサポート[#49217](https://github.com/pingcap/tidb/issues/49217) [#50746](https://github.com/pingcap/tidb/issues/50746) @[xzhangxian1008](https://github.com/xzhangxian1008)

    バージョン8.2.0より前のTiDBでは、ソート演算子は順次実行されるため、大量のデータをソートする際のクエリパフォーマンスに影響が出ていました。

    バージョン8.2.0以降、TiDBは並列ソートをサポートし、ソートパフォーマンスを大幅に向上させました。この機能は手動での設定は不要です。TiDBは、システム変数[`tidb_executor_concurrency`](/system-variables.md#tidb_executor_concurrency-new-in-v50)の値に基づいて、並列ソートを使用するかどうかを自動的に判断します。

    詳細については、 [ドキュメント](/system-variables.md#tidb_executor_concurrency-new-in-v50)を参照してください。

-   TiDB の並列 HashAgg アルゴリズムは、ディスク スピル (GA) をサポートしています。 [#35637](https://github.com/pingcap/tidb/issues/35637) @[xzhangxian1008](https://github.com/xzhangxian1008)

    TiDB v8.0.0 では、実験的機能としてディスクスピルをサポートする並列 HashAgg アルゴリズムが導入されました。v8.2.0 では、この機能が一般提供 (GA) されます。並列 HashAgg アルゴリズムを使用すると、TiDB はメモリ使用量に基づいて自動的にデータスピルをトリガーし、クエリのパフォーマンスとデータスループットのバランスを取ります。この機能はデフォルトで有効になっています。この機能を制御するシステム変数`tidb_enable_parallel_hashagg_spill`は、今後のリリースで非推奨となります。

    詳細については、 [ドキュメント](/system-variables.md#tidb_enable_parallel_hashagg_spill-new-in-v800)を参照してください。

### 信頼性 {#reliability}

-   統計の読み込み効率を最大 10 倍向上 [#52831](https://github.com/pingcap/tidb/issues/52831) @[hawkingrei](https://github.com/hawkingrei)

    SaaSやPaaSアプリケーションでは、データテーブルが多数存在する場合があり、初期統計情報の読み込み速度が低下するだけでなく、高負荷時のロード同期の失敗率も上昇します。TiDBの起動時間や実行プランの精度にも影響が出る可能性があります。v8.2.0では、TiDBは並行処理モデルやメモリ割り当てなど、複数の観点から統計情報の読み込みプロセスを最適化し、レイテンシーの削減、スループットの向上、そしてビジネスのスケーリングに影響を与える統計情報の読み込み速度の低下を回避します。

    適応型同時読み込みがサポートされるようになりました。デフォルトでは、設定項目[`stats-load-concurrency`](/tidb-configuration-file.md#stats-load-concurrency-new-in-v540)は`0`に設定されており、統計情報の読み込みの同時実行数はハードウェア仕様に基づいて自動的に選択されます。

    詳細については、 [ドキュメント](/tidb-configuration-file.md#stats-load-concurrency-new-in-v540)を参照してください。

### 可用性 {#availability}

-   TiProxyは複数のロードバランシングポリシーをサポートします [#465](https://github.com/pingcap/tiproxy/issues/465) @[djshow832](https://github.com/djshow832) @[xhebox](https://github.com/xhebox)

    TiProxyはTiDBの公式プロキシコンポーネントであり、クライアントとTiDBサーバーの間に配置されます。TiProxyはTiDBの負荷分散機能と接続維持関数を提供します。v8.2.0より前のバージョンでは、TiProxyはデフォルトでv1.0.0を使用しており、TiDBサーバーに対してステータスベースおよび接続数ベースの負荷分散ポリシーのみをサポートしています。

    バージョン8.2.0以降、TiProxyはデフォルトでバージョン1.1.0となり、複数の負荷分散ポリシーが導入されました。ステータスベースおよび接続数ベースのポリシーに加え、TiProxyは健全性、メモリ、CPU、およびロケーションに基づいた動的な負荷分散をサポートし、TiDBクラスタの安定性を向上させます。

    [`policy`](/tiproxy/tiproxy-configuration.md#policy)設定項目を通じて、負荷分散ポリシーの組み合わせと優先順位を設定できます。

    -   `resource` : リソース優先度ポリシーは、ステータス、ヘルス、メモリ、CPU、ロケーション、接続数という優先順位に基づいて負荷分散を実行します。
    -   `location` : ロケーション優先度ポリシーは、ステータス、ロケーション、ヘルス、メモリ、CPU、接続数という優先順位に基づいて負荷分散を実行します。
    -   `connection` : 最小接続数優先度ポリシーは、ステータスと接続数という次の優先度に基づいて負荷分散を実行します。

    詳細については、[ドキュメント](/tiproxy/tiproxy-load-balance.md)を参照してください。

### SQL {#sql}

-   TiDBはJSONスキーマ検証機能をサポートしています [#52779](https://github.com/pingcap/tidb/issues/52779) @[dveeden](https://github.com/dveeden)

    v8.2.0より前は、JSONデータの検証に外部ツールやカスタム検証ロジックを使用する必要があり、開発と保守の複雑さが増し、開発効率が低下していました。v8.2.0以降では、 `JSON_SCHEMA_VALID()`関数が導入されました。 `JSON_SCHEMA_VALID()`制約で`CHECK`を使用することで、データが追加された後にチェックするのではなく、不適合なデータが挿入されるのを防ぐことができます。この関数を使用すると、TiDB内でJSONデータの有効性を直接検証できるため、データの整合性と一貫性が向上し、開発効率が向上します。

    詳細については、 [ドキュメント](/functions-and-operators/json-functions.md#validation-functions)を参照してください。

### データベース操作 {#db-operations}

-   TiUPはPDマイクロサービスのデプロイをサポートします [#5766](https://github.com/tikv/pd/issues/5766) @[rleungx](https://github.com/rleungx)

    バージョン8.0.0以降、PDはマイクロサービスモードをサポートしています。このモードでは、PDのタイムスタンプ割り当て機能とクラスタスケジューリング関数が、それぞれ独立してデプロイ可能な個別のマイクロサービスに分割されます。これにより、リソース制御と分離性が向上し、異なるサービス間の影響が軽減されます。バージョン8.2.0より前は、PDマイクロサービスはTiDB Operatorを使用してのみデプロイできます。

    バージョン8.2.0以降、PDマイクロサービスはTiUPを使用してデプロイすることもできます。クラスター内で`tso`マイクロサービスと`scheduling`マイクロサービスを個別にデプロイすることで、PDのパフォーマンス拡張性を向上させ、大規模クラスターにおけるPDのパフォーマンスボトルネックを解消できます。このモードは、スケールアップでは解決できないほどPDが深刻なパフォーマンスボトルネックになった場合に推奨されます。

    詳細については、[ユーザー向けドキュメント](/pd-microservices.md)を参照してください。

-   リソースグループの切り替えに関する権限制御を追加 [#53440](https://github.com/pingcap/tidb/issues/53440) @[glorv](https://github.com/glorv)

    TiDBでは[`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md)コマンドまたは[`RESOURCE_GROUP()`](/optimizer-hints.md#resource_groupresource_group_name)ヒントを使用して他のリソースグループに切り替えることができますが、これにより一部のデータベースユーザーによるリソースグループの悪用につながる可能性があります。TiDB v8.2.0では、リソースグループの切り替えに対する権限制御が導入されました。 `RESOURCE_GROUP_ADMIN`または`RESOURCE_GROUP_USER`動的権限が付与されたデータベースユーザーのみが他のリソースグループに切り替えることができ、システムリソースの保護が強化されます。

    互換性を維持するため、以前のバージョンから v8.2.0 以降のバージョンにアップグレードする場合、元の動作が保持されます。拡張された権限制御を有効にするには、新しい変数[`tidb_resource_control_strict_mode`](/system-variables.md#tidb_resource_control_strict_mode-new-in-v820) `ON`に設定します。

    詳細については、 [ユーザー向けドキュメント](/tidb-resource-control-ru-groups.md#bind-resource-groups)を参照してください。

### 可観測性 {#observability}

-   実行プランがキャッシュされない理由を記録する [#50618](https://github.com/pingcap/tidb/issues/50618) @[qw4990](https://github.com/qw4990)

    場合によっては、実行オーバーヘッドを削減し、レイテンシーを低減するために、ほとんどの実行プランをキャッシュしたい場合があります。現在、SQL の実行プラン キャッシュにはいくつかの制限があります。一部の SQL ステートメントの実行プランはキャッシュできません。キャッシュできない SQL ステートメントと、それに対応する理由を特定するのは困難です。

    そのため、v8.2.0以降、実行プランをキャッシュできない理由を説明する新しい列`PLAN_CACHE_UNQUALIFIED`と`PLAN_CACHE_UNQUALIFIED_LAST_REASON`がシステムテーブル[`STATEMENTS_SUMMARY`](/statement-summary-tables.md)に追加され、パフォーマンスの調整に役立ちます。

    詳細については、 [ドキュメント](/statement-summary-tables.md#fields-description)を参照してください。

### セキュリティ {#security}

-   TiFlashログの感度低下を強化 [#8977](https://github.com/pingcap/tiflash/issues/8977) @[JaySon-Huang](https://github.com/JaySon-Huang)

    TiDB v8.0.0 では、ログの匿名化機能が強化され、TiDB ログ内のユーザー データがマーカー`‹ ›`で囲まれるかどうかを制御できるようになりました。マークされたログに基づいて、ログを表示する際にマークされた情報を削除するかどうかを決定できるため、ログの匿名化の柔軟性が向上します。v8.2.0 では、 TiFlash でログの匿名化に関する同様の機能強化が導入されています。この機能を使用するには、 TiFlash構成項目`security.redact_info_log`を`marker`に設定します。

    詳細については、 [ドキュメント](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)を参照してください。

### データ移行 {#data-migration}

-   複数の変更フィード間で TiCDC 同期ポイントを調整する [#11212](https://github.com/pingcap/tiflow/issues/11212) @[hongyunyan](https://github.com/hongyunyan)

    バージョン 8.2.0 より前は、複数のチェンジフィード間で TiCDC 同期ポイントを整合させるのは困難でした。チェンジフィードの作成時に、他のチェンジフィードの同期ポイントと整合するように、チェンジフィードの`startTs` `sync-point-interval`構成の倍数として作成されます。この変更により、同じ`sync-point-interval`構成を持つ複数のチェンジフィード間で同期ポイントを整合させることが可能になり、複数のダウンストリーム クラスタの整合が簡素化され、機能が向上します。

    詳細については、 [ドキュメント](/ticdc/ticdc-upstream-downstream-check.md#notes)を参照してください。

-   TiCDC Pulsar シンクは`pulsar+http`および`pulsar+https`接続プロトコルの使用をサポートしています [#11336](https://github.com/pingcap/tiflow/issues/11336) @[SandeepPadhi](https://github.com/SandeepPadhi)

    バージョン8.2.0より前は、TiCDC Pulsar Sinkは`pulsar`と`pulsar+ssl`接続プロトコルのみをサポートしていました。バージョン8.2.0以降では、TiCDC Pulsar Sinkは`pulsar+http`と`pulsar+https`プロトコルも接続にサポートするようになりました。この機能強化により、Pulsarへの接続の柔軟性が向上します。

    詳細については、[ドキュメント](/ticdc/ticdc-sink-to-pulsar.md#sink-uri)を参照してください。

## 互換性の変更 {#compatibility-changes}

> **Note:**
>
> このセクションでは、v8.1.0 から最新バージョン (v8.2.0) にアップグレードする際に知っておくべき互換性の変更点について説明します。v8.0.0 以前のバージョンから最新バージョンにアップグレードする場合は、中間バージョンで導入された互換性の変更点も確認する必要があるかもしれません。

### 動作の変更 {#behavior-changes}

-   TiDB Lightningを使用して CSV ファイルをインポートする場合、 `strict-format = true`を設定して大きな CSV ファイルを複数の小さな CSV ファイルに分割し、同時実行性とインポート パフォーマンスを向上させる場合は、 `terminator`明示的に指定する必要があります。指定できる値は、 `\r` 、 `\n` 、または`\r\n`です。行末文字を指定しないと、CSV ファイル データの解析時に例外が発生する可能性があります。 [#37338](https://github.com/pingcap/tidb/issues/37338) @[lance6716](https://github.com/lance6716)

-   [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)を使用して CSV ファイルをインポートする場合、大きな CSV ファイルを複数の小さな CSV ファイルに分割して同時実行性とインポート パフォーマンスを向上させるために`SPLIT_FILE`パラメーターを指定すると、行末文字`LINES_TERMINATED_BY`を明示的に指定する必要があります。指定できる値は`\r` 、 `\n` 、または`\r\n`です。行末文字を指定しないと、CSV ファイル データの解析時に例外が発生する可能性があります。 [#37338](https://github.com/pingcap/tidb/issues/37338) @[lance6716](https://github.com/lance6716)

-   BR v8.2.0 より前は、TiCDC レプリケーション タスクを持つクラスタで[BRデータ復元](/br/backup-and-restore-overview.md)実行することはサポートされていませんでした。v8.2.0 以降、 BR はTiCDC のデータ復元に関する制限を緩和しました。復元対象データの BackupTS (バックアップ時刻) が changefeed [`CheckpointTS`](/ticdc/ticdc-classic-architecture.md#checkpointts) (現在のレプリケーションの進行状況を示すタイムスタンプ) より前であれば、 BR は正常にデータ復元を進めることができます。 `BackupTS`は通常かなり前であることを考慮すると、ほとんどのシナリオで、 BR はTiCDC レプリケーション タスクを持つクラスタのデータ復元をサポートしていると考えられます。 [#53131](https://github.com/pingcap/tidb/issues/53131) @[YuJuncen](https://github.com/YuJuncen)

### MySQLとの互換性 {#mysql-compatibility}

-   v8.2.0より前は、 `PASSWORD REQUIRE CURRENT DEFAULT`オプションを指定して[`CREATE USER`](/sql-statements/sql-statement-create-user.md)ステートメントを実行すると、このオプションがサポートされておらず解析できないためエラーが返されます。v8.2.0以降、TiDBはMySQLとの互換性のためにこのオプションの解析と無視をサポートします。 [#53305](https://github.com/pingcap/tidb/issues/53305) @[dveeden](https://github.com/dveeden)

### システム変数 {#system-variables}

| 変数名                                                                                                                 | 変更の種類  | 説明                                                                                                                                                                                              |
| ------------------------------------------------------------------------------------------------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`tidb_analyze_distsql_scan_concurrency`](/system-variables.md#tidb_analyze_distsql_scan_concurrency-new-in-v760)   | 変更     | 最小値を`1`から`0`に変更します。これを`0`に設定すると、TiDB はクラスタサイズに基づいて`scan`操作を実行する際に`ANALYZE`操作の同時実行性を適応的に調整します。                                                                                                   |
| [`tidb_analyze_skip_column_types`](/system-variables.md#tidb_analyze_skip_column_types-new-in-v720)                 | 変更     | バージョン8.2.0以降、TiDBは潜在的なメモリ不足リスクを回避するため、デフォルトでは`MEDIUMTEXT`および`LONGTEXT`型の列を収集しません。                                                                                                               |
| [`tidb_auto_analyze_partition_batch_size`](/system-variables.md#tidb_auto_analyze_partition_batch_size-new-in-v640) | 変更     | TiDB クラスタのパフォーマンスに対する自動統計収集の影響を軽減するため、デフォルト値を`128`から`8192`に変更します。値の範囲を`[1, 1024]`から`[1, 8192]`に変更します。                                                                                           |
| [`tidb_enable_historical_stats`](/system-variables.md#tidb_enable_historical_stats)                                 | 変更     | デフォルト値を`ON`から`OFF`に変更します。これにより、履歴統計が無効になり、潜在的な安定性の問題を回避できます。                                                                                                                                    |
| [`tidb_executor_concurrency`](/system-variables.md#tidb_executor_concurrency-new-in-v50)                            | 変更     | `sort`演算子の同時実行設定のサポートを追加します。                                                                                                                                                                    |
| [`tidb_sysproc_scan_concurrency`](/system-variables.md#tidb_sysproc_scan_concurrency-new-in-v650)                   | 変更     | 最小値を`1`から`0`に変更します。これを`0`に設定すると、TiDB はクラスタサイズに基づいて、内部 SQL ステートメントの実行時に実行される`scan`操作の同時実行性を適応的に調整します。                                                                                            |
| [`tidb_resource_control_strict_mode`](/system-variables.md#tidb_resource_control_strict_mode-new-in-v820)           | 新しく追加された | [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md)ステートメントおよび[`RESOURCE_GROUP()`](/optimizer-hints.md#resource_groupresource_group_name)オプティマイザヒントに特権制御を適用するかどうかを制御します。 |

### コンフィグレーションファイルパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーションパラメータ                                                                                              | 変更の種類 | 説明                                                                                                                                                                    |
| -------------- | ------------------------------------------------------------------------------------------------------------ | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB           | [`concurrently-init-stats`](/tidb-configuration-file.md#concurrently-init-stats-new-in-v810-and-v752)        | 変更    | 統計情報の初期化にかかる時間を短縮するため、デフォルト値を`false`から`true`に変更します。この設定項目は、 [`lite-init-stats`](/tidb-configuration-file.md#lite-init-stats-new-in-v710) `false`に設定されている場合にのみ有効になります。 |
| TiDB           | [`stats-load-concurrency`](/tidb-configuration-file.md#stats-load-concurrency-new-in-v540)                   | 変更    | デフォルト値を`5`から`0`に変更し、最小値を`1`から`0`に変更します。値`0`は自動モードを意味し、サーバーの設定に基づいて同時実行数を自動的に調整します。                                                                                    |
| TiDB           | [`token-limit`](/tidb-configuration-file.md#token-limit)                                                     | 変更    | TiDB Server のメモリ不足エラー (OOM) が発生するのを避けるため、最大値を`18446744073709551615` (64 ビット プラットフォーム) および`4294967295` `1048576`に変更します。これにより、同時にリクエストを実行できるセッション数は最大`1048576`まで設定できます。 |
| TiKV           | [`max-apply-unpersisted-log-limit`](/tikv-configuration-file.md#max-apply-unpersisted-log-limit-new-in-v810) | 変更    | TiKVノードのI/Oジッターによって発生するロングテールレイテンシーを削減するため、デフォルト値を`0`から`1024`に変更します。これは、コミット済みだが永続化されていないRaftログの最大適用数が、デフォルトでは`1024`であることを意味します。                                      |
| TiKV           | [`server.grpc-compression-type`](/tikv-configuration-file.md#grpc-compression-type)                          | 変更    | この設定項目では、TiKVからTiDBに送信される応答メッセージの圧縮アルゴリズムも制御できるようになりました。圧縮を有効にすると、CPUリソースの消費量が増加する可能性があります。                                                                           |
| TiFlash        | [`security.redact_info_log`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)               | 変更    | 新しい値オプション`marker`が導入されました。値を`marker`に設定すると、ログ内のすべてのユーザーデータが`‹ ›`で囲まれます。                                                                                               |

### システムテーブル {#system-tables}

-   [`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md)および[`INFORMATION_SCHEMA.CLUSTER_PROCESSLIST`](/information-schema/information-schema-processlist.md#cluster_processlist)システム テーブルに`SESSION_ALIAS`フィールドを追加して、現在のセッションのエイリアスを表示します。 [#46889](https://github.com/pingcap/tidb/issues/46889) @[lcwangchao](https://github.com/lcwangchao)

### コンパイラバージョン {#compiler-versions}

-   TiFlashの開発エクスペリエンスを向上させるため、TiDBのコンパイルとビルドに必要なLLVMの最小バージョンが13.0から17.0にアップグレードされました。TiDB開発者の方は、スムーズなビルドを保証するために、LLVMコンパイラのバージョンをアップグレードする必要があります。 [#7193](https://github.com/pingcap/tiflash/issues/7193) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)

## 非推奨機能 {#deprecated-features}

-   バージョン8.2.0以降、以下の機能は非推奨となります。

    -   バージョン8.2.0以降、 [`enable-replica-selector-v2`](/tidb-configuration-file.md#enable-replica-selector-v2-new-in-v800)設定項目は非推奨となりました。TiKVへのRPCリクエスト送信時には、デフォルトで新しいバージョンのリージョンレプリカセレクタが使用されます。
    -   バージョン8.2.0以降、 BRスナップショット復元パラメータ`--concurrency`は非推奨となりました。代替手段として、 [`--tikv-max-restore-concurrency`](/br/use-br-command-line-tool.md#common-options)を使用して、スナップショット復元中のTiKVノードごとの同時実行タスクの最大数を設定できます。
    -   v8.2.0 以降、 BRスナップショット復元パラメータ`--granularity`は非推奨となり、 [粗視化リージョン散乱アルゴリズム](/br/br-snapshot-guide.md#restore-cluster-snapshots)デフォルトで有効になります。

-   以下の機能は、将来のバージョンで廃止される予定です。

    -   バージョン8.0.0では、TiDBは自動統計収集タスクの順序を最適化するために優先度キューを有効にするかどうかを制御するシステム変数[`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-new-in-v800)を導入しました。今後のバージョンでは、優先度キューが自動統計収集タスクの順序付けを行う唯一の方法となり、 [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-new-in-v800)システム変数は非推奨となります。
    -   バージョン8.0.0では、TiDBが並列ハッシュアグリゲーションアルゴリズムのディスクスピルをサポートするかどうかを制御するシステム変数[`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-new-in-v800)が導入されました。今後のバージョンでは、 [`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-new-in-v800)システム変数は非推奨となります。
    -   バージョン7.5.0では、TiDBがパーティション統計情報を非同期でマージしてメモリ不足エラーを回避するために、システム変数[`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-new-in-v750)が導入されました。今後のバージョンでは、パーティション統計情報はデフォルトで非同期でマージされるようになり、システム変数[`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-new-in-v750)は非推奨となります。
    -   今後のリリースでは [実行プランバインディングの自動進化](/sql-plan-management.md#baseline-evolution)が再設計される予定であり、関連する変数や動作が変更される予定です。
    -   TiDB Lightning のパラメータ[`conflict.max-record-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task) 、今後のリリースで非推奨となり、その後削除されます。このパラメータは[`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)に置き換えられます。これは、競合するレコードの最大数が、単一のインポートタスクで許容できる競合レコードの最大数と一致することを意味します。

-   今後のバージョンでは、以下の機能が削除される予定です。

    -   バージョン8.0.0以降、 TiDB Lightningは[旧バージョンの競合検出](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#the-old-version-of-conflict-detection-deprecated-in-v800)戦略を非推奨とし、 [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)パラメータを使用して論理インポートモードと物理インポートモードの両方の競合検出戦略を制御できるようにします。旧バージョンの競合検出の[`duplicate-resolution`](/tidb-lightning/tidb-lightning-configuration.md)パラメータは、今後のリリースで削除されます。

## 改善点 {#improvements}

-   TiDB

    -   [論理DDLステートメント（一般DDL）](/best-practices/ddl-introduction.md#types-of-ddl-statements)の並列実行をサポートします。 v8.1.0 と比較して、10 セッションを使用して異なる DDL ステートメントを同時に送信すると、パフォーマンスが 3 ～ 6 倍向上します [#53246](https://github.com/pingcap/tidb/issues/53246) @[D3Hunter](https://github.com/D3Hunter)
    -   `((a = 1 and b = 2 and c > 3) or (a = 4 and b = 5 and c > 6)) and d > 3`のような式を使用して複数列インデックスを照合するロジックを改善し、より正確な`Range`を生成します。 [#41598](https://github.com/pingcap/tidb/issues/41598) @[ghazalfamilyusa](https://github.com/ghazalfamilyusa)
    -   データ量の多いテーブルに対して単純なクエリを実行する際の、データ分布情報の取得パフォーマンスを最適化する [#53850](https://github.com/pingcap/tidb/issues/53850) @[you06](https://github.com/you06)
    -   集約された結果セットは IndexJoin の内部テーブルとして使用でき、より複雑なクエリを IndexJoin にマッチさせることが可能になり、インデックス作成によってクエリ効率が向上します。 [#37068](https://github.com/pingcap/tidb/issues/37068) @[elsa0520](https://github.com/elsa0520)
    -   TiFlash配置ルールを一括削除することで、パーティションテーブルに対して`TRUNCATE`または`DROP`操作を実行した後のデータGCの処理速度を向上させます [#54068](https://github.com/pingcap/tidb/issues/54068) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    -   Azure Identity LibrariesとMicrosoft Authentication Libraryのバージョンをアップグレードしてセキュリティを強化する [#53990](https://github.com/pingcap/tidb/issues/53990) @[hawkingrei](https://github.com/hawkingrei)
    -   TiDB Server のメモリ不足エラー（OOM）が発生しないように、 `token-limit`の最大値に`1048576`を設定してください。 [#53312](https://github.com/pingcap/tidb/issues/53312) @[djshow832](https://github.com/djshow832)
    -   TiFlash MPP実行パフォーマンスを向上させるため、MPP実行プランの列剪定を改善しました [#52133](https://github.com/pingcap/tidb/issues/52133) @[yibin87](https://github.com/yibin87)
    -   大量のデータ（&gt;1024行）を含むテーブルを検索する際の`IndexLookUp`演算子のパフォーマンスオーバーヘッドを最適化する [#53871](https://github.com/pingcap/tidb/issues/53871) @[crazycs520](https://github.com/crazycs520)
    -   MPPロードバランシング中にリージョンを持たないストアを削除する [#52313](https://github.com/pingcap/tidb/issues/52313) @[xzhangxian1008](https://github.com/xzhangxian1008)

-   TiKV

    -   単一の圧縮ジョブに関係する SST ファイルの数を表示する**圧縮ジョブサイズ (ファイル)**メトリックを追加します [#16837](https://github.com/tikv/tikv/issues/16837) @[zhangjinpeng87](https://github.com/zhangjinpeng87)
    -   [早期応募](/tikv-configuration-file.md#max-apply-unpersisted-log-limit-new-in-v810)をデフォルトで有効にします。この機能を有効にすると、 Raftリーダーは、クォーラム ピアがログを永続化した後、リーダー自身がログを永続化するのを待たずにログを適用できるため、少数の TiKV ノードでのジッターが書き込みリクエストのレイテンシーに与える影響が軽減されます。 [#16717](https://github.com/tikv/tikv/issues/16717) @[glorv](https://github.com/glorv)
    -   **Raftのドロップメッセージ**の可視性を向上させ、書き込み速度低下の根本原因を特定する [#17093](https://github.com/tikv/tikv/issues/17093) @[Connor1996](https://github.com/Connor1996)
    -   クラスターのレイテンシーの問題をトラブルシューティングするために、ファイル取り込みレイテンシーの可視性を向上させる [#17078](https://github.com/tikv/tikv/issues/17078) @[LykxSassinator](https://github.com/LykxSassinator)
    -   リージョンレプリカのクリーンアップに別のスレッドを使用して、重要なRaftの読み取りと書き込みのレイテンシーを安定させる [#16001](https://github.com/tikv/tikv/issues/16001) @[hbisheng](https://github.com/hbisheng)
    -   適用されるスナップショットの数の可視性を向上させる [#17078](https://github.com/tikv/tikv/issues/17078) @[hbisheng](https://github.com/hbisheng)

-   PD

    -   リージョンハートビート処理のパフォーマンスを改善 [#7897](https://github.com/tikv/pd/issues/7897) @[nolouch](https://github.com/nolouch)@[rleungx](https://github.com/rleungx) @[JmPotato](https://github.com/JmPotato)
    -   pd-ctl は、バイトまたはクエリ次元によるホット リージョンのクエリをサポートします [#7369](https://github.com/tikv/pd/issues/7369) @[lhy1024](https://github.com/lhy1024)

-   TiFlash

    -   高並行データ読み取り操作時のロック競合を減らし、短いクエリのパフォーマンスを最適化 [#9125](https://github.com/pingcap/tiflash/issues/9125) @[JinheLin](https://github.com/JinheLin)
    -   `Join`演算子 [#9057](https://github.com/pingcap/tiflash/issues/9057) @[gengliqi](https://github.com/gengliqi)内の Join Key の重複コピーを削除します。
    -   `HashAgg` 演算子で 2 レベルハッシュテーブルの変換処理を同時に実行します [#8956](https://github.com/pingcap/tiflash/issues/8956) @[gengliqi](https://github.com/gengliqi)
    -   `HashAgg`演算子の冗長な集計関数を削除して計算オーバーヘッドを削減 [#8891](https://github.com/pingcap/tiflash/issues/8891) @[guo-shaoge](https://github.com/guo-shaoge)

-   ツール

    -   Backup & Restore (BR)

        -   バックアップ機能を最適化し、ノードの再起動、クラスターのスケールアウト、および多数のテーブルをバックアップする際のネットワーク ジッター時のバックアップ パフォーマンスと安定性を向上させます [#52534](https://github.com/pingcap/tidb/issues/52534) @[3pointer](https://github.com/3pointer)
        -   データ復元時にTiCDCチェンジフィードのきめ細かいチェックを実装します。チェンジフィードの[`CheckpointTS`](/ticdc/ticdc-classic-architecture.md#checkpointts)データバックアップ時刻より後であれば、復元操作に影響はなく、不要な待ち時間を短縮し、ユーザーエクスペリエンスを向上させます。 [#53131](https://github.com/pingcap/tidb/issues/53131) @[YuJuncen](https://github.com/YuJuncen)
        -   [`BACKUP`](/sql-statements/sql-statement-backup.md)ステートメントと[`RESTORE`](/sql-statements/sql-statement-restore.md)ステートメントに、 `CHECKSUM_CONCURRENCY`などのよく使用されるパラメーターをいくつか追加します [#53040](https://github.com/pingcap/tidb/issues/53040) @[RidRisR](https://github.com/RidRisR)
        -   `br log restore`サブコマンドを除き、他のすべての`br log`サブコマンドは、メモリ消費量を削減するために TiDB `domain`データ構造の読み込みをスキップすることをサポートしています [#52088](https://github.com/pingcap/tidb/issues/52088) @[Leavrth](https://github.com/Leavrth)
        -   ログバックアップ中に生成される一時ファイルの暗号化をサポート [#15083](https://github.com/tikv/tikv/issues/15083) @[YuJuncen](https://github.com/YuJuncen)
        -   Grafana ダッシュボードに`tikv_log_backup_pending_initial_scan`モニタリング メトリクスを追加します [#16656](https://github.com/tikv/tikv/issues/16656) @[3pointer](https://github.com/3pointer)
        -   PITRログの出力形式を最適化し、ログに`RestoreTS`フィールドを追加する [#53645](https://github.com/pingcap/tidb/issues/53645) @[dveeden](https://github.com/dveeden)

    -   TiCDC

        -   ダウンストリームがメッセージキュー（MQ）またはクラウドストレージの場合に、生イベントを直接出力する機能をサポートする [#11211](https://github.com/pingcap/tiflow/issues/11211) @[CharlesCheung96](https://github.com/CharlesCheung96)

## バグ修正 {#bug-fixes}

-   TiDB

    -   SQL文に外部結合が含まれ、結合条件に`false IN (column_name)`式が含まれている場合に、クエリ結果に一部のデータが欠落する問題を修正しました。 [#49476](https://github.com/pingcap/tidb/issues/49476) @[ghazalfamilyusa](https://github.com/ghazalfamilyusa)
    -   TiDBがテーブルの統計情報を収集する際に`PREDICATE COLUMNS`システムテーブルの列の統計情報が収集される問題を修正しました [#53403](https://github.com/pingcap/tidb/issues/53403) @[Rustin170506](https://github.com/Rustin170506)
    -   `tidb_enable_column_tracking`システム変数が`tidb_persist_analyze_options`に設定されている場合、 `OFF`システム変数が有効にならない問題を修正します。 [#53478](https://github.com/pingcap/tidb/issues/53478) @[Rustin170506](https://github.com/Rustin170506)
    -   `(*PointGetPlan).StatsInfo()`の実行中に発生する可能性のあるデータ競合の問題を修正します[#49803](https://github.com/pingcap/tidb/issues/49803) [#43339](https://github.com/pingcap/tidb/issues/43339) @[qw4990](https://github.com/qw4990)
    -   データ変更操作を含むトランザクションで仮想列を持つテーブルをクエリすると、TiDB が誤ったクエリ結果を返す可能性がある問題を修正しました [#53951](https://github.com/pingcap/tidb/issues/53951) @[qw4990](https://github.com/qw4990)
    -   `tidb_enable_async_merge_global_stats`および`tidb_analyze_partition_concurrency`システム変数が自動統計収集中に有効にならない問題を修正 [#53972](https://github.com/pingcap/tidb/issues/53972) @[Rustin170506](https://github.com/Rustin170506)
    -   TiDB が`plan not supported`をクエリした際に`TABLESAMPLE`エラーを返す可能性がある問題を修正 [#54015](https://github.com/pingcap/tidb/issues/54015) @[tangenta](https://github.com/tangenta)
    -   `SELECT DISTINCT CAST(col AS DECIMAL), CAST(col AS SIGNED) FROM ...`クエリを実行すると誤った結果が返される可能性がある問題を修正しました [#53726](https://github.com/pingcap/tidb/issues/53726) @[hawkingrei](https://github.com/hawkingrei)
    -   クライアント側でデータ読み取りタイムアウト後にクエリを終了できない問題を修正 [#44009](https://github.com/pingcap/tidb/issues/44009) @[wshwsh12](https://github.com/wshwsh12)
    -   述語における`Longlong`型のオーバーフロー問題を修正 [#45783](https://github.com/pingcap/tidb/issues/45783) @[hawkingrei](https://github.com/hawkingrei)
    -   Window関数内に関連サブクエリがある場合にpanicする可能性がある問題を修正しました [#42734](https://github.com/pingcap/tidb/issues/42734) @[Rustin170506](https://github.com/Rustin170506)
    -   TopN演算子が正しくプッシュダウンされない可能性がある問題を修正しました [#37986](https://github.com/pingcap/tidb/issues/37986) @[qw4990](https://github.com/qw4990)
    -   クラスター化インデックスを述語として使用する場合に`SELECT INTO OUTFILE`が機能しない問題を修正 [#42093](https://github.com/pingcap/tidb/issues/42093) @[qw4990](https://github.com/qw4990)
    -   情報スキーマキャッシュのミスによって古い読み取りのクエリレイテンシーが増加する問題を修正します [#53428](https://github.com/pingcap/tidb/issues/53428) @[crazycs520](https://github.com/crazycs520)
    -   `YEAR`型の列を範囲外の符号なし整数と比較すると誤った結果が生じる問題を修正しました [#50235](https://github.com/pingcap/tidb/issues/50235) @[qw4990](https://github.com/qw4990)
    -   TiDBを再起動した後に、主キー列統計のヒストグラムとTopNが読み込まれない問題を修正しました [#37548](https://github.com/pingcap/tidb/issues/37548) @[hawkingrei](https://github.com/hawkingrei)
    -   `final` AggMode と`non-final` AggMode が大規模並列処理 (MPP) で共存できない問題を修正します [#51362](https://github.com/pingcap/tidb/issues/51362) @[AilinKid](https://github.com/AilinKid)
    -   述語が常に`SHOW ERRORS`である`true`ステートメントを実行すると TiDB がパニックを起こす問題を修正します [#46962](https://github.com/pingcap/tidb/issues/46962) @[elsa0520](https://github.com/elsa0520)
    -   ビューの使用が再帰的CTEで機能しない問題を修正 [#49721](https://github.com/pingcap/tidb/issues/49721) @[hawkingrei](https://github.com/hawkingrei)
    -   TiDB が起動時に統計をロードするときに GC が原因でエラーを報告する可能性がある問題を修正 [#53592](https://github.com/pingcap/tidb/issues/53592) @[you06](https://github.com/you06)
    -   `PREPARE` / `EXECUTE`ステートメントで`CONV`式に`?`引数が含まれている場合、複数回実行するとクエリ結果が正しくない可能性がある問題を修正します。 [#53505](https://github.com/pingcap/tidb/issues/53505) @[qw4990](https://github.com/qw4990)
    -   非 BIGINT 符号なし整数が文字列/10 進数と比較したときに誤った結果を生成する可能性がある問題を修正 [#41736](https://github.com/pingcap/tidb/issues/41736) @[LittleFall](https://github.com/LittleFall)
    -   TiDBが外部キーを持つテーブルを作成する際に、対応する統計メタデータ（ `stats_meta` ）を作成しない問題を修正 [#53652](https://github.com/pingcap/tidb/issues/53652) @[hawkingrei](https://github.com/hawkingrei)
    -   クエリ内の特定のフィルタ条件によってプランナーモジュールが`invalid memory address or nil pointer dereference`エラーを報告する可能性がある問題を修正しました[#53582](https://github.com/pingcap/tidb/issues/53582) [#53580](https://github.com/pingcap/tidb/issues/53580) [#53594](https://github.com/pingcap/tidb/issues/53594) [#53603](https://github.com/pingcap/tidb/issues/53603) @[YangKeao](https://github.com/YangKeao)
    -   `CREATE OR REPLACE VIEW`を同時に実行すると`table doesn't exist`エラーが発生する可能性がある問題を修正しました [#53673](https://github.com/pingcap/tidb/issues/53673) @[tangenta](https://github.com/tangenta)
    -   `STATE`フィールドの`INFORMATION_SCHEMA.TIDB_TRX`が定義されていないため、 `size`テーブルの`STATE`フィールドが空になる問題を修正しました。 [#53026](https://github.com/pingcap/tidb/issues/53026) @[cfzjywxk](https://github.com/cfzjywxk)
    -   `Distinct_count`が無効になっている場合、グローバル統計の`tidb_enable_async_merge_global_stats`情報が正しくない可能性がある問題を修正しました [#53752](https://github.com/pingcap/tidb/issues/53752) @[hawkingrei](https://github.com/hawkingrei)
    -   オプティマイザヒント使用時の警告情報の誤りを修正 [#53767](https://github.com/pingcap/tidb/issues/53767) @[hawkingrei](https://github.com/hawkingrei)
    -   時間型を否定すると誤った値になる問題を修正 [#52262](https://github.com/pingcap/tidb/issues/52262) @[solotzg](https://github.com/solotzg)
    -   `REGEXP()`空のパターン引数に対して明示的にエラーを報告しない問題を修正 [#53221](https://github.com/pingcap/tidb/issues/53221) @[yibin87](https://github.com/yibin87)
    -   JSONをdatetimeに変換すると、場合によっては精度が失われる問題を修正しました [#53352](https://github.com/pingcap/tidb/issues/53352) @[YangKeao](https://github.com/YangKeao)
    -   `JSON_QUOTE()`が場合によっては誤った結果を返す問題を修正 [#37294](https://github.com/pingcap/tidb/issues/37294) @[dveeden](https://github.com/dveeden)
    -   `ALTER TABLE ... REMOVE PARTITIONING`の実行時にデータ損失が発生する可能性がある問題を修正 [#53385](https://github.com/pingcap/tidb/issues/53385) @[mjonss](https://github.com/mjonss)
    -   `auth_socket`認証プラグインを使用している場合、TiDBが認証されていないユーザー接続を拒否できない場合がある問題を修正します [#54031](https://github.com/pingcap/tidb/issues/54031) @[lcwangchao](https://github.com/lcwangchao)
    -   JSON関連の関数が場合によってはMySQLと矛盾するエラーを返す問題を修正 [#53799](https://github.com/pingcap/tidb/issues/53799) @[dveeden](https://github.com/dveeden)
    -   `INDEX_LENGTH`内のパーティションテーブルの`INFORMATION_SCHEMA.PARTITIONS`フィールドが正しくない問題を修正します [#54173](https://github.com/pingcap/tidb/issues/54173) @[Defined2014](https://github.com/Defined2014)
    -   `TIDB_ROW_ID_SHARDING_INFO`テーブルの`INFORMATION_SCHEMA.TABLES`フィールドが正しくない問題を修正 [#52330](https://github.com/pingcap/tidb/issues/52330) @[tangenta](https://github.com/tangenta)
    -   生成された列が無効なタイムスタンプを返す問題を修正 [#52509](https://github.com/pingcap/tidb/issues/52509) @[lcwangchao](https://github.com/lcwangchao)
    -   分散実行フレームワーク（DXF）を使用してインデックスを追加する際に、 `max-index-length`を設定するとTiDBがpanicを起こす問題を修正しました [#53281](https://github.com/pingcap/tidb/issues/53281) @[zimulala](https://github.com/zimulala)
    -   場合によっては無効な列タイプ`DECIMAL(0,0)`が作成される問題を修正 [#53779](https://github.com/pingcap/tidb/issues/53779) @[tangenta](https://github.com/tangenta)
    -   `CURRENT_DATE()`を列のデフォルト値として使用するとクエリ結果が正しくない問題を修正 [#53746](https://github.com/pingcap/tidb/issues/53746) @[tangenta](https://github.com/tangenta)
    -   `ALTER DATABASE ... SET TIFLASH REPLICA`ステートメントがTiFlashレプリカを`SEQUENCE`テーブルに誤って追加する問題を修正しました [#51990](https://github.com/pingcap/tidb/issues/51990) @[jiyfhust](https://github.com/jiyfhust)
    -   `REFERENCED_TABLE_SCHEMA`テーブルの`INFORMATION_SCHEMA.KEY_COLUMN_USAGE`フィールドが正しくない問題を修正します [#52350](https://github.com/pingcap/tidb/issues/52350) @[wd0517](https://github.com/wd0517)
    -   `AUTO_ID_CACHE=1`の場合に、単一のステートメントで複数の行を挿入すると`AUTO_INCREMENT`列が不連続になる問題を修正しました。 [#52465](https://github.com/pingcap/tidb/issues/52465) @[tiancaiamao](https://github.com/tiancaiamao)
    -   非推奨警告のフォーマットを修正 [#52515](https://github.com/pingcap/tidb/issues/52515) @[dveeden](https://github.com/dveeden)
    -   `TRACE`で`copr.buildCopTasks`コマンドが欠落している問題を修正 [#53085](https://github.com/pingcap/tidb/issues/53085) @[time-and-fate](https://github.com/time-and-fate)
    -   `memory_quota`ヒントがサブクエリで機能しない可能性がある問題を修正しました [#53834](https://github.com/pingcap/tidb/issues/53834) @[qw4990](https://github.com/qw4990)
    -   メタデータロックの不適切な使用により、特定の状況下でプランキャッシュを使用する際に異常なデータが書き込まれる可能性がある問題を修正しました [#53634](https://github.com/pingcap/tidb/issues/53634) @[zimulala](https://github.com/zimulala)
    -   トランザクション内のステートメントがメモリ不足で強制終了された後、TiDB が同じトランザクション内の次のステートメントの実行を継続すると、 `Trying to start aggressive locking while it's already started`エラーが発生し、panicが発生する可能性がある問題を修正しました。 [#53540](https://github.com/pingcap/tidb/issues/53540) @[MyonKeminta](https://github.com/MyonKeminta)

-   TiKV

    -   `JSON_ARRAY_APPEND()`関数を TiKV にプッシュダウンすると TiKV がpanicを起こす問題を修正しました [#16930](https://github.com/tikv/tikv/issues/16930) @[dbsid](https://github.com/dbsid)
    -   リーダーが失敗したスナップショットファイルを時間内にクリーンアップしない問題を修正 [#16976](https://github.com/tikv/tikv/issues/16976) @[hbisheng](https://github.com/hbisheng)
    -   高度な同時コプロセッサー要求が TiKV OOM を引き起こす可能性がある問題を修正 [#16653](https://github.com/tikv/tikv/issues/16653) @[overvenus](https://github.com/overvenus)
    -   `raftstore.periodic-full-compact-start-times`設定項目をオンラインで変更すると TiKV がpanicを引き起こす可能性がある問題を修正 [#17066](https://github.com/tikv/tikv/issues/17066) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
    -   `make docker`と`make docker_test`の不具合を修正 [#17075](https://github.com/tikv/tikv/issues/17075) @[shunki-fujita](https://github.com/shunki-fujita)
    -   監視ダッシュボードで**gRPC リクエストソースの期間**メトリクスが正しく表示されない問題を修正 [#17133](https://github.com/tikv/tikv/issues/17133) @[King-Dylan](https://github.com/King-Dylan)
    -   TiKVからTiDBに送信されるメッセージに対して`grpc-compression-type`を介してgRPCメッセージ圧縮方法を設定しても効果がない問題を修正しました [#17176](https://github.com/tikv/tikv/issues/17176) @[ekexium](https://github.com/ekexium)
    -   tikv-ctl の`raft region`コマンドの出力にリージョンステータス情報が含まれていない問題を修正 [#17037](https://github.com/tikv/tikv/issues/17037) @[glorv](https://github.com/glorv)
    -   CDCとlog-backupが`check_leader`構成を使用して`advance-ts-interval` のタイムアウトを制限しないため、場合によってはTiKVが正常に再起動した際に`resolved_ts`のラグが大きくなりすぎる問題を修正しました。 [#17107](https://github.com/tikv/tikv/issues/17107) @[MyonKeminta](https://github.com/MyonKeminta)

-   PD

    -   `ALTER PLACEMENT POLICY`が配置ポリシーを変更できない問題を修正[#52257](https://github.com/pingcap/tidb/issues/52257) [#51712](https://github.com/pingcap/tidb/issues/51712) @[jiyfhust](https://github.com/jiyfhust)
    -   書き込みホットスポットのスケジューリングによって配置ポリシーの制約が破られる可能性がある問題を修正 [#7848](https://github.com/tikv/pd/issues/7848) @[lhy1024](https://github.com/lhy1024)
    -   配置ルール使用時にダウンしたピアが復旧しない可能性がある問題を修正 [#7808](https://github.com/tikv/pd/issues/7808) @[rleungx](https://github.com/rleungx)
    -   リソースグループクエリをキャンセルした際に多数の再試行が発生する問題を修正 [#8217](https://github.com/tikv/pd/issues/8217) @[nolouch](https://github.com/nolouch)
    -   PDリーダーの手動転送が失敗する可能性がある問題を修正 [#8225](https://github.com/tikv/pd/issues/8225) @[HuSharp](https://github.com/HuSharp)

-   TiFlash

    -   空のパーティションを含むパーティションテーブルに対してクエリを実行する際に発生するクエリタイムアウトの問題を修正 [#9024](https://github.com/pingcap/tiflash/issues/9024) @[JinheLin](https://github.com/JinheLin)
    -   分散ストレージおよびコンピューティングアーキテクチャにおいて、DDL操作で非null列を追加した後、クエリでnull値が誤って返される可能性がある問題を修正します [#9084](https://github.com/pingcap/tiflash/issues/9084) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    -   `SUBSTRING_INDEX()`関数が一部の特殊なケースでTiFlashをクラッシュさせる可能性がある問題を修正しました [#9116](https://github.com/pingcap/tiflash/issues/9116) @[wshwsh12](https://github.com/wshwsh12)
    -   BRまたはTiDB Lightning経由でデータをインポートした後、FastScanモードで多数の重複行が読み込まれる可能性がある問題を修正しました [#9118](https://github.com/pingcap/tiflash/issues/9118) @[JinheLin](https://github.com/JinheLin)

-   ツール

    -   Backup & Restore (BR)

        -   空の`EndKey`が原因でBR がトランザクション KV クラスターの復元に失敗する問題を修正 [#52574](https://github.com/pingcap/tidb/issues/52574) @[3pointer](https://github.com/3pointer)
        -   PD接続障害により、ログバックアップアドバンサーの所有者が存在するTiDBインスタンスがpanicを起こす可能性がある問題を修正 [#52597](https://github.com/pingcap/tidb/issues/52597) @[YuJuncen](https://github.com/YuJuncen)
        -   アドバンサー所有者の移行後にログバックアップが一時停止される可能性がある問題を修正 [#53561](https://github.com/pingcap/tidb/issues/53561) @[RidRisR](https://github.com/RidRisR)
        -   復元プロセス中に複数回のネストされた再試行によりBRがエラーを正しく識別できない問題を修正 [#54053](https://github.com/pingcap/tidb/issues/54053) @[RidRisR](https://github.com/RidRisR)
        -   TiKV構成を取得するために使用される接続が閉じられない可能性がある問題を修正 [#52595](https://github.com/pingcap/tidb/issues/52595) @[RidRisR](https://github.com/RidRisR)
        -   `TestStoreRemoved`テストケースが不安定になる問題を修正 [#52791](https://github.com/pingcap/tidb/issues/52791) @[YuJuncen](https://github.com/YuJuncen)
        -   ポイントインタイムリカバリ（PITR）中にTiFlashがクラッシュする問題を修正 [#52628](https://github.com/pingcap/tidb/issues/52628) @[RidRisR](https://github.com/RidRisR)
        -   増分バックアップ中の DDL ジョブのスキャンにおける非効率性の問題を修正 [#54139](https://github.com/pingcap/tidb/issues/54139) @[3pointer](https://github.com/3pointer)
        -   リージョンリーダーのシーク中に中断が発生するため、チェックポイントバックアップ中のバックアップパフォーマンスに影響が出る問題を修正しました [#17168](https://github.com/tikv/tikv/issues/17168) @[Leavrth](https://github.com/Leavrth)

    -   TiCDC

        -   Grafana の**Kafka 送信バイト**パネルの表示が不正確な問題を修正 [#10777](https://github.com/pingcap/tiflow/issues/10777) @[asddongmen](https://github.com/asddongmen)
        -   マルチノード環境で多数の`UPDATE`操作を実行する際に Changefeed を繰り返し再起動するとデータ不整合が発生する可能性がある問題を修正しました [#11219](https://github.com/pingcap/tiflow/issues/11219) @[lidezhu](https://github.com/lidezhu)

    -   TiDB Data Migration (DM)

        -   `go-mysql` をアップグレードして、接続ブロックの問題を修正します。 [#11041](https://github.com/pingcap/tiflow/issues/11041) @[D3Hunter](https://github.com/D3Hunter)
        -   MariaDBデータの移行中に`SET`ステートメントが原因でDMがpanicを起こす問題を修正 [#10206](https://github.com/pingcap/tiflow/issues/10206) @[dveeden](https://github.com/dveeden)

    -   TiDB Lightning

        -   TiDB Lightningがzstd圧縮ファイルのインポート時にエラーを報告する可能性がある問題を修正しました [#53587](https://github.com/pingcap/tidb/issues/53587) @[lance6716](https://github.com/lance6716)

    -   Dumpling

        -   Dumplingがテーブルとビューを同時にエクスポートする際にエラーを報告する問題を修正 [#53682](https://github.com/pingcap/tidb/issues/53682) @[tangenta](https://github.com/tangenta)

    -   TiDB Binlog

        -   TiDB Binlogが有効になっている場合、 `ADD COLUMN`の実行中に行を削除するとエラー`data and columnID count not match`が報告される可能性がある問題を修正しました [#53133](https://github.com/pingcap/tidb/issues/53133) @[tangenta](https://github.com/tangenta)

## 貢献者 {#contributors}

TiDBコミュニティの以下の貢献者の皆様に感謝申し上げます。

-   [CabinfeverB](https://github.com/CabinfeverB)
-   [DanRoscigno](https://github.com/DanRoscigno) (初回貢献者)
-   [ei-sugimoto](https://github.com/ei-sugimoto) (初回貢献者)
-   [eltociear](https://github.com/eltociear)
-   [jiyfhust](https://github.com/jiyfhust)
-   [michaelmdeng](https://github.com/michaelmdeng) (初回貢献者)
-   [mittalrishabh](https://github.com/mittalrishabh)
-   [onlyacat](https://github.com/onlyacat)
-   [qichengzx](https://github.com/qichengzx) (初回貢献者)
-   [SeaRise](https://github.com/SeaRise)
-   [shawn0915](https://github.com/shawn0915)
-   [shunki-fujita](https://github.com/shunki-fujita) (初回貢献者)
-   [tonyxuqqi](https://github.com/tonyxuqqi)
-   [wwu](https://github.com/wwu) (初回貢献者)
-   [yzhan1](https://github.com/yzhan1)
