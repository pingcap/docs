---
title: TiDB 7.1.0 Release Notes
summary: TiDB 7.1.0 の新機能、互換性の変更、改善点、バグ修正について説明します。
---

# TiDB 7.1.0 リリースノート {#tidb-7-1-0-release-notes}

発売日：2023年5月31日

TiDB バージョン: 7.1.0

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v7.1/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v7.1/production-deployment-using-tiup)

TiDB 7.1.0 は長期サポートリリース (LTS) です。

以前の LTS 6.5.0 と比較して、7.1.0 [7.0.0-DMR](/releases/release-7.0.0.md) [6.6.0-DMR](/releases/release-6.6.0.md)リリースされた新機能、改善、バグ修正が含まれているだけでなく、次の主要な機能と改善も導入されています。

<table><thead><tr><th>カテゴリ</th><th>特徴</th><th>説明</th></tr></thead><tbody><tr><td rowspan="4">スケーラビリティとパフォーマンス</td><td>TiFlash は<a href="https://docs.pingcap.com/tidb/v7.1/tiflash-disaggregated-and-s3" target="_blank">、分散storageとコンピューティングアーキテクチャ、および S3 共有storage</a>(実験的、v7.0.0 で導入) をサポートします。</td><td> TiFlash は、オプションとしてクラウドネイティブアーキテクチャを導入します。<ul><li> TiFlash のコンピューティングとstorageを分離します。これは、弾力性のある HTAP リソース利用のマイルストーンとなります。</li><li>低コストで共有storageを提供できる S3 ベースのstorageエンジンを導入します。</li></ul></td></tr><tr><td> TiKV は<a href="https://docs.pingcap.com/tidb/v7.1/system-variables#tidb_store_batch_size" target="_blank">バッチ集約データ要求</a>をサポートします (v6.6.0 で導入)</td><td>この機能強化により、TiKVバッチゲット操作におけるRPCの総数が大幅に削減されます。データが広範囲に分散し、gRPCスレッドプールのリソースが不足している状況では、コプロセッサリクエストをバッチ処理することでパフォーマンスが50%以上向上する可能性があります。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/v7.1/troubleshoot-hot-spot-issues#scatter-read-hotspots" target="_blank">負荷ベースのレプリカ読み取り</a></td><td>読み取りホットスポットのシナリオでは、TiDBはホットスポットTiKVノードへの読み取り要求をそのレプリカにリダイレクトできます。この機能により、読み取りホットスポットが効率的に分散され、クラスタリソースの利用が最適化されます。負荷ベースのレプリカ読み取りをトリガーするしきい値を制御するには、システム変数<a href="https://docs.pingcap.com/tidb/v7.1/system-variables#tidb_load_based_replica_read_threshold-new-in-v700" target="_blank"><code>tidb_load_based_replica_read_threshold</code></a>を調整します。</td></tr><tr><td> TiKV は<a href="https://docs.pingcap.com/tidb/v7.1/partitioned-raft-kv" target="_blank">パーティション化されたRaft KVstorageエンジン</a>をサポートします (実験的)</td><td> TiKVは、新世代のstorageエンジンであるパーティション型Raft KVを導入します。各データリージョンに専用のRocksDBインスタンスを割り当てることで、クラスターのstorage容量をテラバイトレベルからペタバイトレベルまで拡張し、より安定した書き込みレイテンシーと強力なスケーラビリティを実現します。</td></tr><tr><td rowspan="2">信頼性と可用性</td><td><a href="https://docs.pingcap.com/tidb/v7.1/tidb-resource-control" target="_blank">リソースグループによるリソース制御</a>（GA）</td><td>リソースグループに基づくリソース管理をサポートします。これにより、同一クラスター内の異なるワークロードにリソースを割り当て、分離することができます。この機能は、マルチアプリケーション・クラスターの安定性を大幅に向上させ、マルチテナンシーの基盤を構築します。v7.1.0では、この機能により、実際のワークロードまたはハードウェア構成に基づいてシステム容量を見積もる機能が追加されました。</td></tr><tr><td> TiFlash は<a href="https://docs.pingcap.com/tidb/v7.1/tiflash-spill-disk" target="_blank">ディスクへの書き込み</a>をサポートします (v7.0.0 で導入)</td><td> TiFlash は、集約、ソート、ハッシュ結合などのデータ集約型操作における OOM を軽減するために、ディスクへの中間結果のスピルをサポートします。</td></tr><tr><td rowspan="3"> SQL</td><td> <a href="https://docs.pingcap.com/tidb/v7.1/sql-statement-create-index#multi-valued-indexes" target="_blank">多値インデックス</a>（GA）</td><td> MySQL互換の多値インデックスをサポートし、JSON型を拡張することでMySQL 8.0との互換性を向上させました。この機能により、多値列のメンバーシップチェックの効率が向上します。</td></tr><tr><td><a href="https://docs.pingcap.com/tidb/v7.1/time-to-live" target="_blank">行レベルの TTL</a> (v7.0.0 で GA)</td><td>一定の期間が経過したデータを自動的に期限切れにすることで、データベース サイズの管理をサポートし、パフォーマンスを向上します。</td></tr><tr><td><a href="https://docs.pingcap.com/tidb/v7.1/generated-columns" target="_blank">生成された列</a>（GA）</td><td>生成された列の値は、列定義内のSQL式によってリアルタイムに計算されます。この機能により、一部のアプリケーションロジックがデータベースレベルにプッシュされ、クエリの効率が向上します。</td></tr><tr><td rowspan="2">Security</td><td><a href="https://docs.pingcap.com/tidb/v7.1/security-compatibility-with-mysql" target="_blank">LDAP認証</a></td><td>TiDB は、 <a href="https://dev.mysql.com/doc/refman/8.0/en/ldap-pluggable-authentication.html" target="_blank">MySQL 8.0</a>と互換性のある LDAP 認証をサポートしています。</td></tr><tr><td> <a href="https://static.pingcap.com/files/2023/09/18204824/TiDB-Database-Auditing-User-Guide1.pdf" target="_blank">監査ログの強化</a>（<a href="https://www.pingcap.com/tidb-enterprise" target="_blank">エンタープライズエディション</a>のみ）</td><td> TiDB Enterprise Editionは、データベース監査機能を強化しました。よりきめ細かなイベントフィルタリング制御、よりユーザーフレンドリーなフィルタ設定、JSON形式の新しいファイル出力形式、監査ログのライフサイクル管理などにより、システム監査能力が大幅に向上します。</td></tr></tbody></table>

## 機能の詳細 {#feature-details}

### パフォーマンス {#performance}

-   パーティション化されたRaft KVstorageエンジンの強化 (実験的) [＃11515](https://github.com/tikv/tikv/issues/11515) [＃12842](https://github.com/tikv/tikv/issues/12842) @ [忙しいカケス](https://github.com/busyjay) @ [トニー・シュッキ](https://github.com/tonyxuqqi) @ [タボキ](https://github.com/tabokie) @ [バッファフライ](https://github.com/bufferflies) @ [5kbps](https://github.com/5kbpers) @ [スペードA-タン](https://github.com/SpadeA-Tang) @ [ノルーシュ](https://github.com/nolouch)

    TiDB v6.6.0では、実験的機能としてPartitioned Raft KVstorageエンジンが導入されました。このストレージエンジンは、複数のRocksDBインスタンスを使用してTiKVリージョンデータを保存し、各リージョンのデータは独立したRocksDBインスタンスに独立して保存されます。この新しいstorageエンジンは、RocksDBインスタンス内のファイルの数とレベルをより適切に制御し、リージョン間のデータ操作の物理的な分離を実現し、より多くのデータの安定した管理をサポートします。従来のTiKVstorageエンジンと比較して、Partitioned Raft KVstorageエンジンを使用すると、同じハードウェア条件で読み取りと書き込みが混在するシナリオにおいて、書き込みスループットが約2倍になり、エラスティックスケーリング時間が約4/5短縮されます。

    TiDB v7.1.0 では、Partitioned Raft KVstorageエンジンがTiDB Lightning、 BR、TiCDC などのツールをサポートしています。

    現在、この機能は実験的であり、本番環境での使用は推奨されません。このエンジンは新規に作成されたクラスターでのみ使用でき、元のTiKVstorageエンジンから直接アップグレードすることはできません。

    詳細については[ドキュメント](/partitioned-raft-kv.md)参照してください。

-   TiFlashは遅延マテリアライゼーション（GA） [＃5829](https://github.com/pingcap/tiflash/issues/5829) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)をサポートします

    v7.0.0 では、クエリ パフォーマンスを最適化するための実験的機能として、 TiFlashに遅延マテリアライゼーションが導入されました。この機能はデフォルトでは無効になっています ( [`tidb_opt_enable_late_materialization`](/system-variables.md#tidb_opt_enable_late_materialization-new-in-v700)システム変数はデフォルトで`OFF`に設定されます)。フィルタ条件 ( `WHERE`句) を含む`SELECT`ステートメントを処理する場合、 TiFlash はクエリに必要な列からすべてのデータを読み取り、クエリ条件に基づいてデータをフィルタリングして集計します。遅延マテリアライゼーションを有効にすると、TiDB はフィルタ条件の一部を TableScan 演算子にプッシュ ダウンすることをサポートします。つまり、 TiFlash は最初に TableScan 演算子にプッシュ ダウンされたフィルタ条件に関連する列データをスキャンし、条件を満たす行をフィルタリングしてから、これらの行の他の列データをスキャンしてさらに計算することで、データ処理の IO スキャンと計算を削減します。

    バージョン7.1.0以降、 TiFlashの遅延マテリアライゼーション機能が一般提供され、デフォルトで有効化されています（システム変数[`tidb_opt_enable_late_materialization`](/system-variables.md#tidb_opt_enable_late_materialization-new-in-v700)デフォルトで`ON`に設定されています）。TiDBオプティマイザーは、クエリの統計情報とフィルター条件に基づいて、TableScan演算子にプッシュダウンするフィルターを決定します。

    詳細については[ドキュメント](/tiflash/tiflash-late-materialization.md)参照してください。

-   TiFlashは、ネットワーク伝送のオーバーヘッドに応じてMPP Joinアルゴリズムを自動的に選択することをサポートしています[＃7084](https://github.com/pingcap/tiflash/issues/7084) @ [ソロツグ](https://github.com/solotzg)

    TiFlash MPPモードは複数の結合アルゴリズムをサポートしています。v7.1.0より前のバージョンでは、TiDBは[`tidb_broadcast_join_threshold_count`](/system-variables.md#tidb_broadcast_join_threshold_count-new-in-v50)と[`tidb_broadcast_join_threshold_size`](/system-variables.md#tidb_broadcast_join_threshold_size-new-in-v50)変数と実際のデータ量に基づいて、MPPモードでブロードキャストハッシュ結合アルゴリズムを使用するかどうかを判断します。

    v7.1.0では、TiDBに[`tidb_prefer_broadcast_join_by_exchange_data_size`](/system-variables.md#tidb_prefer_broadcast_join_by_exchange_data_size-new-in-v710)変数が導入されました。この変数は、ネットワーク伝送の最小オーバーヘッドに基づいてMPP Joinアルゴリズムを選択するかどうかを制御し、この変数はデフォルトで無効になっています。この変数を`ON`に設定すると、デフォルトのアルゴリズム選択方法がv7.1.0以前と同じになります。この変数を有効にすると、 [`tidb_broadcast_join_threshold_count`](/system-variables.md#tidb_broadcast_join_threshold_count-new-in-v50)と[`tidb_broadcast_join_threshold_size`](/system-variables.md#tidb_broadcast_join_threshold_size-new-in-v50)変数を手動で調整する必要がなくなります（この時点では両方の変数は有効になりません）。TiDBは、異なるJoinアルゴリズムによるネットワーク伝送のしきい値を自動的に推定し、全体的なオーバーヘッドが最小のアルゴリズムを選択します。これにより、ネットワークトラフィックが削減され、MPPクエリのパフォーマンスが向上します。

    詳細については[ドキュメント](/tiflash/use-tiflash-mpp-mode.md#algorithm-support-for-the-mpp-mode)参照してください。

-   読み取りホットスポットを軽減するために負荷ベースのレプリカ読み取りをサポートする[＃14151](https://github.com/tikv/tikv/issues/14151) @ [スティクナーフ](https://github.com/sticnarf) @ [あなた06](https://github.com/you06)

    読み取りホットスポットのシナリオでは、ホットスポット TiKV ノードが読み取り要求を時間内に処理できず、読み取り要求がキューイングされます。ただし、この時点ですべての TiKV リソースが使い果たされるわけではありません。レイテンシーを削減するために、TiDB v7.1.0 では負荷ベースのレプリカ読み取り機能が導入されました。これにより、TiDB はホットスポット TiKV ノードでキューイングすることなく、他の TiKV ノードからデータを読み取ることができます。読み取り要求のキューの長さは、 [`tidb_load_based_replica_read_threshold`](/system-variables.md#tidb_load_based_replica_read_threshold-new-in-v700)システム変数を使用して制御できます。リーダーノードの推定キュー時間がこのしきい値を超えると、TiDB はフォロワーノードからのデータの読み取りを優先します。この機能により、読み取りホットスポットを分散させない場合と比較して、読み取りホットスポットのシナリオで読み取りスループットが 70% ～ 200% 向上します。

    詳細については[ドキュメント](/troubleshoot-hot-spot-issues.md#scatter-read-hotspots)参照してください。

-   非準備済みステートメントの実行プランをキャッシュする機能の強化（実験的） [＃36598](https://github.com/pingcap/tidb/issues/36598) @ [qw4990](https://github.com/qw4990)

    TiDB v7.0.0では、同時実行OLTPの負荷容量を向上させるための実験的機能として、非準備プランキャッシュが導入されました。v7.1.0では、この機能が強化され、より多くのSQL文のキャッシュがサポートされるようになりました。

    メモリ使用率を向上させるため、TiDB v7.1.0 では、準備されていないプランキャッシュと準備済みのプランキャッシュのキャッシュプールを統合します。キャッシュサイズはシステム変数[`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-new-in-v710)使用して制御できます。システム変数[`tidb_prepared_plan_cache_size`](/system-variables.md#tidb_prepared_plan_cache_size-new-in-v610)と[`tidb_non_prepared_plan_cache_size`](/system-variables.md#tidb_non_prepared_plan_cache_size)非推奨です。

    前方互換性を維持するため、以前のバージョンからv7.1.0以降のバージョンにアップグレードする場合、キャッシュサイズ`tidb_session_plan_cache_size` `tidb_prepared_plan_cache_size`と同じ値のままになり、 [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache)アップグレード前の設定のままになります。十分なパフォーマンステストを行った後、 `tidb_enable_non_prepared_plan_cache`を使用して非準備プランキャッシュを有効化できます。新規に作成されたクラスターでは、非準備プランキャッシュはデフォルトで有効化されています。

    非準備プランキャッシュは、デフォルトではDML文をサポートしません。この制限を解除するには、システム変数[`tidb_enable_non_prepared_plan_cache_for_dml`](/system-variables.md#tidb_enable_non_prepared_plan_cache_for_dml-new-in-v710) `ON`に設定します。

    詳細については[ドキュメント](/sql-non-prepared-plan-cache.md)参照してください。

-   TiDB 分散実行フレームワーク (DXF) のサポート (実験的) [＃41495](https://github.com/pingcap/tidb/issues/41495) @ [ベンジャミン2037](https://github.com/benjamin2037)

    TiDB v7.1.0より前では、DDLオーナーとして機能し、同時にDDLタスクを実行できるのは1つのTiDBノードのみでした。TiDB v7.1.0以降の新しいDXFでは、複数のTiDBノードが同じDDLタスクを並列に実行できるため、TiDBクラスターのリソースをより有効に活用し、DDLのパフォーマンスを大幅に向上させることができます。さらに、TiDBノードを追加することで、DDLのパフォーマンスを線形的に向上させることができます。この機能は現在実験的であり、 `ADD INDEX`操作のみをサポートしていることにご注意ください。

    DXFを使用するには、 [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710)の値を`ON`に設定します。

    ```sql
    SET GLOBAL tidb_enable_dist_task = ON;
    ```

    詳細については[ドキュメント](/tidb-distributed-execution-framework.md)参照してください。

### 信頼性 {#reliability}

-   リソース制御が一般提供開始 (GA) [＃38825](https://github.com/pingcap/tidb/issues/38825) @ [ノルーシュ](https://github.com/nolouch) @ [生まれ変わった人](https://github.com/BornChanger) @ [栄光](https://github.com/glorv) @ [天菜まお](https://github.com/tiancaiamao) @ [コナー1996](https://github.com/Connor1996) @ [Jmポテト](https://github.com/JmPotato) @ [ネス](https://github.com/hnes) @ [キャビンフィーバーB](https://github.com/CabinfeverB) @ [HuSharp](https://github.com/HuSharp)

    TiDBは、リソースグループに基づくリソース制御機能を強化し、v7.1.0でGAとなりました。この機能により、TiDBクラスターのリソース利用効率とパフォーマンスが大幅に向上します。リソース制御機能の導入は、TiDBにとって画期的な出来事です。分散データベースクラスターを複数の論理ユニットに分割し、異なるデータベースユーザーを対応するリソースグループにマッピングし、必要に応じて各リソースグループのクォータを設定できます。クラスターリソースが制限されている場合、同じリソースグループ内のセッションで使用されるすべてのリソースはクォータに制限されます。これにより、あるリソースグループが過剰に消費されても、他のリソースグループのセッションには影響しません。

    この機能により、異なるシステムの複数の中小規模アプリケーションを単一のTiDBクラスタに統合できます。アプリケーションのワークロードが大きくなっても、他のアプリケーションの正常な動作に影響を与えることはありません。システムのワークロードが低い場合は、設定されたクォータを超えても、ビジー状態のアプリケーションに必要なシステムリソースを割り当てることができるため、リソースを最大限に活用できます。さらに、リソース制御機能を合理的に活用することで、クラスタ数を削減し、運用・保守の難易度を軽減し、管理コストを削減できます。

    TiDB v7.1.0では、実際のワークロードやハードウェア構成に基づいてシステム容量を見積もる機能が導入されました。この機能により、キャパシティプランニングのより正確な基準が得られ、エンタープライズレベルのシナリオにおける安定性のニーズを満たすためにTiDBのリソース割り当てをより適切に管理できるようになります。

    ユーザーエクスペリエンスを向上させるために、TiDB ダッシュボードは[リソースマネージャーページ](/dashboard/dashboard-resource-manager.md)提供します。このページではリソースグループの構成を表示し、クラスターの容量を視覚的に見積もることができるため、適切なリソース割り当てが容易になります。

    詳細については[ドキュメント](/tidb-resource-control-ru-groups.md)参照してください。

-   フォールトトレランスと自動リカバリ機能を向上させるために、高速オンラインDDLのチェックポイントメカニズムをサポートします[＃42164](https://github.com/pingcap/tidb/issues/42164) @ [接線](https://github.com/tangenta)

    TiDB v7.1.0では、 [高速オンラインDDL](/ddl-introduction.md)のチェックポイント機構が導入され、Fast Online DDLのフォールトトレランスと自動リカバリ機能が大幅に向上しました。TiDBオーナーノードが障害により再起動または変更された場合でも、TiDBは定期的に自動更新されるチェックポイントから進捗状況をリカバリできるため、DDL実行の安定性と効率性が向上します。

    詳細については[ドキュメント](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)参照してください。

-   バックアップとリストアはチェックポイントリストア[＃42339](https://github.com/pingcap/tidb/issues/42339) @ [リーヴルス](https://github.com/Leavrth)をサポートします

    スナップショットリストアまたはログリストアは、ディスク枯渇やノードクラッシュなどの回復可能なエラーにより中断される可能性があります。TiDB v7.1.0より前のバージョンでは、エラーに対処した後でも中断前のリカバリの進行状況が無効になり、リストアを最初からやり直す必要がありました。大規模クラスターでは、これはかなりの追加コストが発生します。

    TiDB v7.1.0以降、バックアップ＆リストア（BR）にチェックポイント・リストア機能が導入され、中断されたリストアを再開できるようになりました。この機能により、中断されたリストアのリカバリ進行状況の大部分を保持できます。

    詳細については[ドキュメント](/br/br-checkpoint-restore.md)参照してください。

-   統計[＃42160](https://github.com/pingcap/tidb/issues/42160) @ [xuyifangreeneyes](https://github.com/xuyifangreeneyes)ロード戦略を最適化する

    TiDB v7.1.0では、軽量統計初期化機能が実験的機能として導入されました。軽量統計初期化により、起動時にロードする必要がある統計情報の数が大幅に削減され、統計情報のロード速度が向上します。この機能により、複雑なランタイム環境におけるTiDBの安定性が向上し、TiDBノードの再起動時にサービス全体への影響が軽減されます。この機能を有効にするには、パラメータ[`lite-init-stats`](/tidb-configuration-file.md#lite-init-stats-new-in-v710) ～ `true`を設定します。

    TiDBの起動時、初期統計情報が完全にロードされる前に実行されるSQL文は、最適ではない実行プランを持つ可能性があり、パフォーマンスの問題を引き起こす可能性があります。このような問題を回避するために、TiDB v7.1.0では構成パラメータ[`force-init-stats`](/tidb-configuration-file.md#force-init-stats-new-in-v657-and-v710)が導入されました。このオプションを使用すると、起動時に統計情報の初期化が完了した後にのみTiDBがサービスを提供するかどうかを制御できます。このパラメータはデフォルトで無効になっています。

    詳細については[ドキュメント](/statistics.md#load-statistics)参照してください。

-   TiCDCは、単一行データのデータ整合性検証機能をサポートしています[＃8718](https://github.com/pingcap/tiflow/issues/8718) [＃42747](https://github.com/pingcap/tidb/issues/42747) @ [3エースショーハンド](https://github.com/3AceShowHand) @ [ジグアン](https://github.com/zyguan)

    v7.1.0以降、TiCDCはデータ整合性検証機能を導入しました。この機能は、チェックサムアルゴリズムを用いて単一行データの整合性を検証します。この機能は、TiDBからデータを書き込み、TiCDCを介して複製し、Kafkaクラスターに書き込むプロセスでエラーが発生していないかどうかを検証するのに役立ちます。データ整合性検証機能は、Kafkaをダウンストリームとして使用するチェンジフィードのみをサポートし、現在はAvroプロトコルをサポートしています。

    詳細については[ドキュメント](/ticdc/ticdc-integrity-check.md)参照してください。

-   TiCDCはDDLレプリケーション操作[＃8686](https://github.com/pingcap/tiflow/issues/8686)を[ハイラスティン](https://github.com/Rustin170506)で最適化します

    バージョン7.1.0より前のバージョンでは、大規模なテーブルのすべての行に影響を及ぼすDDL操作（列の追加や削除など）を実行すると、TiCDCのレプリケーションレイテンシーが大幅に増加していました。バージョン7.1.0以降、TiCDCはこのレプリケーション操作を最適化し、DDL操作が下流のレイテンシーに与える影響を軽減します。

    詳細については[ドキュメント](/ticdc/ticdc-faq.md#does-ticdc-replicate-data-changes-caused-by-lossy-ddl-operations-to-the-downstream)参照してください。

-   TiB レベルのデータをインポートする際のTiDB Lightningの安定性を向上[＃43510](https://github.com/pingcap/tidb/issues/43510) [＃43657](https://github.com/pingcap/tidb/issues/43657) @ [D3ハンター](https://github.com/D3Hunter) @ [ランス6716](https://github.com/lance6716)

    v7.1.0 以降、 TiDB Lightning には、TiB レベルのデータのインポート時の安定性を向上させるための 4 つの構成項目が追加されました。

    -   `tikv-importer.region-split-batch-size` 、バッチでリージョンを分割する際のリージョンの数を制御します。デフォルト値は`4096`です。
    -   `tikv-importer.region-split-concurrency`リージョン分割時の同時実行を制御します。デフォルト値は CPU コア数です。
    -   `tikv-importer.region-check-backoff-limit` 、分割および分散処理後にリージョンがオンラインになるまでの再試行回数を制御します。デフォルト値は`1800`で、最大再試行間隔は 2 秒です。再試行の間にいずれかのリージョンがオンラインになった場合、再試行回数は増加しません。
    -   `tikv-importer.pause-pd-scheduler-scope` 、TiDB Lightning がPD スケジューリングを一時停止する範囲を制御します。値のオプションは`"table"`と`"global"`です。デフォルト値は`"table"`です。v6.1.0 より前のバージョンの TiDB では、データインポート中にグローバルスケジューリングを一時停止する`"global"`オプションのみを設定できます。v6.1.0 以降では、ターゲットテーブルデータが格納されているリージョンのスケジューリングのみが一時停止される`"table"`オプションがサポートされています。データ量が多いシナリオでは、安定性を向上させるために、この設定項目を`"global"`に設定することをお勧めします。

    詳細については[ドキュメント](/tidb-lightning/tidb-lightning-configuration.md)参照してください。

### SQL {#sql}

-   `INSERT INTO SELECT`ステートメントを使用したTiFlashクエリ結果の保存をサポート (GA) [＃37515](https://github.com/pingcap/tidb/issues/37515) @ [ゲンリチ](https://github.com/gengliqi)

    TiDB v6.5.0以降、 `INSERT INTO SELECT`ステートメントの`SELECT`句（分析クエリ）をTiFlashにプッシュダウンできるようになりました。これにより、 TiFlashクエリの結果を`INSERT INTO`で指定されたTiDBテーブルに簡単に保存し、さらに分析することができます。これは、結果のキャッシュ（つまり、結果のマテリアライゼーション）として機能します。

    この機能はバージョン7.1.0で一般公開されています。3 `INSERT INTO SELECT`の`SELECT`節の実行中に、オプティマイザーは[SQLモード](/sql-mode.md)とTiFlashレプリカのコスト見積もりに基づいて、クエリをTiFlashにプッシュダウンするかどうかをインテリジェントに決定できます。そのため、実験的段階で導入された`tidb_enable_tiflash_read_for_write_stmt`システム変数は非推奨となりました。TiFlashの`INSERT INTO SELECT`文の計算ルールは`STRICT SQL Mode`要件を満たしていないため、TiDBは現在のセッションの[SQLモード](/sql-mode.md)が厳密でない場合にのみ、 `INSERT INTO SELECT`文の`SELECT`節をTiFlashにプッシュダウンすることを許可します。つまり、 `sql_mode`値に`STRICT_TRANS_TABLES`と`STRICT_ALL_TABLES`含まれません。

    詳細については[ドキュメント](/tiflash/tiflash-results-materialization.md)参照してください。

-   MySQL互換のマルチ値インデックスが一般提供（GA）される[＃39592](https://github.com/pingcap/tidb/issues/39592) @ [ションジウェイ](https://github.com/xiongjiwei) @ [qw4990](https://github.com/qw4990) @ [ヤンケオ](https://github.com/YangKeao)

    JSON列内の配列の値をフィルタリングすることは一般的な操作ですが、通常のインデックスではこのような操作を高速化できません。配列に複数値インデックスを作成すると、フィルタリングのパフォーマンスが大幅に向上します。JSON列の配列に複数値インデックスがある場合、 `MEMBER OF()` `JSON_CONTAINS()` `JSON_OVERLAPS()`で検索条件をフィルタリングする際に複数値インデックスを使用できます。これにより、I/O消費が削減され、操作速度が向上します。

    バージョン7.1.0では、多値インデックス機能が一般提供（GA）されました。より包括的なデータ型をサポートし、TiDBツールとの互換性も備えています。多値インデックスを使用することで、本番環境におけるJSON配列の検索操作を高速化できます。

    詳細については[ドキュメント](/sql-statements/sql-statement-create-index.md#multi-valued-indexes)参照してください。

-   ハッシュおよびキーパーティションテーブルのパーティション管理を改善[＃42728](https://github.com/pingcap/tidb/issues/42728) @ [ミョンス](https://github.com/mjonss)

    v7.1.0より前のTiDBでは、ハッシュおよびキーでパーティション化されたテーブルは、パーティション管理ステートメント`TRUNCATE PARTITION`をサポートしていました。v7.1.0以降では、ハッシュおよびキーでパーティション化されたテーブルは、パーティション管理ステートメント`ADD PARTITION`および`COALESCE PARTITION`サポートするようになりました。そのため、必要に応じてハッシュおよびキーでパーティション化されたテーブルのパーティション数を柔軟に調整できます。例えば、 `ADD PARTITION`ステートメントでパーティション数を増やしたり、 `COALESCE PARTITION`ステートメントでパーティション数を減らしたりすることができます。

    詳細については[ドキュメント](/partitioned-table.md#manage-hash-and-key-partitions)参照してください。

-   範囲INTERVALパーティションの構文が一般公開（GA） [＃35683](https://github.com/pingcap/tidb/issues/35683) @ [ミョンス](https://github.com/mjonss)になります

    バージョン6.3.0で導入されたRange INTERVALパーティショニングの構文がGAになりました。この構文を使用すると、すべてのパーティションを列挙することなく、任意の間隔でRangeパーティショニングを定義できるため、RangeパーティショニングのDDL文の長さが大幅に短縮されます。この構文は、従来のRangeパーティショニングの構文と同等です。

    詳細については[ドキュメント](/partitioned-table.md#range-interval-partitioning)参照してください。

-   生成された列は[bb7133](https://github.com/bb7133)に一般公開（GA）されます

    生成列はデータベースにとって貴重な機能です。テーブル作成時に、列の値がユーザーによって明示的に挿入または更新されるのではなく、テーブル内の他の列の値に基づいて計算されるように定義できます。この生成列は、仮想列または保存列のいずれかになります。TiDBは以前のバージョンからMySQL互換の生成列をサポートしており、この機能はv7.1.0でGAになります。

    生成列を使用すると、TiDBのMySQLとの互換性が向上し、MySQLからの移行プロセスが簡素化されます。また、データメンテナンスの複雑さが軽減され、データの一貫性とクエリ効率も向上します。

    詳細については[ドキュメント](/generated-columns.md)参照してください。

### DB操作 {#db-operations}

-   DDL 操作を手動でキャンセルせずに、スムーズなクラスタ アップグレードをサポート (実験的) [＃39751](https://github.com/pingcap/tidb/issues/39751) @ [ジムララ](https://github.com/zimulala)

    TiDB v7.1.0 より前のバージョンでは、クラスターをアップグレードするには、アップグレード前に実行中またはキューに入れられた DDL タスクを手動でキャンセルし、アップグレード後に再度追加する必要があります。

    よりスムーズなアップグレードを実現するために、TiDB v7.1.0 では DDL タスクの自動一時停止と再開をサポートしています。v7.1.0 以降では、事前に DDL タスクを手動でキャンセルすることなく、クラスターをアップグレードできます。TiDB は、アップグレード前に実行中またはキューに入っているユーザー DDL タスクを自動的に一時停止し、ローリングアップグレード後にこれらのタスクを再開するため、TiDB クラスターのアップグレードが容易になります。

    詳細については[ドキュメント](/smooth-upgrade-tidb.md)参照してください。

### 可観測性 {#observability}

-   オプティマイザ診断情報の強化[＃43122](https://github.com/pingcap/tidb/issues/43122) @ [時間と運命](https://github.com/time-and-fate)

    SQLパフォーマンス診断では、十分な情報を取得することが鍵となります。TiDB v7.1.0では、様々な診断ツールにオプティマイザ実行時情報が追加され、実行プランの選択方法に関するより詳細な情報を提供し、SQLパフォーマンスの問題のトラブルシューティングを支援します。新しい情報には以下が含まれます。

    -   [`PLAN REPLAYER`](/sql-plan-replayer.md)の出力は`debug_trace.json` 。
    -   [`EXPLAIN`](/explain-walkthrough.md)の出力における`operator info`部分的な統計詳細。
    -   [遅いクエリ](/identify-slow-queries.md)の`Stats`フィールドの部分的な統計詳細。

    詳細については、 [`PLAN REPLAYER`を使用してクラスターのオンサイト情報を保存および復元します](/sql-plan-replayer.md) 、 [`EXPLAIN`ウォークスルー](/explain-walkthrough.md) 、 [遅いクエリを特定する](/identify-slow-queries.md)参照してください。

### Security {#security}

-   TiFlashシステムテーブル情報のクエリに使用されるインターフェースを[＃6941](https://github.com/pingcap/tiflash/issues/6941) @ [フロービーハッピー](https://github.com/flowbehappy)に置き換えます

    v7.1.0 以降、TiDB の[`INFORMATION_SCHEMA.TIFLASH_TABLES`](/information-schema/information-schema-tiflash-tables.md)および[`INFORMATION_SCHEMA.TIFLASH_SEGMENTS`](/information-schema/information-schema-tiflash-segments.md)システム テーブルのクエリ サービスを提供する際に、 TiFlash はHTTP ポートではなく gRPC ポートを使用するため、HTTP サービスのセキュリティ リスクを回避できます。

-   LDAP認証[＃43580](https://github.com/pingcap/tidb/issues/43580) @ [ヤンケオ](https://github.com/YangKeao)サポート

    v7.1.0 以降、TiDB は LDAP 認証をサポートし、 `authentication_ldap_sasl`と`authentication_ldap_simple` 2 つの認証プラグインを提供します。

    詳細については[ドキュメント](/security-compatibility-with-mysql.md)参照してください。

-   データベース監査機能の強化（エンタープライズエディション）

    バージョン 7.1.0 では、TiDB Enterprise Edition のデータベース監査機能が強化され、その機能が大幅に拡張され、ユーザー エクスペリエンスが向上して、企業のデータベース セキュリティ コンプライアンスのニーズに対応できるようになりました。

    -   より詳細な監査イベント定義とよりきめ細かな監査設定のために、「フィルター」と「ルール」の概念を導入します。
    -   JSON 形式でのルールの定義をサポートし、よりユーザーフレンドリーな構成方法を提供します。
    -   自動ログローテーションとスペース管理関数を追加し、保持時間とログサイズの 2 つの次元でのログローテーションの構成をサポートします。
    -   監査ログをTEXTと JSON 形式の両方で出力できるようにサポートし、サードパーティ ツールとの統合を容易にします。
    -   監査ログの編集をサポートします。すべてのリテラルを置き換えてセキュリティを強化できます。

    データベース監査は、TiDB Enterprise Editionの重要な機能です。この機能は、企業のデータセキュリティとコンプライアンスを確保するための強力な監視・監査ツールを提供します。企業の管理者は、データベース操作の発生源と影響を追跡し、不正なデータ盗難や改ざんを防止することができます。さらに、データベース監査は、企業が様々な規制やコンプライアンス要件を満たし、法的および倫理的コンプライアンスを確保するのにも役立ちます。この機能は、企業の情報セキュリティにとって重要なアプリケーション価値を持っています。

    詳細については、 [ユーザーガイド](https://static.pingcap.com/files/2023/09/18204824/TiDB-Database-Auditing-User-Guide1.pdf)ご覧ください。この機能はTiDB Enterprise Editionに含まれています。この機能を使用するには、 [TiDBエンタープライズ](https://www.pingcap.com/tidb-enterprise)ページに移動してTiDB Enterprise Editionを入手してください。

## 互換性の変更 {#compatibility-changes}

> **注記：**
>
> このセクションでは、v7.0.0から最新バージョン（v7.1.0）にアップグレードする際に知っておくべき互換性の変更点について説明します。v6.6.0以前のバージョンから最新バージョンにアップグレードする場合は、中間バージョンで導入された互換性の変更点も確認する必要があるかもしれません。

### 行動の変化 {#behavior-changes}

-   セキュリティを強化するために、 TiFlashはHTTPサービスポート（デフォルト`8123` ）を廃止し、代わりにgRPCポートを使用します。

    TiFlashを v7.1.0 にアップグレードした場合、TiDB を v7.1.0 にアップグレードする際に、TiDB はTiFlashシステム テーブル ( [`INFORMATION_SCHEMA.TIFLASH_TABLES`](/information-schema/information-schema-tiflash-tables.md)と[`INFORMATION_SCHEMA.TIFLASH_SEGMENTS`](/information-schema/information-schema-tiflash-segments.md) ) を読み取ることができません。

-   TiDB バージョン v6.2.0 から v7.0.0 のTiDB Lightning は、 TiDB クラスターのバージョンに基づいてグローバル スケジューリングを一時停止するかどうかを決定します。TiDB クラスター バージョン &gt;= v6.1.0 の場合、スケジューリングはターゲット テーブル データを格納するリージョンに対してのみ一時停止され、ターゲット テーブルのインポートが完了すると再開されます。その他のバージョンの場合、 TiDB Lightning はグローバル スケジューリングを一時停止します。TiDB v7.1.0 以降では、 [`pause-pd-scheduler-scope`](/tidb-lightning/tidb-lightning-configuration.md)構成することで、グローバル スケジューリングを一時停止するかどうかを制御できます。デフォルトでは、 TiDB Lightning はターゲット テーブル データを格納するリージョンのスケジューリングを一時停止します。ターゲット クラスターのバージョンが v6.1.0 より前の場合、エラーが発生します。この場合、パラメータの値を`"global"`に変更して再試行できます。

-   TiDB v7.1.0で[`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-cluster.md)使用すると、FLASHBACK操作が完了した後も、一部のリージョンがFLASHBACKプロセスに残る可能性があります。v7.1.0ではこの機能の使用を避けることをお勧めします。詳細については、問題[＃44292](https://github.com/pingcap/tidb/issues/44292)参照してください。この問題が発生した場合は、機能[TiDBスナップショットのバックアップと復元](/br/br-snapshot-guide.md)を使用してデータをリストアできます。

### システム変数 {#system-variables}

| 変数名                                                                                                                                     | タイプを変更   | 説明                                                                                                                                                                                                                                                                                                                                                                                              |
| --------------------------------------------------------------------------------------------------------------------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`tidb_enable_tiflash_read_for_write_stmt`](/system-variables.md#tidb_enable_tiflash_read_for_write_stmt-new-in-v630)                   | 非推奨      | デフォルト値を`OFF`から`ON`に変更します。 [`tidb_allow_mpp = ON`](/system-variables.md#tidb_allow_mpp-new-in-v50)場合、オプティマイザーは[SQLモード](/sql-mode.md)とTiFlashレプリカのコスト見積もりに基づいて、クエリをTiFlashにプッシュダウンするかどうかをインテリジェントに決定します。                                                                                                                                                                                          |
| [`tidb_non_prepared_plan_cache_size`](/system-variables.md#tidb_non_prepared_plan_cache_size)                                           | 非推奨      | バージョン7.1.0以降、このシステム変数は非推奨となりました。1 [`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-new-in-v710)指定すると、キャッシュできるプランの最大数を制御できます。                                                                                                                                                                                                                                  |
| [`tidb_prepared_plan_cache_size`](/system-variables.md#tidb_prepared_plan_cache_size-new-in-v610)                                       | 非推奨      | バージョン7.1.0以降、このシステム変数は非推奨となりました。1 [`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-new-in-v710)指定すると、キャッシュできるプランの最大数を制御できます。                                                                                                                                                                                                                                  |
| `tidb_ddl_distribute_reorg`                                                                                                             | 削除済み     | この変数の名前は[`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710)に変更されます。                                                                                                                                                                                                                                                                                               |
| [`default_authentication_plugin`](/system-variables.md#default_authentication_plugin)                                                   | 修正済み     | 2 つの新しい値オプション`authentication_ldap_sasl`と`authentication_ldap_simple`導入されました。                                                                                                                                                                                                                                                                                                                    |
| [`tidb_load_based_replica_read_threshold`](/system-variables.md#tidb_load_based_replica_read_threshold-new-in-v700)                     | 修正済み     | バージョン7.1.0以降で有効になり、負荷ベースのレプリカ読み取りをトリガーするためのしきい値を制御します。追加のテストを経て、デフォルト値を`"0s"`から`"1s"`に変更します。                                                                                                                                                                                                                                                                                                    |
| [`tidb_opt_enable_late_materialization`](/system-variables.md#tidb_opt_enable_late_materialization-new-in-v700)                         | 修正済み     | デフォルト値を`OFF`から`ON`に変更します。これは、 TiFlash の遅延マテリアライゼーション機能がデフォルトで有効になっていることを意味します。                                                                                                                                                                                                                                                                                                                  |
| [`authentication_ldap_sasl_auth_method_name`](/system-variables.md#authentication_ldap_sasl_auth_method_name-new-in-v710)               | 新しく追加された | LDAP SASL 認証における認証方法名を指定します。                                                                                                                                                                                                                                                                                                                                                                    |
| [`authentication_ldap_sasl_bind_base_dn`](/system-variables.md#authentication_ldap_sasl_bind_base_dn-new-in-v710)                       | 新しく追加された | LDAP SASL認証における検索ツリー内の検索範囲を制限します。ユーザーが`AS ...`句なしで作成された場合、TiDBはユーザー名に基づいてLDAPサーバー内の`dn`を自動的に検索します。                                                                                                                                                                                                                                                                                              |
| [`authentication_ldap_sasl_bind_root_dn`](/system-variables.md#authentication_ldap_sasl_bind_root_dn-new-in-v710)                       | 新しく追加された | LDAP SASL 認証でユーザーを検索するために LDAPサーバーにログインするために使用される`dn`指定します。                                                                                                                                                                                                                                                                                                                                     |
| [`authentication_ldap_sasl_bind_root_pwd`](/system-variables.md#authentication_ldap_sasl_bind_root_pwd-new-in-v710)                     | 新しく追加された | LDAP SASL 認証でユーザーを検索するために LDAPサーバーにログインするために使用されるパスワードを指定します。                                                                                                                                                                                                                                                                                                                                   |
| [`authentication_ldap_sasl_ca_path`](/system-variables.md#authentication_ldap_sasl_ca_path-new-in-v710)                                 | 新しく追加された | LDAP SASL 認証の StartTLS 接続用の証明機関ファイルの絶対パスを指定します。                                                                                                                                                                                                                                                                                                                                                 |
| [`authentication_ldap_sasl_init_pool_size`](/system-variables.md#authentication_ldap_sasl_init_pool_size-new-in-v710)                   | 新しく追加された | LDAP SASL 認証で LDAPサーバーへの接続プール内の初期接続を指定します。                                                                                                                                                                                                                                                                                                                                                      |
| [`authentication_ldap_sasl_max_pool_size`](/system-variables.md#authentication_ldap_sasl_max_pool_size-new-in-v710)                     | 新しく追加された | LDAP SASL 認証における LDAPサーバーへの接続プールの最大接続数を指定します。                                                                                                                                                                                                                                                                                                                                                   |
| [`authentication_ldap_sasl_server_host`](/system-variables.md#authentication_ldap_sasl_server_host-new-in-v710)                         | 新しく追加された | LDAP SASL 認証で LDAPサーバーホストを指定します。                                                                                                                                                                                                                                                                                                                                                                |
| [`authentication_ldap_sasl_server_port`](/system-variables.md#authentication_ldap_sasl_server_port-new-in-v710)                         | 新しく追加された | LDAP SASL 認証における LDAPサーバーのTCP/IP ポート番号を指定します。                                                                                                                                                                                                                                                                                                                                                   |
| [`authentication_ldap_sasl_tls`](/system-variables.md#authentication_ldap_sasl_tls-new-in-v710)                                         | 新しく追加された | プラグインによる LDAPサーバーへの接続が LDAP SASL 認証の StartTLS で保護されるかどうかを指定します。                                                                                                                                                                                                                                                                                                                                 |
| [`authentication_ldap_simple_auth_method_name`](/system-variables.md#authentication_ldap_simple_auth_method_name-new-in-v710)           | 新しく追加された | LDAP簡易認証における認証方式名を指定します。1のみサポートされます`SIMPLE`                                                                                                                                                                                                                                                                                                                                                     |
| [`authentication_ldap_simple_bind_base_dn`](/system-variables.md#authentication_ldap_simple_bind_base_dn-new-in-v710)                   | 新しく追加された | LDAP簡易認証における検索ツリー内の検索範囲を制限します。1 `AS ...`句を指定せずにユーザーが作成された場合、TiDBはユーザー名に基づいてLDAPサーバー内の`dn`を自動的に検索します。                                                                                                                                                                                                                                                                                            |
| [`authentication_ldap_simple_bind_root_dn`](/system-variables.md#authentication_ldap_simple_bind_root_dn-new-in-v710)                   | 新しく追加された | LDAP 簡易認証でユーザーを検索するために LDAPサーバーにログインするために使用される`dn`指定します。                                                                                                                                                                                                                                                                                                                                        |
| [`authentication_ldap_simple_bind_root_pwd`](/system-variables.md#authentication_ldap_simple_bind_root_pwd-new-in-v710)                 | 新しく追加された | LDAP 簡易認証でユーザーを検索するために LDAPサーバーにログインするために使用されるパスワードを指定します。                                                                                                                                                                                                                                                                                                                                      |
| [`authentication_ldap_simple_ca_path`](/system-variables.md#authentication_ldap_simple_ca_path-new-in-v710)                             | 新しく追加された | LDAP 簡易認証での StartTLS 接続用の証明機関ファイルの絶対パスを指定します。                                                                                                                                                                                                                                                                                                                                                   |
| [`authentication_ldap_simple_init_pool_size`](/system-variables.md#authentication_ldap_simple_init_pool_size-new-in-v710)               | 新しく追加された | LDAP 簡易認証で、LDAPサーバーへの接続プール内の初期接続を指定します。                                                                                                                                                                                                                                                                                                                                                         |
| [`authentication_ldap_simple_max_pool_size`](/system-variables.md#authentication_ldap_simple_max_pool_size-new-in-v710)                 | 新しく追加された | LDAP 簡易認証における LDAPサーバーへの接続プールの最大接続数を指定します。                                                                                                                                                                                                                                                                                                                                                      |
| [`authentication_ldap_simple_server_host`](/system-variables.md#authentication_ldap_simple_server_host-new-in-v710)                     | 新しく追加された | LDAP 簡易認証で LDAPサーバーホストを指定します。                                                                                                                                                                                                                                                                                                                                                                   |
| [`authentication_ldap_simple_server_port`](/system-variables.md#authentication_ldap_simple_server_port-new-in-v710)                     | 新しく追加された | LDAP 簡易認証における LDAPサーバーのTCP/IP ポート番号を指定します。                                                                                                                                                                                                                                                                                                                                                      |
| [`authentication_ldap_simple_tls`](/system-variables.md#authentication_ldap_simple_tls-new-in-v710)                                     | 新しく追加された | プラグインによる LDAPサーバーへの接続が LDAP 簡易認証で StartTLS を使用して保護されるかどうかを指定します。                                                                                                                                                                                                                                                                                                                                |
| [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710)                                                       | 新しく追加された | 分散実行フレームワーク（DXF）を有効にするかどうかを制御します。DXFを有効にすると、DDL、インポート、その他のサポートされているDXFタスクが、クラスター内の複数のTiDBノードによって共同で実行されます。この変数は`tidb_ddl_distribute_reorg`から名前が変更されました。                                                                                                                                                                                                                                         |
| [`tidb_enable_non_prepared_plan_cache_for_dml`](/system-variables.md#tidb_enable_non_prepared_plan_cache_for_dml-new-in-v710)           | 新しく追加された | DML ステートメントに対して[準備されていないプランキャッシュ](/sql-non-prepared-plan-cache.md)機能を有効にするかどうかを制御します。                                                                                                                                                                                                                                                                                                           |
| [`tidb_enable_row_level_checksum`](/system-variables.md#tidb_enable_row_level_checksum-new-in-v710)                                     | 新しく追加された | 単一行データ機能に対して TiCDC データ整合性検証を有効にするかどうかを制御します。                                                                                                                                                                                                                                                                                                                                                    |
| [`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-new-in-v653-and-v710)                                                | 新しく追加された | この変数は、オプティマイザをより細かく制御し、オプティマイザの動作の変更によって引き起こされるアップグレード後のパフォーマンスの低下を防ぐのに役立ちます。                                                                                                                                                                                                                                                                                                                   |
| [`tidb_plan_cache_invalidation_on_fresh_stats`](/system-variables.md#tidb_plan_cache_invalidation_on_fresh_stats-new-in-v710)           | 新しく追加された | 関連テーブルの統計が更新されたときにプラン キャッシュを自動的に無効にするかどうかを制御します。                                                                                                                                                                                                                                                                                                                                                |
| [`tidb_plan_cache_max_plan_size`](/system-variables.md#tidb_plan_cache_max_plan_size-new-in-v710)                                       | 新しく追加された | 準備済みプラン キャッシュまたは準備されていないプラン キャッシュにキャッシュできるプランの最大サイズを制御します。                                                                                                                                                                                                                                                                                                                                      |
| [`tidb_prefer_broadcast_join_by_exchange_data_size`](/system-variables.md#tidb_prefer_broadcast_join_by_exchange_data_size-new-in-v710) | 新しく追加された | ネットワーク転送のオーバーヘッドが最小となるアルゴリズムを使用するかどうかを制御します。この変数を有効にすると、TiDBはネットワークで交換されるデータのサイズをそれぞれ`Broadcast Hash Join`と`Shuffled Hash Join`で推定し、サイズが小さい方を選択します。この変数を有効にすると、 [`tidb_broadcast_join_threshold_count`](/system-variables.md#tidb_broadcast_join_threshold_count-new-in-v50)と[`tidb_broadcast_join_threshold_size`](/system-variables.md#tidb_broadcast_join_threshold_size-new-in-v50)無効になります。 |
| [`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-new-in-v710)                                         | 新しく追加された | キャッシュできるプランの最大数を制御します。準備済みプランのキャッシュと準備されていないプランのキャッシュは同じキャッシュを共有します。                                                                                                                                                                                                                                                                                                                            |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーションパラメータ                                                                                                                | タイプを変更   | 説明                                                                                                                                                                                 |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------ | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB           | [`performance.force-init-stats`](/tidb-configuration-file.md#force-init-stats-new-in-v657-and-v710)                            | 新しく追加された | TiDB の起動中にサービスを提供する前に、統計の初期化が完了するまで待機するかどうかを制御します。                                                                                                                                 |
| TiDB           | [`performance.lite-init-stats`](/tidb-configuration-file.md#lite-init-stats-new-in-v710)                                       | 新しく追加された | TiDB の起動時に軽量統計初期化を使用するかどうかを制御します。                                                                                                                                                  |
| TiDB           | [`log.timeout`](/tidb-configuration-file.md#timeout-new-in-v710)                                                               | 新しく追加された | TiDBにおけるログ書き込み操作のタイムアウトを設定します。ディスク障害によりログの書き込みができない場合、この設定項目によりTiDBプロセスがハングアップする代わりにpanicになる可能性があります。デフォルト値は`0`で、タイムアウトは設定されません。                                                   |
| TiKV           | [`region-compact-min-redundant-rows`](/tikv-configuration-file.md#region-compact-min-redundant-rows-new-in-v710)               | 新しく追加された | RocksDBの圧縮をトリガーするために必要な冗長MVCC行の数を設定します。デフォルト値は`50000`です。                                                                                                                           |
| TiKV           | [`region-compact-redundant-rows-percent`](/tikv-configuration-file.md#region-compact-redundant-rows-percent-new-in-v710)       | 新しく追加された | RocksDBの圧縮をトリガーするために必要な冗長MVCC行の割合を設定します。デフォルト値は`20`です。                                                                                                                             |
| TiKV           | [`split.byte-threshold`](/tikv-configuration-file.md#byte-threshold-new-in-v50)                                                | 修正済み     | [`region-split-size`](/tikv-configuration-file.md#region-split-size)が 4 GB 以上の場合、デフォルト値を`30MiB`から`100MiB`に変更します。                                                                   |
| TiKV           | [`split.qps-threshold`](/tikv-configuration-file.md#qps-threshold)                                                             | 修正済み     | [`region-split-size`](/tikv-configuration-file.md#region-split-size)が 4 GB 以上の場合、デフォルト値を`3000`から`7000`に変更します。                                                                      |
| TiKV           | [`split.region-cpu-overload-threshold-ratio`](/tikv-configuration-file.md#region-cpu-overload-threshold-ratio-new-in-v620)     | 修正済み     | [`region-split-size`](/tikv-configuration-file.md#region-split-size)が 4 GB 以上の場合、デフォルト値を`0.25`から`0.75`に変更します。                                                                      |
| TiKV           | [`region-compact-check-step`](/tikv-configuration-file.md#region-compact-check-step)                                           | 修正済み     | Partitioned Raft KVが有効な場合のデフォルト値を`100`から`5`に変更します（ `storage.engine="partitioned-raft-kv"` ）。                                                                                       |
| PD             | [`store-limit-version`](/pd-configuration-file.md#store-limit-version-new-in-v710)                                             | 新しく追加された | ストア制限のモードを制御します。値のオプションは`"v1"`と`"v2"`です。                                                                                                                                           |
| PD             | [`schedule.enable-diagnostic`](/pd-configuration-file.md#enable-diagnostic-new-in-v630)                                        | 修正済み     | デフォルト値を`false`から`true`に変更します。これは、スケジューラの診断機能がデフォルトで有効になることを意味します。                                                                                                                  |
| TiFlash        | `http_port`                                                                                                                    | 削除済み     | HTTP サービス ポート (デフォルト`8123` ) を廃止します。                                                                                                                                               |
| TiDB Lightning | [`tikv-importer.pause-pd-scheduler-scope`](/tidb-lightning/tidb-lightning-configuration.md)                                    | 新しく追加された | TiDB LightningがPDスケジュールを一時停止する範囲を制御します。デフォルト値は`"table"`で、値のオプションは`"global"`と`"table"`です。                                                                                           |
| TiDB Lightning | [`tikv-importer.region-check-backoff-limit`](/tidb-lightning/tidb-lightning-configuration.md)                                  | 新しく追加された | 分割および分散処理後にリージョンがオンラインになるまでの再試行回数を制御します。デフォルト値は`1800`です。最大再試行間隔は 2 秒です。再試行の間にいずれかのリージョンがオンラインになった場合、再試行回数は増加しません。                                                                  |
| TiDB Lightning | [`tikv-importer.region-split-batch-size`](/tidb-lightning/tidb-lightning-configuration.md)                                     | 新しく追加された | バッチでリージョンを分割する際のリージョン数を制御します。デフォルト値は`4096`です。                                                                                                                                      |
| TiDB Lightning | [`tikv-importer.region-split-concurrency`](/tidb-lightning/tidb-lightning-configuration.md)                                    | 新しく追加された | リージョンを分割する際の同時実行を制御します。デフォルト値はCPUコアの数です。                                                                                                                                           |
| TiCDC          | [`insecure-skip-verify`](/ticdc/ticdc-sink-to-kafka.md)                                                                        | 新しく追加された | Kafka にデータを複製するシナリオで TLS が有効になっている場合に認証アルゴリズムを設定するかどうかを制御します。                                                                                                                      |
| TiCDC          | [`integrity.corruption-handle-level`](/ticdc/ticdc-changefeed-config.md#cli-and-configuration-parameters-of-ticdc-changefeeds) | 新しく追加された | 単一行データのチェックサム検証に失敗した場合のChangefeedのログレベルを指定します。デフォルト値は`"warn"`です。値のオプションは`"warn"`と`"error"`です。                                                                                      |
| TiCDC          | [`integrity.integrity-check-level`](/ticdc/ticdc-changefeed-config.md#cli-and-configuration-parameters-of-ticdc-changefeeds)   | 新しく追加された | 単一行データのチェックサム検証を有効にするかどうかを制御します。デフォルト値は`"none"`で、この機能は無効です。                                                                                                                        |
| TiCDC          | [`sink.only-output-updated-columns`](/ticdc/ticdc-changefeed-config.md#cli-and-configuration-parameters-of-ticdc-changefeeds)  | 新しく追加された | 更新された列のみを出力するかどうかを制御します。デフォルト値は`false`です。                                                                                                                                          |
| TiCDC          | [`sink.enable-partition-separator`](/ticdc/ticdc-changefeed-config.md#cli-and-configuration-parameters-of-ticdc-changefeeds)   | 修正済み     | さらなるテストを経て、デフォルト値を`false`から`true`に変更しました。これは、テーブル内のパーティションがデフォルトで別々のディレクトリに保存されることを意味します。パーティション化されたテーブルをstorageサービスにレプリケーションする際にデータ損失が発生する可能性を回避するため、この値は`true`のままにしておくことをお勧めします。 |

## 改善点 {#improvements}

-   TiDB

    -   対応する列の個別値の数を、 `SHOW INDEX`結果[＃42227](https://github.com/pingcap/tidb/issues/42227) @ [ウィノロス](https://github.com/winoros)の Cardinality 列に表示します。
    -   TTLスキャンクエリがTiKVブロックキャッシュ[＃43206](https://github.com/pingcap/tidb/issues/43206) @ [lcwangchao](https://github.com/lcwangchao)に影響を与えないようにするには`SQL_NO_CACHE`使用します。
    -   `MAX_EXECUTION_TIME`に関連するエラーメッセージを改善し、MySQL [＃43031](https://github.com/pingcap/tidb/issues/43031) @ [ドヴェーデン](https://github.com/dveeden)と互換性を持たせます
    -   IndexLookUp [＃26166](https://github.com/pingcap/tidb/issues/26166) @ [定義2014](https://github.com/Defined2014)のパーティションテーブルでの MergeSort 演算子の使用をサポート
    -   MySQL [＃43576](https://github.com/pingcap/tidb/issues/43576) @ [asjdf](https://github.com/asjdf)と互換性を持たせるために`caching_sha2_password`拡張します

-   TiKV

    -   パーティション化されたRaft KV [＃14447](https://github.com/tikv/tikv/issues/14447) @ [スペードA-タン](https://github.com/SpadeA-Tang)を使用する場合、分割操作による書き込み QPS への影響を軽減します。
    -   パーティション化されたRaft KV [＃14581](https://github.com/tikv/tikv/issues/14581) @ [バッファフライ](https://github.com/bufferflies)を使用するときにスナップショットが占めるスペースを最適化します
    -   TiKV [＃12362](https://github.com/tikv/tikv/issues/12362) @ [cfzjywxk](https://github.com/cfzjywxk)でリクエストの処理の各段階のより詳細な時間情報を提供します
    -   ログバックアップ[＃13867](https://github.com/tikv/tikv/issues/13867) @ [ユジュンセン](https://github.com/YuJuncen)で PD をメタストアとして使用します

-   PD

    -   スナップショットの実行内容に基づいてストア制限のサイズを自動調整するコントローラを追加します。このコントローラを有効にするには、 `store-limit-version`を`v2` （実験的）に設定してください。有効にすると、スケールインまたはスケールアウトの速度を制御するために`store limit`設定を手動で調整する必要がなくなります（ [＃6147](https://github.com/tikv/pd/issues/6147) @ [バッファフライ](https://github.com/bufferflies) 。
    -   storageエンジンが raft-kv2 [＃6297](https://github.com/tikv/pd/issues/6297) @ [バッファフライ](https://github.com/bufferflies)の場合、ホットスポット スケジューラによって不安定な負荷のリージョンが頻繁にスケジュールされるのを避けるために、履歴負荷情報を追加します。
    -   リーダーのヘルスチェックメカニズムを追加します。etcdリーダーが配置されているPDサーバーがリーダーとして選出できない場合、PDはetcdリーダーをアクティブに切り替え、PDリーダーが[＃6403](https://github.com/tikv/pd/issues/6403) @ [ノルーシュ](https://github.com/nolouch)で利用可能であることを確認します。

-   TiFlash

    -   分散storageおよびコンピューティングアーキテクチャにおけるTiFlash のパフォーマンスと安定性を向上[＃6882](https://github.com/pingcap/tiflash/issues/6882) @ [ジェイソン・ファン](https://github.com/JaySon-Huang) @ [そよ風のような](https://github.com/breezewish) @ [ジンヘリン](https://github.com/JinheLin)
    -   小さい方のテーブルをビルド側[＃7280](https://github.com/pingcap/tiflash/issues/7280) @ [イービン87](https://github.com/yibin87)として選択することで、セミ結合またはアンチセミ結合でのクエリパフォーマンスの最適化をサポートします。
    -   デフォルト設定[＃7272](https://github.com/pingcap/tiflash/issues/7272) @ [そよ風のような](https://github.com/breezewish)でBRおよびTiDB LightningからTiFlashへのデータインポートのパフォーマンスを向上

-   ツール

    -   バックアップと復元 (BR)

        -   ログバックアップ[＃14433](https://github.com/tikv/tikv/issues/14433) @ [ジョッカウ](https://github.com/joccau)中に TiKV 構成項目`log-backup.max-flush-interval`変更することをサポート

    -   TiCDC

        -   オブジェクトstorageにデータを複製するシナリオでDDLイベントが発生した場合にディレクトリ構造を最適化する[＃8890](https://github.com/pingcap/tiflow/issues/8890) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)
        -   TiCDC レプリケーションタスクが失敗したときにアップストリームの GC TLS を設定する方法を最適化します[＃8403](https://github.com/pingcap/tiflow/issues/8403) @ [charleszheng44](https://github.com/charleszheng44)
        -   Kafka-on-Pulsar ダウンストリームへのデータ複製をサポート[＃8892](https://github.com/pingcap/tiflow/issues/8892) @ [ハイラスティン](https://github.com/Rustin170506)
        -   Kafka [＃8706](https://github.com/pingcap/tiflow/issues/8706) @ [スドジ](https://github.com/sdojjy)にデータを複製する際に更新が発生した後に変更された列のみを複製するためのオープンプロトコルプロトコルの使用をサポートします。
        -   下流の障害やその他のシナリオにおける TiCDC のエラー処理を最適化する[＃8657](https://github.com/pingcap/tiflow/issues/8657) @ [ヒック](https://github.com/hicqu)
        -   TLS [＃8867](https://github.com/pingcap/tiflow/issues/8867) @ [ハイラスティン](https://github.com/Rustin170506)を有効にするシナリオで認証アルゴリズムを設定するかどうかを制御する構成項目`insecure-skip-verify`を追加します。

    -   TiDB Lightning

        -   不均一なリージョン分布に関連する事前チェック項目の重大度レベルを`Critical`から`Warn`に変更して、ユーザーがデータをインポートできないようにします[＃42836](https://github.com/pingcap/tidb/issues/42836) @ [okJiang](https://github.com/okJiang)
        -   データのインポート中にエラーが発生した場合に再試行メカニズム[＃43291](https://github.com/pingcap/tidb/issues/43291) `unknown RPC` [D3ハンター](https://github.com/D3Hunter)
        -   リージョンジョブ[＃43682](https://github.com/pingcap/tidb/issues/43682) @ [ランス6716](https://github.com/lance6716)の再試行メカニズムを強化

## バグ修正 {#bug-fixes}

-   TiDB

    -   パーティション[＃42183](https://github.com/pingcap/tidb/issues/42183) @ [CbcWestwolf](https://github.com/CbcWestwolf)を再編成した後、手動で`ANALYZE TABLE`実行するプロンプトが表示されない問題を修正しました。
    -   `DROP TABLE`操作が実行されているときに`ADMIN SHOW DDL JOBS`結果にテーブル名が表示されない問題を修正[＃42268](https://github.com/pingcap/tidb/issues/42268) @ [天菜まお](https://github.com/tiancaiamao)
    -   Grafana モニタリング パネル[＃42562](https://github.com/pingcap/tidb/issues/42562) @ [ピンアンドビー](https://github.com/pingandb)で`Ignore Event Per Minute`と`Stats Cache LRU Cost`チャートが正常に表示されないことがある問題を修正しました
    -   `INFORMATION_SCHEMA.COLUMNS`テーブル[＃43379](https://github.com/pingcap/tidb/issues/43379) @ [bb7133](https://github.com/bb7133)をクエリするときに`ORDINAL_POSITION`列目が誤った結果を返す問題を修正しました
    -   キャッシュテーブルに新しい列が追加された後、列[＃42928](https://github.com/pingcap/tidb/issues/42928) @ [lqs](https://github.com/lqs)のデフォルト値ではなく値が`NULL`なる問題を修正しました。
    -   述語[＃43645](https://github.com/pingcap/tidb/issues/43645) @ [ウィノロス](https://github.com/winoros)をプッシュダウンするときに CTE 結果が正しくない問題を修正しました
    -   多数のパーティションとTiFlashレプリカ[＃42940](https://github.com/pingcap/tidb/issues/42940) @ [ミョンス](https://github.com/mjonss)を持つパーティション テーブルに対して`TRUNCATE TABLE`実行するときに書き込み競合によって発生する DDL 再試行の問題を修正しました。
    -   パーティションテーブル[＃41198](https://github.com/pingcap/tidb/issues/41198) [＃41200](https://github.com/pingcap/tidb/issues/41200) @ [ミョンス](https://github.com/mjonss)作成時に`SUBPARTITION`使用すると警告が表示されない問題を修正
    -   生成された列[＃40066](https://github.com/pingcap/tidb/issues/40066) @ [ジフハウス](https://github.com/jiyfhust)の値オーバーフローの問題を処理する際の MySQL との非互換性の問題を修正しました
    -   `REORGANIZE PARTITION`他の DDL 操作[＃42442](https://github.com/pingcap/tidb/issues/42442) @ [bb7133](https://github.com/bb7133)と同時に実行できない問題を修正
    -   DDL でパーティション再編成タスクをキャンセルすると、後続の DDL 操作が失敗する可能性がある問題を修正しました[＃42448](https://github.com/pingcap/tidb/issues/42448) @ [lcwangchao](https://github.com/lcwangchao)
    -   特定の条件下で削除操作のアサーションが正しくない問題を修正[＃42426](https://github.com/pingcap/tidb/issues/42426) @ [天菜まお](https://github.com/tiancaiamao)
    -   cgroup 情報の読み取りエラーにより、TiDBサーバーが起動できない問題を修正しました。エラー メッセージは「cgroup v1 からファイルメモリ.stat を読み取れません: /sys/メモリ.stat をオープンすると、そのようなファイルまたはディレクトリが見つかりません」です[＃42659](https://github.com/pingcap/tidb/issues/42659) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   グローバルインデックス[＃42312](https://github.com/pingcap/tidb/issues/42312) @ [L-メープル](https://github.com/L-maple)を持つパーティションテーブルの行のパーティションキーを更新するときに発生する`Duplicate Key`問題を修正しました
    -   TTLモニタリングパネルの`Scan Worker Time By Phase`チャートにデータ[＃42515](https://github.com/pingcap/tidb/issues/42515) @ [lcwangchao](https://github.com/lcwangchao)が表示されない問題を修正しました
    -   グローバルインデックスを持つパーティションテーブルに対する一部のクエリが誤った結果を返す問題を修正[＃41991](https://github.com/pingcap/tidb/issues/41991) [＃42065](https://github.com/pingcap/tidb/issues/42065) @ [L-メープル](https://github.com/L-maple)
    -   パーティションテーブル[＃42180](https://github.com/pingcap/tidb/issues/42180) @ [ミョンス](https://github.com/mjonss)の再編成プロセス中に一部のエラーログが表示される問題を修正しました
    -   `INFORMATION_SCHEMA.DDL_JOBS`テーブルの`QUERY`列目のデータ長が列定義[＃42440](https://github.com/pingcap/tidb/issues/42440) @ [天菜まお](https://github.com/tiancaiamao)を超える可能性がある問題を修正しました
    -   `INFORMATION_SCHEMA.CLUSTER_HARDWARE`テーブルでコンテナ[＃42851](https://github.com/pingcap/tidb/issues/42851) @ [ホーキングレイ](https://github.com/hawkingrei)に誤った値が表示される可能性がある問題を修正しました
    -   `ORDER BY` + `LIMIT` [＃43158](https://github.com/pingcap/tidb/issues/43158) @ [定義2014](https://github.com/Defined2014)を使用してパーティションテーブルをクエリすると誤った結果が返される問題を修正しました
    -   取り込み方法[＃42903](https://github.com/pingcap/tidb/issues/42903) @ [接線](https://github.com/tangenta)を使用して複数の DDL タスクが同時に実行される問題を修正しました
    -   `Limit` [＃24636](https://github.com/pingcap/tidb/issues/24636)を使用してパーティションテーブルをクエリしたときに返される誤った値を修正しました
    -   IPv6環境で誤ったTiDBアドレスが表示される問題を修正[＃43260](https://github.com/pingcap/tidb/issues/43260) @ [ネクスター](https://github.com/nexustar)
    -   システム変数`tidb_enable_tiflash_read_for_write_stmt`と`tidb_enable_exchange_partition` [＃43281](https://github.com/pingcap/tidb/issues/43281) @ [ゲンリチ](https://github.com/gengliqi)に誤った値が表示される問題を修正しました
    -   `tidb_scatter_region`有効になっている場合、パーティションが切り捨てられた後にリージョンが自動的に分割されない問題を修正[＃43174](https://github.com/pingcap/tidb/issues/43174) [＃43028](https://github.com/pingcap/tidb/issues/43028) @ [ジフハウス](https://github.com/jiyfhust)
    -   生成された列を持つテーブルにチェックを追加し、これらの列でサポートされていない DDL 操作のエラーを報告します[＃38988](https://github.com/pingcap/tidb/issues/38988) [＃24321](https://github.com/pingcap/tidb/issues/24321) @ [天菜まお](https://github.com/tiancaiamao)
    -   特定の型変換エラー[＃41730](https://github.com/pingcap/tidb/issues/41730) @ [ホーキングレイ](https://github.com/hawkingrei)でエラーメッセージが正しく表示されない問題を修正
    -   TiDBノードが正常にシャットダウンした後、このノードでトリガーされたDDLタスクがキャンセルされる問題を修正しました[＃43854](https://github.com/pingcap/tidb/issues/43854) @ [ジムララ](https://github.com/zimulala)
    -   PDメンバーのアドレスが変更されると、 `AUTO_INCREMENT`列目のIDの割り当てが長時間ブロックされる問題を修正[＃42643](https://github.com/pingcap/tidb/issues/42643) @ [天菜まお](https://github.com/tiancaiamao)
    -   DDL実行中に`GC lifetime is shorter than transaction duration`エラーを報告する問題を修正[＃40074](https://github.com/pingcap/tidb/issues/40074) @ [接線](https://github.com/tangenta)
    -   メタデータロックが予期せずDDL実行をブロックする問題を修正[＃43755](https://github.com/pingcap/tidb/issues/43755) @ [wjhuang2016](https://github.com/wjhuang2016)
    -   IPv6環境[＃43286](https://github.com/pingcap/tidb/issues/43286) @ [定義2014](https://github.com/Defined2014)でクラスターが一部のシステムビューを照会できない問題を修正
    -   動的プルーニングモード[＃43686](https://github.com/pingcap/tidb/issues/43686) @ [ミョンス](https://github.com/mjonss)で内部結合中にパーティションが見つからない問題を修正
    -   TiDBがテーブル[＃43392](https://github.com/pingcap/tidb/issues/43392) @ [グオシャオゲ](https://github.com/guo-shaoge)を分析するときに構文エラーを報告する問題を修正しました
    -   テーブル名の変更中に TiCDC が行の変更の一部を失う可能性がある問題を修正[＃43338](https://github.com/pingcap/tidb/issues/43338) @ [接線](https://github.com/tangenta)
    -   クライアントがカーソル読み取り[＃38116](https://github.com/pingcap/tidb/issues/38116) @ [ヤンケオ](https://github.com/YangKeao)を使用すると TiDBサーバーがクラッシュする問題を修正しました
    -   `ADMIN SHOW DDL JOBS LIMIT`誤った結果を返す問題を修正[＃42298](https://github.com/pingcap/tidb/issues/42298) @ [CbcWestwolf](https://github.com/CbcWestwolf)
    -   `UNION` [＃42563](https://github.com/pingcap/tidb/issues/42563) @ [lcwangchao](https://github.com/lcwangchao)でユニオンビューと一時テーブルをクエリするときに発生する TiDBpanic問題を修正しました。
    -   トランザクション[＃39664](https://github.com/pingcap/tidb/issues/39664) @ [天菜まお](https://github.com/tiancaiamao)で複数のステートメントをコミットするときにテーブル名の変更が有効にならない問題を修正しました
    -   時間変換[＃42439](https://github.com/pingcap/tidb/issues/42439) @ [qw4990](https://github.com/qw4990)中に準備済みプラン キャッシュと準備されていないプラン キャッシュの動作間の非互換性の問題を修正しました
    -   Decimal 型[＃43311](https://github.com/pingcap/tidb/issues/43311) @ [qw4990](https://github.com/qw4990)のプラン キャッシュによって発生する誤った結果を修正しました
    -   間違ったフィールドタイプチェック[＃42459](https://github.com/pingcap/tidb/issues/42459) @ [アイリンキッド](https://github.com/AilinKid)による、null 認識アンチ結合 (NAAJ) での TiDBpanic問題を修正しました。
    -   RC分離レベルでの悲観的トランザクションにおけるDML実行の失敗により、データとインデックス[＃43294](https://github.com/pingcap/tidb/issues/43294) @ [エキシウム](https://github.com/ekexium)間に不整合が発生する可能性がある問題を修正しました。
    -   極端なケースで、悲観的トランザクションの最初のステートメントが再試行されるときに、このトランザクションのロックを解決するとトランザクションの正確性に影響する可能性がある問題を修正しました[＃42937](https://github.com/pingcap/tidb/issues/42937) @ [ミョンケミンタ](https://github.com/MyonKeminta)
    -   GC がロック[＃43243](https://github.com/pingcap/tidb/issues/43243) @ [ミョンケミンタ](https://github.com/MyonKeminta)を解決するときに、まれに悲観的トランザクションの残余悲観的ロックがデータの正確性に影響を与える可能性がある問題を修正しました。
    -   `LOCK`から`PUT`への最適化により、特定のクエリ[＃28011](https://github.com/pingcap/tidb/issues/28011) @ [ジグアン](https://github.com/zyguan)で重複したデータが返される問題を修正しました。
    -   データが変更された場合、ユニークインデックスのロック動作がデータが変更されていない場合のロック動作と一致しない問題を修正しました[＃36438](https://github.com/pingcap/tidb/issues/36438) @ [ジグアン](https://github.com/zyguan)

-   TiKV

    -   `tidb_pessimistic_txn_fair_locking`有効にすると、極端なケースで、失敗した RPC 再試行によって期限切れになったリクエストが、ロック解決操作[＃14551](https://github.com/tikv/tikv/issues/14551) @ [ミョンケミンタ](https://github.com/MyonKeminta)中にデータの正確性に影響を与える可能性がある問題を修正しました。
    -   `tidb_pessimistic_txn_fair_locking`有効にすると、極端なケースで、失敗した RPC 再試行によって期限切れのリクエストが発生し、トランザクションの競合が無視され、トランザクションの一貫性[＃14311](https://github.com/tikv/tikv/issues/14311) @ [ミョンケミンタ](https://github.com/MyonKeminta)に影響する可能性がある問題を修正しました。
    -   暗号化キーIDの競合により古いキー[＃14585](https://github.com/tikv/tikv/issues/14585) @ [タボキ](https://github.com/tabokie)が削除される可能性がある問題を修正しました
    -   クラスタを以前のバージョンからv6.5以降のバージョン[＃14780](https://github.com/tikv/tikv/issues/14780) @ [ミョンケミンタ](https://github.com/MyonKeminta)にアップグレードしたときに、蓄積されたロックレコードによって引き起こされるパフォーマンス低下の問題を修正しました。
    -   PITRリカバリプロセス[＃14313](https://github.com/tikv/tikv/issues/14313) @ [ユジュンセン](https://github.com/YuJuncen)中に`raft entry is too large`エラーが発生する問題を修正
    -   PITRリカバリプロセス中に`log_batch` 2GBを超えるためTiKVがパニックになる問題を修正[＃13848](https://github.com/tikv/tikv/issues/13848) @ [ユジュンセン](https://github.com/YuJuncen)

-   PD

    -   TiKVパニック[＃6252](https://github.com/tikv/pd/issues/6252) @ [HuSharp](https://github.com/HuSharp)後にPD監視パネルの`low space store`の数字が異常になる問題を修正
    -   PDリーダースイッチ[＃6366](https://github.com/tikv/pd/issues/6366) @ [イモムクゲ](https://github.com/iosmanthus)後にリージョンヘルス監視データが削除される問題を修正
    -   ルールチェッカーが`schedule=deny`ラベル[＃6426](https://github.com/tikv/pd/issues/6426) @ [ノルーシュ](https://github.com/nolouch)の不健全な領域を修復できない問題を修正しました
    -   TiKVまたはTiFlashの再起動後に既存のラベルの一部が失われる問題を修正[＃6467](https://github.com/tikv/pd/issues/6467) @ [Jmポテト](https://github.com/JmPotato)
    -   レプリケーションモード[＃14704](https://github.com/tikv/tikv/issues/14704) @ [ノルーシュ](https://github.com/nolouch)の学習ノードがある場合、レプリケーションステータスを切り替えることができない問題を修正しました。

-   TiFlash

    -   遅延マテリアライゼーション[＃7455](https://github.com/pingcap/tiflash/issues/7455) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)を有効にした後に、 `TIMESTAMP`または`TIME`タイプのデータをクエリするとエラーが返される問題を修正しました。
    -   大規模な更新トランザクションにより、 TiFlash が繰り返しエラーを報告し、 [＃7316](https://github.com/pingcap/tiflash/issues/7316) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)を再起動する可能性がある問題を修正しました。

-   ツール

    -   バックアップと復元 (BR)

        -   クラスター[＃42973](https://github.com/pingcap/tidb/issues/42973) @ [ユジュンセン](https://github.com/YuJuncen)で TiKV ノードがクラッシュしたときにバックアップ速度が低下する問題を修正しました
        -   一部のケースでバックアップの失敗により不正確なエラーメッセージが表示される問題を修正[＃43236](https://github.com/pingcap/tidb/issues/43236) @ [ユジュンセン](https://github.com/YuJuncen)

    -   TiCDC

        -   TiCDC タイムゾーン設定[＃8798](https://github.com/pingcap/tiflow/issues/8798) @ [ハイラスティン](https://github.com/Rustin170506)の問題を修正
        -   PDアドレスまたはリーダーに障害が発生したときにTiCDCが自動的に回復できない問題を修正[＃8812](https://github.com/pingcap/tiflow/issues/8812) [＃8877](https://github.com/pingcap/tiflow/issues/8877) @ [アズドンメン](https://github.com/asddongmen)
        -   上流の TiKV ノードの 1 つが[＃8858](https://github.com/pingcap/tiflow/issues/8858) @ [ヒック](https://github.com/hicqu)でクラッシュするとチェックポイントの遅延が増加する問題を修正しました
        -   オブジェクトstorageにデータを複製する際に、上流の`EXCHANGE PARTITION`操作が下流の[＃8914](https://github.com/pingcap/tiflow/issues/8914) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)に正しく複製されない問題を修正しました。
        -   一部の特殊なシナリオでソートコンポーネントの過剰なメモリ使用によって引き起こされる OOM 問題を修正[＃8974](https://github.com/pingcap/tiflow/issues/8974) @ [ヒック](https://github.com/hicqu)
        -   下流の Kafka シンクがローリング再起動されたときに発生する TiCDC ノードpanicを修正しました[＃9023](https://github.com/pingcap/tiflow/issues/9023) @ [アズドンメン](https://github.com/asddongmen)

    -   TiDB データ移行 (DM)

        -   レプリケーション[＃7028](https://github.com/pingcap/tiflow/issues/7028) @ [ランス6716](https://github.com/lance6716)中に latin1 データが破損する可能性がある問題を修正しました

    -   TiDBDumpling

        -   `UNSIGNED INTEGER`型の主キーがチャンク[＃42620](https://github.com/pingcap/tidb/issues/42620) @ [リチュンジュ](https://github.com/lichunzhu)分割に使用できない問題を修正しました
        -   `--output-file-template`誤って[＃42391](https://github.com/pingcap/tidb/issues/42391) @ [リチュンジュ](https://github.com/lichunzhu)に設定されている場合に TiDB Dumpling がpanic可能性がある問題を修正しました

    -   TiDBBinlog

        -   失敗したDDL文[＃1228](https://github.com/pingcap/tidb-binlog/issues/1228) @ [okJiang](https://github.com/okJiang)に遭遇したときにエラーが発生する可能性がある問題を修正しました

    -   TiDB Lightning

        -   データインポート[＃42456](https://github.com/pingcap/tidb/issues/42456) @ [ランス6716](https://github.com/lance6716)中のパフォーマンス低下の問題を修正
        -   大量のデータをインポートする際の`write to tikv with no leader returned`の問題を修正[＃43055](https://github.com/pingcap/tidb/issues/43055) @ [ランス6716](https://github.com/lance6716)
        -   データインポート[＃43197](https://github.com/pingcap/tidb/issues/43197) @ [D3ハンター](https://github.com/D3Hunter)中にログが`keys within region is empty, skip doIngest`過剰になる問題を修正
        -   部分書き込み[＃43363](https://github.com/pingcap/tidb/issues/43363) @ [ランス6716](https://github.com/lance6716)中にpanicが発生する可能性がある問題を修正
        -   幅の広いテーブル[＃43728](https://github.com/pingcap/tidb/issues/43728) @ [D3ハンター](https://github.com/D3Hunter)をインポートするときに OOM が発生する可能性がある問題を修正しました
        -   TiDB Lightning Grafanaダッシュボード[＃43357](https://github.com/pingcap/tidb/issues/43357) @ [リチュンジュ](https://github.com/lichunzhu)でデータが欠落する問題を修正
        -   `keyspace-name` [＃43684](https://github.com/pingcap/tidb/issues/43684) @ [沢民州](https://github.com/zeminzhou)の設定が間違っているためにインポートが失敗する問題を修正しました
        -   範囲部分書き込み中にデータのインポートがスキップされる可能性がある問題を修正[＃43768](https://github.com/pingcap/tidb/issues/43768) @ [ランス6716](https://github.com/lance6716)

## パフォーマンステスト {#performance-test}

TiDB v7.1.0 のパフォーマンスについては、 TiDB Cloud Dedicated クラスターの[TPC-Cパフォーマンステストレポート](https://docs.pingcap.com/tidbcloud/v7.1.0-performance-benchmarking-with-tpcc)と[Sysbenchパフォーマンステストレポート](https://docs.pingcap.com/tidbcloud/v7.1.0-performance-benchmarking-with-sysbench)参照してください。

## 寄稿者 {#contributors}

TiDB コミュニティからの以下の貢献者に感謝いたします。

-   [ブラックティア23](https://github.com/blacktear23)
-   [イーサフロー](https://github.com/ethercflow)
-   [ヒヒフフ](https://github.com/hihihuhu)
-   [ジフハウス](https://github.com/jiyfhust)
-   [L-メープル](https://github.com/L-maple)
-   [lqs](https://github.com/lqs)
-   [ピンアンドビー](https://github.com/pingandb)
-   [ヨークヘレン](https://github.com/yorkhellen)
-   [ユジアリスタ](https://github.com/yujiarista) (初回投稿者)
