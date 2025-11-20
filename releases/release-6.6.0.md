---
title: TiDB 6.6.0 Release Notes
summary: TiDB 6.6.0 の新機能、互換性の変更、改善点、バグ修正について説明します。
---

# TiDB 6.6.0 リリースノート {#tidb-6-6-0-release-notes}

発売日：2023年2月20日

TiDBバージョン: 6.6.0- [DMR](/releases/versioning.md#development-milestone-releases)

> **注記：**
>
> TiDB 6.6.0-DMR のドキュメントは[アーカイブ済み](https://docs-archive.pingcap.com/tidb/v6.6/)です。PingCAP では、TiDB データベースの[最新のLTSバージョン](https://docs.pingcap.com/tidb/stable)使用することを推奨しています。

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.6/quick-start-with-tidb)

v6.6.0-DMR の主な新機能と改善点は次のとおりです。

<table><thead><tr><th>カテゴリ</th><th>特徴</th><th>説明</th></tr></thead><tbody><tr><td rowspan="3">スケーラビリティとパフォーマンス<br /></td><td>TiKV は<a href="https://docs.pingcap.com/tidb/v6.6/partitioned-raft-kv" target="_blank">Partitioned Raft KVstorageエンジン</a>をサポートします (実験的)</td><td> TiKV ではパーティション化されたRaft KVstorageエンジンが導入され、各リージョンで独立した RocksDB インスタンスが使用されるため、クラスターのstorage容量を TB から PB に簡単に拡張でき、書き込みレイテンシーの安定化とスケーラビリティの強化が可能になります。</td></tr><tr><td> TiKVは<a href="https://docs.pingcap.com/tidb/v6.6/system-variables#tidb_store_batch_size" target="_blank">データ要求のバッチ集約</a>をサポートします</td><td>この機能強化により、TiKVバッチゲット操作におけるRPCの総数が大幅に削減されます。データが広範囲に分散し、gRPCスレッドプールのリソースが不足している状況では、コプロセッサリクエストをバッチ処理することでパフォーマンスを50%以上向上させることができます。</td></tr><tr><td> TiFlashは<a href="https://docs.pingcap.com/tidb/v6.6/stale-read" target="_blank">ステイル読み取り</a>と<a href="https://docs.pingcap.com/tidb/v6.6/explain-mpp#mpp-version-and-exchange-data-compression" target="_blank">圧縮交換</a>をサポート</td><td>TiFlashはステイルリード機能をサポートしており、リアルタイム性が制限されないシナリオにおいてクエリパフォーマンスを向上させることができます。TiFlashはデータ圧縮をサポートし、並列データ交換の効率性を向上させます。これにより、TPC-H全体のパフォーマンスが10%向上し、ネットワーク使用量を50%以上削減できます。</td></tr><tr><td rowspan="2">信頼性と可用性<br /></td><td><a href="https://docs.pingcap.com/tidb/v6.6/tidb-resource-control" target="_blank">リソース制御</a>（実験的）</td><td>リソース グループに基づくリソース管理をサポートします。これにより、データベース ユーザーを対応するリソース グループにマッピングし、実際のニーズに基づいて各リソース グループのクォータを設定します。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v6.6/sql-plan-management#create-a-binding-according-to-a-historical-execution-plan" target="_blank">歴史的なSQLバインディング</a></td><td>TiDB ダッシュボードで、履歴実行プランのバインドと実行プランの迅速なバインドをサポートします。</td></tr><tr><td rowspan="2"> SQL機能<br /></td><td><a href="https://docs.pingcap.com/tidb/v6.6/foreign-key" target="_blank">外部キー</a>（実験的）</td><td>データの一貫性を維持し、データ品質を向上させるために、MySQL 互換の外部キー制約をサポートします。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v6.6/sql-statement-create-index#multi-valued-indexes" target="_blank">多値インデックス</a>（実験的）</td><td> MySQL 互換の複数値インデックスを導入し、JSON タイプを拡張して、TiDB と MySQL 8.0 の互換性を向上させます。</td></tr><tr><td> DB操作と可観測性<br /></td><td><a href="https://docs.pingcap.com/tidb/v6.6/dm-precheck#check-items-for-physical-import" target="_blank">DM は物理インポートをサポートします</a>(実験的)</td><td> TiDB Data Migration (DM) は、TiDB Lightning の物理インポート モードを統合し、完全なデータ移行のパフォーマンスを最大 10 倍向上させます。</td></tr></tbody></table>

## 機能の詳細 {#feature-details}

### スケーラビリティ {#scalability}

-   パーティション化されたRaft KVstorageエンジンをサポート (実験的) [＃11515](https://github.com/tikv/tikv/issues/11515) [＃12842](https://github.com/tikv/tikv/issues/12842) @ [忙しいカケス](https://github.com/busyjay) @ [トニーシュキ](https://github.com/tonyxuqqi) @ [タボキ](https://github.com/tabokie) @ [バッファフライ](https://github.com/bufferflies) @ [5kbps](https://github.com/5kbpers) @ [スペードA-タン](https://github.com/SpadeA-Tang) @ [ノルーシュ](https://github.com/nolouch)

    TiDB v6.6.0より前では、TiKVのRaftベースのstorageエンジンは、単一のRocksDBインスタンスを使用して、TiKVインスタンスのすべての「リージョン」のデータを格納していました。より安定して大規模なクラスターをサポートするために、TiDB v6.6.0以降では、複数のRocksDBインスタンスを使用してTiKVリージョンデータを格納し、各リージョンのデータは独立したRocksDBインスタンスに独立して格納される新しいTiKVstorageエンジンが導入されました。新しいエンジンは、RocksDBインスタンス内のファイルの数とレベルをより適切に制御し、リージョン間のデータ操作の物理的な分離を実現し、より多くのデータの安定した管理をサポートします。これは、TiKVがパーティショニングによって複数のRocksDBインスタンスを管理しているのと見なすことができるため、この機能はPartitioned-Raft-KVと名付けられています。この機能の主な利点は、書き込みパフォーマンスが向上し、スケーリングが高速になり、同じハードウェアでサポートされるデータ量が増えることです。また、より大きなクラスタースケールもサポートできます。

    現在、この機能は実験的であり、本番環境での使用は推奨されません。

    詳細については[ドキュメント](/partitioned-raft-kv.md)参照してください。

-   DDL操作の分散並列実行フレームワークをサポート（実験的） [＃37125](https://github.com/pingcap/tidb/issues/37125) @ [ジムララ](https://github.com/zimulala)

    以前のバージョンでは、TiDBクラスタ全体のうち1つのTiDBインスタンスのみがDDLオーナーとしてスキーマ変更タスクを処理できました。大規模テーブルのDDL操作におけるDDL同時実行性をさらに向上させるため、TiDB v6.6.0ではDDLの分散並列実行フレームワークが導入されました。これにより、クラスタ内のすべてのTiDBインスタンスが同じタスクの第`StateWriteReorganization`フェーズを同時に実行し、DDL実行を高速化できます。この機能はシステム変数[`tidb_ddl_distribute_reorg`](https://docs.pingcap.com/tidb/v6.6/system-variables#tidb_ddl_distribute_reorg-new-in-v660)によって制御され、現在は`Add Index`操作のみをサポートしています。

### パフォーマンス {#performance}

-   悲観的ロックキュー[＃13298](https://github.com/tikv/tikv/issues/13298) @ [ミョンケミンタ](https://github.com/MyonKeminta)の安定したウェイクアップ モデルをサポート

    アプリケーションがシングルポイントの悲観的ロック競合を頻繁に発生させる場合、既存のウェイクアップメカニズムではトランザクションがロックを取得する時間を保証できず、ロングテールレイテンシーが長くなり、ロック取得タイムアウトが発生することがあります。バージョン6.6.0以降では、システム変数[`tidb_pessimistic_txn_aggressive_locking`](https://docs.pingcap.com/tidb/v6.6/system-variables#tidb_pessimistic_txn_aggressive_locking-new-in-v660)の値を`ON`に設定することで、悲観的ロックに対する安定したウェイクアップモデルを有効にすることができます。このウェイクアップモデルでは、キューのウェイクアップシーケンスを厳密に制御することで、無効なウェイクアップによるリソースの浪費を回避できます。深刻なロック競合が発生するシナリオでは、安定したウェイクアップモデルによってロングテールレイテンシーとP99応答時間を削減できます。

    テストでは、これによりテールレイテンシーが 40 ～ 60% 削減されることが示されています。

    詳細については[ドキュメント](https://docs.pingcap.com/tidb/v6.6/system-variables#tidb_pessimistic_txn_aggressive_locking-new-in-v660)参照してください。

-   バッチ集計データ要求[＃39361](https://github.com/pingcap/tidb/issues/39361) @ [cfzjywxk](https://github.com/cfzjywxk) @ [あなた06](https://github.com/you06)

    TiDB が TiKV にデータ要求を送信すると、TiDB はデータが配置されているリージョンに応じて要求を異なるサブタスクにコンパイルし、各サブタスクは単一のリージョンの要求のみを処理します。アクセスするデータが大きく分散している場合、データのサイズが大きくなくても多くのサブタスクが生成され、その結果、多くの RPC 要求が生成され、余分な時間がかかります。v6.6.0 以降、TiDB は同じ TiKV インスタンスに送信されるデータ要求の部分的なマージをサポートし、サブタスクの数と RPC 要求のオーバーヘッドを削減します。データの分散が大きく、gRPC スレッド プールのリソースが不足している場合は、要求をバッチ処理することでパフォーマンスを 50% 以上向上させることができます。

    この機能はデフォルトで有効になっています。システム変数[`tidb_store_batch_size`](/system-variables.md#tidb_store_batch_size)を使用して、リクエストのバッチサイズを設定できます。

-   `LIMIT`節[＃40219](https://github.com/pingcap/tidb/issues/40219) @ [fzzf678](https://github.com/fzzf678)の制限を削除します

    v6.6.0以降、TiDBプランキャッシュは、 `LIMIT`パラメータに`LIMIT ?`や`LIMIT 10, ?`などの変数を指定した実行プランのキャッシュをサポートします。この機能により、より多くのSQL文がプランキャッシュの恩恵を受けられるようになり、実行効率が向上します。現在、セキュリティ上の配慮から、TiDBは`?`が10000以下の実行プランのみをキャッシュできます。

    詳細については[ドキュメント](/sql-prepared-plan-cache.md)参照してください。

-   TiFlashは圧縮[＃6620](https://github.com/pingcap/tiflash/issues/6620) @ [ソロツグ](https://github.com/solotzg)によるデータ交換をサポート

    TiFlashエンジンは、複数のノードと連携して計算を行うために、異なるノード間でデータを交換する必要があります。交換するデータのサイズが非常に大きい場合、データ交換のパフォーマンスが全体の計算効率に影響を与える可能性があります。v6.6.0では、 TiFlashエンジンに圧縮メカニズムが導入され、交換が必要なデータを必要に応じて圧縮してから交換することで、データ交換の効率が向上しました。

    詳細については[ドキュメント](/explain-mpp.md#mpp-version-and-exchange-data-compression)参照してください。

-   TiFlashはステイル読み取り機能[＃4483](https://github.com/pingcap/tiflash/issues/4483) @ [ヘヘチェン](https://github.com/hehechen)をサポートしています

    ステイル読み取り機能はv5.1.1から一般提供（GA）されており、特定のタイムスタンプまたは指定した期間内の履歴データを読み取ることができます。Stale Readは、ローカルTiKVレプリカから直接データを読み取ることで、読み取りレイテンシーを短縮し、クエリパフォーマンスを向上させます。v6.6.0より前のバージョンでは、 TiFlashはステイル読み取りをサポートしていません。テーブルにTiFlashレプリカが存在する場合でも、 ステイル読み取りはTiKVレプリカのみを読み取ることができます。

    v6.6.0以降、 TiFlashはステイル読み取り機能をサポートします。1 [`AS OF TIMESTAMP`](/as-of-timestamp.md)構文または[`tidb_read_staleness`](/tidb-read-staleness.md)のシステム変数を使用してテーブルの履歴データをクエリする際、テーブルにTiFlashレプリカが存在する場合、オプティマイザーは対応するデータをTiFlashレプリカから読み取ることを選択できるようになりました。これにより、クエリパフォーマンスがさらに向上します。

    詳細については[ドキュメント](/stale-read.md)参照してください。

-   `regexp_replace`文字列機能をTiFlash [＃6115](https://github.com/pingcap/tiflash/issues/6115) @ [xzhangxian1008](https://github.com/xzhangxian1008)にプッシュダウンする機能をサポート

### 信頼性 {#reliability}

-   リソース グループに基づくリソース制御のサポート (実験的) [＃38825](https://github.com/pingcap/tidb/issues/38825) @ [ノルーシュ](https://github.com/nolouch) @ [生まれ変わった人](https://github.com/BornChanger) @ [栄光](https://github.com/glorv) @ [天菜麻緒](https://github.com/tiancaiamao) @ [コナー1996](https://github.com/Connor1996) @ [Jmポテト](https://github.com/JmPotato) @ [ネス](https://github.com/hnes) @ [キャビンフィーバーB](https://github.com/CabinfeverB) @ [HuSharp](https://github.com/HuSharp)

    TiDBクラスターのリソースグループを作成し、異なるデータベースユーザーを対応するリソースグループにバインドし、実際のニーズに応じて各リソースグループのクォータを設定できるようになりました。クラスターリソースが制限されている場合、同じリソースグループ内のセッションで使用されるすべてのリソースはクォータに制限されます。これにより、あるリソースグループが過剰に消費されても、他のリソースグループのセッションには影響しません。TiDBは、Grafanaダッシュボードにリソースの実際の使用状況を表示する組み込みビューを提供し、より合理的なリソース割り当てを支援します。

    リソース制御機能の導入は、TiDBにとって画期的な出来事です。この機能により、分散データベースクラスタを複数の論理ユニットに分割できます。個々のユニットがリソースを過剰に使用しても、他のユニットに必要なリソースが圧迫されることはありません。

    この機能を使用すると、次のことが可能になります。

    -   複数の異なるシステムから複数の中小規模アプリケーションを単一のTiDBクラスタに統合します。あるアプリケーションのワークロードが増加しても、他のアプリケーションの正常な動作に影響を与えることはありません。システムのワークロードが低い場合は、設定された読み取り/書き込みクォータを超えても、高負荷のアプリケーションに必要なシステムリソースを割り当てることができるため、リソースを最大限に活用できます。
    -   すべてのテスト環境を単一のTiDBクラスターに統合するか、リソースを多く消費するバッチタスクを単一のリソースグループにまとめるかを選択できます。これにより、ハードウェア使用率を向上させ、運用コストを削減しながら、重要なアプリケーションに必要なリソースを常に確保できます。

    さらに、リソース制御機能を合理的に使用すると、クラスターの数を削減し、運用と保守の難易度を軽減し、管理コストを節約できます。

    v6.6では、リソース制御を有効にするには、TiDBのグローバル変数[`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-new-in-v660)とTiKV設定項目[`resource-control.enabled`](/tikv-configuration-file.md#resource-control)両方を有効にする必要があります。現在サポートされているクォータ方式は「 [リクエストユニット（RU）](/tidb-resource-control-ru-groups.md#what-is-request-unit-ru) 」に基づいています。RUは、CPUやIOなどのシステムリソースに対するTiDBの統一抽象化単位です。

    詳細については[ドキュメント](/tidb-resource-control-ru-groups.md)参照してください。

-   過去の実行計画のバインドは GA [＃39199](https://github.com/pingcap/tidb/issues/39199) @ [fzzf678](https://github.com/fzzf678)です

    v6.5.0では、TiDBは[`CREATE [GLOBAL | SESSION] BINDING`](/sql-statements/sql-statement-create-binding.md)ステートメントのバインディングターゲットを拡張し、過去の実行プランに基づいたバインディングの作成をサポートします。v6.6.0では、この機能がGAになりました。実行プランの選択は現在のTiDBノードに限定されません。任意のTiDBノードによって生成された過去の実行プランを[SQLバインディング](/sql-statements/sql-statement-create-binding.md)のターゲットとして選択できるため、機能の使いやすさがさらに向上します。

    詳細については[ドキュメント](/sql-plan-management.md#create-a-binding-according-to-a-historical-execution-plan)参照してください。

-   いくつかのオプティマイザヒント[＃39964](https://github.com/pingcap/tidb/issues/39964) @ [思い出させる](https://github.com/Reminiscent)を追加します

    TiDB は、v6.6.0 で、 `LIMIT`操作の実行プランの選択を制御するためのいくつかのオプティマイザーヒントを追加しました。

    -   [`ORDER_INDEX()`](/optimizer-hints.md#order_indext1_name-idx1_name--idx2_name-) : 指定されたインデックスを使用し、データの読み取り時にインデックスの順序を維持するようにオプティマイザに指示し、 `Limit + IndexScan(keep order: true)`と同様のプランを生成します。
    -   [`NO_ORDER_INDEX()`](/optimizer-hints.md#no_order_indext1_name-idx1_name--idx2_name-) : データの読み取り時にインデックスの順序を保持せず、指定されたインデックスを使用するようにオプティマイザに指示し、 `TopN + IndexScan(keep order: false)`と同様のプランを生成します。

    オプティマイザーヒントを継続的に導入することで、ユーザーにさらに多くの介入方法が提供され、SQL パフォーマンスの問題が解決され、全体的なパフォーマンスの安定性が向上します。

-   DDL 操作のリソース使用量の動的管理をサポート (実験的) [＃38025](https://github.com/pingcap/tidb/issues/38025) @ [ホーキングレイ](https://github.com/hawkingrei)

    TiDB v6.6.0では、DDL操作のリソース管理が導入され、これらの操作のCPU使用率を自動的に制御することで、DDL変更がオンラインアプリケーションに与える影響を軽減します。この機能は、 [DDL分散並列実行フレームワーク](https://docs.pingcap.com/tidb/v6.6/system-variables#tidb_ddl_distribute_reorg-new-in-v660)有効になっている場合にのみ有効になります。

### 可用性 {#availability}

-   `SURVIVAL_PREFERENCE`対[SQLの配置ルール](/placement-rules-in-sql.md) [＃38605](https://github.com/pingcap/tidb/issues/38605) [ノルーシュ](https://github.com/nolouch)の構成をサポート

    `SURVIVAL_PREFERENCES` `SURVIVAL_PREFERENCE`指定すると、データの災害時における生存性を高めるためのデータ生存設定が提供されます。2 を指定すると、以下の項目を制御できます。

    -   クラウド リージョン全体に展開された TiDB クラスターの場合、1 つのクラウド リージョンに障害が発生しても、指定されたデータベースまたはテーブルは別のクラウド リージョンで存続できます。
    -   単一のクラウド リージョンにデプロイされた TiDB クラスターの場合、アベイラビリティ ゾーンで障害が発生しても、指定されたデータベースまたはテーブルは別のアベイラビリティ ゾーンで存続できます。

    詳細については[ドキュメント](/placement-rules-in-sql.md#specify-survival-preferences)参照してください。

-   `FLASHBACK CLUSTER TO TIMESTAMP`文[＃14045](https://github.com/tikv/tikv/issues/14045) @ [定義2014](https://github.com/Defined2014) @ [Jmポテト](https://github.com/JmPotato)による DDL 操作のロールバックをサポート

    [`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-cluster.md)ステートメントは、ガベージコレクション（GC）の有効期間内の特定の時点にクラスタ全体を復元することをサポートします。TiDB v6.6.0 では、この機能に DDL 操作のロールバックのサポートが追加されました。これにより、クラスタ上の DML または DDL 操作の誤りを迅速に元に戻したり、数分以内にクラスタをロールバックしたり、特定のデータ変更がいつ発生したかを特定するためにタイムライン上でクラスタを複数回ロールバックしたりできます。

    詳細については[ドキュメント](/sql-statements/sql-statement-flashback-cluster.md)参照してください。

### SQL {#sql}

-   MySQL互換の外部キー制約をサポート（実験的） [＃18209](https://github.com/pingcap/tidb/issues/18209) @ [crazycs520](https://github.com/crazycs520)

    TiDB v6.6.0では、MySQLと互換性のある外部キー制約機能が導入されました。この機能は、テーブル内またはテーブル間の参照、制約の検証、カスケード操作をサポートします。この機能は、アプリケーションのTiDBへの移行、データの一貫性の維持、データ品質の向上、そしてデータモデリングの容易化に役立ちます。

    詳細については[ドキュメント](/foreign-key.md)参照してください。

-   MySQL互換のマルチ値インデックスをサポート（実験的） [＃39592](https://github.com/pingcap/tidb/issues/39592) @ [ションジウェイ](https://github.com/xiongjiwei) @ [qw4990](https://github.com/qw4990)

    TiDBはv6.6.0でMySQL互換の多値インデックスを導入しました。JSON列内の配列の値をフィルタリングすることは一般的な操作ですが、通常のインデックスではこのような操作を高速化できません。配列に多値インデックスを作成すると、フィルタリングのパフォーマンスが大幅に向上します。JSON列の配列に多値インデックスがある場合、多値インデックスを使用して`MEMBER OF()` `JSON_CONTAINS()` `JSON_OVERLAPS()`で検索条件をフィルタリングすることで、I/O消費を大幅に削減し、操作速度を向上させる関数ができます。

    複数値インデックスの導入により、TiDB の JSON データ型のサポートがさらに強化され、TiDB と MySQL 8.0 の互換性も向上します。

    詳細については[ドキュメント](/sql-statements/sql-statement-create-index.md#multi-valued-indexes)参照してください。

### DB操作 {#db-operations}

-   リソースを消費するタスク用の読み取り専用storageノードの構成をサポート @ [v01dスター](https://github.com/v01dstar)

    本番環境では、バックアップや大規模データの読み取り・分析など、一部の読み取り専用操作は定期的に大量のリソースを消費し、クラスター全体のパフォーマンスに影響を与える可能性があります。TiDB v6.6.0では、リソースを消費する読み取り専用タスク用に読み取り専用storageノードを構成することで、オンラインアプリケーションへの影響を軽減しています。現在、TiDB、TiSpark、 BRは読み取り専用storageノードからのデータの読み取りをサポートしています[手順](/best-practices/readonly-nodes.md#procedures)に従って読み取り専用storageノードを構成し、システム変数`tidb_replica_read` 、TiSpark設定項目`spark.tispark.replica_read` 、またはbrコマンドライン引数`--replica-read-label`を介してデータの読み取り先を指定することで、クラスターのパフォーマンスの安定性を確保できます。

    詳細については[ドキュメント](/best-practices/readonly-nodes.md)参照してください。

-   `store-io-pool-size` [＃13964](https://github.com/tikv/tikv/issues/13964) @ [LykxSassinator](https://github.com/LykxSassinator)の動的変更をサポート

    TiKV設定項目[`raftstore.store-io-pool-size`](/tikv-configuration-file.md#store-io-pool-size-new-in-v530) 、 Raft I/Oタスクを処理するスレッドの許容数を指定します。この数は、TiKVパフォーマンスのチューニング時に調整できます。v6.6.0より前では、この設定項目を動的に変更することはできませんでした。v6.6.0以降では、サーバーを再起動せずにこの設定を変更できるため、より柔軟なパフォーマンスチューニングが可能になります。

    詳細については[ドキュメント](/dynamic-config.md)参照してください。

-   TiDB クラスタの初期化時に実行される SQL スクリプトの指定をサポート[＃35624](https://github.com/pingcap/tidb/issues/35624) @ [モルゴ](https://github.com/morgo)

    TiDBクラスタを初めて起動する際に、コマンドラインパラメータ`--initialize-sql-file`を設定することで、実行するSQLスクリプトを指定できます。この機能は、システム変数の値の変更、ユーザーの作成、権限の付与などの操作を行う際に使用できます。

    詳細については[ドキュメント](/tidb-configuration-file.md#initialize-sql-file-new-in-v660)参照してください。

-   TiDBデータ移行（DM）は、TiDB Lightningの物理インポートモードと統合され、完全な移行（実験的）で最大10倍のパフォーマンス向上を実現します[ランス6716](https://github.com/lance6716)

    v6.6.0 では、DM の完全移行機能がTiDB Lightningの物理インポート モードと統合され、DM は完全データ移行のパフォーマンスを最大 10 倍向上させ、大容量データ シナリオでの移行時間を大幅に短縮できるようになりました。

    v6.6.0より前のバージョンでは、大容量データを扱うシナリオでは、高速なフルデータ移行のためにTiDB Lightningで物理インポートタスクを別途設定し、その後DMを使用して増分データ移行を行う必要があり、設定が複雑でした。v6.6.0以降では、 TiDB Lightningタスクを設定することなく大容量データを移行でき、1つのDMタスクで移行を完了できます。

    詳細については[ドキュメント](/dm/dm-precheck.md#check-items-for-physical-import)参照してください。

-   TiDB Lightningは、ソースファイルとターゲットテーブル間の列名の不一致の問題に対処するために、新しい構成パラメータ`"header-schema-match"`を追加しました@ [dsdashun](https://github.com/dsdashun)

    v6.6.0では、 TiDB Lightningに新しいプロファイルパラメータ`"header-schema-match"`が追加されました。デフォルト値は`true`で、これはソースCSVファイルの最初の行が列名として扱われ、ターゲットテーブルの列名と一致していることを意味します。CSVテーブルヘッダーのフィールド名がターゲットテーブルの列名と一致しない場合は、この設定を`false`に設定できます。TiDB TiDB Lightningはエラーを無視し、ターゲットテーブルの列順にデータをインポートし続けます。

    詳細については[ドキュメント](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)参照してください。

-   TiDB Lightningは、 TiKV [＃41163](https://github.com/pingcap/tidb/issues/41163) @ [眠そうなモグラ](https://github.com/sleepymole)にキーと値のペアを送信するときに圧縮転送を有効にすることをサポートします。

    v6.6.0以降、 TiDB Lightningは、ローカルでエンコードおよびソートされたキーと値のペアをTiKVに送信する際に、ネットワーク転送用に圧縮することをサポートします。これにより、ネットワーク経由で転送されるデータ量が削減され、ネットワーク帯域幅のオーバーヘッドが低減されます。この機能がサポートされる以前のTiDBバージョンでは、 TiDB Lightningは比較的高いネットワーク帯域幅を必要とし、大量のデータを扱う場合には高額なトラフィック料金が発生していました。

    この機能はデフォルトで無効になっています。有効にするには、 TiDB Lightningの`compress-kv-pairs`設定項目を`"gzip"`または`"gz"`に設定してください。

    詳細については[ドキュメント](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)参照してください。

-   TiKV-CDCツールがGAとなり、RawKV [＃48](https://github.com/tikv/migration/issues/48) @ [沢民州](https://github.com/zeminzhou) @ [ハオジンミン](https://github.com/haojinming) @ [ピンギュ](https://github.com/pingyu)のデータ変更のサブスクライブをサポートするようになりました。

    TiKV-CDCは、TiKVクラスター用のCDC（変更データキャプチャ）ツールです。TiKVとPDは、TiDBなしで使用することでRawKVと呼ばれるKVデータベースを構成できます。TiKV-CDCは、RawKVのデータ変更をサブスクライブし、下流のTiKVクラスターにリアルタイムで複製することで、RawKVのクラスター間レプリケーションを可能にします。

    詳細については[ドキュメント](https://tikv.org/docs/latest/concepts/explore-tikv-features/cdc/cdc/)参照してください。

-   TiCDC は、Kafka の変更フィード上の単一のテーブルのスケールアウトと、変更フィードを複数の TiCDC ノードに分散することをサポートします (実験的) [＃7720](https://github.com/pingcap/tiflow/issues/7720) @ [金星の上](https://github.com/overvenus)

    バージョン6.6.0より前のバージョンでは、アップストリームテーブルが大量の書き込みを受け入れる場合、そのテーブルのレプリケーション機能をスケールアウトすることができず、レプリケーションレイテンシーが増加していました。TiCDCバージョン6.6.0以降では、アップストリームテーブルの変更フィードをKafkaシンク内の複数のTiCDCノードに分散できるようになり、単一テーブルのレプリケーション機能がスケールアウトされます。

    詳細については[ドキュメント](/ticdc/ticdc-sink-to-kafka.md#scale-out-the-load-of-a-single-large-table-to-multiple-ticdc-nodes)参照してください。

-   [ゴーム](https://github.com/go-gorm/gorm)ではTiDB統合テストが追加されました。これにより、TiDBがGORMでサポートされるデフォルトのデータベースになりました[＃6014](https://github.com/go-gorm/gorm/pull/6014) @ [アイスマップ](https://github.com/Icemap)

    -   v1.4.6では、 [GORM MySQLドライバ](https://github.com/go-gorm/mysql) TiDB [＃104](https://github.com/go-gorm/mysql/pull/104)の`AUTO_RANDOM`属性に適応します。
    -   v1.4.6では、TiDBに接続するときに、 `Unique`フィールドの`Unique`属性が`AutoMigrate` [＃105](https://github.com/go-gorm/mysql/pull/105)中に変更できないという問題が修正されました[GORM MySQLドライバ](https://github.com/go-gorm/mysql)
    -   [GORMドキュメント](https://github.com/go-gorm/gorm.io)デフォルトのデータベースとして TiDB を挙げています[＃638](https://github.com/go-gorm/gorm.io/pull/638)

    詳細については[GORMドキュメント](https://gorm.io/docs/index.html)参照してください。

### 可観測性 {#observability}

-   TiDBダッシュボード[＃781](https://github.com/pingcap/tidb-dashboard/issues/781) @ [イニシュ9506](https://github.com/YiniXu9506)でSQLバインディングを素早く作成するサポート

    TiDB v6.6.0 は、ステートメント履歴からの SQL バインディングの作成をサポートしており、これにより、TiDB ダッシュボード上の特定のプランに SQL ステートメントをすばやくバインドできます。

    この機能は、ユーザーフレンドリーなインターフェースを提供することで、TiDB でのプランのバインドのプロセスを簡素化し、操作の複雑さを軽減し、プランのバインド プロセスの効率とユーザー エクスペリエンスを向上させます。

    詳細については[ドキュメント](/dashboard/dashboard-statement-details.md#fast-plan-binding)参照してください。

-   実行プランのキャッシュに関する警告を[qw4990](https://github.com/qw4990)に追加

    実行計画をキャッシュできない場合、TiDBは診断を容易にするために警告でその理由を表示します。例:

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

    上記の例では、オプティマイザが INT 以外の型を INT 型に変換し、パラメータの変更に伴って実行プランが変わる可能性があるため、TiDB はプランをキャッシュしません。

    詳細については[ドキュメント](/sql-prepared-plan-cache.md#diagnostics-of-prepared-plan-cache)参照してください。

-   スロークエリログ[＃39893](https://github.com/pingcap/tidb/issues/39893) @ [時間と運命](https://github.com/time-and-fate)に`Warnings`フィールドを追加します

    TiDB v6.6.0では、パフォーマンスの問題の診断を支援するため、スロークエリログに`Warnings`フィールドが追加されました。このフィールドには、スロークエリの実行中に生成された警告が記録されます。これらの警告は、TiDBダッシュボードのスロークエリページでも確認できます。

    詳細については[ドキュメント](/identify-slow-queries.md)参照してください。

-   SQL実行プラン[＃38779](https://github.com/pingcap/tidb/issues/38779) @ [イーサール](https://github.com/Yisaer)の生成を自動的にキャプチャします

    実行計画の問題をトラブルシューティングするプロセスにおいて、 `PLAN REPLAYER`状況を保存し、診断の効率を向上させるのに役立ちます。ただし、シナリオによっては、一部の実行計画の生成を自由に再現できないため、診断作業が困難になる場合があります。

    このような問題に対処するため、TiDB v6.6.0では、 `PLAN REPLAYER`自動キャプチャ機能が拡張されました。3 `PLAN REPLAYER CAPTURE`を使用すると、対象のSQL文を事前に登録し、同時に対象の実行プランを指定できます。TiDBは、登録された対象に一致するSQL文または実行プランを検出すると、 `PLAN REPLAYER`情報を自動的に生成してパッケージ化します。実行プランが不安定な場合、この機能により診断効率が向上します。

    この機能を使用するには、 [`tidb_enable_plan_replayer_capture`](/system-variables.md#tidb_enable_plan_replayer_capture)の値を`ON`に設定します。

    詳細については[ドキュメント](/sql-plan-replayer.md#use-plan-replayer-capture)参照してください。

-   永続的なステートメントのサポートの概要（実験的） [＃40812](https://github.com/pingcap/tidb/issues/40812) @ [モーニクス](https://github.com/mornyx)

    v6.6.0より前では、ステートメントサマリーデータはメモリに保存されており、TiDBサーバーの再起動時に失われていました。v6.6.0以降、TiDBはステートメントサマリーの永続化をサポートし、履歴データを定期的にディスクに書き込むことができます。それまでの間、システムテーブルに対するクエリの結果はメモリではなくディスクから取得されます。TiDBの再起動後も、すべての履歴データは引き続き利用可能です。

    詳細については[ドキュメント](/statement-summary-tables.md#persist-statements-summary)参照してください。

### Security {#security}

-   TiFlashはTLS証明書[＃5503](https://github.com/pingcap/tiflash/issues/5503) @ [ywqzzy](https://github.com/ywqzzy)の自動ローテーションをサポートします

    v6.6.0では、TiDBはTiFlash TLS証明書の自動ローテーションをサポートします。コンポーネント間の暗号化データ転送が有効になっているTiDBクラスタでは、 TiFlashのTLS証明書の有効期限が切れて新しい証明書を再発行する必要がある場合、TiDBクラスタを再起動することなく、新しいTiFlash TLS証明書を自動的にロードできます。さらに、TiDBクラスタ内のコンポーネント間でのTLS証明書のローテーションは、TiDBクラスタの使用に影響を与えないため、クラスタの高可用性が確保されます。

    詳細については[ドキュメント](/enable-tls-between-components.md)参照してください。

-   TiDB LightningはAWS IAMロールキーとセッショントークン[＃40750](https://github.com/pingcap/tidb/issues/40750) @ [okJiang](https://github.com/okJiang)を介してAmazon S3データへのアクセスをサポートします

    v6.6.0より前のバージョンでは、 TiDB LightningはAWS IAM**ユーザーのアクセスキー**（各アクセスキーはアクセスキーIDとシークレットアクセスキーで構成されています）を介したS3データへのアクセスのみをサポートしていたため、一時的なセッショントークンを使用してS3データにアクセスすることはできませんでした。v6.6.0以降、 TiDB LightningはAWS IAM**ロールのアクセスキーとセッショントークンを**介したS3データへのアクセスもサポートし、データセキュリティを強化しました。

    詳細については[ドキュメント](/tidb-lightning/tidb-lightning-data-source.md#import-data-from-amazon-s3)参照してください。

### テレメトリー {#telemetry}

-   2023年2月20日以降、TiDBおよびTiDB Dashboardの新しいバージョン（v6.6.0を含む）では、 [テレメトリ機能](/telemetry.md)がデフォルトで無効化されます。デフォルトのテレメトリ設定を使用している以前のバージョンからアップグレードした場合、アップグレード後にテレメトリ機能は無効化されます。具体的なバージョンについては、 [TiDB リリース タイムライン](/releases/release-timeline.md)ご覧ください。
-   v1.11.3 以降、新規に導入されたTiUPではテレメトリ機能がデフォルトで無効化されます。以前のバージョンのTiUPから v1.11.3 以降にアップグレードした場合、テレメトリ機能はアップグレード前と同じ状態を維持します。

## 互換性の変更 {#compatibility-changes}

> **注記：**
>
> このセクションでは、v6.5.0から最新バージョン（v6.6.0）にアップグレードする際に知っておくべき互換性の変更点について説明します。v6.4.0以前のバージョンから最新バージョンにアップグレードする場合は、中間バージョンで導入された互換性の変更点も確認する必要があるかもしれません。

### MySQLの互換性 {#mysql-compatibility}

-   MySQL互換の外部キー制約をサポート（実験的） [＃18209](https://github.com/pingcap/tidb/issues/18209) @ [crazycs520](https://github.com/crazycs520)

    詳細については、このドキュメントの[SQL](#sql)セクションと[ドキュメント](/foreign-key.md)参照してください。

-   MySQL互換のマルチ値インデックスをサポート（実験的） [＃39592](https://github.com/pingcap/tidb/issues/39592) @ [ションジウェイ](https://github.com/xiongjiwei) @ [qw4990](https://github.com/qw4990)

    詳細については、このドキュメントの[SQL](#sql)セクションと[ドキュメント](/sql-statements/sql-statement-create-index.md#multi-valued-indexes)参照してください。

### システム変数 {#system-variables}

| 変数名                                                                                                                                                  | タイプを変更   | 説明                                                                                                                                                                                                                                                            |
| ---------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `tidb_enable_amend_pessimistic_txn`                                                                                                                  | 削除済み     | v6.5.0以降、この変数は非推奨となりました。v6.6.0以降、この変数と`AMEND TRANSACTION`機能は削除されました。TiDBは`Information schema is changed`エラーを回避するために[メタロック](/metadata-lock.md)使用します。                                                                                                           |
| `tidb_enable_concurrent_ddl`                                                                                                                         | 削除済み     | この変数は、TiDBが同時実行DDL文の使用を許可するかどうかを制御します。この変数が無効になっている場合、TiDBは同時実行DDL文のサポートが限定的な古いDDL実行フレームワークを使用します。v6.6.0以降、この変数は削除され、TiDBは古いDDL実行フレームワークをサポートしなくなります。                                                                                                         |
| `tidb_ttl_job_run_interval`                                                                                                                          | 削除済み     | この変数は、バックグラウンドでのTTLジョブのスケジュール間隔を制御するために使用されます。v6.6.0以降、TiDBはすべてのテーブルにTTL実行時間を制御するための属性として`TTL_JOB_INTERVAL`を提供しており、これは`tidb_ttl_job_run_interval`よりも柔軟性が高いため、この変数は削除されました。                                                                                    |
| [`foreign_key_checks`](/system-variables.md#foreign_key_checks)                                                                                      | 修正済み     | この変数は、外部キー制約チェックを有効にするかどうかを制御します。デフォルト値は`OFF`から`ON`に変更され、これは外部キーチェックがデフォルトで有効になることを意味します。                                                                                                                                                                     |
| [`tidb_enable_foreign_key`](/system-variables.md#tidb_enable_foreign_key-new-in-v630)                                                                | 修正済み     | この変数は、外部キー機能を有効にするかどうかを制御します。デフォルト値は`OFF`から`ON`に変更され、デフォルトで外部キーが有効になります。                                                                                                                                                                                      |
| `tidb_enable_general_plan_cache`                                                                                                                     | 修正済み     | この変数は、一般プランキャッシュを有効にするかどうかを制御します。v6.6.0以降、この変数の名前は[`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache)に変更されます。                                                                                                   |
| [`tidb_enable_historical_stats`](/system-variables.md#tidb_enable_historical_stats)                                                                  | 修正済み     | この変数は、履歴統計を有効にするかどうかを制御します。デフォルト値は`OFF`から`ON`に変更され、履歴統計がデフォルトで有効になります。                                                                                                                                                                                        |
| [`tidb_enable_plan_replayer_capture`](/system-variables.md#tidb_enable_plan_replayer_capture)                                                        | 修正済み     | この変数はバージョン6.6.0以降で有効になり、 [`PLAN REPLAYER CAPTURE`機能](/sql-plan-replayer.md#use-plan-replayer-capture-to-capture-target-plans)を有効にするかどうかを制御します。デフォルト値は`OFF`から`ON`に変更され、これは`PLAN REPLAYER CAPTURE`機能がデフォルトで有効であることを意味します。                                       |
| [`tidb_enable_telemetry`](/system-variables.md#tidb_enable_telemetry-new-in-v402)                                                                    | 修正済み     | デフォルト値は`ON`から`OFF`に変更されます。これは、TiDB でテレメトリがデフォルトで無効になっていることを意味します。                                                                                                                                                                                             |
| `tidb_general_plan_cache_size`                                                                                                                       | 修正済み     | この変数は、一般プランキャッシュによってキャッシュできる実行プランの最大数を制御します。v6.6.0以降、この変数の名前は[`tidb_non_prepared_plan_cache_size`](/system-variables.md#tidb_non_prepared_plan_cache_size)に変更されます。                                                                                            |
| [`tidb_replica_read`](/system-variables.md#tidb_replica_read-new-in-v40)                                                                             | 修正済み     | この変数には、TiDB が読み取り専用ノードからデータを読み取るときに使用する学習者レプリカを指定するための新しい値オプション`learner`が追加されました。                                                                                                                                                                             |
| [`tidb_replica_read`](/system-variables.md#tidb_replica_read-new-in-v40)                                                                             | 修正済み     | TiDBクラスタ全体の読み取り可用性を向上させるため、この変数に新しい値オプション`prefer-leader`が追加されました。このオプションを設定すると、TiDBはリーダーレプリカからの読み取りを優先します。リーダーレプリカのパフォーマンスが大幅に低下した場合、TiDBは自動的にフォロワーレプリカからの読み取りに移行します。                                                                                         |
| [`tidb_store_batch_size`](/system-variables.md#tidb_store_batch_size)                                                                                | 修正済み     | この変数は、 `IndexLookUp`オペレータのコプロセッサータスクのバッチサイズを制御します。3 `0`バッチを無効にすることを意味します。v6.6.0以降、デフォルト値は`0`から`4`に変更され、リクエストのバッチごとに4つのコプロセッサータスクが1つのタスクにバッチ処理されるようになりました。                                                                                                     |
| [`mpp_exchange_compression_mode`](/system-variables.md#mpp_exchange_compression_mode-new-in-v660)                                                    | 新しく追加された | この変数は、MPP Exchange演算子のデータ圧縮モードを指定します。TiDBがバージョン番号`1`のMPP実行プランを選択した場合に有効になります。デフォルト値`UNSPECIFIED` 、TiDBが自動的にバージョン番号`FAST`圧縮モードを選択することを意味します。                                                                                                                   |
| [`mpp_version`](/system-variables.md#mpp_version-new-in-v660)                                                                                        | 新しく追加された | この変数は、MPP実行プランのバージョンを指定します。バージョンが指定されると、TiDBは指定されたバージョンのMPP実行プランを選択します。デフォルト値`UNSPECIFIED` 、TiDBが最新のバージョン`1`を自動的に選択することを意味します。                                                                                                                                |
| [`tidb_ddl_distribute_reorg`](https://docs.pingcap.com/tidb/v6.6/system-variables#tidb_ddl_distribute_reorg-new-in-v660)                             | 新しく追加された | この変数は、DDL再編成フェーズの分散実行を有効にしてこのフェーズを高速化するかどうかを制御します。デフォルト値`OFF` 、DDL再編成フェーズの分散実行をデフォルトで有効にしないことを意味します。現在、この変数は`ADD INDEX`場合にのみ有効です。                                                                                                                             |
| [`tidb_enable_historical_stats_for_capture`](/system-variables.md#tidb_enable_historical_stats_for_capture)                                          | 新しく追加された | この変数は、 `PLAN REPLAYER CAPTURE`で取得される情報にデフォルトで履歴統計情報が含まれるかどうかを制御します。デフォルト値`OFF`は、履歴統計情報がデフォルトで含まれないことを意味します。                                                                                                                                                   |
| [`tidb_enable_plan_cache_for_param_limit`](/system-variables.md#tidb_enable_plan_cache_for_param_limit-new-in-v660)                                  | 新しく追加された | この変数は、プリペアドプランキャッシュ が`Limit`後に`COUNT`含む実行プランをキャッシュするかどうかを制御します。デフォルト値は`ON`で、 プリペアドプランキャッシュ がそのような実行プランのキャッシュをサポートすることを意味します。Prepared プリペアドプランキャッシュ は、 10000を超える数値をカウントする`COUNT`条件を含む実行プランのキャッシュをサポートしないことに注意してください。                                           |
| [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-new-in-v660)                                                      | 新しく追加された | この変数は、リソース制御機能を有効にするかどうかを制御します。デフォルト値は`OFF`です。この変数を`ON`に設定すると、TiDB クラスターはリソースグループに基づいてアプリケーションのリソース分離をサポートします。                                                                                                                                                |
| [`tidb_historical_stats_duration`](/system-variables.md#tidb_historical_stats_duration-new-in-v660)                                                  | 新しく追加された | この変数は、履歴統計をstorageに保持する期間を制御します。デフォルト値は7日間です。                                                                                                                                                                                                                 |
| [`tidb_index_join_double_read_penalty_cost_rate`](/system-variables.md#tidb_index_join_double_read_penalty_cost_rate-new-in-v660)                    | 新しく追加された | この変数は、インデックス結合の選択にペナルティコストを追加するかどうかを制御します。デフォルト値`0`は、この機能がデフォルトで無効であることを意味します。                                                                                                                                                                                |
| [`tidb_pessimistic_txn_aggressive_locking`](https://docs.pingcap.com/tidb/v6.6/system-variables#tidb_pessimistic_txn_aggressive_locking-new-in-v660) | 新しく追加された | この変数は、悲観的トランザクションにおいて拡張悲観的ロック・ウェイクアップ・モデルを使用するかどうかを制御します。デフォルト値`OFF`は、悲観的トランザクションにおいてこのウェイクアップ・モデルをデフォルトで使用しないことを意味します。                                                                                                                                       |
| [`tidb_stmt_summary_enable_persistent`](/system-variables.md#tidb_stmt_summary_enable_persistent-new-in-v660)                                        | 新しく追加された | この変数は読み取り専用です。1 [ステートメントの概要の永続性](/statement-summary-tables.md#persist-statements-summary)有効にするかどうかを制御します。この変数の値は、設定項目[`tidb_stmt_summary_enable_persistent`](/tidb-configuration-file.md#tidb_stmt_summary_enable_persistent-new-in-v660)の値と同じです。             |
| [`tidb_stmt_summary_filename`](/system-variables.md#tidb_stmt_summary_filename-new-in-v660)                                                          | 新しく追加された | この変数は読み取り専用です。1 [ステートメントの概要の永続性](/statement-summary-tables.md#persist-statements-summary)有効な場合に永続データが書き込まれるファイルを指定します。この変数の値は、設定項目[`tidb_stmt_summary_filename`](/tidb-configuration-file.md#tidb_stmt_summary_filename-new-in-v660)の値と同じです。                  |
| [`tidb_stmt_summary_file_max_backups`](/system-variables.md#tidb_stmt_summary_file_max_backups-new-in-v660)                                          | 新しく追加された | この変数は読み取り専用です。1 [ステートメントの概要の永続性](/statement-summary-tables.md#persist-statements-summary)有効な場合に、保存できるデータファイルの最大数を指定します。この変数の値は、設定項目[`tidb_stmt_summary_file_max_backups`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_backups-new-in-v660)の値と同じです。 |
| [`tidb_stmt_summary_file_max_days`](/system-variables.md#tidb_stmt_summary_file_max_days-new-in-v660)                                                | 新しく追加された | この変数は読み取り専用です。1 [ステートメントの概要の永続性](/statement-summary-tables.md#persist-statements-summary)有効な場合に、永続データファイルを保持する最大日数を指定します。この変数の値は、設定項目[`tidb_stmt_summary_file_max_days`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_days-new-in-v660)の値と同じです。     |
| [`tidb_stmt_summary_file_max_size`](/system-variables.md#tidb_stmt_summary_file_max_size-new-in-v660)                                                | 新しく追加された | この変数は読み取り専用です。1 [ステートメントの概要の永続性](/statement-summary-tables.md#persist-statements-summary)有効な場合、永続データファイルの最大サイズを指定します。この変数の値は、設定項目[`tidb_stmt_summary_file_max_size`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_size-new-in-v660)の値と同じです。         |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーションパラメータ                                                                                                                                                                                                                                           | タイプを変更   | 説明                                                                                                                                                                                     |
| -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiKV           | `rocksdb.enable-statistics`                                                                                                                                                                                                                               | 削除済み     | この設定項目は、RocksDB統計を有効にするかどうかを指定します。v6.6.0以降、この項目は削除されました。RocksDB統計は、診断を支援するために、すべてのクラスターでデフォルトで有効になっています。詳細については、 [＃13942](https://github.com/tikv/tikv/pull/13942)参照してください。            |
| TiKV           | `raftdb.enable-statistics`                                                                                                                                                                                                                                | 削除済み     | この設定項目は、 Raft RocksDB統計を有効にするかどうかを指定します。v6.6.0以降、この項目は削除されました。Raft RocksDB統計は、診断を容易にするため、すべてのクラスターでデフォルトで有効になっています。詳細については、 [＃13942](https://github.com/tikv/tikv/pull/13942)参照してください。 |
| TiKV           | `storage.block-cache.shared`                                                                                                                                                                                                                              | 削除済み     | v6.6.0以降、この設定項目は削除され、ブロックキャッシュはデフォルトで有効になり、無効にすることはできません。詳細は[＃12936](https://github.com/tikv/tikv/issues/12936)参照してください。                                                               |
| DM             | `on-duplicate`                                                                                                                                                                                                                                            | 削除済み     | この設定項目は、フルインポートフェーズにおける競合の解決方法を制御します。v6.6.0では、 `on-duplicate`に代わる新しい設定項目`on-duplicate-logical`と`on-duplicate-physical`が導入されました。                                                        |
| ティドブ           | [`enable-telemetry`](/tidb-configuration-file.md#enable-telemetry-new-in-v402)                                                                                                                                                                            | 修正済み     | v6.6.0 以降では、デフォルト値が`true`から`false`に変更され、TiDB ではテレメトリがデフォルトで無効になることを意味します。                                                                                                              |
| TiKV           | [`rocksdb.defaultcf.block-size`](/tikv-configuration-file.md#block-size)と[`rocksdb.writecf.block-size`](/tikv-configuration-file.md#block-size)                                                                                                           | 修正済み     | デフォルト値は`64K`から`32K`に変更されます。                                                                                                                                                            |
| TiKV           | [`rocksdb.defaultcf.block-cache-size`](/tikv-configuration-file.md#block-cache-size) [`rocksdb.writecf.block-cache-size`](/tikv-configuration-file.md#block-cache-size) [`rocksdb.lockcf.block-cache-size`](/tikv-configuration-file.md#block-cache-size) | 非推奨      | バージョン6.6.0以降、これらの設定項目は非推奨となりました。詳細は[＃12936](https://github.com/tikv/tikv/issues/12936)参照してください。                                                                                        |
| PD             | [`enable-telemetry`](/pd-configuration-file.md#enable-telemetry)                                                                                                                                                                                          | 修正済み     | v6.6.0 以降では、デフォルト値が`true`から`false`に変更され、TiDB ダッシュボードではテレメトリがデフォルトで無効になることを意味します。                                                                                                       |
| DM             | [`import-mode`](/dm/task-configuration-file-full.md)                                                                                                                                                                                                      | 修正済み     | この設定項目の可能な値は、 `"sql"`と`"loader"`から`"logical"`と`"physical"`に変更されました。デフォルト値は`"logical"`で、これはTiDB Lightningの論理インポートモードを使用してデータをインポートすることを意味します。                                           |
| TiFlash        | [`profile.default.max_memory_usage_for_all_queries`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                                                                                                                                    | 修正済み     | すべてのクエリで生成される中間データのメモリ使用量の上限を指定します。v6.6.0以降、デフォルト値は`0`から`0.8`に変更され、上限は総メモリの80%になります。                                                                                                   |
| TiCDC          | [`consistent.storage`](/ticdc/ticdc-sink-to-mysql.md#prerequisites)                                                                                                                                                                                       | 修正済み     | この構成項目は`scheme` REDOログバックアップが保存されるパスを指定します。1、GCS、Azureの2つの値オプションが追加されました。                                                                                                              |
| ティドブ           | [`initialize-sql-file`](/tidb-configuration-file.md#initialize-sql-file-new-in-v660)                                                                                                                                                                      | 新しく追加された | この設定項目は、TiDBクラスタの初回起動時に実行されるSQLスクリプトを指定します。デフォルト値は空です。                                                                                                                                 |
| ティドブ           | [`tidb_stmt_summary_enable_persistent`](/tidb-configuration-file.md#tidb_stmt_summary_enable_persistent-new-in-v660)                                                                                                                                      | 新しく追加された | この設定項目は、ステートメントサマリーの永続化を有効にするかどうかを制御します。デフォルト値は`false`で、この機能はデフォルトでは有効になっていません。                                                                                                        |
| ティドブ           | [`tidb_stmt_summary_file_max_backups`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_backups-new-in-v660)                                                                                                                                        | 新しく追加された | ステートメント サマリーの永続化が有効になっている場合、この構成では永続化できるデータ ファイルの最大数を指定します。1 `0`ファイル数に制限がないことを意味します。                                                                                                   |
| ティドブ           | [`tidb_stmt_summary_file_max_days`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_days-new-in-v660)                                                                                                                                              | 新しく追加された | ステートメント サマリーの永続性が有効な場合、この構成では永続データ ファイルを保持する最大日数を指定します。                                                                                                                                |
| ティドブ           | [`tidb_stmt_summary_file_max_size`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_size-new-in-v660)                                                                                                                                              | 新しく追加された | ステートメント サマリーの永続性が有効な場合、この構成では永続データ ファイルの最大サイズ (MiB 単位) を指定します。                                                                                                                         |
| ティドブ           | [`tidb_stmt_summary_filename`](/tidb-configuration-file.md#tidb_stmt_summary_filename-new-in-v660)                                                                                                                                                        | 新しく追加された | ステートメント サマリーの永続性が有効な場合、この構成では永続データが書き込まれるファイルを指定します。                                                                                                                                   |
| TiKV           | [`resource-control.enabled`](/tikv-configuration-file.md#resource-control)                                                                                                                                                                                | 新しく追加された | 対応するリソースグループのリクエストユニット（RU）に基づいて、ユーザーのフォアグラウンド読み取り/書き込み要求のスケジュールを有効にするかどうか。デフォルト値は`false`で、対応するリソースグループのRUに基づくスケジュールを無効にすることを意味します。                                                     |
| TiKV           | [`storage.engine`](/tikv-configuration-file.md#engine-new-in-v660)                                                                                                                                                                                        | 新しく追加された | この設定項目は、storageエンジンの種類を指定します。値のオプションは`"raft-kv"`と`"partitioned-raft-kv"`です。この設定項目はクラスターの作成時にのみ指定でき、一度指定した後は変更できません。                                                                    |
| TiKV           | [`rocksdb.write-buffer-flush-oldest-first`](/tikv-configuration-file.md#write-buffer-flush-oldest-first-new-in-v660)                                                                                                                                      | 新しく追加された | この設定項目は、現在の RocksDB の`memtable`のメモリ使用量がしきい値に達したときに使用するフラッシュ戦略を指定します。                                                                                                                   |
| TiKV           | [`rocksdb.write-buffer-limit`](/tikv-configuration-file.md#write-buffer-limit-new-in-v660)                                                                                                                                                                | 新しく追加された | この設定項目は、単一のTiKV内のRocksDBインスタンスのうち`memtable`が使用するメモリの合計上限を指定します。デフォルト値はマシンメモリの合計の25%です。                                                                                                 |
| PD             | [`pd-server.enable-gogc-tuner`](/pd-configuration-file.md#enable-gogc-tuner-new-in-v660)                                                                                                                                                                  | 新しく追加された | この設定項目は、デフォルトでは無効になっている GOGC チューナーを有効にするかどうかを制御します。                                                                                                                                    |
| PD             | [`pd-server.gc-tuner-threshold`](/pd-configuration-file.md#gc-tuner-threshold-new-in-v660)                                                                                                                                                                | 新しく追加された | この設定項目は、GOGCのチューニングにおける最大メモリしきい値比率を指定します。デフォルト値は`0.6`です。                                                                                                                               |
| PD             | [`pd-server.server-memory-limit-gc-trigger`](/pd-configuration-file.md#server-memory-limit-gc-trigger-new-in-v660)                                                                                                                                        | 新しく追加された | この設定項目は、PDがGCをトリガーしようとする閾値比率を指定します。デフォルト値は`0.7`です。                                                                                                                                     |
| PD             | [`pd-server.server-memory-limit`](/pd-configuration-file.md#server-memory-limit-new-in-v660)                                                                                                                                                              | 新しく追加された | この設定項目は、PDインスタンスのメモリ制限率を指定します。値`0`はメモリ制限なしを意味します。                                                                                                                                      |
| TiCDC          | [`scheduler.region-per-span`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)                                                                                                                                                      | 新しく追加された | この設定項目は、リージョン数に基づいてテーブルを複数のレプリケーション範囲に分割するかどうかを制御します。これらの範囲は複数のTiCDCノードによって複製できます。デフォルト値は`50000`です。                                                                                    |
| TiDB Lightning | [`compress-kv-pairs`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)                                                                                                                                                                | 新しく追加された | この設定項目は、物理インポートモードでKVペアをTiKVに送信する際に圧縮を有効にするかどうかを制御します。デフォルト値は空で、圧縮は無効です。                                                                                                               |
| DM             | [`checksum-physical`](/dm/task-configuration-file-full.md)                                                                                                                                                                                                | 新しく追加された | この設定項目は、インポート後にデータ整合性を検証するために、DMが各テーブルに対して`ADMIN CHECKSUM TABLE <table>`実行するかどうかを制御します。デフォルト値は`"required"`で、インポート後に管理チェックサムを実行します。チェックサムが失敗した場合、DMはタスクを一時停止するため、手動でエラーを処理する必要があります。    |
| DM             | [`disk-quota-physical`](/dm/task-configuration-file-full.md)                                                                                                                                                                                              | 新しく追加された | この設定項目はディスククォータを設定します。これはTiDB Lightningの[`disk-quota`設定](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#configure-disk-quota-new-in-v620)に相当します。                         |
| DM             | [`on-duplicate-logical`](/dm/task-configuration-file-full.md)                                                                                                                                                                                             | 新しく追加された | この設定項目は、論理インポートモードにおいてDMが競合データを解決する方法を制御します。デフォルト値は`"replace"`で、これは新しいデータを使用して既存のデータを置き換えることを意味します。                                                                                    |
| DM             | [`on-duplicate-physical`](/dm/task-configuration-file-full.md)                                                                                                                                                                                            | 新しく追加された | この設定項目は、物理インポートモードにおいてDMが競合データを解決する方法を制御します。デフォルト値は`"none"`で、競合データを解決しないことを意味します。 `"none"`パフォーマンスが最も高くなりますが、下流のデータベースでデータの不整合が発生する可能性があります。                                            |
| DM             | [`sorting-dir-physical`](/dm/task-configuration-file-full.md)                                                                                                                                                                                             | 新しく追加された | この設定項目は、物理インポートモードにおけるローカルKVソートに使用するディレクトリを指定します。デフォルト値は設定`dir`と同じです。                                                                                                                  |
| 同期差分インスペクター    | [`skip-non-existing-table`](/sync-diff-inspector/sync-diff-inspector-overview.md#configuration-file-description)                                                                                                                                          | 新しく追加された | この構成項目は、ダウンストリームのテーブルがアップストリームに存在しない場合に、アップストリームとダウンストリームのデータ整合性のチェックをスキップするかどうかを制御します。                                                                                                |
| ティスパーク         | [`spark.tispark.replica_read`](/tispark-overview.md#tispark-configurations)                                                                                                                                                                               | 新しく追加された | この設定項目は、読み取るレプリカの種類を制御します。値のオプションは`leader` 、 `follower` 、 `learner`です。                                                                                                                 |
| ティスパーク         | [`spark.tispark.replica_read.label`](/tispark-overview.md#tispark-configurations)                                                                                                                                                                         | 新しく追加された | この構成項目は、ターゲット TiKV ノードのラベルを設定するために使用されます。                                                                                                                                              |

### その他 {#others}

-   [`store-io-pool-size`](/tikv-configuration-file.md#store-io-pool-size-new-in-v530)動的な変更をサポートします。これにより、より柔軟な TiKV パフォーマンスチューニングが可能になります。
-   `LIMIT`句の制限を削除して、実行パフォーマンスを向上させます。
-   v6.6.0 以降、 BR はv6.1.0 より前のクラスターへのデータの復元をサポートしていません。
-   v6.6.0 以降、TiDB は、潜在的な正確性の問題のため、パーティション化されたテーブルの列タイプの変更をサポートしなくなりました。

## 改善点 {#improvements}

-   ティドブ

    -   TTLバックグラウンドクリーニングタスクのスケジュールメカニズムを改善し、単一テーブルのクリーニングタスクを複数のサブタスクに分割し、複数のTiDBノードで同時に実行するようにスケジュールできるようになりました[＃40361](https://github.com/pingcap/tidb/issues/40361) @ [ヤンケオ](https://github.com/YangKeao)
    -   デフォルト以外の区切り文字[＃39662](https://github.com/pingcap/tidb/issues/39662) @ [ミョンス](https://github.com/mjonss)を設定した後に、複数のステートメントを実行して返される結果の列名の表示を最適化します。
    -   警告メッセージが生成された後のステートメントの実行効率を最適化します[＃39702](https://github.com/pingcap/tidb/issues/39702) @ [天菜麻緒](https://github.com/tiancaiamao)
    -   `ADD INDEX` （実験的） [＃37119](https://github.com/pingcap/tidb/issues/37119) @ [ジムララ](https://github.com/zimulala)の分散データバックフィルをサポート
    -   列[＃38356](https://github.com/pingcap/tidb/issues/38356) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)のデフォルト値として`CURDATE()`使用することをサポートします
    -   `partial order prop push down` LIST 型パーティションテーブル[＃40273](https://github.com/pingcap/tidb/issues/40273) @ [ウィノロス](https://github.com/winoros)をサポートするようになりました
    -   オプティマイザヒントと実行プランバインディング間の競合に関するエラーメッセージを追加する[＃40910](https://github.com/pingcap/tidb/issues/40910) @ [思い出させる](https://github.com/Reminiscent)
    -   いくつかのシナリオでプランキャッシュを使用するときに最適でないプランを回避するためにプランキャッシュ戦略を最適化します[＃40312](https://github.com/pingcap/tidb/pull/40312) [＃40218](https://github.com/pingcap/tidb/pull/40218) [＃40280](https://github.com/pingcap/tidb/pull/40280) [＃41136](https://github.com/pingcap/tidb/pull/41136) [＃40686](https://github.com/pingcap/tidb/pull/40686) @ [qw4990](https://github.com/qw4990)
    -   メモリリークとパフォーマンスの低下を防ぐため、期限切れのリージョンキャッシュを定期的にクリアします[＃40461](https://github.com/pingcap/tidb/issues/40461) @ [スティクナーフ](https://github.com/sticnarf)
    -   `MODIFY COLUMN`はパーティションテーブル[＃39915](https://github.com/pingcap/tidb/issues/39915) @ [wjhuang2016](https://github.com/wjhuang2016)ではサポートされません
    -   パーティションテーブルが依存する列の名前変更を無効にする[＃40150](https://github.com/pingcap/tidb/issues/40150) @ [ミョンス](https://github.com/mjonss)
    -   パーティションテーブルが依存する列が削除されたときに報告されるエラーメッセージを改善する[＃38739](https://github.com/pingcap/tidb/issues/38739) @ [ジフハスト](https://github.com/jiyfhust)
    -   `min-resolved-ts` [＃39836](https://github.com/pingcap/tidb/issues/39836) @ [定義2014](https://github.com/Defined2014)のチェックに失敗した場合、 `FLASHBACK CLUSTER`再試行するメカニズムを追加します。

-   ティクブ

    -   パーティション化されたraft-kvモードにおける一部のパラメータのデフォルト値を最適化しました。TiKV設定項目`storage.block-cache.capacity`のデフォルト値は45%から30%に調整され、デフォルト値`region-split-size`は`96MiB`から`10GiB`に調整されました。raft-kvモードを使用し、 `enable-region-bucket`が`true`の場合、 `region-split-size`はデフォルトで1GiBに調整されます[＃12842](https://github.com/tikv/tikv/issues/12842) @ [トニーシュキ](https://github.com/tonyxuqqi)
    -   Raftstoreの非同期書き込み[＃13730](https://github.com/tikv/tikv/issues/13730) @ [コナー1996](https://github.com/Connor1996)での優先スケジュールをサポート
    -   1コア未満のCPUでのTiKVの起動をサポート[＃13586](https://github.com/tikv/tikv/issues/13586) [＃13752](https://github.com/tikv/tikv/issues/13752) [＃14017](https://github.com/tikv/tikv/issues/14017) @ [アンドレイド・DB](https://github.com/andreid-db)
    -   Raftstoreのスロースコアの新しい検出メカニズムを最適化し、 `evict-slow-trend-scheduler` [＃14131](https://github.com/tikv/tikv/issues/14131) @ [内側](https://github.com/innerr)を追加します
    -   RocksDB のブロックキャッシュを強制的に共有し、CF [＃12936](https://github.com/tikv/tikv/issues/12936) @ [忙しいカケス](https://github.com/busyjay)に従ってブロックキャッシュを個別に設定することはサポートされなくなりました。

-   PD

    -   OOM 問題を軽減するためのグローバルメモリしきい値の管理のサポート (実験的) [＃5827](https://github.com/tikv/pd/issues/5827) @ [ネス](https://github.com/hnes)
    -   GC圧力を軽減するためにGCチューナーを追加する（実験的） [＃5827](https://github.com/tikv/pd/issues/5827) @ [ネス](https://github.com/hnes)
    -   異常ノード[＃5808](https://github.com/tikv/pd/pull/5808) @ [内側](https://github.com/innerr)を検出してスケジュールする`evict-slow-trend-scheduler`スケジューラを追加します。
    -   キースペース[＃5293](https://github.com/tikv/pd/issues/5293) @ [アメーバ原生動物](https://github.com/AmoebaProtozoa)を管理するキースペース マネージャーを追加します。

-   TiFlash

    -   TiFlashデータスキャンプロセスにおけるMVCCフィルタリング操作を分離する独立したMVCCビットマップフィルタをサポートし、将来のデータスキャンプロセスの最適化の基盤を提供します[＃6296](https://github.com/pingcap/tiflash/issues/6296) @ [ジンヘリン](https://github.com/JinheLin)
    -   クエリ[＃6589](https://github.com/pingcap/tiflash/pull/6589) @ [ホンユニャン](https://github.com/hongyunyan)がない場合、 TiFlashのメモリ使用量を最大30％削減します

-   ツール

    -   バックアップと復元 (BR)

        -   TiKV 側でログ バックアップ ファイルのダウンロードの同時実行を最適化して、通常のシナリオ[＃14206](https://github.com/tikv/tikv/issues/14206) @ [ユジュンセン](https://github.com/YuJuncen)での PITR リカバリのパフォーマンスを向上させます。

    -   TiCDC

        -   TiCDC レプリケーションのパフォーマンスを向上させるためにバッチ`UPDATE` DML ステートメントをサポートする[＃8084](https://github.com/pingcap/tiflow/issues/8084) @ [アミャンフェイ](https://github.com/amyangfei)
        -   シンクのスループットを向上させるために、非同期モードでMQシンクとMySQLシンクを実装します[＃5928](https://github.com/pingcap/tiflow/issues/5928) @ [ヒック](https://github.com/hicqu) @ [ハイ・ラスティン](https://github.com/Rustin170506)

    -   TiDB データ移行 (DM)

        -   DMアラートルールとコンテンツ[＃7376](https://github.com/pingcap/tiflow/issues/7376) @ [D3ハンター](https://github.com/D3Hunter)を最適化

            以前は、関連するエラーが発生するたびに「DM_XXX_process_exits_with_error」のようなアラートが発生していました。しかし、アイドル状態のデータベース接続によって発生するアラートもあり、これらは再接続後に回復可能です。このようなアラートを削減するため、DMはエラーを自動的に回復可能なエラーと回復不可能なエラーの2種類に分類しています。

            -   自動的に回復可能なエラーの場合、DM は 2 分以内にエラーが 3 回以上発生した場合にのみアラートを報告します。
            -   自動的に回復できないエラーの場合、DM は元の動作を維持し、直ちにアラートを報告します。

        -   非同期/バッチリレーライター[＃4287](https://github.com/pingcap/tiflow/issues/4287) @ [GMHDBJD](https://github.com/GMHDBJD)を追加してリレーパフォーマンスを最適化します

    -   TiDB Lightning

        -   物理インポートモードはキースペース[＃40531](https://github.com/pingcap/tidb/issues/40531) @ [イモムクゲ](https://github.com/iosmanthus)をサポートします
        -   競合の最大数を`lightning.max-error` [＃40743](https://github.com/pingcap/tidb/issues/40743) @ [dsdashun](https://github.com/dsdashun)に設定できるようになりました
        -   BOM ヘッダー[＃40744](https://github.com/pingcap/tidb/issues/40744) @ [dsdashun](https://github.com/dsdashun)を含む CSV データファイルのインポートをサポート
        -   TiKVフロー制限エラーが発生した場合の処理ロジックを最適化し、代わりに他の利用可能な領域を試します[＃40205](https://github.com/pingcap/tidb/issues/40205) @ [ランス6716](https://github.com/lance6716)
        -   インポート中にテーブルの外部キーのチェックを無効にする[＃40027](https://github.com/pingcap/tidb/issues/40027) @ [眠そうなモグラ](https://github.com/sleepymole)

    -   Dumpling

        -   外部キー[＃39913](https://github.com/pingcap/tidb/issues/39913) @ [リチュンジュ](https://github.com/lichunzhu)の設定のエクスポートをサポート

    -   同期差分インスペクター

        -   下流のテーブルが上流に存在しない場合に上流と下流のデータ整合性のチェックをスキップするかどうかを制御する新しいパラメータ`skip-non-existing-table`を追加します[＃692](https://github.com/pingcap/tidb-tools/issues/692) @ [リチュンジュ](https://github.com/lichunzhu) @ [liumengya94](https://github.com/liumengya94)

## バグ修正 {#bug-fixes}

-   ティドブ

    -   `datetime`値が[＃39336](https://github.com/pingcap/tidb/issues/39336) @ [xuyifangreeneyes](https://github.com/xuyifangreeneyes)と正しくないために統計収集タスクが失敗する問題を修正しました
    -   テーブル作成[＃38189](https://github.com/pingcap/tidb/issues/38189) @ [xuyifangreeneyes](https://github.com/xuyifangreeneyes)の後に`stats_meta`が作成されない問題を修正
    -   DDLデータバックフィル[＃24427](https://github.com/pingcap/tidb/issues/24427) @ [ミョンス](https://github.com/mjonss)を実行するときにトランザクションで頻繁に発生する書き込み競合を修正
    -   取り込みモード[＃39641](https://github.com/pingcap/tidb/issues/39641) @ [接線](https://github.com/tangenta)を使用して空のテーブルにインデックスを作成できないことがある問題を修正しました
    -   スロークエリログの`wait_ts` 、同じトランザクション内の異なるSQL文に対して同じになる問題を修正[＃39713](https://github.com/pingcap/tidb/issues/39713) @ [トンスネークリン](https://github.com/TonsnakeLin)
    -   行レコード[＃39570](https://github.com/pingcap/tidb/issues/39570) @ [wjhuang2016](https://github.com/wjhuang2016)を削除するプロセス中に列を追加すると`Assertion Failed`エラーが報告される問題を修正しました
    -   列タイプ[＃39643](https://github.com/pingcap/tidb/issues/39643) @ [ジムララ](https://github.com/zimulala)を変更するときに`not a DDL owner`エラーが報告される問題を修正しました
    -   `AUTO_INCREMENT`列目[＃38950](https://github.com/pingcap/tidb/issues/38950)列目[ドゥーシル9](https://github.com/Dousir9)の自動増分値が使い果たされた後に行を挿入してもエラーが報告されない問題を修正しました。
    -   式インデックス[＃39784](https://github.com/pingcap/tidb/issues/39784) @ [定義2014](https://github.com/Defined2014)を作成するときに`Unknown column`エラーが報告される問題を修正しました
    -   生成された式にこのテーブルの名前[＃39826](https://github.com/pingcap/tidb/issues/39826) @ [定義2014](https://github.com/Defined2014)が含まれている場合、名前が変更されたテーブルにデータを挿入できない問題を修正しました。
    -   列が書き込み専用の場合に`INSERT ignore`文でデフォルト値を入力できない問題を修正[＃40192](https://github.com/pingcap/tidb/issues/40192) @ [ヤンケオ](https://github.com/YangKeao)
    -   リソース管理モジュール[＃40546](https://github.com/pingcap/tidb/issues/40546) @ [ジムララ](https://github.com/zimulala)を無効にしたときにリソースが解放されない問題を修正しました
    -   TTLタスクが時間[＃40109](https://github.com/pingcap/tidb/issues/40109) @ [ヤンケオ](https://github.com/YangKeao)で統計更新をトリガーできない問題を修正
    -   TiDB がキー範囲[＃40158](https://github.com/pingcap/tidb/issues/40158) @ [天菜麻緒](https://github.com/tiancaiamao)を構築するときに`NULL`値を不適切に処理するため、予期しないデータが読み取られる問題を修正しました。
    -   `MODIFY COLUMN`ステートメントが列[＃40164](https://github.com/pingcap/tidb/issues/40164) @ [wjhuang2016](https://github.com/wjhuang2016)のデフォルト値も変更すると、無効な値がテーブルに書き込まれる問題を修正しました。
    -   テーブル[＃38436](https://github.com/pingcap/tidb/issues/38436) @ [接線](https://github.com/tangenta)に多数のリージョンがある場合に無効なリージョンキャッシュが原因でインデックスの追加操作が非効率になる問題を修正しました。
    -   自動増分ID [＃40584](https://github.com/pingcap/tidb/issues/40584) @ [ドゥーシル9](https://github.com/Dousir9)の割り当て時に発生するデータ競合を修正
    -   JSONのnot演算子の実装がMySQL [＃40683](https://github.com/pingcap/tidb/issues/40683) @ [ヤンケオ](https://github.com/YangKeao)の実装と互換性がない問題を修正しました
    -   同時ビューによって DDL 操作がブロックされる可能性がある問題を修正[＃40352](https://github.com/pingcap/tidb/issues/40352) @ [沢民州](https://github.com/zeminzhou)
    -   パーティションテーブル[＃40620](https://github.com/pingcap/tidb/issues/40620) @ [ミョンス](https://github.com/mjonss) @ [ミョンス](https://github.com/mjonss)の列を変更する DDL ステートメントの同時実行によって発生するデータの不整合を修正します。
    -   パスワード[＃40831](https://github.com/pingcap/tidb/issues/40831) @ [ドヴェーデン](https://github.com/dveeden)を指定せずに認証に`caching_sha2_password`使用すると「不正なパケット」が報告される問題を修正
    -   テーブルの主キーに`ENUM`列[＃40456](https://github.com/pingcap/tidb/issues/40456) @ [lcwangchao](https://github.com/lcwangchao)が含まれている場合にTTLタスクが失敗する問題を修正しました
    -   MDLによってブロックされた一部のDDL操作が`mysql.tidb_mdl_view` [＃40838](https://github.com/pingcap/tidb/issues/40838) @ [ヤンケオ](https://github.com/YangKeao)でクエリできない問題を修正しました
    -   DDL取り込み[＃40970](https://github.com/pingcap/tidb/issues/40970) @ [接線](https://github.com/tangenta)中にデータ競合が発生する可能性がある問題を修正
    -   タイムゾーンの変更後にTTLタスクが一部のデータを誤って削除する可能性がある問題を修正[＃41043](https://github.com/pingcap/tidb/issues/41043) @ [lcwangchao](https://github.com/lcwangchao)
    -   `JSON_OBJECT`場合によってはエラーが報告される可能性がある問題を修正[＃39806](https://github.com/pingcap/tidb/issues/39806) @ [ヤンケオ](https://github.com/YangKeao)
    -   初期化中にTiDBがデッドロックする可能性がある問題を修正[＃40408](https://github.com/pingcap/tidb/issues/40408) @ [定義2014](https://github.com/Defined2014)
    -   メモリ再利用により、システム変数の値が誤って変更される可能性がある問題を修正[＃40979](https://github.com/pingcap/tidb/issues/40979) @ [lcwangchao](https://github.com/lcwangchao)
    -   取り込みモード[＃40464](https://github.com/pingcap/tidb/issues/40464) @ [接線](https://github.com/tangenta)でユニークインデックスが作成された場合に、データがインデックスと矛盾する可能性がある問題を修正しました。
    -   同じテーブルを同時に切り捨てるときに、一部の切り捨て操作が MDL によってブロックされない問題を修正[＃40484](https://github.com/pingcap/tidb/issues/40484) @ [wjhuang2016](https://github.com/wjhuang2016)
    -   `SHOW PRIVILEGES`文が不完全な権限リスト[＃40591](https://github.com/pingcap/tidb/issues/40591) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)を返す問題を修正しました
    -   ユニークインデックス[＃40592](https://github.com/pingcap/tidb/issues/40592) @ [接線](https://github.com/tangenta)を追加するときに TiDB がパニックになる問題を修正しました
    -   `ADMIN RECOVER`文を実行するとインデックスデータが破損する可能性がある問題を修正[＃40430](https://github.com/pingcap/tidb/issues/40430) @ [ションジウェイ](https://github.com/xiongjiwei)
    -   クエリ対象のテーブルに式インデックス[＃40130](https://github.com/pingcap/tidb/issues/40130) @ [ションジウェイ](https://github.com/xiongjiwei)に`CAST`式が含まれている場合にクエリが失敗する可能性がある問題を修正しました。
    -   ユニークインデックスが場合によっては重複データを生成する可能性がある問題を修正[＃40217](https://github.com/pingcap/tidb/issues/40217) @ [接線](https://github.com/tangenta)
    -   多数のリージョンがあるが、 `Prepare`または`Execute` [＃39605](https://github.com/pingcap/tidb/issues/39605) @ [djshow832](https://github.com/djshow832)を使用して一部の仮想テーブルをクエリするときにテーブル ID をプッシュダウンできないという PD OOM 問題を修正しました。
    -   インデックスを[＃40879](https://github.com/pingcap/tidb/issues/40879) @ [接線](https://github.com/tangenta)で追加するとデータ競合が発生する可能性がある問題を修正しました
    -   仮想列[＃41014](https://github.com/pingcap/tidb/issues/41014) @ [アイリンキッド](https://github.com/AilinKid)によって発生する`can't find proper physical plan`問題を修正
    -   動的トリミングモード[＃40368](https://github.com/pingcap/tidb/issues/40368) @ [イーサール](https://github.com/Yisaer)でパーティションテーブルにグローバルバインディングが作成された後にTiDBが再起動できない問題を修正しました
    -   `auto analyze`正常なシャットダウンに長い時間がかかる問題を修正[＃40038](https://github.com/pingcap/tidb/issues/40038) @ [xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    -   IndexMerge 演算子がメモリ制限動作[＃41036](https://github.com/pingcap/tidb/pull/41036) @ [グオシャオゲ](https://github.com/guo-shaoge)をトリガーしたときに TiDBサーバーのpanicを修正しました
    -   パーティションテーブルに対する`SELECT * FROM table_name LIMIT 1`クエリが遅い問題を修正[＃40741](https://github.com/pingcap/tidb/pull/40741) @ [ソロツグ](https://github.com/solotzg)

-   TiKV

    -   `const Enum`型を他の型[＃14156](https://github.com/tikv/tikv/issues/14156) @ [wshwsh12](https://github.com/wshwsh12)にキャストするときに発生するエラーを修正しました
    -   解決されたTSによりネットワークトラフィックが増加する問題を修正[＃14092](https://github.com/tikv/tikv/issues/14092) @ [金星の上](https://github.com/overvenus)
    -   悲観的DML [＃14038](https://github.com/tikv/tikv/issues/14038) @ [ミョンケミンタ](https://github.com/MyonKeminta)の失敗後のDML実行中にTiDBとTiKV間のネットワーク障害によって発生するデータの不整合の問題を修正しました。

-   PD

    -   リージョンスキャッタタスクが予期せず冗長レプリカを生成する問題を修正[＃5909](https://github.com/tikv/pd/issues/5909) @ [フンドゥンDM](https://github.com/HunDunDM)
    -   オンライン安全でないリカバリ機能が`auto-detect`モード[＃5753](https://github.com/tikv/pd/issues/5753) @ [コナー1996](https://github.com/Connor1996)で停止してタイムアウトする問題を修正
    -   特定の条件下で実行`replace-down-peer`遅くなる問題を修正[＃5788](https://github.com/tikv/pd/issues/5788) @ [フンドゥンDM](https://github.com/HunDunDM)
    -   `ReportMinResolvedTS`の呼び出しが[＃5965](https://github.com/tikv/pd/issues/5965) @ [フンドゥンDM](https://github.com/HunDunDM)で頻繁に発生する PD OOM 問題を修正しました

-   TiFlash

    -   TiFlash関連のシステムテーブルをクエリすると[＃6745](https://github.com/pingcap/tiflash/pull/6745) @ [リデジュ](https://github.com/lidezhu)でスタックする可能性がある問題を修正しました
    -   直交積[＃6730](https://github.com/pingcap/tiflash/issues/6730) @ [ゲンリキ](https://github.com/gengliqi)を計算するときにセミ結合が過剰なメモリを使用する問題を修正しました
    -   DECIMALデータ型の除算演算の結果が[＃6393](https://github.com/pingcap/tiflash/issues/6393) @ [リトルフォール](https://github.com/LittleFall)に丸められない問題を修正しました
    -   `start_ts` TiFlashクエリでMPPクエリを一意に識別できないため、MPPクエリが誤ってキャンセルされる可能性がある問題を修正[＃43426](https://github.com/pingcap/tidb/issues/43426) @ [ヘヘチェン](https://github.com/hehechen)

-   ツール

    -   バックアップと復元 (BR)

        -   ログバックアップを復元するときに、ホットリージョンによって復元が失敗する問題を修正しました[＃37207](https://github.com/pingcap/tidb/issues/37207) @ [リーヴルス](https://github.com/Leavrth)
        -   ログバックアップが実行中のクラスタにデータを復元すると、ログバックアップファイルが回復不能になる問題を修正[＃40797](https://github.com/pingcap/tidb/issues/40797) @ [リーヴルス](https://github.com/Leavrth)
        -   PITR機能がCAバンドル[＃38775](https://github.com/pingcap/tidb/issues/38775) @ [ユジュンセン](https://github.com/YuJuncen)をサポートしない問題を修正
        -   リカバリ中に重複した一時テーブルによって発生するpanic問題を修正[＃40797](https://github.com/pingcap/tidb/issues/40797) @ [ジョッカウ](https://github.com/joccau)
        -   PITRがPDクラスタ[＃14165](https://github.com/tikv/tikv/issues/14165) @ [ユジュンセン](https://github.com/YuJuncen)の構成変更をサポートしない問題を修正
        -   PD と tidb-server 間の接続障害により PITR バックアップの進行が[＃41082](https://github.com/pingcap/tidb/issues/41082) @ [ユジュンセン](https://github.com/YuJuncen)に進まない問題を修正しました
        -   PDとTiKV [＃14159](https://github.com/tikv/tikv/issues/14159) @ [ユジュンセン](https://github.com/YuJuncen)間の接続障害によりTiKVがPITRタスクをリッスンできない問題を修正
        -   TiDB クラスタ[＃40759](https://github.com/pingcap/tidb/issues/40759) @ [ジョッカウ](https://github.com/joccau)に PITR バックアップ タスクがない場合に頻度`resolve lock`が高すぎる問題を修正しました
        -   PITRバックアップタスクを削除すると、残りのバックアップデータによって新しいタスク[＃40403](https://github.com/pingcap/tidb/issues/40403) @ [ジョッカウ](https://github.com/joccau)でデータの不整合が発生する問題を修正しました。

    -   TiCDC

        -   `transaction_atomicity`と`protocol`構成ファイル[＃7935](https://github.com/pingcap/tiflow/issues/7935) @ [チャールズ・チャン96](https://github.com/CharlesCheung96)経由で更新できない問題を修正
        -   REDOログ[＃6335](https://github.com/pingcap/tiflow/issues/6335) @ [チャールズ・チャン96](https://github.com/CharlesCheung96)のstorageパスで事前チェ​​ックが実行されない問題を修正
        -   S3storage障害[＃8089](https://github.com/pingcap/tiflow/issues/8089) @ [チャールズ・チャン96](https://github.com/CharlesCheung96)に対して、REDO ログが許容できる期間が不十分である問題を修正しました
        -   TiKV または TiCDC ノード[＃8174](https://github.com/pingcap/tiflow/issues/8174) @ [ヒック](https://github.com/hicqu)のスケールインまたはスケールアウトなどの特別なシナリオで、changefeed がスタックする可能性がある問題を修正しました。
        -   TiKVノード[＃14092](https://github.com/tikv/tikv/issues/14092)と[金星の上](https://github.com/overvenus)の間のトラフィックが多すぎる問題を修正
        -   プルベースのシンクが有効な場合の、CPU 使用率、メモリ制御、スループットに関する TiCDC のパフォーマンスの問題を修正しました[＃8142](https://github.com/pingcap/tiflow/issues/8142) [＃8157](https://github.com/pingcap/tiflow/issues/8157) [＃8001](https://github.com/pingcap/tiflow/issues/8001) [＃5928](https://github.com/pingcap/tiflow/issues/5928) @ [ヒック](https://github.com/hicqu) @ [ハイ・ラスティン](https://github.com/Rustin170506)

    -   TiDB データ移行 (DM)

        -   `binlog-schema delete`コマンドが[＃7373](https://github.com/pingcap/tiflow/issues/7373) @ [liumengya94](https://github.com/liumengya94)の実行に失敗する問題を修正
        -   最後のbinlogがスキップされたDDL [＃8175](https://github.com/pingcap/tiflow/issues/8175) @ [D3ハンター](https://github.com/D3Hunter)の場合にチェックポイントが進まない問題を修正しました
        -   1つのテーブルに「更新」と「非更新」の両方のタイプの式フィルタが指定されている場合、すべての`UPDATE`ステートメントがスキップされるバグを修正しました[＃7831](https://github.com/pingcap/tiflow/issues/7831) @ [ランス6716](https://github.com/lance6716)
        -   テーブルに`update-old-value-expr`または`update-new-value-expr`のいずれか 1 つだけが設定されている場合に、フィルタ ルールが有効にならないか、DM が[＃7774](https://github.com/pingcap/tiflow/issues/7774) @ [ランス6716](https://github.com/lance6716)でパニックになるというバグを修正しました。

    -   TiDB Lightning

        -   一部のシナリオで TiDB の再起動によりTiDB Lightning のタイムアウトがハングする問題を修正[＃33714](https://github.com/pingcap/tidb/issues/33714) @ [リチュンジュ](https://github.com/lichunzhu)
        -   並列インポート中に、最後のTiDB Lightningインスタンスを除くすべてのインスタンスでローカル重複レコードが検出された場合、 TiDB Lightning が競合解決を誤ってスキップする可能性がある問題を修正しました[＃40923](https://github.com/pingcap/tidb/issues/40923) @ [リチュンジュ](https://github.com/lichunzhu)
        -   事前チェックがターゲット クラスター[＃41040](https://github.com/pingcap/tidb/issues/41040) @ [ランス6716](https://github.com/lance6716)で実行中の TiCDC の存在を正確に検出できない問題を修正しました。
        -   TiDB Lightningが分割領域フェーズ[＃40934](https://github.com/pingcap/tidb/issues/40934) @ [ランス6716](https://github.com/lance6716)でパニックになる問題を修正
        -   競合解決ロジック（ `duplicate-resolution` ）によってチェックサム[＃40657](https://github.com/pingcap/tidb/issues/40657) @ [眠そうなモグラ](https://github.com/sleepymole)の不一致が発生する可能性がある問題を修正しました。
        -   データファイル[＃40400](https://github.com/pingcap/tidb/issues/40400) @ [ブチュイトデゴウ](https://github.com/buchuitoudegou)に閉じられていない区切り文字がある場合に発生する可能性のある OOM 問題を修正しました。
        -   エラーレポートのファイルオフセットがファイルサイズ[＃40034](https://github.com/pingcap/tidb/issues/40034) @ [ブチュイトデゴウ](https://github.com/buchuitoudegou)を超える問題を修正しました
        -   PDClient の新バージョンで並列インポートが失敗する可能性がある問題を修正[＃40493](https://github.com/pingcap/tidb/issues/40493) @ [アメーバ原生動物](https://github.com/AmoebaProtozoa)
        -   TiDB Lightning の事前チェックで、以前に失敗したインポート[＃39477](https://github.com/pingcap/tidb/issues/39477) @ [dsdashun](https://github.com/dsdashun)によって残されたダーティデータを見つけられない問題を修正しました

## 寄稿者 {#contributors}

TiDB コミュニティの以下の貢献者に感謝いたします。

-   [モルゴ](https://github.com/morgo)
-   [ジフハスト](https://github.com/jiyfhust)
-   [b41sh](https://github.com/b41sh)
-   [ソースリウ](https://github.com/sourcelliu)
-   [ソンジビン97](https://github.com/songzhibin97)
-   [マミル](https://github.com/mamil)
-   [ドゥーシル9](https://github.com/Dousir9)
-   [ヒヒフフ](https://github.com/hihihuhu)
-   [マイコキシン](https://github.com/mychoxin)
-   [シュニン97](https://github.com/xuning97)
-   [andreid-db](https://github.com/andreid-db)
