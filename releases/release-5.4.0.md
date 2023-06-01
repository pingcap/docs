---
title: TiDB 5.4 Release Notes
---

# TiDB 5.4 リリースノート {#tidb-5-4-release-notes}

発売日：2022年2月15日

TiDB バージョン: 5.4.0

v5.4 の主な新機能または改善点は次のとおりです。

-   GBK文字セットをサポート
-   複数の列のインデックスのフィルタリング結果をマージする、インデックス マージを使用したデータへのアクセスのサポート
-   セッション変数を使用した古いデータの読み取りのサポート
-   統計を収集するための構成の永続化のサポート
-   TiKV のログstorageエンジンとしてRaft Engineの使用をサポート (実験的)
-   クラスターに対するバックアップの影響を最適化する
-   Azure Blob storage をバックアップstorageとして使用するサポート
-   TiFlashと MPP エンジンの安定性とパフォーマンスを継続的に改善します。
-   TiDB Lightningにスイッチを追加して、データを含む既存のテーブルへのインポートを許可するかどうかを決定します。
-   継続的プロファイリング機能を最適化する (実験的)
-   TiSpark はユーザーの識別と認証をサポートします

## 互換性の変更 {#compatibility-changes}

> **ノート：**
>
> 以前の TiDB バージョンから v5.4.0 にアップグレードする場合、すべての中間バージョンの互換性変更メモを知りたい場合は、対応するバージョンの[<a href="/releases/release-notes.md">リリースノート</a>](/releases/release-notes.md)を確認できます。

### システム変数 {#system-variables}

| 変数名                                                                                                                                                                               | 種類の変更    | 説明                                                                                                                                                                                                                                                                                                                                              |
| :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [<a href="/system-variables.md#tidb_enable_column_tracking-new-in-v540">`tidb_enable_column_tracking`</a>](/system-variables.md#tidb_enable_column_tracking-new-in-v540)          | 新しく追加された | TiDB が`PREDICATE COLUMNS`を収集できるようにするかどうかを制御します。デフォルト値は`OFF`です。                                                                                                                                                                                                                                                                                  |
| [<a href="/system-variables.md#tidb_enable_paging-new-in-v540">`tidb_enable_paging`</a>](/system-variables.md#tidb_enable_paging-new-in-v540)                                     | 新しく追加された | `IndexLookUp`オペレーターでコプロセッサー要求を送信するためにページングの方法を使用するかどうかを制御します。デフォルト値は`OFF`です。<br/> `IndexLookup`と`Limit`を使用し、 `Limit` `IndexScan`にプッシュダウンできない読み取りクエリの場合、読み取りクエリのレイテンシーが長くなり、TiKV の`unified read pool` CPU 使用率が高くなる可能性があります。このような場合、 `Limit`演算子は少量のデータ セットのみを必要とするため、 `tidb_enable_paging`を`ON`に設定すると、TiDB が処理するデータが減り、クエリのレイテンシーとリソースの消費が削減されます。 |
| [<a href="/system-variables.md#tidb_enable_top_sql-new-in-v540">`tidb_enable_top_sql`</a>](/system-variables.md#tidb_enable_top_sql-new-in-v540)                                  | 新しく追加された | Top SQL機能を有効にするかどうかを制御します。デフォルト値は`OFF`です。                                                                                                                                                                                                                                                                                                       |
| [<a href="/system-variables.md#tidb_persist_analyze_options-new-in-v540">`tidb_persist_analyze_options`</a>](/system-variables.md#tidb_persist_analyze_options-new-in-v540)       | 新しく追加された | [<a href="/statistics.md#persist-analyze-configurations">構成の永続性を分析する</a>](/statistics.md#persist-analyze-configurations)機能を有効にするかどうかを制御します。デフォルト値は`ON`です。                                                                                                                                                                                       |
| [<a href="/system-variables.md#tidb_read_staleness-new-in-v540">`tidb_read_staleness`</a>](/system-variables.md#tidb_read_staleness-new-in-v540)                                  | 新しく追加された | 現在のセッションで読み取ることができる履歴データの範囲を制御します。デフォルト値は`0`です。                                                                                                                                                                                                                                                                                                 |
| [<a href="/system-variables.md#tidb_regard_null_as_point-new-in-v540">`tidb_regard_null_as_point`</a>](/system-variables.md#tidb_regard_null_as_point-new-in-v540)                | 新しく追加された | オプティマイザがインデックス アクセスの接頭辞条件として NULL 等価性を含むクエリ条件を使用できるかどうかを制御します。                                                                                                                                                                                                                                                                                  |
| [<a href="/system-variables.md#tidb_stats_load_sync_wait-new-in-v540">`tidb_stats_load_sync_wait`</a>](/system-variables.md#tidb_stats_load_sync_wait-new-in-v540)                | 新しく追加された | 統計の同期読み込み機能を有効にするかどうかを制御します。デフォルト値`0`は、機能が無効であり、統計が非同期でロードされることを意味します。この機能が有効な場合、この変数は、SQL 最適化が統計の同期読み込みをタイムアウトするまで待機できる最大時間を制御します。                                                                                                                                                                                                             |
| [<a href="/system-variables.md#tidb_stats_load_pseudo_timeout-new-in-v540">`tidb_stats_load_pseudo_timeout`</a>](/system-variables.md#tidb_stats_load_pseudo_timeout-new-in-v540) | 新しく追加された | 統計の同期ロードがタイムアウトに達するタイミング、SQL が失敗するか ( `OFF` )、疑似統計の使用にフォールバックするか ( `ON` ) を制御します。デフォルト値は`OFF`です。                                                                                                                                                                                                                                                |
| [<a href="/system-variables.md#tidb_backoff_lock_fast">`tidb_backoff_lock_fast`</a>](/system-variables.md#tidb_backoff_lock_fast)                                                 | 修正済み     | デフォルト値が`100`から`10`に変更されました。                                                                                                                                                                                                                                                                                                                     |
| [<a href="/system-variables.md#tidb_enable_index_merge-new-in-v40">`tidb_enable_index_merge`</a>](/system-variables.md#tidb_enable_index_merge-new-in-v40)                        | 修正済み     | デフォルト値が`OFF`から`ON`に変更されました。<br/><ul><li> TiDB クラスターを v4.0.0 より前のバージョンから v5.4.0 以降にアップグレードする場合、この変数はデフォルトで`OFF`です。</li><li> TiDB クラスターを v4.0.0 以降から v5.4.0 以降にアップグレードする場合、この変数はアップグレード前と同じままになります。</li><li> v5.4.0 以降の新しく作成された TiDB クラスターの場合、この変数はデフォルトで`ON`です。</li></ul>                                                                        |
| [<a href="/system-variables.md#tidb_store_limit-new-in-v304-and-v40">`tidb_store_limit`</a>](/system-variables.md#tidb_store_limit-new-in-v304-and-v40)                           | 修正済み     | v5.4.0 より前では、この変数はインスタンス レベルでグローバルに設定できます。 v5.4.0 以降、この変数はグローバル構成のみをサポートします。                                                                                                                                                                                                                                                                    |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル  | コンフィグレーション                                                                                                                                                                                          | 種類の変更    | 説明                                                                                                                                                                                                                                                                                                                                                                                              |
| :-------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB            | [<a href="/tidb-configuration-file.md#stats-load-concurrency-new-in-v540">`stats-load-concurrency`</a>](/tidb-configuration-file.md#stats-load-concurrency-new-in-v540)                             | 新しく追加された | TiDB 同期ロード統計機能が同時に処理できる列の最大数を制御します。デフォルト値は`5`です。                                                                                                                                                                                                                                                                                                                                                |
| TiDB            | [<a href="/tidb-configuration-file.md#stats-load-queue-size-new-in-v540">`stats-load-queue-size`</a>](/tidb-configuration-file.md#stats-load-queue-size-new-in-v540)                                | 新しく追加された | TiDB 同期ロード統計機能がキャッシュできる列リクエストの最大数を制御します。デフォルト値は`1000`です。                                                                                                                                                                                                                                                                                                                                        |
| TiKV            | [<a href="/tikv-configuration-file.md#snap-generator-pool-size-new-in-v540">`snap-generator-pool-size`</a>](/tikv-configuration-file.md#snap-generator-pool-size-new-in-v540)                       | 新しく追加された | `snap-generator`スレッド プールのサイズ。デフォルト値は`2`です。                                                                                                                                                                                                                                                                                                                                                      |
| TiKV            | `log.file.max-size` `log.file.max-days` `log.file.max-backups`                                                                                                                                      | 新しく追加された | 詳細は[<a href="/tikv-configuration-file.md#logfile-new-in-v540">TiKVコンフィグレーションファイル - `log.file`</a>](/tikv-configuration-file.md#logfile-new-in-v540)を参照してください。                                                                                                                                                                                                                                   |
| TiKV            | `raft-engine`                                                                                                                                                                                       | 新しく追加された | `enable` 、 `dir` 、 `batch-compression-threshold` 、 `bytes-per-sync` 、 `target-file-size` 、 `purge-threshold` 、 `recovery-mode` 、 `recovery-read-block-size` 、 `recovery-read-block-size` 、および`recovery-threads`が含まれます。詳細については、 [<a href="/tikv-configuration-file.md#raft-engine">TiKVコンフィグレーションファイル - `raft-engine`</a>](/tikv-configuration-file.md#raft-engine)を参照してください。                    |
| TiKV            | [<a href="/tikv-configuration-file.md#enable-auto-tune-new-in-v540">`backup.enable-auto-tune`</a>](/tikv-configuration-file.md#enable-auto-tune-new-in-v540)                                        | 新しく追加された | v5.3.0 では、デフォルト値は`false`です。 v5.4.0 以降、デフォルト値は`true`に変更されました。このパラメーターは、クラスターのリソース使用率が高い場合に、クラスターへの影響を軽減するためにバックアップ タスクで使用されるリソースを制限するかどうかを制御します。デフォルトの構成では、バックアップ タスクの速度が遅くなる可能性があります。                                                                                                                                                                                                           |
| TiKV            | `log-level` `log-format` `log-file` `log-rotation-size`                                                                                                                                             | 修正済み     | TiKV ログ パラメーターの名前は、TiDB ログ パラメーターと一致する名前 ( `log.level` 、 `log.format` 、 `log.file.filename` 、および`log.enable-timestamp`に置き換えられます。古いパラメータのみを設定し、その値がデフォルト以外の値に設定されている場合、古いパラメータは新しいパラメータとの互換性を維持します。古いパラメータと新しいパラメータの両方が設定されている場合は、新しいパラメータが有効になります。詳細は[<a href="/tikv-configuration-file.md#log-new-in-v540">TiKVコンフィグレーションファイル - ログ</a>](/tikv-configuration-file.md#log-new-in-v540)を参照してください。 |
| TiKV            | `log-rotation-timespan`                                                                                                                                                                             | 削除されました  | ログローテーション間の期間。この期間が経過すると、ログ ファイルがローテーションされます。つまり、現在のログ ファイルのファイル名にタイムスタンプが追加され、新しいログ ファイルが作成されます。                                                                                                                                                                                                                                                                                               |
| TiKV            | `allow-remove-leader`                                                                                                                                                                               | 削除されました  | メインスイッチの削除を許可するかどうかを決定します。                                                                                                                                                                                                                                                                                                                                                                      |
| TiKV            | `raft-msg-flush-interval`                                                                                                                                                                           | 削除されました  | Raftメッセージがバッチで送信される間隔を決定します。 Raftメッセージは、この設定項目で指定された間隔ごとにバッチで送信されます。                                                                                                                                                                                                                                                                                                                            |
| PD              | [<a href="/pd-configuration-file.md#level">`log.level`</a>](/pd-configuration-file.md#level)                                                                                                        | 修正済み     | デフォルト値は「INFO」から「info」に変更され、大文字と小文字は区別されません。                                                                                                                                                                                                                                                                                                                                                     |
| TiFlash         | [<a href="/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file">`profile.default.enable_elastic_threadpool`</a>](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)      | 新しく追加された | エラスティック スレッド プール機能を有効にするか無効にするかを決定します。この構成項目を有効にすると、同時実行性が高いシナリオでTiFlash CPU 使用率が大幅に向上します。デフォルト値は`false`です。                                                                                                                                                                                                                                                                                     |
| TiFlash         | [<a href="/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file">`storage.format_version`</a>](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                         | 新しく追加された | DTFileのバージョンを指定します。デフォルト値は`2`で、この値の下ではハッシュがデータ ファイルに埋め込まれます。値を`3`に設定することもできます。 `3`の場合、データ ファイルにはメタデータとトークン データのチェックサムが含まれ、複数のハッシュ アルゴリズムがサポートされます。                                                                                                                                                                                                                                              |
| TiFlash         | [<a href="/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file">`logger.count`</a>](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                                   | 修正済み     | デフォルト値は`10`に変更されます。                                                                                                                                                                                                                                                                                                                                                                             |
| TiFlash         | [<a href="/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file">`status.metrics_port`</a>](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                            | 修正済み     | デフォルト値は`8234`に変更されます。                                                                                                                                                                                                                                                                                                                                                                           |
| TiFlash         | [<a href="/tiflash/tiflash-configuration.md#configure-the-tiflash-learnertoml-file">`raftstore.apply-pool-size`</a>](/tiflash/tiflash-configuration.md#configure-the-tiflash-learnertoml-file)      | 新しく追加された | Raftデータをstorageにフラッシュするプール内のスレッドの許容数。デフォルト値は`4`です。                                                                                                                                                                                                                                                                                                                                              |
| TiFlash         | [<a href="/tiflash/tiflash-configuration.md#configure-the-tiflash-learnertoml-file">`raftstore.store-pool-size`</a>](/tiflash/tiflash-configuration.md#configure-the-tiflash-learnertoml-file)      | 新しく追加された | Raftを処理するスレッドの許容数。これはRaftstoreスレッド プールのサイズです。デフォルト値は`4`です。                                                                                                                                                                                                                                                                                                                                      |
| TiDB データ移行 (DM) | [<a href="/dm/task-configuration-file-full.md#task-configuration-file-template-advanced">`collation_compatible`</a>](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced) | 新しく追加された | デフォルトの照合順序を`CREATE`の SQL ステートメントで同期するモード。値のオプションは「loose」(デフォルト) と「strict」です。                                                                                                                                                                                                                                                                                                                    |
| TiCDC           | `max-message-bytes`                                                                                                                                                                                 | 修正済み     | Kafka シンクのデフォルト値`max-message-bytes` `104857601` (10MB) に変更します。                                                                                                                                                                                                                                                                                                                                  |
| TiCDC           | `partition-num`                                                                                                                                                                                     | 修正済み     | Kafka Sink のデフォルト値`partition-num`を`4`から`3`に変更します。これにより、TiCDC が Kafaka パーティションにメッセージをより均等に送信できるようになります。                                                                                                                                                                                                                                                                                          |
| TiDB Lightning  | `meta-schema-name`                                                                                                                                                                                  | 修正済み     | ターゲット TiDB 内のメタデータのスキーマ名を指定します。 v5.4.0 以降、このスキーマは[<a href="/tidb-lightning/tidb-lightning-distributed-import.md">並行輸入品</a>](/tidb-lightning/tidb-lightning-distributed-import.md)有効にした場合にのみ作成されます (対応するパラメーターは`tikv-importer.incremental-import = true` )。                                                                                                                                      |
| TiDB Lightning  | `task-info-schema-name`                                                                                                                                                                             | 新しく追加された | TiDB Lightning が競合を検出したときに重複データが保存されるデータベースの名前を指定します。デフォルトでは、値は「lightning_task_info」です。このパラメータは、「重複解決」機能を有効にした場合にのみ指定します。                                                                                                                                                                                                                                                                       |
| TiDB Lightning  | `incremental-import`                                                                                                                                                                                | 新しく追加された | データが既に存在するテーブルへのデータのインポートを許可するかどうかを決定します。デフォルト値は`false`です。                                                                                                                                                                                                                                                                                                                                      |

### その他 {#others}

-   TiDB と PD の間にインターフェイスが追加されます。 `information_schema.TIDB_HOT_REGIONS_HISTORY`システム テーブルを使用する場合、TiDB は対応するバージョンの PD を使用する必要があります。
-   TiDB サーバー、PD サーバー、および TiKV サーバーは、ログ名、出力形式、ローテーションと有効期限のルールを管理するために、ログ関連パラメーターに統一された命名方法を使用し始めます。詳細は[<a href="/tikv-configuration-file.md#log-new-in-v540">TiKV 構成ファイル - ログ</a>](/tikv-configuration-file.md#log-new-in-v540)を参照してください。
-   v5.4.0 以降、プラン キャッシュ経由でキャッシュされた実行プランの SQL バインディングを作成すると、バインディングにより、対応するクエリに対してすでにキャッシュされているプランが無効になります。新しいバインディングは、v5.4.0 より前にキャッシュされた実行プランには影響しません。
-   v5.3 以前のバージョンでは、 [<a href="https://docs.pingcap.com/tidb-data-migration/v5.3/">TiDB データ移行 (DM)</a>](https://docs.pingcap.com/tidb-data-migration/v5.3/)ドキュメントは TiDB ドキュメントから独立しています。 v5.4 以降、DM ドキュメントは同じバージョンの TiDB ドキュメントに統合されています。 [<a href="/dm/dm-overview.md">DMドキュメント</a>](/dm/dm-overview.md) DM ドキュメント サイトにアクセスせずに直接読むことができます。
-   cdclog とともにポイントインタイム リカバリ (PITR) の実験的機能を削除します。 v5.4.0 以降、cdclog ベースの PITR および cdclog はサポートされなくなりました。
-   システム変数を「DEFAULT」に設定する動作をより MySQL 互換にする[<a href="https://github.com/pingcap/tidb/pull/29680">#29680</a>](https://github.com/pingcap/tidb/pull/29680)
-   システム変数`lc_time_names`を読み取り専用[<a href="https://github.com/pingcap/tidb/pull/30084">#30084</a>](https://github.com/pingcap/tidb/pull/30084)設定します。
-   `tidb_store_limit`のスコープを INSTANCE または GLOBAL から GLOBAL [<a href="https://github.com/pingcap/tidb/pull/30756">#30756</a>](https://github.com/pingcap/tidb/pull/30756)に設定します。
-   列にゼロが含まれる場合、整数型列を時間型列に変換することを禁止します[<a href="https://github.com/pingcap/tidb/pull/25728">#25728</a>](https://github.com/pingcap/tidb/pull/25728)
-   浮動小数点値を挿入するときに`Inf`または`NAN`値に対してエラーが報告されない問題を修正します[<a href="https://github.com/pingcap/tidb/pull/30148">#30148</a>](https://github.com/pingcap/tidb/pull/30148)
-   自動 ID が範囲[<a href="https://github.com/pingcap/tidb/pull/30301">#30301</a>](https://github.com/pingcap/tidb/pull/30301)の外にある場合、 `REPLACE`ステートメントが他の行を誤って変更する問題を修正します。

## 新機能 {#new-features}

### SQL {#sql}

-   **TiDB は v5.4.0 以降 GBK 文字セットをサポートしています**

    v5.4.0 より前では、TiDB は`ascii` 、 `binary` 、 `latin1` 、 `utf8` 、および`utf8mb4`文字セットをサポートしていました。

    中国人ユーザーのサポートを強化するために、TiDB は v5.4.0 以降 GBK 文字セットをサポートしています。 TiDB クラスターを初めて初期化するときに TiDB 構成ファイルで[<a href="/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap">`new_collations_enabled_on_first_bootstrap`</a>](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap)オプションを有効にすると、TiDB GBK 文字セットは`gbk_bin`照合順序と`gbk_chinese_ci`照合順序の両方をサポートします。

    GBK 文字セットを使用する場合は、互換性の制限に注意する必要があります。詳細は[<a href="/character-set-gbk.md">文字セットと照合順序 - GBK</a>](/character-set-gbk.md)を参照してください。

### Security {#security}

-   **TiSpark はユーザー認証と認可をサポートします**

    TiSpark 2.5.0 以降、TiSpark はデータベース ユーザー認証とデータベースまたはテーブル レベルでの読み取り/書き込み許可の両方をサポートしています。この機能を有効にすると、ビジネスによるデータ取得のための描画などの未承認のバッチ タスクの実行を防ぐことができ、オンライン クラスターの安定性とデータ セキュリティが向上します。

    この機能はデフォルトでは無効になっています。これが有効になっている場合、TiSpark を介して操作しているユーザーに必要な権限がない場合、ユーザーは TiSpark から例外を受け取ります。

    [<a href="/tispark-overview.md#security">ユーザードキュメント</a>](/tispark-overview.md#security)

-   **TiUP は、 root ユーザーの初期パスワードの生成をサポートします**

    クラスターを起動するコマンドに`--init`パラメーターが導入されます。このパラメーターを使用すると、 TiUPを使用してデプロイされた TiDB クラスターで、 TiUP はデータベース root ユーザー用の強力な初期パスワードを生成します。これにより、空のパスワードを持つ root ユーザーを使用する際のセキュリティ リスクが回避され、データベースのセキュリティが確保されます。

    [<a href="/production-deployment-using-tiup.md#step-7-start-a-tidb-cluster">ユーザードキュメント</a>](/production-deployment-using-tiup.md#step-7-start-a-tidb-cluster)

### パフォーマンス {#performance}

-   **カラムナ型storageエンジンTiFlashとコンピューティング エンジン MPP の安定性とパフォーマンスの継続的な向上**

    -   MPP エンジンへのより多くの関数のプッシュダウンをサポートします。

        -   文字列関数: `LPAD()` 、 `RPAD()` 、 `STRCMP()`
        -   日付関数: `ADDDATE(string, real)` 、 `DATE_ADD(string, real)` 、 `DATE_SUB(string, real)` 、 `SUBDATE(string, real)` 、 `QUARTER()`

    -   リソース使用率を向上させるためにエラスティック スレッド プール機能を導入します (実験的)

    -   TiKV からデータをレプリケートする際に、行ベースのstorage形式から列ベースのstorage形式にデータを変換する効率が向上し、データ レプリケーションの全体的なパフォーマンスが 50% 向上します。

    -   一部の構成項目のデフォルト値を調整することで、 TiFlash のパフォーマンスと安定性を向上させます。 HTAP ハイブリッド ロードでは、単一テーブルに対する単純なクエリのパフォーマンスが最大 20% 向上します。

    ユーザードキュメント: [<a href="/tiflash/tiflash-supported-pushdown-calculations.md">サポートされているプッシュダウン計算</a>](/tiflash/tiflash-supported-pushdown-calculations.md) 、 [<a href="/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file">tflash.toml ファイルを構成する</a>](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)

-   **セッション変数を使用して、指定された時間範囲内の履歴データを読み取ります。**

    TiDB は、 Raftコンセンサス アルゴリズムに基づいたマルチレプリカ分散データベースです。高同時実行性と高スループットのアプリケーション シナリオに直面して、TiDB はフォロワー レプリカを通じて読み取りパフォーマンスをスケールアウトし、読み取りリクエストと書き込みリクエストを分離できます。

    さまざまなアプリケーション シナリオに合わせて、TiDB は、強い一貫性のある読み取りと弱い一貫性のある履歴読み取りという 2 つのフォロワー読み取りモードを提供します。強力な一貫性のある読み取りモードは、リアルタイム データを必要とするアプリケーション シナリオに適しています。ただし、このモードでは、リーダーとフォロワーの間のデータ レプリケーションのレイテンシーとスループットの低下により、特に地理的に分散された展開の場合、読み取りリクエストのレイテンシーが長くなる可能性があります。

    リアルタイム データに対する要件がそれほど厳しくないアプリケーション シナリオの場合は、履歴読み取りモードをお勧めします。このモードでは、レイテンシーが短縮され、スループットが向上します。 TiDB は現在、次の方法による履歴データの読み取りをサポートしています。SQL ステートメントを使用して過去の時点からデータを読み取るか、過去の時点に基づいて読み取り専用トランザクションを開始します。どちらの方法でも、特定の時点または指定された時間範囲内の履歴データの読み取りがサポートされています。詳細は[<a href="/as-of-timestamp.md">`AS OF TIMESTAMP`句を使用した履歴データの読み取り</a>](/as-of-timestamp.md)を参照してください。

    v5.4.0 以降、TiDB は、セッション変数を介して指定された時間範囲内の履歴データの読み取りをサポートすることにより、履歴読み取りモードの使いやすさを向上させています。このモードは、準リアルタイムのシナリオで低遅延、高スループットの読み取りリクエストを処理します。変数は次のように設定できます。

    ```sql
    set @@tidb_replica_read=leader_and_follower
    set @@tidb_read_staleness="-5"
    ```

    この設定により、TiDB は最も近いリーダーまたはフォロワー ノードを選択し、5 秒以内に最新の履歴データを読み取ることができます。

    [<a href="/tidb-read-staleness.md">ユーザードキュメント</a>](/tidb-read-staleness.md)

-   **インデックスマージの一般提供**

    Index Merge は、SQL 最適化のための実験的機能として TiDB v4.0 に導入されました。この方法により、クエリで複数のデータ列のスキャンが必要な場合の条件フィルタリングが大幅に高速化されます。次のクエリを例として考えます。 `WHERE`ステートメントでは、 `OR`で接続されたフィルター条件の列*key1*と*key2*にそれぞれのインデックスがある場合、インデックス マージ機能はそれぞれのインデックスを同時にフィルターし、クエリ結果をマージし、マージされた結果を返します。

    ```sql
    SELECT * FROM table WHERE key1 <= 100 OR key2 = 200;
    ```

    TiDB v4.0 より前では、テーブルのクエリでは、フィルター処理に一度に 1 つのインデックスのみの使用がサポートされていました。複数の列のデータをクエリする場合は、インデックス マージを有効にして、個々の列のインデックスを使用して正確なクエリ結果を短時間で取得できます。インデックス マージにより、不必要なテーブル全体のスキャンが回避され、多数の複合インデックスを確立する必要がありません。

    v5.4.0 では、インデックス マージが GA になります。ただし、次の制限事項に注意する必要があります。

    -   インデックス マージは、選言正規形 (X <sub>1</sub> ⋁ X <sub>2</sub> ⋁ …X <sub>n</sub> ) のみをサポートします。つまり、この機能は、 `WHERE`句のフィルター条件が`OR`で接続されている場合にのみ機能します。

    -   v5.4.0 以降の新しくデプロイされた TiDB クラスターの場合、この機能はデフォルトで有効になっています。以前のバージョンからアップグレードされた v5.4.0 以降の TiDB クラスターの場合、この機能はアップグレード前の設定を継承し、必要に応じて設定を変更できます (v4.0 より前の TiDB クラスターの場合、この機能は存在せず、デフォルトで無効になっています)。 。

    [<a href="/explain-index-merge.md">ユーザードキュメント</a>](/explain-index-merge.md)

-   **Raft Engineのサポート (実験的)**

    TiKV のログstorageエンジンとして[<a href="https://github.com/tikv/raft-engine">Raft Engine</a>](https://github.com/tikv/raft-engine)の使用をサポートします。 RocksDB と比較して、 Raft Engine はTiKV I/O 書き込みトラフィックを最大 40% 削減し、CPU 使用率を 10% 削減すると同時に、特定の負荷の下でフォアグラウンドレイテンシーを約 5% 向上させ、テール レイテンシーを 20% 削減します。さらに、 Raft Engine はログのリサイクル効率を向上させ、極限状態でのログの蓄積の問題を解決します。

    Raft Engine はまだ実験的機能であり、デフォルトでは無効になっています。 v5.4.0 のRaft Engineのデータ形式は以前のバージョンと互換性がないことに注意してください。クラスターをアップグレードする前に、すべての TiKV ノードのRaft Engineが無効になっていることを確認する必要があります。 Raft Engine はv5.4.0 以降のバージョンでのみ使用することをお勧めします。

    [<a href="/tikv-configuration-file.md#raft-engine">ユーザードキュメント</a>](/tikv-configuration-file.md#raft-engine)

-   **`PREDICATE COLUMNS`での統計収集のサポート (実験的)**

    ほとんどの場合、SQL ステートメントを実行するとき、オプティマイザーは一部の列 ( `WHERE` 、 `JOIN` 、 `ORDER BY` 、および`GROUP BY`ステートメントの列など) の統計のみを使用します。これらの使用される列は`PREDICATE COLUMNS`と呼ばれます。

    v5.4.0 以降、 [<a href="/system-variables.md#tidb_enable_column_tracking-new-in-v540">`tidb_enable_column_tracking`</a>](/system-variables.md#tidb_enable_column_tracking-new-in-v540)システム変数の値を`ON`に設定して、TiDB が`PREDICATE COLUMNS`を収集できるようにすることができます。

    設定後、TiDB は 100 * [<a href="/tidb-configuration-file.md#stats-lease">`stats-lease`</a>](/tidb-configuration-file.md#stats-lease)ごとに`PREDICATE COLUMNS`情報を`mysql.column_stats_usage`システムテーブルに書き込みます。ビジネスのクエリ パターンが安定している場合は、 `ANALYZE TABLE TableName PREDICATE COLUMNS`構文を使用して`PREDICATE COLUMNS`列のみの統計を収集できます。これにより、統計収集のオーバーヘッドを大幅に削減できます。

    [<a href="/statistics.md#collect-statistics-on-some-columns">ユーザードキュメント</a>](/statistics.md#collect-statistics-on-some-columns)

-   **統計の同期読み込みをサポート (実験的)**

    v5.4.0 以降、TiDB には統計の同期ロード機能が導入されました。この機能はデフォルトでは無効になっています。この機能を有効にすると、TiDB は SQL ステートメントの実行時に大きなサイズの統計 (ヒストグラム、TopN、Count-Min Sketch 統計など) をメモリに同期的にロードできるようになり、SQL 最適化のための統計の完全性が向上します。

    [<a href="/statistics.md#load-statistics">ユーザードキュメント</a>](/statistics.md#load-statistics)

### 安定性 {#stability}

-   **永続的な ANALYZE 構成のサポート**

    統計は、オプティマイザが実行計画を生成するときに参照する基本情報の 1 つです。統計の精度は、生成された実行計画が妥当かどうかに直接影響します。統計の正確性を確保するには、異なるテーブル、パーティション、インデックスに対して異なる収集構成を設定することが必要になる場合があります。

    v5.4.0 以降、TiDB は一部の`ANALYZE`構成の永続化をサポートします。この機能を使用すると、既存の構成を将来の統計収集に簡単に再利用できます。

    `ANALYZE`構成永続機能はデフォルトで有効になっています (デフォルトでは、システム変数`tidb_analyze_version`は`2` [<a href="/system-variables.md#tidb_persist_analyze_options-new-in-v540">`tidb_persist_analyze_options`</a>](/system-variables.md#tidb_persist_analyze_options-new-in-v540) `ON`です)。この機能を使用すると、ステートメントを手動で実行するときに`ANALYZE`ステートメントで指定された永続性構成を記録できます。一度記録されると、次回 TiDB が自動的に統計を更新するとき、またはこれらの構成を指定せずに統計を手動で収集するときに、TiDB は記録された構成に従って統計を収集します。

    [<a href="/statistics.md#persist-analyze-configurations">ユーザードキュメント</a>](/statistics.md#persist-analyze-configurations)

### 高可用性と災害復旧 {#high-availability-and-disaster-recovery}

-   **クラスタに対するバックアップ タスクの影響を軽減する**

    バックアップと復元 (BR) には、自動調整機能が導入されています (デフォルトで有効)。この機能は、クラスターのリソース使用状況を監視し、バックアップ タスクで使用されるスレッドの数を調整することにより、クラスターに対するバックアップ タスクの影響を軽減できます。場合によっては、バックアップ用のクラスター ハードウェア リソースを増やし、自動調整機能を有効にすると、クラスターに対するバックアップ タスクの影響を 10% 以下に制限できます。

    [<a href="/br/br-auto-tune.md">ユーザードキュメント</a>](/br/br-auto-tune.md)

-   **バックアップのターゲットstorageとして Azure Blob Storage をサポート**

    バックアップと復元 (BR) は、リモート バックアップstorageとして Azure Blob Storage をサポートします。 TiDB を Azure クラウドにデプロイすると、クラスター データを Azure Blob Storage サービスにバックアップできるようになります。

    [<a href="/br/backup-and-restore-storages.md">ユーザードキュメント</a>](/br/backup-and-restore-storages.md)

### データ移行 {#data-migration}

-   **TiDB Lightning は、データを含むテーブルへのデータのインポートを許可するかどうかを決定する新機能を導入します。**

    TiDB Lightning には、構成項目`incremental-import`が導入されています。データを含むテーブルへのデータのインポートを許可するかどうかを決定します。デフォルト値は`false`です。並行インポート モードを使用する場合は、構成を`true`に設定する必要があります。

    [<a href="/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task">ユーザードキュメント</a>](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)

-   **TiDB Lightning、並行インポート用のメタ情報を保存するスキーマ名が導入されています**

    TiDB Lightning には`meta-schema-name`構成項目が導入されています。並列インポート モードでは、このパラメータは、ターゲット クラスタ内の各TiDB Lightningインスタンスのメタ情報を保存するスキーマ名を指定します。デフォルトでは、値は「lightning_metadata」です。このパラメータに設定された値は、同じ並行インポートに参加する各TiDB Lightningインスタンスで同じである必要があります。そうしないと、インポートされたデータの正確性が保証されません。

    [<a href="/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task">ユーザードキュメント</a>](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)

-   **TiDB Lightning重複解決の導入**

    ローカル バックエンド モードでは、 TiDB Lightning はデータのインポートが完了する前に重複したデータを出力し、その重複したデータをデータベースから削除します。インポートの完了後に重複データを解決し、アプリケーション ルールに従って挿入する適切なデータを選択できます。後続の増分データ移行フェーズで発生する重複データによって引き起こされるデータの不整合を避けるために、重複データに基づいてアップストリーム データ ソースをクリーンアップすることをお勧めします。

    [<a href="/tidb-lightning/tidb-lightning-error-resolution.md">ユーザードキュメント</a>](/tidb-lightning/tidb-lightning-error-resolution.md)

-   **TiDB Data Migration (DM) でのリレー ログの使用を最適化する**

    -   `source`構成の`enable-relay`スイッチを復旧します。

    -   `start-relay`および`stop-relay`コマンドを使用したリレー ログの動的有効化および無効化をサポートします。

    -   リレーログのステータスを`source`にバインドします。 `source` 、DM ワーカーに移行された後も、有効または無効の元のステータスを維持します。

    -   中継ログのstorageパスをDM-worker設定ファイルに移動します。

    [<a href="/dm/relay-log.md">ユーザードキュメント</a>](/dm/relay-log.md)

-   **DMの<a href="/character-set-and-collation.md">照合順序</a>処理を最適化する**

    `collation_compatible`設定項目を追加します。値のオプションは`loose` (デフォルト) と`strict`です。

    -   アプリケーションに照合順序に関する厳密な要件がなく、クエリ結果の照合順序がアップストリームとダウンストリームで異なる場合がある場合は、デフォルトの`loose`モードを使用してエラーのレポートを回避できます。
    -   アプリケーションに照合順序に関する厳格な要件があり、照合順序がアップストリームとダウンストリーム間で一貫している必要がある場合は、 `strict`モードを使用できます。ただし、ダウンストリームがアップストリームのデフォルトの照合順序をサポートしていない場合、データ レプリケーションでエラーが報告される可能性があります。

    [<a href="/dm/task-configuration-file-full.md#task-configuration-file-template-advanced">ユーザードキュメント</a>](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)

-   **DM の`transfer source`最適化して、レプリケーション タスクのスムーズな実行をサポートします。**

    DM ワーカー ノードに不均衡な負荷がある場合、 `transfer source`コマンドを使用して`source`の設定を別の負荷に手動で転送できます。最適化後、 `transfer source`コマンドにより手動操作が簡素化されます。 DM は他の操作を内部で完了するため、関連するすべてのタスクを一時停止することなく、ソースをスムーズに転送できます。

-   **DM OpenAPI が一般提供 (GA) になりました**

    DM は、データソースの追加やタスクの管理など、API を介した日常的な管理をサポートします。 v5.4.0 では、DM OpenAPI が GA になります。

    [<a href="/dm/dm-open-api.md">ユーザードキュメント</a>](/dm/dm-open-api.md)

### 診断効率 {#diagnostic-efficiency}

-   **Top SQL (実験的機能)**

    新しい実験的機能であるTop SQL (デフォルトでは無効) は、ソースを消費するクエリを簡単に見つけられるように導入されました。

    [<a href="/dashboard/top-sql.md">ユーザードキュメント</a>](/dashboard/top-sql.md)

### TiDB データ共有サブスクリプション {#tidb-data-share-subscription}

-   **クラスターに対する TiCDC の影響を最適化する**

    TiCDC を使用する場合、TiDB クラスターのパフォーマンスへの影響が大幅に軽減されます。テスト環境では、TiCDC が TiDB に与えるパフォーマンスへの影響は 5% 未満に抑えることができます。

### 導入とメンテナンス {#deployment-and-maintenance}

-   **継続的プロファイリングの強化 (実験的)**

    -   サポートされるコンポーネントの増加: TiDB、PD、TiKV に加えて、TiDB v5.4.0 はTiFlashの CPU プロファイリングもサポートします。

    -   より多くの形式のプロファイリング表示: フレーム チャートでの CPU プロファイリングと Goroutine の結果の表示をサポートします。

    -   より多くのデプロイメント環境がサポートされています: 継続的プロファイリングは、 TiDB Operatorを使用してデプロイされたクラスターにも使用できます。

    継続的プロファイリングはデフォルトでは無効になっていますが、TiDB ダッシュボードで有効にできます。

    継続的プロファイリングは、v1.9.0 以降のTiUPまたは v1.3.0 以降のTiDB Operatorを使用してデプロイまたはアップグレードされたクラスターに適用できます。

    [<a href="/dashboard/continuous-profiling.md">ユーザードキュメント</a>](/dashboard/continuous-profiling.md)

## 改善点 {#improvements}

-   TiDB

    -   キャッシュされたクエリ プラン[<a href="https://github.com/pingcap/tidb/pull/30370">#30370</a>](https://github.com/pingcap/tidb/pull/30370)をクリアするための`ADMIN {SESSION | INSTANCE | GLOBAL} PLAN_CACHE`構文をサポートします。

-   TiKV

    -   コプロセッサーは、ストリームのような方法でリクエストを処理するためのページング API をサポートしています[<a href="https://github.com/tikv/tikv/issues/11448">#11448</a>](https://github.com/tikv/tikv/issues/11448)
    -   サポート`read-through-lock`により、読み取り操作が二次ロックが解決されるまで待機する必要がなくなります[<a href="https://github.com/tikv/tikv/issues/11402">#11402</a>](https://github.com/tikv/tikv/issues/11402)
    -   ディスク領域の枯渇によるpanicを回避するために、ディスク保護メカニズムを追加します[<a href="https://github.com/tikv/tikv/issues/10537">#10537</a>](https://github.com/tikv/tikv/issues/10537)
    -   ログのアーカイブとローテーションをサポート[<a href="https://github.com/tikv/tikv/issues/11651">#11651</a>](https://github.com/tikv/tikv/issues/11651)
    -   Raftクライアントによるシステムコールを削減し、CPU 効率を向上させます[<a href="https://github.com/tikv/tikv/issues/11309">#11309</a>](https://github.com/tikv/tikv/issues/11309)
    -   コプロセッサーは、 TiKV [<a href="https://github.com/tikv/tikv/issues/11495">#11495</a>](https://github.com/tikv/tikv/issues/11495)へのサブストリングのプッシュダウンをサポートします
    -   Read Committed 分離レベル[<a href="https://github.com/tikv/tikv/issues/11485">#11485</a>](https://github.com/tikv/tikv/issues/11485)で読み取りロックをスキップすることで、スキャンのパフォーマンスを向上させます。
    -   バックアップ操作で使用されるデフォルトのスレッド プール サイズを減らし、ストレスが高い場合のスレッド プールの使用を制限します[<a href="https://github.com/tikv/tikv/issues/11000">#11000</a>](https://github.com/tikv/tikv/issues/11000)
    -   アプライ スレッド プールとストア スレッド プールのサイズの動的調整のサポート[<a href="https://github.com/tikv/tikv/issues/11159">#11159</a>](https://github.com/tikv/tikv/issues/11159)
    -   `snap-generator`スレッド プール[<a href="https://github.com/tikv/tikv/issues/11247">#11247</a>](https://github.com/tikv/tikv/issues/11247)のサイズの構成をサポート
    -   頻繁に読み取りと書き込みが行われるファイルが多数ある場合に発生するグローバル ロック競合の問題を最適化します[<a href="https://github.com/tikv/rocksdb/pull/250">#250</a>](https://github.com/tikv/rocksdb/pull/250)

-   PD

    -   デフォルトで過去のホットスポット情報を記録します[<a href="https://github.com/pingcap/tidb/issues/25281">#25281</a>](https://github.com/pingcap/tidb/issues/25281)
    -   リクエストの送信元を識別するための HTTPコンポーネントの署名の追加[<a href="https://github.com/tikv/pd/issues/4490">#4490</a>](https://github.com/tikv/pd/issues/4490)
    -   TiDB ダッシュボードを v2021.12.31 に更新します[<a href="https://github.com/tikv/pd/issues/4257">#4257</a>](https://github.com/tikv/pd/issues/4257)

-   TiFlash

    -   現地オペレーターのコミュニケーションを最適化する
    -   スレッドの頻繁な作成または破棄を避けるために、gRPC の非一時スレッド数を増やします。

-   ツール

    -   バックアップと復元 (BR)

        -   BR が暗号化バックアップを実行するときにキーの有効性チェックを追加します[<a href="https://github.com/pingcap/tidb/issues/29794">#29794</a>](https://github.com/pingcap/tidb/issues/29794)

    -   TiCDC

        -   「EventFeed 再試行速度制限」ログの数を減らす[<a href="https://github.com/pingcap/tiflow/issues/4006">#4006</a>](https://github.com/pingcap/tiflow/issues/4006)
        -   多数のテーブルをレプリケートする場合のレプリケーションのレイテンシーを短縮します[<a href="https://github.com/pingcap/tiflow/issues/3900">#3900</a>](https://github.com/pingcap/tiflow/issues/3900)
        -   TiKV ストアがダウンした場合に KV クライアントが回復するまでの時間を短縮します[<a href="https://github.com/pingcap/tiflow/issues/3191">#3191</a>](https://github.com/pingcap/tiflow/issues/3191)

    -   TiDB データ移行 (DM)

        -   リレー有効時のCPU使用率を下げる[<a href="https://github.com/pingcap/dm/issues/2214">#2214</a>](https://github.com/pingcap/dm/issues/2214)

    -   TiDB Lightning

        -   TiDB バックエンド モード[<a href="https://github.com/pingcap/tidb/pull/30953">#30953</a>](https://github.com/pingcap/tidb/pull/30953)でのパフォーマンスを向上させるために、デフォルトで楽観的トランザクションを使用してデータを書き込みます

    -   Dumpling

        -   Dumpling がデータベース バージョン[<a href="https://github.com/pingcap/tidb/pull/29500">#29500</a>](https://github.com/pingcap/tidb/pull/29500)をチェックする際の互換性を向上しました。
        -   `CREATE DATABASE`と`CREATE TABLE`をダンプするときにデフォルトの照合順序を追加します[<a href="https://github.com/pingcap/tiflow/issues/3420">#3420</a>](https://github.com/pingcap/tiflow/issues/3420)

## バグの修正 {#bug-fixes}

-   TiDB

    -   クラスターを v4.x から v5.x にアップグレードするときに発生する`tidb_analyze_version`値の変更の問題を修正します[<a href="https://github.com/pingcap/tidb/issues/25422">#25422</a>](https://github.com/pingcap/tidb/issues/25422)
    -   サブクエリ[<a href="https://github.com/pingcap/tidb/issues/30748">#30748</a>](https://github.com/pingcap/tidb/issues/30748)で異なる照合順序を使用すると間違った結果が発生する問題を修正します。
    -   TiDB の`concat(ifnull(time(3))`の結果が MySQL [<a href="https://github.com/pingcap/tidb/issues/29498">#29498</a>](https://github.com/pingcap/tidb/issues/29498)の結果と異なる問題を修正
    -   楽観的トランザクション モード[<a href="https://github.com/pingcap/tidb/issues/30410">#30410</a>](https://github.com/pingcap/tidb/issues/30410)での潜在的なデータ インデックスの不一致の問題を修正します。
    -   式を TiKV [<a href="https://github.com/pingcap/tidb/issues/30200">#30200</a>](https://github.com/pingcap/tidb/issues/30200)にプッシュダウンできない場合、IndexMerge のクエリ実行プランが間違っている問題を修正
    -   同時に列の型を変更すると、スキーマとデータの間で不整合が発生する問題を修正します[<a href="https://github.com/pingcap/tidb/issues/31048">#31048</a>](https://github.com/pingcap/tidb/issues/31048)
    -   サブクエリ[<a href="https://github.com/pingcap/tidb/issues/30913">#30913</a>](https://github.com/pingcap/tidb/issues/30913)がある場合にIndexMergeクエリの結果が正しくない問題を修正
    -   クライアント[<a href="https://github.com/pingcap/tidb/issues/30896">#30896</a>](https://github.com/pingcap/tidb/issues/30896)で FetchSize が大きすぎるときに発生するpanicの問題を修正します。
    -   LEFT JOIN が誤って INNER JOIN [<a href="https://github.com/pingcap/tidb/issues/20510">#20510</a>](https://github.com/pingcap/tidb/issues/20510)に変換される可能性がある問題を修正
    -   `CASE-WHEN`式と照合順序を併用するとpanicが発生する場合がある問題を修正[<a href="https://github.com/pingcap/tidb/issues/30245">#30245</a>](https://github.com/pingcap/tidb/issues/30245)
    -   `IN`値にバイナリ定数[<a href="https://github.com/pingcap/tidb/issues/31261">#31261</a>](https://github.com/pingcap/tidb/issues/31261)含まれている場合に、間違ったクエリ結果が発生する問題を修正しました。
    -   CTE にサブクエリ[<a href="https://github.com/pingcap/tidb/issues/31255">#31255</a>](https://github.com/pingcap/tidb/issues/31255)がある場合に誤ったクエリ結果が発生する問題を修正
    -   `INSERT ... SELECT ... ON DUPLICATE KEY UPDATE`ステートメントを実行するとpanic[<a href="https://github.com/pingcap/tidb/issues/28078">#28078</a>](https://github.com/pingcap/tidb/issues/28078)が発生する問題を修正
    -   INDEX HASH JOIN が`send on closed channel`エラー[<a href="https://github.com/pingcap/tidb/issues/31129">#31129</a>](https://github.com/pingcap/tidb/issues/31129)を返す問題を修正

-   TiKV

    -   MVCC 削除レコードが GC [<a href="https://github.com/tikv/tikv/issues/11217">#11217</a>](https://github.com/tikv/tikv/issues/11217)によってクリアされない問題を修正
    -   悲観的トランザクションモードでプリライトリクエストを再試行すると、まれにデータ不整合のリスクが発生する可能性がある問題を修正します[<a href="https://github.com/tikv/tikv/issues/11187">#11187</a>](https://github.com/tikv/tikv/issues/11187)
    -   GC スキャンによりメモリオーバーフローが発生する問題を修正[<a href="https://github.com/tikv/tikv/issues/11410">#11410</a>](https://github.com/tikv/tikv/issues/11410)
    -   ディスク容量がいっぱいの場合、RocksDB のフラッシュまたは圧縮によってpanicが発生する問題を修正します[<a href="https://github.com/tikv/tikv/issues/11224">#11224</a>](https://github.com/tikv/tikv/issues/11224)

-   PD

    -   リージョン統計が`flow-round-by-digit` [<a href="https://github.com/tikv/pd/issues/4295">#4295</a>](https://github.com/tikv/pd/issues/4295)の影響を受けない問題を修正
    -   ターゲット ストアがダウンしているため、スケジューリング オペレーターがフェイル ファストできない問題を修正します[<a href="https://github.com/tikv/pd/issues/3353">#3353</a>](https://github.com/tikv/pd/issues/3353)
    -   オフラインストア上のリージョンを結合できない問題を修正[<a href="https://github.com/tikv/pd/issues/4119">#4119</a>](https://github.com/tikv/pd/issues/4119)
    -   コールド ホットスポット データがホットスポット統計[<a href="https://github.com/tikv/pd/issues/4390">#4390</a>](https://github.com/tikv/pd/issues/4390)から削除できない問題を修正します。

-   TiFlash

    -   MPP クエリが停止するとTiFlash がpanicになる問題を修正
    -   `where <string>`句を含むクエリが間違った結果を返す問題を修正
    -   整数の主キーの列タイプをより大きな範囲に設定するときに発生する可能性があるデータの不整合の潜在的な問題を修正します。
    -   入力時刻が 1970-01-01 00:00:01 UTC より前の場合、 `unix_timestamp`の動作が TiDB または MySQL の動作と一致しない問題を修正
    -   TiFlashの再起動後に`EstablishMPPConnection`エラーが返される場合がある問題を修正
    -   TiFlashと TiDB/TiKV で`CastStringAsDecimal`動作が矛盾する問題を修正
    -   クエリ結果で`DB::Exception: Encode type of coprocessor response is not CHBlock`エラーが返される問題を修正
    -   TiFlashと TiDB/TiKV で`castStringAsReal`動作が矛盾する問題を修正
    -   TiFlashの`date_add_string_xxx`関数の返された結果が MySQL の結果と一致しない問題を修正

-   ツール

    -   バックアップと復元 (BR)

        -   復元操作の完了後にリージョンの分布が不均一になる可能性があるという潜在的な問題を修正します[<a href="https://github.com/pingcap/tidb/issues/30425">#30425</a>](https://github.com/pingcap/tidb/issues/30425)
        -   `minio`をバックアップstorageとして使用する場合、エンドポイントに`'/'`指定できない問題を修正[<a href="https://github.com/pingcap/tidb/issues/30104">#30104</a>](https://github.com/pingcap/tidb/issues/30104)
        -   システム テーブルを同時にバックアップするとテーブル名の更新に失敗するため、システム テーブルを復元できない問題を修正します[<a href="https://github.com/pingcap/tidb/issues/29710">#29710</a>](https://github.com/pingcap/tidb/issues/29710)

    -   TiCDC

        -   `min.insync.replicas`が`replication-factor` [<a href="https://github.com/pingcap/tiflow/issues/3994">#3994</a>](https://github.com/pingcap/tiflow/issues/3994)より小さい場合にレプリケーションが実行できない問題を修正
        -   `cached region`監視メトリクスがマイナス[<a href="https://github.com/pingcap/tiflow/issues/4300">#4300</a>](https://github.com/pingcap/tiflow/issues/4300)になる問題を修正
        -   `mq sink write row`監視データがない問題を修正[<a href="https://github.com/pingcap/tiflow/issues/3431">#3431</a>](https://github.com/pingcap/tiflow/issues/3431)
        -   `sql mode` [<a href="https://github.com/pingcap/tiflow/issues/3810">#3810</a>](https://github.com/pingcap/tiflow/issues/3810)の互換性の問題を修正
        -   レプリケーション タスクが削除されたときに発生する潜在的なpanicの問題を修正します[<a href="https://github.com/pingcap/tiflow/issues/3128">#3128</a>](https://github.com/pingcap/tiflow/issues/3128)
        -   デフォルトの列値[<a href="https://github.com/pingcap/tiflow/issues/3929">#3929</a>](https://github.com/pingcap/tiflow/issues/3929)を出力するときに発生するpanicとデータの不整合の問題を修正します。
        -   デフォルト値を複製できない問題を修正[<a href="https://github.com/pingcap/tiflow/issues/3793">#3793</a>](https://github.com/pingcap/tiflow/issues/3793)
        -   デッドロックによりレプリケーション タスクが停止するという潜在的な問題を修正します[<a href="https://github.com/pingcap/tiflow/issues/4055">#4055</a>](https://github.com/pingcap/tiflow/issues/4055)
        -   ディスクへの書き込みが完了したときにログが出力されない問題を修正[<a href="https://github.com/pingcap/tiflow/issues/3362">#3362</a>](https://github.com/pingcap/tiflow/issues/3362)
        -   DDL ステートメント内の特別なコメントによりレプリケーション タスクが停止する問題を修正します[<a href="https://github.com/pingcap/tiflow/issues/3755">#3755</a>](https://github.com/pingcap/tiflow/issues/3755)
        -   RHEL リリース[<a href="https://github.com/pingcap/tiflow/issues/3584">#3584</a>](https://github.com/pingcap/tiflow/issues/3584)のタイムゾーンの問題によりサービスを開始できない問題を修正
        -   不正確なチェックポイント[<a href="https://github.com/pingcap/tiflow/issues/3545">#3545</a>](https://github.com/pingcap/tiflow/issues/3545)によって引き起こされる潜在的なデータ損失の問題を修正します。
        -   コンテナ環境の OOM 問題を修正する[<a href="https://github.com/pingcap/tiflow/issues/1798">#1798</a>](https://github.com/pingcap/tiflow/issues/1798)
        -   `config.Metadata.Timeout` [<a href="https://github.com/pingcap/tiflow/issues/3352">#3352</a>](https://github.com/pingcap/tiflow/issues/3352)の誤った構成によって引き起こされるレプリケーション停止の問題を修正します。

    -   TiDB データ移行 (DM)

        -   `CREATE VIEW`ステートメントがデータ レプリケーション[<a href="https://github.com/pingcap/tiflow/issues/4173">#4173</a>](https://github.com/pingcap/tiflow/issues/4173)を中断する問題を修正します。
        -   DDL ステートメントがスキップされた後にスキーマをリセットする必要がある問題を修正します[<a href="https://github.com/pingcap/tiflow/issues/4177">#4177</a>](https://github.com/pingcap/tiflow/issues/4177)
        -   DDL ステートメントがスキップされた後、テーブル チェックポイントが時間内に更新されない問題を修正します[<a href="https://github.com/pingcap/tiflow/issues/4184">#4184</a>](https://github.com/pingcap/tiflow/issues/4184)
        -   TiDB バージョンとパーサー バージョン[<a href="https://github.com/pingcap/tiflow/issues/4298">#4298</a>](https://github.com/pingcap/tiflow/issues/4298)の互換性の問題を修正しました。
        -   ステータス[<a href="https://github.com/pingcap/tiflow/issues/4281">#4281</a>](https://github.com/pingcap/tiflow/issues/4281)をクエリする場合にのみ同期メトリクスが更新される問題を修正

    -   TiDB Lightning

        -   TiDB Lightning にテーブル`mysql.tidb`へのアクセス権限[<a href="https://github.com/pingcap/tidb/issues/31088">#31088</a>](https://github.com/pingcap/tidb/issues/31088)ない場合にインポート結果が正しくない問題を修正
        -   TiDB Lightningの再起動時に一部のチェックがスキップされる問題を修正[<a href="https://github.com/pingcap/tidb/issues/30772">#30772</a>](https://github.com/pingcap/tidb/issues/30772)
        -   S3 パスが存在しない場合にTiDB Lightning がエラーを報告できない問題を修正します[<a href="https://github.com/pingcap/tidb/pull/30674">#30674</a>](https://github.com/pingcap/tidb/pull/30674)

    -   TiDBBinlog

        -   `CREATE PLACEMENT POLICY`ステートメント[<a href="https://github.com/pingcap/tidb-binlog/issues/1118">#1118</a>](https://github.com/pingcap/tidb-binlog/issues/1118)と互換性がないためにDrainerが失敗する問題を修正
