---
title: TiDB 6.6.0 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 6.6.0.
---

# TiDB 6.6.0 リリースノート {#tidb-6-6-0-release-notes}

発売日：2023年2月20日

TiDB バージョン: [DMR](/releases/versioning.md#development-milestone-releases)

> **注記：**
>
> TiDB 6.6.0-DMR のドキュメントは[アーカイブされた](https://docs-archive.pingcap.com/tidb/v6.6/)になりました。 PingCAP では、 [最新のLTSバージョン](https://docs.pingcap.com/tidb/stable)の TiDB データベースを使用することをお勧めします。

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.6/quick-start-with-tidb) | [インストールパッケージ](https://www.pingcap.com/download/?version=v6.6.0#version-list)

v6.6.0-DMR の主な新機能と改善点は次のとおりです。

<table><thead><tr><th>カテゴリー</th><th>特徴</th><th>説明</th></tr></thead><tbody><tr><td rowspan="3">スケーラビリティとパフォーマンス<br /></td><td>TiKV は<a href="https://docs.pingcap.com/tidb/v6.6/partitioned-raft-kv" target="_blank">Partitioned Raft KVstorageエンジン</a>をサポートします (実験的)</td><td> TiKV は Partitioned Raft KVstorageエンジンを導入し、各リージョンは独立した RocksDB インスタンスを使用します。これにより、クラスターのstorage容量を TB から PB に簡単に拡張でき、より安定した書き込みレイテンシーと強力なスケーラビリティを実現できます。</td></tr><tr><td> TiKV は<a href="https://docs.pingcap.com/tidb/v6.6/system-variables#tidb_store_batch_size" target="_blank">データリクエストのバッチ集約</a>をサポートします</td><td>この機能強化により、TiKV バッチ取得操作の合計 RPC が大幅に削減されます。データが高度に分散しており、gRPC スレッド プールのリソースが不十分な状況では、コプロセッサ要求をバッチ処理すると、パフォーマンスが 50% 以上向上する可能性があります。</td></tr><tr><td> TiFlash は<a href="https://docs.pingcap.com/tidb/v6.6/stale-read" target="_blank">ステイル読み取り</a>と<a href="https://docs.pingcap.com/tidb/v6.6/explain-mpp#mpp-version-and-exchange-data-compression" target="_blank">圧縮交換</a>をサポートします</td><td>TiFlash は、リアルタイム要件が制限されていないシナリオでクエリのパフォーマンスを向上させることができる古い読み取り機能をサポートしています。 TiFlash は、並列データ交換の効率を向上させるデータ圧縮をサポートしており、TPC-H の全体的なパフォーマンスが 10% 向上し、ネットワーク使用量を 50% 以上節約できます。</td></tr><tr><td rowspan="2">信頼性と可用性<br /></td><td><a href="https://docs.pingcap.com/tidb/v6.6/tidb-resource-control" target="_blank">リソース制御</a>(実験的)</td><td>リソース グループに基づいたリソース管理をサポートします。これにより、データベース ユーザーが対応するリソース グループにマップされ、実際のニーズに基づいて各リソース グループのクォータが設定されます。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v6.6/sql-plan-management#create-a-binding-according-to-a-historical-execution-plan" target="_blank">履歴 SQL バインディング</a></td><td>TiDB ダッシュボードで履歴実行計画のバインドと実行計画の迅速なバインドをサポートします。</td></tr><tr><td rowspan="2"> SQL機能<br /></td><td><a href="https://docs.pingcap.com/tidb/v6.6/foreign-key" target="_blank">外部キー</a>(実験的)</td><td>データの一貫性を維持し、データ品質を向上させるために、MySQL 互換の外部キー制約をサポートします。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v6.6/sql-statement-create-index#multi-valued-indexes" target="_blank">多値インデックス</a>(実験的)</td><td> MySQL と互換性のある多値インデックスを導入し、JSON タイプを強化して、TiDB と MySQL 8.0 の互換性を向上させます。</td></tr><tr><td> DBの操作と可観測性<br /></td><td><a href="https://docs.pingcap.com/tidb/v6.6/dm-precheck#check-items-for-physical-import" target="_blank">DM は物理的なインポートをサポートします</a>(実験的)</td><td> TiDB Data Migration (DM) は、TiDB Lightning の物理インポート モードを統合して、完全なデータ移行のパフォーマンスを向上させ、パフォーマンスが最大 10 倍速くなります。</td></tr></tbody></table>

## 機能の詳細 {#feature-details}

### スケーラビリティ {#scalability}

-   サポートパーティションRaft KVstorageエンジン (実験的) [#11515](https://github.com/tikv/tikv/issues/11515) [#12842](https://github.com/tikv/tikv/issues/12842) @ [ビジージェイ](https://github.com/busyjay) @ [トニーシュクキ](https://github.com/tonyxuqqi) @ [タボキー](https://github.com/tabokie) @ [バッファフライ](https://github.com/bufferflies) @ [5kbps](https://github.com/5kbpers) @ [SpadeA-Tang](https://github.com/SpadeA-Tang) @ [ノールーシュ](https://github.com/nolouch)

    TiDB v6.6.0 より前は、TiKV の Raft ベースのstorageエンジンは単一の RocksDB インスタンスを使用して、TiKV インスタンスのすべての「リージョン」のデータを保存していました。大規模なクラスターをより安定してサポートするために、TiDB v6.6.0 以降では、複数の RocksDB インスタンスを使用して TiKVリージョンデータを保存する新しい TiKVstorageエンジンが導入され、各リージョンのデータは個別の RocksDB インスタンスに個別に保存されます。新しいエンジンは、RocksDB インスタンス内のファイルの数とレベルをより適切に制御し、リージョン間のデータ操作の物理的な分離を実現し、より多くのデータの安定した管理をサポートします。これは、パーティショニングを通じて複数の RocksDB インスタンスを管理する TiKV として見ることができます。そのため、この機能は Partitioned-Raft-KV と名付けられています。この機能の主な利点は、書き込みパフォーマンスの向上、スケーリングの高速化、および同じハードウェアでサポートされるデータ量の増加です。より大きなクラスター規模もサポートできます。

    現在、この機能は実験的であり、本番環境での使用は推奨されません。

    詳細については、 [ドキュメンテーション](/partitioned-raft-kv.md)を参照してください。

-   DDL 操作の分散並列実行フレームワークをサポート (実験的) [#37125](https://github.com/pingcap/tidb/issues/37125) @ [ジムララ](https://github.com/zimulala)

    以前のバージョンでは、TiDB クラスター全体で 1 つの TiDB インスタンスのみが DDL 所有者としてスキーマ変更タスクを処理できました。大規模なテーブルの DDL 操作の DDL 同時実行性をさらに向上させるために、TiDB v6.6.0 では DDL 用の分散並列実行フレームワークが導入されています。これにより、クラスター内のすべての TiDB インスタンスが同じタスクの`StateWriteReorganization`フェーズを同時に実行して、DDL の実行を高速化できます。この機能はシステム変数[`tidb_ddl_distribute_reorg`](https://docs.pingcap.com/tidb/v6.6/system-variables#tidb_ddl_distribute_reorg-new-in-v660)によって制御され、現在`Add Index`操作に対してのみサポートされています。

### パフォーマンス {#performance}

-   悲観的ロック キュー[#13298](https://github.com/tikv/tikv/issues/13298) @ [ミョンケミンタ](https://github.com/MyonKeminta)の安定したウェイクアップ モデルをサポートします。

    アプリケーションで単一ポイントの悲観的ロックの競合が頻繁に発生した場合、既存のウェイクアップ メカニズムではトランザクションがロックを取得する時間を保証できず、ロングテールレイテンシーが長くなり、さらにはロック取得タイムアウトが発生します。 v6.6.0 以降、システム変数の値[`tidb_pessimistic_txn_aggressive_locking`](https://docs.pingcap.com/tidb/v6.6/system-variables#tidb_pessimistic_txn_aggressive_locking-new-in-v660)から`ON`を設定することで、悲観的ロックの安定したウェイクアップ モデルを有効にすることができます。このウェイクアップ モデルでは、キューのウェイクアップ シーケンスを厳密に制御して、無効なウェイクアップによるリソースの無駄を回避できます。深刻なロック競合があるシナリオでは、安定したウェイクアップ モデルにより、ロングテールレイテンシーと P99 応答時間を短縮できます。

    テストでは、これによりテールレイテンシーが40 ～ 60% 短縮されることが示されています。

    詳細については、 [ドキュメンテーション](https://docs.pingcap.com/tidb/v6.6/system-variables#tidb_pessimistic_txn_aggressive_locking-new-in-v660)を参照してください。

-   バッチ集計データ要求[#39361](https://github.com/pingcap/tidb/issues/39361) @ [cfzjywxk](https://github.com/cfzjywxk) @ [あなた06](https://github.com/you06)

    TiDB がデータ リクエストを TiKV に送信すると、TiDB はデータが存在するリージョンに応じてリクエストを異なるサブタスクにコンパイルし、各サブタスクは 1 つのリージョンのリクエストのみを処理します。アクセスするデータが分散性が高い場合、データサイズが大きくなくてもサブタスクが多数生成され、RPCリクエストが多く発生して余分な時間がかかります。 v6.6.0 以降、TiDB は、同じ TiKV インスタンスに送信されるデータ リクエストの部分的なマージをサポートします。これにより、サブタスクの数と RPC リクエストのオーバーヘッドが削減されます。データの分散が高く、gRPC スレッド プール リソースが不十分な場合、リクエストをバッチ処理するとパフォーマンスが 50% 以上向上する可能性があります。

    この機能はデフォルトで有効になっています。システム変数[`tidb_store_batch_size`](/system-variables.md#tidb_store_batch_size)を使用してリクエストのバッチ サイズを設定できます。

-   `LIMIT`条項[#40219](https://github.com/pingcap/tidb/issues/40219) @ [fzzf678](https://github.com/fzzf678)の制限を削除します

    v6.6.0 以降、TiDB プラン キャッシュは、 `LIMIT ?`や`LIMIT 10, ?`などの変数を`LIMIT`パラメータとして使用した実行プランのキャッシュをサポートします。この機能により、より多くの SQL ステートメントがプラン キャッシュの恩恵を受けることができるため、実行効率が向上します。現在、セキュリティを考慮して、TiDB は 10000 以下の`?`の実行プランのみをキャッシュできます。

    詳細については、 [ドキュメンテーション](/sql-prepared-plan-cache.md)を参照してください。

-   TiFlash は圧縮[#6620](https://github.com/pingcap/tiflash/issues/6620) @ [ソロッツグ](https://github.com/solotzg)でのデータ交換をサポートします

    コンピューティングのために複数のノードと連携するには、 TiFlashエンジンは異なるノード間でデータを交換する必要があります。交換されるデータのサイズが非常に大きい場合、データ交換のパフォーマンスが全体的なコンピューティング効率に影響を与える可能性があります。 v6.6.0 では、 TiFlashエンジンに圧縮メカニズムが導入され、必要に応じて交換するデータを圧縮してから交換が行われるため、データ交換の効率が向上します。

    詳細については、 [ドキュメンテーション](/explain-mpp.md#mpp-version-and-exchange-data-compression)を参照してください。

-   TiFlash は、 ステイル読み取り機能[#4483](https://github.com/pingcap/tiflash/issues/4483) @ [へへへん](https://github.com/hehechen)をサポートします。

    ステイル読み取り機能は v5.1.1 から一般提供 (GA) されており、特定のタイムスタンプまたは指定された時間範囲内の履歴データを読み取ることができます。古い読み取りでは、ローカル TiKV レプリカからデータを直接読み取ることで、読み取りレイテンシーを短縮し、クエリのパフォーマンスを向上させることができます。 v6.6.0 より前では、 TiFlash はステイル読み取りをサポートしていません。テーブルにTiFlashレプリカがある場合でも、 ステイル読み取り はその TiKV レプリカのみを読み取ることができます。

    v6.6.0 以降、 TiFlash はステイル読み取り機能をサポートします。 [`AS OF TIMESTAMP`](/as-of-timestamp.md)構文または[`tidb_read_staleness`](/tidb-read-staleness.md)システム変数を使用してテーブルの履歴データをクエリするとき、テーブルにTiFlashレプリカがある場合、オプティマイザはTiFlashレプリカから対応するデータを読み取ることを選択できるようになり、クエリのパフォーマンスがさらに向上します。

    詳細については、 [ドキュメンテーション](/stale-read.md)を参照してください。

-   `regexp_replace`文字列機能のTiFlash [#6115](https://github.com/pingcap/tiflash/issues/6115) @ [xzhangxian1008](https://github.com/xzhangxian1008)へのプッシュダウンをサポート

### 信頼性 {#reliability}

-   リソース グループに基づくリソース制御のサポート (実験的) [#38825](https://github.com/pingcap/tidb/issues/38825) @ [ノールーシュ](https://github.com/nolouch) @ [ボーンチェンジャー](https://github.com/BornChanger) @ [グロルフ](https://github.com/glorv) @ [ティエンチャイアマオ](https://github.com/tiancaiamao) @ [コナー1996](https://github.com/Connor1996) @ [Jmポテト](https://github.com/JmPotato) @ [フネス](https://github.com/hnes) @ [キャビンフィーバーB](https://github.com/CabinfeverB) @ [ヒューシャープ](https://github.com/HuSharp)

    TiDB クラスターのリソース グループを作成し、さまざまなデータベース ユーザーを対応するリソース グループにバインドし、実際のニーズに応じて各リソース グループのクォータを設定できるようになりました。クラスターのリソースが制限されている場合、同じリソース グループ内のセッションで使用されるすべてのリソースはクォータ内に制限されます。これにより、リソース グループが過剰に消費されても、他のリソース グループのセッションは影響を受けません。 TiDB は、Grafana ダッシュボード上のリソースの実際の使用状況を示す組み込みビューを提供し、リソースをより合理的に割り当てるのに役立ちます。

    リソース制御機能の導入は、TiDB にとってマイルストーンです。分散データベース クラスターを複数の論理ユニットに分割できます。たとえ個々のユニットがリソースを過剰に使用しても、他のユニットが必要とするリソースがクラウドアウトされることはありません。

    この機能を使用すると、次のことが可能になります。

    -   異なるシステムからの複数の中小規模のアプリケーションを単一の TiDB クラスターに結合します。アプリケーションのワークロードが大きくなっても、他のアプリケーションの通常の動作には影響しません。システムのワークロードが低い場合は、設定された読み取りおよび書き込みクォータを超えた場合でも、ビジー状態のアプリケーションに必要なシステム リソースを割り当てることができるため、リソースを最大限に活用できます。
    -   すべてのテスト環境を単一の TiDB クラスターに結合するか、より多くのリソースを消費するバッチ タスクを単一のリソース グループにグループ化するかを選択します。重要なアプリケーションが常に必要なリソースを確実に取得できるようにしながら、ハードウェアの使用率を向上させ、運用コストを削減できます。

    さらに、リソース制御機能を合理的に使用することで、クラスタ数を削減し、運用保守の困難を軽減し、管理コストを節約できます。

    v6.6 では、リソース制御を有効にするには、TiDB のグローバル変数[`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-new-in-v660)と TiKV 構成項目[`resource-control.enabled`](/tikv-configuration-file.md#resource-control)の両方を有効にする必要があります。現在サポートされているクォータ方式は「 [リクエストユニット(RU)](/tidb-resource-control.md#what-is-request-unit-ru) 」に基づいています。 RU は、CPU や IO などのシステム リソースに対する TiDB の統合抽象化ユニットです。

    詳細については、 [ドキュメンテーション](/tidb-resource-control.md)を参照してください。

-   過去の実行計画のバインディングは GA [#39199](https://github.com/pingcap/tidb/issues/39199) @ [fzzf678](https://github.com/fzzf678)です

    v6.5.0 では、TiDB は[`CREATE [GLOBAL | SESSION] BINDING`](/sql-statements/sql-statement-create-binding.md)ステートメントのバインディング ターゲットを拡張し、過去の実行計画に従ってバインディングの作成をサポートします。 v6.6.0 では、この機能は GA です。実行プランの選択は、現在の TiDB ノードに限定されません。任意の TiDB ノードによって生成された任意の履歴実行プランを[SQLバインディング](/sql-statements/sql-statement-create-binding.md)のターゲットとして選択できるため、機能の使いやすさがさらに向上します。

    詳細については、 [ドキュメンテーション](/sql-plan-management.md#create-a-binding-according-to-a-historical-execution-plan)を参照してください。

-   いくつかのオプティマイザー ヒント[#39964](https://github.com/pingcap/tidb/issues/39964) @ [懐かしい](https://github.com/Reminiscent)を追加します。

    TiDB は、v6.6.0 で、 `LIMIT`オペレーションの実行プラン選択を制御するためのいくつかのオプティマイザー ヒントを追加します。

    -   [`ORDER_INDEX()`](/optimizer-hints.md#order_indext1_name-idx1_name--idx2_name-) : データ読み取り時にインデックスの順序を維持するために指定されたインデックスを使用するようにオプティマイザーに指示し、 `Limit + IndexScan(keep order: true)`と同様のプランを生成します。
    -   [`NO_ORDER_INDEX()`](/optimizer-hints.md#no_order_indext1_name-idx1_name--idx2_name-) : データの読み取り時にインデックスの順序を維持せず、指定されたインデックスを使用するようにオプティマイザーに指示し、 `TopN + IndexScan(keep order: false)`と同様のプランを生成します。

    オプティマイザー ヒントを継続的に導入することで、ユーザーにさらに多くの介入方法が提供され、SQL パフォーマンスの問題の解決に役立ち、全体的なパフォーマンスの安定性が向上します。

-   DDL 操作のリソース使用量の動的管理のサポート (実験的) [#38025](https://github.com/pingcap/tidb/issues/38025) @ [ホーキングレイ](https://github.com/hawkingrei)

    TiDB v6.6.0 では、DDL 操作のリソース管理が導入されており、これらの操作の CPU 使用率を自動的に制御することで、オンライン アプリケーションに対する DDL 変更の影響を軽減します。この機能は、 [DDL 分散並列実行フレームワーク](https://docs.pingcap.com/tidb/v6.6/system-variables#tidb_ddl_distribute_reorg-new-in-v660)が有効になった後にのみ有効になります。

### 可用性 {#availability}

-   `SURVIVAL_PREFERENCE` for [SQL の配置ルール](/placement-rules-in-sql.md) [#38605](https://github.com/pingcap/tidb/issues/38605) @ [ノールーシュ](https://github.com/nolouch)の構成をサポート

    `SURVIVAL_PREFERENCES`データの災害時の生存性を高めるためのデータ生存性設定を提供します。 `SURVIVAL_PREFERENCE`を指定すると、次のことを制御できます。

    -   クラウド リージョン全体にデプロイされた TiDB クラスターの場合、クラウド リージョンに障害が発生した場合、指定されたデータベースまたはテーブルは別のクラウド リージョンで存続できます。
    -   単一のクラウド リージョンにデプロイされた TiDB クラスターの場合、可用性ゾーンに障害が発生した場合、指定されたデータベースまたはテーブルは別の可用性ゾーンで存続できます。

    詳細については、 [ドキュメンテーション](/placement-rules-in-sql.md#survival-preferences)を参照してください。

-   `FLASHBACK CLUSTER TO TIMESTAMP`ステートメント[#14088](https://github.com/tikv/tikv/pull/14088) @ [定義2014](https://github.com/Defined2014) @ [Jmポテト](https://github.com/JmPotato)による DDL 操作のロールバックのサポート

    [`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-to-timestamp.md)ステートメントは、ガベージ コレクション (GC) の有効期間内の指定された時点へのクラスター全体の復元をサポートします。 TiDB v6.6.0 では、この機能により DDL 操作のロールバックのサポートが追加されています。これを使用すると、クラスター上での DML または DDL の誤操作をすばやく元に戻したり、数分以内にクラスターをロールバックしたり、タイムライン上でクラスターを複数回ロールバックして、特定のデータ変更がいつ発生したかを判断したりすることができます。

    詳細については、 [ドキュメンテーション](/sql-statements/sql-statement-flashback-to-timestamp.md)を参照してください。

### SQL {#sql}

-   MySQL 互換の外部キー制約をサポート (実験的) [#18209](https://github.com/pingcap/tidb/issues/18209) @ [クレイジークス520](https://github.com/crazycs520)

    TiDB v6.6.0 では、MySQL と互換性のある外部キー制約機能が導入されています。この機能は、テーブル内またはテーブル間の参照、制約の検証、およびカスケード操作をサポートします。この機能は、アプリケーションを TiDB に移行し、データの一貫性を維持し、データ品質を向上させ、データ モデリングを容易にするのに役立ちます。

    詳細については、 [ドキュメンテーション](/foreign-key.md)を参照してください。

-   MySQL 互換の複数値インデックスのサポート (実験的) [#39592](https://github.com/pingcap/tidb/issues/39592) @ [ションジウェイ](https://github.com/xiongjiwei) @ [qw4990](https://github.com/qw4990)

    TiDB は、v6.6.0 で MySQL 互換の複数値インデックスを導入します。 JSON 列内の配列の値をフィルター処理するのは一般的な操作ですが、通常のインデックスではそのような操作を高速化することはできません。配列に複数値のインデックスを作成すると、フィルタリングのパフォーマンスが大幅に向上します。 JSON列の配列に多値インデックス`JSON_OVERLAPS()`ある場合、多値インデックスを使用して`MEMBER OF()`関数で検索条件を絞り込むことができるため、I/O `JSON_CONTAINS()`量が大幅に削減され、動作速度が向上します。

    多値インデックスの導入により、TiDB の JSON データ型サポートがさらに強化され、TiDB と MySQL 8.0 の互換性も向上します。

    詳細については、 [ドキュメンテーション](/sql-statements/sql-statement-create-index.md#multi-valued-indexes)を参照してください。

### DB操作 {#db-operations}

-   リソースを消費するタスクのための読み取り専用storageノードの構成をサポート @ [v01dstar](https://github.com/v01dstar)

    本番環境では、一部の読み取り専用操作が定期的に大量のリソースを消費し、バックアップや大規模なデータの読み取りと分析など、クラスター全体のパフォーマンスに影響を与える可能性があります。 TiDB v6.6.0 は、オンライン アプリケーションへの影響を軽減するために、リソースを消費する読み取り専用タスク用の読み取り専用storageノードの構成をサポートしています。現在、TiDB、TiSpark、およびBR は、読み取り専用storageノードからのデータの読み取りをサポートしています。 [ステップ](/best-practices/readonly-nodes.md#procedures)に従って読み取り専用storageノードを構成し、システム変数`tidb_replica_read` 、TiSpark 構成項目`spark.tispark.replica_read` 、または br コマンド ライン引数`--replica-read-label`を通じてデータを読み取る場所を指定して、クラスターのパフォーマンスの安定性を確保できます。

    詳細については、 [ドキュメンテーション](/best-practices/readonly-nodes.md)を参照してください。

-   `store-io-pool-size` [#13964](https://github.com/tikv/tikv/issues/13964) @ [リククスサシネーター](https://github.com/LykxSassinator)の動的変更をサポート

    TiKV 構成項目[`raftstore.store-io-pool-size`](/tikv-configuration-file.md#store-io-pool-size-new-in-v530)は、 Raft I/O タスクを処理するスレッドの許容数を指定します。これは、TiKV パフォーマンスをチューニングするときに調整できます。 v6.6.0 より前では、この構成項目は動的に変更できません。 v6.6.0 以降、サーバーを再起動せずにこの構成を変更できるようになりました。これは、より柔軟なパフォーマンス チューニングを意味します。

    詳細については、 [ドキュメンテーション](/dynamic-config.md)を参照してください。

-   TiDB クラスターの初期化時に実行される SQL スクリプトの指定をサポート[#35624](https://github.com/pingcap/tidb/issues/35624) @ [モルゴ](https://github.com/morgo)

    TiDB クラスターを初めて起動するときは、コマンド ライン パラメーター`--initialize-sql-file`を構成することで、実行する SQL スクリプトを指定できます。この機能は、システム変数の値の変更、ユーザーの作成、権限の権限などの操作を実行する必要がある場合に使用できます。

    詳細については、 [ドキュメンテーション](/tidb-configuration-file.md#initialize-sql-file-new-in-v660)を参照してください。

-   TiDB Data Migration (DM) は、TiDB Lightning の物理インポート モードと統合され、完全な移行 (実験的) @ [ランス6716](https://github.com/lance6716)のパフォーマンスが最大 10 倍向上します。

    v6.6.0 では、DM の完全移行機能がTiDB Lightningの物理インポート モードと統合されており、これにより DM は完全データ移行のパフォーマンスを最大 10 倍向上させ、大規模なデータ ボリュームのシナリオで移行時間を大幅に短縮できます。

    v6.6.0 より前のバージョンでは、大規模なデータ ボリュームのシナリオでは、高速完全データ移行のためにTiDB Lightningで物理インポート タスクを個別に構成し、次に増分データ移行に DM を使用する必要がありましたが、これは複雑な構成でした。 v6.6.0 以降、 TiDB Lightningタスクを構成することなく、大量のデータを移行できるようになりました。 1 つの DM タスクで移行を完了できます。

    詳細については、 [ドキュメンテーション](/dm/dm-precheck.md#check-items-for-physical-import)を参照してください。

-   TiDB Lightning は、ソース ファイルとターゲット テーブル間の列名の不一致の問題に対処するための新しい設定パラメータ`"header-schema-match"`を追加 @ [dsダシュン](https://github.com/dsdashun)

    v6.6.0 では、 TiDB Lightning に新しいプロファイル パラメータ`"header-schema-match"`が追加されています。デフォルト値は`true`です。これは、ソース CSV ファイルの最初の行が列名として扱われ、ターゲット テーブルの最初の行と一貫性があることを意味します。 CSV テーブル ヘッダーのフィールド名がターゲット テーブルの列名と一致しない場合は、この構成を`false`に設定できます。 TiDB Lightning はエラーを無視し、ターゲット テーブルの列の順序でデータのインポートを続行します。

    詳細については、 [ドキュメンテーション](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)を参照してください。

-   TiDB Lightning は、キーと値のペアを TiKV [#41163](https://github.com/pingcap/tidb/issues/41163) @ [ゴズスキー](https://github.com/gozssky)に送信する際の圧縮転送の有効化をサポートします

    v6.6.0 以降、 TiDB Lightning は、TiKV に送信する際のネットワーク転送用にローカルでエンコードおよびソートされたキーと値のペアの圧縮をサポートするため、ネットワーク上で転送されるデータ量が削減され、ネットワーク帯域幅のオーバーヘッドが削減されます。この機能がサポートされる前の以前の TiDB バージョンでは、 TiDB Lightning は比較的広いネットワーク帯域幅を必要とし、データ量が多い場合には高額なトラフィック料金が発生します。

    この機能はデフォルトでは無効になっています。有効にするには、 TiDB Lightningの`compress-kv-pairs`設定項目を`"gzip"`または`"gz"`に設定します。

    詳細については、 [ドキュメンテーション](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)を参照してください。

-   TiKV-CDC ツールは現在 GA であり、RawKV [#48](https://github.com/tikv/migration/issues/48) @ [沢民州](https://github.com/zeminzhou) @ [ハオジンミン](https://github.com/haojinming) @ [ピンギュ](https://github.com/pingyu)のデータ変更のサブスクライブをサポートしています。

    TiKV-CDC は、TiKV クラスター用の CDC (変更データ キャプチャ) ツールです。 TiKV と PD は、TiDB なしで使用される場合、RawKV と呼ばれる KV データベースを構成できます。 TiKV-CDC は、RawKV のデータ変更のサブスクライブと、ダウンストリーム TiKV クラスターへのリアルタイムのレプリケーションをサポートしているため、RawKV のクラスター間レプリケーションが可能になります。

    詳細については、 [ドキュメンテーション](https://tikv.org/docs/latest/concepts/explore-tikv-features/cdc/cdc/)を参照してください。

-   TiCDC は、Kafka チェンジフィード上の単一テーブルのスケールアウトと、複数の TiCDC ノードへのチェンジフィードの分散 (実験的) [#7720](https://github.com/pingcap/tiflow/issues/7720) @ [オーバーヴィーナス](https://github.com/overvenus)をサポートしています。

    v6.6.0 より前では、アップストリームのテーブルが大量の書き込みを受け入れると、このテーブルのレプリケーション機能をスケールアウトできず、レプリケーションのレイテンシーが増加します。 TiCDC v6.6.0 以降。上流テーブルの変更フィードは、Kafka シンク内の複数の TiCDC ノードに分散できます。これは、単一テーブルのレプリケーション機能がスケールアウトされることを意味します。

    詳細については、 [ドキュメンテーション](/ticdc/ticdc-sink-to-kafka.md#scale-out-the-load-of-a-single-large-table-to-multiple-ticdc-nodes)を参照してください。

-   [ゴーム](https://github.com/go-gorm/gorm)では、TiDB 統合テストが追加されます。現在、TiDB は GORM によってサポートされるデフォルトのデータベースです。 [#6014](https://github.com/go-gorm/gorm/pull/6014) @ [アイスマップ](https://github.com/Icemap)

    -   v1.4.6 では、 [GORM MySQL ドライバー](https://github.com/go-gorm/mysql) TiDB [#104](https://github.com/go-gorm/mysql/pull/104)の`AUTO_RANDOM`属性に適合します。
    -   v1.4.6 では、TiDB に接続するときに、 `AutoMigrate` [#105](https://github.com/go-gorm/mysql/pull/105)の間に`Unique`フィールドの`Unique`属性を変更できない問題[GORM MySQL ドライバー](https://github.com/go-gorm/mysql)修正されます。
    -   [GORM ドキュメント](https://github.com/go-gorm/gorm.io) TiDB をデフォルトのデータベースとして挙げています[#638](https://github.com/go-gorm/gorm.io/pull/638)

    詳細については、 [GORM ドキュメント](https://gorm.io/docs/index.html)を参照してください。

### 可観測性 {#observability}

-   TiDB ダッシュボード[#781](https://github.com/pingcap/tidb-dashboard/issues/781) @ [イニシュ9506](https://github.com/YiniXu9506)での SQL バインディングの迅速な作成をサポート

    TiDB v6.6.0 はステートメント履歴からの SQL バインディングの作成をサポートしているため、TiDB ダッシュボード上の特定のプランに SQL ステートメントを迅速にバインドできます。

    この機能は、ユーザー フレンドリーなインターフェイスを提供することで、TiDB でプランをバインドするプロセスを簡素化し、操作の複雑さを軽減し、プラン バインド プロセスの効率とユーザー エクスペリエンスを向上させます。

    詳細については、 [ドキュメンテーション](/dashboard/dashboard-statement-details.md#fast-plan-binding)を参照してください。

-   実行プランのキャッシュに関する警告を追加 @ [qw4990](https://github.com/qw4990)

    実行プランをキャッシュできない場合、TiDB は診断を容易にするために警告で理由を示します。例えば：

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

    前述の例では、オプティマイザーは非 INT 型を INT 型に変換し、パラメーターの変更によって実行プランが変更される可能性があるため、TiDB はプランをキャッシュしません。

    詳細については、 [ドキュメンテーション](/sql-prepared-plan-cache.md#diagnostics-of-prepared-plan-cache)を参照してください。

-   スロークエリログ[#39893](https://github.com/pingcap/tidb/issues/39893) @ [時間と運命](https://github.com/time-and-fate)に`Warnings`フィールドを追加します。

    TiDB v6.6.0 では、パフォーマンスの問題の診断に役立つように、スロー クエリ ログに`Warnings`フィールドが追加されます。このフィールドには、遅いクエリの実行中に生成された警告が記録されます。 TiDB ダッシュボードの低速クエリ ページでも警告を表示できます。

    詳細については、 [ドキュメンテーション](/identify-slow-queries.md)を参照してください。

-   SQL 実行プラン[#38779](https://github.com/pingcap/tidb/issues/38779) @ [イーサール](https://github.com/Yisaer)の生成を自動的にキャプチャします。

    実行計画の問題のトラブルシューティングのプロセスにおいて、 `PLAN REPLAYER`シーンを保存し、診断の効率を向上させるのに役立ちます。ただし、シナリオによっては、一部の実行計画の生成を自由に再現できないため、診断作業がより困難になります。

    このような問題に対処するために、TiDB v6.6.0 では自動キャプチャの機能が`PLAN REPLAYER`されています。 `PLAN REPLAYER CAPTURE`コマンドでは、対象となるSQL文を事前に登録し、同時に対象となる実行計画も指定できます。 TiDB は、登録されたターゲットに一致する SQL ステートメントまたは実行プランを検出すると、 `PLAN REPLAYER`情報を自動的に生成してパッケージ化します。実行計画が不安定な場合、この機能により診断効率が向上します。

    この機能を使用するには、値[`tidb_enable_plan_replayer_capture`](/system-variables.md#tidb_enable_plan_replayer_capture) ～ `ON`を設定します。

    詳細については、 [ドキュメンテーション](/sql-plan-replayer.md#use-plan-replayer-capture)を参照してください。

-   永続的なステートメントのサポートの概要 (実験的) [#40812](https://github.com/pingcap/tidb/issues/40812) @ [モニクス](https://github.com/mornyx)

    v6.6.0 より前では、ステートメントの概要データはメモリに保存されており、TiDBサーバーを再起動すると失われます。 v6.6.0 以降、TiDB はステートメント概要の永続化をサポートしており、これにより履歴データを定期的にディスクに書き込むことができます。それまでの間、システム テーブルに対するクエリの結果は、メモリではなくディスクから取得されます。 TiDB が再起動した後も、すべての履歴データは利用可能なままになります。

    詳細については、 [ドキュメンテーション](/statement-summary-tables.md#persist-statements-summary)を参照してください。

### Security {#security}

-   TiFlash は、 TLS 証明書[#5503](https://github.com/pingcap/tiflash/issues/5503) @ [ywqzzy](https://github.com/ywqzzy)の自動ローテーションをサポートします

    v6.6.0 では、TiDB はTiFlash TLS 証明書の自動ローテーションをサポートします。コンポーネント間の暗号化されたデータ送信が有効になっている TiDB クラスターの場合、 TiFlashの TLS 証明書の有効期限が切れ、新しい証明書で再発行する必要がある場合、TiDB クラスターを再起動せずに、新しいTiFlash TLS 証明書を自動的にロードできます。さらに、TiDB クラスター内のコンポーネント間での TLS 証明書のローテーションは、TiDB クラスターの使用に影響を与えず、クラスターの高可用性が保証されます。

    詳細については、 [ドキュメンテーション](/enable-tls-between-components.md)を参照してください。

-   TiDB Lightning は、 AWS IAMロールキーとセッショントークン[#4075](https://github.com/pingcap/tidb/issues/40750) @ [オクジャン](https://github.com/okJiang)を介した Amazon S3 データへのアクセスをサポートします。

    v6.6.0 より前では、 TiDB Lightning はAWS IAM**ユーザーのアクセス キー**(各アクセス キーはアクセス キー ID とシークレット アクセス キーで構成されます) を介した S3 データへのアクセスのみをサポートしているため、一時セッション トークンを使用して S3 データにアクセスすることはできません。 v6.6.0 以降、 TiDB Lightning は、データ セキュリティを向上させるために、AWS IAM**ロールのアクセス キー + セッション トークンを**介した S3 データへのアクセスもサポートします。

    詳細については、 [ドキュメンテーション](/tidb-lightning/tidb-lightning-data-source.md#import-data-from-amazon-s3)を参照してください。

### テレメトリー {#telemetry}

-   2023 年 2 月 20 日以降、TiDB および TiDB ダッシュボード (v6.6.0 を含む) の新しいバージョンでは、 [テレメトリ機能](/telemetry.md)がデフォルトで無効になります。デフォルトのテレメトリ構成を使用する以前のバージョンからアップグレードする場合、アップグレード後にテレメトリ機能は無効になります。特定のバージョンについては、 [TiDB リリース タイムライン](/releases/release-timeline.md)を参照してください。
-   v1.11.3 以降、新しくデプロイされたTiUPではテレメトリ機能がデフォルトで無効になっています。 TiUPの以前のバージョンから v1.11.3 以降のバージョンにアップグレードした場合、テレメトリ機能はアップグレード前と同じステータスを維持します。

## 互換性の変更 {#compatibility-changes}

> **注記：**
>
> このセクションでは、v6.5.0 から現在のバージョン (v6.6.0) にアップグレードするときに知っておく必要がある互換性の変更について説明します。 v6.4.0 以前のバージョンから現在のバージョンにアップグレードする場合は、中間バージョンで導入された互換性の変更も確認する必要がある場合があります。

### MySQLの互換性 {#mysql-compatibility}

-   MySQL 互換の外部キー制約をサポート (実験的) [#18209](https://github.com/pingcap/tidb/issues/18209) @ [クレイジークス520](https://github.com/crazycs520)

    詳細については、このドキュメントの[SQL](#sql)セクションと[ドキュメンテーション](/foreign-key.md)を参照してください。

-   MySQL と互換性のある複数値インデックスのサポート (実験的) [#39592](https://github.com/pingcap/tidb/issues/39592) @ [ションジウェイ](https://github.com/xiongjiwei) @ [qw4990](https://github.com/qw4990)

    詳細については、このドキュメントの[SQL](#sql)セクションと[ドキュメンテーション](/sql-statements/sql-statement-create-index.md#multi-valued-indexes)を参照してください。

### システム変数 {#system-variables}

| 変数名                                                                                                                                                  | 種類の変更    | 説明                                                                                                                                                                                                                                                         |
| ---------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `tidb_enable_amend_pessimistic_txn`                                                                                                                  | 削除されました  | v6.5.0 以降、この変数は非推奨になりました。 v6.6.0 以降、この変数と`AMEND TRANSACTION`機能は削除されています。 TiDB は`Information schema is changed`エラーを回避するために[メタロック](/metadata-lock.md)使用します。                                                                                                  |
| `tidb_enable_concurrent_ddl`                                                                                                                         | 削除されました  | この変数は、TiDB が同時 DDL ステートメントを使用できるようにするかどうかを制御します。この変数が無効になっている場合、TiDB は古い DDL 実行フレームワークを使用し、同時 DDL 実行のサポートが制限されています。 v6.6.0 以降、この変数は削除され、TiDB は古い DDL 実行フレームワークをサポートしなくなります。                                                                                |
| `tidb_ttl_job_run_interval`                                                                                                                          | 削除されました  | この変数は、バックグラウンドでの TTL ジョブのスケジュール間隔を制御するために使用されます。 v6.6.0 以降、この変数は削除されています。これは、TiDB が TTL ランタイムを制御するためにすべてのテーブルに`TTL_JOB_INTERVAL`属性を提供しており、これは`tidb_ttl_job_run_interval`よりも柔軟であるためです。                                                                      |
| [`foreign_key_checks`](/system-variables.md#foreign_key_checks)                                                                                      | 修正済み     | この変数は、外部キー制約チェックを有効にするかどうかを制御します。デフォルト値は`OFF`から`ON`に変更されます。これは、デフォルトで外部キーのチェックが有効になることを意味します。                                                                                                                                                              |
| [`tidb_enable_foreign_key`](/system-variables.md#tidb_enable_foreign_key-new-in-v630)                                                                | 修正済み     | この変数は、外部キー機能を有効にするかどうかを制御します。デフォルト値は`OFF`から`ON`に変更されます。これは、デフォルトで外部キーが有効になることを意味します。                                                                                                                                                                       |
| `tidb_enable_general_plan_cache`                                                                                                                     | 修正済み     | この変数は、一般プラン キャッシュを有効にするかどうかを制御します。 v6.6.0 以降、この変数の名前は[`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache)に変更されます。                                                                                             |
| [`tidb_enable_historical_stats`](/system-variables.md#tidb_enable_historical_stats)                                                                  | 修正済み     | この変数は、履歴統計を有効にするかどうかを制御します。デフォルト値は`OFF`から`ON`に変更されます。これは、履歴統計がデフォルトで有効になることを意味します。                                                                                                                                                                         |
| [`tidb_enable_telemetry`](/system-variables.md#tidb_enable_telemetry-new-in-v402)                                                                    | 修正済み     | デフォルト値は`ON`から`OFF`に変更されます。これは、TiDB ではテレメトリがデフォルトで無効になっていることを意味します。                                                                                                                                                                                         |
| `tidb_general_plan_cache_size`                                                                                                                       | 修正済み     | この変数は、一般プラン キャッシュによってキャッシュできる実行プランの最大数を制御します。 v6.6.0 以降、この変数の名前は[`tidb_non_prepared_plan_cache_size`](/system-variables.md#tidb_non_prepared_plan_cache_size)に変更されます。                                                                                      |
| [`tidb_replica_read`](/system-variables.md#tidb_replica_read-new-in-v40)                                                                             | 修正済み     | TiDB が読み取り専用ノードからデータを読み取る際に使用する学習器レプリカを指定するために、この変数に新しい値オプション`learner`が追加されました。                                                                                                                                                                            |
| [`tidb_replica_read`](/system-variables.md#tidb_replica_read-new-in-v40)                                                                             | 修正済み     | TiDB クラスターの全体的な読み取り可用性を向上させるために、この変数に新しい値オプション`prefer-leader`が追加されました。このオプションが設定されている場合、TiDB はリーダー レプリカからの読み取りを優先します。リーダー レプリカのパフォーマンスが大幅に低下すると、TiDB は自動的にフォロワー レプリカから読み取ります。                                                                              |
| [`tidb_store_batch_size`](/system-variables.md#tidb_store_batch_size)                                                                                | 修正済み     | この変数は、 `IndexLookUp`オペレーターのコプロセッサータスクのバッチ サイズを制御します。 `0`バッチを無効にすることを意味します。 v6.6.0 以降、デフォルト値は`0`から`4`に変更されます。これは、リクエストのバッチごとに 4 つのコプロセッサータスクが 1 つのタスクにバッチ化されることを意味します。                                                                                      |
| [`mpp_exchange_compression_mode`](/system-variables.md#mpp_exchange_compression_mode-new-in-v660)                                                    | 新しく追加された | この変数は、MPP Exchange オペレーターのデータ圧縮モードを指定します。これは、TiDB がバージョン番号`1`の MPP 実行プランを選択すると有効になります。デフォルト値`UNSPECIFIED` 、TiDB が自動的に`FAST`圧縮モードを選択することを意味します。                                                                                                             |
| [`mpp_version`](/system-variables.md#mpp_version-new-in-v660)                                                                                        | 新しく追加された | この変数は、MPP 実行プランのバージョンを指定します。バージョンが指定されると、TiDB は MPP 実行プランの指定されたバージョンを選択します。デフォルト値`UNSPECIFIED` TiDB が自動的に最新バージョン`1`を選択することを意味します。                                                                                                                          |
| [`tidb_ddl_distribute_reorg`](https://docs.pingcap.com/tidb/v6.6/system-variables#tidb_ddl_distribute_reorg-new-in-v660)                             | 新しく追加された | この変数は、DDL 再編成フェーズの分散実行を有効にして、このフェーズを高速化するかどうかを制御します。デフォルト値`OFF`は、デフォルトでは DDL 再編成フェーズの分散実行を有効にしないことを意味します。現在、この変数は`ADD INDEX`に対してのみ有効です。                                                                                                                    |
| [`tidb_enable_historical_stats_for_capture`](/system-variables.md#tidb_enable_historical_stats_for_capture)                                          | 新しく追加された | この変数は、 `PLAN REPLAYER CAPTURE`によって取得される情報にデフォルトで履歴統計が含まれるかどうかを制御します。デフォルト値`OFF` 、履歴統計がデフォルトで含まれないことを意味します。                                                                                                                                                 |
| [`tidb_enable_plan_cache_for_param_limit`](/system-variables.md#tidb_enable_plan_cache_for_param_limit-new-in-v660)                                  | 新しく追加された | この変数は、 プリペアドプランキャッシュ が`Limit`の後に`COUNT`含む実行プランをキャッシュするかどうかを制御します。デフォルト値は`ON`です。これは、 プリペアドプランキャッシュ がそのような実行計画のキャッシュをサポートすることを意味します。 プリペアドプランキャッシュ は、10000 を超える数をカウントする`COUNT`条件を持つ実行プランのキャッシュをサポートしていないことに注意してください。                                         |
| [`tidb_enable_plan_replayer_capture`](/system-variables.md#tidb_enable_plan_replayer_capture)                                                        | 新しく追加された | この変数は、 [`PLAN REPLAYER CAPTURE`機能を計画する](/sql-plan-replayer.md#use-plan-replayer-capture-to-capture-target-plans)を有効にするかどうかを制御します。デフォルト値`OFF` `PLAN REPLAYER CAPTURE`機能を無効にすることを意味します。                                                                      |
| [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-new-in-v660)                                                      | 新しく追加された | この変数は、リソース制御機能を有効にするかどうかを制御します。デフォルト値は`OFF`です。この変数が`ON`に設定されている場合、TiDB クラスターはリソース グループに基づいたアプリケーションのリソース分離をサポートします。                                                                                                                                        |
| [`tidb_historical_stats_duration`](/system-variables.md#tidb_historical_stats_duration-new-in-v660)                                                  | 新しく追加された | この変数は、履歴統計をstorageに保持する期間を制御します。デフォルト値は 7 日です。                                                                                                                                                                                                             |
| [`tidb_index_join_double_read_penalty_cost_rate`](/system-variables.md#tidb_index_join_double_read_penalty_cost_rate-new-in-v660)                    | 新しく追加された | この変数は、インデックス結合の選択にペナルティ コストを追加するかどうかを制御します。デフォルト値`0` 、この機能がデフォルトで無効になっていることを意味します。                                                                                                                                                                         |
| [`tidb_pessimistic_txn_aggressive_locking`](https://docs.pingcap.com/tidb/v6.6/system-variables#tidb_pessimistic_txn_aggressive_locking-new-in-v660) | 新しく追加された | この変数は、悲観的トランザクションに対して拡張された悲観的ロック ウェイクアップ モデルを使用するかどうかを制御します。デフォルト値`OFF`は、デフォルトではこのようなウェイクアップ モデルを悲観的トランザクションに使用しないことを意味します。                                                                                                                                |
| [`tidb_stmt_summary_enable_persistent`](/system-variables.md#tidb_stmt_summary_enable_persistent-new-in-v660)                                        | 新しく追加された | この変数は読み取り専用です。 [ステートメントの概要の永続性](/statement-summary-tables.md#persist-statements-summary)を有効にするかどうかを制御します。この変数の値は設定項目[`tidb_stmt_summary_enable_persistent`](/tidb-configuration-file.md#tidb_stmt_summary_enable_persistent-new-in-v660)と同じです。             |
| [`tidb_stmt_summary_filename`](/system-variables.md#tidb_stmt_summary_filename-new-in-v660)                                                          | 新しく追加された | この変数は読み取り専用です。 [ステートメントの概要の永続化](/statement-summary-tables.md#persist-statements-summary)が有効な場合に永続データが書き込まれるファイルを指定します。この変数の値は設定項目[`tidb_stmt_summary_filename`](/tidb-configuration-file.md#tidb_stmt_summary_filename-new-in-v660)と同じです。                  |
| [`tidb_stmt_summary_file_max_backups`](/system-variables.md#tidb_stmt_summary_file_max_backups-new-in-v660)                                          | 新しく追加された | この変数は読み取り専用です。 [ステートメントの概要の永続化](/statement-summary-tables.md#persist-statements-summary)が有効な場合に保持できるデータ ファイルの最大数を指定します。この変数の値は設定項目[`tidb_stmt_summary_file_max_backups`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_backups-new-in-v660)と同じです。 |
| [`tidb_stmt_summary_file_max_days`](/system-variables.md#tidb_stmt_summary_file_max_days-new-in-v660)                                                | 新しく追加された | この変数は読み取り専用です。 [ステートメントの概要の永続化](/statement-summary-tables.md#persist-statements-summary)が有効な場合、永続データ ファイルを保持する最大日数を指定します。この変数の値は設定項目[`tidb_stmt_summary_file_max_days`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_days-new-in-v660)と同じです。     |
| [`tidb_stmt_summary_file_max_size`](/system-variables.md#tidb_stmt_summary_file_max_size-new-in-v660)                                                | 新しく追加された | この変数は読み取り専用です。 [ステートメントの概要の永続性](/statement-summary-tables.md#persist-statements-summary)が有効な場合、永続データ ファイルの最大サイズを指定します。この変数の値は設定項目[`tidb_stmt_summary_file_max_size`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_size-new-in-v660)と同じです。        |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーションパラメータ                                                                                                                                                                                                                                           | 種類の変更    | 説明                                                                                                                                                                                      |
| -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiKV           | `rocksdb.enable-statistics`                                                                                                                                                                                                                               | 削除されました  | この設定項目は、RocksDB 統計を有効にするかどうかを指定します。 v6.6.0以降、この項目は削除されています。 RocksDB 統計は、診断に役立つようにデフォルトですべてのクラスターに対して有効になっています。詳細は[#13942](https://github.com/tikv/tikv/pull/13942)を参照してください。            |
| TiKV           | `raftdb.enable-statistics`                                                                                                                                                                                                                                | 削除されました  | この設定項目は、 Raft RocksDB 統計を有効にするかどうかを指定します。 v6.6.0以降、この項目は削除されています。 Raft RocksDB 統計は、診断に役立つようにデフォルトですべてのクラスターに対して有効になっています。詳細は[#13942](https://github.com/tikv/tikv/pull/13942)を参照してください。 |
| TiKV           | `storage.block-cache.shared`                                                                                                                                                                                                                              | 削除されました  | v6.6.0 以降、この構成項目は削除され、ブロックキャッシュはデフォルトで有効になり、無効にすることはできません。詳細は[#12936](https://github.com/tikv/tikv/issues/12936)を参照してください。                                                              |
| DM             | `on-duplicate`                                                                                                                                                                                                                                            | 削除されました  | この構成アイテムは、完全なインポート フェーズ中に競合を解決する方法を制御します。 v6.6.0 では、新しい構成項目`on-duplicate-logical`および`on-duplicate-physical`が導入され、 `on-duplicate`が置き換えられます。                                              |
| TiDB           | [`enable-telemetry`](/tidb-configuration-file.md#enable-telemetry-new-in-v402)                                                                                                                                                                            | 修正済み     | v6.6.0 以降、デフォルト値は`true`から`false`に変更されます。これは、TiDB ではテレメトリがデフォルトで無効になっていることを意味します。                                                                                                        |
| TiKV           | [`rocksdb.defaultcf.block-size`](/tikv-configuration-file.md#block-size)と[`rocksdb.writecf.block-size`](/tikv-configuration-file.md#block-size)                                                                                                           | 修正済み     | デフォルト値は`64K`から`32K`に変更されます。                                                                                                                                                             |
| TiKV           | [`rocksdb.defaultcf.block-cache-size`](/tikv-configuration-file.md#block-cache-size) [`rocksdb.writecf.block-cache-size`](/tikv-configuration-file.md#block-cache-size) [`rocksdb.lockcf.block-cache-size`](/tikv-configuration-file.md#block-cache-size) | 廃止されました  | v6.6.0 以降、これらの構成項目は非推奨になります。詳細は[#12936](https://github.com/tikv/tikv/issues/12936)を参照してください。                                                                                            |
| PD             | [`enable-telemetry`](/pd-configuration-file.md#enable-telemetry)                                                                                                                                                                                          | 修正済み     | v6.6.0 以降、デフォルト値は`true`から`false`に変更されます。これは、TiDB ダッシュボードでテレメトリがデフォルトで無効になることを意味します。                                                                                                     |
| DM             | [`import-mode`](/dm/task-configuration-file-full.md)                                                                                                                                                                                                      | 修正済み     | この構成項目の可能な値は、 `"sql"`および`"loader"`から`"logical"`および`"physical"`に変更されます。デフォルト値は`"logical"`で、これは TiDB Lightning の論理インポート モードを使用してデータをインポートすることを意味します。                                      |
| TiFlash        | [`profile.default.max_memory_usage_for_all_queries`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                                                                                                                                    | 修正済み     | すべてのクエリで生成される中間データのメモリ使用量の制限を指定します。 v6.6.0 以降、デフォルト値は`0`から`0.8`に変更されます。これは、制限が合計メモリの 80% であることを意味します。                                                                                   |
| TiCDC          | [`consistent.storage`](/ticdc/ticdc-sink-to-mysql.md#prerequisites)                                                                                                                                                                                       | 修正済み     | この構成項目は、REDO ログのバックアップが保存されるパスを指定します。 `scheme` 、GCS、および Azure にさらに 2 つの値オプションが追加されます。                                                                                                   |
| TiDB           | [`initialize-sql-file`](/tidb-configuration-file.md#initialize-sql-file-new-in-v660)                                                                                                                                                                      | 新しく追加された | この構成項目は、TiDB クラスターの初回起動時に実行される SQL スクリプトを指定します。デフォルト値は空です。                                                                                                                              |
| TiDB           | [`tidb_stmt_summary_enable_persistent`](/tidb-configuration-file.md#tidb_stmt_summary_enable_persistent-new-in-v660)                                                                                                                                      | 新しく追加された | この構成項目は、ステートメントの要約の永続性を有効にするかどうかを制御します。デフォルト値は`false`で、この機能はデフォルトでは有効になっていないことを意味します。                                                                                                   |
| TiDB           | [`tidb_stmt_summary_file_max_backups`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_backups-new-in-v660)                                                                                                                                        | 新しく追加された | ステートメント概要の永続化が有効になっている場合、この構成では、永続化できるデータ ファイルの最大数を指定します。 `0`ファイル数に制限がないことを意味します。                                                                                                       |
| TiDB           | [`tidb_stmt_summary_file_max_days`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_days-new-in-v660)                                                                                                                                              | 新しく追加された | ステートメント概要の永続性が有効になっている場合、この構成は永続データ ファイルを保持する最大日数を指定します。                                                                                                                                |
| TiDB           | [`tidb_stmt_summary_file_max_size`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_size-new-in-v660)                                                                                                                                              | 新しく追加された | ステートメント概要の永続性が有効になっている場合、この構成は永続データ ファイルの最大サイズ (MiB 単位) を指定します。                                                                                                                         |
| TiDB           | [`tidb_stmt_summary_filename`](/tidb-configuration-file.md#tidb_stmt_summary_filename-new-in-v660)                                                                                                                                                        | 新しく追加された | ステートメントの概要の永続性が有効になっている場合、この構成は永続データが書き込まれるファイルを指定します。                                                                                                                                  |
| TiKV           | [`resource-control.enabled`](/tikv-configuration-file.md#resource-control)                                                                                                                                                                                | 新しく追加された | 対応するリソース グループのリクエスト ユニット (RU) に従って、ユーザーのフォアグラウンド読み取り/書き込みリクエストのスケジューリングを有効にするかどうか。デフォルト値は`false`で、対応するリソース グループの RU に従ってスケジューリングを無効にすることを意味します。                                         |
| TiKV           | [`storage.engine`](/tikv-configuration-file.md#engine-new-in-v660)                                                                                                                                                                                        | 新しく追加された | この構成項目は、storageエンジンのタイプを指定します。値のオプションは`"raft-kv"`と`"partitioned-raft-kv"`です。この設定項目はクラスターの作成時にのみ指定でき、一度指定すると変更することはできません。                                                                |
| TiKV           | [`rocksdb.write-buffer-flush-oldest-first`](/tikv-configuration-file.md#write-buffer-flush-oldest-first-new-in-v660)                                                                                                                                      | 新しく追加された | この構成項目は、現在の RocksDB の`memtable`のメモリ使用量がしきい値に達したときに使用されるフラッシュ戦略を指定します。                                                                                                                   |
| TiKV           | [`rocksdb.write-buffer-limit`](/tikv-configuration-file.md#write-buffer-limit-new-in-v660)                                                                                                                                                                | 新しく追加された | この構成項目は、単一の TiKV 内のすべての RocksDB インスタンスの`memtable`によって使用される合計メモリの制限を指定します。デフォルト値は、マシンの合計メモリの 25% です。                                                                                     |
| PD             | [`pd-server.enable-gogc-tuner`](/pd-configuration-file.md#enable-gogc-tuner-new-in-v660)                                                                                                                                                                  | 新しく追加された | この設定項目は、デフォルトでは無効になっている GOGC チューナーを有効にするかどうかを制御します。                                                                                                                                     |
| PD             | [`pd-server.gc-tuner-threshold`](/pd-configuration-file.md#gc-tuner-threshold-new-in-v660)                                                                                                                                                                | 新しく追加された | この構成項目は、GOGC をチューニングするための最大メモリしきい値比率を指定します。デフォルト値は`0.6`です。                                                                                                                              |
| PD             | [`pd-server.server-memory-limit-gc-trigger`](/pd-configuration-file.md#server-memory-limit-gc-trigger-new-in-v660)                                                                                                                                        | 新しく追加された | この設定項目は、PD が GC をトリガーしようとするしきい値比率を指定します。デフォルト値は`0.7`です。                                                                                                                                 |
| PD             | [`pd-server.server-memory-limit`](/pd-configuration-file.md#server-memory-limit-new-in-v660)                                                                                                                                                              | 新しく追加された | この設定項目は、PD インスタンスのメモリ制限率を指定します。値`0`はメモリ制限がないことを意味します。                                                                                                                                   |
| TiCDC          | [`scheduler.region-per-span`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)                                                                                                                                                      | 新しく追加された | この構成項目は、リージョンの数に基づいてテーブルを複数のレプリケーション範囲に分割するかどうかを制御します。これらの範囲は複数の TiCDC ノードによってレプリケートできます。デフォルト値は`50000`です。                                                                              |
| TiDB Lightning | [`compress-kv-pairs`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)                                                                                                                                                                | 新しく追加された | この構成項目は、物理インポート モードで KV ペアを TiKV に送信するときに圧縮を有効にするかどうかを制御します。デフォルト値は空で、圧縮が有効になっていないことを意味します。                                                                                             |
| DM             | [`checksum-physical`](/dm/task-configuration-file-full.md)                                                                                                                                                                                                | 新しく追加された | この構成項目は、DM がインポート後にデータの整合性を検証するためにテーブルごとに`ADMIN CHECKSUM TABLE <table>`を実行するかどうかを制御します。デフォルト値は`"required"`で、インポート後に管理チェックサムを実行します。チェックサムが失敗した場合、DM はタスクを一時停止するため、失敗を手動で処理する必要があります。     |
| DM             | [`disk-quota-physical`](/dm/task-configuration-file-full.md)                                                                                                                                                                                              | 新しく追加された | この設定項目はディスク クォータを設定します。 TiDB Lightningの[`disk-quota`構成](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#configure-disk-quota-new-in-v620)に相当します。                           |
| DM             | [`on-duplicate-logical`](/dm/task-configuration-file-full.md)                                                                                                                                                                                             | 新しく追加された | この構成項目は、DM が論理インポート モードで競合するデータを解決する方法を制御します。デフォルト値は`"replace"`で、新しいデータを使用して既存のデータを置き換えることを意味します。                                                                                       |
| DM             | [`on-duplicate-physical`](/dm/task-configuration-file-full.md)                                                                                                                                                                                            | 新しく追加された | この構成項目は、DM が物理インポート モードで競合するデータを解決する方法を制御します。デフォルト値は`"none"`で、競合するデータを解決しないことを意味します。 `"none"`のパフォーマンスは最高ですが、ダウンストリーム データベースでデータの不整合が発生する可能性があります。                                       |
| DM             | [`sorting-dir-physical`](/dm/task-configuration-file-full.md)                                                                                                                                                                                             | 新しく追加された | この設定項目は、物理インポート モードでのローカル KV ソートに使用されるディレクトリを指定します。デフォルト値は`dir`構成と同じです。                                                                                                                 |
| 同期差分インスペクター    | [`skip-non-existing-table`](/sync-diff-inspector/sync-diff-inspector-overview.md#configuration-file-description)                                                                                                                                          | 新しく追加された | この構成項目は、ダウンストリームのテーブルがアップストリームに存在しない場合に、アップストリームとダウンストリームのデータ整合性のチェックをスキップするかどうかを制御します。                                                                                                 |
| ティスパーク         | [`spark.tispark.replica_read`](/tispark-overview.md#tispark-configurations)                                                                                                                                                                               | 新しく追加された | この構成項目は、読み取るレプリカのタイプを制御します。値のオプションは`leader` 、 `follower` 、および`learner`です。                                                                                                               |
| ティスパーク         | [`spark.tispark.replica_read.label`](/tispark-overview.md#tispark-configurations)                                                                                                                                                                         | 新しく追加された | この構成アイテムは、ターゲット TiKV ノードのラベルを設定するために使用されます。                                                                                                                                             |

### その他 {#others}

-   動的変更のサポート[`store-io-pool-size`](/tikv-configuration-file.md#store-io-pool-size-new-in-v530) 。これにより、より柔軟な TiKV パフォーマンスのチューニングが容易になります。
-   `LIMIT`句の制限を削除し、実行パフォーマンスを向上させます。
-   v6.6.0 以降、 BR はv6.1.0 より前のクラスターへのデータの復元をサポートしません。
-   v6.6.0 以降、TiDB は、潜在的な正確性の問題のため、パーティション化されたテーブルの列タイプの変更をサポートしなくなりました。

## 改善点 {#improvements}

-   TiDB

    -   TTL バックグラウンド クリーニング タスクのスケジュール メカニズムを改善し、単一テーブルのクリーニング タスクを複数のサブタスクに分割し、複数の TiDB ノードで同時に実行するようにスケジュールできるようにしました[#40361](https://github.com/pingcap/tidb/issues/40361) @ [ヤンケオ](https://github.com/YangKeao)
    -   デフォルト以外の区切り文字[#39662](https://github.com/pingcap/tidb/issues/39662) @ [むじょん](https://github.com/mjonss)を設定した後に複数のステートメントを実行することによって返される結果の列名の表示を最適化します。
    -   警告メッセージが生成された後のステートメントの実行効率を最適化します[#39702](https://github.com/pingcap/tidb/issues/39702) @ [ティエンチャイアマオ](https://github.com/tiancaiamao)
    -   `ADD INDEX` (実験的) [#37119](https://github.com/pingcap/tidb/issues/37119) @ [ジムララ](https://github.com/zimulala)の分散データ バックフィルをサポート
    -   列[#38356](https://github.com/pingcap/tidb/issues/38356) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)のデフォルト値として`CURDATE()`の使用をサポート
    -   `partial order prop push down`は LIST タイプのパーティションテーブル[#40273](https://github.com/pingcap/tidb/issues/40273) @ [ウィノロス](https://github.com/winoros)をサポートするようになりました。
    -   オプティマイザーのヒントと実行プランのバインディング間の競合に関するエラー メッセージを追加[#40910](https://github.com/pingcap/tidb/issues/40910) @ [懐かしい](https://github.com/Reminiscent)
    -   一部のシナリオでプラン キャッシュを使用する場合、最適でないプランを回避するためにプラン キャッシュ戦略を最適化します[#40312](https://github.com/pingcap/tidb/pull/40312) [#40218](https://github.com/pingcap/tidb/pull/40218) [#40280](https://github.com/pingcap/tidb/pull/40280) [#41136](https://github.com/pingcap/tidb/pull/41136) [#40686](https://github.com/pingcap/tidb/pull/40686) @ [qw4990](https://github.com/qw4990)
    -   期限切れの領域キャッシュを定期的にクリアして、メモリリークとパフォーマンスの低下を回避します[#40461](https://github.com/pingcap/tidb/issues/40461) @ [スティックナーフ](https://github.com/sticnarf)
    -   `MODIFY COLUMN`はパーティション テーブル[#39915](https://github.com/pingcap/tidb/issues/39915) @ [wjhuang2016](https://github.com/wjhuang2016)ではサポートされません
    -   パーティションテーブルが依存する列の名前変更を無効にする[#40150](https://github.com/pingcap/tidb/issues/40150) @ [むじょん](https://github.com/mjonss)
    -   パーティションテーブルテーブルが依存する列が削除されたときに報告されるエラー メッセージを調整します[#38739](https://github.com/pingcap/tidb/issues/38739) @ [ジフフスト](https://github.com/jiyfhust)
    -   `FLASHBACK CLUSTER`チェックに失敗した場合にリトライする仕組みを追加`min-resolved-ts` [#39836](https://github.com/pingcap/tidb/issues/39836) @ [定義2014](https://github.com/Defined2014)

-   TiKV

    -   Partitioned-raft-kv モードの一部のパラメーターのデフォルト値を最適化します。TiKV 構成項目`storage.block-cache.capacity`のデフォルト値は 45% から 30% に調整され、デフォルト値`region-split-size`は`96MiB`から`10GiB`に調整されます。 raft-kv モードを使用し、 `enable-region-bucket` `true`である場合、デフォルトでは`region-split-size` 1 GiB に調整されます。 [#12842](https://github.com/tikv/tikv/issues/12842) @ [トニーシュクキ](https://github.com/tonyxuqqi)
    -   Raftstoreの非同期書き込み[#13730](https://github.com/tikv/tikv/issues/13730) @ [コナー1996](https://github.com/Connor1996)での優先スケジューリングのサポート
    -   1 コア未満の CPU での TiKV の起動をサポート[#13586](https://github.com/tikv/tikv/issues/13586) [#13752](https://github.com/tikv/tikv/issues/13752) [#14017](https://github.com/tikv/tikv/issues/14017) @ [アンドロイドデータベース](https://github.com/andreid-db)
    -   Raftstore の遅いスコアの新しい検出メカニズムを最適化し、 `evict-slow-trend-scheduler` [#14131](https://github.com/tikv/tikv/issues/14131) @ [インナー](https://github.com/innerr)を追加します
    -   RocksDB のブロックキャッシュを強制的に共有し、CF [#12936](https://github.com/tikv/tikv/issues/12936) @ [ビジージェイ](https://github.com/busyjay)に従ってブロックキャッシュを個別に設定することはサポートされなくなりました。

-   PD

    -   OOM 問題を軽減するためのグローバルメモリしきい値の管理のサポート (実験的) [#5827](https://github.com/tikv/pd/issues/5827) @ [フネス](https://github.com/hnes)
    -   GC チューナーを追加して GC 圧力を軽減します (実験的) [#5827](https://github.com/tikv/pd/issues/5827) @ [フネス](https://github.com/hnes)
    -   異常なノード[#5808](https://github.com/tikv/pd/pull/5808) @ [インナー](https://github.com/innerr)を検出してスケジュールするために`evict-slow-trend-scheduler`スケジューラを追加します
    -   キースペース[#5293](https://github.com/tikv/pd/issues/5293) @ [アメーバ原生動物](https://github.com/AmoebaProtozoa)を管理するキースペース マネージャーを追加します。

-   TiFlash

    -   TiFlashデータ スキャン プロセスにおける MVCC フィルタリング操作を分離する独立した MVCC ビットマップ フィルタをサポートします。これにより、データ スキャン プロセス[#6296](https://github.com/pingcap/tiflash/issues/6296) @ [ジンヘリン](https://github.com/JinheLin)の将来の最適化のための基盤が提供されます。
    -   クエリがない場合、 TiFlashのメモリ使用量を最大 30% 削減[#6589](https://github.com/pingcap/tiflash/pull/6589) @ [ホンユニャン](https://github.com/hongyunyan)

-   ツール

    -   バックアップと復元 (BR)

        -   TiKV 側でのログ バックアップ ファイルのダウンロードの同時実行性を最適化し、通常のシナリオ[#14206](https://github.com/tikv/tikv/issues/14206) @ [ユジュンセン](https://github.com/YuJuncen)での PITR リカバリのパフォーマンスを向上させます。

    -   TiCDC

        -   バッチ`UPDATE` DML ステートメントをサポートして、TiCDC レプリケーションのパフォーマンス[#8084](https://github.com/pingcap/tiflow/issues/8084) @ [咸陽飛](https://github.com/amyangfei)を向上させます。
        -   MQ シンクと MySQL シンクを非同期モードで実装して、シンクのスループットを向上させます[#5928](https://github.com/pingcap/tiflow/issues/5928) @ [ひっくり返る](https://github.com/hicqu) @ [こんにちはラスティン](https://github.com/hi-rustin)

    -   TiDB データ移行 (DM)

        -   DM アラート ルールとコンテンツの最適化[#7376](https://github.com/pingcap/tiflow/issues/7376) @ [D3ハンター](https://github.com/D3Hunter)

            以前は、関連エラーが発生するたびに、「DM_XXX_process_exits_with_error」のようなアラートが生成されていました。ただし、一部のアラートはアイドル状態のデータベース接続によって発生し、再接続後に回復できます。このような種類のアラートを減らすために、DM はエラーを 2 つのタイプ (自動的に回復可能なエラーと回復不可能なエラー) に分類します。

            -   自動的に回復可能なエラーの場合、DM はエラーが 2 分以内に 3 回以上発生した場合にのみアラートを報告します。
            -   自動的に回復できないエラーの場合、DM は元の動作を維持し、すぐにアラートを報告します。

        -   非同期/バッチ リレー ライター[#4287](https://github.com/pingcap/tiflow/issues/4287) @ [GMHDBJD](https://github.com/GMHDBJD)を追加してリレーのパフォーマンスを最適化します。

    -   TiDB Lightning

        -   物理インポートモードはキースペース[#40531](https://github.com/pingcap/tidb/issues/40531) @ [オスマンサス](https://github.com/iosmanthus)をサポートします
        -   `lightning.max-error` [#40743](https://github.com/pingcap/tidb/issues/40743) @ [dsダシュン](https://github.com/dsdashun)による競合の最大数の設定をサポート
        -   BOM ヘッダー[#40744](https://github.com/pingcap/tidb/issues/40744) @ [dsダシュン](https://github.com/dsdashun)を含む CSV データ ファイルのインポートをサポート
        -   TiKV フロー制限エラーが発生した場合は処理ロジックを最適化し、代わりに他の利用可能なリージョンを試します[#40205](https://github.com/pingcap/tidb/issues/40205) @ [ランス6716](https://github.com/lance6716)
        -   インポート中のテーブル外部キーのチェックを無効にする[#40027](https://github.com/pingcap/tidb/issues/40027) @ [ゴズスキー](https://github.com/gozssky)

    -   Dumpling

        -   外部キー[#39913](https://github.com/pingcap/tidb/issues/39913) @ [リチュンジュ](https://github.com/lichunzhu)の設定のエクスポートをサポート

    -   同期差分インスペクター

        -   新しいパラメータ`skip-non-existing-table`を追加して、ダウンストリームのテーブルがアップストリームに存在しない場合に、アップストリームとダウンストリームのデータ整合性のチェックをスキップするかどうかを制御します[#692](https://github.com/pingcap/tidb-tools/issues/692) @ [リチュンジュ](https://github.com/lichunzhu) @ [リウメンギャ94](https://github.com/liumengya94)

## バグの修正 {#bug-fixes}

-   TiDB

    -   不正な`datetime`値[#39336](https://github.com/pingcap/tidb/issues/39336) @ [シュイファングリーンアイズ](https://github.com/xuyifangreeneyes)が原因で統計収集タスクが失敗する問題を修正します。
    -   テーブル作成[#38189](https://github.com/pingcap/tidb/issues/38189) @ [シュイファングリーンアイズ](https://github.com/xuyifangreeneyes)の後に`stats_meta`が作成されない問題を修正
    -   DDL データ バックフィル[#24427](https://github.com/pingcap/tidb/issues/24427) @ [むじょん](https://github.com/mjonss)を実行するときにトランザクションで頻繁に発生する書き込み競合を修正しました。
    -   インジェスト モード[#39641](https://github.com/pingcap/tidb/issues/39641) @ [タンジェンタ](https://github.com/tangenta)を使用して空のテーブルにインデックスを作成できない場合がある問題を修正
    -   スロークエリログの`wait_ts`同じトランザクション[#39713](https://github.com/pingcap/tidb/issues/39713) @ [トンスネークリン](https://github.com/TonsnakeLin)内の異なる SQL ステートメントで同じであるという問題を修正します。
    -   行レコード[#39570](https://github.com/pingcap/tidb/issues/39570) @ [wjhuang2016](https://github.com/wjhuang2016)の削除プロセス中に列を追加すると、 `Assertion Failed`エラーが報告される問題を修正します。
    -   列タイプ[#39643](https://github.com/pingcap/tidb/issues/39643) @ [ジムララ](https://github.com/zimulala)を変更すると`not a DDL owner`エラーが報告される問題を修正
    -   `AUTO_INCREMENT`列[#38950](https://github.com/pingcap/tidb/issues/38950) @ [ドゥーシール9](https://github.com/Dousir9)の自動インクリメント値を使い果たした後に行を挿入するときにエラーが報告されない問題を修正します。
    -   式インデックス[#39784](https://github.com/pingcap/tidb/issues/39784) @ [定義2014](https://github.com/Defined2014)を作成するときに`Unknown column`エラーが報告される問題を修正
    -   生成された式にこのテーブル[#39826](https://github.com/pingcap/tidb/issues/39826) @ [定義2014](https://github.com/Defined2014)の名前が含まれている場合、名前を変更したテーブルにデータを挿入できない問題を修正します。
    -   列が書き込み専用[#40192](https://github.com/pingcap/tidb/issues/40192) @ [ヤンケオ](https://github.com/YangKeao)の場合、 `INSERT ignore`ステートメントでデフォルト値を入力できない問題を修正します。
    -   リソース管理モジュール[#40546](https://github.com/pingcap/tidb/issues/40546) @ [ジムララ](https://github.com/zimulala)を無効にするとリソースが解放されない問題を修正
    -   TTL タスクが時間[#40109](https://github.com/pingcap/tidb/issues/40109) @ [ヤンケオ](https://github.com/YangKeao)で統計更新をトリガーできない問題を修正
    -   キー範囲[#40158](https://github.com/pingcap/tidb/issues/40158) @ [ティエンチャイアマオ](https://github.com/tiancaiamao)を構築するときに TiDB が`NULL`値を適切に処理しないため、予期しないデータが読み取られる問題を修正
    -   `MODIFT COLUMN`ステートメントが列[#40164](https://github.com/pingcap/tidb/issues/40164) @ [wjhuang2016](https://github.com/wjhuang2016)のデフォルト値も変更する場合、不正な値がテーブルに書き込まれる問題を修正します。
    -   テーブル[#38436](https://github.com/pingcap/tidb/issues/38436) @ [タンジェンタ](https://github.com/tangenta)に多数のリージョンがある場合、無効なリージョンキャッシュによりインデックスの追加操作が非効率になる問題を修正
    -   自動インクリメント ID [#40584](https://github.com/pingcap/tidb/issues/40584) @ [ドゥーシール9](https://github.com/Dousir9)の割り当て時に発生したデータ競合を修正しました。
    -   JSON での not 演算子の実装が MySQL [#40683](https://github.com/pingcap/tidb/issues/40683) @ [ヤンケオ](https://github.com/YangKeao)での実装と互換性がないという問題を修正
    -   同時ビューにより DDL 操作がブロックされる可能性がある問題を修正[#40352](https://github.com/pingcap/tidb/issues/40352) @ [沢民州](https://github.com/zeminzhou)
    -   パーティション テーブル[#40620](https://github.com/pingcap/tidb/issues/40620) @ [むじょん](https://github.com/mjonss) @ [むじょん](https://github.com/mjonss)の列を変更する DDL ステートメントを同時に実行することによって発生するデータの不整合を修正しました。
    -   パスワードを指定せずに認証に`caching_sha2_password`使用すると、「不正なパケット」が報告される問題を修正[#40831](https://github.com/pingcap/tidb/issues/40831) @ [ドヴィーデン](https://github.com/dveeden)
    -   テーブルの主キーに`ENUM`カラム[#40456](https://github.com/pingcap/tidb/issues/40456) @ [ルクワンチャオ](https://github.com/lcwangchao)が含まれる場合、TTL タスクが失敗する問題を修正します。
    -   MDL によってブロックされた一部の DDL 操作が`mysql.tidb_mdl_view` [#40838](https://github.com/pingcap/tidb/issues/40838) @ [ヤンケオ](https://github.com/YangKeao)でクエリできない問題を修正します。
    -   DDL 取り込み[#40970](https://github.com/pingcap/tidb/issues/40970) @ [タンジェンタ](https://github.com/tangenta)中にデータ競合が発生する可能性がある問題を修正
    -   タイムゾーンが変更された後、TTL タスクが一部のデータを誤って削除する可能性がある問題を修正[#41043](https://github.com/pingcap/tidb/issues/41043) @ [ルクワンチャオ](https://github.com/lcwangchao)
    -   `JSON_OBJECT`が場合によってはエラーを報告する場合がある問題を修正[#39806](https://github.com/pingcap/tidb/issues/39806) @ [ヤンケオ](https://github.com/YangKeao)
    -   TiDB が初期化[#40408](https://github.com/pingcap/tidb/issues/40408) @ [定義2014](https://github.com/Defined2014)中にデッドロックする可能性がある問題を修正
    -   メモリの再利用によりシステム変数の値が誤って変更される場合がある問題を修正[#40979](https://github.com/pingcap/tidb/issues/40979) @ [ルクワンチャオ](https://github.com/lcwangchao)
    -   インジェストモード[#40464](https://github.com/pingcap/tidb/issues/40464) @ [タンジェンタ](https://github.com/tangenta)で一意のインデックスを作成すると、データがインデックスと不整合になる可能性がある問題を修正
    -   同じテーブルを同時に切り捨てる場合、一部の切り捨て操作が MDL によってブロックされない問題を修正します[#40484](https://github.com/pingcap/tidb/issues/40484) @ [wjhuang2016](https://github.com/wjhuang2016)
    -   `SHOW PRIVILEGES`ステートメントが不完全な権限リスト[#40591](https://github.com/pingcap/tidb/issues/40591) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)を返す問題を修正します。
    -   一意のインデックス[#40592](https://github.com/pingcap/tidb/issues/40592) @ [タンジェンタ](https://github.com/tangenta)を追加するときに TiDB がパニックになる問題を修正
    -   `ADMIN RECOVER`ステートメントを実行するとインデックス データが破損する可能性がある問題を修正します[#40430](https://github.com/pingcap/tidb/issues/40430) @ [ションジウェイ](https://github.com/xiongjiwei)
    -   クエリ対象のテーブルの式インデックス[#40130](https://github.com/pingcap/tidb/issues/40130) @ [ションジウェイ](https://github.com/xiongjiwei)に`CAST`式が含まれている場合、クエリが失敗する可能性がある問題を修正します。
    -   一意のインデックスによって場合によっては依然として重複データが生成される可能性がある問題を修正します[#40217](https://github.com/pingcap/tidb/issues/40217) @ [タンジェンタ](https://github.com/tangenta)
    -   多数のリージョンがあるにもかかわらず、 `Prepare`または`Execute` [#39605](https://github.com/pingcap/tidb/issues/39605) @ [djshow832](https://github.com/djshow832)を使用して一部の仮想テーブルをクエリするときにテーブル ID をプッシュダウンできない場合の PD OOM の問題を修正します。
    -   インデックス[#40879](https://github.com/pingcap/tidb/issues/40879) @ [タンジェンタ](https://github.com/tangenta)を追加するとデータ競合が発生する可能性がある問題を修正
    -   仮想列[#41014](https://github.com/pingcap/tidb/issues/41014) @ [アイリンキッド](https://github.com/AilinKid)によって引き起こされる`can't find proper physical plan`問題を修正
    -   動的トリミング モード[#40368](https://github.com/pingcap/tidb/issues/40368) @ [イーサール](https://github.com/Yisaer)でパーティション テーブルのグローバル バインディングが作成された後、TiDB が再起動できない問題を修正します。
    -   `auto analyze`により正常なシャットダウンに時間がかかる問題を修正[#40038](https://github.com/pingcap/tidb/issues/40038) @ [シュイファングリーンアイズ](https://github.com/xuyifangreeneyes)
    -   IndexMerge オペレーターがメモリ制限動作をトリガーしたときの TiDBサーバーのpanicを修正しました[#41036](https://github.com/pingcap/tidb/pull/41036) @ [グオシャオゲ](https://github.com/guo-shaoge)
    -   パーティションテーブルに対する`SELECT * FROM table_name LIMIT 1`クエリが遅い[#40741](https://github.com/pingcap/tidb/pull/40741) @ [ソロッツグ](https://github.com/solotzg)という問題を修正

-   TiKV

    -   `const Enum`型を他の型[#14156](https://github.com/tikv/tikv/issues/14156) @ [wshwsh12](https://github.com/wshwsh12)にキャストするときに発生するエラーを修正
    -   解決された TS によりネットワーク トラフィックが増加する問題を修正[#14092](https://github.com/tikv/tikv/issues/14092) @ [オーバーヴィーナス](https://github.com/overvenus)
    -   悲観的DML [#14038](https://github.com/tikv/tikv/issues/14038) @ [ミョンケミンタ](https://github.com/MyonKeminta)が失敗した後の DML の実行中に、TiDB と TiKV の間のネットワーク障害によって引き起こされるデータの不整合の問題を修正しました。

-   PD

    -   リージョン分散タスクが予期せず冗長レプリカを生成する問題を修正します[#5909](https://github.com/tikv/pd/issues/5909) @ [フンドゥンDM](https://github.com/HunDunDM)
    -   オンラインの安全でないリカバリ機能が`auto-detect`モード[#5753](https://github.com/tikv/pd/issues/5753) @ [コナー1996](https://github.com/Connor1996)でスタックしてタイムアウトになる問題を修正
    -   特定の条件下で実行`replace-down-peer`が遅くなる問題を修正[#5788](https://github.com/tikv/pd/issues/5788) @ [フンドゥンDM](https://github.com/HunDunDM)
    -   `ReportMinResolvedTS` [#5965](https://github.com/tikv/pd/issues/5965) @ [フンドゥンDM](https://github.com/HunDunDM)の呼び出しが頻繁すぎる場合に発生する PD OOM 問題を修正します。

-   TiFlash

    -   TiFlash関連のシステム テーブルのクエリがスタックする可能性がある問題を修正[#6745](https://github.com/pingcap/tiflash/pull/6745) @ [リデズ](https://github.com/lidezhu)
    -   デカルト積[#6730](https://github.com/pingcap/tiflash/issues/6730) @ [ゲンリキ](https://github.com/gengliqi)を計算するときにセミ結合が過剰なメモリを使用する問題を修正
    -   DECIMAL データ型の除算演算の結果が[#6393](https://github.com/pingcap/tiflash/issues/6393) @ [リトルフォール](https://github.com/LittleFall)に丸められない問題を修正します。
    -   TiFlashクエリで MPP クエリを`start_ts`に識別できないため、MPP クエリが誤ってキャンセルされる可能性がある問題を修正します[#43426](https://github.com/pingcap/tidb/issues/43426) @ [へへへん](https://github.com/hehechen)

-   ツール

    -   バックアップと復元 (BR)

        -   ログ バックアップを復元するときに、ホット リージョンにより復元が失敗する問題を修正します[#37207](https://github.com/pingcap/tidb/issues/37207) @ [レヴルス](https://github.com/Leavrth)
        -   ログ バックアップが実行されているクラスターにデータを復元すると、ログ バックアップ ファイルが回復不能になる問題を修正します[#40797](https://github.com/pingcap/tidb/issues/40797) @ [レヴルス](https://github.com/Leavrth)
        -   PITR 機能が CA バンドル[#38775](https://github.com/pingcap/tidb/issues/38775) @ [ユジュンセン](https://github.com/YuJuncen)をサポートしない問題を修正
        -   リカバリ[#40797](https://github.com/pingcap/tidb/issues/40797) @ [ジョッカウ](https://github.com/joccau)中に一時テーブルの重複によって引き起こされるpanicの問題を修正
        -   PITR が PD クラスター[#14165](https://github.com/tikv/tikv/issues/14165) @ [ユジュンセン](https://github.com/YuJuncen)の構成変更をサポートしていない問題を修正
        -   PD と tidb-server の間の接続障害により、PITR バックアップの進行状況が[#41082](https://github.com/pingcap/tidb/issues/41082) @ [ユジュンセン](https://github.com/YuJuncen)進まない問題を修正
        -   PD と TiKV [#14159](https://github.com/tikv/tikv/issues/14159) @ [ユジュンセン](https://github.com/YuJuncen)間の接続障害により、TiKV が PITR タスクをリッスンできない問題を修正
        -   TiDB クラスター[#40759](https://github.com/pingcap/tidb/issues/40759) @ [ジョッカウ](https://github.com/joccau)に PITR バックアップ タスクがない場合、 `resolve lock`の頻度が高すぎる問題を修正
        -   PITR バックアップ タスクが削除されると、残ったバックアップ データにより新しいタスク[#40403](https://github.com/pingcap/tidb/issues/40403) @ [ジョッカウ](https://github.com/joccau)でデータの不整合が発生する問題を修正します。

    -   TiCDC

        -   設定ファイル[#7935](https://github.com/pingcap/tiflow/issues/7935) @ [CharlesCheung96](https://github.com/CharlesCheung96)から`transaction_atomicity`と`protocol`を更新できない問題を修正
        -   REDOログ[#6335](https://github.com/pingcap/tiflow/issues/6335) @ [CharlesCheung96](https://github.com/CharlesCheung96)のstorageパスで事前チェ​​ックが行われない問題を修正
        -   S3storage障害[#8089](https://github.com/pingcap/tiflow/issues/8089) @ [CharlesCheung96](https://github.com/CharlesCheung96)に対して REDO ログが許容できる期間が不十分である問題を修正
        -   TiKV または TiCDC ノード[#8174](https://github.com/pingcap/tiflow/issues/8174) @ [ひっくり返る](https://github.com/hicqu)をスケールインまたはスケールアウトするときなど、特殊なシナリオで変更フィードが停止する可能性がある問題を修正します。
        -   TiKV ノード[#14092](https://github.com/tikv/tikv/issues/14092) @ [オーバーヴィーナス](https://github.com/overvenus)間のトラフィックが高すぎる問題を修正
        -   プルベースのシンクが有効になっている場合の、CPU 使用率、メモリ制御、およびスループットに関する[#8157](https://github.com/pingcap/tiflow/issues/8157) [#8142](https://github.com/pingcap/tiflow/issues/8142) [#8001](https://github.com/pingcap/tiflow/issues/8001) [#5928](https://github.com/pingcap/tiflow/issues/5928) [ひっくり返る](https://github.com/hicqu) @ [こんにちはラスティン](https://github.com/hi-rustin)

    -   TiDB データ移行 (DM)

        -   `binlog-schema delete`コマンドの実行に失敗する問題を修正[#7373](https://github.com/pingcap/tiflow/issues/7373) @ [リウメンギャ94](https://github.com/liumengya94)
        -   最後のbinlogがスキップされた DDL [#8175](https://github.com/pingcap/tiflow/issues/8175) @ [D3ハンター](https://github.com/D3Hunter)である場合、チェックポイントが進められない問題を修正します。
        -   1つのテーブルに「更新」タイプと「非更新」タイプの両方の式フィルタを指定した場合、 `UPDATE`ステートメントがすべてスキップされるバグを修正[#7831](https://github.com/pingcap/tiflow/issues/7831) @ [ランス6716](https://github.com/lance6716)
        -   テーブルに`update-old-value-expr`または`update-new-value-expr`のいずれか 1 つだけが設定されている場合、フィルター ルールが有効にならない、または DM パニック[#7774](https://github.com/pingcap/tiflow/issues/7774) @ [ランス6716](https://github.com/lance6716)が発生するバグを修正

    -   TiDB Lightning

        -   一部のシナリオ[#33714](https://github.com/pingcap/tidb/issues/33714) @ [リチュンジュ](https://github.com/lichunzhu)で TiDB の再起動が原因でTiDB Lightningタイムアウトがハングする問題を修正
        -   並列インポート[#40923](https://github.com/pingcap/tidb/issues/40923) @ [リチュンジュ](https://github.com/lichunzhu)中に、最後の TiDB Lightning インスタンスを除くすべてのTiDB Lightningインスタンスでローカルの重複レコードが検出された場合、 TiDB Lightning が誤って競合解決をスキップする可能性がある問題を修正します。
        -   事前チェックがターゲット クラスター[#41040](https://github.com/pingcap/tidb/issues/41040) @ [ランス6716](https://github.com/lance6716)で実行中の TiCDC の存在を正確に検出できない問題を修正します。
        -   TiDB Lightning が分割リージョン フェーズ[#40934](https://github.com/pingcap/tidb/issues/40934) @ [ランス6716](https://github.com/lance6716)でパニックになる問題を修正
        -   競合解決ロジック ( `duplicate-resolution` ) によってチェックサムの不一致が生じる可能性がある問題を修正します[#40657](https://github.com/pingcap/tidb/issues/40657) @ [ゴズスキー](https://github.com/gozssky)
        -   データ ファイル[#40400](https://github.com/pingcap/tidb/issues/40400) @ [ブチュイトデゴウ](https://github.com/buchuitoudegou)に閉じられていない区切り文字がある場合に発生する可能性がある OOM の問題を修正します。
        -   エラーレポートのファイルオフセットがファイルサイズ[#40034](https://github.com/pingcap/tidb/issues/40034) @ [ブチュイトデゴウ](https://github.com/buchuitoudegou)を超える問題を修正
        -   PDClient の新しいバージョンで、並列インポートが失敗する可能性がある問題を修正します[#40493](https://github.com/pingcap/tidb/issues/40493) @ [アメーバ原生動物](https://github.com/AmoebaProtozoa)
        -   TiDB Lightning事前チェックが、以前に失敗したインポート[#39477](https://github.com/pingcap/tidb/issues/39477) @ [dsダシュン](https://github.com/dsdashun)によって残されたダーティ データを見つけられない問題を修正

## 貢献者 {#contributors}

TiDB コミュニティの以下の貢献者に感謝いたします。

-   [モルゴ](https://github.com/morgo)
-   [ジフフスト](https://github.com/jiyfhust)
-   [b41sh](https://github.com/b41sh)
-   [ソーセリュー](https://github.com/sourcelliu)
-   [ソンジビン97](https://github.com/songzhibin97)
-   [マミル](https://github.com/mamil)
-   [ドゥーシール9](https://github.com/Dousir9)
-   [ヒヒヒヒヒ](https://github.com/hihihuhu)
-   [ミチョキシン](https://github.com/mychoxin)
-   [シュニン97](https://github.com/xuning97)
-   [アンドロイドデータベース](https://github.com/andreid-db)
