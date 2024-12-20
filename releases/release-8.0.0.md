---
title: TiDB 8.0.0 Release Notes
summary: TiDB 8.0.0 の新機能、互換性の変更、改善、バグ修正について説明します。
---

# TiDB 8.0.0 リリースノート {#tidb-8-0-0-release-notes}

発売日: 2024年3月29日

TiDB バージョン: 8.0.0

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v8.0/quick-start-with-tidb)

8.0.0 では、次の主要な機能と改善が導入されています。

<table><thead><tr><th>カテゴリ</th><th>機能/拡張機能</th><th>説明</th></tr></thead><tbody><tr><td rowspan="4">スケーラビリティとパフォーマンス</td><td><a href="https://docs.pingcap.com/tidb/v8.0/pd-microservices">スケーラビリティを向上させるための PD の分解 (実験的)</a></td><td>配置Driver(PD) には、TiDB クラスターの正常な動作を確保するための重要なモジュールが複数含まれています。クラスターのワークロードが増加すると、PD 内の各モジュールのリソース消費も増加し、これらのモジュール間の相互干渉を引き起こし、最終的にはクラスターの全体的なサービス品質に影響を及ぼします。v8.0.0 以降、TiDB は PD 内の TSO モジュールとスケジュール モジュールを個別にデプロイ可能なマイクロサービスに分割することで、この問題に対処しています。これにより、クラスターの規模が拡大しても、モジュール間の相互干渉を大幅に削減できます。このアーキテクチャにより、はるかに大きなワークロードを持つ、はるかに大規模なクラスターが可能になりました。</td></tr><tr><td><a href="https://docs.pingcap.com/tidb/v8.0/system-variables#tidb_dml_type-new-in-v800">より大規模なトランザクションのためのバルク DML (実験的)</a></td><td>大規模なクリーンアップ ジョブ、結合、集計などの大規模なバッチ DML ジョブは、大量のメモリを消費する可能性があり、これまでは非常に大規模な規模で制限されていました。バルク DML ( <code>tidb_dml_type = &quot;bulk&quot;</code> ) は、トランザクション保証を提供し、OOM の問題を軽減しながら、大規模なバッチ DML タスクをより効率的に処理するための新しい DML タイプです。この機能は、データのロードに使用する場合、インポート、ロード、および復元操作とは異なります。</td></tr><tr><td><a href="https://docs.pingcap.com/tidb/v8.0/br-snapshot-guide#restore-cluster-snapshots">クラスター スナップショットの復元速度の高速化 (GA)</a></td><td>この機能により、 BR はクラスターのスケールの利点を最大限に活用し、クラスター内のすべての TiKV ノードがデータ復元の準備ステップに参加できるようになります。この機能により、大規模クラスター内の大規模データセットの復元速度が大幅に向上します。実際のテストでは、この機能によりダウンロード帯域幅が飽和し、ダウンロード速度が 8 ～ 10 倍、エンドツーエンドの復元速度が約 1.5 ～ 3 倍向上することが示されています。</td></tr><tr><td>テーブル数が膨大である場合のスキーマ情報のキャッシュの安定性を向上 (実験的)</td><td>マルチテナント アプリケーションの記録システムとして TiDB を使用している SaaS 企業は、多くの場合、相当数のテーブルを保存する必要があります。以前のバージョンでは、100 万以上のテーブル数を処理することは可能でしたが、全体的なユーザー エクスペリエンスが低下する可能性がありました。TiDB v8.0.0 では、 <code>auto analyze</code>用の<a href="https://docs.pingcap.com/tidb/v8.0/system-variables#tidb_enable_auto_analyze_priority_queue-new-in-v800">優先キューを</a>実装することで状況が改善され、プロセスの柔軟性が高まり、より広範なテーブルにわたって安定性が向上しています。</td></tr><tr><td rowspan="1"> DB 操作と可観測性</td><td>インデックス使用統計の監視をサポート</td><td>適切なインデックス設計は、データベースのパフォーマンスを維持するための重要な前提条件です。TiDB v8.0.0 では、インデックスの使用統計を提供する<a href="https://docs.pingcap.com/tidb/v8.0/information-schema-tidb-index-usage"><code>INFORMATION_SCHEMA.TIDB_INDEX_USAGE</code></a>テーブルと<a href="https://docs.pingcap.com/tidb/v8.0/sys-schema-unused-indexes"><code>sys.schema_unused_indexes</code></a>ビューが導入されています。この機能は、データベース内のインデックスの効率を評価し、インデックス設計を最適化するのに役立ちます。</td></tr><tr><td rowspan="2">データ移行</td><td>TiCDC が<a href="https://docs.pingcap.com/tidb/v8.0/ticdc-simple-protocol">シンプルプロトコル</a>のサポートを追加</td><td>TiCDC では、新しいプロトコルである Simple プロトコルが導入されています。このプロトコルは、DDL および BOOTSTRAP イベントにテーブル スキーマ情報を埋め込むことで、インバンド スキーマ追跡機能を提供します。</td></tr><tr><td> TiCDC が<a href="https://docs.pingcap.com/tidb/v8.0/ticdc-debezium">Debezium 形式プロトコル</a>のサポートを追加</td><td>TiCDC は、新しいプロトコルである Debezium プロトコルを導入しました。TiCDC は、Debezium スタイルのメッセージを生成するプロトコルを使用して、データ変更イベントを Kafka シンクに公開できるようになりました。</td></tr></tbody></table>

## 機能の詳細 {#feature-details}

### スケーラビリティ {#scalability}

-   PD はマイクロサービス モード (実験的) [＃5766](https://github.com/tikv/pd/issues/5766) @ [ビンシビン](https://github.com/binshi-bing)をサポートします

    v8.0.0 以降、PD はマイクロサービス モードをサポートします。このモードでは、PD のタイムスタンプ割り当て機能とクラスター スケジューリング関数が、独立してデプロイできる個別のマイクロサービスに分割されるため、PD のパフォーマンス スケーラビリティが向上し、大規模クラスターにおける PD のパフォーマンス ボトルネックが解消されます。

    -   `tso`マイクロサービス: クラスター全体に対して単調に増加するタイムスタンプ割り当てを提供します。
    -   `scheduling`マイクロサービス: 負荷分散、ホットスポット処理、レプリカ修復、レプリカ配置など、クラスター全体のスケジュール関数を提供します。

    各マイクロサービスは独立したプロセスとしてデプロイされます。マイクロサービスに複数のレプリカを構成すると、マイクロサービスはプライマリ/セカンダリ フォールト トレラント モードを自動的に実装し、サービスの高可用性と信頼性を確保します。

    現在、PD マイクロサービスはTiDB Operator を使用してのみデプロイできます。PD がスケールアップでは解決できない重大なパフォーマンスボトルネックになる場合は、このモードを検討することをお勧めします。

    詳細については[ドキュメント](/pd-microservices.md)参照してください。

<!---->

-   Titanエンジン[＃16245](https://github.com/tikv/tikv/issues/16245) @ [コナー1996](https://github.com/Connor1996)の使いやすさを向上

    -   Titan BLOB ファイルと RocksDB ブロック ファイルの共有キャッシュをデフォルトで有効にします ( [`shared-blob-cache`](/tikv-configuration-file.md#shared-blob-cache-new-in-v800)デフォルトは`true`です)。これにより、 [`blob-cache-size`](/tikv-configuration-file.md#blob-cache-size)個別に構成する必要がなくなります。
    -   Titan エンジンを使用するときにパフォーマンスと柔軟性を向上させるために、 [`min-blob-size`](/tikv-configuration-file.md#min-blob-size) 、 [`blob-file-compression`](/tikv-configuration-file.md#blob-file-compression) 、および[`discardable-ratio`](/tikv-configuration-file.md#min-blob-size)動的に変更することをサポートします。

    詳細については[ドキュメント](/storage-engine/titan-configuration.md)参照してください。

### パフォーマンス {#performance}

-   BR はスナップショットの復元速度を向上します (GA) [＃50701](https://github.com/pingcap/tidb/issues/50701) @ [3ポインター](https://github.com/3pointer) @ [リーヴルス](https://github.com/Leavrth)

    TiDB v8.0.0 以降、スナップショット復元速度の高速化が一般提供 (GA) され、デフォルトで有効になっています。BRは、粗粒度のリージョン分散アルゴリズムの採用、データベースとテーブルのバッチ作成、SST ファイルのダウンロードと取り込み操作の相互影響の軽減、テーブル統計の復元の高速化など、さまざまな最適化を実装することで、スナップリージョン復元速度を大幅に向上させます。実際のケースのテスト結果によると、単一の TiKV ノードのデータ復元速度は 1.2 GiB/s で安定し、1 時間以内に 100 TiB のデータを復元できます。

    これは、高負荷環境でもBR が各 TiKV ノードのリソースを最大限に活用できるため、データベースの復元時間が大幅に短縮され、データベースの可用性と信頼性が向上し、データ損失やシステム障害によるダウンタイムとビジネス損失が削減されることを意味します。復元速度の向上は、多数の goroutine の並列実行に起因しており、特にテーブルやリージョンが多い場合は、メモリ消費量が大幅に増加する可能性があることに注意してください。BR クライアントを実行するには、メモリ容量が大きいマシンを使用することをお勧めします。マシンのメモリ容量が限られている場合は、より細粒度のリージョン分散アルゴリズムを使用するBRをお勧めします。また、粗粒度のリージョン分散アルゴリズムは外部storage帯域幅を大量に消費する可能性があるため、外部帯域幅が不足して他のアプリケーションに影響が出ないようにする必要があります。

    詳細については[ドキュメント](/br/br-snapshot-guide.md#restore-cluster-snapshots)参照してください。

-   以下の関数をTiFlash [＃50975](https://github.com/pingcap/tidb/issues/50975) [＃50485](https://github.com/pingcap/tidb/issues/50485) @ [宜ビン87](https://github.com/yibin87) @ [風の話し手](https://github.com/windtalker)にプッシュダウンすることをサポートします

    -   `CAST(DECIMAL AS DOUBLE)`
    -   `POWER()`

    詳細については[ドキュメント](/tiflash/tiflash-supported-pushdown-calculations.md)参照してください。

-   TiDBの並列HashAggアルゴリズムはディスクスピル（実験的） [＃35637](https://github.com/pingcap/tidb/issues/35637) @ [翻訳者](https://github.com/xzhangxian1008)をサポートします

    以前のバージョンの TiDB では、HashAgg 演算子の同時実行アルゴリズムはメモリ内でのみ処理できます。その結果、TiDB は大量のデータをメモリ内で処理する必要があります。データ サイズがメモリ制限を超えると、TiDB は非並列アルゴリズムのみを選択でき、同時実行によるパフォーマンス向上は実現されません。

    v8.0.0 では、TiDB の並列 HashAgg アルゴリズムがディスク スピルをサポートしています。どのような並列条件でも、HashAgg 演算子はメモリ使用量に基づいてデータ スピルを自動的にトリガーできるため、パフォーマンスとデータ スループットのバランスをとることができます。現在、実験的機能として、TiDB はディスク スピルをサポートする並列 HashAgg アルゴリズムを有効にするかどうかを制御する`tidb_enable_parallel_hashagg_spill`変数を導入しています。この変数が`ON`場合、有効であることを意味します。この変数は、将来のリリースで機能が一般提供された後には非推奨になります。

    詳細については[ドキュメント](/system-variables.md#tidb_enable_parallel_hashagg_spill-new-in-v800)参照してください。

-   自動統計収集のための優先キューを導入する[＃50132](https://github.com/pingcap/tidb/issues/50132) @ [ハイラスティン](https://github.com/Rustin170506)

    オプティマイザ統計を最新の状態に維持することが、データベース パフォーマンスを安定させる鍵です。ほとんどのユーザーは、最新の統計を収集するために TiDB が提供する[自動統計収集](/statistics.md#automatic-update)に依存しています。自動統計収集では、すべてのオブジェクトの統計の状態を確認し、異常なオブジェクトをキューに追加して順次収集します。以前のバージョンでは、順序はランダムであったため、より価値のある候補が更新されるまでの待機時間が長くなり、パフォーマンスが低下する可能性がありました。

    v8.0.0 以降、自動統計収集では、さまざまな条件と組み合わせてオブジェクトの優先順位を動的に設定し、新しく作成されたインデックスや定義が変更されたパーティション テーブルなど、より適切な候補が優先的に処理されるようにします。さらに、TiDB はヘルス スコアが低いテーブルを優先し、キューの先頭に配置します。この機能強化により、収集の順序がより合理的になり、古い統計によって発生するパフォーマンスの問題が軽減されるため、データベースの安定性が向上します。

    詳細については[ドキュメント](/system-variables.md#tidb_enable_auto_analyze_priority_queue-new-in-v800)参照してください。

-   実行プランキャッシュの制限をいくつか削除[＃49161](https://github.com/pingcap/tidb/pull/49161) @ [ミョンス](https://github.com/mjonss) @ [qw4990](https://github.com/qw4990)

    TiDB は[プランキャッシュ](/sql-prepared-plan-cache.md)サポートしており、これは OLTP システムのレイテンシーを効果的に削減でき、パフォーマンスにとって重要です。v8.0.0 では、TiDB はプラン キャッシュに関するいくつかの制限を取り除きました。次の項目を含む実行プランをキャッシュできるようになりました。

    -   [パーティションテーブル](/partitioned-table.md)
    -   [生成された列](/generated-columns.md) 、生成された列に依存するオブジェクト（ [多値インデックス](/choose-index.md#multi-valued-indexes-and-plan-cache)など）を含む

    この機能強化により、プラン キャッシュの使用例が拡張され、複雑なシナリオにおけるデータベース全体のパフォーマンスが向上します。

    詳細については[ドキュメント](/sql-prepared-plan-cache.md)参照してください。

-   オプティマイザは複数値インデックスのサポートを強化します[＃47759](https://github.com/pingcap/tidb/issues/47759) [＃46539](https://github.com/pingcap/tidb/issues/46539) @ [アレナトルクス](https://github.com/Arenatlx) @ [時間と運命](https://github.com/time-and-fate)

    TiDB v6.6.0 では、JSON データ型のクエリ パフォーマンスを向上させるために[複数値インデックス](/sql-statements/sql-statement-create-index.md#multi-valued-indexes)導入されています。v8.0.0 では、オプティマイザーは複数値インデックスのサポートを強化し、複雑なシナリオでクエリを最適化するためにそれらを正しく識別して利用できるようになりました。

    -   オプティマイザは、多値インデックスの統計情報を収集し、その統計を使用して実行プランを決定します。SQL ステートメントで複数の多値インデックスを選択できる場合、オプティマイザはコストの低いインデックスを識別できます。
    -   `OR`使用して複数の`member of`条件を接続する場合、オプティマイザーは各 DNF 項目 ( `member of`条件) の有効なインデックス部分パスを一致させ、Union を使用してこれらのパスを結合して`Index Merge`形成できます。これにより、より効率的な条件フィルタリングとデータ フェッチが実現します。

    詳細については[ドキュメント](/sql-statements/sql-statement-create-index.md#multi-valued-indexes)参照してください。

-   低精度TSO [＃51081](https://github.com/pingcap/tidb/issues/51081) @ [テーマ](https://github.com/Tema)の更新間隔の設定をサポート

    TiDB の[低精度TSO機能](/system-variables.md#tidb_low_resolution_tso)では、定期的に更新される TSO がトランザクション タイムスタンプとして使用されます。古いデータの読み取りが許容されるシナリオでは、この機能により、リアルタイム パフォーマンスを犠牲にして小さな読み取り専用トランザクションの TSO 取得のオーバーヘッドが削減され、高同時読み取りの能力が向上します。

    v8.0.0 より前では、低精度 TSO 機能の TSO 更新間隔は固定されており、実際のアプリケーション要件に応じて調整することはできません。v8.0.0 では、TiDB は TSO 更新間隔を制御するシステム変数`tidb_low_resolution_tso_update_interval`導入しています。この機能は、低精度 TSO 機能が有効な場合にのみ有効になります。

    詳細については[ドキュメント](/system-variables.md#tidb_low_resolution_tso_update_interval-new-in-v800)参照してください。

### 可用性 {#availability}

-   プロキシコンポーネントTiProxyが一般提供（GA）される[＃413](https://github.com/pingcap/tiproxy/issues/413) @ [翻訳者](https://github.com/djshow832) @ [xhebox](https://github.com/xhebox)

    TiDB v7.6.0 では、実験的機能としてプロキシコンポーネントTiProxy が導入されています。TiProxy は、クライアントと TiDBサーバーの間にある TiDB の公式プロキシコンポーネントです。TiDB の負荷分散機能と接続永続化関数を提供し、TiDB クラスターのワークロードのバランスをよりとり、メンテナンス操作中にデータベースへのユーザー アクセスに影響を与えないようにします。

    v8.0.0 では、TiProxy が一般提供され、署名証明書の自動生成と監視関数が強化されています。

    TiProxy の使用シナリオは次のとおりです。

    -   TiDB クラスターのローリング再起動、ローリングアップグレード、スケールインなどのメンテナンス操作中は、TiDB サーバーに変更が発生し、クライアントと TiDB サーバー間の接続が中断されます。TiProxy を使用すると、これらのメンテナンス操作中に接続を他の TiDB サーバーにスムーズに移行できるため、クライアントに影響が及ぶことはありません。
    -   TiDBサーバーへのクライアント接続は、他の TiDB サーバーに動的に移行できません。複数の TiDB サーバーのワークロードが不均衡な場合、クラスター全体のリソースは十分であるものの、特定の TiDB サーバーでリソースが枯渇し、レイテンシーが大幅に増加する状況が発生する可能性があります。この問題に対処するために、TiProxy は接続の動的移行を提供します。これにより、クライアントに影響を与えることなく、接続を 1 つの TiDBサーバーから別の TiDB サーバーに移行できるため、TiDB クラスターの負荷分散が実現します。

    TiProxy はTiUP、 TiDB Operator、および TiDB Dashboard に統合されており、構成、展開、保守が容易になります。

    詳細については[ドキュメント](/tiproxy/tiproxy-overview.md)参照してください。

### 構文 {#sql}

-   大量のデータを処理するための新しい DML タイプをサポート (実験的) [＃50215](https://github.com/pingcap/tidb/issues/50215) @ [エキシウム](https://github.com/ekexium)

    v8.0.0 より前のバージョンでは、TiDB はコミットする前にすべてのトランザクション データをメモリに保存します。大量のデータを処理する場合、トランザクションに必要なメモリがボトルネックとなり、TiDB が処理できるトランザクション サイズが制限されます。TiDB は非トランザクション DML を導入し、SQL ステートメントを分割してトランザクション サイズの制限を解決しようとしていますが、この機能にはさまざまな制限があり、実際のシナリオでは理想的なエクスペリエンスを提供しません。

    TiDB は、v8.0.0 以降、大量のデータを処理するための DML タイプをサポートしています。この DML タイプは、実行中にタイムリーに TiKV にデータを書き込み、すべてのトランザクション データをメモリに継続的にstorageことを回避し、メモリ制限を超える大量のデータの処理をサポート`UPDATE`ます。この DML タイプは、トランザクションの整合性を確保し、標準 DML と同じ構文を使用します。1、3、5、および`REPLACE` `INSERT`ステートメントは`DELETE`この新しい DML タイプを使用して大規模な DML 操作を実行できます。

    この DML タイプは[パイプライン化された DML](https://github.com/pingcap/tidb/blob/release-8.0/docs/design/2024-01-09-pipelined-DML.md)機能によって実装され、自動コミットが有効になっているステートメントにのみ影響します。システム変数[`tidb_dml_type`](/system-variables.md#tidb_dml_type-new-in-v800)を設定することで、この DML タイプを有効にするかどうかを制御できます。

    詳細については[ドキュメント](/system-variables.md#tidb_dml_type-new-in-v800)参照してください。

-   テーブル作成時にデフォルトの列値を設定する式の使用をサポート (実験的) [＃50936](https://github.com/pingcap/tidb/issues/50936) @ [ジムララ](https://github.com/zimulala)

    v8.0.0 より前では、テーブルを作成するときに、列のデフォルト値は文字列、数値、日付に制限されていました。v8.0.0 以降では、いくつかの式をデフォルトの列値として使用できます。たとえば、列のデフォルト値を`UUID()`に設定できます。この機能により、より多様な要件を満たすことができます。

    詳細については[ドキュメント](/data-type-default-values.md#specify-expressions-as-default-values)参照してください。

-   `div_precision_increment`システム変数[＃51501](https://github.com/pingcap/tidb/issues/51501) @ [いびん87](https://github.com/yibin87)をサポート

    MySQL 8.0 は、 `/`演算子を使用して実行された除算演算の結果のスケールを増やす桁数を指定する変数`div_precision_increment`をサポートします。v8.0.0 より前の TiDB ではこの変数はサポートされておらず、除算は小数点以下 4 桁まで実行されます。v8.0.0 以降では、TiDB はこの変数をサポートします。除算演算の結果のスケールを増やす桁数を必要に応じて指定できます。

    詳細については[ドキュメント](/system-variables.md#div_precision_increment-new-in-v800)参照してください。

### DB操作 {#db-operations}

-   PITR は Amazon S3 オブジェクト ロック[＃51184](https://github.com/pingcap/tidb/issues/51184) @ [リドリス](https://github.com/RidRisR)をサポートします

    Amazon S3 オブジェクト ロックは、指定された保持期間中にバックアップ データが誤ってまたは意図的に削除されるのを防ぎ、データのセキュリティと整合性を強化します。v6.3.0 以降、 BR はスナップショット バックアップ用の Amazon S3 オブジェクト ロックをサポートし、フル バックアップのレイヤーをさらに強化します。v8.0.0 以降、PITR も Amazon S3 オブジェクト ロックをサポートします。フル バックアップでもログ データ バックアップでも、オブジェクト ロック機能により、より信頼性の高いデータ保護が保証され、データのバックアップとリカバリのセキュリティがさらに強化され、規制要件を満たすことができます。

    詳細については[ドキュメント](/br/backup-and-restore-storages.md#other-features-supported-by-the-storage-service)参照してください。

-   セッションレベル[＃50653](https://github.com/pingcap/tidb/issues/50653) @ [ホーキングレイ](https://github.com/hawkingrei)で非表示のインデックスを可視化する機能をサポート

    デフォルトでは、オプティマイザは[非表示のインデックス](/sql-statements/sql-statement-create-index.md#invisible-index)選択しません。このメカニズムは通常、インデックスを削除するかどうかを評価するために使用されます。インデックスを削除した場合のパフォーマンスへの影響が不明な場合は、インデックスを一時的に非表示に設定し、必要なときにすぐに表示に戻すオプションがあります。

    バージョン 8.0.0 以降では、セッション レベルのシステム変数[`tidb_opt_use_invisible_indexes`](/system-variables.md#tidb_opt_use_invisible_indexes-new-in-v800)から`ON`設定して、現在のセッションで非表示のインデックスを認識できるようになりました。この機能を使用すると、最初にインデックスを可視化し、次に現在のセッションでシステム変数を変更して他のセッションに影響を与えずにテストすることで、新しいインデックスを作成してそのパフォーマンスをテストできます。この改善により、SQL チューニングの安全性が高まり、本番データベースの安定性が向上します。

    詳細については[ドキュメント](/sql-statements/sql-statement-create-index.md#invisible-index)参照してください。

-   一般的なログを別のファイルに書き込むことをサポート[＃51248](https://github.com/pingcap/tidb/issues/51248) @ [定義2014](https://github.com/Defined2014)

    一般ログは、実行されたすべての SQL ステートメントをログに記録して問題の診断に役立てる、MySQL 互換の機能です。TiDB もこの機能をサポートしています。変数[`tidb_general_log`](/system-variables.md#tidb_general_log)設定することで有効にできます。ただし、以前のバージョンでは、一般ログの内容は他の情報とともに TiDB インスタンス ログにのみ書き込むことができたため、ログを長期間保存する必要があるユーザーにとっては不便でした。

    v8.0.0 以降では、構成項目[`log.general-log-file`](/tidb-configuration-file.md#general-log-file-new-in-v800)を有効なファイル名に設定することで、一般ログを指定されたファイルに書き込むことができます。一般ログは、インスタンス ログと同じローテーションおよび保持ポリシーに従います。

    さらに、履歴ログ ファイルが占有するディスク領域を削減するために、TiDB v8.0.0 ではネイティブ ログ圧縮オプションが導入されています。構成項目[`log.file.compression`](/tidb-configuration-file.md#compression-new-in-v800)から`gzip`設定すると、 [`gzip`](https://www.gzip.org/)形式を使用してローテーションされたログを自動的に圧縮できます。

    詳細については[ドキュメント](/tidb-configuration-file.md#general-log-file-new-in-v800)参照してください。

### 可観測性 {#observability}

-   インデックス使用統計の監視をサポート[＃49830](https://github.com/pingcap/tidb/issues/49830) @ [ヤンケオ](https://github.com/YangKeao)

    適切なインデックス設計は、データベースのパフォーマンスを維持するための重要な前提条件です。TiDB v8.0.0 では、現在の TiDB ノード上のすべてのインデックスの統計情報を記録する[`INFORMATION_SCHEMA.TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md)テーブルが導入され、次の情報が含まれます。

    -   インデックスをスキャンするステートメントの累積実行回数
    -   インデックスにアクセスする際にスキャンされる行の総数
    -   インデックスをスキャンする際の選択分布
    -   インデックスへの最終アクセス時刻

    この情報を使用すると、オプティマイザーによって使用されていないインデックスや選択性が低いインデックスを識別し、インデックス設計を最適化してデータベースのパフォーマンスを向上させることができます。

    さらに、TiDB v8.0.0 では、MySQL と互換性のあるビュー[`sys.schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md)が導入されています。このビューには、TiDB インスタンスの最後の起動以降に使用されていないインデックスが表示されます。v8.0.0 より前のバージョンからアップグレードされたクラスターの場合、 `sys`スキーマとビューは自動的に作成されません。 [`sys.schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md#manually-create-the-schema_unused_indexes-view)を参照して手動で作成できます。

    詳細については[ドキュメント](/information-schema/information-schema-tidb-index-usage.md)参照してください。

### Security {#security}

-   保存時の TiKV 暗号化は Google [キー管理サービス (Cloud KMS)](https://cloud.google.com/docs/security/key-management-deep-dive?hl) (実験的) [＃8906](https://github.com/tikv/tikv/issues/8906) @ [栄光](https://github.com/glorv)をサポートします

    TiKV は、保存データの暗号化技術を使用して保存データを暗号化することで、データのセキュリティを確保します。セキュリティのための保存データの暗号化の中核は、キー管理です。v8.0.0 以降では、Google Cloud KMS を使用して TiKV のマスターキーを管理し、Cloud KMS に基づく保存データの暗号化機能を確立して、ユーザーデータのセキュリティを強化できます。

    Google Cloud KMS に基づいて保存時の暗号化を有効にするには、Google Cloud でキーを作成し、TiKV 構成ファイルの`[security.encryption.master-key]`セクションを構成する必要があります。

    詳細については[ドキュメント](/encryption-at-rest.md#tikv-encryption-at-rest)参照してください。

-   TiDB ログ感度低下を[＃51306](https://github.com/pingcap/tidb/issues/51306) @ [xhebox](https://github.com/xhebox)強化

    TiDB ログの感度低下の強化は、ログ ファイル内の SQL テキスト情報をマークすることに基づいており、ユーザーがログを表示するときに機密データを安全に表示されるようになります。ログ情報を感度低下させるかどうかを制御して、さまざまなシナリオで TiDB ログを安全に使用できるようにし、ログ感度低下を使用する際のセキュリティと柔軟性を高めることができます。この機能を使用するには、システム変数`tidb_redact_log`を`MARKER`に設定します。これにより、TiDB ログ内の SQL テキストがマークされます。ログを表示すると、マーカーに基づいて機密データが安全に表示されるため、ログ情報が保護されます。

    詳細については[ドキュメント](/system-variables.md#tidb_redact_log)参照してください。

### データ移行 {#data-migration}

-   TiCDC はシンプルプロトコル[＃9898](https://github.com/pingcap/tiflow/issues/9898) @ [3エースショーハンド](https://github.com/3AceShowHand)のサポートを追加します

    TiCDC では、新しいプロトコルである Simple プロトコルが導入されています。このプロトコルは、DDL および BOOTSTRAP イベントにテーブル スキーマ情報を埋め込むことで、インバンド スキーマ追跡機能を提供します。

    詳細については[ドキュメント](/ticdc/ticdc-simple-protocol.md)参照してください。

-   TiCDC は Debezium フォーマットプロトコル[＃1799](https://github.com/pingcap/tiflow/issues/1799) @ [そよ風のような](https://github.com/breezewish)のサポートを追加します

    TiCDC は、Debezium スタイルの形式でイベント メッセージを生成するプロトコルを使用して、データ変更イベントを Kafka シンクに公開できるようになりました。これにより、現在 Debezium を使用して MySQL からデータをプルし、下流処理に使用しているユーザーにとって、MySQL から TiDB への移行が簡素化されます。

    詳細については[ドキュメント](/ticdc/ticdc-debezium.md)参照してください。

-   DM は、ソース データベースとターゲット データベースのパスワードを暗号化および復号化するために、ユーザーが提供する秘密キーの使用をサポートします[＃9492](https://github.com/pingcap/tiflow/issues/9492) @ [D3ハンター](https://github.com/D3Hunter)

    以前のバージョンでは、DM は比較的セキュリティの低い組み込みの固定秘密鍵を使用していました。v8.0.0 以降では、上流および下流のデータベースのパスワードを暗号化および復号化するための秘密鍵ファイルをアップロードして指定できます。また、必要に応じて秘密鍵ファイルを置き換えて、データ セキュリティを強化することもできます。

    詳細については[ドキュメント](/dm/dm-customized-secret-key.md)参照してください。

-   `IMPORT INTO`機能を強化するために`IMPORT INTO ... FROM SELECT`構文をサポートします (実験的) [＃49883](https://github.com/pingcap/tidb/issues/49883) @ [D3ハンター](https://github.com/D3Hunter)

    以前のバージョンの TiDB では、クエリ結果をターゲット テーブルにインポートするには`INSERT INTO ... SELECT`ステートメントしか使用できませんでしたが、これは大規模なデータセットのシナリオでは比較的非効率的でした。v8.0.0 以降では、 `IMPORT INTO ... FROM SELECT`使用して`SELECT`クエリの結果を空の TiDB ターゲット テーブルにインポートできるようになり、 `INSERT INTO ... SELECT`の最大 8 倍のパフォーマンスが実現され、インポート時間が大幅に短縮されます。

    さらに、 `IMPORT INTO ... FROM SELECT`使用して、 [`AS OF TIMESTAMP`](/as-of-timestamp.md)でクエリされた履歴データをインポートすることもできます。

    詳細については[ドキュメント](/sql-statements/sql-statement-import-into.md)参照してください。

-   TiDB Lightning は競合解決戦略を簡素化し、 `replace`戦略 (実験的) [＃51036](https://github.com/pingcap/tidb/issues/51036) @ [翻訳者](https://github.com/lyzx2001)を使用して競合するデータの処理をサポートします。

    以前のバージョンでは、 TiDB Lightning には論理インポート モードが[1つのデータ競合解決戦略](/tidb-lightning/tidb-lightning-logical-import-mode-usage.md#conflict-detection) 、物理インポート モードが[2つのデータ競合解決戦略](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#conflict-detection)あり、理解して構成するのは簡単ではありませんでした。

    v8.0.0 以降、 TiDB Lightning物理インポート モードの[競合検出の旧バージョン](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#the-old-version-of-conflict-detection-deprecated-in-v800)戦略が廃止され、 [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md)パラメータを介して論理インポート モードと物理インポート モードの両方の競合検出戦略を制御できるようになり、このパラメータの構成が簡素化されました。さらに、物理インポート モードでは、インポート時に主キーまたは一意キーの競合のあるデータが検出された場合に、 `replace`戦略で最新のデータを保持し、古いデータを上書きできるようになりました。

    詳細については[ドキュメント](/tidb-lightning/tidb-lightning-configuration.md)参照してください。

-   グローバルソートが一般提供（GA）され、 `IMPORT INTO`のパフォーマンスと安定性が大幅に向上しました[＃45719](https://github.com/pingcap/tidb/issues/45719) @ [ランス6716](https://github.com/lance6716)

    v7.4.0 より前では、 [分散実行フレームワーク (DXF)](/tidb-distributed-execution-framework.md)使用して`IMPORT INTO`タスクを実行する場合、ローカルstorageスペースが限られているため、TiDB は TiKV にインポートする前にデータの一部のみをローカルでソートします。その結果、TiKV にインポートされたデータが大幅に重複し、インポート中に TiKV で追加の圧縮操作を実行する必要があり、TiKV のパフォーマンスと安定性に影響します。

    v7.4.0 で導入された Global Sort の実験的機能により、TiDB はインポートするデータを TiKV にインポートする前に一時的に外部storage(Amazon S3 など) に保存してグローバルソートできるため、インポート中に TiKV の圧縮操作を行う必要がなくなります。v8.0.0 では、Global Sort が GA になります。この機能により、TiKV のリソース消費が削減され、 `IMPORT INTO`のパフォーマンスと安定性が大幅に向上します。Global Sort を有効にすると、各`IMPORT INTO`タスクで 40 TiB 以内のデータのインポートがサポートされます。

    詳細については[ドキュメント](/tidb-global-sort.md)参照してください。

## 互換性の変更 {#compatibility-changes}

> **注記：**
>
> このセクションでは、v7.6.0 から現在のバージョン (v8.0.0) にアップグレードするときに知っておく必要のある互換性の変更について説明します。v7.5.0 以前のバージョンから現在のバージョンにアップグレードする場合は、中間バージョンで導入された互換性の変更も確認する必要がある可能性があります。

-   TiUPによってデプロイされたデフォルトの Prometheus バージョンを 2.27.1 から 2.49.1 にアップグレードします。
-   TiUPによってデプロイされたデフォルトの Grafana バージョンを 7.5.11 から 7.5.17 にアップグレードします。
-   GA ではないがデフォルトで有効になっている監視関連のスケジューラを削除します[＃7765](https://github.com/tikv/pd/pull/7765) @ [rleungx](https://github.com/rleungx)

### 行動の変化 {#behavior-changes}

-   ユーザーの潜在的な接続問題を防ぐために、Security強化モード (SEM) で[`require_secure_transport`](/system-variables.md#require_secure_transport-new-in-v610)から`ON`設定を禁止します[＃47665](https://github.com/pingcap/tidb/issues/47665) @ [天菜まお](https://github.com/tiancaiamao)
-   DM では、暗号化と復号化の固定秘密鍵が削除され、暗号化と復号化の秘密鍵をカスタマイズできるようになります。アップグレード前に[データソース構成](/dm/dm-source-configuration-file.md)と[移行タスクの構成](/dm/task-configuration-file-full.md)で暗号化パスワードが[＃9492](https://github.com/pingcap/tiflow/issues/9492)されている場合は、追加の操作については[DM 暗号化と復号化のための秘密鍵をカスタマイズする](/dm/dm-customized-secret-key.md)のアップグレード手順を参照する必要があります。7 @ [D3ハンター](https://github.com/D3Hunter)
-   v8.0.0 より前では、 `ADD INDEX`と`CREATE INDEX` ( `tidb_ddl_enable_fast_reorg = ON` ) のアクセラレーションを有効にすると、エンコードされたインデックス キーは`16`の固定同時実行性で TiKV にデータを取り込みますが、これは下流の TiKV 容量に応じて動的に調整することはできません。v8.0.0 以降では、 [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt)システム変数を使用して同時実行性を調整できます。デフォルト値は`4`です。以前のデフォルト値`16`と比較すると、新しいデフォルト値では、インデックス付きキーと値のペアを取り込むときのパフォーマンスが低下します。このシステム変数は、クラスターのワークロードに基づいて調整できます。

### MySQL 互換性 {#mysql-compatibility}

-   `KEY`パーティション タイプは、パーティション フィールドの空のリストを持つステートメントをサポートします。これは、MySQL の動作と一致しています。

### システム変数 {#system-variables}

| 変数名                                                                                                                       | タイプを変更   | 説明                                                                                                                                                                                                                          |
| ------------------------------------------------------------------------------------------------------------------------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`tidb_disable_txn_auto_retry`](/system-variables.md#tidb_disable_txn_auto_retry)                                         | 非推奨      | v8.0.0 以降、このシステム変数は非推奨となり、TiDB は楽観的トランザクションの自動再試行をサポートしなくなりました。 [悲観的なトランザクションモード](/pessimistic-transaction.md)を使用することをお勧めします。楽観的ミスティック トランザクションの競合が発生した場合は、エラーをキャプチャしてアプリケーションでトランザクションを再試行できます。                            |
| `tidb_ddl_version`                                                                                                        | 名前を変更    | TiDB DDL V2 を有効にするかどうかを制御します。v8.0.0 以降では、この変数の名前は、その目的をより適切に反映するために[`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-new-in-v800)に変更されています。                                              |
| [`tidb_enable_collect_execution_info`](/system-variables.md#tidb_enable_collect_execution_info)                           | 修正済み     | [インデックスの使用統計](/information-schema/information-schema-tidb-index-usage.md)を記録するかどうかのコントロールを追加します。デフォルト値は`ON`です。                                                                                                              |
| [`tidb_redact_log`](/system-variables.md#tidb_redact_log)                                                                 | 修正済み     | TiDB ログとスロー ログを記録するときに、SAL テキスト内のユーザー情報を処理する方法を制御します。値のオプションは、 `OFF` (ログ内のユーザー情報を処理しないことを示す) と`ON` (ログ内のユーザー情報を非表示にすることを示す) です。ログ内のユーザー情報をより豊富に処理する方法を提供するために、v8.0.0 では、ログ情報のマーク付けをサポートする`MARKER`オプションが追加されました。             |
| [`div_precision_increment`](/system-variables.md#div_precision_increment-new-in-v800)                                     | 新しく追加された | `/`演算子を使用して実行された除算演算の結果のスケールを増やす桁数を制御します。この変数は MySQL と同じです。                                                                                                                                                                 |
| [`tidb_dml_type`](/system-variables.md#tidb_dml_type-new-in-v800)                                                         | 新しく追加された | DML ステートメントの実行モードを制御します。値のオプションは`"standard"`と`"bulk"`です。                                                                                                                                                                    |
| [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-new-in-v800)     | 新しく追加された | 優先キューを有効にして、統計を自動的に収集するタスクをスケジュールするかどうかを制御します。この変数を有効にすると、TiDB は統計を最も必要とするテーブルの統計収集を優先します。                                                                                                                                  |
| [`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-new-in-v800)               | 新しく追加された | TiDB が並列 HashAgg アルゴリズムのディスク スピルをサポートするかどうかを制御します。 `ON`の場合、並列 HashAgg アルゴリズムのディスク スピルをトリガーできます。 この変数は、この機能が将来のリリースで一般に利用可能になったときに非推奨になります。                                                                                  |
| [`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-new-in-v800)                         | 新しく追加された | [TiDB はテーブル作成を高速化します](/accelerated-table-creation.md)有効にするかどうかを制御します。有効にするには値を`ON`に設定し、無効にするには`OFF`に設定します。デフォルト値は`ON`です。この変数を有効にすると、TiDB は[`CREATE TABLE`](/sql-statements/sql-statement-create-table.md)使用してテーブル作成を高速化します。 |
| [`tidb_load_binding_timeout`](/system-variables.md#tidb_load_binding_timeout-new-in-v800)                                 | 新しく追加された | バインディングの読み込みのタイムアウトを制御します。バインディングの読み込みの実行時間がこの値を超えると、読み込みは停止します。                                                                                                                                                            |
| [`tidb_low_resolution_tso_update_interval`](/system-variables.md#tidb_low_resolution_tso_update_interval-new-in-v800)     | 新しく追加された | TiDB [キャッシュタイムスタンプ](/system-variables.md#tidb_low_resolution_tso)の更新間隔を制御します。                                                                                                                                               |
| [`tidb_opt_ordering_index_selectivity_ratio`](/system-variables.md#tidb_opt_ordering_index_selectivity_ratio-new-in-v800) | 新しく追加された | SQL 文に`ORDER BY`と`LIMIT`句があり、一部のフィルタ条件がインデックスでカバーされていない場合に、SQL 文`ORDER BY`に一致するインデックスの推定行数を制御します。デフォルト値は`-1`で、このシステム変数を無効にすることを意味します。                                                                                       |
| [`tidb_opt_use_invisible_indexes`](/system-variables.md#tidb_opt_use_invisible_indexes-new-in-v800)                       | 新しく追加された | 現在のセッションでオプティマイザがクエリの最適化に[非表示のインデックス](/sql-statements/sql-statement-create-index.md#invisible-index)選択できるかどうかを制御します。変数が`ON`に設定されている場合、オプティマイザはセッションでクエリの最適化に非表示のインデックスを選択できます。                                              |
| [`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-new-in-v800)                                       | 新しく追加された | スキーマ情報のキャッシュに使用できるメモリの上限を制御し、過剰なメモリの占有を回避します。この機能を有効にすると、必要なテーブルをキャッシュするために LRU アルゴリズムが使用され、スキーマ情報によって占有されるメモリが効果的に削減されます。                                                                                                  |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーションパラメータ                                                                                                                                               | タイプを変更   | 説明                                                                                                                                                                                                         |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ティビ            | [`instance.tidb_enable_collect_execution_info`](/tidb-configuration-file.md#tidb_enable_collect_execution_info)                                               | 修正済み     | [インデックスの使用統計](/information-schema/information-schema-tidb-index-usage.md)を記録するかどうかのコントロールを追加します。デフォルト値は`true`です。                                                                                           |
| ティビ            | [`tls-version`](/tidb-configuration-file.md#tls-version)                                                                                                      | 修正済み     | このパラメータは`"TLSv1.0"`と`"TLSv1.1"`サポートしなくなりました。現在は`"TLSv1.2"`と`"TLSv1.3"`のみをサポートしています。                                                                                                                        |
| ティビ            | [`log.file.compression`](/tidb-configuration-file.md#compression-new-in-v800)                                                                                 | 新しく追加された | ポーリング ログの圧縮形式を指定します。デフォルト値は null で、ポーリング ログは圧縮されません。                                                                                                                                                       |
| ティビ            | [`log.general-log-file`](/tidb-configuration-file.md#general-log-file-new-in-v800)                                                                            | 新しく追加された | 一般ログを保存するファイルを指定します。デフォルトは null で、一般ログはインスタンス ファイルに書き込まれます。                                                                                                                                                |
| ティビ            | [`tikv-client.enable-replica-selector-v2`](/tidb-configuration-file.md#enable-replica-selector-v2-new-in-v800)                                                | 新しく追加された | RPC 要求を TiKV に送信するときに、リージョンレプリカ セレクターの新しいバージョンを使用するかどうかを制御します。デフォルト値は`true`です。                                                                                                                             |
| ティクヴ           | [`log-backup.initial-scan-rate-limit`](/tikv-configuration-file.md#initial-scan-rate-limit-new-in-v620)                                                       | 修正済み     | 最小値として`1MiB`の制限を追加します。                                                                                                                                                                                     |
| ティクヴ           | [`raftstore.store-io-pool-size`](/tikv-configuration-file.md#store-io-pool-size-new-in-v530)                                                                  | 修正済み     | TiKV のパフォーマンスを向上させるためにデフォルト値を`0`から`1`に変更します。つまり、StoreWriter スレッド プールのサイズはデフォルトで`1`になります。                                                                                                                   |
| ティクヴ           | [`rocksdb.defaultcf.titan.blob-cache-size`](/tikv-configuration-file.md#blob-cache-size)                                                                      | 修正済み     | v8.0.0 以降、TiKV は`shared-blob-cache`構成項目を導入し、デフォルトで有効になっているため、 `blob-cache-size`別途設定する必要はありません。 `blob-cache-size`の構成は、 `shared-blob-cache` `false`に設定されている場合にのみ有効になります。                                     |
| ティクヴ           | [`security.encryption.master-key.vendor`](/encryption-at-rest.md#specify-a-master-key-via-kms)                                                                | 修正済み     | サービス プロバイダーの使用可能なタイプとして`gcp`追加します。                                                                                                                                                                         |
| ティクヴ           | [`rocksdb.defaultcf.titan.shared-blob-cache`](/tikv-configuration-file.md#shared-blob-cache-new-in-v800)                                                      | 新しく追加された | Titan BLOB ファイルと RocksDB ブロック ファイルの共有キャッシュを有効にするかどうかを制御します。デフォルト値は`true`です。                                                                                                                                |
| ティクヴ           | [`security.encryption.master-key.gcp.credential-file-path`](/encryption-at-rest.md#specify-a-master-key-via-kms)                                              | 新しく追加された | `security.encryption.master-key.vendor`が`gcp`場合、Google Cloud 認証認証情報ファイルへのパスを指定します。                                                                                                                         |
| TiDB Lightning | [`tikv-importer.duplicate-resolution`](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#the-old-version-of-conflict-detection-deprecated-in-v800) | 非推奨      | 物理インポート モードで一意のキーの競合を検出して解決するかどうかを制御します。v8.0.0 以降では、 [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)に置き換えられます。                                                  |
| TiDB Lightning | [`conflict.precheck-conflict-before-import`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)                                             | 新しく追加された | インポート前の競合検出を有効にするかどうかを制御します。これは、データを TiDB にインポートする前に競合をチェックします。このパラメータのデフォルト値は`false`です。つまり、 TiDB Lightning はデータのインポート後にのみ競合をチェックします。このパラメータは、物理インポート モード ( `tikv-importer.backend = "local"` ) でのみ使用できます。 |
| TiDB Lightning | [`logical-import-batch-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)                                                            | 新しく追加された | 論理インポート モードでトランザクションごとに挿入される行の最大数を制御します。デフォルト値は`65536`行です。                                                                                                                                                 |
| TiDB Lightning | [`logical-import-batch-size`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)                                                            | 新しく追加された | 論理インポート モードでダウンストリーム TiDBサーバー上で実行される各 SQL クエリの最大サイズを制御します。デフォルト値は`"96KiB"`です。単位は KB、KiB、MB、または MiB です。                                                                                                     |
| データ移行          | [`secret-key-path`](/dm/dm-master-configuration-file.md)                                                                                                      | 新しく追加された | アップストリームおよびダウンストリーム パスワードの暗号化と復号化に使用される秘密キーのファイル パスを指定します。ファイルには、64 文字の 16 進数 AES-256 秘密キーが含まれている必要があります。                                                                                                  |
| ティCDC          | [`debezium-disable-schema`](/ticdc/ticdc-changefeed-config.md)                                                                                                | 新しく追加された | スキーマ情報の出力を無効にするかどうかを制御します。このパラメータは、シンク タイプが MQ で、出力プロトコルが Debezium の場合にのみ有効です。                                                                                                                             |

| TiCDC | [`tls-certificate-file`](/ticdc/ticdc-sink-to-pulsar.md) | 新しく追加 | Pulsar が TLS 暗号化伝送を有効にするときに必要な、クライアント上の暗号化された証明書ファイルへのパスを指定します。 | | TiCDC | [`tls-key-file-path`](/ticdc/ticdc-sink-to-pulsar.md) | 新しく追加 | Pulsar が TLS 暗号化伝送を有効にするときに必要な、クライアント上の暗号化された秘密キーへのパスを指定します。 |

### システムテーブル {#system-tables}

-   TiDB ノードのインデックス使用統計を記録するために、新しいシステム テーブル[`INFORMATION_SCHEMA.TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md)と[`INFORMATION_SCHEMA.CLUSTER_TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md#cluster_tidb_index_usage)を追加します。
-   新しいシステム スキーマ[`sys`](/sys-schema/sys-schema.md)と新しいビュー[`sys.schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md)を追加します。これは、TiDB の最後の起動以降に使用されていないインデックスを記録します。

## 廃止された機能 {#deprecated-features}

-   v8.0.0 以降、 [`tidb_disable_txn_auto_retry`](/system-variables.md#tidb_disable_txn_auto_retry)システム変数は非推奨となり、TiDB は楽観的トランザクションの自動再試行をサポートしなくなりました。代わりに、楽観的ミスティック トランザクションの競合が発生した場合は、エラーをキャプチャしてアプリケーションでトランザクションを再試行するか、代わりに[悲観的なトランザクションモード](/pessimistic-transaction.md)使用することができます。
-   v8.0.0 以降、TiDB は TLSv1.0 および TLSv1.1 プロトコルをサポートしなくなりました。TLS を TLSv1.2 または TLSv1.3 にアップグレードする必要があります。
-   v8.0.0 以降、 TiDB Lightning物理インポート モードの[競合検出の旧バージョン](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#the-old-version-of-conflict-detection-deprecated-in-v800)戦略が廃止され、 [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md)パラメータを使用して論理インポート モードと物理インポート モードの両方の競合検出戦略を制御できるようになりました。競合検出の旧バージョンの[`duplicate-resolution`](/tidb-lightning/tidb-lightning-configuration.md)パラメータは、将来のリリースで削除される予定です。
-   以降のリリースでは[実行計画バインディングの自動進化](/sql-plan-management.md#baseline-evolution)再設計する予定であり、関連する変数と動作が変更されます。

## 改善点 {#improvements}

-   ティビ

    -   `CREATE TABLE` DDL文の実行パフォーマンスを10倍向上し、線形スケーラビリティ[＃50052](https://github.com/pingcap/tidb/issues/50052) @ [GMHDBJD](https://github.com/GMHDBJD)をサポート
    -   16 `IMPORT INTO ... FROM FILE`タスクの同時送信をサポートし、ターゲット テーブルへの一括データ インポートを容易にし、データ ファイルのインポートの効率とパフォーマンスを大幅に向上させます[＃49008](https://github.com/pingcap/tidb/issues/49008) @ [D3ハンター](https://github.com/D3Hunter)
    -   `Sort`オペレータ[＃47733](https://github.com/pingcap/tidb/issues/47733) @ [翻訳者](https://github.com/xzhangxian1008)のディスクへのデータ書き込みのパフォーマンスを向上
    -   ディスクへのデータのスピル中にクエリをキャンセルする機能をサポートし、データスピル機能の終了メカニズムを最適化します[＃50511](https://github.com/pingcap/tidb/issues/50511) @ [うわー](https://github.com/wshwsh12)
    -   複数の等条件を持つテーブル結合クエリを処理するときに、部分条件に一致するインデックスを使用してインデックス結合を構築することをサポートします[＃47233](https://github.com/pingcap/tidb/issues/47233) @ [ウィノロス](https://github.com/winoros)
    -   インデックスマージの機能を強化して、クエリ内のソート要件を識別し、ソート要件を満たすインデックスを選択します[＃48359](https://github.com/pingcap/tidb/issues/48359) @ [アイリンキッド](https://github.com/AilinKid)
    -   `Apply`演算子が同時に実行されない場合、TiDBでは`SHOW WARNINGS` [＃50256](https://github.com/pingcap/tidb/issues/50256) @ [ホーキングレイ](https://github.com/hawkingrei)を実行することで同時実行をブロックする演算子の名前を表示できます。
    -   すべてのインデックスが`point get`クエリをサポートしている場合、クエリに最適なインデックスを選択して、 `point get`クエリのインデックス選択を最適化します[＃50184](https://github.com/pingcap/tidb/issues/50184) @ [エルサ0520](https://github.com/elsa0520)
    -   TiKV の高負荷時に広範囲にわたるタイムアウトを回避するために、統計を同期的にロードするタスクの優先度を一時的に高く調整します。タイムアウトにより、統計がロードされない可能性があります[＃50332](https://github.com/pingcap/tidb/issues/50332) @ [ウィノロス](https://github.com/winoros)
    -   `PREPARE`ステートメントが実行プランキャッシュにヒットしない場合、TiDBでは`SHOW WARNINGS` [＃50407](https://github.com/pingcap/tidb/issues/50407) @ [ホーキングレイ](https://github.com/hawkingrei)を実行することでその理由を確認できます。
    -   同じデータ行が複数回更新された場合のクエリ推定情報の精度を向上[＃47523](https://github.com/pingcap/tidb/issues/47523) @ [テリー・パーセル](https://github.com/terry1purcell)
    -   インデックスマージは、 `AND`述語[＃51778](https://github.com/pingcap/tidb/issues/51778) @ [時間と運命](https://github.com/time-and-fate)に複数値インデックスと`OR`演算子を埋め込むことをサポートします。
    -   `force-init-stats` `true`に設定すると、TiDB は統計の初期化が完了するまで待機してから、TiDB の起動中にサービスを提供します。この設定により、HTTP サーバーの起動がブロックされなくなり、ユーザーは[＃50854](https://github.com/pingcap/tidb/issues/50854) @ [ホーキングレイ](https://github.com/hawkingrei)監視を継続できます。
    -   MemoryTrackerは`IndexLookup`演算子[＃45901](https://github.com/pingcap/tidb/issues/45901) @ [ソロッツ](https://github.com/solotzg)のメモリ使用量を追跡できます
    -   MemoryTrackerは`MemTableReaderExec`演算子[＃51456](https://github.com/pingcap/tidb/issues/51456) @ [うわー](https://github.com/wshwsh12)のメモリ使用量を追跡できます
    -   大規模なテーブルをクエリするときに、KV 範囲からリージョンへの変換プロセスを高速化するために、PD からリージョンをバッチでロードする機能をサポート[＃51326](https://github.com/pingcap/tidb/issues/51326) @ [シーライズ](https://github.com/SeaRise)
    -   システムテーブル`INFORMATION_SCHEMA.TABLES` 、 `INFORMATION_SCHEMA.STATISTICS` 、 `INFORMATION_SCHEMA.KEY_COLUMN_USAGE` 、 `INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS`のクエリパフォーマンスを最適化します。以前のバージョンと比較し[うわー](https://github.com/ywqzzy) 、パフォーマンスは最大 100 倍向上しました。9 @ [＃50305](https://github.com/pingcap/tidb/issues/50305)

-   ティクヴ

    -   TSOの検証と検出を強化して、構成や操作が不適切な場合のクラスターTSOの堅牢性を向上させる[＃16545](https://github.com/tikv/tikv/issues/16545) @ [翻訳](https://github.com/cfzjywxk)
    -   コミットされていないトランザクションの処理パフォーマンスを向上させるために、悲観的ロックのクリーンアップロジックを最適化します[＃16158](https://github.com/tikv/tikv/issues/16158) @ [翻訳](https://github.com/cfzjywxk)
    -   TiKV の統合ヘルスコントロールを導入して、異常な単一 TiKV ノードがクラスターアクセスパフォーマンスに与える影響を軽減します[`tikv-client.enable-replica-selector-v2`](/tidb-configuration-file.md#enable-replica-selector-v2-new-in-v800)から`false`に設定することで[＃16297](https://github.com/tikv/tikv/issues/16297)この最適化を無効にすることができます。5 [＃1104](https://github.com/tikv/client-go/issues/1104) [＃1167](https://github.com/tikv/client-go/issues/1167) @ [ミョンケミンタ](https://github.com/MyonKeminta) @ [ジグアン](https://github.com/zyguan) @ [クレイジーcs520](https://github.com/crazycs520)
    -   PDクライアントは、メタデータstorageインターフェースを使用して、以前のグローバル構成インターフェース[＃14484](https://github.com/tikv/tikv/issues/14484) @ [ヒューシャープ](https://github.com/HuSharp)を置き換えます。
    -   write cf stats [＃16245](https://github.com/tikv/tikv/issues/16245) @ [コナー1996](https://github.com/Connor1996)を通じてデータの読み込み動作を決定することでスキャンのパフォーマンスを向上させます。
    -   Raft conf 変更プロセス中にノードが削除され、投票者が降格されたかどうか最新のハートビートをチェックして、この動作によってリージョンがアクセス不能にならないことを確認します[＃15799](https://github.com/tikv/tikv/issues/15799) @ [トニー](https://github.com/tonyxuqqi)
    -   パイプライン DML [＃16291](https://github.com/tikv/tikv/issues/16291) @ [エキシウム](https://github.com/ekexium)用の Flush および BufferBatchGet インターフェイスを追加します。
    -   cgroup CPU とメモリ制限の監視とアラートを追加[＃16392](https://github.com/tikv/tikv/issues/16392) @ [ピンとb](https://github.com/pingandb)
    -   リージョンワーカーとスナップショット生成ワーカー[＃16562](https://github.com/tikv/tikv/issues/16562) @ [コナー1996](https://github.com/Connor1996) CPU モニタリングを追加します。
    -   ピアのスローログを追加し、メッセージ[＃16600](https://github.com/tikv/tikv/issues/16600) @ [コナー1996](https://github.com/Connor1996)を保存します。

-   PD

    -   PDクライアントのサービス検出機能を強化して、高可用性と負荷分散を改善します[＃7576](https://github.com/tikv/pd/issues/7576) @ [キャビンフィーバーB](https://github.com/CabinfeverB)
    -   PDクライアント[＃7673](https://github.com/tikv/pd/issues/7673) @ [じゃがいも](https://github.com/JmPotato)の再試行メカニズムを強化
    -   cgroup CPU とメモリ制限の監視とアラートを追加[＃7716](https://github.com/tikv/pd/issues/7716) [＃7918](https://github.com/tikv/pd/issues/7918) @ [ピンとb](https://github.com/pingandb) @ [rleungx](https://github.com/rleungx)
    -   etcd使用時のパフォーマンスと高可用性を向上させる[＃7738](https://github.com/tikv/pd/issues/7738) [＃7724](https://github.com/tikv/pd/issues/7724) [＃7689](https://github.com/tikv/pd/issues/7689) @ [翻訳:](https://github.com/lhy1024)
    -   パフォーマンスのボトルネックをより適切に分析するために、ハートビートの監視メトリックを追加します[＃7868](https://github.com/tikv/pd/issues/7868) @ [ノルーシュ](https://github.com/nolouch)
    -   etcdリーダーのPDリーダーへの影響を軽減する[＃7499](https://github.com/tikv/pd/issues/7499) @ [じゃがいも](https://github.com/JmPotato) @ [ヒューシャープ](https://github.com/HuSharp)
    -   不健全なetcdノードの検出メカニズムを強化する[＃7730](https://github.com/tikv/pd/issues/7730) @ [じゃがいも](https://github.com/JmPotato) @ [ヒューシャープ](https://github.com/HuSharp)
    -   pd-ctl [＃7767](https://github.com/tikv/pd/issues/7767) @ [ノルーシュ](https://github.com/nolouch)の GC セーフポイントの出力を最適化します。
    -   ホットスポットスケジューラ[＃7877](https://github.com/tikv/pd/issues/7877) @ [翻訳者](https://github.com/lhy1024)の履歴ウィンドウ構成の動的変更をサポート
    -   演算子[＃7837](https://github.com/tikv/pd/issues/7837) @ [リーヴルス](https://github.com/Leavrth)作成時のロック競合の問題を軽減します。
    -   GRPC 構成を調整して可用性を向上させる[＃7821](https://github.com/tikv/pd/issues/7821) @ [rleungx](https://github.com/rleungx)

-   TiFlash

    -   `JSON_EXTRACT()`関数[＃8510](https://github.com/pingcap/tiflash/issues/8510) @ [シーライズ](https://github.com/SeaRise)の`json_path`引数に非定数値の使用をサポート
    -   `JSON_LENGTH(json, path)`機能[＃8711](https://github.com/pingcap/tiflash/issues/8711) @ [シーライズ](https://github.com/SeaRise)をサポート

-   ツール

    -   バックアップと復元 (BR)

        -   `br`コマンドラインツールに新しい復元パラメータ`--load-stats`を導入し、統計[＃50568](https://github.com/pingcap/tidb/issues/50568) @ [リーヴルス](https://github.com/Leavrth)を復元するかどうかを制御します。
        -   `br`コマンドライン ツールに新しい復元パラメータ`--tikv-max-restore-concurrency`を導入しました。これは、各 TiKV ノードのダウンロード ファイルと取り込みファイルの最大数を制御します。このパラメータは、ジョブ キューの最大長を制御することで、 BRノードのメモリ消費も制御します[＃51621](https://github.com/pingcap/tidb/issues/51621) @ [3ポインター](https://github.com/3pointer)
        -   粗粒度のリージョン分散アルゴリズムを有効にして同時パラメータ[＃50701](https://github.com/pingcap/tidb/issues/50701) @ [3ポインター](https://github.com/3pointer)を適応的に取得することで、復元パフォーマンスが向上します。
        -   `br` [＃50927](https://github.com/pingcap/tidb/issues/50927) @ [リドリス](https://github.com/RidRisR)のコマンドラインヘルプ情報に`log`コマンドを表示します
        -   復元プロセス中にテーブル ID を事前割り当てして、テーブル ID の再利用を最大限にし、復元パフォーマンスを向上させる[＃51736](https://github.com/pingcap/tidb/issues/51736) @ [リーヴルス](https://github.com/Leavrth)
        -   OOM の問題を回避するために、 BR を使用するときは TiDB 内の GCメモリ制限チューナー機能を無効にします[＃51078](https://github.com/pingcap/tidb/issues/51078) @ [リーヴルス](https://github.com/Leavrth)
        -   より効率的なアルゴリズム[＃50613](https://github.com/pingcap/tidb/issues/50613) @ [リーヴルス](https://github.com/Leavrth)を使用して、データ復元中に SST ファイルをマージする速度を向上します
        -   データ復元中にバッチでデータベースを作成するサポート[＃50767](https://github.com/pingcap/tidb/issues/50767) @ [リーヴルス](https://github.com/Leavrth)
        -   ログバックアップ中にログとメトリックのグローバルチェックポイントの進行に影響を与える最も遅いリージョンの情報を出力します[＃51046](https://github.com/pingcap/tidb/issues/51046) @ [ユジュンセン](https://github.com/YuJuncen)
        -   大規模なデータセットのシナリオで`RESTORE`ステートメントのテーブル作成パフォーマンスを向上[＃48301](https://github.com/pingcap/tidb/issues/48301) @ [リーヴルス](https://github.com/Leavrth)

    -   ティCDC

        -   TiCDCがデータを複製する際のメモリ消費量を削減するために、 `RowChangedEvent`のメモリ消費量を最適化します[＃10386](https://github.com/pingcap/tiflow/issues/10386) @ [リデズ](https://github.com/lidezhu)
        -   変更フィードタスク[＃10499](https://github.com/pingcap/tiflow/issues/10499) @ [3エースショーハンド](https://github.com/3AceShowHand)の作成および再開時に start-ts パラメータが有効であることを確認します。

    -   TiDB データ移行 (DM)

        -   MariaDB プライマリ - セカンダリ レプリケーション シナリオでは、移行パスが MariaDB プライマリ インスタンス -&gt; MariaDB セカンダリ インスタンス -&gt; DM -&gt; TiDB であり、 `gtid_strict_mode = off`で MariaDB セカンダリ インスタンスの GTID が厳密に増加していない場合 (たとえば、MariaDB セカンダリ インスタンスにデータが書き込まれている場合)、DM タスクはエラー`less than global checkpoint position`を報告します。v8.0.0 以降、TiDB はこのシナリオと互換性があり、データを通常どおりにダウンストリームに移行できます[＃10741](https://github.com/pingcap/tiflow/issues/10741) @ [ok江](https://github.com/okJiang)

    -   TiDB Lightning

        -   [`logical-import-batch-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task) [＃46607](https://github.com/pingcap/tidb/issues/46607) @ [ケニー](https://github.com/kennytm)を使用して論理インポート モードでバッチ内の最大行数を構成することをサポートします。
        -   TiDB LightningはTiFlashの容量が不足するとエラーを報告します[＃50324](https://github.com/pingcap/tidb/issues/50324) @ [ok江](https://github.com/okJiang)

## バグ修正 {#bug-fixes}

-   ティビ

    -   データの変更がないのに`auto analyze`が複数回トリガーされる問題を修正[＃51775](https://github.com/pingcap/tidb/issues/51775) @ [ハイラスティン](https://github.com/Rustin170506)
    -   `auto analyze`同時実行が誤って[＃51749](https://github.com/pingcap/tidb/issues/51749) @ [ホーキングレイ](https://github.com/hawkingrei)に設定されている問題を修正
    -   単一のSQL文を使用して複数のインデックスを追加することで発生するインデックスの不整合の問題を修正[＃51746](https://github.com/pingcap/tidb/issues/51746) @ [タンジェンタ](https://github.com/tangenta)
    -   クエリで`NATURAL JOIN` [＃32044](https://github.com/pingcap/tidb/issues/32044) @ [アイリンキッド](https://github.com/AilinKid)が使用される場合に発生する可能性のある`Column ... in from clause is ambiguous`エラーを修正します。
    -   TiDB が`group by` [＃38756](https://github.com/pingcap/tidb/issues/38756) @ [ハイラスティン](https://github.com/Rustin170506)の定数値を誤って削除したために間違ったクエリ結果が発生する問題を修正しました。
    -   `LEADING`のヒントが`UNION ALL`ステートメント[＃50067](https://github.com/pingcap/tidb/issues/50067) @ [ホーキングレイ](https://github.com/hawkingrei)で有効にならない問題を修正
    -   `BIT`型の列が一部の関数の計算に関係する場合にデコード失敗によりクエリ エラーが発生する可能性がある問題を修正しました[＃49566](https://github.com/pingcap/tidb/issues/49566) [＃50850](https://github.com/pingcap/tidb/issues/50850) [＃50855](https://github.com/pingcap/tidb/issues/50855) @ [ジフハウス](https://github.com/jiyfhust)
    -   PD [＃50152](https://github.com/pingcap/tidb/issues/50152) @ [ジムララ](https://github.com/zimulala)との相互作用の問題により、 `tiup cluster upgrade/start`使用してローリング アップグレードを実行すると TiDB がpanicになる可能性がある問題を修正しました。
    -   `ORDER BY`句で`UNIQUE`インデックス検索を実行するとエラー[＃49920](https://github.com/pingcap/tidb/issues/49920) @ [ジャッキー](https://github.com/jackysp)が発生する可能性がある問題を修正しました
    -   定数伝播[＃49440](https://github.com/pingcap/tidb/issues/49440) @ [ウィノロス](https://github.com/winoros)で`ENUM`または`SET`型を処理するときに TiDB が間違ったクエリ結果を返す問題を修正しました
    -   クエリに Apply 演算子が含まれており、 `fatal error: concurrent map writes`エラーが発生すると TiDB がpanicになる可能性がある問題を修正しました[＃50347](https://github.com/pingcap/tidb/issues/50347) @ [シーライズ](https://github.com/SeaRise)
    -   文字列型の変数に対する`SET_VAR`の制御が無効になる可能性がある問題を修正[＃50507](https://github.com/pingcap/tidb/issues/50507) @ [qw4990](https://github.com/qw4990)
    -   `tidb_sysdate_is_now`が`1` [＃49299](https://github.com/pingcap/tidb/issues/49299) @ [ホーキングレイ](https://github.com/hawkingrei)に設定されている場合に、 `SYSDATE()`関数がプラン キャッシュ内の時間を誤って使用する問題を修正しました。
    -   `CREATE GLOBAL BINDING`ステートメントを実行するときに、スキーマ名が大文字の場合、バインディングが有効にならない問題を修正しました[＃50646](https://github.com/pingcap/tidb/issues/50646) @ [qw4990](https://github.com/qw4990)
    -   `Index Path`重複したインデックス[＃50496](https://github.com/pingcap/tidb/issues/50496) @ [アイリンキッド](https://github.com/AilinKid)を選択する問題を修正
    -   `CREATE GLOBAL BINDING`文に`IN()` [＃43192](https://github.com/pingcap/tidb/issues/43192) @ [キング・ディラン](https://github.com/King-Dylan)含まれている場合に`PLAN REPLAYER`バインディングのロードに失敗する問題を修正しました
    -   複数の`analyze`タスクが失敗した場合に失敗理由が正しく記録されない問題を修正[＃50481](https://github.com/pingcap/tidb/issues/50481) @ [ハイラスティン](https://github.com/Rustin170506)
    -   `tidb_stats_load_sync_wait` [ジフハウス](https://github.com/jiyfhust)で[＃50872](https://github.com/pingcap/tidb/issues/50872)反映されない問題を修正
    -   複数のレベルの`max_execute_time`設定が互いに干渉する問題を修正[＃50914](https://github.com/pingcap/tidb/issues/50914) @ [ジフハウス](https://github.com/jiyfhust)
    -   統計[＃50835](https://github.com/pingcap/tidb/issues/50835) @ [ハイラスティン](https://github.com/Rustin170506)の同時更新によって発生するスレッド セーフティの問題を修正しました。
    -   パーティションテーブルで`auto analyze`実行すると TiDB がpanicを起こす可能性がある問題を修正[＃51187](https://github.com/pingcap/tidb/issues/51187) @ [ハイラスティン](https://github.com/Rustin170506)
    -   SQL ステートメントの`IN()`に異なる数の値[＃51222](https://github.com/pingcap/tidb/issues/51222) @ [ホーキングレイ](https://github.com/hawkingrei)が含まれている場合に SQL バインディングが機能しない可能性がある問題を修正しました。
    -   TiDB が式[＃43527](https://github.com/pingcap/tidb/issues/43527) @ [ハイラスティン](https://github.com/Rustin170506)内のシステム変数の型を正しく変換できない問題を修正
    -   `force-init-stats`が[＃51473](https://github.com/pingcap/tidb/issues/51473) @ [ホーキングレイ](https://github.com/hawkingrei)に設定されている場合に TiDB が対応するポートをリッスンしない問題を修正
    -   `determinate`モード ( `tidb_opt_objective='determinate'` ) でクエリに述語が含まれていない場合、統計がロードされない可能性がある問題を修正しました[＃48257](https://github.com/pingcap/tidb/issues/48257) @ [時間と運命](https://github.com/time-and-fate)
    -   `init-stats`プロセスが TiDB をpanicに陥らせ、 `load stats`プロセスが[＃51581](https://github.com/pingcap/tidb/issues/51581) @ [ホーキングレイ](https://github.com/hawkingrei)で終了する可能性がある問題を修正しました。
    -   `IN()`述語に`NULL` [＃51560](https://github.com/pingcap/tidb/issues/51560) @ [ウィノロス](https://github.com/winoros)含まれている場合にクエリ結果が正しくない問題を修正しました
    -   DDL タスクに複数のテーブルが含まれる場合に、ブロックされた DDL ステートメントが MDLビューに表示されない問題を修正[＃47743](https://github.com/pingcap/tidb/issues/47743) @ [翻訳:](https://github.com/wjhuang2016)
    -   テーブル上の`ANALYZE`のタスクのうち`processed_rows`が、そのテーブルの合計行数[＃50632](https://github.com/pingcap/tidb/issues/50632) @ [ホーキングレイ](https://github.com/hawkingrei)を超える可能性がある問題を修正しました。
    -   `HashJoin`演算子がディスク[＃50841](https://github.com/pingcap/tidb/issues/50841) @ [うわー](https://github.com/wshwsh12)にスピルできない場合に発生する可能性のある goroutine リークの問題を修正しました。
    -   CTE クエリのメモリ使用量が制限[＃50337](https://github.com/pingcap/tidb/issues/50337) @ [グオシャオゲ](https://github.com/guo-shaoge)を超えた場合に発生する goroutine リークの問題を修正しました
    -   集計関数をグループ計算に使用した場合に発生する可能性のある`Can't find column ...`エラーを修正[＃50926](https://github.com/pingcap/tidb/issues/50926) @ [qw4990](https://github.com/qw4990)
    -   `CREATE TABLE`ステートメントに特定のパーティションまたは制約が含まれている場合に、テーブル名の変更などの DDL 操作が停止する問題を修正しました[＃50972](https://github.com/pingcap/tidb/issues/50972) @ [lcwangchao](https://github.com/lcwangchao)
    -   Grafana の監視メトリック`tidb_statistics_auto_analyze_total`が整数[＃51051](https://github.com/pingcap/tidb/issues/51051) @ [ホーキングレイ](https://github.com/hawkingrei)として表示されない問題を修正しました。
    -   `tidb_server_memory_limit`変数が変更された後に`tidb_gogc_tuner_threshold`システム変数がそれに応じて調整されない問題を修正[＃48180](https://github.com/pingcap/tidb/issues/48180) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   クエリにJOIN操作[＃42588](https://github.com/pingcap/tidb/issues/42588) @ [アイリンキッド](https://github.com/AilinKid)が含まれる場合に`index out of range`エラーが発生する可能性がある問題を修正
    -   列のデフォルト値が削除されている場合、列のデフォルト値を取得するとエラーが返される問題を修正[＃50043](https://github.com/pingcap/tidb/issues/50043) [＃51324](https://github.com/pingcap/tidb/issues/51324) @ [クレイジーcs520](https://github.com/crazycs520)
    -   TiFlash の遅延マテリアライゼーションが関連列[＃49241](https://github.com/pingcap/tidb/issues/49241) [＃51204](https://github.com/pingcap/tidb/issues/51204) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)を処理するときに間違った結果が返される可能性がある問題を修正しました
    -   バイナリ照合順序入力[＃50393](https://github.com/pingcap/tidb/issues/50393) @ [いびん87](https://github.com/yibin87)を処理するときに`LIKE()`関数が間違った結果を返す可能性がある問題を修正しました
    -   2 番目のパラメータが`NULL` [＃50931](https://github.com/pingcap/tidb/issues/50931) @ [シーライズ](https://github.com/SeaRise)の場合に`JSON_LENGTH()`関数が間違った結果を返す問題を修正しました
    -   特定の状況下で時間精度が失われる`CAST(AS DATETIME)`性がある問題を修正[＃49555](https://github.com/pingcap/tidb/issues/49555) @ [シーライズ](https://github.com/SeaRise)
    -   テーブルにクラスター化インデックス[＃51372](https://github.com/pingcap/tidb/issues/51372) @ [グオシャオゲ](https://github.com/guo-shaoge)がある場合に並列`Apply`で誤った結果が生成される可能性がある問題を修正しました。
    -   主キータイプが`VARCHAR` [＃51810](https://github.com/pingcap/tidb/issues/51810) @ [そよ風のような](https://github.com/breezewish)の場合に`ALTER TABLE ... COMPACT TIFLASH REPLICA`誤って終了する可能性がある問題を修正しました
    -   `EXCHANGE PARTITION`ステートメント[＃47167](https://github.com/pingcap/tidb/issues/47167) @ [ジフハウス](https://github.com/jiyfhust)を使用してパーティション テーブルを交換するときに、 `DEFAULT NULL`属性の`NULL`値のチェックが正しく行われない問題を修正しました。
    -   パーティションテーブル定義がUTF8以外の文字セット[＃49251](https://github.com/pingcap/tidb/issues/49251) @ [ヤンケオ](https://github.com/YangKeao)を使用する際に誤った動作を引き起こす可能性がある問題を修正
    -   一部のシステム変数[＃49461](https://github.com/pingcap/tidb/issues/49461) @ [ジフハウス](https://github.com/jiyfhust) `INFORMATION_SCHEMA.VARIABLES_INFO`テーブルに誤ったデフォルト値が表示される問題を修正
    -   一部のケースでデータベース名に空の文字列が使用された場合にエラーが報告されない問題を修正[＃45873](https://github.com/pingcap/tidb/issues/45873) @ [ヨシキポム](https://github.com/yoshikipom)
    -   `SPLIT TABLE ... INDEX`文で TiDB がpanicを起こす可能性がある問題を修正[＃50177](https://github.com/pingcap/tidb/issues/50177) @ [定義2014](https://github.com/Defined2014)
    -   `KeyPartition`種類のパーティションテーブルをクエリするとエラーが発生する可能性がある問題を修正しました[＃50206](https://github.com/pingcap/tidb/issues/50206) [＃51313](https://github.com/pingcap/tidb/issues/51313) [＃51196](https://github.com/pingcap/tidb/issues/51196) @ [時間と運命](https://github.com/time-and-fate) @ [ジフハウス](https://github.com/jiyfhust) @ [ミョンス](https://github.com/mjonss)
    -   ハッシュパーティションテーブルをクエリすると誤った結果が生成される可能性がある問題を修正[＃50427](https://github.com/pingcap/tidb/issues/50427) @ [定義2014](https://github.com/Defined2014)
    -   オープントレースが正しく動作しない問題を修正[＃50508](https://github.com/pingcap/tidb/issues/50508) @ [定義2014](https://github.com/Defined2014)
    -   `ALTER INSTANCE RELOAD TLS`エラー[＃50699](https://github.com/pingcap/tidb/issues/50699) @ [ドヴェーデン](https://github.com/dveeden)を報告したときにエラー メッセージが完全ではない問題を修正
    -   自動増分 ID [＃50819](https://github.com/pingcap/tidb/issues/50819) @ [天菜まお](https://github.com/tiancaiamao)を割り当てるときに、 `AUTO_INCREMENT`属性によって不要なトランザクション競合が発生し、ID が連続しなくなる問題を修正しました。
    -   いくつかのエラー[＃50849](https://github.com/pingcap/tidb/issues/50849) @ [天菜まお](https://github.com/tiancaiamao)について、TiDB ログ内のスタック情報が不完全になる問題を修正しました
    -   `LIMIT`句の数値が大きすぎる場合に一部のクエリでメモリ使用量が過剰になる問題を修正[＃51188](https://github.com/pingcap/tidb/issues/51188) @ [定義2014](https://github.com/Defined2014)
    -   TTL 機能により、データ範囲の分割が不正確になり、場合によってはデータ ホットスポットが発生する問題を修正しました[＃51527](https://github.com/pingcap/tidb/issues/51527) @ [lcwangchao](https://github.com/lcwangchao)
    -   明示的なトランザクション[＃51387](https://github.com/pingcap/tidb/issues/51387) @ [ヤンケオ](https://github.com/YangKeao)の最初の行に`SET`ステートメントが表示された場合に有効にならない問題を修正しました
    -   `BINARY`タイプの JSON をクエリすると、場合によってはエラーが発生する可能性がある問題を修正しました[＃51547](https://github.com/pingcap/tidb/issues/51547) @ [ヤンケオ](https://github.com/YangKeao)
    -   有効期限[＃51675](https://github.com/pingcap/tidb/issues/51675) @ [lcwangchao](https://github.com/lcwangchao)を計算するときに、TTL が夏時間調整の移行を正しく処理しない問題を修正しました。
    -   特定の条件下では`SURVIVAL_PREFERENCES`属性が`SHOW CREATE PLACEMENT POLICY`ステートメントの出力に表示されない可能性がある問題を修正[＃51699](https://github.com/pingcap/tidb/issues/51699) @ [lcwangchao](https://github.com/lcwangchao)
    -   無効な設定項目[＃51399](https://github.com/pingcap/tidb/issues/51399) @ [定義2014](https://github.com/Defined2014)が含まれている場合に設定ファイルが有効にならない問題を修正しました

-   ティクヴ

    -   `tidb_enable_row_level_checksum`有効にすると TiKV がpanicになる可能性がある問題を修正[＃16371](https://github.com/tikv/tikv/issues/16371) @ [翻訳](https://github.com/cfzjywxk)
    -   例外的な状況で休止状態のリージョンがすぐに起動しない問題を修正[＃16368](https://github.com/tikv/tikv/issues/16368) @ [リクササシネーター](https://github.com/LykxSassinator)
    -   ノードをオフラインにする前に、リージョン内のすべてのレプリカの最後のハートビート時間をチェックすることで、1 つのレプリカがオフラインになるとリージョン全体が使用できなくなる問題を修正しました[＃16465](https://github.com/tikv/tikv/issues/16465) @ [トニー](https://github.com/tonyxuqqi)
    -   最大値`INT64`より大きく最大値`UINT64`より小さい JSON 整数が TiKV によって`FLOAT64`として解析され、TiDB [＃16512](https://github.com/tikv/tikv/issues/16512) @ [ヤンケオ](https://github.com/YangKeao)との不整合が発生する問題を修正しました。
    -   監視メトリック`tikv_unified_read_pool_thread_count`にデータがない場合がある問題を修正[＃16629](https://github.com/tikv/tikv/issues/16629) @ [ユジュンセン](https://github.com/YuJuncen)

-   PD

    -   `MergeLabels`関数が[＃7535](https://github.com/tikv/pd/issues/7535) @ [翻訳者](https://github.com/lhy1024)で呼び出されたときにデータ競合が発生する問題を修正
    -   `evict-leader-scheduler`インターフェースが[＃7672](https://github.com/tikv/pd/issues/7672) @ [キャビンフィーバーB](https://github.com/CabinfeverB)で呼び出されたときに出力がない問題を修正しました
    -   リーダースイッチ[＃7728](https://github.com/tikv/pd/issues/7728) @ [キャビンフィーバーB](https://github.com/CabinfeverB)後にPD監視項目`learner-peer-count`古い値を同期しない問題を修正
    -   `watch etcd`が正しくオフになっていない場合に発生するメモリリークの問題を修正[＃7807](https://github.com/tikv/pd/issues/7807) @ [rleungx](https://github.com/rleungx)
    -   一部の TSO ログでエラー原因[＃7496](https://github.com/tikv/pd/issues/7496) @ [キャビンフィーバーB](https://github.com/CabinfeverB)が印刷されない問題を修正しました
    -   再起動後に予期しない負の監視メトリックが発生する問題を修正[＃4489](https://github.com/tikv/pd/issues/4489) @ [翻訳者](https://github.com/lhy1024)
    -   Leaderリースがログ時間[＃7700](https://github.com/tikv/pd/issues/7700) @ [キャビンフィーバーB](https://github.com/CabinfeverB)より後に期限切れになる問題を修正しました
    -   TiDB（PDクライアント）とPD間のTLSスイッチが不一致の場合にTiDBがパニックになる問題を修正[＃7900](https://github.com/tikv/pd/issues/7900) [＃7902](https://github.com/tikv/pd/issues/7902) [＃7916](https://github.com/tikv/pd/issues/7916) @ [キャビンフィーバーB](https://github.com/CabinfeverB)
    -   Goroutine が適切に閉じられていないときにリークする問題を修正[＃7782](https://github.com/tikv/pd/issues/7782) @ [ヒューシャープ](https://github.com/HuSharp)
    -   pd-ctl が特殊文字[＃7798](https://github.com/tikv/pd/issues/7798) @ [じゃがいも](https://github.com/JmPotato)を含むスケジューラを削除できない問題を修正
    -   TSO [＃7864](https://github.com/tikv/pd/issues/7864) @ [キャビンフィーバーB](https://github.com/CabinfeverB)取得するときに PD クライアントがブロックされる可能性がある問題を修正しました

-   TiFlash

    -   レプリカ移行中にPDとのネットワーク接続が不安定になり、 TiFlashがpanicになる可能性がある問題を修正[＃8323](https://github.com/pingcap/tiflash/issues/8323) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)
    -   クエリが遅いためにメモリ使用量が大幅に増加する問題を修正[＃8564](https://github.com/pingcap/tiflash/issues/8564) @ [ジンヘリン](https://github.com/JinheLin)
    -   TiFlashレプリカを削除して再度追加すると、 TiFlash [＃8695](https://github.com/pingcap/tiflash/issues/8695) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)でデータが破損する可能性がある問題を修正しました。
    -   ポイントインタイムリカバリ（PITR）を実行した後、または`FLASHBACK CLUSTER TO`実行した後にTiFlashレプリカデータが誤って削除され、データ異常[＃8777](https://github.com/pingcap/tiflash/issues/8777) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)が発生する可能性がある問題を修正しました。
    -   `ALTER TABLE ... MODIFY COLUMN ... NOT NULL`を実行した後にTiFlash がパニックを起こし、null 許容列が[＃8419](https://github.com/pingcap/tiflash/issues/8419) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)に非 null 許容列に変更される問題を修正しました。
    -   分散storageとコンピューティングアーキテクチャで、ネットワーク分離後にクエリが永久にブロックされる可能性がある問題を修正[＃8806](https://github.com/pingcap/tiflash/issues/8806) @ [ジンヘリン](https://github.com/JinheLin)
    -   分散storageとコンピューティングアーキテクチャで、シャットダウン中にTiFlash がpanicになる可能性がある問題を修正[＃8837](https://github.com/pingcap/tiflash/issues/8837) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)
    -   リモート読み取り[＃8685](https://github.com/pingcap/tiflash/issues/8685) @ [ソロッツ](https://github.com/solotzg)の場合にデータ競合によりTiFlash がクラッシュする可能性がある問題を修正しました
    -   `CAST(AS JSON)`関数が JSON オブジェクト キー[＃8712](https://github.com/pingcap/tiflash/issues/8712) @ [シーライズ](https://github.com/SeaRise)の重複を排除しない問題を修正しました。
    -   チャンクエンコード[＃8674](https://github.com/pingcap/tiflash/issues/8674) @ [いびん87](https://github.com/yibin87)中に`ENUM`列目が原因でTiFlashがクラッシュする可能性がある問題を修正

-   ツール

    -   バックアップと復元 (BR)

        -   リージョンがリーダーになった直後に分割またはマージされると、ログ バックアップ チェックポイントがスタックする問題を修正しました[＃16469](https://github.com/tikv/tikv/issues/16469) @ [ユジュンセン](https://github.com/YuJuncen)
        -   極端なケースでフルバックアップがピアを見つけられなかった場合に TiKV がパニックになる問題を修正[＃16394](https://github.com/tikv/tikv/issues/16394) @ [リーヴルス](https://github.com/Leavrth)
        -   同じノード[＃50445](https://github.com/pingcap/tidb/issues/50445) @ [3ポインター](https://github.com/3pointer)で TiKV IP アドレスを変更した後にログ バックアップが停止する問題を修正しました。
        -   S3 [＃49942](https://github.com/pingcap/tidb/issues/49942) @ [リーヴルス](https://github.com/Leavrth)からファイル コンテンツを読み取っているときにエラーが発生した場合にBR が再試行できない問題を修正しました。
        -   データの復元に失敗した後、チェックポイントから再開するとエラー`the target cluster is not fresh`が発生する問題を修正[＃50232](https://github.com/pingcap/tidb/issues/50232) @ [リーヴルス](https://github.com/Leavrth)
        -   ログバックアップタスクを停止すると TiDB がクラッシュする問題を修正[＃50839](https://github.com/pingcap/tidb/issues/50839) @ [ユジュンセン](https://github.com/YuJuncen)
        -   TiKVノード[＃50566](https://github.com/pingcap/tidb/issues/50566) @ [リーヴルス](https://github.com/Leavrth)にリーダーがいないためにデータの復元が遅くなる問題を修正
        -   `--filter`オプションを指定した後でも、完全な復元を行うにはターゲット クラスターが空である必要があるという問題を修正しました[＃51009](https://github.com/pingcap/tidb/issues/51009) @ [3ポインター](https://github.com/3pointer)

    -   ティCDC

        -   storageシンク[＃10352](https://github.com/pingcap/tiflow/issues/10352) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)の使用時に、storageサービスによって生成されたファイルシーケンス番号が正しく増加しない可能性がある問題を修正しました。
        -   複数の変更フィード[＃10430](https://github.com/pingcap/tiflow/issues/10430) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)を同時に作成すると TiCDC が`ErrChangeFeedAlreadyExists`エラーを返す問題を修正しました
        -   `ignore-event`で`add table partition`イベントをフィルタリングするように構成した後、TiCDC が関連パーティションの他のタイプの DML 変更をダウンストリーム[＃10524](https://github.com/pingcap/tiflow/issues/10524) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)に複製しない問題を修正しました。
        -   アップストリームテーブル[＃10522](https://github.com/pingcap/tiflow/issues/10522) @ [スドジ](https://github.com/sdojjy)で`TRUNCATE PARTITION`が実行された後に、changefeed がエラーを報告する問題を修正しました。
        -   変更フィードを再開するときに`snapshot lost caused by GC`時間内に報告されず、変更フィードの`checkpoint-ts`が TiDB [＃10463](https://github.com/pingcap/tiflow/issues/10463) @ [スドジ](https://github.com/sdojjy)の GC セーフポイントよりも小さい問題を修正しました。
        -   単一行データのデータ整合性検証が有効になっている場合、タイムゾーンの不一致により TiCDC が`TIMESTAMP`種類のチェックサムを検証できない問題を修正[＃10573](https://github.com/pingcap/tiflow/issues/10573) @ [3エースショーハンド](https://github.com/3AceShowHand)
        -   同期ポイントテーブルが誤って複製される可能性がある問題を修正[＃10576](https://github.com/pingcap/tiflow/issues/10576) @ [アズドンメン](https://github.com/asddongmen)
        -   Apache Pulsarをダウンストリームとして使用する場合にOAuth2.0、TLS、mTLSを適切に有効化できない問題を修正[＃10602](https://github.com/pingcap/tiflow/issues/10602) @ [アズドンメン](https://github.com/asddongmen)
        -   TiKV がリーダー[＃10584](https://github.com/pingcap/tiflow/issues/10584) @ [アズドンメン](https://github.com/asddongmen)をアップグレード、再起動、または排除したときに、チェンジフィードがスタックする可能性がある問題を修正しました。
        -   DDL 文が頻繁に実行されるシナリオで、間違った BarrierTS が原因でデータが間違った CSV ファイルに書き込まれる問題を修正[＃10668](https://github.com/pingcap/tiflow/issues/10668) @ [リデズ](https://github.com/lidezhu)
        -   KVクライアントのデータ競合によりTiCDCがpanicを起こす問題を修正[＃10718](https://github.com/pingcap/tiflow/issues/10718) @ [アズドンメン](https://github.com/asddongmen)
        -   テーブルレプリケーションタスク[＃10613](https://github.com/pingcap/tiflow/issues/10613) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)をスケジュールするときに TiCDC がパニックになる問題を修正

    -   TiDB データ移行 (DM)

        -   アップストリームの主キーがバイナリタイプ[＃10672](https://github.com/pingcap/tiflow/issues/10672) @ [GMHDBJD](https://github.com/GMHDBJD)の場合にデータが失われる問題を修正しました

    -   TiDB Lightning

        -   TiKV スペース[＃43636](https://github.com/pingcap/tidb/issues/43636) @ [ランス6716](https://github.com/lance6716)をチェックすることで発生するパフォーマンス低下の問題を修正しました。
        -   ファイルスキャン中に無効なシンボリックリンクファイルに遭遇すると、 TiDB Lightning がエラーを報告する問題を修正[＃49423](https://github.com/pingcap/tidb/issues/49423) @ [ランス6716](https://github.com/lance6716)
        -   `sql_mode` [＃50757](https://github.com/pingcap/tidb/issues/50757) @ [GMHDBJD](https://github.com/GMHDBJD)に`NO_ZERO_IN_DATE`が含まれていない場合、 TiDB Lightning が`0`含む日付値を正しく解析できない問題を修正しました。

## 寄稿者 {#contributors}

TiDB コミュニティの以下の貢献者に感謝いたします。

-   [アオアン](https://github.com/Aoang)
-   [バッファフライ](https://github.com/bufferflies)
-   [デーモン365](https://github.com/daemon365)
-   [エルトシア](https://github.com/eltociear)
-   [リチュンジュ](https://github.com/lichunzhu)
-   [ジフハウス](https://github.com/jiyfhust)
-   [ピンとb](https://github.com/pingandb)
-   [神奇徳宝子](https://github.com/shenqidebaozi)
-   [スミティズ](https://github.com/Smityz)
-   [歌zhibin97](https://github.com/songzhibin97)
-   [タンジンギュ97](https://github.com/tangjingyu97)
-   [テーマ](https://github.com/Tema)
-   [ub-3](https://github.com/ub-3)
-   [ヨシキポム](https://github.com/yoshikipom)
