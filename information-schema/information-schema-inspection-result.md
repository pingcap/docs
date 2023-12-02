---
title: INSPECTION_RESULT
summary: Learn the `INSPECTION_RESULT` diagnostic result table.
---

# 検査結果 {#inspection-result}

TiDB には、システム内の障害や隠れた問題を検出するためのいくつかの組み込み診断ルールがあります。

`INSPECTION_RESULT`診断テーブルは、問題を迅速に発見し、反復的な手動作業を軽減するのに役立ちます。 `select * from information_schema.inspection_result`ステートメントを使用して内部診断をトリガーできます。

> **注記：**
>
> このテーブルは TiDB セルフホスト型にのみ適用され、 [TiDB Cloud](https://docs.pingcap.com/tidbcloud/)では利用できません。

`information_schema.inspection_result`診断結果テーブル`information_schema.inspection_result`の構造は次のとおりです。

```sql
USE information_schema;
DESC inspection_result;
```

```sql
+----------------+--------------+------+------+---------+-------+
| Field          | Type         | Null | Key  | Default | Extra |
+----------------+--------------+------+------+---------+-------+
| RULE           | varchar(64)  | YES  |      | NULL    |       |
| ITEM           | varchar(64)  | YES  |      | NULL    |       |
| TYPE           | varchar(64)  | YES  |      | NULL    |       |
| INSTANCE       | varchar(64)  | YES  |      | NULL    |       |
| STATUS_ADDRESS | varchar(64)  | YES  |      | NULL    |       |
| VALUE          | varchar(64)  | YES  |      | NULL    |       |
| REFERENCE      | varchar(64)  | YES  |      | NULL    |       |
| SEVERITY       | varchar(64)  | YES  |      | NULL    |       |
| DETAILS        | varchar(256) | YES  |      | NULL    |       |
+----------------+--------------+------+------+---------+-------+
9 rows in set (0.00 sec)
```

フィールドの説明:

-   `RULE` : 診断ルールの名前。現在、次のルールが利用可能です。
    -   `config` : 設定が一貫していて適切であるかどうかをチェックします。同じ構成が異なるインスタンスで一貫性がない場合、 `warning`診断結果が生成されます。
    -   `version` : バージョンの整合性チェック。同じバージョンが異なるインスタンスで一貫性がない場合、 `warning`診断結果が生成されます。
    -   `node-load` :サーバーの負荷をチェックします。現在のシステム負荷が高すぎる場合、対応する`warning`診断結果が生成されます。
    -   `critical-error` : システムの各モジュールは重大なエラーを定義します。対応する期間内に重大なエラーがしきい値を超えると、警告の診断結果が生成されます。
    -   `threshold-check` : 診断システムは主要なメトリックのしきい値をチェックします。しきい値を超えると、対応する診断情報が生成されます。
-   `ITEM` : 各ルールは異なる項目を診断します。このフィールドは、各ルールに対応する具体的な診断項目を示します。
-   `TYPE` : 診断のインスタンス タイプ。オプションの値は`tidb` 、 `pd` 、および`tikv`です。
-   `INSTANCE` : 診断されたインスタンスの特定のアドレス。
-   `STATUS_ADDRESS` : インスタンスの HTTP API サービス アドレス。
-   `VALUE` : 特定の診断項目の値。
-   `REFERENCE` : この診断項目の基準値(閾値)です。 `VALUE`がしきい値を超えると、対応する診断情報が生成されます。
-   `SEVERITY` : 重大度レベル。オプションの値は`warning`と`critical`です。
-   `DETAILS` : 診断の詳細。SQL ステートメントや詳細な診断のためのドキュメント リンクも含まれる場合があります。

## 診断例 {#diagnostics-example}

クラスター内に現在存在する問題を診断します。

```sql
SELECT * FROM information_schema.inspection_result\G
```

```sql
***************************[ 1. row ]***************************
RULE      | config
ITEM      | log.slow-threshold
TYPE      | tidb
INSTANCE  | 172.16.5.40:4000
VALUE     | 0
REFERENCE | not 0
SEVERITY  | warning
DETAILS   | slow-threshold = 0 will record every query to slow log, it may affect performance
***************************[ 2. row ]***************************
RULE      | version
ITEM      | git_hash
TYPE      | tidb
INSTANCE  |
VALUE     | inconsistent
REFERENCE | consistent
SEVERITY  | critical
DETAILS   | the cluster has 2 different tidb version, execute the sql to see more detail: select * from information_schema.cluster_info where type='tidb'
***************************[ 3. row ]***************************
RULE      | threshold-check
ITEM      | storage-write-duration
TYPE      | tikv
INSTANCE  | 172.16.5.40:23151
VALUE     | 130.417
REFERENCE | < 0.100
SEVERITY  | warning
DETAILS   | max duration of 172.16.5.40:23151 tikv storage-write-duration was too slow
***************************[ 4. row ]***************************
RULE      | threshold-check
ITEM      | rocksdb-write-duration
TYPE      | tikv
INSTANCE  | 172.16.5.40:20151
VALUE     | 108.105
REFERENCE | < 0.100
SEVERITY  | warning
DETAILS   | max duration of 172.16.5.40:20151 tikv rocksdb-write-duration was too slow
```

上記の診断結果から次の問題を検出できます。

-   最初の行は、TiDB の`log.slow-threshold`値が`0`に構成されていることを示しており、これはパフォーマンスに影響を与える可能性があります。
-   2 行目は、クラスター内に 2 つの異なる TiDB バージョンが存在することを示しています。
-   3 行目と 4 行目は、TiKV 書き込み遅延が長すぎることを示しています。予想される遅延は 0.1 秒以下ですが、実際の遅延は予想よりもはるかに長くなります。

「2020-03-26 00:03:00」から「2020-03-26 00:08:00」など、指定した範囲内に存在する問題を診断することもできます。時間範囲を指定するには、SQL ヒント`/*+ time_range() */`を使用します。次のクエリの例を参照してください。

```sql
select /*+ time_range("2020-03-26 00:03:00", "2020-03-26 00:08:00") */ * from information_schema.inspection_result\G
```

```sql
***************************[ 1. row ]***************************
RULE      | critical-error
ITEM      | server-down
TYPE      | tidb
INSTANCE  | 172.16.5.40:4009
VALUE     |
REFERENCE |
SEVERITY  | critical
DETAILS   | tidb 172.16.5.40:4009 restarted at time '2020/03/26 00:05:45.670'
***************************[ 2. row ]***************************
RULE      | threshold-check
ITEM      | get-token-duration
TYPE      | tidb
INSTANCE  | 172.16.5.40:10089
VALUE     | 0.234
REFERENCE | < 0.001
SEVERITY  | warning
DETAILS   | max duration of 172.16.5.40:10089 tidb get-token-duration is too slow
```

上記の診断結果から次の問題を検出できます。

-   最初の行は、 `172.16.5.40:4009` TiDB インスタンスが`2020/03/26 00:05:45.670`で再起動されることを示します。
-   2 行目は、 `172.16.5.40:10089` TiDB インスタンスの最大`get-token-duration`時間は 0.234 秒ですが、予想される時間は 0.001 秒未満であることを示しています。

条件を指定して、たとえば`critical`レベルの診断結果をクエリすることもできます。

```sql
select * from information_schema.inspection_result where severity='critical';
```

`critical-error`ルールの診断結果のみをクエリします。

```sql
select * from information_schema.inspection_result where rule='critical-error';
```

## 診断ルール {#diagnostic-rules}

診断モジュールには一連のルールが含まれています。これらのルールは、既存の監視テーブルおよびクラスター情報テーブルをクエリした後、結果をしきい値と比較します。結果がしきい値を超えた場合、 `warning`または`critical`の診断が生成され、対応する情報が`details`列に表示されます。

`inspection_rules`システム テーブルをクエリすることで、既存の診断ルールをクエリできます。

```sql
select * from information_schema.inspection_rules where type='inspection';
```

```sql
+-----------------+------------+---------+
| NAME            | TYPE       | COMMENT |
+-----------------+------------+---------+
| config          | inspection |         |
| version         | inspection |         |
| node-load       | inspection |         |
| critical-error  | inspection |         |
| threshold-check | inspection |         |
+-----------------+------------+---------+
```

### <code>config</code>診断ルール {#code-config-code-diagnostic-rule}

`config`診断ルールでは、 `CLUSTER_CONFIG`システム テーブルをクエリすることによって、次の 2 つの診断ルールが実行されます。

-   同じコンポーネントの設定値が一致しているかどうかを確認します。すべての構成項目にこの一貫性チェックがあるわけではありません。整合性チェックの許可リストは次のとおりです。

    ```go
    // The allowlist of the TiDB configuration consistency check
    port
    status.status-port
    host
    path
    advertise-address
    status.status-port
    log.file.filename
    log.slow-query-file
    tmp-storage-path

    // The allowlist of the PD configuration consistency check
    advertise-client-urls
    advertise-peer-urls
    client-urls
    data-dir
    log-file
    log.file.filename
    metric.job
    name
    peer-urls

    // The allowlist of the TiKV configuration consistency check
    server.addr
    server.advertise-addr
    server.status-addr
    log-file
    raftstore.raftdb-path
    storage.data-dir
    storage.block-cache.capacity
    ```

-   以下の設定項目の値が期待どおりであるかどうかを確認します。

    | 成分   | コンフィグレーション項目       | 期待値      |
    | ---- | ------------------ | -------- |
    | TiDB | log.slow-threshold | `0`より大きい |
    | TiKV | raftstore.同期ログ     | `true`   |

### <code>version</code>診断ルール {#code-version-code-diagnostic-rule}

`version`診断ルールは、 `CLUSTER_INFO`システム テーブルをクエリすることによって、同じコンポーネントのバージョン ハッシュが一貫しているかどうかをチェックします。次の例を参照してください。

```sql
SELECT * FROM information_schema.inspection_result WHERE rule='version'\G
```

```sql
***************************[ 1. row ]***************************
RULE      | version
ITEM      | git_hash
TYPE      | tidb
INSTANCE  |
VALUE     | inconsistent
REFERENCE | consistent
SEVERITY  | critical
DETAILS   | the cluster has 2 different tidb versions, execute the sql to see more detail: SELECT * FROM information_schema.cluster_info WHERE type='tidb'
```

### <code>critical-error</code>診断ルール {#code-critical-error-code-diagnostic-rule}

`critical-error`診断ルールで、次の 2 つの診断ルールが実行されます。

-   メトリクス スキーマ内の関連する監視システム テーブルをクエリすることにより、クラスターに次のエラーがあるかどうかを検出します。

    | 成分   | エラー名                    | 監視テーブル                               | エラーの説明                                       |
    | ---- | ----------------------- | ------------------------------------ | -------------------------------------------- |
    | TiDB | パニックカウント                | tidb_panic_count_total_count         | TiDB でパニックが発生します。                            |
    | TiDB | バイナリログエラー               | tidb_binlog_error_total_count        | TiDB がbinlogを書き込むときにエラーが発生します。               |
    | TiKV | クリティカル・エラー              | tikv_critical_error_total_coun       | TiKV の重大なエラー。                                |
    | TiKV | スケジューラが忙しい              | tikv_scheduler_is_busy_total_count   | TiKV スケジューラがビジー状態であるため、TiKV が一時的に利用できなくなります。 |
    | TiKV | コプロセッサーがビジー状態です         | tikv_coprocessor_is_busy_total_count | TiKVコプロセッサーはビジー状態です。                         |
    | TiKV | チャンネルがいっぱいです            | tikv_channel_full_total_count        | TiKVで「チャンネルフル」エラーが発生します。                     |
    | TiKV | tikv_engine_write_stall | tikv_engine_write_stall              | TiKVで「ストール」エラーが発生します。                        |

-   `metrics_schema.up`監視テーブルと`CLUSTER_LOG`システム テーブルをクエリして、コンポーネントが再起動されているかどうかを確認します。

### <code>threshold-check</code>診断ルール {#code-threshold-check-code-diagnostic-rule}

`threshold-check`診断ルールは、メトリック スキーマ内の関連する監視システム テーブルをクエリすることにより、クラスター内の次のメトリックがしきい値を超えているかどうかを確認します。

| 成分   | モニタリング指標           | 監視テーブル                              | 期待値        | 説明                                                                                                                   |
| :--- | :----------------- | :---------------------------------- | :--------- | :------------------------------------------------------------------------------------------------------------------- |
| TiDB | tso-duration       | pd_tso_wait_duration                | &lt; 50ms  | トランザクションの TSO を取得するまでの待機時間。                                                                                          |
| TiDB | トークンの取得期間          | tidb_get_token_duration             | &lt; 1ms   | トークンの取得にかかる時間を問い合わせます。関連する TiDB 構成項目は[`token-limit`](/command-line-flags-for-tidb-configuration.md#--token-limit)です。 |
| TiDB | ロードスキーマ期間          | tidb_load_schema_duration           | 1秒未満       | TiDB がスキーマ メタデータを更新するのにかかる時間。                                                                                        |
| TiKV | スケジューラ-cmd-期間      | tikv_scheduler_command_duration     | &lt; 0.1秒  | TiKV が KV `cmd`リクエストを実行するのにかかる時間。                                                                                    |
| TiKV | ハンドル スナップショット期間    | tikv_handle_snapshot_duration       | 30代未満      | TiKV がスナップショットを処理するのにかかる時間。                                                                                          |
| TiKV | ストレージ書き込み期間        | tikv_storage_async_request_duration | &lt; 0.1秒  | TiKV の書き込みレイテンシー。                                                                                                    |
| TiKV | ストレージスナップショット期間    | tikv_storage_async_request_duration | &lt; 50ms  | TiKV がスナップショットを取得するのにかかる時間。                                                                                          |
| TiKV | rocksdb-書き込み期間     | tikv_engine_write_duration          | &lt; 100ms | TiKV RocksDB の書き込みレイテンシー。                                                                                            |
| TiKV | ロックスデータベース取得-期間    | tikv_engine_max_get_duration        | &lt; 50ms  | TiKV RocksDB の読み取りレイテンシー。                                                                                            |
| TiKV | ロックスデータベースシーク期間    | tikv_engine_max_seek_duration       | &lt; 50ms  | TiKV RocksDB の実行レイテンシー`seek` 。                                                                                       |
| TiKV | スケジューラー保留中のコマンド数   | tikv_scheduler_pending_commands     | &lt; 1000  | TiKV で停止したコマンドの数。                                                                                                    |
| TiKV | インデックスブロックキャッシュヒット | tikv_block_index_cache_hit          | 0.95       | TiKV のインデックスブロックキャッシュのヒット率。                                                                                          |
| TiKV | フィルターブロックキャッシュヒット  | tikv_block_filter_cache_hit         | 0.95       | TiKV のフィルターブロックキャッシュのヒット率。                                                                                           |
| TiKV | データブロックキャッシュヒット    | tikv_block_data_cache_hit           | 0.80       | TiKV のデータブロックキャッシュのヒット率。                                                                                             |
| TiKV | リーダースコアバランス        | pd_scheduler_store_status           | &lt; 0.05  | 各 TiKV インスタンスのリーダー スコアのバランスが取れているかどうかを確認します。インスタンス間の予想される差異は 5% 未満です。                                                |
| TiKV | リージョンスコアバランス       | pd_scheduler_store_status           | &lt; 0.05  | 各 TiKV インスタンスのリージョンスコアのバランスが取れているかどうかを確認します。インスタンス間の予想される差異は 5% 未満です。                                                |
| TiKV | 店舗利用可能な残高          | pd_scheduler_store_status           | &lt; 0.2   | 各 TiKV インスタンスの利用可能なstorageのバランスが取れているかどうかを確認します。インスタンス間の予想される差異は 20% 未満です。                                           |
| TiKV | 領域数                | pd_scheduler_store_status           | &lt; 20000 | 各 TiKV インスタンスのリージョンの数を確認します。単一インスタンス内の予想されるリージョン数は 20,000 未満です。                                                      |
| PD   | 地域の健康              | pd_region_health                    | &lt; 100   | クラスター内でスケジュール処理中のリージョンの数を検出します。予想される数は合計 100 未満です。                                                                   |

さらに、このルールは、TiKV インスタンス内の次のスレッドの CPU 使用率が高すぎるかどうかもチェックします。

-   スケジューラ-ワーカー-CPU
-   コプロセッサ-通常-CPU
-   コプロセッサーハイCPU
-   コプロセッサー低 CPU
-   grpc-cpu
-   raftstore-CPU
-   適用-CPU
-   ストレージ-読み取りプール-通常-CPU
-   ストレージ-読み取りプール-高-CPU
-   ストレージ読み取りプール低 CPU
-   分割チェックCPU

組み込みの診断ルールは常に改善されています。さらに診断ルールがある場合は、PR または問題を[`tidb`リポジトリ](https://github.com/pingcap/tidb)に作成してください。
