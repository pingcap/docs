---
title: INSPECTION_RESULT
summary: Learn the `INSPECTION_RESULT` diagnostic result table.
---

# INSPECTION_RESULT {#inspection-result}

TiDBには、システムの障害や隠れた問題を検出するための診断ルールが組み込まれています。

`INSPECTION_RESULT`の診断機能は、問題をすばやく見つけて、繰り返しの手作業を減らすのに役立ちます。 `select * from information_schema.inspection_result`ステートメントを使用して、内部診断をトリガーできます。

`information_schema.inspection_result`診断結果表`information_schema.inspection_result`の構成は次のとおりです。

{{< copyable "" >}}

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

フィールドの説明：

-   `RULE` ：診断ルールの名前。現在、次のルールを使用できます。
    -   `config` ：構成が一貫していて適切かどうかを確認します。同じ構成が異なるインスタンスで一貫していない場合、 `warning`の診断結果が生成されます。
    -   `version` ：バージョンの整合性チェック。同じバージョンが異なるインスタンスで一貫していない場合、 `warning`の診断結果が生成されます。
    -   `node-load` ：サーバーの負荷を確認します。現在のシステム負荷が高すぎる場合、対応する`warning`の診断結果が生成されます。
    -   `critical-error` ：システムの各モジュールは重大なエラーを定義します。対応する期間内に重大なエラーがしきい値を超えると、警告診断結果が生成されます。
    -   `threshold-check` ：診断システムは主要なメトリックのしきい値をチェックします。しきい値を超えると、対応する診断情報が生成されます。
-   `ITEM` ：各ルールは異なるアイテムを診断します。このフィールドは、各ルールに対応する特定の診断項目を示します。
-   `TYPE` ：診断のインスタンスタイプ。オプションの値は`tidb` 、および`pd` `tikv` 。
-   `INSTANCE` ：診断されたインスタンスの特定のアドレス。
-   `STATUS_ADDRESS` ：インスタンスのHTTPAPIサービスアドレス。
-   `VALUE` ：特定の診断項目の値。
-   `REFERENCE` ：この診断項目の基準値（しきい値）。 `VALUE`がしきい値を超えると、対応する診断情報が生成されます。
-   `SEVERITY` ：重大度レベル。オプションの値は`warning`と`critical`です。
-   `DETAILS` ：診断の詳細。さらに診断するためのSQLステートメントまたはドキュメントリンクが含まれている場合があります。

## 診断例 {#diagnostics-example}

クラスタに現在存在する問題を診断します。

{{< copyable "" >}}

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

上記の診断結果から、次の問題を検出できます。

-   最初の行は、TiDBの`log.slow-threshold`の値が`0`に構成されていることを示しています。これは、パフォーマンスに影響を与える可能性があります。
-   2行目は、2つの異なるTiDBバージョンがクラスタに存在することを示しています。
-   3行目と4行目は、TiKVの書き込み遅延が長すぎることを示しています。予想される遅延は0.1秒以内ですが、実際の遅延は予想よりはるかに長くなります。

また、「2020-03-2600:03:00」から「2020-03-2600:08:00」など、指定した範囲内に存在する問題を診断することもできます。時間範囲を指定するには、SQLヒント`/*+ time_range() */`を使用します。次のクエリ例を参照してください。

{{< copyable "" >}}

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

上記の診断結果から、次の問題を検出できます。

-   最初の行は、 `172.16.5.40:4009`つのTiDBインスタンスが`2020/03/26 00:05:45.670`で再起動されることを示しています。
-   2番目の行は、 `172.16.5.40:10089`のTiDBインスタンスの最大`get-token-duration`時間が0.234秒であることを示していますが、予想される時間は0.001秒未満です。

たとえば、条件を指定して、 `critical`レベルの診断結果を照会することもできます。

{{< copyable "" >}}

```sql
select * from information_schema.inspection_result where severity='critical';
```

`critical-error`のルールの診断結果のみを照会します。

{{< copyable "" >}}

```sql
select * from information_schema.inspection_result where rule='critical-error';
```

## 診断ルール {#diagnostic-rules}

診断モジュールには一連のルールが含まれています。これらのルールは、既存の監視テーブルとクラスタ情報テーブルにクエリを実行した後、結果をしきい値と比較します。結果がしきい値を超えると、 `warning`または`critical`の診断が生成され、対応する情報が`details`列に表示されます。

`inspection_rules`のシステムテーブルをクエリすることにより、既存の診断ルールをクエリできます。

{{< copyable "" >}}

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

`config`つの診断ルールでは、 `CLUSTER_CONFIG`のシステムテーブルを照会することにより、次の2つの診断ルールが実行されます。

-   同じコンポーネントの構成値に一貫性があるかどうかを確認してください。すべての構成アイテムにこの整合性チェックがあるわけではありません。整合性チェックの許可リストは次のとおりです。

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

-   次の構成項目の値が期待どおりかどうかを確認してください。

    | 成分   | Configuration / コンフィグレーション項目 | 期待値      |
    | ---- | ---------------------------- | -------- |
    | TiDB | log.slow-threshold           | `0`より大きい |
    | TiKV | raftstore.sync-log           | `true`   |

### <code>version</code>診断ルール {#code-version-code-diagnostic-rule}

`version`診断ルールは、 `CLUSTER_INFO`システムテーブルをクエリすることにより、同じコンポーネントのバージョンハッシュが一貫しているかどうかをチェックします。次の例を参照してください。

{{< copyable "" >}}

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

`critical-error`つの診断ルールでは、次の2つの診断ルールが実行されます。

-   メトリックスキーマ内の関連する監視システムテーブルをクエリして、クラスタに次のエラーがあるかどうかを検出します。

    | 成分   | エラー名                    | モニタリングテーブル                           | エラーの説明                                     |
    | ---- | ----------------------- | ------------------------------------ | ------------------------------------------ |
    | TiDB | パニックカウント                | tidb_panic_count_total_count         | パニックはTiDBで発生します。                           |
    | TiDB | binlog-エラー              | tidb_binlog_error_total_count        | TiDBがbinlogを書き込むときにエラーが発生します。              |
    | TiKV | クリティカル・エラー              | tikv_critical_error_total_coun       | TiKVの重大なエラー。                               |
    | TiKV | スケジューラーは忙しい             | tikv_scheduler_is_busy_total_count   | TiKVスケジューラがビジー状態であるため、TiKVが一時的に使用できなくなります。 |
    | TiKV | コプロセッサーはビジーです           | tikv_coprocessor_is_busy_total_count | TiKVコプロセッサーがビジーすぎます。                       |
    | TiKV | チャネルがいっぱいです             | tikv_channel_full_total_count        | 「チャネルフル」エラーはTiKVで発生します。                    |
    | TiKV | tikv_engine_write_stall | tikv_engine_write_stall              | 「ストール」エラーはTiKVで発生します。                      |

-   `metrics_schema.up`の監視テーブルと`CLUSTER_LOG`のシステムテーブルを照会して、コンポーネントが再起動されているかどうかを確認します。

### <code>threshold-check</code>診断ルール {#code-threshold-check-code-diagnostic-rule}

`threshold-check`診断ルールは、メトリックスキーマ内の関連する監視システムテーブルをクエリすることにより、クラスタの次のメトリックがしきい値を超えているかどうかをチェックします。

| 成分   | モニタリングメトリック            | モニタリングテーブル                          | 期待値       | 説明                                                                                                                 |
| :--- | :--------------------- | :---------------------------------- | :-------- | :----------------------------------------------------------------------------------------------------------------- |
| TiDB | tso-期間                 | pd_tso_wait_duration                | &lt;50ms  | トランザクションのTSOを取得するための待機時間。                                                                                          |
| TiDB | get-token-duration     | tidb_get_token_duration             | &lt;1ms   | トークンの取得にかかる時間を照会します。関連するTiDB構成アイテムは[`token-limit`](/command-line-flags-for-tidb-configuration.md#--token-limit)です。 |
| TiDB | load-schema-duration   | tidb_load_schema_duration           | &lt;1秒    | TiDBがスキーマメタデータを更新するのにかかる時間。                                                                                        |
| TiKV | スケジューラー-cmd-期間         | tikv_scheduler_command_duration     | &lt;0.1秒  | TiKVが`cmd`要求を実行するのにかかる時間。                                                                                          |
| TiKV | ハンドル-スナップショット-期間       | tikv_handle_snapshot_duration       | &lt;30秒   | TiKVがスナップショットを処理するのにかかる時間。                                                                                         |
| TiKV | ストレージ-書き込み-期間          | tikv_storage_async_request_duration | &lt;0.1秒  | TiKVの書き込みレイテンシ。                                                                                                    |
| TiKV | ストレージ-スナップショット-期間      | tikv_storage_async_request_duration | &lt;50ms  | TiKVがスナップショットを取得するのにかかる時間。                                                                                         |
| TiKV | rocksdb-書き込み-期間        | tikv_engine_write_duration          | &lt;100ms | TiKVRocksDBの書き込みレイテンシ。                                                                                             |
| TiKV | rocksdb-get-duration   | tikv_engine_max_get_duration        | &lt;50ms  | TiKVRocksDBの読み取りレイテンシ。                                                                                             |
| TiKV | rocksdb-seek-duration  | tikv_engine_max_seek_duration       | &lt;50ms  | TiKVRocksDBが`seek`を実行するまでの待ち時間。                                                                                    |
| TiKV | スケジューラー保留中のcmd-coun    | tikv_scheduler_pending_commands     | &lt;1000  | TiKVで停止したコマンドの数。                                                                                                   |
| TiKV | index-block-cache-hit  | tikv_block_index_cache_hit          | 0.95      | TiKVのインデックスブロックキャッシュのヒット率。                                                                                         |
| TiKV | filter-block-cache-hit | tikv_block_filter_cache_hit         | 0.95      | TiKVのフィルターブロックキャッシュのヒット率。                                                                                          |
| TiKV | data-block-cache-hit   | tikv_block_data_cache_hit           | 0.80      | TiKVのデータブロックキャッシュのヒット率。                                                                                            |
| TiKV | リーダー-スコア-バランス          | pd_scheduler_store_status           | &lt;0.05  | 各TiKVインスタンスのリーダースコアのバランスが取れているかどうかを確認します。インスタンス間の予想される差異は5％未満です。                                                   |
| TiKV | リージョンスコアバランス           | pd_scheduler_store_status           | &lt;0.05  | 各TiKVインスタンスのRegionスコアのバランスが取れているかどうかを確認します。インスタンス間の予想される差異は5％未満です。                                                 |
| TiKV | 店舗利用可能残高               | pd_scheduler_store_status           | &lt;0.2   | 各TiKVインスタンスの使用可能なストレージのバランスが取れているかどうかを確認します。インスタンス間の予想される差異は20％未満です。                                               |
| TiKV | リージョンカウント              | pd_scheduler_store_status           | &lt;20000 | 各TiKVインスタンスのリージョン数を確認します。 1つのインスタンスで予想されるリージョンの数は20,000未満です。                                                       |
| PD   | 地域の健康                  | pd_region_health                    | &lt;100   | クラスタでスケジューリング中のリージョンの数を検出します。予想される数は合計で100未満です。                                                                    |

さらに、このルールは、TiKVインスタンス内の次のスレッドのCPU使用率が高すぎるかどうかもチェックします。

-   スケジューラー-ワーカー-CPU
-   コプロセッサー-通常-CPU
-   コプロセッサー-high-cpu
-   コプロセッサー-low-cpu
-   grpc-cpu
-   raftstore-cpu
-   apply-cpu
-   storage-readpool-normal-cpu
-   storage-readpool-high-cpu
-   storage-readpool-low-cpu
-   split-check-cpu

組み込みの診断ルールは常に改善されています。より多くの診断ルールがある場合は、 [`tidb`リポジトリ](https://github.com/pingcap/tidb)でPRまたは問題を作成することを歓迎します。
