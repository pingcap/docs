---
title: Response and HTTP Status Codes of Data Service
summary: このドキュメントでは、 TiDB Cloudのデータ サービスの応答コードと HTTP ステータス コードについて説明します。
---

# データサービスのレスポンスとHTTPステータスコード {#response-and-http-status-codes-of-data-service}

[データサービス](/tidb-cloud/data-service-overview.md)で定義されたAPIエンドポイントを呼び出すと、データサービスはHTTPレスポンスを返します。このレスポンスの構造とステータスコードの意味を理解することは、データサービスエンドポイントから返されるデータを解釈する上で不可欠です。

このドキュメントでは、 TiDB Cloudのデータ サービスの応答コードとステータス コードについて説明します。

## 応答 {#response}

データ サービスは、JSON 本文を含む HTTP 応答を返します。

> **注記：**
>
> 複数の SQL ステートメントを含むエンドポイントを呼び出すと、Data Service はステートメントを 1 つずつ実行しますが、HTTP 応答では最後のステートメントの実行結果のみを返します。

レスポンス本文には次のフィールドが含まれます。

-   `type` :*文字列*。このエンドポイントのタイプ。値は`"sql_endpoint"`または`"chat2data_endpoint"`になります。エンドポイントによって返されるレスポンスのタイプは異なります。
-   `data` :*オブジェクト*。実行結果には3つの部分が含まれます。

    -   `columns` :*配列*。返されるフィールドのスキーマ情報。

    -   `rows` :*配列*。4 `key:value`形式で結果が返されます。

        エンドポイントに対して**バッチ操作**が有効になっていて、エンドポイントの最後の SQL ステートメントが`INSERT`または`UPDATE`操作である場合は、次の点に注意してください。

        -   エンドポイントから返される結果には、応答とステータスを示す各行の`"message"`フィールドと`"success"`フィールドも含まれます。
        -   ターゲットテーブルの主キー列が`auto_increment`に設定されている場合、エンドポイントから返される結果には各行の`"auto_increment_id"`フィールドも含まれます。このフィールドの値は、 `INSERT`操作の場合は自動インクリメントID、 `UPDATE`などの他の操作の場合は`null`なります。

    -   `result` :*オブジェクト*。SQL文の実行に関する情報（成功/失敗ステータス、実行時間、返された行数、ユーザー設定など）。

応答の例は次のとおりです。

<SimpleTab>
<div label="SQL Endpoint">

```json
{
    "type": "sql_endpoint",
    "data": {
        "columns": [],
        "rows": [
            {
                "auto_increment_id": "270001",
                "index": "0",
                "message": "Row insert successfully",
                "success": "true"
            },
            {
                "auto_increment_id": "270002",
                "index": "1",
                "message": "Row insert successfully",
                "success": "true"
            }
        ],
        "result": {
            "code": 200,
            "message": "Query OK, 2 rows affected (8.359 sec)",
            "start_ms": 1689593360560,
            "end_ms": 1689593368919,
            "latency": "8.359s",
            "row_count": 2,
            "row_affect": 2,
            "limit": 500
        }
    }
}
```

</div>

<div label="Chat2Data Endpoint">

```json
{
  "type": "chat2data_endpoint",
  "data": {
    "columns": [
      {
        "col": "id",
        "data_type": "BIGINT",
        "nullable": false
      },
      {
        "col": "type",
        "data_type": "VARCHAR",
        "nullable": false
      }
    ],
    "rows": [
      {
        "id": "20008295419",
        "type": "CreateEvent"
      }
    ],
    "result": {
      "code": 200,
      "message": "Query OK!",
      "start_ms": 1678965476709,
      "end_ms": 1678965476839,
      "latency": "130ms",
      "row_count": 1,
      "row_affect": 0,
      "limit": 50
      "sql": "select id,type from sample_data.github_events limit 1;",
      "ai_latency": "30ms"
    }
  }
}
```

</div>
</SimpleTab>

## ステータスコード {#status-code}

### 200 {#200}

HTTPステータスコードが`200`で、かつ`data.result.code`フィールドにも`200`表示されている場合、SQL文が正常に実行されたことを示します。それ以外の場合、 TiDB Cloudはエンドポイントで定義されたSQL文の実行に失敗しています。詳細については、 `code`フィールドと`message`フィールドを確認してください。

応答の例は次のとおりです。

```json
{
    "type": "sql_endpoint",
    "data": {
        "columns": [],
        "rows": [],
        "result": {
            "code": 1146,
            "message": "table not found",
            "start_ms": "",
            "end_ms": "",
            "latency": "",
            "row_count": 0,
            "row_affect": 0,
            "limit": 0
        }
    }
}
```

### 400 {#400}

このステータス コードは、パラメータ チェックが失敗したことを示します。

応答の例は次のとおりです。

```json
{
    "type": "sql_endpoint",
    "data": {
        "columns": [],
        "rows": [],
        "result": {
            "code": 400,
            "message": "param check failed! {detailed error}",
            "start_ms": "",
            "end_ms": "",
            "latency": "",
            "row_count": 0,
            "row_affect": 0,
            "limit": 0
        }
    }
}
```

### 401 {#401}

このステータス コードは、権限不足により認証が失敗したことを示します。

応答の例は次のとおりです。

```json
{
    "type": "sql_endpoint",
    "data": {
        "columns": [],
        "rows": [],
        "result": {
            "code": 401,
            "message": "auth failed",
            "start_ms": "",
            "end_ms": "",
            "latency": "",
            "row_count": 0,
            "row_affect": 0,
            "limit": 0
        }
    }
}
```

### 404 {#404}

このステータス コードは、指定されたエンドポイントが見つからないため認証が失敗したことを示します。

応答の例は次のとおりです。

```json
{
    "type": "sql_endpoint",
    "data": {
        "columns": [],
        "rows": [],
        "result": {
            "code": 404,
            "message": "endpoint not found",
            "start_ms": "",
            "end_ms": "",
            "latency": "",
            "row_count": 0,
            "row_affect": 0,
            "limit": 0
        }
    }
}
```

### 405 {#405}

このステータスコードは、リクエストで許可されていないメソッドが使用されたことを示します。データサービスは`GET`と`POST`をサポートすることに注意してください。

応答の例は次のとおりです。

```json
{
    "type": "sql_endpoint",
    "data": {
        "columns": [],
        "rows": [],
        "result": {
            "code": 405,
            "message": "method not allowed",
            "start_ms": "",
            "end_ms": "",
            "latency": "",
            "row_count": 0,
            "row_affect": 0,
            "limit": 0
        }
    }
}
```

### 408 {#408}

このステータスコードは、リクエストがエンドポイントのタイムアウト期間を超えたことを示します。エンドポイントのタイムアウトを変更するには、 [プロパティを構成する](/tidb-cloud/data-service-manage-endpoint.md#configure-properties)を参照してください。

応答の例は次のとおりです。

```json
{
    "type": "sql_endpoint",
    "data": {
        "columns": [],
        "rows": [],
        "result": {
            "code": 408,
            "message": "request timeout.",
            "start_ms": "",
            "end_ms": "",
            "latency": "",
            "row_count": 0,
            "row_affect": 0,
            "limit": 0
        }
    }
}
```

### 429 {#429}

このステータスコードは、リクエストがAPIキーのレート制限を超えていることを示します。クォータを増やすには、サポートチームに[リクエストを送信する](https://tidb.support.pingcap.com/)問い合わせください。

応答の例は次のとおりです。

<SimpleTab>
<div label="SQL Endpoint">

```json
{
  "type": "",
  "data": {
    "columns": [],
    "rows": [],
    "result": {
      "code": 49900007,
      "message": "The request exceeded the limit of 100 times per apikey per minute. For more quota, please contact us: https://tidb.support.pingcap.com/",
      "start_ms": "",
      "end_ms": "",
      "latency": "",
      "row_count": 0,
      "row_affect": 0,
      "limit": 0
    }
  }
}
```

</div>

<div label="Chat2Data Endpoint">

```json
{
  "type": "chat2data_endpoint",
  "data": {
    "columns": [],
    "rows": [],
    "result": {
      "code": 429,
      "message": "The AI request exceeded the limit of 100 times per day. For more quota, please contact us: https://tidb.support.pingcap.com/",
      "start_ms": "",
      "end_ms": "",
      "latency": "",
      "row_count": 0,
      "row_affect": 0,
      "limit": 0
    }
  }
}
```

</div>
</SimpleTab>

### 500 {#500}

このステータスコードは、リクエストで内部エラーが発生したことを示します。このエラーにはさまざまな原因が考えられます。

原因としては、認証サーバーに接続できないために認証が失敗したことが考えられます。

応答の例は次のとおりです。

```json
{
    "type": "sql_endpoint",
    "data": {
        "columns": [],
        "rows": [],
        "result": {
            "code": 500,
            "message": "internal error! defaultPermissionHelper: rpc error: code = DeadlineExceeded desc = context deadline exceeded",
            "start_ms": "",
            "end_ms": "",
            "latency": "",
            "row_count": 0,
            "row_affect": 0,
            "limit": 0
        }
    }
}
```

これは、 TiDB Cloudクラスターに接続できないことにも関連している可能性があります。トラブルシューティングについては、 `message`を参照してください。

```json
{
    "type": "sql_endpoint",
    "data": {
        "columns": [],
        "rows": [],
        "result": {
            "code": 500,
            "message": "internal error! {detailed error}",
            "start_ms": "",
            "end_ms": "",
            "latency": "",
            "row_count": 0,
            "row_affect": 0,
            "limit": 0
        }
    }
}
```
