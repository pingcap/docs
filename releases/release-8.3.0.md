---
title: TiDB 8.3.0 Release Notes
summary: TiDB 8.3.0 の新機能、互換性の変更、改善、バグ修正について説明します。
---

# TiDB 8.3.0 リリースノート {#tidb-8-3-0-release-notes}

発売日: 2024年8月22日

TiDB バージョン: 8.3.0

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v8.3/quick-start-with-tidb)

8.3.0 では、次の主要な機能と改善が導入されています。

<table><thead><tr><th>カテゴリ</th><th>機能/拡張機能</th><th>説明</th></tr></thead><tbody><tr><td rowspan="3">スケーラビリティとパフォーマンス</td><td><a href="https://docs.pingcap.com/tidb/v8.3/partitioned-table#global-indexes">パーティションテーブルのグローバルインデックス（実験的）</a></td><td>グローバル インデックスを使用すると、パーティション化されていない列の取得効率を効果的に向上でき、一意のキーにパーティション キーが含まれていなければならないという制限がなくなります。この機能により、TiDB パーティション テーブルの使用シナリオが拡張され、データ移行に必要なアプリケーション変更作業の一部が回避されます。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v8.3/system-variables#tidb_opt_projection_push_down-new-in-v610">storage子の<code>Projection</code>エンジンへのデフォルトのプッシュダウン</a></td><td><code>Projection</code>演算子をstorageエンジンにプッシュダウンすると、ノード間のデータ転送を減らしながら、storageノード間で負荷を分散できます。この最適化により、特定の SQL クエリの実行時間が短縮され、データベース全体のパフォーマンスが向上します。</td></tr><tr><td><a href="https://docs.pingcap.com/tidb/v8.3/statistics#collect-statistics-on-some-columns">統計を収集する際に不要な列を無視する</a></td><td>TiDB は、オプティマイザが必要な情報を確実に取得できるという前提の下、統計収集を高速化し、統計の適時性を向上させ、最適な実行プランが選択されるようにすることで、クラスターのパフォーマンスを向上させます。同時に、TiDB はシステム オーバーヘッドを削減し、リソースの使用率を向上させます。</td></tr><tr><td rowspan="1">信頼性と可用性</td><td><a href="https://docs.pingcap.com/tidb/v8.3/tiproxy-overview">TiProxyに組み込まれた仮想IP管理</a></td><td>TiProxy には、組み込みの仮想 IP 管理機能が導入されています。設定すると、外部のプラットフォームやツールに依存せずに、自動仮想 IP 切り替えがサポートされます。この機能により、TiProxy の導入が簡素化され、データベース アクセスレイヤーの複雑さが軽減されます。</td></tr></tbody></table>

## 機能の詳細 {#feature-details}

### パフォーマンス {#performance}

-   オプティマイザは、デフォルトで`Projection`演算子をstorageエンジンにプッシュダウンすることを許可します[＃51876](https://github.com/pingcap/tidb/issues/51876) @ [いびん87](https://github.com/yibin87)

    `Projection`演算子をstorageエンジンにプッシュダウンすると、コンピューティング エンジンとstorageエンジン間のデータ転送が削減され、SQL 実行パフォーマンスが向上します。これは、 [JSONクエリ関数](/functions-and-operators/json-functions/json-functions-search.md)または[JSON値属性関数](/functions-and-operators/json-functions/json-functions-return.md)含むクエリで特に効果的です。v8.3.0 以降、TiDB は、この機能を制御するシステム変数のデフォルト値[`tidb_opt_projection_push_down`](/system-variables.md#tidb_opt_projection_push_down-new-in-v610)を`OFF`から`ON`に変更することで、 `Projection`演算子のプッシュダウン機能をデフォルトで有効にします。この機能を有効にすると、オプティマイザーは、適格な JSON クエリ関数と JSON 値属性関数をstorageエンジンに自動的にプッシュダウンします。

    詳細については[ドキュメント](/system-variables.md#tidb_opt_projection_push_down-new-in-v610)参照してください。

-   KV（キー値）リクエストのバッチ処理戦略を最適化する[＃55206](https://github.com/pingcap/tidb/issues/55206) @ [ジグアン](https://github.com/zyguan)

    TiDB は、TiKV に KV 要求を送信してデータを取得します。KV 要求を一括してバッチ処理すると、実行パフォーマンスが大幅に向上します。v8.3.0 より前の TiDB のバッチ処理戦略は効率が悪かったです。v8.3.0 以降、TiDB では既存のものに加えて、より効率的なバッチ処理戦略がいくつか導入されています。1 [`tikv-client.batch-policy`](/tidb-configuration-file.md#batch-policy-new-in-v830)構成項目を使用して、さまざまなワークロードに対応するために、さまざまなバッチ処理戦略を構成できます。

    詳細については[ドキュメント](/tidb-configuration-file.md#batch-policy-new-in-v830)参照してください。

-   TiFlashは、高NDVデータ[＃9196](https://github.com/pingcap/tiflash/issues/9196) @ [グオシャオゲ](https://github.com/guo-shaoge)のパフォーマンスを向上させるHashAgg集計計算モードを導入しました。

    v8.3.0 より前のTiFlashでは、NDV (個別値の数) が高いデータを処理する場合、HashAgg 集計の最初の段階で集計計算の効率が低くなります。v8.3.0 以降、 TiFlash は複数の HashAgg 集計計算モードを導入し、さまざまなデータ特性の集計パフォーマンスを向上させます。必要な HashAgg 集計計算モードを選択するには、 [`tiflash_hashagg_preaggregation_mode`](/system-variables.md#tiflash_hashagg_preaggregation_mode-new-in-v830)システム変数を設定できます。

    詳細については[ドキュメント](/system-variables.md#tiflash_hashagg_preaggregation_mode-new-in-v830)参照してください。

-   統計を収集するときに不要な列を無視する[＃53567](https://github.com/pingcap/tidb/issues/53567) @ [ハイラスティン](https://github.com/Rustin170506)

    オプティマイザーが実行プランを生成する場合、フィルター条件の列、結合キーの列、集計に使用される列など、一部の列の統計のみが必要です。v8.3.0 以降、TiDB は SQL ステートメントで使用される列の履歴レコードを継続的に監視します。デフォルトでは、TiDB はインデックス付きの列と、統計収集が必要であると判断された列の統計のみを収集します。これにより、統計の収集が高速化され、不要なリソース消費が回避されます。

    クラスターを v8.3.0 より前のバージョンから v8.3.0 以降にアップグレードすると、TiDB はデフォルトで元の動作、つまりすべての列の統計を収集します。この機能を有効にするには、システム変数[`tidb_analyze_column_options`](/system-variables.md#tidb_analyze_column_options-new-in-v830)を`PREDICATE`に手動で設定する必要があります。新しくデプロイされたクラスターでは、この機能はデフォルトで有効になっています。

    ランダムクエリを多数実行する分析システムの場合、システム変数[`tidb_analyze_column_options`](/system-variables.md#tidb_analyze_column_options-new-in-v830)を`ALL`に設定してすべての列の統計を収集し、ランダムクエリのパフォーマンスを確保できます。その他のタイプのシステムでは、必要な列の統計のみを収集するために、デフォルト設定 ( `PREDICATE` ) の[`tidb_analyze_column_options`](/system-variables.md#tidb_analyze_column_options-new-in-v830)維持することをお勧めします。

    詳細については[ドキュメント](/statistics.md#collect-statistics-on-some-columns)参照してください。

-   一部のシステムテーブルのクエリパフォーマンスを向上[＃50305](https://github.com/pingcap/tidb/issues/50305) @ [タンジェンタ](https://github.com/tangenta)

    以前のバージョンでは、クラスターのサイズが大きくなり、テーブル数が多くなると、システム テーブルのクエリのパフォーマンスが低下しました。

    v8.0.0 では、次の 4 つのシステム テーブルに対してクエリ パフォーマンスが最適化されています。

    -   `INFORMATION_SCHEMA.TABLES`
    -   `INFORMATION_SCHEMA.STATISTICS`
    -   `INFORMATION_SCHEMA.KEY_COLUMN_USAGE`
    -   `INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS`

    v8.3.0 では、次のシステム テーブルのクエリ パフォーマンスが最適化され、v8.2.0 と比較してパフォーマンスが数倍向上します。

    -   `INFORMATION_SCHEMA.CHECK_CONSTRAINTS`
    -   `INFORMATION_SCHEMA.COLUMNS`
    -   `INFORMATION_SCHEMA.PARTITIONS`
    -   `INFORMATION_SCHEMA.SCHEMATA`
    -   `INFORMATION_SCHEMA.SEQUENCES`
    -   `INFORMATION_SCHEMA.TABLE_CONSTRAINTS`
    -   `INFORMATION_SCHEMA.TIDB_CHECK_CONSTRAINTS`
    -   `INFORMATION_SCHEMA.TiDB_INDEXES`
    -   `INFORMATION_SCHEMA.TIDB_INDEX_USAGE`
    -   `INFORMATION_SCHEMA.VIEWS`

-   パーティション式が`EXTRACT(YEAR_MONTH...)`関数を使用する場合にパーティション プルーニングをサポートして、クエリのパフォーマンスを向上します[＃54209](https://github.com/pingcap/tidb/pull/54209) @ [ミョンス](https://github.com/mjonss)

    以前のバージョンでは、パーティション式で`EXTRACT(YEAR_MONTH...)`関数が使用される場合、パーティション プルーニングはサポートされず、クエリのパフォーマンスが低下しました。v8.3.0 以降では、パーティション式で`EXTRACT(YEAR_MONTH...)`関数が使用される場合にパーティション プルーニングがサポートされ、クエリのパフォーマンスが向上します。

    詳細については[ドキュメント](/partition-pruning.md#scenario-three)参照してください。

-   `CREATE TABLE`のパフォーマンスを1.4倍、 `CREATE DATABASE`パフォーマンスを2.1倍、 `ADD COLUMN`パフォーマンスを[＃54436](https://github.com/pingcap/tidb/issues/54436)倍に向上させます[D3ハンター](https://github.com/D3Hunter)

    TiDB v8.0.0 では、バッチ テーブル作成シナリオでのテーブル作成パフォーマンスを向上させるために、システム変数[`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-new-in-v800)が導入されています。v8.3.0 では、単一のデータベースで 10 セッションを通じて同時にテーブル作成の DDL ステートメントを送信すると、v8.2.0 と比較してパフォーマンスが 1.4 倍向上します。

    v8.3.0 では、バッチ実行における一般的な DDL のパフォーマンスが v8.2.0 と比較して向上しています。10 `CREATE DATABASE`同時実行のパフォーマンスは、v8.1.0 と比較して 19 倍、v8.2.0 と比較して 2.1 倍向上しています。10 セッションを使用して、同じデータベース内の複数のテーブルにバッチで列 ( `ADD COLUMN` ) を追加するパフォーマンスは、v8.1.0 と比較して 10 倍、v8.2.0 と比較して 2.1 倍向上しています。同じデータベース内の複数のテーブルで 10 セッションを使用して`ADD COLUMN`を実行するパフォーマンスは、v8.1.0 と比較して 10 倍、v8.2.0 と比較して 2 倍向上しています。

    詳細については[ドキュメント](/system-variables.md#tidb_enable_fast_create_table-new-in-v800)参照してください。

-   パーティションテーブルはグローバルインデックスをサポートします (実験的) [＃45133](https://github.com/pingcap/tidb/issues/45133) @ [ミョンス](https://github.com/mjonss) @ [定義2014](https://github.com/Defined2014) @ [ジフハウス](https://github.com/jiyfhust) @ [L-メープル](https://github.com/L-maple)

    以前のバージョンのパーティション テーブルでは、グローバル インデックスがサポートされていないため、いくつかの制限があります。たとえば、一意のキーは、テーブルのパーティション式のすべての列を使用する必要があります。クエリ条件でパーティション キーが使用されていない場合、クエリはすべてのパーティションをスキャンするため、パフォーマンスが低下します。v7.6.0 以降では、グローバル インデックス機能を有効にするためにシステム変数[`tidb_enable_global_index`](/system-variables.md#tidb_enable_global_index-new-in-v760)が導入されています。ただし、この機能は当時開発中であったため、有効にすることはお勧めしません。

    v8.3.0 以降、グローバル インデックス機能は実験的機能としてリリースされています。キーワード`Global`を使用してパーティションテーブルにグローバル インデックスを明示的に作成すると、一意のキーがテーブルのパーティション式のすべての列を使用する必要があるという制限がなくなり、柔軟なビジネス ニーズを満たすことができます。グローバル インデックスは、パーティション キーを含まないクエリのパフォーマンスも向上させます。

    詳細については[ドキュメント](/partitioned-table.md#global-indexes)参照してください。

### 信頼性 {#reliability}

-   ストリーミング カーソル結果セットのサポート (実験的) [＃54526](https://github.com/pingcap/tidb/issues/54526) @ [ヤンケオ](https://github.com/YangKeao)

    アプリケーション コードが[カーソルフェッチ](/develop/dev-guide-connection-parameters.md#use-streamingresult-to-get-the-execution-result)使用して結果セットを取得する場合、TiDB は通常、最初に完全な結果セットをメモリに保存し、次にデータをバッチでクライアントに返します。結果セットが大きすぎる場合、TiDB は結果を一時的にハード ディスクに書き込むことがあります。

    v8.3.0 以降では、システム変数[`tidb_enable_lazy_cursor_fetch`](/system-variables.md#tidb_enable_lazy_cursor_fetch-new-in-v830)を`ON`に設定すると、TiDB はすべてのデータを TiDB ノードに読み取らず、クライアントが読み取るにつれて徐々にデータを TiDB ノードに読み取ります。TiDB が大きな結果セットを処理する場合、この機能により TiDB ノードのメモリ使用量が削減され、クラスターの安定性が向上します。

    詳細については[ドキュメント](/system-variables.md#tidb_enable_lazy_cursor_fetch-new-in-v830)参照してください。

-   SQL実行プランバインディングの強化[＃55280](https://github.com/pingcap/tidb/issues/55280) [＃55343](https://github.com/pingcap/tidb/issues/55343) @ [時間と運命](https://github.com/time-and-fate)

    OLTP シナリオでは、ほとんどの SQL ステートメントの最適な実行プランは固定されています。アプリケーション内の重要な SQL ステートメントに SQL 実行プラン バインディングを実装すると、実行プランが悪化する可能性が減り、システムの安定性が向上します。大量の SQL 実行プラン バインディングを作成するという要件を満たすために、TiDB は SQL バインディングの機能とエクスペリエンスを強化し、次の機能を提供します。

    -   単一の SQL ステートメントを使用して、複数の履歴実行プランから SQL 実行プラン バインディングを作成し、バインディングの作成効率を向上させます。
    -   SQL 実行プラン バインディングは、より多くのオプティマイザ ヒントをサポートし、複雑な実行プランの変換方法を最適化するため、実行プランの復元におけるバインディングの安定性が向上します。

    詳細については[ドキュメント](/sql-plan-management.md)参照してください。

### 可用性 {#availability}

-   TiProxyは組み込みの仮想IP管理[＃583](https://github.com/pingcap/tiproxy/issues/583) @ [翻訳者](https://github.com/djshow832)をサポートします

    v8.3.0 より前では、高可用性のためにプライマリ/セカンダリ モードを使用する場合、TiProxy では仮想 IP アドレスを管理するための追加コンポーネントが必要でした。v8.3.0 以降、TiProxy は組み込みの仮想 IP 管理をサポートします。プライマリ/セカンダリ モードでは、プライマリ ノードがフェールオーバーすると、新しいプライマリ ノードは指定された仮想 IP に自動的にバインドされ、クライアントが常に仮想 IP を介して利用可能な TiProxy に接続できるようになります。

    仮想 IP 管理を有効にするには、TiProxy 構成項目[`ha.virtual-ip`](/tiproxy/tiproxy-configuration.md#virtual-ip)を使用して仮想 IP アドレスを指定し、 [`ha.interface`](/tiproxy/tiproxy-configuration.md#interface)使用して仮想 IP をバインドするネットワーク インターフェイスを指定します。仮想 IP は、これらの構成項目の両方が設定されている場合にのみ、TiProxy インスタンスにバインドされます。

    詳細については[ドキュメント](/tiproxy/tiproxy-overview.md)参照してください。

### 構文 {#sql}

-   `SELECT LOCK IN SHARE MODE`排他ロック[＃54999](https://github.com/pingcap/tidb/issues/54999) @ [翻訳](https://github.com/cfzjywxk)へのアップグレードをサポート

    TiDB はまだ`SELECT LOCK IN SHARE MODE`サポートしていません。v8.3.0 以降、TiDB は`SELECT LOCK IN SHARE MODE`排他ロックにアップグレードして`SELECT LOCK IN SHARE MODE`のサポートを有効にすることをサポートしています。新しいシステム変数[`tidb_enable_shared_lock_promotion`](/system-variables.md#tidb_enable_shared_lock_promotion-new-in-v830)使用して、この機能を有効にするかどうかを制御できます。

    詳細については[ドキュメント](/system-variables.md#tidb_enable_shared_lock_promotion-new-in-v830)参照してください。

### 可観測性 {#observability}

-   初期統計[＃53564](https://github.com/pingcap/tidb/issues/53564) @ [ホーキングレイ](https://github.com/hawkingrei)の読み込みの進行状況を表示します

    TiDB は起動時に基本統計を読み込みます。テーブルやパーティションが多数あるシナリオでは、このプロセスに長い時間がかかることがあります。構成項目[`force-init-stats`](/tidb-configuration-file.md#force-init-stats-new-in-v657-and-v710)が`ON`に設定されている場合、TiDB は初期統計が読み込まれるまでサービスを提供しません。この場合、読み込みプロセスを観察してサービスの開始時間を見積もる必要があります。

    v8.3.0 以降、TiDB は初期統計のロードの進行状況を段階的にログに出力、実行ステータスを把握できるようにしました。外部ツールにフォーマットされた結果を提供するために、TiDB は追加の[監視API](/tidb-monitoring-api.md)を追加し、起動フェーズのいつでも初期統計のロードの進行状況を取得できるようにしました。

-   リクエストユニット (RU) 設定に関するメトリックを追加[＃8444](https://github.com/tikv/pd/issues/8444) @ [ノルーシュ](https://github.com/nolouch)

### Security {#security}

-   PD ログ編集を強化[＃8305](https://github.com/tikv/pd/issues/8305) @ [じゃがいも](https://github.com/JmPotato)

    TiDB v8.0.0 では、ログ編集が強化され、TiDB ログ内のユーザー データを`‹ ›`でマークできるようになりました。マークされたログに基づいて、ログを表示するときにマークされた情報を編集するかどうかを決定できるため、ログ編集の柔軟性が向上します。v8.2.0 では、 TiFlashで同様のログ編集強化が実装されています。

    v8.3.0 では、PD は同様のログ編集拡張機能を実装しています。この機能を使用するには、PD 構成項目の値を`security.redact-info-log`から`"marker"`に設定できます。

    詳細については[ドキュメント](/log-redaction.md#log-redaction-in-pd-side)参照してください。

-   TiKV ログ編集[＃17206](https://github.com/tikv/tikv/issues/17206) @ [ルーカスリアン](https://github.com/LykxSassinator)を強化

    TiDB v8.0.0 では、ログ編集が強化され、TiDB ログ内のユーザー データを`‹ ›`でマークできるようになりました。マークされたログに基づいて、ログを表示するときにマークされた情報を編集するかどうかを決定できるため、ログ編集の柔軟性が向上します。v8.2.0 では、 TiFlashで同様のログ編集強化が実装されています。

    v8.3.0 では、TiKV は同様のログ編集拡張機能を実装しています。この機能を使用するには、TiKV 構成項目の値を`security.redact-info-log`から`"marker"`に設定できます。

    詳細については[ドキュメント](/log-redaction.md#log-redaction-in-tikv-side)参照してください。

### データ移行 {#data-migration}

-   TiCDC は双方向レプリケーション (BDR) モードでの DDL ステートメントのレプリケーションをサポートしています (GA) [＃10301](https://github.com/pingcap/tiflow/issues/10301) [＃48519](https://github.com/pingcap/tidb/issues/48519) @ [ok江](https://github.com/okJiang) @ [アズドンメン](https://github.com/asddongmen)

    TiCDC v7.6.0 では、双方向レプリケーションが構成された DDL ステートメントのレプリケーションが導入されました。以前は、DDL ステートメントの双方向レプリケーションは TiCDC でサポートされていなかったため、TiCDC の双方向レプリケーションのユーザーは、両方の TiDB クラスターで DDL ステートメントを個別に実行する必要がありました。この機能を使用すると、クラスターに`PRIMARY` BDR ロールを割り当てた後、TiCDC はそのクラスターから`SECONDARY`クラスターに DDL ステートメントをレプリケートできます。

    v8.3.0 では、この機能が一般提供 (GA) されます。

    詳細については[ドキュメント](/ticdc/ticdc-bidirectional-replication.md)参照してください。

## 互換性の変更 {#compatibility-changes}

> **注記：**
>
> このセクションでは、v8.2.0 から現在のバージョン (v8.3.0) にアップグレードするときに知っておく必要のある互換性の変更について説明します。v8.1.0 以前のバージョンから現在のバージョンにアップグレードする場合は、中間バージョンで導入された互換性の変更も確認する必要がある可能性があります。

### 行動の変化 {#behavior-changes}

-   コマンドの誤使用を避けるため、 `pd-ctl`プレフィックスマッチングメカニズムをキャンセルします。たとえば、 `store remove-tombstone` `store remove` [＃8413](https://github.com/tikv/pd/issues/8413) @ [翻訳者](https://github.com/lhy1024)では呼び出せません。

### システム変数 {#system-variables}

| 変数名                                                                                                           | タイプを変更   | 説明                                                                                                                                                                                                                                                                                                                  |
| ------------------------------------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size)                                 | 修正済み     | SESSION スコープを追加します。                                                                                                                                                                                                                                                                                                 |
| [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt)                                 | 修正済み     | SESSION スコープを追加します。                                                                                                                                                                                                                                                                                                 |
| [`tidb_gc_concurrency`](/system-variables.md#tidb_gc_concurrency-new-in-v50)                                  | 修正済み     | v8.3.0 以降、この変数は[ガベージコレクション (GC)](/garbage-collection-overview.md)プロセスの[ロックを解決する](/garbage-collection-overview.md#resolve-locks)番目と[範囲を削除](/garbage-collection-overview.md#delete-ranges)番目のステップでの同時スレッドの数を制御します。v8.3.0 より前では、この変数は[ロックを解決する](/garbage-collection-overview.md#resolve-locks)番目のステップでのスレッドの数のみを制御します。 |
| [`tidb_low_resolution_tso`](/system-variables.md#tidb_low_resolution_tso)                                     | 修正済み     | GLOBAL スコープを追加します。                                                                                                                                                                                                                                                                                                  |
| [`tidb_opt_projection_push_down`](/system-variables.md#tidb_opt_projection_push_down-new-in-v610)             | 修正済み     | GLOBAL スコープを追加し、変数値をクラスターに保持します。さらにテストを行った後、デフォルト値を`OFF`から`ON`に変更します。つまり、オプティマイザーは`Projection` TiKV コプロセッサにプッシュダウンできます。                                                                                                                                                                                             |
| [`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-new-in-v800)                           | 修正済み     | 値の範囲は`0`または`[536870912, 9223372036854775807]`に変更されました。キャッシュ サイズを小さく設定しすぎてパフォーマンスが低下するのを避けるため、最小値は`536870912`バイト (つまり 512 MiB) です。                                                                                                                                                                                   |
| [`tidb_analyze_column_options`](/system-variables.md#tidb_analyze_column_options-new-in-v830)                 | 新しく追加された | `ANALYZE TABLE`ステートメントの動作を制御します。デフォルト値`PREDICATE`に設定すると、 [述語列](/statistics.md#collect-statistics-on-some-columns)の統計のみが収集され、 `ALL`に設定すると、すべての列の統計が収集されます。                                                                                                                                                           |
| [`tidb_enable_lazy_cursor_fetch`](/system-variables.md#tidb_enable_lazy_cursor_fetch-new-in-v830)             | 新しく追加された | [カーソルフェッチ](/develop/dev-guide-connection-parameters.md#use-streamingresult-to-get-the-execution-result)機能の動作を制御します。                                                                                                                                                                                                 |
| [`tidb_enable_shared_lock_promotion`](/system-variables.md#tidb_enable_shared_lock_promotion-new-in-v830)     | 新しく追加された | 共有ロックを排他ロックにアップグレードする機能を有効にするかどうかを制御します。この変数のデフォルト値は`OFF`で、共有ロックを排他ロックにアップグレードする機能が無効であることを意味します。                                                                                                                                                                                                                   |
| [`tiflash_hashagg_preaggregation_mode`](/system-variables.md#tiflash_hashagg_preaggregation_mode-new-in-v830) | 新しく追加された | TiFlashにプッシュダウンされる 2 段階または 3 段階の HashAgg 操作の最初の段階で使用される事前集計戦略を制御します。                                                                                                                                                                                                                                                |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーションパラメータ                                                                                        | タイプを変更   | 説明                                                                                                                                                      |
| -------------- | ------------------------------------------------------------------------------------------------------ | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ティビ            | [`tikv-client.batch-policy`](/tidb-configuration-file.md#batch-policy-new-in-v830)                     | 新しく追加された | TiDB から TiKV へのリクエストのバッチ処理戦略を制御します。                                                                                                                     |
| PD             | [`security.redact-info-log`](/pd-configuration-file.md#redact-info-log-new-in-v50)                     | 修正済み     | PD 構成項目の値を`security.redact-info-log`から`"marker"`設定して、ログ内の機密情報を直接シールドするのではなく、 `‹ ›`でマークすることをサポートします。7 オプション`"marker"`使用すると、編集ルールをカスタマイズできます。             |
| ティクヴ           | [`security.redact-info-log`](/tikv-configuration-file.md#redact-info-log-new-in-v408)                  | 修正済み     | TiKV 構成項目の値を`security.redact-info-log`から`"marker"`設定して、ログ内の機密情報を直接シールドするのではなく、 `‹ ›`でマークすることをサポートします。7 オプション`"marker"`使用すると、編集ルールをカスタマイズできます。           |
| TiFlash        | [`security.redact-info-log`](/tiflash/tiflash-configuration.md#configure-the-tiflash-learnertoml-file) | 修正済み     | TiFlash Learner構成項目の値を`security.redact-info-log`から`"marker"`設定して、ログ内の機密情報を直接保護するのではなく、 `‹ ›`でマークすることをサポートします。7 `"marker"`を使用すると、編集ルールをカスタマイズできます。       |
| BR             | [`--allow-pitr-from-incremental`](/br/br-incremental-guide.md#limitations)                             | 新しく追加された | 増分バックアップが後続のログ バックアップと互換性があるかどうかを制御します。デフォルト値は`true`で、増分バックアップが後続のログ バックアップと互換性があることを意味します。デフォルト値`true`のままにすると、増分復元が開始される前に、再生する必要がある DDL が厳密にチェックされます。 |

### システムテーブル {#system-tables}

-   [`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md)と[`INFORMATION_SCHEMA.CLUSTER_PROCESSLIST`](/information-schema/information-schema-processlist.md#cluster_processlist)システム テーブルには、DML ステートメント[＃46889](https://github.com/pingcap/tidb/issues/46889) @ [lcwangchao](https://github.com/lcwangchao)によって現在影響を受けている行数を表示する`SESSION_ALIAS`フィールドが追加されます。

## 廃止された機能 {#deprecated-features}

-   以下の機能は、v8.3.0 以降では非推奨となります。

    -   v7.5.0 以降、 [TiDBBinlog](https://docs.pingcap.com/tidb/v8.3/tidb-binlog-overview)レプリ​​ケーションは非推奨です。v8.3.0 以降、 TiDB Binlog は完全に非推奨となり、将来のリリースで削除される予定です。増分データ レプリケーションの場合は、代わりに[ティCDC](/ticdc/ticdc-overview.md)使用します。ポイントインタイム リカバリ (PITR) の場合は、 [ピトル](/br/br-pitr-guide.md)使用します。
    -   v8.3.0 以降、 [`tidb_enable_column_tracking`](/system-variables.md#tidb_enable_column_tracking-new-in-v540)システム変数は非推奨になりました。TiDB はデフォルトで述語列を追跡します。詳細については、 [`tidb_analyze_column_options`](/system-variables.md#tidb_analyze_column_options-new-in-v830)参照してください。

-   以下の機能は将来のバージョンで廃止される予定です。

    -   TiDB では、統計を自動的に収集するタスクの順序を最適化するために優先キューを有効にするかどうかを制御するためのシステム変数[`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-new-in-v800)が導入されています。将来のリリースでは、統計を自動的に収集するタスクを順序付ける唯一の方法は優先キューになるため、このシステム変数は非推奨になります。
    -   TiDB は、v7.5.0 でシステム変数[`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-new-in-v750)を導入しました。これを使用して、TiDB がパーティション統計の非同期マージを使用して OOM の問題を回避するように設定できます。将来のリリースでは、パーティション統計は非同期にマージされるため、このシステム変数は非推奨になります。
    -   以降のリリースでは[実行計画バインディングの自動進化](/sql-plan-management.md#baseline-evolution)再設計する予定であり、関連する変数と動作が変更されます。
    -   v8.0.0 では、TiDB は、同時 HashAgg アルゴリズムのディスク スピルをサポートするかどうかを制御する[`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-new-in-v800)システム変数を導入します。将来のバージョンでは、 [`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-new-in-v800)システム変数は非推奨になります。
    -   TiDB Lightningパラメータ[`conflict.max-record-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)は、将来のリリースで廃止される予定であり、その後削除されます。このパラメータは[`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)に置き換えられます。これは、競合するレコードの最大数が、単一のインポート タスクで許容できる競合するレコードの最大数と一致することを意味します。

-   以下の機能は将来のバージョンで削除される予定です:

    -   v8.0.0 以降、 TiDB Lightning物理インポート モードの[競合検出の旧バージョン](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#the-old-version-of-conflict-detection-deprecated-in-v800)戦略が廃止され、 [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)パラメータを使用して論理インポート モードと物理インポート モードの両方の競合検出戦略を制御できるようになりました。競合検出の旧バージョンの[`duplicate-resolution`](/tidb-lightning/tidb-lightning-configuration.md)パラメータは、将来のリリースで削除される予定です。

## 改善点 {#improvements}

-   ティビ

    -   `SELECT ... STRAIGHT_JOIN ... USING ( ... )`ステートメント[＃54162](https://github.com/pingcap/tidb/issues/54162) @ [ドヴェーデン](https://github.com/dveeden)をサポートする
    -   `((idx_col_1 > 1) or (idx_col_1 = 1 and idx_col_2 > 10)) and ((idx_col_1 < 10) or (idx_col_1 = 10 and idx_col_2 < 20))` [＃54337](https://github.com/pingcap/tidb/issues/54337) @ [ガザルファミリー](https://github.com/ghazalfamilyusa)のようなフィルタ条件に対してより正確なインデックスアクセス範囲を構築する
    -   `WHERE idx_col_1 IS NULL ORDER BY idx_col_2` [＃54188](https://github.com/pingcap/tidb/issues/54188) @ [アリエ](https://github.com/ari-e)のようなSQLクエリの余分なソート操作を避けるためにインデックス順序を使用します。
    -   `mysql.analyze_jobs`システムテーブル[＃53567](https://github.com/pingcap/tidb/issues/53567) @ [ハイラスティン](https://github.com/Rustin170506)の分析されたインデックスを表示します
    -   `EXPLAIN`ステートメントの出力に`tidb_redact_log`設定を適用し、ログ[＃54565](https://github.com/pingcap/tidb/issues/54565) @ [ホーキングレイ](https://github.com/hawkingrei)の処理ロジックをさらに最適化することをサポート
    -   クエリ効率を向上させるために、多値インデックス`IndexRangeScan`で`Selection`演算子を生成するサポート[＃54876](https://github.com/pingcap/tidb/issues/54876) @ [時間と運命](https://github.com/time-and-fate)
    -   設定された時間枠外で実行されているタスクを自動的に`ANALYZE`終了する機能をサポート[＃55283](https://github.com/pingcap/tidb/issues/55283) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   統計がすべて TopN で構成され、対応するテーブル統計の変更された行数がゼロ以外の場合、TopN にヒットしない等価条件の推定結果を 0 から 1 に調整します[＃47400](https://github.com/pingcap/tidb/issues/47400) @ [テリー・パーセル](https://github.com/terry1purcell)
    -   TopN演算子はディスクスピル[＃47733](https://github.com/pingcap/tidb/issues/47733) @ [翻訳者](https://github.com/xzhangxian1008)をサポートします
    -   TiDBノードは、 `WITH ROLLUP`修飾子と`GROUPING`関数[＃42631](https://github.com/pingcap/tidb/issues/42631) @ [アレナトルクス](https://github.com/Arenatlx)を使用したクエリの実行をサポートしています。
    -   システム変数[`tidb_low_resolution_tso`](/system-variables.md#tidb_low_resolution_tso) `GLOBAL`スコープ[＃55022](https://github.com/pingcap/tidb/issues/55022) @ [翻訳](https://github.com/cfzjywxk)をサポートします
    -   同時範囲削除をサポートすることでGC（ガベージコレクション）の効率を向上させます。同時スレッド数は[`tidb_gc_concurrency`](/system-variables.md#tidb_gc_concurrency-new-in-v50) [＃54570](https://github.com/pingcap/tidb/issues/54570) @ [エキシウム](https://github.com/ekexium)で制御できます。
    -   バルクDML実行モードのパフォーマンスを向上させる（ `tidb_dml_type = "bulk"` ） [＃50215](https://github.com/pingcap/tidb/issues/50215) @ [エキシウム](https://github.com/ekexium)
    -   スキーマ情報キャッシュ関連インターフェースのパフォーマンスを向上`SchemaByID` [＃54074](https://github.com/pingcap/tidb/issues/54074) @ [うわー](https://github.com/ywqzzy)
    -   スキーマ情報キャッシュが有効な場合の特定のシステム テーブルのクエリ パフォーマンスを向上[＃50305](https://github.com/pingcap/tidb/issues/50305) @ [タンジェンタ](https://github.com/tangenta)
    -   一意のインデックス[＃53004](https://github.com/pingcap/tidb/issues/53004) @ [ランス6716](https://github.com/lance6716)を追加するときに競合するキーのエラー メッセージを最適化します

-   PD

    -   リーダーの排除プロセスを加速するために、 `pd-ctl`を介して`evict-leader-scheduler`の`batch`構成を変更することをサポートします[＃8265](https://github.com/tikv/pd/issues/8265) @ [rleungx](https://github.com/rleungx)
    -   Grafana の**クラスタ &gt; Label distribution**パネルに`store_id`監視メトリックを追加して、異なるラベル[＃8337](https://github.com/tikv/pd/issues/8337) @ [ヒューシャープ](https://github.com/HuSharp)に対応するストア ID を表示します。
    -   指定されたリソース グループが存在しない場合に、デフォルトのリソース グループへのフォールバックをサポートします[＃8388](https://github.com/tikv/pd/issues/8388) @ [じゃがいも](https://github.com/JmPotato)
    -   `pd-ctl` [＃8412](https://github.com/tikv/pd/issues/8412) @ [沢民州](https://github.com/zeminzhou)の`region`コマンドによって出力されるリージョン情報に`approximate_kv_size`フィールドを追加します。
    -   PD APIを呼び出してTTL設定を削除するときに返されるメッセージを最適化します[＃8450](https://github.com/tikv/pd/issues/8450) @ [翻訳者](https://github.com/lhy1024)
    -   大規模なクエリ読み取り要求の RU 消費動作を最適化して、他の要求への影響を軽減します[＃8457](https://github.com/tikv/pd/issues/8457) @ [ノルーシュ](https://github.com/nolouch)
    -   PD マイクロサービス[＃52912](https://github.com/pingcap/tidb/issues/52912) @ [rleungx](https://github.com/rleungx)を誤って構成した場合に返されるエラー メッセージを最適化します
    -   PDマイクロサービスに`--name`起動パラメータを追加して、デプロイメント中にサービス名をより正確に表示します[＃7995](https://github.com/tikv/pd/issues/7995) @ [ヒューシャープ](https://github.com/HuSharp)
    -   リージョンスキャン時間を短縮するために、領域の数に基づいて`PatrolRegionScanLimit`動的に調整する機能をサポート[＃7963](https://github.com/tikv/pd/issues/7963) @ [翻訳者](https://github.com/lhy1024)

-   ティクヴ

    -   `async-io`有効になっている場合、 Raftログを書き込むためのバッチ処理ポリシーを最適化して、ディスク I/O 帯域幅リソースの消費を削減します[＃16907](https://github.com/tikv/tikv/issues/16907) @ [リクササシネーター](https://github.com/LykxSassinator)
    -   TiCDC デリゲートとダウンストリーム モジュールを再設計して、リージョン部分サブスクリプション[＃16362](https://github.com/tikv/tikv/issues/16362) @ [ヒック](https://github.com/hicqu)をより適切にサポートします。
    -   単一のスロークエリログのサイズを縮小[＃17294](https://github.com/tikv/tikv/issues/17294) @ [コナー1996](https://github.com/Connor1996)
    -   新しい監視メトリックを追加する`min safe ts` [＃17307](https://github.com/tikv/tikv/issues/17307) @ [ミッタルリシャブ](https://github.com/mittalrishabh)
    -   ピアメッセージチャネル[＃16229](https://github.com/tikv/tikv/issues/16229) @ [コナー1996](https://github.com/Connor1996)のメモリ使用量を削減

-   TiFlash

    -   SVG 形式でのアドホック ヒープ プロファイリングの生成をサポート[＃9320](https://github.com/pingcap/tiflash/issues/9320) @ [カルビンネオ](https://github.com/CalvinNeo)

-   ツール

    -   バックアップと復元 (BR)

        -   初めてポイントインタイムリカバリ (PITR) を開始する前に、フルバックアップが存在するかどうかのチェックをサポートします。フルバックアップが見つからない場合、 BR は復元を終了し、エラー[＃54418](https://github.com/pingcap/tidb/issues/54418) @ [リーヴルス](https://github.com/Leavrth)を返します。
        -   スナップショットバックアップを復元する前に、TiKV およびTiFlashのディスク容量が十分かどうかのチェックをサポートします。容量が不十分な場合、 BR は復元を終了し、エラー[＃54316](https://github.com/pingcap/tidb/issues/54316) @ [リドリス](https://github.com/RidRisR)を返します。
        -   TiKV が各 SST ファイルをダウンロードする前に、TiKV のディスク容量が十分かどうかのチェックをサポートします。容量が不十分な場合、 BR は復元を終了し、エラー[＃17224](https://github.com/tikv/tikv/issues/17224) @ [リドリス](https://github.com/RidRisR)を返します。
        -   環境変数[＃45551](https://github.com/pingcap/tidb/issues/45551) @ [リドリス](https://github.com/RidRisR)による Alibaba Cloud アクセス資格情報の設定をサポート
        -   バックアップと復元にBR を使用するときに OOM を回避するために、 BRプロセスの使用可能なメモリに基づいて環境変数`GOMEMLIMIT`を自動的に設定します[＃53777](https://github.com/pingcap/tidb/issues/53777) @ [リーヴルス](https://github.com/Leavrth)
        -   増分バックアップをポイントインタイムリカバリ（PITR） [＃54474](https://github.com/pingcap/tidb/issues/54474) @ [3ポインター](https://github.com/3pointer)と互換性のあるものにする
        -   `mysql.column_stats_usage`テーブル[＃53567](https://github.com/pingcap/tidb/issues/53567) @ [ハイラスティン](https://github.com/Rustin170506)のバックアップと復元をサポート

## バグ修正 {#bug-fixes}

-   ティビ

    -   `PipelinedWindow`の`Open`メソッドのパラメータをリセットして、 `PipelinedWindow`が`Apply`の子ノードとして使用されたときに、繰り返しの開閉操作[＃53600](https://github.com/pingcap/tidb/issues/53600) @ [徐懐玉](https://github.com/XuHuaiyu)によって以前のパラメータ値が再利用されたために発生する予期しないエラーを修正します。
    -   メモリ使用量が`tidb_mem_quota_query` [＃55042](https://github.com/pingcap/tidb/issues/55042) @ [いびん87](https://github.com/yibin87)で設定された制限を超えたためにクエリが終了したときに停止する可能性がある問題を修正しました
    -   HashAgg 演算子のディスク スピルにより並列計算中に誤ったクエリ結果が発生する問題を修正[＃55290](https://github.com/pingcap/tidb/issues/55290) @ [翻訳者](https://github.com/xzhangxian1008)
    -   `YEAR` JSON 形式[＃54494](https://github.com/pingcap/tidb/issues/54494) @ [ヤンケオ](https://github.com/YangKeao)にキャストするときに間違った`JSON_TYPE`発生する問題を修正
    -   `tidb_schema_cache_size`システム変数の値の範囲が間違っている問題を修正[＃54034](https://github.com/pingcap/tidb/issues/54034) @ [リリンハイ](https://github.com/lilinghai)
    -   パーティション式が`EXTRACT(YEAR FROM col)` [＃54210](https://github.com/pingcap/tidb/issues/54210) @ [ミョンス](https://github.com/mjonss)の場合にパーティションプルーニングが機能しない問題を修正しました
    -   データベースに多数のテーブルが存在する場合に`FLASHBACK DATABASE`失敗する問題を修正[＃54415](https://github.com/pingcap/tidb/issues/54415) @ [ランス6716](https://github.com/lance6716)
    -   多数のデータベースを処理するときに`FLASHBACK DATABASE`無限ループに入る問題を修正[＃54915](https://github.com/pingcap/tidb/issues/54915) @ [ランス6716](https://github.com/lance6716)
    -   インデックス加速モードでインデックスを追加すると失敗する可能性がある問題を修正[＃54568](https://github.com/pingcap/tidb/issues/54568) @ [ランス6716](https://github.com/lance6716)
    -   `ADMIN CANCEL DDL JOBS`により DDL が失敗する可能性がある問題を修正[＃54687](https://github.com/pingcap/tidb/issues/54687) @ [ランス6716](https://github.com/lance6716)
    -   DMから複製されたテーブルのインデックス長が`max-index-length` [＃55138](https://github.com/pingcap/tidb/issues/55138) @ [ランス6716](https://github.com/lance6716)で指定された最大長を超えるとテーブル複製が失敗する問題を修正しました。
    -   `tidb_enable_inl_join_inner_multi_pattern`有効にして SQL 文を実行するとエラー`runtime error: index out of range`発生する可能性がある問題を修正[＃54535](https://github.com/pingcap/tidb/issues/54535) @ [ジョーチェン](https://github.com/joechenrh)
    -   統計の初期化プロセス中に、 <kbd>Control</kbd> + <kbd>C を</kbd>使用して TiDB を終了できない問題を修正しました[＃54589](https://github.com/pingcap/tidb/issues/54589) @ [天菜まお](https://github.com/tiancaiamao)
    -   `INL_MERGE_JOIN`オプティマイザヒントが誤った結果を返す問題を修正しました[＃54064](https://github.com/pingcap/tidb/issues/54064) @ [アイリンキッド](https://github.com/AilinKid)を廃止しました。
    -   `WITH ROLLUP`を含む相関サブクエリによって TiDB がpanicを起こし、エラー`runtime error: index out of range` [＃54983](https://github.com/pingcap/tidb/issues/54983) @ [アイリンキッド](https://github.com/AilinKid)を返す可能性がある問題を修正しました。
    -   SQLクエリのフィルタ条件に仮想列が含まれ、実行条件に`UnionScan` [＃54870](https://github.com/pingcap/tidb/issues/54870) @ [qw4990](https://github.com/qw4990)が含まれている場合に述語を適切にプッシュダウンできない問題を修正しました。
    -   `tidb_enable_inl_join_inner_multi_pattern`有効にして SQL 文を実行するとエラー`runtime error: invalid memory address or nil pointer dereference`発生する可能性がある問題を修正[＃55169](https://github.com/pingcap/tidb/issues/55169) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   `UNION`を含むクエリ ステートメントが誤った結果[＃52985](https://github.com/pingcap/tidb/issues/52985) @ [徐懐玉](https://github.com/XuHuaiyu)を返す可能性がある問題を修正しました
    -   `mysql.stats_histograms`の表の`tot_col_size`列目が負の数[＃55126](https://github.com/pingcap/tidb/issues/55126) @ [qw4990](https://github.com/qw4990)になる可能性がある問題を修正しました
    -   `columnEvaluator`入力チャンク内の列参照を識別できず、SQL ステートメント[＃53713](https://github.com/pingcap/tidb/issues/53713) @ [アイリンキッド](https://github.com/AilinKid)を実行すると`runtime error: index out of range`発生する問題を修正しました。
    -   `STATS_EXTENDED`予約キーワード[＃39573](https://github.com/pingcap/tidb/issues/39573) @ [WDデバイス](https://github.com/wddevries)になる問題を修正
    -   `tidb_low_resolution`が有効になっている場合、 `select for update` [＃54684](https://github.com/pingcap/tidb/issues/54684) @ [翻訳](https://github.com/cfzjywxk)実行できる問題を修正
    -   `tidb_redact_log`が有効になっている場合、スロークエリログに内部 SQL クエリが表示されない問題を修正[＃54190](https://github.com/pingcap/tidb/issues/54190) @ [lcwangchao](https://github.com/lcwangchao)
    -   トランザクションによって使用されるメモリが複数回追跡される可能性がある問題を修正[＃53984](https://github.com/pingcap/tidb/issues/53984) @ [エキシウム](https://github.com/ekexium)
    -   `SHOW WARNINGS;`使用して警告を取得するとpanicが発生する可能性がある問題を修正[＃48756](https://github.com/pingcap/tidb/issues/48756) @ [xhebox](https://github.com/xhebox)
    -   インデックス統計の読み込み時にメモリリークが発生する可能性がある問題を修正[＃54022](https://github.com/pingcap/tidb/issues/54022) @ [ハイラスティン](https://github.com/Rustin170506)
    -   照合順序が`utf8_bin`または`utf8mb4_bin` [＃53730](https://github.com/pingcap/tidb/issues/53730) @ [エルサ0520](https://github.com/elsa0520)の場合に`LENGTH()`条件が予期せず削除される問題を修正しました
    -   重複した主キー[＃47539](https://github.com/pingcap/tidb/issues/47539) @ [定義2014](https://github.com/Defined2014)に遭遇したときに統計収集で`stats_history`テーブルが更新されない問題を修正しました
    -   再帰 CTE クエリによって無効なポインタ[＃54449](https://github.com/pingcap/tidb/issues/54449) @ [ホーキングレイ](https://github.com/hawkingrei)が生成される可能性がある問題を修正しました。
    -   ハンドシェイクが完了する前に一部の接続が終了した場合に Grafana の接続数監視メトリックが正しくない問題を修正[＃54428](https://github.com/pingcap/tidb/issues/54428) @ [ヤンケオ](https://github.com/YangKeao)
    -   TiProxy とリソース グループ[#54545](https://github.com/pingcap/tidb/issues/54545) @ [ヤンケオ](https://github.com/YangKeao)使用するときに、各リソース グループの接続数が正しくない問題を修正しました。
    -   クエリに非相関サブクエリと`LIMIT`句が含まれている場合、列のプルーニングが不完全になり、最適でないプラン[＃54213](https://github.com/pingcap/tidb/issues/54213) @ [qw4990](https://github.com/qw4990)になる可能性がある問題を修正しました。
    -   `SELECT ... FOR UPDATE` [＃54652](https://github.com/pingcap/tidb/issues/54652) @ [qw4990](https://github.com/qw4990)の間違ったポイント取得プランを再利用する問題を修正
    -   最初の引数が`month`で、2 番目の引数が負の[＃54908](https://github.com/pingcap/tidb/issues/54908) @ [翻訳者](https://github.com/xzhangxian1008)場合に`TIMESTAMPADD()`関数が無限ループに入る問題を修正しました。
    -   スローログ内の内部SQL文がデフォルトでnullに編集される問題を修正[＃54190](https://github.com/pingcap/tidb/issues/54190) [＃52743](https://github.com/pingcap/tidb/issues/52743) [＃53264](https://github.com/pingcap/tidb/issues/53264) @ [lcwangchao](https://github.com/lcwangchao)
    -   `_tidb_rowid`の実行プラン`PointGet`が[＃54583](https://github.com/pingcap/tidb/issues/54583) @ [定義2014](https://github.com/Defined2014)で生成できる問題を修正
    -   v7.1 [＃54241](https://github.com/pingcap/tidb/issues/54241) @ [タンジェンタ](https://github.com/tangenta)からアップグレードした後に`SHOW IMPORT JOBS`エラー`Unknown column 'summary'`報告する問題を修正
    -   ビュー定義[＃54343](https://github.com/pingcap/tidb/issues/54343) @ [ランス6716](https://github.com/lance6716)でサブクエリが列定義として使用されている場合、 `information_schema.columns`使用して列情報を取得すると警告 1356 が返される問題を修正しました。
    -   厳密に自己増分ではないRANGEパーティションテーブルが[＃54829](https://github.com/pingcap/tidb/issues/54829) @ [定義2014](https://github.com/Defined2014)で作成できる問題を修正
    -   SQLが異常に中断されたときに`INDEX_HASH_JOIN`正常に終了できない問題を修正[＃54688](https://github.com/pingcap/tidb/issues/54688) @ [うわー](https://github.com/wshwsh12)
    -   分散実行フレームワーク (DXF) を使用してインデックスを追加するときにネットワーク パーティションが発生すると、データ インデックス[＃54897](https://github.com/pingcap/tidb/issues/54897) @ [タンジェンタ](https://github.com/tangenta)に不整合が発生する可能性がある問題を修正しました。

-   PD

    -   ロールをリソース グループ[＃54417](https://github.com/pingcap/tidb/issues/54417) @ [じゃがいも](https://github.com/JmPotato)にバインドするときにエラーが報告されない問題を修正しました
    -   500 ミリ秒を超えるトークンをリクエストするとリソース グループがクォータ制限に達する問題を修正[＃8349](https://github.com/tikv/pd/issues/8349) @ [ノルーシュ](https://github.com/nolouch)
    -   `INFORMATION_SCHEMA.RUNAWAY_WATCHES`テーブルの時間データ型が正しくない問題を修正[＃54770](https://github.com/pingcap/tidb/issues/54770) @ [ヒューシャープ](https://github.com/HuSharp)
    -   同時実行性が高い場合にリソース グループがリソースの使用を効果的に制限できない問題を修正[＃8435](https://github.com/tikv/pd/issues/8435) @ [ノルーシュ](https://github.com/nolouch)
    -   テーブル属性[＃55188](https://github.com/pingcap/tidb/issues/55188) @ [じゃがいも](https://github.com/JmPotato)を取得するときに誤った PD API が呼び出される問題を修正しました
    -   `scheduling`マイクロサービスが有効になった後にスケーリングの進行状況が正しく表示されない問題を修正[＃8331](https://github.com/tikv/pd/issues/8331) @ [rleungx](https://github.com/rleungx)
    -   使用前に暗号化マネージャーが初期化されない問題を修正[＃8384](https://github.com/tikv/pd/issues/8384) @ [rleungx](https://github.com/rleungx)
    -   一部のログが編集されていない問題を修正[＃8419](https://github.com/tikv/pd/issues/8419) @ [rleungx](https://github.com/rleungx)
    -   PD マイクロサービス[＃8406](https://github.com/tikv/pd/issues/8406) @ [ヒューシャープ](https://github.com/HuSharp)の起動中にリダイレクトがpanicになる可能性がある問題を修正しました
    -   `split-merge-interval`構成項目の値を繰り返し変更すると（ `1s`から`1h`に変更して`1s`に戻すなど）、その設定項目が有効にならない可能性がある問題を修正しました[＃8404](https://github.com/tikv/pd/issues/8404) @ [翻訳者](https://github.com/lhy1024)
    -   `replication.strictly-match-label`から`true`に設定するとTiFlash が[＃8480](https://github.com/tikv/pd/issues/8480) @ [rleungx](https://github.com/rleungx)で起動しなくなる問題を修正
    -   大きなパーティションテーブルを分析するときに TSO の取得が遅くなり、パフォーマンスの低下が`ANALYZE`発生する問題を修正しました[＃8500](https://github.com/tikv/pd/issues/8500) @ [rleungx](https://github.com/rleungx)
    -   大規模クラスタにおける潜在的なデータ競合を修正[＃8386](https://github.com/tikv/pd/issues/8386) @ [rleungx](https://github.com/rleungx)
    -   クエリがランナウェイ クエリであるかどうかを判断するときに、TiDB はコプロセッサー側で費やされた時間消費のみをカウントし、TiDB 側で費やされた時間消費をカウントしないため、一部のクエリがランナウェイ クエリ[＃51325](https://github.com/pingcap/tidb/issues/51325) @ [ヒューシャープ](https://github.com/HuSharp)として識別されない問題を修正しました。

-   TiFlash

    -   `CAST()`関数を使用して文字列をタイムゾーンまたは無効な文字を含む日付時刻に変換すると、結果が正しくなくなる問題を修正しました[＃8754](https://github.com/pingcap/tiflash/issues/8754) @ [ソロッツ](https://github.com/solotzg)
    -   データベース[＃9132](https://github.com/pingcap/tiflash/issues/9132) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)にまたがる空のパーティションを持つパーティションテーブルで`RENAME TABLE ... TO ...`実行した後にTiFlash がpanic可能性がある問題を修正しました。
    -   遅延マテリアライゼーションが有効になった後に、一部のクエリで列タイプの不一致エラーが報告される問題を修正[＃9175](https://github.com/pingcap/tiflash/issues/9175) @ [ジンヘリン](https://github.com/JinheLin)
    -   遅延マテリアライゼーションが有効になった後、仮想生成列を含むクエリが誤った結果を返す可能性がある問題を修正[＃9188](https://github.com/pingcap/tiflash/issues/9188) @ [ジンヘリン](https://github.com/JinheLin)
    -   TiFlashで SSL 証明書構成を空の文字列に設定すると、誤って TLS が有効になり、 TiFlash が起動しなくなる問題を修正しました[＃9235](https://github.com/pingcap/tiflash/issues/9235) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)
    -   データベースが作成直後に削除されるとTiFlash がpanic可能性がある問題を修正[＃9266](https://github.com/pingcap/tiflash/issues/9266) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)
    -   TiFlashと PD 間のネットワーク パーティション (ネットワーク切断) により読み取り要求タイムアウト エラーが発生する可能性がある問題を修正[＃9243](https://github.com/pingcap/tiflash/issues/9243) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)
    -   分散storageおよびコンピューティングアーキテクチャ[＃9282](https://github.com/pingcap/tiflash/issues/9282) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)でTiFlash書き込みノードが再起動に失敗する可能性がある問題を修正しました
    -   分散storageおよびコンピューティングアーキテクチャ[＃9298](https://github.com/pingcap/tiflash/issues/9298) @ [ジンヘリン](https://github.com/JinheLin)で、 TiFlash書き込みノードの読み取りスナップショットがタイムリーにリリースされない問題を修正しました。

-   ティクヴ

    -   古い領域をクリーンアップすると、有効なデータが誤って削除される可能性がある問題を修正[＃17258](https://github.com/tikv/tikv/issues/17258) @ [ビシェン](https://github.com/hbisheng)
    -   Grafana [＃15990](https://github.com/tikv/tikv/issues/15990) @ [コナー1996](https://github.com/Connor1996)の TiKV ダッシュボードで`Ingestion picked level`と`Compaction Job Size(files)`誤って表示される問題を修正しました
    -   `cancel_generating_snap`誤って`snap_tried_cnt`を更新して TiKV がpanicになる問題を修正[＃17226](https://github.com/tikv/tikv/issues/17226) @ [ビシェン](https://github.com/hbisheng)
    -   `Ingest SST duration seconds`の情報が間違っている問題を修正[＃17239](https://github.com/tikv/tikv/issues/17239) @ [リクササシネーター](https://github.com/LykxSassinator)
    -   エラーが発生したときにCPUプロファイリングフラグが正しくリセットされない問題を修正[＃17234](https://github.com/tikv/tikv/issues/17234) @ [コナー1996](https://github.com/Connor1996)
    -   ブルームフィルタが以前のバージョン（v7.1以前）とそれ以降のバージョン[＃17272](https://github.com/tikv/tikv/issues/17272) @ [v01dスター](https://github.com/v01dstar)の間で互換性がない問題を修正しました

-   ツール

    -   バックアップと復元 (BR)

        -   `ADD INDEX`や`MODIFY COLUMN`などのバックフィルを必要とする DDL が、増分リストア[＃54426](https://github.com/pingcap/tidb/issues/54426) @ [3ポインター](https://github.com/3pointer)中に正しく回復されない可能性がある問題を修正しました。
        -   バックアップと復元中に進行が停止する問題を修正[＃54140](https://github.com/pingcap/tidb/issues/54140) @ [リーヴルス](https://github.com/Leavrth)
        -   バックアップと復元のチェックポイントパスが一部の外部storageと互換性がない問題を修正[＃55265](https://github.com/pingcap/tidb/issues/55265) @ [リーヴルス](https://github.com/Leavrth)

    -   ティCDC

        -   下流の Kafka にアクセスできない場合にプロセッサが停止する可能性がある問題を修正[＃11340](https://github.com/pingcap/tiflow/issues/11340) @ [アズドンメン](https://github.com/asddongmen)

    -   TiDB データ移行 (DM)

        -   スキーマ トラッカーが LIST パーティション テーブルを誤って処理し、DM エラー[＃11408](https://github.com/pingcap/tiflow/issues/11408) @ [ランス6716](https://github.com/lance6716)が発生する問題を修正しました。
        -   インデックスの長さがデフォルト値の`max-index-length` [＃11459](https://github.com/pingcap/tiflow/issues/11459) @ [マイケル・ムデン](https://github.com/michaelmdeng)を超えるとデータレプリケーションが中断される問題を修正
        -   DMが`FAKE_ROTATE_EVENT`正しく処理できない問題を修正[＃11381](https://github.com/pingcap/tiflow/issues/11381) @ [ランス6716](https://github.com/lance6716)

    -   TiDB Lightning

        -   TiDB Lightning がキースペース名[＃54232](https://github.com/pingcap/tidb/issues/54232) @ [ケニー](https://github.com/kennytm)取得に失敗した場合に紛らわしい`WARN`ログを出力する問題を修正しました
        -   TiDB Lightningの TLS 構成がクラスタ証明書[＃54172](https://github.com/pingcap/tidb/issues/54172) @ [杉本栄](https://github.com/ei-sugimoto)に影響する問題を修正
        -   TiDB Lightning [＃49826](https://github.com/pingcap/tidb/issues/49826) @ [ランス6716](https://github.com/lance6716)使用してデータのインポート中にトランザクションの競合が発生する問題を修正しました
        -   多数のデータベースとテーブル[＃55054](https://github.com/pingcap/tidb/issues/55054) @ [D3ハンター](https://github.com/D3Hunter)のインポート中に大きなチェックポイント ファイルによってパフォーマンスが低下する問題を修正しました

## 寄稿者 {#contributors}

TiDB コミュニティの以下の貢献者に感謝いたします。

-   [アリエ](https://github.com/ari-e)
-   [杉本栄](https://github.com/ei-sugimoto)
-   [ハオW30](https://github.com/HaoW30)
-   [ジャックL9u](https://github.com/JackL9u)
-   [マイケル・ムデン](https://github.com/michaelmdeng)
-   [ミッタルリシャブ](https://github.com/mittalrishabh)
-   [清風777](https://github.com/qingfeng777)
-   [サンディープ・パディ](https://github.com/SandeepPadhi)
-   [yzhan1](https://github.com/yzhan1)
