---
title: TiDB 7.4.0 Release Notes
summary: TiDB 7.4.0 の新機能、互換性の変更、改善、バグ修正について説明します。
---

# TiDB 7.4.0 リリースノート {#tidb-7-4-0-release-notes}

発売日: 2023年10月12日

TiDB バージョン: 7.4.0

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v7.4/quick-start-with-tidb)

7.4.0 では、次の主要な機能と改善が導入されています。

<table><thead><tr><th>カテゴリ</th><th>特徴</th><th>説明</th></tr></thead><tbody><tr><td rowspan="3">信頼性と可用性</td><td><a href="https://docs.pingcap.com/tidb/v7.4/tidb-global-sort" target="_blank">グローバルソート</a>による<code>IMPORT INTO</code>および<code>ADD INDEX</code>操作のパフォーマンスと安定性を向上 (実験的)</td><td> v7.4.0 より前では、 <a href="https://docs.pingcap.com/tidb/v7.4/tidb-distributed-execution-framework" target="_blank">TiDB Distributed eXecution Framework (DXF)</a>を使用した<code>ADD INDEX</code>や<code>IMPORT INTO</code>などのタスクは、ローカライズされた部分的なソートを意味し、最終的には TiKV が部分的なソートを補うために多くの追加作業を実行することになりました。また、これらのジョブでは、TiKV にロードする前に、TiDB ノードがソート用のローカル ディスク領域を割り当てる必要がありました。<br/> v7.4.0 で導入されたグローバル ソート機能により、データは TiKV にロードされる前にグローバル ソートのために一時的に外部共有storage(このバージョンでは S3) に保存されます。これにより、TiKV が余分なリソースを消費する必要がなくなり、 <code>ADD INDEX</code>や<code>IMPORT INTO</code>などの操作のパフォーマンスと安定性が大幅に向上します。</td></tr><tr><td>バックグラウンドタスクの<a href="https://docs.pingcap.com/tidb/v7.4/tidb-resource-control#manage-background-tasks" target="_blank">リソース制御</a>（実験的）</td><td> v7.1.0 では、ワークロード間のリソースとstorageのアクセスの干渉を軽減するために、 <a href="https://docs.pingcap.com/tidb/v7.4/tidb-resource-control#use-resource-control-to-achieve-resource-isolation" target="_blank">リソース制御</a>機能が導入されました。TiDB v7.4.0 では、この制御がバックグラウンド タスクにも適用されます。v7.4.0 では、リソース制御によって、自動分析、バックアップと復元、 TiDB Lightningによる一括ロード、オンライン DDL などのバックグラウンド タスクによって生成されたリソースが識別および管理されるようになりました。これは、最終的にはすべてのバックグラウンド タスクに適用されます。</td></tr><tr><td> TiFlash は<a href="https://docs.pingcap.com/tidb/v7.4/tiflash-disaggregated-and-s3" target="_blank">ストレージとコンピューティングの分離と S3</a> (GA) をサポートします</td><td>TiFlash分散storageおよびコンピューティングアーキテクチャと S3 共有storageが一般提供開始:<ul><li> TiFlash のコンピューティングとstorageを分離します。これは、弾力的な HTAP リソース利用のマイルストーンです。</li><li>低コストで共有storageを提供できる S3 ベースのstorageエンジンの使用をサポートします。</li></ul></td></tr><tr><td rowspan="2">構文</td><td>TiDBは<a href="https://docs.pingcap.com/tidb/v7.4/partitioned-table#convert-a-partitioned-table-to-a-non-partitioned-table" target="_blank">パーティションタイプの管理</a>をサポート</td><td>v7.4.0 より前では、範囲/リスト パーティション テーブルは、 <code>TRUNCATE</code> 、 <code>EXCHANGE</code> 、 <code>ADD</code> 、 <code>DROP</code> 、 <code>REORGANIZE</code>などのパーティション管理操作をサポートし、ハッシュ/キー パーティション テーブルは、 <code>ADD</code>や<code>COALESCE</code>などのパーティション管理操作をサポートします。<p>現在、TiDB は次のパーティション タイプ管理操作もサポートしています。</p><ul><li>パーティションテーブルを非パーティションテーブルに変換する</li><li>既存のパーティション化されていないテーブルをパーティション化する</li><li>既存のテーブルのパーティションタイプを変更する</li></ul></td></tr><tr><td>MySQL 8.0 互換性: <a href="https://docs.pingcap.com/tidb/v7.4/character-set-and-collation#character-sets-and-collations-supported-by-tidb" target="_blank">照合順序<code>utf8mb4_0900_ai_ci</code></a>サポート</td><td>MySQL 8.0 の注目すべき変更点の 1 つは、デフォルトの文字セットが utf8mb4 になり、 utf8mb4 のデフォルトの照合照合順序が<code>utf8mb4_0900_ai_ci</code>になったことです。TiDB v7.4.0 でこれに対するサポートが追加されたことで、MySQL 8.0 との互換性が向上し、デフォルトの照合順序を持つ MySQL 8.0 データベースからの移行とレプリケーションがよりスムーズになりました。</td></tr><tr><td> DB 操作と可観測性</td><td><code>IMPORT INTO</code>および<code>ADD INDEX</code> SQL ステートメントを実行するための<a href="https://docs.pingcap.com/tidb/v7.4/system-variables#tidb_service_scope-new-in-v740" target="_blank">それぞれの TiDB ノード</a>を指定します (実験的)</td><td>既存の TiDB ノードまたは新しく追加された TiDB ノードの一部で<code>IMPORT INTO</code>または<code>ADD INDEX</code> SQL ステートメントを実行するかどうかを柔軟に指定できます。このアプローチにより、残りの TiDB ノードからのリソースの分離が可能になり、ビジネス オペレーションへの影響を防ぎながら、前述の SQL ステートメントを実行するための最適なパフォーマンスを確保できます。</td></tr></tbody></table>

## 機能の詳細 {#feature-details}

### スケーラビリティ {#scalability}

-   分散実行フレームワーク (DXF) のバックエンド`ADD INDEX`または`IMPORT INTO`タスクを並列実行するための TiDB ノードの選択をサポート (実験的) [＃46453](https://github.com/pingcap/tidb/pull/46453) @ [うわー](https://github.com/ywqzzy)

    リソースを大量に消費するクラスターで`ADD INDEX`または`IMPORT INTO`タスクを並列に実行すると、大量の TiDB ノード リソースが消費され、クラスターのパフォーマンスが低下する可能性があります。v7.4.0 以降では、システム変数[`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740)使用して、 [TiDB 分散実行フレームワーク (DXF)](/tidb-distributed-execution-framework.md)の下にある各 TiDB ノードのサービス スコープを制御できます。複数の既存の TiDB ノードを選択するか、新しい TiDB ノードの TiDB サービス スコープを設定すると、すべての並列`ADD INDEX`および`IMPORT INTO`タスクがこれらのノードでのみ実行されます。このメカニズムにより、既存のサービスへのパフォーマンスへの影響を回避できます。

    詳細については[ドキュメント](/system-variables.md#tidb_service_scope-new-in-v740)参照してください。

-   パーティション化されたRaft KVstorageエンジンを強化する (実験的) [＃11515](https://github.com/tikv/tikv/issues/11515) [＃12842](https://github.com/tikv/tikv/issues/12842) @ [忙しいカケス](https://github.com/busyjay) @ [トニー](https://github.com/tonyxuqqi) @ [タボキ](https://github.com/tabokie) @ [バッファフライ](https://github.com/bufferflies) @ [5kbpsの](https://github.com/5kbpers) @ [スペードA-タン](https://github.com/SpadeA-Tang) @ [ノルーシュ](https://github.com/nolouch)

    TiDB v6.6.0 では、実験的機能としてパーティション化されたRaft KVstorageエンジンが導入されました。このエンジンは、複数の RocksDB インスタンスを使用して TiKVリージョンデータを保存し、各リージョンのデータは個別の RocksDB インスタンスに独立して保存されます。

    v7.4.0 では、TiDB は Partitioned Raft KVstorageエンジンの互換性と安定性をさらに向上させました。大規模データ テストを通じて、DM、 Dumpling、 TiDB Lightning、TiCDC、 BR、PITR などの TiDB エコシステム ツールおよび機能との互換性が確保されています。さらに、Partitioned Raft KVstorageエンジンは、読み取りと書き込みが混在するワークロードでより安定したパフォーマンスを提供するため、書き込みが多いシナリオに特に適しています。さらに、各 TiKV ノードは 8 コア CPU をサポートし、8 TB のデータstorageと 64 GB のメモリで構成できるようになりました。

    詳細については[ドキュメント](/partitioned-raft-kv.md)参照してください。

-   TiFlashは分散storageおよびコンピューティングアーキテクチャ（GA）をサポートします[＃6882](https://github.com/pingcap/tiflash/issues/6882) @ [ジェイソン・ファン](https://github.com/JaySon-Huang) @ [ジンヘリン](https://github.com/JinheLin) @ [そよ風のような](https://github.com/breezewish) @ [リデズ](https://github.com/lidezhu) @ [カルビンネオ](https://github.com/CalvinNeo) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)

    v7.0.0 では、 TiFlash は分散storageおよびコンピューティングアーキテクチャを実験的機能として導入します。一連の改善により、 TiFlashの分散storageおよびコンピューティングアーキテクチャは、v7.4.0 から GA になります。

    このアーキテクチャでは、 TiFlashノードは 2 種類 (コンピューティング ノードと書き込みノード) に分かれており、S3 API と互換性のあるオブジェクトstorageをサポートします。両方の種類のノードは、コンピューティングまたはstorage容量を個別に拡張できます。分散storageおよびコンピューティングアーキテクチャでは、 TiFlashレプリカの作成、データのクエリ、オプティマイザー ヒントの指定など、結合storageおよびコンピューティングアーキテクチャと同じようにTiFlash を使用できます。

    TiFlash の**分散storageおよびコンピューティングアーキテクチャ**と**結合storageおよびコンピューティングアーキテクチャは、**同じクラスター内で使用したり、相互に変換したりすることはできないことに注意してください。TiFlashをデプロイするときに、使用するアーキテクチャを構成できます。

    詳細については[ドキュメント](/tiflash/tiflash-disaggregated-and-s3.md)参照してください。

### パフォーマンス {#performance}

-   JSON 演算子`MEMBER OF`を TiKV [＃46307](https://github.com/pingcap/tidb/issues/46307) @ [うわー](https://github.com/wshwsh12)にプッシュダウンするサポート

    -   `value MEMBER OF(json_array)`

    詳細については[ドキュメント](/functions-and-operators/expressions-pushed-down.md)参照してください。

-   任意のフレーム定義タイプのウィンドウ関数をTiFlash [＃7376](https://github.com/pingcap/tiflash/issues/7376) @ [翻訳者](https://github.com/xzhangxian1008)にプッシュダウンするサポート

    v7.4.0 より前のTiFlashでは、 `PRECEDING`または`FOLLOWING`含むウィンドウ関数はサポートされておらず、そのようなフレーム定義を含むすべてのウィンドウ関数をTiFlashにプッシュダウンすることはできません。v7.4.0 以降では、 TiFlash はすべてのウィンドウ関数のフレーム定義をサポートします。この機能は自動的に有効になり、フレーム定義を含むウィンドウ関数は、関連する要件が満たされると、自動的にTiFlashにプッシュダウンされて実行されます。

-   クラウド ストレージ ベースのグローバル ソート機能を導入して、並列実行における`ADD INDEX`および`IMPORT INTO`タスクのパフォーマンスと安定性を向上します (実験的) [＃45719](https://github.com/pingcap/tidb/issues/45719) @ [翻訳:](https://github.com/wjhuang2016)

    v7.4.0 より前では、Distributed eXecution Framework (DXF) で`ADD INDEX`や`IMPORT INTO`などのタスクを実行する場合、各 TiDB ノードは、エンコードされたインデックス KV ペアとテーブル データ KV ペアをソートするために、大量のローカル ディスク領域を割り当てる必要があります。ただし、グローバル ソート機能がないため、プロセス中に異なる TiDB ノード間および各ノード内でデータが重複する可能性があります。その結果、TiKV はこれらの KV ペアをstorageエンジンにインポートしながら、常に圧縮操作を実行する必要があり、 `ADD INDEX`と`IMPORT INTO`のパフォーマンスと安定性に影響します。

    v7.4.0 では、TiDB に[グローバルソート](/tidb-global-sort.md)機能が導入されました。エンコードされたデータをローカルに書き込んでそこでソートする代わりに、データはクラウドstorageに書き込まれ、グローバル ソートされるようになりました。ソートされると、インデックス データとテーブル データの両方が TiKV に並行してインポートされるため、パフォーマンスと安定性が向上します。

    詳細については[ドキュメント](/tidb-global-sort.md)参照してください。

-   非準備済みステートメントの実行プランのキャッシュをサポート (GA) [＃36598](https://github.com/pingcap/tidb/issues/36598) @ [qw4990](https://github.com/qw4990)

    TiDB v7.0.0 では、同時実行 OLTP の負荷容量を向上させるための実験的機能として、非準備プラン キャッシュが導入されています。v7.4.0 では、この機能が GA になります。実行プラン キャッシュはより多くのシナリオに適用され、TiDB の同時実行処理容量が向上します。

    準備されていないプラン キャッシュを有効にすると、追加のメモリと CPU オーバーヘッドが発生する可能性があり、すべての状況に適しているとは限りません。v7.4.0 以降では、この機能はデフォルトで無効になっています。1 [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache)使用して有効にし、 [`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-new-in-v710)使用してキャッシュ サイズを制御できます。

    さらに、この機能はデフォルトでは DML 文をサポートしておらず、SQL 文には一定の制限があります。詳細については、 [制限](/sql-non-prepared-plan-cache.md#restrictions)参照してください。

    詳細については[ドキュメント](/sql-non-prepared-plan-cache.md)参照してください。

### 信頼性 {#reliability}

-   TiFlashはクエリレベルのデータスピルをサポート[＃7738](https://github.com/pingcap/tiflash/issues/7738) @ [風の話し手](https://github.com/windtalker)

    v7.0.0 以降、 TiFlash は`GROUP BY` 、 `ORDER BY` 、 `JOIN` 3 つの演算子のデータ スピルの制御をサポートしています。この機能により、データ サイズが使用可能なメモリを超えた場合に、クエリの終了やシステム クラッシュなどの問題が回避されます。ただし、演​​算子ごとにスピルを個別に管理するのは面倒で、全体的なリソース制御には効果がありません。

    v7.4.0 では、 TiFlashにクエリ レベルのデータ スピルが導入されています。TiFlash ノードでのクエリのメモリ制限を[`tiflash_mem_quota_query_per_node`](/system-variables.md#tiflash_mem_quota_query_per_node-new-in-v740)に設定し、データ スピルをトリガーするメモリ比率を[`tiflash_query_spill_ratio`](/system-variables.md#tiflash_query_spill_ratio-new-in-v740)に設定することで、クエリのメモリ使用量を簡単に管理し、 TiFlashメモリリソースをより適切に制御できます。

    詳細については[ドキュメント](/tiflash/tiflash-spill-disk.md)参照してください。

-   ユーザー定義の TiKV 読み取りタイムアウト[＃45380](https://github.com/pingcap/tidb/issues/45380) @ [クレイジーcs520](https://github.com/crazycs520)をサポート

    通常、TiKV は数ミリ秒という非常に高速にリクエストを処理します。ただし、TiKV ノードでディスク I/O ジッターまたはネットワークレイテンシーが発生すると、リクエストの処理時間が大幅に長くなる可能性があります。v7.4.0 より前のバージョンでは、TiKV リクエストのタイムアウト制限は固定されており、調整できません。そのため、TiKV ノードで問題が発生すると、TiDB は固定期間のタイムアウト応答を待機する必要があり、ジッター発生時のアプリケーション クエリ パフォーマンスに顕著な影響が生じます。

    TiDB v7.4.0 では、新しいシステム変数[`tikv_client_read_timeout`](/system-variables.md#tikv_client_read_timeout-new-in-v740)が導入され、クエリで TiDB が TiKV に送信する RPC 読み取り要求のタイムアウトをカスタマイズできるようになりました。つまり、TiKV ノードに送信された要求がディスクまたはネットワークの問題により遅延した場合、TiDB はより早くタイムアウトして他の TiKV ノードに要求を再送信できるため、クエリのレイテンシーが短縮されます。すべての TiKV ノードでタイムアウトが発生した場合、TiDB はデフォルトのタイムアウトを使用して再試行します。さらに、クエリでオプティマイザーヒント`/*+ SET_VAR(TIKV_CLIENT_READ_TIMEOUT=N) */`使用して、TiDB が TiKV RPC 読み取り要求を送信するタイムアウトを設定することもできます。この機能強化により、不安定なネットワークまたはstorage環境に適応する柔軟性が TiDB に与えられ、クエリのパフォーマンスが向上し、ユーザーエクスペリエンスが強化されます。

    詳細については[ドキュメント](/system-variables.md#tikv_client_read_timeout-new-in-v740)参照してください。

-   オプティマイザヒント[＃45892](https://github.com/pingcap/tidb/issues/45892) @ [ウィノロス](https://github.com/winoros)を使用して、一部のシステム変数値を一時的に変更することをサポートします。

    TiDB v7.4.0 では、MySQL 8.0 と同様のオプティマイザヒント`SET_VAR()`が導入されています。SQL 文にヒント`SET_VAR()`を含めることで、文の実行中にシステム変数の値を一時的に変更できます。これにより、さまざまな文の環境を設定できます。たとえば、リソースを大量に消費する SQL 文の並列処理を積極的に増やしたり、変数を通じてオプティマイザの動作を変更したりできます。

    変更できるシステム変数は、ヒント`SET_VAR()`の[システム変数](/system-variables.md)で確認できます。予期しない動作が発生する可能性があるため、明示的にサポートされていない変数を変更しないことを強くお勧めします。

    詳細については[ドキュメント](/optimizer-hints.md)参照してください。

-   TiFlashはリソース制御[＃7660](https://github.com/pingcap/tiflash/issues/7660) @ [グオシャオゲ](https://github.com/guo-shaoge)をサポート

    TiDB v7.1.0 では、リソース制御機能が一般提供され、TiDB と TiKV のリソース管理機能が提供されます。v7.4.0 では、 TiFlashがリソース制御機能をサポートし、TiDB の全体的なリソース管理機能が向上します。TiFlash のTiFlash制御は既存の TiDB リソース制御機能と完全に互換性があり、既存のリソース グループは TiDB、TiKV、およびTiFlashのリソースを同時に管理します。

    TiFlashリソース制御機能を有効にするかどうかを制御するには、 TiFlashパラメータ`enable_resource_control`を設定します。この機能を有効にすると、 TiFlash はTiDB のリソース グループ設定に基づいてリソースのスケジュールと管理を実行し、全体的なリソースの適切な割り当てと使用を保証します。

    詳細については[ドキュメント](/tidb-resource-control.md)参照してください。

-   TiFlashはパイプライン実行モデル（GA） [＃6518](https://github.com/pingcap/tiflash/issues/6518) @ [シーライズ](https://github.com/SeaRise)をサポートします

    v7.2.0 以降、 TiFlash はパイプライン実行モデルを導入しています。このモデルは、すべてのスレッド リソースを集中管理し、タスク実行を均一にスケジュールすることで、リソースの過剰使用を回避しながらスレッド リソースの使用率を最大化します。v7.4.0 では、 TiFlash はスレッド リソース使用状況の統計を改善し、パイプライン実行モデルは GA 機能となり、デフォルトで有効になっています。この機能はTiFlashリソース制御機能と相互に依存しているため、TiDB v7.4.0 では、以前のバージョンでパイプライン実行モデルを有効にするかどうかを制御するために使用されていた変数`tidb_enable_tiflash_pipeline_model`が削除されています。代わりに、 TiFlashパラメータ`tidb_enable_resource_control`を構成することで、パイプライン実行モデルとTiFlashリソース制御機能を有効または無効にすることができます。

    詳細については[ドキュメント](/tiflash/tiflash-pipeline-model.md)参照してください。

-   オプティマイザモード[＃46080](https://github.com/pingcap/tidb/issues/46080) @ [時間と運命](https://github.com/time-and-fate)のオプションを追加

    v7.4.0 では、TiDB に新しいシステム変数[`tidb_opt_objective`](/system-variables.md#tidb_opt_objective-new-in-v740)が導入され、オプティマイザが使用する推定方法を制御しま す。デフォルト値`moderate` 、データの変更に基づいて推定を調整するために実行時統計を使用するという、オプティマイザの以前の動作を維持します。この変数を`determinate`に設定すると、オプティマイザは実行時修正を考慮せずに、統計のみに基づいて実行プランを生成します。

    長期にわたって安定した OLTP アプリケーションの場合、または既存の実行プランに自信がある場合は、テスト後に`determinate`モードに切り替えることをお勧めします。これにより、プランの変更の可能性が減ります。

    詳細については[ドキュメント](/system-variables.md#tidb_opt_objective-new-in-v740)参照してください。

-   TiDB リソース制御はバックグラウンドタスクの管理をサポートします (実験的) [＃44517](https://github.com/pingcap/tidb/issues/44517) @ [栄光](https://github.com/glorv)

    データ バックアップや自動統計収集などのバックグラウンド タスクは、優先度は低いですが、多くのリソースを消費します。これらのタスクは通常、定期的または不定期にトリガーされます。実行中は多くのリソースを消費するため、オンラインの高優先度タスクのパフォーマンスに影響します。v7.4.0 以降、TiDB リソース制御機能はバックグラウンド タスクの管理をサポートします。この機能により、オンライン アプリケーションに対する低優先度タスクのパフォーマンスへの影響が軽減され、合理的なリソース割り当てが可能になり、クラスターの安定性が大幅に向上します。

    TiDB は次の種類のバックグラウンド タスクをサポートします。

    -   `lightning` : [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)または[`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)使用してインポート タスクを実行します。
    -   `br` : [BR](/br/backup-and-restore-overview.md)使用してバックアップおよび復元タスクを実行します。PITR はサポートされていません。
    -   `ddl` : Reorg DDL のバッチ データ書き戻しフェーズ中のリソース使用量を制御します。
    -   `stats` : 手動で実行されるか、TiDB によって自動的にトリガーされる[統計を収集する](/statistics.md#collect-statistics)タスク。

    デフォルトでは、バックグラウンド タスクとしてマークされているタスク タイプは空で、バックグラウンド タスクの管理は無効になっています。このデフォルトの動作は、TiDB v7.4.0 より前のバージョンと同じです。バックグラウンド タスクを管理するには、 `default`リソース グループのバックグラウンド タスク タイプを手動で変更する必要があります。

    詳細については[ドキュメント](/tidb-resource-control.md#manage-background-tasks)参照してください。

-   ロック統計が一般公開 (GA) される[＃46351](https://github.com/pingcap/tidb/issues/46351) @ [ハイラスティン](https://github.com/Rustin170506)

    v7.4.0 では、 [ロック統計](/statistics.md#lock-statistics)一般提供されました。運用上のセキュリティを確保するために、統計のロックとロック解除には、統計の収集と同じ権限が必要です。さらに、TiDB は特定のパーティションの統計のロックとロック解除をサポートしており、柔軟性が向上しています。データベース内のクエリと実行プランに自信があり、変更が発生しないようにしたい場合は、統計をロックして安定性を高めることができます。

    詳細については[ドキュメント](/statistics.md#lock-statistics)参照してください。

-   テーブル[＃46695](https://github.com/pingcap/tidb/issues/46695) @ [コーダープレイ](https://github.com/coderplay)のハッシュ結合を選択するかどうかを制御するシステム変数を導入します。

    MySQL 8.0 では、新しい機能としてテーブルのハッシュ結合が導入されています。この機能は主に、比較的大きな 2 つのテーブルと結果セットを結合するために使用されます。ただし、トランザクション ワークロードや、 MySQL 5.7で実行される一部のアプリケーションでは、テーブルのハッシュ結合によってパフォーマンス リスクが生じる可能性があります。MySQL では、ハッシュ結合をグローバル レベルとセッション レベルのどちらで選択するかを制御する[`optimizer_switch`](https://dev.mysql.com/doc/refman/8.0/en/switchable-optimizations.html#optflag_block-nested-loop)が提供されています。

    v7.4.0 以降、TiDB では、テーブルのハッシュ結合を制御するためのシステム変数[`tidb_opt_enable_hash_join`](/system-variables.md#tidb_opt_enable_hash_join-new-in-v656-v712-and-v740)導入されています。これはデフォルトで有効になっています ( `ON` )。実行プランでテーブル間のハッシュ結合を選択する必要がないことが確実な場合は、変数を`OFF`に変更して、実行プランのロールバックの可能性を減らし、システムの安定性を向上させることができます。

    詳細については[ドキュメント](/system-variables.md#tidb_opt_enable_hash_join-new-in-v656-v712-and-v740)参照してください。

### 構文 {#sql}

-   TiDBはパーティションタイプの管理[＃42728](https://github.com/pingcap/tidb/issues/42728) @ [ミョンス](https://github.com/mjonss)をサポートします

    v7.4.0 より前では、TiDB のパーティション テーブルのパーティション タイプを変更することはできませんでした。v7.4.0 以降、TiDB はパーティション テーブルを非パーティション テーブルに、または非パーティション テーブルをパーティション テーブルに変更すること、およびパーティション タイプの変更をサポートします。したがって、パーティションテーブルのパーティション タイプと数を柔軟に調整できるようになりました。たとえば、 `ALTER TABLE t PARTITION BY ...`ステートメントを使用してパーティション タイプを変更できます。

    詳細については[ドキュメント](/partitioned-table.md#convert-a-partitioned-table-to-a-non-partitioned-table)参照してください。

-   TiDBは`ROLLUP`修飾子と`GROUPING`関数[＃44487](https://github.com/pingcap/tidb/issues/44487) @ [アイリンキッド](https://github.com/AilinKid)の使用をサポートしています

    `WITH ROLLUP`修飾子と`GROUPING`関数は、多次元データ要約のデータ分析でよく使用されます。v7.4.0 以降では、 `GROUP BY`節で`WITH ROLLUP`修飾子と`GROUPING`関数を使用できます。たとえば、 `SELECT ... FROM ... GROUP BY ... WITH ROLLUP`構文で`WITH ROLLUP`修飾子を使用できます。

    詳細については[ドキュメント](/functions-and-operators/group-by-modifier.md)参照してください。

### DB操作 {#db-operations}

-   照合照合順序`utf8mb4_0900_ai_ci`と`utf8mb4_0900_bin` [＃37566](https://github.com/pingcap/tidb/issues/37566) @ [ヤンケオ](https://github.com/YangKeao) @ [ジムララ](https://github.com/zimulala) @ [bb7133](https://github.com/bb7133)をサポート

    TiDB v7.4.0 では、MySQL 8.0 からのデータ移行のサポートが強化され、 `utf8mb4_0900_ai_ci`と`utf8mb4_0900_bin` 2 つの照合順序が追加されました。 `utf8mb4_0900_ai_ci` MySQL 8.0 のデフォルトの照合照合順序です。

    TiDB v7.4.0 では、MySQL 8.0 と互換性のあるシステム変数`default_collation_for_utf8mb4`も導入されています。これにより、utf8mb4 文字セットのデフォルトの照合順序を指定できるようになり、 MySQL 5.7以前のバージョンからの移行やデータ複製との互換性が確保されます。

    詳細については[ドキュメント](/character-set-and-collation.md#character-sets-and-collations-supported-by-tidb)参照してください。

### 可観測性 {#observability}

-   ログへのセッション接続 ID とセッション エイリアスの追加をサポート[＃46071](https://github.com/pingcap/tidb/issues/46071) @ [lcwangchao](https://github.com/lcwangchao)

    SQL 実行の問題をトラブルシューティングする場合、多くの場合、根本原因を特定するために TiDBコンポーネントログの内容を相関させる必要があります。v7.4.0 以降、TiDB はセッション接続 ID ( `CONNECTION_ID` ) をセッション関連ログ (TiDB ログ、スロー クエリ ログ、TiKV のコプロセッサからのスロー ログなど) に書き込むことができます。セッション接続 ID に基づいて複数の種類のログの内容を相関させることで、トラブルシューティングと診断の効率を向上させることができます。

    さらに、セッション レベルのシステム変数[`tidb_session_alias`](/system-variables.md#tidb_session_alias-new-in-v740)を設定することで、上記のログにカスタム識別子を追加できます。ログにアプリケーション識別情報を挿入するこの機能により、ログの内容とアプリケーションを関連付け、アプリケーションからログへのリンクを構築し、診断の難易度を軽減できます。

-   TiDBダッシュボードは、テーブルビューでの実行プランの表示をサポートしています[＃1589](https://github.com/pingcap/tidb-dashboard/issues/1589) @ [バウリン](https://github.com/baurine)

    v7.4.0 では、TiDB ダッシュボードは、診断エクスペリエンスを向上させるために、**スロー クエリ ページ**と**SQL ステートメント**ページで実行プランをテーブル ビューで表示することをサポートしています。

    詳細については[ドキュメント](/dashboard/dashboard-statement-details.md)参照してください。

### データ移行 {#data-migration}

-   `IMPORT INTO`機能を[＃46704](https://github.com/pingcap/tidb/issues/46704) @ [D3ハンター](https://github.com/D3Hunter)強化

    v7.4.0 以降では、 `IMPORT INTO`ステートメントに`CLOUD_STORAGE_URI`オプションを追加して[グローバルソート](/tidb-global-sort.md)機能 (実験的) を有効にし、インポートのパフォーマンスと安定性を向上させることができます。7 `CLOUD_STORAGE_URI`では、エンコードされたデータのクラウドstorageアドレスを指定できます。

    さらに、v7.4.0 では、 `IMPORT INTO`機能に次の機能が導入されています。

    -   `Split_File`オプションの構成をサポートします。これにより、大きな CSV ファイルを複数の 256 MiB の小さな CSV ファイルに分割して並列処理し、インポート パフォーマンスを向上させることができます。
    -   圧縮された CSV および SQL ファイルのインポートをサポートします。サポートされている圧縮形式には、 `.gzip` 、 `.gz` 、 `.zstd` 、 `.zst` 、 `.snappy`が含まれます。

    詳細については[ドキュメント](/sql-statements/sql-statement-import-into.md)参照してください。

-   Dumpling は、データを CSV ファイルにエクスポートするときにユーザー定義のターミネータをサポートします[＃46982](https://github.com/pingcap/tidb/issues/46982) @ [GMHDBJD](https://github.com/GMHDBJD)

    v7.4.0 より前のバージョンでは、 Dumpling はデータを CSV ファイルにエクスポートするときに行末文字として`"\r\n"`使用します。その結果、行末文字として`"\n"`のみを認識する特定の下流システムでは、エクスポートされた CSV ファイルを解析できないか、ファイルを解析する前にサードパーティ製の変換ツールを使用する必要があります。

    v7.4.0 以降、 Dumpling は新しいパラメータ`--csv-line-terminator`を導入します。このパラメータを使用すると、データを CSV ファイルにエクスポートするときに、必要なターミネータを指定できます。このパラメータは`"\r\n"`と`"\n"`サポートします。以前のバージョンとの一貫性を保つために、デフォルトのターミネータは`"\r\n"`です。

    詳細については[ドキュメント](/dumpling-overview.md#option-list-of-dumpling)参照してください。

-   TiCDCはPulsar [＃9413](https://github.com/pingcap/tiflow/issues/9413) @ [ヤムチャイナ](https://github.com/yumchina) @ [アズドンメン](https://github.com/asddongmen)へのデータ複製をサポートします

    Pulsar は、リアルタイム データ ストリーミング エクスペリエンスを大幅に強化するクラウド ネイティブの分散メッセージ ストリーミング プラットフォームです。v7.4.0 以降、TiCDC は変更データを`canal-json`形式で Pulsar に複製し、Pulsar とのシームレスな統合を実現します。この機能により、TiCDC は TiDB の変更を簡単にキャプチャして Pulsar に複製する機能を提供し、データ処理と分析機能に新たな可能性をもたらします。特定のビジネス ニーズを満たすために、Pulsar から新しく生成された変更データを読み取って処理する独自のコンシューマー アプリケーションを開発できます。

    詳細については[ドキュメント](/ticdc/ticdc-sink-to-pulsar.md)参照してください。

<!---->

-   TiCDC はクレームチェックパターン[＃9153](https://github.com/pingcap/tiflow/issues/9153) @ [3エースショーハンド](https://github.com/3AceShowHand)で大きなメッセージの処理を改善します

    v7.4.0 より前のバージョンでは、TiCDC は Kafka の最大メッセージ サイズ ( `max.message.bytes` ) を超える大きなメッセージをダウンストリームに送信できませんでした。v7.4.0 以降では、Kafka をダウンストリームとして変更フィードを構成するときに、大きなメッセージを格納する外部storageの場所を指定し、外部storage内の大きなメッセージのアドレスを含む参照メッセージを Kafka に送信できます。コンシューマーがこの参照メッセージを受信すると、外部storageアドレスからメッセージ コンテンツを取得できます。

    詳細については[ドキュメント](/ticdc/ticdc-sink-to-kafka.md#send-large-messages-to-external-storage)参照してください。

## 互換性の変更 {#compatibility-changes}

> **注記：**
>
> このセクションでは、v7.3.0 から現在のバージョン (v7.4.0) にアップグレードするときに知っておく必要のある互換性の変更について説明します。v7.2.0 以前のバージョンから現在のバージョンにアップグレードする場合は、中間バージョンで導入された互換性の変更も確認する必要がある可能性があります。

### 行動の変化 {#behavior-changes}

-   v7.4.0 以降、TiDB は MySQL 8.0 の重要な機能と互換性があり、 `version()` `8.0.11`で始まるバージョンを返します。

-   TiFlashを以前のバージョンから v7.4.0 にアップグレードした後は、元のバージョンへのインプレース ダウングレードはサポートされません。これは、v7.4 以降、 TiFlash がPageStorage V3 のデータ圧縮ロジックを最適化して、データ圧縮中に生成される読み取りおよび書き込み増幅を削減し、基礎となるstorageファイル名の一部が変更されるためです。

-   TSO タイムスタンプの論理部分を抽出できるように[`TIDB_PARSE_TSO_LOGICAL()`](/functions-and-operators/tidb-functions.md#tidb-specific-functions)関数が追加されました。

-   MySQL 8.0 との互換性を向上させるために[`information_schema.CHECK_CONSTRAINTS`](/information-schema/information-schema-check-constraints.md)テーブルが追加されました。

-   複数の変更を含むトランザクションの場合、更新イベントで主キーまたは null 以外の一意のインデックス値が変更されると、TiCDC はイベントを削除イベントと挿入イベントに分割し、すべてのイベントが挿入イベントに先行する削除イベントのシーケンスに従うようにします。詳細については、 [ドキュメント](/ticdc/ticdc-split-update-behavior.md#transactions-containing-multiple-update-changes)参照してください。

### システム変数 {#system-variables}

| 変数名                                                                                                     | タイプを変更   | 説明                                                                                                                                                                                                                                                                                                                                                         |
| ------------------------------------------------------------------------------------------------------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `tidb_enable_tiflash_pipeline_model`                                                                    | 削除されました  | この変数は、 TiFlashパイプライン実行モデルを有効にするかどうかを制御するために使用されます。v7.4.0 以降では、 TiFlashリソース制御機能を有効にすると、 TiFlashパイプライン実行モデルが自動的に有効になります。                                                                                                                                                                                                                                     |
| [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache)       | 修正済み     | さらにテストを行った後、デフォルト値を`ON`から`OFF`に変更します。これは、準備されていない実行プラン キャッシュが無効であることを意味します。                                                                                                                                                                                                                                                                                |
| [`default_collation_for_utf8mb4`](/system-variables.md#default_collation_for_utf8mb4-new-in-v740)       | 新しく追加された | `utf8mb4`文字セットのデフォルトの照合順序を制御します。デフォルト値は`utf8mb4_bin`です。                                                                                                                                                                                                                                                                                                    |
| [`tidb_cloud_storage_uri`](/system-variables.md#tidb_cloud_storage_uri-new-in-v740)                     | 新しく追加された | 有効にするクラウドstorageURI を指定します[グローバルソート](/tidb-global-sort.md) 。                                                                                                                                                                                                                                                                                               |
| [`tidb_opt_enable_hash_join`](/system-variables.md#tidb_opt_enable_hash_join-new-in-v656-v712-and-v740) | 新しく追加された | オプティマイザがテーブルのハッシュ結合を選択するかどうかを制御します。デフォルトの値は`ON`です。 `OFF`に設定すると、他の実行プランが利用できない場合を除き、オプティマイザはテーブルのハッシュ結合を選択しません。                                                                                                                                                                                                                                             |
| [`tidb_opt_objective`](/system-variables.md#tidb_opt_objective-new-in-v740)                             | 新しく追加された | この変数は、オプティマイザの目的を制御します。1 `moderate` 、TiDB v7.4.0 より前のバージョンのデフォルトの動作を維持し、オプティマイザはより多くの情報を使用して、より優れた実行プランを生成しようとします`determinate`モードはより保守的になり、実行プランがより安定する傾向があります。                                                                                                                                                                                            |
| [`tidb_request_source_type`](/system-variables.md#tidb_request_source_type-new-in-v740)                 | 新しく追加された | 現在のセッションのタスク タイプを明示的に指定します。これは[リソース管理](/tidb-resource-control.md)によって識別および制御されます。例: `SET @@tidb_request_source_type = "background"` 。                                                                                                                                                                                                                      |
| [`tidb_schema_version_cache_limit`](/system-variables.md#tidb_schema_version_cache_limit-new-in-v740)   | 新しく追加された | この変数は、TiDB インスタンスにキャッシュできる履歴スキーマ バージョンの数を制限します。デフォルト値は`16`で、これは、TiDB がデフォルトで 16 個の履歴スキーマ バージョンをキャッシュすることを意味します。                                                                                                                                                                                                                                            |
| [`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740)                             | 新しく追加された | この変数はインスタンス レベルのシステム変数です。これを使用して、 [TiDB 分散実行フレームワーク (DXF)](/tidb-distributed-execution-framework.md)の下にある TiDB ノードのサービス スコープを制御できます。TiDB ノードの`tidb_service_scope` `background`に設定すると、DXF はその TiDB ノードが[`ADD INDEX`](/sql-statements/sql-statement-add-index.md)や[`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)などの DXF タスクを実行するようにスケジュールします。 |
| [`tidb_session_alias`](/system-variables.md#tidb_session_alias-new-in-v740)                             | 新しく追加された | 現在のセッションに関連するログ内の`session_alias`列目の値を制御します。                                                                                                                                                                                                                                                                                                                |
| [`tiflash_mem_quota_query_per_node`](/system-variables.md#tiflash_mem_quota_query_per_node-new-in-v740) | 新しく追加された | TiFlashノードでのクエリの最大メモリ使用量を制限します。クエリのメモリ使用量がこの制限を超えると、 TiFlash はエラーを返し、クエリを終了します。デフォルト値は`0`で、制限がないことを意味します。                                                                                                                                                                                                                                                  |
| [`tiflash_query_spill_ratio`](/system-variables.md#tiflash_query_spill_ratio-new-in-v740)               | 新しく追加された | TiFlash [クエリレベルのスピル](/tiflash/tiflash-spill-disk.md#query-level-spilling)のしきい値を制御します。デフォルト値は`0.7`です。                                                                                                                                                                                                                                                       |
| [`tikv_client_read_timeout`](/system-variables.md#tikv_client_read_timeout-new-in-v740)                 | 新しく追加された | クエリで TiKV RPC 読み取り要求を送信する TiDB のタイムアウトを制御します。デフォルト値`0`は、デフォルトのタイムアウト (通常は 40 秒) が使用されることを示します。                                                                                                                                                                                                                                                             |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーションパラメータ                                                                                                                         | タイプを変更   | 説明                                                                                                                                                                        |
| -------------- | --------------------------------------------------------------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ティビ            | [`enable-stats-cache-mem-quota`](/tidb-configuration-file.md#enable-stats-cache-mem-quota-new-in-v610)                                  | 修正済み     | デフォルト値は`false`から`true`に変更され、TiDB 統計のキャッシュのメモリ制限がデフォルトで有効になっていることを意味します。                                                                                                   |
| ティクヴ           | [`rocksdb.[defaultcf|writecf|lockcf].periodic-compaction-seconds`](/tikv-configuration-file.md#periodic-compaction-seconds-new-in-v720) | 修正済み     | デフォルト値が`"30d"`から`"0s"`に変更され、RocksDB の定期的な圧縮がデフォルトで無効になります。この変更により、TiDB のアップグレード後に大量の圧縮がトリガーされ、フロントエンドの読み取りおよび書き込みパフォーマンスに影響することがなくなります。                                   |
| ティクヴ           | [`rocksdb.[defaultcf|writecf|lockcf].ttl`](/tikv-configuration-file.md#ttl-new-in-v720)                                                 | 修正済み     | デフォルト値が`"30d"`から`"0s"`に変更され、SST ファイルは TTL によりデフォルトで圧縮をトリガーしなくなり、フロントエンドの読み取りおよび書き込みパフォーマンスに影響を与えなくなります。                                                                   |
| TiFlash        | [`flash.compact_log_min_gap`](/tiflash/tiflash-configuration.md)                                                                        | 新しく追加された | 現在のRaftステート マシンによって進められた`applied_index`と最後のディスク スピル時の`applied_index`とのギャップが`compact_log_min_gap`を超えると、 TiFlash はTiKV から`CompactLog`コマンドを実行し、データをディスクにスピルします。              |
| TiFlash        | [`profiles.default.enable_resource_control`](/tiflash/tiflash-configuration.md)                                                         | 新しく追加された | TiFlashリソース制御機能を有効にするかどうかを制御します。                                                                                                                                          |
| TiFlash        | [`storage.format_version`](/tiflash/tiflash-configuration.md)                                                                           | 修正済み     | デフォルト値を`4`から`5`に変更します。新しい形式では、小さいファイルを結合することで物理ファイルの数を減らすことができます。                                                                                                         |
| Dumpling       | [`--csv-line-terminator`](/dumpling-overview.md#option-list-of-dumpling)                                                                | 新しく追加された | CSV ファイルの希望するターミネータを指定します。このオプションは`"\r\n"`と`"\n"`サポートします。デフォルト値は`"\r\n"`で、以前のバージョンと一致しています。                                                                               |
| ティCDC          | [`claim-check-storage-uri`](/ticdc/ticdc-sink-to-kafka.md#send-large-messages-to-external-storage)                                      | 新しく追加された | `large-message-handle-option` `claim-check`に設定する場合、 `claim-check-storage-uri`有効な外部storageアドレスに設定する必要があります。そうしないと、変更フィードを作成するとエラーが発生します。                                   |
| ティCDC          | [`large-message-handle-compression`](/ticdc/ticdc-sink-to-kafka.md#ticdc-data-compression)                                              | 新しく追加された | エンコード中に圧縮を有効にするかどうかを制御します。デフォルト値は空で、有効になっていないことを意味します。                                                                                                                    |
| ティCDC          | [`large-message-handle-option`](/ticdc/ticdc-sink-to-kafka.md#send-large-messages-to-external-storage)                                  | 修正済み     | この設定項目は、新しい値`claim-check`を追加します。これを`claim-check`に設定すると、TiCDC Kafka シンクは、メッセージ サイズが制限を超えた場合にメッセージを外部storageに送信することをサポートし、外部storage内のこの大きなメッセージのアドレスを含むメッセージを Kafka に送信します。 |

## 廃止および削除された機能 {#deprecated-and-removed-features}

-   [マイダンパー](https://docs.pingcap.com/tidb/v4.0/mydumper-overview) v7.5.0 で廃止され、その機能のほとんどは[Dumpling](/dumpling-overview.md)に置き換えられました。mydumper の代わりにDumpling を使用することを強くお勧めします。
-   TiKV インポーターは v7.5.0 で廃止されます。代わりに[TiDB Lightningの物理インポートモード](/tidb-lightning/tidb-lightning-physical-import-mode.md)使用することを強くお勧めします。
-   TiCDC の`enable-old-value`パラメータが削除されます[＃9667](https://github.com/pingcap/tiflow/issues/9667) @ [3エースショーハンド](https://github.com/3AceShowHand)

## 改善点 {#improvements}

-   ティビ

    -   パーティションテーブル[＃47071](https://github.com/pingcap/tidb/issues/47071) [＃47104](https://github.com/pingcap/tidb/issues/47104) [＃46804](https://github.com/pingcap/tidb/issues/46804) @ [ホーキングレイ](https://github.com/hawkingrei)での`ANALYZE`操作のメモリ使用量とパフォーマンスを最適化します
    -   統計ガベージコレクションのメモリ使用量とパフォーマンスを最適化する[＃31778](https://github.com/pingcap/tidb/issues/31778) @ [ウィノロス](https://github.com/winoros)
    -   インデックスマージ交差のプッシュダウン`limit`を最適化してクエリパフォーマンス[＃46863](https://github.com/pingcap/tidb/issues/46863) @ [アイリンキッド](https://github.com/AilinKid)を向上させる
    -   `IndexLookup`多数のテーブル取得タスクが含まれる場合に、誤ってフルテーブルスキャンを選択する可能性を最小限に抑えるためにコストモデルを改善します[＃45132](https://github.com/pingcap/tidb/issues/45132) @ [qw4990](https://github.com/qw4990)
    -   結合除去ルールを最適化して、 `join on unique keys` [＃46248](https://github.com/pingcap/tidb/issues/46248) @ [修正DB](https://github.com/fixdb)のクエリパフォーマンスを向上させます。
    -   実行エラーを回避するために、複数値インデックス列の照合順序を`binary`に変更します[＃46717](https://github.com/pingcap/tidb/issues/46717) @ [ヤンケオ](https://github.com/YangKeao)

-   ティクヴ

    -   OOM [＃15458](https://github.com/tikv/tikv/issues/15458) @ [金星の上](https://github.com/overvenus)防ぐためにリゾルバのメモリ使用量を最適化します
    -   ルータオブジェクトのLRUCacheを排除してメモリ使用量を削減し、OOM [＃15430](https://github.com/tikv/tikv/issues/15430) @ [コナー1996](https://github.com/Connor1996)を防止します。
    -   TiCDC リゾルバ[＃15412](https://github.com/tikv/tikv/issues/15412) @ [金星の上](https://github.com/overvenus)のメモリ使用量を削減
    -   RocksDB 圧縮によるメモリ変動を軽減[＃15324](https://github.com/tikv/tikv/issues/15324) @ [金星の上](https://github.com/overvenus)
    -   Partitioned Raft KV [＃15269](https://github.com/tikv/tikv/issues/15269) @ [金星の上](https://github.com/overvenus)のフロー制御モジュールのメモリ消費を削減
    -   接続再試行のプロセスで PD クライアントのバックオフ メカニズムを追加します。これにより、エラー再試行中に再試行間隔が徐々に長くなり、PD の負荷が軽減されます[＃15428](https://github.com/tikv/tikv/issues/15428) @ [ノルーシュ](https://github.com/nolouch)
    -   RocksDB [＃15424](https://github.com/tikv/tikv/issues/15424) @ [栄光](https://github.com/glorv)の`background_compaction`動的に調整するサポート

-   PD

    -   TSO 関連の問題の調査を容易にするために TSO トレース情報を最適化します[＃6856](https://github.com/tikv/pd/pull/6856) @ [天菜まお](https://github.com/tiancaiamao)
    -   メモリ使用量を削減するために HTTP クライアント接続の再利用をサポート[＃6913](https://github.com/tikv/pd/issues/6913) @ [ノルーシュ](https://github.com/nolouch)
    -   バックアップ クラスタが切断されたときに PD がクラスタ ステータスを自動的に更新する速度を向上[＃6883](https://github.com/tikv/pd/issues/6883) @ [ディスク](https://github.com/disksing)
    -   リソース制御クライアントの構成取得方法を強化し、最新の構成を動的に取得する[＃7043](https://github.com/tikv/pd/issues/7043) @ [ノルーシュ](https://github.com/nolouch)

-   TiFlash

    -   TiFlash書き込みプロセスのスピルポリシーを最適化することで、ランダム書き込みワークロード中の書き込みパフォーマンスを向上します[＃7564](https://github.com/pingcap/tiflash/issues/7564) @ [カルビンネオ](https://github.com/CalvinNeo)
    -   TiFlash [＃8068](https://github.com/pingcap/tiflash/issues/8068) @ [カルビンネオ](https://github.com/CalvinNeo)のRaftレプリケーション プロセスに関するメトリックを追加します。
    -   ファイルシステムの inode [＃7595](https://github.com/pingcap/tiflash/issues/7595) @ [ホンユンヤン](https://github.com/hongyunyan)が枯渇するのを避けるために、小さなファイルの数を減らします。

-   ツール

    -   バックアップと復元 (BR)

        -   リージョンリーダーシップの移行が発生すると、PITR ログバックアップの進行のレイテンシーが長くなるという問題を緩和します[＃13638](https://github.com/tikv/tikv/issues/13638) @ [ユジュンセン](https://github.com/YuJuncen)
        -   HTTPクライアント[＃46011](https://github.com/pingcap/tidb/issues/46011) @ [リーヴルス](https://github.com/Leavrth)で`MaxIdleConns`と`MaxIdleConnsPerHost`パラメータを設定することにより、ログバックアップとPITRリストアタスクの接続再利用のサポートを強化します。
        -   PD または外部 S3storageへの接続に失敗した場合のBRのフォールト トレランスを向上[＃42909](https://github.com/pingcap/tidb/issues/42909) @ [リーヴルス](https://github.com/Leavrth)
        -   新しい復元パラメータ`WaitTiflashReady`を追加します。このパラメータを有効にすると、 TiFlashレプリカが正常に複製された後に復元操作が完了します[＃43828](https://github.com/pingcap/tidb/issues/43828) [＃46302](https://github.com/pingcap/tidb/issues/46302) @ [3ポインター](https://github.com/3pointer)
        -   ログバックアップのCPUオーバーヘッドを削減`resolve lock` [＃40759](https://github.com/pingcap/tidb/issues/40759) @ [3ポインター](https://github.com/3pointer)

    -   ティCDC

        -   `ADD INDEX` DDL操作を複製する実行ロジックを最適化して、後続のDMLステートメント[＃9644](https://github.com/pingcap/tiflow/issues/9644) @ [スドジ](https://github.com/sdojjy)をブロックしないようにします。

    -   TiDB Lightning

        -   リージョン分散フェーズ[＃46203](https://github.com/pingcap/tidb/issues/46203) @ [ミッタルリシャブ](https://github.com/mittalrishabh)中のTiDB Lightningの再試行ロジックを最適化します。
        -   データインポートフェーズ[＃46253](https://github.com/pingcap/tidb/issues/46253) @ [ランス6716](https://github.com/lance6716)中の`no leader`エラーに対するTiDB Lightningの再試行ロジックを最適化します。

## バグ修正 {#bug-fixes}

-   ティビ

    -   ハッシュパーティション化されていないテーブルに対して`BatchPointGet`演算子が誤った結果を返す問題を修正[＃45889](https://github.com/pingcap/tidb/issues/45889) @ [定義2014](https://github.com/Defined2014)
    -   ハッシュパーティションテーブル[＃46779](https://github.com/pingcap/tidb/issues/46779) @ [ジフハウス](https://github.com/jiyfhust)に対して`BatchPointGet`演算子が誤った結果を返す問題を修正しました。
    -   TiDBパーサーが状態のままになり、解析エラーが発生する問題を修正[＃45898](https://github.com/pingcap/tidb/issues/45898) @ [qw4990](https://github.com/qw4990)
    -   `EXCHANGE PARTITION`制約[＃45922](https://github.com/pingcap/tidb/issues/45922) @ [ミョンス](https://github.com/mjonss)をチェックしない問題を修正
    -   `tidb_enforce_mpp`システム変数が正しく復元できない問題を修正[＃46214](https://github.com/pingcap/tidb/issues/46214) @ [翻訳者](https://github.com/djshow832)
    -   `LIKE`節の`_`誤って処理される問題を修正[＃46287](https://github.com/pingcap/tidb/issues/46287) [＃46618](https://github.com/pingcap/tidb/issues/46618) @ [定義2014](https://github.com/Defined2014)
    -   TiDBがスキーマ[＃46325](https://github.com/pingcap/tidb/issues/46325) @ [ヒヒフフ](https://github.com/hihihuhu)取得に失敗した場合、 `schemaTs`が0に設定される問題を修正しました。
    -   `AUTO_ID_CACHE=1`が[＃46444](https://github.com/pingcap/tidb/issues/46444) @ [天菜まお](https://github.com/tiancaiamao)に設定されている場合に`Duplicate entry`発生する可能性がある問題を修正しました
    -   `AUTO_ID_CACHE=1`が[＃46454](https://github.com/pingcap/tidb/issues/46454) @ [天菜まお](https://github.com/tiancaiamao)に設定されている場合に、panic後に TiDB がゆっくりと回復する問題を修正しました。
    -   `AUTO_ID_CACHE=1`が[＃46545](https://github.com/pingcap/tidb/issues/46545) @ [天菜まお](https://github.com/tiancaiamao)に設定されている場合に`SHOW CREATE TABLE`の`next_row_id`が間違っている問題を修正しました
    -   サブクエリ[＃45838](https://github.com/pingcap/tidb/issues/45838) @ [翻訳者](https://github.com/djshow832)で CTE を使用すると解析中に発生するpanic問題を修正しました
    -   `EXCHANGE PARTITION`が失敗またはキャンセルされた場合に、パーティション化されたテーブルの制限が元のテーブルに残る問題を修正[＃45920](https://github.com/pingcap/tidb/issues/45920) [＃45791](https://github.com/pingcap/tidb/issues/45791) @ [ミョンス](https://github.com/mjonss)
    -   リストパーティションの定義で`NULL`と空の文字列[＃45694](https://github.com/pingcap/tidb/issues/45694) @ [ミョンス](https://github.com/mjonss)両方の使用がサポートされない問題を修正
    -   パーティション交換[＃46492](https://github.com/pingcap/tidb/issues/46492) @ [ミョンス](https://github.com/mjonss)中にパーティション定義に準拠していないデータを検出できない問題を修正
    -   `tmp-storage-quota`設定が有効にならない問題を修正[＃45161](https://github.com/pingcap/tidb/issues/45161) [＃26806](https://github.com/pingcap/tidb/issues/26806) @ [うわー](https://github.com/wshwsh12)
    -   `WEIGHT_STRING()`関数が照合順序[＃45725](https://github.com/pingcap/tidb/issues/45725) @ [ドヴェーデン](https://github.com/dveeden)と一致しない問題を修正しました
    -   インデックス結合のエラーによりクエリが停止する可能性がある問題を修正[＃45716](https://github.com/pingcap/tidb/issues/45716) @ [うわー](https://github.com/wshwsh12)
    -   `DATETIME`または`TIMESTAMP`列を数値定数[＃38361](https://github.com/pingcap/tidb/issues/38361) @ [いびん87](https://github.com/yibin87)と比較するときに動作が MySQL と一致しない問題を修正しました。
    -   符号なし型を`Duration`型定数[＃45410](https://github.com/pingcap/tidb/issues/45410) @ [うわー](https://github.com/wshwsh12)と比較したときに発生する誤った結果を修正
    -   アクセスパスのプルーニングロジックが`READ_FROM_STORAGE(TIFLASH[...])`ヒントを無視し、 `Can't find a proper physical plan`エラー[＃40146](https://github.com/pingcap/tidb/issues/40146) @ [アイリンキッド](https://github.com/AilinKid)が発生する問題を修正しました。
    -   `GROUP_CONCAT` `ORDER BY`列[＃41986](https://github.com/pingcap/tidb/issues/41986) @ [アイリンキッド](https://github.com/AilinKid)を解析できない問題を修正
    -   深くネストされた式に対してハッシュコードが繰り返し計算され、メモリ使用量が増加し、OOM [＃42788](https://github.com/pingcap/tidb/issues/42788) @ [アイリンキッド](https://github.com/AilinKid)発生する問題を修正しました。
    -   CAST に精度損失がない場合に`cast(col)=range`条件で FullScan が発生する問題を修正[＃45199](https://github.com/pingcap/tidb/issues/45199) @ [アイリンキッド](https://github.com/AilinKid)
    -   MPP 実行プランで集計がユニオンを介してプッシュダウンされると、結果が正しくなくなる問題を修正しました[＃45850](https://github.com/pingcap/tidb/issues/45850) @ [アイリンキッド](https://github.com/AilinKid)
    -   `in (?)`とのバインディングが`in (?, ... ?)` [＃44298](https://github.com/pingcap/tidb/issues/44298) @ [qw4990](https://github.com/qw4990)と一致しない問題を修正
    -   `non-prep plan cache`実行プラン[＃47008](https://github.com/pingcap/tidb/issues/47008) @ [qw4990](https://github.com/qw4990)を再利用するときに接続照合順序を考慮しないことによって発生するエラーを修正
    -   実行されたプランがプランキャッシュ[＃46159](https://github.com/pingcap/tidb/issues/46159) @ [qw4990](https://github.com/qw4990)にヒットしない場合に警告が報告されない問題を修正しました
    -   `plan replayer dump explain`エラー[＃46197](https://github.com/pingcap/tidb/issues/46197) @ [時間と運命](https://github.com/time-and-fate)を報告する問題を修正
    -   CTE で DML ステートメントを実行するとpanicが発生する可能性がある問題を修正[＃46083](https://github.com/pingcap/tidb/issues/46083) @ [ウィノロス](https://github.com/winoros)
    -   2つのサブクエリ[＃46160](https://github.com/pingcap/tidb/issues/46160) @ [qw4990](https://github.com/qw4990)を結合するときに`TIDB_INLJ`ヒントが有効にならない問題を修正
    -   `MERGE_JOIN`の結果が間違っている問題を修正[＃46580](https://github.com/pingcap/tidb/issues/46580) @ [qw4990](https://github.com/qw4990)

-   ティクヴ

    -   Titan が有効になっているときに TiKV が起動に失敗し、 `Blob file deleted twice`エラーが発生する問題を修正しました[＃15454](https://github.com/tikv/tikv/issues/15454) @ [コナー1996](https://github.com/Connor1996)
    -   スレッド自発的およびスレッド非自発的モニタリング パネル[＃15413](https://github.com/tikv/tikv/issues/15413) @ [スペードA-タン](https://github.com/SpadeA-Tang)にデータがない問題を修正しました
    -   raftstore-applys [＃15371](https://github.com/tikv/tikv/issues/15371) @ [コナー1996](https://github.com/Connor1996)が継続的に増加するデータエラーを修正
    -   リージョン[＃13311](https://github.com/tikv/tikv/issues/13311) @ [ジグアン](https://github.com/zyguan)のメタデータが正しくないことが原因で発生する TiKVpanicの問題を修正しました。
    -   `sync_recovery`から`sync` [＃15366](https://github.com/tikv/tikv/issues/15366) @ [ノルーシュ](https://github.com/nolouch)に切り替えた後に QPS が 0 に低下する問題を修正
    -   オンライン安全でないリカバリがタイムアウト[＃15346](https://github.com/tikv/tikv/issues/15346) @ [コナー1996](https://github.com/Connor1996)で中止されない問題を修正
    -   CpuRecord [＃15304](https://github.com/tikv/tikv/issues/15304) @ [金星の上](https://github.com/overvenus)によって発生する可能性のあるメモリリークの問題を修正しました
    -   バックアップクラスタがダウンし、プライマリクラスタが[＃12914](https://github.com/tikv/tikv/issues/12914) @ [コナー1996](https://github.com/Connor1996)でクエリされたときに`"Error 9002: TiKV server timeout"`発生する問題を修正しました
    -   プライマリ クラスターが[＃12320](https://github.com/tikv/tikv/issues/12320) @ [ディスク](https://github.com/disksing)に回復した後に TiKV が再起動するとバックアップ TiKV が停止する問題を修正しました。

-   PD

    -   フラッシュバック[＃6912](https://github.com/tikv/pd/issues/6912) @ [金星の上](https://github.com/overvenus)中にリージョン情報が更新されず保存されない問題を修正
    -   ストア構成[＃6918](https://github.com/tikv/pd/issues/6918) @ [バッファフライ](https://github.com/bufferflies)の同期が遅いために PD リーダーの切り替えが遅くなる問題を修正しました。
    -   Scatter Peers [＃6962](https://github.com/tikv/pd/issues/6962) @ [バッファフライ](https://github.com/bufferflies)でグループが考慮されない問題を修正
    -   RU消費量が0未満の場合にPDがクラッシュする問題を修正[＃6973](https://github.com/tikv/pd/issues/6973) @ [キャビンフィーバーB](https://github.com/CabinfeverB)
    -   変更された分離レベルがデフォルトの配置ルール[＃7121](https://github.com/tikv/pd/issues/7121) @ [rleungx](https://github.com/rleungx)に同期されない問題を修正しました
    -   クラスターが大きい場合、クライアントが定期的に更新すると`min-resolved-ts` PD OOM が発生する可能性がある問題を修正[＃46664](https://github.com/pingcap/tidb/issues/46664) @ [ヒューシャープ](https://github.com/HuSharp)

-   TiFlash

    -   Grafana [＃7713](https://github.com/pingcap/tiflash/issues/7713) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)で`max_snapshot_lifetime`メトリックが正しく表示されない問題を修正
    -   最大継続時間に関する一部のメトリックが正しくない問題を修正[＃8076](https://github.com/pingcap/tiflash/issues/8076) @ [カルビンネオ](https://github.com/CalvinNeo)
    -   TiDB が MPP タスクが失敗したと誤って報告する問題を修正[＃7177](https://github.com/pingcap/tiflash/issues/7177) @ [いびん87](https://github.com/yibin87)

-   ツール

    -   バックアップと復元 (BR)

        -   バックアップが失敗したときに誤解を招くエラーメッセージ`resolve lock timeout`実際のエラーを隠してしまう問題を修正[＃43236](https://github.com/pingcap/tidb/issues/43236) @ [ユジュンセン](https://github.com/YuJuncen)
        -   PITR を使用して暗黙の主キーを回復すると競合が発生する可能性がある問題を修正[＃46520](https://github.com/pingcap/tidb/issues/46520) @ [3ポインター](https://github.com/3pointer)
        -   PITR を使用してメタ kv を回復するとエラーが発生する可能性がある問題を修正[＃46578](https://github.com/pingcap/tidb/issues/46578) @ [リーヴルス](https://github.com/Leavrth)
        -   BR統合テストケース[＃46561](https://github.com/pingcap/tidb/issues/46561) @ [ピュアリンド](https://github.com/purelind)のエラーを修正

    -   ティCDC

        -   PD のスケールアップおよびスケールダウン中に TiCDC が無効な古いアドレスにアクセスする問題を修正[＃9584](https://github.com/pingcap/tiflow/issues/9584) @ [ふびんず](https://github.com/fubinzh) @ [アズドンメン](https://github.com/asddongmen)
        -   一部のシナリオで changefeed が失敗する問題を修正[＃9309](https://github.com/pingcap/tiflow/issues/9309) [＃9450](https://github.com/pingcap/tiflow/issues/9450) [＃9542](https://github.com/pingcap/tiflow/issues/9542) [＃9685](https://github.com/pingcap/tiflow/issues/9685) @ [ヒック](https://github.com/hicqu) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)
        -   アップストリーム[＃9430](https://github.com/pingcap/tiflow/issues/9430) @ [スドジ](https://github.com/sdojjy)で 1 つのトランザクションで複数の行の一意のキーが変更されると、レプリケーション書き込み競合が発生する可能性がある問題を修正しました。
        -   アップストリームの同じDDL文で複数のテーブルの名前を変更するとレプリケーションエラーが発生する問題を修正[＃9476](https://github.com/pingcap/tiflow/issues/9476) [＃9488](https://github.com/pingcap/tiflow/issues/9488) @ [チャールズ・チュン96](https://github.com/CharlesCheung96) @ [アズドンメン](https://github.com/asddongmen)
        -   CSV ファイルで中国語の文字が検証されない問題を修正[＃9609](https://github.com/pingcap/tiflow/issues/9609) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)
        -   すべての変更フィードが削除された後に上流の TiDB GC がブロックされる問題を修正[＃9633](https://github.com/pingcap/tiflow/issues/9633) @ [スドジ](https://github.com/sdojjy)
        -   `scale-out`が有効になっている場合にノード間で書き込みキーが不均等に分散される問題を修正[＃9665](https://github.com/pingcap/tiflow/issues/9665) @ [スドジ](https://github.com/sdojjy)
        -   ログに機密ユーザー情報が記録される問題を修正[＃9690](https://github.com/pingcap/tiflow/issues/9690) @ [スドジ](https://github.com/sdojjy)

    -   TiDB データ移行 (DM)

        -   DM が大文字と小文字を区別しない照合[＃9489](https://github.com/pingcap/tiflow/issues/9489) @ [ヒヒフフ](https://github.com/hihihuhu)で競合を正しく処理できない問題を修正
        -   DM バリデーターのデッドロック問題を修正し、再試行を[＃9257](https://github.com/pingcap/tiflow/issues/9257) @ [D3ハンター](https://github.com/D3Hunter)に強化しました。
        -   失敗した DDL がスキップされ、後続の DDL が実行されない場合に、DM によって返されるレプリケーション ラグが増大し続ける問題を修正[＃9605](https://github.com/pingcap/tiflow/issues/9605) @ [D3ハンター](https://github.com/D3Hunter)
        -   オンライン DDL [＃9587](https://github.com/pingcap/tiflow/issues/9587) @ [GMHDBJD](https://github.com/GMHDBJD)をスキップするときに DM が上流のテーブル スキーマを適切に追跡できない問題を修正しました。
        -   楽観的モード[＃9588](https://github.com/pingcap/tiflow/issues/9588) @ [GMHDBJD](https://github.com/GMHDBJD)でタスクを再開するときに DM がすべての DML をスキップする問題を修正
        -   DM が楽観的モード[＃9788](https://github.com/pingcap/tiflow/issues/9788) @ [GMHDBJD](https://github.com/GMHDBJD)でパーティション DDL をスキップする問題を修正

    -   TiDB Lightning

        -   TiDB Lightningがテーブル`NONCLUSTERED auto_increment`と`AUTO_ID_CACHE=1`をインポートした後、データを挿入するとエラーが返される問題を修正しました[＃46100](https://github.com/pingcap/tidb/issues/46100) @ [天菜まお](https://github.com/tiancaiamao)
        -   `checksum = "optional"` [＃45382](https://github.com/pingcap/tidb/issues/45382) @ [翻訳者](https://github.com/lyzx2001)のときにチェックサムがエラーを報告する問題を修正しました
        -   PD クラスタ アドレスが[＃43436](https://github.com/pingcap/tidb/issues/43436) @ [リチュンジュ](https://github.com/lichunzhu)に変更されるとデータのインポートが失敗する問題を修正しました

## 寄稿者 {#contributors}

TiDB コミュニティの以下の貢献者に感謝いたします。

-   [あいでんどう](https://github.com/aidendou)
-   [コーダープレイ](https://github.com/coderplay)
-   [運命](https://github.com/fatelei)
-   [ハイポン](https://github.com/highpon)
-   [ヒヒフフ](https://github.com/hihihuhu) (初めての投稿者)
-   [イザベラ0428](https://github.com/isabella0428)
-   [ジフハウス](https://github.com/jiyfhust)
-   [JK1張](https://github.com/JK1Zhang)
-   [ジョーカー53-1](https://github.com/joker53-1) (初めての投稿者)
-   [L-メープル](https://github.com/L-maple)
-   [ミッタルリシャブ](https://github.com/mittalrishabh)
-   [舗装](https://github.com/paveyry)
-   [ショーン0915](https://github.com/shawn0915)
-   [テデュ](https://github.com/tedyu)
-   [ヤムチャイナ](https://github.com/yumchina)
-   [ズズッヘ](https://github.com/ZzzhHe)
