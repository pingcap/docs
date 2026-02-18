---
title: TiDB 8.4.0 Release Notes
summary: TiDB 8.4.0 の新機能、互換性の変更、改善点、バグ修正について説明します。
---

# TiDB 8.4.0 リリースノート {#tidb-8-4-0-release-notes}

発売日：2024年11月11日

TiDB バージョン: 8.4.0

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v8.4/quick-start-with-tidb)

8.4.0 では、次の主な機能と改善が導入されています。

<table><thead><tr><th>カテゴリ</th><th>機能/拡張機能</th><th>説明</th></tr></thead><tbody><tr><td rowspan="4">スケーラビリティとパフォーマンス</td><td><a href="https://docs.pingcap.com/tidb/v8.4/system-variables#tidb_enable_instance_plan_cache-new-in-v840">インスタンスレベルの実行プランキャッシュ</a>（実験的）</td><td>インスタンスレベルのプランキャッシュにより、同じTiDBインスタンス内のすべてのセッションでプランキャッシュを共有できます。セッションレベルのプランキャッシュと比較して、この機能はより多くの実行プランをメモリにキャッシュすることでSQLコンパイル時間を短縮し、全体的なSQL実行時間を短縮します。OLTPのパフォーマンスとスループットを向上させると同時に、メモリ使用量をより適切に制御し、データベースの安定性を高めます。</td></tr><tr><td><a href="https://docs.pingcap.com/tidb/v8.4/partitioned-table#global-indexes">パーティションテーブルのグローバルインデックス</a>（GA）</td><td>グローバルインデックスは、パーティション化されていない列の取得効率を効果的に向上させ、一意のキーがパーティションキーを含んでいなければならないという制約を排除します。この機能により、TiDBパーティションテーブルの利用シナリオが拡張され、データ移行に必要なアプリケーション変更作業の一部が回避されます。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v8.4/system-variables#tidb_tso_client_rpc_mode-new-in-v840">TSOリクエストの並列モード</a></td><td>同時実行性の高いシナリオでは、この機能を使用して、TSO の取得の待機時間を短縮し、クラスターのスループットを向上させることができます。</td></tr><tr><td><a href="https://docs.pingcap.com/tidb/v8.4/cached-tables">キャッシュされたテーブル</a>のクエリパフォーマンスを向上</td><td>キャッシュされたテーブルにおけるインデックススキャンのクエリパフォーマンスが向上し、一部のシナリオでは最大5.4倍のパフォーマンス向上が期待できます。小規模なテーブルに対する高速クエリの場合、キャッシュされたテーブルを使用することで、全体的なパフォーマンスを大幅に向上させることができます。</td></tr><tr><td rowspan="4">信頼性と可用性</td><td><a href="https://docs.pingcap.com/tidb/v8.4/tidb-resource-control#query_limit-parameters">ランナウェイクエリのトリガーをさらにサポートし、リソースグループの切り替えをサポートします。</a></td><td>ランナウェイクエリは、予期せぬSQLパフォーマンス問題がシステムに与える影響を効果的に軽減する手段を提供します。TiDB v8.4.0では、コプロセッサーによって処理されたキー数（ <code>PROCESSED_KEYS</code> ）とリクエスト単位数（ <code>RU</code> ）を識別条件として導入し、識別されたクエリを指定されたリソースグループに配置することで、ランナウェイクエリをより正確に識別・制御します。</td></tr><tr><td><a href="https://docs.pingcap.com/tidb/v8.4/tidb-resource-control#background-parameters">リソース制御のバックグラウンドタスクのリソース使用量の上限設定をサポート</a></td><td>リソース制御において、バックグラウンドタスクの最大パーセンテージ制限を設定することで、様々なアプリケーションシステムのニーズに応じてリソース消費量を制御できます。これにより、バックグラウンドタスクの消費量を低く抑え、オンラインサービスの品質を確保できます。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v8.4/tiproxy-traffic-replay">TiProxy はトラフィックのキャプチャと再生をサポートします</a>(実験的)</td><td> TiProxyを使用すると、クラスタのアップグレード、移行、デプロイメントの変更といった主要な操作を行う前に、TiDB本番クラスタから実際のワークロードをキャプチャできます。これらのワークロードをターゲットのテストクラスタで再生することで、パフォーマンスを検証し、変更が確実に成功することを確認できます。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v8.4/system-variables#tidb_auto_analyze_concurrency-new-in-v840">同時自動統計収集</a></td><td>TiDBクラスタ内で同時に実行される自動分析処理の数を制御するシステム変数<code>tidb_auto_analyze_concurrency</code>を導入しました。TiDBは、ノードの規模とハードウェア仕様に基づいて、スキャンタスクの同時実行数を自動的に決定します。これにより、システムリソースを最大限に活用して統計情報の収集効率が向上し、手動によるチューニングの必要性が軽減され、クラスタの安定したパフォーマンスが確保されます。</td></tr><tr><td rowspan="1"> SQL</td><td><a href="https://docs.pingcap.com/ai/vector-search-overview">ベクトル検索</a>（実験的）</td><td>ベクトル検索は、データのセマンティクスに基づいた検索手法であり、より関連性の高い検索結果を提供します。AIや大規模言語モデル（LLM）の中核関数の一つとして、ベクトル検索は検索拡張生成（RAG）、セマンティック検索、レコメンデーションシステムなど、様々なシナリオで活用できます。</td></tr><tr><td rowspan="3"> DB操作と可観測性</td><td><a href="https://docs.pingcap.com/tidb/v8.4/information-schema-processlist">メモリテーブルに TiKV と TiDB の CPU 時間を表示する</a></td><td>CPU時間がシステムテーブルに統合され、セッションやSQLの他のメトリクスと並べて表示されるようになりました。これにより、CPU消費量の多い操作を複数の視点から観察し、診断効率を向上させることができます。これは、インスタンスにおけるCPU使用率の急上昇や、クラスターにおける読み取り/書き込みのホットスポットといっ​​たシナリオの診断に特に役立ちます。</td></tr><tr><td><a href="https://docs.pingcap.com/tidb/v8.4/top-sql#use-top-sql">テーブルまたはデータベースごとに集計された TiKV CPU 時間の表示をサポート</a></td><td>ホットスポットの問題が個々の SQL ステートメントによって発生していない場合は、 「Top SQL」のテーブルまたはデータベース レベル別に集計された CPU 時間を使用すると、ホットスポットの原因となっているテーブルまたはアプリケーションを迅速に特定できるため、ホットスポットと CPU 消費の問題の診断効率が大幅に向上します。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v8.4/backup-and-restore-storages#authentication">IMDSv2 サービスを有効にした TiKV インスタンスのバックアップをサポート</a></td><td><a href="https://aws.amazon.com/cn/blogs/security/get-the-full-benefits-of-imdsv2-and-disable-imdsv1-across-your-aws-infrastructure/">AWS EC2 は、デフォルトのメタデータサービスとして IMDSv2 を使用するようになりました</a>。TiDB は、IMDSv2 が有効になっている TiKV インスタンスからのデータのバックアップをサポートしており、パブリッククラウドサービスで TiDB クラスターをより効率的に実行するのに役立ちます。</td></tr><tr><td rowspan="1">Security</td><td><a href="https://docs.pingcap.com/tidb/v8.4/br-pitr-manual#encrypt-log-backup-data">ログバックアップデータのクライアント側暗号化</a>（実験的）</td><td>ログ バックアップ データをバックアップstorageにアップロードする前に、バックアップ データを暗号化して、storage中および転送中のセキュリティを確保できます。</td></tr></tbody></table>

## 機能の詳細 {#feature-details}

### パフォーマンス {#performance}

-   TSO リクエストに並列バッチモードを導入し、TSO 取得のレイテンシーを短縮します[＃54960](https://github.com/pingcap/tidb/issues/54960) [＃8432](https://github.com/tikv/pd/issues/8432) @ [ミョンケミンタ](https://github.com/MyonKeminta)

    v8.4.0より前のバージョンでは、PDから[TSO](/tso.md)リクエストを送信すると、TiDBは特定の期間内に複数のTSOリクエストを収集し、それらをバッチ処理してシリアルに処理することで、リモートプロシージャコール（RPC）リクエストの数を減らし、PDのワークロードを軽減していました。しかし、レイテンシが重要なシナリオでは、このシリアルバッチ処理モードのパフォーマンスは理想的ではありません。

    TiDB v8.4.0では、TSOリクエストに対して、異なる同時実行能力を持つ並列バッチ処理モードが導入されました。並列モードはTSO取得のレイテンシーを短縮しますが、PDワークロードが増加する可能性があります。TSO取得に並列RPCモードを設定するには、システム変数[`tidb_tso_client_rpc_mode`](/system-variables.md#tidb_tso_client_rpc_mode-new-in-v840)を設定してください。

    詳細については[ドキュメント](/system-variables.md#tidb_tso_client_rpc_mode-new-in-v840)参照してください。

-   TiDBのハッシュ結合演算子の実行効率を最適化（実験的） [＃55153](https://github.com/pingcap/tidb/issues/55153) [＃53127](https://github.com/pingcap/tidb/issues/53127) @ [ウィンドトーカー](https://github.com/windtalker) @ [xzhangxian1008](https://github.com/xzhangxian1008) @ [徐淮嶼](https://github.com/XuHuaiyu) @ [wshwsh12](https://github.com/wshwsh12)

    TiDB v8.4.0では、ハッシュ結合演算子の最適化バージョンが導入され、実行効率が向上しました。現在、ハッシュ結合の最適化バージョンは内部結合と外部結合の操作にのみ適用され、デフォルトでは無効になっています。この最適化バージョンを有効にするには、システム変数[`tidb_hash_join_version`](/system-variables.md#tidb_hash_join_version-new-in-v840)を`optimized`に設定してください。

    詳細については[ドキュメント](/system-variables.md#tidb_hash_join_version-new-in-v840)参照してください。

-   次の日付関数を TiKV [＃56297](https://github.com/pingcap/tidb/issues/56297) [＃17529](https://github.com/tikv/tikv/issues/17529) @ [ゲンリキ](https://github.com/gengliqi)にプッシュダウンすることをサポートします

    -   `DATE_ADD()`
    -   `DATE_SUB()`
    -   `ADDDATE()`
    -   `SUBDATE()`

    詳細については[ドキュメント](/functions-and-operators/expressions-pushed-down.md)参照してください。

-   インスタンスレベルの実行プランキャッシュをサポート（実験的） [＃54057](https://github.com/pingcap/tidb/issues/54057) @ [qw4990](https://github.com/qw4990)

    インスタンスレベルの実行プランキャッシュにより、同じTiDBインスタンス内のすべてのセッションで実行プランキャッシュを共有できます。この機能により、TiDBクエリの応答時間が大幅に短縮され、クラスタのスループットが向上し、実行プランの変更の可能性が低減され、クラスタの安定したパフォーマンスが維持されます。セッションレベルの実行プランキャッシュと比較して、インスタンスレベルの実行プランキャッシュには以下の利点があります。

    -   冗長性を排除し、同じメモリ消費量でより多くの実行プランをキャッシュします。
    -   インスタンスに固定サイズのメモリを割り当て、メモリ使用量をより効果的に制限します。

    バージョン8.4.0では、インスタンスレベルの実行プランキャッシュはクエリ実行プランのキャッシュのみをサポートしており、デフォルトでは無効になっています。この機能は[`tidb_enable_instance_plan_cache`](/system-variables.md#tidb_enable_instance_plan_cache-new-in-v840)で有効化し、 [`tidb_instance_plan_cache_max_size`](/system-variables.md#tidb_instance_plan_cache_max_size-new-in-v840)で最大メモリ使用量を設定できます。この機能を有効化する前に、 [準備された実行プランのキャッシュ](/sql-prepared-plan-cache.md)と[準備されていない実行プランのキャッシュ](/sql-non-prepared-plan-cache.md)を無効化してください。

    詳細については[ドキュメント](/system-variables.md#tidb_enable_instance_plan_cache-new-in-v840)参照してください。

-   TiDB Lightningの論理インポートモードは、準備されたステートメントとクライアントステートメントキャッシュ[＃54850](https://github.com/pingcap/tidb/issues/54850) @ [dbsid](https://github.com/dbsid)をサポートします。

    設定項目`logical-import-prep-stmt`有効にすると、TiDB Lightningの論理インポートモードで実行されるSQL文は、プリペアドステートメントとクライアントステートメントキャッシュを使用します。これにより、 TiDB SQLの解析とコンパイルのコストが削減され、SQL実行効率が向上し、実行プランキャッシュへのヒット率が向上するため、論理インポートが高速化されます。

    詳細については[ドキュメント](/tidb-lightning/tidb-lightning-configuration.md)参照してください。

-   パーティションテーブルはグローバルインデックス（GA）をサポートします[＃45133](https://github.com/pingcap/tidb/issues/45133) @ [ミョンス](https://github.com/mjonss) @ [定義2014](https://github.com/Defined2014) @ [ジフハスト](https://github.com/jiyfhust) @ [L-メープル](https://github.com/L-maple)

    初期のTiDBバージョンでは、グローバルインデックスをサポートしていないため、パーティションテーブルにはいくつかの制限がありました。例えば、一意キーはテーブルのパーティション式のすべての列を使用する必要があります。クエリ条件でパーティションキーが使用されていない場合、クエリはすべてのパーティションをスキャンするため、パフォーマンスが低下します。v7.6.0以降では、グローバルインデックス機能を有効にするためにシステム変数[`tidb_enable_global_index`](/system-variables.md#tidb_enable_global_index-new-in-v760)が導入されました。ただし、この機能は当時開発中であったため、有効にすることは推奨されません。

    バージョン8.3.0以降、グローバルインデックス機能が実験的機能としてリリースされました。パーティションテーブルに`GLOBAL`キーワードを使用して明示的にグローバルインデックスを作成できます。これにより、パーティションテーブルの一意キーにはパーティション式で使用されるすべての列が含まれていなければならないという制限がなくなり、より柔軟なアプリケーション要件に対応できるようになります。さらに、グローバルインデックスは、パーティション化されていない列に基づくクエリのパフォーマンスも向上させます。

    この機能はv8.4.0で一般提供（GA）されます。グローバルインデックス機能を有効にするためにシステム変数[`tidb_enable_global_index`](/system-variables.md#tidb_enable_global_index-new-in-v760)を設定する代わりに、キーワード`GLOBAL`を使用することでグローバルインデックスを作成できます。v8.4.0以降、このシステム変数は非推奨となり、常に`ON`になります。

    詳細については[ドキュメント](/global-indexes.md)参照してください。

-   いくつかのシナリオでキャッシュされたテーブルのクエリパフォーマンスを向上[＃43249](https://github.com/pingcap/tidb/issues/43249) @ [天菜麻緒](https://github.com/tiancaiamao)

    v8.4.0では、TiDBは`SELECT ... LIMIT 1` `IndexLookup`で実行した場合、キャッシュされたテーブルのクエリパフォーマンスを最大5.4倍向上させます。さらに、TiDBはフルテーブルスキャンと主キークエリのシナリオにおいて`IndexLookupReader`のパフォーマンスを向上させます。

### 信頼性 {#reliability}

-   ランナウェイクエリは、処理されたキーとリクエストユニットの数をしきい値[＃54434](https://github.com/pingcap/tidb/issues/54434) @ [HuSharp](https://github.com/HuSharp)としてサポートします。

    TiDB v8.4.0以降、処理されたキー数（ `PROCESSED_KEYS` ）とリクエストユニット数（ `RU` ）に基づいて、ランナウェイクエリを識別できるようになりました。実行時間（ `EXEC_ELAPSED` ）と比較して、これらの新しいしきい値はクエリのリソース消費をより正確に定義し、全体的なパフォーマンスが低下した場合の識別バイアスを回避します。

    複数の条件を同時に設定することができ、いずれかの条件が満たされた場合、クエリはランナウェイ クエリとして識別されます。

    [明細書要約表](/statement-summary-tables.md)の対応するフィールド ( `RESOURCE_GROUP` 、 `MAX_REQUEST_UNIT_WRITE` 、 `MAX_REQUEST_UNIT_READ` 、 `MAX_PROCESSED_KEYS` ) を観察して、実行履歴に基づいて条件値を判断できます。

    詳細については[ドキュメント](/tidb-resource-control-runaway-queries.md)参照してください。

-   ランナウェイクエリ[＃54434](https://github.com/pingcap/tidb/issues/54434) @ [Jmポテト](https://github.com/JmPotato)のリソースグループの切り替えをサポート

    TiDB v8.4.0以降では、ランナウェイクエリのリソースグループを特定のグループに切り替えることができます。1 `COOLDOWN`メカニズムでリソース消費量を削減できない場合は、 [リソースグループ](/tidb-resource-control-ru-groups.md#create-a-resource-group)を作成し、そのリソースサイズを制限し、 `SWITCH_GROUP`パラメータを設定することで、特定されたランナウェイクエリをこのグループに移動できます。その間、同一セッション内の後続のクエリは元のリソースグループで引き続き実行されます。リソースグループを切り替えることで、リソース使用量をより正確に管理し、リソース消費をより厳密に制御できます。

    詳細については[ドキュメント](/tidb-resource-control-runaway-queries.md#query_limit-parameters)参照してください。

-   `tidb_scatter_region`システム変数[＃55184](https://github.com/pingcap/tidb/issues/55184) @ [D3ハンター](https://github.com/D3Hunter)を使用してクラスターレベルのリージョン分散戦略の設定をサポートします。

    v8.4.0より前では、システム変数`tidb_scatter_region`は有効化または無効化のみ可能です。有効化すると、TiDBはバッチテーブル作成時にテーブルレベルの分散戦略を適用します。しかし、数十万ものテーブルをバッチで作成する場合、この戦略によって一部のTiKVノードに領域が集中し、それらのノードでOOM（メモリ不足）問題が発生します。

    v8.4.0以降、 `tidb_scatter_region`文字列型に変更されました。これにより、クラスターレベルの分散戦略がサポートされ、前述のシナリオにおけるTiKV OOMの問題を回避できるようになります。

    詳細については[ドキュメント](/system-variables.md#tidb_scatter_region)参照してください。

-   リソース制御[＃56019](https://github.com/pingcap/tidb/issues/56019) @ [栄光](https://github.com/glorv)のバックグラウンドタスクのリソース使用量の上限設定をサポート

    TiDBリソース制御は、バックグラウンドタスクの優先度を識別し、下げることができます。特定のシナリオでは、リソースが利用可能であっても、バックグラウンドタスクのリソース消費を制限したい場合があります。v8.4.0以降では、 `UTILIZATION_LIMIT`パラメータを使用して、バックグラウンドタスクが消費できるリソースの最大割合を設定できます。各ノードは、すべてのバックグラウンドタスクのリソース使用量をこの割合以下に抑えます。この機能により、バックグラウンドタスクのリソース消費を正確に制御できるようになり、クラスターの安定性がさらに向上します。

    詳細については[ドキュメント](/tidb-resource-control-background-tasks.md)参照してください。

-   リソースグループ[＃50831](https://github.com/pingcap/tidb/issues/50831) @ [ノルーシュ](https://github.com/nolouch)のリソース割り当て戦略を最適化する

    TiDB は、リソース管理に対するユーザーの期待にさらに応えるために、v8.4.0 でリソース割り当て戦略を改善しました。

    -   実行時に大規模なクエリのリソース割り当てを制御し、リソースグループの制限超過を回避します。また、ランナウェイクエリ`COOLDOWN`と組み合わせることで、大規模なクエリの同時実行性を特定して削減し、瞬間的なリソース消費を削減できます。
    -   デフォルトの優先度スケジューリング戦略を調整します。優先度の異なるタスクが同時に実行される場合、優先度の高いタスクに多くのリソースが割り当てられます。

### 可用性 {#availability}

-   TiProxy はトラフィックリプレイ（実験的） [＃642](https://github.com/pingcap/tiproxy/issues/642) @ [djshow832](https://github.com/djshow832)をサポートします

    TiProxy v1.3.0以降では、 `tiproxyctl`使用してTiProxyインスタンスに接続し、TiDB本番クラスタでアクセストラフィックをキャプチャし、指定したレートでテストクラスタで再生できるようになりました。この機能により、本番クラスタの実際のワークロードをテスト環境で再現し、SQL文の実行結果とパフォーマンスを検証できます。

    トラフィック リプレイは、次のシナリオで役立ちます。

    -   TiDB バージョンのアップグレードを確認する
    -   変更の影響を評価する
    -   TiDBをスケーリングする前にパフォーマンスを検証する
    -   テストパフォーマンスの限界

    詳細については[ドキュメント](/tiproxy/tiproxy-traffic-replay.md)参照してください。

### SQL {#sql}

-   サポートベクター探索（実験的） [＃54245](https://github.com/pingcap/tidb/issues/54245) [＃17290](https://github.com/tikv/tikv/issues/17290) [＃9032](https://github.com/pingcap/tiflash/issues/9032) @ [そよ風のような](https://github.com/breezewish) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger) @ [エリック・ゼクアン](https://github.com/EricZequan) @ [ジムララ](https://github.com/zimulala) @ [ジェイソン・ファン](https://github.com/JaySon-Huang) @ [ウィノロス](https://github.com/winoros) @ [wk989898](https://github.com/wk989898)

    ベクトル検索は、データのセマンティクスに基づいた検索手法であり、より関連性の高い検索結果を提供します。AIや大規模言語モデル（LLM）の中核関数の一つとして、ベクトル検索は検索拡張生成（RAG）、セマンティック検索、レコメンデーションシステムなど、様々なシナリオで活用できます。

    TiDB v8.4.0以降、 [ベクトルデータ型](/ai/reference/vector-search-data-types.md)と[ベクトル検索インデックス](/ai/reference/vector-search-index.md)サポートし、強力なベクトル検索機能を提供します。TiDBベクトルデータ型は最大16,383次元をサポートし、L2距離（ユークリッド距離）、コサイン距離、負の内積、L1距離（マンハッタン距離）など、さまざまな[距離関数](/ai/reference/vector-search-functions-and-operators.md#vector-functions)サポートします。

    ベクトル検索を開始するには、ベクトルデータ型のテーブルを作成し、ベクトルデータを挿入し、ベクトルデータに対するクエリを実行するだけです。ベクトルデータと従来のリレーショナルデータを組み合わせたクエリも実行できます。

    ベクトル検索のパフォーマンスを向上させるには、 [ベクトル検索インデックス](/ai/reference/vector-search-index.md)作成して使用できます。TiDB ベクトル検索インデックスはTiFlashに依存していることに注意してください。ベクトル検索インデックスを使用する前に、TiDB クラスターにTiFlashノードがデプロイされていることを確認してください。

    詳細については[ドキュメント](/ai/concepts/vector-search-overview.md)参照してください。

### DB操作 {#db-operations}

-   BRはログバックアップデータのクライアント側暗号化をサポートします (実験的) [＃55834](https://github.com/pingcap/tidb/issues/55834) @ [トリスタン1900](https://github.com/Tristan1900)

    以前のバージョンのTiDBでは、クライアント側で暗号化できるのはスナップショットバックアップデータのみでした。v8.4.0以降では、ログバックアップデータもクライアント側で暗号化できるようになりました。ログバックアップデータをバックアップstorageにアップロードする前に、以下のいずれかの方法でバックアップデータを暗号化し、セキュリティを確保できます。

    -   カスタム固定キーを使用して暗号化する
    -   ローカルディスクに保存されたマスターキーを使用して暗号化する
    -   キー管理サービス (KMS) によって管理されるマスター キーを使用して暗号化します。

    詳細については[ドキュメント](/br/br-pitr-manual.md#encrypt-the-log-backup-data)参照してください。

-   BRはクラウドstorageシステムでバックアップデータを復元する際に必要な権限が少なくなります[＃55870](https://github.com/pingcap/tidb/issues/55870) @ [リーヴルス](https://github.com/Leavrth)

    v8.4.0より前のバージョンでは、 BRはリストア中にリストアの進行状況に関するチェックポイント情報をバックアップstorageシステムに書き込みます。これらのチェックポイントにより、中断されたリストアを迅速に再開できます。v8.4.0以降では、 BRはリストアのチェックポイント情報をターゲットのTiDBクラスターに書き込みます。つまり、リストア中はBRはバックアップディレクトリへの読み取りアクセスのみを必要とします。

    詳細については[ドキュメント](/br/backup-and-restore-storages.md#authentication)参照してください。

### 可観測性 {#observability}

-   システムテーブル[＃55542](https://github.com/pingcap/tidb/issues/55542) @ [yibin87](https://github.com/yibin87)のTiDBとTiKVによって消費されたCPU時間を表示します。

    [Top SQLページ](/dashboard/top-sql.md) [TiDBダッシュボード](/dashboard/dashboard-intro.md) CPU消費量の高いSQL文を表示します。v8.4.0以降、TiDBはCPU時間消費情報をシステムテーブルに追加し、セッションやSQLの他のメトリクスと併せて表示します。これにより、CPU消費量の高い操作を複数の視点から容易に観察できます。この情報は、インスタンスのCPUスパイクやクラスター内の読み取り/書き込みホットスポットなどのシナリオにおいて、問題の原因を迅速に特定するのに役立ちます。

    -   [明細書要約表](/statement-summary-tables.md) `AVG_TIDB_CPU_TIME`と`AVG_TIKV_CPU_TIME`を追加して、履歴的に個々の SQL ステートメントで消費された平均 CPU 時間を表示します。
    -   [INFORMATION_SCHEMA.PROCESSLIST](/information-schema/information-schema-processlist.md)テーブルには`TIDB_CPU`と`TIKV_CPU`追加され、セッションで現在実行されている SQL ステートメントの累積 CPU 消費量が表示されます。
    -   [スロークエリログ](/analyze-slow-queries.md) `Tidb_cpu_time`フィールドと`Tikv_cpu_time`フィールドを追加し、キャプチャされた SQL ステートメントによって消費された CPU 時間を表示します。

    デフォルトでは、TiKV によって消費された CPU 時間が表示されます。TiDB によって消費された CPU 時間を収集すると、追加のオーバーヘッド（約 8%）が発生するため、TiDB によって消費された CPU 時間は[Top SQL](/dashboard/top-sql.md)有効になっている場合にのみ実際の値が表示され、それ以外の場合は常に`0`と表示されます。

    詳細については、 [`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md)および[`INFORMATION_SCHEMA.SLOW_QUERY`](/information-schema/information-schema-slow-query.md)を参照してください。

-   Top SQL は、テーブルまたはデータベースごとに集計された CPU 時間結果の表示をサポートします[＃55540](https://github.com/pingcap/tidb/issues/55540) @ [ノルーシュ](https://github.com/nolouch)

    バージョン8.4.0より前のバージョンでは、 [Top SQL](/dashboard/top-sql.md) CPU時間をSQLごとに集計していました。CPU時間が消費されるSQL文が少数の場合、SQLごとの集計では問題を効果的に特定できません。バージョン8.4.0以降では、CPU時間を**テーブル別**または**データベース別に**集計できます。複数のシステムが存在するシナリオでは、新しい集計方法により、特定のシステムからの負荷変化をより効果的に特定できるため、診断効率が向上します。

    詳細については[ドキュメント](/dashboard/top-sql.md#use-top-sql)参照してください。

### Security {#security}

-   BRはAWS IMDSv2 [＃16443](https://github.com/tikv/tikv/issues/16443) @ [ピンギュ](https://github.com/pingyu)をサポートします

    TiDB を Amazon EC2 にデプロイする場合、 BR はAWS インスタンスメタデータサービス バージョン 2 (IMDSv2) をサポートします。EC2 インスタンスを設定することで、 BR がインスタンスに関連付けられたIAMロールを使用して Amazon S3 にアクセスするための適切な権限を付与できるようになります。

    詳細については[ドキュメント](/br/backup-and-restore-storages.md#authentication)参照してください。

### データ移行 {#data-migration}

-   TiCDC Claim-Check は、Kafka メッセージの`value`フィールドのみを外部storage[＃11396](https://github.com/pingcap/tiflow/issues/11396) @ [3エースショーハンド](https://github.com/3AceShowHand)に送信することをサポートします。

    v8.4.0 より前では、Claim-Check 機能が有効になっている場合 ( `large-message-handle-option`を`claim-check`に設定)、TiCDC は大きなメッセージを処理するときに、 `key`フィールドと`value`フィールドの両方をエンコードして外部storageシステムに保存します。

    バージョン8.4.0以降、TiCDCはKafkaメッセージの`value`番目のフィールドのみを外部storageに送信することをサポートします。この機能は非Open Protocolプロトコルにのみ適用されます。この機能は`claim-check-raw-value`パラメータを設定することで制御できます。

    詳細については[ドキュメント](/ticdc/ticdc-sink-to-kafka.md#send-the-value-field-to-external-storage-only)参照してください。

-   TiCDC は、更新または削除イベント[＃10969](https://github.com/pingcap/tiflow/issues/10969) @ [3エースショーハンド](https://github.com/3AceShowHand)の古い値を検証するためのチェックサム V2 を導入しました。

    v8.4.0以降、TiDBとTiCDCはChecksum V2アルゴリズムを導入し、 `ADD COLUMN`または`DROP COLUMN`操作後にUpdateイベントまたはDeleteイベントの古い値を検証する際のChecksum V1の問題を解決するようになりました。v8.4.0以降で作成されたクラスター、またはv8.4.0にアップグレードされたクラスターでは、単一行データのチェックサム検証が有効になっている場合、TiDBはデフォルトでChecksum V2を使用します。TiCDCはChecksum V1とV2の両方の処理をサポートしています。この変更はTiDBとTiCDCの内部実装にのみ影響し、下流のKafkaコンシューマーのチェックサム計算方法には影響しません。

    詳細については[ドキュメント](/ticdc/ticdc-integrity-check.md)参照してください。

## 互換性の変更 {#compatibility-changes}

> **注記：**
>
> このセクションでは、v8.3.0から最新バージョン（v8.4.0）にアップグレードする際に知っておくべき互換性の変更点について説明します。v8.2.0以前のバージョンから最新バージョンにアップグレードする場合は、中間バージョンで導入された互換性の変更点も確認する必要があるかもしれません。

### システム変数 {#system-variables}

| 変数名                                                                                                                             | タイプを変更   | 説明                                                                                                                                                                                                                                                                                                  |
| ------------------------------------------------------------------------------------------------------------------------------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `log_bin`                                                                                                                       | 削除済み     | v8.4.0では[TiDBBinlog](https://docs.pingcap.com/tidb/v8.3/tidb-binlog-overview)が削除されました。この変数はTiDB Binlogが使用されているかどうかを示すもので、v8.4.0以降では削除されています。                                                                                                                                                        |
| `sql_log_bin`                                                                                                                   | 削除済み     | v8.4.0では[TiDBBinlog](https://docs.pingcap.com/tidb/v8.3/tidb-binlog-overview)が削除されました。この変数はTiDB Binlogに変更を書き込むかどうかを示すもので、v8.4.0以降では削除されました。                                                                                                                                                         |
| [`tidb_enable_global_index`](/system-variables.md#tidb_enable_global_index-new-in-v760)                                         | 非推奨      | バージョン8.4.0では、この変数は非推奨となりました。値はデフォルト値の`ON`に固定されます。つまり、 [グローバルインデックス](/global-indexes.md)デフォルトで有効になります。グローバルインデックスを作成するには`CREATE TABLE`または`ALTER TABLE`実行する際に、対応する列にキーワード`GLOBAL`を追加するだけで済みます。                                                                                                        |
| [`tidb_enable_list_partition`](/system-variables.md#tidb_enable_list_partition-new-in-v50)                                      | 非推奨      | バージョン8.4.0では、この変数は非推奨となります。値はデフォルト値の`ON`に固定され、デフォルトで[リスト分割](/partitioned-table.md#list-partitioning)有効になります。                                                                                                                                                                                        |
| [`tidb_enable_table_partition`](/system-variables.md#tidb_enable_table_partition)                                               | 非推奨      | バージョン8.4.0では、この変数は非推奨となります。値はデフォルト値の`ON`に固定され、デフォルトで[テーブルパーティション](/partitioned-table.md)有効になります。                                                                                                                                                                                                    |
| [`tidb_analyze_partition_concurrency`](/system-variables.md#tidb_analyze_partition_concurrency)                                 | 修正済み     | 値の範囲を`[1, 18446744073709551615]`から`[1, 128]`に変更します。                                                                                                                                                                                                                                                 |
| [`tidb_enable_inl_join_inner_multi_pattern`](/system-variables.md#tidb_enable_inl_join_inner_multi_pattern-new-in-v700)         | 修正済み     | デフォルト値を`OFF`から`ON`に変更します。v8.4.0以降では、内部テーブルに`Selection` 、 `Aggregation` 、または`Projection`の演算子がある場合、インデックス結合がデフォルトでサポートされます。                                                                                                                                                                           |
| [`tidb_opt_prefer_range_scan`](/system-variables.md#tidb_opt_prefer_range_scan-new-in-v50)                                      | 修正済み     | デフォルト値を`OFF`から`ON`に変更します。統計情報のないテーブル（疑似統計）または空のテーブル（統計情報ゼロ）の場合、オプティマイザはフルテーブルスキャンよりもインターバルスキャンを優先します。                                                                                                                                                                                               |
| [`tidb_scatter_region`](/system-variables.md#tidb_scatter_region)                                                               | 修正済み     | v8.4.0より前では、その型はブール型で、 `ON`と`OFF`をサポートしていました。また、新規作成されたテーブルのリージョンは、有効化後にテーブルレベルの分散のみをサポートします。v8.4.0以降では、 `SESSION`スコープが追加され、型がブール型から列挙型に変更され、デフォルト値が`OFF`からnullに変更され、オプション値として`TABLE`と`GLOBAL`が追加されました。さらに、バッチ処理による高速テーブル作成時にリージョンの不均一な分散によって発生するTiKV OOM問題を回避するため、クラスターレベルの分散ポリシーもサポートされるようになりました。 |
| [`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-new-in-v800)                                             | 修正済み     | デフォルト値を`0`から`536870912` （512 MiB）に変更します。これは、この機能がデフォルトで有効であることを示します。許容される最小値は`67108864` （64 MiB）に設定されています。                                                                                                                                                                                          |
| [`tidb_auto_analyze_concurrency`](/system-variables.md#tidb_auto_analyze_concurrency-new-in-v840)                               | 新しく追加された | TiDBクラスター内の自動分析操作の同時実行数を設定します。v8.4.0より前では、この同時実行数は`1`に固定されています。統計収集タスクを高速化するには、クラスターの利用可能なリソースに応じてこの同時実行数を増やすことができます。                                                                                                                                                                               |
| [`tidb_enable_instance_plan_cache`](/system-variables.md#tidb_enable_instance_plan_cache-new-in-v840)                           | 新しく追加された | インスタンス プラン キャッシュ機能を有効にするかどうかを制御します。                                                                                                                                                                                                                                                                 |
| [`tidb_enable_stats_owner`](/system-variables.md#tidb_enable_stats_owner-new-in-v840)                                           | 新しく追加された | 対応する TiDB インスタンスが自動統計更新タスクを実行できるかどうかを制御します。                                                                                                                                                                                                                                                         |
| [`tidb_hash_join_version`](/system-variables.md#tidb_hash_join_version-new-in-v840)                                             | 新しく追加された | TiDBがハッシュ結合演算子の最適化バージョンを使用するかどうかを制御します。デフォルト値の`legacy`は、最適化バージョンを使用しないことを意味します。 `optimized`に設定すると、TiDBはハッシュ結合演算子の実行時に最適化バージョンを使用し、ハッシュ結合のパフォーマンスを向上させます。                                                                                                                                            |
| [`tidb_instance_plan_cache_max_size`](/system-variables.md#tidb_instance_plan_cache_max_size-new-in-v840)                       | 新しく追加された | インスタンス プラン キャッシュの最大メモリ使用量を設定します。                                                                                                                                                                                                                                                                    |
| [`tidb_instance_plan_cache_reserved_percentage`](/system-variables.md#tidb_instance_plan_cache_reserved_percentage-new-in-v840) | 新しく追加された | メモリの削除後にインスタンス プラン キャッシュ用に予約されるアイドルメモリの割合を制御します。                                                                                                                                                                                                                                                    |
| [`tidb_pre_split_regions`](/system-variables.md#tidb_pre_split_regions-new-in-v840)                                             | 新しく追加された | バージョン8.4.0より前のバージョンでは、新規作成テーブルの行分割スライス数のデフォルト設定には、 `CREATE TABLE` SQL文ごとに`PRE_SPLIT_REGIONS`宣言する必要がありました。これは、多数のテーブルを同様に設定する必要がある場合、煩雑な作業となります。この変数はこうした問題を解決するために導入されました。このシステム変数を`GLOBAL`または`SESSION`レベルに設定することで、ユーザビリティを向上させることができます。                                                            |
| [`tidb_shard_row_id_bits`](/system-variables.md#tidb_shard_row_id_bits-new-in-v840)                                             | 新しく追加された | バージョン8.4.0より前では、新規作成テーブルの行IDのデフォルトのスライス数を設定するには、 `CREATE TABLE`または`ALTER TABLE` SQL文ごとに`SHARD_ROW_ID_BITS`宣言する必要がありました。これは、多数のテーブルを同様に設定する必要がある場合、煩雑になります。この変数は、こうした問題を解決するために導入されました。このシステム変数を`GLOBAL`または`SESSION`レベルに設定することで、ユーザビリティを向上させることができます。                                                |
| [`tidb_tso_client_rpc_mode`](/system-variables.md#tidb_tso_client_rpc_mode-new-in-v840)                                         | 新しく追加された | TiDBがPDにTSO RPCリクエストを送信するモードを切り替えます。このモードは、TSO RPCリクエストを並列処理できるかどうかを決定し、各TS取得操作のバッチ待機時間に影響を与えます。これにより、特定のシナリオにおけるクエリ実行中のTS取得の待機時間を短縮できます。                                                                                                                                                           |

### コンフィグレーションパラメータ {#configuration-parameters}

| コンフィグレーションファイルまたはコンポーネント | コンフィグレーションパラメータ                                                                                                          | タイプを変更   | 説明                                                                                                                                                                          |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------ | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ティドブ                     | [`grpc-keepalive-time`](/tidb-configuration-file.md#grpc-keepalive-time)                                                 | 修正済み     | 最小値`1`を加算します。                                                                                                                                                               |
| ティドブ                     | [`grpc-keepalive-timeout`](/tidb-configuration-file.md#grpc-keepalive-timeout)                                           | 修正済み     | バージョン8.4.0より前では、このパラメータのデータ型はINTで、最小値は`1`でした。バージョン8.4.0以降では、データ型がFLOAT64に変更され、最小値は`0.05`なります。ネットワークジッターが頻繁に発生するシナリオでは、値を小さくして再試行間隔を短くすることで、ネットワークジッターによるパフォーマンスへの影響を軽減できます。 |
| ティドブ                     | [`tidb_enable_stats_owner`](/tidb-configuration-file.md#tidb_enable_stats_owner-new-in-v840)                             | 新しく追加された | 対応する TiDB インスタンスが自動統計更新タスクを実行できるかどうかを制御します。                                                                                                                                 |
| ティクブ                     | [`region-split-keys`](/tikv-configuration-file.md#region-split-keys)                                                     | 修正済み     | デフォルト値を`"960000"`から`"2560000"`に変更します。                                                                                                                                       |
| ティクブ                     | [`region-split-size`](/tikv-configuration-file.md#region-split-size)                                                     | 修正済み     | デフォルト値を`"96MiB"`から`"256MiB"`に変更します。                                                                                                                                         |
| ティクブ                     | [`sst-max-size`](/tikv-configuration-file.md#sst-max-size)                                                               | 修正済み     | デフォルト値を`"144MiB"`から`"384MiB"`に変更します。                                                                                                                                        |
| ティクブ                     | [`pessimistic-txn.in-memory-instance-size-limit`](/tikv-configuration-file.md#in-memory-instance-size-limit-new-in-v840) | 新しく追加された | TiKVインスタンスにおけるメモリ内悲観的ロックのメモリ使用量制限を制御します。この制限を超えると、TiKVは悲観的ロックを永続的に書き込みます。                                                                                                   |
| ティクブ                     | [`pessimistic-txn.in-memory-peer-size-limit`](/tikv-configuration-file.md#in-memory-peer-size-limit-new-in-v840)         | 新しく追加された | リージョン内のメモリ内悲観的ロックのメモリ使用量制限を制御します。この制限を超えると、TiKVは悲観的ロックを永続的に書き込みます。                                                                                                          |
| ティクブ                     | [`raft-engine.spill-dir`](/tikv-configuration-file.md#spill-dir-new-in-v840)                                             | 新しく追加された | RaftstorageRaftを保存するセカンダリ ディレクトリを制御します。                                                                                                                                     |
| ティクブ                     | [`resource-control.priority-ctl-strategy`](/tikv-configuration-file.md#priority-ctl-strategy-new-in-v840)                | 新しく追加された | 低優先度タスクの管理ポリシーを制御します。TiKVは、低優先度タスクにフロー制御を追加することで、高優先度タスクが最初に実行されるようにします。                                                                                                    |
| PD                       | [`cert-allowed-cn`](/enable-tls-between-components.md#verify-component-callers-identity)                                 | 修正済み     | v8.4.0以降では、複数の`Common Names`設定がサポートされます。v8.4.0より前では、 `Common Name` 1つしか設定できませんでした。                                                                                          |
| PD                       | [`max-merge-region-keys`](/pd-configuration-file.md#max-merge-region-keys)                                               | 修正済み     | デフォルト値を`200000`から`540000`に変更します。                                                                                                                                            |
| PD                       | [`max-merge-region-size`](/pd-configuration-file.md#max-merge-region-size)                                               | 修正済み     | デフォルト値を`20`から`54`に変更します。                                                                                                                                                    |
| TiFlash                  | [`storage.format_version`](/tiflash/tiflash-configuration.md)                                                            | 修正済み     | ベクターインデックスの作成とstorageをサポートするため、デフォルトのTiFlashstorageフォーマットのバージョンを`5`から`7`に変更します。このフォーマット変更により、v8.4.0以降にアップグレードされたTiFlashクラスターは、以前のバージョンへのインプレースダウングレードをサポートしなくなります。          |
| TiDBBinlog               | `--enable-binlog`                                                                                                        | 削除済み     | v8.4.0では[TiDBBinlog](https://docs.pingcap.com/tidb/v8.3/tidb-binlog-overview)削除されました。このパラメータはTiDBbinlog生成を有効にするかどうかを制御するもので、v8.4.0以降では削除されています。                             |
| TiCDC                    | [`claim-check-raw-value`](/ticdc/ticdc-sink-to-kafka.md#send-the-value-field-to-external-storage-only)                   | 新しく追加された | TiCDCがKafkaメッセージの`value`フィールドのみを外部storageに送信するかどうかを制御します。この機能は、オープンプロトコル以外のシナリオにのみ適用されます。                                                                                   |
| TiDB Lightning           | [`logical-import-prep-stmt`](/tidb-lightning/tidb-lightning-configuration.md)                                            | 新しく追加された | 論理インポートモードにおいて、このパラメータは、パフォーマンス向上のために準備済みステートメントとステートメントキャッシュを使用するかどうかを制御します。デフォルト値は`false`です。                                                                              |
| BR                       | [`--log.crypter.key`](/br/br-pitr-manual.md#encrypt-the-log-backup-data)                                                 | 新しく追加された | ログバックアップデータの暗号化キーを16進文字列形式で指定します。アルゴリズム`aes128-ctr`の場合は128ビット（16バイト）、アルゴリズム`aes192-ctr`の場合は24バイト、アルゴリズム`aes256-ctr`の場合は32バイトのキーとなります。                                       |
| BR                       | [`--log.crypter.key-file`](/br/br-pitr-manual.md#encrypt-the-log-backup-data)                                            | 新しく追加された | ログバックアップデータのキーファイルを指定します。1 `crypter.key`渡さずに、キーが保存されているファイルパスをパラメータとして直接渡すこともできます。                                                                                          |
| BR                       | [`--log.crypter.method`](/br/br-pitr-manual.md#encrypt-the-log-backup-data)                                              | 新しく追加された | ログバックアップデータの暗号化アルゴリズムを指定します。値は`aes128-ctr` 、 `aes192-ctr` 、または`aes256-ctr`です。デフォルト値は`plaintext`で、データは暗号化されません。                                                              |
| BR                       | [`--master-key`](/br/br-pitr-manual.md#encrypt-the-log-backup-data)                                                      | 新しく追加された | ログバックアップデータのマスターキーを指定します。ローカルディスクに保存されているマスターキー、またはクラウドキー管理サービス (KMS) によって管理されているマスターキーを使用できます。                                                                             |
| BR                       | [`--master-key-crypter-method`](/br/br-pitr-manual.md#encrypt-the-log-backup-data)                                       | 新しく追加された | ログバックアップデータのマスターキーに基づく暗号化アルゴリズムを指定します。値は`aes128-ctr` 、 `aes192-ctr` 、または`aes256-ctr`です。デフォルト値は`plaintext`で、データは暗号化されません。                                                    |

### オフラインパッケージの変更 {#offline-package-changes}

v8.4.0 以降、 `TiDB-community-toolkit` [バイナリパッケージ](/binary-package.md)から以下のコンテンツが削除されます。

-   `pump-{version}-linux-{arch}.tar.gz`
-   `drainer-{version}-linux-{arch}.tar.gz`
-   `binlogctl`
-   `arbiter`

### オペレーティング システムとプラットフォームの要件の変更 {#operating-system-and-platform-requirement-changes}

TiDB をアップグレードする前に、オペレーティング システムのバージョンが[OSおよびプラットフォームの要件](/hardware-and-software-requirements.md#os-and-platform-requirements)満たしていることを確認してください。

-   [CentOS Linux のサポート終了](https://www.centos.org/centos-linux-eol/)によると、CentOS Linux 7のアップストリームサポートは2024年6月30日に終了しました。そのため、TiDBはv8.4.0でCentOS 7のサポートを終了します。Rocky Linux 9.1以降のバージョンの使用をお勧めします。CentOS 7上のTiDBクラスターをv8.4.0にアップグレードすると、クラスターが使用できなくなります。
-   [Red Hat Enterprise Linux ライフサイクル](https://access.redhat.com/support/policy/updates/errata/#Life_Cycle_Dates)によると、Red Hat Enterprise Linux 7のメンテナンスサポートは2024年6月30日に終了しました。TiDBは、8.4 DMRバージョン以降のRed Hat Enterprise Linux 7のサポートを終了します。Rocky Linux 9.1以降のバージョンの使用をお勧めします。Red Hat Enterprise Linux 7上のTiDBクラスターをv8.4.0以降にアップグレードすると、クラスターが使用できなくなります。

## 削除された機能 {#removed-features}

-   v8.4.0 以降では次の機能が削除されます。

    -   v8.4.0では、 [TiDBBinlog](https://docs.pingcap.com/tidb/v8.3/tidb-binlog-overview)は削除されました。v8.3.0以降、TiDB Binlogは完全に非推奨となりました。増分データレプリケーションの場合は、代わりに[TiCDC](/ticdc/ticdc-overview.md)使用してください。ポイントインタイムリカバリ（PITR）の場合は、 [PITR](/br/br-pitr-guide.md)使用してください。TiDBクラスターをv8.4.0以降のバージョンにアップグレードする前に、必ずTiCDCとPITRに切り替えてください。

-   以下の機能は将来のバージョンで削除される予定です。

    -   TiDB Lightning v8.0.0以降、物理インポートモードの[競合検出の古いバージョン](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#the-old-version-of-conflict-detection-deprecated-in-v800)戦略は非推奨となり、 [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)番目のパラメータを使用して論理インポートモードと物理インポートモードの両方の競合検出戦略を制御できるようになりました。旧バージョンの競合検出用の[`duplicate-resolution`](/tidb-lightning/tidb-lightning-configuration.md)のパラメータは、将来のリリースで削除される予定です。

## 非推奨の機能 {#deprecated-features}

以下の機能は将来のバージョンで廃止される予定です。

-   TiDB では、統計を自動収集するタスクの順序を最適化するために、優先度キューを有効にするかどうかを制御するためのシステム変数[`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-new-in-v800)が導入されました。将来のリリースでは、統計を自動収集するタスクの順序付けは優先度キューのみになるため、このシステム変数は非推奨となります。
-   TiDBはv7.5.0でシステム変数[`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-new-in-v750)を導入しました。この変数を使用すると、TiDBがパーティション統計情報の非同期マージを使用し、OOM問題を回避するように設定できます。将来のリリースでは、パーティション統計情報は非同期にマージされるため、このシステム変数は非推奨となります。
-   以降のリリースでは[実行計画バインディングの自動進化](/sql-plan-management.md#baseline-evolution)再設計する予定であり、関連する変数と動作が変更されます。
-   TiDB v8.0.0では、並列HashAggアルゴリズムのディスクスピルをサポートするかどうかを制御するシステム変数[`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-new-in-v800)が導入されました。将来のバージョンでは、システム変数[`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-new-in-v800)は非推奨になります。
-   TiDB Lightningパラメータ[`conflict.max-record-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)は将来のリリースで廃止される予定であり、その後削除されます。このパラメータは[`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)に置き換えられます。これは、競合レコードの最大数が、単一のインポートタスクで許容される競合レコードの最大数と一致することを意味します。
-   バージョン6.3.0以降、パーティションテーブルはデフォルトで[動的プルーニングモード](/partitioned-table.md#dynamic-pruning-mode)使用します。静的プルーニングモードと比較して、動的プルーニングモードはIndexJoinやプランキャッシュなどの機能をサポートし、パフォーマンスが向上します。そのため、静的プルーニングモードは非推奨となります。

## 改善点 {#improvements}

-   ティドブ

    -   大量のデータをスキャンする際のBatchCopタスク構築の効率を最適化[＃55915](https://github.com/pingcap/tidb/issues/55915) [＃55413](https://github.com/pingcap/tidb/issues/55413) @ [wshwsh12](https://github.com/wshwsh12)
    -   トランザクションのバッファを最適化して、トランザクションの書き込みレイテンシーと TiDB CPU 使用率[＃55287](https://github.com/pingcap/tidb/issues/55287) @ [あなた06](https://github.com/you06)を削減します
    -   システム変数`tidb_dml_type` `"bulk"` [＃50215](https://github.com/pingcap/tidb/issues/50215) @ [エキシウム](https://github.com/ekexium)に設定されている場合にDMLステートメントの実行パフォーマンスを最適化します。
    -   [オプティマイザー修正制御 47400](/optimizer-fix-controls.md#47400-new-in-v840)使用して、オプティマイザが`estRows`から`1`の推定最小値を制限するかどうかを制御します。これは、Oracle や Db2 [＃47400](https://github.com/pingcap/tidb/issues/47400) @ [テリー・パーセル](https://github.com/terry1purcell)などのデータベースと一致しています。
    -   [`mysql.tidb_runaway_queries`](/mysql-schema/mysql-schema.md#system-tables-related-to-runaway-queries)ログテーブルに書き込み制御を追加して、多数の同時書き込みによるオーバーヘッドを削減します[＃54434](https://github.com/pingcap/tidb/issues/54434) @ [HuSharp](https://github.com/HuSharp)
    -   内部テーブルに`Selection` 、 `Projection` 、または`Aggregation`演算子がある場合、デフォルトでインデックス結合をサポートします[＃47233](https://github.com/pingcap/tidb/issues/47233) @ [ウィノロス](https://github.com/winoros)
    -   特定のシナリオで`DELETE`操作につき TiKV から取得される列詳細の数を減らし、これらの操作のリソース オーバーヘッドを[＃38911](https://github.com/pingcap/tidb/issues/38911) @ [ウィノロス](https://github.com/winoros)に削減します。
    -   システム変数`tidb_auto_analyze_concurrency` [＃53460](https://github.com/pingcap/tidb/issues/53460) @ [ホーキングレイ](https://github.com/hawkingrei)を使用して、TiDB クラスター内の自動分析操作の同時実行性の設定をサポートします。
    -   内部関数のロジックを最適化して、多数の列を持つテーブルをクエリする際のパフォーマンスを向上します[＃52112](https://github.com/pingcap/tidb/issues/52112) @ [ラスティン170506](https://github.com/Rustin170506)
    -   フィルター条件[＃56005](https://github.com/pingcap/tidb/issues/56005) `a = 1 AND (a > 1 OR (a = 1 AND b = 2))` ～ `a = 1 AND b = 2`のよう[ガザルファミリーUSA](https://github.com/ghazalfamilyusa)簡素化する
    -   最適でない実行プランのリスクが高いシナリオでは、コストモデルでテーブルスキャンのコストを増やし、オプティマイザがインデックス[＃56012](https://github.com/pingcap/tidb/issues/56012) @ [テリー・パーセル](https://github.com/terry1purcell)を優先するようにします。
    -   TiDBは2つの引数のバリアント`MID(str, pos)` [＃52420](https://github.com/pingcap/tidb/issues/52420) @ [ドヴェーデン](https://github.com/dveeden)をサポートしています
    -   非バイナリ主キー[＃55660](https://github.com/pingcap/tidb/issues/55660) @ [lcwangchao](https://github.com/lcwangchao)を持つテーブルの TTL タスクの分割をサポート
    -   システムメタデータ関連ステートメントのパフォーマンスを最適化する[＃50305](https://github.com/pingcap/tidb/issues/50305) @ [ywqzzy](https://github.com/ywqzzy) @ [接線](https://github.com/tangenta) @ [ジョーチェン](https://github.com/joechenrh) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)
    -   自動分析操作用の新しい優先キューを実装して、分析パフォーマンスを向上させ、キュー[＃55906](https://github.com/pingcap/tidb/issues/55906) @ [ラスティン170506](https://github.com/Rustin170506)の再構築コストを削減します。
    -   統計モジュールがDDLイベント[＃55722](https://github.com/pingcap/tidb/issues/55722) @ [fzzf678](https://github.com/fzzf678) @ [ランス6716](https://github.com/lance6716) @ [ラスティン170506](https://github.com/Rustin170506)をサブスクライブできるようにDDL通知機能を導入する
    -   TiDB のアップグレード中に新しい TiDB ノードに DDL 所有権を強制的に引き継がせることで、古い TiDB ノードが所有権[＃51285](https://github.com/pingcap/tidb/pull/51285) @ [wjhuang2016](https://github.com/wjhuang2016)を引き継ぐことによる互換性の問題を回避します。
    -   クラスターレベルの散布リージョン[＃8424](https://github.com/tikv/pd/issues/8424) @ [リバー2000i](https://github.com/River2000i)をサポート

-   TiKV

    -   リージョン[＃17309](https://github.com/tikv/tikv/issues/17309) @ [LykxSassinator](https://github.com/LykxSassinator)が多すぎることによる余分なオーバーヘッドを回避するために、リージョンのデフォルト値を 96 MiB から 256 MiB に増やします。
    -   リージョンまたはTiKVインスタンスにおけるメモリ内悲観的ロックのメモリ使用量制限の設定をサポートします。ホットライトシナリオによって大量の悲観的ロックが発生する場合は、設定によってメモリ制限を増やすことができます。これにより、悲観的ロックのディスクへの書き込みによって発生するCPUおよびI/Oのオーバーヘッドを回避できます[＃17542](https://github.com/tikv/tikv/issues/17542) @ [cfzjywxk](https://github.com/cfzjywxk)
    -   Raft Engineに新しい`spill-dir`設定項目を導入し、 Raftログのマルチディスクstorageをサポートします。ホームディレクトリ（ `dir` ）があるディスクの容量が不足すると、 Raft Engineは自動的に新しいログを`spill-dir`に書き込み、システムの継続的な動作を保証します[＃17356](https://github.com/tikv/tikv/issues/17356) @ [LykxSassinator](https://github.com/LykxSassinator)
    -   RocksDB の圧縮トリガー メカニズムを最適化し、多数の DELETE バージョン[＃17269](https://github.com/tikv/tikv/issues/17269) @ [アンドレ・ムーシュ](https://github.com/AndreMouche)を処理するときにディスク領域の再利用を高速化します。
    -   書き込み操作のフロー制御構成を動的に変更するサポート[＃17395](https://github.com/tikv/tikv/issues/17395) @ [栄光](https://github.com/glorv)
    -   空のテーブルと小さなリージョン[＃17376](https://github.com/tikv/tikv/issues/17376) @ [LykxSassinator](https://github.com/LykxSassinator)のシナリオでのリージョン結合の速度を向上
    -   [パイプラインDML](https://github.com/pingcap/tidb/blob/release-8.4/docs/design/2024-01-09-pipelined-DML.md)resolved-ts を長期間ブロックするのを防ぐ[＃17459](https://github.com/tikv/tikv/issues/17459) @ [エキシウム](https://github.com/ekexium)

-   PD

    -   TiDB Lightning [＃7853](https://github.com/tikv/pd/issues/7853) @ [okJiang](https://github.com/okJiang)によるデータインポート中の TiKV ノードの正常なオフラインをサポート
    -   `pd-ctl`コマンド[＃8379](https://github.com/tikv/pd/issues/8379) @ [okJiang](https://github.com/okJiang)で`scatter-range`を`scatter-range-scheduler`に名前変更
    -   `grant-hot-leader-scheduler` [＃4903](https://github.com/tikv/pd/issues/4903) @ [lhy1024](https://github.com/lhy1024)の競合検出を追加

-   TiFlash

    -   `LENGTH()`と`ASCII()`関数[＃9344](https://github.com/pingcap/tiflash/issues/9344) @ [xzhangxian1008](https://github.com/xzhangxian1008)の実行効率を最適化
    -   分散storageとコンピューティング要求を処理するときにTiFlash が作成する必要があるスレッドの数を減らし、大量のそのような要求を処理するときにTiFlashコンピューティングノードのクラッシュを回避するのに役立ちます[＃9334](https://github.com/pingcap/tiflash/issues/9334) @ [ジンヘリン](https://github.com/JinheLin)
    -   パイプライン実行モデル[＃8869](https://github.com/pingcap/tiflash/issues/8869) @ [シーライズ](https://github.com/SeaRise)におけるタスク待機機構の強化
    -   JOIN演算子のキャンセルメカニズムを改善し、JOIN演算子がキャンセル要求にタイムリーに応答できるようにします[＃9430](https://github.com/pingcap/tiflash/issues/9430) @ [ウィンドトーカー](https://github.com/windtalker)

-   ツール

    -   バックアップと復元 (BR)

        -   `split-table`と`split-region-on-table`構成項目が`false` (デフォルト値) [＃53532](https://github.com/pingcap/tidb/issues/53532) @ [リーヴルス](https://github.com/Leavrth)であるクラスターにデータを復元する場合、テーブルごとにリージョンを分割しないようにして復元速度を向上させます。
        -   デフォルトで`RESTORE` SQL文を使用して空でないクラスタへの完全なデータ復元を無効にする[＃55087](https://github.com/pingcap/tidb/issues/55087) @ [生まれ変わった人](https://github.com/BornChanger)

## バグ修正 {#bug-fixes}

-   ティドブ

    -   `tidb_restricted_read_only`変数が`true` [＃53822](https://github.com/pingcap/tidb/issues/53822) [＃55373](https://github.com/pingcap/tidb/issues/55373) @ [定義2014](https://github.com/Defined2014)に設定されている場合にデッドロックが発生する可能性がある問題を修正しました
    -   TiDB が正常なシャットダウン中に自動コミットトランザクションの完了を待たない問題を修正[＃55464](https://github.com/pingcap/tidb/issues/55464) @ [ヤンケオ](https://github.com/YangKeao)
    -   TTLジョブ実行中に値を`tidb_ttl_delete_worker_count`減らすとジョブが[＃55561](https://github.com/pingcap/tidb/issues/55561) @ [lcwangchao](https://github.com/lcwangchao)で完了しなくなる問題を修正しました
    -   テーブルのインデックスに生成された列が含まれている場合、 `ANALYZE`ステートメント[＃55438](https://github.com/pingcap/tidb/issues/55438) @ [ホーキングレイ](https://github.com/hawkingrei)を介してテーブルの統計情報を収集するときに`Unknown column 'column_name' in 'expression'`エラーが発生する可能性がある問題を修正しました。
    -   冗長なコードを削減するために、統計に関連する不要な設定を廃止する[＃55043](https://github.com/pingcap/tidb/issues/55043) @ [ラスティン170506](https://github.com/Rustin170506)
    -   相関サブクエリと CTE [＃55551](https://github.com/pingcap/tidb/issues/55551) @ [グオシャオゲ](https://github.com/guo-shaoge)を含むクエリを実行すると、TiDB がハングしたり、誤った結果が返されたりする問題を修正しました。
    -   `lite-init-stats`無効にすると統計が同期的にロードされない可能性がある問題を修正[＃54532](https://github.com/pingcap/tidb/issues/54532) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   `UPDATE`または`DELETE`ステートメントに再帰 CTE が含まれている場合、ステートメントがエラーを報告したり、 [＃55666](https://github.com/pingcap/tidb/issues/55666) @ [時間と運命](https://github.com/time-and-fate)が有効にならない可能性がある問題を修正しました。
    -   ウィンドウ関数を含むSQLバインディングが場合によっては有効にならない可能性がある問題を修正[＃55981](https://github.com/pingcap/tidb/issues/55981) @ [ウィノロス](https://github.com/winoros)
    -   統計[＃55684](https://github.com/pingcap/tidb/issues/55684) @ [ウィノロス](https://github.com/winoros)を初期化するときに、非バイナリ照合の文字列列の統計の読み込みに失敗する可能性がある問題を修正しました。
    -   クエリ条件`column IS NULL` [＃56116](https://github.com/pingcap/tidb/issues/56116) @ [ホーキングレイ](https://github.com/hawkingrei)でユニークインデックスにアクセスするときに、オプティマイザが行数を誤って 1 と推定する問題を修正しました。
    -   クエリに`(... AND ...) OR (... AND ...) ...` [＃54323](https://github.com/pingcap/tidb/issues/54323) @ [時間と運命](https://github.com/time-and-fate)のようなフィルタ条件が含まれている場合、オプティマイザが行数推定に最適な複数列統計情報を使用しない問題を修正しました。
    -   クエリに利用可能なインデックスマージ実行プラン[＃56217](https://github.com/pingcap/tidb/issues/56217) @ [アイリンキッド](https://github.com/AilinKid)がある場合に`read_from_storage`ヒントが有効にならない可能性がある問題を修正しました
    -   `IndexNestedLoopHashJoin` [＃49692](https://github.com/pingcap/tidb/issues/49692) @ [ソロツグ](https://github.com/solotzg)のデータ競合問題を修正
    -   `INFORMATION_SCHEMA.STATISTICS`テーブルの`SUB_PART`値が`NULL` [＃55812](https://github.com/pingcap/tidb/issues/55812) @ [定義2014](https://github.com/Defined2014)になる問題を修正しました
    -   DML文にネストされた生成列[＃53967](https://github.com/pingcap/tidb/issues/53967) @ [wjhuang2016](https://github.com/wjhuang2016)が含まれている場合にエラーが発生する問題を修正しました
    -   除算演算において最小表示長を持つ整数型のデータで除算結果が[＃55837](https://github.com/pingcap/tidb/issues/55837) @ [ウィンドトーカー](https://github.com/windtalker)にオーバーフローする可能性がある問題を修正しました。
    -   TopN演算子に続く演算子がメモリ制限を超えたときにフォールバックアクションをトリガーできない問題を修正[＃56185](https://github.com/pingcap/tidb/issues/56185) @ [xzhangxian1008](https://github.com/xzhangxian1008)
    -   ソート演算子の`ORDER BY`列目に定数[＃55344](https://github.com/pingcap/tidb/issues/55344) @ [xzhangxian1008](https://github.com/xzhangxian1008)が含まれている場合に、その列が動かなくなる問題を修正しました。
    -   インデックスを追加するときに、PDリーダーを強制終了した後に`8223 (HY000)`エラーが発生し、テーブル内のデータが[＃55488](https://github.com/pingcap/tidb/issues/55488) @ [接線](https://github.com/tangenta)で不整合になる問題を修正しました。
    -   履歴 DDL ジョブ[＃55711](https://github.com/pingcap/tidb/issues/55711) @ [ジョッカウ](https://github.com/joccau)に関する情報をリクエストすると、DDL 履歴ジョブが多すぎるために OOM が発生する問題を修正しました。
    -   グローバルソートが有効でリージョンサイズが96 MiB [＃55374](https://github.com/pingcap/tidb/issues/55374) @ [ランス6716](https://github.com/lance6716)を超えると`IMPORT INTO`実行が停止する問題を修正
    -   一時テーブルで`IMPORT INTO`実行すると TiDB がクラッシュする問題を修正[＃55970](https://github.com/pingcap/tidb/issues/55970) @ [D3ハンター](https://github.com/D3Hunter)
    -   ユニークインデックスを追加すると`duplicate entry`エラー[＃56161](https://github.com/pingcap/tidb/issues/56161) @ [接線](https://github.com/tangenta)が発生する問題を修正
    -   TiKVが810秒以上ダウンしている場合、 TiDB LightningがすべてのKVペアを取り込まず、テーブル[＃55808](https://github.com/pingcap/tidb/issues/55808) @ [ランス6716](https://github.com/lance6716)のデータが不整合になる問題を修正しました。
    -   `CREATE TABLE LIKE`文がキャッシュされたテーブル[＃56134](https://github.com/pingcap/tidb/issues/56134) @ [天菜麻緒](https://github.com/tiancaiamao)に使用できない問題を修正
    -   CTE [＃56198](https://github.com/pingcap/tidb/pull/56198) @ [ドヴェーデン](https://github.com/dveeden)の`FORMAT()`式に関するわかりにくい警告メッセージを修正しました
    -   パーティションテーブル[＃56094](https://github.com/pingcap/tidb/issues/56094) @ [ミョンス](https://github.com/mjonss)を作成するときに、列の種類の制限が`CREATE TABLE`と`ALTER TABLE`の間で一致しない問題を修正しました。
    -   `INFORMATION_SCHEMA.RUNAWAY_WATCHES`表[＃54770](https://github.com/pingcap/tidb/issues/54770) @ [HuSharp](https://github.com/HuSharp)の誤った時間タイプを修正

-   TiKV

    -   マスターキーがキー管理サービス (KMS) [＃17410](https://github.com/tikv/tikv/issues/17410) @ [hhwyt](https://github.com/hhwyt)に保存されているときにマスターキーのローテーションを妨げる問題を修正しました
    -   大きなテーブルやパーティション[＃17304](https://github.com/tikv/tikv/issues/17304) @ [コナー1996](https://github.com/Connor1996)を削除した後に発生する可能性のあるトラフィック制御の問題を修正しました
    -   古いレプリカがRaftスナップショットを処理するときに、遅い分割操作と新しいレプリカ[＃17469](https://github.com/tikv/tikv/issues/17469) @ [ヒビシェン](https://github.com/hbisheng)の即時削除によってトリガーされ、TiKV がpanicになる可能性がある問題を修正しました。

-   TiFlash

    -   テーブルに無効な文字[＃9461](https://github.com/pingcap/tiflash/issues/9461) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)を含むデフォルト値を持つビット型の列が含まれている場合、 TiFlash がテーブル スキーマを解析できない問題を修正しました。
    -   複数のリージョンがスナップショット[＃9329](https://github.com/pingcap/tiflash/issues/9329) @ [カルビンネオ](https://github.com/CalvinNeo)を同時に適用しているときに発生する誤ったリージョン重複チェックの失敗によりTiFlash がpanicになる可能性がある問題を修正しました。
    -   TiFlashでサポートされていない一部の JSON関数がTiFlash [＃9444](https://github.com/pingcap/tiflash/issues/9444) @ [ウィンドトーカー](https://github.com/windtalker)にプッシュダウンされる問題を修正しました

-   ツール

    -   バックアップと復元 (BR)

        -   TiDBノードが停止したときに監視のPITRチェックポイント間隔が異常に増加し、実際の状況を反映しない問題を修正[＃42419](https://github.com/pingcap/tidb/issues/42419) @ [ユジュンセン](https://github.com/YuJuncen)
        -   バックアッププロセス中に TiKV が応答しなくなった場合にバックアップタスクが停止する可能性がある問題を修正[＃53480](https://github.com/pingcap/tidb/issues/53480) @ [リーヴルス](https://github.com/Leavrth)
        -   ログバックアップが有効になっているときにBRログに機密の資格情報が出力される可能性がある問題を修正[＃55273](https://github.com/pingcap/tidb/issues/55273) @ [リドリスR](https://github.com/RidRisR)
        -   ログバックアップ PITR タスクが失敗して停止すると、そのタスクに関連するセーフポイントが PD [＃17316](https://github.com/tikv/tikv/issues/17316) @ [リーヴルス](https://github.com/Leavrth)で適切にクリアされない問題を修正しました。

    -   TiDB データ移行 (DM)

        -   複数の DM マスターノードが同時にリーダーになり、データの不整合が発生する可能性がある問題を修正しました[＃11602](https://github.com/pingcap/tiflow/issues/11602) @ [GMHDBJD](https://github.com/GMHDBJD)
        -   DMが`ALTER DATABASE`ステートメントを処理するときにデフォルトのデータベースを設定せず、レプリケーションエラー[＃11503](https://github.com/pingcap/tiflow/issues/11503) @ [ランス6716](https://github.com/lance6716)が発生する問題を修正しました。

    -   TiDB Lightning

        -   2つのインスタンスが同時に並列インポートタスクを開始し、同じタスクID [＃55384](https://github.com/pingcap/tidb/issues/55384) @ [杉本英](https://github.com/ei-sugimoto)が割り当てられている場合に、 TiDB Lightningが`verify allocator base failed`エラーを報告する問題を修正しました。

## 寄稿者 {#contributors}

TiDB コミュニティの以下の貢献者に感謝いたします。

-   [杉本英](https://github.com/ei-sugimoto)
-   [エルトシア](https://github.com/eltociear)
-   [グオショウヤン](https://github.com/guoshouyan) (初回投稿者)
-   [ジャックL9u](https://github.com/JackL9u)
-   [カフカ1991](https://github.com/kafka1991) (初回投稿者)
-   [qingfeng777](https://github.com/qingfeng777)
-   [サンバRGB](https://github.com/samba-rgb) (初回投稿者)
-   [シーライズ](https://github.com/SeaRise)
-   [ツジエモン](https://github.com/tuziemon) (初回投稿者)
-   [キシプロト](https://github.com/xyproto) (初回投稿者)
