---
title: TiDB 8.4.0 Release Notes
summary: TiDB 8.4.0 の新機能、互換性の変更、改善、バグ修正について説明します。
---

# TiDB 8.4.0 リリースノート {#tidb-8-4-0-release-notes}

発売日: 2024年11月11日

TiDB バージョン: 8.4.0

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v8.4/quick-start-with-tidb)

8.4.0 では、次の主要な機能と改善が導入されています。

<table><thead><tr><th>カテゴリ</th><th>機能/拡張機能</th><th>説明</th></tr></thead><tbody><tr><td rowspan="4">スケーラビリティとパフォーマンス</td><td><a href="https://docs.pingcap.com/tidb/v8.4/system-variables#tidb_enable_instance_plan_cache-new-in-v840">インスタンスレベルの実行プラン キャッシュ</a>(実験的)</td><td>インスタンス レベルのプラン キャッシュを使用すると、同じ TiDB インスタンス内のすべてのセッションでプラン キャッシュを共有できます。セッション レベルのプラン キャッシュと比較すると、この機能では、より多くの実行プランをメモリにキャッシュすることで SQL コンパイル時間が短縮され、全体的な SQL 実行時間が短縮されます。これにより、OLTP のパフォーマンスとスループットが向上し、メモリ使用量の制御が向上し、データベースの安定性が向上します。</td></tr><tr><td><a href="https://docs.pingcap.com/tidb/v8.4/partitioned-table#global-indexes">パーティションテーブルのグローバルインデックス</a>(GA)</td><td>グローバル インデックスを使用すると、パーティション化されていない列の取得効率を効果的に向上でき、一意のキーにパーティション キーが含まれていなければならないという制限がなくなります。この機能により、TiDB パーティション テーブルの使用シナリオが拡張され、データ移行に必要なアプリケーション変更作業の一部が回避されます。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v8.4/system-variables#tidb_tso_client_rpc_mode-new-in-v840">TSO リクエストの並列モード</a></td><td>同時実行性の高いシナリオでは、この機能を使用して、TSO の取得の待機時間を短縮し、クラスターのスループットを向上させることができます。</td></tr><tr><td><a href="https://docs.pingcap.com/tidb/v8.4/cached-tables">キャッシュされたテーブル</a>のクエリパフォーマンスを向上</td><td>キャッシュされたテーブルでのインデックス スキャンのクエリ パフォーマンスが向上し、シナリオによっては最大 5.4 倍向上します。小さなテーブルでの高速クエリの場合、キャッシュされたテーブルを使用すると、全体的なパフォーマンスが大幅に向上します。</td></tr><tr><td rowspan="4">信頼性と可用性</td><td><a href="https://docs.pingcap.com/tidb/v8.4/tidb-resource-control#query_limit-parameters">ランナウェイクエリのトリガーをさらにサポートし、リソースグループの切り替えをサポートします。</a></td><td>ランナウェイ クエリは、予期しない SQL パフォーマンスの問題がシステムに与える影響を軽減する効果的な方法を提供します。TiDB v8.4.0 では、コプロセッサーによって処理されたキーの数 ( <code>PROCESSED_KEYS</code> ) と要求単位 ( <code>RU</code> ) が識別条件として導入され、識別されたクエリが指定されたリソース グループに配置されるため、ランナウェイ クエリをより正確に識別して制御できます。</td></tr><tr><td><a href="https://docs.pingcap.com/tidb/v8.4/tidb-resource-control#background-parameters">リソース制御のバックグラウンドタスクのリソース使用量の上限設定をサポート</a></td><td>リソース制御のバックグラウンド タスクに最大パーセンテージ制限を設定することで、さまざまなアプリケーション システムのニーズに基づいてリソース消費を制御できます。これにより、バックグラウンド タスクの消費を低いレベルに抑え、オンライン サービスの品質を確保できます。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v8.4/tiproxy-traffic-replay">TiProxy はトラフィックのキャプチャと再生をサポートします</a>(実験的)</td><td> TiProxy を使用して、クラスターのアップグレード、移行、またはデプロイメントの変更などの主要な操作の前に、TiDB 実本番クラスターから実際のワークロードをキャプチャします。これらのワークロードをターゲット テスト クラスターで再生して、パフォーマンスを検証し、変更が成功したことを確認します。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v8.4/system-variables#tidb_auto_analyze_concurrency-new-in-v840">同時自動統計収集</a></td><td>システム変数<code>tidb_auto_analyze_concurrency</code>を使用して、単一の自動統計収集タスク内での同時実行を設定できます。TiDB は、ノードの規模とハードウェア仕様に基づいて、スキャン タスクの同時実行を自動的に決定します。これにより、システム リソースを最大限に活用して統計収集の効率が向上し、手動によるチューニングが減り、安定したクラスター パフォーマンスが保証されます。</td></tr><tr><td rowspan="1">構文</td><td><a href="https://docs.pingcap.com/tidb/v8.4/vector-search-overview">ベクトル検索</a>（実験的）</td><td>ベクトル検索は、データセマンティクスに基づく検索方法であり、より関連性の高い検索結果を提供します。AI と大規模言語モデル (LLM) のコア関数の 1 つとして、ベクトル検索は、検索拡張生成 (RAG)、セマンティック検索、推奨システムなど、さまざまなシナリオで使用できます。</td></tr><tr><td rowspan="3"> DB 操作と可観測性</td><td><a href="https://docs.pingcap.com/tidb/v8.4/information-schema-processlist">メモリテーブルに TiKV と TiDB の CPU 時間を表示する</a></td><td>CPU 時間がシステム テーブルに統合され、セッションや SQL の他のメトリックと一緒に表示されるようになったため、CPU 消費量の多い操作を複数の観点から観察し、診断の効率を向上させることができます。これは、インスタンス内の CPU スパイクやクラスター内の読み取り/書き込みホットスポットなどのシナリオを診断する場合に特に便利です。</td></tr><tr><td><a href="https://docs.pingcap.com/tidb/v8.4/top-sql#use-top-sql">テーブルまたはデータベースごとに集計された TiKV CPU 時間の表示をサポート</a></td><td>ホットスポットの問題が個々の SQL ステートメントによって発生していない場合は、 Top SQLのテーブルまたはデータベース レベル別に集計された CPU 時間を使用すると、ホットスポットの原因となっているテーブルまたはアプリケーションを迅速に特定できるため、ホットスポットと CPU 消費の問題の診断効率が大幅に向上します。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v8.4/backup-and-restore-storages#authentication">IMDSv2 サービスを有効にした TiKV インスタンスのバックアップをサポート</a></td><td><a href="https://aws.amazon.com/cn/blogs/security/get-the-full-benefits-of-imdsv2-and-disable-imdsv1-across-your-aws-infrastructure/">AWS EC2 は、デフォルトのメタデータ サービスとして IMDSv2 を使用するようになりました</a>。TiDB は、IMDSv2 が有効になっている TiKV インスタンスからのデータのバックアップをサポートしており、パブリック クラウド サービスで TiDB クラスターをより効率的に実行するのに役立ちます。</td></tr><tr><td rowspan="1">Security</td><td><a href="https://docs.pingcap.com/tidb/v8.4/br-pitr-manual#encrypt-log-backup-data">ログバックアップデータのクライアント側暗号化</a>（実験的）</td><td>ログ バックアップ データをバックアップstorageにアップロードする前に、バックアップ データを暗号化して、storage中および転送中のセキュリティを確保できます。</td></tr></tbody></table>

## 機能の詳細 {#feature-details}

### パフォーマンス {#performance}

-   TSOリクエストに並列バッチモードを導入し、TSO取得のレイテンシーを短縮する[＃54960](https://github.com/pingcap/tidb/issues/54960) [＃8432](https://github.com/tikv/pd/issues/8432) @ [ミョンケミンタ](https://github.com/MyonKeminta)

    v8.4.0 より前では、PD から[TSO](/tso.md)要求すると、TiDB は特定の期間に複数の TSO 要求を収集し、それらをバッチでシリアルに処理して、リモート プロシージャ コール (RPC) 要求の数を減らし、PD のワークロードを軽減していました。ただし、レイテンシの影響を受けやすいシナリオでは、このシリアル バッチ モードのパフォーマンスは理想的ではありません。

    v8.4.0 では、TiDB は、さまざまな同時実行機能を備えた TSO 要求の並列バッチ モードを導入しています。並列モードでは、TSO 取得のレイテンシーが短縮されますが、PD ワークロードが増加する可能性があります。TSO を取得するための並列 RPC モードを設定するには、 [`tidb_tso_client_rpc_mode`](/system-variables.md#tidb_tso_client_rpc_mode-new-in-v840)システム変数を構成します。

    詳細については[ドキュメント](/system-variables.md#tidb_tso_client_rpc_mode-new-in-v840)参照してください。

-   TiDBのハッシュ結合演算子の実行効率を最適化（実験的） [＃55153](https://github.com/pingcap/tidb/issues/55153) [＃53127](https://github.com/pingcap/tidb/issues/53127) @ [風の話し手](https://github.com/windtalker) @ [翻訳者](https://github.com/xzhangxian1008) @ [徐懐玉](https://github.com/XuHuaiyu) @ [うわー](https://github.com/wshwsh12)

    v8.4.0 では、TiDB はハッシュ結合演算子の最適化バージョンを導入し、実行効率を向上させています。現在、ハッシュ結合の最適化バージョンは内部結合と外部結合操作にのみ適用され、デフォルトでは無効になっています。この最適化バージョンを有効にするには、 [`tidb_hash_join_version`](/system-variables.md#tidb_hash_join_version-new-in-v840)システム変数を`optimized`に設定します。

    詳細については[ドキュメント](/system-variables.md#tidb_hash_join_version-new-in-v840)参照してください。

-   次の日付関数を TiKV [＃56297](https://github.com/pingcap/tidb/issues/56297) [＃17529](https://github.com/tikv/tikv/issues/17529) @ [ゲンリキ](https://github.com/gengliqi)にプッシュダウンすることをサポートします

    -   `DATE_ADD()`
    -   `DATE_SUB()`
    -   `ADDDATE()`
    -   `SUBDATE()`

    詳細については[ドキュメント](/functions-and-operators/expressions-pushed-down.md)参照してください。

-   インスタンスレベルの実行プランキャッシュをサポート (実験的) [＃54057](https://github.com/pingcap/tidb/issues/54057) @ [qw4990](https://github.com/qw4990)

    インスタンス レベルの実行プラン キャッシュを使用すると、同じ TiDB インスタンス内のすべてのセッションで実行プラン キャッシュを共有できます。この機能により、TiDB クエリの応答時間が大幅に短縮され、クラスターのスループットが向上し、実行プランの変更の可能性が減り、安定したクラスター パフォーマンスが維持されます。セッション レベルの実行プラン キャッシュと比較して、インスタンス レベルの実行プラン キャッシュには次の利点があります。

    -   冗長性を排除し、同じメモリ消費量でより多くの実行プランをキャッシュします。
    -   インスタンスに固定サイズのメモリを割り当て、メモリ使用量をより効果的に制限します。

    v8.4.0 では、インスタンス レベルの実行プラン キャッシュはクエリ実行プランのキャッシュのみをサポートしており、デフォルトでは無効になっています。 [`tidb_enable_instance_plan_cache`](/system-variables.md#tidb_enable_instance_plan_cache-new-in-v840)使用してこの機能を有効にし、 [`tidb_instance_plan_cache_max_size`](/system-variables.md#tidb_instance_plan_cache_max_size-new-in-v840)使用して最大メモリ使用量を設定できます。 この機能を有効にする前に、 [準備された実行計画キャッシュ](/sql-prepared-plan-cache.md)と[準備されていない実行プランのキャッシュ](/sql-non-prepared-plan-cache.md)無効にしてください。

    詳細については[ドキュメント](/system-variables.md#tidb_enable_instance_plan_cache-new-in-v840)参照してください。

-   TiDB Lightningの論理インポートモードは、準備されたステートメントとクライアントステートメントキャッシュ[＃54850](https://github.com/pingcap/tidb/issues/54850) @ [dbsid](https://github.com/dbsid)をサポートします。

    `logical-import-prep-stmt`構成項目を有効にすると、TiDB Lightning の論理インポート モードで実行される SQL ステートメントは、準備されたステートメントとクライアント ステートメント キャッシュを使用します。これにより、 TiDB SQL の解析とコンパイルのコストが削減され、SQL 実行効率が向上し、実行プラン キャッシュにヒットする可能性が高くなり、論理インポートが高速化されます。

    詳細については[ドキュメント](/tidb-lightning/tidb-lightning-configuration.md)参照してください。

-   パーティションテーブルはグローバルインデックスをサポートします (GA) [＃45133](https://github.com/pingcap/tidb/issues/45133) @ [ミョンス](https://github.com/mjonss) @ [定義2014](https://github.com/Defined2014) @ [ジフハウス](https://github.com/jiyfhust) @ [L-メープル](https://github.com/L-maple)

    初期の TiDB バージョンでは、グローバル インデックスをサポートしていないため、パーティションテーブルにはいくつかの制限がありました。たとえば、一意のキーは、テーブルのパーティション式のすべての列を使用する必要があります。クエリ条件でパーティション キーが使用されていない場合、クエリはすべてのパーティションをスキャンするため、パフォーマンスが低下します。v7.6.0 以降では、グローバル インデックス機能を有効にするためにシステム変数[`tidb_enable_global_index`](/system-variables.md#tidb_enable_global_index-new-in-v760)が導入されました。ただし、この機能は当時開発中であり、有効にすることは推奨されません。

    v8.3.0 以降、グローバル インデックス機能は実験的機能としてリリースされています。1 キーワードを使用して、パーティションテーブルのグローバル インデックスを明示的に作成できます。これにより、パーティションテーブルの一意のキーにはパーティション式で`GLOBAL`されるすべての列を含める必要があるという制限がなくなり、より柔軟なアプリケーション要件が可能になります。さらに、グローバル インデックスにより、パーティション化されていない列に基づくクエリのパフォーマンスも向上します。

    v8.4.0 では、この機能が一般提供 (GA) されます。グローバル インデックス機能を有効にするためにシステム変数[`tidb_enable_global_index`](/system-variables.md#tidb_enable_global_index-new-in-v760)を設定する代わりに、キーワード`GLOBAL`使用してグローバル インデックスを作成できます。v8.4.0 以降、このシステム変数は非推奨となり、常に`ON`なります。

    詳細については[ドキュメント](/partitioned-table.md#global-indexes)参照してください。

-   いくつかのシナリオでキャッシュされたテーブルのクエリパフォーマンスを向上[＃43249](https://github.com/pingcap/tidb/issues/43249) @ [天菜まお](https://github.com/tiancaiamao)

    v8.4.0 では、TiDB は`SELECT ... LIMIT 1` `IndexLookup`で実行する場合、キャッシュされたテーブルのクエリ パフォーマンスを最大 5.4 倍向上させます。さらに、TiDB はフル テーブル スキャンと主キー クエリ シナリオで`IndexLookupReader`のパフォーマンスを向上させます。

### 信頼性 {#reliability}

-   ランナウェイクエリは、処理されたキーとリクエストユニットの数をしきい値[＃54434](https://github.com/pingcap/tidb/issues/54434) @ [ヒューシャープ](https://github.com/HuSharp)としてサポートします。

    v8.4.0以降、TiDBは処理されたキーの数（ `PROCESSED_KEYS` ）とリクエストユニット数（ `RU` ）に基づいて、暴走クエリを識別できるようになりました。実行時間（ `EXEC_ELAPSED` ）と比較して、これらの新しいしきい値はクエリのリソース消費をより正確に定義し、全体的なパフォーマンスが低下した場合の識別バイアスを回避します。

    複数の条件を同時に設定することができ、いずれかの条件が満たされるとクエリはランナウェイ クエリとして識別されます。

    [ステートメント要約表](/statement-summary-tables.md)の対応するフィールド ( `RESOURCE_GROUP` 、 `MAX_REQUEST_UNIT_WRITE` 、 `MAX_REQUEST_UNIT_READ` 、 `MAX_PROCESSED_KEYS` ) を観察して、実行履歴に基づいて条件値を判断できます。

    詳細については[ドキュメント](/tidb-resource-control.md#manage-queries-that-consume-more-resources-than-expected-runaway-queries)参照してください。

-   ランナウェイクエリ[＃54434](https://github.com/pingcap/tidb/issues/54434) @ [じゃがいも](https://github.com/JmPotato)のリソースグループの切り替えをサポート

    TiDB v8.4.0 以降では、ランナウェイ クエリのリソース グループを特定のグループに切り替えることができます。 `COOLDOWN`メカニズムでリソース消費を抑えることができない場合は、 [リソース グループ](/tidb-resource-control.md#create-a-resource-group)を作成し、そのリソース サイズを制限し、 `SWITCH_GROUP`パラメータを設定して、識別されたランナウェイ クエリをこのグループに移動することができます。その間、同じセッション内の後続のクエリは、元のリソース グループで引き続き実行されます。リソース グループを切り替えることで、リソースの使用をより正確に管理し、リソース消費をより厳密に制御できます。

    詳細については[ドキュメント](/tidb-resource-control.md#query_limit-parameters)参照してください。

-   `tidb_scatter_region`システム変数[＃55184](https://github.com/pingcap/tidb/issues/55184) @ [D3ハンター](https://github.com/D3Hunter)を使用してクラスターレベルのリージョン分散戦略の設定をサポートします。

    v8.4.0 より前では、 `tidb_scatter_region`システム変数は有効または無効にすることしかできませんでした。有効にすると、TiDB はバッチ テーブルの作成時にテーブル レベルの分散戦略を適用します。ただし、バッチで数十万のテーブルを作成すると、この戦略により、いくつかの TiKV ノードに領域が集中し、それらのノードで OOM (メモリ不足) の問題が発生します。

    v8.4.0 以降、 `tidb_scatter_region`文字列型に変更されました。クラスター レベルの分散戦略がサポートされるようになり、前述のシナリオでの TiKV OOM の問題を回避するのに役立ちます。

    詳細については[ドキュメント](/system-variables.md#tidb_scatter_region)参照してください。

-   リソース制御[＃56019](https://github.com/pingcap/tidb/issues/56019) @ [栄光](https://github.com/glorv)のバックグラウンドタスクのリソース使用量の上限設定をサポート

    TiDB リソース制御は、バックグラウンド タスクを識別してその優先度を下げることができます。特定のシナリオでは、リソースが利用可能な場合でも、バックグラウンド タスクのリソース消費を制限する必要がある場合があります。v8.4.0 以降では、 `UTILIZATION_LIMIT`パラメータを使用して、バックグラウンド タスクが消費できるリソースの最大割合を設定できます。各ノードは、すべてのバックグラウンド タスクのリソース使用量をこの割合未満に保ちます。この機能により、バックグラウンド タスクのリソース消費を正確に制御できるようになり、クラスターの安定性がさらに向上します。

    詳細については[ドキュメント](/tidb-resource-control.md#manage-background-tasks)参照してください。

-   リソースグループ[＃50831](https://github.com/pingcap/tidb/issues/50831) @ [ノルーシュ](https://github.com/nolouch)のリソース割り当て戦略を最適化する

    TiDB は、リソース管理に対するユーザーの期待にさらに応えるために、v8.4.0 でリソース割り当て戦略を改善しました。

    -   実行時に大規模なクエリのリソース割り当てを制御して、リソース グループの制限を超えないようにし、ランナウェイ クエリ`COOLDOWN`と組み合わせます。これにより、大規模なクエリの同時実行を識別して削減し、瞬間的なリソース消費を削減できます。
    -   デフォルトの優先度スケジュール戦略を調整します。異なる優先度のタスクが同時に実行される場合、優先度の高いタスクにはより多くのリソースが割り当てられます。

### 可用性 {#availability}

-   TiProxy はトラフィック再生をサポートします (実験的) [＃642](https://github.com/pingcap/tiproxy/issues/642) @ [翻訳者](https://github.com/djshow832)

    TiProxy v1.3.0 以降では、 `tiproxyctl`使用して TiProxy インスタンスに接続し、TiDB本番クラスターでアクセス トラフィックをキャプチャし、指定されたレートでテスト クラスターで再生することができます。この機能により、実本番クラスターの実際のワークロードをテスト環境で再現し、SQL ステートメントの実行結果とパフォーマンスを検証することができます。

    トラフィック リプレイは、次のシナリオで役立ちます。

    -   TiDB バージョンのアップグレードを確認する
    -   変更の影響を評価する
    -   TiDBを拡張する前にパフォーマンスを検証する
    -   テストパフォーマンスの限界

    詳細については[ドキュメント](/tiproxy/tiproxy-traffic-replay.md)参照してください。

### 構文 {#sql}

-   サポートベクター検索（実験的） [＃54245](https://github.com/pingcap/tidb/issues/54245) [＃17290](https://github.com/tikv/tikv/issues/17290) [＃9032](https://github.com/pingcap/tiflash/issues/9032) @ [そよ風のような](https://github.com/breezewish) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger) @ [エリック・ゼクアン](https://github.com/EricZequan) @ [ジムララ](https://github.com/zimulala) @ [ジェイソン・ファン](https://github.com/JaySon-Huang) @ [ウィノロス](https://github.com/winoros) @ [989898 円](https://github.com/wk989898)

    ベクトル検索は、データセマンティクスに基づく検索方法であり、より関連性の高い検索結果を提供します。AI と大規模言語モデル (LLM) のコア関数の 1 つとして、ベクトル検索は、検索拡張生成 (RAG)、セマンティック検索、推奨システムなど、さまざまなシナリオで使用できます。

    v8.4.0 以降、TiDB は[ベクトルデータ型](/vector-search-data-types.md)と[ベクトル検索インデックス](/vector-search-index.md)サポートし、強力なベクトル検索機能を提供します。TiDB ベクトル データ型は最大 16,383 次元をサポートし、L2 距離 (ユークリッド距離)、コサイン距離、負の内積、L1 距離 (マンハッタン距離) など、さまざまな[距離関数](/vector-search-functions-and-operators.md#vector-functions)サポートします。

    ベクトル検索を開始するには、ベクトル データ型のテーブルを作成し、ベクトル データを挿入して、ベクトル データのクエリを実行するだけです。ベクトル データと従来のリレーショナル データの混合クエリを実行することもできます。

    ベクトル検索のパフォーマンスを向上させるには、 [ベクトル検索インデックス](/vector-search-index.md)作成して使用できます。TiDB ベクトル検索インデックスはTiFlashに依存していることに注意してください。ベクトル検索インデックスを使用する前に、 TiFlashノードが TiDB クラスターにデプロイされていることを確認してください。

    詳細については[ドキュメント](/vector-search-overview.md)参照してください。

### DB操作 {#db-operations}

-   BR はログバックアップデータのクライアント側暗号化をサポートします (実験的) [＃55834](https://github.com/pingcap/tidb/issues/55834) @ [トリスタン1900](https://github.com/Tristan1900)

    以前のバージョンの TiDB では、クライアント側で暗号化できるのはスナップショット バックアップ データのみでした。v8.4.0 以降では、ログ バックアップ データもクライアント側で暗号化できます。ログ バックアップ データをバックアップstorageにアップロードする前に、次のいずれかの方法でバックアップ データを暗号化してセキュリティを確保できます。

    -   カスタム固定キーを使用して暗号化する
    -   ローカルディスクに保存されたマスターキーを使用して暗号化する
    -   キー管理サービス (KMS) によって管理されるマスターキーを使用して暗号化する

    詳細については[ドキュメント](/br/br-pitr-manual.md#encrypt-the-log-backup-data)参照してください。

-   BR、クラウドstorageシステムでバックアップ データを復元するときに必要な権限が少なくなります[＃55870](https://github.com/pingcap/tidb/issues/55870) @ [リーヴルス](https://github.com/Leavrth)

    v8.4.0 より前では、 BR は復元中に復元の進行状況に関するチェックポイント情報をバックアップstorageシステムに書き込みます。これらのチェックポイントにより、中断された復元を迅速に再開できます。v8.4.0 以降では、 BR は復元チェックポイント情報をターゲット TiDB クラスターに書き込みます。つまり、 BR は復元中にバックアップ ディレクトリへの読み取りアクセスのみを必要とします。

    詳細については[ドキュメント](/br/backup-and-restore-storages.md#authentication)参照してください。

### 可観測性 {#observability}

-   システムテーブル[＃55542](https://github.com/pingcap/tidb/issues/55542) @ [いびん87](https://github.com/yibin87)のTiDBとTiKVによって消費されたCPU時間を表示します。

    [Top SQLページ](/dashboard/top-sql.md)には[TiDBダッシュボード](/dashboard/dashboard-intro.md) CPU 消費量が多い SQL ステートメントが表示されます。v8.4.0 以降、TiDB はシステム テーブルに CPU 時間消費情報を追加し、セッションまたは SQL の他のメトリックとともに表示します。これにより、複数の観点から CPU 消費量が多い操作を簡単に観察できます。この情報は、インスタンス CPU スパイクやクラスター内の読み取り/書き込みホットスポットなどのシナリオで問題の原因を迅速に特定するのに役立ちます。

    -   [ステートメント要約表](/statement-summary-tables.md) `AVG_TIDB_CPU_TIME`と`AVG_TIKV_CPU_TIME`を加えて、履歴的に個々の SQL ステートメントで消費された平均 CPU 時間を示します。
    -   [INFORMATION_SCHEMA.PROCESSLIST](/information-schema/information-schema-processlist.md)テーブルには`TIDB_CPU`と`TIKV_CPU`追加され、セッションで現在実行されている SQL ステートメントの累積 CPU 消費量が表示されます。
    -   [スロークエリログ](/analyze-slow-queries.md) `Tidb_cpu_time`フィールドと`Tikv_cpu_time`フィールドを追加し、キャプチャされた SQL ステートメントによって消費された CPU 時間を示します。

    デフォルトでは、TiKV によって消費された CPU 時間が表示されます。TiDB によって消費された CPU 時間を収集すると、追加のオーバーヘッド (約 8%) が発生するため、TiDB によって消費された CPU 時間は、 [Top SQL](/dashboard/top-sql.md)が有効な場合にのみ実際の値が表示され、それ以外の場合は常に`0`として表示されます。

    詳細については[`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md)および[`INFORMATION_SCHEMA.SLOW_QUERY`](/information-schema/information-schema-slow-query.md)参照してください。

-   Top SQL は、テーブルまたはデータベースごとに集計された CPU 時間の結果の表示をサポートしています[＃55540](https://github.com/pingcap/tidb/issues/55540) @ [ノルーシュ](https://github.com/nolouch)

    v8.4.0 より前では、 [Top SQL](/dashboard/top-sql.md) CPU 時間を SQL ごとに集計していました。CPU 時間がいくつかの SQL ステートメントによって消費されていない場合、SQL による集計では問題を効果的に特定できません。v8.4.0 以降では、CPU 時間を**テーブル別**または**DB 別に**集計することを選択できます。複数のシステムがあるシナリオでは、新しい集計方法により、特定のシステムからの負荷の変化をより効果的に特定できるため、診断の効率が向上します。

    詳細については[ドキュメント](/dashboard/top-sql.md#use-top-sql)参照してください。

### Security {#security}

-   BRはAWS IMDSv2 [＃16443](https://github.com/tikv/tikv/issues/16443) @ [ピンギュ](https://github.com/pingyu)をサポートします

    TiDB を Amazon EC2 にデプロイする場合、 BR はAWS インスタンス メタデータ サービス バージョン 2 (IMDSv2) をサポートします。EC2 インスタンスを設定して、 BR がインスタンスに関連付けられたIAMロールを使用して Amazon S3 に適切なアクセス権限を付与できるようにすることができます。

    詳細については[ドキュメント](/br/backup-and-restore-storages.md#authentication)参照してください。

### データ移行 {#data-migration}

-   TiCDC Claim-Check は、Kafka メッセージの`value`フィールドのみを外部storage[＃11396](https://github.com/pingcap/tiflow/issues/11396) @ [3エースショーハンド](https://github.com/3AceShowHand)に送信することをサポートします。

    v8.4.0 より前では、Claim-Check 機能が有効になっている場合 ( `large-message-handle-option`を`claim-check`に設定)、TiCDC は大きなメッセージを処理するときに`key`フィールドと`value`フィールドの両方をエンコードして外部storageシステムに保存します。

    v8.4.0 以降、TiCDC は Kafka メッセージの`value`フィールドのみを外部storageに送信することをサポートします。この機能は、非オープン プロトコル プロトコルにのみ適用されます。この機能は、 `claim-check-raw-value`パラメータを設定することで制御できます。

    詳細については[ドキュメント](/ticdc/ticdc-sink-to-kafka.md#send-the-value-field-to-external-storage-only)参照してください。

-   TiCDC は、更新または削除イベント[＃10969](https://github.com/pingcap/tiflow/issues/10969) @ [3エースショーハンド](https://github.com/3AceShowHand)の古い値を検証するためのチェックサム V2 を導入しました。

    v8.4.0 以降、TiDB と TiCDC は、 `ADD COLUMN`または`DROP COLUMN`操作後に更新または削除イベントの古い値を検証する際の Checksum V1 の問題に対処するために、Checksum V2 アルゴリズムを導入しています。v8.4.0 以降で作成されたクラスター、または v8.4.0 にアップグレードされたクラスターの場合、単一行データのチェックサム検証が有効になっていると、TiDB はデフォルトで Checksum V2 を使用します。TiCDC は、Checksum V1 と V2 の両方の処理をサポートしています。この変更は、TiDB と TiCDC の内部実装にのみ影響し、下流の Kafka コンシューマーのチェックサム計算方法には影響しません。

    詳細については[ドキュメント](/ticdc/ticdc-integrity-check.md)参照してください。

## 互換性の変更 {#compatibility-changes}

> **注記：**
>
> このセクションでは、v8.3.0 から現在のバージョン (v8.4.0) にアップグレードするときに知っておく必要のある互換性の変更について説明します。v8.2.0 以前のバージョンから現在のバージョンにアップグレードする場合は、中間バージョンで導入された互換性の変更も確認する必要がある可能性があります。

### システム変数 {#system-variables}

| 変数名                                                                                                                             | タイプを変更   | 説明                                                                                                                                                                                                                                                                                                             |
| ------------------------------------------------------------------------------------------------------------------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `log_bin`                                                                                                                       | 削除されました  | v8.4.0 では、 [TiDBBinlog](https://docs.pingcap.com/tidb/v8.3/tidb-binlog-overview)削除されました。この変数は、TiDB Binlogが使用されているかどうかを示し、v8.4.0 以降では削除されます。                                                                                                                                                                    |
| `sql_log_bin`                                                                                                                   | 削除されました  | v8.4.0 では、 [TiDBBinlog](https://docs.pingcap.com/tidb/v8.3/tidb-binlog-overview)削除されました。この変数は、変更を TiDB Binlogに書き込むかどうかを示し、v8.4.0 以降では削除されます。                                                                                                                                                                   |
| [`tidb_enable_global_index`](/system-variables.md#tidb_enable_global_index-new-in-v760)                                         | 非推奨      | v8.4.0 では、この変数は非推奨です。その値はデフォルト値`ON`に固定されます。つまり、 [グローバルインデックス](/partitioned-table.md#global-indexes)デフォルトで有効になります。グローバル インデックスを作成するには、 `CREATE TABLE`または`ALTER TABLE`を実行するときに、対応する列にキーワード`GLOBAL`を追加するだけです。                                                                                                     |
| [`tidb_enable_list_partition`](/system-variables.md#tidb_enable_list_partition-new-in-v50)                                      | 非推奨      | v8.4.0 では、この変数は非推奨です。その値はデフォルト値`ON`に固定されます。つまり、デフォルトでは[リストの分割](/partitioned-table.md#list-partitioning)が有効になります。                                                                                                                                                                                               |
| [`tidb_enable_table_partition`](/system-variables.md#tidb_enable_table_partition)                                               | 非推奨      | v8.4.0 では、この変数は非推奨です。その値はデフォルト値`ON`に固定されます。つまり、デフォルトでは[テーブルパーティション](/partitioned-table.md)が有効になります。                                                                                                                                                                                                            |
| [`tidb_analyze_partition_concurrency`](/system-variables.md#tidb_analyze_partition_concurrency)                                 | 修正済み     | 値の範囲を`[1, 18446744073709551615]`から`[1, 128]`に変更します。                                                                                                                                                                                                                                                            |
| [`tidb_enable_inl_join_inner_multi_pattern`](/system-variables.md#tidb_enable_inl_join_inner_multi_pattern-new-in-v700)         | 修正済み     | デフォルト値を`OFF`から`ON`に変更します。v8.4.0 以降では、内部テーブルに`Selection` 、 `Aggregation` 、または`Projection`の演算子がある場合、インデックス結合がデフォルトでサポートされます。                                                                                                                                                                                     |
| [`tidb_opt_prefer_range_scan`](/system-variables.md#tidb_opt_prefer_range_scan-new-in-v50)                                      | 修正済み     | デフォルト値を`OFF`から`ON`に変更します。統計のないテーブル (疑似統計) または空のテーブル (統計がゼロ) の場合、オプティマイザは完全なテーブル スキャンよりも間隔スキャンを優先します。                                                                                                                                                                                                           |
| [`tidb_scatter_region`](/system-variables.md#tidb_scatter_region)                                                               | 修正済み     | v8.4.0 より前では、そのタイプはブール型で、 `ON`と`OFF`のみをサポートしており、新しく作成されたテーブルのリージョンは、有効にした後はテーブル レベルの分散のみをサポートします。v8.4.0 以降では、 `SESSION`スコープが追加され、タイプがブール型から列挙型に変更され、デフォルト値が`OFF`から null に変更され、オプションの値`TABLE`と`GLOBAL`が追加されました。さらに、バッチでの高速テーブル作成中にリージョンが不均一に分散されることで発生する TiKV OOM の問題を回避するために、クラスター レベルの分散ポリシーがサポートされるようになりました。 |
| [`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-new-in-v800)                                             | 修正済み     | デフォルト値を`0`から`536870912` (512 MiB) に変更し、この機能がデフォルトで有効になっていることを示します。許可される最小値は`67108864` (64 MiB) に設定されています。                                                                                                                                                                                                      |
| [`tidb_auto_analyze_concurrency`](/system-variables.md#tidb_auto_analyze_concurrency-new-in-v840)                               | 新しく追加された | 単一の自動統計収集タスク内の同時実行性を設定します。v8.4.0 より前では、この同時実行性は`1`に固定されています。統計収集タスクを高速化するには、クラスターの使用可能なリソースに基づいてこの同時実行性を増やすことができます。                                                                                                                                                                                            |
| [`tidb_enable_instance_plan_cache`](/system-variables.md#tidb_enable_instance_plan_cache-new-in-v840)                           | 新しく追加された | インスタンス プラン キャッシュ機能を有効にするかどうかを制御します。                                                                                                                                                                                                                                                                            |
| [`tidb_enable_stats_owner`](/system-variables.md#tidb_enable_stats_owner-new-in-v840)                                           | 新しく追加された | 対応する TiDB インスタンスが自動統計更新タスクを実行できるかどうかを制御します。                                                                                                                                                                                                                                                                    |
| [`tidb_hash_join_version`](/system-variables.md#tidb_hash_join_version-new-in-v840)                                             | 新しく追加された | TiDB がハッシュ結合演算子の最適化バージョンを使用するかどうかを制御します。デフォルト値`legacy`は、最適化バージョンが使用されないことを意味します。 `optimized`に設定すると、TiDB はハッシュ結合演算子の実行時に最適化バージョンを使用して、ハッシュ結合のパフォーマンスを向上させます。                                                                                                                                                    |
| [`tidb_instance_plan_cache_max_size`](/system-variables.md#tidb_instance_plan_cache_max_size-new-in-v840)                       | 新しく追加された | インスタンス プラン キャッシュの最大メモリ使用量を設定します。                                                                                                                                                                                                                                                                               |
| [`tidb_instance_plan_cache_reserved_percentage`](/system-variables.md#tidb_instance_plan_cache_reserved_percentage-new-in-v840) | 新しく追加された | メモリの削除後にインスタンス プラン キャッシュ用に予約されるアイドルメモリの割合を制御します。                                                                                                                                                                                                                                                               |
| [`tidb_pre_split_regions`](/system-variables.md#tidb_pre_split_regions-new-in-v840)                                             | 新しく追加された | v8.4.0 より前では、新しく作成されたテーブルの行分割スライスのデフォルト数を設定するには、 `CREATE TABLE` SQL ステートメントごとに`PRE_SPLIT_REGIONS`宣言する必要がありましたが、多数のテーブルを同様に構成する必要がある場合は複雑になります。この変数は、このような問題を解決するために導入されました。このシステム変数を`GLOBAL`または`SESSION`レベルに設定して、使いやすさを向上させることができます。                                                                           |
| [`tidb_shard_row_id_bits`](/system-variables.md#tidb_shard_row_id_bits-new-in-v840)                                             | 新しく追加された | v8.4.0 より前では、新しく作成されたテーブルの行 ID のスライスのデフォルト数を設定するには、 `CREATE TABLE`または`ALTER TABLE` SQL ステートメントごとに`SHARD_ROW_ID_BITS`宣言する必要がありましたが、多数のテーブルを同様に構成する必要がある場合は複雑になります。この変数は、このような問題を解決するために導入されました。このシステム変数を`GLOBAL`または`SESSION`レベルに設定して、使いやすさを向上させることができます。                                                        |
| [`tidb_tso_client_rpc_mode`](/system-variables.md#tidb_tso_client_rpc_mode-new-in-v840)                                         | 新しく追加された | TiDB が PD に TSO RPC 要求を送信するモードを切り替えます。このモードは、TSO RPC 要求を並列処理できるかどうかを決定し、各 TS 取得操作のバッチ待機に費やされる時間に影響します。これにより、特定のシナリオでのクエリ実行中に TS を取得するための待機時間を短縮できます。                                                                                                                                                           |

### コンフィグレーションパラメータ {#configuration-parameters}

| コンフィグレーションファイルまたはコンポーネント | コンフィグレーションパラメータ                                                                                                          | タイプを変更   | 説明                                                                                                                                                                         |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------ | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ティビ                      | [`grpc-keepalive-time`](/tidb-configuration-file.md#grpc-keepalive-time)                                                 | 修正済み     | 最小値`1`を追加します。                                                                                                                                                              |
| ティビ                      | [`grpc-keepalive-timeout`](/tidb-configuration-file.md#grpc-keepalive-timeout)                                           | 修正済み     | v8.4.0 より前では、このパラメータのデータ型は INT で、最小値は`1`です。v8.4.0 以降では、データ型は FLOAT64 に変更され、最小値は`0.05`なります。ネットワーク ジッターが頻繁に発生するシナリオでは、値を小さくして再試行間隔を短くすることで、ネットワーク ジッターによるパフォーマンスへの影響を軽減できます。 |
| ティビ                      | [`tidb_enable_stats_owner`](/tidb-configuration-file.md#tidb_enable_stats_owner-new-in-v840)                             | 新しく追加された | 対応する TiDB インスタンスが自動統計更新タスクを実行できるかどうかを制御します。                                                                                                                                |
| ティクヴ                     | [`region-split-keys`](/tikv-configuration-file.md#region-split-keys)                                                     | 修正済み     | デフォルト値を`"960000"`から`"2560000"`に変更します。                                                                                                                                      |
| ティクヴ                     | [`region-split-size`](/tikv-configuration-file.md#region-split-size)                                                     | 修正済み     | デフォルト値を`"96MiB"`から`"256MiB"`に変更します。                                                                                                                                        |
| ティクヴ                     | [`sst-max-size`](/tikv-configuration-file.md#sst-max-size)                                                               | 修正済み     | デフォルト値を`"144MiB"`から`"384MiB"`に変更します。                                                                                                                                       |
| ティクヴ                     | [`pessimistic-txn.in-memory-instance-size-limit`](/tikv-configuration-file.md#in-memory-instance-size-limit-new-in-v840) | 新しく追加された | TiKV インスタンス内のメモリ内悲観的ロックのメモリ使用量制限を制御します。この制限を超えると、TiKV は悲観的ロックを永続的に書き込みます。                                                                                                  |
| ティクヴ                     | [`pessimistic-txn.in-memory-peer-size-limit`](/tikv-configuration-file.md#in-memory-peer-size-limit-new-in-v840)         | 新しく追加された | リージョン内のメモリ内悲観的ロックのメモリ使用量制限を制御します。この制限を超えると、TiKV は悲観的ロックを永続的に書き込みます。                                                                                                        |
| ティクヴ                     | [`raft-engine.spill-dir`](/tikv-configuration-file.md#spill-dir-new-in-v840)                                             | 新しく追加された | Raftログ ファイルのマルチディスクstorageをサポートするために、TiKV インスタンスがRaftログ ファイルを保存するセカンダリ ディレクトリを制御します。                                                                                       |
| ティクヴ                     | [`resource-control.priority-ctl-strategy`](/tikv-configuration-file.md#priority-ctl-strategy-new-in-v840)                | 新しく追加された | 優先度の低いタスクの管理ポリシーを制御します。TiKV は、優先度の低いタスクにフロー制御を追加することで、優先度の高いタスクが最初に実行されるようにします。                                                                                            |
| PD                       | [`cert-allowed-cn`](/enable-tls-between-components.md#verify-component-callers-identity)                                 | 修正済み     | v8.4.0 以降では、複数の`Common Names`設定がサポートされます。v8.4.0 より前では、 `Common Name` 1 つしか設定できません。                                                                                         |
| PD                       | [`max-merge-region-keys`](/pd-configuration-file.md#max-merge-region-keys)                                               | 修正済み     | デフォルト値を`200000`から`540000`に変更します。                                                                                                                                           |
| PD                       | [`max-merge-region-size`](/pd-configuration-file.md#max-merge-region-size)                                               | 修正済み     | デフォルト値を`20`から`54`に変更します。                                                                                                                                                   |
| TiFlash                  | [`storage.format_version`](/tiflash/tiflash-configuration.md)                                                            | 修正済み     | ベクター インデックスの作成とstorageをサポートするために、デフォルトのTiFlashstorageフォーマットのバージョンを`5`から`7`に変更します。このフォーマットの変更により、v8.4.0 以降のバージョンにアップグレードされたTiFlashクラスターは、以前のバージョンへのインプレース ダウングレードをサポートしません。 |
| TiDBBinlog               | `--enable-binlog`                                                                                                        | 削除されました  | v8.4.0 では、 [TiDBBinlog](https://docs.pingcap.com/tidb/v8.3/tidb-binlog-overview)削除されました。このパラメータは、TiDBbinlog生成を有効にするかどうかを制御し、v8.4.0 以降では削除されます。                             |
| ティCDC                    | [`claim-check-raw-value`](/ticdc/ticdc-sink-to-kafka.md#send-the-value-field-to-external-storage-only)                   | 新しく追加された | TiCDC が Kafka メッセージの`value`のフィールドのみを外部storageに送信するかどうかを制御します。この機能は、非オープン プロトコル シナリオにのみ適用されます。                                                                              |
| TiDB Lightning           | [`logical-import-prep-stmt`](/tidb-lightning/tidb-lightning-configuration.md)                                            | 新しく追加された | 論理インポート モードでは、このパラメータは、パフォーマンスを向上させるために準備されたステートメントとステートメント キャッシュを使用するかどうかを制御します。デフォルト値は`false`です。                                                                         |
| BR                       | [`--log.crypter.key`](/br/br-pitr-manual.md#encrypt-the-log-backup-data)                                                 | 新しく追加された | ログ バックアップ データの暗号化キーを 16 進文字列形式で指定します。アルゴリズム`aes128-ctr`の場合は 128 ビット (16 バイト) のキー、アルゴリズム`aes192-ctr`の場合は 24 バイトのキー、アルゴリズム`aes256-ctr`の場合は 32 バイトのキーです。                      |
| BR                       | [`--log.crypter.key-file`](/br/br-pitr-manual.md#encrypt-the-log-backup-data)                                            | 新しく追加された | ログバックアップデータのキーファイルを指定します。 `crypter.key`を渡さずに、キーが格納されているファイルパスをパラメータとして直接渡すこともできます。                                                                                         |
| BR                       | [`--log.crypter.method`](/br/br-pitr-manual.md#encrypt-the-log-backup-data)                                              | 新しく追加された | ログ バックアップ データの暗号化アルゴリズムを指定します。指定できる値は`aes128-ctr` 、 `aes192-ctr` 、または`aes256-ctr`です。既定値は`plaintext`で、データは暗号化されないことを示します。                                                   |
| BR                       | [`--master-key`](/br/br-pitr-manual.md#encrypt-the-log-backup-data)                                                      | 新しく追加された | ログ バックアップ データのマスター キーを指定します。ローカル ディスクに保存されているマスター キー、またはクラウド キー管理サービス (KMS) によって管理されるマスター キーを使用できます。                                                                       |
| BR                       | [`--master-key-crypter-method`](/br/br-pitr-manual.md#encrypt-the-log-backup-data)                                       | 新しく追加された | ログ バックアップ データのマスター キーに基づく暗号化アルゴリズムを指定します。指定できる値は`aes128-ctr` 、 `aes192-ctr` 、または`aes256-ctr`です。既定値は`plaintext`で、データは暗号化されないことを示します。                                        |

## オフラインパッケージの変更 {#offline-package-changes}

v8.4.0 以降では、 `TiDB-community-toolkit` [バイナリパッケージ](/binary-package.md)から次のコンテンツが削除されます。

-   `pump-{version}-linux-{arch}.tar.gz`
-   `drainer-{version}-linux-{arch}.tar.gz`
-   `binlogctl`
-   `arbiter`

## オペレーティング システムとプラットフォームの要件の変更 {#operating-system-and-platform-requirement-changes}

TiDB をアップグレードする前に、オペレーティング システムのバージョンが[OSおよびプラットフォームの要件](/hardware-and-software-requirements.md#os-and-platform-requirements)を満たしていることを確認してください。

-   [CentOS Linux のサポート終了](https://www.centos.org/centos-linux-eol/)によると、CentOS Linux 7 のアップストリームサポートは 2024 年 6 月 30 日に終了します。TiDB は、8.4 DMR バージョンから CentOS 7 のサポートを終了します。Rocky Linux 9.1 以降のバージョンを使用することをお勧めします。CentOS 7 上の TiDB クラスターを v8.4.0 以降にアップグレードすると、クラスターが使用できなくなります。
-   [Red Hat Enterprise Linux ライフサイクル](https://access.redhat.com/support/policy/updates/errata/#Life_Cycle_Dates)によると、Red Hat Enterprise Linux 7 のメンテナンスサポートは 2024 年 6 月 30 日に終了します。TiDB は 8.4 DMR バージョンから Red Hat Enterprise Linux 7 のサポートを終了します。Rocky Linux 9.1 以降のバージョンを使用することをお勧めします。Red Hat Enterprise Linux 7 上の TiDB クラスターを v8.4.0 以降にアップグレードすると、クラスターが使用できなくなります。

## 削除された機能 {#removed-features}

-   v8.4.0 以降では次の機能が削除されます。

    -   v8.4.0 では、 [TiDBBinlog](https://docs.pingcap.com/tidb/v8.3/tidb-binlog-overview)​​削除されました。v8.3.0 以降では、 TiDB Binlog は完全に非推奨です。増分データ レプリケーションの場合は、代わりに[ティCDC](/ticdc/ticdc-overview.md)使用します。ポイントインタイム リカバリ (PITR) の場合は、 [ピトル](/br/br-pitr-guide.md)使用します。TiDB クラスターを v8.4.0 以降のバージョンにアップグレードする前に、必ず TiCDC と PITR に切り替えてください。

-   以下の機能は将来のバージョンで削除される予定です:

    -   v8.0.0 以降、 TiDB Lightning物理インポート モードの[競合検出の旧バージョン](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#the-old-version-of-conflict-detection-deprecated-in-v800)戦略が廃止され、 [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)パラメータを使用して論理インポート モードと物理インポート モードの両方の競合検出戦略を制御できるようになりました。競合検出の旧バージョンの[`duplicate-resolution`](/tidb-lightning/tidb-lightning-configuration.md)パラメータは、将来のリリースで削除される予定です。

## 廃止された機能 {#deprecated-features}

以下の機能は将来のバージョンで廃止される予定です。

-   TiDB では、統計を自動的に収集するタスクの順序を最適化するために優先キューを有効にするかどうかを制御するためのシステム変数[`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-new-in-v800)が導入されています。将来のリリースでは、統計を自動的に収集するタスクを順序付ける唯一の方法は優先キューになるため、このシステム変数は非推奨になります。
-   TiDB は、v7.5.0 でシステム変数[`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-new-in-v750)を導入しました。これを使用して、TiDB がパーティション統計の非同期マージを使用して OOM の問題を回避するように設定できます。将来のリリースでは、パーティション統計は非同期にマージされるため、このシステム変数は非推奨になります。
-   以降のリリースでは[実行計画バインディングの自動進化](/sql-plan-management.md#baseline-evolution)再設計する予定であり、関連する変数と動作が変更されます。
-   v8.0.0 では、TiDB は、同時 HashAgg アルゴリズムのディスク スピルをサポートするかどうかを制御する[`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-new-in-v800)システム変数を導入します。将来のバージョンでは、 [`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-new-in-v800)システム変数は非推奨になります。
-   TiDB Lightningパラメータ[`conflict.max-record-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)は、将来のリリースで廃止される予定であり、その後削除されます。このパラメータは[`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)に置き換えられます。これは、競合するレコードの最大数が、単一のインポート タスクで許容できる競合するレコードの最大数と一致することを意味します。
-   v6.3.0 以降、パーティション テーブルはデフォルトで[動的剪定モード](/partitioned-table.md#dynamic-pruning-mode)使用します。静的プルーニング モードと比較して、動的プルーニング モードは IndexJoin やプラン キャッシュなどの機能をサポートし、パフォーマンスが向上します。したがって、静的プルーニング モードは非推奨になります。

## 改善点 {#improvements}

-   ティビ

    -   大量のデータをスキャンする際のBatchCopタスク構築の効率を最適化[＃55915](https://github.com/pingcap/tidb/issues/55915) [＃55413](https://github.com/pingcap/tidb/issues/55413) @ [うわー](https://github.com/wshwsh12)
    -   トランザクションのバッファを最適化して、トランザクションの書き込みレイテンシーと TiDB CPU 使用率を削減します[＃55287](https://github.com/pingcap/tidb/issues/55287) @ [あなた06](https://github.com/you06)
    -   システム変数`tidb_dml_type`が`"bulk"` [＃50215](https://github.com/pingcap/tidb/issues/50215) @ [エキシウム](https://github.com/ekexium)に設定されている場合にDMLステートメントの実行パフォーマンスを最適化します。
    -   [オプティマイザー修正制御 47400](/optimizer-fix-controls.md#47400-new-in-v840)使用して、オプティマイザが`estRows`から`1`の推定最小値を制限するかどうかを制御します。これは、Oracle や DB2 [＃47400](https://github.com/pingcap/tidb/issues/47400) @ [テリー・パーセル](https://github.com/terry1purcell)などのデータベースと一致しています。
    -   多数の同時書き込みによるオーバーヘッドを削減するために、 [`mysql.tidb_runaway_queries`](/mysql-schema/mysql-schema.md#system-tables-related-to-runaway-queries)ログ テーブルに書き込み制御を追加します[＃54434](https://github.com/pingcap/tidb/issues/54434) @ [ヒューシャープ](https://github.com/HuSharp)
    -   内部テーブルに`Selection` 、 `Projection` 、または`Aggregation`演算子がある場合、デフォルトでインデックス結合をサポートします[＃47233](https://github.com/pingcap/tidb/issues/47233) @ [ウィノロス](https://github.com/winoros)
    -   特定のシナリオで`DELETE`操作に対して TiKV から取得される列の詳細の数を減らし、これらの操作のリソース オーバーヘッドを削減します[＃38911](https://github.com/pingcap/tidb/issues/38911) @ [ウィノロス](https://github.com/winoros)
    -   システム変数`tidb_auto_analyze_concurrency` [＃53460](https://github.com/pingcap/tidb/issues/53460) @ [ホーキングレイ](https://github.com/hawkingrei)を使用して、単一の自動統計収集タスク内での同時実行の設定をサポートします。
    -   多数の列を持つテーブルをクエリする際のパフォーマンスを向上させるために、内部関数のロジックを最適化します[＃52112](https://github.com/pingcap/tidb/issues/52112) @ [ラスティン170506](https://github.com/Rustin170506)
    -   フィルター条件を`a = 1 AND (a > 1 OR (a = 1 AND b = 2))` ～ `a = 1 AND b = 2` [＃56005](https://github.com/pingcap/tidb/issues/56005) @ [ガザルファミリー](https://github.com/ghazalfamilyusa)のように簡略化する
    -   最適でない実行プランのリスクが高いシナリオでは、コストモデルでテーブルスキャンのコストを増やし、オプティマイザがインデックス[＃56012](https://github.com/pingcap/tidb/issues/56012) @ [テリー・パーセル](https://github.com/terry1purcell)を優先するようにします。
    -   TiDBは2つの引数のバリアント`MID(str, pos)` [＃52420](https://github.com/pingcap/tidb/issues/52420) @ [ドヴェーデン](https://github.com/dveeden)をサポートしています
    -   非バイナリ主キー[＃55660](https://github.com/pingcap/tidb/issues/55660) @ [lcwangchao](https://github.com/lcwangchao)を持つテーブルの TTL タスクの分割をサポート
    -   システムメタデータ関連ステートメントのパフォーマンスを最適化する[＃50305](https://github.com/pingcap/tidb/issues/50305) @ [うわー](https://github.com/ywqzzy) @ [タンジェンタ](https://github.com/tangenta) @ [ジョーチェン](https://github.com/joechenrh) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)
    -   自動分析操作用の新しい優先キューを実装して、分析パフォーマンスを向上させ、キュー[＃55906](https://github.com/pingcap/tidb/issues/55906) @ [ラスティン170506](https://github.com/Rustin170506)の再構築コストを削減します。
    -   統計モジュールが DDL イベントをサブスクライブできるように DDL 通知機能を導入する[＃55722](https://github.com/pingcap/tidb/issues/55722) @ [ふーふー](https://github.com/fzzf678) @ [ランス6716](https://github.com/lance6716) @ [ラスティン170506](https://github.com/Rustin170506)
    -   TiDB のアップグレード中に新しい TiDB ノードに DDL 所有権を強制的に引き継がせ、古い TiDB ノードが所有権[＃51285](https://github.com/pingcap/tidb/pull/51285) @ [翻訳:](https://github.com/wjhuang2016)を引き継ぐことによる互換性の問題を回避します。
    -   クラスターレベルの散布リージョン[＃8424](https://github.com/tikv/pd/issues/8424) @ [リバー2000i](https://github.com/River2000i)をサポート

-   ティクヴ

    -   リージョン[＃17309](https://github.com/tikv/tikv/issues/17309) @ [リクササシネーター](https://github.com/LykxSassinator)が多すぎることによる余分なオーバーヘッドを回避するために、リージョンのデフォルト値を 96 MiB から 256 MiB に増やします。
    -   リージョンまたは TiKV インスタンス内のメモリ内悲観的ロックのメモリ使用量制限の設定をサポートします。ホット書き込みシナリオで多数の悲観的ロックが発生する場合は、設定によってメモリ制限を増やすことができます。これにより、悲観的ロックがディスクに書き込まれることで[＃17542](https://github.com/tikv/tikv/issues/17542)する CPU および I/O オーバーヘッドを回避できます。1 @ [翻訳](https://github.com/cfzjywxk)
    -   Raft Engineに新しい`spill-dir`設定項目を導入し、 Raftログのマルチディスクstorageをサポートします。ホームディレクトリ（ `dir` ）があるディスクの容量が不足すると、 Raft Engineは自動的に新しいログを`spill-dir`に書き込み、システムの継続的な動作を保証します[＃17356](https://github.com/tikv/tikv/issues/17356) @ [リクササシネーター](https://github.com/LykxSassinator)
    -   RocksDB の圧縮トリガー メカニズムを最適化し、多数の DELETE バージョン[＃17269](https://github.com/tikv/tikv/issues/17269) @ [アンドレ・ムーシュ](https://github.com/AndreMouche)を処理するときにディスク領域の再利用を高速化します。
    -   書き込み操作のフロー制御構成を動的に変更するサポート[＃17395](https://github.com/tikv/tikv/issues/17395) @ [栄光](https://github.com/glorv)
    -   空のテーブルと小さなリージョン[＃17376](https://github.com/tikv/tikv/issues/17376) @ [リクササシネーター](https://github.com/LykxSassinator)シナリオでのリージョンマージの速度を向上
    -   [パイプライン化された DML](https://github.com/pingcap/tidb/blob/release-8.4/docs/design/2024-01-09-pipelined-DML.md)resolved-ts を長期間ブロックするのを防ぐ[＃17459](https://github.com/tikv/tikv/issues/17459) @ [エキシウム](https://github.com/ekexium)

-   PD

    -   TiDB Lightning [＃7853](https://github.com/tikv/pd/issues/7853) @ [ok江](https://github.com/okJiang)によるデータインポート中に TiKV ノードの正常なオフラインをサポート
    -   `pd-ctl`コマンド[＃8379](https://github.com/tikv/pd/issues/8379) @ [ok江](https://github.com/okJiang)で`scatter-range`を`scatter-range-scheduler`に名前変更
    -   `grant-hot-leader-scheduler` [＃4903](https://github.com/tikv/pd/issues/4903) @ [翻訳者](https://github.com/lhy1024)の競合検出を追加

-   TiFlash

    -   `LENGTH()`と`ASCII()`関数の実行効率を最適化[＃9344](https://github.com/pingcap/tiflash/issues/9344) @ [翻訳者](https://github.com/xzhangxian1008)
    -   分散storageとコンピューティング要求を処理するときにTiFlash が作成する必要があるスレッドの数を減らし、大量のそのような要求を処理するときにTiFlashコンピューティングノードのクラッシュを回避するのに役立ちます[＃9334](https://github.com/pingcap/tiflash/issues/9334) @ [ジンヘリン](https://github.com/JinheLin)
    -   パイプライン実行モデル[＃8869](https://github.com/pingcap/tiflash/issues/8869) @ [シーライズ](https://github.com/SeaRise)におけるタスク待機機構の強化
    -   JOIN 演算子のキャンセル メカニズムを改善し、JOIN 演算子がキャンセル要求にタイムリーに応答できるようにします[＃9430](https://github.com/pingcap/tiflash/issues/9430) @ [風の話し手](https://github.com/windtalker)

-   ツール

    -   バックアップと復元 (BR)

        -   `split-table`と`split-region-on-table`構成項目が`false` (デフォルト値) [＃53532](https://github.com/pingcap/tidb/issues/53532) @ [リーヴルス](https://github.com/Leavrth)であるクラスターにデータを復元する場合、復元速度を向上させるためにテーブルによるリージョンの分割を無効にします。
        -   デフォルトで`RESTORE`の SQL ステートメントを使用して空でないクラスターへの完全なデータ復元を無効にする[＃55087](https://github.com/pingcap/tidb/issues/55087) @ [ボーンチェンジャー](https://github.com/BornChanger)

## バグ修正 {#bug-fixes}

-   ティビ

    -   `tidb_restricted_read_only`変数が`true` [＃53822](https://github.com/pingcap/tidb/issues/53822) [＃55373](https://github.com/pingcap/tidb/issues/55373) @ [定義2014](https://github.com/Defined2014)に設定されている場合にデッドロックが発生する可能性がある問題を修正しました
    -   TiDB が正常なシャットダウン中に自動コミットトランザクションの完了を待たない問題を修正[＃55464](https://github.com/pingcap/tidb/issues/55464) @ [ヤンケオ](https://github.com/YangKeao)
    -   TTLジョブ実行中に`tidb_ttl_delete_worker_count`の値を減らすとジョブが[＃55561](https://github.com/pingcap/tidb/issues/55561) @ [lcwangchao](https://github.com/lcwangchao)で完了しなくなる問題を修正
    -   テーブルのインデックスに生成された列が含まれている場合、 `ANALYZE`ステートメント[＃55438](https://github.com/pingcap/tidb/issues/55438) @ [ホーキングレイ](https://github.com/hawkingrei)を介してテーブルの統計情報を収集するときに`Unknown column 'column_name' in 'expression'`エラーが発生する可能性がある問題を修正しました。
    -   冗長なコードを削減するために、統計に関連する不要な設定を廃止する[＃55043](https://github.com/pingcap/tidb/issues/55043) @ [ラスティン170506](https://github.com/Rustin170506)
    -   相関サブクエリと CTE [＃55551](https://github.com/pingcap/tidb/issues/55551) @ [グオシャオゲ](https://github.com/guo-shaoge)含むクエリを実行すると、TiDB がハングしたり、誤った結果が返されたりする問題を修正しました。
    -   `lite-init-stats`無効にすると統計が同期的にロードされない可能性がある問題を修正[＃54532](https://github.com/pingcap/tidb/issues/54532) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   `UPDATE`または`DELETE`ステートメントに再帰 CTE が含まれている場合、ステートメントがエラーを報告したり、 [＃55666](https://github.com/pingcap/tidb/issues/55666) @ [時間と運命](https://github.com/time-and-fate)有効にならない可能性がある問題を修正しました。
    -   ウィンドウ関数を含むSQLバインディングが場合によっては有効にならない可能性がある問題を修正[＃55981](https://github.com/pingcap/tidb/issues/55981) @ [ウィノロス](https://github.com/winoros)
    -   統計[＃55684](https://github.com/pingcap/tidb/issues/55684) @ [ウィノロス](https://github.com/winoros)を初期化するときに、非バイナリ照合順序の文字列列の統計が読み込まれない可能性がある問題を修正しました。
    -   クエリ条件`column IS NULL` [＃56116](https://github.com/pingcap/tidb/issues/56116) @ [ホーキングレイ](https://github.com/hawkingrei)で一意のインデックスにアクセスするときに、オプティマイザが行数を誤って 1 と見積もる問題を修正しました。
    -   クエリに`(... AND ...) OR (... AND ...) ...` [＃54323](https://github.com/pingcap/tidb/issues/54323) @ [時間と運命](https://github.com/time-and-fate)のようなフィルタ条件が含まれている場合、オプティマイザが行数の推定に最適な複数列の統計情報を使用しない問題を修正しました。
    -   クエリに利用可能なインデックスマージ実行プラン[＃56217](https://github.com/pingcap/tidb/issues/56217) @ [アイリンキッド](https://github.com/AilinKid)がある場合に`read_from_storage`ヒントが有効にならない可能性がある問題を修正しました。
    -   `IndexNestedLoopHashJoin` [＃49692](https://github.com/pingcap/tidb/issues/49692) @ [ソロッツ](https://github.com/solotzg)のデータ競合問題を修正
    -   `INFORMATION_SCHEMA.STATISTICS`テーブルの`SUB_PART`値が`NULL` [＃55812](https://github.com/pingcap/tidb/issues/55812) @ [定義2014](https://github.com/Defined2014)になる問題を修正しました
    -   DML文にネストされた生成列[＃53967](https://github.com/pingcap/tidb/issues/53967) @ [翻訳:](https://github.com/wjhuang2016)が含まれている場合にエラーが発生する問題を修正
    -   除算演算で最小表示長を持つ整数型のデータにより、除算結果が[＃55837](https://github.com/pingcap/tidb/issues/55837) @ [風の話し手](https://github.com/windtalker)でオーバーフローする可能性がある問題を修正しました。
    -   TopN演算子に続く演算子がメモリ制限を超えたときにフォールバックアクションをトリガーできない問題を修正[＃56185](https://github.com/pingcap/tidb/issues/56185) @ [翻訳者](https://github.com/xzhangxian1008)
    -   ソート演算子の`ORDER BY`列目に定数[＃55344](https://github.com/pingcap/tidb/issues/55344) @ [翻訳者](https://github.com/xzhangxian1008)が含まれている場合にスタックする問題を修正しました。
    -   インデックスを追加するときに、PDリーダーを強制終了した後に`8223 (HY000)`エラーが発生し、テーブル内のデータが不整合になる問題を修正しました[＃55488](https://github.com/pingcap/tidb/issues/55488) @ [タンジェンタ](https://github.com/tangenta)
    -   履歴 DDL ジョブ[＃55711](https://github.com/pingcap/tidb/issues/55711) @ [ジョッカウ](https://github.com/joccau)に関する情報をリクエストすると、DDL 履歴ジョブが多すぎるために OOM が発生する問題を修正しました。
    -   グローバルソートが有効でリージョンサイズが96 MiB [＃55374](https://github.com/pingcap/tidb/issues/55374) @ [ランス6716](https://github.com/lance6716)を超えると`IMPORT INTO`実行が停止する問題を修正
    -   一時テーブルで`IMPORT INTO`実行すると TiDB がクラッシュする問題を修正[＃55970](https://github.com/pingcap/tidb/issues/55970) @ [D3ハンター](https://github.com/D3Hunter)
    -   ユニークインデックスを追加すると`duplicate entry`エラー[＃56161](https://github.com/pingcap/tidb/issues/56161) @ [タンジェンタ](https://github.com/tangenta)が発生する問題を修正
    -   TiKV が 810 秒以上ダウンしている場合にTiDB Lightning がすべての KV ペアを取り込まず、テーブル[＃55808](https://github.com/pingcap/tidb/issues/55808) @ [ランス6716](https://github.com/lance6716)のデータが不整合になる問題を修正しました。
    -   `CREATE TABLE LIKE`ステートメントがキャッシュされたテーブル[＃56134](https://github.com/pingcap/tidb/issues/56134) @ [天菜まお](https://github.com/tiancaiamao)に使用できない問題を修正
    -   CTE [＃56198](https://github.com/pingcap/tidb/pull/56198) @ [ドヴェーデン](https://github.com/dveeden)の`FORMAT()`式に関する紛らわしい警告メッセージを修正
    -   パーティションテーブル[＃56094](https://github.com/pingcap/tidb/issues/56094) @ [ミョンス](https://github.com/mjonss)を作成するときに、列の型制限が`CREATE TABLE`と`ALTER TABLE`間で一致しない問題を修正しました。
    -   `INFORMATION_SCHEMA.RUNAWAY_WATCHES`表[＃54770](https://github.com/pingcap/tidb/issues/54770) @ [ヒューシャープ](https://github.com/HuSharp)の誤った時間タイプを修正

-   ティクヴ

    -   マスターキーがキー管理サービス (KMS) [＃17410](https://github.com/tikv/tikv/issues/17410) @ [いいえ](https://github.com/hhwyt)に保存されている場合にマスターキーのローテーションが妨げられる問題を修正しました
    -   大きなテーブルやパーティションを削除した後に発生する可能性のあるトラフィック制御の問題を修正[＃17304](https://github.com/tikv/tikv/issues/17304) @ [コナー1996](https://github.com/Connor1996)
    -   古いレプリカがRaftスナップショットを処理するときに、遅い分割操作と新しいレプリカ[＃17469](https://github.com/tikv/tikv/issues/17469) @ [ビシェン](https://github.com/hbisheng)の即時削除によってトリガーされ、TiKV がpanicになる可能性がある問題を修正しました。

-   TiFlash

    -   テーブルに無効な文字[＃9461](https://github.com/pingcap/tiflash/issues/9461) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)を含むデフォルト値を持つビット型列が含まれている場合に、 TiFlash がテーブル スキーマを解析できない問題を修正しました。
    -   複数のリージョンがスナップショット[＃9329](https://github.com/pingcap/tiflash/issues/9329) @ [カルビンネオ](https://github.com/CalvinNeo)を同時に適用しているときに発生する誤ったリージョン重複チェックの失敗によりTiFlash がpanicになる可能性がある問題を修正しました。
    -   TiFlashでサポートされていない一部の JSON関数がTiFlash [＃9444](https://github.com/pingcap/tiflash/issues/9444) @ [風の話し手](https://github.com/windtalker)にプッシュダウンされる問題を修正しました

-   ツール

    -   バックアップと復元 (BR)

        -   TiDBノードが停止したときに監視のPITRチェックポイント間隔が異常に増加し、実際の状況を反映しない問題を修正[＃42419](https://github.com/pingcap/tidb/issues/42419) @ [ユジュンセン](https://github.com/YuJuncen)
        -   バックアッププロセス中に TiKV が応答しなくなった場合にバックアップタスクが停止する可能性がある問題を修正[＃53480](https://github.com/pingcap/tidb/issues/53480) @ [リーヴルス](https://github.com/Leavrth)
        -   ログバックアップが有効になっている場合にBRログに機密の資格情報が出力される可能性がある問題を修正[＃55273](https://github.com/pingcap/tidb/issues/55273) @ [リドリス](https://github.com/RidRisR)
        -   ログ バックアップ PITR タスクが失敗して停止すると、そのタスクに関連するセーフポイントが PD [＃17316](https://github.com/tikv/tikv/issues/17316) @ [リーヴルス](https://github.com/Leavrth)で適切にクリアされない問題を修正しました。

    -   TiDB データ移行 (DM)

        -   複数の DM マスター ノードが同時にリーダーになり、データの不整合が発生する可能性がある問題を修正しました[＃11602](https://github.com/pingcap/tiflow/issues/11602) @ [GMHDBJD](https://github.com/GMHDBJD)
        -   DM が`ALTER DATABASE`ステートメントを処理するときにデフォルトのデータベースを設定せず、レプリケーション エラー[＃11503](https://github.com/pingcap/tiflow/issues/11503) @ [ランス6716](https://github.com/lance6716)が発生する問題を修正しました。

    -   TiDB Lightning

        -   2 つのインスタンスが同時に並列インポート タスクを開始し、同じタスク ID [＃55384](https://github.com/pingcap/tidb/issues/55384) @ [杉本栄](https://github.com/ei-sugimoto)が割り当てられている場合に、 TiDB Lightning が`verify allocator base failed`エラーを報告する問題を修正しました。

## 寄稿者 {#contributors}

TiDB コミュニティの以下の貢献者に感謝いたします。

-   [杉本栄](https://github.com/ei-sugimoto)
-   [エルトシア](https://github.com/eltociear)
-   [グオショウヤン](https://github.com/guoshouyan) (初めての投稿者)
-   [ジャックL9u](https://github.com/JackL9u)
-   [カフカ1991](https://github.com/kafka1991) (初めての投稿者)
-   [清風777](https://github.com/qingfeng777)
-   [サンバRGB](https://github.com/samba-rgb) (初めての投稿者)
-   [シーライズ](https://github.com/SeaRise)
-   [つじえもん](https://github.com/tuziemon) (初めての投稿者)
-   [ジプロト](https://github.com/xyproto) (初めての投稿者)
