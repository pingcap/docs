---
title: Maintain DM Clusters Using OpenAPI
summary: Learn about how to use OpenAPI interface to manage the cluster status and data replication.
---

# OpenAPIを使用してDMクラスターを管理する {#maintain-dm-clusters-using-openapi}

DMは、DMクラスタを簡単に照会および操作するためのOpenAPI機能を提供します。これは、 [dmctlツール](/dm/dmctl-introduction.md)の機能と同様です。この機能を有効にする必要がある場合は、DMマスター構成ファイルに次の構成を追加します。

```toml
openapi = true
```

> **ノート：**
>
> -   DMは、OpenAPI3.0.0標準を満たす[仕様書](https://github.com/pingcap/tiflow/blob/master/dm/openapi/spec/dm.yaml)を提供します。このドキュメントには、すべてのリクエストパラメータと戻り値が含まれています。ドキュメントyamlをコピーして、 [Swaggerエディター](https://editor.swagger.io/)でプレビューできます。
>
> -   DMマスターノードを展開した後、 `http://{master-addr}/api/v1/docs`にアクセスしてドキュメントをオンラインでプレビューできます。

APIを使用して、DMクラスタで次のメンテナンス操作を実行できます。

## クラスターを管理するためのAPI {#apis-for-managing-clusters}

-   [DMマスターノードの情報を取得する](#get-the-information-of-a-dm-master-node)
-   [DMマスターノードを停止します](#stop-a-dm-master-node)
-   [DMワーカーノードの情報を取得します](#get-the-information-of-a-dm-worker-node)
-   [DMワーカーノードを停止します](#stop-a-dm-worker-node)

## データソースを管理するためのAPI {#apis-for-managing-data-sources}

-   [データソースを作成する](#create-a-data-source)
-   [データソースリストを取得する](#get-the-data-source-list)
-   [データソースを削除する](#delete-the-data-source)
-   [データソースの情報を取得する](#get-the-information-of-a-data-source)
-   [データソースのリレーログ機能を開始します](#start-the-relay-log-feature-for-data-sources)
-   [データソースのリレーログ機能を停止します](#stop-the-relay-log-feature-for-data-sources)
-   [データソースのリレーログ機能を一時停止します](#pause-the-relay-log-feature-for-data-sources)
-   [データソースのリレーログ機能を再開します](#resume-the-relay-log-feature-for-data-sources)
-   [データソースとDMワーカー間のバインディングを変更します](#change-the-bindings-between-the-data-source-and-dm-workers)
-   [データソースのスキーマ名のリストを取得する](#get-the-list-of-schema-names-of-a-data-source)
-   [データソース内の指定されたスキーマのテーブル名のリストを取得します](#get-the-list-of-table-names-of-a-specified-schema-in-a-data-source)

## レプリケーションタスクを管理するためのAPI {#apis-for-managing-replication-tasks}

-   [レプリケーションタスクを作成する](#create-a-replication-task)
-   [レプリケーションタスクリストを取得する](#get-the-replication-task-list)
-   [レプリケーションタスクを停止します](#stop-a-replication-task)
-   [レプリケーションタスクの情報を取得します](#get-the-information-of-a-replication-task)
-   [レプリケーションタスクを一時停止します](#pause-a-replication-task)
-   [レプリケーションタスクを再開します](#resume-a-replication-task)
-   [レプリケーションタスクに関連付けられているデータソースのスキーマ名のリストを取得します](#get-the-list-of-schema-names-of-the-data-source-that-is-associated-with-a-replication-task)
-   [レプリケーションタスクに関連付けられているデータソース内の指定されたスキーマのテーブル名のリストを取得します](#get-the-list-of-table-names-of-a-specified-schema-in-the-data-source-that-is-associated-with-a-replication-task)
-   [レプリケーションタスクに関連付けられているデータソースのスキーマのCREATEステートメントを取得します](#get-the-create-statement-for-schemas-of-the-data-source-that-is-associated-with-a-replication-task)
-   [レプリケーションタスクに関連付けられているデータソースのスキーマのCREATEステートメントを更新します](#update-the-create-statement-for-schemas-of-the-data-source-that-is-associated-with-a-replication-task)
-   [レプリケーションタスクに関連付けられているデータソースのスキーマを削除します](#delete-a-schema-of-the-data-source-that-is-associated-with-a-replication-task)

次のセクションでは、APIの具体的な使用法について説明します。

## APIエラーメッセージテンプレート {#api-error-message-template}

APIリクエストを送信した後、エラーが発生した場合、返されるエラーメッセージは次の形式になります。

```json
{
    "error_msg": "",
    "error_code": ""
}
```

上記のJSON出力から、 `error_msg`はエラーメッセージを示し、 `error_code`は対応するエラーコードです。

## DMマスターノードの情報を取得する {#get-the-information-of-a-dm-master-node}

このAPIは同期インターフェースです。リクエストが成功すると、対応するノードの情報が返されます。

### URIをリクエストする {#request-uri}

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

## DMマスターノードを停止します {#stop-a-dm-master-node}

このAPIは同期インターフェースです。リクエストが成功した場合、返される本文のステータスコードは204です。

### URIをリクエストする {#request-uri}

`DELETE /api/v1/cluster/masters/{master-name}`

### 例 {#example}

{{< copyable "" >}}

```shell
curl -X 'DELETE' \
  'http://127.0.0.1:8261/api/v1/cluster/masters/master1' \
  -H 'accept: */*'
```

## DMワーカーノードの情報を取得します {#get-the-information-of-a-dm-worker-node}

このAPIは同期インターフェースです。リクエストが成功すると、対応するノードの情報が返されます。

### URIをリクエストする {#request-uri}

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

## DMワーカーノードを停止します {#stop-a-dm-worker-node}

このAPIは同期インターフェースです。リクエストが成功した場合、返される本文のステータスコードは204です。

### URIをリクエストする {#request-uri}

`DELETE /api/v1/cluster/workers/{worker-name}`

### 例 {#example}

{{< copyable "" >}}

```shell
curl -X 'DELETE' \
  'http://127.0.0.1:8261/api/v1/cluster/workers/worker1' \
  -H 'accept: */*'
```

## データソースを作成する {#create-a-data-source}

このAPIは同期インターフェースです。リクエストが成功すると、対応するデータソースの情報が返されます。

### URIをリクエストする {#request-uri}

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

## データソースリストを取得する {#get-the-data-source-list}

このAPIは同期インターフェースです。リクエストが成功すると、データソースリストが返されます。

### URIをリクエストする {#request-uri}

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

## データソースを削除する {#delete-the-data-source}

このAPIは同期インターフェースです。リクエストが成功した場合、返される本文のステータスコードは204です。

### URIをリクエストする {#request-uri}

`DELETE /api/v1/sources/{source-name}`

### 例 {#example}

{{< copyable "" >}}

```shell
curl -X 'DELETE' \
  'http://127.0.0.1:8261/api/v1/sources/mysql-01?force=true' \
  -H 'accept: application/json'
```

## データソースの情報を取得する {#get-the-information-of-a-data-source}

このAPIは同期インターフェースです。リクエストが成功すると、対応するノードの情報が返されます。

### URIをリクエストする {#request-uri}

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

## データソースのリレーログ機能を開始します {#start-the-relay-log-feature-for-data-sources}

このAPIは非同期インターフェースです。リクエストが成功した場合、返された本文のステータスコードは200です。最新のステータスを確認するには、 [データソースの情報を取得する](#get-the-information-of-a-data-source)を実行できます。

### URIをリクエストする {#request-uri}

`POST /api/v1/sources/{source-name}/start-relay`

### 例 {#example}

{{< copyable "" >}}

```shell
curl -X 'POST' \
  'http://127.0.0.1:8261/api/v1/sources/mysql-01/start-relay' \
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

## データソースのリレーログ機能を停止します {#stop-the-relay-log-feature-for-data-sources}

このAPIは非同期インターフェースです。リクエストが成功した場合、返された本文のステータスコードは200です。最新のステータスを確認するには、 [データソースの情報を取得する](#get-the-information-of-a-data-source)を実行できます。

### URIをリクエストする {#request-uri}

`POST /api/v1/sources/{source-name}/stop-relay`

### 例 {#example}

{{< copyable "" >}}

```shell
curl -X 'POST' \
  'http://127.0.0.1:8261/api/v1/sources/mysql-01/stop-relay' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "worker_name_list": [
    "worker-1"
  ]
}'
```

## データソースのリレーログ機能を一時停止します {#pause-the-relay-log-feature-for-data-sources}

このAPIは非同期インターフェースです。リクエストが成功した場合、返された本文のステータスコードは200です。最新のステータスを確認するには、 [データソースの情報を取得する](#get-the-information-of-a-data-source)を実行できます。

### URIをリクエストする {#request-uri}

`POST /api/v1/sources/{source-name}/pause-relay`

### 例 {#example}

{{< copyable "" >}}

```shell
curl -X 'POST' \
  'http://127.0.0.1:8261/api/v1/sources/mysql-01/pause-relay' \
  -H 'accept: */*'
```

## データソースのリレーログ機能を再開します {#resume-the-relay-log-feature-for-data-sources}

このAPIは非同期インターフェースです。リクエストが成功した場合、返された本文のステータスコードは200です。最新のステータスを確認するには、 [データソースの情報を取得する](#get-the-information-of-a-data-source)を実行できます。

### URIをリクエストする {#request-uri}

`POST /api/v1/sources/{source-name}/resume-relay`

### 例 {#example}

{{< copyable "" >}}

```shell
curl -X 'POST' \
  'http://127.0.0.1:8261/api/v1/sources/mysql-01/resume-relay' \
  -H 'accept: */*'
```

## データソースとDMワーカー間のバインディングを変更します {#change-the-bindings-between-the-data-source-and-dm-workers}

このAPIは非同期インターフェースです。リクエストが成功した場合、返された本文のステータスコードは200です。最新のステータスを確認するには、 [DMワーカーノードの情報を取得する](#get-the-information-of-a-dm-worker-node)を実行できます。

### URIをリクエストする {#request-uri}

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

## データソースのスキーマ名のリストを取得する {#get-the-list-of-schema-names-of-a-data-source}

このAPIは同期インターフェースです。リクエストが成功すると、対応するリストが返されます。

### URIをリクエストする {#request-uri}

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

## データソース内の指定されたスキーマのテーブル名のリストを取得します {#get-the-list-of-table-names-of-a-specified-schema-in-a-data-source}

このAPIは同期インターフェースです。リクエストが成功すると、対応するリストが返されます。

### URIをリクエストする {#request-uri}

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

## レプリケーションタスクを作成する {#create-a-replication-task}

このAPIは非同期インターフェースです。リクエストが成功した場合、返された本文のステータスコードは200です。最新のステータスを確認するには、 [レプリケーションタスクの情報を取得する](#get-the-information-of-a-replication-task)を実行できます。

### URIをリクエストする {#request-uri}

`POST /api/v1/tasks`

### 例 {#example}

{{< copyable "" >}}

```shell
curl -X 'POST' \
  'http://127.0.0.1:8261/api/v1/tasks' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "remove_meta": false,
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
  },
  "source_name_list": [
    "source-1"
  ]
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

## レプリケーションタスクリストを取得する {#get-the-replication-task-list}

このAPIは同期インターフェースです。要求が成功すると、対応するレプリケーションタスクの情報が返されます。

### URIをリクエストする {#request-uri}

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

## レプリケーションタスクを停止します {#stop-a-replication-task}

このAPIは非同期インターフェースです。リクエストが成功した場合、返された本文のステータスコードは204です。最新のステータスについて知るには、 [レプリケーションタスクの情報を取得する](#get-the-information-of-a-replication-task)を実行できます。

### URIをリクエストする {#request-uri}

`DELETE /api/v1/tasks/{task-name}`

### 例 {#example}

{{< copyable "" >}}

```shell
curl -X 'DELETE' \
  'http://127.0.0.1:8261/api/v1/tasks/task-1' \
  -H 'accept: */*'
```

## レプリケーションタスクの情報を取得します {#get-the-information-of-a-replication-task}

このAPIは同期インターフェースです。リクエストが成功すると、対応するノードの情報が返されます。

### URIをリクエストする {#request-uri}

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

## レプリケーションタスクを一時停止します {#pause-a-replication-task}

このAPIは非同期インターフェースです。リクエストが成功した場合、返された本文のステータスコードは200です。最新のステータスを確認するには、 [レプリケーションタスクの情報を取得する](#get-the-information-of-a-replication-task)を実行できます。

### URIをリクエストする {#request-uri}

`POST /api/v1/tasks/task-1/pause`

### 例 {#example}

{{< copyable "" >}}

```shell
curl -X 'POST' \
  'http://127.0.0.1:8261/api/v1/tasks/task-1/pause' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '[
  "source-1"
]'
```

## レプリケーションタスクを再開します {#resume-a-replication-task}

このAPIは非同期インターフェースです。リクエストが成功した場合、返された本文のステータスコードは200です。最新のステータスを確認するには、 [レプリケーションタスクの情報を取得する](#get-the-information-of-a-replication-task)を実行できます。

### URIをリクエストする {#request-uri}

`POST /api/v1/tasks/task-1/resume`

### 例 {#example}

{{< copyable "" >}}

```shell
curl -X 'POST' \
  'http://127.0.0.1:8261/api/v1/tasks/task-1/resume' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '[
  "source-1"
]'
```

## レプリケーションタスクに関連付けられているデータソースのスキーマ名のリストを取得します {#get-the-list-of-schema-names-of-the-data-source-that-is-associated-with-a-replication-task}

このAPIは同期インターフェースです。リクエストが成功すると、対応するリストが返されます。

### URIをリクエストする {#request-uri}

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

## レプリケーションタスクに関連付けられているデータソース内の指定されたスキーマのテーブル名のリストを取得します {#get-the-list-of-table-names-of-a-specified-schema-in-the-data-source-that-is-associated-with-a-replication-task}

このAPIは同期インターフェースです。リクエストが成功すると、対応するリストが返されます。

### URIをリクエストする {#request-uri}

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

## レプリケーションタスクに関連付けられているデータソースのスキーマのCREATEステートメントを取得します {#get-the-create-statement-for-schemas-of-the-data-source-that-is-associated-with-a-replication-task}

このAPIは同期インターフェースです。リクエストが成功すると、対応するCREATEステートメントが返されます。

### URIをリクエストする {#request-uri}

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

## レプリケーションタスクに関連付けられているデータソースのスキーマのCREATEステートメントを更新します {#update-the-create-statement-for-schemas-of-the-data-source-that-is-associated-with-a-replication-task}

このAPIは同期インターフェースです。リクエストが成功した場合、返される本文のステータスコードは200です。

### URIをリクエストする {#request-uri}

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

## レプリケーションタスクに関連付けられているデータソースのスキーマを削除します {#delete-a-schema-of-the-data-source-that-is-associated-with-a-replication-task}

このAPIは同期インターフェースです。リクエストが成功した場合、返される本文のステータスコードは200です。

### URIをリクエストする {#request-uri}

`DELETE /api/v1/tasks/{task-name}/sources/{source-name}/schemas/{schema-name}/{table-name}`

### 例 {#example}

{{< copyable "" >}}

```shell
curl -X 'DELETE' \
  'http://127.0.0.1:8261/api/v1/tasks/task-1/sources/source-1/schemas/db1/table1' \
  -H 'accept: */*'
```
