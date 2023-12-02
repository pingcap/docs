---
title: TiDB 6.2.0 Release Notes
---

# TiDB 6.2.0 リリースノート {#tidb-6-2-0-release-notes}

発売日：2022年8月23日

TiDB バージョン: 6.2.0-DMR

> **注記：**
>
> TiDB 6.2.0-DMR のドキュメントは[アーカイブされた](https://docs-archive.pingcap.com/tidb/v6.2/)になりました。 PingCAP では、 [最新のLTSバージョン](https://docs.pingcap.com/tidb/stable)の TiDB データベースを使用することをお勧めします。

v6.2.0-DMR の主な新機能と改善点は次のとおりです。

-   TiDB ダッシュボードは[視覚的な実行計画](https://docs.pingcap.com/tidb/v6.2/dashboard-slow-query#visual-execution-plans)をサポートしており、実行計画をより直感的に表示できます。
-   TiDB ダッシュボードに[モニタリングページ](/dashboard/dashboard-monitoring.md)を追加すると、パフォーマンス分析とチューニングがより効率的になります。
-   TiDB 機能の[ビューをロックする](/information-schema/information-schema-data-lock-waits.md)は、楽観的トランザクションの待機情報の表示をサポートし、ロック競合の迅速な特定を容易にします。
-   TiFlash は[新しいバージョンのstorage形式](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)をサポートし、安定性とパフォーマンスを強化します。
-   [ファイングレインシャッフル機能](/system-variables.md#tiflash_fine_grained_shuffle_batch_size-new-in-v620)使用すると、複数のスレッドでウィンドウ関数を並列実行できます。
-   新しい同時 DDL フレームワーク: ブロックされる DDL ステートメントが減り、実行効率が向上します。
-   TiKV は[CPU 使用率を自動的に調整する](/tikv-configuration-file.md#background-quota-limiter)をサポートしているため、安定した効率的なデータベース操作が保証されます。
-   [ポイントインタイムリカバリ (PITR)](/br/backup-and-restore-overview.md)は、過去の任意の時点から TiDB クラスターのスナップショットを新しいクラスターに復元するために導入されました。
-   TiDB Lightning は、クラスター レベルではなく、物理インポート モードで[テーブルレベルでのスケジュールの一時停止](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#scope-of-pausing-scheduling-during-import)をサポートします。
-   BR は[ユーザーおよび権限データの復元](/br/br-snapshot-guide.md#restore-tables-in-the-mysql-schema)をサポートし、バックアップと復元をよりスムーズにします。
-   TiCDC は[特定の種類の DDL イベントのフィルタリング](/ticdc/ticdc-filter.md)をサポートすることで、より多くのデータ レプリケーション シナリオを可能にします。
-   [`SAVEPOINT`機構](/sql-statements/sql-statement-savepoint.md)がサポートされており、トランザクション内のロールバック ポイントを柔軟に制御できます。
-   TiDB は[1 つの`ALTER TABLE`ステートメントだけで複数の列またはインデックスを追加、削除、変更する](/sql-statements/sql-statement-alter-table.md)をサポートします。
-   [クラスター間の RawKV レプリケーション](/tikv-configuration-file.md#api-version-new-in-v610)がサポートされるようになりました。

## 新機能 {#new-features}

### SQL {#sql}

-   物理データ圧縮機能は一般提供されています

    TiFlashバックエンドは、特定の条件に基づいて物理データを自動的に圧縮して、無駄なデータのバックログを削減し、データstorage構造を最適化します。

    データ圧縮が自動的にトリガーされる前に、 TiFlashテーブルに一定量の無駄なデータが存在することがよくあります。この機能を使用すると、適切なタイミングを選択して SQL ステートメントを手動で実行し、 TiFlash内の物理データを即座に圧縮できるため、storageスペースの使用量が削減され、クエリのパフォーマンスが向上します。この機能は TiDB v6.1 では実験的であり、現在は TiDB v6.2.0 で一般提供 (GA) されています。

    [ユーザードキュメント](/sql-statements/sql-statement-alter-table-compact.md#alter-table--compact) [#4145](https://github.com/pingcap/tiflash/issues/4145) @ [ブリーズウィッシュ](https://github.com/breezewish)

### 可観測性 {#observability}

-   PD から TiDB ダッシュボードを分割

    TiDB ダッシュボードは PD からモニタリング ノードに移動されます。これにより、PD に対する TiDB ダッシュボードの影響が軽減され、PD がより安定します。

    @ [ホークソンジー](https://github.com/Hawkson-jee)

-   TiDB ダッシュボードにモニタリング ページが追加されました

    新しいモニタリング ページには、パフォーマンス チューニングに必要な主要な指標が表示されます。これに基づいて、 [データベース時間によるパフォーマンスのチューニング](/performance-tuning-methods.md)を参照してパフォーマンスを分析および調整できます。

    具体的には、ユーザー応答時間とデータベース時間をグローバルかつトップダウンの観点から分析し、ユーザー応答時間のボトルネックがデータベースの問題によって引き起こされているかどうかを確認できます。ボトルネックがデータベースにある場合は、データベース時間の概要と SQLレイテンシーの内訳を使用してボトルネックを特定し、パフォーマンスを調整できます。

    [ユーザードキュメント](/dashboard/dashboard-monitoring.md) [#1381](https://github.com/pingcap/tidb-dashboard/issues/1381) @ [イニシュ9506](https://github.com/YiniXu9506)

-   TiDB ダッシュボードは視覚的な実行計画をサポートします

    TiDB ダッシュボードは、SQL ステートメントおよびモニタリング ページを通じて、視覚的な実行プランと基本的な診断サービスを提供します。この機能は、クエリ プランの各ステップを識別するための新たな視点を提供します。したがって、クエリ実行計画のすべてのトレースをより直感的に学習できます。

    この機能は、複雑で大規模なクエリの実行を学習しようとする場合に特に役立ちます。一方、TiDB ダッシュボードは、クエリ実行プランごとに実行の詳細を自動的に分析し、潜在的な問題を特定し、特定のクエリ プランの実行に必要な時間を短縮するための最適化の提案を提供します。

    [ユーザードキュメント](https://docs.pingcap.com/tidb/v6.2/dashboard-slow-query#visual-execution-plans) [#1224](https://github.com/pingcap/tidb-dashboard/issues/1224) @ [時間と運命](https://github.com/time-and-fate)

-   ロックビューは、楽観的トランザクションの待機情報の表示をサポートします

    ロックの競合が多すぎると、重大なパフォーマンスの問題が発生する可能性があり、ロックの競合を検出することは、そのような問題をトラブルシューティングするために必要な方法です。 v6.2.0 より前では、TiDB は`INFORMATION_SCHEMA.DATA_LOCK_WAITS`システム ビューを使用したロック競合関係の表示をサポートしていましたが、楽観的トランザクションの待機情報は表示されませんでした。 TiDB v6.2.0 は`DATA_LOCK_WAITS`ビューを拡張し、ビュー内の悲観的ロックによってブロックされた楽観的トランザクションをリストします。この機能は、ユーザーがロックの競合を迅速に検出するのに役立ち、アプリケーションを改善するための基盤を提供するため、ロックの競合の頻度が減り、全体的なパフォーマンスが向上します。

    [ユーザードキュメント](/information-schema/information-schema-data-lock-waits.md) [#34609](https://github.com/pingcap/tidb/issues/34609) @ [長い牙の歌](https://github.com/longfangsong)

### パフォーマンス {#performance}

-   外部結合の順序付けをサポートするために`LEADING`オプティマイザー ヒントを改善しました。

    v6.1.0 では、テーブルの結合順序を変更するためにオプティマイザー ヒント`LEADING`が導入されました。ただし、このヒントは外部結合を含むクエリには適用できませんでした。詳細については、 [`LEADING`文書](/optimizer-hints.md#leadingt1_name--tl_name-)を参照してください。 v6.2.0 では、TiDB はこの制限を解除します。外部結合を含むクエリで、このヒントを使用してテーブルの結合順序を指定し、SQL 実行パフォーマンスを向上させ、実行計画の突然の変更を回避できるようになりました。

    [ユーザードキュメント](/optimizer-hints.md#leadingt1_name--tl_name-) [#29932](https://github.com/pingcap/tidb/issues/29932) @ [懐かしい](https://github.com/Reminiscent)

-   新しいオプティマイザ`SEMI_JOIN_REWRITE`を追加して`EXISTS`クエリのパフォーマンスを向上させます

    一部のシナリオでは、 `EXISTS`クエリは最適な実行プランを設定できず、実行時間が長すぎる可能性があります。 v6.2.0 では、オプティマイザーはそのようなシナリオ向けの書き換えルールを追加し、クエリで`SEMI_JOIN_REWRITE`を使用すると、オプティマイザーに強制的にクエリを書き換えさせ、クエリのパフォーマンスを向上させることができます。

    [ユーザードキュメント](/optimizer-hints.md#semi_join_rewrite) [#35323](https://github.com/pingcap/tidb/issues/35323) @ [ウィノロス](https://github.com/winoros)

-   新しいオプティマイザー ヒント`MERGE`を追加して、分析クエリのパフォーマンスを向上させます。

    共通テーブル式 (CTE) は、クエリ ロジックを簡素化する効果的な方法です。複雑なクエリを記述するために広く使用されています。 v6.2.0 より前では、 TiFlash環境では CTE を自動的に拡張できず、MPP の実行効率がある程度制限されていました。 v6.2.0 では、MySQL 互換のオプティマイザー ヒント`MERGE`が導入されています。このヒントにより、オプティマイザは CTE インラインを拡張できるようになり、CTE クエリ結果のコンシューマがTiFlashでクエリを同時に実行できるようになり、一部の分析クエリのパフォーマンスが向上します。

    [ユーザードキュメント](/optimizer-hints.md#merge) [#36122](https://github.com/pingcap/tidb/issues/36122) @ [デイックルプ](https://github.com/dayicklp)

-   一部の分析シナリオで集計操作のパフォーマンスを最適化します。

    TiFlashを使用して OLAP シナリオの列に対して集計操作を実行する場合、集計された列の不均等な分散により重大なデータ スキューが存在し、集計された列に多くの異なる値がある場合、その列に対する`COUNT(DISTINCT)`クエリの実行効率は次のようになります。低い。 v6.2.0 では、単一列に対する`COUNT(DISTINCT)`クエリのパフォーマンスを向上させるために、新しい書き換えルールが導入されました。

    [ユーザードキュメント](/system-variables.md#tidb_opt_skew_distinct_agg-new-in-v620) [#36169](https://github.com/pingcap/tidb/issues/36169) @ [修正データベース](https://github.com/fixdb)

-   TiDB は同時 DDL 操作をサポートします

    TiDB v6.2.0 では、新しい同時 DDL フレームワークが導入されています。これにより、DDL ステートメントを異なるテーブル オブジェクトで同時に実行できるようになり、DDL 操作が他のテーブルでの DDL 操作によってブロックされる問題が修正されます。さらに、TiDB は、複数のテーブルにインデックスを追加する場合、または列タイプを変更する場合の DDL の同時実行をサポートします。これにより、DDL 実行の効率が向上します。

    [#32031](https://github.com/pingcap/tidb/issues/32031) @ [wjhuang2016](https://github.com/wjhuang2016)

-   オプティマイザーは文字列一致の推定を強化します

    文字列一致シナリオでは、オプティマイザーが行数を正確に推定できない場合、最適な実行プランの生成に影響します。たとえば、条件は`like '%xyz'`または正規表現の使用`regex ()` 。このようなシナリオでの推定精度を向上させるために、TiDB v6.2.0 では推定方法が強化されています。新しい方法では、統計情報とシステム変数の TopN 情報を組み合わせて精度を向上させ、一致選択性を手動で変更できるようにすることで、SQL パフォーマンスを向上させます。

    [ユーザードキュメント](/system-variables.md#tidb_default_string_match_selectivity-new-in-v620) [#36209](https://github.com/pingcap/tidb/issues/36209) @ [時間と運命](https://github.com/time-and-fate)

-   TiFlashにプッシュダウンされたウィンドウ関数はマルチスレッドで実行可能

    ファイン グレイン シャッフル機能を有効にすると、ウィンドウ関数を単一スレッドではなく複数のスレッドで実行できるようになります。この機能により、ユーザーの動作を変えることなく、クエリの応答時間が大幅に短縮されます。変数の値を調整することで、シャッフルの粒度を制御できます。

    [ユーザードキュメント](/system-variables.md#tiflash_fine_grained_shuffle_batch_size-new-in-v620) [#4631](https://github.com/pingcap/tiflash/issues/4631) @ [グオシャオゲ](https://github.com/guo-shaoge)

-   TiFlash は新しいバージョンのstorage形式をサポートしています

    新しいstorage形式は、同時実行性が高くワークロードが重いシナリオで GC によって引き起こされる高い CPU 使用率を軽減します。これにより、バックグラウンド タスクの IO トラフィックが大幅に削減され、同時実行性が高くワークロードが重い場合の安定性が向上します。同時に、スペースの拡大とディスクの無駄を大幅に削減できます。

    TiDB v6.2.0 では、データはデフォルトで新しいstorage形式で保存されます。 TiFlashが以前のバージョンから v6.2.0 にアップグレードされた場合、以前のTiFlashバージョンは新しいstorage形式を認識できないため、 TiFlashでインプレース ダウングレードを実行できないことに注意してください。

    TiFlashのアップグレードの詳細については、 [TiFlashアップグレード ガイド](/tiflash-upgrade-guide.md)を参照してください。

    [ユーザードキュメント](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file) [#3594](https://github.com/pingcap/tiflash/issues/3594) @ [ジェイ・ソン・ファン](https://github.com/JaySon-Huang) @ [リデズ](https://github.com/lidezhu) @ [佳秋州](https://github.com/jiaqizho)

-   TiFlash は、複数の同時実行シナリオでデータ スキャンのパフォーマンスを最適化します (実験的)

    TiFlash は、同じデータの読み取り操作をマージすることで同じデータの重複読み取りを削減し、複数の同時タスクの場合のリソース オーバーヘッドを最適化してデータ スキャンのパフォーマンスを向上させます。これにより、同じデータが各タスクで個別に読み取られる必要がある状況や、同じデータが複数の同時タスクに関与している場合に同じデータが同時に複数回読み取られる可能性がある状況が回避されます。

    [ユーザードキュメント](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file) [#5376](https://github.com/pingcap/tiflash/issues/5376) @ [ジンヘリン](https://github.com/JinheLin)

-   TiFlash はデータ スキャンに FastScan を追加し、データの一貫性を犠牲にして読み取りおよび書き込み速度を向上させます (実験的)

    TiDB は v6.2.0 で FastScan を導入しました。一貫性チェックのスキップをサポートし、速度を大幅に向上させます。 FastScan は、オフライン分析タスクなど、データの高精度と一貫性を必要としないシナリオに適しています。以前は、データの一貫性を確保するために、 TiFlash はデータ スキャン プロセス中にデータの一貫性チェックを実行して、複数の異なるバージョンから必要なデータを見つける必要がありました。

    以前のバージョンから TiDB v6.2.0 にアップグレードする場合、デフォルトではすべてのテーブルに対して FastScan が有効になりません。これにより、データの一貫性が確保されます。各テーブルに対して個別に FastScan を有効にすることができます。 TiDB v6.2.0 でテーブルが FastScan に設定されている場合、下位バージョンにダウングレードすると無効になりますが、通常のデータ読み取りには影響しません。この場合、強力な整合性読み取りと同等です。

    [ユーザードキュメント](/tiflash/use-fastscan.md) [#5252](https://github.com/pingcap/tiflash/issues/5252) @ [ホンユニャン](https://github.com/hongyunyan)

### 安定性 {#stability}

-   TiKV は CPU 使用率の自動調整をサポートします (実験的)

    通常、データベースには内部操作を実行するバックグラウンド プロセスがあります。統計情報を収集すると、パフォーマンスの問題を特定し、より適切な実行計画を生成し、データベースの安定性とパフォーマンスを向上させることができます。しかし、より効率的に情報を収集する方法、および日常の使用に影響を与えずにバックグラウンド操作とフォアグラウンド操作のリソース オーバーヘッドのバランスをとる方法は、データベース業界にとって常に頭の痛い問題の 1 つです。

    TiDB v6.2.0 以降、TiKV 構成ファイルを使用したバックグラウンド リクエストの CPU 使用率の設定をサポートします。これにより、TiKV での統計の自動収集などのバックグラウンド操作の CPU 使用率が制限され、バックグラウンド操作によるユーザー操作のリソースの横取りが回避されます。極端な場合には。これにより、データベースの動作が安定して効率的になります。

    同時に、TiDB は CPU 使用率の自動調整もサポートします。その後、TiKV は、インスタンスの CPU 使用率に応じて、バックグラウンド リクエストによって占有される CPU リソースを適応的に調整します。この機能はデフォルトでは無効になっています。

    [ユーザードキュメント](/tikv-configuration-file.md#background-quota-limiter) [#12503](https://github.com/tikv/tikv/issues/12503) @ [ボーンチェンジャー](https://github.com/BornChanger)

### 使いやすさ {#ease-of-use}

-   TiKV は、コマンドライン フラグを使用した詳細な構成情報のリストをサポートします

    TiKV 構成ファイルは、TiKV インスタンスの管理に使用できます。ただし、インスタンスが長時間実行され、別のユーザーによって管理されている場合、どの構成項目が変更され、デフォルト値が何であるかを知るのは困難です。これにより、クラスターをアップグレードするときやデータを移行するときに混乱が生じる可能性があります。 TiDB v6.2.0 以降、tikv-server は、すべての TiKV 構成項目のデフォルト値と現在の値をリストする新しいコマンドライン フラグ[`—-config-info`](/command-line-flags-for-tikv-configuration.md#--config-info-format)をサポートし、ユーザーが TiKV プロセスの起動パラメータを迅速に確認できるようにし、使いやすさを向上させます。

    [ユーザードキュメント](/command-line-flags-for-tikv-configuration.md#--config-info-format) [#12492](https://github.com/tikv/tikv/issues/12492) @ [グロルフ](https://github.com/glorv)

### MySQLの互換性 {#mysql-compatibility}

-   TiDB は、単一の`ALTER TABLE`ステートメントでの複数の列またはインデックスの変更をサポートします。

    v6.2.0 より前では、TiDB は単一の DDL 変更のみをサポートしていたため、異種データベースを移行するときに DDL 操作に互換性がなくなり、複雑な DDL ステートメントを TiDB がサポートする複数の単純な DDL ステートメントに変更するには余分な労力がかかりました。さらに、一部のユーザーは SQL でアセンブリを作成するために ORM フレームワークに依存しているため、SQL の非互換性が発生します。 v6.2.0 以降、TiDB は 1 つの SQL ステートメントでの複数のスキーマ オブジェクトの変更をサポートしています。これは、ユーザーが SQL を実装するのに便利であり、使いやすさが向上します。

    [ユーザードキュメント](/sql-statements/sql-statement-alter-table.md) [#14766](https://github.com/pingcap/tidb/issues/14766) @ [タンジェンタ](https://github.com/tangenta)

-   トランザクションでのセーブポイント設定のサポート

    トランザクションは、データベースがACIDプロパティを保証する一連の連続操作の論理的な集合です。一部の複雑なアプリケーション シナリオでは、トランザクション内の多くの操作を管理する必要があり、場合によってはトランザクション内の一部の操作をロールバックする必要がある場合があります。 「セーブポイント」は、トランザクションの内部実装のための名前付きメカニズムです。このメカニズムを使用すると、トランザクション内のロールバック ポイントを柔軟に制御できるため、より複雑なトランザクションを管理し、さまざまなアプリケーションをより自由に設計できるようになります。

    [ユーザードキュメント](/sql-statements/sql-statement-savepoint.md) [#6840](https://github.com/pingcap/tidb/issues/6840) @ [クレイジークス520](https://github.com/crazycs520)

### データ移行 {#data-migration}

-   BR はユーザーおよび権限データの復元をサポートします

    BR は、通常の復元を実行するときに、ユーザーおよび特権データの復元をサポートします。ユーザーと権限のデータを復元するために追加の復元計画は必要ありません。この機能を有効にするには、 BRを使用してデータを復元するときに`--with-sys-table`パラメーターを指定します。

    [ユーザードキュメント](/br/br-snapshot-guide.md#restore-tables-in-the-mysql-schema) [#35395](https://github.com/pingcap/tidb/issues/35395) @ [D3ハンター](https://github.com/D3Hunter)

-   ログとスナップショットのバックアップと復元に基づくポイントインタイム リカバリ (PITR) のサポート

    PITR は、ログとスナップショットのバックアップと復元に基づいて実装されます。これにより、履歴の任意の時点でのクラスターのスナップショットを新しいクラスターに復元できます。この機能は次のニーズを満たします。

    -   災害復旧における RPO を 20 分未満に短縮します。
    -   アプリケーションからの不正な書き込みの場合は、エラー イベントの前にデータをロールバックするなどして処理します。
    -   法令の要件を満たすために履歴データの監査を実行します。

    この機能には使用制限があります。詳細については、ユーザードキュメントを参照してください。

    [ユーザードキュメント](/br/backup-and-restore-overview.md) [#29501](https://github.com/pingcap/tidb/issues/29501) @ [ジョッカウ](https://github.com/joccau)

-   DM は継続的なデータ検証をサポートします (実験的)

    継続的データ検証は、データ移行中にアップストリームのbinlogとダウンストリームに書き込まれたデータを継続的に比較するために使用されます。バリデータは、一貫性のないデータやレコードの欠落などのデータ例外を識別します。

    この機能は、一般的な完全なデータ検証スキームにおける検証の遅延と過剰なリソース消費の問題を解決します。

    [ユーザードキュメント](/dm/dm-continuous-data-validation.md) [#4426](https://github.com/pingcap/tiflow/issues/4426) @ [D3ハンター](https://github.com/D3Hunter) @ [ブチュイトデゴウ](https://github.com/buchuitoudegou)

-   Amazon S3 バケットのリージョンを自動的に識別する

    データ移行タスクでは、Amazon S3 バケットのリージョンを自動的に識別できます。明示的に領域パラメータを渡す必要はありません。

    [#34275](https://github.com/pingcap/tidb/issues/34275) @ [王楽1321](https://github.com/WangLe1321)

-   TiDB Lightningのディスク クォータ構成のサポート (実験的)

    TiDB Lightning が物理インポート モード (backend=&#39;local&#39;) でデータをインポートする場合、sorted-kv-dir にはソース データを保存するのに十分なスペースが必要です。ディスク容量が不十分な場合、インポート タスクが失敗する可能性があります。新しい`disk_quota`構成を使用して、 TiDB Lightningによって使用されるディスク領域の合計量を制限できるようになりました。これにより、sorted-kv-dir に十分なstorage領域がない場合でもインポート タスクを正常に完了できます。

    [ユーザードキュメント](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#configure-disk-quota-new-in-v620) [#446](https://github.com/pingcap/tidb-lightning/issues/446) @ [ブチュイトデゴウ](https://github.com/buchuitoudegou)

-   TiDB Lightning は、物理インポート モードでの本番クラスターへのデータのインポートをサポートしています。

    以前は、 TiDB Lightningの物理インポート モード (backend=&#39;local&#39;) がターゲット クラスターに大きな影響を与えていました。たとえば、移行中、PD グローバル スケジューリングは一時停止されます。したがって、以前の物理インポート モードは、初期データ インポートにのみ適しています。

    TiDB Lightning は、既存の物理インポート モードを改善します。テーブルのスケジュールを一時停止できるようにすることで、インポートの影響がクラスター レベルからテーブル レベルに軽減されます。つまり、インポートされていないテーブルの読み取りと書き込みが可能です。

    この機能は手動で構成する必要はありません。 TiDB クラスターが v6.1.0 以降のバージョンで、 TiDB Lightningが v6.2.0 以降のバージョンの場合、新しい物理インポート モードは自動的に有効になります。

    [ユーザードキュメント](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#scope-of-pausing-scheduling-during-import) [#35148](https://github.com/pingcap/tidb/issues/35148) @ [ゴズスキー](https://github.com/gozssky)

-   [TiDB Lightningのユーザー ドキュメント](/tidb-lightning/tidb-lightning-overview.md)リファクタリングして、その構造をより合理的かつ明確にします。 「バックエンド」の用語も、新規ユーザーの理解の障壁を下げるために変更されています。

    -   「ローカル バックエンド」を「物理インポート モード」に置き換えます。
    -   「tidb バックエンド」を「論理インポート モード」に置き換えます。

### TiDB データ共有サブスクリプション {#tidb-data-share-subscription}

-   クラスター間の RawKV レプリケーションをサポート (実験的)

    新しいコンポーネントTiKV-CDC を使用して、RawKV のデータ変更をサブスクライブし、ダウンストリーム TiKV クラスターにデータ変更をリアルタイムでレプリケートすることをサポートします。これにより、クラスター間のレプリケーションが可能になります。

    [ユーザードキュメント](/tikv-configuration-file.md#api-version-new-in-v610) [#11965](https://github.com/tikv/tikv/issues/11965) @ [ピンギュ](https://github.com/pingyu)

-   DDL および DML イベントのフィルタリングをサポート

    特別な場合には、増分データ変更ログのフィルター ルールを設定することが必要になる場合があります。たとえば、DROP TABLE などの高リスク DDL イベントをフィルタリングします。 v6.2.0 以降、TiCDC は、指定されたタイプの DDL イベントのフィルタリングと、SQL 式に基づいた DML イベントのフィルタリングをサポートします。これにより、TiCDC はより多くのデータ レプリケーション シナリオに適用できるようになります。

    [ユーザードキュメント](/ticdc/ticdc-filter.md) [#6160](https://github.com/pingcap/tiflow/issues/6160) @ [東門](https://github.com/asddongmen)

## 互換性の変更 {#compatibility-changes}

### システム変数 {#system-variables}

| 変数名                                                                                                                    | 種類の変更    | 説明                                                                                                                                                                                                       |
| ---------------------------------------------------------------------------------------------------------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [tidb_enable_new_cost_interface](/system-variables.md#tidb_enable_new_cost_interface-new-in-v620)                      | 新しく追加された | この変数は、 [リファクタリングされたコストモデルの実装](/cost-model.md#cost-model-version-2)を有効にするかどうかを制御します。                                                                                                                      |
| [tidb_cost_model_version](/system-variables.md#tidb_cost_model_version-new-in-v620)                                    | 新しく追加された | TiDB は、物理的な最適化中にコスト モデルを使用してインデックスと演算子を選択します。この変数は、コスト モデルのバージョンを選択するために使用されます。 TiDB v6.2.0 ではコスト モデル バージョン 2 が導入されており、内部テストでは以前のバージョンよりも正確です。                                                           |
| tidb_enable_concurrent_ddl                                                                                             | 新しく追加された | この変数は、TiDB が同時 DDL ステートメントを使用できるようにするかどうかを制御します。この変数は変更しないでください。この変数を無効にするリスクは不明ですが、クラスターのメタデータが破損する可能性があります。                                                                                            |
| [tiflash_fine_graned_shuffle_stream_count](/system-variables.md#tiflash_fine_grained_shuffle_stream_count-new-in-v620) | 新しく追加された | この変数は、ウィンドウ関数が実行のためにTiFlashにプッシュダウンされるときのウィンドウ関数実行の同時実行レベルを制御します。                                                                                                                                        |
| [tiflash_fine_graned_shuffle_batch_size](/system-variables.md#tiflash_fine_grained_shuffle_batch_size-new-in-v620)     | 新しく追加された | Fine Grained Shuffle を有効にすると、 TiFlashにプッシュダウンされたウィンドウ関数を並列実行できます。この変数は、送信者によって送信されるデータのバッチ サイズを制御します。累積行数がこの値を超えると、送信者はデータを送信します。                                                                        |
| [tidb_default_string_match_selectivity](/system-variables.md#tidb_default_string_match_selectivity-new-in-v620)        | 新しく追加された | この変数は、行数を見積もる際のフィルター条件における`like` 、 `rlike` 、および`regexp`関数のデフォルトの選択性を設定するために使用されます。この変数は、TopN がこれらの関数の推定に役立つようにするかどうかも制御します。                                                                              |
| [tidb_enable_analyze_snapshot](/system-variables.md#tidb_enable_analyze_snapshot-new-in-v620)                          | 新しく追加された | この変数は、 `ANALYZE`を実行するときに履歴データを読み取るか最新のデータを読み取るかを制御します。                                                                                                                                                   |
| [tidb_generate_binary_plan](/system-variables.md#tidb_generate_binary_plan-new-in-v620)                                | 新しく追加された | この変数は、スロー ログおよびステートメント サマリーにバイナリ エンコードされた実行プランを生成するかどうかを制御します。                                                                                                                                           |
| [tidb_opt_skew_distinct_agg](/system-variables.md#tidb_opt_skew_distinct_agg-new-in-v620)                              | 新しく追加された | この変数は、オプティマイザが`DISTINCT`集合関数を2 レベルの集合関数に書き換えるかどうか ( `SELECT b, COUNT(DISTINCT a) FROM t GROUP BY b`を`SELECT b, COUNT(a) FROM (SELECT b, a FROM t GROUP BY b, a) t GROUP BY b`に書き換えるなど) を設定します。           |
| [tidb_enable_noop_variables](/system-variables.md#tidb_enable_noop_variables-new-in-v620)                              | 新しく追加された | この変数は、 `SHOW [GLOBAL] VARIABLES`の結果に`noop`変数を表示するかどうかを制御します。                                                                                                                                             |
| [tidb_min_paging_size](/system-variables.md#tidb_min_paging_size-new-in-v620)                                          | 新しく追加された | この変数は、コプロセッサーのページング要求プロセス中に最大行数を設定するために使用されます。                                                                                                                                                           |
| [tidb_txn_commit_batch_size](/system-variables.md#tidb_txn_commit_batch_size-new-in-v620)                              | 新しく追加された | この変数は、TiDB が TiKV に送信するトランザクション コミット リクエストのバッチ サイズを制御するために使用されます。                                                                                                                                        |
| tidb_enable_change_multi_schema                                                                                        | 削除されました  | この変数は、1 つの`ALTER TABLE`ステートメントで複数の列またはインデックスを変更できるかどうかを制御するために使用されます。                                                                                                                                    |
| [tidb_enable_outer_join_reorder](/system-variables.md#tidb_enable_outer_join_reorder-new-in-v610)                      | 修正済み     | この変数は、TiDB の結合したテーブルの再配置アルゴリズムがアウター ジョインをサポートするかどうかを制御します。 v6.1.0 では、デフォルト値は`ON`です。これは、Outer Join に対する Join Reorder のサポートがデフォルトで有効であることを意味します。 v6.2.0 以降、デフォルト値は`OFF`です。これは、サポートがデフォルトで無効になっていることを意味します。 |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーション                                                                                                                | 種類の変更      | 説明                                                                                                         |
| -------------- | ------------------------------------------------------------------------------------------------------------------------- | ---------- | ---------------------------------------------------------------------------------------------------------- |
| TiDB           | フィードバック確率                                                                                                                 | 削除されました    | この構成はもう有効ではないため、お勧めできません。                                                                                  |
| TiDB           | クエリフィードバック制限                                                                                                              | 削除されました    | この構成はもう有効ではないため、お勧めできません。                                                                                  |
| TiKV           | [サーバーの.simplify-metrics](/tikv-configuration-file.md#simplify-metrics-new-in-v620)                                        | 新しく追加された   | この構成では、返される監視メトリックを簡素化するかどうかを指定します。                                                                        |
| TiKV           | [クォータ.バックグラウンド CPU 時間](/tikv-configuration-file.md#background-cpu-time-new-in-v620)                                       | 新しく追加された   | この構成では、読み取りおよび書き込みリクエストを処理するために TiKV バックグラウンドで使用される CPU リソースのソフト制限を指定します。                                  |
| TiKV           | [クォータ.バックグラウンド書き込み帯域幅](/tikv-configuration-file.md#background-write-bandwidth-new-in-v620)                                | 新しく追加された   | この構成では、バックグラウンド トランザクションがデータを書き込む帯域幅のソフト制限を指定します (現在は有効ではありません)。                                           |
| TiKV           | [クォータ.バックグラウンド読み取り帯域幅](/tikv-configuration-file.md#background-read-bandwidth-new-in-v620)                                 | 新しく追加された   | この構成では、バックグラウンド トランザクションとコプロセッサーがデータを読み取る帯域幅のソフト制限を指定します (現在は有効ではありません)。                                   |
| TiKV           | [quota.enable-auto-tune](/tikv-configuration-file.md#enable-auto-tune-new-in-v620)                                        | 新しく追加された   | この構成では、クォータの自動調整を有効にするかどうかを指定します。この構成項目が有効になっている場合、TiKV は TiKV インスタンスの負荷に基づいてバックグラウンド リクエストのクォータを動的に調整します。 |
| TiKV           | rocksdb.enable-pipelined-commit                                                                                           | 削除されました    | この構成は無効になりました。                                                                                             |
| TiKV           | gc-マージ-リライト                                                                                                               | 削除されました    | この構成は無効になりました。                                                                                             |
| TiKV           | [ログバックアップ.有効にする](/tikv-configuration-file.md#enable-new-in-v620)                                                          | 新しく追加された   | この構成は、TiKV でログ バックアップを有効にするかどうかを制御します。                                                                     |
| TiKV           | [ログバックアップ.ファイルサイズ制限](/tikv-configuration-file.md#file-size-limit-new-in-v620)                                             | 新しく追加された   | この構成では、ログ バックアップ データのサイズ制限を指定します。この制限に達すると、データは自動的に外部storageにフラッシュされます。                                    |
| TiKV           | [log-backup.initial-scan-pending-memory-quota](/tikv-configuration-file.md#initial-scan-pending-memory-quota-new-in-v620) | 新しく追加された   | この構成では、増分スキャン データの保存に使用されるキャッシュのクォータを指定します。                                                                |
| TiKV           | [ログバックアップ.最大フラッシュ間隔](/tikv-configuration-file.md#max-flush-interval-new-in-v620)                                          | 新しく追加された   | この構成では、ログバックアップにおいてバックアップデータを外部storageに書き込む最大間隔を指定します。                                                     |
| TiKV           | [ログバックアップ.初期スキャンレート制限](/tikv-configuration-file.md#initial-scan-rate-limit-new-in-v620)                                   | 新しく追加された   | この構成では、ログ バックアップの増分データ スキャンにおけるスループットのレート制限を指定します。                                                         |
| TiKV           | [ログバックアップ.num-threads](/tikv-configuration-file.md#num-threads-new-in-v620)                                               | 新しく追加された   | この構成では、ログのバックアップに使用されるスレッドの数を指定します。                                                                        |
| TiKV           | [ログバックアップ.一時パス](/tikv-configuration-file.md#temp-path-new-in-v620)                                                        | 新しく追加された   | この構成では、ログ ファイルが外部storageにフラッシュされる前に書き込まれる一時パスを指定します。                                                       |
| TiKV           | [rocksdb.defaultcf.format-version](/tikv-configuration-file.md#format-version-new-in-v620)                                | 新しく追加された   | SST ファイルのフォーマット バージョン。                                                                                     |
| TiKV           | [rocksdb.writecf.format-version](/tikv-configuration-file.md#format-version-new-in-v620)                                  | 新しく追加された   | SST ファイルのフォーマット バージョン。                                                                                     |
| TiKV           | [rocksdb.lockcf.format-version](/tikv-configuration-file.md#format-version-new-in-v620)                                   | 新しく追加された   | SST ファイルのフォーマット バージョン。                                                                                     |
| PD             | レプリケーションモード.dr-auto-sync.wait-async-timeout                                                                               | 削除されました    | この構成は有効にならず、削除されます。                                                                                        |
| PD             | レプリケーションモード.dr-auto-sync.wait-sync-timeout                                                                                | 削除されました    | この構成は有効にならず、削除されます。                                                                                        |
| TiFlash        | [`storage.format_version`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                              | 修正済み       | デフォルト値`format_version`が、v6.2.0 以降のバージョンのデフォルト形式である`4`に変更され、書き込み増幅とバックグラウンド タスクのリソース消費が削減されます。              |
| TiFlash        | [profiles.default.dt_enable_read_thread](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                | 新しく追加された   | この構成は、storageエンジンからの読み取りリクエストを処理するためにスレッド プールを使用するかどうかを制御します。デフォルト値は`false`です。                             |
| TiFlash        | [profiles.default.dt_page_gc_threshold](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                 | 新しく追加された   | この構成では、PageStorage データ ファイル内の有効なデータの最小比率を指定します。                                                            |
| TiCDC          | [--上書きチェックポイント-ts](/ticdc/ticdc-manage-changefeed.md#resume-a-replication-task)                                           | 新しく追加された   | この設定は`cdc cli changefeed resume`サブコマンドに追加されます。                                                             |
| TiCDC          | [--いいえ確認](/ticdc/ticdc-manage-changefeed.md#resume-a-replication-task)                                                    | 新しく追加された   | この設定は`cdc cli changefeed resume`サブコマンドに追加されます。                                                             |
| DM             | [モード](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)                                      | 新しく追加された   | この構成はバリデーターパラメーターです。オプションの値は`full` 、 `fast` 、および`none`です。デフォルト値は`none`で、データは検証されません。                       |
| DM             | [ワーカー数](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)                                    | 新しく追加された   | この構成はバリデーター・パラメーターであり、バックグラウンドでの検証ワーカーの数を指定します。デフォルト値は`4`です。                                               |
| DM             | [行エラー遅延](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)                                   | 新しく追加された   | この構成はバリデーターパラメーターです。指定された時間内に行が検証されなかった場合、その行はエラー行としてマークされます。デフォルト値は 30m、つまり 30 分です。                       |
| TiDB Lightning | [tikv-importer.store-write-bwlimit](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)                  | 新たに追加されました | この構成は、 TiDB Lightning が各 TiKV ストアにデータを書き込むときの書き込み帯域幅を決定します。デフォルト値は`0`で、帯域幅が制限されていないことを示します。                |
| TiDB Lightning | [tikv-importer.disk-quota](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#configure-disk-quota-new-in-v620) | 新たに追加されました | この構成では、 TiDB Lightningによって使用されるstorageスペースが制限されます。                                                         |

### その他 {#others}

-   TiFlash `format_version` `4`から`3`にダウングレードすることはできません。詳細は[TiFlashアップグレード ガイド](/tiflash-upgrade-guide.md)を参照してください。
-   v6.2.0 以降のバージョンでは、デフォルト値`false` `dt_enable_logical_split`し、 `true`に変更しないことを強くお勧めします。詳細については、既知の問題[#5576](https://github.com/pingcap/tiflash/issues/5576)を参照してください。
-   バックアップ クラスターにTiFlashレプリカがある場合、PITR を実行すると、復元クラスターにはTiFlashレプリカのデータが含まれなくなります。 TiFlashレプリカからデータを復元するには、 TiFlashレプリカを手動で構成する必要があります。 `exchange partition` DDL ステートメントを実行すると、PITR が失敗する可能性があります。アップストリーム データベースが TiDB Lightning の物理インポート モードを使用してデータをインポートする場合、データはログ バックアップでバックアップできません。データのインポート後に完全バックアップを実行することをお勧めします。 PITR のその他の互換性の問題については、 [PITRの制限](/br/backup-and-restore-overview.md#before-you-use)を参照してください。
-   TiDB v6.2.0 以降、データ復元時にパラメータ`--with-sys-table=true`を指定することで、 `mysql`スキーマでテーブルを復元できます。
-   `ALTER TABLE`ステートメントを実行して複数の列またはインデックスを追加、削除、または変更すると、TiDB は、同じ DDL ステートメントの変更に関係なく、ステートメントの実行前と実行後のテーブルを比較することによってテーブルの一貫性をチェックします。一部のシナリオでは、DDL の実行順序は MySQL と完全な互換性がありません。
-   TiDBコンポーネントが v6.2.0 以降の場合、TiKVコンポーネントはv6.2.0 より前であってはなりません。
-   TiKV は、 [動的構成](/dynamic-config.md#modify-tikv-configuration-dynamically)をサポートする構成項目`split.region-cpu-overload-threshold-ratio`を追加します。
-   低速クエリ ログ`information_schema.statements_summary`および`information_schema.slow_query` 、バイナリ形式でエンコードされた実行プラン`binary_plan`をエクスポートできます。
-   `SHOW TABLE ... REGIONS`ステートメントに`SCHEDULING_CONSTRAINTS`と`SCHEDULING_STATE` 2 つの列が追加されます。これらはそれぞれ、SQL での配置におけるリージョンのスケジュール制約と現在のスケジュール状態を示します。
-   TiDB v6.2.0 以降、 [TiKV-CDC](https://github.com/tikv/migration/tree/main/cdc)を介して RawKV のデータ変更をキャプチャできるようになりました。
-   トランザクションを指定されたセーブポイントにロールバックするために`ROLLBACK TO SAVEPOINT`が使用される場合、MySQL は指定されたセーブポイントの後にのみ保持されているロックを解放しますが、TiDB悲観的トランザクションでは、TiDB は指定されたセーブポイントの後に保持されているロックをすぐには解放しません。代わりに、TiDB はトランザクションがコミットまたはロールバックされるときにすべてのロックを解放します。
-   TiDB v6.2.0 以降、 `SELECT tidb_version()`ステートメントはストア タイプ (tikv または unistore) も返します。
-   TiDB には隠しシステム変数がなくなりました。
-   TiDB v6.2.0 では、2 つの新しいシステム テーブルが導入されています。
    -   `INFORMATION_SCHEMA.VARIABLES_INFO` : TiDB システム変数に関する情報を表示するために使用されます。
    -   `PERFORMANCE_SCHEMA.SESSION_VARIABLES` : TiDB セッションレベルのシステム変数に関する情報を表示するために使用されます。

## 削除された機能 {#removed-feature}

TiDB v6.2.0 以降、 BRを使用した RawKV のバックアップと復元は非推奨になりました。

## 改善点 {#improvements}

-   TiDB

    -   `SHOW COUNT(*) WARNINGS`と`SHOW COUNT(*) ERRORS`ステートメントをサポート[#25068](https://github.com/pingcap/tidb/issues/25068) @ [リクズン](https://github.com/likzn)

    -   いくつかのシステム変数[#35048](https://github.com/pingcap/tidb/issues/35048) @ [モルゴ](https://github.com/morgo)の検証チェックを追加

    -   一部の型変換のエラー メッセージを最適化[#32447](https://github.com/pingcap/tidb/issues/32744) @ [ファンレンフー](https://github.com/fanrenhoo)

    -   `KILL`コマンドは DDL 操作[#24144](https://github.com/pingcap/tidb/issues/24144) @ [モルゴ](https://github.com/morgo)をサポートするようになりました。

    -   もう`SHOW TABLES/DATABASES LIKE …`つの出力を MySQL 互換にします。出力の列名には`LIKE`値[#35116](https://github.com/pingcap/tidb/issues/35116) @ [リクズン](https://github.com/likzn)が含まれます。

    -   JSON関連関数のパフォーマンスを向上[#35859](https://github.com/pingcap/tidb/issues/35859) @ [wjhuang2016](https://github.com/wjhuang2016)

    -   SHA-2 [#35998](https://github.com/pingcap/tidb/issues/35998) @ [ウイルスディフェンダー](https://github.com/virusdefender)を使用したパスワード ログインの検証速度の向上

    -   一部のログ出力を簡素化[#36011](https://github.com/pingcap/tidb/issues/36011) @ [ドヴィーデン](https://github.com/dveeden)

    -   コプロセッサー通信プロトコルを最適化します。これにより、データ読み取り時の TiDB プロセスのメモリ消費量が大幅に削減され、テーブルのスキャンやDumplingによるデータのエクスポートのシナリオにおける OOM 問題がさらに軽減されます。システム変数`tidb_enable_paging`は、この通信プロトコルを (SESSION または GLOBAL の範囲で) 有効にするかどうかを制御するために導入されています。このプロトコルはデフォルトでは無効になっています。有効にするには、変数値を`true` [#35633](https://github.com/pingcap/tidb/issues/35633) @ [ティアンチャイアマ](https://github.com/tiancaiamao) @ [wshwsh12](https://github.com/wshwsh12)に設定します。

    -   一部の演算子 (HashJoin、HashAgg、Update、Delete) のメモリ追跡の精度を最適化します ( [#35634](https://github.com/pingcap/tidb/issues/35634) 、 [#35631](https://github.com/pingcap/tidb/issues/35631) 、 [#35635](https://github.com/pingcap/tidb/issues/35635) @ [wshwsh12](https://github.com/wshwsh12) ) ( [#34096](https://github.com/pingcap/tidb/issues/34096) @ [エキシウム](https://github.com/ekexium) )

    -   システム テーブル`INFORMATION_SCHEMA.DATA_LOCK_WAIT`は、楽観的トランザクション[#34609](https://github.com/pingcap/tidb/issues/34609) @ [ロングファングソン](https://github.com/longfangsong)のロック情報の記録をサポートします。

    -   トランザクション[#34456](https://github.com/pingcap/tidb/issues/34456) @ [長い牙の歌](https://github.com/longfangsong)の監視メトリクスを追加します。

-   TiKV

    -   gzip を使用したメトリクス応答の圧縮をサポートし、HTTP 本文のサイズ[#12355](https://github.com/tikv/tikv/issues/12355) @ [グロルフ](https://github.com/glorv)を削減します。
    -   Grafana ダッシュボード[#12007](https://github.com/tikv/tikv/issues/12007) @ [ケビン・シャンリウ](https://github.com/kevin-xianliu)の TiKV パネルの読みやすさを改善しました。
    -   適用オペレーター[#12898](https://github.com/tikv/tikv/issues/12898) @ [エーテルフロー](https://github.com/ethercflow)のコミット パイプライン パフォーマンスを最適化します。
    -   RocksDB で同時に実行されるサブコンパクション操作の数の動的変更をサポート ( `rocksdb.max-sub-compactions` ) [#13145](https://github.com/tikv/tikv/issues/13145) @ [エーテルフロー](https://github.com/ethercflow)

-   PD

    -   リージョンの CPU 使用率の統計的側面をサポートし、ロード ベース分割[#12063](https://github.com/tikv/tikv/issues/12063) @ [ジンポタト](https://github.com/JmPotato)の使用シナリオを強化します。

-   TiFlash

    -   TiFlash MPP エンジンのエラー処理を改良し、安定性を向上させました[#5095](https://github.com/pingcap/tiflash/issues/5095) @ [ウィンドトーカー](https://github.com/windtalker) @ [イービン87](https://github.com/yibin87)

    -   UTF8_BIN と UTF8MB4_BIN 照合順序[#5294](https://github.com/pingcap/tiflash/issues/5294) @ [ソロッツグ](https://github.com/solotzg)の比較と並べ替えを最適化します。

-   ツール

    -   バックアップと復元 (BR)

        -   バックアップ データ ディレクトリ構造を調整して、大規模クラスタ バックアップ[#30087](https://github.com/pingcap/tidb/issues/30087) @ [モクイシュル28](https://github.com/MoCuishle28)での S3 レート制限によって引き起こされるバックアップの失敗を修正します。

    -   TiCDC

        -   マルチリージョン シナリオ[#5610](https://github.com/pingcap/tiflow/issues/5610) @ [ひっくり返る](https://github.com/hicqu)でのランタイム コンテキストの切り替えによって生じるパフォーマンスのオーバーヘッドを削減します。

        -   REDO ログのパフォーマンスを最適化し、メタおよびデータの不整合の問題を修正します ( [#6011](https://github.com/pingcap/tiflow/issues/6011) @ [CharlesCheung96](https://github.com/CharlesCheung96) ) ( [#5924](https://github.com/pingcap/tiflow/issues/5924) @ [ジャオシンユ](https://github.com/zhaoxinyu) ) ( [#6277](https://github.com/pingcap/tiflow/issues/6277) @ [ひっくり返る](https://github.com/hicqu) )

    -   TiDB Lightning

        -   EOF、読み取りインデックスの準備ができていません、コプロセッサータイムアウト[#36674](https://github.com/pingcap/tidb/issues/36674) 、 [#36566](https://github.com/pingcap/tidb/issues/36566) @ [D3ハンター](https://github.com/D3Hunter)の再試行可能なエラーを追加します。

    -   TiUP

        -   TiUPを使用して新しいクラスターがデプロイされる場合、node-exporter はバージョン[1.3.1](https://github.com/prometheus/node_exporter/releases/tag/v1.3.1)を使用し、blackbox-exporter はバージョン[0.21.1](https://github.com/prometheus/blackbox_exporter/releases/tag/v0.21.1)を使用します。これにより、さまざまなシステムや環境でのデプロイが確実に成功します。

## バグの修正 {#bug-fixes}

-   TiDB

    -   クエリ条件でパーティション キーが使用されており、照合順序がクエリ パーティション テーブル[#32749](https://github.com/pingcap/tidb/issues/32749) @ [むじょん](https://github.com/mjonss)の照合順序と異なる場合、パーティションが誤ってプルーニングされる問題を修正します。
    -   ホスト[#33061](https://github.com/pingcap/tidb/issues/33061) @ [モルゴ](https://github.com/morgo)に大文字がある場合、 `SET ROLE`付与されたロールと一致しない問題を修正
    -   `auto_increment`の列を削除できない問題を修正[#34891](https://github.com/pingcap/tidb/issues/34891) @ [定義2014](https://github.com/Defined2014)
    -   `SHOW CONFIG`に削除された一部の設定項目が表示される問題を修正[#34867](https://github.com/pingcap/tidb/issues/34867) @ [モルゴ](https://github.com/morgo)
    -   `SHOW DATABASES LIKE …`では大文字と小文字が区別される問題を修正[#34766](https://github.com/pingcap/tidb/issues/34766) @ [e1ijah1](https://github.com/e1ijah1)
    -   `SHOW TABLE STATUS LIKE ...`では大文字と小文字が区別される問題を修正[#7518](https://github.com/pingcap/tidb/issues/7518) @ [リクズン](https://github.com/likzn)
    -   `max-index-length`が非厳密モード[#34931](https://github.com/pingcap/tidb/issues/34931) @ [e1ijah1](https://github.com/e1ijah1)でもエラーを報告する問題を修正
    -   `ALTER COLUMN ... DROP DEFAULT`が動作しない問題を修正[#35018](https://github.com/pingcap/tidb/issues/35018) @ [定義2014](https://github.com/Defined2014)
    -   テーブルを作成するときに、デフォルト値と列の型が一致せず、自動的に修正されない問題を修正します[#34881](https://github.com/pingcap/tidb/issues/34881) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)
    -   `DROP USER` [#35059](https://github.com/pingcap/tidb/issues/35059) @ [ルクワンチャオ](https://github.com/lcwangchao)を実行した後、 `mysql.columns_priv`テーブルのデータが同期的に削除されない問題を修正します。
    -   一部のシステム[#35205](https://github.com/pingcap/tidb/issues/35205) @ [タンジェンタ](https://github.com/tangenta)のスキーマ内でのテーブルの作成を禁止することで、DDL ジャムの問題を修正しました。
    -   パーティション テーブルのクエリを実行すると、場合によっては「インデックスが範囲外」および「未使用のインデックス」エラーが報告される場合がある問題を修正します[#35181](https://github.com/pingcap/tidb/issues/35181) @ [むじょん](https://github.com/mjonss)
    -   `INTERVAL expr unit + expr`がエラー[#30253](https://github.com/pingcap/tidb/issues/30253) @ [むじょん](https://github.com/mjonss)を報告する可能性がある問題を修正
    -   トランザクション[#35644](https://github.com/pingcap/tidb/issues/35644) @ [djshow832](https://github.com/djshow832)で一時テーブル作成後に一時テーブルが見つからないバグを修正
    -   照合順序を`ENUM`カラム[#31637](https://github.com/pingcap/tidb/issues/31637) @ [wjhuang2016](https://github.com/wjhuang2016)に設定するときに発生するpanicの問題を修正します。
    -   1 つの PD ノードがダウンすると、他の PD ノード[#35708](https://github.com/pingcap/tidb/issues/35708) @ [タンジェンタ](https://github.com/tangenta)が再試行されないために`information_schema.TIKV_REGION_STATUS`のクエリが失敗する問題を修正します。
    -   `SHOW CREATE TABLE …` `SET character_set_results = GBK` [#31338](https://github.com/pingcap/tidb/issues/31338) @ [タンジェンタ](https://github.com/tangenta)以降のセットまたは`ENUM`列が正しく表示されない問題を修正
    -   システム変数`tidb_log_file_max_days`および`tidb_config` [#35190](https://github.com/pingcap/tidb/issues/35190) @ [モルゴ](https://github.com/morgo)の不正なスコープを修正します。
    -   `SHOW CREATE TABLE`の出力が MySQL の`ENUM`または`SET`列[#36317](https://github.com/pingcap/tidb/issues/36317) @ [定義2014](https://github.com/Defined2014)と互換性がない問題を修正
    -   テーブル作成時の`LONG BYTE`カラムの動作が MySQL [#36239](https://github.com/pingcap/tidb/issues/36239) @ [定義2014](https://github.com/Defined2014)と互換性がない問題を修正
    -   `auto_increment = x`が一時テーブル[#36224](https://github.com/pingcap/tidb/issues/36224) @ [djshow832](https://github.com/djshow832)に反映されない問題を修正
    -   列を同時に変更するときの間違ったデフォルト値を修正[#35846](https://github.com/pingcap/tidb/issues/35846) @ [wjhuang2016](https://github.com/wjhuang2016)
    -   可用性を向上させるために、異常な TiKV ノードへのリクエストの送信を回避します[#34906](https://github.com/pingcap/tidb/issues/34906) @ [スティックナーフ](https://github.com/sticnarf)
    -   LOAD DATA ステートメント[#35198](https://github.com/pingcap/tidb/issues/35198) @ [SpadeA-Tang](https://github.com/SpadeA-Tang)で列リストが機能しない問題を修正します。
    -   一部のシナリオで、悲観的ロックが非一意のセカンダリ インデックス[#36235](https://github.com/pingcap/tidb/issues/36235) @ [エキシウム](https://github.com/ekexium)に誤って追加される問題を修正します。

-   TiKV

    -   悲観的トランザクション[#11612](https://github.com/tikv/tikv/issues/11612) @ [スティックナーフ](https://github.com/sticnarf)で`WriteConflict`エラーの報告を回避する
    -   非同期コミットが有効になっている場合、悲観的トランザクションで発生する可能性のある重複コミット レコードを修正[#12615](https://github.com/tikv/tikv/issues/12615) @ [スティックナーフ](https://github.com/sticnarf)
    -   `storage.api-version`を`1`から`2` [#12600](https://github.com/tikv/tikv/issues/12600) @ [ピンギュ](https://github.com/pingyu)に変更すると TiKV がパニックになる問題を修正
    -   TiKV と PD [#12518](https://github.com/tikv/tikv/issues/12518) @ [5kbps](https://github.com/5kbpers)の間の一貫性のないリージョンサイズ構成の問題を修正
    -   TiKV が PD クライアント[#12506](https://github.com/tikv/tikv/issues/12506) 、 [#12827](https://github.com/tikv/tikv/issues/12827) @ [コナー1996](https://github.com/Connor1996)に再接続し続ける問題を修正します。
    -   空の文字列[#12673](https://github.com/tikv/tikv/issues/12673) @ [wshwsh12](https://github.com/wshwsh12)の型変換を実行すると TiKV がパニックになる問題を修正
    -   `DATETIME`値に小数および`Z` [#12739](https://github.com/tikv/tikv/issues/12739) @ [ゲンリキ](https://github.com/gengliqi)が含まれる場合に発生する時刻解析エラーの問題を修正しました。
    -   Apply オペレーターによって TiKV RocksDB に書き込まれるパフォーマンス コンテキストが粗粒度[#11044](https://github.com/tikv/tikv/issues/11044) @ [リククスサシネーター](https://github.com/LykxSassinator)であるという問題を修正します。
    -   [バックアップ](/tikv-configuration-file.md#backup) / [輸入](/tikv-configuration-file.md#import) / [CDC](/tikv-configuration-file.md#cdc)の設定が無効な場合に TiKV が起動できない問題を修正[#12771](https://github.com/tikv/tikv/issues/12771) @ [3ポインター](https://github.com/3pointer)
    -   ピアの分割と破棄が同時に行われるときに発生する可能性があるpanicの問題を修正[#12825](https://github.com/tikv/tikv/issues/12825) @ [ビジージェイ](https://github.com/BusyJay)
    -   リージョンマージ プロセス[#12663](https://github.com/tikv/tikv/issues/12663) @ [ビジージェイ](https://github.com/BusyJay)でソース ピアがスナップショットによってログを追いつくときに発生する可能性があるpanicの問題を修正します。
    -   `max_sample_size`が`0` [#11192](https://github.com/tikv/tikv/issues/11192) @ [リククスサシネーター](https://github.com/LykxSassinator)に設定されている場合に統計を分析することによって引き起こされるpanicの問題を修正
    -   Raft Engineが有効になっている場合に暗号化キーがクリーンアップされない問題を修正[#12890](https://github.com/tikv/tikv/issues/12890) @ [タボキー](https://github.com/tabokie)
    -   `get_valid_int_prefix`機能がTiDBと互換性がない問題を修正。たとえば、 `FLOAT`タイプが誤って`INT` [#13045](https://github.com/tikv/tikv/issues/13045) @ [グオシャオゲ](https://github.com/guo-shaoge)に変換されました。
    -   新しいリージョンのコミット ログ期間が長すぎるため、QPS が[#13077](https://github.com/tikv/tikv/issues/13077) @ [コナー1996](https://github.com/Connor1996)低下する問題を修正します。
    -   リージョンハートビートが中断された後、PD が TiKV に再接続しない問題を修正[#12934](https://github.com/tikv/tikv/issues/12934) @ [バッファフライ](https://github.com/bufferflies)

-   ツール

    -   バックアップと復元 (BR)

        -   レート制限バックアップ タスク[#31722](https://github.com/pingcap/tidb/issues/31722) @ [モクイシュル28](https://github.com/MoCuishle28)の終了後にBR がレート制限をリセットしない問題を修正します。

## 貢献者 {#contributors}

TiDB コミュニティの以下の貢献者に感謝いたします。

-   [e1ijah1](https://github.com/e1ijah1)
-   [プラジュワルボルカール](https://github.com/PrajwalBorkar)
-   [リクズン](https://github.com/likzn)
-   [ラーハルク789](https://github.com/rahulk789)
-   [ウイルスディフェンダー](https://github.com/virusdefender)
-   [ジョイセ06](https://github.com/joycse06)
-   [モルゴ](https://github.com/morgo)
-   [ixuh12](https://github.com/ixuh12)
-   [ブラックティア23](https://github.com/blacktear23)
-   [ジョンハ×7](https://github.com/johnhaxx7)
-   [ゴーギム1](https://github.com/GoGim1)
-   [レンバオシュオ](https://github.com/renbaoshuo)
-   [ジャオリ](https://github.com/Zheaoli)
-   [ファンレンフー](https://github.com/fanrenhoo)
-   [ニュウェルキン](https://github.com/njuwelkin)
-   [ウィリービーバー](https://github.com/wirybeaver)
-   [おいコン](https://github.com/hey-kong)
-   [ファティレイ](https://github.com/fatelei)
-   [イーストフィッシャー](https://github.com/eastfisher) : 初めて投稿する人
-   [ジュネゼー](https://github.com/Juneezee) : 初めて投稿する人
