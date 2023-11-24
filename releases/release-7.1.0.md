---
title: TiDB 7.1.0 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 7.1.0.
---

# TiDB 7.1.0 リリースノート {#tidb-7-1-0-release-notes}

発売日：2023年5月31日

TiDB バージョン: 7.1.0

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v7.1/quick-start-with-tidb) | [本番展開](https://docs.pingcap.com/tidb/v7.1/production-deployment-using-tiup) | [インストールパッケージ](https://www.pingcap.com/download/?version=v7.1.0#version-list)

TiDB 7.1.0 は長期サポート リリース (LTS) です。

以前の LTS 6.5.0 と比較して、7.1.0 には[6.6.0-DMR](/releases/release-6.6.0.md) 、 [7.0.0-DMR](/releases/release-7.0.0.md)でリリースされた新機能、改善、バグ修正が含まれているだけでなく、次の主要な機能と改善も導入されています。

<table><thead><tr><th>カテゴリー</th><th>特徴</th><th>説明</th></tr></thead><tbody><tr><td rowspan="4">スケーラビリティとパフォーマンス</td><td>TiFlash は<a href="https://docs.pingcap.com/tidb/v7.1/tiflash-disaggregated-and-s3" target="_blank">、分散storageとコンピューティングアーキテクチャ、および S3 共有storage</a>(実験的、v7.0.0 で導入) をサポートしています。</td><td> TiFlash は、オプションとしてクラウドネイティブアーキテクチャを導入しています。<ul><li> TiFlash のコンピューティングとstorageを分割します。これは、Elastic HTAP リソース使用率のマイルストーンです。</li><li>低コストで共有storageを提供できる S3 ベースのstorageエンジンを導入します。</li></ul></td></tr><tr><td> TiKV は、<a href="https://docs.pingcap.com/tidb/v7.1/system-variables#tidb_store_batch_size" target="_blank">データ リクエストのバッチ集約</a>をサポートしています (v6.6.0 で導入)</td><td>この機能強化により、TiKV バッチ取得操作の合計 RPC が大幅に削減されます。データが高度に分散しており、gRPC スレッド プールのリソースが不十分な状況では、コプロセッサ要求をバッチ処理すると、パフォーマンスが 50% 以上向上する可能性があります。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v7.1/troubleshoot-hot-spot-issues#scatter-read-hotspots" target="_blank">負荷ベースのレプリカ読み取り</a></td><td>読み取りホットスポットのシナリオでは、TiDB はホットスポット TiKV ノードの読み取りリクエストをそのレプリカにリダイレクトできます。この機能は、読み取りホットスポットを効率的に分散し、クラスター リソースの使用を最適化します。負荷ベースのレプリカ読み取りをトリガーするためのしきい値を制御するには、システム変数<a href="https://docs.pingcap.com/tidb/v7.1/system-variables#tidb_load_based_replica_read_threshold-new-in-v700" target="_blank"><code>tidb_load_based_replica_read_threshold</code></a>を調整できます。</td></tr><tr><td> TiKV は<a href="https://docs.pingcap.com/tidb/v7.1/partitioned-raft-kv" target="_blank">パーティション分割されたRaft KVstorageエンジン</a>をサポートします (実験的)</td><td> TiKV は、新世代のstorageエンジン、パーティション化されたRaft KV を導入します。各データリージョンに専用の RocksDB インスタンスを持たせることで、クラスターのstorage容量を TB レベルから PB レベルに拡張し、より安定した書き込みレイテンシーと強力なスケーラビリティを実現できます。</td></tr><tr><td rowspan="2">信頼性と可用性</td><td><a href="https://docs.pingcap.com/tidb/v7.1/tidb-resource-control" target="_blank">リソースグループによるリソース制御</a>（GA）</td><td>リソース グループに基づいたリソース管理をサポートします。これにより、同じクラスター内のさまざまなワークロードにリソースが割り当てられ、分離されます。この機能により、マルチアプリケーション クラスターの安定性が大幅に向上し、マルチテナンシーの基盤が築かれます。 v7.1.0 では、この機能により、実際のワークロードまたはハードウェア展開に基づいてシステム容量を見積もる機能が導入されています。</td></tr><tr><td> TiFlash は<a href="https://docs.pingcap.com/tidb/v7.1/tiflash-spill-disk" target="_blank">ディスクへのスピル</a>をサポートします (v7.0.0 で導入)</td><td> TiFlash は、集計、ソート、ハッシュ結合などのデータ集約型操作における OOM を軽減するために、中間結果のディスクへのスピルをサポートしています。</td></tr><tr><td rowspan="3"> SQL</td><td> <a href="https://docs.pingcap.com/tidb/v7.1/sql-statement-create-index#multi-valued-indexes" target="_blank">多値インデックス</a>(GA)</td><td> MySQL と互換性のある複数値インデックスをサポートし、JSON タイプを強化して MySQL 8.0 との互換性を向上させます。この機能により、複数値列のメンバーシップ チェックの効率が向上します。</td></tr><tr><td><a href="https://docs.pingcap.com/tidb/v7.1/time-to-live" target="_blank">行レベル TTL</a> (v7.0.0 で一般提供)</td><td>データベース サイズの管理をサポートし、一定の期間を経過したデータを自動的に期限切れにすることでパフォーマンスを向上させます。</td></tr><tr><td><a href="https://docs.pingcap.com/tidb/v7.1/generated-columns" target="_blank">生成された列</a>(GA)</td><td>生成された列の値は、列定義の SQL 式によってリアルタイムで計算されます。この機能は、一部のアプリケーション ロジックをデータベース レベルにプッシュするため、クエリの効率が向上します。</td></tr><tr><td rowspan="2">Security</td><td><a href="https://docs.pingcap.com/tidb/v7.1/security-compatibility-with-mysql" target="_blank">LDAP認証</a></td><td>TiDB は、 <a href="https://dev.mysql.com/doc/refman/8.0/en/ldap-pluggable-authentication.html" target="_blank">MySQL 8.0</a>と互換性のある LDAP 認証をサポートしています。</td></tr><tr><td> <a href="https://static.pingcap.com/files/2023/09/18204824/TiDB-Database-Auditing-User-Guide1.pdf" target="_blank">監査ログの機能強化</a>( <a href="https://www.pingcap.com/tidb-enterprise" target="_blank">Enterprise Edition</a>のみ)</td><td> TiDB Enterprise Edition はデータベース監査機能を強化します。よりきめ細かいイベント フィルタリング制御、よりユーザー フレンドリーなフィルタ設定、JSON での新しいファイル出力形式、監査ログのライフサイクル管理を提供することにより、システム監査能力が大幅に向上します。</td></tr></tbody></table>

## 機能の詳細 {#feature-details}

### パフォーマンス {#performance}

-   Partitioned Raft KVstorageエンジンの強化 (実験的) [#11515](https://github.com/tikv/tikv/issues/11515) [#12842](https://github.com/tikv/tikv/issues/12842) @ [ビジージェイ](https://github.com/busyjay) @ [トニーシュクキ](https://github.com/tonyxuqqi) @ [タボキー](https://github.com/tabokie) @ [バッファフライ](https://github.com/bufferflies) @ [5kbps](https://github.com/5kbpers) @ [SpadeA-Tang](https://github.com/SpadeA-Tang) @ [ノールーシュ](https://github.com/nolouch)

    TiDB v6.6.0 では、実験的機能として Partitioned Raft KVstorageエンジンが導入されています。これは、複数の RocksDB インスタンスを使用して TiKVリージョンデータを保存し、各リージョンのデータは個別の RocksDB インスタンスに独立して保存されます。新しいstorageエンジンは、RocksDB インスタンス内のファイルの数とレベルをより適切に制御し、リージョン間のデータ操作の物理的な分離を実現し、より多くのデータの安定した管理をサポートします。オリジナルの TiKVstorageエンジンと比較して、Partitioned Raft KVstorageエンジンを使用すると、同じハードウェア条件および読み取りと書き込みの混合シナリオの下で、約 2 倍の書き込みスループットを達成し、エラスティック スケーリング時間を約 4/5 短縮できます。

    TiDB v7.1.0 では、Partitioned Raft KVstorageエンジンは、 TiDB Lightning、 BR、 TiCDC などのツールをサポートします。

    現在、この機能は実験的であり、本番環境での使用は推奨されません。このエンジンは新しく作成されたクラスターでのみ使用でき、元の TiKVstorageエンジンから直接アップグレードすることはできません。

    詳細については、 [ドキュメンテーション](/partitioned-raft-kv.md)を参照してください。

-   TiFlash は遅延マテリアライゼーション (GA) [#5829](https://github.com/pingcap/tiflash/issues/5829) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)をサポートします

    v7.0.0 では、クエリ パフォーマンスを最適化するための実験的機能として、遅延実体化がTiFlashに導入されました。この機能はデフォルトでは無効になっています ( [`tidb_opt_enable_late_materialization`](/system-variables.md#tidb_opt_enable_late_materialization-new-in-v700)システム変数のデフォルトは`OFF`です)。フィルター条件 ( `WHERE`句) を含む`SELECT`ステートメントを処理する場合、 TiFlash はクエリに必要な列からすべてのデータを読み取り、クエリ条件に基づいてデータをフィルター処理して集計します。遅い具体化が有効な場合、TiDB はフィルター条件の一部を TableScan オペレーターにプッシュダウンすることをサポートします。つまり、 TiFlash は、TableScan オペレーターにプッシュダウンされたフィルター条件に関連する列データを最初にスキャンし、条件を満たす行をフィルター処理してから、これらの行の他の列データをスキャンしてさらなる計算を行うことで、IO スキャンとデータ処理の計算。

    v7.1.0 以降、 TiFlash後期実体化機能が一般提供され、デフォルトで有効になっています ( [`tidb_opt_enable_late_materialization`](/system-variables.md#tidb_opt_enable_late_materialization-new-in-v700)システム変数のデフォルトは`ON`です)。 TiDB オプティマイザーは、クエリの統計とフィルター条件に基づいて、どのフィルターを TableScan オペレーターにプッシュダウンするかを決定します。

    詳細については、 [ドキュメンテーション](/tiflash/tiflash-late-materialization.md)を参照してください。

-   TiFlash は、ネットワーク送信のオーバーヘッドに応じて MPP 参加アルゴリズムを自動的に選択することをサポートしています[#7084](https://github.com/pingcap/tiflash/issues/7084) @ [ソロッツグ](https://github.com/solotzg)

    TiFlash MPP モードは、複数の結合アルゴリズムをサポートしています。 v7.1.0 より前では、TiDB は、MPP モードでブロードキャスト ハッシュ結合アルゴリズムを使用するかどうかを、変数[`tidb_broadcast_join_threshold_count`](/system-variables.md#tidb_broadcast_join_threshold_count-new-in-v50)と変数[`tidb_broadcast_join_threshold_size`](/system-variables.md#tidb_broadcast_join_threshold_size-new-in-v50)および実際のデータ量に基づいて決定します。

    v7.1.0 では、TiDB に[`tidb_prefer_broadcast_join_by_exchange_data_size`](/system-variables.md#tidb_prefer_broadcast_join_by_exchange_data_size-new-in-v710)変数が導入され、ネットワーク送信の最小オーバーヘッドに基づいて MPP Join アルゴリズムを選択するかどうかを制御します。この変数はデフォルトでは無効になっており、デフォルトのアルゴリズム選択方法が v7.1.0 以前と同じであることを示しています。変数を`ON`に設定して有効にします。これを有効にすると、 [`tidb_broadcast_join_threshold_count`](/system-variables.md#tidb_broadcast_join_threshold_count-new-in-v50)と[`tidb_broadcast_join_threshold_size`](/system-variables.md#tidb_broadcast_join_threshold_size-new-in-v50)変数を手動で調整する必要がなくなり (この時点では両方の変数は有効になりません)、TiDB はさまざまな結合アルゴリズムによってネットワーク送信のしきい値を自動的に推定し、最も小さいアルゴリズムを選択します。全体的なオーバーヘッドが増加するため、ネットワーク トラフィックが削減され、MPP クエリのパフォーマンスが向上します。

    詳細については、 [ドキュメンテーション](/tiflash/use-tiflash-mpp-mode.md#algorithm-support-for-the-mpp-mode)を参照してください。

-   読み取りホットスポット[#14151](https://github.com/tikv/tikv/issues/14151) @ [スティックナーフ](https://github.com/sticnarf) @ [あなた06](https://github.com/you06)を軽減するために、負荷ベースのレプリカ読み取りをサポートします。

    読み取りホットスポットのシナリオでは、ホットスポット TiKV ノードが読み取りリクエストを時間内に処理できず、読み取りリクエストがキューイングされます。ただし、現時点ではすべての TiKV リソースが使い果たされているわけではありません。レイテンシーを短縮するために、TiDB v7.1.0 には負荷ベースのレプリカ読み取り機能が導入されています。これにより、TiDB は、ホットスポット TiKV ノードでキューに入れることなく、他の TiKV ノードからデータを読み取ることができます。 [`tidb_load_based_replica_read_threshold`](/system-variables.md#tidb_load_based_replica_read_threshold-new-in-v700)システム変数を使用して、読み取りリクエストのキューの長さを制御できます。リーダー ノードの推定キュー時間がこのしきい値を超えると、TiDB はフォロワー ノードからのデータの読み取りを優先します。この機能により、読み取りホットスポットのシナリオでは、読み取りホットスポットを分散しない場合と比較して、読み取りスループットが 70% ～ 200% 向上します。

    詳細については、 [ドキュメンテーション](/troubleshoot-hot-spot-issues.md#scatter-read-hotspots)を参照してください。

-   準備されていないステートメントの実行プランをキャッシュする機能を強化 (実験的) [#36598](https://github.com/pingcap/tidb/issues/36598) @ [qw4990](https://github.com/qw4990)

    TiDB v7.0.0 では、同時 OLTP の負荷容量を向上させるための実験的機能として、準備されていないプラン キャッシュが導入されています。 v7.1.0 では、TiDB はこの機能を強化し、より多くの SQL ステートメントのキャッシュをサポートします。

    メモリ使用率を向上させるために、TiDB v7.1.0 では、準備されていないプラン キャッシュと準備されたプラン キャッシュのキャッシュ プールがマージされます。キャッシュ サイズは、システム変数[`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-new-in-v710)を使用して制御できます。 [`tidb_prepared_plan_cache_size`](/system-variables.md#tidb_prepared_plan_cache_size-new-in-v610)および[`tidb_non_prepared_plan_cache_size`](/system-variables.md#tidb_non_prepared_plan_cache_size)システム変数は非推奨になりました。

    上位互換性を維持するために、以前のバージョンから v7.1.0 以降のバージョンにアップグレードする場合、キャッシュ サイズ`tidb_session_plan_cache_size` `tidb_prepared_plan_cache_size`と同じ値のままで、 [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache)アップグレード前の設定のままです。十分なパフォーマンス テストが完了したら、 `tidb_enable_non_prepared_plan_cache`を使用して未準備のプラン キャッシュを有効にできます。新しく作成されたクラスターの場合、未準備のプラン キャッシュがデフォルトで有効になります。

    準備されていないプラン キャッシュは、デフォルトでは DML ステートメントをサポートしません。この制限を削除するには、 [`tidb_enable_non_prepared_plan_cache_for_dml`](/system-variables.md#tidb_enable_non_prepared_plan_cache_for_dml-new-in-v710)システム変数を`ON`に設定します。

    詳細については、 [ドキュメンテーション](/sql-non-prepared-plan-cache.md)を参照してください。

-   DDL 分散並列実行フレームワークのサポート (実験的) [#41495](https://github.com/pingcap/tidb/issues/41495) @ [ベンジャミン2037](https://github.com/benjamin2037)

    TiDB v7.1.0 より前では、1 つの TiDB ノードのみが DDL 所有者として機能し、同時に DDL タスクを実行できます。 TiDB v7.1.0 以降、新しい分散並列実行フレームワークでは、複数の TiDB ノードが同じ DDL タスクを並列実行できるため、TiDB クラスターのリソースがより有効に活用され、DDL のパフォーマンスが大幅に向上します。さらに、TiDB ノードを追加することで、DDL のパフォーマンスを直線的に向上させることができます。この機能は現在実験的であり、 `ADD INDEX`操作のみをサポートしていることに注意してください。

    分散フレームワークを使用するには、値[`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710)から`ON`を設定します。

    ```sql
    SET GLOBAL tidb_enable_dist_task = ON;
    ```

    詳細については、 [ドキュメンテーション](/tidb-distributed-execution-framework.md)を参照してください。

### 信頼性 {#reliability}

-   リソース制御が一般公開 (GA) [#38825](https://github.com/pingcap/tidb/issues/38825) @ [ノールーシュ](https://github.com/nolouch) @ [ボーンチェンジャー](https://github.com/BornChanger) @ [グロルフ](https://github.com/glorv) @ [ティエンチャイアマオ](https://github.com/tiancaiamao) @ [コナー1996](https://github.com/Connor1996) @ [Jmポテト](https://github.com/JmPotato) @ [フネス](https://github.com/hnes) @ [キャビンフィーバーB](https://github.com/CabinfeverB) @ [ヒューシャープ](https://github.com/HuSharp)

    TiDB は、リソース グループに基づいたリソース制御機能を強化し、v7.1.0 で GA になります。この機能により、TiDB クラスターのリソース利用効率とパフォーマンスが大幅に向上します。リソース制御機能の導入は、TiDB にとってマイルストーンです。分散データベース クラスターを複数の論理ユニットに分割し、さまざまなデータベース ユーザーを対応するリソース グループにマップし、必要に応じて各リソース グループのクォータを設定できます。クラスターのリソースが制限されている場合、同じリソース グループ内のセッションで使用されるすべてのリソースはクォータ内に制限されます。これにより、リソース グループが過剰に消費されても、他のリソース グループのセッションは影響を受けません。

    この機能を使用すると、異なるシステムからの複数の中小規模のアプリケーションを単一の TiDB クラスターに結合できます。アプリケーションのワークロードが大きくなっても、他のアプリケーションの通常の動作には影響しません。システムのワークロードが低い場合は、設定されたクォータを超えた場合でも、ビジーなアプリケーションに必要なシステム リソースを割り当てることができるため、リソースを最大限に活用できます。さらに、リソース制御機能を合理的に使用することで、クラスタ数を削減し、運用保守の困難を軽減し、管理コストを節約できます。

    TiDB v7.1.0 では、この機能により、実際のワークロードまたはハードウェア展開に基づいてシステム容量を見積もる機能が導入されています。推定機能は、キャパシティ プランニングのためのより正確な参照を提供し、エンタープライズ レベルのシナリオの安定性のニーズを満たすために TiDB リソース割り当てをより適切に管理するのに役立ちます。

    ユーザー エクスペリエンスを向上させるために、TiDB ダッシュボードには[リソースマネージャーページ](/dashboard/dashboard-resource-manager.md)用意されています。このページでリソース グループの構成を表示し、視覚的な方法でクラスターの容量を見積もり、合理的なリソース割り当てを容易にすることができます。

    詳細については、 [ドキュメンテーション](/tidb-resource-control.md)を参照してください。

-   Fast Online DDL のチェックポイント メカニズムをサポートし、フォールト トレランスと自動回復機能を向上させます[#42164](https://github.com/pingcap/tidb/issues/42164) @ [タンジェンタ](https://github.com/tangenta)

    TiDB v7.1.0 では、 [高速オンライン DDL](/ddl-introduction.md)のチェックポイント メカニズムが導入されており、Fast Online DDL のフォールト トレランスと自動リカバリ機能が大幅に向上しています。障害により TiDB 所有者ノードが再起動または変更された場合でも、TiDB は定期的に自動的に更新されるチェックポイントから進行状況を回復できるため、DDL の実行がより安定して効率的になります。

    詳細については、 [ドキュメンテーション](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)を参照してください。

-   バックアップと復元はチェックポイント復元[#42339](https://github.com/pingcap/tidb/issues/42339) @ [レヴルス](https://github.com/Leavrth)をサポートします

    スナップショットの復元またはログの復元は、ディスクの枯渇やノードのクラッシュなどの回復可能なエラーにより中断される場合があります。 TiDB v7.1.0 より前では、エラーが解決された後でも中断前のリカバリの進行状況は無効になるため、リストアを最初から開始する必要がありました。大規模なクラスターの場合、これにはかなりの追加コストがかかります。

    TiDB v7.1.0 以降、バックアップ &amp; リストア (BR) にチェックポイント リストア機能が導入され、中断されたリストアを続行できるようになります。この機能により、中断された復元のほとんどの回復進行状況を保持できます。

    詳細については、 [ドキュメンテーション](/br/br-checkpoint-restore.md)を参照してください。

-   統計[#42160](https://github.com/pingcap/tidb/issues/42160) @ [シュイファングリーンアイズ](https://github.com/xuyifangreeneyes)をロードする戦略を最適化します。

    TiDB v7.1.0 では、実験的機能として軽量統計初期化が導入されています。軽量の統計初期化により、起動時にロードする必要がある統計の数が大幅に削減され、統計のロード速度が向上します。この機能により、複雑なランタイム環境における TiDB の安定性が向上し、TiDB ノードの再起動時のサービス全体への影響が軽減されます。パラメータ[`lite-init-stats`](/tidb-configuration-file.md#lite-init-stats-new-in-v710) ～ `true`を設定して、この機能を有効にすることができます。

    TiDB の起動中、初期統計が完全にロードされる前に実行される SQL ステートメントには最適ではない実行プランが含まれる可能性があり、そのためパフォーマンスの問題が発生します。このような問題を回避するために、TiDB v7.1.0 では構成パラメーター[`force-init-stats`](/tidb-configuration-file.md#force-init-stats-new-in-v710)が導入されています。このオプションを使用すると、起動時に統計の初期化が完了した後にのみ TiDB がサービスを提供するかどうかを制御できます。このパラメータはデフォルトでは無効になっています。

    詳細については、 [ドキュメンテーション](/statistics.md#load-statistics)を参照してください。

-   TiCDC は、単一行データ[#8718](https://github.com/pingcap/tiflow/issues/8718) [#42747](https://github.com/pingcap/tidb/issues/42747) @ [3エースショーハンド](https://github.com/3AceShowHand) @ [ジグアン](https://github.com/zyguan)のデータ整合性検証機能をサポートしています。

    v7.1.0 以降、TiCDC には、チェックサム アルゴリズムを使用して単一行データの整合性を検証するデータ整合性検証機能が導入されています。この機能は、TiDB からデータを書き込み、TiCDC を介してデータをレプリケートし、Kafka クラスターに書き込むプロセスでエラーが発生したかどうかを確認するのに役立ちます。データ整合性検証機能は、Kafka をダウンストリームとして使用する変更フィードのみをサポートしており、現在は Avro プロトコルをサポートしています。

    詳細については、 [ドキュメンテーション](/ticdc/ticdc-integrity-check.md)を参照してください。

-   TiCDC は DDL レプリケーション操作[#8686](https://github.com/pingcap/tiflow/issues/8686) @ [こんにちはラスティン](https://github.com/hi-rustin)を最適化します

    v7.1.0 より前では、大きなテーブルのすべての行に影響を与える DDL 操作 (列の追加または削除など) を実行すると、TiCDC のレプリケーションレイテンシーが大幅に増加していました。 v7.1.0 以降、TiCDC はこのレプリケーション操作を最適化し、ダウンストリームのレイテンシーに対する DDL 操作の影響を軽減します。

    詳細については、 [ドキュメンテーション](/ticdc/ticdc-faq.md#does-ticdc-replicate-data-changes-caused-by-lossy-ddl-operations-to-the-downstream)を参照してください。

-   TiB レベルのデータをインポートする際のTiDB Lightningの安定性が向上しました[#43510](https://github.com/pingcap/tidb/issues/43510) [#43657](https://github.com/pingcap/tidb/issues/43657) @ [D3ハンター](https://github.com/D3Hunter) @ [ランス6716](https://github.com/lance6716)

    v7.1.0 以降、 TiDB Lightningには、TiB レベルのデータをインポートする際の安定性を向上させるために 4 つの構成項目が追加されました。

    -   `tikv-importer.region-split-batch-size`バッチ内のリージョンを分割するときのリージョンの数を制御します。デフォルト値は`4096`です。
    -   `tikv-importer.region-split-concurrency`リージョンを分割するときの同時実行性を制御します。デフォルト値は CPU コアの数です。
    -   `tikv-importer.region-check-backoff-limit`分割および分散操作後にリージョンがオンラインになるまで待機する再試行の回数を制御します。デフォルト値は`1800`で、最大再試行間隔は 2 秒です。再試行の間にいずれかのリージョンがオンラインになった場合、再試行の回数は増加しません。
    -   `tikv-importer.pause-pd-scheduler-scope` TiDB Lightning がPD スケジュールを一時停止する範囲を制御します。値のオプションは`"table"`および`"global"`です。デフォルト値は`"table"`です。 v6.1.0 より前の TiDB バージョンでは、データのインポート中にグローバル スケジュールを一時停止する`"global"`オプションのみを構成できます。 v6.1.0 以降、 `"table"`オプションがサポートされます。これは、ターゲット テーブル データを保存するリージョンに対してのみスケジュールが一時停止されることを意味します。安定性を向上させるために、大量のデータを使用するシナリオでは、この構成項目を`"global"`に設定することをお勧めします。

    詳細については、 [ドキュメンテーション](/tidb-lightning/tidb-lightning-configuration.md)を参照してください。

### SQL {#sql}

-   `INSERT INTO SELECT`ステートメント (GA) [#37515](https://github.com/pingcap/tidb/issues/37515) @ [ゲンリキ](https://github.com/gengliqi)を使用したTiFlashクエリ結果の保存をサポート

    v6.5.0 以降、TiDB は`INSERT INTO SELECT`ステートメントの`SELECT`句 (分析クエリ) をTiFlashにプッシュダウンすることをサポートします。このようにして、さらに分析するために、 TiFlashクエリ結果を`INSERT INTO`で指定された TiDB テーブルに簡単に保存できます。これは、結果のキャッシュ (つまり、結果の具体化) として有効になります。

    v7.1.0 では、この機能は一般提供されています。 `INSERT INTO SELECT`ステートメントの`SELECT`句の実行中に、オプティマイザは、 [SQLモード](/sql-mode.md)およびTiFlashレプリカのコスト見積もりに基づいて、クエリをTiFlashにプッシュするかどうかをインテリジェントに決定できます。したがって、実験的段階で導入された`tidb_enable_tiflash_read_for_write_stmt`システム変数は現在非推奨です。 TiFlashの`INSERT INTO SELECT`ステートメントの計算ルールは`STRICT SQL Mode`要件を満たしていないことに注意してください。そのため、TiDB では、現在のセッションの[SQLモード](/sql-mode.md)が厳密でない場合にのみ、 `INSERT INTO SELECT`ステートメントの`SELECT`句をTiFlashにプッシュダウンできます。つまり、 `sql_mode` value には`STRICT_TRANS_TABLES`と`STRICT_ALL_TABLES`は含まれません。

    詳細については、 [ドキュメンテーション](/tiflash/tiflash-results-materialization.md)を参照してください。

-   MySQL 互換の複数値インデックスが一般提供 (GA) [#39592](https://github.com/pingcap/tidb/issues/39592) @ [ションジウェイ](https://github.com/xiongjiwei) @ [qw4990](https://github.com/qw4990) @ [ヤンケオ](https://github.com/YangKeao)

    JSON 列内の配列の値をフィルター処理するのは一般的な操作ですが、通常のインデックスではそのような操作を高速化することはできません。配列に複数値のインデックスを作成すると、フィルタリングのパフォーマンスが大幅に向上します。 JSON列の配列に多値インデックスがある場合、多値インデックスを使用して`MEMBER OF()` 、 `JSON_CONTAINS()` 、 `JSON_OVERLAPS()`関数の検索条件をフィルタリングすることで、I/O 消費量が削減され、動作速度が向上します。

    v7.1.0 では、複数値インデックス機能が一般提供 (GA) されます。より完全なデータ型をサポートし、TiDB ツールと互換性があります。複数値インデックスを使用すると、本番環境での JSON 配列の検索操作を高速化できます。

    詳細については、 [ドキュメンテーション](/sql-statements/sql-statement-create-index.md#multi-valued-indexes)を参照してください。

-   ハッシュおよびキー パーティション テーブル[#42728](https://github.com/pingcap/tidb/issues/42728) @ [むじょん](https://github.com/mjonss)のパーティション管理を改善します。

    v7.1.0 より前では、TiDB のハッシュおよびキー パーティション テーブルは`TRUNCATE PARTITION`パーティション管理ステートメントのみをサポートしていました。 v7.1.0 以降、ハッシュ パーティション テーブルとキー パーティション テーブルは`ADD PARTITION`および`COALESCE PARTITION`パーティション管理ステートメントもサポートします。したがって、必要に応じて、ハッシュ パーティション テーブルとキー パーティション テーブルのパーティション数を柔軟に調整できます。たとえば、 `ADD PARTITION`ステートメントを使用してパーティションの数を増やしたり、 `COALESCE PARTITION`ステートメントを使用してパーティションの数を減らすことができます。

    詳細については、 [ドキュメンテーション](/partitioned-table.md#manage-hash-and-key-partitions)を参照してください。

-   Range INTERVAL パーティショニングの構文が一般公開 (GA) [#35683](https://github.com/pingcap/tidb/issues/35683) @ [むじょん](https://github.com/mjonss)

    Range INTERVAL パーティショニングの構文 (v6.3.0 で導入) が GA になりました。この構文を使用すると、すべてのパーティションを列挙することなく、希望の間隔で範囲パーティションを定義でき、範囲パーティション DDL ステートメントの長さが大幅に短縮されます。構文は、元の Range パーティショニングの構文と同等です。

    詳細については、 [ドキュメンテーション](/partitioned-table.md#range-interval-partitioning)を参照してください。

-   生成された列が[bb7133](https://github.com/bb7133)で一般公開 (GA) される

    生成された列はデータベースにとって貴重な機能です。テーブルを作成するときに、列の値がユーザーによって明示的に挿入または更新されるのではなく、テーブル内の他の列の値に基づいて計算されるように定義できます。この生成された列は、仮想列または格納された列のいずれかになります。 TiDB は以前のバージョンから MySQL 互換の生成列をサポートしており、この機能は v7.1.0 で GA になります。

    生成された列を使用すると、TiDB に対する MySQL の互換性が向上し、MySQL からの移行プロセスが簡素化されます。また、データ保守の複雑さが軽減され、データの一貫性とクエリの効率が向上します。

    詳細については、 [ドキュメンテーション](/generated-columns.md)を参照してください。

### DB操作 {#db-operations}

-   DDL 操作を手動でキャンセルせずにスムーズなクラスターのアップグレードをサポート (実験的) [#39751](https://github.com/pingcap/tidb/issues/39751) @ [ジムララ](https://github.com/zimulala)

    TiDB v7.1.0 より前では、クラスターをアップグレードするには、アップグレード前に実行中の DDL タスクまたはキューに入れられた DDL タスクを手動でキャンセルし、アップグレード後にそれらのタスクを再度追加する必要があります。

    よりスムーズなアップグレード エクスペリエンスを提供するために、TiDB v7.1.0 は DDL タスクの自動的な一時停止と再開をサポートしています。 v7.1.0 以降、DDL タスクを事前に手動でキャンセルしなくてもクラスターをアップグレードできるようになりました。 TiDB は、実行中またはキューに登録されているユーザー DDL タスクをアップグレード前に自動的に一時停止し、ローリング アップグレード後にこれらのタスクを再開するため、TiDB クラスターのアップグレードが容易になります。

    詳細については、 [ドキュメンテーション](/smooth-upgrade-tidb.md)を参照してください。

### 可観測性 {#observability}

-   オプティマイザ診断情報の強化[#43122](https://github.com/pingcap/tidb/issues/43122) @ [時間と運命](https://github.com/time-and-fate)

    SQL パフォーマンス診断の鍵となるのは、十分な情報を取得することです。 v7.1.0 では、TiDB は引き続きオプティマイザーのランタイム情報をさまざまな診断ツールに追加し、実行プランの選択方法についてのより良い洞察を提供し、SQL パフォーマンスの問題のトラブルシューティングを支援します。新しい情報には次のものが含まれます。

    -   [`PLAN REPLAYER`](/sql-plan-replayer.md)の出力には`debug_trace.json`入ります。
    -   [`EXPLAIN`](/explain-walkthrough.md)の出力内の`operator info`の部分的な統計の詳細。
    -   [遅いクエリ](/identify-slow-queries.md)の`Stats`フィールドの部分的な統計の詳細。

    詳細については、 [`PLAN REPLAYER`を使用してクラスターのオンサイト情報を保存および復元する](/sql-plan-replayer.md) 、 [`EXPLAIN`ウォークスルー](/explain-walkthrough.md) 、および[遅いクエリを特定する](/identify-slow-queries.md)を参照してください。

### Security {#security}

-   TiFlashシステム テーブル情報のクエリに使用されるインターフェイスを置き換えます[#6941](https://github.com/pingcap/tiflash/issues/6941) @ [フロービハッピー](https://github.com/flowbehappy)

    v7.1.0 以降、TiDB の[`INFORMATION_SCHEMA.TIFLASH_TABLES`](/information-schema/information-schema-tiflash-tables.md)および[`INFORMATION_SCHEMA.TIFLASH_SEGMENTS`](/information-schema/information-schema-tiflash-segments.md)システム テーブルのクエリ サービスを提供する場合、 TiFlash はHTTP ポートの代わりに gRPC ポートを使用するため、HTTP サービスのセキュリティ リスクが回避されます。

-   LDAP 認証[#43580](https://github.com/pingcap/tidb/issues/43580) @ [ヤンケオ](https://github.com/YangKeao)をサポート

    v7.1.0 以降、TiDB は LDAP 認証をサポートし、2 つの認証プラグイン`authentication_ldap_sasl`と`authentication_ldap_simple`を提供します。

    詳細については、 [ドキュメンテーション](/security-compatibility-with-mysql.md)を参照してください。

-   データベース監査機能の強化（Enterprise Edition）

    v7.1.0 では、TiDB Enterprise Edition はデータベース監査機能を強化し、その容量を大幅に拡張し、データベース セキュリティ コンプライアンスに対する企業のニーズを満たすユーザー エクスペリエンスを向上させます。

    -   より詳細な監査イベント定義とより詳細な監査設定のために、「フィルター」と「ルール」の概念を導入します。
    -   JSON 形式でのルール定義をサポートし、よりユーザーフレンドリーな構成方法を提供します。
    -   自動ログ ローテーションおよびスペース管理関数を追加し、保持時間とログ サイズの 2 つの次元でのログ ローテーションの構成をサポートします。
    -   監査ログの出力をTEXTと JSON 形式の両方でサポートし、サードパーティ ツールとの統合が容易になります。
    -   監査ログの編集をサポートします。セキュリティを強化するために、すべてのリテラルを置き換えることができます。

    データベース監査は、TiDB Enterprise Edition の重要な機能です。この機能は、企業にデータのセキュリティとコンプライアンスを確保するための強力な監視および監査ツールを提供します。これは、企業管理者がデータベース操作のソースと影響を追跡し、違法なデータの盗難や改ざんを防ぐのに役立ちます。さらに、データベース監査は、企業がさまざまな規制要件やコンプライアンス要件を満たし、法的および倫理的なコンプライアンスを確保するのにも役立ちます。この機能には、企業の情報セキュリティにとって重要な応用価値があります。

    詳細については、 [ユーザーガイド](https://static.pingcap.com/files/2023/09/18204824/TiDB-Database-Auditing-User-Guide1.pdf)を参照してください。この機能は TiDB Enterprise Edition に含まれています。この機能を使用するには、 [TiDB エンタープライズ](https://www.pingcap.com/tidb-enterprise)ページに移動して TiDB Enterprise Edition を入手してください。

## 互換性の変更 {#compatibility-changes}

> **注記：**
>
> このセクションでは、v7.0.0 から現在のバージョン (v7.1.0) にアップグレードするときに知っておく必要がある互換性の変更について説明します。 v6.6.0 以前のバージョンから現在のバージョンにアップグレードする場合は、中間バージョンで導入された互換性の変更も確認する必要がある場合があります。

### 行動の変化 {#behavior-changes}

-   セキュリティを向上させるために、 TiFlash はHTTP サービス ポート (デフォルト`8123` ) を廃止し、代わりに gRPC ポートを使用します。

    TiFlashを v7.1.0 にアップグレードした場合、TiDB v7.1.0 へのアップグレード中に、TiDB はTiFlashシステム テーブル ( [`INFORMATION_SCHEMA.TIFLASH_TABLES`](/information-schema/information-schema-tiflash-tables.md)および[`INFORMATION_SCHEMA.TIFLASH_SEGMENTS`](/information-schema/information-schema-tiflash-segments.md) ) を読み取ることができません。

-   TiDB バージョン v6.2.0 から v7.0.0 のTiDB Lightning は、 TiDB クラスターのバージョンに基づいてグローバル スケジューリングを一時停止するかどうかを決定します。 TiDB クラスターのバージョン &gt;= v6.1.0 の場合、スケジュールはターゲット テーブル データを保存するリージョンに対してのみ一時停止され、ターゲット テーブルのインポートが完了すると再開されます。他のバージョンでは、 TiDB Lightning はグローバル スケジューリングを一時停止します。 TiDB v7.1.0 以降、 [`pause-pd-scheduler-scope`](/tidb-lightning/tidb-lightning-configuration.md)を構成することでグローバル スケジュールを一時停止するかどうかを制御できます。デフォルトでは、 TiDB Lightning はターゲットテーブルデータを保存するリージョンのスケジューリングを一時停止します。ターゲット クラスターのバージョンが v6.1.0 より前の場合、エラーが発生します。この場合、パラメータの値を`"global"`に変更して再試行できます。

-   TiDB v7.1.0 で[`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-to-timestamp.md)使用すると、FLASHBACK 操作の完了後でも、一部のリージョンが FLASHBACK プロセスに残る場合があります。 v7.1.0 ではこの機能を使用しないことをお勧めします。詳細については、問題[#44292](https://github.com/pingcap/tidb/issues/44292)を参照してください。この問題が発生した場合は、 [TiDB スナップショットのバックアップと復元](/br/br-snapshot-guide.md)機能を使用してデータを復元できます。

### システム変数 {#system-variables}

| 変数名                                                                                                                                     | 種類の変更    | 説明                                                                                                                                                                                                                                                                                                                                                                                                       |
| --------------------------------------------------------------------------------------------------------------------------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`tidb_enable_tiflash_read_for_write_stmt`](/system-variables.md#tidb_enable_tiflash_read_for_write_stmt-new-in-v630)                   | 廃止されました  | デフォルト値を`OFF`から`ON`に変更します。 [`tidb_allow_mpp = ON`](/system-variables.md#tidb_allow_mpp-new-in-v50)の場合、オプティマイザは、 [SQLモード](/sql-mode.md)とTiFlashレプリカのコスト見積もりに基づいて、クエリをTiFlashにプッシュするかどうかをインテリジェントに決定します。                                                                                                                                                                                                    |
| [`tidb_non_prepared_plan_cache_size`](/system-variables.md#tidb_non_prepared_plan_cache_size)                                           | 廃止されました  | v7.1.0 以降、このシステム変数は非推奨になりました。 [`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-new-in-v710)を使用して、キャッシュできるプランの最大数を制御できます。                                                                                                                                                                                                                                               |
| [`tidb_prepared_plan_cache_size`](/system-variables.md#tidb_prepared_plan_cache_size-new-in-v610)                                       | 廃止されました  | v7.1.0 以降、このシステム変数は非推奨になりました。 [`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-new-in-v710)を使用して、キャッシュできるプランの最大数を制御できます。                                                                                                                                                                                                                                               |
| `tidb_ddl_distribute_reorg`                                                                                                             | 削除されました  | この変数の名前は[`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710)に変更されます。                                                                                                                                                                                                                                                                                                        |
| [`default_authentication_plugin`](/system-variables.md#default_authentication_plugin)                                                   | 修正済み     | 2 つの新しい値オプション`authentication_ldap_sasl`と`authentication_ldap_simple`が導入されました。                                                                                                                                                                                                                                                                                                                            |
| [`tidb_load_based_replica_read_threshold`](/system-variables.md#tidb_load_based_replica_read_threshold-new-in-v700)                     | 修正済み     | v7.1.0 から有効になり、負荷ベースのレプリカ読み取りをトリガーするためのしきい値を制御します。さらにテストを行った後、デフォルト値を`"0s"`から`"1s"`に変更します。                                                                                                                                                                                                                                                                                                               |
| [`tidb_opt_enable_late_materialization`](/system-variables.md#tidb_opt_enable_late_materialization-new-in-v700)                         | 修正済み     | デフォルト値を`OFF`から`ON`に変更します。これは、 TiFlash遅延マテリアライゼーション機能がデフォルトで有効になることを意味します。                                                                                                                                                                                                                                                                                                                                |
| [`authentication_ldap_sasl_auth_method_name`](/system-variables.md#authentication_ldap_sasl_auth_method_name-new-in-v710)               | 新しく追加された | LDAP SASL認証における認証方式名を指定します。                                                                                                                                                                                                                                                                                                                                                                              |
| [`authentication_ldap_sasl_bind_base_dn`](/system-variables.md#authentication_ldap_sasl_bind_base_dn-new-in-v710)                       | 新しく追加された | LDAP SASL認証における検索ツリー内の検索範囲を制限します。ユーザーが`AS ...`句なしで作成された場合、TiDB はユーザー名に従って LDAPサーバー内の`dn`自動的に検索します。                                                                                                                                                                                                                                                                                                       |
| [`authentication_ldap_sasl_bind_root_dn`](/system-variables.md#authentication_ldap_sasl_bind_root_dn-new-in-v710)                       | 新しく追加された | LDAP SASL 認証でユーザーを検索するために LDAPサーバーにログインするために使用される`dn`を指定します。                                                                                                                                                                                                                                                                                                                                             |
| [`authentication_ldap_sasl_bind_root_pwd`](/system-variables.md#authentication_ldap_sasl_bind_root_pwd-new-in-v710)                     | 新しく追加された | LDAP SASL 認証でユーザーを検索するために LDAPサーバーにログインするために使用するパスワードを指定します。                                                                                                                                                                                                                                                                                                                                             |
| [`authentication_ldap_sasl_ca_path`](/system-variables.md#authentication_ldap_sasl_ca_path-new-in-v710)                                 | 新しく追加された | LDAP SASL 認証での StartTLS 接続の認証局ファイルの絶対パスを指定します。                                                                                                                                                                                                                                                                                                                                                           |
| [`authentication_ldap_sasl_init_pool_size`](/system-variables.md#authentication_ldap_sasl_init_pool_size-new-in-v710)                   | 新しく追加された | LDAP SASL 認証における LDAPサーバーへの接続プール内の初期接続を指定します。                                                                                                                                                                                                                                                                                                                                                            |
| [`authentication_ldap_sasl_max_pool_size`](/system-variables.md#authentication_ldap_sasl_max_pool_size-new-in-v710)                     | 新しく追加された | LDAP SASL認証におけるLDAPサーバーへの接続プール内の最大接続数を指定します。                                                                                                                                                                                                                                                                                                                                                             |
| [`authentication_ldap_sasl_server_host`](/system-variables.md#authentication_ldap_sasl_server_host-new-in-v710)                         | 新しく追加された | LDAP SASL認証におけるLDAPサーバーホストを指定します。                                                                                                                                                                                                                                                                                                                                                                        |
| [`authentication_ldap_sasl_server_port`](/system-variables.md#authentication_ldap_sasl_server_port-new-in-v710)                         | 新しく追加された | LDAP SASL認証におけるLDAPサーバーのTCP/IPポート番号を指定します。                                                                                                                                                                                                                                                                                                                                                               |
| [`authentication_ldap_sasl_tls`](/system-variables.md#authentication_ldap_sasl_tls-new-in-v710)                                         | 新しく追加された | プラグインによる LDAPサーバーへの接続を LDAP SASL 認証の StartTLS で保護するかどうかを指定します。                                                                                                                                                                                                                                                                                                                                           |
| [`authentication_ldap_simple_auth_method_name`](/system-variables.md#authentication_ldap_simple_auth_method_name-new-in-v710)           | 新しく追加された | LDAP簡易認証の認証方式名を指定します。 `SIMPLE`のみをサポートします。                                                                                                                                                                                                                                                                                                                                                                |
| [`authentication_ldap_simple_bind_base_dn`](/system-variables.md#authentication_ldap_simple_bind_base_dn-new-in-v710)                   | 新しく追加された | LDAP簡易認証の検索ツリー内の検索範囲を制限します。ユーザーが`AS ...`句なしで作成された場合、TiDB はユーザー名に従って LDAPサーバー内の`dn`自動的に検索します。                                                                                                                                                                                                                                                                                                             |
| [`authentication_ldap_simple_bind_root_dn`](/system-variables.md#authentication_ldap_simple_bind_root_dn-new-in-v710)                   | 新しく追加された | LDAP簡易認証でユーザーを検索するためにLDAPサーバーにログインするときに使用する`dn`を指定します。                                                                                                                                                                                                                                                                                                                                                   |
| [`authentication_ldap_simple_bind_root_pwd`](/system-variables.md#authentication_ldap_simple_bind_root_pwd-new-in-v710)                 | 新しく追加された | LDAP簡易認証でユーザーを検索するためにLDAPサーバーにログインするためのパスワードを指定します。                                                                                                                                                                                                                                                                                                                                                      |
| [`authentication_ldap_simple_ca_path`](/system-variables.md#authentication_ldap_simple_ca_path-new-in-v710)                             | 新しく追加された | LDAP簡易認証におけるStartTLS接続用の認証局ファイルの絶対パスを指定します。                                                                                                                                                                                                                                                                                                                                                              |
| [`authentication_ldap_simple_init_pool_size`](/system-variables.md#authentication_ldap_simple_init_pool_size-new-in-v710)               | 新しく追加された | LDAP簡易認証におけるLDAPサーバーへの接続プール内の初期接続を指定します。                                                                                                                                                                                                                                                                                                                                                                 |
| [`authentication_ldap_simple_max_pool_size`](/system-variables.md#authentication_ldap_simple_max_pool_size-new-in-v710)                 | 新しく追加された | LDAP簡易認証におけるLDAPサーバーへのコネクションプール内の最大接続数を指定します。                                                                                                                                                                                                                                                                                                                                                            |
| [`authentication_ldap_simple_server_host`](/system-variables.md#authentication_ldap_simple_server_host-new-in-v710)                     | 新しく追加された | LDAP簡易認証のLDAPサーバーホストを指定します。                                                                                                                                                                                                                                                                                                                                                                              |
| [`authentication_ldap_simple_server_port`](/system-variables.md#authentication_ldap_simple_server_port-new-in-v710)                     | 新しく追加された | LDAP簡易認証のLDAPサーバーのTCP/IPポート番号を指定します。                                                                                                                                                                                                                                                                                                                                                                     |
| [`authentication_ldap_simple_tls`](/system-variables.md#authentication_ldap_simple_tls-new-in-v710)                                     | 新しく追加された | プラグインによる LDAPサーバーへの接続を LDAP 簡易認証の StartTLS で保護するかどうかを指定します。                                                                                                                                                                                                                                                                                                                                              |
| [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710)                                                       | 新しく追加された | 分散実行フレームワークを有効にするかどうかを制御します。分散実行を有効にすると、DDL、インポート、およびその他のサポートされているバックエンド タスクが、クラスター内の複数の TiDB ノードによって共同で完了されます。この変数の名前は`tidb_ddl_distribute_reorg`から変更されました。                                                                                                                                                                                                                                             |
| [`tidb_enable_non_prepared_plan_cache_for_dml`](/system-variables.md#tidb_enable_non_prepared_plan_cache_for_dml-new-in-v710)           | 新しく追加された | DML ステートメントの[準備されていないプラン キャッシュ](/sql-non-prepared-plan-cache.md)機能を有効にするかどうかを制御します。                                                                                                                                                                                                                                                                                                                      |
| [`tidb_enable_row_level_checksum`](/system-variables.md#tidb_enable_row_level_checksum-new-in-v710)                                     | 新しく追加された | 単一行データの TiCDC データ整合性検証機能を有効にするかどうかを制御します。                                                                                                                                                                                                                                                                                                                                                                |
| [`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-new-in-v710)                                                         | 新しく追加された | この変数は、オプティマイザーに対するよりきめ細かい制御を提供し、オプティマイザーの動作の変更によって引き起こされるアップグレード後のパフォーマンスの低下を防ぐのに役立ちます。                                                                                                                                                                                                                                                                                                                  |
| [`tidb_plan_cache_invalidation_on_fresh_stats`](/system-variables.md#tidb_plan_cache_invalidation_on_fresh_stats-new-in-v710)           | 新しく追加された | 関連テーブルの統計が更新されたときにプラン キャッシュを自動的に無効にするかどうかを制御します。                                                                                                                                                                                                                                                                                                                                                         |
| [`tidb_plan_cache_max_plan_size`](/system-variables.md#tidb_plan_cache_max_plan_size-new-in-v710)                                       | 新しく追加された | 準備済みまたは未準備のプラン キャッシュにキャッシュできるプランの最大サイズを制御します。                                                                                                                                                                                                                                                                                                                                                            |
| [`tidb_prefer_broadcast_join_by_exchange_data_size`](/system-variables.md#tidb_prefer_broadcast_join_by_exchange_data_size-new-in-v710) | 新しく追加された | ネットワーク送信のオーバーヘッドを最小限に抑えたアルゴリズムを使用するかどうかを制御します。この変数が有効な場合、TiDB はネットワーク内で交換されるデータのサイズをそれぞれ`Broadcast Hash Join`と`Shuffled Hash Join`を使用して推定し、サイズの小さい方を選択します。この変数を有効にすると、 [`tidb_broadcast_join_threshold_count`](/system-variables.md#tidb_broadcast_join_threshold_count-new-in-v50)と[`tidb_broadcast_join_threshold_size`](/system-variables.md#tidb_broadcast_join_threshold_size-new-in-v50)は有効になりません。 |
| [`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-new-in-v710)                                         | 新しく追加された | キャッシュできるプランの最大数を制御します。準備済みプラン キャッシュと準備されていないプラン キャッシュは同じキャッシュを共有します。                                                                                                                                                                                                                                                                                                                                     |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーションパラメータ                                                                                                                | 種類の変更    | 説明                                                                                                                                                                              |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------ | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB           | [`performance.force-init-stats`](/tidb-configuration-file.md#force-init-stats-new-in-v710)                                     | 新しく追加された | TiDB の起動時にサービスを提供する前に、統計の初期化が完了するまで待機するかどうかを制御します。                                                                                                                              |
| TiDB           | [`performance.lite-init-stats`](/tidb-configuration-file.md#lite-init-stats-new-in-v710)                                       | 新しく追加された | TiDB の起動時に軽量統計初期化を使用するかどうかを制御します。                                                                                                                                               |
| TiDB           | [`log.timeout`](/tidb-configuration-file.md#timeout-new-in-v710)                                                               | 新しく追加された | TiDB でのログ書き込み操作のタイムアウトを設定します。ディスク障害が発生してログの書き込みができなくなった場合、この構成項目により、TiDB プロセスがハングせずにpanicを引き起こす可能性があります。デフォルト値は`0`で、タイムアウトが設定されていないことを意味します。                                    |
| TiKV           | [`region-compact-min-redundant-rows`](/tikv-configuration-file.md#region-compact-min-redundant-rows-new-in-v710)               | 新しく追加された | RocksDB 圧縮をトリガーするために必要な冗長 MVCC 行の数を設定します。デフォルト値は`50000`です。                                                                                                                      |
| TiKV           | [`region-compact-redundant-rows-percent`](/tikv-configuration-file.md#region-compact-redundant-rows-percent-new-in-v710)       | 新しく追加された | RocksDB 圧縮をトリガーするために必要な冗長 MVCC 行の割合を設定します。デフォルト値は`20`です。                                                                                                                        |
| TiKV           | [`split.byte-threshold`](/tikv-configuration-file.md#byte-threshold-new-in-v50)                                                | 修正済み     | [`region-split-size`](/tikv-configuration-file.md#region-split-size)が 4 GB 以上の場合、デフォルト値を`30MiB`から`100MiB`に変更します。                                                                |
| TiKV           | [`split.qps-threshold`](/tikv-configuration-file.md#qps-threshold)                                                             | 修正済み     | [`region-split-size`](/tikv-configuration-file.md#region-split-size)が 4 GB 以上の場合、デフォルト値を`3000`から`7000`に変更します。                                                                   |
| TiKV           | [`split.region-cpu-overload-threshold-ratio`](/tikv-configuration-file.md#region-cpu-overload-threshold-ratio-new-in-v620)     | 修正済み     | [`region-split-size`](/tikv-configuration-file.md#region-split-size)が 4 GB 以上の場合、デフォルト値を`0.25`から`0.75`に変更します。                                                                   |
| TiKV           | [`region-compact-check-step`](/tikv-configuration-file.md#region-compact-check-step)                                           | 修正済み     | Partitioned Raft KV が有効な場合 ( `storage.engine="partitioned-raft-kv"` )、デフォルト値を`100`から`5`に変更します。                                                                                  |
| PD             | [`store-limit-version`](/pd-configuration-file.md#store-limit-version-new-in-v710)                                             | 新しく追加された | ストア制限のモードを制御します。値のオプションは`"v1"`と`"v2"`です。                                                                                                                                        |
| PD             | [`schedule.enable-diagnostic`](/pd-configuration-file.md#enable-diagnostic-new-in-v630)                                        | 修正済み     | デフォルト値を`false`から`true`に変更します。これは、スケジューラの診断機能がデフォルトで有効になることを意味します。                                                                                                               |
| TiFlash        | `http_port`                                                                                                                    | 削除されました  | HTTP サービス ポート (デフォルトは`8123` ) を廃止します。                                                                                                                                           |
| TiDB Lightning | [`tikv-importer.pause-pd-scheduler-scope`](/tidb-lightning/tidb-lightning-configuration.md)                                    | 新しく追加された | TiDB Lightning がPD スケジュールを一時停止する範囲を制御します。デフォルト値は`"table"`で、値のオプションは`"global"`および`"table"`です。                                                                                    |
| TiDB Lightning | [`tikv-importer.region-check-backoff-limit`](/tidb-lightning/tidb-lightning-configuration.md)                                  | 新しく追加された | 分割および分散操作後にリージョンがオンラインになるまで待機する再試行の回数を制御します。デフォルト値は`1800`です。最大再試行間隔は 2 秒です。再試行の間にいずれかのリージョンがオンラインになった場合、再試行の回数は増加しません。                                                          |
| TiDB Lightning | [`tikv-importer.region-split-batch-size`](/tidb-lightning/tidb-lightning-configuration.md)                                     | 新しく追加された | バッチ内のリージョンを分割するときのリージョンの数を制御します。デフォルト値は`4096`です。                                                                                                                                |
| TiDB Lightning | [`tikv-importer.region-split-concurrency`](/tidb-lightning/tidb-lightning-configuration.md)                                    | 新しく追加された | リージョンを分割するときの同時実行性を制御します。デフォルト値は CPU コアの数です。                                                                                                                                    |
| TiCDC          | [`insecure-skip-verify`](/ticdc/ticdc-sink-to-kafka.md)                                                                        | 新しく追加された | Kafka にデータをレプリケートするシナリオで TLS が有効になっているときに認証アルゴリズムを設定するかどうかを制御します。                                                                                                               |
| TiCDC          | [`integrity.corruption-handle-level`](/ticdc/ticdc-changefeed-config.md#cli-and-configuration-parameters-of-ticdc-changefeeds) | 新しく追加された | 単一行データのチェックサム検証が失敗した場合の Changefeed のログ レベルを指定します。デフォルト値は`"warn"`です。値のオプションは`"warn"`と`"error"`です。                                                                                |
| TiCDC          | [`integrity.integrity-check-level`](/ticdc/ticdc-changefeed-config.md#cli-and-configuration-parameters-of-ticdc-changefeeds)   | 新しく追加された | 単一行データのチェックサム検証を有効にするかどうかを制御します。デフォルト値は`"none"`で、これは機能を無効にすることを意味します。                                                                                                           |
| TiCDC          | [`sink.only-output-updated-columns`](/ticdc/ticdc-changefeed-config.md#cli-and-configuration-parameters-of-ticdc-changefeeds)  | 新しく追加された | 更新された列のみを出力するかどうかを制御します。デフォルト値は`false`です。                                                                                                                                       |
| TiCDC          | [`sink.enable-partition-separator`](/ticdc/ticdc-changefeed-config.md#cli-and-configuration-parameters-of-ticdc-changefeeds)   | 修正済み     | さらにテストを行った後、デフォルト値を`false`から`true`に変更します。これは、テーブル内のパーティションがデフォルトで別のディレクトリに格納されることを意味します。storageサービスへのパーティション テーブルのレプリケーション中にデータ損失が発生する可能性がある問題を回避するために、値を`true`のままにすることをお勧めします。 |

## 改善点 {#improvements}

-   TiDB

    -   `SHOW INDEX`結果[#42227](https://github.com/pingcap/tidb/issues/42227) @ [ウィノロス](https://github.com/winoros)の Cardinality 列に、対応する列の個別の値の数を表示します。
    -   TTL スキャン クエリが TiKVブロックキャッシュに影響を与えるのを防ぐには`SQL_NO_CACHE`を使用します[#43206](https://github.com/pingcap/tidb/issues/43206) @ [ルクワンチャオ](https://github.com/lcwangchao)
    -   `MAX_EXECUTION_TIME`に関連するエラー メッセージを改善し、MySQL [#43031](https://github.com/pingcap/tidb/issues/43031) @ [ドヴィーデン](https://github.com/dveeden)と互換性を持たせるようにしました。
    -   IndexLookUp [#26166](https://github.com/pingcap/tidb/issues/26166) @ [定義2014](https://github.com/Defined2014)のパーティション テーブルでの MergeSort 演算子の使用のサポート
    -   `caching_sha2_password`を強化して MySQL [#43576](https://github.com/pingcap/tidb/issues/43576) @ [asjdf](https://github.com/asjdf)と互換性を持たせる

-   TiKV

    -   パーティション化されたRaft KV [#14447](https://github.com/tikv/tikv/issues/14447) @ [SpadeA-Tang](https://github.com/SpadeA-Tang)を使用する場合、書き込み QPS に対する分割操作の影響を軽減します。
    -   パーティション化されたRaft KV [#14581](https://github.com/tikv/tikv/issues/14581) @ [バッファフライ](https://github.com/bufferflies)を使用する場合に、スナップショットが占有するスペースを最適化します。
    -   TiKV [#12362](https://github.com/tikv/tikv/issues/12362) @ [cfzjywxk](https://github.com/cfzjywxk)でのリクエストの処理の各段階について、より詳細な時間情報を提供します。
    -   PD をログ バックアップ[#13867](https://github.com/tikv/tikv/issues/13867) @ [ユジュンセン](https://github.com/YuJuncen)のメタストアとして使用する

-   PD

    -   スナップショットの実行の詳細に基づいてストア制限のサイズを自動的に調整するコントローラーを追加します。このコントローラーを有効にするには、 `store-limit-version` ～ `v2`を設定します。有効にすると、スケールインまたはスケールアウトの速度を制御するために`store limit`を手動で調整する必要はありません[#6147](https://github.com/tikv/pd/issues/6147) @ [バッファフライ](https://github.com/bufferflies)
    -   storageエンジンが raft-kv2 [#6297](https://github.com/tikv/pd/issues/6297) @ [バッファフライ](https://github.com/bufferflies)の場合に、ホットスポット スケジューラによる負荷が不安定なリージョンの頻繁なスケジューリングを回避するために、負荷履歴情報を追加します。
    -   リーダーのヘルスチェックメカニズムを追加します。 etcd リーダーが配置されている PDサーバーがリーダーとして選出できない場合、PD は etcd リーダーをアクティブに切り替えて、PD リーダーが利用可能であることを確認します[#6403](https://github.com/tikv/pd/issues/6403) @ [ノールーシュ](https://github.com/nolouch)

-   TiFlash

    -   分散storageおよびコンピューティングアーキテクチャにおけるTiFlash のパフォーマンスと安定性を向上[#6882](https://github.com/pingcap/tiflash/issues/6882) @ [ジェイ・ソン・ファン](https://github.com/JaySon-Huang) @ [ブリーズウィッシュ](https://github.com/breezewish) @ [ジンヘリン](https://github.com/JinheLin)
    -   小さいテーブルをビルド側[#7280](https://github.com/pingcap/tiflash/issues/7280) @ [イービン87](https://github.com/yibin87)として選択することにより、セミ結合またはアンチセミ結合でのクエリ パフォーマンスの最適化をサポートします。
    -   デフォルト設定[#7272](https://github.com/pingcap/tiflash/issues/7272) @ [ブリーズウィッシュ](https://github.com/breezewish)でBRおよびTiDB LightningからTiFlashへのデータ インポートのパフォーマンスが向上しました。

-   ツール

    -   バックアップと復元 (BR)

        -   ログ バックアップ[#14433](https://github.com/tikv/tikv/issues/14433) @ [ジョッカウ](https://github.com/joccau)中の TiKV 構成アイテム`log-backup.max-flush-interval`の変更のサポート

    -   TiCDC

        -   オブジェクトstorage[#8890](https://github.com/pingcap/tiflow/issues/8890) @ [CharlesCheung96](https://github.com/CharlesCheung96)にデータをレプリケートするシナリオで DDL イベントが発生したときにディレクトリ構造を最適化します。
        -   TiCDC レプリケーション タスクが失敗した場合のアップストリームの GC TLS 設定方法を最適化します[#8403](https://github.com/pingcap/tiflow/issues/8403) @ [チャールズジェン44](https://github.com/charleszheng44)
        -   Kafka-on-Pulsar ダウンストリーム[#8892](https://github.com/pingcap/tiflow/issues/8892) @ [こんにちはラスティン](https://github.com/hi-rustin)へのデータのレプリケーションのサポート
        -   Kafka [#8706](https://github.com/pingcap/tiflow/issues/8706) @ [スドジ](https://github.com/sdojjy)にデータをレプリケートするときに、更新が発生した後に変更された列のみをレプリケートするオープン プロトコル プロトコルの使用をサポートします。
        -   ダウンストリーム障害またはその他のシナリオでの TiCDC のエラー処理を最適化します[#8657](https://github.com/pingcap/tiflow/issues/8657) @ [ひっくり返る](https://github.com/hicqu)
        -   TLS [#8867](https://github.com/pingcap/tiflow/issues/8867) @ [こんにちはラスティン](https://github.com/hi-rustin)を有効にするシナリオで認証アルゴリズムを設定するかどうかを制御する構成項目`insecure-skip-verify`を追加します。

    -   TiDB Lightning

        -   ユーザーによるデータのインポートのブロックを避けるために、リージョンの不均一な分布に関連する事前チェック項目の重大度レベルを`Critical`から`Warn`に変更します[#42836](https://github.com/pingcap/tidb/issues/42836) @ [オクジャン](https://github.com/okJiang)
        -   データのインポート中に`unknown RPC`エラーが発生した場合の再試行メカニズムを追加[#43291](https://github.com/pingcap/tidb/issues/43291) @ [D3ハンター](https://github.com/D3Hunter)
        -   リージョンジョブ[#43682](https://github.com/pingcap/tidb/issues/43682) @ [ランス6716](https://github.com/lance6716)の再試行メカニズムを強化します

## バグの修正 {#bug-fixes}

-   TiDB

    -   パーティション[#42183](https://github.com/pingcap/tidb/issues/42183) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)を再編成した後、 `ANALYZE TABLE`手動で実行することについてのプロンプトが表示されない問題を修正
    -   `DROP TABLE`操作の実行時に`ADMIN SHOW DDL JOBS`結果でテーブル名が欠落する問題を修正[#42268](https://github.com/pingcap/tidb/issues/42268) @ [ティエンチャイアマオ](https://github.com/tiancaiamao)
    -   Grafana監視パネル[#42562](https://github.com/pingcap/tidb/issues/42562) @ [ピンアンドブ](https://github.com/pingandb)において、チャート`Ignore Event Per Minute`と`Stats Cache LRU Cost`が正常に表示されない場合がある問題を修正
    -   `INFORMATION_SCHEMA.COLUMNS`テーブル[#43379](https://github.com/pingcap/tidb/issues/43379) @ [bb7133](https://github.com/bb7133)をクエリすると、 `ORDINAL_POSITION`列が間違った結果を返す問題を修正します。
    -   権限テーブル[#41048](https://github.com/pingcap/tidb/issues/41048) @ [bb7133](https://github.com/bb7133)の一部の列における大文字と小文字の区別の問題を修正しました。
    -   キャッシュ テーブルに新しい列が追加された後、値が列のデフォルト値[#42928](https://github.com/pingcap/tidb/issues/42928) @ [lqs](https://github.com/lqs)ではなく`NULL`になる問題を修正します。
    -   述語[#43645](https://github.com/pingcap/tidb/issues/43645) @ [ウィノロス](https://github.com/winoros)をプッシュダウンすると CTE の結果が正しくなくなる問題を修正
    -   多くのパーティションとTiFlashレプリカを含むパーティション テーブルに対して`TRUNCATE TABLE`を実行するときに、書き込み競合によって引き起こされる DDL 再試行の問題を修正します[#42940](https://github.com/pingcap/tidb/issues/42940) @ [むじょん](https://github.com/mjonss)
    -   パーティションテーブル[#41198](https://github.com/pingcap/tidb/issues/41198) [#41200](https://github.com/pingcap/tidb/issues/41200) @ [むじょん](https://github.com/mjonss)の作成で`SUBPARTITION`使用すると警告が表示されない問題を修正
    -   生成されたカラム[#40066](https://github.com/pingcap/tidb/issues/40066) @ [ジフフスト](https://github.com/jiyfhust)での値のオーバーフローの問題に対処するときの MySQL との非互換性の問題を修正しました。
    -   `REORGANIZE PARTITION`が他の DDL 操作[#42442](https://github.com/pingcap/tidb/issues/42442) @ [bb7133](https://github.com/bb7133)と同時に実行できない問題を修正
    -   DDL でパーティション再編成タスクをキャンセルすると、後続の DDL 操作が失敗する可能性がある問題を修正します[#42448](https://github.com/pingcap/tidb/issues/42448) @ [ルクワンチャオ](https://github.com/lcwangchao)
    -   特定の条件下で削除操作のアサーションが正しくない問題を修正[#42426](https://github.com/pingcap/tidb/issues/42426) @ [ティエンチャイアマオ](https://github.com/tiancaiamao)
    -   cgroup 情報の読み取りエラーにより TiDBサーバーが起動できず、エラー メッセージ「cgroup v1 からファイルメモリ.stat を読み取れません: /sys/メモリ.stat を開きます。そのようなファイルまたはディレクトリはありません」 [#42659](https://github.com/pingcap/tidb/issues/42659) @ [ホーキングレイ](https://github.com/hawkingrei)が表示される問題を修正します。
    -   グローバル インデックス[#42312](https://github.com/pingcap/tidb/issues/42312) @ [L-カエデ](https://github.com/L-maple)を持つパーティションテーブルの行のパーティション キーを更新するときに発生する`Duplicate Key`問題を修正します。
    -   TTL監視パネルの`Scan Worker Time By Phase`グラフにデータ[#42515](https://github.com/pingcap/tidb/issues/42515) @ [ルクワンチャオ](https://github.com/lcwangchao)が表示されない問題を修正
    -   グローバル インデックスを使用したパーティション テーブルに対する一部のクエリが誤った結果を返す問題を修正します[#41991](https://github.com/pingcap/tidb/issues/41991) [#42065](https://github.com/pingcap/tidb/issues/42065) @ [L-カエデ](https://github.com/L-maple)
    -   パーティションテーブル[#42180](https://github.com/pingcap/tidb/issues/42180) @ [むじょん](https://github.com/mjonss)の再編成プロセス中にエラー ログが表示される問題を修正
    -   `INFORMATION_SCHEMA.DDL_JOBS`テーブルの`QUERY`列のデータ長が列定義[#42440](https://github.com/pingcap/tidb/issues/42440) @ [ティエンチャイアマオ](https://github.com/tiancaiamao)を超える場合がある問題を修正
    -   `INFORMATION_SCHEMA.CLUSTER_HARDWARE`テーブルがコンテナ[#42851](https://github.com/pingcap/tidb/issues/42851) @ [ホーキングレイ](https://github.com/hawkingrei)で間違った値を表示する可能性がある問題を修正
    -   `ORDER BY` + `LIMIT` [#43158](https://github.com/pingcap/tidb/issues/43158) @ [定義2014](https://github.com/Defined2014)を使用してパーティションテーブルをクエリすると、間違った結果が返される問題を修正します。
    -   インジェストメソッド[#42903](https://github.com/pingcap/tidb/issues/42903) @ [タンジェンタ](https://github.com/tangenta)を使用して同時に実行される複数の DDL タスクの問題を修正します。
    -   `Limit` [#24636](https://github.com/pingcap/tidb/issues/24636)を使用してパーティションテーブルをクエリしたときに返される間違った値を修正しました。
    -   IPv6 環境[#43260](https://github.com/pingcap/tidb/issues/43260) @ [ネクスター](https://github.com/nexustar)で誤った TiDB アドレスが表示される問題を修正
    -   システム変数`tidb_enable_tiflash_read_for_write_stmt`および`tidb_enable_exchange_partition` [#43281](https://github.com/pingcap/tidb/issues/43281) @ [ゲンリチ](https://github.com/gengliqi)の誤った値が表示される問題を修正
    -   `tidb_scatter_region`が有効な場合、パーティションが切り捨てられた後、リージョンが自動的に分割されない問題を修正します[#43174](https://github.com/pingcap/tidb/issues/43174) [#43028](https://github.com/pingcap/tidb/issues/43028) @ [ジフフスト](https://github.com/jiyfhust)
    -   生成された列を含むテーブルにチェックを追加し、これらの列に対するサポートされていない DDL 操作のエラーを報告します[#38988](https://github.com/pingcap/tidb/issues/38988) [#24321](https://github.com/pingcap/tidb/issues/24321) @ [ティエンチャイアマオ](https://github.com/tiancaiamao)
    -   特定の型変換エラー[#41730](https://github.com/pingcap/tidb/issues/41730) @ [ホーキングレイ](https://github.com/hawkingrei)でエラー メッセージが正しくない問題を修正
    -   TiDB ノードが通常にシャットダウンされた後、このノードでトリガーされた DDL タスクがキャンセルされる問題を修正します[#43854](https://github.com/pingcap/tidb/issues/43854) @ [ジムララ](https://github.com/zimulala)
    -   PDメンバーアドレスが変更されると、 `AUTO_INCREMENT`カラムへのID割り当てが長時間ブロックされる問題を修正[#42643](https://github.com/pingcap/tidb/issues/42643) @ [ティエンチャイアマオ](https://github.com/tiancaiamao)
    -   DDL 実行中に`GC lifetime is shorter than transaction duration`エラーが報告される問題を修正[#40074](https://github.com/pingcap/tidb/issues/40074) @ [タンジェンタ](https://github.com/tangenta)
    -   メタデータ ロックにより DDL 実行が予期せずブロックされる問題を修正[#43755](https://github.com/pingcap/tidb/issues/43755) @ [wjhuang2016](https://github.com/wjhuang2016)
    -   IPv6 環境[#43286](https://github.com/pingcap/tidb/issues/43286) @ [定義2014](https://github.com/Defined2014)でクラスターが一部のシステム ビューをクエリできない問題を修正
    -   動的プルーニング モード[#43686](https://github.com/pingcap/tidb/issues/43686) @ [むじょん](https://github.com/mjonss)での内部結合中にパーティションが見つからない問題を修正
    -   テーブル[#43392](https://github.com/pingcap/tidb/issues/43392) @ [グオシャオゲ](https://github.com/guo-shaoge)を分析するときに TiDB が構文エラーを報告する問題を修正
    -   テーブルの名前変更[#43338](https://github.com/pingcap/tidb/issues/43338) @ [タンジェンタ](https://github.com/tangenta)中に TiCDC が行の変更の一部を失う可能性がある問題を修正
    -   クライアントがカーソル読み取り[#38116](https://github.com/pingcap/tidb/issues/38116) @ [ヤンケオ](https://github.com/YangKeao)を使用すると TiDBサーバーがクラッシュする問題を修正
    -   `ADMIN SHOW DDL JOBS LIMIT`が間違った結果[#42298](https://github.com/pingcap/tidb/issues/42298) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)を返す問題を修正
    -   `UNION` [#42563](https://github.com/pingcap/tidb/issues/42563) @ [ルクワンチャオ](https://github.com/lcwangchao)を使用してユニオン ビューと一時テーブルをクエリするときに発生する TiDBpanicの問題を修正しました。
    -   トランザクション[#39664](https://github.com/pingcap/tidb/issues/39664) @ [ティエンチャイアマオ](https://github.com/tiancaiamao)で複数のステートメントをコミットすると、テーブルの名前変更が有効にならない問題を修正します。
    -   時間変換[#42439](https://github.com/pingcap/tidb/issues/42439) @ [qw4990](https://github.com/qw4990)中の準備済みプラン キャッシュと準備されていないプラン キャッシュの動作間の非互換性の問題を修正しました。
    -   Decimal type [#43311](https://github.com/pingcap/tidb/issues/43311) @ [qw4990](https://github.com/qw4990)のプラン キャッシュによって引き起こされる間違った結果を修正しました。
    -   間違ったフィールド タイプ チェック[#42459](https://github.com/pingcap/tidb/issues/42459) @ [アイリンキッド](https://github.com/AilinKid)による、null-aware anti join (NAAJ) での TiDBpanic問題を修正しました。
    -   RC 分離レベルでの悲観的トランザクションでの DML 実行の失敗により、データとインデックス[#43294](https://github.com/pingcap/tidb/issues/43294) @ [エキシウム](https://github.com/ekexium)の間で不整合が発生する可能性がある問題を修正します。
    -   極端な場合、悲観的トランザクションの最初のステートメントが再試行されるときに、このトランザクションのロックを解決するとトランザクションの正確性に影響を与える可能性があるという問題を修正します[#42937](https://github.com/pingcap/tidb/issues/42937) @ [ミョンケミンタ](https://github.com/MyonKeminta)
    -   まれに、GC がロック[#43243](https://github.com/pingcap/tidb/issues/43243) @ [ミョンケミンタ](https://github.com/MyonKeminta)を解決するときに、悲観的トランザクションの残存する悲観的ロックがデータの正確性に影響を与える可能性がある問題を修正します。
    -   `LOCK`から`PUT`最適化により、特定のクエリ[#28011](https://github.com/pingcap/tidb/issues/28011) @ [ジグアン](https://github.com/zyguan)で重複データが返される問題を修正します。
    -   データが変更された場合、一意のインデックスのロック動作がデータが変更されていない場合のロック動作と一致しない問題を修正します[#36438](https://github.com/pingcap/tidb/issues/36438) @ [ジグアン](https://github.com/zyguan)

-   TiKV

    -   `tidb_pessimistic_txn_fair_locking`を有効にすると、極端な場合、RPC 再試行の失敗によって期限切れになったリクエストが、ロック解決操作[#14551](https://github.com/tikv/tikv/issues/14551) @ [ミョンケミンタ](https://github.com/MyonKeminta)中のデータの正確性に影響を与える可能性がある問題を修正します。
    -   `tidb_pessimistic_txn_fair_locking`を有効にすると、極端な場合、RPC 再試行の失敗によって期限切れになったリクエストによってトランザクションの競合が無視され、トランザクションの一貫性[#14311](https://github.com/tikv/tikv/issues/14311) @ [ミョンケミンタ](https://github.com/MyonKeminta)に影響を与える可能性がある問題を修正します。
    -   暗号化キー ID の競合により古いキー[#14585](https://github.com/tikv/tikv/issues/14585) @ [タボキー](https://github.com/tabokie)が削除される可能性がある問題を修正
    -   クラスターが以前のバージョンから v6.5 以降のバージョン[#14780](https://github.com/tikv/tikv/issues/14780) @ [ミョンケミンタ](https://github.com/MyonKeminta)にアップグレードされるときに、蓄積されたロック レコードによって引き起こされるパフォーマンス低下の問題を修正します。
    -   PITR回復処理[#14313](https://github.com/tikv/tikv/issues/14313) @ [ユジュンセン](https://github.com/YuJuncen)中に`raft entry is too large`エラーが発生する問題を修正
    -   `log_batch` 2 GB [#13848](https://github.com/tikv/tikv/issues/13848) @ [ユジュンセン](https://github.com/YuJuncen)を超えたため、PITR 回復プロセス中に TiKV がパニックになる問題を修正

-   PD

    -   TiKVパニック[#6252](https://github.com/tikv/pd/issues/6252) @ [ヒューシャープ](https://github.com/HuSharp)後にPD監視パネルの`low space store`の数字が異常になる問題を修正
    -   PD リーダー スイッチ[#6366](https://github.com/tikv/pd/issues/6366) @ [オスマンサス](https://github.com/iosmanthus)後にリージョンヘルス監視データが削除される問題を修正
    -   ルール チェッカーが`schedule=deny`ラベル[#6426](https://github.com/tikv/pd/issues/6426) @ [ノールーシュ](https://github.com/nolouch)の不健全なリージョンを修復できない問題を修正します。
    -   TiKV またはTiFlashの再起動後に一部の既存のラベルが失われる問題を修正[#6467](https://github.com/tikv/pd/issues/6467) @ [Jmポテト](https://github.com/JmPotato)
    -   レプリケーションモード[#14704](https://github.com/tikv/tikv/issues/14704) @ [ノールーシュ](https://github.com/nolouch)の学習ノードが存在する場合、レプリケーション状態を切り替えられない問題を修正

-   TiFlash

    -   遅延実体化[#7455](https://github.com/pingcap/tiflash/issues/7455) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)を有効にした後、 `TIMESTAMP`または`TIME`タイプのデータをクエリするとエラーが返される問題を修正
    -   大規模な更新トランザクションによってTiFlashが繰り返しエラーを報告し、 [#7316](https://github.com/pingcap/tiflash/issues/7316) @ [ジェイ・ソン・ファン](https://github.com/JaySon-Huang)を再起動する可能性がある問題を修正します。

-   ツール

    -   バックアップと復元 (BR)

        -   クラスター[#42973](https://github.com/pingcap/tidb/issues/42973) @ [ユジュンセン](https://github.com/YuJuncen)で TiKV ノードがクラッシュした場合のバックアップの速度低下の問題を修正
        -   場合によってはバックアップの失敗により不正確なエラー メッセージが表示される問題を修正[#43236](https://github.com/pingcap/tidb/issues/43236) @ [ユジュンセン](https://github.com/YuJuncen)

    -   TiCDC

        -   TiCDC タイムゾーン設定[#8798](https://github.com/pingcap/tiflow/issues/8798) @ [こんにちはラスティン](https://github.com/hi-rustin)の問題を修正
        -   PD アドレスまたはリーダーに障害が発生した場合、TiCDC が自動的に回復できない問題を修正[#8812](https://github.com/pingcap/tiflow/issues/8812) [#8877](https://github.com/pingcap/tiflow/issues/8877) @ [東門](https://github.com/asddongmen)
        -   上流の TiKV ノードの 1 つがクラッシュしたときにチェックポイント ラグが増加する問題を修正します[#8858](https://github.com/pingcap/tiflow/issues/8858) @ [ひっくり返る](https://github.com/hicqu)
        -   オブジェクトstorageにデータをレプリケートするときに、アップストリームの`EXCHANGE PARTITION`オペレーションがダウンストリーム[#8914](https://github.com/pingcap/tiflow/issues/8914) @ [CharlesCheung96](https://github.com/CharlesCheung96)に適切にレプリケートできない問題を修正します。
        -   一部の特殊なシナリオ[#8974](https://github.com/pingcap/tiflow/issues/8974) @ [ひっくり返る](https://github.com/hicqu)におけるソーターコンポーネントの過剰なメモリ使用によって引き起こされる OOM 問題を修正します。
        -   ダウンストリーム Kafka シンクがローリング再起動されるときに発生する TiCDC ノードpanicを修正します[#9023](https://github.com/pingcap/tiflow/issues/9023) @ [東門](https://github.com/asddongmen)

    -   TiDB データ移行 (DM)

        -   レプリケーション[#7028](https://github.com/pingcap/tiflow/issues/7028) @ [ランス6716](https://github.com/lance6716)中に latin1 データが破損する可能性がある問題を修正

    -   TiDBDumpling

        -   `UNSIGNED INTEGER`タイプの主キーがチャンク[#42620](https://github.com/pingcap/tidb/issues/42620) @ [リチュンジュ](https://github.com/lichunzhu)の分割に使用できない問題を修正
        -   `--output-file-template`が誤って[#42391](https://github.com/pingcap/tidb/issues/42391) @ [リチュンジュ](https://github.com/lichunzhu)に設定された場合に TiDB Dumplingがpanicになる問題を修正

    -   TiDBBinlog

        -   失敗した DDL ステートメント[#1228](https://github.com/pingcap/tidb-binlog/issues/1228) @ [オクジャン](https://github.com/okJiang)が発生したときにエラーが発生する可能性がある問題を修正します。

    -   TiDB Lightning

        -   データインポート中のパフォーマンス低下の問題を修正[#42456](https://github.com/pingcap/tidb/issues/42456) @ [ランス6716](https://github.com/lance6716)
        -   大量のデータをインポートする場合の`write to tikv with no leader returned`の問題を修正[#43055](https://github.com/pingcap/tidb/issues/43055) @ [ランス6716](https://github.com/lance6716)
        -   データインポート[#43197](https://github.com/pingcap/tidb/issues/43197) @ [D3ハンター](https://github.com/D3Hunter)中に過剰な`keys within region is empty, skip doIngest`ログが発生する問題を修正
        -   部分書き込み[#43363](https://github.com/pingcap/tidb/issues/43363) @ [ランス6716](https://github.com/lance6716)中にpanicが発生することがある問題を修正
        -   ワイドテーブル[#43728](https://github.com/pingcap/tidb/issues/43728) @ [D3ハンター](https://github.com/D3Hunter)をインポートするときに OOM が発生する可能性がある問題を修正
        -   TiDB Lightning Grafana ダッシュボード[#43357](https://github.com/pingcap/tidb/issues/43357) @ [リチュンジュ](https://github.com/lichunzhu)でデータが欠落している問題を修正
        -   `keyspace-name` [#43684](https://github.com/pingcap/tidb/issues/43684) @ [沢民州](https://github.com/zeminzhou)の誤った設定によるインポートの失敗を修正
        -   場合によっては範囲部分書き込み中にデータのインポートがスキップされる場合がある問題を修正[#43768](https://github.com/pingcap/tidb/issues/43768) @ [ランス6716](https://github.com/lance6716)

## 性能テスト {#performance-test}

TiDB v7.1.0 のパフォーマンスについては、TiDB 専用クラスターの[TPC-C パフォーマンス テスト レポート](https://docs.pingcap.com/tidbcloud/v7.1.0-performance-benchmarking-with-tpcc)と[Sysbench パフォーマンス テスト レポート](https://docs.pingcap.com/tidbcloud/v7.1.0-performance-benchmarking-with-sysbench)を参照してください。

## 貢献者 {#contributors}

TiDB コミュニティの以下の貢献者に感謝いたします。

-   [ブラックティア23](https://github.com/blacktear23)
-   [エーテルフロー](https://github.com/ethercflow)
-   [ヒヒヒヒヒ](https://github.com/hihihuhu)
-   [ジフフスト](https://github.com/jiyfhust)
-   [L-カエデ](https://github.com/L-maple)
-   [lqs](https://github.com/lqs)
-   [ピンアンドブ](https://github.com/pingandb)
-   [ヨークヘレン](https://github.com/yorkhellen)
-   [ユジアリスタ](https://github.com/yujiarista) (初投稿者)
