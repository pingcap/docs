---
title: TiDB 6.6.0 Release Notes
summary: TiDB 6.6.0 の新機能、互換性の変更、改善、バグ修正について説明します。
---

# TiDB 6.6.0 リリースノート {#tidb-6-6-0-release-notes}

発売日: 2023年2月20日

TiDB バージョン: 6.6.0- [DMMR の](/releases/versioning.md#development-milestone-releases)

> **注記：**
>
> TiDB 6.6.0-DMR のドキュメントは[アーカイブ済み](https://docs-archive.pingcap.com/tidb/v6.6/)になりました。PingCAP では、TiDB データベースの[最新のLTSバージョン](https://docs.pingcap.com/tidb/stable)使用することを推奨しています。

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.6/quick-start-with-tidb)

v6.6.0-DMR の主な新機能と改善点は次のとおりです。

<table><thead><tr><th>カテゴリ</th><th>特徴</th><th>説明</th></tr></thead><tbody><tr><td rowspan="3">スケーラビリティとパフォーマンス<br /></td><td>TiKV は<a href="https://docs.pingcap.com/tidb/v6.6/partitioned-raft-kv" target="_blank">Partitioned Raft KVstorageエンジン</a>をサポートします (実験的)</td><td> TiKV ではパーティション化されたRaft KVstorageエンジンが導入され、各リージョンで独立した RocksDB インスタンスが使用されるため、クラスターのstorage容量を TB から PB に簡単に拡張でき、より安定した書き込みレイテンシーと強力なスケーラビリティを実現できます。</td></tr><tr><td> TiKVは<a href="https://docs.pingcap.com/tidb/v6.6/system-variables#tidb_store_batch_size" target="_blank">データ要求のバッチ集約</a>をサポートします</td><td>この機能強化により、TiKV バッチ取得操作での合計 RPC が大幅に削減されます。データが高度に分散され、gRPC スレッド プールのリソースが不足している状況では、コプロセッサ要求をバッチ処理すると、パフォーマンスが 50% 以上向上する可能性があります。</td></tr><tr><td> TiFlashは<a href="https://docs.pingcap.com/tidb/v6.6/stale-read" target="_blank">ステイル読み取り</a>と<a href="https://docs.pingcap.com/tidb/v6.6/explain-mpp#mpp-version-and-exchange-data-compression" target="_blank">圧縮交換</a>をサポート</td><td>TiFlash は古い読み取り機能をサポートしており、リアルタイム要件が制限されないシナリオでクエリ パフォーマンスを向上させることができます。TiFlashはデータ圧縮をサポートしており、並列データ交換の効率を向上させ、全体的な TPC-H パフォーマンスが 10% 向上し、ネットワーク使用量を 50% 以上節約できます。</td></tr><tr><td rowspan="2">信頼性と可用性<br /></td><td><a href="https://docs.pingcap.com/tidb/v6.6/tidb-resource-control" target="_blank">リソース制御</a>（実験的）</td><td>リソース グループに基づくリソース管理をサポートします。これにより、データベース ユーザーを対応するリソース グループにマッピングし、実際のニーズに基づいて各リソース グループの割り当てを設定します。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v6.6/sql-plan-management#create-a-binding-according-to-a-historical-execution-plan" target="_blank">歴史的なSQLバインディング</a></td><td>履歴実行プランのバインドと、TiDB ダッシュボードでの実行プランの迅速なバインドをサポートします。</td></tr><tr><td rowspan="2"> SQL機能<br /></td><td><a href="https://docs.pingcap.com/tidb/v6.6/foreign-key" target="_blank">外部キー</a>（実験的）</td><td>データの一貫性を維持し、データ品質を向上させるために、MySQL 互換の外部キー制約をサポートします。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v6.6/sql-statement-create-index#multi-valued-indexes" target="_blank">多値インデックス</a>（実験的）</td><td> MySQL 互換のマルチ値インデックスを導入し、JSON タイプを拡張して、TiDB と MySQL 8.0 の互換性を向上させます。</td></tr><tr><td> DB操作と可観測性<br /></td><td><a href="https://docs.pingcap.com/tidb/v6.6/dm-precheck#check-items-for-physical-import" target="_blank">DM は物理インポートをサポートします</a>(実験的)</td><td> TiDB データ移行 (DM) は、TiDB Lightning の物理インポート モードを統合し、完全なデータ移行のパフォーマンスを最大 10 倍向上させます。</td></tr></tbody></table>

## 機能の詳細 {#feature-details}

### スケーラビリティ {#scalability}

-   パーティション化されたRaft KVstorageエンジンをサポート (実験的) [＃11515](https://github.com/tikv/tikv/issues/11515) [＃12842](https://github.com/tikv/tikv/issues/12842) @ [忙しいカケス](https://github.com/busyjay) @ [トニー](https://github.com/tonyxuqqi) @ [タボキ](https://github.com/tabokie) @ [バッファフライ](https://github.com/bufferflies) @ [5kbpsの](https://github.com/5kbpers) @ [スペードA-タン](https://github.com/SpadeA-Tang) @ [ノルーシュ](https://github.com/nolouch)

    TiDB v6.6.0 より前では、TiKV の Raft ベースのstorageエンジンは、単一の RocksDB インスタンスを使用して、TiKV インスタンスのすべての「リージョン」のデータを格納していました。より安定した大規模なクラスターをサポートするために、TiDB v6.6.0 以降では、新しい TiKVstorageエンジンが導入されました。このエンジンは、複数の RocksDB インスタンスを使用して TiKVリージョンデータを格納し、各リージョンのデータは独立した RocksDB インスタンスに格納されます。新しいエンジンは、RocksDB インスタンス内のファイルの数とレベルをより適切に制御し、リージョン間のデータ操作の物理的な分離を実現し、より多くのデータを安定して管理できるようにします。これは、TiKV がパーティション分割によって複数の RocksDB インスタンスを管理しているのと同じであるため、この機能は Partitioned-Raft-KV と名付けられています。この機能の主な利点は、書き込みパフォーマンスが向上し、スケーリングが高速になり、同じハードウェアでサポートされるデータ量が増えることです。また、より大きなクラスター スケールをサポートすることもできます。

    現在、この機能は実験的であり、本番環境での使用は推奨されません。

    詳細については[ドキュメント](/partitioned-raft-kv.md)参照してください。

-   DDL 操作の分散並列実行フレームワークをサポート (実験的) [＃37125](https://github.com/pingcap/tidb/issues/37125) @ [ジムララ](https://github.com/zimulala)

    以前のバージョンでは、TiDB クラスター全体で 1 つの TiDB インスタンスのみが DDL 所有者としてスキーマ変更タスクを処理できました。大規模テーブルの DDL 操作の DDL 同時実行性をさらに向上させるために、TiDB v6.6.0 では DDL の分散並列実行フレームワークが導入され、クラスター内のすべての TiDB インスタンスが同じタスクの`StateWriteReorganization`フェーズを同時に実行して DDL 実行を高速化できるようになりました。この機能はシステム変数[`tidb_ddl_distribute_reorg`](https://docs.pingcap.com/tidb/v6.6/system-variables#tidb_ddl_distribute_reorg-new-in-v660)によって制御され、現在は`Add Index`操作に対してのみサポートされています。

### パフォーマンス {#performance}

-   悲観的ロックキュー[＃13298](https://github.com/tikv/tikv/issues/13298) @ [ミョンケミンタ](https://github.com/MyonKeminta)の安定したウェイクアップ モデルをサポート

    アプリケーションがシングルポイントの悲観的ロック競合に頻繁に遭遇すると、既存のウェイクアップ メカニズムではトランザクションがロックを取得する時間を保証できず、ロングテールレイテンシーが大きくなり、ロック取得タイムアウトが発生することもあります。v6.6.0 以降では、システム変数の値を[`tidb_pessimistic_txn_aggressive_locking`](https://docs.pingcap.com/tidb/v6.6/system-variables#tidb_pessimistic_txn_aggressive_locking-new-in-v660)から`ON`に設定することで、悲観的ロックの安定したウェイクアップ モデルを有効にすることができます。このウェイクアップ モデルでは、キューのウェイクアップ シーケンスを厳密に制御して、無効なウェイクアップによるリソースの浪費を回避できます。深刻なロック競合が発生するシナリオでは、安定したウェイクアップ モデルによってロングテールレイテンシーと P99 応答時間を削減できます。

    テストでは、これによりテールレイテンシーが 40 ～ 60% 削減されることが示されています。

    詳細については[ドキュメント](https://docs.pingcap.com/tidb/v6.6/system-variables#tidb_pessimistic_txn_aggressive_locking-new-in-v660)参照してください。

-   バッチ集計データ要求[＃39361](https://github.com/pingcap/tidb/issues/39361) @ [翻訳](https://github.com/cfzjywxk) @ [あなた06](https://github.com/you06)

    TiDB が TiKV にデータ要求を送信すると、TiDB はデータが配置されているリージョンに応じて要求を異なるサブタスクにコンパイルし、各サブタスクは単一のリージョンの要求のみを処理します。アクセスするデータが大きく分散している場合、データのサイズが大きくなくても、多くのサブタスクが生成され、その結果、多くの RPC 要求が生成され、余分な時間が消費されます。v6.6.0 以降、TiDB は同じ TiKV インスタンスに送信されるデータ要求を部分的にマージすることがサポートされ、サブタスクの数と RPC 要求のオーバーヘッドが削減されます。データの分散が高く、gRPC スレッド プールのリソースが不十分な場合は、要求をバッチ処理することでパフォーマンスを 50% 以上向上できます。

    この機能はデフォルトで有効になっています。システム変数[`tidb_store_batch_size`](/system-variables.md#tidb_store_batch_size)を使用して、リクエストのバッチ サイズを設定できます。

-   `LIMIT`節[#40219](https://github.com/pingcap/tidb/issues/40219) @ [ふーふー](https://github.com/fzzf678)の制限を解除します

    v6.6.0 以降、TiDB プラン キャッシュは、 `LIMIT ?`や`LIMIT 10, ?`などの変数を`LIMIT`パラメータとして持つ実行プランのキャッシュをサポートします。この機能により、より多くの SQL ステートメントがプラン キャッシュの恩恵を受けられるようになり、実行効率が向上します。現在、セキュリティ上の理由から、TiDB は`?`が 10000 以下である実行プランのみをキャッシュできます。

    詳細については[ドキュメント](/sql-prepared-plan-cache.md)参照してください。

-   TiFlashは圧縮[＃6620](https://github.com/pingcap/tiflash/issues/6620) @ [ソロッツ](https://github.com/solotzg)によるデータ交換をサポート

    複数のノードと連携して計算を行うために、 TiFlashエンジンは異なるノード間でデータを交換する必要があります。交換するデータのサイズが非常に大きい場合、データ交換のパフォーマンスが全体的な計算効率に影響を与える可能性があります。v6.6.0 では、 TiFlashエンジンに圧縮メカニズムが導入され、必要に応じて交換する必要があるデータを圧縮してから交換を実行するため、データ交換の効率が向上します。

    詳細については[ドキュメント](/explain-mpp.md#mpp-version-and-exchange-data-compression)参照してください。

-   TiFlashはステイル読み取り機能[＃4483](https://github.com/pingcap/tiflash/issues/4483) @ [ヘヘチェン](https://github.com/hehechen)をサポートしています

    ステイル読み取り機能は、v5.1.1 以降で一般提供 (GA) されており、特定のタイムスタンプまたは指定された時間範囲内の履歴データを読み取ることができます。Stale Read を使用すると、ローカル TiKV レプリカから直接データを読み取ることで、読み取りレイテンシーを短縮し、クエリ パフォーマンスを向上させることができます。v6.6.0 より前では、 TiFlash はステイル読み取りをサポートしていません。テーブルにTiFlashレプリカがある場合でも、 ステイル読み取りその TiKV レプリカしか読み取れません。

    v6.6.0 以降、 TiFlash はステイル読み取り機能をサポートします。1 構文または[`AS OF TIMESTAMP`](/as-of-timestamp.md)システム変数を使用してテーブルの履歴[`tidb_read_staleness`](/tidb-read-staleness.md)をクエリする場合、テーブルにTiFlashレプリカがあれば、オプティマイザーはTiFlashレプリカから対応するデータを読み取ることを選択できるようになり、クエリ パフォーマンスがさらに向上します。

    詳細については[ドキュメント](/stale-read.md)参照してください。

-   `regexp_replace`ストリング機能をTiFlash [＃6115](https://github.com/pingcap/tiflash/issues/6115) @ [翻訳者](https://github.com/xzhangxian1008)にプッシュダウンする機能をサポート

### 信頼性 {#reliability}

-   リソース グループに基づくリソース制御をサポート (実験的) [＃38825](https://github.com/pingcap/tidb/issues/38825) @ [ノルーシュ](https://github.com/nolouch) @ [ボーンチェンジャー](https://github.com/BornChanger) @ [栄光](https://github.com/glorv) @ [天菜まお](https://github.com/tiancaiamao) @ [コナー1996](https://github.com/Connor1996) @ [じゃがいも](https://github.com/JmPotato) @ [ネス](https://github.com/hnes) @ [キャビンフィーバーB](https://github.com/CabinfeverB) @ [ヒューシャープ](https://github.com/HuSharp)

    TiDB クラスターのリソース グループを作成し、異なるデータベース ユーザーを対応するリソース グループにバインドし、実際のニーズに応じて各リソース グループのクォータを設定できるようになりました。クラスター リソースが制限されている場合、同じリソース グループ内のセッションで使用されるすべてのリソースはクォータに制限されます。このように、リソース グループが過剰に消費されても、他のリソース グループのセッションは影響を受けません。TiDB は、Grafana ダッシュボードでリソースの実際の使用状況の組み込みビューを提供し、リソースをより合理的に割り当てるのに役立ちます。

    リソース制御機能の導入は、TiDB にとって画期的な出来事です。この機能により、分散データベース クラスターを複数の論理ユニットに分割できます。個々のユニットがリソースを過剰に使用しても、他のユニットに必要なリソースが圧迫されることはありません。

    この機能を使用すると、次のことが可能になります。

    -   異なるシステムの複数の中小規模のアプリケーションを 1 つの TiDB クラスターに統合します。アプリケーションのワークロードが大きくなっても、他のアプリケーションの正常な動作には影響しません。システムのワークロードが低い場合は、設定された読み取りおよび書き込みクォータを超えても、ビジー状態のアプリケーションに必要なシステム リソースを割り当てることができるため、リソースを最大限に活用できます。
    -   すべてのテスト環境を単一の TiDB クラスターに結合するか、より多くのリソースを消費するバッチ タスクを単一のリソース グループにグループ化するかを選択します。これにより、重要なアプリケーションが常に必要なリソースを取得できるようにしながら、ハードウェアの使用率を向上させ、運用コストを削減できます。

    さらに、リソース制御機能を合理的に使用すると、クラスターの数を減らし、運用と保守の難易度を軽減し、管理コストを節約できます。

    v6.6 では、リソース制御を有効にするには、TiDB のグローバル変数[`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-new-in-v660)と TiKV 構成項目[`resource-control.enabled`](/tikv-configuration-file.md#resource-control)両方を有効にする必要があります。現在サポートされているクォータ方式は、「 [リクエストユニット (RU)](/tidb-resource-control.md#what-is-request-unit-ru) 」に基づいています。RU は、CPU や IO などのシステム リソースに対する TiDB の統一された抽象化単位です。

    詳細については[ドキュメント](/tidb-resource-control.md)参照してください。

-   過去の実行計画のバインドは GA [＃39199](https://github.com/pingcap/tidb/issues/39199) @ [ふーふー](https://github.com/fzzf678)です

    v6.5.0 では、TiDB は[`CREATE [GLOBAL | SESSION] BINDING`](/sql-statements/sql-statement-create-binding.md)ステートメントのバインディング ターゲットを拡張し、履歴実行プランに従ってバインディングを作成することをサポートします。v6.6.0 では、この機能が GA です。実行プランの選択は、現在の TiDB ノードに限定されません。任意の TiDB ノードによって生成された任意の履歴実行プランを[SQLバインディング](/sql-statements/sql-statement-create-binding.md)のターゲットとして選択できるため、機能の使いやすさがさらに向上します。

    詳細については[ドキュメント](/sql-plan-management.md#create-a-binding-according-to-a-historical-execution-plan)参照してください。

-   いくつかのオプティマイザヒント[＃39964](https://github.com/pingcap/tidb/issues/39964) @ [思い出させる](https://github.com/Reminiscent)を追加します

    TiDB は、 `LIMIT`操作の実行プランの選択を制御するために、v6.6.0 でいくつかのオプティマイザー ヒントを追加します。

    -   [`ORDER_INDEX()`](/optimizer-hints.md#order_indext1_name-idx1_name--idx2_name-) : オプティマイザに指定されたインデックスを使用し、データを読み取るときにインデックスの順序を維持するように指示し、 `Limit + IndexScan(keep order: true)`と同様のプランを生成します。
    -   [`NO_ORDER_INDEX()`](/optimizer-hints.md#no_order_indext1_name-idx1_name--idx2_name-) : データの読み取り時にインデックスの順序を保持せず、指定されたインデックスを使用するようにオプティマイザに指示し、 `TopN + IndexScan(keep order: false)`と同様のプランを生成します。

    オプティマイザーヒントを継続的に導入することで、ユーザーにさらに多くの介入方法が提供され、SQL パフォーマンスの問題を解決し、全体的なパフォーマンスの安定性が向上します。

-   DDL 操作のリソース使用量を動的に管理するサポート (実験的) [＃38025](https://github.com/pingcap/tidb/issues/38025) @ [ホーキングレイ](https://github.com/hawkingrei)

    TiDB v6.6.0 では、DDL 操作のリソース管理が導入され、これらの操作の CPU 使用率を自動的に制御することで、オンライン アプリケーションに対する DDL 変更の影響を軽減します。この機能は、 [DDL分散並列実行フレームワーク](https://docs.pingcap.com/tidb/v6.6/system-variables#tidb_ddl_distribute_reorg-new-in-v660)有効になった後にのみ有効になります。

### 可用性 {#availability}

-   `SURVIVAL_PREFERENCE` for [SQL の配置ルール](/placement-rules-in-sql.md) [＃38605](https://github.com/pingcap/tidb/issues/38605) @ [ノルーシュ](https://github.com/nolouch)の構成をサポート

    `SURVIVAL_PREFERENCES`データの災害時の生存性を高めるためのデータ生存設定を提供します。 `SURVIVAL_PREFERENCE`を指定すると、以下を制御できます。

    -   クラウド リージョン全体に展開された TiDB クラスターの場合、クラウド リージョンで障害が発生しても、指定されたデータベースまたはテーブルは別のクラウド リージョンで存続できます。
    -   単一のクラウド リージョンにデプロイされた TiDB クラスターの場合、可用性ゾーンに障害が発生しても、指定されたデータベースまたはテーブルは別の可用性ゾーンで存続できます。

    詳細については[ドキュメント](/placement-rules-in-sql.md#specify-survival-preferences)参照してください。

-   `FLASHBACK CLUSTER TO TIMESTAMP`ステートメント[＃14045](https://github.com/tikv/tikv/issues/14045) @ [定義2014](https://github.com/Defined2014) @ [じゃがいも](https://github.com/JmPotato)による DDL 操作のロールバックをサポート

    [`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-cluster.md)ステートメントは、ガベージ コレクション (GC) の有効期間内の特定の時点にクラスター全体を復元することをサポートします。TiDB v6.6.0 では、この機能により DDL 操作のロールバックのサポートが追加されました。これを使用すると、クラスター上の DML または DDL の誤った操作をすばやく元に戻したり、数分以内にクラスターをロールバックしたり、タイムライン上でクラスターを複数回ロールバックして、特定のデータ変更がいつ発生したかを確認したりできます。

    詳細については[ドキュメント](/sql-statements/sql-statement-flashback-cluster.md)参照してください。

### 構文 {#sql}

-   MySQL 互換の外部キー制約をサポート (実験的) [＃18209](https://github.com/pingcap/tidb/issues/18209) @ [クレイジーcs520](https://github.com/crazycs520)

    TiDB v6.6.0 では、MySQL と互換性のある外部キー制約機能が導入されています。この機能は、テーブル内またはテーブル間の参照、制約の検証、およびカスケード操作をサポートします。この機能は、アプリケーションを TiDB に移行し、データの一貫性を維持し、データ品質を向上させ、データ モデリングを容易にするのに役立ちます。

    詳細については[ドキュメント](/foreign-key.md)参照してください。

-   MySQL互換のマルチ値インデックスをサポート（実験的） [＃39592](https://github.com/pingcap/tidb/issues/39592) @ [雄吉偉](https://github.com/xiongjiwei) @ [qw4990](https://github.com/qw4990)

    TiDB は、v6.6.0 で MySQL 互換の多値インデックスを導入しました。JSON 列の配列の値をフィルタリングすることは一般的な操作ですが、通常のインデックスではこのような操作を高速化することはできません。配列に多値インデックスを作成すると、フィルタリングのパフォーマンスが大幅に向上します。JSON 列の配列に多値インデックスがある場合は、多値インデックスを使用して`MEMBER OF()` 、 `JSON_CONTAINS()` 、 `JSON_OVERLAPS()`関数で検索条件をフィルタリングできるため、I/O 消費が大幅に削減され、操作速度が向上します。

    複数値インデックスの導入により、TiDB の JSON データ型のサポートがさらに強化され、TiDB と MySQL 8.0 の互換性も向上します。

    詳細については[ドキュメント](/sql-statements/sql-statement-create-index.md#multi-valued-indexes)参照してください。

### DB操作 {#db-operations}

-   リソースを消費するタスク用の読み取り専用storageノードの構成をサポート @ [v01dスター](https://github.com/v01dstar)

    本番環境では、バックアップや大規模なデータの読み取りと分析など、一部の読み取り専用操作が定期的に大量のリソースを消費し、クラスター全体のパフォーマンスに影響を与える可能性があります。TiDB v6.6.0 では、リソースを消費する読み取り専用タスク用に読み取り専用storageノードを構成して、オンライン アプリケーションへの影響を軽減することがサポートされています。現在、TiDB、TiSpark、およびBR は、読み取り専用storageノードからのデータの読み取りをサポートしています[手順](/best-practices/readonly-nodes.md#procedures)に従って読み取り専用storageノードを構成し、システム変数`tidb_replica_read` 、TiSpark 構成項目`spark.tispark.replica_read` 、または br コマンドライン引数`--replica-read-label`を通じてデータの読み取り場所を指定して、クラスターのパフォーマンスの安定性を確保できます。

    詳細については[ドキュメント](/best-practices/readonly-nodes.md)参照してください。

-   `store-io-pool-size` [＃13964](https://github.com/tikv/tikv/issues/13964) @ [リクササシネーター](https://github.com/LykxSassinator)動的変更をサポート

    TiKV 構成項目[`raftstore.store-io-pool-size`](/tikv-configuration-file.md#store-io-pool-size-new-in-v530) 、 Raft I/O タスクを処理するスレッドの許容数を指定します。これは、TiKV パフォーマンスのチューニング時に調整できます。v6.6.0 より前では、この構成項目を動的に変更することはできませんでした。v6.6.0 以降では、サーバーを再起動せずにこの構成を変更できるため、より柔軟なパフォーマンス チューニングが可能になります。

    詳細については[ドキュメント](/dynamic-config.md)参照してください。

-   TiDB クラスタの初期化時に実行される SQL スクリプトの指定をサポート[＃35624](https://github.com/pingcap/tidb/issues/35624) @ [モルゴ](https://github.com/morgo)

    TiDB クラスターを初めて起動するときに、コマンドラインパラメータ`--initialize-sql-file`を設定することで、実行する SQL スクリプトを指定できます。この機能は、システム変数の値の変更、ユーザーの作成、権限の付与などの操作を実行する必要がある場合に使用できます。

    詳細については[ドキュメント](/tidb-configuration-file.md#initialize-sql-file-new-in-v660)参照してください。

-   TiDBデータ移行（DM）は、TiDB Lightningの物理インポートモードと統合され、完全な移行で最大10倍のパフォーマンス向上を実現します（実験的）@ [ランス6716](https://github.com/lance6716)

    v6.6.0 では、DM の完全移行機能がTiDB Lightningの物理インポート モードと統合され、DM は完全データ移行のパフォーマンスを最大 10 倍向上させ、大容量データ シナリオでの移行時間を大幅に短縮できるようになりました。

    v6.6.0 より前では、大容量データ シナリオの場合、高速な完全データ移行のためにTiDB Lightningで物理インポート タスクを個別に構成し、その後 DM を使用して増分データ移行を行う必要があり、これは複雑な構成でした。v6.6.0 以降では、 TiDB Lightningタスクを構成する必要なく大容量データを移行できます。1 つの DM タスクで移行を完了できます。

    詳細については[ドキュメント](/dm/dm-precheck.md#check-items-for-physical-import)参照してください。

-   TiDB Lightningは、ソースファイルとターゲットテーブル間の列名の不一致の問題に対処するために、新しい構成パラメータ`"header-schema-match"`を追加します@ [ダシュン](https://github.com/dsdashun)

    v6.6.0 では、 TiDB Lightning に新しいプロファイル パラメータ`"header-schema-match"`が追加されました。デフォルト値は`true`で、ソース CSV ファイルの最初の行が列名として扱われ、ターゲット テーブル内の列名と一致していることを意味します。CSV テーブル ヘッダーのフィールド名がターゲット テーブルの列名と一致しない場合は、この構成を`false`に設定できます。TiDB TiDB Lightning はエラーを無視し、ターゲット テーブルの列の順序でデータをインポートし続けます。

    詳細については[ドキュメント](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)参照してください。

-   TiDB Lightningは、 TiKV [＃41163](https://github.com/pingcap/tidb/issues/41163) @ [眠いモグラ](https://github.com/sleepymole)にキーと値のペアを送信するときに圧縮転送を有効にすることをサポートします。

    v6.6.0 以降、 TiDB Lightning は、ローカルでエンコードされ、ソートされたキーと値のペアを TiKV に送信する際にネットワーク転送用に圧縮することをサポートしています。これにより、ネットワーク経由で転送されるデータの量が削減され、ネットワーク帯域幅のオーバーヘッドが低減されます。この機能がサポートされる前の TiDB バージョンでは、 TiDB Lightning は比較的高いネットワーク帯域幅を必要とし、大量のデータを扱う場合には高いトラフィック料金が発生します。

    この機能はデフォルトでは無効になっています。有効にするには、 TiDB Lightningの`compress-kv-pairs`構成項目を`"gzip"`または`"gz"`に設定します。

    詳細については[ドキュメント](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)参照してください。

-   TiKV-CDC ツールが GA になり、RawKV [＃48](https://github.com/tikv/migration/issues/48) @ [沢民州](https://github.com/zeminzhou) @ [ハオジンミン](https://github.com/haojinming) @ [ピンギュ](https://github.com/pingyu)のデータ変更のサブスクライブがサポートされるようになりました。

    TiKV-CDC は、TiKV クラスター用の CDC (Change Data Capture) ツールです。TiKV と PD は、TiDB なしで使用すると KV データベースを構成でき、RawKV と呼ばれます。TiKV-CDC は、RawKV のデータ変更をサブスクライブし、それを下流の TiKV クラスターにリアルタイムで複製することをサポートしているため、RawKV のクラスター間レプリケーションが可能になります。

    詳細については[ドキュメント](https://tikv.org/docs/latest/concepts/explore-tikv-features/cdc/cdc/)参照してください。

-   TiCDC は、Kafka の変更フィード上の単一のテーブルのスケールアウトと、変更フィードを複数の TiCDC ノードに分散することをサポートします (実験的) [＃7720](https://github.com/pingcap/tiflow/issues/7720) @ [金星の上](https://github.com/overvenus)

    v6.6.0 より前では、アップストリームのテーブルが大量の書き込みを受け入れる場合、このテーブルのレプリケーション機能をスケールアウトできず、レプリケーションのレイテンシーが増加していました。TiCDC v6.6.0 以降では、アップストリーム テーブルの変更フィードを Kafka シンク内の複数の TiCDC ノードに分散できるようになり、単一のテーブルのレプリケーション機能がスケールアウトされます。

    詳細については[ドキュメント](/ticdc/ticdc-sink-to-kafka.md#scale-out-the-load-of-a-single-large-table-to-multiple-ticdc-nodes)参照してください。

-   [ゴーム](https://github.com/go-gorm/gorm)では TiDB 統合テストが追加されました。これで TiDB が GORM でサポートされるデフォルトのデータベースになりました[＃6014](https://github.com/go-gorm/gorm/pull/6014) @ [アイスマップ](https://github.com/Icemap)

    -   v1.4.6では、 [GORM MySQL ドライバー](https://github.com/go-gorm/mysql) TiDB [＃104](https://github.com/go-gorm/mysql/pull/104)の`AUTO_RANDOM`属性に適応します。
    -   v1.4.6では、1TiDBに接続するときに、 [GORM MySQL ドライバー](https://github.com/go-gorm/mysql)フィールドの`Unique`属性が`AutoMigrate` [＃105](https://github.com/go-gorm/mysql/pull/105)中に変更できない問題を`Unique`しました。
    -   [GORMドキュメント](https://github.com/go-gorm/gorm.io)デフォルトのデータベースとして TiDB を挙げています[＃638](https://github.com/go-gorm/gorm.io/pull/638)

    詳細については[GORMドキュメント](https://gorm.io/docs/index.html)参照してください。

### 可観測性 {#observability}

-   TiDBダッシュボード[＃781](https://github.com/pingcap/tidb-dashboard/issues/781) @ [宜尼Xu9506](https://github.com/YiniXu9506)でSQLバインディングを素早く作成するサポート

    TiDB v6.6.0 では、ステートメント履歴からの SQL バインディングの作成がサポートされており、TiDB ダッシュボード上の特定のプランに SQL ステートメントをすばやくバインドできます。

    この機能は、ユーザーフレンドリーなインターフェースを提供することで、TiDB でのプランのバインド プロセスを簡素化し、操作の複雑さを軽減し、プランのバインド プロセスの効率とユーザー エクスペリエンスを向上させます。

    詳細については[ドキュメント](/dashboard/dashboard-statement-details.md#fast-plan-binding)参照してください。

-   実行プランのキャッシュに関する警告を追加 @ [qw4990](https://github.com/qw4990)

    実行プランをキャッシュできない場合、TiDB は診断を容易にするために警告で理由を示します。例:

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

    前の例では、オプティマイザが INT 以外の型を INT 型に変換し、パラメータの変更によって実行プランが変わる可能性があるため、TiDB はプランをキャッシュしません。

    詳細については[ドキュメント](/sql-prepared-plan-cache.md#diagnostics-of-prepared-plan-cache)参照してください。

-   スロークエリログ[＃39893](https://github.com/pingcap/tidb/issues/39893) @ [時間と運命](https://github.com/time-and-fate)に`Warnings`フィールドを追加します

    TiDB v6.6.0 では、パフォーマンスの問題の診断に役立つように、スロー クエリ ログに`Warnings`フィールドが追加されました。このフィールドには、スロー クエリの実行中に生成された警告が記録されます。TiDB ダッシュボードのスロー クエリ ページでも警告を表示できます。

    詳細については[ドキュメント](/identify-slow-queries.md)参照してください。

-   SQL実行プランの生成を自動的にキャプチャする[＃38779](https://github.com/pingcap/tidb/issues/38779) @ [イサール](https://github.com/Yisaer)

    実行計画の問題をトラブルシューティングするプロセスでは、 `PLAN REPLAYER`シーンを保存し、診断の効率を向上させるのに役立ちます。ただし、一部のシナリオでは、一部の実行計画の生成を自由に再現できないため、診断作業が困難になります。

    このような問題に対処するため、TiDB v6.6.0 では、 `PLAN REPLAYER`自動キャプチャの機能が拡張されました。3 `PLAN REPLAYER CAPTURE`を使用すると、対象の SQL 文を事前に登録し、同時に対象の実行プランも指定できます。TiDB は、登録された対象に一致する SQL 文または実行プランを検出すると、 `PLAN REPLAYER`情報を自動的に生成してパッケージ化します。実行プランが不安定な場合、この機能により診断効率が向上します。

    この機能を使用するには、 [`tidb_enable_plan_replayer_capture`](/system-variables.md#tidb_enable_plan_replayer_capture)の値を`ON`に設定します。

    詳細については[ドキュメント](/sql-plan-replayer.md#use-plan-replayer-capture)参照してください。

-   永続的なステートメントのサポートの概要 (実験的) [＃40812](https://github.com/pingcap/tidb/issues/40812) @ [モーニクス](https://github.com/mornyx)

    v6.6.0 より前では、ステートメント サマリー データはメモリ内に保持され、TiDBサーバーの再起動時に失われていました。v6.6.0 以降、TiDB はステートメント サマリーの永続化の有効化をサポートし、履歴データを定期的にディスクに書き込むことができます。その間、システム テーブルに対するクエリの結果は、メモリではなくディスクから取得されます。TiDB の再起動後も、すべての履歴データは引き続き利用できます。

    詳細については[ドキュメント](/statement-summary-tables.md#persist-statements-summary)参照してください。

### Security {#security}

-   TiFlashはTLS証明書[＃5503](https://github.com/pingcap/tiflash/issues/5503) @ [うわー](https://github.com/ywqzzy)の自動ローテーションをサポートします

    v6.6.0 では、TiDB はTiFlash TLS 証明書の自動ローテーションをサポートしています。コンポーネント間の暗号化データ転送が有効になっている TiDB クラスターの場合、 TiFlashの TLS 証明書の有効期限が切れて新しい証明書を再発行する必要がある場合、TiDB クラスターを再起動せずに新しいTiFlash TLS 証明書を自動的にロードできます。さらに、TiDB クラスター内のコンポーネント間の TLS 証明書のローテーションは TiDB クラスターの使用に影響を与えないため、クラスターの高可用性が保証されます。

    詳細については[ドキュメント](/enable-tls-between-components.md)参照してください。

-   TiDB Lightning は、AWS IAMロールキーとセッショントークン[＃40750](https://github.com/pingcap/tidb/issues/40750) @ [ok江](https://github.com/okJiang)を介して Amazon S3 データへのアクセスをサポートします。

    v6.6.0 より前のバージョンでは、 TiDB Lightning はAWS IAM**ユーザーのアクセスキー**(各アクセスキーはアクセスキー ID とシークレットアクセスキーで構成) 経由での S3 データへのアクセスのみをサポートしていたため、一時セッショントークンを使用して S3 データにアクセスすることはできません。v6.6.0 以降では、 TiDB Lightning はデータセキュリティを向上させるために、AWS IAM**ロールのアクセスキー + セッショントークン**経由での S3 データへのアクセスもサポートしています。

    詳細については[ドキュメント](/tidb-lightning/tidb-lightning-data-source.md#import-data-from-amazon-s3)参照してください。

### テレメトリー {#telemetry}

-   2023 年 2 月 20 日以降、TiDB および TiDB Dashboard の新しいバージョン (v6.6.0 を含む) では、 [テレメトリ機能](/telemetry.md)がデフォルトで無効になります。デフォルトのテレメトリ構成を使用する以前のバージョンからアップグレードすると、アップグレード後にテレメトリ機能が無効になります。具体的なバージョンについては、 [TiDB リリース タイムライン](/releases/release-timeline.md)参照してください。
-   v1.11.3 以降では、新しくデプロイされたTiUPではテレメトリ機能がデフォルトで無効になっています。以前のバージョンのTiUPから v1.11.3 以降のバージョンにアップグレードすると、テレメトリ機能はアップグレード前と同じ状態を維持します。

## 互換性の変更 {#compatibility-changes}

> **注記：**
>
> このセクションでは、v6.5.0 から現在のバージョン (v6.6.0) にアップグレードするときに知っておく必要のある互換性の変更について説明します。v6.4.0 以前のバージョンから現在のバージョンにアップグレードする場合は、中間バージョンで導入された互換性の変更も確認する必要がある可能性があります。

### MySQL 互換性 {#mysql-compatibility}

-   MySQL 互換の外部キー制約をサポート (実験的) [＃18209](https://github.com/pingcap/tidb/issues/18209) @ [クレイジーcs520](https://github.com/crazycs520)

    詳細については、このドキュメントの[構文](#sql)セクションと[ドキュメント](/foreign-key.md)参照してください。

-   MySQL互換のマルチ値インデックスをサポート（実験的） [＃39592](https://github.com/pingcap/tidb/issues/39592) @ [雄吉偉](https://github.com/xiongjiwei) @ [qw4990](https://github.com/qw4990)

    詳細については、このドキュメントの[構文](#sql)セクションと[ドキュメント](/sql-statements/sql-statement-create-index.md#multi-valued-indexes)参照してください。

### システム変数 {#system-variables}

| 変数名                                                                                                                                                  | タイプを変更   | 説明                                                                                                                                                                                                                                                            |
| ---------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `tidb_enable_amend_pessimistic_txn`                                                                                                                  | 削除されました  | v6.5.0 以降、この変数は非推奨です。v6.6.0 以降、この変数と`AMEND TRANSACTION`機能は削除されます。TiDB は`Information schema is changed`エラーを回避するために[メタロック](/metadata-lock.md)使用します。                                                                                                             |
| `tidb_enable_concurrent_ddl`                                                                                                                         | 削除されました  | この変数は、TiDB が同時 DDL ステートメントを使用できるようにするかどうかを制御します。この変数が無効になっている場合、TiDB は同時 DDL 実行を限定的にサポートする古い DDL 実行フレームワークを使用します。v6.6.0 以降では、この変数は削除され、TiDB は古い DDL 実行フレームワークをサポートしなくなりました。                                                                                   |
| `tidb_ttl_job_run_interval`                                                                                                                          | 削除されました  | この変数は、バックグラウンドでの TTL ジョブのスケジュール間隔を制御するために使用されます。v6.6.0 以降では、TiDB がすべてのテーブルに対して TTL ランタイムを制御するための`tidb_ttl_job_run_interval`よりも柔軟な`TTL_JOB_INTERVAL`属性を提供するため、この変数は削除されます。                                                                                     |
| [`foreign_key_checks`](/system-variables.md#foreign_key_checks)                                                                                      | 修正済み     | この変数は、外部キー制約チェックを有効にするかどうかを制御します。デフォルト値は`OFF`から`ON`に変更され、これはデフォルトで外部キーチェックが有効になることを意味します。                                                                                                                                                                     |
| [`tidb_enable_foreign_key`](/system-variables.md#tidb_enable_foreign_key-new-in-v630)                                                                | 修正済み     | この変数は、外部キー機能を有効にするかどうかを制御します。デフォルト値は`OFF`から`ON`に変更され、デフォルトで外部キーが有効になることを意味します。                                                                                                                                                                                |
| `tidb_enable_general_plan_cache`                                                                                                                     | 修正済み     | この変数は、一般プラン キャッシュを有効にするかどうかを制御します。v6.6.0 以降、この変数の名前は[`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache)に変更されます。                                                                                                 |
| [`tidb_enable_historical_stats`](/system-variables.md#tidb_enable_historical_stats)                                                                  | 修正済み     | この変数は、履歴統計を有効にするかどうかを制御します。デフォルト値は`OFF`から`ON`に変更され、履歴統計がデフォルトで有効になっていることを意味します。                                                                                                                                                                               |
| [`tidb_enable_telemetry`](/system-variables.md#tidb_enable_telemetry-new-in-v402-and-deprecated-in-v810)                                             | 修正済み     | デフォルト値は`ON`から`OFF`に変更され、これは TiDB でテレメトリがデフォルトで無効になっていることを意味します。                                                                                                                                                                                               |
| `tidb_general_plan_cache_size`                                                                                                                       | 修正済み     | この変数は、一般プラン キャッシュによってキャッシュできる実行プランの最大数を制御します。v6.6.0 以降、この変数の名前は[`tidb_non_prepared_plan_cache_size`](/system-variables.md#tidb_non_prepared_plan_cache_size)に変更されます。                                                                                          |
| [`tidb_replica_read`](/system-variables.md#tidb_replica_read-new-in-v40)                                                                             | 修正済み     | この変数に新しい値オプション`learner`が追加され、TiDB が読み取り専用ノードからデータを読み取る学習者レプリカが指定されます。                                                                                                                                                                                         |
| [`tidb_replica_read`](/system-variables.md#tidb_replica_read-new-in-v40)                                                                             | 修正済み     | TiDB クラスターの全体的な読み取り可用性を向上させるために、この変数に新しい値オプション`prefer-leader`が追加されました。このオプションが設定されている場合、TiDB はリーダー レプリカからの読み取りを優先します。リーダー レプリカのパフォーマンスが大幅に低下すると、TiDB は自動的にフォロワー レプリカから読み取ります。                                                                                 |
| [`tidb_store_batch_size`](/system-variables.md#tidb_store_batch_size)                                                                                | 修正済み     | この変数は、 `IndexLookUp`オペレータのコプロセッサータスクのバッチ サイズを制御します。3 `0`バッチを無効にすることを意味します。v6.6.0 以降では、デフォルト値が`0`から`4`に変更され、リクエストのバッチごとに 4 つのコプロセッサータスクが 1 つのタスクにバッチ処理されることを意味します。                                                                                             |
| [`mpp_exchange_compression_mode`](/system-variables.md#mpp_exchange_compression_mode-new-in-v660)                                                    | 新しく追加された | この変数は、MPP Exchange 演算子のデータ圧縮モードを指定します。これは、TiDB がバージョン番号`1`の MPP 実行プランを選択した場合に有効になります。デフォルト値`UNSPECIFIED` 、TiDB が自動的に`FAST`圧縮モードを選択することを意味します。                                                                                                                 |
| [`mpp_version`](/system-variables.md#mpp_version-new-in-v660)                                                                                        | 新しく追加された | この変数は、MPP 実行プランのバージョンを指定します。バージョンが指定されると、TiDB は指定されたバージョンの MPP 実行プランを選択します。デフォルト値`UNSPECIFIED`は、TiDB が最新バージョン`1`を自動的に選択することを意味します。                                                                                                                            |
| [`tidb_ddl_distribute_reorg`](https://docs.pingcap.com/tidb/v6.6/system-variables#tidb_ddl_distribute_reorg-new-in-v660)                             | 新しく追加された | この変数は、DDL 再編成フェーズの分散実行を有効にしてこのフェーズを高速化するかどうかを制御します。デフォルト値`OFF` DDL 再編成フェーズの分散実行をデフォルトで有効にしないことを意味します。現在、この変数は`ADD INDEX`に対してのみ有効です。                                                                                                                           |
| [`tidb_enable_historical_stats_for_capture`](/system-variables.md#tidb_enable_historical_stats_for_capture)                                          | 新しく追加された | この変数は、 `PLAN REPLAYER CAPTURE`でキャプチャされた情報にデフォルトで履歴統計が含まれるかどうかを制御します。デフォルト値`OFF` 、履歴統計がデフォルトで含まれないことを意味します。                                                                                                                                                    |
| [`tidb_enable_plan_cache_for_param_limit`](/system-variables.md#tidb_enable_plan_cache_for_param_limit-new-in-v660)                                  | 新しく追加された | この変数は、 プリペアドプランキャッシュ が`Limit`後に`COUNT`含む実行プランをキャッシュするかどうかを制御します。デフォルト値は`ON`で、 プリペアドプランキャッシュ がそのような実行プランのキャッシュをサポートすることを意味します。Prepared プリペアドプランキャッシュ は、 10000 を超える数をカウントする`COUNT`条件を含む実行プランのキャッシュをサポートしないことに注意してください。                                          |
| [`tidb_enable_plan_replayer_capture`](/system-variables.md#tidb_enable_plan_replayer_capture)                                                        | 新しく追加された | この変数は、 [`PLAN REPLAYER CAPTURE`機能](/sql-plan-replayer.md#use-plan-replayer-capture-to-capture-target-plans)を有効にするかどうかを制御します。デフォルト値`OFF` 、 `PLAN REPLAYER CAPTURE`機能を無効にすることを意味します。                                                                            |
| [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-new-in-v660)                                                      | 新しく追加された | この変数は、リソース制御機能を有効にするかどうかを制御します。デフォルト値は`OFF`です。この変数を`ON`に設定すると、TiDB クラスターはリソース グループに基づいてアプリケーションのリソース分離をサポートします。                                                                                                                                               |
| [`tidb_historical_stats_duration`](/system-variables.md#tidb_historical_stats_duration-new-in-v660)                                                  | 新しく追加された | この変数は、履歴統計がstorageに保持される期間を制御します。デフォルト値は 7 日です。                                                                                                                                                                                                               |
| [`tidb_index_join_double_read_penalty_cost_rate`](/system-variables.md#tidb_index_join_double_read_penalty_cost_rate-new-in-v660)                    | 新しく追加された | この変数は、インデックス結合の選択にペナルティ コストを追加するかどうかを制御します。デフォルト値`0`は、この機能がデフォルトで無効になっていることを意味します。                                                                                                                                                                            |
| [`tidb_pessimistic_txn_aggressive_locking`](https://docs.pingcap.com/tidb/v6.6/system-variables#tidb_pessimistic_txn_aggressive_locking-new-in-v660) | 新しく追加された | この変数は、悲観的トランザクションに拡張悲観的ロック ウェイクアップ モデルを使用するかどうかを制御します。デフォルト値`OFF`は、悲観的トランザクションにこのようなウェイクアップ モデルをデフォルトで使用しないことを意味します。                                                                                                                                          |
| [`tidb_stmt_summary_enable_persistent`](/system-variables.md#tidb_stmt_summary_enable_persistent-new-in-v660)                                        | 新しく追加された | この変数は読み取り専用です。 [ステートメントの概要の永続性](/statement-summary-tables.md#persist-statements-summary)有効にするかどうかを制御します。 この変数の値は、構成項目[`tidb_stmt_summary_enable_persistent`](/tidb-configuration-file.md#tidb_stmt_summary_enable_persistent-new-in-v660)の値と同じです。             |
| [`tidb_stmt_summary_filename`](/system-variables.md#tidb_stmt_summary_filename-new-in-v660)                                                          | 新しく追加された | この変数は読み取り専用です。1 [ステートメントの概要の永続性](/statement-summary-tables.md#persist-statements-summary)有効な場合に永続データが書き込まれるファイルを指定します。この変数の値は、構成項目[`tidb_stmt_summary_filename`](/tidb-configuration-file.md#tidb_stmt_summary_filename-new-in-v660)の値と同じです。                  |
| [`tidb_stmt_summary_file_max_backups`](/system-variables.md#tidb_stmt_summary_file_max_backups-new-in-v660)                                          | 新しく追加された | この変数は読み取り専用です。 [ステートメントの概要の永続性](/statement-summary-tables.md#persist-statements-summary)が有効な場合に保持できるデータファイルの最大数を指定します。 この変数の値は、構成項目[`tidb_stmt_summary_file_max_backups`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_backups-new-in-v660)の値と同じです。 |
| [`tidb_stmt_summary_file_max_days`](/system-variables.md#tidb_stmt_summary_file_max_days-new-in-v660)                                                | 新しく追加された | この変数は読み取り専用です。1 [ステートメントの概要の永続性](/statement-summary-tables.md#persist-statements-summary)有効な場合に永続データ ファイルを保持する最大日数を指定します。この変数の値は、構成項目[`tidb_stmt_summary_file_max_days`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_days-new-in-v660)の値と同じです。     |
| [`tidb_stmt_summary_file_max_size`](/system-variables.md#tidb_stmt_summary_file_max_size-new-in-v660)                                                | 新しく追加された | この変数は読み取り専用です。1 [ステートメントの概要の永続性](/statement-summary-tables.md#persist-statements-summary)有効な場合、永続データファイルの最大サイズを指定します。この変数の値は、構成項目[`tidb_stmt_summary_file_max_size`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_size-new-in-v660)の値と同じです。         |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーションパラメータ                                                                                                                                                                                                                                           | タイプを変更   | 説明                                                                                                                                                                                           |
| -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ティクヴ           | `rocksdb.enable-statistics`                                                                                                                                                                                                                               | 削除されました  | この設定項目は、RocksDB 統計を有効にするかどうかを指定します。v6.6.0 以降では、この項目は削除されています。RocksDB 統計は、診断を支援するために、すべてのクラスターでデフォルトで有効になっています。詳細については、 [＃13942](https://github.com/tikv/tikv/pull/13942)参照してください。            |
| ティクヴ           | `raftdb.enable-statistics`                                                                                                                                                                                                                                | 削除されました  | この設定項目は、 Raft RocksDB 統計を有効にするかどうかを指定します。v6.6.0 以降では、この項目は削除されています。Raft RocksDB 統計は、診断を支援するために、すべてのクラスターでデフォルトで有効になっています。詳細については、 [＃13942](https://github.com/tikv/tikv/pull/13942)参照してください。 |
| ティクヴ           | `storage.block-cache.shared`                                                                                                                                                                                                                              | 削除されました  | v6.6.0 以降ではこの設定項目は削除され、ブロックキャッシュはデフォルトで有効になり、無効にすることはできません。詳細については、 [＃12936](https://github.com/tikv/tikv/issues/12936)参照してください。                                                             |
| DM             | `on-duplicate`                                                                                                                                                                                                                                            | 削除されました  | この構成項目は、完全なインポート フェーズ中に競合を解決する方法を制御します。v6.6.0 では、 `on-duplicate`代わりに新しい構成項目`on-duplicate-logical`と`on-duplicate-physical`が導入されました。                                                           |
| ティビ            | [`enable-telemetry`](/tidb-configuration-file.md#enable-telemetry-new-in-v402-and-deprecated-in-v810)                                                                                                                                                     | 修正済み     | v6.6.0 以降では、デフォルト値が`true`から`false`に変更され、TiDB ではテレメトリがデフォルトで無効になっていることを意味します。                                                                                                                 |
| ティクヴ           | [`rocksdb.defaultcf.block-size`](/tikv-configuration-file.md#block-size)と[`rocksdb.writecf.block-size`](/tikv-configuration-file.md#block-size)                                                                                                           | 修正済み     | デフォルト値は`64K`から`32K`に変更されます。                                                                                                                                                                  |
| ティクヴ           | [`rocksdb.defaultcf.block-cache-size`](/tikv-configuration-file.md#block-cache-size) [`rocksdb.writecf.block-cache-size`](/tikv-configuration-file.md#block-cache-size) [`rocksdb.lockcf.block-cache-size`](/tikv-configuration-file.md#block-cache-size) | 非推奨      | v6.6.0 以降では、これらの設定項目は非推奨になりました。詳細については、 [＃12936](https://github.com/tikv/tikv/issues/12936)参照してください。                                                                                         |
| PD             | [`enable-telemetry`](/pd-configuration-file.md#enable-telemetry)                                                                                                                                                                                          | 修正済み     | v6.6.0 以降では、デフォルト値が`true`から`false`に変更され、TiDB ダッシュボードでテレメトリがデフォルトで無効になっていることを意味します。                                                                                                           |
| DM             | [`import-mode`](/dm/task-configuration-file-full.md)                                                                                                                                                                                                      | 修正済み     | この構成項目の可能な値は、 `"sql"`と`"loader"`から`"logical"`と`"physical"`に変更されます。デフォルト値は`"logical"`で、これは TiDB Lightning の論理インポート モードを使用してデータをインポートすることを意味します。                                               |
| TiFlash        | [`profile.default.max_memory_usage_for_all_queries`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                                                                                                                                    | 修正済み     | すべてのクエリで生成される中間データのメモリ使用量の制限を指定します。v6.6.0 以降では、デフォルト値が`0`から`0.8`に変更され、制限が合計メモリの 80% になることを意味します。                                                                                             |
| ティCDC          | [`consistent.storage`](/ticdc/ticdc-sink-to-mysql.md#prerequisites)                                                                                                                                                                                       | 修正済み     | この構成項目は、REDO ログ バックアップが保存されるパスを指定します。1、GCS、および Azure に対して、 `scheme` 2 つの値オプションが追加されました。                                                                                                      |
| ティビ            | [`initialize-sql-file`](/tidb-configuration-file.md#initialize-sql-file-new-in-v660)                                                                                                                                                                      | 新しく追加された | この構成項目は、TiDB クラスターを初めて起動したときに実行される SQL スクリプトを指定します。デフォルト値は空です。                                                                                                                               |
| ティビ            | [`tidb_stmt_summary_enable_persistent`](/tidb-configuration-file.md#tidb_stmt_summary_enable_persistent-new-in-v660)                                                                                                                                      | 新しく追加された | この構成項目は、ステートメント サマリーの永続性を有効にするかどうかを制御します。デフォルト値は`false`で、この機能はデフォルトでは有効になっていないことを意味します。                                                                                                      |
| ティビ            | [`tidb_stmt_summary_file_max_backups`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_backups-new-in-v660)                                                                                                                                        | 新しく追加された | ステートメント サマリーの永続化が有効になっている場合、この構成では永続化できるデータ ファイルの最大数を指定します。1 `0`ファイル数に制限がないことを意味します。                                                                                                         |
| ティビ            | [`tidb_stmt_summary_file_max_days`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_days-new-in-v660)                                                                                                                                              | 新しく追加された | ステートメント サマリーの永続性が有効になっている場合、この構成では永続データ ファイルを保持する最大日数を指定します。                                                                                                                                 |
| ティビ            | [`tidb_stmt_summary_file_max_size`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_size-new-in-v660)                                                                                                                                              | 新しく追加された | ステートメント サマリーの永続性が有効になっている場合、この構成は永続データ ファイルの最大サイズ (MiB 単位) を指定します。                                                                                                                           |
| ティビ            | [`tidb_stmt_summary_filename`](/tidb-configuration-file.md#tidb_stmt_summary_filename-new-in-v660)                                                                                                                                                        | 新しく追加された | ステートメント サマリーの永続性が有効になっている場合、この構成では永続データが書き込まれるファイルを指定します。                                                                                                                                    |
| ティクヴ           | [`resource-control.enabled`](/tikv-configuration-file.md#resource-control)                                                                                                                                                                                | 新しく追加された | 対応するリソース グループの要求単位 (RU) に従って、ユーザーのフォアグラウンド読み取り/書き込み要求のスケジュールを有効にするかどうか。デフォルト値は`false`で、対応するリソース グループの RU に従ってスケジュールを無効にすることを意味します。                                                           |
| ティクヴ           | [`storage.engine`](/tikv-configuration-file.md#engine-new-in-v660)                                                                                                                                                                                        | 新しく追加された | この構成項目は、storageエンジンのタイプを指定します。値のオプションは`"raft-kv"`と`"partitioned-raft-kv"`です。この構成項目は、クラスターの作成時にのみ指定でき、指定した後は変更できません。                                                                          |
| ティクヴ           | [`rocksdb.write-buffer-flush-oldest-first`](/tikv-configuration-file.md#write-buffer-flush-oldest-first-new-in-v660)                                                                                                                                      | 新しく追加された | この構成項目は、現在の RocksDB の`memtable`のメモリ使用量がしきい値に達したときに使用するフラッシュ戦略を指定します。                                                                                                                         |
| ティクヴ           | [`rocksdb.write-buffer-limit`](/tikv-configuration-file.md#write-buffer-limit-new-in-v660)                                                                                                                                                                | 新しく追加された | この構成項目は、単一の TiKV 内のすべての RocksDB インスタンスの`memtable`によって使用される合計メモリの制限を指定します。デフォルト値は、マシンの合計メモリの 25% です。                                                                                          |
| PD             | [`pd-server.enable-gogc-tuner`](/pd-configuration-file.md#enable-gogc-tuner-new-in-v660)                                                                                                                                                                  | 新しく追加された | この設定項目は、デフォルトでは無効になっている GOGC チューナーを有効にするかどうかを制御します。                                                                                                                                          |
| PD             | [`pd-server.gc-tuner-threshold`](/pd-configuration-file.md#gc-tuner-threshold-new-in-v660)                                                                                                                                                                | 新しく追加された | この設定項目は、GOGC を調整するための最大メモリしきい値比率を指定します。デフォルト値は`0.6`です。                                                                                                                                       |
| PD             | [`pd-server.server-memory-limit-gc-trigger`](/pd-configuration-file.md#server-memory-limit-gc-trigger-new-in-v660)                                                                                                                                        | 新しく追加された | この設定項目は、PD が GC をトリガーしようとするしきい値比率を指定します。デフォルト値は`0.7`です。                                                                                                                                      |
| PD             | [`pd-server.server-memory-limit`](/pd-configuration-file.md#server-memory-limit-new-in-v660)                                                                                                                                                              | 新しく追加された | この設定項目は、PD インスタンスのメモリ制限比率を指定します。値`0`はメモリ制限がないことを意味します。                                                                                                                                       |
| ティCDC          | [`scheduler.region-per-span`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)                                                                                                                                                      | 新しく追加された | この設定項目は、リージョンの数に基づいてテーブルを複数のレプリケーション範囲に分割するかどうかを制御します。これらの範囲は、複数の TiCDC ノードによってレプリケートできます。デフォルト値は`50000`です。                                                                                  |
| TiDB Lightning | [`compress-kv-pairs`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)                                                                                                                                                                | 新しく追加された | この設定項目は、物理インポート モードで KV ペアを TiKV に送信するときに圧縮を有効にするかどうかを制御します。デフォルト値は空で、圧縮が有効になっていないことを意味します。                                                                                                  |
| DM             | [`checksum-physical`](/dm/task-configuration-file-full.md)                                                                                                                                                                                                | 新しく追加された | この構成項目は、インポート後にデータの整合性を検証するために DM が各テーブルに対して`ADMIN CHECKSUM TABLE <table>`実行するかどうかを制御します。デフォルト値は`"required"`で、インポート後に管理チェックサムを実行します。チェックサムが失敗すると、DM はタスクを一時停止し、失敗を手動で処理する必要があります。            |
| DM             | [`disk-quota-physical`](/dm/task-configuration-file-full.md)                                                                                                                                                                                              | 新しく追加された | この設定項目はディスククォータを設定します。TiDB TiDB Lightningの[`disk-quota`設定](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#configure-disk-quota-new-in-v620)に相当します。                             |
| DM             | [`on-duplicate-logical`](/dm/task-configuration-file-full.md)                                                                                                                                                                                             | 新しく追加された | この構成項目は、論理インポート モードで DM が競合するデータを解決する方法を制御します。デフォルト値は`"replace"`で、これは新しいデータを使用して既存のデータを置き換えることを意味します。                                                                                        |
| DM             | [`on-duplicate-physical`](/dm/task-configuration-file-full.md)                                                                                                                                                                                            | 新しく追加された | この構成項目は、物理インポート モードで DM が競合するデータを解決する方法を制御します。デフォルト値は`"none"`で、競合するデータを解決しないことを意味します。3 `"none"`パフォーマンスが最高ですが、ダウンストリーム データベースでデータの不整合が発生する可能性があります。                                           |
| DM             | [`sorting-dir-physical`](/dm/task-configuration-file-full.md)                                                                                                                                                                                             | 新しく追加された | この設定項目は、物理インポート モードでのローカル KV ソートに使用するディレクトリを指定します。デフォルト値は`dir`設定と同じです。                                                                                                                       |
| 同期差分インスペクター    | [`skip-non-existing-table`](/sync-diff-inspector/sync-diff-inspector-overview.md#configuration-file-description)                                                                                                                                          | 新しく追加された | この構成項目は、ダウンストリームのテーブルがアップストリームに存在しない場合に、アップストリームとダウンストリームのデータ整合性のチェックをスキップするかどうかを制御します。                                                                                                      |
| ティスパーク         | [`spark.tispark.replica_read`](/tispark-overview.md#tispark-configurations)                                                                                                                                                                               | 新しく追加された | この構成項目は、読み取るレプリカの種類を制御します。値のオプションは`leader` 、 `follower` 、 `learner`です。                                                                                                                       |
| ティスパーク         | [`spark.tispark.replica_read.label`](/tispark-overview.md#tispark-configurations)                                                                                                                                                                         | 新しく追加された | この構成項目は、ターゲット TiKV ノードのラベルを設定するために使用されます。                                                                                                                                                    |

### その他 {#others}

-   [`store-io-pool-size`](/tikv-configuration-file.md#store-io-pool-size-new-in-v530)動的な変更をサポートします。これにより、より柔軟な TiKV パフォーマンス チューニングが可能になります。
-   `LIMIT`句の制限を削除し、実行パフォーマンスを向上させます。
-   v6.6.0 以降、 BR はv6.1.0 より前のクラスターへのデータの復元をサポートしていません。
-   v6.6.0 以降、TiDB は、潜在的な正確性の問題のため、パーティション化されたテーブルの列タイプの変更をサポートしなくなりました。

## 改善点 {#improvements}

-   ティビ

    -   TTL バックグラウンド クリーニング タスクのスケジュール メカニズムを改善し、単一テーブルのクリーニング タスクを複数のサブタスクに分割し、複数の TiDB ノードで同時に実行するようにスケジュールできるようになりました[＃40361](https://github.com/pingcap/tidb/issues/40361) @ [ヤンケオ](https://github.com/YangKeao)
    -   デフォルト以外の区切り文字[＃39662](https://github.com/pingcap/tidb/issues/39662) @ [ミョンス](https://github.com/mjonss)を設定した後に複数のステートメントを実行して返される結果の列名の表示を最適化します。
    -   警告メッセージが生成された後のステートメントの実行効率を最適化する[＃39702](https://github.com/pingcap/tidb/issues/39702) @ [天菜まお](https://github.com/tiancaiamao)
    -   `ADD INDEX` (実験的) [＃37119](https://github.com/pingcap/tidb/issues/37119) @ [ジムララ](https://github.com/zimulala)の分散データバックフィルをサポート
    -   列[＃38356](https://github.com/pingcap/tidb/issues/38356) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)のデフォルト値として`CURDATE()`使用することをサポートします
    -   `partial order prop push down` LIST タイプのパーティションテーブル[＃40273](https://github.com/pingcap/tidb/issues/40273) @ [ウィノロス](https://github.com/winoros)をサポートするようになりました
    -   オプティマイザヒントと実行プランバインディング間の競合に関するエラーメッセージを追加する[＃40910](https://github.com/pingcap/tidb/issues/40910) @ [思い出させる](https://github.com/Reminiscent)
    -   いくつかのシナリオでプラン キャッシュを使用するときに最適でないプランを回避するためにプラン キャッシュ戦略を最適化します[＃40312](https://github.com/pingcap/tidb/pull/40312) [＃40218](https://github.com/pingcap/tidb/pull/40218) [＃40280](https://github.com/pingcap/tidb/pull/40280) [＃41136](https://github.com/pingcap/tidb/pull/41136) [＃40686](https://github.com/pingcap/tidb/pull/40686) @ [qw4990](https://github.com/qw4990)
    -   メモリリークやパフォーマンスの低下を防ぐために、期限切れの領域キャッシュを定期的にクリアします[＃40461](https://github.com/pingcap/tidb/issues/40461) @ [スティクナーフ](https://github.com/sticnarf)
    -   `MODIFY COLUMN`はパーティションテーブル[＃39915](https://github.com/pingcap/tidb/issues/39915) @ [翻訳:](https://github.com/wjhuang2016)ではサポートされていません
    -   パーティションテーブルが依存する列の名前変更を無効にする[#40150](https://github.com/pingcap/tidb/issues/40150) @ [ミョンス](https://github.com/mjonss)
    -   パーティションテーブルが依存する列が削除されたときに報告されるエラーメッセージを改善する[＃38739](https://github.com/pingcap/tidb/issues/38739) @ [ジフハウス](https://github.com/jiyfhust)
    -   `min-resolved-ts` [＃39836](https://github.com/pingcap/tidb/issues/39836) @ [定義2014](https://github.com/Defined2014)のチェックに失敗した場合、 `FLASHBACK CLUSTER`再試行するメカニズムを追加します。

-   ティクヴ

    -   パーティション化された raft-kv モードでのいくつかのパラメータのデフォルト値を最適化します。TiKV 構成項目`storage.block-cache.capacity`のデフォルト値は 45% から 30% に調整され、デフォルト値`region-split-size`は`96MiB`から`10GiB`に調整されます。raft-kv モードを使用し、 `enable-region-bucket`が`true`の場合、 `region-split-size`デフォルトで 1 GiB に調整されます[＃12842](https://github.com/tikv/tikv/issues/12842) @ [トニー](https://github.com/tonyxuqqi)
    -   Raftstore非同期書き込み[＃13730](https://github.com/tikv/tikv/issues/13730) @ [コナー1996](https://github.com/Connor1996)での優先スケジューリングをサポート
    -   1コア未満のCPUでのTiKVの起動をサポート[＃13586](https://github.com/tikv/tikv/issues/13586) [＃13752](https://github.com/tikv/tikv/issues/13752) [＃14017](https://github.com/tikv/tikv/issues/14017) @ [アンドレイドDB](https://github.com/andreid-db)
    -   Raftstoreスロースコアの新しい検出メカニズムを最適化し、 `evict-slow-trend-scheduler` [＃14131](https://github.com/tikv/tikv/issues/14131) @ [内側](https://github.com/innerr)を追加します
    -   RocksDB のブロックキャッシュを強制的に共有し、CF [＃12936](https://github.com/tikv/tikv/issues/12936) @ [忙しいカケス](https://github.com/busyjay)に従ってブロックキャッシュを個別に設定することはサポートされなくなりました。

-   PD

    -   OOM 問題を軽減するためのグローバルメモリしきい値の管理のサポート (実験的) [＃5827](https://github.com/tikv/pd/issues/5827) @ [ネス](https://github.com/hnes)
    -   GC圧力を緩和するためにGCチューナーを追加する（実験的） [＃5827](https://github.com/tikv/pd/issues/5827) @ [ネス](https://github.com/hnes)
    -   異常なノードを検出してスケジュールする`evict-slow-trend-scheduler`スケジューラを追加します[＃5808](https://github.com/tikv/pd/pull/5808) @ [内側](https://github.com/innerr)
    -   キースペース[＃5293](https://github.com/tikv/pd/issues/5293) @ [アメーバ原生動物](https://github.com/AmoebaProtozoa)管理するキースペース マネージャーを追加します。

-   TiFlash

    -   TiFlashデータスキャンプロセスにおけるMVCCフィルタリング操作を分離する独立したMVCCビットマップフィルタをサポートし、将来のデータスキャンプロセスの最適化の基盤を提供します[＃6296](https://github.com/pingcap/tiflash/issues/6296) @ [ジンヘリン](https://github.com/JinheLin)
    -   クエリがない場合、 TiFlashのメモリ使用量を最大30％削減します[＃6589](https://github.com/pingcap/tiflash/pull/6589) @ [ホンユンヤン](https://github.com/hongyunyan)

-   ツール

    -   バックアップと復元 (BR)

        -   TiKV 側でのログ バックアップ ファイルのダウンロードの同時実行を最適化して、通常のシナリオでの PITR リカバリのパフォーマンスを向上させます[＃14206](https://github.com/tikv/tikv/issues/14206) @ [ユジュンセン](https://github.com/YuJuncen)

    -   ティCDC

        -   TiCDC レプリケーション パフォーマンスを向上させるバッチ`UPDATE` DML ステートメントのサポート[＃8084](https://github.com/pingcap/tiflow/issues/8084) @ [アミヤンフェイ](https://github.com/amyangfei)
        -   シンクのスループットを向上させるために、非同期モードでMQシンクとMySQLシンクを実装する[＃5928](https://github.com/pingcap/tiflow/issues/5928) @ [ヒック](https://github.com/hicqu) @ [ハイラスティン](https://github.com/Rustin170506)

    -   TiDB データ移行 (DM)

        -   DMアラートルールとコンテンツを最適化する[＃7376](https://github.com/pingcap/tiflow/issues/7376) @ [D3ハンター](https://github.com/D3Hunter)

            以前は、関連するエラーが発生するたびに、「DM_XXX_process_exits_with_error」のようなアラートが発生していました。しかし、一部のアラートはアイドル状態のデータベース接続によって発生し、再接続後に回復できます。このようなアラートを減らすために、DM はエラーを自動的に回復可能なエラーと回復不可能なエラーの 2 種類に分類しています。

            -   自動的に回復可能なエラーの場合、DM は 2 分以内にエラーが 3 回以上発生した場合にのみアラートを報告します。
            -   自動的に回復できないエラーの場合、DM は元の動作を維持し、すぐにアラートを報告します。

        -   非同期/バッチリレーライター[＃4287](https://github.com/pingcap/tiflow/issues/4287) @ [GMHDBJD](https://github.com/GMHDBJD)を追加してリレーパフォーマンスを最適化します

    -   TiDB Lightning

        -   物理インポートモードはキースペース[＃40531](https://github.com/pingcap/tidb/issues/40531) @ [イオマンサス](https://github.com/iosmanthus)をサポートします
        -   競合の最大数を`lightning.max-error` [＃40743](https://github.com/pingcap/tidb/issues/40743) @ [ダシュン](https://github.com/dsdashun)で設定するサポート
        -   BOM ヘッダー[＃40744](https://github.com/pingcap/tidb/issues/40744) @ [ダシュン](https://github.com/dsdashun)を含む CSV データ ファイルのインポートをサポート
        -   TiKV フロー制限エラーが発生した場合は処理ロジックを最適化し、代わりに他の利用可能な領域を試します[#40205](https://github.com/pingcap/tidb/issues/40205) @ [ランス6716](https://github.com/lance6716)
        -   インポート中にテーブルの外部キーのチェックを無効にする[#40027](https://github.com/pingcap/tidb/issues/40027) @ [眠いモグラ](https://github.com/sleepymole)

    -   Dumpling

        -   外部キー[＃39913](https://github.com/pingcap/tidb/issues/39913) @ [リチュンジュ](https://github.com/lichunzhu)の設定のエクスポートをサポート

    -   同期差分インスペクター

        -   下流のテーブルが上流に存在しない場合に上流と下流のデータ整合性のチェックをスキップするかどうかを制御する新しいパラメータ`skip-non-existing-table`を追加します[＃692](https://github.com/pingcap/tidb-tools/issues/692) @ [リチュンジュ](https://github.com/lichunzhu) @ [りゅうめんぎゃ](https://github.com/liumengya94)

## バグ修正 {#bug-fixes}

-   ティビ

    -   `datetime`値[＃39336](https://github.com/pingcap/tidb/issues/39336) @ [翻訳者](https://github.com/xuyifangreeneyes)が正しくないために統計収集タスクが失敗する問題を修正しました
    -   テーブル作成[＃38189](https://github.com/pingcap/tidb/issues/38189) @ [翻訳者](https://github.com/xuyifangreeneyes)の後に`stats_meta`が作成されない問題を修正
    -   DDL データ バックフィル[＃24427](https://github.com/pingcap/tidb/issues/24427) @ [ミョンス](https://github.com/mjonss)を実行するときにトランザクションで頻繁に発生する書き込み競合を修正
    -   取り込みモード[＃39641](https://github.com/pingcap/tidb/issues/39641) @ [タンジェンタ](https://github.com/tangenta)を使用して空のテーブルにインデックスを作成できないことがある問題を修正しました。
    -   同じトランザクション内の異なるSQL文に対して、スロークエリログの`wait_ts`同じになる問題を修正[＃39713](https://github.com/pingcap/tidb/issues/39713) @ [トンスネークリン](https://github.com/TonsnakeLin)
    -   行レコード[＃39570](https://github.com/pingcap/tidb/issues/39570) @ [翻訳:](https://github.com/wjhuang2016)を削除するプロセス中に列を追加すると`Assertion Failed`エラーが報告される問題を修正しました
    -   列タイプ[＃39643](https://github.com/pingcap/tidb/issues/39643) @ [ジムララ](https://github.com/zimulala)を変更するときに`not a DDL owner`エラーが報告される問題を修正しました
    -   `AUTO_INCREMENT`列[＃38950](https://github.com/pingcap/tidb/issues/38950) @ [ドゥージール9](https://github.com/Dousir9)の自動増分値が使い果たされた後に行を挿入してもエラーが報告されない問題を修正
    -   式インデックス[＃39784](https://github.com/pingcap/tidb/issues/39784) @ [定義2014](https://github.com/Defined2014)を作成するときに`Unknown column`エラーが報告される問題を修正しました
    -   生成された式にこのテーブルの名前が含まれている場合、名前が変更されたテーブルにデータを挿入できない問題を修正しました[＃39826](https://github.com/pingcap/tidb/issues/39826) @ [定義2014](https://github.com/Defined2014)
    -   列が書き込み専用の場合、 `INSERT ignore`ステートメントでデフォルト値を入力できない問題を修正[＃40192](https://github.com/pingcap/tidb/issues/40192) @ [ヤンケオ](https://github.com/YangKeao)
    -   リソース管理モジュール[＃40546](https://github.com/pingcap/tidb/issues/40546) @ [ジムララ](https://github.com/zimulala)を無効にしたときにリソースが解放されない問題を修正
    -   TTLタスクが時間[#40109](https://github.com/pingcap/tidb/issues/40109) @ [ヤンケオ](https://github.com/YangKeao)で統計更新をトリガーできない問題を修正
    -   TiDB がキー範囲[＃40158](https://github.com/pingcap/tidb/issues/40158) @ [天菜まお](https://github.com/tiancaiamao)を構築するときに`NULL`値を不適切に処理するため、予期しないデータが読み取られる問題を修正しました。
    -   `MODIFY COLUMN`文で列[＃40164](https://github.com/pingcap/tidb/issues/40164) @ [翻訳:](https://github.com/wjhuang2016)のデフォルト値も変更すると、テーブルに不正な値が書き込まれる問題を修正しました。
    -   テーブル[＃38436](https://github.com/pingcap/tidb/issues/38436) @ [タンジェンタ](https://github.com/tangenta)に多くのリージョンがある場合、無効なリージョンキャッシュが原因でインデックス追加操作が非効率になる問題を修正しました。
    -   自動増分 ID [＃40584](https://github.com/pingcap/tidb/issues/40584) @ [ドゥージール9](https://github.com/Dousir9)の割り当て時に発生するデータ競合を修正
    -   JSON の not 演算子の実装が MySQL [＃40683](https://github.com/pingcap/tidb/issues/40683) @ [ヤンケオ](https://github.com/YangKeao)の実装と互換性がない問題を修正しました
    -   同時ビューによって DDL 操作がブロックされる可能性がある問題を修正[＃40352](https://github.com/pingcap/tidb/issues/40352) @ [沢民州](https://github.com/zeminzhou)
    -   パーティション化されたテーブルの列を変更する DDL ステートメントを同時に実行することによって発生するデータの不整合を修正します[#40620](https://github.com/pingcap/tidb/issues/40620) @ [ミョンス](https://github.com/mjonss) @ [ミョンス](https://github.com/mjonss)
    -   パスワード[＃40831](https://github.com/pingcap/tidb/issues/40831) @ [ドヴェーデン](https://github.com/dveeden)を指定せずに認証に`caching_sha2_password`使用すると「不正なパケット」が報告される問題を修正
    -   テーブルの主キーに`ENUM`列[＃40456](https://github.com/pingcap/tidb/issues/40456) @ [lcwangchao](https://github.com/lcwangchao)が含まれている場合にTTLタスクが失敗する問題を修正
    -   MDLによってブロックされた一部のDDL操作が`mysql.tidb_mdl_view` [＃40838](https://github.com/pingcap/tidb/issues/40838) @ [ヤンケオ](https://github.com/YangKeao)でクエリできない問題を修正
    -   DDL取り込み[＃40970](https://github.com/pingcap/tidb/issues/40970) @ [タンジェンタ](https://github.com/tangenta)中にデータ競合が発生する可能性がある問題を修正
    -   タイムゾーンの変更後にTTLタスクが一部のデータを誤って削除する可能性がある問題を修正[＃41043](https://github.com/pingcap/tidb/issues/41043) @ [lcwangchao](https://github.com/lcwangchao)
    -   `JSON_OBJECT`場合によってはエラーを報告する可能性がある問題を修正[＃39806](https://github.com/pingcap/tidb/issues/39806) @ [ヤンケオ](https://github.com/YangKeao)
    -   初期化中に TiDB がデッドロックする可能性がある問題を修正[#40408](https://github.com/pingcap/tidb/issues/40408) @ [定義2014](https://github.com/Defined2014)
    -   メモリの再利用により、システム変数の値が誤って変更される場合がある問題を修正[＃40979](https://github.com/pingcap/tidb/issues/40979) @ [lcwangchao](https://github.com/lcwangchao)
    -   取り込みモード[＃40464](https://github.com/pingcap/tidb/issues/40464) @ [タンジェンタ](https://github.com/tangenta)で一意のインデックスが作成されるときに、データがインデックスと一致しない可能性がある問題を修正しました。
    -   同じテーブルを同時に切り捨てるときに、一部の切り捨て操作が MDL によってブロックできない問題を修正[＃40484](https://github.com/pingcap/tidb/issues/40484) @ [翻訳:](https://github.com/wjhuang2016)
    -   `SHOW PRIVILEGES`文が不完全な権限リスト[＃40591](https://github.com/pingcap/tidb/issues/40591) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)を返す問題を修正
    -   ユニークインデックス[＃40592](https://github.com/pingcap/tidb/issues/40592) @ [タンジェンタ](https://github.com/tangenta)を追加するときに TiDB がパニックになる問題を修正
    -   `ADMIN RECOVER`ステートメントを実行するとインデックスデータが破損する可能性がある問題を修正[#40430](https://github.com/pingcap/tidb/issues/40430) @ [雄吉偉](https://github.com/xiongjiwei)
    -   クエリ対象のテーブルに式インデックス[#40130](https://github.com/pingcap/tidb/issues/40130) @ [雄吉偉](https://github.com/xiongjiwei)に`CAST`式が含まれている場合にクエリが失敗する可能性がある問題を修正しました。
    -   ユニークインデックスが重複データを生成する場合がある問題を修正[＃40217](https://github.com/pingcap/tidb/issues/40217) @ [タンジェンタ](https://github.com/tangenta)
    -   多数のリージョンがあるが、 `Prepare`または`Execute` [＃39605](https://github.com/pingcap/tidb/issues/39605) @ [翻訳者](https://github.com/djshow832)を使用して一部の仮想テーブルをクエリするときにテーブル ID をプッシュダウンできない PD OOM 問題を修正しました。
    -   インデックスを[＃40879](https://github.com/pingcap/tidb/issues/40879) @ [タンジェンタ](https://github.com/tangenta)で追加するとデータ競合が発生する可能性がある問題を修正しました
    -   仮想列[＃41014](https://github.com/pingcap/tidb/issues/41014) @ [アイリンキッド](https://github.com/AilinKid)によって発生する`can't find proper physical plan`問題を修正
    -   動的トリミングモード[＃40368](https://github.com/pingcap/tidb/issues/40368) @ [イサール](https://github.com/Yisaer)でパーティションテーブルにグローバルバインディングが作成された後に TiDB が再起動できない問題を修正しました。
    -   `auto analyze`により正常なシャットダウンに長い時間がかかる問題を修正[＃40038](https://github.com/pingcap/tidb/issues/40038) @ [翻訳者](https://github.com/xuyifangreeneyes)
    -   IndexMerge 演算子がメモリ制限動作をトリガーしたときに TiDBサーバーのパニックが発生するpanicを修正[＃41036](https://github.com/pingcap/tidb/pull/41036) @ [グオシャオゲ](https://github.com/guo-shaoge)
    -   パーティションテーブルに対する`SELECT * FROM table_name LIMIT 1`クエリが遅い問題を修正[＃40741](https://github.com/pingcap/tidb/pull/40741) @ [ソロッツ](https://github.com/solotzg)

-   ティクヴ

    -   `const Enum`型を他の型[＃14156](https://github.com/tikv/tikv/issues/14156) @ [うわー](https://github.com/wshwsh12)にキャストするときに発生するエラーを修正
    -   解決されたTSによりネットワークトラフィックが増加する問題を修正[＃14092](https://github.com/tikv/tikv/issues/14092) @ [金星の上](https://github.com/overvenus)
    -   悲観的DML [＃14038](https://github.com/tikv/tikv/issues/14038) @ [ミョンケミンタ](https://github.com/MyonKeminta)が失敗した後の DML 実行中に TiDB と TiKV 間のネットワーク障害によって発生するデータの不整合の問題を修正しました。

-   PD

    -   リージョンスキャッタータスクが予期せず冗長レプリカを生成する問題を修正[＃5909](https://github.com/tikv/pd/issues/5909) @ [フンドゥンDM](https://github.com/HunDunDM)
    -   オンライン安全でないリカバリ機能が`auto-detect`モード[＃5753](https://github.com/tikv/pd/issues/5753) @ [コナー1996](https://github.com/Connor1996)で停止してタイムアウトする問題を修正
    -   特定の条件下で実行`replace-down-peer`が遅くなる問題を修正[＃5788](https://github.com/tikv/pd/issues/5788) @ [フンドゥンDM](https://github.com/HunDunDM)
    -   `ReportMinResolvedTS`の呼び出しが頻繁すぎる場合に発生する PD OOM 問題を修正[＃5965](https://github.com/tikv/pd/issues/5965) @ [フンドゥンDM](https://github.com/HunDunDM)

-   TiFlash

    -   TiFlash関連のシステム テーブルのクエリが停止する可能性がある問題を修正[＃6745](https://github.com/pingcap/tiflash/pull/6745) @ [リデズ](https://github.com/lidezhu)
    -   直交積[＃6730](https://github.com/pingcap/tiflash/issues/6730) @ [ゲンリキ](https://github.com/gengliqi)を計算するときにセミ結合が過剰なメモリを使用する問題を修正しました
    -   DECIMAL データ型の除算演算の結果が[＃6393](https://github.com/pingcap/tiflash/issues/6393) @ [リトルフォール](https://github.com/LittleFall)に丸められない問題を修正しました。
    -   `start_ts` TiFlashクエリで MPP クエリを一意に識別できないため、MPP クエリが誤ってキャンセルされる可能性がある問題を修正しました[＃43426](https://github.com/pingcap/tidb/issues/43426) @ [ヘヘチェン](https://github.com/hehechen)

-   ツール

    -   バックアップと復元 (BR)

        -   ログバックアップを復元するときに、ホットリージョンが原因で復元が失敗する問題を修正[＃37207](https://github.com/pingcap/tidb/issues/37207) @ [リーヴルス](https://github.com/Leavrth)
        -   ログバックアップが実行されているクラスターにデータを復元すると、ログバックアップファイルが回復不能になる問題を修正[＃40797](https://github.com/pingcap/tidb/issues/40797) @ [リーヴルス](https://github.com/Leavrth)
        -   PITR機能がCAバンドル[＃38775](https://github.com/pingcap/tidb/issues/38775) @ [ユジュンセン](https://github.com/YuJuncen)をサポートしない問題を修正
        -   リカバリ中に重複した一時テーブルによって発生するpanic問題を修正[＃40797](https://github.com/pingcap/tidb/issues/40797) @ [ジョッカウ](https://github.com/joccau)
        -   PITRがPDクラスタ[＃14165](https://github.com/tikv/tikv/issues/14165) @ [ユジュンセン](https://github.com/YuJuncen)の構成変更をサポートしない問題を修正
        -   PD と tidb-server 間の接続障害により PITR バックアップの進行が[＃41082](https://github.com/pingcap/tidb/issues/41082) @ [ユジュンセン](https://github.com/YuJuncen)に進まない問題を修正しました。
        -   PDとTiKV [＃14159](https://github.com/tikv/tikv/issues/14159) @ [ユジュンセン](https://github.com/YuJuncen)間の接続障害によりTiKVがPITRタスクをリッスンできない問題を修正
        -   TiDB クラスター[＃40759](https://github.com/pingcap/tidb/issues/40759) @ [ジョッカウ](https://github.com/joccau)に PITR バックアップ タスクがない場合に`resolve lock`の頻度が高すぎる問題を修正
        -   PITR バックアップ タスクを削除すると、残りのバックアップ データによって新しいタスク[#40403](https://github.com/pingcap/tidb/issues/40403) @ [ジョッカウ](https://github.com/joccau)でデータの不整合が発生する問題を修正しました。

    -   ティCDC

        -   `transaction_atomicity`と`protocol`構成ファイル[＃7935](https://github.com/pingcap/tiflow/issues/7935) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)経由で更新できない問題を修正
        -   REDOログ[＃6335](https://github.com/pingcap/tiflow/issues/6335) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)のstorageパスで事前チェ​​ックが実行されない問題を修正
        -   S3storage障害[＃8089](https://github.com/pingcap/tiflow/issues/8089) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)に対して REDO ログが許容できる期間が不十分である問題を修正
        -   TiKV または TiCDC ノード[＃8174](https://github.com/pingcap/tiflow/issues/8174) @ [ヒック](https://github.com/hicqu)スケールインまたはスケールアウトなどの特殊なシナリオで、changefeed がスタックする可能性がある問題を修正しました。
        -   TiKVノード[＃14092](https://github.com/tikv/tikv/issues/14092) @ [金星の上](https://github.com/overvenus)間のトラフィックが高すぎる問題を修正
        -   プルベースのシンクが有効な場合のCPU使用率、メモリ制御、スループットに関するTiCDCのパフォーマンスの問題を修正[＃8142](https://github.com/pingcap/tiflow/issues/8142) [＃8157](https://github.com/pingcap/tiflow/issues/8157) [＃8001](https://github.com/pingcap/tiflow/issues/8001) [＃5928](https://github.com/pingcap/tiflow/issues/5928) @ [ヒック](https://github.com/hicqu) @ [ハイラスティン](https://github.com/Rustin170506)

    -   TiDB データ移行 (DM)

        -   `binlog-schema delete`コマンドが[＃7373](https://github.com/pingcap/tiflow/issues/7373) @ [りゅうめんぎゃ](https://github.com/liumengya94)の実行に失敗する問題を修正
        -   最後のbinlogがスキップされた DDL [＃8175](https://github.com/pingcap/tiflow/issues/8175) @ [D3ハンター](https://github.com/D3Hunter)の場合にチェックポイントが進まない問題を修正しました
        -   1 つのテーブルに「更新」と「非更新」の両方のタイプの式フィルターが指定されている場合、すべての`UPDATE`ステートメントがスキップされるバグを修正しました[＃7831](https://github.com/pingcap/tiflow/issues/7831) @ [ランス6716](https://github.com/lance6716)
        -   テーブルに`update-old-value-expr`または`update-new-value-expr`のいずれか一方のみが設定されている場合に、フィルタ ルールが有効にならないか、DM が[＃7774](https://github.com/pingcap/tiflow/issues/7774) @ [ランス6716](https://github.com/lance6716)パニックになるというバグを修正しました。

    -   TiDB Lightning

        -   一部のシナリオで TiDB の再起動によりTiDB Lightningタイムアウトがハングする問題を修正[＃33714](https://github.com/pingcap/tidb/issues/33714) @ [リチュンジュ](https://github.com/lichunzhu)
        -   並列インポート中に最後のTiDB Lightningインスタンスを除くすべてのインスタンスでローカル重複レコードが検出された場合、 TiDB Lightning が競合解決を誤ってスキップする可能性がある問題を修正[＃40923](https://github.com/pingcap/tidb/issues/40923) @ [リチュンジュ](https://github.com/lichunzhu)
        -   事前チェックがターゲット クラスター[＃41040](https://github.com/pingcap/tidb/issues/41040) @ [ランス6716](https://github.com/lance6716)で実行中の TiCDC の存在を正確に検出できない問題を修正しました。
        -   TiDB Lightningが分割領域フェーズ[＃40934](https://github.com/pingcap/tidb/issues/40934) @ [ランス6716](https://github.com/lance6716)でパニックになる問題を修正
        -   競合解決ロジック（ `duplicate-resolution` ）によりチェックサム[＃40657](https://github.com/pingcap/tidb/issues/40657) @ [眠いモグラ](https://github.com/sleepymole)の不一致が発生する可能性がある問題を修正
        -   データファイル[#40400](https://github.com/pingcap/tidb/issues/40400) @ [ブチュイトウデゴウ](https://github.com/buchuitoudegou)に閉じられていない区切り文字がある場合に発生する可能性のある OOM 問題を修正しました。
        -   エラーレポートのファイルオフセットがファイルサイズ[#40034](https://github.com/pingcap/tidb/issues/40034) @ [ブチュイトウデゴウ](https://github.com/buchuitoudegou)を超える問題を修正
        -   PDClient の新バージョンで並列インポートが失敗する可能性がある問題を修正[＃40493](https://github.com/pingcap/tidb/issues/40493) @ [アメーバ原生動物](https://github.com/AmoebaProtozoa)
        -   TiDB Lightning の事前チェックで、以前に失敗したインポートによって残されたダーティ データを見つけられない問題を修正[＃39477](https://github.com/pingcap/tidb/issues/39477) @ [ダシュン](https://github.com/dsdashun)

## 寄稿者 {#contributors}

TiDB コミュニティの以下の貢献者に感謝いたします。

-   [モルゴ](https://github.com/morgo)
-   [ジフハウス](https://github.com/jiyfhust)
-   [b41sh](https://github.com/b41sh)
-   [ソースリウ](https://github.com/sourcelliu)
-   [歌zhibin97](https://github.com/songzhibin97)
-   [マミル](https://github.com/mamil)
-   [ドゥージール9](https://github.com/Dousir9)
-   [ヒヒフフ](https://github.com/hihihuhu)
-   [マイコキシン](https://github.com/mychoxin)
-   [翻訳者](https://github.com/xuning97)
-   [アンドレイドDB](https://github.com/andreid-db)
