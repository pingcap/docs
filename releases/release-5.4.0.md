---
title: TiDB 5.4 Release Notes
summary: TiDB 5.4 では、GBK 文字セット、インデックス マージ、古いデータの読み取り、統計構成の永続化、および TiKV のログストレージエンジンとしてのRaft Engine の使用がサポートされます。また、バックアップの影響が改善され、Azure Blobストレージがサポートされ、 TiFlashと MPP エンジンが強化されます。互換性の変更には、新しいシステム変数と構成ファイル パラメーターが含まれます。その他の改善点には、SQL、セキュリティ、パフォーマンス、安定性、高可用性、データ移行、診断効率、およびデプロイメントが含まれます。バグ修正では、TiDB、TiKV、PD、 TiFlash、 BR、TiCDC、DM、 TiDB Lightning、および TiDB Binlogの問題に対処します。
---

# TiDB 5.4 リリースノート {#tidb-5-4-release-notes}

発売日：2022年2月15日

TiDB バージョン: 5.4.0

バージョン5.4における主な新機能または改善点は以下のとおりです。

-   GBK文字セットをサポート
-   インデックスマージを使用してデータにアクセスすることをサポートします。これは、複数の列のインデックスのフィルタリング結果をマージします。
-   セッション変数を使用して古いデータを読み取ることをサポートする
-   統計情報を収集するための設定を永続化する機能をサポートする
-   TiKVのログストレージエンジンとしてRaft Engineを使用することをサポートする（実験的）
-   バックアップがクラスタに与える影響を最適化する
-   バックアップストレージとしてAzure Blobストレージの使用をサポートします。
-   TiFlashおよびMPPエンジンの安定性と性能を継続的に向上させる
-   TiDB Lightningに、既存のテーブルへのデータインポートを許可するかどうかを決定するスイッチを追加します。
-   継続的プロファイリング機能の最適化（実験的）
-   TiSparkはユーザー識別と認証をサポートしています

## 互換性の変更 {#compatibility-changes}

> **注記：**
>
> 以前の TiDB バージョンから v5.4.0 にアップグレードする場合、中間バージョンの互換性変更点を確認したい場合は、該当バージョンの[リリースノート](/releases/_index.md)参照してください。

### システム変数 {#system-variables}

<table><thead><tr><th>変数名</th><th>変更の種類</th><th>説明</th></tr></thead><tbody><tr><td><a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_enable_column_tracking-new-in-v540"><code>tidb_enable_column_tracking</code></a></td><td>新しく追加された</td><td>TiDBが<code>PREDICATE COLUMNS</code>を収集することを許可するかどうかを制御します。デフォルト値は<code>OFF.</code></td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_enable_paging-new-in-v540"><code>tidb_enable_paging</code></a></td><td>新しく追加された</td><td><code>IndexLookUp</code>演算子でコプロセッサ要求を送信する際にページング方式を使用するかどうかを制御します。デフォルト値は<code>OFF</code>です。<br/> <code>IndexLookup</code>と<code>Limit</code>を使用する読み取りクエリで、 <code>Limit</code>を<code>IndexScan</code>にプッシュダウンできない場合、読み取りクエリのレイテンシーが高くなり、TiKVの<code>unified read pool</code>のCPU使用率が高くなる可能性があります。このような場合、 <code>Limit</code>演算子は少量のデータしか必要としないため、 <code>tidb_enable_paging</code> <code>ON</code>に設定すると、TiDBが処理するデータ量が少なくなり、クエリのレイテンシーとリソース消費が削減されます。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_enable_top_sql-new-in-v540"><code>tidb_enable_top_sql</code></a></td><td>新しく追加された</td><td>Top SQL機能を有効にするかどうかを制御します。デフォルト値は<code>OFF</code>です。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_persist_analyze_options-new-in-v540"><code>tidb_persist_analyze_options</code></a></td><td>新しく追加された</td><td><a href="https://docs.pingcap.com/tidb/dev/statistics#persist-analyze-configurations">ANALYZE構成の永続化</a>機能を有効にするかどうかを制御します。デフォルト値は<code>ON</code>です。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_read_staleness-new-in-v540"><code>tidb_read_staleness</code></a></td><td>新しく追加された</td><td>現在のセッションで読み取れる履歴データの範囲を制御します。デフォルト値は<code>0</code>です。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_regard_null_as_point-new-in-v540"><code>tidb_regard_null_as_point</code></a></td><td>新しく追加された</td><td>オプティマイザが、NULL等価性を含むクエリ条件をインデックスアクセスのプレフィックス条件として使用できるかどうかを制御します。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_stats_load_sync_wait-new-in-v540"><code>tidb_stats_load_sync_wait</code></a></td><td>新しく追加された</td><td>同期的に統計情報を読み込む機能を有効にするかどうかを制御します。デフォルト値の<code>0</code>は、この機能が無効になっており、統計情報が非同期的に読み込まれることを意味します。この機能が有効になっている場合、この変数は、SQL 最適化がタイムアウトする前に同期的に統計情報を読み込むのを待機できる最大時間を制御します。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_stats_load_pseudo_timeout-new-in-v540"><code>tidb_stats_load_pseudo_timeout</code></a></td><td>新しく追加された</td><td>同期的に統計情報を読み込む際にタイムアウトが発生した場合、SQLが失敗するか（ <code>OFF</code> ）、擬似統計情報を使用するようにフォールバックするか（ <code>ON</code> ）を制御します。デフォルト値は<code>OFF</code>です。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_backoff_lock_fast"><code>tidb_backoff_lock_fast</code></a></td><td>修正済み</td><td>デフォルト値が<code>100</code>から<code>10</code>に変更されました。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_enable_index_merge-new-in-v40"><code>tidb_enable_index_merge</code></a></td><td>修正済み</td><td>デフォルト値が<code>OFF</code>から<code>ON</code>に変更されます。<ul><li> TiDBクラスタをv4.0.0より前のバージョンからv5.4.0以降にアップグレードする場合、この変数はデフォルトで<code>OFF</code>なります。</li><li> TiDBクラスタをv4.0.0以降からv5.4.0以降にアップグレードした場合、この変数はアップグレード前と同じままです。</li><li>バージョン5.4.0以降で新たに作成されたTiDBクラスタでは、この変数はデフォルトで<code>ON</code>なっています。</li></ul></td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_store_limit-new-in-v304-and-v40"><code>tidb_store_limit</code></a></td><td>修正済み</td><td>バージョン5.4.0より前は、この変数はインスタンスレベルとグローバルレベルの両方で設定可能でした。バージョン5.4.0以降は、この変数はグローバル設定のみをサポートします。</td></tr></tbody></table>

### コンフィグレーションファイルパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーション                                                                                                      | 変更の種類  | 説明                                                                                                                                                                                                                                                                                                                    |
| :------------- | :-------------------------------------------------------------------------------------------------------------- | :------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB           | [`stats-load-concurrency`](/tidb-configuration-file.md#stats-load-concurrency-new-in-v540)                      | 新しく追加された | TiDBの同期ロード統計機能が同時に処理できる列の最大数を制御します。デフォルト値は`5`です。                                                                                                                                                                                                                                                                      |
| TiDB           | [`stats-load-queue-size`](/tidb-configuration-file.md#stats-load-queue-size-new-in-v540)                        | 新しく追加された | TiDBの同期ロード統計機能がキャッシュできる列リクエストの最大数を制御します。デフォルト値は`1000`です。                                                                                                                                                                                                                                                              |
| TiKV           | [`snap-generator-pool-size`](/tikv-configuration-file.md#snap-generator-pool-size-new-in-v540)                  | 新しく追加された | `snap-generator`スレッドプールのサイズ。デフォルト値は`2`です。                                                                                                                                                                                                                                                                             |
| TiKV           | `log.file.max-size` 、 `log.file.max-days` 、 `log.file.max-backups`                                              | 新しく追加された | 詳細については、 [TiKVコンフィグレーションファイル - `log.file`](/tikv-configuration-file.md#logfile-new-in-v540)を参照してください。                                                                                                                                                                                                                 |
| TiKV           | `raft-engine`                                                                                                   | 新しく追加された | `enable` 、 `dir` 、 `batch-compression-threshold` 、 `bytes-per-sync` 、 `target-file-size` 、 `purge-threshold` 、 `recovery-mode` 、 `recovery-read-block-size` 、 `recovery-read-block-size` 、および`recovery-threads`含まれます。詳細は、 [TiKVコンフィグレーションファイル - `raft-engine`](/tikv-configuration-file.md#raft-engine)を参照してください。     |
| TiKV           | [`backup.enable-auto-tune`](/tikv-configuration-file.md#enable-auto-tune-new-in-v540)                           | 新しく追加された | v5.3.0 では、デフォルト値は`false`です。v5.4.0 以降では、デフォルト値は`true`に変更されました。このパラメータは、クラスタのリソース使用率が高い場合に、バックアップ タスクで使用されるリソースを制限してクラスタへの影響を軽減するかどうかを制御します。デフォルト設定では、バックアップ タスクの速度が低下する可能性があります。                                                                                                                                       |
| TiKV           | `log-level` 、 `log-format` 、 `log-file` 、 `log-rotation-size`                                                   | 修正済み     | TiKV ログ パラメータの名前は、TiDB ログ パラメータと互換性のある名前`log.level` 、 `log.format` 、 `log.file.filename` 、および`log.enable-timestamp` 。古いパラメータのみを設定し、その値をデフォルト値以外に設定した場合、古いパラメータは新しいパラメータと互換性があります。古いパラメータと新しいパラメータの両方を設定した場合、新しいパラメータが有効になります。詳細については、[TiKVコンフィグレーションファイル - ログ](/tikv-configuration-file.md#log-new-in-v540)を参照してください。 |
| TiKV           | `log-rotation-timespan`                                                                                         | 削除済み     | ログファイルのローテーション間隔。この間隔が経過すると、ログファイルがローテーションされます。これは、現在のログファイルのファイル名にタイムスタンプが追加され、新しいログファイルが作成されることを意味します。                                                                                                                                                                                                              |
| TiKV           | `allow-remove-leader`                                                                                           | 削除済み     | メインスイッチの削除を許可するかどうかを決定します。                                                                                                                                                                                                                                                                                            |
| TiKV           | `raft-msg-flush-interval`                                                                                       | 削除済み     | Raftメッセージがバッチで送信される間隔を決定します。Raftメッセージは、この設定項目で指定された間隔ごとにバッチで送信されます。                                                                                                                                                                                                                                                   |
| PD             | [`log.level`](/pd-configuration-file.md#level)                                                                  | 修正済み     | デフォルト値が「INFO」から「info」に変更され、大文字と小文字を区別しないことが保証されます。                                                                                                                                                                                                                                                                    |
| TiFlash        | [`profile.default.enable_elastic_threadpool`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file) | 新しく追加された | エラスティック スレッド プール機能を有効にするか無効にするかを決定します。この設定項目を有効にすると、高並行処理シナリオでのTiFlash CPU 使用率が大幅に向上します。デフォルト値は`false`です。                                                                                                                                                                                                             |
| TiFlash        | [`storage.format_version`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                    | 新しく追加された | DTFile のバージョンを指定します。デフォルト値は`2`で、このバージョンではハッシュがデータファイルに埋め込まれます。値を`3`に設定することもできます。 `3`の場合、データファイルにはメタデータとトークンデータのチェックサムが含まれ、複数のハッシュアルゴリズムがサポートされます。                                                                                                                                                                     |
| TiFlash        | [`logger.count`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                              | 修正済み     | デフォルト値は`10`に変更されます。                                                                                                                                                                                                                                                                                                   |
| TiFlash        | [`status.metrics_port`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                       | 修正済み     | デフォルト値は`8234`に変更されます。                                                                                                                                                                                                                                                                                                 |
| TiFlash        | [`raftstore.apply-pool-size`](/tiflash/tiflash-configuration.md#configure-the-tiflash-learnertoml-file)         | 新しく追加された | Raftデータをストレージにフラッシュするプール内のスレッドの許容数。デフォルト値は`4`です。                                                                                                                                                                                                                                                                    |
| TiFlash        | [`raftstore.store-pool-size`](/tiflash/tiflash-configuration.md#configure-the-tiflash-learnertoml-file)         | 新しく追加された | Raftを処理するスレッドの許容数。これはRaftstoreスレッドプールのサイズです。デフォルト値は`4`です。                                                                                                                                                                                                                                                             |
| TiDB Data Migration (DM)  | [`collation_compatible`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)         | 新しく追加された | `CREATE` SQL ステートメントのデフォルトの照合順序を同期するモード。値のオプションは「loose」（デフォルト）と「strict」です。                                                                                                                                                                                                                                          |
| TiCDC          | `max-message-bytes`                                                                                             | 修正済み     | Kafkaシンクの`max-message-bytes`のデフォルト値を`104857601`に変更します（10MB）。                                                                                                                                                                                                                                                          |
| TiCDC          | `partition-num`                                                                                                 | 修正済み     | Kafka Sink の`partition-num`のデフォルト値を`4`から`3`に変更します。これにより、TiCDC が Kafaka パーティションにメッセージをより均等に送信できるようになります。                                                                                                                                                                                                               |
| TiDB Lightning | `meta-schema-name`                                                                                              | 修正済み     | ターゲット TiDB 内のメタデータのスキーマ名を指定します。v5.4.0 以降、このスキーマは有効になっている場合にのみ作成されます[並列インポート](/tidb-lightning/tidb-lightning-distributed-import.md)(対応するパラメータは`tikv-importer.incremental-import = true`です)。                                                                                                                            |
| TiDB Lightning | `task-info-schema-name`                                                                                         | 新しく追加された | TiDB Lightning が競合を検出した際に、重複データが格納されるデータベース名を指定します。デフォルト値は「lightning_task_info」です。このパラメータは、「重複データの解決」機能を有効にしている場合にのみ指定してください。                                                                                                                                                                                         |
| TiDB Lightning | `incremental-import`                                                                                            | 新しく追加された | 既にデータが存在するテーブルにデータをインポートすることを許可するかどうかを決定します。デフォルト値は`false`です。                                                                                                                                                                                                                                                         |

### その他 {#others}

-   TiDBとPDの間にインターフェースが追加されました。 `information_schema.TIDB_HOT_REGIONS_HISTORY`システムテーブルを使用する場合、TiDBは対応するバージョンのPDを使用する必要があります。
-   TiDB サーバー、PD サーバー、および TiKV サーバーは、ログ名、出力形式、ローテーションと有効期限のルールを管理するために、ログ関連パラメーターに統一された命名方法を使用し始めます。詳しくは[TiKV設定ファイル - ログ](/tikv-configuration-file.md#log-new-in-v540)をご覧ください。
-   バージョン5.4.0以降、プランキャッシュによってキャッシュされた実行プランに対してSQLバインディングを作成すると、対応するクエリに対して既にキャッシュされているプラ​​ンが無効化されます。この新しいバインディングは、バージョン5.4.0より前にキャッシュされた実行プランには影響しません。
-   v5.3 以前のバージョンでは、 [TiDB Data Migration (DM)](https://docs.pingcap.com/tidb-data-migration/v5.3/)ドキュメントは TiDB ドキュメントから独立しています。 v5.4 以降、DM ドキュメントは同じバージョンの TiDB ドキュメントに統合されています。 DM ドキュメント サイトにアクセスせずに、 [DMドキュメント](/dm/dm-overview.md)を直接読むことができます。
-   ポイントインタイムリカバリ（PITR）の実験的機能をcdclogとともに削除しました。バージョン5.4.0以降、cdclogベースのPITRおよびcdclogはサポートされなくなりました。
-   システム変数を「DEFAULT」に設定する動作をMySQLとの互換性を高める [#29680](https://github.com/pingcap/tidb/pull/29680)
-   システム変数`lc_time_names`を読み取り専用に設定する [#30084](https://github.com/pingcap/tidb/pull/30084)
-   `tidb_store_limit`のスコープを INSTANCE または GLOBAL から GLOBAL に変更する [#30756](https://github.com/pingcap/tidb/pull/30756)
-   列にゼロが含まれている場合、整数型の列を時間型の列に変換することを禁止する [#25728](https://github.com/pingcap/tidb/pull/25728)
-   浮動小数点値を挿入する際に`Inf`または`NAN`の値に対してエラーが報告されない問題を修正します [#30148](https://github.com/pingcap/tidb/pull/30148)
-   `REPLACE`ステートメントが自動 ID が範囲外の場合に他の行を誤って変更してしまう問題を修正しました [#30301](https://github.com/pingcap/tidb/pull/30301)

## 新機能 {#new-features}

### SQL {#sql}

-   **TiDBはバージョン5.4.0以降、GBK文字セットをサポートしています。**

    バージョン 5.4.0 より前の TiDB は、 `ascii` 、 `binary` 、 `latin1` 、 `utf8` 、および`utf8mb4`文字セットをサポートしています。

    中国語ユーザーをより適切にサポートするため、TiDB はバージョン 5.4.0 以降、GBK 文字セットをサポートしています。TiDB クラスタを初めて初期化する際に、TiDB 設定ファイルで[`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap)オプションを有効にすると、TiDB GBK 文字セットは`gbk_bin`と`gbk_chinese_ci`の照合順序をサポートします。

    GBK 文字セットを使用する場合は、互換性の制限に注意する必要があります。詳細については、[文字セットと照合 - GBK](/character-set-gbk.md)参照してください。

### セキュリティ {#security}

-   **TiSparkはユーザー認証と認可をサポートしています。**

    TiSpark 2.5.0以降、TiSparkはデータベースユーザー認証と、データベースまたはテーブルレベルでの読み書き権限の両方をサポートしています。この機能を有効にすることで、データ取得のためのドローなどの不正なバッチタスクの実行を防止でき、オンラインクラスタの安定性とデータセキュリティが向上します。

    この機能はデフォルトでは無効になっています。有効にした場合、TiSpark を介して操作するユーザーに必要な権限がない場合、TiSpark から例外が返されます。

    [ユーザー向けドキュメント](https://docs-archive.pingcap.com/tidb/v5.4/tispark-overview#security)

-   **TiUPはrootユーザーの初期パスワード生成をサポートしています。**

    クラスター起動コマンドに`--init`パラメータが追加されました。このパラメータを使用すると、 TiUPを使用してデプロイされたTiDBクラスターにおいて、 TiUPがデータベースのrootユーザー用に強力な初期パスワードを生成します。これにより、パスワードが空のrootユーザーを使用することによるセキュリティリスクを回避し、データベースのセキュリティを確保できます。

    [ユーザー向けドキュメント](/production-deployment-using-tiup.md#step-7-start-a-tidb-cluster)

### パフォーマンス {#performance}

-   **カラム型ストレージエンジンTiFlashおよび演算エンジンMPPの安定性とパフォーマンスの向上を継続する。**

    -   MPPエンジンへの関数委譲をさらに強化する：

        -   文字列関数: `LPAD()` 、 `RPAD()` 、 `STRCMP()`
        -   日付関数: `ADDDATE(string, real)` 、 `DATE_ADD(string, real)` 、 `DATE_SUB(string, real)` 、 `SUBDATE(string, real)` 、 `QUARTER()`

    -   リソース利用率を向上させるための弾性スレッドプール機能を導入（実験的）

    -   TiKVからデータを複製する際に、行ベースのストレージ形式から列ベースのストレージ形式へのデータ変換の効率を向上させ、データ複製の全体的なパフォーマンスを50%向上させました。

    -   一部の設定項目のデフォルト値を調整することで、 TiFlashのパフォーマンスと安定性を向上させることができます。HTAPハイブリッドロード環境では、単一テーブルに対する単純なクエリのパフォーマンスが最大20%向上します。

    ユーザードキュメント: [プッシュダウン計算に対応](/tiflash/tiflash-supported-pushdown-calculations.md)、 [tiflash.toml ファイルを設定します](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)

-   **セッション変数を使用して、指定された期間内の履歴データを読み取ります。**

    TiDBは、 Raftコンセンサスアルゴリズムに基づいたマルチレプリカ分散データベースです。高並行性および高スループットのアプリケーションシナリオにおいて、TiDBはフォロワーレプリカによって読み取りパフォーマンスをスケールアウトし、読み取りリクエストと書き込みリクエストを分離することができます。

    TiDBは、さまざまなアプリケーションシナリオに対応するため、フォロワー読み取りに「強一貫性読み取り」と「弱一貫性履歴読み取り」の2つのモードを提供しています。「強一貫性読み取り」モードは、リアルタイムデータを必要とするアプリケーションシナリオに適しています。ただし、このモードでは、リーダーとフォロワー間のデータ複製レイテンシーとスループットの低下により、特に地理的に分散したデプロイメントの場合、読み取りリクエストのレイテンシーが大きくなる可能性があります。

    リアルタイムデータに対する要件がそれほど厳しくないアプリケーションシナリオでは、履歴読み取りモードが推奨されます。このモードでは、レイテンシーを削減し、スループットを向上させることができます。TiDBは現在、以下の方法で履歴データの読み取りをサポートしています。SQLステートメントを使用して過去の時点からデータを読み取るか、過去の時点に基づいて読み取り専用トランザクションを開始します。どちらの方法も、特定の時点または指定された時間範囲内の履歴データの読み取りをサポートしています。詳細については、 [`AS OF TIMESTAMP`句を使用して履歴データを読み取る](/as-of-timestamp.md).

    バージョン5.4.0以降、TiDBはセッション変数を使用して指定した時間範囲内の履歴データを読み取る機能をサポートすることで、履歴読み取りモードの使いやすさを向上させました。このモードは、準リアルタイムシナリオにおいて、低遅延かつ高スループットの読み取りリクエストに対応します。変数は次のように設定できます。

    ```sql
    set @@tidb_replica_read=leader_and_follower
    set @@tidb_read_staleness="-5"
    ```

    この設定により、TiDBは最も近いリーダーノードまたはフォロワーノードを選択し、5秒以内に最新の履歴データを読み取ることができます。

    [ユーザー向けドキュメント](/tidb-read-staleness.md)

-   **インデックスマージのためのGA**

    インデックスマージは、SQL最適化のための実験的機能としてTiDB v4.0で導入されました。この方法は、クエリで複数のデータ列をスキャンする必要がある場合に、条件フィルタリングを大幅に高速化します。次のクエリを例にとります。 `WHERE`ステートメントにおいて、 `OR`で接続されたフィルタリング条件にそれぞれ列*key1*と*key2の*インデックスがある場合、インデックスマージ機能はそれぞれのインデックスを同時にフィルタリングし、クエリ結果をマージして、マージされた結果を返します。

    ```sql
    SELECT * FROM table WHERE key1 <= 100 OR key2 = 200;
    ```

    TiDB v4.0より前のバージョンでは、テーブルに対するクエリで一度にフィルタリングに使用できるインデックスは1つだけでした。複数の列のデータに対してクエリを実行する場合は、インデックスマージを有効にすることで、個々の列のインデックスを使用して短時間で正確なクエリ結果を取得できます。インデックスマージは不要なフルテーブルスキャンを回避し、多数の複合インデックスを作成する必要もありません。

    バージョン5.4.0では、インデックスマージが一般提供開始（GA）となりました。ただし、以下の制限事項には引き続き注意が必要です。

    -   インデックス マージは、選言正規形 (X <sub>1</sub> ⋁ X <sub>2</sub> ⋁ …X <sub>n</sub> ) のみをサポートします。つまり、この機能は`WHERE`句のフィルタリング条件が`OR`で接続されている場合にのみ機能します。

    -   新規にデプロイされたv5.4.0以降のTiDBクラスタでは、この機能はデフォルトで有効になっています。以前のバージョンからアップグレードされたv5.4.0以降のTiDBクラスタでは、この機能はアップグレード前の設定を継承し、必要に応じて設定を変更できます（v4.0より前のTiDBクラスタでは、この機能は存在せず、デフォルトで無効になっています）。

    [ユーザー向けドキュメント](/explain-index-merge.md)

-   **Raft Engineのサポート（実験的）**

    TiKVのログストレージエンジンとして[Raft Engine](https://github.com/tikv/raft-engine)使用をサポートします。RocksDBと比較して、 Raft EngineはTiKVのI/O書き込みトラフィックを最大40%、CPU使用率を10%削減し、特定の負荷条件下ではフォアグラウンドスループットを約5%向上させ、テールレイテンシーを20%削減します。さらに、 Raft Engineはログリサイクルの効率を向上させ、極端な条件下でのログ蓄積の問題を解決します。

    Raft Engine はまだ実験的機能であり、デフォルトでは無効になっています。v5.4.0 のRaft Engineのデータ形式は、以前のバージョンと互換性がないことに注意してください。クラスターをアップグレードする前に、すべての TiKV ノードでRaft Engine が無効になっていることを確認する必要があります。Raft Raft Engine はv5.4.0 以降のバージョンでのみ使用することをお勧めします。

    [ユーザー向けドキュメント](/tikv-configuration-file.md#raft-engine)

-   **`PREDICATE COLUMNS`に関する統計情報の収集をサポートする（実験的）**

    ほとんどの場合、SQL ステートメントを実行する際に、オプティマイザは一部の列 ( `WHERE` 、`JOIN`、 `ORDER BY` `JOIN` 、および`GROUP BY`ステートメントの列など) の統計情報のみを使用します。これらの使用される列は`PREDICATE COLUMNS`と呼ばれます。

    バージョン5.4.0以降では、 [`tidb_enable_column_tracking`](/system-variables.md#tidb_enable_column_tracking-new-in-v540)システム変数の値を`ON`に設定することで、TiDBが`PREDICATE COLUMNS`を収集できるようになります。

    設定後、TiDB は`PREDICATE COLUMNS`情報を 100 * [`stats-lease`](/tidb-configuration-file.md#stats-lease)ごとに`mysql.column_stats_usage`システム テーブルに書き込みます。ビジネスのクエリ パターンが安定している場合は、 `ANALYZE TABLE TableName PREDICATE COLUMNS`構文を使用して`PREDICATE COLUMNS`列のみの統計情報を収集することで、統計情報の収集オーバーヘッドを大幅に削減できます。

    [ユーザー向けドキュメント](/statistics.md#collect-statistics-on-some-columns)

-   **統計情報の同期読み込みをサポート（実験的）**

    バージョン5.4.0以降、TiDBは統計情報の同期読み込み機能を導入しました。この機能はデフォルトでは無効になっています。この機能を有効にすると、SQL文の実行時に、ヒストグラム、TopN、Count-Min Sketch統計情報などの大規模な統計情報をメモリに同期的に読み込むことができるようになり、SQL最適化のための統計情報の網羅性が向上します。

    [ユーザー向けドキュメント](/statistics.md#load-statistics)

### 安定性 {#stability}

-   **ANALYZE構成の永続化をサポートする**

    統計は、オプティマイザが実行計画を生成する際に参照する基本情報の一種です。統計情報の精度は、生成される実行計画の妥当性に直接影響します。統計情報の精度を確保するためには、テーブル、パーティション、インデックスごとに異なる収集構成を設定する必要がある場合があります。

    バージョン5.4.0以降、TiDBは一部の`ANALYZE`設定の永続化をサポートしています。この機能により、既存の設定を今後の統計情報収集に簡単に再利用できます。

    `ANALYZE`構成永続化機能はデフォルトで有効になっています (システム変数`tidb_analyze_version`は`2`で、 [`tidb_persist_analyze_options`](/system-variables.md#tidb_persist_analyze_options-new-in-v540)はデフォルトで`ON`です)。この機能を使用すると、 `ANALYZE`ステートメントを手動で実行する際に、ステートメントで指定された永続化構成を記録できます。記録されると、次回 TiDB が統計情報を自動的に更新する場合、またはこれらの構成を指定せずに手動で統計情報を収集する場合、TiDB は記録された構成に従って統計情報を収集します。

    [ユーザー向けドキュメント](/statistics.md#persist-analyze-configurations)

### 高可用性とディザスタリカバリ {#high-availability-and-disaster-recovery}

-   **バックアップタスクがクラスタに与える影響を軽減する**

    Backup & Restore (BR) では、自動調整機能 (デフォルトで有効) が導入されました。この機能は、クラスタのリソース使用状況を監視し、バックアップタスクで使用されるスレッド数を調整することで、クラスタに対するバックアップタスクの影響を軽減します。場合によっては、バックアップ用のクラスタハードウェアリソースを増やし、自動調整機能を有効にすると、クラスタに対するバックアップタスクの影響を 10% 以下に抑えることができます。

    [ユーザー向けドキュメント](/br/br-auto-tune.md)

-   **バックアップのターゲットストレージとしてAzure Blob Storageをサポートする**

    Backup &amp; Restore (BR) は、リモートバックアップストレージとして Azure Blob Storage をサポートしています。Azure クラウドに TiDB をデプロイしている場合、クラスタデータを Azure Blob Storage サービスにバックアップできるようになりました。

    [ユーザー向けドキュメント](/br/backup-and-restore-storages.md)

### データ移行 {#data-migration}

-   **TiDB Lightning は、データを含むテーブルへのデータのインポートを許可するかどうかを判断する新機能を導入しました。**

    TiDB Lightning、設定項目`incremental-import`が導入されました。これは、データを含むテーブルへのデータのインポートを許可するかどうかを決定します。デフォルト値は`false`です。並列インポートモードを使用する場合は、設定を`true`に設定する必要があります。

    [ユーザー向けドキュメント](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)

-   **TiDB Lightningは、並列インポート用のメタ情報を格納するスキーマ名を導入しました。**

    TiDB Lightning、 `meta-schema-name`という構成項目が導入されました。並列インポートモードでは、このパラメータは、ターゲットクラスタ内の各TiDB Lightningインスタンスのメタ情報を格納するスキーマ名を指定します。デフォルト値は「lightning_metadata」です。このパラメータに設定する値は、同じ並列インポートに参加する各TiDB Lightningインスタンスで同じである必要があります。そうでない場合、インポートされたデータの正確性が保証されません。

    [ユーザー向けドキュメント](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)

-   **TiDB Lightningに重複解決機能が導入されました**

    ローカルバックエンドモードでは、 TiDB Lightningはデータインポートが完了する前に重複データを出力し、その後データベースからその重複データを削除します。インポート完了後に重複データを解決し、アプリケーションルールに従って挿入する適切なデータを選択できます。後続の増分データ移行フェーズで発生する重複データによるデータ不整合を回避するため、重複データに基づいて上流のデータソースをクリーンアップすることをお勧めします。

    [ユーザー向けドキュメント](/tidb-lightning/tidb-lightning-error-resolution.md)

-   **TiDB Data Migration (DM)におけるリレーログの使用を最適化する**

    -   `enable-relay`構成で`source` } スイッチを復元します。

    -   `start-relay`および`stop-relay`コマンドを使用して、リレーログを動的に有効化および無効化することをサポートします。

    -   リレーログの状態を`source`にバインドします。 `source`どの DM-worker に移行されても、有効または無効の元の状態を維持します。

    -   リレーログのストレージパスをDM-workerの設定ファイルに移動します。

    [ユーザー向けドキュメント](/dm/relay-log.md)

-   **DMにおける<a href="/character-set-and-collation.md">照合順序</a>処理を最適化する**

    `collation_compatible`設定項目を追加します。値のオプションは`loose` (デフォルト) と`strict`です。

    -   アプリケーションに照合順序に関する厳密な要件がなく、クエリ結果の照合順序が上流と下流で異なる可能性がある場合は、デフォルトの`loose`モードを使用してエラーの報告を回避できます。
    -   アプリケーションで照合順序に関する厳格な要件があり、アップストリームとダウンストリーム間で照合順序を統一する必要がある場合は、 `strict`モードを使用できます。ただし、ダウンストリームがアップストリームのデフォルトの照合順序をサポートしていない場合、データレプリケーションでエラーが発生する可能性があります。

    [ユーザー向けドキュメント](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)

-   **DM の`transfer source`を最適化して、レプリケーション タスクをスムーズに実行できるようにします。**

    DMワーカーノードの負荷が不均衡な場合、 `transfer source`コマンドを使用して、 `source`の構成を別の負荷に手動で転送できます。最適化後、 `transfer source`コマンドを使用すると、手動操作が簡素化されます。DMは他の操作を内部的に完了するため、関連するすべてのタスクを一時停止することなく、ソースをスムーズに転送できます。

-   **DM OpenAPIが一般提供開始（GA）となりました**

    DMは、データソースの追加やタスク管理など、APIを介した日常的な管理をサポートしています。バージョン5.4.0では、DM OpenAPIが一般提供開始となります。

    [ユーザー向けドキュメント](/dm/dm-open-api.md)

### 診断効率 {#diagnostic-efficiency}

-   **Top SQL （実験的機能）**

    ソースコードを大量に消費するクエリを簡単に見つけるのに役立つ、新しい実験的機能である「Top SQL」 （デフォルトでは無効）が導入されました。

    [ユーザー向けドキュメント](/dashboard/top-sql.md)

### TiDBデータ共有サブスクリプション {#tidb-data-share-subscription}

-   **TiCDCがクラスターに与える影響を最適化する**

    TiCDCを使用すると、TiDBクラスタのパフォーマンスへの影響を大幅に軽減できます。テスト環境では、TiCDCがTiDBに与えるパフォーマンスへの影響を5%未満に抑えることが可能です。

### 導入と保守 {#deployment-and-maintenance}

-   **継続的プロファイリングの強化（実験的）**

    -   サポートされているコンポーネントがさらに増えました: TiDB v5.4.0 では、TiDB、PD、TiKV に加えて、 TiFlashの CPU プロファイリングもサポートしています。

    -   プロファイリング表示の形式がさらに充実：CPUプロファイリングとゴルーチンの結果をフレームチャートに表示できるようになりました。

    -   サポートされているデプロイメント環境がさらに増えました: TiDB Operatorを使用してデプロイされたクラスターでも、継続的プロファイリングを使用できます。

    継続的プロファイリングはデフォルトでは無効になっており、TiDB Dashboardで有効にすることができます。

    継続的プロファイリングは、 TiUP v1.9.0以降、またはTiDB Operator v1.3.0以降を使用してデプロイまたはアップグレードされたクラスタに適用可能です。

    [ユーザー向けドキュメント](/dashboard/continuous-profiling.md)

## 改善点 {#improvements}

-   TiDB

    -   キャッシュされたクエリ プランをクリアするための`ADMIN {SESSION | INSTANCE | GLOBAL} PLAN_CACHE`構文をサポート [#30370](https://github.com/pingcap/tidb/pull/30370)

-   TiKV

    -   コプロセッサーがページングAPIをサポートし、リクエストをストリームのように処理する [#11448](https://github.com/tikv/tikv/issues/11448)
    -   読み取り操作が二次ロックの解決を待つ必要がないように、 `read-through-lock`をサポートする [#11402](https://github.com/tikv/tikv/issues/11402)
    -   ディスク容量不足によるpanicを防ぐため、ディスク保護メカニズムを追加する [#10537](https://github.com/tikv/tikv/issues/10537)
    -   ログのアーカイブとローテーションをサポートする [#11651](https://github.com/tikv/tikv/issues/11651)
    -   Raftクライアントによるシステムコールを削減し、CPU効率を向上させる [#11309](https://github.com/tikv/tikv/issues/11309)
    -   コプロセッサーが部分文字列をTiKVにプッシュダウンする機能をサポート [#11495](https://github.com/tikv/tikv/issues/11495)
    -   Read Committed分離レベルで読み取りロックをスキップすることでスキャンパフォーマンスを向上させる [#11485](https://github.com/tikv/tikv/issues/11485)
    -   バックアップ操作で使用されるデフォルトのスレッドプールサイズを縮小し、負荷が高い場合のスレッドプールの使用を制限する [#11000](https://github.com/tikv/tikv/issues/11000)
    -   適用スレッドプールとストアスレッドプールのサイズを動的に調整する機能をサポートする [#11159](https://github.com/tikv/tikv/issues/11159)
    -   `snap-generator`スレッドプールのサイズ設定をサポートする [#11247](https://github.com/tikv/tikv/issues/11247)
    -   多数のファイルがあり、頻繁な読み書きが発生する場合に発生するグローバルロック競合の問題を最適化します [#250](https://github.com/tikv/rocksdb/pull/250)

-   PD

    -   過去のホットスポット情報をデフォルトで記録する [#25281](https://github.com/pingcap/tidb/issues/25281)
    -   HTTPコンポーネントにリクエスト元を識別するための署名を追加する [#4490](https://github.com/tikv/pd/issues/4490)
    -   TiDB Dashboardをv2021.12.31にアップデート [#4257](https://github.com/tikv/pd/issues/4257)

-   TiFlash

    -   ローカルオペレーター間の通信を最適化する
    -   gRPCの非一時スレッド数を増やして、頻繁なスレッドの生成や破棄を回避する。

-   ツール

    -   Backup & Restore (BR)

        -   BRが暗号化バックアップを実行する際に、キーの有効性チェックを追加する [#29794](https://github.com/pingcap/tidb/issues/29794)

    -   TiCDC

        -   「EventFeed retry rate limited」ログの数を減らす [#4006](https://github.com/pingcap/tiflow/issues/4006)
        -   多数のテーブルを複製する際のレプリケーションレイテンシーを削減する [#3900](https://github.com/pingcap/tiflow/issues/3900)
        -   TiKVストアがダウンした際にKVクライアントが復旧するまでの時間を短縮する [#3191](https://github.com/pingcap/tiflow/issues/3191)

    -   TiDB Data Migration (DM)

        -   リレー有効時のCPU使用率を下げる [#2214](https://github.com/pingcap/dm/issues/2214)

    -   TiDB Lightning

        -   TiDBバックエンドモードのパフォーマンス向上のため、デフォルトで楽観的トランザクションを使用してデータを書き込むようにする [#30953](https://github.com/pingcap/tidb/pull/30953)

    -   Dumpling

        -   Dumplingがデータベースのバージョンを確認する際の互換性を改善 [#29500](https://github.com/pingcap/tidb/pull/29500)
        -   `CREATE DATABASE`と`CREATE TABLE`をダンプする際に、デフォルトの照合順序を追加する [#3420](https://github.com/pingcap/tiflow/issues/3420)

## バグ修正 {#bug-fixes}

-   TiDB

    -   クラスターをv4.xからv5.xにアップグレードする際に発生する`tidb_analyze_version`値の変更に関する問題を修正します。 [#25422](https://github.com/pingcap/tidb/issues/25422)
    -   サブクエリで異なる照合順序を使用した場合に発生する誤った結果の問題を修正しました [#30748](https://github.com/pingcap/tidb/issues/30748)
    -   TiDB における`concat(ifnull(time(3))`の結果が MySQL における結果と異なる問題を修正しました [#29498](https://github.com/pingcap/tidb/issues/29498)
    -   楽観的トランザクションモードにおける潜在的なデータインデックスの不整合の問題を修正 [#30410](https://github.com/pingcap/tidb/issues/30410)
    -   式を TiKV にプッシュダウンできない場合に IndexMerge のクエリ実行プランが誤っている問題を修正しました [#30200](https://github.com/pingcap/tidb/issues/30200)
    -   同時実行される列型変更によってスキーマとデータの間に不整合が生じる問題を修正します [#31048](https://github.com/pingcap/tidb/issues/31048)
    -   サブクエリが存在する場合に IndexMerge クエリの結果が間違っている問題を修正しました [#30913](https://github.com/pingcap/tidb/issues/30913)
    -   クライアントで FetchSize が大きすぎると発生するpanic問題を修正しました [#30896](https://github.com/pingcap/tidb/issues/30896)
    -   LEFT JOINが誤ってINNER JOINに変換される可能性がある問題を修正しました [#20510](https://github.com/pingcap/tidb/issues/20510)
    -   `CASE-WHEN`式と照合順序を併用した場合にpanicが発生する可能性がある問題を修正しました [#30245](https://github.com/pingcap/tidb/issues/30245)
    -   `IN`の値にバイナリ定数が含まれている場合に発生する、誤ったクエリ結果の問題を修正しました [#31261](https://github.com/pingcap/tidb/issues/31261)
    -   CTEにサブクエリがある場合に発生する、誤ったクエリ結果の問題を修正しました [#31255](https://github.com/pingcap/tidb/issues/31255)
    -   `INSERT ... SELECT ... ON DUPLICATE KEY UPDATE`ステートメントを実行するとpanicが発生する問題を修正しました [#28078](https://github.com/pingcap/tidb/issues/28078)
    -   INDEX HASH JOIN が`send on closed channel`エラーを返す問題を修正します [#31129](https://github.com/pingcap/tidb/issues/31129)

-   TiKV

    -   MVCC削除レコードがGCによってクリアされない問題を修正しました [#11217](https://github.com/tikv/tikv/issues/11217)
    -   悲観的トランザクションモードでプリライト要求を再試行すると、まれにデータ不整合のリスクが発生する可能性がある問題を修正しました [#11187](https://github.com/tikv/tikv/issues/11187)
    -   GCスキャンによってメモリオーバーフローが発生する問題を修正 [#11410](https://github.com/tikv/tikv/issues/11410)
    -   RocksDBのフラッシュまたは圧縮時にディスク容量がいっぱいになったときにpanicが発生する問題を修正 [#11224](https://github.com/tikv/tikv/issues/11224)

-   PD

    -   リージョン統計が`flow-round-by-digit`の影響を受けない問題を修正します [#4295](https://github.com/tikv/pd/issues/4295)
    -   ターゲットストアがダウンしているため、スケジューリング演算子が迅速に失敗できない問題を修正します [#3353](https://github.com/tikv/pd/issues/3353)
    -   オフラインストアのリージョンをマージできない問題を修正 [#4119](https://github.com/tikv/pd/issues/4119)
    -   コールドホットスポットのデータがホットスポット統計から削除できない問題を修正しました [#4390](https://github.com/tikv/pd/issues/4390)

-   TiFlash

    -   MPPクエリが停止した際にTiFlashがpanic可能性がある問題を修正しました。
    -   `where <string>`句を含むクエリが誤った結果を返す問題を修正しました。
    -   整数型の主キーの列型をより広い範囲に設定した場合に発生する可能性のあるデータ不整合の問題を修正します。
    -   入力時刻が 1970-01-01 00:00:01 UTC より前の場合に`unix_timestamp`の動作が TiDB または MySQL の動作と一致しない問題を修正します。
    -   TiFlashを再起動した後に`EstablishMPPConnection`エラーが返される可能性がある問題を修正しました。
    -   TiFlashとTiDB/TiKVで`CastStringAsDecimal`の動作が一貫していない問題を修正します。
    -   クエリ結果で`DB::Exception: Encode type of coprocessor response is not CHBlock`エラーが返される問題を修正します。
    -   TiFlashとTiDB/TiKVで`castStringAsReal`の動作が一貫していない問題を修正します。
    -   TiFlashの`date_add_string_xxx`関数の戻り値が MySQL の戻り値と一致しない問題を修正します。

-   ツール

    -   Backup & Restore (BR)

        -   リストア操作完了後にリージョン分布が不均一になる可能性がある問題を修正 [#30425](https://github.com/pingcap/tidb/issues/30425)
        -   `'/'`バックアップストレージとして使用している場合、エンドポイントで`minio`指定できない問題を修正しました [#30104](https://github.com/pingcap/tidb/issues/30104)
        -   システムテーブルの同時バックアップによってテーブル名の更新が失敗し、システムテーブルを復元できない問題を修正しました [#29710](https://github.com/pingcap/tidb/issues/29710)

    -   TiCDC

        -   `min.insync.replicas`が`replication-factor`より小さい場合にレプリケーションが実行できない問題を修正します [#3994](https://github.com/pingcap/tiflow/issues/3994)
        -   `cached region`モニタリングメトリックが負の値になる問題を修正しました [#4300](https://github.com/pingcap/tiflow/issues/4300)
        -   `mq sink write row`に監視データがない問題を修正 [#3431](https://github.com/pingcap/tiflow/issues/3431)
        -   `sql mode`の互換性の問題を修正しました [#3810](https://github.com/pingcap/tiflow/issues/3810)
        -   レプリケーションタスクが削除された際に発生する可能性のあるpanic問題を修正 [#3128](https://github.com/pingcap/tiflow/issues/3128)
        -   デフォルト列値を出力する際に​​発生するpanicとデータ不整合の問題を修正しました [#3929](https://github.com/pingcap/tiflow/issues/3929)
        -   デフォルト値が複製できない問題を修正 [#3793](https://github.com/pingcap/tiflow/issues/3793)
        -   デッドロックによってレプリケーションタスクが停止する可能性のある問題を修正します [#4055](https://github.com/pingcap/tiflow/issues/4055)
        -   ディスクへの書き込みが完了した際にログが出力されない問題を修正 [#3362](https://github.com/pingcap/tiflow/issues/3362)
        -   DDLステートメント内の特殊コメントがレプリケーションタスクの停止を引き起こす問題を修正 [#3755](https://github.com/pingcap/tiflow/issues/3755)
        -   RHELリリース [#3584](https://github.com/pingcap/tiflow/issues/3584)において、タイムゾーンの問題によりサービスを開始できない問題を修正しました。
        -   不正確なチェックポイントによって引き起こされる可能性のあるデータ損失の問題を修正しました [#3545](https://github.com/pingcap/tiflow/issues/3545)
        -   コンテナ環境におけるOOM問題を修正 [#1798](https://github.com/pingcap/tiflow/issues/1798)
        -   `config.Metadata.Timeout`の設定ミスが原因で発生するレプリケーション停止の問題を修正します [#3352](https://github.com/pingcap/tiflow/issues/3352)

    -   TiDB Data Migration (DM)

        -   `CREATE VIEW`ステートメントがデータ複製を中断する問題を修正 [#4173](https://github.com/pingcap/tiflow/issues/4173)
        -   DDLステートメントがスキップされた後にスキーマをリセットする必要がある問題を修正します [#4177](https://github.com/pingcap/tiflow/issues/4177)
        -   DDLステートメントがスキップされた後、テーブルチェックポイントが時間内に更新されない問題を修正しました [#4184](https://github.com/pingcap/tiflow/issues/4184)
        -   TiDBのバージョンとパーサーのバージョン間の互換性の問題を修正しました [#4298](https://github.com/pingcap/tiflow/issues/4298)
        -   同期メトリクスがステータスを照会した時のみ更新される問題を修正 [#4281](https://github.com/pingcap/tiflow/issues/4281)

    -   TiDB Lightning

        -   TiDB Lightningが`mysql.tidb`テーブルにアクセスする権限を持たない場合に発生する、インポート結果の誤りに関する問題を修正しました [#31088](https://github.com/pingcap/tidb/issues/31088)
        -   TiDB Lightningの再起動時に一部のチェックがスキップされる問題を修正しました [#30772](https://github.com/pingcap/tidb/issues/30772)
        -   S3パスが存在しない場合にTiDB Lightningがエラーを報告しない問題を修正しました [#30674](https://github.com/pingcap/tidb/pull/30674)

    -   TiDB Binlog

        -   `CREATE PLACEMENT POLICY`ステートメントと互換性がないためDrainer が失敗する問題を修正します [#1118](https://github.com/pingcap/tidb-binlog/issues/1118)
