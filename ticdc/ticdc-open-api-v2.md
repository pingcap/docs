---
title: TiCDC OpenAPI v2
summary: Learn how to use the OpenAPI v2 interface to manage the cluster status and data replication.
---

# TiCDC OpenAPI v2 {#ticdc-openapi-v2}

<!-- markdownlint-disable MD024 -->

TiCDC は、TiCDC クラスターのクエリと操作のための OpenAPI 機能を提供します。 OpenAPI 機能は[`cdc cli`ツール](/ticdc/ticdc-manage-changefeed.md)のサブセットです。

> **注記：**
>
> TiCDC OpenAPI v1 は将来削除される予定です。 TiCDC OpenAPI v2 を使用することをお勧めします。

API を使用して、TiCDC クラスター上で次のメンテナンス操作を実行できます。

-   [TiCDC ノードのステータス情報を取得する](#get-the-status-information-of-a-ticdc-node)
-   [TiCDC クラスターの健全性ステータスを確認する](#check-the-health-status-of-a-ticdc-cluster)
-   [レプリケーションタスクを作成する](#create-a-replication-task)
-   [レプリケーションタスクを削除する](#remove-a-replication-task)
-   [レプリケーション構成を更新する](#update-the-replication-configuration)
-   [レプリケーションタスクリストのクエリ](#query-the-replication-task-list)
-   [特定のレプリケーションタスクをクエリする](#query-a-specific-replication-task)
-   [レプリケーションタスクを一時停止する](#pause-a-replication-task)
-   [レプリケーションタスクを再開する](#resume-a-replication-task)
-   [レプリケーションサブタスクリストのクエリ](#query-the-replication-subtask-list)
-   [特定のレプリケーションサブタスクをクエリする](#query-a-specific-replication-subtask)
-   [TiCDC サービス プロセス リストのクエリ](#query-the-ticdc-service-process-list)
-   [所有者ノードを削除する](#evict-an-owner-node)
-   [TiCDCサーバーのログ レベルを動的に調整する](#dynamically-adjust-the-log-level-of-the-ticdc-server)

すべての API のリクエスト本文と戻り値は JSON 形式です。リクエストが成功すると、 `200 OK`メッセージが返されます。次のセクションでは、API の具体的な使用法について説明します。

次の例では、TiCDCサーバーのリスニング IP アドレスは`127.0.0.1` 、ポートは`8300`です。 TiCDCサーバーを起動するときに、 `--addr=ip:port`介して TiCDC にバインドされる IP アドレスとポートを指定できます。

## APIエラーメッセージテンプレート {#api-error-message-template}

API リクエストの送信後にエラーが発生した場合、返されるエラー メッセージは次の形式になります。

```json
{
    "error_msg": "",
    "error_code": ""
}
```

上記の JSON 出力では、 `error_msg`エラー メッセージを示し、 `error_code`は対応するエラー コードを示します。

## APIリストインターフェースの戻り形式 {#return-format-of-the-api-list-interface}

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

上の例では:

-   `total` : リソースの総数を示します。
-   `items` : このリクエストによって返されたすべてのリソースを含む配列。配列のすべての要素は同じリソースに属します。

## TiCDC ノードのステータス情報を取得する {#get-the-status-information-of-a-ticdc-node}

この API は同期インターフェイスです。リクエストが成功すると、該当ノードのステータス情報が返されます。

### リクエストURI {#request-uri}

`GET /api/v2/status`

### 例 {#example}

次のリクエストは、IP アドレスが`127.0.0.1`でポート番号が`8300` TiCDC ノードのステータス情報を取得します。

```shell
curl -X GET http://127.0.0.1:8300/api/v2/status
```

```json
{
  "version": "v7.1.2",
  "git_hash": "10413bded1bdb2850aa6d7b94eb375102e9c44dc",
  "id": "d2912e63-3349-447c-90ba-72a4e04b5e9e",
  "pid": 1447,
  "is_owner": true,
  "liveness": 0
}
```

上記の出力のパラメータは次のように説明されます。

-   `version` : TiCDC の現在のバージョン番号。
-   `git_hash` : Git ハッシュ値。
-   `id` : ノードのキャプチャ ID。
-   `pid` : ノードのキャプチャ プロセス ID (PID)。
-   `is_owner` : ノードが所有者であるかどうかを示します。
-   `liveness` : このノードがライブであるかどうか。 `0`通常を意味します。 `1`ノードが`graceful shutdown`状態にあることを意味します。

## TiCDC クラスターの健全性ステータスを確認する {#check-the-health-status-of-a-ticdc-cluster}

この API は同期インターフェイスです。クラスターが正常な場合は`200 OK`が返されます。

### リクエストURI {#request-uri}

`GET /api/v2/health`

### 例 {#example}

```shell
curl -X GET http://127.0.0.1:8300/api/v2/health
```

クラスターが正常な場合、応答は`200 OK`で空の JSON オブジェクトになります。

```json
{}
```

クラスターが正常でない場合、応答はエラー メッセージを含む JSON オブジェクトです。

## レプリケーションタスクを作成する {#create-a-replication-task}

このインターフェイスは、レプリケーション タスクを TiCDC に送信するために使用されます。リクエストが成功すると`200 OK`が返されます。返された結果は、サーバーがコマンドの実行に同意したことを意味するだけで、コマンドが正常に実行されることを保証するものではありません。

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

パラメータは次のように説明されます。

| パラメータ名           | 説明                                                                                                                           |
| :--------------- | :--------------------------------------------------------------------------------------------------------------------------- |
| `changefeed_id`  | `STRING`タイプ。レプリケーションタスクのID。 (オプション)                                                                                          |
| `replica_config` | レプリケーションタスクのコンフィグレーションパラメータ。 (オプション)                                                                                         |
| **`sink_uri`**   | `STRING`タイプ。レプリケーションタスクの下流アドレス。 （**必須**）                                                                                     |
| `start_ts`       | `UINT64`タイプ。変更フィードの開始 TSO を指定します。 TiCDC クラスターは、この TSO からのデータのプルを開始します。デフォルト値は現在時刻です。 (オプション)                                 |
| `target_ts`      | `UINT64`タイプ。変更フィードのターゲット TSO を指定します。 TiCDC クラスターは、この TSO に到達するとデータのプルを停止します。デフォルト値は空です。これは、TiCDC が自動的に停止しないことを意味します。 (オプション) |

`changefeed_id` 、 `start_ts` 、 `target_ts` 、 `sink_uri`の意味と形式は、ドキュメント[`cdc cli`を使用してレプリケーション タスクを作成する](/ticdc/ticdc-manage-changefeed.md#create-a-replication-task)に記載されているものと同じです。これらのパラメータの詳細については、そのドキュメントを参照してください。 `sink_uri`で証明書のパスを指定する場合は、対応する証明書を対応する TiCDCサーバーにアップロードしていることを確認してください。

`replica_config`パラメータの説明は次のとおりです。

| パラメータ名                    | 説明                                                                                                                                                                           |
| :------------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `bdr_mode`                | `BOOLEAN`タイプ。 [双方向レプリケーション](/ticdc/ticdc-bidirectional-replication.md)を有効にするかどうかを決定します。デフォルト値は`false`です。 (オプション)                                                             |
| `case_sensitive`          | `BOOLEAN`タイプ。テーブル名をフィルタリングするときに大文字と小文字を区別するかどうかを決定します。デフォルト値は`true`です。 (オプション)                                                                                               |
| `check_gc_safe_point`     | `BOOLEAN`タイプ。レプリケーション タスクの開始時刻が GC 時刻よりも前であることを確認するかどうかを決定します。デフォルト値は`true`です。 (オプション)                                                                                       |
| `consistent`              | REDO ログの構成パラメータ。 (オプション)                                                                                                                                                     |
| `enable_old_value`        | `BOOLEAN`タイプ。古い値（更新前の値）を出力するかどうかを決定します。デフォルト値は`true`です。 (オプション)                                                                                                              |
| `enable_sync_point`       | `BOOLEAN`タイプ。 `sync point`を有効にするかどうかを決定します。 (オプション)                                                                                                                          |
| `filter`                  | `filter`の構成パラメータ。 (オプション)                                                                                                                                                    |
| `force_replicate`         | `BOOLEAN`タイプ。デフォルト値は`false`です。これを`true`に設定すると、レプリケーション タスクは一意のインデックスのないテーブルを強制的にレプリケートします。 (オプション)                                                                           |
| `ignore_ineligible_table` | `BOOLEAN`タイプ。デフォルト値は`false`です。これを`true`に設定すると、レプリケーション タスクはレプリケートできないテーブルを無視します。 (オプション)                                                                                     |
| `memory_quota`            | `UINT64`タイプ。レプリケーション タスクのメモリクォータ。 (オプション)                                                                                                                                    |
| `mounter`                 | `mounter`の構成パラメータ。 (オプション)                                                                                                                                                   |
| `sink`                    | `sink`の構成パラメータ。 (オプション)                                                                                                                                                      |
| `sync_point_interval`     | `STRING`タイプ。戻り値は`UINT64`種類のナノ秒単位の時間であることに注意してください。 `sync point`機能が有効な場合、このパラメータは、Syncpoint がアップストリームとダウンストリームのスナップショットを調整する間隔を指定します。デフォルト値は`10m`で、最小値は`30s`です。 (オプション)       |
| `sync_point_retention`    | `STRING`タイプ。戻り値は`UINT64`種類のナノ秒単位の時間であることに注意してください。 `sync point`機能が有効な場合、このパラメータは、同期ポイントによってダウンストリーム テーブルにデータが保持される期間を指定します。この期間を超えると、データはクリーンアップされます。デフォルト値は`24h`です。 (オプション) |

`consistent`パラメータは次のように説明されます。

| パラメータ名           | 説明                                           |
| :--------------- | :------------------------------------------- |
| `flush_interval` | `UINT64`タイプ。 REDO ログ ファイルをフラッシュする間隔。 (オプション) |
| `level`          | `STRING`タイプ。レプリケートされたデータの整合性レベル。 (オプション)     |
| `max_log_size`   | `UINT64`タイプ。 REDOログの最大値。 (オプション)             |
| `storage`        | `STRING`タイプ。storageの宛先アドレス。 (オプション)          |

`filter`パラメータは次のように説明されます。

| パラメータ名                | 説明                                                                                                                           |
| :-------------------- | :--------------------------------------------------------------------------------------------------------------------------- |
| `do_dbs`              | `STRING ARRAY`タイプ。レプリケートされるデータベース。 (オプション)                                                                                   |
| `do_tables`           | レプリケートされるテーブル。 (オプション)                                                                                                       |
| `ignore_dbs`          | `STRING ARRAY`タイプ。無視されるデータベース。 (オプション)                                                                                       |
| `ignore_tables`       | 無視されるテーブル。 (オプション)                                                                                                           |
| `event_filters`       | イベントをフィルタリングするための構成。 (オプション)                                                                                                 |
| `ignore_txn_start_ts` | `UINT64 ARRAY`タイプ。これを指定すると、 `[1, 2]`などの`start_ts`を指定したトランザクションは無視されます。 (オプション)                                               |
| `rules`               | `STRING ARRAY`タイプ。テーブル スキーマ フィルタリングのルール ( `['foo*.*', 'bar*.*']`など)。詳細については、 [テーブルフィルター](/table-filter.md)を参照してください。 (オプション) |

`filter.event_filters`パラメータは次のように説明されます。詳細については、 [変更フィードログフィルター](/ticdc/ticdc-filter.md)を参照してください。

| パラメータ名                         | 説明                                                                                                                          |
| :----------------------------- | :-------------------------------------------------------------------------------------------------------------------------- |
| `ignore_delete_value_expr`     | `STRING ARRAY`タイプ。たとえば、 `"name = 'john'"` 、 `name = 'john'`条件を含む DELETE DML ステートメントをフィルターで除外することを意味します。 (オプション)             |
| `ignore_event`                 | `STRING ARRAY`タイプ。たとえば、 `["insert"]` INSERT イベントがフィルターで除外されることを示します。 (オプション)                                                |
| `ignore_insert_value_expr`     | `STRING ARRAY`タイプ。たとえば、 `"id >= 100"` 、条件`id >= 100`に一致する INSERT DML ステートメントを除外することを意味します。 (オプション)                          |
| `ignore_sql`                   | `STRING ARRAY`タイプ。たとえば、 `["^drop", "add column"]` 、 `DROP`で始まるか、 `ADD COLUMN`を含む DDL ステートメントをフィルタリングして除外することを意味します。 (オプション) |
| `ignore_update_new_value_expr` | `STRING ARRAY`タイプ。たとえば、 `"gender = 'male'"` 、新しい値`gender = 'male'`を持つ UPDATE DML ステートメントをフィルターで除外することを意味します。 (オプション)        |
| `ignore_update_old_value_expr` | `STRING ARRAY`タイプ。たとえば、 `"age < 18"` 、古い値`age < 18`を持つ UPDATE DML ステートメントをフィルタリングして除外することを意味します。 (オプション)                    |
| `matcher`                      | `STRING ARRAY`タイプ。ホワイトリストとして機能します。たとえば、 `["test.worker"]` 、フィルタ ルールが`test`データベース内の`worker`テーブルにのみ適用されることを意味します。 (オプション)     |

`mounter`パラメータは次のように説明されます。

| パラメータ名       | 説明                                                                               |
| :----------- | :------------------------------------------------------------------------------- |
| `worker_num` | `INT`タイプ。マウンタのスレッド数。マウンタは、TiKV から出力されたデータをデコードするために使用されます。デフォルト値は`16`です。 (オプション) |

`sink`パラメータは次のように説明されます。

| パラメータ名                        | 説明                                                                                                                                 |
| :---------------------------- | :--------------------------------------------------------------------------------------------------------------------------------- |
| `column_selectors`            | 列セレクターの構成。 (オプション)                                                                                                                 |
| `csv`                         | CSV 構成。 (オプション)                                                                                                                    |
| `date_separator`              | `STRING`タイプ。ファイルディレクトリの日付区切り文字のタイプを示します。値のオプションは`none` 、 `year` 、 `month` 、および`day`です。 `none`はデフォルト値で、日付が区切られていないことを意味します。 (オプション) |
| `dispatchers`                 | イベントディスパッチ用の構成配列。 (オプション)                                                                                                          |
| `encoder_concurrency`         | `INT`タイプ。 MQ シンク内のエンコーダー スレッドの数。デフォルト値は`16`です。 (オプション)                                                                             |
| `protocol`                    | `STRING`タイプ。 MQ シンクの場合、メッセージのプロトコル形式を指定できます。現在サポートされているプロトコルは`canal-json` 、 `open-protocol` 、 `canal` 、 `avro` 、および`maxwell`です。    |
| `schema_registry`             | `STRING`タイプ。スキーマ レジストリ アドレス。 (オプション)                                                                                               |
| `terminator`                  | `STRING`タイプ。ターミネータは、2 つのデータ変更イベントを区切るために使用されます。デフォルト値は null です。これは、 `"\r\n"`がターミネータとして使用されることを意味します。 (オプション)                       |
| `transaction_atomicity`       | `STRING`タイプ。トランザクションのアトミックレベル。 (オプション)                                                                                             |
| `only_output_updated_columns` | `BOOLEAN`タイプ。 `canal-json`または`open-protocol`プロトコルを使用する MQ シンクの場合、変更された列のみを出力するかどうかを指定できます。デフォルト値は`false`です。 (オプション)                |

`sink.column_selectors`は配列です。パラメータは次のように説明されます。

| パラメータ名    | 説明                                                |
| :-------- | :------------------------------------------------ |
| `columns` | `STRING ARRAY`タイプ。列配列。                            |
| `matcher` | `STRING ARRAY`タイプ。マッチャーの構成。フィルター ルールと同じ一致構文を持ちます。 |

`sink.csv`パラメータは次のように説明されます。

| パラメータ名              | 説明                                                                          |
| :------------------ | :-------------------------------------------------------------------------- |
| `delimiter`         | `STRING`タイプ。 CSV ファイル内のフィールドを区切るために使用される文字。値は ASCII 文字である必要があり、デフォルトは`,`です。 |
| `include_commit_ts` | `BOOLEAN`タイプ。 CSV 行に commit-t を含めるかどうか。デフォルト値は`false`です。                    |
| `null`              | `STRING`タイプ。 CSV 列が null の場合に表示される文字。デフォルト値は`\N`です。                         |
| `quote`             | `STRING`タイプ。 CSV ファイル内のフィールドを囲むために使用される引用符。値が空の場合、引用符は使用されません。デフォルト値は`"`です。 |

`sink.dispatchers` : MQ タイプのシンクの場合、このパラメーターを使用してイベント ディスパッチャーを構成できます。次のディスパッチャーがサポートされています: `default` 、 `ts` 、 `rowid` 、および`table` 。ディスパッチャのルールは次のとおりです。

-   `default` : 複数の一意のインデックス (主キーを含む) が存在する場合、イベントはテーブル モードで送出されます。一意のインデックス (または主キー) が 1 つだけ存在する場合、イベントは ROWID モードで送出されます。 Old Value 機能が有効になっている場合、イベントはテーブル モードでディスパッチされます。
-   `ts` : 行変更の commitT を使用してハッシュ値を作成し、イベントをディスパッチします。
-   `rowid` : 選択した HandleKey 列の名前と値を使用して、ハッシュ値を作成し、イベントをディスパッチします。
-   `table` : テーブルのスキーマ名とテーブル名を使用してハッシュ値を作成し、イベントをディスパッチします。

`sink.dispatchers`は配列です。パラメータは次のように説明されます。

| パラメータ名      | 説明                                         |
| :---------- | :----------------------------------------- |
| `matcher`   | `STRING ARRAY`タイプ。フィルター ルールと同じ一致構文を持ちます。   |
| `partition` | `STRING`タイプ。イベントをディスパッチするためのターゲット パーティション。 |
| `topic`     | `STRING`タイプ。イベントをディスパッチする対象のトピック。          |

### 例 {#example}

次のリクエストは、ID が`test5`および`sink_uri` `blackhome://`タスクを作成します。

```shell
curl -X POST -H "'Content-type':'application/json'" http://127.0.0.1:8300/api/v2/changefeeds -d '{"changefeed_id":"test5","sink_uri":"blackhole://"}'
```

リクエストが成功すると`200 OK`が返されます。リクエストが失敗した場合は、エラー メッセージとエラー コードが返されます。

### レスポンスボディの形式 {#response-body-format}

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

パラメータは次のように説明されます。

| パラメータ名            | 説明                                                                                     |
| :---------------- | :------------------------------------------------------------------------------------- |
| `admin_job_type`  | `INTEGER`タイプ。管理者のジョブタイプ。                                                               |
| `checkpoint_time` | `STRING`タイプ。レプリケーション タスクの現在のチェックポイントの形式化された時刻。                                         |
| `checkpoint_ts`   | `STRING`タイプ。レプリケーション タスクの現在のチェックポイントの TSO。                                             |
| `config`          | レプリケーションタスクの構成。構造と意味はレプリケーションタスク作成時の構成`replica_config`と同じです。                           |
| `create_time`     | `STRING`タイプ。レプリケーションタスクが作成された時刻。                                                       |
| `creator_version` | `STRING`タイプ。レプリケーション タスクが作成されたときの TiCDC バージョン。                                         |
| `error`           | レプリケーションタスクのエラー。                                                                       |
| `id`              | `STRING`タイプ。レプリケーションタスクID。                                                             |
| `resolved_ts`     | `UINT64`タイプ。レプリケーション タスクにより ts が解決されました。                                               |
| `sink_uri`        | `STRING`タイプ。レプリケーション タスクのシンク URI。                                                      |
| `start_ts`        | `UINT64`タイプ。レプリケーション タスクが ts を開始します。                                                   |
| `state`           | `STRING`タイプ。レプリケーションタスクのステータス。 `normal` 、または`finished` `failed` `error` `stopped`なります。 |
| `target_ts`       | `UINT64`タイプ。レプリケーションタスクのターゲット ts。                                                      |
| `task_status`     | レプリケーションタスクのディスパッチの詳細なステータス。                                                           |

`task_status`パラメータは次のように説明されます。

| パラメータ名       | 説明                                           |
| :----------- | :------------------------------------------- |
| `capture_id` | `STRING`タイプ。キャプチャID。                         |
| `table_ids`  | `UINT64 ARRAY`タイプ。このキャプチャでレプリケートされるテーブルの ID。 |

`error`パラメータは次のように説明されます。

| パラメータ名    | 説明                     |
| :-------- | :--------------------- |
| `addr`    | `STRING`タイプ。キャプチャアドレス。 |
| `code`    | `STRING`タイプ。エラーコード。    |
| `message` | `STRING`タイプ。エラーの詳細。    |

## レプリケーションタスクを削除する {#remove-a-replication-task}

この API は、レプリケーション タスクを削除するための冪等インターフェイス (つまり、最初の適用を超えて結果を変更することなく複数回適用できます) です。リクエストが成功すると`200 OK`が返されます。返された結果は、サーバーがコマンドの実行に同意したことを意味するだけで、コマンドが正常に実行されることを保証するものではありません。

### リクエストURI {#request-uri}

`DELETE /api/v2/changefeeds/{changefeed_id}`

### パラメータの説明 {#parameter-descriptions}

#### パスパラメータ {#path-parameters}

| パラメータ名          | 説明                              |
| :-------------- | :------------------------------ |
| `changefeed_id` | 削除するレプリケーション タスク (変更フィード) の ID。 |

### 例 {#example}

次のリクエストは、ID `test1`のレプリケーション タスクを削除します。

```shell
curl -X DELETE http://127.0.0.1:8300/api/v2/changefeeds/test1
```

リクエストが成功すると`200 OK`が返されます。リクエストが失敗した場合は、エラー メッセージとエラー コードが返されます。

## レプリケーション構成を更新する {#update-the-replication-configuration}

この API は、レプリケーション タスクを更新するために使用されます。リクエストが成功すると`200 OK`が返されます。返された結果は、サーバーがコマンドの実行に同意したことを意味するだけで、コマンドが正常に実行されることを保証するものではありません。

チェンジフィード構成を変更するには、 `pause the replication task -> modify the configuration -> resume the replication task`の手順に従います。

### リクエストURI {#request-uri}

`PUT /api/v2/changefeeds/{changefeed_id}`

### パラメータの説明 {#parameter-descriptions}

#### パスパラメータ {#path-parameters}

| パラメータ名          | 説明                              |
| :-------------- | :------------------------------ |
| `changefeed_id` | 更新するレプリケーション タスク (変更フィード) の ID。 |

#### リクエストボディのパラメータ {#parameters-for-the-request-body}

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

現在、API 経由で変更できるのは次の構成のみです。

| パラメータ名           | 説明                                           |
| :--------------- | :------------------------------------------- |
| `target_ts`      | `UINT64`タイプ。変更フィードのターゲット TSO を指定します。 (オプション) |
| `sink_uri`       | `STRING`タイプ。レプリケーションタスクの下流アドレス。 (オプション)      |
| `replica_config` | シンクの構成パラメータ。それは完全でなければなりません。 (オプション)         |

上記パラメータの意味は[レプリケーションタスクを作成する](#create-a-replication-task)項と同様です。詳細については、そのセクションを参照してください。

### 例 {#example}

次のリクエストは、ID が`test1`レプリケーション タスクの`target_ts`を`32`に更新します。

```shell
 curl -X PUT -H "'Content-type':'application/json'" http://127.0.0.1:8300/api/v2/changefeeds/test1 -d '{"target_ts":32}'
```

リクエストが成功すると`200 OK`が返されます。リクエストが失敗した場合は、エラー メッセージとエラー コードが返されます。 JSON レスポンスボディの意味は[レプリケーションタスクを作成する](#create-a-replication-task)セクションと同じです。詳細については、そのセクションを参照してください。

## レプリケーションタスクリストのクエリ {#query-the-replication-task-list}

この API は同期インターフェイスです。リクエストが成功すると、TiCDC クラスター内のすべてのレプリケーション タスク (変更フィード) の基本情報が返されます。

### リクエストURI {#request-uri}

`GET /api/v2/changefeeds`

### パラメータの説明 {#parameter-descriptions}

#### クエリパラメータ {#query-parameter}

| パラメータ名  | 説明                                                    |
| :------ | :---------------------------------------------------- |
| `state` | このパラメータを指定すると、その指定された状態のレプリケーションタスクの情報が返されます。 (オプション) |

`state`の値のオプションは`all` 、 `normal` 、 `stopped` 、 `error` 、 `failed` 、および`finished`です。

このパラメータが指定されていない場合、デフォルトでは、 `normal` 、 `stopped` 、または`failed`状態のレプリケーション タスクの基本情報が返されます。

### 例 {#example}

次のリクエストは、 `normal`状態のすべてのレプリケーション タスクの基本情報をクエリします。

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

上記で返された結果のパラメータは次のように説明されます。

-   `id` : レプリケーション タスクの ID。
-   `state` : レプリケーションタスクの現在の[州](/ticdc/ticdc-changefeed-overview.md#changefeed-state-transfer) 。
-   `checkpoint_tso` : レプリケーション タスクの現在のチェックポイントの TSO。
-   `checkpoint_time` : レプリケーション タスクの現在のチェックポイントのフォーマットされた時刻。
-   `error` : レプリケーションタスクのエラー情報。

## 特定のレプリケーションタスクをクエリする {#query-a-specific-replication-task}

この API は同期インターフェイスです。リクエストが成功すると、指定したレプリケーションタスクの詳細情報（変更フィード）が返されます。

### リクエストURI {#request-uri}

`GET /api/v2/changefeeds/{changefeed_id}`

### パラメータの説明 {#parameter-description}

#### パスパラメータ {#path-parameter}

| パラメータ名          | 説明                                |
| :-------------- | :-------------------------------- |
| `changefeed_id` | クエリ対象のレプリケーション タスク (変更フィード) の ID。 |

### 例 {#example}

次のリクエストは、ID `test1`のレプリケーション タスクの詳細情報をクエリします。

```shell
curl -X GET http://127.0.0.1:8300/api/v2/changefeeds/test1
```

JSON レスポンスボディの意味は[レプリケーションタスクを作成する](#create-a-replication-task)セクションと同じです。詳細については、そのセクションを参照してください。

## レプリケーションタスクを一時停止する {#pause-a-replication-task}

この API はレプリケーション タスクを一時停止します。リクエストが成功すると`200 OK`が返されます。返された結果は、サーバーがコマンドの実行に同意したことを意味するだけで、コマンドが正常に実行されることを保証するものではありません。

### リクエストURI {#request-uri}

`POST /api/v2/changefeeds/{changefeed_id}/pause`

### パラメータの説明 {#parameter-description}

#### パスパラメータ {#path-parameter}

| パラメータ名          | 説明                                |
| :-------------- | :-------------------------------- |
| `changefeed_id` | 一時停止するレプリケーション タスク (変更フィード) の ID。 |

### 例 {#example}

次のリクエストは、ID `test1`のレプリケーション タスクを一時停止します。

```shell
curl -X POST http://127.0.0.1:8300/api/v2/changefeeds/test1/pause
```

リクエストが成功すると`200 OK`が返されます。リクエストが失敗した場合は、エラー メッセージとエラー コードが返されます。

## レプリケーションタスクを再開する {#resume-a-replication-task}

この API はレプリケーション タスクを再開します。リクエストが成功すると`200 OK`が返されます。返された結果は、サーバーがコマンドの実行に同意したことを意味するだけで、コマンドが正常に実行されることを保証するものではありません。

### リクエストURI {#request-uri}

`POST /api/v2/changefeeds/{changefeed_id}/resume`

### パラメータの説明 {#parameter-description}

#### パスパラメータ {#path-parameter}

| パラメータ名          | 説明                              |
| :-------------- | :------------------------------ |
| `changefeed_id` | 再開するレプリケーション タスク (変更フィード) の ID。 |

#### リクエストボディのパラメータ {#parameters-for-the-request-body}

```json
{
  "overwrite_checkpoint_ts": 0
}
```

| パラメータ名                    | 説明                                                                 |
| :------------------------ | :----------------------------------------------------------------- |
| `overwrite_checkpoint_ts` | `UINT64`タイプ。レプリケーション タスク (変更フィード) を再開するときに、チェックポイント TSO を再割り当てします。 |

### 例 {#example}

次のリクエストは、ID `test1`のレプリケーション タスクを再開します。

```shell
curl -X POST http://127.0.0.1:8300/api/v2/changefeeds/test1/resume -d '{}'
```

リクエストが成功すると`200 OK`が返されます。リクエストが失敗した場合は、エラー メッセージとエラー コードが返されます。

## レプリケーションサブタスクリストのクエリ {#query-the-replication-subtask-list}

この API は同期インターフェイスです。リクエストが成功すると、すべてのレプリケーション サブタスク ( `processor` ) の基本情報が返されます。

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

パラメータは次のように説明されます。

-   `changefeed_id` : チェンジフィード ID。
-   `capture_id` : キャプチャID。

## 特定のレプリケーションサブタスクをクエリする {#query-a-specific-replication-subtask}

この API は同期インターフェイスです。リクエストが成功すると、指定されたレプリケーションサブタスク ( `processor` ) の詳細情報が返されます。

### リクエストURI {#request-uri}

`GET /api/v2/processors/{changefeed_id}/{capture_id}`

### パラメータの説明 {#parameter-descriptions}

#### パスパラメータ {#path-parameters}

| パラメータ名          | 説明                              |
| :-------------- | :------------------------------ |
| `changefeed_id` | クエリ対象のレプリケーション サブタスクの変更フィード ID。 |
| `capture_id`    | クエリ対象のレプリケーション サブタスクのキャプチャ ID。  |

### 例 {#example}

次のリクエストは、 `changefeed_id`が`test` 、 `capture_id`が`561c3784-77f0-4863-ad52-65a3436db6af`であるサブタスクの詳細情報をクエリします。サブタスクは`changefeed_id`と`capture_id`で識別できます。

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

パラメータは次のように説明されます。

-   `table_ids` : このキャプチャでレプリケートされるテーブル ID。

## TiCDC サービス プロセス リストのクエリ {#query-the-ticdc-service-process-list}

この API は同期インターフェイスです。リクエストが成功すると、すべてのレプリケーション プロセスの基本情報 ( `capture` ) が返されます。

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

パラメータは次のように説明されます。

-   `id` : キャプチャID。
-   `is_owner` : キャプチャが所有者であるかどうか。
-   `address` : キャプチャのアドレス。

## 所有者ノードを削除する {#evict-an-owner-node}

この API は非同期インターフェイスです。リクエストが成功すると`200 OK`が返されます。返された結果は、サーバーがコマンドの実行に同意したことを意味するだけで、コマンドが正常に実行されることを保証するものではありません。

### リクエストURI {#request-uri}

`POST /api/v2/owner/resign`

### 例 {#example}

次のリクエストは、TiCDC の現在の所有者ノードを削除し、新しいラウンドの選挙をトリガーして新しい所有者ノードを生成します。

```shell
curl -X POST http://127.0.0.1:8300/api/v2/owner/resign
```

リクエストが成功すると`200 OK`が返されます。リクエストが失敗した場合は、エラー メッセージとエラー コードが返されます。

## TiCDCサーバーのログ レベルを動的に調整する {#dynamically-adjust-the-log-level-of-the-ticdc-server}

この API は同期インターフェイスです。リクエストが成功すると`200 OK`が返されます。

### リクエストURI {#request-uri}

`POST /api/v2/log`

### リクエストパラメータ {#request-parameter}

#### リクエストボディのパラメータ {#parameter-for-the-request-body}

| パラメータ名      | 説明         |
| :---------- | :--------- |
| `log_level` | 設定するログレベル。 |

`log_level` 「debug」、「info」、「warn」、「error」、「dpanic」、「panic」、および「fatal」の[zap によって提供されるログ レベル](https://godoc.org/go.uber.org/zap#UnmarshalText)をサポートします。

### 例 {#example}

```shell
curl -X POST -H "'Content-type':'application/json'" http://127.0.0.1:8300/api/v2/log -d '{"log_level":"debug"}'
```

リクエストが成功すると`200 OK`が返されます。リクエストが失敗した場合は、エラー メッセージとエラー コードが返されます。
