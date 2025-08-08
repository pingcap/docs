---
title: TiDB 8.3.0 Release Notes
summary: TiDB 8.3.0 の新機能、互換性の変更、改善点、バグ修正について説明します。
---

# TiDB 8.3.0 リリースノート {#tidb-8-3-0-release-notes}

発売日：2024年8月22日

TiDB バージョン: 8.3.0

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v8.3/quick-start-with-tidb)

8.3.0 では、次の主な機能と改善が導入されています。

<table><thead><tr><th>カテゴリ</th><th>機能/拡張機能</th><th>説明</th></tr></thead><tbody><tr><td rowspan="3">スケーラビリティとパフォーマンス</td><td><a href="https://docs.pingcap.com/tidb/v8.3/partitioned-table#global-indexes">パーティションテーブルのグローバルインデックス（実験的）</a></td><td>グローバルインデックスは、パーティション化されていない列の取得効率を効果的に向上させ、一意のキーがパーティションキーを含んでいなければならないという制約を排除します。この機能により、TiDBパーティションテーブルの利用シナリオが拡張され、データ移行に必要となる可能性のあるアプリケーションの変更作業の一部を回避できます。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v8.3/system-variables#tidb_opt_projection_push_down-new-in-v610"><code>Projection</code>演算子のstorageエンジンへのデフォルトのプッシュダウン</a></td><td><code>Projection</code>演算子をstorageエンジンにプッシュダウンすることで、storageノード間の負荷を分散し、ノード間のデータ転送を削減できます。この最適化により、特定のSQLクエリの実行時間が短縮され、データベース全体のパフォーマンスが向上します。</td></tr><tr><td><a href="https://docs.pingcap.com/tidb/v8.3/statistics#collect-statistics-on-some-columns">統計を収集する際に不要な列を無視する</a></td><td>TiDBは、オプティマイザが必要な情報を確実に取得できるという前提のもと、統計収集を高速化し、統計の適時性を向上させ、最適な実行プランの選択を保証することで、クラスターのパフォーマンスを向上させます。同時に、TiDBはシステムオーバーヘッドを削減し、リソース利用率を向上させます。</td></tr><tr><td rowspan="1">信頼性と可用性</td><td><a href="https://docs.pingcap.com/tidb/v8.3/tiproxy-overview">TiProxyに組み込まれた仮想IP管理</a></td><td>TiProxyは、組み込みの仮想IP管理機能を導入しています。設定により、外部プラットフォームやツールに依存せずに、仮想IPの自動切り替えをサポートします。この機能により、TiProxyの導入が簡素化され、データベースアクセスレイヤーの複雑さが軽減されます。</td></tr></tbody></table>

## 機能の詳細 {#feature-details}

### パフォーマンス {#performance}

-   オプティマイザは、デフォルトで`Projection`演算子をstorageエンジンにプッシュダウンすることを許可します[＃51876](https://github.com/pingcap/tidb/issues/51876) @ [イービン87](https://github.com/yibin87)

    `Projection`演算子をstorageエンジンにプッシュダウンすると、コンピューティングエンジンとstorageエンジン間のデータ転送が削減され、SQL実行パフォーマンスが向上します。これは、 [JSONクエリ関数](/functions-and-operators/json-functions/json-functions-search.md)または[JSON値属性関数](/functions-and-operators/json-functions/json-functions-return.md)含むクエリで特に効果的です。TiDB v8.3.0以降、この機能を制御するシステム変数のデフォルト値[`tidb_opt_projection_push_down`](/system-variables.md#tidb_opt_projection_push_down-new-in-v610)を`OFF`から`ON`に変更することで、 `Projection`演算子のプッシュダウン機能がデフォルトで有効になります。この機能が有効になっていると、オプティマイザーは適切なJSONクエリ関数とJSON値属性関数を自動的にstorageエンジンにプッシュダウンします。

    詳細については[ドキュメント](/system-variables.md#tidb_opt_projection_push_down-new-in-v610)参照してください。

-   KV（キーバリュー）リクエスト[＃55206](https://github.com/pingcap/tidb/issues/55206) @ [ジグアン](https://github.com/zyguan)のバッチ処理戦略を最適化

    TiDBは、TiKVにKVリクエストを送信することでデータを取得します。KVリクエストをバッチ処理して一括処理することで、実行パフォーマンスを大幅に向上させることができます。v8.3.0より前のTiDBのバッチ処理戦略は効率が低かったです。v8.3.0以降、TiDBは既存のバッチ処理戦略に加えて、より効率的なバッチ処理戦略をいくつか導入しました。1 [`tikv-client.batch-policy`](/tidb-configuration-file.md#batch-policy-new-in-v830)設定項目を使用して、様々なワークロードに対応するために異なるバッチ処理戦略を設定できます。

    詳細については[ドキュメント](/tidb-configuration-file.md#batch-policy-new-in-v830)参照してください。

-   TiFlashは、高NDVデータ[＃9196](https://github.com/pingcap/tiflash/issues/9196) @ [グオシャオゲ](https://github.com/guo-shaoge)パフォーマンスを向上させるHashAgg集約計算モードを導入しました。

    v8.3.0より前のバージョンでは、 TiFlashは、NDV（個別値の数）の高いデータを扱う場合、HashAgg集計の第一段階で集計計算効率が低下していました。v8.3.0以降、 TiFlashは複数のHashAgg集計計算モードを導入し、さまざまなデータ特性における集計パフォーマンスを向上させています。必要なHashAgg集計計算モードを選択するには、システム変数[`tiflash_hashagg_preaggregation_mode`](/system-variables.md#tiflash_hashagg_preaggregation_mode-new-in-v830)設定します。

    詳細については[ドキュメント](/system-variables.md#tiflash_hashagg_preaggregation_mode-new-in-v830)参照してください。

-   統計を収集するときに不要な列を無視する[＃53567](https://github.com/pingcap/tidb/issues/53567) @ [ハイラスティン](https://github.com/Rustin170506)

    オプティマイザが実行プランを生成する際には、フィルタ条件の列、結合キーの列、集計に使用される列など、一部の列の統計情報のみが必要です。v8.3.0以降、TiDBはSQL文で使用される列の履歴を継続的に監視します。デフォルトでは、TiDBはインデックスが設定された列と、統計情報収集が必要であると判断された列の統計情報のみを収集します。これにより、統計情報の収集が高速化され、不要なリソース消費を回避できます。

    クラスターをv8.3.0より前のバージョンからv8.3.0以降にアップグレードすると、TiDBはデフォルトで元の動作（すべての列の統計情報を収集する）を維持します。この機能を有効にするには、システム変数[`tidb_analyze_column_options`](/system-variables.md#tidb_analyze_column_options-new-in-v830)手動で`PREDICATE`設定する必要があります。新規にデプロイされたクラスターでは、この機能はデフォルトで有効になっています。

    ランダムクエリを多数実行する分析システムでは、システム変数[`tidb_analyze_column_options`](/system-variables.md#tidb_analyze_column_options-new-in-v830)を`ALL`設定することで、すべての列の統計情報を収集し、ランダムクエリのパフォーマンスを確保できます。その他のシステムでは、必要な列のみの統計を収集するため、デフォルト設定（ `PREDICATE` ）の[`tidb_analyze_column_options`](/system-variables.md#tidb_analyze_column_options-new-in-v830)ままにしておくことをお勧めします。

    詳細については[ドキュメント](/statistics.md#collect-statistics-on-some-columns)参照してください。

-   一部のシステムテーブル[＃50305](https://github.com/pingcap/tidb/issues/50305) @ [接線](https://github.com/tangenta)のクエリパフォーマンスを向上

    以前のバージョンでは、クラスターのサイズが大きくなり、テーブル数が多くなると、システム テーブルのクエリのパフォーマンスが低下しました。

    バージョン 8.0.0 では、次の 4 つのシステム テーブルに対してクエリ パフォーマンスが最適化されています。

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

-   パーティション式が`EXTRACT(YEAR_MONTH...)`関数を使用する場合にパーティションプルーニングをサポートして、クエリパフォーマンス[＃54209](https://github.com/pingcap/tidb/pull/54209) @ [ミョンス](https://github.com/mjonss)向上します。

    以前のバージョンでは、パーティション式で`EXTRACT(YEAR_MONTH...)`関数を使用する場合、パーティションプルーニングがサポートされず、クエリパフォーマンスが低下していました。v8.3.0 以降では、パーティション式で`EXTRACT(YEAR_MONTH...)`関数を使用する場合でもパーティションプルーニングがサポートされ、クエリパフォーマンスが向上します。

    詳細については[ドキュメント](/partition-pruning.md#scenario-three)参照してください。

-   `CREATE TABLE`のパフォーマンスを1.4倍、 `CREATE DATABASE`パフォーマンスを2.1倍、 `ADD COLUMN`パフォーマンスを[＃54436](https://github.com/pingcap/tidb/issues/54436)倍に向上させます[D3ハンター](https://github.com/D3Hunter)

    TiDB v8.0.0では、バッチテーブル作成シナリオにおけるテーブル作成パフォーマンスを向上させるシステム変数[`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-new-in-v800)が導入されました。v8.3.0では、単一データベースで10セッションに同時にテーブル作成用のDDL文を送信した場合、v8.2.0と比較してパフォーマンスが1.4倍向上します。

    v8.3.0では、バッチ実行における一般的なDDLのパフォーマンスがv8.2.0と比較して向上しています。10セッション同時実行の`CREATE DATABASE`のパフォーマンスは、v8.1.0と比較して19倍、v8.2.0と比較して2.1倍向上しています。10セッションを使用して、同一データベース内の複数のテーブルに列（ `ADD COLUMN` ）をバッチで追加するパフォーマンスは、v8.1.0と比較して10倍、v8.2.0と比較して2.1倍向上しています。同一データベース内の複数のテーブルで10セッションの`ADD COLUMN`のパフォーマンスは、v8.1.0と比較して10倍、v8.2.0と比較して2倍向上しています。

    詳細については[ドキュメント](/system-variables.md#tidb_enable_fast_create_table-new-in-v800)参照してください。

-   パーティションテーブルはグローバルインデックスをサポートします（実験的） [＃45133](https://github.com/pingcap/tidb/issues/45133) @ [ミョンス](https://github.com/mjonss) @ [定義2014](https://github.com/Defined2014) @ [ジフハウス](https://github.com/jiyfhust) @ [L-メープル](https://github.com/L-maple)

    以前のバージョンのパーティションテーブルでは、グローバルインデックスがサポートされていないため、いくつかの制限がありました。例えば、一意キーはテーブルのパーティション式のすべての列を使用する必要があります。クエリ条件でパーティションキーが使用されていない場合、クエリはすべてのパーティションをスキャンするため、パフォーマンスが低下します。バージョン7.6.0以降では、グローバルインデックス機能を有効にするためにシステム変数[`tidb_enable_global_index`](/system-variables.md#tidb_enable_global_index-new-in-v760)導入されました。ただし、この機能は当時開発中であったため、有効化することは推奨されません。

    バージョン8.3.0以降、グローバルインデックス機能が実験的機能としてリリースされました。パーティションテーブルにキーワード`Global`指定してグローバルインデックスを明示的に作成することで、一意キーがテーブルのパーティション式のすべての列を使用する必要があるという制約がなくなり、柔軟なビジネスニーズに対応できます。グローバルインデックスは、パーティションキーを含まないクエリのパフォーマンスも向上させます。

    詳細については[ドキュメント](/partitioned-table.md#global-indexes)参照してください。

### 信頼性 {#reliability}

-   ストリーミングカーソル結果セットのサポート（実験的） [＃54526](https://github.com/pingcap/tidb/issues/54526) @ [ヤンケオ](https://github.com/YangKeao)

    アプリケーションコードが[カーソルフェッチ](/develop/dev-guide-connection-parameters.md#use-streamingresult-to-get-the-execution-result)使用して結果セットを取得する場合、TiDB は通常、まず完全な結果セットをメモリに保存し、その後、データをバッチ処理でクライアントに返します。結果セットが大きすぎる場合、TiDB は結果を一時的にハードディスクに書き込むことがあります。

    バージョン8.3.0以降、システム変数[`tidb_enable_lazy_cursor_fetch`](/system-variables.md#tidb_enable_lazy_cursor_fetch-new-in-v830)を`ON`に設定すると、TiDBはすべてのデータをTiDBノードに読み取らず、クライアントからの読み取りに応じて徐々にデータをTiDBノードに読み込みます。この機能により、TiDBが大規模な結果セットを処理する際に、TiDBノードのメモリ使用量が削減され、クラスターの安定性が向上します。

    詳細については[ドキュメント](/system-variables.md#tidb_enable_lazy_cursor_fetch-new-in-v830)参照してください。

-   SQL実行プランバインディングの強化[＃55280](https://github.com/pingcap/tidb/issues/55280) [＃55343](https://github.com/pingcap/tidb/issues/55343) @ [時間と運命](https://github.com/time-and-fate)

    OLTPシナリオでは、ほとんどのSQL文の最適な実行計画は固定されています。アプリケーション内の重要なSQL文にSQL実行計画バインディングを実装することで、実行計画が悪化する可能性を低減し、システムの安定性を向上させることができます。多数のSQL実行計画バインディングを作成するという要件を満たすため、TiDBはSQLバインディングの機能とエクスペリエンスを強化し、以下の機能を提供します。

    -   単一の SQL ステートメントを使用して、複数の履歴実行プランから SQL 実行プラン バインディングを作成し、バインディングの作成効率を向上させます。
    -   SQL 実行プラン バインディングでは、より多くのオプティマイザ ヒントがサポートされ、複雑な実行プランの変換方法が最適化されるため、実行プランの復元時にバインディングがより安定します。

    詳細については[ドキュメント](/sql-plan-management.md)参照してください。

### 可用性 {#availability}

-   TiProxyは組み込みの仮想IP管理[＃583](https://github.com/pingcap/tiproxy/issues/583) @ [djshow832](https://github.com/djshow832)をサポートします

    v8.3.0より前のバージョンでは、高可用性のためにプライマリ/セカンダリモードを使用する場合、TiProxyは仮想IPアドレスを管理するための追加コンポーネントを必要としていました。v8.3.0以降、TiProxyは組み込みの仮想IP管理をサポートします。プライマリ/セカンダリモードでは、プライマリノードがフェイルオーバーすると、新しいプライマリノードは指定された仮想IPに自動的にバインドされるため、クライアントは常に仮想IPを介して利用可能なTiProxyに接続できます。

    仮想IP管理を有効にするには、TiProxy設定項目[`ha.virtual-ip`](/tiproxy/tiproxy-configuration.md#virtual-ip)使用して仮想IPアドレスを指定し、 [`ha.interface`](/tiproxy/tiproxy-configuration.md#interface)使用して仮想IPをバインドするネットワークインターフェースを指定します。これらの設定項目の両方が設定されている場合にのみ、仮想IPはTiProxyインスタンスにバインドされます。

    詳細については[ドキュメント](/tiproxy/tiproxy-overview.md)参照してください。

### SQL {#sql}

-   `SELECT LOCK IN SHARE MODE`排他ロック[＃54999](https://github.com/pingcap/tidb/issues/54999) @ [cfzjywxk](https://github.com/cfzjywxk)へのアップグレードをサポート

    TiDB はまだ`SELECT LOCK IN SHARE MODE`サポートしていません。v8.3.0 以降、TiDB は`SELECT LOCK IN SHARE MODE`排他ロックにアップグレードすることで`SELECT LOCK IN SHARE MODE`をサポートできるようになりました。この機能を有効にするかどうかは、新しいシステム変数[`tidb_enable_shared_lock_promotion`](/system-variables.md#tidb_enable_shared_lock_promotion-new-in-v830)で制御できます。

    詳細については[ドキュメント](/system-variables.md#tidb_enable_shared_lock_promotion-new-in-v830)参照してください。

### 可観測性 {#observability}

-   初期統計[＃53564](https://github.com/pingcap/tidb/issues/53564) @ [ホーキングレイ](https://github.com/hawkingrei)読み込みの進行状況を表示します

    TiDBは起動時に基本統計を読み込みます。テーブルやパーティションの数が多い場合、このプロセスには長い時間がかかることがあります。設定項目[`force-init-stats`](/tidb-configuration-file.md#force-init-stats-new-in-v657-and-v710) `ON`に設定すると、初期統計が読み込まれるまでTiDBはサービスを提供しません。この場合、サービスの開始時間を推定するには、読み込みプロセスを観察する必要があります。

    v8.3.0以降、TiDBは初期統計のロードの進行状況を段階的にログに出力、実行状況を把握できるようになりました。外部ツールにフォーマットされた結果を提供するために、TiDBは[監視API](/tidb-monitoring-api.md)という変数を追加し、起動フェーズの任意の時点で初期統計のロードの進行状況を確認できるようにしました。

-   リクエストユニット（RU）設定に関するメトリックを[＃8444](https://github.com/tikv/pd/issues/8444) @ [ノルーシュ](https://github.com/nolouch)追加します

### Security {#security}

-   PDログ編集[＃8305](https://github.com/tikv/pd/issues/8305)を[Jmポテト](https://github.com/JmPotato)で強化

    TiDB v8.0.0ではログ編集機能が強化され、TiDBログ内のユーザーデータを`‹ ›`でマークできるようになりました。マークされたログに基づいて、ログ表示時にマークされた情報を編集するかどうかを決定できるため、ログ編集の柔軟性が向上します。v8.2.0では、 TiFlashにも同様のログ編集機能が実装されています。

    バージョン8.3.0では、PDに同様のログ編集拡張機能が実装されています。この機能を使用するには、PD設定項目`security.redact-info-log`の値を`"marker"`に設定してください。

    詳細については[ドキュメント](/log-redaction.md#log-redaction-in-pd-side)参照してください。

-   TiKV ログ編集[＃17206](https://github.com/tikv/tikv/issues/17206) @ [ルーカスリアン](https://github.com/LykxSassinator)を強化

    TiDB v8.0.0ではログ編集機能が強化され、TiDBログ内のユーザーデータを`‹ ›`でマークできるようになりました。マークされたログに基づいて、ログ表示時にマークされた情報を編集するかどうかを決定できるため、ログ編集の柔軟性が向上します。v8.2.0では、 TiFlashにも同様のログ編集機能が実装されています。

    バージョン8.3.0では、TiKVに同様のログ編集拡張機能が実装されています。この機能を使用するには、TiKV設定項目の値を`security.redact-info-log`から`"marker"`に設定してください。

    詳細については[ドキュメント](/log-redaction.md#log-redaction-in-tikv-side)参照してください。

### データ移行 {#data-migration}

-   TiCDCは双方向レプリケーション（BDR）モードでのDDLステートメントのレプリケーションをサポートしています（GA） [＃10301](https://github.com/pingcap/tiflow/issues/10301) [＃48519](https://github.com/pingcap/tidb/issues/48519) @ [okJiang](https://github.com/okJiang) @ [アズドンメン](https://github.com/asddongmen)

    TiCDC v7.6.0では、双方向レプリケーションが設定されたDDL文のレプリケーションが導入されました。これまで、TiCDCではDDL文の双方向レプリケーションがサポートされていなかったため、TiCDCの双方向レプリケーションを利用するユーザーは、両方のTiDBクラスタでDDL文を個別に実行する必要がありました。この機能により、クラスタに`PRIMARY` BDRロールを割り当てることで、TiCDCはそのクラスタから`SECONDARY`クラスタにDDL文を複製できるようになります。

    v8.3.0 では、この機能が一般提供 (GA) されます。

    詳細については[ドキュメント](/ticdc/ticdc-bidirectional-replication.md)参照してください。

## 互換性の変更 {#compatibility-changes}

> **注記：**
>
> このセクションでは、v8.2.0から最新バージョン（v8.3.0）にアップグレードする際に知っておくべき互換性の変更点について説明します。v8.1.0以前のバージョンから最新バージョンにアップグレードする場合は、中間バージョンで導入された互換性の変更点も確認する必要があるかもしれません。

### 行動の変化 {#behavior-changes}

-   コマンドの誤用を防ぐため、 `pd-ctl`プレフィックスマッチング機構をキャンセルします。例えば、 `store remove-tombstone` `store remove` [＃8413](https://github.com/tikv/pd/issues/8413) @ [lhy1024](https://github.com/lhy1024)で呼び出すことはできません。

### システム変数 {#system-variables}

| 変数名                                                                                                           | タイプを変更   | 説明                                                                                                                                                                                                                                                                                                                  |
| ------------------------------------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size)                                 | 修正済み     | SESSION スコープを追加します。                                                                                                                                                                                                                                                                                                 |
| [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt)                                 | 修正済み     | SESSION スコープを追加します。                                                                                                                                                                                                                                                                                                 |
| [`tidb_enable_column_tracking`](/system-variables.md#tidb_enable_column_tracking-new-in-v540)                 | 修正済み     | さらにテストを行った後、デフォルト値を`OFF`から`ON`に変更します。つまり、TiDB はデフォルトで`PREDICATE COLUMNS`収集することになります。                                                                                                                                                                                                                                |
| [`tidb_gc_concurrency`](/system-variables.md#tidb_gc_concurrency-new-in-v50)                                  | 修正済み     | バージョン8.3.0以降、この変数は[ガベージコレクション（GC）](/garbage-collection-overview.md)のプロセスのステップ[ロックを解決する](/garbage-collection-overview.md#resolve-locks)と[範囲を削除](/garbage-collection-overview.md#delete-ranges)における同時スレッド数を制御します。バージョン8.3.0より前では、この変数はステップ[ロックを解決する](/garbage-collection-overview.md#resolve-locks)におけるスレッド数のみを制御します。 |
| [`tidb_low_resolution_tso`](/system-variables.md#tidb_low_resolution_tso)                                     | 修正済み     | GLOBAL スコープを追加します。                                                                                                                                                                                                                                                                                                  |
| [`tidb_opt_projection_push_down`](/system-variables.md#tidb_opt_projection_push_down-new-in-v610)             | 修正済み     | GLOBALスコープを追加し、変数値をクラスターに永続化します。さらにテストを行った後、デフォルト値を`OFF`から`ON`に変更します。これにより、オプティマイザーはTiKVコプロセッサに`Projection`プッシュダウンできるようになります。                                                                                                                                                                                       |
| [`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-new-in-v800)                           | 修正済み     | 値の範囲は`0`または`[536870912, 9223372036854775807]`に変更されました。キャッシュサイズが小さすぎるとパフォーマンスが低下するのを防ぐため、最小値は`536870912`バイト（つまり 512 MiB）です。                                                                                                                                                                                          |
| [`tidb_analyze_column_options`](/system-variables.md#tidb_analyze_column_options-new-in-v830)                 | 新しく追加された | `ANALYZE TABLE`ステートメントの動作を制御します。デフォルト値の`PREDICATE`に設定すると、 [述語列](/statistics.md#collect-statistics-on-some-columns)統計のみが収集され、 `ALL`に設定すると、すべての列の統計が収集されます。                                                                                                                                                           |
| [`tidb_enable_lazy_cursor_fetch`](/system-variables.md#tidb_enable_lazy_cursor_fetch-new-in-v830)             | 新しく追加された | [カーソルフェッチ](/develop/dev-guide-connection-parameters.md#use-streamingresult-to-get-the-execution-result)機能の動作を制御します。                                                                                                                                                                                                 |
| [`tidb_enable_shared_lock_promotion`](/system-variables.md#tidb_enable_shared_lock_promotion-new-in-v830)     | 新しく追加された | 共有ロックを排他ロックにアップグレードする機能を有効にするかどうかを制御します。この変数のデフォルト値は`OFF`で、共有ロックを排他ロックにアップグレードする機能は無効です。                                                                                                                                                                                                                            |
| [`tiflash_hashagg_preaggregation_mode`](/system-variables.md#tiflash_hashagg_preaggregation_mode-new-in-v830) | 新しく追加された | TiFlashにプッシュダウンされる 2 段階または 3 段階の HashAgg 操作の最初の段階で使用される事前集計戦略を制御します。                                                                                                                                                                                                                                                |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーションパラメータ                                                                                        | タイプを変更   | 説明                                                                                                                                                    |
| -------------- | ------------------------------------------------------------------------------------------------------ | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB           | [`tikv-client.batch-policy`](/tidb-configuration-file.md#batch-policy-new-in-v830)                     | 新しく追加された | TiDB から TiKV へのリクエストのバッチ処理戦略を制御します。                                                                                                                   |
| PD             | [`security.redact-info-log`](/pd-configuration-file.md#redact-info-log-new-in-v50)                     | 修正済み     | PD設定項目の値を`security.redact-info-log`から`"marker"`設定すると、ログ内の機密情報を直接シールドするのではなく、 `‹ ›`でマークできます`"marker"`オプションを使用すると、編集ルールをカスタマイズできます。                     |
| TiKV           | [`security.redact-info-log`](/tikv-configuration-file.md#redact-info-log-new-in-v408)                  | 修正済み     | TiKV設定項目の値を`security.redact-info-log`から`"marker"`設定すると、ログ内の機密情報を直接シールドするのではなく、 `‹ ›`でマークできます`"marker"`オプションを使用すると、編集ルールをカスタマイズできます。                   |
| TiFlash        | [`security.redact-info-log`](/tiflash/tiflash-configuration.md#configure-the-tiflash-learnertoml-file) | 修正済み     | TiFlash Learner設定項目の値を`security.redact-info-log`から`"marker"`設定することで、ログ内の機密情報を直接保護するのではなく、 `‹ ›`でマークできます。7 `"marker"`オプションを使用すると、編集ルールをカスタマイズできます。     |
| BR             | [`--allow-pitr-from-incremental`](/br/br-incremental-guide.md#limitations)                             | 新しく追加された | 増分バックアップが後続のログバックアップと互換性があるかどうかを制御します。デフォルト値は`true`で、これは増分バックアップが後続のログバックアップと互換性があることを意味します。デフォルト値`true`ままにしておくと、増分リストアを開始する前に、再生が必要なDDLが厳密にチェックされます。 |

### システムテーブル {#system-tables}

-   [`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md)と[`INFORMATION_SCHEMA.CLUSTER_PROCESSLIST`](/information-schema/information-schema-processlist.md#cluster_processlist)システムテーブルには、DML ステートメント[＃46889](https://github.com/pingcap/tidb/issues/46889) @ [lcwangchao](https://github.com/lcwangchao)によって現在影響を受けている行数を示す`SESSION_ALIAS`フィールドが追加されます。

## 非推奨の機能 {#deprecated-features}

-   次の機能は、v8.3.0 以降では非推奨になります。

    -   v7.5.0以降、 [TiDBBinlog](https://docs.pingcap.com/tidb/v8.3/tidb-binlog-overview)レプリケーションは非推奨となりました。v8.3.0以降、TiDB Binlogは完全に非推奨となり、将来のリリースで削除される予定です。増分データレプリケーションの場合は、代わりに[TiCDC](/ticdc/ticdc-overview.md)使用してください。ポイントインタイムリカバリ（PITR）の場合は、 [PITR](/br/br-pitr-guide.md)使用してください。
    -   バージョン8.3.0以降、システム変数[`tidb_enable_column_tracking`](/system-variables.md#tidb_enable_column_tracking-new-in-v540)非推奨となりました。TiDBはデフォルトで述語列を追跡します。詳細については、 [`tidb_analyze_column_options`](/system-variables.md#tidb_analyze_column_options-new-in-v830)参照してください。

-   以下の機能は将来のバージョンで廃止される予定です。

    -   TiDBでは、統計を自動的に収集するタスクの順序を最適化するために、優先度キューを有効にするかどうかを制御するためのシステム変数[`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-new-in-v800)が導入されました。将来のリリースでは、統計を自動的に収集するタスクの順序付けは優先度キューのみになるため、このシステム変数は非推奨となります。
    -   TiDBはv7.5.0でシステム変数[`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-new-in-v750)導入しました。この変数を使用すると、TiDBがパーティション統計情報を非同期にマージするように設定し、OOM問題を回避することができます。将来のリリースでは、パーティション統計情報は非同期にマージされるため、このシステム変数は非推奨となります。
    -   以降のリリースでは[実行計画バインディングの自動進化](/sql-plan-management.md#baseline-evolution)再設計する予定であり、関連する変数と動作が変更されます。
    -   TiDB v8.0.0では、並列HashAggアルゴリズムのディスクスピルをサポートするかどうかを制御するシステム変数[`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-new-in-v800)導入されました。将来のバージョンでは、システム変数[`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-new-in-v800)非推奨となる予定です。
    -   TiDB Lightningパラメータ[`conflict.max-record-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)将来のリリースで廃止される予定であり、その後削除されます。このパラメータは[`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)に置き換えられます。これは、競合レコードの最大数が、単一のインポートタスクで許容される競合レコードの最大数と一致することを意味します。

-   以下の機能は将来のバージョンで削除される予定です。

    -   TiDB Lightning v8.0.0以降、物理インポートモードの[競合検出の古いバージョン](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#the-old-version-of-conflict-detection-deprecated-in-v800)戦略は非推奨となり、 [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)パラメータを使用して論理インポートモードと物理インポートモードの両方の競合検出戦略を制御できるようになりました。旧バージョンの競合検出用の[`duplicate-resolution`](/tidb-lightning/tidb-lightning-configuration.md)パラメータは、将来のリリースで削除される予定です。

## 改善点 {#improvements}

-   TiDB

    -   `SELECT ... STRAIGHT_JOIN ... USING ( ... )`ステートメント[＃54162](https://github.com/pingcap/tidb/issues/54162) @ [ドヴェーデン](https://github.com/dveeden)をサポート
    -   `((idx_col_1 > 1) or (idx_col_1 = 1 and idx_col_2 > 10)) and ((idx_col_1 < 10) or (idx_col_1 = 10 and idx_col_2 < 20))` [＃54337](https://github.com/pingcap/tidb/issues/54337) @ [ガザルファミリーUSA](https://github.com/ghazalfamilyusa)のようなフィルタ条件に対してより正確なインデックスアクセス範囲を構築する
    -   `WHERE idx_col_1 IS NULL ORDER BY idx_col_2` [＃54188](https://github.com/pingcap/tidb/issues/54188) @ [アリエ](https://github.com/ari-e)のようなSQLクエリの余分なソート操作を避けるためにインデックス順序を使用します。
    -   `mysql.analyze_jobs`システムテーブル[＃53567](https://github.com/pingcap/tidb/issues/53567) @ [ハイラスティン](https://github.com/Rustin170506)の分析されたインデックスを表示します
    -   `EXPLAIN`ステートメントの出力に`tidb_redact_log`設定を適用し、ログ[＃54565](https://github.com/pingcap/tidb/issues/54565) @ [ホーキングレイ](https://github.com/hawkingrei)の処理ロジックをさらに最適化することをサポート
    -   クエリ効率を向上させるために、多値インデックスの`IndexRangeScan`で`Selection`演算子を生成することをサポート[＃54876](https://github.com/pingcap/tidb/issues/54876) @ [時間と運命](https://github.com/time-and-fate)
    -   設定された時間枠外で実行されているタスク`ANALYZE`自動的に強制終了する機能をサポート[＃55283](https://github.com/pingcap/tidb/issues/55283) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   統計情報がすべて TopN で構成され、対応するテーブル統計の変更された行数が 0 以外である場合に、TopN にヒットしない等価条件の推定結果を 0 から 1 に調整します[＃47400](https://github.com/pingcap/tidb/issues/47400) @ [テリー・パーセル](https://github.com/terry1purcell)
    -   TopN演算子はディスクスピル[＃47733](https://github.com/pingcap/tidb/issues/47733) @ [xzhangxian1008](https://github.com/xzhangxian1008)をサポートします
    -   TiDBノードは`WITH ROLLUP`修飾子と`GROUPING`関数[＃42631](https://github.com/pingcap/tidb/issues/42631) @ [アリーナルクス](https://github.com/Arenatlx)を使用したクエリの実行をサポートしています。
    -   システム変数[`tidb_low_resolution_tso`](/system-variables.md#tidb_low_resolution_tso) `GLOBAL`スコープ[＃55022](https://github.com/pingcap/tidb/issues/55022) @ [cfzjywxk](https://github.com/cfzjywxk)をサポートします
    -   同時実行範囲削除をサポートすることで、GC（ガベージコレクション）の効率を向上します。同時実行スレッド数は[`tidb_gc_concurrency`](/system-variables.md#tidb_gc_concurrency-new-in-v50) [＃54570](https://github.com/pingcap/tidb/issues/54570) @ [エキシウム](https://github.com/ekexium)で制御できます。
    -   バルクDML実行モードのパフォーマンスを向上させる（ `tidb_dml_type = "bulk"` ） [＃50215](https://github.com/pingcap/tidb/issues/50215) @ [エキシウム](https://github.com/ekexium)
    -   スキーマ情報キャッシュ関連インターフェース`SchemaByID` [＃54074](https://github.com/pingcap/tidb/issues/54074) @ [ywqzzy](https://github.com/ywqzzy)のパフォーマンスを向上
    -   スキーマ情報キャッシュが有効な場合の特定のシステムテーブルのクエリパフォーマンスを向上[＃50305](https://github.com/pingcap/tidb/issues/50305) @ [接線](https://github.com/tangenta)
    -   一意のインデックス[＃53004](https://github.com/pingcap/tidb/issues/53004) @ [ランス6716](https://github.com/lance6716)を追加するときに競合するキーのエラーメッセージを最適化します

-   PD

    -   リーダーの排除プロセスを加速するために、 `pd-ctl`を介して`evict-leader-scheduler`の`batch`構成を変更することをサポートします[＃8265](https://github.com/tikv/pd/issues/8265) @ [rleungx](https://github.com/rleungx)
    -   Grafanaの**「クラスタ&gt; ラベル配布**パネル」に`store_id`監視メトリックを追加して、異なるラベル[＃8337](https://github.com/tikv/pd/issues/8337) @ [HuSharp](https://github.com/HuSharp)に対応するストアIDを表示します。
    -   指定されたリソース グループが存在しない場合に、デフォルトのリソース グループへのフォールバックをサポートします[＃8388](https://github.com/tikv/pd/issues/8388) @ [Jmポテト](https://github.com/JmPotato)
    -   `pd-ctl` [＃8412](https://github.com/tikv/pd/issues/8412) @ [沢民州](https://github.com/zeminzhou)の`region`コマンドによって出力されたリージョン情報に`approximate_kv_size`フィールドを追加します。
    -   PD APIを呼び出してTTL構成[＃8450](https://github.com/tikv/pd/issues/8450) @ [lhy1024](https://github.com/lhy1024)を削除するときに返されるメッセージを最適化します
    -   大規模なクエリ読み取り要求の RU 消費動作を最適化して、他の要求への影響を軽減します[＃8457](https://github.com/tikv/pd/issues/8457) @ [ノルーシュ](https://github.com/nolouch)
    -   PDマイクロサービス[＃52912](https://github.com/pingcap/tidb/issues/52912) @ [rleungx](https://github.com/rleungx)の設定ミス時に返されるエラーメッセージを最適化します
    -   PDマイクロサービスに`--name`起動パラメータを追加して、デプロイメント中にサービス名をより正確に表示します[＃7995](https://github.com/tikv/pd/issues/7995) @ [HuSharp](https://github.com/HuSharp)
    -   領域の数に基づいて`PatrolRegionScanLimit`動的に調整して、リージョンスキャン時間を短縮する[＃7963](https://github.com/tikv/pd/issues/7963) @ [lhy1024](https://github.com/lhy1024)をサポートします。

-   TiKV

    -   `async-io`有効になっている場合、 Raftログを書き込むためのバッチポリシーを最適化して、ディスク I/O 帯域幅リソースの消費を削減します[＃16907](https://github.com/tikv/tikv/issues/16907) @ [LykxSassinator](https://github.com/LykxSassinator)
    -   TiCDC デリゲートとダウンストリーム モジュールを再設計して、リージョン部分サブスクリプション[＃16362](https://github.com/tikv/tikv/issues/16362) @ [ヒック](https://github.com/hicqu)をより適切にサポートします。
    -   単一のスロークエリログのサイズを[＃17294](https://github.com/tikv/tikv/issues/17294) @ [コナー1996](https://github.com/Connor1996)に削減
    -   新しい監視メトリック`min safe ts` [＃17307](https://github.com/tikv/tikv/issues/17307) @ [ミッタルリシャブ](https://github.com/mittalrishabh)を追加する
    -   ピアメッセージチャネル[＃16229](https://github.com/tikv/tikv/issues/16229)のメモリ使用量を[コナー1996](https://github.com/Connor1996)に減らす

-   TiFlash

    -   SVG 形式[＃9320](https://github.com/pingcap/tiflash/issues/9320) @ [カルビンネオ](https://github.com/CalvinNeo)でのアドホック ヒープ プロファイリングの生成をサポート

-   ツール

    -   バックアップと復元 (BR)

        -   ポイントインタイムリカバリ（PITR）を初めて開始する前に、フルバックアップが存在するかどうかの確認をサポートします。フルバックアップが見つからない場合、 BRはリストアを終了し、エラー[＃54418](https://github.com/pingcap/tidb/issues/54418) @ [リーヴルス](https://github.com/Leavrth)を返します。
        -   スナップショットバックアップを復元する前に、TiKVおよびTiFlashのディスク容量が十分かどうかのチェックをサポートします。容量が不足している場合、 BRは復元を終了し、エラー[＃54316](https://github.com/pingcap/tidb/issues/54316) @ [リドリスR](https://github.com/RidRisR)を返します。
        -   TiKVが各SSTファイルをダウンロードする前に、TiKVのディスク容量が十分かどうかのチェックをサポートします。容量が不足している場合、 BRは復元を終了し、エラー[＃17224](https://github.com/tikv/tikv/issues/17224) @ [リドリスR](https://github.com/RidRisR)を返します。
        -   環境変数[＃45551](https://github.com/pingcap/tidb/issues/45551) @ [リドリスR](https://github.com/RidRisR)による Alibaba Cloud アクセス資格情報の設定をサポート
        -   バックアップとリストアにBRを使用するときに OOM を回避するために、 BRプロセスの使用可能なメモリに基づいて環境変数`GOMEMLIMIT`自動的に設定します[＃53777](https://github.com/pingcap/tidb/issues/53777) @ [リーヴルス](https://github.com/Leavrth)
        -   増分バックアップをポイントインタイムリカバリ（PITR）と互換性のあるものにする[＃54474](https://github.com/pingcap/tidb/issues/54474) @ [3ポイントシュート](https://github.com/3pointer)
        -   `mysql.column_stats_usage`テーブル[＃53567](https://github.com/pingcap/tidb/issues/53567) @ [ハイラスティン](https://github.com/Rustin170506)のバックアップと復元をサポート

## バグ修正 {#bug-fixes}

-   TiDB

    -   `PipelinedWindow`の`Open`メソッドのパラメータをリセットして、 `PipelinedWindow`が`Apply`の子ノードとして使用されたときに、繰り返しの開閉操作[＃53600](https://github.com/pingcap/tidb/issues/53600) @ [徐淮嶼](https://github.com/XuHuaiyu)によって発生した以前のパラメータ値の再利用により発生する予期しないエラーを修正します。
    -   メモリ使用量が`tidb_mem_quota_query` [＃55042](https://github.com/pingcap/tidb/issues/55042) @ [イービン87](https://github.com/yibin87)で設定された制限を超えたためにクエリが終了したときに停止する可能性がある問題を修正しました
    -   HashAgg 演算子のディスク スピルにより並列計算[＃55290](https://github.com/pingcap/tidb/issues/55290) @ [xzhangxian1008](https://github.com/xzhangxian1008)中に誤ったクエリ結果が発生する問題を修正しました
    -   `YEAR` JSON 形式[＃54494](https://github.com/pingcap/tidb/issues/54494) @ [ヤンケオ](https://github.com/YangKeao)にキャストするときに間違った`JSON_TYPE`発生する問題を修正
    -   `tidb_schema_cache_size`システム変数の値の範囲が間違っている問題を修正[＃54034](https://github.com/pingcap/tidb/issues/54034) @ [リーリンハイ](https://github.com/lilinghai)
    -   パーティション式が`EXTRACT(YEAR FROM col)` [＃54210](https://github.com/pingcap/tidb/issues/54210) @ [ミョンス](https://github.com/mjonss)の場合にパーティションプルーニングが機能しない問題を修正しました
    -   データベースに多くのテーブルが存在する場合に`FLASHBACK DATABASE`失敗する問題を修正[＃54415](https://github.com/pingcap/tidb/issues/54415) @ [ランス6716](https://github.com/lance6716)
    -   多数のデータベース[＃54915](https://github.com/pingcap/tidb/issues/54915) @ [ランス6716](https://github.com/lance6716)を処理するときに`FLASHBACK DATABASE`無限ループに入る問題を修正
    -   インデックス加速モードでのインデックスの追加が失敗する可能性がある問題を修正[＃54568](https://github.com/pingcap/tidb/issues/54568) @ [ランス6716](https://github.com/lance6716)
    -   `ADMIN CANCEL DDL JOBS`により DDL が失敗する可能性がある問題を修正[＃54687](https://github.com/pingcap/tidb/issues/54687) @ [ランス6716](https://github.com/lance6716)
    -   DMから複製されたテーブルのインデックスの長さが`max-index-length` [＃55138](https://github.com/pingcap/tidb/issues/55138) @ [ランス6716](https://github.com/lance6716)で指定された最大長を超えるとテーブル複製が失敗する問題を修正しました
    -   `tidb_enable_inl_join_inner_multi_pattern`有効になっている状態で SQL 文を実行するとエラー`runtime error: index out of range`が発生する可能性がある問題を修正しました[＃54535](https://github.com/pingcap/tidb/issues/54535) @ [ヨッヘンrh](https://github.com/joechenrh)
    -   統計[＃54589](https://github.com/pingcap/tidb/issues/54589) @ [天菜まお](https://github.com/tiancaiamao)初期化プロセス中に<kbd>Control</kbd> + <kbd>C</kbd>を使用してTiDBを終了できない問題を修正しました
    -   `INL_MERGE_JOIN`オプティマイザヒントが誤った結果を返す問題を修正しました[＃54064](https://github.com/pingcap/tidb/issues/54064) @ [アイリンキッド](https://github.com/AilinKid)を廃止しました。
    -   `WITH ROLLUP`を含む相関サブクエリによって TiDB がpanic、エラー`runtime error: index out of range` [＃54983](https://github.com/pingcap/tidb/issues/54983) @ [アイリンキッド](https://github.com/AilinKid)を返す可能性がある問題を修正しました。
    -   SQLクエリのフィルタ条件に仮想列が含まれており、実行条件に`UnionScan` [＃54870](https://github.com/pingcap/tidb/issues/54870) @ [qw4990](https://github.com/qw4990)が含まれている場合に述語を適切にプッシュダウンできない問題を修正しました。
    -   `tidb_enable_inl_join_inner_multi_pattern`有効になっている状態で SQL 文を実行するとエラー`runtime error: invalid memory address or nil pointer dereference`が発生する可能性がある問題を修正しました[＃55169](https://github.com/pingcap/tidb/issues/55169) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   `UNION`を含むクエリステートメントが誤った結果[＃52985](https://github.com/pingcap/tidb/issues/52985) @ [徐淮嶼](https://github.com/XuHuaiyu)を返す可能性がある問題を修正しました
    -   `mysql.stats_histograms`表の`tot_col_size`列目が負の数[＃55126](https://github.com/pingcap/tidb/issues/55126) @ [qw4990](https://github.com/qw4990)になる可能性がある問題を修正しました
    -   `columnEvaluator`入力チャンク内の列参照を識別できず、SQL 文[＃53713](https://github.com/pingcap/tidb/issues/53713) @ [アイリンキッド](https://github.com/AilinKid)を実行すると`runtime error: index out of range`が発生する問題を修正しました。
    -   `STATS_EXTENDED`予約キーワード[＃39573](https://github.com/pingcap/tidb/issues/39573) @ [ドライブ](https://github.com/wddevries)になる問題を修正
    -   `tidb_low_resolution`有効になっている場合、 `select for update` [＃54684](https://github.com/pingcap/tidb/issues/54684) @ [cfzjywxk](https://github.com/cfzjywxk)で実行できる問題を修正しました
    -   `tidb_redact_log`有効になっている場合、内部 SQL クエリがスロークエリログに表示されない問題を修正[＃54190](https://github.com/pingcap/tidb/issues/54190) @ [lcwangchao](https://github.com/lcwangchao)
    -   トランザクションで使用されるメモリが複数回追跡される可能性がある問題を修正[＃53984](https://github.com/pingcap/tidb/issues/53984) @ [エキシウム](https://github.com/ekexium)
    -   `SHOW WARNINGS;`使用して警告を取得するとpanicが発生する可能性がある問題を修正[＃48756](https://github.com/pingcap/tidb/issues/48756) @ [xhebox](https://github.com/xhebox)
    -   インデックス統計の読み込み時にメモリリークが発生する可能性がある問題を修正[＃54022](https://github.com/pingcap/tidb/issues/54022) @ [ハイラスティン](https://github.com/Rustin170506)
    -   照合順序が`utf8_bin`または`utf8mb4_bin` [＃53730](https://github.com/pingcap/tidb/issues/53730) @ [エルサ0520](https://github.com/elsa0520)の場合に`LENGTH()`条件が予期せず削除される問題を修正しました
    -   重複した主キー[＃47539](https://github.com/pingcap/tidb/issues/47539) @ [定義2014](https://github.com/Defined2014)に遭遇したときに統計収集で`stats_history`テーブルが更新されない問題を修正しました
    -   再帰CTEクエリが無効なポインタ[＃54449](https://github.com/pingcap/tidb/issues/54449) @ [ホーキングレイ](https://github.com/hawkingrei)を生成する可能性がある問題を修正しました
    -   ハンドシェイクが完了する前に一部の接続が終了した場合に、Grafana の接続数監視メトリックが正しく表示されない問題を修正しました[＃54428](https://github.com/pingcap/tidb/issues/54428) @ [ヤンケオ](https://github.com/YangKeao)
    -   TiProxy とリソース グループ[＃54545](https://github.com/pingcap/tidb/issues/54545) @ [ヤンケオ](https://github.com/YangKeao)の使用時に各リソース グループの接続数が正しくない問題を修正しました
    -   クエリに非相関サブクエリと`LIMIT`句が含まれている場合、列のプルーニングが不完全になり、最適でないプラン[＃54213](https://github.com/pingcap/tidb/issues/54213) @ [qw4990](https://github.com/qw4990)になる可能性がある問題を修正しました。
    -   `SELECT ... FOR UPDATE` [＃54652](https://github.com/pingcap/tidb/issues/54652) @ [qw4990](https://github.com/qw4990)の間違ったポイント取得プランを再利用する問題を修正しました
    -   最初の引数が`month`で、2番目の引数が負の[＃54908](https://github.com/pingcap/tidb/issues/54908) @ [xzhangxian1008](https://github.com/xzhangxian1008)場合に`TIMESTAMPADD()`関数が無限ループに入る問題を修正しました。
    -   スローログ内の内部SQL文がデフォルトでnullに編集される問題を修正[＃54190](https://github.com/pingcap/tidb/issues/54190) [＃52743](https://github.com/pingcap/tidb/issues/52743) [＃53264](https://github.com/pingcap/tidb/issues/53264) @ [lcwangchao](https://github.com/lcwangchao)
    -   `_tidb_rowid`の`PointGet`実行プランが[＃54583](https://github.com/pingcap/tidb/issues/54583) @ [定義2014](https://github.com/Defined2014)で生成できる問題を修正
    -   v7.1 [＃54241](https://github.com/pingcap/tidb/issues/54241) @ [接線](https://github.com/tangenta)からアップグレードした後に`SHOW IMPORT JOBS`エラー`Unknown column 'summary'`を報告する問題を修正しました
    -   ビュー定義[＃54343](https://github.com/pingcap/tidb/issues/54343) @ [ランス6716](https://github.com/lance6716)でサブクエリが列定義として使用されている場合、 `information_schema.columns`を使用して列情報を取得すると警告1356が返される問題を修正しました。
    -   厳密に自己増分ではないRANGEパーティションテーブルが[＃54829](https://github.com/pingcap/tidb/issues/54829) @ [定義2014](https://github.com/Defined2014)で作成できる問題を修正
    -   SQLが異常中断されたときに`INDEX_HASH_JOIN`正常に終了できない問題を修正[＃54688](https://github.com/pingcap/tidb/issues/54688) @ [wshwsh12](https://github.com/wshwsh12)
    -   分散実行フレームワーク (DXF) を使用してインデックスを追加する際のネットワーク パーティションによって、データ インデックス[＃54897](https://github.com/pingcap/tidb/issues/54897) @ [接線](https://github.com/tangenta)の不整合が発生する可能性がある問題を修正しました。

-   PD

    -   ロールをリソースグループ[＃54417](https://github.com/pingcap/tidb/issues/54417) @ [Jmポテト](https://github.com/JmPotato)にバインドするときにエラーが報告されない問題を修正しました
    -   500 ミリ秒を超えるトークンをリクエストするとリソース グループがクォータ制限に達する問題を修正[＃8349](https://github.com/tikv/pd/issues/8349) @ [ノルーシュ](https://github.com/nolouch)
    -   `INFORMATION_SCHEMA.RUNAWAY_WATCHES`テーブルの時間データ型が正しくない問題を修正[＃54770](https://github.com/pingcap/tidb/issues/54770) @ [HuSharp](https://github.com/HuSharp)
    -   同時実行性が高い場合にリソース グループがリソース使用量を効果的に制限できない問題を修正[＃8435](https://github.com/tikv/pd/issues/8435) @ [ノルーシュ](https://github.com/nolouch)
    -   テーブル属性[＃55188](https://github.com/pingcap/tidb/issues/55188) @ [Jmポテト](https://github.com/JmPotato)を取得するときに誤った PD API が呼び出される問題を修正しました
    -   `scheduling`マイクロサービスが[＃8331](https://github.com/tikv/pd/issues/8331) @ [rleungx](https://github.com/rleungx)で有効化された後にスケーリングの進行状況が正しく表示されない問題を修正
    -   暗号化マネージャーが使用前に初期化されない問題を修正[＃8384](https://github.com/tikv/pd/issues/8384) @ [rleungx](https://github.com/rleungx)
    -   一部のログが編集されない問題を修正[＃8419](https://github.com/tikv/pd/issues/8419) @ [rleungx](https://github.com/rleungx)
    -   PDマイクロサービス[＃8406](https://github.com/tikv/pd/issues/8406) @ [HuSharp](https://github.com/HuSharp)の起動中にリダイレクトがpanicになる可能性がある問題を修正しました
    -   `split-merge-interval`構成項目の値を繰り返し変更すると（ `1s`から`1h`に変更して`1s`に戻すなど）、その設定項目が有効にならない可能性がある問題を修正しました[＃8404](https://github.com/tikv/pd/issues/8404) @ [lhy1024](https://github.com/lhy1024)
    -   `replication.strictly-match-label`を`true`に設定するとTiFlashが[＃8480](https://github.com/tikv/pd/issues/8480) @ [rleungx](https://github.com/rleungx)で起動しなくなる問題を修正
    -   大規模なパーティションテーブルを分析するときにTSOの取得が遅くなり、パフォーマンスが`ANALYZE` [rleungx](https://github.com/rleungx)する問題を修正しました[＃8500](https://github.com/tikv/pd/issues/8500)
    -   大規模クラスタにおける潜在的なデータ競合を修正[＃8386](https://github.com/tikv/pd/issues/8386) @ [rleungx](https://github.com/rleungx)
    -   クエリがランナウェイ クエリであるかどうかを判断するときに、TiDB はコプロセッサー側で費やされた時間消費のみをカウントし、TiDB 側で費やされた時間消費をカウントしないため、一部のクエリがランナウェイ クエリ[＃51325](https://github.com/pingcap/tidb/issues/51325) @ [HuSharp](https://github.com/HuSharp)として識別されない問題を修正しました。

-   TiFlash

    -   `CAST()`関数を使用して文字列をタイムゾーンまたは無効な文字を含む日付時刻に変換すると、結果が正しくなくなる問題を修正しました[＃8754](https://github.com/pingcap/tiflash/issues/8754) @ [ソロツグ](https://github.com/solotzg)
    -   データベース[＃9132](https://github.com/pingcap/tiflash/issues/9132) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)にまたがる空のパーティションを持つパーティションテーブルで`RENAME TABLE ... TO ...`実行した後にTiFlash がpanic可能性がある問題を修正しました。
    -   遅延マテリアライゼーションが有効になった後に、一部のクエリで列タイプの不一致エラーが報告される可能性がある問題を修正[＃9175](https://github.com/pingcap/tiflash/issues/9175) @ [ジンヘリン](https://github.com/JinheLin)
    -   遅延マテリアライゼーションが有効になった後、仮想生成列を含むクエリが誤った結果を返す可能性がある問題を修正[＃9188](https://github.com/pingcap/tiflash/issues/9188) @ [ジンヘリン](https://github.com/JinheLin)
    -   TiFlashで SSL 証明書の構成を空の文字列に設定すると、誤って TLS が有効になり、 TiFlashが起動しなくなる問題を修正しました[＃9235](https://github.com/pingcap/tiflash/issues/9235) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)
    -   データベースの作成直後に削除されるとTiFlash がpanic可能性がある問題を修正[＃9266](https://github.com/pingcap/tiflash/issues/9266) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)
    -   TiFlashとPD間のネットワークパーティション（ネットワーク切断）により、読み取り要求タイムアウトエラー[＃9243](https://github.com/pingcap/tiflash/issues/9243) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)が発生する可能性がある問題を修正しました。
    -   分散storageおよびコンピューティングアーキテクチャ[＃9282](https://github.com/pingcap/tiflash/issues/9282) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)でTiFlash書き込みノードが再起動に失敗する可能性がある問題を修正しました
    -   分散storageおよびコンピューティングアーキテクチャ[＃9298](https://github.com/pingcap/tiflash/issues/9298) @ [ジンヘリン](https://github.com/JinheLin)で、 TiFlash書き込みノードの読み取りスナップショットがタイムリーにリリースされない問題を修正しました。

-   TiKV

    -   古い領域をクリーンアップすると、有効なデータ[＃17258](https://github.com/tikv/tikv/issues/17258) @ [ヒビシェン](https://github.com/hbisheng)が誤って削除される可能性がある問題を修正しました
    -   Grafana [＃15990](https://github.com/tikv/tikv/issues/15990) @ [コナー1996](https://github.com/Connor1996)の TiKV ダッシュボードで`Ingestion picked level`と`Compaction Job Size(files)`誤って表示される問題を修正しました
    -   `cancel_generating_snap`誤って更新すると`snap_tried_cnt`が TiKV でpanicになる問題を修正[＃17226](https://github.com/tikv/tikv/issues/17226) @ [ヒビシェン](https://github.com/hbisheng)
    -   `Ingest SST duration seconds`の情報が間違っている問題を修正[＃17239](https://github.com/tikv/tikv/issues/17239) @ [LykxSassinator](https://github.com/LykxSassinator)
    -   エラー発生時にCPUプロファイリングフラグが正しくリセットされない問題を修正[＃17234](https://github.com/tikv/tikv/issues/17234) @ [コナー1996](https://github.com/Connor1996)
    -   ブルームフィルタが以前のバージョン（v7.1より前）とそれ以降のバージョン[＃17272](https://github.com/tikv/tikv/issues/17272) @ [v01dstar](https://github.com/v01dstar)の間で互換性がない問題を修正しました

-   ツール

    -   バックアップと復元 (BR)

        -   `ADD INDEX`や`MODIFY COLUMN`などのバックフィルを必要とする DDL が、増分リストア[＃54426](https://github.com/pingcap/tidb/issues/54426) @ [3ポイントシュート](https://github.com/3pointer)中に正しく回復されない可能性がある問題を修正しました。
        -   バックアップと復元[＃54140](https://github.com/pingcap/tidb/issues/54140) @ [リーヴルス](https://github.com/Leavrth)中に進行が停止する問題を修正
        -   バックアップと復元のチェックポイントパスが一部の外部storageと互換性がない問題を修正[＃55265](https://github.com/pingcap/tidb/issues/55265) @ [リーヴルス](https://github.com/Leavrth)

    -   TiCDC

        -   下流の Kafka にアクセスできない場合にプロセッサがスタックする可能性がある問題を修正[＃11340](https://github.com/pingcap/tiflow/issues/11340) @ [アズドンメン](https://github.com/asddongmen)

    -   TiDB データ移行 (DM)

        -   スキーマ トラッカーが LIST パーティション テーブルを誤って処理し、DM エラー[＃11408](https://github.com/pingcap/tiflow/issues/11408) @ [ランス6716](https://github.com/lance6716)が発生する問題を修正しました。
        -   インデックスの長さがデフォルト値の`max-index-length` [＃11459](https://github.com/pingcap/tiflow/issues/11459) @ [マイケル・ムデン](https://github.com/michaelmdeng)を超えるとデータレプリケーションが中断される問題を修正しました
        -   DMが`FAKE_ROTATE_EVENT`正しく処理できない問題を修正[＃11381](https://github.com/pingcap/tiflow/issues/11381) @ [ランス6716](https://github.com/lance6716)

    -   TiDB Lightning

        -   TiDB Lightningがキースペース名[＃54232](https://github.com/pingcap/tidb/issues/54232) @ [ケニーtm](https://github.com/kennytm)の取得に失敗したときに混乱を招く`WARN`ログを出力する問題を修正
        -   TiDB LightningのTLS構成がクラスタ証明書[＃54172](https://github.com/pingcap/tidb/issues/54172) @ [杉本英](https://github.com/ei-sugimoto)に影響する問題を修正
        -   TiDB Lightning [＃49826](https://github.com/pingcap/tidb/issues/49826) @ [ランス6716](https://github.com/lance6716)を使用してデータのインポート中にトランザクションの競合が発生する問題を修正しました
        -   多数のデータベースとテーブル[＃55054](https://github.com/pingcap/tidb/issues/55054) @ [D3ハンター](https://github.com/D3Hunter)のインポート中に大きなチェックポイント ファイルによってパフォーマンスが低下する問題を修正しました

## 寄稿者 {#contributors}

TiDB コミュニティからの以下の貢献者に感謝いたします。

-   [アリエ](https://github.com/ari-e)
-   [杉本英](https://github.com/ei-sugimoto)
-   [HaoW30](https://github.com/HaoW30)
-   [ジャックL9u](https://github.com/JackL9u)
-   [マイケル・ムデン](https://github.com/michaelmdeng)
-   [ミッタルリシャブ](https://github.com/mittalrishabh)
-   [qingfeng777](https://github.com/qingfeng777)
-   [サンディープ・パディ](https://github.com/SandeepPadhi)
-   [yzhan1](https://github.com/yzhan1)
