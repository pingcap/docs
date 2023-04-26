---
title: TiCDC OpenAPI v1
summary: Learn how to use the OpenAPI interface to manage the cluster status and data replication.
---

# TiCDC OpenAPI v1 {#ticdc-openapi-v1}

<!-- markdownlint-disable MD024 -->

> **ノート**
>
> TiCDC OpenAPI v1 は非推奨であり、将来削除される予定です。 [TiCDC OpenAPI v2](/ticdc/ticdc-open-api-v2.md)を使用することをお勧めします。

TiCDC は、TiCDC クラスターを照会および操作するための OpenAPI 機能を提供します。これは[`cdc cli`ツール](/ticdc/ticdc-manage-changefeed.md)の機能に似ています。

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
-   [レプリケーション タスクですべてのテーブルの負荷分散を手動でトリガーする](#manually-trigger-the-load-balancing-of-all-tables-in-a-replication-task)
-   [テーブルを別のノードに手動でスケジュールする](#manually-schedule-a-table-to-another-node)
-   [TiCDCサーバーのログレベルを動的に調整する](#dynamically-adjust-the-log-level-of-the-ticdc-server)

すべての API の要求本文と戻り値は JSON 形式です。以下のセクションでは、API の特定の使用法について説明します。

次の例では、TiCDCサーバーのリッスン IP アドレスは`127.0.0.1`で、ポートは`8300`です。 TiCDCサーバーの起動時に、指定した IP とポートを`--addr=ip:port`経由でバインドできます。

## API エラー メッセージ テンプレート {#api-error-message-template}

API リクエストの送信後にエラーが発生した場合、次の形式のエラー メッセージが返されます。

```json
{
    "error_msg": "",
    "error_code": ""
}
```

上記の JSON 出力から、 `error_msg`はエラー メッセージを表し、 `error_code`は対応するエラー コードです。

## TiCDC ノードのステータス情報を取得する {#get-the-status-information-of-a-ticdc-node}

この API は同期インターフェースです。リクエストが成功すると、対応するノードのステータス情報が返されます。

### リクエストURI {#request-uri}

`GET /api/v1/status`

### 例 {#example}

次のリクエストは、IP アドレスが`127.0.0.1`でポート番号が`8300` TiCDC ノードのステータス情報を取得します。

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

上記の出力のフィールドは次のとおりです。

-   version: 現在の TiCDC のバージョン番号。
-   git_hash: Git ハッシュ値。
-   id: ノードのキャプチャ ID。
-   pid: ノードのキャプチャ プロセス PID。
-   is_owner: ノードが所有者かどうかを示します。

## TiCDC クラスターのヘルス ステータスを確認する {#check-the-health-status-of-a-ticdc-cluster}

この API は同期インターフェースです。クラスターが正常な場合、 `200 OK`が返されます。

### リクエストURI {#request-uri}

`GET /api/v1/health`

### 例 {#example}

{{< copyable "" >}}

```shell
curl -X GET http://127.0.0.1:8300/api/v1/health
```

## レプリケーション タスクを作成する {#create-a-replication-task}

この API は非同期インターフェースです。リクエストが成功した場合、 `202 Accepted`が返されます。返された結果は、サーバーがコマンドの実行に同意したことを意味するだけで、コマンドが正常に実行されることを保証するものではありません。

### リクエストURI {#request-uri}

`POST /api/v1/changefeeds`

### パラメータの説明 {#parameter-description}

`cli`コマンドを使用してレプリケーション タスクを作成するためのオプション パラメータと比較すると、API を使用してそのようなタスクを作成するためのオプション パラメータは完全ではありません。この API は、次のパラメーターをサポートしています。

#### リクエスト本文のパラメータ {#parameters-for-the-request-body}

| |パラメータ名 |説明 | | | :------------------------ | : ---------------------- --------------------------- ---- | | | `changefeed_id` | `STRING`タイプ。レプリケーション タスクの ID。 (オプション) | | | `start_ts` | `UINT64`型。 changefeed の開始 TSO を指定します。 (オプション) | | | `target_ts` | `UINT64`型。 changefeed のターゲット TSO を指定します。 (オプション) | | | **`sink_uri`** | `STRING`型。レプリケーション タスクのダウンストリーム アドレス。 (<strong>必須</strong>) | | | `force_replicate` | `BOOLEAN`型。一意のインデックスを持たないテーブルを強制的にレプリケートするかどうかを決定します。 (オプション) | | | `ignore_ineligible_table` | `BOOLEAN`型。レプリケートできないテーブルを無視するかどうかを決定します。 (オプション) | | | `filter_rules` | `STRING`型配列。テーブル スキーマ フィルタリングのルール。 (オプション) | | | `ignore_txn_start_ts` | `UINT64`型配列。指定した start_ts のトランザクションを無視します。 (オプション) | | | `mounter_worker_num` | `INT`型。マウンターのスレッド番号。 (オプション) | | | `sink_config` |シンクの構成パラメーター。 (オプション) |

`changefeed_id` 、 `start_ts` 、 `target_ts` 、および`sink_uri`の意味と形式は、 [`cdc cli`を使用してレプリケーション タスクを作成する](/ticdc/ticdc-manage-changefeed.md#create-a-replication-task)ドキュメントで説明されているものと同じです。これらのパラメータの詳細な説明については、このドキュメントを参照してください。 `sink_uri`で証明書パスを指定するときは、対応する証明書を対応する TiCDCサーバーにアップロードしたことを確認してください。

上記の表のその他のパラメータについては、以下で詳しく説明します。

`force_replicate` : このパラメータのデフォルトは`false`です。 `true`と指定すると、TiCDC はユニーク インデックスを持たないテーブルを強制的に複製しようとします。

`ignore_ineligible_table` : このパラメータのデフォルトは`false`です。 `true`と指定すると、TiCDC はレプリケートできないテーブルを無視します。

`filter_rules` : `filter_rules = ['foo*.*','bar*.*']`などのテーブル スキーマ フィルタリングのルール。詳細は[テーブル フィルター](/table-filter.md)ドキュメントを参照してください。

`ignore_txn_start_ts` : このパラメーターを指定すると、指定された start_ts は無視されます。たとえば、 `ignore-txn-start-ts = [1, 2]`です。

`mounter_worker_num` : マウンタのスレッド番号。マウンタは、TiKV から出力されたデータをデコードするために使用されます。デフォルト値は`16`です。

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

`dispatchers` : MQ タイプのシンクの場合、ディスパッチャーを使用してイベント ディスパッチャーを構成できます。 `default` 、 `ts` 、 `rowid` 、および`table` 4 つのディスパッチャがサポートされています。ディスパッチャのルールは次のとおりです。

-   `default` : 複数の一意のインデックス (主キーを含む) が存在する場合、または古い値機能が有効になっている場合、イベントは`table`モードでディスパッチされます。一意のインデックス (または主キー) が 1 つだけ存在する場合、イベントは`rowid`モードで送出されます。
-   `ts` : 行変更の commitTs を使用してハッシュ値を作成し、イベントをディスパッチします。
-   `rowid` : 選択した HandleKey 列の名前と値を使用してハッシュ値を作成し、イベントをディスパッチします。
-   `table` : テーブルのスキーマ名とテーブル名を使用してハッシュ値を作成し、イベントをディスパッチします。

`matcher` : マッチャーのマッチング構文は、フィルター ルールの構文と同じです。

`protocol` : MQ タイプのシンクの場合、メッセージのプロトコル形式を指定できます。現在、次のプロトコルがサポートされています: `canal-json` 、 `open-protocol` 、 `canal` 、 `avro` 、および`maxwell` 。

### 例 {#example}

次のリクエストは、ID が`test5`で`sink_uri` of `blackhome://`のレプリケーション タスクを作成します。

{{< copyable "" >}}

```shell
curl -X POST -H "'Content-type':'application/json'" http://127.0.0.1:8300/api/v1/changefeeds -d '{"changefeed_id":"test5","sink_uri":"blackhole://"}'
```

リクエストが成功した場合、 `202 Accepted`が返されます。リクエストが失敗すると、エラー メッセージとエラー コードが返されます。

## レプリケーション タスクを削除する {#remove-a-replication-task}

この API は非同期インターフェースです。リクエストが成功した場合、 `202 Accepted`が返されます。返された結果は、サーバーがコマンドの実行に同意したことを意味するだけで、コマンドが正常に実行されることを保証するものではありません。

### リクエストURI {#request-uri}

`DELETE /api/v1/changefeeds/{changefeed_id}`

### パラメータの説明 {#parameter-description}

#### パス パラメータ {#path-parameters}

| パラメータ名          | 説明                                  |
| :-------------- | :---------------------------------- |
| `changefeed_id` | 削除するレプリケーション タスク (changefeed) の ID。 |

### 例 {#example}

次のリクエストは、ID `test1`のレプリケーション タスクを削除します。

{{< copyable "" >}}

```shell
curl -X DELETE http://127.0.0.1:8300/api/v1/changefeeds/test1
```

リクエストが成功した場合、 `202 Accepted`が返されます。リクエストが失敗すると、エラー メッセージとエラー コードが返されます。

## レプリケーション構成を更新する {#update-the-replication-configuration}

この API は非同期インターフェースです。リクエストが成功した場合、 `202 Accepted`が返されます。返された結果は、サーバーがコマンドの実行に同意したことを意味するだけで、コマンドが正常に実行されることを保証するものではありません。

changefeed 構成を変更するには、 `pause the replication task -> modify the configuration -> resume the replication task`の手順に従います。

### リクエストURI {#request-uri}

`PUT /api/v1/changefeeds/{changefeed_id}`

### パラメータの説明 {#parameter-description}

#### パス パラメータ {#path-parameters}

| パラメータ名          | 説明                                  |
| :-------------- | :---------------------------------- |
| `changefeed_id` | 更新するレプリケーション タスク (changefeed) の ID。 |

#### リクエスト本文のパラメータ {#parameters-for-the-request-body}

現在、API 経由で変更できるのは次の構成のみです。

| |パラメータ名 |説明 | | | :-------------------- | : -------------------------- ----------------------------------- ---- | | | `target_ts` | `UINT64`タイプ。 changefeed のターゲット TSO を指定します。 (オプション) | | | `sink_uri` | `STRING`型。レプリケーション タスクのダウンストリーム アドレス。 (オプション) | | | `filter_rules` | `STRING`型配列。テーブル スキーマ フィルタリングのルール。 (オプション) | | | `ignore_txn_start_ts` | `UINT64`型配列。指定した start_ts のトランザクションを無視します。 (オプション) | | | `mounter_worker_num` | `INT`型。マウンターのスレッド番号。 (オプション) | | | `sink_config` |シンクの構成パラメーター。 (オプション) |

上記のパラメータの意味は、セクション[レプリケーション タスクを作成する](#create-a-replication-task)と同じです。詳細については、そのセクションを参照してください。

### 例 {#example}

次のリクエストは、レプリケーション タスクの`mounter_worker_num` ID `test1`から`32`に更新します。

{{< copyable "" >}}

```shell
 curl -X PUT -H "'Content-type':'application/json'" http://127.0.0.1:8300/api/v1/changefeeds/test1 -d '{"mounter_worker_num":32}'
```

リクエストが成功した場合、 `202 Accepted`が返されます。リクエストが失敗すると、エラー メッセージとエラー コードが返されます。

## レプリケーション タスク リストを照会する {#query-the-replication-task-list}

この API は同期インターフェースです。リクエストが成功すると、TiCDC クラスター内のすべてのノードの基本情報が返されます。

### リクエストURI {#request-uri}

`GET /api/v1/changefeeds`

### パラメータの説明 {#parameter-description}

#### クエリ パラメータ {#query-parameters}

| |パラメータ名 |説明 | | | :-------- | :-------------------------------------------- ----- | | | `state` |このパラメーターを指定すると、この状態のレプリケーション ステータス情報のみが返されます。

`state`の値のオプションは`all` 、 `normal` 、 `stopped` 、 `error` 、 `failed` 、および`finished`です。

このパラメータが指定されていない場合、状態が正常、停止、または失敗のレプリケーション タスクの基本情報がデフォルトで返されます。

### 例 {#example}

次のリクエストは、状態が`normal`であるすべてのレプリケーション タスクの基本情報をクエリします。

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

上記の返された結果のフィールドは次のとおりです。

-   id: レプリケーション タスクの ID。
-   状態: レプリケーション タスクの現在の[州](/ticdc/ticdc-changefeed-overview.md#changefeed-state-transfer) 。
-   checkpoint_tso: レプリケーション タスクの現在のチェックポイントの TSO 表現。
-   checkpoint_time: レプリケーション タスクの現在のチェックポイントのフォーマットされた時間表現。
-   error: レプリケーション タスクのエラー情報。

## 特定のレプリケーション タスクを照会する {#query-a-specific-replication-task}

この API は同期インターフェースです。リクエストが成功すると、指定されたレプリケーション タスクの詳細情報が返されます。

### リクエストURI {#request-uri}

`GET /api/v1/changefeeds/{changefeed_id}`

### パラメータの説明 {#parameter-description}

#### パス パラメータ {#path-parameters}

| パラメータ名          | 説明                           |
| :-------------- | :--------------------------- |
| `changefeed_id` | 照会する複製タスク (changefeed) の ID。 |

### 例 {#example}

次のリクエストは、ID `test1`のレプリケーション タスクの詳細情報を照会します。

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

## レプリケーション タスクを一時停止する {#pause-a-replication-task}

この API は非同期インターフェースです。リクエストが成功した場合、 `202 Accepted`が返されます。返された結果は、サーバーがコマンドの実行に同意したことを意味するだけで、コマンドが正常に実行されることを保証するものではありません。

### リクエストURI {#request-uri}

`POST /api/v1/changefeeds/{changefeed_id}/pause`

### パラメータの説明 {#parameter-description}

#### パス パラメータ {#path-parameters}

| パラメータ名          | 説明                                    |
| :-------------- | :------------------------------------ |
| `changefeed_id` | 一時停止するレプリケーション タスク (changefeed) の ID。 |

### 例 {#example}

次のリクエストは、ID `test1`のレプリケーション タスクを一時停止します。

{{< copyable "" >}}

```shell
curl -X POST http://127.0.0.1:8300/api/v1/changefeeds/test1/pause
```

リクエストが成功した場合、 `202 Accepted`が返されます。リクエストが失敗すると、エラー メッセージとエラー コードが返されます。

## レプリケーション タスクを再開する {#resume-a-replication-task}

この API は非同期インターフェースです。リクエストが成功した場合、 `202 Accepted`が返されます。返された結果は、サーバーがコマンドの実行に同意したことを意味するだけで、コマンドが正常に実行されることを保証するものではありません。

### リクエストURI {#request-uri}

`POST /api/v1/changefeeds/{changefeed_id}/resume`

### パラメータの説明 {#parameter-description}

#### パス パラメータ {#path-parameters}

| パラメータ名          | 説明                                  |
| :-------------- | :---------------------------------- |
| `changefeed_id` | 再開するレプリケーション タスク (changefeed) の ID。 |

### 例 {#example}

次のリクエストは、ID `test1`のレプリケーション タスクを再開します。

{{< copyable "" >}}

```shell
curl -X POST http://127.0.0.1:8300/api/v1/changefeeds/test1/resume
```

リクエストが成功した場合、 `202 Accepted`が返されます。リクエストが失敗すると、エラー メッセージとエラー コードが返されます。

## レプリケーション サブタスク リストを照会する {#query-the-replication-subtask-list}

この API は同期インターフェースです。リクエストが成功すると、すべてのレプリケーション サブタスクの基本情報 ( `processor` ) が返されます。

### リクエストURI {#request-uri}

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

## 特定のレプリケーション サブタスクを照会する {#query-a-specific-replication-subtask}

この API は同期インターフェースです。リクエストが成功すると、指定されたレプリケーション サブタスクの詳細情報 ( `processor` ) が返されます。

### リクエストURI {#request-uri}

`GET /api/v1/processors/{changefeed_id}/{capture_id}`

### パラメータの説明 {#parameter-description}

#### パス パラメータ {#path-parameters}

| パラメータ名          | 説明                             |
| :-------------- | :----------------------------- |
| `changefeed_id` | 照会する複製サブタスクの変更フィード ID。         |
| `capture_id`    | クエリ対象のレプリケーション サブタスクのキャプチャ ID。 |

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

## TiCDC サービス プロセス リストのクエリ {#query-the-ticdc-service-process-list}

この API は同期インターフェースです。リクエストが成功すると、すべてのレプリケーション プロセスの基本情報 ( `capture` ) が返されます。

### リクエストURI {#request-uri}

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

## 所有者ノードを削除する {#evict-an-owner-node}

この API は非同期インターフェースです。リクエストが成功した場合、 `202 Accepted`が返されます。返された結果は、サーバーがコマンドの実行に同意したことを意味するだけで、コマンドが正常に実行されることを保証するものではありません。

### リクエストURI {#request-uri}

`POST /api/v1/owner/resign`

### 例 {#example}

次のリクエストは、TiCDC の現在の所有者ノードを削除し、新しい所有者ノードを生成するための新しいラウンドの選挙をトリガーします。

{{< copyable "" >}}

```shell
curl -X POST http://127.0.0.1:8300/api/v1/owner/resign
```

リクエストが成功した場合、 `202 Accepted`が返されます。リクエストが失敗すると、エラー メッセージとエラー コードが返されます。

## レプリケーション タスクですべてのテーブルの負荷分散を手動でトリガーする {#manually-trigger-the-load-balancing-of-all-tables-in-a-replication-task}

この API は非同期インターフェースです。リクエストが成功した場合、 `202 Accepted`が返されます。返された結果は、サーバーがコマンドの実行に同意したことを意味するだけで、コマンドが正常に実行されることを保証するものではありません。

### リクエストURI {#request-uri}

`POST /api/v1/changefeeds/{changefeed_id}/tables/rebalance_table`

### パラメータの説明 {#parameter-description}

#### パス パラメータ {#path-parameters}

| パラメータ名          | 説明                                      |
| :-------------- | :-------------------------------------- |
| `changefeed_id` | スケジュールするレプリケーション タスク (changefeed) の ID。 |

### 例 {#example}

次のリクエストは、ID が`test1`の changefeed 内のすべてのテーブルの負荷分散をトリガーします。

{{< copyable "" >}}

```shell
 curl -X POST http://127.0.0.1:8300/api/v1/changefeeds/test1/tables/rebalance_table
```

リクエストが成功した場合、 `202 Accepted`が返されます。リクエストが失敗すると、エラー メッセージとエラー コードが返されます。

## テーブルを別のノードに手動でスケジュールする {#manually-schedule-a-table-to-another-node}

この API は非同期インターフェースです。リクエストが成功した場合、 `202 Accepted`が返されます。返された結果は、サーバーがコマンドの実行に同意したことを意味するだけで、コマンドが正常に実行されることを保証するものではありません。

### リクエストURI {#request-uri}

`POST /api/v1/changefeeds/{changefeed_id}/tables/move_table`

### パラメータの説明 {#parameter-description}

#### パス パラメータ {#path-parameters}

| パラメータ名          | 説明                                      |
| :-------------- | :-------------------------------------- |
| `changefeed_id` | スケジュールするレプリケーション タスク (changefeed) の ID。 |

#### リクエスト本文のパラメータ {#parameters-for-the-request-body}

| パラメータ名              | 説明                |
| :------------------ | :---------------- |
| `target_capture_id` | ターゲット キャプチャの ID。  |
| `table_id`          | スケジュールするテーブルの ID。 |

### 例 {#example}

次のリクエストは、ID `test1`の changefeed 内の ID `49`のテーブルを ID `6f19a6d9-0f8c-4dc9-b299-3ba7c0f216f5`のキャプチャにスケジュールします。

{{< copyable "" >}}

```shell
curl -X POST -H "'Content-type':'application/json'" http://127.0.0.1:8300/api/v1/changefeeds/changefeed-test1/tables/move_table -d '{"capture_id":"6f19a6d9-0f8c-4dc9-b299-3ba7c0f216f5","table_id":49}'

```

リクエストが成功した場合、 `202 Accepted`が返されます。リクエストが失敗すると、エラー メッセージとエラー コードが返されます。

## TiCDCサーバーのログレベルを動的に調整する {#dynamically-adjust-the-log-level-of-the-ticdc-server}

この API は同期インターフェースです。リクエストが成功した場合、 `202 OK`が返されます。

### リクエストURI {#request-uri}

`POST /api/v1/log`

### リクエストパラメータ {#request-parameters}

#### リクエスト本文のパラメータ {#parameters-for-the-request-body}

| パラメータ名      | 説明          |
| :---------- | :---------- |
| `log_level` | 設定するログ レベル。 |

`log_level` [zap によって提供されるログ レベル](https://godoc.org/go.uber.org/zap#UnmarshalText)サポートします: &quot;debug&quot;、&quot;info&quot;、&quot;warn&quot;、&quot;error&quot;、&quot;dpanic&quot;、&quot;panic&quot;、および &quot;fatal&quot;。

### 例 {#example}

{{< copyable "" >}}

```shell
curl -X POST -H "'Content-type':'application/json'" http://127.0.0.1:8300/api/v1/log -d '{"log_level":"debug"}'

```

リクエストが成功した場合、 `202 OK`が返されます。リクエストが失敗すると、エラー メッセージとエラー コードが返されます。
