---
title: TiDB 8.5.0 Release Notes
summary: TiDB 8.5.0 の新機能、互換性の変更、改善、バグ修正について説明します。
---

# TiDB 8.5.0 リリースノート {#tidb-8-5-0-release-notes}

<EmailSubscriptionWrapper />

発売日: 2024年12月19日

TiDB バージョン: 8.5.0

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v8.5/quick-start-with-tidb) | [実稼働環境への導入](https://docs.pingcap.com/tidb/v8.5/production-deployment-using-tiup)

TiDB 8.5.0 は長期サポートリリース (LTS) です。

以前の LTS 8.1.0 と比較して、8.5.0 には、 [8.2.0-DMR](/releases/release-8.2.0.md) 、 [8.3.0-DMR](/releases/release-8.3.0.md) 、 [8.4.0-DMR](/releases/release-8.4.0.md)でリリースされた新機能、改善、バグ修正が含まれています。8.1.x から 8.5.0 にアップグレードする場合、 [TiDB リリースノート PDF](https://docs-download.pingcap.com/pdf/tidb-v8.2-to-v8.5-en-release-notes.pdf)をダウンロードして、2 つの LTS バージョン間のすべてのリリース ノートを表示できます。次の表に、8.1.0 から 8.5.0 への主な変更点を示します。

<table><thead><tr><th>カテゴリ</th><th>機能/拡張機能</th><th>説明</th></tr></thead><tbody><tr><td rowspan="7">スケーラビリティとパフォーマンス</td><td>複数の次元でデータ処理のレイテンシーを削減</td><td>TiDB は、データ処理を継続的に改良してパフォーマンスを向上させ、金融シナリオにおける低レイテンシの SQL 処理要件を効果的に満たします。主な更新内容は次のとおりです。<li> <a href="https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_executor_concurrency-new-in-v50">並列ソート</a>をサポート（v8.2.0 で導入）</li><li> <a href="https://docs.pingcap.com/tidb/v8.5/tidb-configuration-file#batch-policy-new-in-v830">KV (キー値) リクエストのバッチ処理戦略</a>を最適化 (v8.3.0 で導入)</li><li> <a href="https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_tso_client_rpc_mode-new-in-v840">TSO リクエストの並列モード</a>をサポート (v8.4.0 で導入)</li><li> <a href="https://docs.pingcap.com/tidb/v8.5/sql-statement-delete">DELETE</a>操作のリソース オーバーヘッドを削減 (v8.4.0 で導入)</li><li><a href="https://docs.pingcap.com/tidb/v8.5/cached-tables">キャッシュされたテーブル</a>のクエリ パフォーマンスを向上 (v8.4.0 で導入)</li><li><a href="https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_hash_join_version-new-in-v840">ハッシュ結合の最適化バージョン</a>を導入します (実験的、v8.4.0 で導入)</li></td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v8.5/tikv-in-memory-engine">TiKV MVCC インメモリ エンジン (IME)</a> (v8.5.0 で導入)</td><td> TiKV MVCC インメモリ エンジンは、最新の MVCC バージョンのデータをメモリにキャッシュし、TiKV が古いバージョンをすばやくスキップして最新のデータを取得できるようにします。この機能により、データ レコードが頻繁に更新されるシナリオや、履歴バージョンが長期間保持されるシナリオで、データ スキャンのパフォーマンスが大幅に向上します。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v8.5/tune-region-performance#use-the-active-pd-follower-feature-to-enhance-the-scalability-of-pds-region-information-query-service">アクティブ PD フォロワーを使用して PD のリージョン情報クエリ サービスを強化します</a>(v8.5.0 で GA)</td><td> TiDB v7.6.0 では、PD フォロワーがリージョン情報クエリ サービスを提供できるようにする実験的機能「Active PD Follower 」が導入されています。この機能により、多数の TiDB ノードとリージョンを持つクラスターで<code>GetRegion</code>および<code>ScanRegions</code>要求を処理する PD クラスターの機能が向上し、PD リーダーの CPU 負荷が軽減されます。v8.5.0 では、この機能が一般提供 (GA) されます。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_enable_instance_plan_cache-new-in-v840">インスタンスレベルの実行プラン キャッシュ</a>(実験的、v8.4.0 で導入)</td><td>インスタンス レベルのプラン キャッシュを使用すると、同じ TiDB インスタンス内のすべてのセッションでプラン キャッシュを共有できます。セッション レベルのプラン キャッシュと比較すると、この機能では、より多くの実行プランをメモリにキャッシュすることで SQL コンパイル時間が短縮され、全体的な SQL 実行時間が短縮されます。これにより、OLTP のパフォーマンスとスループットが向上し、メモリ使用量の制御が向上し、データベースの安定性が向上します。</td></tr><tr><td><a href="https://docs.pingcap.com/tidb/v8.5/partitioned-table#global-indexes">パーティションテーブルのグローバル インデックス</a>(v8.4.0 で GA)</td><td>グローバル インデックスを使用すると、パーティション化されていない列の取得効率を効果的に向上させ、一意のキーにパーティション キーが含まれていなければならないという制限を排除できます。この機能により、TiDB パーティション テーブルの使用シナリオが拡張され、パーティション テーブルのパフォーマンスが向上し、特定のクエリ シナリオでのリソース消費が削減されます。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_opt_projection_push_down-new-in-v610">storage演算子の<code>Projection</code>エンジンへのデフォルトのプッシュダウン</a>(v8.3.0 で導入)</td><td> <code>Projection</code>演算子をstorageエンジンにプッシュダウンすると、ノード間のデータ転送を減らしながら、storageノード間で負荷を分散できます。この最適化により、特定の SQL クエリの実行時間が短縮され、データベース全体のパフォーマンスが向上します。</td></tr><tr><td><a href="https://docs.pingcap.com/tidb/v8.5/statistics#collect-statistics-on-some-columns">統計を収集する際に不要な列を無視する</a>(v8.3.0 で導入)</td><td> TiDB は、オプティマイザが必要な情報を確実に取得できるという前提の下、統計収集を高速化し、統計の適時性を向上させ、最適な実行プランが選択されるようにすることで、クラスターのパフォーマンスを向上させます。同時に、TiDB はシステム オーバーヘッドを削減し、リソースの使用率を向上させます。</td></tr><tr><td rowspan="5">信頼性と可用性</td><td>大規模クラスタの安定性を向上</td><td>TiDB を使用してマルチテナントまたは SaaS アプリケーションを実行する企業では、多くの場合、多数のテーブルを保存する必要があります。v8.5.0 では、TiDB によって大規模クラスターの安定性が大幅に向上します。<li><a href="https://docs.pingcap.com/tidb/v8.5/schema-cache">スキーマ キャッシュ制御</a>と<a href="https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_stats_cache_mem_quota-new-in-v610">TiDB 統計キャッシュのメモリクォータの設定</a>が一般提供 (GA) され、過剰なメモリ消費によって発生する安定性の問題が軽減されます。</li><li> PD は、多数のリージョンによってもたらされる負荷に対処するために<a href="https://docs.pingcap.com/tidb/v8.5/tune-region-performance#use-the-active-pd-follower-feature-to-enhance-the-scalability-of-pds-region-information-query-service">Active Follower を</a>導入し、 <a href="https://docs.pingcap.com/tidb/v8.5/pd-microservices">PD によって処理されるサービスを徐々に分離して</a>独立した展開を実現します。</li><li> PD はリージョンハートビート処理のパフォーマンスを向上させ、単一のクラスターに対して数千万のリージョンをサポートします。</li><li> <a href="https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_auto_analyze_concurrency-new-in-v840">同時実行性を高め</a>、<a href="https://docs.pingcap.com/tidb/v8.5/statistics#collect-statistics-on-some-columns">収集されるオブジェクトの数を減らすこと</a>で、統計の収集と読み込みの効率を向上させ、大規模なクラスターでの実行プランの安定性を確保できます。</li></td></tr><tr><td><a href="https://docs.pingcap.com/tidb/v8.5/tidb-resource-control#query_limit-parameters">ランナウェイクエリのトリガーをさらにサポートし、リソースグループの切り替えをサポートします</a>(v8.4.0 で導入)</td><td>ランナウェイ クエリは、予期しない SQL パフォーマンスの問題がシステムに与える影響を軽減する効果的な方法を提供します。TiDB v8.4.0 では、コプロセッサーによって処理されたキーの数 ( <code>PROCESSED_KEYS</code> ) と要求単位 ( <code>RU</code> ) が識別条件として導入され、識別されたクエリが指定されたリソース グループに配置されるため、ランナウェイ クエリをより正確に識別して制御できます。</td></tr><tr><td><a href="https://docs.pingcap.com/tidb/v8.5/tidb-resource-control#background-parameters">リソース制御のバックグラウンド タスクのリソース使用量の上限設定をサポート</a>(実験的、v8.4.0 で導入)</td><td>リソース制御のバックグラウンド タスクに最大パーセンテージ制限を設定することで、さまざまなアプリケーション システムのニーズに基づいてリソース消費を制御できます。これにより、バックグラウンド タスクの消費を低いレベルに抑え、オンライン サービスの品質を確保できます。</td></tr><tr><td> TiProxyの使用例を強化および拡張する</td><td>TiDB の高可用性の重要なコンポーネントとして、 <a href="https://docs.pingcap.com/tidb/v8.5/tiproxy-overview">TiProxy は</a>SQL トラフィックのアクセスと転送を超えて機能を拡張し、クラスターの変更評価をサポートします。主な機能は次のとおりです。<li> <a href="https://docs.pingcap.com/tidb/v8.5/tiproxy-traffic-replay">TiProxy はトラフィックのキャプチャと再生をサポートします</a>(実験的、v8.4.0 で導入)</li><li> <a href="https://docs.pingcap.com/tidb/v8.5/tiproxy-overview">TiProxy は組み込みの仮想 IP 管理をサポートします</a>(v8.3.0 で導入)</li><li> <a href="https://docs.pingcap.com/tidb/v8.5/tiproxy-load-balance">TiProxy は複数の負荷分散ポリシーをサポートします</a>(v8.2.0 で導入)</li></td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_enable_parallel_hashagg_spill-new-in-v800">TiDB の並列 HashAgg アルゴリズムはディスク スピルをサポートします</a>(v8.2.0 で GA)</td><td> HashAgg は、同じフィールド値を持つ行を効率的に集計するために TiDB で広く使用されている集計演算子です。TiDB v8.0.0 では、処理速度をさらに向上させるための実験的機能として並列 HashAgg が導入されています。メモリリソースが不足している場合、並列 HashAgg は一時的にソートされたデータをディスクに書き出し、過剰なメモリ使用によって発生する潜在的な OOM リスクを回避します。これにより、ノードの安定性を維持しながらクエリ パフォーマンスが向上します。v8.2.0 では、この機能が一般提供 (GA) され、デフォルトで有効になっているため、 <code>tidb_executor_concurrency</code>を使用して並列 HashAgg の同時実行を安全に構成できます。</td></tr><tr><td rowspan="2">構文</td><td><a href="https://docs.pingcap.com/tidb/v8.5/foreign-key">外部キー</a>(v8.5.0 で GA)</td><td>外部キーは、テーブル間の関係を確立し、データの一貫性と整合性を保証するデータベースの制約です。外部キーは、子テーブルで参照されるデータが親テーブルに存在することを保証し、無効なデータの挿入を防止します。外部キーはカスケード操作 (削除または更新時の自動同期など) もサポートし、ビジネス ロジックの実装を簡素化し、データ関係を手動で維持する複雑さを軽減します。</td></tr><tr><td><a href="https://docs.pingcap.com/tidb/v8.5/vector-search-overview">ベクトル検索</a>(実験的、v8.4.0 で導入)</td><td>ベクトル検索は、データセマンティクスに基づく検索方法であり、より関連性の高い検索結果を提供します。AI と大規模言語モデル (LLM) のコア関数の 1 つとして、ベクトル検索は、検索拡張生成 (RAG)、セマンティック検索、推奨システムなど、さまざまなシナリオで使用できます。</td></tr><tr><td rowspan="3"> DB 操作と可観測性</td><td><a href="https://docs.pingcap.com/tidb/v8.5/information-schema-processlist">メモリテーブルに TiKV および TiDB CPU 時間を表示する</a>(v8.4.0 で導入)</td><td> CPU 時間がシステム テーブルに統合され、セッションや SQL の他のメトリックと一緒に表示されるようになったため、CPU 消費量の多い操作を複数の観点から観察し、診断の効率を向上させることができます。これは、インスタンス内の CPU スパイクやクラスター内の読み取り/書き込みホットスポットなどのシナリオを診断する場合に特に便利です。</td></tr><tr><td><a href="https://docs.pingcap.com/tidb/v8.5/top-sql#use-top-sql">テーブルまたはデータベースごとに集計された TiKV CPU 時間の表示をサポート</a>(v8.4.0 で導入)</td><td>ホットスポットの問題が個々の SQL ステートメントによって発生していない場合は、 Top SQLのテーブルまたはデータベース レベル別に集計された CPU 時間を使用すると、ホットスポットの原因となっているテーブルまたはアプリケーションを迅速に特定できるため、ホットスポットと CPU 消費の問題の診断効率が大幅に向上します。</td></tr><tr><td><a href="https://docs.pingcap.com/tidb/v8.5/backup-and-restore-overview">バックアップと復元 (BR) は、</a> <a href="https://aws.amazon.com/sdk-for-rust/">AWS SDK for Rust を</a>使用して外部storageにアクセスします (v8.5.0 で導入)</td><td> BR は、TiKV から Amazon S3 などの外部storageにアクセスするために、元の Rusoto ライブラリを<a href="https://aws.amazon.com/sdk-for-rust/">AWS SDK for Rust</a>に置き換えます。この変更により、 <a href="https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html">IMDSv2</a>や<a href="https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html">EKS Pod Identity</a>などの AWS 機能との互換性が向上します。</td></tr><tr><td rowspan="1">Security</td><td><a href="https://docs.pingcap.com/tidb/v8.5/br-snapshot-manual#encrypt-the-backup-data">スナップショット バックアップ データ</a>と<a href="https://docs.pingcap.com/tidb/v8.5/br-pitr-manual#encrypt-log-backup-data">ログ バックアップ データ</a>のクライアント側暗号化 (v8.5.0 で GA)</td><td>バックアップ データをバックアップstorageにアップロードする前に、バックアップ データを暗号化して、storage中および転送中のセキュリティを確保できます。</td></tr></tbody></table>

## 機能の詳細 {#feature-details}

### スケーラビリティ {#scalability}

-   スキーマ キャッシュのメモリ制限の設定が一般提供 (GA) されました。テーブル数が数十万、あるいは数百万に達すると、この機能によりスキーマ メタデータのメモリ使用量が大幅に削減されます[＃50959](https://github.com/pingcap/tidb/issues/50959) @ [天菜まお](https://github.com/tiancaiamao) @ [翻訳:](https://github.com/wjhuang2016) @ [翻訳者](https://github.com/gmhdbjd) @ [タンジェンタ](https://github.com/tangenta)

    SaaS シナリオによっては、テーブルの数が数十万、あるいは数百万に達する場合があり、スキーマ メタデータが大量のメモリを消費することがあります。この機能を有効にすると、TiDB は Least Recently Used (LRU) アルゴリズムを使用して対応するスキーマ メタデータをキャッシュして削除し、メモリ使用量を効果的に削減します。

    v8.4.0 以降では、この機能はデフォルトで有効になっており、デフォルト値は`536870912` (つまり 512 MiB) です。必要に応じて変数[`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-new-in-v800)使用して調整できます。

    詳細については[ドキュメント](/schema-cache.md)参照してください。

-   PDのリージョン情報クエリサービス（GA） [＃7431](https://github.com/tikv/pd/issues/7431) @ [ok江](https://github.com/okJiang)のスケーラビリティを強化するために、アクティブPDFollower機能を提供します。

    多数のリージョンを持つ TiDB クラスターでは、ハートビートの処理とタスクのスケジュール設定のオーバーヘッドが増加するため、PD リーダーの CPU 負荷が高くなる可能性があります。クラスターに多数の TiDB インスタンスがあり、リージョン情報に対する要求の同時実行性が高い場合、PD リーダーの CPU 負荷がさらに増加し​​、PD サービスが利用できなくなる可能性があります。

    高可用性を確保するために、TiDB v7.6.0 では、PD のリージョン情報クエリ サービスのスケーラビリティを強化する実験的機能として Active PD Follower が導入されています。v8.5.0 では、この機能が一般提供 (GA) されます。システム変数[`pd_enable_follower_handle_region`](/system-variables.md#pd_enable_follower_handle_region-new-in-v760)を`ON`に設定することで、Active PD Follower機能を有効にすることができます。この機能を有効にすると、TiDB はリージョン情報要求をすべての PD サーバーに均等に分散し、PD フォロワーもリージョン要求を処理できるため、PD リーダーの CPU 負荷が軽減されます。

    詳細については[ドキュメント](/tune-region-performance.md#use-the-active-pd-follower-feature-to-enhance-the-scalability-of-pds-region-information-query-service)参照してください。

### パフォーマンス {#performance}

-   TiDB によるテーブル作成の高速化が一般提供 (GA) され、データ移行とクラスター初期化時間が大幅に短縮されます[＃50052](https://github.com/pingcap/tidb/issues/50052) @ [D3ハンター](https://github.com/D3Hunter) @ [翻訳者](https://github.com/gmhdbjd)

    TiDB v7.6.0 では、システム変数[`tidb_ddl_version`](https://docs.pingcap.com/tidb/v7.6/system-variables#tidb_ddl_version-new-in-v760)によって制御される高速テーブル作成が実験的機能として導入されています。v8.0.0 以降では、このシステム変数の名前が[`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-new-in-v800)に変更されています。

    v8.5.0 では、TiDB の高速テーブル作成が一般提供 (GA) され、デフォルトで有効になっています。この機能は、データ移行およびクラスターの初期化中に、数百万のテーブルの迅速な作成をサポートし、操作時間を大幅に短縮します。

    詳細については[ドキュメント](/accelerated-table-creation.md)参照してください。

-   TiKVはMVCCインメモリエンジン（IME）をサポートしており、広範なMVCC履歴バージョン[＃16141](https://github.com/tikv/tikv/issues/16141) @ [スペードA-タン](https://github.com/SpadeA-Tang) @ [栄光](https://github.com/glorv) @ [金星の上](https://github.com/overvenus)のスキャンを含むクエリを高速化します。

    レコードが頻繁に更新される場合、または TiDB が履歴バージョンを長期間 (たとえば 24 時間) 保持する必要がある場合、MVCC バージョンの蓄積によってスキャン パフォーマンスが低下する可能性があります。TiKV MVCC インメモリ エンジンは、最新の MVCC バージョンをメモリにキャッシュし、高速 GC メカニズムを使用して履歴バージョンをメモリから削除することで、スキャン パフォーマンスを向上させます。

    v8.5.0 以降、TiKV では MVCC インメモリ エンジンが導入されています。TiKV クラスター内の MVCC バージョンの蓄積によってスキャン パフォーマンスが低下する場合は、TiKV 構成パラメータ[`in-memory-engine.enable`](/tikv-in-memory-engine.md#usage)を設定することで、TiKV MVCC インメモリ エンジンを有効にしてスキャン パフォーマンスを向上させることができます。

    詳細については[ドキュメント](/tikv-in-memory-engine.md)参照してください。

### 信頼性 {#reliability}

-   PD [＃5739](https://github.com/tikv/pd/issues/5739) @ [rleungx](https://github.com/rleungx)で処理されるリクエストの最大レートと同時実行数の制限をサポート

    PD に突然大量のリクエストが送信されると、ワークロードが増大し、PD のパフォーマンスに影響を及ぼす可能性があります。v8.5.0 以降では、 [`pd-ctl`](/pd-control.md)使用して PD によって処理されるリクエストの最大レートと同時実行性を制限し、PD の安定性を向上させることができます。

    詳細については[ドキュメント](/pd-control.md)参照してください。

### 構文 {#sql}

-   外部キーのサポート (GA) [＃36982](https://github.com/pingcap/tidb/issues/36982) @ [ヤンケオ](https://github.com/YangKeao) @ [クレイジーcs520](https://github.com/crazycs520)

    外部キー機能は、v8.5.0 で一般提供 (GA) されます。外部キー制約は、データの一貫性と整合性を確保するのに役立ちます。カスケード更新と削除のサポートにより、テーブル間の外部キー関係を簡単に確立でき、データ管理が簡素化されます。この機能により、複雑なデータ関係を持つアプリケーションのサポートが強化されます。

    詳細については[ドキュメント](/foreign-key.md)参照してください。

-   DDLジョブのオンライン変更をサポートするために`ADMIN ALTER DDL JOBS`ステートメントを導入する[＃57229](https://github.com/pingcap/tidb/issues/57229) @ [ふーふー](https://github.com/fzzf678) @ [タンジェンタ](https://github.com/tangenta)

    v8.3.0 以降では、変数[`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size)と[`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt)セッション レベルで設定できます。その結果、これら 2 つの変数をグローバルに設定しても、実行中のすべての DDL ジョブには影響しなくなりました。これらの変数の値を変更するには、まず DDL ジョブをキャンセルし、変数を調整してから、ジョブを再送信する必要があります。

    TiDB v8.5.0 では`ADMIN ALTER DDL JOBS`ステートメントが導入され、特定の DDL ジョブの変数値をオンラインで調整できるようになりました。これにより、リソース消費とパフォーマンスを柔軟にバランスさせることができます。変更は個々のジョブに限定されるため、影響をより制御しやすくなります。例:

    -   `ADMIN ALTER DDL JOBS job_id THREAD = 8;` : 指定された DDL ジョブの`tidb_ddl_reorg_worker_cnt`オンラインで調整します。
    -   `ADMIN ALTER DDL JOBS job_id BATCH_SIZE = 256;` : 指定されたジョブの`tidb_ddl_reorg_batch_size`オンラインで調整します。
    -   `ADMIN ALTER DDL JOBS job_id MAX_WRITE_SPEED = '200MiB';` : 各 TiKV ノードへのインデックス データの書き込みトラフィックをオンラインで調整します。

    詳細については[ドキュメント](/sql-statements/sql-statement-admin-alter-ddl.md)参照してください。

### Security {#security}

-   BRは、フルバックアップデータとログバックアップデータの両方のクライアント側暗号化をサポートします（GA） [＃28640](https://github.com/pingcap/tidb/issues/28640) [＃56433](https://github.com/pingcap/tidb/issues/56433) @ [ジョッカウ](https://github.com/joccau) @ [トリスタン1900](https://github.com/Tristan1900)

    -   完全バックアップ データのクライアント側暗号化 (TiDB v5.3.0 で実験的的に導入) により、カスタム固定キーを使用してクライアント側でバックアップ データを暗号化できるようになります。

    -   ログ バックアップ データのクライアント側暗号化 (TiDB v8.4.0 で実験的的に導入) を使用すると、次のいずれかの方法を使用して、クライアント側でログ バックアップ データを暗号化できます。

        -   カスタム固定キーを使用して暗号化する
        -   ローカルディスクに保存されたマスターキーを使用して暗号化する
        -   キー管理サービス (KMS) によって管理されるマスターキーを使用して暗号化する

    v8.5.0 以降では、両方の暗号化機能が一般提供 (GA) され、クライアント側のデータ セキュリティが強化されます。

    詳細については[バックアップデータを暗号化する](/br/br-snapshot-manual.md#encrypt-the-backup-data)および[ログバックアップデータを暗号化する](/br/br-pitr-manual.md#encrypt-the-log-backup-data)参照してください。

-   保存時の TiKV 暗号化は[Google Cloud キー管理サービス (Google Cloud KMS)](https://cloud.google.com/docs/security/key-management-deep-dive) (GA) [＃8906](https://github.com/tikv/tikv/issues/8906) @ [栄光](https://github.com/glorv)をサポートします

    TiKV は、保存時の暗号化技術を使用して保存データを暗号化することで、データのセキュリティを確保します。この技術の中核となるのは、適切なキー管理です。v8.0.0 では、保存時の TiKV 暗号化は、マスター キー管理に Google Cloud KMS を使用することを試験的にサポートしています。

    v8.5.0 以降では、Google Cloud KMS を使用した保存時の暗号化が一般提供 (GA) されます。この機能を使用するには、まず Google Cloud でキーを作成し、次に TiKV 構成ファイルの`[security.encryption.master-key]`セクションを構成します。

    詳細については[ドキュメント](/encryption-at-rest.md#tikv-encryption-at-rest)参照してください。

## 互換性の変更 {#compatibility-changes}

> **注記：**
>
> このセクションでは、v8.4.0 から現在のバージョン (v8.5.0) にアップグレードするときに知っておく必要のある互換性の変更について説明します。v8.3.0 以前のバージョンから現在のバージョンにアップグレードする場合は、中間バージョンで導入された互換性の変更も確認する必要がある可能性があります。

### 行動の変化 {#behavior-changes}

-   非厳密モード（ `sql_mode = ''` ）では、 `NULL`以外の列に`NULL`値を[＃55457](https://github.com/pingcap/tidb/issues/55457)すると、MySQL互換性のためにエラーが返されるようになりました。7 @ [ジョーチェン](https://github.com/joechenrh)
-   `ALTER TABLE ... DROP FOREIGN KEY IF EXISTS ...`ステートメントはサポートされなくなりました。3 [＃56703](https://github.com/pingcap/tidb/pull/56703) [ヤンケオ](https://github.com/YangKeao)

### システム変数 {#system-variables}

| 変数名                                                                                                 | タイプを変更   | 説明                                                                                                                                                                                                                           |
| --------------------------------------------------------------------------------------------------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-new-in-v800)   | 修正済み     | さらにテストを行った後、デフォルト値を`OFF`から`ON`に変更します。つまり、 [テーブル作成の高速化](/accelerated-table-creation.md)機能はデフォルトで有効になります。                                                                                                                      |
| [`tidb_ddl_reorg_max_write_speed`](/system-variables.md#tidb_ddl_reorg_max_write_speed-new-in-v850) | 新しく追加された | 各 TiKV ノードの書き込み帯域幅を制限し、インデックス作成アクセラレーションが有効になっている場合にのみ有効になります ( [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)変数によって制御されます)。たとえば、変数を`200MiB`に設定すると、最大書き込み速度が 200 MiB/s に制限されます。 |

### コンフィグレーションパラメータ {#configuration-parameters}

| コンフィグレーションファイルまたはコンポーネント | コンフィグレーションパラメータ                                                                                    | タイプを変更   | 説明                                                                                                           |
| ------------------------ | -------------------------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------ |
| ティビ                      | [`deprecate-integer-display-length`](/tidb-configuration-file.md#deprecate-integer-display-length) | 修正済み     | v8.5.0 以降、整数表示幅機能は非推奨になりました。この構成項目のデフォルト値は`false`から`true`に変更されました。                                           |
| ティクヴ                     | [`raft-client-queue-size`](/tikv-configuration-file.md#raft-client-queue-size)                     | 修正済み     | デフォルト値を`8192`から`16384`に変更します。                                                                                |
| PD                       | [`patrol-region-worker-count`](/pd-configuration-file.md#patrol-region-worker-count-new-in-v850)   | 新しく追加された | リージョンのヘルス状態を検査するときにチェッカーによって作成される同時実行[オペレーター](/glossary.md#operator)の数を制御します。                                |
| BR                       | [`--checksum`](/br/br-snapshot-manual.md)                                                          | 修正済み     | デフォルト値を`true`から`false`に変更します。これにより、 BR は、バックアップ パフォーマンスを向上させるために、フル バックアップ中にテーブル レベルのチェックサムをデフォルトで計算しなくなります。 |

## オペレーティング システムとプラットフォームの要件の変更 {#operating-system-and-platform-requirement-changes}

TiDB をアップグレードする前に、オペレーティング システムのバージョンが[OSおよびプラットフォームの要件](/hardware-and-software-requirements.md#os-and-platform-requirements)を満たしていることを確認してください。

-   [CentOS Linux のサポート終了](https://www.centos.org/centos-linux-eol/)によると、CentOS Linux 7 のアップストリームサポートは 2024 年 6 月 30 日に終了します。TiDB は、8.4 DMR バージョンから CentOS 7 のサポートを終了します。Rocky Linux 9.1 以降のバージョンを使用することをお勧めします。CentOS 7 上の TiDB クラスターを v8.4.0 以降にアップグレードすると、クラスターが使用できなくなります。
-   [Red Hat Enterprise Linux ライフサイクル](https://access.redhat.com/support/policy/updates/errata/#Life_Cycle_Dates)によると、Red Hat Enterprise Linux 7 のメンテナンスサポートは 2024 年 6 月 30 日に終了します。TiDB は 8.4 DMR バージョンから Red Hat Enterprise Linux 7 のサポートを終了します。Rocky Linux 9.1 以降のバージョンを使用することをお勧めします。Red Hat Enterprise Linux 7 上の TiDB クラスターを v8.4.0 以降にアップグレードすると、クラスターが使用できなくなります。

## 削除された機能 {#removed-features}

-   以下の機能は削除されました:

    -   v8.4.0 では、 [TiDBBinlog](https://docs.pingcap.com/tidb/v8.3/tidb-binlog-overview)​​削除されました。v8.3.0 以降では、 TiDB Binlog は完全に非推奨です。増分データ レプリケーションの場合は、代わりに[ティCDC](/ticdc/ticdc-overview.md)使用します。ポイントインタイム リカバリ (PITR) の場合は、 [ピトル](/br/br-pitr-guide.md)使用します。TiDB クラスターを v8.4.0 以降のバージョンにアップグレードする前に、必ず TiCDC と PITR に切り替えてください。

-   以下の機能は将来のバージョンで削除される予定です:

    -   v8.0.0 以降、 TiDB Lightning物理インポート モードの[競合検出の旧バージョン](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#the-old-version-of-conflict-detection-deprecated-in-v800)戦略が廃止され、 [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)パラメータを使用して論理インポート モードと物理インポート モードの両方の競合検出戦略を制御できるようになりました。競合検出の旧バージョンの[`duplicate-resolution`](/tidb-lightning/tidb-lightning-configuration.md)パラメータは、将来のリリースで削除される予定です。

## 廃止された機能 {#deprecated-features}

以下の機能は将来のバージョンで廃止される予定です。

-   v8.0.0 では、TiDB は、統計を自動的に収集するタスクの順序を最適化するために優先キューを有効にするかどうかを制御する[`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-new-in-v800)システム変数を導入しています。将来のリリースでは、優先キューが統計を自動的に収集するタスクを順序付ける唯一の方法になるため、このシステム変数は非推奨になります。
-   v7.5.0 では、TiDB に[`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-new-in-v750)システム変数が導入されました。これを使用して、TiDB がパーティション統計の非同期マージを使用して OOM の問題を回避するように設定できます。将来のリリースでは、パーティション統計は非同期にマージされるため、このシステム変数は非推奨になります。
-   以降のリリースでは[実行計画バインディングの自動進化](/sql-plan-management.md#baseline-evolution)再設計する予定であり、関連する変数と動作が変更されます。
-   v8.0.0 では、TiDB は、同時 HashAgg アルゴリズムのディスク スピルをサポートするかどうかを制御する[`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-new-in-v800)システム変数を導入します。将来のバージョンでは、このシステム変数は非推奨になります。
-   v5.1 では、TiDB は、パーティション化されたテーブルに対して動的プルーニング モードを有効にするかどうかを制御する[`tidb_partition_prune_mode`](/system-variables.md#tidb_partition_prune_mode-new-in-v51)システム変数を導入しました。v8.5.0 以降では、この変数を`static`または`static-only`に設定すると警告が返されます。将来のバージョンでは、このシステム変数は非推奨になります。
-   TiDB Lightningパラメータ[`conflict.max-record-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)は、将来のリリースで廃止される予定であり、その後削除されます。このパラメータは[`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)に置き換えられます。これは、競合するレコードの最大数が、単一のインポート タスクで許容できる競合するレコードの最大数と一致することを意味します。
-   v6.3.0 以降、パーティション テーブルはデフォルトで[動的剪定モード](/partitioned-table.md#dynamic-pruning-mode)使用します。静的プルーニング モードと比較して、動的プルーニング モードは IndexJoin やプラン キャッシュなどの機能をサポートし、パフォーマンスが向上します。したがって、静的プルーニング モードは非推奨になります。

## 改善点 {#improvements}

-   ティビ

    -   分散実行フレームワーク (DXF) [＃56017](https://github.com/pingcap/tidb/issues/56017) @ [ランス6716](https://github.com/lance6716)を無効にした場合の`ADD INDEX`アクセラレーション機能のジョブキャンセルの応答速度を改善しました
    -   小さなテーブルへのインデックス追加速度の向上[＃54230](https://github.com/pingcap/tidb/issues/54230) @ [タンジェンタ](https://github.com/tangenta)
    -   インデックス[＃57156](https://github.com/pingcap/tidb/issues/57156) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)を追加する際の取り込みフェーズの最大速度を制限する新しいシステム変数`tidb_ddl_reorg_max_write_speed`を追加します。
    -   場合によっては`information_schema.tables`クエリのパフォーマンスを向上[＃57295](https://github.com/pingcap/tidb/issues/57295) @ [タンジェンタ](https://github.com/tangenta)
    -   より多くの DDL ジョブパラメータを動的に調整するサポート[＃57526](https://github.com/pingcap/tidb/issues/57526) @ [ふーふー](https://github.com/fzzf678)
    -   パーティション式[＃56230](https://github.com/pingcap/tidb/issues/56230) @ [定義2014](https://github.com/Defined2014)のすべての列を含むグローバル インデックスをサポートします。
    -   範囲クエリシナリオ[＃56673](https://github.com/pingcap/tidb/issues/56673) @ [定義2014](https://github.com/Defined2014)でリストパーティションテーブルのパーティションプルーニングをサポート
    -   FixControl#46177 をデフォルトで有効にして、場合によってはインデックス範囲スキャンではなくテーブル全体のスキャンが誤って選択される問題を修正します[＃46177](https://github.com/pingcap/tidb/issues/46177) @ [テリー・パーセル](https://github.com/terry1purcell)
    -   内部推定ロジックを改善し、複数列および複数値インデックスの統計をより有効に活用して、複数値インデックス[＃56915](https://github.com/pingcap/tidb/issues/56915) @ [時間と運命](https://github.com/time-and-fate)を含む特定のクエリの推定精度を向上させます。
    -   特定のシナリオにおけるフルテーブルスキャンのコスト見積もりを改善し、フルテーブルスキャンを誤って選択する可能性を減らします[＃57085](https://github.com/pingcap/tidb/issues/57085) @ [テリー・パーセル](https://github.com/terry1purcell)
    -   統計の同期ロードに必要なデータ量を最適化して、ロードパフォーマンスを向上させる[＃56812](https://github.com/pingcap/tidb/issues/56812) @ [ウィノロス](https://github.com/winoros)
    -   `OUTER JOIN`が一意のインデックスと`ORDER BY ... LIMIT`句を含む特定のケースで実行プランを最適化し、実行効率[＃56321](https://github.com/pingcap/tidb/issues/56321) @ [ウィノロス](https://github.com/winoros)を向上させます。

-   ティクヴ

    -   別のスレッドを使用してレプリカをクリーンアップし、 Raft の読み取りと書き込みの重要なパスの安定したレイテンシーを確保します[＃16001](https://github.com/tikv/tikv/issues/16001) @ [ビシェン](https://github.com/hbisheng)
    -   SIMD [＃17290](https://github.com/tikv/tikv/issues/17290) @ [エリック・ゼクアン](https://github.com/EricZequan)サポートすることでベクトル距離関数のパフォーマンスを向上

-   PD

    -   マイクロサービスモードと非マイクロサービスモード間の`tso`のサービスの動的切り替えをサポート[＃8477](https://github.com/tikv/pd/issues/8477) @ [rleungx](https://github.com/rleungx)
    -   `pd-ctl config`出力[＃8694](https://github.com/tikv/pd/issues/8694) @ [翻訳者](https://github.com/lhy1024)の特定のフィールドの大文字小文字の形式を最適化します
    -   [ストア制限 v2](/configure-store-limit.md#principles-of-store-limit-v2)一般公開（GA）される[＃8865](https://github.com/tikv/pd/issues/8865) @ [翻訳者](https://github.com/lhy1024)
    -   リージョン検査の同時実行の設定をサポート (実験的) [＃8866](https://github.com/tikv/pd/issues/8866) @ [翻訳者](https://github.com/lhy1024)

-   TiFlash

    -   クラスター化インデックス[＃9529](https://github.com/pingcap/tiflash/issues/9529) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)を持つテーブルで、バックグラウンドでの古いデータのガベージコレクションの速度が向上しました。
    -   データ更新シナリオ[＃9599](https://github.com/pingcap/tiflash/issues/9599) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)でのベクトル検索のクエリ パフォーマンスの向上
    -   ベクトルインデックス構築中のCPU使用率の監視メトリックを追加[＃9032](https://github.com/pingcap/tiflash/issues/9032) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)
    -   論理演算子[＃9146](https://github.com/pingcap/tiflash/issues/9146) @ [風の話し手](https://github.com/windtalker)の実行効率を向上させる

-   ツール

    -   バックアップと復元 (BR)

        -   バックアップ中の不要なログ出力を削減[＃55902](https://github.com/pingcap/tidb/issues/55902) @ [リーヴルス](https://github.com/Leavrth)
        -   暗号化キーのエラーメッセージを最適化`--crypter.key` [＃56388](https://github.com/pingcap/tidb/issues/56388) @ [トリスタン1900](https://github.com/Tristan1900)
        -   データベース作成時にBRの同時実行性を高めて、データ復元パフォーマンスを向上させる[＃56866](https://github.com/pingcap/tidb/issues/56866) @ [リーヴルス](https://github.com/Leavrth)
        -   バックアップパフォーマンスを向上させるために、フルバックアップ中のテーブルレベルのチェックサム計算をデフォルトで無効にする（ `--checksum=false` ） [＃56373](https://github.com/pingcap/tidb/issues/56373) @ [トリスタン1900](https://github.com/Tristan1900)
        -   各storageノードの接続タイムアウトを独立して追跡およびリセットするメカニズムを追加し、低速ノードの処理を強化してバックアップ操作のハングアップを防止します[＃57666](https://github.com/pingcap/tidb/issues/57666) @ [3ポインター](https://github.com/3pointer)

    -   TiDB データ移行 (DM)

        -   DM クラスターの起動中に DM ワーカーが DM マスターに接続するための再試行を[＃4287](https://github.com/pingcap/tiflow/issues/4287) @ [GMHDBJD](https://github.com/GMHDBJD)に追加します。

## バグ修正 {#bug-fixes}

-   ティビ

    -   PD から返されたリージョンメタデータにLeader情報が不足している場合に TiDB がリクエストを自動的に再試行せず、実行エラーが発生する可能性がある問題を修正しました[＃56757](https://github.com/pingcap/tidb/issues/56757) @ [翻訳](https://github.com/cfzjywxk)
    -   書き込み競合が発生したときに TTL タスクをキャンセルできない問題を修正[＃56422](https://github.com/pingcap/tidb/issues/56422) @ [ヤンケオ](https://github.com/YangKeao)
    -   TTLタスクをキャンセルした際に、対応するSQLが強制終了されない問題を修正[＃56511](https://github.com/pingcap/tidb/issues/56511) @ [lcwangchao](https://github.com/lcwangchao)
    -   v6.5 から v7.5 以降にアップグレードされたクラスターで、既存の TTL タスクが予期せず頻繁に実行される問題を修正[＃56539](https://github.com/pingcap/tidb/issues/56539) @ [lcwangchao](https://github.com/lcwangchao)
    -   `INSERT ... ON DUPLICATE KEY`ステートメントが`mysql_insert_id` [＃55965](https://github.com/pingcap/tidb/issues/55965) @ [天菜まお](https://github.com/tiancaiamao)と互換性がない問題を修正
    -   storageエンジン[＃56402](https://github.com/pingcap/tidb/issues/56402) @ [ヤンケオ](https://github.com/YangKeao)として TiKV が選択されていない場合に TTL が失敗する可能性がある問題を修正しました
    -   `IMPORT INTO`ステートメント[＃56476](https://github.com/pingcap/tidb/issues/56476) @ [D3ハンター](https://github.com/D3Hunter)を使用してデータをインポートした後、 `AUTO_INCREMENT`フィールドが正しく設定されない問題を修正しました。
    -   `ADD INDEX` [＃56930](https://github.com/pingcap/tidb/issues/56930) @ [ふーふー](https://github.com/fzzf678)を実行するときに TiDB がインデックスの長さ制限をチェックしない問題を修正しました
    -   `RECOVER TABLE BY JOB JOB_ID;`実行すると TiDB がpanicになる可能性がある問題を修正[＃55113](https://github.com/pingcap/tidb/issues/55113) @ [クレイジーcs520](https://github.com/crazycs520)
    -   古い読み取りが読み取り操作のタイムスタンプを厳密に検証しない問題を修正しました。その結果、TSO と実際の物理時間[＃56809](https://github.com/pingcap/tidb/issues/56809) @ [ミョンケミンタ](https://github.com/MyonKeminta)の間にオフセットが存在する場合に、トランザクションの一貫性にわずかながら影響が出る可能性があります。
    -   DDL 所有者ノードが[＃56506](https://github.com/pingcap/tidb/issues/56506) @ [タンジェンタ](https://github.com/tangenta)に切り替えられた後、TiDB が以前の進行状況から Reorg DDL タスクを再開できない問題を修正しました。
    -   Distributed eXecution Framework (DXF) の監視パネルの一部のメトリックが不正確であるという問題を修正[＃57172](https://github.com/pingcap/tidb/issues/57172) @ [ふーふー](https://github.com/fzzf678) [＃56942](https://github.com/pingcap/tidb/issues/56942) @ [ふーふー](https://github.com/fzzf678)
    -   `REORGANIZE PARTITION`特定のケースでエラー理由を返さない問題を修正[＃56634](https://github.com/pingcap/tidb/issues/56634) @ [ミョンス](https://github.com/mjonss)
    -   大文字と小文字の区別により、 `INFORMATION_SCHEMA.TABLES`クエリすると誤った結果が返される問題を修正[＃56987](https://github.com/pingcap/tidb/issues/56987) @ [ジョーチェン](https://github.com/joechenrh)
    -   共通テーブル式 (CTE) に複数のデータ コンシューマーがあり、1 つのコンシューマーがデータを読み取らずに終了した場合に発生する可能性のある不正なメモリアクセスの問題を修正しました[＃55881](https://github.com/pingcap/tidb/issues/55881) @ [風の話し手](https://github.com/windtalker)
    -   異常終了時に`INDEX_HASH_JOIN`アップする可能性がある問題を修正[＃54055](https://github.com/pingcap/tidb/issues/54055) @ [うわー](https://github.com/wshwsh12)
    -   `NULL`値[＃53546](https://github.com/pingcap/tidb/issues/53546) @ [つじえもん](https://github.com/tuziemon)処理するときに`TRUNCATE`ステートメントが誤った結果を返す問題を修正しました
    -   `CAST AS CHAR`関数が型推論エラーにより誤った結果を返す問題を修正[＃56640](https://github.com/pingcap/tidb/issues/56640) @ [ジムララ](https://github.com/zimulala)
    -   型推論エラーにより一部の関数の出力で文字列が切り捨てられる問題を修正[＃56587](https://github.com/pingcap/tidb/issues/56587) @ [ジョーチェン](https://github.com/joechenrh)
    -   `ADDTIME()`および`SUBTIME()`関数の最初の引数が日付型[＃57569](https://github.com/pingcap/tidb/issues/57569) @ [翻訳者](https://github.com/xzhangxian1008)の場合に誤った結果を返す問題を修正しました
    -   非厳密モードで無効な`NULL`値が挿入される問題を修正 ( `sql_mode = ''` ) [＃56381](https://github.com/pingcap/tidb/issues/56381) @ [ジョーチェン](https://github.com/joechenrh)
    -   `UPDATE`文が`ENUM`型[＃56832](https://github.com/pingcap/tidb/issues/56832) @ [xhebox](https://github.com/xhebox)の値を誤って更新する問題を修正しました。
    -   `tidb_low_resolution_tso`変数を有効にすると、 `SELECT FOR UPDATE`ステートメント[＃55468](https://github.com/pingcap/tidb/issues/55468) @ [天菜まお](https://github.com/tiancaiamao)の実行中にリソース リークが発生する問題を修正しました。
    -   `JSON_TYPE()`関数がパラメータ タイプを検証せず、JSON 以外のデータ型が渡されたときにエラーが返されない問題を修正しました[＃54029](https://github.com/pingcap/tidb/issues/54029) @ [ヤンケオ](https://github.com/YangKeao)
    -   `PREPARE`ステートメントで JSON関数を使用すると実行エラーが発生する可能性がある問題を修正[＃54044](https://github.com/pingcap/tidb/issues/54044) @ [ヤンケオ](https://github.com/YangKeao)
    -   `BIT`型から`CHAR`型にデータを変換すると TiKV パニック[＃56494](https://github.com/pingcap/tidb/issues/56494) @ [lcwangchao](https://github.com/lcwangchao)発生する可能性がある問題を修正しました
    -   `CREATE VIEW`ステートメントで変数またはパラメータを使用してもエラーが報告されない問題を修正[＃53176](https://github.com/pingcap/tidb/issues/53176) @ [ミョンス](https://github.com/mjonss)
    -   `JSON_VALID()`関数が誤った結果を返す問題を修正[＃56293](https://github.com/pingcap/tidb/issues/56293) @ [ヤンケオ](https://github.com/YangKeao)
    -   `tidb_ttl_job_enable`変数が無効になった後、TTL タスクがキャンセルされない問題を修正[＃57404](https://github.com/pingcap/tidb/issues/57404) @ [ヤンケオ](https://github.com/YangKeao)
    -   `RANGE COLUMNS`パーティション関数と`utf8mb4_0900_ai_ci`照合順序を同時に使用すると、クエリ結果[＃57261](https://github.com/pingcap/tidb/issues/57261) @ [定義2014](https://github.com/Defined2014)正しくなくなる可能性がある問題を修正しました。
    -   改行文字で始まるプリペアドステートメントを実行すると、配列が範囲外になるランタイム エラーを修正しました[＃54283](https://github.com/pingcap/tidb/issues/54283) @ [定義2014](https://github.com/Defined2014)
    -   `UTC_TIMESTAMP()`関数の精度の問題を修正します。たとえば、精度を高く設定しすぎます[＃56451](https://github.com/pingcap/tidb/issues/56451) @ [チャゲロ](https://github.com/chagelo)
    -   `UPDATE` `DELETE IGNORE`ステートメントで外部キーエラーが省略されない問題を修正[＃56678](https://github.com/pingcap/tidb/issues/56678) `INSERT` [ヤンケオ](https://github.com/YangKeao)
    -   `information_schema.cluster_slow_query`テーブルをクエリするときに、時間フィルターが追加されていない場合、最新のスロー ログ ファイルのみがクエリされる問題を修正しました[＃56100](https://github.com/pingcap/tidb/issues/56100) @ [クレイジーcs520](https://github.com/crazycs520)
    -   TTL テーブル[＃56934](https://github.com/pingcap/tidb/issues/56934) @ [lcwangchao](https://github.com/lcwangchao)のメモリリークの問題を修正
    -   ステータス`write_only`のテーブルに対して外部キー制約が有効にならず、ステータス`non-public`のテーブルを[＃55813](https://github.com/pingcap/tidb/issues/55813) @ [ヤンケオ](https://github.com/YangKeao)で使用できない問題を修正しました。
    -   `NATURAL JOIN`または`USING`節の後にサブクエリを使用するとエラー[＃53766](https://github.com/pingcap/tidb/issues/53766) @ [ダッシュ12653](https://github.com/dash12653)が発生する可能性がある問題を修正しました
    -   CTE に`ORDER BY` 、 `LIMIT` 、または`SELECT DISTINCT`節が含まれており、別の CTE の再帰部分によって参照されている場合、誤ってインライン化され、実行エラー[＃56603](https://github.com/pingcap/tidb/issues/56603) @ [エルサ0520](https://github.com/elsa0520)が発生する可能性がある問題を修正しました。
    -   `VIEW`で定義されたCTEが誤ってインライン化される問題を修正[＃56582](https://github.com/pingcap/tidb/issues/56582) @ [エルサ0520](https://github.com/elsa0520)
    -   外部キー[＃56456](https://github.com/pingcap/tidb/issues/56456) @ [ホーキングレイ](https://github.com/hawkingrei)を含むテーブル構造をインポートするときに Plan Replayer がエラーを報告する可能性がある問題を修正しました。
    -   配置ルール[＃54961](https://github.com/pingcap/tidb/issues/54961) @ [ホーキングレイ](https://github.com/hawkingrei)を含むテーブル構造をインポートするときに Plan Replayer がエラーを報告する可能性がある問題を修正しました。
    -   `ANALYZE`使用してテーブルの統計情報を収集する場合、テーブルに仮想的に生成された列の式インデックスが含まれていると、実行時にエラー[＃57079](https://github.com/pingcap/tidb/issues/57079) @ [ホーキングレイ](https://github.com/hawkingrei)が報告される問題を修正しました。
    -   `DROP DATABASE`ステートメントが統計[＃57227](https://github.com/pingcap/tidb/issues/57227) @ [ラスティン170506](https://github.com/Rustin170506)の対応する更新を正しくトリガーしない問題を修正しました。
    -   CTE でデータベース名を解析するときに間違ったデータベース名[＃54582](https://github.com/pingcap/tidb/issues/54582) @ [ホーキングレイ](https://github.com/hawkingrei)が返される問題を修正しました
    -   `DUMP STATS`統計を JSON [＃56083](https://github.com/pingcap/tidb/issues/56083) @ [ホーキングレイ](https://github.com/hawkingrei)に変換するときにヒストグラムの上限と下限が壊れる問題を修正
    -   `EXISTS`サブクエリの結果が、さらに代数演算に関係する場合、MySQL [＃56641](https://github.com/pingcap/tidb/issues/56641) @ [風の話し手](https://github.com/windtalker)の結果と異なる可能性がある問題を修正しました。
    -   エイリアス[＃56726](https://github.com/pingcap/tidb/issues/56726) @ [ホーキングレイ](https://github.com/hawkingrei)を持つマルチテーブル`DELETE`ステートメントに対して実行プラン バインディングを作成できない問題を修正しました。
    -   複雑な述語を簡略化するときにオプティマイザが文字セットと照合順序を考慮せず、実行エラーが発生する可能性がある問題を修正しました[＃56479](https://github.com/pingcap/tidb/issues/56479) @ [ダッシュ12653](https://github.com/dash12653)
    -   Grafana の**Stats Healthy Distribution**パネルのデータが正しくない可能性がある問題を修正[＃57176](https://github.com/pingcap/tidb/issues/57176) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   クラスター化インデックス[＃57627](https://github.com/pingcap/tidb/issues/57627) @ [ウィノロス](https://github.com/winoros)を持つテーブルをクエリするときにベクトル検索が誤った結果を返す可能性がある問題を修正しました

-   ティクヴ

    -   読み取りスレッドがRaft Engine[＃17383](https://github.com/tikv/tikv/issues/17383) @ [リクササシネーター](https://github.com/LykxSassinator)のMemTable内の古いインデックスにアクセスしたときに発生するpanic問題を修正しました。
    -   多数のトランザクションが同じキーのロック解除待ち行列に入っていて、キーが頻繁に更新される場合、デッドロック検出に過度の負荷がかかり、TiKV OOM 問題[＃17394](https://github.com/tikv/tikv/issues/17394) @ [ミョンケミンタ](https://github.com/MyonKeminta)が発生する可能性がある問題を修正しました。
    -   リソース制御のバックグラウンドタスクのCPU使用率が2回カウントされる問題を修正[＃17603](https://github.com/tikv/tikv/issues/17603) @ [栄光](https://github.com/glorv)
    -   CDC内部タスク[＃17696](https://github.com/tikv/tikv/issues/17696) @ [3エースショーハンド](https://github.com/3AceShowHand)の蓄積によりTiKV OOMが発生する可能性がある問題を修正
    -   `raft-entry-max-size`高く設定しすぎると、大量のバッチ書き込みによってパフォーマンスジッターが発生する問題を修正[＃17701](https://github.com/tikv/tikv/issues/17701) @ [スペードA-タン](https://github.com/SpadeA-Tang)
    -   リージョンを[＃17602](https://github.com/tikv/tikv/issues/17602)対[リクササシネーター](https://github.com/LykxSassinator)に分割した後、リーダーをすぐに選出できない問題を修正しました。
    -   `RADIANS()`または`DEGREES()`関数を含むクエリを実行するときに TiKV がpanicになる可能性がある問題を修正[＃17852](https://github.com/tikv/tikv/issues/17852) @ [ゲンリキ](https://github.com/gengliqi)
    -   すべての休止状態の領域が[＃17101](https://github.com/tikv/tikv/issues/17101) @ [いいえ](https://github.com/hhwyt)で起動したときに書き込みジッターが発生する可能性がある問題を修正しました

-   PD

    -   ホットスポット キャッシュ[＃8698](https://github.com/tikv/pd/issues/8698) @ [翻訳者](https://github.com/lhy1024)のメモリリーク問題を修正
    -   リソース グループ セレクターがどのパネルでも有効にならない問題を修正[＃56572](https://github.com/pingcap/tidb/issues/56572) @ [栄光](https://github.com/glorv)
    -   削除されたリソース グループが監視パネル[＃8716](https://github.com/tikv/pd/issues/8716) @ [アンドレ・ムーシュ](https://github.com/AndreMouche)に引き続き表示される問題を修正しました
    -   リージョン同期の読み込みプロセス中の不明瞭なログの説明を修正[＃8717](https://github.com/tikv/pd/issues/8717) @ [翻訳者](https://github.com/lhy1024)
    -   ラベル統計[＃8700](https://github.com/tikv/pd/issues/8700) @ [翻訳者](https://github.com/lhy1024)のメモリリーク問題を修正
    -   `tidb_enable_tso_follower_proxy`から`0`または`OFF`を設定しても TSOFollowerプロキシ機能[＃8709](https://github.com/tikv/pd/issues/8709) @ [じゃがいも](https://github.com/JmPotato)を無効にできない問題を修正しました。

-   TiFlash

    -   `SUBSTRING()`関数が特定の整数型の`pos`番目と`len`引数をサポートせず、クエリ エラー[＃9473](https://github.com/pingcap/tiflash/issues/9473) @ [ゲンリキ](https://github.com/gengliqi)が発生する問題を修正しました。
    -   分散storageおよびコンピューティングアーキテクチャ[＃9637](https://github.com/pingcap/tiflash/issues/9637) @ [コラフィッシュ](https://github.com/kolafish)でTiFlash書き込みノードをスケールアウトした後にベクトル検索のパフォーマンスが低下する可能性がある問題を修正しました。
    -   2 番目のパラメータが負の[＃9604](https://github.com/pingcap/tiflash/issues/9604) @ [グオシャオゲ](https://github.com/guo-shaoge)の場合に`SUBSTRING()`関数が誤った結果を返す問題を修正しました
    -   最初のパラメータが定数[＃9522](https://github.com/pingcap/tiflash/issues/9522) @ [グオシャオゲ](https://github.com/guo-shaoge)の場合に`REPLACE()`関数がエラーを返す問題を修正しました
    -   `LPAD()`と`RPAD()`関数が場合によっては誤った結果を返す問題を修正[＃9465](https://github.com/pingcap/tiflash/issues/9465) @ [グオシャオゲ](https://github.com/guo-shaoge)
    -   ベクトルインデックスを作成した後、ベクトルインデックスを構築する内部タスクが予期せず中断されると、 TiFlash が破損したデータを書き込み、再起動できなくなる可能性がある問題を修正しました[＃9714](https://github.com/pingcap/tiflash/issues/9714) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)

-   ツール

    -   バックアップと復元 (BR)

        -   未完了の範囲ギャップが多すぎる場合のバックアップ中の OOM 問題を修正し、事前割り当てメモリ[＃53529](https://github.com/pingcap/tidb/issues/53529) @ [リーヴルス](https://github.com/Leavrth)の量を減らします。
        -   グローバルインデックスをバックアップできない問題を修正[＃57469](https://github.com/pingcap/tidb/issues/57469) @ [定義2014](https://github.com/Defined2014)
        -   ログに暗号化された情報が出力される問題を修正[＃57585](https://github.com/pingcap/tidb/issues/57585) @ [ケニー](https://github.com/kennytm)
        -   アドバンサーがロック競合を処理できない問題を修正[＃57134](https://github.com/pingcap/tidb/issues/57134) @ [3ポインター](https://github.com/3pointer)
        -   `k8s.io/api`ライブラリ バージョン[＃57790](https://github.com/pingcap/tidb/issues/57790) @ [ボーンチェンジャー](https://github.com/BornChanger)にアップグレードして潜在的なセキュリティ脆弱性を修正します
        -   クラスター内に多数のテーブルがあるが、実際のデータ サイズが小さい場合に PITR タスクが`Information schema is out of date`エラーを返す可能性がある問題を修正しました[＃57743](https://github.com/pingcap/tidb/issues/57743) @ [トリスタン1900](https://github.com/Tristan1900)
        -   アドバンサー所有者が[＃58031](https://github.com/pingcap/tidb/issues/58031) @ [3ポインター](https://github.com/3pointer)に切り替わったときに、ログ バックアップが予期せず一時停止状態になる可能性がある問題を修正しました。
        -   `tiup br restore`コマンドがデータベースまたはテーブルの復元中にターゲット クラスター テーブルが既に存在するかどうかのチェックを省略し、既存のテーブル[＃58168](https://github.com/pingcap/tidb/issues/58168) @ [リドリス](https://github.com/RidRisR)を上書きする可能性がある問題を修正しました。

    -   ティCDC

        -   Debezium プロトコル[＃1799](https://github.com/pingcap/tiflow/issues/1799) @ [989898 円](https://github.com/wk989898)を使用するときに Kafka メッセージにキー フィールドが欠落する問題を修正しました
        -   やり直しモジュールがエラー[＃11744](https://github.com/pingcap/tiflow/issues/11744) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)を適切に報告できない問題を修正
        -   TiDB DDL 所有者の変更中に DDL タスクのスキーマ バージョンが非増分になったときに、TiCDC が誤って DDL タスクを破棄する問題を修正[＃11714](https://github.com/pingcap/tiflow/issues/11714) @ [ウィリアム](https://github.com/wlwilliamx)

    -   TiDB Lightning

        -   TiDB Lightning がTiKV [＃56114](https://github.com/pingcap/tidb/issues/56114) @ [フィシュウ](https://github.com/fishiu)から送信されたサイズ超過のメッセージを受信できない問題を修正しました
        -   物理インポートモード[＃56814](https://github.com/pingcap/tidb/issues/56814) @ [D3ハンター](https://github.com/D3Hunter)を使用してデータをインポートした後に`AUTO_INCREMENT`値が高すぎる値に設定される問題を修正しました

## 寄稿者 {#contributors}

TiDB コミュニティの以下の貢献者に感謝いたします。

-   [ダッシュ12653](https://github.com/dash12653) (初めての投稿者)
-   [チャゲロ](https://github.com/chagelo) (初めての投稿者)
-   [リンダサマー](https://github.com/LindaSummer)
-   [歌zhibin97](https://github.com/songzhibin97)
-   [ヘキシリー](https://github.com/Hexilee)
