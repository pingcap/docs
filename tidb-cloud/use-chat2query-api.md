---
title: 开始使用 Chat2Query API
summary: 了解如何通过 TiDB Cloud Chat2Query API 提供指令，利用 AI 生成并执行 SQL 语句。
---

# 开始使用 Chat2Query API

TiDB Cloud 提供了 Chat2Query API，这是一个 RESTful 接口，可以让你通过提供指令，利用 AI 生成并执行 SQL 语句。随后，API 会返回查询结果。

Chat2Query API 只能通过 HTTPS 访问，确保所有在网络上传输的数据都通过 TLS 加密。

> **Note:**
>
> Chat2Query API 仅适用于托管在 AWS 上的 [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter) 集群。如需在 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群上使用 Chat2Query API，请联系 [TiDB Cloud support](/tidb-cloud/tidb-cloud-support.md)。

## 开始之前

在调用 Chat2Query 端点之前，你需要创建一个 Chat2Query Data App，并为该 Data App 创建一个 API key。

### 创建 Chat2Query Data App

要为你的项目创建 Data App，请执行以下步骤：

1. 在项目的 [**Data Service**](https://tidbcloud.com/project/data-service) 页面左侧，点击 <MDSvgIcon name="icon-create-data-app" /> **Create DataApp**。此时会弹出数据应用创建对话框。

    > **Tip:**
    >
    > 如果你在集群的 **SQL Editor** 页面，也可以通过点击右上角的 **...**，选择 **Access Chat2Query via API**，再点击 **New Chat2Query Data App** 打开数据应用创建对话框。

2. 在对话框中，为你的 Data App 定义一个名称，选择所需的集合作为数据源，并将 **Data App** 类型选择为 **Chat2Query Data App**。你还可以为该应用填写描述（可选）。

3. 点击 **Create**。

   新创建的 Chat2Query Data App 会显示在左侧面板。在该 Data App 下，你可以看到 Chat2Query 端点的列表。

### 创建 API key

在调用端点之前，你需要为 Chat2Query Data App 创建一个 API key，端点会使用该 key 访问你在 TiDB Cloud 集群中的数据。

创建 API key 的步骤如下：

1. 在 [**Data Service**](https://tidbcloud.com/project/data-service) 左侧面板，点击你的 Chat2Query Data App，在右侧查看其详细信息。
2. 在 **Authentication** 区域，点击 **Create API Key**。
3. 在 **Create API Key** 对话框中，输入描述，并为你的 API key 选择以下角色之一：

   - `Chat2Query Admin`：允许该 API key 管理数据摘要、根据指令生成 SQL 语句并执行任意 SQL 语句。
   - `Chat2Query Data Summary Management Role`：仅允许该 API key 生成和更新数据摘要。

        > **Tip:**
        >
        > 对于 Chat2Query API，数据摘要是 AI 对你的数据库进行分析后的结果，包括数据库描述、表描述和列描述。通过为数据库生成数据摘要，可以在根据指令生成 SQL 语句时获得更准确的响应。

   - `Chat2Query SQL ReadOnly`：仅允许该 API key 根据指令生成 SQL 语句并执行 `SELECT` SQL 语句。
   - `Chat2Query SQL ReadWrite`：允许该 API key 根据指令生成 SQL 语句并执行任意 SQL 语句。

4. 默认情况下，API key 永不过期。如果你希望为该 key 设置过期时间，点击 **Expires in**，选择时间单位（`Minutes`、`Days` 或 `Months`），然后填写期望的时间数值。

5. 点击 **Next**。此时会显示公钥和私钥。

    请确保你已将私钥复制并保存在安全的位置。离开此页面后，将无法再次获取完整的私钥。

6. 点击 **Done**。

## 调用 Chat2Query 端点

> **Note:**
>
> 每个 Chat2Query Data App 每天有 100 次请求的速率限制。如果超过速率限制，API 会返回 `429` 错误。如需更多配额，可以 [提交请求](https://tidb.support.pingcap.com/) 联系我们的支持团队。

在每个 Chat2Query Data App 中，你可以找到以下端点：

- Chat2Query v3 端点：端点名称以 `/v3` 开头，如 `/v3/dataSummaries` 和 `/v3/chat2data`（推荐）
- Chat2Query v2 端点：端点名称以 `/v2` 开头，如 `/v2/dataSummaries` 和 `/v2/chat2data`
- Chat2Query v1 端点：`/v1/chat2data`（已弃用）

> **Tip:**
>
> 与 `/v1/chat2data` 相比，`/v3/chat2data` 和 `/v2/chat2data` 需要你先通过调用 `/v3/dataSummaries` 或 `/v2/dataSummaries` 对数据库进行分析。因此，`/v3/chat2data` 和 `/v2/chat2data` 返回的结果通常更为准确。

### 获取端点的代码示例

TiDB Cloud 提供了代码示例，帮助你快速调用 Chat2Query 端点。要获取 Chat2Query 端点的代码示例，请执行以下步骤：

1. 在 [**Data Service**](https://tidbcloud.com/project/data-service) 页面左侧，点击某个 Chat2Query 端点的名称。

    右侧会显示调用该端点所需的信息，如端点 URL、代码示例和请求方法。

2. 点击 **Show Code Example**。

3. 在弹出的对话框中，选择你想要调用端点的集群、数据库和认证方式，然后复制代码示例。

    > **Note:**
    >
    > 对于某些端点（如 `/v2/jobs/{job_id}`），你只需选择认证方式即可。

4. 要调用端点，你可以将示例粘贴到你的应用中，将示例中的参数（如 `${PUBLIC_KEY}` 和 `${PRIVATE_KEY}` 占位符）替换为你自己的 API key，然后运行即可。

### 调用 Chat2Query v3 或 v2 端点

TiDB Cloud Data Service 提供了以下 Chat2Query v3 和 v2 端点：

| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| POST   | `/v3/dataSummaries` | 该端点通过人工智能分析，为你的数据库 schema、表 schema 和列 schema 生成数据摘要。 |
| GET    | `/v3/dataSummaries` | 该端点获取你数据库的所有数据摘要。 |
| GET    | `/v3/dataSummaries/{data_summary_id}` | 该端点获取指定的数据摘要。 |
| PUT    | `/v3/dataSummaries/{data_summary_id}` | 该端点更新指定的数据摘要。 |
| PUT    | `/v3/dataSummaries/{data_summary_id}/tables/{table_name}` | 该端点更新指定数据摘要中某个表的描述。 |
| PUT    | `/v3/dataSummaries/{data_summary_id}/tables/{table_name}/columns` | 该端点更新指定数据摘要中某个表的列描述。 |
| POST   | `/v3/knowledgeBases` | 该端点创建新的知识库。关于知识库相关端点的用法，详见 [使用知识库](/tidb-cloud/use-chat2query-knowledge.md)。  |
| GET    | `/v3/knowledgeBases` | 该端点获取所有知识库。 |
| GET    | `/v3/knowledgeBases/{knowledge_base_id}` | 该端点获取指定的知识库。 |
| PUT    | `/v3/knowledgeBases/{knowledge_base_id}` | 该端点更新指定的知识库。 |
| POST   | `/v3/knowledgeBases/{knowledge_base_id}/data` | 该端点向指定知识库添加数据。 |
| GET    | `/v3/knowledgeBases/{knowledge_base_id}/data` | 该端点从指定知识库获取数据。 |
| PUT    | `/v3/knowledgeBases/{knowledge_base_id}/data/{knowledge_data_id}` | 该端点更新知识库中的指定数据。 |
| DEL    | `/v3/knowledgeBases/{knowledge_base_id}/data/{knowledge_data_id}` | 该端点从知识库中删除指定数据。 |
| POST   | `/v3/sessions` | 该端点创建新的会话。关于会话相关端点的用法，详见 [开启多轮 Chat2Query](/tidb-cloud/use-chat2query-sessions.md)。 |
| GET    | `/v3/sessions` | 该端点获取所有会话的列表。 |
| GET    | `/v3/sessions/{session_id}` | 该端点获取指定会话的详细信息。 |
| PUT    | `/v3/sessions/{session_id}` | 该端点更新指定会话。 |
| PUT    | `/v3/sessions/{session_id}/reset` | 该端点重置指定会话。 |
| POST   | `/v3/sessions/{session_id}/chat2data` | 该端点在指定会话中通过人工智能生成并执行 SQL 语句。详见 [通过会话开启多轮 Chat2Query](/tidb-cloud/use-chat2query-sessions.md)。 |
| POST   | `/v3/chat2data` | 该端点允许你通过提供数据摘要 ID 和指令，利用人工智能生成并执行 SQL 语句。 |
| POST   | `/v3/refineSql` | 该端点通过人工智能优化已有 SQL 查询。 |
| POST   | `/v3/suggestQuestions` | 该端点基于提供的数据摘要推荐问题。 |
| POST   | `/v2/dataSummaries` | 该端点通过人工智能为你的数据库 schema、表 schema 和列 schema 生成数据摘要。 |
| GET    | `/v2/dataSummaries` | 该端点获取所有数据摘要。 |
| POST   | `/v2/chat2data` | 该端点允许你通过提供数据摘要 ID 和指令，利用人工智能生成并执行 SQL 语句。 |
| GET    | `/v2/jobs/{job_id}` | 该端点允许你查询指定数据摘要生成任务的状态。 |

调用 `/v3/chat2data` 和 `/v2/chat2data` 的步骤相同。以下以 `/v3/chat2data` 为例，介绍如何调用。

#### 1. 通过调用 `/v3/dataSummaries` 生成数据摘要

在调用 `/v3/chat2data` 之前，先通过调用 `/v3/dataSummaries` 让 AI 分析数据库并生成数据摘要，这样 `/v3/chat2data` 在后续生成 SQL 时能获得更好的效果。

以下是调用 `/v3/dataSummaries` 分析 `sp500insight` 数据库并生成数据摘要的代码示例：

```bash
curl --digest --user ${PUBLIC_KEY}:${PRIVATE_KEY} --request POST 'https://<region>.data.tidbcloud.com/api/v1beta/app/chat2query-<ID>/endpoint/v3/dataSummaries'\
 --header 'content-type: application/json'\
 --data-raw '{
    "cluster_id": "10140100115280519574",
    "database": "sp500insight",
    "description": "Data summary for SP500 Insight",
    "reuse": false
}'
```

在上述示例中，请求体是一个 JSON 对象，包含以下属性：

- `cluster_id`：_string_。TiDB 集群的唯一标识符。
- `database`：_string_。数据库名称。
- `description`：_string_。数据摘要的描述。
- `reuse`：_boolean_。是否复用已有的数据摘要。如果设置为 `true`，API 会复用已有的数据摘要；如果设置为 `false`，API 会生成新的数据摘要。

示例响应如下：

```js
{
  "code": 200,
  "msg": "",
  "result": {
    "data_summary_id": 304823,
    "job_id": "fb99ef785da640ab87bf69afed60903d"
  }
}
```

#### 2. 通过调用 `/v2/jobs/{job_id}` 检查分析状态

`/v3/dataSummaries` API 是异步的。对于数据量较大的数据库，分析并返回完整数据摘要可能需要几分钟。

你可以通过调用 `/v2/jobs/{job_id}` 端点检查数据库的分析状态：

```bash
curl --digest --user ${PUBLIC_KEY}:${PRIVATE_KEY} --request GET 'https://<region>.data.dev.tidbcloud.com/api/v1beta/app/chat2query-<ID>`/endpoint/v2/jobs/{job_id}'\
 --header 'content-type: application/json'
```

示例响应如下：

```js
{
  "code": 200,
  "msg": "",
  "result": {
    "ended_at": 1699518950, // 任务完成时的 UNIX 时间戳
    "job_id": "fb99ef785da640ab87bf69afed60903d", // 当前任务的 ID
    "result": DataSummaryObject, // 指定数据库的 AI 探索信息
    "status": "done" // 当前任务的状态
  }
}
```

如果 `"status"` 为 `"done"`，则完整数据摘要已就绪，你现在可以通过调用 `/v3/chat2data` 为该数据库生成并执行 SQL 语句。否则，你需要等待并稍后再次检查分析状态，直到完成。

响应中的 `DataSummaryObject` 表示指定数据库的 AI 探索信息。其结构如下：

```js
{
    "cluster_id": "10140100115280519574", // 集群 ID
    "data_summary_id": 304823, // 数据摘要 ID
    "database": "sp500insight", // 数据库名称
    "default": false, // 该数据摘要是否为默认摘要
    "status": "done", // 数据摘要状态
    "description": {
        "system": "Data source for financial analysis and decision-making in stock market", // AI 生成的数据摘要描述
        "user": "Data summary for SP500 Insight" // 用户提供的数据摘要描述
    },
    "keywords": ["User_Stock_Selection", "Index_Composition"], // 数据摘要关键词
    "relationships": {
        "companies": {
            "referencing_table": "...", // 引用 `companies` 表的表
            "referencing_table_column": "...", // 引用 `companies` 表的列
            "referenced_table": "...", // `companies` 表引用的表
            "referenced_table_column": "..." // `companies` 表引用的列
        }
    }, // 表之间的关系
    "summary": "Financial data source for stock market analysis", // 数据摘要的总结
    "tables": { // 数据库中的表
      "companies": {
        "name": "companies" // 表名
        "description": "This table provides comprehensive...", // 表描述
        "columns": {
          "city": { // 表中的列
            "name": "city" // 列名
            "description": "The city where the company is headquartered.", // 列描述
          }
        },
      },
    }
}
```

#### 3. 通过调用 `/v3/chat2data` 生成并执行 SQL 语句

当数据库的数据摘要准备好后，你可以通过提供集群 ID、数据库名称和你的问题，调用 `/v3/chat2data` 生成并执行 SQL 语句。

例如：

```bash
curl --digest --user ${PUBLIC_KEY}:${PRIVATE_KEY} --request POST 'https://<region>.data.tidbcloud.com/api/v1beta/app/chat2query-<ID>/endpoint/v3/chat2data'\
 --header 'content-type: application/json'\
 --data-raw '{
    "cluster_id": "10140100115280519574",
    "database": "sp500insight",
    "question": "<Your question to generate data>",
    "sql_generate_mode": "direct"
}'
```

请求体是一个 JSON 对象，包含以下属性：

- `cluster_id`：_string_。TiDB 集群的唯一标识符。
- `database`：_string_。数据库名称。
- `data_summary_id`：_integer_。用于生成 SQL 的数据摘要 ID。仅当未提供 `cluster_id` 和 `database` 时生效。如果同时指定 `cluster_id` 和 `database`，API 会使用该数据库的默认数据摘要。
- `question`：_string_。用自然语言描述你想要查询的问题。
- `sql_generate_mode`：_string_。SQL 语句生成模式。可选值为 `direct` 或 `auto_breakdown`。如果设置为 `direct`，API 会直接根据你提供的 `question` 生成 SQL 语句；如果设置为 `auto_breakdown`，API 会将 `question` 拆解为多个任务，并为每个任务生成 SQL 语句。

示例响应如下：

```js
{
  "code": 200,
  "msg": "",
  "result": {
    "cluster_id": "10140100115280519574",
    "database": "sp500insight",
    "job_id": "20f7577088154d7889964f1a5b12cb26",
    "session_id": 304832
  }
}
```

如果你收到如下状态码为 `400` 的响应，说明需要等待数据摘要准备好。

```js
{
    "code": 400,
    "msg": "Data summary is not ready, please wait for a while and retry",
    "result": {}
}
```

`/v3/chat2data` API 是异步的。你可以通过调用 `/v2/jobs/{job_id}` 端点检查任务状态：

```bash
curl --digest --user ${PUBLIC_KEY}:${PRIVATE_KEY} --request GET 'https://<region>.data.dev.tidbcloud.com/api/v1beta/app/chat2query-<ID>/endpoint/v2/jobs/{job_id}'\
 --header 'content-type: application/json'
```

示例响应如下：

```js
{
  "code": 200,
  "msg": "",
  "result": {
    "ended_at": 1718785006, // 任务完成时的 UNIX 时间戳
    "job_id": "20f7577088154d7889964f1a5b12cb26",
    "reason": "", // 任务失败时的原因
    "result": {
      "assumptions": [],
      "chart_options": { // 结果生成的图表选项
        "chart_name": "Table",
        "option": {
          "columns": [
            "total_users"
          ]
        },
        "title": "Total Number of Users in the Database"
      },
      "clarified_task": "Count the total number of users in the database.", // 明确后的任务描述
      "data": { // SQL 语句返回的数据
        "columns": [
          {
            "col": "total_users"
          }
        ],
        "rows": [
          [
            "1"
          ]
        ]
      },
      "description": "",
      "sql": "SELECT COUNT(`user_id`) AS total_users FROM `users`;", // 生成的 SQL 语句
      "sql_error": null, // SQL 语句的错误信息
      "status": "done", // 任务状态
      "task_id": "0",
      "type": "data_retrieval" // 任务类型
    },
    "status": "done"
  }
}
```

### 调用 Chat2Data v1 端点（已弃用）

> **Note:**
>
> Chat2Data v1 端点已弃用。建议优先调用 Chat2Data v3 端点。

TiDB Cloud Data Service 提供以下 Chat2Query v1 端点：

|  Method | Endpoint| Description |
|  ----  | ----  |----  |
|  POST | `/v1/chat2data`  | 该端点允许你通过提供目标数据库名称和指令，利用人工智能生成并执行 SQL 语句。  |

你可以直接调用 `/v1/chat2data` 端点生成并执行 SQL 语句。与 `/v2/chat2data` 相比，`/v1/chat2data` 响应更快但性能较低。

TiDB Cloud 会生成代码示例，帮助你调用端点。获取示例并运行代码，详见 [获取端点的代码示例](#get-the-code-example-of-an-endpoint)。

调用 `/v1/chat2data` 时，你需要替换以下参数：

- 将 `${PUBLIC_KEY}` 和 `${PRIVATE_KEY}` 占位符替换为你的 API key。
- 将 `<your table name, optional>` 占位符替换为你要查询的表名。如果未指定表名，AI 会查询数据库中的所有表。
- 将 `<your instruction>` 占位符替换为你希望 AI 生成并执行 SQL 语句的指令。

> **Note:**
>
> - 每个 Chat2Query Data App 每天有 100 次请求的速率限制。如果超过速率限制，API 会返回 `429` 错误。如需更多配额，可以 [提交请求](https://tidb.support.pingcap.com/) 联系我们的支持团队。
> - 角色为 `Chat2Query Data Summary Management Role` 的 API Key 无法调用 Chat2Data v1 端点。

以下代码示例用于统计 `sp500insight.users` 表中的用户数量：

```bash
curl --digest --user ${PUBLIC_KEY}:${PRIVATE_KEY} --request POST 'https://<region>.data.dev.tidbcloud.com/api/v1beta/app/chat2query-<ID>/endpoint/chat2data'\
 --header 'content-type: application/json'\
 --data-raw '{
    "cluster_id": "10939961583884005252",
    "database": "sp500insight",
    "tables": ["users"],
    "instruction": "count the users"
}'
```

在上述示例中，请求体是一个 JSON 对象，包含以下属性：

- `cluster_id`：_string_。TiDB 集群的唯一标识符。
- `database`：_string_。数据库名称。
- `tables`：_array_。（可选）要查询的表名列表。
- `instruction`：_string_。用自然语言描述你想要查询的指令。

响应如下：

```json
{
  "type": "chat2data_endpoint",
  "data": {
    "columns": [
      {
        "col": "COUNT(`user_id`)",
        "data_type": "BIGINT",
        "nullable": false
      }
    ],
    "rows": [
      {
        "COUNT(`user_id`)": "1"
      }
    ],
    "result": {
      "code": 200,
      "message": "Query OK!",
      "start_ms": 1699529488292,
      "end_ms": 1699529491901,
      "latency": "3.609656403s",
      "row_count": 1,
      "row_affect": 0,
      "limit": 1000,
      "sql": "SELECT COUNT(`user_id`) FROM `users`;",
      "ai_latency": "3.054822491s"
    }
  }
}
```

如果 API 调用失败，你会收到非 `200` 的状态码。以下是 `500` 状态码的示例：

```json
{
  "type": "chat2data_endpoint",
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

## 了解更多

- [管理 API key](/tidb-cloud/data-service-api-key.md)
- [开启多轮 Chat2Query](/tidb-cloud/use-chat2query-sessions.md)
- [使用知识库](/tidb-cloud/use-chat2query-knowledge.md)
- [Data Service 的响应与状态码](/tidb-cloud/data-service-response-and-status-code.md)
