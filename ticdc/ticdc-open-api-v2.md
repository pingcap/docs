---
title: TiCDC OpenAPI v2
summary: OpenAPI v2 インターフェースを使用してクラスターのステータスとデータレプリケーションを管理する方法を学習します。
---

# TiCDC オープンAPI v2 {#ticdc-openapi-v2}

<!-- markdownlint-disable MD024 -->

TiCDCは、TiCDCクラスターのクエリと操作のためのOpenAPI機能を提供します。OpenAPI機能は、 [`cdc cli`ツール](/ticdc/ticdc-manage-changefeed.md)のサブセットです。

> **注記：**
>
> TiCDC OpenAPI v1は将来削除される予定です。TiCDC OpenAPI v2のご利用をお勧めします。

API を使用して、TiCDC クラスターで次のメンテナンス操作を実行できます。

-   [TiCDCノードのステータス情報を取得する](#get-the-status-information-of-a-ticdc-node)
-   [TiCDC クラスターのヘルスステータスを確認する](#check-the-health-status-of-a-ticdc-cluster)
-   [レプリケーションタスクを作成する](#create-a-replication-task)
-   [レプリケーションタスクを削除する](#remove-a-replication-task)
-   [レプリケーション構成を更新する](#update-the-replication-configuration)
-   [レプリケーションタスクリストをクエリする](#query-the-replication-task-list)
-   [特定のレプリケーションタスクをクエリする](#query-a-specific-replication-task)
-   [レプリケーションタスクを一時停止する](#pause-a-replication-task)
-   [レプリケーションタスクを再開する](#resume-a-replication-task)
-   [レプリケーションサブタスクリストを照会する](#query-the-replication-subtask-list)
-   [特定のレプリケーションサブタスクをクエリする](#query-a-specific-replication-subtask)
-   [TiCDC サービス プロセス リストを照会する](#query-the-ticdc-service-process-list)
-   [所有者ノードの退去](#evict-an-owner-node)
-   [TiCDCサーバーのログレベルを動的に調整する](#dynamically-adjust-the-log-level-of-the-ticdc-server)

すべてのAPIのリクエストボディと戻り値はJSON形式です。リクエストが成功すると、 `200 OK`メッセージが返されます。以下のセクションでは、APIの具体的な使用方法について説明します。

以下の例では、TiCDCサーバーのリスニングIPアドレスは`127.0.0.1` 、ポートは`8300`です。TiCDCサーバーの起動時に、 `--addr=ip:port`でTiCDCにバインドされたIPアドレスとポートを指定できます。

## APIエラーメッセージテンプレート {#api-error-message-template}

API リクエストの送信後にエラーが発生した場合、返されるエラー メッセージは次の形式になります。

```json
{
    "error_msg": "",
    "error_code": ""
}
```

上記の JSON 出力では、 `error_msg`エラー メッセージを示し、 `error_code`対応するエラー コードを示します。

## APIリストインターフェースの戻り形式 {#return-format-of-the-api-list-interface}

API リクエストがリソースのリスト (たとえば、すべての`Captures`のリスト) を返す場合、TiCDC の戻り形式は次のようになります。

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

上記の例では、

-   `total` : リソースの合計数を示します。
-   `items` : このリクエストによって返されるすべてのリソースを含む配列。配列のすべての要素は同じリソースです。

## TiCDCノードのステータス情報を取得する {#get-the-status-information-of-a-ticdc-node}

このAPIは同期インターフェースです。リクエストが成功すると、対応するノードのステータス情報が返されます。

### リクエストURI {#request-uri}

`GET /api/v2/status`

### 例 {#example}

次のリクエストは、IP アドレスが`127.0.0.1`でポート番号が`8300`ある TiCDC ノードのステータス情報を取得します。

```shell
curl -X GET http://127.0.0.1:8300/api/v2/status
```

```json
{
  "version": "v8.5.3",
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
-   `pid` : ノードのキャプチャプロセス ID (PID)。
-   `is_owner` : ノードが所有者であるかどうかを示します。
-   `liveness` : このノードがライブかどうか。2 `0`正常を意味します。4 `1`ノードが`graceful shutdown`状態にあることを意味します。

## TiCDC クラスターのヘルスステータスを確認する {#check-the-health-status-of-a-ticdc-cluster}

このAPIは同期インターフェースです。クラスターが正常な場合は`200 OK`返されます。

### リクエストURI {#request-uri}

`GET /api/v2/health`

### 例 {#example}

```shell
curl -X GET http://127.0.0.1:8300/api/v2/health
```

クラスターが正常な場合、応答は`200 OK`と空の JSON オブジェクトになります。

```json
{}
```

クラスターが正常でない場合、応答はエラー メッセージを含む JSON オブジェクトになります。

## レプリケーションタスクを作成する {#create-a-replication-task}

このインターフェースは、TiCDCにレプリケーションタスクを送信するために使用されます。リクエストが成功した場合、 `200 OK`が返されます。返された結果は、サーバーがコマンドの実行に同意したことを意味するだけで、コマンドが正常に実行されることを保証するものではありません。

### リクエストURI {#request-uri}

`POST /api/v2/changefeeds`

### パラメータの説明 {#parameter-descriptions}

```json
{
  "changefeed_id": "string",
  "replica_config": {
    "bdr_mode": true,
    "case_sensitive": false,
    "check_gc_safe_point": true,
    "consistent": {
      "flush_interval": 0,
      "level": "string",
      "max_log_size": 0,
      "storage": "string"
    },
    "enable_sync_point": true,
    "filter": {
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

| パラメータ名           | 説明                                                                                                     |
| :--------------- | :----------------------------------------------------------------------------------------------------- |
| `changefeed_id`  | `STRING`型。レプリケーションタスクのID。（オプション）                                                                       |
| `replica_config` | レプリケーションタスクのコンフィグレーションパラメータ。(オプション)                                                                    |
| **`sink_uri`**   | `STRING`型。レプリケーションタスクのダウンストリームアドレス。（**必須**）                                                            |
| `start_ts`       | `UINT64`型。変更フィードの開始TSOを指定します。TiCDCクラスターは、このTSOからデータのプルを開始します。デフォルト値は現在時刻です。（オプション）                     |
| `target_ts`      | `UINT64`型。変更フィードのターゲットTSOを指定します。TiCDCクラスターは、このTSOに到達するとデータのプルを停止します。デフォルト値は空で、TiCDCは自動的に停止しません。(オプション) |

`changefeed_id` `target_ts`意味と`sink_uri`は、 [`cdc cli`を使用してレプリケーションタスクを作成する](/ticdc/ticdc-manage-changefeed.md#create-a-replication-task)ドキュメントに記載されているものと同じです。これら`start_ts`パラメータの詳細については、 `sink_uri`のドキュメントを参照してください。11 で証明書パスを指定する際は、対応する証明書が対応する TiCDCサーバーにアップロードされていることを確認してください。

`replica_config`パラメータの説明は次のとおりです。

| パラメータ名                    | 説明                                                                                                                                                                |
| :------------------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `bdr_mode`                | `BOOLEAN`型。2 [双方向レプリケーション](/ticdc/ticdc-bidirectional-replication.md)有効にするかどうかを決定します。デフォルト値は`false`です。（オプション）                                                     |
| `case_sensitive`          | `BOOLEAN`型。テーブル名をフィルタリングする際に大文字と小文字を区別するかどうかを指定します。v6.5.6、v7.1.3、v7.5.0以降では、デフォルト値が`true`から`false`に変更されます。（オプション）                                                 |
| `check_gc_safe_point`     | `BOOLEAN`型。レプリケーションタスクの開始時刻がGC時刻よりも前であるかどうかを確認するかどうかを指定します。デフォルト値は`true`です。（オプション）                                                                                |
| `consistent`              | REDOログの設定パラメータ。(オプション)                                                                                                                                            |
| `enable_sync_point`       | `BOOLEAN`型。2 `sync point`有効にするかどうかを決定します。（オプション）                                                                                                                  |
| `filter`                  | `filter`の設定パラメータ。(オプション)                                                                                                                                          |
| `force_replicate`         | `BOOLEAN`型。デフォルト値は`false`です`true`に設定すると、レプリケーションタスクは一意のインデックスを持たないテーブルを強制的にレプリケートします。（オプション）                                                                      |
| `ignore_ineligible_table` | `BOOLEAN`型。デフォルト値は`false`です`true`に設定すると、レプリケーションタスクはレプリケートできないテーブルを無視します。（オプション）                                                                                  |
| `memory_quota`            | `UINT64`型。レプリケーションタスクのメモリクォータ。（オプション）                                                                                                                             |
| `mounter`                 | `mounter`の設定パラメータ。(オプション)                                                                                                                                         |
| `sink`                    | `sink`の設定パラメータ。(オプション)                                                                                                                                            |
| `sync_point_interval`     | `STRING`型。返される値は`UINT64`型のナノ秒単位の時間であることに注意してください。4 `sync point`が有効な場合、このパラメータは同期ポイントが上流と下流のスナップショットを同期させる間隔を指定します。デフォルト値は`10m`で、最小値は`30s`です。（オプション）               |
| `sync_point_retention`    | `STRING`型。返される値は`UINT64`型のナノ秒単位の時間であることに注意してください。4 `sync point`が有効な場合、このパラメータは、下流テーブルにおける同期ポイントによるデータの保持期間を指定します。この期間を超えると、データはクリーンアップされます。デフォルト値は`24h`です。（オプション） |

`consistent`パラメータは次のように記述されます。

| パラメータ名                | 説明                                                                                      |
| :-------------------- | :-------------------------------------------------------------------------------------- |
| `flush_interval`      | `UINT64`型。REDOログファイルをフラッシュする間隔。（オプション）                                                  |
| `level`               | `STRING`型。複製されたデータの一貫性レベル。（オプション）                                                       |
| `max_log_size`        | `UINT64`型。REDOログの最大値。（オプション）                                                            |
| `storage`             | `STRING`型。storageの宛先アドレス。（オプション）                                                        |
| `use_file_backend`    | `BOOL`タイプ。REDOログをローカルファイルに保存するかどうかを指定します。（オプション）                                        |
| `encoding_worker_num` | `INT`型。REDOモジュール内のエンコードおよびデコードワーカーの数。（オプション）                                            |
| `flush_worker_num`    | `INT`型。REDOモジュール内のフラッシュワーカーの数。（オプション）                                                   |
| `compression`         | `STRING`タイプ。REDOログファイルを圧縮する動作。使用可能なオプションは`""`と`"lz4"`です。デフォルト値は`""`で、圧縮なしを意味します。（オプション） |
| `flush_concurrency`   | `INT`型。単一ファイルのアップロードにおける同時実行数。デフォルト値は`1`で、同時実行が無効であることを意味します。（オプション）                    |

`filter`パラメータは次のように記述されます。

| パラメータ名                | 説明                                                                                                                     |
| :-------------------- | :--------------------------------------------------------------------------------------------------------------------- |
| `event_filters`       | イベントをフィルタリングするための設定。(オプション)                                                                                            |
| `ignore_txn_start_ts` | `UINT64 ARRAY`型。これを指定すると、 `[1, 2]`など`start_ts`指定するトランザクションは無視されます。（オプション）                                              |
| `rules`               | `STRING ARRAY`型。テーブルスキーマフィルタリングのルール（例： `['foo*.*', 'bar*.*']` ）。詳細については、 [テーブルフィルター](/table-filter.md)参照してください。（オプション） |

`filter.event_filters`パラメータの説明は以下のとおりです。詳細については[変更フィードログフィルター](/ticdc/ticdc-filter.md)参照してください。

| パラメータ名                         | 説明                                                                                                                 |
| :----------------------------- | :----------------------------------------------------------------------------------------------------------------- |
| `ignore_delete_value_expr`     | `STRING ARRAY`型。例えば、 `"name = 'john'"` `name = 'john'`条件を含む DELETE DML 文を除外することを意味します。(オプション)                      |
| `ignore_event`                 | `STRING ARRAY`型。例えば、 `["insert"]` INSERTイベントが除外されることを示します。（オプション）                                                  |
| `ignore_insert_value_expr`     | `STRING ARRAY`型。例えば、 `"id >= 100"` `id >= 100`条件に一致する INSERT DML 文を除外することを意味します。(オプション)                            |
| `ignore_sql`                   | `STRING ARRAY`型。例えば、 `["^drop", "add column"]` `DROP`で始まるか`ADD COLUMN`含むDDL文を除外することを意味します。（オプション）                  |
| `ignore_update_new_value_expr` | `STRING ARRAY`型。例えば、 `"gender = 'male'"` 、新しい値`gender = 'male'`を持つ UPDATE DML 文を除外することを意味します。（オプション）               |
| `ignore_update_old_value_expr` | `STRING ARRAY`型。例えば、 `"age < 18"`古い値`age < 18`を持つ UPDATE DML 文を除外することを意味します。（オプション）                                |
| `matcher`                      | `STRING ARRAY`型。ホワイトリストとして機能します。例えば、 `["test.worker"]` 、フィルタールールが`test`データベースの`worker`テーブルにのみ適用されることを意味します。(オプション) |

`mounter`パラメータは次のように記述されます。

| パラメータ名       | 説明                                                                          |
| :----------- | :-------------------------------------------------------------------------- |
| `worker_num` | `INT`型。マウントスレッドの数。マウントはTiKVから出力されたデータをデコードするために使用されます。デフォルト値は`16`です。（オプション） |

`sink`パラメータは次のように記述されます。

| パラメータ名                        | 説明                                                                                                                           |
| :---------------------------- | :--------------------------------------------------------------------------------------------------------------------------- |
| `column_selectors`            | 列セレクターの構成。(オプション)                                                                                                            |
| `csv`                         | CSV 構成。(オプション)                                                                                                               |
| `date_separator`              | `STRING`型。ファイルディレクトリの日付区切り文字の種類を示します。値の選択肢は`none` 、 `year` 、 `month` 、 `day`です。10 `none`デフォルト値で、日付が区切られないことを意味します。(オプション)    |
| `dispatchers`                 | イベントディスパッチ用の構成配列。(オプション)                                                                                                     |
| `encoder_concurrency`         | `INT`型。MQシンク内のエンコーダスレッドの数。デフォルト値は`16`です。（オプション）                                                                              |
| `protocol`                    | `STRING`型。MQシンクの場合、メッセージのプロトコル形式を指定できます。現在サポートされているプロトコルは、 `canal-json` 、 `open-protocol` 、 `avro` 、 `debezium` 、 `simple` 。 |
| `schema_registry`             | `STRING`型。スキーマレジストリアドレス。（オプション）                                                                                              |
| `terminator`                  | `STRING`型。ターミネータは、2つのデータ変更イベントを区切るために使用されます。デフォルト値はnullで、 `"\r\n"`ターミネータとして使用されます。（オプション）                                    |
| `transaction_atomicity`       | `STRING`型。トランザクションのアトミック性レベル。（オプション）                                                                                         |
| `only_output_updated_columns` | `BOOLEAN`型。2 または`canal-json`プロトコル`open-protocol`使用するMQシンクの場合、変更された列のみを出力するかどうかを指定できます。デフォルト値は`false`です。（オプション）               |
| `cloud_storage_config`        | storageシンクの構成。(オプション)                                                                                                        |
| `open`                        | オープンプロトコルの構成。(オプション)                                                                                                         |
| `debezium`                    | Debezium プロトコルの設定。(オプション)                                                                                                    |

`sink.column_selectors`は配列です。パラメータは以下のとおりです。

| パラメータ名    | 説明                                              |
| :-------- | :---------------------------------------------- |
| `columns` | `STRING ARRAY`型。列配列。                            |
| `matcher` | `STRING ARRAY`型。マッチャー設定。フィルタルールと同じマッチング構文を持ちます。 |

`sink.csv`パラメータは次のように記述されます。

| パラメータ名                   | 説明                                                                           |
| :----------------------- | :--------------------------------------------------------------------------- |
| `delimiter`              | `STRING`型。CSVファイル内のフィールドを区切るために使用される文字。値はASCII文字でなければならず、デフォルトは`,`です。        |
| `include_commit_ts`      | `BOOLEAN`型。CSV行にコミット情報を含めるかどうか。デフォルト値は`false`です。                             |
| `null`                   | `STRING`型。CSV列がnullの場合に表示される文字。デフォルト値は`\N`です。                                |
| `quote`                  | `STRING`型。CSVファイル内のフィールドを囲むために使用される引用符文字。値が空の場合、引用符は使用されません。デフォルト値は`"`です。    |
| `binary_encoding_method` | `STRING`型。バイナリデータのエンコード方式。2 または`"base64"` `"hex"`指定できます。デフォルト値は`"base64"`です。 |

`sink.dispatchers` : MQタイプのシンクの場合、このパラメータを使用してイベントディスパッチャを設定できます。サポートされているディスパッチャは`default` 、 `ts` 、 `index-value` 、 `table`です。ディスパッチャのルールは以下のとおりです。

-   `default` : `table`モードでイベントを送信します。
-   `ts` : 行変更の commitTs を使用してハッシュ値を作成し、イベントをディスパッチします。
-   `index-value` : 選択した HandleKey 列の名前と値を使用してハッシュ値を作成し、イベントをディスパッチします。
-   `table` : テーブルのスキーマ名とテーブル名を使用してハッシュ値を作成し、イベントをディスパッチします。

`sink.dispatchers`は配列です。パラメータは以下のとおりです。

| パラメータ名      | 説明                                      |
| :---------- | :-------------------------------------- |
| `matcher`   | `STRING ARRAY`型。フィルタールールと同じ一致構文を持ちます。   |
| `partition` | `STRING`タイプ。イベントをディスパッチするターゲット パーティション。 |
| `topic`     | `STRING`型。イベントをディスパッチするターゲットトピック。       |

`sink.cloud_storage_config`パラメータは次のように記述されます。

| パラメータ名                    | 説明                                                                                                                                              |
| :------------------------ | :---------------------------------------------------------------------------------------------------------------------------------------------- |
| `worker_count`            | `INT`型。下流のクラウドストレージへのデータstorageの同時実行性が変更されます。                                                                                                   |
| `flush_interval`          | `STRING`型。下流のクラウドstorageへのデータ保存間隔が変更されます。                                                                                                       |
| `file_size`               | `INT`型。このファイル内のバイト数がこのパラメータの値を超えると、データ変更ファイルがクラウドstorageに保存されます。                                                                                |
| `file_expiration_days`    | `INT`タイプ。ファイルを保持する期間。2 `date-separator` `day`に設定されている場合にのみ有効になります。                                                                              |
| `file_cleanup_cron_spec`  | `STRING`型。crontab 設定と互換性のある、スケジュールされたクリーンアップタスクの実行サイクル。形式は`<Second> <Minute> <Hour> <Day of the month> <Month> <Day of the week (Optional)>`です。 |
| `flush_concurrency`       | `INT`型。単一ファイルのアップロードの同時実行性。                                                                                                                     |
| `output_raw_change_event` | `BOOLEAN`タイプ。MySQL 以外のシンクの元のデータ変更イベントを出力するかどうかを制御します。                                                                                           |

`sink.open`パラメータは次のように記述されます。

| パラメータ名             | 説明                                                                                                      |
| :----------------- | :------------------------------------------------------------------------------------------------------ |
| `output_old_value` | `BOOLEAN`型。行データが変更される前に値を出力するかどうかを制御します。デフォルト値は`true`です。無効にすると、UPDATE イベントは &quot;p&quot; フィールドを出力しません。 |

`sink.debezium`パラメータは次のように記述されます。

| パラメータ名             | 説明                                                                                            |
| :----------------- | :-------------------------------------------------------------------------------------------- |
| `output_old_value` | `BOOLEAN`型。行データが変更される前の値を出力するかどうかを制御します。デフォルト値はtrueです。無効にすると、UPDATEイベントは「before」フィールドを出力しません。 |

### 例 {#example}

次のリクエストは、ID が`test5`で`blackhome://` `sink_uri`あるレプリケーション タスクを作成します。

```shell
curl -X POST -H "Content-type: application/json" http://127.0.0.1:8300/api/v2/changefeeds -d '{"changefeed_id":"test5","sink_uri":"blackhole://"}'
```

リクエストが成功した場合は`200 OK`返されます。リクエストが失敗した場合は、エラーメッセージとエラーコードが返されます。

### レスポンス本文の形式 {#response-body-format}

```json
{
  "admin_job_type": 0,
  "checkpoint_time": "string",
  "checkpoint_ts": 0,
  "config": {
    "bdr_mode": true,
    "case_sensitive": false,
    "check_gc_safe_point": true,
    "consistent": {
      "flush_interval": 0,
      "level": "string",
      "max_log_size": 0,
      "storage": "string"
    },
    "enable_sync_point": true,
    "filter": {
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

| パラメータ名            | 説明                                                                                  |
| :---------------- | :---------------------------------------------------------------------------------- |
| `admin_job_type`  | `INTEGER`タイプ。管理ジョブのタイプ。                                                             |
| `checkpoint_time` | `STRING`タイプ。レプリケーションタスクの現在のチェックポイントのフォーマットされた時刻。                                    |
| `checkpoint_ts`   | `STRING`タイプ。レプリケーション タスクの現在のチェックポイントの TSO。                                          |
| `config`          | レプリケーションタスクの設定。構造と意味は、レプリケーションタスク作成時の`replica_config`の設定と同じです。                      |
| `create_time`     | `STRING`型。レプリケーションタスクが作成された時刻。                                                      |
| `creator_version` | `STRING`タイプ。レプリケーションタスク作成時の TiCDC バージョン。                                            |
| `error`           | レプリケーション タスク エラー。                                                                   |
| `id`              | `STRING`タイプ。レプリケーション タスク ID。                                                        |
| `resolved_ts`     | `UINT64`タイプ。レプリケーション タスクは ts を解決しました。                                               |
| `sink_uri`        | `STRING`タイプ。レプリケーション タスク シンクの URI。                                                  |
| `start_ts`        | `UINT64`タイプ。レプリケーションタスクが開始されます。                                                     |
| `state`           | `STRING`型。レプリケーションタスクの`failed` 。2、4、6、8、10 `stopped` `normal`か`finished`なります`error` |
| `target_ts`       | `UINT64`タイプ。レプリケーションタスクのターゲット ts。                                                   |
| `task_status`     | レプリケーション タスクのディスパッチの詳細なステータス。                                                       |

`task_status`パラメータは次のように記述されます。

| パラメータ名       | 説明                                           |
| :----------- | :------------------------------------------- |
| `capture_id` | `STRING`型。キャプチャID。                           |
| `table_ids`  | `UINT64 ARRAY`タイプ。このキャプチャでレプリケートされるテーブルの ID。 |

`error`パラメータは次のように記述されます。

| パラメータ名    | 説明                   |
| :-------- | :------------------- |
| `addr`    | `STRING`型。キャプチャアドレス。 |
| `code`    | `STRING`型。エラーコード。    |
| `message` | `STRING`型。エラーの詳細。    |

## レプリケーションタスクを削除する {#remove-a-replication-task}

このAPIは、レプリケーションタスクを削除するためのべき等インターフェース（つまり、最初の適用後、結果を変更することなく複数回適用できるインターフェース）です。リクエストが成功した場合、 `200 OK`が返されます。返された結果は、サーバーがコマンドの実行に同意したことを意味するだけで、コマンドが正常に実行されることを保証するものではありません。

### リクエストURI {#request-uri}

`DELETE /api/v2/changefeeds/{changefeed_id}`

### パラメータの説明 {#parameter-descriptions}

#### パスパラメータ {#path-parameters}

| パラメータ名          | 説明                                  |
| :-------------- | :---------------------------------- |
| `changefeed_id` | 削除するレプリケーション タスク (changefeed) の ID。 |

### 例 {#example}

次のリクエストは、ID `test1`のレプリケーション タスクを削除します。

```shell
curl -X DELETE http://127.0.0.1:8300/api/v2/changefeeds/test1
```

リクエストが成功した場合は`200 OK`返されます。リクエストが失敗した場合は、エラーメッセージとエラーコードが返されます。

## レプリケーション構成を更新する {#update-the-replication-configuration}

このAPIはレプリケーションタスクの更新に使用されます。リクエストが成功した場合、 `200 OK`返されます。返された結果は、サーバーがコマンドの実行に同意したことを意味するだけで、コマンドが正常に実行されることを保証するものではありません。

changefeed 設定を変更するには、 `pause the replication task -> modify the configuration -> resume the replication task`の手順に従います。

### リクエストURI {#request-uri}

`PUT /api/v2/changefeeds/{changefeed_id}`

### パラメータの説明 {#parameter-descriptions}

#### パスパラメータ {#path-parameters}

| パラメータ名          | 説明                                  |
| :-------------- | :---------------------------------- |
| `changefeed_id` | 更新するレプリケーション タスク (changefeed) の ID。 |

#### リクエスト本体のパラメータ {#parameters-for-the-request-body}

```json
{
  "replica_config": {
    "bdr_mode": true,
    "case_sensitive": false,
    "check_gc_safe_point": true,
    "consistent": {
      "flush_interval": 0,
      "level": "string",
      "max_log_size": 0,
      "storage": "string"
    },
    "enable_sync_point": true,
    "filter": {
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

| パラメータ名           | 説明                                          |
| :--------------- | :------------------------------------------ |
| `target_ts`      | `UINT64`タイプ。チェンジフィードのターゲットTSOを指定します。（オプション） |
| `sink_uri`       | `STRING`型。レプリケーションタスクのダウンストリームアドレス。（オプション）  |
| `replica_config` | シンクの設定パラメータ。すべて指定する必要があります。（オプション）          |

上記のパラメータの意味はセクション[レプリケーションタスクを作成する](#create-a-replication-task)と同じです。詳細については、セクション1を参照してください。

### 例 {#example}

次のリクエストは、ID `test1`のレプリケーション タスクの`target_ts` `32`に更新します。

```shell
curl -X PUT -H "Content-type: application/json" http://127.0.0.1:8300/api/v2/changefeeds/test1 -d '{"target_ts":32}'
```

リクエストが成功した場合は`200 OK`返されます。リクエストが失敗した場合は、エラーメッセージとエラーコードが返されます。JSONレスポンスボディの意味は[レプリケーションタスクを作成する](#create-a-replication-task)セクションと同じです。詳細は3のセクションを参照してください。

## レプリケーションタスクリストをクエリする {#query-the-replication-task-list}

このAPIは同期インターフェースです。リクエストが成功すると、TiCDCクラスター内のすべてのレプリケーションタスク（変更フィード）の基本情報が返されます。

### リクエストURI {#request-uri}

`GET /api/v2/changefeeds`

### パラメータの説明 {#parameter-descriptions}

#### クエリパラメータ {#query-parameter}

| パラメータ名  | 説明                                                   |
| :------ | :--------------------------------------------------- |
| `state` | このパラメータを指定すると、指定された状態にあるレプリケーションタスクの情報が返されます。（オプション） |

`state`の値のオプションは`all` 、 `normal` 、 `stopped` 、 `error` 、 `failed` 、 `finished`です。

このパラメータを指定しない場合は、 `normal` 、 `stopped` 、または`failed`状態のレプリケーション タスクの基本情報がデフォルトで返されます。

### 例 {#example}

次のリクエストは、状態`normal`にあるすべてのレプリケーション タスクの基本情報を照会します。

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

上記の返された結果のパラメータは次のように説明されます。

-   `id` : レプリケーション タスクの ID。
-   `state` : レプリケーション タスクの現在の[州](/ticdc/ticdc-changefeed-overview.md#changefeed-state-transfer) 。
-   `checkpoint_tso` : レプリケーション タスクの現在のチェックポイントの TSO。
-   `checkpoint_time` : レプリケーション タスクの現在のチェックポイントのフォーマットされた時刻。
-   `error` : レプリケーション タスクのエラー情報。

## 特定のレプリケーションタスクをクエリする {#query-a-specific-replication-task}

このAPIは同期インターフェースです。リクエストが成功すると、指定されたレプリケーションタスク（changefeed）の詳細情報が返されます。

### リクエストURI {#request-uri}

`GET /api/v2/changefeeds/{changefeed_id}`

### パラメータの説明 {#parameter-description}

#### パスパラメータ {#path-parameter}

| パラメータ名          | 説明                                   |
| :-------------- | :----------------------------------- |
| `changefeed_id` | クエリするレプリケーション タスク (changefeed) の ID。 |

### 例 {#example}

次のリクエストは、ID `test1`のレプリケーション タスクの詳細情報を照会します。

```shell
curl -X GET http://127.0.0.1:8300/api/v2/changefeeds/test1
```

JSONレスポンスボディの意味はセクション[レプリケーションタスクを作成する](#create-a-replication-task)と同じです。詳細はセクション1を参照してください。

## 特定のレプリケーションタスクが完了したかどうかを照会する {#query-whether-a-specific-replication-task-is-completed}

このAPIは同期インターフェースです。リクエストが成功すると、指定されたレプリケーションタスク（changefeed）の同期ステータス（タスクの完了の有無など）が返されます。

### リクエストURI {#request-uri}

`GET /api/v2/changefeeds/{changefeed_id}/synced`

### パラメータの説明 {#parameter-description}

#### パスパラメータ {#path-parameter}

| パラメータ名          | 説明                                   |
| :-------------- | :----------------------------------- |
| `changefeed_id` | クエリするレプリケーション タスク (changefeed) の ID。 |

### 例 {#examples}

次のリクエストは、ID `test1`のレプリケーション タスクの同期ステータスを照会します。

```shell
curl -X GET http://127.0.0.1:8300/api/v2/changefeeds/test1/synced
```

**例1: 同期が完了しました**

```json
{
  "synced": true,
  "sink_checkpoint_ts": "2023-11-30 15:14:11.015",
  "puller_resolved_ts": "2023-11-30 15:14:12.215",
  "last_synced_ts": "2023-11-30 15:08:35.510",
  "now_ts": "2023-11-30 15:14:11.511",
  "info": "Data syncing is finished"
}
```

応答には次のフィールドが含まれます。

-   `synced` : このレプリケーションタスクが完了したかどうか。2 `true`タスクが完了したこと、 `false`タスクが完了していない可能性があることを意味します。6 `false`場合は、 `info`フィールドとその他のフィールドの両方で具体的なステータスを確認する必要があります。
-   `sink_checkpoint_ts` : シンク モジュールのチェックポイント ts 値 (PD 時間)。
-   `puller_resolved_ts` : PD 時間での、プラー モジュールのresolved-ts値。
-   `last_synced_ts` : TiCDC によって処理された最新のデータの commit-ts 値 (PD 時間)。
-   `now_ts` : 現在の PD 時間。
-   `info` : 特に`synced`が`false`場合、同期ステータスの判別を支援する補足情報。

**例2: 同期が完了していない**

```json
{
  "synced": false,
  "sink_checkpoint_ts": "2023-11-30 15:26:31.519",
  "puller_resolved_ts": "2023-11-30 15:26:23.525",
  "last_synced_ts": "2023-11-30 15:24:30.115",
  "now_ts": "2023-11-30 15:26:31.511",
  "info": "The data syncing is not finished, please wait"
}
```

この例は、進行中のレプリケーションタスクの応答を示しています。フィールド`synced`と`info`両方を確認することで、レプリケーションタスクがまだ完了しておらず、さらに待機する必要があることがわかります。

**例3: 同期ステータスをさらに確認する必要がある**

```json
{
  "synced":false,
  "sink_checkpoint_ts":"2023-12-13 11:45:13.515",
  "puller_resolved_ts":"2023-12-13 11:45:13.525",
  "last_synced_ts":"2023-12-13 11:45:07.575",
  "now_ts":"2023-12-13 11:50:24.875",
  "info":"Please check whether PD is online and TiKV Regions are all available. If PD is offline or some TiKV regions are not available, it means that the data syncing process is complete. To check whether TiKV regions are all available, you can view 'TiKV-Details' > 'Resolved-Ts' > 'Max Leader Resolved TS gap' on Grafana. If the gap is large, such as a few minutes, it means that some regions in TiKV are unavailable. Otherwise, if the gap is small and PD is online, it means the data syncing is incomplete, so please wait"
}
```

このAPIを使用すると、上流クラスタで災害が発生した場合でも同期ステータスを照会できます。状況によっては、TiCDCの現在のデータレプリケーションタスクが完了しているかどうかを直接確認できない場合があります。そのような場合は、このAPIをリクエストし、レスポンスの`info`フィールドと上流クラスタの現在のステータスの両方を確認することで、具体的なステータスを確認できます。

この例では、 `sink_checkpoint_ts` `now_ts`より遅れていますが、これは TiCDC がまだデータレプリケーションに追いついていないか、PD または TiKV に障害が発生しているためです。TiCDC がまだデータレプリケーションに追いついていない場合は、レプリケーションタスクがまだ完了していないことを意味します。PD または TiKV に障害が発生した場合は、レプリケーションタスクが完了していることを意味します。したがって、クラスターのステータスを確認するには、 `info`フィールドを確認する必要があります。

**例4: クエリエラー**

```json
{
  "error_msg": "[CDC:ErrPDEtcdAPIError]etcd api call error: context deadline exceeded",
  "error_code": "CDC:ErrPDEtcdAPIError"
}
```

上流クラスターのPDに長時間障害が発生した場合、このAPIクエリを実行すると、前述のエラーと同様のエラーが返されることがあります。このエラーでは、それ以上確認するための情報は提供されません。PDの障害はTiCDCのデータレプリケーションに直接影響するため、このようなエラーが発生した場合、TiCDCは可能な限りデータレプリケーションを完了していると考えられますが、下流クラスターではPDの障害によりデータ損失が発生する可能性が依然としてあります。

## レプリケーションタスクを一時停止する {#pause-a-replication-task}

このAPIはレプリケーションタスクを一時停止します。リクエストが成功した場合、 `200 OK`が返されます。返された結果は、サーバーがコマンドの実行に同意したことを意味するだけで、コマンドが正常に実行されることを保証するものではありません。

### リクエストURI {#request-uri}

`POST /api/v2/changefeeds/{changefeed_id}/pause`

### パラメータの説明 {#parameter-description}

#### パスパラメータ {#path-parameter}

| パラメータ名          | 説明                                    |
| :-------------- | :------------------------------------ |
| `changefeed_id` | 一時停止するレプリケーション タスク (changefeed) の ID。 |

### 例 {#example}

次のリクエストは、ID `test1`のレプリケーション タスクを一時停止します。

```shell
curl -X POST http://127.0.0.1:8300/api/v2/changefeeds/test1/pause
```

リクエストが成功した場合は`200 OK`返されます。リクエストが失敗した場合は、エラーメッセージとエラーコードが返されます。

## レプリケーションタスクを再開する {#resume-a-replication-task}

このAPIはレプリケーションタスクを再開します。リクエストが成功した場合、 `200 OK`が返されます。返された結果は、サーバーがコマンドの実行に同意したことを意味するだけで、コマンドが正常に実行されることを保証するものではありません。

### リクエストURI {#request-uri}

`POST /api/v2/changefeeds/{changefeed_id}/resume`

### パラメータの説明 {#parameter-description}

#### パスパラメータ {#path-parameter}

| パラメータ名          | 説明                                  |
| :-------------- | :---------------------------------- |
| `changefeed_id` | 再開するレプリケーション タスク (changefeed) の ID。 |

#### リクエスト本体のパラメータ {#parameters-for-the-request-body}

```json
{
  "overwrite_checkpoint_ts": 0
}
```

| パラメータ名                    | 説明                                                                    |
| :------------------------ | :-------------------------------------------------------------------- |
| `overwrite_checkpoint_ts` | `UINT64`タイプ。レプリケーション タスク (changefeed) を再開するときにチェックポイント TSO を再割り当てします。 |

### 例 {#example}

次のリクエストは、ID `test1`のレプリケーション タスクを再開します。

```shell
curl -X POST http://127.0.0.1:8300/api/v2/changefeeds/test1/resume -d '{}'
```

リクエストが成功した場合は`200 OK`返されます。リクエストが失敗した場合は、エラーメッセージとエラーコードが返されます。

## レプリケーションサブタスクリストを照会する {#query-the-replication-subtask-list}

このAPIは同期インターフェースです。リクエストが成功すると、すべてのレプリケーションサブタスク( `processor` )の基本情報が返されます。

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

## 特定のレプリケーションサブタスクをクエリする {#query-a-specific-replication-subtask}

このAPIは同期インターフェースです。リクエストが成功すると、指定されたレプリケーションサブタスク( `processor` )の詳細情報を返します。

### リクエストURI {#request-uri}

`GET /api/v2/processors/{changefeed_id}/{capture_id}`

### パラメータの説明 {#parameter-descriptions}

#### パスパラメータ {#path-parameters}

| パラメータ名          | 説明                             |
| :-------------- | :----------------------------- |
| `changefeed_id` | クエリするレプリケーション サブタスクの変更フィード ID。 |
| `capture_id`    | クエリするレプリケーション サブタスクのキャプチャ ID。  |

### 例 {#example}

次のリクエストは、 `changefeed_id`が`test` 、 `capture_id`が`561c3784-77f0-4863-ad52-65a3436db6af`あるサブタスクの詳細情報を取得します。サブタスクは`changefeed_id`と`capture_id`で識別できます。

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

パラメータの説明は次のとおりです。

-   `table_ids` : このキャプチャで複製されるテーブル ID。

## TiCDC サービス プロセス リストを照会する {#query-the-ticdc-service-process-list}

このAPIは同期インターフェースです。リクエストが成功すると、すべてのレプリケーションプロセスの基本情報( `capture` )が返されます。

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
-   `is_owner` : キャプチャが所有者であるかどうか。
-   `address` : キャプチャのアドレス。

## 所有者ノードの退去 {#evict-an-owner-node}

このAPIは非同期インターフェースです。リクエストが成功した場合、 `200 OK`が返されます。返された結果は、サーバーがコマンドの実行に同意したことを意味するだけで、コマンドが正常に実行されることを保証するものではありません。

### リクエストURI {#request-uri}

`POST /api/v2/owner/resign`

### 例 {#example}

次のリクエストは、TiCDC の現在の所有者ノードを削除し、新しい所有者ノードを生成するための新しいラウンドの選挙をトリガーします。

```shell
curl -X POST http://127.0.0.1:8300/api/v2/owner/resign
```

リクエストが成功した場合は`200 OK`返されます。リクエストが失敗した場合は、エラーメッセージとエラーコードが返されます。

## TiCDCサーバーのログレベルを動的に調整する {#dynamically-adjust-the-log-level-of-the-ticdc-server}

このAPIは同期インターフェースです。リクエストが成功すると`200 OK`返されます。

### リクエストURI {#request-uri}

`POST /api/v2/log`

### リクエストパラメータ {#request-parameter}

#### リクエスト本体のパラメータ {#parameter-for-the-request-body}

| パラメータ名      | 説明          |
| :---------- | :---------- |
| `log_level` | 設定するログ レベル。 |

`log_level` 、「debug」、「info」、「warn」、「error」、「dpanic」、「panic」、「fatal」の[zapが提供するログレベル](https://godoc.org/go.uber.org/zap#UnmarshalText)サポートします。

### 例 {#example}

```shell
curl -X POST -H "Content-type: application/json" http://127.0.0.1:8300/api/v2/log -d '{"log_level":"debug"}'
```

リクエストが成功した場合は`200 OK`返されます。リクエストが失敗した場合は、エラーメッセージとエラーコードが返されます。
