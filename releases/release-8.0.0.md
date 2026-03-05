---
title: TiDB 8.0.0 Release Notes
summary: TiDB 8.0.0 の新機能、互換性の変更、改善点、バグ修正について説明します。
---

# TiDB 8.0.0 リリースノート {#tidb-8-0-0-release-notes}

発売日：2024年3月29日

TiDB バージョン: 8.0.0

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v8.0/quick-start-with-tidb)

8.0.0 では、次の主な機能と改善が導入されています。

<table><thead><tr><th>カテゴリ</th><th>機能/拡張機能</th><th>説明</th></tr></thead><tbody><tr><td rowspan="4">スケーラビリティとパフォーマンス</td><td><a href="https://docs.pingcap.com/tidb/v8.0/pd-microservices">スケーラビリティ向上のためのPDの分解（実験的）</a></td><td>配置Driver（PD）には、TiDBクラスタの正常な動作を確保するために、複数の重要なモジュールが含まれています。クラスタのワークロードが増加すると、PD内の各モジュールのリソース消費量も増加し、これらのモジュール間の相互干渉を引き起こし、最終的にはクラスタ全体のサービス品質に影響を与えます。v8.0.0以降、TiDBはPD内のTSOモジュールとスケジューリングモジュールを独立してデプロイ可能なマイクロサービスに分割することで、この問題に対処しています。これにより、クラスタのスケールアップに伴うモジュール間の相互干渉を大幅に軽減できます。このアーキテクチャにより、はるかに大規模なクラスタと、はるかに大規模なワークロードを実現できるようになりました。</td></tr><tr><td><a href="https://docs.pingcap.com/tidb/v8.0/system-variables#tidb_dml_type-new-in-v800">大規模なトランザクションのためのバルク DML (実験的)</a></td><td>大規模なクリーンアップジョブ、結合、集計といった大規模なバッチDMLジョブは、大量のメモリを消費する可能性があり、これまでは非常に大規模なスケールでは制限されていました。バルクDML（ <code>tidb_dml_type = &quot;bulk&quot;</code> ）は、トランザクション保証を提供し、OOM（メモリ不足）の問題を軽減しながら、大規模なバッチDMLタスクをより効率的に処理するための新しいDMLタイプです。この機能は、データのロードに使用する場合、インポート、ロード、リストアの各操作とは異なります。</td></tr><tr><td><a href="https://docs.pingcap.com/tidb/v8.0/br-snapshot-guide#restore-cluster-snapshots">クラスター スナップショットの復元速度の高速化 (GA)</a></td><td>この機能により、 BRはクラスタのスケールメリットを最大限に活用し、クラスタ内のすべてのTiKVノードがデータ復元の準備ステップに参加できるようになります。この機能により、大規模クラスタにおける大規模データセットの復元速度が大幅に向上します。実環境テストでは、この機能によりダウンロード帯域幅が飽和状態になり、ダウンロード速度が8～10倍、エンドツーエンドの復元速度が約1.5～3倍向上することが示されています。</td></tr><tr><td>テーブル数が膨大である場合のスキーマ情報のキャッシュの安定性を向上（実験的）</td><td>マルチテナントアプリケーションの記録システムとしてTiDBを使用しているSaaS企業は、多くの場合、膨大な数のテーブルを保存する必要があります。以前のバージョンでは、100万個以上のテーブル数を処理することは可能でしたが、全体的なユーザーエクスペリエンスが低下する可能性がありました。TiDB v8.0.0では、 <code>auto analyze</code>に<a href="https://docs.pingcap.com/tidb/v8.0/system-variables#tidb_enable_auto_analyze_priority_queue-new-in-v800">優先キュー</a>を実装することで状況が改善され、プロセスの柔軟性が向上し、より広範なテーブルにわたる安定性が向上しました。</td></tr><tr><td rowspan="1"> DB操作と可観測性</td><td>インデックスの使用統計の監視をサポート</td><td>適切なインデックス設計は、データベースのパフォーマンス維持に不可欠な前提条件です。TiDB v8.0.0では、インデックスの使用状況統計を提供する<a href="https://docs.pingcap.com/tidb/v8.0/information-schema-tidb-index-usage"><code>INFORMATION_SCHEMA.TIDB_INDEX_USAGE</code></a>テーブルと<a href="https://docs.pingcap.com/tidb/v8.0/sys-schema-unused-indexes"><code>sys.schema_unused_indexes</code></a>ビューが導入されました。この機能は、データベース内のインデックスの効率性を評価し、インデックス設計を最適化するのに役立ちます。</td></tr><tr><td rowspan="2">データ移行</td><td>TiCDCが<a href="https://docs.pingcap.com/tidb/v8.0/ticdc-simple-protocol">シンプルプロトコル</a>のサポートを追加</td><td>TiCDCは、新しいプロトコル「Simpleプロトコル」を導入しました。このプロトコルは、DDLおよびBOOTSTRAPイベントにテーブルスキーマ情報を埋め込むことで、インバンドスキーマ追跡機能を提供します。</td></tr><tr><td> TiCDC が<a href="https://docs.pingcap.com/tidb/v8.0/ticdc-debezium">Debezium 形式プロトコル</a>のサポートを追加</td><td>TiCDC は新しいプロトコル、Debezium プロトコルを導入しました。TiCDC は、Debezium スタイルのメッセージを生成するプロトコルを使用して、データ変更イベントを Kafka シンクにパブリッシュできるようになりました。</td></tr></tbody></table>

## 機能の詳細 {#feature-details}

### スケーラビリティ {#scalability}

-   PDはマイクロサービスモード（実験的） [＃5766](https://github.com/tikv/pd/issues/5766) @ [ビンシビン](https://github.com/binshi-bing)をサポートします

    バージョン8.0.0以降、PDはマイクロサービスモードをサポートします。このモードでは、PDのタイムスタンプ割り当て機能とクラスタスケジューリング関数が、独立してデプロイ可能な個別のマイクロサービスに分割されます。これにより、PDのパフォーマンススケーラビリティが向上し、大規模クラスタにおけるPDのパフォーマンスボトルネックが解消されます。

    -   `tso`マイクロサービス: クラスター全体に対して単調に増加するタイムスタンプ割り当てを提供します。
    -   `scheduling`マイクロサービス: 負荷分散、ホットスポット処理、レプリカ修復、レプリカ配置など、クラスター全体のスケジュール関数を提供します。

    各マイクロサービスは独立したプロセスとしてデプロイされます。マイクロサービスに複数のレプリカを設定すると、マイクロサービスはプライマリ/セカンダリフォールトトレラントモードを自動的に実装し、サービスの高可用性と信頼性を確保します。

    現在、PDマイクロサービスはTiDB Operatorを使用してのみデプロイできます。PDがスケールアップでは解決できない重大なパフォーマンスボトルネックになった場合は、このモードを検討することをお勧めします。

    詳細については[ドキュメント](/pd-microservices.md)参照してください。

<!---->

-   Titanエンジン[＃16245](https://github.com/tikv/tikv/issues/16245) @ [コナー1996](https://github.com/Connor1996)の使いやすさを向上

    -   Titan BLOB ファイルと RocksDB ブロック ファイルの共有キャッシュをデフォルトで有効にし ( [`shared-blob-cache`](/tikv-configuration-file.md#shared-blob-cache-new-in-v800)デフォルトは`true` )、 [`blob-cache-size`](/tikv-configuration-file.md#blob-cache-size)個別に構成する必要がなくなります。
    -   Titan エンジンを使用する際にパフォーマンスと柔軟性を向上させるために、 [`min-blob-size`](/tikv-configuration-file.md#min-blob-size) 、 [`blob-file-compression`](/tikv-configuration-file.md#blob-file-compression) 、 [`discardable-ratio`](/tikv-configuration-file.md#min-blob-size)動的に変更することをサポートします。

    詳細については[ドキュメント](/storage-engine/titan-configuration.md)参照してください。

### パフォーマンス {#performance}

-   BR はスナップショットの復元速度を向上します (GA) [＃50701](https://github.com/pingcap/tidb/issues/50701) @ [3ポイントシュート](https://github.com/3pointer) @ [リーヴルス](https://github.com/Leavrth)

    TiDB v8.0.0以降、スナップショット復元速度の高速化が一般提供（GA）され、デフォルトで有効化されました。BRは、粗粒度のリージョン分散アルゴリズムの採用、データベースとテーブルのバッチ作成、SSTファイルのダウンロードと取り込み操作の相互影響の低減、テーブル統計の復元高速化など、様々な最適化を実装することで、スナップショット復元速度を大幅に向上させます。実環境におけるテスト結果によると、単一のTiKVノードのデータ復元速度は1.2 GiB/sで安定し、100 TiBのデータを1時間以内に復元できます。

    これは、高負荷環境でもBR が各 TiKV ノードのリソースを最大限に活用できることを意味します。これにより、データベースのリストア時間が大幅に短縮され、データベースの可用性と信頼性が向上し、データ損失やシステム障害によるダウンタイムとビジネス損失が削減されます。リストア速度の向上は、多数の goroutine の並列実行に起因しており、特にテーブルやリージョンが多い場合は、メモリ消費量が大幅に増加する可能性があることに注意してください。BRBRを実行するには、メモリ容量の高いマシンを使用することをお勧めします。マシンのメモリ容量が限られている場合は、より細粒度のリージョン分散アルゴリズムを使用することをお勧めします。また、粗粒度のリージョン分散アルゴリズムは外部storage帯域幅を大量に消費する可能性があるため、外部帯域幅の不足による他のアプリケーションへの影響を回避する必要があります。

    詳細については[ドキュメント](/br/br-snapshot-guide.md#restore-cluster-snapshots)参照してください。

-   以下の関数をTiFlash [＃50975](https://github.com/pingcap/tidb/issues/50975) [＃50485](https://github.com/pingcap/tidb/issues/50485) @ [イービン87](https://github.com/yibin87) @ [ウィンドトーカー](https://github.com/windtalker)にプッシュダウンすることをサポートします

    -   `CAST(DECIMAL AS DOUBLE)`
    -   `POWER()`

    詳細については[ドキュメント](/tiflash/tiflash-supported-pushdown-calculations.md)参照してください。

-   TiDBの並列HashAggアルゴリズムはディスクスピル（実験的） [＃35637](https://github.com/pingcap/tidb/issues/35637) @ [xzhangxian1008](https://github.com/xzhangxian1008)をサポートします。

    TiDBの以前のバージョンでは、HashAgg演算子の同時実行アルゴリズムはディスクへの書き込みをサポートしていませんでした。SQL文の実行プランに並列HashAgg演算子が含まれている場合、そのSQL文のすべてのデータはメモリ内でのみ処理できます。その結果、TiDBは大量のデータをメモリ内で処理する必要がありました。データサイズがメモリ制限を超えると、TiDBは非並列アルゴリズムしか選択できず、同時実行によるパフォーマンス向上は期待できません。

    v8.0.0では、TiDBの並列HashAggアルゴリズムがディスクスピルをサポートします。並列処理の条件を問わず、HashAgg演算子はメモリ使用量に基づいてデータスピルを自動的にトリガーできるため、パフォーマンスとデータスループットのバランスを取ることができます。現在、TiDBは実験的機能として、ディスクスピルをサポートする並列HashAggアルゴリズムを有効にするかどうかを制御する変数`tidb_enable_parallel_hashagg_spill`導入しています。この変数が`ON`場合、有効です。この機能が将来のリリースで一般提供された後、この変数は非推奨となります。

    詳細については[ドキュメント](/system-variables.md#tidb_enable_parallel_hashagg_spill-new-in-v800)参照してください。

-   自動統計収集のための優先キューを導入する[＃50132](https://github.com/pingcap/tidb/issues/50132) @ [ハイラスティン](https://github.com/Rustin170506)

    オプティマイザ統計を最新の状態に保つことは、データベースのパフォーマンスを安定させる鍵です。ほとんどのユーザーは、最新の統計を収集するためにTiDBが提供する[自動統計収集](/statistics.md#automatic-update)に依存しています。自動統計収集機能は、すべてのオブジェクトの統計状態を確認し、問題のあるオブジェクトをキューに追加して順次収集します。以前のバージョンでは、順序はランダムであったため、より適切な候補の更新を待つ時間が長くなり、パフォーマンスの低下を引き起こす可能性がありました。

    バージョン8.0.0以降、自動統計収集機能は、様々な条件と組み合わせてオブジェクトの優先順位を動的に設定し、より適切な候補（新規作成されたインデックスや定義変更されたパーティションテーブルなど）が優先的に処理されるようにします。さらに、TiDBはヘルススコアが低いテーブルを優先し、キューの先頭に配置します。この機能強化により、収集順序がより合理的になり、古い統計情報に起因するパフォーマンスの問題が軽減され、データベースの安定性が向上します。

    詳細については[ドキュメント](/system-variables.md#tidb_enable_auto_analyze_priority_queue-new-in-v800)参照してください。

-   実行プランキャッシュ[＃49161](https://github.com/pingcap/tidb/pull/49161) @ [ミョンス](https://github.com/mjonss) @ [qw4990](https://github.com/qw4990)の制限の一部を削除

    TiDBは[プランキャッシュ](/sql-prepared-plan-cache.md)サポートしています。これはOLTPシステムのレイテンシーを効果的に削減でき、パフォーマンスにとって重要です。v8.0.0では、TiDBはプランキャッシュに関するいくつかの制限を解除しました。以下の項目を含む実行プランをキャッシュできるようになりました。

    -   [パーティションテーブル](/partitioned-table.md)
    -   [生成された列](/generated-columns.md) 、生成された列に依存するオブジェクト（ [多値インデックス](/choose-index.md#multi-valued-indexes-and-plan-cache)など）を含む

    この機能強化により、プラン キャッシュの使用ケースが拡張され、複雑なシナリオにおけるデータベース全体のパフォーマンスが向上します。

    詳細については[ドキュメント](/sql-prepared-plan-cache.md)参照してください。

-   オプティマイザは、複数値インデックスのサポートを強化します[＃47759](https://github.com/pingcap/tidb/issues/47759) [＃46539](https://github.com/pingcap/tidb/issues/46539) @ [アリーナルクス](https://github.com/Arenatlx) @ [時間と運命](https://github.com/time-and-fate)

    TiDB v6.6.0では、JSONデータ型のクエリパフォーマンスを向上させる[複数値インデックス](/sql-statements/sql-statement-create-index.md#multi-valued-indexes)導入されました。v8.0.0では、オプティマイザーによる多値インデックスのサポートが強化され、複雑なシナリオでもクエリを最適化するために多値インデックスを正しく識別・活用できるようになりました。

    -   オプティマイザは多値インデックスの統計情報を収集し、それに基づいて実行計画を決定します。SQL文で複数の多値インデックスが選択可能な場合、オプティマイザはコストが低いインデックスを特定できます。
    -   `OR`用いて複数の`member of`条件を接続する場合、オプティマイザーは各 DNF 項目（ `member of`条件）に対して有効なインデックス部分パスを一致させ、これらのパスを Union を用いて結合して`Index Merge`形成します。これにより、より効率的な条件フィルタリングとデータフェッチが実現されます。

    詳細については[ドキュメント](/sql-statements/sql-statement-create-index.md#multi-valued-indexes)参照してください。

-   低精度TSO [＃51081](https://github.com/pingcap/tidb/issues/51081) @ [テーマ](https://github.com/Tema)の更新間隔の設定をサポート

    TiDBの[低精度TSO機能](/system-variables.md#tidb_low_resolution_tso) 、定期的に更新されるTSOをトランザクションのタイムスタンプとして使用します。古いデータの読み取りが許容されるシナリオでは、この機能により、リアルタイム性は犠牲になりますが、小規模な読み取り専用トランザクションでTSOを取得する際のオーバーヘッドが削減され、高同時実行読み取りの能力が向上します。

    v8.0.0より前のバージョンでは、低精度TSO機能のTSO更新間隔は固定されており、実際のアプリケーション要件に合わせて調整することはできませんでした。v8.0.0では、TiDBにTSO更新間隔を制御するためのシステム変数`tidb_low_resolution_tso_update_interval`導入されました。この機能は、低精度TSO機能が有効な場合にのみ有効になります。

    詳細については[ドキュメント](/system-variables.md#tidb_low_resolution_tso_update_interval-new-in-v800)参照してください。

### 可用性 {#availability}

-   プロキシコンポーネントTiProxyが一般提供（GA）される[＃413](https://github.com/pingcap/tiproxy/issues/413) @ [djshow832](https://github.com/djshow832) @ [xhebox](https://github.com/xhebox)

    TiDB v7.6.0 では、プロキシコンポーネントTiProxy が実験的機能として導入されました。TiProxy は TiDB の公式プロキシコンポーネントであり、クライアントと TiDBサーバーの間に配置されます。TiProxy は TiDB の負荷分散機能と接続の永続化関数を提供し、TiDB クラスタのワークロードのバランスを向上させ、メンテナンス作業中のデータベースへのユーザーアクセスに影響を与えません。

    v8.0.0 では、TiProxy が一般提供され、署名証明書の自動生成と監視関数が強化されています。

    TiProxy の使用シナリオは次のとおりです。

    -   TiDBクラスタのローリング再起動、ローリングアップグレード、スケールインなどのメンテナンス作業中は、TiDBサーバに変更が発生し、クライアントとTiDBサーバ間の接続が中断される可能性があります。TiProxyを使用することで、これらのメンテナンス作業中にクライアントへの影響を最小限に抑え、接続を他のTiDBサーバにスムーズに移行できます。
    -   TiDBサーバーへのクライアント接続は、他のTiDBサーバに動的に移行できません。複数のTiDBサーバのワークロードが不均衡な場合、クラスタ全体のリソースは十分であるにもかかわらず、特定のTiDBサーバでリソース枯渇が発生し、レイテンシーが大幅に増加するという状況が発生する可能性があります。この問題に対処するため、TiProxyは接続の動的移行機能を提供します。これにより、クライアントに影響を与えることなく、接続をあるTiDBサーバーから別のTiDBサーバに移行できるため、TiDBクラスタの負荷分散が実現します。

    TiProxy はTiUP、 TiDB Operator、および TiDB Dashboard に統合されており、構成、展開、保守が容易になります。

    詳細については[ドキュメント](/tiproxy/tiproxy-overview.md)参照してください。

### SQL {#sql}

-   大量データ処理用の新しいDMLタイプをサポート（実験的） [＃50215](https://github.com/pingcap/tidb/issues/50215) @ [エキシウム](https://github.com/ekexium)

    v8.0.0より前のTiDBでは、コミット前にすべてのトランザクションデータをメモリに保存していました。大量のデータを処理する場合、トランザクションに必要なメモリがボトルネックとなり、TiDBが処理できるトランザクションサイズが制限されます。TiDBは非トランザクションDMLを導入し、SQL文を分割することでトランザクションサイズの制限を解決しようと試みていますが、この機能には様々な制限があり、実際のシナリオでは理想的なエクスペリエンスを提供できません。

    TiDBはv8.0.0以降、大量データ処理用のDMLタイプをサポートしています。このDMLタイプは、実行中にデータをTiKVにタイムリーに書き込むため、すべてのトランザクションデータがメモリに継続的にstorageことを回避し、メモリ制限を超える大量データの処理をサポートします。このDMLタイプはトランザクション`DELETE` `REPLACE` `INSERT` `UPDATE`この新しいDMLタイプを使用して大規模なDML操作を実行できます。

    このDMLタイプは[パイプラインDML](https://github.com/pingcap/tidb/blob/release-8.0/docs/design/2024-01-09-pipelined-DML.md)機能によって実装されており、自動コミットが有効になっているステートメントでのみ有効になります。このDMLタイプを有効にするかどうかは、システム変数[`tidb_dml_type`](/system-variables.md#tidb_dml_type-new-in-v800)設定することで制御できます。

    詳細については[ドキュメント](/system-variables.md#tidb_dml_type-new-in-v800)参照してください。

-   テーブル作成時にデフォルトの列値を設定するための式の使用をサポート (実験的) [＃50936](https://github.com/pingcap/tidb/issues/50936) @ [ジムララ](https://github.com/zimulala)

    バージョン8.0.0より前のバージョンでは、テーブルを作成する際に、列のデフォルト値は文字列、数値、日付に制限されていました。バージョン8.0.0以降では、列のデフォルト値としていくつかの式を使用できるようになりました。例えば、列のデフォルト値を`UUID()`に設定できます。この機能により、より多様な要件に対応できるようになります。

    詳細については[ドキュメント](/data-type-default-values.md#specify-expressions-as-default-values)参照してください。

-   `div_precision_increment`システム変数[＃51501](https://github.com/pingcap/tidb/issues/51501) @ [イービン87](https://github.com/yibin87)をサポート

    MySQL 8.0では、 `/`演算子を用いた除算の結果のスケールを何桁増やすかを指定する変数`div_precision_increment`がサポートされています。v8.0.0より前のTiDBではこの変数はサポートされておらず、除算は小数点以下4桁まで実行されます。v8.0.0以降では、TiDBはこの変数をサポートしています。除算の結果のスケールを何桁増やすかを、必要に応じて指定できます。

    詳細については[ドキュメント](/system-variables.md#div_precision_increment-new-in-v800)参照してください。

### DB操作 {#db-operations}

-   PITRはAmazon S3オブジェクトロック[＃51184](https://github.com/pingcap/tidb/issues/51184) @ [リドリスR](https://github.com/RidRisR)をサポートします

    Amazon S3 オブジェクトロックは、指定された保持期間中のバックアップデータの偶発的または意図的な削除を防ぎ、データのセキュリティと整合性を強化します。バージョン6.3.0以降、 BRはスナップショットバックアップでAmazon S3 オブジェクトロックをサポートし、フルバックアップのレイヤーをさらに強化します。バージョン8.0.0以降、PITRもAmazon S3 オブジェクトロックをサポートします。フルバックアップでもログデータバックアップでも、オブジェクトロック機能はより信頼性の高いデータ保護を実現し、データのバックアップとリカバリのセキュリティをさらに強化し、規制要件を満たします。

    詳細については[ドキュメント](/br/backup-and-restore-storages.md#other-features-supported-by-the-storage-service)参照してください。

-   セッションレベル[＃50653](https://github.com/pingcap/tidb/issues/50653) @ [ホーキングレイ](https://github.com/hawkingrei)で非表示のインデックスを可視化する機能をサポート

    デフォルトでは、オプティマイザは[目に見えないインデックス](/sql-statements/sql-statement-create-index.md#invisible-index)選択しません。このメカニズムは通常、インデックスを削除するかどうかを判断するために使用されます。インデックスの削除によるパフォーマンスへの影響が不明な場合は、インデックスを一時的に非表示に設定し、必要に応じてすぐに表示に戻すという選択肢があります。

    バージョン8.0.0以降では、セッションレベルのシステム変数[`tidb_opt_use_invisible_indexes`](/system-variables.md#tidb_opt_use_invisible_indexes-new-in-v800) ～ `ON`を設定することで、現在のセッションで非表示のインデックスを認識できるようになりました。この機能を使用すると、新しいインデックスを作成してパフォーマンスをテストする際に、まずインデックスを可視化し、その後、現在のセッションでシステム変数を変更することで、他のセッションに影響を与えることなくテストを行うことができます。この改善により、SQLチューニングの安全性が向上し、本番データベースの安定性が向上します。

    詳細については[ドキュメント](/sql-statements/sql-statement-create-index.md#invisible-index)参照してください。

-   一般的なログを別のファイルに書き込むことをサポート[＃51248](https://github.com/pingcap/tidb/issues/51248) @ [定義2014](https://github.com/Defined2014)

    一般ログは、実行されたすべてのSQL文をログに記録し、問題の診断に役立てるMySQL互換機能です。TiDBもこの機能をサポートしています。変数[`tidb_general_log`](/system-variables.md#tidb_general_log)設定することで有効にできます。ただし、以前のバージョンでは、一般ログの内容は他の情報と共にTiDBインスタンスログにのみ書き込まれるため、長期間にわたってログを保持する必要があるユーザーにとっては不便でした。

    バージョン8.0.0以降では、設定項目[`log.general-log-file`](/tidb-configuration-file.md#general-log-file-new-in-v800)に有効なファイル名を設定することで、一般ログを指定のファイルに書き込むことができます。一般ログは、インスタンスログと同じローテーションおよび保持ポリシーに従います。

    さらに、履歴ログファイルが占有するディスク容量を削減するため、TiDB v8.0.0ではネイティブログ圧縮オプションが導入されました。設定項目[`log.file.compression`](/tidb-configuration-file.md#compression-new-in-v800) ～ `gzip`を設定すると、ローテーションされたログを[`gzip`](https://www.gzip.org/)形式で自動的に圧縮できます。

    詳細については[ドキュメント](/tidb-configuration-file.md#general-log-file-new-in-v800)参照してください。

### 可観測性 {#observability}

-   インデックス使用統計の監視をサポート[＃49830](https://github.com/pingcap/tidb/issues/49830) @ [ヤンケオ](https://github.com/YangKeao)

    適切なインデックス設計は、データベースのパフォーマンスを維持するための重要な前提条件です。TiDB v8.0.0では、現在のTiDBノード上のすべてのインデックスの統計情報を記録するテーブル[`INFORMATION_SCHEMA.TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md)導入されました。これには以下の情報が含まれます。

    -   インデックスをスキャンするステートメントの累積実行回数
    -   インデックスにアクセスする際にスキャンされる行の総数
    -   インデックスをスキャンする際の選択分布
    -   インデックスへの最終アクセス時刻

    この情報を使用すると、オプティマイザーによって使用されていないインデックスや選択性が低いインデックスを識別し、インデックス設計を最適化してデータベースのパフォーマンスを向上させることができます。

    さらに、TiDB v8.0.0 では、MySQL と互換性のあるビュー[`sys.schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md)が導入されました。このビューは、TiDB インスタンスの前回の起動以降に使用されていないインデックスを表示します。v8.0.0 より前のバージョンからアップグレードしたクラスターでは、 `sys`スキーマとビューは自動的に作成されません。 [`sys.schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md#manually-create-the-schema_unused_indexes-view)を参照して手動で作成できます。

    詳細については[ドキュメント](/information-schema/information-schema-tidb-index-usage.md)参照してください。

### Security {#security}

-   保存時の TiKV 暗号化は Google [鍵管理サービス（クラウド KMS）](https://cloud.google.com/docs/security/key-management-deep-dive?hl) (実験的) [＃8906](https://github.com/tikv/tikv/issues/8906) @ [栄光](https://github.com/glorv)をサポートします

    TiKVは、保存データを保存時の暗号化技術を用いて暗号化することで、データセキュリティを確保します。セキュリティのための保存時の暗号化の中核は鍵管理です。バージョン8.0.0以降では、Google Cloud KMSを使用してTiKVのマスター鍵を管理し、Cloud KMSベースの保存時の暗号化機能を確立することで、ユーザーデータのセキュリティを強化できます。

    Google Cloud KMS に基づいて保存時の暗号化を有効にするには、Google Cloud でキーを作成し、TiKV 構成ファイルの`[security.encryption.master-key]`セクションを構成する必要があります。

    詳細については[ドキュメント](/encryption-at-rest.md#tikv-encryption-at-rest)参照してください。

-   TiDB ログ感度低下を[＃51306](https://github.com/pingcap/tidb/issues/51306) @ [xhebox](https://github.com/xhebox)強化

    TiDBログの感度低下機能の強化は、ログファイル内のSQLテキスト情報をマーキングすることで、ユーザーがログを表示する際に機密データを安全に表示されるようにします。ログ情報の感度低下を制御することで、様々なシナリオでTiDBログを安全に使用でき、ログ感度低下機能を使用する際のセキュリティと柔軟性が向上します。この機能を使用するには、システム変数`tidb_redact_log`を`MARKER`に設定します。これにより、TiDBログ内のSQLテキストがマーキングされます。ログを表示すると、機密データはマーカーに基づいて安全に表示されるため、ログ情報が保護されます。

    詳細については[ドキュメント](/system-variables.md#tidb_redact_log)参照してください。

### データ移行 {#data-migration}

-   TiCDC はシンプルプロトコル[＃9898](https://github.com/pingcap/tiflow/issues/9898) @ [3エースショーハンド](https://github.com/3AceShowHand)のサポートを追加しました

    TiCDCは、新しいプロトコル「Simpleプロトコル」を導入しました。このプロトコルは、DDLおよびBOOTSTRAPイベントにテーブルスキーマ情報を埋め込むことで、インバンドスキーマ追跡機能を提供します。

    詳細については[ドキュメント](/ticdc/ticdc-simple-protocol.md)参照してください。

-   TiCDC は Debezium フォーマットプロトコル[＃1799](https://github.com/pingcap/tiflow/issues/1799) @ [そよ風のような](https://github.com/breezewish)のサポートを追加しました

    TiCDCは、Debezium形式のイベントメッセージを生成するプロトコルを使用して、データ変更イベントをKafkaシンクにパブリッシュできるようになりました。これにより、現在Debeziumを使用してMySQLからデータをプルし、下流処理に利用しているユーザーにとって、MySQLからTiDBへの移行が簡素化されます。

    詳細については[ドキュメント](/ticdc/ticdc-debezium.md)参照してください。

-   DM は、ソース データベースとターゲット データベースのパスワードを暗号化および復号化するために、ユーザーが提供する秘密鍵の使用をサポートします[＃9492](https://github.com/pingcap/tiflow/issues/9492) @ [D3ハンター](https://github.com/D3Hunter)

    以前のバージョンでは、DMは比較的セキュリティの低い組み込みの固定秘密鍵を使用していました。v8.0.0以降では、上流および下流データベースのパスワードの暗号化と復号化に使用する秘密鍵ファイルをアップロードして指定できるようになりました。また、必要に応じて秘密鍵ファイルを置き換えることで、データセキュリティを強化できます。

    詳細については[ドキュメント](/dm/dm-customized-secret-key.md)参照してください。

-   `IMPORT INTO`機能を強化するために`IMPORT INTO ... FROM SELECT`構文をサポートします (実験的) [＃49883](https://github.com/pingcap/tidb/issues/49883) @ [D3ハンター](https://github.com/D3Hunter)

    以前のバージョンのTiDBでは、クエリ結果をターゲットテーブルにインポートするには`INSERT INTO ... SELECT`ステートメントしか使用できませんでした。これは、大規模なデータセットを扱うシナリオによっては、比較的効率が悪かったです。v8.0.0以降では、 `IMPORT INTO ... FROM SELECT`ステートメントを使用して`SELECT`のクエリの結果を空のTiDBターゲットテーブルにインポートできるようになり、 `INSERT INTO ... SELECT`のステートメントと比較して最大8倍のパフォーマンスを実現し、インポート時間を大幅に短縮します。

    さらに、 `IMPORT INTO ... FROM SELECT`を使用して[`AS OF TIMESTAMP`](/as-of-timestamp.md)でクエリされた履歴データをインポートすることもできます。

    詳細については[ドキュメント](/sql-statements/sql-statement-import-into.md)参照してください。

-   TiDB Lightningは競合解決戦略を簡素化し、 `replace`戦略（実験的） [＃51036](https://github.com/pingcap/tidb/issues/51036) @ [lyzx2001](https://github.com/lyzx2001)を使用して競合するデータの処理をサポートします。

    以前のバージョンでは、 TiDB Lightningには論理インポート モードが[1つのデータ競合解決戦略](/tidb-lightning/tidb-lightning-logical-import-mode-usage.md#conflict-detection) 、物理インポート モードが[2つのデータ競合解決戦略](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#conflict-detection)あり、理解して構成するのは簡単ではありませんでした。

    TiDB Lightning v8.0.0以降、物理インポートモードにおける[競合検出の古いバージョン](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#the-old-version-of-conflict-detection-deprecated-in-v800)戦略は廃止され、 [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md)パラメータを使用して論理インポートモードと物理インポートモードの両方で競合検出戦略を制御できるようになり、このパラメータの設定が簡素化されました。さらに、物理インポートモードにおいて、 `replace`戦略では、インポート時に主キーまたは一意キーの競合が検出された場合に、最新のデータを保持し、古いデータを上書きする機能がサポートされるようになりました。

    詳細については[ドキュメント](/tidb-lightning/tidb-lightning-configuration.md)参照してください。

-   グローバルソートが一般提供（GA）され、 `IMPORT INTO`のパフォーマンスと安定性が大幅に向上しました[＃45719](https://github.com/pingcap/tidb/issues/45719) @ [ランス6716](https://github.com/lance6716)

    v7.4.0より前のバージョンでは、 [分散実行フレームワーク (DXF)](/tidb-distributed-execution-framework.md)使用して`IMPORT INTO`タスクを実行する場合、ローカルstorage容量の制限により、TiDBはTiKVにインポートする前にデータの一部のみをローカルでソートしていました。その結果、TiKVにインポートされたデータに大きな重複が生じ、インポート時にTiKVで追加の圧縮操作を実行する必要があり、TiKVのパフォーマンスと安定性に影響を与えていました。

    バージョン7.4.0で導入された実験的機能であるグローバルソートにより、TiDBはインポートするデータをTiKVにインポートする前に、外部storage（Amazon S3など）に一時的に保存してグローバルソート処理を行うことができます。これにより、インポート時にTiKVの圧縮操作を行う必要がなくなります。バージョン8.0.0では、グローバルソートがGAになります。この機能により、TiKVのリソース消費が削減され、 `IMPORT INTO`のパフォーマンスと安定性が大幅に向上します。グローバルソートを有効にすると、 `IMPORT INTO`タスクそれぞれで40TiB以内のデータのインポートがサポートされます。

    詳細については[ドキュメント](/tidb-global-sort.md)参照してください。

## 互換性の変更 {#compatibility-changes}

> **注記：**
>
> このセクションでは、v7.6.0から最新バージョン（v8.0.0）にアップグレードする際に知っておくべき互換性の変更点について説明します。v7.5.0以前のバージョンから最新バージョンにアップグレードする場合は、中間バージョンで導入された互換性の変更点も確認する必要があるかもしれません。

-   TiUPによってデプロイされたデフォルトの Prometheus バージョンを 2.27.1 から 2.49.1 にアップグレードします。
-   TiUPによってデプロイされたデフォルトの Grafana バージョンを 7.5.11 から 7.5.17 にアップグレードします。
-   GA ではないがデフォルトで有効になっている監視関連のスケジューラを削除します[＃7765](https://github.com/tikv/pd/pull/7765) @ [rleungx](https://github.com/rleungx)

### 行動の変化 {#behavior-changes}

-   ユーザーの潜在的な接続問題を防ぐために、Security強化モード (SEM) で[`require_secure_transport`](/system-variables.md#require_secure_transport-new-in-v610)から`ON`設定を禁止します[＃47665](https://github.com/pingcap/tidb/issues/47665) @ [天菜まお](https://github.com/tiancaiamao)
-   DMでは、暗号化と復号化に使用する固定の秘密鍵が削除され、暗号化と復号化に使用する秘密鍵をカスタマイズできるようになります。アップグレード前に[データソース構成](/dm/dm-source-configuration-file.md)と[移行タスクの構成](/dm/task-configuration-file-full.md)で暗号化されたパスワードを使用している場合は、追加の操作については[DM 暗号化と復号化用の秘密鍵をカスタマイズする](/dm/dm-customized-secret-key.md)のアップグレード手順を参照してください[＃9492](https://github.com/pingcap/tiflow/issues/9492) @ [D3ハンター](https://github.com/D3Hunter)
-   バージョン8.0.0より前では、 `ADD INDEX`と`CREATE INDEX` （ `tidb_ddl_enable_fast_reorg = ON` ）のアクセラレーションを有効にすると、エンコードされたインデックスキーはTiKVにデータを取り込みますが、その際の同時実行数は固定で`16`であり、下流のTiKV容量に応じて動的に調整することはできませんでした。バージョン8.0.0以降では、システム変数[`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt)使用して同時実行数を調整できます。デフォルト値は`4`です。以前のデフォルト値`16`と比較して、新しいデフォルト値ではインデックス付きキーと値のペアを取り込む際のパフォーマンスが低下します。このシステム変数は、クラスターのワークロードに応じて調整できます。

### MySQLの互換性 {#mysql-compatibility}

-   `KEY`パーティション タイプは、パーティション フィールドの空のリストを持つステートメントをサポートします。これは、MySQL の動作と一致しています。

### システム変数 {#system-variables}

| 変数名                                                                                                                       | タイプを変更   | 説明                                                                                                                                                                                                                        |
| ------------------------------------------------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`tidb_disable_txn_auto_retry`](/system-variables.md#tidb_disable_txn_auto_retry)                                         | 非推奨      | バージョン8.0.0以降、このシステム変数は非推奨となり、TiDBは楽観的トランザクションの自動再試行をサポートしなくなりました[悲観的なトランザクションモード](/pessimistic-transaction.md)使用することをお勧めします。楽観的ミスティックトランザクションの競合が発生した場合は、エラーをキャプチャしてアプリケーションでトランザクションを再試行できます。                            |
| `tidb_ddl_version`                                                                                                        | 名前変更     | TiDB DDL V2 を有効にするかどうかを制御します。v8.0.0 以降、この変数の名前は、その目的をより適切に反映するために[`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-new-in-v800)に変更されました。                                               |
| [`tidb_enable_collect_execution_info`](/system-variables.md#tidb_enable_collect_execution_info)                           | 修正済み     | [インデックスの使用統計](/information-schema/information-schema-tidb-index-usage.md)記録するかどうかのコントロールを追加します。デフォルト値は`ON`です。                                                                                                             |
| [`tidb_redact_log`](/system-variables.md#tidb_redact_log)                                                                 | 修正済み     | TiDBログおよびスローログを記録する際に、SALテキスト内のユーザー情報の処理方法を制御します。値のオプションは`OFF` （ログ内のユーザー情報を処理しない）と`ON` （ログ内のユーザー情報を非表示にする）です。ログ内のユーザー情報の処理をより柔軟にするため、v8.0.0ではログ情報のマーキングをサポートするオプション`MARKER`が追加されました。                                      |
| [`div_precision_increment`](/system-variables.md#div_precision_increment-new-in-v800)                                     | 新しく追加された | `/`演算子を用いた除算の結果の桁数を増加させる桁数を制御します。この変数はMySQLと同じです。                                                                                                                                                                         |
| [`tidb_dml_type`](/system-variables.md#tidb_dml_type-new-in-v800)                                                         | 新しく追加された | DML文の実行モードを制御します。値のオプションは`"standard"`と`"bulk"`です。                                                                                                                                                                         |
| [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-new-in-v800)     | 新しく追加された | 統計の自動収集タスクをスケジュールするために、優先キューを有効にするかどうかを制御します。この変数を有効にすると、TiDBは統計を最も必要とするテーブルの統計収集を優先します。                                                                                                                                  |
| [`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-new-in-v800)               | 新しく追加された | TiDBが並列HashAggアルゴリズムのディスクスピルをサポートするかどうかを制御します`ON`の場合、並列HashAggアルゴリズムのディスクスピルがトリガーされます。この機能が将来のリリースで一般公開された時点で、この変数は非推奨となります。                                                                                              |
| [`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-new-in-v800)                         | 新しく追加された | [TiDB はテーブル作成を高速化します](/accelerated-table-creation.md)有効にするかどうかを制御します。有効にするには値を`ON`に、無効にするには`OFF`に設定します。デフォルト値は`ON`です。この変数を有効にすると、TiDB は[`CREATE TABLE`](/sql-statements/sql-statement-create-table.md)を使用してテーブル作成を高速化します。 |
| [`tidb_load_binding_timeout`](/system-variables.md#tidb_load_binding_timeout-new-in-v800)                                 | 新しく追加された | バインディングの読み込みのタイムアウトを制御します。バインディングの読み込みの実行時間がこの値を超えると、読み込みは停止します。                                                                                                                                                          |
| [`tidb_low_resolution_tso_update_interval`](/system-variables.md#tidb_low_resolution_tso_update_interval-new-in-v800)     | 新しく追加された | TiDB [キャッシュタイムスタンプ](/system-variables.md#tidb_low_resolution_tso)更新間隔を制御します。                                                                                                                                              |
| [`tidb_opt_ordering_index_selectivity_ratio`](/system-variables.md#tidb_opt_ordering_index_selectivity_ratio-new-in-v800) | 新しく追加された | SQL文に`ORDER BY`または`LIMIT`句があり、一部のフィルタ条件がインデックスでカバーされていない場合に、SQL文`ORDER BY`一致するインデックスの推定行数を制御します。デフォルト値は`-1`で、このシステム変数は無効です。                                                                                               |
| [`tidb_opt_use_invisible_indexes`](/system-variables.md#tidb_opt_use_invisible_indexes-new-in-v800)                       | 新しく追加された | 現在のセッションにおいて、オプティマイザがクエリの最適化に[目に見えないインデックス](/sql-statements/sql-statement-create-index.md#invisible-index)選択できるかどうかを制御します。この変数が`ON`に設定されている場合、オプティマイザはセッションにおいてクエリの最適化に非表示のインデックスを選択できます。                                 |
| [`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-new-in-v800)                                       | 新しく追加された | スキーマ情報のキャッシュに使用できるメモリの上限を制御し、過剰なメモリ消費を回避します。この機能を有効にすると、LRUアルゴリズムを使用して必要なテーブルがキャッシュされ、スキーマ情報によって占有されるメモリが効果的に削減されます。                                                                                                      |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーションパラメータ                                                                                                                                               | タイプを変更   | 説明                                                                                                                                                                                               |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| TiDB           | [`instance.tidb_enable_collect_execution_info`](/tidb-configuration-file.md#tidb_enable_collect_execution_info)                                               | 修正済み     | [インデックスの使用統計](/information-schema/information-schema-tidb-index-usage.md)記録するかどうかのコントロールを追加します。デフォルト値は`true`です。                                                                                  |
| TiDB           | [`tls-version`](/tidb-configuration-file.md#tls-version)                                                                                                      | 修正済み     | このパラメータは`"TLSv1.0"`と`"TLSv1.1"`サポートしなくなりました。現在は`"TLSv1.2"`と`"TLSv1.3"`のみをサポートします。                                                                                                                |
| TiDB           | [`log.file.compression`](/tidb-configuration-file.md#compression-new-in-v800)                                                                                 | 新しく追加された | ポーリングログの圧縮形式を指定します。デフォルト値はnullで、ポーリングログは圧縮されません。                                                                                                                                                 |
| TiDB           | [`log.general-log-file`](/tidb-configuration-file.md#general-log-file-new-in-v800)                                                                            | 新しく追加された | 一般ログを保存するファイルを指定します。デフォルトはnullで、一般ログはインスタンスファイルに書き込まれます。                                                                                                                                         |
| TiDB           | [`tikv-client.enable-replica-selector-v2`](/tidb-configuration-file.md#enable-replica-selector-v2-new-in-v800)                                                | 新しく追加された | RPCリクエストをTiKVに送信する際に、新しいバージョンのリージョンレプリカセレクタを使用するかどうかを制御します。デフォルト値は`true`です。                                                                                                                      |
| TiKV           | [`log-backup.initial-scan-rate-limit`](/tikv-configuration-file.md#initial-scan-rate-limit-new-in-v620)                                                       | 修正済み     | 最小値として`1MiB`の制限を追加します。                                                                                                                                                                           |
| TiKV           | [`raftstore.store-io-pool-size`](/tikv-configuration-file.md#store-io-pool-size-new-in-v530)                                                                  | 修正済み     | TiKV のパフォーマンスを向上させるためにデフォルト値を`0`から`1`に変更します。つまり、StoreWriter スレッド プールのサイズはデフォルトで`1`になります。                                                                                                         |
| TiKV           | [`rocksdb.defaultcf.titan.blob-cache-size`](/tikv-configuration-file.md#blob-cache-size)                                                                      | 修正済み     | バージョン8.0.0以降、TiKVは設定項目`shared-blob-cache`を導入し、デフォルトで有効になっているため、 `blob-cache-size`別途設定する必要はありません`blob-cache-size`の設定は、 `shared-blob-cache` `false`に設定されている場合にのみ有効になります。                           |
| TiKV           | [`rocksdb.titan.max-background-gc`](/tikv-configuration-file.md#max-background-gc)                                                                            | 修正済み     | Titan GC プロセスによるスレッド リソースの占有を減らすために、デフォルト値を`4`から`1`に変更します。                                                                                                                                       |
| TiKV           | [`security.encryption.master-key.vendor`](/encryption-at-rest.md#specify-a-master-key-via-kms)                                                                | 修正済み     | サービス プロバイダーの使用可能なタイプとして`gcp`追加します。                                                                                                                                                               |
| TiKV           | [`storage.block-cache.low-pri-pool-ratio`](/tikv-configuration-file.md#low-pri-pool-ratio-new-in-v800)                                                        | 新しく追加された | Titanコンポーネントが使用できるブロックキャッシュ全体の割合を指定します。デフォルト値は`0.2`です。                                                                                                                                           |
| TiKV           | [`rocksdb.defaultcf.titan.shared-blob-cache`](/tikv-configuration-file.md#shared-blob-cache-new-in-v800)                                                      | 新しく追加された | Titan BLOBファイルとRocksDBブロックファイルの共有キャッシュを有効にするかどうかを制御します。デフォルト値は`true`です。                                                                                                                          |
| TiKV           | [`security.encryption.master-key.gcp.credential-file-path`](/encryption-at-rest.md#specify-a-master-key-via-kms)                                              | 新しく追加された | `security.encryption.master-key.vendor`が`gcp`場合、Google Cloud 認証認証情報ファイルへのパスを指定します。                                                                                                               |
| PD             | [`schedule.enable-heartbeat-breakdown-metrics`](/pd-configuration-file.md#enable-heartbeat-breakdown-metrics-new-in-v800)                                     | 新しく追加された | リージョンハートビートの内訳メトリクスを有効にするかどうかを制御します。これらのメトリクスは、リージョンハートビート処理の各段階で消費された時間を測定し、監視による分析を容易にします。デフォルト値は`true`です。                                                                                     |
| PD             | [`schedule.enable-heartbeat-concurrent-runner`](/pd-configuration-file.md#enable-heartbeat-concurrent-runner-new-in-v800)                                     | 新しく追加された | リージョンハートビートの非同期並行処理を有効にするかどうかを制御します。有効にすると、独立したエグゼキューターがリージョンハートビートリクエストを非同期かつ並行して処理するため、ハートビート処理のスループットが向上し、レイテンシーが短縮されます。デフォルト値は`true`です。                                                      |
| TiDB Lightning | [`tikv-importer.duplicate-resolution`](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#the-old-version-of-conflict-detection-deprecated-in-v800) | 非推奨      | 物理インポートモードで一意キーの競合を検出して解決するかどうかを制御します。v8.0.0以降では、 [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)に置き換えられます。                                           |
| TiDB Lightning | [`conflict.precheck-conflict-before-import`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)                                             | 新しく追加された | インポート前の競合検出を有効にするかどうかを制御します。これは、TiDBにインポートする前にデータ内の競合をチェックします。このパラメータのデフォルト値は`false`で、 TiDB Lightningはデータのインポート後にのみ競合をチェックします。このパラメータは、物理インポートモード（ `tikv-importer.backend = "local"` ）でのみ使用できます。 |
| TiDB Lightning | [`logical-import-batch-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)                                                            | 新しく追加された | 論理インポートモードにおいて、トランザクションごとに挿入される行の最大数を制御します。デフォルト値は`65536`行です。                                                                                                                                    |
| TiDB Lightning | [`logical-import-batch-size`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)                                                            | 新しく追加された | 論理インポートモードにおいて、下流TiDBサーバーで実行される各SQLクエリの最大サイズを制御します。デフォルト値は`"96KiB"`です。単位はKB、KiB、MB、またはMiBです。                                                                                                     |
| データ移行          | [`secret-key-path`](/dm/dm-master-configuration-file.md)                                                                                                      | 新しく追加された | アップストリームおよびダウンストリームのパスワードの暗号化と復号化に使用する秘密鍵のファイルパスを指定します。ファイルには、64文字の16進数AES-256秘密鍵が含まれている必要があります。                                                                                                 |
| TiCDC          | [`debezium-disable-schema`](/ticdc/ticdc-changefeed-config.md)                                                                                                | 新しく追加された | スキーマ情報の出力を無効にするかどうかを制御します。このパラメータは、シンクタイプがMQで、出力プロトコルがDebeziumの場合にのみ有効です。                                                                                                                        |
| TiCDC          | [`tls-certificate-file`](/ticdc/ticdc-sink-to-pulsar.md)                                                                                                      | 新しく追加された | Pulsar が TLS 暗号化伝送を有効にするときに必要な、クライアント上の暗号化された証明書ファイルへのパスを指定します。                                                                                                                                  |
| TiCDC          | [`tls-key-file-path`](/ticdc/ticdc-sink-to-pulsar.md)                                                                                                         | 新しく追加された | Pulsar が TLS 暗号化伝送を有効にするときに必要な、クライアント上の暗号化された秘密鍵へのパスを指定します。                                                                                                                                      |

### システムテーブル {#system-tables}

-   TiDB ノードのインデックス使用統計を記録するために、新しいシステム テーブル[`INFORMATION_SCHEMA.TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md)と[`INFORMATION_SCHEMA.CLUSTER_TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md#cluster_tidb_index_usage)追加します。
-   新しいシステム スキーマ[`sys`](/sys-schema/sys-schema.md)と、TiDB の最後の起動以降に使用されていないインデックスを記録する新しいビュー[`sys.schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md)追加します。

## 非推奨の機能 {#deprecated-features}

-   バージョン8.0.0以降、システム変数[`tidb_disable_txn_auto_retry`](/system-variables.md#tidb_disable_txn_auto_retry)非推奨となり、TiDBは楽観的トランザクションの自動再試行をサポートしなくなりました。代替策として、楽観的トランザクションの競合が発生した場合は、エラーをキャプチャしてアプリケーション内でトランザクションを再試行するか、代わりに[悲観的なトランザクションモード](/pessimistic-transaction.md)使用してください。
-   v8.0.0以降、TiDBはTLSv1.0およびTLSv1.1プロトコルをサポートしなくなりました。TLSをTLSv1.2またはTLSv1.3にアップグレードする必要があります。
-   TiDB Lightning v8.0.0以降、物理インポートモードの[競合検出の古いバージョン](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#the-old-version-of-conflict-detection-deprecated-in-v800)戦略は非推奨となり、 [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md)パラメータを使用して論理インポートモードと物理インポートモードの両方の競合検出戦略を制御できるようになりました。旧バージョンの競合検出用の[`duplicate-resolution`](/tidb-lightning/tidb-lightning-configuration.md)パラメータは、将来のリリースで削除される予定です。
-   以降のリリースでは[実行計画バインディングの自動進化](/sql-plan-management.md#baseline-evolution)再設計する予定であり、関連する変数と動作が変更されます。

## 改善点 {#improvements}

-   TiDB

    -   `CREATE TABLE` DDL文の実行パフォーマンスを10倍向上し、線形スケーラビリティ[＃50052](https://github.com/pingcap/tidb/issues/50052) @ [GMHDBJD](https://github.com/GMHDBJD)をサポートします。
    -   16 `IMPORT INTO ... FROM FILE`タスクの同時送信をサポートし、ターゲットテーブルへの一括データインポートを容易にし、データファイル[＃49008](https://github.com/pingcap/tidb/issues/49008) @ [D3ハンター](https://github.com/D3Hunter)のインポートの効率とパフォーマンスを大幅に向上させます。
    -   `Sort`オペレータ[＃47733](https://github.com/pingcap/tidb/issues/47733) @ [xzhangxian1008](https://github.com/xzhangxian1008)のディスクへのデータ書き込みのパフォーマンスを向上
    -   ディスクへのデータのスピル中にクエリをキャンセルすることをサポートし、データスピル機能[＃50511](https://github.com/pingcap/tidb/issues/50511) @ [wshwsh12](https://github.com/wshwsh12)の終了メカニズムを最適化します。
    -   複数の等号条件を持つテーブル結合クエリを処理する際に、部分条件に一致するインデックスを使用してインデックス結合を構築することをサポートします[＃47233](https://github.com/pingcap/tidb/issues/47233) @ [ウィノロス](https://github.com/winoros)
    -   インデックスマージの機能を強化して、クエリ内のソート要件を識別し、ソート要件を満たすインデックスを選択します[＃48359](https://github.com/pingcap/tidb/issues/48359) @ [アイリンキッド](https://github.com/AilinKid)
    -   `Apply`演算子が同時に実行されない場合、TiDBでは`SHOW WARNINGS` [＃50256](https://github.com/pingcap/tidb/issues/50256) @ [ホーキングレイ](https://github.com/hawkingrei)を実行することで同時実行をブロックする演算子の名前を表示できます。
    -   すべてのインデックスが`point get`クエリ[＃50184](https://github.com/pingcap/tidb/issues/50184) @ [エルサ0520](https://github.com/elsa0520)をサポートしている場合、クエリに最適なインデックスを選択して`point get`クエリのインデックス選択を最適化します。
    -   TiKV の高負荷時に広範囲にわたるタイムアウトを回避するために、統計を同期的にロードするタスクの優先度を一時的に高く調整します。タイムアウトにより、統計がロードされない可能性があります[＃50332](https://github.com/pingcap/tidb/issues/50332) @ [ウィノロス](https://github.com/winoros)
    -   `PREPARE`文が実行計画キャッシュにヒットしない場合、TiDBでは`SHOW WARNINGS` [＃50407](https://github.com/pingcap/tidb/issues/50407) @ [ホーキングレイ](https://github.com/hawkingrei)を実行することでその理由を確認できます。
    -   同じデータ行が複数回更新された場合のクエリ推定情報の精度を向上[＃47523](https://github.com/pingcap/tidb/issues/47523) @ [テリー・パーセル](https://github.com/terry1purcell)
    -   インデックスマージは`AND`述語[＃51778](https://github.com/pingcap/tidb/issues/51778) @ [時間と運命](https://github.com/time-and-fate)に複数値インデックスと`OR`演算子を埋め込むことをサポートします。
    -   `force-init-stats` `true`に設定すると、TiDB は起動時にサービスを提供する前に統計情報の初期化が完了するのを待ちます。この設定により HTTP サーバーの起動がブロックされなくなり、ユーザーは[＃50854](https://github.com/pingcap/tidb/issues/50854) @ [ホーキングレイ](https://github.com/hawkingrei)で監視を継続できます。
    -   MemoryTrackerは`IndexLookup`演算子[＃45901](https://github.com/pingcap/tidb/issues/45901) @ [ソロツグ](https://github.com/solotzg)のメモリ使用量を追跡できます
    -   MemoryTrackerは`MemTableReaderExec`演算子[＃51456](https://github.com/pingcap/tidb/issues/51456) @ [wshwsh12](https://github.com/wshwsh12)のメモリ使用量を追跡できます
    -   PD からリージョンを一括ロードすることをサポートし、大規模なテーブル[＃51326](https://github.com/pingcap/tidb/issues/51326) @ [シーライズ](https://github.com/SeaRise)をクエリするときに KV 範囲からリージョンへの変換プロセスを高速化します。
    -   システムテーブル`INFORMATION_SCHEMA.TABLES`のクエリパフォーマンス`INFORMATION_SCHEMA.STATISTICS`最適化しまし`INFORMATION_SCHEMA.KEY_COLUMN_USAGE` 。以前のバージョンと比較して、パフォーマンス[ywqzzy](https://github.com/ywqzzy)最大100倍向上しました[＃50305](https://github.com/pingcap/tidb/issues/50305) @ `INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS`

-   TiKV

    -   TSOの検証と検出を強化して、構成または操作が不適切な場合のクラスターTSOの堅牢性を向上させます[＃16545](https://github.com/tikv/tikv/issues/16545) @ [cfzjywxk](https://github.com/cfzjywxk)
    -   悲観的ロックのクリーンアップロジックを最適化して、コミットされていないトランザクション[＃16158](https://github.com/tikv/tikv/issues/16158) @ [cfzjywxk](https://github.com/cfzjywxk)の処理パフォーマンスを向上させます。
    -   TiKVの統合ヘルスコントロールを導入し[＃1167](https://github.com/tikv/client-go/issues/1167)異常な単一TiKVノードがクラスタアクセスパフォーマンスに与える影響を軽減します。この最適化を無効にするには、 [`tikv-client.enable-replica-selector-v2`](/tidb-configuration-file.md#enable-replica-selector-v2-new-in-v800)を`false`に設定します。5 [＃16297](https://github.com/tikv/tikv/issues/16297) [＃1104](https://github.com/tikv/client-go/issues/1104) @ [ミョンケミンタ](https://github.com/MyonKeminta) @ [ジグアン](https://github.com/zyguan) @ [crazycs520](https://github.com/crazycs520)
    -   PDクライアントはメタデータstorageインターフェースを使用して、以前のグローバル構成インターフェース[＃14484](https://github.com/tikv/tikv/issues/14484) @ [HuSharp](https://github.com/HuSharp)を置き換えます。
    -   write cf stats [＃16245](https://github.com/tikv/tikv/issues/16245) @ [コナー1996](https://github.com/Connor1996)を通じてデータの読み込み動作を決定することでスキャンのパフォーマンスを向上させます。
    -   Raft conf 変更プロセス中にノードが削除され、投票者が降格されていないか最新のハートビートをチェックして、この動作によってリージョンがアクセス不能にならないことを確認します[＃15799](https://github.com/tikv/tikv/issues/15799) @ [トニー・シュッキ](https://github.com/tonyxuqqi)
    -   パイプラインDML [＃16291](https://github.com/tikv/tikv/issues/16291) @ [エキシウム](https://github.com/ekexium)のFlushおよびBufferBatchGetインターフェースを追加
    -   cgroup の CPU とメモリの制限[＃16392](https://github.com/tikv/tikv/issues/16392) @ [ピンアンドビー](https://github.com/pingandb)の監視とアラートを追加します
    -   リージョンワーカーとスナップショット生成ワーカー[＃16562](https://github.com/tikv/tikv/issues/16562) @ [コナー1996](https://github.com/Connor1996)の CPU 監視を追加します。
    -   ピアのスローログを追加し、メッセージ[＃16600](https://github.com/tikv/tikv/issues/16600) @ [コナー1996](https://github.com/Connor1996)を保存します

-   PD

    -   PDクライアントのサービス検出機能を強化して、高可用性と負荷分散を改善します[＃7576](https://github.com/tikv/pd/issues/7576) @ [キャビンフィーバーB](https://github.com/CabinfeverB)
    -   PDクライアント[＃7673](https://github.com/tikv/pd/issues/7673)の再試行メカニズムを強化[Jmポテト](https://github.com/JmPotato)
    -   cgroup の CPU とメモリの制限の監視とアラートを追加[＃7716](https://github.com/tikv/pd/issues/7716) [＃7918](https://github.com/tikv/pd/issues/7918) @ [ピンアンドビー](https://github.com/pingandb) @ [rleungx](https://github.com/rleungx)
    -   etcd 使用時のパフォーマンスと高可用性の向上[＃7738](https://github.com/tikv/pd/issues/7738) [＃7724](https://github.com/tikv/pd/issues/7724) [＃7689](https://github.com/tikv/pd/issues/7689) @ [lhy1024](https://github.com/lhy1024)
    -   ハートビートの監視メトリックを追加して、パフォーマンスのボトルネックをより適切に分析します[＃7868](https://github.com/tikv/pd/issues/7868) @ [ノルーシュ](https://github.com/nolouch)
    -   etcdリーダーのPDリーダーへの影響を軽減する[＃7499](https://github.com/tikv/pd/issues/7499) @ [Jmポテト](https://github.com/JmPotato) @ [HuSharp](https://github.com/HuSharp)
    -   不健全な etcd ノードの検出メカニズムを強化する[＃7730](https://github.com/tikv/pd/issues/7730) @ [Jmポテト](https://github.com/JmPotato) @ [HuSharp](https://github.com/HuSharp)
    -   pd-ctl [＃7767](https://github.com/tikv/pd/issues/7767) @ [ノルーシュ](https://github.com/nolouch)の GC セーフポイントの出力を最適化します。
    -   ホットスポットスケジューラ[＃7877](https://github.com/tikv/pd/issues/7877) @ [lhy1024](https://github.com/lhy1024)の履歴ウィンドウ構成の動的な変更をサポート
    -   演算子[＃7837](https://github.com/tikv/pd/issues/7837) @ [リーヴルス](https://github.com/Leavrth)作成時のロック競合の問題を軽減します
    -   GRPC 構成を調整して可用性を向上[＃7821](https://github.com/tikv/pd/issues/7821) @ [rleungx](https://github.com/rleungx)

-   TiFlash

    -   `JSON_EXTRACT()`関数[＃8510](https://github.com/pingcap/tiflash/issues/8510) @ [シーライズ](https://github.com/SeaRise)の`json_path`の引数に非定数値の使用をサポート
    -   `JSON_LENGTH(json, path)`機能[＃8711](https://github.com/pingcap/tiflash/issues/8711)を[シーライズ](https://github.com/SeaRise)でサポート

-   ツール

    -   バックアップと復元 (BR)

        -   `br`コマンドラインツールに新しい復元パラメータ`--load-stats`導入し、統計[＃50568](https://github.com/pingcap/tidb/issues/50568) @ [リーヴルス](https://github.com/Leavrth)を復元するかどうかを制御します。
        -   コマンドラインツール`br`に新しい復元パラメータ`--tikv-max-restore-concurrency`を導入しました。このパラメータは、TiKVノードごとにダウンロードおよび取り込み可能なファイルの最大数を制御します。また、ジョブキューの最大長を制御することで、 BRノードのメモリ消費量も制御します[＃51621](https://github.com/pingcap/tidb/issues/51621) @ [3ポイントシュート](https://github.com/3pointer)
        -   粗粒度のリージョン分散アルゴリズムを有効にして同時パラメータ[＃50701](https://github.com/pingcap/tidb/issues/50701) @ [3ポイントシュート](https://github.com/3pointer)を適応的に取得することで、復元パフォーマンスが向上します。
        -   `br` [＃50927](https://github.com/pingcap/tidb/issues/50927) @ [リドリスR](https://github.com/RidRisR)のコマンドラインヘルプ情報に`log`コマンドを表示します
        -   リストアプロセス中にテーブルIDを事前割り当てすることで、テーブルIDの再利用を最大化し、リストアパフォーマンスを向上します[＃51736](https://github.com/pingcap/tidb/issues/51736) @ [リーヴルス](https://github.com/Leavrth)
        -   OOM の問題を回避するために、 BRを使用するときは TiDB 内の GCメモリ制限チューナー機能を無効にします[＃51078](https://github.com/pingcap/tidb/issues/51078) @ [リーヴルス](https://github.com/Leavrth)
        -   より効率的なアルゴリズム[＃50613](https://github.com/pingcap/tidb/issues/50613) @ [リーヴルス](https://github.com/Leavrth)を使用して、データ復元中に SST ファイルをマージする速度を改善します
        -   データ復元中にデータベースをバッチで作成するサポート[＃50767](https://github.com/pingcap/tidb/issues/50767) @ [リーヴルス](https://github.com/Leavrth)
        -   ログバックアップ[＃51046](https://github.com/pingcap/tidb/issues/51046) @ [ユジュンセン](https://github.com/YuJuncen)中に、ログとメトリックのグローバルチェックポイントの進行に影響を与える最も遅いリージョンの情報を出力します。
        -   大規模なデータセット[＃48301](https://github.com/pingcap/tidb/issues/48301) @ [リーヴルス](https://github.com/Leavrth)シナリオで`RESTORE`ステートメントのテーブル作成パフォーマンスを向上

    -   TiCDC

        -   TiCDCがデータ[＃10386](https://github.com/pingcap/tiflow/issues/10386) [リデジュ](https://github.com/lidezhu)で複製する際のメモリ消費を削減するために、 `RowChangedEvent`のメモリ消費を最適化します。
        -   変更フィードタスク[＃10499](https://github.com/pingcap/tiflow/issues/10499) @ [3エースショーハンド](https://github.com/3AceShowHand)作成および再開時に、start-ts パラメータが有効であることを確認します。

    -   TiDB データ移行 (DM)

        -   MariaDBプライマリ-セカンダリレプリケーションシナリオにおいて、移行パスがMariaDBプライマリインスタンス -&gt; MariaDBセカンダリインスタンス -&gt; DM -&gt; TiDBの場合、 `gtid_strict_mode = off`でMariaDBセカンダリインスタンスのGTIDが厳密に増加していない場合（例えば、MariaDBセカンダリインスタンスへのデータ書き込みがある場合）、DMタスクはエラー`less than global checkpoint position`を報告します。v8.0.0以降、TiDBはこのシナリオに対応しており、データは正常に下流に移行できます[＃10741](https://github.com/pingcap/tiflow/issues/10741) @ [okJiang](https://github.com/okJiang)

    -   TiDB Lightning

        -   [`logical-import-batch-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task) [＃46607](https://github.com/pingcap/tidb/issues/46607) @ [ケニーtm](https://github.com/kennytm)を使用して論理インポート モードでバッチ内の最大行数を構成することをサポート
        -   TiDB LightningはTiFlashの容量が不足するとエラーを報告します[＃50324](https://github.com/pingcap/tidb/issues/50324) @ [okJiang](https://github.com/okJiang)

## バグ修正 {#bug-fixes}

-   TiDB

    -   データの変更がないのに`auto analyze`が複数回トリガーされる問題を修正[＃51775](https://github.com/pingcap/tidb/issues/51775) @ [ハイラスティン](https://github.com/Rustin170506)
    -   `auto analyze`同時実行が[＃51749](https://github.com/pingcap/tidb/issues/51749) @ [ホーキングレイ](https://github.com/hawkingrei)に誤って設定されている問題を修正
    -   単一のSQL文を使用して複数のインデックスを追加することによって発生するインデックスの不整合の問題を修正[＃51746](https://github.com/pingcap/tidb/issues/51746) @ [接線](https://github.com/tangenta)
    -   クエリで`NATURAL JOIN` [＃32044](https://github.com/pingcap/tidb/issues/32044) @ [アイリンキッド](https://github.com/AilinKid)が使用される場合に発生する可能性のある`Column ... in from clause is ambiguous`エラーを修正します
    -   TiDB が`group by` [＃38756](https://github.com/pingcap/tidb/issues/38756) @ [ハイラスティン](https://github.com/Rustin170506)の定数値を誤って削除することによる間違ったクエリ結果の問題を修正しました
    -   `LEADING`ヒントが`UNION ALL`ステートメント[＃50067](https://github.com/pingcap/tidb/issues/50067) @ [ホーキングレイ](https://github.com/hawkingrei)で有効にならない問題を修正しました
    -   `BIT`型の列が一部の関数の計算に関係する場合にデコード失敗によりクエリエラーが発生する可能性がある問題を修正しました[＃49566](https://github.com/pingcap/tidb/issues/49566) [＃50850](https://github.com/pingcap/tidb/issues/50850) [＃50855](https://github.com/pingcap/tidb/issues/50855) @ [ジフハウス](https://github.com/jiyfhust)
    -   PD [＃50152](https://github.com/pingcap/tidb/issues/50152) @ [ジムララ](https://github.com/zimulala)との相互作用の問題により、 `tiup cluster upgrade/start`使用してローリング アップグレードを実行すると TiDB がpanicになる可能性がある問題を修正しました。
    -   `ORDER BY`句で`UNIQUE`インデックス検索を実行するとエラー[＃49920](https://github.com/pingcap/tidb/issues/49920) @ [ジャッキーsp](https://github.com/jackysp)が発生する可能性がある問題を修正しました。
    -   定数伝播[＃49440](https://github.com/pingcap/tidb/issues/49440) @ [ウィノロス](https://github.com/winoros)で`ENUM`または`SET`型を処理するときに TiDB が間違ったクエリ結果を返す問題を修正しました
    -   クエリに Apply 演算子が含まれており、 `fatal error: concurrent map writes`エラーが[＃50347](https://github.com/pingcap/tidb/issues/50347) @ [シーライズ](https://github.com/SeaRise)で発生すると TiDB がpanic可能性がある問題を修正しました。
    -   文字列型の変数の`SET_VAR`制御が無効になる可能性がある問題を修正[＃50507](https://github.com/pingcap/tidb/issues/50507) @ [qw4990](https://github.com/qw4990)
    -   `tidb_sysdate_is_now` `1` [＃49299](https://github.com/pingcap/tidb/issues/49299) @ [ホーキングレイ](https://github.com/hawkingrei)に設定されている場合に、 `SYSDATE()`関数がプラン キャッシュ内の時間を誤って使用する問題を修正しました。
    -   `CREATE GLOBAL BINDING`文を実行するときに、スキーマ名が大文字の場合、バインディングが有効にならない問題を修正しました[＃50646](https://github.com/pingcap/tidb/issues/50646) @ [qw4990](https://github.com/qw4990)
    -   `Index Path`重複したインデックス[＃50496](https://github.com/pingcap/tidb/issues/50496) @ [アイリンキッド](https://github.com/AilinKid)を選択する問題を修正
    -   `CREATE GLOBAL BINDING`文に`IN()` [＃43192](https://github.com/pingcap/tidb/issues/43192) @ [キング・ディラン](https://github.com/King-Dylan)が含まれている場合に`PLAN REPLAYER`バインディングのロードに失敗する問題を修正しました
    -   複数の`analyze`タスクが失敗した場合、失敗理由が正しく記録されない問題を修正[＃50481](https://github.com/pingcap/tidb/issues/50481) @ [ハイラスティン](https://github.com/Rustin170506)
    -   `tidb_stats_load_sync_wait` [ジフハウス](https://github.com/jiyfhust)で[＃50872](https://github.com/pingcap/tidb/issues/50872)効かない問題を修正
    -   複数のレベルの`max_execute_time`設定が互いに干渉する問題を修正[＃50914](https://github.com/pingcap/tidb/issues/50914) @ [ジフハウス](https://github.com/jiyfhust)
    -   統計[＃50835](https://github.com/pingcap/tidb/issues/50835) @ [ハイラスティン](https://github.com/Rustin170506)の同時更新によって発生するスレッドの安全性の問題を修正しました
    -   パーティションテーブルで`auto analyze`実行すると TiDB がpanic可能性がある問題を修正[＃51187](https://github.com/pingcap/tidb/issues/51187) @ [ハイラスティン](https://github.com/Rustin170506)
    -   SQL 文の`IN()`異なる数の値[＃51222](https://github.com/pingcap/tidb/issues/51222) @ [ホーキングレイ](https://github.com/hawkingrei)が含まれている場合に SQL バインディングが機能しない可能性がある問題を修正しました。
    -   TiDBが式[＃43527](https://github.com/pingcap/tidb/issues/43527) @ [ハイラスティン](https://github.com/Rustin170506)内のシステム変数の型を正しく変換できない問題を修正
    -   `force-init-stats` [＃51473](https://github.com/pingcap/tidb/issues/51473) @ [ホーキングレイ](https://github.com/hawkingrei)に設定されている場合に TiDB が対応するポートを listen しない問題を修正しました
    -   `determinate`モード（ `tidb_opt_objective='determinate'` ）でクエリに述語が含まれていない場合、統計がロードされない可能性がある問題を修正しました[＃48257](https://github.com/pingcap/tidb/issues/48257) @ [時間と運命](https://github.com/time-and-fate)
    -   `init-stats`プロセスが TiDB をpanicに陥らせ、 `load stats`プロセスが[＃51581](https://github.com/pingcap/tidb/issues/51581) @ [ホーキングレイ](https://github.com/hawkingrei)で終了する可能性がある問題を修正しました。
    -   `IN()`述語に`NULL` [＃51560](https://github.com/pingcap/tidb/issues/51560) @ [ウィノロス](https://github.com/winoros)が含まれている場合にクエリ結果が正しくない問題を修正しました
    -   DDLタスクに複数のテーブルが含まれる場合に、ブロックされたDDL文がMDLビューに表示されない問題を修正[＃47743](https://github.com/pingcap/tidb/issues/47743) @ [wjhuang2016](https://github.com/wjhuang2016)
    -   テーブル上の`ANALYZE`タスクのうち`processed_rows` 、そのテーブルの合計行数[＃50632](https://github.com/pingcap/tidb/issues/50632) @ [ホーキングレイ](https://github.com/hawkingrei)を超える可能性がある問題を修正しました。
    -   `HashJoin`演算子がディスク[＃50841](https://github.com/pingcap/tidb/issues/50841) @ [wshwsh12](https://github.com/wshwsh12)にスピルできない場合に発生する可能性のある goroutine リークの問題を修正しました。
    -   CTEクエリのメモリ使用量が制限[＃50337](https://github.com/pingcap/tidb/issues/50337) @ [グオシャオゲ](https://github.com/guo-shaoge)を超えたときに発生するゴルーチンリークの問題を修正しました
    -   集計関数をグループ計算に使用すると発生する可能性のある`Can't find column ...`エラーを修正[＃50926](https://github.com/pingcap/tidb/issues/50926) @ [qw4990](https://github.com/qw4990)
    -   `CREATE TABLE`文に特定のパーティションまたは制約が含まれている場合に、テーブル名の変更などの DDL 操作が停止する問題を修正しました[＃50972](https://github.com/pingcap/tidb/issues/50972) @ [lcwangchao](https://github.com/lcwangchao)
    -   Grafana の監視メトリック`tidb_statistics_auto_analyze_total`整数[＃51051](https://github.com/pingcap/tidb/issues/51051) @ [ホーキングレイ](https://github.com/hawkingrei)として表示されない問題を修正しました
    -   `tidb_server_memory_limit`変数が[＃48180](https://github.com/pingcap/tidb/issues/48180) @ [ホーキングレイ](https://github.com/hawkingrei)に変更された後、 `tidb_gogc_tuner_threshold`システム変数がそれに応じて調整されない問題を修正しました
    -   クエリにJOIN操作[＃42588](https://github.com/pingcap/tidb/issues/42588) @ [アイリンキッド](https://github.com/AilinKid)が含まれる場合に`index out of range`エラーが発生する可能性がある問題を修正しました
    -   列のデフォルト値が削除されている場合、列のデフォルト値を取得するとエラーが返される問題を修正[＃50043](https://github.com/pingcap/tidb/issues/50043) [＃51324](https://github.com/pingcap/tidb/issues/51324) @ [crazycs520](https://github.com/crazycs520)
    -   TiFlash の遅延マテリアライゼーションが関連列[＃49241](https://github.com/pingcap/tidb/issues/49241) [＃51204](https://github.com/pingcap/tidb/issues/51204) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)を処理するときに間違った結果が返される可能性がある問題を修正しました
    -   バイナリ照合順序入力[＃50393](https://github.com/pingcap/tidb/issues/50393) @ [イービン87](https://github.com/yibin87)を処理するときに`LIKE()`関数が間違った結果を返す可能性がある問題を修正しました
    -   2番目のパラメータが`NULL` [＃50931](https://github.com/pingcap/tidb/issues/50931) @ [シーライズ](https://github.com/SeaRise)の場合に`JSON_LENGTH()`関数が間違った結果を返す問題を修正しました
    -   特定の状況下で時間精度が失われる可能[＃49555](https://github.com/pingcap/tidb/issues/49555) `CAST(AS DATETIME)` [シーライズ](https://github.com/SeaRise)
    -   テーブルにクラスター化インデックス[＃51372](https://github.com/pingcap/tidb/issues/51372) @ [グオシャオゲ](https://github.com/guo-shaoge)がある場合に並列`Apply`で誤った結果が生成される可能性がある問題を修正しました。
    -   主キーの型が`VARCHAR` [＃51810](https://github.com/pingcap/tidb/issues/51810) @ [そよ風のような](https://github.com/breezewish)の場合に`ALTER TABLE ... COMPACT TIFLASH REPLICA`誤って終了する可能性がある問題を修正しました
    -   `EXCHANGE PARTITION`ステートメント[＃47167](https://github.com/pingcap/tidb/issues/47167) @ [ジフハウス](https://github.com/jiyfhust)を使用してパーティション テーブルを交換するときに、 `DEFAULT NULL`属性の`NULL`値のチェックが正しく行われない問題を修正しました。
    -   パーティションテーブル定義がUTF8以外の文字セット[＃49251](https://github.com/pingcap/tidb/issues/49251) @ [ヤンケオ](https://github.com/YangKeao)を使用するときに誤った動作を引き起こす可能性がある問題を修正しました
    -   一部のシステム変数[＃49461](https://github.com/pingcap/tidb/issues/49461) @ [ジフハウス](https://github.com/jiyfhust)の`INFORMATION_SCHEMA.VARIABLES_INFO`テーブルに誤ったデフォルト値が表示される問題を修正しました
    -   一部のケースでデータベース名に空の文字列が使用された場合にエラーが報告されない問題を修正[＃45873](https://github.com/pingcap/tidb/issues/45873) @ [ヨシキポム](https://github.com/yoshikipom)
    -   `SPLIT TABLE ... INDEX`文で TiDB がpanicを起こす可能性がある問題を修正[＃50177](https://github.com/pingcap/tidb/issues/50177) @ [定義2014](https://github.com/Defined2014)
    -   `KeyPartition`タイプのパーティションテーブルをクエリするとエラーが発生する可能性がある問題を修正しました[＃50206](https://github.com/pingcap/tidb/issues/50206) [＃51313](https://github.com/pingcap/tidb/issues/51313) [＃51196](https://github.com/pingcap/tidb/issues/51196) @ [時間と運命](https://github.com/time-and-fate) @ [ジフハウス](https://github.com/jiyfhust) @ [ミョンス](https://github.com/mjonss)
    -   ハッシュパーティションテーブルをクエリすると誤った結果が生成される可能性がある問題を修正[＃50427](https://github.com/pingcap/tidb/issues/50427) @ [定義2014](https://github.com/Defined2014)
    -   OpenTracingが正しく動作しない問題を修正[＃50508](https://github.com/pingcap/tidb/issues/50508) @ [定義2014](https://github.com/Defined2014)
    -   `ALTER INSTANCE RELOAD TLS`エラー[＃50699](https://github.com/pingcap/tidb/issues/50699) @ [ドヴェーデン](https://github.com/dveeden)を報告したときにエラーメッセージが完全ではない問題を修正しました
    -   自動増分 ID [＃50819](https://github.com/pingcap/tidb/issues/50819) @ [天菜まお](https://github.com/tiancaiamao)を割り当てるときに、 `AUTO_INCREMENT`属性によって不要なトランザクション競合が発生し、ID が連続しなくなる問題を修正しました。
    -   一部のエラー[＃50849](https://github.com/pingcap/tidb/issues/50849) @ [天菜まお](https://github.com/tiancaiamao)について、TiDB ログ内の不完全なスタック情報の問題を修正しました
    -   `LIMIT`句の数値が大きすぎる場合に一部のクエリで過剰なメモリ使用が発生する問題を修正しました[＃51188](https://github.com/pingcap/tidb/issues/51188) @ [定義2014](https://github.com/Defined2014)
    -   TTL 機能により、データ範囲の分割が不正確になり、場合によっては[＃51527](https://github.com/pingcap/tidb/issues/51527) @ [lcwangchao](https://github.com/lcwangchao)でデータ ホットスポットが発生する問題を修正しました。
    -   明示的なトランザクション[＃51387](https://github.com/pingcap/tidb/issues/51387) @ [ヤンケオ](https://github.com/YangKeao)の最初の行に`SET`文が表示されても有効にならない問題を修正しました
    -   `BINARY`タイプの JSON をクエリすると、場合によってはエラーが発生する可能性がある問題を修正しました[＃51547](https://github.com/pingcap/tidb/issues/51547) @ [ヤンケオ](https://github.com/YangKeao)
    -   有効期限[＃51675](https://github.com/pingcap/tidb/issues/51675) @ [lcwangchao](https://github.com/lcwangchao)を計算するときに、TTL が夏時間調整の移行を正しく処理しない問題を修正しました。
    -   特定の条件下で`SURVIVAL_PREFERENCES`属性が`SHOW CREATE PLACEMENT POLICY`ステートメントの出力に表示されない可能性がある問題を修正[＃51699](https://github.com/pingcap/tidb/issues/51699) @ [lcwangchao](https://github.com/lcwangchao)
    -   無効な設定項目[＃51399](https://github.com/pingcap/tidb/issues/51399) @ [定義2014](https://github.com/Defined2014)が含まれている場合、設定ファイルが有効にならない問題を修正しました

-   TiKV

    -   `tidb_enable_row_level_checksum`有効にするとTiKVがpanicを起こす可能性がある問題を修正[＃16371](https://github.com/tikv/tikv/issues/16371) @ [cfzjywxk](https://github.com/cfzjywxk)
    -   例外的な状況で休止状態の領域がすぐに復帰しない問題を修正[＃16368](https://github.com/tikv/tikv/issues/16368) @ [LykxSassinator](https://github.com/LykxSassinator)
    -   ノードをオフラインにする前に、リージョン内のすべてのレプリカの最後のハートビート時間をチェックすることで、1 つのレプリカがオフラインになるとリージョン全体が使用できなくなる問題を修正しました[＃16465](https://github.com/tikv/tikv/issues/16465) @ [トニー・シュッキ](https://github.com/tonyxuqqi)
    -   JSON 整数の最大値`INT64`より大きく最大値`UINT64`より小さい値が TiKV によって`FLOAT64`として解析され、TiDB [＃16512](https://github.com/tikv/tikv/issues/16512) @ [ヤンケオ](https://github.com/YangKeao)との不整合が発生する問題を修正しました。
    -   監視メトリック`tikv_unified_read_pool_thread_count`にデータがない場合がある問題を修正[＃16629](https://github.com/tikv/tikv/issues/16629) @ [ユジュンセン](https://github.com/YuJuncen)

-   PD

    -   `MergeLabels`関数が[＃7535](https://github.com/tikv/pd/issues/7535) @ [lhy1024](https://github.com/lhy1024)で呼び出されたときにデータ競合が発生する問題を修正しました
    -   `evict-leader-scheduler`インターフェースが[＃7672](https://github.com/tikv/pd/issues/7672) @ [キャビンフィーバーB](https://github.com/CabinfeverB)で呼び出されたときに出力がない問題を修正しました
    -   リーダースイッチ[＃7728](https://github.com/tikv/pd/issues/7728) @ [キャビンフィーバーB](https://github.com/CabinfeverB)後にPD監視項目`learner-peer-count`古い値を同期しない問題を修正
    -   `watch etcd`正しくオフになっていない場合に発生するメモリリークの問題を修正[＃7807](https://github.com/tikv/pd/issues/7807) @ [rleungx](https://github.com/rleungx)
    -   一部のTSOログにエラー原因[＃7496](https://github.com/tikv/pd/issues/7496) @ [キャビンフィーバーB](https://github.com/CabinfeverB)が出力されない問題を修正
    -   再起動[＃4489](https://github.com/tikv/pd/issues/4489) @ [lhy1024](https://github.com/lhy1024)後に予期しないネガティブな監視メトリックが発生する問題を修正
    -   Leaderリースの有効期限がログ時間[＃7700](https://github.com/tikv/pd/issues/7700) @ [キャビンフィーバーB](https://github.com/CabinfeverB)より遅くなる問題を修正しました
    -   TiDB（PDクライアント）とPD間のTLSスイッチが不一致の場合にTiDBがパニックになる問題を修正[＃7900](https://github.com/tikv/pd/issues/7900) [＃7902](https://github.com/tikv/pd/issues/7902) [＃7916](https://github.com/tikv/pd/issues/7916) @ [キャビンフィーバーB](https://github.com/CabinfeverB)
    -   Goroutine が適切に閉じられていないときにリークする問題を修正[＃7782](https://github.com/tikv/pd/issues/7782) @ [HuSharp](https://github.com/HuSharp)
    -   pd-ctlが特殊文字[＃7798](https://github.com/tikv/pd/issues/7798) @ [Jmポテト](https://github.com/JmPotato)を含むスケジューラを削除できない問題を修正
    -   TSO [＃7864](https://github.com/tikv/pd/issues/7864) @ [キャビンフィーバーB](https://github.com/CabinfeverB)を取得する際に PD クライアントがブロックされる可能性がある問題を修正しました

-   TiFlash

    -   レプリカ移行[＃8323](https://github.com/pingcap/tiflash/issues/8323) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)中に PD とのネットワーク接続が不安定になり、 TiFlash がpanic可能性がある問題を修正しました
    -   クエリ[＃8564](https://github.com/pingcap/tiflash/issues/8564) @ [ジンヘリン](https://github.com/JinheLin)の低速化によりメモリ使用量が大幅に増加する問題を修正
    -   TiFlashレプリカを削除して再度追加すると、 TiFlash [＃8695](https://github.com/pingcap/tiflash/issues/8695) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)でデータ破損が発生する可能性がある問題を修正しました。
    -   ポイントインタイムリカバリ（PITR）を実行した後、または`FLASHBACK CLUSTER TO`実行した後にTiFlashレプリカデータが誤って削除され、データ異常[＃8777](https://github.com/pingcap/tiflash/issues/8777) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)が発生する可能性がある問題を修正しました。
    -   `ALTER TABLE ... MODIFY COLUMN ... NOT NULL`実行した後にTiFlash がパニックを起こし、NULL 可能列が[＃8419](https://github.com/pingcap/tiflash/issues/8419) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)に非 NULL に変更される問題を修正しました。
    -   分散storageおよびコンピューティングアーキテクチャで、ネットワーク分離[＃8806](https://github.com/pingcap/tiflash/issues/8806) @ [ジンヘリン](https://github.com/JinheLin)後にクエリが永続的にブロックされる可能性がある問題を修正しました
    -   分散storageとコンピューティングアーキテクチャで、シャットダウン[＃8837](https://github.com/pingcap/tiflash/issues/8837) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)中にTiFlash がpanicになる可能性がある問題を修正しました。
    -   リモート読み取り[＃8685](https://github.com/pingcap/tiflash/issues/8685) @ [ソロツグ](https://github.com/solotzg)の場合にデータ競合によりTiFlash がクラッシュする可能性がある問題を修正しました
    -   `CAST(AS JSON)`関数が JSON オブジェクトキー[＃8712](https://github.com/pingcap/tiflash/issues/8712) @ [シーライズ](https://github.com/SeaRise)の重複を排除しない問題を修正しました
    -   チャンクエンコード[＃8674](https://github.com/pingcap/tiflash/issues/8674) @ [イービン87](https://github.com/yibin87)中に`ENUM`列目がTiFlashを引き起こす可能性がある問題を修正しました

-   ツール

    -   バックアップと復元 (BR)

        -   リージョンがリーダー[＃16469](https://github.com/tikv/tikv/issues/16469) @ [ユジュンセン](https://github.com/YuJuncen)になった直後に分割またはマージされると、ログ バックアップ チェックポイントがスタックする問題を修正しました。
        -   フルバックアップでピアが見つからない場合に TiKV がパニックを起こす問題を修正[＃16394](https://github.com/tikv/tikv/issues/16394) @ [リーヴルス](https://github.com/Leavrth)
        -   同じノード[＃50445](https://github.com/pingcap/tidb/issues/50445) @ [3ポイントシュート](https://github.com/3pointer)で TiKV IP アドレスを変更した後にログ バックアップが停止する問題を修正しました
        -   S3 [＃49942](https://github.com/pingcap/tidb/issues/49942) @ [リーヴルス](https://github.com/Leavrth)からファイル コンテンツを読み取っているときにエラーが発生した場合にBR が再試行できない問題を修正しました
        -   データの復元に失敗した後、チェックポイントから再開するとエラー`the target cluster is not fresh`が発生する問題を修正しました[＃50232](https://github.com/pingcap/tidb/issues/50232) @ [リーヴルス](https://github.com/Leavrth)
        -   ログバックアップタスクを停止すると TiDB がクラッシュする問題を修正[＃50839](https://github.com/pingcap/tidb/issues/50839) @ [ユジュンセン](https://github.com/YuJuncen)
        -   TiKVノード[＃50566](https://github.com/pingcap/tidb/issues/50566) @ [リーヴルス](https://github.com/Leavrth)にリーダーがいないためにデータ復元が遅くなる問題を修正
        -   `--filter`オプションを指定した後でも、完全な復元を行うにはターゲット クラスターが空である必要があるという問題を修正しました[＃51009](https://github.com/pingcap/tidb/issues/51009) @ [3ポイントシュート](https://github.com/3pointer)

    -   TiCDC

        -   storageシンク[＃10352](https://github.com/pingcap/tiflow/issues/10352) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)使用時に、storageサービスによって生成されたファイルシーケンス番号が正しく増加しない可能性がある問題を修正しました。
        -   複数のチェンジフィード[＃10430](https://github.com/pingcap/tiflow/issues/10430) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)を同時に作成すると TiCDC が`ErrChangeFeedAlreadyExists`エラーを返す問題を修正しました
        -   `ignore-event`で`add table partition`イベントをフィルタリングするように構成した後、TiCDC が関連パーティションの他のタイプの DML 変更をダウンストリーム[＃10524](https://github.com/pingcap/tiflow/issues/10524) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)に複製しない問題を修正しました。
        -   アップストリームテーブル[＃10522](https://github.com/pingcap/tiflow/issues/10522) @ [スドジ](https://github.com/sdojjy)で`TRUNCATE PARTITION`が実行された後にチェンジフィードがエラーを報告する問題を修正しました
        -   変更フィードを再開するときに`snapshot lost caused by GC`時間内に報告されず、変更フィードの`checkpoint-ts` TiDB [＃10463](https://github.com/pingcap/tiflow/issues/10463) @ [スドジ](https://github.com/sdojjy)の GC セーフポイントよりも小さい問題を修正しました。
        -   単一行データのデータ整合性検証が有効にされた後、タイムゾーンの不一致により TiCDC が`TIMESTAMP`種類のチェックサムの検証に失敗する問題を修正[＃10573](https://github.com/pingcap/tiflow/issues/10573) @ [3エースショーハンド](https://github.com/3AceShowHand)
        -   同期ポイントテーブルが誤って複製される可能性がある問題を修正[＃10576](https://github.com/pingcap/tiflow/issues/10576) @ [アズドンメン](https://github.com/asddongmen)
        -   Apache Pulsarをダウンストリーム[＃10602](https://github.com/pingcap/tiflow/issues/10602) @ [アズドンメン](https://github.com/asddongmen)として使用するとOAuth2.0、TLS、mTLSが正しく有効化できない問題を修正
        -   TiKV がリーダー[＃10584](https://github.com/pingcap/tiflow/issues/10584) @ [アズドンメン](https://github.com/asddongmen)をアップグレード、再起動、または排除したときに、変更フィードがスタックする可能性がある問題を修正しました。
        -   DDL文が頻繁に実行されるシナリオで、間違ったBarrierTSが原因でデータが間違ったCSVファイルに書き込まれる問題を修正[＃10668](https://github.com/pingcap/tiflow/issues/10668) @ [リデジュ](https://github.com/lidezhu)
        -   KVクライアントのデータ競合によりTiCDCがpanic[＃10718](https://github.com/pingcap/tiflow/issues/10718) @ [アズドンメン](https://github.com/asddongmen)になる問題を修正
        -   テーブルレプリケーションタスク[＃10613](https://github.com/pingcap/tiflow/issues/10613) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)をスケジュールするときに TiCDC がパニックになる問題を修正しました

    -   TiDB データ移行 (DM)

        -   アップストリーム主キーがバイナリタイプ[＃10672](https://github.com/pingcap/tiflow/issues/10672) @ [GMHDBJD](https://github.com/GMHDBJD)の場合にデータが失われる問題を修正しました

    -   TiDB Lightning

        -   TiKVスペース[＃43636](https://github.com/pingcap/tidb/issues/43636) @ [ランス6716](https://github.com/lance6716)チェックによって発生するパフォーマンス低下の問題を修正
        -   ファイルスキャン中に無効なシンボリックリンクファイルに遭遇すると、 TiDB Lightning がエラーを報告する問題を修正しました[＃49423](https://github.com/pingcap/tidb/issues/49423) @ [ランス6716](https://github.com/lance6716)
        -   `sql_mode` [＃50757](https://github.com/pingcap/tidb/issues/50757) @ [GMHDBJD](https://github.com/GMHDBJD)に`NO_ZERO_IN_DATE`含まれていない場合に、 TiDB Lightning が`0`を含む日付値を正しく解析できない問題を修正しました。

## 寄稿者 {#contributors}

TiDB コミュニティからの以下の貢献者に感謝いたします。

-   [アオアン](https://github.com/Aoang)
-   [バッファフライ](https://github.com/bufferflies)
-   [デーモン365](https://github.com/daemon365)
-   [エルトシア](https://github.com/eltociear)
-   [リチュンジュ](https://github.com/lichunzhu)
-   [ジフハウス](https://github.com/jiyfhust)
-   [ピンアンドビー](https://github.com/pingandb)
-   [シェンキデバオジ](https://github.com/shenqidebaozi)
-   [スミティズ](https://github.com/Smityz)
-   [ソンジビン97](https://github.com/songzhibin97)
-   [タンジンユ97](https://github.com/tangjingyu97)
-   [テーマ](https://github.com/Tema)
-   [ub-3](https://github.com/ub-3)
-   [ヨシキポム](https://github.com/yoshikipom)
