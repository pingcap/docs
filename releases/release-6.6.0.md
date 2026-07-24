---
title: TiDB 6.6.0 Release Notes
summary: TiDB 6.6.0 の新機能、互換性の変更点、改善点、およびバグ修正についてご確認ください。
---

# TiDB 6.6.0 リリースノート {#tidb-6-6-0-release-notes}

発売日：2023年2月20日

TiDB バージョン: 6.6.0- [DMR](/releases/versioning.md#development-milestone-releases)

> **Note:**
>
> TiDB 6.6.0-DMR ドキュメントは[アーカイブ済み](https://docs-archive.pingcap.com/tidb/v6.6/)です。 PingCAP は、TiDB データベースの[最新のLTSバージョン](https://docs.pingcap.com/tidb/stable)を使用することを推奨します。

クイックアクセス: [クイックスタート](https://docs-archive.pingcap.com/tidb/v6.6/quick-start-with-tidb)

バージョン6.6.0-DMRの主な新機能と改善点は以下のとおりです。

<table><thead><tr><th>カテゴリ</th><th>特徴</th><th>説明</th></tr></thead><tbody><tr><td rowspan="3">拡張性とパフォーマンス<br /></td><td>TiKVは<a href="https://docs-archive.pingcap.com/tidb/v6.6/partitioned-raft-kv" target="_blank">パーティション化されたRaft KVストレージエンジン</a>をサポートしています（実験的）。</td><td> TiKVはパーティション化されたRaft KVストレージエンジンを導入しており、各リージョンは独立したRocksDBインスタンスを使用するため、クラスターのストレージ容量をテラバイトからペタバイトまで容易に拡張でき、より安定した書き込みレイテンシーと強力なスケーラビリティを実現します。</td></tr><tr><td> TiKVは<a href="https://docs-archive.pingcap.com/tidb/v6.6/system-variables#tidb_store_batch_size" target="_blank">データ要求のバッチ集計</a>をサポートしています</td><td>この機能強化により、TiKVのバッチ取得操作におけるRPCの総数が大幅に削減されます。データが高度に分散しており、gRPCスレッドプールのリソースが不足している状況では、コプロセッサ要求をバッチ処理することで、パフォーマンスを50%以上向上させることができます。</td></tr><tr><td> TiFlashは、 <a href="https://docs-archive.pingcap.com/tidb/v6.6/stale-read" target="_blank">ステイル読み取り</a>と<a href="https://docs-archive.pingcap.com/tidb/v6.6/explain-mpp#mpp-version-and-exchange-data-compression" target="_blank">圧縮交換</a>をサポートしています。</td><td> TiFlashは、リアルタイム要件に制約がないシナリオにおいてクエリ性能を向上させることができる、古いデータの読み取り機能をサポートしています。また、 TiFlashはデータ圧縮をサポートしており、並列データ交換の効率を向上させ、TPC-H全体のパフォーマンスを10%向上させ、ネットワーク使用量を50%以上削減できます。</td></tr><tr><td rowspan="2">信頼性と可用性<br /></td><td><a href="https://docs-archive.pingcap.com/tidb/v6.6/tidb-resource-control" target="_blank">リソース制御</a>（実験的）</td><td>リソースグループに基づいたリソース管理をサポートします。これにより、データベースユーザーを対応するリソースグループにマッピングし、実際のニーズに基づいて各リソースグループの割り当て量を設定します。</td></tr><tr><td> <a href="https://docs-archive.pingcap.com/tidb/v6.6/sql-plan-management#create-a-binding-according-to-a-historical-execution-plan" target="_blank">履歴SQLバインディング</a></td><td>TiDB Dashboard上で、過去の実行計画のバインドと、実行計画の迅速なバインドをサポートします。</td></tr><tr><td rowspan="2"> SQLの機能<br /></td><td><a href="https://docs-archive.pingcap.com/tidb/v6.6/foreign-key" target="_blank">外部キー</a>（実験的）</td><td>データの一貫性を維持し、データ品質を向上させるために、MySQL互換の外部キー制約をサポートします。</td></tr><tr><td> <a href="https://docs-archive.pingcap.com/tidb/v6.6/sql-statement-create-index#multi-valued-indexes" target="_blank">多値インデックス</a>（実験的）</td><td> MySQL互換の多値インデックスを導入し、JSON型を拡張することで、TiDBのMySQL 8.0との互換性を向上させます。</td></tr><tr><td> DB操作と可観測性<br /></td><td><a href="https://docs-archive.pingcap.com/tidb/v6.6/dm-precheck#check-items-for-physical-import" target="_blank">DMは物理的なインポートをサポートします</a>（実験的）</td><td> TiDBデータ移行（DM）は、TiDB Lightningの物理インポートモードを統合することで、フルデータ移行のパフォーマンスを向上させ、最大10倍高速化します。</td></tr></tbody></table>

## 機能の詳細 {#feature-details}

### 拡張性 {#scalability}

-   サポートパーティションRaft KVストレージエンジン (実験的) [#11515](https://github.com/tikv/tikv/issues/11515) [#12842](https://github.com/tikv/tikv/issues/12842) @[busyjay](https://github.com/busyjay)@[tonyxuqqi](https://github.com/tonyxuqqi)@ [tabokie](https://github.com/tabokie)@ [bufferflies](https://github.com/bufferflies)[5kb](https://github.com/5kbpers) @[SpadeA-Tang](https://github.com/SpadeA-Tang)@[nolouch](https://github.com/nolouch)

    TiDB v6.6.0 より前は、TiKV の Raft ベースのストレージエンジンは、単一の RocksDB インスタンスを使用して、TiKV インスタンスのすべての「リージョン」のデータを保存していました。より大規模なクラスタをより安定してサポートするために、TiDB v6.6.0 以降では、複数の RocksDB インスタンスを使用して TiKVリージョンデータを保存する新しい TiKVストレージエンジンが導入され、各リージョンのデータは個別の RocksDB インスタンスに独立して保存されます。この新しいエンジンは、RocksDB インスタンス内のファイルの数とレベルをより適切に制御し、リージョン間のデータ操作の物理的な分離を実現し、より多くのデータを安定して管理できます。これは、TiKV がパーティショニングによって複数の RocksDB インスタンスを管理していると考えることができます。そのため、この機能は Partitioned-Raft-KV と呼ばれています。この機能の主な利点は、書き込みパフォーマンスの向上、スケーリングの高速化、および同じハードウェアでサポートできるデータ量の拡大です。また、より大規模なクラスタにも対応できます。

    現在、この機能は実験的であり、本番環境での使用は推奨されません。

    詳細については、[ドキュメント](/partitioned-raft-kv.md)を参照してください。

-   DDL操作のための分散並列実行フレームワークのサポート（実験的） [#37125](https://github.com/pingcap/tidb/issues/37125) @[zimulala](https://github.com/zimulala)

    以前のバージョンでは、TiDB クラスタ全体で 1 つの TiDB インスタンスのみが DDL オーナーとしてスキーマ変更タスクを処理できました。大規模テーブルの DDL 操作の DDL 並行性をさらに向上させるため、TiDB v6.6.0 では、DDL 用の分散並列実行フレームワークが導入されました。これにより、クラスタ内のすべての TiDB インスタンスが同じタスクの`StateWriteReorganization`フェーズを同時に実行して、DDL の実行を高速化できます。この機能はシステム変数[`tidb_ddl_distribute_reorg`](https://docs-archive.pingcap.com/tidb/v6.6/system-variables#tidb_ddl_distribute_reorg-new-in-v660)によって制御され、現在は`Add Index`操作のみでサポートされています。

### パフォーマンス {#performance}

-   悲観的ロック キューの安定したウェイクアップ モデルをサポート [#13298](https://github.com/tikv/tikv/issues/13298) @[MyonKeminta](https://github.com/MyonKeminta)

    アプリケーションで頻繁に単一ポイントの悲観的ロック競合が発生する場合、既存のウェイクアップメカニズムではトランザクションがロックを取得する時間を保証できず、ロングテールレイテンシーが大きくなり、ロック取得タイムアウトが発生することもあります。v6.6.0 以降では、システム変数[`tidb_pessimistic_txn_aggressive_locking`](https://docs-archive.pingcap.com/tidb/v6.6/system-variables#tidb_pessimistic_txn_aggressive_locking-new-in-v660)の値を`ON`に設定することで、悲観的ロック用の安定したウェイクアップ モデルを有効にできます。このウェイクアップ モデルでは、無効なウェイクアップによるリソースの浪費を回避するために、キューのウェイクアップ シーケンスを厳密に制御できます。深刻なロック競合が発生するシナリオでは、この安定したウェイクアップ モデルにより、ロングテールレイテンシーと P99 応答時間を短縮できます。

    テスト結果によると、これによりテールレイテンシーが40～60%削減されることが示されています。

    詳細については、 [ドキュメント](https://docs-archive.pingcap.com/tidb/v6.6/system-variables#tidb_pessimistic_txn_aggressive_locking-new-in-v660)を参照してください。

-   バッチ集計データ要求 [#39361](https://github.com/pingcap/tidb/issues/39361) @[cfzjywxk](https://github.com/cfzjywxk) @[you06](https://github.com/you06)

    TiDB が TiKV にデータ要求を送信すると、TiDB はデータが存在するリージョンに応じて要求を複数のサブタスクにコンパイルし、各サブタスクは単一のリージョンの要求のみを処理します。アクセスするデータが高度に分散している場合、データのサイズが大きくなくても、多くのサブタスクが生成され、結果として多くの RPC 要求が発生し、余分な時間を消費します。v6.6.0 以降、TiDB は同じ TiKV インスタンスに送信されるデータ要求を部分的にマージする機能をサポートしており、サブタスクの数と RPC 要求のオーバーヘッドを削減します。データの分散度が高く、gRPC スレッド プールのリソースが不足している場合、要求をバッチ処理することでパフォーマンスを 50% 以上向上させることができます。

    この機能はデフォルトで有効になっています。システム変数[`tidb_store_batch_size`](/system-variables.md#tidb_store_batch_size)を使用して、リクエストのバッチサイズを設定できます。

-   `LIMIT`条項の制限を解除 [#40219](https://github.com/pingcap/tidb/issues/40219) @[fzzf678](https://github.com/fzzf678)

    バージョン 6.6.0 以降、TiDB プラン キャッシュは`LIMIT`や`LIMIT ?`などの変数を`LIMIT 10, ?`パラメータとして指定した実行プランのキャッシュをサポートします。この機能により、より多くの SQL ステートメントがプラン キャッシュの恩恵を受けられるようになり、実行効率が向上します。現在、セキュリティ上の理由から、TiDB は`?`が 10000 を超えない実行プランのみをキャッシュできます。

    詳細については、[ドキュメント](/sql-prepared-plan-cache.md)を参照してください。

-   TiFlashは圧縮によるデータ交換をサポートします [#6620](https://github.com/pingcap/tiflash/issues/6620) @[solotzg](https://github.com/solotzg)

    TiFlashエンジンは、複数のノードと連携して計算を行うために、異なるノード間でデータを交換する必要があります。交換するデータのサイズが非常に大きい場合、データ交換のパフォーマンスが全体の計算効率に影響を与える可能性があります。v6.6.0では、 TiFlashエンジンに圧縮メカニズムが導入され、必要に応じて交換するデータを圧縮してから交換を実行することで、データ交換の効率が向上しました。

    詳細については、 [ドキュメント](/explain-mpp.md#mpp-version-and-exchange-data-compression)を参照してください。

-   TiFlash は、 ステイル読み取り機能 [#4483](https://github.com/pingcap/tiflash/issues/4483) @[hehechen](https://github.com/hehechen)をサポートしています

    ステイル読み取り機能はv5.1.1以降、一般提供（GA）されており、特定のタイムスタンプまたは指定された時間範囲内の履歴データを読み取ることができます。Stale Readは、ローカルのTiKVレプリカからデータを直接読み取ることで、読み取りレイテンシーを削減し、クエリのパフォーマンスを向上させることができます。v6.6.0より前のTiFlashでは、 ステイル読み取りはサポートされていません。テーブルにTiFlashレプリカが存在する場合でも、 ステイル読み取りはTiKVレプリカのみを読み取ることができます。

    バージョン6.6.0以降、 TiFlashはステイル読み取り機能をサポートしています。[`AS OF TIMESTAMP`](/as-of-timestamp.md)構文または[`tidb_read_staleness`](/tidb-read-staleness.md)システム変数を使用してテーブルの履歴データをクエリする場合、テーブルにTiFlashレプリカが存在すると、オプティマイザは対応するデータをTiFlashレプリカから読み込むことを選択できるようになり、クエリのパフォーマンスがさらに向上します。

    詳細については、[ドキュメント](/stale-read.md)を参照してください。

-   TiFlashに`regexp_replace`文字列関数をプッシュダウンする機能のサポート [#6115](https://github.com/pingcap/tiflash/issues/6115) @[xzhangxian1008](https://github.com/xzhangxian1008)

### 信頼性 {#reliability}

-   リソース グループに基づくリソース制御のサポート (実験的) [#38825](https://github.com/pingcap/tidb/issues/38825) @[nolouch](https://github.com/nolouch)@[BornChanger](https://github.com/BornChanger)@ [glorv](https://github.com/glorv)@[tiancaiamao](https://github.com/tiancaiamao)@[Connor1996](https://github.com/Connor1996) @[JmPotato](https://github.com/JmPotato) @[hnes](https://github.com/hnes) @[CabinfeverB](https://github.com/CabinfeverB) @[HuSharp](https://github.com/HuSharp)

    TiDBクラスタのリソースグループを作成し、異なるデータベースユーザーを対応するリソースグループにバインドし、実際のニーズに応じて各リソースグループのクォータを設定できるようになりました。クラスタのリソースが制限されている場合、同じリソースグループ内のセッションで使用されるすべてのリソースはクォータに制限されます。このようにして、リソースグループが過剰に消費された場合でも、他のリソースグループのセッションには影響しません。TiDBは、Grafanaダッシュボード上でリソースの実際の使用状況を表示する組み込みビューを提供し、リソースをより合理的に割り当てるのに役立ちます。

    リソース制御機能の導入は、TiDBにとって画期的な出来事です。この機能により、分散データベースクラスタを複数の論理ユニットに分割できます。たとえ個々のユニットがリソースを過剰に使用したとしても、他のユニットが必要とするリソースを圧迫することはありません。

    この機能を使うと、次のことができます。

    -   異なるシステムに存在する複数の中小規模アプリケーションを単一のTiDBクラスタに統合します。アプリケーションのワークロードが増加しても、他のアプリケーションの正常な動作には影響しません。システムワークロードが低い場合、ビジー状態のアプリケーションは、設定された読み取り/書き込みクォータを超えても必要なシステムリソースを割り当てられるため、リソースを最大限に活用できます。
    -   すべてのテスト環境を単一のTiDBクラスタに統合するか、より多くのリソースを消費するバッチタスクを単一のリソースグループにまとめるかを選択できます。これにより、ハードウェア利用率を向上させ、運用コストを削減しながら、重要なアプリケーションが常に必要なリソースを確保できるようになります。

    さらに、リソース制御機能を合理的に活用することで、クラスタ数を削減し、運用・保守の難易度を下げ、管理コストを削減することができます。

    v6.6 では、リソース制御を有効にするには、TiDB のグローバル変数[`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-new-in-v660)と TiKV 設定項目[`resource-control.enabled`](/tikv-configuration-file.md#resource-control)両方を有効にする必要があります。現在サポートされているクォータ方式は「 [リクエストユニット（RU）](/tidb-resource-control-ru-groups.md#what-is-request-unit-ru) 」に基づいています。RU は、CPU や IO などのシステム リソースに対する TiDB の統一抽象化ユニットです。

    詳細については、[ドキュメント](/tidb-resource-control-ru-groups.md)を参照してください。

-   過去の実行計画を拘束することは、GA [#39199](https://github.com/pingcap/tidb/issues/39199) @[fzzf678](https://github.com/fzzf678)です。

    バージョン6.5.0では、TiDBは[`CREATE [GLOBAL | SESSION] BINDING`](/sql-statements/sql-statement-create-binding.md)文のバインディングターゲットを拡張し、過去の実行プランに基づいてバインディングを作成する機能をサポートしています。バージョン6.6.0では、この機能は一般提供（GA）となります。実行プランの選択は、現在のTiDBノードに限定されません。任意のTiDBノードによって生成された過去の実行プランを[SQLバインディング](/sql-statements/sql-statement-create-binding.md)のターゲットとして選択できるため、機能の使いやすさがさらに向上します。

    詳細については、 [ドキュメント](/sql-plan-management.md#create-a-binding-according-to-a-historical-execution-plan)を参照してください。

-   いくつかのオプティマイザー ヒントを追加 [#39964](https://github.com/pingcap/tidb/issues/39964) @[Reminiscent](https://github.com/Reminiscent)

    TiDB は v6.6.0 で`LIMIT`操作の実行プランの選択を制御するためのオプティマイザヒントをいくつか追加しました。

    -   [`ORDER_INDEX()`](/optimizer-hints.md#order_indext1_name-idx1_name--idx2_name-) : オプティマイザに指定されたインデックスを使用するように指示し、データの読み取り時にインデックスの順序を維持し、 `Limit + IndexScan(keep order: true)`に似たプランを生成します。
    -   [`NO_ORDER_INDEX()`](/optimizer-hints.md#no_order_indext1_name-idx1_name--idx2_name-) : オプティマイザに指定されたインデックスを使用するように指示し、データの読み取り時にインデックスの順序を保持せず、 `TopN + IndexScan(keep order: false)`に似たプランを生成します。

    オプティマイザヒントを継続的に導入することで、ユーザーはより多くの介入方法を利用できるようになり、SQLのパフォーマンス問題の解決に役立ち、全体的なパフォーマンスの安定性が向上します。

-   DDL操作のリソース使用量を動的に管理するサポート（実験的） [#38025](https://github.com/pingcap/tidb/issues/38025) @[hawkingrei](https://github.com/hawkingrei)

    TiDB v6.6.0 では、DDL 操作のリソース管理が導入されており、これらの操作の CPU 使用率を自動的に制御することで、オンライン アプリケーションに対する DDL 変更の影響を軽減します。この機能は[DDL分散並列実行フレームワーク](https://docs-archive.pingcap.com/tidb/v6.6/system-variables#tidb_ddl_distribute_reorg-new-in-v660)が有効になった後にのみ有効です。

### 可用性 {#availability}

-   [SQLにおける配置ルール](/placement-rules-in-sql.md) [#38605](https://github.com/pingcap/tidb/issues/38605) @[nolouch](https://github.com/nolouch)の`SURVIVAL_PREFERENCE`の構成のサポート

    `SURVIVAL_PREFERENCES` 、データの災害時における耐障害性を高めるためのデータ耐障害性設定を提供します。 `SURVIVAL_PREFERENCE`を指定することで、以下の項目を制御できます。

    -   クラウドリージョンをまたいでデプロイされたTiDBクラスタの場合、あるクラウドリージョンで障害が発生しても、指定されたデータベースまたはテーブルは別のクラウドリージョンで存続できます。
    -   単一のクラウドリージョンにデプロイされたTiDBクラスタの場合、可用性ゾーンに障害が発生した場合でも、指定されたデータベースまたはテーブルは別の可用性ゾーンで存続できます。

    詳細については、 [ドキュメント](/placement-rules-in-sql.md#specify-survival-preferences)を参照してください。

-   `FLASHBACK CLUSTER TO TIMESTAMP`ステートメントによる DDL 操作のロールバックのサポート [#14045](https://github.com/tikv/tikv/issues/14045) @[Defined2014](https://github.com/Defined2014) @[JmPotato](https://github.com/JmPotato)

    [`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-cluster.md)ステートメントは、ガベージ コレクション (GC) の有効期間内の指定された時点にクラスタ全体を復元することをサポートします。TiDB v6.6.0 では、この機能に DDL 操作のロールバック機能が追加されました。これにより、クラスタ上で発生した DML または DDL 操作の誤りを迅速に取り消したり、クラスタを数分以内にロールバックしたり、タイムライン上でクラスタを複数回ロールバックして特定のデータ変更が発生したタイミングを特定したりすることができます。

    詳細については、 [ドキュメント](/sql-statements/sql-statement-flashback-cluster.md)を参照してください。

### SQL {#sql}

-   MySQL互換の外部キー制約をサポート（実験的） [#18209](https://github.com/pingcap/tidb/issues/18209) @[crazycs520](https://github.com/crazycs520)

    TiDB v6.6.0では、MySQLと互換性のある外部キー制約機能が導入されました。この機能は、テーブル内またはテーブル間の参照、制約の検証、およびカスケード操作をサポートします。この機能は、アプリケーションのTiDBへの移行、データの一貫性の維持、データ品質の向上、およびデータモデリングの容易化に役立ちます。

    詳細については、[ドキュメント](/foreign-key.md)を参照してください。

-   MySQL互換の多値インデックスのサポート（実験的） [#39592](https://github.com/pingcap/tidb/issues/39592) @[xiongjiwei](https://github.com/xiongjiwei)@[qw4990](https://github.com/qw4990)

    TiDB は v6.6.0 で MySQL 互換の多値インデックスを導入しました。JSON 列の配列の値をフィルタリングすることは一般的な操作ですが、通常のインデックスではこの操作を高速化することはできません。配列に多値インデックスを作成することで、フィルタリングのパフォーマンスを大幅に向上させることができます。JSON 列の配列に多値インデックスがある場合、その多値インデックスを使用して`MEMBER OF()` 、 `JSON_CONTAINS()` 、 `JSON_OVERLAPS()`関数で取得条件をフィルタリングすることで、I/O 消費を大幅に削減し、操作速度を向上させることができます。

    多値インデックスの導入により、TiDBのJSONデータ型に対するサポートがさらに強化され、MySQL 8.0との互換性も向上します。

    詳細については、 [ドキュメント](/sql-statements/sql-statement-create-index.md#multi-valued-indexes)を参照してください。

### データベース操作 {#db-operations}

-   リソースを大量に消費するタスク向けに読み取り専用ストレージノードを構成する機能をサポート @[v01dstar](https://github.com/v01dstar)

    本番環境では、バックアップや大規模なデータ読み取りと分析など、読み取り専用操作が定期的に大量のリソースを消費し、クラスタ全体のパフォーマンスに影響を与える場合があります。TiDB v6.6.0 では、リソースを消費する読み取り専用タスク用に読み取り専用ストレージノードを構成して、オンライン アプリケーションへの影響を軽減できます。現在、TiDB、TiSpark、およびBR は、読み取り専用ストレージノードからのデータ読み取りをサポートしています。 [手順](/best-practices/readonly-nodes.md#procedures)のパフォーマンスの安定性を確保するため、システム変数`tidb_replica_read` 、TiSpark 構成項目`spark.tispark.replica_read` 、または br コマンドstorage引数`--replica-read-label` 、読み取り先を指定して、読み取り専用ストレージ ノードを次のように構成できます。

    詳細については、[ドキュメント](/best-practices/readonly-nodes.md)を参照してください。

-   `store-io-pool-size`の動的な変更をサポート [#13964](https://github.com/tikv/tikv/issues/13964) @[LykxSassinator](https://github.com/LykxSassinator)

    TiKV の設定項目[`raftstore.store-io-pool-size`](/tikv-configuration-file.md#store-io-pool-size-new-in-v530) 、 Raft I/O タスクを処理するスレッドの許容数を指定します。この値は、TiKV のパフォーマンスをチューニングする際に調整できます。バージョン 6.6.0 より前のバージョンでは、この設定項目を動的に変更することはできませんでした。バージョン 6.6.0 以降では、サーバーを再起動せずにこの設定を変更できるため、より柔軟なパフォーマンス調整が可能になります。

    詳細については、[ドキュメント](/dynamic-config.md)を参照してください。

-   TiDBクラスタ初期化時に実行されるSQLスクリプトの指定をサポートする [#35624](https://github.com/pingcap/tidb/issues/35624) @[morgo](https://github.com/morgo)

    TiDB クラスタを初めて起動する際に、コマンドライン パラメータ`--initialize-sql-file`を設定することで、実行する SQL スクリプトを指定できます。この機能は、システム変数の値の変更、ユーザーの作成、権限の付与などの操作を実行する必要がある場合に使用できます。

    詳細については、 [ドキュメント](/tidb-configuration-file.md#initialize-sql-file-new-in-v660)を参照してください。

-   TiDB Data Migration (DM)は、TiDB Lightningの物理インポートモードと統合され、完全移行のパフォーマンスを最大10倍向上させます（実験的）@[lance6716](https://github.com/lance6716)

    バージョン6.6.0では、DMの完全移行機能がTiDB Lightningの物理インポートモードと統合され、DMによる完全データ移行のパフォーマンスが最大10倍向上し、大容量データシナリオにおける移行時間を大幅に短縮できるようになりました。

    バージョン6.6.0より前は、大容量データの場合、高速なフルデータ移行のためにTiDB Lightningで物理インポートタスクを個別に設定し、その後DMを使用して増分データ移行を行う必要があり、複雑な設定が必要でした。バージョン6.6.0以降では、 TiDB Lightningタスクを設定することなく大容量データを移行できます。1つのDMタスクで移行を完了できます。

    詳細については、 [ドキュメント](/dm/dm-precheck.md#check-items-for-physical-import)を参照してください。

-   TiDB Lightning は、ソース ファイルとターゲット テーブル間の列名の不一致の問題に対処するため、新しい構成パラメータ`"header-schema-match"`を追加しました。@[dsdashun](https://github.com/dsdashun)

    TiDB Lightning v6.6.0では、新しいプロファイルパラメータ`"header-schema-match"`が追加されました。デフォルト値は`true`で、これはソースCSVファイルの最初の行が列名として扱われ、ターゲットテーブルの列名と一致することを意味します。CSVテーブルヘッダーのフィールド名がターゲットテーブルの列名と一致しない場合は、この設定を`false`に設定できます。TiDB Lightningはエラーを無視し、ターゲットテーブルの列の順序でデータのインポートを続行します。

    詳細については、 [ドキュメント](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)を参照してください。

-   TiDB Lightning は、キーと値のペアを TiKV に送信する際の圧縮転送の有効化をサポートします [#41163](https://github.com/pingcap/tidb/issues/41163) @[sleepymole](https://github.com/sleepymole)

    バージョン6.6.0以降、 TiDB Lightningは、ローカルでエンコードおよびソートされたキーと値のペアをTiKVに送信する際に圧縮してネットワーク転送する機能をサポートしており、ネットワーク経由で転送されるデータ量を削減し、ネットワーク帯域幅のオーバーヘッドを低減します。この機能がサポートされる以前のTiDBバージョンでは、 TiDB Lightningは比較的高いネットワーク帯域幅を必要とし、データ量が多い場合には高額なトラフィック料金が発生していました。

    この機能はデフォルトでは無効になっています。有効にするには、 TiDB Lightningの構成項目`compress-kv-pairs`を`"gzip"`または`"gz"`に設定してください。

    詳細については、 [ドキュメント](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)を参照してください。

-   TiKV-CDC ツールは現在 GA であり、RawKV [#48](https://github.com/tikv/migration/issues/48) @[zeminzhou](https://github.com/zeminzhou)@[haojinming](https://github.com/haojinming)@ [pingyu](https://github.com/pingyu)データ変更のサブスクライブをサポートしています。

    TiKV-CDCは、TiKVクラスタ用のCDC（変更データキャプチャ）ツールです。TiKVとPDは、TiDBを使用しない場合、RawKVと呼ばれるKVデータベースを構成できます。TiKV-CDCは、RawKVのデータ変更を購読し、それを下流のTiKVクラスタにリアルタイムで複製することをサポートしており、RawKVのクラスタ間レプリケーションを可能にします。

    詳細については、 [ドキュメント](https://tikv.org/docs/latest/concepts/explore-tikv-features/cdc/cdc/)を参照してください。

-   TiCDC は、Kafka チェンジフィード上の単一テーブルのスケールアウトと複数の TiCDC ノードへのチェンジフィードの分散をサポートします (実験的) [#7720](https://github.com/pingcap/tiflow/issues/7720) @[overvenus](https://github.com/overvenus)

    v6.6.0より前は、アップストリームのテーブルが大量の書き込みを受け入れると、そのテーブルのレプリケーション機能をスケールアウトできず、レプリケーションのレイテンシーが増加していました。TiCDC v6.6.0以降では、アップストリームテーブルの変更フィードをKafkaシンク内の複数のTiCDCノードに分散できるため、単一テーブルのレプリケーション機能をスケールアウトできます。

    詳細については、 [ドキュメント](/ticdc/ticdc-sink-to-kafka.md#scale-out-the-load-of-a-single-large-table-to-multiple-ticdc-nodes)を参照してください。

-   [GORM](https://github.com/go-gorm/gorm)TiDB 統合テストを追加します。現在、TiDB は GORM によってサポートされるデフォルトのデータベースです。 [#6014](https://github.com/go-gorm/gorm/pull/6014) @[Icemap](https://github.com/Icemap)

    -   v1.4.6 では、 [GORM MySQL ドライバー](https://github.com/go-gorm/mysql)TiDB [#104](https://github.com/go-gorm/mysql/pull/104)の`AUTO_RANDOM`属性に適応します
    -   v1.4.6 では、 [GORM MySQL ドライバー](https://github.com/go-gorm/mysql)は、TiDB に接続する際に、 `Unique`フィールドの`Unique`属性が`AutoMigrate`中に変更できない問題を修正しました。 [#105](https://github.com/go-gorm/mysql/pull/105)
    -   [GORMドキュメント](https://github.com/go-gorm/gorm.io)TiDB をデフォルトのデータベースとして言及しています [#638](https://github.com/go-gorm/gorm.io/pull/638)

    詳細については、 [GORMドキュメント](https://gorm.io/docs/index.html)を参照してください。

### 可観測性 {#observability}

-   TiDB DashboardでSQLバインディングを素早く作成するサポート [#781](https://github.com/pingcap/tidb-dashboard/issues/781) @[YiniXu9506](https://github.com/YiniXu9506)

    TiDB v6.6.0では、ステートメント履歴からSQLバインディングを作成する機能がサポートされており、TiDB Dashboard上でSQLステートメントを特定の実行プランにすばやくバインドできます。

    この機能は、ユーザーフレンドリーなインターフェースを提供することで、TiDBにおけるプランのバインディングプロセスを簡素化し、操作の複雑さを軽減し、プランバインディングプロセスの効率とユーザーエクスペリエンスを向上させます。

    詳細については、 [ドキュメント](/dashboard/dashboard-statement-details.md#fast-plan-binding)を参照してください。

-   実行プランのキャッシュに関する警告を追加 @[qw4990](https://github.com/qw4990)

    実行プランをキャッシュできない場合、TiDB は診断を容易にするために警告でその理由を示します。例:

    ```sql
    mysql> PREPARE st FROM 'SELECT * FROM t WHERE a<?';
    Query OK, 0 rows affected (0.00 sec)

    mysql> SET @a='1';
    Query OK, 0 rows affected (0.00 sec)

    mysql> EXECUTE st USING @a;
    Empty set, 1 warning (0.01 sec)

    mysql> SHOW WARNINGS;
    +---------+------+----------------------------------------------+
    | Level   | Code | Message                                      |
    +---------+------+----------------------------------------------+
    | Warning | 1105 | skip plan-cache: '1' may be converted to INT |
    +---------+------+----------------------------------------------+
    ```

    前述の例では、オプティマイザが非INT型をINT型に変換し、パラメータの変更に伴って実行プランが変わる可能性があるため、TiDBはプランをキャッシュしません。

    詳細については、 [ドキュメント](/sql-prepared-plan-cache.md#diagnostics-of-prepared-plan-cache)を参照してください。

-   `Warnings`フィールドをスロークエリログに追加します [#39893](https://github.com/pingcap/tidb/issues/39893) @[time-and-fate](https://github.com/time-and-fate)

    TiDB v6.6.0 では、パフォーマンスの問題を診断しやすくするために、スロークエリログに`Warnings`フィールドが追加されました。このフィールドには、スロークエリの実行中に生成された警告が記録されます。これらの警告は、TiDB Dashboardのスロークエリページでも確認できます。

    詳細については、[ドキュメント](/identify-slow-queries.md)を参照してください。

-   SQL実行プランの生成を自動的にキャプチャする [#38779](https://github.com/pingcap/tidb/issues/38779) @[Yisaer](https://github.com/Yisaer)

    実行計画の問題をトラブルシューティングする過程で、 `PLAN REPLAYER`現場を保存し、診断の効率を向上させるのに役立ちます。しかし、シナリオによっては、一部の実行計画の生成を自由に再現できないため、診断作業がより困難になります。

    このような問題に対処するため、TiDB v6.6.0 では`PLAN REPLAYER`により自動キャプチャ機能が拡張されました。 `PLAN REPLAYER CAPTURE`コマンドを使用すると、対象の SQL ステートメントを事前に登録し、同時に対象の実行プランを指定できます。TiDB は、登録された対象に一致する SQL ステートメントまたは実行プランを検出すると、 `PLAN REPLAYER`情報を自動的に生成してパッケージ化します。実行プランが不安定な場合、この機能により診断効率が向上します。

    この機能を使用するには、 [`tidb_enable_plan_replayer_capture`](/system-variables.md#tidb_enable_plan_replayer_capture)の値を`ON`に設定してください。

    詳細については、 [ドキュメント](/sql-plan-replayer.md#use-plan-replayer-capture)を参照してください。

-   永続化ステートメントのサポート概要（実験的） [#40812](https://github.com/pingcap/tidb/issues/40812) @[mornyx](https://github.com/mornyx)

    バージョン6.6.0より前は、ステートメントサマリーデータはメモリに保持されていたため、TiDBサーバーの再起動時に失われていました。バージョン6.6.0以降、TiDBはステートメントサマリーの永続化をサポートするようになり、履歴データを定期的にディスクに書き込むことが可能になりました。これにより、システムテーブルに対するクエリの結果は、メモリではなくディスクから取得されます。TiDBの再起動後も、すべての履歴データは保持されます。

    詳細については、 [ドキュメント](/statement-summary-tables.md#persist-statements-summary)を参照してください。

### セキュリティ {#security}

-   TiFlashはTLS証明書の自動ローテーションをサポートします [#5503](https://github.com/pingcap/tiflash/issues/5503) @[ywqzzy](https://github.com/ywqzzy)

    バージョン6.6.0では、TiDBはTiFlash TLS証明書の自動ローテーションをサポートしています。コンポーネント間で暗号化されたデータ転送が有効になっているTiDBクラスタでは、 TiFlashのTLS証明書の有効期限が切れて新しい証明書に再発行する必要が生じた場合、TiDBクラスタを再起動することなく、新しいTiFlash TLS証明書を自動的にロードできます。さらに、TiDBクラスタ内のコンポーネント間でTLS証明書をローテーションしても、TiDBクラスタの使用には影響しないため、クラスタの高い可用性が確保されます。

    詳細については、[ドキュメント](/enable-tls-between-components.md)を参照してください。

-   TiDB LightningはAWS IAMロールキーとセッショントークンを介してAmazon S3データへのアクセスをサポートします [#40750](https://github.com/pingcap/tidb/issues/40750) @[okJiang](https://github.com/okJiang)

    バージョン6.6.0より前は、 TiDB LightningはAWS IAM**ユーザーのアクセスキー**（各アクセスキーはアクセスキーIDとシークレットアクセスキーで構成されます）によるS3データへのアクセスのみをサポートしていたため、一時的なセッショントークンを使用してS3データにアクセスすることはできませんでした。バージョン6.6.0以降では、データセキュリティを向上させるため、 TiDB LightningはAWS IAM**ロールのアクセスキーとセッショントークン**によるS3データへのアクセスもサポートするようになりました。

    詳細については、 [ドキュメント](/tidb-lightning/tidb-lightning-data-source.md#import-data-from-amazon-s3)を参照してください。

### テレメトリー {#telemetry}

-   2023 年 2 月 20 日以降、TiDB および TiDB Dashboard (v6.6.0 を含む) の新しいバージョンでは[テレメトリ機能](/telemetry.md)デフォルトで無効になります。デフォルトのテレメトリ構成を使用する以前のバージョンからアップグレードする場合、アップグレード後にテレメトリ機能は無効になります。特定のバージョンについては、 [TiDBのリリーススケジュール](/releases/release-timeline.md)を参照してください。
-   バージョン1.11.3以降、新規にデプロイされたTiUPでは、テレメトリ機能はデフォルトで無効になっています。以前のバージョンのTiUPからバージョン1.11.3以降にアップグレードした場合、テレメトリ機能はアップグレード前と同じ状態を維持します。

## 互換性の変更 {#compatibility-changes}

> **Note:**
>
> このセクションでは、バージョン6.5.0から最新バージョン（6.6.0）にアップグレードする際に知っておくべき互換性の変更点について説明します。バージョン6.4.0以前のバージョンから最新バージョンにアップグレードする場合は、中間バージョンで導入された互換性の変更点も確認する必要があるかもしれません。

### MySQLとの互換性 {#mysql-compatibility}

-   MySQL互換の外部キー制約をサポート（実験的） [#18209](https://github.com/pingcap/tidb/issues/18209) @[crazycs520](https://github.com/crazycs520)

    詳細については、このドキュメントおよび[ドキュメント](/foreign-key.md)の[SQL](#sql)セクションを参照してください。

-   MySQL互換の多値インデックスのサポート（実験的） [#39592](https://github.com/pingcap/tidb/issues/39592) @[xiongjiwei](https://github.com/xiongjiwei)@[qw4990](https://github.com/qw4990)

    詳細については、このドキュメントおよび[ドキュメント](/sql-statements/sql-statement-create-index.md#multi-valued-indexes)の[SQL](#sql)セクションを参照してください。

### システム変数 {#system-variables}

| 変数名                                                                                                                                                          | 変更の種類  | 説明                                                                                                                                                                                                                                                           |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `tidb_enable_amend_pessimistic_txn`                                                                                                                          | 削除済み     | バージョン6.5.0以降、この変数は非推奨です。バージョン6.6.0以降、この変数と`AMEND TRANSACTION`機能は削除されます。TiDBは[メタロック](/metadata-lock.md)を使用して`Information schema is changed`エラーを回避します。                                                                                                         |
| `tidb_enable_concurrent_ddl`                                                                                                                                 | 削除済み     | この変数は、TiDB が同時 DDL ステートメントを使用することを許可するかどうかを制御します。この変数が無効になっている場合、TiDB は古い DDL 実行フレームワークを使用します。このフレームワークは、同時 DDL 実行を限定的にサポートします。バージョン 6.6.0 以降、この変数は削除され、TiDB は古い DDL 実行フレームワークをサポートしなくなりました。                                                                 |
| `tidb_ttl_job_run_interval`                                                                                                                                  | 削除済み     | この変数は、バックグラウンドでの TTL ジョブのスケジュール間隔を制御するために使用されます。v6.6.0 以降、この変数は削除されました。TiDB は、 `TTL_JOB_INTERVAL`よりも柔軟な、TTL ランタイムを制御するための`tidb_ttl_job_run_interval`属性をすべてのテーブルに提供しているためです。                                                                                  |
| [`foreign_key_checks`](/system-variables.md#foreign_key_checks)                                                                                              | 変更     | この変数は、外部キー制約チェックを有効にするかどうかを制御します。デフォルト値は`OFF`から`ON`に変更され、これはデフォルトで外部キーチェックが有効になることを意味します。                                                                                                                                                                    |
| [`tidb_enable_foreign_key`](/system-variables.md#tidb_enable_foreign_key-new-in-v630)                                                                        | 変更     | この変数は、外部キー機能を有効にするかどうかを制御します。デフォルト値は`OFF`から`ON`に変更され、これはデフォルトで外部キーが有効になることを意味します。                                                                                                                                                                            |
| `tidb_enable_general_plan_cache`                                                                                                                             | 変更     | この変数は、一般プランキャッシュを有効にするかどうかを制御します。v6.6.0以降、この変数は[`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache)に名前が変更されました。                                                                                                 |
| [`tidb_enable_historical_stats`](/system-variables.md#tidb_enable_historical_stats)                                                                          | 変更     | この変数は、履歴統計を有効にするかどうかを制御します。デフォルト値は`OFF`から`ON`に変更され、履歴統計がデフォルトで有効になります。                                                                                                                                                                                       |
| [`tidb_enable_plan_replayer_capture`](/system-variables.md#tidb_enable_plan_replayer_capture)                                                                | 変更     | この変数はv6.6.0から有効になり、 [`PLAN REPLAYER CAPTURE`機能](/sql-plan-replayer.md#use-plan-replayer-capture-to-capture-target-plans)を有効にするかどうかを制御します。デフォルト値は`OFF`から`ON`に変更され、 `PLAN REPLAYER CAPTURE`機能がデフォルトで有効になります。                                                   |
| [`tidb_enable_telemetry`](/system-variables.md#tidb_enable_telemetry-new-in-v402)                                                                            | 変更     | デフォルト値が`ON`から`OFF`に変更されます。これは、TiDB でテレメトリがデフォルトで無効になっていることを意味します。                                                                                                                                                                                            |
| `tidb_general_plan_cache_size`                                                                                                                               | 変更     | この変数は、General Plan Cache によってキャッシュできる実行プランの最大数を制御します。v6.6.0 以降、この変数は[`tidb_non_prepared_plan_cache_size`](/system-variables.md#tidb_non_prepared_plan_cache_size)に名前が変更されました。                                                                                |
| [`tidb_replica_read`](/system-variables.md#tidb_replica_read-new-in-v40)                                                                                     | 変更     | この変数に新しい値オプション`learner`が追加され、TiDB が読み取り専用ノードからデータを読み取る際に使用するラーナーレプリカを指定できます。                                                                                                                                                                                  |
| [`tidb_replica_read`](/system-variables.md#tidb_replica_read-new-in-v40)                                                                                     | 変更     | TiDBクラスタの読み取り可用性を向上させるため、この変数に新しい値オプション`prefer-leader`が追加されました。このオプションを設定すると、TiDBはリーダーレプリカからの読み取りを優先します。リーダーレプリカのパフォーマンスが著しく低下した場合、TiDBは自動的にフォロワーレプリカからの読み取りに切り替わります。                                                                                        |
| [`tidb_store_batch_size`](/system-variables.md#tidb_store_batch_size)                                                                                        | 変更     | この変数は`IndexLookUp`オペレータのコプロセッサータスクのバッチ サイズを制御します。 `0`バッチを無効にすることを意味します。v6.6.0 以降、デフォルト値は`0`から`4`に変更され、リクエストのバッチごとに 4 つのコプロセッサータスクが 1 つのタスクにまとめられます。                                                                                                          |
| [`mpp_exchange_compression_mode`](/system-variables.md#mpp_exchange_compression_mode-new-in-v660)                                                            | 新しく追加された | この変数は、MPP Exchange オペレータのデータ圧縮モードを指定します。この変数は、TiDB がバージョン番号`1`の MPP 実行プランを選択した場合に有効になります。デフォルト値`UNSPECIFIED`は、TiDB が自動的に`FAST`圧縮モードを選択することを意味します。                                                                                                            |
| [`mpp_version`](/system-variables.md#mpp_version-new-in-v660)                                                                                                | 新しく追加された | この変数は、MPP実行プランのバージョンを指定します。バージョンを指定すると、TiDBは指定されたバージョンのMPP実行プランを選択します。デフォルト値`UNSPECIFIED` 、TiDBが最新バージョン`1`自動的に選択することを意味します。                                                                                                                                  |
| [`tidb_ddl_distribute_reorg`](https://docs-archive.pingcap.com/tidb/v6.6/system-variables#tidb_ddl_distribute_reorg-new-in-v660)                             | 新しく追加された | この変数は、DDL 再編成フェーズの分散実行を有効にしてこのフェーズを高速化するかどうかを制御します。デフォルト値`OFF`は、デフォルトでは DDL 再編成フェーズの分散実行を有効にしないことを意味します。現在、この変数は`ADD INDEX`に対してのみ有効です。                                                                                                                       |
| [`tidb_enable_historical_stats_for_capture`](/system-variables.md#tidb_enable_historical_stats_for_capture)                                                  | 新しく追加された | この変数は`PLAN REPLAYER CAPTURE`で取得される情報に、デフォルトで履歴統計が含まれるかどうかを制御します。デフォルト値の`OFF`は、デフォルトでは履歴統計が含まれないことを意味します。                                                                                                                                                     |
| [`tidb_enable_plan_cache_for_param_limit`](/system-variables.md#tidb_enable_plan_cache_for_param_limit-new-in-v660)                                          | 新しく追加された | この変数は`COUNT` `Limit` 0-PLACEHOLDER-E}} が含まれる実行プランをプリペアドプランキャッシュがキャッシュするかどうかを制御します。デフォルト値は`ON`で、これはプリペアドプランキャッシュ がそのような実行プランのキャッシュをサポートすることを意味します。ただし、 プリペアドプランキャッシュ は、 10000 を超える数値をカウントする`COUNT`条件を含む実行プランのキャッシュをサポートしていないことに注意してください。                      |
| [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-new-in-v660)                                                              | 新しく追加された | この変数は、リソース制御機能を有効にするかどうかを制御します。デフォルト値は`OFF`です。この変数を`ON`に設定すると、TiDB クラスタはリソース グループに基づいたアプリケーションのリソース分離をサポートします。                                                                                                                                               |
| [`tidb_historical_stats_duration`](/system-variables.md#tidb_historical_stats_duration-new-in-v660)                                                          | 新しく追加された | この変数は、過去の統計情報をストレージに保存する期間を制御します。デフォルト値は7日間です。                                                                                                                                                                                                             |
| [`tidb_index_join_double_read_penalty_cost_rate`](/system-variables.md#tidb_index_join_double_read_penalty_cost_rate-new-in-v660)                            | 新しく追加された | この変数は、インデックス結合の選択にペナルティコストを追加するかどうかを制御します。デフォルト値`0`は、この機能がデフォルトで無効になっていることを意味します。                                                                                                                                                                            |
| [`tidb_pessimistic_txn_aggressive_locking`](https://docs-archive.pingcap.com/tidb/v6.6/system-variables#tidb_pessimistic_txn_aggressive_locking-new-in-v660) | 新しく追加された | この変数は、悲観的トランザクションに対して拡張悲観的ロックウェイクアップモデルを使用するかどうかを制御します。デフォルト値`OFF`は、デフォルトでは悲観的トランザクションに対してこのようなウェイクアップモデルを使用しないことを意味します。                                                                                                                                     |
| [`tidb_stmt_summary_enable_persistent`](/system-variables.md#tidb_stmt_summary_enable_persistent-new-in-v660)                                                | 新しく追加された | この変数は読み取り専用です。 [ステートメントの要約持続性](/statement-summary-tables.md#persist-statements-summary)を有効にするかどうかを制御します。この変数の値は、構成項目[`tidb_stmt_summary_enable_persistent`](/tidb-configuration-file.md#tidb_stmt_summary_enable_persistent-new-in-v660)の値と同じです。             |
| [`tidb_stmt_summary_filename`](/system-variables.md#tidb_stmt_summary_filename-new-in-v660)                                                                  | 新しく追加された | この変数は読み取り専用です。 [ステートメントの要約持続性](/statement-summary-tables.md#persist-statements-summary)が有効な場合に永続データが書き込まれるファイルを指定します。この変数の値は、構成項目[`tidb_stmt_summary_filename`](/tidb-configuration-file.md#tidb_stmt_summary_filename-new-in-v660)の値と同じです。                  |
| [`tidb_stmt_summary_file_max_backups`](/system-variables.md#tidb_stmt_summary_file_max_backups-new-in-v660)                                                  | 新しく追加された | この変数は読み取り専用です。 [ステートメントの要約持続性](/statement-summary-tables.md#persist-statements-summary)が有効な場合に保存できるデータ ファイルの最大数を指定します。この変数の値は、構成項目[`tidb_stmt_summary_file_max_backups`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_backups-new-in-v660)の値と同じです。 |
| [`tidb_stmt_summary_file_max_days`](/system-variables.md#tidb_stmt_summary_file_max_days-new-in-v660)                                                        | 新しく追加された | この変数は読み取り専用です。 [ステートメントの要約持続性](/statement-summary-tables.md#persist-statements-summary)が有効な場合に、永続的なデータ ファイルを保持する最大日数を指定します。この変数の値は、構成項目[`tidb_stmt_summary_file_max_days`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_days-new-in-v660)の値と同じです。  |
| [`tidb_stmt_summary_file_max_size`](/system-variables.md#tidb_stmt_summary_file_max_size-new-in-v660)                                                        | 新しく追加された | この変数は読み取り専用です。 [ステートメントの要約持続性](/statement-summary-tables.md#persist-statements-summary)が有効な場合の永続データ ファイルの最大サイズを指定します。この変数の値は、構成項目[`tidb_stmt_summary_file_max_size`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_size-new-in-v660)の値と同じです。        |

### コンフィグレーションファイルパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーションパラメータ                                                                                                                                                                                                                                               | 変更の種類  | 説明                                                                                                                                                                                              |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiKV           | `rocksdb.enable-statistics`                                                                                                                                                                                                                                   | 削除済み     | この設定項目は、RocksDB の統計情報を有効にするかどうかを指定します。v6.6.0 以降、この項目は削除されました。RocksDB の統計情報は、診断を支援するために、デフォルトですべてのクラスタで有効になっています。詳細については、 [#13942](https://github.com/tikv/tikv/pull/13942)を参照してください。            |
| TiKV           | `raftdb.enable-statistics`                                                                                                                                                                                                                                    | 削除済み     | この設定項目は、 Raft RocksDB の統計情報を有効にするかどうかを指定します。v6.6.0 以降、この項目は削除されました。Raft RocksDBの統計情報は、診断を支援するために、デフォルトですべてのクラスターで有効になっています。詳細については、 [#13942](https://github.com/tikv/tikv/pull/13942)を参照してください。 |
| TiKV           | `storage.block-cache.shared`                                                                                                                                                                                                                                  | 削除済み     | バージョン6.6.0以降、この設定項目は削除され、ブロックキャッシュはデフォルトで有効になり、無効にすることはできません。詳細は[#12936](https://github.com/tikv/tikv/issues/12936)を参照してください。                                                                   |
| DM             | `on-duplicate`                                                                                                                                                                                                                                                | 削除済み     | この構成項目は、完全インポートフェーズ中に競合を解決する方法を制御します。v6.6.0 では、 `on-duplicate-logical` `on-duplicate-physical`と`on-duplicate`が導入されました。                                                                          |
| TiDB           | [`enable-telemetry`](/tidb-configuration-file.md#enable-telemetry-new-in-v402)                                                                                                                                                                                | 変更     | バージョン6.6.0以降、デフォルト値が`true`から`false`に変更され、TiDBではデフォルトでテレメトリが無効になります。                                                                                                                             |
| TiKV           | [`rocksdb.defaultcf.block-size`](/tikv-configuration-file.md#block-size)および[`rocksdb.writecf.block-size`](/tikv-configuration-file.md#block-size)                                                                                                             | 変更     | デフォルト値が`64K`から`32K`に変更されます。                                                                                                                                                                     |
| TiKV           | [`rocksdb.defaultcf.block-cache-size`](/tikv-configuration-file.md#block-cache-size) 、 [`rocksdb.writecf.block-cache-size`](/tikv-configuration-file.md#block-cache-size) 、 [`rocksdb.lockcf.block-cache-size`](/tikv-configuration-file.md#block-cache-size) | 非推奨      | バージョン6.6.0以降、これらの設定項目は非推奨となりました。詳細は[#12936](https://github.com/tikv/tikv/issues/12936)を参照してください。                                                                                                |
| PD             | [`enable-telemetry`](/pd-configuration-file.md#enable-telemetry)                                                                                                                                                                                              | 変更     | バージョン6.6.0以降、デフォルト値が`true`から`false`に変更され、TiDB Dashboardではテレメトリがデフォルトで無効になります。                                                                                                                      |
| DM             | [`import-mode`](/dm/task-configuration-file-full.md)                                                                                                                                                                                                          | 変更     | この構成項目の指定可能な値は、 `"sql"`および`"loader"`から`"logical"`および`"physical"`に変更されます。デフォルト値は`"logical"`で、これは TiDB Lightning の論理インポートモードを使用してデータをインポートすることを意味します。                                             |
| TiFlash        | [`profile.default.max_memory_usage_for_all_queries`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                                                                                                                                        | 変更     | すべてのクエリで生成される中間データのメモリ使用量制限を指定します。v6.6.0以降、デフォルト値は`0`から`0.8`に変更され、制限は総メモリの80%になります。                                                                                                             |
| TiCDC          | [`consistent.storage`](/ticdc/ticdc-sink-to-mysql.md#prerequisites)                                                                                                                                                                                           | 変更     | この構成項目は、リドゥログのバックアップが保存されるパスを指定します。 `scheme` 、GCS、およびAzure用に、さらに2つの値オプションが追加されました。                                                                                                              |
| TiDB           | [`initialize-sql-file`](/tidb-configuration-file.md#initialize-sql-file-new-in-v660)                                                                                                                                                                          | 新しく追加された | この設定項目は、TiDBクラスタが初めて起動されたときに実行されるSQLスクリプトを指定します。デフォルト値は空です。                                                                                                                                     |
| TiDB           | [`tidb_stmt_summary_enable_persistent`](/tidb-configuration-file.md#tidb_stmt_summary_enable_persistent-new-in-v660)                                                                                                                                          | 新しく追加された | この設定項目は、明細書の要約を永続化するかどうかを制御します。デフォルト値は`false`で、これはこの機能がデフォルトでは無効になっていることを意味します。                                                                                                                 |
| TiDB           | [`tidb_stmt_summary_file_max_backups`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_backups-new-in-v660)                                                                                                                                            | 新しく追加された | ステートメントサマリーの永続化が有効になっている場合、この設定では永続化できるデータファイルの最大数を指定します。 `0`ファイル数に制限がないことを意味します。                                                                                                               |
| TiDB           | [`tidb_stmt_summary_file_max_days`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_days-new-in-v660)                                                                                                                                                  | 新しく追加された | 明細書の要約データの永続化が有効になっている場合、この設定では永続データファイルを保持する最大日数を指定します。                                                                                                                                        |
| TiDB           | [`tidb_stmt_summary_file_max_size`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_size-new-in-v660)                                                                                                                                                  | 新しく追加された | ステートメントサマリーの永続化が有効になっている場合、この設定では永続データファイルの最大サイズ（MiB単位）を指定します。                                                                                                                                  |
| TiDB           | [`tidb_stmt_summary_filename`](/tidb-configuration-file.md#tidb_stmt_summary_filename-new-in-v660)                                                                                                                                                            | 新しく追加された | 明細書の要約データの永続化が有効になっている場合、この設定では永続データが書き込まれるファイルを指定します。                                                                                                                                          |
| TiKV           | [`resource-control.enabled`](/tikv-configuration-file.md#resource-control)                                                                                                                                                                                    | 新しく追加された | 対応するリソース グループの要求単位 (RU) に基づいて、ユーザーのフォアグラウンド読み取り/書き込み要求のスケジューリングを有効にするかどうか。デフォルト値は`false`で、これは対応するリソース グループの RU に基づくスケジューリングを無効にすることを意味します。                                                      |
| TiKV           | [`storage.engine`](/tikv-configuration-file.md#engine-new-in-v660)                                                                                                                                                                                            | 新しく追加された | この構成項目は、ストレージエンジンのタイプを指定します。値のオプションは`"raft-kv"`と`"partitioned-raft-kv"`です。この構成項目は、クラスタ作成時にのみ指定でき、一度指定すると変更できません。                                                                              |
| TiKV           | [`rocksdb.write-buffer-flush-oldest-first`](/tikv-configuration-file.md#write-buffer-flush-oldest-first-new-in-v660)                                                                                                                                          | 新しく追加された | この設定項目は、現在の RocksDB の`memtable`のメモリ使用量がしきい値に達したときに使用されるフラッシュ戦略を指定します。                                                                                                                           |
| TiKV           | [`rocksdb.write-buffer-limit`](/tikv-configuration-file.md#write-buffer-limit-new-in-v660)                                                                                                                                                                    | 新しく追加された | この設定項目は、単一の TiKV 内のすべての RocksDB インスタンス`memtable`が使用する合計メモリの制限を指定します。デフォルト値は、マシン全体のメモリの 25% です。                                                                                                  |
| PD             | [`pd-server.enable-gogc-tuner`](/pd-configuration-file.md#enable-gogc-tuner-new-in-v660)                                                                                                                                                                      | 新しく追加された | この設定項目は、GOGCチューナーを有効にするかどうかを制御します。デフォルトでは無効になっています。                                                                                                                                             |
| PD             | [`pd-server.gc-tuner-threshold`](/pd-configuration-file.md#gc-tuner-threshold-new-in-v660)                                                                                                                                                                    | 新しく追加された | この設定項目は、GOGC のチューニングにおける最大メモリしきい値比率を指定します。デフォルト値は`0.6`です。                                                                                                                                       |
| PD             | [`pd-server.server-memory-limit-gc-trigger`](/pd-configuration-file.md#server-memory-limit-gc-trigger-new-in-v660)                                                                                                                                            | 新しく追加された | この設定項目は、PD が GC をトリガーしようとするしきい値比率を指定します。デフォルト値は`0.7`です。                                                                                                                                         |
| PD             | [`pd-server.server-memory-limit`](/pd-configuration-file.md#server-memory-limit-new-in-v660)                                                                                                                                                                  | 新しく追加された | この設定項目は、PDインスタンスのメモリ制限比率を指定します。値`0`は、メモリ制限なしを意味します。                                                                                                                                             |
| TiCDC          | [`scheduler.region-per-span`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)                                                                                                                                                          | 新しく追加された | この構成項目は、リージョンの数に基づいてテーブルを複数のレプリケーション範囲に分割するかどうかを制御し、これらの範囲は複数の TiCDC ノードによってレプリケートできます。デフォルト値は`50000`です。                                                                                        |
| TiDB Lightning | [`compress-kv-pairs`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)                                                                                                                                                                    | 新しく追加された | この設定項目は、物理インポートモードでKVペアをTiKVに送信する際に圧縮を有効にするかどうかを制御します。デフォルト値は空欄で、これは圧縮が無効になっていることを意味します。                                                                                                        |
| DM             | [`checksum-physical`](/dm/task-configuration-file-full.md)                                                                                                                                                                                                    | 新しく追加された | この設定項目は、インポート後にデータ整合性を検証するために、DM が各テーブルに対して`ADMIN CHECKSUM TABLE <table>`を実行するかどうかを制御します。デフォルト値は`"required"`で、インポート後に管理者チェックサムを実行します。チェックサムが失敗した場合、DM はタスクを一時停止し、手動でエラーを処理する必要があります。            |
| DM             | [`disk-quota-physical`](/dm/task-configuration-file-full.md)                                                                                                                                                                                                  | 新しく追加された | この設定項目はディスククォータを設定します。これは、 TiDB Lightningの[`disk-quota`設定](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#configure-disk-quota-new-in-v620)に対応します。                                |
| DM             | [`on-duplicate-logical`](/dm/task-configuration-file-full.md)                                                                                                                                                                                                 | 新しく追加された | この設定項目は、論理インポートモードで DM が競合するデータをどのように解決するかを制御します。デフォルト値は`"replace"`で、これは新しいデータを使用して既存のデータを置き換えることを意味します。                                                                                        |
| DM             | [`on-duplicate-physical`](/dm/task-configuration-file-full.md)                                                                                                                                                                                                | 新しく追加された | この設定項目は、物理インポートモードで DM が競合データをどのように解決するかを制御します。デフォルト値は`"none"`で、これは競合データを解決しないことを意味します。 `"none"`は最高のパフォーマンスを発揮しますが、下流のデータベースでデータの不整合が発生する可能性があります。                                              |
| DM             | [`sorting-dir-physical`](/dm/task-configuration-file-full.md)                                                                                                                                                                                                 | 新しく追加された | この設定項目は、物理インポートモードでローカルKVソートに使用されるディレクトリを指定します。デフォルト値は`dir`設定と同じです。                                                                                                                             |
| sync-diff-inspector      | [`skip-non-existing-table`](/sync-diff-inspector/sync-diff-inspector-overview.md#configuration-file-description)                                                                                                                                              | 新しく追加された | この設定項目は、下流側のテーブルが上流側に存在しない場合に、上流側と下流側のデータ整合性のチェックをスキップするかどうかを制御します。                                                                                                                             |
| TiSpark        | [`spark.tispark.replica_read`](https://docs-archive.pingcap.com/tidb/v6.6/tispark-overview/#tispark-configurations)                                                                                                                                           | 新しく追加された | この構成項目は、読み取るレプリカの種類を制御します。値のオプションは`leader` 、 `follower` 、および`learner` 。                                                                                                                         |
| TiSpark        | [`spark.tispark.replica_read.label`](https://docs-archive.pingcap.com/tidb/v6.6/tispark-overview#tispark-configurations)                                                                                                                                      | 新しく追加された | この設定項目は、対象となるTiKVノードのラベルを設定するために使用されます。                                                                                                                                                         |

### その他 {#others}

-   [`store-io-pool-size`](/tikv-configuration-file.md#store-io-pool-size-new-in-v530)動的に変更できるようにサポートします。これにより、TiKVのパフォーマンスチューニングがより柔軟になります。
-   `LIMIT`句の制限を解除することで、実行パフォーマンスを向上させます。
-   バージョン6.6.0以降、 BRはバージョン6.1.0より前のクラスターへのデータ復元をサポートしていません。
-   バージョン6.6.0以降、TiDBは潜在的な正確性の問題のため、パーティション化されたテーブルの列型の変更をサポートしなくなりました。

## 改善点 {#improvements}

-   TiDB

    -   TTLバックグラウンドクリーニングタスクのスケジューリングメカニズムを改善し、単一テーブルのクリーニングタスクを複数のサブタスクに分割して、複数のTiDBノードで同時に実行するようにスケジュールできるようにする [#40361](https://github.com/pingcap/tidb/issues/40361) @[YangKeao](https://github.com/YangKeao)
    -   デフォルト以外の区切り文字を設定した後に複数ステートメントを実行することで返される結果の列名表示を最適化する [#39662](https://github.com/pingcap/tidb/issues/39662) @[mjonss](https://github.com/mjonss)
    -   警告メッセージ生成後のステートメントの実行効率を最適化する [#39702](https://github.com/pingcap/tidb/issues/39702) @[tiancaiamao](https://github.com/tiancaiamao)
    -   `ADD INDEX`の分散データバックフィルをサポート（実験的） [#37119](https://github.com/pingcap/tidb/issues/37119) @[zimulala](https://github.com/zimulala)
    -   `CURDATE()`を列のデフォルト値として使用することをサポートします [#38356](https://github.com/pingcap/tidb/issues/38356) @[CbcWestwolf](https://github.com/CbcWestwolf)
    -   `partial order prop push down`が LIST 型のパーティション テーブルをサポートするようになりました [#40273](https://github.com/pingcap/tidb/issues/40273) @[winoros](https://github.com/winoros)
    -   オプティマイザーのヒントと実行プランのバインディング間の競合に関するエラー メッセージを追加 [#40910](https://github.com/pingcap/tidb/issues/40910) @[Reminiscent](https://github.com/Reminiscent)
    -   プランキャッシュ戦略を最適化し、一部のシナリオでプランキャッシュを使用する際に最適でないプランを回避する[#40312](https://github.com/pingcap/tidb/pull/40312) [#40218](https://github.com/pingcap/tidb/pull/40218) [#40280](https://github.com/pingcap/tidb/pull/40280) [#41136](https://github.com/pingcap/tidb/pull/41136) [#40686](https://github.com/pingcap/tidb/pull/40686) @[qw4990](https://github.com/qw4990)
    -   メモリリークとパフォーマンスの低下を避けるために、期限切れの領域キャッシュを定期的にクリアします [#40461](https://github.com/pingcap/tidb/issues/40461) @[sticnarf](https://github.com/sticnarf)
    -   `MODIFY COLUMN`はパーティションテーブルではサポートされていません [#39915](https://github.com/pingcap/tidb/issues/39915) @[wjhuang2016](https://github.com/wjhuang2016)
    -   パーティションテーブルが依存する列の名前変更を無効にする [#40150](https://github.com/pingcap/tidb/issues/40150) @[mjonss](https://github.com/mjonss)
    -   パーティションテーブルが依存する列が削除されたときに報告されるエラーメッセージを改善する [#38739](https://github.com/pingcap/tidb/issues/38739) @[jiyfhust](https://github.com/jiyfhust)
    -   `FLASHBACK CLUSTER`が`min-resolved-ts`のチェックに失敗した場合に再試行するメカニズムを追加します [#39836](https://github.com/pingcap/tidb/issues/39836) @[Defined2014](https://github.com/Defined2014)

-   TiKV

    -   partitioned-raft-kv モードにおける一部のパラメータのデフォルト値を最適化します。TiKV 設定項目`storage.block-cache.capacity`のデフォルト値を 45% から 30% に調整し、 `region-split-size`のデフォルト値を`96MiB`から`10GiB`に調整します。raft-kv モードを使用し、 `enable-region-bucket`が`true`の場合、 `region-split-size`はデフォルトで 1 GiB に調整されます。 [#12842](https://github.com/tikv/tikv/issues/12842) @[tonyxuqqi](https://github.com/tonyxuqqi)
    -   Raftstoreの非同期書き込みにおける優先度スケジューリングのサポート [#13730](https://github.com/tikv/tikv/issues/13730) @[Connor1996](https://github.com/Connor1996)
    -   コア数が1未満のCPUでTiKVを起動するサポート[#13586](https://github.com/tikv/tikv/issues/13586) [#13752](https://github.com/tikv/tikv/issues/13752) [#14017](https://github.com/tikv/tikv/issues/14017) @[andreid-db](https://github.com/andreid-db)
    -   Raftstoreのスロースコアの新しい検出メカニズムを最適化し、 `evict-slow-trend-scheduler` [#14131](https://github.com/tikv/tikv/issues/14131) @[innerr](https://github.com/innerr)を追加しました
    -   RocksDB のブロックキャッシュを共有し、CF に従ってブロックキャッシュを個別に設定することをサポートしなくなりました。 [#12936](https://github.com/tikv/tikv/issues/12936) @[busyjay](https://github.com/busyjay)

-   PD

    -   OOM問題を軽減するためのグローバルメモリしきい値の管理をサポート（実験的） [#5827](https://github.com/tikv/pd/issues/5827) @[hnes](https://github.com/hnes)
    -   GC圧力を軽減するためにGCチューナーを追加（実験的） [#5827](https://github.com/tikv/pd/issues/5827) @[hnes](https://github.com/hnes)
    -   異常なノードを検出してスケジュールするための`evict-slow-trend-scheduler`スケジューラを追加します [#5808](https://github.com/tikv/pd/pull/5808) @[innerr](https://github.com/innerr)
    -   キースペースを管理するためにキースペース マネージャーを追加 [#5293](https://github.com/tikv/pd/issues/5293) @[AmoebaProtozoa](https://github.com/AmoebaProtozoa)

-   TiFlash

    -   TiFlashデータスキャンプロセスにおけるMVCCフィルタリング操作を分離する独立したMVCCビットマップフィルタをサポートし、データスキャンプロセスの将来的な最適化の基盤を提供する [#6296](https://github.com/pingcap/tiflash/issues/6296) @[JinheLin](https://github.com/JinheLin)
    -   クエリがない場合、 TiFlashのメモリ使用量を最大30%削減します [#6589](https://github.com/pingcap/tiflash/pull/6589) @[hongyunyan](https://github.com/hongyunyan)

-   ツール

    -   Backup & Restore (BR)

        -   TiKV側でのログバックアップファイルのダウンロードの同時実行性を最適化し、通常のシナリオにおけるPITRリカバリのパフォーマンスを向上させる [#14206](https://github.com/tikv/tikv/issues/14206) @[YuJuncen](https://github.com/YuJuncen)

    -   TiCDC

        -   TiCDCレプリケーションのパフォーマンスを向上させるためのバッチ`UPDATE` DMLステートメントのサポート [#8084](https://github.com/pingcap/tiflow/issues/8084) @[amyangfei](https://github.com/amyangfei)
        -   MQ シンクと MySQL シンクを非同期モードで実装して、シンクのスループットを向上させます [#5928](https://github.com/pingcap/tiflow/issues/5928) @[hicqu](https://github.com/hicqu)@[Rustin170506](https://github.com/Rustin170506)

    -   TiDB Data Migration (DM)

        -   DM アラート ルールとコンテンツを最適化 [#7376](https://github.com/pingcap/tiflow/issues/7376) @[D3Hunter](https://github.com/D3Hunter)

            従来は、関連するエラーが発生するたびに「DM_XXX_process_exits_with_error」のようなアラートが発生していました。しかし、一部のアラートはアイドル状態のデータベース接続が原因で発生し、再接続後に回復できる場合があります。このようなアラートを減らすため、DMはエラーを自動的に回復可能なエラーと回復不可能なエラーの2種類に分類します。

            -   自動的に回復可能なエラーの場合、DMは2分以内にエラーが3回以上発生した場合にのみアラートを報告します。
            -   自動的に回復できないエラーの場合、DMは元の動作を維持し、アラートを即座に報告します。

        -   非同期/バッチリレーライターを追加してリレーパフォーマンスを最適化 [#4287](https://github.com/pingcap/tiflow/issues/4287) @[GMHDBJD](https://github.com/GMHDBJD)

    -   TiDB Lightning

        -   物理インポートモードはキースペース [#40531](https://github.com/pingcap/tidb/issues/40531) @[iosmanthus](https://github.com/iosmanthus)をサポートします
        -   `lightning.max-error`による競合の最大数設定のサポート [#40743](https://github.com/pingcap/tidb/issues/40743) @[dsdashun](https://github.com/dsdashun)
        -   BOMヘッダー付きCSVデータファイルのインポートをサポート [#40744](https://github.com/pingcap/tidb/issues/40744) @[dsdashun](https://github.com/dsdashun)
        -   TiKVフロー制限エラーが発生した場合の処理​​ロジックを最適化し、代わりに他の利用可能な領域を試す [#40205](https://github.com/pingcap/tidb/issues/40205) @[lance6716](https://github.com/lance6716)
        -   インポート中のテーブル外部キーのチェックを無効にする [#40027](https://github.com/pingcap/tidb/issues/40027) @[sleepymole](https://github.com/sleepymole)

    -   Dumpling

        -   外部キーの設定のエクスポートをサポート [#39913](https://github.com/pingcap/tidb/issues/39913) @[lichunzhu](https://github.com/lichunzhu)

    -   sync-diff-inspector

        -   下流のテーブルが上流に存在しない場合に、上流と下流のデータ整合性のチェックをスキップするかどうかを制御する新しいパラメータ`skip-non-existing-table`を追加します [#692](https://github.com/pingcap/tidb-tools/issues/692) @[lichunzhu](https://github.com/lichunzhu)@[liumengya94](https://github.com/liumengya94)

## バグ修正 {#bug-fixes}

-   TiDB

    -   統計収集タスクが`datetime`値の誤りにより失敗する問題を修正 [#39336](https://github.com/pingcap/tidb/issues/39336) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    -   テーブル作成後に`stats_meta`が作成されない問題を修正 [#38189](https://github.com/pingcap/tidb/issues/38189) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    -   DDLデータバックフィル実行時のトランザクションにおける頻繁な書き込み競合を修正 [#24427](https://github.com/pingcap/tidb/issues/24427) @[mjonss](https://github.com/mjonss)
    -   インジェストモードを使用して空のテーブルにインデックスを作成できない場合がある問題を修正 [#39641](https://github.com/pingcap/tidb/issues/39641) @[tangenta](https://github.com/tangenta)
    -   スロークエリログの`wait_ts`が同じトランザクション内の異なる SQL ステートメントでも同じである問題を修正 [#39713](https://github.com/pingcap/tidb/issues/39713) @[TonsnakeLin](https://github.com/TonsnakeLin)
    -   行レコードの削除処理中に列を追加した際に`Assertion Failed`エラーが報告される問題を修正しました [#39570](https://github.com/pingcap/tidb/issues/39570) @[wjhuang2016](https://github.com/wjhuang2016)
    -   列タイプを変更する際に`not a DDL owner`エラーが報告される問題を修正しました [#39643](https://github.com/pingcap/tidb/issues/39643) @[zimulala](https://github.com/zimulala)
    -   `AUTO_INCREMENT`列のAUTO_INCREMENT値が使い果たされた後に行を挿入してもエラーが報告されない問題を修正しました [#38950](https://github.com/pingcap/tidb/issues/38950) @[Dousir9](https://github.com/Dousir9)
    -   式インデックスの作成時に`Unknown column`エラーが報告される問題を修正 [#39784](https://github.com/pingcap/tidb/issues/39784) @[Defined2014](https://github.com/Defined2014)
    -   生成された式にこのテーブルの名前が含まれている場合、名前が変更されたテーブルにデータを挿入できない問題を修正します [#39826](https://github.com/pingcap/tidb/issues/39826) @[Defined2014](https://github.com/Defined2014)
    -   列が書き込み専用の場合に`INSERT ignore`ステートメントがデフォルト値を入力できない問題を修正 [#40192](https://github.com/pingcap/tidb/issues/40192) @[YangKeao](https://github.com/YangKeao)
    -   リソース管理モジュールを無効にしたときにリソースが解放されない問題を修正 [#40546](https://github.com/pingcap/tidb/issues/40546) @[zimulala](https://github.com/zimulala)
    -   TTLタスクが統計情報の更新を時間内にトリガーできない問題を修正 [#40109](https://github.com/pingcap/tidb/issues/40109) @[YangKeao](https://github.com/YangKeao)
    -   TiDBがキー範囲を構築する際に`NULL`値を適切に処理しないために予期しないデータが読み込まれる問題を修正しました [#40158](https://github.com/pingcap/tidb/issues/40158) @[tiancaiamao](https://github.com/tiancaiamao)
    -   `MODIFY COLUMN`ステートメントが列のデフォルト値も変更する場合に、無効な値がテーブルに書き込まれる問題を修正します [#40164](https://github.com/pingcap/tidb/issues/40164) @[wjhuang2016](https://github.com/wjhuang2016)
    -   テーブル内にリージョンが多数存在する場合に、リージョンキャッシュが無効になるためインデックス追加操作が非効率になる問題を修正しました [#38436](https://github.com/pingcap/tidb/issues/38436) @[tangenta](https://github.com/tangenta)
    -   AUTO_INCREMENT IDの割り当て時に発生したデータ競合を修正 [#40584](https://github.com/pingcap/tidb/issues/40584) @[Dousir9](https://github.com/Dousir9)
    -   JSON の not 演算子の実装が MySQL の実装と互換性がない問題を修正しました [#40683](https://github.com/pingcap/tidb/issues/40683) @[YangKeao](https://github.com/YangKeao)
    -   同時ビューがDDL操作をブロックする可能性がある問題を修正 [#40352](https://github.com/pingcap/tidb/issues/40352) @[zeminzhou](https://github.com/zeminzhou)
    -   パーティションテーブルの列を変更するDDLステートメントを同時に実行することによって発生するデータの不整合を修正 [#40620](https://github.com/pingcap/tidb/issues/40620) @[mjonss](https://github.com/mjonss)@[mjonss](https://github.com/mjonss)
    -   `caching_sha2_password`を認証に使用し、パスワードを指定しない場合に「不正なパケット」が報告される問題を修正 [#40831](https://github.com/pingcap/tidb/issues/40831) @[dveeden](https://github.com/dveeden)
    -   テーブルの主キーに`ENUM`列が含まれている場合に TTL タスクが失敗する問題を修正しました [#40456](https://github.com/pingcap/tidb/issues/40456) @[lcwangchao](https://github.com/lcwangchao)
    -   `mysql.tidb_mdl_view` [#40838](https://github.com/pingcap/tidb/issues/40838) @[YangKeao](https://github.com/YangKeao)で、MDLによってブロックされた一部のDDL操作をクエリできない問題を修正します。
    -   DDL取り込み中にデータ競合が発生する可能性がある問題を修正 [#40970](https://github.com/pingcap/tidb/issues/40970) @[tangenta](https://github.com/tangenta)
    -   タイムゾーン変更後にTTLタスクが一部のデータを誤って削除する可能性がある問題を修正 [#41043](https://github.com/pingcap/tidb/issues/41043) @[lcwangchao](https://github.com/lcwangchao)
    -   `JSON_OBJECT`が場合によってはエラーを報告する問題を修正 [#39806](https://github.com/pingcap/tidb/issues/39806) @[YangKeao](https://github.com/YangKeao)
    -   TiDB が初期化中にデッドロックする可能性がある問題を修正 [#40408](https://github.com/pingcap/tidb/issues/40408) @[Defined2014](https://github.com/Defined2014)
    -   メモリ再利用によりシステム変数の値が場合によっては誤って変更される可能性がある問題を修正 [#40979](https://github.com/pingcap/tidb/issues/40979) @[lcwangchao](https://github.com/lcwangchao)
    -   取り込みモードで一意インデックスを作成すると、データがインデックスと矛盾する可能性がある問題を修正します [#40464](https://github.com/pingcap/tidb/issues/40464) @[tangenta](https://github.com/tangenta)
    -   同じテーブルを同時に切り捨てる際に、一部の切り捨て操作がMDLによってブロックされない問題を修正しました [#40484](https://github.com/pingcap/tidb/issues/40484) @[wjhuang2016](https://github.com/wjhuang2016)
    -   `SHOW PRIVILEGES`ステートメントが不完全な特権リストを返す問題を修正 [#40591](https://github.com/pingcap/tidb/issues/40591) @[CbcWestwolf](https://github.com/CbcWestwolf)
    -   一意インデックスを追加するときに TiDB がパニックになる問題を修正 [#40592](https://github.com/pingcap/tidb/issues/40592) @[tangenta](https://github.com/tangenta)
    -   `ADMIN RECOVER`ステートメントを実行するとインデックスデータが破損する可能性がある問題を修正しました [#40430](https://github.com/pingcap/tidb/issues/40430) @[xiongjiwei](https://github.com/xiongjiwei)
    -   クエリ対象のテーブルに式インデックスに`CAST`式が含まれている場合にクエリが失敗する可能性がある問題を修正しました [#40130](https://github.com/pingcap/tidb/issues/40130) @[xiongjiwei](https://github.com/xiongjiwei)
    -   一意インデックスが場合によっては重複データを生成する可能性がある問題を修正 [#40217](https://github.com/pingcap/tidb/issues/40217) @[tangenta](https://github.com/tangenta)
    -   `Prepare`または`Execute` [#39605](https://github.com/pingcap/tidb/issues/39605) @[djshow832](https://github.com/djshow832)
    -   インデックス追加時にデータ競合が発生する可能性がある問題を修正 [#40879](https://github.com/pingcap/tidb/issues/40879) @[tangenta](https://github.com/tangenta)
    -   仮想列 [#41014](https://github.com/pingcap/tidb/issues/41014) @[AilinKid](https://github.com/AilinKid)によって引き起こされる`can't find proper physical plan`の問題を修正します
    -   動的トリミングモードでパーティションテーブルのグローバルバインディングが作成された後、TiDBが再起動できない問題を修正 [#40368](https://github.com/pingcap/tidb/issues/40368) @[Yisaer](https://github.com/Yisaer)
    -   `auto analyze`が原因で正常シャットダウンに時間がかかる問題を修正 [#40038](https://github.com/pingcap/tidb/issues/40038) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    -   IndexMerge オペレーターがメモリ制限動作をトリガーしたときの TiDBサーバーのpanicを修正 [#41036](https://github.com/pingcap/tidb/pull/41036) @[guo-shaoge](https://github.com/guo-shaoge)
    -   パーティションテーブルに対する`SELECT * FROM table_name LIMIT 1`クエリが遅い問題を修正 [#40741](https://github.com/pingcap/tidb/pull/40741) @[solotzg](https://github.com/solotzg)

-   TiKV

    -   `const Enum`型を他の型にキャストする際に発生するエラーを修正します [#14156](https://github.com/tikv/tikv/issues/14156) @[wshwsh12](https://github.com/wshwsh12)
    -   解決された TS によりネットワーク トラフィックが増加する問題を修正 [#14092](https://github.com/tikv/tikv/issues/14092) @[overvenus](https://github.com/overvenus)
    -   TiDBとTiKV間のネットワーク障害によって発生するデータ不整合の問題を修正。DML実行中に悲観的DMLが失敗した後に発生するデータ不整合の問題を修正 [#14038](https://github.com/tikv/tikv/issues/14038) @[MyonKeminta](https://github.com/MyonKeminta)

-   PD

    -   リージョン Scatterタスクが予期せず冗長なレプリカを生成する問題を修正 [#5909](https://github.com/tikv/pd/issues/5909) @[HunDunDM](https://github.com/HunDunDM)
    -   オンラインの安全でない回復機能が`auto-detect`モードで停止してタイムアウトする問題を修正しました [#5753](https://github.com/tikv/pd/issues/5753) @[Connor1996](https://github.com/Connor1996)
    -   特定の条件下で`replace-down-peer`実行が遅くなる問題を修正 [#5788](https://github.com/tikv/pd/issues/5788) @[HunDunDM](https://github.com/HunDunDM)
    -   `ReportMinResolvedTS`の呼び出しが頻繁すぎる場合に発生する PD OOM 問題を修正します [#5965](https://github.com/tikv/pd/issues/5965) @[HunDunDM](https://github.com/HunDunDM)

-   TiFlash

    -   TiFlash関連のシステムテーブルへのクエリが停止する可能性がある問題を修正 [#6745](https://github.com/pingcap/tiflash/pull/6745) @[lidezhu](https://github.com/lidezhu)
    -   セミジョインがデカルト積を計算する際に過剰なメモリを使用する問題を修正 [#6730](https://github.com/pingcap/tiflash/issues/6730) @[gengliqi](https://github.com/gengliqi)
    -   DECIMAL データ型の除算演算の結果が丸められない問題を修正 [#6393](https://github.com/pingcap/tiflash/issues/6393) @[LittleFall](https://github.com/LittleFall)
    -   TiFlashクエリで`start_ts`がMPPクエリを一意に識別できない問題を修正します。これにより、MPPクエリが誤ってキャンセルされる可能性があります [#43426](https://github.com/pingcap/tidb/issues/43426) @[hehechen](https://github.com/hehechen)

-   ツール

    -   Backup & Restore (BR)

        -   ログバックアップの復元時に、ホットリージョンが原因で復元が失敗する問題を修正 [#37207](https://github.com/pingcap/tidb/issues/37207) @[Leavrth](https://github.com/Leavrth)
        -   ログバックアップが実行されているクラスターにデータを復元すると、ログバックアップファイルが復元不能になる問題を修正しました [#40797](https://github.com/pingcap/tidb/issues/40797) @[Leavrth](https://github.com/Leavrth)
        -   PITR 機能が CA バンドルをサポートしていない問題を修正 [#38775](https://github.com/pingcap/tidb/issues/38775) @[YuJuncen](https://github.com/YuJuncen)
        -   リカバリ中に重複する一時テーブルが原因で発生するpanic問題を修正 [#40797](https://github.com/pingcap/tidb/issues/40797) @[joccau](https://github.com/joccau)
        -   PITR が PD クラスターの構成変更をサポートしていない問題を修正 [#14165](https://github.com/tikv/tikv/issues/14165) @[YuJuncen](https://github.com/YuJuncen)
        -   PDとtidb-server間の接続障害によりPITRバックアップの進行状況が進まなくなる問題を修正 [#41082](https://github.com/pingcap/tidb/issues/41082) @[YuJuncen](https://github.com/YuJuncen)
        -   PDとTiKV間の接続障害によりTiKVがPITRタスクをリッスンできない問題を修正 [#14159](https://github.com/tikv/tikv/issues/14159) @[YuJuncen](https://github.com/YuJuncen)
        -   TiDBクラスタにPITRバックアップタスクがない場合、 `resolve lock`の頻度が高すぎる問題を修正 [#40759](https://github.com/pingcap/tidb/issues/40759) @[joccau](https://github.com/joccau)
        -   PITRバックアップタスクが削除された際に、残存バックアップデータが原因で新しいタスクのデータ不整合が発生する問題を修正しました [#40403](https://github.com/pingcap/tidb/issues/40403) @[joccau](https://github.com/joccau)

    -   TiCDC

        -   `transaction_atomicity`と`protocol`が設定ファイル経由で更新できない問題を修正しました [#7935](https://github.com/pingcap/tiflow/issues/7935) @[CharlesCheung96](https://github.com/CharlesCheung96)
        -   リドゥログのストレージパスで事前チェ​​ックが実行されない問題を修正 [#6335](https://github.com/pingcap/tiflow/issues/6335) @[CharlesCheung96](https://github.com/CharlesCheung96)
        -   S3storage障害時にリドゥログが許容できる期間が不十分であるという問題を修正 [#8089](https://github.com/pingcap/tiflow/issues/8089) @[CharlesCheung96](https://github.com/CharlesCheung96)
        -   TiKVまたはTiCDCノードのスケールインまたはスケールアウト時などの特殊なシナリオでchangefeedが停止する可能性がある問題を修正しました [#8174](https://github.com/pingcap/tiflow/issues/8174) @[hicqu](https://github.com/hicqu)
        -   TiKV ノード間のトラフィックが多すぎる問題を修正 [#14092](https://github.com/tikv/tikv/issues/14092) @[overvenus](https://github.com/overvenus)
        -   プルベースのシンクが有効になっている場合の CPU 使用率、メモリ制御、スループットに関する TiCDC のパフォーマンスの問題を修正[#8142](https://github.com/pingcap/tiflow/issues/8142) [#8157](https://github.com/pingcap/tiflow/issues/8157) [#8001](https://github.com/pingcap/tiflow/issues/8001) [#5928](https://github.com/pingcap/tiflow/issues/5928) @[hicqu](https://github.com/hicqu)@[Rustin170506](https://github.com/Rustin170506)

    -   TiDB Data Migration (DM)

        -   `binlog-schema delete`コマンドの実行に失敗する問題を修正しました [#7373](https://github.com/pingcap/tiflow/issues/7373) @[liumengya94](https://github.com/liumengya94)
        -   最後のbinlogがスキップされたDDLである場合にチェックポイントが進まない問題を修正 [#8175](https://github.com/pingcap/tiflow/issues/8175) @[D3Hunter](https://github.com/D3Hunter)
        -   1 つのテーブルで「更新」タイプと「非更新」タイプの両方の式フィルターが指定されている場合、すべての`UPDATE`ステートメントがスキップされるバグを修正しました [#7831](https://github.com/pingcap/tiflow/issues/7831) @[lance6716](https://github.com/lance6716)
        -   テーブルに`update-old-value-expr`または`update-new-value-expr`のいずれか一方のみが設定されている場合、フィルタルールが有効にならないか、DM がパニックを起こすバグを修正しました。 [#7774](https://github.com/pingcap/tiflow/issues/7774) @[lance6716](https://github.com/lance6716)

    -   TiDB Lightning

        -   一部のシナリオで TiDB の再起動によりTiDB Lightningタイムアウトがハングする問題を修正 [#33714](https://github.com/pingcap/tidb/issues/33714) @[lichunzhu](https://github.com/lichunzhu)
        -   TiDB Lightning が並列インポート中に最後のTiDB Lightningインスタンスを除くすべてのインスタンスでローカルの重複レコードに遭遇した場合に、競合解決を誤ってスキップする可能性がある問題を修正しました [#40923](https://github.com/pingcap/tidb/issues/40923) @[lichunzhu](https://github.com/lichunzhu)
        -   事前チェックでターゲットクラスター内で実行中の TiCDC の存在を正確に検出できない問題を修正します [#41040](https://github.com/pingcap/tidb/issues/41040) @[lance6716](https://github.com/lance6716)
        -   TiDB Lightningが分割リージョンフェーズでパニックを起こす問題を修正 [#40934](https://github.com/pingcap/tidb/issues/40934) @[lance6716](https://github.com/lance6716)
        -   競合解決ロジック ( `duplicate-resolution` ) がチェックサムの不一致を引き起こす可能性がある問題を修正 [#40657](https://github.com/pingcap/tidb/issues/40657) @[sleepymole](https://github.com/sleepymole)
        -   データ ファイルに閉じられていない区切り文字がある場合に発生する可能性のある OOM 問題を修正 [#40400](https://github.com/pingcap/tidb/issues/40400) @[buchuitoudegou](https://github.com/buchuitoudegou)
        -   エラーレポート内のファイルオフセットがファイルサイズを超える問題を修正 [#40034](https://github.com/pingcap/tidb/issues/40034) @[buchuitoudegou](https://github.com/buchuitoudegou)
        -   PDClient の新しいバージョンで並列インポートが失敗する可能性がある問題を修正 [#40493](https://github.com/pingcap/tidb/issues/40493) @[AmoebaProtozoa](https://github.com/AmoebaProtozoa)
        -   TiDB Lightningの事前チェックで、以前のインポート失敗によって残されたダーティデータを見つけられない問題を修正 [#39477](https://github.com/pingcap/tidb/issues/39477) @[dsdashun](https://github.com/dsdashun)

## 貢献者 {#contributors}

TiDBコミュニティの以下の貢献者の皆様に感謝申し上げます。

-   [morgo](https://github.com/morgo)
-   [jiyfhust](https://github.com/jiyfhust)
-   [b41sh](https://github.com/b41sh)
-   [sourcelliu](https://github.com/sourcelliu)
-   [songzhibin97](https://github.com/songzhibin97)
-   [mamil](https://github.com/mamil)
-   [Dousir9](https://github.com/Dousir9)
-   [hihihuhu](https://github.com/hihihuhu)
-   [mychoxin](https://github.com/mychoxin)
-   [xuning97](https://github.com/xuning97)
-   [andreid-db](https://github.com/andreid-db)
