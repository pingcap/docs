---
title: TiDB 5.4 Release Notes
summary: TiDB 5.4 では、GBK 文字セット、インデックス マージ、古いデータの読み取り、統計構成の永続化、および TiKV のログstorageエンジンとしてのRaft Engineの使用のサポートが導入されています。また、バックアップの影響が改善され、Azure Blobstorageがサポートされ、 TiFlashと MPP エンジンが強化されています。互換性の変更には、新しいシステム変数と構成ファイル パラメーターが含まれます。その他の改善点には、SQL、セキュリティ、パフォーマンス、安定性、高可用性、データ移行、診断効率、および展開が含まれます。バグ修正では、TiDB、TiKV、PD、 TiFlash、 BR、TiCDC、DM、 TiDB Lightning、および TiDB Binlogの問題が対処されています。
---

# TiDB 5.4 リリースノート {#tidb-5-4-release-notes}

発売日: 2022年2月15日

TiDB バージョン: 5.4.0

v5.4 の主な新機能または改善点は次のとおりです。

-   GBK文字セットをサポート
-   複数の列のインデックスのフィルタリング結果をマージするインデックスマージを使用したデータへのアクセスをサポートします。
-   セッション変数を使用した古いデータの読み取りをサポート
-   統計情報を収集するための設定の永続化をサポート
-   TiKV のログstorageエンジンとしてRaft Engine の使用をサポート (実験的)
-   クラスタへのバックアップの影響を最適化する
-   バックアップstorageとして Azure Blobstorageの使用をサポート
-   TiFlashとMPPエンジンの安定性とパフォーマンスを継続的に改善します
-   TiDB Lightningにスイッチを追加して、既存のテーブルにデータをインポートするかどうかを決定します。
-   継続的プロファイリング機能の最適化（実験的）
-   TiSparkはユーザーの識別と認証をサポートします

## 互換性の変更 {#compatibility-changes}

> **注記：**
>
> 以前の TiDB バージョンから v5.4.0 にアップグレードする場合、すべての中間バージョンの互換性変更ノートを知りたい場合は、該当するバージョンの[リリースノート](/releases/release-notes.md)を確認できます。

### システム変数 {#system-variables}

<table><thead><tr><th>変数名</th><th>タイプを変更</th><th>説明</th></tr></thead><tbody><tr><td><a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_enable_column_tracking-new-in-v540"><code>tidb_enable_column_tracking</code></a></td><td>新しく追加された</td><td>TiDB が<code>PREDICATE COLUMNS</code>収集できるようにするかどうかを制御します。デフォルト値は<code>OFF.</code></td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_enable_paging-new-in-v540"><code>tidb_enable_paging</code></a></td><td>新しく追加された</td><td><code>IndexLookUp</code>演算子でコプロセッサ要求を送信するためにページング方式を使用するかどうかを制御します。デフォルト値は<code>OFF</code>です。<br/> <code>IndexLookup</code>と<code>Limit</code>使用し、 <code>Limit</code> <code>IndexScan</code>にプッシュダウンできない読み取りクエリの場合、読み取りクエリのレイテンシーが高くなり、TiKV の<code>unified read pool</code>の CPU 使用率が高くなる可能性があります。このような場合、 <code>Limit</code>演算子は少量のデータ セットのみを必要とするため、 <code>tidb_enable_paging</code> <code>ON</code>に設定すると、TiDB が処理するデータが少なくなり、クエリのレイテンシーとリソース消費が削減されます。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_enable_top_sql-new-in-v540"><code>tidb_enable_top_sql</code></a></td><td>新しく追加された</td><td>Top SQL機能を有効にするかどうかを制御します。デフォルト値は<code>OFF</code>です。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_persist_analyze_options-new-in-v540"><code>tidb_persist_analyze_options</code></a></td><td>新しく追加された</td><td><a href="https://docs.pingcap.com/tidb/dev/statistics#persist-analyze-configurations">ANALYZE 構成の永続性</a>機能を有効にするかどうかを制御します。デフォルト値は<code>ON</code>です。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_read_staleness-new-in-v540"><code>tidb_read_staleness</code></a></td><td>新しく追加された</td><td>現在のセッションで読み取ることができる履歴データの範囲を制御します。デフォルト値は<code>0</code>です。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_regard_null_as_point-new-in-v540"><code>tidb_regard_null_as_point</code></a></td><td>新しく追加された</td><td>オプティマイザーがインデックス アクセスのプレフィックス条件として NULL 等価性を含むクエリ条件を使用できるかどうかを制御します。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_stats_load_sync_wait-new-in-v540"><code>tidb_stats_load_sync_wait</code></a></td><td>新しく追加された</td><td>統計の同期読み込み機能を有効にするかどうかを制御します。デフォルト値<code>0</code>は、機能が無効であり、統計が非同期に読み込まれることを意味します。この機能を有効にすると、この変数は、タイムアウト前に SQL 最適化が統計の同期読み込みを待機できる最大時間を制御します。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_stats_load_pseudo_timeout-new-in-v540"><code>tidb_stats_load_pseudo_timeout</code></a></td><td>新しく追加された</td><td>統計の同期ロードがタイムアウトに達したときに、SQL が失敗するか ( <code>OFF</code> )、疑似統計の使用にフォールバックするか ( <code>ON</code> ) を制御します。デフォルト値は<code>OFF</code>です。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_backoff_lock_fast"><code>tidb_backoff_lock_fast</code></a></td><td>修正済み</td><td>デフォルト値は<code>100</code>から<code>10</code>に変更されます。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_enable_index_merge-new-in-v40"><code>tidb_enable_index_merge</code></a></td><td>修正済み</td><td>デフォルト値が<code>OFF</code>から<code>ON</code>に変更されます。<ul><li> TiDB クラスターを v4.0.0 より前のバージョンから v5.4.0 以降にアップグレードする場合、この変数はデフォルトで<code>OFF</code>なります。</li><li> TiDB クラスターを v4.0.0 以降から v5.4.0 以降にアップグレードする場合、この変数はアップグレード前と同じままになります。</li><li> v5.4.0 以降で新しく作成された TiDB クラスターの場合、この変数はデフォルトで<code>ON</code>なります。</li></ul></td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_store_limit-new-in-v304-and-v40"><code>tidb_store_limit</code></a></td><td>修正済み</td><td>v5.4.0 より前では、この変数はインスタンス レベルとグローバルで設定できます。v5.4.0 以降では、この変数はグローバル設定のみをサポートします。</td></tr></tbody></table>

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル  | コンフィグレーション                                                                                                      | タイプを変更   | 説明                                                                                                                                                                                                                                                                                                                                   |
| :-------------- | :-------------------------------------------------------------------------------------------------------------- | :------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ティビ             | [`stats-load-concurrency`](/tidb-configuration-file.md#stats-load-concurrency-new-in-v540)                      | 新しく追加された | TiDB 同期ロード統計機能が同時に処理できる列の最大数を制御します。デフォルト値は`5`です。                                                                                                                                                                                                                                                                                     |
| ティビ             | [`stats-load-queue-size`](/tidb-configuration-file.md#stats-load-queue-size-new-in-v540)                        | 新しく追加された | TiDB 同期ロード統計機能がキャッシュできる列リクエストの最大数を制御します。デフォルト値は`1000`です。                                                                                                                                                                                                                                                                             |
| ティクヴ            | [`snap-generator-pool-size`](/tikv-configuration-file.md#snap-generator-pool-size-new-in-v540)                  | 新しく追加された | `snap-generator`スレッド プールのサイズ。デフォルト値は`2`です。                                                                                                                                                                                                                                                                                           |
| ティクヴ            | `log.file.max-size` `log.file.max-days` `log.file.max-backups`                                                  | 新しく追加された | 詳細は[TiKVコンフィグレーションファイル - `log.file`](/tikv-configuration-file.md#logfile-new-in-v540)参照。                                                                                                                                                                                                                                             |
| ティクヴ            | `raft-engine`                                                                                                   | 新しく追加された | `enable` `dir` `recovery-read-block-size`れ`recovery-read-block-size` 。詳細`recovery-threads` `batch-compression-threshold` `bytes-per-sync` [TiKVコンフィグレーションファイル - `raft-engine`](/tikv-configuration-file.md#raft-engine) `target-file-size` `recovery-mode` `purge-threshold`ください。                                                    |
| ティクヴ            | [`backup.enable-auto-tune`](/tikv-configuration-file.md#enable-auto-tune-new-in-v540)                           | 新しく追加された | v5.3.0 では、デフォルト値は`false`です。v5.4.0 以降では、デフォルト値は`true`に変更されています。このパラメータは、クラスター リソースの使用率が高い場合に、クラスターへの影響を軽減するために、バックアップ タスクで使用されるリソースを制限するかどうかを制御します。デフォルト構成では、バックアップ タスクの速度が低下する可能性があります。                                                                                                                                              |
| ティクヴ            | `log-level` `log-format` `log-file` `log-rotation-size`                                                         | 修正済み     | TiKV ログ パラメータの名前は、TiDB ログ パラメータと一致する名前 ( `log.level` 、 `log.format` 、 `log.file.filename` 、および`log.enable-timestamp`に置き換えられます。古いパラメータのみを設定し、その値をデフォルト以外の値に設定した場合、古いパラメータは新しいパラメータと互換性が保たれます。古いパラメータと新しいパラメータの両方が設定されている場合は、新しいパラメータが有効になります。詳細については、 [TiKVコンフィグレーションファイル - ログ](/tikv-configuration-file.md#log-new-in-v540)参照してください。 |
| ティクヴ            | `log-rotation-timespan`                                                                                         | 削除されました  | ログのローテーション間の期間。この期間が経過すると、ログ ファイルがローテーションされ、現在のログ ファイルのファイル名にタイムスタンプが追加され、新しいログ ファイルが作成されます。                                                                                                                                                                                                                                         |
| ティクヴ            | `allow-remove-leader`                                                                                           | 削除されました  | メインスイッチの削除を許可するかどうかを決定します。                                                                                                                                                                                                                                                                                                           |
| ティクヴ            | `raft-msg-flush-interval`                                                                                       | 削除されました  | Raftメッセージがバッチで送信される間隔を決定します。Raft メッセージは、この構成項目で指定された間隔ごとにバッチで送信されます。                                                                                                                                                                                                                                                                 |
| PD              | [`log.level`](/pd-configuration-file.md#level)                                                                  | 修正済み     | デフォルト値は「INFO」から「info」に変更され、大文字と小文字が区別されないことが保証されます。                                                                                                                                                                                                                                                                                  |
| TiFlash         | [`profile.default.enable_elastic_threadpool`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file) | 新しく追加された | エラスティック スレッド プール機能を有効にするか無効にするかを決定します。この構成項目を有効にすると、同時実行性の高いシナリオでTiFlash CPU 使用率が大幅に向上します。デフォルト値は`false`です。                                                                                                                                                                                                                          |
| TiFlash         | [`storage.format_version`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                    | 新しく追加された | DTFile のバージョンを指定します。デフォルト値は`2`で、ハッシュがデータ ファイルに埋め込まれます。値を`3`に設定することもできます。値が`3`の場合、データ ファイルにはメタデータとトークン データ チェックサムが含まれ、複数のハッシュ アルゴリズムがサポートされます。                                                                                                                                                                                        |
| TiFlash         | [`logger.count`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                              | 修正済み     | デフォルト値は`10`に変更されます。                                                                                                                                                                                                                                                                                                                  |
| TiFlash         | [`status.metrics_port`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                       | 修正済み     | デフォルト値は`8234`に変更されます。                                                                                                                                                                                                                                                                                                                |
| TiFlash         | [`raftstore.apply-pool-size`](/tiflash/tiflash-configuration.md#configure-the-tiflash-learnertoml-file)         | 新しく追加された | Raftデータをstorageにフラッシュするプール内の許容スレッド数。デフォルト値は`4`です。                                                                                                                                                                                                                                                                                    |
| TiFlash         | [`raftstore.store-pool-size`](/tiflash/tiflash-configuration.md#configure-the-tiflash-learnertoml-file)         | 新しく追加された | Raftを処理するスレッドの許容数。これはRaftstoreスレッド プールのサイズです。デフォルト値は`4`です。                                                                                                                                                                                                                                                                           |
| TiDB データ移行 (DM) | [`collation_compatible`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)         | 新しく追加された | `CREATE` SQL ステートメントでデフォルトの照合順序を同期するモード。値のオプションは、「loose」(デフォルト) と「strict」です。                                                                                                                                                                                                                                                         |
| ティCDC           | `max-message-bytes`                                                                                             | 修正済み     | Kafka シンクのデフォルト値`max-message-bytes`を`104857601` (10MB) に変更します。                                                                                                                                                                                                                                                                       |
| ティCDC           | `partition-num`                                                                                                 | 修正済み     | Kafka Sink のデフォルト値`partition-num`を`4`から`3`に変更します。これにより、TiCDC は Kafaka パーティションにメッセージをより均等に送信するようになります。                                                                                                                                                                                                                                |
| TiDB Lightning  | `meta-schema-name`                                                                                              | 修正済み     | ターゲット TiDB 内のメタデータのスキーマ名を指定します。v5.4.0 以降では、このスキーマは[並行輸入](/tidb-lightning/tidb-lightning-distributed-import.md)有効にした場合にのみ作成されます (対応するパラメータは`tikv-importer.incremental-import = true`です)。                                                                                                                                              |
| TiDB Lightning  | `task-info-schema-name`                                                                                         | 新しく追加された | TiDB Lightning が競合を検出したときに重複データを保存するデータベースの名前を指定します。デフォルトでは、値は「lightning_task_info」です。このパラメータは、「duplicate-resolution」機能を有効にした場合にのみ指定します。                                                                                                                                                                                             |
| TiDB Lightning  | `incremental-import`                                                                                            | 新しく追加された | データがすでに存在するテーブルへのデータのインポートを許可するかどうかを決定します。デフォルト値は`false`です。                                                                                                                                                                                                                                                                          |

### その他 {#others}

-   TiDB と PD の間にインターフェースが追加`information_schema.TIDB_HOT_REGIONS_HISTORY`れました。1 システム テーブルを使用する場合、TiDB は対応するバージョンの PD を使用する必要があります。
-   TiDB サーバー、PD サーバー、および TiKV サーバーは、ログ名、出力形式、ローテーションと有効期限のルールを管理するために、ログ関連のパラメータに統一された命名方法を使用するようになりました。詳細については、 [TiKV 構成ファイル - ログ](/tikv-configuration-file.md#log-new-in-v540)参照してください。
-   v5.4.0 以降、プラン キャッシュによってキャッシュされた実行プランの SQL バインディングを作成すると、バインディングによって、対応するクエリに対してすでにキャッシュされているプランが無効になります。新しいバインディングは、v5.4.0 より前にキャッシュされた実行プランには影響しません。
-   v5.3 以前のバージョンでは、 [TiDB データ移行 (DM)](https://docs.pingcap.com/tidb-data-migration/v5.3/)ドキュメントは TiDB のドキュメントとは独立していました。v5.4 以降では、DM のドキュメントは TiDB のドキュメントに同じバージョンで統合されています。DM のドキュメントサイトにアクセスしなくても、 [DM ドキュメント](/dm/dm-overview.md)直接読むことができます。
-   cdclog とともに、Point-in-time recovery (PITR) の実験的機能を削除します。v5.4.0 以降、cdclog ベースの PITR と cdclog はサポートされなくなりました。
-   システム変数を「DEFAULT」に設定する動作をMySQLとより互換性のあるものにする[＃29680](https://github.com/pingcap/tidb/pull/29680)
-   システム変数`lc_time_names`読み取り専用[＃30084](https://github.com/pingcap/tidb/pull/30084)に設定する
-   `tidb_store_limit`のスコープをINSTANCEまたはGLOBALからGLOBAL [＃30756](https://github.com/pingcap/tidb/pull/30756)に設定する
-   列にゼロが含まれている場合、整数型列を時間型列に変換することを禁止する[＃25728](https://github.com/pingcap/tidb/pull/25728)
-   浮動小数点値を挿入するときに`Inf`または`NAN`値に対してエラーが報告されない問題を修正しました[＃30148](https://github.com/pingcap/tidb/pull/30148)
-   自動IDが範囲外の場合に`REPLACE`文が他の行を誤って変更する問題を修正[#30301](https://github.com/pingcap/tidb/pull/30301)

## 新機能 {#new-features}

### 構文 {#sql}

-   **TiDBはv5.4.0以降、GBK文字セットをサポートしています。**

    v5.4.0 より前では、 TiDB は`ascii` 、 `binary` 、 `latin1` 、 `utf8` 、および`utf8mb4`文字セットをサポートしています。

    中国語ユーザーをより適切にサポートするために、TiDB はバージョン 5.4.0 以降で GBK 文字セットをサポートしています。TiDB クラスターを初めて初期化するときに TiDB 構成ファイルで[`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap)オプションを有効にすると、TiDB GBK 文字セットは`gbk_bin`と`gbk_chinese_ci`両方の照合をサポートします。

    GBK文字セットを使用する場合は、互換性の制限に注意する必要があります。詳細については、 [文字セットと照合順序 - GBK](/character-set-gbk.md)参照してください。

### Security {#security}

-   **TiSparkはユーザー認証と承認をサポートします**

    TiSpark 2.5.0 以降、TiSpark はデータベース ユーザー認証と、データベースまたはテーブル レベルでの読み取り/書き込み承認の両方をサポートしています。この機能を有効にすると、データを取得するための描画などの不正なバッチ タスクの実行をビジネスで防止できるため、オンライン クラスターの安定性とデータ セキュリティが向上します。

    この機能はデフォルトで無効になっています。有効にすると、TiSpark を介して操作するユーザーに必要な権限がない場合、そのユーザーは TiSpark から例外を受け取ります。

    [ユーザードキュメント](/tispark-overview.md#security)

-   **TiUPはルートユーザーの初期パスワードの生成をサポートしています**

    クラスターを起動するコマンドに`--init`パラメーターが導入されました。このパラメーターにより、 TiUP を使用してデプロイされた TiDB クラスターでは、 TiUP がデータベース ルート ユーザーの初期強力パスワードを生成します。これにより、空のパスワードを持つルート ユーザーを使用することによるセキュリティ リスクが回避され、データベースのセキュリティが確保されます。

    [ユーザードキュメント](/production-deployment-using-tiup.md#step-7-start-a-tidb-cluster)

### パフォーマンス {#performance}

-   **列指向storageエンジンTiFlashとコンピューティングエンジンMPPの安定性とパフォーマンスを継続的に向上**

    -   より多くの関数をMPP エンジンにプッシュダウンすることをサポートします。

        -   `RPAD()` `STRCMP()`関数: `LPAD()`
        -   `QUARTER()`関数`SUBDATE(string, real)` `ADDDATE(string, real)` `DATE_ADD(string, real)` `DATE_SUB(string, real)`

    -   リソース使用率を向上させるためにエラスティック スレッド プール機能を導入します (実験的)

    -   TiKVからデータを複製する際に、行ベースのstorage形式から列ベースのstorage形式にデータを変換する効率を改善し、データ複製の全体的なパフォーマンスを50%向上させます。

    -   いくつかの構成項目のデフォルト値を調整することで、 TiFlash のパフォーマンスと安定性が向上します。HTAP ハイブリッド ロードでは、単一テーブルに対する単純なクエリのパフォーマンスが最大 20% 向上します。

    ユーザードキュメント: [プッシュダウン計算をサポート](/tiflash/tiflash-supported-pushdown-calculations.md) 、 [tiflash.tomlファイルを設定する](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)

-   **セッション変数を通じて指定された時間範囲内の履歴データを読み取る**

    TiDB は、 Raftコンセンサス アルゴリズムに基づくマルチレプリカ分散データベースです。高同時実行性と高スループットのアプリケーション シナリオでは、TiDB はフォロワー レプリカを通じて読み取りパフォーマンスをスケールアウトし、読み取り要求と書き込み要求を分離できます。

    さまざまなアプリケーション シナリオに対して、TiDB は、強力な一貫性のある読み取りと弱い一貫性のある履歴読み取りという 2 つのフォロワー読み取りモードを提供します。強力な一貫性のある読み取りモードは、リアルタイム データを必要とするアプリケーション シナリオに適しています。ただし、このモードでは、リーダーとフォロワー間のデータ レプリケーションのレイテンシーとスループットの低下により、特に地理的に分散された展開では、読み取り要求のレイテンシーが長くなる可能性があります。

    リアルタイム データに対する要件がそれほど厳しくないアプリケーション シナリオでは、履歴読み取りモードが推奨されます。このモードでは、レイテンシーが短縮され、スループットが向上します。TiDB は現在、次の方法による履歴データの読み取りをサポートしています。SQL ステートメントを使用して過去のある時点からデータを読み取るか、過去の時点に基づいて読み取り専用トランザクションを開始します。どちらの方法でも、特定の時点または指定された時間範囲内の履歴データの読み取りがサポートされています。詳細については、 [`AS OF TIMESTAMP`句を使用して履歴データを読み取る](/as-of-timestamp.md)を参照してください。

    v5.4.0 以降、TiDB はセッション変数を通じて指定された時間範囲内の履歴データの読み取りをサポートすることで、履歴読み取りモードの使いやすさを向上させました。このモードは、準リアルタイム シナリオで低レイテンシ、高スループットの読み取り要求に対応します。変数は次のように設定できます。

    ```sql
    set @@tidb_replica_read=leader_and_follower
    set @@tidb_read_staleness="-5"
    ```

    この設定により、TiDB は最も近いリーダー ノードまたはフォロワー ノードを選択し、5 秒以内に最新の履歴データを読み取ることができます。

    [ユーザードキュメント](/tidb-read-staleness.md)

-   **インデックス統合の GA**

    インデックス マージは、SQL 最適化の実験的機能として TiDB v4.0 で導入されました。この方法は、クエリで複数のデータ列のスキャンが必要な場合に、条件のフィルタリングを大幅に高速化します。次のクエリを例に挙げます`WHERE`ステートメントで、 `OR`で接続されたフィルタリング条件に列*key1*と*key2*のそれぞれのインデックスがある場合、インデックス マージ機能はそれぞれのインデックスを同時にフィルタリングし、クエリ結果をマージして、マージされた結果を返します。

    ```sql
    SELECT * FROM table WHERE key1 <= 100 OR key2 = 200;
    ```

    TiDB v4.0 より前では、テーブルに対するクエリでは、フィルタリングに一度に 1 つのインデックスのみを使用できます。複数のデータ列をクエリする場合は、インデックス マージを有効にして、個々の列のインデックスを使用することで、短時間で正確なクエリ結果を取得できます。インデックス マージにより、不要なテーブル全体のスキャンが回避され、多数の複合インデックスを確立する必要がなくなります。

    v5.4.0 では、インデックス マージが GA になります。ただし、以下の制限には引き続き注意する必要があります。

    -   インデックスマージは、選言正規形 (X <sub>1</sub> ⋁ X <sub>2</sub> ⋁ …X <sub>n</sub> ) のみをサポートします。つまり、この機能は、 `WHERE`節のフィルタリング条件が`OR`で接続されている場合にのみ機能します。

    -   新しくデプロイされた v5.4.0 以降の TiDB クラスターの場合、この機能はデフォルトで有効になっています。以前のバージョンからアップグレードされた v5.4.0 以降の TiDB クラスターの場合、この機能はアップグレード前の設定を継承し、必要に応じて設定を変更できます (v4.0 より前の TiDB クラスターの場合、この機能は存在せず、デフォルトで無効になっています)。

    [ユーザードキュメント](/explain-index-merge.md)

-   **Raft Engineのサポート (実験的)**

    TiKV のログstorageエンジンとして[Raft Engine](https://github.com/tikv/raft-engine)使用をサポートします。RocksDB と比較して、 Raft Engine はTiKV I/O 書き込みトラフィックを最大 40%、CPU 使用率を 10% 削減し、フォアグラウンド スループットを約 5% 向上させ、特定の負荷下でテールレイテンシーを 20% 削減します。さらに、 Raft Engine はログのリサイクル効率を向上させ、極端な状況でのログ蓄積の問題を修正します。

    Raft Engineはまだ実験的機能であり、デフォルトでは無効になっています。v5.4.0 のRaft EngineはRaft Engine以降のバージョンでのみ使用することをお勧めします。

    [ユーザードキュメント](/tikv-configuration-file.md#raft-engine)

-   **`PREDICATE COLUMNS`の統計収集をサポート (実験的)**

    ほとんどの場合、SQL ステートメントを実行するときに、オプティマイザは一部の列 ( `WHERE` 、 `JOIN` 、 `ORDER BY` 、および`GROUP BY`ステートメントの列など) の統計のみを使用します。これらの使用される列は`PREDICATE COLUMNS`と呼ばれます。

    v5.4.0 以降では、 [`tidb_enable_column_tracking`](/system-variables.md#tidb_enable_column_tracking-new-in-v540)システム変数の値を`ON`に設定して、TiDB が`PREDICATE COLUMNS`収集できるようにすることができます。

    設定後、TiDB は 100 * [`stats-lease`](/tidb-configuration-file.md#stats-lease)ごとに`PREDICATE COLUMNS`情報を`mysql.column_stats_usage`システム テーブルに書き込みます。ビジネスのクエリ パターンが安定している場合は、 `ANALYZE TABLE TableName PREDICATE COLUMNS`構文を使用して`PREDICATE COLUMNS`列のみの統計を収集できます。これにより、統計収集のオーバーヘッドを大幅に削減できます。

    [ユーザードキュメント](/statistics.md#collect-statistics-on-some-columns)

-   **統計情報の同期読み込みをサポート (実験的)**

    v5.4.0 以降、TiDB では統計の同期ロード機能が導入されています。この機能はデフォルトでは無効になっています。この機能を有効にすると、SQL ステートメントを実行するときに、TiDB は大規模な統計 (ヒストグラム、TopN、Count-Min Sketch 統計など) をメモリに同期ロードできるようになり、SQL 最適化の統計の完全性が向上します。

    [ユーザードキュメント](/statistics.md#load-statistics)

### 安定性 {#stability}

-   **永続的なANALYZE構成をサポート**

    統計は、オプティマイザが実行プランを生成する際に参照する基本情報の 1 つです。統計の精度は、生成された実行プランが妥当かどうかに直接影響します。統計の精度を確保するには、テーブル、パーティション、インデックスごとに異なる収集構成を設定する必要がある場合があります。

    v5.4.0 以降、TiDB はいくつかの`ANALYZE`の構成の永続化をサポートしています。この機能により、将来の統計収集に既存の構成を簡単に再利用できます。

    `ANALYZE`構成の永続性機能はデフォルトで有効になっています (システム変数`tidb_analyze_version`は`2`で[`tidb_persist_analyze_options`](/system-variables.md#tidb_persist_analyze_options-new-in-v540)デフォルトで`ON`です)。この機能を使用すると、 `ANALYZE`ステートメントを手動で実行するときに、ステートメントで指定された永続性構成を記録できます。記録されると、次に TiDB が統計を自動的に更新するか、これらの構成を指定せずに手動で統計を収集するときに、TiDB は記録された構成に従って統計を収集します。

    [ユーザードキュメント](/statistics.md#persist-analyze-configurations)

### 高可用性と災害復旧 {#high-availability-and-disaster-recovery}

-   **バックアップタスクによるクラスタへの影響を軽減する**

    バックアップと復元 (BR) では、自動調整機能が導入されています (デフォルトで有効)。この機能は、クラスター リソースの使用状況を監視し、バックアップ タスクで使用されるスレッドの数を調整することで、クラスターに対するバックアップ タスクの影響を軽減できます。場合によっては、バックアップ用のクラスター ハードウェア リソースを増やし、自動調整機能を有効にすると、クラスターに対するバックアップ タスクの影響を 10% 以下に抑えることができます。

    [ユーザードキュメント](/br/br-auto-tune.md)

-   **バックアップのターゲットstorageとしてAzure Blob Storageをサポート**

    バックアップと復元 (BR) は、リモート バックアップstorageとして Azure Blob Storage をサポートします。Azure Cloud に TiDB をデプロイすると、クラスター データを Azure Blob Storage サービスにバックアップできるようになります。

    [ユーザードキュメント](/br/backup-and-restore-storages.md)

### データ移行 {#data-migration}

-   **TiDB Lightningは、データを含むテーブルへのデータのインポートを許可するかどうかを決定する新しい機能を導入しました。**

    TiDB Lightning、構成項目`incremental-import`が導入されています。これは、データを含むテーブルへのデータのインポートを許可するかどうかを決定します。デフォルト値は`false`です。並列インポート モードを使用する場合は、構成を`true`に設定する必要があります。

    [ユーザードキュメント](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)

-   **TiDB Lightningは並列インポートのメタ情報を格納するスキーマ名を導入します**

    TiDB Lightningでは、 `meta-schema-name`構成項目が導入されています。並列インポート モードでは、このパラメータは、ターゲット クラスター内の各TiDB Lightningインスタンスのメタ情報を格納するスキーマ名を指定します。デフォルトでは、値は「lightning_metadata」です。このパラメータに設定される値は、同じ並列インポートに参加する各TiDB Lightningインスタンスで同じである必要があります。そうでない場合、インポートされたデータの正確性は保証されません。

    [ユーザードキュメント](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)

-   **TiDB Lightningが重複解決を導入**

    ローカルバックエンド モードでは、 TiDB Lightning はデータのインポートが完了する前に重複データを出力し、その重複データをデータベースから削除します。インポートが完了したら重複データを解決し、アプリケーション ルールに従って挿入する適切なデータを選択できます。後続の増分データ移行フェーズで重複データが発生することによるデータの不整合を回避するために、重複データに基づいて上流のデータ ソースをクリーンアップすることをお勧めします。

    [ユーザードキュメント](/tidb-lightning/tidb-lightning-error-resolution.md)

-   **TiDB データ移行 (DM) におけるリレー ログの使用を最適化します。**

    -   `source`構成内の`enable-relay`スイッチを回復します。

    -   `start-relay`および`stop-relay`コマンドを使用してリレー ログを動的に有効化および無効化することをサポートします。

    -   リレー ログのステータスを`source`にバインドします。 `source`任意の DM ワーカーに移行された後も、有効または無効の元のステータスを保持します。

    -   リレー ログのstorageパスを DM-worker 構成ファイルに移動します。

    [ユーザードキュメント](/dm/relay-log.md)

-   **DMでの<a href="/character-set-and-collation.md">照合順序</a>処理を最適化**

    `collation_compatible`構成項目を追加します。値のオプションは`loose` (デフォルト) と`strict`です。

    -   アプリケーションに照合順序に関する厳密な要件がなく、クエリ結果の照合順序がアップストリームとダウンストリームで異なる可能性がある場合は、デフォルトの`loose`モードを使用してエラーの報告を回避できます。
    -   アプリケーションに照合順序に関する厳格な要件があり、アップストリームとダウンストリームの間で照合順序の一貫性を保つ必要がある場合は、 `strict`モードを使用できます。ただし、ダウンストリームがアップストリームのデフォルトの照合順序をサポートしていない場合、データ レプリケーションでエラーが報告される可能性があります。

    [ユーザードキュメント](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)

-   **DM の`transfer source`最適化して、レプリケーション タスクをスムーズに実行できるようにします。**

    DM ワーカー ノードに不均衡な負荷がある場合、 `transfer source`コマンドを使用して、 `source`の構成を別の負荷に手動で転送できます。最適化後、 `transfer source`コマンドによって手動操作が簡素化されます。DM は他の操作を内部的に完了するため、関連するすべてのタスクを一時停止する代わりに、ソースをスムーズに転送できます。

-   **DM OpenAPI が一般公開 (GA) されました**

    DM は、データ ソースの追加やタスクの管理など、API 経由の日常管理をサポートします。v5.4.0 では、DM OpenAPI が GA になります。

    [ユーザードキュメント](/dm/dm-open-api.md)

### 診断効率 {#diagnostic-efficiency}

-   **Top SQL （実験的機能）**

    ソースを消費するクエリを簡単に見つけられるように、新しい実験的機能であるTop SQL (デフォルトでは無効) が導入されました。

    [ユーザードキュメント](/dashboard/top-sql.md)

### TiDBデータ共有サブスクリプション {#tidb-data-share-subscription}

-   **TiCDC のクラスターへの影響を最適化する**

    TiCDC を使用すると、TiDB クラスターのパフォーマンスへの影響が大幅に軽減されます。テスト環境では、TiCDC が TiDB に及ぼすパフォーマンスの影響を 5% 未満に軽減できます。

### 導入とメンテナンス {#deployment-and-maintenance}

-   **継続的プロファイリングの強化 (実験的)**

    -   サポートされるコンポーネントの追加: TiDB、PD、TiKV に加えて、TiDB v5.4.0 はTiFlashの CPU プロファイリングもサポートします。

    -   プロファイリング表示のより多くの形式: フレーム チャートでの CPU プロファイリングと Goroutine の結果の表示をサポートします。

    -   より多くのデプロイメント環境がサポートされます: 継続的なプロファイリングは、 TiDB Operator を使用してデプロイされたクラスターでも使用できます。

    継続的なプロファイリングはデフォルトで無効になっていますが、TiDB ダッシュボードで有効にすることができます。

    継続的なプロファイリングは、 TiUP v1.9.0 以降またはTiDB Operator v1.3.0 以降を使用してデプロイまたはアップグレードされたクラスターに適用できます。

    [ユーザードキュメント](/dashboard/continuous-profiling.md)

## 改善点 {#improvements}

-   ティビ

    -   キャッシュされたクエリプランをクリアするための`ADMIN {SESSION | INSTANCE | GLOBAL} PLAN_CACHE`構文をサポートする[＃30370](https://github.com/pingcap/tidb/pull/30370)

-   ティクヴ

    -   コプロセッサーは、ストリームのような方法でリクエストを処理するためのページングAPIをサポートしています[＃11448](https://github.com/tikv/tikv/issues/11448)
    -   読み取り操作で二次ロックが解決されるのを待つ必要がないように`read-through-lock`サポートする[＃11402](https://github.com/tikv/tikv/issues/11402)
    -   ディスク容量の枯渇によるpanicを回避するためにディスク保護メカニズムを追加する[＃10537](https://github.com/tikv/tikv/issues/10537)
    -   ログのアーカイブとローテーションをサポート[＃11651](https://github.com/tikv/tikv/issues/11651)
    -   Raftクライアントによるシステムコールを減らしCPU効率を上げる[＃11309](https://github.com/tikv/tikv/issues/11309)
    -   コプロセッサーはTiKV [＃11495](https://github.com/tikv/tikv/issues/11495)への部分文字列のプッシュダウンをサポートします。
    -   Read Committed分離レベル[＃11485](https://github.com/tikv/tikv/issues/11485)でロックの読み取りをスキップすることでスキャンパフォーマンスを向上します。
    -   バックアップ操作で使用されるデフォルトのスレッドプールサイズを減らし、ストレスが高いときにスレッドプールの使用を制限する[＃11000](https://github.com/tikv/tikv/issues/11000)
    -   Apply スレッド プールと Store スレッド プールのサイズを動的に調整する機能をサポート[＃11159](https://github.com/tikv/tikv/issues/11159)
    -   `snap-generator`スレッドプール[＃11247](https://github.com/tikv/tikv/issues/11247)のサイズ設定をサポート
    -   頻繁に読み書きされるファイルが多数ある場合に発生するグローバルロック競合の問題を最適化します[＃250](https://github.com/tikv/rocksdb/pull/250)

-   PD

    -   デフォルトで過去のホットスポット情報を記録する[＃25281](https://github.com/pingcap/tidb/issues/25281)
    -   リクエストソースを識別するためにHTTPコンポーネントに署名を追加する[＃4490](https://github.com/tikv/pd/issues/4490)
    -   TiDBダッシュボードをv2021.12.31 [＃4257](https://github.com/tikv/pd/issues/4257)に更新

-   TiFlash

    -   ローカルオペレータのコミュニケーションを最適化する
    -   スレッドの頻繁な作成や破棄を避けるために、gRPC の非一時的スレッド数を増やす

-   ツール

    -   バックアップと復元 (BR)

        -   BRが暗号化バックアップ[＃29794](https://github.com/pingcap/tidb/issues/29794)を実行するときにキーの有効性チェックを追加する

    -   ティCDC

        -   「EventFeed 再試行レート制限」ログの数を減らす[＃4006](https://github.com/pingcap/tiflow/issues/4006)
        -   多数のテーブルを複製する場合のレプリケーションのレイテンシーを減らす[＃3900](https://github.com/pingcap/tiflow/issues/3900)
        -   TiKVストアがダウンしたときにKVクライアントが回復するまでの時間を短縮する[＃3191](https://github.com/pingcap/tiflow/issues/3191)

    -   TiDB データ移行 (DM)

        -   リレー有効時のCPU使用率を下げる[＃2214](https://github.com/pingcap/dm/issues/2214)

    -   TiDB Lightning

        -   TiDBバックエンドモード[＃30953](https://github.com/pingcap/tidb/pull/30953)でのパフォーマンスを向上させるために、デフォルトで楽観的トランザクションを使用してデータを書き込む

    -   Dumpling

        -   Dumpling がデータベース バージョン[＃29500](https://github.com/pingcap/tidb/pull/29500)をチェックする際の互換性を向上
        -   `CREATE DATABASE`と`CREATE TABLE`ダンプするときにデフォルトの照合照合順序を追加する[＃3420](https://github.com/pingcap/tiflow/issues/3420)

## バグ修正 {#bug-fixes}

-   ティビ

    -   クラスターをv4.xからv5.xにアップグレードするときに発生する`tidb_analyze_version`値の変更の問題を修正しました[＃25422](https://github.com/pingcap/tidb/issues/25422)
    -   サブクエリ[＃30748](https://github.com/pingcap/tidb/issues/30748)で異なる照合順序を使用した場合に誤った結果が発生する問題を修正しました
    -   TiDBの`concat(ifnull(time(3))`の結果がMySQL [＃29498](https://github.com/pingcap/tidb/issues/29498)の結果と異なる問題を修正
    -   楽観的トランザクションモード[＃30410](https://github.com/pingcap/tidb/issues/30410)でデータインデックスの不整合が発生する可能性がある問題を修正
    -   式を TiKV [#30200](https://github.com/pingcap/tidb/issues/30200)にプッシュダウンできない場合に IndexMerge のクエリ実行プランが間違っている問題を修正しました。
    -   同時列型変更によりスキーマとデータの間に不整合が発生する問題を修正[＃31048](https://github.com/pingcap/tidb/issues/31048)
    -   サブクエリ[＃30913](https://github.com/pingcap/tidb/issues/30913)がある場合にIndexMergeクエリの結果が間違っている問題を修正
    -   クライアント[＃30896](https://github.com/pingcap/tidb/issues/30896)で FetchSize が大きすぎる値に設定されている場合に発生するpanic問題を修正しました。
    -   LEFT JOINが誤ってINNER JOIN [＃20510](https://github.com/pingcap/tidb/issues/20510)に変換される可能性がある問題を修正
    -   `CASE-WHEN`式と照合順序を一緒に使用するとpanicが発生する可能性がある問題を修正[#30245](https://github.com/pingcap/tidb/issues/30245)
    -   `IN`値にバイナリ定数[＃31261](https://github.com/pingcap/tidb/issues/31261)が含まれている場合に発生する誤ったクエリ結果の問題を修正しました
    -   CTE にサブクエリ[＃31255](https://github.com/pingcap/tidb/issues/31255)ある場合に発生する誤ったクエリ結果の問題を修正しました
    -   `INSERT ... SELECT ... ON DUPLICATE KEY UPDATE`文を実行するとpanic[＃28078](https://github.com/pingcap/tidb/issues/28078)が発生する問題を修正
    -   INDEX HASH JOINが`send on closed channel`エラーを返す問題を修正しました[＃31129](https://github.com/pingcap/tidb/issues/31129)

-   ティクヴ

    -   MVCC削除レコードがGC [＃11217](https://github.com/tikv/tikv/issues/11217)によってクリアされない問題を修正
    -   悲観的トランザクションモードで事前書き込み要求を再試行すると、まれにデータの不整合が発生するリスクがある問題を修正しました[＃11187](https://github.com/tikv/tikv/issues/11187)
    -   GCスキャンによりメモリオーバーフローが発生する問題を修正[＃11410](https://github.com/tikv/tikv/issues/11410)
    -   ディスク容量がいっぱいのときにRocksDBのフラッシュまたは圧縮によってpanicが発生する問題を修正[＃11224](https://github.com/tikv/tikv/issues/11224)

-   PD

    -   リージョン統計が`flow-round-by-digit` [＃4295](https://github.com/tikv/pd/issues/4295)の影響を受けない問題を修正
    -   ターゲットストアがダウンしているためにスケジューリングオペレータがフェイルファストを実行できない問題を修正[＃3353](https://github.com/tikv/pd/issues/3353)
    -   オフラインストアの地域を統合できない問題を修正[＃4119](https://github.com/tikv/pd/issues/4119)
    -   ホットスポット統計からコールドホットスポットデータを削除できない問題を修正[＃4390](https://github.com/tikv/pd/issues/4390)

-   TiFlash

    -   MPPクエリが停止したときにTiFlashがpanicになる可能性がある問題を修正
    -   `where <string>`句のクエリが間違った結果を返す問題を修正しました
    -   整数主キーの列タイプをより大きな範囲に設定するときに発生する可能性のあるデータの不整合の問題を修正しました。
    -   入力時間が 1970-01-01 00:00:01 UTC より前の場合、 `unix_timestamp`の動作が TiDB または MySQL の動作と一致しない問題を修正しました。
    -   TiFlashが再起動後に`EstablishMPPConnection`エラーを返す可能性がある問題を修正しました
    -   `CastStringAsDecimal`動作がTiFlashと TiDB/TiKV で一貫していない問題を修正
    -   クエリ結果に`DB::Exception: Encode type of coprocessor response is not CHBlock`エラーが返される問題を修正
    -   `castStringAsReal`動作がTiFlashと TiDB/TiKV で一貫していない問題を修正
    -   TiFlashの`date_add_string_xxx`関数の戻り結果がMySQLの結果と一致しない問題を修正

-   ツール

    -   バックアップと復元 (BR)

        -   復元操作が完了した後にリージョンの配分が不均一になる可能性がある問題を修正[＃30425](https://github.com/pingcap/tidb/issues/30425)
        -   バックアップstorage[#30104](https://github.com/pingcap/tidb/issues/30104)として`minio`使用されている場合、エンドポイントに`'/'`指定できない問題を修正
        -   システムテーブルを同時にバックアップするとテーブル名の更新に失敗するため、システムテーブルを復元できない問題を修正[＃29710](https://github.com/pingcap/tidb/issues/29710)

    -   ティCDC

        -   `min.insync.replicas`が`replication-factor`より小さい場合にレプリケーションを実行できない問題を修正しました[＃3994](https://github.com/pingcap/tiflow/issues/3994)
        -   `cached region`監視メトリックが負の[＃4300](https://github.com/pingcap/tiflow/issues/4300)になる問題を修正
        -   `mq sink write row`に監視データがない問題を修正[＃3431](https://github.com/pingcap/tiflow/issues/3431)
        -   `sql mode` [＃3810](https://github.com/pingcap/tiflow/issues/3810)の互換性問題を修正
        -   レプリケーションタスクが削除されたときに発生する可能性のあるpanic問題を修正[＃3128](https://github.com/pingcap/tiflow/issues/3128)
        -   デフォルトの列値[＃3929](https://github.com/pingcap/tiflow/issues/3929)を出力するときに発生するpanicとデータの不整合の問題を修正
        -   デフォルト値を複製できない問題を修正[＃3793](https://github.com/pingcap/tiflow/issues/3793)
        -   デッドロックによりレプリケーションタスクが停止する可能性がある問題を修正[＃4055](https://github.com/pingcap/tiflow/issues/4055)
        -   ディスクが完全に書き込まれたときにログが出力されない問題を修正[＃3362](https://github.com/pingcap/tiflow/issues/3362)
        -   DDL ステートメント内の特別なコメントによってレプリケーション タスクが停止する問題を修正[＃3755](https://github.com/pingcap/tiflow/issues/3755)
        -   RHELリリース[＃3584](https://github.com/pingcap/tiflow/issues/3584)のタイムゾーンの問題によりサービスを開始できない問題を修正
        -   不正確なチェックポイント[＃3545](https://github.com/pingcap/tiflow/issues/3545)によって発生する潜在的なデータ損失の問題を修正
        -   コンテナ環境のOOM問題を修正[＃1798](https://github.com/pingcap/tiflow/issues/1798)
        -   `config.Metadata.Timeout` [＃3352](https://github.com/pingcap/tiflow/issues/3352)の誤った構成によって発生するレプリケーション停止の問題を修正

    -   TiDB データ移行 (DM)

        -   `CREATE VIEW`ステートメントがデータレプリケーション[＃4173](https://github.com/pingcap/tiflow/issues/4173)を中断する問題を修正
        -   DDL ステートメントをスキップした後にスキーマをリセットする必要がある問題を修正[＃4177](https://github.com/pingcap/tiflow/issues/4177)
        -   DDL 文がスキップされた後にテーブル チェックポイントが時間内に更新されない問題を修正[＃4184](https://github.com/pingcap/tiflow/issues/4184)
        -   TiDBバージョンとパーサーバージョン[＃4298](https://github.com/pingcap/tiflow/issues/4298)の互換性の問題を修正
        -   ステータス[＃4281](https://github.com/pingcap/tiflow/issues/4281)を照会するときにのみ同期メトリックが更新される問題を修正しました

    -   TiDB Lightning

        -   TiDB Lightningに`mysql.tidb`テーブル[＃31088](https://github.com/pingcap/tidb/issues/31088)にアクセスする権限がない場合に発生する誤ったインポート結果の問題を修正しました。
        -   TiDB Lightningの再起動時に一部のチェックがスキップされる問題を修正[＃30772](https://github.com/pingcap/tidb/issues/30772)
        -   S3 パスが存在しない場合にTiDB Lightning がエラーを報告できない問題を修正[＃30674](https://github.com/pingcap/tidb/pull/30674)

    -   TiDBBinlog

        -   `CREATE PLACEMENT POLICY`ステートメント[＃1118](https://github.com/pingcap/tidb-binlog/issues/1118)と互換性がないため、 Drainer が失敗する問題を修正しました。
