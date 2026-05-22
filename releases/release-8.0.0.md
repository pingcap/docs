---
title: TiDB 8.0.0 Release Notes
summary: TiDB 8.0.0 の新機能、互換性の変更点、改善点、およびバグ修正についてご確認ください。
---

# TiDB 8.0.0 リリースノート {#tidb-8-0-0-release-notes}

発売日：2024年3月29日

TiDB バージョン: 8.0.0

クイックアクセス: [クイックスタート](https://docs-archive.pingcap.com/tidb/v8.0/quick-start-with-tidb)

バージョン8.0.0では、以下の主要な機能と改善点が導入されています。

<table><thead><tr><th>カテゴリ</th><th>機能／改善点</th><th>説明</th></tr></thead><tbody><tr><td rowspan="4">拡張性とパフォーマンス</td><td><a href="https://docs-archive.pingcap.com/tidb/v8.0/pd-microservices">スケーラビリティ向上のためのPDの分解（実験的）</a></td><td>配置Driver（PD）には、TiDBクラスターの正常な動作を保証するための複数の重要なモジュールが含まれています。クラスターのワークロードが増加すると、PD内の各モジュールのリソース消費量も増加し、これらのモジュール間で相互干渉が発生し、最終的にクラスター全体のサービス品質に影響を与えます。v8.0.0以降、TiDBはこの問題に対処するため、PD内のTSOモジュールとスケジューリングモジュールを独立してデプロイ可能なマイクロサービスに分割しました。これにより、クラスターの規模が拡大するにつれて、モジュール間の相互干渉を大幅に削減できます。このアーキテクチャにより、より大規模なワークロードを持つ、より大規模なクラスターの構築が可能になりました。</td></tr><tr><td><a href="https://docs-archive.pingcap.com/tidb/v8.0/system-variables#tidb_dml_type-new-in-v800">より大規模なトランザクション向けの一括DML（実験的）</a></td><td>大規模なバッチ DML ジョブ（大規模なクリーンアップ ジョブ、結合、集計など）は、大量のメモリを消費する可能性があり、これまで非常に大規模な処理には制限がありました。バルク DML ( <code>tidb_dml_type = &quot;bulk&quot;</code> ) は、トランザクション保証を提供し、メモリ不足の問題を軽減しながら、大規模なバッチ DML タスクをより効率的に処理するための新しい DML タイプです。この機能は、データ ロードに使用する場合、インポート、ロード、およびリストア操作とは異なります。</td></tr><tr><td><a href="https://docs-archive.pingcap.com/tidb/v8.0/br-snapshot-guide#restore-cluster-snapshots">クラスタースナップショット復元速度の向上（GA）</a></td><td>この機能により、 BRはクラスターの規模の利点を最大限に活用し、クラスター内のすべてのTiKVノードがデータ復元の準備段階に参加できるようになります。この機能は、大規模クラスターにおける大規模データセットの復元速度を大幅に向上させます。実際のテストでは、この機能によりダウンロード帯域幅が飽和状態になり、ダウンロード速度が8～10倍、エンドツーエンドの復元速度が約1.5～3倍向上することが示されています。</td></tr><tr><td>テーブル数が膨大な場合のスキーマ情報のキャッシュの安定性を向上させる（実験的）</td><td> TiDBをマルチテナントアプリケーションの記録システムとして利用するSaaS企業は、多くの場合、膨大な数のテーブルを保存する必要があります。以前のバージョンでは、100万個以上のテーブルを処理することは可能でしたが、ユーザーエクスペリエンス全体が低下する可能性がありました。TiDB v8.0.0では、 <code>auto analyze</code>用の<a href="https://docs-archive.pingcap.com/tidb/v8.0/system-variables#tidb_enable_auto_analyze_priority_queue-new-in-v800">優先度キュー</a>を実装することで状況が改善され、処理がより柔軟になり、より幅広いテーブルで安定性が向上します。</td></tr><tr><td rowspan="1">データベースの運用と可観測性</td><td>インデックス使用統計の監視をサポートします</td><td>適切なインデックス設計は、データベースのパフォーマンスを維持するための重要な前提条件です。TiDB v8.0.0 では、インデックスの使用状況統計情報を提供する<a href="https://docs-archive.pingcap.com/tidb/v8.0/information-schema-tidb-index-usage"><code>INFORMATION_SCHEMA.TIDB_INDEX_USAGE</code></a>テーブルと<a href="https://docs-archive.pingcap.com/tidb/v8.0/sys-schema-unused-indexes"><code>sys.schema_unused_indexes</code></a>ビューが導入されました。この機能は、データベース内のインデックスの効率性を評価し、インデックス設計を最適化するのに役立ちます。</td></tr><tr><td rowspan="2">データ移行</td><td>TiCDCが<a href="https://docs-archive.pingcap.com/tidb/v8.0/ticdc-simple-protocol">Simpleプロトコル</a>のサポートを追加</td><td>TiCDCは、新しいプロトコルであるSimpleプロトコルを導入しました。このプロトコルは、DDLおよびBOOTSTRAPイベントにテーブルスキーマ情報を埋め込むことで、インバンドスキーマ追跡機能を提供します。</td></tr><tr><td> TiCDCは<a href="https://docs-archive.pingcap.com/tidb/v8.0/ticdc-debezium">Debeziumフォーマットプロトコル</a>のサポートを追加しました。</td><td> TiCDCは、新しいプロトコルであるDebeziumプロトコルを導入しました。TiCDCは、Debezium形式のメッセージを生成するプロトコルを使用して、データ変更イベントをKafkaシンクに発行できるようになりました。</td></tr></tbody></table>

## 機能の詳細 {#feature-details}

### 拡張性 {#scalability}

-   PDはマイクロサービスモードをサポートしています（実験的） [#5766](https://github.com/tikv/pd/issues/5766) @[binshi-bing](https://github.com/binshi-bing)

    バージョン8.0.0以降、PDはマイクロサービスモードをサポートしています。このモードでは、PDのタイムスタンプ割り当て機能とクラスタースケジューリング関数を個別のマイクロサービスに分割し、それぞれを独立してデプロイできるため、PDのパフォーマンス拡張性が向上し、大規模クラスターにおけるPDのパフォーマンスボトルネックが解消されます。

    -   `tso`マイクロサービス: クラスター全体に単調増加するタイムスタンプ割り当てを提供します。
    -   `scheduling`マイクロサービス: 負荷分散、ホットスポット処理、レプリカ修復、レプリカ配置などを含むがこれらに限定されない、クラスター全体のスケジューリング関数を提供します。

    各マイクロサービスは独立したプロセスとしてデプロイされます。マイクロサービスに複数のレプリカを設定すると、マイクロサービスは自動的にプライマリ/セカンダリのフォールトトレラントモードを実装し、サービスの高い可用性と信頼性を確保します。

    現在、PDマイクロサービスはTiDB Operatorを使用してのみデプロイできます。PDがスケールアップでは解決できないほどの深刻なパフォーマンスボトルネックとなった場合は、このモードを検討することをお勧めします。

    詳細については、[ドキュメント](/pd-microservices.md)を参照してください。

<!---->

-   Titan エンジンの使いやすさを向上 [#16245](https://github.com/tikv/tikv/issues/16245) @[Connor1996](https://github.com/Connor1996)

    -   Titan blob ファイルと RocksDB ブロックファイルの共有キャッシュをデフォルトで有効にします ( [`shared-blob-cache`](/tikv-configuration-file.md#shared-blob-cache-new-in-v800)デフォルト値は`true`です)。これにより、[`blob-cache-size`](/tikv-configuration-file.md#blob-cache-size)個別に設定する必要がなくなります。
    -   Titanエンジンを使用する際のパフォーマンスと柔軟性を向上させるため、 [`min-blob-size`](/tikv-configuration-file.md#min-blob-size) 、 [`blob-file-compression`](/tikv-configuration-file.md#blob-file-compression) 、 [`discardable-ratio`](/tikv-configuration-file.md#min-blob-size)を動的に変更することをサポートします。

    詳細については、[ドキュメント](/ストレージ-engine/titan-configuration.md)を参照してください。

### パフォーマンス {#performance}

-   BRによりスナップショットの復元速度が向上 (GA) [#50701](https://github.com/pingcap/tidb/issues/50701) @[3pointer](https://github.com/3pointer)@[Leavrth](https://github.com/Leavrth)

    TiDB v8.0.0以降、スナップショット復元速度の高速化が一般提供（GA）となり、デフォルトで有効になっています。BRは、粗粒度リージョン分散アルゴリズムの採用、データベースとテーブルのバッチ作成、SSTファイルダウンロードと取り込み操作間の相互影響の低減、テーブル統計情報の復元の高速化など、さまざまな最適化を実装することで、スナップショット復元速度を大幅に向上させています。実際のケースでのテスト結果によると、単一のTiKVノードのデータ復元速度は1.2 GiB/sで安定し、100 TiBのデータを1時間以内に復元できます。

    これは、高負荷環境でもBRが各 TiKVノードのリソースを最大限に活用し、データベースの復元時間を大幅に短縮し、データベースの可用性と信頼性を向上させ、データ損失やシステム障害によるダウンタイムやビジネス損失を削減できることを意味します。復元速度の向上は、多数のゴルーチンの並列実行によるものであり、特にテーブルやリージョンが多い場合は、メモリ消費量が大幅に増加する可能性があることに注意してください。BRを実行するには、メモリ容量の大きいマシンを使用することをお勧めします。マシンのメモリ容量が限られている場合は、よりきめ細かいリージョン分散アルゴリズムを使用することをお勧めします。また、粗い粒度のリージョン分散アルゴリズムは外部ストレージの帯域幅を大量に消費する可能性があるため、外部帯域幅不足による他のアプリケーションへの影響を避ける必要があります。

    詳細については、 [ドキュメント](/br/br-snapshot-guide.md#restore-cluster-snapshots)を参照してください。

-   TiFlashへの以下の関数のプッシュダウンをサポート[#50975](https://github.com/pingcap/tidb/issues/50975) [#50485](https://github.com/pingcap/tidb/issues/50485) @[yibin87](https://github.com/yibin87) @[windtalker](https://github.com/windtalker)

    -   `CAST(DECIMAL AS DOUBLE)`
    -   `POWER()`

    詳細については、 [ドキュメント](/tiflash/tiflash-supported-pushdown-calculations.md)を参照してください。

-   TiDB の並列 HashAgg アルゴリズムはディスク スピルをサポートします (実験的) [#35637](https://github.com/pingcap/tidb/issues/35637) @[xzhangxian1008](https://github.com/xzhangxian1008)

    TiDBの以前のバージョンでは、HashAgg演算子の並行処理アルゴリズムはディスクスピルをサポートしていませんでした。SQL文の実行プランに並列HashAgg演算子が含まれている場合、そのSQL文のすべてのデータはメモリ内でしか処理できません。そのため、TiDBは大量のデータをメモリ内で処理する必要があります。データサイズがメモリ制限を超えると、TiDBは並列処理を行わないアルゴリズムしか選択できず、パフォーマンス向上のための並行処理を活用できません。

    バージョン 8.0.0 では、TiDB の並列 HashAgg アルゴリズムがディスク スピルをサポートしています。並列処理のあらゆる状況において、HashAgg オペレータはメモリ使用量に基づいてデータ スピルを自動的にトリガーし、パフォーマンスとデータ スループットのバランスを取ることができます。現在、実験的機能として、TiDB はディスク スピルをサポートする並列 HashAgg アルゴリズムを有効にするかどうかを制御する`tidb_enable_parallel_hashagg_spill`変数を導入しています。この変数が`ON`の場合、有効になっていることを意味します。この機能が将来のリリースで一般提供されるようになった後、この変数は非推奨となります。

    詳細については、 [ドキュメント](/system-variables.md#tidb_enable_parallel_hashagg_spill-new-in-v800)を参照してください。

-   自動統計収集の優先キューを導入 [#50132](https://github.com/pingcap/tidb/issues/50132) @[Rustin170506](https://github.com/Rustin170506)

    オプティマイザ統計を最新の状態に保つことは、データベースのパフォーマンスを安定させる鍵となります。ほとんどのユーザーは、最新の統計情報を収集するために、TiDB が提供する[自動統計収集](/statistics.md#automatic-update)機能を利用しています。自動統計収集機能は、すべてのオブジェクトの統計ステータスをチェックし、異常なオブジェクトをキューに追加して順次収集します。以前のバージョンでは、この順序がランダムであったため、より適切な候補が更新されるまで過剰な待ち時間が発生し、パフォーマンスの低下につながる可能性がありました。

    バージョン8.0.0以降、自動統計収集機能は、さまざまな条件に基づいてオブジェクトの優先順位を動的に設定し、新規作成されたインデックスや定義変更のあるパーティションテーブルなど、より優先度の高い候補が優先的に処理されるようにします。さらに、TiDBは健全性スコアの低いテーブルを優先し、キューの最上位に配置します。この機能強化により、収集順序がより合理的になり、古い統計情報によって引き起こされるパフォーマンスの問題が軽減されるため、データベースの安定性が向上します。

    詳細については、 [ドキュメント](/system-variables.md#tidb_enable_auto_analyze_priority_queue-new-in-v800)を参照してください。

-   実行プランのキャッシュに関するいくつかの制限を削除 [#49161](https://github.com/pingcap/tidb/pull/49161) @[mjonss](https://github.com/mjonss)@[qw4990](https://github.com/qw4990)

    TiDBは[プランキャッシュ](/sql-prepared-plan-cache.md)キャッシュをサポートしており、OLTPシステムのレイテンシーを効果的に削減し、パフォーマンス向上に重要な役割を果たします。バージョン8.0.0では、TiDBはプランキャッシュに関するいくつかの制限を撤廃しました。以下の項目を含む実行プランをキャッシュできるようになりました。

    -   [パーティションテーブル](/partitioned-table.md)
    -   [生成された列](/generated-columns.md)(生成された列に依存するオブジェクト ( [多値インデックス](/choose-index.md#multi-valued-indexes-and-plan-cache)など) を含む)

    この機能強化により、プランキャッシュのユースケースが拡張され、複雑なシナリオにおけるデータベース全体のパフォーマンスが向上します。

    詳細については、[ドキュメント](/sql-prepared-plan-cache.md)を参照してください。

-   オプティマイザーが多値インデックスのサポートを強化[#47759](https://github.com/pingcap/tidb/issues/47759) [#46539](https://github.com/pingcap/tidb/issues/46539) @[Arenatlx](https://github.com/Arenatlx)@[time-and-fate](https://github.com/time-and-fate)

    TiDB v6.6.0 では[複数値インデックス](/sql-statements/sql-statement-create-index.md#multi-valued-indexes)が導入され、JSON データ型のクエリ パフォーマンスが向上しました。v8.0.0 では、オプティマイザがマルチ値インデックスのサポートを強化し、複雑なシナリオでクエリを最適化するために、それらを正しく識別して利用できるようになりました。

    -   オプティマイザは、複数値インデックスに関する統計情報を収集し、その統計情報に基づいて実行プランを決定します。SQL文で複数の複数値インデックスを選択できる場合、オプティマイザはコストが最も低いインデックスを特定できます。
    -   `OR`を使用して複数の`member of`条件を接続する場合、オプティマイザは各 DNF 項目 ( `member of`条件) に対して有効なインデックス部分パスを照合し、これらのパスを Union を使用して結合して`Index Merge`を形成できます。これにより、条件フィルタリングとデータ取得の効率が向上します。

    詳細については、 [ドキュメント](/sql-statements/sql-statement-create-index.md#multi-valued-indexes)を参照してください。

-   低精度 TSO [#51081](https://github.com/pingcap/tidb/issues/51081) @[Tema](https://github.com/Tema)の更新間隔の構成をサポート

    TiDBの[低精度TSO機能](/system-variables.md#tidb_low_resolution_tso)定期的に更新されるTSOをトランザクションのタイムスタンプとして使用します。古いデータの読み取りが許容されるシナリオでは、この機能はリアルタイム性能を犠牲にすることで、小規模な読み取り専用トランザクションのTSO取得のオーバーヘッドを削減し、高並行読み取りの能力を向上させます。

    バージョン8.0.0より前は、低精度TSO機能のTSO更新間隔は固定されており、実際のアプリケーション要件に応じて調整できませんでした。バージョン8.0.0では、TiDBはTSO更新間隔を制御するためのシステム変数`tidb_low_resolution_tso_update_interval`を導入しました。この機能は、低精度TSO機能が有効になっている場合にのみ有効です。

    詳細については、 [ドキュメント](/system-variables.md#tidb_low_resolution_tso_update_interval-new-in-v800)を参照してください。

### 可用性 {#availability}

-   プロキシコンポーネントTiProxyが一般提供開始（GA）になりました [#413](https://github.com/pingcap/tiproxy/issues/413) @[djshow832](https://github.com/djshow832) @[xhebox](https://github.com/xhebox)

    TiDB v7.6.0では、実験的機能としてプロキシコンポーネントTiProxyが導入されました。TiProxyはTiDBの公式プロキシコンポーネントであり、クライアントとTiDBサーバーの間に配置されます。TiProxyはTiDBの負荷分散と接続維持関数を提供し、TiDBクラスターのワークロードをよりバランス良く分散させ、メンテナンス作業中のデータベースへのユーザーアクセスに影響を与えないようにします。

    バージョン8.0.0では、TiProxyが一般提供開始となり、署名証明書の自動生成機能と監視関数が強化されました。

    TiProxyの利用シナリオは以下のとおりです。

    -   TiDBクラスターにおけるローリング再起動、ローリングアップグレード、スケールインなどのメンテナンス作業中、TiDBサーバーに変更が発生すると、クライアントとTiDBサーバー間の接続が中断されます。TiProxyを使用することで、これらのメンテナンス作業中に接続を他のTiDBサーバーにスムーズに移行できるため、クライアントへの影響を最小限に抑えることができます。
    -   TiDBサーバーへのクライアント接続を、他のTiDBサーバーに動的に移行することはできません。複数のTiDBサーバーのワークロードが不均衡になると、クラスター全体のリソースは十分であっても、特定のTiDBサーバーでリソース枯渇が発生し、レイテンシーが大幅に増加する可能性があります。この問題を解決するために、TiProxyは接続の動的移行機能を提供します。これにより、クライアントに影響を与えることなく、接続をあるTiDBサーバーから別のTiDBサーバーに移行できるため、TiDBクラスターの負荷分散が実現されます。

    TiProxyはTiUP、 TiDB Operator、およびTiDB Dashboardに統合されているため、設定、デプロイ、およびメンテナンスが容易です。

    詳細については、[ドキュメント](/tiproxy/tiproxy-overview.md)を参照してください。

### SQL {#sql}

-   大量のデータを処理するための新しいDMLタイプをサポート（実験的） [#50215](https://github.com/pingcap/tidb/issues/50215) @[ekexium](https://github.com/ekexium)

    バージョン8.0.0より前のTiDBでは、トランザクションデータをコミットする前にすべてメモリに格納していました。大量のデータを処理する場合、トランザクションに必要なメモリがボトルネックとなり、TiDBが処理できるトランザクションサイズが制限されていました。TiDBは、SQL文を分割することでトランザクションサイズの制限を解消しようと、非トランザクションDMLを導入しましたが、この機能には様々な制限があり、実際のシナリオでは理想的なエクスペリエンスを提供できませんでした。

    バージョン 8.0.0 以降、TiDB は大量のデータを処理するための DML タイプをサポートしています。この DML タイプは、実行中にデータを TiKV にタイムリーに書き込み、すべてのトランザクション データをメモリに継続的にストレージことを回避し、メモリ制限を超える大量のデータの処理をサポートします。この DML タイプはトランザクションの整合性を保証し、標準 DML と同じ構文を使用します。 `INSERT` 、 `UPDATE` 、 `REPLACE` 、および`DELETE`ステートメントは、この新しい DML タイプを使用して大規模な DML 操作を実行できます。

    この DML タイプは[パイプラインDML](https://github.com/pingcap/tidb/blob/release-8.0/docs/design/2024-01-09-pipelined-DML.md)機能によって実装され、自動コミットが有効になっているステートメントでのみ有効になります。この DML タイプを有効にするかどうかは、システム変数[`tidb_dml_type`](/system-variables.md#tidb_dml_type-new-in-v800)設定することで制御できます。

    詳細については、 [ドキュメント](/system-variables.md#tidb_dml_type-new-in-v800)を参照してください。

-   テーブル作成時に一部の式を使用してデフォルトの列値を設定できるようにサポート（実験的） [#50936](https://github.com/pingcap/tidb/issues/50936) @[zimulala](https://github.com/zimulala)

    バージョン8.0.0より前は、テーブルを作成する際に、列のデフォルト値は文字列、数値、日付に限定されていました。バージョン8.0.0以降では、いくつかの式を列のデフォルト値として使用できます。たとえば、列のデフォルト値を`UUID()`に設定できます。この機能により、より多様な要件に対応できます。

    詳細については、 [ドキュメント](/data-type-default-values.md#specify-expressions-as-default-values)を参照してください。

-   `div_precision_increment`システム変数 [#51501](https://github.com/pingcap/tidb/issues/51501)をサポートします @[yibin87](https://github.com/yibin87)

    MySQL 8.0 では、 `div_precision_increment`演算子を使用して実行される除算演算の結果の桁数を増やすことを指定する変数`/`がサポートされています。v8.0.0 より前の TiDB ではこの変数はサポートされておらず、除算は 4 桁の小数点以下で実行されます。v8.0.0 以降では、TiDB はこの変数をサポートしています。除算演算の結果の桁数を増やすことを必要に応じて指定できます。

    詳細については、 [ドキュメント](/system-variables.md#div_precision_increment-new-in-v800)を参照してください。

### データベース操作 {#db-operations}

-   PITR は Amazon S3 オブジェクト ロック [#51184](https://github.com/pingcap/tidb/issues/51184) @[RidRisR](https://github.com/RidRisR)をサポートします

    Amazon S3 オブジェクトロックを使用すると、指定された保持期間中にバックアップデータが誤ってまたは意図的に削除されるのを防ぎ、データのセキュリティと整合性を強化できます。バージョン 6.3.0 以降、 BR はスナップショットバックアップで Amazon S3 オブジェクトロックをサポートし、フルバックアップにセキュリティレイヤーを追加します。バージョン 8.0.0 以降、PITR も Amazon S3 オブジェクトロックをサポートします。フルバックアップでもログデータバックアップでも、オブジェクトロック機能はより信頼性の高いデータ保護を保証し、データバックアップとリカバリのセキュリティをさらに強化し、規制要件を満たします。

    詳細については、 [ドキュメント](/br/backup-and-restore-ストレージs.md#other-features-supported-by-the-ストレージ-service)を参照してください。

-   セッションレベルで非表示のインデックスを可視化する機能のサポート [#50653](https://github.com/pingcap/tidb/issues/50653) @[hawkingrei](https://github.com/hawkingrei)

    デフォルトでは、オプティマイザは[目に見えないインデックス](/sql-statements/sql-statement-create-index.md#invisible-index)表示 を選択しません。このメカニズムは通常、インデックスを削除するかどうかを評価するために使用されます。インデックスを削除した場合のパフォーマンスへの影響が不明な場合は、インデックスを一時的に非表示に設定し、必要に応じてすぐに表示に戻すことができます。

    バージョン8.0.0以降では、セッションレベルのシステム変数[`tidb_opt_use_invisible_indexes`](/system-variables.md#tidb_opt_use_invisible_indexes-new-in-v800) `ON`に設定することで、現在のセッションで非表示インデックスを認識させることができます。この機能を使用すると、新しいインデックスを作成し、最初にインデックスを可視化してから、現在のセッションのシステム変数を変更してテストすることで、他のセッションに影響を与えることなくパフォーマンスをテストできます。この改善により、SQLチューニングの安全性が向上し、本番データベースの安定性も向上します。

    詳細については、 [ドキュメント](/sql-statements/sql-statement-create-index.md#invisible-index)を参照してください。

-   一般ログの別ファイルへの書き込みをサポート [#51248](https://github.com/pingcap/tidb/issues/51248) @[Defined2014](https://github.com/Defined2014)

    一般ログは、MySQL互換の機能で、実行されたすべてのSQLステートメントをログに記録し、問題の診断に役立ちます。TiDBもこの機能をサポートしています。変数[`tidb_general_log`](/system-variables.md#tidb_general_log)設定することで有効にできます。ただし、以前のバージョンでは、一般ログの内容は他の情報とともにTiDBインスタンスログにしか書き込まれず、ログを長期間保持する必要があるユーザーにとっては不便でした。

    バージョン8.0.0以降では、設定項目[`log.general-log-file`](/tidb-configuration-file.md#general-log-file-new-in-v800)に有効なファイル名を設定することで、一般ログを指定したファイルに書き込むことができます。一般ログは、インスタンスログと同じローテーションおよび保持ポリシーに従います。

    さらに、履歴ログファイルが占めるディスク容量を削減するため、TiDB v8.0.0 ではネイティブのログ圧縮オプションが導入されました。設定項目[`log.file.compression`](/tidb-configuration-file.md#compression-new-in-v800) `gzip`に設定すると、ローテーションされたログが[`gzip`](https://www.gzip.org/)形式で自動的に圧縮されます。

    詳細については、 [ドキュメント](/tidb-configuration-file.md#general-log-file-new-in-v800)を参照してください。

### 可観測性 {#observability}

-   監視インデックスの使用統計をサポートする [#49830](https://github.com/pingcap/tidb/issues/49830) @[YangKeao](https://github.com/YangKeao)

    適切なインデックス設計は、データベースのパフォーマンスを維持するための重要な前提条件です。TiDB v8.0.0 では、現在の TiDB ノード上のすべてのインデックスの統計情報を記録する[`INFORMATION_SCHEMA.TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md)テーブルが導入されました。このテーブルには、以下の情報が含まれます。

    -   インデックスをスキャンするステートメントの累積実行回数
    -   インデックスにアクセスした際にスキャンされた行の総数
    -   インデックスをスキャンしたときの選択性分布
    -   インデックスへの最終アクセス時刻

    この情報を用いることで、オプティマイザで使用されていないインデックスや選択性の低いインデックスを特定し、インデックス設計を最適化することでデータベースのパフォーマンスを向上させることができます。

    さらに、TiDB v8.0.0 では MySQL と互換性のあるビュー[`sys.schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md)が導入されました。このビューには、TiDB インスタンスの最後の起動以降に使用されていないインデックスが表示されます。v8.0.0 より前のバージョンからアップグレードされたクラスターの場合、 `sys`スキーマとビューは自動的に作成されません[`sys.schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md#manually-create-the-schema_unused_indexes-view)を参照して手動で作成できます。

    詳細については、 [ドキュメント](/information-schema/information-schema-tidb-index-usage.md)を参照してください。

### Security {#security}

-   TiKV 保存時の暗号化は Google [キー管理サービス（クラウドKMS）](https://cloud.google.com/docs/security/key-management-deep-dive?hl)をサポートします (実験的) [#8906](https://github.com/tikv/tikv/issues/8906) @[glorv](https://github.com/glorv)

    TiKVは、保存データの暗号化技術を用いてデータのセキュリティを確保します。セキュリティのための保存データ暗号化の中核となるのは鍵管理です。バージョン8.0.0以降では、Google Cloud KMSを使用してTiKVのマスターキーを管理し、Cloud KMSに基づいた保存データ暗号化機能を確立することで、ユーザーデータのセキュリティを強化できます。

    Google Cloud KMS に基づく保存時の暗号化を有効にするには、Google Cloud でキーを作成し、TiKV 構成ファイルの`[security.encryption.master-key]`セクションを構成する必要があります。

    詳細については、 [ドキュメント](/encryption-at-rest.md#tikv-encryption-at-rest)を参照してください。

-   TiDBログの非機密化機能を強化する [#51306](https://github.com/pingcap/tidb/issues/51306) @[xhebox](https://github.com/xhebox)

    TiDBログの機密性低減機能の強化は、ログファイル内のSQLテキスト情報をマークすることで、ユーザーがログを表示する際に機密データを安全に表示できるようにするものです。ログ情報の機密性低減を制御できるため、さまざまなシナリオでTiDBログを安全に使用でき、ログの機密性低減のセキュリティと柔軟性が向上します。この機能を使用するには、システム変数`tidb_redact_log`を`MARKER`に設定します。これにより、TiDBログ内のSQLテキストがマークされます。ログを表示すると、機密データはマーカーに基づいて安全に表示され、ログ情報が保護されます。

    詳細については、[ドキュメント](/system-variables.md#tidb_redact_log)を参照してください。

### データ移行 {#data-migration}

-   TiCDC は、Simple プロトコル [#9898](https://github.com/pingcap/tiflow/issues/9898) @[3AceShowHand](https://github.com/3AceShowHand)のサポートを追加します

    TiCDCは、新しいプロトコルであるSimpleプロトコルを導入しました。このプロトコルは、DDLおよびBOOTSTRAPイベントにテーブルスキーマ情報を埋め込むことで、インバンドスキーマ追跡機能を提供します。

    詳細については、[ドキュメント](/ticdc/ticdc-simple-protocol.md)を参照してください。

-   TiCDC が Debezium 形式プロトコルのサポートを追加 [#1799](https://github.com/pingcap/tiflow/issues/1799) @[breezewish](https://github.com/breezewish)

    TiCDCは、Debeziumスタイルの形式でイベントメッセージを生成するプロトコルを使用して、データ変更イベントをKafkaシンクに発行できるようになりました。これにより、現在Debeziumを使用してMySQLからデータを取得し、下流処理に利用しているユーザーにとって、MySQLからTiDBへの移行が簡素化されます。

    詳細については、[ドキュメント](/ticdc/ticdc-debezium.md)を参照してください。

-   DMは、ソースデータベースとターゲットデータベースのパスワードを暗号化および復号化するために、ユーザーが提供する秘密鍵の使用をサポートします [#9492](https://github.com/pingcap/tiflow/issues/9492) @[D3Hunter](https://github.com/D3Hunter)

    以前のバージョンでは、DMはセキュリティレベルが比較的低い固定の秘密鍵を内蔵していました。バージョン8.0.0以降では、アップストリームおよびダウンストリームデータベースのパスワードの暗号化と復号化に使用する秘密鍵ファイルをアップロードして指定できるようになりました。さらに、必要に応じて秘密鍵ファイルを置き換えることで、データセキュリティを強化できます。

    詳細については、[ドキュメント](/dm/dm-customized-secret-key.md)を参照してください。

-   `IMPORT INTO ... FROM SELECT`の機能を拡張するために`IMPORT INTO`構文をサポートします (実験的) [#49883](https://github.com/pingcap/tidb/issues/49883) @[D3Hunter](https://github.com/D3Hunter)

    以前の TiDB バージョンでは、クエリ結果をターゲット テーブルにインポートするには`INSERT INTO ... SELECT`ステートメントを使用するしかなく、大規模なデータセットのシナリオでは効率が悪かった。v8.0.0 以降では、TiDB で`IMPORT INTO ... FROM SELECT`を使用して`SELECT`クエリの結果を空の TiDB ターゲット テーブルにインポートできるようになり、 `INSERT INTO ... SELECT`の最大 8 倍のパフォーマンスを実現し、インポート時間を大幅に短縮できる。

    さらに、 `IMPORT INTO ... FROM SELECT`を使用して、 [`AS OF TIMESTAMP`](/as-of-timestamp.md)でクエリされた履歴データをインポートできます。

    詳細については、 [ドキュメント](/sql-statements/sql-statement-import-into.md)を参照してください。

-   TiDB Lightning は競合解決戦略を簡素化し、 `replace`戦略を使用した競合データの処理をサポートします (実験的) [#51036](https://github.com/pingcap/tidb/issues/51036) @[lyzx2001](https://github.com/lyzx2001)

    以前のバージョンでは、 TiDB Lightning には論理インポート モード用の[データ競合解決戦略](/tidb-lightning/tidb-lightning-logical-import-mode-usage.md#conflict-detection)と物理インポート モード用の[2つのデータ競合解決戦略](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#conflict-detection)ありましたが、これらは理解して設定するのが簡単ではありませんでした。

    バージョン 8.0.0 以降、 TiDB Lightning は[旧バージョンの競合検出](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#the-old-version-of-conflict-detection-deprecated-in-v800)物理インポートモードの戦略を非推奨とし、 [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md)パラメータを使用して論理インポートモードと物理インポートモードの両方の競合検出戦略を制御できるようにし、このパラメータの設定を簡素化しました。さらに、物理インポートモードでは、 `replace`戦略が、インポート時に主キーまたは一意キーの競合があるデータが検出された場合、最新のデータを保持して古いデータを上書きすることをサポートするようになりました。

    詳細については、 [ドキュメント](/tidb-lightning/tidb-lightning-configuration.md)を参照してください。

-   グローバルソートが一般提供開始（GA）となり、 `IMPORT INTO`のパフォーマンスと安定性が大幅に向上しました [#45719](https://github.com/pingcap/tidb/issues/45719) @[lance6716](https://github.com/lance6716)

    バージョン7.4.0より前では、[分散実行フレームワーク（DXF）](/tidb-distributed-execution-framework.md)を使用して`IMPORT INTO`タスクを実行すると、ローカルストレージ容量が限られているため、TiDBはデータの一部をローカルでソートしてからTiKVにインポートしていました。このため、TiKVにインポートされたデータにかなりの重複が生じ、インポート中にTiKVが追加の圧縮操作を実行する必要が生じ、TiKVのパフォーマンスと安定性に影響が出ていました。

    v7.4.0 で導入された実験的機能であるグローバル ソートを使用すると、TiDB はインポートするデータを TiKV にインポートする前に、グローバル ソートのために一時的に外部ストレージ(Amazon S3 など) に保存できます。これにより、インポート中の TiKV 圧縮操作が不要になります。v8.0.0 では、グローバル ソートが GA になります。この機能により、TiKV のリソース消費が削減され、 `IMPORT INTO`のパフォーマンスと安定性が大幅に向上します。グローバル ソートを有効にすると、各`IMPORT INTO`タスクは 40 TiB 以内のデータのインポートをサポートします。

    詳細については、[ドキュメント](/tidb-global-sort.md)を参照してください。

## 互換性の変更 {#compatibility-changes}

> **注記：**
>
> このセクションでは、バージョン7.6.0から最新バージョン（8.0.0）にアップグレードする際に知っておくべき互換性の変更点について説明します。バージョン7.5.0以前のバージョンから最新バージョンにアップグレードする場合は、中間バージョンで導入された互換性の変更点も確認する必要があるかもしれません。

-   TiUPによってデフォルトでデプロイされているPrometheusのバージョンを2.27.1から2.49.1にアップグレードします。
-   TiUPによってデプロイされたデフォルトのGrafanaバージョンを7.5.11から7.5.17にアップグレードします。
-   GAではないがデフォルトで有効になっている証人関連のスケジューラを削除する [#7765](https://github.com/tikv/pd/pull/7765) @[rleungx](https://github.com/rleungx)

### 行動の変化 {#behavior-changes}

-   Security強化モード（SEM）で[`require_secure_transport`](/system-variables.md#require_secure_transport-new-in-v610) `ON`に設定することを禁止し、ユーザーの接続に関する潜在的な問題を防止します。 [#47665](https://github.com/pingcap/tidb/issues/47665) @[tiancaiamao](https://github.com/tiancaiamao)
-   DM では、暗号化および復号化用の固定秘密キーが削除され、暗号化および復号化用の秘密キーをカスタマイズできるようになります。アップグレード前に[データソース構成](/dm/dm-source-configuration-file.md)と[移行タスクの設定](/dm/task-configuration-file-full.md)で暗号化されたパスワードが使用されている場合、追加の操作については[DMの暗号化と復号化のための秘密鍵をカスタマイズする](/dm/dm-customized-secret-key.md)のアップグレード手順を参照する必要があります。 [#9492](https://github.com/pingcap/tiflow/issues/9492) @[D3Hunter](https://github.com/D3Hunter)
-   v8.0.0 より前では、 `ADD INDEX`および`CREATE INDEX` ( `tidb_ddl_enable_fast_reorg = ON` ) の高速化を有効にした後、エンコードされたインデックス キーは、下流の TiKV 容量に応じて動的に調整できない固定の同時実行数`16`で TiKV にデータを取り込みます。v8.0.0 以降では、 [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt)システム変数を使用して同時実行数を調整できます。デフォルト値は`4`です。以前のデフォルト値`16`と比較すると、新しいデフォルト値では、インデックス付きキーと値のペアを取り込むときのパフォーマンスが低下します。このシステム変数は、クラスターのワークロードに基づいて調整できます。

### MySQLとの互換性 {#mysql-compatibility}

-   `KEY`パーティションタイプは、パーティションフィールドのリストが空であるステートメントをサポートしており、これは MySQL の動作と一致しています。

### システム変数 {#system-variables}

| 変数名                                                                                                                       | 種類を変更する  | 説明                                                                                                                                                                                                                         |
| ------------------------------------------------------------------------------------------------------------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`tidb_disable_txn_auto_retry`](/system-variables.md#tidb_disable_txn_auto_retry)                                         | 非推奨      | バージョン8.0.0以降、このシステム変数は非推奨となり、TiDBは楽観的トランザクションの自動再試行をサポートしなくなりました。[悲観的なトランザクションモード](/pessimistic-transaction.md)使用をお勧めします。楽観的トランザクションの競合が発生した場合は、エラーを捕捉してアプリケーションでトランザクションを再試行できます。                                               |
| `tidb_ddl_version`                                                                                                        | 名称変更     | TiDB DDL V2 を有効にするかどうかを制御します。バージョン 8.0.0 以降、この変数は目的をより明確にするために[`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-new-in-v800)に名称変更されました。                                                 |
| [`tidb_enable_collect_execution_info`](/system-variables.md#tidb_enable_collect_execution_info)                           | 修正済み     | [インデックスの使用統計](/information-schema/information-schema-tidb-index-usage.md)を記録するかどうかのコントロールを追加します。デフォルト値は`ON`です。                                                                                                             |
| [`tidb_redact_log`](/system-variables.md#tidb_redact_log)                                                                 | 修正済み     | TiDB ログおよびスロー ログを記録する際に、SAL テキスト内のユーザー情報をどのように処理するかを制御します。値のオプションは`OFF` (ログ内のユーザー情報を処理しないことを示す) と`ON` (ログ内のユーザー情報を非表示にすることを示す) です。ログ内のユーザー情報をより詳細に処理できるように、v8.0.0 ではログ情報をマークするための`MARKER`オプションが追加されました。                    |
| [`div_precision_increment`](/system-variables.md#div_precision_increment-new-in-v800)                                     | 新しく追加された | `/`演算子を使用して実行される除算演算の結果の桁数を増やすかどうかを制御します。この変数はMySQLと同じです。                                                                                                                                                                  |
| [`tidb_dml_type`](/system-variables.md#tidb_dml_type-new-in-v800)                                                         | 新しく追加された | DML ステートメントの実行モードを制御します。値のオプションは`"standard"`と`"bulk"`です。                                                                                                                                                                   |
| [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-new-in-v800)     | 新しく追加された | 統計情報の自動収集タスクをスケジュールするための優先度キューを有効にするかどうかを制御します。この変数を有効にすると、TiDB は統計情報を最も必要とするテーブルの統計情報の収集を優先します。                                                                                                                           |
| [`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-new-in-v800)               | 新しく追加された | TiDBが並列HashAggアルゴリズムでディスクスピルをサポートするかどうかを制御します。 `ON`の場合、並列HashAggアルゴリズムでディスクスピルがトリガーされます。この機能が将来のリリースで一般提供されるようになったら、この変数は非推奨になります。                                                                                         |
| [`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-new-in-v800)                         | 新しく追加された | [TiDBがテーブル作成を高速化](/accelerated-table-creation.md)機能を有効にするかどうかを制御します。有効にするには`ON`に、無効にするには`OFF`に設定します。デフォルト値は`ON`です。この変数が有効になっている場合、TiDB は[`CREATE TABLE`](/sql-statements/sql-statement-create-table.md)を使用してテーブル作成を高速化します。 |
| [`tidb_load_binding_timeout`](/system-variables.md#tidb_load_binding_timeout-new-in-v800)                                 | 新しく追加された | バインディングの読み込みタイムアウトを制御します。バインディングの読み込み実行時間がこの値を超えると、読み込みが停止します。                                                                                                                                                             |
| [`tidb_low_resolution_tso_update_interval`](/system-variables.md#tidb_low_resolution_tso_update_interval-new-in-v800)     | 新しく追加された | TiDB [キャッシュタイムスタンプ](/system-variables.md#tidb_low_resolution_tso)スタンプを更新する間隔を制御します。                                                                                                                                        |
| [`tidb_opt_ordering_index_selectivity_ratio`](/system-variables.md#tidb_opt_ordering_index_selectivity_ratio-new-in-v800) | 新しく追加された | SQL ステートメントに`ORDER BY`および`ORDER BY` } 句が存在するものの、インデックスでカバーされていないフィルタ条件がある場合に、SQL ステートメント`LIMIT`に一致するインデックスの推定行数を制御します。デフォルト値は`-1`で、このシステム変数を無効にすることを意味します。                                                                 |
| [`tidb_opt_use_invisible_indexes`](/system-variables.md#tidb_opt_use_invisible_indexes-new-in-v800)                       | 新しく追加された | オプティマイザーが現在のセッションでクエリ最適化のために[目に見えないインデックス](/sql-statements/sql-statement-create-index.md#invisible-index)を選択できるかどうかを制御します。変数が`ON`に設定されている場合、オプティマイザーはセッション内のクエリ最適化のために非表示のインデックスを選択できます。                                   |
| [`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-new-in-v800)                                       | 新しく追加された | スキーマ情報のキャッシュに使用できるメモリの上限を制御し、メモリの過剰使用を防ぎます。この機能を有効にすると、LRUアルゴリズムを使用して必要なテーブルをキャッシュし、スキーマ情報によって占有されるメモリを効果的に削減します。                                                                                                          |

### 設定ファイルパラメータ {#configuration-file-parameters}

| 設定ファイル | 設定パラメータ                                                                                                                                               | 種類を変更する  | 説明                                                                                                                                                                                                          |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB           | [`instance.tidb_enable_collect_execution_info`](/tidb-configuration-file.md#tidb_enable_collect_execution_info)                                               | 修正済み     | [インデックスの使用統計](/information-schema/information-schema-tidb-index-usage.md)を記録するかどうかのコントロールを追加します。デフォルト値は`true`です。                                                                                            |
| TiDB           | [`tls-version`](/tidb-configuration-file.md#tls-version)                                                                                                      | 修正済み     | このパラメータは`"TLSv1.0"`と`"TLSv1.1"`をサポートしなくなりました。現在は`"TLSv1.2"`と`"TLSv1.3"`のみをサポートしています。                                                                                                                        |
| TiDB           | [`log.file.compression`](/tidb-configuration-file.md#compression-new-in-v800)                                                                                 | 新しく追加された | ポーリングログの圧縮形式を指定します。デフォルト値はnullで、これはポーリングログが圧縮されないことを意味します。                                                                                                                                                  |
| TiDB           | [`log.general-log-file`](/tidb-configuration-file.md#general-log-file-new-in-v800)                                                                            | 新しく追加された | 一般ログを保存するファイルを指定します。デフォルト値はnullで、これは一般ログがインスタンスファイルに書き込まれることを意味します。                                                                                                                                         |
| TiDB           | [`tikv-client.enable-replica-selector-v2`](/tidb-configuration-file.md#enable-replica-selector-v2-new-in-v800)                                                | 新しく追加された | TiKV に RPC リクエストを送信する際に、リージョンレプリカセレクターの新しいバージョンを使用するかどうかを制御します。デフォルト値は`true`です。                                                                                                                             |
| TiKV           | [`log-backup.initial-scan-rate-limit`](/tikv-configuration-file.md#initial-scan-rate-limit-new-in-v620)                                                       | 修正済み     | 最小値として`1MiB`の制限を追加します。                                                                                                                                                                                      |
| TiKV           | [`raftstore.store-io-pool-size`](/tikv-configuration-file.md#store-io-pool-size-new-in-v530)                                                                  | 修正済み     | TiKV のパフォーマンスを向上させるため、デフォルト値を`0`から`1`に変更します。つまり、StoreWriter スレッド プールのサイズはデフォルトで`1`になります。                                                                                                                    |
| TiKV           | [`rocksdb.defaultcf.titan.blob-cache-size`](/tikv-configuration-file.md#blob-cache-size)                                                                      | 修正済み     | バージョン8.0.0以降、TiKVは`shared-blob-cache`設定項目を導入し、デフォルトで有効にしているため、 `blob-cache-size`を別途設定する必要はありません。 `blob-cache-size`の設定は、 `shared-blob-cache`が`false`に設定されている場合にのみ有効になります。                                    |
| TiKV           | [`rocksdb.titan.max-background-gc`](/tikv-configuration-file.md#max-background-gc)                                                                            | 修正済み     | Titan GC プロセスによるスレッド リソースの占有を減らすため、デフォルト値を`4`から`1`に変更します。                                                                                                                                                   |
| TiKV           | [`security.encryption.master-key.vendor`](/encryption-at-rest.md#specify-a-master-key-via-kms)                                                                | 修正済み     | サービスプロバイダで使用可能なタイプとして`gcp`を追加します。                                                                                                                                                                           |
| TiKV           | [`ストレージ.block-cache.low-pri-pool-ratio`](/tikv-configuration-file.md#low-pri-pool-ratio-new-in-v800)                                                        | 新しく追加された | Titanコンポーネントが使用できるブロックキャッシュ全体の割合を指定します。デフォルト値は`0.2`です。                                                                                                                                                      |
| TiKV           | [`rocksdb.defaultcf.titan.shared-blob-cache`](/tikv-configuration-file.md#shared-blob-cache-new-in-v800)                                                      | 新しく追加された | Titan blob ファイルと RocksDB ブロックファイルの共有キャッシュを有効にするかどうかを制御します。デフォルト値は`true`です。                                                                                                                                  |
| TiKV           | [`security.encryption.master-key.gcp.credential-file-path`](/encryption-at-rest.md#specify-a-master-key-via-kms)                                              | 新しく追加された | `security.encryption.master-key.vendor`が`gcp`の場合に、Google Cloud 認証情報ファイルへのパスを指定します。                                                                                                                          |
| PD             | [`schedule.enable-heartbeat-breakdown-metrics`](/pd-configuration-file.md#enable-heartbeat-breakdown-metrics-new-in-v800)                                     | 新しく追加された | リージョンハートビートの内訳メトリクスを有効にするかどうかを制御します。これらのメトリクスは、リージョンハートビート処理の各段階で消費された時間を測定し、監視による分析を容易にします。デフォルト値は`true`です。                                                                                                |
| PD             | [`schedule.enable-heartbeat-concurrent-runner`](/pd-configuration-file.md#enable-heartbeat-concurrent-runner-new-in-v800)                                     | 新しく追加された | リージョンハートビートの非同期同時処理を有効にするかどうかを制御します。有効にすると、独立したエグゼキュータがリージョンハートビート要求を非同期かつ同時に処理し、ハートビート処理のスループットを向上させ、レイテンシーを削減できます。デフォルト値は`true`です。                                                                        |
| TiDB Lightning | [`tikv-importer.duplicate-resolution`](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#the-old-version-of-conflict-detection-deprecated-in-v800) | 非推奨      | 物理インポートモードで一意キーの競合を検出して解決するかどうかを制御します。v8.0.0以降は[`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)に置き換えられています。                                                       |
| TiDB Lightning | [`conflict.precheck-conflict-before-import`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)                                             | 新しく追加された | TiDB にデータをインポートする前にデータの競合をチェックする、インポート前の競合検出を有効にするかどうかを制御します。このパラメータのデフォルト値は`false`で、これはTiDB Lightning がデータのインポート後にのみ競合をチェックすることを意味します。このパラメータは、物理インポートモード ( `tikv-importer.backend = "local"` ) でのみ使用できます。 |
| TiDB Lightning | [`logical-import-batch-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)                                                            | 新しく追加された | 論理インポートモードでトランザクションごとに挿入される行の最大数を制御します。デフォルト値は`65536`行です。                                                                                                                                                   |
| TiDB Lightning | [`logical-import-batch-size`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)                                                            | 新しく追加された | 論理インポートモードでダウンストリームのTiDBサーバー上で実行される各SQLクエリの最大サイズを制御します。デフォルト値は`"96KiB"`です。単位はKB、KiB、MB、またはMiBです。                                                                                                            |
| データ移行          | [`secret-key-path`](/dm/dm-master-configuration-file.md)                                                                                                      | 新しく追加された | 上流および下流のパスワードの暗号化と復号化に使用される秘密鍵のファイルパスを指定します。ファイルには、64文字の16進数AES-256秘密鍵が含まれている必要があります。                                                                                                                       |
| TiCDC          | [`debezium-disable-schema`](/ticdc/ticdc-changefeed-config.md)                                                                                                | 新しく追加された | スキーマ情報の出力を無効にするかどうかを制御します。このパラメータは、シンクタイプがMQで、出力プロトコルがDebeziumの場合にのみ有効です。                                                                                                                                   |
| TiCDC          | [`tls-certificate-file`](/ticdc/ticdc-sink-to-pulsar.md)                                                                                                      | 新しく追加された | クライアント上の暗号化証明書ファイルへのパスを指定します。これは、PulsarがTLS暗号化通信を有効にする場合に必要です。                                                                                                                                              |
| TiCDC          | [`tls-key-file-path`](/ticdc/ticdc-sink-to-pulsar.md)                                                                                                         | 新しく追加された | クライアント上の暗号化された秘密鍵へのパスを指定します。これは、PulsarがTLS暗号化通信を有効にする場合に必要となります。                                                                                                                                            |

### システムテーブル {#system-tables}

-   TiDBノード上のインデックス使用統計を記録するために、新しいシステムテーブル[`INFORMATION_SCHEMA.TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md)と[`INFORMATION_SCHEMA.CLUSTER_TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md#cluster_tidb_index_usage)を追加します。
-   新しいシステムスキーマ[`sys`](/sys-schema/sys-schema.md)と、TiDB の前回の起動以降に使用されていないインデックスを記録する新しいビュー[`sys.schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md)を追加します。

## 非推奨機能 {#deprecated-features}

-   バージョン8.0.0以降、 [`tidb_disable_txn_auto_retry`](/system-variables.md#tidb_disable_txn_auto_retry)システム変数は非推奨となり、TiDBは楽観的トランザクションの自動再試行をサポートしなくなりました。代替策として、楽観的トランザクションの競合が発生した場合は、エラーを捕捉してアプリケーションでトランザクションを再試行するか、[悲観的なトランザクションモード](/pessimistic-transaction.md)を使用してください。
-   バージョン8.0.0以降、TiDBはTLSv1.0およびTLSv1.1プロトコルをサポートしなくなりました。TLSをTLSv1.2またはTLSv1.3にアップグレードする必要があります。
-   バージョン8.0.0以降、 TiDB Lightningは[旧バージョンの競合検出](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#the-old-version-of-conflict-detection-deprecated-in-v800)戦略を非推奨とし、 [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md)パラメータを使用して論理インポートモードと物理インポートモードの両方の競合検出戦略を制御できるようにします。旧バージョンの競合検出の[`duplicate-resolution`](/tidb-lightning/tidb-lightning-configuration.md)パラメータは、今後のリリースで削除されます。
-   今後のリリースでは [実行プランバインディングの自動進化](/sql-plan-management.md#baseline-evolution)が再設計される予定であり、関連する変数や動作が変更される予定です。

## 改善点 {#improvements}

-   TiDB

    -   `CREATE TABLE` DDL ステートメントの実行パフォーマンスを 10 倍向上させ、線形スケーラビリティをサポート [#50052](https://github.com/pingcap/tidb/issues/50052) @[GMHDBJD](https://github.com/GMHDBJD)
    -   16個の`IMPORT INTO ... FROM FILE`タスクを同時に送信することをサポートし、ターゲットテーブルへの大量データインポートを容易にし、データファイルのインポートの効率とパフォーマンスを大幅に向上させます [#49008](https://github.com/pingcap/tidb/issues/49008) @[D3Hunter](https://github.com/D3Hunter)
    -   `Sort`オペレーターのディスクへのデータスピル処理のパフォーマンスを改善 [#47733](https://github.com/pingcap/tidb/issues/47733) @[xzhangxian1008](https://github.com/xzhangxian1008)
    -   ディスクへのデータ流出中にクエリをキャンセルする機能をサポートし、データ流出機能の終了メカニズムを最適化します [#50511](https://github.com/pingcap/tidb/issues/50511) @[wshwsh12](https://github.com/wshwsh12)
    -   複数の等しい条件を持つテーブル結合クエリを処理する際に、部分条件に一致するインデックスを使用してインデックス結合を構築することをサポートする [#47233](https://github.com/pingcap/tidb/issues/47233) @[winoros](https://github.com/winoros)
    -   クエリ内のソート要件を識別し、ソート要件を満たすインデックスを選択するインデックスマージ機能を強化します [#48359](https://github.com/pingcap/tidb/issues/48359) @[AilinKid](https://github.com/AilinKid)
    -   `Apply`演算子が同時に実行されない場合、TiDB では`SHOW WARNINGS`実行することで、同時実行をブロックしている演算子の名前を表示できます。 [#50256](https://github.com/pingcap/tidb/issues/50256) @[hawkingrei](https://github.com/hawkingrei)
    -   `point get`クエリがすべてのインデックスでサポートされている場合に、クエリに最適なインデックスを選択することで`point get`クエリのインデックス選択を最適化します。 [#50184](https://github.com/pingcap/tidb/issues/50184) @[elsa0520](https://github.com/elsa0520)
    -   TiKVの負荷が高い時に広範囲にわたるタイムアウトが発生するのを避けるため、統計情報を同期的にロードするタスクの優先度を一時的に「高」に調整します。タイムアウトが発生すると、統計情報がロードされない可能性があります。 [#50332](https://github.com/pingcap/tidb/issues/50332) @[winoros](https://github.com/winoros)
    -   `PREPARE`ステートメントが実行プランキャッシュにヒットしなかった場合、TiDB では`SHOW WARNINGS`を実行することで理由を確認できます。 [#50407](https://github.com/pingcap/tidb/issues/50407) @[hawkingrei](https://github.com/hawkingrei)
    -   同じデータ行が複数回更新された場合のクエリ推定情報の精度を向上させる [#47523](https://github.com/pingcap/tidb/issues/47523) @[terry1purcell](https://github.com/terry1purcell)
    -   インデックスマージは、 `OR`述語への複数値インデックスと`AND`演算子の埋め込みをサポートします [#51778](https://github.com/pingcap/tidb/issues/51778) @[time-and-fate](https://github.com/time-and-fate)
    -   `force-init-stats` `true`に設定すると、TiDB は TiDB 起動中にサービスを提供する前に統計情報の初期化が完了するまで待機します。この設定により HTTP サーバーの起動がブロックされなくなり、ユーザーは引き続き監視できるようになります [#50854](https://github.com/pingcap/tidb/issues/50854) @[hawkingrei](https://github.com/hawkingrei)
    -   MemoryTrackerは`IndexLookup`演算子 [#45901](https://github.com/pingcap/tidb/issues/45901) @[solotzg](https://github.com/solotzg)のメモリ使用量を追跡できます
    -   MemoryTracker は`MemTableReaderExec`オペレーター [#51456](https://github.com/pingcap/tidb/issues/51456) @[wshwsh12](https://github.com/wshwsh12)のメモリ使用量を追跡できます
    -   大規模テーブルをクエリする際に、PD からリージョンをバッチでロードして KV 範囲からリージョンへの変換プロセスを高速化するサポート [#51326](https://github.com/pingcap/tidb/issues/51326) @[SeaRise](https://github.com/SeaRise)
    -   システムテーブル`INFORMATION_SCHEMA.TABLES` 、 `INFORMATION_SCHEMA.STATISTICS` 、 `INFORMATION_SCHEMA.KEY_COLUMN_USAGE` 、および`INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS`パフォーマンスを最適化しました。以前のバージョンと比較して、パフォーマンスが最大 100 倍向上しています。 [#50305](https://github.com/pingcap/tidb/issues/50305) @[ywqzzy](https://github.com/ywqzzy)

-   TiKV

    -   構成や操作が不適切な場合のクラスターTSOの堅牢性を向上させるため、TSOの検証と検出機能を強化する [#16545](https://github.com/tikv/tikv/issues/16545) @[cfzjywxk](https://github.com/cfzjywxk)
    -   未コミットトランザクションの処理パフォーマンスを向上させるため、悲観的ロックのクリーンアップロジックを最適化する [#16158](https://github.com/tikv/tikv/issues/16158) @[cfzjywxk](https://github.com/cfzjywxk)
    -   TiKV の統一ヘルス制御を導入し、異常な単一の TiKV ノードがクラスター アクセス パフォーマンスに与える影響を軽減します。この最適化は、 [`tikv-client.enable-replica-selector-v2`](/tidb-configuration-file.md#enable-replica-selector-v2-new-in-v800)を`false`に設定することで無効にできます。 [#16297](https://github.com/tikv/tikv/issues/16297) [#1104](https://github.com/tikv/client-go/issues/1104) [#1167](https://github.com/tikv/client-go/issues/1167) @[MyonKeminta](https://github.com/MyonKeminta)@[zyguan](https://github.com/zyguan)@[crazycs520](https://github.com/crazycs520)
    -   PDクライアントはメタデータストレージインターフェースを使用して、以前のグローバル構成インターフェースを置き換えます [#14484](https://github.com/tikv/tikv/issues/14484) @[HuSharp](https://github.com/HuSharp)
    -   cf stats の書き込みによるデータ読み込み動作の判定により、スキャン性能を向上させる [#16245](https://github.com/tikv/tikv/issues/16245) @[Connor1996](https://github.com/Connor1996)
    -   Raft設定変更プロセス中にノードが削除され、投票者が降格された最新のハートビートをチェックして、この動作によってリージョンにアクセスできなくなることがないようにしてください [#15799](https://github.com/tikv/tikv/issues/15799) @[tonyxuqqi](https://github.com/tonyxuqqi)
    -   パイプラインDML用のFlushおよびBufferBatchGetインターフェースを追加 [#16291](https://github.com/tikv/tikv/issues/16291) @[ekexium](https://github.com/ekexium)
    -   cgroupのCPUとメモリ制限の監視とアラート機能を追加 [#16392](https://github.com/tikv/tikv/issues/16392) @[pingandb](https://github.com/pingandb)
    -   リージョンワーカーとスナップショット生成ワーカーのCPU監視機能を追加 [#16562](https://github.com/tikv/tikv/issues/16562) @[Connor1996](https://github.com/Connor1996)
    -   ピアおよびストアメッセージの低速ログを追加 [#16600](https://github.com/tikv/tikv/issues/16600) @[Connor1996](https://github.com/Connor1996)

-   PD

    -   PD クライアントのサービス検出機能を強化して、高可用性と負荷分散を向上させます [#7576](https://github.com/tikv/pd/issues/7576) @[CabinfeverB](https://github.com/CabinfeverB)
    -   PDクライアントの再試行メカニズムを強化する [#7673](https://github.com/tikv/pd/issues/7673) @[JmPotato](https://github.com/JmPotato)
    -   cgroupのCPUとメモリ制限の監視とアラート機能を追加[#7716](https://github.com/tikv/pd/issues/7716) [#7918](https://github.com/tikv/pd/issues/7918) @[pingandb](https://github.com/pingandb) @[rleungx](https://github.com/rleungx)
    -   etcd ウォッチ使用時のパフォーマンスと高可用性を向上させる[#7738](https://github.com/tikv/pd/issues/7738) [#7724](https://github.com/tikv/pd/issues/7724) [#7689](https://github.com/tikv/pd/issues/7689) @[lhy1024](https://github.com/lhy1024)
    -   パフォーマンスのボトルネックをより適切に分析するために、ハートビートの監視メトリクスを追加します [#7868](https://github.com/tikv/pd/issues/7868) @[nolouch](https://github.com/nolouch)
    -   etcdリーダーがPDリーダーに与える影響を軽減する [#7499](https://github.com/tikv/pd/issues/7499) @[JmPotato](https://github.com/JmPotato) @[HuSharp](https://github.com/HuSharp)
    -   異常な etcd ノードの検出メカニズムを強化する [#7730](https://github.com/tikv/pd/issues/7730) @[JmPotato](https://github.com/JmPotato) @[HuSharp](https://github.com/HuSharp)
    -   pd-ctlのGCセーフポイントの出力を最適化する [#7767](https://github.com/tikv/pd/issues/7767) @[nolouch](https://github.com/nolouch)
    -   ホットスポットスケジューラにおける履歴ウィンドウ構成の動的な変更をサポートする [#7877](https://github.com/tikv/pd/issues/7877) @[lhy1024](https://github.com/lhy1024)
    -   オペレーター作成時のロック競合問題を軽減する [#7837](https://github.com/tikv/pd/issues/7837) @[Leavrth](https://github.com/Leavrth)
    -   可用性を向上させるためにGRPC構成を調整 [#7821](https://github.com/tikv/pd/issues/7821) @[rleungx](https://github.com/rleungx)

-   TiFlash

    -   `json_path`関数の`JSON_EXTRACT()`引数に非定数値を使用することをサポートする [#8510](https://github.com/pingcap/tiflash/issues/8510) @[SeaRise](https://github.com/SeaRise)
    -   `JSON_LENGTH(json, path)`機能 [#8711](https://github.com/pingcap/tiflash/issues/8711)[シーライズ](https://github.com/SeaRise)をサポートします

-   ツール

    -   バックアップと復元 (BR)

        -   `--load-stats` `br` } を導入します。 [#50568](https://github.com/pingcap/tidb/issues/50568) @[Leavrth](https://github.com/Leavrth)
        -   `--tikv-max-restore-concurrency`コマンドラインツールに、新しい復元パラメータ { `br` } を導入します。このパラメータは、各 TiKV ノードのダウンロードおよび取り込みファイルの最大数を制御します。また、ジョブキューの最大長を制御することで、 BRノードのメモリ消費量も制御します。 [#51621](https://github.com/pingcap/tidb/issues/51621) @[3pointer](https://github.com/3pointer)シュート
        -   粒度の粗いリージョン分散アルゴリズムを有効にして同時パラメータを適応的に取得できるようにすることで、復元パフォーマンスを向上させます [#50701](https://github.com/pingcap/tidb/issues/50701) @[3pointer](https://github.com/3pointer)
        -   `log`のコマンドラインヘルプ情報に`br`コマンドを表示する [#50927](https://github.com/pingcap/tidb/issues/50927) @[RidRisR](https://github.com/RidRisR)
        -   テーブルIDの再利用を最大化し、リストアパフォーマンスを向上させるため、リストアプロセス中にテーブルIDを事前割り当てする機能をサポートする [#51736](https://github.com/pingcap/tidb/issues/51736) @[Leavrth](https://github.com/Leavrth)
        -   BR使用時にTiDB内のGCメモリ制限チューナー機能を無効にしてOOM問題を回避する [#51078](https://github.com/pingcap/tidb/issues/51078) @[Leavrth](https://github.com/Leavrth)
        -   データ復元時のSSTファイルのマージ速度を、より効率的なアルゴリズムを使用して改善する [#50613](https://github.com/pingcap/tidb/issues/50613) @[Leavrth](https://github.com/Leavrth)
        -   データ復元時にデータベースをバッチ処理で作成する機能をサポート [#50767](https://github.com/pingcap/tidb/issues/50767) @[Leavrth](https://github.com/Leavrth)
        -   ログバックアップ中に、グローバルチェックポイントの進行に影響を与える最も遅いリージョンの情報をログとメトリクスに出力する [#51046](https://github.com/pingcap/tidb/issues/51046) @[YuJuncen](https://github.com/YuJuncen)
        -   大規模データセットのシナリオにおける`RESTORE`ステートメントのテーブル作成パフォーマンスを改善 [#48301](https://github.com/pingcap/tidb/issues/48301) @[Leavrth](https://github.com/Leavrth)

    -   TiCDC

        -   TiCDCがデータを複製する際のメモリ消費量を削減するために、 `RowChangedEvent`のメモリ消費量を最適化します [#10386](https://github.com/pingcap/tiflow/issues/10386) @[lidezhu](https://github.com/lidezhu)
        -   チェンジフィードタスクの作成と再開時に start-ts パラメータが有効であることを確認します [#10499](https://github.com/pingcap/tiflow/issues/10499) @[3AceShowHand](https://github.com/3AceShowHand)

    -   TiDBデータ移行（DM）

        -   MariaDBプライマリ/セカンダリレプリケーションシナリオにおいて、移行パスがMariaDBプライマリインスタンス→MariaDBセカンダリインスタンス→DM→TiDBである場合、 `gtid_strict_mode = off`かつMariaDBセカンダリインスタンスのGTIDが厳密にインクリメントされていない場合（例えば、MariaDBセカンダリインスタンスへのデータ書き込みがある場合）、DMタスクは`less than global checkpoint position`エラーを報告します。v8.0.0以降、TiDBはこのシナリオと互換性があり、データは正常に下流に移行できます。 [#10741](https://github.com/pingcap/tiflow/issues/10741) @[okJiang](https://github.com/okJiang)

    -   TiDB Lightning

        -   論理インポートモードでのバッチ内の最大行数の設定をサポートする[`logical-import-batch-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task) [#46607](https://github.com/pingcap/tidb/issues/46607) @[kennytm](https://github.com/kennytm)
        -   TiDB Lightning はTiFlashの容量が不足している場合にエラーを報告する [#50324](https://github.com/pingcap/tidb/issues/50324) @[okJiang](https://github.com/okJiang)

## バグ修正 {#bug-fixes}

-   TiDB

    -   データ変更がないにもかかわらず`auto analyze`が複数回トリガーされる問題を修正 [#51775](https://github.com/pingcap/tidb/issues/51775) @[Rustin170506](https://github.com/Rustin170506)
    -   `auto analyze`の同時実行設定が正しくない問題を修正 [#51749](https://github.com/pingcap/tidb/issues/51749) @[hawkingrei](https://github.com/hawkingrei)
    -   単一のSQL文を使用して複数のインデックスを追加した際に発生するインデックスの不整合の問題を修正 [#51746](https://github.com/pingcap/tidb/issues/51746) @[tangenta](https://github.com/tangenta)
    -   クエリで`Column ... in from clause is ambiguous`を使用する場合に発生する可能性がある`NATURAL JOIN`エラーを修正 [#32044](https://github.com/pingcap/tidb/issues/32044) @[AilinKid](https://github.com/AilinKid)
    -   TiDB が`group by`の定数値を誤って削除したことによる誤ったクエリ結果の問題を修正 [#38756](https://github.com/pingcap/tidb/issues/38756) @[Rustin170506](https://github.com/Rustin170506)ラスティン
    -   `LEADING`ヒントが`UNION ALL`ステートメントで有効にならない問題を修正 [#50067](https://github.com/pingcap/tidb/issues/50067) @[hawkingrei](https://github.com/hawkingrei)
    -   `BIT`型の列が一部の関数の計算に関与している場合、デコードエラーによりクエリエラーが発生する可能性がある問題を修正しました。 [#49566](https://github.com/pingcap/tidb/issues/49566) [#50850](https://github.com/pingcap/tidb/issues/50850) [#50855](https://github.com/pingcap/tidb/issues/50855) @[jiyfhust](https://github.com/jiyfhust)
    -   PDとの相互作用の問題により、 `tiup cluster upgrade/start`を使用してローリングアップグレードを実行するとTiDBがpanic可能性がある問題を修正しました [#50152](https://github.com/pingcap/tidb/issues/50152) @[zimulala](https://github.com/zimulala)
    -   `UNIQUE`句を使用して`ORDER BY`インデックス ルックアップを実行するとエラーが発生する可能性がある問題を修正 [#49920](https://github.com/pingcap/tidb/issues/49920) @[jackysp](https://github.com/jackysp)
    -   TiDBが`ENUM`または`SET`型を定数伝播で処理する際に誤ったクエリ結果を返す問題を修正 [#49440](https://github.com/pingcap/tidb/issues/49440) @[winoros](https://github.com/winoros)
    -   クエリに Apply 演算子が含まれている場合に TiDB がpanicを起こし、 `fatal error: concurrent map writes`エラーが発生する問題を修正しました [#50347](https://github.com/pingcap/tidb/issues/50347) @[SeaRise](https://github.com/SeaRise)
    -   文字列型の変数に対する`SET_VAR`の制御が無効になる可能性がある問題を修正しました [#50507](https://github.com/pingcap/tidb/issues/50507) @[qw4990](https://github.com/qw4990)
    -   `SYSDATE()`が`tidb_sysdate_is_now`に設定されている場合、 `1`関数がプランキャッシュ内の時間を誤って使用する問題を修正しました。 [#49299](https://github.com/pingcap/tidb/issues/49299) @[hawkingrei](https://github.com/hawkingrei)
    -   `CREATE GLOBAL BINDING`ステートメントを実行する際に、スキーマ名が大文字の場合、バインディングが有効にならない問題を修正しました [#50646](https://github.com/pingcap/tidb/issues/50646) @[qw4990](https://github.com/qw4990)
    -   `Index Path`が重複したインデックスを選択する問題を修正 [#50496](https://github.com/pingcap/tidb/issues/50496) @[AilinKid](https://github.com/AilinKid)
    -   `PLAN REPLAYER`ステートメントに`CREATE GLOBAL BINDING`が含まれている場合`IN()`がバインディングのロードに失敗する問題を修正 [#43192](https://github.com/pingcap/tidb/issues/43192) @[King-Dylan](https://github.com/King-Dylan)
    -   複数の`analyze`タスクが失敗した場合に、失敗理由が正しく記録されない問題を修正します [#50481](https://github.com/pingcap/tidb/issues/50481) @[Rustin170506](https://github.com/Rustin170506)
    -   `tidb_stats_load_sync_wait`が有効にならない問題を修正 [#50872](https://github.com/pingcap/tidb/issues/50872) @[jiyfhust](https://github.com/jiyfhust)
    -   `max_execute_time`設定が複数のレベルで互いに干渉する問題を修正 [#50914](https://github.com/pingcap/tidb/issues/50914) @[jiyfhust](https://github.com/jiyfhust)
    -   統計情報の同時更新によって発生するスレッドセーフティの問題を修正 [#50835](https://github.com/pingcap/tidb/issues/50835) @[Rustin170506](https://github.com/Rustin170506)
    -   パーティション テーブルで`auto analyze`を実行すると TiDB がpanicを引き起こす可能性がある問題を修正 [#51187](https://github.com/pingcap/tidb/issues/51187) @[Rustin170506](https://github.com/Rustin170506)
    -   SQL文中の`IN()`に異なる数の値が含まれている場合、SQLバインディングが機能しない可能性がある問題を修正しました [#51222](https://github.com/pingcap/tidb/issues/51222) @[hawkingrei](https://github.com/hawkingrei)
    -   TiDB が式内のシステム変数の型を正しく変換できない問題を修正 [#43527](https://github.com/pingcap/tidb/issues/43527) @[Rustin170506](https://github.com/Rustin170506)
    -   `force-init-stats`が設定されている場合に TiDB が対応するポートをリッスンしない問題を修正 [#51473](https://github.com/pingcap/tidb/issues/51473) @[hawkingrei](https://github.com/hawkingrei)
    -   `determinate`モード ( `tidb_opt_objective='determinate'` ) において、クエリに述語が含まれていない場合、統計情報がロードされない可能性がある問題を修正します [#48257](https://github.com/pingcap/tidb/issues/48257) @[time-and-fate](https://github.com/time-and-fate)
    -   `init-stats`プロセスが TiDB をpanic、 `load stats`プロセスを終了する可能性がある問題を修正しました [#51581](https://github.com/pingcap/tidb/issues/51581) @[hawkingrei](https://github.com/hawkingrei)
    -   `IN()`述語に`NULL`が含まれている場合にクエリ結果が正しくない問題を修正 [#51560](https://github.com/pingcap/tidb/issues/51560) @[winoros](https://github.com/winoros)
    -   DDLタスクが複数のテーブルに関係する場合、ブロックされたDDLステートメントがMDLビューに表示されない問題を修正します [#47743](https://github.com/pingcap/tidb/issues/47743) @[wjhuang2016](https://github.com/wjhuang2016)
    -   テーブル上の`processed_rows`タスクの`ANALYZE`が、そのテーブルの総行数を超える可能性がある問題を修正しました [#50632](https://github.com/pingcap/tidb/issues/50632) @ホーキング[ホーキングレイ](https://github.com/hawkingrei)
    -   `HashJoin`演算子がディスクにスピルしない場合に発生する可能性のあるゴルーチンリークの問題を修正 [#50841](https://github.com/pingcap/tidb/issues/50841) @[wshwsh12](https://github.com/wshwsh12)
    -   CTEクエリのメモリ使用量が制限を超えた場合に発生するゴルーチンリークの問題を修正 [#50337](https://github.com/pingcap/tidb/issues/50337) @[guo-shaoge](https://github.com/guo-shaoge)
    -   集計関数をグループ計算に使用した際に発生する可能性のある`Can't find column ...`エラーを修正 [#50926](https://github.com/pingcap/tidb/issues/50926) @[qw4990](https://github.com/qw4990)
    -   `CREATE TABLE`ステートメントに特定のパーティションまたは制約が含まれている場合に、テーブル名の変更などの DDL 操作が停止する問題を修正しました [#50972](https://github.com/pingcap/tidb/issues/50972) @[lcwangchao](https://github.com/lcwangchao)
    -   Grafana の監視メトリック`tidb_statistics_auto_analyze_total`が整数として表示されない問題を修正 [#51051](https://github.com/pingcap/tidb/issues/51051) @[hawkingrei](https://github.com/hawkingrei)
    -   `tidb_gogc_tuner_threshold`変数が変更された後、 `tidb_server_memory_limit`システム変数が適切に調整されない問題を修正 [#48180](https://github.com/pingcap/tidb/issues/48180) @[hawkingrei](https://github.com/hawkingrei)
    -   クエリに JOIN 操作が含まれる場合に`index out of range`エラーが発生する可能性がある問題を修正 [#42588](https://github.com/pingcap/tidb/issues/42588) @[AilinKid](https://github.com/AilinKid)
    -   列のデフォルト値が削除されている場合、列のデフォルト値を取得するとエラーが返される問題を修正します[#50043](https://github.com/pingcap/tidb/issues/50043) [#51324](https://github.com/pingcap/tidb/issues/51324) @[crazycs520](https://github.com/crazycs520)
    -   TiFlash の遅延実体化処理で関連する列が処理されると、間違った結果が返される場合がある問題を修正[#49241](https://github.com/pingcap/tidb/issues/49241) [#51204](https://github.com/pingcap/tidb/issues/51204) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    -   `LIKE()`関数がバイナリ照合順序入力を処理する際に誤った結果を返す可能性がある問題を修正しました [#50393](https://github.com/pingcap/tidb/issues/50393) @[yibin87](https://github.com/yibin87)
    -   `JSON_LENGTH()`関数が、2 番目のパラメータが`NULL`の場合に誤った結果を返す問題を修正しました [#50931](https://github.com/pingcap/tidb/issues/50931) @[SeaRise](https://github.com/SeaRise)
    -   `CAST(AS DATETIME)`が特定の状況下で時間精度を失う可能性がある問題を修正 [#49555](https://github.com/pingcap/tidb/issues/49555) @[SeaRise](https://github.com/SeaRise)
    -   テーブルにクラスター化インデックスがある場合、並列処理`Apply`が誤った結果を生成する可能性がある問題を修正 [#51372](https://github.com/pingcap/tidb/issues/51372) @[guo-shaoge](https://github.com/guo-shaoge)
    -   プライマリキーのタイプが`ALTER TABLE ... COMPACT TIFLASH REPLICA` `VARCHAR`が正しく終了しない可能性がある問題を修正 [#51810](https://github.com/pingcap/tidb/issues/51810) @[breezewish](https://github.com/breezewish)
    -   `NULL`ステートメントを使用してパーティション テーブルを交換する際に`DEFAULT NULL`属性の`EXCHANGE PARTITION`値のチェックが正しく行われない問題を修正しました。 [#47167](https://github.com/pingcap/tidb/issues/47167) @[jiyfhust](https://github.com/jiyfhust)
    -   パーティションテーブルの定義が、UTF8以外の文字セットを使用した場合に誤った動作を引き起こす可能性がある問題を修正しました [#49251](https://github.com/pingcap/tidb/issues/49251) @[YangKeao](https://github.com/YangKeao)
    -   一部のシステム変数について、 `INFORMATION_SCHEMA.VARIABLES_INFO`テーブルに誤ったデフォルト値が表示される問題を修正しました [#49461](https://github.com/pingcap/tidb/issues/49461) @[jiyfhust](https://github.com/jiyfhust)
    -   データベース名に空の文字列を使用した場合にエラーが報告されない場合がある問題を修正 [#45873](https://github.com/pingcap/tidb/issues/45873) @[yoshikipom](https://github.com/yoshikipom)
    -   `SPLIT TABLE ... INDEX`ステートメントにより TiDB がpanicを引き起こす可能性がある問題を修正 [#50177](https://github.com/pingcap/tidb/issues/50177) @[Defined2014](https://github.com/Defined2014)
    -   `KeyPartition`タイプのパーティションテーブルをクエリするとエラーが発生する可能性がある問題を修正[#50206](https://github.com/pingcap/tidb/issues/50206) [#51313](https://github.com/pingcap/tidb/issues/51313) [#51196](https://github.com/pingcap/tidb/issues/51196) @[time-and-fate](https://github.com/time-and-fate)@[jiyfhust](https://github.com/jiyfhust)@[mjonss](https://github.com/mjonss)
    -   ハッシュパーティションテーブルをクエリすると誤った結果が生成される可能性がある問題を修正 [#50427](https://github.com/pingcap/tidb/issues/50427) @[Defined2014](https://github.com/Defined2014)
    -   opentracing が正しく動作しない問題を修正 [#50508](https://github.com/pingcap/tidb/issues/50508) @[Defined2014](https://github.com/Defined2014)
    -   `ALTER INSTANCE RELOAD TLS`がエラーを報告した際にエラーメッセージが不完全になる問題を修正しました [#50699](https://github.com/pingcap/tidb/issues/50699) @[dveeden](https://github.com/dveeden)
    -   `AUTO_INCREMENT`属性が自動インクリメントIDを割り当てる際に不要なトランザクション競合を引き起こし、IDが連続しなくなる問題を修正しました [#50819](https://github.com/pingcap/tidb/issues/50819) @[tiancaiamao](https://github.com/tiancaiamao)
    -   TiDBログにおける一部のエラーのスタック情報が不完全な問題を修正 [#50849](https://github.com/pingcap/tidb/issues/50849) @[tiancaiamao](https://github.com/tiancaiamao)
    -   `LIMIT`句の数値が大きすぎる場合に、一部のクエリでメモリ使用量が過剰になる問題を修正しました [#51188](https://github.com/pingcap/tidb/issues/51188) @[Defined2014](https://github.com/Defined2014)
    -   TTL機能によって、場合によってはデータ範囲の分割が正しく行われずデータホットスポットが発生する問題を修正しました [#51527](https://github.com/pingcap/tidb/issues/51527) @[lcwangchao](https://github.com/lcwangchao)
    -   `SET`ステートメントが明示的トランザクションの最初の行にある場合に有効にならない問題を修正 [#51387](https://github.com/pingcap/tidb/issues/51387) @[YangKeao](https://github.com/YangKeao)
    -   `BINARY`タイプの JSON をクエリすると、場合によってはエラーが発生する問題を修正しました [#51547](https://github.com/pingcap/tidb/issues/51547) @[YangKeao](https://github.com/YangKeao)
    -   TTLが有効期限を計算する際に、夏時間調整の移行を正しく処理しない問題を修正 [#51675](https://github.com/pingcap/tidb/issues/51675) @[lcwangchao](https://github.com/lcwangchao)
    -   `SURVIVAL_PREFERENCES`ステートメントの出力に`SHOW CREATE PLACEMENT POLICY`属性が特定の条件下で表示されない問題を修正しました [#51699](https://github.com/pingcap/tidb/issues/51699) @[lcwangchao](https://github.com/lcwangchao)
    -   設定ファイルに無効な設定項目が含まれている場合に、設定ファイルが有効にならない問題を修正します [#51399](https://github.com/pingcap/tidb/issues/51399) @[Defined2014](https://github.com/Defined2014)

-   TiKV

    -   `tidb_enable_row_level_checksum`を有効にするとTiKVがpanicを起こす可能性がある問題を修正しました [#16371](https://github.com/tikv/tikv/issues/16371) @[cfzjywxk](https://github.com/cfzjywxk)
    -   例外的な状況で休止状態のリージョンがすぐに起動されない問題を修正 [#16368](https://github.com/tikv/tikv/issues/16368) @[LykxSassinator](https://github.com/LykxSassinator)
    -   レプリカが1つオフラインになったときにリージョン全体が利用できなくなる問題を修正するため、ノードをオフラインにする前にリージョンのすべてのレプリカの最終ハートビート時間をチェックします [#16465](https://github.com/tikv/tikv/issues/16465) [tonyxuqqi](https://github.com/tonyxuqqi)
    -   TiKV が、最大値`INT64`より大きく、最大値`UINT64`より小さい JSON 整数を`FLOAT64`として解析し、TiDB との不整合を引き起こす問題を修正しました。 [#16512](https://github.com/tikv/tikv/issues/16512) @[YangKeao](https://github.com/YangKeao)
    -   監視メトリック`tikv_unified_read_pool_thread_count`にデータがない場合がある問題を修正 [#16629](https://github.com/tikv/tikv/issues/16629) @[YuJuncen](https://github.com/YuJuncen)

-   PD

    -   `MergeLabels`関数が呼び出されたときにデータ競合が発生する問題を修正します [#7535](https://github.com/tikv/pd/issues/7535) @[lhy1024](https://github.com/lhy1024)
    -   `evict-leader-scheduler`インターフェイスを呼び出したときに出力がない問題を修正 [#7672](https://github.com/tikv/pd/issues/7672) @[CabinfeverB](https://github.com/CabinfeverB)
    -   PD監視項目`learner-peer-count`がリーダー切り替え後に古い値を同期しない問題を修正 [#7728](https://github.com/tikv/pd/issues/7728) @[CabinfeverB](https://github.com/CabinfeverB)
    -   `watch etcd`正しくオフになっていない場合に発生するメモリリークの問題を修正しました [#7807](https://github.com/tikv/pd/issues/7807) @[rleungx](https://github.com/rleungx)
    -   一部の TSO ログでエラー原因 [#7496](https://github.com/tikv/pd/issues/7496) @[CabinfeverB](https://github.com/CabinfeverB)が出力されない問題を修正
    -   再起動後に予期しない負のモニタリング指標が発生する問題を修正 [#4489](https://github.com/tikv/pd/issues/4489) @[lhy1024](https://github.com/lhy1024)
    -   Leaderのリースがログ時刻よりも後に期限切れになる問題を修正 [#7700](https://github.com/tikv/pd/issues/7700) @[CabinfeverB](https://github.com/CabinfeverB)
    -   TiDB (PD クライアント) と PD 間の TLS スイッチが矛盾している場合に TiDB がパニックになる問題を修正[#7900](https://github.com/tikv/pd/issues/7900) [#7902](https://github.com/tikv/pd/issues/7902) [#7916](https://github.com/tikv/pd/issues/7916) @[CabinfeverB](https://github.com/CabinfeverB)
    -   Goroutine が正しく閉じられなかった場合にメモリリークが発生する問題を修正しました [#7782](https://github.com/tikv/pd/issues/7782) @[HuSharp](https://github.com/HuSharp)
    -   特殊文字を含むスケジューラをpd-ctlが削除できない問題を修正 [#7798](https://github.com/tikv/pd/issues/7798) @[JmPotato](https://github.com/JmPotato)
    -   TSO [#7864](https://github.com/tikv/pd/issues/7864) @[CabinfeverB](https://github.com/CabinfeverB)を取得するときに PD クライアントがブロックされる可能性がある問題を修正

-   TiFlash

    -   レプリカ移行中にPDとのネットワーク接続が不安定になりTiFlashがpanicになる問題を修正 [#8323](https://github.com/pingcap/tiflash/issues/8323) @[JaySon-Huang](https://github.com/JaySon-Huang)
    -   クエリの遅延によりメモリ使用量が大幅に増加する問題を修正 [#8564](https://github.com/pingcap/tiflash/issues/8564) @[JinheLin](https://github.com/JinheLin)
    -   TiFlashレプリカを削除して再追加するとTiFlashでデータ破損が発生する可能性がある問題を修正 [#8695](https://github.com/pingcap/tiflash/issues/8695) @[JaySon-Huang](https://github.com/JaySon-Huang)
    -   ポイントインタイムリカバリ(PITR) の実行後、または`FLASHBACK CLUSTER TO`の実行後にTiFlashレプリカ データが誤って削除され、データ異常が発生する可能性がある問題を修正 [#8777](https://github.com/pingcap/tiflash/issues/8777) @[JaySon-Huang](https://github.com/JaySon-Huang)
    -   Null 許容カラムを null 許容カラム以外に変更する`ALTER TABLE ... MODIFY COLUMN ... NOT NULL`の実行後にTiFlash がパニックになる問題を修正 [#8419](https://github.com/pingcap/tiflash/issues/8419) @[JaySon-Huang](https://github.com/JaySon-Huang)
    -   分散ストレージとコンピューティングアーキテクチャにおいて、ネットワーク分離後にクエリが永久にブロックされる可能性がある問題を修正 [#8806](https://github.com/pingcap/tiflash/issues/8806) @[JinheLin](https://github.com/JinheLin)
    -   分散ストレージとコンピューティングアーキテクチャにおいて、 TiFlash がシャットダウン中にpanic可能性がある問題を修正 [#8837](https://github.com/pingcap/tiflash/issues/8837) @[JaySon-Huang](https://github.com/JaySon-Huang)
    -   リモート読み取り時にデータ競合によりTiFlashがクラッシュする可能性がある問題を修正 [#8685](https://github.com/pingcap/tiflash/issues/8685) @[solotzg](https://github.com/solotzg)
    -   `CAST(AS JSON)`関数が JSON オブジェクト キーの重複を削除しない問題を修正 [#8712](https://github.com/pingcap/tiflash/issues/8712) @[SeaRise](https://github.com/SeaRise)
    -   `ENUM`列がチャンクエンコード中にTiFlashを引き起こす可能性がある問題を修正しました [#8674](https://github.com/pingcap/tiflash/issues/8674) @[yibin87](https://github.com/yibin87)

-   ツール

    -   バックアップと復元 (BR)

        -   リージョンがリーダーになった直後に分割またはマージされると、ログバックアップのチェックポイントが停止する問題を修正 [#16469](https://github.com/tikv/tikv/issues/16469) @[YuJuncen](https://github.com/YuJuncen)
        -   一部の極端なケースでフルバックアップがピアを見つけられなかった際にTiKVがパニックを起こす問題を修正 [#16394](https://github.com/tikv/tikv/issues/16394) @[Leavrth](https://github.com/Leavrth)
        -   同じノード上の TiKV IP アドレスを変更した後にログのバックアップが停止する問題を修正 [#50445](https://github.com/pingcap/tidb/issues/50445) @[3pointer](https://github.com/3pointer)
        -   S3からファイルコンテンツを読み取る際にエラーが発生した場合にBRが再試行できない問題を修正 [#49942](https://github.com/pingcap/tidb/issues/49942) @[Leavrth](https://github.com/Leavrth)
        -   データ復元失敗後にチェックポイントから再開するとエラー`the target cluster is not fresh`発生する問題を修正 [#50232](https://github.com/pingcap/tidb/issues/50232) @[Leavrth](https://github.com/Leavrth)
        -   ログ バックアップ タスクを停止すると TiDB がクラッシュする問題を修正 [#50839](https://github.com/pingcap/tidb/issues/50839) @[YuJuncen](https://github.com/YuJuncen)
        -   TiKVノードにリーダーがいないためにデータ復元が遅くなる問題を修正 [#50566](https://github.com/pingcap/tidb/issues/50566) @[Leavrth](https://github.com/Leavrth)
        -   `--filter`オプションを指定した後でも完全復元ではターゲット クラスターが空である必要がある問題を修正 [#51009](https://github.com/pingcap/tidb/issues/51009) @[3pointer](https://github.com/3pointer)

    -   TiCDC

        -   ストレージシンク使用時にストレージサービスによって生成されるファイルシーケンス番号が正しくインクリメントされない可能性がある問題を修正しました [#10352](https://github.com/pingcap/tiflow/issues/10352) @[CharlesCheung96](https://github.com/CharlesCheung96)
        -   TiCDCが複数のチェンジフィードを同時に作成する際に`ErrChangeFeedAlreadyExists`エラーを返す問題を修正 [#10430](https://github.com/pingcap/tiflow/issues/10430) @[CharlesCheung96](https://github.com/CharlesCheung96)
        -   `add table partition`で`ignore-event`イベントをフィルタリングした後、TiCDC が関連パーティションの他のタイプの DML 変更を下流にレプリケートしない問題を修正します。 [#10524](https://github.com/pingcap/tiflow/issues/10524) @[CharlesCheung96](https://github.com/CharlesCheung96)
        -   アップストリームテーブルで`TRUNCATE PARTITION`が実行された後、changefeed がエラーを報告する問題を修正します [#10522](https://github.com/pingcap/tiflow/issues/10522) @[sdojjy](https://github.com/sdojjy)
        -   変更フィードを再開する際に`snapshot lost caused by GC`が時間内に報告されず、変更フィードの`checkpoint-ts`が TiDB の GC セーフポイントより小さい問題を修正します [#10463](https://github.com/pingcap/tiflow/issues/10463) @[sdojjy](https://github.com/sdojjy)
        -   単一行データのデータ整合性検証が有効になった後、タイムゾーンの不一致により TiCDC `TIMESTAMP`タイプのチェックサムを検証できない問題を修正 [#10573](https://github.com/pingcap/tiflow/issues/10573) @[3AceShowHand](https://github.com/3AceShowHand)
        -   Syncpoint テーブルが正しく複製されない可能性がある問題を修正しました [#10576](https://github.com/pingcap/tiflow/issues/10576) @[asddongmen](https://github.com/asddongmen)
        -   Apache Pulsarをダウンストリームとして使用する際に、OAuth2.0、TLS、mTLSが正しく有効化できない問題を修正 [#10602](https://github.com/pingcap/tiflow/issues/10602) @[asddongmen](https://github.com/asddongmen)
        -   TiKVがアップグレード、再起動、またはリーダーを追放した際に、変更フィードが停止する可能性がある問題を修正しました [#10584](https://github.com/pingcap/tiflow/issues/10584) @[asddongmen](https://github.com/asddongmen)
        -   DDLステートメントが頻繁に実行されるシナリオで、BarrierTSが間違っているためにデータが間違ったCSVファイルに書き込まれる問題を修正 [#10668](https://github.com/pingcap/tiflow/issues/10668) @[lidezhu](https://github.com/lidezhu)
        -   KVクライアントでのデータ競合によりTiCDCがpanicを起こす問題を修正 [#10718](https://github.com/pingcap/tiflow/issues/10718) @[asddongmen](https://github.com/asddongmen)
        -   TiCDCがテーブルレプリケーションタスクのスケジュール時にパニックを起こす問題を修正 [#10613](https://github.com/pingcap/tiflow/issues/10613) @[CharlesCheung96](https://github.com/CharlesCheung96)

    -   TiDBデータ移行（DM）

        -   アップストリームのプライマリキーがバイナリタイプの場合にデータが失われる問題を修正 [#10672](https://github.com/pingcap/tiflow/issues/10672) @[GMHDBJD](https://github.com/GMHDBJD)

    -   TiDB Lightning

        -   TiKVスペースのチェックによって発生するパフォーマンス低下の問題を修正 [#43636](https://github.com/pingcap/tidb/issues/43636) @[lance6716](https://github.com/lance6716)
        -   TiDB Lightningがファイルスキャン中に無効なシンボリックリンクファイルに遭遇した際にエラーを報告する問題を修正しました [#49423](https://github.com/pingcap/tidb/issues/49423) @[lance6716](https://github.com/lance6716)
        -   `0`が`NO_ZERO_IN_DATE` } に含まれていない場合に、 TiDB Lightning が`sql_mode`を含む日付値を正しく解析できない問題 [#50757](https://github.com/pingcap/tidb/issues/50757) @[GMHDBJD](https://github.com/GMHDBJD)

## 寄稿者 {#contributors}

TiDBコミュニティの以下の貢献者の皆様に感謝申し上げます。

-   [アオアン](https://github.com/Aoang)
-   [バッファロー](https://github.com/bufferflies)
-   [デーモン365](https://github.com/daemon365)
-   [エルトシアー](https://github.com/eltociear)
-   [リチュンジュ](https://github.com/lichunzhu)
-   [ジフハスト](https://github.com/jiyfhust)
-   [pingandb](https://github.com/pingandb)
-   [シェンキデバオジ](https://github.com/shenqidebaozi)
-   [スミティーズ](https://github.com/Smityz)
-   [ソンジビン97](https://github.com/songzhibin97)
-   [タンジンユ97](https://github.com/tangjingyu97)
-   [テーマ](https://github.com/Tema)
-   [ub-3](https://github.com/ub-3)
-   [ヨシキポム](https://github.com/yoshikipom)
