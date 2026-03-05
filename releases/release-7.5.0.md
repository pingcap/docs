---
title: TiDB 7.5.0 Release Notes
summary: TiDB 7.5.0 の新機能、互換性の変更、改善点、バグ修正について説明します。
---

# TiDB 7.5.0 リリースノート {#tidb-7-5-0-release-notes}

発売日：2023年12月1日

TiDB バージョン: 7.5.0

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v7.5/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v7.5/production-deployment-using-tiup)

TiDB 7.5.0 は長期サポートリリース (LTS) です。

以前のLTSバージョン7.1.0と比較して、7.5.0には[7.3.0-DMR](/releases/release-7.3.0.md) [7.2.0-DMR](/releases/release-7.2.0.md)リリースされた新機能、改善、バグ修正が含まれています。7.1.xから7.5.0にアップグレードする場合、バージョン[TiDB リリースノート PDF](https://docs-download.pingcap.com/pdf/tidb-v7.2-to-v7.5-en-release-notes.pdf)をダウンロードして、2つのLTSバージョン間のすべてのリリースノートをご覧いただけます。以下の表は、7.2.0から[7.4.0-DMR](/releases/release-7.4.0.md)への主な変更点です。

<table><thead><tr><th>カテゴリ</th><th>特徴</th><th>説明</th></tr></thead><tbody><tr><td>スケーラビリティとパフォーマンス</td><td>複数の<code>ADD INDEX</code>文を並列実行することをサポート</td><td>この機能により、複数のジョブを並列実行して単一テーブルに複数のインデックスを追加できるようになります。以前は、2つの<code>ADD INDEX</code>文（XとY ）を同時に実行すると、XとYの時間がかかっていました。この機能により、1つのSQLで2つのインデックスXとYを同時に追加できるようになり、DDLの実行時間が大幅に短縮されます。特に幅の広いテーブルを扱うシナリオでは、社内テストデータでパフォーマンスが最大94%向上することが示されています。</td></tr><tr><td rowspan="3">信頼性と可用性</td><td><a href="https://docs.pingcap.com/tidb/v7.5/tidb-global-sort" target="_blank">グローバルソート</a>の最適化（実験的、v7.4.0 で導入）</td><td> TiDB v7.1.0 では <a href="https://docs.pingcap.com/tidb/v7.5/tidb-distributed-execution-framework" target="_blank">、分散実行フレームワーク (DXF)</a>が導入されました。このフレームワークを利用するタスク向けに、v7.4 ではグローバルソートが導入され、データ再編成タスク中に一時的に順序が乱れたデータによって発生する不要な I/O、CPU、メモリのスパイクを解消します。グローバルソートは、ジョブ実行中に中間ファイルを保存するために外部共有オブジェクトstorage(この最初のイテレーションでは Amazon S3) を利用するため、柔軟性とコスト削減が向上します。ADD <code>ADD INDEX</code>や<code>IMPORT INTO</code>などの操作は、より高速で、より回復力があり、より安定し、より柔軟になり、実行コストも削減されます。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v7.5/tidb-resource-control#manage-background-tasks" target="_blank">バックグラウンド タスクのリソース制御</a>(実験的、v7.4.0 で導入)</td><td> v7.1.0では、ワークロード間のリソースおよびstorageアクセスの干渉を軽減するために、<a href="https://docs.pingcap.com/tidb/v7.5/tidb-resource-control" target="_blank">リソース制御</a>機能が導入されました。TiDB v7.4.0では、この制御がバックグラウンドタスクの優先度にも適用されました。v7.4.0では、リソース制御が自動分析、バックアップと復元、 TiDB Lightningによるバルクロード、オンラインDDLといったバックグラウンドタスク実行の優先度を識別・管理するようになりました。将来のリリースでは、この制御は最終的にすべてのバックグラウンドタスクに適用される予定です。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v7.5/tidb-resource-control#manage-queries-that-consume-more-resources-than-expected-runaway-queries">暴走クエリを管理する</a>ためのリソース制御（実験的、v7.2.0 で導入）</td><td><a href="https://docs.pingcap.com/tidb/v7.5/tidb-resource-control" target="_blank">リソース制御は</a>、リソースグループごとにワークロードをリソース分離するためのフレームワークですが、個々のクエリが各グループ内の作業にどのような影響を与えるかについては考慮しません。TiDB v7.2.0では、「ランナウェイクエリ制御」が導入され、TiDBがリソースグループごとにこれらのクエリを識別および処理する方法を制御できるようになりました。必要に応じて、長時間実行クエリは終了または抑制される可能性があり、クエリは正確なSQLテキスト、SQLダイジェスト、またはプランダイジェストによって識別されるため、より汎用化されます。v7.3.0では、TiDBはデータベースレベルのSQLブロックリストと同様に、既知の不正なクエリをプロアクティブに監視できるようになりました。</td></tr><tr><td> SQL</td><td> MySQL 8.0 との互換性 (v7.4.0 で導入)</td><td> MySQL 8.0 では、デフォルトの文字セットは utf8mb4 で、utf8mb4 のデフォルトの照合照合順序は<code>utf8mb4_0900_ai_ci</code>です。TiDB v7.4.0 でこれに対するサポートが追加されたことで、MySQL 8.0 との互換性が向上し、デフォルトの照合順序を持つ MySQL 8.0 データベースからの移行とレプリケーションがよりスムーズになりました。</td></tr><tr><td rowspan="4"> DB操作と可観測性</td><td>TiDB Lightning の物理インポート モードが<a href="https://docs.pingcap.com/tidb/v7.5/sql-statement-import-into"><code>IMPORT INTO</code></a> (GA) で TiDB に統合されました</td><td>v7.2.0より前は、ファイルシステムに基づいてデータをインポートするには、 <a href="https://docs.pingcap.com/tidb/v7.5/tidb-lightning-overview">TiDB Lightning</a>をインストールし、その物理インポートモードを使用する必要がありました。現在、同じ機能が<code>IMPORT INTO</code>ステートメントに統合されているため、追加のツールをインストールすることなく、このステートメントを使用して迅速にデータをインポートできます。また、このステートメントは並列インポート用の<a href="https://docs.pingcap.com/tidb/v7.5/tidb-distributed-execution-framework" target="_blank">Distributed eXecution Framework（DXF）</a>をサポートしており、大規模なインポート時のインポート効率が向上します。</td></tr><tr><td> <code>ADD INDEX</code>および<code>IMPORT INTO</code> SQL ステートメントを実行するための<a href="https://docs.pingcap.com/tidb/v7.5/system-variables#tidb_service_scope-new-in-v740" target="_blank">それぞれの TiDB ノード</a>を指定します (GA)</td><td> <code>ADD INDEX</code>または<code>IMPORT INTO</code> SQL 文を、既存の TiDB ノードの一部、または新規に追加された TiDB ノードに対して実行するかどうかを柔軟に指定できます。このアプローチにより、他の TiDB ノードからのリソース分離が可能になり、業務への影響を防ぎながら、先行する SQL 文の実行に最適なパフォーマンスを確保できます。v7.5.0 では、この機能が一般提供 (GA) されます。</td></tr><tr><td> DDL は<a href="https://docs.pingcap.com/tidb/v7.5/ddl-introduction#ddl-related-commands">一時停止と再開の操作</a>をサポートします (GA)</td><td>インデックスの追加はリソースを大量に消費し、オンライントラフィックに影響を与える可能性があります。リソースグループ内で制限されている場合やラベル付きノードに分離されている場合でも、緊急時にはこれらのジョブを一時停止する必要があるかもしれません。v7.2.0以降、TiDBはこれらのバックグラウンドジョブを任意の数だけ同時に一時停止することをネイティブにサポートし、ジョブのキャンセルと再開を回避しながら必要なリソースを解放します。</td></tr><tr><td> TiDBダッシュボードはTiKVのヒーププロファイリングをサポート<a href="https://docs.pingcap.com/tidb/v7.5/dashboard-profiling" target="_blank"></a></td><td>これまで、TiKV OOM や高メモリ使用量の問題に対処するには、インスタンス環境で<code>jeprof</code>を手動で実行してヒーププロファイルを生成する必要がありました。v7.5.0 以降、TiKV はヒーププロファイルのリモート処理に対応しました。ヒーププロファイルのフレームグラフとコールグラフに直接アクセスできるようになりました。この機能は、Go ヒーププロファイリングと同様にシンプルで使いやすいエクスペリエンスを提供します。</td></tr></tbody></table>

## 機能の詳細 {#feature-details}

### スケーラビリティ {#scalability}

-   分散実行フレームワーク (DXF) が有効な場合に、 `ADD INDEX`または`IMPORT INTO`タスクを分散実行するための TiDB ノードの指定と分離をサポート[＃46258](https://github.com/pingcap/tidb/issues/46258) @ [ywqzzy](https://github.com/ywqzzy)

    リソースを大量に消費するクラスターで`ADD INDEX`または`IMPORT INTO`タスクを並列実行すると、TiDBノードのリソースを大量に消費し、クラスターのパフォーマンス低下につながる可能性があります。既存のサービスへのパフォーマンスへの影響を回避するため、v7.4.0では、システム変数[`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740)実験的機能として導入し、 [TiDB 分散実行フレームワーク (DXF)](/tidb-distributed-execution-framework.md)の配下にある各TiDBノードのサービススコープを制御します。複数の既存のTiDBノードを選択するか、新しいTiDBノードにTiDBサービススコープを設定することで、分散実行されるすべての`ADD INDEX`および`IMPORT INTO`タスクがこれらのノードでのみ実行されます。v7.5.0では、この機能が一般提供（GA）されます。

    詳細については[ドキュメント](/system-variables.md#tidb_service_scope-new-in-v740)参照してください。

### パフォーマンス {#performance}

-   TiDB分散実行フレームワーク（DXF）が一般提供（GA）され、並列実行[＃45719](https://github.com/pingcap/tidb/issues/45719) @ [wjhuang2016](https://github.com/wjhuang2016)における`ADD INDEX`および`IMPORT INTO`タスクのパフォーマンスと安定性が向上しました。

    v7.1.0で導入されたDXFがGAになりました。TiDB v7.1.0より前のバージョンでは、DDLタスクを同時に実行できるのは1つのTiDBノードのみでした。v7.1.0以降では、DXFの下で複数のTiDBノードが同じDDLタスクを並列実行できるようになりました。v7.2.0以降では、DXFは複数のTiDBノードが同じ`IMPORT INTO`タスクを並列実行することをサポートします。これにより、TiDBクラスターのリソースをより有効に活用し、DDLと`IMPORT INTO`タスクのパフォーマンスを大幅に向上させることができます。さらに、TiDBノードを増やすことで、これらのタスクのパフォーマンスを線形的に向上させることもできます。

    DXF を使用するには、 [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710)値を`ON`に設定します。

    ```sql
    SET GLOBAL tidb_enable_dist_task = ON;
    ```

    詳細については[ドキュメント](/tidb-global-sort.md)参照してください。

-   単一のSQL文で複数のインデックスを追加するパフォーマンスを向上する[＃41602](https://github.com/pingcap/tidb/issues/41602) @ [接線](https://github.com/tangenta)

    v7.5.0より前では、単一のSQL文で複数のインデックス（ `ADD INDEX` ）を追加する場合、パフォーマンスは別々のSQL文で複数のインデックスを追加する場合と同程度でした。v7.5.0以降では、単一のSQL文で複数のインデックスを追加する場合のパフォーマンスが大幅に向上しました。特に幅の広いテーブルを扱うシナリオでは、内部テストデータによるとパフォーマンスが最大94%向上することが示されています。

### DB操作 {#db-operations}

-   DDL ジョブは一時停止と再開操作をサポートします (GA) [＃18015](https://github.com/pingcap/tidb/issues/18015) @ [ゴドゥム](https://github.com/godouxm)

    バージョン7.2.0で導入されたDDLジョブの一時停止および再開操作が一般提供（GA）されました。これらの操作により、リソースを大量に消費するDDLジョブ（インデックス作成など）を一時停止してリソースを節約し、オンライントラフィックへの影響を最小限に抑えることができます。リソースに余裕があれば、DDLジョブをキャンセルして再開することなく、シームレスに再開できます。この機能により、リソース使用率が向上し、ユーザーエクスペリエンスが向上し、スキーマ変更プロセスが簡素化されます。

    `ADMIN PAUSE DDL JOBS`または`ADMIN RESUME DDL JOBS`を使用して複数の DDL ジョブを一時停止および再開できます。

    ```sql
    ADMIN PAUSE DDL JOBS 1,2;
    ADMIN RESUME DDL JOBS 1,2;
    ```

    詳細については[ドキュメント](/best-practices/ddl-introduction.md#ddl-related-commands)参照してください。

-   BRは統計情報のバックアップと復元をサポートします[＃48008](https://github.com/pingcap/tidb/issues/48008) @ [リーヴルス](https://github.com/Leavrth)

    TiDB v7.5.0以降、brコマンドラインツールにデータベース統計のバックアップと復元のためのパラメータ`--ignore-stats`が導入されました。このパラメータを`false`に設定すると、brコマンドラインツールは列、インデックス、およびテーブルの統計のバックアップと復元をサポートします。この場合、バックアップから復元されたTiDBデータベースの統計収集タスクを手動で実行したり、自動収集タスクの完了を待ったりする必要はありません。この機能により、データベースのメンテナンス作業が簡素化され、クエリパフォーマンスが向上します。

    詳細については[ドキュメント](/br/br-snapshot-manual.md#back-up-statistics)参照してください。

### 可観測性 {#observability}

-   TiDBダッシュボードはTiKV [＃15927](https://github.com/tikv/tikv/issues/15927) @ [コナー1996](https://github.com/Connor1996)のヒーププロファイリングをサポートします

    以前は、TiKV OOM や高メモリ使用量の問題に対処するには、通常、インスタンス環境でヒーププロファイルを生成するために`jeprof`手動で実行する必要がありました。v7.5.0 以降、TiKV はヒーププロファイルのリモート処理を可能にします。ヒーププロファイルのフレームグラフとコールグラフに直接アクセスできるようになりました。この機能は、Go ヒーププロファイリングと同様にシンプルで使いやすいエクスペリエンスを提供します。

    詳細については[ドキュメント](/dashboard/dashboard-profiling.md)参照してください。

### データ移行 {#data-migration}

-   `IMPORT INTO` SQL文（GA） [＃46704](https://github.com/pingcap/tidb/issues/46704) @ [D3ハンター](https://github.com/D3Hunter)をサポート

    v7.5.0では、 `IMPORT INTO` SQL文が一般提供（GA）されます。この文はTiDB Lightningの[物理インポートモード](/tidb-lightning/tidb-lightning-physical-import-mode.md)機能を統合し、CSV、SQL、PARQUETなどの形式のデータをTiDBの空のテーブルに迅速にインポートできます。このインポート方法により、TiDB Lightningを個別に導入・管理する必要がなくなり、データインポートの複雑さが軽減され、インポート効率が大幅に向上します。

    詳細については[ドキュメント](/sql-statements/sql-statement-import-into.md)参照してください。

-   データ移行（DM）は、互換性のない（データの一貫性を損なう）DDL変更[＃9692](https://github.com/pingcap/tiflow/issues/9692) @ [GMHDBJD](https://github.com/GMHDBJD)のブロックをサポートします。

    v7.5.0より前のDM Binlog Filter機能は、指定されたイベントのみを移行またはフィルタリングすることができ、粒度も比較的粗いものでした。例えば、 `ALTER`のような大きな粒度のDDLイベントのみをフィルタリングできます。この方法は、一部のシナリオでは制限があります。例えば、アプリケーションは`ADD COLUMN`許可しますが`DROP COLUMN`許可しませんが、以前のDMバージョンではどちらも`ALTER`イベントでフィルタリングされます。

    このような問題に対処するため、v7.5.0では、サポートされるDDLイベントの粒度を改良しました。例えば、 `MODIFY COLUMN` . 列のデータ型の変更、 `DROP COLUMN` . フィルタリングのサポート、その他、データ損失、データの切り捨て、精度の低下につながるきめ細かいDDLイベントなどです。必要に応じて設定できます。この機能は、互換性のないDDL変更をブロックし、そのような変更に対してエラーを報告することもサポートしているため、下流のアプリケーションデータへの影響を回避するために、適切なタイミングで手動で介入することができます。

    詳細については[ドキュメント](/dm/dm-binlog-event-filter.md#parameter-descriptions)参照してください。

-   継続的なデータ検証のためのリアルタイムチェックポイント更新をサポート[＃8463](https://github.com/pingcap/tiflow/issues/8463) @ [リチュンジュ](https://github.com/lichunzhu)

    v7.5.0より前のバージョンでは、 [継続的なデータ検証機能](/dm/dm-continuous-data-validation.md)はDMから下流へのレプリケーション中にデータの整合性を確保していました。これは、上流データベースからTiDBへのビジネストラフィックのカットオーバーの基盤として機能します。しかし、レプリケーションの遅延や不整合データの再検証待ちなど、様々な要因により、継続的検証チェックポイントは数分ごとに更新する必要がありました。これは、カットオーバー時間が数十秒に制限されている一部のビジネスシナリオでは許容されません。

    継続的なデータ検証のためのチェックポイントのリアルタイム更新の導入により、上流データベースからbinlogの位置を取得できるようになりました。継続的検証プログラムは、このbinlogの位置をメモリ内で検出すると、数分ごとに更新するのではなく、即座にチェックポイントを更新します。そのため、この即時更新されたチェックポイントに基づいて、迅速にカットオフ操作を実行できます。

    詳細については[ドキュメント](/dm/dm-continuous-data-validation.md#set-the-cutover-point-for-continuous-data-validation)参照してください。

## 互換性の変更 {#compatibility-changes}

> **注記：**
>
> このセクションでは、v7.4.0から最新バージョン（v7.5.0）にアップグレードする際に知っておくべき互換性の変更点について説明します。v7.3.0以前のバージョンから最新バージョンにアップグレードする場合は、中間バージョンで導入された互換性の変更点も確認する必要があるかもしれません。

### システム変数 {#system-variables}

| 変数名                                                                                                               | タイプを変更   | 説明                                                                                           |
| ----------------------------------------------------------------------------------------------------------------- | -------- | -------------------------------------------------------------------------------------------- |
| [`tidb_enable_fast_analyze`](/system-variables.md#tidb_enable_fast_analyze)                                       | 非推奨      | 統計`Fast Analyze`機能を有効にするかどうかを制御します。この機能はバージョン7.5.0で非推奨となりました。                                |
| [`tidb_analyze_partition_concurrency`](/system-variables.md#tidb_analyze_partition_concurrency)                   | 修正済み     | さらにテストを行った後、デフォルト値を`1`から`2`に変更します。                                                           |
| [`tidb_build_stats_concurrency`](/system-variables.md#tidb_build_stats_concurrency)                               | 修正済み     | さらにテストを行った後、デフォルト値を`4`から`2`に変更します。                                                           |
| [`tidb_merge_partition_stats_concurrency`](/system-variables.md#tidb_merge_partition_stats_concurrency)           | 修正済み     | このシステム変数はバージョン7.5.0以降で有効になります。TiDBがパーティションテーブルを分析する際に、パーティションテーブルの統計情報をマージする際の同時実行性を指​​定します。 |
| [`tidb_build_sampling_stats_concurrency`](/system-variables.md#tidb_build_sampling_stats_concurrency-new-in-v750) | 新しく追加された | `ANALYZE`プロセスのサンプリング同時実行を制御します。                                                              |
| [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-new-in-v750)   | 新しく追加された | この変数は、OOM の問題を回避するために統計を非同期的にマージするために TiDB によって使用されます。                                       |
| [`tidb_gogc_tuner_max_value`](/system-variables.md#tidb_gogc_tuner_max_value-new-in-v750)                         | 新しく追加された | GOGC チューナーが調整できる GOGC の最大値を制御します。                                                            |
| [`tidb_gogc_tuner_min_value`](/system-variables.md#tidb_gogc_tuner_min_value-new-in-v750)                         | 新しく追加された | GOGC チューナーが調整できる GOGC の最小値を制御します。                                                            |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーションパラメータ                                                                                                                    | タイプを変更   | 説明                                                                                                                            |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------- |
| ティドブ           | [`tikv-client.copr-req-timeout`](/tidb-configuration-file.md#copr-req-timeout-new-in-v750)                                         | 新しく追加された | 単一のコプロセッサー要求のタイムアウトを設定します。                                                                                                    |
| TiKV           | [`raftstore.inspect-interval`](/tikv-configuration-file.md#inspect-interval)                                                       | 修正済み     | 低速ノード検出の感度を向上させるためにアルゴリズムを最適化した後、デフォルト値を`500ms`から`100ms`に変更します。                                                               |
| TiKV           | [`raftstore.region-compact-min-redundant-rows`](/tikv-configuration-file.md#region-compact-min-redundant-rows-new-in-v710)         | 修正済み     | RocksDBのコンパクションをトリガーするために必要な冗長MVCC行数を設定します。v7.5.0以降、この設定項目は`"raft-kv"`storageエンジンに適用されます。                                     |
| TiKV           | [`raftstore.region-compact-redundant-rows-percent`](/tikv-configuration-file.md#region-compact-redundant-rows-percent-new-in-v710) | 修正済み     | RocksDBのコンパクションをトリガーするために必要な冗長MVCC行の割合を設定します。v7.5.0以降、この設定項目は`"raft-kv"`storageエンジンに適用されます。                                   |
| TiKV           | [`raftstore.evict-cache-on-memory-ratio`](/tikv-configuration-file.md#evict-cache-on-memory-ratio-new-in-v750)                     | 新しく追加された | TiKV のメモリ使用量がシステム使用可能メモリの 90% を超え、 Raftエントリ キャッシュが占有するメモリが使用メモリの`evict-cache-on-memory-ratio`超えると、TiKV はRaftエントリ キャッシュを削除します。 |
| TiKV           | [`memory.enable-heap-profiling`](/tikv-configuration-file.md#enable-heap-profiling-new-in-v750)                                    | 新しく追加された | TiKV のメモリ使用量を追跡するためにヒープ プロファイリングを有効にするかどうかを制御します。                                                                             |
| TiKV           | [`memory.profiling-sample-per-bytes`](/tikv-configuration-file.md#profiling-sample-per-bytes-new-in-v750)                          | 新しく追加された | ヒープ プロファイリングによって毎回サンプリングされるデータの量を、最も近い 2 の累乗に切り上げて指定します。                                                                      |
| BR             | [`--ignore-stats`](/br/br-snapshot-manual.md#back-up-statistics)                                                                   | 新しく追加された | データベース統計のバックアップと復元を行うかどうかを制御します。このパラメータを`false`に設定すると、br コマンドラインツールは列、インデックス、およびテーブルの統計のバックアップと復元をサポートします。                    |
| TiCDC          | [`case-sensitive`](/ticdc/ticdc-changefeed-config.md)                                                                              | 修正済み     | さらにテストを行った後、デフォルト値を`true`から`false`に変更します。つまり、TiCDC 構成ファイル内のテーブル名とデータベース名は、デフォルトで大文字と小文字が区別されません。                              |
| TiCDC          | [`sink.dispatchers.partition`](/ticdc/ticdc-changefeed-config.md)                                                                  | 修正済み     | TiCDC が Kafka パーティションに増分データをディスパッチする方法を制御します。v7.5.0 では、明示的に指定された列値を使用してパーティション番号を計算する新しい値オプション`columns`が導入されました。              |
| TiCDC          | [`changefeed-error-stuck-duration`](/ticdc/ticdc-changefeed-config.md)                                                             | 新しく追加された | 内部エラーまたは例外が発生したときに、変更フィードが自動的に再試行できる期間を制御します。                                                                                 |
| TiCDC          | [`encoding-worker-num`](/ticdc/ticdc-changefeed-config.md)                                                                         | 新しく追加された | やり直しモジュール内のエンコードおよびデコード ワーカーの数を制御します。                                                                                         |
| TiCDC          | [`flush-worker-num`](/ticdc/ticdc-changefeed-config.md)                                                                            | 新しく追加された | 再実行モジュール内のフラッシュワーカーの数を制御します。                                                                                                  |
| TiCDC          | [`sink.column-selectors`](/ticdc/ticdc-changefeed-config.md)                                                                       | 新しく追加された | 増分データをディスパッチするときに TiCDC が Kafka に送信するデータ変更イベントの指定された列を制御します。                                                                  |
| TiCDC          | [`sql-mode`](/ticdc/ticdc-changefeed-config.md)                                                                                    | 新しく追加された | TiCDCがDDL文を解析する際に使用するSQLモードを指定します。デフォルト値はTiDBのデフォルトのSQLモードと同じです。                                                              |
| TiDB Lightning | `--importer`                                                                                                                       | 削除済み     | バージョン 7.5.0 で非推奨となった TiKV インポーターのアドレスを指定します。                                                                                  |

## オフラインパッケージの変更 {#offline-package-changes}

v7.5.0 以降、 `TiDB-community-toolkit` [バイナリパッケージ](/binary-package.md)から以下のコンテンツが削除されます。

-   `tikv-importer-{version}-linux-{arch}.tar.gz`
-   `mydumper`
-   `spark-{version}-any-any.tar.gz`
-   `tispark-{version}-any-any.tar.gz`

## 非推奨の機能 {#deprecated-features}

-   [マイダンパー](https://docs.pingcap.com/tidb/v4.0/mydumper-overview)はバージョン7.5.0で非推奨となり、その機能の大部分は[Dumpling](/dumpling-overview.md)に置き換えられました。MydumperではなくDumplingを使用することを強くお勧めします。

-   TiKVインポーターはv7.5.0で非推奨となりました。代替として[TiDB Lightningの物理インポートモード](/tidb-lightning/tidb-lightning-physical-import-mode.md)使用することを強くお勧めします。

-   TiDB v7.5.0以降、 [TiDBBinlog](https://docs.pingcap.com/tidb/v7.5/tidb-binlog-overview)のデータレプリケーション機能のテクニカルサポートは提供されなくなりました。データレプリケーションの代替ソリューションとして、 [TiCDC](/ticdc/ticdc-overview.md)使用することを強くお勧めします。TiDB Binlog v7.5.0はポイントインタイムリカバリ（PITR）シナリオを引き続きサポートしていますが、このコンポーネントは将来のバージョンで完全に廃止される予定です。データリカバリの代替ソリューションとして、 [PITR](/br/br-pitr-guide.md)使用することを推奨します。

-   統計の[`Fast Analyze`](/system-variables.md#tidb_enable_fast_analyze)機能 (実験的) は、v7.5.0 で非推奨になりました。

-   統計の[増分コレクション](https://docs.pingcap.com/tidb/v7.4/statistics#incremental-collection)機能 (実験的) は、v7.5.0 で非推奨になりました。

## 改善点 {#improvements}

-   ティドブ

    -   グローバル統計情報のマージにおける同時実行モデルを最適化します[`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-new-in-v750)導入することで、統計情報の同時ロードとマージが可能になり、パーティションテーブルにおけるグローバル統計情報の生成速度が向上します。グローバル統計情報のマージにおけるメモリ使用量を最適化し、OOM（オブジェクトメモリオーバーヘッド）を回避し、メモリ割り当てを削減します[＃47219](https://github.com/pingcap/tidb/issues/47219) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   `ANALYZE`プロセスを最適化します。3 [`tidb_build_sampling_stats_concurrency`](/system-variables.md#tidb_build_sampling_stats_concurrency-new-in-v750)導入することで、 `ANALYZE`並行処理をより適切に制御し、リソース消費を削減します。7 `ANALYZE`メモリ使用量を最適化してメモリ割り当てを削減し、中間結果を再利用することで頻繁なGCを回避します[＃47275](https://github.com/pingcap/tidb/issues/47275) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   配置ポリシーの使用を最適化します。ポリシーの範囲をグローバルに設定できるようにし、一般的なシナリオの構文サポートを改善しました[＃45384](https://github.com/pingcap/tidb/issues/45384) @ [ノルーシュ](https://github.com/nolouch)
    -   `tidb_ddl_enable_fast_reorg`有効にした状態でのインデックス追加パフォーマンスを向上しました。社内テストでは、v7.5.0 は v6.5.0 と比較して最大 62.5% のパフォーマンス向上を確認しました[＃47757](https://github.com/pingcap/tidb/issues/47757) @ [接線](https://github.com/tangenta)

-   TiKV

    -   Titan マニフェストファイルを書き込むときにミューテックスを保持しないようにして、他のスレッドに影響を与えないようにします[＃15351](https://github.com/tikv/tikv/issues/15351) @ [コナー1996](https://github.com/Connor1996)

-   PD

    -   `evict-slow-trend`スケジューラ[＃7156](https://github.com/tikv/pd/issues/7156) @ [LykxSassinato](https://github.com/LykxSassinator)の安定性と使いやすさを向上

-   ツール

    -   バックアップと復元 (BR)

        -   スナップショットバックアップ用の新しいテーブル間バックアップパラメータ`table-concurrency`を追加します。このパラメータは、統計バックアップやデータ検証などのメタ情報のテーブル間同時実行を制御するために使用されます[＃48571](https://github.com/pingcap/tidb/issues/48571) @ [3ポイントシュート](https://github.com/3pointer)
        -   スナップショットバックアップの復元中に、 BRは特定のネットワークエラーが発生すると再試行します[＃48528](https://github.com/pingcap/tidb/issues/48528) @ [リーヴルス](https://github.com/Leavrth)

## バグ修正 {#bug-fixes}

-   ティドブ

    -   非整数クラスター化インデックス[＃47350](https://github.com/pingcap/tidb/issues/47350) @ [接線](https://github.com/tangenta)でのテーブル分割操作を禁止する
    -   タイムゾーン情報が正しくない時間フィールドをエンコードする問題を修正[＃46033](https://github.com/pingcap/tidb/issues/46033) @ [接線](https://github.com/tangenta)
    -   ソート演算子がスピルプロセス中に TiDB をクラッシュさせる可能性がある問題を修正[＃47538](https://github.com/pingcap/tidb/issues/47538) @ [ウィンドトーカー](https://github.com/windtalker)
    -   TiDBが`GROUP_CONCAT` [＃41957](https://github.com/pingcap/tidb/issues/41957) @ [アイリンキッド](https://github.com/AilinKid)のクエリに対して`Can't find column`返す問題を修正
    -   `batch-client` in `client-go` [＃47691](https://github.com/pingcap/tidb/issues/47691) @ [crazycs520](https://github.com/crazycs520)のpanic問題を修正
    -   `INDEX_LOOKUP_HASH_JOIN` [＃47788](https://github.com/pingcap/tidb/issues/47788) @ [シーライズ](https://github.com/SeaRise)のメモリ使用量の見積もりが間違っている問題を修正
    -   長期間オフラインであったTiFlashノードの再参加によって発生するワークロードの不均一性の問題を修正[＃35418](https://github.com/pingcap/tidb/issues/35418) @ [ウィンドトーカー](https://github.com/windtalker)
    -   HashJoin演算子がプローブ[＃48082](https://github.com/pingcap/tidb/issues/48082) @ [wshwsh12](https://github.com/wshwsh12)を実行するときにチャンクを再利用できない問題を修正しました
    -   `COALESCE()`関数が`DATE`の型パラメータ[＃46475](https://github.com/pingcap/tidb/issues/46475) @ [xzhangxian1008](https://github.com/xzhangxian1008)に対して誤った結果型を返す問題を修正しました
    -   サブクエリを含む`UPDATE`ステートメントが PointGet [＃48171](https://github.com/pingcap/tidb/issues/48171) @ [ハイ・ラスティン](https://github.com/Rustin170506)に誤って変換される問題を修正しました
    -   キャッシュされた実行プランに日付型と`unix_timestamp` [＃48165](https://github.com/pingcap/tidb/issues/48165) @ [qw4990](https://github.com/qw4990)の比較が含まれている場合に誤った結果が返される問題を修正しました。
    -   集計関数またはウィンドウ関数を含むデフォルトのインライン共通テーブル式 (CTE) が再帰 CTE [＃47881](https://github.com/pingcap/tidb/issues/47881) @ [エルサ0520](https://github.com/elsa0520)によって参照されるとエラーが報告される問題を修正しました
    -   ウィンドウ関数[＃46177](https://github.com/pingcap/tidb/issues/46177) @ [qw4990](https://github.com/qw4990)によって導入されたソートを削減するために、オプティマイザが誤って IndexFullScan を選択する問題を修正しました。
    -   CTE [＃47881](https://github.com/pingcap/tidb/issues/47881) @ [ウィノロス](https://github.com/winoros)の条件プッシュダウンにより、CTE への複数の参照が誤った結果をもたらす問題を修正しました。
    -   MySQL 圧縮プロトコルが大量のデータ (&gt;=16M) を処理できない問題を修正[＃47152](https://github.com/pingcap/tidb/issues/47152) [＃47157](https://github.com/pingcap/tidb/issues/47157) [＃47161](https://github.com/pingcap/tidb/issues/47161) @ [ドヴェーデン](https://github.com/dveeden)
    -   TiDBが`systemd` [＃47442](https://github.com/pingcap/tidb/issues/47442) @ [ホーキングレイ](https://github.com/hawkingrei)で起動したときに`cgroup`リソース制限を読み取らない問題を修正

-   TiKV

    -   悲観的トランザクションモードで事前書き込み要求を再試行すると、まれにデータの不整合が発生するリスクがある問題を修正しました[＃11187](https://github.com/tikv/tikv/issues/11187) @ [ミョンケミンタ](https://github.com/MyonKeminta)

-   PD

    -   `evict-leader-scheduler` [HuSharp](https://github.com/HuSharp)で構成[＃6897](https://github.com/tikv/pd/issues/6897)を失う可能性がある問題を修正
    -   ストアがオフラインになった後、その統計の監視メトリックが削除されない問題を修正[＃7180](https://github.com/tikv/pd/issues/7180) @ [rleungx](https://github.com/rleungx)
    -   配置ルールの設定が複雑な場合、データレプリケーション自動同期（DR自動同期）モードを採用しているクラスタで`canSync`と`hasMajority`誤って計算される可能性がある問題を修正しました[＃7201](https://github.com/tikv/pd/issues/7201) @ [ディスク](https://github.com/disksing)
    -   ルールチェッカーが配置ルール[＃7185](https://github.com/tikv/pd/issues/7185) @ [ノルーシュ](https://github.com/nolouch)の設定に従って学習者を追加しない問題を修正しました
    -   TiDBダッシュボードがPD `trace`データを正しく読み取れない問題を修正[＃7253](https://github.com/tikv/pd/issues/7253) @ [ノルーシュ](https://github.com/nolouch)
    -   内部的に取得された空の領域[＃7261](https://github.com/tikv/pd/issues/7261) @ [lhy1024](https://github.com/lhy1024)により PD がpanic可能性がある問題を修正しました
    -   データレプリケーション自動同期（DR自動同期）モードを採用しているクラスタで`available_stores`誤って計算される問題を修正[＃7221](https://github.com/tikv/pd/issues/7221) @ [ディスク](https://github.com/disksing)
    -   TiKVノードが利用できない場合にPDが通常のピアを削除する可能性がある問題を修正[＃7249](https://github.com/tikv/pd/issues/7249) @ [lhy1024](https://github.com/lhy1024)
    -   大規模クラスタに複数の TiKV ノードを追加すると、TiKVハートビートレポートが遅くなったり停止したりする可能性がある問題を修正しました[＃7248](https://github.com/tikv/pd/issues/7248) @ [rleungx](https://github.com/rleungx)

-   TiFlash

    -   `UPPER()`と`LOWER()`関数が TiDB とTiFlash [＃7695](https://github.com/pingcap/tiflash/issues/7695) @ [ウィンドトーカー](https://github.com/windtalker)の間で矛盾した結果を返す問題を修正しました
    -   空のパーティションでクエリを実行するとクエリ失敗[＃8220](https://github.com/pingcap/tiflash/issues/8220) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)が発生する問題を修正しました
    -   TiFlashレプリカ[＃8217](https://github.com/pingcap/tiflash/issues/8217) @ [ホンユニャン](https://github.com/hongyunyan)を複製する際のテーブル作成失敗によって発生するpanic問題を修正しました

-   ツール

    -   バックアップと復元 (BR)

        -   PITRが`CREATE INDEX` DDL文[＃47482](https://github.com/pingcap/tidb/issues/47482) @ [リーヴルス](https://github.com/Leavrth)の復元をスキップする可能性がある問題を修正しました
        -   大規模なワイドテーブル[＃15714](https://github.com/tikv/tikv/issues/15714) @ [ユジュンセン](https://github.com/YuJuncen)をバックアップするときに、一部のシナリオでログバックアップが停止する可能性がある問題を修正しました。

    -   TiCDC

        -   オブジェクトストアシンク[＃10041](https://github.com/pingcap/tiflow/issues/10041) @ [チャールズ・チャン96](https://github.com/CharlesCheung96)にデータを複製するときに NFS ディレクトリにアクセスすることによって発生するパフォーマンスの問題を修正しました
        -   `claim-check`有効になっているときにstorageパスのスペルが間違っている問題を修正[＃10036](https://github.com/pingcap/tiflow/issues/10036) @ [3エースショーハンド](https://github.com/3AceShowHand)
        -   TiCDC のスケジュールが[＃9845](https://github.com/pingcap/tiflow/issues/9845) @ [3エースショーハンド](https://github.com/3AceShowHand)でバランスが取れないケースがある問題を修正しました
        -   Kafka [＃9855](https://github.com/pingcap/tiflow/issues/9855) @ [ヒック](https://github.com/hicqu)にデータを複製するときに TiCDC が停止する可能性がある問題を修正しました
        -   TiCDCプロセッサが場合によってはpanic可能性がある問題を修正[＃9849](https://github.com/pingcap/tiflow/issues/9849) [＃9915](https://github.com/pingcap/tiflow/issues/9915) @ [ヒック](https://github.com/hicqu) @ [3エースショーハンド](https://github.com/3AceShowHand)
        -   `kv-client.enable-multiplexing`を有効にするとレプリケーションタスクが[＃9673](https://github.com/pingcap/tiflow/issues/9673) @ [フビンズ](https://github.com/fubinzh)で停止する問題を修正しました
        -   REDOログが有効な場合にNFS障害によりオーナーノードが停止する問題を修正[＃9886](https://github.com/pingcap/tiflow/issues/9886) @ [3エースショーハンド](https://github.com/3AceShowHand)

## パフォーマンステスト {#performance-test}

TiDB v7.5.0 のパフォーマンスについては、 TiDB Cloud Dedicated クラスターの[TPC-Cパフォーマンステストレポート](https://docs.pingcap.com/tidbcloud/v7.5.0-performance-benchmarking-with-tpcc)と[Sysbenchパフォーマンステストレポート](https://docs.pingcap.com/tidbcloud/v7.5.0-performance-benchmarking-with-sysbench)を参照してください。

## 寄稿者 {#contributors}

TiDB コミュニティの以下の貢献者に感謝いたします。

-   [jgrande](https://github.com/jgrande) (初回投稿者)
-   [ショーン0915](https://github.com/shawn0915)
