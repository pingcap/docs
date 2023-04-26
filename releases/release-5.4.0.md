---
title: TiDB 5.4 Release Notes
---

# TiDB 5.4 リリースノート {#tidb-5-4-release-notes}

発売日：2022年2月15日

TiDB バージョン: 5.4.0

v5.4 の主な新機能または改善点は次のとおりです。

-   GBK 文字セットをサポート
-   複数の列のインデックスのフィルタリング結果をマージする Index Merge を使用したデータ アクセスのサポート
-   セッション変数を使用した古いデータの読み取りをサポート
-   統計を収集するための構成の永続化をサポート
-   Raft Engineを TiKV のログstorageエンジンとしてサポート (実験的)
-   クラスターに対するバックアップの影響を最適化する
-   バックアップstorageとしての Azure Blob storageの使用をサポート
-   TiFlashと MPP エンジンの安定性とパフォーマンスを継続的に改善します
-   TiDB Lightningにスイッチを追加して、データを含む既存のテーブルへのインポートを許可するかどうかを決定します
-   継続的なプロファイリング機能を最適化 (実験的)
-   TiSpark はユーザーの識別と認証をサポートします

## 互換性の変更 {#compatibility-changes}

> **ノート：**
>
> 以前の TiDB バージョンから v5.4.0 にアップグレードする場合、すべての中間バージョンの互換性の変更点を知りたい場合は、該当するバージョンの[リリースノート](/releases/release-notes.md)を確認できます。

### システム変数 {#system-variables}

| 変数名                                                                                                 | タイプを変更 | 説明                                                                                                                                                                                                                                                                                                                                        |
| :-------------------------------------------------------------------------------------------------- | :----- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`tidb_enable_column_tracking`](/system-variables.md#tidb_enable_column_tracking-new-in-v540)       | 新規追加   | TiDB が`PREDICATE COLUMNS`を収集できるようにするかどうかを制御します。デフォルト値は`OFF`です。                                                                                                                                                                                                                                                                            |
| [`tidb_enable_paging`](/system-variables.md#tidb_enable_paging-new-in-v540)                         | 新規追加   | ページング方式を使用して`IndexLookUp`のオペレーターでコプロセッサー要求を送信するかどうかを制御します。デフォルト値は`OFF`です。<br/> `IndexLookup`と`Limit`使用し、 `Limit` `IndexScan`にプッシュできない読み取りクエリの場合、読み取りクエリのレイテンシーが高くなり、TiKV の`unified read pool` CPU 使用率が高くなる可能性があります。このような場合、 `Limit`演算子は小さなデータセットしか必要としないため、 `tidb_enable_paging`を`ON`に設定すると、TiDB が処理するデータが少なくなり、クエリのレイテンシーとリソース消費が削減されます。 |
| [`tidb_enable_top_sql`](/system-variables.md#tidb_enable_top_sql-new-in-v540)                       | 新規追加   | Top SQL機能を有効にするかどうかを制御します。デフォルト値は`OFF`です。                                                                                                                                                                                                                                                                                                 |
| [`tidb_persist_analyze_options`](/system-variables.md#tidb_persist_analyze_options-new-in-v540)     | 新規追加   | [ANALYZE 構成の永続性](/statistics.md#persist-analyze-configurations)機能を有効にするかどうかを制御します。デフォルト値は`ON`です。                                                                                                                                                                                                                                          |
| [`tidb_read_staleness`](/system-variables.md#tidb_read_staleness-new-in-v540)                       | 新規追加   | 現在のセッションで読み取ることができる履歴データの範囲を制御します。デフォルト値は`0`です。                                                                                                                                                                                                                                                                                           |
| [`tidb_regard_null_as_point`](/system-variables.md#tidb_regard_null_as_point-new-in-v540)           | 新規追加   | オプティマイザーが NULL 等価を含むクエリ条件をインデックス アクセスのプレフィックス条件として使用できるかどうかを制御します。                                                                                                                                                                                                                                                                        |
| [`tidb_stats_load_sync_wait`](/system-variables.md#tidb_stats_load_sync_wait-new-in-v540)           | 新規追加   | 統計の同期読み込み機能を有効にするかどうかを制御します。デフォルト値`0`は、機能が無効になっており、統計が非同期にロードされることを意味します。この機能が有効になっている場合、この変数は、SQL 最適化がタイムアウトになる前に統計を同期的にロードするのを待機できる最大時間を制御します。                                                                                                                                                                                          |
| [`tidb_stats_load_pseudo_timeout`](/system-variables.md#tidb_stats_load_pseudo_timeout-new-in-v540) | 新規追加   | SQL が失敗する ( `OFF` ) か、疑似統計を使用するようにフォールバックする ( `ON` ) かで、統計の同期ロードがタイムアウトに達するタイミングを制御します。デフォルト値は`OFF`です。                                                                                                                                                                                                                                    |
| [`tidb_backoff_lock_fast`](/system-variables.md#tidb_backoff_lock_fast)                             | 修正済み   | デフォルト値が`100`から`10`に変更されました。                                                                                                                                                                                                                                                                                                               |
| [`tidb_enable_index_merge`](/system-variables.md#tidb_enable_index_merge-new-in-v40)                | 修正済み   | デフォルト値が`OFF`から`ON`に変更されました。<br/><ul><li> TiDB クラスターを v4.0.0 より前のバージョンから v5.4.0 以降にアップグレードする場合、この変数はデフォルトで`OFF`です。</li><li> TiDB クラスターを v4.0.0 以降から v5.4.0 以降にアップグレードする場合、この変数はアップグレード前と同じままです。</li><li> v5.4.0 以降の新しく作成された TiDB クラスターの場合、この変数はデフォルトで`ON`です。</li></ul>                                                                     |
| [`tidb_store_limit`](/system-variables.md#tidb_store_limit-new-in-v304-and-v40)                     | 修正済み   | v5.4.0 より前では、この変数はインスタンス レベルでグローバルに構成できます。 v5.4.0 以降、この変数はグローバル構成のみをサポートします。                                                                                                                                                                                                                                                              |

### コンフィグレーションファイルのパラメーター {#configuration-file-parameters}

| コンフィグレーションファイル  | コンフィグレーション                                                                                                      | タイプを変更 | 説明                                                                                                                                                                                                                                                                                                                                       |
| :-------------- | :-------------------------------------------------------------------------------------------------------------- | :----- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB            | [`stats-load-concurrency`](/tidb-configuration-file.md#stats-load-concurrency-new-in-v540)                      | 新規追加   | TiDB 同期ロード統計機能が同時に処理できる列の最大数を制御します。デフォルト値は`5`です。                                                                                                                                                                                                                                                                                         |
| TiDB            | [`stats-load-queue-size`](/tidb-configuration-file.md#stats-load-queue-size-new-in-v540)                        | 新規追加   | TiDB 同期ロード統計機能がキャッシュできる列リクエストの最大数を制御します。デフォルト値は`1000`です。                                                                                                                                                                                                                                                                                 |
| TiKV            | [`snap-generator-pool-size`](/tikv-configuration-file.md#snap-generator-pool-size-new-in-v540)                  | 新規追加   | `snap-generator`スレッド プールのサイズ。デフォルト値は`2`です。                                                                                                                                                                                                                                                                                               |
| TiKV            | `log.file.max-size` 、 `log.file.max-days` 、 `log.file.max-backups`                                              | 新規追加   | 詳細については、 [TiKVコンフィグレーションファイル - `log.file`](/tikv-configuration-file.md#logfile-new-in-v540)を参照してください。                                                                                                                                                                                                                                    |
| TiKV            | `raft-engine`                                                                                                   | 新規追加   | `enable` 、 `dir` 、 `batch-compression-threshold` 、 `bytes-per-sync` 、 `target-file-size` 、 `purge-threshold` 、 `recovery-mode` 、 `recovery-read-block-size` 、 `recovery-read-block-size` 、および`recovery-threads`が含まれます。詳しくは[TiKVコンフィグレーションファイル - `raft-engine`](/tikv-configuration-file.md#raft-engine)をご覧ください。                          |
| TiKV            | [`backup.enable-auto-tune`](/tikv-configuration-file.md#enable-auto-tune-new-in-v540)                           | 新規追加   | v5.3.0 では、デフォルト値は`false`です。 v5.4.0 以降、デフォルト値は`true`に変更されました。このパラメータは、クラスタ リソースの使用率が高い場合に、バックアップ タスクで使用されるリソースを制限してクラスタへの影響を軽減するかどうかを制御します。デフォルトの構成では、バックアップ タスクの速度が遅くなる場合があります。                                                                                                                                                          |
| TiKV            | `log-level` 、 `log-format` 、 `log-file` 、 `log-rotation-size`                                                   | 修正済み   | TiKV ログ パラメータの名前は、TiDB ログ パラメータと一致する名前 ( `log.level` 、 `log.format` 、 `log.file.filename` 、および`log.enable-timestamp`に置き換えられます。古いパラメータのみを設定し、それらの値がデフォルト以外の値に設定されている場合、古いパラメータは新しいパラメータと互換性があります。古いパラメータと新しいパラメータの両方が設定されている場合、新しいパラメータが有効になります。詳細については、 [TiKVコンフィグレーションファイル - ログ](/tikv-configuration-file.md#log-new-in-v540)を参照してください。 |
| TiKV            | `log-rotation-timespan`                                                                                         | 削除しました | ログ ローテーション間の期間。この期間が経過すると、ログ ファイルがローテーションされます。つまり、現在のログ ファイルのファイル名にタイムスタンプが追加され、新しいログ ファイルが作成されます。                                                                                                                                                                                                                                       |
| TiKV            | `allow-remove-leader`                                                                                           | 削除しました | メインスイッチの削除を許可するかどうかを決定します。                                                                                                                                                                                                                                                                                                               |
| TiKV            | `raft-msg-flush-interval`                                                                                       | 削除しました | Raftメッセージがバッチで送信される間隔を決定します。 Raftメッセージは、この構成項目で指定された間隔ごとにバッチで送信されます。                                                                                                                                                                                                                                                                     |
| PD              | [`log.level`](/pd-configuration-file.md#level)                                                                  | 修正済み   | デフォルト値は「INFO」から「info」に変更され、大文字と小文字が区別されないことが保証されています。                                                                                                                                                                                                                                                                                    |
| TiFlash         | [`profile.default.enable_elastic_threadpool`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file) | 新規追加   | エラスティック スレッド プール機能を有効にするか無効にするかを決定します。この構成項目を有効にすると、同時実行性の高いシナリオでTiFlash のCPU 使用率を大幅に改善できます。デフォルト値は`false`です。                                                                                                                                                                                                                            |
| TiFlash         | [`storage.format_version`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                    | 新規追加   | DTFile のバージョンを指定します。デフォルト値は`2`で、ハッシュがデータ ファイルに埋め込まれます。値を`3`に設定することもできます。 `3`の場合、データ ファイルにはメタデータとトークン データのチェックサムが含まれ、複数のハッシュ アルゴリズムがサポートされます。                                                                                                                                                                                             |
| TiFlash         | [`logger.count`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                              | 修正済み   | デフォルト値は`10`に変更されます。                                                                                                                                                                                                                                                                                                                      |
| TiFlash         | [`status.metrics_port`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                       | 修正済み   | デフォルト値は`8234`に変更されます。                                                                                                                                                                                                                                                                                                                    |
| TiFlash         | [`raftstore.apply-pool-size`](/tiflash/tiflash-configuration.md#configure-the-tiflash-learnertoml-file)         | 新規追加   | Raftデータをstorageにフラッシュするプール内のスレッドの許容数。デフォルト値は`4`です。                                                                                                                                                                                                                                                                                       |
| TiFlash         | [`raftstore.store-pool-size`](/tiflash/tiflash-configuration.md#configure-the-tiflash-learnertoml-file)         | 新規追加   | Raftstoreスレッド プールのサイズである、 Raftを処理するスレッドの許容数。デフォルト値は`4`です。                                                                                                                                                                                                                                                                                |
| TiDB データ移行 (DM) | [`collation_compatible`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)         | 新規追加   | `CREATE` SQL ステートメントで既定の照合順序を同期するモード。値のオプションは、&quot;loose&quot; (デフォルト) と &quot;strict&quot; です。                                                                                                                                                                                                                                         |
| TiCDC           | `max-message-bytes`                                                                                             | 修正済み   | Kafka シンクのデフォルト値`max-message-bytes` `104857601` (10MB) に変更します。                                                                                                                                                                                                                                                                           |
| TiCDC           | `partition-num`                                                                                                 | 修正済み   | Kafka Sink のデフォルト値`partition-num`を`4`から`3`に変更します。 TiCDC がメッセージを Kafaka パーティションにより均等に送信するようにします。                                                                                                                                                                                                                                          |
| TiDB Lightning  | `meta-schema-name`                                                                                              | 修正済み   | ターゲット TiDB 内のメタデータのスキーマ名を指定します。 v5.4.0 以降、このスキーマは[並行輸入](/tidb-lightning/tidb-lightning-distributed-import.md)有効にした場合にのみ作成されます (対応するパラメーターは`tikv-importer.incremental-import = true`です)。                                                                                                                                                  |
| TiDB Lightning  | `task-info-schema-name`                                                                                         | 新規追加   | TiDB Lightning が競合を検出したときに、複製されたデータが保存されるデータベースの名前を指定します。デフォルトの値は「lightning_task_info」です。このパラメータは、「重複解決」機能を有効にしている場合にのみ指定してください。                                                                                                                                                                                                         |
| TiDB Lightning  | `incremental-import`                                                                                            | 新規追加   | データが既に存在するテーブルへのデータのインポートを許可するかどうかを決定します。デフォルト値は`false`です。                                                                                                                                                                                                                                                                               |

### その他 {#others}

-   TiDB と PD の間にインターフェースが追加されます。 `information_schema.TIDB_HOT_REGIONS_HISTORY`システム テーブルを使用する場合、TiDB は対応するバージョンの PD を使用する必要があります。
-   TiDB サーバー、PD サーバー、および TiKV サーバーは、ログ関連のパラメーターに統一された命名方法を使用して開始し、ログ名、出力形式、およびローテーションと有効期限のルールを管理します。詳細については、 [TiKV 構成ファイル - ログ](/tikv-configuration-file.md#log-new-in-v540)を参照してください。
-   v5.4.0 以降、プラン キャッシュを介してキャッシュされた実行プランの SQL バインディングを作成すると、バインディングは、対応するクエリに対して既にキャッシュされているプランを無効にします。新しいバインディングは、v5.4.0 より前にキャッシュされた実行プランには影響しません。
-   v5.3 以前のバージョンでは、 [TiDB データ移行 (DM)](https://docs.pingcap.com/tidb-data-migration/v5.3/)ドキュメントが TiDB ドキュメントから独立しています。 v5.4 以降、DM ドキュメントは同じバージョンの TiDB ドキュメントに統合されています。 DMドキュメンテーションサイトにアクセスしなくても、 [DM ドキュメント](/dm/dm-overview.md)直接読むことができます。
-   ポイントインタイム リカバリ (PITR) の実験的機能を cdclog と共に削除します。 v5.4.0 以降、cdclog ベースの PITR と cdclog はサポートされなくなりました。
-   システム変数を「DEFAULT」に設定する動作をより MySQL 互換にする[#29680](https://github.com/pingcap/tidb/pull/29680)
-   システム変数`lc_time_names`を読み取り専用[#30084](https://github.com/pingcap/tidb/pull/30084)設定します
-   `tidb_store_limit`のスコープを INSTANCE または GLOBAL から GLOBAL [#30756](https://github.com/pingcap/tidb/pull/30756)に設定します
-   列にゼロが含まれる場合、整数型の列を時間型の列に変換することを禁止します[#25728](https://github.com/pingcap/tidb/pull/25728)
-   浮動小数点値[#30148](https://github.com/pingcap/tidb/pull/30148)を挿入するときに、 `Inf`または`NAN`値に対してエラーが報告されない問題を修正します。
-   自動 ID が範囲外の場合に`REPLACE`ステートメントが他の行を誤って変更する問題を修正します[#30301](https://github.com/pingcap/tidb/pull/30301)

## 新機能 {#new-features}

### SQL {#sql}

-   **TiDB は v5.4.0 以降、GBK 文字セットをサポートしています**

    v5.4.0 より前の TiDB は、 `ascii` 、 `binary` 、 `latin1` 、 `utf8` 、および`utf8mb4`文字セットをサポートしています。

    中国語ユーザーのサポートを強化するために、TiDB は v5.4.0 以降、GBK 文字セットをサポートしています。初めて TiDB クラスターを初期化するときに TiDB 構成ファイルで[`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap)オプションを有効にすると、TiDB GBK 文字セットは`gbk_bin`と`gbk_chinese_ci`両方の照合をサポートします。

    GBK 文字セットを使用する場合は、互換性の制限に注意する必要があります。詳細については、 [文字セットと照合 - GBK](/character-set-gbk.md)を参照してください。

### Security {#security}

-   **TiSpark はユーザー認証と承認をサポートします**

    TiSpark 2.5.0 以降、TiSpark はデータベース ユーザー認証と、データベースまたはテーブル レベルでの読み取り/書き込み承認の両方をサポートしています。この機能を有効にすると、企業がドローなどの不正なバッチ タスクを実行してデータを取得することを防止できるため、オンライン クラスターの安定性とデータ セキュリティが向上します。

    この機能はデフォルトで無効になっています。有効にすると、TiSpark を介して操作しているユーザーが必要なアクセス許可を持っていない場合、ユーザーは TiSpark から例外を受け取ります。

    [ユーザー文書](/tispark-overview.md#security)

-   **TiUP はroot ユーザーの初期パスワードの生成をサポートします**

    クラスターを開始するためのコマンドに`--init`パラメーターが導入されました。このパラメーターを使用すると、 TiUPを使用してデプロイされた TiDB クラスターで、 TiUP はデータベース ルート ユーザーの強力な初期パスワードを生成します。これにより、空のパスワードで root ユーザーを使用する際のセキュリティ リスクが回避され、データベースのセキュリティが確保されます。

    [ユーザー文書](/production-deployment-using-tiup.md#step-7-start-a-tidb-cluster)

### パフォーマンス {#performance}

-   **列型storageエンジンTiFlashとコンピューティング エンジン MPP の安定性とパフォーマンスを継続的に改善します。**

    -   より多くの関数をMPP エンジンにプッシュすることをサポートします。

        -   文字列関数: `LPAD()` 、 `RPAD()` 、 `STRCMP()`
        -   日付関数: `ADDDATE(string, real)` 、 `DATE_ADD(string, real)` 、 `DATE_SUB(string, real)` 、 `SUBDATE(string, real)` 、 `QUARTER()`

    -   リソース使用率を改善するためのエラスティック スレッド プール機能の導入 (実験的)

    -   TiKV からデータをレプリケートする際に、行ベースのstorage形式から列ベースのstorage形式にデータを変換する効率が向上し、データ レプリケーションの全体的なパフォーマンスが 50% 向上します。

    -   一部の構成項目のデフォルト値を調整して、 TiFlash のパフォーマンスと安定性を向上させます。 HTAP ハイブリッド ロードでは、1 つのテーブルに対する単純なクエリのパフォーマンスが最大 20% 向上します。

    ユーザー文書: [サポートされているプッシュダウン計算](/tiflash/tiflash-supported-pushdown-calculations.md) 、 [tiflash.toml ファイルを構成する](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)

-   **セッション変数を使用して、指定された時間範囲内の履歴データを読み取ります**

    TiDB は、 Raftコンセンサス アルゴリズムに基づくマルチレプリカ分散データベースです。同時実行性とスループットの高いアプリケーション シナリオに直面した場合、TiDB はフォロワー レプリカを介して読み取りパフォーマンスをスケールアウトし、読み取り要求と書き込み要求を分離できます。

    さまざまなアプリケーション シナリオに対して、TiDB はフォロワー読み取りの 2 つのモードを提供します。強整合性読み取りと弱整合性履歴読み取りです。強力な一貫性のある読み取りモードは、リアルタイム データを必要とするアプリケーション シナリオに適しています。ただし、このモードでは、リーダーとフォロワー間のデータ レプリケーションのレイテンシーとスループットの低下により、特に地理的に分散された展開の場合、読み取り要求の待機レイテンシーが長くなる可能性があります。

    リアルタイム データの要件がそれほど厳しくないアプリケーション シナリオでは、履歴読み取りモードをお勧めします。このモードでは、レイテンシーが短縮され、スループットが向上します。 TiDB は現在、次の方法による履歴データの読み取りをサポートしています。SQL ステートメントを使用して過去の時点からデータを読み取るか、過去の時点に基づいて読み取り専用トランザクションを開始します。どちらの方法も、特定の時点または指定された時間範囲内の履歴データの読み取りをサポートしています。詳細については、 [`AS OF TIMESTAMP`句を使用した履歴データの読み取り](/as-of-timestamp.md)を参照してください。

    v5.4.0 以降、TiDB は、セッション変数を介して指定された時間範囲内の履歴データの読み取りをサポートすることにより、履歴読み取りモードの使いやすさを向上させます。このモードは、準リアルタイムのシナリオで低レイテンシ、高スループットの読み取り要求を処理します。変数は次のように設定できます。

    ```sql
    set @@tidb_replica_read=leader_and_follower
    set @@tidb_read_staleness="-5"
    ```

    この設定により、TiDB は最も近いリーダーまたはフォロワー ノードを選択し、5 秒以内に最新の履歴データを読み取ることができます。

    [ユーザー文書](/tidb-read-staleness.md)

-   **インデックス マージの GA**

    Index Merge は、SQL 最適化の実験的機能として TiDB v4.0 に導入されました。この方法は、クエリで複数のデータ列のスキャンが必要な場合に条件フィルタリングを大幅に高速化します。例として、次のクエリを取り上げます。 `WHERE`ステートメントで、 `OR`で接続されたフィルター条件が列*key1*および<em>key2</em>にそれぞれのインデックスを持っている場合、インデックス マージ機能はそれぞれのインデックスを同時にフィルター処理し、クエリ結果をマージして、マージされた結果を返します。

    ```sql
    SELECT * FROM table WHERE key1 <= 100 OR key2 = 200;
    ```

    TiDB v4.0 より前では、テーブルに対するクエリは、一度にフィルタリングするために 1 つのインデックスのみを使用することをサポートしていました。データの複数の列に対してクエリを実行する場合は、インデックス マージを有効にして、個々の列のインデックスを使用して正確なクエリ結果を短時間で取得できます。インデックス マージは、不要な全テーブル スキャンを回避し、多数の複合インデックスを確立する必要がありません。

    v5.4.0 では、Index Merge が GA になります。ただし、次の制限に注意する必要があります。

    -   Index Merge は、論理和正規形 (X <sub>1</sub> ⋁ X <sub>2</sub> ⋁ …X <sub>n</sub> ) のみをサポートします。つまり、この機能は、 `WHERE`句のフィルタリング条件が`OR`で接続されている場合にのみ機能します。

    -   v5.4.0 以降の新しくデプロイされた TiDB クラスターの場合、この機能はデフォルトで有効になっています。以前のバージョンからアップグレードされた v5.4.0 以降の TiDB クラスターの場合、この機能はアップグレード前の設定を継承し、必要に応じて設定を変更できます (v4.0 より前の TiDB クラスターの場合、この機能は存在せず、デフォルトで無効になっています)。 .

    [ユーザー文書](/explain-index-merge.md)

-   **Raft Engineのサポート (実験的)**

    TiKV のログstorageエンジンとして[Raft Engine](https://github.com/tikv/raft-engine)を使用することをサポートします。 RocksDB と比較して、 Raft Engine はTiKV I/O 書き込みトラフィックを最大 40% 削減し、CPU 使用率を 10% 削減し、フォアグラウンド スループットを約 5% 向上させ、特定の負荷の下でテールレイテンシーを 20% 削減できます。さらに、 Raft Engine はログのリサイクルの効率を改善し、極端な状況でのログの蓄積の問題を修正します。

    Raft Engine はまだ実験的機能であり、デフォルトでは無効になっています。 v5.4.0 のRaft Engineのデータ形式は、以前のバージョンと互換性がないことに注意してください。クラスターをアップグレードする前に、すべての TiKV ノードでRaft Engine が無効になっていることを確認する必要があります。 v5.4.0 以降のバージョンでのみRaft Engineを使用することをお勧めします。

    [ユーザー文書](/tikv-configuration-file.md#raft-engine)

-   **`PREDICATE COLUMNS`での統計収集のサポート (実験的)**

    ほとんどの場合、SQL ステートメントを実行するとき、オプティマイザーは一部の列 ( `WHERE` 、 `JOIN` 、 `ORDER BY` 、および`GROUP BY`ステートメントの列など) の統計のみを使用します。これらの使用済み列は`PREDICATE COLUMNS`と呼ばれます。

    v5.4.0 以降、システム変数[`tidb_enable_column_tracking`](/system-variables.md#tidb_enable_column_tracking-new-in-v540)の値を`ON`に設定して、TiDB が`PREDICATE COLUMNS`を収集できるようにすることができます。

    設定後、TiDB は 100 * [`stats-lease`](/tidb-configuration-file.md#stats-lease)ごとに`PREDICATE COLUMNS`情報を`mysql.column_stats_usage`システム テーブルに書き込みます。ビジネスのクエリ パターンが安定している場合は、 `ANALYZE TABLE TableName PREDICATE COLUMNS`構文を使用して`PREDICATE COLUMNS`列のみの統計を収集できます。これにより、統計収集のオーバーヘッドを大幅に削減できます。

    [ユーザー文書](/statistics.md#collect-statistics-on-some-columns)

-   **統計の同期読み込みをサポート (実験的)**

    v5.4.0 以降、TiDB は同期読み込み統計機能を導入しています。この機能はデフォルトで無効になっています。この機能を有効にすると、TiDB は、SQL ステートメントを実行するときに大規模な統計 (ヒストグラム、TopN、Count-Min Sketch 統計など) をメモリに同期的にロードできるため、SQL 最適化の統計の完全性が向上します。

    [ユーザー文書](/statistics.md#load-statistics)

### 安定性 {#stability}

-   **ANALYZE 構成の永続化をサポート**

    統計は、オプティマイザが実行計画を生成するときに参照する基本情報の一種です。統計の精度は、生成された実行計画が適切かどうかに直接影響します。統計の精度を確保するために、さまざまなテーブル、パーティション、およびインデックスに対してさまざまなコレクション構成を設定する必要がある場合があります。

    v5.4.0 以降、TiDB は`ANALYZE`の構成の永続化をサポートしています。この機能を使用すると、既存の構成を将来の統計収集に簡単に再利用できます。

    `ANALYZE`構成永続化機能は、デフォルトで有効になっています (システム変数`tidb_analyze_version`デフォルトで`2`で、 [`tidb_persist_analyze_options`](/system-variables.md#tidb_persist_analyze_options-new-in-v540)は`ON`です)。この機能を使用して、ステートメントを手動で実行するときに、 `ANALYZE`ステートメントで指定された持続性構成を記録できます。記録されると、次に TiDB が自動的に統計を更新するか、これらの構成を指定せずに手動で統計を収集するときに、TiDB は記録された構成に従って統計を収集します。

    [ユーザー文書](/statistics.md#persist-analyze-configurations)

### 高可用性と災害復旧 {#high-availability-and-disaster-recovery}

-   **クラスターに対するバックアップ タスクの影響を軽減する**

    バックアップと復元 (BR) では、自動調整機能が導入されています (既定で有効になっています)。この機能は、クラスター リソースの使用状況を監視し、バックアップ タスクで使用されるスレッドの数を調整することで、クラスターに対するバックアップ タスクの影響を軽減できます。場合によっては、バックアップ用のクラスター ハードウェア リソースを増やして自動調整機能を有効にすると、クラスターに対するバックアップ タスクの影響を 10% 以下に制限できます。

    [ユーザー文書](/br/br-auto-tune.md)

-   **バックアップのターゲットstorageとして Azure Blob Storage をサポートする**

    バックアップと復元 (BR) は、Azure Blob Storage をリモート バックアップstorageとしてサポートします。 TiDB を Azure クラウドにデプロイすると、クラスター データを Azure Blob Storage サービスにバックアップできるようになりました。

    [ユーザー文書](/br/backup-and-restore-storages.md)

### データ移行 {#data-migration}

-   **TiDB Lightning は、データを含むテーブルへのデータのインポートを許可するかどうかを決定する新しい機能を導入します**

    TiDB Lightning は構成項目`incremental-import`を導入します。データを含むテーブルへのデータのインポートを許可するかどうかを決定します。デフォルト値は`false`です。並行インポート モードを使用する場合は、構成を`true`に設定する必要があります。

    [ユーザー文書](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)

-   **TiDB Lightningに並行インポート用のメタ情報を格納するスキーマ名を導入**

    TiDB Lightning、 `meta-schema-name`構成アイテムが導入されています。並行インポート モードでは、このパラメーターは、ターゲット クラスター内の各TiDB Lightningインスタンスのメタ情報を格納するスキーマ名を指定します。デフォルトの値は「lightning_metadata」です。このパラメータに設定する値は、同じ並列インポートに参加するTiDB Lightningインスタンスごとに同じにする必要があります。そうしないと、インポートされたデータの正確性が保証されません。

    [ユーザー文書](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)

-   **TiDB Lightning が重複解決を導入**

    ローカル バックエンド モードでは、 TiDB Lightning は、データのインポートが完了する前に重複データを出力し、その重複データをデータベースから削除します。インポートの完了後に重複データを解決し、アプリケーション ルールに従って挿入する適切なデータを選択できます。後続の増分データ移行フェーズで発生する重複データによって引き起こされるデータの不整合を回避するために、重複データに基づいてアップストリーム データ ソースをクリーンアップすることをお勧めします。

    [ユーザー文書](/tidb-lightning/tidb-lightning-error-resolution.md)

-   **TiDB Data Migration (DM) でのリレー ログの使用を最適化する**

    -   `source`構成の`enable-relay`スイッチを回復します。

    -   `start-relay`および`stop-relay`コマンドを使用して、リレー ログの動的な有効化と無効化をサポートします。

    -   リレーログのステータスを`source`にバインドします。 `source`任意の DM-worker に移行された後、有効または無効の元のステータスを保持します。

    -   中継ログのstorageパスを DM-worker 設定ファイルに移動します。

    [ユーザー文書](/dm/relay-log.md)

-   **DMでの<a href="/character-set-and-collation.md">照合順序</a>処理を最適化**

    `collation_compatible`構成アイテムを追加します。値のオプションは`loose` (デフォルト) と`strict`です。

    -   アプリケーションに照合順序に関する厳密な要件がなく、クエリ結果の照合順序がアップストリームとダウンストリームで異なる可能性がある場合は、デフォルトの`loose`モードを使用してエラーの報告を回避できます。
    -   アプリケーションが照合順序に対して厳密な要件を持ち、上流と下流の間で照合順序が一貫している必要がある場合は、 `strict`モードを使用できます。ただし、ダウンストリームがアップストリームのデフォルトの照合順序をサポートしていない場合、データ レプリケーションでエラーが報告されることがあります。

    [ユーザー文書](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)

-   **DM の`transfer source`最適化して、レプリケーション タスクのスムーズな実行をサポート**

    DM-worker ノードの負荷が不均衡な場合、 `transfer source`コマンドを使用して、 `source`の構成を別の負荷に手動で転送できます。最適化後、 `transfer source`コマンドは手動操作を簡素化します。 DMが内部で他の操作を完了するため、関連するすべてのタスクを一時停止する代わりに、ソースをスムーズに転送できます。

-   **DM OpenAPI の一般提供開始 (GA)**

    DM は、データ ソースの追加やタスクの管理など、API を介して日常的な管理をサポートします。 v5.4.0 では、DM OpenAPI が GA になります。

    [ユーザー文書](/dm/dm-open-api.md)

### 診断効率 {#diagnostic-efficiency}

-   **Top SQL (実験的機能)**

    ソースを消費するクエリを簡単に見つけられるように、新しい実験的機能であるTop SQL (既定では無効) が導入されました。

    [ユーザー文書](/dashboard/top-sql.md)

### TiDB データ共有サブスクリプション {#tidb-data-share-subscription}

-   **クラスターに対する TiCDC の影響を最適化する**

    TiCDC を使用すると、TiDB クラスターのパフォーマンスへの影響が大幅に軽減されます。テスト環境では、TiDB に対する TiCDC のパフォーマンスへの影響を 5% 未満に減らすことができます。

### 展開とメンテナンス {#deployment-and-maintenance}

-   **継続的なプロファイリングの強化 (実験的)**

    -   サポートされるコンポーネントの増加: TiDB、PD、および TiKV に加えて、TiDB v5.4.0 はTiFlashの CPU プロファイリングもサポートします。

    -   より多くの形式のプロファイリング表示: フレーム チャートでの CPU プロファイリングとゴルーチンの結果の表示をサポートします。

    -   サポートされる展開環境の増加: 継続的なプロファイリングは、 TiDB Operatorを使用して展開されたクラスターにも使用できます。

    継続的なプロファイリングはデフォルトで無効になっており、TiDB ダッシュボードで有効にすることができます。

    継続的プロファイリングは、v1.9.0 以降のTiUPまたは v1.3.0 以降のTiDB Operatorを使用してデプロイまたはアップグレードされたクラスターに適用されます。

    [ユーザー文書](/dashboard/continuous-profiling.md)

## 改良点 {#improvements}

-   TiDB

    -   `ADMIN {SESSION | INSTANCE | GLOBAL} PLAN_CACHE`構文をサポートして、キャッシュされたクエリ プランをクリアします[#30370](https://github.com/pingcap/tidb/pull/30370)

-   TiKV

    -   コプロセッサーは、ストリームのような方法で要求を処理するページング API をサポートします[#11448](https://github.com/tikv/tikv/issues/11448)
    -   `read-through-lock`サポートして、読み取り操作が 2 次ロックの解決を待つ必要がないようにする[#11402](https://github.com/tikv/tikv/issues/11402)
    -   ディスク領域の枯渇によるpanicを回避するために、ディスク保護メカニズムを追加します[#10537](https://github.com/tikv/tikv/issues/10537)
    -   ログのアーカイブとローテーションのサポート[#11651](https://github.com/tikv/tikv/issues/11651)
    -   Raftクライアントによるシステム コールを減らし、CPU 効率を高める[#11309](https://github.com/tikv/tikv/issues/11309)
    -   コプロセッサーは部分文字列の TiKV [#11495](https://github.com/tikv/tikv/issues/11495)へのプッシュダウンをサポート
    -   Read Committed 分離レベル[#11485](https://github.com/tikv/tikv/issues/11485)で読み取りロックをスキップすることにより、スキャンのパフォーマンスを向上させます。
    -   バックアップ操作で使用されるデフォルトのスレッド プール サイズを減らし、負荷が高い場合にスレッド プールの使用を制限する[#11000](https://github.com/tikv/tikv/issues/11000)
    -   Apply スレッド プールと Store スレッド プールのサイズを動的に調整するサポート[#11159](https://github.com/tikv/tikv/issues/11159)
    -   `snap-generator`スレッド プール[#11247](https://github.com/tikv/tikv/issues/11247)のサイズの構成をサポート
    -   読み取りと書き込みが頻繁に行われるファイルが多数ある場合に発生するグローバル ロック競合の問題を最適化します[#250](https://github.com/tikv/rocksdb/pull/250)

-   PD

    -   デフォルトで過去のホットスポット情報を記録する[#25281](https://github.com/pingcap/tidb/issues/25281)
    -   HTTPコンポーネントの署名を追加して、要求元を識別します[#4490](https://github.com/tikv/pd/issues/4490)
    -   TiDB ダッシュボードを v2021.12.31 に更新する[#4257](https://github.com/tikv/pd/issues/4257)

-   TiFlash

    -   現地オペレーターのコミュニケーションを最適化
    -   gRPC の非一時的なスレッド数を増やして、スレッドの頻繁な作成または破棄を回避します

-   ツール

    -   バックアップと復元 (BR)

        -   BR が暗号化されたバックアップを実行するときのキーの有効性チェックを追加します[#29794](https://github.com/pingcap/tidb/issues/29794)

    -   TiCDC

        -   「EventFeed retry rate limited」ログのカウントを減らします[#4006](https://github.com/pingcap/tiflow/issues/4006)
        -   多数のテーブルをレプリケートする場合のレプリケーションレイテンシーを削減する[#3900](https://github.com/pingcap/tiflow/issues/3900)
        -   TiKV ストアがダウンしたときに KV クライアントが回復するまでの時間を短縮する[#3191](https://github.com/pingcap/tiflow/issues/3191)

    -   TiDB データ移行 (DM)

        -   リレー有効時のCPU使用率を下げる[#2214](https://github.com/pingcap/dm/issues/2214)

    -   TiDB Lightning

        -   デフォルトで楽観的トランザクションを使用してデータを書き込み、TiDB バックエンド モード[#30953](https://github.com/pingcap/tidb/pull/30953)でのパフォーマンスを向上させます

    -   Dumpling

        -   Dumpling がデータベース バージョン[#29500](https://github.com/pingcap/tidb/pull/29500)をチェックするときの互換性を改善
        -   `CREATE DATABASE`と`CREATE TABLE` [#3420](https://github.com/pingcap/tiflow/issues/3420)をダンプするときにデフォルトの照合順序を追加します

## バグの修正 {#bug-fixes}

-   TiDB

    -   クラスターを v4.x から v5.x にアップグレードするときに発生する`tidb_analyze_version`値の変更の問題を修正します[#25422](https://github.com/pingcap/tidb/issues/25422)
    -   サブクエリで異なる照合順序を使用した場合に発生する間違った結果の問題を修正します[#30748](https://github.com/pingcap/tidb/issues/30748)
    -   TiDB の`concat(ifnull(time(3))`の結果が MySQL [#29498](https://github.com/pingcap/tidb/issues/29498)の結果と異なる問題を修正
    -   楽観的トランザクション モード[#30410](https://github.com/pingcap/tidb/issues/30410)での潜在的なデータ インデックスの不整合の問題を修正します。
    -   TiKV [#30200](https://github.com/pingcap/tidb/issues/30200)に式をプッシュダウンできない場合、IndexMerge のクエリ実行プランが間違っている問題を修正
    -   列の型を同時に変更すると、スキーマとデータの間で不整合が発生する問題を修正します[#31048](https://github.com/pingcap/tidb/issues/31048)
    -   サブクエリがあるとIndexMergeのクエリ結果がおかしくなる問題を修正[#30913](https://github.com/pingcap/tidb/issues/30913)
    -   クライアント[#30896](https://github.com/pingcap/tidb/issues/30896)で FetchSize の設定が大きすぎる場合に発生するpanicの問題を修正します。
    -   LEFT JOIN が誤って INNER JOIN [#20510](https://github.com/pingcap/tidb/issues/20510)に変換される可能性がある問題を修正
    -   `CASE-WHEN`式と照合順序を併用するとpanicが発生することがある問題を修正[#30245](https://github.com/pingcap/tidb/issues/30245)
    -   `IN`値にバイナリ定数[#31261](https://github.com/pingcap/tidb/issues/31261)含まれている場合に発生する間違ったクエリ結果の問題を修正します。
    -   CTE にサブクエリがある場合に発生する間違ったクエリ結果の問題を修正します[#31255](https://github.com/pingcap/tidb/issues/31255)
    -   `INSERT ... SELECT ... ON DUPLICATE KEY UPDATE`ステートメントを実行するとpanic[#28078](https://github.com/pingcap/tidb/issues/28078)が発生する問題を修正します。
    -   INDEX HASH JOIN が`send on closed channel`エラー[#31129](https://github.com/pingcap/tidb/issues/31129)を返す問題を修正

-   TiKV

    -   MVCC 削除レコードが GC でクリアされない問題を修正します[#11217](https://github.com/tikv/tikv/issues/11217)
    -   悲観的トランザクション モードでプリライト リクエストを再試行すると、まれにデータの不整合が発生する可能性がある問題を修正します[#11187](https://github.com/tikv/tikv/issues/11187)
    -   GC スキャンがメモリオーバーフローを引き起こす問題を修正します[#11410](https://github.com/tikv/tikv/issues/11410)
    -   ディスク容量がいっぱいになると、RocksDB のフラッシュまたは圧縮によってpanicが発生する問題を修正します[#11224](https://github.com/tikv/tikv/issues/11224)

-   PD

    -   リージョン統計が`flow-round-by-digit` [#4295](https://github.com/tikv/pd/issues/4295)の影響を受けない問題を修正
    -   ターゲットストアがダウンしているため、スケジューリングオペレーターが高速に失敗できない問題を修正します[#3353](https://github.com/tikv/pd/issues/3353)
    -   オフライン ストアのリージョンをマージできない問題を修正します[#4119](https://github.com/tikv/pd/issues/4119)
    -   コールド ホットスポット データがホットスポット統計から削除できない問題を修正します[#4390](https://github.com/tikv/pd/issues/4390)

-   TiFlash

    -   MPP クエリが停止したときにTiFlash がpanicになる問題を修正
    -   `where <string>`句を含むクエリが間違った結果を返す問題を修正
    -   整数主キーの列タイプをより大きな範囲に設定するときに発生する可能性のあるデータの不整合の問題を修正します
    -   入力時刻が 1970-01-01 00:00:01 UTC より前の場合、 `unix_timestamp`の動作が TiDB や MySQL の動作と一致しない問題を修正
    -   再起動後にTiFlash が`EstablishMPPConnection`エラーを返すことがある問題を修正
    -   `CastStringAsDecimal`動作がTiFlashと TiDB/TiKV で一致しない問題を修正
    -   クエリ結果に`DB::Exception: Encode type of coprocessor response is not CHBlock`のエラーが返される問題を修正
    -   `castStringAsReal`動作がTiFlashと TiDB/TiKV で一致しない問題を修正
    -   TiFlashの`date_add_string_xxx`関数の返される結果が MySQL の結果と一致しない問題を修正します。

-   ツール

    -   バックアップと復元 (BR)

        -   復元操作の完了後にリージョンの分布が不均一になる可能性がある潜在的な問題を修正します[#30425](https://github.com/pingcap/tidb/issues/30425)
        -   バックアップstorageとして`minio`使用する場合、エンドポイントに`'/'`指定できない問題を修正[#30104](https://github.com/pingcap/tidb/issues/30104)
        -   システム テーブルを同時にバックアップすると、テーブル名が更新されないため、システム テーブルを復元できない問題を修正します[#29710](https://github.com/pingcap/tidb/issues/29710)

    -   TiCDC

        -   `min.insync.replicas`が`replication-factor` [#3994](https://github.com/pingcap/tiflow/issues/3994)より小さい場合にレプリケーションが実行できない問題を修正
        -   `cached region`モニタリング指標がマイナス[#4300](https://github.com/pingcap/tiflow/issues/4300)になる問題を修正
        -   `mq sink write row`監視データがない問題を修正[#3431](https://github.com/pingcap/tiflow/issues/3431)
        -   `sql mode` [#3810](https://github.com/pingcap/tiflow/issues/3810)の互換性の問題を修正
        -   レプリケーション タスクが削除されたときに発生する潜在的なpanicの問題を修正します[#3128](https://github.com/pingcap/tiflow/issues/3128)
        -   デフォルトの列値[#3929](https://github.com/pingcap/tiflow/issues/3929)を出力するときに発生するpanicとデータの不整合の問題を修正します。
        -   デフォルト値をレプリケートできない問題を修正[#3793](https://github.com/pingcap/tiflow/issues/3793)
        -   デッドロックが原因でレプリケーション タスクがスタックする潜在的な問題を修正します[#4055](https://github.com/pingcap/tiflow/issues/4055)
        -   ディスクが完全に書き込まれたときにログが出力されない問題を修正[#3362](https://github.com/pingcap/tiflow/issues/3362)
        -   DDL ステートメントの特殊なコメントによってレプリケーション タスクが停止する問題を修正します[#3755](https://github.com/pingcap/tiflow/issues/3755)
        -   RHEL リリース[#3584](https://github.com/pingcap/tiflow/issues/3584)でタイムゾーンの問題が原因でサービスを開始できない問題を修正
        -   不正確なチェックポイント[#3545](https://github.com/pingcap/tiflow/issues/3545)によって引き起こされる潜在的なデータ損失の問題を修正します。
        -   コンテナー環境での OOM の問題を修正する[#1798](https://github.com/pingcap/tiflow/issues/1798)
        -   `config.Metadata.Timeout` [#3352](https://github.com/pingcap/tiflow/issues/3352)の構成が正しくないために発生するレプリケーション停止の問題を修正します。

    -   TiDB データ移行 (DM)

        -   `CREATE VIEW`ステートメントがデータ レプリケーションを中断する問題を修正します[#4173](https://github.com/pingcap/tiflow/issues/4173)
        -   DDL ステートメントがスキップされた後にスキーマをリセットする必要がある問題を修正します[#4177](https://github.com/pingcap/tiflow/issues/4177)
        -   DDL ステートメントがスキップされた後、テーブル チェックポイントが時間内に更新されないという問題を修正します[#4184](https://github.com/pingcap/tiflow/issues/4184)
        -   TiDB バージョンとパーサー バージョン[#4298](https://github.com/pingcap/tiflow/issues/4298)の互換性の問題を修正
        -   ステータス[#4281](https://github.com/pingcap/tiflow/issues/4281)を照会した場合にのみ syncer メトリクスが更新される問題を修正します。

    -   TiDB Lightning

        -   TiDB Lightning が`mysql.tidb`テーブルへのアクセス権限を持っていない場合に発生する間違ったインポート結果の問題を修正[#31088](https://github.com/pingcap/tidb/issues/31088)
        -   TiDB Lightningの再起動時に一部のチェックがスキップされる問題を修正[#30772](https://github.com/pingcap/tidb/issues/30772)
        -   S3 パスが存在しない場合にTiDB Lightning がエラーを報告しない問題を修正します[#30674](https://github.com/pingcap/tidb/pull/30674)

    -   TiDBBinlog

        -   Drainer が`CREATE PLACEMENT POLICY`文[#1118](https://github.com/pingcap/tidb-binlog/issues/1118)と互換性がないために失敗する問題を修正
