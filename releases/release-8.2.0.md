---
title: TiDB 8.2.0 Release Notes
summary: TiDB 8.2.0 の新機能、互換性の変更、改善、バグ修正について説明します。
---

# TiDB 8.2.0 リリースノート {#tidb-8-2-0-release-notes}

発売日: 2024年7月11日

TiDB バージョン: 8.2.0

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v8.2/quick-start-with-tidb)

8.2.0 では、次の主要な機能と改善が導入されています。

<table><thead><tr><th>カテゴリ</th><th>機能/拡張機能</th><th>説明</th></tr></thead><tbody><tr><td rowspan="3">信頼性と可用性</td><td><a href="https://docs.pingcap.com/tidb/v8.2/tiproxy-load-balance">TiProxyは複数の負荷分散ポリシーをサポート</a></td><td>TiDB v8.2.0 では、TiProxy はステータス、接続数、健全性、メモリ、CPU、場所などのさまざまな次元に基づいて TiDB ノードを評価し、ランク付けします。 <code>policy</code>構成項目で指定された負荷分散ポリシーに従って、TiProxy はデータベース操作を実行する最適な TiDB ノードを動的に選択します。これにより、全体的なリソース使用が最適化され、クラスターのパフォーマンスが向上し、スループットが向上します。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v8.2/system-variables#tidb_enable_parallel_hashagg_spill-new-in-v800">TiDB の並列 HashAgg アルゴリズムはディスク スピル (GA) をサポートします</a></td><td>HashAgg は、同じフィールド値を持つ行を効率的に集計するために TiDB で広く使用されている集計演算子です。TiDB v8.0.0 では、処理速度をさらに向上させるための実験的機能として並列 HashAgg が導入されています。メモリリソースが不足している場合、並列 HashAgg は一時的にソートされたデータをディスクに書き出し、過剰なメモリ使用によって発生する潜在的な OOM リスクを回避します。これにより、ノードの安定性を維持しながらクエリ パフォーマンスが向上します。v8.2.0 では、この機能が一般提供 (GA) され、デフォルトで有効になっているため、 <code>tidb_executor_concurrency</code>を使用して並列 HashAgg の同時実行を安全に構成できます。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v8.2/tidb-configuration-file#stats-load-concurrency-new-in-v540">統計読み込み効率を最大10倍向上</a></td><td>SaaS や PaaS サービスなど、多数のテーブルとパーティションを持つクラスターの場合、統計の読み込み効率を向上させることで、TiDB インスタンスの起動が遅い問題を解決し、統計の動的読み込みの成功率を高めることができます。この改善により、統計の読み込みの失敗によるパフォーマンスのロールバックが削減され、クラスターの安定性が向上します。</td></tr><tr><td rowspan="1"> DB 操作と可観測性</td><td><a href="https://docs.pingcap.com/tidb/v8.2/tidb-resource-control#bind-resource-groups">切り替えリソースグループの権限制御を導入する</a></td><td>リソース制御が広く使用されているため、リソース グループの切り替えの権限制御により、データベース ユーザーによるリソースの悪用を防ぎ、管理者の全体的なリソース使用の保護を強化し、クラスターの安定性を向上させることができます。</td></tr></tbody></table>

## 機能の詳細 {#feature-details}

### パフォーマンス {#performance}

-   次の JSON関数を TiKV [＃50601](https://github.com/pingcap/tidb/issues/50601) @ [dbsid](https://github.com/dbsid)にプッシュダウンすることをサポートします。

    -   `JSON_ARRAY_APPEND()`
    -   `JSON_MERGE_PATCH()`
    -   `JSON_REPLACE()`

    詳細については[ドキュメント](/functions-and-operators/expressions-pushed-down.md)参照してください。

-   TiDBは並列ソートをサポート[＃49217](https://github.com/pingcap/tidb/issues/49217) [＃50746](https://github.com/pingcap/tidb/issues/50746) @ [翻訳者](https://github.com/xzhangxian1008)

    v8.2.0 より前のバージョンでは、TiDB は Sort 演算子を順番にのみ実行するため、大量のデータをソートする場合のクエリ パフォーマンスに影響します。

    v8.2.0 以降、TiDB は並列ソートをサポートしており、ソートのパフォーマンスが大幅に向上しています。この機能は手動で構成する必要はありません。TiDB は、 [`tidb_executor_concurrency`](/system-variables.md#tidb_executor_concurrency-new-in-v50)システム変数の値に基づいて、並列ソートを使用するかどうかを自動的に決定します。

    詳細については[ドキュメント](/system-variables.md#tidb_executor_concurrency-new-in-v50)参照してください。

-   TiDB の並列 HashAgg アルゴリズムは、ディスク スピル (GA) [＃35637](https://github.com/pingcap/tidb/issues/35637) @ [翻訳者](https://github.com/xzhangxian1008)をサポートします。

    TiDB v8.0.0 では、ディスク スピルをサポートする並列 HashAgg アルゴリズムが実験的機能として導入されています。v8.2.0 では、この機能が一般提供 (GA) されます。並列 HashAgg アルゴリズムを使用すると、TiDB はメモリ使用量に基づいてデータ スピルを自動的にトリガーし、クエリ パフォーマンスとデータ スループットのバランスをとります。この機能はデフォルトで有効になっています。この機能を制御するシステム変数`tidb_enable_parallel_hashagg_spill`は、将来のリリースで廃止される予定です。

    詳細については[ドキュメント](/system-variables.md#tidb_enable_parallel_hashagg_spill-new-in-v800)参照してください。

### 信頼性 {#reliability}

-   統計読み込み効率を最大10倍向上[＃52831](https://github.com/pingcap/tidb/issues/52831) @ [ホーキングレイ](https://github.com/hawkingrei)

    SaaS または PaaS アプリケーションには多数のデータ テーブルが存在する可能性があり、これにより初期統計の読み込み速度が遅くなるだけでなく、高負荷時の負荷同期の失敗率も増加します。TiDB の起動時間と実行プランの精度が影響を受ける可能性があります。v8.2.0 では、TiDB は同時実行モデルやメモリ割り当てなどの複数の観点から統計の読み込みプロセスを最適化し、レイテンシーを削減し、スループットを向上させ、ビジネスのスケーリングに影響する統計の読み込み速度の低下を回避します。

    適応型同時ロードがサポートされるようになりました。デフォルトでは、構成項目[`stats-load-concurrency`](/tidb-configuration-file.md#stats-load-concurrency-new-in-v540)は`0`に設定され、統計ロードの同時実行性はハードウェア仕様に基づいて自動的に選択されます。

    詳細については[ドキュメント](/tidb-configuration-file.md#stats-load-concurrency-new-in-v540)参照してください。

### 可用性 {#availability}

-   TiProxyは複数の負荷分散ポリシーをサポートします[＃465](https://github.com/pingcap/tiproxy/issues/465) @ [翻訳者](https://github.com/djshow832) @ [xhebox](https://github.com/xhebox)

    TiProxy は、クライアントと TiDBサーバーの間にある、TiDB の公式プロキシコンポーネントです。TiDB の負荷分散機能と接続永続化関数を提供します。v8.2.0 より前のバージョンでは、TiProxy のデフォルトは v1.0.0 で、TiDB サーバーに対してステータスベースおよび接続数ベースの負荷分散ポリシーのみがサポートされます。

    v8.2.0 以降、TiProxy はデフォルトで v1.1.0 に設定され、複数の負荷分散ポリシーが導入されています。ステータスベースおよび接続数ベースのポリシーに加えて、TiProxy はヘルス、メモリ、CPU、および場所に基づく動的な負荷分散をサポートし、TiDB クラスターの安定性を向上させます。

    [`policy`](/tiproxy/tiproxy-configuration.md#policy)構成項目を通じて、負荷分散ポリシーの組み合わせと優先順位を設定できます。

    -   `resource` : リソース優先度ポリシーは、ステータス、ヘルス、メモリ、CPU、場所、接続数の優先順位に基づいて負荷分散を実行します。
    -   `location` : 場所の優先順位ポリシーは、ステータス、場所、健全性、メモリ、CPU、接続数の優先順位に基づいて負荷分散を実行します。
    -   `connection` : 最小接続数優先ポリシーは、ステータスと接続数の優先順位に基づいて負荷分散を実行します。

    詳細については[ドキュメント](/tiproxy/tiproxy-load-balance.md)参照してください。

### 構文 {#sql}

-   TiDBはJSONスキーマ検証機能[＃52779](https://github.com/pingcap/tidb/issues/52779) @ [ドヴェーデン](https://github.com/dveeden)をサポートしています

    v8.2.0 より前では、JSON データの検証には外部ツールやカスタマイズされた検証ロジックに頼る必要があり、開発と保守の複雑さが増し、開発効率が低下していました。v8.2.0 からは、 `JSON_SCHEMA_VALID()`機能が導入されました`CHECK`制約で`JSON_SCHEMA_VALID()`使用すると、データを追加した後にチェックするのではなく、不適合なデータが挿入されるのを防ぐことができます。この機能を使用すると、TiDB で直接 JSON データの有効性を検証できるため、データの整合性と一貫性が向上し、開発効率が向上します。

    詳細については[ドキュメント](/functions-and-operators/json-functions.md#validation-functions)参照してください。

### DB操作 {#db-operations}

-   TiUPはPDマイクロサービス[＃5766](https://github.com/tikv/pd/issues/5766) @ [rleungx](https://github.com/rleungx)の導入をサポートします

    v8.0.0 以降、PD はマイクロサービス モードをサポートします。このモードでは、PD のタイムスタンプ割り当て機能とクラスター スケジューリング関数が、独立してデプロイできる個別のマイクロサービスに分割されるため、リソースの制御と分離が向上し、異なるサービス間の影響が軽減されます。v8.2.0 より前では、PD マイクロサービスはTiDB Operator を使用してのみデプロイできます。

    v8.2.0 以降では、PD マイクロサービスもTiUP を使用してデプロイできます。1 `tso`サービスと`scheduling`マイクロサービスをクラスターに個別にデプロイして、PD パフォーマンスのスケーラビリティを強化し、大規模クラスターの PD パフォーマンスのボトルネックに対処することができます。PD がスケールアップでは解決できない重大なパフォーマンスのボトルネックになった場合は、このモードを使用することをお勧めします。

    詳細については[ユーザードキュメント](/pd-microservices.md)参照してください。

-   切り替えリソースグループ[＃53440](https://github.com/pingcap/tidb/issues/53440) @ [栄光](https://github.com/glorv)の権限制御を追加

    TiDB では、ユーザーは[`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md)コマンドまたは[`RESOURCE_GROUP()`](/optimizer-hints.md#resource_groupresource_group_name)ヒントを使用して他のリソース グループに切り替えることができますが、これにより、一部のデータベース ユーザーによるリソース グループの悪用が発生する可能性があります。TiDB v8.2.0 では、リソース グループの切り替えの権限制御が導入されています。5 または`RESOURCE_GROUP_ADMIN` `RESOURCE_GROUP_USER`動的権限が付与されたデータベース ユーザーのみが他のリソース グループに切り替えることができるため、システム リソースの保護が強化されます。

    互換性を維持するために、以前のバージョンから v8.2.0 以降のバージョンにアップグレードする場合、元の動作が保持されます。拡張された権限制御を有効にするには、新しい変数[`tidb_resource_control_strict_mode`](/system-variables.md#tidb_resource_control_strict_mode-new-in-v820)を`ON`に設定します。

    詳細については[ユーザードキュメント](/tidb-resource-control.md#bind-resource-groups)参照してください。

### 可観測性 {#observability}

-   実行プランがキャッシュされない理由を記録する[＃50618](https://github.com/pingcap/tidb/issues/50618) @ [qw4990](https://github.com/qw4990)

    シナリオによっては、実行オーバーヘッドを節約し、レイテンシーを減らすために、ほとんどの実行プランをキャッシュする必要がある場合があります。現在、実行プランのキャッシュには SQL に対するいくつかの制限があります。一部の SQL ステートメントの実行プランはキャッシュできません。キャッシュできない SQL ステートメントとその理由を特定することは困難です。

    そのため、v8.2.0 以降では、実行プランをキャッシュできない理由を説明する新しい列`PLAN_CACHE_UNQUALIFIED`と`PLAN_CACHE_UNQUALIFIED_LAST_REASON`システム テーブル[`STATEMENTS_SUMMARY`](/statement-summary-tables.md)に追加され、パフォーマンスの調整に役立ちます。

    詳細については[ドキュメント](/statement-summary-tables.md#fields-description)参照してください。

### Security {#security}

-   TiFlashログ感度低下を強化[＃8977](https://github.com/pingcap/tiflash/issues/8977) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)

    TiDB v8.0.0 では、ログの感度低下機能が強化され、TiDB ログ内のユーザー データがマーカー`‹ ›`で囲まれるかどうかを制御できるようになりました。マークされたログに基づいて、ログを表示するときにマークされた情報を編集するかどうかを決定できるため、ログの感度低下の柔軟性が向上します。v8.2.0 では、 TiFlashでログの感度低下に同様の機能強化が導入されています。この機能を使用するには、 TiFlash構成項目`security.redact_info_log`を`marker`に設定します。

    詳細については[ドキュメント](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)参照してください。

### データ移行 {#data-migration}

-   複数の変更フィードにわたって TiCDC 同期ポイントを[＃11212](https://github.com/pingcap/tiflow/issues/11212) @ [ホンユンヤン](https://github.com/hongyunyan)揃える

    v8.2.0 より前では、複数の変更フィード間で TiCDC 同期ポイントを揃えることは困難でした。変更フィードの作成時に、他の変更フィードの同期ポイントと揃うように、変更フィードの`startTs`を慎重に選択する必要がありました。v8.2.0 以降では、変更フィードの同期ポイントは、変更フィードの`sync-point-interval`構成の倍数として作成されます。この変更により、同じ`sync-point-interval`構成を持つ複数の変更フィード間で同期ポイントを揃えることができるようになり、複数のダウンストリーム クラスターを揃える機能が簡素化および向上します。

    詳細については[ドキュメント](/ticdc/ticdc-upstream-downstream-check.md#notes)参照してください。

-   TiCDC Pulsar Sinkは、 `pulsar+http`と`pulsar+https`接続プロトコル[＃11336](https://github.com/pingcap/tiflow/issues/11336) @ [サンディープ・パディ](https://github.com/SandeepPadhi)の使用をサポートしています。

    v8.2.0 より前では、TiCDC Pulsar Sink は`pulsar`と`pulsar+ssl`接続プロトコルのみをサポートしています。v8.2.0 以降では、TiCDC Pulsar Sink は`pulsar+http`と`pulsar+https`接続プロトコルもサポートしています。この機能強化により、Pulsar への接続の柔軟性が向上します。

    詳細については[ドキュメント](/ticdc/ticdc-sink-to-pulsar.md#sink-uri)参照してください。

## 互換性の変更 {#compatibility-changes}

> **注記：**
>
> このセクションでは、v8.1.0 から現在のバージョン (v8.2.0) にアップグレードするときに知っておく必要のある互換性の変更について説明します。v8.0.0 以前のバージョンから現在のバージョンにアップグレードする場合は、中間バージョンで導入された互換性の変更も確認する必要がある可能性があります。

### 行動の変化 {#behavior-changes}

-   TiDB Lightning を使用して CSV ファイルをインポートする場合、同時実行性とインポート パフォーマンスを向上させるために`strict-format = true` [＃37338](https://github.com/pingcap/tidb/issues/37338)して大きな CSV ファイルを複数の小さな CSV ファイルに分割する場合は、 `terminator`明示的に指定する必要があります。値は`\r` 、 `\n` 、または`\r\n`です。行末文字を指定しないと、CSV ファイル データを解析するときに例外が発生する可能性があります。11 @ [ランス6716](https://github.com/lance6716)

-   [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)使用して CSV ファイルをインポートする場合、同時実行性とインポート パフォーマンスを向上させるために`SPLIT_FILE`パラメータを指定して大きな CSV ファイルを複数の小さな CSV ファイルに分割する場合は、行末文字`LINES_TERMINATED_BY`を明示的に指定する必要があります。値[＃37338](https://github.com/pingcap/tidb/issues/37338) `\r` 、 `\n` 、または`\r\n`です。行末文字を指定しないと、CSV ファイル データを解析するときに例外が発生する可能性があります。13 @ [ランス6716](https://github.com/lance6716)

-   BR v8.2.0 より前では、TiCDC レプリケーション タスクを含むクラスターで[BRデータの復元](/br/backup-and-restore-overview.md)実行することはサポートされていません。v8.2.0 以降、 BR はTiCDC のデータ復元に関する制限を緩和します。復元するデータの BackupTS (バックアップ時間) が changefeed [`CheckpointTS`](/ticdc/ticdc-architecture.md#checkpointts) (現在のレプリケーションの進行状況を示すタイムスタンプ) よりも前であれば、 BR はデータ復元を正常に続行できます。5 `BackupTS`通常[＃53131](https://github.com/pingcap/tidb/issues/53131)もっと早いため、ほとんどのシナリオでBR はTiCDC レプリケーション タスクを含むクラスターのデータの復元をサポートしていると想定できます。7 @ [ユジュンセン](https://github.com/YuJuncen)

### MySQL 互換性 {#mysql-compatibility}

-   v8.2.0 より前では、 `PASSWORD REQUIRE CURRENT DEFAULT`オプションを指定して[`CREATE USER`](/sql-statements/sql-statement-create-user.md)ステートメントを実行すると、このオプションはサポートされておらず解析[＃53305](https://github.com/pingcap/tidb/issues/53305)ないため、エラーが返されます。v8.2.0 以降、TiDB は MySQL との互換性のためにこのオプションの解析と無視をサポートしています。5 @ [ドヴェーデン](https://github.com/dveeden)

### システム変数 {#system-variables}

| 変数名                                                                                                               | タイプを変更   | 説明                                                                                                                                                                                               |
| ----------------------------------------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [`tidb_analyze_distsql_scan_concurrency`](/system-variables.md#tidb_analyze_distsql_scan_concurrency-new-in-v760) | 修正済み     | 最小値を`1`から`0`に変更します。 `0`に設定すると、TiDB はクラスターのサイズに基づいて`ANALYZE`操作を実行するときに`scan`操作の同時実行性を適応的に調整します。                                                                                                   |
| [`tidb_analyze_skip_column_types`](/system-variables.md#tidb_analyze_skip_column_types-new-in-v720)               | 修正済み     | v8.2.0 以降、TiDB は潜在的な OOM リスクを回避するために、デフォルトでは`MEDIUMTEXT`と`LONGTEXT`型の列を収集しません。                                                                                                                   |
| [`tidb_enable_historical_stats`](/system-variables.md#tidb_enable_historical_stats)                               | 修正済み     | デフォルト値を`ON`から`OFF`に変更し、潜在的な安定性の問題を回避するために履歴統計をオフにします。                                                                                                                                            |
| [`tidb_executor_concurrency`](/system-variables.md#tidb_executor_concurrency-new-in-v50)                          | 修正済み     | `sort`演算子の同時実行性を設定するためのサポートが追加されました。                                                                                                                                                             |
| [`tidb_sysproc_scan_concurrency`](/system-variables.md#tidb_sysproc_scan_concurrency-new-in-v650)                 | 修正済み     | 最小値を`1`から`0`に変更します。 `0`に設定すると、TiDB はクラスター サイズに基づいて内部 SQL ステートメントを実行するときに実行される`scan`操作の同時実行性を適応的に調整します。                                                                                           |
| [`tidb_resource_control_strict_mode`](/system-variables.md#tidb_resource_control_strict_mode-new-in-v820)         | 新しく追加された | [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md)のステートメントと[`RESOURCE_GROUP()`](/optimizer-hints.md#resource_groupresource_group_name)オプティマイザ ヒントに権限制御が適用されるかどうかを制御します。 |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーションパラメータ                                                                                              | タイプを変更 | 説明                                                                                                                                                                                    |
| -------------- | ------------------------------------------------------------------------------------------------------------ | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ティビ            | [`stats-load-concurrency`](/tidb-configuration-file.md#stats-load-concurrency-new-in-v540)                   | 修正済み   | デフォルト値を`5`から`0`に、最小値を`1`から`0`に変更します。値`0`は自動モードを意味し、サーバーの構成に基づいて同時実行性を自動的に調整します。                                                                                                       |
| ティビ            | [`token-limit`](/tidb-configuration-file.md#token-limit)                                                     | 修正済み   | 最大値を`18446744073709551615` (64 ビット プラットフォーム) および`4294967295` (32 ビット プラットフォーム) から`1048576`に変更し、設定値が大きすぎる場合に TiDB サーバーの OOM が発生するのを回避します。つまり、同時にリクエストを実行できるセッションの数は最大`1048576`に設定できます。 |
| ティクヴ           | [`max-apply-unpersisted-log-limit`](/tikv-configuration-file.md#max-apply-unpersisted-log-limit-new-in-v810) | 修正済み   | デフォルト値を`0`から`1024`に変更して、TiKV ノードの I/O ジッターによって発生するロングテールレイテンシーを削減します。つまり、コミットされているが永続化されていないRaftログの適用可能な最大数は、デフォルトで`1024`なります。                                                        |
| ティクヴ           | [`server.grpc-compression-type`](/tikv-configuration-file.md#grpc-compression-type)                          | 修正済み   | この構成項目は、TiKV から TiDB に送信される応答メッセージの圧縮アルゴリズムも制御するようになりました。圧縮を有効にすると、CPU リソースの消費量が増える可能性があります。                                                                                          |
| TiFlash        | [`security.redact_info_log`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)               | 修正済み   | 新しい値オプション`marker`が導入されました。値を`marker`に設定すると、ログ内のすべてのユーザー データが`‹ ›`でラップされます。                                                                                                            |

### システムテーブル {#system-tables}

-   [`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md)および[`INFORMATION_SCHEMA.CLUSTER_PROCESSLIST`](/information-schema/information-schema-processlist.md#cluster_processlist)システム テーブルには、現在のセッションのエイリアスを表示する`SESSION_ALIAS`フィールドが追加されています[＃46889](https://github.com/pingcap/tidb/issues/46889) @ [lcwangchao](https://github.com/lcwangchao)

### コンパイラのバージョン {#compiler-versions}

-   TiFlash開発エクスペリエンスを向上させるために、TiDB のコンパイルとビルドに必要な LLVM の最小バージョンが 13.0 から 17.0 にアップグレードされました。TiDB 開発者の場合は、スムーズなビルドを確実に行うために LLVM コンパイラのバージョンをアップグレードする必要があります[＃7193](https://github.com/pingcap/tiflash/issues/7193) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)

## 廃止された機能 {#deprecated-features}

-   以下の機能は、v8.2.0 以降では非推奨となります。

    -   v8.2.0 以降、 [`enable-replica-selector-v2`](/tidb-configuration-file.md#enable-replica-selector-v2-new-in-v800)構成項目は非推奨になりました。TiKV に RPC 要求を送信するときは、新しいバージョンのリージョンレプリカ セレクターがデフォルトで使用されます。
    -   v8.2.0 以降、 BRスナップショット復元パラメータ`--concurrency`は非推奨になりました。代わりに、 [`--tikv-max-restore-concurrency`](/br/use-br-command-line-tool.md#common-options)使用して、スナップショット復元中に TiKV ノードごとに同時実行タスクの最大数を設定できます。
    -   v8.2.0 以降では、 BRスナップショット復元パラメータ`--granularity`非推奨となり、 [粗粒度リージョン分散アルゴリズム](/br/br-snapshot-guide.md#restore-cluster-snapshots)デフォルトで有効になります。

-   以下の機能は将来のバージョンで廃止される予定です。

    -   v8.0.0 では、TiDB は、自動統計収集タスクの順序を最適化するために優先キューを有効にするかどうかを制御する[`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-new-in-v800)システム変数を導入しました。将来のバージョンでは、優先キューが自動統計収集タスクを順序付ける唯一の方法となり、 [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-new-in-v800)システム変数は廃止される予定です。
    -   v8.0.0 では、TiDB は、同時 HashAgg アルゴリズムのディスク スピルをサポートするかどうかを制御する[`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-new-in-v800)システム変数を導入します。将来のバージョンでは、 [`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-new-in-v800)システム変数は非推奨になります。
    -   v7.5.0 では、TiDB は[`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-new-in-v750)システム変数を導入し、TiDB がパーティション統計を非同期にマージして OOM の問題を回避できるようにします。将来のバージョンでは、パーティション統計はデフォルトで非同期にマージされ、 [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-new-in-v750)システム変数は非推奨になります。
    -   以降のリリースでは[実行計画バインディングの自動進化](/sql-plan-management.md#baseline-evolution)再設計する予定であり、関連する変数と動作が変更されます。
    -   TiDB Lightningパラメータ[`conflict.max-record-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)は、将来のリリースで廃止される予定であり、その後削除されます。このパラメータは[`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)に置き換えられます。これは、競合するレコードの最大数が、単一のインポート タスクで許容できる競合するレコードの最大数と一致することを意味します。

-   以下の機能は将来のバージョンで削除される予定です:

    -   v8.0.0 以降、 TiDB Lightning物理インポート モードの[競合検出の旧バージョン](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#the-old-version-of-conflict-detection-deprecated-in-v800)戦略が廃止され、 [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)パラメータを使用して論理インポート モードと物理インポート モードの両方の競合検出戦略を制御できるようになりました。競合検出の旧バージョンの[`duplicate-resolution`](/tidb-lightning/tidb-lightning-configuration.md)パラメータは、将来のリリースで削除される予定です。

## 改善点 {#improvements}

-   ティビ

    -   [論理 DDL ステートメント (一般的な DDL)](/ddl-introduction.md#types-of-ddl-statements)の並列実行をサポートします。v8.1.0と比較して、10セッションを使用して異なるDDL文を同時に送信する場合、パフォーマンスは3〜6倍向上します[＃53246](https://github.com/pingcap/tidb/issues/53246) @ [D3ハンター](https://github.com/D3Hunter)
    -   `((a = 1 and b = 2 and c > 3) or (a = 4 and b = 5 and c > 6)) and d > 3`ような式を使用して複数列のインデックスを一致させるロジックを改善し、より正確な`Range` [＃41598](https://github.com/pingcap/tidb/issues/41598) @ [ガザルファミリー](https://github.com/ghazalfamilyusa)を生成します。
    -   大量のデータを持つテーブルに対して単純なクエリを実行するときに、データ分布情報を取得するパフォーマンスを最適化します[＃53850](https://github.com/pingcap/tidb/issues/53850) @ [あなた06](https://github.com/you06)
    -   集約された結果セットはIndexJoinの内部テーブルとして使用でき、より複雑なクエリをIndexJoinに一致させることが可能になり、インデックス[＃37068](https://github.com/pingcap/tidb/issues/37068) @ [エルサ0520](https://github.com/elsa0520)を通じてクエリの効率が向上します。
    -   TiFlash配置ルールを一括削除することで、パーティションテーブル[＃54068](https://github.com/pingcap/tidb/issues/54068) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)で`TRUNCATE`または`DROP`操作を実行した後のデータGCの処理速度が向上します。
    -   Azure Identity Libraries と Microsoft Authentication Library のバージョンをアップグレードしてセキュリティを強化する[＃53990](https://github.com/pingcap/tidb/issues/53990) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   最大値を`token-limit`から`1048576`設定して、設定値が大きすぎる場合にTiDBサーバーのOOMが発生しないようにします[＃53312](https://github.com/pingcap/tidb/issues/53312) @ [翻訳者](https://github.com/djshow832)
    -   MPP 実行プランの列プルーニングを改善して、 TiFlash MPP 実行パフォーマンスを向上[＃52133](https://github.com/pingcap/tidb/issues/52133) @ [いびん87](https://github.com/yibin87)
    -   大量のデータ（&gt;1024行）を含むテーブルを検索するときの`IndexLookUp`演算子のパフォーマンスオーバーヘッドを最適化します[＃53871](https://github.com/pingcap/tidb/issues/53871) @ [クレイジーcs520](https://github.com/crazycs520)
    -   MPP ロード バランシング中にリージョンのないストアを削除する[＃52313](https://github.com/pingcap/tidb/issues/52313) @ [翻訳者](https://github.com/xzhangxian1008)

-   ティクヴ

    -   **圧縮ジョブサイズ（ファイル）**メトリックを追加して、単一の圧縮ジョブに含まれる SST ファイルの数を表示します[＃16837](https://github.com/tikv/tikv/issues/16837) @ [張金鵬87](https://github.com/zhangjinpeng87)
    -   [早期申請](/tikv-configuration-file.md#max-apply-unpersisted-log-limit-new-in-v810)機能をデフォルトで有効にします。この機能を有効にすると、 Raftリーダーは、リーダー自身がログを永続化するのを待たずに、クォーラム ピアがログを永続化した後にログを適用できるため、いくつかの TiKV ノードのジッターが書き込み要求のレイテンシー[＃16717](https://github.com/tikv/tikv/issues/16717) @ [栄光](https://github.com/glorv)に与える影響が軽減されます。
    -   **Raft のドロップされたメッセージ**の観測可能性を改善し、書き込み速度が遅い原因を特定します[＃17093](https://github.com/tikv/tikv/issues/17093) @ [コナー1996](https://github.com/Connor1996)
    -   クラスターのレイテンシーの問題をトラブルシューティングするために、取り込みファイルのレイテンシーの観測性を向上させる[＃17078](https://github.com/tikv/tikv/issues/17078) @ [リクササシネーター](https://github.com/LykxSassinator)
    -   重要なRaft の読み取りと書き込みの安定したレイテンシーを確保するために、別のスレッドを使用してリージョンのレプリカをクリーンアップします[＃16001](https://github.com/tikv/tikv/issues/16001) @ [ビシェン](https://github.com/hbisheng)
    -   適用されるスナップショットの数の観測性を向上させる[＃17078](https://github.com/tikv/tikv/issues/17078) @ [ビシェン](https://github.com/hbisheng)

-   PD

    -   リージョンハートビート処理のパフォーマンスを向上[＃7897](https://github.com/tikv/pd/issues/7897) @ [ノルーシュ](https://github.com/nolouch) @ [rleungx](https://github.com/rleungx) @ [じゃがいも](https://github.com/JmPotato)
    -   pd-ctl は、バイトまたはクエリ次元[＃7369](https://github.com/tikv/pd/issues/7369) @ [翻訳者](https://github.com/lhy1024)によるホット リージョンのクエリをサポートします。

-   TiFlash

    -   同時実行性の高いデータ読み取り操作でのロック競合を減らし、短いクエリのパフォーマンスを最適化します[＃9125](https://github.com/pingcap/tiflash/issues/9125) @ [ジンヘリン](https://github.com/JinheLin)
    -   `Join`演算子[＃9057](https://github.com/pingcap/tiflash/issues/9057) @ [ゲンリキ](https://github.com/gengliqi)の結合キーの冗長コピーを排除する
    -   `HashAgg`演算子[＃8956](https://github.com/pingcap/tiflash/issues/8956) @ [ゲンリキ](https://github.com/gengliqi)で2レベルハッシュテーブルを変換する処理を同時に実行する
    -   `HashAgg`演算子の冗長な集計関数を削除して計算オーバーヘッドを削減する[＃8891](https://github.com/pingcap/tiflash/issues/8891) @ [グオシャオゲ](https://github.com/guo-shaoge)

-   ツール

    -   バックアップと復元 (BR)

        -   バックアップ機能を最適化し、ノードの再起動、クラスターのスケールアウト、および多数のテーブルをバックアップする際のネットワークジッター中のバックアップパフォーマンスと安定性を向上させます[＃52534](https://github.com/pingcap/tidb/issues/52534) @ [3ポインター](https://github.com/3pointer)
        -   データ復元中に TiCDC の変更フィードのきめ細かなチェックを実装します。変更フィード[`CheckpointTS`](/ticdc/ticdc-architecture.md#checkpointts)データ バックアップ時間より遅い場合、復元操作は影響を受けないため、不要な待機時間が短縮され、ユーザー エクスペリエンスが向上します[＃53131](https://github.com/pingcap/tidb/issues/53131) @ [ユジュンセン](https://github.com/YuJuncen)
        -   [`BACKUP`](/sql-statements/sql-statement-backup.md)文と[`RESTORE`](/sql-statements/sql-statement-restore.md)文に、よく使われるパラメータをいくつか追加します（例： `CHECKSUM_CONCURRENCY` [＃53040](https://github.com/pingcap/tidb/issues/53040) @ [リドリス](https://github.com/RidRisR)
        -   `br log restore`サブコマンドを除き、他の`br log`サブコマンドはすべて、メモリ消費量を削減するために TiDB `domain`データ構造のロードをスキップすることをサポートしています[＃52088](https://github.com/pingcap/tidb/issues/52088) @ [リーヴルス](https://github.com/Leavrth)
        -   ログバックアップ中に生成される一時ファイルの暗号化をサポート[＃15083](https://github.com/tikv/tikv/issues/15083) @ [ユジュンセン](https://github.com/YuJuncen)
        -   Grafanaダッシュボードに`tikv_log_backup_pending_initial_scan`監視メトリックを追加する[＃16656](https://github.com/tikv/tikv/issues/16656) @ [3ポインター](https://github.com/3pointer)
        -   PITRログの出力形式を最適化し、ログに`RestoreTS`フィールドを追加します[＃53645](https://github.com/pingcap/tidb/issues/53645) @ [ドヴェーデン](https://github.com/dveeden)

    -   ティCDC

        -   ダウンストリームがメッセージキュー（MQ）またはクラウドstorageの場合、生のイベントを直接出力することをサポートします[＃11211](https://github.com/pingcap/tiflow/issues/11211) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)

## バグ修正 {#bug-fixes}

-   ティビ

    -   SQL 文に外部結合が含まれ、結合条件に`false IN (column_name)`式が含まれている場合、クエリ結果に一部のデータが欠落する問題を修正しました[＃49476](https://github.com/pingcap/tidb/issues/49476) @ [ガザルファミリー](https://github.com/ghazalfamilyusa)
    -   TiDB がテーブル[＃53403](https://github.com/pingcap/tidb/issues/53403) @ [ハイラスティン](https://github.com/Rustin170506)の統計を`PREDICATE COLUMNS`収集するときに、システム テーブルの列の統計が収集される問題を修正しました。
    -   `tidb_persist_analyze_options`システム変数が`OFF` [＃53478](https://github.com/pingcap/tidb/issues/53478) @ [ハイラスティン](https://github.com/Rustin170506)に設定されている場合に`tidb_enable_column_tracking`システム変数が有効にならない問題を修正しました
    -   `(*PointGetPlan).StatsInfo()` [＃49803](https://github.com/pingcap/tidb/issues/49803) [＃43339](https://github.com/pingcap/tidb/issues/43339) @ [qw4990](https://github.com/qw4990)の実行中に発生する可能性のあるデータ競合の問題を修正しました
    -   データ変更操作[＃53951](https://github.com/pingcap/tidb/issues/53951) @ [qw4990](https://github.com/qw4990)を含むトランザクションで仮想列を持つテーブルをクエリすると、TiDB が誤ったクエリ結果を返す可能性がある問題を修正しました。
    -   自動統計収集中にシステム変数`tidb_enable_async_merge_global_stats`と`tidb_analyze_partition_concurrency`が有効にならない問題を修正[＃53972](https://github.com/pingcap/tidb/issues/53972) @ [ハイラスティン](https://github.com/Rustin170506)
    -   `TABLESAMPLE` [＃54015](https://github.com/pingcap/tidb/issues/54015) @ [タンジェンタ](https://github.com/tangenta)をクエリしたときに TiDB が`plan not supported`エラーを返す可能性がある問題を修正しました
    -   `SELECT DISTINCT CAST(col AS DECIMAL), CAST(col AS SIGNED) FROM ...`クエリを実行すると誤った結果が返される可能性がある問題を修正[＃53726](https://github.com/pingcap/tidb/issues/53726) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   クライアント側でデータ読み取りタイムアウト後にクエリを終了できない問題を修正[＃44009](https://github.com/pingcap/tidb/issues/44009) @ [うわー](https://github.com/wshwsh12)
    -   述語[＃45783](https://github.com/pingcap/tidb/issues/45783) @ [ホーキングレイ](https://github.com/hawkingrei)の`Longlong`型のオーバーフローの問題を修正
    -   関連するサブクエリがある場合にウィンドウ関数がpanicになる可能性がある問題を修正[＃42734](https://github.com/pingcap/tidb/issues/42734) @ [ハイラスティン](https://github.com/Rustin170506)
    -   TopN演算子が誤ってプッシュダウンされる可能性がある問題を修正[＃37986](https://github.com/pingcap/tidb/issues/37986) @ [qw4990](https://github.com/qw4990)
    -   クラスター化インデックスを述語として使用すると`SELECT INTO OUTFILE`機能しない問題を修正[＃42093](https://github.com/pingcap/tidb/issues/42093) @ [qw4990](https://github.com/qw4990)
    -   情報スキーマキャッシュミス[＃53428](https://github.com/pingcap/tidb/issues/53428) @ [クレイジーcs520](https://github.com/crazycs520)により、古い読み取りのクエリレイテンシーが増加する問題を修正しました。
    -   `YEAR`型の列を範囲外の符号なし整数と比較すると誤った結果が発生する問題を修正[＃50235](https://github.com/pingcap/tidb/issues/50235) @ [qw4990](https://github.com/qw4990)
    -   TiDB [＃37548](https://github.com/pingcap/tidb/issues/37548) @ [ホーキングレイ](https://github.com/hawkingrei)を再起動した後、主キー列統計のヒストグラムと TopN がロードされない問題を修正しました。
    -   超並列処理 (MPP) [＃51362](https://github.com/pingcap/tidb/issues/51362) @ [アイリンキッド](https://github.com/AilinKid)で`final` AggMode と`non-final` AggMode が共存できない問題を修正
    -   常に`true` [＃46962](https://github.com/pingcap/tidb/issues/46962) @ [エルサ0520](https://github.com/elsa0520)の述語を持つ`SHOW ERRORS`ステートメントを実行すると TiDB がパニックになる問題を修正しました。
    -   再帰 CTE [＃49721](https://github.com/pingcap/tidb/issues/49721) @ [ホーキングレイ](https://github.com/hawkingrei)でビューの使用が機能しない問題を修正
    -   起動時に統計をロードするときに TiDB が GC によるエラーを報告する可能性がある問題を修正[＃53592](https://github.com/pingcap/tidb/issues/53592) @ [あなた06](https://github.com/you06)
    -   `?`引数を含む`CONV`の式を持つ`PREPARE` `EXECUTE`を複数回実行すると、誤ったクエリ結果が返される可能性がある問題を修正しました[＃53505](https://github.com/pingcap/tidb/issues/53505) @ [qw4990](https://github.com/qw4990)
    -   BIGINT 以外の符号なし整数を文字列/小数と比較すると誤った結果が生成される可能性がある問題を修正[＃41736](https://github.com/pingcap/tidb/issues/41736) @ [リトルフォール](https://github.com/LittleFall)
    -   外部キー[＃53652](https://github.com/pingcap/tidb/issues/53652) @ [ホーキングレイ](https://github.com/hawkingrei)を持つテーブルを作成するときに、TiDBが対応する統計メタデータ（ `stats_meta` ）を作成しない問題を修正しました
    -   クエリ内の特定のフィルター条件により、プランナーモジュールが`invalid memory address or nil pointer dereference`エラー[＃53582](https://github.com/pingcap/tidb/issues/53582) [＃53580](https://github.com/pingcap/tidb/issues/53580) [＃53594](https://github.com/pingcap/tidb/issues/53594) [＃53603](https://github.com/pingcap/tidb/issues/53603) [ヤンケオ](https://github.com/YangKeao)を報告する可能性がある問題を修正しました。
    -   `CREATE OR REPLACE VIEW`同時に実行すると`table doesn't exist`エラー[＃53673](https://github.com/pingcap/tidb/issues/53673) @ [タンジェンタ](https://github.com/tangenta)が発生する可能性がある問題を修正
    -   `STATE`フィールドのうち`size`が定義されていないため、 `INFORMATION_SCHEMA.TIDB_TRX`テーブルの`STATE`フィールドが空になる問題を修正しました[＃53026](https://github.com/pingcap/tidb/issues/53026) @ [翻訳](https://github.com/cfzjywxk)
    -   `tidb_enable_async_merge_global_stats`が無効になっている場合に、グローバル統計の`Distinct_count`情報が正しくなくなる可能性がある問題を修正[＃53752](https://github.com/pingcap/tidb/issues/53752) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   オプティマイザーヒント[＃53767](https://github.com/pingcap/tidb/issues/53767) @ [ホーキングレイ](https://github.com/hawkingrei)使用時に誤った警告情報が表示される問題を修正しました
    -   時間型を否定すると誤った値[＃52262](https://github.com/pingcap/tidb/issues/52262) @ [ソロッツ](https://github.com/solotzg)になる問題を修正しました
    -   `REGEXP()`空のパターン引数[＃53221](https://github.com/pingcap/tidb/issues/53221) @ [いびん87](https://github.com/yibin87)に対してエラーを明示的に報告しない問題を修正
    -   JSON を datetime に変換すると精度が失われる場合がある問題を修正[＃53352](https://github.com/pingcap/tidb/issues/53352) @ [ヤンケオ](https://github.com/YangKeao)
    -   `JSON_QUOTE()`場合によっては誤った結果を返す問題を修正[＃37294](https://github.com/pingcap/tidb/issues/37294) @ [ドヴェーデン](https://github.com/dveeden)
    -   `ALTER TABLE ... REMOVE PARTITIONING`実行するとデータが失われる可能性がある問題を修正[＃53385](https://github.com/pingcap/tidb/issues/53385) @ [ミョンス](https://github.com/mjonss)
    -   `auth_socket`認証プラグイン[＃54031](https://github.com/pingcap/tidb/issues/54031) @ [lcwangchao](https://github.com/lcwangchao)を使用する場合、TiDB が認証されていないユーザー接続を拒否できないことがある問題を修正しました。
    -   JSON関連の関数がMySQLと一致しないエラーを返す場合がある問題を修正[＃53799](https://github.com/pingcap/tidb/issues/53799) @ [ドヴェーデン](https://github.com/dveeden)
    -   `INFORMATION_SCHEMA.PARTITIONS`のパーティションテーブルの`INDEX_LENGTH`フィールドが正しくない[＃54173](https://github.com/pingcap/tidb/issues/54173) @ [定義2014](https://github.com/Defined2014)という問題を修正
    -   `INFORMATION_SCHEMA.TABLES`テーブルの`TIDB_ROW_ID_SHARDING_INFO`フィールドが正しくない[＃52330](https://github.com/pingcap/tidb/issues/52330) @ [タンジェンタ](https://github.com/tangenta)という問題を修正
    -   生成された列が不正なタイムスタンプ[＃52509](https://github.com/pingcap/tidb/issues/52509) @ [lcwangchao](https://github.com/lcwangchao)を返す問題を修正
    -   分散実行フレームワーク (DXF) [＃53281](https://github.com/pingcap/tidb/issues/53281) @ [ジムララ](https://github.com/zimulala)を使用してインデックスを追加するときに`max-index-length`を設定すると TiDB がpanicになる問題を修正しました。
    -   場合によっては不正な列タイプ`DECIMAL(0,0)`が作成される可能性がある問題を修正[＃53779](https://github.com/pingcap/tidb/issues/53779) @ [タンジェンタ](https://github.com/tangenta)
    -   列のデフォルト値として`CURRENT_DATE()`使用するとクエリ結果が不正確になる問題を修正[＃53746](https://github.com/pingcap/tidb/issues/53746) @ [タンジェンタ](https://github.com/tangenta)
    -   `ALTER DATABASE ... SET TIFLASH REPLICA`文が誤ってTiFlashレプリカを`SEQUENCE`テーブル[＃51990](https://github.com/pingcap/tidb/issues/51990) @ [ジフハウス](https://github.com/jiyfhust)に追加する問題を修正しました。
    -   `INFORMATION_SCHEMA.KEY_COLUMN_USAGE`テーブルの`REFERENCED_TABLE_SCHEMA`フィールドが正しくない[＃52350](https://github.com/pingcap/tidb/issues/52350) @ [0517 ...](https://github.com/wd0517)という問題を修正
    -   1つのステートメントに複数の行を挿入すると、 `AUTO_ID_CACHE=1` [＃52465](https://github.com/pingcap/tidb/issues/52465) @ [天菜まお](https://github.com/tiancaiamao)のときに`AUTO_INCREMENT`列目が不連続になる問題を修正しました。
    -   非推奨警告の形式を修正[＃52515](https://github.com/pingcap/tidb/issues/52515) @ [ドヴェーデン](https://github.com/dveeden)
    -   `copr.buildCopTasks` [＃53085](https://github.com/pingcap/tidb/issues/53085) @ [時間と運命](https://github.com/time-and-fate)で`TRACE`コマンドが欠落している問題を修正
    -   `memory_quota`ヒントがサブクエリ[＃53834](https://github.com/pingcap/tidb/issues/53834) @ [qw4990](https://github.com/qw4990)で機能しない可能性がある問題を修正しました
    -   特定の状況下でプラン キャッシュを使用する際に、メタデータ ロックを不適切に使用すると異常なデータが書き込まれる可能性がある問題を修正しました[＃53634](https://github.com/pingcap/tidb/issues/53634) @ [ジムララ](https://github.com/zimulala)
    -   トランザクション内のステートメントが OOM によって強制終了された後、TiDB が同じトランザクション内で次のステートメントの実行を継続すると、エラー`Trying to start aggressive locking while it's already started`が発生し、panic[＃53540](https://github.com/pingcap/tidb/issues/53540) @ [ミョンケミンタ](https://github.com/MyonKeminta)が発生する可能性がある問題を修正しました。

-   ティクヴ

    -   `JSON_ARRAY_APPEND()`関数を TiKV にプッシュダウンすると TiKV が[＃16930](https://github.com/tikv/tikv/issues/16930) @ [dbsid](https://github.com/dbsid)でpanicになる問題を修正しました
    -   リーダーが失敗したスナップショットファイルを時間[＃16976](https://github.com/tikv/tikv/issues/16976) @ [ビシェン](https://github.com/hbisheng)内にクリーンアップしない問題を修正しました
    -   同時実行性の高いコプロセッサー要求により TiKV OOM [＃16653](https://github.com/tikv/tikv/issues/16653) @ [金星の上](https://github.com/overvenus)が発生する可能性がある問題を修正
    -   `raftstore.periodic-full-compact-start-times`構成項目をオンラインで変更すると TiKV がpanicになる可能性がある問題を修正[＃17066](https://github.com/tikv/tikv/issues/17066) @ [スペードA-タン](https://github.com/SpadeA-Tang)
    -   `make docker`と`make docker_test`の失敗を修正[＃17075](https://github.com/tikv/tikv/issues/17075) @ [藤田俊樹](https://github.com/shunki-fujita)
    -   **gRPC リクエスト ソースの継続時間**メトリックが監視ダッシュボード[＃17133](https://github.com/tikv/tikv/issues/17133) @ [キング・ディラン](https://github.com/King-Dylan)に正しく表示されない問題を修正しました
    -   gRPC メッセージ圧縮方式を`grpc-compression-type`で設定しても、TiKV から TiDB [＃17176](https://github.com/tikv/tikv/issues/17176) @ [エキシウム](https://github.com/ekexium)に送信されるメッセージには反映されない問題を修正しました。
    -   tikv-ctlの`raft region`コマンドの出力にリージョンステータス情報[＃17037](https://github.com/tikv/tikv/issues/17037) @ [栄光](https://github.com/glorv)が含まれていない問題を修正
    -   CDC とログバックアップが`advance-ts-interval`構成を使用して`check_leader`のタイムアウトを制限しないため、TiKV が正常に再起動したときに`resolved_ts`遅延が大きくなる場合がある問題を修正しました[＃17107](https://github.com/tikv/tikv/issues/17107) @ [ミョンケミンタ](https://github.com/MyonKeminta)

-   PD

    -   `ALTER PLACEMENT POLICY`配置ポリシーを変更できない問題を修正[＃52257](https://github.com/pingcap/tidb/issues/52257) [＃51712](https://github.com/pingcap/tidb/issues/51712) @ [ジフハウス](https://github.com/jiyfhust)
    -   書き込みホットスポットのスケジュール設定により配置ポリシーの制約が破られる可能性がある問題を修正[＃7848](https://github.com/tikv/pd/issues/7848) @ [翻訳者](https://github.com/lhy1024)
    -   配置ルール[＃7808](https://github.com/tikv/pd/issues/7808) @ [rleungx](https://github.com/rleungx)を使用すると、ダウンしたピアが回復しない可能性がある問題を修正しました。
    -   リソース グループ クエリ[＃8217](https://github.com/tikv/pd/issues/8217) @ [ノルーシュ](https://github.com/nolouch)をキャンセルするときに再試行が大量に発生する問題を修正しました
    -   PDリーダーを手動で転送すると失敗する可能性がある問題を修正[＃8225](https://github.com/tikv/pd/issues/8225) @ [ヒューシャープ](https://github.com/HuSharp)

-   TiFlash

    -   空のパーティション[＃9024](https://github.com/pingcap/tiflash/issues/9024) @ [ジンヘリン](https://github.com/JinheLin)を含むパーティション テーブルでクエリを実行するときに発生するクエリ タイムアウトの問題を修正しました。
    -   分散storageおよびコンピューティングアーキテクチャで、DDL 操作[＃9084](https://github.com/pingcap/tiflash/issues/9084) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)で非 NULL 列を追加した後にクエリで NULL 値が誤って返される可能性がある問題を修正しました。
    -   `SUBSTRING_INDEX()`関数が一部のコーナーケースでTiFlash をクラッシュさせる可能性がある問題を修正[＃9116](https://github.com/pingcap/tiflash/issues/9116) @ [うわー](https://github.com/wshwsh12)
    -   BRまたはTiDB Lightning [＃9118](https://github.com/pingcap/tiflash/issues/9118) @ [ジンヘリン](https://github.com/JinheLin)経由でデータをインポートした後、FastScan モードで多数の重複行が読み取られる可能性がある問題を修正しました。

-   ツール

    -   バックアップと復元 (BR)

        -   空の`EndKey` [＃52574](https://github.com/pingcap/tidb/issues/52574) @ [3ポインター](https://github.com/3pointer)が原因でBR がトランザクション KV クラスターを復元できない問題を修正しました。
        -   PD 接続障害により、ログ バックアップ アドバンサ所有者が配置されている TiDB インスタンスがpanicになる可能性がある問題を修正しました[＃52597](https://github.com/pingcap/tidb/issues/52597) @ [ユジュンセン](https://github.com/YuJuncen)
        -   アドバンサー所有者の移行[＃53561](https://github.com/pingcap/tidb/issues/53561) @ [リドリス](https://github.com/RidRisR)後にログバックアップが一時停止される可能性がある問題を修正
        -   復元プロセス中に複数のネストされた再試行が原因でBR がエラーを正しく識別できない問題を修正[＃54053](https://github.com/pingcap/tidb/issues/54053) @ [リドリス](https://github.com/RidRisR)
        -   TiKV 構成を取得するために使用される接続が閉じられない可能性がある問題を修正[＃52595](https://github.com/pingcap/tidb/issues/52595) @ [リドリス](https://github.com/RidRisR)
        -   `TestStoreRemoved`テストケースが不安定になる問題を修正[＃52791](https://github.com/pingcap/tidb/issues/52791) @ [ユジュンセン](https://github.com/YuJuncen)
        -   ポイントインタイムリカバリ（PITR）中にTiFlashがクラッシュする問題を修正[＃52628](https://github.com/pingcap/tidb/issues/52628) @ [リドリス](https://github.com/RidRisR)
        -   増分バックアップ[＃54139](https://github.com/pingcap/tidb/issues/54139) @ [3ポインター](https://github.com/3pointer)中の DDL ジョブのスキャンにおける非効率性の問題を修正
        -   リージョンリーダー[＃17168](https://github.com/tikv/tikv/issues/17168) @ [リーヴルス](https://github.com/Leavrth)シークの中断により、チェックポイントバックアップ中のバックアップパフォーマンスが影響を受ける問題を修正しました。

    -   ティCDC

        -   Grafana [＃10777](https://github.com/pingcap/tiflow/issues/10777) @ [アズドンメン](https://github.com/asddongmen)の**Kafka 送信バイト**パネルの不正確な表示を修正
        -   マルチノード環境で大量の`UPDATE`操作を実行する際にChangefeedを繰り返し再起動するとデータの不整合が発生する可能性がある問題を修正[＃11219](https://github.com/pingcap/tiflow/issues/11219) @ [リデズ](https://github.com/lidezhu)

    -   TiDB データ移行 (DM)

        -   `go-mysql` [＃11041](https://github.com/pingcap/tiflow/issues/11041) @ [D3ハンター](https://github.com/D3Hunter)にアップグレードして接続ブロックの問題を修正
        -   MariaDB データの移行中に`SET`ステートメントによって DM がpanicになる問題を修正[＃10206](https://github.com/pingcap/tiflow/issues/10206) @ [ドヴェーデン](https://github.com/dveeden)

    -   TiDB Lightning

        -   zstd 圧縮ファイルをインポートするときにTiDB Lightning がエラーを報告する可能性がある問題を修正[＃53587](https://github.com/pingcap/tidb/issues/53587) @ [ランス6716](https://github.com/lance6716)

    -   Dumpling

        -   テーブルとビューを同時にエクスポートするとDumpling がエラーを報告する問題を修正[＃53682](https://github.com/pingcap/tidb/issues/53682) @ [タンジェンタ](https://github.com/tangenta)

    -   TiDBBinlog

        -   TiDB Binlogが有効な場合、 `ADD COLUMN`の実行中に行を削除するとエラー`data and columnID count not match`が報告される可能性がある問題を修正[＃53133](https://github.com/pingcap/tidb/issues/53133) @ [タンジェンタ](https://github.com/tangenta)

## 寄稿者 {#contributors}

TiDB コミュニティの以下の貢献者に感謝いたします。

-   [キャビンフィーバーB](https://github.com/CabinfeverB)
-   [ダン・ロシニョ](https://github.com/DanRoscigno) (初めての投稿者)
-   [杉本栄](https://github.com/ei-sugimoto) (初めての投稿者)
-   [エルトシア](https://github.com/eltociear)
-   [ジフハウス](https://github.com/jiyfhust)
-   [マイケル・ムデン](https://github.com/michaelmdeng) (初めての投稿者)
-   [ミッタルリシャブ](https://github.com/mittalrishabh)
-   [猫のみ](https://github.com/onlyacat)
-   [キチェン](https://github.com/qichengzx) (初めての投稿者)
-   [シーライズ](https://github.com/SeaRise)
-   [ショーン0915](https://github.com/shawn0915)
-   [藤田俊樹](https://github.com/shunki-fujita) (初めての投稿者)
-   [トニー](https://github.com/tonyxuqqi)
-   [わーい](https://github.com/wwu) (初めての投稿者)
-   [yzhan1](https://github.com/yzhan1)
