---
title: TiDB 6.2.0 Release Notes
summary: TiDB 6.2.0-DMRでは、ビジュアル実行プラン、モニタリングページ、ロックビューなどの新機能が導入されました。また、同時DDL操作をサポートし、集計操作のパフォーマンスが向上しています。TiKVは、CPU使用率の自動調整と詳細な構成情報リスト表示をサポートするようになりました。TiFlashは、データスキャン用のFastScanを追加し、エラー処理を改善しました。BRは、継続的なデータ検証をサポートし、Amazon S3バケットのリージョンを自動的に識別します。TiCDCは、DDLおよびDMLイベントのフィルタリングをサポートします。さらに、さまざまなツールにおいて、互換性の変更、バグ修正、および改善が行われています。
---

# TiDB 6.2.0 リリースノート {#tidb-6-2-0-release-notes}

発売日：2022年8月23日

TiDBバージョン: 6.2.0-DMR

> **注記：**
>
> TiDB 6.2.0-DMR ドキュメントは[アーカイブ済み](https://docs-archive.pingcap.com/tidb/v6.2/)です。 PingCAP は、TiDB データベースの[最新のLTSバージョン](https://docs.pingcap.com/tidb/stable)を使用することを推奨します。

バージョン6.2.0-DMRの主な新機能と改善点は以下のとおりです。

-   TiDB ダッシュボードは[視覚的な実行計画](https://docs-archive.pingcap.com/tidb/v6.2/dashboard-slow-query#visual-execution-plans)をサポートしており、実行計画をより直感的に表示できます。
-   パフォーマンス分析とチューニングをより効率的に行うために、TiDB ダッシュボードに[監視ページ](/dashboard/dashboard-monitoring.md)を追加します。
-   TiDB の[ロックビュー](/information-schema/information-schema-data-lock-waits.md)機能は、楽観的トランザクションの待機情報の表示をサポートし、ロック競合の迅速な特定を容易にします。
-   TiFlash は[ストレージフォーマットの新しいバージョン](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)をサポートし、安定性とパフォーマンスを強化します。
-   [きめ細かいシャッフル機能](/system-variables.md#tiflash_fine_grained_shuffle_batch_size-new-in-v620)ウィンドウ関数を複数のスレッドで並列実行できます。
-   新しい並行DDLフレームワーク：DDLステートメントのブロックが減り、実行効率が向上します。
-   TiKV は[CPU使用率を自動的に調整する](/tikv-configuration-file.md#background-quota-limiter)をサポートしており、安定した効率的なデータベース運用を保証します。
-   [特定時点リカバリ（PITR）](/br/backup-and-restore-overview.md)は、過去の任意の時点から TiDB クラスターのスナップショットを新しいクラスターに復元するために導入されました。
-   TiDB Lightning は、クラスター レベルではなく、物理インポート モードでテーブル[テーブルレベルでのスケジューリングを一時停止する](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#scope-of-pausing-scheduling-during-import)をサポートしています。
-   BR は[ユーザーおよび権限データの復元](/br/br-snapshot-guide.md#restore-tables-in-the-mysql-schema)サポートしており、バックアップと復元がよりスムーズになります。
-   TiCDC[特定の種類のDDLイベントをフィルタリングする](/ticdc/ticdc-filter.md)フィルタリングすることをサポートすることで、より多くのデータ レプリケーション シナリオを可能にします。
-   [`SAVEPOINT`機構](/sql-statements/sql-statement-savepoint.md)がサポートされており、トランザクション内のロールバックポイントを柔軟に制御できます。
-   TiDB は[1つの`ALTER TABLE`ステートメントだけで、複数の列またはインデックスの追加、削除、変更を行う](/sql-statements/sql-statement-alter-table.md)サポートしています。
-   [クラスター間RawKV複製](/tikv-configuration-file.md#api-version-new-in-v610)サポートされるようになりました。

## 新機能 {#new-features}

### SQL {#sql}

-   物理データ圧縮機能はGAです

    TiFlashのバックエンドは、特定の条件に基づいて物理データを自動的に圧縮し、不要なデータの蓄積を減らし、データストレージ構造を最適化します。

    TiFlashテーブルには、データ圧縮が自動的にトリガーされる前に、一定量の不要なデータが含まれていることがよくあります。この機能を使用すると、適切なタイミングを選択してSQLステートメントを手動で実行し、 TiFlash内の物理データを即座に圧縮できるため、ストレージ容量の使用量を削減し、クエリのパフォーマンスを向上させることができます。この機能はTiDB v6.1では実験的でしたが、TiDB v6.2.0で一般提供（GA）となりました。

    [ユーザー向けドキュメント](/sql-statements/sql-statement-alter-table-compact.md#alter-table--compact) [#4145](https://github.com/pingcap/tiflash/issues/4145) @[breezewish](https://github.com/breezewish)

### 可観測性 {#observability}

-   TiDBダッシュボードをPDから分離

    TiDBダッシュボードはPDから監視ノードに移動されました。これにより、TiDBダッシュボードがPDに与える影響が軽減され、PDの安定性が向上します。

    @[Hawkson-jee](https://github.com/Hawkson-jee)

-   TiDB Dashboardにモニタリングページが追加されました

    新しいモニタリング ページには、パフォーマンス チューニングに必要な主要な指標が表示され、これに基づいて[データベース時間によるパフォーマンスチューニング](/performance-tuning-methods.md)参照してパフォーマンスを分析および調整できます。

    具体的には、ユーザー応答時間とデータベース時間を全体的かつトップダウンの視点から分析することで、ユーザー応答時間のボトルネックがデータベースの問題によるものかどうかを確認できます。ボトルネックがデータベースにある場合は、データベース時間の概要とSQLレイテンシーの内訳を使用してボトルネックを特定し、パフォーマンスを調整できます。

    [ユーザー向けドキュメント](/dashboard/dashboard-monitoring.md) [#1381](https://github.com/pingcap/tidb-dashboard/issues/1381) @[YiniXu9506](https://github.com/YiniXu9506)

-   TiDB Dashboardはビジュアル実行プランをサポートしています

    TiDB Dashboardは、SQLステートメントページとモニタリングページを通じて、視覚的な実行プランと基本的な診断サービスを提供します。この機能により、クエリプランの各ステップを特定するための新しい視点が得られます。そのため、クエリ実行プランのすべての痕跡をより直感的に把握できます。

    この機能は、複雑で大規模なクエリの実行方法を学習する際に特に役立ちます。また、TiDB Dashboardは各クエリ実行プランについて、実行の詳細を自動的に分析し、潜在的な問題点を特定し、特定のクエリプランの実行時間を短縮するための最適化提案を提供します。

    [ユーザー向けドキュメント](https://docs-archive.pingcap.com/tidb/v6.2/dashboard-slow-query#visual-execution-plans) [#1224](https://github.com/pingcap/tidb-dashboard/issues/1224) @[time-and-fate](https://github.com/time-and-fate)

-   Lock ビューは、楽観的トランザクションの待機情報の表示をサポートしています。

    ロックの競合が多すぎると、深刻なパフォーマンスの問題を引き起こす可能性があり、そのような問題のトラブルシューティングにはロックの競合を検出することが不可欠です。v6.2.0 より前の TiDB では、 `INFORMATION_SCHEMA.DATA_LOCK_WAITS`システム ビューを使用してロックの競合関係を表示することはできましたが、楽観的トランザクションの待機情報は表示されませんでした。TiDB v6.2.0 では`DATA_LOCK_WAITS`ビューが拡張され、悲観的ロックによってブロックされている楽観的トランザクションがビューに一覧表示されます。この機能により、ユーザーはロックの競合を迅速に検出でき、アプリケーションの改善の基礎となるため、ロックの競合の頻度を減らし、全体的なパフォーマンスを向上させることができます。

    [ユーザー向けドキュメント](/information-schema/information-schema-data-lock-waits.md) [#34609](https://github.com/pingcap/tidb/issues/34609) @[longfangsong](https://github.com/longfangsong)

### パフォーマンス {#performance}

-   `LEADING`オプティマイザヒントを改善し、外部結合の順序付けをサポートするようにしました。

    バージョン 6.1.0 では、テーブルの結合順序を変更するためにオプティマイザヒント`LEADING`が導入されました。しかし、このヒントは外部結合を含むクエリには適用できませんでした。詳細については、 [`LEADING`文書](/optimizer-hints.md#leadingt1_name--tl_name-)を参照してください。バージョン 6.2.0 では、TiDB はこの制限を解除しました。外部結合を含むクエリでも、このヒントを使用してテーブルの結合順序を指定できるようになり、SQL の実行パフォーマンスが向上し、実行プランの急激な変更を回避できます。

    [ユーザー向けドキュメント](/optimizer-hints.md#leadingt1_name--tl_name-) [#29932](https://github.com/pingcap/tidb/issues/29932) @[Reminiscent](https://github.com/Reminiscent)

-   `SEMI_JOIN_REWRITE`クエリのパフォーマンスを向上させるために、新しいオプティマイザ`EXISTS` }を追加します。

    場合によっては、 `EXISTS`を含むクエリは最適な実行プランを取得できず、実行時間が長くなる可能性があります。v6.2.0 では、このようなシナリオに対応するためにオプティマイザに書き換えルールが追加され、クエリ内で`SEMI_JOIN_REWRITE`を使用することで、オプティマイザにクエリを強制的に書き換えさせ、クエリのパフォーマンスを向上させることができます。

    [ユーザー向けドキュメント](/optimizer-hints.md#semi_join_rewrite) [#35323](https://github.com/pingcap/tidb/issues/35323) @[winoros](https://github.com/winoros)

-   分析クエリのパフォーマンスを向上させるために、新しいオプティマイザヒント`MERGE`を追加します。

    共通テーブル式 (CTE) は、クエリロジックを簡素化する効果的な方法です。複雑なクエリを作成する際に広く使用されています。v6.2.0 より前のバージョンでは、 TiFlash環境で CTE を自動的に展開することができなかったため、MPP の実行効率が多少制限されていました。v6.2.0 では、MySQL 互換のオプティマイザヒント`MERGE`が導入されました。このヒントにより、オプティマイザは CTE インラインを展開できるようになり、CTE クエリ結果のコンシューマーがTiFlashでクエリを並行して実行できるようになったため、一部の分析クエリのパフォーマンスが向上しました。

    [ユーザー向けドキュメント](/optimizer-hints.md#merge) [#36122](https://github.com/pingcap/tidb/issues/36122) @[dayicklp](https://github.com/dayicklp)

-   一部の分析シナリオにおける集計操作のパフォーマンスを最適化する

    TiFlash を使用して OLAP シナリオで列に対して集計操作を実行する場合、集計列の分布が不均一であるために深刻なデータスキューが発生し、集計列にさまざまな値が含まれている場合、その列に対する`COUNT(DISTINCT)`クエリの実行効率が低下します。v6.2.0 では、単一の列に対する`COUNT(DISTINCT)`クエリのパフォーマンスを向上させるための新しい書き換えルールが導入されました。

    [ユーザー向けドキュメント](/system-variables.md#tidb_opt_skew_distinct_agg-new-in-v620) [#36169](https://github.com/pingcap/tidb/issues/36169) @[fixdb](https://github.com/fixdb)

-   TiDBは同時DDL操作をサポートしています

    TiDB v6.2.0では、新しい同時実行DDLフレームワークが導入されました。これにより、異なるテーブルオブジェクトに対してDDLステートメントを同時実行できるようになり、他のテーブルに対するDDL操作によってDDL操作がブロックされる問題が修正されました。さらに、TiDBは、複数のテーブルにインデックスを追加したり、列の型を変更したりする際に、同時DDL実行をサポートします。これにより、DDL実行の効率が向上します。

    [#32031](https://github.com/pingcap/tidb/issues/32031) @[wjhuang2016](https://github.com/wjhuang2016)

-   オプティマイザは文字列マッチングの推定精度を向上させます

    文字列マッチングのシナリオでは、オプティマイザが行数を正確に推定できない場合、最適な実行プランの生成に影響します。たとえば、条件が`like '%xyz'`または正規表現`regex ()`の場合です。このようなシナリオでの推定精度を向上させるため、TiDB v6.2.0 では推定方法を強化しました。新しい方法では、統計情報とシステム変数の TopN 情報を組み合わせて精度を向上させ、マッチングの選択性を手動で変更できるようにすることで、SQL のパフォーマンスを向上させています。

    [ユーザー向けドキュメント](/system-variables.md#tidb_default_string_match_selectivity-new-in-v620) [#36209](https://github.com/pingcap/tidb/issues/36209) @[time-and-fate](https://github.com/time-and-fate)

-   TiFlashにプッシュダウンされたウィンドウ関数は、複数のスレッドで実行できます。

    きめ細かいシャッフル機能を有効にすると、ウィンドウ関数を単一のスレッドではなく、複数のスレッドで実行できるようになります。この機能により、ユーザーの操作を変更することなく、クエリの応答時間を大幅に短縮できます。変数の値を調整することで、シャッフルの粒度を制御できます。

    [ユーザー向けドキュメント](/system-variables.md#tiflash_fine_grained_shuffle_batch_size-new-in-v620) [#4631](https://github.com/pingcap/tiflash/issues/4631) @[guo-shaoge](https://github.com/guo-shaoge)

-   TiFlashは、より新しいバージョンのストレージフォーマットをサポートしています。

    新しいストレージフォーマットは、高並列処理や高負荷なワークロード環境において、ガベージコレクション（GC）によって引き起こされるCPU使用率の上昇を緩和します。これにより、バックグラウンドタスクのI/Oトラフィックが大幅に削減され、高並列処理や高負荷なワークロード環境下での安定性が向上します。同時に、ディスク容量の増大やディスクの無駄遣いも大幅に削減できます。

    TiDB v6.2.0では、データはデフォルトで新しいストレージ形式で保存されます。TiFlashを以前のバージョンからv6.2.0にアップグレードする場合、以前のTiFlashバージョンでは新しいストレージ形式を認識できないため、 TiFlash上​​でインプレースダウングレードを実行することはできませんのでご注意ください。

    TiFlash のアップグレードの詳細については、 [TiFlashアップグレードガイド](/tiflash-upgrade-guide.md)を参照してください。

    [ユーザー向けドキュメント](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file) [#3594](https://github.com/pingcap/tiflash/issues/3594) @[JaySon-Huang](https://github.com/JaySon-Huang)@[lidezhu](https://github.com/lidezhu)@[jiaqizho](https://github.com/jiaqizho)

-   TiFlashは、複数の同時実行シナリオにおけるデータスキャン性能を最適化します（実験的）。

    TiFlashは、同一データの読み取り操作を統合することで、同一データの重複読み取りを削減し、複数の同時タスクにおけるリソースオーバーヘッドを最適化することで、データスキャン性能を向上させます。これにより、同一データが複数の同時タスクに関与する場合に、各タスクで同一データを個別に読み取る必要が生じたり、同一データが同時に複数回読み取られたりする状況を回避します。

    [ユーザー向けドキュメント](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file) [#5376](https://github.com/pingcap/tiflash/issues/5376) @[JinheLin](https://github.com/JinheLin)

-   TiFlashは、データの一貫性を犠牲にして読み書き速度を向上させるため、データスキャン用のFastScan機能を追加しました（実験的）。

    TiDBはv6.2.0でFastScanを導入しました。FastScanは整合性チェックをスキップすることで処理速度を大幅に向上させます。FastScanは、オフライン分析タスクなど、データの高精度や整合性が求められないシナリオに適しています。従来、 TiFlashはデータの整合性を確保するために、データスキャン処理中にデータの整合性チェックを実行し、複数の異なるバージョンから必要なデータを見つける必要がありました。

    TiDB v6.2.0 に以前のバージョンからアップグレードすると、データの一貫性を確保するために、すべてのテーブルで FastScan がデフォルトで有効になりません。FastScan は各テーブルごとに個別に有効にできます。TiDB v6.2.0 で FastScan が有効になっているテーブルは、それより低いバージョンにダウングレードすると無効になりますが、通常のデータ読み取りには影響しません。この場合、強力な一貫性読み取りと同等になります。

    [ユーザー向けドキュメント](/tiflash/use-fastscan.md) [#5252](https://github.com/pingcap/tiflash/issues/5252) @[hongyunyan](https://github.com/hongyunyan)

### 安定性 {#stability}

-   TiKVはCPU使用率の自動調整をサポートしています（実験的）。

    データベースは通常、内部処理を実行するためのバックグラウンドプロセスを備えています。統計情報を収集することで、パフォーマンスの問題を特定し、より適切な実行計画を作成し、データベースの安定性とパフォーマンスを向上させることができます。しかし、より効率的に情報を収集する方法、そして日常的な利用に影響を与えずにバックグラウンド処理とフォアグラウンド処理のリソースオーバーヘッドのバランスを取る方法は、データベース業界における長年の課題の一つでした。

    バージョン6.2.0以降、TiDBはTiKV設定ファイルを使用してバックグラウンドリクエストのCPU使用率を設定できるようになりました。これにより、TiKVでの統計情報の自動収集などのバックグラウンド操作のCPU使用率を制限し、極端な場合にバックグラウンド操作によるユーザー操作のリソース占有を回避できます。これにより、データベースの操作の安定性と効率性が確保されます。

    同時に、TiDBはCPU使用率の自動調整もサポートしています。TiKVは、インスタンスのCPU使用率に応じて、バックグラウンドリクエストが占めるCPUリソースを適応的に調整します。この機能はデフォルトでは無効になっています。

    [ユーザー向けドキュメント](/tikv-configuration-file.md#background-quota-limiter) [#12503](https://github.com/tikv/tikv/issues/12503) @[BornChanger](https://github.com/BornChanger)

### 使いやすさ {#ease-of-use}

-   TiKVは、コマンドラインフラグを使用して詳細な設定情報を一覧表示することをサポートしています。

    TiKV 設定ファイルは、TiKV インスタンスの管理に使用できます。しかし、長時間実行され、複数のユーザーによって管理されているインスタンスの場合、どの設定項目が変更されたか、デフォルト値は何かを把握するのは困難です。これは、クラスタのアップグレードやデータの移行時に混乱を招く可能性があります。TiDB v6.2.0 以降、tikv-server は、すべての TiKV 設定項目のデフォルト値と現在の値を一覧表示する新しいコマンドラインフラグ[`—-config-info`](/command-line-flags-for-tikv-configuration.md#--config-info-format)をサポートしており、TiKV プロセスの起動パラメータをユーザーがすばやく確認できるようになり、使いやすさが向上します。

    [ユーザー向けドキュメント](/command-line-flags-for-tikv-configuration.md#--config-info-format) [#12492](https://github.com/tikv/tikv/issues/12492)[グロルヴ](https://github.com/glorv)

### MySQLとの互換性 {#mysql-compatibility}

-   TiDBは、単一の`ALTER TABLE`ステートメントで複数の列またはインデックスを変更することをサポートしています。

    バージョン6.2.0より前は、TiDBは単一のDDL変更のみをサポートしていたため、異種データベースを移行する際にDDL操作の互換性が損なわれ、複雑なDDLステートメントをTiDBがサポートする複数の単純なDDLステートメントに変換するには余分な労力が必要でした。さらに、一部のユーザーはORMフレームワークを使用してSQLでアセンブリを作成していたため、SQLの互換性の問題も発生していました。バージョン6.2.0以降、TiDBは単一のSQLステートメントで複数のスキーマオブジェクトを変更できるようになり、ユーザーにとってSQLの実装が容易になり、使いやすさが向上しました。

    [ユーザー向けドキュメント](/sql-statements/sql-statement-alter-table.md) [#14766](https://github.com/pingcap/tidb/issues/14766) @[tangenta](https://github.com/tangenta)

-   トランザクションにおけるセーブポイントの設定をサポートする

    トランザクションとは、データベースがACID特性を保証する一連の連続した操作の論理的な集合です。複雑なアプリケーションシナリオでは、トランザクション内で多数の操作を管理する必要があり、場合によってはトランザクション内の操作をロールバックする必要が生じることもあります。「セーブポイント」は、トランザクションの内部実装のための名前付きメカニズムです。このメカニズムを使用することで、トランザクション内のロールバックポイントを柔軟に制御でき、より複雑なトランザクションを管理し、多様なアプリケーション設計においてより自由度を高めることができます。

    [ユーザー向けドキュメント](/sql-statements/sql-statement-savepoint.md) [#6840](https://github.com/pingcap/tidb/issues/6840) @[crazycs520](https://github.com/crazycs520)

### データ移行 {#data-migration}

-   BRはユーザーデータと権限データの復元をサポートしています

    BR は、通常の復元を実行する際に、ユーザーデータと権限データの復元をサポートします。ユーザーデータと権限データを復元するために、追加の復元プランは必要ありません。この機能を有効にするには、 BRを使用してデータを復元する際に`--with-sys-table`パラメーターを指定してください。

    [ユーザー向けドキュメント](/br/br-snapshot-guide.md#restore-tables-in-the-mysql-schema) [#35395](https://github.com/pingcap/tidb/issues/35395) @[D3Hunter](https://github.com/D3Hunter)

-   ログとスナップショットのバックアップと復元に基づくポイントインタイムリカバリ（PITR）をサポートします。

    PITRは、ログとスナップショットのバックアップおよび復元に基づいて実装されています。これにより、クラスタの履歴上の任意の時点のスナップショットを新しいクラスタに復元できます。この機能は、以下のニーズを満たします。

    -   ディザスタリカバリにおけるRPO（目標復旧時点）を20分未満に短縮する。
    -   アプリケーションからの書き込みエラーが発生した場合は、例えば、エラー発生前の状態にデータをロールバックするなどの方法で対処します。
    -   法令の要件を満たすため、履歴データの監査を実施する。

    この機能には使用上の制限があります。詳細はユーザーマニュアルを参照してください。

    [ユーザー向けドキュメント](/br/backup-and-restore-overview.md) [#29501](https://github.com/pingcap/tidb/issues/29501) @[joccau](https://github.com/joccau)

-   DMは継続的なデータ検証をサポートします（実験的）

    継続的なデータ検証は、データ移行中に上流のbinlogと下流に書き込まれたデータを継続的に比較するために使用されます。検証ツールは、データの不整合やレコードの欠落など、データの例外を特定します。

    この機能は、一般的な完全データ検証方式における検証の遅延や過剰なリソース消費といった問題を解決します。

    [ユーザー向けドキュメント](/dm/dm-continuous-data-validation.md) [#4426](https://github.com/pingcap/tiflow/issues/4426) @[D3Hunter](https://github.com/D3Hunter)@[buchuitoudegou](https://github.com/buchuitoudegou)

-   Amazon S3バケットのリージョンを自動的に識別する

    データ移行タスクでは、Amazon S3バケットのリージョンを自動的に識別できます。リージョンパラメータを明示的に渡す必要はありません。

    [#34275](https://github.com/pingcap/tidb/issues/34275) @[WangLe1321](https://github.com/WangLe1321)

-   TiDB Lightningのディスククォータ設定をサポート（実験的）

    TiDB Lightning が物理インポートモード (backend=&#39;local&#39;) でデータをインポートする場合、`sorted-kv-dir` にはソースデータを格納するのに十分な空き容量が必要です。ディスク容量が不足すると、インポートタスクが失敗する可能性があります。TiDB Lightning が使用するディスク容量の合計を制限するために、新しい`disk_quota`設定を使用すれば、`sorted-kv-dir` に十分なストレージ容量がない場合でも、インポートタスクを正常に完了できます。

    [ユーザー向けドキュメント](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#configure-disk-quota-new-in-v620) [#446](https://github.com/pingcap/tidb-lightning/issues/446) @[buchuitoudegou](https://github.com/buchuitoudegou)

-   TiDB Lightningは、物理インポートモードでの本番クラスタへのデータインポートをサポートしています。

    従来、 TiDB Lightningの物理インポートモード（backend=&#39;local&#39;）は、対象クラスタに大きな影響を与えていました。例えば、移行中にPDのグローバルスケジューリングが一時停止されるといった問題がありました。そのため、従来の物理インポートモードは、初期データインポートにのみ適していました。

    TiDB Lightningは、既存の物理インポートモードを改良しました。テーブルのスケジュールを一時停止できるようにすることで、インポートの影響をクラスタレベルからテーブルレベルにまで軽減します。つまり、インポートされていないテーブルの読み書きが可能になります。

    この機能には手動設定は不要です。TiDBクラスタがv6.1.0以降、かつTiDB Lightningがv6.2.0以降の場合、新しい物理インポートモードは自動的に有効になります。

    [ユーザー向けドキュメント](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#scope-of-pausing-scheduling-during-import) [#35148](https://github.com/pingcap/tidb/issues/35148) @[sleepymole](https://github.com/sleepymole)

-   [TiDB Lightningのユーザー向けドキュメント](/tidb-lightning/tidb-lightning-overview.md)ドキュメントをリファクタリングして、その構造をより合理的かつ明確にします。 「バックエンド」の用語も、新規ユーザーの理解の障壁を下げるために変更されています。

    -   「ローカルバックエンド」を「物理インポートモード」に置き換えてください。
    -   「tidb backend」を「logical import mode」に置き換えてください。

### TiDBデータ共有サブスクリプション {#tidb-data-share-subscription}

-   クラスター間RawKVレプリケーションのサポート（実験的）

    新しいコンポーネントTiKV-CDCを使用して、RawKVのデータ変更を購読し、そのデータ変更を下流のTiKVクラスタにリアルタイムで複製することをサポートします。これにより、クラスタ間の複製が可能になります。

    [ユーザー向けドキュメント](/tikv-configuration-file.md#api-version-new-in-v610) [#11965](https://github.com/tikv/tikv/issues/11965) @[pingyu](https://github.com/pingyu)

-   DDLおよびDMLイベントのフィルタリングをサポートします。

    特別な状況では、増分データ変更ログに対してフィルタルールを設定したい場合があります。たとえば、DROP TABLEなどの高リスクなDDLイベントをフィルタリングする場合などです。TiCDCはバージョン6.2.0以降、指定されたタイプのDDLイベントのフィルタリングと、SQL式に基づくDMLイベントのフィルタリングをサポートしています。これにより、TiCDCはより多くのデータレプリケーションシナリオに適用可能になります。

    [ユーザー向けドキュメント](/ticdc/ticdc-filter.md) [#6160](https://github.com/pingcap/tiflow/issues/6160) @[asddongmen](https://github.com/asddongmen)

## 互換性の変更 {#compatibility-changes}

### システム変数 {#system-variables}

| 変数名                                                                                                                     | 変更の種類  | 説明                                                                                                                                                                                                           |
| ----------------------------------------------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [tidb_enable_new_cost_interface](/system-variables.md#tidb_enable_new_cost_interface-new-in-v620)                       | 新しく追加された | この変数は[コストモデルの実装をリファクタリングしました](/cost-model.md#cost-model-version-2)を有効にするかどうかを制御します。                                                                                                                          |
| [tidb_cost_model_version](/system-variables.md#tidb_cost_model_version-new-in-v620)                                     | 新しく追加された | TiDBは、物理最適化の際にインデックスと演算子を選択するためにコストモデルを使用します。この変数は、コストモデルのバージョンを選択するために使用されます。TiDB v6.2.0では、内部テストで以前のバージョンよりも精度が向上したコストモデルバージョン2が導入されました。                                                                    |
| tidb_enable_concurrent_ddl                                                                                              | 新しく追加された | この変数は、TiDBが同時DDLステートメントを使用することを許可するかどうかを制御します。この変数は変更しないでください。この変数を無効にすると、リスクは不明であり、クラスタのメタデータが破損する可能性があります。                                                                                                 |
| [tiflash_fine_grained_shuffle_stream_count](/system-variables.md#tiflash_fine_grained_shuffle_stream_count-new-in-v620) | 新しく追加された | この変数は、ウィンドウ関数が実行のためにTiFlashにプッシュダウンされる際の、ウィンドウ関数実行の並行レベルを制御します。                                                                                                                                              |
| [tiflash_fine_grained_shuffle_batch_size](/system-variables.md#tiflash_fine_grained_shuffle_batch_size-new-in-v620)     | 新しく追加された | 細粒度シャッフルが有効になっている場合、 TiFlashにプッシュダウンされるウィンドウ関数を並列実行できます。この変数は、送信側から送信されるデータのバッチサイズを制御します。送信側は、累積行数がこの値を超えた時点でデータを送信します。                                                                                      |
| [tidb_default_string_match_selectivity](/system-variables.md#tidb_default_string_match_selectivity-new-in-v620)         | 新しく追加された | この変数は、行数を推定する際のフィルタ条件における`like` 、 `rlike` 、および`regexp`関数のデフォルトの選択性を設定するために関数。また、この変数は、これらの関数の推定を支援するために TopN を有効にするかどうかも制御します。                                                                               |
| [tidb_enable_analyze_snapshot](/system-variables.md#tidb_enable_analyze_snapshot-new-in-v620)                           | 新しく追加された | この変数は`ANALYZE`を実行する際に、履歴データまたは最新データを読み込むかどうかを制御します。                                                                                                                                                          |
| [tidb_generate_binary_plan](/system-variables.md#tidb_generate_binary_plan-new-in-v620)                                 | 新しく追加された | この変数は、スローログとステートメントサマリーにバイナリエンコードされた実行プランを生成するかどうかを制御します。                                                                                                                                                    |
| [tidb_opt_skew_distinct_agg](/system-variables.md#tidb_opt_skew_distinct_agg-new-in-v620)                               | 新しく追加された | この変数は、オプティマイザが`DISTINCT`を含む集計関数を2レベルの集計関数に書き換えるかどうかを設定します。たとえば`SELECT b, COUNT(DISTINCT a) FROM t GROUP BY b`を`SELECT b, COUNT(a) FROM (SELECT b, a FROM t GROUP BY b, a) t GROUP BY b`に書き換えます。              |
| [tidb_enable_noop_variables](/system-variables.md#tidb_enable_noop_variables-new-in-v620)                               | 新しく追加された | この変数は`noop`の結果に`SHOW [GLOBAL] VARIABLES` } 変数を表示するかどうかを制御します。                                                                                                                                                |
| [tidb_min_paging_size](/system-variables.md#tidb_min_paging_size-new-in-v620)                                           | 新しく追加された | この変数は、コプロセッサのページング要求処理中に処理される行の最大数を設定するために使用されます。                                                                                                                                                            |
| [tidb_txn_commit_batch_size](/system-variables.md#tidb_txn_commit_batch_size-new-in-v620)                               | 新しく追加された | この変数は、TiDBがTiKVに送信するトランザクションコミット要求のバッチサイズを制御するために使用されます。                                                                                                                                                     |
| tidb_enable_change_multi_schema                                                                                         | 削除済み     | この変数は、v6.2.0 以降では、デフォルトで 1 つの`ALTER TABLE`ステートメントで複数の列またはインデックスを変更できるため、削除されます。                                                                                                                              |
| [tidb_enable_outer_join_reorder](/system-variables.md#tidb_enable_outer_join_reorder-new-in-v610)                       | 修正済み     | この変数は、TiDB の結合したテーブルの再配置アルゴリズムが Outer Join をサポートするかどうかを制御します。v6.1.0 では、デフォルト値は`ON`であり、これは Join Reorder の Outer Join のサポートがデフォルトで有効になっていることを意味します。v6.2.0 以降では、デフォルト値は`OFF`であり、これはサポートがデフォルトで無効になっていることを意味します。 |

### コンフィグレーションファイルパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーション                                                                                                                | 変更の種類  | 説明                                                                                                  |
| -------------- | ------------------------------------------------------------------------------------------------------------------------- | -------- | --------------------------------------------------------------------------------------------------- |
| TiDB           | フィードバック確率                                                                                                                 | 削除済み     | この設定はもはや有効ではなく、推奨されません。                                                                             |
| TiDB           | クエリフィードバック制限                                                                                                              | 削除済み     | この設定はもはや有効ではなく、推奨されません。                                                                             |
| TiKV           | [サーバー.simplify-metrics](/tikv-configuration-file.md#simplify-metrics-new-in-v620)                                         | 新しく追加された | この設定では、返される監視メトリクスを簡略化するかどうかを指定します。                                                                 |
| TiKV           | [quota.background-cpu-time](/tikv-configuration-file.md#background-cpu-time-new-in-v620)                                  | 新しく追加された | この設定では、TiKVのバックグラウンド処理で読み取りおよび書き込み要求を処理するために使用されるCPUリソースのソフトリミットを指定します。                             |
| TiKV           | [quota.background-write-bandwidth](/tikv-configuration-file.md#background-write-bandwidth-new-in-v620)                    | 新しく追加された | この設定では、バックグラウンド トランザクションがデータを書き込む際の帯域幅のソフト リミットを指定します (現在は有効ではありません)。                               |
| TiKV           | [クォータ.バックグラウンド読み取り帯域幅](/tikv-configuration-file.md#background-read-bandwidth-new-in-v620)                                 | 新しく追加された | この設定では、バックグラウンドトランザクションとコプロセッサーがデータを読み取る際の帯域幅のソフトリミットを指定します（現在は有効ではありません）。                          |
| TiKV           | [quota.enable-auto-tune](/tikv-configuration-file.md#enable-auto-tune-new-in-v620)                                        | 新しく追加された | この設定では、クォータの自動調整を有効にするかどうかを指定します。この設定項目を有効にすると、TiKVはTiKVインスタンスの負荷に基づいて、バックグラウンドリクエストのクォータを動的に調整します。 |
| TiKV           | rocksdb.enable-pipelined-commit                                                                                           | 削除済み     | この設定はもはや有効ではありません。                                                                                  |
| TiKV           | gc-merge-rewrite                                                                                                          | 削除済み     | この設定はもはや有効ではありません。                                                                                  |
| TiKV           | [ログバックアップを有効にする](/tikv-configuration-file.md#enable-new-in-v620)                                                          | 新しく追加された | この設定は、TiKV 上でログバックアップを有効にするかどうかを制御します。                                                              |
| TiKV           | [ログバックアップ.ファイルサイズ制限](/tikv-configuration-file.md#file-size-limit-new-in-v620)                                             | 新しく追加された | この設定では、ログバックアップデータのサイズ制限を指定します。この制限に達すると、データは自動的に外部ストレージに書き込まれます。                                 |
| TiKV           | [ログバックアップ.初期スキャン保留中のメモリ割り当て](/tikv-configuration-file.md#initial-scan-pending-memory-quota-new-in-v620)                   | 新しく追加された | この設定では、増分スキャンデータを保存するために使用されるキャッシュのクォータを指定します。                                                      |
| TiKV           | [log-backup.max-flush-interval](/tikv-configuration-file.md#max-flush-interval-new-in-v620)                               | 新しく追加された | この設定では、ログバックアップにおいてバックアップデータを外部ストレージに書き込む最大間隔を指定します。                                              |
| TiKV           | [ログバックアップの初期スキャンレート制限](/tikv-configuration-file.md#initial-scan-rate-limit-new-in-v620)                                   | 新しく追加された | この設定では、ログバックアップにおける増分データスキャンのスループットのレート制限を指定します。                                                    |
| TiKV           | [log-backup.num-threads](/tikv-configuration-file.md#num-threads-new-in-v620)                                             | 新しく追加された | この設定では、ログバックアップで使用されるスレッド数を指定します。                                                                   |
| TiKV           | [log-backup.temp-path](/tikv-configuration-file.md#temp-path-new-in-v620)                                                 | 新しく追加された | この設定では、ログファイルが外部ストレージに書き込まれる前に一時的に保存されるパスを指定します。                                                  |
| TiKV           | [rocksdb.defaultcf.format-version](/tikv-configuration-file.md#format-version-new-in-v620)                                | 新しく追加された | SSTファイルのフォーマットバージョン。                                                                                |
| TiKV           | [rocksdb.writecf.format-version](/tikv-configuration-file.md#format-version-new-in-v620)                                  | 新しく追加された | SSTファイルのフォーマットバージョン。                                                                                |
| TiKV           | [rocksdb.lockcf.format-version](/tikv-configuration-file.md#format-version-new-in-v620)                                   | 新しく追加された | SSTファイルのフォーマットバージョン。                                                                                |
| PD             | レプリケーションモード.dr-auto-sync.wait-async-timeout                                                                               | 削除済み     | この設定は有効にならず、削除されます。                                                                                 |
| PD             | レプリケーションモード.dr-auto-sync.wait-sync-timeout                                                                                | 削除済み     | この設定は有効にならず、削除されます。                                                                                 |
| TiFlash        | [`storage.format_version`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                              | 修正済み     | `format_version`のデフォルト値が`4`に変更されます。これは v6.2.0 以降のバージョンのデフォルト形式であり、書き込み増幅とバックグラウンド タスクのリソース消費を削減します。 |
| TiFlash        | [profiles.default.dt_enable_read_thread](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                | 新しく追加された | この設定は、ストレージエンジンからの読み取り要求を処理するためにスレッド プールを使用するかどうかを制御します。デフォルト値は`false`です。                         |
| TiFlash        | [profiles.default.dt_page_gc_threshold](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                 | 新しく追加された | この設定では、PageStorageデータファイル内の有効データの最小比率を指定します。                                                        |
| TiCDC          | [--overwrite-checkpoint-ts](/ticdc/ticdc-manage-changefeed.md#resume-a-replication-task)                                  | 新しく追加された | この設定は`cdc cli changefeed resume`サブコマンドに追加されます。                                                      |
| TiCDC          | [--確認しない](/ticdc/ticdc-manage-changefeed.md#resume-a-replication-task)                                                    | 新しく追加された | この設定は`cdc cli changefeed resume`サブコマンドに追加されます。                                                      |
| DM             | [モード](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)                                      | 新しく追加された | この設定はバリデーターパラメータです。オプションの値は`full` 、 `fast` 、および`none`です。デフォルト値は`none`で、これはデータの検証を行いません。             |
| DM             | [労働者数](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)                                     | 新しく追加された | この設定はバリデーターパラメータであり、バックグラウンドで実行される検証ワーカーの数を指定します。デフォルト値は`4`です。                                      |
| DM             | [行エラー遅延](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)                                   | 新しく追加された | この設定はバリデーターパラメータです。指定された時間内に検証が行われなかった場合、その行はエラー行としてマークされます。デフォルト値は30mで、これは30分を意味します。               |
| TiDB Lightning | [tikv-importer.store-write-bwlimit](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)                  | 新しく追加された | この設定は、TiDB Lightning が各 TiKV ストアにデータを書き込む際の書き込み帯域幅を決定します。デフォルト値は`0`で、帯域幅に制限がないことを示します。              |
| TiDB Lightning | [tikv-importer.disk-quota](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#configure-disk-quota-new-in-v620) | 新しく追加された | この構成により、TiDB Lightningが使用するストレージ容量が制限されます。                                                        |

### その他 {#others}

-   TiFlash `format_version` `4`から`3`にダウングレードすることはできません。詳細については、 [TiFlashアップグレードガイド](/tiflash-upgrade-guide.md)を参照してください。
-   バージョン6.2.0以降では、デフォルト値の`false`を`dt_enable_logical_split`のままにして、 `true`に変更しないことを強くお勧めします。詳細は、既知の問題[#5576](https://github.com/pingcap/tiflash/issues/5576)を参照してください。
-   バックアップ クラスタにTiFlashレプリカがある場合、PITR を実行すると、リストア クラスタにはTiFlashレプリカ内のデータが含まれません。TiFlash レプリカからデータをリストアするには、 TiFlashレプリカを手動で構成する必要があります。 `exchange partition` DDL ステートメントを実行すると、PITR が失敗する可能性があります。アップTiFlashデータベースが TiDB Lightning の物理インポート モードを使用してデータをインポートする場合、ログ バックアップでデータをバックアップできません。データ インポート後にフル バックアップを実行することをお勧めします。PITR のその他の互換性の問題については、 [PITRの制限](/br/backup-and-restore-overview.md#before-you-use)参照してください。
-   TiDB v6.2.0以降では、データ復元時に`mysql`パラメータを指定することで`--with-sys-table=true`スキーマのテーブルを復元できます。
-   `ALTER TABLE`ステートメントを実行して複数の列またはインデックスを追加、削除、または変更する場合、TiDB は同じ DDL ステートメントの変更内容に関わらず、ステートメント実行前後のテーブルを比較してテーブルの一貫性をチェックします。DDL の実行順序は、シナリオによっては MySQL と完全には互換性がない場合があります。
-   TiDBコンポーネントがv6.2.0以降の場合、TiKVコンポーネントはv6.2.0より前のバージョンであってはなりません。
-   TiKV は[動的構成](/dynamic-config.md#modify-tikv-configuration-dynamically)をサポートする構成アイテム`split.region-cpu-overload-threshold-ratio`を追加します。
-   スロークエリログ、 `information_schema.statements_summary` 、および`information_schema.slow_query`は`binary_plan` 、またはバイナリ形式でエンコードされた実行プランをエクスポートできます。
-   `SHOW TABLE ... REGIONS`ステートメントに、 `SCHEDULING_CONSTRAINTS`と`SCHEDULING_STATE` 2 つの列が追加されます。これらはそれぞれ、SQL の配置におけるリージョンスケジューリング制約と現在のスケジューリング状態を示します。
-   TiDB v6.2.0以降では、 [TiKV-CDC](https://github.com/tikv/migration/tree/main/cdc)を介してRawKVのデータ変更をキャプチャできます。
-   `ROLLBACK TO SAVEPOINT`を使用してトランザクションを特定のセーブポイントまでロールバックする場合、MySQL は指定されたセーブポイント以降に保持されているロックのみを解放しますが、TiDB の悲観的トランザクションでは、TiDB は指定されたセーブポイント以降に保持されているロックをすぐには解放しません。代わりに、TiDB はトランザクションがコミットまたはロールバックされたときにすべてのロックを解放します。
-   TiDB v6.2.0以降、 `SELECT tidb_version()`ステートメントはストアタイプ（tikvまたはunistore）も返します。
-   TiDBには隠しシステム変数はなくなりました。
-   TiDB v6.2.0では、2つの新しいシステムテーブルが導入されました。
    -   `INFORMATION_SCHEMA.VARIABLES_INFO` : TiDB システム変数に関する情報を表示するために使用されます。
    -   `PERFORMANCE_SCHEMA.SESSION_VARIABLES` : TiDB セッションレベルのシステム変数に関する情報を表示するために使用されます。

## 削除された機能 {#removed-feature}

TiDB v6.2.0以降、 BRを使用したRawKVのバックアップと復元は非推奨となりました。

## 改善点 {#improvements}

-   TiDB

    -   `SHOW COUNT(*) WARNINGS`および`SHOW COUNT(*) ERRORS`ステートメントのサポート [#25068](https://github.com/pingcap/tidb/issues/25068) @[likzn](https://github.com/likzn)

    -   一部のシステム変数に対する検証チェックを追加 [#35048](https://github.com/pingcap/tidb/issues/35048) @[morgo](https://github.com/morgo)

    -   一部の型変換のエラー メッセージを最適化 [#32744](https://github.com/pingcap/tidb/issues/32744) @[fanrenhoo](https://github.com/fanrenhoo)

    -   `KILL`コマンドが DDL 操作をサポートするようになりました [#24144](https://github.com/pingcap/tidb/issues/24144) @[morgo](https://github.com/morgo)

    -   `SHOW TABLES/DATABASES LIKE …`の出力を MySQL とより互換性のあるものにしてください。出力の列名には`LIKE`の値が含まれています [#35116](https://github.com/pingcap/tidb/issues/35116) @[likzn](https://github.com/likzn)

    -   JSON関連関数のパフォーマンスを改善する [#35859](https://github.com/pingcap/tidb/issues/35859) @[wjhuang2016](https://github.com/wjhuang2016)

    -   SHA-2を使用したパスワードログインの検証速度を向上 [#35998](https://github.com/pingcap/tidb/issues/35998) @[virusdefender](https://github.com/virusdefender)

    -   ログ出力の一部を簡略化 [#36011](https://github.com/pingcap/tidb/issues/36011) @[dveeden](https://github.com/dveeden)

    -   コプロセッサー通信プロトコルを最適化します。これにより、TiDB プロセスがデータを読み取る際のメモリ消費量を大幅に削減し、Dumplingによるテーブルのスキャンとデータのエクスポートのシナリオにおける OOM 問題をさらに軽減できます。システム変数`tidb_enable_paging`を導入し、この通信プロトコルを有効にするかどうか (SESSION または GLOBAL のスコープで) を制御します。このプロトコルはデフォルトでは無効になっています。有効にするには、変数の値を`true`に設定します。 [#35633](https://github.com/pingcap/tidb/issues/35633) @[tiancaiamao](https://github.com/tiancaiamao)@[wshwsh12](https://github.com/wshwsh12)

    -   一部の演算子 (HashJoin、HashAgg、Update、Delete) のメモリ追跡の精度を最適化しました ( [#35634](https://github.com/pingcap/tidb/issues/35634) 、 [#35631](https://github.com/pingcap/tidb/issues/35631) 、 [#35635](https://github.com/pingcap/tidb/issues/35635) @[wshwsh12](https://github.com/wshwsh12) ) ( [#34096](https://github.com/pingcap/tidb/issues/34096) @[ekexium](https://github.com/ekexium))

    -   システム テーブル`INFORMATION_SCHEMA.DATA_LOCK_WAIT`楽観的トランザクションのロック情報の記録をサポートしています [#34609](https://github.com/pingcap/tidb/issues/34609) @[longfangsong](https://github.com/longfangsong)

    -   トランザクションの監視メトリクスを追加 [#34456](https://github.com/pingcap/tidb/issues/34456) @[longfangsong](https://github.com/longfangsong)

-   TiKV

    -   HTTPボディサイズを削減するために、gzipを使用してメトリクスレスポンスを圧縮するサポート [#12355](https://github.com/tikv/tikv/issues/12355) @[glorv](https://github.com/glorv)
    -   Grafana ダッシュボードの TiKV パネルの読みやすさを改善 [#12007](https://github.com/tikv/tikv/issues/12007) @[kevin-xianliu](https://github.com/kevin-xianliu)
    -   Applyオペレーターのコミットパイプラインのパフォーマンスを最適化する [#12898](https://github.com/tikv/tikv/issues/12898) @[ethercflow](https://github.com/ethercflow)
    -   RocksDB で同時に実行されるサブコンパクション操作の数を動的に変更する機能のサポート ( `rocksdb.max-sub-compactions` ) [#13145](https://github.com/tikv/tikv/issues/13145) @[ethercflow](https://github.com/ethercflow)

-   PD

    -   リージョンのCPU使用率の統計的側面をサポートし、ロードベース分割の使用シナリオを強化する [#12063](https://github.com/tikv/tikv/issues/12063) @[JmPotato](https://github.com/JmPotato)

-   TiFlash

    -   TiFlash MPP エンジンのエラー処理を改良し、安定性を向上 [#5095](https://github.com/pingcap/tiflash/issues/5095) @[windtalker](https://github.com/windtalker) @[yibin87](https://github.com/yibin87)

    -   UTF8_BIN と UTF8MB4_BIN 照合順序の比較と並べ替えを最適化します [#5294](https://github.com/pingcap/tiflash/issues/5294) @[solotzg](https://github.com/solotzg)

-   ツール

    -   バックアップと復元 (BR)

        -   大規模クラスタバックアップにおけるS3レート制限によるバックアップ失敗を修正するため、バックアップデータディレクトリ構造を調整しました [#30087](https://github.com/pingcap/tidb/issues/30087) @[MoCuishle28](https://github.com/MoCuishle28)

    -   TiCDC

        -   複数リージョンシナリオにおけるランタイムコンテキスト切り替えによるパフォーマンスオーバーヘッドを削減 [#5610](https://github.com/pingcap/tiflow/issues/5610) @[hicqu](https://github.com/hicqu)

        -   REDO ログのパフォーマンスを最適化し、メタおよびデータの不整合の問題を修正します ( [#6011](https://github.com/pingcap/tiflow/issues/6011) @[CharlesCheung96](https://github.com/CharlesCheung96) ) ( [#5924](https://github.com/pingcap/tiflow/issues/5924) @[zhaoxinyu](https://github.com/zhaoxinyu)) ( [#6277](https://github.com/pingcap/tiflow/issues/6277)[ヒック](https://github.com/hicqu))

    -   TiDB Lightning

        -   EOF、読み取りインデックスが準備できていない、コプロセッサータイムアウトなど、再試行可能なエラーをさらに追加[#36674](https://github.com/pingcap/tidb/issues/36674) 、 [#36566](https://github.com/pingcap/tidb/issues/36566) @[D3Hunter](https://github.com/D3Hunter)

    -   TiUP

        -   TiUPを使用して新しいクラスターをデプロイする場合、node-exporterはバージョン[1.3.1](https://github.com/prometheus/node_exporter/releases/tag/v1.3.1)を、blackbox-exporterはバージョン[0.21.1](https://github.com/prometheus/blackbox_exporter/releases/tag/v0.21.1)を使用するため、さまざまなシステムや環境でのデプロイが確実に成功します。

## バグ修正 {#bug-fixes}

-   TiDB

    -   クエリ条件でパーティションキーが使用され、照合順序がクエリパーティションテーブルのものと異なる場合に、パーティションが正しく削除されない問題を修正します [#32749](https://github.com/pingcap/tidb/issues/32749) @[mjonss](https://github.com/mjonss)
    -   `SET ROLE`ホストに大文字が含まれている場合に付与されたロールと一致しない問題を修正 [#33061](https://github.com/pingcap/tidb/issues/33061) @[morgo](https://github.com/morgo)
    -   `auto_increment`を持つ列を削除できない問題を修正 [#34891](https://github.com/pingcap/tidb/issues/34891) @[Defined2014](https://github.com/Defined2014)
    -   `SHOW CONFIG`に削除された設定項目が表示される問題を修正 [#34867](https://github.com/pingcap/tidb/issues/34867) @[morgo](https://github.com/morgo)
    -   `SHOW DATABASES LIKE …`が大文字と小文字を区別する問題を修正 [#34766](https://github.com/pingcap/tidb/issues/34766) @[e1ijah1](https://github.com/e1ijah1)
    -   `SHOW TABLE STATUS LIKE ...`が大文字小文字を区別する問題を修正 [#7518](https://github.com/pingcap/tidb/issues/7518) @[likzn](https://github.com/likzn)
    -   `max-index-length`非厳格モードでエラーを報告する問題を修正 [#34931](https://github.com/pingcap/tidb/issues/34931) @[e1ijah1](https://github.com/e1ijah1)
    -   `ALTER COLUMN ... DROP DEFAULT`が機能しない問題を修正 [#35018](https://github.com/pingcap/tidb/issues/35018) @[Defined2014](https://github.com/Defined2014)
    -   テーブル作成時に、デフォルト値と列の型が一致せず、自動的に修正されない問題を修正しました [#34881](https://github.com/pingcap/tidb/issues/34881) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    -   `mysql.columns_priv`を実行した後、 `DROP USER`テーブルのデータが同期的に削除されない問題を修正しました [#35059](https://github.com/pingcap/tidb/issues/35059) @[lcwangchao](https://github.com/lcwangchao)
    -   一部のシステムのスキーマ内でテーブルを作成することを禁止することで、DDL ジャムの問題を修正します [#35205](https://github.com/pingcap/tidb/issues/35205) @[tangenta](https://github.com/tangenta)
    -   パーティション化されたテーブルをクエリした際に、場合によっては「index-out-of-range」および「non used index」エラーが報告される問題を修正しました [#35181](https://github.com/pingcap/tidb/issues/35181) @[mjonss](https://github.com/mjonss)
    -   `INTERVAL expr unit + expr`がエラーを報告する可能性がある問題を修正 [#30253](https://github.com/pingcap/tidb/issues/30253) @[mjonss](https://github.com/mjonss)
    -   トランザクション内で作成された一時テーブルが見つからないバグを修正 [#35644](https://github.com/pingcap/tidb/issues/35644) @[djshow832](https://github.com/djshow832)
    -   `ENUM`列に照合順序を設定する際に発生するpanic問題を修正しました [#31637](https://github.com/pingcap/tidb/issues/31637) @[wjhuang2016](https://github.com/wjhuang2016)
    -   PDノードが1つダウンした際に、他のPDノードを再試行しないために`information_schema.TIKV_REGION_STATUS`のクエリが失敗する問題を修正しました [#35708](https://github.com/pingcap/tidb/issues/35708) @[tangenta](https://github.com/tangenta)
    -   `SHOW CREATE TABLE …`が`ENUM`の後にセットまたは`SET character_set_results = GBK`列を正しく表示できない問題 [#31338](https://github.com/pingcap/tidb/issues/31338) @[tangenta](https://github.com/tangenta)
    -   システム変数`tidb_log_file_max_days`と`tidb_config`のスコープの誤りを修正 [#35190](https://github.com/pingcap/tidb/issues/35190) @[morgo](https://github.com/morgo)
    -   `SHOW CREATE TABLE`の出力が、 `ENUM`または`SET`列の MySQL と互換性がない問題を修正します [#36317](https://github.com/pingcap/tidb/issues/36317) @[Defined2014](https://github.com/Defined2014)
    -   テーブル作成時に`LONG BYTE`列の動作が MySQL と互換性がない問題を修正しました [#36239](https://github.com/pingcap/tidb/issues/36239) @[Defined2014](https://github.com/Defined2014)
    -   `auto_increment = x`が一時テーブルに適用されない問題を修正 [#36224](https://github.com/pingcap/tidb/issues/36224) @[djshow832](https://github.com/djshow832)
    -   列を同時に変更する際の誤ったデフォルト値を修正 [#35846](https://github.com/pingcap/tidb/issues/35846) @[wjhuang2016](https://github.com/wjhuang2016)
    -   可用性を向上させるために、異常な TiKV ノードにリクエストを送信しないようにします [#34906](https://github.com/pingcap/tidb/issues/34906) @[sticnarf](https://github.com/sticnarf)
    -   LOAD DATA ステートメントで列リストが機能しない問題を修正 [#35198](https://github.com/pingcap/tidb/issues/35198) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
    -   一部のシナリオで悲観的ロックが非一意のセカンダリインデックスに誤って追加される問題を修正 [#36235](https://github.com/pingcap/tidb/issues/36235) @[ekexium](https://github.com/ekexium)

-   TiKV

    -   悲観的トランザクションで`WriteConflict`エラーを報告しないようにします [#11612](https://github.com/tikv/tikv/issues/11612) @[sticnarf](https://github.com/sticnarf)
    -   非同期コミットが有効になっている場合に、悲観的トランザクションで発生する可能性のある重複コミット レコードを修正 [#12615](https://github.com/tikv/tikv/issues/12615) @[sticnarf](https://github.com/sticnarf)
    -   `storage.api-version`を`1`から`2`に変更した際に TiKV がパニック [#12600](https://github.com/tikv/tikv/issues/12600) @[pingyu](https://github.com/pingyu)
    -   TiKVとPD間のリージョンサイズ構成の不整合の問題を修正 [#12518](https://github.com/tikv/tikv/issues/12518) @[5kbpers](https://github.com/5kbpers)
    -   TiKV が PD クライアントに再接続し続ける問題を修正[#12506](https://github.com/tikv/tikv/issues/12506) 、 [#12827](https://github.com/tikv/tikv/issues/12827) @[Connor1996](https://github.com/Connor1996)
    -   TiKVが空文字列の型変換時にパニックを起こす問題を修正 [#12673](https://github.com/tikv/tikv/issues/12673) @[wshwsh12](https://github.com/wshwsh12)
    -   `DATETIME`の値に小数が含まれている場合と`Z`の値が含まれている場合に発生する時間解析エラーの問題を修正しました [#12739](https://github.com/tikv/tikv/issues/12739) @[gengliqi](https://github.com/gengliqi)
    -   Apply オペレーターが TiKV RocksDB に書き込む perf コンテキストが粗粒度である問題を修正 [#11044](https://github.com/tikv/tikv/issues/11044) @[LykxSassinator](https://github.com/LykxSassinator)
    -   [バックアップ](/tikv-configuration-file.md#backup)/[インポート](/tikv-configuration-file.md#import)/ [CDC](/tikv-configuration-file.md#cdc)の設定が無効な場合にTiKVが起動できない問題を修正 [#12771](https://github.com/tikv/tikv/issues/12771) @[3pointer](https://github.com/3pointer)
    -   ピアが分割され、同時に破棄される際に発生する可能性のあるpanic問題を修正 [#12825](https://github.com/tikv/tikv/issues/12825) @[BusyJay](https://github.com/BusyJay)
    -   リージョンマージプロセスでソースピアがスナップショットによってログを追いついたときに発生する可能性のpanic問題を修正 [#12663](https://github.com/tikv/tikv/issues/12663) @[BusyJay](https://github.com/BusyJay)
    -   `max_sample_size`が`0`に設定されている場合に統計分析で発生するpanic問題を修正 [#11192](https://github.com/tikv/tikv/issues/11192) @[LykxSassinator](https://github.com/LykxSassinator)
    -   Raft Engineが有効になっているときに暗号化キーがクリーンアップされない問題を修正 [#12890](https://github.com/tikv/tikv/issues/12890) @[tabokie](https://github.com/tabokie)
    -   `get_valid_int_prefix`関数が TiDB と互換性がない問題を修正します。例えば、 `FLOAT`型が`INT`に誤って変換されていました [#13045](https://github.com/tikv/tikv/issues/13045) @[guo-shaoge](https://github.com/guo-shaoge)
    -   新しいリージョンのコミットログ期間が長すぎるためにQPSが低下する問題を修正しました [#13077](https://github.com/tikv/tikv/issues/13077) @[Connor1996](https://github.com/Connor1996)
    -   リージョンのハートビートが中断された後、PD が TiKV に再接続しない問題を修正 [#12934](https://github.com/tikv/tikv/issues/12934) @[bufferflies](https://github.com/bufferflies)

-   ツール

    -   バックアップと復元 (BR)

        -   レート制限付きバックアップタスク完了後にBRがレート制限をリセットしない問題を修正 [#31722](https://github.com/pingcap/tidb/issues/31722) @[MoCuishle28](https://github.com/MoCuishle28)

## 貢献者 {#contributors}

TiDBコミュニティの以下の貢献者の皆様に感謝申し上げます。

-   [e1ijah1](https://github.com/e1ijah1)
-   [PrajwalBorkar](https://github.com/PrajwalBorkar)
-   [likzn](https://github.com/likzn)
-   [rahulk789](https://github.com/rahulk789)
-   [virusdefender](https://github.com/virusdefender)
-   [joycse06](https://github.com/joycse06)
-   [morgo](https://github.com/morgo)
-   [ixuh12](https://github.com/ixuh12)
-   [blacktear23](https://github.com/blacktear23)
-   [johnhaxx7](https://github.com/johnhaxx7)
-   [GoGim1](https://github.com/GoGim1)
-   [renbaoshuo](https://github.com/renbaoshuo)
-   [Zheaoli](https://github.com/Zheaoli)
-   [fanrenhoo](https://github.com/fanrenhoo)
-   [njuwelkin](https://github.com/njuwelkin)
-   [wirybeaver](https://github.com/wirybeaver)
-   [hey-kong](https://github.com/hey-kong)
-   [fatelei](https://github.com/fatelei)
-   [eastfisher](https://github.com/eastfisher): 初回貢献者
-   [Juneezee](https://github.com/Juneezee): 初回貢献者
