---
title: TiDB 5.4 Release Notes
---

# TiDB5.4リリースノート {#tidb-5-4-release-notes}

発売日：2022年2月15日

TiDBバージョン：5.4.0

v5.4では、主な新機能または改善点は次のとおりです。

-   GBK文字セットをサポートする
-   複数の列のインデックスのフィルタリング結果をマージするデータへのアクセスにインデックスマージを使用することをサポートします
-   セッション変数を使用した古いデータの読み取りをサポート
-   統計を収集するための構成の永続化をサポート
-   TiKVのログストレージRaft EngineとしてのRaftEngineの使用のサポート（実験的）
-   クラスタへのバックアップの影響を最適化する
-   バックアップストレージとしてのAzureBlobストレージの使用のサポート
-   TiFlashとMPPエンジンの安定性とパフォーマンスを継続的に改善します
-   TiDB Lightningにスイッチを追加して、データを含む既存のテーブルへのインポートを許可するかどうかを決定します
-   連続プロファイリング機能の最適化（実験的）
-   TiSparkはユーザーの識別と認証をサポートします

## 互換性の変更 {#compatibility-changes}

> **ノート：**
>
> 以前のTiDBバージョンからv5.4.0にアップグレードするときに、すべての中間バージョンの互換性変更に関する注意事項を知りたい場合は、対応するバージョンの[リリースノート](/releases/release-notes.md)を確認できます。

### システム変数 {#system-variables}

| 変数名                                                                                                 | タイプを変更する   | 説明                                                                                                                                                                                                                                                                                                                                         |
| :-------------------------------------------------------------------------------------------------- | :--------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`tidb_enable_column_tracking`](/system-variables.md#tidb_enable_column_tracking-new-in-v540)       | 新しく追加されました | TiDBが`PREDICATE COLUMNS`を収集できるようにするかどうかを制御します。デフォルト値は`OFF`です。                                                                                                                                                                                                                                                                              |
| [`tidb_enable_paging`](/system-variables.md#tidb_enable_paging-new-in-v540)                         | 新しく追加されました | `IndexLookUp`のオペレーターでコプロセッサー要求を送信するためにページングの方法を使用するかどうかを制御します。デフォルト値は`OFF`です。<br/> `IndexLookup`と`Limit`を使用し、 `Limit`を`IndexScan`にプッシュダウンできない読み取りクエリの場合、読み取りクエリの待機時間が長くなり、TiKVの`unified read pool`のCPU使用率が高くなる可能性があります。このような場合、 `Limit`演算子は少量のデータセットしか必要としないため、 `tidb_enable_paging`を`ON`に設定すると、TiDBが処理するデータが少なくなり、クエリの待機時間とリソース消費が削減されます。 |
| [`tidb_enable_top_sql`](/system-variables.md#tidb_enable_top_sql-new-in-v540)                       | 新しく追加されました | Top SQL機能を有効にするかどうかを制御します。デフォルト値は`OFF`です。                                                                                                                                                                                                                                                                                                  |
| [`tidb_persist_analyze_options`](/system-variables.md#tidb_persist_analyze_options-new-in-v540)     | 新しく追加されました | [ANALYZE構成の永続性](/statistics.md#persist-analyze-configurations)機能を有効にするかどうかを制御します。デフォルト値は`ON`です。                                                                                                                                                                                                                                            |
| [`tidb_read_staleness`](/system-variables.md#tidb_read_staleness-new-in-v540)                       | 新しく追加されました | 現在のセッションで読み取ることができる履歴データの範囲を制御します。デフォルト値は`0`です。                                                                                                                                                                                                                                                                                            |
| [`tidb_regard_null_as_point`](/system-variables.md#tidb_regard_null_as_point-new-in-v540)           | 新しく追加されました | オプティマイザが、インデックスアクセスのプレフィックス条件としてnull等価を含むクエリ条件を使用できるかどうかを制御します。                                                                                                                                                                                                                                                                            |
| [`tidb_stats_load_sync_wait`](/system-variables.md#tidb_stats_load_sync_wait-new-in-v540)           | 新しく追加されました | 統計の同期ロード機能を有効にするかどうかを制御します。デフォルト値`0`は、機能が無効になっていて、統計が非同期にロードされることを意味します。この機能が有効になっている場合、この変数は、SQL最適化がタイムアウトする前に統計の同期ロードを待機できる最大時間を制御します。                                                                                                                                                                                                   |
| [`tidb_stats_load_pseudo_timeout`](/system-variables.md#tidb_stats_load_pseudo_timeout-new-in-v540) | 新しく追加されました | SQLが失敗するか（ `OFF` ）、疑似統計の使用にフォールバックするか（ `ON` ）、統計の同期ロードがタイムアウトに達するタイミングを制御します。デフォルト値は`OFF`です。                                                                                                                                                                                                                                               |
| [`tidb_backoff_lock_fast`](/system-variables.md#tidb_backoff_lock_fast)                             | 変更         | デフォルト値は`100`から`10`に変更されます。                                                                                                                                                                                                                                                                                                                 |
| [`tidb_enable_index_merge`](/system-variables.md#tidb_enable_index_merge-new-in-v40)                | 変更         | デフォルト値は`OFF`から`ON`に変更されます。<br/><ul><li> TiDBクラスタをv4.0.0より前のバージョンからv5.4.0以降にアップグレードする場合、この変数はデフォルトで`OFF`です。</li><li> TiDBクラスタをv4.0.0以降からv5.4.0以降にアップグレードする場合、この変数はアップグレード前と同じままです。</li><li> v5.4.0以降の新しく作成されたTiDBクラスターの場合、この変数はデフォルトで`ON`です。</li></ul>                                                                                      |
| [`tidb_store_limit`](/system-variables.md#tidb_store_limit-new-in-v304-and-v40)                     | 変更         | v5.4.0より前では、この変数はインスタンスレベルおよびグローバルに構成できました。 v5.4.0以降、この変数はグローバル構成のみをサポートします。                                                                                                                                                                                                                                                               |

### Configuration / コンフィグレーションファイルのパラメーター {#configuration-file-parameters}

| Configuration / コンフィグレーションファイル | Configuration / コンフィグレーション                                                                                      | タイプを変更する   | 説明                                                                                                                                                                                                                                                                                                                    |
| :----------------------------- | :-------------------------------------------------------------------------------------------------------------- | :--------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB                           | [`stats-load-concurrency`](/tidb-configuration-file.md#stats-load-concurrency-new-in-v540)                      | 新しく追加されました | TiDB同期ロード統計機能が同時に処理できる列の最大数を制御します。デフォルト値は`5`です。                                                                                                                                                                                                                                                                       |
| TiDB                           | [`stats-load-queue-size`](/tidb-configuration-file.md#stats-load-queue-size-new-in-v540)                        | 新しく追加されました | TiDB同期ロード統計機能がキャッシュできる列要求の最大数を制御します。デフォルト値は`1000`です。                                                                                                                                                                                                                                                                  |
| TiKV                           | [`snap-generator-pool-size`](/tikv-configuration-file.md#snap-generator-pool-size-new-in-v540)                  | 新しく追加されました | `snap-generator`スレッドプールのサイズ。デフォルト値は`2`です。                                                                                                                                                                                                                                                                             |
| TiKV                           | `log.file.max-size` `log.file.max-days` `log.file.max-backups`                                                  | 新しく追加されました | 詳細については、 [TiKVConfiguration / コンフィグレーションファイル`log.file`](/tikv-configuration-file.md#logfile-new-in-v540)を参照してください。                                                                                                                                                                                                    |
| TiKV                           | `raft-engine`                                                                                                   | 新しく追加されました | `enable` `recovery-mode` `target-file-size` `bytes-per-sync` `recovery-read-block-size` `purge-threshold` `recovery-read-block-size` `batch-compression-threshold` `recovery-threads` `dir`詳細については、 [TiKVConfiguration / コンフィグレーションファイル-raft `raft-engine`](/tikv-configuration-file.md#raft-engine)を参照してください。        |
| TiKV                           | [`backup.enable-auto-tune`](/tikv-configuration-file.md#enable-auto-tune-new-in-v540)                           | 新しく追加されました | v5.3.0では、デフォルト値は`false`です。 v5.4.0以降、デフォルト値は`true`に変更されています。このパラメーターは、クラスタリソースの使用率が高い場合に、バックアップタスクで使用されるリソースを制限して、クラスタへの影響を減らすかどうかを制御します。デフォルト構成では、バックアップタスクの速度が低下する可能性があります。                                                                                                                                          |
| TiKV                           | `log-level` `log-format` `log-file` `log-rotation-size`                                                         | 変更         | TiKVログパラメータの名前は、 `log.enable-timestamp` `log.level` `log.format`置き換えられ`log.file.filename` 。古いパラメータのみを設定し、それらの値がデフォルト以外の値に設定されている場合、古いパラメータは新しいパラメータとの互換性を維持します。古いパラメータと新しいパラメータの両方が設定されている場合、新しいパラメータが有効になります。詳細については、 [TiKVConfiguration / コンフィグレーションファイル-ログ](/tikv-configuration-file.md#log-new-in-v540)を参照してください。 |
| TiKV                           | `log-rotation-timespan`                                                                                         | 削除         | ログローテーション間のタイムスパン。このタイムスパンが経過すると、ログファイルがローテーションされます。つまり、現在のログファイルのファイル名にタイムスタンプが追加され、新しいログファイルが作成されます。                                                                                                                                                                                                                |
| TiKV                           | `allow-remove-leader`                                                                                           | 削除         | メインスイッチの削除を許可するかどうかを決定します。                                                                                                                                                                                                                                                                                            |
| TiKV                           | `raft-msg-flush-interval`                                                                                       | 削除         | Raftメッセージがバッチで送信される間隔を決定します。 Raftメッセージは、この構成アイテムで指定された間隔ごとにバッチで送信されます。                                                                                                                                                                                                                                                |
| PD                             | [`log.level`](/pd-configuration-file.md#level)                                                                  | 変更         | デフォルト値は「INFO」から「info」に変更され、大文字と小文字が区別されないことが保証されています。                                                                                                                                                                                                                                                                 |
| TiFlash                        | [`profile.default.enable_elastic_threadpool`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file) | 新しく追加されました | エラスティックスレッドプール機能を有効にするか無効にするかを決定します。この構成アイテムを有効にすると、同時実行性の高いシナリオでTiFlashCPU使用率を大幅に向上させることができます。デフォルト値は`false`です。                                                                                                                                                                                                      |
| TiFlash                        | [`storage.format_version`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                    | 新しく追加されました | DTFileのバージョンを指定します。デフォルト値は`2`で、その下にハッシュがデータファイルに埋め込まれます。値を`3`に設定することもできます。 `3`の場合、データファイルにはメタデータとトークンデータのチェックサムが含まれ、複数のハッシュアルゴリズムをサポートします。                                                                                                                                                                            |
| TiFlash                        | [`logger.count`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                              | 変更         | デフォルト値は`10`に変更されます。                                                                                                                                                                                                                                                                                                   |
| TiFlash                        | [`status.metrics_port`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                       | 変更         | デフォルト値は`8234`に変更されます。                                                                                                                                                                                                                                                                                                 |
| TiFlash                        | [`raftstore.apply-pool-size`](/tiflash/tiflash-configuration.md#configure-the-tiflash-learnertoml-file)         | 新しく追加されました | Raftデータをストレージにフラッシュするプール内のスレッドの許容数。デフォルト値は`4`です。                                                                                                                                                                                                                                                                      |
| TiFlash                        | [`raftstore.store-pool-size`](/tiflash/tiflash-configuration.md#configure-the-tiflash-learnertoml-file)         | 新しく追加されました | Raftを処理するスレッドの許容数。これはRaftstoreスレッドプールのサイズです。デフォルト値は`4`です。                                                                                                                                                                                                                                                             |
| TiDBデータ移行（DM）                  | [`collation_compatible`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)         | 新しく追加されました | `CREATE`のSQLステートメントでデフォルトの照合順序を同期するモード。値のオプションは「loose」（デフォルト）と「strict」です。                                                                                                                                                                                                                                             |
| TiCDC                          | `max-message-bytes`                                                                                             | 変更         | Kafkaシンクのデフォルト値`max-message-bytes`を`104857601` （10MB）に変更します                                                                                                                                                                                                                                                           |
| TiCDC                          | `partition-num`                                                                                                 | 変更         | KafkaSinkのデフォルト値`partition-num`を`4`から`3`に変更します。これにより、TiCDCはKafakaパーティションにメッセージをより均等に送信します。                                                                                                                                                                                                                            |
| TiDB Lightning                 | `meta-schema-name`                                                                                              | 変更         | ターゲットTiDBのメタデータのスキーマ名を指定します。 v5.4.0以降、このスキーマは[並列インポート](/tidb-lightning/tidb-lightning-distributed-import.md)を有効にした場合にのみ作成されます（対応するパラメーターは`tikv-importer.incremental-import = true`です）。                                                                                                                                |
| TiDB Lightning                 | `task-info-schema-name`                                                                                         | 新しく追加されました | TiDBLightningが競合を検出したときに重複データが保存されるデータベースの名前を指定します。デフォルトでは、値は「lightning_task_info」です。このパラメーターは、「重複解決」機能を有効にしている場合にのみ指定してください。                                                                                                                                                                                         |
| TiDB Lightning                 | `incremental-import`                                                                                            | 新しく追加されました | データがすでに存在するテーブルへのデータのインポートを許可するかどうかを決定します。デフォルト値は`false`です。                                                                                                                                                                                                                                                           |

### その他 {#others}

-   TiDBとPDの間にインターフェースが追加されます。 `information_schema.TIDB_HOT_REGIONS_HISTORY`システムテーブルを使用する場合、TiDBは対応するバージョンのPDを使用する必要があります。
-   TiDBサーバー、PDサーバー、およびTiKVサーバーは、ログに関連するパラメーターに統一された命名方法を使用して、ログ名、出力形式、およびローテーションと有効期限のルールを管理し始めます。詳細については、 [TiKV構成ファイル-ログ](/tikv-configuration-file.md#log-new-in-v540)を参照してください。
-   v5.4.0以降、プランキャッシュを介してキャッシュされた実行プランのSQLバインディングを作成すると、バインディングは、対応するクエリに対してすでにキャッシュされているプランを無効にします。新しいバインディングは、v5.4.0より前にキャッシュされた実行プランには影響しません。
-   v5.3以前のバージョンでは、 [TiDBデータ移行（DM）](https://docs.pingcap.com/tidb-data-migration/v5.3/)のドキュメントはTiDBドキュメントから独立しています。 v5.4以降、DMドキュメントは同じバージョンのTiDBドキュメントに統合されています。 DMドキュメントサイトにアクセスしなくても、 [DMドキュメント](/dm/dm-overview.md)を直接読むことができます。
-   cdclogとともに、ポイントインタイムリカバリ（PITR）の実験的機能を削除します。 v5.4.0以降、cdclogベースのPITRおよびcdclogはサポートされなくなりました。
-   システム変数を「DEFAULT」に設定する動作をよりMySQL互換にします[＃29680](https://github.com/pingcap/tidb/pull/29680)
-   システム変数`lc_time_names`を読み取り専用[＃30084](https://github.com/pingcap/tidb/pull/30084)に設定します
-   `tidb_store_limit`のスコープをINSTANCEまたはGLOBALからGLOBAL3に設定し[＃30756](https://github.com/pingcap/tidb/pull/30756)
-   列にゼロが含まれている場合、整数型の列を時間型の列に変換することを禁止します[＃25728](https://github.com/pingcap/tidb/pull/25728)
-   浮動小数点値を挿入するときに`Inf`または`NAN`の値でエラーが報告されない問題を修正します[＃30148](https://github.com/pingcap/tidb/pull/30148)
-   自動IDが範囲[＃30301](https://github.com/pingcap/tidb/pull/30301)から外れると、 `REPLACE`ステートメントが他の行を誤って変更する問題を修正します。

## 新機能 {#new-features}

### SQL {#sql}

-   **TiDBは、v5.4.0以降のGBK文字セットをサポートしています**

    `latin1`より前では、 `binary`は`ascii` 、および`utf8`文字セットをサポートしてい`utf8mb4` 。

    中国語ユーザーをより適切にサポートするために、TiDBはv5.4.0以降のGBK文字セットをサポートしています。 TiDBクラスタを初めて初期化するときにTiDB構成ファイルで[`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap)オプションを有効にした後、TiDBGBK文字セットは`gbk_bin`と`gbk_chinese_ci`の両方の照合をサポートします。

    GBK文字セットを使用する場合は、互換性の制限に注意する必要があります。詳細については、 [文字セットと照合-GBK](/character-set-gbk.md)を参照してください。

### 安全 {#security}

-   **TiSparkはユーザー認証と承認をサポートします**

    TiSpark 2.5.0以降、TiSparkは、データベースユーザー認証とデータベースまたはテーブルレベルでの読み取り/書き込み認証の両方をサポートしています。この機能を有効にすると、データを取得するための描画など、ビジネスが不正なバッチタスクを実行するのを防ぐことができます。これにより、オンラインクラスターの安定性とデータセキュリティが向上します。

    この機能はデフォルトで無効になっています。有効になっている場合、TiSparkを介して操作しているユーザーに必要な権限がない場合、ユーザーはTiSparkから例外を受け取ります。

    [ユーザードキュメント](/tispark-overview.md#security)

-   **TiUPは、rootユーザーの初期パスワードの生成をサポートしています**

    クラスタを起動するためのコマンドに`--init`つのパラメータが導入されています。このパラメーターを使用すると、TiUPを使用してデプロイされたTiDBクラスタで、TiUPはデータベースrootユーザーの初期の強力なパスワードを生成します。これにより、パスワードが空のrootユーザーを使用する際のセキュリティリスクが回避され、データベースのセキュリティが確保されます。

    [ユーザードキュメント](/production-deployment-using-tiup.md#step-7-start-a-tidb-cluster)

### パフォーマンス {#performance}

-   **列指向ストレージエンジンTiFlashとコンピューティングエンジンMPPの安定性とパフォーマンスを継続的に改善します**

    -   MPPエンジンへのより多くの機能の融合をサポートします。

        -   文字列`RPAD()` `STRCMP()` `LPAD()`
        -   `SUBDATE()` `QUARTER()` `DATE_SUB()` `ADDDATE()` `DATE_ADD()`

    -   リソース使用率を改善するためのエラスティックスレッドプール機能の導入（実験的）

    -   TiKVからデータを複製するときに、行ベースのストレージ形式から列ベースのストレージ形式にデータを変換する効率を向上させます。これにより、データ複製の全体的なパフォーマンスが50％向上します。

    -   一部の構成アイテムのデフォルト値を調整することにより、TiFlashのパフォーマンスと安定性を向上させます。 HTAPハイブリッドロードでは、単一のテーブルに対する単純なクエリのパフォーマンスが最大20％向上します。

    ユーザー[tiflash.tomlファイルを構成します](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file) ： [サポートされているプッシュダウン計算](/tiflash/tiflash-supported-pushdown-calculations.md)

-   **セッション変数を介して指定された時間範囲内の履歴データを読み取ります**

    TiDBは、Raftコンセンサスアルゴリズムに基づくマルチレプリカ分散データベースです。同時実行性とスループットが高いアプリケーションシナリオに直面した場合、TiDBは、フォロワーレプリカを介して読み取りパフォーマンスをスケールアウトし、読み取り要求と書き込み要求を分離できます。

    さまざまなアプリケーションシナリオに対して、TiDBはフォロワー読み取りの2つのモードを提供します。強一貫性のある読み取りと弱一貫性のある履歴の読み取りです。強一貫性のある読み取りモードは、リアルタイムデータを必要とするアプリケーションシナリオに適しています。ただし、このモードでは、リーダーとフォロワー間のデータレプリケーションのレイテンシーとスループットの低下により、特に地理的に分散された展開では、読み取りリクエストのレイテンシーが高くなる可能性があります。

    リアルタイムデータに対する要件がそれほど厳しくないアプリケーションシナリオでは、履歴読み取りモードをお勧めします。このモードは、待ち時間を短縮し、スループットを向上させることができます。 TiDBは現在、次の方法による履歴データの読み取りをサポートしています。SQLステートメントを使用して、過去のある時点からデータを読み取るか、過去の時点に基づいて読み取り専用トランザクションを開始します。どちらの方法も、特定の時点または指定された時間範囲内の履歴データの読み取りをサポートしています。詳しくは[`AS OF TIMESTAMP`句を使用して履歴データを読み取る](/as-of-timestamp.md)をご覧ください。

    v5.4.0以降、TiDBは、セッション変数を介して指定された時間範囲内の履歴データの読み取りをサポートすることにより、履歴読み取りモードの使いやすさを向上させます。このモードは、準リアルタイムのシナリオで低遅延、高スループットの読み取り要求を処理します。変数は次のように設定できます。

    ```sql
    set @@tidb_replica_read=leader_and_follower
    set @@tidb_read_staleness="-5"
    ```

    この設定により、TiDBは最も近いリーダーまたはフォロワーノードを選択し、5秒以内に最新の履歴データを読み取ることができます。

    [ユーザードキュメント](/tidb-read-staleness.md)

-   **インデックスマージのGA**

    インデックスマージは、SQL最適化の実験的機能としてTiDBv4.0に導入されました。このメソッドは、クエリで複数列のデータのスキャンが必要な場合に、条件フィルタリングを大幅に高速化します。例として次のクエリを取り上げます。 `WHERE`ステートメントで、 `OR`で接続されたフィルタリング条件の列*key1*と<em>key2</em>にそれぞれのインデックスがある場合、インデックスマージ機能は、それぞれのインデックスを同時にフィルタリングし、クエリ結果をマージして、マージされた結果を返します。

    ```sql
    SELECT * FROM table WHERE key1 <= 100 OR key2 = 200;
    ```

    TiDB v4.0より前では、テーブルに対するクエリは、一度に1つのインデックスのみを使用してフィルタリングすることをサポートしていました。データの複数の列をクエリする場合は、インデックスマージを有効にして、個々の列のインデックスを使用することにより、正確なクエリ結果を短時間で取得できます。インデックスマージは、不要な全表スキャンを回避し、多数の複合インデックスを確立する必要がありません。

    v5.4.0では、インデックスマージはGAになります。ただし、次の制限に注意する必要があります。

    -   インデックスマージは、選言標準形（ <sub>X1⋁X2⋁</sub> <sub>…</sub> <sub>Xn</sub> ）のみをサポートします。つまり、この機能は、 `WHERE`句のフィルタリング条件が`OR`で接続されている場合にのみ機能します。

    -   v5.4.0以降の新しくデプロイされたTiDBクラスターの場合、この機能はデフォルトで有効になっています。以前のバージョンからアップグレードされたv5.4.0以降のTiDBクラスターの場合、この機能はアップグレード前の設定を継承し、必要に応じて設定を変更できます（v4.0より前のTiDBクラスターの場合、この機能は存在せず、デフォルトで無効になっています） 。

    [ユーザードキュメント](/explain-index-merge.md)

-   **Raft Engineのサポート（実験的）**

    TiKVのログストレージエンジンとして[Raft Engine](https://github.com/tikv/raft-engine)を使用することをサポートします。 RocksDBと比較して、 Raft EngineはTiKVI / O書き込みトラフィックを最大40％、CPU使用率を10％削減し、特定の負荷の下でフォアグラウンドスループットを約5％向上させ、テールレイテンシーを20％削減します。さらに、 Raft Engineはログのリサイクルの効率を改善し、極端な状況でのログの蓄積の問題を修正します。

    Raft Engineはまだ実験的機能であり、デフォルトでは無効になっています。 Raft EngineのRaftEngineのデータ形式は、以前のバージョンと互換性がないことに注意してください。クラスタをアップグレードする前に、すべてのTiKVノードでRaft Engineが無効になっていることを確認する必要があります。 RaftEngineはRaft Engine以降のバージョンでのみ使用することをお勧めします。

    [ユーザードキュメント](/tikv-configuration-file.md#raft-engine)

-   **`PREDICATE COLUMNS`に関する統計の収集をサポート（実験的）**

    ほとんどの場合、SQLステートメントを実行するとき、オプティマイザーは一部の列（ `WHERE` 、および`JOIN` `GROUP BY`の列など）の統計のみを使用し`ORDER BY` 。これらの使用される列は`PREDICATE COLUMNS`と呼ばれます。

    v5.4.0以降、 [`tidb_enable_column_tracking`](/system-variables.md#tidb_enable_column_tracking-new-in-v540)システム変数の値を`ON`に設定して、TiDBが`PREDICATE COLUMNS`を収集できるようにすることができます。

    設定後、TiDBは100* [`stats-lease`](/tidb-configuration-file.md#stats-lease)ごとに`PREDICATE COLUMNS`の情報を`mysql.column_stats_usage`のシステムテーブルに書き込みます。ビジネスのクエリパターンが安定している場合は、 `ANALYZE TABLE TableName PREDICATE COLUMNS`構文を使用して、 `PREDICATE COLUMNS`列のみの統計を収集できます。これにより、統計収集のオーバーヘッドを大幅に削減できます。

    [ユーザードキュメント](/statistics.md#collect-statistics-on-some-columns)

-   **統計の同期読み込みをサポート（実験的）**

    v5.4.0以降、TiDBは同期ロード統計機能を導入しています。この機能はデフォルトで無効になっています。この機能を有効にした後、TiDBは、SQLステートメントの実行時に、大きなサイズの統計（ヒストグラム、TopN、Count-Min Sketch統計など）をメモリに同期的にロードできます。これにより、SQL最適化の統計の完全性が向上します。

    [ユーザードキュメント](/statistics.md#load-statistics)

### 安定 {#stability}

-   **ANALYZE構成の永続化をサポート**

    統計は、オプティマイザーが実行プランを生成するときに参照する基本情報の1つのタイプです。統計の正確さは、生成された実行計画が妥当であるかどうかに直接影響します。統計の正確性を確保するために、テーブル、パーティション、およびインデックスごとに異なるコレクション構成を設定する必要がある場合があります。

    v5.4.0以降、TiDBはいくつかの`ANALYZE`構成の永続化をサポートしています。この機能を使用すると、既存の構成を将来の統計収集に簡単に再利用できます。

    `ANALYZE`構成永続化機能は、デフォルトで有効になっています（システム変数`tidb_analyze_version`は`2`で、 [`tidb_persist_analyze_options`](/system-variables.md#tidb_persist_analyze_options-new-in-v540)はデフォルトで`ON`です）。この機能を使用して、ステートメントを手動で実行するときに、 `ANALYZE`ステートメントで指定された永続性構成を記録できます。記録されると、次にTiDBが統計を自動的に更新するか、これらの構成を指定せずに手動で統計を収集すると、TiDBは記録された構成に従って統計を収集します。

    [ユーザードキュメント](/statistics.md#persist-analyze-configurations)

### 高可用性とディザスタリカバリ {#high-availability-and-disaster-recovery}

-   **クラスタへのバックアップタスクの影響を減らす**

    Backup＆Restore（BR）は、自動調整機能を導入します（デフォルトで有効になっています）。この機能は、クラスタリソースの使用状況を監視し、バックアップタスクで使用されるスレッドの数を調整することで、クラスタへのバックアップタスクの影響を減らすことができます。場合によっては、バックアップ用のクラスタハードウェアリソースを増やして自動調整機能を有効にすると、クラスタへのバックアップタスクの影響を10％以下に制限できます。

    [ユーザードキュメント](/br/br-auto-tune.md)

-   **バックアップのターゲットストレージとしてAzureBlobStorageをサポートする**

    Backup＆Restore（BR）は、リモートバックアップストレージとしてAzureBlobStorageをサポートします。 TiDBをAzureCloudにデプロイすると、クラスタデータをAzureBlobStorageサービスにバックアップできるようになります。

    [ユーザードキュメント](/br/backup-storage-azblob.md)

### データ移行 {#data-migration}

-   **TiDB Lightningには、データを含むテーブルへのデータのインポートを許可するかどうかを決定するための新機能が導入されています。**

    TiDB Lightningでは、構成アイテム`incremental-import`が導入されています。データを含むテーブルへのデータのインポートを許可するかどうかを決定します。デフォルト値は`false`です。並列インポートモードを使用する場合は、構成を`true`に設定する必要があります。

    [ユーザードキュメント](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)

-   **TiDB Lightningは、並列インポート用のメタ情報を格納するスキーマ名を導入します**

    TiDB Lightningは、 `meta-schema-name`の構成アイテムを導入します。並列インポートモードでは、このパラメーターは、ターゲットクラスタの各TiDBLightningインスタンスのメタ情報を格納するスキーマ名を指定します。デフォルトでは、値は「lightning_metadata」です。このパラメーターに設定される値は、同じ並列インポートに参加する各TiDBLightningインスタンスで同じである必要があります。そうしないと、インポートされたデータの正確性を保証できません。

    [ユーザードキュメント](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)

-   **TiDBLightningは重複した解像度を導入します**

    ローカルバックエンドモードでは、TiDB Lightningは、データのインポートが完了する前に重複データを出力し、その重複データをデータベースから削除します。インポートの完了後に重複データを解決し、アプリケーションルールに従って挿入する適切なデータを選択できます。後続の増分データ移行フェーズで検出された重複データによって引き起こされるデータの不整合を回避するために、重複データに基づいてアップストリームデータソースをクリーンアップすることをお勧めします。

    [ユーザードキュメント](/tidb-lightning/tidb-lightning-error-resolution.md)

-   **TiDBデータ移行（DM）でのリレーログの使用を最適化する**

    -   `source`の構成で`enable-relay`のスイッチを回復します。

    -   `start-relay`および`stop-relay`コマンドを使用して、リレーログの動的な有効化と無効化をサポートします。

    -   リレーログのステータスを`source`にバインドします。 `source`は、DMワーカーに移行された後も、有効または無効の元のステータスを維持します。

    -   リレーログのストレージパスをDM-worker構成ファイルに移動します。

    [ユーザードキュメント](/dm/relay-log.md)

-   **DMでの<a href="/character-set-and-collation.md">照合順序</a>の処理を最適化する**

    `collation_compatible`の構成アイテムを追加します。値のオプションは`loose` （デフォルト）と`strict`です：

    -   アプリケーションに照合順序に関する厳密な要件がなく、クエリ結果の照合順序がアップストリームとダウンストリームで異なる可能性がある場合は、デフォルトの`loose`モードを使用してエラーの報告を回避できます。
    -   アプリケーションに照合順序に関する厳しい要件があり、照合順序がアップストリームとダウンストリームの間で一貫している必要がある場合は、 `strict`モードを使用できます。ただし、ダウンストリームがアップストリームのデフォルトの照合順序をサポートしていない場合、データレプリケーションでエラーが報告されることがあります。

    [ユーザードキュメント](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)

-   **DMの`transfer source`を最適化して、レプリケーションタスクのスムーズな実行をサポートします**

    DMワーカーノードの負荷が不均衡な場合、 `transfer source`コマンドを使用して、 `source`の構成を別の負荷に手動で転送できます。最適化後、 `transfer source`コマンドは手動操作を簡素化します。 DMは他の操作を内部で完了するため、関連するすべてのタスクを一時停止するのではなく、ソースをスムーズに転送できます。

-   **DM OpenAPIが一般提供になります（GA）**

    DMは、データソースの追加やタスクの管理など、APIを介した日常の管理をサポートします。 v5.4.0では、DMOpenAPIがGAになります。

    [ユーザードキュメント](/dm/dm-open-api.md)

### 診断効率 {#diagnostic-efficiency}

-   **Top SQL （実験的機能）**

    新しい実験的機能であるTop SQL （デフォルトでは無効）が導入され、ソースを消費するクエリを簡単に見つけることができます。

    [ユーザードキュメント](/dashboard/top-sql.md)

### TiDBデータ共有サブスクリプション {#tidb-data-share-subscription}

-   **クラスターに対するTiCDCの影響を最適化する**

    TiCDCを使用すると、TiDBクラスターのパフォーマンスへの影響が大幅に減少します。テスト環境では、TiDBに対するTiCDCのパフォーマンスへの影響を5％未満に減らすことができます。

### 展開とメンテナンス {#deployment-and-maintenance}

-   **連続プロファイリングの強化（実験的）**

    -   サポートされるその他のコンポーネント：TiDB、PD、およびTiKVに加えて、TiDBv5.4.0はTiFlashのCPUプロファイリングもサポートします。

    -   より多くの形式のプロファイリング表示：フレームチャートでのCPUプロファイリングとGoroutine結果の表示をサポートします。

    -   サポートされるより多くのデプロイメント環境：継続的プロファイリングは、 TiDB Operatorを使用してデプロイされたクラスターにも使用できます。

    継続的プロファイリングはデフォルトで無効になっており、TiDBダッシュボードで有効にできます。

    継続的プロファイリングは、v1.9.0以降のTiUPまたはv1.3.0以降のTiDB Operatorを使用してデプロイまたはアップグレードされたクラスターに適用できます。

    [ユーザードキュメント](/dashboard/continuous-profiling.md)

## 改善 {#improvements}

-   TiDB

    -   キャッシュされたクエリプラン[＃30370](https://github.com/pingcap/tidb/pull/30370)をクリアするための`ADMIN {SESSION | INSTANCE | GLOBAL} PLAN_CACHE`構文をサポートする

-   TiKV

    -   コプロセッサーは、ストリームのような方法でリクエストを処理するためのページングAPIをサポートします[＃11448](https://github.com/tikv/tikv/issues/11448)
    -   `read-through-lock`をサポートして、読み取り操作が2次ロックが解決されるのを待つ必要がないようにします[＃11402](https://github.com/tikv/tikv/issues/11402)
    -   ディスクスペースの枯渇によるパニックを回避するためのディスク保護メカニズムを追加する[＃10537](https://github.com/tikv/tikv/issues/10537)
    -   ログのアーカイブとローテーションのサポート[＃11651](https://github.com/tikv/tikv/issues/11651)
    -   Raftクライアントによるシステムコールを減らし、CPU効率を向上させます[＃11309](https://github.com/tikv/tikv/issues/11309)
    -   コプロセッサーは、部分文字列をTiKV1にプッシュダウンすることをサポートし[＃11495](https://github.com/tikv/tikv/issues/11495)
    -   読み取りコミット分離レベル[＃11485](https://github.com/tikv/tikv/issues/11485)で読み取りロックをスキップすることにより、スキャンパフォーマンスを向上させます
    -   バックアップ操作で使用されるデフォルトのスレッドプールサイズを減らし、ストレスが高い場合はスレッドプールの使用を制限します[＃11000](https://github.com/tikv/tikv/issues/11000)
    -   アプライスレッドプールとストアスレッドプールのサイズの動的調整をサポート[＃11159](https://github.com/tikv/tikv/issues/11159)
    -   `snap-generator`スレッドプール[＃11247](https://github.com/tikv/tikv/issues/11247)のサイズの構成をサポートします。
    -   読み取りと書き込みが頻繁に行われるファイルが多数ある場合に発生するグローバルロック競合の問題を最適化する[＃250](https://github.com/tikv/rocksdb/pull/250)

-   PD

    -   デフォルトで履歴ホットスポット情報を記録する[＃25281](https://github.com/pingcap/tidb/issues/25281)
    -   HTTPコンポーネントの署名を追加して、リクエストソースを識別します[＃4490](https://github.com/tikv/pd/issues/4490)
    -   TiDBダッシュボードをv2021.12.31に更新します[＃4257](https://github.com/tikv/pd/issues/4257)

-   TiFlash

    -   ローカルオペレーターのコミュニケーションを最適化する
    -   スレッドの頻繁な作成または破棄を回避するために、gRPCの非一時的なスレッド数を増やします

-   ツール

    -   バックアップと復元（BR）

        -   BRが暗号化されたバックアップを実行するときにキーの有効性チェックを追加する[＃29794](https://github.com/pingcap/tidb/issues/29794)

    -   TiCDC

        -   「EventFeed再試行レート制限」ログの数を減らす[＃4006](https://github.com/pingcap/tiflow/issues/4006)
        -   多くのテーブルを複製するときの複製待ち時間を短縮する[＃3900](https://github.com/pingcap/tiflow/issues/3900)
        -   TiKVストアがダウンしたときにKVクライアントが回復する時間を短縮する[＃3191](https://github.com/pingcap/tiflow/issues/3191)

    -   TiDBデータ移行（DM）

        -   リレー有効時のCPU使用率を下げる[＃2214](https://github.com/pingcap/dm/issues/2214)

    -   TiDB Lightning

        -   TiDBバックエンドモード[＃30953](https://github.com/pingcap/tidb/pull/30953)でのパフォーマンスを向上させるためにデータを書き込むには、デフォルトで楽観的なトランザクションを使用します

    -   Dumpling

        -   Dumplingがデータベースバージョン[＃29500](https://github.com/pingcap/tidb/pull/29500)をチェックするときの互換性を改善します
        -   `CREATE DATABASE`と[＃3420](https://github.com/pingcap/tiflow/issues/3420)をダンプするときにデフォルトの照合順序を追加し`CREATE TABLE`

## バグの修正 {#bug-fixes}

-   TiDB

    -   クラスタをv4.xから[＃25422](https://github.com/pingcap/tidb/issues/25422)にアップグレードするときに発生する`tidb_analyze_version`の値の変更の問題を修正します。
    -   サブクエリで異なる照合を使用するときに発生する間違った結果の問題を修正します[＃30748](https://github.com/pingcap/tidb/issues/30748)
    -   TiDBの`concat(ifnull(time(3))`の結果がMySQL3の結果と異なる問題を修正し[＃29498](https://github.com/pingcap/tidb/issues/29498)
    -   楽観的なトランザクションモード[＃30410](https://github.com/pingcap/tidb/issues/30410)での潜在的なデータインデックスの不整合の問題を修正します
    -   [＃30200](https://github.com/pingcap/tidb/issues/30200)をTiKV1にプッシュダウンできない場合に、IndexMergeのクエリ実行プランが間違っている問題を修正します。
    -   列タイプの同時変更によりスキーマとデータの間に不整合が生じる問題を修正します[＃31048](https://github.com/pingcap/tidb/issues/31048)
    -   サブクエリ[＃30913](https://github.com/pingcap/tidb/issues/30913)がある場合にIndexMergeクエリの結果が間違っている問題を修正します
    -   クライアントでFetchSizeの設定が大きすぎる場合に発生するパニックの問題を修正します[＃30896](https://github.com/pingcap/tidb/issues/30896)
    -   LEFTJOINが誤ってINNERJOIN1に変換される可能性がある問題を修正し[＃20510](https://github.com/pingcap/tidb/issues/20510)
    -   `CASE-WHEN`式と照合順序を一緒に使用するとパニックが発生する可能性がある問題を修正します[＃30245](https://github.com/pingcap/tidb/issues/30245)
    -   `IN`の値に2進定数[＃31261](https://github.com/pingcap/tidb/issues/31261)が含まれている場合に発生する誤ったクエリ結果の問題を修正します
    -   CTEにサブクエリ[＃31255](https://github.com/pingcap/tidb/issues/31255)がある場合に発生する誤ったクエリ結果の問題を修正します
    -   `INSERT ... SELECT ... ON DUPLICATE KEY UPDATE`ステートメントを実行するとパニックになる問題を修正します[＃28078](https://github.com/pingcap/tidb/issues/28078)
    -   INDEXHASHJOINが`send on closed channel`エラー[＃31129](https://github.com/pingcap/tidb/issues/31129)を返す問題を修正します

-   TiKV

    -   MVCC削除レコードがGC1によってクリアされない問題を修正し[＃11217](https://github.com/tikv/tikv/issues/11217)
    -   悲観的なトランザクションモードで事前書き込み要求を再試行すると、まれにデータの不整合のリスクが発生する可能性があるという問題を修正します[＃11187](https://github.com/tikv/tikv/issues/11187)
    -   GCスキャンがメモリオーバーフローを引き起こす問題を修正します[＃11410](https://github.com/tikv/tikv/issues/11410)
    -   ディスク容量がいっぱいになると、RocksDBのフラッシュまたは圧縮によってパニックが発生する問題を修正します[＃11224](https://github.com/tikv/tikv/issues/11224)

-   PD

    -   リージョン統計が[＃4295](https://github.com/tikv/pd/issues/4295)の影響を受けない問題を修正し`flow-round-by-digit`
    -   ターゲットストアがダウンしているためにスケジューリングオペレーターが迅速に失敗できない問題を修正します[＃3353](https://github.com/tikv/pd/issues/3353)
    -   オフラインストアのリージョンをマージできない問題を修正します[＃4119](https://github.com/tikv/pd/issues/4119)
    -   コールドホットスポットデータをホットスポット統計から削除できない問題を修正します[＃4390](https://github.com/tikv/pd/issues/4390)

-   TiFlash

    -   MPPクエリが停止したときにTiFlashがパニックになる可能性がある問題を修正します
    -   `where <string>`句を使用したクエリが間違った結果を返す問題を修正します
    -   整数主キーの列タイプをより広い範囲に設定するときに発生する可能性があるデータの不整合の潜在的な問題を修正します
    -   入力時刻が1970-01-0100:00:01UTCより前の場合、 `unix_timestamp`の動作がTiDBまたはMySQLの動作と矛盾する問題を修正します
    -   再起動後にTiFlashが`EstablishMPPConnection`エラーを返す可能性がある問題を修正します
    -   `CastStringAsDecimal`の動作がTiFlashとTiDB/TiKVで一貫していない問題を修正します
    -   クエリ結果に`DB::Exception: Encode type of coprocessor response is not CHBlock`のエラーが返される問題を修正します
    -   `castStringAsReal`の動作がTiFlashとTiDB/TiKVで一貫していない問題を修正します
    -   TiFlashの`date_add_string_xxx`関数の返される結果がMySQLの結果と矛盾する問題を修正します

-   ツール

    -   バックアップと復元（BR）

        -   復元操作の終了後にリージョンの分布が不均一になる可能性があるという潜在的な問題を修正します[＃30425](https://github.com/pingcap/tidb/issues/30425)
        -   `minio`がバックアップストレージとして使用されている場合、エンドポイントで`'/'`を指定できない問題を修正します[＃30104](https://github.com/pingcap/tidb/issues/30104)
        -   システムテーブルを同時にバックアップするとテーブル名の更新に失敗するため、システムテーブルを復元できない問題を修正します[＃29710](https://github.com/pingcap/tidb/issues/29710)

    -   TiCDC

        -   `min.insync.replicas`が[＃3994](https://github.com/pingcap/tiflow/issues/3994)より小さい場合、レプリケーションを実行できない問題を修正し`replication-factor` 。
        -   `cached region`モニタリングメトリックが負の[＃4300](https://github.com/pingcap/tiflow/issues/4300)である問題を修正します
        -   `mq sink write row`に監視データがないという問題を修正します[＃3431](https://github.com/pingcap/tiflow/issues/3431)
        -   [＃3810](https://github.com/pingcap/tiflow/issues/3810)の互換性の問題を修正し`sql mode`
        -   レプリケーションタスクが削除されたときに発生する可能性のあるパニックの問題を修正する[＃3128](https://github.com/pingcap/tiflow/issues/3128)
        -   デフォルトの列値[＃3929](https://github.com/pingcap/tiflow/issues/3929)を出力するときに発生するパニックとデータの不整合の問題を修正します
        -   デフォルト値を複製できない問題を修正します[＃3793](https://github.com/pingcap/tiflow/issues/3793)
        -   デッドロックによってレプリケーションタスクがスタックするという潜在的な問題を修正します[＃4055](https://github.com/pingcap/tiflow/issues/4055)
        -   ディスクが完全に書き込まれたときにログが出力されない問題を修正します[＃3362](https://github.com/pingcap/tiflow/issues/3362)
        -   DDLステートメントの特別なコメントによってレプリケーションタスクが停止する問題を修正します[＃3755](https://github.com/pingcap/tiflow/issues/3755)
        -   RHELリリース[＃3584](https://github.com/pingcap/tiflow/issues/3584)のタイムゾーンの問題が原因でサービスを開始できない問題を修正します
        -   不正確なチェックポイント[＃3545](https://github.com/pingcap/tiflow/issues/3545)によって引き起こされる潜在的なデータ損失の問題を修正します
        -   コンテナ環境でのOOMの問題を修正します[＃1798](https://github.com/pingcap/tiflow/issues/1798)
        -   `config.Metadata.Timeout`の誤った構成によって引き起こされるレプリケーション停止の問題を修正し[＃3352](https://github.com/pingcap/tiflow/issues/3352) 。

    -   TiDBデータ移行（DM）

        -   `CREATE VIEW`ステートメントがデータレプリケーションを中断する問題を修正します[＃4173](https://github.com/pingcap/tiflow/issues/4173)
        -   DDLステートメントがスキップされた後にスキーマをリセットする必要がある問題を修正します[＃4177](https://github.com/pingcap/tiflow/issues/4177)
        -   DDLステートメントがスキップされた後にテーブルチェックポイントが時間内に更新されない問題を修正します[＃4184](https://github.com/pingcap/tiflow/issues/4184)
        -   TiDBバージョンとParserバージョン[＃4298](https://github.com/pingcap/tiflow/issues/4298)の互換性の問題を修正します
        -   シンカーメトリックがステータス[＃4281](https://github.com/pingcap/tiflow/issues/4281)をクエリするときにのみ更新される問題を修正します

    -   TiDB Lightning

        -   TiDBLightningに`mysql.tidb`テーブル[＃31088](https://github.com/pingcap/tidb/issues/31088)にアクセスする権限がない場合に発生する誤ったインポート結果の問題を修正します。
        -   TiDBLightningの再起動時に一部のチェックがスキップされる問題を修正します[＃30772](https://github.com/pingcap/tidb/issues/30772)
        -   S3パスが存在しない場合にTiDBLightingがエラーを報告できない問題を修正します[＃30674](https://github.com/pingcap/tidb/pull/30674)

    -   TiDB Binlog

        -   `CREATE PLACEMENT POLICY`ステートメント[＃1118](https://github.com/pingcap/tidb-binlog/issues/1118)と互換性がないためにDrainerが失敗する問題を修正します
