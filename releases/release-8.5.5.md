---
title: TiDB 8.5.5 Release Notes
summary: TiDB 8.5.5 の機能、互換性の変更点、改善点、およびバグ修正について学びましょう。
---

# TiDB 8.5.5 リリースノート {#tidb-8-5-5-release-notes}

発売日：2026年1月15日

TiDBバージョン：8.5.5

クイックアクセス： [クイックスタート](https://docs.pingcap.com/tidb/v8.5/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v8.5/production-deployment-using-tiup)

## 特徴 {#features}

### パフォーマンス {#performance}

-   特定の損失を伴う DDL 操作 ( `BIGINT → INT`および`CHAR(120) → VARCHAR(60)`など) に対して大幅なパフォーマンス改善を導入します。データ切り捨てが発生しない場合、これらの操作の実行時間は数時間から数分、数秒、あるいはミリ秒に短縮され、数万倍から数十万倍のパフォーマンス向上を実現します[#63366](https://github.com/pingcap/tidb/issues/63366) @[wjhuang2016](https://github.com/wjhuang2016) 、 @[tangenta](https://github.com/tangenta) 、 @[fzzf678](https://github.com/fzzf678)

    最適化戦略は以下のとおりです。

    -   厳密なSQLモードでは、TiDBは型​​変換中に発生する可能性のあるデータ切り捨てのリスクを事前にチェックします。
    -   データ切り捨てのリスクが検出されない場合、TiDBはメタデータのみを更新し、可能な限りインデックスの再構築を回避します。
    -   インデックスの再構築が必要な場合、TiDBはより効率的な取り込みプロセスを使用することで、インデックス再構築のパフォーマンスを大幅に向上させます。

    以下の表は、114 GiB のデータと 6 億行のデータを含むテーブルに対するベンチマーク テストに基づいたパフォーマンス改善の例を示しています。テスト クラスタは、3 つの TiDB ノード、6 つの TiKV ノード、および 1 つの PD ノードで構成されています。すべてのノードは、16 個の CPU コアと 32 GiB のメモリで構成されています。

    | シナリオ      | 操作タイプ                     | 最適化前   | 最適化後   | パフォーマンスの向上 |
    | --------- | ------------------------- | ------ | ------ | ---------- |
    | インデックスなし列 | `BIGINT → INT`            | 2時間34分 | 1分5秒   | 142倍速い     |
    | インデックス付き列 | `BIGINT → INT`            | 6時間25分 | 0.05秒  | 46万倍高速     |
    | インデックス付き列 | `CHAR(120) → VARCHAR(60)` | 7時間16分 | 12分56秒 | 34倍速い      |

    なお、上記のテスト結果は、DDL実行中にデータ切り捨てが発生しないという条件に基づいています。これらの最適化は、符号付き整数型と符号なし整数型間の変換、文字セット間の変換、またはTiFlashレプリカを持つテーブルには適用されません。

    詳細については、 [ドキュメント](/sql-statements/sql-statement-modify-column.md)参照してください。

-   外部キーが多数存在するシナリオにおけるDDLパフォーマンスを向上させ、論理DDLパフォーマンスを最大25倍向上させます[#61126](https://github.com/pingcap/tidb/issues/61126) @[GMHDBJD](https://github.com/GMHDBJD)

    バージョン8.5.5より前のバージョンでは、超大規模テーブル（例えば、外部キーを持つ数十万のテーブルを含む、合計1,000万のテーブルを持つクラスタなど）を扱うシナリオにおいて、論理DDL操作（テーブルの作成や列の追加など）のパフォーマンスが約4QPSまで低下することがありました。これは、マルチテナントSaaS環境における運用効率の低下につながっていました。

    TiDB v8.5.5 はこれらのシナリオを最適化します。テスト結果によると、1,000 万テーブル（外部キーを持つテーブル 20 万テーブルを含む）という極限環境においても、論理 DDL 処理性能は一貫して 100 QPS を維持します。これは以前のバージョンと比較して 25 倍向上しており、超大規模クラスタの運用応答性を大幅に向上させます。

-   クエリパフォーマンスを向上させるために、インデックス検索をTiKVにプッシュダウンする機能をサポートします[#62575](https://github.com/pingcap/tidb/issues/62575) @[lcwangchao](https://github.com/lcwangchao)

    バージョン8.5.5以降、TiDBは[オプティマイザのヒント](/optimizer-hints.md)使用して`IndexLookUp`演算子をTiKVノードにプッシュダウンすることをサポートしています。これにより、リモートプロシージャコール（RPC）の数が削減され、クエリのパフォーマンスが向上する可能性があります。実際のパフォーマンス向上はワークロードによって異なるため、検証にはテストが必要です。

    特定のテーブルに対してインデックス検索をTiKVにプッシュダウンするようにオプティマイザに明示的に指示するには、ヒント[`INDEX_LOOKUP_PUSHDOWN(t1_name, idx1_name [, idx2_name ...])`](https://docs.pingcap.com/tidb/v8.5/optimizer-hints#index_lookup_pushdownt1_name-idx1_name--idx2_name--new-in-v855)を使用します。このヒントは、テーブルのAFFINITY属性と組み合わせて使用​​することをお勧めします。たとえば、通常のテーブルの場合は`AFFINITY="table"` 、パーティションテーブルの場合は`AFFINITY="partition"`設定します。

    特定のテーブルに対して、TiKVへのインデックス検索プッシュダウンを無効にするには、ヒント[`NO_INDEX_LOOKUP_PUSHDOWN(t1_name)`](https://docs.pingcap.com/tidb/v8.5/optimizer-hints#no_index_lookup_pushdownt1_name-new-in-v855)を使用します。

    詳細については、 [ドキュメント](https://docs.pingcap.com/tidb/v8.5/optimizer-hints#index_lookup_pushdownt1_name-idx1_name--idx2_name--new-in-v855)参照してください。

-   テーブルレベルのデータアフィニティをサポートしてクエリパフォーマンスを向上させる（実験的） [#9764](https://github.com/tikv/pd/issues/9764) @[lhy1024](https://github.com/lhy1024)

    バージョン8.5.5以降では、テーブルの作成または変更時に、 `AFFINITY`テーブルオプションを`table`または`partition`に設定できます。このオプションを有効にすると、PDは同じテーブルまたは同じパーティションに属するリージョンを1つのアフィニティグループにグループ化します。スケジューリング中、PDはこれらのリージョンのリーダーおよびボーターレプリカを少数のTiKVノードの同じサブセットに配置することを優先します。このシナリオでは、クエリで[`INDEX_LOOKUP_PUSHDOWN`](https://docs.pingcap.com/tidb/v8.5/optimizer-hints#index_lookup_pushdownt1_name-idx1_name--idx2_name--new-in-v855)ヒントを使用することで、インデックス検索をTiKVにプッシュするようにオプティマイザに明示的に指示でき、ノード間分散クエリによって発生するレイテンシーを削減し、クエリのパフォーマンスを向上させることができます。

    この機能は現在実験的であり、デフォルトでは無効になっています。有効にするには、PD構成項目[`schedule.affinity-schedule-limit`](https://docs.pingcap.com/tidb/v8.5/pd-configuration-file#affinity-schedule-limit-new-in-v855)値を`0`より大きい値に設定してください。この構成項目は、PDが同時に実行できるアフィニティスケジューリングタスクの最大数を制御します。

    詳細については、 [ドキュメント](https://docs.pingcap.com/tidb/v8.5/table-affinity)参照してください。

-   ポイントインタイムリカバリ（PITR）は、圧縮ログバックアップからのリカバリをサポートし、より高速なリストアを実現します[#56522](https://github.com/pingcap/tidb/issues/56522) @[YuJuncen](https://github.com/YuJuncen)

    バージョン8.5.5以降、ログバックアップ圧縮機能にオフライン圧縮機能が追加され、非構造化ログバックアップデータを構造化SSTファイルに変換できるようになりました。これにより、以下の改善が実現します。

    -   **リカバリ性能の向上**：SSTファイルをより迅速にクラスターにインポートできるようになりました。
    -   **storage容量の削減**：圧縮処理中に冗長データが削除されます。
    -   **アプリケーションへの影響を軽減**：スナップショットベースのフルバックアップの頻度を減らすことで、RPO（リカバリポイント目標）を維持できます。

    詳細については、 [ドキュメント](https://docs.pingcap.com/tidb/v8.5/br-compact-log-backup)参照してください。

-   バックアップからのシステムテーブルのリカバリを高速化する[#58757](https://github.com/pingcap/tidb/issues/58757) @[Leavrth](https://github.com/Leavrth)

    バージョン8.5.5以降、 BRはバックアップからシステムテーブルを復元する際に、論理復元ではなく物理復元を使用するための新しいパラメータ`--fast-load-sys-tables`を導入しました。このパラメータを有効にすると、 BRは既存のシステムテーブルにデータを復元するのではなく、完全に置き換えるか上書きするため、大規模な展開における復元パフォーマンスが大幅に向上します。

    詳細については、 [ドキュメント](/br/br-snapshot-guide.md#restore-tables-in-the-mysql-schema)参照してください。

### 信頼性 {#reliability}

-   ネットワークジッター時のTiKVにおけるスケジューリングの安定性を向上させる[#9359](https://github.com/tikv/pd/issues/9359) @[okJiang](https://github.com/okJiang)

    バージョン8.5.5以降、TiKVはネットワークの遅延ノードを検出してフィードバックするメカニズムを導入しました。このメカニズムが有効になっている場合、TiKVはノード間のネットワークレイテンシーをプローブし、ネットワーク遅延スコアを計算して、そのスコアをPDに報告します。PDはこのスコアに基づいてTiKVノードのネットワーク状態を評価し、それに応じてスケジューリングを調整します。TiKVノードでネットワークジッターが発生していることが検出されると、PDはそのノードへの新しいリーダーのスケジューリングを制限します。ネットワークジッターが続く場合、PDは影響を受けているノードから既存のリーダーを他のTiKVノードに積極的に移動させ、ネットワークの問題がクラスタに与える影響を軽減します。

    詳細については、 [ドキュメント](/pd-control.md#scheduler-config-evict-slow-store-scheduler)参照してください。

### 可用性 {#availability}

-   PD [#8678](https://github.com/tikv/pd/issues/8678) @[Tema](https://github.com/Tema)のクライアント回路遮断器パターンを紹介します

    TiDBは、再試行の頻発や同様のフィードバックループによるPDリーダーの過負荷を防ぐため、サーキットブレーカーパターンを実装しました。エラー率が事前に定義されたしきい値に達すると、サーキットブレーカーは受信トラフィックを制限し、システムの回復と安定化を促します。サーキットブレーカーの制御には、システム変数`tidb_cb_pd_metadata_error_rate_threshold_ratio`使用できます。

    詳細については、 [ドキュメント](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_cb_pd_metadata_error_rate_threshold_ratio-new-in-v855)参照してください。

### SQL {#sql}

-   分散ジョブの同時実行性とスループットを動的に変更するサポート`ADD INDEX`ジョブ[#64947](https://github.com/pingcap/tidb/issues/64947) @[joechenrh](https://github.com/joechenrh)

    TiDB バージョン v8.5.5 より前のバージョンでは、分散実行フレームワーク (DXF) [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710)が有効になっている場合、実行中のジョブ`ADD INDEX`の`THREAD` 、または`MAX_WRITE_SPEED`パラメータの変更はサポートされていません。これらのパラメータを変更するには、実行中のジョブ`ADD INDEX` `BATCH_SIZE`キャンセルし、パラメータを再設定してからジョブを再送信する必要があり、非効率的です。

    バージョン8.5.5以降では、 `ADMIN ALTER DDL JOBS`ステートメントを使用して、ジョブを中断することなく、現在のワークロードとパフォーマンス要件に基づいて、実行中の分散`ADD INDEX`のこれらのパラメータを動的に調整できます。

    詳細については、 [ドキュメント](/sql-statements/sql-statement-admin-alter-ddl.md)参照してください。

### データベース操作 {#db-operations}

-   TiKV [#17221](https://github.com/tikv/tikv/issues/17221) @[hujiatao0](https://github.com/hujiatao0)の正常なシャットダウンをサポートします

    TiKVサーバーをシャットダウンする際、TiKVはシャットダウン前に、設定可能なタイムアウト時間内にノード上のLeaderレプリカを他のTiKVノードに転送しようとします。デフォルトのタイムアウト時間は20秒で、設定項目[`server.graceful-shutdown-timeout`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#graceful-shutdown-timeout-new-in-v855)を使用して調整できます。タイムアウトに達しても一部のリーダーが正常に転送されなかった場合、TiKVは残りのLeader転送をスキップしてシャットダウンを続行します。

    詳細については、 [ドキュメント](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#graceful-shutdown-timeout-new-in-v855)参照してください。

-   進行中のログバックアップとスナップショット復元間の互換性を改善[#58685](https://github.com/pingcap/tidb/issues/58685) @[BornChanger](https://github.com/BornChanger)

    バージョン8.5.5以降では、ログバックアップタスクの実行中でも、前提条件を満たしていればスナップショット復元を実行できます。これにより、復元処理中に進行中のログバックアップを停止することなく続行でき、復元されたデータは進行中のログバックアップに正しく記録されます。

    詳細については、 [ドキュメント](https://docs.pingcap.com/tidb/v8.5/br-pitr-manual#compatibility-between-ongoing-log-backup-and-snapshot-restore)参照してください。

-   ログバックアップからのテーブルレベルの復元をサポート[#57613](https://github.com/pingcap/tidb/issues/57613) @[Tristan1900](https://github.com/Tristan1900)

    バージョン8.5.5以降では、フィルタを使用してログバックアップから個々のテーブルのポイントインタイムリカバリ（PITR）を実行できます。クラスタ全体ではなく特定のテーブルを特定の時点に復元することで、より柔軟で影響の少ないリカバリオプションが提供されます。

    詳細については、 [ドキュメント](/br/br-pitr-manual.md#restore-data-using-filters)参照してください。

### 可観測性 {#observability}

-   ステートメントサマリーテーブルとスロークエリログにstorageエンジン識別子を追加する[#61736](https://github.com/pingcap/tidb/issues/61736) @[henrybw](https://github.com/henrybw)

    TiKVとTiFlashの両方がクラスタにデプロイされている場合、データベースの診断やパフォーマンス最適化の際に、storageエンジンごとにSQLステートメントをフィルタリングする必要が生じることがよくあります。たとえば、 TiFlashに高負荷がかかっている場合、潜在的な原因を特定するために、 TiFlash上​​で実行されているSQLステートメントを識別する必要があるかもしれません。このニーズに応えるため、TiDBはv8.5.5以降、ステートメントサマリーテーブルとスロークエリログにstorageエンジン識別子フィールドを追加しました。

    [明細書概要表](/statement-summary-tables.md)の新しいフィールド:

    -   `STORAGE_KV` : `1` 、SQL ステートメントが TiKV にアクセスしていることを示します。
    -   `STORAGE_MPP` : `1` 、SQL ステートメントがTiFlashにアクセスすることを示します。

    [スロークエリログ](/identify-slow-queries.md)の新しいフィールド:

    -   `Storage_from_kv` : `true` 、SQL ステートメントが TiKV にアクセスしていることを示します。
    -   `Storage_from_mpp` : `true` 、SQL ステートメントがTiFlashにアクセスすることを示します。

    この機能は、特定の診断およびパフォーマンス最適化シナリオにおけるワークフローを簡素化し、問題特定効率を向上させます。

    詳細については、 [明細書概要表](/statement-summary-tables.md)と[遅いクエリを特定する](/identify-slow-queries.md)参照してください。

### Security {#security}

-   Azure Blob Storage へのバックアップと復元 (BR) で Azure Managed Identity (MI) 認証をサポートする[#19006](https://github.com/tikv/tikv/issues/19006) @[RidRisR](https://github.com/RidRisR)

    バージョン8.5.5以降、 BRはAzure Blob Storageへの認証にAzure Managed Identity（MI）をサポートし、静的SASトークンが不要になりました。これにより、Azureのセキュリティベストプラクティスに準拠した、安全でキーレスな一時的な認証が可能になります。

    この機能により、 BRとTiKVに組み込まれたBRワーカーは、Azureインスタンスメタデータサービス（IMDS）から直接アクセストークンを取得できるため、認証情報の漏洩リスクが軽減され、Azure上のセルフマネージドおよびクラウドデプロイメントの両方で認証情報のローテーション管理が簡素化されます。

    この機能は、Azure Kubernetes Service (AKS) またはその他の Azure 環境で実行されている TiDB クラスターに適用されます。特に、バックアップおよび復元操作に対して厳格なセキュリティ制御が求められるエンタープライズ環境において有効です。

    詳細については、 [ドキュメント](/br/backup-and-restore-storages.md#authentication)参照してください。

## 互換性の変更 {#compatibility-changes}

TiDBクラスタがv8.5.4で新規にデプロイされている場合（つまり、v8.5.3より前のバージョンからアップグレードされていない場合）、v8.5.5へスムーズにアップグレードできます。v8.5.5の変更点のほとんどは通常のアップグレードでは問題ありませんが、このリリースには動作の変更、MySQLとの互換性調整、​​システム変数の更新、構成パラメータの更新、システムテーブルの変更も含まれています。アップグレードする前に、このセクションをよくお読みください。

### 行動の変化 {#behavior-changes}

-   バージョン8.5.5以降、TiDBはデータ復元時にターゲットテーブルを自動的にモード`restore`に設定します。モード`restore`のテーブルでは、ユーザーによる読み取りおよび書き込み操作が禁止されます。復元が完了すると、TiDBはこれらのテーブルのモードを自動的にモード`normal`に戻し、ユーザーが通常どおりテーブルを読み書きできるようにします。この動作により、復元プロセス中のタスクの安定性とデータの一貫性が確保されます。
-   バージョン8.5.5以降、パラメータ`--load-stats`を`false`に設定した場合、 BRは復元されたテーブルの統計情報をテーブル`mysql.stats_meta`に書き込まなくなりました。関連する統計情報を更新するには、復元後に[`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)手動で実行してください。

### MySQLとの互換性 {#mysql-compatibility}

-   TiDBはv8.5.5以降、テーブルまたはパーティションのデータアフィニティを制御するための新しいプロパティ`AFFINITY`をテーブルに導入しました。このプロパティは、 `CREATE TABLE`または`ALTER TABLE`ステートメントを使用して構成できます。詳細については、 [ドキュメント](https://docs.pingcap.com/tidb/v8.5/table-affinity)参照してください。
-   バージョン8.5.5以降、TiDBはテーブルのアフィニティ情報を表示するための新しいステートメント`SHOW AFFINITY`を導入しました。このステートメントはMySQL構文のTiDB拡張です。詳細については、 [ドキュメント](https://docs.pingcap.com/tidb/v8.5/sql-statement-show-affinity)参照してください。

### システム変数 {#system-variables}

| 変数名                                                                                                                                                                | 種類を変更する  | 説明                                                                                                                                                                                                                                                                                                  |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`tidb_analyze_column_options`](/system-variables.md#tidb_analyze_column_options-new-in-v830)                                                                      | 修正済み     | OLAPおよびHTAPシナリオにおける統計情報の完全性を向上させるため、デフォルト値を`PREDICATE`から`ALL`に変更します。                                                                                                                                                                                                                                |
| [`tidb_advancer_check_point_lag_limit`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_advancer_check_point_lag_limit-new-in-v855)                       | 新しく追加された | ログバックアップタスクのチェックポイント遅延の最大値を制御します。デフォルト値は`48h0m0s`です。タスクのチェックポイント遅延がこの制限を超えると、TiDB Advancer はタスクを一時停止します。                                                                                                                                                                                            |
| [`tidb_cb_pd_metadata_error_rate_threshold_ratio`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_cb_pd_metadata_error_rate_threshold_ratio-new-in-v855) | 新しく追加された | TiDBがサーキットブレーカーをトリガーするタイミングを制御します。デフォルト値は`0`で、これはサーキットブレーカーが無効であることを意味します。3～ `1` `0.01`値を設定すると有効になり、PDに送信される特定のリクエストのエラー率がしきい値に達するか超えた場合にサーキットブレーカーがトリガーされます。                                                                                                                                       |
| [`tidb_index_lookup_pushdown_policy`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_index_lookup_pushdown_policy-new-in-v855)                           | 新しく追加された | TiDBが`IndexLookUp`演算子をTiKVにプッシュダウンするかどうか、またそのタイミングを制御します。デフォルト値は`hint-only`で、これはSQL文で[`INDEX_LOOKUP_PUSHDOWN`](https://docs.pingcap.com/tidb/v8.5/optimizer-hints#index_lookup_pushdownt1_name-idx1_name--idx2_name--new-in-v855)ヒントが明示的に指定されている場合にのみ、TiDBが`IndexLookUp`演算子をTiKVにプッシュダウンすることを意味します。 |

### コンフィグレーションパラメータ {#configuration-parameters}

| コンフィグレーションファイルまたはコンポーネント | コンフィグレーションパラメータ                                                                                                                                      | 種類を変更する  | 説明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| TiDB                     | [`performance.enable-async-batch-get`](https://docs.pingcap.com/tidb/v8.5/tidb-configuration-file#enable-async-batch-get-new-in-v855)                | 新しく追加された | TiDBがバッチ取得演算子を実行する際に非同期モードを使用するかどうかを制御します。デフォルト値は`false`です。                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| ティクヴ                     | [`rocksdb.(defaultcf|writecf|lockcf|raftcf).level0-slowdown-writes-trigger`](/tikv-configuration-file.md#level0-slowdown-writes-trigger)             | 修正済み     | バージョン 8.5.5 以降では、フロー制御メカニズムが有効になっている場合 ( [`storage.flow-control.enable`](/tikv-configuration-file.md#enable) `true`に設定されている場合)、この設定項目は、その値が`storage.flow-control.l0-files-threshold`より大きい場合にのみ[`storage.flow-control.l0-files-threshold`](/tikv-configuration-file.md#l0-files-threshold)によって上書きされます。この動作により、フロー制御しきい値を上げたときに RocksDB の圧縮加速メカニズムが弱まるのを防ぎます。バージョン 8.5.4 以前のバージョンでは、フロー制御メカニズムが有効になっている場合、この設定項目は`storage.flow-control.l0-files-threshold`によって直接上書きされます。                                                               |
| ティクヴ                     | [`rocksdb.(defaultcf|writecf|lockcf|raftcf).soft-pending-compaction-bytes-limit`](/tikv-configuration-file.md#soft-pending-compaction-bytes-limit-1) | 修正済み     | バージョン 8.5.5 以降では、フロー制御メカニズムが有効になっている場合 ( [`storage.flow-control.enable`](/tikv-configuration-file.md#enable) `true`に設定されている場合)、この設定項目は、その値が`storage.flow-control.soft-pending-compaction-bytes-limit`より大きい場合にのみ[`storage.flow-control.soft-pending-compaction-bytes-limit`](/tikv-configuration-file.md#soft-pending-compaction-bytes-limit)で上書きされます。この動作により、フロー制御しきい値を上げたときに RocksDB の圧縮加速メカニズムが弱まるのを防ぎます。バージョン 8.5.4 以前のバージョンでは、フロー制御メカニズムが有効になっている場合、この設定項目は`storage.flow-control.soft-pending-compaction-bytes-limit`で直接上書きされます。 |
| ティクヴ                     | [`readpool.cpu-threshold`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#cpu-threshold-new-in-v855)                                     | 新しく追加された | 統合リードプールのCPU使用率のしきい値を指定します。デフォルト値は`0.0`で、これは統合リードプールのCPU使用率に制限がないことを意味します。スレッドプールのサイズは、ビジースレッドスケーリングアルゴリズムによってのみ決定され、現在のタスクを処理するスレッド数に基づいてサイズが動的に調整されます。                                                                                                                                                                                                                                                                                                                                                                             |
| ティクヴ                     | [`server.graceful-shutdown-timeout`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#graceful-shutdown-timeout-new-in-v855)               | 新しく追加された | TiKVの正常なシャットダウンのタイムアウト時間を制御します。デフォルト値は`20s`です。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ティクヴ                     | [`server.inspect-network-interval`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#inspect-network-interval-new-in-v855)                 | 新しく追加された | TiKV HealthCheckerがPDや他のTiKVノードに対してネットワーク検出をアクティブに実行する間隔を制御します。デフォルト値は`100ms`です。                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| PD                       | [`schedule.max-affinity-merge-region-size`](https://docs.pingcap.com/tidb/v8.5/pd-configuration-file#max-affinity-merge-region-size-new-in-v855)     | 新しく追加された | 同じ[親和性グループ](https://docs.pingcap.com/tidb/v8.5/table-affinity)内の隣接する小さな領域を自動的にマージするためのしきい値を制御します。デフォルト値は`256` (MiB 単位) です。                                                                                                                                                                                                                                                                                                                                                                                                           |
| PD                       | [`schedule.affinity-schedule-limit`](https://docs.pingcap.com/tidb/v8.5/pd-configuration-file#affinity-schedule-limit-new-in-v855)                   | 新しく追加された | 同時に実行できるスケジューリングタスクの[親和性](https://docs.pingcap.com/tidb/v8.5/table-affinity)を制御します。デフォルト値は`0`で、これはアフィニティスケジューリングがデフォルトで無効になっていることを意味します。                                                                                                                                                                                                                                                                                                                                                                                             |
| BR                       | [`--checkpoint-storage`](/br/br-checkpoint-restore.md#implementation-details-store-checkpoint-data-in-the-downstream-cluster)                        | 新しく追加された | チェックポイントデータの外部storageを指定します。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| BR                       | [`--fast-load-sys-tables`](/br/br-snapshot-guide.md#restore-tables-in-the-mysql-schema)                                                              | 新しく追加された | 新しいクラスタ上でのシステムテーブルの物理的な復元をサポートします。このパラメータはデフォルトで有効になっています。                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| BR                       | [`--filter`](/br/br-pitr-manual.md#restore-data-using-filters)                                                                                       | 新しく追加された | 復元対象に含める、または除外する特定のデータベースまたはテーブルを指定するパターンを指定します。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |

### システムテーブル {#system-tables}

-   システムテーブル[`INFORMATION_SCHEMA.TABLES`](/information-schema/information-schema-tables.md)と[`INFORMATION_SCHEMA.PARTITIONS`](/information-schema/information-schema-partitions.md) 、データ親和性レベルを表示するための新しい列`TIDB_AFFINITY`が追加されています。

### その他の変更点 {#other-changes}

-   TiDBのパフォーマンスを向上させるため、TiDBのGoコンパイラバージョンをgo1.23.6からgo1.25.5にアップグレードしてください。TiDB開発者の方は、スムーズなコンパイルを保証するために、Goコンパイラバージョンをアップグレードすることをお勧めします。

-   BR v8.5.5を使用して以前のTiDBバージョン（v8.5.4やv8.1.2など）でPITRリカバリを実行すると、ログリカバリ段階で失敗し、エラーが返される場合があります。

    この問題により、データの完全バックアップと復元は影響を受けません。

    ターゲットとなるTiDBクラスタのバージョンと一致するBRバージョンを使用することをお勧めします。たとえば、TiDB v8.5.4クラスタでPITRを実行する場合は、 BR v8.5.4を使用してください。

## 改善点 {#improvements}

-   TiDB

    -   エンコードエラーが発生した際の`IMPORT INTO`メッセージを改善し、ユーザーが問題をより正確に特定できるようにする[#63763](https://github.com/pingcap/tidb/issues/63763) @[D3Hunter](https://github.com/D3Hunter)
    -   Parquetファイルの解析メカニズムを強化し、Parquet形式データのインポートパフォーマンスを向上させます[#62906](https://github.com/pingcap/tidb/issues/62906) @[joechenrh](https://github.com/joechenrh)
    -   デフォルト値の`tidb_analyze_column_options`を`ALL`に変更して、デフォルトですべての列の統計情報を収集します[#64992](https://github.com/pingcap/tidb/issues/64992) @[0xPoe](https://github.com/0xPoe)
    -   特定のJOINシナリオでインクリメンタル処理を使用することで、 `IndexHashJoin`演算子の実行ロジックを最適化し、一度に大量のデータをロードすることを回避することで、メモリ使用量を大幅に削減し、パフォーマンスを向上させます[#63303](https://github.com/pingcap/tidb/issues/63303) @[ChangRui-Ryan](https://github.com/ChangRui-Ryan)
    -   分散実行フレームワーク（DXF）における内部SQLステートメントのCPU使用率を最適化する[#59344](https://github.com/pingcap/tidb/issues/59344) @[D3Hunter](https://github.com/D3Hunter)
    -   `expression.Contains`機能[#61373](https://github.com/pingcap/tidb/issues/61373) @[hawkingrei](https://github.com/hawkingrei)のパフォーマンスを改善します

-   ティクヴ

    -   ホットリードワークロード下でのCPU飢餓を回避するために、統合リードプールにCPU認識スケーリングを導入します[#18464](https://github.com/tikv/tikv/issues/18464) @[mittalrishabh](https://github.com/mittalrishabh)
    -   ネットワークレイテンシーを考慮した処理をスロースコアに追加し、ネットワーク状態が不安定なTiKVノードへのリーダーの割り当てを回避する[#18797](https://github.com/tikv/tikv/issues/18797) @[okJiang](https://github.com/okJiang)
    -   リーダーが過半数の投票を受けた後、オフラインの非投票ピアを待たずにすぐに休止状態に入ることができるようにすることで、休止状態のリージョン動作を最適化します[#19070](https://github.com/tikv/tikv/issues/19070) @[jiadebin](https://github.com/jiadebin)
    -   TiKVのメモリ使用量が多い場合にBRログ復元要求を制限して、TiKV OOM [#18124](https://github.com/tikv/tikv/issues/18124) @[3pointer](https://github.com/3pointer)を防止します

-   PD

    -   PDメモリ使用量を削減し、監視システムへの負荷を軽減するために、カーディナリティの高いメトリクスを最適化します[#9357](https://github.com/tikv/pd/issues/9357) @[rleungx](https://github.com/rleungx)
    -   タイムスタンプの進行とリーダー選出のロジックを最適化する[#9981](https://github.com/tikv/pd/issues/9981) @[bufferflies](https://github.com/bufferflies)
    -   storageエンジン（TiKVまたはTiFlash）によるTiKVストア制限のバッチ構成をサポート[#9970](https://github.com/tikv/pd/issues/9970) @[bufferflies](https://github.com/bufferflies)
    -   `pd_cluster_status`メトリック[#9855](https://github.com/tikv/pd/issues/9855) @[SerjKol80](https://github.com/SerjKol80)に`store`ラベルを追加します

-   ツール

    -   TiCDC

        -   変更フィードの構成検証ロジックを強化します。変更フィードを作成または更新する際に、ディスパッチャ構成で参照されている列が存在しない場合、TiCDC はエラーを返して操作を拒否し、実行失敗を防ぎます[#12253](https://github.com/pingcap/tiflow/issues/12253) @[wk989898](https://github.com/wk989898)

## バグ修正 {#bug-fixes}

-   TiDB

    -   TiDBが起動時に初期化バインディングを実行するために変数`tidb_mem_quota_binding_cache`の最新値を読み取れない問題を修正[#65381](https://github.com/pingcap/tidb/issues/65381) @[qw4990](https://github.com/qw4990)
    -   `extractBestCNFItemRanges`で候補アイテムが誤ってスキップされ、クエリ範囲の計算が不正確になる問題を修正します[#62547](https://github.com/pingcap/tidb/issues/62547) @[hawkingrei](https://github.com/hawkingrei)
    -   `plan replayer`バインディング[#64811](https://github.com/pingcap/tidb/issues/64811) @[hawkingrei](https://github.com/hawkingrei)をロードできない問題を修正します
    -   メモリが十分な場合でも`PointGet`を再利用できず、不要なメモリ割り当てが発生する問題を修正します[#63920](https://github.com/pingcap/tidb/issues/63920) @[hawkingrei](https://github.com/hawkingrei)
    -   `LogicalProjection.DeriveStats`メモリを過剰に割り当てる問題を修正[#63810](https://github.com/pingcap/tidb/issues/63810) @[hawkingrei](https://github.com/hawkingrei)
    -   `plan replayer`がパニックを起こしたときにダンプが失敗する問題を修正します[#64835](https://github.com/pingcap/tidb/issues/64835) @[hawkingrei](https://github.com/hawkingrei)
    -   TTLテーブルの`SHOW CREATE TABLE`出力における属性順序が特定のシナリオで誤って表示される問題を修正しました[#64876](https://github.com/pingcap/tidb/issues/64876) @[YangKeao](https://github.com/YangKeao)
    -   TTLジョブの実行サマリー情報が、ジョブのタイムアウト時に空になる問題を修正しました[#61509](https://github.com/pingcap/tidb/issues/61509) @[YangKeao](https://github.com/YangKeao)
    -   プランキャッシュが有効になっている場合に、相関サブクエリが予期しないフルテーブルスキャンを引き起こす可能性がある問題を修正しました[#64645](https://github.com/pingcap/tidb/issues/64645) @[winoros](https://github.com/winoros)
    -   システムテーブルが原因でテーブルの状態監視結果[#64080](https://github.com/pingcap/tidb/issues/64080) [#57176](https://github.com/pingcap/tidb/issues/57176) [0xPoe](https://github.com/0xPoe)
    -   自動統計更新を無効にした後、 `mysql.tidb_ddl_notifier`テーブルをクリーンアップできない問題を修正します ( `tidb_enable_auto_analyze = OFF` ) [#64038](https://github.com/pingcap/tidb/issues/64038) @[0xPoe](https://github.com/0xPoe)
    -   `newLocalColumnPool` [#63809](https://github.com/pingcap/tidb/issues/63809) @[hawkingrei](https://github.com/hawkingrei)で列が繰り返し割り当てられる問題を修正します
    -   `syncload`障害に関する無効な警告ログが生成される問題を修正します[#63880](https://github.com/pingcap/tidb/issues/63880) @[0xPoe](https://github.com/0xPoe)
    -   トランザクション[#63956](https://github.com/pingcap/tidb/issues/63956) @[wshwsh12](https://github.com/wshwsh12)を実行中の接続を手動で終了すると、TiDBがpanicて異常終了する可能性がある問題を修正しました。
    -   TiFlashレプリカ[#63329](https://github.com/pingcap/tidb/issues/63329)からキャッシュされたテーブルを読み取る際に、ゴルーチンとメモリリークが発生する可能性がある問題を修正しました[xzhangxian1008](https://github.com/xzhangxian1008)
    -   `ALTER TABLE child CHANGE COLUMN`を実行して列[#59705](https://github.com/pingcap/tidb/issues/59705) @[fzzf678](https://github.com/fzzf678)を変更した後、外部キーが更新されない問題を修正します。
    -   TiDB [#64413](https://github.com/pingcap/tidb/issues/64413)の以前のバージョンから`RENAME TABLE`ジョブ引数が正しくデコードされない可能性がある問題を修正しました @[joechenrh](https://github.com/joechenrh)
    -   BR復元が失敗した場合に自動インクリメントIDが再ベースされない問題を修正[#60804](https://github.com/pingcap/tidb/issues/60804) @[joechenrh](https://github.com/joechenrh)
    -   TiDBノードがアップグレード中に停止する可能性がある問題を修正[#64539](https://github.com/pingcap/tidb/issues/64539) @[joechenrh](https://github.com/joechenrh)
    -   インデックスレコードが欠落している場合に管理者チェックがエラーを報告しない問題を修正しました[#63698](https://github.com/pingcap/tidb/issues/63698) @[wjhuang2016](https://github.com/wjhuang2016)
    -   `MODIFY COLUMN`を介して照合順序を変更するとデータ インデックスの不整合が発生する問題を修正します[#61668](https://github.com/pingcap/tidb/issues/61668) @[tangenta](https://github.com/tangenta)
    -   複数のスキーマ変更を実行する際に、DDL の組み込み機能`ANALYZE`トリガーされない可能性がある問題を修正しました[#65040](https://github.com/pingcap/tidb/issues/65040) @[joechenrh](https://github.com/joechenrh)
    -   `ADD INDEX`ジョブ[#64129](https://github.com/pingcap/tidb/issues/64129) @[tangenta](https://github.com/tangenta)をキャンセルした後、分散実行フレームワーク (DXF) タスクがキャンセルされない問題を修正します。
    -   外部キーを含むテーブルのテーブル情報をロードするかどうかを決定する際の検証ロジックが誤っている問題を修正しました[#60044](https://github.com/pingcap/tidb/issues/60044) @[JQWong7](https://github.com/JQWong7)
    -   テーブル情報のコピー時に外部キー関連フィールドの初期化が正しく行われない問題を修正しました[#60044](https://github.com/pingcap/tidb/issues/60044) @[JQWong7](https://github.com/JQWong7)
    -   異なるデータベース間でテーブル名を変更した後に自動IDが正しく設定されない問題を修正[#64561](https://github.com/pingcap/tidb/issues/64561) @[joechenrh](https://github.com/joechenrh)
    -   メタキーの不適切な処理によってCPU使用率が高くなる問題を修正しました[#64323](https://github.com/pingcap/tidb/issues/64323) @[wjhuang2016](https://github.com/wjhuang2016)
    -   スキーマファイルの末尾にセミコロンがない場合にTiDB Lightning がエラーを報告しない問題を修正[#63414](https://github.com/pingcap/tidb/issues/63414) @[GMHDBJD](https://github.com/GMHDBJD)
    -   グローバルソートを有効にして`IMPORT INTO`実行すると、ファイル[#61177](https://github.com/pingcap/tidb/issues/61177) @[CbcWestwolf](https://github.com/CbcWestwolf)の読み込み中に無限ループが発生する問題を修正しました。
    -   `IMPORT INTO` [#64657](https://github.com/pingcap/tidb/issues/64657) @[D3Hunter](https://github.com/D3Hunter)で生成された列を処理する際にpanicが発生する問題を修正します
    -   単一の SQL ステートメントに複数の`AS OF TIMESTAMP`式が含まれている場合にエラーが誤って報告される可能性がある問題を修正します[#65090](https://github.com/pingcap/tidb/issues/65090) @[you06](https://github.com/you06)
    -   システムテーブル[#58985](https://github.com/pingcap/tidb/issues/58985) @[tangenta](https://github.com/tangenta)をクエリする際のメモリ使用量監視を改善することで、クエリ`information_schema.tables`時に発生する可能性のある OOM 問題を修正します。
    -   `client-go` [#65522](https://github.com/pingcap/tidb/issues/65522) @[bufferflies](https://github.com/bufferflies)の潜在的なメモリリークを修正

-   ティクヴ

    -   分析リクエストの`KV Cursor Operations`メトリックが常に`0` [#19206](https://github.com/tikv/tikv/issues/19206) @[glorv](https://github.com/glorv)になる問題を修正します
    -   リーダー変更後にリージョンハートビートがPDに誤ったリージョンサイズまたはキー統計を報告する可能性がある問題を修正[#19180](https://github.com/tikv/tikv/issues/19180) @[glorv](https://github.com/glorv)
    -   安全でないリカバリが停止する問題を修正するには、安全でないリカバリ降格リストから墓石TiFlash学習者を削除します[#18458](https://github.com/tikv/tikv/issues/18458) @[v01dstar](https://github.com/v01dstar)
    -   連続書き込み中にスナップショットが繰り返しキャンセルされる可能性があり、レプリカのリカバリを妨げる問題を修正しました[#18872](https://github.com/tikv/tikv/issues/18872) @[exit-code-1](https://github.com/exit-code-1)
    -   流量制御しきい値の増加により圧縮速度が低下する問題を修正します[#18708](https://github.com/tikv/tikv/issues/18708) @[hhwyt](https://github.com/hhwyt)
    -   特殊なケースでRaftピアが予定より早く休止状態に入り、TiKV再起動後にビジー状態が続きリーダー転送をブロックしてしまう問題を修正しました[#19203](https://github.com/tikv/tikv/issues/19203) @[LykxSassinator](https://github.com/LykxSassinator)

-   PD

    -   ノードをオンラインにするプロセス中にノードが取り外せない可能性がある問題を修正します[#8997](https://github.com/tikv/pd/issues/8997) @[lhy1024](https://github.com/lhy1024)
    -   Leader転送が多数発生するとリージョンサイズが急激に変化する可能性がある問題を修正しました[#10014](https://github.com/tikv/pd/issues/10014) @[lhy1024](https://github.com/lhy1024)
    -   スケジューリング中にPDpanicが発生する可能性がある問題を修正します[#9951](https://github.com/tikv/pd/issues/9951) @[bufferflies](https://github.com/bufferflies)
    -   インポート処理中にデータが不均衡になる可能性がある問題を修正します[#9088](https://github.com/tikv/pd/issues/9088) @[GMHDBJD](https://github.com/GMHDBJD)
    -   Active PD Follower機能を有効にした後、 Followerノードで失敗したリクエストが、再試行のためにLeaderノードに正しくフォールバックできない問題を修正しました[#64933](https://github.com/pingcap/tidb/issues/64933) @[okJiang](https://github.com/okJiang)
    -   PDマイクロサービスモード[#9825](https://github.com/tikv/pd/issues/9825)で一部のリクエストが正しく転送されない問題を修正 @[lhy1024](https://github.com/lhy1024)
    -   `tso`および`scheduling`マイクロサービスで TLS 構成が正しくロードされないために接続が失敗する可能性がある問題を修正します[#9367](https://github.com/tikv/pd/issues/9367) @[rleungx](https://github.com/rleungx)

-   TiFlash

    -   BRがデータを復元している際にTiFlashがpanic可能性がある問題を修正しました[#10606](https://github.com/pingcap/tiflash/issues/10606) @[CalvinNeo](https://github.com/CalvinNeo)
    -   TiFlashがBRでデータ復元中に16個以上のCPUコアを完全に利用できない問題を修正しました[#10605](https://github.com/pingcap/tiflash/issues/10605) @[JaySon-Huang](https://github.com/JaySon-Huang)
    -   TiFlashがディスクスピルをトリガーした際に予期せず終了する可能性がある問題を修正しました[#10553](https://github.com/pingcap/tiflash/issues/10553) `GROUP_CONCAT` [チャンルイ・ライアン](https://github.com/ChangRui-Ryan) 。

-   ツール

    -   バックアップと復元 (BR)

        -   クラスターに多数のリージョンが含まれている場合に、ログバックアップを有効にするとメモリ使用量が過剰になる問題を修正しました[#18719](https://github.com/tikv/tikv/issues/18719) @[YuJuncen](https://github.com/YuJuncen)
        -   Azure SDK が環境から適切なキーを見つけられない問題を修正します[#18206](https://github.com/tikv/tikv/issues/18206) @[YuJuncen](https://github.com/YuJuncen)
        -   `restore point` [#61642](https://github.com/pingcap/tidb/issues/61642) @[Leavrth](https://github.com/Leavrth)の間に外部キーが正しく復元できない問題を修正します
        -   バックアップとターゲットクラスタ間でシステムテーブルの照合順序に互換性がない場合にリストアが失敗する問題を修正するため、v6.5 から v7.5 への特権テーブルのリストアをサポートするパラメータ`--sys-check-collation`を追加しました[#64667](https://github.com/pingcap/tidb/issues/64667) @[Leavrth](https://github.com/Leavrth)
        -   操作が安全であっても、 `restore point`失敗した後に`restore log`実行できない問題を修正します[#64908](https://github.com/pingcap/tidb/issues/64908) @[RidRisR](https://github.com/RidRisR)
        -   チェックポイントからのログバックアップデータがフルバックアップ[#58685](https://github.com/pingcap/tidb/issues/58685)と混在している場合に、 `restore point`panic可能性がある問題を修正しました[ユジュンセン](https://github.com/YuJuncen)

    -   TiCDC

        -   オブジェクトstorageへのレプリケーション中にライターのクローズエラーが正しく捕捉されないためにデータが失われる可能性がある問題を修正しました[#12436](https://github.com/pingcap/tiflow/issues/12436) @[wk989898](https://github.com/wk989898)
        -   パーティションテーブルで`TRUNCATE`操作を複製すると、変更フィードの失敗が発生する可能性がある問題を修正しました[#12430](https://github.com/pingcap/tiflow/issues/12430) @[wk989898](https://github.com/wk989898)
        -   複数テーブル`RENAME` DDLステートメントを複製する際に、下流の実行順序が正しくない可能性がある問題を修正しました[#12449](https://github.com/pingcap/tiflow/issues/12449) @[wlwilliamx](https://github.com/wlwilliamx)
        -   Glue Schema Registry の使用時に発生する可能性のある接続エラーを修正するため、依存関係のバージョン`aws-sdk-go-v2` @[wk989898](https://github.com/wk989898) [#12424](https://github.com/pingcap/tiflow/issues/12424)アップグレードします。
        -   TiKV CDCコンポーネントが再起動後にメモリ割り当てを正しく解放しないために、changefeedタスクが停止する可能性がある問題を修正しました[#18169](https://github.com/tikv/tikv/issues/18169) @[asddongmen](https://github.com/asddongmen)
        -   TiKV CDC [#18915](https://github.com/tikv/tikv/issues/18915) @[asddongmen](https://github.com/asddongmen)でインクリメンタルスキャンタスクが蓄積された際に、gRPC接続がアイドル状態と誤判断され、予期せず閉じられる可能性がある問題を修正しました。
