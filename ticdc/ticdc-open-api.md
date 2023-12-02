---
title: TiCDC OpenAPI v1
summary: Learn how to use the OpenAPI interface to manage the cluster status and data replication.
---

# TiCDC OpenAPI v1 {#ticdc-openapi-v1}

<!-- markdownlint-disable MD024 -->

> **注記**
>
> TiCDC OpenAPI v1 は非推奨となり、将来削除される予定です。 [TiCDC OpenAPI v2](/ticdc/ticdc-open-api-v2.md)を使用することをお勧めします。

TiCDC は、TiCDC クラスターのクエリと操作のための OpenAPI 機能を提供します。これは、 [`cdc cli`ツール](/ticdc/ticdc-manage-changefeed.md)の機能に似ています。

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
-   [レプリケーション タスク内のすべてのテーブルの負荷分散を手動でトリガーする](#manually-trigger-the-load-balancing-of-all-tables-in-a-replication-task)
-   [テーブルを別のノードに手動でスケジュールする](#manually-schedule-a-table-to-another-node)
-   [TiCDCサーバーのログ レベルを動的に調整する](#dynamically-adjust-the-log-level-of-the-ticdc-server)

すべての API のリクエスト本文と戻り値は JSON 形式です。次のセクションでは、API の具体的な使用法について説明します。

次の例では、TiCDCサーバーのリスニング IP アドレスは`127.0.0.1` 、ポートは`8300`です。 TiCDCサーバーの起動時に、指定した IP とポートを`--addr=ip:port`経由でバインドできます。

## APIエラーメッセージテンプレート {#api-error-message-template}

API リクエストの送信後にエラーが発生した場合、返されるエラー メッセージは次の形式になります。

```json
{
    "error_msg": "",
    "error_code": ""
}
```

上記の JSON 出力から、 `error_msg`エラー メッセージを説明し、 `error_code`は対応するエラー コードです。

## TiCDC ノードのステータス情報を取得する {#get-the-status-information-of-a-ticdc-node}

この API は同期インターフェイスです。リクエストが成功すると、該当ノードのステータス情報が返されます。

### リクエストURI {#request-uri}

`GET /api/v1/status`

### 例 {#example}

次のリクエストは、IP アドレスが`127.0.0.1`でポート番号が`8300` TiCDC ノードのステータス情報を取得します。

```shell
curl -X GET http://127.0.0.1:8300/api/v1/status
```

```json
{
    "version": "v5.2.0-master-dirty",
    "git_hash": "f191cd00c53fdf7a2b1c9308a355092f9bf8824e",
    "id": "c6a43c16-0717-45af-afd6-8b3e01e44f5d",
    "pid": 25432,
    "is_owner": true
}
```

上記の出力のフィールドは次のように説明されます。

-   version: 現在の TiCDC バージョン番号。
-   git_hash: Git ハッシュ値。
-   id: ノードのキャプチャ ID。
-   pid: ノードのキャプチャ プロセス PID。
-   is_owner: ノードが所有者であるかどうかを示します。

## TiCDC クラスターの健全性ステータスを確認する {#check-the-health-status-of-a-ticdc-cluster}

この API は同期インターフェイスです。クラスターが正常な場合は`200 OK`が返されます。

### リクエストURI {#request-uri}

`GET /api/v1/health`

### 例 {#example}

```shell
curl -X GET http://127.0.0.1:8300/api/v1/health
```

## レプリケーションタスクを作成する {#create-a-replication-task}

この API は非同期インターフェイスです。リクエストが成功すると`202 Accepted`が返されます。返された結果は、サーバーがコマンドの実行に同意したことを意味するだけで、コマンドが正常に実行されることを保証するものではありません。

### リクエストURI {#request-uri}

`POST /api/v1/changefeeds`

### パラメータの説明 {#parameter-description}

`cli`コマンドを使用してレプリケーション タスクを作成するためのオプション パラメータと比較すると、API を使用してそのようなタスクを作成するためのオプション パラメータは完全ではありません。この API は次のパラメータをサポートしています。

#### リクエストボディのパラメータ {#parameters-for-the-request-body}

|パラメータ名 |説明 | | :---------------------- | :---------------------- ------------------------- ---- | | `changefeed_id` | `STRING`タイプ。レプリケーションタスクのID。 (オプション) | | `start_ts` | `UINT64`型。変更フィードの開始 TSO を指定します。 (オプション) | | `target_ts` | `UINT64`型。変更フィードのターゲット TSO を指定します。 (オプション) | | **`sink_uri`** | `STRING`型。レプリケーションタスクの下流アドレス。 (**必須**) | | `force_replicate` | `BOOLEAN`型。一意のインデックスのないテーブルを強制的にレプリケートするかどうかを決定します。 (オプション) | | `ignore_ineligible_table` | `BOOLEAN`タイプ。複製できないテーブルを無視するかどうかを決定します。 (オプション) | | `filter_rules` | `STRING`型配列。テーブルスキーマフィルタリングのルール。 (オプション) | | `ignore_txn_start_ts` | `UINT64`型配列。指定された start_ts のトランザクションを無視します。 (オプション) | | `mounter_worker_num` | `INT`型。マウンターのスレッド番号。 (オプション) | | `sink_config` |シンクの構成パラメータ。 (オプション) |

`changefeed_id` 、 `start_ts` 、 `target_ts` 、 `sink_uri`の意味と形式は、ドキュメント[`cdc cli`を使用してレプリケーション タスクを作成する](/ticdc/ticdc-manage-changefeed.md#create-a-replication-task)に記載されているものと同じです。これらのパラメータの詳細については、このドキュメントを参照してください。 `sink_uri`で証明書のパスを指定する場合は、対応する証明書が対応する TiCDCサーバーにアップロードされていることを確認してください。

上の表の他のパラメータについては、以下でさらに説明します。

`force_replicate` : このパラメータのデフォルトは`false`です。 `true`として指定すると、TiCDC は一意のインデックスを持たないテーブルを強制的に複製しようとします。

`ignore_ineligible_table` : このパラメータのデフォルトは`false`です。 `true`として指定すると、TiCDC は複製できないテーブルを無視します。

`filter_rules` : テーブル スキーマ フィルタリングのルール ( `filter_rules = ['foo*.*','bar*.*']`など)。詳細は資料[テーブルフィルター](/table-filter.md)をご参照ください。

`ignore_txn_start_ts` : このパラメータを指定した場合、指定された start_ts は無視されます。たとえば、 `ignore-txn-start-ts = [1, 2]` 。

`mounter_worker_num` : マウンタのスレッド番号。マウンタは、TiKV から出力されたデータをデコードするために使用されます。デフォルト値は`16`です。

シンクの構成パラメータは次のとおりです。

```json
{
  "dispatchers":[
    {"matcher":["test1.*", "test2.*"], "dispatcher":"ts"},
    {"matcher":["test3.*", "test4.*"], "dispatcher":"rowid"}
  ],
  "protocal":"canal-json"
}
```

`dispatchers` : MQ タイプのシンクの場合、ディスパッチャーを使用してイベント ディスパッチャーを構成できます。 4 つのディスパッチャー ( `default` 、 `ts` 、 `rowid` 、および`table`がサポートされています。ディスパッチャのルールは次のとおりです。

-   `default` : `table`モードでイベントをディスパッチします。
-   `ts` : 行変更の commitT を使用してハッシュ値を作成し、イベントをディスパッチします。
-   `rowid` : 選択した HandleKey 列の名前と値を使用して、ハッシュ値を作成し、イベントをディスパッチします。
-   `table` : テーブルのスキーマ名とテーブル名を使用してハッシュ値を作成し、イベントをディスパッチします。

`matcher` : matcher のマッチング構文はフィルター ルールの構文と同じです。

`protocol` : MQ タイプのシンクの場合、メッセージのプロトコル形式を指定できます。現在、次のプロトコルがサポートされています: `canal-json` 、 `open-protocol` 、 `canal` 、 `avro` 、および`maxwell` 。

### 例 {#example}

次のリクエストは、ID が`test5`および`sink_uri`が`blackhole://`のレプリケーション タスクを作成します。

```shell
curl -X POST -H "'Content-type':'application/json'" http://127.0.0.1:8300/api/v1/changefeeds -d '{"changefeed_id":"test5","sink_uri":"blackhole://"}'
```

リクエストが成功すると`202 Accepted`が返されます。リクエストが失敗した場合は、エラー メッセージとエラー コードが返されます。

## レプリケーションタスクを削除する {#remove-a-replication-task}

この API は非同期インターフェイスです。リクエストが成功すると`202 Accepted`が返されます。返された結果は、サーバーがコマンドの実行に同意したことを意味するだけで、コマンドが正常に実行されることを保証するものではありません。

### リクエストURI {#request-uri}

`DELETE /api/v1/changefeeds/{changefeed_id}`

### パラメータの説明 {#parameter-description}

#### パスパラメータ {#path-parameters}

| パラメータ名          | 説明                              |
| :-------------- | :------------------------------ |
| `changefeed_id` | 削除するレプリケーション タスク (変更フィード) の ID。 |

### 例 {#example}

次のリクエストは、ID `test1`のレプリケーション タスクを削除します。

```shell
curl -X DELETE http://127.0.0.1:8300/api/v1/changefeeds/test1
```

リクエストが成功すると`202 Accepted`が返されます。リクエストが失敗した場合は、エラー メッセージとエラー コードが返されます。

## レプリケーション構成を更新する {#update-the-replication-configuration}

この API は非同期インターフェイスです。リクエストが成功すると`202 Accepted`が返されます。返された結果は、サーバーがコマンドの実行に同意したことを意味するだけで、コマンドが正常に実行されることを保証するものではありません。

チェンジフィード構成を変更するには、 `pause the replication task -> modify the configuration -> resume the replication task`の手順に従います。

### リクエストURI {#request-uri}

`PUT /api/v1/changefeeds/{changefeed_id}`

### パラメータの説明 {#parameter-description}

#### パスパラメータ {#path-parameters}

| パラメータ名          | 説明                              |
| :-------------- | :------------------------------ |
| `changefeed_id` | 更新するレプリケーション タスク (変更フィード) の ID。 |

#### リクエストボディのパラメータ {#parameters-for-the-request-body}

現在、API 経由で変更できるのは次の構成のみです。

|パラメータ名 |説明 | | :---------------------- | :-------------------------- ------------ ---- | | `target_ts` | `UINT64`タイプ。変更フィードのターゲット TSO を指定します。 (オプション) | | `sink_uri` | `STRING`型。レプリケーションタスクの下流アドレス。 (オプション) | | `filter_rules` | `STRING`型配列。テーブルスキーマフィルタリングのルール。 (オプション) | | `ignore_txn_start_ts` | `UINT64`型配列。指定された start_ts のトランザクションを無視します。 (オプション) | | `mounter_worker_num` | `INT`型。マウンターのスレッド番号。 (オプション) | | `sink_config` |シンクの構成パラメータ。 (オプション) |

上記パラメータの意味は[レプリケーションタスクを作成する](#create-a-replication-task)項と同様です。詳細については、そのセクションを参照してください。

### 例 {#example}

次のリクエストは、ID が`test1`レプリケーション タスクの`mounter_worker_num`を`32`に更新します。

```shell
 curl -X PUT -H "'Content-type':'application/json'" http://127.0.0.1:8300/api/v1/changefeeds/test1 -d '{"mounter_worker_num":32}'
```

リクエストが成功すると`202 Accepted`が返されます。リクエストが失敗した場合は、エラー メッセージとエラー コードが返されます。

## レプリケーションタスクリストのクエリ {#query-the-replication-task-list}

この API は同期インターフェイスです。リクエストが成功すると、TiCDC クラスター内のすべてのノードの基本情報が返されます。

### リクエストURI {#request-uri}

`GET /api/v1/changefeeds`

### パラメータの説明 {#parameter-description}

#### クエリパラメータ {#query-parameters}

|パラメータ名 |説明 | | :------ | :------------------------------------------ ----- | | `state` |このパラメーターを指定すると、この状態のレプリケーション ステータス情報のみが返されます。(オプション) |

`state`の値のオプションは`all` 、 `normal` 、 `stopped` 、 `error` 、 `failed` 、および`finished`です。

このパラメータが指定されていない場合、デフォルトでは、状態が正常、停止、または失敗のレプリケーション タスクの基本情報が返されます。

### 例 {#example}

次のリクエストは、状態が`normal`であるすべてのレプリケーション タスクの基本情報をクエリします。

```shell
curl -X GET http://127.0.0.1:8300/api/v1/changefeeds?state=normal
```

```json
[
    {
        "id": "test1",
        "state": "normal",
        "checkpoint_tso": 426921294362574849,
        "checkpoint_time": "2021-08-10 14:04:54.242",
        "error": null
    },
    {
        "id": "test2",
        "state": "normal",
        "checkpoint_tso": 426921294362574849,
        "checkpoint_time": "2021-08-10 14:04:54.242",
        "error": null
    }
]
```

上記で返された結果のフィールドは次のように説明されます。

-   id: レプリケーションタスクのID。
-   state: レプリケーションタスクの現在の[州](/ticdc/ticdc-changefeed-overview.md#changefeed-state-transfer) 。
-   checkpoint_tso: レプリケーション タスクの現在のチェックポイントの TSO 表現。
-   checkpoint_time: レプリケーション タスクの現在のチェックポイントの形式化された時刻表現。
-   error: レプリケーションタスクのエラー情報。

## 特定のレプリケーションタスクをクエリする {#query-a-specific-replication-task}

この API は同期インターフェイスです。リクエストが成功すると、指定したレプリケーション タスクの詳細情報が返されます。

### リクエストURI {#request-uri}

`GET /api/v1/changefeeds/{changefeed_id}`

### パラメータの説明 {#parameter-description}

#### パスパラメータ {#path-parameters}

| パラメータ名          | 説明                                |
| :-------------- | :-------------------------------- |
| `changefeed_id` | クエリ対象のレプリケーション タスク (変更フィード) の ID。 |

### 例 {#example}

次のリクエストは、ID `test1`のレプリケーション タスクの詳細情報をクエリします。

```shell
curl -X GET http://127.0.0.1:8300/api/v1/changefeeds/test1
```

```json
{
    "id": "test1",
    "sink_uri": "blackhole://",
    "create_time": "2021-08-10 11:41:30.642",
    "start_ts": 426919038970232833,
    "target_ts": 0,
    "checkpoint_tso": 426921014615867393,
    "checkpoint_time": "2021-08-10 13:47:07.093",
    "sort_engine": "unified",
    "state": "normal",
    "error": null,
    "error_history": null,
    "creator_version": "",
    "task_status": [
        {
            "capture_id": "d8924259-f52f-4dfb-97a9-c48d26395945",
            "table_ids": [
                63,
                65
            ],
            "table_operations": {}
        }
    ]
}
```

## レプリケーションタスクを一時停止する {#pause-a-replication-task}

この API は非同期インターフェイスです。リクエストが成功すると`202 Accepted`が返されます。返された結果は、サーバーがコマンドの実行に同意したことを意味するだけで、コマンドが正常に実行されることを保証するものではありません。

### リクエストURI {#request-uri}

`POST /api/v1/changefeeds/{changefeed_id}/pause`

### パラメータの説明 {#parameter-description}

#### パスパラメータ {#path-parameters}

| パラメータ名          | 説明                                |
| :-------------- | :-------------------------------- |
| `changefeed_id` | 一時停止するレプリケーション タスク (変更フィード) の ID。 |

### 例 {#example}

次のリクエストは、ID `test1`のレプリケーション タスクを一時停止します。

```shell
curl -X POST http://127.0.0.1:8300/api/v1/changefeeds/test1/pause
```

リクエストが成功すると`202 Accepted`が返されます。リクエストが失敗した場合は、エラー メッセージとエラー コードが返されます。

## レプリケーションタスクを再開する {#resume-a-replication-task}

この API は非同期インターフェイスです。リクエストが成功すると`202 Accepted`が返されます。返された結果は、サーバーがコマンドの実行に同意したことを意味するだけで、コマンドが正常に実行されることを保証するものではありません。

### リクエストURI {#request-uri}

`POST /api/v1/changefeeds/{changefeed_id}/resume`

### パラメータの説明 {#parameter-description}

#### パスパラメータ {#path-parameters}

| パラメータ名          | 説明                              |
| :-------------- | :------------------------------ |
| `changefeed_id` | 再開するレプリケーション タスク (変更フィード) の ID。 |

### 例 {#example}

次のリクエストは、ID `test1`のレプリケーション タスクを再開します。

```shell
curl -X POST http://127.0.0.1:8300/api/v1/changefeeds/test1/resume
```

リクエストが成功すると`202 Accepted`が返されます。リクエストが失敗した場合は、エラー メッセージとエラー コードが返されます。

## レプリケーションサブタスクリストのクエリ {#query-the-replication-subtask-list}

この API は同期インターフェイスです。リクエストが成功すると、すべてのレプリケーション サブタスク ( `processor` ) の基本情報が返されます。

### リクエストURI {#request-uri}

`GET /api/v1/processors`

### 例 {#example}

```shell
curl -X GET http://127.0.0.1:8300/api/v1/processors
```

```json
[
    {
        "changefeed_id": "test1",
        "capture_id": "561c3784-77f0-4863-ad52-65a3436db6af"
    }
]
```

## 特定のレプリケーションサブタスクをクエリする {#query-a-specific-replication-subtask}

この API は同期インターフェイスです。リクエストが成功すると、指定されたレプリケーションサブタスク ( `processor` ) の詳細情報が返されます。

### リクエストURI {#request-uri}

`GET /api/v1/processors/{changefeed_id}/{capture_id}`

### パラメータの説明 {#parameter-description}

#### パスパラメータ {#path-parameters}

| パラメータ名          | 説明                              |
| :-------------- | :------------------------------ |
| `changefeed_id` | クエリ対象のレプリケーション サブタスクの変更フィード ID。 |
| `capture_id`    | クエリ対象のレプリケーション サブタスクのキャプチャ ID。  |

### 例 {#example}

次のリクエストは、 `changefeed_id`が`test` 、 `capture_id`が`561c3784-77f0-4863-ad52-65a3436db6af`であるサブタスクの詳細情報をクエリします。サブタスクは`changefeed_id`と`capture_id`で識別できます。

```shell
curl -X GET http://127.0.0.1:8300/api/v1/processors/test1/561c3784-77f0-4863-ad52-65a3436db6af
```

```json
{
    "checkpoint_ts": 426919123303006208,
    "resolved_ts": 426919123369066496,
    "table_ids": [
        63,
        65
    ],
    "error": null
}
```

## TiCDC サービス プロセス リストのクエリ {#query-the-ticdc-service-process-list}

この API は同期インターフェイスです。リクエストが成功すると、すべてのレプリケーション プロセスの基本情報 ( `capture` ) が返されます。

### リクエストURI {#request-uri}

`GET /api/v1/captures`

### 例 {#example}

```shell
curl -X GET http://127.0.0.1:8300/api/v1/captures
```

```json
[
    {
        "id": "561c3784-77f0-4863-ad52-65a3436db6af",
        "is_owner": true,
        "address": "127.0.0.1:8300"
    }
]
```

## 所有者ノードを削除する {#evict-an-owner-node}

この API は非同期インターフェイスです。リクエストが成功すると`202 Accepted`が返されます。返された結果は、サーバーがコマンドの実行に同意したことを意味するだけで、コマンドが正常に実行されることを保証するものではありません。

### リクエストURI {#request-uri}

`POST /api/v1/owner/resign`

### 例 {#example}

次のリクエストは、TiCDC の現在の所有者ノードを削除し、新しいラウンドの選挙をトリガーして新しい所有者ノードを生成します。

```shell
curl -X POST http://127.0.0.1:8300/api/v1/owner/resign
```

リクエストが成功すると`202 Accepted`が返されます。リクエストが失敗した場合は、エラー メッセージとエラー コードが返されます。

## レプリケーション タスク内のすべてのテーブルの負荷分散を手動でトリガーする {#manually-trigger-the-load-balancing-of-all-tables-in-a-replication-task}

この API は非同期インターフェイスです。リクエストが成功すると`202 Accepted`が返されます。返された結果は、サーバーがコマンドの実行に同意したことを意味するだけで、コマンドが正常に実行されることを保証するものではありません。

### リクエストURI {#request-uri}

`POST /api/v1/changefeeds/{changefeed_id}/tables/rebalance_table`

### パラメータの説明 {#parameter-description}

#### パスパラメータ {#path-parameters}

| パラメータ名          | 説明                                   |
| :-------------- | :----------------------------------- |
| `changefeed_id` | スケジュールされるレプリケーション タスク (変更フィード) の ID。 |

### 例 {#example}

次のリクエストは、ID `test1`を持つ変更フィード内のすべてのテーブルの負荷分散をトリガーします。

```shell
 curl -X POST http://127.0.0.1:8300/api/v1/changefeeds/test1/tables/rebalance_table
```

リクエストが成功すると`202 Accepted`が返されます。リクエストが失敗した場合は、エラー メッセージとエラー コードが返されます。

## テーブルを別のノードに手動でスケジュールする {#manually-schedule-a-table-to-another-node}

この API は非同期インターフェイスです。リクエストが成功すると`202 Accepted`が返されます。返された結果は、サーバーがコマンドの実行に同意したことを意味するだけで、コマンドが正常に実行されることを保証するものではありません。

### リクエストURI {#request-uri}

`POST /api/v1/changefeeds/{changefeed_id}/tables/move_table`

### パラメータの説明 {#parameter-description}

#### パスパラメータ {#path-parameters}

| パラメータ名          | 説明                                   |
| :-------------- | :----------------------------------- |
| `changefeed_id` | スケジュールされるレプリケーション タスク (変更フィード) の ID。 |

#### リクエストボディのパラメータ {#parameters-for-the-request-body}

| パラメータ名              | 説明                |
| :------------------ | :---------------- |
| `target_capture_id` | ターゲット キャプチャの ID。  |
| `table_id`          | スケジュールするテーブルの ID。 |

### 例 {#example}

次のリクエストは、ID `test1`の変更フィード内の ID `49`のテーブルを ID `6f19a6d9-0f8c-4dc9-b299-3ba7c0f216f5`のキャプチャにスケジュールします。

```shell
curl -X POST -H "'Content-type':'application/json'" http://127.0.0.1:8300/api/v1/changefeeds/changefeed-test1/tables/move_table -d '{"capture_id":"6f19a6d9-0f8c-4dc9-b299-3ba7c0f216f5","table_id":49}'

```

リクエストが成功すると`202 Accepted`が返されます。リクエストが失敗した場合は、エラー メッセージとエラー コードが返されます。

## TiCDCサーバーのログ レベルを動的に調整する {#dynamically-adjust-the-log-level-of-the-ticdc-server}

この API は同期インターフェイスです。リクエストが成功すると`202 OK`が返されます。

### リクエストURI {#request-uri}

`POST /api/v1/log`

### リクエストパラメータ {#request-parameters}

#### リクエストボディのパラメータ {#parameters-for-the-request-body}

| パラメータ名      | 説明         |
| :---------- | :--------- |
| `log_level` | 設定するログレベル。 |

`log_level` 「debug」、「info」、「warn」、「error」、「dpanic」、「panic」、および「fatal」の[zap によって提供されるログ レベル](https://godoc.org/go.uber.org/zap#UnmarshalText)をサポートします。

### 例 {#example}

```shell
curl -X POST -H "'Content-type':'application/json'" http://127.0.0.1:8300/api/v1/log -d '{"log_level":"debug"}'

```

リクエストが成功すると`202 OK`が返されます。リクエストが失敗した場合は、エラー メッセージとエラー コードが返されます。
