---
title: TiDB 7.2.0 Release Notes
summary: TiDB 7.2.0 の新機能、互換性の変更、改善点、バグ修正について説明します。
---

# TiDB 7.2.0 リリースノート {#tidb-7-2-0-release-notes}

発売日：2023年6月29日

TiDB バージョン: 7.2.0

クイックアクセス: [クイックスタート](https://docs-archive.pingcap.com/tidb/v7.2/quick-start-with-tidb)

7.2.0 では、次の主な機能と改善が導入されています。

<table><thead><tr><th>カテゴリ</th><th>特徴</th><th>説明</th></tr></thead><tbody><tr><td rowspan="2">スケーラビリティとパフォーマンス</td><td>リソース グループは<a href="https://docs-archive.pingcap.com/tidb/v7.2/tidb-resource-control#manage-queries-that-consume-more-resources-than-expected-runaway-queries">、暴走クエリの管理</a>をサポートします (実験的)</td><td>クエリのタイムアウトをより細かく管理できるようになり、クエリの分類に基づいて異なる動作が可能になります。指定したしきい値に達したクエリは、優先順位を下げたり、終了させたりできます。</td></tr><tr><td> TiFlash は<a href="https://docs-archive.pingcap.com/tidb/v7.2/tiflash-pipeline-model">パイプライン実行モデル</a>をサポートしています (実験的)</td><td> TiFlash は、スレッド リソース制御を最適化するためにパイプライン実行モデルをサポートしています。</td></tr><tr><td rowspan="1"> SQL</td><td>データインポート用の新しい SQL ステートメント<a href="https://docs-archive.pingcap.com/tidb/v7.2/sql-statement-import-into">IMPORT INTO</a>をサポートします (実験的)</td><td> TiDB Lightningの導入とメンテナンスを簡素化するために、TiDB では新しい SQL ステートメント<code>IMPORT INTO</code>が導入されました。このステートメントは、Amazon S3 または Google Cloud Storage (GCS) から TiDB への直接リモートインポートを含む、 TiDB Lightningの物理インポートモードを統合します。</td></tr><tr><td rowspan="2"> DB操作と可観測性</td><td>DDL は<a href="https://docs-archive.pingcap.com/tidb/v7.2/ddl-introduction#ddl-related-commands">一時停止と再開の操作</a>をサポートします (実験的)</td><td>この新機能により、インデックス作成などのリソースを大量に消費するDDL操作を一時的に停止することで、リソースを節約し、オンライントラフィックへの影響を最小限に抑えることができます。これらの操作は、キャンセルして再起動することなく、準備ができたらシームレスに再開できます。この機能により、リソース利用率が向上し、ユーザーエクスペリエンスが向上し、スキーマ変更が効率化されます。</td></tr></tbody></table>

## 機能の詳細 {#feature-details}

### パフォーマンス {#performance}

-   次の2つの[ウィンドウ関数](/tiflash/tiflash-supported-pushdown-calculations.md) TiFlash [＃7427](https://github.com/pingcap/tiflash/issues/7427) @ [xzhangxian1008](https://github.com/xzhangxian1008)に押し下げることをサポートします

    -   `FIRST_VALUE`
    -   `LAST_VALUE`

-   TiFlashはパイプライン実行モデル（実験的） [＃6518](https://github.com/pingcap/tiflash/issues/6518) @ [シーライズ](https://github.com/SeaRise)をサポートしています

    v7.2.0より前のバージョンでは、 TiFlashエンジンの各タスクは実行中に個別にスレッドリソースを要求する必要がありました。TiFlashはタスク数を制御することでスレッドリソースの使用量を制限し、過剰な使用を防いでいますが、この問題を完全に解消することはできませんでした。この問題に対処するため、v7.2.0以降、 TiFlashはパイプライン実行モデルを導入しました。このモデルは、すべてのスレッドリソースを一元管理し、タスク実行を均一にスケジュールすることで、リソースの過剰な使用を回避しながらスレッドリソースの利用率を最大化します。パイプライン実行モデルを有効または無効にするには、システム変数[`tidb_enable_tiflash_pipeline_model`](https://docs.pingcap.com/tidb/v7.2/system-variables#tidb_enable_tiflash_pipeline_model-new-in-v720)変更します。

    詳細については[ドキュメント](/tiflash/tiflash-pipeline-model.md)参照してください。

-   TiFlashはスキーマレプリケーションのレイテンシーを[＃7630](https://github.com/pingcap/tiflash/issues/7630) @ [ホンユニャン](https://github.com/hongyunyan)短縮します

    テーブルのスキーマが変更されると、 TiFlash はTiKV から最新のスキーマをタイムリーに複製する必要があります。v7.2.0 より前のバージョンでは、 TiFlash がテーブルデータにアクセスし、データベース内のテーブルスキーマの変更を検出すると、 TiFlash はTiFlashレプリカのないテーブルも含め、このデータベース内のすべてのテーブルのスキーマを再度複製する必要がありました。その結果、多数のテーブルを持つデータベースでは、 TiFlashを使用して単一のテーブルからデータを読み取るだけの場合でも、 TiFlash がすべてのテーブルのスキーマ複製を完了するまでにかなりのレイテンシーが発生する可能性があります。

    v7.2.0では、 TiFlashはスキーマレプリケーションのメカニズムを最適化し、 TiFlashレプリカを持つテーブルのスキーマレプリケーションのみをサポートします。TiFlashTiFlashを持つテーブルでスキーマ変更が検出されると、 TiFlashはそのテーブルのスキーマのみをレプリケーションします。これにより、 TiFlashのスキーマレプリケーションのレイテンシーが短縮され、DDL操作がTiFlashデータレプリケーションに与える影響が最小限に抑えられます。この最適化は自動的に適用され、手動での設定は不要です。

-   統計収集のパフォーマンスを向上[＃44725](https://github.com/pingcap/tidb/issues/44725) @ [xuyifangreeneyes](https://github.com/xuyifangreeneyes)

    TiDB v7.2.0では、統計収集戦略が最適化され、重複情報やオプティマイザにとって価値の低い情報をスキップするようになりました。統計収集の全体的な速度は30%向上しました。この改善により、TiDBはデータベースの統計をよりタイムリーに更新できるようになり、生成される実行プランの精度が向上し、データベース全体のパフォーマンスが向上します。

    デフォルトでは、統計収集は`JSON` 、 `BLOB` 、 `MEDIUMBLOB` 、 `LONGBLOB`型の列をスキップします。このデフォルトの動作は、システム変数[`tidb_analyze_skip_column_types`](/system-variables.md#tidb_analyze_skip_column_types-new-in-v720)を設定することで変更できます。TiDB は、 `JSON` 、 `BLOB` 、 `TEXT`型とそのサブタイプのスキップをサポートしています。

    詳細については[ドキュメント](/system-variables.md#tidb_analyze_skip_column_types-new-in-v720)参照してください。

-   データとインデックスの一貫性チェックのパフォーマンスを向上[＃43693](https://github.com/pingcap/tidb/issues/43693) @ [wjhuang2016](https://github.com/wjhuang2016)

    [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md)文は、テーブル内のデータと対応するインデックス間の整合性をチェックするために使用されます。v7.2.0 では、TiDB はデータ整合性チェックの方法を最適化し、 [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md)の実行効率を大幅に向上させました。大量のデータを扱うシナリオでは、この最適化によりパフォーマンスが数百倍向上する可能性があります。

    最適化はデフォルトで有効（デフォルトは[`tidb_enable_fast_table_check`](/system-variables.md#tidb_enable_fast_table_check-new-in-v720)または`ON` ）になっており、大規模なテーブルでのデータ整合性チェックにかかる時間を大幅に短縮し、運用効率を高めます。

    詳細については[ドキュメント](/system-variables.md#tidb_enable_fast_table_check-new-in-v720)参照してください。

### 信頼性 {#reliability}

-   予想よりも多くのリソースを消費するクエリを自動的に管理する（実験的） [＃43691](https://github.com/pingcap/tidb/issues/43691) @ [コナー1996](https://github.com/Connor1996) @ [キャビンフィーバーB](https://github.com/CabinfeverB) @ [栄光](https://github.com/glorv) @ [HuSharp](https://github.com/HuSharp) @ [ノルーシュ](https://github.com/nolouch)

    データベースの安定性における最も一般的な課題は、突発的なSQLパフォーマンスの問題によって引き起こされる、データベース全体のパフォーマンスの低下です。SQLパフォーマンスの問題には、十分にテストされていない新しいSQL文、データ量の急激な変化、実行計画の急激な変更など、多くの原因があります。これらの問題を根本的に完全に回避することは困難です。TiDB v7.2.0は、予想よりも多くのリソースを消費するクエリを管理する機能を提供します。この機能により、パフォーマンス問題が発生した場合の影響範囲を迅速に縮小できます。

    これらのクエリを管理するには、リソースグループに対してクエリの最大実行時間を設定できます。クエリの実行時間がこの制限を超えると、クエリは自動的に優先順位が下げられるかキャンセルされます。また、テキストまたは実行プランに基づいて特定されたクエリを直ちに照合する期間を設定することもできます。これにより、特定フェーズにおいて問題のあるクエリが同時に実行され、予想以上に多くのリソースを消費するのを防ぐことができます。

    予想以上にリソースを消費するクエリを自動的に管理することで、予期せぬクエリパフォーマンスの問題に迅速に対応するための効果的な手段となります。この機能により、問題がデータベース全体のパフォーマンスに与える影響を軽減し、データベースの安定性を向上させることができます。

    詳細については[ドキュメント](/tidb-resource-control.md#manage-queries-that-consume-more-resources-than-expected-runaway-queries)参照してください。

-   履歴実行プラン[＃39199](https://github.com/pingcap/tidb/issues/39199) @ [qw4990](https://github.com/qw4990)に従ってバインディングを作成する機能を強化します

    TiDB v7.2.0では、 [履歴実行計画に従ってバインディングを作成する](/sql-plan-management.md#create-a-binding-according-to-a-historical-execution-plan)の機能が強化されました。この機能により、複雑なステートメントの解析とバインディングのプロセスが改善され、バインディングがより安定するほか、以下の新しいヒントがサポートされます。

    -   [`AGG_TO_COP()`](/optimizer-hints.md#agg_to_cop)
    -   [`LIMIT_TO_COP()`](/optimizer-hints.md#limit_to_cop)
    -   [`ORDER_INDEX`](/optimizer-hints.md#order_indext1_name-idx1_name--idx2_name-)
    -   [`NO_ORDER_INDEX()`](/optimizer-hints.md#no_order_indext1_name-idx1_name--idx2_name-)

    詳細については[ドキュメント](/sql-plan-management.md)参照してください。

-   オプティマイザの動作をきめ細かく制御するためのオプティマイザ修正制御メカニズムを導入する[＃43169](https://github.com/pingcap/tidb/issues/43169) @ [時間と運命](https://github.com/time-and-fate)

    より合理的な実行計画を生成するために、TiDBオプティマイザの動作は製品のイテレーションを通じて進化していきます。しかし、特定のシナリオでは、これらの変更がパフォーマンスの低下につながる可能性があります。TiDB v7.2.0では、オプティマイザのきめ細かな動作を制御できるオプティマイザ修正制御が導入されました。これにより、新しい変更の一部をロールバックしたり、制御したりすることが可能になります。

    制御可能な各動作は、修正番号に対応するGitHub Issueで説明されています。制御可能なすべての動作は[オプティマイザー修正コントロール](/optimizer-fix-controls.md)にリストされています。動作制御を実現するには、 [`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-new-in-v653-and-v710)システム変数を設定することで、1つまたは複数の動作の目標値を設定できます。

    オプティマイザ修正制御メカニズムは、TiDBオプティマイザをきめ細かなレベルで制御するのに役立ちます。アップグレードプロセスによって発生するパフォーマンスの問題を修正する新しい手段を提供し、TiDBの安定性を向上させます。

    詳細については[ドキュメント](/optimizer-fix-controls.md)参照してください。

-   軽量統計初期化が一般提供 (GA) [＃42160](https://github.com/pingcap/tidb/issues/42160) @ [xuyifangreeneyes](https://github.com/xuyifangreeneyes)に開始

    v7.2.0以降、軽量統計初期化機能がGAとなります。軽量統計初期化により、起動時にロードする必要がある統計情報の数が大幅に削減され、統計情報のロード速度が向上します。この機能により、複雑なランタイム環境におけるTiDBの安定性が向上し、TiDBノードの再起動時にサービス全体への影響が軽減されます。

    v7.2.0以降のバージョンで新規作成されたクラスターでは、TiDBは起動時にデフォルトで軽量統計情報を読み込み、読み込みが完了するまで待機してからサービスを提供します。以前のバージョンからアップグレードしたクラスターでは、TiDB設定項目[`lite-init-stats`](/tidb-configuration-file.md#lite-init-stats-new-in-v710)および[`force-init-stats`](/tidb-configuration-file.md#force-init-stats-new-in-v657-and-v710) ～ `true`設定することでこの機能を有効化できます。

    詳細については[ドキュメント](/statistics.md#load-statistics)参照してください。

### SQL {#sql}

-   `CHECK`制約[＃41711](https://github.com/pingcap/tidb/issues/41711) @ [fzzf678](https://github.com/fzzf678)をサポートする

    バージョン7.2.0以降では、 `CHECK`制約を使用して、テーブル内の1つ以上の列の値を、指定した条件を満たすように制限できます。3制約`CHECK`テーブルに追加されると、TiDBはテーブルにデータを挿入または更新する前に、制約が満たされているかどうかを確認します。制約を満たすデータのみが書き込まれます。

    この機能はデフォルトで無効になっています。システム変数[`tidb_enable_check_constraint`](/system-variables.md#tidb_enable_check_constraint-new-in-v720) `ON`に設定すると有効になります。

    詳細については[ドキュメント](/constraints.md#check)参照してください。

### DB操作 {#db-operations}

-   DDL ジョブは一時停止と再開操作をサポートします (実験的) [＃18015](https://github.com/pingcap/tidb/issues/18015) @ [ゴドゥム](https://github.com/godouxm)

    TiDB v7.2.0より前のバージョンでは、DDLジョブの実行中にビジネスピークが発生した場合、ビジネスへの影響を軽減するためには、DDLジョブを手動でキャンセルするしかありませんでした。v7.2.0では、TiDBはDDLジョブの一時停止と再開操作を導入しました。これらの操作により、ピーク時にDDLジョブを一時停止し、ピーク終了後に再開することで、アプリケーションワークロードへの影響を回避できます。

    たとえば、 `ADMIN PAUSE DDL JOBS`または`ADMIN RESUME DDL JOBS`を使用して複数の DDL ジョブを一時停止および再開できます。

    ```sql
    ADMIN PAUSE DDL JOBS 1,2;
    ADMIN RESUME DDL JOBS 1,2;
    ```

    詳細については[ドキュメント](/ddl-introduction.md#ddl-related-commands)参照してください。

### データ移行 {#data-migration}

-   データのインポート効率を大幅に向上させる新しいSQL文`IMPORT INTO`を導入（実験的） [＃42930](https://github.com/pingcap/tidb/issues/42930) @ [D3ハンター](https://github.com/D3Hunter)

    `IMPORT INTO`ステートメントは、 TiDB Lightningの[物理インポートモード](/tidb-lightning/tidb-lightning-physical-import-mode.md)機能を統合します。このステートメントを使用すると、CSV、SQL、PARQUET などの形式のデータを TiDB の空のテーブルに迅速にインポートできます。このインポート方法により、 TiDB Lightningを個別に導入・管理する必要がなくなり、データインポートの複雑さが軽減され、インポート効率が大幅に向上します。

    Amazon S3 または GCS に保存されているデータファイルの場合、 [TiDB 分散実行フレームワーク (DXF)](/tidb-distributed-execution-framework.md)有効になっていると、 `IMPORT INTO`データインポートジョブを複数のサブジョブに分割し、それらを複数の TiDB ノードにスケジュールして並列インポートすることもサポートしており、これによりインポートのパフォーマンスがさらに向上します。

    詳細については[ドキュメント](/sql-statements/sql-statement-import-into.md)参照してください。

-   TiDB Lightningは、Latin-1文字セットを含むソースファイルをTiDB [＃44434](https://github.com/pingcap/tidb/issues/44434) @ [ランス6716](https://github.com/lance6716)にインポートすることをサポートします。

    この機能により、 TiDB Lightningを使用して Latin-1 文字セットを含むソースファイルを TiDB に直接インポートできます。v7.2.0 より前では、このようなファイルのインポートには追加の前処理または変換が必要でした。v7.2.0 以降では、 TiDB Lightning のインポートタスクの設定時に`character-set = "latin1"`指定するだけで済みます。その後は、 TiDB Lightning がインポートプロセス中に文字セットの変換を自動的に処理し、データの整合性と正確性を確保します。

    詳細については[ドキュメント](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)参照してください。

## 互換性の変更 {#compatibility-changes}

> **注記：**
>
> このセクションでは、v7.1.0から最新バージョン（v7.2.0）にアップグレードする際に知っておくべき互換性の変更点について説明します。v7.0.0以前のバージョンから最新バージョンにアップグレードする場合は、中間バージョンで導入された互換性の変更点も確認する必要があるかもしれません。

### 行動の変化 {#behavior-changes}

-   更新イベントの処理中に、イベント内で主キーまたはnull以外の一意のインデックス値が変更された場合、TiCDCはイベントを削除イベントと挿入イベントに分割します。詳細については、 [ドキュメント](/ticdc/ticdc-split-update-behavior.md#transactions-containing-a-single-update-change)参照してください。
-   デフォルト値[`tidb_remove_orderby_in_subquery`](/system-variables.md#tidb_remove_orderby_in_subquery-new-in-v610)を`OFF`から`ON`に変更します。これは、オプティマイザーがサブクエリから`ORDER BY`句を削除し、不要なソート操作を回避することを意味します。この変更により、クエリ結果の行の順序が異なる場合があります。ISO/IEC SQL 標準では、クエリ結果がサブクエリで指定された`ORDER BY`ソートに従う必要はありません。最終結果で特定の順序を確保する必要がある場合は、外部クエリに`ORDER BY`句を追加します。アプリケーションがサブクエリのソートに依存している場合は、この変数を`OFF`に設定できます。以前のバージョンからアップグレードされたクラスターは、デフォルトで以前の動作を保持します。

### システム変数 {#system-variables}

| 変数名                                                                                                                                                | タイプを変更   | 説明                                                                                                                                                                                                                                                                       |
| -------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [`last_insert_id`](/system-variables.md#last_insert_id)                                                                                            | 修正済み     | MySQL と一致するように、最大値を`9223372036854775807`から`18446744073709551615`に変更します。                                                                                                                                                                                                  |
| [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache)                                                  | 修正済み     | さらにテストを行った後、デフォルト値を`OFF`から`ON`に変更します。これは、準備されていない実行プラン キャッシュが有効になっていることを意味します。                                                                                                                                                                                           |
| [`tidb_remove_orderby_in_subquery`](/system-variables.md#tidb_remove_orderby_in_subquery-new-in-v610)                                              | 修正済み     | さらにテストを行った後、デフォルト値を`OFF`から`ON`に変更します。つまり、オプティマイザーはサブクエリ内の`ORDER BY`句を削除します。                                                                                                                                                                                              |
| [`tidb_analyze_skip_column_types`](/system-variables.md#tidb_analyze_skip_column_types-new-in-v720)                                                | 新しく追加された | 統計情報を収集するコマンド`ANALYZE`を実行する際に、統計収集からスキップする列の種類を制御します。この変数は[`tidb_analyze_version = 2`](/system-variables.md#tidb_analyze_version-new-in-v510)にのみ適用されます。 `ANALYZE TABLE t COLUMNS c1, ..., cn`の構文を使用する場合、指定された列の型が`tidb_analyze_skip_column_types`に含まれる場合、その列の統計は収集されません。 |
| [`tidb_enable_check_constraint`](/system-variables.md#tidb_enable_check_constraint-new-in-v720)                                                    | 新しく追加された | `CHECK`制約を有効にするかどうかを制御します。デフォルト値は`OFF`で、この機能は無効です。                                                                                                                                                                                                                       |
| [`tidb_enable_fast_table_check`](/system-variables.md#tidb_enable_fast_table_check-new-in-v720)                                                    | 新しく追加された | テーブル内のデータとインデックスの整合性を迅速にチェックするために、チェックサムベースのアプローチを使用するかどうかを制御します。デフォルト値は`ON`で、この機能が有効であることを意味します。                                                                                                                                                                        |
| [`tidb_enable_tiflash_pipeline_model`](https://docs-archive.pingcap.com/tidb/v7.2/system-variables#tidb_enable_tiflash_pipeline_model-new-in-v720) | 新しく追加された | TiFlashの新しい実行モデル[パイプラインモデル](/tiflash/tiflash-pipeline-model.md)を有効にするかどうかを制御します。デフォルト値は`OFF`で、パイプラインモデルが無効であることを意味します。                                                                                                                                                   |
| [`tidb_expensive_txn_time_threshold`](/system-variables.md#tidb_expensive_txn_time_threshold-new-in-v720)                                          | 新しく追加された | 高価なトランザクションをログに記録するためのしきい値を制御します。デフォルトでは600秒です。トランザクションの実行時間がしきい値を超え、コミットもロールバックも行われない場合、そのトランザクションは高価なトランザクションとみなされ、ログに記録されます。                                                                                                                                          |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーションパラメータ                                                                                                                                 | タイプを変更   | 説明                                                                                                                                                                                                                                                                        |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB           | [`lite-init-stats`](/tidb-configuration-file.md#lite-init-stats-new-in-v710)                                                                    | 修正済み     | さらにテストを行った後、デフォルト値を`false`から`true`に変更します。つまり、TiDB は、初期化の効率を向上させるために、TiDB の起動時にデフォルトで軽量統計初期化を使用します。                                                                                                                                                                        |
| TiDB           | [`force-init-stats`](/tidb-configuration-file.md#force-init-stats-new-in-v657-and-v710)                                                         | 修正済み     | デフォルト値を`false`から`true`に変更して[`lite-init-stats`](/tidb-configuration-file.md#lite-init-stats-new-in-v710)に合わせます。つまり、TiDB の起動中にサービスを提供する前に、統計の初期化が完了するまで TiDB は待機します。                                                                                                        |
| TiKV           | [`rocksdb.[defaultcf|writecf|lockcf].compaction-guard-min-output-file-size`](/tikv-configuration-file.md#compaction-guard-min-output-file-size) | 修正済み     | RocksDB の圧縮タスクのデータ量を削減するために、デフォルト値を`"8MB"`から`"1MB"`に変更します。                                                                                                                                                                                                                |
| TiKV           | [`rocksdb.[defaultcf|writecf|lockcf].optimize-filters-for-memory`](/tikv-configuration-file.md#optimize-filters-for-memory-new-in-v720)         | 新しく追加された | メモリの内部断片化を最小限に抑えるブルーム/リボン フィルターを生成するかどうかを制御します。                                                                                                                                                                                                                           |
| TiKV           | [`rocksdb.[defaultcf|writecf|lockcf].periodic-compaction-seconds`](/tikv-configuration-file.md#periodic-compaction-seconds-new-in-v720)         | 新しく追加された | 定期的な圧縮の間隔を制御します。この値よりも古い更新を含む SST ファイルが圧縮対象として選択され、これらの SST ファイルが元々存在していたレベルと同じレベルに書き換えられます。                                                                                                                                                                              |
| TiKV           | [`rocksdb.[defaultcf|writecf|lockcf].ribbon-filter-above-level`](/tikv-configuration-file.md#ribbon-filter-above-level-new-in-v720)             | 新しく追加された | この値以上のレベルにはリボン フィルターを使用し、この値未満のレベルには非ブロックベースのブルーム フィルターを使用するかどうかを制御します。                                                                                                                                                                                                   |
| TiKV           | [`rocksdb.[defaultcf|writecf|lockcf].ttl`](/tikv-configuration-file.md#ttl-new-in-v720)                                                         | 新しく追加された | TTL よりも古い更新を含む SST ファイルは自動的に圧縮対象として選択されます。                                                                                                                                                                                                                                |
| TiDB Lightning | `send-kv-pairs`                                                                                                                                 | 非推奨      | バージョン7.2.0以降、パラメータ`send-kv-pairs`非推奨となりました。物理インポートモードでTiKVにデータを送信する際、1リクエストの最大サイズを制御するにはパラメータ[`send-kv-size`](/tidb-lightning/tidb-lightning-configuration.md)使用します。                                                                                                      |
| TiDB Lightning | [`character-set`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)                                                          | 修正済み     | データインポートでサポートされる文字セットに新しい値オプション`latin1`が導入されました。このオプションを使用すると、Latin-1文字セットのソースファイルをインポートできます。                                                                                                                                                                             |
| TiDB Lightning | [`send-kv-size`](/tidb-lightning/tidb-lightning-configuration.md)                                                                               | 新しく追加された | 物理インポートモードでTiKVにデータを送信する際の1リクエストの最大サイズを指定します。キーと値のペアのサイズが指定されたしきい値に達すると、 TiDB Lightningはそれらを直ちにTiKVに送信します。これにより、大規模で幅の広いテーブルをインポートする際に、 TiDB Lightningノードがメモリ内にキーと値のペアを過剰に蓄積することで発生するOOM問題を回避できます。このパラメータを調整することで、メモリ使用量とインポート速度のバランスを調整し、インポートプロセスの安定性と効率性を向上させることができます。 |
| データ移行          | [`strict-optimistic-shard-mode`](/dm/feature-shard-merge-optimistic.md)                                                                         | 新しく追加された | この設定項目は、TiDB Data Migration v2.0 の DDL シャードマージ動作との互換性を保つために使用されます。この設定項目は楽観的モードで有効にできます。有効にすると、Type 2 の DDL 文が検出されるとレプリケーションタスクが中断されます。複数のテーブルにおける DDL 変更間に依存関係がある場合、適切なタイミングで中断される可能性があります。上流と下流の間のデータ整合性を確保するため、レプリケーションタスクを再開する前に、各テーブルの DDL 文を手動で処理する必要があります。         |
| TiCDC          | [`sink.protocol`](/ticdc/ticdc-changefeed-config.md)                                                                                            | 修正済み     | ダウンストリームがKafkaの場合、新しい値オプション`"open-protocol"`が導入されました。メッセージのエンコードに使用するプロトコル形式を指定します。                                                                                                                                                                                       |
| TiCDC          | [`sink.delete-only-output-handle-key-columns`](/ticdc/ticdc-changefeed-config.md)                                                               | 新しく追加された | DELETEイベントの出力を指定します。このパラメータはプロトコル`"canal-json"`および`"open-protocol"`でのみ有効です。デフォルト値は`false` 、すべての列が出力されます。 `true`に設定すると、主キー列または一意のインデックス列のみが出力されます。                                                                                                                         |

## 改善点 {#improvements}

-   TiDB

    -   インデックススキャン範囲を構築するロジックを最適化し、複雑な条件をインデックススキャン範囲[＃41572](https://github.com/pingcap/tidb/issues/41572) [＃44389](https://github.com/pingcap/tidb/issues/44389) @ [xuyifangreeneyes](https://github.com/xuyifangreeneyes)に変換できるようにしました。
    -   新しい監視メトリック`Stale Read OPS`と`Stale Read Traffic` [＃43325](https://github.com/pingcap/tidb/issues/43325) @ [あなた06](https://github.com/you06)を追加
    -   古い読み取りの再試行リーダーがロックに遭遇すると、TiDBはロックを解決した後、リーダーで強制的に再試行し、不要なオーバーヘッドを回避します[＃43659](https://github.com/pingcap/tidb/issues/43659) @ [あなた06](https://github.com/you06)
    -   推定時間を使用して古い読み取りtsを計算し、古い読み取り[＃44215](https://github.com/pingcap/tidb/issues/44215) @ [あなた06](https://github.com/you06)のオーバーヘッドを削減します。
    -   長時間実行されるトランザクションのログとシステム変数を追加する[＃41471](https://github.com/pingcap/tidb/issues/41471) @ [crazycs520](https://github.com/crazycs520)
    -   圧縮MySQLプロトコル経由でTiDBに接続できるようになりました。これにより、低帯域幅ネットワークにおけるデータ集約型クエリのパフォーマンスが向上し、帯域幅コストを削減できます。1 `zlib`と`zstd`ベースの両方の圧縮をサポートしています[＃22605](https://github.com/pingcap/tidb/issues/22605) @ [ドヴェーデン](https://github.com/dveeden)
    -   `utf8`と`utf8bm3`両方を従来の 3 バイト UTF-8 文字セットエンコーディングとして認識します。これにより、MySQL 8.0 から TiDB [＃26226](https://github.com/pingcap/tidb/issues/26226) @ [ドヴェーデン](https://github.com/dveeden)への従来の UTF-8 エンコーディングを持つテーブルの移行が容易になります。
    -   `UPDATE`ステートメント[＃44751](https://github.com/pingcap/tidb/issues/44751) @ [CbcWestwolf](https://github.com/CbcWestwolf)での割り当てに`:=`使用することをサポート

-   TiKV

    -   `pd.retry-interval` [＃14964](https://github.com/tikv/tikv/issues/14964) @ [rleungx](https://github.com/rleungx)を使用した接続要求の失敗などのシナリオでの PD 接続の再試行間隔の構成をサポート
    -   グローバルリソース使用量[＃14604](https://github.com/tikv/tikv/issues/14604) @ [コナー1996](https://github.com/Connor1996)を組み込むことで、リソース制御スケジューリングアルゴリズムを最適化します。
    -   `check_leader`リクエストに gzip 圧縮を使用してトラフィック[＃14553](https://github.com/tikv/tikv/issues/14553) @ [あなた06](https://github.com/you06)を削減します
    -   `check_leader`リクエスト[＃14658](https://github.com/tikv/tikv/issues/14658) @ [あなた06](https://github.com/you06)の関連メトリックを追加します
    -   TiKV が書き込みコマンド[＃12362](https://github.com/tikv/tikv/issues/12362) @ [cfzjywxk](https://github.com/cfzjywxk)を処理する際の詳細な時間情報を提供します

-   PD

    -   他のリクエスト[＃6403](https://github.com/tikv/pd/issues/6403) @ [rleungx](https://github.com/rleungx)の影響を防ぐために、PDリーダー選出には別のgRPC接続を使用する
    -   マルチリージョンシナリオにおけるホットスポットの問題を軽減するために、バケット分割をデフォルトで有効にする[＃6433](https://github.com/tikv/pd/issues/6433) @ [バッファフライ](https://github.com/bufferflies)

-   ツール

    -   バックアップと復元 (BR)

        -   共有アクセス署名 (SAS) [＃44199](https://github.com/pingcap/tidb/issues/44199) @ [リーヴルス](https://github.com/Leavrth)による Azure Blob Storage へのアクセスをサポート

    -   TiCDC

        -   オブジェクトstorageサービスへのレプリケーションのシナリオでDDL操作が発生したときにデータファイルが格納されるディレクトリの構造を最適化します[＃8891](https://github.com/pingcap/tiflow/issues/8891) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)
        -   Kafka [＃8865](https://github.com/pingcap/tiflow/issues/8865) @ [ハイラスティン](https://github.com/Rustin170506)へのレプリケーションのシナリオでOAUTHBEARER認証をサポート
        -   Kafka [＃9143](https://github.com/pingcap/tiflow/issues/9143) @ [3エースショーハンド](https://github.com/3AceShowHand)へのレプリケーションのシナリオで`DELETE`操作のハンドルキーのみを出力するオプションを追加

    -   TiDB データ移行 (DM)

        -   MySQL 8.0 で圧縮されたバイナリログを増分レプリケーションのデータソースとして読み取る機能をサポート[＃6381](https://github.com/pingcap/tiflow/issues/6381) @ [ドヴェーデン](https://github.com/dveeden)

    -   TiDB Lightning

        -   インポート中の再試行メカニズムを最適化して、リーダーの切り替え[＃44263](https://github.com/pingcap/tidb/issues/44263) @ [ランス6716](https://github.com/lance6716)によるエラーを回避します。
        -   インポート後にSQLでチェックサムを検証し、検証[＃41941](https://github.com/pingcap/tidb/issues/41941) @ [GMHDBJD](https://github.com/GMHDBJD)の安定性を向上
        -   ワイドテーブル[＃43853](https://github.com/pingcap/tidb/issues/43853) @ [D3ハンター](https://github.com/D3Hunter)をインポートする際のTiDB Lightning OOM の問題を最適化します

## バグ修正 {#bug-fixes}

-   TiDB

    -   CTE を含むクエリによって TiDB がハングする問題を修正[＃43749](https://github.com/pingcap/tidb/issues/43749) [＃36896](https://github.com/pingcap/tidb/issues/36896) @ [グオシャオゲ](https://github.com/guo-shaoge)
    -   `min, max`クエリ結果が正しくない問題を修正[＃43805](https://github.com/pingcap/tidb/issues/43805) @ [wshwsh12](https://github.com/wshwsh12)
    -   `SHOW PROCESSLIST`文でサブクエリ時間が長い文のトランザクションの TxnStart を表示できない問題を修正[＃40851](https://github.com/pingcap/tidb/issues/40851) @ [crazycs520](https://github.com/crazycs520)
    -   コプロセッサータスク[＃43365](https://github.com/pingcap/tidb/issues/43365) @ [あなた06](https://github.com/you06)に`TxnScope`が不足しているため、古い読み取りグローバル最適化が有効にならない問題を修正しました。
    -   フォロワー読み取りが再試行前にフラッシュバックエラーを処理せず、クエリエラー[＃43673](https://github.com/pingcap/tidb/issues/43673) @ [あなた06](https://github.com/you06)が発生する問題を修正しました
    -   `ON UPDATE`文が主キー[＃44565](https://github.com/pingcap/tidb/issues/44565) @ [ジグアン](https://github.com/zyguan)を正しく更新しない場合にデータとインデックスが不整合になる問題を修正しました
    -   権限テーブル[＃41048](https://github.com/pingcap/tidb/issues/41048) @ [bb7133](https://github.com/bb7133)の一部の列における大文字と小文字の区別の問題を修正しました
    -   MySQL 8.0.28以降のバージョン[＃43987](https://github.com/pingcap/tidb/issues/43987) @ [ヤンケオ](https://github.com/YangKeao)と一致するように、 `UNIX_TIMESTAMP()`関数の上限を`3001-01-19 03:14:07.999999 UTC`に変更します。
    -   取り込みモード[＃44137](https://github.com/pingcap/tidb/issues/44137) @ [接線](https://github.com/tangenta)でインデックスの追加が失敗する問題を修正
    -   ロールバック状態でDDLタスクをキャンセルすると、関連するメタデータ[＃44143](https://github.com/pingcap/tidb/issues/44143) @ [wjhuang2016](https://github.com/wjhuang2016)にエラーが発生する問題を修正しました
    -   カーソルフェッチで`memTracker`使用するとメモリリークが発生する問題を修正[＃44254](https://github.com/pingcap/tidb/issues/44254) @ [ヤンケオ](https://github.com/YangKeao)
    -   データベースを削除するとGCの進行が遅くなる問題を修正[＃33069](https://github.com/pingcap/tidb/issues/33069) @ [天菜まお](https://github.com/tiancaiamao)
    -   インデックス結合[＃43686](https://github.com/pingcap/tidb/issues/43686) @ [アイリンキッド](https://github.com/AilinKid) @ [ミョンス](https://github.com/mjonss)のプローブフェーズでパーティションテーブル内の対応する行が見つからない場合に TiDB がエラーを返す問題を修正しました。
    -   `SUBPARTITION`を使用してパーティションテーブル[＃41198](https://github.com/pingcap/tidb/issues/41198) [＃41200](https://github.com/pingcap/tidb/issues/41200) @ [ミョンス](https://github.com/mjonss)を作成するときに警告が表示されない問題を修正しました
    -   クエリが`MAX_EXECUTION_TIME`超えたために強制終了された場合に返されるエラーメッセージが MySQL [＃43031](https://github.com/pingcap/tidb/issues/43031) @ [ドヴェーデン](https://github.com/dveeden)のものと一致しない問題を修正しました。
    -   `LEADING`ヒントがブロックエイリアス[＃44645](https://github.com/pingcap/tidb/issues/44645) @ [qw4990](https://github.com/qw4990)のクエリをサポートしない問題を修正しました
    -   `LAST_INSERT_ID()`関数の戻り値の型を VARCHAR から LONGLONG に変更して、MySQL [＃44574](https://github.com/pingcap/tidb/issues/44574) @ [定義2014](https://github.com/Defined2014)の戻り値の型と一致するようにします。
    -   非相関サブクエリ[＃44051](https://github.com/pingcap/tidb/issues/44051) @ [ウィノロス](https://github.com/winoros)を含むステートメントで共通テーブル式 (CTE) を使用すると誤った結果が返される可能性がある問題を修正しました
    -   結合したテーブルの再配置により外部結合結果が不正確になる可能性がある問題を修正[＃44314](https://github.com/pingcap/tidb/issues/44314) @ [アイリンキッド](https://github.com/AilinKid)
    -   `PREPARE stmt FROM "ANALYZE TABLE xxx"` `tidb_mem_quota_query` [＃44320](https://github.com/pingcap/tidb/issues/44320) @ [クリサン](https://github.com/chrysan)で殺される可能性がある問題を修正

-   TiKV

    -   TiKV が古い悲観的ロックの競合[＃13298](https://github.com/tikv/tikv/issues/13298) @ [cfzjywxk](https://github.com/cfzjywxk)を処理するときにトランザクションが誤った値を返す問題を修正しました
    -   メモリ内悲観的ロックがフラッシュバックの失敗やデータの不整合を引き起こす可能性がある問題を修正[＃13303](https://github.com/tikv/tikv/issues/13303) @ [Jmポテト](https://github.com/JmPotato)
    -   TiKV が古いリクエスト[＃13298](https://github.com/tikv/tikv/issues/13298) @ [cfzjywxk](https://github.com/cfzjywxk)を処理するときにフェアロックが正しくない可能性がある問題を修正しました
    -   `autocommit`と`point get replica read`が[＃14715](https://github.com/tikv/tikv/issues/14715) @ [cfzjywxk](https://github.com/cfzjywxk)の線形化可能性を壊す可能性がある問題を修正

-   PD

    -   一部のコーナーケースで冗長レプリカが自動的に修復されない問題を修正[＃6573](https://github.com/tikv/pd/issues/6573) @ [ノルーシュ](https://github.com/nolouch)

-   TiFlash

    -   Joinビルド側のデータが非常に大きく、多くの小さな文字列型の列[＃7416](https://github.com/pingcap/tiflash/issues/7416) @ [イービン87](https://github.com/yibin87)が含まれている場合に、クエリが必要以上にメモリを消費する可能性がある問題を修正しました。

-   ツール

    -   バックアップと復元 (BR)

        -   `checksum mismatch`場合によっては誤って報告される問題を修正[＃44472](https://github.com/pingcap/tidb/issues/44472) @ [リーヴルス](https://github.com/Leavrth)
        -   `resolved lock timeout`場合によっては誤って報告される問題を修正[＃43236](https://github.com/pingcap/tidb/issues/43236) @ [ユジュンセン](https://github.com/YuJuncen)
        -   統計情報[＃44490](https://github.com/pingcap/tidb/issues/44490) @ [接線](https://github.com/tangenta)を復元するときに TiDB がpanic可能性がある問題を修正しました

    -   TiCDC

        -   解決済みのTSが[＃8963](https://github.com/pingcap/tiflow/issues/8963) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)で正しく進まない場合がある問題を修正
        -   AvroまたはCSVプロトコルが使用されている場合、 `UPDATE`操作で古い値を出力できない問題を修正しました[＃9086](https://github.com/pingcap/tiflow/issues/9086) @ [3エースショーハンド](https://github.com/3AceShowHand)
        -   Kafka [＃8959](https://github.com/pingcap/tiflow/issues/8959) @ [ハイラスティン](https://github.com/Rustin170506)にデータを複製する際に下流のメタデータを頻繁に読み取ることによって下流に過度の負荷がかかる問題を修正しました
        -   TiDB または MySQL [＃9180](https://github.com/pingcap/tiflow/issues/9180) @ [アズドンメン](https://github.com/asddongmen)にデータを複製するときに、下流の双方向レプリケーション関連の変数を頻繁に設定することによって発生する下流ログが多すぎる問題を修正しました。
        -   PDノードがクラッシュするとTiCDCノードが[＃8868](https://github.com/pingcap/tiflow/issues/8868) @ [アズドンメン](https://github.com/asddongmen)で再起動する問題を修正
        -   TiCDC が下流の Kafka-on-Pulsar [＃8892](https://github.com/pingcap/tiflow/issues/8892) @ [ハイラスティン](https://github.com/Rustin170506)で変更フィードを作成できない問題を修正しました

    -   TiDB Lightning

        -   `experimental.allow-expression-index`が有効でデフォルト値が UUID [＃44497](https://github.com/pingcap/tidb/issues/44497) @ [リチュンジュ](https://github.com/lichunzhu)の場合に発生するTiDB Lightningpanic問題を修正しました
        -   データファイル[＃43195](https://github.com/pingcap/tidb/issues/43195) @ [ランス6716](https://github.com/lance6716)を分割中にタスクが終了したときに発生するTiDB Lightningpanic問題を修正しました

## 寄稿者 {#contributors}

TiDB コミュニティからの以下の貢献者に感謝いたします。

-   [asjdf](https://github.com/asjdf)
-   [ブラックティア23](https://github.com/blacktear23)
-   [キャヴァンスー](https://github.com/Cavan-xu)
-   [ダラエス](https://github.com/darraes)
-   [デモマニト](https://github.com/demoManito)
-   [ディサム](https://github.com/dhysum)
-   [ハッピーv587](https://github.com/happy-v587)
-   [ジフハウス](https://github.com/jiyfhust)
-   [L-メープル](https://github.com/L-maple)
-   [ニュリク](https://github.com/nyurik)
-   [シージC](https://github.com/SeigeC)
-   [タンジンユ97](https://github.com/tangjingyu97)
