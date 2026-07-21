---
title: TiDB 8.3.0 Release Notes
summary: TiDB 8.3.0 の新機能、互換性の変更点、改善点、およびバグ修正についてご確認ください。
---

# TiDB 8.3.0 リリースノート {#tidb-8-3-0-release-notes}

発売日：2024年8月22日

TiDBバージョン：8.3.0

クイックアクセス: [クイックスタート](https://docs-archive.pingcap.com/tidb/v8.3/quick-start-with-tidb/)

バージョン8.3.0では、以下の主要な機能と改善点が導入されています。

<table><thead><tr><th>カテゴリ</th><th>機能／改善点</th><th>説明</th></tr></thead><tbody><tr><td rowspan="3">拡張性とパフォーマンス</td><td><a href="https://docs-archive.pingcap.com/tidb/v8.3/partitioned-table/#global-indexes">パーティションテーブルのグローバルインデックス（実験的）</a></td><td>グローバルインデックスを使用すると、パーティション化されていない列の取得効率を効果的に向上させることができ、一意キーにパーティションキーを含める必要があるという制約を取り除くことができます。この機能により、TiDBパーティションテーブルの使用シナリオが拡張され、データ移行時に必要となる可能性のあるアプリケーションの変更作業の一部を回避できます。</td></tr><tr><td> <a href="https://docs-archive.pingcap.com/tidb/v8.3/system-variables/#tidb_opt_projection_push_down-new-in-v610"><code>Projection</code>演算子をストレージエンジンにデフォルトでプッシュダウンする</a></td><td><code>Projection</code>演算子をストレージエンジンにプッシュダウンすることで、ストレージノード全体に負荷を分散させ、ノード間のデータ転送量を削減できます。この最適化により、特定のSQLクエリの実行時間が短縮され、データベース全体のパフォーマンスが向上します。</td></tr><tr><td><a href="https://docs-archive.pingcap.com/tidb/v8.3/statistics/#collect-statistics-on-some-columns">統計情報を収集する際に不要な列を無視する</a></td><td>オプティマイザが必要な情報を確実に取得できるという前提のもと、TiDBは統計情報の収集を高速化し、統計情報の適時性を向上させることで、最適な実行プランの選択を保証し、クラスタのパフォーマンスを向上させます。同時に、TiDBはシステムオーバーヘッドを削減し、リソース利用率も向上させます。</td></tr><tr><td rowspan="1">信頼性と可用性</td><td><a href="https://docs-archive.pingcap.com/tidb/v8.3/tiproxy-overview/">TiProxyに組み込まれた仮想IP管理機能</a></td><td>TiProxyは、仮想IP管理機能を内蔵しています。設定することで、外部プラットフォームやツールに依存することなく、仮想IPの自動切り替えをサポートします。この機能により、TiProxyの導入が簡素化され、データベースアクセスレイヤーの複雑さが軽減されます。</td></tr></tbody></table>

## 機能の詳細 {#feature-details}

### パフォーマンス {#performance}

-   オプティマイザは`Projection`演算子をデフォルトでストレージエンジンにプッシュダウンすることを可能にします [#51876](https://github.com/pingcap/tidb/issues/51876) @[yibin87](https://github.com/yibin87)

    `Projection`演算子をストレージエンジンにプッシュダウンすると、計算エンジンとストレージエンジン間のデータ転送が削減され、SQL 実行パフォーマンスが向上します。これは[JSONクエリ関数](/functions-and-operators/json-functions/json-functions-search.md)含むクエリに特に効果的です。 または[JSON値属性関数](/functions-and-operators/json-functions/json-functions-return.md)。v8.3.0 以降、TiDB は、この機能を制御するシステム変数[`tidb_opt_projection_push_down`](/system-variables.md#tidb_opt_projection_push_down-new-in-v610)のデフォルト値を`Projection`から`OFF` `ON`ダウン機能をデフォルトで有効にします。この機能が有効になると、オプティマイザは、対象となる JSON クエリ関数と JSON 値属性関数を自動的にストレージエンジンにプッシュダウンします。

    詳細については、 [ドキュメント](/system-variables.md#tidb_opt_projection_push_down-new-in-v610)を参照してください。

-   キーバリュー（KV）リクエストのバッチ処理戦略を最適化する [#55206](https://github.com/pingcap/tidb/issues/55206) @[zyguan](https://github.com/zyguan)

    TiDB は、TiKV に KV リクエストを送信することでデータを取得します。KV リクエストをバッチ処理することで、実行パフォーマンスを大幅に向上させることができます。v8.3.0 より前のバージョンでは、TiDB のバッチ処理戦略は効率が劣っていました。v8.3.0 以降では、既存の戦略に加えて、より効率的なバッチ処理戦略がいくつか導入されています。さまざまなワークロードに対応するため、 [`tikv-client.batch-policy`](/tidb-configuration-file.md#batch-policy-new-in-v830)設定項目を使用して、異なるバッチ処理戦略を設定できます。

    詳細については、 [ドキュメント](/tidb-configuration-file.md#batch-policy-new-in-v830)を参照してください。

-   TiFlash は、高 NDV データのパフォーマンスを向上させるために HashAgg 集計計算モードを導入 [#9196](https://github.com/pingcap/tiflash/issues/9196) @[guo-shaoge](https://github.com/guo-shaoge)

    バージョン8.3.0より前のTiFlashでは、NDV（一意の値の数）が多いデータを扱う場合、HashAgg集計の最初の段階で集計計算効率が低いという問題がありました。バージョン8.3.0以降、 TiFlashは複数のHashAgg集計計算モードを導入し、さまざまなデータ特性に対応した集計パフォーマンスを向上させています。目的のHashAgg集計計算モードを選択するには、システム変数[`tiflash_hashagg_preaggregation_mode`](/system-variables.md#tiflash_hashagg_preaggregation_mode-new-in-v830)を設定してください。

    詳細については、 [ドキュメント](/system-variables.md#tiflash_hashagg_preaggregation_mode-new-in-v830)を参照してください。

-   統計を収集するときに不要な列を無視する [#53567](https://github.com/pingcap/tidb/issues/53567) @[Rustin170506](https://github.com/Rustin170506)

    オプティマイザが実行プランを生成する際、フィルタ条件の列、結合キーの列、集計に使用される列など、一部の列の統計情報のみが必要となります。TiDBはv8.3.0以降、SQL文で使用される列の履歴レコードを継続的に監視します。デフォルトでは、TiDBはインデックスを持つ列と、統計情報の収集が必要であると判断された列の統計情報のみを収集します。これにより、統計情報の収集が高速化され、不要なリソース消費が回避されます。

    クラスターをv8.3.0より前のバージョンからv8.3.0以降にアップグレードすると、TiDBはデフォルトで元の動作、つまりすべての列の統計情報を収集する動作を維持します。この機能を有効にするには、システム変数[`tidb_analyze_column_options`](/system-variables.md#tidb_analyze_column_options-new-in-v830) `PREDICATE`に手動で設定する必要があります。新しくデプロイされたクラスターでは、この機能はデフォルトで有効になっています。

    ランダムクエリを多数実行する分析システムの場合、ランダムクエリのパフォーマンスを確保するために、システム変数[`tidb_analyze_column_options`](/system-variables.md#tidb_analyze_column_options-new-in-v830) `ALL`に設定して、すべての列の統計情報を収集することができます。その他のタイプのシステムでは、tidb_analyze_column_options のデフォルト設定 ( `PREDICATE` ) を維持して、必要な列のみの統計情報を収集することを[`tidb_analyze_column_options`](/system-variables.md#tidb_analyze_column_options-new-in-v830) 。

    詳細については、 [ドキュメント](/statistics.md#collect-statistics-on-some-columns)を参照してください。

-   一部のシステムテーブルのクエリパフォーマンスを改善 [#50305](https://github.com/pingcap/tidb/issues/50305) @[tangenta](https://github.com/tangenta)

    以前のバージョンでは、クラスタサイズが大きくなり、テーブル数が多くなると、システムテーブルへのクエリのパフォーマンスが低下していました。

    バージョン8.0.0では、以下の4つのシステムテーブルについてクエリパフォーマンスが最適化されています。

    -   `INFORMATION_SCHEMA.TABLES`
    -   `INFORMATION_SCHEMA.STATISTICS`
    -   `INFORMATION_SCHEMA.KEY_COLUMN_USAGE`
    -   `INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS`

    バージョン8.3.0では、以下のシステムテーブルについてクエリのパフォーマンスが最適化され、バージョン8.2.0と比較してパフォーマンスが大幅に向上しています。

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

-   パーティション式`EXTRACT(YEAR_MONTH...)`関数を使用する場合にパーティション剪定をサポートしてクエリのパフォーマンスを向上させる [#54209](https://github.com/pingcap/tidb/pull/54209) @[mjonss](https://github.com/mjonss)

    以前のバージョンでは、パーティション式で`EXTRACT(YEAR_MONTH...)`関数を使用する場合、パーティションプルーニングがサポートされておらず、クエリのパフォーマンスが低下していました。v8.3.0 以降では、パーティション式で`EXTRACT(YEAR_MONTH...)`関数を使用する場合にパーティションプルーニングがサポートされ、クエリのパフォーマンスが向上します。

    詳細については、[ドキュメント](/partition-pruning.md#scenario-three)を参照してください。

-   `CREATE TABLE`のパフォーマンスを 1.4 倍、 `CREATE DATABASE`のパフォーマンスを 2.1 倍、 `ADD COLUMN`を 2 倍向上させます [#54436](https://github.com/pingcap/tidb/issues/54436) @[D3Hunter](https://github.com/D3Hunter)

    TiDB v8.0.0では、バッチテーブル作成シナリオにおけるテーブル作成パフォーマンスを向上させるため、システム変数[`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-new-in-v800)が導入されました。v8.3.0では、単一データベース内で10セッションにわたってテーブル作成用のDDLステートメントを同時に送信した場合、v8.2.0と比較してパフォーマンスが1.4倍向上しています。

    v8.3.0 では、v8.2.0 と比較して、バッチ実行における一般的な DDL のパフォーマンスが向上しました。10 セッションを同時に実行した場合の`CREATE DATABASE`のパフォーマンスは、v8.1.0 と比較して 19 倍、v8.2.0 と比較して 2.1 倍向上しました。同じデータベース内の複数のテーブルに列 ( `ADD COLUMN` ) をバッチで追加するために 10 セッションを使用した場合のパフォーマンスは、v8.1.0 と比較して 10 倍、v8.2.0 と比較して 2.1 倍向上しました。同じデータベース内の複数のテーブルで 10 セッションを使用した`ADD COLUMN`のパフォーマンスは、v8.1.0 と比較して 10 倍、v8.2.0 と比較して 2 倍向上しました。

    詳細については、 [ドキュメント](/system-variables.md#tidb_enable_fast_create_table-new-in-v800)を参照してください。

-   パーティション テーブルはグローバル インデックスをサポートします (実験的) [#45133](https://github.com/pingcap/tidb/issues/45133) @[mjonss](https://github.com/mjonss)@[Defined2014](https://github.com/Defined2014) @[jiyfhust](https://github.com/jiyfhust)@[L-maple](https://github.com/L-maple)

    以前のバージョンのパーティションテーブルでは、グローバルインデックスがサポートされていないため、いくつかの制限がありました。たとえば、一意キーはテーブルのパーティション式内のすべての列を使用する必要があります。クエリ条件でパーティションキーを使用しない場合、クエリはすべてのパーティションをスキャンするため、パフォーマンスが低下します。v7.6.0以降では、グローバルインデックス機能を有効にするためにシステム変数[`tidb_enable_global_index`](/system-variables.md#tidb_enable_global_index-new-in-v760)が導入されました。ただし、この機能は当時開発中であったため、有効にすることは推奨されません。

    バージョン8.3.0以降、グローバルインデックス機能は実験的機能としてリリースされました。キーワード`Global`を使用してパーティションテーブルのグローバルインデックスを明示的に作成することで、一意キーがテーブルのパーティション式内のすべての列を使用する必要があるという制約を取り除き、柔軟なビジネスニーズに対応できます。グローバルインデックスは、パーティションキーを含まないクエリのパフォーマンスも向上させます。

    詳細については、[ドキュメント](/global-indexes.md)を参照してください。

### 信頼性 {#reliability}

-   ストリーミングカーソル結果セットのサポート（実験的） [#54526](https://github.com/pingcap/tidb/issues/54526) @[YangKeao](https://github.com/YangKeao)

    アプリケーションコードが[カーソルフェッチ](/develop/dev-guide-connection-parameters.md#use-streamingresult-to-get-the-execution-result)を使用して結果セットを取得する場合、TiDBは通常、まず結果セット全体をメモリに格納し、その後データをバッチ処理でクライアントに返します。結果セットが大きすぎる場合は、TiDBは一時的に結果をハードディスクに書き込むことがあります。

    バージョン8.3.0以降では、システム変数[`tidb_enable_lazy_cursor_fetch`](/system-variables.md#tidb_enable_lazy_cursor_fetch-new-in-v830) `ON`に設定すると、TiDBはすべてのデータをTiDBノードに読み込むのではなく、クライアントが読み込むにつれて徐々にデータをTiDBノードに読み込むようになります。TiDBが大規模な結果セットを処理する場合、この機能によりTiDBノードのメモリ使用量が削減され、クラスタの安定性が向上します。

    詳細については、 [ドキュメント](/system-variables.md#tidb_enable_lazy_cursor_fetch-new-in-v830)を参照してください。

-   SQL 実行プランのバインディングを強化[#55280](https://github.com/pingcap/tidb/issues/55280) [#55343](https://github.com/pingcap/tidb/issues/55343) @[time-and-fate](https://github.com/time-and-fate)

    OLTPシナリオでは、ほとんどのSQLステートメントの最適な実行プランは固定されています。アプリケーション内の重要なSQLステートメントに対してSQL実行プランバインディングを実装することで、実行プランが悪化する可能性を低減し、システムの安定性を向上させることができます。多数のSQL実行プランバインディングを作成するという要件を満たすために、TiDBはSQLバインディングの機能とエクスペリエンスを強化しており、具体的には以下の機能が含まれています。

    -   単一のSQL文を使用して、複数の過去の実行プランからSQL実行プランバインディングを作成することで、バインディング作成の効率を向上させます。
    -   SQL実行プランバインディングは、より多くのオプティマイザヒントをサポートし、複雑な実行プランの変換方法を最適化することで、実行プランの復元におけるバインディングの安定性を向上させます。

    詳細については、[ドキュメント](/sql-plan-management.md)を参照してください。

### 可用性 {#availability}

-   TiProxyは仮想IP管理機能を内蔵しています [#583](https://github.com/pingcap/tiproxy/issues/583) @[djshow832](https://github.com/djshow832)

    バージョン8.3.0より前は、高可用性を実現するためにプライマリ/セカンダリモードを使用する場合、TiProxyは仮想IPアドレスを管理するための追加コンポーネントを必要としていました。バージョン8.3.0以降、TiProxyは仮想IPアドレス管理機能を内蔵しています。プライマリ/セカンダリモードでプライマリノードがフェイルオーバーすると、新しいプライマリノードは指定された仮想IPアドレスに自動的にバインドされるため、クライアントは常に仮想IPアドレスを介して利用可能なTiProxyに接続できます。

    仮想IPアドレス管理を有効にするには、TiProxy設定項目[`ha.virtual-ip`](/tiproxy/tiproxy-configuration.md#virtual-ip)使用して仮想IPアドレスを指定し、[`ha.interface`](/tiproxy/tiproxy-configuration.md#interface)を使用して仮想IPアドレスをバインドするネットワークインターフェイスを指定します。仮想IPアドレスは、これら両方の設定項目が設定されている場合にのみ、TiProxyインスタンスにバインドされます。

    詳細については、[ドキュメント](/tiproxy/tiproxy-overview.md)を参照してください。

### SQL {#sql}

-   `SELECT LOCK IN SHARE MODE`を排他ロックにアップグレードするサポート [#54999](https://github.com/pingcap/tidb/issues/54999) @[cfzjywxk](https://github.com/cfzjywxk)

    TiDB はまだ`SELECT LOCK IN SHARE MODE`をサポートしていません。v8.3.0 以降、TiDB は`SELECT LOCK IN SHARE MODE`排他ロックにアップグレードして`SELECT LOCK IN SHARE MODE`のサポートを有効にすることをサポートしています。この機能を有効にするかどうかは、新しいシステム変数[`tidb_enable_shared_lock_promotion`](/system-variables.md#tidb_enable_shared_lock_promotion-new-in-v830)を使用して制御できます。

    詳細については、 [ドキュメント](/system-variables.md#tidb_enable_shared_lock_promotion-new-in-v830)を参照してください。

### 可観測性 {#observability}

-   初期統計の読み込みの進行状況を表示 [#53564](https://github.com/pingcap/tidb/issues/53564) @[hawkingrei](https://github.com/hawkingrei)

    TiDB は起動時に基本統計情報をロードします。テーブルやパーティションが多いシナリオでは、この処理に時間がかかる場合があります。設定項目[`force-init-stats`](/tidb-configuration-file.md#force-init-stats-new-in-v657-and-v710)が`ON`に設定されている場合、TiDB は初期統計情報がロードされるまでサービスを提供しません。この場合、ロード処理を監視してサービスの開始時間を推定する必要があります。

    バージョン8.3.0以降、TiDBは初期統計情報の読み込み状況を段階的にログに出力ようになり、実行状況を把握しやすくなりました。外部ツールにフォーマット済みの結果を提供するために、TiDBは[監視API](/tidb-monitoring-api.md)を追加しました。これにより、起動フェーズ中の任意の時点で初期統計情報の読み込み状況を取得できます。

-   リクエストユニット（RU）設定に関するメトリクスを追加 [#8444](https://github.com/tikv/pd/issues/8444) @[nolouch](https://github.com/nolouch)

### セキュリティ {#security}

-   PDログの編集機能強化 [#8305](https://github.com/tikv/pd/issues/8305) @[JmPotato](https://github.com/JmPotato)

    TiDB v8.0.0 では、ログのマスキング機能が強化され、TiDB ログ内のユーザーデータを`‹ ›`でマークできるようになりました。マークされたログに基づいて、ログを表示する際にマークされた情報をマスキングするかどうかを決定できるため、ログのマスキングの柔軟性が向上します。v8.2.0 では、 TiFlash同様のログマスキング機能強化を実装しています。

    バージョン8.3.0では、PDは同様のログ編集機能強化を実装しています。この機能を使用するには、PD構成項目`security.redact-info-log`の値を`"marker"`に設定します。

    詳細については、 [ドキュメント](/log-redaction.md#log-redaction-in-pd-side)を参照してください。

-   TiKV ログ編集の強化 [#17206](https://github.com/tikv/tikv/issues/17206) @[LykxSassinator](https://github.com/LykxSassinator)

    TiDB v8.0.0 では、ログのマスキング機能が強化され、TiDB ログ内のユーザーデータを`‹ ›`でマークできるようになりました。マークされたログに基づいて、ログを表示する際にマークされた情報をマスキングするかどうかを決定できるため、ログのマスキングの柔軟性が向上します。v8.2.0 では、 TiFlash同様のログマスキング機能強化を実装しています。

    バージョン8.3.0では、TiKVは同様のログ編集機能強化を実装しています。この機能を使用するには、TiKV構成項目`security.redact-info-log`の値を`"marker"`に設定します。

    詳細については、 [ドキュメント](/log-redaction.md#log-redaction-in-tikv-side)を参照してください。

### データ移行 {#data-migration}

-   TiCDCは双方向レプリケーション（BDR）モードでのDDLステートメントのレプリケーションをサポートします（GA） [#10301](https://github.com/pingcap/tiflow/issues/10301) [#48519](https://github.com/pingcap/tidb/issues/48519) @[okJiang](https://github.com/okJiang) @[asddongmen](https://github.com/asddongmen)

    TiCDC v7.6.0 では、双方向レプリケーションが構成された DDL ステートメントのレプリケーションが導入されました。以前は、TiCDC は DDL ステートメントの双方向レプリケーションをサポートしていなかったため、TiCDC の双方向レプリケーションを使用するユーザーは、両方の TiDB クラスタで DDL ステートメントを個別に実行する必要がありました。この機能により、クラスタに`PRIMARY` BDR ロールを割り当てると、TiCDC はそのクラスタから`SECONDARY`クラスタに DDL ステートメントをレプリケートできます。

    バージョン8.3.0では、この機能が一般提供（GA）されます。

    詳細については、 [ドキュメント](/ticdc/ticdc-bidirectional-replication.md)を参照してください。

## 互換性の変更 {#compatibility-changes}

> **Note:**
>
> このセクションでは、v8.2.0 から最新バージョン (v8.3.0) にアップグレードする際に知っておくべき互換性の変更点について説明します。v8.1.0 以前のバージョンから最新バージョンにアップグレードする場合は、中間バージョンで導入された互換性の変更点も確認する必要があるかもしれません。

### 動作の変更 {#behavior-changes}

-   コマンドの誤用を防ぐため、 `pd-ctl`はプレフィックスマッチングメカニズムを無効にします。たとえば、 `store remove-tombstone` `store remove`を介して呼び出すことはできません。 [#8413](https://github.com/tikv/pd/issues/8413) @[lhy1024](https://github.com/lhy1024)

### システム変数 {#system-variables}

| 変数名                                                                                                           | 変更の種類  | 説明                                                                                                                                                                                                                                                                                                       |
| ------------------------------------------------------------------------------------------------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size)                                 | 変更     | SESSIONスコープを追加します。                                                                                                                                                                                                                                                                                       |
| [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt)                                 | 変更     | SESSIONスコープを追加します。                                                                                                                                                                                                                                                                                       |
| [`tidb_enable_column_tracking`](/system-variables.md#tidb_enable_column_tracking-new-in-v540)                 | 変更     | さらなるテストの結果、デフォルト値が`OFF`から`ON`に変更されます。これは、TiDB がデフォルトで`PREDICATE COLUMNS`を収集することを意味します。                                                                                                                                                                                                                   |
| [`tidb_gc_concurrency`](/system-variables.md#tidb_gc_concurrency-new-in-v50)                                  | 変更     | v8.3.0 以降、この変数は[ごみ収集（GC）](/garbage-collection-overview.md)プロセスの[ロックを解除する](/garbage-collection-overview.md#resolve-locks)ステップと[範囲を削除](/garbage-collection-overview.md#delete-ranges)ステップ中の同時スレッドの数を制御します。 v8.3.0 より前では、この変数は[ロックを解除する](/garbage-collection-overview.md#resolve-locks)ステップ中のスレッド数のみを制御します。 |
| [`tidb_low_resolution_tso`](/system-variables.md#tidb_low_resolution_tso)                                     | 変更     | グローバルスコープを追加します。                                                                                                                                                                                                                                                                                         |
| [`tidb_opt_projection_push_down`](/system-variables.md#tidb_opt_projection_push_down-new-in-v610)             | 変更     | GLOBAL スコープを追加し、変数の値をクラスタに永続化します。さらにテストを行った結果、デフォルト値を`OFF`から`ON`に変更します。これは、オプティマイザが`Projection` TiKV コプロセッサにプッシュできることを意味します。                                                                                                                                                                             |
| [`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-new-in-v800)                           | 変更     | 値の範囲は`0`または`[536870912, 9223372036854775807]`に変更されました。キャッシュサイズが小さすぎてパフォーマンスが低下するのを避けるため、最小値は`536870912`バイト (つまり 512 MiB) です。                                                                                                                                                                             |
| [`tidb_analyze_column_options`](/system-variables.md#tidb_analyze_column_options-new-in-v830)                 | 新しく追加された | `ANALYZE TABLE`ステートメントの動作を制御します。デフォルト値の`PREDICATE`に設定すると、 [述語列](/statistics.md#collect-statistics-on-some-columns)の統計情報のみが収集されます。 `ALL`に設定すると、すべての列の統計情報が収集されます。                                                                                                                                         |
| [`tidb_enable_lazy_cursor_fetch`](/system-variables.md#tidb_enable_lazy_cursor_fetch-new-in-v830)             | 新しく追加された | [カーソルフェッチ](/develop/dev-guide-connection-parameters.md#use-streamingresult-to-get-the-execution-result)機能の動作を制御します。                                                                                                                                                                                      |
| [`tidb_enable_shared_lock_promotion`](/system-variables.md#tidb_enable_shared_lock_promotion-new-in-v830)     | 新しく追加された | 共有ロックを排他ロックにアップグレードする機能を有効にするかどうかを制御します。この変数のデフォルト値は`OFF`であり、これは共有ロックを排他ロックにアップグレードする機能が無効になっていることを意味します。                                                                                                                                                                                                |
| [`tiflash_hashagg_preaggregation_mode`](/system-variables.md#tiflash_hashagg_preaggregation_mode-new-in-v830) | 新しく追加された | TiFlashにプッシュダウンされる2段階または3段階のHashAgg操作の最初の段階で使用される事前集計戦略を制御します。                                                                                                                                                                                                                                           |

### コンフィグレーションファイルパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーションパラメータ                                                                                        | 変更の種類  | 説明                                                                                                                                                      |
| -------------- | ------------------------------------------------------------------------------------------------------ | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB           | [`tikv-client.batch-policy`](/tidb-configuration-file.md#batch-policy-new-in-v830)                     | 新しく追加された | TiDBからTiKVへのリクエストのバッチ処理戦略を制御します。                                                                                                                        |
| PD             | [`security.redact-info-log`](/pd-configuration-file.md#redact-info-log-new-in-v50)                     | 変更     | PD構成項目`security.redact-info-log`の値を`"marker"`に設定することで、ログ内の機密情報を直接シールドする代わりに`‹ ›`でマークできます。 `"marker"`オプションを使用すると、マスキングルールをカスタマイズできます。                    |
| TiKV           | [`security.redact-info-log`](/tikv-configuration-file.md#redact-info-log-new-in-v408)                  | 変更     | TiKV 設定項目`security.redact-info-log`の値を`"marker"`に設定することで、ログ内の機密情報を直接シールドする代わりに`‹ ›`でマークできます。 `"marker"`オプションを使用すると、マスキングルールをカスタマイズできます。                 |
| TiFlash        | [`security.redact-info-log`](/tiflash/tiflash-configuration.md#configure-the-tiflash-learnertoml-file) | 変更     | TiFlash Learnerの設定項目`security.redact-info-log`の値を`"marker"`に設定することで、ログ内の機密情報を直接シールドする代わりに`‹ ›`でマークすることができます。 `"marker"`オプションを使用すると、マスキングルールをカスタマイズできます。 |
| BR             | [`--allow-pitr-from-incremental`](/br/br-incremental-guide.md#limitations)                             | 新しく追加された | 増分バックアップが後続のログバックアップと互換性があるかどうかを制御します。デフォルト値は`true`で、これは増分バックアップが後続のログバックアップと互換性があることを意味します。デフォルト値`true`ままにすると、増分リストアが開始される前に、再生が必要な DDL が厳密にチェックされます。  |

### システムテーブル {#system-tables}

-   [`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md)および[`INFORMATION_SCHEMA.CLUSTER_PROCESSLIST`](/information-schema/information-schema-processlist.md#cluster_processlist)システム テーブルに`SESSION_ALIAS`フィールドが追加され、DML ステートメントによって現在影響を受けている行数が表示されます。[#46889](https://github.com/pingcap/tidb/issues/46889) @[lcwangchao](https://github.com/lcwangchao)

## 非推奨機能 {#deprecated-features}

-   バージョン8.3.0以降、以下の機能は非推奨となります。

    -   バージョン 7.5.0 以降、 [TiDB Binlog](https://docs-archive.pingcap.com/tidb/v8.3/tidb-binlog-overview/)レプリケーションは非推奨となりました。バージョン 8.3.0 以降、TiDB Binlog は完全に非推奨となり、今後のリリースで削除される予定です。増分データレプリケーションには、代わりに[TiCDC](/ticdc/ticdc-overview.md)を使用してください。ポイントインタイムリカバリ(PITR) には、 [PITR](/br/br-pitr-guide.md)を使用してください。
    -   バージョン8.3.0以降、 [`tidb_enable_column_tracking`](/system-variables.md#tidb_enable_column_tracking-new-in-v540)システム変数は非推奨となりました。TiDBはデフォルトで述語列を追跡します。詳細については、 [`tidb_analyze_column_options`](/system-variables.md#tidb_analyze_column_options-new-in-v830)参照してください。

-   以下の機能は、将来のバージョンで廃止される予定です。

    -   TiDBでは、統計情報を自動的に収集するタスクの順序を最適化するために優先度キューを有効にするかどうかを制御するためのシステム変数[`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-new-in-v800)が導入されました。今後のリリースでは、統計情報を自動的に収集するタスクの順序付けには優先度キューが唯一の方法となるため、このシステム変数は非推奨となります。
    -   TiDBはv7.5.0でシステム変数[`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-new-in-v750)を導入しました。この変数を使用すると、TiDBがパーティション統計の非同期マージを使用するように設定し、メモリ不足の問題を回避できます。今後のリリースでは、パーティション統計は非同期でマージされるため、このシステム変数は非推奨となります。
    -   今後のリリースでは [実行プランバインディングの自動進化](/sql-plan-management.md#baseline-evolution)が再設計される予定であり、関連する変数と動作が変更されます。
    -   バージョン8.0.0では、TiDBが並列ハッシュアグリゲーションアルゴリズムのディスクスピルをサポートするかどうかを制御するシステム変数[`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-new-in-v800)が導入されました。今後のバージョンでは、 [`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-new-in-v800)システム変数は非推奨となります。
    -   TiDB Lightning のパラメータ[`conflict.max-record-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task) 、今後のリリースで非推奨となり、その後削除されます。このパラメータは[`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)に置き換えられます。これは、競合するレコードの最大数が、単一のインポートタスクで許容できる競合レコードの最大数と一致することを意味します。

-   今後のバージョンでは、以下の機能が削除される予定です。

    -   バージョン8.0.0以降、 TiDB Lightningは[旧バージョンの競合検出](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#the-old-version-of-conflict-detection-deprecated-in-v800)戦略を非推奨とし、 [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)パラメータを使用して論理インポートモードと物理インポートモードの両方の競合検出戦略を制御できるようにします。旧バージョンの競合検出の[`duplicate-resolution`](/tidb-lightning/tidb-lightning-configuration.md)パラメータは、今後のリリースで削除されます。

## 改善点 {#improvements}

-   TiDB

    -   `SELECT ... STRAIGHT_JOIN ... USING ( ... )` ステートメントをサポートします [#54162](https://github.com/pingcap/tidb/issues/54162) @[dveeden](https://github.com/dveeden)
    -   `((idx_col_1 > 1) or (idx_col_1 = 1 and idx_col_2 > 10)) and ((idx_col_1 < 10) or (idx_col_1 = 10 and idx_col_2 < 20))`のようなフィルター条件のより正確なインデックス アクセス範囲を構築します [#54337](https://github.com/pingcap/tidb/issues/54337) @[ghazalfamilyusa](https://github.com/ghazalfamilyusa)
    -   インデックス順序を使用して、 `WHERE idx_col_1 IS NULL ORDER BY idx_col_2`のような SQL クエリの余分なソート操作を回避します [#54188](https://github.com/pingcap/tidb/issues/54188) @[ari-e](https://github.com/ari-e)
    -   `mysql.analyze_jobs`システムテーブル [#53567](https://github.com/pingcap/tidb/issues/53567) @[Rustin170506](https://github.com/Rustin170506)に分析済みインデックスを表示します。
    -   `tidb_redact_log`ステートメントの出力に`EXPLAIN`設定を適用することをサポートし、ログ処理ロジックをさらに最適化します [#54565](https://github.com/pingcap/tidb/issues/54565) @[hawkingrei](https://github.com/hawkingrei)
    -   クエリ効率を向上させるため、多値インデックスに対して`Selection` `IndexRangeScan`演算子を生成するサポート [#54876](https://github.com/pingcap/tidb/issues/54876) @[time-and-fate](https://github.com/time-and-fate)
    -   設定された時間枠外で実行されている自動タスク`ANALYZE`の強制終了をサポート [#55283](https://github.com/pingcap/tidb/issues/55283) @[hawkingrei](https://github.com/hawkingrei)
    -   統計情報が完全に TopN で構成され、対応するテーブル統計情報の変更された行数がゼロでない場合、TopN に到達しない等価条件の推定結果を 0 から 1 に調整します。 [#47400](https://github.com/pingcap/tidb/issues/47400) @[terry1purcell](https://github.com/terry1purcell)
    -   TopNオペレーターはディスクスピルをサポートします [#47733](https://github.com/pingcap/tidb/issues/47733) @[xzhangxian1008](https://github.com/xzhangxian1008)
    -   TiDB ノードは`WITH ROLLUP`修飾子と`GROUPING`関数を使用したクエリの実行をサポートしています [#42631](https://github.com/pingcap/tidb/issues/42631) @[Arenatlx](https://github.com/Arenatlx)
    -   システム変数[`tidb_low_resolution_tso`](/system-variables.md#tidb_low_resolution_tso) `GLOBAL`スコープ [#55022](https://github.com/pingcap/tidb/issues/55022) @[cfzjywxk](https://github.com/cfzjywxk)をサポートしています
    -   同時範囲削除をサポートすることで、GC（ガベージコレクション）の効率を向上させます。同時実行スレッド数は、 [`tidb_gc_concurrency`](/system-variables.md#tidb_gc_concurrency-new-in-v50) [#54570](https://github.com/pingcap/tidb/issues/54570) @[ekexium](https://github.com/ekexium)を使用して制御できます。
    -   一括DML実行モードのパフォーマンスを改善（ `tidb_dml_type = "bulk"` ） [#50215](https://github.com/pingcap/tidb/issues/50215) @[ekexium](https://github.com/ekexium)
    -   スキーマ情報キャッシュ関連インターフェースのパフォーマンスを改善`SchemaByID` [#54074](https://github.com/pingcap/tidb/issues/54074) @[ywqzzy](https://github.com/ywqzzy)
    -   スキーマ情報キャッシュが有効になっている場合、特定のシステムテーブルのクエリパフォーマンスを改善します [#50305](https://github.com/pingcap/tidb/issues/50305) @[tangenta](https://github.com/tangenta)
    -   一意インデックスを追加する際の競合キーに関するエラーメッセージを最適化 [#53004](https://github.com/pingcap/tidb/issues/53004) @[lance6716](https://github.com/lance6716)

-   PD

    -   `batch`を介して`evict-leader-scheduler`の`pd-ctl`構成を変更してリーダー退去プロセスを加速するサポート [#8265](https://github.com/tikv/pd/issues/8265) @[rleungx](https://github.com/rleungx)
    -   Grafana の**クラスタ &gt; Label 配信**パネルに`store_id`モニタリングメトリックを追加して、異なるラベルに対応するストア ID を表示します [#8337](https://github.com/tikv/pd/issues/8337) @[HuSharp](https://github.com/HuSharp)
    -   指定されたリソースグループが存在しない場合、デフォルトのリソースグループへのフォールバックをサポートする [#8388](https://github.com/tikv/pd/issues/8388) @[JmPotato](https://github.com/JmPotato)
    -   `approximate_kv_size`の`region`コマンドが出力するリージョン情報に`pd-ctl`フィールドを追加します。 [#8412](https://github.com/tikv/pd/issues/8412) @[zeminzhou](https://github.com/zeminzhou)
    -   PD APIを呼び出してTTL設定を削除したときに返されるメッセージを最適化します [#8450](https://github.com/tikv/pd/issues/8450) @[lhy1024](https://github.com/lhy1024)
    -   大規模クエリ読み取りリクエストのRU消費動作を最適化し、他のリクエストへの影響を軽減する [#8457](https://github.com/tikv/pd/issues/8457) @[nolouch](https://github.com/nolouch)
    -   PDマイクロサービスの設定ミス時に返されるエラーメッセージを最適化する [#52912](https://github.com/pingcap/tidb/issues/52912) @[rleungx](https://github.com/rleungx)
    -   PDマイクロサービスに`--name`起動パラメータを追加して、デプロイ中にサービス名をより正確に表示します [#7995](https://github.com/tikv/pd/issues/7995) @[HuSharp](https://github.com/HuSharp)
    -   領域数に基づいて`PatrolRegionScanLimit`を動的に調整してリージョンスキャン時間を短縮する機能をサポート [#7963](https://github.com/tikv/pd/issues/7963) @[lhy1024](https://github.com/lhy1024)

-   TiKV

    -   `async-io`が有効になっている場合、 Raftログの書き込みバッチ処理ポリシーを最適化して、ディスク I/O 帯域幅リソースの消費を削減します [#16907](https://github.com/tikv/tikv/issues/16907) @[LykxSassinator](https://github.com/LykxSassinator)
    -   リージョン部分購読をより適切にサポートするために、TiCDCデリゲートとダウンストリームモジュールを再設計します [#16362](https://github.com/tikv/tikv/issues/16362) @[hicqu](https://github.com/hicqu)
    -   単一のスロークエリ ログのサイズを削減 [#17294](https://github.com/tikv/tikv/issues/17294) @[Connor1996](https://github.com/Connor1996)
    -   新しいモニタリング指標を追加`min safe ts` [#17307](https://github.com/tikv/tikv/issues/17307) @[mittalrishabh](https://github.com/mittalrishabh)
    -   ピアメッセージチャネルのメモリ使用量を削減します [#16229](https://github.com/tikv/tikv/issues/16229) @[Connor1996](https://github.com/Connor1996)

-   TiFlash

    -   SVG 形式でのアドホック ヒープ プロファイリングの生成をサポート [#9320](https://github.com/pingcap/tiflash/issues/9320) @[CalvinNeo](https://github.com/CalvinNeo)

-   ツール

    -   Backup & Restore (BR)

        -   ポイントインタイムリカバリ（PITR）を初めて開始する前に、完全バックアップが存在するかどうかを確認する機能をサポートします。完全バックアップが見つからない場合、 BRはリストアを終了し、エラーを返します。[#54418](https://github.com/pingcap/tidb/issues/54418) @[Leavrth](https://github.com/Leavrth)
        -   スナップショットバックアップを復元する前に、TiKVとTiFlashのディスク容量が十分かどうかを確認する機能をサポートします。容量が不足している場合、 BRは復元を終了し、エラーを返します。[#54316](https://github.com/pingcap/tidb/issues/54316) @[RidRisR](https://github.com/RidRisR)
        -   TiKVが各SSTファイルをダウンロードする前に、TiKVのディスク容量が十分かどうかを確認する機能をサポートします。容量が不足している場合、 BRはリストアを終了し、エラーを返します。[#17224](https://github.com/tikv/tikv/issues/17224) @[RidRisR](https://github.com/RidRisR)
        -   Alibaba Cloudへのアクセス認証情報を環境変数で設定するサポート [#45551](https://github.com/pingcap/tidb/issues/45551) @[RidRisR](https://github.com/RidRisR)
        -   BR をバックアップおよびリストアに使用する際に OOM を回避するため、 BRプロセスの利用可能なメモリに基づいて環境変数`GOMEMLIMIT`を自動的に設定します [#53777](https://github.com/pingcap/tidb/issues/53777) @[Leavrth](https://github.com/Leavrth)
        -   ポイントインタイムリカバリ(PITR) と互換性のある増分バックアップを作成する [#54474](https://github.com/pingcap/tidb/issues/54474) @[3pointer](https://github.com/3pointer)
        -   `mysql.column_stats_usage`テーブル [#53567](https://github.com/pingcap/tidb/issues/53567) @[Rustin170506](https://github.com/Rustin170506)バックアップと復元をサポートします。

## バグ修正 {#bug-fixes}

-   TiDB

    -   `Open`の`PipelinedWindow`メソッドのパラメータをリセットし、 `PipelinedWindow`を`Apply`の子ノードとして使用した際に、繰り返し開閉操作によって以前のパラメータ値が再利用されることで発生する予期しないエラーを修正します。 [#53600](https://github.com/pingcap/tidb/issues/53600) @[XuHuaiyu](https://github.com/XuHuaiyu)
    -   `tidb_mem_quota_query`で設定された制限を超えるメモリ使用量のため、クエリ終了時に処理が停止する可能性がある問題を修正しました。 [#55042](https://github.com/pingcap/tidb/issues/55042) @[yibin87](https://github.com/yibin87)
    -   HashAgg演算子のディスクスピルによって並列計算中にクエリ結果が不正になる問題を修正しました [#55290](https://github.com/pingcap/tidb/issues/55290) @[xzhangxian1008](https://github.com/xzhangxian1008)
    -   `JSON_TYPE` JSON 形式にキャストした際に`YEAR`が間違って表示される問題を修正 [#54494](https://github.com/pingcap/tidb/issues/54494) @[YangKeao](https://github.com/YangKeao)
    -   `tidb_schema_cache_size`システム変数の値の範囲が間違っている問題を修正 [#54034](https://github.com/pingcap/tidb/issues/54034) @[lilinghai](https://github.com/lilinghai)
    -   パーティション式が`EXTRACT(YEAR FROM col)`の場合にパーティション剪定が機能しない問題を修正 [#54210](https://github.com/pingcap/tidb/issues/54210) @[mjonss](https://github.com/mjonss)
    -   データベースに多数のテーブルが存在する場合に`FLASHBACK DATABASE`が失敗する問題を修正 [#54415](https://github.com/pingcap/tidb/issues/54415) @[lance6716](https://github.com/lance6716)
    -   `FLASHBACK DATABASE`多数のデータベースを処理する際に無限ループに陥る問題を修正しました [#54915](https://github.com/pingcap/tidb/issues/54915) @[lance6716](https://github.com/lance6716)
    -   インデックス加速モードでインデックスを追加すると失敗する可能性がある問題を修正 [#54568](https://github.com/pingcap/tidb/issues/54568) @[lance6716](https://github.com/lance6716)
    -   `ADMIN CANCEL DDL JOBS`が原因で DDL が失敗する可能性がある問題を修正しました [#54687](https://github.com/pingcap/tidb/issues/54687) @[lance6716](https://github.com/lance6716)
    -   DMからレプリケートされたテーブルのインデックス長が`max-index-length`で指定された最大長を超えると、テーブルのレプリケーションが失敗する問題を修正します。 [#55138](https://github.com/pingcap/tidb/issues/55138) @[lance6716](https://github.com/lance6716)
    -   `runtime error: index out of range` `tidb_enable_inl_join_inner_multi_pattern`が発生する可能性がある問題を修正します [#54535](https://github.com/pingcap/tidb/issues/54535) @[joechenrh](https://github.com/joechenrh)
    -   統計情報の初期化処理中に<kbd>Control</kbd> + <kbd>C</kbd>を使用してTiDBを終了できない問題を修正しました [#54589](https://github.com/pingcap/tidb/issues/54589) @[tiancaiamao](https://github.com/tiancaiamao)
    -   `INL_MERGE_JOIN`オプティマイザー ヒントが非推奨となり、誤った結果を返す問題を修正 [#54064](https://github.com/pingcap/tidb/issues/54064) @[AilinKid](https://github.com/AilinKid)
    -   `WITH ROLLUP`を含む相関サブクエリによって TiDB がpanicを起こし、エラー`runtime error: index out of range`を返す可能性がある問題を修正しました。 [#54983](https://github.com/pingcap/tidb/issues/54983) @[AilinKid](https://github.com/AilinKid)
    -   SQLクエリのフィルタ条件に仮想列が含まれ、実行条件に`UnionScan`が含まれている場合に、述語が正しくプッシュダウンされない問題を修正します [#54870](https://github.com/pingcap/tidb/issues/54870) @[qw4990](https://github.com/qw4990)
    -   `runtime error: invalid memory address or nil pointer dereference` `tidb_enable_inl_join_inner_multi_pattern`が発生する可能性がある問題を修正しました [#55169](https://github.com/pingcap/tidb/issues/55169) @[hawkingrei](https://github.com/hawkingrei)
    -   `UNION`を含むクエリステートメントが誤った結果を返す可能性がある問題を修正しました [#52985](https://github.com/pingcap/tidb/issues/52985) @[XuHuaiyu](https://github.com/XuHuaiyu)
    -   `tot_col_size`テーブルの`mysql.stats_histograms`列が負の数になる可能性がある問題を修正しました [#55126](https://github.com/pingcap/tidb/issues/55126) @[qw4990](https://github.com/qw4990)
    -   `columnEvaluator`入力チャンク内の列参照を識別できず、SQL ステートメントの実行時に`runtime error: index out of range`が発生する問題を修正しました。 [#53713](https://github.com/pingcap/tidb/issues/53713) @[AilinKid](https://github.com/AilinKid)
    -   `STATS_EXTENDED`が予約語になる問題を修正 [#39573](https://github.com/pingcap/tidb/issues/39573) @[wddevries](https://github.com/wddevries)
    -   `tidb_low_resolution`が有効になっている場合に`select for update`が実行できてしまう問題を修正しました [#54684](https://github.com/pingcap/tidb/issues/54684) @[cfzjywxk](https://github.com/cfzjywxk)
    -   `tidb_redact_log`が有効になっている場合に、内部SQLクエリがスロークエリログに表示されない問題を修正しました [#54190](https://github.com/pingcap/tidb/issues/54190) @[lcwangchao](https://github.com/lcwangchao)
    -   トランザクションで使用されるメモリが複数回追跡される可能性がある問題を修正 [#53984](https://github.com/pingcap/tidb/issues/53984) @[ekexium](https://github.com/ekexium)
    -   `SHOW WARNINGS;`を使用して警告を取得するとpanicが発生する可能性がある問題を修正しました [#48756](https://github.com/pingcap/tidb/issues/48756) @[xhebox](https://github.com/xhebox)
    -   インデックス統計情報の読み込み時にメモリリークが発生する可能性がある問題を修正 [#54022](https://github.com/pingcap/tidb/issues/54022) @[Rustin170506](https://github.com/Rustin170506)
    -   照合順序が`LENGTH()`または`utf8_bin`の場合に { `utf8mb4_bin`条件が予期せず照合順序します [#53730](https://github.com/pingcap/tidb/issues/53730) @[elsa0520](https://github.com/elsa0520)
    -   重複する主キーに遭遇した場合に統計収集が`stats_history`テーブルを更新しない問題を修正 [#47539](https://github.com/pingcap/tidb/issues/47539) @[Defined2014](https://github.com/Defined2014)
    -   再帰的なCTEクエリによって無効なポインタが生成される可能性がある問題を修正 [#54449](https://github.com/pingcap/tidb/issues/54449) @[hawkingrei](https://github.com/hawkingrei)
    -   Grafana の接続数監視メトリックが、ハンドシェイクが完了する前に一部の接続が切断された場合に正しく表示されない問題を修正しました [#54428](https://github.com/pingcap/tidb/issues/54428) @[YangKeao](https://github.com/YangKeao)
    -   TiProxyとリソースグループを使用している際に、各リソースグループの接続数が正しく表示されない問題を修正しました [#54545](https://github.com/pingcap/tidb/issues/54545) @[YangKeao](https://github.com/YangKeao)
    -   クエリに相関のないサブクエリと`LIMIT`句が含まれている場合、列のプルーニングが不完全になり、最適ではない実行プランが生成される可能性がある問題を修正しました。 [#54213](https://github.com/pingcap/tidb/issues/54213) @[qw4990](https://github.com/qw4990)
    -   `SELECT ... FOR UPDATE`の誤ったPointGetプランを再利用してしまう問題を修正します [#54652](https://github.com/pingcap/tidb/issues/54652) @[qw4990](https://github.com/qw4990)
    -   `TIMESTAMPADD()`関数の最初の引数が`month`で、2 番目の引数が負の値の場合に無限ループに陥る問題を修正しました。 [#54908](https://github.com/pingcap/tidb/issues/54908) @[xzhangxian1008](https://github.com/xzhangxian1008)
    -   スローログ内の内部SQLステートメントがデフォルトでnullに編集される問題を修正[#54190](https://github.com/pingcap/tidb/issues/54190) [#52743](https://github.com/pingcap/tidb/issues/52743) [#53264](https://github.com/pingcap/tidb/issues/53264) @[lcwangchao](https://github.com/lcwangchao)
    -   `PointGet`の実行プランが`_tidb_rowid`に対して生成されてしまう問題を修正します [#54583](https://github.com/pingcap/tidb/issues/54583) @[Defined2014](https://github.com/Defined2014)
    -   `SHOW IMPORT JOBS`が v7.1 からアップグレード後にエラー`Unknown column 'summary'`を報告する問題を修正 [#54241](https://github.com/pingcap/tidb/issues/54241) @[tangenta](https://github.com/tangenta)
    -   ビュー定義で列定義としてサブクエリが使用されている場合、 `information_schema.columns`を使用して列情報を取得すると警告 1356 が返される問題を修正しました [#54343](https://github.com/pingcap/tidb/issues/54343) @[lance6716](https://github.com/lance6716)
    -   厳密に自己インクリメントではないRANGEパーティションテーブルが作成できてしまう問題を修正 [#54829](https://github.com/pingcap/tidb/issues/54829) @[Defined2014](https://github.com/Defined2014)
    -   SQLが異常中断されたときに`INDEX_HASH_JOIN`正常に終了できない問題を修正 [#54688](https://github.com/pingcap/tidb/issues/54688) @[wshwsh12](https://github.com/wshwsh12)
    -   分散実行フレームワーク（DXF）を使用してインデックスを追加する際のネットワーク分断により、データインデックスに不整合が生じる可能性がある問題を修正しました [#54897](https://github.com/pingcap/tidb/issues/54897) @[tangenta](https://github.com/tangenta)

-   PD

    -   リソースグループにロールをバインドする際にエラーが報告されない問題を修正 [#54417](https://github.com/pingcap/tidb/issues/54417) @[JmPotato](https://github.com/JmPotato)
    -   リソースグループが500ミリ秒以上トークンを要求するとクォータ制限に遭遇する問題を修正 [#8349](https://github.com/tikv/pd/issues/8349) @[nolouch](https://github.com/nolouch)
    -   `INFORMATION_SCHEMA.RUNAWAY_WATCHES`テーブル内の時間データ型が正しくない問題を修正 [#54770](https://github.com/pingcap/tidb/issues/54770) @[HuSharp](https://github.com/HuSharp)
    -   リソースグループが高同時実行時にリソース使用量を効果的に制限できない問題を修正 [#8435](https://github.com/tikv/pd/issues/8435) @[nolouch](https://github.com/nolouch)
    -   テーブル属性を取得する際に誤ったPD APIが呼び出される問題を修正 [#55188](https://github.com/pingcap/tidb/issues/55188) @[JmPotato](https://github.com/JmPotato)
    -   `scheduling`マイクロサービスが有効になった後にスケーリングの進行状況が正しく表示されない問題を修正しました [#8331](https://github.com/tikv/pd/issues/8331) @[rleungx](https://github.com/rleungx)
    -   暗号化マネージャが使用前に初期化されていない問題を修正 [#8384](https://github.com/tikv/pd/issues/8384) @[rleungx](https://github.com/rleungx)
    -   一部のログが編集されない問題を修正 [#8419](https://github.com/tikv/pd/issues/8419) @[rleungx](https://github.com/rleungx)
    -   PDマイクロサービスの起動中にリダイレクトがpanic可能性がある問題を修正 [#8406](https://github.com/tikv/pd/issues/8406) @[HuSharp](https://github.com/HuSharp)
    -   `split-merge-interval`設定項目の値が繰り返し変更された場合（例えば、 `1s`から`1h` に変更し、再び`1s` に戻す場合など）に、その設定が有効にならない可能性がある問題を修正します。 [#8404](https://github.com/tikv/pd/issues/8404) @[lhy1024](https://github.com/lhy1024)
    -   `replication.strictly-match-label`を`true`に設定するとTiFlash が起動に失敗する問題を修正しました [#8480](https://github.com/tikv/pd/issues/8480) @[rleungx](https://github.com/rleungx)
    -   大規模なパーティションテーブルを分析する際にTSOの取得が遅くなり、 `ANALYZE`パフォーマンス低下を引き起こす問題を修正しました [#8500](https://github.com/tikv/pd/issues/8500) @[rleungx](https://github.com/rleungx)
    -   大規模クラスターにおける潜在的なデータ競合を修正 [#8386](https://github.com/tikv/pd/issues/8386) @[rleungx](https://github.com/rleungx)
    -   クエリが暴走クエリかどうかを判断する際に、TiDB がコプロセッサー側で費やされた時間消費のみをカウントし、TiDB 側で費やされた時間消費がカウントされないため、一部のクエリが暴走クエリとして識別されない問題を修正します。 [#51325](https://github.com/pingcap/tidb/issues/51325) @[HuSharp](https://github.com/HuSharp)

-   TiFlash

    -   `CAST()`関数を使用して文字列をタイムゾーンまたは無効な文字を含む datetime に変換すると、結果が正しくない問題を修正しました [#8754](https://github.com/pingcap/tiflash/issues/8754) @[solotzg](https://github.com/solotzg)
    -   データベース全体に空のパーティションがあるパーティションテーブルで`RENAME TABLE ... TO ...`実行するとTiFlash がpanicになる問題を修正 [#9132](https://github.com/pingcap/tiflash/issues/9132) @[JaySon-Huang](https://github.com/JaySon-Huang)
    -   遅延マテリアライゼーションが有効になった後、一部のクエリで列型の不一致エラーが報告される可能性がある問題を修正 [#9175](https://github.com/pingcap/tiflash/issues/9175) @[JinheLin](https://github.com/JinheLin)
    -   仮想生成列を含むクエリが遅延マテリアライゼーション有効後に誤った結果を返す可能性がある問題を修正 [#9188](https://github.com/pingcap/tiflash/issues/9188) @[JinheLin](https://github.com/JinheLin)
    -   TiFlashでSSL証明書の設定を空文字列に設定するとTLSが誤って有効になり、 TiFlashが起動に失敗する問題を修正しました [#9235](https://github.com/pingcap/tiflash/issues/9235) @[JaySon-Huang](https://github.com/JaySon-Huang)
    -   データベース作成直後にデータベースが削除されるとTiFlash がpanicことがある問題を修正 [#9266](https://github.com/pingcap/tiflash/issues/9266) @[JaySon-Huang](https://github.com/JaySon-Huang)
    -   TiFlashと任意の PD 間のネットワーク パーティション (ネットワークの切断) により、読み取りリクエストのタイムアウト エラーが発生する可能性がある問題を修正 [#9243](https://github.com/pingcap/tiflash/issues/9243) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    -   分散ストレージおよびコンピューティングアーキテクチャでTiFlash書き込みノードの再起動に失敗することがある問題を修正 [#9282](https://github.com/pingcap/tiflash/issues/9282) @[JaySon-Huang](https://github.com/JaySon-Huang)
    -   分散ストレージおよびコンピューティングアーキテクチャにおいて、 TiFlash書き込みノードの読み取りスナップショットがタイムリーに解放されない問題を修正します [#9298](https://github.com/pingcap/tiflash/issues/9298) @[JinheLin](https://github.com/JinheLin)

-   TiKV

    -   古いリージョンをクリーンアップすると、誤って有効なデータが削除される可能性がある問題を修正 [#17258](https://github.com/tikv/tikv/issues/17258) @[hbisheng](https://github.com/hbisheng)
    -   Grafana の TiKV ダッシュボードで`Ingestion picked level`と`Compaction Job Size(files)`が正しく表示されない問題を修正します [#15990](https://github.com/tikv/tikv/issues/15990) @[Connor1996](https://github.com/Connor1996)
    -   `cancel_generating_snap`が`snap_tried_cnt`を誤って更新すると TiKV がpanicを起こす問題を修正 [#17226](https://github.com/tikv/tikv/issues/17226) @[hbisheng](https://github.com/hbisheng)
    -   `Ingest SST duration seconds`の情報が間違っている問題を修正しました [#17239](https://github.com/tikv/tikv/issues/17239) @[LykxSassinator](https://github.com/LykxSassinator)
    -   エラー発生時にCPUプロファイリングフラグが正しくリセットされない問題を修正 [#17234](https://github.com/tikv/tikv/issues/17234) @[Connor1996](https://github.com/Connor1996)
    -   ブルームフィルターが以前のバージョン（v7.1より前）と以降のバージョン間で互換性がない問題を修正しました [#17272](https://github.com/tikv/tikv/issues/17272) @[v01dstar](https://github.com/v01dstar)

-   ツール

    -   Backup & Restore (BR)

        -   `ADD INDEX`や`MODIFY COLUMN`など、バックフィルが必要な DDL が増分リストア中に正しく復元されない可能性がある問題を修正します [#54426](https://github.com/pingcap/tidb/issues/54426) @[3pointer](https://github.com/3pointer)
        -   バックアップと復元中に進行状況が停止する問題を修正 [#54140](https://github.com/pingcap/tidb/issues/54140) @[Leavrth](https://github.com/Leavrth)
        -   バックアップとリストアのチェックポイントパスが一部の外部ストレージと互換性がない問題を修正 [#55265](https://github.com/pingcap/tidb/issues/55265) @[Leavrth](https://github.com/Leavrth)

    -   TiCDC

        -   下流の Kafka にアクセスできない場合にプロセッサが停止する可能性がある問題を修正しました [#11340](https://github.com/pingcap/tiflow/issues/11340) @[asddongmen](https://github.com/asddongmen)

    -   TiDB Data Migration (DM)

        -   スキーマトラッカーがLISTパーティションテーブルを正しく処理せず、DMエラーが発生する問題を修正しました [#11408](https://github.com/pingcap/tiflow/issues/11408) @[lance6716](https://github.com/lance6716)
        -   インデックスの長さが`max-index-length`のデフォルト値を超えるとデータレプリケーションが中断される問題を修正します [#11459](https://github.com/pingcap/tiflow/issues/11459) @[michaelmdeng](https://github.com/michaelmdeng)
        -   DMが`FAKE_ROTATE_EVENT`を正しく処理できない問題を修正 [#11381](https://github.com/pingcap/tiflow/issues/11381) @[lance6716](https://github.com/lance6716)

    -   TiDB Lightning

        -   TiDB Lightningがキースペース名の取得に失敗した際に、紛らわしい`WARN`ログを出力する問題を修正 [#54232](https://github.com/pingcap/tidb/issues/54232) @[kennytm](https://github.com/kennytm)
        -   TiDB Lightningの TLS 構成がクラスター証明書に影響する問題を修正 [#54172](https://github.com/pingcap/tidb/issues/54172) @[ei-sugimoto](https://github.com/ei-sugimoto)
        -   TiDB Lightningを使用したデータインポート中にトランザクションの競合が発生する問題を修正しました [#49826](https://github.com/pingcap/tidb/issues/49826) @[lance6716](https://github.com/lance6716)
        -   多数のデータベースとテーブルのインポート中に、大きなチェックポイントファイルがパフォーマンス低下を引き起こす問題を修正 [#55054](https://github.com/pingcap/tidb/issues/55054) @[D3Hunter](https://github.com/D3Hunter)

## 貢献者 {#contributors}

TiDBコミュニティの以下の貢献者の皆様に感謝申し上げます。

-   [ari-e](https://github.com/ari-e)
-   [ei-sugimoto](https://github.com/ei-sugimoto)
-   [HaoW30](https://github.com/HaoW30)
-   [JackL9u](https://github.com/JackL9u)
-   [michaelmdeng](https://github.com/michaelmdeng)
-   [mittalrishabh](https://github.com/mittalrishabh)
-   [qingfeng777](https://github.com/qingfeng777)
-   [SandeepPadhi](https://github.com/SandeepPadhi)
-   [yzhan1](https://github.com/yzhan1)
