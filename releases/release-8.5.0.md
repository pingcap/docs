---
title: TiDB 8.5.0 Release Notes
summary: TiDB 8.5.0 の新機能、互換性の変更点、改善点、およびバグ修正についてご確認ください。
---

# TiDB 8.5.0 リリースノート {#tidb-8-5-0-release-notes}

<EmailSubscriptionWrapper />

発売日：2024年12月19日

TiDB バージョン: 8.5.0

クイックアクセス： [クイックスタート](https://docs.pingcap.com/tidb/v8.5/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v8.5/production-deployment-using-tiup)

TiDB 8.5.0は長期サポートリリース（LTS）です。

以前の LTS 8.1.0 と比較して、8.5.0 には、 [8.2.0-DMR](/releases/release-8.2.0.md)でリリースされた新機能、改善点、およびバグ修正が含まれています。8.1.x から[8.4.0-DMR](/releases/release-8.4.0.md)にアップグレードする場合、 [TiDB リリースノート PDF](https://docs-download.pingcap.com/pdf/tidb-v8.2-to-v8.5-en-release-notes.pdf)をダウンロードして、2 つの LTS バージョン間のすべてのリリース ノートを表示できます。次の表は[8.3.0-DMR](/releases/release-8.3.0.md) 8.1.0 から 8.5.0 までのハイライトの一部を示しています。

<table><thead><tr><th>カテゴリ</th><th>機能／改善点</th><th>説明</th></tr></thead><tbody><tr><td rowspan="7">拡張性とパフォーマンス</td><td>複数の次元でデータ処理のレイテンシーを削減する</td><td>TiDBは、パフォーマンス向上のためにデータ処理を継続的に改良し、金融分野における低遅延SQL処理の要件を効果的に満たしています。主なアップデート内容は以下のとおりです。<ul><li> <a href="https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_executor_concurrency-new-in-v50">並列ソート</a>をサポート（バージョン8.2.0で導入）</li><li><a href="https://docs.pingcap.com/tidb/v8.5/tidb-configuration-file#batch-policy-new-in-v830">キーバリュー（KV）リクエストのバッチ処理戦略</a>を最適化（v8.3.0で導入）</li><li> <a href="https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_tso_client_rpc_mode-new-in-v840">TSOリクエストの並列モード</a>をサポート（v8.4.0で導入）</li><li> <a href="https://docs.pingcap.com/tidb/v8.5/sql-statement-delete">DELETE</a>操作のリソースオーバーヘッドを削減します（v8.4.0で導入）。</li><li><a href="https://docs.pingcap.com/tidb/v8.5/cached-tables">キャッシュされたテーブル</a>のクエリパフォーマンスを向上させました（v8.4.0で導入）。</li><li><a href="https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_hash_join_version-new-in-v840">ハッシュ結合の最適化バージョン</a>を導入します（実験的、v8.4.0で導入）。</li></ul></td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v8.5/tikv-in-memory-engine">TiKV MVCC インメモリエンジン (IME)</a> (バージョン8.5.0で導入)</td><td> TiKV MVCCのインメモリエンジンは、最新のMVCCバージョンのデータをメモリにキャッシュすることで、古いバージョンをスキップして最新のデータを迅速に取得できるようにします。この機能は、データレコードが頻繁に更新される場合や、履歴バージョンが長期間保持される場合に、データスキャン性能を大幅に向上させることができます。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v8.5/tune-region-performance#use-the-active-pd-follower-feature-to-enhance-the-scalability-of-pds-region-information-query-service">アクティブなPDフォロワーを使用して、PDのリージョン情報クエリサービスを強化します</a>（v8.5.0で一般提供開始）。</td><td> TiDB v7.6.0 では、実験的機能「アクティブ PDFollower」が導入されました。これにより、PD フォロワーがリージョン情報クエリサービスを提供できるようになります。この機能は、多数の TiDB ノードとリージョンを持つクラスターにおいて、PD クラスターが<code>GetRegion</code>および<code>ScanRegions</code>リクエストを処理する能力を向上させ、PD リーダーの CPU 負荷を軽減します。この機能は、v8.5.0 で一般提供 (GA) されます。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_enable_instance_plan_cache-new-in-v840">インスタンスレベルの実行プランキャッシュ</a>（実験的、v8.4.0で導入）</td><td>インスタンスレベルのプランキャッシュを使用すると、同じ TiDB インスタンス内のすべてのセッションでプランキャッシュを共有できます。セッションレベルのプランキャッシュと比較して、この機能はメモリに多くの実行プランをキャッシュすることで SQL コンパイル時間を短縮し、SQL 全体の実行時間を短縮します。これにより、OLTP のパフォーマンスとスループットが向上するとともに、メモリ使用量をより適切に制御し、データベースの安定性を高めることができます。</td></tr><tr><td><a href="https://docs.pingcap.com/tidb/v8.5/global-indexes">パーティションテーブルのグローバルインデックス</a>（バージョン8.4.0で一般提供開始）</td><td>グローバルインデックスは、パーティション化されていない列の取得効率を効果的に向上させ、一意キーにパーティションキーを含める必要があるという制約を取り除きます。この機能により、TiDBパーティションテーブルの利用シナリオが拡張され、パーティションテーブルのパフォーマンスが向上し、特定のクエリシナリオにおけるリソース消費量が削減されます。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_opt_projection_push_down-new-in-v610"><code>Projection</code>演算子をstorageエンジンにデフォルトでプッシュダウンする機能</a>（v8.3.0で導入）</td><td> <code>Projection</code>演算子をstorageエンジンにプッシュダウンすることで、storageノード全体に負荷を分散させ、ノード間のデータ転送量を削減できます。この最適化により、特定のSQLクエリの実行時間が短縮され、データベース全体のパフォーマンスが向上します。</td></tr><tr><td><a href="https://docs.pingcap.com/tidb/v8.5/statistics#collect-statistics-on-some-columns">統計情報を収集する際に不要な列を無視する機能</a>（バージョン8.3.0で導入）</td><td>オプティマイザが必要な情報を確実に取得できるという前提のもと、TiDBは統計情報の収集を高速化し、統計情報の適時性を向上させることで、最適な実行プランの選択を保証し、クラスタのパフォーマンスを向上させます。同時に、TiDBはシステムオーバーヘッドを削減し、リソース利用率も向上させます。</td></tr><tr><td rowspan="5">信頼性と可用性</td><td>大規模クラスターの安定性を向上させる</td><td>TiDBを使用してマルチテナントアプリケーションやSaaSアプリケーションを運用する企業は、多くの場合、大量のテーブルを保存する必要があります。バージョン8.5.0では、TiDBは大規模クラスタの安定性を大幅に向上させました。<ul><li><a href="https://docs.pingcap.com/tidb/v8.5/schema-cache">スキーマキャッシュの制御</a>と、 <a href="https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_stats_cache_mem_quota-new-in-v610">TiDB統計キャッシュのメモリ割り当て量の設定が</a>一般提供（GA）となり、過剰なメモリ消費によって引き起こされる安定性の問題が軽減されます。</li><li> PDは、多数のリージョンによって生じる負荷に対処するために<a href="https://docs.pingcap.com/tidb/v8.5/tune-region-performance#use-the-active-pd-follower-feature-to-enhance-the-scalability-of-pds-region-information-query-service">アクティブFollower</a>を導入し、 <a href="https://docs.pingcap.com/tidb/v8.5/pd-microservices">PDが処理するサービスを段階的に分離して</a>独立したデプロイメントを実現します。</li><li> PDはリージョンハートビート処理のパフォーマンスを向上させ、単一のクラスタで数千万ものリージョンをサポートします。</li><li> <a href="https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_auto_analyze_concurrency-new-in-v840">並行処理を増やし</a>、<a href="https://docs.pingcap.com/tidb/v8.5/statistics#collect-statistics-on-some-columns">収集するオブジェクトの数を減らす</a>ことで、統計情報の収集とロードの効率を向上させ、大規模クラスタにおける実行計画の安定性を確保できます。</li></ul></td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v8.5/tidb-resource-control-runaway-queries#query_limit-parameters">暴走クエリに対するトリガーの追加サポート、およびリソースグループの切り替えサポート</a>（v8.4.0で導入）</td><td>暴走クエリは、予期しないSQLパフォーマンスの問題がシステムに与える影響を軽減する効果的な手段です。TiDB v8.4.0では、識別条件としてコプロセッサーによって処理されたキーの数（ <code>PROCESSED_KEYS</code> ）とリクエストユニット（ <code>RU</code> ）が導入され、識別されたクエリを指定されたリソースグループに配置することで、暴走クエリのより正確な識別と制御が可能になりました。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v8.5/tidb-resource-control-background-tasks#background-parameters">リソース制御のバックグラウンドタスクにおけるリソース使用量の上限設定をサポート</a>（実験的、v8.4.0で導入）</td><td>リソース制御のバックグラウンドタスクに最大パーセンテージ制限を設定することで、さまざまなアプリケーションシステムのニーズに基づいてリソース消費を制御できます。これにより、バックグラウンドタスクの消費量を低く抑え、オンラインサービスの品質を確保できます。</td></tr><tr><td> TiProxyのユースケースを強化および拡張する</td><td>TiDBの高可用性を実現する上で重要なコンポーネントである<a href="https://docs.pingcap.com/tidb/v8.5/tiproxy-overview">TiProxyは</a>、SQLトラフィックのアクセスと転送にとどまらず、クラスタ変更の評価をサポートする機能も備えています。主な機能は以下のとおりです。<ul><li> <a href="https://docs.pingcap.com/tidb/v8.5/tiproxy-traffic-replay">TiProxyはトラフィックのキャプチャと再生をサポートしています</a>（実験的、v8.4.0で導入）。</li><li> <a href="https://docs.pingcap.com/tidb/v8.5/tiproxy-overview">TiProxyは、組み込みの仮想IP管理機能をサポートしています</a>（バージョン8.3.0で導入）。</li><li> <a href="https://docs.pingcap.com/tidb/v8.5/tiproxy-load-balance">TiProxyは複数のロードバランシングポリシーをサポートしています</a>（バージョン8.2.0で導入）。</li></ul></td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_enable_parallel_hashagg_spill-new-in-v800">TiDBの並列HashAggアルゴリズムはディスクスピルをサポートしています</a>（v8.2.0でGA対応）。</td><td> HashAgg は、同じフィールド値を持つ行を効率的に集計するために TiDB で広く使用されている集計演算子です。TiDB v8.0.0 では、処理速度をさらに向上させる実験的機能として parallel HashAgg が導入されました。メモリリソースが不足している場合、parallel HashAgg は一時的にソートされたデータをディスクに書き出すことで、過剰なメモリ使用による潜在的な OOM リスクを回避します。これにより、ノードの安定性を維持しながらクエリ パフォーマンスが向上します。v8.2.0 では、この機能が一般提供 (GA) となり、デフォルトで有効になっているため、 <code>tidb_executor_concurrency</code>を使用して parallel HashAgg の同時実行性を安全に構成できます。</td></tr><tr><td rowspan="2"> SQL</td><td><a href="https://docs.pingcap.com/tidb/v8.5/foreign-key">外部キー</a>（バージョン8.5.0でGA対応）</td><td>外部キーは、データベースにおける制約であり、テーブル間の関係を確立し、データの一貫性と整合性を確保します。外部キーは、子テーブルで参照されるデータが親テーブルに存在することを保証し、無効なデータの挿入を防ぎます。また、外部キーはカスケード操作（削除や更新時の自動同期など）をサポートし、ビジネスロジックの実装を簡素化し、データ関係を手動で維持する複雑さを軽減します。</td></tr><tr><td><a href="https://docs.pingcap.com/ai/vector-search-overview">ベクトル検索</a>（実験的、v8.4.0で導入）</td><td>ベクトル検索は、データの意味論に基づいた検索手法であり、より関連性の高い検索結果を提供します。AIや大規模言語モデル（LLM）の中核関数の一つとして、ベクトル検索は、検索拡張生成（RAG）、意味検索、推薦システムなど、さまざまなシナリオで活用できます。</td></tr><tr><td rowspan="3">データベースの運用と可観測性</td><td><a href="https://docs.pingcap.com/tidb/v8.5/information-schema-processlist">TiKVおよびTiDBのCPU時間をメモリテーブルに表示する</a>（バージョン8.4.0で導入）</td><td> CPU時間はシステムテーブルに統合され、セッションやSQLなどの他のメトリックと並べて表示されるようになりました。これにより、CPU使用率の高い操作を複数の視点から把握し、診断効率を向上させることができます。これは、インスタンスにおけるCPUスパイクやクラスタにおける読み書きホットスポットなどのシナリオを診断する際に特に役立ちます。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v8.5/top-sql#use-top-sql">TiKVのCPU時間をテーブル別またはデータベース別に集計して表示する機能をサポート</a>（v8.4.0で導入）</td><td>ホットスポットの問題が個々のSQL文によって引き起こされていない場合、 Top SQLでテーブルまたはデータベースレベルごとに集計されたCPU時間を使用することで、ホットスポットの原因となっているテーブルやアプリケーションを迅速に特定でき、ホットスポットやCPU消費の問題の診断効率を大幅に向上させることができます。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v8.5/backup-and-restore-overview">Backup &amp; Restore (BR)</a>は、 <a href="https://aws.amazon.com/sdk-for-rust/">AWS SDK for Rust</a>を使用して外部storageにアクセスします (v8.5.0 で導入)。</td><td> BRは、TiKVからAmazon S3などの外部storageにアクセスするために、元のRusotoライブラリを<a href="https://aws.amazon.com/sdk-for-rust/">AWS SDK for Rust</a>に置き換えます。この変更により、 <a href="https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html">IMDSv2</a>や<a href="https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html">EKS Pod Identity</a>などのAWS機能との互換性が向上します。</td></tr><tr><td rowspan="1">Security</td><td><a href="https://docs.pingcap.com/tidb/v8.5/br-snapshot-manual#encrypt-the-backup-data">スナップショットバックアップデータ</a>および<a href="https://docs.pingcap.com/tidb/v8.5/br-pitr-manual#encrypt-log-backup-data">ログバックアップデータ</a>のクライアント側暗号化（v8.5.0で一般提供開始）</td><td>バックアップデータをバックアップstorageにアップロードする前に、バックアップデータを暗号化することで、storage中および転送中のセキュリティを確保できます。</td></tr></tbody></table>

## 機能の詳細 {#feature-details}

### 拡張性 {#scalability}

-   スキーマキャッシュのメモリ制限設定が一般提供開始（GA）となりました。テーブル数が数十万、あるいは数百万に達すると、この機能はスキーマメタデータのメモリ使用量を大幅に削減します[#50959](https://github.com/pingcap/tidb/issues/50959) @[tiancaiamao](https://github.com/tiancaiamao) @[wjhuang2016](https://github.com/wjhuang2016) @[gmhdbjd](https://github.com/gmhdbjd) @[tangenta](https://github.com/tangenta)

    SaaS環境によっては、テーブル数が数十万、あるいは数百万に達する場合、スキーマメタデータが相当量のメモリを消費することがあります。この機能を有効にすると、TiDBはLRU（Least Recently Used：最小使用頻度）アルゴリズムを使用して、対応するスキーマメタデータをキャッシュおよび削除することで、メモリ使用量を効果的に削減します。

    バージョン8.4.0以降、この機能はデフォルトで有効になっており、デフォルト値は`536870912` （つまり512MiB）です。必要に応じて変数[`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-new-in-v800)を使用して調整できます。

    詳細については、 [ドキュメント](/schema-cache.md)参照してください。

-   PDのリージョン情報クエリサービス（GA）のスケーラビリティを向上させるため、アクティブPDFollower機能を提供する[#7431](https://github.com/tikv/pd/issues/7431) @[okJiang](https://github.com/okJiang)

    リージョン数の多いTiDBクラスタでは、ハートビート処理やタスクスケジューリングに伴うオーバーヘッドが増加するため、PDリーダーのCPU負荷が高くなる可能性があります。クラスタにTiDBインスタンスが多数存在し、リージョン情報へのリクエストが同時に多数発生すると、PDリーダーのCPU負荷はさらに高まり、PDサービスが利用できなくなる恐れがあります。

    高可用性を確保するため、TiDB v7.6.0 では、PD のリージョン情報クエリサービスの拡張性を向上させる実験的機能として Active PD Followerが導入されました。v8.5.0 では、この機能が一般提供 (GA) されます。Active PD Follower機能は、システム変数[`pd_enable_follower_handle_region`](/system-variables.md#pd_enable_follower_handle_region-new-in-v760)から`ON`に設定することで有効にできます。この機能を有効にすると、TiDB はリージョン情報要求をすべての PD サーバーに均等に分散し、PD フォロワーもリージョン要求を処理できるようになるため、PD リーダーの CPU 負荷が軽減されます。

    詳細については、 [ドキュメント](/tune-region-performance.md#use-the-active-pd-follower-feature-to-enhance-the-scalability-of-pds-region-information-query-service)参照してください。

### パフォーマンス {#performance}

-   TiDBの高速テーブル作成機能が一般提供開始（GA）となり、データ移行とクラスタ初期化時間を大幅に短縮[#50052](https://github.com/pingcap/tidb/issues/50052) @[D3Hunter](https://github.com/D3Hunter) @[gmhdbjd](https://github.com/gmhdbjd)

    TiDB v7.6.0 では、システム変数[`tidb_ddl_version`](https://docs.pingcap.com/tidb/v7.6/system-variables#tidb_ddl_version-new-in-v760)によって制御される高速テーブル作成が実験的機能として導入されました。v8.0.0 以降、このシステム変数は[`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-new-in-v800)に名前が変更されました。

    バージョン8.5.0では、TiDBの高速テーブル作成機能が一般提供（GA）となり、デフォルトで有効になっています。データ移行やクラスタ初期化の際に、この機能は数百万ものテーブルを迅速に作成できるため、操作時間を大幅に短縮できます。

    詳細については、 [ドキュメント](/accelerated-table-creation.md)参照してください。

-   TiKVはMVCCインメモリエンジン（IME）をサポートしており、広範なMVCC履歴バージョン[#16141](https://github.com/tikv/tikv/issues/16141)のスキャン[グロルヴ](https://github.com/glorv)含むクエリ[オーバーヴィーナス](https://github.com/overvenus)高速化します[スペードアタン](https://github.com/SpadeA-Tang)

    レコードが頻繁に更新される場合、または TiDB が履歴バージョンを長期間 (例えば 24 時間) 保持する必要がある場合、MVCC バージョンの蓄積によりスキャン パフォーマンスが低下する可能性があります。TiKV の MVCC インメモリ エンジンは、最新の MVCC バージョンをメモリにキャッシュし、高速な GC メカニズムを使用して履歴バージョンをメモリから削除することで、スキャン パフォーマンスを向上させます。

    バージョン8.5.0以降、TiKVはMVCCインメモリエンジンを導入しました。TiKVクラスタにMVCCバージョンが蓄積されてスキャンパフォーマンスが低下する場合は、TiKV構成パラメータ[`in-memory-engine.enable`](/tikv-in-memory-engine.md#usage)を設定することで、TiKV MVCCインメモリエンジンを有効にしてスキャンパフォーマンスを向上させることができます。

    詳細については、 [ドキュメント](/tikv-in-memory-engine.md)参照してください。

### 信頼性 {#reliability}

-   PD [#5739](https://github.com/tikv/pd/issues/5739) @[rleungx](https://github.com/rleungx)で処理されるリクエストの最大レートと同時実行数を制限する機能をサポートします。

    PDにリクエストが急増すると、ワークロードが増大し、PDのパフォーマンスに影響を与える可能性があります。バージョン8.5.0以降では、 [`pd-ctl`](/pd-control.md)使用してPDが処理するリクエストの最大レートと同時実行数を制限し、安定性を向上させることができます。

    詳細については、 [ドキュメント](/pd-control.md)参照してください。

### SQL {#sql}

-   外部キー (GA) [#36982](https://github.com/pingcap/tidb/issues/36982) @[YangKeao](https://github.com/YangKeao) @[crazycs520](https://github.com/crazycs520)をサポート

    外部キー機能はバージョン8.5.0で一般提供開始（GA）となります。外部キー制約は、データの一貫性と整合性を確保するのに役立ちます。テーブル間の外部キー関係を容易に確立でき、カスケード更新とカスケード削除をサポートすることで、データ管理を簡素化します。この機能により、複雑なデータ関係を持つアプリケーションのサポートが強化されます。

    詳細については、 [ドキュメント](/foreign-key.md)参照してください。

-   オンラインで DDL ジョブを変更することをサポートする`ADMIN ALTER DDL JOBS`ステートメントを導入します[#57229](https://github.com/pingcap/tidb/issues/57229) @[fzzf678](https://github.com/fzzf678) @[tangenta](https://github.com/tangenta)

    バージョン8.3.0以降では、変数[`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size)と変数[`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt)セッションレベルで設定できるようになりました。そのため、これらの変数をグローバルに設定しても、実行中のすべてのDDLジョブには影響しなくなりました。これらの変数の値を変更するには、まずDDLジョブをキャンセルし、変数を調整してから、ジョブを再実行する必要があります。

    TiDB v8.5.0 では、特定の DDL ジョブの変数値をオンラインで調整できる`ADMIN ALTER DDL JOBS`ステートメントが導入されました。これにより、リソース消費とパフォーマンスの柔軟なバランス調整が可能になります。変更は個々のジョブに限定されるため、影響をより制御しやすくなります。例:

    -   `ADMIN ALTER DDL JOBS job_id THREAD = 8;` : 指定された DDL ジョブの`tidb_ddl_reorg_worker_cnt`オンラインで調整します。
    -   `ADMIN ALTER DDL JOBS job_id BATCH_SIZE = 256;` ：指定されたジョブの`tidb_ddl_reorg_batch_size`オンラインで調整します。
    -   `ADMIN ALTER DDL JOBS job_id MAX_WRITE_SPEED = '200MiB';` ：オンラインの各TiKVノードへのインデックスデータの書き込みトラフィックを調整します。

    詳細については、 [ドキュメント](/sql-statements/sql-statement-admin-alter-ddl.md)参照してください。

### Security {#security}

-   BRは、フルバックアップデータとログバックアップデータの両方のクライアント側暗号化をサポートします（GA） [#28640](https://github.com/pingcap/tidb/issues/28640) [#56433](https://github.com/pingcap/tidb/issues/56433) @[joccau](https://github.com/joccau) @[Tristan1900](https://github.com/Tristan1900)

    -   TiDB v5.3.0で実験的的に導入された、クライアント側でのフルバックアップデータの暗号化機能を使用すると、カスタムの固定キーを使用してクライアント側でバックアップデータを暗号化できます。

    -   ログバックアップデータのクライアント側暗号化（TiDB v8.4.0で実験的に導入）を使用すると、以下のいずれかの方法を使用してクライアント側でログバックアップデータを暗号化できます。

        -   カスタム固定キーを使用して暗号化する
        -   ローカルディスクに保存されているマスターキーを使用して暗号化します。
        -   キー管理サービス（KMS）によって管理されるマスターキーを使用して暗号化します。

    バージョン8.5.0以降、両方の暗号化機能が一般提供（GA）となり、クライアント側のデータセキュリティが強化されます。

    詳細については、 [バックアップデータを暗号化する](/br/br-snapshot-manual.md#encrypt-the-backup-data)と[ログバックアップデータを暗号化する](/br/br-pitr-manual.md#encrypt-the-log-backup-data)参照してください。

-   TiKVの保存時暗号化は[Google Cloud Key Management Service (Google Cloud KMS)](https://cloud.google.com/docs/security/key-management-deep-dive) （GA） [#8906](https://github.com/tikv/tikv/issues/8906) @[glorv](https://github.com/glorv)をサポートします

    TiKVは、保存データの暗号化に「保存時暗号化」技術を用いることで、データのセキュリティを確保します。この技術の中核となるのは、適切な鍵管理です。バージョン8.0.0では、TiKVの保存時暗号化において、マスターキー管理にGoogle Cloud KMSを試験的にサポートするようになりました。

    バージョン8.5.0以降、Google Cloud KMSを使用した保存データの暗号化が一般提供（GA）されます。この機能を使用するには、まずGoogle Cloudでキーを作成し、次にTiKV設定ファイルのセクション`[security.encryption.master-key]`を設定してください。

    詳細については、 [ドキュメント](/encryption-at-rest.md#tikv-encryption-at-rest)参照してください。

## 互換性の変更 {#compatibility-changes}

> **注記：**
>
> このセクションでは、バージョン8.4.0から最新バージョン（8.5.0）にアップグレードする際に知っておくべき互換性の変更点について説明します。バージョン8.3.0以前のバージョンから最新バージョンにアップグレードする場合は、中間バージョンで導入された互換性の変更点も確認する必要があるかもしれません。

### 行動の変化 {#behavior-changes}

-   非厳格モード（ `sql_mode = ''` ）では、 `NULL`列以外の列に`NULL`値を挿入すると、MySQL互換性の問題でエラーが返されるようになりました[#55457](https://github.com/pingcap/tidb/issues/55457) @[joechenrh](https://github.com/joechenrh)
-   `ALTER TABLE ... DROP FOREIGN KEY IF EXISTS ...`記述はサポートされなくなりました。 [#56703](https://github.com/pingcap/tidb/pull/56703) @[YangKeao](https://github.com/YangKeao)

### システム変数 {#system-variables}

| 変数名                                                                                                                | 種類を変更する  | 説明                                                                                                                                                                                                         |
| ------------------------------------------------------------------------------------------------------------------ | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-new-in-v800)                  | 修正済み     | さらなるテストの結果、デフォルト値を`OFF`から`ON`に変更しました。つまり、 [テーブル作成の高速化](/accelerated-table-creation.md)機能がデフォルトで有効になります。                                                                                                    |
| [`tidb_ddl_reorg_max_write_speed`](/system-variables.md#tidb_ddl_reorg_max_write_speed-new-in-v6512-v755-and-v850) | 新しく追加された | 各TiKVノードの書き込み帯域幅を制限し、インデックス作成の高速化が有効になっている場合（変数[`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)で制御）にのみ有効になります。たとえば、変数を`200MiB`に設定すると、最大書き込み速度が200 MiB/sに制限されます。 |

### コンフィグレーションパラメータ {#configuration-parameters}

| コンフィグレーションファイルまたはコンポーネント | コンフィグレーションパラメータ                                                                                                         | 種類を変更する  | 説明                                                                                                                                                 |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB                     | [`deprecate-integer-display-length`](/tidb-configuration-file.md#deprecate-integer-display-length)                      | 修正済み     | バージョン8.5.0以降、整数値による表示幅指定機能は非推奨となりました。この設定項目のデフォルト値は`false`から`true`に変更されました。                                                                        |
| ティクヴ                     | [`raft-client-queue-size`](/tikv-configuration-file.md#raft-client-queue-size)                                          | 修正済み     | デフォルト値を`8192`から`16384`に変更します。                                                                                                                      |
| ティクヴ                     | [`in-memory-engine.capacity`](/tikv-configuration-file.md#capacity-new-in-v850)                                         | 新しく追加された | TiKV MVCC インメモリエンジンが使用できる最大メモリサイズを制御します。デフォルト値は`min(the system memory * 10%, 5 GiB)`です。                                                            |
| ティクヴ                     | [`in-memory-engine.enable`](/tikv-configuration-file.md#enable-new-in-v850)                                             | 新しく追加された | TiKV MVCCのインメモリエンジンを有効にして、マルチバージョンクエリを高速化するかどうかを制御します。デフォルト値は`false`で、これはインメモリエンジンが無効になっていることを意味します。                                               |
| ティクヴ                     | [`in-memory-engine.gc-run-interval`](/tikv-configuration-file.md#gc-run-interval-new-in-v850)                           | 新しく追加された | インメモリエンジンがキャッシュされたMVCCバージョンに対してガベージコレクション（GC）を実行する時間間隔を制御します。デフォルト値は`"3m"`です。                                                                      |
| ティクヴ                     | [`in-memory-engine.mvcc-amplification-threshold`](/tikv-configuration-file.md#mvcc-amplification-threshold-new-in-v850) | 新しく追加された | インメモリエンジンがリージョンを選択してロードする際の、MVCC読み取り増幅のしきい値を制御します。デフォルト値は`10`で、リージョン内の1行を読み取るのに10を超えるMVCCバージョンを処理する必要がある場合は、そのリージョンがインメモリエンジンにロードされる可能性があることを示します。 |
| PD                       | [`patrol-region-worker-count`](/pd-configuration-file.md#patrol-region-worker-count-new-in-v850)                        | 新しく追加された | リージョンの健全性状態を検査する際にチェッカーによって作成される同時実行[オペレーター](/glossary.md#operator)の数を制御します。                                                                       |
| BR                       | [`--checksum`](/br/br-snapshot-manual.md)                                                                               | 修正済み     | デフォルト値を`true`から`false`に変更します。これは、デフォルトではBRがフルバックアップ中にテーブルレベルのチェックサムを計算しないことを意味し、バックアップのパフォーマンスを向上させます。                                             |

### オペレーティングシステムとプラットフォームの要件変更 {#operating-system-and-platform-requirement-changes}

TiDB をアップグレードする前に、オペレーティングシステムのバージョンが[OSおよびプラットフォームの要件](/hardware-and-software-requirements.md#os-and-platform-requirements)満たしていることを確認してください。

-   [CentOS Linux サポート終了](https://www.centos.org/centos-linux-eol/)によると、CentOS Linux 7のアップストリームサポートは2024年6月30日に終了しました。そのため、TiDBはv8.4.0およびv8.5.0でCentOS 7のサポートを終了します。Rocky Linux 9.1以降のバージョンを使用することをお勧めします。CentOS 7上のTiDBクラスタをv8.4.0またはv8.5.0にアップグレードすると、クラスタが利用できなくなるリスクがあります。CentOS Linux 7をまだ使用しているユーザーを支援するために、TiDB v8.5.1ではCentOS Linux 7のテストが再開され、互換性があります。詳細については、 [TiDB v8.5.1 リリースノート](/releases/release-8.5.1.md)参照してください。
-   [Red Hat Enterprise Linux ライフサイクル](https://access.redhat.com/support/policy/updates/errata/#Life_Cycle_Dates)によると、Red Hat Enterprise Linux 7の保守サポートは2024年6月30日に終了しました。TiDBはv8.4.0以降、Red Hat Enterprise Linux 7のサポートを終了します。Rocky Linux 9.1以降のバージョンを使用することをお勧めします。Red Hat Enterprise Linux 7上のTiDBクラスタをv8.4.0以降にアップグレードすると、クラスタが利用できなくなります。

## 削除された機能 {#removed-features}

-   以下の機能が削除されました。

    -   v8.4.0 では、 [TiDBBinlog](https://docs.pingcap.com/tidb/v8.3/tidb-binlog-overview)は削除されました。v8.3.0 以降、TiDB Binlog は完全に非推奨となりました。増分データレプリケーションには、代わりに[TiCDC](/ticdc/ticdc-overview.md)使用してください。ポイントインタイムリカバリ(PITR) には、 [PITR](/br/br-pitr-guide.md)使用してください。TiDB クラスタを v8.4.0 以降のバージョンにアップグレードする前に、必ず TiCDC と PITR に切り替えてください。

-   今後のバージョンでは、以下の機能が削除される予定です。

    -   バージョン8.0.0以降、 TiDB Lightningは物理インポートモードにおける[旧バージョンの競合検出](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#the-old-version-of-conflict-detection-deprecated-in-v800)戦略を非推奨とし、 [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)番目のパラメータを使用して論理インポートモードと物理インポートモードの両方で競合検出戦略を制御できるようにしました。旧バージョンの競合検出に使用される[`duplicate-resolution`](/tidb-lightning/tidb-lightning-configuration.md)のパラメータは、今後のリリースで削除される予定です。

## 非推奨機能 {#deprecated-features}

以下の機能は、将来のバージョンで廃止される予定です。

-   TiDB v8.0.0では、統計情報を自動的に収集するタスクの順序を最適化するために優先度キューを有効にするかどうかを制御するシステム変数[`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-new-in-v800)が導入されました。今後のリリースでは、統計情報を自動的に収集するタスクの順序付けには優先度キューが唯一の方法となるため、このシステム変数は非推奨となります。
-   バージョン7.5.0では、TiDBにシステム変数[`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-new-in-v750)導入されました。この変数を使用すると、TiDBがパーティション統計の非同期マージを使用するように設定し、メモリ不足の問題を回避できます。今後のリリースでは、パーティション統計は非同期でマージされるため、このシステム変数は非推奨となります。
-   今後のリリースでは、 [実行プランバインディングの自動進化](/sql-plan-management.md#baseline-evolution)再設計する予定であり、関連する変数と動作が変更されます。
-   バージョン8.0.0では、TiDBが並列ハッシュアグリゲーションアルゴリズムのディスクスピルをサポートするかどうかを制御するシステム変数[`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-new-in-v800)導入されました。今後のバージョンでは、このシステム変数は非推奨となります。
-   TiDB v5.1では、パーティションテーブルの動的プルーニングモードを有効にするかどうかを制御するシステム変数[`tidb_partition_prune_mode`](/system-variables.md#tidb_partition_prune_mode-new-in-v51)が導入されました。v8.5.0以降では、この変数を`static`または`static-only`に設定すると警告が表示されます。今後のバージョンでは、このシステム変数は非推奨となります。
-   TiDB Lightningパラメータ[`conflict.max-record-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)は、今後のリリースで非推奨となり、その後削除されます。このパラメータは[`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)に置き換えられます。これは、競合するレコードの最大数が、単一のインポート タスクで許容できる競合レコードの最大数と一致することを意味します。
-   バージョン6.3.0以降、パーティションテーブルではデフォルトで[動的剪定モード](/partitioned-table.md#dynamic-pruning-mode)使用されます。静的プルーニングモードと比較して、動的プルーニングモードはIndexJoinやプランキャッシュなどの機能をサポートし、パフォーマンスが向上しています。そのため、静的プルーニングモードは非推奨となります。

## 改善点 {#improvements}

-   TiDB

    -   分散実行フレームワーク（DXF） [#56017](https://github.com/pingcap/tidb/issues/56017) @[lance6716](https://github.com/lance6716)を無効にした場合の、 `ADD INDEX`アクセラレーション機能におけるジョブキャンセルの応答速度を改善します。
    -   小規模テーブルへのインデックス追加速度を改善する[#54230](https://github.com/pingcap/tidb/issues/54230) @[tangenta](https://github.com/tangenta)
    -   インデックス[#57156](https://github.com/pingcap/tidb/issues/57156) @[CbcWestwolf](https://github.com/CbcWestwolf)を追加する際の取り込みフェーズの最大速度を制限する新しいシステム変数`tidb_ddl_reorg_max_write_speed`を追加します。
    -   クエリ`information_schema.tables`のパフォーマンスを場合によっては改善する[#57295](https://github.com/pingcap/tidb/issues/57295) @[tangenta](https://github.com/tangenta)
    -   より多くのDDLジョブパラメータを動的に調整するサポート[#57526](https://github.com/pingcap/tidb/issues/57526) @[fzzf678](https://github.com/fzzf678)
    -   パーティション式[#56230](https://github.com/pingcap/tidb/issues/56230) @[Defined2014](https://github.com/Defined2014)のすべての列を含むグローバル インデックスをサポートします
    -   範囲クエリシナリオにおけるリストパーティションテーブルのパーティションプルーニングのサポート[#56673](https://github.com/pingcap/tidb/issues/56673) @[Defined2014](https://github.com/Defined2014)
    -   FixControl#46177をデフォルトで有効にして、場合によってはインデックス範囲スキャンではなくフルテーブルスキャンが誤って選択される問題を修正します[#46177](https://github.com/pingcap/tidb/issues/46177) @[terry1purcell](https://github.com/terry1purcell)
    -   内部推定ロジックを改善し、複数列および複数値インデックスの統計情報をより効果的に活用することで、複数値インデックスを含む特定のクエリの推定精度を向上させます[#56915](https://github.com/pingcap/tidb/issues/56915) @[time-and-fate](https://github.com/time-and-fate)
    -   特定のシナリオにおけるフルテーブルスキャンのコスト見積もりを改善し、フルテーブルスキャンを誤って選択する確率を低減します[#57085](https://github.com/pingcap/tidb/issues/57085) @[terry1purcell](https://github.com/terry1purcell)
    -   統計情報の同期読み込みに必要なデータ量を最適化して、読み込みパフォーマンスを向上させます[#56812](https://github.com/pingcap/tidb/issues/56812) @[winoros](https://github.com/winoros)
    -   `OUTER JOIN`インデックスと`ORDER BY ... LIMIT`を含む特定のケースで実行プランを最適化し、実行効率を向上させます[#56321](https://github.com/pingcap/tidb/issues/56321) @[winoros](https://github.com/winoros)

-   ティクヴ

    -   レプリカのクリーンアップには別のスレッドを使用し、 Raftの読み取りと書き込みのクリティカル パスのレイテンシーを安定させます[#16001](https://github.com/tikv/tikv/issues/16001) @[hbisheng](https://github.com/hbisheng)
    -   SIMD [#17290](https://github.com/tikv/tikv/issues/17290) @[EricZequan](https://github.com/EricZequan)をサポートすることで、ベクトル距離関数のパフォーマンスを向上させます。

-   PD

    -   `tso`サービスのマイクロサービスモードと非マイクロサービスモード間の動的な切り替えをサポートする[#8477](https://github.com/tikv/pd/issues/8477) @[rleungx](https://github.com/rleungx)
    -   出力`pd-ctl config`特定のフィールドのケース形式を最適化します[#8694](https://github.com/tikv/pd/issues/8694) @[lhy1024](https://github.com/lhy1024)
    -   [ストア制限v2](/configure-store-limit.md#principles-of-store-limit-v2)が一般提供開始（GA） [#8865](https://github.com/tikv/pd/issues/8865) @[lhy1024](https://github.com/lhy1024)
    -   リージョン検査の同時実行設定をサポート（実験的） [#8866](https://github.com/tikv/pd/issues/8866) @[lhy1024](https://github.com/lhy1024)

-   TiFlash

    -   クラスタ化インデックスを持つテーブルのバックグラウンドでの古いデータのガベージコレクション速度を改善[#9529](https://github.com/pingcap/tiflash/issues/9529) @[JaySon-Huang](https://github.com/JaySon-Huang)
    -   データ更新シナリオ[#9599](https://github.com/pingcap/tiflash/issues/9599)におけるベクトル検索のクエリパフォーマンスを向上させる @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    -   ベクトルインデックス構築中のCPU使用率の監視メトリクスを追加します[#9032](https://github.com/pingcap/tiflash/issues/9032) @[JaySon-Huang](https://github.com/JaySon-Huang)
    -   論理演算子[#9146](https://github.com/pingcap/tiflash/issues/9146) @[windtalker](https://github.com/windtalker)の実行効率を向上させる

-   ツール

    -   バックアップと復元 (BR)

        -   バックアップ中の不要なログ出力を減らす[#55902](https://github.com/pingcap/tidb/issues/55902) @[Leavrth](https://github.com/Leavrth)
        -   暗号化キー`--crypter.key` [#56388](https://github.com/pingcap/tidb/issues/56388) @[Tristan1900](https://github.com/Tristan1900)のエラーメッセージを最適化します
        -   データベース作成時のBRの同時実行数を増やしてデータ復元パフォーマンスを向上させる[#56866](https://github.com/pingcap/tidb/issues/56866) @[Leavrth](https://github.com/Leavrth)
        -   フルバックアップ中にテーブルレベルのチェックサム計算をデフォルトで無効にする（ `--checksum=false` ）ことで、バックアップパフォーマンスを向上させることができます[#56373](https://github.com/pingcap/tidb/issues/56373) @[Tristan1900](https://github.com/Tristan1900)
        -   各storageノードの接続タイムアウトを個別に追跡およびリセットするメカニズムを追加し、低速ノードの処理を強化し、バックアップ操作がハングアップするのを防ぎます[#57666](https://github.com/pingcap/tidb/issues/57666) @[3pointer](https://github.com/3pointer)

    -   TiDBデータ移行（DM）

        -   DMクラスタ起動時にDMワーカーがDMマスターに接続するための再試行を追加[#4287](https://github.com/pingcap/tiflow/issues/4287) @[GMHDBJD](https://github.com/GMHDBJD)

## バグ修正 {#bug-fixes}

-   TiDB

    -   TiDBがPDから返されるリージョンメタデータにLeader情報が含まれていない場合にリクエストを自動的に再試行しない問題を修正し、実行エラーが発生する可能性があった[#56757](https://github.com/pingcap/tidb/issues/56757) @[cfzjywxk](https://github.com/cfzjywxk)
    -   書き込み競合が発生した場合にTTLタスクをキャンセルできない問題を修正[#56422](https://github.com/pingcap/tidb/issues/56422) @[YangKeao](https://github.com/YangKeao)
    -   TTLタスクをキャンセルした際に、対応するSQLが強制終了されない問題を修正しました[#56511](https://github.com/pingcap/tidb/issues/56511) @[lcwangchao](https://github.com/lcwangchao)
    -   v6.5からv7.5以降にアップグレードしたクラスターで、既存のTTLタスクが予期せず頻繁に実行される問題を修正します[#56539](https://github.com/pingcap/tidb/issues/56539) @[lcwangchao](https://github.com/lcwangchao)
    -   `INSERT ... ON DUPLICATE KEY`ステートメントが`mysql_insert_id` [#55965](https://github.com/pingcap/tidb/issues/55965) @[tiancaiamao](https://github.com/tiancaiamao)と互換性がない問題を修正します
    -   TiKVがstorageエンジンとして選択されていない場合、TTLが失敗する可能性がある問題を修正しました[#56402](https://github.com/pingcap/tidb/issues/56402) @[YangKeao](https://github.com/YangKeao)
    -   `IMPORT INTO`ステートメントを使用してデータをインポートした後、 `AUTO_INCREMENT`フィールドが正しく設定されない問題を修正します[#56476](https://github.com/pingcap/tidb/issues/56476) @[D3Hunter](https://github.com/D3Hunter)
    -   TiDBが`ADD INDEX` [#56930](https://github.com/pingcap/tidb/issues/56930) @[fzzf678](https://github.com/fzzf678)を実行する際にインデックス長の制限をチェックしない問題を修正します
    -   `RECOVER TABLE BY JOB JOB_ID;`実行すると TiDB がpanicを起こす可能性がある問題を修正[#55113](https://github.com/pingcap/tidb/issues/55113) @[crazycs520](https://github.com/crazycs520)
    -   古い読み取りが読み取り操作のタイムスタンプを厳密に検証しないため、TSOと実際の物理時間の間にオフセットが存在する場合にトランザクションの一貫性に影響を与える可能性がわずかにある問題を修正しました[#56809](https://github.com/pingcap/tidb/issues/56809) @[MyonKeminta](https://github.com/MyonKeminta)
    -   DDLオーナーノードが切り替わった後、TiDBがReorg DDLタスクを以前の進行状況から再開できない問題を修正しました[#56506](https://github.com/pingcap/tidb/issues/56506) @[tangenta](https://github.com/tangenta)
    -   分散実行フレームワーク（DXF）の監視パネルの一部のメトリックが不正確である問題を修正します[#57172](https://github.com/pingcap/tidb/issues/57172) @[fzzf678](https://github.com/fzzf678) [#56942](https://github.com/pingcap/tidb/issues/56942) @[fzzf678](https://github.com/fzzf678)
    -   特定のケースでエラー理由が返されない問題[#56634](https://github.com/pingcap/tidb/issues/56634) `REORGANIZE PARTITION` [ムジョンス](https://github.com/mjonss)
    -   クエリ`INFORMATION_SCHEMA.TABLES`で大文字小文字の区別により誤った結果が返される問題を修正[#56987](https://github.com/pingcap/tidb/issues/56987) @[joechenrh](https://github.com/joechenrh)
    -   共通テーブル式（CTE）に複数のデータコンシューマーがあり、そのうちの1つのコンシューマーがデータを読み取らずに終了した場合に発生する可能性のある、無効なメモリアクセスの問題を修正します[#55881](https://github.com/pingcap/tidb/issues/55881) @[windtalker](https://github.com/windtalker)
    -   異常終了時に`INDEX_HASH_JOIN`ハングアップする可能性がある問題を修正[#54055](https://github.com/pingcap/tidb/issues/54055) @[wshwsh12](https://github.com/wshwsh12)
    -   `TRUNCATE`ステートメントが`NULL`値[#53546](https://github.com/pingcap/tidb/issues/53546) @[tuziemon](https://github.com/tuziemon)を処理する際に誤った結果を返す問題を修正します
    -   型推論エラーにより関数`CAST AS CHAR`が誤った結果を返す問題を修正[#56640](https://github.com/pingcap/tidb/issues/56640) @[zimulala](https://github.com/zimulala)
    -   型推論エラーにより一部の関数の出力で文字列が切り詰められる問題を修正しました[#56587](https://github.com/pingcap/tidb/issues/56587) @[joechenrh](https://github.com/joechenrh)
    -   `ADDTIME()`と`SUBTIME()`関数が最初の引数が日付型の場合に誤った結果を返す問題を修正しました[#57569](https://github.com/pingcap/tidb/issues/57569) @[xzhangxian1008](https://github.com/xzhangxian1008)
    -   非厳格モードで無効な`NULL`値が挿入される問題を修正します（ `sql_mode = ''` ） [#56381](https://github.com/pingcap/tidb/issues/56381) @[joechenrh](https://github.com/joechenrh)
    -   `UPDATE`ステートメントが`ENUM`型の[#56832](https://github.com/pingcap/tidb/issues/56832) @[xhebox](https://github.com/xhebox)の値を誤って更新する問題を修正します
    -   `tidb_low_resolution_tso`変数を有効にすると、 `SELECT FOR UPDATE`ステートメントの実行中にリソース リークが発生する問題を修正します[#55468](https://github.com/pingcap/tidb/issues/55468) @[tiancaiamao](https://github.com/tiancaiamao)
    -   `JSON_TYPE()`関数がパラメータの型を検証しないため、JSON 以外のデータ型が渡されたときにエラーが返されない問題を修正しました[#54029](https://github.com/pingcap/tidb/issues/54029) @[YangKeao](https://github.com/YangKeao)
    -   JSON関数を`PREPARE`ステートメントで使用すると実行エラーが発生する可能性がある問題を修正しました[#54044](https://github.com/pingcap/tidb/issues/54044) @[YangKeao](https://github.com/YangKeao)
    -   `BIT`型から`CHAR`型へのデータ変換時にTiKVパニックが発生する可能性がある問題を修正しました[#56494](https://github.com/pingcap/tidb/issues/56494) @[lcwangchao](https://github.com/lcwangchao)
    -   `CREATE VIEW`ステートメントで変数またはパラメータを使用してもエラー[#53176](https://github.com/pingcap/tidb/issues/53176) @[mjonss](https://github.com/mjonss)が報告されない問題を修正します
    -   `JSON_VALID()`関数が誤った結果を返す問題を修正[#56293](https://github.com/pingcap/tidb/issues/56293) @[YangKeao](https://github.com/YangKeao)
    -   変数`tidb_ttl_job_enable`が無効化された後もTTLタスクがキャンセルされない問題を修正[#57404](https://github.com/pingcap/tidb/issues/57404) @[YangKeao](https://github.com/YangKeao)
    -   パーティション関数`RANGE COLUMNS`と照合順序`utf8mb4_0900_ai_ci`を同時に使用すると、クエリ結果が正しくない可能性がある問題を修正しました[#57261](https://github.com/pingcap/tidb/issues/57261) @[Defined2014](https://github.com/Defined2014)
    -   改行文字で始まるプリペアドステートメント済みステートメントの実行によって発生する実行時エラーを修正します。このエラーにより、配列の範囲外エラーが発生します[#54283](https://github.com/pingcap/tidb/issues/54283) @[Defined2014](https://github.com/Defined2014)
    -   `UTC_TIMESTAMP()`関数の精度に関する問題を修正します。例えば、精度を高く設定しすぎているなどです[#56451](https://github.com/pingcap/tidb/issues/56451) @[chagelo](https://github.com/chagelo)
    -   `UPDATE` `INSERT` `DELETE IGNORE`ステートメントで外部キーのエラーが省略されない問題を修正します[#56678](https://github.com/pingcap/tidb/issues/56678) @[YangKeao](https://github.com/YangKeao)
    -   テーブル`information_schema.cluster_slow_query`をクエリする際に、時間フィルタが追加されていない場合、最新のスローログファイルのみがクエリされる問題を修正しました[#56100](https://github.com/pingcap/tidb/issues/56100) @[crazycs520](https://github.com/crazycs520)
    -   TTLテーブル[#56934](https://github.com/pingcap/tidb/issues/56934)のメモリリークの問題を修正 @[lcwangchao](https://github.com/lcwangchao)
    -   ステータス`write_only`のテーブルで外部キー制約が有効にならず、ステータス`non-public`のテーブルが使用できなくなる問題を修正します[#55813](https://github.com/pingcap/tidb/issues/55813) @[YangKeao](https://github.com/YangKeao)
    -   `NATURAL JOIN`または`USING`句の後にサブクエリを使用するとエラー[#53766](https://github.com/pingcap/tidb/issues/53766) @[dash12653](https://github.com/dash12653)が発生する可能性がある問題を修正しました
    -   CTEに`ORDER BY` `LIMIT`または`SELECT DISTINCT`句が含まれており、別のCTEの再帰部分から参照されている場合、誤ってインライン化されて実行エラー[#56603](https://github.com/pingcap/tidb/issues/56603) @[elsa0520](https://github.com/elsa0520)が発生する可能性がある問題を修正しました。
    -   `VIEW`で定義されたCTEが誤ってインライン化されている問題を修正します[#56582](https://github.com/pingcap/tidb/issues/56582) @[elsa0520](https://github.com/elsa0520)
    -   Plan Replayerが外部キー[#56456](https://github.com/pingcap/tidb/issues/56456) @[hawkingrei](https://github.com/hawkingrei)を含むテーブル構造をインポートする際にエラーを報告する可能性がある問題を修正しました。
    -   Plan Replayer が配置ルール[#54961](https://github.com/pingcap/tidb/issues/54961) @[hawkingrei](https://github.com/hawkingrei)を含むテーブル構造をインポートする際にエラーを報告する可能性がある問題を修正しました。
    -   テーブルの統計情報を収集するために`ANALYZE`使用する際に、テーブルに仮想的に生成された列の式インデックスが含まれている場合、実行時にエラー[#57079](https://github.com/pingcap/tidb/issues/57079) @[hawkingrei](https://github.com/hawkingrei)が報告される問題を修正しました。
    -   `DROP DATABASE`ステートメントが統計[#57227](https://github.com/pingcap/tidb/issues/57227) @[Rustin170506](https://github.com/Rustin170506)の対応する更新を正しくトリガーしない問題を修正します
    -   CTEでデータベース名を解析する際に、誤ったデータベース名が返される問題を修正しました[#54582](https://github.com/pingcap/tidb/issues/54582) @[hawkingrei](https://github.com/hawkingrei)
    -   統計情報を`DUMP STATS`に変換する際に、ヒストグラムの上限と下限が破損する問題を修正しました[#56083](https://github.com/pingcap/tidb/issues/56083) @[hawkingrei](https://github.com/hawkingrei)
    -   `EXISTS`の結果が、代数演算にさらに関与した場合、MySQL [#56641](https://github.com/pingcap/tidb/issues/56641)の結果と異なる可能性がある問題を修正しました @[windtalker](https://github.com/windtalker)
    -   エイリアス[#56726](https://github.com/pingcap/tidb/issues/56726) @[hawkingrei](https://github.com/hawkingrei)を持つマルチテーブル`DELETE`ステートメントに対して実行プランバインディングを作成できない問題を修正します。
    -   オプティマイザが複雑な述語を簡略化する際に文字セットと照合順序を考慮しないため、実行エラーが発生する可能性がある問題を修正しました[#56479](https://github.com/pingcap/tidb/issues/56479) @[dash12653](https://github.com/dash12653)
    -   Grafanaの**Stats Healthy Distribution**パネルのデータが正しくない可能性がある問題を修正しました[#57176](https://github.com/pingcap/tidb/issues/57176) @[hawkingrei](https://github.com/hawkingrei)
    -   クラスタ化インデックスを持つテーブルをクエリする際に、ベクトル検索が誤った結果を返す可能性がある問題を修正しました[#57627](https://github.com/pingcap/tidb/issues/57627) @[winoros](https://github.com/winoros)

-   ティクヴ

    -   Raft Engine [#17383](https://github.com/tikv/tikv/issues/17383)のMemTable内の古いインデックスに読み取りスレッドがアクセスした際に発生するpanic問題を修正しました。@[LykxSassinator](https://github.com/LykxSassinator)
    -   多数のトランザクションが同じキーのロック解除をキューイングしており、キーが頻繁に更新される場合、デッドロック検出に過度の負荷がかかり、TiKV OOM の問題[#17394](https://github.com/tikv/tikv/issues/17394) @[MyonKeminta](https://github.com/MyonKeminta)が発生する可能性がある問題を修正しました。
    -   リソース制御のバックグラウンドタスクのCPU使用率が二重にカウントされる問題を修正[#17603](https://github.com/tikv/tikv/issues/17603) @[glorv](https://github.com/glorv)
    -   CDC内部タスクの蓄積によりTiKVのメモリ不足（OOM）が発生する可能性がある問題を修正しました[#17696](https://github.com/tikv/tikv/issues/17696) @[3AceShowHand](https://github.com/3AceShowHand)
    -   `raft-entry-max-size`高く設定しすぎると、大きなバッチ書き込みでパフォーマンスのジッターが発生する問題を修正します[#17701](https://github.com/tikv/tikv/issues/17701) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
    -   リージョン分割後、リーダーが迅速に選出されない問題を修正[#17602](https://github.com/tikv/tikv/issues/17602) @[LykxSassinator](https://github.com/LykxSassinator)
    -   TiKVが`RADIANS()`または`DEGREES()`関数を含むクエリを実行する際にpanic可能性がある問題を修正しました[#17852](https://github.com/tikv/tikv/issues/17852) @[gengliqi](https://github.com/gengliqi)
    -   休止状態のすべてのリージョンが起動されたときに書き込みジッターが発生する可能性がある問題を修正[#17101](https://github.com/tikv/tikv/issues/17101) @[hhwyt](https://github.com/hhwyt)

-   PD

    -   ホットスポットキャッシュ[#8698](https://github.com/tikv/pd/issues/8698)のメモリリーク問題を修正 @[lhy1024](https://github.com/lhy1024)
    -   リソースグループセレクターがどのパネルにも適用されない問題を修正します[#56572](https://github.com/pingcap/tidb/issues/56572) @[glorv](https://github.com/glorv)
    -   削除されたリソースグループが監視パネルに表示され続ける問題を修正します[#8716](https://github.com/tikv/pd/issues/8716) @[AndreMouche](https://github.com/AndreMouche)
    -   リージョン同期処理中の不明瞭なログ記述を修正[#8717](https://github.com/tikv/pd/issues/8717) @[lhy1024](https://github.com/lhy1024)
    -   ラベル統計[#8700](https://github.com/tikv/pd/issues/8700)のメモリリーク問題を修正 @[lhy1024](https://github.com/lhy1024)
    -   `tidb_enable_tso_follower_proxy` ～ `0`または`OFF`を設定してもTSOFollowerプロキシ機能が無効にならない問題を修正します[#8709](https://github.com/tikv/pd/issues/8709) @[JmPotato](https://github.com/JmPotato)

-   TiFlash

    -   `SUBSTRING()`関数が特定の整数型に対して`pos`および`len`引数をサポートしていないためクエリ エラー[#9473](https://github.com/pingcap/tiflash/issues/9473) @[gengliqi](https://github.com/gengliqi)が発生する問題を修正しました。
    -   分散型storageおよびコンピューティングアーキテクチャにおいて、 TiFlash書き込みノードをスケールアウトした後にベクトル検索のパフォーマンスが低下する可能性がある問題を修正しました[#9637](https://github.com/pingcap/tiflash/issues/9637) @[kolafish](https://github.com/kolafish)
    -   2番目のパラメータが負の値の場合に、 `SUBSTRING()`関数が誤った結果を返す問題を修正します[#9604](https://github.com/pingcap/tiflash/issues/9604) @[guo-shaoge](https://github.com/guo-shaoge)
    -   最初のパラメータが定数の場合に関数`REPLACE()`がエラーを返す問題を修正します[#9522](https://github.com/pingcap/tiflash/issues/9522) @[guo-shaoge](https://github.com/guo-shaoge)
    -   `LPAD()`と`RPAD()`関数が場合によっては誤った結果を返す問題を修正[#9465](https://github.com/pingcap/tiflash/issues/9465) @[guo-shaoge](https://github.com/guo-shaoge)
    -   ベクトルインデックスを作成した後、ベクトルインデックス構築のための内部タスクが予期せず中断された場合、 TiFlashが破損したデータを書き込み、再起動できなくなる可能性がある問題を修正しました[#9714](https://github.com/pingcap/tiflash/issues/9714) @[JaySon-Huang](https://github.com/JaySon-Huang)

-   ツール

    -   バックアップと復元 (BR)

        -   バックアップ中に未完了の範囲ギャップが多すぎる場合に発生するOOM問題を修正し、事前割り当てメモリの量を削減します[#53529](https://github.com/pingcap/tidb/issues/53529) @[Leavrth](https://github.com/Leavrth)
        -   グローバルインデックスのバックアップができない問題を修正[#57469](https://github.com/pingcap/tidb/issues/57469) @[Defined2014](https://github.com/Defined2014)
        -   ログに暗号化された情報が出力される可能性がある問題を修正[#57585](https://github.com/pingcap/tidb/issues/57585) @[kennytm](https://github.com/kennytm)
        -   アドバンサーがロックの競合を処理できない問題を修正[#57134](https://github.com/pingcap/tidb/issues/57134) @[3pointer](https://github.com/3pointer)
        -   `k8s.io/api`のバージョン[#57790](https://github.com/pingcap/tidb/issues/57790) @[BornChanger](https://github.com/BornChanger)にアップグレードすることで、潜在的なセキュリティ脆弱性を修正します。
        -   クラスター内に多数のテーブルが存在するが実際のデータサイズが小さい場合に、PITRタスクがエラー`Information schema is out of date`を返す可能性がある問題を修正しました[#57743](https://github.com/pingcap/tidb/issues/57743) @[Tristan1900](https://github.com/Tristan1900)
        -   アドバンサーの所有者が[#58031](https://github.com/pingcap/tidb/issues/58031) @[3pointer](https://github.com/3pointer)を切り替えたときに、ログバックアップが予期せず一時停止状態になる可能性がある問題を修正します。
        -   データベースまたはテーブルの復元時に、コマンド`tiup br restore`ターゲットクラスタテーブルが既に存在するかどうかのチェックを省略し、既存のテーブルを上書きする可能性がある問題を修正します[#58168](https://github.com/pingcap/tidb/issues/58168) @[RidRisR](https://github.com/RidRisR)

    -   TiCDC

        -   Debeziumプロトコル使用時にKafkaメッセージにキーフィールドが欠落する問題を修正[#1799](https://github.com/pingcap/tiflow/issues/1799) @[wk989898](https://github.com/wk989898)
        -   再実行モジュールがエラーを正しく報告しない問題を修正[#11744](https://github.com/pingcap/tiflow/issues/11744) @[CharlesCheung96](https://github.com/CharlesCheung96)
        -   TiDB DDL の所有者変更中に DDL タスクのスキーマ バージョンが非増分になった場合に、TiCDC が誤って DDL タスクを破棄してしまう問題を修正しました[#11714](https://github.com/pingcap/tiflow/issues/11714) @[wlwilliamx](https://github.com/wlwilliamx)

    -   TiDB Lightning

        -   TiDB LightningがTiKV [#56114](https://github.com/pingcap/tidb/issues/56114) @[fishiu](https://github.com/fishiu)から送信された過大サイズのメッセージを受信できない問題を修正します。
        -   物理インポートモード[#56814](https://github.com/pingcap/tidb/issues/56814)を使用してデータをインポートした後、 `AUTO_INCREMENT`値が高すぎるように設定される問題を修正します[D3ハンター](https://github.com/D3Hunter)

## 性能テスト {#performance-test}

TiDB v8.5.0 のパフォーマンスについては、 TiDB Cloud Dedicatedクラスターの[性能テストレポート](https://docs.pingcap.com/tidbcloud/v8.5-performance-highlights)を参照してください。

## 寄稿者 {#contributors}

TiDBコミュニティの以下の貢献者の皆様に感謝申し上げます。

-   [ダッシュ12653](https://github.com/dash12653) （初回投稿者）
-   [チャゲロ](https://github.com/chagelo) （初回投稿者）
-   [リンダサマー](https://github.com/LindaSummer)
-   [ソンジビン97](https://github.com/songzhibin97)
-   [ヘクシリー](https://github.com/Hexilee)
