---
title: TiDB 6.2.0 Release Notes
summary: TiDB 6.2.0-DMR では、ビジュアル実行プラン、監視ページ、ロック ビューなどの新機能が導入されています。また、同時 DDL 操作もサポートされ、集計操作のパフォーマンスが向上しています。TiKV では、CPU 使用率の自動調整と詳細な構成情報のリストがサポートされるようになりました。TiFlashTiFlash、データ スキャン用の FastScan が追加され、エラー処理が改善されています。BRBR、継続的なデータ検証がサポートされ、Amazon S3 バケットのリージョンが自動的に識別されます。TiCDC では、DDL および DML イベントのフィルタリングがサポートされています。また、さまざまなツールで互換性の変更、バグ修正、改善が行われています。
---

# TiDB 6.2.0 リリースノート {#tidb-6-2-0-release-notes}

発売日: 2022年8月23日

TiDB バージョン: 6.2.0-DMR

> **注記：**
>
> TiDB 6.2.0-DMR のドキュメントは[アーカイブ済み](https://docs-archive.pingcap.com/tidb/v6.2/)です。PingCAP では、TiDB データベースの[最新のLTSバージョン](https://docs.pingcap.com/tidb/stable)使用することを推奨しています。

v6.2.0-DMR の主な新機能と改善点は次のとおりです。

-   TiDB ダッシュボードは[視覚的な実行計画](https://docs.pingcap.com/tidb/v6.2/dashboard-slow-query#visual-execution-plans)サポートしており、実行プランをより直感的に表示できます。
-   パフォーマンス分析とチューニングをより効率的にするために、TiDB ダッシュボードに[監視ページ](/dashboard/dashboard-monitoring.md)追加します。
-   TiDB 機能の[ビューをロック](/information-schema/information-schema-data-lock-waits.md)では、楽観的トランザクションの待機情報の表示がサポートされており、ロック競合の迅速な特定が容易になります。
-   TiFlash は[新しいバージョンのstorage形式](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)サポートし、安定性とパフォーマンスを向上させます。
-   [きめ細かなシャッフル機能](/system-variables.md#tiflash_fine_grained_shuffle_batch_size-new-in-v620)は、複数のスレッドでウィンドウ関数を並列実行することを可能にします。
-   新しい同時実行 DDL フレームワーク: ブロックされる DDL ステートメントが少なくなり、実行効率が向上します。
-   TiKV は[CPU使用率を自動的に調整する](/tikv-configuration-file.md#background-quota-limiter)サポートしているため、安定した効率的なデータベース操作が保証されます。
-   [ポイントインタイムリカバリ (PITR)](/br/backup-and-restore-overview.md)は、過去の任意の時点から TiDB クラスターのスナップショットを新しいクラスターに復元するために導入されました。
-   TiDB Lightning は、クラスター レベルではなく、物理インポート モードで[テーブルレベルでスケジュールを一時停止する](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#scope-of-pausing-scheduling-during-import)サポートします。
-   BR は[ユーザーと権限のデータの復元](/br/br-snapshot-guide.md#restore-tables-in-the-mysql-schema)サポートしており、バックアップと復元がよりスムーズになります。
-   TiCDC は、 [特定の種類のDDLイベントをフィルタリングする](/ticdc/ticdc-filter.md)サポートすることで、より多くのデータ複製シナリオを実現します。
-   [`SAVEPOINT`メカニズム](/sql-statements/sql-statement-savepoint.md)がサポートされており、トランザクション内のロールバック ポイントを柔軟に制御できます。
-   TiDB は[1 つの`ALTER TABLE`ステートメントだけで複数の列またはインデックスを追加、削除、および変更する](/sql-statements/sql-statement-alter-table.md)サポートします。
-   [クラスタ間RawKVレプリケーション](/tikv-configuration-file.md#api-version-new-in-v610)サポートされるようになりました。

## 新機能 {#new-features}

### 構文 {#sql}

-   物理データ圧縮機能はGAです

    TiFlashバックエンドは、特定の条件に基づいて物理データを自動的に圧縮し、無駄なデータのバックログを削減し、データstorage構造を最適化します。

    多くの場合、データ圧縮が自動的にトリガーされる前に、 TiFlashテーブルに一定量の無駄なデータがあります。この機能を使用すると、適切なタイミングを選択して SQL ステートメントを手動で実行し、 TiFlash内の物理データを即座に圧縮できるため、storage領域の使用量が削減され、クエリのパフォーマンスが向上します。この機能は TiDB v6.1 では実験的であり、現在 TiDB v6.2.0 で一般提供 (GA) されています。

    [ユーザードキュメント](/sql-statements/sql-statement-alter-table-compact.md#alter-table--compact) [＃4145](https://github.com/pingcap/tiflash/issues/4145) @ [そよ風のような](https://github.com/breezewish)

### 可観測性 {#observability}

-   TiDBダッシュボードをPDから分離する

    TiDB ダッシュボードは PD から監視ノードに移動されました。これにより、TiDB ダッシュボードの PD への影響が軽減され、PD がより安定します。

    @ [ホークソンジー](https://github.com/Hawkson-jee)

-   TiDBダッシュボードに監視ページが追加されました

    新しい「監視」ページには、パフォーマンス チューニングに必要な主要な指標が表示され、それに基づいて[データベース時間によるパフォーマンスチューニング](/performance-tuning-methods.md)を参照してパフォーマンスを分析およびチューニングできます。

    具体的には、ユーザー応答時間とデータベース時間をグローバルかつトップダウンの観点から分析し、ユーザー応答時間のボトルネックの原因がデータベースの問題であるかどうかを確認できます。ボトルネックの原因がデータベースにある場合は、データベース時間の概要と SQLレイテンシーの内訳を使用してボトルネックを特定し、パフォーマンスを調整できます。

    [ユーザードキュメント](/dashboard/dashboard-monitoring.md) [＃1381](https://github.com/pingcap/tidb-dashboard/issues/1381) @ [宜尼Xu9506](https://github.com/YiniXu9506)

-   TiDBダッシュボードは視覚的な実行計画をサポートします

    TiDB ダッシュボードは、SQL ステートメントと監視ページを通じて、視覚的な実行プランと基本的な診断サービスを提供します。この機能は、クエリ プランの各ステップを識別するための新しい視点を提供します。そのため、クエリ実行プランのすべてのトレースをより直感的に把握できます。

    この機能は、複雑で大規模なクエリの実行方法を学習する場合に特に便利です。一方、TiDB ダッシュボードは、各クエリ実行プランの実行の詳細を自動的に分析し、潜在的な問題を特定し、特定のクエリ プランの実行に必要な時間を短縮するための最適化の提案を提供します。

    [ユーザードキュメント](https://docs.pingcap.com/tidb/v6.2/dashboard-slow-query#visual-execution-plans) [＃1224](https://github.com/pingcap/tidb-dashboard/issues/1224) @ [時間と運命](https://github.com/time-and-fate)

-   ロックビューは、楽観的トランザクションの待機情報の表示をサポートします。

    ロック競合が多すぎると、重大なパフォーマンスの問題が発生する可能性があり、ロック競合を検出することは、このような問題のトラブルシューティングに必要な方法です。v6.2.0 より前の TiDB では、 `INFORMATION_SCHEMA.DATA_LOCK_WAITS`システム ビューを使用してロック競合関係を表示できましたが、楽観的トランザクションの待機情報は表示されませんでした。TiDB v6.2.0 では`DATA_LOCK_WAITS`ビューが拡張され、悲観的ロックによってブロックされた楽観的トランザクションがビューにリストされます。この機能により、ユーザーはロック競合を迅速に検出でき、アプリケーションを改善するための基盤が提供されるため、ロック競合の頻度が減り、全体的なパフォーマンスが向上します。

    [ユーザードキュメント](/information-schema/information-schema-data-lock-waits.md) [＃34609](https://github.com/pingcap/tidb/issues/34609) @ [ロングファングソン](https://github.com/longfangsong)

### パフォーマンス {#performance}

-   `LEADING`オプティマイザヒントを改善して外部結合順序をサポートする

    v6.1.0 では、テーブルの結合順序を変更するためにオプティマイザ ヒント`LEADING`が導入されました。ただし、このヒントは外部結合を含むクエリには適用できませんでした。詳細については、 [`LEADING`文書](/optimizer-hints.md#leadingt1_name--tl_name-)参照してください。v6.2.0 では、TiDB はこの制限を解除しました。外部結合を含むクエリでは、このヒントを使用してテーブルの結合順序を指定し、SQL 実行パフォーマンスを向上させ、実行プランの突然の変更を回避できるようになりました。

    [ユーザードキュメント](/optimizer-hints.md#leadingt1_name--tl_name-) [＃29932](https://github.com/pingcap/tidb/issues/29932) @ [思い出させる](https://github.com/Reminiscent)

-   `EXISTS`のクエリのパフォーマンスを向上させるために新しいオプティマイザ`SEMI_JOIN_REWRITE`を追加します

    シナリオによっては、 `EXISTS`のクエリでは最適な実行プランを作成できず、実行に時間がかかりすぎる可能性があります。v6.2.0 では、オプティマイザーがこのようなシナリオの書き換えルールを追加し、クエリで`SEMI_JOIN_REWRITE`使用してオプティマイザーに強制的にクエリを書き換えさせ、クエリのパフォーマンスを向上させることができます。

    [ユーザードキュメント](/optimizer-hints.md#semi_join_rewrite) [＃35323](https://github.com/pingcap/tidb/issues/35323) @ [ウィノロス](https://github.com/winoros)

-   分析クエリのパフォーマンスを向上させるために、新しいオプティマイザヒント`MERGE`を追加します。

    共通テーブル式 (CTE) は、クエリ ロジックを簡素化する効果的な方法です。複雑なクエリの作成に広く使用されています。v6.2.0 より前のバージョンでは、 TiFlash環境では CTE を自動的に展開することができず、MPP の実行効率がある程度制限されていました。v6.2.0 では、MySQL 互換のオプティマイザー ヒント`MERGE`が導入されました。このヒントにより、オプティマイザーは CTE インラインを展開できるようになり、CTE クエリ結果のコンシューマーはTiFlashでクエリを同時に実行できるようになり、一部の分析クエリのパフォーマンスが向上しました。

    [ユーザードキュメント](/optimizer-hints.md#merge) [＃36122](https://github.com/pingcap/tidb/issues/36122) @ [デイックルプ](https://github.com/dayicklp)

-   いくつかの分析シナリオにおける集計操作のパフォーマンスを最適化します

    OLAP シナリオでTiFlash を使用して列の集計操作を実行する場合、集計列の不均一な分布により深刻なデータ スキューが存在し、集計列に多くの異なる値がある場合、列に対する`COUNT(DISTINCT)`のクエリの実行効率は低くなります。v6.2.0 では、新しい書き換えルールが導入され、1 つの列に対する`COUNT(DISTINCT)`のクエリのパフォーマンスが向上しました。

    [ユーザードキュメント](/system-variables.md#tidb_opt_skew_distinct_agg-new-in-v620) [＃36169](https://github.com/pingcap/tidb/issues/36169) @ [修正DB](https://github.com/fixdb)

-   TiDBは同時DDL操作をサポート

    TiDB v6.2.0 では、新しい同時実行 DDL フレームワークが導入され、異なるテーブル オブジェクトで DDL ステートメントを同時に実行できるようになり、他のテーブルでの DDL 操作によって DDL 操作がブロックされる問題が修正されました。さらに、TiDB は、複数のテーブルにインデックスを追加したり、列の型を変更したりするときに、同時実行 DDL 実行をサポートします。これにより、DDL 実行の効率が向上します。

    [＃32031](https://github.com/pingcap/tidb/issues/32031) @ [翻訳:](https://github.com/wjhuang2016)

-   オプティマイザーは文字列マッチングの推定を強化します

    文字列マッチングのシナリオでは、オプティマイザが行数を正確に推定できない場合、最適な実行プランの生成に影響します。たとえば、条件が`like '%xyz'`場合や、正規表現`regex ()`使用している場合などです。このようなシナリオでの推定精度を向上させるために、TiDB v6.2.0 では推定方法が強化されています。新しい方法では、統計の TopN 情報とシステム変数を組み合わせて精度を向上させ、一致選択性を手動で変更できるようにすることで、SQL パフォーマンスが向上します。

    [ユーザードキュメント](/system-variables.md#tidb_default_string_match_selectivity-new-in-v620) [＃36209](https://github.com/pingcap/tidb/issues/36209) @ [時間と運命](https://github.com/time-and-fate)

-   TiFlashにプッシュダウンされたウィンドウ関数は複数のスレッドで実行できます

    細粒度シャッフル機能を有効にすると、ウィンドウ関数を単一のスレッドではなく複数のスレッドで実行できるようになります。この機能により、ユーザーの動作を変えずにクエリの応答時間が大幅に短縮されます。変数の値を調整することで、シャッフルの粒度を制御できます。

    [ユーザードキュメント](/system-variables.md#tiflash_fine_grained_shuffle_batch_size-new-in-v620) [＃4631](https://github.com/pingcap/tiflash/issues/4631) @ [グオシャオゲ](https://github.com/guo-shaoge)

-   TiFlashは新しいバージョンのstorageフォーマットをサポートしています

    新しいstorage形式により、同時実行性が高く、ワークロードが重いシナリオで GC によって発生する CPU 使用率の上昇が軽減されます。これにより、バックグラウンド タスクの IO トラフィックが大幅に削減され、同時実行性が高く、ワークロードが重い状況でも安定性が向上します。同時に、スペースの増大とディスクの無駄も大幅に削減されます。

    TiDB v6.2.0 では、データはデフォルトで新しいstorage形式で保存されます。TiFlashを以前のバージョンから v6.2.0 にアップグレードする場合、以前のバージョンのTiFlashでは新しいstorage形式を認識できないため、 TiFlashでインプレース ダウングレードを実行できないことに注意してください。

    TiFlash のアップグレードの詳細については、 [TiFlashアップグレード ガイド](/tiflash-upgrade-guide.md)参照してください。

    [ユーザードキュメント](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file) [＃3594](https://github.com/pingcap/tiflash/issues/3594) @ [ジェイソン・ファン](https://github.com/JaySon-Huang) @ [リデズ](https://github.com/lidezhu) @ [ジアキゾ](https://github.com/jiaqizho)

-   TiFlash は、複数の同時実行シナリオでのデータスキャン パフォーマンスを最適化します (実験的)

    TiFlash は、同じデータの読み取り操作をマージすることで、同じデータの重複読み取りを減らし、複数の同時タスクの場合にリソース オーバーヘッドを最適化して、データ スキャンのパフォーマンスを向上させます。これにより、同じデータが複数の同時タスクに関係している場合、各タスクで同じデータを個別に読み取る必要がある状況や、同じデータが同時に複数回読み取られる状況を回避できます。

    [ユーザードキュメント](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file) [＃5376](https://github.com/pingcap/tiflash/issues/5376) @ [ジンヘリン](https://github.com/JinheLin)

-   TiFlash は、データの一貫性を犠牲にして読み取りと書き込みの速度を向上させるために、データスキャン用の FastScan を追加しました (実験的)

    TiDB は、v6.2.0 で FastScan を導入しました。これは、一貫性チェックのスキップをサポートし、速度を大幅に向上させます。FastScan は、オフライン分析タスクなど、データの高精度と一貫性を必要としないシナリオに適しています。以前は、データの一貫性を確保するために、 TiFlash はデータ スキャン プロセス中にデータ一貫性チェックを実行し、複数の異なるバージョンから必要なデータを見つける必要がありました。

    以前のバージョンから TiDB v6.2.0 にアップグレードすると、データの一貫性を確保するために、すべてのテーブルで FastScan がデフォルトで有効になりません。各テーブルに対して個別に FastScan を有効にすることができます。TiDB v6.2.0 でテーブルが FastScan に設定されている場合、下位バージョンにダウングレードすると無効になりますが、通常のデータ読み取りには影響しません。この場合、強力な一貫性読み取りに相当します。

    [ユーザードキュメント](/tiflash/use-fastscan.md) [＃5252](https://github.com/pingcap/tiflash/issues/5252) @ [ホンユンヤン](https://github.com/hongyunyan)

### 安定性 {#stability}

-   TiKV は CPU 使用率の自動調整をサポートします (実験的)

    データベースには通常、内部操作を実行するためのバックグラウンド プロセスがあります。統計情報を収集することで、パフォーマンスの問題を特定し、より適切な実行プランを生成し、データベースの安定性とパフォーマンスを向上させることができます。ただし、より効率的に情報を収集する方法、日常的な使用に影響を与えずにバックグラウンド操作とフォアグラウンド操作のリソース オーバーヘッドのバランスをとる方法は、常にデータベース業界の悩みの種となっています。

    v6.2.0 以降、TiDB は TiKV 構成ファイルを使用してバックグラウンド リクエストの CPU 使用率を設定することをサポートし、これにより、TiKV での統計の自動収集などのバックグラウンド操作の CPU 使用率を制限し、極端なケースでバックグラウンド操作によるユーザー操作のリソースのプリエンプションを回避します。これにより、データベースの操作が安定して効率的になります。

    同時に、TiDB は CPU 使用率の自動調整もサポートしています。その後、TiKV はインスタンスの CPU 使用率に応じて、バックグラウンド リクエストによって占有される CPU リソースを適応的に調整します。この機能はデフォルトでは無効になっています。

    [ユーザードキュメント](/tikv-configuration-file.md#background-quota-limiter) [＃12503](https://github.com/tikv/tikv/issues/12503) @ [ボーンチェンジャー](https://github.com/BornChanger)

### 使いやすさ {#ease-of-use}

-   TiKVはコマンドラインフラグを使用して詳細な構成情報の一覧表示をサポートします

    TiKV 構成ファイルを使用して、TiKV インスタンスを管理できます。ただし、長期間実行され、異なるユーザーによって管理されているインスタンスの場合、どの構成項目が変更されたか、デフォルト値が何であるかを把握することは困難です。これにより、クラスターのアップグレードやデータの移行時に混乱が生じる可能性があります。TiDB v6.2.0 以降、tikv-server は、すべての TiKV 構成項目のデフォルト値と現在の値を一覧表示する新しいコマンドライン フラグ[`—-config-info`](/command-line-flags-for-tikv-configuration.md#--config-info-format)をサポートし、ユーザーが TiKV プロセスの起動パラメータをすばやく確認できるようにし、使いやすさを向上させます。

    [ユーザードキュメント](/command-line-flags-for-tikv-configuration.md#--config-info-format) [＃12492](https://github.com/tikv/tikv/issues/12492) @ [栄光](https://github.com/glorv)

### MySQL 互換性 {#mysql-compatibility}

-   TiDBは、 `ALTER TABLE`つのステートメントで複数の列またはインデックスの変更をサポートします。

    v6.2.0 より前の TiDB では、単一の DDL 変更のみがサポートされていたため、異種データベースの移行時に互換性のない DDL 操作が発生し、複雑な DDL ステートメントを TiDB がサポートする複数の単純な DDL ステートメントに変更するには余分な労力がかかります。さらに、一部のユーザーは ORM フレームワークに依存して SQL でアセンブリを作成するため、SQL の非互換性が発生します。v6.2.0 以降、TiDB は単一の SQL ステートメントで複数のスキーマ オブジェクトの変更をサポートしており、ユーザーが SQL を実装するのに便利で、使いやすさが向上しています。

    [ユーザードキュメント](/sql-statements/sql-statement-alter-table.md) [＃14766](https://github.com/pingcap/tidb/issues/14766) @ [タンジェンタ](https://github.com/tangenta)

-   トランザクションでのセーブポイントの設定をサポート

    トランザクションは、データベースがACIDプロパティを保証する一連の連続した操作の論理的な集合です。複雑なアプリケーション シナリオでは、トランザクションで多くの操作を管理する必要があり、場合によってはトランザクションで一部の操作をロールバックする必要があることがあります。「セーブポイント」は、トランザクションの内部実装のための名前を付けられるメカニズムです。このメカニズムを使用すると、トランザクション内のロールバック ポイントを柔軟に制御できるため、より複雑なトランザクションを管理し、さまざまなアプリケーションをより自由に設計できます。

    [ユーザードキュメント](/sql-statements/sql-statement-savepoint.md) [＃6840](https://github.com/pingcap/tidb/issues/6840) @ [クレイジーcs520](https://github.com/crazycs520)

### データ移行 {#data-migration}

-   BRはユーザーと権限データの復元をサポートします

    BR は、通常の復元を実行するときに、ユーザーと権限のデータの復元をサポートします。ユーザーと権限のデータを復元するために追加の復元プランは必要ありません。この機能を有効にするには、 BR を使用してデータを復元するときに`--with-sys-table`パラメータを指定します。

    [ユーザードキュメント](/br/br-snapshot-guide.md#restore-tables-in-the-mysql-schema) [＃35395](https://github.com/pingcap/tidb/issues/35395) @ [D3ハンター](https://github.com/D3Hunter)

-   ログとスナップショットのバックアップと復元に基づくポイントインタイムリカバリ（PITR）をサポート

    PITR は、ログとスナップショットのバックアップと復元に基づいて実装されています。これにより、履歴の任意の時点でのクラスターのスナップショットを新しいクラスターに復元できます。この機能は、次のニーズを満たします。

    -   災害復旧における RPO を 20 分未満に短縮します。
    -   たとえば、データをエラー イベント前の状態にロールバックするなどして、アプリケーションからの不正な書き込みのケースを処理します。
    -   法令の要件を満たすために履歴データ監査を実行します。

    この機能には使用制限があります。詳細については、ユーザードキュメントを参照してください。

    [ユーザードキュメント](/br/backup-and-restore-overview.md) [＃29501](https://github.com/pingcap/tidb/issues/29501) @ [ジョッカウ](https://github.com/joccau)

-   DM は継続的なデータ検証をサポートします (実験的)

    継続的なデータ検証は、データ移行中に上流のbinlogと下流に書き込まれたデータを継続的に比較するために使用されます。検証ツールは、不整合なデータや欠落したレコードなどのデータ例外を識別します。

    この機能は、一般的な完全なデータ検証スキームにおける検証の遅れと過剰なリソース消費の問題を解決します。

    [ユーザードキュメント](/dm/dm-continuous-data-validation.md) [＃4426](https://github.com/pingcap/tiflow/issues/4426) @ [D3ハンター](https://github.com/D3Hunter) @ [ブチュイトウデゴウ](https://github.com/buchuitoudegou)

-   Amazon S3バケットのリージョンを自動的に識別する

    データ移行タスクは、Amazon S3 バケットのリージョンを自動的に識別できます。リージョンパラメータを明示的に渡す必要はありません。

    [＃34275](https://github.com/pingcap/tidb/issues/34275) @ [ワンレ1321](https://github.com/WangLe1321)

-   TiDB Lightningのディスク クォータ設定のサポート (実験的)

    TiDB Lightning が物理インポート モード (backend=&#39;local&#39;) でデータをインポートする場合、sorted-kv-dir にはソース データを格納するのに十分なスペースが必要です。ディスク スペースが不足すると、インポート タスクが失敗する可能性があります。新しい`disk_quota`構成を使用して、 TiDB Lightningが使用するディスク スペースの合計量を制限できるようになりました。これにより、sorted-kv-dir に十分なstorageスペースがない場合でも、インポート タスクを正常に完了できます。

    [ユーザードキュメント](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#configure-disk-quota-new-in-v620) [＃446](https://github.com/pingcap/tidb-lightning/issues/446) @ [ブチュイトウデゴウ](https://github.com/buchuitoudegou)

-   TiDB Lightningは物理インポートモードでの本番クラスタへのデータのインポートをサポートします

    以前は、 TiDB Lightning (backend=&#39;local&#39;) の物理インポート モードは、ターゲット クラスターに大きな影響を与えていました。たとえば、移行中は PD グローバル スケジューリングが一時停止されます。そのため、以前の物理インポート モードは、初期データ インポートにのみ適しています。

    TiDB Lightning は、既存の物理インポート モードを改良します。テーブルのスケジュールを一時停止できるようにすることで、インポートの影響がクラスター レベルからテーブル レベルまで軽減されます。つまり、インポートされていないテーブルを読み書きできます。

    この機能は手動で構成する必要はありません。TiDB クラスターが v6.1.0 以降で、 TiDB Lightningが v6.2.0 以降の場合、新しい物理インポート モードが自動的に有効になります。

    [ユーザードキュメント](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#scope-of-pausing-scheduling-during-import) [＃35148](https://github.com/pingcap/tidb/issues/35148) @ [眠いモグラ](https://github.com/sleepymole)

-   [TiDB Lightningのユーザードキュメント](/tidb-lightning/tidb-lightning-overview.md)リファクタリングして、構造をより合理的かつ明確にします。また、「バックエンド」の用語も変更され、新しいユーザーの理解の障壁が低くなります。

    -   「ローカル バックエンド」を「物理インポート モード」に置き換えます。
    -   「tidb backend」を「logical import mode」に置き換えます。

### TiDBデータ共有サブスクリプション {#tidb-data-share-subscription}

-   クラスタ間の RawKV レプリケーションをサポート (実験的)

    新しいコンポーネントTiKV-CDC を使用して、RawKV のデータ変更をサブスクライブし、データ変更を下流の TiKV クラスターにリアルタイムで複製することをサポートし、クラスター間のレプリケーションを可能にします。

    [ユーザードキュメント](/tikv-configuration-file.md#api-version-new-in-v610) [＃11965](https://github.com/tikv/tikv/issues/11965) @ [ピンギュ](https://github.com/pingyu)

-   DDLおよびDMLイベントのフィルタリングをサポート

    特別な場合には、増分データ変更ログのフィルター ルールを設定する必要があります。たとえば、DROP TABLE などの高リスクの DDL イベントをフィルターします。v6.2.0 以降、TiCDC は指定されたタイプの DDL イベントのフィルターと、SQL 式に基づく DML イベントのフィルターをサポートします。これにより、TiCDC はより多くのデータ レプリケーション シナリオに適用できます。

    [ユーザードキュメント](/ticdc/ticdc-filter.md) [＃6160](https://github.com/pingcap/tiflow/issues/6160) @ [アズドンメン](https://github.com/asddongmen)

## 互換性の変更 {#compatibility-changes}

### システム変数 {#system-variables}

| 変数名                                                                                                                     | タイプを変更   | 説明                                                                                                                                                                                                  |
| ----------------------------------------------------------------------------------------------------------------------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [tidb_enable_new_cost_interface](/system-variables.md#tidb_enable_new_cost_interface-new-in-v620)                       | 新しく追加された | この変数は、 [コストモデルの実装をリファクタリング](/cost-model.md#cost-model-version-2)を有効にするかどうかを制御します。                                                                                                                   |
| [tidb_コスト_モデル_バージョン](/system-variables.md#tidb_cost_model_version-new-in-v620)                                          | 新しく追加された | TiDB は、物理的な最適化中にコスト モデルを使用してインデックスと演算子を選択します。この変数は、コスト モデル バージョンを選択するために使用されます。TiDB v6.2.0 では、内部テストで以前のバージョンよりも精度の高いコスト モデル バージョン 2 が導入されています。                                                      |
| tidb_enable_concurrent_ddl                                                                                              | 新しく追加された | この変数は、TiDB が同時 DDL ステートメントを使用できるようにするかどうかを制御します。この変数を変更しないでください。この変数を無効にするリスクは不明であり、クラスターのメタデータが破損する可能性があります。                                                                                       |
| [tiflash_fine_grained_shuffle_stream_count](/system-variables.md#tiflash_fine_grained_shuffle_stream_count-new-in-v620) | 新しく追加された | この変数は、ウィンドウ関数が実行のためにTiFlashにプッシュダウンされるときに、ウィンドウ関数実行の同時実行レベルを制御します。                                                                                                                                  |
| [tiflash_fine_grained_shuffle_batch_size](/system-variables.md#tiflash_fine_grained_shuffle_batch_size-new-in-v620)     | 新しく追加された | Fine Grained Shuffle を有効にすると、 TiFlashにプッシュダウンされたウィンドウ関数を並列で実行できます。この変数は、送信者が送信するデータのバッチ サイズを制御します。送信者は、累積行数がこの値を超えるとデータを送信します。                                                                      |
| [tidb_default_string_match_selectivity](/system-variables.md#tidb_default_string_match_selectivity-new-in-v620)         | 新しく追加された | この変数は、行数を推定するときに、フィルター条件で`like` 、 `rlike` 、および`regexp`関数の関数の選択性を設定するために使用されます。この変数は、これらの関数の推定を支援するために TopN を有効にするかどうかも制御します。                                                                        |
| [tidb_enable_analyze_snapshot](/system-variables.md#tidb_enable_analyze_snapshot-new-in-v620)                           | 新しく追加された | この変数は、 `ANALYZE`実行するときに履歴データを読み取るか、最新のデータを読み取るかを制御します。                                                                                                                                              |
| [tidb_generate_binary_plan](/system-variables.md#tidb_generate_binary_plan-new-in-v620)                                 | 新しく追加された | この変数は、スロー ログとステートメントの概要にバイナリ エンコードされた実行プランを生成するかどうかを制御します。                                                                                                                                          |
| [tidb_opt_skew_distinct_agg](/system-variables.md#tidb_opt_skew_distinct_agg-new-in-v620)                               | 新しく追加された | この変数は、オプティマイザが`DISTINCT`含む集計関数を2 レベルの集計関数に書き換えるかどうか (たとえば、 `SELECT b, COUNT(DISTINCT a) FROM t GROUP BY b`を`SELECT b, COUNT(a) FROM (SELECT b, a FROM t GROUP BY b, a) t GROUP BY b`に書き換える) を設定します。 |
| [tidb_enable_noop_variables](/system-variables.md#tidb_enable_noop_variables-new-in-v620)                               | 新しく追加された | この変数は、 `SHOW [GLOBAL] VARIABLES`の結果に`noop`変数を表示するかどうかを制御します。                                                                                                                                        |
| [tidb_min_paging_size](/system-variables.md#tidb_min_paging_size-new-in-v620)                                           | 新しく追加された | この変数は、コプロセッサ ページング要求プロセス中の最大行数を設定するために使用されます。                                                                                                                                                       |
| [tidb_txn_commit_batch_size](/system-variables.md#tidb_txn_commit_batch_size-new-in-v620)                               | 新しく追加された | この変数は、TiDB が TiKV に送信するトランザクション コミット要求のバッチ サイズを制御するために使用されます。                                                                                                                                       |
| tidb_enable_change_multi_schema                                                                                         | 削除されました  | この変数は、v6.2.0 以降ではデフォルトで`ALTER TABLE`ステートメントで複数の列またはインデックスを変更できるため削除されます。                                                                                                                            |
| [tidb_enable_outer_join_reorder](/system-variables.md#tidb_enable_outer_join_reorder-new-in-v610)                       | 修正済み     | この変数は、TiDB の結合したテーブルの再配置アルゴリズムが外部結合をサポートするかどうかを制御します。v6.1.0 では、デフォルト値は`ON`で、結合順序の外部結合のサポートがデフォルトで有効になっていることを意味します。v6.2.0 以降では、デフォルト値は`OFF`で、サポートがデフォルトで無効になっていることを意味します。                            |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーション                                                                                                              | タイプを変更   | 説明                                                                                                 |
| -------------- | ----------------------------------------------------------------------------------------------------------------------- | -------- | -------------------------------------------------------------------------------------------------- |
| ティビ            | フィードバック確率                                                                                                               | 削除されました  | この構成はもはや有効ではなく、推奨されません。                                                                            |
| ティビ            | クエリフィードバック制限                                                                                                            | 削除されました  | この構成はもはや有効ではなく、推奨されません。                                                                            |
| ティクヴ           | [サーバー.simplify-metrics](/tikv-configuration-file.md#simplify-metrics-new-in-v620)                                       | 新しく追加された | この構成は、返される監視メトリックを簡素化するかどうかを指定します。                                                                 |
| ティクヴ           | [クォータ.バックグラウンドCPU時間](/tikv-configuration-file.md#background-cpu-time-new-in-v620)                                       | 新しく追加された | この構成は、読み取りおよび書き込み要求を処理するために TiKV バックグラウンドで使用される CPU リソースのソフト制限を指定します。                              |
| ティクヴ           | [クォータ.バックグラウンド書き込み帯域幅](/tikv-configuration-file.md#background-write-bandwidth-new-in-v620)                              | 新しく追加された | この構成は、バックグラウンド トランザクションがデータを書き込む帯域幅のソフト制限を指定します (現在は有効ではありません)。                                    |
| ティクヴ           | [クォータ.バックグラウンド読み取り帯域幅](/tikv-configuration-file.md#background-read-bandwidth-new-in-v620)                               | 新しく追加された | この構成は、バックグラウンド トランザクションとコプロセッサーがデータを読み取る帯域幅のソフト制限を指定します (現在は有効ではありません)。                            |
| ティクヴ           | [クォータの自動調整を有効にする](/tikv-configuration-file.md#enable-auto-tune-new-in-v620)                                             | 新しく追加された | この構成では、クォータの自動調整を有効にするかどうかを指定します。この構成項目を有効にすると、TiKV は TiKV インスタンスの負荷に基づいてバックグラウンド要求のクォータを動的に調整します。 |
| ティクヴ           | rocksdb.パイプラインコミットを有効にする                                                                                                | 削除されました  | この構成はもう有効ではありません。                                                                                  |
| ティクヴ           | gc-マージ-書き換え                                                                                                             | 削除されました  | この構成はもう有効ではありません。                                                                                  |
| ティクヴ           | [ログバックアップを有効にする](/tikv-configuration-file.md#enable-new-in-v620)                                                        | 新しく追加された | この構成は、TiKV でログ バックアップを有効にするかどうかを制御します。                                                             |
| ティクヴ           | [ログバックアップのファイルサイズ制限](/tikv-configuration-file.md#file-size-limit-new-in-v620)                                           | 新しく追加された | この構成は、ログ バックアップ データのサイズ制限を指定します。この制限に達すると、データは自動的に外部storageにフラッシュされます。                             |
| ティクヴ           | [ログバックアップ.初期スキャン保留中のメモリ割り当て](/tikv-configuration-file.md#initial-scan-pending-memory-quota-new-in-v620)                 | 新しく追加された | この構成は、増分スキャン データを格納するために使用されるキャッシュの割り当てを指定します。                                                     |
| ティクヴ           | [ログバックアップの最大フラッシュ間隔](/tikv-configuration-file.md#max-flush-interval-new-in-v620)                                        | 新しく追加された | この構成は、ログ バックアップでバックアップ データを外部storageに書き込む最大間隔を指定します。                                               |
| ティクヴ           | [ログバックアップ初期スキャンレート制限](/tikv-configuration-file.md#initial-scan-rate-limit-new-in-v620)                                  | 新しく追加された | この構成は、ログ バックアップの増分データ スキャンにおけるスループットのレート制限を指定します。                                                  |
| ティクヴ           | [ログバックアップ.スレッド数](/tikv-configuration-file.md#num-threads-new-in-v620)                                                   | 新しく追加された | この構成は、ログ バックアップで使用されるスレッドの数を指定します。                                                                 |
| ティクヴ           | [ログバックアップ.temp-path](/tikv-configuration-file.md#temp-path-new-in-v620)                                                 | 新しく追加された | この構成は、ログ ファイルが外部storageにフラッシュされる前に書き込まれる一時パスを指定します。                                                |
| ティクヴ           | [rocksdb.defaultcf.フォーマットバージョン](/tikv-configuration-file.md#format-version-new-in-v620)                                 | 新しく追加された | SST ファイルの形式バージョン。                                                                                  |
| ティクヴ           | [rocksdb.writecf.フォーマットバージョン](/tikv-configuration-file.md#format-version-new-in-v620)                                   | 新しく追加された | SST ファイルの形式バージョン。                                                                                  |
| ティクヴ           | [rocksdb.lockcf.フォーマットバージョン](/tikv-configuration-file.md#format-version-new-in-v620)                                    | 新しく追加された | SST ファイルの形式バージョン。                                                                                  |
| PD             | レプリケーション モード.dr-auto-sync.wait-async-timeout                                                                            | 削除されました  | この設定は有効にならず、削除されます。                                                                                |
| PD             | レプリケーション モード.dr-auto-sync.wait-sync-timeout                                                                             | 削除されました  | この設定は有効にならず、削除されます。                                                                                |
| TiFlash        | [`storage.format_version`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                            | 修正済み     | デフォルト値`format_version`は、v6.2.0 以降のバージョンのデフォルト形式である`4`に変更され、書き込み増幅とバックグラウンド タスクのリソース消費が削減されます。      |
| TiFlash        | [プロファイル.default.dt_enable_read_thread](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                | 新しく追加された | この構成は、storageエンジンからの読み取り要求を処理するためにスレッド プールを使用するかどうかを制御します。デフォルト値は`false`です。                        |
| TiFlash        | [プロファイル.default.dt_page_gc_threshold](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                 | 新しく追加された | この構成は、PageStorage データ ファイル内の有効なデータの最小比率を指定します。                                                     |
| ティCDC          | [--overwrite-checkpoint-ts](/ticdc/ticdc-manage-changefeed.md#resume-a-replication-task)                                | 新しく追加された | この設定は`cdc cli changefeed resume`サブコマンドに追加されます。                                                     |
| ティCDC          | [--確認しない](/ticdc/ticdc-manage-changefeed.md#resume-a-replication-task)                                                  | 新しく追加された | この設定は`cdc cli changefeed resume`サブコマンドに追加されます。                                                     |
| DM             | [モード](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)                                    | 新しく追加された | この設定は検証パラメータです。オプションの値は`full` 、 `fast` 、 `none`です。デフォルト値は`none`で、データは検証されません。                      |
| DM             | [労働者数](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)                                   | 新しく追加された | この設定はバリデータパラメータであり、バックグラウンドでの検証ワーカーの数を指定します。デフォルト値は`4`です。                                          |
| DM             | [行エラー遅延](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)                                 | 新しく追加された | この設定は検証パラメータです。指定された時間内に行が検証されない場合、エラー行としてマークされます。デフォルト値は 30m で、これは 30 分を意味します。                    |
| TiDB Lightning | [tikv-importer.store-write-bwlimit](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)                | 新しく追加された | この設定は、 TiDB Lightning が各 TiKV ストアにデータを書き込むときの書き込み帯域幅を決定します。デフォルト値は`0`で、帯域幅が制限されていないことを示します。        |
| TiDB Lightning | [tikv-importer.ディスククォータ](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#configure-disk-quota-new-in-v620) | 新しく追加された | この構成により、 TiDB Lightningが使用するstorageスペースが制限されます。                                                    |

### その他 {#others}

-   TiFlash `format_version` `4`から`3`にダウングレードできません。詳細については[TiFlashアップグレード ガイド](/tiflash-upgrade-guide.md)参照してください。
-   v6.2.0 以降のバージョンでは、デフォルト値`false`を`dt_enable_logical_split`のままにして、 `true`に変更しないことを強くお勧めします。詳細については、既知の問題[＃5576](https://github.com/pingcap/tiflash/issues/5576)を参照してください。
-   バックアップ クラスターにTiFlashレプリカがある場合、 TiFlashを実行すると、復元クラスターにはTiFlashレプリカのデータが含まれなくなります。TiFlash レプリカからデータを復元するには、 TiFlashレプリカを手動で構成する必要があります`exchange partition` DDL ステートメントを実行すると、PITR が失敗する可能性があります。アップストリーム データベースが TiDB Lightning の物理インポート モードを使用してデータをインポートする場合、ログ バックアップでデータをバックアップすることはできません。データのインポート後に完全バックアップを実行することをお勧めします。PITR のその他の互換性の問題については、 [PITRの制限](/br/backup-and-restore-overview.md#before-you-use)参照してください。
-   TiDB v6.2.0 以降では、データの復元時にパラメータ`--with-sys-table=true`を指定することで、 `mysql`スキーマでテーブルを復元できます。
-   `ALTER TABLE`ステートメントを実行して複数の列またはインデックスを追加、削除、または変更する場合、TiDB は、同じ DDL ステートメントの変更に関係なく、ステートメントの実行前と実行後のテーブルを比較してテーブルの一貫性をチェックします。一部のシナリオでは、DDL の実行順序が MySQL と完全に互換性がありません。
-   TiDBコンポーネントが v6.2.0 以降の場合、TiKVコンポーネントはv6.2.0 より前のバージョンであってはなりません。
-   TiKV は[動的構成](/dynamic-config.md#modify-tikv-configuration-dynamically)サポートする構成項目`split.region-cpu-overload-threshold-ratio`追加します。
-   スロークエリログ`information_schema.statements_summary`および`information_schema.slow_query` 、バイナリ形式でエンコードされた`binary_plan`または実行プランをエクスポートできます。
-   `SHOW TABLE ... REGIONS`ステートメントに`SCHEDULING_CONSTRAINTS`と`SCHEDULING_STATE` 2 つの列が追加されます。これらはそれぞれ、SQL の配置におけるリージョンスケジュール制約と現在のスケジュール状態を示します。
-   TiDB v6.2.0 以降では、 [ティKV-CDC](https://github.com/tikv/migration/tree/main/cdc)を介して RawKV のデータ変更をキャプチャできます。
-   `ROLLBACK TO SAVEPOINT`を使用してトランザクションを指定されたセーブポイントまでロールバックすると、MySQL は指定されたセーブポイント後にのみ保持されたロックを解放しますが、TiDB悲観的トランザクションでは、TiDB は指定されたセーブポイント後に保持されたロックをすぐには解放しません。代わりに、TiDB はトランザクションがコミットまたはロールバックされたときにすべてのロックを解放します。
-   TiDB v6.2.0 以降、 `SELECT tidb_version()`ステートメントはストア タイプ (tikv または unistore) も返します。
-   TiDB には隠しシステム変数がなくなりました。
-   TiDB v6.2.0 では、2 つの新しいシステム テーブルが導入されました。
    -   `INFORMATION_SCHEMA.VARIABLES_INFO` : TiDB システム変数に関する情報を表示するために使用されます。
    -   `PERFORMANCE_SCHEMA.SESSION_VARIABLES` : TiDB セッション レベルのシステム変数に関する情報を表示するために使用されます。

## 削除された機能 {#removed-feature}

TiDB v6.2.0 以降、 BR を使用した RawKV のバックアップと復元は非推奨になりました。

## 改善点 {#improvements}

-   ティビ

    -   `SHOW COUNT(*) WARNINGS`と`SHOW COUNT(*) ERRORS`ステートメント[＃25068](https://github.com/pingcap/tidb/issues/25068) @ [いいね](https://github.com/likzn)をサポートする

    -   いくつかのシステム変数の検証チェックを追加[＃35048](https://github.com/pingcap/tidb/issues/35048) @ [モルゴ](https://github.com/morgo)

    -   いくつかの型変換のエラーメッセージを最適化[＃32744](https://github.com/pingcap/tidb/issues/32744) @ [ファンレンフー](https://github.com/fanrenhoo)

    -   `KILL`コマンドは DDL 操作[＃24144](https://github.com/pingcap/tidb/issues/24144) @ [モルゴ](https://github.com/morgo)をサポートするようになりました

    -   `SHOW TABLES/DATABASES LIKE …`の出力をMySQL互換にします。出力の列名には`LIKE`値[＃35116](https://github.com/pingcap/tidb/issues/35116) @ [いいね](https://github.com/likzn)が含まれます。

    -   JSON関連関数のパフォーマンスを向上[＃35859](https://github.com/pingcap/tidb/issues/35859) @ [翻訳:](https://github.com/wjhuang2016)

    -   SHA-2 [＃35998](https://github.com/pingcap/tidb/issues/35998) @ [ウイルスディフェンダー](https://github.com/virusdefender)を使用したパスワードログインの検証速度を向上

    -   いくつかのログ出力を簡素化する[＃36011](https://github.com/pingcap/tidb/issues/36011) @ [ドヴェーデン](https://github.com/dveeden)

    -   コプロセッサー通信プロトコルを最適化します。これにより、データ読み取り時の TiDB プロセスのメモリ消費量が大幅に削減され、テーブルをスキャンしてDumplingでデータをエクスポートするシナリオで OOM の問題がさらに軽減されます。システム変数`tidb_enable_paging`は、この通信プロトコルを有効にするかどうかを制御するために使用されます (SESSION または GLOBAL のスコープ)。このプロトコルはデフォルトでは無効になっています。有効にするには、変数値を`true` [＃35633](https://github.com/pingcap/tidb/issues/35633) @ [天菜あま](https://github.com/tiancaiamao) @ [うわー](https://github.com/wshwsh12)に設定します。

    -   一部の演算子（HashJoin、HashAgg、Update、Delete） [うわー](https://github.com/wshwsh12)メモリ追跡の精度を最適化（ [＃35634](https://github.com/pingcap/tidb/issues/35634) @ [＃35635](https://github.com/pingcap/tidb/issues/35635) ）（ [＃34096](https://github.com/pingcap/tidb/issues/34096) [＃35631](https://github.com/pingcap/tidb/issues/35631) [エキシウム](https://github.com/ekexium) ）

    -   システムテーブル`INFORMATION_SCHEMA.DATA_LOCK_WAIT`楽観的トランザクション[＃34609](https://github.com/pingcap/tidb/issues/34609) @ [ロングファンソン](https://github.com/longfangsong)のロック情報の記録をサポートします。

    -   トランザクション[＃34456](https://github.com/pingcap/tidb/issues/34456) @ [ロングファングソン](https://github.com/longfangsong)の監視メトリックを追加します。

-   ティクヴ

    -   HTTP ボディのサイズを縮小するために、gzip を使用してメトリック応答を圧縮することをサポートします[＃12355](https://github.com/tikv/tikv/issues/12355) @ [栄光](https://github.com/glorv)
    -   Grafana ダッシュボード[＃12007](https://github.com/tikv/tikv/issues/12007) @ [ケビン・シアンリウ](https://github.com/kevin-xianliu)の TiKV パネルの読みやすさを向上
    -   Apply演算子[＃12898](https://github.com/tikv/tikv/issues/12898) @ [イーサフロー](https://github.com/ethercflow)のコミットパイプラインのパフォーマンスを最適化する
    -   RocksDBで同時に実行されるサブコンパクション操作の数を動的に変更する機能をサポート ( `rocksdb.max-sub-compactions` ) [＃13145](https://github.com/tikv/tikv/issues/13145) @ [イーサフロー](https://github.com/ethercflow)

-   PD

    -   リージョンのCPU使用率の統計ディメンションをサポートし、Load Base Split [＃12063](https://github.com/tikv/tikv/issues/12063) @ [じゃんぽーと](https://github.com/JmPotato)の使用シナリオを強化します。

-   TiFlash

    -   TiFlash MPPエンジンのエラー処理を改良し、安定性を向上[＃5095](https://github.com/pingcap/tiflash/issues/5095) @ [風の話し手](https://github.com/windtalker) @ [いびん87](https://github.com/yibin87)

    -   UTF8_BIN と UTF8MB4_BIN 照合の比較と並べ替えを最適化[＃5294](https://github.com/pingcap/tiflash/issues/5294) @ [ソロッツ](https://github.com/solotzg)

-   ツール

    -   バックアップと復元 (BR)

        -   大規模クラスタ バックアップ[＃30087](https://github.com/pingcap/tidb/issues/30087) @ [モクイシュル28](https://github.com/MoCuishle28)での S3 レート制限によって発生するバックアップ障害を修正するために、バックアップ データ ディレクトリ構造を調整します。

    -   ティCDC

        -   マルチリージョンシナリオでのランタイムコンテキスト切り替えによって発生するパフォーマンスオーバーヘッドを削減[＃5610](https://github.com/pingcap/tiflow/issues/5610) @ [ヒック](https://github.com/hicqu)

        -   REDOログのパフォーマンスを最適化し、メタデータとデータの不整合の問題を修正します（ [＃6011](https://github.com/pingcap/tiflow/issues/6011) @ [チャールズ・チュン96](https://github.com/CharlesCheung96) ）（ [＃5924](https://github.com/pingcap/tiflow/issues/5924) @ [趙新宇](https://github.com/zhaoxinyu) ）（ [＃6277](https://github.com/pingcap/tiflow/issues/6277) @ [ヒック](https://github.com/hicqu) ）

    -   TiDB Lightning

        -   EOF、読み取りインデックスの準備ができていない、コプロセッサーのタイムアウトなどの再試行可能なエラーを追加します[＃36674](https://github.com/pingcap/tidb/issues/36674) 、 [＃36566](https://github.com/pingcap/tidb/issues/36566) @ [D3ハンター](https://github.com/D3Hunter)

    -   TiUP

        -   TiUPを使用して新しいクラスターがデプロイされると、node-exporterはバージョン[1.3.1](https://github.com/prometheus/node_exporter/releases/tag/v1.3.1)を使用し、blackbox-exporterはバージョン[0.21.1](https://github.com/prometheus/blackbox_exporter/releases/tag/v0.21.1)を使用します。これにより、さまざまなシステムや環境でのデプロイメントが成功します。

## バグ修正 {#bug-fixes}

-   ティビ

    -   クエリ条件でパーティション キーが使用され、照合がクエリ パーティション テーブル[＃32749](https://github.com/pingcap/tidb/issues/32749) @ [ミョンス](https://github.com/mjonss)の照合と異なる場合にパーティションが誤ってプルーニングされる問題を修正しました。
    -   ホスト[＃33061](https://github.com/pingcap/tidb/issues/33061) @ [モルゴ](https://github.com/morgo)に大文字が含まれている場合、 `SET ROLE`付与されたロールと一致しない問題を修正しました。
    -   `auto_increment`の列を[＃34891](https://github.com/pingcap/tidb/issues/34891) @ [定義2014](https://github.com/Defined2014)でドロップできない問題を修正
    -   `SHOW CONFIG`削除された構成項目がいくつか表示される問題を修正[＃34867](https://github.com/pingcap/tidb/issues/34867) @ [モルゴ](https://github.com/morgo)
    -   `SHOW DATABASES LIKE …`大文字と小文字を区別する問題を修正[＃34766](https://github.com/pingcap/tidb/issues/34766) @ [エ1イヤ1](https://github.com/e1ijah1)
    -   `SHOW TABLE STATUS LIKE ...`大文字と小文字を区別する問題を修正[＃7518](https://github.com/pingcap/tidb/issues/7518) @ [いいね](https://github.com/likzn)
    -   `max-index-length`が非厳密モードでエラーを報告する問題を修正[＃34931](https://github.com/pingcap/tidb/issues/34931) @ [エ1イヤ1](https://github.com/e1ijah1)
    -   `ALTER COLUMN ... DROP DEFAULT`機能しない問題を修正[＃35018](https://github.com/pingcap/tidb/issues/35018) @ [定義2014](https://github.com/Defined2014)
    -   テーブルを作成するときに、列のデフォルト値とタイプが一致せず、自動的に修正されない問題を修正[＃34881](https://github.com/pingcap/tidb/issues/34881) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)
    -   `DROP USER` [＃35059](https://github.com/pingcap/tidb/issues/35059) @ [lcwangchao](https://github.com/lcwangchao)を実行した後、 `mysql.columns_priv`テーブルのデータが同期的に削除されない問題を修正しました。
    -   一部のシステムのスキーマ内でのテーブル作成を禁止することで、DDL ジャムの問題を修正しました[＃35205](https://github.com/pingcap/tidb/issues/35205) @ [タンジェンタ](https://github.com/tangenta)
    -   パーティション化されたテーブルをクエリすると、場合によっては「インデックス範囲外」および「未使用のインデックス」エラーが報告される問題を修正[＃35181](https://github.com/pingcap/tidb/issues/35181) @ [ミョンス](https://github.com/mjonss)
    -   `INTERVAL expr unit + expr`エラー[#30253](https://github.com/pingcap/tidb/issues/30253) @ [ミョンス](https://github.com/mjonss)を報告する可能性がある問題を修正
    -   トランザクション[＃35644](https://github.com/pingcap/tidb/issues/35644) @ [翻訳者](https://github.com/djshow832)で作成された後に一時テーブルが見つからないバグを修正
    -   照合順序を`ENUM`列[＃31637](https://github.com/pingcap/tidb/issues/31637) @ [翻訳:](https://github.com/wjhuang2016)に設定すると発生するpanic問題を修正
    -   1 つの PD ノードがダウンすると、他の PD ノード[＃35708](https://github.com/pingcap/tidb/issues/35708) @ [タンジェンタ](https://github.com/tangenta)を再試行しないため、 `information_schema.TIKV_REGION_STATUS`のクエリが失敗する問題を修正しました。
    -   `SHOW CREATE TABLE …`セットまたは`SET character_set_results = GBK` [＃31338](https://github.com/pingcap/tidb/issues/31338) @ [タンジェンタ](https://github.com/tangenta)の後の`ENUM`列が正しく表示されない問題を修正しました
    -   システム変数`tidb_log_file_max_days`と`tidb_config` [＃35190](https://github.com/pingcap/tidb/issues/35190) @ [モルゴ](https://github.com/morgo)の誤ったスコープを修正
    -   `SHOW CREATE TABLE`の出力が MySQL の`ENUM`目または`SET`列目[＃36317](https://github.com/pingcap/tidb/issues/36317) @ [定義2014](https://github.com/Defined2014)と互換性がない問題を修正しました。
    -   テーブル作成時に`LONG BYTE`列の動作がMySQL [＃36239](https://github.com/pingcap/tidb/issues/36239) @ [定義2014](https://github.com/Defined2014)と互換性がない問題を修正
    -   `auto_increment = x`一時テーブル[＃36224](https://github.com/pingcap/tidb/issues/36224) @ [翻訳者](https://github.com/djshow832)に反映されない問題を修正
    -   列を同時に変更する際の誤ったデフォルト値を修正[＃35846](https://github.com/pingcap/tidb/issues/35846) @ [翻訳:](https://github.com/wjhuang2016)
    -   可用性を向上させるために、不健全な TiKV ノードにリクエストを送信しないようにする[＃34906](https://github.com/pingcap/tidb/issues/34906) @ [スティクナーフ](https://github.com/sticnarf)
    -   LOAD DATA ステートメント[＃35198](https://github.com/pingcap/tidb/issues/35198) @ [スペードA-タン](https://github.com/SpadeA-Tang)で列リストが機能しない問題を修正
    -   いくつかのシナリオで、悲観的ロックが非一意のセカンダリインデックス[＃36235](https://github.com/pingcap/tidb/issues/36235) @ [エキシウム](https://github.com/ekexium)に誤って追加される問題を修正しました。

-   ティクヴ

    -   悲観的トランザクション[＃11612](https://github.com/tikv/tikv/issues/11612) @ [スティクナーフ](https://github.com/sticnarf)で`WriteConflict`エラーを報告しないようにする
    -   非同期コミットが有効な場合の悲観的トランザクションにおけるコミットレコードの重複の可能性を修正[＃12615](https://github.com/tikv/tikv/issues/12615) @ [スティクナーフ](https://github.com/sticnarf)
    -   `storage.api-version` `1`から`2` [＃12600](https://github.com/tikv/tikv/issues/12600) @ [ピンギュ](https://github.com/pingyu)に変更するときに TiKV がパニックになる問題を修正しました
    -   TiKV と PD [＃12518](https://github.com/tikv/tikv/issues/12518) @ [5kbpsの](https://github.com/5kbpers)間のリージョンサイズ設定が一致しない問題を修正
    -   TiKVがPDクライアント[＃12506](https://github.com/tikv/tikv/issues/12506) @ [コナー1996](https://github.com/Connor1996) [＃12827](https://github.com/tikv/tikv/issues/12827)再接続し続ける問題を修正
    -   空の文字列[＃12673](https://github.com/tikv/tikv/issues/12673) @ [うわー](https://github.com/wshwsh12)型変換を実行するときに TiKV がパニックになる問題を修正
    -   `DATETIME`値に小数点が含まれる場合や`Z` [＃12739](https://github.com/tikv/tikv/issues/12739) @ [ゲンリキ](https://github.com/gengliqi)場合に発生する時間解析エラーの問題を修正しました。
    -   Apply 演算子によって TiKV RocksDB に書き込まれるパフォーマンス コンテキストが粗粒度[＃11044](https://github.com/tikv/tikv/issues/11044) @ [リクササシネーター](https://github.com/LykxSassinator)になる問題を修正しました
    -   [バックアップ](/tikv-configuration-file.md#backup) / [輸入](/tikv-configuration-file.md#import) / [CDC](/tikv-configuration-file.md#cdc)の設定が無効な場合に TiKV が起動に失敗する問題を修正[＃12771](https://github.com/tikv/tikv/issues/12771) @ [3ポインター](https://github.com/3pointer)
    -   ピアが同時に分割され、破棄されたときに発生する可能性のあるpanic問題を修正[＃12825](https://github.com/tikv/tikv/issues/12825) @ [ビジージェイ](https://github.com/BusyJay)
    -   リージョンマージプロセス[＃12663](https://github.com/tikv/tikv/issues/12663) @ [ビジージェイ](https://github.com/BusyJay)でソースピアがスナップショットによってログをキャッチアップするときに発生する可能性のあるpanic問題を修正しました。
    -   `max_sample_size`が`0` [＃11192](https://github.com/tikv/tikv/issues/11192) @ [リクササシネーター](https://github.com/LykxSassinator)に設定されている場合に統計を分析すると発生するpanicの問題を修正しました
    -   Raft Engineが有効になっているときに暗号化キーがクリーンアップされない問題を修正[＃12890](https://github.com/tikv/tikv/issues/12890) @ [タボキ](https://github.com/tabokie)
    -   `get_valid_int_prefix`関数が TiDB と互換性がない問題を修正しました。たとえば、 `FLOAT`型が誤って`INT` [＃13045](https://github.com/tikv/tikv/issues/13045) @ [グオシャオゲ](https://github.com/guo-shaoge)に変換されていました。
    -   新しいリージョンのコミットログ期間が長すぎるため、QPS が[＃13077](https://github.com/tikv/tikv/issues/13077) @ [コナー1996](https://github.com/Connor1996)低下する問題を修正しました。
    -   リージョンハートビートが中断された後にPDがTiKVに再接続しない問題を修正[＃12934](https://github.com/tikv/tikv/issues/12934) @ [バッファフライ](https://github.com/bufferflies)

-   ツール

    -   バックアップと復元 (BR)

        -   レート制限されたバックアップタスク[＃31722](https://github.com/pingcap/tidb/issues/31722) @ [モクイシュル28](https://github.com/MoCuishle28)を終了した後、 BR がレート制限をリセットしない問題を修正しました

## 寄稿者 {#contributors}

TiDB コミュニティの以下の貢献者に感謝いたします。

-   [エ1イヤ1](https://github.com/e1ijah1)
-   [プラジュワルボルカル](https://github.com/PrajwalBorkar)
-   [いいね](https://github.com/likzn)
-   [翻訳者](https://github.com/rahulk789)
-   [ウイルスディフェンダー](https://github.com/virusdefender)
-   [ジョイセ06](https://github.com/joycse06)
-   [モルゴ](https://github.com/morgo)
-   [ixuh12](https://github.com/ixuh12)
-   [えり](https://github.com/blacktear23)
-   [ジョンハックス7](https://github.com/johnhaxx7)
-   [ゴーギム1](https://github.com/GoGim1)
-   [レンバオシュオ](https://github.com/renbaoshuo)
-   [ジェオリ](https://github.com/Zheaoli)
-   [ファンレンフー](https://github.com/fanrenhoo)
-   [ヌジュウェルキン](https://github.com/njuwelkin)
-   [ワイリービーバー](https://github.com/wirybeaver)
-   [ヘイコン](https://github.com/hey-kong)
-   [運命](https://github.com/fatelei)
-   [イーストフィッシャー](https://github.com/eastfisher) : 初めての投稿者
-   [ジュニージー](https://github.com/Juneezee) : 初めての投稿者
