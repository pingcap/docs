---
title: TiDB 7.4.0 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 7.4.0.
---

# TiDB 7.4.0 リリースノート {#tidb-7-4-0-release-notes}

発売日：2023年10月12日

TiDB バージョン: 7.4.0

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v7.4/quick-start-with-tidb) | [インストールパッケージ](https://www.pingcap.com/download/?version=v7.4.0#version-list)

7.4.0 では、次の主要な機能と改善点が導入されています。

<table><thead><tr><th>カテゴリー</th><th>特徴</th><th>説明</th></tr></thead><tbody><tr><td rowspan="3">信頼性と可用性</td><td><a href="https://docs.pingcap.com/tidb/v7.4/tidb-global-sort" target="_blank">グローバルソート</a>による<code>IMPORT INTO</code>および<code>ADD INDEX</code>操作のパフォーマンスと安定性を向上します (実験的)</td><td> v7.4.0 より前は、 <a href="https://docs.pingcap.com/tidb/v7.4/tidb-distributed-execution-framework" target="_blank">分散実行フレームワーク</a>を使用した<code>ADD INDEX</code>や<code>IMPORT INTO</code>などのタスクは、ローカライズされた部分的なソートを意味しており、最終的に TiKV は部分的なソートを補うために多くの追加作業を行うことになりました。これらのジョブでは、TiKV にロードする前に、TiDB ノードでソート用のローカル ディスク領域を割り当てる必要もありました。<br/> v7.4.0 でのグローバル ソート機能の導入により、データは TiKV にロードされる前にグローバル ソートのために外部共有storage(このバージョンでは S3) に一時的に保存されます。これにより、TiKV が余分なリソースを消費する必要がなくなり、 <code>ADD INDEX</code>や<code>IMPORT INTO</code>などの操作のパフォーマンスと安定性が大幅に向上します。</td></tr><tr><td>バックグラウンドタスクの<a href="https://docs.pingcap.com/tidb/v7.4/tidb-resource-control#manage-background-tasks" target="_blank">リソース制御</a>(実験的)</td><td> v7.1.0 では、ワークロード間のリソースとstorageのアクセス干渉を軽減するために、 <a href="https://docs.pingcap.com/tidb/v7.4/tidb-resource-control#use-resource-control-to-achieve-resource-isolation" target="_blank">リソース制御</a>機能が導入されました。 TiDB v7.4.0 では、この制御をバックグラウンド タスクにも適用します。 v7.4.0 では、リソース コントロールは、自動分析、バックアップと復元、 TiDB Lightningによる一括ロード、オンライン DDL などのバックグラウンド タスクによって生成されたリソースを識別して管理するようになりました。これは最終的にはすべてのバックグラウンド タスクに適用されます。</td></tr><tr><td> TiFlash は<a href="https://docs.pingcap.com/tidb/v7.4/tiflash-disaggregated-and-s3" target="_blank">ストレージとコンピューティングの分離と S3</a> (GA) をサポートします</td><td>TiFlash の分散storageとコンピューティングアーキテクチャ、および S3 共有storageが一般提供されます。<ul><li> TiFlash のコンピューティングとstorageを分割します。これは、Elastic HTAP リソース使用率のマイルストーンです。</li><li> S3 ベースのstorageエンジンの使用をサポートし、低コストで共有storageを提供できます。</li></ul></td></tr><tr><td rowspan="2"> SQL</td><td> TiDB は<a href="https://docs.pingcap.com/tidb/v7.4/partitioned-table#convert-a-partitioned-table-to-a-non-partitioned-table" target="_blank">パーティション タイプの管理を</a>サポートします</td><td>v7.4.0 より前では、レンジ/リスト パーティション テーブルは<code>TRUNCATE</code> 、 <code>EXCHANGE</code> 、 <code>ADD</code> 、 <code>DROP</code> 、 <code>REORGANIZE</code>などのパーティション管理操作をサポートし、ハッシュ/キー パーティション テーブルは<code>ADD</code>や<code>COALESCE</code>などのパーティション管理操作をサポートします。<p> TiDB は、次のパーティション タイプ管理操作もサポートするようになりました。</p><ul><li>パーティション化されたテーブルを非パーティション化テーブルに変換する</li><li>既存のパーティション化されていないテーブルをパーティション化する</li><li>既存のテーブルのパーティション タイプを変更する</li></ul></td></tr><tr><td>MySQL 8.0 互換性: <a href="https://docs.pingcap.com/tidb/v7.4/character-set-and-collation#character-sets-and-collations-supported-by-tidb" target="_blank">照合順序<code>utf8mb4_0900_ai_ci</code></a>をサポート</td><td>MySQL 8.0 の注目すべき変更点の 1 つは、デフォルトの文字セットが utf8mb4 であり、 utf8mb4 のデフォルトの照合順序が<code>utf8mb4_0900_ai_ci</code>であることです。 TiDB v7.4.0 ではこのサポートが追加され、MySQL 8.0 との互換性が強化され、デフォルトの照合順序を使用した MySQL 8.0 データベースからの移行とレプリケーションがよりスムーズになりました。</td></tr><tr><td> DB の操作と可観測性</td><td><code>IMPORT INTO</code>および<code>ADD INDEX</code> SQL ステートメントを実行するための<a href="https://docs.pingcap.com/tidb/v7.4/system-variables#tidb_service_scope-new-in-v740" target="_blank">それぞれの TiDB ノード</a>を指定します (実験的)</td><td>既存の TiDB ノードまたは新しく追加された TiDB ノードのいずれかで<code>IMPORT INTO</code>または<code>ADD INDEX</code> SQL ステートメントを実行するかどうかを柔軟に指定できます。このアプローチにより、残りの TiDB ノードからリソースを分離でき、ビジネス運営への影響を防ぎながら、前述の SQL ステートメントを実行するための最適なパフォーマンスを確保できます。</td></tr></tbody></table>

## 機能の詳細 {#feature-details}

### スケーラビリティ {#scalability}

-   分散実行フレームワークのバックエンド`ADD INDEX`または`IMPORT INTO`タスクを並列実行するための TiDB ノードの選択をサポート (実験的) [#46453](https://github.com/pingcap/tidb/pull/46453) @ [ywqzzy](https://github.com/ywqzzy)

    リソースを大量に消費するクラスターで`ADD INDEX`または`IMPORT INTO`タスクを並行して実行すると、大量の TiDB ノード リソースが消費され、クラスターのパフォーマンスの低下につながる可能性があります。 v7.4.0 以降、システム変数[`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740)を使用して、 [TiDB バックエンド タスク分散実行フレームワーク](/tidb-distributed-execution-framework.md)の下の各 TiDB ノードのサービス スコープを制御できます。複数の既存の TiDB ノードを選択することも、新しい TiDB ノードの TiDB サービス スコープを設定することもでき、すべての並列`ADD INDEX`および`IMPORT INTO`タスクはこれらのノードでのみ実行されます。このメカニズムにより、既存のサービスへのパフォーマンスへの影響を回避できます。

    詳細については、 [ドキュメンテーション](/system-variables.md#tidb_service_scope-new-in-v740)を参照してください。

-   Partitioned Raft KVstorageエンジンの強化 (実験的) [#11515](https://github.com/tikv/tikv/issues/11515) [#12842](https://github.com/tikv/tikv/issues/12842) @ [ビジージェイ](https://github.com/busyjay) @ [トニーシュクキ](https://github.com/tonyxuqqi) @ [タボキー](https://github.com/tabokie) @ [バッファフライ](https://github.com/bufferflies) @ [5kbps](https://github.com/5kbpers) @ [SpadeA-Tang](https://github.com/SpadeA-Tang) @ [ノールーシュ](https://github.com/nolouch)

    TiDB v6.6.0 では、実験的機能として Partitioned Raft KVstorageエンジンが導入されています。これは、複数の RocksDB インスタンスを使用して TiKVリージョンデータを保存し、各リージョンのデータは個別の RocksDB インスタンスに独立して保存されます。

    v7.4.0 では、TiDB は Partitioned Raft KVstorageエンジンの互換性と安定性をさらに向上させます。大規模なデータ テストを通じて、DM、 Dumpling、 TiDB Lightning、TiCDC、 BR、PITR などの TiDB エコシステム ツールおよび機能との互換性が保証されます。さらに、パーティション化されたRaft KVstorageエンジンは、読み取りと書き込みの混合ワークロード下でより安定したパフォーマンスを提供し、書き込み負荷の高いシナリオに特に適しています。さらに、各 TiKV ノードは 8 コア CPU をサポートし、8 TB データstorageと 64 GBメモリで構成できるようになりました。

    詳細については、 [ドキュメンテーション](/partitioned-raft-kv.md)を参照してください。

-   TiFlash は、分散storageおよびコンピューティングアーキテクチャ(GA) [#6882](https://github.com/pingcap/tiflash/issues/6882) @ [ジェイ・ソン・ファン](https://github.com/JaySon-Huang) @ [ジンヘリン](https://github.com/JinheLin) @ [ブリーズウィッシュ](https://github.com/breezewish) @ [リデジュ](https://github.com/lidezhu) @ [カルビンネオ](https://github.com/CalvinNeo) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)をサポートしています。

    v7.0.0 では、 TiFlashに実験的機能として分散storageおよびコンピューティングアーキテクチャが導入されています。一連の改善により、 TiFlashの分散storageおよびコンピューティングアーキテクチャが v7.4.0 から GA になります。

    このアーキテクチャでは、 TiFlashノードは 2 つのタイプ (コンピューティング ノードと書き込みノード) に分けられ、S3 API と互換性のあるオブジェクトstorageをサポートします。どちらのタイプのノードも、コンピューティング容量またはstorage容量に合わせて個別にスケーリングできます。分離されたstorageとコンピューティングアーキテクチャでは、 TiFlashレプリカの作成、データのクエリ、オプティマイザ ヒントの指定など、結合されたストレージとコンピューティングアーキテクチャと同じ方法でTiFlashを使用できます。

    TiFlash**の分離されたstorageとコンピューティングアーキテクチャ**と、**結合されたstorageとコンピューティングアーキテクチャは、**同じクラスター内で使用したり、相互に変換したりすることはできないことに注意してください。 TiFlash を展開するときに使用するアーキテクチャを構成できます。

    詳細については、 [ドキュメンテーション](/tiflash/tiflash-disaggregated-and-s3.md)を参照してください。

### パフォーマンス {#performance}

-   JSON 演算子`MEMBER OF`を TiKV [#46307](https://github.com/pingcap/tidb/issues/46307) @ [wshwsh12](https://github.com/wshwsh12)にプッシュダウンするサポート

    -   `value MEMBER OF(json_array)`

    詳細については、 [ドキュメンテーション](/functions-and-operators/expressions-pushed-down.md)を参照してください。

-   任意のフレーム定義タイプのウィンドウ関数のTiFlash [#7376](https://github.com/pingcap/tiflash/issues/7376) @ [xzhangxian1008](https://github.com/xzhangxian1008)へのプッシュダウンをサポート

    v7.4.0 より前では、 TiFlash は`PRECEDING`または`FOLLOWING`含むウィンドウ関数をサポートしておらず、そのようなフレーム定義を含むすべてのウィンドウ関数をTiFlashにプッシュダウンすることはできません。 v7.4.0 以降、 TiFlash はすべてのウィンドウ関数のフレーム定義をサポートします。この機能は自動的に有効になり、関連する要件が満たされると、フレーム定義を含むウィンドウ関数が自動的にTiFlashにプッシュダウンされて実行されます。

-   クラウド ストレージ ベースのグローバル ソート機能を導入して、並列実行時の`ADD INDEX`および`IMPORT INTO`タスクのパフォーマンスと安定性を向上させます (実験的) [#45719](https://github.com/pingcap/tidb/issues/45719) @ [wjhuang2016](https://github.com/wjhuang2016)

    v7.4.0 より前は、分散並列実行フレームワークで`ADD INDEX`や`IMPORT INTO`ようなタスクを実行する場合、各 TiDB ノードは、エンコードされたインデックス KV ペアとテーブル データ KV ペアをソートするために大量のローカル ディスク領域を割り当てる必要がありました。ただし、グローバルな並べ替え機能がないため、プロセス中に異なる TiDB ノード間および個々のノード内でデータが重複する可能性があります。その結果、TiKV はこれらの KV ペアをstorageエンジンにインポートする間、常に圧縮操作を実行する必要があり、これが`ADD INDEX`と`IMPORT INTO`のパフォーマンスと安定性に影響を与えます。

    v7.4.0 では、TiDB に[グローバルソート](/tidb-global-sort.md)機能が導入されています。エンコードされたデータをローカルに書き込んでそこで並べ替えるのではなく、データはクラウドstorageに書き込まれてグローバルに並べ替えられるようになりました。並べ替えが完了すると、インデックス付きデータとテーブル データの両方が TiKV に並行してインポートされるため、パフォーマンスと安定性が向上します。

    詳細については、 [ドキュメンテーション](/tidb-global-sort.md)を参照してください。

-   非プリペアド ステートメント (GA) [#36598](https://github.com/pingcap/tidb/issues/36598) @ [qw4990](https://github.com/qw4990)の実行プランのキャッシュをサポート

    TiDB v7.0.0 では、同時 OLTP の負荷容量を向上させるための実験的機能として、準備されていないプラン キャッシュが導入されています。 v7.4.0 では、この機能は GA になります。実行プラン キャッシュはより多くのシナリオに適用されるため、TiDB の同時処理能力が向上します。

    準備されていないプラン キャッシュを有効にすると、追加のメモリと CPU オーバーヘッドが発生する可能性があり、すべての状況に適しているとは限りません。 v7.4.0 以降、この機能はデフォルトで無効になっています。 [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache)使用して有効にし、 [`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-new-in-v710)を使用してキャッシュ サイズを制御できます。

    さらに、この機能はデフォルトでは DML ステートメントをサポートしておらず、SQL ステートメントに特定の制限があります。詳細については、 [制限](/sql-non-prepared-plan-cache.md#restrictions)を参照してください。

    詳細については、 [ドキュメンテーション](/sql-non-prepared-plan-cache.md)を参照してください。

### 信頼性 {#reliability}

-   TiFlash はクエリレベルのデータスピル[#7738](https://github.com/pingcap/tiflash/issues/7738) @ [ウィンドトーカー](https://github.com/windtalker)をサポートします

    v7.0.0 以降、 TiFlash は3 つの演算子 ( `GROUP BY` 、 `ORDER BY` 、および`JOIN` ) のデータ スピルの制御をサポートします。この機能により、データ サイズが使用可能なメモリを超えた場合のクエリの終了やシステム クラッシュなどの問題が防止されます。ただし、各オペレータの流出を個別に管理するのは煩雑であり、全体的なリソース制御にとって非効率的になる可能性があります。

    v7.4.0 では、 TiFlash にクエリレベルのデータ流出が導入されました。 TiFlashノード上のクエリのメモリ制限を[`tiflash_mem_quota_query_per_node`](/system-variables.md#tiflash_mem_quota_query_per_node-new-in-v740)に設定し、データ スピルをトリガーするメモリ比率を[`tiflash_query_spill_ratio`](/system-variables.md#tiflash_query_spill_ratio-new-in-v740)に設定すると、クエリのメモリ使用量を簡単に管理でき、 TiFlashメモリリソースをより適切に制御できます。

    詳細については、 [ドキュメンテーション](/tiflash/tiflash-spill-disk.md)を参照してください。

-   ユーザー定義の TiKV 読み取りタイムアウト[#45380](https://github.com/pingcap/tidb/issues/45380) @ [クレイジークス520](https://github.com/crazycs520)をサポート

    通常、TiKV はリクエストを数ミリ秒以内に非常に迅速に処理します。ただし、TiKV ノードでディスク I/O ジッターやネットワークレイテンシーが発生すると、リクエストの処理時間が大幅に増加する可能性があります。 v7.4.0 より前のバージョンでは、TiKV リクエストのタイムアウト制限は固定されており、調整できません。したがって、TiKV ノードで問題が発生した場合、TiDB は固定期間のタイムアウト応答を待つ必要があり、その結果、ジッター中のアプリケーション クエリのパフォーマンスに顕著な影響が生じます。

    TiDB v7.4.0 では、新しいシステム変数[`tikv_client_read_timeout`](/system-variables.md#tikv_client_read_timeout-new-in-v740)が導入されており、これにより、TiDB がクエリで TiKV に送信する RPC 読み取りリクエストのタイムアウトをカスタマイズできます。つまり、ディスクまたはネットワークの問題により TiKV ノードに送信されたリクエストが遅延した場合、TiDB はタイムアウトを早めてリクエストを他の TiKV ノードに再送信できるため、クエリのレイテンシーが短縮されます。すべての TiKV ノードでタイムアウトが発生した場合、TiDB はデフォルトのタイムアウトを使用して再試行します。さらに、クエリでオプティマイザ ヒント`/*+ SET_VAR(TIKV_CLIENT_READ_TIMEOUT=N) */`使用して、TiDB が TiKV RPC 読み取りリクエストを送信するためのタイムアウトを設定することもできます。この機能強化により、TiDB は不安定なネットワークまたはstorage環境に適応する柔軟性が得られ、クエリのパフォーマンスが向上し、ユーザー エクスペリエンスが向上します。

    詳細については、 [ドキュメンテーション](/system-variables.md#tikv_client_read_timeout-new-in-v740)を参照してください。

-   オプティマイザー ヒント[#45892](https://github.com/pingcap/tidb/issues/45892) @ [ウィノロス](https://github.com/winoros)を使用した一部のシステム変数値の一時的な変更をサポートします。

    TiDB v7.4.0 では、MySQL 8.0 と同様のオプティマイザー ヒント`SET_VAR()`が導入されています。 SQL ステートメントにヒント`SET_VAR()`含めることにより、ステートメントの実行中にシステム変数の値を一時的に変更できます。これは、さまざまなステートメントの環境を設定するのに役立ちます。たとえば、リソースを大量に消費する SQL ステートメントの並列処理を積極的に増やしたり、変数を使用してオプティマイザーの動作を変更したりできます。

    ヒント`SET_VAR()`の[システム変数](/system-variables.md)を使用して、変更できるシステム変数を見つけることができます。明示的にサポートされていない変数を変更すると、予期しない動作が発生する可能性があるため、変更しないことを強くお勧めします。

    詳細については、 [ドキュメンテーション](/optimizer-hints.md)を参照してください。

-   TiFlash はリソース制御[#7660](https://github.com/pingcap/tiflash/issues/7660) @ [グオシャオゲ](https://github.com/guo-shaoge)をサポートします

    TiDB v7.1.0 では、リソース制御機能が一般提供され、TiDB と TiKV にリソース管理機能が提供されます。 v7.4.0 では、 TiFlash はリソース制御機能をサポートし、TiDB の全体的なリソース管理機能を向上させます。 TiFlashのリソース制御は、既存の TiDB リソース制御機能と完全な互換性があり、既存のリソース グループは TiDB、TiKV、およびTiFlashのリソースを同時に管理します。

    TiFlashリソース制御機能を有効にするかどうかを制御するには、 TiFlashパラメーター`enable_resource_control`を構成します。この機能を有効にすると、 TiFlash はTiDB のリソース グループ構成に基づいてリソースのスケジューリングと管理を実行し、リソース全体の合理的な割り当てと使用を保証します。

    詳細については、 [ドキュメンテーション](/tidb-resource-control.md)を参照してください。

-   TiFlash はパイプライン実行モデル (GA) [#6518](https://github.com/pingcap/tiflash/issues/6518) @ [シーライズ](https://github.com/SeaRise)をサポートします。

    v7.2.0 以降、 TiFlash にはパイプライン実行モデルが導入されています。このモデルは、すべてのスレッド リソースを集中管理し、タスクの実行を均一にスケジュールすることで、リソースの過剰使用を回避しながらスレッド リソースの利用率を最大化します。 v7.4.0 では、 TiFlashによりスレッド リソース使用量の統計が改善され、パイプライン実行モデルが GA 機能となり、デフォルトで有効になります。この機能はTiFlashリソース制御機能と相互に依存しているため、TiDB v7.4.0 では、以前のバージョンでパイプライン実行モデルを有効にするかどうかの制御に使用されていた変数`tidb_enable_tiflash_pipeline_model`削除されています。代わりに、 TiFlashパラメータ`tidb_enable_resource_control`を構成することで、パイプライン実行モデルとTiFlashリソース制御機能を有効または無効にすることができます。

    詳細については、 [ドキュメンテーション](/tiflash/tiflash-pipeline-model.md)を参照してください。

-   オプティマイザモード[#46080](https://github.com/pingcap/tidb/issues/46080) @ [時間と運命](https://github.com/time-and-fate)のオプションを追加

    v7.4.0 では、TiDB に新しいシステム変数[`tidb_opt_objective`](/system-variables.md#tidb_opt_objective-new-in-v740)導入され、オプティマイザが使用する推定方法を制御します。デフォルト値`moderate`では、オプティマイザの以前の動作が維持され、ランタイム統計を使用してデータの変更に基づいて推定が調整されます。この変数が`determinate`に設定されている場合、オプティマイザーは実行時の修正を考慮せずに統計のみに基づいて実行計画を生成します。

    長期的に安定した OLTP アプリケーション、または既存の実行計画に自信がある状況の場合は、テスト後に`determinate`モードに切り替えることをお勧めします。これにより、計画変更の可能性が減ります。

    詳細については、 [ドキュメンテーション](/system-variables.md#tidb_opt_objective-new-in-v740)を参照してください。

-   TiDB リソース制御は、バックグラウンド タスクの管理をサポートします (実験的) [#44517](https://github.com/pingcap/tidb/issues/44517) @ [グロルフ](https://github.com/glorv)

    データのバックアップや自動統計収集などのバックグラウンド タスクは優先度は低いですが、多くのリソースを消費します。これらのタスクは通常、定期的または不定期にトリガーされます。実行中に大量のリソースが消費されるため、オンラインの優先度の高いタスクのパフォーマンスに影響します。 v7.4.0 以降、TiDB リソース制御機能はバックグラウンド タスクの管理をサポートします。この機能により、オンライン アプリケーションに対する優先度の低いタスクのパフォーマンスへの影響が軽減され、合理的なリソース割り当てが可能になり、クラスターの安定性が大幅に向上します。

    TiDB は、次のタイプのバックグラウンド タスクをサポートします。

    -   `lightning` : [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)または[`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)を使用してインポート タスクを実行します。
    -   `br` : [BR](/br/backup-and-restore-overview.md)を使用してバックアップおよび復元タスクを実行します。 PITR はサポートされていません。
    -   `ddl` : Reorg DDL のバッチ データ ライトバック フェーズ中のリソース使用量を制御します。
    -   `stats` : 手動で実行されるか、TiDB によって自動的にトリガーされる[統計を収集する](/statistics.md#collect-statistics)タスク。

    デフォルトでは、バックグラウンド タスクとしてマークされているタスク タイプは空であり、バックグラウンド タスクの管理は無効になっています。このデフォルトの動作は、TiDB v7.4.0 より前のバージョンの動作と同じです。バックグラウンド タスクを管理するには、 `default`リソース グループのバックグラウンド タスクの種類を手動で変更する必要があります。

    詳細については、 [ドキュメンテーション](/tidb-resource-control.md#manage-background-tasks)を参照してください。

-   統計[#46351](https://github.com/pingcap/tidb/issues/46351) @ [こんにちはラスティン](https://github.com/hi-rustin)をロックする機能を強化

    v7.4.0 では、TiDB の機能が[ロック統計](/statistics.md#lock-statistics)に強化されました。現在、運用上のセキュリティを確保するために、統計のロックとロック解除には統計の収集と同じ権限が必要です。さらに、TiDB は特定のパーティションの統計のロックとロック解除をサポートしており、柔軟性が向上します。データベース内のクエリと実行プランに自信があり、変更が発生しないようにしたい場合は、統計をロックして安定性を高めることができます。

    詳細については、 [ドキュメンテーション](/statistics.md#lock-statistics)を参照してください。

-   テーブル[#46695](https://github.com/pingcap/tidb/issues/46695) @ [コードプレイ](https://github.com/coderplay)にハッシュ結合を選択するかどうかを制御するシステム変数を導入します。

    MySQL 8.0 では、新機能としてテーブルのハッシュ結合が導入されています。この機能は主に、2 つの比較的大きなテーブルと結果セットを結合するために使用されます。ただし、トランザクション ワークロード、またはMySQL 5.7で実行されている一部のアプリケーションの場合、テーブルのハッシュ結合はパフォーマンス リスクを引き起こす可能性があります。 MySQL は、ハッシュ結合をグローバル レベルで選択するかセッション レベルで選択するかを制御する[`optimizer_switch`](https://dev.mysql.com/doc/refman/8.0/en/switchable-optimizations.html#optflag_block-nested-loop)を提供します。

    v7.4.0 以降、TiDB ではテーブルのハッシュ結合を制御するためにシステム変数[`tidb_opt_enable_hash_join`](/system-variables.md#tidb_opt_enable_hash_join-new-in-v740)が導入されています。これはデフォルトで有効になっています ( `ON` )。実行計画内のテーブル間のハッシュ結合を選択する必要がないことが確実な場合は、変数を`OFF`に変更して、実行計画のロールバックの可能性を減らし、システムの安定性を向上させることができます。

    詳細については、 [ドキュメンテーション](/system-variables.md#tidb_opt_enable_hash_join-new-in-v740)を参照してください。

### SQL {#sql}

-   TiDB はパーティション タイプ管理[#42728](https://github.com/pingcap/tidb/issues/42728) @ [むじょん](https://github.com/mjonss)をサポートします

    v7.4.0 より前は、TiDB のパーティション テーブルのパーティション タイプを変更できません。 v7.4.0 以降、TiDB は、パーティション化テーブルから非パーティション化テーブルへ、または非パーティション化テーブルからパーティション化テーブルへの変更をサポートし、パーティション タイプの変更をサポートします。したがって、パーティションテーブルのパーティション タイプと数を柔軟に調整できるようになりました。たとえば、 `ALTER TABLE t PARTITION BY ...`ステートメントを使用してパーティション タイプを変更できます。

    詳細については、 [ドキュメンテーション](/partitioned-table.md#convert-a-partitioned-table-to-a-non-partitioned-table)を参照してください。

-   TiDB は、 `ROLLUP`修飾子と`GROUPING`関数[#44487](https://github.com/pingcap/tidb/issues/44487) @ [アイリンキッド](https://github.com/AilinKid)の使用をサポートしています。

    `WITH ROLLUP`修飾子と`GROUPING`関数は、多次元データの要約のためのデータ分析でよく使用されます。 v7.4.0 以降、 `GROUP BY`句で`WITH ROLLUP`修飾子と`GROUPING`関数を使用できるようになりました。たとえば、 `SELECT ... FROM ... GROUP BY ... WITH ROLLUP`構文で`WITH ROLLUP`修飾子を使用できます。

    詳細については、 [ドキュメンテーション](/functions-and-operators/group-by-modifier.md)を参照してください。

### DB操作 {#db-operations}

-   照合順序`utf8mb4_0900_ai_ci`および`utf8mb4_0900_bin` [#37566](https://github.com/pingcap/tidb/issues/37566) @ [ヤンケオ](https://github.com/YangKeao) @ [ジムララ](https://github.com/zimulala) @ [bb7133](https://github.com/bb7133)をサポート

    TiDB v7.4.0 では、MySQL 8.0 からのデータ移行のサポートが強化され、2 つの照合順序`utf8mb4_0900_ai_ci`と`utf8mb4_0900_bin`が追加されています。 `utf8mb4_0900_ai_ci`は MySQL 8.0 のデフォルトの照合順序です。

    TiDB v7.4.0 では、MySQL 8.0 と互換性のあるシステム変数`default_collation_for_utf8mb4`も導入されています。これにより、utf8mb4 文字セットのデフォルトの照合順序を指定できるようになり、 MySQL 5.7以前のバージョンからの移行またはデータ レプリケーションとの互換性が提供されます。

    詳細については、 [ドキュメンテーション](/character-set-and-collation.md#character-sets-and-collations-supported-by-tidb)を参照してください。

### 可観測性 {#observability}

-   セッション接続 ID とセッション エイリアスのログ[#46071](https://github.com/pingcap/tidb/issues/46071) @ [ルクワンチャオ](https://github.com/lcwangchao)への追加をサポート

    SQL 実行の問題のトラブルシューティングを行う場合、多くの場合、TiDBコンポーネントログの内容を関連付けて、根本原因を特定することが必要になります。 v7.4.0 以降、TiDB は、TiDB ログ、スロー クエリ ログ、TiKV 上のコプロセッサからのスロー ログなどのセッション関連ログにセッション接続 ID ( `CONNECTION_ID` ) を書き込むことができます。セッション接続 ID に基づいていくつかのタイプのログの内容を関連付けることで、トラブルシューティングと診断の効率を向上させることができます。

    さらに、セッションレベルのシステム変数[`tidb_session_alias`](/system-variables.md#tidb_session_alias-new-in-v740)を設定すると、上記のログにカスタム識別子を追加できます。アプリケーション識別情報をログに挿入するこの機能を使用すると、ログの内容をアプリケーションと関連付け、アプリケーションからログへのリンクを構築し、診断の難易度を下げることができます。

-   TiDB ダッシュボードは、テーブル ビュー[#1589](https://github.com/pingcap/tidb-dashboard/issues/1589) @ [バーリン](https://github.com/baurine)での実行プランの表示をサポートします。

    v7.4.0 では、TiDB ダッシュボードは、診断エクスペリエンスを向上させるために、テーブル ビューの**[スロー クエリ]**ページと**[SQL ステートメント]**ページでの実行プランの表示をサポートします。

    詳細については、 [ドキュメンテーション](/dashboard/dashboard-statement-details.md)を参照してください。

### データ移行 {#data-migration}

-   `IMPORT INTO`機能[#46704](https://github.com/pingcap/tidb/issues/46704) @ [D3ハンター](https://github.com/D3Hunter)を強化

    v7.4.0 以降、 `IMPORT INTO`ステートメントに`CLOUD_STORAGE_URI`オプションを追加して[グローバルソート](/tidb-global-sort.md)機能 (実験的) を有効にすることができます。これにより、インポートのパフォーマンスと安定性が向上します。 `CLOUD_STORAGE_URI`オプションでは、エンコードされたデータのクラウドstorageアドレスを指定できます。

    さらに、v7.4.0 では、 `IMPORT INTO`機能により次の機能が導入されています。

    -   `Split_File`オプションの構成をサポートします。これにより、大きな CSV ファイルを複数の 256 MiB の小さな CSV ファイルに分割して並列処理できるようになり、インポートのパフォーマンスが向上します。
    -   圧縮された CSV および SQL ファイルのインポートをサポートします。サポートされている圧縮形式には、 `.gzip` 、 `.gz` 、 `.zstd` 、 `.zst` 、および`.snappy`が含まれます。

    詳細については、 [ドキュメンテーション](/sql-statements/sql-statement-import-into.md)を参照してください。

-   Dumpling は、データを CSV ファイルにエクスポートするときにユーザー定義のターミネータをサポートします[#46982](https://github.com/pingcap/tidb/issues/46982) @ [GMHDBJD](https://github.com/GMHDBJD)

    v7.4.0 より前では、 Dumpling はデータを CSV ファイルにエクスポートするときに行末記号として`"\r\n"`を使用します。その結果、ターミネータとして`"\n"`を認識する特定のダウンストリーム システムでは、エクスポートされた CSV ファイルを解析できないか、ファイルを解析する前に変換にサードパーティ ツールを使用する必要があります。

    v7.4.0 以降、 Dumpling には新しいパラメータ`--csv-line-terminator`が導入されています。このパラメータを使用すると、データを CSV ファイルにエクスポートするときに必要なターミネータを指定できます。このパラメータは`"\r\n"`と`"\n"`をサポートします。以前のバージョンとの一貫性を保つために、デフォルトのターミネータは`"\r\n"`です。

    詳細については、 [ドキュメンテーション](/dumpling-overview.md#option-list-of-dumpling)を参照してください。

-   TiCDC は Pulsar [#9413](https://github.com/pingcap/tiflow/issues/9413) @ [ヤムチナ](https://github.com/yumchina) @ [東門](https://github.com/asddongmen)へのデータの複製をサポートします

    Pulsar は、リアルタイム データ ストリーミング エクスペリエンスを大幅に強化する、クラウドネイティブの分散型メッセージ ストリーミング プラットフォームです。 v7.4.0 以降、TiCDC は、Pulsar とのシームレスな統合を実現するために、 `canal-json`形式での Pulsar への変更データのレプリケートをサポートします。この機能により、TiCDC は、TiDB の変更を簡単にキャプチャして Pulsar に複製する機能を提供し、データ処理と分析機能の新たな可能性を提供します。特定のビジネス ニーズを満たすために、Pulsar から新しく生成された変更データを読み取って処理する独自のコンシューマ アプリケーションを開発できます。

    詳細については、 [ドキュメンテーション](/ticdc/ticdc-sink-to-pulsar.md)を参照してください。

<!---->

-   TiCDC は、クレーム チェック パターン[#9153](https://github.com/pingcap/tiflow/issues/9153) @ [3エースショーハンド](https://github.com/3AceShowHand)を使用して大きなメッセージの処理を改善します

    v7.4.0 より前では、TiCDC は Kafka の最大メッセージ サイズ ( `max.message.bytes` ) を超える大きなメッセージをダウンストリームに送信できませんでした。 v7.4.0 以降、Kafka をダウンストリームとして使用してチェンジフィードを構成する場合、大きなメッセージを保存するための外部storageの場所を指定し、外部storage内の大きなメッセージのアドレスを含む参照メッセージを Kafka に送信できます。コンシューマーは、この参照メッセージを受信すると、外部storageアドレスからメッセージの内容を取得できます。

    詳細については、 [ドキュメンテーション](/ticdc/ticdc-sink-to-kafka.md#send-large-messages-to-external-storage)を参照してください。

## 互換性の変更 {#compatibility-changes}

> **注記：**
>
> このセクションでは、v7.3.0 から現在のバージョン (v7.4.0) にアップグレードするときに知っておく必要がある互換性の変更について説明します。 v7.2.0 以前のバージョンから現在のバージョンにアップグレードする場合は、中間バージョンで導入された互換性の変更も確認する必要がある場合があります。

### 行動の変化 {#behavior-changes}

-   v7.4.0 以降、TiDB は MySQL 8.0 の重要な機能と互換性があり、 `version()`​​接頭辞`8.0.11`が付いているバージョンを返します。

-   TiFlash が以前のバージョンから v7.4.0 にアップグレードされた後は、元のバージョンへのインプレース ダウングレードはサポートされません。これは、v7.4 以降、 TiFlash はPageStorage V3 のデータ圧縮ロジックを最適化し、データ圧縮中に生成される読み取りおよび書き込みの増幅を軽減し、これにより基礎となるstorageファイル名の一部が変更されるためです。

-   TSO タイムスタンプの論理部分を抽出できるようにする[`TIDB_PARSE_TSO_LOGICAL()`](/functions-and-operators/tidb-functions.md#tidb-specific-functions)関数が追加されました。

-   MySQL 8.0 との互換性を向上させるために、 [`information_schema.CHECK_CONSTRAINTS`](/information-schema/information-schema-check-constraints.md)テーブルが追加されました。

### システム変数 {#system-variables}

| 変数名                                                                                                     | 種類の変更    | 説明                                                                                                                                                                                                                                                                                                                                                                  |
| ------------------------------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `tidb_enable_tiflash_pipeline_model`                                                                    | 削除されました  | この変数は、 TiFlashパイプライン実行モデルを有効にするかどうかを制御するために使用されました。 v7.4.0 以降、 TiFlashリソース制御機能が有効になると、 TiFlashパイプライン実行モデルが自動的に有効になります。                                                                                                                                                                                                                                              |
| [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache)       | 修正済み     | さらにテストを行った後、デフォルト値を`ON`から`OFF`に変更します。これは、準備されていない実行プランのキャッシュが無効になることを意味します。                                                                                                                                                                                                                                                                                         |
| [`default_collation_for_utf8mb4`](/system-variables.md#default_collation_for_utf8mb4-new-in-v740)       | 新しく追加された | `utf8mb4`文字セットのデフォルトの照合順序を制御します。デフォルト値は`utf8mb4_bin`です。                                                                                                                                                                                                                                                                                                             |
| [`tidb_cloud_storage_uri`](/system-variables.md#tidb_cloud_storage_uri-new-in-v740)                     | 新しく追加された | [グローバルソート](/tidb-global-sort.md)を有効にするクラウドstorageURI を指定します。                                                                                                                                                                                                                                                                                                        |
| [`tidb_opt_enable_hash_join`](/system-variables.md#tidb_opt_enable_hash_join-new-in-v740)               | 新しく追加された | オプティマイザーがテーブルのハッシュ結合を選択するかどうかを制御します。デフォルトの値は`ON`です。 `OFF`に設定すると、オプティマイザは、他に利用可能な実行プランがない限り、テーブルのハッシュ結合の選択を回避します。                                                                                                                                                                                                                                                    |
| [`tidb_opt_objective`](/system-variables.md#tidb_opt_objective-new-in-v740)                             | 新しく追加された | この変数は、オプティマイザーの目的を制御します。 `moderate` TiDB v7.4.0 より前のバージョンのデフォルトの動作を維持しており、オプティマイザはより多くの情報を使用してより適切な実行プランを生成しようとします。 `determinate`モードはより保守的になる傾向があり、実行計画がより安定します。                                                                                                                                                                                                    |
| [`tidb_schema_version_cache_limit`](/system-variables.md#tidb_schema_version_cache_limit-new-in-v740)   | 新しく追加された | この変数は、TiDB インスタンスにキャッシュできる過去のスキーマ バージョンの数を制限します。デフォルト値は`16`です。これは、TiDB がデフォルトで 16 個の履歴スキーマ バージョンをキャッシュすることを意味します。                                                                                                                                                                                                                                                   |
| [`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740)                             | 新しく追加された | この変数はインスタンスレベルのシステム変数です。これを使用して、 [TiDB 分散実行フレームワーク](/tidb-distributed-execution-framework.md)の下の TiDB ノードのサービス スコープを制御できます。 TiDB ノードの`tidb_service_scope` `background`に設定すると、TiDB 分散実行フレームワークは、その TiDB ノードが[`ADD INDEX`](/sql-statements/sql-statement-add-index.md)や[`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)などのバックグラウンド タスクを実行するようにスケジュールします。 |
| [`tidb_session_alias`](/system-variables.md#tidb_session_alias-new-in-v740)                             | 新しく追加された | 現在のセッションに関連するログの`session_alias`列の値を制御します。                                                                                                                                                                                                                                                                                                                           |
| [`tiflash_mem_quota_query_per_node`](/system-variables.md#tiflash_mem_quota_query_per_node-new-in-v740) | 新しく追加された | TiFlashノード上のクエリの最大メモリ使用量を制限します。クエリのメモリ使用量がこの制限を超えると、 TiFlash はエラーを返し、クエリを終了します。デフォルト値は`0`で、制限がないことを意味します。                                                                                                                                                                                                                                                           |
| [`tiflash_query_spill_ratio`](/system-variables.md#tiflash_query_spill_ratio-new-in-v740)               | 新しく追加された | TiFlash [クエリレベルの流出](/tiflash/tiflash-spill-disk.md#query-level-spilling)のしきい値を制御します。デフォルト値は`0.7`です。                                                                                                                                                                                                                                                                 |
| [`tikv_client_read_timeout`](/system-variables.md#tikv_client_read_timeout-new-in-v740)                 | 新しく追加された | TiDB がクエリで TiKV RPC 読み取りリクエストを送信するときのタイムアウトを制御します。デフォルト値`0`は、デフォルトのタイムアウト (通常は 40 秒) が使用されることを示します。                                                                                                                                                                                                                                                                 |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーションパラメータ                                                                                                                         | 種類の変更    | 説明                                                                                                                                                                        |
| -------------- | --------------------------------------------------------------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB           | [`enable-stats-cache-mem-quota`](/tidb-configuration-file.md#enable-stats-cache-mem-quota-new-in-v610)                                  | 修正済み     | デフォルト値が`false`から`true`に変更されました。これは、TiDB 統計をキャッシュするためのメモリ制限がデフォルトで有効になることを意味します。                                                                                           |
| TiKV           | [`rocksdb.[defaultcf|writecf|lockcf].periodic-compaction-seconds`](/tikv-configuration-file.md#periodic-compaction-seconds-new-in-v720) | 修正済み     | RocksDB の定期的な圧縮をデフォルトで無効にするために、デフォルト値が`"30d"`から`"0s"`に変更されました。この変更により、フロントエンドの読み取りおよび書き込みパフォーマンスに影響を与える、TiDB アップグレード後にトリガーされる大量の圧縮が回避されます。                                |
| TiKV           | [`rocksdb.[defaultcf|writecf|lockcf].ttl`](/tikv-configuration-file.md#ttl-new-in-v720)                                                 | 修正済み     | デフォルト値は`"30d"`から`"0s"`に変更され、SST ファイルが TTL のためにデフォルトで圧縮をトリガーしないようにします。これにより、フロントエンドの読み取りおよび書き込みパフォーマンスへの影響が回避されます。                                                         |
| TiFlash        | [`flash.compact_log_min_gap`](/tiflash/tiflash-configuration.md)                                                                        | 新しく追加された | 現在のRaftステート マシンによって進められた`applied_index`と、最後のディスク スピル時の`applied_index`ギャップが`compact_log_min_gap`を超えると、 TiFlash はTiKV からの`CompactLog`コマンドを実行し、データをディスクにスピルします。              |
| TiFlash        | [`profiles.default.enable_resource_control`](/tiflash/tiflash-configuration.md)                                                         | 新しく追加された | TiFlashリソース制御機能を有効にするかどうかを制御します。                                                                                                                                          |
| TiFlash        | [`storage.format_version`](/tiflash/tiflash-configuration.md)                                                                           | 修正済み     | デフォルト値を`4`から`5`に変更します。新しい形式では、より小さなファイルを結合することで物理ファイルの数を減らすことができます。                                                                                                       |
| Dumpling       | [`--csv-line-terminator`](/dumpling-overview.md#option-list-of-dumpling)                                                                | 新しく追加された | CSV ファイルの目的のターミネータを指定します。このオプションは`"\r\n"`と`"\n"`をサポートします。デフォルト値は`"\r\n"`で、これは以前のバージョンと一致しています。                                                                            |
| TiCDC          | [`claim-check-storage-uri`](/ticdc/ticdc-sink-to-kafka.md#send-large-messages-to-external-storage)                                      | 新しく追加された | `large-message-handle-option`を`claim-check`に設定する場合、 `claim-check-storage-uri`有効な外部storageアドレスに設定する必要があります。そうしないと、変更フィードの作成でエラーが発生します。                                     |
| TiCDC          | [`large-message-handle-compression`](/ticdc/ticdc-sink-to-kafka.md#ticdc-data-compression)                                              | 新しく追加された | エンコード中に圧縮を有効にするかどうかを制御します。デフォルト値は空であり、有効になっていないことを意味します。                                                                                                                  |
| TiCDC          | [`large-message-handle-option`](/ticdc/ticdc-sink-to-kafka.md#send-large-messages-to-external-storage)                                  | 修正済み     | この構成アイテムにより、新しい値`claim-check`が追加されます。 `claim-check`に設定すると、TiCDC Kafka シンクは、メッセージ サイズが制限を超えた場合に外部storageへのメッセージの送信をサポートし、外部storage内のこの大きなメッセージのアドレスを含むメッセージを Kafka に送信します。 |

## 廃止された機能 {#deprecated-features}

-   [マイダンパー](https://docs.pingcap.com/tidb/v4.0/mydumper-overview) v7.5.0 で非推奨となり、その機能のほとんどは[Dumpling](/dumpling-overview.md)に置き換えられました。 mydumper の代わりにDumpling を使用することを強くお勧めします。
-   TiKV インポーターは v7.5.0 で非推奨になります。代わりに[TiDB Lightningの物理インポート モード](/tidb-lightning/tidb-lightning-physical-import-mode.md)を使用することを強くお勧めします。

## 改善点 {#improvements}

-   TiDB

    -   パーティション化されたテーブルに対する`ANALYZE`オペレーションのメモリ使用量とパフォーマンスを最適化する[#47071](https://github.com/pingcap/tidb/issues/47071) [#47104](https://github.com/pingcap/tidb/issues/47104) [#46804](https://github.com/pingcap/tidb/issues/46804) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   統計ガベージコレクション[#31778](https://github.com/pingcap/tidb/issues/31778) @ [ウィノロス](https://github.com/winoros)のメモリ使用量とパフォーマンスを最適化します。
    -   インデックス マージ交差のプッシュダウン`limit`最適化して、クエリ パフォーマンス[#46863](https://github.com/pingcap/tidb/issues/46863) @ [アイリンキッド](https://github.com/AilinKid)を向上させます。
    -   コスト モデルを改善して、 `IndexLookup`のテーブル取得タスク[#45132](https://github.com/pingcap/tidb/issues/45132) @ [qw4990](https://github.com/qw4990)が含まれる場合に、誤ってフル テーブル スキャンを選択する可能性を最小限に抑えます。
    -   結合除去ルールを最適化して、 `join on unique keys` [#46248](https://github.com/pingcap/tidb/issues/46248) @ [修正データベース](https://github.com/fixdb)のクエリ パフォーマンスを向上させます。
    -   実行失敗を避けるために、複数値インデックス列の照合順序を`binary`に変更します[#46717](https://github.com/pingcap/tidb/issues/46717) @ [ヤンケオ](https://github.com/YangKeao)

-   TiKV

    -   OOM [#15458](https://github.com/tikv/tikv/issues/15458) @ [オーバーヴィーナス](https://github.com/overvenus)を防ぐためにリゾルバーのメモリ使用量を最適化します。
    -   Router オブジェクトの LRUCache を削除してメモリ使用量を削減し、OOM [#15430](https://github.com/tikv/tikv/issues/15430) @ [コナー1996](https://github.com/Connor1996)を防止します。
    -   TiCDC Resolver [#15412](https://github.com/tikv/tikv/issues/15412) @ [オーバーヴィーナス](https://github.com/overvenus)のメモリ使用量を削減
    -   RocksDB の圧縮[#15324](https://github.com/tikv/tikv/issues/15324) @ [オーバーヴィーナス](https://github.com/overvenus)によって引き起こされるメモリの変動を軽減します。
    -   Partitioned Raft KV [#15269](https://github.com/tikv/tikv/issues/15269) @ [オーバーヴィーナス](https://github.com/overvenus)のフロー制御モジュールのメモリ消費量を削減
    -   接続再試行のプロセスで PD クライアントのバックオフ メカニズムを追加します。これにより、エラー再試行中の再試行間隔が徐々に増加し、PD プレッシャー[#15428](https://github.com/tikv/tikv/issues/15428) @ [ノールーシュ](https://github.com/nolouch)が軽減されます。
    -   RocksDB [#15424](https://github.com/tikv/tikv/issues/15424) @ [グロルフ](https://github.com/glorv)の`background_compaction`を動的に調整するサポート

-   PD

    -   TSO トレース情報を最適化して、TSO 関連の問題の調査を容易にする[#6856](https://github.com/tikv/pd/pull/6856) @ [ティエンチャイアマオ](https://github.com/tiancaiamao)
    -   メモリ使用量を削減するための HTTP クライアント接続の再利用をサポート[#6913](https://github.com/tikv/pd/issues/6913) @ [ノールーシュ](https://github.com/nolouch)
    -   バックアップ クラスターが切断されたときにクラスター ステータスを自動的に更新する PD の速度が向上しました[#6883](https://github.com/tikv/pd/issues/6883) @ [ディスク化](https://github.com/disksing)
    -   リソース制御クライアントの構成取得方法を強化し、最新の構成を動的に取得できるようにしました[#7043](https://github.com/tikv/pd/issues/7043) @ [ノールーシュ](https://github.com/nolouch)

-   TiFlash

    -   TiFlash書き込みプロセス[#7564](https://github.com/pingcap/tiflash/issues/7564) @ [カルビンネオ](https://github.com/CalvinNeo)のスピル ポリシーを最適化することで、ランダム書き込みワークロード中の書き込みパフォーマンスを向上させます。
    -   TiFlash [#8068](https://github.com/pingcap/tiflash/issues/8068) @ [カルビンネオ](https://github.com/CalvinNeo)のRaftレプリケーション プロセスに関するメトリクスを追加します。
    -   ファイル システムの i ノード[#7595](https://github.com/pingcap/tiflash/issues/7595) @ [ホンユニャン](https://github.com/hongyunyan)が枯渇する可能性を避けるために、小さなファイルの数を減らします。

-   ツール

    -   バックアップと復元 (BR)

        -   リージョンリーダーの移行が発生したときに PITR ログ バックアップの進行状況のレイテンシーが増加する問題を緩和します[#13638](https://github.com/tikv/tikv/issues/13638) @ [ユジュンセン](https://github.com/YuJuncen)
        -   HTTP クライアント[#46011](https://github.com/pingcap/tidb/issues/46011) @ [レヴルス](https://github.com/Leavrth)で`MaxIdleConns`および`MaxIdleConnsPerHost`パラメータを設定することにより、ログ バックアップおよび PITR 復元タスクの接続再利用のサポートを強化します。
        -   PD または外部 S3storage[#42909](https://github.com/pingcap/tidb/issues/42909) @ [レヴルス](https://github.com/Leavrth)への接続に失敗した場合のBRのフォールト トレランスを向上させます。
        -   新しい復元パラメータを追加します`WaitTiflashReady` 。このパラメータが有効な場合、 TiFlashレプリカが正常に複製された後に復元操作が完了します[#43828](https://github.com/pingcap/tidb/issues/43828) [#46302](https://github.com/pingcap/tidb/issues/46302) @ [3ポインター](https://github.com/3pointer)
        -   ログバックアップの CPU オーバーヘッドを削減`resolve lock` [#40759](https://github.com/pingcap/tidb/issues/40759) @ [3ポインター](https://github.com/3pointer)

    -   TiCDC

        -   `ADD INDEX` DDL 操作を複製する実行ロジックを最適化して、後続の DML ステートメントのブロックを回避します[#9644](https://github.com/pingcap/tiflow/issues/9644) @ [スドジ](https://github.com/sdojjy)

    -   TiDB Lightning

        -   リージョン分散フェーズ[#46203](https://github.com/pingcap/tidb/issues/46203) @ [ミタルリシャブ](https://github.com/mittalrishabh)中のTiDB Lightningの再試行ロジックを最適化します。
        -   データ インポート フェーズ[#46253](https://github.com/pingcap/tidb/issues/46253) @ [ランス6716](https://github.com/lance6716)中の`no leader`エラーに対するTiDB Lightningの再試行ロジックを最適化します。

## バグの修正 {#bug-fixes}

-   TiDB

    -   ハッシュ パーティション[#45889](https://github.com/pingcap/tidb/issues/45889) @ [定義2014](https://github.com/Defined2014)ではないテーブルに対して`BatchPointGet`演算子が誤った結果を返す問題を修正します。
    -   `BatchPointGet`演算子がハッシュ パーティション テーブル[#46779](https://github.com/pingcap/tidb/issues/46779) @ [ジフフスト](https://github.com/jiyfhust)に対して誤った結果を返す問題を修正
    -   TiDB パーサーが状態のままになり、解析エラー[#45898](https://github.com/pingcap/tidb/issues/45898) @ [qw4990](https://github.com/qw4990)が発生する問題を修正します。
    -   `EXCHANGE PARTITION`が制約[#45922](https://github.com/pingcap/tidb/issues/45922) @ [むじょん](https://github.com/mjonss)をチェックしない問題を修正
    -   `tidb_enforce_mpp`システム変数が正しく復元できない問題を修正[#46214](https://github.com/pingcap/tidb/issues/46214) @ [djshow832](https://github.com/djshow832)
    -   `LIKE`節の`_` [#46287](https://github.com/pingcap/tidb/issues/46287) [#46618](https://github.com/pingcap/tidb/issues/46618) @ [定義2014](https://github.com/Defined2014)と誤って処理される問題を修正
    -   TiDB がスキーマ[#46325](https://github.com/pingcap/tidb/issues/46325) @ [ヒヒヒヒヒ](https://github.com/hihihuhu)の取得に失敗した場合に`schemaTs`が 0 に設定される問題を修正
    -   `AUTO_ID_CACHE=1`を[#46444](https://github.com/pingcap/tidb/issues/46444) @ [ティエンチャイアマオ](https://github.com/tiancaiamao)に設定すると`Duplicate entry`発生する場合がある問題を修正
    -   `AUTO_ID_CACHE=1`を[#46454](https://github.com/pingcap/tidb/issues/46454) @ [ティエンチャイアマオ](https://github.com/tiancaiamao)に設定すると、panic後の TiDB の回復が遅くなる問題を修正
    -   `AUTO_ID_CACHE=1`が[#46545](https://github.com/pingcap/tidb/issues/46545) @ [ティエンチャイアマオ](https://github.com/tiancaiamao)に設定されている場合、 `SHOW CREATE TABLE`の`next_row_id`が正しくない問題を修正
    -   サブクエリ[#45838](https://github.com/pingcap/tidb/issues/45838) @ [djshow832](https://github.com/djshow832)で CTE を使用するときに解析中に発生するpanicの問題を修正します。
    -   `EXCHANGE PARTITION`失敗するかキャンセルされると、パーティション テーブルに対する制限が元のテーブルに残る問題を修正します[#45920](https://github.com/pingcap/tidb/issues/45920) [#45791](https://github.com/pingcap/tidb/issues/45791) @ [むじょん](https://github.com/mjonss)
    -   リスト パーティションの定義で`NULL`と空の文字列[#45694](https://github.com/pingcap/tidb/issues/45694) @ [むじょん](https://github.com/mjonss)の両方の使用がサポートされていない問題を修正します。
    -   パーティション交換[#46492](https://github.com/pingcap/tidb/issues/46492) @ [むじょん](https://github.com/mjonss)時にパーティション定義に準拠しないデータを検出できない問題を修正
    -   `tmp-storage-quota`設定が有効にならない問題を修正[#45161](https://github.com/pingcap/tidb/issues/45161) [#26806](https://github.com/pingcap/tidb/issues/26806) @ [wshwsh12](https://github.com/wshwsh12)
    -   `WEIGHT_STRING()`関数が照合照合順序[#45725](https://github.com/pingcap/tidb/issues/45725) @ [ドヴィーデン](https://github.com/dveeden)と一致しない問題を修正
    -   インデックス結合のエラーによりクエリがスタックする可能性がある問題を修正します[#45716](https://github.com/pingcap/tidb/issues/45716) @ [wshwsh12](https://github.com/wshwsh12)
    -   `DATETIME`または`TIMESTAMP`列を数値定数[#38361](https://github.com/pingcap/tidb/issues/38361) @ [イービン87](https://github.com/yibin87)と比較するときに動作が MySQL と矛盾する問題を修正
    -   符号なし型と`Duration`型定数[#45410](https://github.com/pingcap/tidb/issues/45410) @ [wshwsh12](https://github.com/wshwsh12)を比較するときに発生する誤った結果を修正しました。
    -   アクセス パス プルーニング ロジックが`READ_FROM_STORAGE(TIFLASH[...])`ヒントを無視し、 `Can't find a proper physical plan`エラー[#40146](https://github.com/pingcap/tidb/issues/40146) @ [アイリンキッド](https://github.com/AilinKid)を引き起こす問題を修正します。
    -   `GROUP_CONCAT`が`ORDER BY`列[#41986](https://github.com/pingcap/tidb/issues/41986) @ [アイリンキッド](https://github.com/AilinKid)を解析できない問題を修正
    -   深くネストされた式に対して HashCode が繰り返し計算され、メモリ使用量が増加し、OOM [#42788](https://github.com/pingcap/tidb/issues/42788) @ [アイリンキッド](https://github.com/AilinKid)が発生する問題を修正します。
    -   CAST に精度の損失がない[#45199](https://github.com/pingcap/tidb/issues/45199) @ [アイリンキッド](https://github.com/AilinKid)のときに、 `cast(col)=range`条件によってフルスキャンが発生する問題を修正します。
    -   MPP 実行プランの Union を介して集計がプッシュダウンされると、結果が正しくない[#45850](https://github.com/pingcap/tidb/issues/45850) @ [アイリンキッド](https://github.com/AilinKid)という問題を修正します。
    -   `in (?)`のバインディングが`in (?, ... ?)` [#44298](https://github.com/pingcap/tidb/issues/44298) @ [qw4990](https://github.com/qw4990)と一致しない問題を修正
    -   `non-prep plan cache`が実行プラン[#47008](https://github.com/pingcap/tidb/issues/47008) @ [qw4990](https://github.com/qw4990)を再利用するときに接続照合照合順序が考慮されないことによって発生するエラーを修正
    -   実行されたプランがプラン キャッシュ[#46159](https://github.com/pingcap/tidb/issues/46159) @ [qw4990](https://github.com/qw4990)にヒットしない場合に警告が報告されない問題を修正します。
    -   `plan replayer dump explain`がエラー[#46197](https://github.com/pingcap/tidb/issues/46197) @ [時間と運命](https://github.com/time-and-fate)を報告する問題を修正
    -   CTE を使用して DML ステートメントを実行するとpanic[#46083](https://github.com/pingcap/tidb/issues/46083) @ [ウィノロス](https://github.com/winoros)が発生する可能性がある問題を修正
    -   2 つのサブクエリ[#46160](https://github.com/pingcap/tidb/issues/46160) @ [qw4990](https://github.com/qw4990)を結合するときに`TIDB_INLJ`ヒントが有効にならない問題を修正
    -   `MERGE_JOIN`の結果が正しくない問題を修正[#46580](https://github.com/pingcap/tidb/issues/46580) @ [qw4990](https://github.com/qw4990)

-   TiKV

    -   Titan が有効になっているときに TiKV が起動できず、 `Blob file deleted twice`エラーが発生する問題を修正します[#15454](https://github.com/tikv/tikv/issues/15454) @ [コナー1996](https://github.com/Connor1996)
    -   スレッド自主監視パネルとスレッド非自主監視パネル[#15413](https://github.com/tikv/tikv/issues/15413) @ [SpadeA-Tang](https://github.com/SpadeA-Tang)にデータがない問題を修正
    -   raftstore-applys [#15371](https://github.com/tikv/tikv/issues/15371) @ [コナー1996](https://github.com/Connor1996)が増加し続けるデータ エラーを修正
    -   リージョン[#13311](https://github.com/tikv/tikv/issues/13311) @ [ジグアン](https://github.com/zyguan)の不正なメタデータによって引き起こされる TiKVpanic問題を修正
    -   `sync_recovery`から`sync` [#15366](https://github.com/tikv/tikv/issues/15366) @ [ノールーシュ](https://github.com/nolouch)に切り替えた後に QPS が 0 に低下する問題を修正
    -   オンライン安全でないリカバリがタイムアウト[#15346](https://github.com/tikv/tikv/issues/15346) @ [コナー1996](https://github.com/Connor1996)で中止されない問題を修正
    -   CpuRecord [#15304](https://github.com/tikv/tikv/issues/15304) @ [オーバーヴィーナス](https://github.com/overvenus)によって引き起こされる潜在的なメモリリークの問題を修正
    -   バックアップ クラスターがダウンし、プライマリ クラスターがクエリされると`"Error 9002: TiKV server timeout"`が発生する問題を修正します[#12914](https://github.com/tikv/tikv/issues/12914) @ [コナー1996](https://github.com/Connor1996)
    -   プライマリ クラスターが[#12320](https://github.com/tikv/tikv/issues/12320) @ [ディスク化](https://github.com/disksing)回復した後に TiKV を再起動すると、バックアップ TiKV がスタックする問題を修正します。

-   PD

    -   Flashback [#6912](https://github.com/tikv/pd/issues/6912) @ [オーバーヴィーナス](https://github.com/overvenus)中にリージョン情報が更新および保存されない問題を修正
    -   ストア設定[#6918](https://github.com/tikv/pd/issues/6918) @ [バッファフライ](https://github.com/bufferflies)の同期が遅いため、PD リーダーの切り替えが遅い問題を修正
    -   Scatter Peers [#6962](https://github.com/tikv/pd/issues/6962) @ [バッファフライ](https://github.com/bufferflies)でグループが考慮されない問題を修正
    -   RU 消費量が 0 未満であると PD がクラッシュする問題を修正します[#6973](https://github.com/tikv/pd/issues/6973) @ [キャビンフィーバーB](https://github.com/CabinfeverB)
    -   変更された分離レベルがデフォルトの配置ルール[#7121](https://github.com/tikv/pd/issues/7121) @ [ルルンクス](https://github.com/rleungx)に同期されない問題を修正します。
    -   クラスターが大きい[#46664](https://github.com/pingcap/tidb/issues/46664) @ [ヒューシャープ](https://github.com/HuSharp)の場合、client-go を定期的`min-resolved-ts`更新すると PD OOM が発生する可能性がある問題を修正

-   TiFlash

    -   Grafana [#7713](https://github.com/pingcap/tiflash/issues/7713) @ [ジェイ・ソン・ファン](https://github.com/JaySon-Huang)で`max_snapshot_lifetime`メトリクスが正しく表示されない問題を修正
    -   最大期間に関する一部のメトリクスが正しくない問題を修正[#8076](https://github.com/pingcap/tiflash/issues/8076) @ [カルビンネオ](https://github.com/CalvinNeo)
    -   TiDB が MPP タスクが失敗したと誤って報告する問題を修正します[#7177](https://github.com/pingcap/tiflash/issues/7177) @ [イービン87](https://github.com/yibin87)

-   ツール

    -   バックアップと復元 (BR)

        -   バックアップ失敗時の誤解を招くエラー メッセージ`resolve lock timeout`が実際のエラーを隠蔽する問題を修正[#43236](https://github.com/pingcap/tidb/issues/43236) @ [ユジュンセン](https://github.com/YuJuncen)
        -   PITR を使用して暗黙的な主キーを回復すると競合が発生する可能性がある問題を修正[#46520](https://github.com/pingcap/tidb/issues/46520) @ [3ポインター](https://github.com/3pointer)
        -   PITR を使用してメタ KV を回復するとエラー[#46578](https://github.com/pingcap/tidb/issues/46578) @ [レヴルス](https://github.com/Leavrth)が発生する可能性がある問題を修正
        -   BR統合テスト ケース[#45561](https://github.com/pingcap/tidb/issues/46561) @ [ピュアリンド](https://github.com/purelind)のエラーを修正

    -   TiCDC

        -   PD のスケールアップおよびスケールダウン中に TiCDC が無効な古いアドレスにアクセスする問題を修正します[#9584](https://github.com/pingcap/tiflow/issues/9584) @ [フビンジ](https://github.com/fubinzh) @ [東門](https://github.com/asddongmen)
        -   一部のシナリオで変更フィードが失敗する問題を修正[#9309](https://github.com/pingcap/tiflow/issues/9309) [#9450](https://github.com/pingcap/tiflow/issues/9450) [#9542](https://github.com/pingcap/tiflow/issues/9542) [#9685](https://github.com/pingcap/tiflow/issues/9685) @ [ひっくり返る](https://github.com/hicqu) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   アップストリーム[#9430](https://github.com/pingcap/tiflow/issues/9430) @ [スドジ](https://github.com/sdojjy)の 1 つのトランザクションで複数の行の一意のキーが変更されると、レプリケーション書き込みの競合が発生する可能性がある問題を修正します。
        -   アップストリーム[#9476](https://github.com/pingcap/tiflow/issues/9476) [#9488](https://github.com/pingcap/tiflow/issues/9488) @ [CharlesCheung96](https://github.com/CharlesCheung96) @ [東門](https://github.com/asddongmen)の同じ DDL ステートメントで複数のテーブルの名前が変更されると、レプリケーション エラーが発生する問題を修正します。
        -   CSV ファイル[#9609](https://github.com/pingcap/tiflow/issues/9609) @ [CharlesCheung96](https://github.com/CharlesCheung96)で中国語の文字が検証されない問題を修正
        -   すべての変更フィードが削除された後、上流の TiDB GC がブロックされる問題を修正[#9633](https://github.com/pingcap/tiflow/issues/9633) @ [スドジ](https://github.com/sdojjy)
        -   `scale-out`が有効になっている場合、 [#9665](https://github.com/pingcap/tiflow/issues/9665) @ [スドジ](https://github.com/sdojjy)の場合にノード間で書き込みキーが不均等に分散される問題を修正します。
        -   機密ユーザー情報がログ[#9690](https://github.com/pingcap/tiflow/issues/9690) @ [スドジ](https://github.com/sdojjy)に記録される問題を修正

    -   TiDB データ移行 (DM)

        -   DM が大文字と小文字を区別しない照合順序[#9489](https://github.com/pingcap/tiflow/issues/9489) @ [ヒヒヒヒヒ](https://github.com/hihihuhu)との競合を正しく処理できない問題を修正します。
        -   DM バリデーターのデッドロック問題を修正し、再試行[#9257](https://github.com/pingcap/tiflow/issues/9257) @ [D3ハンター](https://github.com/D3Hunter)を強化しました。
        -   失敗した DDL がスキップされ、後続の DDL が実行されない場合、DM から返されるレプリケーション ラグが増大し続ける問題を修正します[#9605](https://github.com/pingcap/tiflow/issues/9605) @ [D3ハンター](https://github.com/D3Hunter)
        -   オンライン DDL [#9587](https://github.com/pingcap/tiflow/issues/9587) @ [GMHDBJD](https://github.com/GMHDBJD)をスキップすると、DM がアップストリーム テーブル スキーマを適切に追跡できない問題を修正します。
        -   楽観的モード[#9588](https://github.com/pingcap/tiflow/issues/9588) @ [GMHDBJD](https://github.com/GMHDBJD)でタスクを再開すると、DM がすべての DML をスキップする問題を修正します。
        -   DM が楽観的モード[#9788](https://github.com/pingcap/tiflow/issues/9788) @ [GMHDBJD](https://github.com/GMHDBJD)でパーティション DDL をスキップする問題を修正

    -   TiDB Lightning

        -   TiDB Lightning がテーブル`NONCLUSTERED auto_increment`とテーブル`AUTO_ID_CACHE=1`をインポートした後、データを挿入するとエラーが返される問題を修正します[#46100](https://github.com/pingcap/tidb/issues/46100) @ [ティエンチャイアマオ](https://github.com/tiancaiamao)
        -   `checksum = "optional"` [#45382](https://github.com/pingcap/tidb/issues/45382) @ [lyzx2001](https://github.com/lyzx2001)の場合でもチェックサムがエラーを報告する問題を修正
        -   PDクラスタアドレスが[#43436](https://github.com/pingcap/tidb/issues/43436) @ [リチュンジュ](https://github.com/lichunzhu)に変更されるとデータインポートが失敗する問題を修正

## 貢献者 {#contributors}

TiDB コミュニティの以下の貢献者に感謝いたします。

-   [あいでんどう](https://github.com/aidendou)
-   [コードプレイ](https://github.com/coderplay)
-   [ファティレイ](https://github.com/fatelei)
-   [ハイポン](https://github.com/highpon)
-   [ヒヒヒヒヒ](https://github.com/hihihuhu) (初投稿者)
-   [イザベラ0428](https://github.com/isabella0428)
-   [ジフフスト](https://github.com/jiyfhust)
-   [JK1張](https://github.com/JK1Zhang)
-   [ジョーカー53-1](https://github.com/joker53-1) (初投稿者)
-   [L-カエデ](https://github.com/L-maple)
-   [ミタルリシャブ](https://github.com/mittalrishabh)
-   [舗装路](https://github.com/paveyry)
-   [ショーン0915](https://github.com/shawn0915)
-   [テデュ](https://github.com/tedyu)
-   [ヤムチナ](https://github.com/yumchina)
-   [ジュオハオヘ](https://github.com/ZhuohaoHe)
