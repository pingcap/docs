---
title: TiCDC OpenAPI v2
summary: Learn how to use the OpenAPI v2 interface to manage the cluster status and data replication.
---

# TiCDC OpenAPI v2 {#ticdc-openapi-v2}

<!-- markdownlint-disable MD024 -->

TiCDC は、TiCDC クラスターを照会および操作するための OpenAPI 機能を提供します。 OpenAPI 機能は[`cdc cli`ツール](/ticdc/ticdc-manage-changefeed.md)のサブセットです。

> **ノート：**
>
> -   TiCDC は、v6.5.x リリース シリーズの v6.5.2 から始まる OpenAPI v2 をサポートします。 TiCDC のバージョンが v6.5.0 または v6.5.1 の場合は、代わりに[TiCDC OpenAPI v1](/ticdc/ticdc-open-api.md)を使用してください。
> -   TiCDC OpenAPI v1 は、将来のリリースで削除される予定です。 TiCDC OpenAPI v2 を使用することをお勧めします。

API を使用して、TiCDC クラスターで次のメンテナンス操作を実行できます。

-   [TiCDC ノードのステータス情報を取得する](#get-the-status-information-of-a-ticdc-node)
-   [TiCDC クラスターのヘルス ステータスを確認する](#check-the-health-status-of-a-ticdc-cluster)
-   [レプリケーション タスクを作成する](#create-a-replication-task)
-   [レプリケーション タスクを削除する](#remove-a-replication-task)
-   [レプリケーション構成を更新する](#update-the-replication-configuration)
-   [レプリケーション タスク リストを照会する](#query-the-replication-task-list)
-   [特定のレプリケーション タスクを照会する](#query-a-specific-replication-task)
-   [レプリケーション タスクを一時停止する](#pause-a-replication-task)
-   [レプリケーション タスクを再開する](#resume-a-replication-task)
-   [レプリケーション サブタスク リストを照会する](#query-the-replication-subtask-list)
-   [特定のレプリケーション サブタスクを照会する](#query-a-specific-replication-subtask)
-   [TiCDC サービス プロセス リストのクエリ](#query-the-ticdc-service-process-list)
-   [所有者ノードを削除する](#evict-an-owner-node)
-   [TiCDCサーバーのログレベルを動的に調整する](#dynamically-adjust-the-log-level-of-the-ticdc-server)

すべての API の要求本文と戻り値は JSON 形式です。リクエストが成功すると、 `200 OK`メッセージが返されます。以下のセクションでは、API の特定の使用法について説明します。

次の例では、TiCDCサーバーのリッスン IP アドレスは`127.0.0.1`で、ポートは`8300`です。 TiCDCサーバーの起動時に、 `--addr=ip:port`経由で TiCDC にバインドされた IP アドレスとポートを指定できます。

## API エラー メッセージ テンプレート {#api-error-message-template}

API リクエストの送信後にエラーが発生した場合、次の形式のエラー メッセージが返されます。

```json
{
    "error_msg": "",
    "error_code": ""
}
```

上記の JSON 出力で、 `error_msg`エラー メッセージを表し、 `error_code`は対応するエラー コードです。

## API リスト インターフェイスの戻り形式 {#return-format-of-the-api-list-interface}

API リクエストがリソースのリスト (たとえば、すべて`Captures`のリスト) を返す場合、TiCDC の戻り形式は次のとおりです。

```json
{
  "total": 2,
  "items": [
    {
      "id": "d2912e63-3349-447c-90ba-wwww",
      "is_owner": true,
      "address": "127.0.0.1:8300"
    },
    {
      "id": "d2912e63-3349-447c-90ba-xxxx",
      "is_owner": false,
      "address": "127.0.0.1:8302"
    }
  ]
}
```

上記の例では:

-   `total` : リソースの総数を示します。
-   `items` : このリクエストによって返されるすべてのリソースを含む配列。配列のすべての要素は同じリソースです。

## TiCDC ノードのステータス情報を取得する {#get-the-status-information-of-a-ticdc-node}

この API は同期インターフェースです。リクエストが成功すると、対応するノードのステータス情報が返されます。

### リクエストURI {#request-uri}

`GET /api/v2/status`

### 例 {#example}

次のリクエストは、IP アドレスが`127.0.0.1`でポート番号が`8300` TiCDC ノードのステータス情報を取得します。

```shell
curl -X GET http://127.0.0.1:8300/api/v2/status
```

```json
{
  "version": "v7.0.0-master-dirty",
  "git_hash": "10413bded1bdb2850aa6d7b94eb375102e9c44dc",
  "id": "d2912e63-3349-447c-90ba-72a4e04b5e9e",
  "pid": 1447,
  "is_owner": true,
  "liveness": 0
}
```

上記の出力のパラメータは次のとおりです。

-   `version` : TiCDC の現在のバージョン番号。
-   `git_hash` : Git ハッシュ値。
-   `id` : ノードのキャプチャ ID。
-   `pid` : ノードのキャプチャ プロセス ID (PID)。
-   `is_owner` : ノードが所有者かどうかを示します。
-   `liveness` : このノードがライブかどうか。 `0`通常を意味します。 `1`ノードが`graceful shutdown`状態であることを意味します。

## TiCDC クラスターのヘルス ステータスを確認する {#check-the-health-status-of-a-ticdc-cluster}

この API は同期インターフェースです。クラスターが正常な場合、 `200 OK`が返されます。

### リクエストURI {#request-uri}

`GET /api/v2/health`

### 例 {#example}

```shell
curl -X GET http://127.0.0.1:8300/api/v2/health
```

クラスターが正常な場合、応答は`200 OK`で、空の JSON オブジェクトです。

```json
{}
```

クラスターが正常でない場合、応答はエラー メッセージを含む JSON オブジェクトです。

## レプリケーション タスクを作成する {#create-a-replication-task}

このインターフェイスは、レプリケーション タスクを TiCDC に送信するために使用されます。リクエストが成功した場合、 `200 OK`が返されます。返された結果は、サーバーがコマンドの実行に同意したことを意味するだけで、コマンドが正常に実行されることを保証するものではありません。

### リクエストURI {#request-uri}

`POST /api/v2/changefeeds`

### パラメータの説明 {#parameter-descriptions}

```json
{
  "changefeed_id": "string",
  "replica_config": {
    "bdr_mode": true,
    "case_sensitive": true,
    "check_gc_safe_point": true,
    "consistent": {
      "flush_interval": 0,
      "level": "string",
      "max_log_size": 0,
      "storage": "string"
    },
    "enable_old_value": true,
    "enable_sync_point": true,
    "filter": {
      "do_dbs": [
        "string"
      ],
      "do_tables": [
        {
          "database_name": "string",
          "table_name": "string"
        }
      ],
      "event_filters": [
        {
          "ignore_delete_value_expr": "string",
          "ignore_event": [
            "string"
          ],
          "ignore_insert_value_expr": "string",
          "ignore_sql": [
            "string"
          ],
          "ignore_update_new_value_expr": "string",
          "ignore_update_old_value_expr": "string",
          "matcher": [
            "string"
          ]
        }
      ],
      "ignore_dbs": [
        "string"
      ],
      "ignore_tables": [
        {
          "database_name": "string",
          "table_name": "string"
        }
      ],
      "ignore_txn_start_ts": [
        0
      ],
      "rules": [
        "string"
      ]
    },
    "force_replicate": true,
    "ignore_ineligible_table": true,
    "memory_quota": 0,
    "mounter": {
      "worker_num": 0
    },
    "sink": {
      "column_selectors": [
        {
          "columns": [
            "string"
          ],
          "matcher": [
            "string"
          ]
        }
      ],
      "csv": {
        "delimiter": "string",
        "include_commit_ts": true,
        "null": "string",
        "quote": "string"
      },
      "date_separator": "string",
      "dispatchers": [
        {
          "matcher": [
            "string"
          ],
          "partition": "string",
          "topic": "string"
        }
      ],
      "enable_partition_separator": true,
      "encoder_concurrency": 0,
      "protocol": "string",
      "schema_registry": "string",
      "terminator": "string",
      "transaction_atomicity": "string"
    },
    "sync_point_interval": "string",
    "sync_point_retention": "string"
  },
  "sink_uri": "string",
  "start_ts": 0,
  "target_ts": 0
}
```

パラメータの説明は次のとおりです。

| パラメータ名           | 説明                                                                                                                        |
| :--------------- | :------------------------------------------------------------------------------------------------------------------------ |
| `changefeed_id`  | `STRING`型。レプリケーション タスクの ID。 (オプション)                                                                                       |
| `replica_config` | レプリケーション タスクのコンフィグレーションパラメーター。 (オプション)                                                                                    |
| **`sink_uri`**   | `STRING`型。レプリケーション タスクのダウンストリーム アドレス。 (**必須**)                                                                            |
| `start_ts`       | `UINT64`型。 changefeed の開始 TSO を指定します。 TiCDC クラスターは、この TSO からデータのプルを開始します。デフォルト値は現在の時刻です。 (オプション)                          |
| `target_ts`      | `UINT64`型。 changefeed のターゲット TSO を指定します。 TiCDC クラスターは、この TSO に到達するとデータのプルを停止します。デフォルト値は空です。つまり、TiCDC は自動的に停止しません。 (オプション) |

`changefeed_id` 、 `start_ts` 、 `target_ts` 、および`sink_uri`の意味と形式は、 [`cdc cli`を使用してレプリケーション タスクを作成する](/ticdc/ticdc-manage-changefeed.md#create-a-replication-task)ドキュメントで説明されているものと同じです。これらのパラメーターの詳細な説明については、そのドキュメントを参照してください。 `sink_uri`で証明書パスを指定するときは、対応する証明書を対応する TiCDCサーバーにアップロードしたことを確認してください。

`replica_config`パラメータの説明は次のとおりです。

| パラメータ名                    | 説明                                                                                                                                                                                 |
| :------------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `bdr_mode`                | `BOOLEAN`型。 [双方向レプリケーション](/ticdc/ticdc-bidirectional-replication.md)を有効にするかどうかを決定します。デフォルト値は`false`です。 (オプション)                                                                     |
| `case_sensitive`          | `BOOLEAN`型。テーブル名をフィルタリングするときに大文字と小文字を区別するかどうかを決定します。デフォルト値は`true`です。 (オプション)                                                                                                       |
| `check_gc_safe_point`     | `BOOLEAN`型。レプリケーション タスクの開始時刻が GC 時刻よりも早いことを確認するかどうかを決定します。デフォルト値は`true`です。 (オプション)                                                                                                 |
| `consistent`              | REDO ログの構成パラメーター。 (オプション)                                                                                                                                                          |
| `enable_old_value`        | `BOOLEAN`型。古い値 (つまり、更新前の値) を出力するかどうかを決定します。デフォルト値は`true`です。 (オプション)                                                                                                                |
| `enable_sync_point`       | `BOOLEAN`型。 `sync point`を有効にするかどうかを決定します。 (オプション)                                                                                                                                  |
| `filter`                  | `filter`の構成パラメーター。 (オプション)                                                                                                                                                         |
| `force_replicate`         | `BOOLEAN`型。デフォルト値は`false`です。 `true`に設定すると、レプリケーション タスクは、一意のインデックスを持たないテーブルを強制的にレプリケートします。 (オプション)                                                                                  |
| `ignore_ineligible_table` | `BOOLEAN`型。デフォルト値は`false`です。 `true`に設定すると、複製タスクは、複製できないテーブルを無視します。 (オプション)                                                                                                         |
| `memory_quota`            | `UINT64`型。レプリケーション タスクのメモリクォータ。 (オプション)                                                                                                                                            |
| `mounter`                 | `mounter`の構成パラメーター。 (オプション)                                                                                                                                                        |
| `sink`                    | `sink`の構成パラメーター。 (オプション)                                                                                                                                                           |
| `sync_point_interval`     | `STRING`型。戻り値は`UINT64`型のナノ秒単位の時間であることに注意してください。 `sync point`機能が有効な場合、このパラメーターは、同期点が上流と下流のスナップショットを調整する間隔を指定します。デフォルト値は`10m`で、最小値は`30s`です。 (オプション)                                  |
| `sync_point_retention`    | `STRING`型。戻り値は`UINT64`型のナノ秒単位の時間であることに注意してください。 `sync point`フィーチャーが使用可能になっている場合、このパラメーターは、データが同期点によってダウンストリーム・テーブルに保持される期間を指定します。この期間を超えると、データはクリーンアップされます。デフォルト値は`24h`です。 (オプション) |

`consistent`パラメータは次のように説明されています。

| パラメータ名           | 説明                                         |
| :--------------- | :----------------------------------------- |
| `flush_interval` | `UINT64`型。 REDO ログ ファイルをフラッシュする間隔。 (オプション) |
| `level`          | `STRING`型。レプリケートされたデータの整合性レベル。 (オプション)     |
| `max_log_size`   | `UINT64`型。 REDO ログの最大値。 (オプション)            |
| `storage`        | `STRING`型。storageの宛先アドレス。 (オプション)          |

`filter`パラメータは次のように説明されています。

| パラメータ名                | 説明                                                                                                                        |
| :-------------------- | :------------------------------------------------------------------------------------------------------------------------ |
| `do_dbs`              | `STRING ARRAY`型。レプリケートするデータベース。 (オプション)                                                                                   |
| `do_tables`           | レプリケートされるテーブル。 (オプション)                                                                                                    |
| `ignore_dbs`          | `STRING ARRAY`型。無視するデータベース。 (オプション)                                                                                       |
| `ignore_tables`       | 無視するテーブル。 (オプション)                                                                                                         |
| `event_filters`       | イベントをフィルタリングするための構成。 (オプション)                                                                                              |
| `ignore_txn_start_ts` | `UINT64 ARRAY`型。これを指定すると、 `[1, 2]`などの`start_ts`を指定するトランザクションは無視されます。 (オプション)                                              |
| `rules`               | `STRING ARRAY`型。 `['foo*.*', 'bar*.*']`などのテーブル スキーマ フィルタリングのルール。詳細については、 [テーブル フィルター](/table-filter.md)を参照してください。 (オプション) |

`filter.event_filters`パラメータの説明は次のとおりです。詳細については、 [Changefeed ログ フィルタ](/ticdc/ticdc-filter.md)を参照してください。

| パラメータ名                         | 説明                                                                                                                 |
| :----------------------------- | :----------------------------------------------------------------------------------------------------------------- |
| `ignore_delete_value_expr`     | `STRING ARRAY`型。たとえば、 `"name = 'john'"` 、 `name = 'john'`条件を含む DELETE DML ステートメントを除外することを意味します。 (オプション)            |
| `ignore_event`                 | `STRING ARRAY`型。たとえば、 `["insert"]` 、INSERT イベントが除外されることを示します。 (オプション)                                              |
| `ignore_insert_value_expr`     | `STRING ARRAY`型。たとえば、 `"id >= 100"` 、 `id >= 100`条件に一致する INSERT DML ステートメントを除外することを意味します。 (オプション)                  |
| `ignore_sql`                   | `STRING ARRAY`型。たとえば、 `["^drop", "add column"]` 、 `DROP`で始まるか`ADD COLUMN`を含む DDL ステートメントを除外することを意味します。 (オプション)     |
| `ignore_update_new_value_expr` | `STRING ARRAY`型。たとえば、 `"gender = 'male'"` 、新しい値`gender = 'male'`を持つ UPDATE DML ステートメントを除外することを意味します。 (オプション)       |
| `ignore_update_old_value_expr` | `STRING ARRAY`型。たとえば、 `"age < 18"` 、古い値`age < 18`を持つ UPDATE DML ステートメントを除外することを意味します。 (オプション)                      |
| `matcher`                      | `STRING ARRAY`型。許可リストとして機能します。たとえば、 `["test.worker"]` 、フィルタ ルールが`test`データベースの`worker`テーブルにのみ適用されることを意味します。 (オプション) |

`mounter`パラメータの説明は次のとおりです。

| パラメータ名       | 説明                                                                              |
| :----------- | :------------------------------------------------------------------------------ |
| `worker_num` | `INT`型。マウンターのスレッド数。マウンタは、TiKV から出力されたデータをデコードするために使用されます。デフォルト値は`16`です。 (オプション) |

`sink`パラメータは次のように説明されています。

| パラメータ名                  | 説明                                                                                                                              |
| :---------------------- | :------------------------------------------------------------------------------------------------------------------------------ |
| `column_selectors`      | 列セレクターの構成。 (オプション)                                                                                                              |
| `csv`                   | CSV 構成。 (オプション)                                                                                                                 |
| `date_separator`        | `STRING`型。ファイル ディレクトリの日付区切りの種類を示します。値のオプションは`none` 、 `year` 、 `month` 、および`day`です。 `none`はデフォルト値で、日付が区切られていないことを意味します。 (オプション)  |
| `dispatchers`           | イベントディスパッチ用の構成配列。 (オプション)                                                                                                       |
| `encoder_concurrency`   | `INT`型。 MQ シンク内のエンコーダ スレッドの数。デフォルト値は`16`です。 (オプション)                                                                             |
| `protocol`              | `STRING`型。 MQ シンクの場合、メッセージのプロトコル形式を指定できます。現在サポートされているプロトコルは、 `canal-json` 、 `open-protocol` 、 `canal` 、 `avro` 、および`maxwell`です。 |
| `schema_registry`       | `STRING`型。スキーマ レジストリ アドレス。 (オプション)                                                                                              |
| `terminator`            | `STRING`型。ターミネータは、2 つのデータ変更イベントを区切るために使用されます。デフォルト値は null です。これは、ターミネータとして`"\r\n"`が使用されることを意味します。 (オプション)                       |
| `transaction_atomicity` | `STRING`型。トランザクションの原子性レベル。 (オプション)                                                                                              |

`sink.column_selectors`は配列です。パラメータの説明は次のとおりです。

| パラメータ名    | 説明                                                 |
| :-------- | :------------------------------------------------- |
| `columns` | `STRING ARRAY`型。列配列。                               |
| `matcher` | `STRING ARRAY`型。マッチャー構成。これは、フィルター ルールと同じ一致構文を持ちます。 |

`sink.csv`パラメータは次のように説明されています。

| パラメータ名              | 説明                                                                        |
| :------------------ | :------------------------------------------------------------------------ |
| `delimiter`         | `STRING`型。 CSV ファイル内のフィールドを区切るために使用される文字。値は ASCII 文字でなければならず、デフォルトは`,`です。 |
| `include_commit_ts` | `BOOLEAN`型。 CSV 行に commit-ts を含めるかどうか。デフォルト値は`false`です。                   |
| `null`              | `STRING`型。 CSV 列が null の場合に表示される文字。デフォルト値は`\N`です。                         |
| `quote`             | `STRING`型。 CSV ファイル内のフィールドを囲むために使用される引用符。値が空の場合、引用符は使用されません。デフォルト値は`"`です。 |

`sink.dispatchers` : MQ タイプのシンクの場合、このパラメーターを使用してイベント ディスパッチャーを構成できます。次のディスパッチャーがサポートされています: `default` 、 `ts` 、 `rowid` 、および`table` 。ディスパッチャのルールは次のとおりです。

-   `default` : 複数の一意のインデックス (主キーを含む) が存在する場合、イベントはテーブル モードでディスパッチされます。一意のインデックス (または主キー) が 1 つだけ存在する場合、イベントは行 ID モードでディスパッチされます。古い値機能が有効になっている場合、イベントはテーブル モードでディスパッチされます。
-   `ts` : 行変更の commitTs を使用してハッシュ値を作成し、イベントをディスパッチします。
-   `rowid` : 選択した HandleKey 列の名前と値を使用して、ハッシュ値を作成し、イベントをディスパッチします。
-   `table` : テーブルのスキーマ名とテーブル名を使用してハッシュ値を作成し、イベントをディスパッチします。

`sink.dispatchers`は配列です。パラメータの説明は次のとおりです。

| パラメータ名      | 説明                                         |
| :---------- | :----------------------------------------- |
| `matcher`   | `STRING ARRAY`型。これは、フィルター ルールと同じ一致構文を持ちます。 |
| `partition` | `STRING`型。イベントをディスパッチするターゲット パーティション。      |
| `topic`     | `STRING`型。イベントをディスパッチするためのターゲット トピック。      |

### 例 {#example}

次のリクエストは、ID が`test5`と`sink_uri` of `blackhome://`のレプリケーション タスクを作成します。

```shell
curl -X POST -H "'Content-type':'application/json'" http://127.0.0.1:8300/api/v2/changefeeds -d '{"changefeed_id":"test5","sink_uri":"blackhole://"}'
```

リクエストが成功した場合、 `200 OK`が返されます。リクエストが失敗すると、エラー メッセージとエラー コードが返されます。

### 応答本文の形式 {#response-body-format}

```json
{
  "admin_job_type": 0,
  "checkpoint_time": "string",
  "checkpoint_ts": 0,
  "config": {
    "bdr_mode": true,
    "case_sensitive": true,
    "check_gc_safe_point": true,
    "consistent": {
      "flush_interval": 0,
      "level": "string",
      "max_log_size": 0,
      "storage": "string"
    },
    "enable_old_value": true,
    "enable_sync_point": true,
    "filter": {
      "do_dbs": [
        "string"
      ],
      "do_tables": [
        {
          "database_name": "string",
          "table_name": "string"
        }
      ],
      "event_filters": [
        {
          "ignore_delete_value_expr": "string",
          "ignore_event": [
            "string"
          ],
          "ignore_insert_value_expr": "string",
          "ignore_sql": [
            "string"
          ],
          "ignore_update_new_value_expr": "string",
          "ignore_update_old_value_expr": "string",
          "matcher": [
            "string"
          ]
        }
      ],
      "ignore_dbs": [
        "string"
      ],
      "ignore_tables": [
        {
          "database_name": "string",
          "table_name": "string"
        }
      ],
      "ignore_txn_start_ts": [
        0
      ],
      "rules": [
        "string"
      ]
    },
    "force_replicate": true,
    "ignore_ineligible_table": true,
    "memory_quota": 0,
    "mounter": {
      "worker_num": 0
    },
    "sink": {
      "column_selectors": [
        {
          "columns": [
            "string"
          ],
          "matcher": [
            "string"
          ]
        }
      ],
      "csv": {
        "delimiter": "string",
        "include_commit_ts": true,
        "null": "string",
        "quote": "string"
      },
      "date_separator": "string",
      "dispatchers": [
        {
          "matcher": [
            "string"
          ],
          "partition": "string",
          "topic": "string"
        }
      ],
      "enable_partition_separator": true,
      "encoder_concurrency": 0,
      "protocol": "string",
      "schema_registry": "string",
      "terminator": "string",
      "transaction_atomicity": "string"
    },
    "sync_point_interval": "string",
    "sync_point_retention": "string"
  },
  "create_time": "string",
  "creator_version": "string",
  "error": {
    "addr": "string",
    "code": "string",
    "message": "string"
  },
  "id": "string",
  "resolved_ts": 0,
  "sink_uri": "string",
  "start_ts": 0,
  "state": "string",
  "target_ts": 0,
  "task_status": [
    {
      "capture_id": "string",
      "table_ids": [
        0
      ]
    }
  ]
}
```

パラメータの説明は次のとおりです。

| パラメータ名            | 説明                                                                                            |
| :---------------- | :-------------------------------------------------------------------------------------------- |
| `admin_job_type`  | `INTEGER`型。管理者のジョブ タイプ。                                                                       |
| `checkpoint_time` | `STRING`型。レプリケーション タスクの現在のチェックポイントのフォーマットされた時刻。                                               |
| `checkpoint_ts`   | `STRING`型。複製タスクの現在のチェックポイントの TSO。                                                             |
| `config`          | レプリケーション タスクの構成。構造と意味はレプリケーションタスク作成時の`replica_config`構成と同じです。                                 |
| `create_time`     | `STRING`型。レプリケーション タスクが作成される時刻。                                                               |
| `creator_version` | `STRING`型。レプリケーション タスクが作成されたときの TiCDC のバージョン。                                                 |
| `error`           | レプリケーション タスク エラー。                                                                             |
| `id`              | `STRING`型。レプリケーション タスク ID。                                                                    |
| `resolved_ts`     | `UINT64`型。複製タスクは ts を解決しました。                                                                  |
| `sink_uri`        | `STRING`型。レプリケーション タスク シンク URI。                                                               |
| `start_ts`        | `UINT64`型。レプリケーション タスクが ts で開始されます。                                                           |
| `state`           | `STRING`型。レプリケーション タスクのステータス。 `normal` 、 `stopped` 、 `error` 、 `failed` 、または`finished`いずれかです。 |
| `target_ts`       | `UINT64`型。レプリケーション タスクのターゲット ts。                                                              |
| `task_status`     | レプリケーション タスクのディスパッチの詳細なステータス。                                                                 |

`task_status`パラメータは次のように説明されています。

| パラメータ名       | 説明                                         |
| :----------- | :----------------------------------------- |
| `capture_id` | `STRING`型。キャプチャ ID。                        |
| `table_ids`  | `UINT64 ARRAY`型。このキャプチャでレプリケートされるテーブルの ID。 |

`error`パラメータは次のように説明されています。

| パラメータ名    | 説明                    |
| :-------- | :-------------------- |
| `addr`    | `STRING`型。キャプチャ アドレス。 |
| `code`    | `STRING`型。エラーコード。     |
| `message` | `STRING`型。エラーの詳細。     |

## レプリケーション タスクを削除する {#remove-a-replication-task}

この API は、レプリケーション タスクを削除するためのべき等インターフェイスです (つまり、最初の適用を超えて結果を変更することなく、複数回適用できます)。リクエストが成功した場合、 `200 OK`が返されます。返された結果は、サーバーがコマンドの実行に同意したことを意味するだけで、コマンドが正常に実行されることを保証するものではありません。

### リクエストURI {#request-uri}

`DELETE /api/v2/changefeeds/{changefeed_id}`

### パラメータの説明 {#parameter-descriptions}

#### パス パラメータ {#path-parameters}

| パラメータ名          | 説明                                  |
| :-------------- | :---------------------------------- |
| `changefeed_id` | 削除するレプリケーション タスク (changefeed) の ID。 |

### 例 {#example}

次のリクエストは、ID `test1`のレプリケーション タスクを削除します。

```shell
curl -X DELETE http://127.0.0.1:8300/api/v2/changefeeds/test1
```

リクエストが成功した場合、 `200 OK`が返されます。リクエストが失敗すると、エラー メッセージとエラー コードが返されます。

## レプリケーション構成を更新する {#update-the-replication-configuration}

この API は、レプリケーション タスクの更新に使用されます。リクエストが成功した場合、 `200 OK`が返されます。返された結果は、サーバーがコマンドの実行に同意したことを意味するだけで、コマンドが正常に実行されることを保証するものではありません。

changefeed 構成を変更するには、 `pause the replication task -> modify the configuration -> resume the replication task`の手順に従います。

### リクエストURI {#request-uri}

`PUT /api/v2/changefeeds/{changefeed_id}`

### パラメータの説明 {#parameter-descriptions}

#### パス パラメータ {#path-parameters}

| パラメータ名          | 説明                                  |
| :-------------- | :---------------------------------- |
| `changefeed_id` | 更新するレプリケーション タスク (changefeed) の ID。 |

#### リクエスト本文のパラメータ {#parameters-for-the-request-body}

```json
{
  "replica_config": {
    "bdr_mode": true,
    "case_sensitive": true,
    "check_gc_safe_point": true,
    "consistent": {
      "flush_interval": 0,
      "level": "string",
      "max_log_size": 0,
      "storage": "string"
    },
    "enable_old_value": true,
    "enable_sync_point": true,
    "filter": {
      "do_dbs": [
        "string"
      ],
      "do_tables": [
        {
          "database_name": "string",
          "table_name": "string"
        }
      ],
      "event_filters": [
        {
          "ignore_delete_value_expr": "string",
          "ignore_event": [
            "string"
          ],
          "ignore_insert_value_expr": "string",
          "ignore_sql": [
            "string"
          ],
          "ignore_update_new_value_expr": "string",
          "ignore_update_old_value_expr": "string",
          "matcher": [
            "string"
          ]
        }
      ],
      "ignore_dbs": [
        "string"
      ],
      "ignore_tables": [
        {
          "database_name": "string",
          "table_name": "string"
        }
      ],
      "ignore_txn_start_ts": [
        0
      ],
      "rules": [
        "string"
      ]
    },
    "force_replicate": true,
    "ignore_ineligible_table": true,
    "memory_quota": 0,
    "mounter": {
      "worker_num": 0
    },
    "sink": {
      "column_selectors": [
        {
          "columns": [
            "string"
          ],
          "matcher": [
            "string"
          ]
        }
      ],
      "csv": {
        "delimiter": "string",
        "include_commit_ts": true,
        "null": "string",
        "quote": "string"
      },
      "date_separator": "string",
      "dispatchers": [
        {
          "matcher": [
            "string"
          ],
          "partition": "string",
          "topic": "string"
        }
      ],
      "enable_partition_separator": true,
      "encoder_concurrency": 0,
      "protocol": "string",
      "schema_registry": "string",
      "terminator": "string",
      "transaction_atomicity": "string"
    },
    "sync_point_interval": "string",
    "sync_point_retention": "string"
  },
  "sink_uri": "string",
  "target_ts": 0
}
```

現在、API を介して変更できるのは次の構成のみです。

| パラメータ名           | 説明                                               |
| :--------------- | :----------------------------------------------- |
| `target_ts`      | `UINT64`型。 changefeed のターゲット TSO を指定します。 (オプション) |
| `sink_uri`       | `STRING`型。レプリケーション タスクのダウンストリーム アドレス。 (オプション)    |
| `replica_config` | シンクの構成パラメーター。完全でなければなりません。 (オプション)               |

上記のパラメータの意味は、セクション[レプリケーション タスクを作成する](#create-a-replication-task)と同じです。詳細については、そのセクションを参照してください。

### 例 {#example}

次のリクエストは、レプリケーション タスクの`target_ts` ID `test1`から`32`に更新します。

```shell
 curl -X PUT -H "'Content-type':'application/json'" http://127.0.0.1:8300/api/v2/changefeeds/test1 -d '{"target_ts":32}'
```

リクエストが成功した場合、 `200 OK`が返されます。リクエストが失敗すると、エラー メッセージとエラー コードが返されます。 JSON レスポンスボディの意味は、セクション[レプリケーション タスクを作成する](#create-a-replication-task)と同じです。詳細については、そのセクションを参照してください。

## レプリケーション タスク リストを照会する {#query-the-replication-task-list}

この API は同期インターフェースです。リクエストが成功すると、TiCDC クラスター内のすべてのレプリケーション タスク (changefeed) の基本情報が返されます。

### リクエストURI {#request-uri}

`GET /api/v2/changefeeds`

### パラメータの説明 {#parameter-descriptions}

#### クエリ パラメータ {#query-parameter}

| パラメータ名  | 説明                                                      |
| :------ | :------------------------------------------------------ |
| `state` | このパラメーターを指定すると、この指定された状態のレプリケーション タスクの情報が返されます。 (オプション) |

`state`の値のオプションは`all` 、 `normal` 、 `stopped` 、 `error` 、 `failed` 、および`finished`です。

このパラメータが指定されていない場合、デフォルトで`normal` 、 `stopped` 、または`failed`状態のレプリケーション タスクの基本情報が返されます。

### 例 {#example}

次のリクエストは、状態`normal`のすべてのレプリケーション タスクの基本情報を照会します。

```shell
curl -X GET http://127.0.0.1:8300/api/v2/changefeeds?state=normal
```

```json
{
  "total": 2,
  "items": [
    {
      "id": "test",
      "state": "normal",
      "checkpoint_tso": 439749918821711874,
      "checkpoint_time": "2023-02-27 23:46:52.888",
      "error": null
    },
    {
      "id": "test2",
      "state": "normal",
      "checkpoint_tso": 439749918821711874,
      "checkpoint_time": "2023-02-27 23:46:52.888",
      "error": null
    }
  ]
}
```

上記の返された結果のパラメータは次のとおりです。

-   `id` : レプリケーション タスクの ID。
-   `state` : レプリケーション タスクの現在の[州](/ticdc/ticdc-changefeed-overview.md#changefeed-state-transfer) 。
-   `checkpoint_tso` : レプリケーション タスクの現在のチェックポイントの TSO。
-   `checkpoint_time` : レプリケーション タスクの現在のチェックポイントのフォーマットされた時刻。
-   `error` : レプリケーション タスクのエラー情報。

## 特定のレプリケーション タスクを照会する {#query-a-specific-replication-task}

この API は同期インターフェースです。リクエストが成功すると、指定されたレプリケーション タスク (changefeed) の詳細情報が返されます。

### リクエストURI {#request-uri}

`GET /api/v2/changefeeds/{changefeed_id}`

### パラメータの説明 {#parameter-description}

#### パス パラメータ {#path-parameter}

| パラメータ名          | 説明                           |
| :-------------- | :--------------------------- |
| `changefeed_id` | 照会する複製タスク (changefeed) の ID。 |

### 例 {#example}

次のリクエストは、ID `test1`のレプリケーション タスクの詳細情報を照会します。

```shell
curl -X GET http://127.0.0.1:8300/api/v2/changefeeds/test1
```

JSON レスポンスボディの意味は、 [レプリケーション タスクを作成する](#create-a-replication-task)節と同じです。詳細については、そのセクションを参照してください。

## レプリケーション タスクを一時停止する {#pause-a-replication-task}

この API は、レプリケーション タスクを一時停止します。リクエストが成功した場合、 `200 OK`が返されます。返された結果は、サーバーがコマンドの実行に同意したことを意味するだけで、コマンドが正常に実行されることを保証するものではありません。

### リクエストURI {#request-uri}

`POST /api/v2/changefeeds/{changefeed_id}/pause`

### パラメータの説明 {#parameter-description}

#### パス パラメータ {#path-parameter}

| パラメータ名          | 説明                                    |
| :-------------- | :------------------------------------ |
| `changefeed_id` | 一時停止するレプリケーション タスク (changefeed) の ID。 |

### 例 {#example}

次のリクエストは、ID `test1`のレプリケーション タスクを一時停止します。

```shell
curl -X POST http://127.0.0.1:8300/api/v2/changefeeds/test1/pause
```

リクエストが成功した場合、 `200 OK`が返されます。リクエストが失敗すると、エラー メッセージとエラー コードが返されます。

## レプリケーション タスクを再開する {#resume-a-replication-task}

この API は、レプリケーション タスクを再開します。リクエストが成功した場合、 `200 OK`が返されます。返された結果は、サーバーがコマンドの実行に同意したことを意味するだけで、コマンドが正常に実行されることを保証するものではありません。

### リクエストURI {#request-uri}

`POST /api/v2/changefeeds/{changefeed_id}/resume`

### パラメータの説明 {#parameter-description}

#### パス パラメータ {#path-parameter}

| パラメータ名          | 説明                                  |
| :-------------- | :---------------------------------- |
| `changefeed_id` | 再開するレプリケーション タスク (changefeed) の ID。 |

#### リクエスト本文のパラメータ {#parameters-for-the-request-body}

```json
{
  "overwrite_checkpoint_ts": 0
}
```

| パラメータ名                    | 説明                                                                   |
| :------------------------ | :------------------------------------------------------------------- |
| `overwrite_checkpoint_ts` | `UINT64`型。レプリケーション タスク (changefeed) を再開するときに、チェックポイント TSO を再割り当てします。 |

### 例 {#example}

次のリクエストは、ID `test1`のレプリケーション タスクを再開します。

```shell
curl -X POST http://127.0.0.1:8300/api/v2/changefeeds/test1/resume -d '{}'
```

リクエストが成功した場合、 `200 OK`が返されます。リクエストが失敗すると、エラー メッセージとエラー コードが返されます。

## レプリケーション サブタスク リストを照会する {#query-the-replication-subtask-list}

この API は同期インターフェースです。リクエストが成功すると、すべてのレプリケーション サブタスクの基本情報 ( `processor` ) が返されます。

### リクエストURI {#request-uri}

`GET /api/v2/processors`

### 例 {#example}

```shell
curl -X GET http://127.0.0.1:8300/api/v2/processors
```

```json
{
  "total": 3,
  "items": [
    {
      "changefeed_id": "test2",
      "capture_id": "d2912e63-3349-447c-90ba-72a4e04b5e9e"
    },
    {
      "changefeed_id": "test1",
      "capture_id": "d2912e63-3349-447c-90ba-72a4e04b5e9e"
    },
    {
      "changefeed_id": "test",
      "capture_id": "d2912e63-3349-447c-90ba-72a4e04b5e9e"
    }
  ]
}
```

パラメータの説明は次のとおりです。

-   `changefeed_id` : 変更フィード ID。
-   `capture_id` : キャプチャ ID。

## 特定のレプリケーション サブタスクを照会する {#query-a-specific-replication-subtask}

この API は同期インターフェースです。リクエストが成功すると、指定されたレプリケーション サブタスクの詳細情報 ( `processor` ) が返されます。

### リクエストURI {#request-uri}

`GET /api/v2/processors/{changefeed_id}/{capture_id}`

### パラメータの説明 {#parameter-descriptions}

#### パス パラメータ {#path-parameters}

| パラメータ名          | 説明                             |
| :-------------- | :----------------------------- |
| `changefeed_id` | 照会する複製サブタスクの変更フィード ID。         |
| `capture_id`    | クエリ対象のレプリケーション サブタスクのキャプチャ ID。 |

### 例 {#example}

次のリクエストは、 `changefeed_id`が`test`で`capture_id`が`561c3784-77f0-4863-ad52-65a3436db6af`のサブタスクの詳細情報を照会します。サブタスクは`changefeed_id`と`capture_id`で識別できます。

```shell
curl -X GET http://127.0.0.1:8300/api/v2/processors/test/561c3784-77f0-4863-ad52-65a3436db6af
```

```json
{
  "table_ids": [
    80
  ]
}
```

パラメータは次のように記述されます。

-   `table_ids` : このキャプチャでレプリケートされるテーブル ID。

## TiCDC サービス プロセス リストのクエリ {#query-the-ticdc-service-process-list}

この API は同期インターフェースです。リクエストが成功すると、すべてのレプリケーション プロセスの基本情報 ( `capture` ) が返されます。

### リクエストURI {#request-uri}

`GET /api/v2/captures`

### 例 {#example}

```shell
curl -X GET http://127.0.0.1:8300/api/v2/captures
```

```json
{
  "total": 1,
  "items": [
    {
      "id": "d2912e63-3349-447c-90ba-72a4e04b5e9e",
      "is_owner": true,
      "address": "127.0.0.1:8300"
    }
  ]
}
```

パラメータの説明は次のとおりです。

-   `id` : キャプチャ ID。
-   `is_owner` : キャプチャが所有者かどうか。
-   `address` : キャプチャのアドレス。

## 所有者ノードを削除する {#evict-an-owner-node}

この API は非同期インターフェースです。リクエストが成功した場合、 `200 OK`が返されます。返された結果は、サーバーがコマンドの実行に同意したことを意味するだけで、コマンドが正常に実行されることを保証するものではありません。

### リクエストURI {#request-uri}

`POST /api/v2/owner/resign`

### 例 {#example}

次のリクエストは、TiCDC の現在の所有者ノードを削除し、新しい所有者ノードを生成するための新しいラウンドの選挙をトリガーします。

```shell
curl -X POST http://127.0.0.1:8300/api/v2/owner/resign
```

リクエストが成功した場合、 `200 OK`が返されます。リクエストが失敗すると、エラー メッセージとエラー コードが返されます。

## TiCDCサーバーのログレベルを動的に調整する {#dynamically-adjust-the-log-level-of-the-ticdc-server}

この API は同期インターフェースです。リクエストが成功した場合、 `200 OK`が返されます。

### リクエストURI {#request-uri}

`POST /api/v2/log`

### リクエストパラメータ {#request-parameter}

#### リクエストボディのパラメータ {#parameter-for-the-request-body}

| パラメータ名      | 説明          |
| :---------- | :---------- |
| `log_level` | 設定するログ レベル。 |

`log_level` [zap によって提供されるログ レベル](https://godoc.org/go.uber.org/zap#UnmarshalText)サポートします: &quot;debug&quot;、&quot;info&quot;、&quot;warn&quot;、&quot;error&quot;、&quot;dpanic&quot;、&quot;panic&quot;、および &quot;fatal&quot;。

### 例 {#example}

```shell
curl -X POST -H "'Content-type':'application/json'" http://127.0.0.1:8300/api/v2/log -d '{"log_level":"debug"}'
```

リクエストが成功した場合、 `200 OK`が返されます。リクエストが失敗すると、エラー メッセージとエラー コードが返されます。
