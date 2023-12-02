---
title: TiDB 7.5.0 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 7.5.0.
---

# TiDB 7.5.0 リリースノート {#tidb-7-5-0-release-notes}

発売日：2023年12月1日

TiDB バージョン: 7.5.0

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v7.5/quick-start-with-tidb) | [本番展開](https://docs.pingcap.com/tidb/v7.5/production-deployment-using-tiup) | [インストールパッケージ](https://www.pingcap.com/download/?version=v7.5.0#version-list)

TiDB 7.5.0 は長期サポート リリース (LTS) です。

以前の LTS 7.1.0 と比較して、7.5.0 には[7.2.0-DMR](/releases/release-7.2.0.md) 、 [7.3.0-DMR](/releases/release-7.3.0.md) 、および[7.4.0-DMR](/releases/release-7.4.0.md)でリリースされた新機能、改善、バグ修正が含まれています。 7.1.x から 7.5.0 にアップグレードする場合、 [TiDB リリース ノート PDF](https://download.pingcap.org/tidb-v7.2-to-v7.5-en-release-notes.pdf)ダウンロードして 2 つの LTS バージョン間のすべてのリリース ノートを表示できます。次の表に、7.2.0 から 7.5.0 までのいくつかのハイライトを示します。

<table><thead><tr><th>カテゴリー</th><th>特徴</th><th>説明</th></tr></thead><tbody><tr><td>スケーラビリティとパフォーマンス</td><td>複数の<code>ADD INDEX</code>ステートメントの並列実行をサポート</td><td>この機能により、同時ジョブで 1 つのテーブルに複数のインデックスを追加できるようになります。以前は、2 つの<code>ADD INDEX</code>ステートメント ( X とY ) を同時に実行するには、 X の時間にYの時間を加えた時間がかかりました。この機能により、1 つの SQL で 2 つのインデックス X とY を追加する処理を同時に実行できるようになり、DDL の合計実行時間が大幅に短縮されます。特に幅の広いテーブルを使用するシナリオでは、パフォーマンスが最大 94% 向上することが内部テスト データで示されています。</td></tr><tr><td rowspan="3">信頼性と可用性</td><td><a href="https://docs.pingcap.com/tidb/v7.5/tidb-global-sort" target="_blank">グローバル ソートの</a>最適化 (実験的、v7.4.0 で導入)</td><td> TiDB v7.2.0 では、 <a href="https://docs.pingcap.com/tidb/v7.5/tidb-distributed-execution-framework" target="_blank">分散実行フレームワークが</a>導入されました。このフレームワークを利用するタスクのために、v7.4 ではグローバル ソートを導入し、データ再編成タスク中に一時的に順序が狂ったデータによって引き起こされる不必要な I/O、CPU、メモリのスパイクを排除します。グローバル並べ替えでは、外部共有オブジェクトstorage(この最初の反復では Amazon S3) を利用してジョブ中に中間ファイルを保存し、柔軟性とコスト削減を高めます。 <code>ADD INDEX</code>や<code>IMPORT INTO</code>などの操作は、より速く、より復元力があり、より安定し、より柔軟になり、実行コストが削減されます。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v7.5/tidb-resource-control#manage-background-tasks" target="_blank">バックグラウンド タスクのリソース制御</a>(実験的、v7.4.0 で導入)</td><td> v7.1.0 では、ワークロード間のリソースとstorageのアクセス干渉を軽減するために、<a href="https://docs.pingcap.com/tidb/v7.5/tidb-resource-control" target="_blank">リソース制御</a>機能が導入されました。 TiDB v7.4.0 では、この制御をバックグラウンド タスクの優先順位にも適用しました。 v7.4.0 では、リソース コントロールは、自動分析、バックアップと復元、 TiDB Lightningによる一括ロード、オンライン DDL などのバックグラウンド タスク実行の優先順位を識別して管理するようになりました。将来のリリースでは、このコントロールは最終的にすべてのバックグラウンド タスクに適用される予定です。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v7.5/tidb-resource-control#manage-queries-that-consume-more-resources-than-expected-runaway-queries">暴走クエリを管理する</a>ためのリソース制御 (実験的、v7.2.0 で導入)</td><td><a href="https://docs.pingcap.com/tidb/v7.5/tidb-resource-control" target="_blank">リソース コントロールは、</a>リソース グループごとにワークロードをリソース分離するためのフレームワークですが、個々のクエリが各グループ内の作業にどのような影響を与えるかについては言及しません。 TiDB v7.2.0 では、「暴走クエリ制御」が導入され、TiDB がリソース グループごとにこれらのクエリをどのように識別して処理するかを制御できるようになりました。ニーズに応じて、長時間実行されているクエリは終了または調整される可能性があり、より一般化するために、正確な SQL テキスト、SQL ダイジェスト、またはそのプラン ダイジェストによってクエリを識別できます。 v7.3.0 では、TiDB を使用して、データベース レベルの SQL ブロックリストと同様に、既知の不正なクエリを積極的に監視できます。</td></tr><tr><td> SQL</td><td> MySQL 8.0 との互換性 (v7.4.0 で導入)</td><td> MySQL 8.0 では、デフォルトの文字セットは utf8mb4 で、utf8mb4 のデフォルトの照合順序は<code>utf8mb4_0900_ai_ci</code>です。 TiDB v7.4.0 ではこのサポートが追加され、MySQL 8.0 との互換性が強化され、デフォルトの照合順序を使用した MySQL 8.0 データベースからの移行とレプリケーションがよりスムーズになりました。</td></tr><tr><td rowspan="4"> DB の操作と可観測性</td><td>TiDB Lightning の物理インポート モードが<a href="https://docs.pingcap.com/tidb/v7.5/sql-statement-import-into"><code>IMPORT INTO</code></a> (GA) で TiDB に統合されました</td><td>v7.2.0 より前は、ファイル システムに基づいてデータをインポートするには、 <a href="https://docs.pingcap.com/tidb/v7.5/tidb-lightning-overview">TiDB Lightning</a>をインストールし、その物理インポート モードを使用する必要がありました。現在、同じ機能が<code>IMPORT INTO</code>ステートメントに統合されているため、このステートメントを使用すると、追加のツールをインストールせずにデータを迅速にインポートできます。このステートメントは、並行インポートの <a href="https://docs.pingcap.com/tidb/v7.5/tidb-distributed-execution-framework" target="_blank">分散実行フレームワーク</a>もサポートしているため、大規模なインポート時のインポート効率が向上します。</td></tr><tr><td> <code>ADD INDEX</code>および<code>IMPORT INTO</code> SQL ステートメントを実行するための<a href="https://docs.pingcap.com/tidb/v7.5/system-variables#tidb_service_scope-new-in-v740" target="_blank">それぞれの TiDB ノード</a>を指定します (GA)</td><td>既存の TiDB ノードまたは新しく追加された TiDB ノードのいずれかで<code>ADD INDEX</code>または<code>IMPORT INTO</code> SQL ステートメントを実行するかどうかを柔軟に指定できます。このアプローチにより、残りの TiDB ノードからリソースを分離でき、ビジネス運営への影響を防ぎながら、前述の SQL ステートメントを実行するための最適なパフォーマンスを確保できます。 v7.5.0 では、この機能は一般提供 (GA) になります。</td></tr><tr><td> DDL は<a href="https://docs.pingcap.com/tidb/v7.5/ddl-introduction#ddl-related-commands">一時停止および再開操作</a>をサポートします (GA)</td><td>インデックスの追加はリソースを大量に消費する可能性があり、オンライン トラフィックに影響を与える可能性があります。リソース グループ内で調整されている場合や、ラベル付きノードに分離されている場合でも、緊急時にはこれらのジョブを一時停止する必要がある場合があります。 v7.2.0 の時点で、TiDB はこれらのバックグラウンド ジョブの任意の数の同時一時停止をネイティブにサポートするようになり、ジョブをキャンセルして再開する必要を避けながら、必要なリソースを解放します。</td></tr><tr><td> TiDB ダッシュボードは TiKV のヒープ プロファイリングをサポートします<a href="https://docs.pingcap.com/tidb/v7.5/dashboard-profiling" target="_blank"></a></td><td>以前は、TiKV OOM または高メモリ使用量の問題に対処するには、通常、インスタンス環境でヒープ プロファイルを生成するために<code>jeprof</code>を手動で実行する必要がありました。 v7.5.0 以降、TiKV ではヒープ プロファイルのリモート処理が可能になります。ヒープ プロファイルのフレーム グラフとコール グラフに直接アクセスできるようになりました。この機能は、Go ヒープ プロファイリングと同じシンプルで使いやすいエクスペリエンスを提供します。</td></tr></tbody></table>

## 機能の詳細 {#feature-details}

### スケーラビリティ {#scalability}

-   分散実行フレームワークが有効な場合、 `ADD INDEX`または`IMPORT INTO`タスクを分散実行するための TiDB ノードの指定と分離をサポート[#46258](https://github.com/pingcap/tidb/issues/46258) @ [ywqzzy](https://github.com/ywqzzy)

    リソースを大量に消費するクラスターで`ADD INDEX`または`IMPORT INTO`タスクを並行して実行すると、大量の TiDB ノード リソースが消費され、クラスターのパフォーマンスの低下につながる可能性があります。既存のサービスへのパフォーマンスへの影響を回避するために、v7.4.0 では、実験的機能としてシステム変数[`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740)を導入し、 [TiDB バックエンド タスク分散実行フレームワーク](/tidb-distributed-execution-framework.md)の下で各 TiDB ノードのサービス スコープを制御します。複数の既存の TiDB ノードを選択することも、新しい TiDB ノードの TiDB サービス スコープを設定することもでき、分散実行されるすべての`ADD INDEX`および`IMPORT INTO`タスクはこれらのノードでのみ実行されます。 v7.5.0 では、この機能は一般提供 (GA) になります。

    詳細については、 [ドキュメンテーション](/system-variables.md#tidb_service_scope-new-in-v740)を参照してください。

### パフォーマンス {#performance}

-   TiDB バックエンド タスク分散実行フレームワークが一般提供 (GA) され、並列実行における`ADD INDEX`および`IMPORT INTO`タスクのパフォーマンスと安定性が向上しました[#45719](https://github.com/pingcap/tidb/issues/45719) @ [wjhuang2016](https://github.com/wjhuang2016)

    v6.6.0 で導入されたバックエンド タスク分散実行フレームワークは GA になりました。 TiDB v7.1.0 より前のバージョンでは、DDL タスクを同時に実行できる TiDB ノードは 1 つだけです。 v7.1.0 以降、複数の TiDB ノードがバックエンド タスク分散実行フレームワークの下で同じ DDL タスクを並行して実行できるようになりました。 v7.2.0 以降、バックエンド タスク分散実行フレームワークは、複数の TiDB ノードが同じ`IMPORT INTO`のタスクを並行して実行することをサポートします。これにより、TiDB クラスターのリソースがより有効に活用され、DDL および`IMPORT INTO`タスクのパフォーマンスが大幅に向上します。さらに、TiDB ノードを増やして、これらのタスクのパフォーマンスを直線的に向上させることもできます。

    バックエンド タスク分散実行フレームワークを使用するには、値[`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710)を`ON`に設定します。

    ```sql
    SET GLOBAL tidb_enable_dist_task = ON;
    ```

    詳細については、 [ドキュメンテーション](/tidb-global-sort.md)を参照してください。

-   単一の SQL ステートメントで複数のインデックスを追加するパフォーマンスが向上しました[#41602](https://github.com/pingcap/tidb/issues/41602) @ [タンジェンタ](https://github.com/tangenta)

    v7.5.0 より前では、単一の SQL ステートメントに複数のインデックス ( `ADD INDEX` ) を追加する場合、パフォーマンスは個別の SQL ステートメントを使用して複数のインデックスを追加する場合と同様でした。 v7.5.0 以降、単一の SQL ステートメントで複数のインデックスを追加するパフォーマンスが大幅に向上しました。特に幅の広いテーブルを使用するシナリオでは、パフォーマンスが最大 94% 向上することが内部テスト データで示されています。

### DB操作 {#db-operations}

-   DDL ジョブは、一時停止および再開操作 (GA) [#18015](https://github.com/pingcap/tidb/issues/18015) @ [ゴドゥム](https://github.com/godouxm)をサポートします。

    v7.2.0 で導入された DDL ジョブの一時停止および再開操作が一般提供 (GA) になりました。これらの操作により、リソースを大量に消費する DDL ジョブ (インデックスの作成など) を一時停止して、リソースを節約し、オンライン トラフィックへの影響を最小限に抑えることができます。リソースが許せば、DDL ジョブをキャンセルして再開することなく、シームレスに再開できます。この機能により、リソースの使用率が向上し、ユーザー エクスペリエンスが向上し、スキーマ変更プロセスが簡素化されます。

    `ADMIN PAUSE DDL JOBS`または`ADMIN RESUME DDL JOBS`を使用して、複数の DDL ジョブを一時停止および再開できます。

    ```sql
    ADMIN PAUSE DDL JOBS 1,2;
    ADMIN RESUME DDL JOBS 1,2;
    ```

    詳細については、 [ドキュメンテーション](/ddl-introduction.md#ddl-related-commands)を参照してください。

-   BR は統計のバックアップと復元をサポートします[#48008](https://github.com/pingcap/tidb/issues/48008) @ [レヴルス](https://github.com/Leavrth)

    TiDB v7.5.0 以降、br コマンドライン ツールには、データベース統計をバックアップおよび復元するための`--ignore-stats`パラメータが導入されています。このパラメーターを`false`に設定すると、 br コマンドライン ツールは、列、インデックス、テーブルの統計のバックアップと復元をサポートします。この場合、バックアップから復元された TiDB データベースの統計収集タスクを手動で実行したり、自動収集タスクの完了を待つ必要はありません。この機能により、データベースのメンテナンス作業が簡素化され、クエリのパフォーマンスが向上します。

    詳細については、 [ドキュメンテーション](/br/br-snapshot-manual.md#back-up-statistics)を参照してください。

### 可観測性 {#observability}

-   TiDB ダッシュボードは TiKV [#15927](https://github.com/tikv/tikv/issues/15927) @ [コナー1996](https://github.com/Connor1996)のヒープ プロファイリングをサポートします

    以前は、TiKV OOM または高メモリ使用量の問題に対処するには、通常、インスタンス環境でヒープ プロファイルを生成するために`jeprof`を手動で実行する必要がありました。 v7.5.0 以降、TiKV ではヒープ プロファイルのリモート処理が可能になります。ヒープ プロファイルのフレーム グラフとコール グラフに直接アクセスできるようになりました。この機能は、Go ヒープ プロファイリングと同じシンプルで使いやすいエクスペリエンスを提供します。

    詳細については、 [ドキュメンテーション](/dashboard/dashboard-profiling.md)を参照してください。

### データ移行 {#data-migration}

-   `IMPORT INTO` SQL ステートメント (GA) [#46704](https://github.com/pingcap/tidb/issues/46704) @ [D3ハンター](https://github.com/D3Hunter)をサポート

    v7.5.0 では、 `IMPORT INTO` SQL ステートメントが一般提供 (GA) になりました。このステートメントは、 TiDB Lightningの[物理インポートモード](/tidb-lightning/tidb-lightning-physical-import-mode.md)機能を統合し、CSV、SQL、PARQUET などの形式でデータを TiDB の空のテーブルに迅速にインポートできるようにします。このインポート方法により、 TiDB Lightningを個別に展開して管理する必要がなくなり、データ インポートの複雑さが軽減され、インポート効率が大幅に向上します。

    詳細については、 [ドキュメンテーション](/sql-statements/sql-statement-import-into.md)を参照してください。

-   データ移行 (DM) は、互換性のない (データ整合性を損なう) DDL 変更のブロックをサポートします[#9692](https://github.com/pingcap/tiflow/issues/9692) @ [GMHDBJD](https://github.com/GMHDBJD)

    v7.5.0 より前では、DMBinlogフィルター機能は指定されたイベントのみを移行またはフィルターでき、粒度は比較的粗かったです。たとえば、 `ALTER`などの大きな粒度の DDL イベントのみをフィルタリングできます。この方法は一部のシナリオでは制限されます。たとえば、アプリケーションで`ADD COLUMN`許可されますが、 `DROP COLUMN`許可されませんが、以前の DM バージョンでは両方とも`ALTER`イベントによってフィルタリングされます。

    このような問題に対処するために、v7.5.0 では、フィルタリング`MODIFY COLUMN` (列データ型の変更)、 `DROP COLUMN`や、データ損失、データの切り捨て、および精度の低下。必要に応じて設定できます。この機能は、互換性のない DDL 変更のブロックやそのような変更に対するエラーのレポートもサポートしているため、ダウンストリーム アプリケーション データへの影響を回避するために適切なタイミングで手動で介入できます。

    詳細については、 [ドキュメンテーション](/dm/dm-binlog-event-filter.md#parameter-descriptions)を参照してください。

-   継続的なデータ検証のためのリアルタイムのチェックポイント更新をサポート[#8463](https://github.com/pingcap/tiflow/issues/8463) @ [リチュンジュ](https://github.com/lichunzhu)

    v7.5.0 より前では、 [継続的なデータ検証機能](/dm/dm-continuous-data-validation.md)により DM からダウンストリームへのレプリケーション中のデータの整合性が保証されます。これは、上流のデータベースから TiDB へのビジネス トラフィックをカットオーバーするための基礎として機能します。ただし、レプリケーションの遅延や不整合データの再検証の待機などのさまざまな要因により、継続的検証チェックポイントは数分ごとに更新する必要があります。これは、カットオーバー時間が数十秒に制限されている一部のビジネス シナリオでは受け入れられません。

    継続的なデータ検証のためのチェックポイントのリアルタイム更新の導入により、アップストリーム データベースからbinlogの位置を提供できるようになりました。継続的検証プログラムは、メモリ内でこのbinlogの位置を検出すると、チェックポイントを数分ごとに更新するのではなく、ただちに更新します。したがって、この即時に更新されるチェックポイントに基づいて、カットオフ操作を迅速に実行できます。

    詳細については、 [ドキュメンテーション](/dm/dm-continuous-data-validation.md#set-the-cutover-point-for-continuous-data-validation)を参照してください。

## 互換性の変更 {#compatibility-changes}

> **注記：**
>
> このセクションでは、v7.4.0 から現在のバージョン (v7.5.0) にアップグレードするときに知っておく必要がある互換性の変更について説明します。 v7.3.0 以前のバージョンから現在のバージョンにアップグレードする場合は、中間バージョンで導入された互換性の変更も確認する必要がある場合があります。

### システム変数 {#system-variables}

| 変数名                                                                                                               | 種類の変更      | 説明                                                                                       |
| ----------------------------------------------------------------------------------------------------------------- | ---------- | ---------------------------------------------------------------------------------------- |
| [`tidb_enable_fast_analyze`](/system-variables.md#tidb_enable_fast_analyze)                                       | 廃止されました    | 統計`Fast Analyze`機能を有効にするかどうかを制御します。この機能は v7.5.0 で非推奨になりました。                              |
| [`tidb_analyze_partition_concurrency`](/system-variables.md#tidb_analyze_partition_concurrency)                   | 修正済み       | さらにテストを行った後、デフォルト値を`1`から`2`に変更します。                                                       |
| [`tidb_build_stats_concurrency`](/system-variables.md#tidb_build_stats_concurrency)                               | 修正済み       | さらにテストを行った後、デフォルト値を`4`から`2`に変更します。                                                       |
| [`tidb_merge_partition_stats_concurrency`](/system-variables.md#tidb_merge_partition_stats_concurrency)           | 修正済み       | このシステム変数は、v7.5.0 から有効になります。 TiDB がパーティションテーブルを分析するときに、パーティションテーブルの統計をマージする同時実行性を指​​定します。 |
| [`tidb_build_sampling_stats_concurrency`](/system-variables.md#tidb_build_sampling_stats_concurrency-new-in-v750) | 新たに追加されました | `ANALYZE`プロセスのサンプリング同時実行性を制御します。                                                         |
| [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-new-in-v750)   | 新しく追加された   | この変数は、OOM の問題を回避するために、統計を非同期的にマージするために TiDB によって使用されます。                                  |
| [`tidb_gogc_tuner_max_value`](/system-variables.md#tidb_gogc_tuner_max_value-new-in-v750)                         | 新しく追加された   | GOGC チューナーが調整できる GOGC の最大値を制御します。                                                        |
| [`tidb_gogc_tuner_min_value`](/system-variables.md#tidb_gogc_tuner_min_value-new-in-v750)                         | 新しく追加された   | GOGC チューナーが調整できる GOGC の最小値を制御します。                                                        |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーションパラメータ                                                                                                                    | 種類の変更    | 説明                                                                                                                                       |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| TiKV           | [`raftstore.region-compact-min-redundant-rows`](/tikv-configuration-file.md#region-compact-min-redundant-rows-new-in-v710)         | 修正済み     | RocksDB 圧縮をトリガーするために必要な冗長 MVCC 行の数を設定します。 v7.5.0 以降、この構成項目は`"raft-kv"`storageエンジンに対して有効になります。                                            |
| TiKV           | [`raftstore.region-compact-redundant-rows-percent`](/tikv-configuration-file.md#region-compact-redundant-rows-percent-new-in-v710) | 修正済み     | RocksDB 圧縮をトリガーするために必要な冗長 MVCC 行の割合を設定します。 v7.5.0 以降、この構成項目は`"raft-kv"`storageエンジンに対して有効になります。                                           |
| TiKV           | [`raftstore.evict-cache-on-memory-ratio`](/tikv-configuration-file.md#evict-cache-on-memory-ratio-new-in-v750)                     | 新しく追加された | TiKV のメモリ使用量がシステムの利用可能なメモリの 90% を超え、 Raftエントリ キャッシュによって占有されているメモリが使用済みメモリの`evict-cache-on-memory-ratio`を超えると、TiKV はRaftエントリ キャッシュを削除します。 |
| TiKV           | [`memory.enable-heap-profiling`](/tikv-configuration-file.md#enable-heap-profiling-new-in-v750)                                    | 新しく追加された | TiKV のメモリ使用量を追跡するためにヒープ プロファイリングを有効にするかどうかを制御します。                                                                                        |
| TiKV           | [`memory.profiling-sample-per-bytes`](/tikv-configuration-file.md#profiling-sample-per-bytes-new-in-v750)                          | 新しく追加された | ヒープ プロファイリングによって毎回サンプリングされるデータの量を、最も近い 2 の累乗に切り上げて指定します。                                                                                 |
| BR             | [`--ignore-stats`](/br/br-snapshot-manual.md#back-up-statistics)                                                                   | 新しく追加された | データベース統計をバックアップおよび復元するかどうかを制御します。このパラメーターを`false`に設定すると、 br コマンドライン ツールは、列、インデックス、テーブルの統計のバックアップと復元をサポートします。                             |
| TiCDC          | [`case-sensitive`](/ticdc/ticdc-changefeed-config.md)                                                                              | 修正済み     | さらにテストを行った後、デフォルト値を`true`から`false`変更します。これは、TiCDC 構成ファイル内のテーブル名とデータベース名がデフォルトで大文字と小文字を区別しないことを意味します。                                     |
| TiCDC          | [`sink.dispatchers.partition`](/ticdc/ticdc-changefeed-config.md)                                                                  | 修正済み     | TiCDC が増分データを Kafka パーティションにディスパッチする方法を制御します。 v7.5.0 では、新しい値オプション`columns`が導入されており、明示的に指定された列値を使用してパーティション番号を計算します。                      |
| TiCDC          | [`sink.column-selectors`](/ticdc/ticdc-changefeed-config.md)                                                                       | 新しく追加された | 増分データをディスパッチするときに TiCDC が Kafka に送信するデータ変更イベントの指定された列を制御します。                                                                             |
| TiCDC          | [`sql-mode`](/ticdc/ticdc-changefeed-config.md)                                                                                    | 新しく追加された | DDL ステートメントを解析するときに TiCDC が使用する SQL モードを指定します。デフォルト値は、TiDB のデフォルト SQL モードと同じです。                                                          |
| TiDB Lightning | `--importer`                                                                                                                       | 削除されました  | TiKV インポーターのアドレスを指定します。これは v7.5.0 で非推奨になりました。                                                                                            |

## オフラインパッケージの変更 {#offline-package-changes}

v7.5.0 以降、次のコンテンツが`TiDB-community-toolkit` [バイナリパッケージ](/binary-package.md)から削除されます。

-   `tikv-importer-{version}-linux-{arch}.tar.gz`
-   `mydumper`
-   `spark-{version}-any-any.tar.gz`
-   `tispark-{version}-any-any.tar.gz`

## 廃止された機能 {#deprecated-features}

-   [マイダンパー](https://docs.pingcap.com/tidb/v4.0/mydumper-overview)は v7.5.0 で非推奨となり、その機能のほとんどが[Dumpling](/dumpling-overview.md)に置き換えられました。 Mydumper の代わりにDumpling を使用することを強くお勧めします。

-   TiKV インポーターは v7.5.0 で非推奨になりました。代わりに[TiDB Lightningの物理インポート モード](/tidb-lightning/tidb-lightning-physical-import-mode.md)を使用することを強くお勧めします。

-   TiDB v7.5.0 以降、 [TiDBBinlog](/tidb-binlog/tidb-binlog-overview.md)のデータ レプリケーション機能のテクニカル サポートは提供されなくなりました。データ レプリケーションの代替ソリューションとして[TiCDC](/ticdc/ticdc-overview.md)を使用することを強くお勧めします。 TiDB Binlog v7.5.0 は引き続きポイントインタイム リカバリ (PITR) シナリオをサポートしていますが、このコンポーネントは将来のバージョンでは完全に非推奨になります。データ回復の代替ソリューションとして[PITR](/br/br-pitr-guide.md)を使用することをお勧めします。

-   統計の[`Fast Analyze`](/system-variables.md#tidb_enable_fast_analyze)機能 (実験的) は、v7.5.0 で非推奨になりました。

-   統計の[増分コレクション](https://docs.pingcap.com/tidb/v7.4/statistics#incremental-collection)機能 (実験的) は、v7.5.0 で非推奨になりました。

## 改善点 {#improvements}

-   TiDB

    -   GlobalStats をマージする同時実行モデルを最適化します[`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-new-in-v750)を導入すると、統計の同時読み込みとマージが可能になり、パーティション化されたテーブルでの GlobalStats の生成が高速化されます。 GlobalStats をマージする際のメモリ使用量を最適化して、OOM を回避し、メモリ割り当てを削減します。 [#47219](https://github.com/pingcap/tidb/issues/47219) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   `ANALYZE`プロセスを最適化します[`tidb_build_sampling_stats_concurrency`](/system-variables.md#tidb_build_sampling_stats_concurrency-new-in-v750)を導入して`ANALYZE`の同時実行をより適切に制御し、リソース消費を削減します。 `ANALYZE`のメモリ使用量を最適化してメモリ割り当てを削減し、一部の中間結果を再利用することで頻繁な GC を回避します。 [#47275](https://github.com/pingcap/tidb/issues/47275) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   配置ポリシーの使用を最適化します。ポリシーの範囲をグローバルに構成することをサポートし、一般的なシナリオの構文サポートを改善します。 [#45384](https://github.com/pingcap/tidb/issues/45384) @ [ノールーシュ](https://github.com/nolouch)
    -   `tidb_ddl_enable_fast_reorg`を有効にすると、インデックスを追加するパフォーマンスが向上します。内部テストでは、v7.5.0 は v6.5.0 と比較してパフォーマンスが最大 62.5% 向上しました。 [#47757](https://github.com/pingcap/tidb/issues/47757) @ [タンジェンタ](https://github.com/tangenta)

-   TiKV

    -   他のスレッドへの影響を防ぐために、Titan マニフェスト ファイルを書き込むときにミューテックスを保持しないようにします[#15351](https://github.com/tikv/tikv/issues/15351) @ [コナー1996](https://github.com/Connor1996)

-   PD

    -   `evict-slow-trend`スケジューラ[#7156](https://github.com/tikv/pd/issues/7156) @ [リクサシナト](https://github.com/LykxSassinator)の安定性と使いやすさを向上

-   ツール

    -   バックアップと復元 (BR)

        -   スナップショット バックアップ用の新しいテーブル間バックアップ パラメータ`table-concurrency`を追加します。このパラメータは、統計のバックアップやデータ検証などのメタ情報のテーブル間の同時実行性を制御するために使用されます[#48571](https://github.com/pingcap/tidb/issues/48571) @ [3ポインター](https://github.com/3pointer)
        -   スナップショット バックアップの復元中に、特定のネットワーク エラーが発生すると、 BR は再試行します[#48528](https://github.com/pingcap/tidb/issues/48528) @ [レヴルス](https://github.com/Leavrth)

## バグの修正 {#bug-fixes}

-   TiDB

    -   非整数クラスター化インデックス[#47350](https://github.com/pingcap/tidb/issues/47350) @ [タンジェンタ](https://github.com/tangenta)での分割テーブル操作の禁止
    -   間違ったタイムゾーン情報[#46033](https://github.com/pingcap/tidb/issues/46033) @ [タンジェンタ](https://github.com/tangenta)を使用して時間フィールドをエンコードする問題を修正
    -   Sort オペレーターにより、スピル プロセス[#47538](https://github.com/pingcap/tidb/issues/47538) @ [ウィンドトーカー](https://github.com/windtalker)中に TiDB がクラッシュする可能性がある問題を修正します。
    -   TiDB が`GROUP_CONCAT` [#41957](https://github.com/pingcap/tidb/issues/41957) @ [アイリンキッド](https://github.com/AilinKid)のクエリに対して`Can't find column`を返す問題を修正
    -   `batch-client` `client-go` @ [クレイジークス520](https://github.com/crazycs520) [#47691](https://github.com/pingcap/tidb/issues/47691)panicの問題を修正
    -   `INDEX_LOOKUP_HASH_JOIN` [#47788](https://github.com/pingcap/tidb/issues/47788) @ [シーライズ](https://github.com/SeaRise)でのメモリ使用量の推定が正しくない問題を修正
    -   長期間オフラインだったTiFlashノードの再参加によって引き起こされる不均一なワークロードの問題を修正します[#35418](https://github.com/pingcap/tidb/issues/35418) @ [ウィンドトーカー](https://github.com/windtalker)
    -   HashJoin オペレーターがプローブ[#48082](https://github.com/pingcap/tidb/issues/48082) @ [wshwsh12](https://github.com/wshwsh12)を実行するとチャンクが再利用できない問題を修正
    -   `COALESCE()`関数が`DATE`型パラメータ[#46475](https://github.com/pingcap/tidb/issues/46475) @ [xzhangxian1008](https://github.com/xzhangxian1008)に対して間違った結果型を返す問題を修正
    -   サブクエリを含む`UPDATE`ステートメントが誤って PointGet [#48171](https://github.com/pingcap/tidb/issues/48171) @ [こんにちはラスティン](https://github.com/hi-rustin)に変換される問題を修正
    -   キャッシュされた実行プランに日付型と`unix_timestamp` [#48165](https://github.com/pingcap/tidb/issues/48165) @ [qw4990](https://github.com/qw4990)の比較が含まれている場合に、誤った結果が返される問題を修正します。
    -   集約関数またはウィンドウ関数を含むデフォルトのインライン共通関数式 (CTE) が再帰 CTE [#47881](https://github.com/pingcap/tidb/issues/47881) @ [エルサ0520](https://github.com/elsa0520)によって参照されるとエラーが報告される問題を修正します。
    -   ウィンドウ関数[#46177](https://github.com/pingcap/tidb/issues/46177) @ [qw4990](https://github.com/qw4990)によって導入される並べ替えを削減するために、オプティマイザーが誤って IndexFullScan を選択する問題を修正します。
    -   CTE [#47881](https://github.com/pingcap/tidb/issues/47881) @ [ウィノロス](https://github.com/winoros)の条件プッシュダウンにより、CTE への複数の参照により不正確な結果が生じる問題を修正
    -   MySQL 圧縮プロトコルが大量のデータ (&gt;=16M) のロードを処理できないという問題を修正します[#47152](https://github.com/pingcap/tidb/issues/47152) [#47157](https://github.com/pingcap/tidb/issues/47157) [#47161](https://github.com/pingcap/tidb/issues/47161) @ [ドヴィーデン](https://github.com/dveeden)
    -   TiDB が`systemd` [#47442](https://github.com/pingcap/tidb/issues/47442) @ [ホーキングレイ](https://github.com/hawkingrei)で起動されたときに`cgroup`リソース制限を読み込まない問題を修正

-   TiKV

    -   悲観的トランザクションモードでプリライトリクエストを再試行すると、まれにデータ不整合のリスクが発生する可能性がある問題を修正[#11187](https://github.com/tikv/tikv/issues/11187) @ [ミョンケミンタ](https://github.com/MyonKeminta)

-   PD

    -   `evict-leader-scheduler`が設定[#6897](https://github.com/tikv/pd/issues/6897) @ [ヒューシャープ](https://github.com/HuSharp)を失う可能性がある問題を修正
    -   ストアがオフラインになった後、その統計の監視メトリックが削除されない問題を修正します[#7180](https://github.com/tikv/pd/issues/7180) @ [ルルンクス](https://github.com/rleungx)
    -   配置ルールの構成が複雑な場合、データ レプリケーション自動同期 (DR Auto-Sync) モードを採用しているクラスターで`canSync`と`hasMajority`正しく計算されないことがある問題を修正[#7201](https://github.com/tikv/pd/issues/7201) @ [ディスク化](https://github.com/disksing)
    -   ルール チェッカーが配置ルール[#7185](https://github.com/tikv/pd/issues/7185) @ [ノールーシュ](https://github.com/nolouch)の設定に従って学習者を追加しない問題を修正
    -   TiDB ダッシュボードが PD `trace`データを正しく読み取れない問題を修正[#7253](https://github.com/tikv/pd/issues/7253) @ [ノールーシュ](https://github.com/nolouch)
    -   内部的に取得された空のリージョンが原因で PD がpanicになる問題を修正[#7261](https://github.com/tikv/pd/issues/7261) @ [lhy1024](https://github.com/lhy1024)
    -   データ レプリケーション自動同期 (DR Auto-Sync) モード[#7221](https://github.com/tikv/pd/issues/7221) @ [ディスク化](https://github.com/disksing)を採用しているクラスターで`available_stores`が正しく計算されない問題を修正します。
    -   TiKV ノードが利用できない場合に PD が通常のピアを削除する可能性がある問題を修正[#7249](https://github.com/tikv/pd/issues/7249) @ [lhy1024](https://github.com/lhy1024)
    -   大規模なクラスターに複数の TiKV ノードを追加すると、TiKVハートビートレポートが遅くなったりスタックしたりする可能性がある問題を修正します[#7248](https://github.com/tikv/pd/issues/7248) @ [ルルンクス](https://github.com/rleungx)

-   TiFlash

    -   `UPPER()`と`LOWER()`関数が TiDB とTiFlash [#7695](https://github.com/pingcap/tiflash/issues/7695) @ [ウィンドトーカー](https://github.com/windtalker)の間で一貫性のない結果を返す問題を修正
    -   空のパーティションでクエリを実行するとクエリ失敗[#8220](https://github.com/pingcap/tiflash/issues/8220) @ [ジェイ・ソン・ファン](https://github.com/JaySon-Huang)が発生する問題を修正します。
    -   TiFlashレプリカ[#8217](https://github.com/pingcap/tiflash/issues/8217) @ [ホンユニャン](https://github.com/hongyunyan)をレプリケートする際のテーブル作成の失敗によって引き起こされるpanicの問題を修正

-   ツール

    -   バックアップと復元 (BR)

        -   PITR が`CREATE INDEX` DDL ステートメント[#47482](https://github.com/pingcap/tidb/issues/47482) @ [レヴルス](https://github.com/Leavrth)の復元をスキップする可能性がある問題を修正します。
        -   大きな幅のテーブル[#15714](https://github.com/tikv/tikv/issues/15714) @ [ユジュンセン](https://github.com/YuJuncen)をバックアップするときに、一部のシナリオでログ バックアップが停止する可能性がある問題を修正します。

    -   TiCDC

        -   データをオブジェクト ストア シンク[#10041](https://github.com/pingcap/tiflow/issues/10041) @ [CharlesCheung96](https://github.com/CharlesCheung96)にレプリケートするときに NFS ディレクトリにアクセスすることによって発生するパフォーマンスの問題を修正します。
        -   `claim-check`が有効になっている場合にstorageパスのスペルが間違っている問題を修正[#10036](https://github.com/pingcap/tiflow/issues/10036) @ [3エースショーハンド](https://github.com/3AceShowHand)
        -   場合によっては TiCDC スケジューリングのバランスが取れていない問題を修正[#9845](https://github.com/pingcap/tiflow/issues/9845) @ [3エースショーハンド](https://github.com/3AceShowHand)
        -   Kafka [#9855](https://github.com/pingcap/tiflow/issues/9855) @ [ひっくり返る](https://github.com/hicqu)にデータをレプリケートするときに TiCDC がスタックする可能性がある問題を修正
        -   場合によっては TiCDC プロセッサがpanicになる問題を修正[#9849](https://github.com/pingcap/tiflow/issues/9849) [#9915](https://github.com/pingcap/tiflow/issues/9915) @ [ひっくり返る](https://github.com/hicqu) @ [3エースショーハンド](https://github.com/3AceShowHand)
        -   `kv-client.enable-multiplexing`を有効にするとレプリケーション タスクがスタックする問題を修正します[#9673](https://github.com/pingcap/tiflow/issues/9673) @ [フビンジ](https://github.com/fubinzh)
        -   REDO ログが有効になっている場合に、NFS 障害が原因でオーナー ノードがスタックする問題を修正[#9886](https://github.com/pingcap/tiflow/issues/9886) @ [3エースショーハンド](https://github.com/3AceShowHand)

## 性能テスト {#performance-test}

TiDB v7.5.0 のパフォーマンスについては、TiDB 専用クラスターの[TPC-C パフォーマンス テスト レポート](https://docs.pingcap.com/tidbcloud/v7.5.0-performance-benchmarking-with-tpcc)と[Sysbench パフォーマンス テスト レポート](https://docs.pingcap.com/tidbcloud/v7.5.0-performance-benchmarking-with-sysbench)を参照してください。

## 貢献者 {#contributors}

TiDB コミュニティの以下の貢献者に感謝いたします。

-   [ジグランデ](https://github.com/jgrande) (初投稿者)
-   [ショーン0915](https://github.com/shawn0915)
