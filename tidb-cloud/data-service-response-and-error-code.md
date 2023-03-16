---
title: Response and Error Codes of Data Service
summary: This document describes the response and error codes of Data Service in TiDB Cloud.
---

# Response and Error Codes of Data Service

When you call an API endpoint defined in [Data Service](/tidb-cloud/data-service-overview.md), Data Service returns a HTTP response. Understanding the structure of an API response and the meaning of error codes is essential for interpreting data returned by a Data Service API.

This document describes the response and error codes of Data Service in TiDB Cloud.

## Response

Data Service returns a HTTP response with a JSON body. The response body contains the following fields:

- `type`: _string_. The type of this endpoint. The value might be `"sql_endpoint"` or `"chat2query_endpoint"`. Different endpoints return different types of responses.
- `data`: _object_. The execution results, which include three parts:

    - `columns`: _array_. Schema information for the returned fields.
    - `rows`: _array_. The returned results in key:value format.
    - `result`: _object_. The execution-related information of the SQL statement, including success/failure status, execution time, number of rows returned, and user configuration.

An example response is as follows:

<SimpleTab>
<div label="SQL Endpoint">

```json
{
    "type": "sql_endpoint",
    "data": {
        "columns": [
            {
                "col": "id",
                "data_type": "INT",
                "nullable": false
            },
            {
                "col": "name",
                "data_type": "VARCHAR",
                "nullable": true
            }
        ],
        "rows": [
            {
                "id": "1",
                "name": "a"
            }
        ],
        "result": {
            "code": 200,
            "message": "message=ok/message=${system error}/sql_error_message",
            "start_ms": "2023-03-01 16:53:08.277",
            "end_ms": "2023-03-01 16:53:08.713",
            "latency": "436ms",
            "row_count": 1,
            "row_affect": 0,
            "limit": 500,
            "query": "Query OK!"
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
                "data_type": "INT",
                "nullable": false
            },
            {
                "col": "name",
                "data_type": "VARCHAR",
                "nullable": true
            }
        ],
        "rows": [
            {
                "id": "1",
                "name": "a"
            }
        ],
        "result": {
            "code": 200,
            "message": "message=ok/message=${system error}/sql_error_message",
            "start_ms": "2023-03-01 16:53:08.277",
            "end_ms": "2023-03-01 16:53:08.713",
            "latency": "436ms",
            "row_count": 1,
            "row_affect": 0,
            "limit": 500,
            "query": "Query OK!",
            "ai_latency": "3000ms"
        }
    }
}
```

</div>
</SimpleTab>

## Error code

### 200

This error code indicates that TiDB Cloud fails to execute the SQL statement defined in your endpoint. You can check the `code` and `message` fields for detailed information.

An example response is as follows:

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
            "limit": 0,
            "query": ""
        }
    }
}
```

### 400

This error code indicates that the parameter check failed.

An example response is as follows:

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
            "limit": 0,
            "query": ""
        }
    }
}
```

### 401

This error code indicates that the authentication failed due to lack of permission.

An example response is as follows:

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
            "limit": 0,
            "query": ""
        }
    }
}
```

### 404

This error code indicates that the authentication failed due to the inability to find the specified endpoint.

An example response is as follows:

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
            "limit": 0,
            "query": ""
        }
    }
}
```

### 405

This error code indicates that the request used a method that is not allowed. Note that Data Service only supports `GET` and `POST`.

An example response is as follows:

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
            "limit": 0,
            "query": ""
        }
    }
}
```

### 408

This error code indicates that the request exceeds the timeout duration of the endpoint.

An example response is as follows:

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
            "limit": 0,
            "query": ""
        }
    }
}
```

### 500

This error code indicates that the request met an internal error. There might be various causes for this error.

One possible cause is that the authentication failed due to the inability to connect to the authentication server.

An example response is as follows:

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
            "limit": 0,
            "query": ""
        }
    }
}
```

This might also be related to inability to connect the TiDB Cloud cluster. You need to refer to the `message` for troubleshooting.

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
            "limit": 0,
            "query": ""
        }
    }
}
```
