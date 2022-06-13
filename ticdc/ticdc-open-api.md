---
title: TiCDC OpenAPI
summary: Learn how to use the OpenAPI interface to manage the cluster status and data replication.
---

# TiCDC OpenAPI {#ticdc-openapi}

<!-- markdownlint-disable MD024 -->

TiCDCは、TiCDCクラスタを照会および操作するためのOpenAPI機能を提供します。これは、 [`cdc cli`ツール](/ticdc/manage-ticdc.md#use-cdc-cli-to-manage-cluster-status-and-data-replication-task)の機能と同様です。

APIを使用して、TiCDCクラスタで次のメンテナンス操作を実行できます。

-   [TiCDCノードのステータス情報を取得します](#get-the-status-information-of-a-ticdc-node)
-   [TiCDCクラスタのヘルスステータスを確認します](#check-the-health-status-of-a-ticdc-cluster)
-   [レプリケーションタスクを作成する](#create-a-replication-task)
-   [レプリケーションタスクを削除する](#remove-a-replication-task)
-   [レプリケーション構成を更新します](#update-the-replication-configuration)
-   [レプリケーションタスクリストをクエリする](#query-the-replication-task-list)
-   [特定のレプリケーションタスクをクエリする](#query-a-specific-replication-task)
-   [レプリケーションタスクを一時停止します](#pause-a-replication-task)
-   [レプリケーションタスクを再開します](#resume-a-replication-task)
-   [レプリケーションサブタスクリストをクエリします](#query-the-replication-subtask-list)
-   [特定のレプリケーションサブタスクをクエリする](#query-a-specific-replication-subtask)
-   [TiCDCサービスプロセスリストを照会する](#query-the-ticdc-service-process-list)
-   [所有者ノードを削除します](#evict-an-owner-node)
-   [レプリケーションタスクですべてのテーブルの負荷分散を手動でトリガーします](#manually-trigger-the-load-balancing-of-all-tables-in-a-replication-task)
-   [テーブルを別のノードに手動でスケジュールする](#manually-schedule-a-table-to-another-node)
-   [TiCDCサーバーのログレベルを動的に調整します](#dynamically-adjust-the-log-level-of-the-ticdc-server)

すべてのAPIのリクエスト本文と戻り値はJSON形式です。次のセクションでは、APIの具体的な使用法について説明します。

次の例では、TiCDCサーバーのリスニングIPアドレスは`127.0.0.1`で、ポートは`8300`です。 TiCDCサーバーの起動時に、指定したIPとポートを`--addr=ip:port`経由でバインドできます。

## APIエラーメッセージテンプレート {#api-error-message-template}

APIリクエストを送信した後、エラーが発生した場合、返されるエラーメッセージは次の形式になります。

```json
{
    "error_msg": "",
    "error_code": ""
}
```

上記のJSON出力から、 `error_msg`はエラーメッセージを示し、 `error_code`は対応するエラーコードです。

## TiCDCノードのステータス情報を取得します {#get-the-status-information-of-a-ticdc-node}

このAPIは同期インターフェースです。リクエストが成功すると、対応するノードのステータス情報が返されます。

### URIをリクエストする {#request-uri}

`GET /api/v1/status`

### 例 {#example}

次のリクエストは、IPアドレスが`127.0.0.1`でポート番号が`8300`のTiCDCノードのステータス情報を取得します。

{{< copyable "" >}}

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

上記の出力のフィールドは次のように説明されています。

-   version：現在のTiCDCバージョン番号。
-   git_hash：Gitハッシュ値。
-   id：ノードのキャプチャID。
-   pid：ノードのキャプチャプロセスPID。
-   is_owner：ノードが所有者であるかどうかを示します。

## TiCDCクラスタのヘルスステータスを確認します {#check-the-health-status-of-a-ticdc-cluster}

このAPIは同期インターフェースです。クラスタが正常である場合、 `200 OK`が返されます。

### URIをリクエストする {#request-uri}

`GET /api/v1/health`

### 例 {#example}

{{< copyable "" >}}

```shell
curl -X GET http://127.0.0.1:8300/api/v1/health
```

## レプリケーションタスクを作成する {#create-a-replication-task}

このAPIは非同期インターフェースです。リクエストが成功すると、 `202 Accepted`が返されます。返された結果は、サーバーがコマンドの実行に同意したことを意味するだけであり、コマンドが正常に実行されることを保証するものではありません。

### URIをリクエストする {#request-uri}

`POST /api/v1/changefeeds`

### パラメータの説明 {#parameter-description}

`cli`コマンドを使用してレプリケーションタスクを作成するためのオプションのパラメーターと比較すると、APIを使用してそのようなタスクを作成するためのオプションのパラメーターはそれほど完全ではありません。このAPIは、次のパラメーターをサポートします。

#### リクエスト本文のパラメータ {#parameters-for-the-request-body}

|パラメータ名|説明| | ：------------------------ | ：---------------------- --------------------------- ---- | | `changefeed_id` | `STRING`タイプ。レプリケーションタスクのID。 （オプション）| | `start_ts` | `UINT64`タイプ。チェンジフィードの開始TSOを指定します。 （オプション）| | `target_ts` | `UINT64`タイプ。チェンジフィードのターゲットTSOを指定します。 （オプション）| | **`sink_uri`** | `STRING`タイプ。レプリケーションタスクのダウンストリームアドレス。 （<strong>必須</strong>）| | `force_replicate` | `BOOLEAN`タイプ。一意のインデックスなしでテーブルを強制的に複製するかどうかを決定します。 （オプション）| | `ignore_ineligible_table` | `BOOLEAN`タイプ。複製できないテーブルを無視するかどうかを決定します。 （オプション）| | `filter_rules` | `STRING`型配列。テーブルスキーマフィルタリングのルール。 （オプション）| | `ignore_txn_start_ts` | `UINT64`型配列。指定されたstart_tsのトランザクションを無視します。 （オプション）| | `mounter_worker_num` | `INT`タイプ。マウンターのスレッド番号。 （オプション）| | `sink_config` |シンクの構成パラメーター。 （オプション）|

`changefeed_id` 、および`start_ts`の意味と形式は、 `target_ts`の[`cdc cli`を使用してレプリケーションタスクを作成します](/ticdc/manage-ticdc.md#create-a-replication-task)で説明されているものと同じ`sink_uri` 。これらのパラメータの詳細については、このドキュメントを参照してください。 `sink_uri`で証明書パスを指定するときは、対応する証明書が対応するTiCDCサーバーにアップロードされていることを確認してください。

上記の表の他のいくつかのパラメータについて、以下でさらに説明します。

`force_replicate` ：このパラメーターのデフォルトは`false`です。 `true`と指定すると、TiCDCは一意のインデックスを持たないテーブルを強制的に複製しようとします。

`ignore_ineligible_table` ：このパラメーターのデフォルトは`false`です。 `true`として指定されている場合、TiCDCは複製できないテーブルを無視します。

`filter_rules` ： `filter_rules = ['foo*.*','bar*.*']`などのテーブルスキーマフィルタリングのルール。詳細については、 [テーブルフィルター](/table-filter.md)のドキュメントを参照してください。

`ignore_txn_start_ts` ：このパラメーターを指定すると、指定したstart_tsは無視されます。たとえば、 `ignore-txn-start-ts = [1, 2]` 。

`mounter_worker_num` ：マウンターのスレッド番号。マウンターは、TiKVから出力されたデータをデコードするために使用されます。デフォルト値は`16`です。

シンクの構成パラメーターは次のとおりです。

```json
{
  "dispatchers":[
    {"matcher":["test1.*", "test2.*"], "dispatcher":"ts"},
    {"matcher":["test3.*", "test4.*"], "dispatcher":"rowid"}
  ],
  "protocal":"canal-json"
}
```

`dispatchers` ：MQタイプのシンクの場合、ディスパッチャーを使用してイベントディスパッチャーを構成できます。 `ts` `table`のディスパッチャがサポートされています： `default` 、および`rowid` 。ディスパッチャのルールは次のとおりです。

-   `default` ：複数の一意のインデックス（主キーを含む）が存在する場合、または古い値機能が有効になっている場合、イベントは`table`モードでディスパッチされます。一意のインデックス（または主キー）が1つしかない場合、イベントは`rowid`モードでディスパッチされます。
-   `ts` ：行変更のcommitTを使用して、ハッシュ値とディスパッチイベントを作成します。
-   `rowid` ：選択したHandleKey列の名前と値を使用して、ハッシュ値とディスパッチイベントを作成します。
-   `table` ：テーブルのスキーマ名とテーブル名を使用して、ハッシュ値とディスパッチイベントを作成します。

`matcher` ：マッチャーのマッチング構文はフィルタールール構文と同じです。

`protocol` ：MQタイプのシンクの場合、メッセージのプロトコル形式を指定できます。現在、次のプロトコルがサポートされて`maxwell` `open-protocol` ： `canal-json` 、 `avro` `canal` 。

### 例 {#example}

次のリクエストは、IDが`test5`で`sink_uri`が`blackhome://`のレプリケーションタスクを作成します。

{{< copyable "" >}}

```shell
curl -X POST -H "'Content-type':'application/json'" http://127.0.0.1:8300/api/v1/changefeeds -d '{"changefeed_id":"test5","sink_uri":"blackhole://"}'
```

リクエストが成功すると、 `202 Accepted`が返されます。リクエストが失敗した場合、エラーメッセージとエラーコードが返されます。

## レプリケーションタスクを削除する {#remove-a-replication-task}

このAPIは非同期インターフェースです。リクエストが成功すると、 `202 Accepted`が返されます。返された結果は、サーバーがコマンドの実行に同意したことを意味するだけであり、コマンドが正常に実行されることを保証するものではありません。

### URIをリクエストする {#request-uri}

`DELETE /api/v1/changefeeds/{changefeed_id}`

### パラメータの説明 {#parameter-description}

#### パスパラメータ {#path-parameters}

| パラメータ名          | 説明                              |
| :-------------- | :------------------------------ |
| `changefeed_id` | 削除するレプリケーションタスク（changefeed）のID。 |

### 例 {#example}

次のリクエストは、 `test1`のレプリケーションタスクを削除します。

{{< copyable "" >}}

```shell
curl -X DELETE http://127.0.0.1:8300/api/v1/changefeeds/test1
```

リクエストが成功すると、 `202 Accepted`が返されます。リクエストが失敗した場合、エラーメッセージとエラーコードが返されます。

## レプリケーション構成を更新します {#update-the-replication-configuration}

このAPIは非同期インターフェースです。リクエストが成功すると、 `202 Accepted`が返されます。返された結果は、サーバーがコマンドの実行に同意したことを意味するだけであり、コマンドが正常に実行されることを保証するものではありません。

チェンジフィード構成を変更するには、 `pause the replication task -> modify the configuration -> resume the replication task`の手順に従います。

### URIをリクエストする {#request-uri}

`PUT /api/v1/changefeeds/{changefeed_id}`

### パラメータの説明 {#parameter-description}

#### パスパラメータ {#path-parameters}

| パラメータ名          | 説明                              |
| :-------------- | :------------------------------ |
| `changefeed_id` | 更新するレプリケーションタスク（changefeed）のID。 |

#### リクエスト本文のパラメータ {#parameters-for-the-request-body}

現在、APIを介して変更できるのは次の構成のみです。

|パラメータ名|説明| | ：-------------------- | ：-------------------------- ----------------------- ---- | | `target_ts` | `UINT64`タイプ。チェンジフィードのターゲットTSOを指定します。 （オプション）| | `sink_uri` | `STRING`タイプ。レプリケーションタスクのダウンストリームアドレス。 （オプション）| | `filter_rules` | `STRING`型配列。テーブルスキーマフィルタリングのルール。 （オプション）| | `ignore_txn_start_ts` | `UINT64`型配列。指定されたstart_tsのトランザクションを無視します。 （オプション）| | `mounter_worker_num` | `INT`タイプ。マウンターのスレッド番号。 （オプション）| | `sink_config` |シンクの構成パラメーター。 （オプション）|

上記のパラメータの意味は、 [レプリケーションタスクを作成する](#create-a-replication-task)セクションの意味と同じです。詳細については、そのセクションを参照してください。

### 例 {#example}

次のリクエストは、 `test1`から`32`のレプリケーションタスクの`mounter_worker_num`を更新します。

{{< copyable "" >}}

```shell
 curl -X PUT -H "'Content-type':'application/json'" http://127.0.0.1:8300/api/v1/changefeeds/test1 -d '{"mounter_worker_num":32}'
```

リクエストが成功すると、 `202 Accepted`が返されます。リクエストが失敗した場合、エラーメッセージとエラーコードが返されます。

## レプリケーションタスクリストをクエリする {#query-the-replication-task-list}

このAPIは同期インターフェースです。要求が成功すると、TiCDCクラスタのすべてのノードの基本情報が返されます。

### URIをリクエストする {#request-uri}

`GET /api/v1/changefeeds`

### パラメータの説明 {#parameter-description}

#### クエリパラメータ {#query-parameters}

|パラメータ名|説明| | ：------ | ：---------------------------------------- ----- | | `state` |このパラメーターを指定すると、この状態のレプリケーション状況情報のみが返されます。（オプション）|

`state`の値`normal` `finished` 、 `all` 、 `error` `stopped` `failed` 。

このパラメーターが指定されていない場合、状態が正常、停止、または失敗したレプリケーション・タスクの基本情報がデフォルトで返されます。

### 例 {#example}

次のリクエストは、状態が`normal`であるすべてのレプリケーションタスクの基本情報を照会します。

{{< copyable "" >}}

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

上記の返される結果のフィールドは次のように説明されています。

-   id：レプリケーションタスクのID。
-   状態：レプリケーションタスクの現在の[州](/ticdc/manage-ticdc.md#state-transfer-of-replication-tasks) 。
-   checkpoint_tso：レプリケーションタスクの現在のチェックポイントのTSO表現。
-   checkpoint_tso：レプリケーションタスクの現在のチェックポイントのフォーマットされた時間表現。
-   エラー：レプリケーションタスクのエラー情報。

## 特定のレプリケーションタスクをクエリする {#query-a-specific-replication-task}

このAPIは同期インターフェースです。要求が成功すると、指定されたレプリケーションタスクの詳細情報が返されます。

### URIをリクエストする {#request-uri}

`GET /api/v1/changefeeds/{changefeed_id}`

### パラメータの説明 {#parameter-description}

#### パスパラメータ {#path-parameters}

| パラメータ名          | 説明                              |
| :-------------- | :------------------------------ |
| `changefeed_id` | 照会するレプリケーションタスク（changefeed）のID。 |

### 例 {#example}

次のリクエストは、 `test1`のレプリケーションタスクの詳細情報を照会します。

{{< copyable "" >}}

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

## レプリケーションタスクを一時停止します {#pause-a-replication-task}

このAPIは非同期インターフェースです。リクエストが成功すると、 `202 Accepted`が返されます。返される結果は、サーバーがコマンドの実行に同意したことを意味するだけであり、コマンドが正常に実行されることを保証するものではありません。

### URIをリクエストする {#request-uri}

`POST /api/v1/changefeeds/{changefeed_id}/pause`

### パラメータの説明 {#parameter-description}

#### パスパラメータ {#path-parameters}

| パラメータ名          | 説明                                |
| :-------------- | :-------------------------------- |
| `changefeed_id` | 一時停止するレプリケーションタスク（changefeed）のID。 |

### 例 {#example}

次のリクエストは、 `test1`のレプリケーションタスクを一時停止します。

{{< copyable "" >}}

```shell
curl -X POST http://127.0.0.1:8300/api/v1/changefeeds/test1/pause
```

リクエストが成功すると、 `202 Accepted`が返されます。リクエストが失敗した場合、エラーメッセージとエラーコードが返されます。

## レプリケーションタスクを再開します {#resume-a-replication-task}

このAPIは非同期インターフェースです。リクエストが成功すると、 `202 Accepted`が返されます。返される結果は、サーバーがコマンドの実行に同意したことを意味するだけであり、コマンドが正常に実行されることを保証するものではありません。

### URIをリクエストする {#request-uri}

`POST /api/v1/changefeeds/{changefeed_id}/resume`

### パラメータの説明 {#parameter-description}

#### パスパラメータ {#path-parameters}

| パラメータ名          | 説明                              |
| :-------------- | :------------------------------ |
| `changefeed_id` | 再開するレプリケーションタスク（changefeed）のID。 |

### 例 {#example}

次のリクエストは、 `test1`でレプリケーションタスクを再開します。

{{< copyable "" >}}

```shell
curl -X POST http://127.0.0.1:8300/api/v1/changefeeds/test1/resume
```

リクエストが成功すると、 `202 Accepted`が返されます。リクエストが失敗した場合、エラーメッセージとエラーコードが返されます。

## レプリケーションサブタスクリストをクエリします {#query-the-replication-subtask-list}

このAPIは同期インターフェースです。要求が成功すると、すべてのレプリケーションサブタスク（ `processor` ）の基本情報が返されます。

### URIをリクエストする {#request-uri}

`GET /api/v1/processors`

### 例 {#example}

{{< copyable "" >}}

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

このAPIは同期インターフェースです。要求が成功すると、指定されたレプリケーションサブタスク（ `processor` ）の詳細情報が返されます。

### URIをリクエストする {#request-uri}

`GET /api/v1/processors/{changefeed_id}/{capture_id}`

### パラメータの説明 {#parameter-description}

#### パスパラメータ {#path-parameters}

| パラメータ名          | 説明                         |
| :-------------- | :------------------------- |
| `changefeed_id` | 照会する複製サブタスクのチェンジフィードID。    |
| `capture_id`    | 照会するレプリケーションサブタスクのキャプチャID。 |

### 例 {#example}

次のリクエストは、 `changefeed_id`が`test`で`capture_id`が`561c3784-77f0-4863-ad52-65a3436db6af`のサブタスクの詳細情報を照会します。サブタスクは`changefeed_id`と`capture_id`で識別できます。

{{< copyable "" >}}

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

## TiCDCサービスプロセスリストを照会する {#query-the-ticdc-service-process-list}

このAPIは同期インターフェースです。要求が成功すると、すべてのレプリケーションプロセスの基本情報（ `capture` ）が返されます。

### URIをリクエストする {#request-uri}

`GET /api/v1/captures`

### 例 {#example}

{{< copyable "" >}}

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

## 所有者ノードを削除します {#evict-an-owner-node}

このAPIは非同期インターフェースです。リクエストが成功すると、 `202 Accepted`が返されます。返された結果は、サーバーがコマンドの実行に同意したことを意味するだけであり、コマンドが正常に実行されることを保証するものではありません。

### URIをリクエストする {#request-uri}

`POST /api/v1/owner/resign`

### 例 {#example}

次のリクエストは、TiCDCの現在の所有者ノードを削除し、新しい所有者ノードを生成するために新しいラウンドの選挙をトリガーします。

{{< copyable "" >}}

```shell
curl -X POST http://127.0.0.1:8300/api/v1/owner/resign
```

リクエストが成功すると、 `202 Accepted`が返されます。リクエストが失敗した場合、エラーメッセージとエラーコードが返されます。

## レプリケーションタスクですべてのテーブルの負荷分散を手動でトリガーします {#manually-trigger-the-load-balancing-of-all-tables-in-a-replication-task}

このAPIは非同期インターフェースです。リクエストが成功すると、 `202 Accepted`が返されます。返された結果は、サーバーがコマンドの実行に同意したことを意味するだけであり、コマンドが正常に実行されることを保証するものではありません。

### URIをリクエストする {#request-uri}

`POST /api/v1/changefeeds/{changefeed_id}/tables/rebalance_table`

### パラメータの説明 {#parameter-description}

#### パスパラメータ {#path-parameters}

| パラメータ名          | 説明                                  |
| :-------------- | :---------------------------------- |
| `changefeed_id` | スケジュールするレプリケーションタスク（changefeed）のID。 |

### 例 {#example}

次のリクエストは、 `test1`のチェンジフィード内のすべてのテーブルの負荷分散をトリガーします。

{{< copyable "" >}}

```shell
 curl -X POST http://127.0.0.1:8300/api/v1/changefeeds/test1/tables/rebalance_table
```

リクエストが成功すると、 `202 Accepted`が返されます。リクエストが失敗した場合、エラーメッセージとエラーコードが返されます。

## テーブルを別のノードに手動でスケジュールする {#manually-schedule-a-table-to-another-node}

このAPIは非同期インターフェースです。リクエストが成功すると、 `202 Accepted`が返されます。返された結果は、サーバーがコマンドの実行に同意したことを意味するだけであり、コマンドが正常に実行されることを保証するものではありません。

### URIをリクエストする {#request-uri}

`POST /api/v1/changefeeds/{changefeed_id}/tables/move_table`

### パラメータの説明 {#parameter-description}

#### パスパラメータ {#path-parameters}

| パラメータ名          | 説明                                  |
| :-------------- | :---------------------------------- |
| `changefeed_id` | スケジュールするレプリケーションタスク（changefeed）のID。 |

#### リクエスト本文のパラメータ {#parameters-for-the-request-body}

| パラメータ名              | 説明               |
| :------------------ | :--------------- |
| `target_capture_id` | ターゲットキャプチャのID。   |
| `table_id`          | スケジュールするテーブルのID。 |

### 例 {#example}

次のリクエストは、 `test1`のチェンジフィードにある`49`のテーブルを、 `6f19a6d9-0f8c-4dc9-b299-3ba7c0f216f5`のキャプチャにスケジュールします。

{{< copyable "" >}}

```shell
curl -X POST -H "'Content-type':'application/json'" http://127.0.0.1:8300/api/v1/changefeeds/changefeed-test1/tables/move_table -d '{"capture_id":"6f19a6d9-0f8c-4dc9-b299-3ba7c0f216f5","table_id":49}'

```

リクエストが成功すると、 `202 Accepted`が返されます。リクエストが失敗した場合、エラーメッセージとエラーコードが返されます。

## TiCDCサーバーのログレベルを動的に調整します {#dynamically-adjust-the-log-level-of-the-ticdc-server}

このAPIは同期インターフェースです。リクエストが成功すると、 `202 OK`が返されます。

### URIをリクエストする {#request-uri}

`POST /api/v1/log`

### リクエストパラメータ {#request-parameters}

#### リクエスト本文のパラメータ {#parameters-for-the-request-body}

| パラメータ名      | 説明         |
| :---------- | :--------- |
| `log_level` | 設定するログレベル。 |

`log_level`は、「debug」、「info」、「warn」、「error」、「dpanic」、「panic」、および「fatal」の[zapによって提供されるログレベル](https://godoc.org/go.uber.org/zap#UnmarshalText)をサポートします。

### 例 {#example}

{{< copyable "" >}}

```shell
curl -X POST -H "'Content-type':'application/json'" http://127.0.0.1:8300/api/v1/log -d '{"log_level":"debug"}'

```

リクエストが成功すると、 `202 OK`が返されます。リクエストが失敗した場合、エラーメッセージとエラーコードが返されます。
