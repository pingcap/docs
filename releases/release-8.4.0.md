---
title: TiDB 8.4.0 Release Notes
summary: TiDB 8.4.0 の新機能、互換性の変更点、改善点、およびバグ修正についてご確認ください。
---

# TiDB 8.4.0 リリースノート {#tidb-8-4-0-release-notes}

発売日：2024年11月11日

TiDB バージョン: 8.4.0

クイックアクセス: [クイックスタート](https://docs-archive.pingcap.com/tidb/v8.4/quick-start-with-tidb)

バージョン8.4.0では、以下の主要な機能と改善点が導入されています。

<table><thead><tr><th>カテゴリ</th><th>機能／改善点</th><th>説明</th></tr></thead><tbody><tr><td rowspan="4">拡張性とパフォーマンス</td><td><a href="https://docs-archive.pingcap.com/tidb/v8.4/system-variables#tidb_enable_instance_plan_cache-new-in-v840">インスタンスレベルの実行プランキャッシュ</a>（実験的）</td><td>インスタンスレベルのプランキャッシュを使用すると、同じ TiDB インスタンス内のすべてのセッションでプランキャッシュを共有できます。セッションレベルのプランキャッシュと比較して、この機能はメモリに多くの実行プランをキャッシュすることで SQL コンパイル時間を短縮し、SQL 全体の実行時間を短縮します。これにより、OLTP のパフォーマンスとスループットが向上するとともに、メモリ使用量をより適切に制御し、データベースの安定性を高めることができます。</td></tr><tr><td><a href="https://docs-archive.pingcap.com/tidb/v8.4/partitioned-table#global-indexes">パーティションテーブルのグローバルインデックス</a>（GA）</td><td>グローバルインデックスを使用すると、パーティション化されていない列の取得効率を効果的に向上させることができ、一意キーにパーティションキーを含める必要があるという制約を取り除くことができます。この機能により、TiDBパーティションテーブルの使用シナリオが拡張され、データ移行に必要なアプリケーションの変更作業の一部が不要になります。</td></tr><tr><td> <a href="https://docs-archive.pingcap.com/tidb/v8.4/system-variables#tidb_tso_client_rpc_mode-new-in-v840">TSOリクエストの並列モード</a></td><td>高並行処理環境では、この機能を使用することでTSOの取得待ち時間を短縮し、クラスタのスループットを向上させることができます。</td></tr><tr><td><a href="https://docs-archive.pingcap.com/tidb/v8.4/cached-tables">キャッシュされたテーブル</a>のクエリパフォーマンスを向上させる</td><td>キャッシュされたテーブルに対するインデックススキャンのクエリパフォーマンスが向上し、場合によっては最大5.4倍の改善が見られます。小規模なテーブルに対する高速クエリの場合、キャッシュされたテーブルを使用することで、全体的なパフォーマンスを大幅に向上させることができます。</td></tr><tr><td rowspan="4">信頼性と可用性</td><td> <a href="https://docs-archive.pingcap.com/tidb/v8.4/tidb-resource-control#query_limit-parameters">暴走クエリに対するトリガーの追加と、リソースグループの切り替えのサポート</a></td><td>暴走クエリは、予期しないSQLパフォーマンスの問題がシステムに与える影響を軽減する効果的な手段です。TiDB v8.4.0では、識別条件としてコプロセッサーによって処理されたキーの数（ <code>PROCESSED_KEYS</code> ）とリクエストユニット（ <code>RU</code> ）が導入され、識別されたクエリを指定されたリソースグループに配置することで、暴走クエリのより正確な識別と制御が可能になりました。</td></tr><tr><td><a href="https://docs-archive.pingcap.com/tidb/v8.4/tidb-resource-control#background-parameters">リソース制御のバックグラウンドタスクにおけるリソース使用量の上限設定をサポートする</a></td><td>リソース制御のバックグラウンドタスクに最大パーセンテージ制限を設定することで、さまざまなアプリケーションシステムのニーズに基づいてリソース消費を制御できます。これにより、バックグラウンドタスクの消費量を低く抑え、オンラインサービスの品質を確保できます。</td></tr><tr><td> <a href="https://docs-archive.pingcap.com/tidb/v8.4/tiproxy-traffic-replay">TiProxyはトラフィックのキャプチャと再生をサポートします</a>（実験的）。</td><td> TiProxyを使用して、クラスターのアップグレード、移行、デプロイメントの変更などの主要な操作を行う前に、TiDB本番クラスターから実際のワークロードをキャプチャします。これらのワークロードをターゲットのテストクラスターで再生することで、パフォーマンスを検証し、変更が確実に成功することを確認します。</td></tr><tr><td> <a href="https://docs-archive.pingcap.com/tidb/v8.4/system-variables#tidb_auto_analyze_concurrency-new-in-v840">同時自動統計収集</a></td><td>TiDBクラスタ内での同時実行自動分析操作の数を制御するために、システム変数<code>tidb_auto_analyze_concurrency</code>を導入します。TiDBは、ノードの規模とハードウェア仕様に基づいて、スキャンタスクの同時実行数を自動的に決定します。これにより、システムリソースを最大限に活用して統計情報の収集効率が向上し、手動による調整が削減され、クラスタの安定したパフォーマンスが確保されます。</td></tr><tr><td rowspan="1"> SQL</td><td><a href="https://docs.pingcap.com/ai/vector-search-overview">ベクトル検索</a>（実験的）</td><td>ベクトル検索は、データの意味論に基づいた検索手法であり、より関連性の高い検索結果を提供します。AIや大規模言語モデル（LLM）の中核関数の一つとして、ベクトル検索は、検索拡張生成（RAG）、意味検索、推薦システムなど、さまざまなシナリオで活用できます。</td></tr><tr><td rowspan="3">データベースの運用と可観測性</td><td><a href="https://docs-archive.pingcap.com/tidb/v8.4/information-schema-processlist">TiKVとTiDBのCPU時間をメモリテーブルに表示する</a></td><td>CPU時間はシステムテーブルに統合され、セッションやSQLなどの他のメトリックと並べて表示されるようになりました。これにより、CPU使用率の高い操作を複数の視点から把握し、診断効率を向上させることができます。これは、インスタンスにおけるCPUスパイクやクラスタにおける読み書きホットスポットなどのシナリオを診断する際に特に役立ちます。</td></tr><tr><td><a href="https://docs-archive.pingcap.com/tidb/v8.4/top-sql#use-top-sql">テーブルまたはデータベースごとに集計されたTiKV CPU時間を表示する機能をサポートします。</a></td><td>ホットスポットの問題が個々のSQL文によって引き起こされていない場合、 Top SQLでテーブルまたはデータベースレベルごとに集計されたCPU時間を使用することで、ホットスポットの原因となっているテーブルやアプリケーションを迅速に特定でき、ホットスポットやCPU消費の問題の診断効率を大幅に向上させることができます。</td></tr><tr><td> <a href="https://docs-archive.pingcap.com/tidb/v8.4/backup-and-restore-storages#authentication">IMDSv2サービスが有効になっているTiKVインスタンスのバックアップをサポートします。</a></td><td> <a href="https://aws.amazon.com/cn/blogs/security/get-the-full-benefits-of-imdsv2-and-disable-imdsv1-across-your-aws-infrastructure/">AWS EC2 では、デフォルトのメタデータ サービスとして IMDSv2 が使用されるようになりました</a>。TiDB は、IMDSv2 が有効になっている TiKV インスタンスからのデータバックアップをサポートしており、パブリック クラウド サービスで TiDB クラスターをより効率的に実行するのに役立ちます。</td></tr><tr><td rowspan="1">Security</td><td><a href="https://docs-archive.pingcap.com/tidb/v8.4/br-pitr-manual#encrypt-log-backup-data">ログバックアップデータのクライアント側暗号化</a>（実験的）</td><td>ログバックアップデータをバックアップストレージにアップロードする前に、バックアップデータを暗号化することで、storage中および転送中のセキュリティを確保できます。</td></tr></tbody></table>

## 機能の詳細 {#feature-details}

### パフォーマンス {#performance}

-   TSOリクエストに並列バッチモードを導入し、TSO取得のレイテンシーを削減する[#54960](https://github.com/pingcap/tidb/issues/54960) [#8432](https://github.com/tikv/pd/issues/8432) @[MyonKeminta](https://github.com/MyonKeminta)

    バージョン8.4.0より前では、TiDBはPDから[TSO](/tso.md)要求する際に、特定の期間に複数のTSO要求を収集し、それらをバッチ処理で順次処理することで、リモートプロシージャコール（RPC）要求の数を減らし、PDのワークロードを軽減していました。しかし、レイテンシに敏感なシナリオでは、この逐次バッチ処理モードのパフォーマンスは理想的ではありませんでした。

    TiDB v8.4.0では、異なる同時実行能力を持つTSOリクエスト用の並列バッチモードが導入されました。並列モードはTSO取得のレイテンシーを短縮しますが、PDのワークロードが増加する可能性があります。TSO取得に並列RPCモードを設定するには、 [`tidb_tso_client_rpc_mode`](/system-variables.md#tidb_tso_client_rpc_mode-new-in-v840)システム変数を構成してください。

    詳細については、 [ドキュメント](/system-variables.md#tidb_tso_client_rpc_mode-new-in-v840)を参照してください。

-   TiDB のハッシュ結合演算子の実行効率を最適化する (実験的) [#55153](https://github.com/pingcap/tidb/issues/55153) [#53127](https://github.com/pingcap/tidb/issues/53127) @[windtalker](https://github.com/windtalker)@[xzhangxian1008](https://github.com/xzhangxian1008) @[XuHuaiyu](https://github.com/XuHuaiyu)@[wshwsh12](https://github.com/wshwsh12)

    TiDB v8.4.0では、ハッシュ結合演算子の最適化バージョンが導入され、実行効率が向上しました。現在、最適化バージョンのハッシュ結合は内部結合と外部結合操作にのみ適用され、デフォルトでは無効になっています。この最適化バージョンを有効にするには、 [`tidb_hash_join_version`](/system-variables.md#tidb_hash_join_version-new-in-v840)システム変数を`optimized`に設定してください。

    詳細については、 [ドキュメント](/system-variables.md#tidb_hash_join_version-new-in-v840)を参照してください。

-   TiKVへの以下の日付関数のプッシュダウンをサポート[#56297](https://github.com/pingcap/tidb/issues/56297) [#17529](https://github.com/tikv/tikv/issues/17529) @[gengliqi](https://github.com/gengliqi)

    -   `DATE_ADD()`
    -   `DATE_SUB()`
    -   `ADDDATE()`
    -   `SUBDATE()`

    詳細については、 [ドキュメント](/functions-and-operators/expressions-pushed-down.md)を参照してください。

-   インスタンスレベルの実行プランキャッシュのサポート（実験的） [#54057](https://github.com/pingcap/tidb/issues/54057) @[qw4990](https://github.com/qw4990)

    インスタンスレベルの実行プランキャッシュを使用すると、同じ TiDB インスタンス内のすべてのセッションで実行プランキャッシュを共有できます。この機能により、TiDB クエリの応答時間が大幅に短縮され、クラスタのスループットが向上し、実行プランの変更の可能性が低減され、クラスタのパフォーマンスが安定します。セッションレベルの実行プランキャッシュと比較して、インスタンスレベルの実行プランキャッシュには次の利点があります。

    -   冗長性を排除し、同じメモリ消費量でより多くの実行プランをキャッシュします。
    -   インスタンスに固定サイズのメモリを割り当て、メモリ使用量をより効果的に制限します。

    v8.4.0 では、インスタンス レベルの実行プラン キャッシュはクエリ実行プランのキャッシュのみをサポートしており、デフォルトでは無効になっています。 [`tidb_enable_instance_plan_cache`](/system-variables.md#tidb_enable_instance_plan_cache-new-in-v840)を使用してこの機能を有効にし、 [`tidb_instance_plan_cache_max_size`](/system-variables.md#tidb_instance_plan_cache_max_size-new-in-v840)を使用して最大メモリ使用量を設定できます。この機能を有効にする前に、[プリペアドプランキャッシュ](/sql-prepared-plan-cache.md)と[非プリペアドプランキャッシュ](/sql-non-prepared-plan-cache.md)を無効にしてください。

    詳細については、 [ドキュメント](/system-variables.md#tidb_enable_instance_plan_cache-new-in-v840)を参照してください。

-   TiDB Lightningの論理インポートモードは、プリペアドステートメントとクライアントステートメントキャッシュをサポートします [#54850](https://github.com/pingcap/tidb/issues/54850) @[dbsid](https://github.com/dbsid)

    `logical-import-prep-stmt`設定項目を有効にすると、TiDB Lightning の論理インポートモードで実行される SQL ステートメントは、プリペアド ステートメントとクライアント ステートメント キャッシュを使用します。これにより、 TiDB SQLの解析とコンパイルのコストが削減され、SQL の実行効率が向上し、実行プラン キャッシュへのアクセス確率が高まるため、論理インポートが高速化されます。

    詳細については、 [ドキュメント](/tidb-lightning/tidb-lightning-configuration.md)を参照してください。

-   パーティション テーブルはグローバル インデックスをサポート (GA) [#45133](https://github.com/pingcap/tidb/issues/45133) @[mjonss](https://github.com/mjonss)@[Defined2014](https://github.com/Defined2014) @[jiyfhust](https://github.com/jiyfhust)@[L-maple](https://github.com/L-maple)

    TiDBの初期バージョンでは、パーティションテーブルはグローバルインデックスをサポートしていないため、いくつかの制限がありました。たとえば、一意キーはテーブルのパーティション式内のすべての列を使用する必要があります。クエリ条件でパーティションキーを使用しない場合、クエリはすべてのパーティションをスキャンするため、パフォーマンスが低下します。v7.6.0以降では、グローバルインデックス機能を有効にするためにシステム変数[`tidb_enable_global_index`](/system-variables.md#tidb_enable_global_index-new-in-v760)が導入されました。しかし、この機能は当時開発中であったため、有効にすることは推奨されません。

    バージョン8.3.0以降、グローバルインデックス機能は実験的機能としてリリースされました。 `GLOBAL`キーワードを使用すると、パーティションテーブルのグローバルインデックスを明示的に作成できます。これにより、パーティションテーブルの一意キーにパーティション式で使用されるすべての列を含める必要があるという制約がなくなり、より柔軟なアプリケーション要件に対応できるようになります。さらに、グローバルインデックスは、パーティション化されていない列に基づくクエリのパフォーマンスも向上させます。

    バージョン 8.4.0 では、この機能が一般提供 (GA) になります。グローバル インデックス機能を有効にするためにシステム変数[`tidb_enable_global_index`](/system-variables.md#tidb_enable_global_index-new-in-v760)を設定する代わりに、キーワード`GLOBAL`を使用してグローバル インデックスを作成できます。バージョン 8.4.0 以降、このシステム変数は非推奨となり、常に`ON`になります。

    詳細については、[ドキュメント](/global-indexes.md)を参照してください。

-   一部のシナリオでキャッシュされたテーブルのクエリパフォーマンスを改善 [#43249](https://github.com/pingcap/tidb/issues/43249) @[tiancaiamao](https://github.com/tiancaiamao)

    バージョン8.4.0では、TiDBは`SELECT ... LIMIT 1` `IndexLookup`と共に実行する際に、キャッシュされたテーブルのクエリパフォーマンスを最大5.4倍向上させます。さらに、TiDBはフルテーブルスキャンと主キークエリのシナリオにおいて、 `IndexLookupReader`のパフォーマンスを向上させます。

### 信頼性 {#reliability}

-   暴走クエリは、処理されたキーとリクエストユニットの数をしきい値としてサポートします [#54434](https://github.com/pingcap/tidb/issues/54434) @[HuSharp](https://github.com/HuSharp)

    バージョン8.4.0以降、TiDBは処理されたキーの数（ `PROCESSED_KEYS` ）とリクエストユニットの数（ `RU` ）に基づいて、暴走クエリを識別できるようになりました。実行時間（ `EXEC_ELAPSED` ）と比較すると、これらの新しいしきい値はクエリのリソース消費をより正確に定義し、全体的なパフォーマンスが低下した際の識別バイアスを回避します。

    複数の条件を同時に設定することができ、いずれかの条件が満たされた場合、そのクエリは暴走クエリとして識別されます。

    履歴実行に基づいて条件値を決定するには、 概要表で対応するフィールド（ `RESOURCE_GROUP` `MAX_REQUEST_UNIT_WRITE` `MAX_REQUEST_UNIT_READ` 、 `MAX_PROCESSED_KEYS` ）[ステートメントサマリーテーブル](/statement-summary-tables.md)を確認できます。

    詳細については、 [ドキュメント](/tidb-resource-control-runaway-queries.md)を参照してください。

-   暴走クエリに対するリソースグループの切り替えのサポート [#54434](https://github.com/pingcap/tidb/issues/54434) @[JmPotato](https://github.com/JmPotato)

    TiDB v8.4.0以降では、暴走クエリのリソースグループを特定のリソースグループに切り替えることができます。 `COOLDOWN`メカニズムでリソース消費量を削減できない場合は、 [リソースグループ](/tidb-resource-control-ru-groups.md#create-a-resource-group)を作成し、そのリソースサイズを制限し、 `SWITCH_GROUP`パラメータを設定して、識別された暴走クエリをこのグループに移動できます。一方、同じセッション内の後続のクエリは、元のリソースグループで引き続き実行されます。リソースグループを切り替えることで、リソース使用状況をより正確に管理し、リソース消費量をより厳密に制御できます。

    詳細については、 [ドキュメント](/tidb-resource-control-runaway-queries.md#query_limit-parameters)を参照してください。

-   `tidb_scatter_region` システム変数を使用してクラスターレベルのリージョン散乱戦略を設定することをサポートします [#55184](https://github.com/pingcap/tidb/issues/55184) @[D3Hunter](https://github.com/D3Hunter)

    バージョン8.4.0より前では、 `tidb_scatter_region`システム変数は有効化または無効化のみが可能でした。有効化すると、TiDBはバッチテーブル作成時にテーブルレベルの分散戦略を適用します。しかし、バッチで数十万ものテーブルを作成する場合、この戦略によってリージョンが少数のTiKVノードに集中し、それらのノードでOOM（メモリ不足）の問題が発生します。

    バージョン8.4.0以降、 `tidb_scatter_region`は文字列型に変更されました。これにより、クラスタレベルの分散戦略がサポートされ、前述のシナリオにおけるTiKVのメモリ不足問題​​を回避するのに役立ちます。

    詳細については、[ドキュメント](/system-variables.md#tidb_scatter_region)を参照してください。

-   リソース制御のバックグラウンドタスクにおけるリソース使用量の上限設定をサポートする [#56019](https://github.com/pingcap/tidb/issues/56019) @[glorv](https://github.com/glorv)

    TiDBのリソース制御機能を使用すると、バックグラウンドタスクを識別して優先度を下げることができます。特定のシナリオでは、リソースが利用可能な場合でも、バックグラウンドタスクのリソース消費を制限したい場合があります。v8.4.0以降では、 `UTILIZATION_LIMIT`パラメータを使用して、バックグラウンドタスクが消費できるリソースの最大割合を設定できます。各ノードは、すべてのバックグラウンドタスクのリソース使用量をこの割合以下に抑えます。この機能により、バックグラウンドタスクのリソース消費を正確に制御できるため、クラスタの安定性がさらに向上します。

    詳細については、 [ドキュメント](/tidb-resource-control-background-tasks.md)を参照してください。

-   リソースグループのリソース割り当て戦略を最適化する [#50831](https://github.com/pingcap/tidb/issues/50831) @[nolouch](https://github.com/nolouch)

    TiDBはバージョン8.4.0でリソース割り当て戦略を改善し、リソース管理に関するユーザーの期待にさらに応えられるようにしました。

    -   実行時に大規模クエリのリソース割り当てを制御してリソースグループの制限を超えないようにし、暴走クエリ`COOLDOWN`と組み合わせることで、大規模クエリの同時実行を特定して削減し、瞬間的なリソース消費を削減できます。
    -   デフォルトの優先度スケジューリング戦略を調整します。優先度の異なるタスクが同時に実行される場合、優先度の高いタスクにより多くのリソースが割り当てられます。

### 可用性 {#availability}

-   TiProxyがトラフィック再生をサポート（実験的） [#642](https://github.com/pingcap/tiproxy/issues/642) @[djshow832](https://github.com/djshow832)

    TiProxy v1.3.0以降では、 `tiproxyctl`を使用してTiProxyインスタンスに接続し、TiDB本番クラスタのアクセストラフィックをキャプチャして、指定したレートでテストクラスタに再生できます。この機能により、本番クラスタの実際のワークロードをテスト環境で再現し、SQLステートメントの実行結果とパフォーマンスを検証できます。

    交通状況のリプレイは、次のような状況で役立ちます。

    -   TiDBのバージョンアップグレードを確認する
    -   変更の影響を評価する
    -   TiDBを拡張する前にパフォーマンスを検証する
    -   試験性能限界

    詳細については、[ドキュメント](/tiproxy/tiproxy-traffic-replay.md)を参照してください。

### SQL {#sql}

-   ベクトル検索のサポート (実験的) [#54245](https://github.com/pingcap/tidb/issues/54245) [#17290](https://github.com/tikv/tikv/issues/17290) [#9032](https://github.com/pingcap/tiflash/issues/9032) @[breezewish](https://github.com/breezewish)@[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)@[zimulala](https://github.com/zimulala)@ [EricZequan](https://github.com/EricZequan)@[JaySon-Huang](https://github.com/JaySon-Huang)@[winoros](https://github.com/winoros)@[wk989898](https://github.com/wk989898)

    ベクトル検索は、データの意味論に基づいた検索手法であり、より関連性の高い検索結果を提供します。AIや大規模言語モデル（LLM）の中核関数の一つとして、ベクトル検索は、検索拡張生成（RAG）、意味検索、推薦システムなど、さまざまなシナリオで活用できます。

    v8.4.0 以降、TiDB は [ベクトルデータ型](/ai/reference/vector-search-data-types.md)と[ベクトル検索インデックス](/ai/reference/vector-search-index.md)をサポートし、強力なベクトル検索機能を提供します。 TiDB ベクトル データ タイプは、最大 16,383 次元をサポートし、L2 距離 (ユークリッド距離)、コサイン距離、負の内積、L1 距離 (マンハッタン距離) を含むさまざまな[距離関数](/ai/reference/vector-search-functions-and-operators.md#vector-functions)をサポートします。

    ベクトル検索を開始するには、ベクトルデータ型のテーブルを作成し、ベクトルデータを挿入し、ベクトルデータに対するクエリを実行するだけで済みます。ベクトルデータと従来の関係データを組み合わせたクエリを実行することも可能です。

    ベクトル検索のパフォーマンスを向上させるために、[ベクトル検索インデックス](/ai/reference/vector-search-index.md)を作成して使用できます。 TiDB ベクトル検索インデックスはTiFlashに依存していることに注意してください。ベクトル検索インデックスを使用する前に、 TiFlashノードが TiDB クラスターにデプロイされていることを確認してください。

    詳細については、[ドキュメント](/ai/concepts/vector-search-overview.md)を参照してください。

### データベース操作 {#db-operations}

-   BRはログ バックアップ データのクライアント側暗号化をサポートします (実験的) [#55834](https://github.com/pingcap/tidb/issues/55834) @[Tristan1900](https://github.com/Tristan1900)

    以前のTiDBバージョンでは、スナップショットバックアップデータのみがクライアント側で暗号化されていました。v8.4.0以降では、ログバックアップデータもクライアント側で暗号化できるようになりました。ログバックアップデータをバックアップストレージにアップロードする前に、以下のいずれかの方法でバックアップデータを暗号化してセキュリティを確保できます。

    -   カスタム固定キーを使用して暗号化する
    -   ローカルディスクに保存されているマスターキーを使用して暗号化します。
    -   キー管理サービス（KMS）によって管理されるマスターキーを使用して暗号化します。

    詳細については、 [ドキュメント](/br/br-pitr-manual.md#encrypt-the-log-backup-data)を参照してください。

-   BRはクラウドストレージシステムでバックアップデータを復元する際に、より少ない権限しか必要としない [#55870](https://github.com/pingcap/tidb/issues/55870) @[Leavrth](https://github.com/Leavrth)

    バージョン8.4.0より前は、 BRはリストア中にリストアの進行状況に関するチェックポイント情報をバックアップストレージシステムに書き込みます。これらのチェックポイントにより、中断されたリストアを迅速に再開できます。バージョン8.4.0以降では、 BRはリストアチェックポイント情報をターゲットのTiDBクラスタに書き込みます。つまり、 BRはリストア中にバックアップディレクトリへの読み取りアクセスのみを必要とします。

    詳細については、 [ドキュメント](/br/backup-and-restore-storages.md#authentication)を参照してください。

### 可観測性 {#observability}

-   TiDBとTiKVが消費したCPU時間をシステムテーブルに表示する [#55542](https://github.com/pingcap/tidb/issues/55542) @[yibin87](https://github.com/yibin87)

    [TiDB Dashboard](/dashboard/dashboard-intro.md)の[Top SQLページ](/dashboard/top-sql.md)CPU 使用率の高い SQL ステートメントを表示します。バージョン 8.4.0 以降、TiDB はシステム テーブルに CPU 使用時間情報を追加し、セッションや SQL の他のメトリックと並べて表示することで、CPU 使用率の高い操作をさまざまな視点から簡単に把握できるようにしました。この情報は、インスタンスの CPU スパイクやクラスタ内の読み書きホットスポットなどのシナリオで、問題の原因を迅速に特定するのに役立ちます。

    -   [ステートメントサマリーテーブル](/statement-summary-tables.md)には`AVG_TIDB_CPU_TIME`と`AVG_TIKV_CPU_TIME`が追加され、過去の個々の SQL ステートメントによって消費された平均 CPU 時間が表示されます。
    -   [情報スキーマ.プロセスリスト](/information-schema/information-schema-processlist.md)テーブルには、 `TIDB_CPU`と`TIKV_CPU`が追加され、現在セッションで実行されている SQL ステートメントの累積 CPU 消費量が表示されます。
    -   [スロークエリログ](/analyze-slow-queries.md)には`Tidb_cpu_time`フィールドと`Tikv_cpu_time`フィールドが追加され、キャプチャされた SQL ステートメントによって消費された CPU 時間が表示されます。

    デフォルトでは、TiKV が消費する CPU 時間が表示されます。TiDB が消費する CPU 時間を収集すると追加のオーバーヘッド (約 8%) が発生するため、TiDB が消費する CPU 時間は、 [Top SQL](/dashboard/top-sql.md)が有効になっている場合にのみ実際の値が表示されます。それ以外の場合は、常に`0`と表示されます。

    詳細については、 [`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md)および[`INFORMATION_SCHEMA.SLOW_QUERY`](/information-schema/information-schema-slow-query.md)を参照してください。

-   Top SQLは、テーブルまたはデータベースごとに集計されたCPU時間結果を表示する機能をサポートしています [#55540](https://github.com/pingcap/tidb/issues/55540) @[nolouch](https://github.com/nolouch)

    バージョン8.4.0より前は、 [Top SQL](/dashboard/top-sql.md) SQLごとにCPU時間を集計していました。CPU時間が少数のSQL文によって消費されていない場合、SQLによる集計では問題を効果的に特定できませんでした。バージョン8.4.0以降では、CPU時間を**テーブル**別または**データベース**別に集計できるようになりました。複数のシステムが存在するシナリオでは、この新しい集計方法により、特定のシステムからの負荷変動をより効果的に特定でき、診断効率が向上します。

    詳細については、[ドキュメント](/dashboard/top-sql.md#use-top-sql)を参照してください。

### セキュリティ {#security}

-   BRはAWS IMDSv2をサポートしています [#16443](https://github.com/tikv/tikv/issues/16443) @[pingyu](https://github.com/pingyu)

    TiDBをAmazon EC2にデプロイする場合、 BRはAWSインスタンスメタデータサービスバージョン2（IMDSv2）をサポートします。EC2インスタンスを設定することで、 BRがインスタンスに関連付けられたIAMロールを使用してAmazon S3にアクセスするための適切な権限を取得できます。

    詳細については、 [ドキュメント](/br/backup-and-restore-storages.md#authentication)を参照してください。

### データ移行 {#data-migration}

-   TiCDC Claim-Check は、Kafka メッセージの`value`フィールドの外部ストレージへの送信のみをサポートします [#11396](https://github.com/pingcap/tiflow/issues/11396) @[3AceShowHand](https://github.com/3AceShowHand)

    バージョン 8.4.0 より前では、クレームチェック機能が有効になっている場合 ( `large-message-handle-option`を`claim-check`に設定した場合)、TiCDC は大きなメッセージを処理する際に、 `key`と`value`フィールドの両方をエンコードして外部ストレージシステムに保存します。

    バージョン8.4.0以降、TiCDCはKafkaメッセージの`value`フィールドのみを外部ストレージに送信する機能をサポートしています。この機能は、Open Protocol以外のプロトコルにのみ適用されます。 `claim-check-raw-value`パラメータを設定することで、この機能を制御できます。

    詳細については、 [ドキュメント](/ticdc/ticdc-sink-to-kafka.md#send-the-value-field-to-external-storage-only)を参照してください。

-   TiCDC は、更新または削除イベントで古い値を検証するための Checksum V2 を導入 [#10969](https://github.com/pingcap/tiflow/issues/10969) @[3AceShowHand](https://github.com/3AceShowHand)

    バージョン 8.4.0 以降、TiDB と TiCDC は`ADD COLUMN`または`DROP COLUMN`操作後の Update イベントまたは Delete イベントで古い値を検証する際の Checksum V1 の問題に対処するため、Checksum V2 アルゴリズムを導入しました。バージョン 8.4.0 以降で作成されたクラスタ、またはバージョン 8.4.0 にアップグレードされたクラスタでは、単一行データのチェックサム検証が有効になっている場合、TiDB はデフォルトで Checksum V2 を使用します。TiCDC は Checksum V1 と V2 の両方の処理をサポートしています。この変更は TiDB と TiCDC の内部実装にのみ影響し、下流の Kafka コンシューマーのチェックサム計算方法には影響しません。

    詳細については、[ドキュメント](/ticdc/ticdc-integrity-check.md)を参照してください。

## 互換性の変更 {#compatibility-changes}

> **Note:**
>
> このセクションでは、v8.3.0 から最新バージョン (v8.4.0) にアップグレードする際に知っておくべき互換性の変更点について説明します。v8.2.0 以前のバージョンから最新バージョンにアップグレードする場合は、中間バージョンで導入された互換性の変更点も確認する必要があるかもしれません。

### システム変数 {#system-variables}

| 変数名                                                                                                                             | 変更の種類  | 説明                                                                                                                                                                                                                                                                                           |
| ------------------------------------------------------------------------------------------------------------------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `log_bin`                                                                                                                       | 削除済み     | バージョン8.4.0では、 [TiDB Binlog](https://docs-archive.pingcap.com/tidb/v8.3/tidb-binlog-overview/)が削除されました。この変数はTiDB Binlogが使用されているかどうかを示し、バージョン8.4.0以降は削除されます。                                                                                                                                    |
| `sql_log_bin`                                                                                                                   | 削除済み     | バージョン8.4.0では、 [TiDB Binlog](https://docs-archive.pingcap.com/tidb/v8.3/tidb-binlog-overview/)が削除されました。この変数は、変更内容をTiDB Binlogに書き込むかどうかを示すもので、バージョン8.4.0以降は削除されます。                                                                                                                              |
| [`tidb_enable_global_index`](/system-variables.md#tidb_enable_global_index-new-in-v760)                                         | 非推奨      | v8.4.0 では、この変数は非推奨です。その値はデフォルト値`ON`に固定されます。つまり、[グローバルインデックス](/global-indexes.md)はデフォルトで有効になっています。 `GLOBAL`または`CREATE TABLE`を実行してグローバル インデックスを作成する際に、対応する列にキーワード`ALTER TABLE`追加するだけで済みます。                                                                                                     |
| [`tidb_enable_list_partition`](/system-variables.md#tidb_enable_list_partition-new-in-v50)                                      | 非推奨      | バージョン8.4.0では、この変数は非推奨となります。その値はデフォルト値`ON`に固定され、[リスト分割](/partitioned-table.md#list-partitioning)がデフォルトで有効になります。                                                                                                                                                                               |
| [`tidb_enable_table_partition`](/system-variables.md#tidb_enable_table_partition)                                               | 非推奨      | v8.4.0 では、この変数は非推奨になりました。その値はデフォルト値`ON`に固定されます。つまり、[テーブルパーティショニング](/partitioned-table.md)はデフォルトで有効になります。                                                                                                                                                                                     |
| [`tidb_analyze_partition_concurrency`](/system-variables.md#tidb_analyze_partition_concurrency)                                 | 変更     | 値の範囲を`[1, 18446744073709551615]`から`[1, 128]`に変更します。                                                                                                                                                                                                                                          |
| [`tidb_enable_inl_join_inner_multi_pattern`](/system-variables.md#tidb_enable_inl_join_inner_multi_pattern-new-in-v700)         | 変更     | デフォルト値を`OFF`から`ON`に変更します。v8.4.0 以降、内部テーブルに`Selection` 、 `Aggregation` 、または`Projection`演算子がある場合、Index Join がデフォルトでサポートされます。                                                                                                                                                              |
| [`tidb_opt_prefer_range_scan`](/system-variables.md#tidb_opt_prefer_range_scan-new-in-v50)                                      | 変更     | デフォルト値を`OFF`から`ON`に変更します。統計情報がないテーブル (擬似統計情報) または空のテーブル (統計情報がゼロ) の場合、オプティマイザはフルテーブルスキャンよりもインターバルスキャンを優先します。                                                                                                                                                                                 |
| [`tidb_scatter_region`](/system-variables.md#tidb_scatter_region)                                                               | 変更     | v8.4.0 より前は、型はブール型で、 `ON`と`OFF`のみをサポートし、新しく作成されたテーブルのリージョンは、有効化後にのみテーブルレベルの分散をサポートします。v8.4.0 以降では、 `SESSION`スコープが追加され、型がブール型から列挙型に変更され、デフォルト値が`OFF`から null に変更され、オプション値`TABLE`と`GLOBAL`が追加されました。さらに、バッチでの高速テーブル作成中にリージョンの不均一な分散によって発生する TiKV OOM の問題を回避するために、クラスタレベルの分散ポリシーがサポートされるようになりました。 |
| [`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-new-in-v800)                                             | 変更     | デフォルト値を`0`から`536870912` (512 MiB) に変更し、この機能がデフォルトで有効になっていることを示します。許可される最小値は`67108864` (64 MiB) に設定されています。                                                                                                                                                                                    |
| [`tidb_auto_analyze_concurrency`](/system-variables.md#tidb_auto_analyze_concurrency-new-in-v840)                               | 新しく追加された | TiDB クラスタ内での自動分析操作の同時実行数を設定します。v8.4.0 より前のバージョンでは、この同時実行数は`1`に固定されていました。統計情報の収集タスクを高速化するには、クラスタで使用可能なリソースに基づいてこの同時実行数を増やすことができます。                                                                                                                                                            |
| [`tidb_enable_instance_plan_cache`](/system-variables.md#tidb_enable_instance_plan_cache-new-in-v840)                           | 新しく追加された | インスタンスプランキャッシュ機能を有効にするかどうかを制御します。                                                                                                                                                                                                                                                            |
| [`tidb_enable_stats_owner`](/system-variables.md#tidb_enable_stats_owner-new-in-v840)                                           | 新しく追加された | 対応するTiDBインスタンスが自動統計更新タスクを実行できるかどうかを制御します。                                                                                                                                                                                                                                                    |
| [`tidb_hash_join_version`](/system-variables.md#tidb_hash_join_version-new-in-v840)                                             | 新しく追加された | TiDB がハッシュ結合演算子の最適化バージョンを使用するかどうかを制御します。デフォルト値の`legacy`は、最適化バージョンが使用されないことを意味します。これを`optimized`に設定すると、TiDB はハッシュ結合演算子の実行時に最適化バージョンを使用して、ハッシュ結合のパフォーマンスを向上させます。                                                                                                                               |
| [`tidb_instance_plan_cache_max_size`](/system-variables.md#tidb_instance_plan_cache_max_size-new-in-v840)                       | 新しく追加された | インスタンスプランキャッシュの最大メモリ使用量を設定します。                                                                                                                                                                                                                                                               |
| [`tidb_instance_plan_cache_reserved_percentage`](/system-variables.md#tidb_instance_plan_cache_reserved_percentage-new-in-v840) | 新しく追加された | メモリ解放後にインスタンスプランキャッシュ用に予約されるアイドルメモリの割合を制御します。                                                                                                                                                                                                                                                |
| [`tidb_pre_split_regions`](/system-variables.md#tidb_pre_split_regions-new-in-v840)                                             | 新しく追加された | バージョン 8.4.0 より前では、新しく作成されたテーブルのデフォルトの行分割スライス数を設定するには、各`PRE_SPLIT_REGIONS` SQL ステートメントで`CREATE TABLE`宣言する必要がありましたが、多数のテーブルを同様に構成する必要がある場合は複雑でした。この変数は、このような問題を解決するために導入されました。使いやすさを向上させるために、このシステム変数を`GLOBAL`または`SESSION`レベルで設定できます。                                                          |
| [`tidb_shard_row_id_bits`](/system-variables.md#tidb_shard_row_id_bits-new-in-v840)                                             | 新しく追加された | バージョン 8.4.0 より前では、新しく作成されたテーブルの行 ID のスライス数のデフォルト設定を行うには、 `SHARD_ROW_ID_BITS`または`CREATE TABLE` SQL ステートメントごとに`ALTER TABLE`宣言する必要がありましたが、多数のテーブルを同様に構成する必要がある場合は複雑でした。この変数は、このような問題を解決するために導入されました。使いやすさを向上させるために、このシステム変数を`GLOBAL`または`SESSION`レベルで設定できます。                                     |
| [`tidb_tso_client_rpc_mode`](/system-variables.md#tidb_tso_client_rpc_mode-new-in-v840)                                         | 新しく追加された | TiDBがPDにTSO RPCリクエストを送信するモードを切り替えます。このモードによって、TSO RPCリクエストを並列処理できるかどうかが決まり、各TS取得操作のバッチ待機時間に影響するため、特定のシナリオにおけるクエリ実行中のTS取得の待機時間を短縮できます。                                                                                                                                                        |

### コンフィグレーションパラメータ {#configuration-parameters}

| コンフィグレーションファイルまたはコンポーネント | コンフィグレーションパラメータ                                                                                                          | 変更の種類  | 説明                                                                                                                                                                                      |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------ | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB                     | [`grpc-keepalive-time`](/tidb-configuration-file.md#grpc-keepalive-time)                                                 | 変更     | `1`の最小値を追加します。                                                                                                                                                                          |
| TiDB                     | [`grpc-keepalive-timeout`](/tidb-configuration-file.md#grpc-keepalive-timeout)                                           | 変更     | バージョン 8.4.0 より前は、このパラメータのデータ型は INT で、最小値は`1`でした。バージョン 8.4.0 以降では、データ型が FLOAT64 に変更され、最小値は`0.05`になります。ネットワークのジッターが頻繁に発生するシナリオでは、値を小さく設定して再試行間隔を短くすることで、ネットワークのジッターがパフォーマンスに与える影響を軽減できます。 |
| TiDB                     | [`tidb_enable_stats_owner`](/tidb-configuration-file.md#tidb_enable_stats_owner-new-in-v840)                             | 新しく追加された | 対応するTiDBインスタンスが自動統計更新タスクを実行できるかどうかを制御します。                                                                                                                                               |
| TiKV                     | [`region-split-keys`](/tikv-configuration-file.md#region-split-keys)                                                     | 変更     | デフォルト値を`"960000"`から`"2560000"`に変更します。                                                                                                                                                   |
| TiKV                     | [`region-split-size`](/tikv-configuration-file.md#region-split-size)                                                     | 変更     | デフォルト値を`"96MiB"`から`"256MiB"`に変更します。                                                                                                                                                     |
| TiKV                     | [`sst-max-size`](/tikv-configuration-file.md#sst-max-size)                                                               | 変更     | デフォルト値を`"144MiB"`から`"384MiB"`に変更します。                                                                                                                                                    |
| TiKV                     | [`pessimistic-txn.in-memory-instance-size-limit`](/tikv-configuration-file.md#in-memory-instance-size-limit-new-in-v840) | 新しく追加された | TiKVインスタンスにおけるメモリ内悲観的ロックのメモリ使用量制限を制御します。この制限を超えると、TiKVは悲観的ロックを永続的に書き込みます。                                                                                                               |
| TiKV                     | [`pessimistic-txn.in-memory-peer-size-limit`](/tikv-configuration-file.md#in-memory-peer-size-limit-new-in-v840)         | 新しく追加された | リージョン内のメモリ内悲観的ロックのメモリ使用量制限を制御します。この制限を超えると、TiKV は悲観的ロックを永続的に書き込みます。                                                                                                                     |
| TiKV                     | [`raft-engine.spill-dir`](/tikv-configuration-file.md#spill-dir-new-in-v840)                                             | 新しく追加された | TiKVインスタンスがRaftログファイルを保存するセカンダリディレクトリを制御し、 Raftログファイルのマルチディスクストレージをサポートします。                                                                                                           |
| TiKV                     | [`resource-control.priority-ctl-strategy`](/tikv-configuration-file.md#priority-ctl-strategy-new-in-v840)                | 新しく追加された | 優先度の低いタスクの管理ポリシーを制御します。TiKVは、優先度の低いタスクにフロー制御を追加することで、優先度の高いタスクが優先的に実行されるようにします。                                                                                                         |
| PD                       | [`cert-allowed-cn`](/enable-tls-between-components.md#verify-component-callers-identity)                                 | 変更     | バージョン8.4.0以降では、複数の`Common Names`の設定がサポートされています。バージョン8.4.0より前は、 `Common Name` 1つしか設定できませんでした。                                                                                            |
| PD                       | [`max-merge-region-keys`](/pd-configuration-file.md#max-merge-region-keys)                                               | 変更     | デフォルト値を`200000`から`540000`に変更します。                                                                                                                                                        |
| PD                       | [`max-merge-region-size`](/pd-configuration-file.md#max-merge-region-size)                                               | 変更     | デフォルト値を`20`から`54`に変更します。                                                                                                                                                                |
| TiFlash                  | [`storage.format_version`](/tiflash/tiflash-configuration.md)                                                            | 変更     | ベクトルインデックスの作成とストレージをサポートするため、デフォルトのTiFlashストレージフォーマットバージョンを`5`から`7`に変更します。このフォーマット変更により、v8.4.0以降のバージョンにアップグレードされたTiFlashクラスタでは、以前のバージョンへのインプレースダウングレードはサポートされません。                   |
| TiDB Binlog               | `--enable-binlog`                                                                                                        | 削除済み     | バージョン8.4.0では、 [TiDB Binlog](https://docs-archive.pingcap.com/tidb/v8.3/tidb-binlog-overview/)が削除されました。このパラメータは、TiDBbinlogの生成を有効にするかどうかを制御するもので、バージョン8.4.0以降は削除されます。                      |
| TiCDC                    | [`claim-check-raw-value`](/ticdc/ticdc-sink-to-kafka.md#send-the-value-field-to-external-storage-only)                   | 新しく追加された | TiCDCがKafkaメッセージの`value`フィールドのみを外部ストレージに送信するかどうかを制御します。この機能は、オープンプロトコルを使用しないシナリオでのみ適用されます。                                                                                            |
| TiDB Lightning           | [`logical-import-prep-stmt`](/tidb-lightning/tidb-lightning-configuration.md)                                            | 新しく追加された | 論理インポートモードでは、このパラメーターは、パフォーマンスを向上させるためにプリペアドステートメントとステートメントキャッシュを使用するかどうかを制御します。デフォルト値は`false`です。                                                                                       |
| BR                       | [`--log.crypter.key`](/br/br-pitr-manual.md#encrypt-the-log-backup-data)                                                 | 新しく追加された | ログバックアップデータの暗号化キーを16進数文字列形式で指定します。アルゴリズム`aes128-ctr`の場合は128ビット（16バイト）のキー、アルゴリズム`aes192-ctr` `aes256-ctr`の場合は32バイトのキーです。                                                                 |
| BR                       | [`--log.crypter.key-file`](/br/br-pitr-manual.md#encrypt-the-log-backup-data)                                            | 新しく追加された | ログバックアップデータのキーファイルを指定します。 `crypter.key`を渡さずに、キーが格納されているファイルパスをパラメータとして直接渡すことができます。                                                                                                      |
| BR                       | [`--log.crypter.method`](/br/br-pitr-manual.md#encrypt-the-log-backup-data)                                              | 新しく追加された | ログバックアップデータの暗号化アルゴリズムを指定します。指定できる値は、 `aes128-ctr` 、 `aes192-ctr` 、または`aes256-ctr`です。デフォルト値は`plaintext`で、データが暗号化されないことを示します。                                                             |
| BR                       | [`--master-key`](/br/br-pitr-manual.md#encrypt-the-log-backup-data)                                                      | 新しく追加された | ログバックアップデータのマスターキーを指定します。ローカルディスクに保存されているマスターキー、またはクラウドキー管理サービス（KMS）によって管理されているマスターキーを指定できます。                                                                                           |
| BR                       | [`--master-key-crypter-method`](/br/br-pitr-manual.md#encrypt-the-log-backup-data)                                       | 新しく追加された | ログバックアップデータのマスターキーに基づく暗号化アルゴリズムを指定します。マスターキーは、 `aes128-ctr` 、 `aes192-ctr` 、または`aes256-ctr`のいずれかです。デフォルト値は`plaintext`で、データが暗号化されないことを示します。                                              |

### オフラインパッケージの変更 {#offline-package-changes}

v8.4.0 以降、次のコンテンツが`TiDB-community-toolkit`[バイナリパッケージ](/binary-package.md)から削除されます。

-   `pump-{version}-linux-{arch}.tar.gz`
-   `drainer-{version}-linux-{arch}.tar.gz`
-   `binlogctl`
-   `arbiter`

### オペレーティングシステムとプラットフォームの要件変更 {#operating-system-and-platform-requirement-changes}

TiDB をアップグレードする前に、オペレーティング システムのバージョンが[OSおよびプラットフォームの要件](/hardware-and-software-requirements.md#os-and-platform-requirements)を満たしていることを確認してください。

-   [CentOS Linux サポート終了](https://www.centos.org/centos-linux-eol/)CentOS Linux 7 のアップストリームサポートは 2024 年 6 月 30 日に終了しました。そのため、TiDB は v8.4.0 で CentOS 7 のサポートを終了します。Rocky Linux 9.1 以降のバージョンを使用することをお勧めします。CentOS 7 上の TiDB クラスタを v8.4.0 にアップグレードすると、クラスタが利用できなくなります。
-   [Red Hat Enterprise Linux ライフサイクル](https://access.redhat.com/support/policy/updates/errata/#Life_Cycle_Dates)によると、Red Hat Enterprise Linux 7 のメンテナンスサポートは 2024 年 6 月 30 日に終了しました。TiDB は、8.4 DMR バージョン以降、Red Hat Enterprise Linux 7 のサポートを終了します。Rocky Linux 9.1 以降のバージョンを使用することをお勧めします。Red Hat Enterprise Linux 7 上の TiDB クラスタを v8.4.0 以降にアップグレードすると、クラスタが使用できなくなります。

## 削除された機能 {#removed-features}

-   バージョン8.4.0以降、以下の機能が削除されます。

    -   バージョン 8.4.0 では、 [TiDB Binlog](https://docs-archive.pingcap.com/tidb/v8.3/tidb-binlog-overview/)は削除されました。バージョン 8.3.0 以降、TiDB Binlog は完全に非推奨となっています。増分データレプリケーションには、代わりに[TiCDC](/ticdc/ticdc-overview.md)を使用してください。ポイントインタイムリカバリ(PITR) には、 [PITR](/br/br-pitr-guide.md)を使用してください。TiDB クラスタをバージョン 8.4.0 以降にアップグレードする前に、必ず TiCDC と PITR に切り替えてください。

-   今後のバージョンでは、以下の機能が削除される予定です。

    -   バージョン8.0.0以降、 TiDB Lightningは[旧バージョンの競合検出](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#the-old-version-of-conflict-detection-deprecated-in-v800)戦略を非推奨とし、 [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)パラメータを使用して論理インポートモードと物理インポートモードの両方の競合検出戦略を制御できるようにします。旧バージョンの競合検出の[`duplicate-resolution`](/tidb-lightning/tidb-lightning-configuration.md)パラメータは、今後のリリースで削除されます。

## 非推奨機能 {#deprecated-features}

以下の機能は、将来のバージョンで廃止される予定です。

-   TiDBでは、統計情報を自動的に収集するタスクの順序を最適化するために優先度キューを有効にするかどうかを制御するためのシステム変数[`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-new-in-v800)が導入されました。今後のリリースでは、統計情報を自動的に収集するタスクの順序付けには優先度キューが唯一の方法となるため、このシステム変数は非推奨となります。
-   TiDBはv7.5.0でシステム変数[`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-new-in-v750)を導入しました。この変数を使用すると、TiDBがパーティション統計の非同期マージを使用するように設定し、メモリ不足の問題を回避できます。今後のリリースでは、パーティション統計は非同期でマージされるため、このシステム変数は非推奨となります。
-   今後のリリースでは [実行プランバインディングの自動進化](/sql-plan-management.md#baseline-evolution)が再設計される予定であり、関連する変数と動作が変更されます。
-   バージョン8.0.0では、TiDBが並列ハッシュアグリゲーションアルゴリズムのディスクスピルをサポートするかどうかを制御するシステム変数[`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-new-in-v800)が導入されました。今後のバージョンでは、 [`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-new-in-v800)システム変数は非推奨となります。
-   TiDB Lightning のパラメータ[`conflict.max-record-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task) 、今後のリリースで非推奨となり、その後削除されます。このパラメータは[`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)に置き換えられます。これは、競合するレコードの最大数が、単一のインポートタスクで許容できる競合レコードの最大数と一致することを意味します。
-   バージョン6.3.0以降、パーティションテーブルはデフォルトで [動的剪定モード](/partitioned-table.md#dynamic-pruning-mode)を使用します。静的剪定モードと比較して、動的剪定モードはIndexJoinやプランキャッシュなどの機能をサポートし、パフォーマンスが向上しています。そのため、静的剪定モードは非推奨となります。

## 改善点 {#improvements}

-   TiDB

    -   大量のデータをスキャンする際のBatchCopタスク構築の効率を最適化する[#55915](https://github.com/pingcap/tidb/issues/55915) [#55413](https://github.com/pingcap/tidb/issues/55413) @[wshwsh12](https://github.com/wshwsh12)
    -   トランザクションのバッファを最適化して、トランザクション内の書き込みレイテンシーと TiDB の CPU 使用率を削減します [#55287](https://github.com/pingcap/tidb/issues/55287) @[you06](https://github.com/you06)
    -   システム変数`tidb_dml_type`が`"bulk"`に設定されている場合の DML ステートメントの実行パフォーマンスを最適化する [#50215](https://github.com/pingcap/tidb/issues/50215) @[ekexium](https://github.com/ekexium)
    -   [オプティマイザー修正制御 47400](/optimizer-fix-controls.md#47400-new-in-v840)の使用をサポートし、オプティマイザーが`estRows`の推定最小値を`1` 。これは、Oracle や Db2 などのデータベースと一貫性があります [#47400](https://github.com/pingcap/tidb/issues/47400) @[terry1purcell](https://github.com/terry1purcell)
    -   [`mysql.tidb_runaway_queries`](/mysql-schema/mysql-schema.md#system-tables-related-to-runaway-queries)ログ テーブルに書き込み制御を追加し、多数の同時書き込みによって発生するオーバーヘッドを削減します [#54434](https://github.com/pingcap/tidb/issues/54434) @[HuSharp](https://github.com/HuSharp)
    -   内部テーブルに`Selection` 、 `Projection` 、または`Aggregation`演算子がある場合、デフォルトでインデックス結合をサポートします [#47233](https://github.com/pingcap/tidb/issues/47233) @[winoros](https://github.com/winoros)
    -   特定のシナリオにおける`DELETE`操作のために TiKV から取得する列の詳細の数を減らし、これらの操作のリソースオーバーヘッドを削減します [#38911](https://github.com/pingcap/tidb/issues/38911) @[winoros](https://github.com/winoros)
    -   TiDBクラスタ内での自動分析操作の同時実行設定をシステム変数`tidb_auto_analyze_concurrency`を使用してサポートする [#53460](https://github.com/pingcap/tidb/issues/53460) @[hawkingrei](https://github.com/hawkingrei)
    -   多数の列を持つテーブルをクエリする際のパフォーマンスを向上させるため、内部関数のロジックを最適化します [#52112](https://github.com/pingcap/tidb/issues/52112) @[Rustin170506](https://github.com/Rustin170506)
    -   `a = 1 AND (a > 1 OR (a = 1 AND b = 2))`から`a = 1 AND b = 2`のようなフィルター条件を簡素化 [#56005](https://github.com/pingcap/tidb/issues/56005) @[ghazalfamilyusa](https://github.com/ghazalfamilyusa)
    -   最適ではない実行プランのリスクが高いシナリオでは、コストモデルでテーブルスキャンのコストを増やし、オプティマイザがインデックスを優先するようにします [#56012](https://github.com/pingcap/tidb/issues/56012) @[terry1purcell](https://github.com/terry1purcell)
    -   TiDB は 2 つの引数を持つバリアント`MID(str, pos)`をサポートしています [#52420](https://github.com/pingcap/tidb/issues/52420) @[dveeden](https://github.com/dveeden)
    -   バイナリ型以外の主キーを持つテーブルのTTLタスクの分割をサポート [#55660](https://github.com/pingcap/tidb/issues/55660) @[lcwangchao](https://github.com/lcwangchao)
    -   システムのメタデータ関連ステートメントのパフォーマンスを最適化する [#50305](https://github.com/pingcap/tidb/issues/50305) @[ywqzzy](https://github.com/ywqzzy) @[tangenta](https://github.com/tangenta)@[joechenrh](https://github.com/joechenrh) @[CbcWestwolf](https://github.com/CbcWestwolf)
    -   自動分析操作に新しい優先度キューを実装して、分析パフォーマンスを向上させ、キューの再構築コストを削減します [#55906](https://github.com/pingcap/tidb/issues/55906) @[Rustin170506](https://github.com/Rustin170506)
    -   統計モジュールがDDLイベントを購読できるように、DDL通知機能を導入する [#55722](https://github.com/pingcap/tidb/issues/55722) @[fzzf678](https://github.com/fzzf678) @[lance6716](https://github.com/lance6716) @[Rustin170506](https://github.com/Rustin170506)
    -   TiDB のアップグレード中に、新しい TiDB ノードが DDL の所有権を引き継ぐように強制することで、古い TiDB ノードが所有権を引き継ぐことによる互換性の問題を回避する [#51285](https://github.com/pingcap/tidb/pull/51285) @[wjhuang2016](https://github.com/wjhuang2016)
    -   クラスターレベルの散乱リージョンをサポート [#8424](https://github.com/tikv/pd/issues/8424) @[River2000i](https://github.com/River2000i)

-   TiKV

    -   リージョンのデフォルト値を 96 MiB から 256 MiB に増やして、Region が多すぎることによる余分なオーバーヘッドを回避します [#17309](https://github.com/tikv/tikv/issues/17309) @[LykxSassinator](https://github.com/LykxSassinator)
    -   リージョンまたはTiKVインスタンスにおけるインメモリ悲観的ロックのメモリ使用量制限の設定をサポートします。ホットライトシナリオで多数の悲観的ロックが発生する場合、構成によってメモリ制限を増やすことができます。これにより、悲観的ロックがディスクに書き込まれることによって発生するCPUおよびI/Oオーバーヘッドを回避できます。 [#17542](https://github.com/tikv/tikv/issues/17542) @[cfzjywxk](https://github.com/cfzjywxk)
    -   Raft Engineに新しい設定項目`spill-dir`を導入し、 Raftログのマルチディスクストレージをサポートします。ホームディレクトリ ( `dir`が配置されているディスクの空き容量がなくなると、 Raft Engine は新しいログを自動的に`spill-dir`に書き込み、システムの継続的な動作を保証します [#17356](https://github.com/tikv/tikv/issues/17356) @[LykxSassinator](https://github.com/LykxSassinator)
    -   RocksDB の圧縮トリガー メカニズムを最適化し、多数の DELETE バージョンを処理する際のディスク領域の再利用を加速します [#17269](https://github.com/tikv/tikv/issues/17269) @[AndreMouche](https://github.com/AndreMouche)
    -   書き込み操作のフロー制御構成を動的に変更するサポート [#17395](https://github.com/tikv/tikv/issues/17395) @[glorv](https://github.com/glorv)
    -   空のテーブルと小さなリージョンを含むシナリオでのリージョンマージの速度を改善 [#17376](https://github.com/tikv/tikv/issues/17376) @[LykxSassinator](https://github.com/LykxSassinator)
    -   [パイプラインDML](https://github.com/pingcap/tidb/blob/release-8.4/docs/design/2024-01-09-pipelined-DML.md)resolved-ts を長期間ブロックしないようにします [#17459](https://github.com/tikv/tikv/issues/17459) @[ekexium](https://github.com/ekexium)

-   PD

    -   TiDB Lightningによるデータインポート中のTiKVノードのグレースフルオフラインをサポート [#7853](https://github.com/tikv/pd/issues/7853) @[okJiang](https://github.com/okJiang)
    -   `scatter-range`コマンドで`scatter-range-scheduler`を`pd-ctl`に名前変更する [#8379](https://github.com/tikv/pd/issues/8379) @[okJiang](https://github.com/okJiang)
    -   `grant-hot-leader-scheduler`の競合検出機能を追加 [#4903](https://github.com/tikv/pd/issues/4903) @[lhy1024](https://github.com/lhy1024)

-   TiFlash

    -   `LENGTH()`および`ASCII()`関数の実行効率を最適化する [#9344](https://github.com/pingcap/tiflash/issues/9344) @[xzhangxian1008](https://github.com/xzhangxian1008)
    -   TiFlashが分散ストレージとコンピューティング要求を処理する際に作成する必要のあるスレッド数を減らし、そのような要求を多数処理する際のTiFlashコンピューティングノードのクラッシュを回避するのに役立ちます [#9334](https://github.com/pingcap/tiflash/issues/9334) @[JinheLin](https://github.com/JinheLin)
    -   パイプライン実行モデルにおけるタスク待機メカニズムの強化 [#8869](https://github.com/pingcap/tiflash/issues/8869) @[SeaRise](https://github.com/SeaRise)
    -   JOIN オペレーターがキャンセル要求にタイムリーに応答できるように、JOIN オペレーターのキャンセル メカニズムを改善 [#9430](https://github.com/pingcap/tiflash/issues/9430) @[windtalker](https://github.com/windtalker)

-   ツール

    -   Backup & Restore (BR)

        -   `split-table`および`split-region-on-table`構成項目が`false` (デフォルト値) であるクラスターにデータを復元する際、テーブルによるリージョンの分割を無効にすることで復元速度を向上させます。 [#53532](https://github.com/pingcap/tidb/issues/53532) @[Leavrth](https://github.com/Leavrth)
        -   デフォルトでは、 `RESTORE` SQL ステートメントを使用して、空ではないクラスターへの完全なデータの復元を無効にします [#55087](https://github.com/pingcap/tidb/issues/55087) @[BornChanger](https://github.com/BornChanger)

## バグ修正 {#bug-fixes}

-   TiDB

    -   `tidb_restricted_read_only`変数が`true`に設定されている場合にデッドロックが発生する可能性がある問題を修正します。 [#53822](https://github.com/pingcap/tidb/issues/53822) [#55373](https://github.com/pingcap/tidb/issues/55373) @[Defined2014](https://github.com/Defined2014)
    -   TiDBが正常シャットダウン中に自動コミットトランザクションの完了を待たない問題を修正 [#55464](https://github.com/pingcap/tidb/issues/55464) @[YangKeao](https://github.com/YangKeao)
    -   TTLジョブ実行中に`tidb_ttl_delete_worker_count`の値を減らすとジョブが完了しない問題を修正 [#55561](https://github.com/pingcap/tidb/issues/55561) @[lcwangchao](https://github.com/lcwangchao)
    -   テーブルのインデックスに生成列が含まれている場合、 `Unknown column 'column_name' in 'expression'`ステートメントを使用してテーブルの統計情報を収集する際に`ANALYZE`エラーが発生する可能性がある問題を修正しました。 [#55438](https://github.com/pingcap/tidb/issues/55438) @[hawkingrei](https://github.com/hawkingrei)
    -   統計関連の不要な設定を非推奨にして、冗長なコードを削減する [#55043](https://github.com/pingcap/tidb/issues/55043) @[Rustin170506](https://github.com/Rustin170506)
    -   相関サブクエリとCTEを含むクエリを実行するとTiDBがハングアップしたり、誤った結果を返す可能性がある問題を修正しました [#55551](https://github.com/pingcap/tidb/issues/55551) @[guo-shaoge](https://github.com/guo-shaoge)
    -   `lite-init-stats`を無効にすると統計情報が同期的に読み込まれない可能性がある問題を修正しました [#54532](https://github.com/pingcap/tidb/issues/54532) @[hawkingrei](https://github.com/hawkingrei)
    -   `UPDATE`または`DELETE`ステートメントに再帰 CTE が含まれている場合、ステートメントがエラーを報告するか、効果を発揮しない可能性がある問題を修正します [#55666](https://github.com/pingcap/tidb/issues/55666) @[time-and-fate](https://github.com/time-and-fate)
    -   ウィンドウ関数を含む SQL バインディングが場合によっては有効にならない問題を修正しました [#55981](https://github.com/pingcap/tidb/issues/55981) @[winoros](https://github.com/winoros)
    -   非バイナリ照合順序を持つ文字列列の統計情報が、統計情報の初期化時にロードに失敗する可能性がある問題を修正 [#55684](https://github.com/pingcap/tidb/issues/55684) @[winoros](https://github.com/winoros)
    -   クエリ条件`column IS NULL`を使用して一意インデックスにアクセスする際に、オプティマイザが行数を誤って 1 と推定する問題を修正しました。 [#56116](https://github.com/pingcap/tidb/issues/56116) @[hawkingrei](https://github.com/hawkingrei)
    -   クエリに`(... AND ...) OR (... AND ...) ...`のようなフィルタ条件が含まれている場合、オプティマイザが行数推定に最適な複数列統計情報を使用しない問題を修正します [#54323](https://github.com/pingcap/tidb/issues/54323) @[time-and-fate](https://github.com/time-and-fate)
    -   クエリに利用可能なインデックス マージ実行プランがある場合、 `read_from_storage`ヒントが有効にならない可能性がある問題を修正 [#56217](https://github.com/pingcap/tidb/issues/56217) @[AilinKid](https://github.com/AilinKid)
    -   `IndexNestedLoopHashJoin` のデータ競合問題を修正 [#49692](https://github.com/pingcap/tidb/issues/49692) @[solotzg](https://github.com/solotzg)
    -   `SUB_PART`テーブル内の`INFORMATION_SCHEMA.STATISTICS`の値が`NULL`になっている問題を修正します [#55812](https://github.com/pingcap/tidb/issues/55812) @[Defined2014](https://github.com/Defined2014)
    -   DMLステートメントにネストされた生成列が含まれている場合にエラーが発生する問題を修正しました [#53967](https://github.com/pingcap/tidb/issues/53967) @[wjhuang2016](https://github.com/wjhuang2016)
    -   除算演算において最小表示長の整数型データを使用すると除算結果がオーバーフローする場合がある問題を修正 [#55837](https://github.com/pingcap/tidb/issues/55837) @[windtalker](https://github.com/windtalker)
    -   TopN オペレーターに続くオペレーターがメモリ制限を超えた場合にフォールバックアクションをトリガーできない問題を修正しました [#56185](https://github.com/pingcap/tidb/issues/56185) @[xzhangxian1008](https://github.com/xzhangxian1008)
    -   ソート演算子の`ORDER BY`列に定数が含まれている場合に、列が固定されてしまう問題を修正しました。 [#55344](https://github.com/pingcap/tidb/issues/55344) @[xzhangxian1008](https://github.com/xzhangxian1008)
    -   インデックスを追加する際に、PDリーダーを終了させた後に`8223 (HY000)`エラーが発生し、テーブル内のデータが不整合になる問題を修正しました [#55488](https://github.com/pingcap/tidb/issues/55488) @[tangenta](https://github.com/tangenta)
    -   DDL履歴ジョブが多すぎると、履歴DDLジョブに関する情報を要求するとOOMが発生する問題を修正 [#55711](https://github.com/pingcap/tidb/issues/55711) @[joccau](https://github.com/joccau)
    -   グローバルソートが有効で、リージョンサイズが96 MiBを超える場合に`IMPORT INTO`の実行が停止する問題を修正しました。 [#55374](https://github.com/pingcap/tidb/issues/55374) @[lance6716](https://github.com/lance6716)
    -   一時テーブルで`IMPORT INTO`を実行すると TiDB がクラッシュする問題を修正しました [#55970](https://github.com/pingcap/tidb/issues/55970) @[D3Hunter](https://github.com/D3Hunter)
    -   一意インデックスを追加すると`duplicate entry`エラーが発生する問題を修正 [#56161](https://github.com/pingcap/tidb/issues/56161) @[tangenta](https://github.com/tangenta)
    -   TiKVが810秒以上ダウンしている場合、 TiDB LightningがすべてのKVペアを取り込まないため、テーブル内のデータが不整合になる問題を修正しました [#55808](https://github.com/pingcap/tidb/issues/55808) @[lance6716](https://github.com/lance6716)
    -   `CREATE TABLE LIKE`ステートメントがキャッシュされたテーブルに使用できない問題を修正 [#56134](https://github.com/pingcap/tidb/issues/56134) @[tiancaiamao](https://github.com/tiancaiamao)
    -   CTE 内の`FORMAT()`式の紛らわしい警告メッセージを修正 [#56198](https://github.com/pingcap/tidb/pull/56198) @[dveeden](https://github.com/dveeden)
    -   パーティションテーブルを作成する際に、 `CREATE TABLE`と`ALTER TABLE`の間で列タイプの制限が矛盾する問題を修正 [#56094](https://github.com/pingcap/tidb/issues/56094) @[mjonss](https://github.com/mjonss)
    -   `INFORMATION_SCHEMA.RUNAWAY_WATCHES`テーブル内の誤った時間タイプを修正 [#54770](https://github.com/pingcap/tidb/issues/54770) @[HuSharp](https://github.com/HuSharp)

-   TiKV

    -   マスターキーがキー管理サービス（KMS）に保存されている場合にマスターキーのローテーションが妨げられる問題を修正しました [#17410](https://github.com/tikv/tikv/issues/17410) @[hhwyt](https://github.com/hhwyt)
    -   大きなテーブルやパーティションを削除した後に発生する可能性のあるトラフィック制御の問題を修正 [#17304](https://github.com/tikv/tikv/issues/17304) @[Connor1996](https://github.com/Connor1996)
    -   TiKVが、遅い分割操作と新しいレプリカの即時削除によってトリガーされる、古いレプリカがRaftスナップショットを処理する際にpanic可能性がある問題を修正しました [#17469](https://github.com/tikv/tikv/issues/17469) @[hbisheng](https://github.com/hbisheng)

-   TiFlash

    -   テーブルに無効な文字を含むデフォルト値を持つビット型列が含まれている場合、 TiFlashがテーブルスキーマを解析できない問題を修正しました [#9461](https://github.com/pingcap/tiflash/issues/9461) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    -   複数のリージョンが同時にスナップショットを適用している際に発生する、リージョン重複チェックの誤った失敗によりTiFlashがpanic可能性がある問題を修正しました [#9329](https://github.com/pingcap/tiflash/issues/9329) @[CalvinNeo](https://github.com/CalvinNeo)
    -   TiFlashでサポートされていない一部の JSON関数がTiFlashにプッシュダウンされる問題を修正 [#9444](https://github.com/pingcap/tiflash/issues/9444) @[windtalker](https://github.com/windtalker)

-   ツール

    -   Backup & Restore (BR)

        -   TiDBノードが停止した際に、監視中のPITRチェックポイント間隔が異常に増加し、実際の状況を反映しない問題を修正しました [#42419](https://github.com/pingcap/tidb/issues/42419) @[YuJuncen](https://github.com/YuJuncen)
        -   バックアップ処理中にTiKVが応答しなくなった場合にバックアップタスクが停止する可能性がある問題を修正 [#53480](https://github.com/pingcap/tidb/issues/53480) @[Leavrth](https://github.com/Leavrth)
        -   ログバックアップが有効になっている場合に、 BRログに機密の認証情報が出力される可能性がある問題を修正 [#55273](https://github.com/pingcap/tidb/issues/55273) @[RidRisR](https://github.com/RidRisR)
        -   ログバックアップPITRタスクが失敗して停止した後、そのタスクに関連するセーフポイントが正しくクリアされない問題を修正しました（PD [#17316](https://github.com/tikv/tikv/issues/17316) @[Leavrth](https://github.com/Leavrth)

    -   TiDB Data Migration (DM)

        -   複数のDMマスターノードが同時にリーダーになる可能性があり、データ不整合を引き起こす問題を修正しました [#11602](https://github.com/pingcap/tiflow/issues/11602) @[GMHDBJD](https://github.com/GMHDBJD)
        -   `ALTER DATABASE`ステートメントを処理する際に DM がデフォルト データベースを設定しない問題を修正します。これにより、レプリケーション エラー [#11503](https://github.com/pingcap/tiflow/issues/11503)が発生します。@[lance6716](https://github.com/lance6716)

    -   TiDB Lightning

        -   TiDB Lightning が、2 つのインスタンスが同時に並列インポートタスクを開始し、同じタスク ID が割り当てられた場合、 `verify allocator base failed`エラーを報告する問題を修正しました [#55384](https://github.com/pingcap/tidb/issues/55384) @[ei-sugimoto](https://github.com/ei-sugimoto)

## 貢献者 {#contributors}

TiDBコミュニティの以下の貢献者の皆様に感謝申し上げます。

-   [ei-sugimoto](https://github.com/ei-sugimoto)
-   [eltociear](https://github.com/eltociear)
-   [guoshouyan](https://github.com/guoshouyan) (初回貢献者)
-   [JackL9u](https://github.com/JackL9u)
-   [kafka1991](https://github.com/kafka1991) (初回貢献者)
-   [qingfeng777](https://github.com/qingfeng777)
-   [samba-rgb](https://github.com/samba-rgb) (初回貢献者)
-   [SeaRise](https://github.com/SeaRise)
-   [tuziemon](https://github.com/tuziemon) (初回貢献者)
-   [xyproto](https://github.com/xyproto) (初回貢献者)
