---
title: Data App Configuration Files
summary: This document describes the configuration files of Data Service in TiDB Cloud.
---

# Data App Configuration Files

This document describes the configuration files of Data App in TiDB Cloud.

If you have [connected your Data App to GitHub](/tidb-cloud/data-service-manage-github-integration.md), you can find the configuration files of your Data App in your specified directory on GitHub as follows:

```
├── <Your Data App directory>
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

The data source of a Data App comes from the linked TiDB clusters of this App. You can configure the data source in `cluster.json`.

```
├── <Your Data App directory>
│   ├── data_sources
│   │   └── cluster.json
```

For each Data App, you can link to one or multiple TiDB clusters. The following is an example configuration of `cluster.json`.

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

The description of each field is as follows:

| Field   | Type    | Description  |
|---------|---------|--------------|
| `cluster_id` | Integer | The ID of your TiDB cluster. You can get it from the URL of your TiDB cluster. For example, if your cluster URL is `https://tidbcloud.com/console/clusters/1379111944646164111/overview`, your cluster ID is `1379111944646164111`. |

## Data App configuration

The basic information of a Data App contains the App ID, name, and type. You can configure the basic information in the `cluster.json` file.

```
├── <Your Data App directory>
│   ├── dataapp_config.json
```

The following is an example configuration of `cluster.json`.

```json
{
  "app_id": "<Data App ID>",
  "app_name": "<Data App name>",
  "app_type": "dataapi"
}
```

The description of each field is as follows:

| Field      | Type   | Description        |
|------------|--------|--------------------|
| `app_id`   | string | The Data App ID. Do not change this field unless your `cluster.json` file is copied from another Data App and actual ID of your current Data App. |
| `app_name` | string | The Data App name. |
| `app_type` | string | The Data App type, which can only be `dataapi`. |

## HTTP endpoint configuration

In your Data App directory, you can find endpoint configurations in `http_endpoints/config.json` and the SQL files in `http_endpoints/sql/<method>-<endpoint-name>.sql`.

```
├── <Your Data App directory>
│   ├── http_endpoints
│   │   ├── config.json
│   │   └── sql
│   │       ├── <method>-<endpoint-name1>.sql
│   │       ├── <method>-<endpoint-name2>.sql
│   │       └── <method>-<endpoint-name3>.sql
```

### Endpoint information configuration

In `http_endpoints/config.json`, you can configure the

For each Data App, you can define one or multiple endpoints.

The following is an example endpoint configuration of a Data App. In this example, you can see that there are two endpoints for this Data.

```json
[
  {
    "name": "<Endpoint name>",
    "description": "<Endpoint description>",
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
    "name": "<Endpoint name>",
    "description": "<Endpoint description>",
    "method": "<HTTP method>",
    "endpoint": "<Endpoint path>",
    "data_source": {
      "cluster_id": <Endpoint ID>
    },
    "params": [
      {
        "name": "<Parameter name>",
        "type": "<Parameter type>",
        "required": <0 | 1>,
        "default": "<Parameter default value>"
      }
    ],
    "settings": {
      "timeout": <Endpoint Timeout>,
      "row_limit": <Maximum rows>
    },
    "sql_file": "<SQL file directory>",
    "type": "sql_endpoint",
    "return_type": "json"
  }
]
```

The description of each field is as follows:

| Field         | Type   | Description |
|---------------|--------|-------------|
| `name`        | String | The endpoint name.            |
| `description` | String | The endpoint description (optional).          |
| `method`      | String | The HTTP method of the endpoint. You can use `GET` to query data or use `POST` to insert data. |
| `endpoint`    | String | The unique path of the endpoint in the Data App. Only letters, numbers, underscores (`_`), and slashes (`/`) are allowed in the path, which must start with a slash (`/`). For example, `/my_endpoint/get_id`. The length of the path must be less than 64 characters.|
| `cluster_id`  | String | The ID of the target TiDB cluster for your endpoint. You can get it from the URL of your TiDB cluster. For example, if your cluster URL is `https://tidbcloud.com/console/clusters/1379111944646164111/overview`, the cluster ID is `1379111944646164111`. |
| `params` | Array | The parameters used in the endpoint. By defining parameters, you can dynamically replace the parameter value in your queries through the endpoint. In `params`, you can define one or multiple parameters. For each parameter, you need to define its `name`, `type`, `required`, and `default` fields. If your endpoint does not need any parameter. You can leave `params` empty such as `"params": []`. |
| `params.name` | string | The name of the parameter. The name can only include letters, digits, and underscores (`_`) and must start with a letter or an underscore (`_`).          |
| `params.type` | string | The data type of the parameter. Supported values are `string`, `number`, and `boolean`. When using a `string` type parameter, you do not need to add quotation marks (`'` or `"`). For example, `foo` is valid for the `STRING` type and is processed as `"foo"`, whereas `"foo"` is processed as `"\"foo\""`.|
| `params.required` | Integer | Specifies whether the parameter is required in the request. Supported values are `0` (not required) and `1` (required).  The default value is `0`.  |
| `params.default` | String | The default value of the parameter. Make sure that the value match the type of parameter. Otherwise, the endpoint returns an error. If you do not set a test value for a parameter in the TiDB Cloud console, the default value is used when testing the endpoint. |
| `timeout`     | Integer | The timeout for the endpoint in milliseconds, which is `5000` by default. You can set it to an integer from `1` to `30000`.  |
| `row_limit`   | Integer  | The maximum number of rows that the endpoint returns, which is `50` by default. You can set it to an integer from `1` to `2000`.          |
| `sql_file`    | string | The directory of the SQL file for the endpoint. For example, `"sql/GET-v1.sql"`. Make sure that the SQL file do exist in the directory. |
| `type`        | string | The type of the endpoint, which can only be `"sql_endpoint"`.          |
| `return_type` | string | The response format of the endpoint, which can only be `"json"`.             |

### SQL file configuration

You can modify SQL statements of your endpoints in the `http_endpoints/sql/` directory. For each endpoint, there should be a corresponding SQL file.

The name of a SQL file is in the `<method>-<endpoint-name>.sql` format, where `<method>` and `<endpoint-name>` must match the endpoint configuration in `http_endpoints/config.json`.

In the SQL files, you can write statements such as table join queries, complex queries, and aggregate functions. In the beginning of the SQL file, you need to first specify the database in the SQL statements. For example, `USE database_name;`.

To define a parameter of the endpoint, you can insert it as a variable placeholder like `${ID}` in the SQL statement. For example, `SELECT * FROM table_name WHERE id = ${ID}`. Make sure that the parameter name in the SQL file match the parameter name configured in `http_endpoints/config.json`.

> **Note:**
>
> - The parameter name is case-sensitive.
> - The parameter cannot be a table name or column name.

The following is an example SQL file.

```sql
/* Getting Started:
Enter "USE {database};" before entering your SQL statements.
Type "--your question" + Enter to try out AI-generated SQL queries in the TiDB Cloud console.
Declare a parameter like "Where id = ${arg}".
*/
USE sample_data;
SELECT repo_name FROM sample_data.github_events WHERE event_year=${event_year} LIMIT 9;

```
