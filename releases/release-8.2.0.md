---
title: TiDB 8.2.0 Release Notes
summary: TiDB 8.2.0 の新機能、互換性の変更、改善点、バグ修正について説明します。
---

# TiDB 8.2.0 リリースノート {#tidb-8-2-0-release-notes}

発売日：2024年7月11日

TiDB バージョン: 8.2.0

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v8.2/quick-start-with-tidb)

8.2.0 では、次の主な機能と改善が導入されています。

<table><thead><tr><th>カテゴリ</th><th>機能/拡張機能</th><th>説明</th></tr></thead><tbody><tr><td rowspan="3">信頼性と可用性</td><td><a href="https://docs.pingcap.com/tidb/v8.2/tiproxy-load-balance">TiProxyは複数の負荷分散ポリシーをサポート</a></td><td>TiDB v8.2.0では、TiProxyはステータス、接続数、健全性、メモリ、CPU、ロケーションなど、様々な要素に基づいてTiDBノードを評価し、ランク付けします。 <code>policy</code>設定項目で指定された負荷分散ポリシーに従って、TiProxyはデータベース操作を実行する最適なTiDBノードを動的に選択します。これにより、全体的なリソース使用率が最適化され、クラスタのパフォーマンスとスループットが向上します。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v8.2/system-variables#tidb_enable_parallel_hashagg_spill-new-in-v800">TiDB の並列 HashAgg アルゴリズムはディスク スピル (GA) をサポートします</a></td><td>HashAggは、同じフィールド値を持つ行を効率的に集計するためにTiDBで広く使用されている集計演算子です。TiDB v8.0.0では、処理速度をさらに向上させるための実験的機能として並列HashAggが導入されました。メモリリソースが不足している場合、並列HashAggは一時的にソートされたデータをディスクに書き出すことで、過剰なメモリ使用による潜在的なOOMリスクを回避します。これにより、ノードの安定性を維持しながらクエリパフォーマンスが向上します。v8.2.0では、この機能が一般提供（GA）され、デフォルトで有効化されているため、 <code>tidb_executor_concurrency</code>を使用して並列HashAggの同時実行性を安全に設定できます。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v8.2/tidb-configuration-file#stats-load-concurrency-new-in-v540">統計読み込み効率を最大10倍向上</a></td><td>SaaSやPaaSサービスなど、多数のテーブルとパーティションを持つクラスターでは、統計情報の読み込み効率を向上させることで、TiDBインスタンスの起動が遅い問題を解決し、統計情報の動的読み込みの成功率を向上させることができます。この改善により、統計情報の読み込み失敗によるパフォーマンスのロールバックが削減され、クラスターの安定性が向上します。</td></tr><tr><td rowspan="1"> DB操作と可観測性</td><td><a href="https://docs.pingcap.com/tidb/v8.2/tidb-resource-control#bind-resource-groups">スイッチングリソースグループの権限制御を導入する</a></td><td>リソース制御が広く使用されているため、リソース グループの切り替えの権限制御により、データベース ユーザーによるリソースの悪用を防ぎ、管理者の全体的なリソース使用の保護を強化し、クラスターの安定性を向上させることができます。</td></tr></tbody></table>

## 機能の詳細 {#feature-details}

### パフォーマンス {#performance}

-   次の JSON関数をTiKV [＃50601](https://github.com/pingcap/tidb/issues/50601) @ [dbsid](https://github.com/dbsid)にプッシュダウンすることをサポートします

    -   `JSON_ARRAY_APPEND()`
    -   `JSON_MERGE_PATCH()`
    -   `JSON_REPLACE()`

    詳細については[ドキュメント](/functions-and-operators/expressions-pushed-down.md)参照してください。

-   TiDBは並列ソートをサポート[＃49217](https://github.com/pingcap/tidb/issues/49217) [＃50746](https://github.com/pingcap/tidb/issues/50746) @ [xzhangxian1008](https://github.com/xzhangxian1008)

    v8.2.0 より前のバージョンでは、TiDB は Sort 演算子を順番にのみ実行するため、大量のデータをソートする場合のクエリ パフォーマンスに影響します。

    TiDB v8.2.0以降、並列ソートをサポートし、ソートパフォーマンスを大幅に向上させます。この機能は手動での設定を必要としません。TiDBは、システム変数[`tidb_executor_concurrency`](/system-variables.md#tidb_executor_concurrency-new-in-v50)の値に基づいて、並列ソートを使用するかどうかを自動的に判断します。

    詳細については[ドキュメント](/system-variables.md#tidb_executor_concurrency-new-in-v50)参照してください。

-   TiDB の並列 HashAgg アルゴリズムは、ディスク スピル (GA) [＃35637](https://github.com/pingcap/tidb/issues/35637) @ [xzhangxian1008](https://github.com/xzhangxian1008)をサポートします。

    TiDB v8.0.0では、ディスクスピルをサポートする並列HashAggアルゴリズムが実験的機能として導入されました。v8.2.0では、この機能が一般提供（GA）されます。並列HashAggアルゴリズムを使用すると、TiDBはメモリ使用量に基づいて自動的にデータスピルをトリガーし、クエリパフォーマンスとデータスループットのバランスをとります。この機能はデフォルトで有効になっています。この機能を制御するシステム変数`tidb_enable_parallel_hashagg_spill` 、将来のリリースで廃止される予定です。

    詳細については[ドキュメント](/system-variables.md#tidb_enable_parallel_hashagg_spill-new-in-v800)参照してください。

### 信頼性 {#reliability}

-   統計読み込み効率を最大10倍向上[＃52831](https://github.com/pingcap/tidb/issues/52831) @ [ホーキングレイ](https://github.com/hawkingrei)

    SaaSまたはPaaSアプリケーションは多数のデータテーブルを持つ場合があり、初期統計の読み込み速度が低下するだけでなく、高負荷時の負荷同期の失敗率も高まります。TiDBの起動時間や実行計画の精度にも影響が出る可能性があります。v8.2.0では、TiDBは同時実行モデルやメモリ割り当てなど、複数の観点から統計の読み込みプロセスを最適化し、レイテンシーを削減し、スループットを向上させ、ビジネスのスケーリングに影響を与える統計の読み込み速度の低下を回避します。

    適応型同時ロードがサポートされました。デフォルトでは、設定項目[`stats-load-concurrency`](/tidb-configuration-file.md#stats-load-concurrency-new-in-v540)は`0`に設定されており、統計情報のロードの同時実行数はハードウェア仕様に基づいて自動的に選択されます。

    詳細については[ドキュメント](/tidb-configuration-file.md#stats-load-concurrency-new-in-v540)参照してください。

### 可用性 {#availability}

-   TiProxyは複数の負荷分散ポリシー[＃465](https://github.com/pingcap/tiproxy/issues/465) @ [djshow832](https://github.com/djshow832) @ [xhebox](https://github.com/xhebox)をサポートします

    TiProxyは、TiDBの公式プロキシコンポーネントであり、クライアントとTiDBサーバーの間に配置されます。TiDBの負荷分散機能と接続持続関数を提供します。v8.2.0より前のバージョンでは、TiProxyのデフォルトはv1.0.0で、TiDBサーバーのステータスベースおよび接続数ベースの負荷分散ポリシーのみをサポートします。

    v8.2.0以降、TiProxyのデフォルトはv1.1.0となり、複数の負荷分散ポリシーが導入されます。ステータスベースおよび接続数ベースのポリシーに加え、TiProxyはヘルス、メモリ、CPU、ロケーションに基づいた動的な負荷分散をサポートし、TiDBクラスタの安定性を向上させます。

    [`policy`](/tiproxy/tiproxy-configuration.md#policy)構成項目を通じて、負荷分散ポリシーの組み合わせと優先順位を設定できます。

    -   `resource` : リソース優先度ポリシーは、ステータス、ヘルス、メモリ、CPU、場所、接続数の優先順位に基づいて負荷分散を実行します。
    -   `location` : 場所の優先順位ポリシーは、ステータス、場所、正常性、メモリ、CPU、接続数の優先順位に基づいて負荷分散を実行します。
    -   `connection` : 最小接続数優先ポリシーは、ステータスと接続数の優先順位に基づいて負荷分散を実行します。

    詳細については[ドキュメント](/tiproxy/tiproxy-load-balance.md)参照してください。

### SQL {#sql}

-   TiDBはJSONスキーマ検証機能[＃52779](https://github.com/pingcap/tidb/issues/52779) @ [ドヴェーデン](https://github.com/dveeden)をサポートしています

    v8.2.0より前では、JSONデータの検証には外部ツールやカスタマイズされた検証ロジックに頼る必要があり、開発と保守の複雑さが増し、開発効率が低下していました。v8.2.0以降では、 `JSON_SCHEMA_VALID()`関数が導入されました。5制約に`JSON_SCHEMA_VALID()`使用することで`CHECK`データを追加した後にチェックするのではなく、不適合なデータが挿入されるのを防ぐことができます。この機能により、TiDB内でJSONデータの妥当性を直接検証できるため、データの整合性と一貫性が向上し、開発効率が向上します。

    詳細については[ドキュメント](/functions-and-operators/json-functions.md#validation-functions)参照してください。

### DB操作 {#db-operations}

-   TiUPはPDマイクロサービス[＃5766](https://github.com/tikv/pd/issues/5766) @ [rleungx](https://github.com/rleungx)の導入をサポート

    v8.0.0以降、PDはマイクロサービスモードをサポートします。このモードでは、PDのタイムスタンプ割り当て機能とクラスタスケジューリング関数が、独立してデプロイ可能な個別のマイクロサービスに分割されます。これにより、リソース制御と分離性が向上し、異なるサービス間の影響が軽減されます。v8.2.0より前では、PDマイクロサービスはTiDB Operatorを使用してのみデプロイできます。

    v8.2.0以降、PDマイクロサービスもTiUPを使用してデプロイできるようになりました。1 `tso`マイクロサービスと`scheduling`マイクロサービスをクラスター内に個別にデプロイすることで、PDパフォーマンスのスケーラビリティを向上させ、大規模クラスターにおけるPDパフォーマンスのボトルネックを解消できます。PDがスケールアップでは解決できない重大なパフォーマンスボトルネックになっている場合は、このモードの使用をお勧めします。

    詳細については[ユーザードキュメント](/pd-microservices.md)参照してください。

-   スイッチングリソースグループ[＃53440](https://github.com/pingcap/tidb/issues/53440) @ [栄光](https://github.com/glorv)の権限制御を追加

    TiDBでは、 [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md)コマンドまたは[`RESOURCE_GROUP()`](/optimizer-hints.md#resource_groupresource_group_name)ヒントを使用して他のリソースグループに切り替えることができますが、一部のデータベースユーザーによるリソースグループの不正使用につながる可能性があります。TiDB v8.2.0では、リソースグループの切り替えに関する権限制御が導入されました。5または`RESOURCE_GROUP_USER` `RESOURCE_GROUP_ADMIN`権限を付与されたデータベースユーザーのみが他のリソースグループに切り替えることができるため、システムリソースの保護が強化されます。

    互換性を維持するため、以前のバージョンからv8.2.0以降のバージョンにアップグレードした場合でも、元の動作は保持されます。拡張権限制御を有効にするには、新しい変数[`tidb_resource_control_strict_mode`](/system-variables.md#tidb_resource_control_strict_mode-new-in-v820)を`ON`に設定してください。

    詳細については[ユーザードキュメント](/tidb-resource-control-ru-groups.md#bind-resource-groups)参照してください。

### 可観測性 {#observability}

-   実行プランがキャッシュされない理由を記録する[＃50618](https://github.com/pingcap/tidb/issues/50618) @ [qw4990](https://github.com/qw4990)

    シナリオによっては、実行オーバーヘッドを削減し、レイテンシーを削減するために、ほとんどの実行プランをキャッシュしたい場合があります。現在、実行プランのキャッシュにはSQLに対する制限があります。一部のSQL文の実行プランはキャッシュできません。キャッシュできないSQL文とその理由を特定するのは困難です。

    そのため、v8.2.0 以降では、実行プランをキャッシュできない理由を説明する新しい列`PLAN_CACHE_UNQUALIFIED`と`PLAN_CACHE_UNQUALIFIED_LAST_REASON`システム テーブル[`STATEMENTS_SUMMARY`](/statement-summary-tables.md)に追加され、パフォーマンスの調整に役立ちます。

    詳細については[ドキュメント](/statement-summary-tables.md#fields-description)参照してください。

### Security {#security}

-   TiFlashログ感度補正を[＃8977](https://github.com/pingcap/tiflash/issues/8977) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)に強化

    TiDB v8.0.0 ではログの感度低下機能が強化され、TiDB ログ内のユーザーデータをマーカー`‹ ›`で囲むかどうかを制御できるようになりました。マーカーで囲まれたログに基づいて、ログを表示する際にマーカー情報を編集するかどうかを決定できるため、ログの感度低下の柔軟性が向上します。v8.2.0 では、 TiFlash にログの感度低下に関する同様の機能強化が導入されています。この機能を使用するには、 TiFlash設定項目`security.redact_info_log` `marker`に設定してください。

    詳細については[ドキュメント](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)参照してください。

### データ移行 {#data-migration}

-   複数の変更フィードにわたって TiCDC 同期ポイントを[＃11212](https://github.com/pingcap/tiflow/issues/11212) @ [ホンユニャン](https://github.com/hongyunyan)に揃える

    v8.2.0より前は、複数の変更フィード間でTiCDC同期ポイントを整合させる`startTs`が困難でした。変更フィードを作成する際に、他の変更フィードの同期ポイントと整合するように、変更フィードの同期ポイントを慎重に選択する必要がありました。v8.2.0以降では、変更フィードの同期ポイントは、変更フィードの`sync-point-interval`の構成の倍数として作成されます。この変更により、同じ`sync-point-interval`構成を持つ複数の変更フィード間で同期ポイントを整合できるようになり、複数の下流クラスターの整合が簡素化および改善されます。

    詳細については[ドキュメント](/ticdc/ticdc-upstream-downstream-check.md#notes)参照してください。

-   TiCDC Pulsar Sinkは、 `pulsar+http`と`pulsar+https`接続プロトコル[＃11336](https://github.com/pingcap/tiflow/issues/11336) @ [サンディープ・パディ](https://github.com/SandeepPadhi)の使用をサポートしています。

    v8.2.0より前では、TiCDC Pulsar Sinkは`pulsar`と`pulsar+ssl`接続プロトコルのみをサポートしていました。v8.2.0以降、TiCDC Pulsar Sinkは`pulsar+http`と`pulsar+https`接続プロトコルもサポートします。この機能強化により、Pulsarへの接続の柔軟性が向上します。

    詳細については[ドキュメント](/ticdc/ticdc-sink-to-pulsar.md#sink-uri)参照してください。

## 互換性の変更 {#compatibility-changes}

> **注記：**
>
> このセクションでは、v8.1.0から最新バージョン（v8.2.0）にアップグレードする際に知っておくべき互換性の変更点について説明します。v8.0.0以前のバージョンから最新バージョンにアップグレードする場合は、中間バージョンで導入された互換性の変更点も確認する必要があるかもしれません。

### 行動の変化 {#behavior-changes}

-   TiDB Lightningを使用してCSVファイルをインポートする際、並列性とインポートパフォーマンスを向上させるために大きなCSVファイルを複数の小さなCSVファイルに分割するために`strict-format = true`設定する場合は、明示的に`terminator`を指定する必要があります。値は`\r` 、または`\r\n` `\n`かです。行末文字を指定しないと、CSVファイルデータの解析時に例外が発生する可能性があります[＃37338](https://github.com/pingcap/tidb/issues/37338) @ [ランス6716](https://github.com/lance6716)

-   [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)使用してCSVファイルをインポートする際、 `SPLIT_FILE`パラメータを指定して大きなCSVファイルを複数の小さなCSVファイルに分割し、同時実行性とインポートパフォーマンスを向上させる場合は、行末文字`LINES_TERMINATED_BY`を明示的に指定する必要があります。値は`\r` 、 `\n` 、または`\r\n`です。行末文字を指定しないと、CSVファイルデータの解析時に例外が発生する可能性があります[＃37338](https://github.com/pingcap/tidb/issues/37338) @ [ランス6716](https://github.com/lance6716)

-   BR v8.2.0より前のバージョンでは、TiCDCレプリケーションタスクを含むクラスターで[BRデータの復元](/br/backup-and-restore-overview.md)実行することはサポートされていませんでした。v8.2.0以降、 BRはTiCDCのデータ復元に関する制限を緩和しました。復元対象データのBackupTS（バックアップ時刻）がchangefeed [`CheckpointTS`](/ticdc/ticdc-classic-architecture.md#checkpointts) （現在のレプリケーションの進行状況を示すタイムスタンプ）よりも前であれば、 BRは通常通りデータ復元を続行できます。5は通常`BackupTS`よりもずっと早いため、ほとんどのシナリオにおいて、 BRはTiCDCレプリケーションタスクを含むクラスターのデータ復元をサポートしていると推測できます[＃53131](https://github.com/pingcap/tidb/issues/53131) @ [ユジュンセン](https://github.com/YuJuncen)

### MySQLの互換性 {#mysql-compatibility}

-   v8.2.0より前では、 `PASSWORD REQUIRE CURRENT DEFAULT`オプションを指定して[`CREATE USER`](/sql-statements/sql-statement-create-user.md)ステートメントを実行すると、このオプションはサポートされておらず解析できないためエラーが返されます。v8.2.0以降、TiDBはMySQLとの互換性のため、このオプションの解析と無視をサポートします[＃53305](https://github.com/pingcap/tidb/issues/53305) @ [ドヴェーデン](https://github.com/dveeden)

### システム変数 {#system-variables}

| 変数名                                                                                                                 | タイプを変更   | 説明                                                                                                                                                                                              |
| ------------------------------------------------------------------------------------------------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`tidb_analyze_distsql_scan_concurrency`](/system-variables.md#tidb_analyze_distsql_scan_concurrency-new-in-v760)   | 修正済み     | 最小値を`1`から`0`に変更します。 `0`に設定すると、TiDB はクラスターのサイズに基づいて、 `ANALYZE`操作を実行する際に`scan`操作の同時実行性を適応的に調整します。                                                                                                 |
| [`tidb_analyze_skip_column_types`](/system-variables.md#tidb_analyze_skip_column_types-new-in-v720)                 | 修正済み     | v8.2.0 以降、TiDB は潜在的な OOM リスクを回避するために、デフォルトで`MEDIUMTEXT`および`LONGTEXT`型の列を収集しません。                                                                                                                 |
| [`tidb_auto_analyze_partition_batch_size`](/system-variables.md#tidb_auto_analyze_partition_batch_size-new-in-v640) | 修正済み     | 自動統計収集がTiDBクラスタのパフォーマンスに与える影響を軽減するため、デフォルト値を`128`から`8192`に変更します。値の範囲を`[1, 1024]`から`[1, 8192]`に変更します。                                                                                            |
| [`tidb_enable_historical_stats`](/system-variables.md#tidb_enable_historical_stats)                                 | 修正済み     | デフォルト値を`ON`から`OFF`に変更します。これにより、潜在的な安定性の問題を回避するために履歴統計がオフになります。                                                                                                                                  |
| [`tidb_executor_concurrency`](/system-variables.md#tidb_executor_concurrency-new-in-v50)                            | 修正済み     | `sort`演算子の同時実行性を設定するためのサポートが追加されました。                                                                                                                                                            |
| [`tidb_sysproc_scan_concurrency`](/system-variables.md#tidb_sysproc_scan_concurrency-new-in-v650)                   | 修正済み     | 最小値を`1`から`0`に変更します。 `0`に設定すると、TiDBはクラスタサイズに基づいて、内部SQL文の実行時に実行される`scan`操作の同時実行性を適応的に調整します。                                                                                                       |
| [`tidb_resource_control_strict_mode`](/system-variables.md#tidb_resource_control_strict_mode-new-in-v820)           | 新しく追加された | [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md)ステートメントと[`RESOURCE_GROUP()`](/optimizer-hints.md#resource_groupresource_group_name)オプティマイザ ヒントに権限制御が適用されるかどうかを制御します。 |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーションパラメータ                                                                                              | タイプを変更 | 説明                                                                                                                                                                                               |
| -------------- | ------------------------------------------------------------------------------------------------------------ | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| ティドブ           | [`concurrently-init-stats`](/tidb-configuration-file.md#concurrently-init-stats-new-in-v810-and-v752)        | 修正済み   | 統計情報の初期化にかかる時間を短縮するため、デフォルト値を`false`から`true`に変更します。この設定項目は、 [`lite-init-stats`](/tidb-configuration-file.md#lite-init-stats-new-in-v710) `false`に設定されている場合にのみ有効になります。                            |
| ティドブ           | [`stats-load-concurrency`](/tidb-configuration-file.md#stats-load-concurrency-new-in-v540)                   | 修正済み   | デフォルト値を`5`から`0`に、最小値を`1`から`0`に変更します。値`0`は自動モードを意味し、サーバーの設定に基づいて同時実行性を自動的に調整します。                                                                                                                  |
| ティドブ           | [`token-limit`](/tidb-configuration-file.md#token-limit)                                                     | 修正済み   | 最大値を`18446744073709551615` （64ビットプラットフォーム）および`4294967295` （32ビットプラットフォーム）から`1048576`に変更しました。これは、設定値が大きすぎる場合にTiDBサーバーのOOM（オーバーヘッドオーバー）が発生するのを防ぐためです。つまり、同時にリクエストを実行できるセッション数は最大`1048576`まで設定できます。 |
| TiKV           | [`max-apply-unpersisted-log-limit`](/tikv-configuration-file.md#max-apply-unpersisted-log-limit-new-in-v810) | 修正済み   | TiKVノードのI/Oジッターによって発生するロングテールレイテンシーを削減するため、デフォルト値を`0`から`1024`に変更します。つまり、コミット済みだが永続化されていないRaftログの最大適用数は、デフォルトで`1024`になります。                                                                        |
| TiKV           | [`server.grpc-compression-type`](/tikv-configuration-file.md#grpc-compression-type)                          | 修正済み   | この設定項目は、TiKVからTiDBに送信される応答メッセージの圧縮アルゴリズムも制御するようになりました。圧縮を有効にすると、CPUリソースの消費量が増加する可能性があります。                                                                                                        |
| TiFlash        | [`security.redact_info_log`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)               | 修正済み   | 新しい値オプション`marker`が導入されました。値を`marker`に設定すると、ログ内のすべてのユーザーデータが`‹ ›`で囲まれます。                                                                                                                          |

### システムテーブル {#system-tables}

-   [`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md)と[`INFORMATION_SCHEMA.CLUSTER_PROCESSLIST`](/information-schema/information-schema-processlist.md#cluster_processlist)システム テーブルには、現在のセッションのエイリアスを表示するための`SESSION_ALIAS`フィールドが追加されます[＃46889](https://github.com/pingcap/tidb/issues/46889) @ [lcwangchao](https://github.com/lcwangchao)

### コンパイラのバージョン {#compiler-versions}

-   TiFlash開発エクスペリエンスの向上のため、TiDBのコンパイルとビルドに必要なLLVMの最小バージョンが13.0から17.0にアップグレードされました。TiDB開発者の方は、スムーズなビルドを実現するためにLLVMコンパイラのバージョンをアップグレードする必要があります[＃7193](https://github.com/pingcap/tiflash/issues/7193) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)

## 非推奨の機能 {#deprecated-features}

-   以下の機能は、v8.2.0 以降では非推奨となります。

    -   バージョン8.2.0以降、 [`enable-replica-selector-v2`](/tidb-configuration-file.md#enable-replica-selector-v2-new-in-v800)設定項目は非推奨となりました。TiKVへのRPCリクエストの送信時には、新しいバージョンのリージョンレプリカセレクターがデフォルトで使用されます。
    -   バージョン8.2.0以降、 BRスナップショット復元パラメータ`--concurrency`は非推奨となりました。代わりに、スナップショット復元時にTiKVノードごとに同時実行タスクの最大数を[`--tikv-max-restore-concurrency`](/br/use-br-command-line-tool.md#common-options)に設定できます。
    -   v8.2.0 以降、 BRスナップショット復元パラメータ`--granularity`は非推奨となり、 [粗粒度リージョン散乱アルゴリズム](/br/br-snapshot-guide.md#restore-cluster-snapshots)がデフォルトで有効になります。

-   以下の機能は将来のバージョンで廃止される予定です。

    -   TiDB v8.0.0では、自動統計収集タスクの順序を最適化するために優先キューを有効にするかどうかを制御するシステム変数[`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-new-in-v800)が導入されました。将来のバージョンでは、自動統計収集タスクの順序付けは優先キューのみとなり、システム変数[`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-new-in-v800)は廃止される予定です。
    -   TiDB v8.0.0では、並列HashAggアルゴリズムのディスクスピルをサポートするかどうかを制御するシステム変数[`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-new-in-v800)が導入されました。将来のバージョンでは、システム変数[`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-new-in-v800)は非推奨になります。
    -   v7.5.0では、TiDBがパーティション統計を非同期にマージしてOOM問題を回避するためのシステム変数[`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-new-in-v750)導入されました。将来のバージョンでは、パーティション統計はデフォルトで非同期にマージされるようになり、システム変数[`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-new-in-v750)は廃止される予定です。
    -   以降のリリースでは[実行計画バインディングの自動進化](/sql-plan-management.md#baseline-evolution)再設計する予定であり、関連する変数と動作が変更されます。
    -   TiDB Lightningパラメータ[`conflict.max-record-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)は将来のリリースで廃止される予定であり、その後削除されます。このパラメータは[`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)に置き換えられます。これは、競合レコードの最大数が、単一のインポートタスクで許容される競合レコードの最大数と一致することを意味します。

-   以下の機能は将来のバージョンで削除される予定です。

    -   TiDB Lightning v8.0.0以降、物理インポートモードの[競合検出の古いバージョン](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#the-old-version-of-conflict-detection-deprecated-in-v800)戦略は非推奨となり、 [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)番目のパラメータを使用して論理インポートモードと物理インポートモードの両方の競合検出戦略を制御できるようになりました。旧バージョンの競合検出用の[`duplicate-resolution`](/tidb-lightning/tidb-lightning-configuration.md)のパラメータは、将来のリリースで削除される予定です。

## 改善点 {#improvements}

-   ティドブ

    -   [論理DDL文（一般DDL）](/ddl-introduction.md#types-of-ddl-statements)の並列実行をサポートします。v8.1.0と比較して、10セッションを使用して異なるDDL文を同時に送信する場合、パフォーマンスは3～6倍向上します[＃53246](https://github.com/pingcap/tidb/issues/53246) @ [D3ハンター](https://github.com/D3Hunter)
    -   `((a = 1 and b = 2 and c > 3) or (a = 4 and b = 5 and c > 6)) and d > 3`ような式を使用して複数列のインデックスを一致させるロジックを改善し、より正確な`Range` [＃41598](https://github.com/pingcap/tidb/issues/41598) @ [ガザルファミリーUSA](https://github.com/ghazalfamilyusa)を生成します。
    -   大容量データを持つテーブルに対して単純なクエリを実行する際に、データ分布情報を取得するパフォーマンスを最適化します[＃53850](https://github.com/pingcap/tidb/issues/53850) @ [あなた06](https://github.com/you06)
    -   集約された結果セットはIndexJoinの内部テーブルとして使用することができ、より複雑なクエリをIndexJoinに一致させることが可能となり、インデックス[＃37068](https://github.com/pingcap/tidb/issues/37068) @ [エルサ0520](https://github.com/elsa0520)を通じてクエリの効率が向上します。
    -   TiFlash配置ルールを一括削除することで、パーティションテーブル[＃54068](https://github.com/pingcap/tidb/issues/54068) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)で`TRUNCATE`または`DROP`操作を実行した後のデータGCの処理速度が向上します。
    -   Azure Identity Libraries と Microsoft Authentication Library のバージョンをアップグレードしてセキュリティを強化する[＃53990](https://github.com/pingcap/tidb/issues/53990) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   最大値を`token-limit`から`1048576`に設定して、設定値が大きすぎる場合に TiDB サーバーの OOM が発生しないようにします[＃53312](https://github.com/pingcap/tidb/issues/53312) @ [djshow832](https://github.com/djshow832)
    -   MPP 実行プランの列プルーニングを改善して、 TiFlash MPP 実行パフォーマンスを向上します[＃52133](https://github.com/pingcap/tidb/issues/52133) @ [yibin87](https://github.com/yibin87)
    -   大量のデータ（1024行以上）を持つテーブルを検索する際の`IndexLookUp`演算子のパフォーマンスオーバーヘッドを最適化します[＃53871](https://github.com/pingcap/tidb/issues/53871) @ [crazycs520](https://github.com/crazycs520)
    -   MPP ロード バランシング[＃52313](https://github.com/pingcap/tidb/issues/52313) @ [xzhangxian1008](https://github.com/xzhangxian1008)中にリージョンのないストアを削除する

-   TiKV

    -   **圧縮ジョブサイズ（ファイル）**メトリックを追加して、1回の圧縮ジョブに含まれるSSTファイルの数を表示します[＃16837](https://github.com/tikv/tikv/issues/16837) @ [張金鵬87](https://github.com/zhangjinpeng87)
    -   [早期申請](/tikv-configuration-file.md#max-apply-unpersisted-log-limit-new-in-v810)機能をデフォルトで有効にします。この機能を有効にすると、 Raftリーダーは、クォーラムピアがログを永続化した後、リーダー自身がログを永続化するのを待たずにログを適用できるため、一部のTiKVノードにおけるジッターが書き込みリクエストのレイテンシー[＃16717](https://github.com/tikv/tikv/issues/16717) @ [栄光](https://github.com/glorv)に与える影響を軽減できます。
    -   **Raftのドロップされたメッセージ**の観測性を改善し、書き込み速度が遅い原因を特定します[＃17093](https://github.com/tikv/tikv/issues/17093) @ [コナー1996](https://github.com/Connor1996)
    -   クラスタのレイテンシー問題をトラブルシューティングするために、取り込みファイルのレイテンシーの観測性を向上させる[＃17078](https://github.com/tikv/tikv/issues/17078) @ [LykxSassinator](https://github.com/LykxSassinator)
    -   重要なRaft の読み取りと書き込みのレイテンシーを安定させるために、別のスレッドを使用してリージョンのレプリカをクリーンアップします[＃16001](https://github.com/tikv/tikv/issues/16001) @ [ヒビシェン](https://github.com/hbisheng)
    -   適用されるスナップショットの数の観測性を向上させる[＃17078](https://github.com/tikv/tikv/issues/17078) @ [ヒビシェン](https://github.com/hbisheng)

-   PD

    -   リージョンハートビート処理のパフォーマンスを向上[＃7897](https://github.com/tikv/pd/issues/7897) @ [ノルーシュ](https://github.com/nolouch) @ [rleungx](https://github.com/rleungx) @ [Jmポテト](https://github.com/JmPotato)
    -   pd-ctlは、バイトまたはクエリ次元[＃7369](https://github.com/tikv/pd/issues/7369) @ [lhy1024](https://github.com/lhy1024)によるホットリージョンのクエリをサポートします。

-   TiFlash

    -   同時実行性の高いデータ読み取り操作におけるロック競合を減らし、短いクエリのパフォーマンスを最適化します[＃9125](https://github.com/pingcap/tiflash/issues/9125) @ [ジンヘリン](https://github.com/JinheLin)
    -   `Join`演算子[＃9057](https://github.com/pingcap/tiflash/issues/9057) @ [ゲンリキ](https://github.com/gengliqi)の結合キーの冗長コピーを排除する
    -   `HashAgg`演算子[＃8956](https://github.com/pingcap/tiflash/issues/8956) @ [ゲンリキ](https://github.com/gengliqi)で2レベルハッシュテーブルを変換する処理を同時に実行する
    -   `HashAgg`演算子の冗長な集計関数を削除して計算オーバーヘッドを削減する[＃8891](https://github.com/pingcap/tiflash/issues/8891) @ [グオシャオゲ](https://github.com/guo-shaoge)

-   ツール

    -   バックアップと復元 (BR)

        -   バックアップ機能を最適化し、ノードの再起動、クラスターのスケールアウト、および多数のテーブル[＃52534](https://github.com/pingcap/tidb/issues/52534) @ [3ポイントシュート](https://github.com/3pointer)をバックアップする際のネットワーク ジッター中のバックアップ パフォーマンスと安定性を改善します。
        -   データ復元時にTiCDCの変更フィードをきめ細かくチェックします。変更フィード[`CheckpointTS`](/ticdc/ticdc-classic-architecture.md#checkpointts)データバックアップ時刻より遅い場合、復元操作は影響を受けません。これにより、不要な待機時間が削減され、ユーザーエクスペリエンスが向上します[＃53131](https://github.com/pingcap/tidb/issues/53131) @ [ユジュンセン](https://github.com/YuJuncen)
        -   [`BACKUP`](/sql-statements/sql-statement-backup.md)ステートメントと[`RESTORE`](/sql-statements/sql-statement-restore.md)ステートメントに、 `CHECKSUM_CONCURRENCY` [＃53040](https://github.com/pingcap/tidb/issues/53040) @ [リドリスR](https://github.com/RidRisR)などのよく使用されるパラメータをいくつか追加します。
        -   `br log restore`サブコマンドを除き、他の`br log`サブコマンドはすべて、メモリ消費量を削減するために TiDB `domain`データ構造のロードをスキップすることをサポートしています[＃52088](https://github.com/pingcap/tidb/issues/52088) @ [リーヴルス](https://github.com/Leavrth)
        -   ログバックアップ中に生成される一時ファイルの暗号化をサポート[＃15083](https://github.com/tikv/tikv/issues/15083) @ [ユジュンセン](https://github.com/YuJuncen)
        -   Grafanaダッシュボードに`tikv_log_backup_pending_initial_scan`監視メトリックを追加する[＃16656](https://github.com/tikv/tikv/issues/16656) @ [3ポイントシュート](https://github.com/3pointer)
        -   PITRログの出力形式を最適化し、ログに`RestoreTS`フィールドを追加します[＃53645](https://github.com/pingcap/tidb/issues/53645) @ [ドヴェーデン](https://github.com/dveeden)

    -   TiCDC

        -   ダウンストリームがメッセージキュー（MQ）またはクラウドstorageの場合、生のイベントを直接出力することをサポート[＃11211](https://github.com/pingcap/tiflow/issues/11211) @ [チャールズ・チャン96](https://github.com/CharlesCheung96)

## バグ修正 {#bug-fixes}

-   ティドブ

    -   SQL文に外部結合が含まれており、結合条件に`false IN (column_name)`式が含まれている場合、クエリ結果にデータ[＃49476](https://github.com/pingcap/tidb/issues/49476) @ [ガザルファミリーUSA](https://github.com/ghazalfamilyusa)が欠落する問題を修正しました。
    -   TiDB がテーブル[＃53403](https://github.com/pingcap/tidb/issues/53403) @ [ハイ・ラスティン](https://github.com/Rustin170506)の統計を`PREDICATE COLUMNS`収集するときに、システム テーブルの列の統計が収集される問題を修正しました。
    -   `tidb_persist_analyze_options`システム変数が`OFF` [＃53478](https://github.com/pingcap/tidb/issues/53478) @ [ハイ・ラスティン](https://github.com/Rustin170506)に設定されている場合に`tidb_enable_column_tracking`システム変数が有効にならない問題を修正しました
    -   `(*PointGetPlan).StatsInfo()` [＃49803](https://github.com/pingcap/tidb/issues/49803) [＃43339](https://github.com/pingcap/tidb/issues/43339) @ [qw4990](https://github.com/qw4990)の実行中に発生する可能性のあるデータ競合の問題を修正しました
    -   データ変更操作[＃53951](https://github.com/pingcap/tidb/issues/53951) @ [qw4990](https://github.com/qw4990)を含むトランザクションで仮想列を持つテーブルをクエリすると、TiDB が誤ったクエリ結果を返す可能性がある問題を修正しました
    -   自動統計収集中にシステム変数`tidb_enable_async_merge_global_stats`と`tidb_analyze_partition_concurrency`有効にならない問題を修正[＃53972](https://github.com/pingcap/tidb/issues/53972) @ [ハイ・ラスティン](https://github.com/Rustin170506)
    -   `TABLESAMPLE` [＃54015](https://github.com/pingcap/tidb/issues/54015) @ [接線](https://github.com/tangenta)をクエリしたときに TiDB が`plan not supported`エラーを返す可能性がある問題を修正しました
    -   `SELECT DISTINCT CAST(col AS DECIMAL), CAST(col AS SIGNED) FROM ...`クエリを実行すると誤った結果が返される可能性がある問題を修正[＃53726](https://github.com/pingcap/tidb/issues/53726) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   クライアント側でデータ読み取りタイムアウト後にクエリを終了できない問題を修正[＃44009](https://github.com/pingcap/tidb/issues/44009) @ [wshwsh12](https://github.com/wshwsh12)
    -   述語[＃45783](https://github.com/pingcap/tidb/issues/45783) @ [ホーキングレイ](https://github.com/hawkingrei)の`Longlong`型のオーバーフローの問題を修正
    -   関連するサブクエリがある場合にウィンドウ関数がpanic可能性がある問題を修正[＃42734](https://github.com/pingcap/tidb/issues/42734) @ [ハイ・ラスティン](https://github.com/Rustin170506)
    -   TopN演算子が誤って[＃37986](https://github.com/pingcap/tidb/issues/37986) @ [qw4990](https://github.com/qw4990)にプッシュダウンされる可能性がある問題を修正しました
    -   クラスター化インデックスを述語として使用すると`SELECT INTO OUTFILE`機能しない問題を修正[＃42093](https://github.com/pingcap/tidb/issues/42093) @ [qw4990](https://github.com/qw4990)
    -   情報スキーマキャッシュミス[＃53428](https://github.com/pingcap/tidb/issues/53428) @ [crazycs520](https://github.com/crazycs520)により、古い読み取りのクエリレイテンシーが増加する問題を修正しました。
    -   `YEAR`型の列を範囲外の符号なし整数と比較すると誤った結果が発生する問題を修正[＃50235](https://github.com/pingcap/tidb/issues/50235) @ [qw4990](https://github.com/qw4990)
    -   TiDB [＃37548](https://github.com/pingcap/tidb/issues/37548) @ [ホーキングレイ](https://github.com/hawkingrei)を再起動した後、主キー列統計のヒストグラムと TopN がロードされない問題を修正しました
    -   大規模並列処理 (MPP) [＃51362](https://github.com/pingcap/tidb/issues/51362) @ [アイリンキッド](https://github.com/AilinKid)で`final` AggMode と`non-final` AggMode が共存できない問題を修正しました
    -   常に`true` [＃46962](https://github.com/pingcap/tidb/issues/46962) @ [エルサ0520](https://github.com/elsa0520)となる述語を持つ`SHOW ERRORS`ステートメントを実行すると TiDB がパニックを起こす問題を修正しました。
    -   再帰CTE [＃49721](https://github.com/pingcap/tidb/issues/49721) @ [ホーキングレイ](https://github.com/hawkingrei)でビューの使用が機能しない問題を修正
    -   起動時に統計情報をロードするときに、TiDB が GC によるエラーを報告する可能性がある問題を修正[＃53592](https://github.com/pingcap/tidb/issues/53592) @ [あなた06](https://github.com/you06)
    -   `?`の引数を含む`CONV`の式を持つ`PREPARE` `EXECUTE`ステートメントを複数回実行すると、誤ったクエリ結果が返される可能性がある問題を修正しました[＃53505](https://github.com/pingcap/tidb/issues/53505) @ [qw4990](https://github.com/qw4990)
    -   BIGINT 以外の符号なし整数が文字列/小数点[＃41736](https://github.com/pingcap/tidb/issues/41736) @ [リトルフォール](https://github.com/LittleFall)と比較されたときに誤った結果を生成する可能性がある問題を修正しました
    -   外部キー[＃53652](https://github.com/pingcap/tidb/issues/53652) @ [ホーキングレイ](https://github.com/hawkingrei)を持つテーブルを作成するときに、TiDBが対応する統計メタデータ（ `stats_meta` ）を作成しない問題を修正しました。
    -   クエリ内の特定のフィルタ条件により、プランナーモジュールが`invalid memory address or nil pointer dereference`エラー[＃53582](https://github.com/pingcap/tidb/issues/53582) [＃53580](https://github.com/pingcap/tidb/issues/53580) [＃53594](https://github.com/pingcap/tidb/issues/53594) [＃53603](https://github.com/pingcap/tidb/issues/53603) @ [ヤンケオ](https://github.com/YangKeao)を報告する可能性がある問題を修正しました
    -   `CREATE OR REPLACE VIEW`同時に実行すると`table doesn't exist`エラー[＃53673](https://github.com/pingcap/tidb/issues/53673) @ [接線](https://github.com/tangenta)が発生する可能性がある問題を修正
    -   `STATE`フィールドのうち`size`が定義されていないため、 `INFORMATION_SCHEMA.TIDB_TRX`テーブルの`STATE`フィールドが空になる問題を修正しました[＃53026](https://github.com/pingcap/tidb/issues/53026) @ [cfzjywxk](https://github.com/cfzjywxk)
    -   `tidb_enable_async_merge_global_stats`無効になっている場合、グローバル統計の`Distinct_count`情報が正しくない可能性がある問題を修正しました[＃53752](https://github.com/pingcap/tidb/issues/53752) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   オプティマイザーヒント[＃53767](https://github.com/pingcap/tidb/issues/53767) @ [ホーキングレイ](https://github.com/hawkingrei)使用時に誤った警告情報が表示される問題を修正しました
    -   時間型を否定すると誤った値[＃52262](https://github.com/pingcap/tidb/issues/52262) @ [ソロツグ](https://github.com/solotzg)が返される問題を修正しました
    -   `REGEXP()`空のパターン引数[＃53221](https://github.com/pingcap/tidb/issues/53221) @ [yibin87](https://github.com/yibin87)に対して明示的にエラーを報告しない問題を修正しました
    -   JSON を datetime に変換すると精度が失われる場合がある問題を修正[＃53352](https://github.com/pingcap/tidb/issues/53352) @ [ヤンケオ](https://github.com/YangKeao)
    -   `JSON_QUOTE()`場合によっては誤った結果を返す問題を修正[＃37294](https://github.com/pingcap/tidb/issues/37294) @ [ドヴェーデン](https://github.com/dveeden)
    -   `ALTER TABLE ... REMOVE PARTITIONING`実行すると[＃53385](https://github.com/pingcap/tidb/issues/53385) @ [ミョンス](https://github.com/mjonss)でデータが失われる可能性がある問題を修正
    -   `auth_socket`認証プラグイン[＃54031](https://github.com/pingcap/tidb/issues/54031) @ [lcwangchao](https://github.com/lcwangchao)を使用しているときに、TiDB が認証されていないユーザーの接続を拒否できないことがある問題を修正しました。
    -   JSON関連の関数がMySQLと矛盾するエラーを返す場合がある問題を修正[＃53799](https://github.com/pingcap/tidb/issues/53799) @ [ドヴェーデン](https://github.com/dveeden)
    -   `INFORMATION_SCHEMA.PARTITIONS`のパーティションテーブルの`INDEX_LENGTH`フィールドが正しくない[＃54173](https://github.com/pingcap/tidb/issues/54173) @ [定義2014](https://github.com/Defined2014)という問題を修正しました
    -   `INFORMATION_SCHEMA.TABLES`テーブルの`TIDB_ROW_ID_SHARDING_INFO`フィールドが正しくない[＃52330](https://github.com/pingcap/tidb/issues/52330) @ [接線](https://github.com/tangenta)という問題を修正しました
    -   生成された列が無効なタイムスタンプ[＃52509](https://github.com/pingcap/tidb/issues/52509) @ [lcwangchao](https://github.com/lcwangchao)を返す問題を修正しました
    -   分散実行フレームワーク (DXF) [＃53281](https://github.com/pingcap/tidb/issues/53281) @ [ジムララ](https://github.com/zimulala)を使用してインデックスを追加するときに設定`max-index-length`で TiDB がpanicになる問題を修正しました
    -   場合によっては無効な列タイプ`DECIMAL(0,0)`が作成される可能性がある問題を修正[＃53779](https://github.com/pingcap/tidb/issues/53779) @ [接線](https://github.com/tangenta)
    -   列のデフォルト値として`CURRENT_DATE()`使用すると、クエリ結果[＃53746](https://github.com/pingcap/tidb/issues/53746) @ [接線](https://github.com/tangenta)が正しくなくなる問題を修正しました
    -   `ALTER DATABASE ... SET TIFLASH REPLICA`文が誤ってTiFlashレプリカを`SEQUENCE`テーブル[＃51990](https://github.com/pingcap/tidb/issues/51990) @ [ジフハスト](https://github.com/jiyfhust)に追加する問題を修正しました。
    -   `INFORMATION_SCHEMA.KEY_COLUMN_USAGE`テーブルの`REFERENCED_TABLE_SCHEMA`フィールドが正しくない[＃52350](https://github.com/pingcap/tidb/issues/52350) @ [wd0517](https://github.com/wd0517)という問題を修正しました
    -   1つのステートメントに複数の行を挿入すると、 `AUTO_ID_CACHE=1` [＃52465](https://github.com/pingcap/tidb/issues/52465) @ [天菜麻緒](https://github.com/tiancaiamao)のときに`AUTO_INCREMENT`列目が不連続になる問題を修正しました。
    -   非推奨警告[＃52515](https://github.com/pingcap/tidb/issues/52515) @ [ドヴェーデン](https://github.com/dveeden)の形式を修正
    -   `copr.buildCopTasks` [＃53085](https://github.com/pingcap/tidb/issues/53085) @ [時間と運命](https://github.com/time-and-fate)で`TRACE`コマンドが欠落している問題を修正しました
    -   `memory_quota`ヒントがサブクエリ[＃53834](https://github.com/pingcap/tidb/issues/53834) @ [qw4990](https://github.com/qw4990)で機能しない可能性がある問題を修正しました
    -   特定の状況下でプランキャッシュを使用する際に、メタデータロックの不適切な使用によって異常なデータが書き込まれる可能性がある問題を修正しました[＃53634](https://github.com/pingcap/tidb/issues/53634) @ [ジムララ](https://github.com/zimulala)
    -   トランザクション内のステートメントが OOM によって強制終了された後、TiDB が同じトランザクション内で次のステートメントの実行を継続すると、エラー`Trying to start aggressive locking while it's already started`が発生し、panic[＃53540](https://github.com/pingcap/tidb/issues/53540) @ [ミョンケミンタ](https://github.com/MyonKeminta)が発生する可能性がある問題を修正しました。

-   TiKV

    -   `JSON_ARRAY_APPEND()`関数を TiKV にプッシュダウンすると TiKV が[＃16930](https://github.com/tikv/tikv/issues/16930) @ [dbsid](https://github.com/dbsid)でpanicになる問題を修正しました
    -   リーダーが失敗したスナップショットファイルを時間[＃16976](https://github.com/tikv/tikv/issues/16976) @ [ヒビシェン](https://github.com/hbisheng)でクリーンアップしない問題を修正しました
    -   同時実行性の高いコプロセッサー要求により TiKV OOM [＃16653](https://github.com/tikv/tikv/issues/16653) @ [金星の上](https://github.com/overvenus)が発生する可能性がある問題を修正しました
    -   `raftstore.periodic-full-compact-start-times`構成項目をオンラインで変更すると、TiKVがpanicを起こす可能性がある問題を修正しました[＃17066](https://github.com/tikv/tikv/issues/17066) @ [スペードA-タン](https://github.com/SpadeA-Tang)
    -   `make docker`と`make docker_test`の失敗を修正[＃17075](https://github.com/tikv/tikv/issues/17075) @ [藤田俊希](https://github.com/shunki-fujita)
    -   **gRPC リクエスト ソースの継続時間**メトリックが監視ダッシュボード[＃17133](https://github.com/tikv/tikv/issues/17133) @ [キング・ディラン](https://github.com/King-Dylan)に誤って表示される問題を修正しました
    -   gRPC メッセージ圧縮方式を`grpc-compression-type`で設定しても、TiKV から TiDB [＃17176](https://github.com/tikv/tikv/issues/17176) @ [エキシウム](https://github.com/ekexium)に送信されるメッセージには反映されない問題を修正しました。
    -   tikv-ctlの`raft region`コマンドの出力にリージョンステータス情報[＃17037](https://github.com/tikv/tikv/issues/17037) @ [栄光](https://github.com/glorv)が含まれていない問題を修正しました
    -   CDC とログバックアップが`advance-ts-interval`構成を使用して`check_leader`のタイムアウトを制限しないため、TiKV が正常に再起動したときに`resolved_ts`遅延が大きくなる場合がある問題を修正しました[＃17107](https://github.com/tikv/tikv/issues/17107) @ [ミョンケミンタ](https://github.com/MyonKeminta)

-   PD

    -   `ALTER PLACEMENT POLICY`配置ポリシー[＃52257](https://github.com/pingcap/tidb/issues/52257) [＃51712](https://github.com/pingcap/tidb/issues/51712) @ [ジフハスト](https://github.com/jiyfhust)を変更できない問題を修正
    -   書き込みホットスポットのスケジュール設定により配置ポリシーの制約が破られる可能性がある問題を修正[＃7848](https://github.com/tikv/pd/issues/7848) @ [lhy1024](https://github.com/lhy1024)
    -   配置ルール[＃7808](https://github.com/tikv/pd/issues/7808) @ [rleungx](https://github.com/rleungx)を使用しているときに、ダウンしたピアが回復しない可能性がある問題を修正しました。
    -   リソースグループクエリ[＃8217](https://github.com/tikv/pd/issues/8217) @ [ノルーシュ](https://github.com/nolouch)をキャンセルするときに再試行回数が多すぎる問題を修正
    -   PDリーダーを手動で転送すると[＃8225](https://github.com/tikv/pd/issues/8225) @ [HuSharp](https://github.com/HuSharp)失敗する可能性がある問題を修正しました

-   TiFlash

    -   空のパーティション[＃9024](https://github.com/pingcap/tiflash/issues/9024) @ [ジンヘリン](https://github.com/JinheLin)を含むパーティション テーブルでクエリを実行するときに発生するクエリ タイムアウトの問題を修正しました。
    -   分散storageおよびコンピューティングアーキテクチャで、DDL操作[＃9084](https://github.com/pingcap/tiflash/issues/9084) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)で非NULL列を追加した後にクエリでNULL値が誤って返される可能性がある問題を修正しました。
    -   `SUBSTRING_INDEX()`関数が一部のコーナーケースでTiFlash のクラッシュを引き起こす可能性がある問題を修正[＃9116](https://github.com/pingcap/tiflash/issues/9116) @ [wshwsh12](https://github.com/wshwsh12)
    -   BRまたはTiDB Lightning [＃9118](https://github.com/pingcap/tiflash/issues/9118) @ [ジンヘリン](https://github.com/JinheLin)経由でデータをインポートした後、FastScanモードで多数の重複行が読み取られる可能性がある問題を修正しました。

-   ツール

    -   バックアップと復元 (BR)

        -   空の`EndKey` [＃52574](https://github.com/pingcap/tidb/issues/52574) @ [3ポイントシュート](https://github.com/3pointer)が原因でBR がトランザクション KV クラスターの復元に失敗する問題を修正しました
        -   PD接続障害により、ログバックアップアドバンサ所有者が配置されているTiDBインスタンスがpanic[＃52597](https://github.com/pingcap/tidb/issues/52597) @ [ユジュンセン](https://github.com/YuJuncen)になる可能性がある問題を修正しました。
        -   アドバンサーオーナーの移行[＃53561](https://github.com/pingcap/tidb/issues/53561) @ [リドリスR](https://github.com/RidRisR)後にログバックアップが一時停止される可能性がある問題を修正しました
        -   復元プロセス中に複数のネストされた再試行によりBR がエラーを正しく識別できない問題を修正[＃54053](https://github.com/pingcap/tidb/issues/54053) @ [リドリスR](https://github.com/RidRisR)
        -   TiKV 構成を取得するために使用される接続が閉じられない可能性がある問題を修正[＃52595](https://github.com/pingcap/tidb/issues/52595) @ [リドリスR](https://github.com/RidRisR)
        -   `TestStoreRemoved`テストケースが不安定になる問題を修正[＃52791](https://github.com/pingcap/tidb/issues/52791) @ [ユジュンセン](https://github.com/YuJuncen)
        -   ポイントインタイムリカバリ（PITR） [＃52628](https://github.com/pingcap/tidb/issues/52628) @ [リドリスR](https://github.com/RidRisR)中にTiFlashがクラッシュする問題を修正
        -   増分バックアップ[＃54139](https://github.com/pingcap/tidb/issues/54139) @ [3ポイントシュート](https://github.com/3pointer)中の DDL ジョブのスキャンの非効率性の問題を修正
        -   リージョンリーダー[＃17168](https://github.com/tikv/tikv/issues/17168) @ [リーヴルス](https://github.com/Leavrth)の探索の中断により、チェックポイントバックアップ中のバックアップパフォーマンスが影響を受ける問題を修正しました。

    -   TiCDC

        -   Grafana [＃10777](https://github.com/pingcap/tiflow/issues/10777) @ [アズドンメン](https://github.com/asddongmen)の**Kafka 送信バイト**パネルの表示が不正確になる問題を修正
        -   マルチノード環境で大量の`UPDATE`操作を実行する際にChangefeedを繰り返し再起動するとデータの不整合が発生する可能性がある問題を修正[＃11219](https://github.com/pingcap/tiflow/issues/11219) @ [リデズ](https://github.com/lidezhu)

    -   TiDB データ移行 (DM)

        -   `go-mysql` [＃11041](https://github.com/pingcap/tiflow/issues/11041) @ [D3ハンター](https://github.com/D3Hunter)にアップグレードして接続ブロックの問題を修正しました
        -   MariaDBデータの移行中に`SET`ステートメントがDMpanicを引き起こす問題を修正[＃10206](https://github.com/pingcap/tiflow/issues/10206) @ [ドヴェーデン](https://github.com/dveeden)

    -   TiDB Lightning

        -   TiDB Lightningがzstd圧縮ファイルをインポートする際にエラーを報告する可能性がある問題を修正[＃53587](https://github.com/pingcap/tidb/issues/53587) @ [ランス6716](https://github.com/lance6716)

    -   Dumpling

        -   テーブルとビューを同時にエクスポートするとDumpling がエラーを報告する問題を修正[＃53682](https://github.com/pingcap/tidb/issues/53682) @ [接線](https://github.com/tangenta)

    -   TiDBBinlog

        -   TiDB Binlogが有効な場合、 `ADD COLUMN`の実行中に行を削除するとエラー`data and columnID count not match`が報告される可能性がある問題を修正しました[＃53133](https://github.com/pingcap/tidb/issues/53133) @ [接線](https://github.com/tangenta)

## 寄稿者 {#contributors}

TiDB コミュニティの以下の貢献者に感謝いたします。

-   [キャビンフィーバーB](https://github.com/CabinfeverB)
-   [ダン・ロシニョ](https://github.com/DanRoscigno) (初回投稿者)
-   [杉本英](https://github.com/ei-sugimoto) (初回投稿者)
-   [エルトシア](https://github.com/eltociear)
-   [ジフハスト](https://github.com/jiyfhust)
-   [マイケル・ムデン](https://github.com/michaelmdeng) (初回投稿者)
-   [ミッタルリシャブ](https://github.com/mittalrishabh)
-   [猫のみ](https://github.com/onlyacat)
-   [qichengzx](https://github.com/qichengzx) (初回投稿者)
-   [シーライズ](https://github.com/SeaRise)
-   [ショーン0915](https://github.com/shawn0915)
-   [藤田俊希](https://github.com/shunki-fujita) (初回投稿者)
-   [トニーシュキ](https://github.com/tonyxuqqi)
-   [わーい](https://github.com/wwu) (初回投稿者)
-   [yzhan1](https://github.com/yzhan1)
