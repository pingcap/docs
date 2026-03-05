---
title: TiDB 6.2.0 Release Notes
summary: TiDB 6.2.0-DMRでは、ビジュアル実行プラン、モニタリングページ、ロックビューなどの新機能が導入されています。また、同時DDL操作のサポートと集計操作のパフォーマンス向上も実現しています。TiKVでは、CPU使用率の自動チューニングと詳細な設定情報リストのサポートが追加されました。TiFlashTiFlash、データスキャン用のFastScanが追加され、エラー処理が改善されました。BRBR、継続的なデータ検証のサポートが追加され、Amazon S3バケットのリージョンの自動識別も可能になりました。TiCDCでは、DDLおよびDMLイベントのフィルタリングがサポートされています。さらに、各種ツールにおける互換性の改善、バグ修正、改善も行われています。
---

# TiDB 6.2.0 リリースノート {#tidb-6-2-0-release-notes}

発売日：2022年8月23日

TiDB バージョン: 6.2.0-DMR

> **注記：**
>
> TiDB 6.2.0-DMR のドキュメントは[アーカイブ済み](https://docs-archive.pingcap.com/tidb/v6.2/)です。PingCAP では、TiDB データベースの[最新のLTSバージョン](https://docs.pingcap.com/tidb/stable)使用することを推奨しています。

v6.2.0-DMR の主な新機能と改善点は次のとおりです。

-   TiDB ダッシュボードは[視覚的な実行計画](https://docs.pingcap.com/tidb/v6.2/dashboard-slow-query#visual-execution-plans)サポートしており、実行プランをより直感的に表示できます。
-   パフォーマンス分析とチューニングをより効率的にするために、TiDB ダッシュボードに[監視ページ](/dashboard/dashboard-monitoring.md)追加します。
-   TiDB 機能の[ビューをロック](/information-schema/information-schema-data-lock-waits.md)では、楽観的トランザクションの待機情報の表示がサポートされており、ロックの競合を迅速に特定できます。
-   TiFlash は[新しいバージョンのstorage形式](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)サポートし、安定性とパフォーマンスを向上させます。
-   [細粒度シャッフル機能](/system-variables.md#tiflash_fine_grained_shuffle_batch_size-new-in-v620) 、複数のスレッドでウィンドウ関数を並列実行することを可能にします。
-   新しい並行 DDL フレームワーク: ブロックされる DDL ステートメントが少なくなり、実行効率が向上します。
-   TiKV は[CPU使用率を自動的に調整する](/tikv-configuration-file.md#background-quota-limiter)サポートしているため、安定した効率的なデータベース操作が保証されます。
-   [ポイントインタイムリカバリ（PITR）](/br/backup-and-restore-overview.md) 、過去の任意の時点から TiDB クラスターのスナップショットを新しいクラスターに復元するために導入されました。
-   TiDB Lightning は、クラスター レベルではなく、物理インポート モードで[テーブルレベルでのスケジュールの一時停止](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#scope-of-pausing-scheduling-during-import)サポートします。
-   BRは[ユーザーと権限データの復元](/br/br-snapshot-guide.md#restore-tables-in-the-mysql-schema)サポートしており、バックアップと復元がよりスムーズになります。
-   TiCDC は、 [特定の種類のDDLイベントをフィルタリングする](/ticdc/ticdc-filter.md)サポートすることで、より多くのデータ複製シナリオを実現します。
-   [`SAVEPOINT`メカニズム](/sql-statements/sql-statement-savepoint.md)がサポートされており、トランザクション内のロールバック ポイントを柔軟に制御できます。
-   TiDB は[1 つの`ALTER TABLE`文だけで複数の列またはインデックスを追加、削除、変更する](/sql-statements/sql-statement-alter-table.md)サポートします。
-   [クラスタ間RawKVレプリケーション](/tikv-configuration-file.md#api-version-new-in-v610)がサポートされるようになりました。

## 新機能 {#new-features}

### SQL {#sql}

-   物理データ圧縮機能はGAです

    TiFlashバックエンドは、特定の条件に基づいて物理データを自動的に圧縮し、不要なデータのバックログを削減して、データstorage構造を最適化します。

    TiFlashテーブルには、データ圧縮が自動的に実行される前に、一定量の不要なデータが存在することがよくあります。この機能を使用すると、適切なタイミングを選択してSQL文を手動で実行することで、 TiFlash内の物理データを即座に圧縮できるため、storage使用量を削減し、クエリパフォーマンスを向上させることができます。この機能はTiDB v6.1では実験的ており、現在TiDB v6.2.0で一般提供（GA）されています。

    [ユーザードキュメント](/sql-statements/sql-statement-alter-table-compact.md#alter-table--compact) [＃4145](https://github.com/pingcap/tiflash/issues/4145) @ [そよ風のような](https://github.com/breezewish)

### 可観測性 {#observability}

-   TiDBダッシュボードをPDから分離する

    TiDBダッシュボードはPDから監視ノードに移動されました。これにより、TiDBダッシュボードがPDに与える影響が軽減され、PDの安定性が向上します。

    @ [ホークソンジー](https://github.com/Hawkson-jee)

-   TiDBダッシュボードに監視ページが追加

    新しい監視ページには、パフォーマンス チューニングに必要な主要な指標が表示され、それに基づいて[データベース時間によるパフォーマンスチューニング](/performance-tuning-methods.md)を参照してパフォーマンスを分析およびチューニングできます。

    具体的には、ユーザー応答時間とデータベース時間をグローバルかつトップダウンの視点から分析し、ユーザー応答時間のボトルネックがデータベースの問題に起因しているかどうかを確認できます。ボトルネックがデータベースにある場合は、データベース時間の概要とSQLレイテンシーの内訳を使用してボトルネックを特定し、パフォーマンスを調整できます。

    [ユーザードキュメント](/dashboard/dashboard-monitoring.md) [＃1381](https://github.com/pingcap/tidb-dashboard/issues/1381) @ [イニシュ9506](https://github.com/YiniXu9506)

-   TiDBダッシュボードは視覚的な実行プランをサポートします

    TiDBダッシュボードは、SQLステートメントとモニタリングページを通じて、視覚的な実行プランと基本的な診断サービスを提供します。この機能は、クエリプランの各ステップを特定するための新たな視点を提供します。これにより、クエリ実行プランのすべてのトレースをより直感的に把握できます。

    この機能は、複雑で大規模なクエリの実行方法を学習したい場合に特に役立ちます。一方、TiDBダッシュボードは、各クエリ実行プランについて、実行の詳細を自動的に分析し、潜在的な問題を特定し、特定のクエリプランの実行時間を短縮するための最適化の提案を提供します。

    [ユーザードキュメント](https://docs.pingcap.com/tidb/v6.2/dashboard-slow-query#visual-execution-plans) [＃1224](https://github.com/pingcap/tidb-dashboard/issues/1224) @ [時間と運命](https://github.com/time-and-fate)

-   ロックビューは、楽観的トランザクションの待機情報の表示をサポートします。

    ロック競合が多すぎると深刻なパフォーマンス問題を引き起こす可能性があり、ロック競合の検出はこうした問題のトラブルシューティングに不可欠です。TiDB v6.2.0より前のバージョンでは、 `INFORMATION_SCHEMA.DATA_LOCK_WAITS`システムビューを使用してロック競合関係を表示できましたが、楽観的トランザクションの待機情報は表示されませんでした。TiDB v6.2.0では`DATA_LOCK_WAITS`システムビューが拡張され、悲観的ロックによってブロックされている楽観的トランザクションがビューに一覧表示されます。この機能は、ユーザーがロック競合を迅速に検出するのに役立ち、アプリケーションを改善するための基盤を提供することで、ロック競合の頻度を減らし、全体的なパフォーマンスを向上させることができます。

    [ユーザードキュメント](/information-schema/information-schema-data-lock-waits.md) [＃34609](https://github.com/pingcap/tidb/issues/34609) @ [ロングファングソン](https://github.com/longfangsong)

### パフォーマンス {#performance}

-   `LEADING`オプティマイザヒントを改善して外部結合順序をサポートする

    v6.1.0では、テーブルの結合順序を変更するためのオプティマイザヒント`LEADING`導入されました。しかし、このヒントは外部結合を含むクエリには適用できませんでした。詳細については、 [`LEADING`文書](/optimizer-hints.md#leadingt1_name--tl_name-)参照してください。v6.2.0では、TiDBはこの制限を解除しました。外部結合を含むクエリでは、このヒントを使用してテーブルの結合順序を指定し、SQL実行パフォーマンスを向上させ、実行プランの突然の変更を回避できるようになりました。

    [ユーザードキュメント](/optimizer-hints.md#leadingt1_name--tl_name-) [＃29932](https://github.com/pingcap/tidb/issues/29932) @ [思い出させる](https://github.com/Reminiscent)

-   `EXISTS`クエリのパフォーマンスを向上させるために新しいオプティマイザ`SEMI_JOIN_REWRITE`を追加します

    状況によっては、 `EXISTS`のクエリでは最適な実行プランが得られず、実行時間が長すぎる可能性があります。v6.2.0 では、このようなシナリオに対応する書き換えルールがオプティマイザーに追加されました。クエリで`SEMI_JOIN_REWRITE`使用すると、オプティマイザーが強制的にクエリを書き換え、クエリパフォーマンスを向上させることができます。

    [ユーザードキュメント](/optimizer-hints.md#semi_join_rewrite) [＃35323](https://github.com/pingcap/tidb/issues/35323) @ [ウィノロス](https://github.com/winoros)

-   分析クエリのパフォーマンスを向上させるために、新しいオプティマイザヒント`MERGE`追加します。

    共通テーブル式（CTE）は、クエリロジックを簡素化する効果的な方法であり、複雑なクエリの作成に広く使用されています。v6.2.0より前のバージョンでは、 TiFlash環境ではCTEを自動的に展開することができず、MPPの実行効率がある程度制限されていました。v6.2.0では、MySQL互換のオプティマイザヒント`MERGE`導入されました。このヒントにより、オプティマイザはCTEインライン展開を許可し、CTEクエリ結果のコンシューマーがTiFlash内でクエリを並行実行できるようになりました。これにより、一部の分析クエリのパフォーマンスが向上します。

    [ユーザードキュメント](/optimizer-hints.md#merge) [＃36122](https://github.com/pingcap/tidb/issues/36122) @ [デイイックルプ](https://github.com/dayicklp)

-   いくつかの分析シナリオにおける集計操作のパフォーマンスを最適化します

    OLAPシナリオにおいて、 TiFlashを使用して列の集計処理を実行する際、集計対象列の分布が不均一なために深刻なデータ偏りが生じ、かつ集計対象列に多くの異なる値が含まれている場合、その列に対する`COUNT(DISTINCT)`のクエリの実行効率は低下します。v6.2.0では、新しい書き換えルールが導入され、1つの列に対する`COUNT(DISTINCT)`のクエリの実行効率が向上しました。

    [ユーザードキュメント](/system-variables.md#tidb_opt_skew_distinct_agg-new-in-v620) [＃36169](https://github.com/pingcap/tidb/issues/36169) @ [修正データベース](https://github.com/fixdb)

-   TiDBは同時DDL操作をサポート

    TiDB v6.2.0では、新しい同時DDLフレームワークが導入されました。これにより、異なるテーブルオブジェクトに対するDDL文の同時実行が可能になり、他のテーブルに対するDDL操作によってDDL操作がブロックされる問題が修正されました。さらに、TiDBは複数のテーブルへのインデックスの追加や列の型変更を行う際にも、同時DDL実行をサポートします。これにより、DDL実行の効率が向上します。

    [＃32031](https://github.com/pingcap/tidb/issues/32031) @ [wjhuang2016](https://github.com/wjhuang2016)

-   オプティマイザーは文字列マッチングの推定を強化します

    文字列マッチングのシナリオにおいて、オプティマイザが行数を正確に推定できない場合、最適な実行プランの生成に影響します。例えば、条件が`like '%xyz'`場合や、正規表現が`regex ()`場合などです。このようなシナリオにおける推定精度を向上させるため、TiDB v6.2.0では推定手法が強化されました。この新しい手法では、統計情報のTopN情報とシステム変数を組み合わせることで精度が向上し、一致選択性を手動で変更できるため、SQLパフォーマンスが向上します。

    [ユーザードキュメント](/system-variables.md#tidb_default_string_match_selectivity-new-in-v620) [＃36209](https://github.com/pingcap/tidb/issues/36209) @ [時間と運命](https://github.com/time-and-fate)

-   TiFlashにプッシュダウンされたウィンドウ関数は複数のスレッドで実行できます

    Fine Grained Shuffle機能を有効にすると、ウィンドウ関数を単一スレッドではなく複数スレッドで実行できるようになります。この機能により、ユーザーの動作を変えることなく、クエリの応答時間を大幅に短縮できます。シャッフルの粒度は、変数の値を調整することで制御できます。

    [ユーザードキュメント](/system-variables.md#tiflash_fine_grained_shuffle_batch_size-new-in-v620) [＃4631](https://github.com/pingcap/tiflash/issues/4631) @ [グオシャオゲ](https://github.com/guo-shaoge)

-   TiFlashは新しいバージョンのstorageフォーマットをサポートしています

    新しいstorageフォーマットは、高同時実行性および高負荷ワークロードのシナリオにおいて、GCによるCPU使用率の上昇を軽減します。これにより、バックグラウンドタスクのIOトラフィックが大幅に削減され、高同時実行性および高負荷ワークロードにおける安定性が向上します。同時に、スペースの増幅とディスクの無駄も大幅に削減されます。

    TiDB v6.2.0では、データはデフォルトで新しいstorage形式で保存されます。TiFlashを以前のバージョンからv6.2.0にアップグレードした場合、以前のバージョンのTiFlashは新しいstorage形式を認識できないため、 TiFlashのインプレースダウングレードは実行できないことに注意してください。

    TiFlash のアップグレードの詳細については、 [TiFlashアップグレードガイド](/tiflash-upgrade-guide.md)参照してください。

    [ユーザードキュメント](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file) [＃3594](https://github.com/pingcap/tiflash/issues/3594) @ [ジェイソン・ファン](https://github.com/JaySon-Huang) @ [リデジュ](https://github.com/lidezhu) @ [佳秋州](https://github.com/jiaqizho)

-   TiFlash は、複数の同時実行シナリオでのデータスキャンパフォーマンスを最適化します (実験的)

    TiFlashは、同じデータの読み取り操作を統合することで、同じデータの重複読み取りを削減し、複数の同時タスク実行時のリソースオーバーヘッドを最適化して、データスキャンのパフォーマンスを向上させます。これにより、同じデータが複数の同時タスクで処理される場合、各タスクで同じデータを個別に読み取る必要がある状況や、同じデータが同時に複数回読み取られる状況を回避します。

    [ユーザードキュメント](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file) [＃5376](https://github.com/pingcap/tiflash/issues/5376) @ [ジンヘリン](https://github.com/JinheLin)

-   TiFlash は、データの一貫性を犠牲にして読み取りおよび書き込み速度を向上させるデータスキャン用の FastScan を追加します (実験的)

    TiDBはv6.2.0でFastScanを導入しました。これにより、整合性チェックを省略して速度を大幅に向上させることができます。FastScanは、オフライン分析タスクなど、データの高精度と整合性が求められないシナリオに適しています。以前は、データの整合性を確保するために、 TiFlashはデータスキャンプロセス中に複数の異なるバージョンから必要なデータを見つけるために、データ整合性チェックを実行する必要がありました。

    以前のバージョンからTiDB v6.2.0にアップグレードする場合、データの一貫性を確保するために、すべてのテーブルでFastScanがデフォルトで有効になっていません。各テーブルごとにFastScanを個別に有効にすることができます。TiDB v6.2.0でテーブルがFastScanに設定されている場合、下位バージョンにダウングレードすると無効になりますが、通常のデータ読み取りには影響しません。この場合、強力な一貫性読み取りと同等の読み取りが行われます。

    [ユーザードキュメント](/tiflash/use-fastscan.md) [＃5252](https://github.com/pingcap/tiflash/issues/5252) @ [ホンユニャン](https://github.com/hongyunyan)

### 安定性 {#stability}

-   TiKV は CPU 使用率の自動調整をサポートします (実験的)

    データベースは通常、内部操作を実行するためのバックグラウンドプロセスを備えています。統計情報を収集することで、パフォーマンスの問題を特定し、より適切な実行プランを生成し、データベースの安定性とパフォーマンスを向上させることができます。しかし、より効率的に情報を収集する方法、そして日常的な使用に影響を与えずにバックグラウンド操作とフォアグラウンド操作のリソースオーバーヘッドのバランスをとる方法は、データベース業界における長年の悩みの種でした。

    TiDB v6.2.0以降、TiKV設定ファイルを用いたバックグラウンドリクエストのCPU使用率設定がサポートされるようになりました。これにより、TiKVへの統計情報の自動収集などのバックグラウンド操作のCPU使用率を制限し、極端なケースにおいてバックグラウンド操作によるユーザー操作のリソース占有を回避できます。これにより、データベースの運用が安定的かつ効率的になります。

    同時に、TiDBはCPU使用率の自動調整もサポートしています。これにより、TiKVはインスタンスのCPU使用率に応じて、バックグラウンドリクエストが占有するCPUリソースを適応的に調整します。この機能はデフォルトで無効になっています。

    [ユーザードキュメント](/tikv-configuration-file.md#background-quota-limiter) [＃12503](https://github.com/tikv/tikv/issues/12503) @ [生まれ変わった人](https://github.com/BornChanger)

### 使いやすさ {#ease-of-use}

-   TiKVはコマンドラインフラグを使用して詳細な構成情報の一覧表示をサポートします

    TiKV設定ファイルはTiKVインスタンスの管理に使用できます。しかし、長期間実行され、複数のユーザーによって管理されているインスタンスの場合、どの設定項目が変更されたか、デフォルト値は何かを把握することが困難です。これは、クラスターのアップグレードやデータの移行時に混乱を招く可能性があります。TiDB v6.2.0以降、tikv-serverは新しいコマンドラインフラグ[`—-config-info`](/command-line-flags-for-tikv-configuration.md#--config-info-format)サポートしています。このフラグは、すべてのTiKV設定項目のデフォルト値と現在の値を一覧表示します。これにより、ユーザーはTiKVプロセスの起動パラメータを迅速に確認でき、ユーザビリティが向上します。

    [ユーザードキュメント](/command-line-flags-for-tikv-configuration.md#--config-info-format) [＃12492](https://github.com/tikv/tikv/issues/12492) @ [栄光](https://github.com/glorv)

### MySQLの互換性 {#mysql-compatibility}

-   TiDBは、 `ALTER TABLE`つのステートメントで複数の列またはインデックスの変更をサポートします。

    v6.2.0より前のTiDBは単一のDDL変更のみをサポートしていたため、異機種データベースの移行時にDDL操作の互換性が失われ、複雑なDDL文をTiDBがサポートする複数のシンプルなDDL文に変更するには余分な手間がかかっていました。さらに、一部のユーザーはORMフレームワークを使用してSQLでアセンブリを作成するため、SQLの互換性が失われていました。v6.2.0以降、TiDBは単一のSQL文で複数のスキーマオブジェクトを変更できるようになりました。これにより、ユーザーにとってSQLの実装が容易になり、ユーザビリティが向上します。

    [ユーザードキュメント](/sql-statements/sql-statement-alter-table.md) [＃14766](https://github.com/pingcap/tidb/issues/14766) @ [接線](https://github.com/tangenta)

-   トランザクションでのセーブポイントの設定をサポート

    トランザクションとは、データベースがACID特性を保証する一連の連続した操作の論理的な集合です。複雑なアプリケーションシナリオでは、1つのトランザクション内で多くの操作を管理する必要があり、場合によってはトランザクション内の一部の操作をロールバックする必要があることもあります。「セーブポイント」は、トランザクションの内部実装のための名前付きメカニズムです。このメカニズムにより、トランザクション内のロールバックポイントを柔軟に制御できるため、より複雑なトランザクションを管理し、多様なアプリケーションをより自由に設計できるようになります。

    [ユーザードキュメント](/sql-statements/sql-statement-savepoint.md) [＃6840](https://github.com/pingcap/tidb/issues/6840) @ [crazycs520](https://github.com/crazycs520)

### データ移行 {#data-migration}

-   BRはユーザーと権限データの復元をサポートします

    BRは通常の復元を実行する際に、ユーザーデータと権限データの復元をサポートします。ユーザーデータと権限データの復元には、追加の復元プランは必要ありません。この機能を有効にするには、 BRを使用してデータを復元する際にパラメータ`--with-sys-table`指定します。

    [ユーザードキュメント](/br/br-snapshot-guide.md#restore-tables-in-the-mysql-schema) [＃35395](https://github.com/pingcap/tidb/issues/35395) @ [D3ハンター](https://github.com/D3Hunter)

-   ログとスナップショットのバックアップと復元に基づくポイントインタイムリカバリ（PITR）をサポート

    PITRは、ログとスナップショットのバックアップとリストアに基づいて実装されています。これにより、クラスターの任意の時点のスナップショットを新しいクラスターにリストアできます。この機能は、以下のニーズを満たします。

    -   災害復旧における RPO を 20 分未満に短縮します。
    -   たとえば、データをエラー イベント前の状態にロールバックするなどして、アプリケーションからの不正な書き込みのケースを処理します。
    -   法令の要件を満たすために履歴データ監査を実行します。

    この機能には使用制限があります。詳細については、ユーザードキュメントを参照してください。

    [ユーザードキュメント](/br/backup-and-restore-overview.md) [＃29501](https://github.com/pingcap/tidb/issues/29501) @ [ジョッカウ](https://github.com/joccau)

-   DM は継続的なデータ検証をサポートします (実験的)

    継続的なデータ検証は、データ移行中に上流のbinlogと下流に書き込まれたデータを継続的に比較するために使用されます。この検証ツールは、データの不整合やレコードの欠落などのデータ例外を特定します。

    この機能は、一般的な完全なデータ検証スキームにおける検証の遅れと過剰なリソース消費の問題を解決します。

    [ユーザードキュメント](/dm/dm-continuous-data-validation.md) [＃4426](https://github.com/pingcap/tiflow/issues/4426) @ [D3ハンター](https://github.com/D3Hunter) @ [ブチュイトデゴウ](https://github.com/buchuitoudegou)

-   Amazon S3 バケットのリージョンを自動的に識別する

    データ移行タスクはAmazon S3バケットのリージョンを自動的に識別します。リージョンパラメータを明示的に渡す必要はありません。

    [＃34275](https://github.com/pingcap/tidb/issues/34275) @ [王楽1321](https://github.com/WangLe1321)

-   TiDB Lightningのディスク クォータ設定のサポート (実験的)

    TiDB Lightning が物理インポートモード（backend=&#39;local&#39;）でデータをインポートする場合、sorted-kv-dir にソースデータを保存するための十分な容量が必要です。ディスク容量が不足すると、インポートタスクが失敗する可能性があります。新しい設定`disk_quota`を使用すると、 TiDB Lightningが使用するディスク容量の合計を制限できます。これにより、sorted-kv-dir に十分なstorage容量がない場合でも、インポートタスクを正常に完了できます。

    [ユーザードキュメント](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#configure-disk-quota-new-in-v620) [＃446](https://github.com/pingcap/tidb-lightning/issues/446) @ [ブチュイトデゴウ](https://github.com/buchuitoudegou)

-   TiDB Lightningは物理インポートモードでの本番クラスタへのデータのインポートをサポートします。

    これまで、 TiDB Lightning （backend=&#39;local&#39;）の物理インポートモードは、ターゲットクラスタに大きな影響を与えていました。例えば、移行中はPDグローバルスケジューリングが一時停止されるため、以前の物理インポートモードは初期データインポートにのみ適しています。

    TiDB Lightningは、既存の物理インポートモードを改良しました。テーブルのスケジュールを一時停止できるようにすることで、インポートの影響がクラスターレベルからテーブルレベルまで軽減されます。つまり、インポートされていないテーブルでも読み書きが可能になります。

    この機能は手動での設定は不要です。TiDBクラスタがv6.1.0以降、 TiDB Lightningがv6.2.0以降の場合、新しい物理インポートモードは自動的に有効になります。

    [ユーザードキュメント](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#scope-of-pausing-scheduling-during-import) [＃35148](https://github.com/pingcap/tidb/issues/35148) @ [眠そうなモグラ](https://github.com/sleepymole)

-   [TiDB Lightningのユーザードキュメント](/tidb-lightning/tidb-lightning-overview.md)リファクタリングし、構造をより合理的かつ明確にしました。また、「バックエンド」の用語も変更し、新規ユーザーの理解を促しました。

    -   「ローカル バックエンド」を「物理インポート モード」に置き換えます。
    -   「tidb backend」を「logical import mode」に置き換えます。

### TiDBデータ共有サブスクリプション {#tidb-data-share-subscription}

-   クラスタ間の RawKV レプリケーションをサポート (実験的)

    新しいコンポーネントTiKV-CDC を使用して、RawKV のデータ変更をサブスクライブし、下流の TiKV クラスターにデータ変更をリアルタイムで複製することをサポートし、クラスター間のレプリケーションが可能になります。

    [ユーザードキュメント](/tikv-configuration-file.md#api-version-new-in-v610) [＃11965](https://github.com/tikv/tikv/issues/11965) @ [ピンギュ](https://github.com/pingyu)

-   DDLおよびDMLイベントのフィルタリングをサポート

    特殊な状況では、増分データ変更ログにフィルタールールを設定する必要がある場合があります。例えば、DROP TABLEなどの高リスクDDLイベントをフィルタリングする場合などです。TiCDC v6.2.0以降では、指定されたタイプのDDLイベントのフィルタリングと、SQL式に基づくDMLイベントのフィルタリングがサポートされます。これにより、TiCDCはより多くのデータレプリケーションシナリオに適用可能になります。

    [ユーザードキュメント](/ticdc/ticdc-filter.md) [＃6160](https://github.com/pingcap/tiflow/issues/6160) @ [アズドンメン](https://github.com/asddongmen)

## 互換性の変更 {#compatibility-changes}

### システム変数 {#system-variables}

| 変数名                                                                                                                     | タイプを変更   | 説明                                                                                                                                                                                                   |
| ----------------------------------------------------------------------------------------------------------------------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [tidb_enable_new_cost_interface](/system-variables.md#tidb_enable_new_cost_interface-new-in-v620)                       | 新しく追加された | この変数は、 [コストモデルの実装をリファクタリング](/cost-model.md#cost-model-version-2)有効にするかどうかを制御します。                                                                                                                     |
| [tidb_コストモデルバージョン](/system-variables.md#tidb_cost_model_version-new-in-v620)                                            | 新しく追加された | TiDBは、物理最適化時にコストモデルを使用してインデックスと演算子を選択します。この変数は、コストモデルのバージョンを選択するために使用されます。TiDB v6.2.0では、コストモデルバージョン2が導入されており、内部テストでは以前のバージョンよりも精度が高くなっています。                                                          |
| tidb_enable_concurrent_ddl                                                                                              | 新しく追加された | この変数は、TiDBが同時DDL文の使用を許可するかどうかを制御します。この変数を変更しないでください。この変数を無効化した場合のリスクは不明であり、クラスタのメタデータが破損する可能性があります。                                                                                                  |
| [tiflash_fine_grained_shuffle_stream_count](/system-variables.md#tiflash_fine_grained_shuffle_stream_count-new-in-v620) | 新しく追加された | この変数は、ウィンドウ関数が実行のためにTiFlashにプッシュダウンされるときの、ウィンドウ関数実行の同時実行レベルを制御します。                                                                                                                                   |
| [tiflash_fine_grained_shuffle_batch_size](/system-variables.md#tiflash_fine_grained_shuffle_batch_size-new-in-v620)     | 新しく追加された | Fine Grained Shuffle を有効にすると、 TiFlashにプッシュダウンされたウィンドウ関数を並列実行できます。この変数は、送信側が送信するデータのバッチサイズを制御します。送信側は、累積行数がこの値を超えるとデータを送信します。                                                                         |
| [tidb_default_string_match_selectivity](/system-variables.md#tidb_default_string_match_selectivity-new-in-v620)         | 新しく追加された | この変数は、行数を推定する際に、フィルター条件における`like` 、 `rlike` 、 `regexp`関数のデフォルトの選択度を設定するために使用されます。また、これらの関数の推定を支援するためにTopNを有効にするかどうかも制御します。                                                                           |
| [tidb_enable_analyze_snapshot](/system-variables.md#tidb_enable_analyze_snapshot-new-in-v620)                           | 新しく追加された | この変数は`ANALYZE`実行するときに履歴データを読み取るか最新データを読み取るかを制御します。                                                                                                                                                   |
| [tidb_generate_binary_plan](/system-variables.md#tidb_generate_binary_plan-new-in-v620)                                 | 新しく追加された | この変数は、スロー ログとステートメント サマリーにバイナリ エンコードされた実行プランを生成するかどうかを制御します。                                                                                                                                         |
| [tidb_opt_skew_distinct_agg](/system-variables.md#tidb_opt_skew_distinct_agg-new-in-v620)                               | 新しく追加された | この変数は、オプティマイザが`DISTINCT`を含む集計関数を2 レベルの集計関数に書き換えるかどうか (たとえば、 `SELECT b, COUNT(DISTINCT a) FROM t GROUP BY b`を`SELECT b, COUNT(a) FROM (SELECT b, a FROM t GROUP BY b, a) t GROUP BY b`に書き換える) を設定します。 |
| [tidb_enable_noop_variables](/system-variables.md#tidb_enable_noop_variables-new-in-v620)                               | 新しく追加された | この変数は、 `SHOW [GLOBAL] VARIABLES`の結果に`noop`変数を表示するかどうかを制御します。                                                                                                                                         |
| [tidb_min_paging_size](/system-variables.md#tidb_min_paging_size-new-in-v620)                                           | 新しく追加された | この変数は、コプロセッサ ページング要求プロセス中の最大行数を設定するために使用されます。                                                                                                                                                        |
| [tidb_txn_commit_batch_size](/system-variables.md#tidb_txn_commit_batch_size-new-in-v620)                               | 新しく追加された | この変数は、TiDB が TiKV に送信するトランザクション コミット要求のバッチ サイズを制御するために使用されます。                                                                                                                                        |
| tidb_enable_change_multi_schema                                                                                         | 削除済み     | この変数は、v6.2.0 以降ではデフォルトで`ALTER TABLE`ステートメントで複数の列またはインデックスを変更できるため、削除されます。                                                                                                                            |
| [tidb_enable_outer_join_reorder](/system-variables.md#tidb_enable_outer_join_reorder-new-in-v610)                       | 修正済み     | この変数は、TiDBの結合したテーブルの再配置アルゴリズムが外部結合をサポートするかどうかを制御します。v6.1.0では、デフォルト値は`ON`で、結合順序変更アルゴリズムによる外部結合のサポートがデフォルトで有効になります。v6.2.0以降では、デフォルト値は`OFF`で、サポートがデフォルトで無効になります。                                        |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーション                                                                                                              | タイプを変更   | 説明                                                                                                 |
| -------------- | ----------------------------------------------------------------------------------------------------------------------- | -------- | -------------------------------------------------------------------------------------------------- |
| TiDB           | フィードバック確率                                                                                                               | 削除済み     | この構成はもはや効果的ではないため、推奨されません。                                                                         |
| TiDB           | クエリフィードバック制限                                                                                                            | 削除済み     | この構成はもはや効果的ではないため、推奨されません。                                                                         |
| TiKV           | [サーバー.simplify-metrics](/tikv-configuration-file.md#simplify-metrics-new-in-v620)                                       | 新しく追加された | この構成では、返される監視メトリックを簡素化するかどうかを指定します。                                                                |
| TiKV           | [クォータ.バックグラウンドCPU時間](/tikv-configuration-file.md#background-cpu-time-new-in-v620)                                       | 新しく追加された | この構成は、読み取りおよび書き込み要求を処理するために TiKV バックグラウンドで使用される CPU リソースのソフト制限を指定します。                              |
| TiKV           | [クォータ.バックグラウンド書き込み帯域幅](/tikv-configuration-file.md#background-write-bandwidth-new-in-v620)                              | 新しく追加された | この構成は、バックグラウンド トランザクションがデータを書き込む帯域幅のソフト制限を指定します (現在は有効ではありません)。                                    |
| TiKV           | [クォータ.バックグラウンド読み取り帯域幅](/tikv-configuration-file.md#background-read-bandwidth-new-in-v620)                               | 新しく追加された | この構成は、バックグラウンド トランザクションとコプロセッサーがデータを読み取る帯域幅のソフト制限を指定します (現在は有効ではありません)。                            |
| TiKV           | [クォータの自動調整を有効にする](/tikv-configuration-file.md#enable-auto-tune-new-in-v620)                                             | 新しく追加された | この設定は、クォータの自動調整を有効にするかどうかを指定します。この設定項目を有効にすると、TiKVはTiKVインスタンスの負荷に基づいて、バックグラウンドリクエストのクォータを動的に調整します。 |
| TiKV           | rocksdb.パイプラインコミットを有効にする                                                                                                | 削除済み     | この構成はもう有効ではありません。                                                                                  |
| TiKV           | GCマージ書き換え                                                                                                               | 削除済み     | この構成はもう有効ではありません。                                                                                  |
| TiKV           | [ログバックアップを有効にする](/tikv-configuration-file.md#enable-new-in-v620)                                                        | 新しく追加された | この構成は、TiKV でログ バックアップを有効にするかどうかを制御します。                                                             |
| TiKV           | [ログバックアップのファイルサイズ制限](/tikv-configuration-file.md#file-size-limit-new-in-v620)                                           | 新しく追加された | この設定は、ログバックアップデータのサイズ制限を指定します。この制限に達すると、データは自動的に外部storageにフラッシュされます。                               |
| TiKV           | [ログバックアップ.初期スキャン保留中のメモリクォータ](/tikv-configuration-file.md#initial-scan-pending-memory-quota-new-in-v620)                 | 新しく追加された | この構成は、増分スキャン データの保存に使用されるキャッシュのクォータを指定します。                                                         |
| TiKV           | [ログバックアップの最大フラッシュ間隔](/tikv-configuration-file.md#max-flush-interval-new-in-v620)                                        | 新しく追加された | この構成は、ログ バックアップでバックアップ データを外部storageに書き込む最大間隔を指定します。                                               |
| TiKV           | [ログバックアップ初期スキャンレート制限](/tikv-configuration-file.md#initial-scan-rate-limit-new-in-v620)                                  | 新しく追加された | この構成は、ログ バックアップの増分データ スキャンにおけるスループットのレート制限を指定します。                                                  |
| TiKV           | [ログバックアップ.スレッド数](/tikv-configuration-file.md#num-threads-new-in-v620)                                                   | 新しく追加された | この構成は、ログ バックアップで使用されるスレッドの数を指定します。                                                                 |
| TiKV           | [ログバックアップの一時パス](/tikv-configuration-file.md#temp-path-new-in-v620)                                                      | 新しく追加された | この構成は、ログ ファイルが外部storageにフラッシュされる前に書き込まれる一時パスを指定します。                                                |
| TiKV           | [rocksdb.defaultcf.format-version](/tikv-configuration-file.md#format-version-new-in-v620)                              | 新しく追加された | SST ファイルの形式バージョン。                                                                                  |
| TiKV           | [rocksdb.writecf.format-version](/tikv-configuration-file.md#format-version-new-in-v620)                                | 新しく追加された | SST ファイルの形式バージョン。                                                                                  |
| TiKV           | [rocksdb.lockcf.フォーマットバージョン](/tikv-configuration-file.md#format-version-new-in-v620)                                    | 新しく追加された | SST ファイルの形式バージョン。                                                                                  |
| PD             | レプリケーションモード.dr-auto-sync.wait-async-timeout                                                                             | 削除済み     | この設定は有効にならないため削除されます。                                                                              |
| PD             | レプリケーションモード.dr-auto-sync.wait-sync-timeout                                                                              | 削除済み     | この設定は有効にならないため削除されます。                                                                              |
| TiFlash        | [`storage.format_version`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                            | 修正済み     | デフォルト値`format_version`は、v6.2.0 以降のバージョンのデフォルト形式である`4`に変更され、書き込み増幅とバックグラウンド タスクのリソース消費が削減されます。      |
| TiFlash        | [プロファイル.default.dt_enable_read_thread](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                | 新しく追加された | この設定は、storageエンジンからの読み取りリクエストを処理するためにスレッドプールを使用するかどうかを制御します。デフォルト値は`false`です。                      |
| TiFlash        | [プロファイル.default.dt_page_gc_threshold](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                 | 新しく追加された | この構成は、PageStorage データ ファイル内の有効なデータの最小比率を指定します。                                                     |
| TiCDC          | [--overwrite-checkpoint-ts](/ticdc/ticdc-manage-changefeed.md#resume-a-replication-task)                                | 新しく追加された | この設定は`cdc cli changefeed resume`サブコマンドに追加されます。                                                     |
| TiCDC          | [--確認なし](/ticdc/ticdc-manage-changefeed.md#resume-a-replication-task)                                                   | 新しく追加された | この設定は`cdc cli changefeed resume`サブコマンドに追加されます。                                                     |
| DM             | [モード](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)                                    | 新しく追加された | この設定は検証パラメータです。オプションの値は`full` 、 `fast` 、 `none`です。デフォルト値は`none`で、この場合、データは検証されません。                 |
| DM             | [労働者数](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)                                   | 新しく追加された | この設定はバリデータパラメータであり、バックグラウンドで実行されるバリデーションワーカーの数を指定します。デフォルト値は`4`です。                                 |
| DM             | [行エラー遅延](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)                                 | 新しく追加された | この設定はバリデータパラメータです。指定された時間内に行が検証されない場合、エラー行としてマークされます。デフォルト値は30m（30分）です。                            |
| TiDB Lightning | [tikv-importer.store-write-bwlimit](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)                | 新しく追加された | この設定は、TiDB Lightningが各TiKVストアにデータを書き込む際の書き込み帯域幅を決定します。デフォルト値は`0`で、帯域幅が制限されないことを示します。               |
| TiDB Lightning | [tikv-importer.ディスククォータ](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#configure-disk-quota-new-in-v620) | 新しく追加された | この構成により、 TiDB Lightningが使用するstorageスペースが制限されます。                                                    |

### その他 {#others}

-   TiFlash `format_version` `4`から`3`にダウングレードできません。詳細は[TiFlashアップグレードガイド](/tiflash-upgrade-guide.md)ご覧ください。
-   v6.2.0以降のバージョンでは、デフォルト値の`false`を`dt_enable_logical_split`のままにし、 `true`に変更しないことを強くお勧めします。詳細については、既知の問題[＃5576](https://github.com/pingcap/tiflash/issues/5576)参照してください。
-   バックアップクラスターにTiFlashレプリカがある場合、PITR実行後、リストアクラスターにはTiFlashレプリカのデータが含まれません。TiFlashレプリカからデータをリストアするには、 TiFlashレプリカを手動で設定する必要があります。1 DDL文`exchange partition`実行すると、PITRが失敗する可能性があります。上流データベースがTiDB Lightningの物理インポートモードを使用してデータをインポートしている場合、ログバックアップではデータをバックアップできません。データのインポート後は、フルバックアップを実行することをお勧めします。PITRのその他の互換性の問題については、 [PITRの制限](/br/backup-and-restore-overview.md#before-you-use)参照してください。
-   TiDB v6.2.0 以降では、データの復元時にパラメータ`--with-sys-table=true`指定することにより、 `mysql`スキーマでテーブルを復元できます。
-   複数の列またはインデックスを追加、削除、または変更する`ALTER TABLE`ステートメントを実行すると、TiDBは、同じDDLステートメント内の変更に関係なく、ステートメント実行前後のテーブルを比較することでテーブルの一貫性をチェックします。DDLの実行順序は、一部のシナリオではMySQLと完全に互換性がありません。
-   TiDBコンポーネントが v6.2.0 以降の場合、TiKVコンポーネントはv6.2.0 より前のバージョンであってはなりません。
-   TiKV は[動的構成](/dynamic-config.md#modify-tikv-configuration-dynamically)サポートする構成項目`split.region-cpu-overload-threshold-ratio`追加します。
-   スロークエリログ、 `information_schema.statements_summary` `information_schema.slow_query` 、バイナリ形式でエンコードされた`binary_plan` 、つまり実行プランをエクスポートできます。
-   `SHOW TABLE ... REGIONS`ステートメントに`SCHEDULING_CONSTRAINTS`と`SCHEDULING_STATE` 2 つの列が追加されました。これらはそれぞれ、SQL の配置におけるリージョンスケジュール制約と現在のスケジュール状態を示します。
-   TiDB v6.2.0 以降では、 [TiKV-CDC](https://github.com/tikv/migration/tree/main/cdc)経由で RawKV のデータ変更をキャプチャできます。
-   `ROLLBACK TO SAVEPOINT`使用してトランザクションを指定されたセーブポイントまでロールバックすると、MySQL は指定されたセーブポイント以降に保持されているロックのみを解放します。一方、TiDB の悲観的トランザクションでは、TiDB は指定されたセーブポイント以降に保持されているロックをすぐには解放しません。代わりに、TiDB はトランザクションがコミットまたはロールバックされた時点ですべてのロックを解放します。
-   TiDB v6.2.0 以降、 `SELECT tidb_version()`ステートメントはストア タイプ (tikv または unistore) も返します。
-   TiDB には隠しシステム変数がなくなりました。
-   TiDB v6.2.0 では、次の 2 つの新しいシステム テーブルが導入されています。
    -   `INFORMATION_SCHEMA.VARIABLES_INFO` : TiDB システム変数に関する情報を表示するために使用されます。
    -   `PERFORMANCE_SCHEMA.SESSION_VARIABLES` : TiDB セッション レベルのシステム変数に関する情報を表示するために使用されます。

## 削除された機能 {#removed-feature}

TiDB v6.2.0 以降、 BRを使用した RawKV のバックアップと復元は非推奨になりました。

## 改善点 {#improvements}

-   TiDB

    -   `SHOW COUNT(*) WARNINGS`と`SHOW COUNT(*) ERRORS`文を[＃25068](https://github.com/pingcap/tidb/issues/25068) @ [いいね](https://github.com/likzn)でサポートする

    -   いくつかのシステム変数[＃35048](https://github.com/pingcap/tidb/issues/35048) @ [モルゴ](https://github.com/morgo)検証チェックを追加します

    -   いくつかの型変換のエラーメッセージを最適化[＃32744](https://github.com/pingcap/tidb/issues/32744) @ [ファンレンフー](https://github.com/fanrenhoo)

    -   `KILL`コマンドは DDL 操作[＃24144](https://github.com/pingcap/tidb/issues/24144) @ [モルゴ](https://github.com/morgo)をサポートするようになりました

    -   `SHOW TABLES/DATABASES LIKE …`の出力をMySQL互換にします。出力の列名には`LIKE`値[＃35116](https://github.com/pingcap/tidb/issues/35116) @ [いいね](https://github.com/likzn)が含まれます。

    -   JSON関連関数のパフォーマンスを向上[＃35859](https://github.com/pingcap/tidb/issues/35859) @ [wjhuang2016](https://github.com/wjhuang2016)

    -   SHA-2 [＃35998](https://github.com/pingcap/tidb/issues/35998) @ [ウイルスディフェンダー](https://github.com/virusdefender)を使用したパスワードログインの検証速度を向上

    -   いくつかのログ出力を簡素化する[＃36011](https://github.com/pingcap/tidb/issues/36011) @ [ドヴェーデン](https://github.com/dveeden)

    -   コプロセッサー通信プロトコルを最適化します。これにより、TiDBプロセスによるデータ読み取り時のメモリ消費量が大幅に削減され、 DumplingによるテーブルスキャンとデータエクスポートのシナリオにおけるOOM問題がさらに軽減されます。システム変数`tidb_enable_paging` 、この通信プロトコル（SESSIONまたはGLOBAL）を有効にするかどうかを制御するために使用されます。このプロトコルはデフォルトで無効になっています。有効にするには、変数値を`true` [＃35633](https://github.com/pingcap/tidb/issues/35633) @ [天菜あま](https://github.com/tiancaiamao) @ [wshwsh12](https://github.com/wshwsh12)に設定します。

    -   一部[wshwsh12](https://github.com/wshwsh12)演算子（HashJoin、HashAgg、Update、Delete）のメモリ追跡の精度を最適化（ [＃35634](https://github.com/pingcap/tidb/issues/35634) @ [＃35635](https://github.com/pingcap/tidb/issues/35635) [＃35631](https://github.com/pingcap/tidb/issues/35631) （ [＃34096](https://github.com/pingcap/tidb/issues/34096) @ [エキシウム](https://github.com/ekexium) ）

    -   システムテーブル`INFORMATION_SCHEMA.DATA_LOCK_WAIT` 、楽観的トランザクション[＃34609](https://github.com/pingcap/tidb/issues/34609) @ [ロングファンソン](https://github.com/longfangsong)のロック情報の記録をサポートします。

    -   トランザクション[＃34456](https://github.com/pingcap/tidb/issues/34456) @ [ロングファングソン](https://github.com/longfangsong)監視メトリックを追加します

-   TiKV

    -   HTTPボディサイズを[＃12355](https://github.com/tikv/tikv/issues/12355) @ [栄光](https://github.com/glorv)に削減するために、gzipを使用してメトリック応答を圧縮することをサポートします。
    -   Grafanaダッシュボード[＃12007](https://github.com/tikv/tikv/issues/12007) @ [ケビン・シャンリウ](https://github.com/kevin-xianliu)のTiKVパネルの読みやすさを改善
    -   Apply演算子[＃12898](https://github.com/tikv/tikv/issues/12898) @ [イーサフロー](https://github.com/ethercflow)のコミットパイプラインのパフォーマンスを最適化する
    -   RocksDBで同時に実行されるサブコンパクション操作の数を動的に変更する機能をサポート ( `rocksdb.max-sub-compactions` ) [＃13145](https://github.com/tikv/tikv/issues/13145) @ [イーサフロー](https://github.com/ethercflow)

-   PD

    -   リージョンのCPU使用率の統計ディメンションをサポートし、Load Base Split [＃12063](https://github.com/tikv/tikv/issues/12063) @ [Jmポテト](https://github.com/JmPotato)の使用シナリオを強化します。

-   TiFlash

    -   TiFlash MPPエンジンのエラー処理を改良し、安定性を向上[＃5095](https://github.com/pingcap/tiflash/issues/5095) @ [ウィンドトーカー](https://github.com/windtalker) @ [イービン87](https://github.com/yibin87)

    -   UTF8_BIN と UTF8MB4_BIN 照合の比較と並べ替えを最適化[＃5294](https://github.com/pingcap/tiflash/issues/5294) @ [ソロツグ](https://github.com/solotzg)

-   ツール

    -   バックアップと復元 (BR)

        -   大規模クラスタバックアップ[＃30087](https://github.com/pingcap/tidb/issues/30087) @ [モクイシュル28](https://github.com/MoCuishle28)での S3 レート制限によるバックアップ失敗を修正するために、バックアップデータディレクトリ構造を調整します。

    -   TiCDC

        -   マルチリージョンシナリオにおける実行時コンテキスト切り替えによるパフォーマンスオーバーヘッドを削減[＃5610](https://github.com/pingcap/tiflow/issues/5610) @ [ヒック](https://github.com/hicqu)

        -   REDOログのパフォーマンスを最適化し、メタデータとデータの不整合の問題を修正します（ [＃6011](https://github.com/pingcap/tiflow/issues/6011) @ [チャールズ・チュン96](https://github.com/CharlesCheung96) ）（ [＃5924](https://github.com/pingcap/tiflow/issues/5924) @ [ジャオシンユ](https://github.com/zhaoxinyu) ）（ [＃6277](https://github.com/pingcap/tiflow/issues/6277) @ [ヒック](https://github.com/hicqu) ）

    -   TiDB Lightning

        -   EOF、読み取りインデックスの準備ができていない、コプロセッサーのタイムアウト[＃36674](https://github.com/pingcap/tidb/issues/36674) 、 [＃36566](https://github.com/pingcap/tidb/issues/36566) @ [D3ハンター](https://github.com/D3Hunter)などの再試行可能なエラーを追加します。

    -   TiUP

        -   TiUPを使用して新しいクラスターを展開すると、node-exporter はバージョン[1.3.1](https://github.com/prometheus/node_exporter/releases/tag/v1.3.1)を使用し、blackbox-exporter はバージョン[0.21.1](https://github.com/prometheus/blackbox_exporter/releases/tag/v0.21.1)使用します。これにより、さまざまなシステムや環境での展開が確実に成功します。

## バグ修正 {#bug-fixes}

-   TiDB

    -   クエリ条件でパーティションキーが使用され、照合がクエリパーティションテーブル[＃32749](https://github.com/pingcap/tidb/issues/32749) @ [ミョンス](https://github.com/mjonss)の照合と異なる場合にパーティションが誤ってプルーニングされる問題を修正しました。
    -   ホスト[＃33061](https://github.com/pingcap/tidb/issues/33061) @ [モルゴ](https://github.com/morgo)に大文字が含まれている場合、 `SET ROLE`付与されたロールと一致しない問題を修正しました
    -   `auto_increment`の列を[＃34891](https://github.com/pingcap/tidb/issues/34891) @ [定義2014](https://github.com/Defined2014)にドロップできない問題を修正
    -   `SHOW CONFIG`で削除された構成項目がいくつか表示される問題を修正[＃34867](https://github.com/pingcap/tidb/issues/34867) @ [モルゴ](https://github.com/morgo)
    -   `SHOW DATABASES LIKE …`が大文字と小文字を区別する問題を修正[＃34766](https://github.com/pingcap/tidb/issues/34766) @ [エリヤ1](https://github.com/e1ijah1)
    -   `SHOW TABLE STATUS LIKE ...`が大文字と小文字を区別する問題を修正[＃7518](https://github.com/pingcap/tidb/issues/7518) @ [いいね](https://github.com/likzn)
    -   `max-index-length`が非厳密モードでエラーを報告する問題を修正[＃34931](https://github.com/pingcap/tidb/issues/34931) @ [エリヤ1](https://github.com/e1ijah1)
    -   `ALTER COLUMN ... DROP DEFAULT` [＃35018](https://github.com/pingcap/tidb/issues/35018) @ [定義2014](https://github.com/Defined2014)で動作しない問題を修正
    -   テーブルを作成するときに、列のデフォルト値とタイプが一致せず、自動的に修正されない問題を修正[＃34881](https://github.com/pingcap/tidb/issues/34881) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)
    -   `DROP USER` [＃35059](https://github.com/pingcap/tidb/issues/35059) @ [lcwangchao](https://github.com/lcwangchao)を実行した後に`mysql.columns_priv`テーブルのデータが同期的に削除されない問題を修正しました
    -   一部のシステムのスキーマ内でのテーブル作成を禁止することで、DDL ジャムの問題を修正しました[＃35205](https://github.com/pingcap/tidb/issues/35205) @ [接線](https://github.com/tangenta)
    -   パーティションテーブルをクエリすると、場合によっては「インデックス範囲外」および「未使用のインデックス」エラーが報告される問題を修正[＃35181](https://github.com/pingcap/tidb/issues/35181) @ [ミョンス](https://github.com/mjonss)
    -   `INTERVAL expr unit + expr`エラー[＃30253](https://github.com/pingcap/tidb/issues/30253) @ [ミョンス](https://github.com/mjonss)を報告する可能性がある問題を修正しました
    -   トランザクション[＃35644](https://github.com/pingcap/tidb/issues/35644) @ [djshow832](https://github.com/djshow832)で作成された一時テーブルが見つからないバグを修正
    -   照合順序を`ENUM`列[＃31637](https://github.com/pingcap/tidb/issues/31637) @ [wjhuang2016](https://github.com/wjhuang2016)に設定すると発生するpanic問題を修正
    -   1つのPDノードがダウンした場合、他のPDノード[＃35708](https://github.com/pingcap/tidb/issues/35708) @ [接線](https://github.com/tangenta)を再試行しないため、 `information_schema.TIKV_REGION_STATUS`のクエリが失敗する問題を修正しました。
    -   `SHOW CREATE TABLE …`セットまたは`SET character_set_results = GBK` [＃31338](https://github.com/pingcap/tidb/issues/31338) @ [接線](https://github.com/tangenta)の後の`ENUM`列を正しく表示できない問題を修正しました
    -   システム変数`tidb_log_file_max_days`と`tidb_config` [＃35190](https://github.com/pingcap/tidb/issues/35190) @ [モルゴ](https://github.com/morgo)の誤ったスコープを修正しました
    -   `SHOW CREATE TABLE`の出力がMySQLの`ENUM`または`SET`列目[＃36317](https://github.com/pingcap/tidb/issues/36317) @ [定義2014](https://github.com/Defined2014)と互換性がない問題を修正しました
    -   テーブル作成時に`LONG BYTE`列目の挙動がMySQL [＃36239](https://github.com/pingcap/tidb/issues/36239) @ [定義2014](https://github.com/Defined2014)と互換性がない問題を修正
    -   `auto_increment = x`一時テーブル[＃36224](https://github.com/pingcap/tidb/issues/36224) @ [djshow832](https://github.com/djshow832)に反映されない問題を修正
    -   列を同時に変更する際の誤ったデフォルト値を修正[＃35846](https://github.com/pingcap/tidb/issues/35846) @ [wjhuang2016](https://github.com/wjhuang2016)
    -   可用性を向上させるために、不健全な TiKV ノードへのリクエストの送信を避ける[＃34906](https://github.com/pingcap/tidb/issues/34906) @ [スティクナーフ](https://github.com/sticnarf)
    -   LOAD DATA文[＃35198](https://github.com/pingcap/tidb/issues/35198) @ [スペードA-タン](https://github.com/SpadeA-Tang)で列リストが機能しない問題を修正
    -   一部のシナリオで、悲観的ロックが非一意のセカンダリインデックス[＃36235](https://github.com/pingcap/tidb/issues/36235) @ [エキシウム](https://github.com/ekexium)に誤って追加される問題を修正しました。

-   TiKV

    -   悲観的トランザクション[＃11612](https://github.com/tikv/tikv/issues/11612)で`WriteConflict`エラーを報告しないようにする[スティクナーフ](https://github.com/sticnarf)
    -   非同期コミットが有効な場合の悲観的トランザクションにおけるコミットレコードの重複の可能性を修正[＃12615](https://github.com/tikv/tikv/issues/12615) @ [スティクナーフ](https://github.com/sticnarf)
    -   `storage.api-version` `1`から`2` [＃12600](https://github.com/tikv/tikv/issues/12600) @ [ピンギュ](https://github.com/pingyu)に変更するときにTiKVがパニックになる問題を修正しました
    -   TiKVとPD [＃12518](https://github.com/tikv/tikv/issues/12518) @ [5kbps](https://github.com/5kbpers)間のリージョンサイズ設定が一致しない問題を修正
    -   TiKVがPDクライアント[＃12506](https://github.com/tikv/tikv/issues/12506) @ [コナー1996](https://github.com/Connor1996) [＃12827](https://github.com/tikv/tikv/issues/12827)再接続し続ける問題を修正
    -   空の文字列[＃12673](https://github.com/tikv/tikv/issues/12673) @ [wshwsh12](https://github.com/wshwsh12)型変換を実行するときに TiKV がパニックになる問題を修正しました
    -   `DATETIME`値に小数点が含まれる場合と`Z` [＃12739](https://github.com/tikv/tikv/issues/12739) @ [ゲンリキ](https://github.com/gengliqi)場合に発生する時間解析エラーの問題を修正しました
    -   Apply 演算子によって TiKV RocksDB に書き込まれるパフォーマンスコンテキストが粗粒度[＃11044](https://github.com/tikv/tikv/issues/11044) @ [LykxSassinator](https://github.com/LykxSassinator)になる問題を修正しました
    -   [バックアップ](/tikv-configuration-file.md#backup) / [輸入](/tikv-configuration-file.md#import) / [CDC](/tikv-configuration-file.md#cdc)の設定が無効な場合にTiKVの起動に失敗する問題を修正[＃12771](https://github.com/tikv/tikv/issues/12771) @ [3ポイントシュート](https://github.com/3pointer)
    -   ピアが同時に分割され、破棄されたときに発生する可能性のあるpanic問題を修正[＃12825](https://github.com/tikv/tikv/issues/12825) @ [ビジージェイ](https://github.com/BusyJay)
    -   リージョンマージプロセス[＃12663](https://github.com/tikv/tikv/issues/12663) @ [ビジージェイ](https://github.com/BusyJay)でソースピアがスナップショットによってログをキャッチアップするときに発生する可能性のあるpanic問題を修正しました。
    -   `max_sample_size` `0` [＃11192](https://github.com/tikv/tikv/issues/11192) @ [LykxSassinator](https://github.com/LykxSassinator)に設定されている場合に統計を分析することによって発生するpanicの問題を修正しました
    -   Raft Engineが有効になっているときに暗号化キーがクリーンアップされない問題を修正[＃12890](https://github.com/tikv/tikv/issues/12890) @ [タボキ](https://github.com/tabokie)
    -   `get_valid_int_prefix`関数がTiDBと互換性がない問題を修正しました。例えば、 `FLOAT`型は誤って`INT` [＃13045](https://github.com/tikv/tikv/issues/13045) @ [グオシャオゲ](https://github.com/guo-shaoge)に変換されていました。
    -   新しいリージョンのコミットログ期間が長すぎるため、QPS が[＃13077](https://github.com/tikv/tikv/issues/13077) @ [コナー1996](https://github.com/Connor1996)低下する問題を修正しました。
    -   リージョンハートビートが中断された後にPDがTiKVに再接続しない問題を修正[＃12934](https://github.com/tikv/tikv/issues/12934) @ [バッファフライ](https://github.com/bufferflies)

-   ツール

    -   バックアップと復元 (BR)

        -   レート制限されたバックアップタスク[＃31722](https://github.com/pingcap/tidb/issues/31722) @ [モクイシュル28](https://github.com/MoCuishle28)を終了した後、 BR がレート制限をリセットしない問題を修正しました

## 寄稿者 {#contributors}

TiDB コミュニティからの以下の貢献者に感謝いたします。

-   [エリヤ1](https://github.com/e1ijah1)
-   [プラジュワル・ボルカル](https://github.com/PrajwalBorkar)
-   [いいね](https://github.com/likzn)
-   [rahulk789](https://github.com/rahulk789)
-   [ウイルスディフェンダー](https://github.com/virusdefender)
-   [ジョイセ06](https://github.com/joycse06)
-   [モルゴ](https://github.com/morgo)
-   [ixuh12](https://github.com/ixuh12)
-   [ブラックティア23](https://github.com/blacktear23)
-   [ジョンハックス7](https://github.com/johnhaxx7)
-   [ゴギム1](https://github.com/GoGim1)
-   [レンバオシュオ](https://github.com/renbaoshuo)
-   [ジャオリ](https://github.com/Zheaoli)
-   [ファンレンフー](https://github.com/fanrenhoo)
-   [ヌジュウェルキン](https://github.com/njuwelkin)
-   [ワイリービーバー](https://github.com/wirybeaver)
-   [ヘイコン](https://github.com/hey-kong)
-   [運命](https://github.com/fatelei)
-   [イーストフィッシャー](https://github.com/eastfisher) : 初回投稿者
-   [ジュニージー](https://github.com/Juneezee) : 初回投稿者
