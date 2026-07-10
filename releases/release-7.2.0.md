---
title: TiDB 7.2.0 Release Notes
summary: TiDB 7.2.0 の新機能、互換性の変更点、改善点、およびバグ修正についてご確認ください。
---

# TiDB 7.2.0 リリースノート {#tidb-7-2-0-release-notes}

発売日：2023年6月29日

TiDB バージョン: 7.2.0

クイックアクセス: [クイックスタート](https://docs-archive.pingcap.com/tidb/v7.2/quick-start-with-tidb)

バージョン7.2.0では、以下の主要な機能と改善点が導入されています。

<table><thead><tr><th>カテゴリ</th><th>特徴</th><th>説明</th></tr></thead><tbody><tr><td rowspan="2">拡張性とパフォーマンス</td><td>リソースグループは<a href="https://docs-archive.pingcap.com/tidb/v7.2/tidb-resource-control#manage-queries-that-consume-more-resources-than-expected-runaway-queries">暴走クエリの管理を</a>サポートします（実験的）</td><td>クエリのタイムアウトをより細かく管理できるようになり、クエリの分類に基づいて異なる動作を設定できるようになりました。指定したしきい値に達したクエリは、優先度を下げたり、終了させたりすることができます。</td></tr><tr><td> TiFlashは<a href="https://docs-archive.pingcap.com/tidb/v7.2/tiflash-pipeline-model">パイプライン実行モデル</a>をサポートしています（実験的）。</td><td> TiFlashは、スレッドリソース制御を最適化するために、パイプライン実行モデルをサポートしています。</td></tr><tr><td rowspan="1"> SQL</td><td>データインポート用の新しいSQL文<a href="https://docs-archive.pingcap.com/tidb/v7.2/sql-statement-import-into">「IMPORT INTO」</a>をサポート（実験的）</td><td> TiDB Lightningの導入とメンテナンスを簡素化するために、TiDB は新しい SQL ステートメント<code>IMPORT INTO</code>導入しました。これにより、Amazon S3 や Google Cloud Storage (GCS) からのリモートインポートを含むTiDB Lightningの物理インポートモードが TiDB に直接統合されます。</td></tr><tr><td rowspan="2">データベースの運用と可観測性</td><td>DDLは<a href="https://docs-archive.pingcap.com/tidb/v7.2/ddl-introduction#ddl-related-commands">一時停止および再開操作</a>をサポートします（実験的）。</td><td>この新機能により、インデックス作成などのリソースを大量に消費するDDL操作を一時的に中断し、リソースを節約してオンライントラフィックへの影響を最小限に抑えることができます。準備が整い次第、キャンセルや再起動の必要なく、これらの操作をシームレスに再開できます。この機能は、リソース利用効率の向上、ユーザーエクスペリエンスの改善、スキーマ変更の効率化に貢献します。</td></tr></tbody></table>

## 機能の詳細 {#feature-details}

### パフォーマンス {#performance}

-   TiFlash への次の 2 つの[ウィンドウ関数](/tiflash/tiflash-supported-pushdown-calculations.md)プッシュダウンをサポートします。 [#7427](https://github.com/pingcap/tiflash/issues/7427) @[xzhangxian1008](https://github.com/xzhangxian1008)

    -   `FIRST_VALUE`
    -   `LAST_VALUE`

-   TiFlashはパイプライン実行モデルをサポートします（実験的） [#6518](https://github.com/pingcap/tiflash/issues/6518) @[SeaRise](https://github.com/SeaRise)

    バージョン7.2.0より前は、 TiFlashエンジン内の各タスクは実行時に個別にスレッドリソースを要求する必要がありました。TiFlashはタスク数を制御することでスレッドリソースの使用量を制限し、過剰使用を防いでいましたが、この問題を完全に解消することはできませんでした。この問題に対処するため、バージョン7.2.0以降、 TiFlashはパイプライン実行モデルを導入しました。このモデルでは、すべてのスレッドリソースを一元的に管理し、タスクの実行を均一にスケジュールすることで、リソースの過剰使用を回避しながらスレッドリソースの利用率を最大化します。パイプライン実行モデルを有効または無効にするには、システム変数[`tidb_enable_tiflash_pipeline_model`](https://docs-archive.pingcap.com/tidb/v7.2/system-variables/#tidb_enable_tiflash_pipeline_model-new-in-v720)を変更してください。

    詳細については、[ドキュメント](/tiflash/tiflash-pipeline-model.md)を参照してください。

-   TiFlash はスキーマ複製のレイテンシーを削減します [#7630](https://github.com/pingcap/tiflash/issues/7630) @[hongyunyan](https://github.com/hongyunyan)

    テーブルのスキーマが変更されると、 TiFlash はTiKV から最新のスキーマをタイムリーにレプリケートする必要があります。v7.2.0 より前のバージョンでは、 TiFlash がテーブルデータにアクセスし、データベース内のテーブルスキーマの変更を検出すると、 TiFlashレプリカを持たないテーブルも含め、このデータベース内のすべてのテーブルのスキーマを再度レプリケートする必要がありました。そのため、テーブル数の多いデータベースでは、 TiFlashを使用して単一のテーブルからデータを読み取る場合でも、 TiFlash がすべてのテーブルのスキーマ複製を完了するまで待機する必要があり、かなりのレイテンシーが発生する可能性があります。

    バージョン7.2.0では、 TiFlashのスキーマレプリケーションメカニズムが最適化され、 TiFlashレプリカを持つテーブルのスキーマのみをレプリケートするようになりました。TiFlashレプリカを持つテーブルでスキーマ変更が検出されると、 TiFlashはそのテーブルのスキーマのみをレプリケートします。これにより、 TiFlashのスキーマレプリケーションのレイテンシーが短縮され、DDL操作がTiFlashデータレプリケーションに与える影響が最小限に抑えられます。この最適化は自動的に適用され、手動での設定は不要です。

-   統計情報の収集パフォーマンスを改善する [#44725](https://github.com/pingcap/tidb/issues/44725) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)

    TiDB v7.2.0では、統計情報の収集戦略が最適化され、重複情報やオプティマイザにとって価値の低い情報がスキップされるようになりました。統計情報の収集速度は全体で30%向上しています。この改善により、TiDBはデータベースの統計情報をより迅速に更新できるようになり、生成される実行プランの精度が向上し、結果としてデータベース全体のパフォーマンスが向上します。

    デフォルトでは、統計情報の収集では`JSON` 、 `BLOB` 、 `MEDIUMBLOB` 、および`LONGBLOB`型の列がスキップされます。デフォルトの動作は、 [`tidb_analyze_skip_column_types`](/system-variables.md#tidb_analyze_skip_column_types-new-in-v720)システム変数を設定することで変更できます。TiDB は`JSON` 、 `BLOB` 、および`TEXT`型とそのサブタイプのスキップをサポートしています。

    詳細については、 [ドキュメント](/system-variables.md#tidb_analyze_skip_column_types-new-in-v720)を参照してください。

-   データとインデックスの一貫性チェックのパフォーマンスを改善 [#43693](https://github.com/pingcap/tidb/issues/43693) @[wjhuang2016](https://github.com/wjhuang2016)

    [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md)ステートメントは、テーブル内のデータとそれに対応するインデックスとの整合性をチェックするために使用されます。v7.2.0 では、TiDB はデータ整合性チェックの方法を最適化し、 [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md)の実行効率を大幅に向上させました。大量のデータを扱うシナリオでは、この最適化によりパフォーマンスが数百倍向上する可能性があります。

    最適化はデフォルトで有効になっており（ [`tidb_enable_fast_table_check`](/system-variables.md#tidb_enable_fast_table_check-new-in-v720)はデフォルトで`ON`です）、大規模テーブルにおけるデータ整合性チェックに必要な時間を大幅に短縮し、運用効率を向上させます。

    詳細については、 [ドキュメント](/system-variables.md#tidb_enable_fast_table_check-new-in-v720)を参照してください。

### 信頼性 {#reliability}

-   予想よりも多くのリソースを消費するクエリを自動的に管理する (実験的) [#43691](https://github.com/pingcap/tidb/issues/43691) @[Connor1996](https://github.com/Connor1996) @[glorv](https://github.com/glorv)[キャビンフィーバーB](https://github.com/CabinfeverB) @グロルヴ@[HuSharp](https://github.com/HuSharp) @[nolouch](https://github.com/nolouch)

    データベースの安定性に対する最も一般的な課題は、SQLのパフォーマンス問題が突発的に発生することによるデータベース全体のパフォーマンス低下です。SQLのパフォーマンス問題には、十分にテストされていない新しいSQL文、データ量の急激な変化、実行プランの急激な変更など、多くの原因があります。これらの問題を根本から完全に回避することは困難です。TiDB v7.2.0では、想定よりも多くのリソースを消費するクエリを管理する機能を提供しています。この機能により、パフォーマンス問題が発生した場合の影響範囲を迅速に縮小できます。

    これらのクエリを管理するために、リソースグループごとにクエリの最大実行時間を設定できます。クエリの実行時間がこの制限を超えると、クエリの優先度が自動的に下げられるか、キャンセルされます。また、テキストまたは実行プランに基づいて特定されたクエリを即座に照合する期間を設定することもできます。これにより、特定フェーズ中に問題のあるクエリが多数同時実行されることを防ぎ、想定以上のリソース消費を回避できます。

    想定以上のリソースを消費するクエリを自動的に管理することで、予期せぬクエリパフォーマンスの問題に迅速に対応できる効果的な手段が得られます。この機能は、問題がデータベース全体のパフォーマンスに与える影響を軽減し、データベースの安定性を向上させます。

    詳細については、 [ドキュメント](/tidb-resource-control-runaway-queries.md)を参照してください。

-   過去の実行計画に基づいてバインディングを作成する機能を強化する [#39199](https://github.com/pingcap/tidb/issues/39199) @[qw4990](https://github.com/qw4990)

    TiDB v7.2.0 は[過去の実行計画に従ってバインディングを作成する](/sql-plan-management.md#create-a-binding-according-to-a-historical-execution-plan)機能を強化します。この機能により、複雑なステートメントの解析とバインドのプロセスが改善され、バインディングがより安定し、次の新しいヒントがサポートされます。

    -   [`AGG_TO_COP()`](/optimizer-hints.md#agg_to_cop)
    -   [`LIMIT_TO_COP()`](/optimizer-hints.md#limit_to_cop)
    -   [`ORDER_INDEX`](/optimizer-hints.md#order_indext1_name-idx1_name--idx2_name-)
    -   [`NO_ORDER_INDEX()`](/optimizer-hints.md#no_order_indext1_name-idx1_name--idx2_name-)

    詳細については、[ドキュメント](/sql-plan-management.md)を参照してください。

-   オプティマイザー修正制御メカニズムを導入して、オプティマイザーの動作をきめ細かく制御できるようにします [#43169](https://github.com/pingcap/tidb/issues/43169) @[time-and-fate](https://github.com/time-and-fate)

    より適切な実行プランを生成するため、TiDB オプティマイザの動作は製品のバージョンアップごとに進化しています。しかし、特定のシナリオでは、変更によってパフォーマンスが低下する場合があります。TiDB v7.2.0 では、オプティマイザの細かい動作を制御できるオプティマイザ修正コントロールが導入されました。これにより、一部の新しい変更をロールバックしたり、制御したりすることが可能になります。

    制御可能な各動作は、修正番号に対応する GitHub の問題によって説明されます。制御可能な動作はすべてオプティマ[オプティマイザー修正コントロール](/optimizer-fix-controls.md)にリストされています。動作制御を実現するために[`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-new-in-v653-and-v710)システム変数を設定することにより、1 つ以上の動作の目標値を設定できます。

    オプティマイザ修正制御メカニズムを使用すると、TiDBオプティマイザをきめ細かく制御できます。これにより、アップグレードプロセスによって発生するパフォーマンスの問題を修正する新しい手段が提供され、TiDBの安定性が向上します。

    詳細については、[ドキュメント](/optimizer-fix-controls.md)を参照してください。

-   軽量統計初期化が一般提供開始 (GA) [#42160](https://github.com/pingcap/tidb/issues/42160) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)

    バージョン7.2.0以降、軽量統計初期化機能が一般提供（GA）となりました。軽量統計初期化機能により、起動時にロードする必要のある統計情報の数を大幅に削減できるため、統計情報のロード速度が向上します。この機能は、複雑な実行環境におけるTiDBの安定性を高め、TiDBノードの再起動時にサービス全体への影響を軽減します。

    v7.2.0以降のバージョンで新規作成されたクラスタの場合、TiDBはデフォルトでTiDB起動時に軽量統計情報をロードし、ロードが完了するまでサービスの提供を待ちます。以前のバージョンからアップグレードしたクラスタの場合は、TiDB構成項目[`lite-init-stats`](/tidb-configuration-file.md#lite-init-stats-new-in-v710)と[`force-init-stats`](/tidb-configuration-file.md#force-init-stats-new-in-v657-and-v710)を`true`に設定することで、この機能を有効にできます。

    詳細については、[ドキュメント](/statistics.md#load-statistics)を参照してください。

### SQL {#sql}

-   `CHECK`制約のサポート [#41711](https://github.com/pingcap/tidb/issues/41711) @[fzzf678](https://github.com/fzzf678)

    バージョン7.2.0以降では、 `CHECK`制約を使用して、テーブル内の1つまたは複数の列の値を、指定した条件を満たすように制限できます。 `CHECK`制約がテーブルに追加されると、TiDBはテーブルにデータを挿入または更新する前に、その制約が満たされているかどうかを確認します。制約を満たすデータのみが書き込まれます。

    この機能はデフォルトでは無効になっています。有効にするには、 [`tidb_enable_check_constraint`](/system-variables.md#tidb_enable_check_constraint-new-in-v720)システム変数を`ON`に設定してください。

    詳細については、[ドキュメント](/constraints.md#check)を参照してください。

### データベース操作 {#db-operations}

-   DDL ジョブは操作の一時停止と再開をサポートします (実験的) [#18015](https://github.com/pingcap/tidb/issues/18015) @[godouxm](https://github.com/godouxm)

    TiDB v7.2.0より前は、DDLジョブの実行中に業務のピークが発生した場合、業務への影響を軽減するには、DDLジョブを手動でキャンセルするしかありませんでした。v7.2.0では、TiDBはDDLジョブの一時停止と再開操作を導入しました。これらの操作により、ピーク時にDDLジョブを一時停止し、ピーク終了後に再開できるため、アプリケーションのワークロードへの影響を回避できます。

    例えば、 `ADMIN PAUSE DDL JOBS`または`ADMIN RESUME DDL JOBS`を使用して、複数の DDL ジョブを一時停止および再開できます。

    ```sql
    ADMIN PAUSE DDL JOBS 1,2;
    ADMIN RESUME DDL JOBS 1,2;
    ```

    詳細については、 [ドキュメント](/best-practices/ddl-introduction.md#ddl-related-commands)を参照してください。

### データ移行 {#data-migration}

-   データインポート効率を大幅に向上させる新しいSQLステートメント`IMPORT INTO`を導入（実験的） [#42930](https://github.com/pingcap/tidb/issues/42930) @[D3Hunter](https://github.com/D3Hunter)

    `IMPORT INTO`ステートメントは、 TiDB Lightningの[物理インポートモード](/tidb-lightning/tidb-lightning-physical-import-mode.md)機能を統合します。このステートメントを使用すると、CSV、SQL、PARQUET などの形式のデータを TiDB の空のテーブルにすばやくインポートできます。このインポート方法により、 TiDB Lightningの個別のデプロイと管理が不要になり、データインポートの複雑さが軽減され、インポート効率が大幅に向上します。

    Amazon S3 または GCS に保存されているデータ ファイルの場合、 [TiDB分散実行フレームワーク（DXF）](/tidb-distributed-execution-framework.md)が有効になっていると、 `IMPORT INTO`は、データ インポート ジョブを複数のサブ ジョブに分割し、それらを複数の TiDB ノードにスケジュールして並列インポートを行うこともサポートしており、インポート パフォーマンスをさらに向上させます。

    詳細については、 [ドキュメント](/sql-statements/sql-statement-import-into.md)を参照してください。

-   TiDB Lightningは、 Latin-1文字セットのソースファイルをTiDBにインポートすることをサポートします [#44434](https://github.com/pingcap/tidb/issues/44434) @[lance6716](https://github.com/lance6716)

    この機能を使用すると、 TiDB Lightningを使用して、Latin-1 文字セットのソースファイルを TiDB に直接インポートできます。v7.2.0 より前のバージョンでは、このようなファイルをインポートするには、追加の前処理または変換が必要でした。v7.2.0 以降では、 TiDB Lightningインポートタスクを設定する際に`character-set = "latin1"`を指定するだけで済みます。その後、 TiDB Lightning はインポート処理中に文字セットの変換を自動的に処理し、データの整合性と正確性を確保します。

    詳細については、 [ドキュメント](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)を参照してください。

## 互換性の変更 {#compatibility-changes}

> **注記：**
>
> このセクションでは、バージョン7.1.0から最新バージョン（7.2.0）にアップグレードする際に知っておくべき互換性の変更点について説明します。バージョン7.0.0以前のバージョンから最新バージョンにアップグレードする場合は、中間バージョンで導入された互換性の変更点も確認する必要があるかもしれません。

### 動作の変更 {#behavior-changes}

-   更新イベントを処理する際、TiCDC は、イベント内で主キーまたは NULL 以外の一意インデックス値が変更された場合、そのイベントを削除イベントと挿入イベントに分割します。詳細については、 [ドキュメント](/ticdc/ticdc-split-update-behavior.md#transactions-containing-a-single-update-change)を参照してください。
-   [`tidb_remove_orderby_in_subquery`](/system-variables.md#tidb_remove_orderby_in_subquery-new-in-v610)のデフォルト値を`OFF`から`ON`に変更します。これは、オプティマイザが不要なソート操作を回避するために、サブクエリから`ORDER BY`句を削除することを意味します。この変更により、クエリ結果の行の順序が変わる可能性があります。ISO/IEC SQL 標準では、クエリ結果がサブクエリで指定された`ORDER BY`ソートに従うことを要求していません。最終結果で特定の順序を確保する必要がある場合は、外側のクエリに`ORDER BY`句を追加します。アプリケーションがサブクエリのソートに依存している場合は、この変数を`OFF`に設定できます。以前のバージョンからアップグレードされたクラスターは、デフォルトでは以前の動作を維持します。

### システム変数 {#system-variables}

| 変数名                                                                                                                                                | 変更の種類  | 説明                                                                                                                                                                                                                                                                                     |
| -------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`last_insert_id`](/system-variables.md#last_insert_id)                                                                                            | 変更     | MySQL の最大値と一致させるため、最大値を`9223372036854775807`から`18446744073709551615`に変更します。                                                                                                                                                                                                            |
| [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache)                                                  | 変更     | 追加テストの後、デフォルト値を`OFF`から`ON`に変更します。これは、準備されていない実行プラン キャッシュが有効になることを意味します。                                                                                                                                                                                                                |
| [`tidb_remove_orderby_in_subquery`](/system-variables.md#tidb_remove_orderby_in_subquery-new-in-v610)                                              | 変更     | さらなるテストの後、デフォルト値を`OFF`から`ON`に変更します。これは、オプティマイザがサブクエリ内の`ORDER BY`句を削除することを意味します。                                                                                                                                                                                                        |
| [`tidb_analyze_skip_column_types`](/system-variables.md#tidb_analyze_skip_column_types-new-in-v720)                                                | 新しく追加された | `ANALYZE`コマンドを実行して統計情報を収集する際に、どのタイプの列を統計収集から除外するかを制御します。この変数は、 [`tidb_analyze_version = 2`](/system-variables.md#tidb_analyze_version-new-in-v510)の場合にのみ適用されます。 `ANALYZE TABLE t COLUMNS c1, ..., cn`の構文を使用する場合、指定された列のタイプが`tidb_analyze_skip_column_types`に含まれている場合、この列の統計情報は収集されません。 |
| [`tidb_enable_check_constraint`](/system-variables.md#tidb_enable_check_constraint-new-in-v720)                                                    | 新しく追加された | `CHECK`制約を有効にするかどうかを制御します。デフォルト値は`OFF`で、これはこの機能が無効になっていることを意味します。                                                                                                                                                                                                                      |
| [`tidb_enable_fast_table_check`](/system-variables.md#tidb_enable_fast_table_check-new-in-v720)                                                    | 新しく追加された | テーブル内のデータとインデックスの一貫性を迅速にチェックするために、チェックサムベースのアプローチを使用するかどうかを制御します。デフォルト値は`ON`で、これはこの機能が有効になっていることを意味します。                                                                                                                                                                                |
| [`tidb_enable_tiflash_pipeline_model`](https://docs-archive.pingcap.com/tidb/v7.2/system-variables#tidb_enable_tiflash_pipeline_model-new-in-v720) | 新しく追加された | TiFlashの新しい実行モデルで[パイプラインモデル](/tiflash/tiflash-pipeline-model.md)モデルを有効にするかどうかを制御します。デフォルト値は`OFF`で、パイプライン モデルが無効であることを意味します。                                                                                                                                                            |
| [`tidb_expensive_txn_time_threshold`](/system-variables.md#tidb_expensive_txn_time_threshold-new-in-v720)                                          | 新しく追加された | 高額トランザクションをログに記録するしきい値を制御します。デフォルト値は600秒です。トランザクションの所要時間がこのしきい値を超え、かつコミットもロールバックもされない場合、そのトランザクションは高額トランザクションとみなされ、ログに記録されます。                                                                                                                                                          |

### コンフィグレーションファイルパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーションパラメータ                                                                                                                                 | 変更の種類  | 説明                                                                                                                                                                                                                                                                                             |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB           | [`lite-init-stats`](/tidb-configuration-file.md#lite-init-stats-new-in-v710)                                                                    | 変更     | さらなるテストの結果、デフォルト値が`false`から`true`に変更されました。これは、TiDB の起動時にデフォルトで軽量統計初期化を使用して初期化効率を向上させることを意味します。                                                                                                                                                                                                 |
| TiDB           | [`force-init-stats`](/tidb-configuration-file.md#force-init-stats-new-in-v657-and-v710)                                                         | 変更     | [`lite-init-stats`](/tidb-configuration-file.md#lite-init-stats-new-in-v710)に合わせて、デフォルト値を`false`から`true`に変更します。これにより、TiDB の起動時に、TiDB は統計情報の初期化が完了するまでサービスの提供を待ちます。                                                                                                                             |
| TiKV           | [`rocksdb.[defaultcf|writecf|lockcf].compaction-guard-min-output-file-size`](/tikv-configuration-file.md#compaction-guard-min-output-file-size) | 変更     | RocksDB の圧縮タスクのデータ量を削減するために、デフォルト値を`"8MB"`から`"1MB"`に変更します。                                                                                                                                                                                                                                     |
| TiKV           | [`rocksdb.[defaultcf|writecf|lockcf].optimize-filters-for-memory`](/tikv-configuration-file.md#optimize-filters-for-memory-new-in-v720)         | 新しく追加された | メモリ内部の断片化を最小限に抑えるブルーム/リボンフィルタを生成するかどうかを制御します。                                                                                                                                                                                                                                                  |
| TiKV           | [`rocksdb.[defaultcf|writecf|lockcf].periodic-compaction-seconds`](/tikv-configuration-file.md#periodic-compaction-seconds-new-in-v720)         | 新しく追加された | 定期的な圧縮の間隔を制御します。この値よりも古い更新履歴を持つSSTファイルが圧縮対象として選択され、元のSSTファイルと同じ階層に書き換えられます。                                                                                                                                                                                                                    |
| TiKV           | [`rocksdb.[defaultcf|writecf|lockcf].ribbon-filter-above-level`](/tikv-configuration-file.md#ribbon-filter-above-level-new-in-v720)             | 新しく追加された | この値以上のレベルではリボンフィルターを使用し、この値未満のレベルではブロックベースではないブルームフィルターを使用するかどうかを制御します。                                                                                                                                                                                                                        |
| TiKV           | [`rocksdb.[defaultcf|writecf|lockcf].ttl`](/tikv-configuration-file.md#ttl-new-in-v720)                                                         | 新しく追加された | TTLよりも古い更新情報を持つSSTファイルは、自動的に圧縮対象として選択されます。                                                                                                                                                                                                                                                     |
| TiDB Lightning | `send-kv-pairs`                                                                                                                                 | 非推奨      | バージョン7.2.0以降、パラメータ`send-kv-pairs`は非推奨となりました。物理インポートモードでTiKVにデータを送信する際の1リクエストの最大サイズを制御するには、 [`send-kv-size`](/tidb-lightning/tidb-lightning-configuration.md)使用してください。                                                                                                                          |
| TiDB Lightning | [`character-set`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)                                                          | 変更     | データインポートでサポートされる文字セットに、新しい値オプション`latin1`が追加されました。このオプションを使用すると、Latin-1 文字セットのソースファイルをインポートできます。                                                                                                                                                                                                |
| TiDB Lightning | [`send-kv-size`](/tidb-lightning/tidb-lightning-configuration.md)                                                                               | 新しく追加された | 物理インポートモードでTiKVにデータを送信する際の、1リクエストあたりの最大サイズを指定します。キーと値のペアのサイズが指定されたしきい値に達すると、 TiDB Lightningは直ちにそれらをTiKVに送信します。これにより、大規模なワイドテーブルをインポートする際に、 TiDB Lightningノードがメモリ内に大量のキーと値のペアを蓄積することによって発生するメモリ不足（OOM）の問題を回避できます。このパラメータを調整することで、メモリ使用量とインポート速度のバランスを取り、インポートプロセスの安定性と効率性を向上させることができます。         |
| データ移行          | [`strict-optimistic-shard-mode`](/dm/feature-shard-merge-optimistic.md)                                                                         | 新しく追加された | この構成項目は、TiDB Data Migration v2.0 の DDL シャード マージ動作との互換性を確保するために使用されます。この構成項目は、楽観的モードで有効にできます。有効にすると、レプリケーション タスクはタイプ 2 の DDL ステートメントに遭遇した際に中断されます。複数のテーブルの DDL 変更間に依存関係があるシナリオでは、適切なタイミングで中断を行うことができます。アップストリームとダウンストリーム間のデータの一貫性を確保するため、レプリケーション タスクを再開する前に、各テーブルの DDL ステートメントを手動で処理する必要があります。 |
| TiCDC          | [`sink.protocol`](/ticdc/ticdc-changefeed-config.md)                                                                                            | 変更     | ダウンストリームが Kafka の場合に、新しい値オプション`"open-protocol"`を導入します。メッセージのエンコードに使用されるプロトコル形式を指定します。                                                                                                                                                                                                          |
| TiCDC          | [`sink.delete-only-output-handle-key-columns`](/ticdc/ticdc-changefeed-config.md)                                                               | 新しく追加された | DELETE イベントの出力を指定します。このパラメーターは`"canal-json"`および`"open-protocol"`プロトコルでのみ有効です。デフォルト値は`false`で、これはすべての列を出力することを意味します。これを`true`に設定すると、主キー列または一意インデックス列のみが出力されます。                                                                                                                                  |

## 改善点 {#improvements}

-   TiDB

    -   インデックススキャン範囲の構築ロジックを最適化し、複雑な条件をインデックススキャン範囲に変換することをサポートする[#41572](https://github.com/pingcap/tidb/issues/41572) [#44389](https://github.com/pingcap/tidb/issues/44389) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    -   新しい監視メトリクス`Stale Read OPS`と`Stale Read Traffic`を追加 [#43325](https://github.com/pingcap/tidb/issues/43325) @[you06](https://github.com/you06)
    -   古い読み取りの再試行リーダーがロックに遭遇した場合、TiDB はロックを解決した後、リーダーで強制的に再試行します。これにより、不要なオーバーヘッドが回避されます。 [#43659](https://github.com/pingcap/tidb/issues/43659) @[you06](https://github.com/you06)
    -   推定時間を使用して古い読み取りtsを計算し、古い読み取りのオーバーヘッドを削減します [#44215](https://github.com/pingcap/tidb/issues/44215) @[you06](https://github.com/you06)
    -   長時間実行されるトランザクションのログとシステム変数を追加する [#41471](https://github.com/pingcap/tidb/issues/41471) @[crazycs520](https://github.com/crazycs520)
    -   圧縮されたMySQLプロトコルを介したTiDBへの接続をサポートします。これにより、低帯域幅ネットワーク下でのデータ集約型クエリのパフォーマンスが向上し、帯域幅コストが削減されます。これは`zlib`と`zstd`ベースの圧縮の両方をサポートします。 [#22605](https://github.com/pingcap/tidb/issues/22605) @[dveeden](https://github.com/dveeden)
    -   `utf8`と`utf8bm3`の両方を従来の 3 バイト UTF-8 文字セットエンコーディングとして認識することで、従来の UTF-8 エンコーディングを持つテーブルを MySQL 8.0 から TiDB に移行しやすくなります。 [#26226](https://github.com/pingcap/tidb/issues/26226) @[dveeden](https://github.com/dveeden)
    -   `:=`ステートメントでの代入に`UPDATE`を使用するサポート [#44751](https://github.com/pingcap/tidb/issues/44751) @[CbcWestwolf](https://github.com/CbcWestwolf)

-   TiKV

    -   `pd.retry-interval`を使用した接続要求失敗などのシナリオで PD 接続の再試行間隔を設定することをサポートします [#14964](https://github.com/tikv/tikv/issues/14964) @[rleungx](https://github.com/rleungx)
    -   グローバルなリソース使用状況を組み込むことで、リソース制御スケジューリングアルゴリズムを最適化する [#14604](https://github.com/tikv/tikv/issues/14604) @[Connor1996](https://github.com/Connor1996)
    -   `check_leader`リクエストに gzip 圧縮を使用してトラフィックを削減します [#14553](https://github.com/tikv/tikv/issues/14553) @[you06](https://github.com/you06)
    -   `check_leader`リクエストに関連するメトリクスを追加 [#14658](https://github.com/tikv/tikv/issues/14658) @[you06](https://github.com/you06)
    -   TiKVが書き込みコマンドを処理する際の詳細な時間情報を提供する [#12362](https://github.com/tikv/tikv/issues/12362) @[cfzjywxk](https://github.com/cfzjywxk)

-   PD

    -   PDリーダー選出には別のgRPC接続を使用して、他のリクエストの影響を防ぐ [#6403](https://github.com/tikv/pd/issues/6403) @[rleungx](https://github.com/rleungx)
    -   マルチリージョンのシナリオにおけるホットスポットの問題を軽減するために、デフォルトでバケット分割を有効にします [#6433](https://github.com/tikv/pd/issues/6433) @[bufferflies](https://github.com/bufferflies)

-   ツール

    -   Backup & Restore (BR)

        -   Azure Blob Storage への共有アクセス署名 (SAS) によるアクセスをサポート [#44199](https://github.com/pingcap/tidb/issues/44199) @[Leavrth](https://github.com/Leavrth)

    -   TiCDC

        -   オブジェクトストレージサービスへのレプリケーションシナリオでDDL操作が発生した場合に、データファイルが格納されるディレクトリの構造を最適化する [#8891](https://github.com/pingcap/tiflow/issues/8891) @[CharlesCheung96](https://github.com/CharlesCheung96)
        -   KafkaへのレプリケーションシナリオにおけるOAUTHBEARER認証のサポート [#8865](https://github.com/pingcap/tiflow/issues/8865) @[Rustin170506](https://github.com/Rustin170506)
        -   Kafka [#9143](https://github.com/pingcap/tiflow/issues/9143) @[3AceShowHand](https://github.com/3AceShowHand)ショーハンドにレプリケーションシナリオの`DELETE`オペレーションのハンドルキーのみを出力するオプションを追加

    -   TiDB Data Migration (DM)

        -   MySQL 8.0 で圧縮バイナリログを増分レプリケーションのデータソースとして読み込むことをサポートする [#6381](https://github.com/pingcap/tiflow/issues/6381) @[dveeden](https://github.com/dveeden)

    -   TiDB Lightning

        -   リーダー切り替えによるエラーを回避するため、インポート時の再試行メカニズムを最適化する [#44263](https://github.com/pingcap/tidb/issues/44263) @[lance6716](https://github.com/lance6716)
        -   インポート後にSQLでチェックサムを検証して検証の安定性を向上させる [#41941](https://github.com/pingcap/tidb/issues/41941) @[GMHDBJD](https://github.com/GMHDBJD)
        -   幅の広いテーブルをインポートする際のTiDB Lightning OOM の問題の最適化 [#43853](https://github.com/pingcap/tidb/issues/43853) @[D3Hunter](https://github.com/D3Hunter)

## バグ修正 {#bug-fixes}

-   TiDB

    -   CTE を使用したクエリによって TiDB がハングする問題を修正[#43749](https://github.com/pingcap/tidb/issues/43749) [#36896](https://github.com/pingcap/tidb/issues/36896) @[guo-shaoge](https://github.com/guo-shaoge)
    -   `min, max`クエリ結果が正しくない問題を修正 [#43805](https://github.com/pingcap/tidb/issues/43805) @[wshwsh12](https://github.com/wshwsh12)
    -   `SHOW PROCESSLIST`ステートメントで、サブクエリ時間が長いステートメントのトランザクションの TxnStart が表示されない問題を修正します [#40851](https://github.com/pingcap/tidb/issues/40851) @[crazycs520](https://github.com/crazycs520)
    -   コプロセッサータスクに`TxnScope`がないため、古いデータの読み取りグローバル最適化が有効にならない問題を修正します [#43365](https://github.com/pingcap/tidb/issues/43365) @[you06](https://github.com/you06)
    -   フォロワー読み取りが再試行前にフラッシュバックエラーを処理しないためクエリエラーが発生する問題を修正します [#43673](https://github.com/pingcap/tidb/issues/43673) @[you06](https://github.com/you06)
    -   `ON UPDATE`ステートメントが主キーを正しく更新しない場合にデータとインデックスが不整合になる問題を修正 [#44565](https://github.com/pingcap/tidb/issues/44565) @[zyguan](https://github.com/zyguan)
    -   権限テーブルの一部の列における大文字小文字の区別に関する問題を修正しました [#41048](https://github.com/pingcap/tidb/issues/41048) @[bb7133](https://github.com/bb7133)
    -   `UNIX_TIMESTAMP()`関数の上限を`3001-01-19 03:14:07.999999 UTC`に変更し、MySQL 8.0.28 以降のバージョンと整合性を取る [#43987](https://github.com/pingcap/tidb/issues/43987) @[YangKeao](https://github.com/YangKeao)
    -   インジェストモードでインデックスの追加が失敗する問題を修正 [#44137](https://github.com/pingcap/tidb/issues/44137) @[tangenta](https://github.com/tangenta)
    -   ロールバック状態のDDLタスクをキャンセルすると、関連するメタデータにエラーが発生する問題を修正しました [#44143](https://github.com/pingcap/tidb/issues/44143) @[wjhuang2016](https://github.com/wjhuang2016)
    -   `memTracker`をカーソルフェッチで使用するとメモリリークが発生する問題を修正 [#44254](https://github.com/pingcap/tidb/issues/44254) @[YangKeao](https://github.com/YangKeao)
    -   データベースを削除するとGCの進行が遅くなる問題を修正 [#33069](https://github.com/pingcap/tidb/issues/33069) @[tiancaiamao](https://github.com/tiancaiamao)
    -   インデックス結合のプローブフェーズでパーティションテーブル内の対応する行が見つからない場合に TiDB がエラーを返す問題を修正 [#43686](https://github.com/pingcap/tidb/issues/43686) @[AilinKid](https://github.com/AilinKid)@[mjonss](https://github.com/mjonss)
    -   `SUBPARTITION`を使用してパーティションテーブルを作成する際に警告が表示されない問題を修正[#41198](https://github.com/pingcap/tidb/issues/41198) [#41200](https://github.com/pingcap/tidb/issues/41200) @[mjonss](https://github.com/mjonss)
    -   `MAX_EXECUTION_TIME`を超えるクエリが強制終了された場合、返されるエラーメッセージが MySQL のエラーメッセージと一致しない問題を修正します。 [#43031](https://github.com/pingcap/tidb/issues/43031) @[dveeden](https://github.com/dveeden)
    -   `LEADING`ヒントがブロックエイリアスのクエリをサポートしていない問題を修正 [#44645](https://github.com/pingcap/tidb/issues/44645) @[qw4990](https://github.com/qw4990)
    -   `LAST_INSERT_ID()`関数の戻り値の型を VARCHAR から LONGLONG に変更し、MySQL の戻り値の型と一致させます [#44574](https://github.com/pingcap/tidb/issues/44574) @[Defined2014](https://github.com/Defined2014)
    -   相関のないサブクエリを含むステートメントで共通テーブル式（CTE）を使用すると、誤った結果が返される可能性がある問題を修正しました [#44051](https://github.com/pingcap/tidb/issues/44051) @[winoros](https://github.com/winoros)
    -   結合したテーブルの再配置によって不正な外部結合結果が生じる可能性がある問題を修正 [#44314](https://github.com/pingcap/tidb/issues/44314) @[AilinKid](https://github.com/AilinKid)
    -   `PREPARE stmt FROM "ANALYZE TABLE xxx"`が`tidb_mem_quota_query`によって強制終了される可能性がある問題を修正 [#44320](https://github.com/pingcap/tidb/issues/44320) @[chrysan](https://github.com/chrysan)

-   TiKV

    -   TiKVが古い悲観的ロックの競合を処理する際にトランザクションが誤った値を返す問題を修正 [#13298](https://github.com/tikv/tikv/issues/13298) @[cfzjywxk](https://github.com/cfzjywxk)
    -   インメモリ悲観的ロックがフラッシュバックの失敗やデータの不整合を引き起こす可能性がある問題を修正 [#13303](https://github.com/tikv/tikv/issues/13303) @[JmPotato](https://github.com/JmPotato)
    -   TiKVが古いリクエストを処理する際にフェアロックが正しくない可能性がある問題を修正 [#13298](https://github.com/tikv/tikv/issues/13298) @[cfzjywxk](https://github.com/cfzjywxk)
    -   `autocommit`と`point get replica read`が線形化可能性を損なう可能性がある問題を修正 [#14715](https://github.com/tikv/tikv/issues/14715) @[cfzjywxk](https://github.com/cfzjywxk)

-   PD

    -   特定の特殊なケースで冗長レプリカが自動的に修復されない問題を修正 [#6573](https://github.com/tikv/pd/issues/6573) @[nolouch](https://github.com/nolouch)

-   TiFlash

    -   結合構築側のデータが非常に大きく、小さな文字列型の列が多数含まれている場合、クエリが必要以上にメモリを消費する可能性がある問題を修正します [#7416](https://github.com/pingcap/tiflash/issues/7416) @[yibin87](https://github.com/yibin87)

-   ツール

    -   Backup & Restore (BR)

        -   `checksum mismatch`が一部のケースで誤って報告される問題を修正 [#44472](https://github.com/pingcap/tidb/issues/44472) @[Leavrth](https://github.com/Leavrth)
        -   `resolved lock timeout`が一部のケースで誤って報告される問題を修正 [#43236](https://github.com/pingcap/tidb/issues/43236) @[YuJuncen](https://github.com/YuJuncen)
        -   統計情報の復元時に TiDB がpanic可能性がある問題を修正 [#44490](https://github.com/pingcap/tidb/issues/44490) @[tangenta](https://github.com/tangenta)

    -   TiCDC

        -   解決済みTSが一部のケースで正しく進まない問題を修正 [#8963](https://github.com/pingcap/tiflow/issues/8963) @[CharlesCheung96](https://github.com/CharlesCheung96)
        -   Avro または CSV プロトコルが使用されている場合、 `UPDATE`オペレーションが古い値を出力できない問題を修正 [#9086](https://github.com/pingcap/tiflow/issues/9086) @[3AceShowHand](https://github.com/3AceShowHand)
        -   Kafkaへのデータ複製時にダウンストリームメタデータを頻繁に読み取ることで発生する、ダウンストリームへの過剰な負荷の問題を修正します [#8959](https://github.com/pingcap/tiflow/issues/8959) @[Rustin170506](https://github.com/Rustin170506)
        -   TiDBまたはMySQLへのデータ複製時に、下流の双方向レプリケーション関連変数を頻繁に設定することで発生する、下流ログが多すぎる問題を修正しました [#9180](https://github.com/pingcap/tiflow/issues/9180) @[asddongmen](https://github.com/asddongmen)
        -   PDノードのクラッシュによってTiCDCノードが再起動する問題を修正 [#8868](https://github.com/pingcap/tiflow/issues/8868) @[asddongmen](https://github.com/asddongmen)
        -   TiCDCが下流のKafka-on-Pulsarで変更フィードを作成できない問題を修正 [#8892](https://github.com/pingcap/tiflow/issues/8892) @[Rustin170506](https://github.com/Rustin170506)

    -   TiDB Lightning

        -   `experimental.allow-expression-index`が有効でデフォルト値がUUIDの場合に発生するTiDB Lightningpanic問題を修正 [#44497](https://github.com/pingcap/tidb/issues/44497) @[lichunzhu](https://github.com/lichunzhu)
        -   データファイルの分割中にタスクが終了した際に発生するTiDB Lightningpanicの問題を修正 [#43195](https://github.com/pingcap/tidb/issues/43195) @[lance6716](https://github.com/lance6716)

## 貢献者 {#contributors}

TiDBコミュニティの以下の貢献者の皆様に感謝申し上げます。

-   [asjdf](https://github.com/asjdf)
-   [blacktear23](https://github.com/blacktear23)
-   [Cavan-xu](https://github.com/Cavan-xu)
-   [darraes](https://github.com/darraes)
-   [demoManito](https://github.com/demoManito)
-   [dhysum](https://github.com/dhysum)
-   [happy-v587](https://github.com/happy-v587)
-   [jiyfhust](https://github.com/jiyfhust)
-   [L-maple](https://github.com/L-maple)
-   [nyurik](https://github.com/nyurik)
-   [SeigeC](https://github.com/SeigeC)
-   [tangjingyu97](https://github.com/tangjingyu97)
