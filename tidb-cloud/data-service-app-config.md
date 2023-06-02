---
title: Data App Configuration Files
summary: This document describes the configuration files of Data Service in TiDB Cloud.
---

# Data App Configuration Files

This document describes the configuration files of Data Service in TiDB Cloud.

If you have connected your Data App to GitHub, you can find the configuration files of your Data App in your specified directory on GitHub. For more information, see [Deploy Automatically with GitHub](/tidb-cloud/data-service-manage-github-integration.md).

```
├── app
│   ├── data_sources
│   │   └── cluster.json
│   ├── dataapp_config.json
│   ├── http_endpoints
│   │   ├── config.json
│   │   └── sql
│   │       ├── <method>-<endpoint-name1>.sql
│   │       ├── <method>-<endpoint-name2>.sql
│   │       └── <method>-<endpoint-name3>.sql
```

## Data source configuration

The data source of a Data App is the linked clusters for this App. You can configure the data source in `cluster.json`.

```
├── app
│   ├── data_sources
│   │   └── cluster.json
```

The following is an example configuration of `cluster.json`.

```json
[
  {
    "cluster_id": <Cluster ID>
  },
  {
    "cluster_id": <Cluster ID>
  }
]
```

| Field   | Type    | Description  |
|---------|---------|--------------|
| `cluster_id` | Number | The ID of your TiDB cluster. You can get it from the URL of your TiDB cluster. For example, if your cluster URL is https://tidbcloud.com/console/clusters/1379111944646164111/overview, the cluster ID is `1379111944646164111`. |

## Data App configuration

The basic information of a Data App is contained in the `cluster.json` file.

```
├── app
│   ├── dataapp_config.json
```

The following is an example configuration of `cluster.json`.

```
{
  "app_id": "dataapi-kPjinlcu",
  "app_name": "caiqian-test213",
  "app_type": "dataapi"
}
```

| Field      | Type   | Description        |
|------------|--------|--------------------|
| `app_id`   | string | The Data App ID.   |
| `app_name` | string | The Data App name. |
| `app_type` | string | The Data App type. |

## HTTP endpoint configuration

For each Data App, you can configure its endpoints in `http_endpoints/config.json` and the SQL files of these endpoints in `http_endpoints/sql/<method>-<endpoint-name>.sql`.

```
├── app
│   ├── http_endpoints
│   │   ├── config.json
│   │   └── sql
│   │       ├── <method>-<endpoint-name1>.sql
│   │       ├── <method>-<endpoint-name2>.sql
│   │       └── <method>-<endpoint-name3>.sql
```

### Endpoint information configuration

In `http_endpoints/config.json`, you can configure the 

The following is an example configuration:

```json
[
  {
    "name": "<Endpoint name>",
    "description": "<Endpoint description",
    "method": "<HTTP method>",
    "endpoint": "<Endpoint path>",
    "data_source": {
      "cluster_id": <Endpoint ID>
    },
    "params": [],
    "settings": {
      "timeout": <Endpoint Timeout>,
      "row_limit": <Maximum rows>
    },
    "sql_file": "<SQL file directory>",
    "type": "sql_endpoint",
    "return_type": "json"
  },
  {
    "name": "/v1",
    "description": "",
    "method": "GET",
    "endpoint": "/v1",
    "data_source": {
      "cluster_id": 2939271
    },
    "params": [],
    "settings": {
      "timeout": 5000,
      "row_limit": 50
    },
    "sql_file": "sql/GET-v1.sql",
    "type": "sql_endpoint",
    "return_type": "json"
  },
]
```

| Field         | Type   | Description |
|---------------|--------|-------------|
| `name`        | string | The endpoint name.            |
| `description` | string | The endpoint description.            |
| `method`      | string | The HTTP method of the endpoint. You can use `GET` to query data or use `POST` to write data. |
| `endpoint`    | string | The unique path of the endpoint in the Data App. Only letters, numbers, underscores (`_`), and slashes (`/`) are allowed in the path, which must start with a slash (`/`). For example, `/my_endpoint/get_id`. The length of the path must be less than 64 characters.|
| `cluster_id`  | string | The ID of your TiDB cluster. You can get it from the URL of your TiDB cluster. For example, if your cluster URL is https://tidbcloud.com/console/clusters/1379111944646164111/overview, the cluster ID is `1379111944646164111`. |
| `params`      | string |             |
| `timeout`     | string | The timeout for the endpoint millisecond. Maximum value: `30000`. Minimum value: `1`. If not specified, the default value is `5000`. |
| `row_limit`   | string | The maximum number of rows that the endpoint returns. You can set it a value between `1` and `30000`. If not specified, the default value is `5000`.           |
| `sql_file`    | string |             |
| `type`        | string |             |
| `return_type` | string |             |

### Endpoint SQL configuration

`http_endpoints/sql/<method>-<endpoint-name1>.sql`

