---
title: TiDB 7.5.0 Release Notes
summary: TiDB 7.5.0 の新機能、互換性の変更点、改善点、およびバグ修正についてご確認ください。
---

# TiDB 7.5.0 リリースノート {#tidb-7-5-0-release-notes}

発売日：2023年12月1日

TiDB バージョン: 7.5.0

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v7.5/quick-start-with-tidb)| [本番環境への展開](https://docs.pingcap.com/tidb/v7.5/production-deployment-using-tiup)

TiDB 7.5.0は長期サポートリリース（LTS）です。

以前の LTS 7.1.0 と比較して、7.5.0 には[7.2.0-DMR](/releases/release-7.2.0.md) 、 [7.3.0-DMR](/releases/release-7.3.0.md) 、および[7.4.0-DMR](/releases/release-7.4.0.md)でリリースされた新機能、改善点、およびバグ修正が含まれています。7.1.x から 7.5.0 にアップグレードすると、 [TiDB リリースノート PDF](https://docs-download.pingcap.com/pdf/tidb-v7.2-to-v7.5-en-release-notes.pdf)をダウンロードして、2 つの LTS バージョン間のすべてのリリースノートを確認できます。次の表は、7.2.0 から 7.5.0 までのハイライトの一部を示しています。

<table><thead><tr><th>カテゴリ</th><th>特徴</th><th>説明</th></tr></thead><tbody><tr><td>拡張性とパフォーマンス</td><td>複数の<code>ADD INDEX</code>ステートメントを並列実行することをサポートする</td><td>この機能により、単一のテーブルに対して複数のインデックスを同時に追加するジョブを実行できます。従来は、2つの<code>ADD INDEX</code>ステートメント（XとY ）を同時に実行するには、Xの実行時間とYの実行時間を合わせた時間が必要でした。この機能により、1つのSQLで2つのインデックスXとYを同時に追加できるため、DDLの実行時間が大幅に短縮されます。特に、テーブルサイズが大きいシナリオでは、社内テストデータによると、パフォーマンスが最大94%向上することが示されています。</td></tr><tr><td rowspan="3">信頼性と可用性</td><td><a href="https://docs.pingcap.com/tidb/v7.5/tidb-global-sort" target="_blank">グローバルソート</a>の最適化（実験的、v7.4.0で導入）</td><td> TiDB v7.1.0 では <a href="https://docs.pingcap.com/tidb/v7.5/tidb-distributed-execution-framework" target="_blank">、分散実行フレームワーク (DXF)</a>が導入されました。v7.4 では、このフレームワークを活用するタスク向けにグローバルソートが導入され、データ再編成タスク中に一時的にデータが順不同になることで発生する不要な I/O、CPU、およびメモリの急増を解消します。グローバルソートは、外部共有オブジェクトストレージ(この最初のバージョンでは Amazon S3) を利用してジョブ実行中に中間ファイルを保存することで、柔軟性とコスト削減を実現します。ADD <code>ADD INDEX</code>や<code>IMPORT INTO</code>などの操作は、より高速で、より堅牢で、より安定し、より柔軟になり、実行コストも削減されます。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v7.5/tidb-resource-control#manage-background-tasks" target="_blank">バックグラウンドタスクのリソース制御</a>（実験的、v7.4.0で導入）</td><td>バージョン7.1.0では、ワークロード間のリソースおよびstorageアクセス干渉を軽減するために、<a href="https://docs.pingcap.com/tidb/v7.5/tidb-resource-control" target="_blank">リソース制御</a>機能が導入されました。TiDB v7.4.0では、この制御がバックグラウンドタスクの優先度にも適用されるようになりました。v7.4.0では、リソース制御により、自動分析、バックアップと復元、 TiDB Lightningによる一括ロード、オンラインDDLなどのバックグラウンドタスクの実行優先度が識別され、管理されるようになりました。今後のリリースでは、この制御は最終的にすべてのバックグラウンドタスクに適用される予定です。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v7.5/tidb-resource-control#manage-queries-that-consume-more-resources-than-expected-runaway-queries">暴走クエリを管理する</a>ためのリソース制御（実験的、v7.2.0で導入）</td><td><a href="https://docs.pingcap.com/tidb/v7.5/tidb-resource-control" target="_blank">リソース制御は</a>、リソース グループごとにワークロードをリソース分離するためのフレームワークですが、各グループ内の個々のクエリが作業にどのように影響するかについては何も規定していません。TiDB v7.2.0 では、「暴走クエリ制御」が導入され、リソース グループごとに TiDB がこれらのクエリをどのように識別して処理するかを制御できるようになりました。必要に応じて、実行時間の長いクエリを終了または制限することができ、クエリは、より汎用性を高めるために、正確な SQL テキスト、SQL ダイジェスト、または実行プラン ダイジェストで識別できます。v7.3.0 では、データベース レベルの SQL ブロック リストと同様に、既知の不正なクエリを事前に監視できるようになりました。</td></tr><tr><td> SQL</td><td> MySQL 8.0との互換性（バージョン7.4.0で導入）</td><td> MySQL 8.0 では、デフォルトの文字セットは utf8mb4 であり、utf8mb4 のデフォルトの照合照合順序は<code>utf8mb4_0900_ai_ci</code>です。TiDB v7.4.0 でこのサポートが追加されたことで、MySQL 8.0 との互換性が向上し、デフォルトの照合順序を持つ MySQL 8.0 データベースからの移行やレプリケーションがはるかにスムーズになりました。</td></tr><tr><td rowspan="4">データベースの運用と可観測性</td><td>TiDB Lightningの物理インポートモードが<a href="https://docs.pingcap.com/tidb/v7.5/sql-statement-import-into"><code>IMPORT INTO</code></a> (GA)でTiDBに統合されました</td><td>バージョン7.2.0より前は、ファイルシステムに基づいてデータをインポートするには、 <a href="https://docs.pingcap.com/tidb/v7.5/tidb-lightning-overview">TiDB Lightning</a>をインストールし、その物理インポートモードを使用する必要がありました。現在では、同じ機能が<code>IMPORT INTO</code>ステートメントに統合されているため、追加のツールをインストールすることなく、このステートメントを使用してデータを迅速にインポートできます。このステートメントは、並列インポート用の <a href="https://docs.pingcap.com/tidb/v7.5/tidb-distributed-execution-framework" target="_blank">分散実行フレームワーク（DXF）</a>もサポートしており、大規模なインポート時のインポート効率が向上します。</td></tr><tr><td> <code>ADD INDEX</code>および<code>IMPORT INTO</code> SQLステートメントを実行する<a href="https://docs.pingcap.com/tidb/v7.5/system-variables#tidb_service_scope-new-in-v740" target="_blank">TiDBノード</a>を指定します（GA）。</td><td>既存のTiDBノードの一部、または新しく追加されたTiDBノードで<code>ADD INDEX</code>または<code>IMPORT INTO</code> SQLステートメントを実行するかどうかを柔軟に指定できます。このアプローチにより、他のTiDBノードからリソースを分離できるため、業務への影響を防ぎながら、前述のSQLステートメントの実行において最適なパフォーマンスを確保できます。この機能は、バージョン7.5.0で一般提供（GA）されます。</td></tr><tr><td> DDLは<a href="https://docs.pingcap.com/tidb/v7.5/ddl-introduction#ddl-related-commands">一時停止および再開操作</a>をサポートします（一般提供）。</td><td>インデックスの追加は大量のリソースを消費し、オンラインのトラフィックに影響を与える可能性があります。リソースグループでスロットリングしたり、ラベル付きノードに隔離したりした場合でも、緊急時にはこれらのジョブを一時停止する必要が生じる場合があります。TiDBはバージョン7.2.0以降、これらのバックグラウンドジョブを一度にいくつでも一時停止できる機能をネイティブにサポートしており、ジョブのキャンセルと再起動を回避しながら必要なリソースを解放できます。</td></tr><tr><td> TiDB DashboardはTiKVのヒーププロファイリングをサポートしています<a href="https://docs.pingcap.com/tidb/v7.5/dashboard-profiling" target="_blank"></a></td><td>従来、TiKVのメモリ不足（OOM）やメモリ使用量過多の問題に対処するには、インスタンス環境で<code>jeprof</code>を手動で実行してヒーププロファイルを生成する必要がありました。v7.5.0以降、TiKVはヒーププロファイルのリモート処理に対応しました。これにより、ヒーププロファイルのフレームグラフとコールグラフに直接アクセスできるようになりました。この機能は、Goのヒーププロファイリングと同様に、シンプルで使いやすい操作性を提供します。</td></tr></tbody></table>

## 機能の詳細 {#feature-details}

### 拡張性 {#scalability}

-   分散実行フレームワーク (DXF) が有効になっている場合に`ADD INDEX`または`IMPORT INTO`タスクを分散実行するために TiDB ノードを指定および分離する機能をサポートする [#46258](https://github.com/pingcap/tidb/issues/46258) @[ywqzzy](https://github.com/ywqzzy)

    リソース集約型のクラスタで`ADD INDEX`または`IMPORT INTO`タスクを並列実行すると、大量の TiDB ノード リソースが消費され、クラスタのパフォーマンスが低下する可能性があります。既存のサービスのパフォーマンスへの影響を回避するため、v7.4.0 では、 [TiDB分散実行フレームワーク（DXF）](/tidb-distributed-execution-framework.md)の下で各 TiDB ノードのサービス スコープを制御する実験的機能としてシステム変数[`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740)を導入しました。既存の TiDB ノードを複数選択するか、新しい TiDB ノードの TiDB サービス スコープを設定すると、分散実行される`ADD INDEX`および`IMPORT INTO`タスクは、これらのノードでのみ実行されます。この機能は、v7.5.0 で一般提供 (GA) されます。

    詳細については、 [ドキュメント](/system-variables.md#tidb_service_scope-new-in-v740)を参照してください。

### パフォーマンス {#performance}

-   TiDB 分散実行フレームワーク (DXF) が一般提供 (GA) となり、 `ADD INDEX`および`IMPORT INTO`タスクの並列実行におけるパフォーマンスと安定性が向上しました [#45719](https://github.com/pingcap/tidb/issues/45719) @[wjhuang2016](https://github.com/wjhuang2016)

    v7.1.0 で導入された DXF が GA になりました。TiDB v7.1.0 より前のバージョンでは、同時に実行できる TiDB ノードは 1 つだけでした。v7.1.0 以降では、DXF の下で複数の TiDB ノードが同じ DDL タスクを並列実行できます。v7.2.0 以降では、DXF は複数の TiDB ノードが同じ`IMPORT INTO`タスクを並列実行することをサポートし、TiDB クラスタのリソースをより有効に活用し、DDL および`IMPORT INTO`タスクのパフォーマンスを大幅に向上させます。さらに、TiDB ノードを増やすことで、これらのタスクのパフォーマンスを線形的に向上させることもできます。

    DXFを使用するには、 [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710)値を`ON`に設定します。

    ```sql
    SET GLOBAL tidb_enable_dist_task = ON;
    ```

    詳細については、[ドキュメント](/tidb-global-sort.md)を参照してください。

-   単一のSQL文で複数のインデックスを追加する際のパフォーマンスを改善する [#41602](https://github.com/pingcap/tidb/issues/41602) @[tangenta](https://github.com/tangenta)

    バージョン7.5.0より前は、1つのSQL文で複数のインデックス（ `ADD INDEX` ）を追加した場合、パフォーマンスは個別のSQL文で複数のインデックスを追加した場合とほぼ同じでした。バージョン7.5.0以降では、1つのSQL文で複数のインデックスを追加する際のパフォーマンスが大幅に向上しました。特に、テーブルサイズが大きいシナリオでは、社内テストデータによると、パフォーマンスが最大94%向上することが示されています。

### データベース操作 {#db-operations}

-   DDL ジョブは操作の一時停止と再開をサポート (GA) [#18015](https://github.com/pingcap/tidb/issues/18015) @[godouxm](https://github.com/godouxm)

    バージョン7.2.0で導入されたDDLジョブの一時停止および再開機能が一般提供（GA）となりました。これらの機能により、インデックス作成などのリソースを大量に消費するDDLジョブを一時停止してリソースを節約し、オンライントラフィックへの影響を最小限に抑えることができます。リソースに余裕ができたら、DDLジョブをキャンセルして再起動することなく、シームレスに再開できます。この機能により、リソース利用率が向上し、ユーザーエクスペリエンスが強化され、スキーマ変更プロセスが簡素化されます。

    `ADMIN PAUSE DDL JOBS`または`ADMIN RESUME DDL JOBS`を使用して、複数の DDL ジョブを一時停止および再開できます。

    ```sql
    ADMIN PAUSE DDL JOBS 1,2;
    ADMIN RESUME DDL JOBS 1,2;
    ```

    詳細については、 [ドキュメント](/best-practices/ddl-introduction.md#ddl-related-commands)を参照してください。

-   BRは統計情報のバックアップと復元をサポートします [#48008](https://github.com/pingcap/tidb/issues/48008) @[Leavrth](https://github.com/Leavrth)

    TiDB v7.5.0以降、brコマンドラインツールでは、データベース統計のバックアップと復元を行うための`--ignore-stats`パラメータが導入されました。このパラメータを`false`に設定すると、brコマンドラインツールは列、インデックス、およびテーブルの統計のバックアップと復元をサポートします。この場合、バックアップから復元されたTiDBデータベースの統計収集タスクを手動で実行したり、自動収集タスクの完了を待ったりする必要はありません。この機能により、データベースのメンテナンス作業が簡素化され、クエリのパフォーマンスが向上します。

    詳細については、 [ドキュメント](/br/br-snapshot-manual.md#back-up-statistics)を参照してください。

### 可観測性 {#observability}

-   TiDB Dashboardは TiKV のヒープ プロファイリングをサポートします [#15927](https://github.com/tikv/tikv/issues/15927) @[Connor1996](https://github.com/Connor1996)

    従来、TiKV の OOM やメモリ使用量過多の問題に対処するには、インスタンス環境でヒープ プロファイルを生成するために`jeprof`を手動で実行する必要がありました。v7.5.0 以降、TiKV はヒープ プロファイルのリモート処理に対応しました。ヒープ プロファイルのフレーム グラフとコール グラフに直接アクセスできるようになりました。この機能により、Go のヒープ プロファイリングと同様に、シンプルで使いやすい操作性を実現しています。

    詳細については、[ドキュメント](/dashboard/dashboard-profiling.md)を参照してください。

### データ移行 {#data-migration}

-   `IMPORT INTO` SQL ステートメントのサポート (GA) [#46704](https://github.com/pingcap/tidb/issues/46704) @[D3Hunter](https://github.com/D3Hunter)

    バージョン7.5.0では、 `IMPORT INTO` SQLステートメントが一般提供（GA）されます。このステートメントは、 TiDB Lightningの[物理インポートモード](/tidb-lightning/tidb-lightning-physical-import-mode.md)機能を統合し、CSV、SQL、PARQUETなどの形式のデータをTiDBの空のテーブルにすばやくインポートできるようにします。このインポート方法により、 TiDB Lightningの個別のデプロイと管理が不要になり、データインポートの複雑さが軽減され、インポート効率が大幅に向上します。

    詳細については、 [ドキュメント](/sql-statements/sql-statement-import-into.md)を参照してください。

-   データ移行 (DM) は、互換性のない (データ整合性を損なう) DDL 変更のブロックをサポートします [#9692](https://github.com/pingcap/tiflow/issues/9692) @[GMHDBJD](https://github.com/GMHDBJD)

    v7.5.0 より前の DM Binlog Filter 機能は、指定されたイベントを移行またはフィルタリングすることしかできず、粒度が比較的粗いものでした。たとえば、 `ALTER`のような DDL イベントの大きな粒度しかフィルタリングできませんでした。この方法は、いくつかのシナリオで制限がありました。たとえば、アプリケーションは`ADD COLUMN`は許可しますが、 `DROP COLUMN`許可しませんが、以前の DM バージョンでは両方とも`ALTER`イベントでフィルタリングされていました。

    このような問題に対処するため、v7.5.0 では、 `MODIFY COLUMN` (列のデータ型の変更)、 `DROP COLUMN` などのフィルタリングや、データ損失、データの切り捨て、精度低下につながるその他の細かい DDL イベントなど、サポートされる DDL イベントの粒度を細かくしています。必要に応じて設定できます。この機能は、互換性のない DDL 変更をブロックし、そのような変更のエラーを報告することもサポートしているため、下流のアプリケーション データへの影響を回避するために、タイムリーに手動で介入できます。

    詳細については、 [ドキュメント](/dm/dm-binlog-event-filter.md#parameter-descriptions)を参照してください。

-   継続的なデータ検証のためのリアルタイムチェックポイント更新をサポート [#8463](https://github.com/pingcap/tiflow/issues/8463) @[lichunzhu](https://github.com/lichunzhu)

    バージョン7.5.0より前では、 データ[継続的なデータ検証機能](/dm/dm-continuous-data-validation.md)DMからダウンストリームへのレプリケーション中にデータの一貫性を保証します。これは、アップストリームデータベースからTiDBへのビジネストラフィックの切り替えの基礎となります。しかし、レプリケーションの遅延や不整合データの再検証待ちなど、さまざまな要因により、継続的な検証チェックポイントを数分ごとに更新する必要がありました。切り替え時間が数十秒に制限されている一部のビジネスシナリオでは、これは許容できません。

    連続データ検証におけるチェックポイントのリアルタイム更新機能の導入により、上流データベースからbinlogの位置を指定できるようになりました。連続検証プログラムは、メモリ内でこのbinlogの位置を検出すると、数分ごとに更新するのではなく、即座にチェックポイントを更新します。そのため、この即座に更新されたチェックポイントに基づいて、迅速なカットオフ処理を実行できます。

    詳細については、 [ドキュメント](/dm/dm-continuous-data-validation.md#set-the-cutover-point-for-continuous-data-validation)を参照してください。

## 互換性の変更 {#compatibility-changes}

> **注記：**
>
> このセクションでは、バージョン7.4.0から最新バージョン（7.5.0）にアップグレードする際に知っておくべき互換性の変更点について説明します。バージョン7.3.0以前のバージョンから最新バージョンにアップグレードする場合は、中間バージョンで導入された互換性の変更点も確認する必要があるかもしれません。

### システム変数 {#system-variables}

| 変数名                                                                                                               | 変更の種類  | 説明                                                                                    |
| ----------------------------------------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------- |
| [`tidb_enable_fast_analyze`](/system-variables.md#tidb_enable_fast_analyze)                                       | 非推奨      | 統計情報`Fast Analyze`機能を有効にするかどうかを制御します。この機能はバージョン 7.5.0 で非推奨になりました。                     |
| [`tidb_analyze_partition_concurrency`](/system-variables.md#tidb_analyze_partition_concurrency)                   | 変更     | さらなるテストの結果、デフォルト値を`1`から`2`に変更します。                                                     |
| [`tidb_build_stats_concurrency`](/system-variables.md#tidb_build_stats_concurrency)                               | 変更     | さらなるテストの結果、デフォルト値を`4`から`2`に変更します。                                                     |
| [`tidb_merge_partition_stats_concurrency`](/system-variables.md#tidb_merge_partition_stats_concurrency)           | 変更     | このシステム変数はv7.5.0から有効になります。TiDBがパーティションテーブルを分析する際に、パーティションテーブルの統計情報をマージする際の同時実行数を指定します。 |
| [`tidb_build_sampling_stats_concurrency`](/system-variables.md#tidb_build_sampling_stats_concurrency-new-in-v750) | 新しく追加された | `ANALYZE`プロセスのサンプリング同時実行性を制御します。                                                      |
| [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-new-in-v750)   | 新しく追加された | この変数は、TiDBが統計情報を非同期的にマージしてメモリ不足の問題を回避するために使用されます。                                     |
| [`tidb_gogc_tuner_max_value`](/system-variables.md#tidb_gogc_tuner_max_value-new-in-v750)                         | 新しく追加された | GOGCチューナーが調整できるGOGCの最大値を制御します。                                                        |
| [`tidb_gogc_tuner_min_value`](/system-variables.md#tidb_gogc_tuner_min_value-new-in-v750)                         | 新しく追加された | GOGCチューナーが調整できるGOGCの最小値を制御します。                                                        |

### コンフィグレーションファイルパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーションパラメータ                                                                                                                    | 変更の種類  | 説明                                                                                                                                      |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB           | [`tikv-client.copr-req-timeout`](/tidb-configuration-file.md#copr-req-timeout-new-in-v750)                                         | 新しく追加された | 単一のコプロセッサー要求のタイムアウトを設定します。                                                                                                              |
| TiKV           | [`raftstore.inspect-interval`](/tikv-configuration-file.md#inspect-interval)                                                       | 変更     | 低速ノード検出の感度を向上させるためにアルゴリズムを最適化した後、デフォルト値を`500ms`から`100ms`に変更します。                                                                         |
| TiKV           | [`raftstore.region-compact-min-redundant-rows`](/tikv-configuration-file.md#region-compact-min-redundant-rows-new-in-v710)         | 変更     | RocksDB の圧縮をトリガーするために必要な冗長 MVCC 行の数を設定します。v7.5.0 以降、この設定項目は`"raft-kv"`ストレージエンジンに対して有効になります。                                           |
| TiKV           | [`raftstore.region-compact-redundant-rows-percent`](/tikv-configuration-file.md#region-compact-redundant-rows-percent-new-in-v710) | 変更     | RocksDB の圧縮をトリガーするために必要な冗長 MVCC 行の割合を設定します。v7.5.0 以降、この設定項目は`"raft-kv"`ストレージエンジンに対して有効になります。                                          |
| TiKV           | [`raftstore.evict-cache-on-memory-ratio`](/tikv-configuration-file.md#evict-cache-on-memory-ratio-new-in-v750)                     | 新しく追加された | TiKV のメモリ使用量がシステムで使用可能なメモリの 90% を超え、Raftエントリ キャッシュによって占有されているメモリが使用済みメモリの`evict-cache-on-memory-ratio`を超えると、TiKV はRaftエントリ キャッシュを削除します。 |
| TiKV           | [`memory.enable-heap-profiling`](/tikv-configuration-file.md#enable-heap-profiling-new-in-v750)                                    | 新しく追加された | TiKVのメモリ使用量を追跡するためにヒーププロファイリングを有効にするかどうかを制御します。                                                                                         |
| TiKV           | [`memory.profiling-sample-per-bytes`](/tikv-configuration-file.md#profiling-sample-per-bytes-new-in-v750)                          | 新しく追加された | ヒーププロファイリングによって毎回サンプリングされるデータ量を指定します。値は2のべき乗に切り上げられます。                                                                                  |
| BR             | [`--ignore-stats`](/br/br-snapshot-manual.md#back-up-statistics)                                                                   | 新しく追加された | データベース統計情報のバックアップと復元を行うかどうかを制御します。このパラメーター`false`に設定すると、br コマンドラインツールは列、インデックス、およびテーブルの統計情報のバックアップと復元をサポートします。                          |
| TiCDC          | [`case-sensitive`](/ticdc/ticdc-changefeed-config.md)                                                                              | 変更     | さらなるテストの結果、デフォルト値が`true`から`false`に変更されました。これは、TiCDC 構成ファイル内のテーブル名とデータベース名がデフォルトで大文字と小文字を区別しないことを意味します。                                  |
| TiCDC          | [`sink.dispatchers.partition`](/ticdc/ticdc-changefeed-config.md)                                                                  | 変更     | TiCDC が増分データを Kafka パーティションにディスパッチする方法を制御します。v7.5.0 では、明示的に指定された列の値を使用してパーティション番号を計算する新しい値オプション`columns`が導入されました。                       |
| TiCDC          | [`changefeed-error-stuck-duration`](/ticdc/ticdc-changefeed-config.md)                                                             | 新しく追加された | 内部エラーや例外が発生した場合に、チェンジフィードが自動的に再試行する期間を制御します。                                                                                            |
| TiCDC          | [`encoding-worker-num`](/ticdc/ticdc-changefeed-config.md)                                                                         | 新しく追加された | リドゥモジュール内のエンコードワーカーとデコードワーカーの数を制御します。                                                                                                   |
| TiCDC          | [`flush-worker-num`](/ticdc/ticdc-changefeed-config.md)                                                                            | 新しく追加された | リドゥモジュール内のフラッシュワーカーの数を制御します。                                                                                                            |
| TiCDC          | [`sink.column-selectors`](/ticdc/ticdc-changefeed-config.md)                                                                       | 新しく追加された | TiCDCが増分データをディスパッチする際にKafkaに送信する、指定されたデータ変更イベントの列を制御します。                                                                                |
| TiCDC          | [`sql-mode`](/ticdc/ticdc-changefeed-config.md)                                                                                    | 新しく追加された | TiCDCがDDLステートメントを解析する際に使用するSQLモードを指定します。デフォルト値はTiDBのデフォルトのSQLモードと同じです。                                                                  |
| TiDB Lightning | `--importer`                                                                                                                       | 削除済み     | TiKV-importerのアドレスを指定します。この機能はv7.5.0で非推奨となりました。                                                                                         |

## オフラインパッケージの変更 {#offline-package-changes}

v7.5.0 以降、次のコンテンツが`TiDB-community-toolkit`[バイナリパッケージ](/binary-package.md)から削除されます。

-   `tikv-importer-{version}-linux-{arch}.tar.gz`
-   `mydumper`
-   `spark-{version}-any-any.tar.gz`
-   `tispark-{version}-any-any.tar.gz`

## 非推奨機能 {#deprecated-features}

-   [mydumper](https://docs-archive.pingcap.com/tidb/v4.0/mydumper-overview)はバージョン7.5.0で非推奨となり、その機能のほとんどは[Dumpling](/dumpling-overview.md)に置き換えられました。Mydumperの代わりにDumplingを使用することを強くお勧めします。

-   TiKV インポーターは v7.5.0 で非推奨になりました。代わりに[TiDB Lightningの物理インポートモード](/tidb-lightning/tidb-lightning-physical-import-mode.md)を使用することを強くお勧めします。

-   TiDB v7.5.0以降、 [TiDB Binlog](https://docs.pingcap.com/tidb/v7.5/tidb-binlog-overview)のデータレプリケーション機能に関する技術サポートは提供されなくなりました。データレプリケーションの代替ソリューションとして[TiCDC](/ticdc/ticdc-overview.md)を使用することを強くお勧めします。TiDB Binlog v7.5.0は引き続きポイントインタイムリカバリ（PITR）シナリオをサポートしていますが、このコンポーネントは将来のバージョンで完全に非推奨となります。データリカバリの代替ソリューションとして[PITR](/br/br-pitr-guide.md)使用することをお勧めします。

-   統計情報用の[`Fast Analyze`](/system-variables.md#tidb_enable_fast_analyze)機能（実験的）は、バージョン7.5.0で非推奨となりました。

-   統計の[増分収集](https://docs-archive.pingcap.com/tidb/v7.4/statistics#incremental-collection)機能 (実験的) は v7.5.0 で非推奨になりました。

## 改善点 {#improvements}

-   TiDB

    -   グローバル統計情報のマージにおける並行処理モデルを最適化： [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-new-in-v750)を導入し、統計情報の同時ロードとマージを可能にすることで、パーティションテーブル上のグローバル統計情報の生成を高速化します。グローバル統計情報のマージにおけるメモリ使用量を最適化し、メモリ不足エラー（OOM）を回避し、メモリ割り当てを削減します。 [#47219](https://github.com/pingcap/tidb/issues/47219) @[hawkingrei](https://github.com/hawkingrei)
    -   `ANALYZE`プロセスを最適化します。tidb_build_sampling_stats_concurrency [`tidb_build_sampling_stats_concurrency`](/system-variables.md#tidb_build_sampling_stats_concurrency-new-in-v750)導入し`ANALYZE`の並行性をより適切に制御してリソース消費を削減します。 `ANALYZE`のメモリ使用量を最適化し、中間結果を再利用することでメモリ割り当てを削減し、頻繁な GC を回避します。 [#47275](https://github.com/pingcap/tidb/issues/47275) @[hawkingrei](https://github.com/hawkingrei)
    -   配置ポリシーの使用を最適化：ポリシーの範囲をグローバルに設定する機能をサポートし、一般的なシナリオにおける構文サポートを改善します。 [#45384](https://github.com/pingcap/tidb/issues/45384) @[nolouch](https://github.com/nolouch)
    -   `tidb_ddl_enable_fast_reorg`が有効になっている場合のインデックス追加のパフォーマンスを向上させます。内部テストでは、v7.5.0 は v6.5.0 と比較して最大 62.5% パフォーマンスが向上しています。 [#47757](https://github.com/pingcap/tidb/issues/47757) @[tangenta](https://github.com/tangenta)

-   TiKV

    -   Titanマニフェストファイルを書き込む際にミューテックスを保持しないようにして、他のスレッドへの影響を防ぐ [#15351](https://github.com/tikv/tikv/issues/15351) @[Connor1996](https://github.com/Connor1996)

-   PD

    -   `evict-slow-trend`スケジューラの安定性と使いやすさを改善 [#7156](https://github.com/tikv/pd/issues/7156) @[LykxSassinator](https://github.com/LykxSassinator)

-   ツール

    -   Backup & Restore (BR)

        -   スナップショットバックアップ用の新しいテーブル間バックアップパラメータ`table-concurrency`を追加します。このパラメータは、統計バックアップやデータ検証などのメタ情報のテーブル間同時実行を制御するために使用されます。 [#48571](https://github.com/pingcap/tidb/issues/48571) @[3pointer](https://github.com/3pointer)
        -   スナップショットバックアップの復元中に、 BR は特定のネットワークエラーに遭遇すると再試行します [#48528](https://github.com/pingcap/tidb/issues/48528) @[Leavrth](https://github.com/Leavrth)

## バグ修正 {#bug-fixes}

-   TiDB

    -   非整数クラスター化インデックスでの分割テーブル操作を禁止 [#47350](https://github.com/pingcap/tidb/issues/47350) @[tangenta](https://github.com/tangenta)
    -   タイムゾーン情報が間違っているタイムフィールドのエンコード問題を修正 [#46033](https://github.com/pingcap/tidb/issues/46033) @[tangenta](https://github.com/tangenta)
    -   Sort オペレーターがスピル プロセス中に TiDB をクラッシュさせる可能性がある問題を修正 [#47538](https://github.com/pingcap/tidb/issues/47538) @[windtalker](https://github.com/windtalker)
    -   TiDB が`Can't find column`を使用したクエリに対して`GROUP_CONCAT`を返す問題を修正 [#41957](https://github.com/pingcap/tidb/issues/41957) @[AilinKid](https://github.com/AilinKid)
    -   `batch-client`の`client-go`のpanic問題を修正 [#47691](https://github.com/pingcap/tidb/issues/47691) @[crazycs520](https://github.com/crazycs520)
    -   `INDEX_LOOKUP_HASH_JOIN` のメモリ使用量推定の誤りを修正 [#47788](https://github.com/pingcap/tidb/issues/47788) @[SeaRise](https://github.com/SeaRise)
    -   長期間オフラインだったTiFlashノードの再参加によって生じる不均一なワークロードの問題を修正 [#35418](https://github.com/pingcap/tidb/issues/35418) @[windtalker](https://github.com/windtalker)
    -   HashJoin オペレーターがプローブを実行する際にチャンクを再利用できない問題を修正します [#48082](https://github.com/pingcap/tidb/issues/48082) @[wshwsh12](https://github.com/wshwsh12)
    -   `COALESCE()`関数が`DATE`型のパラメータに対して誤った結果型を返す問題を修正しました [#46475](https://github.com/pingcap/tidb/issues/46475) @[xzhangxian1008](https://github.com/xzhangxian1008)
    -   サブクエリを含む`UPDATE`ステートメントが誤って PointGet に変換される問題を修正 [#48171](https://github.com/pingcap/tidb/issues/48171) @[Rustin170506](https://github.com/Rustin170506)
    -   キャッシュされた実行プランに日付型と`unix_timestamp`の比較が含まれている場合に誤った結果が返される問題を修正します [#48165](https://github.com/pingcap/tidb/issues/48165) @[qw4990](https://github.com/qw4990)
    -   集計関数またはウィンドウ関数を含むデフォルトのインライン共通テーブル式（CTE）が再帰CTEによって参照された場合にエラーが報告される問題を修正します [#47881](https://github.com/pingcap/tidb/issues/47881) @[elsa0520](https://github.com/elsa0520)
    -   ウィンドウ関数によって導入されたソートを削減するために、オプティマイザが誤って IndexFullScan を選択する問題を修正しました [#46177](https://github.com/pingcap/tidb/issues/46177) @[qw4990](https://github.com/qw4990)
    -   CTEの条件プッシュダウンにより、複数のCTE参照によって誤った結果が生じる問題を修正 [#47881](https://github.com/pingcap/tidb/issues/47881) @[winoros](https://github.com/winoros)
    -   MySQLの圧縮プロトコルが大量のデータ（&gt;=16M）を処理できない問題を修正[#47152](https://github.com/pingcap/tidb/issues/47152) [#47157](https://github.com/pingcap/tidb/issues/47157) [#47161](https://github.com/pingcap/tidb/issues/47161) @[dveeden](https://github.com/dveeden)
    -   TiDBが`cgroup`で起動されたときに`systemd`のリソース制限を読み取らない問題を修正 [#47442](https://github.com/pingcap/tidb/issues/47442) @[hawkingrei](https://github.com/hawkingrei)

-   TiKV

    -   悲観的トランザクションモードでのプリライト要求の再試行が、まれにデータ不整合のリスクを引き起こす可能性がある問題を修正しました [#11187](https://github.com/tikv/tikv/issues/11187) @[MyonKeminta](https://github.com/MyonKeminta)

-   PD

    -   `evict-leader-scheduler`の設定が失われる可能性がある問題を修正 [#6897](https://github.com/tikv/pd/issues/6897) @[HuSharp](https://github.com/HuSharp)
    -   ストアがオフラインになった後、その統計情報の監視メトリックが削除されない問題を修正します [#7180](https://github.com/tikv/pd/issues/7180) @[rleungx](https://github.com/rleungx)
    -   データレプリケーション自動同期（DR Auto-Sync）モードを採用しているクラスターにおいて、配置ルールの設定が複雑な場合に`canSync` `hasMajority`が正しく計算されない可能性がある問題を修正します [#7201](https://github.com/tikv/pd/issues/7201) @[disksing](https://github.com/disksing)
    -   ルールチェッカーが配置ルールの設定に従ってラーナーを追加しない問題を修正 [#7185](https://github.com/tikv/pd/issues/7185) @[nolouch](https://github.com/nolouch)
    -   TiDB DashboardがPD `trace`データを正しく読み取れない問題を修正 [#7253](https://github.com/tikv/pd/issues/7253) @[nolouch](https://github.com/nolouch)
    -   内部的に取得したリージョンが空であるためにPDがpanic可能性がある問題を修正 [#7261](https://github.com/tikv/pd/issues/7261) @[lhy1024](https://github.com/lhy1024)
    -   データレプリケーション自動同期（DR Auto-Sync）モードを採用しているクラスターで`available_stores`が正しく計算されない問題を修正します [#7221](https://github.com/tikv/pd/issues/7221) @[disksing](https://github.com/disksing)
    -   TiKVノードが利用できない場合にPDが通常のピアを削除する可能性がある問題を修正 [#7249](https://github.com/tikv/pd/issues/7249) @[lhy1024](https://github.com/lhy1024)
    -   大規模クラスターに複数の TiKV ノードを追加すると、TiKV のハートビート報告が遅くなったり停止したりする可能性がある問題を修正しました [#7248](https://github.com/tikv/pd/issues/7248) @[rleungx](https://github.com/rleungx)

-   TiFlash

    -   `UPPER()`関数と`LOWER()`関数がTiDB とTiFlashの間で一貫性のない結果を返す問題を修正 [#7695](https://github.com/pingcap/tiflash/issues/7695) @[windtalker](https://github.com/windtalker)
    -   空のパーティションでクエリを実行するとクエリが失敗する問題を修正 [#8220](https://github.com/pingcap/tiflash/issues/8220) @[JaySon-Huang](https://github.com/JaySon-Huang)
    -   TiFlashレプリカの複製時にテーブル作成失敗によって発生するpanic問題を修正 [#8217](https://github.com/pingcap/tiflash/issues/8217) @[hongyunyan](https://github.com/hongyunyan)

-   ツール

    -   Backup & Restore (BR)

        -   PITRが`CREATE INDEX` DDLステートメントの復元をスキップする可能性がある問題を修正 [#47482](https://github.com/pingcap/tidb/issues/47482) @[Leavrth](https://github.com/Leavrth)
        -   大規模で幅の広いテーブルをバックアップする際に、ログバックアップが一部のシナリオで停止する可能性がある問題を修正しました [#15714](https://github.com/tikv/tikv/issues/15714) @[YuJuncen](https://github.com/YuJuncen)

    -   TiCDC

        -   オブジェクトストアシンクへのデータ複製時にNFSディレクトリにアクセスすることで発生するパフォーマンス問題を修正 [#10041](https://github.com/pingcap/tiflow/issues/10041) @[CharlesCheung96](https://github.com/CharlesCheung96)
        -   `claim-check`が有効な場合にストレージパスのスペルが間違っている問題を修正 [#10036](https://github.com/pingcap/tiflow/issues/10036) @[3AceShowHand](https://github.com/3AceShowHand)
        -   TiCDCのスケジューリングのバランスが崩れる場合がある問題を修正 [#9845](https://github.com/pingcap/tiflow/issues/9845) @[3AceShowHand](https://github.com/3AceShowHand)
        -   TiCDCがKafkaへのデータ複製時に停止する可能性がある問題を修正 [#9855](https://github.com/pingcap/tiflow/issues/9855) @[hicqu](https://github.com/hicqu)
        -   場合によっては TiCDC プロセッサがpanicになる問題を修正[#9849](https://github.com/pingcap/tiflow/issues/9849) [#9915](https://github.com/pingcap/tiflow/issues/9915) @[hicqu](https://github.com/hicqu)@[3AceShowHand](https://github.com/3AceShowHand)
        -   `kv-client.enable-multiplexing`を有効にするとレプリケーションタスクが停止する問題を修正 [#9673](https://github.com/pingcap/tiflow/issues/9673) @[fubinzh](https://github.com/fubinzh)
        -   REDOログが有効な場合にNFS障害によりオーナーノードがスタックする問題を修正 [#9886](https://github.com/pingcap/tiflow/issues/9886) @[3AceShowHand](https://github.com/3AceShowHand)

## 性能テスト {#performance-test}

TiDB v7.5.0 のパフォーマンスについては、 [TPC-C性能試験報告書](https://docs.pingcap.com/tidbcloud/v7.5.0-performance-benchmarking-with-tpcc)とTiDB Cloud Dedicatedクラスターの[Sysbenchパフォーマンステストレポート](https://docs.pingcap.com/tidbcloud/v7.5.0-performance-benchmarking-with-sysbench)を参照してください。

## 貢献者 {#contributors}

TiDBコミュニティの以下の貢献者の皆様に感謝申し上げます。

-   [jgrande](https://github.com/jgrande) (初回貢献者)
-   [shawn0915](https://github.com/shawn0915)
