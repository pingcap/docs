---
title: TiDB 7.5.0 Release Notes
summary: TiDB 7.5.0 の新機能、互換性の変更、改善、バグ修正について説明します。
---

# TiDB 7.5.0 リリースノート {#tidb-7-5-0-release-notes}

発売日: 2023年12月1日

TiDB バージョン: 7.5.0

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v7.5/quick-start-with-tidb) | [実稼働環境への導入](https://docs.pingcap.com/tidb/v7.5/production-deployment-using-tiup)

TiDB 7.5.0 は長期サポートリリース (LTS) です。

以前の LTS 7.1.0 と比較して、 7.5.0 には、 [7.2.0-DMR](/releases/release-7.2.0.md) 、 [7.3.0-DMR](/releases/release-7.3.0.md) 、 [7.4.0-DMR](/releases/release-7.4.0.md)でリリースされた新機能、改善、バグ修正が含まれています。 7.1.x から 7.5.0 にアップグレードする場合、 [TiDB リリースノート PDF](https://docs-download.pingcap.com/pdf/tidb-v7.2-to-v7.5-en-release-notes.pdf)をダウンロードして、2 つの LTS バージョン間のすべてのリリース ノートを表示できます。 次の表に、 7.2.0 から 7.5.0 までのハイライトの一部を示します。

<table><thead><tr><th>カテゴリ</th><th>特徴</th><th>説明</th></tr></thead><tbody><tr><td>スケーラビリティとパフォーマンス</td><td>複数の<code>ADD INDEX</code>ステートメントを並列実行することをサポート</td><td>この機能により、同時ジョブで 1 つのテーブルに複数のインデックスを追加できます。以前は、2 つの<code>ADD INDEX</code>ステートメント (X とY ) を同時に実行するには、X の時間とYの時間がかかっていました。この機能により、1 つの SQL で 2 つのインデックス X とY を追加する処理を同時に実行できるようになり、DDL の合計実行時間が大幅に短縮されます。特に、テーブルが広いシナリオでは、内部テスト データによると、パフォーマンスが最大 94% 向上することが示されています。</td></tr><tr><td rowspan="3">信頼性と可用性</td><td><a href="https://docs.pingcap.com/tidb/v7.5/tidb-global-sort" target="_blank">グローバルソート</a>の最適化 (実験的、v7.4.0 で導入)</td><td> TiDB v7.1.0 では <a href="https://docs.pingcap.com/tidb/v7.5/tidb-distributed-execution-framework" target="_blank">、分散実行フレームワーク (DXF)</a>が導入されました。このフレームワークを利用するタスクでは、v7.4 でグローバル ソートが導入され、データ再編成タスク中に一時的に順序が乱れたデータによって発生する不要な I/O、CPU、メモリのスパイクが排除されます。グローバル ソートでは、ジョブ中に中間ファイルを保存するために外部共有オブジェクトstorage(この最初のイテレーションでは Amazon S3) が活用され、柔軟性とコスト削減が向上します。ADD <code>ADD INDEX</code>や<code>IMPORT INTO</code>などの操作は、より高速で、より回復力があり、より安定し、より柔軟になり、実行コストも削減されます。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v7.5/tidb-resource-control#manage-background-tasks" target="_blank">バックグラウンド タスクのリソース制御</a>(実験的、v7.4.0 で導入)</td><td> v7.1.0 では、ワークロード間のリソースとstorageのアクセスの干渉を軽減するために、<a href="https://docs.pingcap.com/tidb/v7.5/tidb-resource-control" target="_blank">リソース制御</a>機能が導入されました。TiDB v7.4.0 では、この制御がバックグラウンド タスクの優先度にも適用されました。v7.4.0 では、リソース制御によって、自動分析、バックアップと復元、 TiDB Lightningによる一括ロード、オンライン DDL などのバックグラウンド タスク実行の優先度が識別および管理されるようになりました。将来のリリースでは、この制御は最終的にすべてのバックグラウンド タスクに適用される予定です。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v7.5/tidb-resource-control#manage-queries-that-consume-more-resources-than-expected-runaway-queries">暴走クエリを管理する</a>ためのリソース制御 (実験的、v7.2.0 で導入)</td><td><a href="https://docs.pingcap.com/tidb/v7.5/tidb-resource-control" target="_blank">リソース コントロールは</a>、リソース グループによってリソースを分離するワークロードのフレームワークですが、個々のクエリが各グループ内の作業にどのように影響するかについては考慮しません。TiDB v7.2.0 では、「ランナウェイ クエリ コントロール」が導入され、TiDB がリソース グループごとにこれらのクエリを識別して処理する方法を制御できるようになりました。必要に応じて、長時間実行されるクエリは終了または調整される可能性があり、クエリは正確な SQL テキスト、SQL ダイジェスト、またはそのプラン ダイジェストによって識別され、より一般化されます。v7.3.0 では、TiDB によって、データベース レベルの SQL ブロックリストと同様に、既知の不良クエリをプロアクティブに監視できます。</td></tr><tr><td>構文</td><td>MySQL 8.0 互換性 (v7.4.0 で導入)</td><td> MySQL 8.0 では、デフォルトの文字セットは utf8mb4 で、 utf8mb4 のデフォルトの照合照合順序は<code>utf8mb4_0900_ai_ci</code>です。TiDB v7.4.0 でこれに対するサポートが追加されたことで、MySQL 8.0 との互換性が向上し、デフォルトの照合順序を持つ MySQL 8.0 データベースからの移行とレプリケーションがよりスムーズになりました。</td></tr><tr><td rowspan="4"> DB 操作と可観測性</td><td>TiDB Lightning の物理インポート モードが<a href="https://docs.pingcap.com/tidb/v7.5/sql-statement-import-into"><code>IMPORT INTO</code></a> (GA) で TiDB に統合されました</td><td>v7.2.0 より前では、ファイル システムに基づいてデータをインポートするには、 <a href="https://docs.pingcap.com/tidb/v7.5/tidb-lightning-overview">TiDB Lightning</a>をインストールし、その物理インポート モードを使用する必要がありました。現在では、同じ機能が<code>IMPORT INTO</code>ステートメントに統合されているため、このステートメントを使用して、追加のツールをインストールせずにデータをすばやくインポートできます。このステートメントは、並列インポート用の<a href="https://docs.pingcap.com/tidb/v7.5/tidb-distributed-execution-framework" target="_blank">Distributed eXecution Framework (DXF)</a>もサポートしており、大規模なインポート時のインポート効率が向上します。</td></tr><tr><td> <code>ADD INDEX</code>および<code>IMPORT INTO</code> SQL ステートメントを実行するための<a href="https://docs.pingcap.com/tidb/v7.5/system-variables#tidb_service_scope-new-in-v740" target="_blank">それぞれの TiDB ノード</a>を指定します (GA)</td><td>既存の TiDB ノードまたは新しく追加された TiDB ノードの一部で<code>ADD INDEX</code>または<code>IMPORT INTO</code> SQL ステートメントを実行するかどうかを柔軟に指定できます。このアプローチにより、残りの TiDB ノードからのリソース分離が可能になり、ビジネス オペレーションへの影響を防ぎながら、前述の SQL ステートメントを実行するための最適なパフォーマンスを確保できます。v7.5.0 では、この機能が一般提供 (GA) されます。</td></tr><tr><td> DDL は<a href="https://docs.pingcap.com/tidb/v7.5/ddl-introduction#ddl-related-commands">一時停止と再開の操作</a>をサポートします (GA)</td><td>インデックスを追加すると、大量のリソースが消費され、オンライン トラフィックに影響を与える可能性があります。リソース グループで調整されている場合やラベル付きノードに分離されている場合でも、緊急時にはこれらのジョブを一時停止する必要がある可能性があります。v7.2.0 以降、TiDB は、これらのバックグラウンド ジョブを一度にいくつでも一時停止することをネイティブにサポートするようになりました。これにより、ジョブをキャンセルして再開する必要がなくなり、必要なリソースが解放されます。</td></tr><tr><td> TiDBダッシュボードはTiKVのヒーププロファイリングをサポート<a href="https://docs.pingcap.com/tidb/v7.5/dashboard-profiling" target="_blank"></a></td><td>以前は、TiKV OOM または高メモリ使用量の問題に対処するには、通常、インスタンス環境でヒープ プロファイルを生成するために<code>jeprof</code>を手動で実行する必要がありました。v7.5.0 以降、TiKV ではヒープ プロファイルのリモート処理が可能になります。ヒープ プロファイルのフレーム グラフとコール グラフに直接アクセスできるようになりました。この機能は、Go ヒープ プロファイリングと同じシンプルで使いやすいエクスペリエンスを提供します。</td></tr></tbody></table>

## 機能の詳細 {#feature-details}

### スケーラビリティ {#scalability}

-   分散実行フレームワーク (DXF) が有効な場合に、 `ADD INDEX`または`IMPORT INTO`タスクを分散実行するための TiDB ノードの指定と分離をサポート[＃46258](https://github.com/pingcap/tidb/issues/46258) @ [うわー](https://github.com/ywqzzy)

    リソースを大量に消費するクラスターで`ADD INDEX`または`IMPORT INTO`タスクを並行して実行すると、大量の TiDB ノード リソースが消費され、クラスターのパフォーマンスが低下する可能性があります。既存のサービスへのパフォーマンスへの影響を回避するために、v7.4.0 では、 [TiDB 分散実行フレームワーク (DXF)](/tidb-distributed-execution-framework.md)の下にある各 TiDB ノードのサービス スコープを制御するための実験的機能としてシステム変数[`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740)導入されています。複数の既存の TiDB ノードを選択するか、新しい TiDB ノードの TiDB サービス スコープを設定すると、分散実行されるすべての`ADD INDEX`および`IMPORT INTO`タスクはこれらのノードでのみ実行されます。v7.5.0 では、この機能が一般提供 (GA) されます。

    詳細については[ドキュメント](/system-variables.md#tidb_service_scope-new-in-v740)参照してください。

### パフォーマンス {#performance}

-   TiDB 分散実行フレームワーク (DXF) が一般提供 (GA) され、並列実行[＃45719](https://github.com/pingcap/tidb/issues/45719) @ [翻訳:](https://github.com/wjhuang2016)における`ADD INDEX`および`IMPORT INTO`タスクのパフォーマンスと安定性が向上しました。

    v7.1.0 で導入された DXF が GA になりました。TiDB v7.1.0 より前のバージョンでは、1 つの TiDB ノードのみが同時に DDL タスクを実行できました。v7.1.0 以降では、DXF の下で複数の TiDB ノードが同じ DDL タスクを並列に実行できます。v7.2.0 以降では、DXF は複数の TiDB ノードが同じ`IMPORT INTO`タスクを並列に実行することをサポートするため、TiDB クラスターのリソースをより有効に活用し、DDL および`IMPORT INTO`タスクのパフォーマンスを大幅に向上できます。さらに、TiDB ノードを増やすことで、これらのタスクのパフォーマンスを直線的に向上させることもできます。

    DXF を使用するには、 [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710)値を`ON`に設定します。

    ```sql
    SET GLOBAL tidb_enable_dist_task = ON;
    ```

    詳細については[ドキュメント](/tidb-global-sort.md)参照してください。

-   単一のSQL文で複数のインデックスを追加するパフォーマンスを向上する[＃41602](https://github.com/pingcap/tidb/issues/41602) @ [タンジェンタ](https://github.com/tangenta)

    v7.5.0 より前では、単一の SQL ステートメントで複数のインデックス ( `ADD INDEX` ) を追加すると、パフォーマンスは個別の SQL ステートメントを使用して複数のインデックスを追加する場合と同等でした。v7.5.0 以降では、単一の SQL ステートメントで複数のインデックスを追加する場合のパフォーマンスが大幅に向上しています。特に幅の広いテーブルを使用するシナリオでは、内部テスト データによると、パフォーマンスが最大 94% 向上することが示されています。

### DB操作 {#db-operations}

-   DDL ジョブは一時停止と再開操作をサポートします (GA) [＃18015](https://github.com/pingcap/tidb/issues/18015) @ [ゴドゥム](https://github.com/godouxm)

    v7.2.0 で導入された DDL ジョブの一時停止および再開操作が一般提供 (GA) されます。これらの操作により、リソースを大量に消費する DDL ジョブ (インデックスの作成など) を一時停止して、リソースを節約し、オンライン トラフィックへの影響を最小限に抑えることができます。リソースが許せば、DDL ジョブをキャンセルして再開することなく、シームレスに再開できます。この機能により、リソースの使用率が向上し、ユーザー エクスペリエンスが強化され、スキーマ変更プロセスが簡素化されます。

    `ADMIN PAUSE DDL JOBS`または`ADMIN RESUME DDL JOBS`使用して複数の DDL ジョブを一時停止および再開できます。

    ```sql
    ADMIN PAUSE DDL JOBS 1,2;
    ADMIN RESUME DDL JOBS 1,2;
    ```

    詳細については[ドキュメント](/ddl-introduction.md#ddl-related-commands)参照してください。

-   BRは統計情報のバックアップと復元をサポートします[＃48008](https://github.com/pingcap/tidb/issues/48008) @ [リーヴルス](https://github.com/Leavrth)

    TiDB v7.5.0 以降、br コマンドライン ツールでは、データベース統計のバックアップと復元を行うための`--ignore-stats`パラメータが導入されています。このパラメータを`false`に設定すると、br コマンドライン ツールは、列、インデックス、およびテーブルの統計のバックアップと復元をサポートします。この場合、バックアップから復元された TiDB データベースの統計収集タスクを手動で実行したり、自動収集タスクの完了を待ったりする必要はありません。この機能により、データベースのメンテナンス作業が簡素化され、クエリのパフォーマンスが向上します。

    詳細については[ドキュメント](/br/br-snapshot-manual.md#back-up-statistics)参照してください。

### 可観測性 {#observability}

-   TiDBダッシュボードはTiKV [＃15927](https://github.com/tikv/tikv/issues/15927) @ [コナー1996](https://github.com/Connor1996)のヒーププロファイリングをサポートします

    以前は、TiKV OOM または高メモリ使用量の問題に対処するには、通常、インスタンス環境でヒープ プロファイルを生成するために`jeprof`を手動で実行する必要がありました。v7.5.0 以降、TiKV ではヒープ プロファイルのリモート処理が可能になります。ヒープ プロファイルのフレーム グラフとコール グラフに直接アクセスできるようになりました。この機能は、Go ヒープ プロファイリングと同じシンプルで使いやすいエクスペリエンスを提供します。

    詳細については[ドキュメント](/dashboard/dashboard-profiling.md)参照してください。

### データ移行 {#data-migration}

-   `IMPORT INTO` SQL文（GA） [＃46704](https://github.com/pingcap/tidb/issues/46704) @ [D3ハンター](https://github.com/D3Hunter)をサポート

    v7.5.0 では、 `IMPORT INTO` SQL ステートメントが一般提供 (GA) されます。このステートメントは、 TiDB Lightningの[物理インポートモード](/tidb-lightning/tidb-lightning-physical-import-mode.md)機能を統合し、CSV、SQL、PARQUET などの形式のデータを TiDB の空のテーブルにすばやくインポートできるようにします。このインポート方法により、 TiDB Lightningを個別に展開および管理する必要がなくなり、データ インポートの複雑さが軽減され、インポートの効率が大幅に向上します。

    詳細については[ドキュメント](/sql-statements/sql-statement-import-into.md)参照してください。

-   データ移行 (DM) は、互換性のない (データの一貫性を損なう) DDL 変更のブロックをサポートします[＃9692](https://github.com/pingcap/tiflow/issues/9692) @ [GMHDBJD](https://github.com/GMHDBJD)

    v7.5.0 より前の DM Binlog Filter 機能では、指定されたイベントのみを移行またはフィルタリングすることができ、粒度は比較的粗いものでした。たとえば、 `ALTER`などの大きな粒度の DDL イベントのみをフィルタリングできます。この方法は、一部のシナリオでは制限されています。たとえば、アプリケーションでは`ADD COLUMN`許可されますが`DROP COLUMN`許可されませんが、以前の DM バージョンでは、どちらも`ALTER`イベントでフィルタリングされます。

    このような問題に対処するため、v7.5.0 では、サポートされる DDL イベントの粒度が改良され、 `MODIFY COLUMN`フィルタリング (列のデータ型の変更)、 `DROP COLUMN`などの、データ損失、データの切り捨て、精度の低下につながる細かい DDL イベントがサポートされるようになりました。必要に応じて構成できます。この機能では、互換性のない DDL 変更のブロックや、そのような変更のエラーの報告もサポートされているため、下流のアプリケーション データに影響を与えないように、適切なタイミングで手動で介入できます。

    詳細については[ドキュメント](/dm/dm-binlog-event-filter.md#parameter-descriptions)参照してください。

-   継続的なデータ検証のためのリアルタイムチェックポイント更新をサポート[＃8463](https://github.com/pingcap/tiflow/issues/8463) @ [リチュンジュ](https://github.com/lichunzhu)

    v7.5.0 より前では、 [継続的なデータ検証機能](/dm/dm-continuous-data-validation.md)は DM から下流へのレプリケーション中にデータの一貫性を保証します。これは、上流データベースから TiDB へのビジネス トラフィックの切り替えの基盤として機能します。ただし、レプリケーションの遅延や不整合データの再検証の待機など、さまざまな要因により、継続的な検証チェックポイントは数分ごとに更新する必要があります。これは、切り替え時間が数十秒に制限されている一部のビジネス シナリオでは受け入れられません。

    継続的なデータ検証のためのチェックポイントのリアルタイム更新の導入により、上流データベースからbinlogの位置を提供できるようになりました。継続的な検証プログラムは、メモリ内でこのbinlogの位置を検出すると、数分ごとにチェックポイントを更新するのではなく、すぐにチェックポイントを更新します。したがって、すぐに更新されるこのチェックポイントに基づいて、カットオフ操作をすばやく実行できます。

    詳細については[ドキュメント](/dm/dm-continuous-data-validation.md#set-the-cutover-point-for-continuous-data-validation)参照してください。

## 互換性の変更 {#compatibility-changes}

> **注記：**
>
> このセクションでは、v7.4.0 から現在のバージョン (v7.5.0) にアップグレードするときに知っておく必要のある互換性の変更について説明します。v7.3.0 以前のバージョンから現在のバージョンにアップグレードする場合は、中間バージョンで導入された互換性の変更も確認する必要がある可能性があります。

### システム変数 {#system-variables}

| 変数名                                                                                                               | タイプを変更   | 説明                                                                                    |
| ----------------------------------------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------- |
| [`tidb_enable_fast_analyze`](/system-variables.md#tidb_enable_fast_analyze)                                       | 非推奨      | 統計`Fast Analyze`機能を有効にするかどうかを制御します。この機能はバージョン 7.5.0 では非推奨です。                          |
| [`tidb_analyze_partition_concurrency`](/system-variables.md#tidb_analyze_partition_concurrency)                   | 修正済み     | さらにテストを行った後、デフォルト値を`1`から`2`に変更します。                                                    |
| [`tidb_build_stats_concurrency`](/system-variables.md#tidb_build_stats_concurrency)                               | 修正済み     | さらにテストを行った後、デフォルト値を`4`から`2`に変更します。                                                    |
| [`tidb_merge_partition_stats_concurrency`](/system-variables.md#tidb_merge_partition_stats_concurrency)           | 修正済み     | このシステム変数は、v7.5.0 以降で有効になります。TiDB がパーティションテーブルを分析するときに、パーティションテーブルの統計をマージする同時実行を指定します。 |
| [`tidb_build_sampling_stats_concurrency`](/system-variables.md#tidb_build_sampling_stats_concurrency-new-in-v750) | 新しく追加された | `ANALYZE`のプロセスのサンプリング同時実行を制御します。                                                      |
| [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-new-in-v750)   | 新しく追加された | この変数は、OOM の問題を回避するために統計を非同期的にマージするために TiDB によって使用されます。                                |
| [`tidb_gogc_tuner_max_value`](/system-variables.md#tidb_gogc_tuner_max_value-new-in-v750)                         | 新しく追加された | GOGC チューナーが調整できる GOGC の最大値を制御します。                                                     |
| [`tidb_gogc_tuner_min_value`](/system-variables.md#tidb_gogc_tuner_min_value-new-in-v750)                         | 新しく追加された | GOGC チューナーが調整できる GOGC の最小値を制御します。                                                     |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーションパラメータ                                                                                                                    | タイプを変更   | 説明                                                                                                                            |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------- |
| ティビ            | [`tikv-client.copr-req-timeout`](/tidb-configuration-file.md#copr-req-timeout-new-in-v750)                                         | 新しく追加された | 単一のコプロセッサー要求のタイムアウトを設定します。                                                                                                    |
| ティクヴ           | [`raftstore.inspect-interval`](/tikv-configuration-file.md#inspect-interval)                                                       | 修正済み     | 低速ノード検出の感度を向上させるためにアルゴリズムを最適化した後、デフォルト値を`500ms`から`100ms`に変更します。                                                               |
| ティクヴ           | [`raftstore.region-compact-min-redundant-rows`](/tikv-configuration-file.md#region-compact-min-redundant-rows-new-in-v710)         | 修正済み     | RocksDB 圧縮をトリガーするために必要な冗長 MVCC 行の数を設定します。v7.5.0 以降、この構成項目は`"raft-kv"`storageエンジンに対して有効になります。                                  |
| ティクヴ           | [`raftstore.region-compact-redundant-rows-percent`](/tikv-configuration-file.md#region-compact-redundant-rows-percent-new-in-v710) | 修正済み     | RocksDB 圧縮をトリガーするために必要な冗長 MVCC 行の割合を設定します。v7.5.0 以降、この構成項目は`"raft-kv"`storageエンジンに対して有効になります。                                 |
| ティクヴ           | [`raftstore.evict-cache-on-memory-ratio`](/tikv-configuration-file.md#evict-cache-on-memory-ratio-new-in-v750)                     | 新しく追加された | TiKV のメモリ使用量がシステム使用可能メモリの 90% を超え、 Raftエントリ キャッシュが占有するメモリが使用メモリの`evict-cache-on-memory-ratio`超えると、TiKV はRaftエントリ キャッシュを削除します。 |
| ティクヴ           | [`memory.enable-heap-profiling`](/tikv-configuration-file.md#enable-heap-profiling-new-in-v750)                                    | 新しく追加された | TiKV のメモリ使用量を追跡するためにヒープ プロファイリングを有効にするかどうかを制御します。                                                                             |
| ティクヴ           | [`memory.profiling-sample-per-bytes`](/tikv-configuration-file.md#profiling-sample-per-bytes-new-in-v750)                          | 新しく追加された | ヒープ プロファイリングによって毎回サンプリングされるデータの量を、最も近い 2 の累乗に切り上げて指定します。                                                                      |
| BR             | [`--ignore-stats`](/br/br-snapshot-manual.md#back-up-statistics)                                                                   | 新しく追加された | データベース統計をバックアップおよび復元するかどうかを制御します。このパラメータを`false`に設定すると、br コマンドライン ツールは、列、インデックス、およびテーブルの統計のバックアップと復元をサポートします。                 |
| ティCDC          | [`case-sensitive`](/ticdc/ticdc-changefeed-config.md)                                                                              | 修正済み     | さらにテストを行った後、デフォルト値を`true`から`false`に変更します。つまり、TiCDC 構成ファイル内のテーブル名とデータベース名は、デフォルトで大文字と小文字が区別されません。                              |
| ティCDC          | [`sink.dispatchers.partition`](/ticdc/ticdc-changefeed-config.md)                                                                  | 修正済み     | TiCDC が増分データを Kafka パーティションに送信する方法を制御します。v7.5.0 では、明示的に指定された列値を使用してパーティション番号を計算する新しい値オプション`columns`が導入されました。                  |
| ティCDC          | [`changefeed-error-stuck-duration`](/ticdc/ticdc-changefeed-config.md)                                                             | 新しく追加された | 内部エラーまたは例外が発生したときに、変更フィードが自動的に再試行できる期間を制御します。                                                                                 |
| ティCDC          | [`encoding-worker-num`](/ticdc/ticdc-changefeed-config.md)                                                                         | 新しく追加された | やり直しモジュール内のエンコードおよびデコード ワーカーの数を制御します。                                                                                         |
| ティCDC          | [`flush-worker-num`](/ticdc/ticdc-changefeed-config.md)                                                                            | 新しく追加された | 再実行モジュール内のフラッシュワーカーの数を制御します。                                                                                                  |
| ティCDC          | [`sink.column-selectors`](/ticdc/ticdc-changefeed-config.md)                                                                       | 新しく追加された | 増分データをディスパッチするときに TiCDC が Kafka に送信するデータ変更イベントの指定された列を制御します。                                                                  |
| ティCDC          | [`sql-mode`](/ticdc/ticdc-changefeed-config.md)                                                                                    | 新しく追加された | DDL ステートメントを解析するときに TiCDC が使用する SQL モードを指定します。デフォルト値は、TiDB のデフォルトの SQL モードと同じです。                                              |
| TiDB Lightning | `--importer`                                                                                                                       | 削除されました  | v7.5.0 で非推奨となった TiKV インポーターのアドレスを指定します。                                                                                       |

## オフラインパッケージの変更 {#offline-package-changes}

v7.5.0 以降では、 `TiDB-community-toolkit` [バイナリパッケージ](/binary-package.md)から次のコンテンツが削除されます。

-   `tikv-importer-{version}-linux-{arch}.tar.gz`
-   `mydumper`
-   `spark-{version}-any-any.tar.gz`
-   `tispark-{version}-any-any.tar.gz`

## 廃止された機能 {#deprecated-features}

-   [マイダンパー](https://docs.pingcap.com/tidb/v4.0/mydumper-overview)は v7.5.0 で非推奨となり、その機能のほとんどは[Dumpling](/dumpling-overview.md)に置き換えられました。Mydumper の代わりにDumpling を使用することを強くお勧めします。

-   TiKV インポーターは v7.5.0 では非推奨です。代わりに[TiDB Lightningの物理インポートモード](/tidb-lightning/tidb-lightning-physical-import-mode.md)使用することを強くお勧めします。

-   TiDB v7.5.0 以降、 [TiDBBinlog](/tidb-binlog/tidb-binlog-overview.md)のデータ レプリケーション機能のテクニカル サポートは提供されなくなりました。データ レプリケーションの代替ソリューションとして[ティCDC](/ticdc/ticdc-overview.md)使用することを強くお勧めします。TiDB Binlog v7.5.0 では、ポイントインタイム リカバリ (PITR) シナリオが引き続きサポートされていますが、このコンポーネントは将来のバージョンでは完全に廃止される予定です。データ復旧の代替ソリューションとして[ピトル](/br/br-pitr-guide.md)使用することを推奨します。

-   統計の[`Fast Analyze`](/system-variables.md#tidb_enable_fast_analyze)機能 (実験的) は、v7.5.0 で非推奨になりました。

-   統計の[増分コレクション](https://docs.pingcap.com/tidb/v7.4/statistics#incremental-collection)機能 (実験的) は、v7.5.0 で非推奨になりました。

## 改善点 {#improvements}

-   ティビ

    -   GlobalStats のマージの同時実行モデル[＃47219](https://github.com/pingcap/tidb/issues/47219)最適化します[`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-new-in-v750)導入して統計の同時読み込みとマージを可能にし、パーティション テーブルでの GlobalStats の生成を高速化します。GlobalStats のマージのメモリ使用量を最適化して、OOM を回避し、メモリ割り当てを削減します。3 @ [ホーキングレイ](https://github.com/hawkingrei)
    -   `ANALYZE`プロセスを最適化します[`tidb_build_sampling_stats_concurrency`](/system-variables.md#tidb_build_sampling_stats_concurrency-new-in-v750)導入して`ANALYZE`の同時実行性をより適切に制御し、リソース消費を削減します`ANALYZE`のメモリ使用量を最適化してメモリ割り当てを削減し、中間結果を再利用することで頻繁な GC を回避します[＃47275](https://github.com/pingcap/tidb/issues/47275) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   配置ポリシーの使用を最適化: ポリシーの範囲をグローバルに設定できるようにサポートし、一般的なシナリオの構文サポートを改善します[＃45384](https://github.com/pingcap/tidb/issues/45384) @ [ノルーシュ](https://github.com/nolouch)
    -   `tidb_ddl_enable_fast_reorg`を有効にしてインデックスを追加するパフォーマンスを改善しました。内部テストでは、v7.5.0 は v6.5.0 と比較してパフォーマンスが最大 62.5% 向上しました[＃47757](https://github.com/pingcap/tidb/issues/47757) @ [タンジェンタ](https://github.com/tangenta)

-   ティクヴ

    -   他のスレッドに影響を与えないように、Titan マニフェスト ファイルを書き込むときにミューテックスを保持しないようにします[＃15351](https://github.com/tikv/tikv/issues/15351) @ [コナー1996](https://github.com/Connor1996)

-   PD

    -   `evict-slow-trend`スケジューラ[＃7156](https://github.com/tikv/pd/issues/7156) @ [リクサシナト](https://github.com/LykxSassinator)の安定性と使いやすさを向上

-   ツール

    -   バックアップと復元 (BR)

        -   スナップショットバックアップ用の新しいテーブル間バックアップパラメータ`table-concurrency`を追加します。このパラメータは、統計バックアップやデータ検証などのメタ情報のテーブル間同時実行を制御するために使用されます[＃48571](https://github.com/pingcap/tidb/issues/48571) @ [3ポインター](https://github.com/3pointer)
        -   スナップショットバックアップの復元中に、 BR は特定のネットワークエラーが発生すると再試行します[＃48528](https://github.com/pingcap/tidb/issues/48528) @ [リーヴルス](https://github.com/Leavrth)

## バグ修正 {#bug-fixes}

-   ティビ

    -   非整数クラスター化インデックス[＃47350](https://github.com/pingcap/tidb/issues/47350) @ [タンジェンタ](https://github.com/tangenta)でのテーブル分割操作を禁止する
    -   タイムゾーン情報が正しくない時間フィールドをエンコードする問題を修正[＃46033](https://github.com/pingcap/tidb/issues/46033) @ [タンジェンタ](https://github.com/tangenta)
    -   ソート演算子によりスピル処理中に TiDB がクラッシュする可能性がある問題を修正[＃47538](https://github.com/pingcap/tidb/issues/47538) @ [風の話し手](https://github.com/windtalker)
    -   TiDBが`GROUP_CONCAT` [＃41957](https://github.com/pingcap/tidb/issues/41957) @ [アイリンキッド](https://github.com/AilinKid)のクエリに対して`Can't find column`を返す問題を修正
    -   `batch-client` in `client-go` [＃47691](https://github.com/pingcap/tidb/issues/47691) @ [クレイジーcs520](https://github.com/crazycs520)のpanic問題を修正
    -   `INDEX_LOOKUP_HASH_JOIN` [＃47788](https://github.com/pingcap/tidb/issues/47788) @ [シーライズ](https://github.com/SeaRise)でのメモリ使用量の推定が不正確になる問題を修正
    -   長期間オフラインだったTiFlashノードの再参加によって生じるワークロードの不均一性の問題を修正[＃35418](https://github.com/pingcap/tidb/issues/35418) @ [風の話し手](https://github.com/windtalker)
    -   HashJoin 演算子がプローブ[＃48082](https://github.com/pingcap/tidb/issues/48082) @ [うわー](https://github.com/wshwsh12)を実行するときにチャンクを再利用できない問題を修正しました。
    -   `COALESCE()`関数が`DATE`の型パラメータ[＃46475](https://github.com/pingcap/tidb/issues/46475) @ [翻訳者](https://github.com/xzhangxian1008)に対して誤った結果型を返す問題を修正しました
    -   サブクエリを含む`UPDATE`ステートメントが誤って PointGet [＃48171](https://github.com/pingcap/tidb/issues/48171) @ [ハイラスティン](https://github.com/Rustin170506)に変換される問題を修正しました
    -   キャッシュされた実行プランに日付型と`unix_timestamp` [＃48165](https://github.com/pingcap/tidb/issues/48165) @ [qw4990](https://github.com/qw4990)の比較が含まれている場合に誤った結果が返される問題を修正しました。
    -   集計関数またはウィンドウ関数を含むデフォルトのインライン共通テーブル式 (CTE) が再帰 CTE [＃47881](https://github.com/pingcap/tidb/issues/47881) @ [エルサ0520](https://github.com/elsa0520)によって参照されるとエラーが報告される問題を修正しました
    -   ウィンドウ関数[＃46177](https://github.com/pingcap/tidb/issues/46177) @ [qw4990](https://github.com/qw4990)によって導入されたソートを減らすために、オプティマイザが誤って IndexFullScan を選択する問題を修正しました。
    -   CTE [＃47881](https://github.com/pingcap/tidb/issues/47881) @ [ウィノロス](https://github.com/winoros)の条件プッシュダウンにより、CTE への複数の参照が誤った結果になる問題を修正しました。
    -   MySQL 圧縮プロトコルが大量のデータ (&gt;=16M) を処理できない問題を修正[＃47152](https://github.com/pingcap/tidb/issues/47152) [＃47157](https://github.com/pingcap/tidb/issues/47157) [＃47161](https://github.com/pingcap/tidb/issues/47161) @ [ドヴェーデン](https://github.com/dveeden)
    -   TiDB が`systemd` [＃47442](https://github.com/pingcap/tidb/issues/47442) @ [ホーキングレイ](https://github.com/hawkingrei)で起動したときに`cgroup`リソース制限を読み取らない問題を修正しました

-   ティクヴ

    -   悲観的トランザクションモードで事前書き込み要求を再試行すると、まれにデータの不整合が発生するリスクがある問題を修正[＃11187](https://github.com/tikv/tikv/issues/11187) @ [ミョンケミンタ](https://github.com/MyonKeminta)

-   PD

    -   `evict-leader-scheduler`構成[＃6897](https://github.com/tikv/pd/issues/6897) @ [ヒューシャープ](https://github.com/HuSharp)失う可能性がある問題を修正
    -   ストアがオフラインになった後、その統計の監視メトリックが削除されない問題を修正[＃7180](https://github.com/tikv/pd/issues/7180) @ [rleungx](https://github.com/rleungx)
    -   配置ルールの構成が複雑な場合に、データレプリケーション自動同期 (DR 自動同期) モードを採用しているクラスターで`canSync`と`hasMajority`誤って計算される可能性がある問題を修正しました[＃7201](https://github.com/tikv/pd/issues/7201) @ [ディスク](https://github.com/disksing)
    -   ルールチェッカーが配置ルール[＃7185](https://github.com/tikv/pd/issues/7185) @ [ノルーシュ](https://github.com/nolouch)の設定に従って学習者を追加しない問題を修正しました。
    -   TiDBダッシュボードがPD `trace`データを正しく読み取れない問題を修正[＃7253](https://github.com/tikv/pd/issues/7253) @ [ノルーシュ](https://github.com/nolouch)
    -   内部的に取得された空の領域が原因でPDがpanic可能性がある問題を修正[＃7261](https://github.com/tikv/pd/issues/7261) @ [翻訳者](https://github.com/lhy1024)
    -   データレプリケーション自動同期（DR自動同期）モード[＃7221](https://github.com/tikv/pd/issues/7221) @ [ディスク](https://github.com/disksing)を採用しているクラスターで`available_stores`誤って計算される問題を修正
    -   TiKV ノードが利用できない場合に PD が通常のピアを削除する可能性がある問題を修正[＃7249](https://github.com/tikv/pd/issues/7249) @ [翻訳者](https://github.com/lhy1024)
    -   大規模なクラスターに複数の TiKV ノードを追加すると、TiKVハートビートレポートが遅くなったり停止したりする可能性がある問題を修正しました[＃7248](https://github.com/tikv/pd/issues/7248) @ [rleungx](https://github.com/rleungx)

-   TiFlash

    -   `UPPER()`と`LOWER()`関数が TiDB とTiFlash [＃7695](https://github.com/pingcap/tiflash/issues/7695) @ [風の話し手](https://github.com/windtalker)の間で矛盾した結果を返す問題を修正しました
    -   空のパーティションでクエリを実行するとクエリが失敗する問題を修正[＃8220](https://github.com/pingcap/tiflash/issues/8220) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)
    -   TiFlashレプリカ[＃8217](https://github.com/pingcap/tiflash/issues/8217) @ [ホンユンヤン](https://github.com/hongyunyan)を複製するときにテーブル作成の失敗によって発生するpanic問題を修正しました。

-   ツール

    -   バックアップと復元 (BR)

        -   PITRが`CREATE INDEX` DDL文[＃47482](https://github.com/pingcap/tidb/issues/47482) @ [リーヴルス](https://github.com/Leavrth)の復元をスキップする可能性がある問題を修正
        -   大規模なワイドテーブル[＃15714](https://github.com/tikv/tikv/issues/15714) @ [ユジュンセン](https://github.com/YuJuncen)をバックアップするときに、一部のシナリオでログバックアップが停止する可能性がある問題を修正しました。

    -   ティCDC

        -   オブジェクト ストア シンク[＃10041](https://github.com/pingcap/tiflow/issues/10041) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)にデータを複製するときに NFS ディレクトリにアクセスすることによって発生するパフォーマンスの問題を修正しました。
        -   `claim-check`が有効になっているときにstorageパスのスペルが間違っている問題を修正[＃10036](https://github.com/pingcap/tiflow/issues/10036) @ [3エースショーハンド](https://github.com/3AceShowHand)
        -   TiCDC のスケジュールが場合によってはバランスが取れない問題を修正[＃9845](https://github.com/pingcap/tiflow/issues/9845) @ [3エースショーハンド](https://github.com/3AceShowHand)
        -   Kafka [＃9855](https://github.com/pingcap/tiflow/issues/9855) @ [ヒック](https://github.com/hicqu)にデータを複製するときに TiCDC が停止する可能性がある問題を修正しました
        -   TiCDCプロセッサが場合によってはpanic可能性がある問題を修正[＃9849](https://github.com/pingcap/tiflow/issues/9849) [＃9915](https://github.com/pingcap/tiflow/issues/9915) @ [ヒック](https://github.com/hicqu) @ [3エースショーハンド](https://github.com/3AceShowHand)
        -   `kv-client.enable-multiplexing`を有効にするとレプリケーション タスクが[＃9673](https://github.com/pingcap/tiflow/issues/9673) @ [ふびんず](https://github.com/fubinzh)で停止する問題を修正しました
        -   REDOログが有効になっている場合にNFS障害により所有者ノードが停止する問題を修正[＃9886](https://github.com/pingcap/tiflow/issues/9886) @ [3エースショーハンド](https://github.com/3AceShowHand)

## パフォーマンステスト {#performance-test}

TiDB v7.5.0 のパフォーマンスについては、 TiDB Cloud Dedicated クラスターの[TPC-C パフォーマンステストレポート](https://docs.pingcap.com/tidbcloud/v7.5.0-performance-benchmarking-with-tpcc)と[Sysbench パフォーマンステストレポート](https://docs.pingcap.com/tidbcloud/v7.5.0-performance-benchmarking-with-sysbench)を参照してください。

## 寄稿者 {#contributors}

TiDB コミュニティの以下の貢献者に感謝いたします。

-   [グランデ](https://github.com/jgrande) (初めての投稿者)
-   [ショーン0915](https://github.com/shawn0915)
