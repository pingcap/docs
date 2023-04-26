---
title: TiDB 6.2.0 Release Notes
---

# TiDB 6.2.0 リリースノート {#tidb-6-2-0-release-notes}

発売日：2022年8月23日

TiDB バージョン: 6.2.0-DMR

> **ノート：**
>
> TiDB 6.2.0-DMR のドキュメントは[アーカイブ済み](https://docs-archive.pingcap.com/tidb/v6.2/)です。 PingCAP では、 [最新の LTS バージョン](https://docs.pingcap.com/tidb/stable)の TiDB データベースを使用することをお勧めします。

v6.2.0-DMR の主な新機能と改善点は次のとおりです。

-   TiDB ダッシュボードは[ビジュアル実行計画](/dashboard/dashboard-slow-query.md#visual-execution-plans)をサポートしており、実行計画をより直感的に表示できます。
-   TiDB ダッシュボードに[モニタリングページ](/dashboard/dashboard-monitoring.md)を追加して、パフォーマンス分析とチューニングをより効率的にします。
-   TiDB 機能の[ビューをロック](/information-schema/information-schema-data-lock-waits.md)は、楽観的トランザクションの待機情報の表示をサポートし、ロック競合の迅速な特定を容易にします。
-   TiFlash は[新しいバージョンのstorage形式](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)をサポートし、安定性とパフォーマンスを向上させます。
-   [ファイングレイン シャッフル機能](/system-variables.md#tiflash_fine_grained_shuffle_batch_size-new-in-v620)指定すると、複数のスレッドでウィンドウ関数を並列実行できます。
-   A [新しい並行 DDL フレームワーク](/system-variables.md#tidb_enable_concurrent_ddl-new-in-v620) : ブロックされる DDL ステートメントが少なくなり、実行効率が高くなります。
-   TiKV は[CPU使用率の自動チューニング](/tikv-configuration-file.md#background-quota-limiter)をサポートしているため、安定した効率的なデータベース操作が保証されます。
-   [ポイントインタイムリカバリ (PITR)](/br/backup-and-restore-overview.md)は、TiDB クラスターのスナップショットを過去の任意の時点から新しいクラスターに復元するために導入されました。
-   TiDB Lightning は、クラスター レベルではなく、物理インポート モードで[テーブルレベルでのスケジューリングの一時停止](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#pause-scheduling-on-the-table-level)をサポートします。
-   BR は[ユーザーおよび権限データの復元](/br/br-snapshot-guide.md#restore-tables-in-the-mysql-schema)をサポートし、バックアップと復元をよりスムーズにします。
-   TiCDC は[特定のタイプの DDL イベントのフィルタリング](/ticdc/ticdc-filter.md)をサポートすることで、より多くのデータ レプリケーション シナリオを解き放ちます。
-   トランザクション内のロールバック ポイントを柔軟に制御できる[`SAVEPOINT`メカニズム](/sql-statements/sql-statement-savepoint.md)がサポートされています。
-   TiDB は[1 つの`ALTER TABLE`ステートメントのみで複数の列またはインデックスを追加、削除、および変更する](/sql-statements/sql-statement-alter-table.md)をサポートしています。
-   [クラスタ間の RawKV レプリケーション](/tikv-configuration-file.md#api-version-new-in-v610)がサポートされるようになりました。

## 新機能 {#new-features}

### SQL {#sql}

-   物理データ圧縮機能は GA です

    TiFlashバックエンドは、特定の条件に基づいて物理データを自動的に圧縮し、不要なデータのバックログを削減し、データstorage構造を最適化します。

    データ圧縮が自動的にトリガーされる前に、 TiFlashテーブルに一定量の役に立たないデータが存在することがよくあります。この機能を使用すると、適切なタイミングを選択して SQL ステートメントを手動で実行し、 TiFlash内の物理データを即座に圧縮できるため、storageスペースの使用量が削減され、クエリのパフォーマンスが向上します。この機能は TiDB v6.1 で実験的であり、現在 TiDB v6.2.0 で一般提供 (GA) されています。

    [ユーザー文書](/sql-statements/sql-statement-alter-table-compact.md#alter-table--compact) [#4145](https://github.com/pingcap/tiflash/issues/4145) @ [そよ風](https://github.com/breezewish)

### 可観測性 {#observability}

-   PD から TiDB ダッシュボードを分割する

    TiDB ダッシュボードは、PD から監視ノードに移動されます。これにより、PD に対する TiDB ダッシュボードの影響が軽減され、PD がより安定します。

    @ [ホークソンジー](https://github.com/Hawkson-jee)

-   TiDB ダッシュボードに監視ページを追加

    新しい [監視] ページには、パフォーマンス チューニングに必要な主要な指標が表示されます。これに基づいて、 [データベース時間によるパフォーマンス チューニング](/performance-tuning-methods.md)を参照してパフォーマンスを分析および調整できます。

    具体的には、グローバルおよびトップダウンの観点からユーザー応答時間とデータベース時間を分析して、ユーザー応答時間のボトルネックがデータベースの問題によって引き起こされているかどうかを確認できます。ボトルネックがデータベースにある場合は、データベース時間の概要と SQLレイテンシーの内訳を使用して、ボトルネックを特定し、パフォーマンスを調整できます。

    [ユーザー文書](/dashboard/dashboard-monitoring.md) [#1381](https://github.com/pingcap/tidb-dashboard/issues/1381) @ [YiniXu9506](https://github.com/YiniXu9506)

-   TiDB ダッシュボードは視覚的な実行計画をサポートしています

    TiDB ダッシュボードは、SQL ステートメントと監視ページを通じて、視覚的な実行計画と基本的な診断サービスを提供します。この機能は、クエリ プランの各ステップを識別するための新鮮な新しい視点を提供します。したがって、クエリ実行プランのすべてのトレースをより直感的に学習できます。

    この機能は、複雑で大規模なクエリの実行を学習しようとしている場合に特に役立ちます。一方、各クエリ実行プランについて、TiDB ダッシュボードは実行の詳細を自動的に分析し、潜在的な問題を特定し、特定のクエリ プランの実行に必要な時間を短縮するための最適化の提案を提供します。

    [ユーザー文書](/dashboard/dashboard-slow-query.md#visual-execution-plans) [#1224](https://github.com/pingcap/tidb-dashboard/issues/1224) @ [時間と運命](https://github.com/time-and-fate)

-   Lock ビュー は、楽観的トランザクションの待機情報の表示をサポートします

    ロックの競合が多すぎると、重大なパフォーマンスの問題が発生する可能性があり、ロックの競合を検出することは、このような問題をトラブルシューティングするために必要な方法です。 v6.2.0 より前の TiDB は、 `INFORMATION_SCHEMA.DATA_LOCK_WAITS`システム ビューを使用してロックの競合関係を表示することをサポートしていましたが、楽観的トランザクションの待機情報は表示しません。 TiDB v6.2.0 は`DATA_LOCK_WAITS`ビューを拡張し、悲観的ロックによってブロックされた楽観的トランザクションをビューにリストします。この機能は、ユーザーがロックの競合を迅速に検出するのに役立ち、アプリケーションを改善するための基礎を提供することで、ロックの競合の頻度を減らし、全体的なパフォーマンスを向上させます。

    [ユーザー文書](/information-schema/information-schema-data-lock-waits.md) [#34609](https://github.com/pingcap/tidb/issues/34609) @ [ロングファンソング](https://github.com/longfangsong)

### パフォーマンス {#performance}

-   `LEADING`オプティマイザ ヒントを改善して、外部結合の順序付けをサポートする

    v6.1.0 では、オプティマイザー ヒント`LEADING`が導入され、テーブルの結合順序が変更されました。ただし、このヒントは、外部結合を含むクエリには適用できませんでした。詳細については、 [`LEADING`文書](/optimizer-hints.md#leadingt1_name--tl_name-)を参照してください。 v6.2.0 では、TiDB はこの制限を解除します。外部結合を含むクエリでは、このヒントを使用してテーブルの結合順序を指定し、SQL 実行のパフォーマンスを向上させ、実行計画の突然の変更を回避できるようになりました。

    [ユーザー文書](/optimizer-hints.md#leadingt1_name--tl_name-) [#29932](https://github.com/pingcap/tidb/issues/29932) @ [思い出す](https://github.com/Reminiscent)

-   `EXISTS`クエリのパフォーマンスを向上させるために、新しいオプティマイザ`SEMI_JOIN_REWRITE`を追加します

    一部のシナリオでは、 `EXISTS`のクエリは最適な実行プランを持つことができず、長時間実行される可能性があります。 v6.2.0 では、オプティマイザーはこのようなシナリオの書き換えルールを追加し、クエリで`SEMI_JOIN_REWRITE`を使用してオプティマイザーに強制的にクエリを書き換えさせ、クエリのパフォーマンスを向上させることができます。

    [ユーザー文書](/optimizer-hints.md#semi_join_rewrite) [#35323](https://github.com/pingcap/tidb/issues/35323) @ [ウィノロス](https://github.com/winoros)

-   新しいオプティマイザー ヒント`MERGE`を追加して、分析クエリのパフォーマンスを向上させます

    共通テーブル式 (CTE) は、クエリ ロジックを簡素化する効果的な方法です。複雑なクエリを記述するために広く使用されています。 v6.2.0 より前では、 TiFlash環境で CTE を自動的に拡張することはできず、MPP の実行効率がある程度制限されていました。 v6.2.0 では、MySQL 互換のオプティマイザー ヒント`MERGE`が導入されました。このヒントにより、オプティマイザーは CTE インラインを展開できるようになり、CTE クエリ結果のコンシューマーがTiFlashでクエリを同時に実行できるようになり、一部の分析クエリのパフォーマンスが向上します。

    [ユーザー文書](/optimizer-hints.md#merge) [#36122](https://github.com/pingcap/tidb/issues/36122) @ [dayicklp](https://github.com/dayicklp)

-   一部の分析シナリオで集計操作のパフォーマンスを最適化する

    TiFlashを使用して OLAP シナリオで列に対して集計操作を実行する場合、集計された列の不均一な分散により深刻なデータ スキューが存在し、集計された列に多くの異なる値がある場合、列に対する`COUNT(DISTINCT)`クエリの実行効率は低い。 v6.2.0 では、1 つの列に対する`COUNT(DISTINCT)`クエリのパフォーマンスを向上させるために、新しい書き換えルールが導入されました。

    [ユーザー文書](/system-variables.md#tidb_opt_skew_distinct_agg-new-in-v620) [#36169](https://github.com/pingcap/tidb/issues/36169) @ [fixdb](https://github.com/fixdb)

-   TiDB は同時 DDL 操作をサポートします

    TiDB v6.2.0 では、新しいコンカレント DDL フレームワークが導入されました。これにより、DDL ステートメントを異なるテーブル オブジェクトで同時に実行できるようになり、DDL 操作が他のテーブルの DDL 操作によってブロックされるという問題が修正されます。さらに、TiDB は、複数のテーブルにインデックスを追加したり、列の型を変更したりするときに、DDL の同時実行をサポートします。これにより、DDL 実行の効率が向上します。

    [ユーザー文書](/system-variables.md#tidb_enable_concurrent_ddl-new-in-v620) [#32031](https://github.com/pingcap/tidb/issues/32031) @ [wjhuang2016](https://github.com/wjhuang2016)

-   オプティマイザーは文字列一致の推定を強化します

    文字列一致のシナリオでは、オプティマイザが行数を正確に見積もることができない場合、最適な実行計画の生成に影響します。たとえば、条件は`like '%xyz'`であるか、正規表現`regex ()`を使用しています。このようなシナリオでの推定精度を向上させるために、TiDB v6.2.0 では推定方法が強化されています。新しい方法は、統計の TopN 情報とシステム変数を組み合わせて精度を向上させ、一致の選択性を手動で変更できるようにすることで、SQL のパフォーマンスを向上させます。

    [ユーザー文書](/system-variables.md#tidb_default_string_match_selectivity-new-in-v620) [#36209](https://github.com/pingcap/tidb/issues/36209) @ [時間と運命](https://github.com/time-and-fate)

-   TiFlashにプッシュされたウィンドウ関数は、複数のスレッドで実行できます。

    詳細なシャッフル機能を有効にすると、ウィンドウ関数を単一のスレッドではなく、複数のスレッドで実行できます。この機能により、ユーザーの動作を変更することなく、クエリの応答時間が大幅に短縮されます。変数の値を調整することで、シャッフルの粒度を制御できます。

    [ユーザー文書](/system-variables.md#tiflash_fine_grained_shuffle_batch_size-new-in-v620) [#4631](https://github.com/pingcap/tiflash/issues/4631) @ [グオシャオゲ](https://github.com/guo-shaoge)

-   TiFlash は新しいバージョンのstorage形式をサポートしています

    新しいstorage形式は、同時実行性が高くワークロードが重いシナリオで GC によって引き起こされる高い CPU 使用率を軽減します。これにより、バックグラウンド タスクの IO トラフィックが大幅に削減され、高い同時実行性と重いワークロードの下での安定性が向上します。同時に、スペースの増幅とディスクの無駄を大幅に削減できます。

    TiDB v6.2.0 では、データはデフォルトで新しいstorage形式で保存されます。 TiFlashが以前のバージョンから v6.2.0 にアップグレードされた場合、以前のTiFlashバージョンは新しいstorage形式を認識できないため、 TiFlashでインプレース ダウングレードを実行できないことに注意してください。

    TiFlashのアップグレードの詳細については、 [TiFlash v6.2.0 アップグレード ガイド](/tiflash-620-upgrade-guide.md)を参照してください。

    [ユーザー文書](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file) [#3594](https://github.com/pingcap/tiflash/issues/3594) @ [ジェイソン・ファン](https://github.com/JaySon-Huang) @ [リデジュ](https://github.com/lidezhu) @ [ジアキゾー](https://github.com/jiaqizho)

-   TiFlash は、複数の同時実行シナリオでデータ スキャンのパフォーマンスを最適化します (実験的)

    TiFlash は、同じデータの読み取り操作をマージすることにより、同じデータの重複読み取りを減らし、複数の同時タスクの場合のリソース オーバーヘッドを最適化して、データ スキャンのパフォーマンスを向上させます。同じデータが複数の同時タスクに関係している場合、同じデータを各タスクで個別に読み取る必要がある状況や、同じデータを同時に複数回読み取る必要がある状況を回避します。

    [ユーザー文書](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file) [#5376](https://github.com/pingcap/tiflash/issues/5376) @ [リン・ジンヘ](https://github.com/JinheLin)

-   TiFlash はデータ スキャン用の FastScan を追加し、データの一貫性を犠牲にして読み書き速度を向上させます (実験的)。

    TiDB は v6.2.0 で FastScan を導入しています。一貫性チェックのスキップをサポートして、速度を大幅に向上させます。 FastScan は、オフライン分析タスクなど、データの高い精度と一貫性を必要としないシナリオに適しています。以前は、データの一貫性を確保するために、 TiFlash はデータ スキャン プロセス中にデータの一貫性チェックを実行して、複数の異なるバージョンから必要なデータを見つける必要がありました。

    以前のバージョンから TiDB v6.2.0 にアップグレードする場合、FastScan はデフォルトですべてのテーブルに対して有効になっていないため、データの一貫性が保証されます。各テーブルの FastScan を個別に有効にすることができます。テーブルが TiDB v6.2.0 で FastScan に設定されている場合、下位バージョンにダウングレードすると無効になりますが、これは通常のデータ読み取りには影響しません。この場合は、強整合性読み取りと同等です。

    [ユーザー文書](/develop/dev-guide-use-fastscan.md) [#5252](https://github.com/pingcap/tiflash/issues/5252) @ [ホンユニャン](https://github.com/hongyunyan)

### 安定性 {#stability}

-   TiKV は、CPU 使用率の自動調整をサポートしています (実験的)。

    データベースには通常、内部操作を実行するためのバックグラウンド プロセスがあります。統計情報を収集して、パフォーマンスの問題を特定し、より適切な実行計画を生成し、データベースの安定性とパフォーマンスを向上させることができます。しかし、より効率的に情報を収集する方法と、日常の使用に影響を与えずにバックグラウンド操作とフォアグラウンド操作のリソース オーバーヘッドのバランスをとる方法は、データベース業界の頭痛の種の 1 つです。

    v6.2.0 以降、TiDB は、TiKV 構成ファイルを使用したバックグラウンド リクエストの CPU 使用率の設定をサポートします。これにより、TiKV での統計の自動収集などのバックグラウンド操作の CPU 使用率を制限し、バックグラウンド操作によるユーザー操作のリソース プリエンプションを回避します。極端な場合。これにより、データベースの操作が安定して効率的になります。

    同時に、TiDB は CPU 使用率の自動調整もサポートしています。次に、TiKV は、インスタンスの CPU 使用率に応じて、バックグラウンド リクエストによって占有される CPU リソースを適応的に調整します。この機能はデフォルトで無効になっています。

    [ユーザー文書](/tikv-configuration-file.md#background-quota-limiter) [#12503](https://github.com/tikv/tikv/issues/12503) @ [ボーンチェンジャー](https://github.com/BornChanger)

### 使いやすさ {#ease-of-use}

-   TiKV は、コマンドライン フラグを使用した詳細な構成情報の一覧表示をサポートしています

    TiKV 構成ファイルを使用して、TiKV インスタンスを管理できます。ただし、長時間実行され、別のユーザーによって管理されているインスタンスの場合、どの構成項目が変更され、デフォルト値が何であるかを知ることは困難です。これにより、クラスターをアップグレードしたりデータを移行したりするときに混乱が生じる可能性があります。 TiDB v6.2.0 以降、tikv-server は、すべての TiKV 構成項目のデフォルト値と現在の値を一覧表示する新しいコマンドライン フラグ[`—-config-info`](/command-line-flags-for-tikv-configuration.md#--config-info-format)をサポートし、ユーザーが TiKV プロセスの起動パラメーターをすばやく確認できるようにし、使いやすさを向上させます。

    [ユーザー文書](/command-line-flags-for-tikv-configuration.md#--config-info-format) [#12492](https://github.com/tikv/tikv/issues/12492) @ [栄光](https://github.com/glorv)

### MySQL の互換性 {#mysql-compatibility}

-   TiDB は、単一の`ALTER TABLE`ステートメントで複数の列またはインデックスを変更することをサポートしています

    v6.2.0 より前では、TiDB は単一の DDL 変更のみをサポートしているため、異種データベースを移行するときに互換性のない DDL 操作が発生し、複雑な DDL ステートメントを TiDB でサポートされている複数の単純な DDL ステートメントに変更するには、余分な労力が必要です。さらに、一部のユーザーは ORM フレームワークに依存して SQL でアセンブリを作成するため、SQL の非互換性が発生します。 v6.2.0 以降、TiDB は単一の SQL ステートメントで複数のスキーマ オブジェクトを変更することをサポートしています。これは、ユーザーが SQL を実装するのに便利で、使いやすさを向上させます。

    [ユーザー文書](/sql-statements/sql-statement-alter-table.md) [#14766](https://github.com/pingcap/tidb/issues/14766) @ [接線](https://github.com/tangenta)

-   トランザクションでのセーブポイントの設定をサポート

    トランザクションは、データベースがACIDプロパティを保証する一連の連続した操作の論理的な集合です。一部の複雑なアプリケーション シナリオでは、トランザクション内の多くの操作を管理する必要があり、トランザクション内の一部の操作をロールバックする必要がある場合があります。 「セーブポイント」は、トランザクションの内部実装のための命名可能なメカニズムです。このメカニズムにより、トランザクション内のロールバック ポイントを柔軟に制御できるため、より複雑なトランザクションを管理し、多様なアプリケーションをより自由に設計できます。

    [ユーザー文書](/sql-statements/sql-statement-savepoint.md) [#6840](https://github.com/pingcap/tidb/issues/6840) @ [クレイジーcs520](https://github.com/crazycs520)

### データ移行 {#data-migration}

-   BR は、ユーザーおよび権限データの復元をサポートします

    BR は、通常の復元を実行するときに、ユーザーおよび権限データの復元をサポートします。ユーザーおよび権限データを復元するために、追加の復元計画は必要ありません。この機能を有効にするには、 BRを使用してデータを復元するときに`--with-sys-table`パラメーターを指定します。

    [ユーザー文書](/br/br-snapshot-guide.md#restore-tables-in-the-mysql-schema) [#35395](https://github.com/pingcap/tidb/issues/35395) @ [D3ハンター](https://github.com/D3Hunter)

-   ログとスナップショットのバックアップと復元に基づくポイントインタイム リカバリ (PITR) をサポート

    PITR は、ログとスナップショットのバックアップと復元に基づいて実装されます。これにより、履歴の任意の時点でのクラスターのスナップショットを新しいクラスターに復元できます。この機能は、次のニーズを満たします。

    -   ディザスタ リカバリの RPO を 20 分未満に短縮します。
    -   たとえば、エラー イベントの前にデータをロールバックすることによって、アプリケーションからの誤った書き込みのケースを処理します。
    -   履歴データの監査を実施し、法規制の要件を満たします。

    この機能には使用上の制限があります。詳細については、ユーザードキュメントを参照してください。

    [ユーザー文書](/br/backup-and-restore-overview.md) [#29501](https://github.com/pingcap/tidb/issues/29501) @ [ジョッカウ](https://github.com/joccau)

-   DM は継続的なデータ検証をサポートしています (実験的)

    継続的なデータ検証を使用して、データ移行中にアップストリームのbinlogとダウンストリームに書き込まれたデータを継続的に比較します。バリデーターは、不整合なデータや欠落したレコードなどのデータ例外を識別します。

    この機能は、一般的な完全なデータ検証スキームでの検証の遅延と過度のリソース消費の問題を解決します。

    [ユーザー文書](/dm/dm-continuous-data-validation.md) [#4426](https://github.com/pingcap/tiflow/issues/4426) @ [D3ハンター](https://github.com/D3Hunter) @ [ぶちゅとでごう](https://github.com/buchuitoudegou)

-   Amazon S3 バケットのリージョンを自動的に識別する

    データ移行タスクは、Amazon S3 バケットのリージョンを自動的に識別できます。 region パラメーターを明示的に渡す必要はありません。

    [#34275](https://github.com/pingcap/tidb/issues/34275) @ [WangLe1321](https://github.com/WangLe1321)

-   TiDB Lightningのディスク クォータの構成をサポート (実験的)

    TiDB Lightning が物理インポート モード (backend=&#39;local&#39;) でデータをインポートする場合、sorted-kv-dir にはソース データを格納するのに十分なスペースが必要です。ディスク容量が不足していると、インポート タスクが失敗する可能性があります。新しい`disk_quota`構成を使用して、 TiDB Lightningが使用するディスク容量の合計を制限できるようになりました。これにより、sorted-kv-dir に十分なstorage容量がない場合でも、インポート タスクを正常に完了することができます。

    [ユーザー文書](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#configure-disk-quota-new-in-v620) [#446](https://github.com/pingcap/tidb-lightning/issues/446) @ [ぶちゅとでごう](https://github.com/buchuitoudegou)

-   TiDB Lightning は、物理インポート モードでの本番クラスターへのデータのインポートをサポートします

    以前は、 TiDB Lightning (backend=&#39;local&#39;) の物理インポート モードがターゲット クラスターに大きな影響を与えていました。たとえば、移行中、PD グローバル スケジューリングは一時停止されます。したがって、以前の物理インポート モードは、初期データ インポートにのみ適しています。

    TiDB Lightning は、既存の物理インポート モードを改善します。テーブルのスケジューリングを一時停止できるようにすることで、クラスター レベルからテーブル レベルへのインポートの影響が軽減されます。つまり、インポートされていないテーブルを読み書きできます。

    この機能を手動で構成する必要はありません。 TiDB クラスターが v6.1.0 以降のバージョンで、 TiDB Lightningが v6.2.0 以降のバージョンの場合、新しい物理インポート モードが自動的に有効になります。

    [ユーザー文書](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#pause-scheduling-on-the-table-level) [#35148](https://github.com/pingcap/tidb/issues/35148) @ [ゴズスキー](https://github.com/gozssky)

-   [TiDB Lightningのユーザー ドキュメント](/tidb-lightning/tidb-lightning-overview.md)リファクタリングして、その構造をより合理的かつ明確にします。 「バックエンド」の用語も、新規ユーザーの理解の障壁を下げるために変更されています。

    -   「ローカル バックエンド」を「物理インポート モード」に置き換えます。
    -   「tidb バックエンド」を「論理インポート モード」に置き換えます。

### TiDB データ共有サブスクリプション {#tidb-data-share-subscription}

-   クラスター間の RawKV レプリケーションをサポート (実験的)

    RawKV のデータ変更をサブスクライブし、新しいコンポーネントTiKV-CDC を使用してデータ変更を下流の TiKV クラスターにリアルタイムで複製することをサポートします。これにより、クラスター間の複製が可能になります。

    [ユーザー文書](/tikv-configuration-file.md#api-version-new-in-v610) [#11965](https://github.com/tikv/tikv/issues/11965) @ [ピンギュ](https://github.com/pingyu)

-   DDL および DML イベントのフィルタリングをサポート

    特別な場合に、増分データ変更ログのフィルター規則を設定したい場合があります。たとえば、DROP TABLE などのリスクの高い DDL イベントをフィルタリングします。 v6.2.0 以降、TiCDC は、指定されたタイプの DDL イベントのフィルタリングと、SQL 式に基づく DML イベントのフィルタリングをサポートしています。これにより、TiCDC はより多くのデータ レプリケーション シナリオに適用できるようになります。

    [ユーザー文書](/ticdc/ticdc-filter.md) [#6160](https://github.com/pingcap/tiflow/issues/6160) @ [アスドンメン](https://github.com/asddongmen)

## 互換性の変更 {#compatibility-changes}

### システム変数 {#system-variables}

| 変数名                                                                                                                     | タイプを変更 | 説明                                                                                                                                                                                                          |
| ----------------------------------------------------------------------------------------------------------------------- | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [tidb_enable_new_cost_interface](/system-variables.md#tidb_enable_new_cost_interface-new-in-v620)                       | 新規追加   | この変数は、 [リファクタリングされたコスト モデルの実装](/cost-model.md#cost-model-version-2)を有効にするかどうかを制御します。                                                                                                                        |
| [tidb_cost_model_version](/system-variables.md#tidb_cost_model_version-new-in-v620)                                     | 新規追加   | TiDB はコスト モデルを使用して、物理的な最適化中にインデックスと演算子を選択します。この変数は、コスト モデルのバージョンを選択するために使用されます。 TiDB v6.2.0 では、コスト モデル バージョン 2 が導入されました。これは、内部テストで以前のバージョンよりも正確です。                                                          |
| [tidb_enable_concurrent_ddl](/system-variables.md#tidb_enable_concurrent_ddl-new-in-v620)                               | 新規追加   | この変数は、TiDB が同時 DDL ステートメントを使用できるようにするかどうかを制御します。この変数を変更しないでください。この変数を無効にするリスクは不明であり、クラスターのメタデータが破損する可能性があります。                                                                                               |
| [tiflash_fine_grained_shuffle_stream_count](/system-variables.md#tiflash_fine_grained_shuffle_stream_count-new-in-v620) | 新規追加   | この変数は、ウィンドウ関数が実行のためにTiFlashにプッシュされるときのウィンドウ関数実行の同時実行レベルを制御します。                                                                                                                                              |
| [tiflash_fine_grained_shuffle_batch_size](/system-variables.md#tiflash_fine_grained_shuffle_batch_size-new-in-v620)     | 新規追加   | Fine Grained Shuffle が有効な場合、 TiFlashにプッシュ ダウンされたウィンドウ関数を並行して実行できます。この変数は、送信者によって送信されるデータのバッチ サイズを制御します。行の累積数がこの値を超えると、送信者はデータを送信します。                                                                        |
| [tidb_default_string_match_selectivity](/system-variables.md#tidb_default_string_match_selectivity-new-in-v620)         | 新規追加   | この変数は、行数を見積もるときのフィルタ条件で`like` 、 `rlike` 、および`regexp`関数のデフォルトの選択性を設定するために使用されます。この変数は、TopN を有効にしてこれらの関数を推定するかどうかも制御します。                                                                                      |
| [tidb_enable_analyze_snapshot](/system-variables.md#tidb_enable_analyze_snapshot-new-in-v620)                           | 新規追加   | この変数は、実行時に過去のデータを読み取るか最新のデータを読み取るかを制御します`ANALYZE` 。                                                                                                                                                         |
| [tidb_generate_binary_plan](/system-variables.md#tidb_generate_binary_plan-new-in-v620)                                 | 新規追加   | この変数は、スロー ログとステートメント サマリーでバイナリ エンコードされた実行プランを生成するかどうかを制御します。                                                                                                                                                |
| [tidb_opt_skew_distinct_agg](/system-variables.md#tidb_opt_skew_distinct_agg-new-in-v620)                               | 新規追加   | この変数は、オプティマイザが`DISTINCT`集約関数を2 レベルの集約関数に書き換えるかどうか ( `SELECT b, COUNT(DISTINCT a) FROM t GROUP BY b`を`SELECT b, COUNT(a) FROM (SELECT b, a FROM t GROUP BY b, a) t GROUP BY b`に書き換えるなど) を設定します。              |
| [tidb_enable_noop_variables](/system-variables.md#tidb_enable_noop_variables-new-in-v620)                               | 新規追加   | この変数は、 `SHOW [GLOBAL] VARIABLES`の結果に`noop`変数を表示するかどうかを制御します。                                                                                                                                                |
| [tidb_min_paging_size](/system-variables.md#tidb_min_paging_size-new-in-v620)                                           | 新規追加   | この変数は、コプロセッサーのページング要求プロセス中に行の最大数を設定するために使用されます。                                                                                                                                                             |
| [tidb_txn_commit_batch_size](/system-variables.md#tidb_txn_commit_batch_size-new-in-v620)                               | 新規追加   | この変数は、TiDB が TiKV に送信するトランザクション コミット リクエストのバッチ サイズを制御するために使用されます。                                                                                                                                           |
| tidb_enable_change_multi_schema                                                                                         | 削除しました | この変数は、1 つの`ALTER TABLE`ステートメントで複数の列またはインデックスを変更できるかどうかを制御するために使用されます。                                                                                                                                       |
| [tidb_enable_outer_join_reorder](/system-variables.md#tidb_enable_outer_join_reorder-new-in-v610)                       | 修正済み   | この変数は、TiDB の結合したテーブルの再配置アルゴリズムが Outer Join をサポートするかどうかを制御します。 v6.1.0 では、デフォルト値は`ON`です。これは、Join Reorder の Outer Join のサポートがデフォルトで有効になっていることを意味します。 v6.2.0 以降、デフォルト値は`OFF`です。これは、サポートがデフォルトで無効になっていることを意味します。 |

### コンフィグレーションファイルのパラメーター {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーション                                                                                                                | タイプを変更 | 説明                                                                                                          |
| -------------- | ------------------------------------------------------------------------------------------------------------------------- | ------ | ----------------------------------------------------------------------------------------------------------- |
| TiDB           | フィードバック確率                                                                                                                 | 削除しました | この構成は有効ではなくなり、推奨されません。                                                                                      |
| TiDB           | クエリ フィードバック制限                                                                                                             | 削除しました | この構成は有効ではなくなり、推奨されません。                                                                                      |
| TiKV           | [サーバー.simplify-metrics](/tikv-configuration-file.md#simplify-metrics-new-in-v620)                                         | 新規追加   | この構成は、返されたモニタリング メトリックを単純化するかどうかを指定します。                                                                     |
| TiKV           | [quota.background-cpu-time](/tikv-configuration-file.md#background-cpu-time-new-in-v620)                                  | 新規追加   | この構成は、TiKV バックグラウンドが読み取りおよび書き込み要求を処理するために使用する CPU リソースのソフト制限を指定します。                                         |
| TiKV           | [quota.background-write-bandwidth](/tikv-configuration-file.md#background-write-bandwidth-new-in-v620)                    | 新規追加   | この構成は、バックグラウンド トランザクションがデータを書き込む帯域幅のソフト リミットを指定します (現在は有効ではありません)。                                          |
| TiKV           | [quota.background-read-bandwidth](/tikv-configuration-file.md#background-read-bandwidth-new-in-v620)                      | 新規追加   | この構成は、バックグラウンド トランザクションとコプロセッサーがデータを読み取る帯域幅のソフト リミットを指定します (現在は有効ではありません)。                                  |
| TiKV           | [quota.enable-auto-tune](/tikv-configuration-file.md#enable-auto-tune-new-in-v620)                                        | 新規追加   | この構成では、クォータの自動調整を有効にするかどうかを指定します。この構成項目が有効になっている場合、TiKV は、TiKV インスタンスの負荷に基づいて、バックグラウンド リクエストのクォータを動的に調整します。 |
| TiKV           | rocksdb.enable-pipelined-commit                                                                                           | 削除しました | この構成は有効ではなくなりました。                                                                                           |
| TiKV           | gc-マージ-リライト                                                                                                               | 削除しました | この構成は有効ではなくなりました。                                                                                           |
| TiKV           | [ログバックアップを有効にします](/tikv-configuration-file.md#enable-new-in-v620)                                                         | 新規追加   | この構成は、TiKV でログ バックアップを有効にするかどうかを制御します。                                                                      |
| TiKV           | [log-backup.file-size-limit](/tikv-configuration-file.md#file-size-limit-new-in-v620)                                     | 新規追加   | この構成では、ログ バックアップ データのサイズ制限を指定します。この制限に達すると、データは自動的に外部storageにフラッシュされます。                                     |
| TiKV           | [log-backup.initial-scan-pending-memory-quota](/tikv-configuration-file.md#initial-scan-pending-memory-quota-new-in-v620) | 新規追加   | この構成は、インクリメンタル スキャン データの格納に使用されるキャッシュのクォータを指定します。                                                           |
| TiKV           | [log-backup.max-flush-interval](/tikv-configuration-file.md#max-flush-interval-new-in-v620)                               | 新規追加   | この構成では、ログ バックアップでバックアップ データを外部storageに書き込む最大間隔を指定します。                                                       |
| TiKV           | [log-backup.initial-scan-rate-limit](/tikv-configuration-file.md#initial-scan-rate-limit-new-in-v620)                     | 新規追加   | この構成では、ログ バックアップの増分データ スキャンでのスループットのレート制限を指定します。                                                            |
| TiKV           | [log-backup.num-threads](/tikv-configuration-file.md#num-threads-new-in-v620)                                             | 新規追加   | この構成は、ログ バックアップで使用されるスレッドの数を指定します。                                                                          |
| TiKV           | [ログバックアップ.一時パス](/tikv-configuration-file.md#temp-path-new-in-v620)                                                        | 新規追加   | この構成は、外部storageにフラッシュされる前にログ ファイルが書き込まれる一時パスを指定します。                                                         |
| PD             | replication-mode.dr-auto-sync.wait-async-timeout                                                                          | 削除しました | この構成は有効にならず、削除されます。                                                                                         |
| PD             | replication-mode.dr-auto-sync.wait-sync-timeout                                                                           | 削除しました | この構成は有効にならず、削除されます。                                                                                         |
| TiFlash        | [`storage.format_version`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                              | 修正済み   | デフォルト値の`format_version`は、v6.2.0 以降のバージョンのデフォルト形式である`4`に変更され、書き込み増幅とバックグラウンド タスクのリソース消費が削減されます。              |
| TiFlash        | [profile.default.dt_enable_read_thread](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                 | 新規追加   | この構成は、スレッド プールを使用してstorageエンジンからの読み取り要求を処理するかどうかを制御します。デフォルト値は`false`です。                                    |
| TiFlash        | [profile.default.dt_page_gc_threshold](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                  | 新規追加   | この構成は、PageStorage データ ファイル内の有効なデータの最小比率を指定します。                                                              |
| TiCDC          | [--overwrite-checkpoint-ts](/ticdc/ticdc-manage-changefeed.md#resume-a-replication-task)                                  | 新規追加   | この構成は、 `cdc cli changefeed resume`サブコマンドに追加されます。                                                            |
| TiCDC          | [--未確認](/ticdc/ticdc-manage-changefeed.md#resume-a-replication-task)                                                      | 新規追加   | この構成は、 `cdc cli changefeed resume`サブコマンドに追加されます。                                                            |
| DM             | [モード](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)                                      | 新規追加   | この構成はバリデータ パラメータです。オプションの値は`full` 、 `fast` 、および`none`です。デフォルト値は`none`で、データを検証しません。                          |
| DM             | [ワーカー数](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)                                    | 新規追加   | この構成はバリデーターのパラメーターであり、バックグラウンドでの検証ワーカーの数を指定します。デフォルト値は`4`です。                                                |
| DM             | [行エラー遅延](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)                                   | 新規追加   | この構成はバリデータ パラメータです。行が指定された時間内に検証されない場合、エラー行としてマークされます。デフォルト値は 30m で、これは 30 分を意味します。                         |
| TiDB Lightning | [tikv-importer.store-write-bwlimit](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)                  | 新規追加   | この構成は、 TiDB Lightning が各 TiKV ストアにデータを書き込むときの書き込み帯域幅を決定します。デフォルト値は`0`で、帯域幅が制限されていないことを示します。                 |
| TiDB Lightning | [tikv-importer.disk-quota](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#configure-disk-quota-new-in-v620) | 新規追加   | この設定により、 TiDB Lightningが使用するstorageスペースが制限されます。                                                             |

### その他 {#others}

-   TiFlash `format_version` `4`から`3`にダウングレードできません。詳細については、 [TiFlash v6.2.0 アップグレード ガイド](/tiflash-620-upgrade-guide.md)を参照してください。
-   v6.2.0 以降のバージョンでは、デフォルト値`false`の`dt_enable_logical_split`を維持し、それを`true`に変更しないことを強くお勧めします。詳細については、既知の問題[#5576](https://github.com/pingcap/tiflash/issues/5576)を参照してください。
-   バックアップ クラスタにTiFlashレプリカがある場合、PITR を実行した後、復元クラスタにはTiFlashレプリカのデータが含まれません。 TiFlashレプリカからデータを復元するには、 TiFlashレプリカを手動で構成する必要があります。 `exchange partition` DDL ステートメントを実行すると、PITR が失敗する可能性があります。アップストリーム データベースが TiDB Lightning の物理インポート モードを使用してデータをインポートする場合、ログ バックアップでデータをバックアップすることはできません。データのインポート後に完全バックアップを実行することをお勧めします。 PITR のその他の互換性の問題については、 [PITR の制限](/br/backup-and-restore-overview.md#before-you-use)を参照してください。
-   TiDB v6.2.0以降、データ復元時にパラメータ`--with-sys-table=true`を指定することで、 `mysql`スキーマにテーブルを復元できるようになりました。
-   `ALTER TABLE`ステートメントを実行して複数の列またはインデックスを追加、削除、または変更すると、TiDB は、同じ DDL ステートメントの変更に関係なく、ステートメントの実行前後のテーブルを比較して、テーブルの整合性をチェックします。一部のシナリオでは、DDL の実行順序は MySQL と完全には互換性がありません。
-   TiDBコンポーネントが v6.2.0 以降の場合、TiKVコンポーネントはv6.2.0 より前であってはなりません。
-   TiKV は[動的構成](/dynamic-config.md#modify-tikv-configuration-dynamically)をサポートする構成アイテム`split.region-cpu-overload-threshold-ratio`を追加します。
-   スロー クエリ ログ`information_schema.statements_summary`および`information_schema.slow_query` 、バイナリ形式でエンコードされた`binary_plan`または実行プランをエクスポートできます。
-   2 つの列が`SHOW TABLE ... REGIONS`ステートメントに追加されます: `SCHEDULING_CONSTRAINTS`と`SCHEDULING_STATE`は、SQL での配置のリージョンスケジュール制約と現在のスケジュール状態をそれぞれ示します。
-   TiDB v6.2.0 以降、RawKV のデータ変更を[TiKV-CDC](https://github.com/tikv/migration/tree/main/cdc)経由で取得できます。
-   トランザクションを指定されたセーブポイントにロールバックするために`ROLLBACK TO SAVEPOINT`が使用される場合、MySQL は指定されたセーブポイントの後にのみ保持されたロックを解放しますが、TiDB悲観的トランザクションでは、TiDB は指定されたセーブポイントの後に保持されたロックをすぐには解放しません。代わりに、トランザクションがコミットまたはロールバックされると、TiDB はすべてのロックを解放します。
-   TiDB v6.2.0 以降、 `SELECT tidb_version()`ステートメントは Store タイプ (tikv または unistore) も返します。
-   TiDB には隠しシステム変数がなくなりました。
-   TiDB v6.2.0 では、2 つの新しいシステム テーブルが導入されています。
    -   `INFORMATION_SCHEMA.VARIABLES_INFO` : TiDB システム変数に関する情報を表示するために使用されます。
    -   `PERFORMANCE_SCHEMA.SESSION_VARIABLES` : TiDB セッションレベルのシステム変数に関する情報を表示するために使用されます。

## 削除された機能 {#removed-feature}

TiDB v6.2.0 以降、 BRを使用した RawKV のバックアップと復元は非推奨になりました。

## 改良点 {#improvements}

-   TiDB

    -   `SHOW COUNT(*) WARNINGS`および`SHOW COUNT(*) ERRORS`ステートメント[#25068](https://github.com/pingcap/tidb/issues/25068) @ [リクズン](https://github.com/likzn)をサポート

    -   一部のシステム変数の検証チェックを追加[#35048](https://github.com/pingcap/tidb/issues/35048) @ [モルゴ](https://github.com/morgo)

    -   一部の型変換のエラー メッセージを最適化する[#32447](https://github.com/pingcap/tidb/issues/32744) @ [ファンレンフー](https://github.com/fanrenhoo)

    -   `KILL`コマンドが DDL 操作[#24144](https://github.com/pingcap/tidb/issues/24144) @ [モルゴ](https://github.com/morgo)をサポートするようになりました

    -   もう`SHOW TABLES/DATABASES LIKE …`つの出力を MySQL 互換にします。出力の列名には`LIKE`値[#35116](https://github.com/pingcap/tidb/issues/35116) @ [リクズン](https://github.com/likzn)が含まれています

    -   JSON 関連関数のパフォーマンスを改善する[#35859](https://github.com/pingcap/tidb/issues/35859) @ [wjhuang2016](https://github.com/wjhuang2016)

    -   SHA-2 [#35998](https://github.com/pingcap/tidb/issues/35998) @ [ウィルスディフェンダー](https://github.com/virusdefender)を使用したパスワード ログインの検証速度の向上

    -   一部のログ出力を簡略化[#36011](https://github.com/pingcap/tidb/issues/36011) @ [ドヴィーデン](https://github.com/dveeden)

    -   コプロセッサー通信プロトコルを最適化します。これにより、データを読み取るときの TiDB プロセスのメモリ消費を大幅に削減でき、テーブルをスキャンしてDumplingによってデータをエクスポートするシナリオでの OOM の問題をさらに軽減できます。この通信プロトコルを (SESSION または GLOBAL のスコープで) 有効にするかどうかを制御するために、システム変数`tidb_enable_paging`が導入されました。このプロトコルはデフォルトで無効になっています。有効にするには、変数値を`true` [#35633](https://github.com/pingcap/tidb/issues/35633) @ [ティアンカイアマ](https://github.com/tiancaiamao) @ [wshwsh12](https://github.com/wshwsh12)に設定します。

    -   一部の演算子 (HashJoin、HashAgg、Update、Delete) のメモリ追跡の精度を最適化 ( [#35634](https://github.com/pingcap/tidb/issues/35634) 、 [#35631](https://github.com/pingcap/tidb/issues/35631) 、 [#35635](https://github.com/pingcap/tidb/issues/35635) @ [wshwsh12](https://github.com/wshwsh12) ) ( [#34096](https://github.com/pingcap/tidb/issues/34096) @ [エキキシウム](https://github.com/ekexium) )

    -   システム テーブル`INFORMATION_SCHEMA.DATA_LOCK_WAIT`は、楽観的トランザクション[#34609](https://github.com/pingcap/tidb/issues/34609) @ [ロングファングソン](https://github.com/longfangsong)のロック情報の記録をサポートします。

    -   トランザクション[#34456](https://github.com/pingcap/tidb/issues/34456) @ [ロングファンソング](https://github.com/longfangsong)のモニタリング メトリックを追加します。

-   TiKV

    -   gzip を使用したメトリクス応答の圧縮をサポートして、HTTP 本文のサイズを縮小します[#12355](https://github.com/tikv/tikv/issues/12355) @ [栄光](https://github.com/glorv)
    -   Grafana ダッシュボード[#12007](https://github.com/tikv/tikv/issues/12007) @ [ケビン・シアンリウ](https://github.com/kevin-xianliu)の TiKV パネルの読みやすさを改善
    -   適用オペレーター[#12898](https://github.com/tikv/tikv/issues/12898) @ [イーサフロー](https://github.com/ethercflow)のコミット パイプライン パフォーマンスを最適化する
    -   RocksDB で同時に実行されるサブ圧縮操作の数を動的に変更するサポート ( `rocksdb.max-sub-compactions` ) [#13145](https://github.com/tikv/tikv/issues/13145) @ [イーサフロー](https://github.com/ethercflow)

-   PD

    -   リージョンの CPU 使用率の統計的次元をサポートし、Load Base Split [#12063](https://github.com/tikv/tikv/issues/12063) @ [ジャムポテト](https://github.com/JmPotato)の使用シナリオを強化します

-   TiFlash

    -   TiFlash MPP エンジンのエラー処理を改善し、安定性を向上[#5095](https://github.com/pingcap/tiflash/issues/5095) @ [風の語り手](https://github.com/windtalker) @ [イビン87](https://github.com/yibin87)

    -   UTF8_BIN および UTF8MB4_BIN 照合順序[#5294](https://github.com/pingcap/tiflash/issues/5294) @ [ソロツグ](https://github.com/solotzg)の比較と並べ替えを最適化します

-   ツール

    -   バックアップと復元 (BR)

        -   バックアップ データのディレクトリ構造を調整して、大規模なクラスター バックアップ[#30087](https://github.com/pingcap/tidb/issues/30087) @ [MoCuishle28](https://github.com/MoCuishle28)での S3 レート制限によって引き起こされるバックアップの失敗を修正します。

    -   TiCDC

        -   マルチリージョン シナリオ[#5610](https://github.com/pingcap/tiflow/issues/5610) @ [ヒック](https://github.com/hicqu)でランタイム コンテキストの切り替えによって発生するパフォーマンス オーバーヘッドを削減する

        -   REDO ログのパフォーマンスを最適化し、メタとデータの不整合の問題を修正します ( [#6011](https://github.com/pingcap/tiflow/issues/6011) @ [チャールズ・チャン96](https://github.com/CharlesCheung96) ) ( [#5924](https://github.com/pingcap/tiflow/issues/5924) @ [照信雨](https://github.com/zhaoxinyu) ) ( [#6277](https://github.com/pingcap/tiflow/issues/6277) @ [ヒック](https://github.com/hicqu) )

    -   TiDB Lightning

        -   EOF、Read index not ready、 コプロセッサー timeout [#36674](https://github.com/pingcap/tidb/issues/36674) 、 [#36566](https://github.com/pingcap/tidb/issues/36566) @ [D3ハンター](https://github.com/D3Hunter)などの再試行可能なエラーを追加します。

    -   TiUP

        -   TiUPを使用して新しいクラスターをデプロイすると、node-exporter は[1.3.1](https://github.com/prometheus/node_exporter/releases/tag/v1.3.1)バージョンを使用し、blackbox-exporter は[0.21.1](https://github.com/prometheus/blackbox_exporter/releases/tag/v0.21.1)バージョンを使用します。これにより、さまざまなシステムや環境でのデプロイが確実に成功します。

## バグの修正 {#bug-fixes}

-   TiDB

    -   パーティション キーがクエリ条件で使用され、照合がクエリ パーティション テーブル[#32749](https://github.com/pingcap/tidb/issues/32749) @ [ミヨンス](https://github.com/mjonss)のものと異なる場合、パーティションが誤ってプルーニングされる問題を修正します。
    -   ホスト[#33061](https://github.com/pingcap/tidb/issues/33061) @ [モルゴ](https://github.com/morgo)に大文字がある場合、付与されたロールに`SET ROLE`一致しない問題を修正
    -   `auto_increment`の列をドロップできない問題を修正[#34891](https://github.com/pingcap/tidb/issues/34891) @ [定義済み2014](https://github.com/Defined2014)
    -   削除された一部の構成アイテムが`SHOW CONFIG`に表示される問題を修正[#34867](https://github.com/pingcap/tidb/issues/34867) @ [モルゴ](https://github.com/morgo)
    -   `SHOW DATABASES LIKE …`大文字と小文字が区別される問題を修正[#34766](https://github.com/pingcap/tidb/issues/34766) @ [e1ijah1](https://github.com/e1ijah1)
    -   `SHOW TABLE STATUS LIKE ...`大文字と小文字が区別される問題を修正[#7518](https://github.com/pingcap/tidb/issues/7518) @ [リクズン](https://github.com/likzn)
    -   非厳密モード[#34931](https://github.com/pingcap/tidb/issues/34931) @ [e1ijah1](https://github.com/e1ijah1)で`max-index-length`が依然としてエラーを報告する問題を修正します。
    -   `ALTER COLUMN ... DROP DEFAULT`が動かない問題を修正[#35018](https://github.com/pingcap/tidb/issues/35018) @ [定義済み2014](https://github.com/Defined2014)
    -   テーブルを作成するときに、デフォルト値と列のタイプが一致せず、自動的に修正されない問題を修正します[#34881](https://github.com/pingcap/tidb/issues/34881) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)
    -   `DROP USER` [#35059](https://github.com/pingcap/tidb/issues/35059) @ [ルクァンチャオ](https://github.com/lcwangchao)を実行した後、 `mysql.columns_priv`テーブルのデータが同期的に削除されない問題を修正します。
    -   一部のシステムのスキーマ内でのテーブルの作成を禁止することで、DDL ジャムの問題を修正します[#35205](https://github.com/pingcap/tidb/issues/35205) @ [接線](https://github.com/tangenta)
    -   パーティション化されたテーブルをクエリすると、場合によっては「インデックスが範囲外」および「未使用のインデックス」エラーが報告される可能性があるという問題を修正します[#35181](https://github.com/pingcap/tidb/issues/35181) @ [ミヨンス](https://github.com/mjonss)
    -   `INTERVAL expr unit + expr`がエラー[#30253](https://github.com/pingcap/tidb/issues/30253) @ [ミヨンス](https://github.com/mjonss)を報告する可能性がある問題を修正します
    -   トランザクション[#35644](https://github.com/pingcap/tidb/issues/35644) @ [DJshow832](https://github.com/djshow832)で作成した後に一時テーブルが見つからない不具合を修正
    -   照合順序を`ENUM`列[#31637](https://github.com/pingcap/tidb/issues/31637) @ [wjhuang2016](https://github.com/wjhuang2016)に設定すると発生するpanicの問題を修正します。
    -   1 つの PD ノードがダウンすると、他の PD ノード[#35708](https://github.com/pingcap/tidb/issues/35708) @ [接線](https://github.com/tangenta)が再試行されないために`information_schema.TIKV_REGION_STATUS`のクエリが失敗する問題を修正します
    -   `SHOW CREATE TABLE …`が`SET character_set_results = GBK` [#31338](https://github.com/pingcap/tidb/issues/31338) @ [接線](https://github.com/tangenta)の後にセットまたは`ENUM`列を正しく表示できない問題を修正します
    -   システム変数`tidb_log_file_max_days`および`tidb_config` [#35190](https://github.com/pingcap/tidb/issues/35190) @ [モルゴ](https://github.com/morgo)の誤ったスコープを修正
    -   `SHOW CREATE TABLE`の出力が`ENUM`または`SET`列[#36317](https://github.com/pingcap/tidb/issues/36317) @ [定義済み2014](https://github.com/Defined2014)の MySQL と互換性がないという問題を修正します
    -   テーブルを作成するとき、 `LONG BYTE`列の動作が MySQL [#36239](https://github.com/pingcap/tidb/issues/36239) @ [定義済み2014](https://github.com/Defined2014)と互換性がない問題を修正します。
    -   一時テーブル[#36224](https://github.com/pingcap/tidb/issues/36224) @ [DJshow832](https://github.com/djshow832)で`auto_increment = x`が有効にならない問題を修正
    -   列を同時に変更するときの間違ったデフォルト値を修正[#35846](https://github.com/pingcap/tidb/issues/35846) @ [wjhuang2016](https://github.com/wjhuang2016)
    -   可用性を向上させるために、異常な TiKV ノードにリクエストを送信しないようにする[#34906](https://github.com/pingcap/tidb/issues/34906) @ [スティックナーフ](https://github.com/sticnarf)
    -   LOAD DATA ステートメントで列リストが機能しない問題を修正[#35198](https://github.com/pingcap/tidb/issues/35198) @ [スペード・ア・タン](https://github.com/SpadeA-Tang)
    -   一部のシナリオで悲観的ロックが一意でないセカンダリ インデックス[#36235](https://github.com/pingcap/tidb/issues/36235) @ [エキキシウム](https://github.com/ekexium)に誤って追加される問題を修正します。

-   TiKV

    -   悲観的トランザクション[#11612](https://github.com/tikv/tikv/issues/11612) @ [スティックナーフ](https://github.com/sticnarf)で`WriteConflict`エラーを報告しないようにする
    -   非同期コミットが有効になっている場合にペシ悲観的トランザクションでコミット レコードが重複する可能性がある問題を修正します[#12615](https://github.com/tikv/tikv/issues/12615) @ [スティックナーフ](https://github.com/sticnarf)
    -   `storage.api-version`を`1`から`2` [#12600](https://github.com/tikv/tikv/issues/12600) @ [ピンギュ](https://github.com/pingyu)に変更すると TiKV がパニックになる問題を修正
    -   TiKV と PD [#12518](https://github.com/tikv/tikv/issues/12518) @ [5kbps](https://github.com/5kbpers)の間でリージョンサイズの設定が一致しない問題を修正
    -   TiKV が PD クライアント[#12506](https://github.com/tikv/tikv/issues/12506) 、 [#12827](https://github.com/tikv/tikv/issues/12827) @ [コナー1996](https://github.com/Connor1996)を再接続し続ける問題を修正
    -   空の文字列[#12673](https://github.com/tikv/tikv/issues/12673) @ [wshwsh12](https://github.com/wshwsh12)の型変換を実行すると TiKV がパニックになる問題を修正
    -   `DATETIME`値に分数と`Z` [#12739](https://github.com/tikv/tikv/issues/12739) @ [ゲンリキ](https://github.com/gengliqi)が含まれている場合に発生する時間解析エラーの問題を修正します。
    -   Apply オペレーターによって TiKV RocksDB に書き込まれた perf コンテキストが粗粒度[#11044](https://github.com/tikv/tikv/issues/11044) @ [Lykxサシネーター](https://github.com/LykxSassinator)である問題を修正します。
    -   [バックアップ](/tikv-configuration-file.md#backup) / [輸入](/tikv-configuration-file.md#import) / [CDC](/tikv-configuration-file.md#cdc)の構成が無効な場合に TiKV の起動に失敗する問題を修正[#12771](https://github.com/tikv/tikv/issues/12771) @ [3ポインター](https://github.com/3pointer)
    -   ピアの分割と破棄が同時に行われると発生する可能性があるpanicの問題を修正します[#12825](https://github.com/tikv/tikv/issues/12825) @ [ビジージェイ](https://github.com/BusyJay)
    -   ソース ピアがリージョンマージ プロセス[#12663](https://github.com/tikv/tikv/issues/12663) @ [ビジージェイ](https://github.com/BusyJay)でスナップショットによってログをキャッチするときに発生する可能性があるpanicの問題を修正します。
    -   `max_sample_size`が`0` [#11192](https://github.com/tikv/tikv/issues/11192) @ [Lykxサシネーター](https://github.com/LykxSassinator)に設定されている場合に統計を分析することによって引き起こされるpanicの問題を修正します
    -   Raft Engineが有効になっているときに暗号化キーがクリーンアップされない問題を修正します[#12890](https://github.com/tikv/tikv/issues/12890) @ [タボキー](https://github.com/tabokie)
    -   `get_valid_int_prefix`関数が TiDB と互換性がない問題を修正します。たとえば、 `FLOAT`型は`INT` [#13045](https://github.com/tikv/tikv/issues/13045) @ [グオシャオゲ](https://github.com/guo-shaoge)に誤って変換されました
    -   新しいリージョンのコミット ログ期間が長すぎるため、QPS が[#13077](https://github.com/tikv/tikv/issues/13077) @ [コナー1996](https://github.com/Connor1996)低下する問題を修正します。
    -   リージョンのハートビートが中断された後、PD が TiKV に再接続しない問題を修正します[#12934](https://github.com/tikv/tikv/issues/12934) @ [バタフライ](https://github.com/bufferflies)

-   ツール

    -   バックアップと復元 (BR)

        -   レート制限されたバックアップ タスク[#31722](https://github.com/pingcap/tidb/issues/31722) @ [MoCuishle28](https://github.com/MoCuishle28)を終了した後、 BR がレート制限をリセットしない問題を修正します。

## 寄稿者 {#contributors}

TiDB コミュニティの次の貢献者に感謝します。

-   [e1ijah1](https://github.com/e1ijah1)
-   [プラグワルボルカル](https://github.com/PrajwalBorkar)
-   [リクズン](https://github.com/likzn)
-   [ラーフルク789](https://github.com/rahulk789)
-   [ウィルスディフェンダー](https://github.com/virusdefender)
-   [joycse06](https://github.com/joycse06)
-   [モルゴ](https://github.com/morgo)
-   [ixuh12](https://github.com/ixuh12)
-   [ブラックティア23](https://github.com/blacktear23)
-   [ジョンハックス7](https://github.com/johnhaxx7)
-   [GoGim1](https://github.com/GoGim1)
-   [レンバオシュオ](https://github.com/renbaoshuo)
-   [ゼアオリ](https://github.com/Zheaoli)
-   [ファンレンホー](https://github.com/fanrenhoo)
-   [ニューウェルキン](https://github.com/njuwelkin)
-   [ワイヤービーバー](https://github.com/wirybeaver)
-   [ヘイコン](https://github.com/hey-kong)
-   [ファテレイ](https://github.com/fatelei)
-   [イーストフィッシャー](https://github.com/eastfisher) : 初めての貢献者
-   [ジュネジー](https://github.com/Juneezee) : 初めての貢献者
