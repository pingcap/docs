---
title: TiDB 7.2.0 Release Notes
summary: TiDB 7.2.0 の新機能、互換性の変更、改善、バグ修正について説明します。
---

# TiDB 7.2.0 リリースノート {#tidb-7-2-0-release-notes}

発売日: 2023年6月29日

TiDB バージョン: 7.2.0

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v7.2/quick-start-with-tidb)

7.2.0 では、次の主要な機能と改善が導入されています。

<table><thead><tr><th>カテゴリ</th><th>特徴</th><th>説明</th></tr></thead><tbody><tr><td rowspan="2">スケーラビリティとパフォーマンス</td><td>リソース グループは、 <a href="https://docs.pingcap.com/tidb/v7.2/tidb-resource-control#manage-queries-that-consume-more-resources-than-expected-runaway-queries">ランナウェイ クエリの管理を</a>サポートします (実験的)</td><td>クエリのタイムアウトをより細かく管理できるようになり、クエリの分類に基づいてさまざまな動作が可能になります。指定したしきい値を満たすクエリは、優先順位を下げたり終了したりできます。</td></tr><tr><td> TiFlash は<a href="https://docs.pingcap.com/tidb/v7.2/tiflash-pipeline-model">パイプライン実行モデル</a>をサポートします (実験的)</td><td> TiFlash は、スレッド リソース制御を最適化するためにパイプライン実行モデルをサポートしています。</td></tr><tr><td rowspan="1">構文</td><td>データインポート用の新しい SQL ステートメント<a href="https://docs.pingcap.com/tidb/v7.2/sql-statement-import-into">IMPORT INTO</a>をサポートします (実験的)</td><td> TiDB Lightningの導入とメンテナンスを簡素化するために、TiDB では新しい SQL ステートメント<code>IMPORT INTO</code>導入されました。このステートメントは、Amazon S3 または Google Cloud Storage (GCS) から TiDB への直接リモートインポートを含む、 TiDB Lightningの物理インポートモードを統合します。</td></tr><tr><td rowspan="2"> DB 操作と可観測性</td><td>DDL は<a href="https://docs.pingcap.com/tidb/v7.2/ddl-introduction#ddl-related-commands">一時停止および再開操作</a>をサポートします (実験的)</td><td>この新しい機能により、インデックス作成などのリソースを大量に消費する DDL 操作を一時的に停止して、リソースを節約し、オンライン トラフィックへの影響を最小限に抑えることができます。準備ができたら、キャンセルして再起動する必要なく、これらの操作をシームレスに再開できます。この機能により、リソースの使用率が向上し、ユーザー エクスペリエンスが向上し、スキーマの変更が効率化されます。</td></tr></tbody></table>

## 機能の詳細 {#feature-details}

### パフォーマンス {#performance}

-   次の2つの[ウィンドウ関数](/tiflash/tiflash-supported-pushdown-calculations.md) TiFlash [＃7427](https://github.com/pingcap/tiflash/issues/7427) @ [翻訳者](https://github.com/xzhangxian1008)に押し下げることをサポートします

    -   `FIRST_VALUE`
    -   `LAST_VALUE`

-   TiFlashはパイプライン実行モデル（実験的） [＃6518](https://github.com/pingcap/tiflash/issues/6518) @ [シーライズ](https://github.com/SeaRise)をサポートします

    v7.2.0 より前では、 TiFlashエンジンの各タスクは実行中に個別にスレッド リソースを要求する必要があります。TiFlashはタスクの数を制御してスレッド リソースの使用を制限し、過剰使用を防止しますが、この問題を完全に排除することはできませんでした。この問題に対処するために、v7.2.0 以降、 TiFlash はパイプライン実行モデルを導入しています。このモデルは、すべてのスレッド リソースを集中管理し、タスク実行を均一にスケジュールして、スレッド リソースの使用率を最大化しながらリソースの過剰使用を回避します。パイプライン実行モデルを有効または無効にするには、 [`tidb_enable_tiflash_pipeline_model`](https://docs.pingcap.com/tidb/v7.2/system-variables#tidb_enable_tiflash_pipeline_model-new-in-v720)システム変数を変更します。

    詳細については[ドキュメント](/tiflash/tiflash-pipeline-model.md)参照してください。

-   TiFlashはスキーマレプリケーションのレイテンシーを短縮します[＃7630](https://github.com/pingcap/tiflash/issues/7630) @ [ホンユンヤン](https://github.com/hongyunyan)

    テーブルのスキーマが変更されると、 TiFlash は最新のスキーマを TiKV からタイムリーに複製する必要があります。v7.2.0 より前では、 TiFlash がテーブル データにアクセスし、データベース内のテーブル スキーマの変更を検出すると、 TiFlash は、 TiFlashレプリカのないテーブルも含め、このデータベース内のすべてのテーブルのスキーマを再度複製する必要があります。その結果、多数のテーブルがあるデータベースでは、 TiFlash を使用して 1 つのテーブルからデータを読み取るだけでよい場合でも、 TiFlash がすべてのテーブルのスキーマ複製を完了するまで待機するレイテンシーが長くなる可能性があります。

    v7.2.0 では、 TiFlash はスキーマ レプリケーション メカニズムを最適化し、 TiFlashレプリカを持つテーブルのスキーマのレプリケーションのみをサポートします。TiFlash レプリカを持つテーブルでスキーマの変更が検出されると、 TiFlash はそのテーブルのスキーマのみをレプリケーションします。これにより、 TiFlashのスキーマ レプリケーションのレイテンシーが短縮され、 TiFlashデータ レプリケーションに対する DDL 操作の影響が最小限に抑えられます。この最適化は自動的に適用され、手動での構成は必要ありません。

-   統計収集のパフォーマンスを向上させる[＃44725](https://github.com/pingcap/tidb/issues/44725) @ [翻訳者](https://github.com/xuyifangreeneyes)

    TiDB v7.2.0 では、統計収集戦略が最適化され、重複した情報やオプティマイザーにとって価値の低い情報がスキップされます。統計収集の全体的な速度が 30% 向上しました。この改善により、TiDB はデータベースの統計をよりタイムリーに更新できるようになり、生成された実行プランがより正確になり、データベース全体のパフォーマンスが向上します。

    デフォルトでは、統計収集では`JSON` 、 `BLOB` 、 `MEDIUMBLOB` 、および`LONGBLOB`タイプの列がスキップされます。 [`tidb_analyze_skip_column_types`](/system-variables.md#tidb_analyze_skip_column_types-new-in-v720)システム変数を設定することで、デフォルトの動作を変更できます。 TiDB は、 `JSON` 、 `BLOB` 、および`TEXT`タイプとそのサブタイプのスキップをサポートしています。

    詳細については[ドキュメント](/system-variables.md#tidb_analyze_skip_column_types-new-in-v720)参照してください。

-   データとインデックスの一貫性チェックのパフォーマンスを向上[＃43693](https://github.com/pingcap/tidb/issues/43693) @ [翻訳:](https://github.com/wjhuang2016)

    [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md)ステートメントは、テーブル内のデータとそれに対応するインデックス間の一貫性をチェックするために使用されます。v7.2.0 では、TiDB はデータの一貫性をチェックする方法を最適化し、 [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md)の実行効率を大幅に向上させました。大量のデータを扱うシナリオでは、この最適化によりパフォーマンスが数百倍向上します。

    最適化はデフォルトで有効（デフォルトでは[`tidb_enable_fast_table_check`](/system-variables.md#tidb_enable_fast_table_check-new-in-v720)または`ON` ）になっており、大規模なテーブルでのデータ整合性チェックに必要な時間を大幅に短縮し、運用効率を高めます。

    詳細については[ドキュメント](/system-variables.md#tidb_enable_fast_table_check-new-in-v720)参照してください。

### 信頼性 {#reliability}

-   予想よりも多くのリソースを消費するクエリを自動的に管理する (実験的) [＃43691](https://github.com/pingcap/tidb/issues/43691) @ [コナー1996](https://github.com/Connor1996) @ [キャビンフィーバーB](https://github.com/CabinfeverB) @ [栄光](https://github.com/glorv) @ [ヒューシャープ](https://github.com/HuSharp) @ [ノルーシュ](https://github.com/nolouch)

    データベースの安定性に対する最も一般的な課題は、突然の SQL パフォーマンスの問題によってデータベース全体のパフォーマンスが低下することです。SQL パフォーマンスの問題には、十分にテストされていない新しい SQL ステートメント、データ量の大幅な変更、実行プランの突然の変更など、多くの原因があります。これらの問題を根本的に完全に回避することは困難です。TiDB v7.2.0 では、予想よりも多くのリソースを消費するクエリを管理する機能が提供されています。この機能により、パフォーマンスの問題が発生した場合の影響範囲を迅速に縮小できます。

    これらのクエリを管理するには、リソース グループのクエリの最大実行時間を設定できます。クエリの実行時間がこの制限を超えると、クエリは自動的に優先順位が下げられるか、キャンセルされます。また、テキストまたは実行プランによって識別されたクエリをすぐに照合する期間を設定することもできます。これにより、識別フェーズ中に問題のあるクエリが同時に実行され、予想よりも多くのリソースが消費されるのを防ぐことができます。

    予想よりも多くのリソースを消費するクエリを自動的に管理することで、予期しないクエリ パフォーマンスの問題に迅速に対応するための効果的な手段が提供されます。この機能により、問題がデータベース全体のパフォーマンスに与える影響を軽減し、データベースの安定性を向上させることができます。

    詳細については[ドキュメント](/tidb-resource-control.md#manage-queries-that-consume-more-resources-than-expected-runaway-queries)参照してください。

-   履歴実行計画に従ってバインディングを作成する機能を強化する[＃39199](https://github.com/pingcap/tidb/issues/39199) @ [qw4990](https://github.com/qw4990)

    TiDB v7.2.0 では、 [過去の実行計画に従ってバインディングを作成する](/sql-plan-management.md#create-a-binding-according-to-a-historical-execution-plan)の機能が強化されています。この機能により、複雑なステートメントの解析とバインディングのプロセスが改善され、バインディングがより安定し、次の新しいヒントがサポートされます。

    -   [`AGG_TO_COP()`](/optimizer-hints.md#agg_to_cop)
    -   [`LIMIT_TO_COP()`](/optimizer-hints.md#limit_to_cop)
    -   [`ORDER_INDEX`](/optimizer-hints.md#order_indext1_name-idx1_name--idx2_name-)
    -   [`NO_ORDER_INDEX()`](/optimizer-hints.md#no_order_indext1_name-idx1_name--idx2_name-)

    詳細については[ドキュメント](/sql-plan-management.md)参照してください。

-   オプティマイザの動作を細かく制御するためのオプティマイザ修正制御メカニズムを導入する[＃43169](https://github.com/pingcap/tidb/issues/43169) @ [時間と運命](https://github.com/time-and-fate)

    より合理的な実行プランを生成するために、TiDB オプティマイザーの動作は製品の反復を通じて進化します。ただし、特定のシナリオでは、変更によってパフォーマンスが低下する可能性があります。TiDB v7.2.0 では、オプティマイザーのきめ細かい動作の一部を制御できるオプティマイザー修正コントロールが導入されています。これにより、いくつかの新しい変更をロールバックまたは制御できます。

    制御可能な各動作は、修正番号に対応する GitHub の問題によって説明されています。制御可能なすべての動作は[オプティマイザー修正コントロール](/optimizer-fix-controls.md)にリストされています。動作制御を実現するには、 [`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-new-in-v653-and-v710)システム変数を設定することで、1 つ以上の動作のターゲット値を設定できます。

    オプティマイザー修正制御メカニズムは、TiDB オプティマイザーをきめ細かいレベルで制御するのに役立ちます。アップグレード プロセスによって発生するパフォーマンスの問題を修正する新しい手段を提供し、TiDB の安定性を向上させます。

    詳細については[ドキュメント](/optimizer-fix-controls.md)参照してください。

-   軽量統計初期化が一般提供 (GA) [＃42160](https://github.com/pingcap/tidb/issues/42160) @ [翻訳者](https://github.com/xuyifangreeneyes)に開始

    v7.2.0 以降、軽量統計初期化機能が GA になります。軽量統計初期化により、起動時にロードする必要がある統計の数が大幅に削減され、統計のロード速度が向上します。この機能により、複雑なランタイム環境での TiDB の安定性が向上し、TiDB ノードの再起動時にサービス全体に与える影響が軽減されます。

    v7.2.0 以降のバージョンの新しく作成されたクラスターの場合、TiDB はデフォルトで TiDB の起動時に軽量統計をロードし、ロードが完了するまで待ってからサービスを提供します。以前のバージョンからアップグレードされたクラスターの場合、この機能を有効にするには、TiDB 構成項目[`lite-init-stats`](/tidb-configuration-file.md#lite-init-stats-new-in-v710)および[`force-init-stats`](/tidb-configuration-file.md#force-init-stats-new-in-v657-and-v710) ～ `true`を設定できます。

    詳細については[ドキュメント](/statistics.md#load-statistics)参照してください。

### 構文 {#sql}

-   `CHECK`制約[＃41711](https://github.com/pingcap/tidb/issues/41711) @ [ふーふー](https://github.com/fzzf678)をサポート

    v7.2.0 以降では、 `CHECK`制約を使用して、指定した条件を満たすようにテーブル内の 1 つ`CHECK`の列の値を制限できます。3 制約がテーブルに追加されると、TiDB はテーブルにデータを挿入または更新する前に、制約が満たされているかどうかを確認します。制約を満たすデータのみを書き込むことができます。

    この機能はデフォルトで無効になっています。有効にするには、 [`tidb_enable_check_constraint`](/system-variables.md#tidb_enable_check_constraint-new-in-v720)システム変数を`ON`に設定します。

    詳細については[ドキュメント](/constraints.md#check)参照してください。

### DB操作 {#db-operations}

-   DDL ジョブは一時停止と再開操作をサポートします (実験的) [＃18015](https://github.com/pingcap/tidb/issues/18015) @ [ゴドゥム](https://github.com/godouxm)

    TiDB v7.2.0 より前では、DDL ジョブの実行中にビジネス ピークが発生した場合、ビジネスへの影響を軽減するために、DDL ジョブを手動でキャンセルすることしかできませんでした。v7.2.0 では、TiDB に DDL ジョブの一時停止および再開操作が導入されています。これらの操作により、ピーク時に DDL ジョブを一時停止し、ピーク終了後に再開できるため、アプリケーション ワークロードへの影響を回避できます。

    たとえば、 `ADMIN PAUSE DDL JOBS`または`ADMIN RESUME DDL JOBS`使用して複数の DDL ジョブを一時停止および再開できます。

    ```sql
    ADMIN PAUSE DDL JOBS 1,2;
    ADMIN RESUME DDL JOBS 1,2;
    ```

    詳細については[ドキュメント](/ddl-introduction.md#ddl-related-commands)参照してください。

### データ移行 {#data-migration}

-   データのインポート効率を大幅に向上させる新しいSQL文`IMPORT INTO`を導入（実験的） [＃42930](https://github.com/pingcap/tidb/issues/42930) @ [D3ハンター](https://github.com/D3Hunter)

    `IMPORT INTO`ステートメントは、 TiDB Lightningの[物理インポートモード](/tidb-lightning/tidb-lightning-physical-import-mode.md)機能を統合します。このステートメントを使用すると、CSV、SQL、PARQUET などの形式のデータを TiDB の空のテーブルにすばやくインポートできます。このインポート方法により、 TiDB Lightningを個別に展開および管理する必要がなくなり、データ インポートの複雑さが軽減され、インポート効率が大幅に向上します。

    Amazon S3 または GCS に保存されているデータ ファイルの場合、 [TiDB 分散実行フレームワーク (DXF)](/tidb-distributed-execution-framework.md)が有効になっていると、 `IMPORT INTO`データ インポート ジョブを複数のサブジョブに分割し、それらを複数の TiDB ノードにスケジュールして並列インポートすることもサポートするため、インポートのパフォーマンスがさらに向上します。

    詳細については[ドキュメント](/sql-statements/sql-statement-import-into.md)参照してください。

-   TiDB Lightningは、Latin-1文字セットのソースファイルをTiDB [＃44434](https://github.com/pingcap/tidb/issues/44434) @ [ランス6716](https://github.com/lance6716)にインポートすることをサポートします。

    この機能により、 TiDB Lightningを使用して Latin-1 文字セットを含むソース ファイルを TiDB に直接インポートできます。 v7.2.0 より前では、このようなファイルをインポートするには追加の前処理または変換が必要でした。 v7.2.0 以降では、 TiDB Lightningインポート タスクを構成するときに`character-set = "latin1"`指定するだけで済みます。その後、 TiDB Lightning はインポート プロセス中に文字セットの変換を自動的に処理し、データの整合性と正確性を確保します。

    詳細については[ドキュメント](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)参照してください。

## 互換性の変更 {#compatibility-changes}

> **注記：**
>
> このセクションでは、v7.1.0 から現在のバージョン (v7.2.0) にアップグレードするときに知っておく必要のある互換性の変更について説明します。v7.0.0 以前のバージョンから現在のバージョンにアップグレードする場合は、中間バージョンで導入された互換性の変更も確認する必要がある可能性があります。

### 行動の変化 {#behavior-changes}

-   更新イベントを処理する際、イベント内で主キーまたは null 以外の一意のインデックス値が変更されると、TiCDC はイベントを削除イベントと挿入イベントに分割します。詳細については、 [ドキュメント](/ticdc/ticdc-split-update-behavior.md#transactions-containing-a-single-update-change)参照してください。

### システム変数 {#system-variables}

| 変数名                                                                                                                                        | タイプを変更   | 説明                                                                                                                                                                                                                                                                        |
| ------------------------------------------------------------------------------------------------------------------------------------------ | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`last_insert_id`](/system-variables.md#last_insert_id)                                                                                    | 修正済み     | MySQL と一致するように最大値を`9223372036854775807`から`18446744073709551615`に変更します。                                                                                                                                                                                                    |
| [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache)                                          | 修正済み     | さらにテストを行った後、デフォルト値を`OFF`から`ON`に変更します。これは、準備されていない実行プラン キャッシュが有効になっていることを意味します。                                                                                                                                                                                            |
| [`tidb_remove_orderby_in_subquery`](/system-variables.md#tidb_remove_orderby_in_subquery-new-in-v610)                                      | 修正済み     | さらにテストを行った後、デフォルト値を`OFF`から`ON`に変更します。つまり、オプティマイザーはサブクエリ内の`ORDER BY`句を削除します。                                                                                                                                                                                               |
| [`tidb_analyze_skip_column_types`](/system-variables.md#tidb_analyze_skip_column_types-new-in-v720)                                        | 新しく追加された | 統計を収集する`ANALYZE`コマンドを実行するときに、統計収集でスキップされる列の種類を制御します。この変数は[`tidb_analyze_version = 2`](/system-variables.md#tidb_analyze_version-new-in-v510)にのみ適用されます。 `ANALYZE TABLE t COLUMNS c1, ..., cn`の構文を使用する場合、指定された列の種類が`tidb_analyze_skip_column_types`に含まれていると、この列の統計は収集されません。 |
| [`tidb_enable_check_constraint`](/system-variables.md#tidb_enable_check_constraint-new-in-v720)                                            | 新しく追加された | `CHECK`制約を有効にするかどうかを制御します。デフォルト値は`OFF`で、この機能は無効であることを意味します。                                                                                                                                                                                                               |
| [`tidb_enable_fast_table_check`](/system-variables.md#tidb_enable_fast_table_check-new-in-v720)                                            | 新しく追加された | チェックサムベースのアプローチを使用して、テーブル内のデータとインデックスの一貫性をすばやくチェックするかどうかを制御します。デフォルト値は`ON`で、この機能が有効であることを意味します。                                                                                                                                                                           |
| [`tidb_enable_tiflash_pipeline_model`](https://docs.pingcap.com/tidb/v7.2/system-variables#tidb_enable_tiflash_pipeline_model-new-in-v720) | 新しく追加された | TiFlashの新しい実行モデル[パイプラインモデル](/tiflash/tiflash-pipeline-model.md)を有効にするかどうかを制御します。デフォルト値は`OFF`で、パイプライン モデルが無効であることを意味します。                                                                                                                                                   |
| [`tidb_expensive_txn_time_threshold`](/system-variables.md#tidb_expensive_txn_time_threshold-new-in-v720)                                  | 新しく追加された | 高価なトランザクションをログに記録するためのしきい値を制御します。デフォルトでは 600 秒です。トランザクションの期間がしきい値を超え、トランザクションがコミットもロールバックもされない場合、そのトランザクションは高価なトランザクションとみなされ、ログに記録されます。                                                                                                                                   |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーションパラメータ                                                                                                                                 | タイプを変更   | 説明                                                                                                                                                                                                                                                                                  |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ティビ            | [`lite-init-stats`](/tidb-configuration-file.md#lite-init-stats-new-in-v710)                                                                    | 修正済み     | さらにテストを行った後、デフォルト値を`false`から`true`に変更します。つまり、TiDB は、初期化の効率を向上させるために、TiDB の起動時にデフォルトで軽量統計初期化を使用します。                                                                                                                                                                                  |
| ティビ            | [`force-init-stats`](/tidb-configuration-file.md#force-init-stats-new-in-v657-and-v710)                                                         | 修正済み     | デフォルト値を`false`から`true`に変更して[`lite-init-stats`](/tidb-configuration-file.md#lite-init-stats-new-in-v710)に合わせます。つまり、TiDB は、起動時にサービスを提供する前に、統計の初期化が完了するまで待機します。                                                                                                                        |
| ティクヴ           | [`rocksdb.[defaultcf|writecf|lockcf].compaction-guard-min-output-file-size`](/tikv-configuration-file.md#compaction-guard-min-output-file-size) | 修正済み     | RocksDB の圧縮タスクのデータ量を削減するために、デフォルト値を`"8MB"`から`"1MB"`に変更します。                                                                                                                                                                                                                          |
| ティクヴ           | [`rocksdb.[defaultcf|writecf|lockcf].optimize-filters-for-memory`](/tikv-configuration-file.md#optimize-filters-for-memory-new-in-v720)         | 新しく追加された | メモリの内部断片化を最小限に抑える Bloom/Ribbon フィルターを生成するかどうかを制御します。                                                                                                                                                                                                                                |
| ティクヴ           | [`rocksdb.[defaultcf|writecf|lockcf].periodic-compaction-seconds`](/tikv-configuration-file.md#periodic-compaction-seconds-new-in-v720)         | 新しく追加された | 定期的な圧縮の時間間隔を制御します。この値より古い更新を含む SST ファイルは圧縮対象として選択され、これらの SST ファイルが元々存在していたレベルと同じレベルに書き換えられます。                                                                                                                                                                                       |
| ティクヴ           | [`rocksdb.[defaultcf|writecf|lockcf].ribbon-filter-above-level`](/tikv-configuration-file.md#ribbon-filter-above-level-new-in-v720)             | 新しく追加された | この値以上のレベルにはリボン フィルターを使用し、この値未満のレベルには非ブロックベースのブルーム フィルターを使用するかどうかを制御します。                                                                                                                                                                                                             |
| ティクヴ           | [`rocksdb.[defaultcf|writecf|lockcf].ttl`](/tikv-configuration-file.md#ttl-new-in-v720)                                                         | 新しく追加された | TTL より古い更新を含む SST ファイルは自動的に圧縮対象として選択されます。                                                                                                                                                                                                                                           |
| TiDB Lightning | `send-kv-pairs`                                                                                                                                 | 非推奨      | v7.2.0 以降、パラメータ`send-kv-pairs`は非推奨になりました。物理インポート モードで TiKV にデータを送信するときに、1 つのリクエストの最大サイズを制御するには、 [`send-kv-size`](/tidb-lightning/tidb-lightning-configuration.md)使用できます。                                                                                                            |
| TiDB Lightning | [`character-set`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)                                                          | 修正済み     | データ インポートでサポートされる文字セットに新しい値オプション`latin1`が導入されました。このオプションを使用すると、Latin-1 文字セットを含むソース ファイルをインポートできます。                                                                                                                                                                                  |
| TiDB Lightning | [`send-kv-size`](/tidb-lightning/tidb-lightning-configuration.md)                                                                               | 新しく追加された | 物理インポート モードで TiKV にデータを送信する際の 1 つのリクエストの最大サイズを指定します。キーと値のペアのサイズが指定されたしきい値に達すると、 TiDB Lightning はそれらを直ちに TiKV に送信します。これにより、大きな幅の広いテーブルをインポートするときにTiDB Lightningノードがメモリ内にキーと値のペアを過剰に蓄積することで発生する OOM の問題を回避できます。このパラメータを調整することで、メモリ使用量とインポート速度のバランスを見つけることができ、インポート プロセスの安定性と効率が向上します。 |
| データ移行          | [`strict-optimistic-shard-mode`](/dm/feature-shard-merge-optimistic.md)                                                                         | 新しく追加された | この構成項目は、TiDB Data Migration v2.0 の DDL シャード マージ動作との互換性を保つために使用されます。この構成項目は、楽観的モードで有効にできます。これを有効にすると、レプリケーション タスクは、タイプ 2 DDL ステートメントに遭遇すると中断されます。複数のテーブルでの DDL 変更間に依存関係があるシナリオでは、タイムリーな中断が発生する可能性があります。上流と下流の間のデータ整合性を確保するには、レプリケーション タスクを再開する前に、各テーブルの DDL ステートメントを手動で処理する必要があります。  |
| ティCDC          | [`sink.protocol`](/ticdc/ticdc-changefeed-config.md)                                                                                            | 修正済み     | ダウンストリームが Kafka の場合、新しい値オプション`"open-protocol"`を導入します。メッセージのエンコードに使用されるプロトコル形式を指定します。                                                                                                                                                                                                |
| ティCDC          | [`sink.delete-only-output-handle-key-columns`](/ticdc/ticdc-changefeed-config.md)                                                               | 新しく追加された | DELETE イベントの出力を指定します。このパラメータは、プロトコル`"canal-json"`および`"open-protocol"`でのみ有効です。デフォルト値は`false`で、すべての列を出力することを意味します。 `true`に設定すると、主キー列または一意のインデックス列のみが出力されます。                                                                                                                           |

## 改善点 {#improvements}

-   ティビ

    -   インデックススキャン範囲を構築するロジックを最適化し、複雑な条件をインデックススキャン範囲[＃41572](https://github.com/pingcap/tidb/issues/41572) [＃44389](https://github.com/pingcap/tidb/issues/44389) @ [翻訳者](https://github.com/xuyifangreeneyes)に変換できるようにします。
    -   新しい監視メトリック`Stale Read OPS`と`Stale Read Traffic` [＃43325](https://github.com/pingcap/tidb/issues/43325) @ [あなた06](https://github.com/you06)を追加
    -   古い読み取りの再試行リーダーがロックに遭遇すると、TiDBはロックを解決した後、リーダーで強制的に再試行し、不要なオーバーヘッドを回避します[＃43659](https://github.com/pingcap/tidb/issues/43659) @ [あなた06](https://github.com/you06)
    -   推定時間を使用して古い読み取りtsを計算し、古い読み取り[＃44215](https://github.com/pingcap/tidb/issues/44215) @ [あなた06](https://github.com/you06)のオーバーヘッドを削減します。
    -   長時間実行されるトランザクションのログとシステム変数を追加する[＃41471](https://github.com/pingcap/tidb/issues/41471) @ [クレイジーcs520](https://github.com/crazycs520)
    -   圧縮された MySQL プロトコルを介して TiDB に接続することをサポートします。これにより、低帯域幅ネットワークでのデータ集約型クエリのパフォーマンスが向上し、帯域幅コストが節約されます。これは`zlib`と`zstd`ベースの両方の圧縮をサポートします[＃22605](https://github.com/pingcap/tidb/issues/22605) @ [ドヴェーデン](https://github.com/dveeden)
    -   `utf8`と`utf8bm3`両方を従来の 3 バイト UTF-8 文字セット エンコーディングとして認識します。これにより、従来の UTF-8 エンコーディングを持つテーブルを MySQL 8.0 から TiDB [＃26226](https://github.com/pingcap/tidb/issues/26226) @ [ドヴェーデン](https://github.com/dveeden)に移行しやすくなります。
    -   `UPDATE`ステートメント[＃44751](https://github.com/pingcap/tidb/issues/44751) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)での割り当てに`:=`使用することをサポートします

-   ティクヴ

    -   `pd.retry-interval` [＃14964](https://github.com/tikv/tikv/issues/14964) @ [rleungx](https://github.com/rleungx)を使用した接続要求の失敗などのシナリオでの PD 接続の再試行間隔の構成をサポートします。
    -   グローバルリソース使用量[＃14604](https://github.com/tikv/tikv/issues/14604) @ [コナー1996](https://github.com/Connor1996)を組み込むことでリソース制御スケジューリングアルゴリズムを最適化します
    -   `check_leader`リクエストに gzip 圧縮を使用してトラフィックを削減[＃14553](https://github.com/tikv/tikv/issues/14553) @ [あなた06](https://github.com/you06)
    -   `check_leader`リクエスト[＃14658](https://github.com/tikv/tikv/issues/14658) @ [あなた06](https://github.com/you06)の関連メトリックを追加
    -   TiKV が書き込みコマンド[＃12362](https://github.com/tikv/tikv/issues/12362) @ [翻訳](https://github.com/cfzjywxk)を処理する際の詳細な時間情報を提供する

-   PD

    -   他のリクエストの影響を防ぐために、PDリーダー選出には別のgRPC接続を使用する[＃6403](https://github.com/tikv/pd/issues/6403) @ [rleungx](https://github.com/rleungx)
    -   マルチリージョンシナリオでのホットスポットの問題を軽減するために、バケット分割をデフォルトで有効にする[＃6433](https://github.com/tikv/pd/issues/6433) @ [バッファフライ](https://github.com/bufferflies)

-   ツール

    -   バックアップと復元 (BR)

        -   共有アクセス署名 (SAS) [＃44199](https://github.com/pingcap/tidb/issues/44199) @ [リーヴルス](https://github.com/Leavrth)による Azure Blob Storage へのアクセスをサポート

    -   ティCDC

        -   オブジェクトstorageサービスへのレプリケーションのシナリオでDDL操作が発生したときにデータファイルが格納されるディレクトリの構造を最適化します[＃8891](https://github.com/pingcap/tiflow/issues/8891) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)
        -   Kafka [＃8865](https://github.com/pingcap/tiflow/issues/8865) @ [ハイラスティン](https://github.com/Rustin170506)へのレプリケーションのシナリオで OAUTHBEARER 認証をサポートする
        -   Kafka [＃9143](https://github.com/pingcap/tiflow/issues/9143) @ [3エースショーハンド](https://github.com/3AceShowHand)へのレプリケーションのシナリオで`DELETE`操作のハンドルキーのみを出力するオプションを追加します

    -   TiDB データ移行 (DM)

        -   MySQL 8.0 の圧縮されたバイナリログを増分レプリケーションのデータソースとして読み取る機能をサポート[＃6381](https://github.com/pingcap/tiflow/issues/6381) @ [ドヴェーデン](https://github.com/dveeden)

    -   TiDB Lightning

        -   リーダー切り替え[＃44263](https://github.com/pingcap/tidb/issues/44263) @ [ランス6716](https://github.com/lance6716)によるエラーを回避するために、インポート中の再試行メカニズムを最適化します。
        -   インポート後にSQLでチェックサムを検証し、検証[＃41941](https://github.com/pingcap/tidb/issues/41941) @ [GMHDBJD](https://github.com/GMHDBJD)の安定性を向上
        -   ワイドテーブル[＃43853](https://github.com/pingcap/tidb/issues/43853) @ [D3ハンター](https://github.com/D3Hunter)をインポートする際のTiDB Lightning OOM の問題を最適化

## バグ修正 {#bug-fixes}

-   ティビ

    -   CTE を含むクエリによって TiDB がハングする問題を修正[＃43749](https://github.com/pingcap/tidb/issues/43749) [＃36896](https://github.com/pingcap/tidb/issues/36896) @ [グオシャオゲ](https://github.com/guo-shaoge)
    -   `min, max`クエリ結果が正しくない問題を修正[＃43805](https://github.com/pingcap/tidb/issues/43805) @ [うわー](https://github.com/wshwsh12)
    -   `SHOW PROCESSLIST`文がサブクエリ時間が長い文のトランザクションの TxnStart を表示できない問題を修正[＃40851](https://github.com/pingcap/tidb/issues/40851) @ [クレイジーcs520](https://github.com/crazycs520)
    -   コプロセッサータスク[＃43365](https://github.com/pingcap/tidb/issues/43365) @ [あなた06](https://github.com/you06)に`TxnScope`がないため、古い読み取りグローバル最適化が有効にならない問題を修正しました。
    -   フォロワー読み取りが再試行前にフラッシュバック エラーを処理せず、クエリ エラー[＃43673](https://github.com/pingcap/tidb/issues/43673) @ [あなた06](https://github.com/you06)が発生する問題を修正しました。
    -   `ON UPDATE`ステートメントが主キー[＃44565](https://github.com/pingcap/tidb/issues/44565) @ [ジグアン](https://github.com/zyguan)を正しく更新しない場合にデータとインデックスが不整合になる問題を修正しました
    -   権限テーブル[＃41048](https://github.com/pingcap/tidb/issues/41048) @ [bb7133](https://github.com/bb7133)の一部の列における大文字と小文字の区別の問題を修正
    -   MySQL 8.0.28以降のバージョン[＃43987](https://github.com/pingcap/tidb/issues/43987) @ [ヤンケオ](https://github.com/YangKeao)と一致するように、 `UNIX_TIMESTAMP()`関数の上限を`3001-01-19 03:14:07.999999 UTC`に変更します。
    -   取り込みモード[＃44137](https://github.com/pingcap/tidb/issues/44137) @ [タンジェンタ](https://github.com/tangenta)でインデックスの追加が失敗する問題を修正
    -   ロールバック状態で DDL タスクをキャンセルすると、関連するメタデータ[＃44143](https://github.com/pingcap/tidb/issues/44143) @ [翻訳:](https://github.com/wjhuang2016)にエラーが発生する問題を修正しました
    -   カーソルフェッチで`memTracker`使用するとメモリリークが発生する問題を修正[＃44254](https://github.com/pingcap/tidb/issues/44254) @ [ヤンケオ](https://github.com/YangKeao)
    -   データベースを削除すると GC の進行が遅くなる問題を修正[＃33069](https://github.com/pingcap/tidb/issues/33069) @ [天菜まお](https://github.com/tiancaiamao)
    -   インデックス結合[＃43686](https://github.com/pingcap/tidb/issues/43686) @ [アイリンキッド](https://github.com/AilinKid) @ [ミョンス](https://github.com/mjonss)のプローブフェーズでパーティションテーブル内の対応する行が見つからない場合に TiDB がエラーを返す問題を修正しました。
    -   `SUBPARTITION`使用してパーティション テーブル[＃41198](https://github.com/pingcap/tidb/issues/41198) [＃41200](https://github.com/pingcap/tidb/issues/41200) @ [ミョンス](https://github.com/mjonss)を作成するときに警告が表示されない問題を修正しました
    -   クエリが`MAX_EXECUTION_TIME`超えたために強制終了された場合に返されるエラーメッセージが MySQL [＃43031](https://github.com/pingcap/tidb/issues/43031) @ [ドヴェーデン](https://github.com/dveeden)のものと一致しない問題を修正しました。
    -   `LEADING`ヒントがブロック エイリアス[＃44645](https://github.com/pingcap/tidb/issues/44645) @ [qw4990](https://github.com/qw4990)のクエリをサポートしない問題を修正しました
    -   `LAST_INSERT_ID()`関数の戻り値の型を VARCHAR から LONGLONG に変更して、MySQL [＃44574](https://github.com/pingcap/tidb/issues/44574) @ [定義2014](https://github.com/Defined2014)の戻り値と一致するようにします。
    -   非相関サブクエリを含むステートメントで共通テーブル式 (CTE) を使用すると、誤った結果が返される可能性がある問題を修正しました[＃44051](https://github.com/pingcap/tidb/issues/44051) @ [ウィノロス](https://github.com/winoros)
    -   結合したテーブルの再配置により外部結合結果が不正確になる可能性がある問題を修正[＃44314](https://github.com/pingcap/tidb/issues/44314) @ [アイリンキッド](https://github.com/AilinKid)
    -   `PREPARE stmt FROM "ANALYZE TABLE xxx"` `tidb_mem_quota_query` [＃44320](https://github.com/pingcap/tidb/issues/44320) @ [クリサン](https://github.com/chrysan)によって殺される可能性がある問題を修正

-   ティクヴ

    -   TiKV が古い悲観的ロックの競合[＃13298](https://github.com/tikv/tikv/issues/13298) @ [翻訳](https://github.com/cfzjywxk)を処理するときにトランザクションが誤った値を返す問題を修正しました
    -   メモリ内の悲観的ロックによりフラッシュバックの失敗やデータの不整合が発生する可能性がある問題を修正[＃13303](https://github.com/tikv/tikv/issues/13303) @ [じゃがいも](https://github.com/JmPotato)
    -   TiKV が古いリクエスト[＃13298](https://github.com/tikv/tikv/issues/13298) @ [翻訳](https://github.com/cfzjywxk)を処理するときにフェア ロックが正しくない可能性がある問題を修正しました
    -   `autocommit`と`point get replica read` [＃14715](https://github.com/tikv/tikv/issues/14715) @ [翻訳](https://github.com/cfzjywxk)の線形化可能性を壊す可能性がある問題を修正

-   PD

    -   一部の特殊なケースで冗長レプリカを自動的に修復できない問題を修正[＃6573](https://github.com/tikv/pd/issues/6573) @ [ノルーシュ](https://github.com/nolouch)

-   TiFlash

    -   結合ビルド側のデータが非常に大きく、小さな文字列型の列が多数含まれている場合、クエリが必要以上にメモリを消費する可能性がある問題を修正しました[＃7416](https://github.com/pingcap/tiflash/issues/7416) @ [いびん87](https://github.com/yibin87)

-   ツール

    -   バックアップと復元 (BR)

        -   `checksum mismatch`が誤って報告される場合がある問題を修正[＃44472](https://github.com/pingcap/tidb/issues/44472) @ [リーヴルス](https://github.com/Leavrth)
        -   `resolved lock timeout`が誤って報告される場合がある問題を修正[＃43236](https://github.com/pingcap/tidb/issues/43236) @ [ユジュンセン](https://github.com/YuJuncen)
        -   統計情報[＃44490](https://github.com/pingcap/tidb/issues/44490) @ [タンジェンタ](https://github.com/tangenta)を復元するときに TiDB がpanicになる可能性がある問題を修正

    -   ティCDC

        -   解決済みのTSが一部のケースで正しく進まない問題を修正[＃8963](https://github.com/pingcap/tiflow/issues/8963) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)
        -   Avro または CSV プロトコルが使用されている場合に`UPDATE`操作で古い値を出力できない問題を修正[＃9086](https://github.com/pingcap/tiflow/issues/9086) @ [3エースショーハンド](https://github.com/3AceShowHand)
        -   Kafka [＃8959](https://github.com/pingcap/tiflow/issues/8959) @ [ハイラスティン](https://github.com/Rustin170506)にデータを複製するときに、ダウンストリーム メタデータを頻繁に読み取ることによって発生するダウンストリームの過度の負荷の問題を修正しました。
        -   TiDB または MySQL [＃9180](https://github.com/pingcap/tiflow/issues/9180) @ [アズドンメン](https://github.com/asddongmen)にデータを複製するときに、下流の双方向レプリケーション関連の変数を頻繁に設定することによって発生する下流ログが多すぎる問題を修正しました。
        -   PDノードがクラッシュするとTiCDCノードが[＃8868](https://github.com/pingcap/tiflow/issues/8868) @ [アズドンメン](https://github.com/asddongmen)で再起動する問題を修正
        -   TiCDC が下流の Kafka-on-Pulsar [＃8892](https://github.com/pingcap/tiflow/issues/8892) @ [ハイラスティン](https://github.com/Rustin170506)で変更フィードを作成できない問題を修正しました

    -   TiDB Lightning

        -   `experimental.allow-expression-index`が有効でデフォルト値が UUID [＃44497](https://github.com/pingcap/tidb/issues/44497) @ [リチュンジュ](https://github.com/lichunzhu)の場合のTiDB Lightningpanic問題を修正しました
        -   データファイル[＃43195](https://github.com/pingcap/tidb/issues/43195) @ [ランス6716](https://github.com/lance6716)を分割中にタスクが終了したときに発生するTiDB Lightningpanicの問題を修正しました。

## 寄稿者 {#contributors}

TiDB コミュニティの以下の貢献者に感謝いたします。

-   [アスジェ](https://github.com/asjdf)
-   [えり](https://github.com/blacktear23)
-   [カヴァン・シュ](https://github.com/Cavan-xu)
-   [ダラエス](https://github.com/darraes)
-   [デモマニト](https://github.com/demoManito)
-   [ディサム](https://github.com/dhysum)
-   [ハッピーv587](https://github.com/happy-v587)
-   [ジフハウス](https://github.com/jiyfhust)
-   [L-メープル](https://github.com/L-maple)
-   [ニュリク](https://github.com/nyurik)
-   [シージC](https://github.com/SeigeC)
-   [タンジンギュ97](https://github.com/tangjingyu97)
