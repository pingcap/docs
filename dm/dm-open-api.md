---
title: Maintain DM Clusters Using OpenAPI
summary: Learn about how to use OpenAPI interface to manage the cluster status and data replication.
---

# OpenAPI を使用して DM クラスターを管理 {#maintain-dm-clusters-using-openapi}

DM は、DM クラスタのクエリと操作を簡単にするための OpenAPI 機能を提供します。これは[dmctl ツール](/dm/dmctl-introduction.md)の機能に似ています。

OpenAPI を有効にするには、次の操作のいずれかを実行します。

-   DM クラスターがバイナリを使用して直接デプロイされている場合は、次の構成を DM-master 構成ファイルに追加します。

    ```toml
    openapi = true
    ```

-   DM クラスターがTiUPを使用してデプロイされている場合は、次の構成をトポロジ ファイルに追加します。

    ```yaml
    server_configs:
      master:
        openapi: true
    ```

> **ノート：**
>
> -   DM は、OpenAPI 3.0.0 標準を満たす[仕様書](https://github.com/pingcap/tiflow/blob/master/dm/openapi/spec/dm.yaml)を提供します。このドキュメントには、すべてのリクエスト パラメータと戻り値が含まれています。ドキュメント yaml をコピーして[Swagger エディター](https://editor.swagger.io/)でプレビューできます。
>
> -   DM-master ノードをデプロイした後、 `http://{master-addr}/api/v1/docs`にアクセスしてドキュメントをオンラインでプレビューできます。

API を使用して、DM クラスターで次のメンテナンス操作を実行できます。

## クラスターを管理するための API {#apis-for-managing-clusters}

-   [DMマスターノードの情報を取得する](#get-the-information-of-a-dm-master-node)
-   [DM マスター ノードを停止する](#stop-a-dm-master-node)
-   [DM-worker ノードの情報を取得する](#get-the-information-of-a-dm-worker-node)
-   [DM-worker ノードを停止する](#stop-a-dm-worker-node)

## データ ソースを管理するための API {#apis-for-managing-data-sources}

-   [データ ソースを作成する](#create-a-data-source)
-   [データ ソースを取得する](#get-a-data-source)
-   [データ ソースを削除する](#delete-the-data-source)
-   [データ ソースを更新する](#update-a-data-source)
-   [データ ソースを有効にする](#enable-a-data-source)
-   [データ ソースを無効にする](#disable-a-data-source)
-   [データ ソースの情報を取得する](#get-the-information-of-a-data-source)
-   [データ ソース リストを取得する](#get-the-data-source-list)
-   [データ ソースのリレー ログ機能を開始する](#start-the-relay-log-feature-for-data-sources)
-   [データ ソースのリレー ログ機能を停止する](#stop-the-relay-log-feature-for-data-sources)
-   [不要になったリレー ログ ファイルをパージする](#purge-relay-log-files-that-are-no-longer-required)
-   [データ ソースと DM-worker 間のバインディングを変更する](#change-the-bindings-between-the-data-source-and-dm-workers)
-   [データ ソースのスキーマ名のリストを取得する](#get-the-list-of-schema-names-of-a-data-source)
-   [データ ソース内の指定されたスキーマのテーブル名のリストを取得します](#get-the-list-of-table-names-of-a-specified-schema-in-a-data-source)

## レプリケーション タスクを管理するための API {#apis-for-managing-replication-tasks}

-   [レプリケーション タスクを作成する](#create-a-replication-task)
-   [レプリケーション タスクを取得する](#get-a-replication-task)
-   [レプリケーション タスクを削除する](#delete-a-replication-task)
-   [レプリケーション タスクを更新する](#update-a-replication-task)
-   [レプリケーション タスクを開始する](#start-a-replication-task)
-   [レプリケーション タスクを停止する](#stop-a-replication-task)
-   [レプリケーション タスクの情報を取得する](#get-the-information-of-a-replication-task)
-   [レプリケーション タスク リストを取得する](#get-the-replication-task-list)
-   [レプリケーション タスクの移行ルールを取得する](#get-the-migration-rules-of-a-replication-task)
-   [レプリケーション タスクに関連付けられているデータ ソースのスキーマ名のリストを取得します](#get-the-list-of-schema-names-of-the-data-source-that-is-associated-with-a-replication-task)
-   [レプリケーション タスクに関連付けられているデータ ソース内の指定されたスキーマのテーブル名のリストを取得します](#get-the-list-of-table-names-of-a-specified-schema-in-the-data-source-that-is-associated-with-a-replication-task)
-   [レプリケーション タスクに関連付けられているデータ ソースのスキーマの CREATE ステートメントを取得する](#get-the-create-statement-for-schemas-of-the-data-source-that-is-associated-with-a-replication-task)
-   [レプリケーション タスクに関連付けられているデータ ソースのスキーマの CREATE ステートメントを更新する](#update-the-create-statement-for-schemas-of-the-data-source-that-is-associated-with-a-replication-task)
-   [レプリケーション タスクに関連付けられているデータ ソースのスキーマを削除する](#delete-a-schema-of-the-data-source-that-is-associated-with-a-replication-task)

以下のセクションでは、API の特定の使用法について説明します。

## API エラー メッセージ テンプレート {#api-error-message-template}

API リクエストの送信後にエラーが発生した場合、次の形式のエラー メッセージが返されます。

```json
{
    "error_msg": "",
    "error_code": ""
}
```

上記の JSON 出力から、 `error_msg`はエラー メッセージを表し、 `error_code`は対応するエラー コードです。

## DMマスターノードの情報を取得する {#get-the-information-of-a-dm-master-node}

この API は同期インターフェースです。リクエストが成功すると、対応するノードの情報が返されます。

### リクエストURI {#request-uri}

`GET /api/v1/cluster/masters`

### 例 {#example}

{{< copyable "" >}}

```shell
curl -X 'GET' \
  'http://127.0.0.1:8261/api/v1/cluster/masters' \
  -H 'accept: application/json'
```

```json
{
  "total": 1,
  "data": [
    {
      "name": "master1",
      "alive": true,
      "leader": true,
      "addr": "127.0.0.1:8261"
    }
  ]
}
```

## DM マスター ノードを停止する {#stop-a-dm-master-node}

この API は同期インターフェースです。リクエストが成功した場合、返されるボディのステータス コードは 204 です。

### リクエストURI {#request-uri}

`DELETE /api/v1/cluster/masters/{master-name}`

### 例 {#example}

{{< copyable "" >}}

```shell
curl -X 'DELETE' \
  'http://127.0.0.1:8261/api/v1/cluster/masters/master1' \
  -H 'accept: */*'
```

## DM-worker ノードの情報を取得する {#get-the-information-of-a-dm-worker-node}

この API は同期インターフェースです。リクエストが成功すると、対応するノードの情報が返されます。

### リクエストURI {#request-uri}

`GET /api/v1/cluster/workers`

### 例 {#example}

{{< copyable "" >}}

```shell
curl -X 'GET' \
  'http://127.0.0.1:8261/api/v1/cluster/workers' \
  -H 'accept: application/json'
```

```json
{
  "total": 1,
  "data": [
    {
      "name": "worker1",
      "addr": "127.0.0.1:8261",
      "bound_stage": "bound",
      "bound_source_name": "mysql-01"
    }
  ]
}
```

## DM-worker ノードを停止する {#stop-a-dm-worker-node}

この API は同期インターフェースです。リクエストが成功した場合、返されるボディのステータス コードは 204 です。

### リクエストURI {#request-uri}

`DELETE /api/v1/cluster/workers/{worker-name}`

### 例 {#example}

{{< copyable "" >}}

```shell
curl -X 'DELETE' \
  'http://127.0.0.1:8261/api/v1/cluster/workers/worker1' \
  -H 'accept: */*'
```

## データ ソースを作成する {#create-a-data-source}

この API は同期インターフェースです。リクエストが成功すると、対応するデータ ソースの情報が返されます。

### リクエストURI {#request-uri}

`POST /api/v1/sources`

### 例 {#example}

{{< copyable "" >}}

```shell
curl -X 'POST' \
  'http://127.0.0.1:8261/api/v1/sources' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "source_name": "mysql-01",
  "host": "127.0.0.1",
  "port": 3306,
  "user": "root",
  "password": "123456",
  "enable": true,
  "enable_gtid": false,
  "security": {
    "ssl_ca_content": "",
    "ssl_cert_content": "",
    "ssl_key_content": "",
    "cert_allowed_cn": [
      "string"
    ]
  },
  "purge": {
    "interval": 3600,
    "expires": 0,
    "remain_space": 15
  }
}'
```

```json
{
  "source_name": "mysql-01",
  "host": "127.0.0.1",
  "port": 3306,
  "user": "root",
  "password": "123456",
  "enable": true,
  "enable_gtid": false,
  "security": {
    "ssl_ca_content": "",
    "ssl_cert_content": "",
    "ssl_key_content": "",
    "cert_allowed_cn": [
      "string"
    ]
  },
  "purge": {
    "interval": 3600,
    "expires": 0,
    "remain_space": 15
  },
  "status_list": [
    {
      "source_name": "mysql-replica-01",
      "worker_name": "worker-1",
      "relay_status": {
        "master_binlog": "(mysql-bin.000001, 1979)",
        "master_binlog_gtid": "e9a1fc22-ec08-11e9-b2ac-0242ac110003:1-7849",
        "relay_dir": "./sub_dir",
        "relay_binlog_gtid": "e9a1fc22-ec08-11e9-b2ac-0242ac110003:1-7849",
        "relay_catch_up_master": true,
        "stage": "Running"
      },
      "error_msg": "string"
    }
  ]
}
```

## データ ソースを取得する {#get-a-data-source}

この API は同期インターフェースです。リクエストが成功すると、対応するデータ ソースの情報が返されます。

### リクエストURI {#request-uri}

`GET /api/v1/sources/{source-name}`

### 例 {#example}

{{< copyable "" >}}

```shell
curl -X 'GET' \
  'http://127.0.0.1:8261/api/v1/sources/source-1?with_status=true' \
  -H 'accept: application/json'
```

```json
{
  "source_name": "mysql-01",
  "host": "127.0.0.1",
  "port": 3306,
  "user": "root",
  "password": "123456",
  "enable_gtid": false,
  "enable": false,
  "flavor": "mysql",
  "task_name_list": [
    "task1"
  ],
  "security": {
    "ssl_ca_content": "",
    "ssl_cert_content": "",
    "ssl_key_content": "",
    "cert_allowed_cn": [
      "string"
    ]
  },
  "purge": {
    "interval": 3600,
    "expires": 0,
    "remain_space": 15
  },
  "status_list": [
    {
      "source_name": "mysql-replica-01",
      "worker_name": "worker-1",
      "relay_status": {
        "master_binlog": "(mysql-bin.000001, 1979)",
        "master_binlog_gtid": "e9a1fc22-ec08-11e9-b2ac-0242ac110003:1-7849",
        "relay_dir": "./sub_dir",
        "relay_binlog_gtid": "e9a1fc22-ec08-11e9-b2ac-0242ac110003:1-7849",
        "relay_catch_up_master": true,
        "stage": "Running"
      },
      "error_msg": "string"
    }
  ],
  "relay_config": {
    "enable_relay": true,
    "relay_binlog_name": "mysql-bin.000002",
    "relay_binlog_gtid": "e9a1fc22-ec08-11e9-b2ac-0242ac110003:1-7849",
    "relay_dir": "./relay_log"
  }
}
```

## データ ソースを削除する {#delete-the-data-source}

この API は同期インターフェースです。リクエストが成功した場合、返されるボディのステータス コードは 204 です。

### リクエストURI {#request-uri}

`DELETE /api/v1/sources/{source-name}`

### 例 {#example}

{{< copyable "" >}}

```shell
curl -X 'DELETE' \
  'http://127.0.0.1:8261/api/v1/sources/mysql-01?force=true' \
  -H 'accept: application/json'
```

## データ ソースを更新する {#update-a-data-source}

この API は同期インターフェースです。リクエストが成功すると、対応するデータ ソースの情報が返されます。

> **ノート：**
>
> この API を使用してデータ ソース構成を更新する場合は、現在のデータ ソースで実行中のタスクがないことを確認してください。

### リクエストURI {#request-uri}

`PUT /api/v1/sources/{source-name}`

### 例 {#example}

{{< copyable "" >}}

```shell
curl -X 'PUT' \
  'http://127.0.0.1:8261/api/v1/sources/mysql-01' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "source": {
    "source_name": "mysql-01",
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "123456",
    "enable_gtid": false,
    "enable": false,
    "flavor": "mysql",
    "task_name_list": [
      "task1"
    ],
    "security": {
      "ssl_ca_content": "",
      "ssl_cert_content": "",
      "ssl_key_content": "",
      "cert_allowed_cn": [
        "string"
      ]
    },
    "purge": {
      "interval": 3600,
      "expires": 0,
      "remain_space": 15
    },
    "relay_config": {
      "enable_relay": true,
      "relay_binlog_name": "mysql-bin.000002",
      "relay_binlog_gtid": "e9a1fc22-ec08-11e9-b2ac-0242ac110003:1-7849",
      "relay_dir": "./relay_log"
    }
  }
}'
```

```json
{
  "source_name": "mysql-01",
  "host": "127.0.0.1",
  "port": 3306,
  "user": "root",
  "password": "123456",
  "enable": true,
  "enable_gtid": false,
  "security": {
    "ssl_ca_content": "",
    "ssl_cert_content": "",
    "ssl_key_content": "",
    "cert_allowed_cn": [
      "string"
    ]
  },
  "purge": {
    "interval": 3600,
    "expires": 0,
    "remain_space": 15
  }
}
```

## データ ソースを有効にする {#enable-a-data-source}

これは、要求が成功したときにデータ ソースを有効にし、このデータ ソースに依存するタスクのすべてのサブタスクをバッチで開始する同期インターフェイスです。

### リクエストURI {#request-uri}

`POST /api/v1/sources/{source-name}/enable`

### 例 {#example}

{{< copyable "" >}}

```shell
curl -X 'POST' \
  'http://127.0.0.1:8261/api/v1/sources/mysql-01/enable' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json'
```

## データ ソースを無効にする {#disable-a-data-source}

これは、要求が成功するとこのデータ ソースを非アクティブ化し、それに依存するタスクのすべてのサブタスクをバッチで停止する同期インターフェイスです。

### リクエストURI {#request-uri}

`POST /api/v1/sources/{source-name}/disable`

### 例 {#example}

{{< copyable "" >}}

```shell
curl -X 'POST' \
  'http://127.0.0.1:8261/api/v1/sources/mysql-01/disable' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json'
```

## データ ソース リストを取得する {#get-the-data-source-list}

この API は同期インターフェースです。リクエストが成功すると、データ ソース リストが返されます。

### リクエストURI {#request-uri}

`GET /api/v1/sources`

### 例 {#example}

{{< copyable "" >}}

```shell
curl -X 'GET' \
  'http://127.0.0.1:8261/api/v1/sources?with_status=true' \
  -H 'accept: application/json'
```

```json
{
  "data": [
    {
      "enable_gtid": false,
      "host": "127.0.0.1",
      "password": "******",
      "port": 3306,
      "purge": {
        "expires": 0,
        "interval": 3600,
        "remain_space": 15
      },
      "security": null,
      "source_name": "mysql-01",
      "user": "root"
    },
    {
      "enable_gtid": false,
      "host": "127.0.0.1",
      "password": "******",
      "port": 3307,
      "purge": {
        "expires": 0,
        "interval": 3600,
        "remain_space": 15
      },
      "security": null,
      "source_name": "mysql-02",
      "user": "root"
    }
  ],
  "total": 2
}
```

## データ ソースの情報を取得する {#get-the-information-of-a-data-source}

この API は同期インターフェースです。リクエストが成功すると、対応するノードの情報が返されます。

### リクエストURI {#request-uri}

`GET /api/v1/sources/{source-name}/status`

### 例 {#example}

{{< copyable "" >}}

```shell
curl -X 'GET' \
  'http://127.0.0.1:8261/api/v1/sources/mysql-replica-01/status' \
  -H 'accept: application/json'
```

```json
{
  "total": 1,
  "data": [
    {
      "source_name": "mysql-replica-01",
      "worker_name": "worker-1",
      "relay_status": {
        "master_binlog": "(mysql-bin.000001, 1979)",
        "master_binlog_gtid": "e9a1fc22-ec08-11e9-b2ac-0242ac110003:1-7849",
        "relay_dir": "./sub_dir",
        "relay_binlog_gtid": "e9a1fc22-ec08-11e9-b2ac-0242ac110003:1-7849",
        "relay_catch_up_master": true,
        "stage": "Running"
      },
      "error_msg": "string"
    }
  ]
}
```

## データ ソースのリレー ログ機能を開始する {#start-the-relay-log-feature-for-data-sources}

この API は非同期インターフェースです。リクエストが成功した場合、返された本文のステータス コードは 200 です。最新のステータスを知るには、 [データ ソースの情報を取得する](#get-the-information-of-a-data-source) .

### リクエストURI {#request-uri}

`POST /api/v1/sources/{source-name}/relay/enable`

### 例 {#example}

{{< copyable "" >}}

```shell
curl -X 'POST' \
  'http://127.0.0.1:8261/api/v1/sources/mysql-01/relay/enable' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "worker_name_list": [
    "worker-1"
  ],
  "relay_binlog_name": "mysql-bin.000002",
  "relay_binlog_gtid": "e9a1fc22-ec08-11e9-b2ac-0242ac110003:1-7849",
  "relay_dir": "./relay_log"
}'
```

## データ ソースのリレー ログ機能を停止する {#stop-the-relay-log-feature-for-data-sources}

この API は非同期インターフェースです。リクエストが成功した場合、返された本文のステータス コードは 200 です。最新のステータスを知るには、 [データ ソースの情報を取得する](#get-the-information-of-a-data-source) .

### リクエストURI {#request-uri}

`POST /api/v1/sources/{source-name}/relay/disable`

### 例 {#example}

{{< copyable "" >}}

```shell
curl -X 'POST' \
  'http://127.0.0.1:8261/api/v1/sources/mysql-01/relay/disable' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "worker_name_list": [
    "worker-1"
  ]
}'
```

## 不要になったリレー ログ ファイルをパージする {#purge-relay-log-files-that-are-no-longer-required}

この API は非同期インターフェースです。リクエストが成功した場合、返された本文のステータス コードは 200 です。最新のステータスを知るには、 [データ ソースの情報を取得する](#get-the-information-of-a-data-source) .

### リクエストURI {#request-uri}

`POST /api/v1/sources/{source-name}/relay/purge`

### 例 {#example}

{{< copyable "" >}}

```shell
curl -X 'POST' \
  'http://127.0.0.1:8261/api/v1/sources/mysql-01/relay/purge' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "relay_binlog_name": "mysql-bin.000002",
  "relay_dir": "string"
}'
```

## データ ソースと DM-worker 間のバインディングを変更する {#change-the-bindings-between-the-data-source-and-dm-workers}

この API は非同期インターフェースです。リクエストが成功した場合、返された本文のステータス コードは 200 です。最新のステータスを知るには、 [DM-worker ノードの情報を取得する](#get-the-information-of-a-dm-worker-node) .

### リクエストURI {#request-uri}

`POST /api/v1/sources/{source-name}/transfer`

### 例 {#example}

{{< copyable "" >}}

```shell
curl -X 'POST' \
  'http://127.0.0.1:8261/api/v1/sources/mysql-01/transfer' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "worker_name": "worker-1"
}'
```

## データ ソースのスキーマ名のリストを取得する {#get-the-list-of-schema-names-of-a-data-source}

この API は同期インターフェースです。リクエストが成功すると、対応するリストが返されます。

### リクエストURI {#request-uri}

`GET /api/v1/sources/{source-name}/schemas`

### 例 {#example}

{{< copyable "" >}}

```shell
curl -X 'GET' \
  'http://127.0.0.1:8261/api/v1/sources/source-1/schemas' \
  -H 'accept: application/json'
```

```json
[
  "db1"
]
```

## データ ソース内の指定されたスキーマのテーブル名のリストを取得します {#get-the-list-of-table-names-of-a-specified-schema-in-a-data-source}

この API は同期インターフェースです。リクエストが成功すると、対応するリストが返されます。

### リクエストURI {#request-uri}

`GET /api/v1/sources/{source-name}/schemas/{schema-name}`

### 例 {#example}

{{< copyable "" >}}

```shell
curl -X 'GET' \
  'http://127.0.0.1:8261/api/v1/sources/source-1/schemas/db1' \
  -H 'accept: application/json'
```

```json
[
  "table1"
]
```

## レプリケーション タスクを作成する {#create-a-replication-task}

この API は同期インターフェースです。リクエストが成功した場合、返されるボディのステータス コードは 200 です。リクエストが成功すると、対応するレプリケーション タスクの情報が返されます。

### リクエストURI {#request-uri}

`POST /api/v1/tasks`

### 例 {#example}

{{< copyable "" >}}

```shell
curl -X 'POST' \
  'http://127.0.0.1:8261/api/v1/tasks' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "task": {
    "name": "task-1",
    "task_mode": "all",
    "shard_mode": "pessimistic",
    "meta_schema": "dm-meta",
    "enhance_online_schema_change": true,
    "on_duplicate": "overwrite",
    "target_config": {
      "host": "127.0.0.1",
      "port": 3306,
      "user": "root",
      "password": "123456",
      "security": {
        "ssl_ca_content": "",
        "ssl_cert_content": "",
        "ssl_key_content": "",
        "cert_allowed_cn": [
          "string"
        ]
      }
    },
    "binlog_filter_rule": {
      "rule-1": {
        "ignore_event": [
          "all dml"
        ],
        "ignore_sql": [
          "^Drop"
        ]
      },
      "rule-2": {
        "ignore_event": [
          "all dml"
        ],
        "ignore_sql": [
          "^Drop"
        ]
      },
      "rule-3": {
        "ignore_event": [
          "all dml"
        ],
        "ignore_sql": [
          "^Drop"
        ]
      }
    },
    "table_migrate_rule": [
      {
        "source": {
          "source_name": "source-name",
          "schema": "db-*",
          "table": "tb-*"
        },
        "target": {
          "schema": "db1",
          "table": "tb1"
        },
        "binlog_filter_rule": [
          "rule-1",
          "rule-2",
          "rule-3",
        ]
      }
    ],
    "source_config": {
      "full_migrate_conf": {
        "export_threads": 4,
        "import_threads": 16,
        "data_dir": "./exported_data",
        "consistency": "auto"
      },
      "incr_migrate_conf": {
        "repl_threads": 16,
        "repl_batch": 100
      },
      "source_conf": [
        {
          "source_name": "mysql-replica-01",
          "binlog_name": "binlog.000001",
          "binlog_pos": 4,
          "binlog_gtid": "03fc0263-28c7-11e7-a653-6c0b84d59f30:1-7041423,05474d3c-28c7-11e7-8352-203db246dd3d:1-170"
        }
      ]
    }
  }
}'
```

```json
{
  "name": "task-1",
  "task_mode": "all",
  "shard_mode": "pessimistic",
  "meta_schema": "dm-meta",
  "enhance_online_schema_change": true,
  "on_duplicate": "overwrite",
  "target_config": {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "123456",
    "security": {
      "ssl_ca_content": "",
      "ssl_cert_content": "",
      "ssl_key_content": "",
      "cert_allowed_cn": [
        "string"
      ]
    }
  },
  "binlog_filter_rule": {
    "rule-1": {
      "ignore_event": [
        "all dml"
      ],
      "ignore_sql": [
        "^Drop"
      ]
    },
    "rule-2": {
      "ignore_event": [
        "all dml"
      ],
      "ignore_sql": [
        "^Drop"
      ]
    },
    "rule-3": {
      "ignore_event": [
        "all dml"
      ],
      "ignore_sql": [
        "^Drop"
      ]
    }
  },
  "table_migrate_rule": [
    {
      "source": {
        "source_name": "source-name",
        "schema": "db-*",
        "table": "tb-*"
      },
      "target": {
        "schema": "db1",
        "table": "tb1"
      },
      "binlog_filter_rule": [
        "rule-1",
        "rule-2",
        "rule-3",
      ]
    }
  ],
  "source_config": {
    "full_migrate_conf": {
      "export_threads": 4,
      "import_threads": 16,
      "data_dir": "./exported_data",
      "consistency": "auto"
    },
    "incr_migrate_conf": {
      "repl_threads": 16,
      "repl_batch": 100
    },
    "source_conf": [
      {
        "source_name": "mysql-replica-01",
        "binlog_name": "binlog.000001",
        "binlog_pos": 4,
        "binlog_gtid": "03fc0263-28c7-11e7-a653-6c0b84d59f30:1-7041423,05474d3c-28c7-11e7-8352-203db246dd3d:1-170"
      }
    ]
  }
}
```

## レプリケーション タスクを取得する {#get-a-replication-task}

この API は同期インターフェースです。リクエストが成功すると、対応するレプリケーション タスクの情報が返されます。

### リクエストURI {#request-uri}

`GET /api/v1/tasks/{task-name}?with_status=true`

### 例 {#example}

{{< copyable "" >}}

```shell
curl -X 'GET' \
  'http://127.0.0.1:8261/api/v1/tasks/task-1?with_status=true' \
  -H 'accept: application/json'
```

```json
{
  "name": "task-1",
  "task_mode": "all",
  "shard_mode": "pessimistic",
  "meta_schema": "dm-meta",
  "enhance_online_schema_change": true,
  "on_duplicate": "overwrite",
  "target_config": {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "123456",
    "security": {
      "ssl_ca_content": "",
      "ssl_cert_content": "",
      "ssl_key_content": "",
      "cert_allowed_cn": [
        "string"
      ]
    }
  },
  "binlog_filter_rule": {
    "rule-1": {
      "ignore_event": [
        "all dml"
      ],
      "ignore_sql": [
        "^Drop"
      ]
    },
    "rule-2": {
      "ignore_event": [
        "all dml"
      ],
      "ignore_sql": [
        "^Drop"
      ]
    },
    "rule-3": {
      "ignore_event": [
        "all dml"
      ],
      "ignore_sql": [
        "^Drop"
      ]
    }
  },
  "table_migrate_rule": [
    {
      "source": {
        "source_name": "source-name",
        "schema": "db-*",
        "table": "tb-*"
      },
      "target": {
        "schema": "db1",
        "table": "tb1"
      },
      "binlog_filter_rule": [
        "rule-1",
        "rule-2",
        "rule-3",
      ]
    }
  ],
  "source_config": {
    "full_migrate_conf": {
      "export_threads": 4,
      "import_threads": 16,
      "data_dir": "./exported_data",
      "consistency": "auto"
    },
    "incr_migrate_conf": {
      "repl_threads": 16,
      "repl_batch": 100
    },
    "source_conf": [
      {
        "source_name": "mysql-replica-01",
        "binlog_name": "binlog.000001",
        "binlog_pos": 4,
        "binlog_gtid": "03fc0263-28c7-11e7-a653-6c0b84d59f30:1-7041423,05474d3c-28c7-11e7-8352-203db246dd3d:1-170"
      }
    ]
  }
}
```

## レプリケーション タスクを削除する {#delete-a-replication-task}

このインターフェイスは同期インターフェイスであり、リクエストが成功すると返されるボディのステータス コードは 204 です。

### リクエストURI {#request-uri}

`DELETE /api/v1/tasks/{task-name}`

### 例 {#example}

{{< copyable "" >}}

```shell
curl -X 'DELETE' \
  'http://127.0.0.1:8261/api/v1/tasks/task-1' \
  -H 'accept: application/json'
```

## レプリケーション タスクを更新する {#update-a-replication-task}

このインターフェイスは同期インターフェイスであり、要求が成功するとタスクの情報が返されます。

> **ノート：**
>
> この API を使用してタスク構成を更新する場合は、タスクが停止され、増分同期が実行され、一部のフィールドのみが更新可能であることを確認してください。

### リクエストURI {#request-uri}

`PUT /api/v1/tasks/{task-name}`

### 例 {#example}

{{< copyable "" >}}

```shell
curl -X 'PUT' \
  'http://127.0.0.1:8261/api/v1/tasks/task-1' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "task": {
    "name": "task-1",
    "task_mode": "all",
    "shard_mode": "pessimistic",
    "meta_schema": "dm-meta",
    "enhance_online_schema_change": true,
    "on_duplicate": "overwrite",
    "target_config": {
      "host": "127.0.0.1",
      "port": 3306,
      "user": "root",
      "password": "123456",
      "security": {
        "ssl_ca_content": "",
        "ssl_cert_content": "",
        "ssl_key_content": "",
        "cert_allowed_cn": [
          "string"
        ]
      }
    },
    "binlog_filter_rule": {
      "rule-1": {
        "ignore_event": [
          "all dml"
        ],
        "ignore_sql": [
          "^Drop"
        ]
      },
      "rule-2": {
        "ignore_event": [
          "all dml"
        ],
        "ignore_sql": [
          "^Drop"
        ]
      },
      "rule-3": {
        "ignore_event": [
          "all dml"
        ],
        "ignore_sql": [
          "^Drop"
        ]
      }
    },
    "table_migrate_rule": [
      {
        "source": {
          "source_name": "source-name",
          "schema": "db-*",
          "table": "tb-*"
        },
        "target": {
          "schema": "db1",
          "table": "tb1"
        },
        "binlog_filter_rule": [
          "rule-1",
          "rule-2",
          "rule-3",
        ]
      }
    ],
    "source_config": {
      "full_migrate_conf": {
        "export_threads": 4,
        "import_threads": 16,
        "data_dir": "./exported_data",
        "consistency": "auto"
      },
      "incr_migrate_conf": {
        "repl_threads": 16,
        "repl_batch": 100
      },
      "source_conf": [
        {
          "source_name": "mysql-replica-01",
          "binlog_name": "binlog.000001",
          "binlog_pos": 4,
          "binlog_gtid": "03fc0263-28c7-11e7-a653-6c0b84d59f30:1-7041423,05474d3c-28c7-11e7-8352-203db246dd3d:1-170"
        }
      ]
    }
  }
}'
```

```json
{
  "name": "task-1",
  "task_mode": "all",
  "shard_mode": "pessimistic",
  "meta_schema": "dm-meta",
  "enhance_online_schema_change": true,
  "on_duplicate": "overwrite",
  "target_config": {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "123456",
    "security": {
      "ssl_ca_content": "",
      "ssl_cert_content": "",
      "ssl_key_content": "",
      "cert_allowed_cn": [
        "string"
      ]
    }
  },
  "binlog_filter_rule": {
    "rule-1": {
      "ignore_event": [
        "all dml"
      ],
      "ignore_sql": [
        "^Drop"
      ]
    },
    "rule-2": {
      "ignore_event": [
        "all dml"
      ],
      "ignore_sql": [
        "^Drop"
      ]
    },
    "rule-3": {
      "ignore_event": [
        "all dml"
      ],
      "ignore_sql": [
        "^Drop"
      ]
    }
  },
  "table_migrate_rule": [
    {
      "source": {
        "source_name": "source-name",
        "schema": "db-*",
        "table": "tb-*"
      },
      "target": {
        "schema": "db1",
        "table": "tb1"
      },
      "binlog_filter_rule": [
        "rule-1",
        "rule-2",
        "rule-3",
      ]
    }
  ],
  "source_config": {
    "full_migrate_conf": {
      "export_threads": 4,
      "import_threads": 16,
      "data_dir": "./exported_data",
      "consistency": "auto"
    },
    "incr_migrate_conf": {
      "repl_threads": 16,
      "repl_batch": 100
    },
    "source_conf": [
      {
        "source_name": "mysql-replica-01",
        "binlog_name": "binlog.000001",
        "binlog_pos": 4,
        "binlog_gtid": "03fc0263-28c7-11e7-a653-6c0b84d59f30:1-7041423,05474d3c-28c7-11e7-8352-203db246dd3d:1-170"
      }
    ]
  }
}
```

## レプリケーション タスクを開始する {#start-a-replication-task}

この API は非同期インターフェースです。リクエストが成功した場合、返される本文のステータス コードは 204 です。タスクの最新のステータスを知るには、 [複製タスクの情報を取得する](#get-the-information-of-a-replication-task)ことができます。

### リクエストURI {#request-uri}

`POST /api/v1/tasks/{task-name}/start`

### 例 {#example}

{{< copyable "" >}}

```shell
curl -X 'POST' \
  'http://127.0.0.1:8261/api/v1/tasks/task-1/start' \
  -H 'accept: */*'
```

## レプリケーション タスクを停止する {#stop-a-replication-task}

この API は非同期インターフェースです。リクエストが成功した場合、返される本文のステータス コードは 200 です。タスクの最新のステータスを知るには、 [複製タスクの情報を取得する](#get-the-information-of-a-replication-task)ことができます。

### リクエストURI {#request-uri}

`POST /api/v1/tasks/{task-name}/stop`

### 例 {#example}

{{< copyable "" >}}

```shell
curl -X 'POST' \
  'http://127.0.0.1:8261/api/v1/tasks/task-1/stop' \
  -H 'accept: */*'
```

## レプリケーション タスクの情報を取得する {#get-the-information-of-a-replication-task}

この API は同期インターフェースです。リクエストが成功すると、対応するノードの情報が返されます。

### リクエストURI {#request-uri}

`GET /api/v1/tasks/task-1/status`

### 例 {#example}

{{< copyable "" >}}

```shell
curl -X 'GET' \
  'http://127.0.0.1:8261/api/v1/tasks/task-1/status?stage=running' \
  -H 'accept: application/json'
```

```json
{
  "total": 1,
  "data": [
    {
      "name": "string",
      "source_name": "string",
      "worker_name": "string",
      "stage": "runing",
      "unit": "sync",
      "unresolved_ddl_lock_id": "string",
      "load_status": {
        "finished_bytes": 0,
        "total_bytes": 0,
        "progress": "string",
        "meta_binlog": "string",
        "meta_binlog_gtid": "string"
      },
      "sync_status": {
        "total_events": 0,
        "total_tps": 0,
        "recent_tps": 0,
        "master_binlog": "string",
        "master_binlog_gtid": "string",
        "syncer_binlog": "string",
        "syncer_binlog_gtid": "string",
        "blocking_ddls": [
          "string"
        ],
        "unresolved_groups": [
          {
            "target": "string",
            "ddl_list": [
              "string"
            ],
            "first_location": "string",
            "synced": [
              "string"
            ],
            "unsynced": [
              "string"
            ]
          }
        ],
        "synced": true,
        "binlog_type": "string",
        "seconds_behind_master": 0
      }
    }
  ]
}
```

## レプリケーション タスク リストを取得する {#get-the-replication-task-list}

この API は同期インターフェースであり、要求が成功すると、対応するタスクのリストが返されます。

### リクエストURI {#request-uri}

`GET /api/v1/tasks`

### 例 {#example}

{{< copyable "" >}}

```shell
curl -X 'GET' \
  'http://127.0.0.1:8261/api/v1/tasks' \
  -H 'accept: application/json'
```

```json
{
  "total": 2,
  "data": [
    {
      "name": "task-1",
      "task_mode": "all",
      "shard_mode": "pessimistic",
      "meta_schema": "dm-meta",
      "enhance_online_schema_change": true,
      "on_duplicate": "overwrite",
      "target_config": {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "password": "123456",
        "security": {
          "ssl_ca_content": "",
          "ssl_cert_content": "",
          "ssl_key_content": "",
          "cert_allowed_cn": [
            "string"
          ]
        }
      },
      "binlog_filter_rule": {
        "rule-1": {
          "ignore_event": [
            "all dml"
          ],
          "ignore_sql": [
            "^Drop"
          ]
        },
        "rule-2": {
          "ignore_event": [
            "all dml"
          ],
          "ignore_sql": [
            "^Drop"
          ]
        },
        "rule-3": {
          "ignore_event": [
            "all dml"
          ],
          "ignore_sql": [
            "^Drop"
          ]
        }
      },
      "table_migrate_rule": [
        {
          "source": {
            "source_name": "source-name",
            "schema": "db-*",
            "table": "tb-*"
          },
          "target": {
            "schema": "db1",
            "table": "tb1"
          },
          "binlog_filter_rule": [
            "rule-1",
            "rule-2",
            "rule-3",
          ]
        }
      ],
      "source_config": {
        "full_migrate_conf": {
          "export_threads": 4,
          "import_threads": 16,
          "data_dir": "./exported_data",
          "consistency": "auto"
        },
        "incr_migrate_conf": {
          "repl_threads": 16,
          "repl_batch": 100
        },
        "source_conf": [
          {
            "source_name": "mysql-replica-01",
            "binlog_name": "binlog.000001",
            "binlog_pos": 4,
            "binlog_gtid": "03fc0263-28c7-11e7-a653-6c0b84d59f30:1-7041423,05474d3c-28c7-11e7-8352-203db246dd3d:1-170"
          }
        ]
      }
    }
  ]
}
```

## レプリケーション タスクの移行ルールを取得する {#get-the-migration-rules-of-a-replication-task}

この API は同期インターフェースであり、リクエストが成功すると、このタスクの移行ルールのリストが返されます。

### リクエストURI {#request-uri}

`GET /api/v1/tasks/{task-name}/sources/{source-name}/migrate_targets`

### 例 {#example}

{{< copyable "" >}}

```shell
curl -X 'GET' \
  'http://127.0.0.1:8261/api/v1/tasks/task-1/sources/source-1/migrate_targets' \
  -H 'accept: application/json'
```

```json
{
  "total": 0,
  "data": [
    {
      "source_schema": "db1",
      "source_table": "tb1",
      "target_schema": "db1",
      "target_table": "tb1"
    }
  ]
}
```

## レプリケーション タスクに関連付けられているデータ ソースのスキーマ名のリストを取得します {#get-the-list-of-schema-names-of-the-data-source-that-is-associated-with-a-replication-task}

この API は同期インターフェースです。リクエストが成功すると、対応するリストが返されます。

### リクエストURI {#request-uri}

`GET /api/v1/tasks/{task-name}/sources/{source-name}/schemas`

### 例 {#example}

{{< copyable "" >}}

```shell
curl -X 'GET' \
  'http://127.0.0.1:8261/api/v1/tasks/task-1/sources/source-1/schemas' \
  -H 'accept: application/json'
```

```json
[
  "db1"
]
```

## レプリケーション タスクに関連付けられているデータ ソース内の指定されたスキーマのテーブル名のリストを取得します {#get-the-list-of-table-names-of-a-specified-schema-in-the-data-source-that-is-associated-with-a-replication-task}

この API は同期インターフェースです。リクエストが成功すると、対応するリストが返されます。

### リクエストURI {#request-uri}

`GET /api/v1/tasks/{task-name}/sources/{source-name}/schemas/{schema-name}`

### 例 {#example}

{{< copyable "" >}}

```shell
curl -X 'GET' \
  'http://127.0.0.1:8261/api/v1/tasks/task-1/sources/source-1/schemas/db1' \
  -H 'accept: application/json'
```

```json
[
  "table1"
]
```

## レプリケーション タスクに関連付けられているデータ ソースのスキーマの CREATE ステートメントを取得する {#get-the-create-statement-for-schemas-of-the-data-source-that-is-associated-with-a-replication-task}

この API は同期インターフェースです。リクエストが成功すると、対応する CREATE ステートメントが返されます。

### リクエストURI {#request-uri}

`GET /api/v1/tasks/{task-name}/sources/{source-name}/schemas/{schema-name}/{table-name}`

### 例 {#example}

{{< copyable "" >}}

```shell
curl -X 'GET' \
  'http://127.0.0.1:8261/api/v1/tasks/task-1/sources/source-1/schemas/db1/table1' \
  -H 'accept: application/json'
```

```json
{
  "schema_name": "db1",
  "table_name": "table1",
  "schema_create_sql": "CREATE TABLE `t1` (`id` int(11) NOT NULL AUTO_INCREMENT,PRIMARY KEY (`id`) /*T![clustered_index] CLUSTERED */) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin"
}
```

## レプリケーション タスクに関連付けられているデータ ソースのスキーマの CREATE ステートメントを更新する {#update-the-create-statement-for-schemas-of-the-data-source-that-is-associated-with-a-replication-task}

この API は同期インターフェースです。リクエストが成功した場合、返されるボディのステータス コードは 200 です。

### リクエストURI {#request-uri}

`POST /api/v1/tasks/{task-name}/sources/{source-name}/schemas/{schema-name}/{table-name}`

### 例 {#example}

{{< copyable "" >}}

```shell
curl -X 'PUT' \
  'http://127.0.0.1:8261/api/v1/tasks/task-1/sources/task-1/schemas/db1/table1' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "sql_content": "CREATE TABLE `t1` ( `c1` int(11) DEFAULT NULL, `c2` int(11) DEFAULT NULL, `c3` int(11) DEFAULT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;",
  "flush": true,
  "sync": true
}'
```

## レプリケーション タスクに関連付けられているデータ ソースのスキーマを削除する {#delete-a-schema-of-the-data-source-that-is-associated-with-a-replication-task}

この API は同期インターフェースです。リクエストが成功した場合、返されるボディのステータス コードは 200 です。

### リクエストURI {#request-uri}

`DELETE /api/v1/tasks/{task-name}/sources/{source-name}/schemas/{schema-name}/{table-name}`

### 例 {#example}

{{< copyable "" >}}

```shell
curl -X 'DELETE' \
  'http://127.0.0.1:8261/api/v1/tasks/task-1/sources/source-1/schemas/db1/table1' \
  -H 'accept: */*'
```
