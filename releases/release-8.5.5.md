---
title: TiDB 8.5.5 Release Notes
summary: TiDB 8.5.5 の機能、互換性の変更、改善、バグ修正について説明します。
---

# TiDB 8.5.5 リリースノート {#tidb-8-5-5-release-notes}

発売日：2026年1月15日

TiDB バージョン: 8.5.5

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v8.5/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v8.5/production-deployment-using-tiup)

## 特徴 {#features}

### パフォーマンス {#performance}

-   特定の損失のある DDL 操作 ( `BIGINT → INT`や`CHAR(120) → VARCHAR(60)`など) のパフォーマンスが大幅に向上します。データの切り捨てが発生しない場合、これらの操作の実行時間は数時間から数分、数秒、さらには数ミリ秒に短縮され、数十万倍から数十万倍のパフォーマンス向上が実現します[＃63366](https://github.com/pingcap/tidb/issues/63366) @ [wjhuang2016](https://github.com/wjhuang2016) 、 @ [接線](https://github.com/tangenta) 、 @ [fzzf678](https://github.com/fzzf678)

    最適化戦略は次のとおりです。

    -   厳密な SQL モードでは、TiDB は型変換中に潜在的なデータ切り捨てリスクを事前にチェックします。
    -   データの切り捨てリスクが検出されない場合、TiDB はメタデータのみを更新し、可能な限りインデックスの再構築を回避します。
    -   インデックスの再構築が必要な場合、TiDB はより効率的な取り込みプロセスを使用して、インデックスの再構築パフォーマンスを大幅に向上させます。

    次の表は、114 GiBのデータと6億行を持つテーブルに対するベンチマークテストに基づくパフォーマンス向上の例を示しています。テストクラスターは、3つのTiDBノード、6つのTiKVノード、1つのPDノードで構成されています。すべてのノードは、16個のCPUコアと32 GiBのメモリで構成されています。

    | シナリオ       | 操作タイプ                     | 最適化前   | 最適化後   | パフォーマンスの向上 |
    | ---------- | ------------------------- | ------ | ------ | ---------- |
    | インデックスのない列 | `BIGINT → INT`            | 2時間34分 | 1分5秒   | 142倍高速     |
    | インデックス列    | `BIGINT → INT`            | 6時間25分 | 0.05秒  | 46万倍高速     |
    | インデックス列    | `CHAR(120) → VARCHAR(60)` | 7時間16分 | 12分56秒 | 34倍高速      |

    上記のテスト結果は、DDL実行中にデータの切り捨てが発生しないという条件に基づいていることに注意してください。最適化は、符号付き整数型と符号なし整数型間の変換、文字セット間の変換、またはTiFlashレプリカを持つテーブルには適用されません。

    詳細については[ドキュメント](/sql-statements/sql-statement-modify-column.md)参照してください。

-   多数の外部キーがあるシナリオでの DDL パフォーマンスが向上し、論理 DDL パフォーマンスが最大 25 倍向上します[＃61126](https://github.com/pingcap/tidb/issues/61126) @ [GMHDBJD](https://github.com/GMHDBJD)

    v8.5.5より前のバージョンでは、超大規模テーブル（例えば、外部キーを持つ数十万のテーブルを含む、合計1,000万のテーブルを持つクラスター）を扱うシナリオでは、論理DDL操作（テーブルの作成や列の追加など）のパフォーマンスが約4 QPSまで低下することがありました。これは、マルチテナントSaaS環境における運用効率の低下につながります。

    TiDB v8.5.5はこれらのシナリオを最適化します。テスト結果によると、1,000万テーブル（外部キーを持つ20万テーブルを含む）という過酷な環境において、論理DDL処理性能は一貫して100 QPSを維持しました。以前のバージョンと比較して、パフォーマンスは25倍向上し、超大規模クラスターの運用応答性が大幅に向上しました。

-   クエリパフォーマンスを向上させるために、インデックス検索を TiKV にプッシュダウンすることをサポートします[＃62575](https://github.com/pingcap/tidb/issues/62575) @ [lcwangchao](https://github.com/lcwangchao)

    TiDB v8.5.5以降、 [オプティマイザヒント](/optimizer-hints.md)使用して`IndexLookUp`演算子をTiKVノードにプッシュダウンできるようになりました。これにより、リモートプロシージャコール（RPC）の回数が削減され、クエリパフォーマンスが向上します。実際のパフォーマンス向上はワークロードによって異なるため、検証にはテストが必要です。

    特定のテーブルについて、インデックス検索をTiKVにプッシュダウンするようオプティマイザに明示的に指示するには、 [`INDEX_LOOKUP_PUSHDOWN(t1_name, idx1_name [, idx2_name ...])`](https://docs.pingcap.com/tidb/v8.5/optimizer-hints#index_lookup_pushdownt1_name-idx1_name--idx2_name--new-in-v855)ヒントを使用します。このヒントは、テーブルのAFFINITY属性と組み合わせることをお勧めします。例えば、通常のテーブルの場合は`AFFINITY="table"` 、パーティションテーブルの場合は`AFFINITY="partition"`設定します。

    特定のテーブルに対して TiKV へのインデックス検索プッシュダウンを無効にするには、ヒント[`NO_INDEX_LOOKUP_PUSHDOWN(t1_name)`](https://docs.pingcap.com/tidb/v8.5/optimizer-hints#no_index_lookup_pushdownt1_name--new-in-v855)を使用します。

    詳細については[ドキュメント](https://docs.pingcap.com/tidb/v8.5/optimizer-hints#index_lookup_pushdownt1_name-idx1_name--idx2_name--new-in-v855)参照してください。

-   クエリパフォーマンスを向上させるためにテーブルレベルのデータアフィニティをサポートする（実験的） [＃9764](https://github.com/tikv/pd/issues/9764) @ [lhy1024](https://github.com/lhy1024)

    バージョン8.5.5以降では、テーブルの作成または変更時に、 `AFFINITY`テーブルオプションを`table`または`partition`に設定できます。このオプションを有効にすると、PDは同じテーブルまたは同じパーティションに属するリージョンを単一のアフィニティグループにグループ化します。PDはスケジューリング時に、これらのリージョンのリーダーレプリカとボーターレプリカを、いくつかのTiKVノードの同じサブセットに配置することを優先します。このシナリオでは、クエリで[`INDEX_LOOKUP_PUSHDOWN`](https://docs.pingcap.com/tidb/v8.5/optimizer-hints#index_lookup_pushdownt1_name-idx1_name--idx2_name--new-in-v855)ヒントを使用することで、オプティマイザーにインデックスルックアップをTiKVにプッシュダウンするよう明示的に指示することができ、ノード間の分散クエリによるレイテンシーを削減し、クエリパフォーマンスを向上させることができます。

    この機能は現在実験的であり、デフォルトでは無効になっています。有効にするには、PD設定項目[`schedule.affinity-schedule-limit`](https://docs.pingcap.com/tidb/v8.5/pd-configuration-file#affinity-schedule-limit-new-in-v855) `0`より大きい値に設定してください。この設定項目は、PDが同時に実行できるアフィニティスケジューリングタスクの最大数を制御します。

    詳細については[ドキュメント](https://docs.pingcap.com/tidb/v8.5/table-affinity)参照してください。

-   ポイントインタイムリカバリ（PITR）は、圧縮されたログバックアップからのリカバリをサポートし、復元を高速化します[＃56522](https://github.com/pingcap/tidb/issues/56522) @ [ユジュンセン](https://github.com/YuJuncen)

    バージョン8.5.5以降、ログバックアップ圧縮機能にオフライン圧縮機能が追加され、非構造化ログバックアップデータを構造化SSTファイルに変換できるようになりました。これにより、以下の改善がもたらされます。

    -   **回復パフォーマンスの向上**: SST ファイルをクラスターにさらに迅速にインポートできます。
    -   **storageスペースの消費量の削減**: 圧縮中に冗長データが削除されます。
    -   **アプリケーションへの影響の軽減**: 完全なスナップショットベースのバックアップの頻度を減らすことで、RPO (復旧ポイント目標) を維持できます。

    詳細については[ドキュメント](https://docs.pingcap.com/tidb/v8.5/br-compact-log-backup)参照してください。

-   バックアップ[＃58757](https://github.com/pingcap/tidb/issues/58757) @ [リーヴルス](https://github.com/Leavrth)からのシステム テーブルのリカバリを高速化

    v8.5.5以降、バックアップからシステムテーブルを復元する際に、論理復元ではなく物理復元を使用するための新しいパラメータ`--fast-load-sys-tables`が導入されました。このパラメータを有効にすると、 BRは既存のシステムテーブルにデータを復元するのではなく、完全に置き換えまたは上書きするため、大規模環境での復元パフォーマンスが大幅に向上します。

    詳細については[ドキュメント](/br/br-snapshot-guide.md#restore-tables-in-the-mysql-schema)参照してください。

### 信頼性 {#reliability}

-   ネットワークジッタ[＃9359](https://github.com/tikv/pd/issues/9359) @ [okJiang](https://github.com/okJiang)時のTiKVのスケジューリング安定性を向上

    v8.5.5以降、TiKVはネットワークの低速ノード検出およびフィードバックメカニズムを導入しました。このメカニズムを有効にすると、TiKVはノード間のネットワークレイテンシーをプローブし、ネットワーク低速スコアを計算してPDに報告します。PDはこのスコアに基づいてTiKVノードのネットワーク状態を評価し、それに応じてスケジューリングを調整します。TiKVノードでネットワークジッターが発生していることが検出されると、PDはそのノードへの新しいリーダーのスケジューリングを制限します。ネットワークジッターが持続する場合、PDは影響を受けたノードから既存のリーダーを他のTiKVノードにプロアクティブに移動させることで、クラスターへのネットワーク問題の影響を軽減します。

    詳細については[ドキュメント](/pd-control.md#scheduler-config-evict-slow-store-scheduler)参照してください。

### 可用性 {#availability}

-   PD [＃8678](https://github.com/tikv/pd/issues/8678) @ [テーマ](https://github.com/Tema)のクライアント サーキット ブレーカー パターンを導入する

    リトライストームや同様のフィードバックループによるPDリーダーの過負荷を防ぐため、TiDBはサーキットブレーカーパターンを実装しました。エラー率が事前定義されたしきい値に達すると、サーキットブレーカーは受信トラフィックを制限し、システムの回復と安定化を可能にします。サーキットブレーカーは、システム変数`tidb_cb_pd_metadata_error_rate_threshold_ratio`使用して制御できます。

    詳細については[ドキュメント](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_cb_pd_metadata_error_rate_threshold_ratio-new-in-v855)参照してください。

### SQL {#sql}

-   分散ジョブ`ADD INDEX`の同時実行性とスループットを動的に変更する機能をサポート[＃64947](https://github.com/pingcap/tidb/issues/64947) @ [ジョーチェン](https://github.com/joechenrh)

    TiDB v8.5.5より前のバージョンでは、Distributed eXecution Framework (DXF) [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710)が有効な場合、実行中の`ADD INDEX`ジョブの`THREAD` 、 `BATCH_SIZE` 、または`MAX_WRITE_SPEED`パラメータの変更はサポートされていません。これらのパラメータを変更するには、実行中の`ADD INDEX`ジョブをキャンセルし、パラメータを再設定してからジョブを再送信する必要があり、これは非効率的です。

    v8.5.5 以降では、 `ADMIN ALTER DDL JOBS`ステートメントを使用して、ジョブを中断することなく、現在のワークロードとパフォーマンス要件に基づいて、実行中の分散`ADD INDEX`ジョブのこれらのパラメータを動的に調整できます。

    詳細については[ドキュメント](/sql-statements/sql-statement-admin-alter-ddl.md)参照してください。

### DB操作 {#db-operations}

-   TiKV [＃17221](https://github.com/tikv/tikv/issues/17221) @ [ふじあたお0](https://github.com/hujiatao0)の正常なシャットダウンをサポート

    TiKVサーバーをシャットダウンする際、TiKVはシャットダウン前に、設定可能なタイムアウト時間内に、ノード上のLeaderレプリカを他のTiKVノードに転送しようとします。デフォルトのタイムアウト時間は20秒ですが、 [`server.graceful-shutdown-timeout`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#graceful-shutdown-timeout-new-in-v855)設定項目を使用して調整できます。タイムアウトに達し、一部のリーダーが正常に転送されていない場合、TiKVは残りのLeader転送をスキップし、シャットダウンを続行します。

    詳細については[ドキュメント](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#graceful-shutdown-timeout-new-in-v855)参照してください。

-   進行中のログバックアップとスナップショット復元の互換性を向上[＃58685](https://github.com/pingcap/tidb/issues/58685) @ [生まれ変わった人](https://github.com/BornChanger)

    バージョン8.5.5以降では、ログバックアップタスクの実行中でも、前提条件を満たしていればスナップショット復元を実行できます。これにより、復元プロセス中にログバックアップを停止することなく、実行中のログバックアップを続行でき、復元されたデータは実行中のログバックアップによって適切に記録されます。

    詳細については[ドキュメント](https://docs.pingcap.com/tidb/v8.5/br-pitr-manual#compatibility-between-ongoing-log-backup-and-snapshot-restore)参照してください。

-   ログバックアップ[＃57613](https://github.com/pingcap/tidb/issues/57613) @ [トリスタン1900](https://github.com/Tristan1900)からのテーブルレベルの復元をサポート

    バージョン8.5.5以降では、フィルターを使用してログバックアップから個々のテーブルに対してポイントインタイムリカバリ（PITR）を実行できます。クラスター全体ではなく特定のテーブルをターゲットポイントインタイムに復元することで、より柔軟で中断の少ないリカバリオプションが提供されます。

    詳細については[ドキュメント](/br/br-pitr-manual.md#restore-data-using-filters)参照してください。

### 可観測性 {#observability}

-   ステートメントサマリーテーブルとスロークエリログにstorageエンジン識別子を追加する[＃61736](https://github.com/pingcap/tidb/issues/61736) @ [ヘンリーBW](https://github.com/henrybw)

    TiKVとTiFlashの両方をクラスターに導入している場合、データベース診断やパフォーマンス最適化の際に、storageエンジン別にSQL文をフィルタリングする必要があることがよくあります。例えば、 TiFlashの負荷が高い場合、潜在的な原因を特定するために、 TiFlash上​​で実行されているSQL文を特定する必要があるかもしれません。こうしたニーズに対応するため、TiDBはv8.5.5以降、ステートメントサマリーテーブルとスロークエリログにstorageエンジン識別子フィールドを追加しました。

    [明細書要約表](/statement-summary-tables.md)の新しいフィールド:

    -   `STORAGE_KV` : `1` 、SQL ステートメントが TiKV にアクセスすることを示します。
    -   `STORAGE_MPP` : `1` 、SQL ステートメントがTiFlashにアクセスすることを示します。

    [スロークエリログ](/identify-slow-queries.md)の新しいフィールド:

    -   `Storage_from_kv` : `true` 、SQL ステートメントが TiKV にアクセスすることを示します。
    -   `Storage_from_mpp` : `true` 、SQL ステートメントがTiFlashにアクセスすることを示します。

    この機能により、特定の診断およびパフォーマンス最適化シナリオでのワークフローが簡素化され、問題の識別効率が向上します。

    詳細については、 [明細書要約表](/statement-summary-tables.md)および[遅いクエリを特定する](/identify-slow-queries.md)を参照してください。

### Security {#security}

-   Azure Blob Storage [＃19006](https://github.com/tikv/tikv/issues/19006) @ [リドリスR](https://github.com/RidRisR)へのバックアップと復元 (BR) のための Azure マネージド ID (MI) 認証のサポート

    v8.5.5以降、 BRはAzure Blob Storageへの認証にAzure Managed Identity (MI)をサポートし、静的SASトークンが不要になります。これにより、Azureのセキュリティのベストプラクティスに準拠した、安全でキーレスかつ一時的な認証が可能になります。

    この機能により、 BRと TiKV の埋め込みBRワーカーは、Azure Instance Metadata Service (IMDS) から直接アクセス トークンを取得できるため、資格情報の漏洩リスクが軽減され、Azure 上の自己管理型およびクラウド型の両方の展開において資格情報のローテーション管理が簡素化されます。

    この機能は、Azure Kubernetes Service (AKS) またはその他の Azure 環境で実行されている TiDB クラスターに適用されます。特に、バックアップおよび復元操作に厳格なセキュリティ制御を必要とするエンタープライズ環境に適用されます。

    詳細については[ドキュメント](/br/backup-and-restore-storages.md#authentication)参照してください。

## 互換性の変更 {#compatibility-changes}

v8.5.4で新規に導入されたTiDBクラスタ（つまり、v8.5.3より前のバージョンからアップグレードされていないクラスタ）は、v8.5.5へのスムーズなアップグレードが可能です。v8.5.5の変更点のほとんどは通常のアップグレードで問題ありませんが、このリリースには、動作の変更、MySQL互換性の調整、システム変数の更新、構成パラメータの更新、システムテーブルの変更もいくつか含まれています。アップグレード前に、このセクションをよくお読みください。

### 行動の変化 {#behavior-changes}

-   v8.5.5以降、TiDBはデータ復元時にターゲットテーブルを自動的にモード`restore`に設定します。モード`restore`のテーブルでは、ユーザーによる読み取りおよび書き込み操作は禁止されます。復元が完了すると、TiDBはこれらのテーブルのモードを自動的にモード`normal`に戻し、ユーザーによる読み取りおよび書き込み操作を通常通り実行できるようになります。この動作により、復元プロセス中のタスクの安定性とデータの一貫性が確保されます。
-   v8.5.5以降、パラメータ`--load-stats`を`false`に設定すると、 BRは復元されたテーブルの統計情報を`mysql.stats_meta`テーブルに書き込まなくなりました。関連する統計情報を更新するには、復元後に手動で[`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)実行してください。

### MySQLの互換性 {#mysql-compatibility}

-   TiDB v8.5.5以降、テーブルまたはパーティションのデータアフィニティを制御するための新しいプロパティ`AFFINITY`がテーブルに導入されました。このプロパティは、 `CREATE TABLE`または`ALTER TABLE`ステートメントを使用して設定できます。詳細については、 [ドキュメント](https://docs.pingcap.com/tidb/v8.5/table-affinity)参照してください。
-   TiDB v8.5.5以降、テーブルのアフィニティ情報を表示するための新しい`SHOW AFFINITY`ステートメントが導入されました。このステートメントは、MySQL構文のTiDB拡張です。詳細については、 [ドキュメント](https://docs.pingcap.com/tidb/v8.5/sql-statement-show-affinity)参照してください。

### システム変数 {#system-variables}

| 変数名                                                                                                                                                                | タイプを変更   | 説明                                                                                                                                                                                                                                                                                                          |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`tidb_analyze_column_options`](/system-variables.md#tidb_analyze_column_options-new-in-v830)                                                                      | 修正済み     | OLAP および HTAP シナリオでの統計の完全性を向上させるために、デフォルト値を`PREDICATE`から`ALL`に変更します。                                                                                                                                                                                                                                        |
| [`tidb_advancer_check_point_lag_limit`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_advancer_check_point_lag_limit-new-in-v855)                       | 新しく追加された | ログバックアップタスクの最大許容チェックポイントラグを制御します。デフォルト値は`48h0m0s`です。タスクのチェックポイントラグがこの制限を超えると、TiDB Advancer はタスクを一時停止します。                                                                                                                                                                                                    |
| [`tidb_cb_pd_metadata_error_rate_threshold_ratio`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_cb_pd_metadata_error_rate_threshold_ratio-new-in-v855) | 新しく追加された | TiDBがサーキットブレーカーをトリガーするタイミングを制御します。デフォルト値は`0`で、サーキットブレーカーは無効です。3 から`0.01` `1`を設定するとサーキットブレーカーが有効になり、PDに送信された特定のリクエストのエラー率がしきい値に達するか超過するとサーキットブレーカーがトリガーされます。                                                                                                                                                 |
| [`tidb_index_lookup_pushdown_policy`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_index_lookup_pushdown_policy-new-in-v855)                           | 新しく追加された | TiDBが`IndexLookUp`の演算子をTiKVにプッシュダウンするかどうか、またプッシュダウンするタイミングを制御します。デフォルト値は`hint-only`です。これは、SQL文で[`INDEX_LOOKUP_PUSHDOWN`](https://docs.pingcap.com/tidb/v8.5/optimizer-hints#index_lookup_pushdownt1_name-idx1_name--idx2_name--new-in-v855)ヒントが明示的に指定された場合にのみ、TiDBが`IndexLookUp`演算子をTiKVにプッシュダウンすることを意味します。 |

### コンフィグレーションパラメータ {#configuration-parameters}

| コンフィグレーションファイルまたはコンポーネント | コンフィグレーションパラメータ                                                                                                                                      | タイプを変更   | 説明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ティドブ                     | [`performance.enable-async-batch-get`](https://docs.pingcap.com/tidb/v8.5/tidb-configuration-file#enable-async-batch-get-new-in-v855)                | 新しく追加された | TiDBがBatch Getオペレータを実行する際に非同期モードを使用するかどうかを制御します。デフォルト値は`false`です。                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ティクブ                     | [`rocksdb.(defaultcf|writecf|lockcf|raftcf).level0-slowdown-writes-trigger`](/tikv-configuration-file.md#level0-slowdown-writes-trigger)             | 修正済み     | v8.5.5以降では、フロー制御メカニズムが有効になっている場合（ [`storage.flow-control.enable`](/tikv-configuration-file.md#enable) `true`に設定されている場合）、この設定項目は 5 の値が`storage.flow-control.l0-files-threshold`より大きい場合にのみ[`storage.flow-control.l0-files-threshold`](/tikv-configuration-file.md#l0-files-threshold)で上書きされます。この動作により、フロー制御しきい値を上げた際にRocksDBの圧縮加速メカニズムが弱まるのを防ぎます。v8.5.4以前のバージョンでは、フロー制御メカニズムが有効になっている場合、この設定項目は`storage.flow-control.l0-files-threshold`で直接上書きされていました。                                                                  |
| ティクブ                     | [`rocksdb.(defaultcf|writecf|lockcf|raftcf).soft-pending-compaction-bytes-limit`](/tikv-configuration-file.md#soft-pending-compaction-bytes-limit-1) | 修正済み     | v8.5.5以降では、フロー制御メカニズムが有効になっている場合（ [`storage.flow-control.enable`](/tikv-configuration-file.md#enable) `true`に設定されている場合）、この設定項目は、値が`storage.flow-control.soft-pending-compaction-bytes-limit`より大きい場合にのみ[`storage.flow-control.soft-pending-compaction-bytes-limit`](/tikv-configuration-file.md#soft-pending-compaction-bytes-limit)で上書きされます。この動作により、フロー制御しきい値を上げた際にRocksDBの圧縮加速メカニズムが弱まるのを防ぎます。v8.5.4以前のバージョンでは、フロー制御メカニズムが有効になっている場合、この設定項目は`storage.flow-control.soft-pending-compaction-bytes-limit`で直接上書きされていました。 |
| ティクブ                     | [`readpool.cpu-threshold`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#cpu-threshold-new-in-v855)                                     | 新しく追加された | 統合読み取りプールのCPU使用率のしきい値を指定します。デフォルト値は`0.0`で、統合読み取りプールのCPU使用率に制限がないことを意味します。スレッドプールのサイズは、ビジースレッドスケーリングアルゴリズムによってのみ決定され、現在のタスクを処理しているスレッドの数に基づいてサイズが動的に調整されます。                                                                                                                                                                                                                                                                                                                                                            |
| TiKV                     | [`server.graceful-shutdown-timeout`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#graceful-shutdown-timeout-new-in-v855)               | 新しく追加された | TiKVの正常なシャットダウンのタイムアウト時間を制御します。デフォルト値は`20s`です。                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| ティクブ                     | [`server.inspect-network-interval`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#inspect-network-interval-new-in-v855)                 | 新しく追加された | TiKVヘルスチェッカーがPDおよび他のTiKVノードに対してネットワーク検出をアクティブに実行する間隔を制御します。デフォルト値は`100ms`です。                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| PD                       | [`schedule.max-affinity-merge-region-size`](https://docs.pingcap.com/tidb/v8.5/pd-configuration-file#max-affinity-merge-region-size-new-in-v855)     | 新しく追加された | 同じ[アフィニティグループ](https://docs.pingcap.com/tidb/v8.5/table-affinity)内の隣接する小さな領域を自動的に結合するためのしきい値を制御します。デフォルト値は`256` （MiB単位）です。                                                                                                                                                                                                                                                                                                                                                                                            |
| PD                       | [`schedule.affinity-schedule-limit`](https://docs.pingcap.com/tidb/v8.5/pd-configuration-file#affinity-schedule-limit-new-in-v855)                   | 新しく追加された | 同時に実行できる[親和性](https://docs.pingcap.com/tidb/v8.5/table-affinity)スケジューリングタスクの数を制御します。デフォルト値は`0`で、アフィニティスケジューリングはデフォルトで無効になっています。                                                                                                                                                                                                                                                                                                                                                                                       |
| BR                       | [`--checkpoint-storage`](/br/br-checkpoint-restore.md#implementation-details-store-checkpoint-data-in-the-downstream-cluster)                        | 新しく追加された | チェックポイント データの外部storageを指定します。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| BR                       | [`--fast-load-sys-tables`](/br/br-snapshot-guide.md#restore-tables-in-the-mysql-schema)                                                              | 新しく追加された | 新しいクラスター上のシステムテーブルの物理的な復元をサポートします。このパラメータはデフォルトで有効になっています。                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| BR                       | [`--filter`](/br/br-pitr-manual.md#restore-data-using-filters)                                                                                       | 新しく追加された | 復元対象に特定のデータベースまたはテーブルを含めるか除外するかのパターンを指定します。                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |

### システムテーブル {#system-tables}

-   システム テーブル[`INFORMATION_SCHEMA.TABLES`](/information-schema/information-schema-tables.md)と[`INFORMATION_SCHEMA.PARTITIONS`](/information-schema/information-schema-partitions.md) 、データ アフィニティ レベルを表示するための新しい列`TIDB_AFFINITY`が追加されます。

### その他の変更点 {#other-changes}

-   TiDBのGoコンパイラバージョンをgo1.23.6からgo1.25.5にアップグレードすると、TiDBのパフォーマンスが向上します。TiDB開発者の方は、スムーズなコンパイルを実現するためにGoコンパイラバージョンをアップグレードしてください。

-   BR v8.5.5 を使用して以前の TiDB バージョン (v8.5.4 や v8.1.2 など) で PITR リカバリを実行すると、ログ リカバリ ステージが失敗し、エラーが返される可能性があります。

    完全なデータバックアップと復元はこの問題の影響を受けません。

    ターゲットのTiDBクラスタバージョンと一致するBRバージョンを使用することをお勧めします。例えば、TiDB v8.5.4クラスタでPITRを実行する場合は、 BR v8.5.4を使用してください。

## 改善点 {#improvements}

-   ティドブ

    -   エンコードエラーが発生したときにユーザーが問題をより正確に識別できるように、 `IMPORT INTO`のエラーメッセージを改善します[＃63763](https://github.com/pingcap/tidb/issues/63763) @ [D3ハンター](https://github.com/D3Hunter)
    -   Parquet ファイルの解析メカニズムを強化して、Parquet 形式のデータのインポート パフォーマンスを向上します[＃62906](https://github.com/pingcap/tidb/issues/62906) @ [ジョーチェン](https://github.com/joechenrh)
    -   デフォルト値の`tidb_analyze_column_options`を`ALL`に変更して、すべての列の統計をデフォルトで[＃64992](https://github.com/pingcap/tidb/issues/64992) @ [0xポー](https://github.com/0xPoe)で収集します。
    -   特定のJOINシナリオで増分処理を使用して`IndexHashJoin`演算子の実行ロジックを最適化し、一度に大量のデータをロードすることを回避して、メモリ使用量を大幅に削減し、パフォーマンスを向上させます[＃63303](https://github.com/pingcap/tidb/issues/63303) @ [チャンルイ・ライアン](https://github.com/ChangRui-Ryan)
    -   分散実行フレームワーク (DXF) [＃59344](https://github.com/pingcap/tidb/issues/59344) @ [D3ハンター](https://github.com/D3Hunter)の内部 SQL 文の CPU 使用率を最適化します
    -   `expression.Contains`機能[＃61373](https://github.com/pingcap/tidb/issues/61373) @ [ホーキングレイ](https://github.com/hawkingrei)のパフォーマンスを向上させる

-   ティクブ

    -   ホットリードワークロード[＃18464](https://github.com/tikv/tikv/issues/18464) @ [ミッタルリシャブ](https://github.com/mittalrishabh)でのCPU不足を回避するために、統合リードプールにCPUを考慮したスケーリングを導入します。
    -   不安定なネットワーク状態の TiKV ノードにリーダーをスケジュールすることを避けるために、低速スコアにネットワークレイテンシー認識を追加します[＃18797](https://github.com/tikv/tikv/issues/18797) @ [okJiang](https://github.com/okJiang)
    -   オフラインの非投票者ピアを待たずに、リーダーが過半数の投票を受け取った直後に休止状態に入ることができるようにすることで、休止状態リージョンの動作を最適化します[＃19070](https://github.com/tikv/tikv/issues/19070) @ [嘉徳賓](https://github.com/jiadebin)
    -   TiKVメモリ使用量が多い場合は、TiKV OOM [＃18124](https://github.com/tikv/tikv/issues/18124) @ [3ポイントシュート](https://github.com/3pointer)を防ぐためにBRログ復元要求を抑制します。

-   PD

    -   高いカーディナリティを持つメトリックを最適化してPDメモリ使用量を削減し、監視システム[＃9357](https://github.com/tikv/pd/issues/9357) @ [rleungx](https://github.com/rleungx)への負荷を軽減します
    -   タイムスタンプの進行とリーダー選出のロジックを最適化[＃9981](https://github.com/tikv/pd/issues/9981) @ [バッファフライ](https://github.com/bufferflies)
    -   storageエンジン（TiKV またはTiFlash）による TiKV ストア制限のバッチ構成をサポート[＃9970](https://github.com/tikv/pd/issues/9970) @ [バッファフライ](https://github.com/bufferflies)
    -   `store`ラベルを`pd_cluster_status`メトリック[＃9855](https://github.com/tikv/pd/issues/9855) @ [セルジコル80](https://github.com/SerjKol80)に追加します

-   ツール

    -   TiCDC

        -   変更フィードの構成検証ロジックを強化しました。変更フィードを作成または更新するときに、ディスパッチャ構成で参照されている列が存在しない場合は、TiCDC はエラーを返し、実行の失敗を防ぐために操作を拒否します[＃12253](https://github.com/pingcap/tiflow/issues/12253) @ [wk989898](https://github.com/wk989898)

## バグ修正 {#bug-fixes}

-   ティドブ

    -   TiDBが起動時に初期化バインディングを実行するために`tidb_mem_quota_binding_cache`変数の最新値を読み取れない問題を修正[＃65381](https://github.com/pingcap/tidb/issues/65381) @ [qw4990](https://github.com/qw4990)
    -   `extractBestCNFItemRanges`で候補項目が誤ってスキップされ、クエリ範囲の計算が不正確になる問題を修正[＃62547](https://github.com/pingcap/tidb/issues/62547) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   `plan replayer`バインディング[＃64811](https://github.com/pingcap/tidb/issues/64811) @ [ホーキングレイ](https://github.com/hawkingrei)をロードできない問題を修正しました
    -   `PointGet`メモリが十分であってもチャンクの再利用に失敗し、不要なメモリ割り当てが発生する問題を修正[＃63920](https://github.com/pingcap/tidb/issues/63920) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   `LogicalProjection.DeriveStats`メモリ[＃63810](https://github.com/pingcap/tidb/issues/63810) @ [ホーキングレイ](https://github.com/hawkingrei)を割り当てすぎる問題を修正
    -   クエリパニック時にダンプに失敗する問題[＃64835](https://github.com/pingcap/tidb/issues/64835) `plan replayer` [ホーキングレイ](https://github.com/hawkingrei)
    -   特定のシナリオ[＃64876](https://github.com/pingcap/tidb/issues/64876) @ [ヤンケオ](https://github.com/YangKeao)でTTLテーブルの`SHOW CREATE TABLE`出力の属性順序が正しく表示されない問題を修正
    -   ジョブが[＃61509](https://github.com/pingcap/tidb/issues/61509) @ [ヤンケオ](https://github.com/YangKeao)でタイムアウトすると、TTL ジョブの実行概要情報が空になる問題を修正しました。
    -   プランキャッシュが有効な場合に相関サブクエリが予期しないフルテーブルスキャンをトリガーする可能性がある問題を修正[＃64645](https://github.com/pingcap/tidb/issues/64645) @ [ウィノロス](https://github.com/winoros)
    -   システムテーブルが誤ったテーブルヘルスモニタリング結果を引き起こす問題を修正[＃57176](https://github.com/pingcap/tidb/issues/57176) 、 [＃64080](https://github.com/pingcap/tidb/issues/64080) @ [0xポー](https://github.com/0xPoe)
    -   自動統計更新を無効にした後、 `mysql.tidb_ddl_notifier`テーブルをクリーンアップできない問題を修正（ `tidb_enable_auto_analyze = OFF` ） [＃64038](https://github.com/pingcap/tidb/issues/64038) @ [0xポー](https://github.com/0xPoe)
    -   `newLocalColumnPool` [＃63809](https://github.com/pingcap/tidb/issues/63809) @ [ホーキングレイ](https://github.com/hawkingrei)で列が繰り返し割り当てられる問題を修正
    -   `syncload`障害に関する無効な警告ログが[＃63880](https://github.com/pingcap/tidb/issues/63880) / [0xポー](https://github.com/0xPoe)生成される問題を修正
    -   トランザクション[＃63956](https://github.com/pingcap/tidb/issues/63956) @ [wshwsh12](https://github.com/wshwsh12)を実行している接続を手動で終了すると、TiDB がpanicて異常終了する可能性がある問題を修正しました。
    -   キャッシュされたテーブルがTiFlashレプリカ[＃63329](https://github.com/pingcap/tidb/issues/63329) @ [xzhangxian1008](https://github.com/xzhangxian1008)から読み取るときに、goroutine とメモリリークが発生する可能性がある問題を修正しました。
    -   `ALTER TABLE child CHANGE COLUMN`を実行して列[＃59705](https://github.com/pingcap/tidb/issues/59705) @ [fzzf678](https://github.com/fzzf678)を変更した後、外部キーが更新されない問題を修正しました。
    -   以前の TiDB バージョン[＃64413](https://github.com/pingcap/tidb/issues/64413) @ [ジョーチェン](https://github.com/joechenrh)から`RENAME TABLE`ジョブ引数が誤ってデコードされる可能性がある問題を修正しました。
    -   BR復元が[＃60804](https://github.com/pingcap/tidb/issues/60804) @ [ジョーチェン](https://github.com/joechenrh)で失敗したときに自動インクリメント ID の再ベースに失敗する問題を修正しました
    -   アップグレード[＃64539](https://github.com/pingcap/tidb/issues/64539) @ [ジョーチェン](https://github.com/joechenrh)中に TiDB ノードが停止する可能性がある問題を修正しました
    -   インデックスレコードが[＃63698](https://github.com/pingcap/tidb/issues/63698) @ [wjhuang2016](https://github.com/wjhuang2016)欠落しているときに管理者チェックでエラーが報告されない問題を修正しました
    -   `MODIFY COLUMN`で照合順序順序を変更すると、データ インデックスの不整合[＃61668](https://github.com/pingcap/tidb/issues/61668) @ [接線](https://github.com/tangenta)が発生する問題を修正しました。
    -   複数のスキーマ変更[＃65040](https://github.com/pingcap/tidb/issues/65040) @ [ジョーチェン](https://github.com/joechenrh)を実行するときに、DDL に埋め込まれた`ANALYZE`機能がトリガーされない可能性がある問題を修正しました
    -   `ADD INDEX`ジョブ[＃64129](https://github.com/pingcap/tidb/issues/64129) @ [接線](https://github.com/tangenta)をキャンセルした後、分散実行フレームワーク（DXF）タスクがキャンセルされない問題を修正しました。
    -   外部キー[＃60044](https://github.com/pingcap/tidb/issues/60044) @ [JQウォン7](https://github.com/JQWong7)を含むテーブルのテーブル情報をロードするかどうかを決定する際の検証ロジックが正しくない問題を修正しました
    -   テーブル情報[＃60044](https://github.com/pingcap/tidb/issues/60044) @ [JQウォン7](https://github.com/JQWong7)をコピーする際に外部キー関連フィールドの初期化が正しく行われない問題を修正
    -   異なるデータベース間でテーブルの名前を変更した後に自動IDが誤って設定される問題を修正[＃64561](https://github.com/pingcap/tidb/issues/64561) @ [ジョーチェン](https://github.com/joechenrh)
    -   メタキーの不適切な処理によりCPU使用率が上昇する問題を修正[＃64323](https://github.com/pingcap/tidb/issues/64323) @ [wjhuang2016](https://github.com/wjhuang2016)
    -   スキーマファイルに末尾のセミコロンがない場合にTiDB Lightning がエラーを報告できない問題を修正しました[＃63414](https://github.com/pingcap/tidb/issues/63414) @ [GMHDBJD](https://github.com/GMHDBJD)
    -   グローバルソートを有効にして`IMPORT INTO`実行すると、ファイル[＃61177](https://github.com/pingcap/tidb/issues/61177) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)の読み取り中に無限ループが発生する問題を修正しました。
    -   `IMPORT INTO` [＃64657](https://github.com/pingcap/tidb/issues/64657) @ [D3ハンター](https://github.com/D3Hunter)中に生成された列を処理するときにpanicが発生する問題を修正しました
    -   1つのSQL文に複数の`AS OF TIMESTAMP`式[＃65090](https://github.com/pingcap/tidb/issues/65090) @ [あなた06](https://github.com/you06)が含まれている場合にエラーが誤って報告される可能性がある問題を修正しました
    -   システムテーブル[＃58985](https://github.com/pingcap/tidb/issues/58985) @ [接線](https://github.com/tangenta)をクエリする際のメモリ使用量の監視を改善することにより、クエリ`information_schema.tables`の潜在的な OOM 問題を修正しました。

-   ティクブ

    -   分析リクエストの`KV Cursor Operations`メトリックが常に`0` [＃19206](https://github.com/tikv/tikv/issues/19206) @ [栄光](https://github.com/glorv)になる問題を修正しました
    -   リーダー変更[＃19180](https://github.com/tikv/tikv/issues/19180) @ [栄光](https://github.com/glorv)後にリージョンハートビートが PD に誤ったリージョンサイズまたはキー統計を報告する可能性がある問題を修正しました
    -   トゥームストーンTiFlash学習者を安全でないリカバリ降格リスト[＃18458](https://github.com/tikv/tikv/issues/18458) @ [v01dスター](https://github.com/v01dstar)から削除することにより、安全でないリカバリが停止する問題を修正しました。
    -   連続書き込み中にスナップショットが繰り返しキャンセルされ、レプリカの回復がブロックされる問題を修正[＃18872](https://github.com/tikv/tikv/issues/18872) @ [終了コード1](https://github.com/exit-code-1)
    -   フロー制御しきい値[＃18708](https://github.com/tikv/tikv/issues/18708) @ [hhwyt](https://github.com/hhwyt)の増加により圧縮が遅くなる問題を修正しました
    -   まれにRaftピアが休止状態に入り、ビジー状態のままになり、TiKV の再起動後にリーダー転送がブロックされる問題を修正しました[＃19203](https://github.com/tikv/tikv/issues/19203) @ [LykxSassinator](https://github.com/LykxSassinator)

-   PD

    -   ノードをオンラインにするプロセス中にノードを削除できない可能性がある問題を修正[＃8997](https://github.com/tikv/pd/issues/8997) @ [lhy1024](https://github.com/lhy1024)
    -   多数のLeaderの移行により、リージョンサイズ[＃10014](https://github.com/tikv/pd/issues/10014) @ [lhy1024](https://github.com/lhy1024)が突然変更される可能性がある問題を修正しました。
    -   [＃9951](https://github.com/tikv/pd/issues/9951) @ [バッファフライ](https://github.com/bufferflies)のスケジュール中に PDpanicを引き起こす可能性がある問題を修正しました
    -   インポートプロセス中にデータが不均衡になる可能性がある問題を修正[＃9088](https://github.com/tikv/pd/issues/9088) @ [GMHDBJD](https://github.com/GMHDBJD)
    -   アクティブPDFollower機能を有効にした後、Followerノードで失敗したリクエストがLeaderノードに正しくフォールバックして再試行[＃64933](https://github.com/pingcap/tidb/issues/64933) @ [okJiang](https://github.com/okJiang)を実行できない問題を修正しました。
    -   PDマイクロサービスモード[＃9825](https://github.com/tikv/pd/issues/9825) @ [lhy1024](https://github.com/lhy1024)で一部のリクエストが正しく転送されない問題を修正
    -   `tso`および`scheduling`マイクロサービス[＃9367](https://github.com/tikv/pd/issues/9367) @ [rleungx](https://github.com/rleungx)で TLS 構成の読み込みが正しくないために接続が失敗する可能性がある問題を修正しました

-   TiFlash

    -   BRがデータ[＃10606](https://github.com/pingcap/tiflash/issues/10606) @ [カルビンネオ](https://github.com/CalvinNeo)を復元しているときにTiFlashがpanic可能性がある問題を修正しました
    -   BRがデータ[＃10605](https://github.com/pingcap/tiflash/issues/10605) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)を復元しているときにTiFlashが16個を超えるCPUコアを完全に利用できない問題を修正しました
    -   `GROUP_CONCAT`ディスクスピル[＃10553](https://github.com/pingcap/tiflash/issues/10553) @ [チャンルイ・ライアン](https://github.com/ChangRui-Ryan)をトリガーするとTiFlash が予期せず終了する可能性がある問題を修正しました

-   ツール

    -   バックアップと復元 (BR)

        -   クラスターにリージョン[＃18719](https://github.com/tikv/tikv/issues/18719) @ [ユジュンセン](https://github.com/YuJuncen)が多数含まれている場合にログ バックアップを有効にするとメモリ使用量が過剰になる問題を修正しました。
        -   Azure SDKが環境[＃18206](https://github.com/tikv/tikv/issues/18206) @ [ユジュンセン](https://github.com/YuJuncen)から適切なキーを見つけられない問題を修正
        -   `restore point` [＃61642](https://github.com/pingcap/tidb/issues/61642) @ [リーヴルス](https://github.com/Leavrth)中に外部キーが適切に復元されない問題を修正
        -   バックアップとターゲット クラスタ間でシステム テーブル照合に互換性がない場合に復元が失敗する問題を修正しました`--sys-check-collation`パラメータを追加して、権限テーブルを v6.5 から v7.5 [＃64667](https://github.com/pingcap/tidb/issues/64667) @ [リーヴルス](https://github.com/Leavrth)に復元できるようにしました。
        -   操作が安全であっても、失敗した`restore point`の後に`restore log`実行できない問題を修正しました[＃64908](https://github.com/pingcap/tidb/issues/64908) @ [リドリスR](https://github.com/RidRisR)
        -   ログバックアップデータがフルバックアップ[＃58685](https://github.com/pingcap/tidb/issues/58685) @ [ユジュンセン](https://github.com/YuJuncen)と混在している場合、チェックポイントからの`restore point`panicになる可能性がある問題を修正しました。

    -   TiCDC

        -   ライタークローズエラーが正しくキャプチャされないため、オブジェクトstorageへのレプリケーション中にデータが失われる可能性がある問題を修正[＃12436](https://github.com/pingcap/tiflow/issues/12436) @ [wk989898](https://github.com/wk989898)
        -   パーティションテーブルで`TRUNCATE`操作を複製すると、変更フィードエラー[＃12430](https://github.com/pingcap/tiflow/issues/12430) @ [wk989898](https://github.com/wk989898)が発生する可能性がある問題を修正しました
        -   複数テーブル`RENAME` DDL ステートメント[＃12449](https://github.com/pingcap/tiflow/issues/12449) @ [wlwilliamx](https://github.com/wlwilliamx)を複製するときに下流の実行順序が正しくない可能性がある問題を修正しました。
        -   Glue Schema Registry の使用時に発生する可能性のある接続エラーを修正するには、 `aws-sdk-go-v2`依存関係バージョン[＃12424](https://github.com/pingcap/tiflow/issues/12424) @ [wk989898](https://github.com/wk989898)にアップグレードします。
        -   再起動後に TiKV CDCコンポーネントがメモリクォータを正しく解放できないために、変更フィード タスクが停止する可能性がある問題を修正しました[＃18169](https://github.com/tikv/tikv/issues/18169) @ [アズドンメン](https://github.com/asddongmen)
        -   TiKV CDC [＃18915](https://github.com/tikv/tikv/issues/18915) @ [アズドンメン](https://github.com/asddongmen)で増分スキャンタスクが蓄積されると、gRPC 接続がアイドル状態であると誤って判断され、予期せず閉じられる可能性がある問題を修正しました。
