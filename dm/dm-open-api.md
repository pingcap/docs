---
title: Maintain DM Clusters Using OpenAPI
summary: OpenAPI を使用した DM クラスターの管理についての記事です。DM は、DM クラスターのクエリと操作を簡単に行うための機能を提供します。OpenAPI を有効にするには、構成ファイルに設定を追加します。API を使用して、DM クラスター上で次のメンテナンス操作を実行できます。クラスターを管理するための API、データソースを管理するための API、レプリケーションタスクを管理するための APIがあります。API エラーメッセージテンプレートも提供されています。
---

# OpenAPI を使用した DM クラスターの管理 {#maintain-dm-clusters-using-openapi}

DM は、DM クラスターのクエリと操作を簡単に行うための OpenAPI 機能を提供します。これは[dmctl ツール](/dm/dmctl-introduction.md)の機能と同様です。

OpenAPI を有効にするには、次のいずれかの操作を実行します。

-   DM クラスターがバイナリを使用して直接デプロイされている場合は、次の構成を DM マスター構成ファイルに追加します。

    ```toml
    openapi = true
    ```

-   DM クラスターがTiUPを使用してデプロイされている場合は、次の構成をトポロジー ファイルに追加します。

    ```yaml
    server_configs:
      master:
        openapi: true
    ```

> **注記：**
>
> -   DM は、OpenAPI 3.0.0 標準を満たす[仕様書](https://github.com/pingcap/tiflow/blob/release-7.5/dm/openapi/spec/dm.yaml)を提供します。このドキュメントには、すべてのリクエスト パラメーターと戻り値が含まれています。ドキュメント yaml をコピーして、 [スワガーエディター](https://editor.swagger.io/)でプレビューできます。
>
> -   DM マスター ノードを展開した後、 `http://{master-addr}/api/v1/docs`にアクセスしてドキュメントをオンラインでプレビューできます。
>
> -   構成ファイルでサポートされている一部の機能は、OpenAPI ではサポートされていません。それらの機能は完全には一致していません。本番環境では、 [設定ファイル](/dm/dm-config-overview.md)を使用することをお勧めします。

API を使用して、DM クラスター上で次のメンテナンス操作を実行できます。

## クラスターを管理するための API {#apis-for-managing-clusters}

-   [DMマスターノードの情報を取得する](#get-the-information-of-a-dm-master-node)
-   [DMマスターノードを停止する](#stop-a-dm-master-node)
-   [DMワーカーノードの情報を取得する](#get-the-information-of-a-dm-worker-node)
-   [DM ワーカー ノードを停止する](#stop-a-dm-worker-node)

## データソースを管理するための API {#apis-for-managing-data-sources}

-   [データソースを作成する](#create-a-data-source)
-   [データソースを取得する](#get-a-data-source)
-   [データソースを削除する](#delete-the-data-source)
-   [データソースを更新する](#update-a-data-source)
-   [データソースを有効にする](#enable-a-data-source)
-   [データソースを無効にする](#disable-a-data-source)
-   [データソースの情報を取得する](#get-the-information-of-a-data-source)
-   [データソースリストを取得する](#get-the-data-source-list)
-   [データソースのリレーログ機能を開始する](#start-the-relay-log-feature-for-data-sources)
-   [データソースのリレーログ機能を停止する](#stop-the-relay-log-feature-for-data-sources)
-   [不要になったリレーログファイルをパージする](#purge-relay-log-files-that-are-no-longer-required)
-   [データソースとDMワーカー間のバインディングを変更する](#change-the-bindings-between-the-data-source-and-dm-workers)
-   [データソースのスキーマ名のリストを取得します。](#get-the-list-of-schema-names-of-a-data-source)
-   [データソース内の指定されたスキーマのテーブル名のリストを取得します。](#get-the-list-of-table-names-of-a-specified-schema-in-a-data-source)

## レプリケーションタスクを管理するための API {#apis-for-managing-replication-tasks}

-   [レプリケーションタスクを作成する](#create-a-replication-task)
-   [レプリケーションタスクを取得する](#get-a-replication-task)
-   [レプリケーションタスクを削除する](#delete-a-replication-task)
-   [レプリケーションタスクを更新する](#update-a-replication-task)
-   [レプリケーションタスクを開始する](#start-a-replication-task)
-   [レプリケーションタスクを停止する](#stop-a-replication-task)
-   [レプリケーションタスクの情報を取得する](#get-the-information-of-a-replication-task)
-   [レプリケーションタスクリストを取得する](#get-the-replication-task-list)
-   [レプリケーションタスクの移行ルールを取得する](#get-the-migration-rules-of-a-replication-task)
-   [レプリケーションタスクに関連付けられたデータソースのスキーマ名のリストを取得します。](#get-the-list-of-schema-names-of-the-data-source-that-is-associated-with-a-replication-task)
-   [レプリケーション タスクに関連付けられているデータ ソース内の指定されたスキーマのテーブル名のリストを取得します。](#get-the-list-of-table-names-of-a-specified-schema-in-the-data-source-that-is-associated-with-a-replication-task)
-   [レプリケーション タスクに関連付けられたデータ ソースのスキーマの CREATE ステートメントを取得します。](#get-the-create-statement-for-schemas-of-the-data-source-that-is-associated-with-a-replication-task)
-   [レプリケーション タスクに関連付けられたデータ ソースのスキーマの CREATE ステートメントを更新します。](#update-the-create-statement-for-schemas-of-the-data-source-that-is-associated-with-a-replication-task)
-   [レプリケーションタスクに関連付けられたデータソースのスキーマを削除します](#delete-a-schema-of-the-data-source-that-is-associated-with-a-replication-task)

次のセクションでは、API の具体的な使用法について説明します。

## APIエラーメッセージテンプレート {#api-error-message-template}

API リクエストの送信後にエラーが発生した場合、返されるエラー メッセージは次の形式になります。

```json
{
    "error_msg": "",
    "error_code": ""
}
```

上記の JSON 出力から、 `error_msg`エラー メッセージを説明し、 `error_code`は対応するエラー コードです。

## DMマスターノードの情報を取得する {#get-the-information-of-a-dm-master-node}

この API は同期インターフェイスです。リクエストが成功すると、該当ノードの情報が返されます。

### リクエストURI {#request-uri}

`GET /api/v1/cluster/masters`

### 例 {#example}

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

## DMマスターノードを停止する {#stop-a-dm-master-node}

この API は同期インターフェイスです。リクエストが成功した場合、返される本文のステータス コードは 204 です。

### リクエストURI {#request-uri}

`DELETE /api/v1/cluster/masters/{master-name}`

### 例 {#example}

```shell
curl -X 'DELETE' \
  'http://127.0.0.1:8261/api/v1/cluster/masters/master1' \
  -H 'accept: */*'
```

## DMワーカーノードの情報を取得する {#get-the-information-of-a-dm-worker-node}

この API は同期インターフェイスです。リクエストが成功すると、該当ノードの情報が返されます。

### リクエストURI {#request-uri}

`GET /api/v1/cluster/workers`

### 例 {#example}

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

## DM ワーカー ノードを停止する {#stop-a-dm-worker-node}

この API は同期インターフェイスです。リクエストが成功した場合、返される本文のステータス コードは 204 です。

### リクエストURI {#request-uri}

`DELETE /api/v1/cluster/workers/{worker-name}`

### 例 {#example}

```shell
curl -X 'DELETE' \
  'http://127.0.0.1:8261/api/v1/cluster/workers/worker1' \
  -H 'accept: */*'
```

## データソースを作成する {#create-a-data-source}

この API は同期インターフェイスです。リクエストが成功すると、対応するデータ ソースの情報が返されます。

### リクエストURI {#request-uri}

`POST /api/v1/sources`

### 例 {#example}

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

## データソースを取得する {#get-a-data-source}

この API は同期インターフェイスです。リクエストが成功すると、対応するデータ ソースの情報が返されます。

### リクエストURI {#request-uri}

`GET /api/v1/sources/{source-name}`

### 例 {#example}

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

## データソースを削除する {#delete-the-data-source}

この API は同期インターフェイスです。リクエストが成功した場合、返される本文のステータス コードは 204 です。

### リクエストURI {#request-uri}

`DELETE /api/v1/sources/{source-name}`

### 例 {#example}

```shell
curl -X 'DELETE' \
  'http://127.0.0.1:8261/api/v1/sources/mysql-01?force=true' \
  -H 'accept: application/json'
```

## データソースを更新する {#update-a-data-source}

この API は同期インターフェイスです。リクエストが成功すると、対応するデータ ソースの情報が返されます。

> **注記：**
>
> この API を使用してデータ ソース構成を更新する場合は、現在のデータ ソースで実行中のタスクがないことを確認してください。

### リクエストURI {#request-uri}

`PUT /api/v1/sources/{source-name}`

### 例 {#example}

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

## データソースを有効にする {#enable-a-data-source}

これは、リクエストが成功するとデータ ソースを有効にし、このデータ ソースに依存するタスクのすべてのサブタスクをバッチで開始する同期インターフェイスです。

### リクエストURI {#request-uri}

`POST /api/v1/sources/{source-name}/enable`

### 例 {#example}

```shell
curl -X 'POST' \
  'http://127.0.0.1:8261/api/v1/sources/mysql-01/enable' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json'
```

## データソースを無効にする {#disable-a-data-source}

これは、リクエストが成功するとこのデータ ソースを非アクティブ化し、それに依存するタスクのすべてのサブタスクをバッチで停止する同期インターフェイスです。

### リクエストURI {#request-uri}

`POST /api/v1/sources/{source-name}/disable`

### 例 {#example}

```shell
curl -X 'POST' \
  'http://127.0.0.1:8261/api/v1/sources/mysql-01/disable' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json'
```

## データソースリストを取得する {#get-the-data-source-list}

この API は同期インターフェイスです。リクエストが成功すると、データ ソース リストが返されます。

### リクエストURI {#request-uri}

`GET /api/v1/sources`

### 例 {#example}

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

## データソースの情報を取得する {#get-the-information-of-a-data-source}

この API は同期インターフェイスです。リクエストが成功すると、該当ノードの情報が返されます。

### リクエストURI {#request-uri}

`GET /api/v1/sources/{source-name}/status`

### 例 {#example}

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

## データソースのリレーログ機能を開始する {#start-the-relay-log-feature-for-data-sources}

この API は非同期インターフェイスです。リクエストが成功した場合、返される本文のステータス コードは 200 です。最新のステータスを確認するには、 [データソースの情報を取得する](#get-the-information-of-a-data-source)手順を実行します。

### リクエストURI {#request-uri}

`POST /api/v1/sources/{source-name}/relay/enable`

### 例 {#example}

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

## データソースのリレーログ機能を停止する {#stop-the-relay-log-feature-for-data-sources}

この API は非同期インターフェイスです。リクエストが成功した場合、返される本文のステータス コードは 200 です。最新のステータスを確認するには、 [データソースの情報を取得する](#get-the-information-of-a-data-source)手順を実行します。

### リクエストURI {#request-uri}

`POST /api/v1/sources/{source-name}/relay/disable`

### 例 {#example}

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

## 不要になったリレー ログ ファイルを削除する {#purge-relay-log-files-that-are-no-longer-required}

この API は非同期インターフェイスです。リクエストが成功した場合、返される本文のステータス コードは 200 です。最新のステータスを確認するには、 [データソースの情報を取得する](#get-the-information-of-a-data-source)手順を実行します。

### リクエストURI {#request-uri}

`POST /api/v1/sources/{source-name}/relay/purge`

### 例 {#example}

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

## データソースとDMワーカー間のバインディングを変更する {#change-the-bindings-between-the-data-source-and-dm-workers}

この API は非同期インターフェイスです。リクエストが成功した場合、返される本文のステータス コードは 200 です。最新のステータスを確認するには、 [DMワーカーノードの情報を取得する](#get-the-information-of-a-dm-worker-node)手順を実行します。

### リクエストURI {#request-uri}

`POST /api/v1/sources/{source-name}/transfer`

### 例 {#example}

```shell
curl -X 'POST' \
  'http://127.0.0.1:8261/api/v1/sources/mysql-01/transfer' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "worker_name": "worker-1"
}'
```

## データソースのスキーマ名のリストを取得します。 {#get-the-list-of-schema-names-of-a-data-source}

この API は同期インターフェイスです。リクエストが成功すると、対応するリストが返されます。

### リクエストURI {#request-uri}

`GET /api/v1/sources/{source-name}/schemas`

### 例 {#example}

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

## データソース内の指定されたスキーマのテーブル名のリストを取得します。 {#get-the-list-of-table-names-of-a-specified-schema-in-a-data-source}

この API は同期インターフェイスです。リクエストが成功すると、対応するリストが返されます。

### リクエストURI {#request-uri}

`GET /api/v1/sources/{source-name}/schemas/{schema-name}`

### 例 {#example}

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

## レプリケーションタスクを作成する {#create-a-replication-task}

この API は同期インターフェイスです。リクエストが成功した場合、返される本文のステータス コードは 200 です。リクエストが成功すると、対応するレプリケーション タスクの情報が返されます。

### リクエストURI {#request-uri}

`POST /api/v1/tasks`

### 例 {#example}

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
        "import_mode": "physical",
        "sorting_dir": "./sort_dir",
        "disk_quota": "80G",
        "checksum": "required",
        "analyze": "optional",
        "range_concurrency": 0,
        "compress-kv-pairs": "",
        "pd_addr": "",
        "on_duplicate_logical": "error",
        "on_duplicate_physical": "none"
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
      "import_mode": "physical",
      "sorting_dir": "./sort_dir",
      "disk_quota": "80G",
      "checksum": "required",
      "analyze": "optional",
      "range_concurrency": 0,
      "compress-kv-pairs": "",
      "pd_addr": "",
      "on_duplicate_logical": "error",
      "on_duplicate_physical": "none"
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

## レプリケーションタスクを取得する {#get-a-replication-task}

この API は同期インターフェイスです。リクエストが成功すると、対応するレプリケーション タスクの情報が返されます。

### リクエストURI {#request-uri}

`GET /api/v1/tasks/{task-name}?with_status=true`

### 例 {#example}

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
      "consistency": "auto",
      "import_mode": "physical",
      "sorting_dir": "./sort_dir",
      "disk_quota": "80G",
      "checksum": "required",
      "analyze": "optional",
      "range_concurrency": 0,
      "compress-kv-pairs": "",
      "pd_addr": "",
      "on_duplicate_logical": "error",
      "on_duplicate_physical": "none"
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

## レプリケーションタスクを削除する {#delete-a-replication-task}

このインターフェイスは同期インターフェイスであり、要求が成功すると返される本体のステータス コードは 204 になります。

### リクエストURI {#request-uri}

`DELETE /api/v1/tasks/{task-name}`

### 例 {#example}

```shell
curl -X 'DELETE' \
  'http://127.0.0.1:8261/api/v1/tasks/task-1' \
  -H 'accept: application/json'
```

## レプリケーションタスクを更新する {#update-a-replication-task}

このインターフェイスは同期インターフェイスであり、リクエストが成功するとタスクの情報が返されます。

> **注記：**
>
> この API を使用してタスク構成を更新する場合は、タスクが停止されて増分同期が実行されていること、および一部のフィールドのみが更新できることを確認してください。

### リクエストURI {#request-uri}

`PUT /api/v1/tasks/{task-name}`

### 例 {#example}

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
        "consistency": "auto",
        "import_mode": "physical",
        "sorting_dir": "./sort_dir",
        "disk_quota": "80G",
        "checksum": "required",
        "analyze": "optional",
        "range_concurrency": 0,
        "compress-kv-pairs": "",
        "pd_addr": "",
        "on_duplicate_logical": "error",
        "on_duplicate_physical": "none"
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
      "import_mode": "physical",
      "sorting_dir": "./sort_dir",
      "disk_quota": "80G",
      "checksum": "required",
      "analyze": "optional",
      "range_concurrency": 0,
      "compress-kv-pairs": "",
      "pd_addr": "",
      "on_duplicate_logical": "error",
      "on_duplicate_physical": "none"
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

## レプリケーションタスクを開始する {#start-a-replication-task}

この API は非同期インターフェイスです。リクエストが成功した場合、返される本文のステータス コードは 204 です。タスクの最新のステータスを確認するには、 [レプリケーションタスクの情報を取得する](#get-the-information-of-a-replication-task)を実行します。

### リクエストURI {#request-uri}

`POST /api/v1/tasks/{task-name}/start`

### 例 {#example}

```shell
curl -X 'POST' \
  'http://127.0.0.1:8261/api/v1/tasks/task-1/start' \
  -H 'accept: */*'
```

## レプリケーションタスクを停止する {#stop-a-replication-task}

この API は非同期インターフェイスです。リクエストが成功した場合、返される本文のステータス コードは 200 です。タスクの最新のステータスを確認するには、 [レプリケーションタスクの情報を取得する](#get-the-information-of-a-replication-task)を行うことができます。

### リクエストURI {#request-uri}

`POST /api/v1/tasks/{task-name}/stop`

### 例 {#example}

```shell
curl -X 'POST' \
  'http://127.0.0.1:8261/api/v1/tasks/task-1/stop' \
  -H 'accept: */*'
```

## レプリケーションタスクの情報を取得する {#get-the-information-of-a-replication-task}

この API は同期インターフェイスです。リクエストが成功すると、該当ノードの情報が返されます。

### リクエストURI {#request-uri}

`GET /api/v1/tasks/task-1/status`

### 例 {#example}

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

## レプリケーションタスクリストを取得する {#get-the-replication-task-list}

この API は同期インターフェイスであり、リクエストが成功すると、対応するタスクのリストが返されます。

### リクエストURI {#request-uri}

`GET /api/v1/tasks`

### 例 {#example}

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
          "consistency": "auto",
          "import_mode": "physical",
          "sorting_dir": "./sort_dir",
          "disk_quota": "80G",
          "checksum": "required",
          "analyze": "optional",
          "range_concurrency": 0,
          "compress-kv-pairs": "",
          "pd_addr": "",
          "on_duplicate_logical": "error",
          "on_duplicate_physical": "none"
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

## レプリケーションタスクの移行ルールを取得する {#get-the-migration-rules-of-a-replication-task}

この API は同期インターフェイスであり、リクエストが成功すると、このタスクの移行ルールのリストが返されます。

### リクエストURI {#request-uri}

`GET /api/v1/tasks/{task-name}/sources/{source-name}/migrate_targets`

### 例 {#example}

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

## レプリケーションタスクに関連付けられたデータソースのスキーマ名のリストを取得します。 {#get-the-list-of-schema-names-of-the-data-source-that-is-associated-with-a-replication-task}

この API は同期インターフェイスです。リクエストが成功すると、対応するリストが返されます。

### リクエストURI {#request-uri}

`GET /api/v1/tasks/{task-name}/sources/{source-name}/schemas`

### 例 {#example}

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

## レプリケーション タスクに関連付けられているデータ ソース内の指定されたスキーマのテーブル名のリストを取得します。 {#get-the-list-of-table-names-of-a-specified-schema-in-the-data-source-that-is-associated-with-a-replication-task}

この API は同期インターフェイスです。リクエストが成功すると、対応するリストが返されます。

### リクエストURI {#request-uri}

`GET /api/v1/tasks/{task-name}/sources/{source-name}/schemas/{schema-name}`

### 例 {#example}

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

## レプリケーション タスクに関連付けられたデータ ソースのスキーマの CREATE ステートメントを取得します。 {#get-the-create-statement-for-schemas-of-the-data-source-that-is-associated-with-a-replication-task}

この API は同期インターフェイスです。リクエストが成功すると、対応する CREATE ステートメントが返されます。

### リクエストURI {#request-uri}

`GET /api/v1/tasks/{task-name}/sources/{source-name}/schemas/{schema-name}/{table-name}`

### 例 {#example}

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

## レプリケーション タスクに関連付けられたデータ ソースのスキーマの CREATE ステートメントを更新します。 {#update-the-create-statement-for-schemas-of-the-data-source-that-is-associated-with-a-replication-task}

この API は同期インターフェイスです。リクエストが成功した場合、返される本文のステータス コードは 200 です。

### リクエストURI {#request-uri}

`POST /api/v1/tasks/{task-name}/sources/{source-name}/schemas/{schema-name}/{table-name}`

### 例 {#example}

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

## レプリケーションタスクに関連付けられたデータソースのスキーマを削除します {#delete-a-schema-of-the-data-source-that-is-associated-with-a-replication-task}

この API は同期インターフェイスです。リクエストが成功した場合、返される本文のステータス コードは 200 です。

### リクエストURI {#request-uri}

`DELETE /api/v1/tasks/{task-name}/sources/{source-name}/schemas/{schema-name}/{table-name}`

### 例 {#example}

```shell
curl -X 'DELETE' \
  'http://127.0.0.1:8261/api/v1/tasks/task-1/sources/source-1/schemas/db1/table1' \
  -H 'accept: */*'
```
