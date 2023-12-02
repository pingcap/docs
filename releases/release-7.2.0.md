---
title: TiDB 7.2.0 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 7.2.0.
---

# TiDB 7.2.0 リリースノート {#tidb-7-2-0-release-notes}

発売日：2023年6月29日

TiDB バージョン: 7.2.0

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v7.2/quick-start-with-tidb) | [インストールパッケージ](https://www.pingcap.com/download/?version=v7.2.0#version-list)

7.2.0 では、次の主要な機能と改善点が導入されています。

<table><thead><tr><th>カテゴリー</th><th>特徴</th><th>説明</th></tr></thead><tbody><tr><td rowspan="2">スケーラビリティとパフォーマンス</td><td>リソース グループは<a href="https://docs.pingcap.com/tidb/v7.2/tidb-resource-control#manage-queries-that-consume-more-resources-than-expected-runaway-queries">暴走クエリの管理を</a>サポートします (実験的)</td><td>クエリのタイムアウトをより詳細に管理できるようになり、クエリの分類に基づいてさまざまな動作が可能になります。指定したしきい値を満たすクエリは、優先順位を下げたり、終了したりできます。</td></tr><tr><td> TiFlash は<a href="https://docs.pingcap.com/tidb/v7.2/tiflash-pipeline-model">パイプライン実行モデルを</a>サポートします (実験的)</td><td> TiFlash は、スレッド リソース制御を最適化するパイプライン実行モデルをサポートしています。</td></tr><tr><td rowspan="1"> SQL</td><td>データインポート用の新しい SQL ステートメント<a href="https://docs.pingcap.com/tidb/v7.2/sql-statement-import-into">IMPORT INTO</a>をサポートします (実験的)</td><td> TiDB Lightningのデプロイメントとメンテナンスを簡素化するために、TiDB では新しい SQL ステートメント<code>IMPORT INTO</code>を導入しています。これは、Amazon S3 または Google Cloud Storage (GCS) から TiDB に直接リモート インポートするなど、 TiDB Lightningの物理インポート モードを統合します。</td></tr><tr><td rowspan="2"> DB の操作と可観測性</td><td>DDL は<a href="https://docs.pingcap.com/tidb/v7.2/ddl-introduction#ddl-related-commands">一時停止および再開操作</a>をサポートします (実験的)</td><td>この新機能により、インデックス作成などのリソースを大量に消費する DDL 操作を一時的に停止して、リソースを節約し、オンライン トラフィックへの影響を最小限に抑えることができます。準備ができたら、キャンセルして再起動することなく、これらの操作をシームレスに再開できます。この機能により、リソースの使用率が向上し、ユーザー エクスペリエンスが向上し、スキーマの変更が合理化されます。</td></tr></tbody></table>

## 機能の詳細 {#feature-details}

### パフォーマンス {#performance}

-   次の 2 つの[ウィンドウ関数](/tiflash/tiflash-supported-pushdown-calculations.md) TiFlash [#7427](https://github.com/pingcap/tiflash/issues/7427) @ [xzhangxian1008](https://github.com/xzhangxian1008)にプッシュダウンすることをサポートします。

    -   `FIRST_VALUE`
    -   `LAST_VALUE`

-   TiFlash はパイプライン実行モデル (実験的) [#6518](https://github.com/pingcap/tiflash/issues/6518) @ [シーライズ](https://github.com/SeaRise)をサポートしています。

    v7.2.0 より前では、 TiFlashエンジンの各タスクは実行中に個別にスレッド リソースを要求する必要がありました。 TiFlash は、スレッド リソースの使用量を制限し、過剰使用を防ぐためにタスクの数を制御しますが、この問題を完全に排除することはできませんでした。この問題に対処するために、 TiFlash には v7.2.0 以降、パイプライン実行モデルが導入されています。このモデルは、すべてのスレッド リソースを集中管理し、タスクの実行を均一にスケジュールすることで、リソースの過剰使用を回避しながらスレッド リソースの利用率を最大化します。パイプライン実行モデルを有効または無効にするには、 [`tidb_enable_tiflash_pipeline_model`](https://docs.pingcap.com/tidb/v7.2/system-variables#tidb_enable_tiflash_pipeline_model-new-in-v720)システム変数を変更します。

    詳細については、 [ドキュメンテーション](/tiflash/tiflash-pipeline-model.md)を参照してください。

-   TiFlash は、スキーマ レプリケーションのレイテンシー[#7630](https://github.com/pingcap/tiflash/issues/7630) @ [ホンユニャン](https://github.com/hongyunyan)を削減します。

    テーブルのスキーマが変更されると、 TiFlash はTiKV から最新のスキーマをタイムリーに複製する必要があります。 v7.2.0 より前では、 TiFlash がテーブル データにアクセスし、データベース内のテーブル スキーマの変更を検出した場合、 TiFlash は、 TiFlashレプリカのないテーブルも含め、このデータベース内のすべてのテーブルのスキーマを再度複製する必要があります。その結果、多数のテーブルを含むデータベースでは、 TiFlashを使用して 1 つのテーブルからデータを読み取るだけでよい場合でも、 TiFlash がすべてのテーブルのスキーマ レプリケーションを完了するまでにかなりのレイテンシーが発生する可能性があります。

    v7.2.0 では、 TiFlash はスキーマ レプリケーション メカニズムを最適化し、 TiFlashレプリカを使用したテーブルのスキーマのレプリケーションのみをサポートします。 TiFlashレプリカを含むテーブルのスキーマ変更が検出されると、 TiFlash はそのテーブルのスキーマのみをレプリケートします。これにより、 TiFlashのスキーマ レプリケーションのレイテンシーが短縮され、 TiFlashデータ レプリケーションに対する DDL 操作の影響が最小限に抑えられます。この最適化は自動的に適用されるため、手動による構成は必要ありません。

-   統計収集[#44725](https://github.com/pingcap/tidb/issues/44725) @ [シュイファングリーンアイズ](https://github.com/xuyifangreeneyes)のパフォーマンスを向上させます。

    TiDB v7.2.0 は統計収集戦略を最適化し、重複情報やオプティマイザーにとってほとんど価値のない情報の一部をスキップします。統計収集の全体的な速度が 30% 向上しました。この改善により、TiDB はデータベースの統計をよりタイムリーに更新できるようになり、生成された実行計画がより正確になり、データベース全体のパフォーマンスが向上します。

    デフォルトでは、統計収集では`JSON` 、 `BLOB` 、 `MEDIUMBLOB` 、および`LONGBLOB`タイプの列がスキップされます。 [`tidb_analyze_skip_column_types`](/system-variables.md#tidb_analyze_skip_column_types-new-in-v720)システム変数を設定することで、デフォルトの動作を変更できます。 TiDB は`JSON` 、 `BLOB` 、および`TEXT`タイプとそのサブタイプのスキップをサポートします。

    詳細については、 [ドキュメンテーション](/system-variables.md#tidb_analyze_skip_column_types-new-in-v720)を参照してください。

-   データとインデックスの整合性チェックのパフォーマンスを向上[#43693](https://github.com/pingcap/tidb/issues/43693) @ [wjhuang2016](https://github.com/wjhuang2016)

    [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md)ステートメントは、テーブル内のデータとそれに対応するインデックス間の整合性をチェックするために使用されます。 v7.2.0 では、TiDB はデータの整合性をチェックする方法を最適化し、 [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md)の実行効率を大幅に向上させます。大量のデータを使用するシナリオでは、この最適化によりパフォーマンスが数百倍向上します。

    最適化はデフォルトで有効になっており (デフォルトでは[`tidb_enable_fast_table_check`](/system-variables.md#tidb_enable_fast_table_check-new-in-v720)は`ON` )、大規模なテーブルのデータ整合性チェックに必要な時間が大幅に短縮され、運用効率が向上します。

    詳細については、 [ドキュメンテーション](/system-variables.md#tidb_enable_fast_table_check-new-in-v720)を参照してください。

### 信頼性 {#reliability}

-   予想よりも多くのリソースを消費するクエリを自動的に管理する (実験的) [#43691](https://github.com/pingcap/tidb/issues/43691) @ [コナー1996](https://github.com/Connor1996) @ [キャビンフィーバーB](https://github.com/CabinfeverB) @ [グロルフ](https://github.com/glorv) @ [ヒューシャープ](https://github.com/HuSharp) @ [ノールーシュ](https://github.com/nolouch)

    データベースの安定性に対する最も一般的な課題は、突然の SQL パフォーマンスの問題によって引き起こされるデータベース全体のパフォーマンスの低下です。 SQL パフォーマンスの問題には、十分にテストされていない新しい SQL ステートメント、データ量の大幅な変更、実行計画の突然の変更など、さまざまな原因が考えられます。これらの問題を根本から完全に回避することは困難です。 TiDB v7.2.0 は、予想よりも多くのリソースを消費するクエリを管理する機能を提供します。この機能により、パフォーマンスの問題が発生した場合に、影響範囲を迅速に縮小できます。

    これらのクエリを管理するために、リソース グループのクエリの最大実行時間を設定できます。クエリの実行時間がこの制限を超えると、クエリは自動的に優先順位が下げられるかキャンセルされます。特定されたクエリをテキストまたは実行プランで即座に照合する期間を設定することもできます。これは、予想よりも多くのリソースを消費する可能性がある、識別フェーズ中に問題のあるクエリの同時実行性が高くなることを防ぐのに役立ちます。

    予想よりも多くのリソースを消費するクエリの自動管理により、予期しないクエリのパフォーマンスの問題に迅速に対応するための効果的な手段が提供されます。この機能により、データベース全体のパフォーマンスに対する問題の影響が軽減され、データベースの安定性が向上します。

    詳細については、 [ドキュメンテーション](/tidb-resource-control.md#manage-queries-that-consume-more-resources-than-expected-runaway-queries)を参照してください。

-   過去の実行計画に従ってバインディングを作成する機能を強化[#39199](https://github.com/pingcap/tidb/issues/39199) @ [qw4990](https://github.com/qw4990)

    TiDB v7.2.0 は[過去の実行計画に従ってバインディングを作成する](/sql-plan-management.md#create-a-binding-according-to-a-historical-execution-plan)の機能を強化します。この機能により、複雑なステートメントの解析とバインドのプロセスが改善され、バインディングがより安定し、次の新しいヒントがサポートされます。

    -   [`AGG_TO_COP()`](/optimizer-hints.md#agg_to_cop)
    -   [`LIMIT_TO_COP()`](/optimizer-hints.md#limit_to_cop)
    -   [`ORDER_INDEX`](/optimizer-hints.md#order_indext1_name-idx1_name--idx2_name-)
    -   [`NO_ORDER_INDEX()`](/optimizer-hints.md#no_order_indext1_name-idx1_name--idx2_name-)

    詳細については、 [ドキュメンテーション](/sql-plan-management.md)を参照してください。

-   オプティマイザー修正制御メカニズムを導入して、オプティマイザーの動作をきめ細かく制御できるようにします[#43169](https://github.com/pingcap/tidb/issues/43169) @ [時間と運命](https://github.com/time-and-fate)

    より合理的な実行計画を生成するために、TiDB オプティマイザーの動作は製品の反復を通じて進化します。ただし、特定のシナリオでは、変更によりパフォーマンスの低下が生じる可能性があります。 TiDB v7.2.0 では、オプティマイザーの詳細な動作の一部を制御できるオプティマイザー修正コントロールが導入されています。これにより、いくつかの新しい変更をロールバックしたり制御したりできます。

    制御可能な各動作は、修正番号に対応する GitHub の問題によって説明されます。制御可能な動作はすべて[オプティマイザー修正コントロール](/optimizer-fix-controls.md)にリストされています。 [`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-new-in-v710)システム変数を設定して 1 つ以上の動作の目標値を設定し、動作制御を実現できます。

    オプティマイザー修正制御メカニズムは、TiDB オプティマイザーを詳細なレベルで制御するのに役立ちます。これは、アップグレード プロセスによって引き起こされるパフォーマンスの問題を修正する新しい手段を提供し、TiDB の安定性を向上させます。

    詳細については、 [ドキュメンテーション](/optimizer-fix-controls.md)を参照してください。

-   軽量の統計初期化が一般公開 (GA) [#42160](https://github.com/pingcap/tidb/issues/42160) @ [シュイファングリーンアイズ](https://github.com/xuyifangreeneyes)

    v7.2.0 以降、軽量統計初期化機能が GA になりました。軽量の統計初期化により、起動時にロードする必要がある統計の数が大幅に削減され、統計のロード速度が向上します。この機能により、複雑なランタイム環境における TiDB の安定性が向上し、TiDB ノードの再起動時のサービス全体への影響が軽減されます。

    v7.2.0 以降のバージョンで新しく作成されたクラスターの場合、TiDB は TiDB の起動時にデフォルトで軽量統計をロードし、ロードが完了するまで待ってからサービスを提供します。以前のバージョンからアップグレードされたクラスターの場合、TiDB 構成項目[`lite-init-stats`](/tidb-configuration-file.md#lite-init-stats-new-in-v710)および[`force-init-stats`](/tidb-configuration-file.md#force-init-stats-new-in-v710)から`true`を設定して、この機能を有効にすることができます。

    詳細については、 [ドキュメンテーション](/statistics.md#load-statistics)を参照してください。

### SQL {#sql}

-   `CHECK`制約[#41711](https://github.com/pingcap/tidb/issues/41711) @ [fzzf678](https://github.com/fzzf678)をサポート

    v7.2.0 以降、 `CHECK`制約を使用して、指定した条件を満たすようにテーブル内の 1 つ以上の列の値を制限できます。 `CHECK`制約がテーブルに追加されると、TiDB はテーブルにデータを挿入または更新する前に制約が満たされているかどうかをチェックします。制約を満たすデータのみを書き込むことができます。

    この機能はデフォルトでは無効になっています。 [`tidb_enable_check_constraint`](/system-variables.md#tidb_enable_check_constraint-new-in-v720)システム変数を`ON`に設定して有効にできます。

    詳細については、 [ドキュメンテーション](/constraints.md#check)を参照してください。

### DB操作 {#db-operations}

-   DDL ジョブは操作の一時停止と再開をサポートします (実験的) [#18015](https://github.com/pingcap/tidb/issues/18015) @ [ゴドゥム](https://github.com/godouxm)

    TiDB v7.2.0 より前では、DDL ジョブの実行中にビジネス ピークが発生した場合、DDL ジョブを手動でキャンセルしてビジネスへの影響を軽減することしかできませんでした。 v7.2.0 では、TiDB に DDL ジョブの一時停止および再開操作が導入されました。これらの操作により、ピーク時に DDL ジョブを一時停止し、ピーク終了後に再開できるため、アプリケーションのワークロードへの影響を回避できます。

    たとえば、 `ADMIN PAUSE DDL JOBS`または`ADMIN RESUME DDL JOBS`を使用して複数の DDL ジョブを一時停止および再開できます。

    ```sql
    ADMIN PAUSE DDL JOBS 1,2;
    ADMIN RESUME DDL JOBS 1,2;
    ```

    詳細については、 [ドキュメンテーション](/ddl-introduction.md#ddl-related-commands)を参照してください。

### データ移行 {#data-migration}

-   データのインポート効率を大幅に向上させる新しい SQL ステートメント`IMPORT INTO`を導入します (実験的) [#42930](https://github.com/pingcap/tidb/issues/42930) @ [D3ハンター](https://github.com/D3Hunter)

    `IMPORT INTO`ステートメントは、 TiDB Lightningの[物理インポートモード](/tidb-lightning/tidb-lightning-physical-import-mode.md)機能を統合します。このステートメントを使用すると、CSV、SQL、PARQUET などの形式でデータを TiDB の空のテーブルにすばやくインポートできます。このインポート方法により、 TiDB Lightningを個別に展開して管理する必要がなくなり、データ インポートの複雑さが軽減され、インポート効率が大幅に向上します。

    Amazon S3 または GCS に保存されているデータ ファイルの場合、 [バックエンドタスク分散実行フレームワーク](/tidb-distributed-execution-framework.md)が有効な場合、 `IMPORT INTO`データ インポート ジョブを複数のサブジョブに分割し、それらを並行インポート用に複数の TiDB ノードにスケジュールすることもサポートします。これにより、インポートのパフォーマンスがさらに向上します。

    詳細については、 [ドキュメンテーション](/sql-statements/sql-statement-import-into.md)を参照してください。

-   TiDB Lightning は、 Latin-1 文字セットを含むソース ファイルの TiDB [#44434](https://github.com/pingcap/tidb/issues/44434) @ [ランス6716](https://github.com/lance6716)へのインポートをサポートしています。

    この機能を使用すると、 TiDB Lightningを使用して、Latin-1 文字セットを含むソース ファイルを TiDB に直接インポートできます。 v7.2.0 より前では、このようなファイルをインポートするには追加の前処理または変換が必要です。 v7.2.0 以降、 TiDB Lightningインポート タスクを構成するときに`character-set = "latin1"`を指定するだけで済みます。その後、 TiDB Lightning はインポート プロセス中に自動的に文字セット変換を処理し、データの整合性と正確性を確保します。

    詳細については、 [ドキュメンテーション](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)を参照してください。

## 互換性の変更 {#compatibility-changes}

> **注記：**
>
> このセクションでは、v7.1.0 から現在のバージョン (v7.2.0) にアップグレードするときに知っておく必要がある互換性の変更について説明します。 v7.0.0 以前のバージョンから現在のバージョンにアップグレードする場合は、中間バージョンで導入された互換性の変更も確認する必要がある場合があります。

### システム変数 {#system-variables}

| 変数名                                                                                                                                        | 種類の変更    | 説明                                                                                                                                                                                                                                                                            |
| ------------------------------------------------------------------------------------------------------------------------------------------ | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`last_insert_id`](/system-variables.md#last_insert_id)                                                                                    | 修正済み     | MySQL の最大値と一致するように、最大​​値を`9223372036854775807`から`18446744073709551615`に変更します。                                                                                                                                                                                                 |
| [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache)                                          | 修正済み     | さらにテストを行った後、デフォルト値を`OFF`から`ON`に変更します。これは、準備されていない実行プラン キャッシュが有効になることを意味します。                                                                                                                                                                                                   |
| [`tidb_remove_orderby_in_subquery`](/system-variables.md#tidb_remove_orderby_in_subquery-new-in-v610)                                      | 修正済み     | さらにテストを行った後、デフォルト値を`OFF`から`ON`に変更します。これは、オプティマイザがサブクエリ内の`ORDER BY`句を削除することを意味します。                                                                                                                                                                                             |
| [`tidb_analyze_skip_column_types`](/system-variables.md#tidb_analyze_skip_column_types-new-in-v720)                                        | 新しく追加された | 統計を収集するコマンド`ANALYZE`を実行するときに、統計収集のためにどのタイプの列をスキップするかを制御します。この変数は[`tidb_analyze_version = 2`](/system-variables.md#tidb_analyze_version-new-in-v510)にのみ適用されます。 `ANALYZE TABLE t COLUMNS c1, ..., cn`の構文を使用する場合、指定した列の型が`tidb_analyze_skip_column_types`に含まれる場合、この列の統計は収集されません。 |
| [`tidb_enable_check_constraint`](/system-variables.md#tidb_enable_check_constraint-new-in-v720)                                            | 新しく追加された | `CHECK`制約を有効にするかどうかを制御します。デフォルト値は`OFF`で、この機能が無効であることを意味します。                                                                                                                                                                                                                   |
| [`tidb_enable_fast_table_check`](/system-variables.md#tidb_enable_fast_table_check-new-in-v720)                                            | 新しく追加された | テーブル内のデータとインデックスの整合性を迅速にチェックするためにチェックサムベースのアプローチを使用するかどうかを制御します。デフォルト値は`ON`で、この機能が有効であることを意味します。                                                                                                                                                                              |
| [`tidb_enable_tiflash_pipeline_model`](https://docs.pingcap.com/tidb/v7.2/system-variables#tidb_enable_tiflash_pipeline_model-new-in-v720) | 新しく追加された | TiFlashの新しい実行モデル[パイプラインモデル](/tiflash/tiflash-pipeline-model.md)を有効にするかどうかを制御します。デフォルト値は`OFF`で、パイプライン モデルが無効であることを意味します。                                                                                                                                                       |
| [`tidb_expensive_txn_time_threshold`](/system-variables.md#tidb_expensive_txn_time_threshold-new-in-v720)                                  | 新しく追加された | 高価なトランザクションをログに記録するためのしきい値を制御します。デフォルトでは 600 秒です。トランザクションの継続時間がしきい値を超え、トランザクションがコミットもロールバックもされない場合、そのトランザクションは高価なトランザクションとみなされ、ログに記録されます。                                                                                                                                     |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーションパラメータ                                                                                                                                 | 種類の変更    | 説明                                                                                                                                                                                                                                                                                      |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB           | [`lite-init-stats`](/tidb-configuration-file.md#lite-init-stats-new-in-v710)                                                                    | 修正済み     | さらにテストを行った後、デフォルト値を`false`から`true`に変更します。これは、TiDB が初期化効率を向上させるために、TiDB の起動時にデフォルトで軽量統計初期化を使用することを意味します。                                                                                                                                                                                 |
| TiDB           | [`force-init-stats`](/tidb-configuration-file.md#force-init-stats-new-in-v710)                                                                  | 修正済み     | デフォルト値を`false`から`true`に変更して[`lite-init-stats`](/tidb-configuration-file.md#lite-init-stats-new-in-v710)に合わせます。これは、TiDB が TiDB の起動中にサービスを提供する前に統計の初期化が完了するのを待つことを意味します。                                                                                                                  |
| TiKV           | [`rocksdb.[defaultcf|writecf|lockcf].compaction-guard-min-output-file-size`](/tikv-configuration-file.md#compaction-guard-min-output-file-size) | 修正済み     | RocksDB の圧縮タスクのデータ量を減らすために、デフォルト値を`"8MB"`から`"1MB"`に変更します。                                                                                                                                                                                                                               |
| TiKV           | [`rocksdb.[defaultcf|writecf|lockcf].optimize-filters-for-memory`](/tikv-configuration-file.md#optimize-filters-for-memory-new-in-v720)         | 新しく追加された | メモリ内部の断片化を最小限に抑えるブルーム/リボン フィルターを生成するかどうかを制御します。                                                                                                                                                                                                                                         |
| TiKV           | [`rocksdb.[defaultcf|writecf|lockcf].periodic-compaction-seconds`](/tikv-configuration-file.md#periodic-compaction-seconds-new-in-v720)         | 新しく追加された | 定期的な圧縮の時間間隔を制御します。この値より古い更新を含む SST ファイルは圧縮対象として選択され、これらの SST ファイルが元々存在していたレベルと同じレベルに再書き込みされます。                                                                                                                                                                                          |
| TiKV           | [`rocksdb.[defaultcf|writecf|lockcf].ribbon-filter-above-level`](/tikv-configuration-file.md#ribbon-filter-above-level-new-in-v720)             | 新しく追加された | この値以上のレベルにリボン フィルターを使用するか、この値未満のレベルに非ブロックベースのブルーム フィルターを使用するかを制御します。                                                                                                                                                                                                                    |
| TiKV           | [`rocksdb.[defaultcf|writecf|lockcf].ttl`](/tikv-configuration-file.md#ttl-new-in-v720)                                                         | 新しく追加された | TTL より古い更新を含む SST ファイルは、圧縮対象として自動的に選択されます。                                                                                                                                                                                                                                              |
| TiDB Lightning | `send-kv-pairs`                                                                                                                                 | 廃止されました  | v7.2.0 以降、パラメータ`send-kv-pairs`は非推奨になりました。物理インポート モードで TiKV にデータを送信する場合、 [`send-kv-size`](/tidb-lightning/tidb-lightning-configuration.md)を使用して 1 つのリクエストの最大サイズを制御できます。                                                                                                                  |
| TiDB Lightning | [`character-set`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)                                                          | 修正済み     | データ インポートでサポートされる文字セットに新しい値オプション`latin1`が導入されました。このオプションを使用すると、Latin-1 文字セットを含むソース ファイルをインポートできます。                                                                                                                                                                                      |
| TiDB Lightning | [`send-kv-size`](/tidb-lightning/tidb-lightning-configuration.md)                                                                               | 新しく追加された | 物理インポートモードでTiKVにデータを送信する際の1リクエストの最大サイズを指定します。キーと値のペアのサイズが指定されたしきい値に達すると、 TiDB Lightningはそれらのペアを直ちに TiKV に送信します。これにより、大きな幅のテーブルをインポートするときにTiDB Lightningノードがメモリ内にあまりにも多くのキーと値のペアを蓄積することによって引き起こされる OOM 問題が回避されます。このパラメータを調整すると、メモリ使用量とインポート速度のバランスが取れ、インポート プロセスの安定性と効率が向上します。           |
| データ移行          | [`strict-optimistic-shard-mode`](/dm/feature-shard-merge-optimistic.md)                                                                         | 新しく追加された | この構成アイテムは、TiDB Data Migration v2.0 の DDL シャード マージ動作と互換性を保つために使用されます。この設定項目は楽観的モードで有効にできます。これを有効にすると、レプリケーション タスクはタイプ 2 DDL ステートメントに遭遇すると中断されます。複数のテーブルの DDL 変更間に依存関係があるシナリオでは、適時に中断される可能性があります。アップストリームとダウンストリームの間でデータの一貫性を確保するには、レプリケーション タスクを再開する前に各テーブルの DDL ステートメントを手動で処理する必要があります。 |
| TiCDC          | [`sink.protocol`](/ticdc/ticdc-changefeed-config.md)                                                                                            | 修正済み     | ダウンストリームが Kafka の場合、新しい値のオプション`"open-protocol"`が導入されます。メッセージのエンコードに使用されるプロトコル形式を指定します。                                                                                                                                                                                                  |
| TiCDC          | [`sink.delete-only-output-handle-key-columns`](/ticdc/ticdc-changefeed-config.md)                                                               | 新しく追加された | DELETE イベントの出力を指定します。このパラメータは、 `"canal-json"`および`"open-protocol"`プロトコルに対してのみ有効です。デフォルト値は`false`で、すべての列を出力することを意味します。 `true`に設定すると、主キー列または一意のインデックス列のみが出力されます。                                                                                                                           |

## 改善点 {#improvements}

-   TiDB

    -   複雑な条件をインデックス スキャン範囲[#41572](https://github.com/pingcap/tidb/issues/41572) [#44389](https://github.com/pingcap/tidb/issues/44389) @ [シュイファングリーンアイズ](https://github.com/xuyifangreeneyes)に変換できるように、インデックス スキャン範囲を構築するロジックを最適化します。
    -   新しい監視メトリクス`Stale Read OPS`および`Stale Read Traffic` [#43325](https://github.com/pingcap/tidb/issues/43325) @ [あなた06](https://github.com/you06)を追加
    -   古い読み取りの再試行リーダーがロックに遭遇すると、TiDB はロックを解決した後にリーダーで強制的に再試行します。これにより、不要なオーバーヘッドが回避されます[#43659](https://github.com/pingcap/tidb/issues/43659) @ [あなた06](https://github.com/you06)
    -   推定時間を使用して古い読み取り ts を計算し、古い読み取り[#44215](https://github.com/pingcap/tidb/issues/44215) @ [あなた06](https://github.com/you06)のオーバーヘッドを削減します。
    -   長時間実行トランザクションのログとシステム変数を追加[#41471](https://github.com/pingcap/tidb/issues/41471) @ [クレイジークス520](https://github.com/crazycs520)
    -   圧縮 MySQL プロトコルを介した TiDB への接続をサポートします。これにより、低帯域幅ネットワーク下でのデータ集約型クエリのパフォーマンスが向上し、帯域幅コストが節約されます。これは、 `zlib`ベースの圧縮と`zstd`の圧縮の両方をサポートします。 [#22605](https://github.com/pingcap/tidb/issues/22605) @ [ドヴィーデン](https://github.com/dveeden)
    -   `utf8`と`utf8bm3`の両方を従来の 3 バイト UTF-8 文字セット エンコーディングとして認識するため、従来の UTF-8 エンコーディングを使用したテーブルの MySQL 8.0 から TiDB [#26226](https://github.com/pingcap/tidb/issues/26226) @ [ドヴィーデン](https://github.com/dveeden)への移行が容易になります。
    -   `UPDATE`ステートメント[#44751](https://github.com/pingcap/tidb/issues/44751) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)での代入に`:=`を使用するサポート

-   TiKV

    -   `pd.retry-interval` [#14964](https://github.com/tikv/tikv/issues/14964) @ [ルルンクス](https://github.com/rleungx)を使用した接続要求の失敗などのシナリオでの PD 接続の再試行間隔の構成のサポート
    -   グローバル リソース使用量[#14604](https://github.com/tikv/tikv/issues/14604) @ [コナー1996](https://github.com/Connor1996)を組み込むことにより、リソース制御スケジューリング アルゴリズムを最適化します。
    -   `check_leader`リクエストに gzip 圧縮を使用してトラフィック[#14553](https://github.com/tikv/tikv/issues/14553) @ [あなた06](https://github.com/you06)を削減します
    -   `check_leader`リクエスト[#14658](https://github.com/tikv/tikv/issues/14658) @ [あなた06](https://github.com/you06)に関連するメトリクスを追加
    -   TiKV の書き込みコマンド処理中に詳細な時間情報を提供します[#12362](https://github.com/tikv/tikv/issues/12362) @ [cfzjywxk](https://github.com/cfzjywxk)

-   PD

    -   他のリクエストの影響を防ぐために、PD リーダーの選出には別の gRPC 接続を使用します[#6403](https://github.com/tikv/pd/issues/6403) @ [ルルンクス](https://github.com/rleungx)
    -   マルチリージョン シナリオ[#6433](https://github.com/tikv/pd/issues/6433) @ [バッファフライ](https://github.com/bufferflies)でのホットスポットの問題を軽減するために、デフォルトでバケット分割を有効にします。

-   ツール

    -   バックアップと復元 (BR)

        -   Shared Access Signature (SAS) [#44199](https://github.com/pingcap/tidb/issues/44199) @ [レヴルス](https://github.com/Leavrth)による Azure Blob Storage へのアクセスのサポート

    -   TiCDC

        -   オブジェクトstorageサービスへのレプリケーションのシナリオで DDL 操作が発生するときに、データ ファイルが保存されるディレクトリの構造を最適化します[#8891](https://github.com/pingcap/tiflow/issues/8891) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   Kafka [#8865](https://github.com/pingcap/tiflow/issues/8865) @ [こんにちはラスティン](https://github.com/hi-rustin)へのレプリケーションのシナリオで OAUTHBEARER 認証をサポートします。
        -   Kafka [#9143](https://github.com/pingcap/tiflow/issues/9143) @ [3エースショーハンド](https://github.com/3AceShowHand)にレプリケーションのシナリオにおける`DELETE`オペレーションのハンドルキーのみを出力するオプションを追加

    -   TiDB データ移行 (DM)

        -   インクリメンタル レプリケーション[#6381](https://github.com/pingcap/tiflow/issues/6381) @ [ドヴィーデン](https://github.com/dveeden)のデータ ソースとして、MySQL 8.0 で圧縮されたバイナリログの読み取りをサポートします。

    -   TiDB Lightning

        -   リーダー切り替え[#44478](https://github.com/pingcap/tidb/pull/44478) @ [ランス6716](https://github.com/lance6716)によって引き起こされるエラーを回避するために、インポート中の再試行メカニズムを最適化します。
        -   インポート後に SQL でチェックサムを検証し、検証の安定性を向上させる[#41941](https://github.com/pingcap/tidb/issues/41941) @ [GMHDBJD](https://github.com/GMHDBJD)
        -   幅の広いテーブル[#43853](https://github.com/pingcap/tidb/issues/43853) @ [D3ハンター](https://github.com/D3Hunter)をインポートする際のTiDB Lightning OOM 問題の最適化

## バグの修正 {#bug-fixes}

-   TiDB

    -   CTE を使用したクエリにより TiDB がハングする問題を修正[#43749](https://github.com/pingcap/tidb/issues/43749) [#36896](https://github.com/pingcap/tidb/issues/36896) @ [グオシャオゲ](https://github.com/guo-shaoge)
    -   `min, max`クエリ結果が正しくない問題を修正[#43805](https://github.com/pingcap/tidb/issues/43805) @ [wshwsh12](https://github.com/wshwsh12)
    -   `SHOW PROCESSLIST`ステートメントがサブクエリ時間の長いステートメント[#40851](https://github.com/pingcap/tidb/issues/40851) @ [クレイジークス520](https://github.com/crazycs520)のトランザクションの TxnStart を表示できない問題を修正
    -   コプロセッサータスク[#43365](https://github.com/pingcap/tidb/issues/43365) @ [あなた06](https://github.com/you06)に`TxnScope`がないため、古い読み取りグローバル最適化が有効にならない問題を修正
    -   フォロワー読み取りが再試行する前にフラッシュバック エラーを処理せず、クエリ エラー[#43673](https://github.com/pingcap/tidb/issues/43673) @ [あなた06](https://github.com/you06)が発生する問題を修正します。
    -   `ON UPDATE`ステートメントが主キー[#44565](https://github.com/pingcap/tidb/issues/44565) @ [ジグアン](https://github.com/zyguan)を正しく更新しない場合、データとインデックスが矛盾する問題を修正します。
    -   MySQL 8.0.28 以降のバージョン[#43987](https://github.com/pingcap/tidb/issues/43987) @ [ヤンケオ](https://github.com/YangKeao)の上限と一致するように、 `UNIX_TIMESTAMP()`関数の上限を`3001-01-19 03:14:07.999999 UTC`に変更します。
    -   インジェストモード[#44137](https://github.com/pingcap/tidb/issues/44137) @ [タンジェンタ](https://github.com/tangenta)でインデックスの追加が失敗する問題を修正
    -   ロールバック状態で DDL タスクをキャンセルすると、関連するメタデータ[#44143](https://github.com/pingcap/tidb/issues/44143) @ [wjhuang2016](https://github.com/wjhuang2016)でエラーが発生する問題を修正します。
    -   カーソルフェッチで`memTracker`を使用するとメモリリーク[#44254](https://github.com/pingcap/tidb/issues/44254) @ [ヤンケオ](https://github.com/YangKeao)が発生する問題を修正
    -   データベースを削除すると GC の進行が遅くなる問題を修正[#33069](https://github.com/pingcap/tidb/issues/33069) @ [ティエンチャイアマオ](https://github.com/tiancaiamao)
    -   インデックス結合[#43686](https://github.com/pingcap/tidb/issues/43686) @ [アイリンキッド](https://github.com/AilinKid) @ [むじょん](https://github.com/mjonss)のプローブフェーズでパーティションテーブル内の対応する行が見つからない場合、TiDB がエラーを返す問題を修正します。
    -   `SUBPARTITION`使用してパーティション テーブル[#41198](https://github.com/pingcap/tidb/issues/41198) [#41200](https://github.com/pingcap/tidb/issues/41200) @ [むじょん](https://github.com/mjonss)を作成するときに警告が表示されない問題を修正します。
    -   `MAX_EXECUTION_TIME`を超えたためにクエリが強制終了された場合、返されるエラー メッセージが MySQL [#43031](https://github.com/pingcap/tidb/issues/43031) @ [ドヴィーデン](https://github.com/dveeden)のエラー メッセージと一致しない問題を修正
    -   `LEADING`ヒントがブロック エイリアス[#44645](https://github.com/pingcap/tidb/issues/44645) @ [qw4990](https://github.com/qw4990)のクエリをサポートしていない問題を修正します。
    -   MySQL [#44574](https://github.com/pingcap/tidb/issues/44574) @ [定義2014](https://github.com/Defined2014)の戻り値と一致するように、 `LAST_INSERT_ID()`関数の戻り値の型を VARCHAR から LONGLONG に変更します。
    -   非相関サブクエリ[#44051](https://github.com/pingcap/tidb/issues/44051) @ [ウィノロス](https://github.com/winoros)を含むステートメントで共通テーブル式 (CTE) を使用すると、誤った結果が返される可能性がある問題を修正します。
    -   結合したテーブルの再配置により不正な外部結合結果[#44314](https://github.com/pingcap/tidb/issues/44314) @ [アイリンキッド](https://github.com/AilinKid)が発生する可能性がある問題を修正
    -   `PREPARE stmt FROM "ANALYZE TABLE xxx"`が`tidb_mem_quota_query` [#44320](https://github.com/pingcap/tidb/issues/44320) @ [クリサン](https://github.com/chrysan)に殺される可能性がある問題を修正

-   TiKV

    -   TiKV が古い悲観的ロックの競合[#13298](https://github.com/tikv/tikv/issues/13298) @ [cfzjywxk](https://github.com/cfzjywxk)を処理するときに、トランザクションが不正な値を返す問題を修正します。
    -   メモリ内の悲観的ロックがフラッシュバックの失敗とデータの不整合を引き起こす可能性がある問題を修正します[#13303](https://github.com/tikv/tikv/issues/13303) @ [Jmポテト](https://github.com/JmPotato)
    -   TiKV が古いリクエスト[#13298](https://github.com/tikv/tikv/issues/13298) @ [cfzjywxk](https://github.com/cfzjywxk)を処理するときにフェア ロックが正しくない可能性がある問題を修正
    -   `autocommit`と`point get replica read`線形化可能性[#14715](https://github.com/tikv/tikv/issues/14715) @ [cfzjywxk](https://github.com/cfzjywxk)を壊す可能性がある問題を修正

-   PD

    -   一部の特殊なケースで冗長レプリカが自動的に修復できない問題を修正[#6573](https://github.com/tikv/pd/issues/6573) @ [ノールーシュ](https://github.com/nolouch)

-   TiFlash

    -   結合ビルド側のデータが非常に大きく、小さな文字列型の列[#7416](https://github.com/pingcap/tiflash/issues/7416) @ [イービン87](https://github.com/yibin87)が多数含まれている場合、クエリが必要以上のメモリを消費する可能性がある問題を修正します。

-   ツール

    -   バックアップと復元 (BR)

        -   `checksum mismatch`が[#44472](https://github.com/pingcap/tidb/issues/44472) @ [レヴルス](https://github.com/Leavrth)と誤って報告される場合がある問題を修正
        -   `resolved lock timeout`が[#43236](https://github.com/pingcap/tidb/issues/43236) @ [ユジュンセン](https://github.com/YuJuncen)と誤って報告される場合がある問題を修正
        -   統計情報[#44490](https://github.com/pingcap/tidb/issues/44490) @ [タンジェンタ](https://github.com/tangenta)を復元するときに TiDB がpanic可能性がある問題を修正

    -   TiCDC

        -   Resolved TSが正常に進まない場合がある問題を修正[#8963](https://github.com/pingcap/tiflow/issues/8963) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   Avro または CSV プロトコルが使用されている場合、 `UPDATE`操作で古い値を出力できない問題を修正[#9086](https://github.com/pingcap/tiflow/issues/9086) @ [3エースショーハンド](https://github.com/3AceShowHand)
        -   データを Kafka [#8959](https://github.com/pingcap/tiflow/issues/8959) @ [こんにちはラスティン](https://github.com/hi-rustin)にレプリケートするときに、ダウンストリーム メタデータを頻繁に読み取ることによって引き起こされる過度のダウンストリーム プレッシャーの問題を修正します。
        -   データを TiDB または MySQL [#9180](https://github.com/pingcap/tiflow/issues/9180) @ [東門](https://github.com/asddongmen)にレプリケートするときに、ダウンストリーム双方向レプリケーション関連の変数を頻繁に設定することによって発生するダウンストリーム ログが多すぎる問題を修正します。
        -   PD ノードのクラッシュにより TiCDC ノードが再起動される問題を修正します[#8868](https://github.com/pingcap/tiflow/issues/8868) @ [東門](https://github.com/asddongmen)
        -   TiCDC がダウンストリーム Kafka-on-Pulsar [#8892](https://github.com/pingcap/tiflow/issues/8892) @ [こんにちはラスティン](https://github.com/hi-rustin)でチェンジフィードを作成できない問題を修正

    -   TiDB Lightning

        -   `experimental.allow-expression-index`が有効で、デフォルト値が UUID [#44497](https://github.com/pingcap/tidb/issues/44497) @ [リチュンジュ](https://github.com/lichunzhu)である場合のTiDB Lightningpanicの問題を修正
        -   データ ファイル[#43195](https://github.com/pingcap/tidb/issues/43195) @ [ランス6716](https://github.com/lance6716)の分割中にタスクが終了したときのTiDB Lightningpanicの問題を修正しました。

## 貢献者 {#contributors}

TiDB コミュニティの以下の貢献者に感謝いたします。

-   [asjdf](https://github.com/asjdf)
-   [ブラックティア23](https://github.com/blacktear23)
-   [キャヴァンスー](https://github.com/Cavan-xu)
-   [ダラエス](https://github.com/darraes)
-   [デモマニト](https://github.com/demoManito)
-   [ジサム](https://github.com/dhysum)
-   [ハッピーアンクル](https://github.com/HappyUncle)
-   [ジフフスト](https://github.com/jiyfhust)
-   [L-カエデ](https://github.com/L-maple)
-   [ニュリク](https://github.com/nyurik)
-   [SeigeC](https://github.com/SeigeC)
-   [タンジンユ97](https://github.com/tangjingyu97)
