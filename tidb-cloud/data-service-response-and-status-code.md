---
title: Response and HTTP Status Codes of Data Service
summary: このドキュメントでは、TiDB Cloudのデータサービスの応答と HTTP ステータス コードについて説明します。
---

# データサービスの応答とHTTPステータスコード {#response-and-http-status-codes-of-data-service}

データサービスで定義されたAPIエンドポイントを呼び出すと、データサービスはHTTPレスポンスを返します。このレスポンスの構造とステータスコードの意味を理解することは[データサービス](/tidb-cloud/data-service-overview.md)データサービスのエンドポイントから返されるデータを解釈する上で不可欠です。

このドキュメントでは、TiDB Cloudのデータサービスの応答コードとステータスコードについて説明します。

## 応答 {#response}

データサービスは、JSON形式のボディを持つHTTPレスポンスを返します。

> **注記：**
>
> 複数のSQL文を含むエンドポイントを呼び出すと、データサービスは文を一つずつ実行しますが、HTTPレスポンスには最後の文の実行結果のみを返します。

レスポンスボディには以下のフィールドが含まれます。

-   `type` :*文字列*。このエンドポイントのタイプ。値は`"sql_endpoint"`または`"chat2data_endpoint"`のいずれかになります。エンドポイントによって返されるレスポンスのタイプが異なります。
-   `data` :*オブジェクト*。実行結果は、次の3つの部分から構成されます。

    -   `columns` :*配列*。返されるフィールドのスキーマ情報。

    -   `rows` :*配列*。返される結果は`key:value`形式です。

        エンドポイントで**バッチ操作**が有効になっており、エンドポイントの最後の SQL ステートメントが`INSERT`または`UPDATE`操作である場合は、次の点に注意してください。

        -   エンドポイントから返される結果には、各行の応答とステータスを示す`"message"`および`"success"`フィールドも含まれます。
        -   対象テーブルの主キー列が`auto_increment`に設定されている場合、エンドポイントから返される結果には、各行の`"auto_increment_id"`フィールドも含まれます。このフィールドの値は、 `INSERT`操作の自動インクリメント ID であり、 `null`などの他の操作の場合は`UPDATE`となります。

    -   `result` :*オブジェクト*。SQL ステートメントの実行関連情報。成功/失敗ステータス、実行時間、返された行数、ユーザー構成などが含まれます。

回答例は以下のとおりです。

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

HTTPステータスコードが`200`で、 `data.result.code`フィールドにも`200`が表示されている場合、SQLステートメントが正常に実行されたことを示しています。それ以外の場合は、 TiDB Cloudはエンドポイントで定義されたSQLステートメントの実行に失敗しています。詳細については`code`フィールドと`message`フィールドを確認してください。

回答例は以下のとおりです。

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

このステータスコードは、パラメータチェックが失敗したことを示しています。

回答例は以下のとおりです。

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

このステータスコードは、権限不足のため認証に失敗したことを示しています。

回答例は以下のとおりです。

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

このステータスコードは、指定されたエンドポイントが見つからなかったため、認証に失敗したことを示しています。

回答例は以下のとおりです。

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

このステータスコードは、リクエストで許可されていないメソッドが使用されたことを示しています。データサービスは`GET`と`POST`のみをサポートしていることに注意してください。

回答例は以下のとおりです。

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

このステータス コードは、リクエストがエンドポイントのタイムアウト期間を超えたことを示します。エンドポイントのタイムアウトを変更するには、 [プロパティを構成する](/tidb-cloud/data-service-manage-endpoint.md#configure-properties)を参照してください。

回答例は以下のとおりです。

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

このステータス コードは、リクエストが API キーのレート制限を超えていることを示します。さらに多くの割り当てが必要な場合は、サポート チームに[リクエストを送信する](https://tidb.support.pingcap.com/)ください。

回答例は以下のとおりです。

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

このステータスコードは、リクエスト中に内部エラーが発生したことを示しています。このエラーには様々な原因が考えられます。

考えられる原因の一つは、認証サーバーに接続できなかったために認証が失敗したことです。

回答例は以下のとおりです。

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

これは、 TiDB Cloud Starterインスタンスに接続できないことにも関連している可能性があります。トラブルシューティングについては`message`を参照してください。

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
