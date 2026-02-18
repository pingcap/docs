---
title: TiDB 5.4 Release Notes
summary: TiDB 5.4では、GBK文字セット、インデックスマージ、古いデータの読み取り、統計設定の永続化、TiKVのログstorageエンジンとしてのRaft Engineの使用のサポートが導入されました。また、バックアップの影響が改善され、Azure Blobstorageがサポートされ、 TiFlashとMPPエンジンが強化されました。互換性の変更には、新しいシステム変数と構成ファイルパラメータが含まれます。その他の改善点としては、SQL、セキュリティ、パフォーマンス、安定性、高可用性、データ移行、診断効率、デプロイメントが挙げられます。バグ修正では、TiDB、TiKV、PD、 TiFlash、 BR、TiCDC、DM、 TiDB Lightning、TiDB Binlogの問題が修正されています。
---

# TiDB 5.4 リリースノート {#tidb-5-4-release-notes}

発売日：2022年2月15日

TiDB バージョン: 5.4.0

v5.4 の主な新機能または改善点は次のとおりです。

-   GBK文字セットをサポートする
-   複数の列のインデックスのフィルタリング結果をマージするインデックスマージを使用したデータへのアクセスをサポートします。
-   セッション変数を使用した古いデータの読み取りをサポート
-   統計情報を収集するための設定の永続化をサポート
-   TiKV のログstorageエンジンとしてRaft Engineの使用をサポート (実験的)
-   クラスタへのバックアップの影響を最適化する
-   バックアップstorageとして Azure Blobstorageの使用をサポート
-   TiFlashとMPPエンジンの安定性とパフォーマンスを継続的に向上させます
-   TiDB Lightningにスイッチを追加して、既存のテーブルにデータをインポートできるようにするかどうかを決定します。
-   継続的なプロファイリング機能の最適化（実験的）
-   TiSparkはユーザーの識別と認証をサポートします

## 互換性の変更 {#compatibility-changes}

> **注記：**
>
> 以前の TiDB バージョンから v5.4.0 にアップグレードする場合、すべての中間バージョンの互換性変更ノートを知りたい場合は、該当するバージョンの[リリースノート](/releases/_index.md)確認できます。

### システム変数 {#system-variables}

<table><thead><tr><th>変数名</th><th>タイプを変更</th><th>説明</th></tr></thead><tbody><tr><td><a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_enable_column_tracking-new-in-v540"><code>tidb_enable_column_tracking</code></a></td><td>新しく追加された</td><td>TiDBが<code>PREDICATE COLUMNS</code>を収集することを許可するかどうかを制御します。デフォルト値は<code>OFF.</code></td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_enable_paging-new-in-v540"><code>tidb_enable_paging</code></a></td><td>新しく追加された</td><td><code>IndexLookUp</code>演算子でコプロセッサリクエストを送信する際にページング方式を使用するかどうかを制御します。デフォルト値は<code>OFF</code>です。<br/> <code>IndexLookup</code>と<code>Limit</code>を使用し、 <code>Limit</code>を<code>IndexScan</code>にプッシュダウンできない読み取りクエリの場合、読み取りクエリのレイテンシーが長くなり、TiKV の<code>unified read pool</code>の CPU 使用率が高くなる可能性があります。このような場合、 <code>Limit</code>演算子は少量のデータしか必要としないため、 <code>tidb_enable_paging</code> <code>ON</code>に設定すると、TiDB が処理するデータ量が少なくなり、クエリのレイテンシーとリソース消費が削減されます。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_enable_top_sql-new-in-v540"><code>tidb_enable_top_sql</code></a></td><td>新しく追加された</td><td>Top SQL機能を有効にするかどうかを制御します。デフォルト値は<code>OFF</code>です。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_persist_analyze_options-new-in-v540"><code>tidb_persist_analyze_options</code></a></td><td>新しく追加された</td><td><a href="https://docs.pingcap.com/tidb/dev/statistics#persist-analyze-configurations">ANALYZE構成の永続化</a>機能を有効にするかどうかを制御します。デフォルト値は<code>ON</code>です。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_read_staleness-new-in-v540"><code>tidb_read_staleness</code></a></td><td>新しく追加された</td><td>現在のセッションで読み取ることができる履歴データの範囲を制御します。デフォルト値は<code>0</code>です。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_regard_null_as_point-new-in-v540"><code>tidb_regard_null_as_point</code></a></td><td>新しく追加された</td><td>オプティマイザーがインデックス アクセスのプレフィックス条件として NULL 等価性を含むクエリ条件を使用できるかどうかを制御します。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_stats_load_sync_wait-new-in-v540"><code>tidb_stats_load_sync_wait</code></a></td><td>新しく追加された</td><td>統計情報の同期読み込み機能を有効にするかどうかを制御します。デフォルト値<code>0</code>は、この機能が無効であり、統計情報が非同期に読み込まれることを意味します。この機能が有効になっている場合、この変数は、SQL最適化が統計情報の同期読み込みをタイムアウトまでに待機できる最大時間を制御します。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_stats_load_pseudo_timeout-new-in-v540"><code>tidb_stats_load_pseudo_timeout</code></a></td><td>新しく追加された</td><td>統計情報の同期ロードがタイムアウトに達したときに、SQLが失敗するか（ <code>OFF</code> ）、疑似統計情報を使用するか（ <code>ON</code> ）を制御します。デフォルト値は<code>OFF</code>です。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_backoff_lock_fast"><code>tidb_backoff_lock_fast</code></a></td><td>修正済み</td><td>デフォルト値は<code>100</code>から<code>10</code>に変更されます。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_enable_index_merge-new-in-v40"><code>tidb_enable_index_merge</code></a></td><td>修正済み</td><td>デフォルト値が<code>OFF</code>から<code>ON</code>に変更されます。<ul><li> TiDB クラスターを v4.0.0 より前のバージョンから v5.4.0 以降にアップグレードする場合、この変数はデフォルトで<code>OFF</code>なります。</li><li> TiDB クラスターを v4.0.0 以降から v5.4.0 以降にアップグレードする場合、この変数はアップグレード前と同じままになります。</li><li> v5.4.0 以降で新しく作成された TiDB クラスターの場合、この変数はデフォルトで<code>ON</code>なります。</li></ul></td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_store_limit-new-in-v304-and-v40"><code>tidb_store_limit</code></a></td><td>修正済み</td><td>バージョン5.4.0より前では、この変数はインスタンスレベルとグローバルの両方で設定できました。バージョン5.4.0以降では、この変数はグローバル設定のみをサポートします。</td></tr></tbody></table>

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル  | コンフィグレーション                                                                                                      | タイプを変更   | 説明                                                                                                                                                                                                                                                                                                             |
| :-------------- | :-------------------------------------------------------------------------------------------------------------- | :------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ティドブ            | [`stats-load-concurrency`](/tidb-configuration-file.md#stats-load-concurrency-new-in-v540)                      | 新しく追加された | TiDB同期ロード統計機能が同時に処理できる列の最大数を制御します。デフォルト値は`5`です。                                                                                                                                                                                                                                                                |
| ティドブ            | [`stats-load-queue-size`](/tidb-configuration-file.md#stats-load-queue-size-new-in-v540)                        | 新しく追加された | TiDB同期ロード統計機能がキャッシュできる列リクエストの最大数を制御します。デフォルト値は`1000`です。                                                                                                                                                                                                                                                        |
| ティクブ            | [`snap-generator-pool-size`](/tikv-configuration-file.md#snap-generator-pool-size-new-in-v540)                  | 新しく追加された | `snap-generator`スレッドプールのサイズ。デフォルト値は`2`です。                                                                                                                                                                                                                                                                      |
| ティクブ            | `log.file.max-size` `log.file.max-days` `log.file.max-backups`                                                  | 新しく追加された | 詳細は[TiKVコンフィグレーションファイル - `log.file`](/tikv-configuration-file.md#logfile-new-in-v540)参照。                                                                                                                                                                                                                       |
| ティクブ            | `raft-engine`                                                                                                   | 新しく追加された | `enable` 、 `dir` 、 `batch-compression-threshold` 、 `bytes-per-sync` 、 `target-file-size` 、 `purge-threshold` 、 `recovery-mode` 、 `recovery-read-block-size` 、 `recovery-read-block-size` 、 `recovery-threads`が含まれます。詳細は[TiKVコンフィグレーションファイル - `raft-engine`](/tikv-configuration-file.md#raft-engine)参照してください。  |
| ティクブ            | [`backup.enable-auto-tune`](/tikv-configuration-file.md#enable-auto-tune-new-in-v540)                           | 新しく追加された | バージョン5.3.0では、デフォルト値は`false`です。バージョン5.4.0以降では、デフォルト値は`true`に変更されました。このパラメータは、クラスターリソースの使用率が高い場合に、バックアップタスクで使用されるリソースを制限することでクラスターへの影響を軽減するかどうかを制御します。デフォルト設定では、バックアップタスクの速度が低下する可能性があります。                                                                                                                       |
| ティクブ            | `log-level` `log-format` `log-file` `log-rotation-size`                                                         | 修正済み     | TiKVログパラメータの名前は、TiDBログパラメータと一致する名前`log.file.filename` `log.level` `log.enable-timestamp`に置き換えられます。古いパラメータのみを設定し、その値をデフォルト以外の値に設定した場合、古いパラメータは新しいパラメータと互換性を保ちます。古いパラメータと新しいパラメータの両方を設定した場合、新しいパラメータ`log.format`有効になります。詳細については、 [TiKVコンフィグレーションファイル - ログ](/tikv-configuration-file.md#log-new-in-v540)参照してください。 |
| ティクブ            | `log-rotation-timespan`                                                                                         | 削除済み     | ログローテーションの間隔。この期間が経過すると、ログファイルがローテーションされます。つまり、現在のログファイルのファイル名にタイムスタンプが追加され、新しいログファイルが作成されます。                                                                                                                                                                                                                  |
| TiKV            | `allow-remove-leader`                                                                                           | 削除済み     | メインスイッチの削除を許可するかどうかを決定します。                                                                                                                                                                                                                                                                                     |
| TiKV            | `raft-msg-flush-interval`                                                                                       | 削除済み     | Raftメッセージをバッチ送信する間隔を指定します。Raft メッセージは、この設定項目で指定された間隔ごとにRaft送信されます。                                                                                                                                                                                                                                             |
| PD              | [`log.level`](/pd-configuration-file.md#level)                                                                  | 修正済み     | デフォルト値は「INFO」から「info」に変更され、大文字と小文字が区別されないことが保証されます。                                                                                                                                                                                                                                                            |
| TiFlash         | [`profile.default.enable_elastic_threadpool`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file) | 新しく追加された | エラスティックスレッドプール機能を有効または無効にするかどうかを決定します。この設定項目を有効にすると、同時実行性の高いシナリオにおいてTiFlashのCPU使用率が大幅に向上します。デフォルト値は`false`です。                                                                                                                                                                                                  |
| TiFlash         | [`storage.format_version`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                    | 新しく追加された | DTFileのバージョンを指定します。デフォルト値は`2`で、ハッシュがデータファイルに埋め込まれます。値を`3`に設定することもできます。 `3`の場合、データファイルにはメタデータとトークンデータのチェックサムが含まれ、複数のハッシュアルゴリズムがサポートされます。                                                                                                                                                                        |
| TiFlash         | [`logger.count`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                              | 修正済み     | デフォルト値は`10`に変更されます。                                                                                                                                                                                                                                                                                            |
| TiFlash         | [`status.metrics_port`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                       | 修正済み     | デフォルト値は`8234`に変更されます。                                                                                                                                                                                                                                                                                          |
| TiFlash         | [`raftstore.apply-pool-size`](/tiflash/tiflash-configuration.md#configure-the-tiflash-learnertoml-file)         | 新しく追加された | Raftデータをstorageにフラッシュするプール内のスレッドの許容数。デフォルト値は`4`です。                                                                                                                                                                                                                                                             |
| TiFlash         | [`raftstore.store-pool-size`](/tiflash/tiflash-configuration.md#configure-the-tiflash-learnertoml-file)         | 新しく追加された | Raftを処理するスレッドの許容数。これはRaftstoreスレッドプールのサイズです。デフォルト値は`4`です。                                                                                                                                                                                                                                                      |
| TiDB データ移行 (DM) | [`collation_compatible`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)         | 新しく追加された | `CREATE` SQL文のデフォルトの照合照合順序を同期するモード。値のオプションは「loose」（デフォルト）と「strict」です。                                                                                                                                                                                                                                          |
| TiCDC           | `max-message-bytes`                                                                                             | 修正済み     | Kafkaシンクのデフォルト値`max-message-bytes`を`104857601` （10MB）に変更します。                                                                                                                                                                                                                                                   |
| TiCDC           | `partition-num`                                                                                                 | 修正済み     | Kafka Sink のデフォルト値`partition-num`を`4`から`3`に変更します。これにより、TiCDC は Kafaka パーティションにメッセージをより均等に送信するようになります。                                                                                                                                                                                                          |
| TiDB Lightning  | `meta-schema-name`                                                                                              | 修正済み     | ターゲットTiDB内のメタデータのスキーマ名を指定します。v5.4.0以降では、 [並行輸入](/tidb-lightning/tidb-lightning-distributed-import.md) （対応するパラメータは`tikv-importer.incremental-import = true` ）を有効にした場合にのみこのスキーマが作成されます。                                                                                                                          |
| TiDB Lightning  | `task-info-schema-name`                                                                                         | 新しく追加された | TiDB Lightningが競合を検出した際に重複データを保存するデータベース名を指定します。デフォルトの値は「lightning_task_info」です。このパラメータは、「duplicate-resolution」機能を有効にした場合にのみ指定してください。                                                                                                                                                                          |
| TiDB Lightning  | `incremental-import`                                                                                            | 新しく追加された | 既にデータが存在するテーブルへのデータのインポートを許可するかどうかを決定します。デフォルト値は`false`です。                                                                                                                                                                                                                                                     |

### その他 {#others}

-   TiDBとPDの間にインターフェースが追加されました。1システムテーブル`information_schema.TIDB_HOT_REGIONS_HISTORY`使用する場合、TiDBは対応するバージョンのPDを使用する必要があります。
-   TiDBサーバー、PDサーバー、およびTiKVサーバーは、ログ名、出力形式、ローテーションおよび有効期限のルールを管理するために、ログ関連パラメータに統一された命名方法を使用します。詳細については、 [TiKV 構成ファイル - ログ](/tikv-configuration-file.md#log-new-in-v540)参照してください。
-   バージョン5.4.0以降、プランキャッシュによってキャッシュされた実行プランに対してSQLバインディングを作成すると、そのバインディングによって、対応するクエリに対して既にキャッシュされているプラ​​ンが無効化されます。新しいバインディングは、バージョン5.4.0より前にキャッシュされた実行プランには影響しません。
-   v5.3以前のバージョンでは、 [TiDB データ移行 (DM)](https://docs.pingcap.com/tidb-data-migration/v5.3/)ドキュメントはTiDBのドキュメントとは独立していました。v5.4以降、DMのドキュメントはTiDBのドキュメントに統合され、同じバージョンのDMドキュメントサイトにアクセスすることなく、 [DMドキュメント](/dm/dm-overview.md)直接読むことができます。
-   cdclog とともに、実験的機能である Point-in-time Recovery (PITR) を削除しました。v5.4.0 以降、cdclog ベースの PITR と cdclog はサポートされなくなりました。
-   システム変数を「DEFAULT」に設定する動作をMySQLとより互換性のあるものにする[＃29680](https://github.com/pingcap/tidb/pull/29680)
-   システム変数`lc_time_names`読み取り専用[＃30084](https://github.com/pingcap/tidb/pull/30084)に設定する
-   `tidb_store_limit`のスコープをINSTANCEまたはGLOBALからGLOBAL [＃30756](https://github.com/pingcap/tidb/pull/30756)に設定する
-   列にゼロが含まれている場合、整数型列を時間型列に変換することを禁止します[＃25728](https://github.com/pingcap/tidb/pull/25728)
-   浮動小数点値[＃30148](https://github.com/pingcap/tidb/pull/30148)を挿入するときに`Inf`または`NAN`値に対してエラーが報告されない問題を修正しました
-   自動IDが範囲外の場合に`REPLACE`文が他の行を誤って変更する問題を修正[＃30301](https://github.com/pingcap/tidb/pull/30301)

## 新機能 {#new-features}

### SQL {#sql}

-   **TiDBはv5.4.0以降、GBK文字セットをサポートしています。**

    v5.4.0 より前では、 TiDB は`ascii` 、 `binary` 、 `latin1` 、 `utf8` 、および`utf8mb4`文字セットをサポートしています。

    中国語ユーザーへのサポートを強化するため、TiDBはv5.4.0以降、GBK文字セットをサポートしています。TiDBクラスタを初めて初期化する際に、TiDB構成ファイルで[`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap)オプションを有効にすると、TiDB GBK文字セットは`gbk_bin`と`gbk_chinese_ci`両方の照合順序をサポートします。

    GBK文字セットを使用する場合は、互換性の制限に注意する必要があります。詳細については[文字セットと照合順序 - GBK](/character-set-gbk.md)参照してください。

### Security {#security}

-   **TiSparkはユーザー認証と承認をサポートします**

    TiSpark 2.5.0以降、TiSparkはデータベースユーザー認証と、データベースレベルまたはテーブルレベルの読み取り/書き込み権限の両方をサポートしています。この機能を有効にすると、データ取得のための描画などの不正なバッチタスクの実行を防止でき、オンラインクラスターの安定性とデータセキュリティが向上します。

    この機能はデフォルトで無効になっています。有効にすると、TiSpark を介して操作するユーザーに必要な権限がない場合、TiSpark から例外が発行されます。

    [ユーザードキュメント](https://docs.pingcap.com/tidb/v5.4/tispark-overview#security)

-   **TiUPはルートユーザーの初期パスワードの生成をサポートしています**

    クラスタ起動コマンドにパラメータ`--init`が導入されました。このパラメータにより、 TiUPを使用してデプロイされた TiDB クラスタでは、 TiUP がデータベースの root ユーザーに対して強力な初期パスワードを生成します。これにより、空のパスワードを持つ root ユーザーを使用することによるセキュリティリスクを回避し、データベースのセキュリティを確保します。

    [ユーザードキュメント](/production-deployment-using-tiup.md#step-7-start-a-tidb-cluster)

### パフォーマンス {#performance}

-   **列指向storageエンジンTiFlashとコンピューティングエンジンMPPの安定性とパフォーマンスを継続的に向上**

    -   より多くの関数をMPP エンジンにプッシュダウンすることをサポートします。

        -   `STRCMP()` `RPAD()`関数: `LPAD()`
        -   `QUARTER()`関数`SUBDATE(string, real)` `ADDDATE(string, real)` `DATE_ADD(string, real)` `DATE_SUB(string, real)`

    -   リソース利用率を向上させるためにエラスティック スレッド プール機能を導入します (実験的)

    -   TiKVからデータを複製する際に、行ベースのstorage形式から列ベースのstorage形式にデータを変換する効率を改善し、データ複製の全体的なパフォーマンスを50％向上させます。

    -   一部の設定項目のデフォルト値を調整することで、 TiFlash のパフォーマンスと安定性が向上します。HTAP ハイブリッドロードでは、単一テーブルに対する単純なクエリのパフォーマンスが最大 20% 向上します。

    ユーザー[tiflash.tomlファイルを設定する](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file) : [プッシュダウン計算をサポート](/tiflash/tiflash-supported-pushdown-calculations.md)

-   **セッション変数を通じて指定された時間範囲内の履歴データを読み取る**

    TiDBは、 Raftコンセンサスアルゴリズムに基づくマルチレプリカ分散データベースです。高同時実行性と高スループットが求められるアプリケーションシナリオにおいて、TiDBはフォロワーレプリカを通じて読み取りパフォーマンスをスケールアウトし、読み取りリクエストと書き込みリクエストを分離します。

    TiDBは、様々なアプリケーションシナリオに対応できるよう、フォロワー読み取りモードとして、強力な一貫性のある読み取りと弱い一貫性のある履歴読み取りの2つのモードを提供しています。強力な一貫性のある読み取りモードは、リアルタイムデータを必要とするアプリケーションシナリオに適しています。ただし、このモードでは、リーダーとフォロワー間のデータレプリケーションのレイテンシーとスループットの低下により、特に地理的に分散したデプロイメントでは、読み取りリクエストのレイテンシーが大きくなる可能性があります。

    リアルタイムデータに対する要件がそれほど厳しくないアプリケーションシナリオでは、履歴読み取りモードが推奨されます。このモードはレイテンシーを短縮し、スループットを向上させることができます。TiDBは現在、以下の方法による履歴データの読み取りをサポートしています。SQL文を使用して過去の時点からデータを読み取るか、過去の時点に基づいて読み取り専用トランザクションを開始するかです。どちらの方法でも、特定の時点または指定された時間範囲内の履歴データの読み取りがサポートされています。詳細については、 [`AS OF TIMESTAMP`句を使用して履歴データを読み取る](/as-of-timestamp.md)を参照してください。

    v5.4.0以降、TiDBはセッション変数を介して指定された時間範囲内の履歴データの読み取りをサポートすることで、履歴読み取りモードの使いやすさを向上させました。このモードは、準リアルタイムシナリオにおいて、低レイテンシかつ高スループットの読み取りリクエストに対応します。変数は以下のように設定できます。

    ```sql
    set @@tidb_replica_read=leader_and_follower
    set @@tidb_read_staleness="-5"
    ```

    この設定により、TiDB は最も近いリーダー ノードまたはフォロワー ノードを選択し、5 秒以内に最新の履歴データを読み取ることができます。

    [ユーザードキュメント](/tidb-read-staleness.md)

-   **インデックス統合の GA**

    インデックスマージは、TiDB v4.0でSQL最適化のための実験的機能として導入されました。この手法は、クエリで複数列のデータのスキャンが必要な場合の条件フィルタリングを大幅に高速化します。次のクエリを例に挙げましょう。1 `WHERE`のステートメントで、 `OR`で接続されたフィルタリング条件がそれぞれ列*key1*と*key2*にインデックスを持っている場合、インデックスマージ機能はそれぞれのインデックスを同時にフィルタリングし、クエリ結果をマージして、マージされた結果を返します。

    ```sql
    SELECT * FROM table WHERE key1 <= 100 OR key2 = 200;
    ```

    TiDB v4.0より前のバージョンでは、テーブルに対するクエリは、フィルタリングに一度に1つのインデックスのみを使用できます。複数の列のデータをクエリする場合は、インデックスマージを有効にすると、個々の列のインデックスを使用して、短時間で正確なクエリ結果を取得できます。インデックスマージにより、不要なテーブル全体のスキャンが回避され、多数の複合インデックスを作成する必要がなくなります。

    バージョン5.4.0では、インデックスマージがGAになります。ただし、以下の制限事項にご注意ください。

    -   インデックスマージは、選言正規形（X <sub>1</sub> ⋁ X <sub>2</sub> ⋁ …X <sub>n</sub> ）のみをサポートします。つまり、この機能は、 `WHERE`の節内のフィルタリング条件が`OR`の節で連結されている場合にのみ機能します。

    -   新規にデプロイされたv5.4.0以降のTiDBクラスターでは、この機能はデフォルトで有効になっています。以前のバージョンからアップグレードされたv5.4.0以降のTiDBクラスターでは、この機能はアップグレード前の設定を継承し、必要に応じて設定を変更できます（v4.0より前のTiDBクラスターではこの機能は存在せず、デフォルトで無効になっています）。

    [ユーザードキュメント](/explain-index-merge.md)

-   **Raft Engineのサポート (実験的)**

    TiKVのログstorageエンジンとして[Raft Engine](https://github.com/tikv/raft-engine)使用をサポートします。RocksDBと比較して、 Raft EngineはTiKVのI/O書き込みトラフィックを最大40%、CPU使用率を10%削減し、フォアグラウンドスループットを約5%向上させ、特定の負荷条件下でテールレイテンシーを20%削減します。さらに、 Raft Engineはログリサイクルの効率を向上させ、過酷な条件下でのログ蓄積の問題を修正します。

    Raft Engineはまだ実験的機能であり、デフォルトでは無効になっています。v5.4.0のRaft Engineのデータ形式は以前のバージョンと互換性がありませんのでご注意ください。クラスターをアップグレードする前に、すべてのTiKVノードでRaft Engineが無効になっていることを確認してください。RaftRaft Engineはv5.4.0以降のバージョンでのみ使用することをお勧めします。

    [ユーザードキュメント](/tikv-configuration-file.md#raft-engine)

-   **`PREDICATE COLUMNS`の統計収集をサポート (実験的)**

    ほとんどの場合、SQL文を実行する際、オプティマイザは一部の列（例えば、文中の`WHERE` 、 `JOIN` 、 `ORDER BY` 、 `GROUP BY`列）の統計情報のみを使用します。これらの使用される列は`PREDICATE COLUMNS`呼ばれます。

    v5.4.0 以降では、 [`tidb_enable_column_tracking`](/system-variables.md#tidb_enable_column_tracking-new-in-v540)システム変数の値を`ON`に設定して、TiDB が`PREDICATE COLUMNS`収集できるようにすることができます。

    設定後、TiDBは100 * [`stats-lease`](/tidb-configuration-file.md#stats-lease)ごとに`PREDICATE COLUMNS`情報を`mysql.column_stats_usage`のシステムテーブルに書き込みます。ビジネスのクエリパターンが安定している場合は、 `ANALYZE TABLE TableName PREDICATE COLUMNS`構文を使用して`PREDICATE COLUMNS`番目の列のみの統計情報を収集することで、統計収集のオーバーヘッドを大幅に削減できます。

    [ユーザードキュメント](/statistics.md#collect-statistics-on-some-columns)

-   **統計情報の同期読み込みをサポート（実験的）**

    v5.4.0以降、TiDBは統計情報の同期ロード機能を導入しました。この機能はデフォルトでは無効になっています。この機能を有効にすると、SQL文の実行時に、TiDBはヒストグラム、TopN、Count-Min Sketch統計などの大規模な統計情報をメモリに同期ロードできるようになります。これにより、SQL最適化における統計情報の完全性が向上します。

    [ユーザードキュメント](/statistics.md#load-statistics)

### 安定性 {#stability}

-   **永続的なANALYZE構成をサポート**

    統計は、オプティマイザが実行計画を生成する際に参照する基本情報の一種です。統計の精度は、生成される実行計画の妥当性に直接影響します。統計の精度を確保するためには、テーブル、パーティション、インデックスごとに異なる収集設定を設定する必要がある場合があります。

    v5.4.0以降、TiDBはいくつか`ANALYZE`設定の永続化をサポートしています。この機能により、既存の設定を将来の統計収集に簡単に再利用できます。

    `ANALYZE`設定の永続化機能はデフォルトで有効になっています（システム変数`tidb_analyze_version`はデフォルトで`2` [`tidb_persist_analyze_options`](/system-variables.md#tidb_persist_analyze_options-new-in-v540)デフォルトで`ON`です）。この機能を使用すると、 `ANALYZE`文を手動で実行する際に、その文で指定された永続化設定を記録できます。記録されると、次回 TiDB が統計を自動的に更新するとき、またはこれらの設定を指定せずに手動で統計を収集するときに、TiDB は記録された設定に従って統計を収集します。

    [ユーザードキュメント](/statistics.md#persist-analyze-configurations)

### 高可用性と災害復旧 {#high-availability-and-disaster-recovery}

-   **クラスタへのバックアップタスクの影響を軽減する**

    バックアップと復元（BR）では、自動チューニング機能（デフォルトで有効）が導入されています。この機能は、クラスターリソースの使用状況を監視し、バックアップタスクで使用されるスレッド数を調整することで、バックアップタスクがクラスターに与える影響を軽減します。場合によっては、バックアップ用のクラスターハードウェアリソースを増やし、自動チューニング機能を有効にすると、バックアップタスクがクラスターに与える影響を10%以下に抑えることができます。

    [ユーザードキュメント](/br/br-auto-tune.md)

-   **バックアップのターゲットstorageとして Azure Blob Storage をサポート**

    バックアップと復元（BR）は、リモートバックアップstorageとしてAzure Blob Storageをサポートしています。Azure CloudにTiDBをデプロイすると、クラスターデータをAzure Blob Storageサービスにバックアップできるようになります。

    [ユーザードキュメント](/br/backup-and-restore-storages.md)

### データ移行 {#data-migration}

-   **TiDB Lightningは、データを含むテーブルへのデータのインポートを許可するかどうかを決定する新しい機能を導入しました。**

    TiDB Lightning、設定項目`incremental-import`が導入されました。これは、データが存在するテーブルへのデータのインポートを許可するかどうかを決定します。デフォルト値は`false`です。並列インポートモードを使用する場合は、設定を`true`に設定する必要があります。

    [ユーザードキュメント](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)

-   **TiDB Lightningは並列インポートのメタ情報を格納するスキーマ名を導入します**

    TiDB Lightning、 `meta-schema-name`設定項目が導入されています。並列インポートモードにおいて、このパラメータは、ターゲットクラスタ内の各TiDB Lightningインスタンスのメタ情報を格納するスキーマ名を指定します。デフォルトの値は「lightning_metadata」です。このパラメータに設定される値は、同じ並列インポートに参加する各TiDB Lightningインスタンスで同じである必要があります。そうでない場合、インポートされたデータの正確性は保証されません。

    [ユーザードキュメント](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)

-   **TiDB Lightningは重複解決を導入**

    ローカルバックエンドモードでは、 TiDB Lightningはデータのインポートが完了する前に重複データを出力し、その後データベースから重複データを削除します。インポート完了後に重複データを解決し、アプリケーションルールに従って適切なデータを選択して挿入することができます。後続の増分データ移行フェーズで重複データが発生することを防ぐため、重複データに基づいて上流のデータソースをクリーンアップすることをお勧めします。

    [ユーザードキュメント](/tidb-lightning/tidb-lightning-error-resolution.md)

-   **TiDB データ移行 (DM) におけるリレー ログの使用を最適化します。**

    -   `source`構成内の`enable-relay`スイッチを回復します。

    -   `start-relay`および`stop-relay`コマンドを使用してリレー ログを動的に有効化および無効化することをサポートします。

    -   リレー ログのステータスを`source`にバインドします。3 `source`任意の DM ワーカーに移行された後も、有効または無効の元のステータスを維持します。

    -   リレー ログのstorageパスを DM-worker 構成ファイルに移動します。

    [ユーザードキュメント](/dm/relay-log.md)

-   **DMにおける<a href="/character-set-and-collation.md">照合順序</a>処理の最適化**

    設定項目を`collation_compatible`追加します。値のオプションは`loose` （デフォルト）と`strict`です。

    -   アプリケーションに照合順序に関する厳密な要件がなく、クエリ結果の照合順序がアップストリームとダウンストリームで異なる可能性がある場合は、デフォルトの`loose`モードを使用してエラーの報告を回避できます。
    -   アプリケーションで照合順序に関する厳格な要件があり、上流と下流の照合順序が一貫している必要がある場合は、モード`strict`を使用できます。ただし、下流が上流のデフォルトの照合順序をサポートしていない場合、データレプリケーションでエラーが発生する可能性があります。

    [ユーザードキュメント](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)

-   **DM の`transfer source`を最適化して、レプリケーション タスクをスムーズに実行できるようにします。**

    DMワーカーノードの負荷が不均衡な場合、コマンド`transfer source`を使用して、 `source`の設定を別の負荷に手動で転送できます。最適化後、コマンド`transfer source`によって手動操作が簡素化されます。DMは他の操作を内部的に完了するため、関連するすべてのタスクを一時停止することなく、ソースをスムーズに転送できます。

-   **DM OpenAPI が一般公開 (GA) されました**

    DMは、データソースの追加やタスク管理など、APIを介した日常的な管理をサポートします。バージョン5.4.0では、DM OpenAPIがGAになります。

    [ユーザードキュメント](/dm/dm-open-api.md)

### 診断効率 {#diagnostic-efficiency}

-   **Top SQL （実験的機能）**

    ソースを消費するクエリを簡単に見つけられるように、新しい実験的機能であるTop SQL (デフォルトでは無効) が導入されました。

    [ユーザードキュメント](/dashboard/top-sql.md)

### TiDBデータ共有サブスクリプション {#tidb-data-share-subscription}

-   **TiCDC のクラスターへの影響を最適化する**

    TiCDC を使用すると、TiDB クラスターのパフォーマンスへの影響が大幅に軽減されます。テスト環境では、TiCDC が TiDB に及ぼすパフォーマンスへの影響を 5% 未満に抑えることができました。

### 展開と保守 {#deployment-and-maintenance}

-   **継続的なプロファイリングの強化（実験的）**

    -   サポートされるコンポーネントの追加: TiDB、PD、TiKV に加えて、TiDB v5.4.0 はTiFlashの CPU プロファイリングもサポートします。

    -   より多くの形式のプロファイリング表示: フレーム チャート上での CPU プロファイリングと Goroutine の結果の表示をサポートします。

    -   より多くのデプロイメント環境がサポートされます: 継続的なプロファイリングは、 TiDB Operatorを使用してデプロイされたクラスターでも使用できます。

    継続的なプロファイリングはデフォルトで無効になっていますが、TiDB ダッシュボードで有効にすることができます。

    継続的なプロファイリングは、 TiUP v1.9.0 以降またはTiDB Operator v1.3.0 以降を使用してデプロイまたはアップグレードされたクラスターに適用できます。

    [ユーザードキュメント](/dashboard/continuous-profiling.md)

## 改善点 {#improvements}

-   ティドブ

    -   キャッシュされたクエリプランをクリアするための`ADMIN {SESSION | INSTANCE | GLOBAL} PLAN_CACHE`構文をサポートする[＃30370](https://github.com/pingcap/tidb/pull/30370)

-   TiKV

    -   コプロセッサーは、ストリームのような方法でリクエストを処理するためのページングAPIをサポートしています[＃11448](https://github.com/tikv/tikv/issues/11448)
    -   読み取り操作で二次ロックが解決されるのを待つ必要がないように`read-through-lock`サポートする[＃11402](https://github.com/tikv/tikv/issues/11402)
    -   ディスク領域の枯渇によるpanicを回避するためにディスク保護メカニズムを追加する[＃10537](https://github.com/tikv/tikv/issues/10537)
    -   ログのアーカイブとローテーションをサポート[＃11651](https://github.com/tikv/tikv/issues/11651)
    -   Raftクライアントによるシステムコールを減らしCPU効率を上げる[＃11309](https://github.com/tikv/tikv/issues/11309)
    -   コプロセッサーはTiKV [＃11495](https://github.com/tikv/tikv/issues/11495)への部分文字列のプッシュダウンをサポートします
    -   読み取りコミット分離レベル[＃11485](https://github.com/tikv/tikv/issues/11485)でロックの読み取りをスキップすることでスキャンパフォーマンスを向上します。
    -   バックアップ操作で使用されるデフォルトのスレッドプールのサイズを減らし、負荷が高いときにスレッドプールの使用を制限します[＃11000](https://github.com/tikv/tikv/issues/11000)
    -   Apply スレッド プールと Store スレッド プールのサイズを動的に調整する機能をサポート[＃11159](https://github.com/tikv/tikv/issues/11159)
    -   `snap-generator`スレッドプール[＃11247](https://github.com/tikv/tikv/issues/11247)のサイズ設定をサポート
    -   頻繁に読み書きが行われるファイルが多数ある場合に発生するグローバルロック競合の問題を最適化します[＃250](https://github.com/tikv/rocksdb/pull/250)

-   PD

    -   デフォルトで過去のホットスポット情報を記録する[＃25281](https://github.com/pingcap/tidb/issues/25281)
    -   リクエストソースを識別するためのHTTPコンポーネントの署名を追加する[＃4490](https://github.com/tikv/pd/issues/4490)
    -   TiDBダッシュボードをv2021.12.31 [＃4257](https://github.com/tikv/pd/issues/4257)に更新

-   TiFlash

    -   現地オペレーターのコミュニケーションを最適化する
    -   gRPC の非一時的スレッド数を増やして、スレッドの頻繁な作成や破棄を回避する

-   ツール

    -   バックアップと復元 (BR)

        -   BRが暗号化バックアップ[＃29794](https://github.com/pingcap/tidb/issues/29794)を実行するときにキーの有効性チェックを追加する

    -   TiCDC

        -   「EventFeed再試行レート制限」ログの数を減らす[＃4006](https://github.com/pingcap/tiflow/issues/4006)
        -   多数のテーブルを複製する際のレプリケーションのレイテンシーを削減する[＃3900](https://github.com/pingcap/tiflow/issues/3900)
        -   TiKVストアがダウンしたときにKVクライアントが回復するまでの時間を短縮する[＃3191](https://github.com/pingcap/tiflow/issues/3191)

    -   TiDB データ移行 (DM)

        -   リレー有効時のCPU使用率を下げる[＃2214](https://github.com/pingcap/dm/issues/2214)

    -   TiDB Lightning

        -   TiDBバックエンドモード[＃30953](https://github.com/pingcap/tidb/pull/30953)でのパフォーマンスを向上させるために、デフォルトで楽観的トランザクションを使用してデータを書き込む

    -   Dumpling

        -   Dumpling がデータベース バージョン[＃29500](https://github.com/pingcap/tidb/pull/29500)をチェックする際の互換性を向上
        -   `CREATE DATABASE`と`CREATE TABLE`ダンプするときにデフォルトの照合順序を追加する[＃3420](https://github.com/pingcap/tiflow/issues/3420)

## バグ修正 {#bug-fixes}

-   ティドブ

    -   クラスターをv4.xからv5.xにアップグレードするときに発生する`tidb_analyze_version`値の変更の問題を修正しました[＃25422](https://github.com/pingcap/tidb/issues/25422)
    -   サブクエリ[＃30748](https://github.com/pingcap/tidb/issues/30748)で異なる照合順序を使用した場合に誤った結果が発生する問題を修正しました
    -   TiDBの`concat(ifnull(time(3))`の結果がMySQL [＃29498](https://github.com/pingcap/tidb/issues/29498)の結果と異なる問題を修正
    -   楽観的トランザクションモード[＃30410](https://github.com/pingcap/tidb/issues/30410)で潜在的なデータインデックスの不整合が発生する問題を修正
    -   式を TiKV [＃30200](https://github.com/pingcap/tidb/issues/30200)にプッシュダウンできない場合に IndexMerge のクエリ実行プランが間違っている問題を修正しました
    -   同時列型変更によりスキーマとデータの間に不整合が発生する問題を修正[＃31048](https://github.com/pingcap/tidb/issues/31048)
    -   サブクエリ[＃30913](https://github.com/pingcap/tidb/issues/30913)がある場合にIndexMergeクエリの結果が間違っている問題を修正
    -   クライアント[＃30896](https://github.com/pingcap/tidb/issues/30896)でFetchSizeが大きすぎる値に設定されている場合に発生するpanic問題を修正しました
    -   LEFT JOIN が誤って INNER JOIN [＃20510](https://github.com/pingcap/tidb/issues/20510)に変換される可能性がある問題を修正しました
    -   `CASE-WHEN`式と照合順序を一緒に使用するとpanicが発生する可能性がある問題を修正[＃30245](https://github.com/pingcap/tidb/issues/30245)
    -   `IN`値にバイナリ定数[＃31261](https://github.com/pingcap/tidb/issues/31261)が含まれている場合に発生する誤ったクエリ結果の問題を修正しました
    -   CTE にサブクエリ[＃31255](https://github.com/pingcap/tidb/issues/31255)がある場合に発生する誤ったクエリ結果の問題を修正しました
    -   `INSERT ... SELECT ... ON DUPLICATE KEY UPDATE`文を実行するとpanic[＃28078](https://github.com/pingcap/tidb/issues/28078)が発生する問題を修正しました
    -   INDEX HASH JOINが`send on closed channel`エラーを返す問題を修正しました[＃31129](https://github.com/pingcap/tidb/issues/31129)

-   TiKV

    -   MVCC削除レコードがGC [＃11217](https://github.com/tikv/tikv/issues/11217)によってクリアされない問題を修正
    -   悲観的トランザクションモードで事前書き込み要求を再試行すると、まれにデータの不整合が発生するリスクがある問題を修正しました[＃11187](https://github.com/tikv/tikv/issues/11187)
    -   GCスキャンによってメモリオーバーフローが発生する問題を修正[＃11410](https://github.com/tikv/tikv/issues/11410)
    -   ディスク容量がいっぱいのときにRocksDBのフラッシュまたは圧縮によってpanicが発生する問題を修正しました[＃11224](https://github.com/tikv/tikv/issues/11224)

-   PD

    -   リージョン統計が`flow-round-by-digit` [＃4295](https://github.com/tikv/pd/issues/4295)の影響を受けない問題を修正
    -   ターゲットストアがダウンしているため、スケジュールオペレータがフェイルファストを実行できない問題を修正しました[＃3353](https://github.com/tikv/pd/issues/3353)
    -   オフラインストアの地域を統合できない問題を修正[＃4119](https://github.com/tikv/pd/issues/4119)
    -   ホットスポット統計からコールドホットスポットデータを削除できない問題を修正[＃4390](https://github.com/tikv/pd/issues/4390)

-   TiFlash

    -   MPPクエリが停止したときにTiFlashがpanicになる可能性がある問題を修正しました
    -   `where <string>`句を含むクエリが間違った結果を返す問題を修正しました
    -   整数主キーの列タイプをより広い範囲に設定すると発生する可能性のあるデータの不整合の問題を修正しました。
    -   入力時間が1970-01-01 00:00:01 UTCより前の場合、 `unix_timestamp`の動作がTiDBまたはMySQLの動作と一致しない問題を修正しました。
    -   TiFlash が再起動後に`EstablishMPPConnection`エラーを返す可能性がある問題を修正しました
    -   `CastStringAsDecimal` TiFlashとTiDB/TiKVの動作が一致しない問題を修正
    -   クエリ結果に`DB::Exception: Encode type of coprocessor response is not CHBlock`エラーが返される問題を修正しました
    -   `castStringAsReal` TiFlashとTiDB/TiKVの動作が一致しない問題を修正
    -   TiFlashの`date_add_string_xxx`関数の返された結果がMySQLの結果と一致しない問題を修正しました

-   ツール

    -   バックアップと復元 (BR)

        -   復元操作が完了した後にリージョンの配分が不均一になる可能性がある問題を修正[＃30425](https://github.com/pingcap/tidb/issues/30425)
        -   バックアップstorage[＃30104](https://github.com/pingcap/tidb/issues/30104)として`minio`が使用されている場合、エンドポイントに`'/'`指定できない問題を修正
        -   システムテーブルを同時にバックアップするとテーブル名の更新に失敗し、システムテーブルを復元できない問題を修正しました[＃29710](https://github.com/pingcap/tidb/issues/29710)

    -   TiCDC

        -   `min.insync.replicas`が`replication-factor`より小さい場合にレプリケーションを実行できない問題を修正しました[＃3994](https://github.com/pingcap/tiflow/issues/3994)
        -   `cached region`監視メトリックがマイナス[＃4300](https://github.com/pingcap/tiflow/issues/4300)になる問題を修正
        -   `mq sink write row`監視データがない問題を修正[＃3431](https://github.com/pingcap/tiflow/issues/3431)
        -   `sql mode` [＃3810](https://github.com/pingcap/tiflow/issues/3810)の互換性の問題を修正
        -   レプリケーションタスクが削除されたときに発生する可能性のあるpanic問題を修正[＃3128](https://github.com/pingcap/tiflow/issues/3128)
        -   デフォルトの列値[＃3929](https://github.com/pingcap/tiflow/issues/3929)を出力するときに発生するpanicとデータの不整合の問題を修正しました
        -   デフォルト値を複製できない問題を修正[＃3793](https://github.com/pingcap/tiflow/issues/3793)
        -   デッドロックによりレプリケーションタスクが停止する可能性がある問題を修正[＃4055](https://github.com/pingcap/tiflow/issues/4055)
        -   ディスクが完全に書き込まれたときにログが出力されない問題を修正[＃3362](https://github.com/pingcap/tiflow/issues/3362)
        -   DDL文の特別なコメントによりレプリケーションタスクが停止する問題を修正[＃3755](https://github.com/pingcap/tiflow/issues/3755)
        -   RHELリリース[＃3584](https://github.com/pingcap/tiflow/issues/3584)のタイムゾーンの問題によりサービスを開始できない問題を修正しました
        -   不正確なチェックポイント[＃3545](https://github.com/pingcap/tiflow/issues/3545)によって発生する可能性のあるデータ損失の問題を修正しました
        -   コンテナ環境[＃1798](https://github.com/pingcap/tiflow/issues/1798)のOOM問題を修正
        -   `config.Metadata.Timeout` [＃3352](https://github.com/pingcap/tiflow/issues/3352)の誤った構成によって発生するレプリケーション停止の問題を修正しました

    -   TiDB データ移行 (DM)

        -   `CREATE VIEW`文がデータレプリケーション[＃4173](https://github.com/pingcap/tiflow/issues/4173)を中断する問題を修正
        -   DDL文をスキップした後にスキーマをリセットする必要がある問題を修正[＃4177](https://github.com/pingcap/tiflow/issues/4177)
        -   DDL文がスキップされた後にテーブルチェックポイントが時間内に更新されない問題を修正[＃4184](https://github.com/pingcap/tiflow/issues/4184)
        -   TiDBバージョンとパーサーバージョン[＃4298](https://github.com/pingcap/tiflow/issues/4298)の互換性の問題を修正
        -   ステータス[＃4281](https://github.com/pingcap/tiflow/issues/4281)を照会するときにのみ同期メトリックが更新される問題を修正しました

    -   TiDB Lightning

        -   TiDB Lightningが`mysql.tidb`テーブル[＃31088](https://github.com/pingcap/tidb/issues/31088)にアクセスする権限を持っていない場合に発生する間違ったインポート結果の問題を修正しました。
        -   TiDB Lightning の再起動時に一部のチェックがスキップされる問題を修正[＃30772](https://github.com/pingcap/tidb/issues/30772)
        -   S3パスが存在しない場合にTiDB Lightningがエラーを報告できない問題を修正しました[＃30674](https://github.com/pingcap/tidb/pull/30674)

    -   TiDBBinlog

        -   `CREATE PLACEMENT POLICY`ステートメント[＃1118](https://github.com/pingcap/tidb-binlog/issues/1118)と互換性がないため、 Drainer が失敗する問題を修正しました。
