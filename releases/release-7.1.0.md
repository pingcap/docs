---
title: TiDB 7.1.0 Release Notes
summary: TiDB 7.1.0 の新機能、互換性の変更、改善、バグ修正について説明します。
---

# TiDB 7.1.0 リリースノート {#tidb-7-1-0-release-notes}

発売日: 2023年5月31日

TiDB バージョン: 7.1.0

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v7.1/quick-start-with-tidb) | [実稼働環境への導入](https://docs.pingcap.com/tidb/v7.1/production-deployment-using-tiup)

TiDB 7.1.0 は長期サポートリリース (LTS) です。

以前の LTS 6.5.0 と比較して、7.1.0 には、 [6.6.0-DMR](/releases/release-6.6.0.md) 、 [7.0.0-DMR](/releases/release-7.0.0.md)でリリースされた新機能、改善、バグ修正が含まれているだけでなく、次の主要な機能と改善も導入されています。

<table><thead><tr><th>カテゴリ</th><th>特徴</th><th>説明</th></tr></thead><tbody><tr><td rowspan="4">スケーラビリティとパフォーマンス</td><td>TiFlash は<a href="https://docs.pingcap.com/tidb/v7.1/tiflash-disaggregated-and-s3" target="_blank">、分散storageとコンピューティングアーキテクチャ、および S3 共有storage</a>(実験的、v7.0.0 で導入) をサポートします。</td><td> TiFlash は、オプションとしてクラウドネイティブアーキテクチャを導入します。<ul><li> TiFlash のコンピューティングとstorageを分離します。これは、弾力的な HTAP リソース利用のマイルストーンです。</li><li>低コストで共有storageを提供できる S3 ベースのstorageエンジンを導入します。</li></ul></td></tr><tr><td> TiKV は<a href="https://docs.pingcap.com/tidb/v7.1/system-variables#tidb_store_batch_size" target="_blank">バッチ集約データ要求</a>をサポートします (v6.6.0 で導入)</td><td>この機能強化により、TiKV バッチ取得操作での合計 RPC が大幅に削減されます。データが高度に分散され、gRPC スレッド プールのリソースが不足している状況では、コプロセッサ要求をバッチ処理すると、パフォーマンスが 50% 以上向上する可能性があります。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v7.1/troubleshoot-hot-spot-issues#scatter-read-hotspots" target="_blank">負荷ベースのレプリカ読み取り</a></td><td>読み取りホットスポットのシナリオでは、TiDB はホットスポット TiKV ノードの読み取り要求をそのレプリカにリダイレクトできます。この機能により、読み取りホットスポットが効率的に分散され、クラスター リソースの使用が最適化されます。負荷ベースのレプリカ読み取りをトリガーするためのしきい値を制御するには、システム変数<a href="https://docs.pingcap.com/tidb/v7.1/system-variables#tidb_load_based_replica_read_threshold-new-in-v700" target="_blank"><code>tidb_load_based_replica_read_threshold</code></a>を調整します。</td></tr><tr><td> TiKV は<a href="https://docs.pingcap.com/tidb/v7.1/partitioned-raft-kv" target="_blank">パーティション化されたRaft KVstorageエンジン</a>をサポートします (実験的)</td><td> TiKV は、パーティション化されたRaft KV という新世代のstorageエンジンを導入します。各データリージョンに専用の RocksDB インスタンスを持たせることで、クラスターのstorage容量を TB レベルから PB レベルに拡張し、より安定した書き込みレイテンシーと強力なスケーラビリティを実現できます。</td></tr><tr><td rowspan="2">信頼性と可用性</td><td><a href="https://docs.pingcap.com/tidb/v7.1/tidb-resource-control" target="_blank">リソース グループによるリソース制御</a>(GA)</td><td>リソース グループに基づくリソース管理をサポートします。これにより、同じクラスター内の異なるワークロードにリソースを割り当てて分離します。この機能により、マルチアプリケーション クラスターの安定性が大幅に向上し、マルチテナントの基盤が築かれます。v7.1.0 では、この機能により、実際のワークロードまたはハードウェアの展開に基づいてシステム容量を見積もる機能が導入されています。</td></tr><tr><td> TiFlash は<a href="https://docs.pingcap.com/tidb/v7.1/tiflash-spill-disk" target="_blank">ディスクへの書き込み</a>をサポートします (v7.0.0 で導入)</td><td> TiFlash は、集約、ソート、ハッシュ結合などのデータ集約型操作における OOM を軽減するために、ディスクへの中間結果のスピルをサポートします。</td></tr><tr><td rowspan="3">構文</td><td><a href="https://docs.pingcap.com/tidb/v7.1/sql-statement-create-index#multi-valued-indexes" target="_blank">多値インデックス</a>(GA)</td><td> MySQL 互換の複数値インデックスをサポートし、JSON タイプを拡張して MySQL 8.0 との互換性を向上させます。この機能により、複数値列のメンバーシップ チェックの効率が向上します。</td></tr><tr><td><a href="https://docs.pingcap.com/tidb/v7.1/time-to-live" target="_blank">行レベルの TTL</a> (v7.0.0 で GA)</td><td>一定の期間が経過したデータを自動的に期限切れにすることで、データベース サイズの管理をサポートし、パフォーマンスを向上します。</td></tr><tr><td><a href="https://docs.pingcap.com/tidb/v7.1/generated-columns" target="_blank">生成された列</a>(GA)</td><td>生成された列の値は、列定義の SQL 式によってリアルタイムで計算されます。この機能により、一部のアプリケーション ロジックがデータベース レベルにプッシュされ、クエリの効率が向上します。</td></tr><tr><td rowspan="2">Security</td><td><a href="https://docs.pingcap.com/tidb/v7.1/security-compatibility-with-mysql" target="_blank">LDAP認証</a></td><td>TiDB は、 <a href="https://dev.mysql.com/doc/refman/8.0/en/ldap-pluggable-authentication.html" target="_blank">MySQL 8.0</a>と互換性のある LDAP 認証をサポートしています。</td></tr><tr><td> <a href="https://static.pingcap.com/files/2023/09/18204824/TiDB-Database-Auditing-User-Guide1.pdf" target="_blank">監査ログの強化</a>（<a href="https://www.pingcap.com/tidb-enterprise" target="_blank">エンタープライズ エディション</a>のみ）</td><td> TiDB Enterprise Edition は、データベース監査機能を強化します。よりきめ細かいイベント フィルタリング制御、よりユーザー フレンドリなフィルタ設定、JSON での新しいファイル出力形式、監査ログのライフサイクル管理を提供することで、システム監査機能が大幅に向上します。</td></tr></tbody></table>

## 機能の詳細 {#feature-details}

### パフォーマンス {#performance}

-   パーティション化されたRaft KVstorageエンジンを強化する (実験的) [＃11515](https://github.com/tikv/tikv/issues/11515) [＃12842](https://github.com/tikv/tikv/issues/12842) @ [忙しいカケス](https://github.com/busyjay) @ [トニー](https://github.com/tonyxuqqi) @ [タボキ](https://github.com/tabokie) @ [バッファフライ](https://github.com/bufferflies) @ [5kbpsの](https://github.com/5kbpers) @ [スペードA-タン](https://github.com/SpadeA-Tang) @ [ノルーシュ](https://github.com/nolouch)

    TiDB v6.6.0 では、実験的機能として Partitioned Raft KVstorageエンジンが導入されました。このstorageエンジンは、複数の RocksDB インスタンスを使用して TiKVリージョンデータを保存し、各リージョンのデータは独立した RocksDB インスタンスに保存されます。新しいストレージ エンジンは、RocksDB インスタンス内のファイルの数とレベルをより適切に制御し、リージョン間のデータ操作の物理的な分離を実現し、より多くのデータを安定して管理することをサポートします。元の TiKVstorageエンジンと比較して、Partitioned Raft KVstorageエンジンを使用すると、同じハードウェア条件と読み取りと書き込みの混在シナリオで、書き込みスループットが約 2 倍になり、エラスティック スケーリング時間が約 4/5 短縮されます。

    TiDB v7.1.0 では、Partitioned Raft KVstorageエンジンがTiDB Lightning、 BR、TiCDC などのツールをサポートしています。

    現在、この機能は実験的であり、本番環境での使用は推奨されません。このエンジンは新しく作成されたクラスターでのみ使用でき、元の TiKVstorageエンジンから直接アップグレードすることはできません。

    詳細については[ドキュメント](/partitioned-raft-kv.md)参照してください。

-   TiFlash は遅延マテリアライゼーション (GA) [＃5829](https://github.com/pingcap/tiflash/issues/5829) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)をサポートします

    v7.0.0 では、クエリ パフォーマンスを最適化するための実験的機能として、 TiFlashに遅延マテリアライゼーションが導入されました。この機能は、デフォルトでは無効になっています ( [`tidb_opt_enable_late_materialization`](/system-variables.md#tidb_opt_enable_late_materialization-new-in-v700)システム変数はデフォルトで`OFF`に設定されます)。フィルター条件 ( `WHERE`句) を含む`SELECT`ステートメントを処理する場合、 TiFlash はクエリに必要な列からすべてのデータを読み取り、クエリ条件に基づいてデータをフィルター処理して集計します。遅延マテリアライゼーションを有効にすると、TiDB はフィルター条件の一部を TableScan 演算子にプッシュダウンすることをサポートします。つまり、 TiFlash は最初に TableScan 演算子にプッシュダウンされたフィルター条件に関連する列データをスキャンし、条件を満たす行をフィルター処理してから、これらの行の他の列データをスキャンしてさらに計算するため、IO スキャンとデータ処理の計算が削減されます。

    v7.1.0 以降、 TiFlash の遅延マテリアライゼーション機能が一般に利用可能になり、デフォルトで有効になっています ( [`tidb_opt_enable_late_materialization`](/system-variables.md#tidb_opt_enable_late_materialization-new-in-v700)システム変数はデフォルトで`ON`に設定されます)。TiDB オプティマイザーは、クエリの統計とフィルター条件に基づいて、どのフィルターを TableScan オペレーターにプッシュダウンするかを決定します。

    詳細については[ドキュメント](/tiflash/tiflash-late-materialization.md)参照してください。

-   TiFlashは、ネットワーク伝送のオーバーヘッドに応じてMPP Joinアルゴリズムを自動的に選択することをサポートしています[＃7084](https://github.com/pingcap/tiflash/issues/7084) @ [ソロッツ](https://github.com/solotzg)

    TiFlash MPP モードは複数の結合アルゴリズムをサポートします。v7.1.0 より前では、TiDB は[`tidb_broadcast_join_threshold_count`](/system-variables.md#tidb_broadcast_join_threshold_count-new-in-v50)番目と[`tidb_broadcast_join_threshold_size`](/system-variables.md#tidb_broadcast_join_threshold_size-new-in-v50)の変数と実際のデータ量に基づいて、MPP モードでブロードキャスト ハッシュ結合アルゴリズムを使用するかどうかを決定します。

    v7.1.0 では、TiDB は[`tidb_prefer_broadcast_join_by_exchange_data_size`](/system-variables.md#tidb_prefer_broadcast_join_by_exchange_data_size-new-in-v710)変数を導入しました。これは、ネットワーク伝送の最小オーバーヘッドに基づいて MPP Join アルゴリズムを選択するかどうかを制御します。この変数はデフォルトで無効になっており、デフォルトのアルゴリズム選択方法は v7.1.0 以前と同じであることを示しています。変数を`ON`に設定すると有効になります。有効にすると、 [`tidb_broadcast_join_threshold_count`](/system-variables.md#tidb_broadcast_join_threshold_count-new-in-v50)と[`tidb_broadcast_join_threshold_size`](/system-variables.md#tidb_broadcast_join_threshold_size-new-in-v50)変数を手動で調整する必要がなくなり (この時点では両方の変数は有効になりません)、TiDB は異なる Join アルゴリズムによるネットワーク伝送のしきい値を自動的に推定し、全体的なオーバーヘッドが最小のアルゴリズムを選択するため、ネットワーク トラフィックが削減され、MPP クエリのパフォーマンスが向上します。

    詳細については[ドキュメント](/tiflash/use-tiflash-mpp-mode.md#algorithm-support-for-the-mpp-mode)参照してください。

-   読み取りホットスポットを軽減するために負荷ベースのレプリカ読み取りをサポートする[＃14151](https://github.com/tikv/tikv/issues/14151) @ [スティクナーフ](https://github.com/sticnarf) @ [あなた06](https://github.com/you06)

    読み取りホットスポットのシナリオでは、ホットスポット TiKV ノードは読み取り要求を時間内に処理できず、読み取り要求がキューイングされます。ただし、この時点ですべての TiKV リソースが使い果たされるわけではありません。レイテンシーを削減するために、TiDB v7.1.0 では負荷ベースのレプリカ読み取り機能が導入され、これにより、TiDB はホットスポット TiKV ノードでキューイングすることなく、他の TiKV ノードからデータを読み取ることができます。読み取り要求のキューの長さは、 [`tidb_load_based_replica_read_threshold`](/system-variables.md#tidb_load_based_replica_read_threshold-new-in-v700)システム変数を使用して制御できます。リーダー ノードの推定キュー時間がこのしきい値を超えると、TiDB はフォロワー ノードからのデータの読み取りを優先します。この機能により、読み取りホットスポットを分散させない場合と比較して、読み取りホットスポットのシナリオで読み取りスループットが 70% ～ 200% 向上します。

    詳細については[ドキュメント](/troubleshoot-hot-spot-issues.md#scatter-read-hotspots)参照してください。

-   非準備済みステートメントの実行プランをキャッシュする機能の強化 (実験的) [＃36598](https://github.com/pingcap/tidb/issues/36598) @ [qw4990](https://github.com/qw4990)

    TiDB v7.0.0 では、同時実行 OLTP の負荷容量を向上させるための実験的機能として、準備されていないプラン キャッシュが導入されています。v7.1.0 では、TiDB はこの機能を強化し、より多くの SQL ステートメントのキャッシュをサポートします。

    メモリ使用率を向上させるために、TiDB v7.1.0 では、準備されていないプラン キャッシュと準備されたプラン キャッシュのキャッシュ プールが統合されます。システム変数[`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-new-in-v710)を使用してキャッシュ サイズを制御できます。システム変数[`tidb_prepared_plan_cache_size`](/system-variables.md#tidb_prepared_plan_cache_size-new-in-v610)と[`tidb_non_prepared_plan_cache_size`](/system-variables.md#tidb_non_prepared_plan_cache_size)非推奨です。

    前方互換性を維持するために、以前のバージョンから v7.1.0 以降のバージョンにアップグレードする場合、キャッシュ サイズ`tidb_session_plan_cache_size`は`tidb_prepared_plan_cache_size`と同じ値のままになり、 [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache)アップグレード前の設定のままになります。十分なパフォーマンス テストを行った後、 `tidb_enable_non_prepared_plan_cache`使用して、準備されていないプラン キャッシュを有効にすることができます。新しく作成されたクラスターでは、準備されていないプラン キャッシュはデフォルトで有効になっています。

    準備されていないプラン キャッシュは、デフォルトでは DML ステートメントをサポートしません。この制限を削除するには、 [`tidb_enable_non_prepared_plan_cache_for_dml`](/system-variables.md#tidb_enable_non_prepared_plan_cache_for_dml-new-in-v710)システム変数を`ON`に設定します。

    詳細については[ドキュメント](/sql-non-prepared-plan-cache.md)参照してください。

-   TiDB 分散実行フレームワーク (DXF) のサポート (実験的) [＃41495](https://github.com/pingcap/tidb/issues/41495) @ [ベンジャミン2037](https://github.com/benjamin2037)

    TiDB v7.1.0 より前では、1 つの TiDB ノードのみが DDL 所有者として機能し、同時に DDL タスクを実行できました。TiDB v7.1.0 以降の新しい DXF では、複数の TiDB ノードが同じ DDL タスクを並行して実行できるため、TiDB クラスターのリソースをより有効に活用し、DDL のパフォーマンスを大幅に向上できます。さらに、TiDB ノードを追加することで、DDL のパフォーマンスを直線的に向上させることができます。この機能は現在実験的であり、 `ADD INDEX`操作のみをサポートしていることに注意してください。

    DXFを使用するには、 [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710)の値を`ON`に設定します。

    ```sql
    SET GLOBAL tidb_enable_dist_task = ON;
    ```

    詳細については[ドキュメント](/tidb-distributed-execution-framework.md)参照してください。

### 信頼性 {#reliability}

-   リソース コントロールが一般提供 (GA) される[＃38825](https://github.com/pingcap/tidb/issues/38825) @ [ノルーシュ](https://github.com/nolouch) @ [ボーンチェンジャー](https://github.com/BornChanger) @ [栄光](https://github.com/glorv) @ [天菜まお](https://github.com/tiancaiamao) @ [コナー1996](https://github.com/Connor1996) @ [じゃがいも](https://github.com/JmPotato) @ [ネス](https://github.com/hnes) @ [キャビンフィーバーB](https://github.com/CabinfeverB) @ [ヒューシャープ](https://github.com/HuSharp)

    TiDB は、リソース グループに基づくリソース制御機能を強化し、v7.1.0 で GA になりました。この機能により、TiDB クラスターのリソース利用効率とパフォーマンスが大幅に向上します。リソース制御機能の導入は、TiDB にとって画期的な出来事です。分散データベース クラスターを複数の論理ユニットに分割し、異なるデータベース ユーザーを対応するリソース グループにマップし、必要に応じて各リソース グループのクォータを設定できます。クラスター リソースが制限されている場合、同じリソース グループ内のセッションで使用されるすべてのリソースはクォータに制限されます。このように、リソース グループが過剰に消費されても、他のリソース グループのセッションには影響しません。

    この機能により、異なるシステムの複数の中小規模のアプリケーションを 1 つの TiDB クラスターに統合できます。アプリケーションのワークロードが大きくなっても、他のアプリケーションの正常な動作には影響しません。システムのワークロードが低い場合は、設定されたクォータを超えても、ビジー状態のアプリケーションに必要なシステム リソースを割り当てることができるため、リソースを最大限に活用できます。さらに、リソース制御機能を合理的に使用すると、クラスターの数を減らし、運用と保守の難しさを軽減し、管理コストを節約できます。

    TiDB v7.1.0 では、この機能により、実際のワークロードまたはハードウェアの展開に基づいてシステム容量を見積もる機能が導入されています。この見積機能により、容量計画のより正確な参照が提供され、エンタープライズ レベルのシナリオの安定性のニーズを満たすために TiDB リソース割り当てをより適切に管理できるようになります。

    ユーザー エクスペリエンスを向上させるために、TiDB ダッシュボードは[リソース マネージャー ページ](/dashboard/dashboard-resource-manager.md)提供します。このページでリソース グループの構成を表示し、クラスターの容量を視覚的に見積もって、適切なリソース割り当てを容易にすることができます。

    詳細については[ドキュメント](/tidb-resource-control.md)参照してください。

-   高速オンラインDDLのチェックポイントメカニズムをサポートし、フォールトトレランスと自動リカバリ機能を向上させます[＃42164](https://github.com/pingcap/tidb/issues/42164) @ [タンジェンタ](https://github.com/tangenta)

    TiDB v7.1.0 では、 [高速オンラインDDL](/ddl-introduction.md)のチェックポイント メカニズムが導入され、Fast Online DDL のフォールト トレランスと自動リカバリ機能が大幅に向上しました。障害により TiDB 所有者ノードが再起動または変更された場合でも、TiDB は定期的に自動更新されるチェックポイントから進行状況を回復できるため、DDL 実行の安定性と効率が向上します。

    詳細については[ドキュメント](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)参照してください。

-   バックアップと復元はチェックポイント復元[＃42339](https://github.com/pingcap/tidb/issues/42339) @ [リーヴルス](https://github.com/Leavrth)をサポートします

    スナップショットの復元やログの復元は、ディスクの枯渇やノードのクラッシュなどの回復可能なエラーにより中断される可能性があります。TiDB v7.1.0 より前では、エラーに対処した後でも中断前の復元の進行状況は無効になり、復元を最初からやり直す必要がありました。大規模なクラスターの場合、これにはかなりの追加コストがかかります。

    TiDB v7.1.0 以降、バックアップと復元 (BR) にチェックポイント復元機能が導入され、中断された復元を続行できるようになりました。この機能により、中断された復元の回復の進行状況のほとんどを保持できます。

    詳細については[ドキュメント](/br/br-checkpoint-restore.md)参照してください。

-   統計[＃42160](https://github.com/pingcap/tidb/issues/42160) @ [翻訳者](https://github.com/xuyifangreeneyes)のロード戦略を最適化する

    TiDB v7.1.0 では、軽量統計初期化が実験的機能として導入されています。軽量統計初期化により、起動時にロードする必要がある統計の数が大幅に削減され、統計のロード速度が向上します。この機能により、複雑なランタイム環境での TiDB の安定性が向上し、TiDB ノードの再起動時にサービス全体に与える影響が軽減されます。この機能を有効にするには、パラメータ[`lite-init-stats`](/tidb-configuration-file.md#lite-init-stats-new-in-v710)から`true`に設定できます。

    TiDB の起動時に、初期統計が完全にロードされる前に実行される SQL 文の実行プランが最適ではない場合があり、パフォーマンスの問題が発生します。このような問題を回避するために、TiDB v7.1.0 では構成パラメータ[`force-init-stats`](/tidb-configuration-file.md#force-init-stats-new-in-v657-and-v710)が導入されています。このオプションを使用すると、起動時に統計の初期化が完了した後にのみ TiDB がサービスを提供するかどうかを制御できます。このパラメータはデフォルトでは無効になっています。

    詳細については[ドキュメント](/statistics.md#load-statistics)参照してください。

-   TiCDCは、単一行データのデータ整合性検証機能をサポートしています[＃8718](https://github.com/pingcap/tiflow/issues/8718) [＃42747](https://github.com/pingcap/tidb/issues/42747) @ [3エースショーハンド](https://github.com/3AceShowHand) @ [ジグアン](https://github.com/zyguan)

    v7.1.0 以降、TiCDC では、チェックサム アルゴリズムを使用して単一行データの整合性を検証するデータ整合性検証機能が導入されています。この機能は、TiDB からデータを書き込み、それを TiCDC 経由で複製し、それを Kafka クラスターに書き込むプロセスでエラーが発生していないかどうかを確認するのに役立ちます。データ整合性検証機能は、Kafka をダウンストリームとして使用する変更フィードのみをサポートし、現在は Avro プロトコルをサポートしています。

    詳細については[ドキュメント](/ticdc/ticdc-integrity-check.md)参照してください。

-   TiCDCはDDLレプリケーション操作[＃8686](https://github.com/pingcap/tiflow/issues/8686) @ [ハイラスティン](https://github.com/Rustin170506)を最適化します

    v7.1.0 より前では、大きなテーブルのすべての行に影響する DDL 操作 (列の追加や削除など) を実行すると、TiCDC のレプリケーションレイテンシーが大幅に増加していました。v7.1.0 以降、TiCDC はこのレプリケーション操作を最適化し、DDL 操作によるダウンストリームレイテンシーへの影響を軽減します。

    詳細については[ドキュメント](/ticdc/ticdc-faq.md#does-ticdc-replicate-data-changes-caused-by-lossy-ddl-operations-to-the-downstream)参照してください。

-   TiB レベルのデータをインポートする際のTiDB Lightningの安定性を向上[＃43510](https://github.com/pingcap/tidb/issues/43510) [＃43657](https://github.com/pingcap/tidb/issues/43657) @ [D3ハンター](https://github.com/D3Hunter) @ [ランス6716](https://github.com/lance6716)

    v7.1.0 以降、 TiDB Lightning には、TiB レベルのデータをインポートする際の安定性を向上させるための 4 つの構成項目が追加されました。

    -   `tikv-importer.region-split-batch-size` 、バッチでリージョンを分割するときのリージョンの数を制御します。デフォルト値は`4096`です。
    -   `tikv-importer.region-split-concurrency` 、リージョンを分割する際の同時実行性を制御します。デフォルト値は CPU コアの数です。
    -   `tikv-importer.region-check-backoff-limit`分割および分散操作後にリージョンがオンラインになるまで待機する再試行回数を制御します。デフォルト値は`1800`で、最大再試行間隔は 2 秒です。再試行の間にいずれかのリージョンがオンラインになった場合、再試行回数は増加しません。
    -   `tikv-importer.pause-pd-scheduler-scope` TiDB Lightning がPD スケジューリングを一時停止する範囲を制御します。値のオプションは`"table"`と`"global"`です。デフォルト値は`"table"`です。v6.1.0 より前のバージョンの TiDB では、データのインポート中にグローバル スケジューリングを一時停止する`"global"`オプションのみを設定できます。v6.1.0 以降では、ターゲット テーブル データを格納するリージョンに対してのみスケジューリングが一時停止される`"table"`オプションがサポートされています。データ量が多いシナリオでは、安定性を向上させるために、この設定項目を`"global"`に設定することをお勧めします。

    詳細については[ドキュメント](/tidb-lightning/tidb-lightning-configuration.md)参照してください。

### 構文 {#sql}

-   `INSERT INTO SELECT`ステートメントを使用したTiFlashクエリ結果の保存をサポート (GA) [＃37515](https://github.com/pingcap/tidb/issues/37515) @ [ゲンリキ](https://github.com/gengliqi)

    v6.5.0 以降、TiDB は`INSERT INTO SELECT`ステートメントの`SELECT`句 (分析クエリ) をTiFlashにプッシュダウンすることをサポートしています。これにより、 TiFlashクエリ結果を`INSERT INTO`で指定された TiDB テーブルに簡単に保存してさらに分析することができ、結果のキャッシュ (つまり、結果のマテリアライゼーション) として機能します。

    v7.1.0 では、この機能が一般に提供されています。 `INSERT INTO SELECT`ステートメントの`SELECT`句の実行中に、オプティマイザーは、 [SQL モード](/sql-mode.md)とTiFlashレプリカのコスト見積もりに基づいて、クエリをTiFlashにプッシュダウンするかどうかをインテリジェントに決定できます。したがって、実験的フェーズで導入された`tidb_enable_tiflash_read_for_write_stmt`システム変数は非推奨になりましたTiFlashの`INSERT INTO SELECT`ステートメントの計算ルールは`STRICT SQL Mode`要件を満たしていないため、TiDB では、現在のセッションの[SQL モード](/sql-mode.md)が厳密でない場合にのみ、 `INSERT INTO SELECT`ステートメントの`SELECT`句をTiFlashにプッシュダウンできます。つまり、 `sql_mode`値に`STRICT_TRANS_TABLES`と`STRICT_ALL_TABLES`含まれません。

    詳細については[ドキュメント](/tiflash/tiflash-results-materialization.md)参照してください。

-   MySQL 互換のマルチ値インデックスが一般提供 (GA) される[＃39592](https://github.com/pingcap/tidb/issues/39592) @ [雄吉偉](https://github.com/xiongjiwei) @ [qw4990](https://github.com/qw4990) @ [ヤンケオ](https://github.com/YangKeao)

    JSON 列の配列の値をフィルタリングすることは一般的な操作ですが、通常のインデックスではこのような操作を高速化することはできません。配列に複数値インデックスを作成すると、フィルタリングのパフォーマンスが大幅に向上します。JSON 列の配列に複数値インデックスがある場合は、複数値インデックスを使用して`MEMBER OF()` 、 `JSON_CONTAINS()` 、および`JSON_OVERLAPS()`関数で検索条件をフィルタリングできるため、I/O 消費が削減され、操作速度が向上します。

    v7.1.0 では、多値インデックス機能が一般提供 (GA) されます。より完全なデータ型をサポートし、TiDB ツールと互換性があります。多値インデックスを使用すると、本番環境での JSON 配列の検索操作を高速化できます。

    詳細については[ドキュメント](/sql-statements/sql-statement-create-index.md#multi-valued-indexes)参照してください。

-   ハッシュおよびキーパーティションテーブルのパーティション管理を改善する[＃42728](https://github.com/pingcap/tidb/issues/42728) @ [ミョンス](https://github.com/mjonss)

    v7.1.0 より前では、TiDB のハッシュおよびキー パーティション テーブルは、 `TRUNCATE PARTITION`パーティション管理ステートメントのみをサポートしています。v7.1.0 以降では、ハッシュおよびキー パーティション テーブルは、 `ADD PARTITION`および`COALESCE PARTITION`パーティション管理ステートメントもサポートします。したがって、必要に応じて、ハッシュおよびキー パーティション テーブルのパーティション数を柔軟に調整できます。たとえば、 `ADD PARTITION`ステートメントでパーティション数を増やしたり、 `COALESCE PARTITION`ステートメントでパーティション数を減らしたりすることができます。

    詳細については[ドキュメント](/partitioned-table.md#manage-hash-and-key-partitions)参照してください。

-   範囲INTERVALパーティションの構文が一般公開（GA） [＃35683](https://github.com/pingcap/tidb/issues/35683) @ [ミョンス](https://github.com/mjonss)になります

    Range INTERVAL パーティション分割 (v6.3.0 で導入) の構文が GA になりました。この構文を使用すると、すべてのパーティションを列挙せずに、必要な間隔で Range パーティション分割を定義できるため、Range パーティション分割の DDL ステートメントの長さが大幅に短縮されます。この構文は、元の範囲パーティション分割の構文と同じです。

    詳細については[ドキュメント](/partitioned-table.md#range-interval-partitioning)参照してください。

-   生成された列は[bb7133](https://github.com/bb7133)で一般公開 (GA) されます

    生成された列は、データベースにとって貴重な機能です。テーブルを作成するときに、列の値が、ユーザーによって明示的に挿入または更新されるのではなく、テーブル内の他の列の値に基づいて計算されるように定義できます。この生成された列は、仮想列または保存された列のいずれかになります。TiDB は以前のバージョンから MySQL 互換の生成列をサポートしており、この機能は v7.1.0 で GA になります。

    生成された列を使用すると、TiDB の MySQL 互換性が向上し、MySQL からの移行プロセスが簡素化されます。また、データ保守の複雑さが軽減され、データの一貫性とクエリの効率が向上します。

    詳細については[ドキュメント](/generated-columns.md)参照してください。

### DB操作 {#db-operations}

-   DDL 操作を手動でキャンセルせずに、スムーズなクラスタ アップグレードをサポート (実験的) [＃39751](https://github.com/pingcap/tidb/issues/39751) @ [ジムララ](https://github.com/zimulala)

    TiDB v7.1.0 より前のバージョンでは、クラスターをアップグレードするには、アップグレード前に実行中またはキューに入れられた DDL タスクを手動でキャンセルし、アップグレード後に再度追加する必要があります。

    よりスムーズなアップグレード エクスペリエンスを提供するために、TiDB v7.1.0 では DDL タスクの自動一時停止と再開がサポートされています。v7.1.0 以降では、事前に DDL タスクを手動でキャンセルしなくてもクラスターをアップグレードできます。TiDB はアップグレード前に実行中またはキューに入れられたユーザー DDL タスクを自動的に一時停止し、ローリング アップグレード後にこれらのタスクを再開するため、TiDB クラスターのアップグレードが容易になります。

    詳細については[ドキュメント](/smooth-upgrade-tidb.md)参照してください。

### 可観測性 {#observability}

-   オプティマイザ診断情報の強化[＃43122](https://github.com/pingcap/tidb/issues/43122) @ [時間と運命](https://github.com/time-and-fate)

    十分な情報を取得することが、SQL パフォーマンス診断の鍵となります。v7.1.0 では、TiDB はさまざまな診断ツールにオプティマイザー ランタイム情報を引き続き追加し、実行プランの選択方法に関するより詳細な情報を提供し、SQL パフォーマンスの問題のトラブルシューティングを支援します。新しい情報には次のものが含まれます。

    -   [`PLAN REPLAYER`](/sql-plan-replayer.md)の出力は`debug_trace.json` 。
    -   [`EXPLAIN`](/explain-walkthrough.md)の出力における`operator info`の部分的な統計詳細。
    -   [遅いクエリ](/identify-slow-queries.md)の`Stats`フィールドの部分的な統計詳細。

    詳細については、 [`PLAN REPLAYER`使用してクラスターの現場情報を保存および復元します](/sql-plan-replayer.md) 、 [`EXPLAIN`ウォークスルー](/explain-walkthrough.md) 、 [遅いクエリを特定する](/identify-slow-queries.md)を参照してください。

### Security {#security}

-   TiFlashシステムテーブル情報のクエリに使用するインターフェイスを置き換えます[＃6941](https://github.com/pingcap/tiflash/issues/6941) @ [フロービーハッピー](https://github.com/flowbehappy)

    v7.1.0 以降、TiDB の[`INFORMATION_SCHEMA.TIFLASH_TABLES`](/information-schema/information-schema-tiflash-tables.md)および[`INFORMATION_SCHEMA.TIFLASH_SEGMENTS`](/information-schema/information-schema-tiflash-segments.md)システム テーブルのクエリ サービスを提供するときに、 TiFlash はHTTP ポートではなく gRPC ポートを使用するため、HTTP サービスのセキュリティ リスクを回避できます。

-   LDAP認証[＃43580](https://github.com/pingcap/tidb/issues/43580) @ [ヤンケオ](https://github.com/YangKeao)をサポート

    v7.1.0 以降、TiDB は LDAP 認証をサポートし、 `authentication_ldap_sasl`と`authentication_ldap_simple` 2 つの認証プラグインを提供します。

    詳細については[ドキュメント](/security-compatibility-with-mysql.md)参照してください。

-   データベース監査機能の強化 (Enterprise Edition)

    v7.1.0 では、TiDB Enterprise Edition のデータベース監査機能が強化され、その機能が大幅に拡張され、ユーザー エクスペリエンスが向上して、企業のデータベース セキュリティ コンプライアンスのニーズに対応できるようになりました。

    -   より詳細な監査イベント定義とよりきめ細かい監査設定のために、「フィルター」と「ルール」の概念を導入します。
    -   JSON 形式でのルールの定義をサポートし、よりユーザーフレンドリーな構成方法を提供します。
    -   自動ログローテーションとスペース管理関数を追加し、保持時間とログサイズの 2 つの次元でのログローテーションの構成をサポートします。
    -   監査ログをTEXT形式と JSON 形式の両方で出力できるようにサポートし、サードパーティ ツールとの統合を容易にします。
    -   監査ログの編集をサポートします。すべてのリテラルを置き換えてセキュリティを強化できます。

    データベース監査は、TiDB Enterprise Edition の重要な機能です。この機能は、企業がデータのセキュリティとコンプライアンスを確保するための強力な監視および監査ツールを提供します。企業の管理者は、データベース操作のソースと影響を追跡して、違法なデータの盗難や改ざんを防ぐことができます。さらに、データベース監査は、企業がさまざまな規制やコンプライアンスの要件を満たし、法的および倫理的コンプライアンスを確保するのにも役立ちます。この機能は、企業の情報セキュリティにとって重要なアプリケーション価値を持っています。

    詳細については、 [ユーザーガイド](https://static.pingcap.com/files/2023/09/18204824/TiDB-Database-Auditing-User-Guide1.pdf)参照してください。この機能は、TiDB Enterprise Edition に含まれています。この機能を使用するには、 [TiDBエンタープライズ](https://www.pingcap.com/tidb-enterprise)ページに移動して TiDB Enterprise Edition を入手してください。

## 互換性の変更 {#compatibility-changes}

> **注記：**
>
> このセクションでは、v7.0.0 から現在のバージョン (v7.1.0) にアップグレードするときに知っておく必要のある互換性の変更について説明します。v6.6.0 以前のバージョンから現在のバージョンにアップグレードする場合は、中間バージョンで導入された互換性の変更も確認する必要がある可能性があります。

### 行動の変化 {#behavior-changes}

-   セキュリティを向上させるため、 TiFlashはHTTPサービスポート（デフォルト`8123` ）を廃止し、代わりにgRPCポートを使用します。

    TiFlash をv7.1.0 にアップグレードした場合、TiDB を v7.1.0 にアップグレードする際に、TiDB はTiFlashシステム テーブル ( [`INFORMATION_SCHEMA.TIFLASH_TABLES`](/information-schema/information-schema-tiflash-tables.md)および[`INFORMATION_SCHEMA.TIFLASH_SEGMENTS`](/information-schema/information-schema-tiflash-segments.md) ) を読み取ることができません。

-   TiDB バージョン v6.2.0 から v7.0.0 のTiDB Lightning は、TiDB クラスターのバージョンに基づいてグローバル スケジューリングを一時停止するかどうかを決定します。TiDB クラスター バージョン &gt;= v6.1.0 の場合、スケジューリングはターゲット テーブル データを格納するリージョンに対してのみ一時停止され、ターゲット テーブルのインポートが完了すると再開されます。その他のバージョンの場合、 TiDB Lightning はグローバル スケジューリングを一時停止します。TiDB v7.1.0 以降では、 [`pause-pd-scheduler-scope`](/tidb-lightning/tidb-lightning-configuration.md)構成することで、グローバル スケジューリングを一時停止するかどうかを制御できます。デフォルトでは、 TiDB Lightning はターゲット テーブル データを格納するリージョンに対してスケジューリングを一時停止します。ターゲット クラスターのバージョンが v6.1.0 より前の場合、エラーが発生します。この場合、パラメータの値を`"global"`に変更して再試行できます。

-   TiDB v7.1.0 で[`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-cluster.md)使用すると、FLASHBACK 操作が完了した後も、一部の領域が FLASHBACK プロセスに残ることがあります。v7.1.0 ではこの機能を使用しないことをお勧めします。詳細については、問題[＃44292](https://github.com/pingcap/tidb/issues/44292)を参照してください。この問題が発生した場合は、 [TiDB スナップショットのバックアップと復元](/br/br-snapshot-guide.md)機能を使用してデータを復元できます。

### システム変数 {#system-variables}

| 変数名                                                                                                                                     | タイプを変更   | 説明                                                                                                                                                                                                                                                                                                                                                                                                |
| --------------------------------------------------------------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`tidb_enable_tiflash_read_for_write_stmt`](/system-variables.md#tidb_enable_tiflash_read_for_write_stmt-new-in-v630)                   | 非推奨      | デフォルト値を`OFF`から`ON`に変更します。 [`tidb_allow_mpp = ON`](/system-variables.md#tidb_allow_mpp-new-in-v50)の場合、オプティマイザは[SQL モード](/sql-mode.md)とTiFlashレプリカのコスト見積もりに基づいて、クエリをTiFlashにプッシュダウンするかどうかをインテリジェントに決定します。                                                                                                                                                                                           |
| [`tidb_non_prepared_plan_cache_size`](/system-variables.md#tidb_non_prepared_plan_cache_size)                                           | 非推奨      | v7.1.0 以降、このシステム変数は非推奨です。1 [`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-new-in-v710)使用して、キャッシュできるプランの最大数を制御できます。                                                                                                                                                                                                                                            |
| [`tidb_prepared_plan_cache_size`](/system-variables.md#tidb_prepared_plan_cache_size-new-in-v610)                                       | 非推奨      | v7.1.0 以降、このシステム変数は非推奨です。1 [`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-new-in-v710)使用して、キャッシュできるプランの最大数を制御できます。                                                                                                                                                                                                                                            |
| `tidb_ddl_distribute_reorg`                                                                                                             | 削除されました  | この変数の名前は[`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710)に変更されます。                                                                                                                                                                                                                                                                                                 |
| [`default_authentication_plugin`](/system-variables.md#default_authentication_plugin)                                                   | 修正済み     | 2 つの新しい値オプション`authentication_ldap_sasl`と`authentication_ldap_simple`が導入されました。                                                                                                                                                                                                                                                                                                                     |
| [`tidb_load_based_replica_read_threshold`](/system-variables.md#tidb_load_based_replica_read_threshold-new-in-v700)                     | 修正済み     | v7.1.0 から有効になり、負荷ベースのレプリカ読み取りをトリガーするためのしきい値を制御します。さらにテストを行った後、デフォルト値を`"0s"`から`"1s"`に変更します。                                                                                                                                                                                                                                                                                                        |
| [`tidb_opt_enable_late_materialization`](/system-variables.md#tidb_opt_enable_late_materialization-new-in-v700)                         | 修正済み     | デフォルト値を`OFF`から`ON`に変更します。これは、 TiFlash の遅延マテリアライゼーション機能がデフォルトで有効になっていることを意味します。                                                                                                                                                                                                                                                                                                                    |
| [`authentication_ldap_sasl_auth_method_name`](/system-variables.md#authentication_ldap_sasl_auth_method_name-new-in-v710)               | 新しく追加された | LDAP SASL 認証における認証方法名を指定します。                                                                                                                                                                                                                                                                                                                                                                      |
| [`authentication_ldap_sasl_bind_base_dn`](/system-variables.md#authentication_ldap_sasl_bind_base_dn-new-in-v710)                       | 新しく追加された | LDAP SASL 認証の検索ツリー内の検索範囲を制限します。ユーザーが`AS ...`句なしで作成された場合、TiDB はユーザー名に従って LDAPサーバーで`dn`を自動的に検索します。                                                                                                                                                                                                                                                                                                  |
| [`authentication_ldap_sasl_bind_root_dn`](/system-variables.md#authentication_ldap_sasl_bind_root_dn-new-in-v710)                       | 新しく追加された | LDAP SASL 認証でユーザーを検索するために LDAPサーバーにログインするために使用される`dn`指定します。                                                                                                                                                                                                                                                                                                                                       |
| [`authentication_ldap_sasl_bind_root_pwd`](/system-variables.md#authentication_ldap_sasl_bind_root_pwd-new-in-v710)                     | 新しく追加された | LDAP SASL 認証でユーザーを検索するために LDAPサーバーにログインするために使用されるパスワードを指定します。                                                                                                                                                                                                                                                                                                                                     |
| [`authentication_ldap_sasl_ca_path`](/system-variables.md#authentication_ldap_sasl_ca_path-new-in-v710)                                 | 新しく追加された | LDAP SASL 認証での StartTLS 接続用の証明機関ファイルの絶対パスを指定します。                                                                                                                                                                                                                                                                                                                                                  |
| [`authentication_ldap_sasl_init_pool_size`](/system-variables.md#authentication_ldap_sasl_init_pool_size-new-in-v710)                   | 新しく追加された | LDAP SASL 認証で LDAPサーバーへの接続プール内の初期接続を指定します。                                                                                                                                                                                                                                                                                                                                                        |
| [`authentication_ldap_sasl_max_pool_size`](/system-variables.md#authentication_ldap_sasl_max_pool_size-new-in-v710)                     | 新しく追加された | LDAP SASL 認証における LDAPサーバーへの接続プールの最大接続数を指定します。                                                                                                                                                                                                                                                                                                                                                     |
| [`authentication_ldap_sasl_server_host`](/system-variables.md#authentication_ldap_sasl_server_host-new-in-v710)                         | 新しく追加された | LDAP SASL 認証で LDAPサーバーホストを指定します。                                                                                                                                                                                                                                                                                                                                                                  |
| [`authentication_ldap_sasl_server_port`](/system-variables.md#authentication_ldap_sasl_server_port-new-in-v710)                         | 新しく追加された | LDAP SASL 認証における LDAPサーバーのTCP/IP ポート番号を指定します。                                                                                                                                                                                                                                                                                                                                                     |
| [`authentication_ldap_sasl_tls`](/system-variables.md#authentication_ldap_sasl_tls-new-in-v710)                                         | 新しく追加された | プラグインによる LDAPサーバーへの接続が LDAP SASL 認証で StartTLS を使用して保護されるかどうかを指定します。                                                                                                                                                                                                                                                                                                                               |
| [`authentication_ldap_simple_auth_method_name`](/system-variables.md#authentication_ldap_simple_auth_method_name-new-in-v710)           | 新しく追加された | LDAP シンプル認証における認証方法名を指定します。 `SIMPLE`のみをサポートします。                                                                                                                                                                                                                                                                                                                                                   |
| [`authentication_ldap_simple_bind_base_dn`](/system-variables.md#authentication_ldap_simple_bind_base_dn-new-in-v710)                   | 新しく追加された | LDAP シンプル認証の検索ツリー内の検索範囲を制限します。1 `AS ...`なしでユーザーが作成された場合、TiDB はユーザー名に従って LDAPサーバー内で`dn`を自動的に検索します。                                                                                                                                                                                                                                                                                                 |
| [`authentication_ldap_simple_bind_root_dn`](/system-variables.md#authentication_ldap_simple_bind_root_dn-new-in-v710)                   | 新しく追加された | LDAP 簡易認証でユーザーを検索するために LDAPサーバーにログインするために使用される`dn`指定します。                                                                                                                                                                                                                                                                                                                                          |
| [`authentication_ldap_simple_bind_root_pwd`](/system-variables.md#authentication_ldap_simple_bind_root_pwd-new-in-v710)                 | 新しく追加された | LDAP 簡易認証でユーザーを検索するために LDAPサーバーにログインするために使用されるパスワードを指定します。                                                                                                                                                                                                                                                                                                                                        |
| [`authentication_ldap_simple_ca_path`](/system-variables.md#authentication_ldap_simple_ca_path-new-in-v710)                             | 新しく追加された | LDAP 簡易認証での StartTLS 接続用の証明機関ファイルの絶対パスを指定します。                                                                                                                                                                                                                                                                                                                                                     |
| [`authentication_ldap_simple_init_pool_size`](/system-variables.md#authentication_ldap_simple_init_pool_size-new-in-v710)               | 新しく追加された | LDAP シンプル認証で、LDAPサーバーへの接続プール内の初期接続を指定します。                                                                                                                                                                                                                                                                                                                                                         |
| [`authentication_ldap_simple_max_pool_size`](/system-variables.md#authentication_ldap_simple_max_pool_size-new-in-v710)                 | 新しく追加された | LDAP 簡易認証における LDAPサーバーへの接続プールの最大接続数を指定します。                                                                                                                                                                                                                                                                                                                                                        |
| [`authentication_ldap_simple_server_host`](/system-variables.md#authentication_ldap_simple_server_host-new-in-v710)                     | 新しく追加された | LDAP シンプル認証で LDAPサーバーホストを指定します。                                                                                                                                                                                                                                                                                                                                                                   |
| [`authentication_ldap_simple_server_port`](/system-variables.md#authentication_ldap_simple_server_port-new-in-v710)                     | 新しく追加された | LDAP シンプル認証で LDAPサーバーのTCP/IP ポート番号を指定します。                                                                                                                                                                                                                                                                                                                                                         |
| [`authentication_ldap_simple_tls`](/system-variables.md#authentication_ldap_simple_tls-new-in-v710)                                     | 新しく追加された | プラグインによる LDAPサーバーへの接続が LDAP 簡易認証で StartTLS を使用して保護されるかどうかを指定します。                                                                                                                                                                                                                                                                                                                                  |
| [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710)                                                       | 新しく追加された | Distributed eXecution Framework (DXF) を有効にするかどうかを制御します。DXF を有効にすると、DDL、インポート、およびその他のサポートされている DXF タスクが、クラスター内の複数の TiDB ノードによって共同で完了します。この変数の名前は`tidb_ddl_distribute_reorg`から変更されました。                                                                                                                                                                                                              |
| [`tidb_enable_non_prepared_plan_cache_for_dml`](/system-variables.md#tidb_enable_non_prepared_plan_cache_for_dml-new-in-v710)           | 新しく追加された | DML ステートメントの[準備されていないプラン キャッシュ](/sql-non-prepared-plan-cache.md)機能を有効にするかどうかを制御します。                                                                                                                                                                                                                                                                                                               |
| [`tidb_enable_row_level_checksum`](/system-variables.md#tidb_enable_row_level_checksum-new-in-v710)                                     | 新しく追加された | 単一行データ機能に対して TiCDC データ整合性検証を有効にするかどうかを制御します。                                                                                                                                                                                                                                                                                                                                                      |
| [`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-new-in-v653-and-v710)                                                | 新しく追加された | この変数は、オプティマイザをより細かく制御し、オプティマイザの動作の変更によってアップグレード後に発生するパフォーマンスの低下を防ぐのに役立ちます。                                                                                                                                                                                                                                                                                                                        |
| [`tidb_plan_cache_invalidation_on_fresh_stats`](/system-variables.md#tidb_plan_cache_invalidation_on_fresh_stats-new-in-v710)           | 新しく追加された | 関連テーブルの統計が更新されたときにプラン キャッシュを自動的に無効にするかどうかを制御します。                                                                                                                                                                                                                                                                                                                                                  |
| [`tidb_plan_cache_max_plan_size`](/system-variables.md#tidb_plan_cache_max_plan_size-new-in-v710)                                       | 新しく追加された | 準備済みプラン キャッシュまたは準備されていないプラン キャッシュにキャッシュできるプランの最大サイズを制御します。                                                                                                                                                                                                                                                                                                                                        |
| [`tidb_prefer_broadcast_join_by_exchange_data_size`](/system-variables.md#tidb_prefer_broadcast_join_by_exchange_data_size-new-in-v710) | 新しく追加された | ネットワーク転送のオーバーヘッドが最小のアルゴリズムを使用するかどうかを制御します。この変数を有効にすると、TiDB はそれぞれ`Broadcast Hash Join`と`Shuffled Hash Join`使用してネットワークで交換されるデータのサイズを推定し、サイズの小さい方を選択します。この変数を有効にすると、 [`tidb_broadcast_join_threshold_count`](/system-variables.md#tidb_broadcast_join_threshold_count-new-in-v50)と[`tidb_broadcast_join_threshold_size`](/system-variables.md#tidb_broadcast_join_threshold_size-new-in-v50)無効になります。 |
| [`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-new-in-v710)                                         | 新しく追加された | キャッシュできるプランの最大数を制御します。準備されたプラン キャッシュと準備されていないプラン キャッシュは同じキャッシュを共有します。                                                                                                                                                                                                                                                                                                                             |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーションパラメータ                                                                                                                | タイプを変更   | 説明                                                                                                                                                                               |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------ | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ティビ            | [`performance.force-init-stats`](/tidb-configuration-file.md#force-init-stats-new-in-v657-and-v710)                            | 新しく追加された | TiDB の起動中にサービスを提供する前に、統計の初期化が完了するまで待機するかどうかを制御します。                                                                                                                               |
| ティビ            | [`performance.lite-init-stats`](/tidb-configuration-file.md#lite-init-stats-new-in-v710)                                       | 新しく追加された | TiDB の起動時に軽量統計初期化を使用するかどうかを制御します。                                                                                                                                                |
| ティビ            | [`log.timeout`](/tidb-configuration-file.md#timeout-new-in-v710)                                                               | 新しく追加された | TiDB でのログ書き込み操作のタイムアウトを設定します。ディスク障害によりログの書き込みができない場合、この構成項目により、TiDB プロセスがハングするのではなくpanicになる可能性があります。デフォルト値は`0`で、タイムアウトが設定されていないことを意味します。                                         |
| ティクヴ           | [`region-compact-min-redundant-rows`](/tikv-configuration-file.md#region-compact-min-redundant-rows-new-in-v710)               | 新しく追加された | RocksDB 圧縮をトリガーするために必要な冗長 MVCC 行の数を設定します。デフォルト値は`50000`です。                                                                                                                       |
| ティクヴ           | [`region-compact-redundant-rows-percent`](/tikv-configuration-file.md#region-compact-redundant-rows-percent-new-in-v710)       | 新しく追加された | RocksDB 圧縮をトリガーするために必要な冗長 MVCC 行の割合を設定します。デフォルト値は`20`です。                                                                                                                         |
| ティクヴ           | [`split.byte-threshold`](/tikv-configuration-file.md#byte-threshold-new-in-v50)                                                | 修正済み     | [`region-split-size`](/tikv-configuration-file.md#region-split-size)が 4 GB 以上の場合、デフォルト値を`30MiB`から`100MiB`に変更します。                                                                 |
| ティクヴ           | [`split.qps-threshold`](/tikv-configuration-file.md#qps-threshold)                                                             | 修正済み     | [`region-split-size`](/tikv-configuration-file.md#region-split-size)が 4 GB 以上の場合、デフォルト値を`3000`から`7000`に変更します。                                                                    |
| ティクヴ           | [`split.region-cpu-overload-threshold-ratio`](/tikv-configuration-file.md#region-cpu-overload-threshold-ratio-new-in-v620)     | 修正済み     | [`region-split-size`](/tikv-configuration-file.md#region-split-size)が 4 GB 以上の場合、デフォルト値を`0.25`から`0.75`に変更します。                                                                    |
| ティクヴ           | [`region-compact-check-step`](/tikv-configuration-file.md#region-compact-check-step)                                           | 修正済み     | Partitioned Raft KVが有効な場合（ `storage.engine="partitioned-raft-kv"` ）、デフォルト値を`100`から`5`に変更します。                                                                                     |
| PD             | [`store-limit-version`](/pd-configuration-file.md#store-limit-version-new-in-v710)                                             | 新しく追加された | ストア制限のモードを制御します。値のオプションは`"v1"`と`"v2"`です。                                                                                                                                         |
| PD             | [`schedule.enable-diagnostic`](/pd-configuration-file.md#enable-diagnostic-new-in-v630)                                        | 修正済み     | デフォルト値を`false`から`true`に変更します。これは、スケジューラの診断機能がデフォルトで有効になっていることを意味します。                                                                                                             |
| TiFlash        | `http_port`                                                                                                                    | 削除されました  | HTTP サービス ポート (デフォルト`8123` ) を非推奨にします。                                                                                                                                           |
| TiDB Lightning | [`tikv-importer.pause-pd-scheduler-scope`](/tidb-lightning/tidb-lightning-configuration.md)                                    | 新しく追加された | TiDB Lightning がPD スケジューリングを一時停止する範囲を制御します。デフォルト値は`"table"`で、値のオプションは`"global"`と`"table"`です。                                                                                     |
| TiDB Lightning | [`tikv-importer.region-check-backoff-limit`](/tidb-lightning/tidb-lightning-configuration.md)                                  | 新しく追加された | 分割および分散操作後にリージョンがオンラインになるまで待機する再試行回数を制御します。デフォルト値は`1800`です。最大再試行間隔は 2 秒です。再試行の間にいずれかのリージョンがオンラインになった場合、再試行回数は増加しません。                                                             |
| TiDB Lightning | [`tikv-importer.region-split-batch-size`](/tidb-lightning/tidb-lightning-configuration.md)                                     | 新しく追加された | バッチでリージョンを分割するときのリージョンの数を制御します。デフォルト値は`4096`です。                                                                                                                                  |
| TiDB Lightning | [`tikv-importer.region-split-concurrency`](/tidb-lightning/tidb-lightning-configuration.md)                                    | 新しく追加された | リージョンを分割する際の同時実行性を制御します。デフォルト値は CPU コアの数です。                                                                                                                                      |
| ティCDC          | [`insecure-skip-verify`](/ticdc/ticdc-sink-to-kafka.md)                                                                        | 新しく追加された | Kafka にデータを複製するシナリオで TLS が有効になっている場合に認証アルゴリズムを設定するかどうかを制御します。                                                                                                                    |
| ティCDC          | [`integrity.corruption-handle-level`](/ticdc/ticdc-changefeed-config.md#cli-and-configuration-parameters-of-ticdc-changefeeds) | 新しく追加された | 単一行データのチェックサム検証が失敗した場合の Changefeed のログ レベルを指定します。既定値は`"warn"`です。値のオプションは`"warn"`と`"error"`です。                                                                                    |
| ティCDC          | [`integrity.integrity-check-level`](/ticdc/ticdc-changefeed-config.md#cli-and-configuration-parameters-of-ticdc-changefeeds)   | 新しく追加された | 単一行データのチェックサム検証を有効にするかどうかを制御します。デフォルト値は`"none"`で、この機能を無効にすることを意味します。                                                                                                             |
| ティCDC          | [`sink.only-output-updated-columns`](/ticdc/ticdc-changefeed-config.md#cli-and-configuration-parameters-of-ticdc-changefeeds)  | 新しく追加された | 更新された列のみを出力するかどうかを制御します。デフォルト値は`false`です。                                                                                                                                        |
| ティCDC          | [`sink.enable-partition-separator`](/ticdc/ticdc-changefeed-config.md#cli-and-configuration-parameters-of-ticdc-changefeeds)   | 修正済み     | さらにテストを行った後、デフォルト値を`false`から`true`に変更します。これは、テーブル内のパーティションがデフォルトで別のディレクトリに保存されることを意味します。パーティション化されたテーブルをstorageサービスにレプリケーションする際にデータ損失が発生する可能性を回避するために、値を`true`のままにしておくことをお勧めします。 |

## 改善点 {#improvements}

-   ティビ

    -   `SHOW INDEX`結果[＃42227](https://github.com/pingcap/tidb/issues/42227) @ [ウィノロス](https://github.com/winoros)の Cardinality 列に対応する列の個別値の数を表示します。
    -   TTLスキャンクエリがTiKVブロックキャッシュ[＃43206](https://github.com/pingcap/tidb/issues/43206) @ [lcwangchao](https://github.com/lcwangchao)に影響を与えないようにするには`SQL_NO_CACHE`使用します。
    -   `MAX_EXECUTION_TIME`に関連するエラー メッセージを改善して、MySQL [＃43031](https://github.com/pingcap/tidb/issues/43031) @ [ドヴェーデン](https://github.com/dveeden)と互換性を持たせます。
    -   IndexLookUp [＃26166](https://github.com/pingcap/tidb/issues/26166) @ [定義2014](https://github.com/Defined2014)のパーティション テーブルでの MergeSort 演算子の使用をサポート
    -   MySQL [＃43576](https://github.com/pingcap/tidb/issues/43576) @ [アスジェ](https://github.com/asjdf)と互換性を持たせるために`caching_sha2_password`拡張します

-   ティクヴ

    -   パーティション化されたRaft KV [＃14447](https://github.com/tikv/tikv/issues/14447) @ [スペードA-タン](https://github.com/SpadeA-Tang)使用する場合、分割操作による書き込み QPS への影響を軽減します。
    -   パーティション化されたRaft KV [＃14581](https://github.com/tikv/tikv/issues/14581) @ [バッファフライ](https://github.com/bufferflies)使用するときにスナップショットが占めるスペースを最適化します
    -   TiKV [＃12362](https://github.com/tikv/tikv/issues/12362) @ [翻訳](https://github.com/cfzjywxk)でリクエストの処理の各段階について、より詳細な時間情報を提供します。
    -   ログバックアップ[＃13867](https://github.com/tikv/tikv/issues/13867) @ [ユジュンセン](https://github.com/YuJuncen)で PD をメタストアとして使用します

-   PD

    -   スナップショットの実行の詳細に基づいてストア制限のサイズを自動的に調整するコントローラを追加します。このコントローラを有効にするには、 `store-limit-version`を`v2` (実験的) に設定します。有効にすると、スケールインまたはスケールアウトの速度を制御するために`store limit`構成を手動で調整する必要がなくなります[＃6147](https://github.com/tikv/pd/issues/6147) @ [バッファフライ](https://github.com/bufferflies)
    -   storageエンジンが raft-kv2 [＃6297](https://github.com/tikv/pd/issues/6297) @ [バッファフライ](https://github.com/bufferflies)の場合、ホットスポット スケジューラによって負荷が不安定なリージョンが頻繁にスケジュールされるのを避けるために、履歴負荷情報を追加します。
    -   リーダーのヘルスチェックメカニズムを追加します。etcdリーダーが配置されているPDサーバーがリーダーとして選出できない場合、PDはetcdリーダーをアクティブに切り替えて、PDリーダーが利用可能であることを確認します[＃6403](https://github.com/tikv/pd/issues/6403) @ [ノルーシュ](https://github.com/nolouch)

-   TiFlash

    -   分散storageおよびコンピューティングアーキテクチャにおけるTiFlash のパフォーマンスと安定性を向上[＃6882](https://github.com/pingcap/tiflash/issues/6882) @ [ジェイソン・ファン](https://github.com/JaySon-Huang) @ [そよ風のような](https://github.com/breezewish) @ [ジンヘリン](https://github.com/JinheLin)
    -   小さい方のテーブルをビルド側として選択することで、セミ結合またはアンチセミ結合でのクエリパフォーマンスの最適化をサポートします[＃7280](https://github.com/pingcap/tiflash/issues/7280) @ [いびん87](https://github.com/yibin87)
    -   デフォルト設定[＃7272](https://github.com/pingcap/tiflash/issues/7272) @ [そよ風のような](https://github.com/breezewish)でBRおよびTiDB LightningからTiFlashへのデータ インポートのパフォーマンスを向上

-   ツール

    -   バックアップと復元 (BR)

        -   ログバックアップ[＃14433](https://github.com/tikv/tikv/issues/14433) @ [ジョッカウ](https://github.com/joccau)中に TiKV 構成項目`log-backup.max-flush-interval`変更することをサポート

    -   ティCDC

        -   オブジェクトstorageにデータを複製するシナリオで DDL イベントが発生した場合にディレクトリ構造を最適化する[＃8890](https://github.com/pingcap/tiflow/issues/8890) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)
        -   TiCDC レプリケーションタスクが失敗した場合にアップストリームの GC TLS を設定する方法を最適化する[＃8403](https://github.com/pingcap/tiflow/issues/8403) @ [チャールズ・ジェン44](https://github.com/charleszheng44)
        -   Kafka-on-Pulsar ダウンストリームへのデータ複製をサポート[＃8892](https://github.com/pingcap/tiflow/issues/8892) @ [ハイラスティン](https://github.com/Rustin170506)
        -   オープンプロトコルプロトコルを使用して、Kafka [＃8706](https://github.com/pingcap/tiflow/issues/8706) @ [スドジ](https://github.com/sdojjy)にデータを複製するときに更新が発生した後に変更された列のみを複製することをサポートします。
        -   下流の障害やその他のシナリオにおける TiCDC のエラー処理を最適化する[＃8657](https://github.com/pingcap/tiflow/issues/8657) @ [ヒック](https://github.com/hicqu)
        -   TLS [＃8867](https://github.com/pingcap/tiflow/issues/8867) @ [ハイラスティン](https://github.com/Rustin170506)を有効にするシナリオで認証アルゴリズムを設定するかどうかを制御する構成項目`insecure-skip-verify`を追加します。

    -   TiDB Lightning

        -   不均一なリージョン分布に関連する事前チェック項目の重大度レベルを`Critical`から`Warn`に変更して、ユーザーがデータをインポートできないようにする[＃42836](https://github.com/pingcap/tidb/issues/42836) @ [ok江](https://github.com/okJiang)
        -   データのインポート中に`unknown RPC`が発生した場合に再試行メカニズムを追加する[＃43291](https://github.com/pingcap/tidb/issues/43291) @ [D3ハンター](https://github.com/D3Hunter)
        -   リージョンジョブ[＃43682](https://github.com/pingcap/tidb/issues/43682) @ [ランス6716](https://github.com/lance6716)の再試行メカニズムを強化

## バグ修正 {#bug-fixes}

-   ティビ

    -   パーティション[＃42183](https://github.com/pingcap/tidb/issues/42183) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)を再編成した後、手動で`ANALYZE TABLE`実行するプロンプトが表示されない問題を修正しました。
    -   `DROP TABLE`操作が実行されているときに`ADMIN SHOW DDL JOBS`結果にテーブル名が表示されない問題を修正[＃42268](https://github.com/pingcap/tidb/issues/42268) @ [天菜まお](https://github.com/tiancaiamao)
    -   Grafana モニタリング パネル[＃42562](https://github.com/pingcap/tidb/issues/42562) @ [ピンとb](https://github.com/pingandb)で`Ignore Event Per Minute`と`Stats Cache LRU Cost`チャートが正常に表示されない問題を修正しました。
    -   `INFORMATION_SCHEMA.COLUMNS`テーブル[＃43379](https://github.com/pingcap/tidb/issues/43379) @ [bb7133](https://github.com/bb7133)をクエリしたときに`ORDINAL_POSITION`列が誤った結果を返す問題を修正しました
    -   キャッシュ テーブルに新しい列が追加された後、列[＃42928](https://github.com/pingcap/tidb/issues/42928) @ [ルクス](https://github.com/lqs)のデフォルト値ではなく値が`NULL`なる問題を修正しました。
    -   述語[＃43645](https://github.com/pingcap/tidb/issues/43645) @ [ウィノロス](https://github.com/winoros)をプッシュダウンするときに CTE 結果が正しくない問題を修正しました
    -   多数のパーティションとTiFlashレプリカ[＃42940](https://github.com/pingcap/tidb/issues/42940) @ [ミョンス](https://github.com/mjonss)を持つパーティション テーブルに対して`TRUNCATE TABLE`実行するときに書き込み競合によって発生する DDL 再試行の問題を修正しました。
    -   パーティションテーブル[＃41198](https://github.com/pingcap/tidb/issues/41198) [＃41200](https://github.com/pingcap/tidb/issues/41200) @ [ミョンス](https://github.com/mjonss)作成時に`SUBPARTITION`使用すると警告が表示されない問題を修正
    -   生成された列[＃40066](https://github.com/pingcap/tidb/issues/40066) @ [ジフハウス](https://github.com/jiyfhust)の値オーバーフローの問題を処理する際の MySQL との非互換性の問題を修正
    -   `REORGANIZE PARTITION`他の DDL 操作[＃42442](https://github.com/pingcap/tidb/issues/42442) @ [bb7133](https://github.com/bb7133)と同時に実行できない問題を修正
    -   DDL でパーティション再編成タスクをキャンセルすると、後続の DDL 操作が失敗する可能性がある問題を修正[＃42448](https://github.com/pingcap/tidb/issues/42448) @ [lcwangchao](https://github.com/lcwangchao)
    -   特定の条件下で削除操作のアサーションが正しくない問題を修正[＃42426](https://github.com/pingcap/tidb/issues/42426) @ [天菜まお](https://github.com/tiancaiamao)
    -   cgroup 情報の読み取りエラーにより、TiDBサーバーが起動できない問題を修正しました。エラー メッセージは「cgroup v1 からファイルメモリ.stat を読み取れません: /sys/ メモリ.stat を開いても、そのようなファイルまたはディレクトリはありません」です[＃42659](https://github.com/pingcap/tidb/issues/42659) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   グローバルインデックス[＃42312](https://github.com/pingcap/tidb/issues/42312) @ [L-メープル](https://github.com/L-maple)を持つパーティションテーブルの行のパーティションキーを更新するときに発生する`Duplicate Key`問題を修正します
    -   TTLモニタリングパネルの`Scan Worker Time By Phase`チャートにデータ[＃42515](https://github.com/pingcap/tidb/issues/42515) @ [lcwangchao](https://github.com/lcwangchao)が表示されない問題を修正
    -   グローバルインデックスを持つパーティションテーブルに対する一部のクエリが誤った結果を返す問題を修正[＃41991](https://github.com/pingcap/tidb/issues/41991) [＃42065](https://github.com/pingcap/tidb/issues/42065) @ [L-メープル](https://github.com/L-maple)
    -   パーティションテーブル[＃42180](https://github.com/pingcap/tidb/issues/42180) @ [ミョンス](https://github.com/mjonss)の再編成プロセス中に一部のエラー ログが表示される問題を修正しました
    -   `INFORMATION_SCHEMA.DDL_JOBS`テーブルの`QUERY`列目のデータ長が列定義[＃42440](https://github.com/pingcap/tidb/issues/42440) @ [天菜まお](https://github.com/tiancaiamao)を超える可能性がある問題を修正しました。
    -   `INFORMATION_SCHEMA.CLUSTER_HARDWARE`テーブルでコンテナー[＃42851](https://github.com/pingcap/tidb/issues/42851) @ [ホーキングレイ](https://github.com/hawkingrei)に誤った値が表示される可能性がある問題を修正しました
    -   `ORDER BY` + `LIMIT` [＃43158](https://github.com/pingcap/tidb/issues/43158) @ [定義2014](https://github.com/Defined2014)を使用してパーティションテーブルをクエリすると、誤った結果が返される問題を修正しました。
    -   取り込み方法[＃42903](https://github.com/pingcap/tidb/issues/42903) @ [タンジェンタ](https://github.com/tangenta)を使用して複数の DDL タスクが同時に実行される問題を修正しました
    -   `Limit` [＃24636](https://github.com/pingcap/tidb/issues/24636)を使用してパーティションテーブルをクエリしたときに返される誤った値を修正しました。
    -   IPv6環境で誤ったTiDBアドレスが表示される問題を修正[＃43260](https://github.com/pingcap/tidb/issues/43260) @ [ネクスター](https://github.com/nexustar)
    -   システム変数`tidb_enable_tiflash_read_for_write_stmt`と`tidb_enable_exchange_partition` [＃43281](https://github.com/pingcap/tidb/issues/43281) @ [ゲンリキ](https://github.com/gengliqi)値が誤って表示される問題を修正しました
    -   `tidb_scatter_region`が有効になっている場合、パーティションが切り捨てられた後にリージョンが自動的に分割されない問題を修正[＃43174](https://github.com/pingcap/tidb/issues/43174) [＃43028](https://github.com/pingcap/tidb/issues/43028) @ [ジフハウス](https://github.com/jiyfhust)
    -   生成された列を持つテーブルにチェックを追加し、これらの列でサポートされていない DDL 操作のエラーを報告します[＃38988](https://github.com/pingcap/tidb/issues/38988) [＃24321](https://github.com/pingcap/tidb/issues/24321) @ [天菜まお](https://github.com/tiancaiamao)
    -   特定の型変換エラーでエラーメッセージが正しく表示されない問題を修正[＃41730](https://github.com/pingcap/tidb/issues/41730) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   TiDBノードが正常にシャットダウンされた後、このノードでトリガーされたDDLタスクがキャンセルされる問題を修正[＃43854](https://github.com/pingcap/tidb/issues/43854) @ [ジムララ](https://github.com/zimulala)
    -   PDメンバーアドレスが変更されると、 `AUTO_INCREMENT`列目のIDの割り当てが長時間ブロックされる問題を修正[＃42643](https://github.com/pingcap/tidb/issues/42643) @ [天菜まお](https://github.com/tiancaiamao)
    -   DDL実行中に`GC lifetime is shorter than transaction duration`エラーを報告する問題を修正[＃40074](https://github.com/pingcap/tidb/issues/40074) @ [タンジェンタ](https://github.com/tangenta)
    -   メタデータ ロックが予期せず DDL 実行をブロックする問題を修正[＃43755](https://github.com/pingcap/tidb/issues/43755) @ [翻訳:](https://github.com/wjhuang2016)
    -   IPv6 環境[＃43286](https://github.com/pingcap/tidb/issues/43286) @ [定義2014](https://github.com/Defined2014)でクラスターが一部のシステム ビューを照会できない問題を修正
    -   動的プルーニングモード[＃43686](https://github.com/pingcap/tidb/issues/43686) @ [ミョンス](https://github.com/mjonss)で内部結合中にパーティションが見つからない問題を修正
    -   テーブル[＃43392](https://github.com/pingcap/tidb/issues/43392) @ [グオシャオゲ](https://github.com/guo-shaoge)を分析するときに TiDB が構文エラーを報告する問題を修正しました。
    -   テーブル名の変更中に TiCDC が行の変更の一部を失う可能性がある問題を修正[＃43338](https://github.com/pingcap/tidb/issues/43338) @ [タンジェンタ](https://github.com/tangenta)
    -   クライアントがカーソル読み取り[＃38116](https://github.com/pingcap/tidb/issues/38116) @ [ヤンケオ](https://github.com/YangKeao)を使用すると TiDBサーバーがクラッシュする問題を修正しました
    -   `ADMIN SHOW DDL JOBS LIMIT`誤った結果を返す問題を修正[＃42298](https://github.com/pingcap/tidb/issues/42298) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)
    -   `UNION` [＃42563](https://github.com/pingcap/tidb/issues/42563) @ [lcwangchao](https://github.com/lcwangchao)でユニオンビューと一時テーブルをクエリするときに発生する TiDBpanic問題を修正しました。
    -   トランザクション[＃39664](https://github.com/pingcap/tidb/issues/39664) @ [天菜まお](https://github.com/tiancaiamao)で複数のステートメントをコミットするときにテーブル名の変更が有効にならない問題を修正しました
    -   時間変換[＃42439](https://github.com/pingcap/tidb/issues/42439) @ [qw4990](https://github.com/qw4990)中に準備済みプラン キャッシュと準備されていないプラン キャッシュの動作間の非互換性の問題を修正しました
    -   Decimal 型[＃43311](https://github.com/pingcap/tidb/issues/43311) @ [qw4990](https://github.com/qw4990)のプラン キャッシュによって発生する誤った結果を修正しました。
    -   間違ったフィールドタイプチェック[＃42459](https://github.com/pingcap/tidb/issues/42459) @ [アイリンキッド](https://github.com/AilinKid)による、null 認識アンチ結合 (NAAJ) での TiDBpanic問題を修正
    -   RC 分離レベルでの悲観的トランザクションにおける DML 実行の失敗により、データとインデックス[＃43294](https://github.com/pingcap/tidb/issues/43294) @ [エキシウム](https://github.com/ekexium)の間に不整合が発生する可能性がある問題を修正しました。
    -   極端なケースで、悲観的トランザクションの最初のステートメントが再試行されるときに、このトランザクションのロックを解決するとトランザクションの正確性に影響する可能性がある問題を修正しました[＃42937](https://github.com/pingcap/tidb/issues/42937) @ [ミョンケミンタ](https://github.com/MyonKeminta)
    -   GC がロック[＃43243](https://github.com/pingcap/tidb/issues/43243) @ [ミョンケミンタ](https://github.com/MyonKeminta)を解決するときに、まれに悲観的トランザクションの残留悲観的ロックがデータの正確性に影響を与える可能性がある問題を修正しました。
    -   `LOCK`から`PUT`最適化により、特定のクエリ[＃28011](https://github.com/pingcap/tidb/issues/28011) @ [ジグアン](https://github.com/zyguan)で重複データが返される問題を修正しました。
    -   データが変更された場合、ユニークインデックスのロック動作がデータが変更されていない場合のロック動作と一致しない問題を修正[＃36438](https://github.com/pingcap/tidb/issues/36438) @ [ジグアン](https://github.com/zyguan)

-   ティクヴ

    -   `tidb_pessimistic_txn_fair_locking`有効にすると、極端なケースでは、失敗した RPC 再試行によって期限切れになった要求が、ロック解決操作[＃14551](https://github.com/tikv/tikv/issues/14551) @ [ミョンケミンタ](https://github.com/MyonKeminta)中のデータの正確性に影響を与える可能性がある問題を修正しました。
    -   `tidb_pessimistic_txn_fair_locking`有効にすると、極端なケースでは、失敗した RPC 再試行によって期限切れのリクエストが発生し、トランザクションの競合が無視され、トランザクションの一貫性[＃14311](https://github.com/tikv/tikv/issues/14311) @ [ミョンケミンタ](https://github.com/MyonKeminta)に影響する可能性がある問題を修正しました。
    -   暗号化キーIDの競合により古いキー[＃14585](https://github.com/tikv/tikv/issues/14585) @ [タボキ](https://github.com/tabokie)が削除される可能性がある問題を修正
    -   クラスターを以前のバージョンから v6.5 以降のバージョンにアップグレードしたときに、蓄積されたロック レコードによって発生するパフォーマンス低下の問題を修正しました[＃14780](https://github.com/tikv/tikv/issues/14780) @ [ミョンケミンタ](https://github.com/MyonKeminta)
    -   PITRリカバリプロセス[＃14313](https://github.com/tikv/tikv/issues/14313) @ [ユジュンセン](https://github.com/YuJuncen)中に`raft entry is too large`エラーが発生する問題を修正
    -   PITRリカバリプロセス中に`log_batch` 2GBを超えるためTiKVがパニックになる問題を修正[＃13848](https://github.com/tikv/tikv/issues/13848) @ [ユジュンセン](https://github.com/YuJuncen)

-   PD

    -   TiKV パニック[＃6252](https://github.com/tikv/pd/issues/6252) @ [ヒューシャープ](https://github.com/HuSharp)後に PD 監視パネルの`low space store`の数値が異常になる問題を修正
    -   PDリーダースイッチ[＃6366](https://github.com/tikv/pd/issues/6366) @ [イオマンサス](https://github.com/iosmanthus)後にリージョンヘルス監視データが削除される問題を修正
    -   ルールチェッカーが`schedule=deny`ラベル[＃6426](https://github.com/tikv/pd/issues/6426) @ [ノルーシュ](https://github.com/nolouch)の不健全な領域を修復できない問題を修正しました
    -   TiKV またはTiFlash の再起動後に既存のラベルの一部が失われる問題を修正[＃6467](https://github.com/tikv/pd/issues/6467) @ [じゃがいも](https://github.com/JmPotato)
    -   レプリケーションモード[＃14704](https://github.com/tikv/tikv/issues/14704) @ [ノルーシュ](https://github.com/nolouch)の学習ノードがある場合にレプリケーションステータスを切り替えることができない問題を修正

-   TiFlash

    -   遅延マテリアライゼーション[＃7455](https://github.com/pingcap/tiflash/issues/7455) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)を有効にした後、 `TIMESTAMP`または`TIME`タイプのデータをクエリするとエラーが返される問題を修正しました。
    -   大規模な更新トランザクションにより、 TiFlash が繰り返しエラーを報告し、 [＃7316](https://github.com/pingcap/tiflash/issues/7316) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)を再起動する可能性がある問題を修正しました。

-   ツール

    -   バックアップと復元 (BR)

        -   クラスター[＃42973](https://github.com/pingcap/tidb/issues/42973) @ [ユジュンセン](https://github.com/YuJuncen)で TiKV ノードがクラッシュしたときにバックアップが遅くなる問題を修正
        -   一部のケースでバックアップの失敗により不正確なエラーメッセージが表示される問題を修正[＃43236](https://github.com/pingcap/tidb/issues/43236) @ [ユジュンセン](https://github.com/YuJuncen)

    -   ティCDC

        -   TiCDC タイムゾーン設定[＃8798](https://github.com/pingcap/tiflow/issues/8798) @ [ハイラスティン](https://github.com/Rustin170506)の問題を修正
        -   PDアドレスまたはリーダーに障害が発生したときにTiCDCが自動的に回復できない問題を修正[＃8812](https://github.com/pingcap/tiflow/issues/8812) [＃8877](https://github.com/pingcap/tiflow/issues/8877) @ [アズドンメン](https://github.com/asddongmen)
        -   上流の TiKV ノードの 1 つがクラッシュするとチェックポイントの遅延が増加する問題を修正[＃8858](https://github.com/pingcap/tiflow/issues/8858) @ [ヒック](https://github.com/hicqu)
        -   オブジェクトstorageにデータを複製する際に、上流の`EXCHANGE PARTITION`操作が下流の[＃8914](https://github.com/pingcap/tiflow/issues/8914) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)に正しく複製されない問題を修正しました。
        -   いくつかの特殊なシナリオでソートコンポーネントのメモリ使用量が過剰になることによって発生する OOM 問題を修正[＃8974](https://github.com/pingcap/tiflow/issues/8974) @ [ヒック](https://github.com/hicqu)
        -   下流の Kafka シンクがローリング再起動されたときに発生する TiCDC ノードpanicを修正[＃9023](https://github.com/pingcap/tiflow/issues/9023) @ [アズドンメン](https://github.com/asddongmen)

    -   TiDB データ移行 (DM)

        -   レプリケーション[＃7028](https://github.com/pingcap/tiflow/issues/7028) @ [ランス6716](https://github.com/lance6716)中に latin1 データが破損する可能性がある問題を修正しました

    -   TiDBDumpling

        -   `UNSIGNED INTEGER`型の主キーがチャンク[＃42620](https://github.com/pingcap/tidb/issues/42620) @ [リチュンジュ](https://github.com/lichunzhu)分割に使用できない問題を修正
        -   `--output-file-template`が誤って[＃42391](https://github.com/pingcap/tidb/issues/42391) @ [リチュンジュ](https://github.com/lichunzhu)に設定されている場合に TiDB Dumpling がpanicになる可能性がある問題を修正しました

    -   TiDBBinlog

        -   失敗したDDL文[＃1228](https://github.com/pingcap/tidb-binlog/issues/1228) @ [ok江](https://github.com/okJiang)に遭遇したときにエラーが発生する可能性がある問題を修正

    -   TiDB Lightning

        -   データインポート[＃42456](https://github.com/pingcap/tidb/issues/42456) @ [ランス6716](https://github.com/lance6716)中のパフォーマンス低下の問題を修正
        -   大量のデータをインポートする際の`write to tikv with no leader returned`の問題を修正[＃43055](https://github.com/pingcap/tidb/issues/43055) @ [ランス6716](https://github.com/lance6716)
        -   データインポート[＃43197](https://github.com/pingcap/tidb/issues/43197) @ [D3ハンター](https://github.com/D3Hunter)中にログが`keys within region is empty, skip doIngest`過剰になる問題を修正
        -   部分書き込み[＃43363](https://github.com/pingcap/tidb/issues/43363) @ [ランス6716](https://github.com/lance6716)中にpanicが発生する可能性がある問題を修正
        -   幅の広いテーブル[＃43728](https://github.com/pingcap/tidb/issues/43728) @ [D3ハンター](https://github.com/D3Hunter)をインポートするときに OOM が発生する可能性がある問題を修正しました
        -   TiDB Lightning Grafanaダッシュボード[＃43357](https://github.com/pingcap/tidb/issues/43357) @ [リチュンジュ](https://github.com/lichunzhu)でデータが欠落する問題を修正
        -   `keyspace-name` [＃43684](https://github.com/pingcap/tidb/issues/43684) @ [沢民州](https://github.com/zeminzhou)の設定が間違っているためにインポートに失敗する問題を修正
        -   範囲の部分書き込み中にデータのインポートがスキップされる可能性がある問題を修正[＃43768](https://github.com/pingcap/tidb/issues/43768) @ [ランス6716](https://github.com/lance6716)

## パフォーマンステスト {#performance-test}

TiDB v7.1.0 のパフォーマンスについては、 TiDB Cloud Dedicated クラスターの[TPC-C パフォーマンステストレポート](https://docs.pingcap.com/tidbcloud/v7.1.0-performance-benchmarking-with-tpcc)と[Sysbench パフォーマンステストレポート](https://docs.pingcap.com/tidbcloud/v7.1.0-performance-benchmarking-with-sysbench)を参照してください。

## 寄稿者 {#contributors}

TiDB コミュニティの以下の貢献者に感謝いたします。

-   [えり](https://github.com/blacktear23)
-   [イーサフロー](https://github.com/ethercflow)
-   [ヒヒフフ](https://github.com/hihihuhu)
-   [ジフハウス](https://github.com/jiyfhust)
-   [L-メープル](https://github.com/L-maple)
-   [ルクス](https://github.com/lqs)
-   [ピンとb](https://github.com/pingandb)
-   [ヨークヘレン](https://github.com/yorkhellen)
-   [ユジアリスタ](https://github.com/yujiarista) (初めての投稿者)
