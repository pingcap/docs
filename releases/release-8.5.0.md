---
title: TiDB 8.5.0 Release Notes
summary: TiDB 8.5.0 の新機能、互換性の変更、改善点、バグ修正について説明します。
---

# TiDB 8.5.0 リリースノート {#tidb-8-5-0-release-notes}

<EmailSubscriptionWrapper />

発売日：2024年12月19日

TiDB バージョン: 8.5.0

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v8.5/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v8.5/production-deployment-using-tiup)

TiDB 8.5.0 は長期サポートリリース (LTS) です。

以前のLTSバージョン8.1.0と比較して、8.5.0には[8.3.0-DMR](/releases/release-8.3.0.md) [8.2.0-DMR](/releases/release-8.2.0.md)リリースされた新機能、改善、バグ修正が含まれています。8.1.xから[8.4.0-DMR](/releases/release-8.4.0.md)にアップグレードする際は、バージョン[TiDB リリースノート PDF](https://docs-download.pingcap.com/pdf/tidb-v8.2-to-v8.5-en-release-notes.pdf)をダウンロードして、2つのLTSバージョン間のすべてのリリースノートをご覧いただけます。以下の表は、バージョン8.1.0から8.5.0への主な変更点です。

<table><thead><tr><th>カテゴリ</th><th>機能/拡張機能</th><th>説明</th></tr></thead><tbody><tr><td rowspan="7">スケーラビリティとパフォーマンス</td><td>多次元でのデータ処理レイテンシーを削減</td><td>TiDBはデータ処理を継続的に改良することでパフォーマンスを向上させ、金融シナリオにおける低レイテンシのSQL処理要件を効果的に満たします。主なアップデートは以下の通りです。<ul><li> <a href="https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_executor_concurrency-new-in-v50">並列ソート</a>をサポート（v8.2.0 で導入）</li><li> <a href="https://docs.pingcap.com/tidb/v8.5/tidb-configuration-file#batch-policy-new-in-v830">KV（キー値）リクエストのバッチ処理戦略</a>を最適化（v8.3.0 で導入）</li><li> <a href="https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_tso_client_rpc_mode-new-in-v840">TSO リクエストの並列モード</a>をサポート (v8.4.0 で導入)</li><li> <a href="https://docs.pingcap.com/tidb/v8.5/sql-statement-delete">DELETE</a>操作のリソース オーバーヘッドを削減します (v8.4.0 で導入)</li><li><a href="https://docs.pingcap.com/tidb/v8.5/cached-tables">キャッシュされたテーブル</a>のクエリ パフォーマンスを向上 (v8.4.0 で導入)</li><li><a href="https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_hash_join_version-new-in-v840">ハッシュ結合の最適化バージョン</a>を導入します（実験的、v8.4.0 で導入）</li></ul></td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v8.5/tikv-in-memory-engine">TiKV MVCC インメモリ エンジン (IME)</a> (v8.5.0 で導入)</td><td> TiKV MVCCインメモリエンジンは、最新のMVCCバージョンのデータをメモリにキャッシュします。これにより、TiKVは古いバージョンをスキップして最新のデータを迅速に取得できます。この機能は、データレコードが頻繁に更新されるシナリオや、履歴バージョンが長期間保持されるシナリオにおいて、データスキャンのパフォーマンスを大幅に向上させます。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v8.5/tune-region-performance#use-the-active-pd-follower-feature-to-enhance-the-scalability-of-pds-region-information-query-service">アクティブ PD フォロワーを使用して、PD のリージョン情報クエリ サービスを強化します</a>(v8.5.0 で GA)</td><td> TiDB v7.6.0では、PDフォロワーがリージョン情報クエリサービスを提供できる実験的機能「Active PD Follower 」が導入されました。この機能により、多数のTiDBノードとリージョンを持つクラスターにおいて、PDクラスターの<code>GetRegion</code>および<code>ScanRegions</code>リクエスト処理能力が向上し、PDリーダーのCPU負荷が軽減されます。v8.5.0では、この機能が一般提供（GA）されます。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_enable_instance_plan_cache-new-in-v840">インスタンスレベルの実行プランキャッシュ</a>（実験的、v8.4.0 で導入）</td><td>インスタンスレベルのプランキャッシュにより、同じTiDBインスタンス内のすべてのセッションでプランキャッシュを共有できます。セッションレベルのプランキャッシュと比較して、この機能はより多くの実行プランをメモリにキャッシュすることでSQLコンパイル時間を短縮し、全体的なSQL実行時間を短縮します。OLTPのパフォーマンスとスループットを向上させると同時に、メモリ使用量をより適切に制御し、データベースの安定性を高めます。</td></tr><tr><td><a href="https://docs.pingcap.com/tidb/v8.5/global-indexes">パーティションテーブルのグローバルインデックス</a>（v8.4.0 で GA）</td><td>グローバルインデックスは、パーティション化されていない列の取得効率を効果的に向上させ、一意のキーがパーティションキーを含んでいなければならないという制約を排除します。この機能により、TiDBパーティションテーブルの利用シナリオが拡張され、パーティションテーブルのパフォーマンスが向上し、特定のクエリシナリオにおけるリソース消費が削減されます。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_opt_projection_push_down-new-in-v610"><code>Projection</code>演算子のstorageエンジンへのデフォルトのプッシュダウン</a>(v8.3.0 で導入)</td><td> <code>Projection</code>演算子をstorageエンジンにプッシュダウンすることで、storageノード間の負荷を分散し、ノード間のデータ転送を削減できます。この最適化により、特定のSQLクエリの実行時間が短縮され、データベース全体のパフォーマンスが向上します。</td></tr><tr><td><a href="https://docs.pingcap.com/tidb/v8.5/statistics#collect-statistics-on-some-columns">統計情報を収集する際に不要な列を無視する</a>（v8.3.0 で導入）</td><td> TiDBは、オプティマイザが必要な情報を確実に取得できるという前提のもと、統計収集を高速化し、統計の適時性を向上させ、最適な実行プランが選択されることを保証することで、クラスターのパフォーマンスを向上させます。同時に、TiDBはシステムオーバーヘッドを削減し、リソース利用率を向上させます。</td></tr><tr><td rowspan="5">信頼性と可用性</td><td>大規模クラスタの安定性を向上</td><td>TiDBを使用してマルチテナントアプリケーションやSaaSアプリケーションを運用する企業は、多くの場合、多数のテーブルを保存する必要があります。v8.5.0では、TiDBは大規模クラスターの安定性を大幅に向上させます。<ul><li><a href="https://docs.pingcap.com/tidb/v8.5/schema-cache">スキーマ キャッシュ制御</a>と<a href="https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_stats_cache_mem_quota-new-in-v610">TiDB 統計キャッシュのメモリクォータの設定が</a>一般提供 (GA) され、過剰なメモリ消費によって発生する安定性の問題が軽減されます。</li><li> PD は、多数のリージョンによってもたらされる負荷に対処するために<a href="https://docs.pingcap.com/tidb/v8.5/tune-region-performance#use-the-active-pd-follower-feature-to-enhance-the-scalability-of-pds-region-information-query-service">Active Follower</a>を導入し、 <a href="https://docs.pingcap.com/tidb/v8.5/pd-microservices">PD によって処理されるサービスを徐々に分離して</a>独立した展開を実現します。</li><li> PD はリージョンハートビート処理のパフォーマンスを向上させ、単一のクラスターに対して数千万のリージョンをサポートします。</li><li> <a href="https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_auto_analyze_concurrency-new-in-v840">同時実行性を高め</a>、<a href="https://docs.pingcap.com/tidb/v8.5/statistics#collect-statistics-on-some-columns">収集されるオブジェクトの数を減らす</a>ことで、統計の収集と読み込みの効率が向上し、大規模なクラスターでの実行プランの安定性が確保されます。</li></ul></td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v8.5/tidb-resource-control-runaway-queries#query_limit-parameters">ランナウェイクエリのトリガーをさらにサポートし、リソース グループの切り替えをサポートします</a>(v8.4.0 で導入)</td><td>ランナウェイクエリは、予期せぬSQLパフォーマンス問題がシステムに与える影響を効果的に軽減する手段を提供します。TiDB v8.4.0では、コプロセッサーによって処理されたキー数（ <code>PROCESSED_KEYS</code> ）とリクエスト単位数（ <code>RU</code> ）を識別条件として導入し、識別されたクエリを指定されたリソースグループに配置することで、ランナウェイクエリをより正確に識別・制御します。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v8.5/tidb-resource-control-background-tasks#background-parameters">リソース制御のバックグラウンド タスクのリソース使用量の上限設定をサポート</a>(実験的、v8.4.0 で導入)</td><td>リソース制御において、バックグラウンドタスクの最大パーセンテージ制限を設定することで、様々なアプリケーションシステムのニーズに応じてリソース消費量を制御できます。これにより、バックグラウンドタスクの消費量を低く抑え、オンラインサービスの品質を確保できます。</td></tr><tr><td> TiProxyの使用事例の強化と拡大</td><td>TiDBの高可用性を実現する重要なコンポーネントである<a href="https://docs.pingcap.com/tidb/v8.5/tiproxy-overview">TiProxyは</a>、SQLトラフィックのアクセスと転送機能に加え、クラスタ変更の評価をサポートする機能を拡張しています。主な機能は以下のとおりです。<ul><li> <a href="https://docs.pingcap.com/tidb/v8.5/tiproxy-traffic-replay">TiProxy はトラフィックのキャプチャと再生をサポートします</a>(実験的、v8.4.0 で導入)</li><li> <a href="https://docs.pingcap.com/tidb/v8.5/tiproxy-overview">TiProxy は組み込みの仮想 IP 管理をサポートしています</a>(v8.3.0 で導入)</li><li> <a href="https://docs.pingcap.com/tidb/v8.5/tiproxy-load-balance">TiProxy は複数の負荷分散ポリシーをサポートします</a>(v8.2.0 で導入)</li></ul></td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_enable_parallel_hashagg_spill-new-in-v800">TiDBの並列HashAggアルゴリズムはディスクスピルをサポートします</a>（v8.2.0でGA）</td><td> HashAggは、同じフィールド値を持つ行を効率的に集計するためにTiDBで広く使用されている集計演算子です。TiDB v8.0.0では、処理速度をさらに向上させるための実験的機能として並列HashAggが導入されました。メモリリソースが不足している場合、並列HashAggは一時的にソートされたデータをディスクに書き出すことで、過剰なメモリ使用による潜在的なOOMリスクを回避します。これにより、ノードの安定性を維持しながらクエリパフォーマンスが向上します。v8.2.0では、この機能が一般提供（GA）され、デフォルトで有効化されているため、 <code>tidb_executor_concurrency</code>を使用して並列HashAggの同時実行性を安全に設定できます。</td></tr><tr><td rowspan="2"> SQL</td><td><a href="https://docs.pingcap.com/tidb/v8.5/foreign-key">外部キー</a>（v8.5.0 で GA）</td><td>外部キーは、データベースにおける制約であり、テーブル間の関係を確立することでデータの一貫性と整合性を確保します。子テーブルで参照されているデータが親テーブルにも存在することを保証し、無効なデータの挿入を防ぎます。また、外部キーはカスケード操作（削除や更新時の自動同期など）もサポートするため、ビジネスロジックの実装が簡素化され、データ関係を手動で管理する際の複雑さが軽減されます。</td></tr><tr><td><a href="https://docs.pingcap.com/ai/vector-search-overview">ベクトル検索</a>（実験的、v8.4.0 で導入）</td><td>ベクトル検索は、データのセマンティクスに基づいた検索手法であり、より関連性の高い検索結果を提供します。AIや大規模言語モデル（LLM）の中核関数の一つとして、ベクトル検索は検索拡張生成（RAG）、セマンティック検索、レコメンデーションシステムなど、様々なシナリオで活用できます。</td></tr><tr><td rowspan="3"> DB操作と可観測性</td><td><a href="https://docs.pingcap.com/tidb/v8.5/information-schema-processlist">メモリテーブルに TiKV および TiDB CPU 時間を表示する</a>(v8.4.0 で導入)</td><td> CPU時間がシステムテーブルに統合され、セッションやSQLの他のメトリクスと並べて表示されるようになりました。これにより、CPU消費量の多い操作を複数の視点から観察し、診断効率を向上させることができます。これは、インスタンスにおけるCPU使用率の急上昇や、クラスターにおける読み取り/書き込みのホットスポットといっ​​たシナリオの診断に特に役立ちます。</td></tr><tr><td><a href="https://docs.pingcap.com/tidb/v8.5/top-sql#use-top-sql">テーブルまたはデータベースごとに集計された TiKV CPU 時間の表示をサポート</a>(v8.4.0 で導入)</td><td>ホットスポットの問題が個々の SQL ステートメントによって発生していない場合は、 「Top SQL」のテーブルまたはデータベース レベル別に集計された CPU 時間を使用すると、ホットスポットの原因となっているテーブルまたはアプリケーションを迅速に特定できるため、ホットスポットと CPU 消費の問題の診断効率が大幅に向上します。</td></tr><tr><td><a href="https://docs.pingcap.com/tidb/v8.5/backup-and-restore-overview">バックアップとリストア（BR）</a>は、 <a href="https://aws.amazon.com/sdk-for-rust/">AWS SDK for Rust</a>を使用して外部storageにアクセスします（v8.5.0 で導入）</td><td> BRは、TiKVからAmazon S3などの外部storageにアクセスするために、オリジナルのRusotoライブラリを<a href="https://aws.amazon.com/sdk-for-rust/">AWS SDK for Rust</a>に置き換えました。この変更により、 <a href="https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html">IMDSv2</a>や<a href="https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html">EKS Pod Identity</a>などのAWS機能との互換性が向上します。</td></tr><tr><td rowspan="1">Security</td><td><a href="https://docs.pingcap.com/tidb/v8.5/br-snapshot-manual#encrypt-the-backup-data">スナップショット バックアップ データ</a>と<a href="https://docs.pingcap.com/tidb/v8.5/br-pitr-manual#encrypt-log-backup-data">ログ バックアップ データ</a>のクライアント側暗号化 (v8.5.0 で GA)</td><td>バックアップ データをバックアップstorageにアップロードする前に、バックアップ データを暗号化して、storage中および転送中のセキュリティを確保できます。</td></tr></tbody></table>

## 機能の詳細 {#feature-details}

### スケーラビリティ {#scalability}

-   スキーマキャッシュのメモリ制限設定が一般提供（GA）されました。テーブル数が数十万、あるいは数百万に達すると、この機能によりスキーマメタデータのメモリ使用量が大幅に削減されます[＃50959](https://github.com/pingcap/tidb/issues/50959) @ [天菜麻緒](https://github.com/tiancaiamao) @ [wjhuang2016](https://github.com/wjhuang2016) @ [gmhdbjd](https://github.com/gmhdbjd) @ [接線](https://github.com/tangenta)

    SaaS シナリオによっては、テーブル数が数十万、あるいは数百万に達する場合があり、スキーマメタデータが大量のメモリを消費することがあります。この機能を有効にすると、TiDB は Least Recently Used (LRU) アルゴリズムを使用して対応するスキーマメタデータをキャッシュおよび削除し、メモリ使用量を効果的に削減します。

    バージョン8.4.0以降、この機能はデフォルトで有効になっており、デフォルト値は`536870912` （つまり512MiB）です。必要に応じて変数[`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-new-in-v800)を使用して調整できます。

    詳細については[ドキュメント](/schema-cache.md)参照してください。

-   PDのリージョン情報クエリサービス（GA） [＃7431](https://github.com/tikv/pd/issues/7431) @ [okJiang](https://github.com/okJiang)のスケーラビリティを強化するために、アクティブPDFollower機能を提供します。

    多数のリージョンを持つTiDBクラスターでは、ハートビート処理とタスクのスケジューリングによるオーバーヘッドの増加により、PDリーダーのCPU負荷が高くなる可能性があります。クラスターに多数のTiDBインスタンスがあり、リージョン情報へのリクエストが同時に発生する場合、PDリーダーへのCPU負荷がさらに高まり、PDサービスが利用できなくなる可能性があります。

    高可用性を確保するため、TiDB v7.6.0 では、PD のリージョン情報クエリサービスのスケーラビリティを強化する実験的機能として Active PD Followerが導入されました。v8.5.0 では、この機能が一般提供 (GA) されます。Active PD Follower機能を有効にするには、システム変数[`pd_enable_follower_handle_region`](/system-variables.md#pd_enable_follower_handle_region-new-in-v760)を`ON`に設定します。この機能を有効にすると、TiDB はリージョン情報リクエストをすべての PD サーバーに均等に分散し、PD フォロワーもリージョンリクエストを処理できるようになるため、PD リーダーの CPU 負荷が軽減されます。

    詳細については[ドキュメント](/tune-region-performance.md#use-the-active-pd-follower-feature-to-enhance-the-scalability-of-pds-region-information-query-service)参照してください。

### パフォーマンス {#performance}

-   TiDB によるテーブル作成の高速化が一般提供 (GA) され、データ移行とクラスタ初期化時間が大幅に短縮されます[＃50052](https://github.com/pingcap/tidb/issues/50052) @ [D3ハンター](https://github.com/D3Hunter) @ [gmhdbjd](https://github.com/gmhdbjd)

    TiDB v7.6.0では、実験的機能として高速テーブル作成が導入され、システム変数[`tidb_ddl_version`](https://docs.pingcap.com/tidb/v7.6/system-variables#tidb_ddl_version-new-in-v760)によって制御されます。v8.0.0以降、このシステム変数の名前は[`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-new-in-v800)に変更されます。

    v8.5.0では、TiDB高速テーブル作成機能が一般提供（GA）され、デフォルトで有効化されます。この機能は、データ移行およびクラスター初期化中に数百万個のテーブルを迅速に作成し、操作時間を大幅に短縮します。

    詳細については[ドキュメント](/accelerated-table-creation.md)参照してください。

-   TiKVはMVCCインメモリエンジン（IME）をサポートしており、広範なMVCC履歴バージョン[＃16141](https://github.com/tikv/tikv/issues/16141) @ [スペードA-タン](https://github.com/SpadeA-Tang) @ [栄光](https://github.com/glorv) @ [金星の上](https://github.com/overvenus)のスキャンを含むクエリを高速化します。

    レコードが頻繁に更新される場合、またはTiDBが履歴バージョンを長期間（例えば24時間）保持する必要がある場合、MVCCバージョンの蓄積によってスキャンパフォーマンスが低下する可能性があります。TiKV MVCCインメモリエンジンは、最新のMVCCバージョンをメモリにキャッシュし、高速GCメカニズムを使用して履歴バージョンをメモリから削除することで、スキャンパフォーマンスを向上させます。

    バージョン8.5.0以降、TiKVにMVCCインメモリエンジンが導入されました。TiKVクラスター内でMVCCバージョンが蓄積され、スキャンパフォーマンスが低下する場合は、TiKV構成パラメータ[`in-memory-engine.enable`](/tikv-in-memory-engine.md#usage)を設定することで、TiKV MVCCインメモリエンジンを有効にし、スキャンパフォーマンスを向上させることができます。

    詳細については[ドキュメント](/tikv-in-memory-engine.md)参照してください。

### 信頼性 {#reliability}

-   PD [＃5739](https://github.com/tikv/pd/issues/5739) @ [rleungx](https://github.com/rleungx)で処理されるリクエストの最大レートと同時実行数の制限をサポート

    PDに大量のリクエストが送信されると、ワークロードの増加につながり、PDのパフォーマンスに影響を及ぼす可能性があります。v8.5.0以降では、 [`pd-ctl`](/pd-control.md)使用することでPDで処理されるリクエストの最大レートと同時実行数を制限し、PDの安定性を向上させることができます。

    詳細については[ドキュメント](/pd-control.md)参照してください。

### SQL {#sql}

-   外部キーのサポート (GA) [＃36982](https://github.com/pingcap/tidb/issues/36982) @ [ヤンケオ](https://github.com/YangKeao) @ [crazycs520](https://github.com/crazycs520)

    外部キー機能はv8.5.0で一般提供（GA）されます。外部キー制約は、データの一貫性と整合性の確保に役立ちます。テーブル間の外部キー関係を容易に確立でき、カスケード更新とカスケード削除をサポートすることで、データ管理を簡素化します。この機能により、複雑なデータ関係を持つアプリケーションのサポートが強化されます。

    詳細については[ドキュメント](/foreign-key.md)参照してください。

-   DDLジョブのオンライン変更をサポートするために`ADMIN ALTER DDL JOBS`ステートメントを導入します[＃57229](https://github.com/pingcap/tidb/issues/57229) @ [fzzf678](https://github.com/fzzf678) @ [接線](https://github.com/tangenta)

    バージョン8.3.0以降では、変数[`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size)と[`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt)セッションレベルで設定できるようになりました。そのため、これら2つの変数をグローバルに設定しても、実行中のすべてのDDLジョブには影響しなくなりました。これらの変数の値を変更するには、まずDDLジョブをキャンセルし、変数を調整してから、ジョブを再送信する必要があります。

    TiDB v8.5.0では、 `ADMIN ALTER DDL JOBS`文が導入され、特定のDDLジョブの変数値をオンラインで調整できるようになりました。これにより、リソース消費とパフォーマンスのバランスを柔軟に調整できます。変更は個々のジョブに限定されるため、影響をより制御しやすくなります。例えば、

    -   `ADMIN ALTER DDL JOBS job_id THREAD = 8;` : 指定された DDL ジョブの`tidb_ddl_reorg_worker_cnt`オンラインで調整します。
    -   `ADMIN ALTER DDL JOBS job_id BATCH_SIZE = 256;` : 指定されたジョブの`tidb_ddl_reorg_batch_size`オンラインで調整します。
    -   `ADMIN ALTER DDL JOBS job_id MAX_WRITE_SPEED = '200MiB';` : 各 TiKV ノードへのインデックス データの書き込みトラフィックをオンラインで調整します。

    詳細については[ドキュメント](/sql-statements/sql-statement-admin-alter-ddl.md)参照してください。

### Security {#security}

-   BRは、フルバックアップデータとログバックアップデータの両方のクライアント側暗号化をサポートします（GA） [＃28640](https://github.com/pingcap/tidb/issues/28640) [＃56433](https://github.com/pingcap/tidb/issues/56433) @ [ジョッカウ](https://github.com/joccau) @ [トリスタン1900](https://github.com/Tristan1900)

    -   完全バックアップ データのクライアント側暗号化 (TiDB v5.3.0 で実験的に導入) により、カスタム固定キーを使用してクライアント側でバックアップ データを暗号化できるようになります。

    -   ログ バックアップ データのクライアント側暗号化 (TiDB v8.4.0 で実験的に導入) を使用すると、次のいずれかの方法を使用してクライアント側でログ バックアップ データを暗号化できます。

        -   カスタム固定キーを使用して暗号化する
        -   ローカルディスクに保存されたマスターキーを使用して暗号化する
        -   キー管理サービス (KMS) によって管理されるマスター キーを使用して暗号化します。

    バージョン 8.5.0 以降では、両方の暗号化機能が一般提供 (GA) され、クライアント側のデータ セキュリティが強化されます。

    詳細については、 [バックアップデータを暗号化する](/br/br-snapshot-manual.md#encrypt-the-backup-data)および[ログバックアップデータを暗号化する](/br/br-pitr-manual.md#encrypt-the-log-backup-data)を参照してください。

-   保存時の TiKV 暗号化は[Google Cloud 鍵管理サービス (Google Cloud KMS)](https://cloud.google.com/docs/security/key-management-deep-dive) (GA) [＃8906](https://github.com/tikv/tikv/issues/8906) @ [栄光](https://github.com/glorv)をサポートします

    TiKVは、保存データの暗号化に保管時暗号化技術を用いることでデータセキュリティを確保します。この技術の中核となるのは、適切な鍵管理です。バージョン8.0.0では、TiKVの保管時暗号化は、マスター鍵管理にGoogle Cloud KMSを使用した試験的なサポートを開始しました。

    バージョン8.5.0以降、Google Cloud KMSを使用した保存時の暗号化が一般提供（GA）されます。この機能を使用するには、まずGoogle Cloudで鍵を作成し、TiKV設定ファイルの`[security.encryption.master-key]`セクションを設定してください。

    詳細については[ドキュメント](/encryption-at-rest.md#tikv-encryption-at-rest)参照してください。

## 互換性の変更 {#compatibility-changes}

> **注記：**
>
> このセクションでは、v8.4.0から最新バージョン（v8.5.0）にアップグレードする際に知っておくべき互換性の変更点について説明します。v8.3.0以前のバージョンから最新バージョンにアップグレードする場合は、中間バージョンで導入された互換性の変更点も確認する必要があるかもしれません。

### 行動の変化 {#behavior-changes}

-   非厳密モード（ `sql_mode = ''` ）では、 `NULL`以外の列に`NULL`値を挿入すると、MySQLとの互換性のためにエラーが返されるようになりました[＃55457](https://github.com/pingcap/tidb/issues/55457) @ [ジョーチェン](https://github.com/joechenrh)
-   `ALTER TABLE ... DROP FOREIGN KEY IF EXISTS ...`ステートメントはサポートされなくなりました[＃56703](https://github.com/pingcap/tidb/pull/56703) @ [ヤンケオ](https://github.com/YangKeao)

### システム変数 {#system-variables}

| 変数名                                                                                                                | タイプを変更   | 説明                                                                                                                                                                                                             |
| ------------------------------------------------------------------------------------------------------------------ | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-new-in-v800)                  | 修正済み     | さらにテストを行った後、デフォルト値を`OFF`から`ON`に変更します。つまり、 [高速テーブル作成](/accelerated-table-creation.md)機能はデフォルトで有効になります。                                                                                                          |
| [`tidb_ddl_reorg_max_write_speed`](/system-variables.md#tidb_ddl_reorg_max_write_speed-new-in-v6512-v755-and-v850) | 新しく追加された | 各TiKVノードの書き込み帯域幅を制限します。インデックス作成アクセラレーションが有効になっている場合（変数[`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)で制御）のみ有効になります。例えば、変数を`200MiB`に設定すると、最大書き込み速度は200MiB/sに制限されます。 |

### コンフィグレーションパラメータ {#configuration-parameters}

| コンフィグレーションファイルまたはコンポーネント | コンフィグレーションパラメータ                                                                                                         | タイプを変更   | 説明                                                                                                                                           |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| ティドブ                     | [`deprecate-integer-display-length`](/tidb-configuration-file.md#deprecate-integer-display-length)                      | 修正済み     | バージョン8.5.0以降、整数表示幅機能は非推奨となりました。この設定項目のデフォルト値は`false`から`true`に変更されました。                                                                        |
| ティクブ                     | [`raft-client-queue-size`](/tikv-configuration-file.md#raft-client-queue-size)                                          | 修正済み     | デフォルト値を`8192`から`16384`に変更します。                                                                                                                |
| ティクブ                     | [`in-memory-engine.capacity`](/tikv-configuration-file.md#capacity-new-in-v850)                                         | 新しく追加された | TiKV MVCCインメモリエンジンが使用できる最大メモリサイズを制御します。デフォルト値はシステムメモリの10%です。最大値は5GiBです。                                                                      |
| ティクブ                     | [`in-memory-engine.enable`](/tikv-configuration-file.md#enable-new-in-v850)                                             | 新しく追加された | マルチバージョンクエリを高速化するために、TiKV MVCCインメモリエンジンを有効にするかどうかを制御します。デフォルト値は`false`で、インメモリエンジンが無効であることを意味します。                                             |
| ティクブ                     | [`in-memory-engine.gc-run-interval`](/tikv-configuration-file.md#gc-run-interval-new-in-v850)                           | 新しく追加された | インメモリエンジンがキャッシュされたMVCCバージョンに対してガベージコレクション（GC）を実行する間隔を制御します。デフォルト値は`"3m"`です。                                                                  |
| ティクブ                     | [`in-memory-engine.mvcc-amplification-threshold`](/tikv-configuration-file.md#mvcc-amplification-threshold-new-in-v850) | 新しく追加された | インメモリエンジンがリージョンを選択してロードする際のMVCC読み取り増幅のしきい値を制御します。デフォルト値は`10`で、リージョン内の1行の読み取りに10を超えるMVCCバージョンの処理が必要な場合、このリージョンはインメモリエンジンにロードされる可能性があることを示します。 |
| PD                       | [`patrol-region-worker-count`](/pd-configuration-file.md#patrol-region-worker-count-new-in-v850)                        | 新しく追加された | リージョンのヘルス状態を検査するときにチェッカーによって作成される同時実行[オペレーター](/glossary.md#operator)の数を制御します。                                                                |
| BR                       | [`--checksum`](/br/br-snapshot-manual.md)                                                                               | 修正済み     | デフォルト値を`true`から`false`に変更します。これにより、 BR は、バックアップ パフォーマンスを向上させるために、フル バックアップ中にテーブル レベルのチェックサムをデフォルトで計算しなくなります。                                 |

### オペレーティング システムとプラットフォームの要件の変更 {#operating-system-and-platform-requirement-changes}

TiDB をアップグレードする前に、オペレーティング システムのバージョンが[OSおよびプラットフォームの要件](/hardware-and-software-requirements.md#os-and-platform-requirements)満たしていることを確認してください。

-   [CentOS Linux のサポート終了](https://www.centos.org/centos-linux-eol/)によると、CentOS Linux 7のアップストリームサポートは2024年6月30日に終了しました。そのため、TiDBはv8.4.0およびv8.5.0でCentOS 7のサポートを終了します。Rocky Linux 9.1以降のバージョンの使用をお勧めします。CentOS 7上のTiDBクラスタをv8.4.0またはv8.5.0にアップグレードすると、クラスタが利用できなくなるリスクがあります。CentOS Linux 7を引き続き使用しているユーザーを支援するため、TiDB v8.5.1ではCentOS Linux 7のテストを再開し、互換性を確保しています。詳細については、 [TiDB v8.5.1 リリースノート](/releases/release-8.5.1.md)参照してください。
-   [Red Hat Enterprise Linux ライフサイクル](https://access.redhat.com/support/policy/updates/errata/#Life_Cycle_Dates)によると、Red Hat Enterprise Linux 7のメンテナンスサポートは2024年6月30日に終了しました。TiDBはRed Hat Enterprise Linux 7 v8.4.0以降のサポートを終了します。Rocky Linux 9.1以降のバージョンの使用をお勧めします。Red Hat Enterprise Linux 7上のTiDBクラスタをv8.4.0以降にアップグレードすると、クラスタが使用できなくなります。

## 削除された機能 {#removed-features}

-   次の機能は削除されました:

    -   v8.4.0では、 [TiDBBinlog](https://docs.pingcap.com/tidb/v8.3/tidb-binlog-overview)は削除されました。v8.3.0以降、TiDB Binlogは完全に非推奨となりました。増分データレプリケーションの場合は、代わりに[TiCDC](/ticdc/ticdc-overview.md)使用してください。ポイントインタイムリカバリ（PITR）の場合は、 [PITR](/br/br-pitr-guide.md)使用してください。TiDBクラスターをv8.4.0以降のバージョンにアップグレードする前に、必ずTiCDCとPITRに切り替えてください。

-   以下の機能は将来のバージョンで削除される予定です。

    -   TiDB Lightning v8.0.0以降、物理インポートモードの[競合検出の古いバージョン](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#the-old-version-of-conflict-detection-deprecated-in-v800)戦略は非推奨となり、 [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)番目のパラメータを使用して論理インポートモードと物理インポートモードの両方の競合検出戦略を制御できるようになりました。旧バージョンの競合検出用の[`duplicate-resolution`](/tidb-lightning/tidb-lightning-configuration.md)のパラメータは、将来のリリースで削除される予定です。

## 非推奨の機能 {#deprecated-features}

以下の機能は将来のバージョンで廃止される予定です。

-   TiDB v8.0.0では、統計を自動収集するタスクの順序を最適化するために、優先度キューを有効にするかどうかを制御するシステム変数[`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-new-in-v800)が導入されました。将来のリリースでは、統計を自動収集するタスクの順序付けは優先度キューのみになるため、このシステム変数は廃止される予定です。
-   v7.5.0では、TiDBにシステム変数[`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-new-in-v750)導入されました。この変数を使用すると、TiDBがパーティション統計情報の非同期マージを使用することで、OOM問題を回避することができます。将来のリリースでは、パーティション統計情報は非同期にマージされるため、このシステム変数は非推奨となります。
-   以降のリリースでは[実行計画バインディングの自動進化](/sql-plan-management.md#baseline-evolution)再設計する予定であり、関連する変数と動作が変更されます。
-   TiDB v8.0.0では、並列HashAggアルゴリズムのディスクスピルをサポートするかどうかを制御するシステム変数[`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-new-in-v800)導入されました。将来のバージョンでは、このシステム変数は非推奨になります。
-   TiDB v5.1では、パーティションテーブルの動的プルーニングモードを有効にするかどうかを制御するシステム変数[`tidb_partition_prune_mode`](/system-variables.md#tidb_partition_prune_mode-new-in-v51)が導入されました。v8.5.0以降では、この変数を`static`または`static-only`に設定すると警告が返されます。将来のバージョンでは、このシステム変数は非推奨になります。
-   TiDB Lightningパラメータ[`conflict.max-record-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)は将来のリリースで廃止される予定であり、その後削除されます。このパラメータは[`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)に置き換えられます。これは、競合レコードの最大数が、単一のインポートタスクで許容される競合レコードの最大数と一致することを意味します。
-   バージョン6.3.0以降、パーティションテーブルはデフォルトで[動的プルーニングモード](/partitioned-table.md#dynamic-pruning-mode)使用します。静的プルーニングモードと比較して、動的プルーニングモードはIndexJoinやプランキャッシュなどの機能をサポートし、パフォーマンスが向上します。そのため、静的プルーニングモードは非推奨となります。

## 改善点 {#improvements}

-   ティドブ

    -   分散実行フレームワーク（DXF） [＃56017](https://github.com/pingcap/tidb/issues/56017) @ [ランス6716](https://github.com/lance6716)を無効にした場合の`ADD INDEX`加速機能のジョブキャンセルの応答速度を改善しました。
    -   小さなテーブルへのインデックス追加速度の向上[＃54230](https://github.com/pingcap/tidb/issues/54230) @ [接線](https://github.com/tangenta)
    -   インデックス[＃57156](https://github.com/pingcap/tidb/issues/57156) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)を追加する際の取り込みフェーズの最大速度を制限する新しいシステム変数`tidb_ddl_reorg_max_write_speed`を追加します。
    -   場合によっては`information_schema.tables`クエリのパフォーマンスを[＃57295](https://github.com/pingcap/tidb/issues/57295) @ [接線](https://github.com/tangenta)で改善
    -   より多くの DDL ジョブパラメータを動的に調整するサポート[＃57526](https://github.com/pingcap/tidb/issues/57526) @ [fzzf678](https://github.com/fzzf678)
    -   パーティション式[＃56230](https://github.com/pingcap/tidb/issues/56230) @ [定義2014](https://github.com/Defined2014)のすべての列を含むグローバルインデックスをサポートします。
    -   範囲クエリシナリオ[＃56673](https://github.com/pingcap/tidb/issues/56673) @ [定義2014](https://github.com/Defined2014)でリストパーティションテーブルのパーティションプルーニングをサポート
    -   FixControl#46177 をデフォルトで有効にして、場合によってはインデックス範囲スキャンではなくテーブル全体のスキャンが誤って選択される問題を修正します[＃46177](https://github.com/pingcap/tidb/issues/46177) @ [テリー・パーセル](https://github.com/terry1purcell)
    -   内部推定ロジックを改善し、複数列および複数値インデックスの統計をより有効に活用して、複数値インデックス[＃56915](https://github.com/pingcap/tidb/issues/56915) @ [時間と運命](https://github.com/time-and-fate)を含む特定のクエリの推定精度を向上させました。
    -   特定のシナリオにおけるフルテーブルスキャンのコスト見積りを改善し、誤ってフルテーブルスキャンを選択する可能性を低減します[＃57085](https://github.com/pingcap/tidb/issues/57085) @ [テリー・パーセル](https://github.com/terry1purcell)
    -   統計の同期ロードに必要なデータ量を最適化して、ロードパフォーマンスを向上させる[＃56812](https://github.com/pingcap/tidb/issues/56812) @ [ウィノロス](https://github.com/winoros)
    -   `OUTER JOIN`が一意のインデックスと`ORDER BY ... LIMIT`句を含む特定のケースで実行プランを最適化し、実行効率[＃56321](https://github.com/pingcap/tidb/issues/56321) @ [ウィノロス](https://github.com/winoros)を向上させます

-   ティクブ

    -   レプリカをクリーンアップするために別のスレッドを使用し、 Raft の読み取りと書き込みの重要なパスの安定したレイテンシーを確保します[＃16001](https://github.com/tikv/tikv/issues/16001) @ [ヒビシェン](https://github.com/hbisheng)
    -   SIMD [＃17290](https://github.com/tikv/tikv/issues/17290) @ [エリック・ゼクアン](https://github.com/EricZequan)をサポートすることでベクトル距離関数のパフォーマンスが向上します

-   PD

    -   `tso`サービスのマイクロサービス モードと非マイクロサービス モード間の動的切り替えをサポート[＃8477](https://github.com/tikv/pd/issues/8477) @ [rleungx](https://github.com/rleungx)
    -   `pd-ctl config`出力[＃8694](https://github.com/tikv/pd/issues/8694) @ [lhy1024](https://github.com/lhy1024)の特定のフィールドの大文字と小文字の形式を最適化します
    -   [店舗制限 v2](/configure-store-limit.md#principles-of-store-limit-v2)が一般公開（GA）される[＃8865](https://github.com/tikv/pd/issues/8865) @ [lhy1024](https://github.com/lhy1024)
    -   リージョン検査の同時実行の設定をサポート（実験的） [＃8866](https://github.com/tikv/pd/issues/8866) @ [lhy1024](https://github.com/lhy1024)

-   TiFlash

    -   クラスター化インデックス[＃9529](https://github.com/pingcap/tiflash/issues/9529) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)を持つテーブルで、バックグラウンドでの古いデータのガベージコレクションの速度が向上しました。
    -   データ更新シナリオ[＃9599](https://github.com/pingcap/tiflash/issues/9599) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)におけるベクトル検索のクエリパフォーマンスの向上
    -   ベクトルインデックス構築中のCPU使用率の監視メトリックを追加[＃9032](https://github.com/pingcap/tiflash/issues/9032) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)
    -   論理演算子[＃9146](https://github.com/pingcap/tiflash/issues/9146) @ [ウィンドトーカー](https://github.com/windtalker)の実行効率を向上させる

-   ツール

    -   バックアップと復元 (BR)

        -   バックアップ中の不要なログ出力を削減[＃55902](https://github.com/pingcap/tidb/issues/55902) @ [リーヴルス](https://github.com/Leavrth)
        -   暗号化キーのエラーメッセージを最適化`--crypter.key` [＃56388](https://github.com/pingcap/tidb/issues/56388) @ [トリスタン1900](https://github.com/Tristan1900)
        -   データベース作成時にBRの同時実行性を高めて、データ復元パフォーマンスを向上します[＃56866](https://github.com/pingcap/tidb/issues/56866) @ [リーヴルス](https://github.com/Leavrth)
        -   バックアップパフォーマンスを向上させるために、フルバックアップ中のテーブルレベルのチェックサム計算をデフォルトで無効にする（ `--checksum=false` ） [＃56373](https://github.com/pingcap/tidb/issues/56373) @ [トリスタン1900](https://github.com/Tristan1900)
        -   各storageノードの接続タイムアウトを独立して追跡およびリセットするメカニズムを追加し、低速ノードの処理を強化して、バックアップ操作がハングするのを防ぎます[＃57666](https://github.com/pingcap/tidb/issues/57666) @ [3ポイントシュート](https://github.com/3pointer)

    -   TiDB データ移行 (DM)

        -   DM クラスターの起動中に DM ワーカーが DM マスターに接続するための再試行を[＃4287](https://github.com/pingcap/tiflow/issues/4287) / [GMHDBJD](https://github.com/GMHDBJD)回追加します。

## バグ修正 {#bug-fixes}

-   ティドブ

    -   PDから返されたリージョンメタデータにLeader情報が欠けている場合にTiDBがリクエストを自動的に再試行せず、実行エラーが発生する可能性がある問題を修正しました[＃56757](https://github.com/pingcap/tidb/issues/56757) @ [cfzjywxk](https://github.com/cfzjywxk)
    -   書き込み競合が発生したときにTTLタスクをキャンセルできない問題を修正[＃56422](https://github.com/pingcap/tidb/issues/56422) @ [ヤンケオ](https://github.com/YangKeao)
    -   TTLタスクをキャンセルした際に、対応するSQLが強制終了されない問題を修正[＃56511](https://github.com/pingcap/tidb/issues/56511) @ [lcwangchao](https://github.com/lcwangchao)
    -   v6.5からv7.5以降にアップグレードされたクラスターで、既存のTTLタスクが予期せず頻繁に実行される問題を修正[＃56539](https://github.com/pingcap/tidb/issues/56539) @ [lcwangchao](https://github.com/lcwangchao)
    -   `INSERT ... ON DUPLICATE KEY`文が`mysql_insert_id` [＃55965](https://github.com/pingcap/tidb/issues/55965) @ [天菜麻緒](https://github.com/tiancaiamao)と互換性がない問題を修正
    -   storageエンジン[＃56402](https://github.com/pingcap/tidb/issues/56402) @ [ヤンケオ](https://github.com/YangKeao)としてTiKVが選択されていない場合にTTLが失敗する可能性がある問題を修正
    -   `IMPORT INTO`ステートメント[＃56476](https://github.com/pingcap/tidb/issues/56476) @ [D3ハンター](https://github.com/D3Hunter)を使用してデータをインポートした後、 `AUTO_INCREMENT`フィールドが正しく設定されない問題を修正しました。
    -   `ADD INDEX` [＃56930](https://github.com/pingcap/tidb/issues/56930) @ [fzzf678](https://github.com/fzzf678)を実行するときに TiDB がインデックスの長さ制限をチェックしない問題を修正しました
    -   `RECOVER TABLE BY JOB JOB_ID;`実行すると TiDB がpanicを起こす可能性がある問題を修正[＃55113](https://github.com/pingcap/tidb/issues/55113) @ [crazycs520](https://github.com/crazycs520)
    -   stale read が読み取り操作のタイムスタンプを厳密に検証しない問題を修正しました。その結果、TSO と実際の物理時間[＃56809](https://github.com/pingcap/tidb/issues/56809) @ [ミョンケミンタ](https://github.com/MyonKeminta)の間にオフセットが存在する場合に、トランザクションの一貫性にわずかながら影響する可能性が生じます。
    -   DDL所有者ノードが[＃56506](https://github.com/pingcap/tidb/issues/56506) @ [接線](https://github.com/tangenta)に切り替えられた後、TiDBが以前の進行状況からReorg DDLタスクを再開できない問題を修正しました。
    -   Distributed eXecution Framework (DXF) の監視パネルの一部のメトリックが不正確であるという問題を修正しました[＃57172](https://github.com/pingcap/tidb/issues/57172) @ [fzzf678](https://github.com/fzzf678) [＃56942](https://github.com/pingcap/tidb/issues/56942) @ [fzzf678](https://github.com/fzzf678)
    -   `REORGANIZE PARTITION`特定のケースでエラー理由を返さない問題を修正[＃56634](https://github.com/pingcap/tidb/issues/56634) @ [ミョンス](https://github.com/mjonss)
    -   大文字と小文字の区別により、 `INFORMATION_SCHEMA.TABLES`クエリで誤った結果が返される問題を修正[＃56987](https://github.com/pingcap/tidb/issues/56987) @ [ジョーチェン](https://github.com/joechenrh)
    -   共通テーブル式 (CTE) に複数のデータ コンシューマーがあり、1 つのコンシューマーがデータを読み取らずに終了した場合に発生する可能性のある無効なメモリアクセスの問題を修正しました[＃55881](https://github.com/pingcap/tidb/issues/55881) @ [ウィンドトーカー](https://github.com/windtalker)
    -   異常終了時に`INDEX_HASH_JOIN`アップする可能性がある問題を修正[＃54055](https://github.com/pingcap/tidb/issues/54055) @ [wshwsh12](https://github.com/wshwsh12)
    -   `NULL`値[＃53546](https://github.com/pingcap/tidb/issues/53546) @ [ツジエモン](https://github.com/tuziemon)を処理するときに`TRUNCATE`ステートメントが誤った結果を返す問題を修正しました
    -   `CAST AS CHAR`関数が型推論エラーにより誤った結果を返す問題を修正[＃56640](https://github.com/pingcap/tidb/issues/56640) @ [ジムララ](https://github.com/zimulala)
    -   型推論エラーにより一部の関数の出力で文字列が切り捨てられる問題を修正[＃56587](https://github.com/pingcap/tidb/issues/56587) @ [ジョーチェン](https://github.com/joechenrh)
    -   `ADDTIME()`と`SUBTIME()`関数の最初の引数が日付型[＃57569](https://github.com/pingcap/tidb/issues/57569) @ [xzhangxian1008](https://github.com/xzhangxian1008)の場合に誤った結果を返す問題を修正しました。
    -   非厳密モードで無効な`NULL`値が挿入される問題を修正 ( `sql_mode = ''` ) [＃56381](https://github.com/pingcap/tidb/issues/56381) @ [ジョーチェン](https://github.com/joechenrh)
    -   `UPDATE`文が`ENUM`型[＃56832](https://github.com/pingcap/tidb/issues/56832) @ [xhebox](https://github.com/xhebox)の値を誤って更新する問題を修正しました
    -   `tidb_low_resolution_tso`変数を有効にすると、 `SELECT FOR UPDATE`ステートメント[＃55468](https://github.com/pingcap/tidb/issues/55468) @ [天菜麻緒](https://github.com/tiancaiamao)の実行中にリソース リークが発生する問題を修正しました。
    -   `JSON_TYPE()`関数がパラメータの型を検証せず、JSON 以外のデータ型が渡されたときにエラーが返されない問題を修正しました[＃54029](https://github.com/pingcap/tidb/issues/54029) @ [ヤンケオ](https://github.com/YangKeao)
    -   `PREPARE`ステートメントで JSON関数を使用すると実行エラーが発生する可能性がある問題を修正しました[＃54044](https://github.com/pingcap/tidb/issues/54044) @ [ヤンケオ](https://github.com/YangKeao)
    -   `BIT`型から`CHAR`型にデータを変換すると TiKV パニック[＃56494](https://github.com/pingcap/tidb/issues/56494) @ [lcwangchao](https://github.com/lcwangchao)が発生する可能性がある問題を修正しました
    -   `CREATE VIEW`ステートメントで変数またはパラメータを使用してもエラーが報告されない問題を修正[＃53176](https://github.com/pingcap/tidb/issues/53176) @ [ミョンス](https://github.com/mjonss)
    -   `JSON_VALID()`関数が誤った結果を返す問題を修正[＃56293](https://github.com/pingcap/tidb/issues/56293) @ [ヤンケオ](https://github.com/YangKeao)
    -   `tidb_ttl_job_enable`変数が無効になった後、TTL タスクがキャンセルされない問題を修正[＃57404](https://github.com/pingcap/tidb/issues/57404) @ [ヤンケオ](https://github.com/YangKeao)
    -   `RANGE COLUMNS`パーティション関数と`utf8mb4_0900_ai_ci`照合順序を同時に使用すると、クエリ結果[＃57261](https://github.com/pingcap/tidb/issues/57261) @ [定義2014](https://github.com/Defined2014)が正しくなくなる可能性がある問題を修正しました。
    -   改行文字で始まるプリペアドステートメントを実行することによって発生する実行時エラーを修正し、配列が範囲外になる問題[定義2014](https://github.com/Defined2014)修正しました[＃54283](https://github.com/pingcap/tidb/issues/54283)
    -   `UTC_TIMESTAMP()`関数の精度の問題を修正しました。精度を高く設定しすぎている[＃56451](https://github.com/pingcap/tidb/issues/56451) @ [チャゲロ](https://github.com/chagelo)
    -   `UPDATE` `INSERT`ステートメント`DELETE IGNORE` @ [ヤンケオ](https://github.com/YangKeao) [＃56678](https://github.com/pingcap/tidb/issues/56678)外部キーエラーが省略されない問題を修正
    -   `information_schema.cluster_slow_query`テーブルをクエリするときに、時間フィルターが追加されていない場合、最新のスローログファイルのみがクエリされる問題を修正しました[＃56100](https://github.com/pingcap/tidb/issues/56100) @ [crazycs520](https://github.com/crazycs520)
    -   TTLテーブル[＃56934](https://github.com/pingcap/tidb/issues/56934) @ [lcwangchao](https://github.com/lcwangchao)のメモリリークの問題を修正
    -   ステータス`write_only`のテーブルでは外部キー制約が有効にならないため、ステータス`non-public`のテーブルを[＃55813](https://github.com/pingcap/tidb/issues/55813) @ [ヤンケオ](https://github.com/YangKeao)で使用できない問題を修正しました。
    -   `NATURAL JOIN`または`USING`節の後にサブクエリを使用するとエラー[＃53766](https://github.com/pingcap/tidb/issues/53766) @ [ダッシュ12653](https://github.com/dash12653)が発生する可能性がある問題を修正しました
    -   CTE に`ORDER BY` 、 `LIMIT` 、または`SELECT DISTINCT`節が含まれており、別の CTE の再帰部分によって参照されている場合、誤ってインライン化され、実行エラー[＃56603](https://github.com/pingcap/tidb/issues/56603) @ [エルサ0520](https://github.com/elsa0520)が発生する可能性がある問題を修正しました。
    -   `VIEW`で定義されたCTEが誤ってインライン化される問題を修正[＃56582](https://github.com/pingcap/tidb/issues/56582) @ [エルサ0520](https://github.com/elsa0520)
    -   外部キー[＃56456](https://github.com/pingcap/tidb/issues/56456) @ [ホーキングレイ](https://github.com/hawkingrei)を含むテーブル構造をインポートするときに Plan Replayer がエラーを報告する可能性がある問題を修正しました。
    -   配置ルール[＃54961](https://github.com/pingcap/tidb/issues/54961) @ [ホーキングレイ](https://github.com/hawkingrei)を含むテーブル構造をインポートするときに Plan Replayer がエラーを報告する可能性がある問題を修正しました。
    -   `ANALYZE`使用してテーブルの統計情報を収集するときに、テーブルに仮想生成列の式インデックスが含まれていると、実行時にエラー[＃57079](https://github.com/pingcap/tidb/issues/57079) @ [ホーキングレイ](https://github.com/hawkingrei)が報告される問題を修正しました。
    -   `DROP DATABASE`文が統計[＃57227](https://github.com/pingcap/tidb/issues/57227) @ [ラスティン170506](https://github.com/Rustin170506)の対応する更新を正しくトリガーしない問題を修正しました
    -   CTE でデータベース名を解析するときに間違ったデータベース名[＃54582](https://github.com/pingcap/tidb/issues/54582) @ [ホーキングレイ](https://github.com/hawkingrei)が返される問題を修正しました
    -   `DUMP STATS`統計を JSON [＃56083](https://github.com/pingcap/tidb/issues/56083) @ [ホーキングレイ](https://github.com/hawkingrei)に変換するときにヒストグラムの上限と下限が壊れる問題を修正
    -   `EXISTS`サブクエリの結果が、さらに代数演算に関係する場合、MySQL [＃56641](https://github.com/pingcap/tidb/issues/56641) @ [ウィンドトーカー](https://github.com/windtalker)の結果と異なる可能性がある問題を修正しました。
    -   エイリアス[＃56726](https://github.com/pingcap/tidb/issues/56726) @ [ホーキングレイ](https://github.com/hawkingrei)を持つマルチテーブル`DELETE`ステートメントに対して実行プラン バインディングを作成できない問題を修正しました。
    -   複雑な述語を単純化する際にオプティマイザが文字セットと照合順序を考慮せず、実行エラーが発生する可能性がある問題を修正しました[＃56479](https://github.com/pingcap/tidb/issues/56479) @ [ダッシュ12653](https://github.com/dash12653)
    -   Grafanaの**Stats Healthy Distribution**パネルのデータが正しくない可能性がある問題を修正しました[＃57176](https://github.com/pingcap/tidb/issues/57176) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   クラスター化インデックス[＃57627](https://github.com/pingcap/tidb/issues/57627) @ [ウィノロス](https://github.com/winoros)を持つテーブルをクエリするときにベクトル検索が誤った結果を返す可能性がある問題を修正しました

-   ティクブ

    -   読み取りスレッドがRaft Engine[＃17383](https://github.com/tikv/tikv/issues/17383) @ [LykxSassinator](https://github.com/LykxSassinator)のMemTable内の古いインデックスにアクセスしたときに発生するpanic問題を修正しました。
    -   多数のトランザクションが同じキーのロック解除待ち行列に入っていて、キーが頻繁に更新される場合、デッドロック検出への過度の圧力によって TiKV OOM 問題[＃17394](https://github.com/tikv/tikv/issues/17394) @ [ミョンケミンタ](https://github.com/MyonKeminta)が発生する可能性がある問題を修正しました
    -   リソース制御のバックグラウンドタスクのCPU使用率が[＃17603](https://github.com/tikv/tikv/issues/17603) @ [栄光](https://github.com/glorv)で2回カウントされる問題を修正
    -   CDC内部タスク[＃17696](https://github.com/tikv/tikv/issues/17696) @ [3エースショーハンド](https://github.com/3AceShowHand)の蓄積によりTiKV OOMが発生する可能性がある問題を修正
    -   `raft-entry-max-size` [＃17701](https://github.com/tikv/tikv/issues/17701) @ [スペードA-タン](https://github.com/SpadeA-Tang)と高く設定されすぎると、大規模なバッチ書き込みによってパフォーマンスジッターが発生する問題を修正しました。
    -   リージョンを[＃17602](https://github.com/tikv/tikv/issues/17602) [LykxSassinator](https://github.com/LykxSassinator)に分割した後、リーダーをすぐに選出できない問題を修正しました
    -   `RADIANS()`または`DEGREES()`関数を含むクエリを実行するとTiKVがpanic可能性がある問題を修正しました[＃17852](https://github.com/tikv/tikv/issues/17852) @ [ゲンリキ](https://github.com/gengliqi)
    -   すべての休止状態の領域が[＃17101](https://github.com/tikv/tikv/issues/17101) @ [hhwyt](https://github.com/hhwyt)で起動すると書き込みジッターが発生する可能性がある問題を修正しました

-   PD

    -   ホットスポット キャッシュ[＃8698](https://github.com/tikv/pd/issues/8698) @ [lhy1024](https://github.com/lhy1024)のメモリリーク問題を修正
    -   リソース グループ セレクターがどのパネル[＃56572](https://github.com/pingcap/tidb/issues/56572) @ [栄光](https://github.com/glorv)でも有効にならない問題を修正しました
    -   削除されたリソース グループが監視パネル[＃8716](https://github.com/tikv/pd/issues/8716) @ [アンドレ・ムーシュ](https://github.com/AndreMouche)に引き続き表示される問題を修正しました
    -   リージョン同期の読み込みプロセス中の不明瞭なログの説明を修正[＃8717](https://github.com/tikv/pd/issues/8717) @ [lhy1024](https://github.com/lhy1024)
    -   ラベル統計[＃8700](https://github.com/tikv/pd/issues/8700) @ [lhy1024](https://github.com/lhy1024)のメモリリーク問題を修正
    -   `tidb_enable_tso_follower_proxy`から`0`または`OFF`を設定しても TSOFollowerプロキシ機能[＃8709](https://github.com/tikv/pd/issues/8709) @ [Jmポテト](https://github.com/JmPotato)を無効にできない問題を修正しました

-   TiFlash

    -   `SUBSTRING()`関数が特定の整数型に対して`pos`と`len`引数をサポートせず、クエリエラー[＃9473](https://github.com/pingcap/tiflash/issues/9473) @ [ゲンリキ](https://github.com/gengliqi)が発生する問題を修正しました
    -   分散storageおよびコンピューティングアーキテクチャ[＃9637](https://github.com/pingcap/tiflash/issues/9637) @ [コラフィッシュ](https://github.com/kolafish)でTiFlash書き込みノードをスケールアウトした後にベクトル検索のパフォーマンスが低下する可能性がある問題を修正しました。
    -   2番目のパラメータが負の[＃9604](https://github.com/pingcap/tiflash/issues/9604) @ [グオシャオゲ](https://github.com/guo-shaoge)の場合に`SUBSTRING()`関数が誤った結果を返す問題を修正しました
    -   最初のパラメータが定数[＃9522](https://github.com/pingcap/tiflash/issues/9522) @ [グオシャオゲ](https://github.com/guo-shaoge)の場合に`REPLACE()`関数がエラーを返す問題を修正しました
    -   `LPAD()`と`RPAD()`関数が、場合によっては誤った結果を返す問題を修正しました[＃9465](https://github.com/pingcap/tiflash/issues/9465) @ [グオシャオゲ](https://github.com/guo-shaoge)
    -   ベクトルインデックスを作成した後、ベクトルインデックスを構築する内部タスクが予期せず中断されると、 TiFlash が破損したデータを書き込み、 [＃9714](https://github.com/pingcap/tiflash/issues/9714) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)を再起動できなくなる可能性がある問題を修正しました。

-   ツール

    -   バックアップと復元 (BR)

        -   未完了の範囲ギャップが多すぎる場合のバックアップ中の OOM 問題を修正し、事前割り当てメモリの量を減らします[＃53529](https://github.com/pingcap/tidb/issues/53529) @ [リーヴルス](https://github.com/Leavrth)
        -   グローバルインデックスをバックアップできない問題を修正[＃57469](https://github.com/pingcap/tidb/issues/57469) @ [定義2014](https://github.com/Defined2014)
        -   ログに暗号化された情報[＃57585](https://github.com/pingcap/tidb/issues/57585) @ [ケニーtm](https://github.com/kennytm)が出力される問題を修正
        -   アドバンサーがロック競合[＃57134](https://github.com/pingcap/tidb/issues/57134) @ [3ポイントシュート](https://github.com/3pointer)を処理できない問題を修正
        -   `k8s.io/api`ライブラリバージョン[＃57790](https://github.com/pingcap/tidb/issues/57790) @ [生まれ変わった人](https://github.com/BornChanger)にアップグレードして潜在的なセキュリティ脆弱性を修正します
        -   クラスター内に多数のテーブルがあるが、実際のデータサイズが小さい場合に PITR タスクが`Information schema is out of date`エラーを返す可能性がある問題を修正しました[＃57743](https://github.com/pingcap/tidb/issues/57743) @ [トリスタン1900](https://github.com/Tristan1900)
        -   アドバンサー所有者が[＃58031](https://github.com/pingcap/tidb/issues/58031) @ [3ポイントシュート](https://github.com/3pointer)に切り替わったときに、ログバックアップが予期せず一時停止状態になる可能性がある問題を修正しました。
        -   `tiup br restore`コマンドがデータベースまたはテーブルの復元中にターゲット クラスタ テーブルが既に存在するかどうかのチェックを省略し、既存のテーブル[＃58168](https://github.com/pingcap/tidb/issues/58168) @ [リドリスR](https://github.com/RidRisR)を上書きする可能性がある問題を修正しました。

    -   TiCDC

        -   Debezium プロトコル[＃1799](https://github.com/pingcap/tiflow/issues/1799) @ [wk989898](https://github.com/wk989898)を使用するときに Kafka メッセージにキーフィールドが不足する問題を修正しました
        -   やり直しモジュールがエラー[＃11744](https://github.com/pingcap/tiflow/issues/11744) @ [チャールズ・チャン96](https://github.com/CharlesCheung96)を正しく報告できない問題を修正しました
        -   TiDB DDL 所有者の変更中に DDL タスクのスキーマ バージョンが非増分になったときに、TiCDC が誤って DDL タスクを破棄する問題を修正[＃11714](https://github.com/pingcap/tiflow/issues/11714) @ [wlwilliamx](https://github.com/wlwilliamx)

    -   TiDB Lightning

        -   TiDB LightningがTiKV [＃56114](https://github.com/pingcap/tidb/issues/56114) @ [フィシュウ](https://github.com/fishiu)から送信されたサイズ超過のメッセージを受信できない問題を修正しました
        -   物理インポートモード[＃56814](https://github.com/pingcap/tidb/issues/56814) @ [D3ハンター](https://github.com/D3Hunter)を使用してデータをインポートした後に`AUTO_INCREMENT`値が高すぎる値に設定される問題を修正しました

## パフォーマンステスト {#performance-test}

TiDB v8.5.0 のパフォーマンスについて詳しくは、 TiDB Cloud Dedicated クラスターの[パフォーマンステストレポート](https://docs.pingcap.com/tidbcloud/v8.5-performance-highlights)を参照してください。

## 寄稿者 {#contributors}

TiDB コミュニティの以下の貢献者に感謝いたします。

-   [ダッシュ12653](https://github.com/dash12653) (初回投稿者)
-   [チャゲロ](https://github.com/chagelo) (初回投稿者)
-   [リンダサマー](https://github.com/LindaSummer)
-   [ソンジビン97](https://github.com/songzhibin97)
-   [ヘキシリー](https://github.com/Hexilee)
