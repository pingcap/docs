---
title: TiDB 5.3 Release Notes
---

# TiDB5.3リリースノート {#tidb-5-3-release-notes}

発売日：2021年11月30日

TiDBバージョン：5.3.0

v5.3では、主な新機能または改善点は次のとおりです。

-   一時テーブルを導入して、アプリケーションロジックを簡素化し、パフォーマンスを向上させます
-   テーブルとパーティションの属性設定をサポート
-   システムセキュリティを強化するために、TiDBダッシュボードで最小特権を持つユーザーの作成をサポートする
-   TiDBのタイムスタンプ処理フローを最適化して、全体的なパフォーマンスを向上させます
-   TiDBデータ移行（DM）のパフォーマンスを強化して、データがMySQLからTiDBに低レイテンシで移行されるようにします
-   複数のTiDBLightningインスタンスを使用した並列インポートをサポートして、完全なデータ移行の効率を向上させます
-   単一のSQLステートメントでクラスタのオンサイト情報の保存と復元をサポートします。これにより、実行プランに関連する問題のトラブルシューティングの効率が向上します。
-   継続的なプロファイリングの実験的機能をサポートして、データベースのパフォーマンスの可観測性を向上させます
-   システムのパフォーマンスと安定性を向上させるために、ストレージエンジンとコンピューティングエンジンの最適化を継続します
-   I / O操作をRaftstoreスレッドプールから分離することにより、TiKVの書き込みレイテンシを短縮します（デフォルトでは無効になっています）

## 互換性の変更 {#compatibility-changes}

> **ノート：**
>
> 以前のTiDBバージョンからv5.3.0にアップグレードするときに、すべての中間バージョンの互換性変更に関する注意事項を知りたい場合は、対応するバージョンの[リリースノート](/releases/release-notes.md)を確認できます。

### システム変数 {#system-variables}

| 変数名                                                                                                               | タイプを変更する   | 説明                                                                                                                                                                                                                                                                         |
| :---------------------------------------------------------------------------------------------------------------- | :--------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`tidb_enable_noop_functions`](/system-variables.md#tidb_enable_noop_functions-new-in-v40)                        | 変更         | 一時テーブルがTiDBでサポートされるようになったため、 `CREATE TEMPORARY TABLE`と`DROP TEMPORARY TABLE`で`tidb_enable_noop_functions`を有効にする必要がなくなりました。                                                                                                                                                 |
| [`tidb_enable_pseudo_for_outdated_stats`](/system-variables.md#tidb_enable_pseudo_for_outdated_stats-new-in-v530) | 新しく追加されました | テーブルの統計が期限切れになったときのオプティマイザーの動作を制御します。デフォルト値は`ON`です。テーブル内の変更された行の数が合計行の80％を超える場合（この比率は構成[`pseudo-estimate-ratio`](/tidb-configuration-file.md#pseudo-estimate-ratio)で調整可能）、オプティマイザーは、行の合計数以外の統計は信頼できなくなったと見なし、疑似を使用します代わりに統計。値を`OFF`に設定すると、統計の有効期限が切れても、オプティマイザーはそれらを使用します。 |
| [`tidb_enable_tso_follower_proxy`](/system-variables.md#tidb_enable_tso_follower_proxy-new-in-v530)               | 新しく追加されました | TSOフォロワープロキシ機能を有効にするか無効にするかを決定します。デフォルト値は`OFF`です。これは、TSOフォロワープロキシ機能が無効になっていることを意味します。現時点では、TiDBはPDリーダーからのみTSOを取得します。この機能を有効にすると、TiDBはTSOを取得するときにすべてのPDノードに要求を均等に送信します。次に、PDフォロワーはTSO要求を転送して、PDリーダーのCPUプレッシャーを減らします。                                                        |
| [`tidb_tso_client_batch_max_wait_time`](/system-variables.md#tidb_tso_client_batch_max_wait_time-new-in-v530)     | 新しく追加されました | TiDBがPDにTSOを要求したときのバッチ保存操作の最大待機時間を設定します。デフォルト値は`0`です。これは、追加の待機がないことを意味します。                                                                                                                                                                                                 |
| [`tidb_tmp_table_max_size`](/system-variables.md#tidb_tmp_table_max_size-new-in-v530)                             | 新しく追加されました | 単一の[一時テーブル](/temporary-tables.md)の最大サイズを制限します。一時テーブルがこのサイズを超えると、エラーが発生します。                                                                                                                                                                                                 |

### Configuration / コンフィグレーションファイルのパラメーター {#configuration-file-parameters}

| Configuration / コンフィグレーションファイル | Configuration / コンフィグレーション項目                                                                       | タイプを変更する   | 説明                                                                                                                                                                                              |
| :----------------------------- | :------------------------------------------------------------------------------------------------- | :--------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB                           | [`prepared-plan-cache.capacity`](/tidb-configuration-file.md#capacity)                             | 変更         | キャッシュされたステートメントの数を制御します。デフォルト値は`100`から`1000`に変更されます。                                                                                                                                            |
| TiKV                           | [`storage.reserve-space`](/tikv-configuration-file.md#reserve-space)                               | 変更         | TiKVの起動時にディスク保護用に予約されているスペースを制御します。 v5.3.0以降、予約済みスペースの80％は、ディスクスペースが不足している場合の運用および保守に必要な追加のディスクスペースとして使用され、残りの20％は一時ファイルの保存に使用されます。                                                             |
| TiKV                           | `memory-usage-limit`                                                                               | 変更         | この構成アイテムはTiDBv5.3.0の新機能であり、その値はstorage.block-cache.capacityに基づいて計算されます。                                                                                                                         |
| TiKV                           | [`raftstore.store-io-pool-size`](/tikv-configuration-file.md#store-io-pool-size-new-in-v530)       | 新しく追加されました | Raft I / Oタスクを処理するスレッドの許容数。これは、StoreWriterスレッドプールのサイズです。このスレッドプールのサイズを変更する場合は、 [TiKVスレッドプールのパフォーマンスチューニング](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)を参照してください。 |
| TiKV                           | [`raftstore.raft-write-size-limit`](/tikv-configuration-file.md#raft-write-size-limit-new-in-v530) | 新しく追加されました | Raftデータがディスクに書き込まれるしきい値を決定します。データサイズがこの構成アイテムの値よりも大きい場合、データはディスクに書き込まれます。 `raftstore.store-io-pool-size`の値が`0`の場合、この構成項目は有効になりません。                                                              |
| TiKV                           | `raftstore.raft-msg-flush-interval`                                                                | 新しく追加されました | Raftメッセージがバッチで送信される間隔を決定します。バッチのラフトメッセージは、この構成アイテムで指定された間隔ごとに送信されます。 `raftstore.store-io-pool-size`の値が`0`の場合、この構成項目は有効になりません。                                                                   |
| TiKV                           | `raftstore.raft-reject-transfer-leader-duration`                                                   | 削除         | リーダーが新しく追加されたノードに転送される最小期間を決定します。                                                                                                                                                               |
| PD                             | [`log.file.max-days`](/pd-configuration-file.md#max-days)                                          | 変更         | ログが保持される最大日数を制御します。デフォルト値は`1`から`0`に変更されます。                                                                                                                                                      |
| PD                             | [`log.file.max-backups`](/pd-configuration-file.md#max-backups)                                    | 変更         | 保持されるログの最大数を制御します。デフォルト値は`7`から`0`に変更されます。                                                                                                                                                       |
| PD                             | [`patrol-region-interval`](/pd-configuration-file.md#patrol-region-interval)                       | 変更         | ReplicaCheckerがリージョンのヘルス状態をチェックする実行頻度を制御します。この値が小さいほど、replicaCheckerの実行速度は速くなります。通常、このパラメータを調整する必要はありません。デフォルト値は`100ms`から`10ms`に変更されます。                                                         |
| PD                             | [`max-snapshot-count`](/pd-configuration-file.md#max-snapshot-count)                               | 変更         | 1つのストアが同時に受信または送信するスナップショットの最大数を制御します。 PDスケジューラーは、通常のトラフィックに使用されるリソースがプリエンプションされるのを防ぐために、この構成に依存しています。デフォルト値は`3`から`64`に変更されます。                                                                  |
| PD                             | [`max-pending-peer-count`](/pd-configuration-file.md#max-pending-peer-count)                       | 変更         | 1つのストアで保留中のピアの最大数を制御します。 PDスケジューラーは、この構成に依存して、古いログを持つリージョンが一部のノードで生成されるのを防ぎます。デフォルト値は`16`から`64`に変更されます。                                                                                         |
| TiDライトニング                      | `meta-schema-name`                                                                                 | 新しく追加されました | 各TiDBLightningインスタンスのメタ情報がターゲットクラスタに格納されているスキーマ名。デフォルト値は「lightning_metadata」です。                                                                                                                 |

### その他 {#others}

-   一時テーブル：

    -   v5.3.0より前のTiDBクラスタでローカル一時テーブルを作成した場合、これらのテーブルは実際には通常のテーブルであり、クラスタがv5.3.0以降のバージョンにアップグレードされた後は通常のテーブルとして処理されます。 v5.3.0以降のバージョンのTiDBクラスタでグローバル一時テーブルを作成した場合、クラスタがv5.3.0より前のバージョンにダウングレードされると、これらのテーブルは通常のテーブルとして処理され、データエラーが発生します。
    -   v5.3.0以降、TiCDCおよびBRは[グローバル一時テーブル](/temporary-tables.md#global-temporary-tables)をサポートします。 v5.3.0より前のバージョンのTiCDCおよびBRを使用して、グローバル一時テーブルをダウンストリームに複製すると、テーブル定義エラーが発生します。
    -   次のクラスターはv5.3.0以降であると予想されます。それ以外の場合は、グローバル一時テーブルを作成するときにデータエラーが報告されます。

        -   TiDB移行ツールを使用してインポートされるクラスタ
        -   TiDB移行ツールを使用して復元されたクラスタ
        -   TiDB移行ツールを使用したレプリケーションタスクのダウンストリームクラスタ
    -   一時テーブルの互換性情報については、 [MySQL一時テーブルとの互換性](/temporary-tables.md#compatibility-with-mysql-temporary-tables)と[他のTiDB機能との互換性の制限](/temporary-tables.md#compatibility-restrictions-with-other-tidb-features)を参照してください。

-   v5.3.0より前のリリースでは、システム変数が不正な値に設定されている場合、TiDBはエラーを報告します。 v5.3.0以降のリリースでは、システム変数が不正な値に設定されている場合、TiDBは「|警告| 1292 |切り捨てられた不正なxxx：&#39;xx&#39;」などの警告とともに成功を返します。

-   `SHOW CREATE VIEW`を実行するために`SHOW VIEW`の権限が必要ないという問題を修正します。これで、 `SHOW CREATE VIEW`ステートメントを実行するための`SHOW VIEW`の権限が必要になります。

-   システム変数`sql_auto_is_null`がnoop関数に追加されます。 `tidb_enable_noop_functions = 0/OFF`の場合、この変数値を変更するとエラーが発生します。

-   `GRANT ALL ON performance_schema.*`構文は許可されなくなりました。このステートメントをTiDBで実行すると、エラーが発生します。

-   v5.3.0より前に新しいインデックスが追加されたときに、指定された期間外に自動分析が予期せずトリガーされる問題を修正します。 v5.3.0では、 `tidb_auto_analyze_start_time`変数と`tidb_auto_analyze_end_time`変数を使用して期間を設定した後、自動分析はこの期間中にのみトリガーされます。

-   プラグインのデフォルトのストレージディレクトリが`""`から`/data/deploy/plugin`に変更されました。

-   DMコードは[TiCDCコードリポジトリのフォルダ「dm」](https://github.com/pingcap/tiflow/tree/master/dm)に移行されます。現在、DMはバージョン番号でTiDBに従います。 v2.0.xの次に、新しいDMバージョンはv5.3.0であり、リスクなしでv2.0.xからv5.3.0にアップグレードできます。

-   Prometheusのデフォルトでデプロイされたバージョンは、v2.8.1から2021年5月にリリースされた[v2.27.1](https://github.com/prometheus/prometheus/releases/tag/v2.27.1)にアップグレードされます。このバージョンは、より多くの機能を提供し、セキュリティの問題を修正します。 Prometheus v2.8.1と比較して、v2.27.1のアラート時間の表現はUnixタイムスタンプからUTCに変更されています。詳細については、 [プロメテウスコミット](https://github.com/prometheus/prometheus/commit/7646cbca328278585be15fa615e22f2a50b47d06)を参照してください。

## 新機能 {#new-features}

### SQL {#sql}

-   **SQLインターフェイスを使用してデータの配置ルールを設定する（実験的機能）**

    データの配置ルールを設定するためのSQLインターフェイスを提供する`[CREATE | ALTER] PLACEMENT POLICY`の構文をサポートします。この機能を使用すると、特定のリージョン、データセンター、ラック、ホスト、またはレプリカカウントルールにスケジュールするテーブルとパーティションを指定できます。これは、低コストと高柔軟性に対するアプリケーションの要求を満たします。一般的なユーザーシナリオは次のとおりです。

    -   異なるアプリケーションの複数のデータベースをマージして、データベースメンテナンスのコストを削減し、ルール構成を通じてアプリケーションリソースの分離を実現します
    -   重要なデータのレプリカ数を増やして、アプリケーションの可用性とデータの信頼性を向上させます
    -   新しいデータをSSDに保存し、古いデータをHHDに保存して、データのアーカイブとストレージのコストを削減します
    -   ホットスポットデータのリーダーを高性能TiKVインスタンスにスケジュールする
    -   コールドデータを低コストのストレージメディアに分離して、コスト効率を向上させます

    [ユーザードキュメント](/placement-rules-in-sql.md) [＃18030](https://github.com/pingcap/tidb/issues/18030)

-   **一時テーブル**

    一時テーブルを作成するための`CREATE [GLOBAL] TEMPORARY TABLE`ステートメントをサポートします。この機能を使用すると、アプリケーションの計算プロセスで生成された一時データを簡単に管理できます。一時データはメモリに保存され、 `tidb_tmp_table_max_size`変数を使用して一時テーブルのサイズを制限できます。 TiDBは、次のタイプの一時テーブルをサポートしています。

    -   グローバル一時テーブル
        -   クラスタのすべてのセッションに表示され、テーブルスキーマは永続的です。
        -   トランザクションレベルのデータ分離を提供します。一時データは、トランザクションでのみ有効です。トランザクションが終了すると、データは自動的に削除されます。
    -   ローカル一時テーブル

        -   現在のセッションでのみ表示され、テーブルスキーマは永続的ではありません。
        -   重複したテーブル名をサポートします。アプリケーションの複雑な命名規則を設計する必要はありません。
        -   セッションレベルのデータ分離を提供します。これにより、より単純なアプリケーションロジックを設計できます。トランザクションが終了すると、一時テーブルは削除されます。

        [ユーザードキュメント](/temporary-tables.md) [＃24169](https://github.com/pingcap/tidb/issues/24169)

-   **`FOR UPDATE OF TABLES`構文をサポートする**

    複数のテーブルを結合するSQLステートメントの場合、TiDBは、 `OF TABLES`に含まれるテーブルに相関する行の悲観的ロックの取得をサポートします。

    [ユーザードキュメント](/sql-statements/sql-statement-select.md) [＃28689](https://github.com/pingcap/tidb/issues/28689)

-   **テーブル属性**

    テーブルまたはパーティションの属性を設定できる`ALTER TABLE [PARTITION] ATTRIBUTES`ステートメントをサポートします。現在、TiDBは`merge_option`属性の設定のみをサポートしています。この属性を追加することにより、リージョンのマージ動作を明示的に制御できます。

    ユーザーシナリオ： `SPLIT TABLE`操作を実行するときに、一定期間（PDパラメーター[`split-merge-interval`](/pd-configuration-file.md#split-merge-interval)によって制御される）後にデータが挿入されない場合、空のリージョンはデフォルトで自動的にマージされます。この場合、リージョンの自動マージを回避するために、テーブル属性を`merge_option=deny`に設定できます。

    [ユーザードキュメント](/table-attributes.md) [＃3839](https://github.com/tikv/pd/issues/3839)

### 安全 {#security}

-   **TiDBダッシュボードで最小特権を持つユーザーの作成をサポートする**

    TiDBダッシュボードのアカウントシステムは、TiDBSQLのアカウントシステムと一致しています。 TiDBダッシュボードにアクセスするユーザーは、TiDBSQLユーザーの特権に基づいて認証および承認されます。したがって、TiDBダッシュボードには、制限された特権、または単に読み取り専用の特権が必要です。最小特権の原則に基づいてTiDBダッシュボードにアクセスするようにユーザーを構成できるため、特権の高いユーザーのアクセスを回避できます。

    TiDBダッシュボードにアクセスしてサインインするための最小特権SQLユーザーを作成することをお勧めします。これにより、特権の高いユーザーのアクセスが回避され、セキュリティが向上します。

    [ユーザードキュメント](/dashboard/dashboard-user.md)

### パフォーマンス {#performance}

-   **PDのタイムスタンプ処理フローを最適化する**

    TiDBは、PD Follower Proxyを有効にし、PDクライアントがバッチでTSOを要求するときに必要なバッチ待機時間を変更することにより、タイムスタンプ処理フローを最適化し、PDのタイムスタンプ処理負荷を軽減します。これにより、システムの全体的なスケーラビリティが向上します。

    -   システム変数[`tidb_enable_tso_follower_proxy`](/system-variables.md#tidb_enable_tso_follower_proxy-new-in-v530)を介してPDフォロワープロキシの有効化または無効化をサポートします。 TSOがPDの負荷が高すぎることを要求するとします。この場合、PDフォロワープロキシを有効にすると、フォロワーのリクエストサイクル中に収集されたTSOリクエストをリーダーノードにバッチ転送できます。このソリューションは、クライアントとリーダー間の直接的なやり取りの数を効果的に減らし、リーダーへの負荷のプレッシャーを減らし、TiDBの全体的なパフォーマンスを向上させることができます。

    > **ノート：**
    >
    > クライアントの数が少なく、PDリーダーのCPU負荷がいっぱいでない場合は、PDフォロワープロキシを有効にすることはお勧めしません。

    -   システム変数[`tidb_tso_client_batch_max_wait_time`](/system-variables.md#tidb_tso_client_batch_max_wait_time-new-in-v530)を使用して、PDクライアントがTSOをバッチ要求するために必要な最大待機時間を設定することをサポートします。この時間の単位はミリ秒です。 PDのTSO要求の負荷が高い場合は、待機時間を長くしてバッチサイズを大きくすることで、負荷を減らしてスループットを向上させることができます。

    > **ノート：**
    >
    > TSO要求の負荷が高くない場合、この変数値を変更することはお勧めしません。

    [ユーザードキュメント](/system-variables.md#tidb_tso_client_batch_max_wait_time-new-in-v530) [＃3149](https://github.com/tikv/pd/issues/3149)

### 安定 {#stability}

-   **一部の店舗が恒久的に損傷した後のオンラインの安全でない回復をサポートする（実験的機能）**

    オンラインデータの安全でないリカバリを実行する`pd-ctl unsafe remove-failed-stores`のコマンドをサポートします。データレプリカの大部分が永続的な損傷（ディスクの損傷など）などの問題に遭遇し、これらの問題が原因でアプリケーションのデータ範囲が読み取りまたは書き込み不能になったとします。この場合、PDに実装されているOnline Unsafe Recovery機能を使用してデータを回復し、データの読み取りまたは書き込みを再度行うことができます。

    TiDBチームのサポートを受けて、機能関連の操作を実行することをお勧めします。

    [ユーザードキュメント](/online-unsafe-recovery.md) [＃10483](https://github.com/tikv/tikv/issues/10483)

### データ移行 {#data-migration}

-   **DMレプリケーションのパフォーマンスが向上**

    MySQLからTiDBへの低レイテンシのデータレプリケーションを保証するために、次の機能をサポートします。

    -   1つの行の複数の更新を1つのステートメントに圧縮します
    -   複数の行のバッチ更新を1つのステートメントにマージします

-   **DM OpenAPIを追加して、DMクラスターをより適切に維持する（実験的機能）**

    DMは、DMクラスタを照会および操作するためのOpenAPI機能を提供します。 [dmctlツール](/dm/dmctl-introduction.md)の機能に似ています。

    現在、DM OpenAPIは実験的機能であり、デフォルトで無効になっています。実稼働環境での使用はお勧めしません。

    [ユーザードキュメント](/dm/dm-open-api.md)

-   **TiDB Lightning Parallel Import**

    TiDB Lightningは、元の機能を拡張するための並列インポート機能を提供します。複数のLightningインスタンスを同時にデプロイして、単一のテーブルまたは複数のテーブルをダウンストリームTiDBに並行してインポートできます。顧客の使用方法を変更することなく、データ移行機能が大幅に向上し、データをよりリアルタイムで移行して、さらに処理、統合、分析することができます。エンタープライズデータ管理の効率を向上させます。

    私たちのテストでは、10個のTiDB Lightningインスタンスを使用して、合計20個のTiBMySQLデータを8時間以内にTiDBにインポートできます。複数テーブルのインポートのパフォーマンスも向上します。単一のTiDBLightningインスタンスは250GiB/ hでのインポートをサポートでき、全体的な移行は元のパフォーマンスの8倍高速です。

    [ユーザードキュメント](/tidb-lightning/tidb-lightning-distributed-import.md)

-   **TiDBLightningの事前チェック**

    TiDB Lightningには、移行タスクを実行する前に構成を確認する機能があります。デフォルトで有効になっています。この機能は、ディスク容量と実行構成の定期的なチェックを自動的に実行します。主な目的は、後続のインポートプロセス全体がスムーズに行われるようにすることです。

    [ユーザードキュメント](/tidb-lightning/tidb-lightning-prechecks.md)

-   **TiDB Lightningは、GBK文字セットのファイルのインポートをサポートしています**

    ソースデータファイルの文字セットを指定できます。 TiDB Lightningは、インポートプロセス中に、ソースファイルを指定された文字セットからUTF-8エンコーディングに変換します。

    [ユーザードキュメント](/tidb-lightning/tidb-lightning-configuration.md)

-   **Sync-diff-inspectorの改善**

    -   比較速度を375MB/秒から700MB/秒に改善します
    -   比較中にTiDBノードのメモリ消費をほぼ半分に削減します
    -   ユーザーインターフェイスを最適化し、比較中に進行状況バーを表示します

    [ユーザードキュメント](/sync-diff-inspector/sync-diff-inspector-overview.md)

### 診断効率 {#diagnostic-efficiency}

-   **クラスタのオンサイト情報を保存および復元します**

    TiDBクラスタの問題を見つけてトラブルシューティングするときは、多くの場合、システムとクエリプランに関する情報を提供する必要があります。より便利で効率的な方法で情報を取得し、クラスタの問題をトラブルシューティングするのに役立つように、 `PLAN REPLAYER`コマンドがTiDBv5.3.0に導入されました。このコマンドを使用すると、クラスタのオンサイト情報を簡単に保存および復元でき、トラブルシューティングの効率が向上し、管理のために問題をより簡単にアーカイブできます。

    `PLAN REPLAYER`の特徴は次のとおりです。

    -   オンサイトトラブルシューティングでのTiDBクラスタの情報をZIP形式のファイルにエクスポートして保存します。
    -   別のTiDBクラスタからエクスポートされたZIP形式のファイルをクラスタにインポートします。このファイルには、オンサイトトラブルシューティングでの後者のTiDBクラスタの情報が含まれています。

    [ユーザードキュメント](/sql-plan-replayer.md) [＃26325](https://github.com/pingcap/tidb/issues/26325)

### TiDBデータ共有サブスクリプション {#tidb-data-share-subscription}

-   **TiCDC結果整合性レプリケーション**

    TiCDCは、災害シナリオで結果整合性のあるレプリケーション機能を提供します。プライマリTiDBクラスタで災害が発生し、サービスを短期間で再開できない場合、TiCDCはセカンダリクラスタのデータの整合性を確保する機能を提供する必要があります。一方、TiCDCは、データベースが長期間使用できなくなり、ビジネスに影響を与えないように、ビジネスがトラフィックをセカンダリクラスタにすばやく切り替えることができるようにする必要があります。

    この機能は、TiCDCをサポートして、増分データをTiDBクラスタからセカンダリリレーショナルデータベースTiDB / Aurora/ MySQL/MariaDBに複製します。プライマリクラスタがクラッシュした場合、災害前のTiCDCのレプリケーションステータスは正常であり、レプリケーションラグが小さいという条件で、TiCDCは5分以内にセカンダリクラスタをプライマリクラスタの特定のスナップショットに回復できます。 30分未満、つまりRTO &lt;= 5分、RPO&lt;=30分のデータ損失が可能です。

    [ユーザードキュメント](/ticdc/manage-ticdc.md)

-   **TiCDCは、TiCDCタスクを管理するためのHTTPプロトコルOpenAPIをサポートしています**

    TiDB v5.3.0以降、TiCDC OpenAPIは一般可用性（GA）機能になります。実稼働環境でOpenAPIを使用して、TiCDCクラスターを照会および操作できます。

### 展開とメンテナンス {#deployment-and-maintenance}

-   **連続プロファイリング（実験的機能）**

    TiDBダッシュボードは、TiDBクラスターの実行時にインスタンスのパフォーマンス分析結果をリアルタイムで自動的に保存する連続プロファイリング機能をサポートしています。パフォーマンス分析の結果をフレームグラフで確認できます。これにより、より観察しやすくなり、トラブルシューティング時間が短縮されます。

    この機能はデフォルトで無効になっているため、TiDBダッシュボードの[**連続プロファイル**]ページで有効にする必要があります。

    この機能は、TiUPv1.7.0以降を使用してアップグレードまたはインストールされたクラスターでのみ使用できます。

    [ユーザードキュメント](/dashboard/continuous-profiling.md)

## テレメトリー {#telemetry}

TiDBは、TEMPORARYTABLE機能が使用されているかどうかに関する情報をテレメトリレポートに追加します。これには、テーブル名またはテーブルデータは含まれません。

テレメトリとこの動作を無効にする方法の詳細については、 [テレメトリー](/telemetry.md)を参照してください。

## 削除された機能 {#removed-feature}

TiCDC v5.3.0以降、TiDBクラスター間のサイクリックレプリケーション機能（v5.0.0の実験的機能）は削除されました。 TiCDCをアップグレードする前にこの機能を使用してデータを複製したことがある場合、アップグレード後も関連データは影響を受けません。

## 改善 {#improvements}

-   TiDB

    -   コプロセッサーがロックに遭遇したときに、影響を受けるSQLステートメントをデバッグ・ログに表示します。これは、問題の診断に役立ちます[＃27718](https://github.com/pingcap/tidb/issues/27718)
    -   SQL論理層[＃27247](https://github.com/pingcap/tidb/issues/27247)でデータをバックアップおよび復元するときに、バックアップおよび復元データのサイズを表示することをサポートします。
    -   `tidb_analyze_version`が`2`の場合のANALYZEのデフォルトの収集ロジックを改善します。これにより、収集が高速化され、リソースのオーバーヘッドが削減されます。
    -   `ANALYZE TABLE table_name COLUMNS col_1, col_2, ... , col_n`構文を導入します。この構文では、幅の広いテーブルの列の一部についてのみ統計を収集できるため、統計収集の速度が向上します。

-   TiKV

    -   ディスクスペース保護を強化して、ストレージの安定性を向上させます

        ディスクの完全書き込みエラーが発生した場合にTiKVがパニックになる可能性がある問題を解決するために、TiKVは2レベルのしきい値防御メカニズムを導入して、ディスクの残りのスペースが過剰なトラフィックによって使い果たされるのを防ぎます。さらに、このメカニズムは、しきい値がトリガーされたときにスペースを再利用する機能を提供します。残りのスペースのしきい値がトリガーされると、一部の書き込み操作が失敗し、TiKVはディスクフルエラーとディスクフルノードのリストを返します。この場合、スペースを回復してサービスを復元するには、 `Drop/Truncate Table`を実行するか、ノードをスケールアウトします。

    -   L0フロー制御のアルゴリズムを簡素化する[＃10879](https://github.com/tikv/tikv/issues/10879)

    -   ラフトクライアントモジュール[＃10944](https://github.com/tikv/tikv/pull/10944)のエラーログレポートを改善する

    -   ロギングスレッドを改善して、パフォーマンスのボトルネックにならないようにします[＃10841](https://github.com/tikv/tikv/issues/10841)

    -   書き込みクエリの統計タイプをさらに追加する[＃10507](https://github.com/tikv/tikv/issues/10507)

    -   I / O操作をRaftstoreスレッドプールから分離することにより、書き込みレイテンシを短縮します（デフォルトでは無効になっています）。 [＃10540](https://github.com/tikv/tikv/issues/10540)の詳細については、 [TiKVスレッドプールのパフォーマンスを調整する](/tune-tikv-thread-performance.md)を参照してください。

-   PD

    -   ホットスポットスケジューラのQPSディメンションにさらに多くの種類の書き込みクエリを追加する[＃3869](https://github.com/tikv/pd/issues/3869)
    -   スケジューラのパフォーマンスを向上させるために、バランス領域スケジューラの再試行制限を動的に調整することをサポートします[＃3744](https://github.com/tikv/pd/issues/3744)
    -   TiDBダッシュボードをv2021.10.08.1に更新します[＃4070](https://github.com/tikv/pd/pull/4070)
    -   エビクトリーダースケジューラが異常なピアを持つリージョンをスケジュールできることをサポートする[＃4093](https://github.com/tikv/pd/issues/4093)
    -   スケジューラーの終了プロセスを高速化する[＃4146](https://github.com/tikv/pd/issues/4146)

-   TiFlash

    -   TableScanオペレーターの実行効率を大幅に向上させます

    -   交換演算子の実行効率を向上させる

    -   ストレージエンジンのGC中のライトアンプリフィケーションとメモリ使用量を削減します（実験的機能）

    -   TiFlashの再起動時のTiFlashの安定性と可用性を向上させ、再起動後に発生する可能性のあるクエリの失敗を減らします

    -   複数の新しい文字列および時間関数をMPPエンジンにプッシュダウンすることをサポート

        -   文字列関数：LIKEパターン、FORMAT（）、LOWER（）、LTRIM（）、RTRIM（）、SUBSTRING_INDEX（）、TRIM（）、UCASE（）、UPPER（）
        -   数学関数：ROUND（decimal、int）
        -   日付と時刻の関数：HOUR（）、MICROSECOND（）、MINUTE（）、SECOND（）、SYSDATE（）
        -   型変換関数：CAST（時間、実数）
        -   集計関数：GROUP_CONCAT（）、SUM（列挙型）

    -   512ビットSIMDをサポート

    -   古いデータのクリーンアップアルゴリズムを強化して、ディスク使用量を減らし、ファイルをより効率的に読み取る

    -   一部のLinux以外のシステムでダッシュボードにメモリまたはCPU情報が表示されない問題を修正します

    -   TiFlashログファイルの命名スタイルを統一し（命名スタイルをTiKVの命名スタイルと一致させてください）、logger.countとlogger.sizeの動的な変更をサポートします

    -   列ベースのファイルのデータ検証機能を改善します（チェックサム、実験的機能）

-   ツール

    -   TiCDC

        -   Kafkaシンク構成アイテム`MaxMessageBytes`のデフォルト値を64MBから1MBに減らして、大きなメッセージが[＃3104](https://github.com/pingcap/tiflow/pull/3104)によって拒否される問題を修正します。
        -   [＃3037](https://github.com/pingcap/tiflow/pull/3037)パイプ[＃2726](https://github.com/pingcap/tiflow/pull/2726)のメモリ使用量を削減する[＃2553](https://github.com/pingcap/tiflow/issues/2553)
        -   監視項目とアラートルールを最適化して、同期リンク、メモリGC、およびストックデータスキャンプロセスの可観測性を向上させます[＃2735](https://github.com/pingcap/tiflow/pull/2735) [＃1606](https://github.com/pingcap/tiflow/issues/1606) [＃3000](https://github.com/pingcap/tiflow/pull/3000) [＃2985](https://github.com/pingcap/tiflow/issues/2985) [＃2156](https://github.com/pingcap/tiflow/issues/2156)
        -   同期タスクのステータスが正常な場合、誤解を招くユーザーを避けるために、履歴エラーメッセージは表示されなくなります[＃2242](https://github.com/pingcap/tiflow/issues/2242)

## バグの修正 {#bug-fixes}

-   TiDB

    -   間違った実行プランが原因で実行中に発生するエラーを修正します。誤った実行プランは、パーティションテーブルの集計演算子をプッシュダウンするときのスキーマ列の浅いコピーが原因で発生します[＃27797](https://github.com/pingcap/tidb/issues/27797) [＃26554](https://github.com/pingcap/tidb/issues/26554)
    -   `plan cache`が符号なしフラグの変更を検出できない問題を修正します[＃28254](https://github.com/pingcap/tidb/issues/28254)
    -   パーティション関数が範囲[＃28233](https://github.com/pingcap/tidb/issues/28233)外にある場合の誤ったパーティションプルーニングを修正します
    -   プランナーが`join` 、場合によっては[＃28087](https://github.com/pingcap/tidb/issues/28087)の無効なプランをキャッシュする可能性がある問題を修正します
    -   ハッシュ列タイプが`enum`の場合の間違った`IndexLookUpJoin`を[＃27893](https://github.com/pingcap/tidb/issues/27893)
    -   まれに、アイドル状態の接続をリサイクルするとリクエストの送信がブロックされる可能性があるというバッチクライアントのバグを修正します[＃27688](https://github.com/pingcap/tidb/pull/27688)
    -   ターゲットクラスタでチェックサムを実行できない場合のTiDBLightningパニックの問題を修正します[＃27686](https://github.com/pingcap/tidb/pull/27686)
    -   場合によっては`date_add`と`date_sub`の関数の間違った結果を修正します[＃27232](https://github.com/pingcap/tidb/issues/27232)
    -   ベクトル化された式[＃28643](https://github.com/pingcap/tidb/issues/28643)の`hour`関数の誤った結果を修正します
    -   MySQL5.1または古いクライアントバージョン[＃27855](https://github.com/pingcap/tidb/issues/27855)に接続する際の認証の問題を修正します
    -   新しいインデックスが追加されたときに、指定された時間外に自動分析がトリガーされる可能性がある問題を修正します[＃28698](https://github.com/pingcap/tidb/issues/28698)
    -   セッション変数を設定すると`tidb_snapshot`が無効になるバグを修正し[＃28683](https://github.com/pingcap/tidb/pull/28683)
    -   ピア領域が多数欠落しているクラスターでBRが機能しないバグを修正します[＃27534](https://github.com/pingcap/tidb/issues/27534)
    -   サポートされていない`cast`がTiFlash5にプッシュダウンされたときの`tidb_cast to Int32 is not supported`などの予期しないエラーを修正し[＃23907](https://github.com/pingcap/tidb/issues/23907)
    -   `%s value is out of range in '%s'`エラーメッセージ[＃27964](https://github.com/pingcap/tidb/issues/27964)で`DECIMAL overflow`が欠落している問題を修正します。
    -   一部のコーナーケースでMPPノードの可用性検出が機能しないバグを修正します[＃3118](https://github.com/pingcap/tics/issues/3118)
    -   35を割り当てるときの`DATA RACE` [＃27952](https://github.com/pingcap/tidb/issues/27952)問題を修正し`MPP task ID`
    -   空の[＃28250](https://github.com/pingcap/tidb/issues/28250)を削除した後のMPPクエリの`INDEX OUT OF RANGE`エラーを修正し`dual table`
    -   MPPクエリ[＃1791](https://github.com/pingcap/tics/issues/1791)の誤検知エラーログ`invalid cop task execution summaries length`の問題を修正します
    -   MPPクエリ[＃28149](https://github.com/pingcap/tidb/pull/28149)のエラーログ`cannot found column in Schema column`の問題を修正します
    -   TiFlashがシャットダウンしているときにTiDBがパニックになる可能性がある問題を修正します[＃28096](https://github.com/pingcap/tidb/issues/28096)
    -   安全でない3DES（トリプルデータ暗号化アルゴリズム）ベースのTLS暗号スイートのサポートを削除します[＃27859](https://github.com/pingcap/tidb/pull/27859)
    -   事前チェック中にLightningがオフラインのTiKVノードに接続し、インポートの失敗を引き起こす問題を修正します[＃27826](https://github.com/pingcap/tidb/pull/27826)
    -   多くのファイルをテーブルにインポートするときに事前チェックに時間がかかりすぎる問題を修正します[＃27605](https://github.com/pingcap/tidb/issues/27605)
    -   式を書き換えると、 `between`が間違った照合順序を推測する[＃27146](https://github.com/pingcap/tidb/issues/27146)という問題を修正します。
    -   `group_concat`の関数が照合順序[＃27429](https://github.com/pingcap/tidb/issues/27429)を考慮しなかった問題を修正します
    -   `extract`関数の引数が負の期間[＃27236](https://github.com/pingcap/tidb/issues/27236)である場合に発生する誤った結果を修正します
    -   `NO_UNSIGNED_SUBTRACTION`が設定されている場合にパーティションの作成が失敗する問題を修正します[＃26765](https://github.com/pingcap/tidb/issues/26765)
    -   列のプルーニングと集計のプッシュダウンで副作用のある式を避ける[＃27106](https://github.com/pingcap/tidb/issues/27106)
    -   不要なgRPCログを削除する[＃24190](https://github.com/pingcap/tidb/issues/24190)
    -   精度関連の問題を修正するには、有効な10進数の長さを制限してください[＃3091](https://github.com/pingcap/tics/issues/3091)
    -   `plus`式[＃26977](https://github.com/pingcap/tidb/issues/26977)のオーバーフローをチェックする間違った方法の問題を修正します
    -   `new collation`のデータを含むテーブルから統計をダンプするときの`data too long`のエラーの問題を修正します[＃27024](https://github.com/pingcap/tidb/issues/27024)
    -   再試行されたトランザクションのステートメントが[＃28670](https://github.com/pingcap/tidb/pull/28670)に含まれない問題を修正し`TIDB_TRX`
    -   `plugin_dir`構成[＃28084](https://github.com/pingcap/tidb/issues/28084)の誤ったデフォルト値を修正します
    -   名前付きタイムゾーンとUTCオフセット[＃8311](https://github.com/pingcap/tidb/issues/8311)が指定されている場合、 `CONVERT_TZ`関数が`NULL`を返す問題を修正します。
    -   ステートメント[＃27214](https://github.com/pingcap/tidb/issues/27214)の一部として何も指定されていない場合、 `CREATE SCHEMA`が`character_set_server`および`collation_server`で指定された文字セットを新しいスキーマに使用しないという問題を修正します。

-   TiKV

    -   リージョンの移行時にRaftstoreのデッドロックが原因で発生するTiKVが利用できない問題を修正します。回避策は、スケジューリングを無効にして、使用できない[＃10909](https://github.com/tikv/tikv/issues/10909)を再起動することです。
    -   輻輳エラー[＃11082](https://github.com/tikv/tikv/issues/11082)が原因でCDCがスキャンの再試行を頻繁に追加する問題を修正します
    -   チャネルがいっぱいになるとラフト接続が切断される問題を修正します[＃11047](https://github.com/tikv/tikv/issues/11047)
    -   Raftクライアントの実装でバッチメッセージが大きすぎるという問題を修正します[＃9714](https://github.com/tikv/tikv/issues/9714)
    -   一部のコルーチンが[＃10965](https://github.com/tikv/tikv/issues/10965)でリークする問題を修正し`resolved_ts`
    -   応答のサイズが[＃9012](https://github.com/tikv/tikv/issues/9012)を超えたときにコプロセッサーに発生するパニックの問題を修正します。
    -   スナップショットファイルをガベージコレクションできない場合に、スナップショットガベージコレクション（GC）がGCスナップショットファイルを見逃す問題を修正します[＃10813](https://github.com/tikv/tikv/issues/10813)
    -   コプロセッサー要求を処理するときのタイムアウトによって引き起こされるパニックの問題を修正します[＃10852](https://github.com/tikv/tikv/issues/10852)
    -   統計スレッド[＃11195](https://github.com/tikv/tikv/issues/11195)の監視データによって引き起こされるメモリリークを修正します
    -   一部のプラットフォームからcgroup情報を取得することによって引き起こされるパニックの問題を修正します[＃10980](https://github.com/tikv/tikv/pull/10980)
    -   MVCC削除バージョンが圧縮フィルターGC1によってドロップされないため、スキャンパフォーマンスが低下する問題を修正し[＃11248](https://github.com/tikv/tikv/pull/11248) 。

-   PD

    -   ピアの数が設定されたピアの数を超えているために、PDがデータを持ち保留状態のピアを誤って削除する問題を修正します[＃4045](https://github.com/tikv/pd/issues/4045)
    -   PDが時間内にピアを修正しないという問題を修正します[＃4077](https://github.com/tikv/pd/issues/4077)
    -   散布範囲スケジューラが空のリージョン[＃4118](https://github.com/tikv/pd/pull/4118)をスケジュールできない問題を修正します
    -   キーマネージャのCPUコストが高すぎるという問題を修正します[＃4071](https://github.com/tikv/pd/issues/4071)
    -   ホットリージョンスケジューラの構成を設定するときに発生する可能性のあるデータ競合の問題を修正します[＃4159](https://github.com/tikv/pd/issues/4159)
    -   スタックしたリージョンシンカー[＃3936](https://github.com/tikv/pd/issues/3936)によって引き起こされる遅いリーダー選出を修正

-   TiFlash

    -   不正確なTiFlashストアサイズ統計の問題を修正します
    -   ライブラリ`nsl`がないために、一部のプラットフォームでTiFlashが起動しない問題を修正します。
    -   書き込みの負荷が大きい場合（デフォルトのタイムアウト5分が追加されます）、 `wait index`の無限待機をブロックします。これにより、TiFlashがデータレプリケーションがサービスを提供するのを長時間待機するのを防ぎます。
    -   ログボリュームが大きい場合のログ検索の速度が遅く、結果が出ない問題を修正します
    -   古い履歴ログを検索するときに最新のログしか検索できない問題を修正します
    -   新しい照合順序が有効になっているときに発生する可能性のある間違った結果を修正します
    -   SQLステートメントに非常に長いネストされた式が含まれている場合に発生する可能性のある解析エラーを修正します
    -   Exchange演算子の考えられる`Block schema mismatch`のエラーを修正します
    -   10進数タイプを比較するときに発生する可能性のある`Can't compare`のエラーを修正します
    -   `left/substring`関数の`3rd arguments of function substringUTF8 must be constants`エラーを修正

-   ツール

    -   TiCDC

        -   アップストリームTiDBインスタンスが予期せず終了したときにTiCDCレプリケーションタスクが終了する可能性がある問題を修正します[＃3061](https://github.com/pingcap/tiflow/issues/3061)
        -   TiKVが同じリージョン[＃2386](https://github.com/pingcap/tiflow/issues/2386)に重複するリクエストを送信すると、TiCDCプロセスがパニックになる可能性がある問題を修正します。
        -   ダウンストリームのTiDB/MySQLの可用性を確認する際の不要なCPU消費を修正[＃3073](https://github.com/pingcap/tiflow/issues/3073)
        -   TiCDCによって生成されるKafkaメッセージの量が[＃2962](https://github.com/pingcap/tiflow/issues/2962)によって制約されないという問題を修正し`max-message-size`
        -   Kafkaメッセージの書き込み中にエラーが発生したときにTiCDC同期タスクが一時停止する可能性がある問題を修正します[＃2978](https://github.com/pingcap/tiflow/issues/2978)
        -   `force-replicate`が有効になっている場合、有効なインデックスのない一部のパーティションテーブルが無視される可能性がある問題を修正します[＃2834](https://github.com/pingcap/tiflow/issues/2834)
        -   ストックデータのスキャンに時間がかかりすぎると、TiKVがGCを実行するためにストックデータのスキャンが失敗する可能性がある問題を修正します[＃2470](https://github.com/pingcap/tiflow/issues/2470)
        -   一部のタイプの列をOpenProtocol形式にエンコードするときに発生する可能性のあるパニックの問題を修正します[＃2758](https://github.com/pingcap/tiflow/issues/2758)
        -   一部のタイプの列をAvro形式[＃2648](https://github.com/pingcap/tiflow/issues/2648)にエンコードするときに発生する可能性のあるパニックの問題を修正します

    -   TiDB Binlog

        -   ほとんどのテーブルが除外されると、特別な負荷がかかった状態でチェックポイントを更新できないという問題を修正します[＃1075](https://github.com/pingcap/tidb-binlog/pull/1075)
