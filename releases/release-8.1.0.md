---
title: TiDB 8.1.0 Release Notes
summary: TiDB 8.1.0 の新機能、互換性の変更、改善、バグ修正について説明します。
---

# TiDB 8.1.0 リリースノート {#tidb-8-1-0-release-notes}

<EmailSubscriptionWrapper />

発売日: 2024年5月24日

TiDB バージョン: 8.1.0

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v8.1/quick-start-with-tidb) | [実稼働環境への導入](https://docs.pingcap.com/tidb/v8.1/production-deployment-using-tiup)

TiDB 8.1.0 は長期サポートリリース (LTS) です。

以前の LTS 7.5.0 と比較して、8.1.0 には[7.6.0-DMR](/releases/release-7.6.0.md)および[8.0.0-DMR](/releases/release-8.0.0.md)でリリースされた新機能、改善、バグ修正が含まれています。7.5.x から 8.1.0 にアップグレードする場合、 [TiDB リリースノート PDF](https://download.pingcap.org/tidb-v7.6-to-v8.1-en-release-notes.pdf)ダウンロードして、2 つの LTS バージョン間のすべてのリリース ノートを表示できます。次の表に、7.6.0 から 8.1.0 への主な変更点を示します。

<table><thead><tr><th>カテゴリ</th><th>機能/拡張機能</th><th>説明</th></tr></thead><tbody><tr><td rowspan="5">スケーラビリティとパフォーマンス</td><td><a href="https://docs.pingcap.com/tidb/v8.1/br-snapshot-guide#restore-cluster-snapshots">クラスター スナップショットの復元速度の高速化</a>(v8.0.0 で GA)</td><td>この機能により、 BR はクラスターのスケールの利点を最大限に活用し、クラスター内のすべての TiKV ノードがデータ復元の準備ステップに参加できるようになります。この機能により、大規模クラスター内の大規模データセットの復元速度が大幅に向上します。実際のテストでは、この機能によりダウンロード帯域幅が飽和し、ダウンロード速度が 8 ～ 10 倍、エンドツーエンドの復元速度が約 1.5 ～ 3 倍向上することが示されています。</td></tr><tr><td><a href="https://docs.pingcap.com/tidb/v8.1/accelerated-table-creation">バッチでテーブルを作成する場合、最大 10 倍の速度を実現します</a>(実験的、v7.6.0 で導入)</td><td> v7.6.0 で新しい DDLアーキテクチャが実装されたことで、バッチ テーブル作成のパフォーマンスが最大 10 倍高速化し、大幅に向上しました。この大幅な機能強化により、多数のテーブルの作成に必要な時間が大幅に短縮されます。この高速化は、数万から数十万に及ぶ大量のテーブルが一般的に存在する SaaS シナリオで特に顕著です。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v8.1/tune-region-performance#use-the-active-pd-follower-feature-to-enhance-the-scalability-of-pds-region-information-query-service">アクティブ PD フォロワーを使用して PD のリージョン情報クエリ サービスを強化します</a>(実験的、v7.6.0 で導入)</td><td> TiDB v7.6.0 では、PD フォロワーがリージョン情報クエリ サービスを提供できるようにする実験的機能「Active PD Follower 」が導入されています。この機能により、多数の TiDB ノードとリージョンを持つクラスターで<code>GetRegion</code>および<code>ScanRegions</code>要求を処理する PD クラスターの機能が向上し、PD リーダーの CPU 負荷が軽減されます。</td></tr><tr><td><a href="https://docs.pingcap.com/tidb/v8.1/system-variables#tidb_dml_type-new-in-v800">より大規模なトランザクションのためのバルク DML</a> (実験的、v8.0.0 で導入)</td><td>大規模なクリーンアップ ジョブ、結合、集計などの大規模なバッチ DML ジョブは、大量のメモリを消費する可能性があり、これまでは非常に大規模な規模で制限されていました。バルク DML ( <code>tidb_dml_type = &quot;bulk&quot;</code> ) は、トランザクション保証を提供し、OOM の問題を軽減しながら、大規模なバッチ DML タスクをより効率的に処理するための新しい DML タイプです。この機能は、データのロードに使用する場合、インポート、ロード、および復元操作とは異なります。</td></tr><tr><td>テーブル数が膨大である場合のスキーマ情報のキャッシュの安定性を向上 (実験的、v8.0.0 で導入)</td><td>マルチテナント アプリケーションの記録システムとして TiDB を使用している SaaS 企業は、多くの場合、相当数のテーブルを保存する必要があります。以前のバージョンでは、100 万以上のテーブル数を処理することは可能でしたが、全体的なユーザー エクスペリエンスが低下する可能性がありました。TiDB v8.0.0 では、 <code>auto analyze</code>用の<a href="https://docs.pingcap.com/tidb/v8.1/system-variables#tidb_enable_auto_analyze_priority_queue-new-in-v800">優先キューを</a>実装することで状況が改善され、プロセスの柔軟性が高まり、より広範なテーブルにわたって安定性が向上しています。</td></tr><tr><td rowspan="5">信頼性と可用性</td><td><a href="https://docs.pingcap.com/tidb/v8.1/tidb-global-sort">グローバル ソート</a>(v8.0.0 で GA)</td><td>グローバル ソート機能は、 <code>IMPORT INTO</code>および<code>CREATE INDEX</code>の安定性と効率性を向上させることを目的としています。処理するデータをグローバルにソートすることで、この機能は TiKV へのデータ書き込みの安定性、制御性、およびスケーラビリティを向上させ、結果としてデータのインポートとインデックス作成のユーザー エクスペリエンスとサービス品質を高めます。グローバル ソートを有効にすると、各<code>IMPORT INTO</code>または<code>CREATE INDEX</code>ステートメントは、最大 40 TiB のデータのインポートまたはインデックスの追加をサポートするようになりました。</td></tr><tr><td><a href="https://docs.pingcap.com/tidb/v8.1/sql-plan-management#cross-database-binding">クロスデータベース SQL バインディング</a>(v7.6.0 で導入)</td><td>同じスキーマを持つ数百のデータベースを管理する場合、これらのデータベース全体に SQL バインディングを適用する必要があることがよくあります。たとえば、SaaS または PaaS データ プラットフォームでは、各ユーザーは通常、同じスキーマを持つ個別のデータベースを操作し、それらに対して同様の SQL クエリを実行します。この場合、各データベースに SQL を 1 つずつバインドするのは現実的ではありません。TiDB v7.6.0 では、すべてのスキーマが同等のデータベース間でバインディングを一致させることができるデータベース間 SQL バインディングが導入されています。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v8.1/tiproxy-overview">TiProxy をサポート</a>(v8.0.0 で GA)</td><td>デプロイメント ツールを使用して簡単にデプロイできる TiProxy サービスを完全にサポートし、ローリング再起動、アップグレード、またはスケーリング イベントを通じて TiDB への接続を管理および維持します。</td></tr><tr><td><a href="https://docs.pingcap.com/tidb/v8.1/dm-compatibility-catalog">データ移行 (DM) は MySQL 8.0 (v7.6.0 で GA) を正式にサポートします</a></td><td>これまで、DM を使用して MySQL 8.0 からデータを移行することは実験的機能であり、実本番環境では使用できませんでした。TiDB v7.6.0 では、この機能の安定性と互換性が強化され、実本番環境で MySQL 8.0 から TiDB にデータをスムーズかつ迅速に移行できるようになります。v7.6.0 では、この機能が一般提供 (GA) されます。</td></tr><tr><td> TiDB リソース制御は<a href="https://docs.pingcap.com/tidb/v8.1/tidb-resource-control#manage-queries-that-consume-more-resources-than-expected-runaway-queries">、予想よりも多くのリソースを消費するクエリの管理</a>をサポートします (v8.1.0 で GA)</td><td> TiDB は、リソース グループのルールを通じて、予想よりも多くのリソースを消費するクエリを自動的に識別し、これらのクエリを制限またはキャンセルできます。ルールによってクエリが識別されない場合でも、クエリ特性を手動で追加し、対応する対策を講じて、突然のクエリ パフォーマンスの問題がデータベース全体に与える影響を軽減できます。</td></tr><tr><td rowspan="1"> DB 操作と可観測性</td><td>インデックス使用統計の監視をサポート (v8.0.0 で導入)</td><td>適切なインデックス設計は、データベースのパフォーマンスを維持するための重要な前提条件です。TiDB v8.0.0 では、インデックスの使用統計を提供する<a href="https://docs.pingcap.com/tidb/v8.1/information-schema-tidb-index-usage"><code>INFORMATION_SCHEMA.TIDB_INDEX_USAGE</code></a>テーブルと<a href="https://docs.pingcap.com/tidb/v8.1/sys-schema-unused-indexes"><code>sys.schema_unused_indexes</code></a>ビューが導入されています。この機能は、データベース内のインデックスの効率を評価し、インデックス設計を最適化するのに役立ちます。</td></tr><tr><td rowspan="3">データ移行</td><td>TiCDC は<a href="https://docs.pingcap.com/tidb/v8.1/ticdc-simple-protocol">シンプル プロトコル</a>(v8.0.0 で導入) をサポートしています。</td><td> TiCDC では、新しいプロトコルである Simple プロトコルが導入されています。このプロトコルは、DDL および BOOTSTRAP イベントにテーブル スキーマ情報を埋め込むことで、インバンド スキーマ追跡機能を提供します。</td></tr><tr><td> TiCDC は<a href="https://docs.pingcap.com/tidb/v8.1/ticdc-debezium">Debezium 形式プロトコル</a>(v8.0.0 で導入) をサポートしています。</td><td> TiCDC は、新しいプロトコルである Debezium プロトコルを導入しました。TiCDC は、Debezium スタイルのメッセージを生成するプロトコルを使用して、データ変更イベントを Kafka シンクに公開できるようになりました。</td></tr><tr><td> TiCDC は<a href="https://docs.pingcap.com/tidb/v8.1/ticdc-client-authentication">クライアント認証</a>をサポートしています (v8.1.0 で導入)</td><td> TiCDC は、相互トランスポート層Security(mTLS) または TiDB ユーザー名とパスワードを使用したクライアント認証をサポートしています。この機能により、CLI または OpenAPI クライアントは TiCDC への接続を認証できます。</td></tr></tbody></table>

## 機能の詳細 {#feature-details}

### 信頼性 {#reliability}

-   予想よりも多くのリソースを消費するクエリの管理をサポート (GA) [＃43691](https://github.com/pingcap/tidb/issues/43691) @ [ノルーシュ](https://github.com/nolouch)

    突然の SQL クエリ パフォーマンスの問題は、データベース全体のパフォーマンスの低下を引き起こす可能性があり、これはデータベースの安定性に対する最も一般的な課題です。これらの問題の原因は、テストされていない新しい SQL ステートメント、データ量の大幅な変更、実行プランの突然の変更など、多岐にわたります。これらの問題をソースで完全に回避することは困難です。TiDB v7.2.0 では、予想よりも多くのリソースを消費するクエリを管理して、突然のクエリ パフォーマンスの問題の影響を迅速に軽減する機能が導入されました。この機能は、v8.1.0 で一般提供されます。

    リソース グループ内のクエリの最大実行時間を設定できます。クエリの実行時間が設定値を超えると、クエリの優先度が自動的に下げられるか、クエリがキャンセルされます。また、問題のあるクエリの同時実行が高すぎる場合に識別フェーズで過剰なリソース消費を回避するために、一定期間内にテキストまたは実行プランを通じて特定されたクエリにすぐに一致するように設定することもできます。

    TiDB は、クエリの手動マークもサポートしています。1 コマンドを使用すると、SQL テキスト、SQL ダイジェスト、または実行プランに基づいてクエリをマークできます。マークに一致するクエリ[`QUERY WATCH`](/sql-statements/sql-statement-query-watch.md)ダウングレードまたはキャンセルでき、SQL ブロックリストを追加する目的を達成できます。

    予想よりも多くのリソースを消費するクエリの自動管理機能により、根本原因が特定される前にクエリの問題が全体的なパフォーマンスに与える影響を迅速に軽減する効果的な手段がユーザーに提供され、データベースの安定性が向上します。

    詳細については[ドキュメント](/tidb-resource-control.md#manage-queries-that-consume-more-resources-than-expected-runaway-queries)参照してください。

### 構文 {#sql}

-   テーブル作成時にデフォルトの列値を設定する式をさらにサポート (GA) [＃50936](https://github.com/pingcap/tidb/issues/50936) @ [ジムララ](https://github.com/zimulala)

    v8.0.0 より前では、テーブルを作成するときに、列のデフォルト値は文字列、数値、日付、および特定の式に制限されていました。v8.0.0 以降では、デフォルトの列値としてさらに多くの式を使用できます。たとえば、列のデフォルト値を`DATE_FORMAT`に設定できます。この機能により、より多様な要件を満たすことができます。v8.1.0 では、この機能が GA になります。

    v8.1.0 以降では、列を`ADD COLUMN`ずつ追加するときに、式をデフォルト値として使用できます。

    詳細については[ドキュメント](/data-type-default-values.md#specify-expressions-as-default-values)参照してください。

### DB操作 {#db-operations}

-   デフォルトで TiDB 分散実行フレームワーク (DXF) を有効にして、 `ADD INDEX`または`IMPORT INTO`タスクの並列実行のパフォーマンスと安定性を向上させます[＃52441](https://github.com/pingcap/tidb/issues/52441) @ [D3ハンター](https://github.com/D3Hunter)

    DXF は v7.5.0 で一般提供 (GA) されますが、デフォルトでは無効になっています。つまり、 `ADD INDEX`または`IMPORT INTO`タスクは、デフォルトでは 1 つの TiDB ノードによってのみ実行されます。

    v8.1.0 以降、TiDB はデフォルトでこの機能を有効にします ( [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710)デフォルトは`ON`です)。有効にすると、DXF は複数の TiDB ノードをスケジュールして、同じ`ADD INDEX`または`IMPORT INTO`タスクを並行して実行し、TiDB クラスターのリソースを最大限に活用して、これらのタスクのパフォーマンスを大幅に向上させることができます。さらに、TiDB ノードを追加し、新しく追加されたノードに[`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740)構成することで、 `ADD INDEX`および`IMPORT INTO`タスクのパフォーマンスを直線的に向上させることができます。

    詳細については[ドキュメント](/tidb-distributed-execution-framework.md)参照してください。

### Security {#security}

-   TiDB ログ感度低下 (GA) [＃52364](https://github.com/pingcap/tidb/issues/52364) @ [xhebox](https://github.com/xhebox)を強化

    強化された TiDB ログの非感度化は、ログ ファイル内の SQL テキスト情報をマークすることによって実装され、ユーザーがログを表示するときに機密データを削除することをサポートします。ログ情報をマークするかどうかを制御して、さまざまなシナリオで TiDB ログを安全に使用できるようにすることで、ログの非感度化を使用する際のセキュリティと柔軟性が向上します。この機能を使用するには、システム変数`tidb_redact_log`を`MARKER`に設定すると、TiDB のランタイム ログ内の SQL テキストがマークされます。さらに、TiDBサーバーで`collect-log`サブコマンドを使用して、マークされた機密データをログから削除し、ログを安全な方法で表示できます。すべてのマーカーを削除して通常のログを取得することもできます。この機能は、v8.1.0 で一般提供されました。

    詳細については[ドキュメント](/system-variables.md#tidb_redact_log)参照してください。

### データ移行 {#data-migration}

-   `IMPORT INTO ... FROM SELECT`構文（GA） [＃49883](https://github.com/pingcap/tidb/issues/49883) @ [D3ハンター](https://github.com/D3Hunter)をサポート

    v8.0.0 より前では、クエリ結果をターゲット テーブルにインポートするには`INSERT INTO ... SELECT`ステートメントを使用するしかなく、大規模なデータセットのシナリオによっては効率が悪かったです。v8.0.0 では、TiDB は`IMPORT INTO ... FROM SELECT`実験的機能として導入し、 `SELECT`クエリの結果を空の TiDB ターゲット テーブルにインポートできるようになりました。これにより、 `INSERT INTO ... SELECT`の最大 8 倍のパフォーマンスが実現され、インポート時間が大幅に短縮されます。さらに、 `IMPORT INTO ... FROM SELECT`使用して、 [`AS OF TIMESTAMP`](/as-of-timestamp.md)でクエリされた履歴データをインポートできます。

    v8.1.0 では、 `IMPORT INTO ... FROM SELECT`構文が一般提供 (GA) され、 `IMPORT INTO`ステートメントの機能シナリオが強化されます。

    詳細については[ドキュメント](/sql-statements/sql-statement-import-into.md)参照してください。

-   TiDB Lightningは競合解決戦略を簡素化し、 `replace`戦略（GA） [＃51036](https://github.com/pingcap/tidb/issues/51036) @ [翻訳者](https://github.com/lyzx2001)を使用して競合するデータの処理をサポートします。

    v8.0.0 より前のTiDB Lightningには、論理インポート モードが[1つのデータ競合解決戦略](/tidb-lightning/tidb-lightning-logical-import-mode-usage.md#conflict-detection) 、物理インポート モードが[2つのデータ競合解決戦略](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#conflict-detection)あり、理解して構成するのは簡単ではありません。

    v8.0.0 では、 TiDB Lightning は物理インポート モードの[競合検出の旧バージョン](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#the-old-version-of-conflict-detection-deprecated-in-v800)戦略を非推奨にし、 [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md)パラメータ (実験的) を介して論理インポート モードと物理インポート モードの両方の競合検出戦略を制御できるようにし、このパラメータの構成を簡素化しました。さらに、物理インポート モードでは、インポート時に主キーまたは一意キーの競合のあるデータが検出された場合に、 `replace`戦略で最新のデータを保持し、古いデータを上書きすることがサポートされます。v8.1.0 では、 `replace`戦略で競合するデータを処理する機能が一般提供 (GA) されます。

    詳細については[ドキュメント](/tidb-lightning/tidb-lightning-configuration.md)参照してください。

-   TiCDCはクライアント認証[＃10636](https://github.com/pingcap/tiflow/issues/10636) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)をサポートします

    v8.1.0 では、TiCDC は、TiCDC CLI または OpenAPI を使用しているときにクライアント認証をサポートします。この機能により、クライアント証明書を使用したクライアント認証を要求するように TiCDC を構成し、相互トランスポート層Security(mTLS) を確立できます。さらに、TiDB のユーザー名とパスワードに基づいて認証を構成することもできます。

    詳細については[ドキュメント](/ticdc/ticdc-client-authentication.md)参照してください。

## 互換性の変更 {#compatibility-changes}

> **注記：**
>
> このセクションでは、v8.0.0 から現在のバージョン (v8.1.0) にアップグレードするときに知っておく必要のある互換性の変更について説明します。v7.6.0 以前のバージョンから現在のバージョンにアップグレードする場合は、中間バージョンで導入された互換性の変更も確認する必要がある可能性があります。

### 行動の変化 {#behavior-changes}

-   以前のバージョンでは、 TiDB Lightningの`tidb.tls`構成項目は、値`"false"`と`""`同様に扱い、値`"preferred"`と`"skip-verify"`同様に扱いました。 v8.1.0 以降、 TiDB Lightning は`tidb.tls`に対して`"false"` 、 `""` 、 `"skip-verify"` 、および`"preferred"`の動作を区別します。 詳細については、 [TiDB Lightning構成](/tidb-lightning/tidb-lightning-configuration.md)参照してください。
-   `AUTO_ID_CACHE=1`のテーブルの場合、TiDB は[集中型自動増分ID割り当てサービス](/auto-increment.md#mysql-compatibility-mode)サポートします。以前のバージョンでは、このサービスのプライマリ TiDB ノードは、TiDB プロセスが終了すると (たとえば、TiDB ノードの再起動中)、自動的に`forceRebase`操作を実行して、自動割り当て ID が可能な限り連続した状態を維持していました。ただし、 `AUTO_ID_CACHE=1`のテーブルが多すぎると、 `forceRebase`の実行に非常に時間がかかり、TiDB がすぐに再起動できなくなり、データの書き込みがブロックされて、システムの可用性に影響します。この問題を解決するために、v8.1.0 以降、TiDB は`forceRebase`動作を削除しますが、この変更により、フェイルオーバー中に一部の自動割り当て ID が連続しなくなります。
-   以前のバージョンでは、 `UPDATE`変更を含むトランザクションを処理するときに、主キーまたは null 以外の一意のインデックス値が`UPDATE`イベントで変更されると、TiCDC はこのイベントを`DELETE`のイベントと`INSERT`イベントに分割しました。v8.1.0 では、MySQL シンクを使用する場合、 `UPDATE`変更のトランザクション`commitTS`が TiCDC `thresholdTS` (TiCDC の起動時に PD から取得する現在のタイムスタンプ) より小さい場合、TiCDC は`UPDATE`イベントを`DELETE`と`INSERT`のイベントに分割します。この動作変更は、TiCDC が受信した`UPDATE`イベントの順序が間違っている可能性があり、分割された`DELETE`と`INSERT`イベントの順序が間違っている可能性があることによって発生するダウンストリーム データの不整合の問題に対処します。詳細については、 [ドキュメント](/ticdc/ticdc-split-update-behavior.md#split-update-events-for-mysql-sinks)参照してください。

### システム変数 {#system-variables}

| 変数名                                                                                                      | タイプを変更 | 説明                                                                                                                                                                                                                                                                                                                                                                     |
| -------------------------------------------------------------------------------------------------------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`tidb_enable_telemetry`](/system-variables.md#tidb_enable_telemetry-new-in-v402-and-deprecated-in-v810) | 非推奨    | v8.1.0 以降では、TiDB のテレメトリ機能が削除され、この変数は機能しなくなりました。これは、以前のバージョンとの互換性のためだけに保持されています。                                                                                                                                                                                                                                                                                        |
| [`tidb_auto_analyze_ratio`](/system-variables.md#tidb_auto_analyze_ratio)                                | 修正済み   | 値の範囲を`[0, 18446744073709551615]`から`(0, 1]`に変更します。                                                                                                                                                                                                                                                                                                                      |
| [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710)                        | 修正済み   | デフォルト値を`OFF`から`ON`に変更します。これは、Distributed eXecution Framework (DXF) がデフォルトで有効になっていることを意味します。これにより、TiDB クラスターのリソースが十分に活用され、 `ADD INDEX`および`IMPORT INTO`タスクのパフォーマンスが大幅に向上します。DXF が有効になっているクラスターを v8.1.0 以降にアップグレードする場合は、アップグレード前に DXF を無効にします ( `tidb_enable_dist_task`を`OFF`に設定)。これにより、アップグレード中に`ADD INDEX`操作が行われてデータ インデックスの不整合が発生するのを回避できます。アップグレード後に、DXF を手動で有効にできます。 |
| [`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740)                              | 修正済み   | オプションの値を`""`または`background`から最大 64 文字の文字列に変更します。これにより、各 TiDB ノードのサービス スコープをより柔軟に制御できます。有効な文字は、数字`0-9` 、文字`a-zA-Z` 、アンダースコア`_` 、ハイフン`-`です。Distributed eXecution Framework (DXF) は、この変数の値に基づいて、どの TiDB ノードが分散タスクを実行するようにスケジュールできるかを決定します。具体的なルールについては、 [タスクのスケジュール](/tidb-distributed-execution-framework.md#task-scheduling)参照してください。                                   |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーションパラメータ                                                                                            | タイプを変更   | 説明                                                                                                                                                                                                |
| -------------- | ---------------------------------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ティビ            | [`enable-telemetry`](/tidb-configuration-file.md#enable-telemetry-new-in-v402-and-deprecated-in-v810)      | 非推奨      | v8.1.0 以降では、TiDB のテレメトリ機能が削除され、この構成項目は機能しなくなりました。これは、以前のバージョンとの互換性のためだけに保持されています。                                                                                                                 |
| ティビ            | [`concurrently-init-stats`](/tidb-configuration-file.md#concurrently-init-stats-new-in-v810-and-v752)      | 新しく追加された | TiDB の起動時に統計を同時に初期化するかどうかを制御します。デフォルト値は`false`です。                                                                                                                                                 |
| PD             | [`enable-telemetry`](/pd-configuration-file.md#enable-telemetry)                                           | 非推奨      | v8.1.0 以降では、TiDB ダッシュボードのテレメトリ機能が削除され、この構成項目は機能しなくなりました。これは、以前のバージョンとの互換性のためだけに保持されています。                                                                                                          |
| TiDB Lightning | [`conflict.max-record-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-configuration) | 修正済み     | v8.1.0 以降では、ユーザー入力に関係なく、 TiDB Lightning が`conflict.max-record-rows`の値に`conflict.threshold`の値を自動的に割り当てるため、 `conflict.max-record-rows`手動で構成する必要はありません。 `conflict.max-record-rows`将来のリリースで廃止される予定です。 |
| TiDB Lightning | [`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)                | 修正済み     | デフォルト値を`9223372036854775807`から`10000`に変更して、異常なタスクを迅速に中断し、対応する調整をできるだけ早く行えるようにします。これにより、異常なデータ ソースや不正なテーブル スキーマ定義が原因で、インポート後に大量の競合データが発見されるシナリオを回避し、時間と計算リソースを節約できます。                              |
| ティCDC          | [`security.client-allowed-user`](/ticdc/ticdc-server-config.md#cdc-server-configuration-file-parameters)   | 新しく追加された | クライアント認証に許可されるユーザー名を一覧表示します。このリストにないユーザー名による認証要求は拒否されます。デフォルト値は null です。                                                                                                                          |
| ティCDC          | [`security.client-user-required`](/ticdc/ticdc-server-config.md#cdc-server-configuration-file-parameters)  | 新しく追加された | クライアント認証にユーザー名とパスワードを使用するかどうかを制御します。デフォルト値は`false`です。                                                                                                                                             |
| ティCDC          | [`security.mtls`](/ticdc/ticdc-server-config.md#cdc-server-configuration-file-parameters)                  | 新しく追加された | TLS クライアント認証を有効にするかどうかを制御します。デフォルト値は`false`です。                                                                                                                                                    |
| ティCDC          | [`sink.debezium.output-old-value`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)  | 新しく追加された | 行データが変更される前に値を出力するかどうかを制御します。デフォルト値は`true`です。無効にすると、 `UPDATE`イベントは「前」フィールドを出力しません。                                                                                                                |
| ティCDC          | [`sink.open.output-old-value`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)      | 新しく追加された | 行データが変更される前に値を出力するかどうかを制御します。デフォルト値は`true`です。無効にすると、 `UPDATE`イベントは &quot;p&quot; フィールドを出力しません。                                                                                                    |

## 廃止された機能 {#deprecated-features}

-   v8.1.0 以降では、TiDB および TiDB ダッシュボードのテレメトリ機能が削除されます。

    -   システム変数[`tidb_enable_telemetry`](/system-variables.md#tidb_enable_telemetry-new-in-v402-and-deprecated-in-v810) 、 TiDB 構成項目[`enable-telemetry`](/tidb-configuration-file.md#enable-telemetry-new-in-v402-and-deprecated-in-v810) 、および PD 構成項目[`enable-telemetry`](/pd-configuration-file.md#enable-telemetry)非推奨となり、機能しなくなりました。
    -   `ADMIN SHOW TELEMETRY`構文は削除されます。
    -   キーワード`TELEMETRY`と`TELEMETRY_ID`は削除されます。

-   以降のリリースでは[実行計画バインディングの自動進化](/sql-plan-management.md#baseline-evolution)再設計する予定であり、関連する変数と動作が変更されます。

-   TiDB Lightningパラメータ[`conflict.max-record-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)は、将来のリリースで廃止される予定であり、その後削除されます。このパラメータは`conflict.threshold`に置き換えられます。これは、競合するレコードの最大数が、単一のインポート タスクで許容できる競合するレコードの最大数と一致することを意味します。

-   v8.0.0 以降、 TiDB Lightning物理インポート モードの[競合検出の旧バージョン](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#the-old-version-of-conflict-detection-deprecated-in-v800)戦略が廃止され、 [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md)パラメータを使用して論理インポート モードと物理インポート モードの両方の競合検出戦略を制御できるようになりました。競合検出の旧バージョンの[`duplicate-resolution`](/tidb-lightning/tidb-lightning-configuration.md)パラメータは、将来のリリースで削除される予定です。

## 改善点 {#improvements}

-   ティビ

    -   `SHOW CREATE TABLE` [＃51837](https://github.com/pingcap/tidb/issues/51837) @ [ネガチョフ](https://github.com/negachov)の出力に表示される外部キーの MySQL 互換性を改善しました
    -   `SHOW CREATE TABLE` [＃52939](https://github.com/pingcap/tidb/issues/52939) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)の出力に表示される式のデフォルト値の MySQL 互換性を改善しました
    -   取り込みモード[＃52596](https://github.com/pingcap/tidb/issues/52596) @ [ランス6716](https://github.com/lance6716)で複数のインデックスを同時に追加する機能をサポート
    -   システム変数`tidb_service_scope`さまざまな値で構成し、分散実行フレームワーク (DXF) [＃52441](https://github.com/pingcap/tidb/issues/52441) @ [うわー](https://github.com/ywqzzy)の利用率を向上させることをサポート
    -   常に`false`である DNF 項目の処理を強化し、そのようなフィルター条件を直接無視することで、不要なテーブル全体のスキャンを回避します[＃40997](https://github.com/pingcap/tidb/issues/40997) @ [ハイラスティン](https://github.com/Rustin170506)
    -   オプティマイザがクエリに対して単一インデックススキャン方式（フルテーブルスキャン以外）を選択できる場合、オプティマイザがクエリに対してインデックスマージを自動的に選択しないという制限を削除するために、オプティマイザ修正コントロールの使用をサポートします[＃52869](https://github.com/pingcap/tidb/issues/52869) @ [時間と運命](https://github.com/time-and-fate)
    -   コプロセッサー演算子[＃28937](https://github.com/pingcap/tidb/issues/28937) @ [翻訳](https://github.com/cfzjywxk)の列`execution info`に`total_kv_read_wall_time`メトリックを追加します。
    -   リソースコントロールダッシュボードに`RU (max)`メトリックを追加する[＃49318](https://github.com/pingcap/tidb/issues/49318) @ [ノルーシュ](https://github.com/nolouch)
    -   リソースロック (RLock) が時間内に解放されない問題を回避するために、LDAP 認証にタイムアウトメカニズムを追加します[＃51883](https://github.com/pingcap/tidb/issues/51883) @ [ヤンケオ](https://github.com/YangKeao)

-   ティクヴ

    -   TiKV の安定性を向上させるために、 Raftstoreスレッドでスナップショット ファイルに対する IO 操作を実行しないようにします[＃16564](https://github.com/tikv/tikv/issues/16564) @ [コナー1996](https://github.com/Connor1996)
    -   TiKV [＃16680](https://github.com/tikv/tikv/issues/16680) @ [リクササシネーター](https://github.com/LykxSassinator)のシャットダウン速度を加速する
    -   スレッド[＃15927](https://github.com/tikv/tikv/issues/15927) @ [コナー1996](https://github.com/Connor1996)ごとのメモリ使用量のメトリックを追加します。

-   PD

    -   競合ロック[＃7897](https://github.com/tikv/pd/issues/7897) @ [ノルーシュ](https://github.com/nolouch)のオーバーヘッドを削減するために`OperatorController`ロジックを最適化します

-   TiFlash

    -   TLS を有効にした後に証明書を更新することでTiFlash がpanicになる可能性がある問題を軽減します[＃8535](https://github.com/pingcap/tiflash/issues/8535) @ [風の話し手](https://github.com/windtalker)

-   ツール

    -   バックアップと復元 (BR)

        -   ログバックアップの互換性テストとインデックスアクセラレーション[＃51987](https://github.com/pingcap/tidb/issues/51987) @ [リーヴルス](https://github.com/Leavrth)の追加をカバーする PITR 統合テストケースを追加します。
        -   ログバックアップの開始時にアクティブな DDL ジョブの無効な検証を削除します[＃52733](https://github.com/pingcap/tidb/issues/52733) @ [リーヴルス](https://github.com/Leavrth)
        -   PITR とインデックス追加機能の高速化の互換性をテストするためのテスト ケースを追加します[＃51988](https://github.com/pingcap/tidb/issues/51988) @ [リーヴルス](https://github.com/Leavrth)
        -   BR はデータ復旧中に空の SST ファイルをクリーンアップします[＃16005](https://github.com/tikv/tikv/issues/16005) @ [リーヴルス](https://github.com/Leavrth)

    -   ティCDC

        -   REDOログを使用してデータリカバリ中のメモリの安定性を向上させ、OOM [＃10900](https://github.com/pingcap/tiflow/issues/10900) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)の可能性を低減します。
        -   トランザクション競合シナリオでのデータレプリケーションの安定性が大幅に向上し、パフォーマンスが最大10倍向上します[＃10896](https://github.com/pingcap/tiflow/issues/10896) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)

## バグ修正 {#bug-fixes}

-   ティビ

    -   複数値インデックスを持つテーブルを含むSQL文を実行すると、 `Can't find a proper physical plan for this query`エラー[＃49438](https://github.com/pingcap/tidb/issues/49438) @ [qw4990](https://github.com/qw4990)が返される可能性がある問題を修正しました。
    -   OOM エラーが発生した後に自動統計収集が停止する問題を修正[＃51993](https://github.com/pingcap/tidb/issues/51993) @ [ハイラスティン](https://github.com/Rustin170506)
    -   BR を使用して統計情報のないテーブルを復元した後、そのテーブルの統計情報の健全性が 100% のままになる問題を修正しました[＃29769](https://github.com/pingcap/tidb/issues/29769) @ [ウィノロス](https://github.com/winoros)
    -   アップグレード[＃52040](https://github.com/pingcap/tidb/issues/52040) @ [ハイラスティン](https://github.com/Rustin170506)中に TiDB がシステム テーブルの統計を作成する問題を修正
    -   統計の初期化が完了する前に自動統計収集がトリガーされる問題を修正[＃52346](https://github.com/pingcap/tidb/issues/52346) @ [ハイラスティン](https://github.com/Rustin170506)
    -   `tidb_mem_quota_analyze`が有効になっていて、統計の更新に使用されるメモリが制限[＃52601](https://github.com/pingcap/tidb/issues/52601) @ [ホーキングレイ](https://github.com/hawkingrei)を超えると TiDB がクラッシュする可能性がある問題を修正しました
    -   TiDB の同期的な統計読み込みメカニズムが空の統計の読み込みを無期限に再試行し、 `fail to get stats version for this histogram` log [＃52657](https://github.com/pingcap/tidb/issues/52657) @ [ホーキングレイ](https://github.com/hawkingrei)を出力問題を修正しました。
    -   照合の新しいフレームワークが無効になっている場合、異なる照合を含む式によってクエリがpanicになる可能性がある問題を修正[＃52772](https://github.com/pingcap/tidb/issues/52772) @ [翻訳:](https://github.com/wjhuang2016)
    -   `CPS by type`メトリックに誤った値[＃52605](https://github.com/pingcap/tidb/issues/52605) @ [ノルーシュ](https://github.com/nolouch)が表示される問題を修正
    -   `INFORMATION_SCHEMA.TIKV_REGION_STATUS` [＃52013](https://github.com/pingcap/tidb/issues/52013) @ [じゃがいも](https://github.com/JmPotato)をクエリすると nil ポインタエラーが発生する問題を修正しました
    -   列[＃51592](https://github.com/pingcap/tidb/issues/51592) @ [ダンキシュ](https://github.com/danqixu)に無効なデフォルト値が指定されたときに表示される誤ったエラー メッセージを修正しました。
    -   取り込みモードでインデックスを追加すると、一部のコーナーケースでデータインデックスの不整合が発生する可能性がある問題を修正[＃51954](https://github.com/pingcap/tidb/issues/51954) @ [ランス6716](https://github.com/lance6716)
    -   外部キー[＃51838](https://github.com/pingcap/tidb/issues/51838) @ [ヤンケオ](https://github.com/YangKeao)を持つテーブルを復元するときに DDL 操作が停止する問題を修正しました
    -   TiDBネットワークが分離されているときにインデックスの追加が失敗する問題を修正[＃51846](https://github.com/pingcap/tidb/issues/51846) @ [うわー](https://github.com/ywqzzy)
    -   インデックスの名前を変更した後に同じ名前のインデックスを追加するとエラーが発生する問題を修正[＃51431](https://github.com/pingcap/tidb/issues/51431) @ [ランス6716](https://github.com/lance6716)
    -   インデックス[＃52411](https://github.com/pingcap/tidb/issues/52411) @ [タンジェンタ](https://github.com/tangenta)の追加中にクラスターのアップグレードによって発生するデータ インデックスの不整合の問題を修正しました。
    -   分散実行フレームワーク (DXF) [＃52640](https://github.com/pingcap/tidb/issues/52640) @ [タンジェンタ](https://github.com/tangenta)を有効にした後に、大きなテーブルにインデックスを追加できない問題を修正しました。
    -   インデックスを同時に追加するとエラー`no such file or directory` [＃52475](https://github.com/pingcap/tidb/issues/52475) @ [タンジェンタ](https://github.com/tangenta)が報告される問題を修正しました
    -   インデックスの追加が失敗した後に一時データをクリーンアップできない問題を修正[＃52639](https://github.com/pingcap/tidb/issues/52639) @ [ランス6716](https://github.com/lance6716)
    -   プラン キャッシュ シナリオ[＃51407](https://github.com/pingcap/tidb/issues/51407) @ [翻訳:](https://github.com/wjhuang2016)でメタデータ ロックが DDL 操作の実行を阻止できない問題を修正しました。
    -   大量のデータをインポートするときに`IMPORT INTO`操作が停止する問題を修正[＃52884](https://github.com/pingcap/tidb/issues/52884) @ [ランス6716](https://github.com/lance6716)
    -   gRPC エラー[＃51301](https://github.com/pingcap/tidb/issues/51301) @ [グオシャオゲ](https://github.com/guo-shaoge)をログに記録するときに TiDB が予期せず再起動する問題を修正しました
    -   IndexHashJoin が Anti Left Outer Semi Join [＃52923](https://github.com/pingcap/tidb/issues/52923) @ [いびん87](https://github.com/yibin87)を計算するときに冗長データを出力する問題を修正しました。
    -   相関サブクエリ[＃52777](https://github.com/pingcap/tidb/issues/52777) @ [いびん87](https://github.com/yibin87)の TopN 演算子の誤った結果を修正
    -   HashJoin プローブ[＃52222](https://github.com/pingcap/tidb/issues/52222) @ [風の話し手](https://github.com/windtalker)の不正確な実行時間統計を修正
    -   静的パーティションプルーニングモードで`TABLESAMPLE`使用すると誤った結果が返される問題を修正（ `tidb_partition_prune_mode='static'` ） [＃52282](https://github.com/pingcap/tidb/issues/52282) @ [タンジェンタ](https://github.com/tangenta)
    -   夏時間[＃51675](https://github.com/pingcap/tidb/issues/51675) @ [lcwangchao](https://github.com/lcwangchao)で TTL が 1 時間ずれる問題を修正
    -   TiDBダッシュボード監視ページ[＃51889](https://github.com/pingcap/tidb/issues/51889) @ [ヤンケオ](https://github.com/YangKeao)での接続数（接続数）の計算と表示が誤っていた問題を修正
    -   パーティション DDL タスク[＃51090](https://github.com/pingcap/tidb/issues/51090) @ [ジフハウス](https://github.com/jiyfhust)をロールバックするときにステータスが停止する問題を修正しました
    -   `EXPLAIN ANALYZE` [＃52646](https://github.com/pingcap/tidb/issues/52646) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)を実行すると`max_remote_stream`の値が正しくなくなる問題を修正しました
    -   `TIDB_HOT_REGIONS`テーブルをクエリすると、誤って`INFORMATION_SCHEMA`テーブル[＃50810](https://github.com/pingcap/tidb/issues/50810) @ [定義2014](https://github.com/Defined2014)が返される可能性がある問題を修正しました。
    -   特定の列の統計が完全にロードされていない場合に、 `EXPLAIN`ステートメントの結果に誤った列 ID が表示される可能性がある問題を修正しました[＃52207](https://github.com/pingcap/tidb/issues/52207) @ [時間と運命](https://github.com/time-and-fate)
    -   `IFNULL`関数によって返される型が MySQL [＃51765](https://github.com/pingcap/tidb/issues/51765) @ [ヤンケオ](https://github.com/YangKeao)と一致しない問題を修正
    -   ユニークインデックスを追加すると TiDB がpanicを起こす可能性がある問題を修正[＃52312](https://github.com/pingcap/tidb/issues/52312) @ [翻訳:](https://github.com/wjhuang2016)

-   ティクヴ

    -   古いリージョンピアが GC メッセージ[＃16504](https://github.com/tikv/tikv/issues/16504) @ [クレイジーcs520](https://github.com/crazycs520)を無視すると、resolve-ts がブロックされる問題を修正しました。
    -   RocksDB の非アクティブな Write Ahead Logs (WAL) によってデータが破損する可能性がある問題を修正[＃16705](https://github.com/tikv/tikv/issues/16705) @ [コナー1996](https://github.com/Connor1996)

-   PD

    -   PD マイクロサービス モードのオン/オフを切り替えるときに TSO が停止する可能性がある問題を修正[＃7849](https://github.com/tikv/pd/issues/7849) @ [じゃがいも](https://github.com/JmPotato)
    -   DR自動同期の`State`監視メトリックにデータが表示されない問題を修正[＃7974](https://github.com/tikv/pd/issues/7974) @ [翻訳者](https://github.com/lhy1024)
    -   バイナリバージョンのチェックでPDpanic[＃7978](https://github.com/tikv/pd/issues/7978) @ [じゃがいも](https://github.com/JmPotato)が発生する可能性がある問題を修正
    -   TTLパラメータを解析するときに発生する型変換エラーを修正[＃7980](https://github.com/tikv/pd/issues/7980) @ [ヒューシャープ](https://github.com/HuSharp)
    -   展開された 2 つのデータセンター間でLeaderを切り替えると転送が失敗する問題を修正[＃7992](https://github.com/tikv/pd/issues/7992) @ [トンスネークリン](https://github.com/TonsnakeLin)
    -   pd-ctl の`PrintErrln`が`stderr` [＃8022](https://github.com/tikv/pd/issues/8022) @ [ヒューシャープ](https://github.com/HuSharp)にエラーメッセージを出力できない問題を修正しました
    -   `Merge`スケジュール[＃8049](https://github.com/tikv/pd/issues/8049) @ [ノルーシュ](https://github.com/nolouch)を生成するときに PD がpanicになる可能性がある問題を修正しました
    -   `GetAdditionalInfo` [＃8079](https://github.com/tikv/pd/issues/8079) @ [ヒューシャープ](https://github.com/HuSharp)によって引き起こされるpanic問題を修正
    -   PDの`Filter target`監視メトリックが散布範囲情報を提供しない問題を修正[＃8125](https://github.com/tikv/pd/issues/8125) @ [ヒューシャープ](https://github.com/HuSharp)
    -   クエリ結果`SHOW CONFIG`に非推奨の構成項目`trace-region-flow` [＃7917](https://github.com/tikv/pd/issues/7917) @ [rleungx](https://github.com/rleungx)が含まれる問題を修正しました
    -   スケーリングの進行状況が正しく表示されない問題を修正[＃7726](https://github.com/tikv/pd/issues/7726) @ [キャビンフィーバーB](https://github.com/CabinfeverB)

-   TiFlash

    -   非厳密な`sql_mode` [＃8803](https://github.com/pingcap/tiflash/issues/8803) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)で無効なデフォルト値を持つ列にデータを挿入するとTiFlash がpanicになる可能性がある問題を修正しました
    -   同時実行性の高い読み取りシナリオでTiFlash が一時的に誤った結果を返す可能性がある問題を修正[＃8845](https://github.com/pingcap/tiflash/issues/8845) @ [ジンヘリン](https://github.com/JinheLin)
    -   分散storageおよびコンピューティングアーキテクチャで、 TiFlashコンピューティング ノード[＃8920](https://github.com/pingcap/tiflash/issues/8920) @ [ジンヘリン](https://github.com/JinheLin)の`storage.remote.cache.capacity`構成項目の値を変更した後、Grafana に表示されるディスク`used_size`メトリックが正しくない問題を修正しました。
    -   クラスターを v6.5.0 より前のバージョンから v6.5.0 以降にアップグレードするときに、 TiFlashメタデータが破損してプロセスがpanicになる可能性がある問題を修正しました[＃9039](https://github.com/pingcap/tiflash/issues/9039) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)
    -   分散storageとコンピューティングアーキテクチャで、コンピューティングノードのプロセスが停止するとTiFlash がpanicになる可能性がある問題を修正しました[＃8860](https://github.com/pingcap/tiflash/issues/8860) @ [グオシャオゲ](https://github.com/guo-shaoge)
    -   仮想生成列[＃8787](https://github.com/pingcap/tiflash/issues/8787) @ [グオシャオゲ](https://github.com/guo-shaoge)を含むクエリを実行するとTiFlash がエラーを返す可能性がある問題を修正しました。

-   ツール

    -   バックアップと復元 (BR)

        -   BRが`AUTO_RANDOM`列[＃52255](https://github.com/pingcap/tidb/issues/52255) @ [リーヴルス](https://github.com/Leavrth)を含むユニオン クラスター化インデックスの`AUTO_RANDOM` ID 割り当ての進行状況をバックアップできない問題を修正しました。
        -   ログバックアップタスクを一時停止後に削除しても、GCセーフポイント[＃52082](https://github.com/pingcap/tidb/issues/52082) @ [3ポインター](https://github.com/3pointer)すぐに復元されない問題を修正しました。
        -   特別なイベントのタイミングにより、ログ バックアップ[＃16739](https://github.com/tikv/tikv/issues/16739) @ [ユジュンセン](https://github.com/YuJuncen)でデータが失われる可能性があるというまれな問題を修正しました。
        -   TiKV の再起動により、ログ バックアップのグローバル チェックポイントが実際のバックアップ ファイルの書き込みポイントよりも先に進められ、少量のバックアップ データが失われる可能性がある問題を修正しました[＃16809](https://github.com/tikv/tikv/issues/16809) @ [ユジュンセン](https://github.com/YuJuncen)
        -   フルバックアップ[＃50837](https://github.com/pingcap/tidb/issues/50837) @ [ボーンチェンジャー](https://github.com/BornChanger)中に`--concurrency`に関連する紛らわしい情報がログに表示される問題を修正
        -   BR を使用してデータを復元する場合、または物理インポート モードでTiDB Lightning を使用してデータをインポートする場合に、PD から取得されたリージョンにLeaderがない問題を修正しました[＃51124](https://github.com/pingcap/tidb/issues/51124) [#50501](https://github.com/pingcap/tidb/issues/50501) @ [リーヴルス](https://github.com/Leavrth)
        -   ログバックアップタスクを一時停止、停止、再構築した後、タスクの状態は正常であるが、チェックポイントが[＃53047](https://github.com/pingcap/tidb/issues/53047) @ [リドリス](https://github.com/RidRisR)に進まない問題を修正しました。
        -   不安定なテストケースを修正`TestClearCache` [＃51671](https://github.com/pingcap/tidb/issues/51671) @ [翻訳者](https://github.com/zxc111)
        -   不安定なテストケースを修正`TestGetMergeRegionSizeAndCount` [＃52095](https://github.com/pingcap/tidb/issues/52095) @ [3ポインター](https://github.com/3pointer)
        -   不安定な統合テストを修正`br_tikv_outage` [＃52673](https://github.com/pingcap/tidb/issues/52673) @ [リーヴルス](https://github.com/Leavrth)
        -   テストケース`TestGetTSWithRetry`の実行に時間がかかりすぎる問題を修正[＃52547](https://github.com/pingcap/tidb/issues/52547) @ [リーヴルス](https://github.com/Leavrth)
        -   PD [＃17020](https://github.com/tikv/tikv/issues/17020) @ [ユジュンセン](https://github.com/YuJuncen)へのネットワーク接続が不安定な状態で一時停止中のログ バックアップ タスクを再開すると TiKV がpanicになる可能性がある問題を修正しました。

    -   ティCDC

        -   TiCDC所有者ノードを退去させるAPI（ `/api/v2/owner/resign` ）を呼び出すと、TiCDCタスクが予期せず再起動する問題を修正しました[＃10781](https://github.com/pingcap/tiflow/issues/10781) @ [スドジ](https://github.com/sdojjy)
        -   下流の Pulsar が停止しているときに、changefeed を削除すると通常の TiCDC プロセスが停止し、他の changefeed プロセスも停止するという問題を修正しました[＃10629](https://github.com/pingcap/tiflow/issues/10629) @ [アズドンメン](https://github.com/asddongmen)
        -   Grafana の**所有権履歴**パネルが不安定になる問題を修正[＃10796](https://github.com/pingcap/tiflow/issues/10796) @ [ホンユンヤン](https://github.com/hongyunyan)
        -   PD を再起動すると、TiCDC ノードがエラー[＃10799](https://github.com/pingcap/tiflow/issues/10799) @ [3エースショーハンド](https://github.com/3AceShowHand)で再起動する可能性がある問題を修正しました。
        -   PD ディスク I/O の高レイテンシーによりデータレプリケーション[＃9054](https://github.com/pingcap/tiflow/issues/9054) @ [アズドンメン](https://github.com/asddongmen)で深刻なレイテンシーが発生する問題を修正
        -   `TIMEZONE`種類のデフォルト値が正しいタイムゾーン[＃10931](https://github.com/pingcap/tiflow/issues/10931) @ [3エースショーハンド](https://github.com/3AceShowHand)に従って設定されない問題を修正
        -   `DROP PRIMARY KEY`と`DROP UNIQUE KEY`ステートメントが正しく複製されない問題を修正[＃10890](https://github.com/pingcap/tiflow/issues/10890) @ [アズドンメン](https://github.com/asddongmen)
        -   TiCDC が上流に書き込まれた後に下流の`Exchange Partition ... With Validation` DDL の実行に失敗し、変更フィードが[＃10859](https://github.com/pingcap/tiflow/issues/10859) @ [ホンユンヤン](https://github.com/hongyunyan)で停止する問題を修正しました。

    -   TiDB Lightning

        -   ソースファイル[＃51800](https://github.com/pingcap/tidb/issues/51800) @ [ランス6716](https://github.com/lance6716)内の互換性のない SQL ステートメントが原因で、 TiDB Lightning がデータインポート中に`no database selected`報告する問題を修正しました。
        -   TiDB Lightning がサーバーモード[＃36374](https://github.com/pingcap/tidb/issues/36374) @ [ケニー](https://github.com/kennytm)でログに機密情報を出力する可能性がある問題を修正しました
        -   PDLeaderを強制終了すると、 TiDB Lightning がデータ インポート[#50501](https://github.com/pingcap/tidb/issues/50501) @ [リーヴルス](https://github.com/Leavrth)中に`invalid store ID 0`エラーを報告する問題を修正しました。
        -   `replace`戦略[＃52886](https://github.com/pingcap/tidb/issues/52886) @ [翻訳者](https://github.com/lyzx2001)を使用して競合するデータを処理するときにTiDB Lightning が`Unknown column in where clause`エラーを報告する問題を修正しました。
        -   Parquet 形式[＃52518](https://github.com/pingcap/tidb/issues/52518) @ [ケニー](https://github.com/kennytm)の空のテーブルをインポートするときにTiDB Lightning がパニックになる問題を修正しました。

## パフォーマンステスト {#performance-test}

TiDB v8.1.0 のパフォーマンスについては、 TiDB Cloud Dedicated クラスターの[TPC-C パフォーマンステストレポート](https://docs.pingcap.com/tidbcloud/v8.1-performance-benchmarking-with-tpcc)と[Sysbench パフォーマンステストレポート](https://docs.pingcap.com/tidbcloud/v8.1-performance-benchmarking-with-sysbench)を参照してください。

## 寄稿者 {#contributors}

TiDB コミュニティの以下の貢献者に感謝いたします。

-   [アルトゥルメランチク](https://github.com/arturmelanchyk) (初めての投稿者)
-   [キャビンフィーバーB](https://github.com/CabinfeverB)
-   [ダンキシュ](https://github.com/danqixu) (初めての投稿者)
-   [イマラソン](https://github.com/imalasong) (初めての投稿者)
-   [ジフハウス](https://github.com/jiyfhust)
-   [ネガチョフ](https://github.com/negachov) (初めての投稿者)
-   [テストウィル](https://github.com/testwill)
-   [yzhan1](https://github.com/yzhan1) (初めての投稿者)
-   [翻訳者](https://github.com/zxc111) (初めての投稿者)
