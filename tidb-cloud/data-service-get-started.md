---
title: 快速开始使用 Data Service
summary: 了解如何使用 TiDB Cloud Data Service 通过 HTTPS 请求访问你的数据。
---

# 快速开始使用 Data Service

Data Service（测试版）使你能够通过自定义 API 端点以 HTTPS 请求方式访问 TiDB Cloud 数据，并允许你无缝集成到任何兼容 HTTPS 的应用或服务中。

> **提示：**
>
> TiDB Cloud 为 TiDB 集群提供了 Chat2Query API。启用后，TiDB Cloud 会自动创建一个名为 **Chat2Query** 的系统 Data App，并在 Data Service 中创建一个 Chat2Data 端点。你可以调用该端点，通过提供指令让 AI 生成并 execute SQL statement。
>
> 详细信息，参见 [快速开始使用 Chat2Query API](/tidb-cloud/use-chat2query-api.md)。

本文介绍如何通过创建 Data App、开发、test、deploy 端点并调用端点，快速开始使用 TiDB Cloud Data Service（测试版）。Data App 是一组端点的集合，你可以用它来为特定应用 access 数据。

## 开始之前

在创建 Data App 之前，请确保你已经创建了一个托管在 AWS 上的 [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md) 集群。如果还没有，请按照 [创建 TiDB Cloud Starter 或 Essential 集群](/tidb-cloud/create-tidb-cluster-serverless.md) 的步骤进行创建。

> **注意：**
>
> Data Service 仅适用于托管在 AWS 上的 [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md) 集群。如需在 TiDB Cloud Dedicated 集群中使用 Data Service，请联系 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md)。

## 通过示例 Data App 快速入门

创建一个示例 Data App 是快速入门 Data Service 的最佳方式。如果你的项目还没有任何 Data App，可以按照 **Data Service** 页面上的引导创建一个示例 Data App，并用该 App 体验 Data Service 的功能。

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 的左侧导航栏，点击 <MDSvgIcon name="icon-left-data-service" /> **Data Service**。

2. 在 **Data Service** 页面，点击 **Create Sample Data App**。会弹出一个对话框。

3. 在对话框中，如有需要可修改 App 名称，选择你希望 Data App access 的集群，然后点击 **Create**。

    创建过程只需几秒钟。

    > **注意：**
    >
    > 如果当前项目下没有集群，可以在 **Link Data Sources** 下拉列表中点击 **Create New Cluster** 先创建一个集群。

4. 示例 Data App 自动创建完成后，你可以在左侧看到 App 名称和端点列表，在中间看到某个端点的 SQL statement，在右侧看到关于如何使用该示例 Data App 的说明。

5. 按照右侧说明选择一个端点，并使用 curl 命令调用该端点。

## 快速开始创建你自己的 Data App

你也可以创建自己的 Data App，然后按照以下步骤开发、test、deploy 并调用端点，快速开始使用 Data Service。

### 步骤 1. 创建 Data App

要创建 Data App，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 的左侧导航栏，点击 <MDSvgIcon name="icon-left-data-service" /> **Data Service**。

2. 在项目的 [**Data Service**](https://tidbcloud.com/project/data-service) 页面左侧，点击 <MDSvgIcon name="icon-create-data-app" /> **Create DataApp**。

    > **提示：**
    >
    > 如果这是你项目中的第一个 Data App，请在页面中间点击 **Create Data App**。

3. 在 **Create Data App** 对话框中，输入名称、描述，并选择你希望 Data App access 的集群。

    > **注意：**
    >
    > 默认情况下，Data App 类型为 **Standard Data App**。如果你想创建 **Chat2Query Data App**，请参考 [快速开始使用 Chat2Query API](/tidb-cloud/use-chat2query-api.md)，而不是本文档。

4. （可选）如需将 Data App 的端点自动 deploy 到你指定的 GitHub repository 和分支，请启用 **Connect to GitHub**，然后执行以下操作：

    1. 点击 **Install on GitHub**，并按照页面指引将 **TiDB Cloud Data Service** 作为应用安装到目标 repository。
    2. 返回 TiDB Cloud 控制台，点击 **Authorize**，授予对 GitHub 应用的 access 权限。
    3. 指定你希望保存 Data App configuration file 的 repository、分支和 directory。

    > **注意：**
    >
    > - directory 必须以斜杠（`/`）开头，例如 `/mydata`。如果你指定的 directory 在目标 repository 和分支下不存在，会自动创建。
    > - repository、分支和 directory 的组合唯一标识 configuration file 的路径，在所有 Data App 中必须唯一。如果你指定的路径已被其他 Data App 使用，需要重新指定路径。否则，在 TiDB Cloud 控制台为当前 Data App 配置的端点会覆盖你指定路径下的文件。

5. 点击 **Create Data App**。会显示 [**Data Service**](https://tidbcloud.com/project/data-service) 详情页。

6. 如果你已配置将 Data App 连接到 GitHub，请检查你指定的 GitHub directory。你会发现 [Data App configuration file](/tidb-cloud/data-service-app-config-files.md) 已由 `tidb-cloud-data-service` 提交到该 directory，说明 Data App 已成功连接到 GitHub。

    对于新建的 Data App，**Auto Sync & Deployment** 和 **Review Draft** 默认开启，你可以方便地在 TiDB Cloud 控制台和 GitHub 之间同步 Data App 变更，并在 deploy 前 review 变更。关于 GitHub 集成的更多信息，参见 [通过 GitHub 自动 deploy Data App 变更](/tidb-cloud/data-service-manage-github-connection.md)。

### 步骤 2. 开发端点

端点是你可以自定义以 execute SQL statement 的 Web API。

要创建新端点，定位到新建的 Data App，点击 App 名称右侧的 **+** **Create Endpoint**。

#### 配置属性

在右侧面板点击 **Properties** 标签页，为端点设置属性，例如：

- **Path**：用户 access 端点时使用的路径。request method 与 path 的组合在同一个 Data App 内必须唯一。

- **Endpoint URL**：（只读）URL 会根据对应集群所在 region、Data App 的 service URL 以及端点 path 自动生成。例如，如果端点 path 为 `/my_endpoint/get_id`，则端点 URL 为 `https://<region>.data.tidbcloud.com/api/v1beta/app/<App ID>/endpoint/my_endpoint/get_id`。

- **Request Method**：端点的 HTTP method。你可以用 `GET` 读数据，用 `POST` 创建或插入数据，用 `PUT` update 或修改数据，用 `DELETE` 删除数据。

关于端点属性的详细信息，参见 [配置属性](/tidb-cloud/data-service-manage-endpoint.md#configure-properties)。

#### 编写 SQL statement

你可以在 <Tooltip id="sql-editor">SQL Editor</Tooltip>（**Data Service** 页的中间面板）为端点自定义 SQL statement。

1. 选择集群。

    > **注意：**
    >
    > 只有已关联到 Data App 的集群会显示在下拉列表中。要管理已关联集群，参见 [管理已关联集群](/tidb-cloud/data-service-manage-data-app.md#manage-linked-data-sources)。

    在 SQL editor 上方，从下拉列表中选择你希望 execute SQL statement 的集群。然后，你可以在右侧面板的 **Schema** 标签页查看该集群的所有数据库。

2. 编写 SQL statement。

    在 query 或 update 数据前，需要先在 SQL statement 中指定数据库。例如：`USE database_name;`。

    在 SQL editor 中，你可以编写表关联查询、复杂查询、aggregate function 等 statement。你也可以直接输入 `--` 加上你的指令，让 AI 自动生成 SQL statement。

    > **注意：**
    >
    > 如需体验 TiDB Cloud 的 AI 能力，你需要允许 PingCAP 和 Amazon Bedrock 使用你的代码片段进行研究和服务改进。详细信息，参见 [启用或禁用 AI 生成 SQL 查询](/tidb-cloud/explore-data-with-chat2query.md#enable-or-disable-ai-to-generate-sql-queries)。

    如需定义 parameter，可以在 SQL statement 中以 `${ID}` 形式插入 variable 占位符。例如：`SELECT * FROM table_name WHERE id = ${ID}`。然后，你可以点击右侧面板的 **Params** 标签页，修改 parameter 定义和 test 值。

    > **注意：**
    >
    > - parameter 名称大小写敏感。
    > - parameter 不能用作表名或列名。

    - 在 **Definition** 区域，你可以指定 parameter 是否为必填、数据类型和默认值。
    - 在 **Test Values** 区域，你可以为 parameter 设置 test 值。test 值用于运行 SQL statement 或 test 端点时。如果未设置 test 值，则使用默认值。
    - 详细信息，参见 [配置参数](/tidb-cloud/data-service-manage-endpoint.md#configure-parameters)。

3. 运行 SQL statement。

    如果 SQL statement 中包含 parameter，请确保你已在右侧 **Params** 标签页为 parameter 设置了 test 值或默认值，否则会 return 错误。

    <SimpleTab>
    <div label="macOS">

    对于 macOS：

    - 如果 editor 中只有一条 statement，按 **⌘ + Enter** 或点击 <svg width="1rem" height="1rem" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.70001 20.7756C6.01949 20.3926 6.00029 19.5259 6.00034 19.0422L6.00034 12.1205L6 5.33028C6 4.75247 6.00052 3.92317 6.38613 3.44138C6.83044 2.88625 7.62614 2.98501 7.95335 3.05489C8.05144 3.07584 8.14194 3.12086 8.22438 3.17798L19.2865 10.8426C19.2955 10.8489 19.304 10.8549 19.3126 10.8617C19.4069 10.9362 20 11.4314 20 12.1205C20 12.7913 19.438 13.2784 19.3212 13.3725C19.307 13.3839 19.2983 13.3902 19.2831 13.4002C18.8096 13.7133 8.57995 20.4771 8.10002 20.7756C7.60871 21.0812 7.22013 21.0683 6.70001 20.7756Z" fill="currentColor"></path></svg>**Run** 即可运行。

    - 如果 editor 中有多条 statement，要顺序运行其中一条或多条，将光标放在目标 statement 上或用光标选中目标 statement 的行，然后按 **⌘ + Enter** 或点击 **Run**。

    - 要顺序运行 editor 中所有 statement，按 **⇧ + ⌘ + Enter**，或用光标选中所有 statement 的行后点击 **Run**。

    </div>

    <div label="Windows/Linux">

    对于 Windows 或 Linux：

    - 如果 editor 中只有一条 statement，按 **Ctrl + Enter** 或点击 <svg width="1rem" height="1rem" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.70001 20.7756C6.01949 20.3926 6.00029 19.5259 6.00034 19.0422L6.00034 12.1205L6 5.33028C6 4.75247 6.00052 3.92317 6.38613 3.44138C6.83044 2.88625 7.62614 2.98501 7.95335 3.05489C8.05144 3.07584 8.14194 3.12086 8.22438 3.17798L19.2865 10.8426C19.2955 10.8489 19.304 10.8549 19.3126 10.8617C19.4069 10.9362 20 11.4314 20 12.1205C20 12.7913 19.438 13.2784 19.3212 13.3725C19.307 13.3839 19.2983 13.3902 19.2831 13.4002C18.8096 13.7133 8.57995 20.4771 8.10002 20.7756C7.60871 21.0812 7.22013 21.0683 6.70001 20.7756Z" fill="currentColor"></path></svg>**Run** 即可运行。

    - 如果 editor 中有多条 statement，要顺序运行其中一条或多条，将光标放在目标 statement 上或用光标选中目标 statement 的行，然后按 **Ctrl + Enter** 或点击 **Run**。

    - 要顺序运行 editor 中所有 statement，按 **Shift + Ctrl + Enter**，或用光标选中所有 statement 的行后点击 **Run**。

    </div>
    </SimpleTab>

    运行后，你可以在页面底部的 **Result** 标签页立即看到 query 结果。

### 步骤 3. test 端点（可选）

配置端点后，你可以先 test 端点，verify 是否符合预期，再进行 deploy。

要 test 端点，点击右上角的 **Test**，或按 **F5**。

随后，你可以在页面底部的 **HTTP Response** 标签页看到 response。关于 response 的详细信息，参见 [端点的响应](/tidb-cloud/data-service-manage-endpoint.md#response)。

### 步骤 4. deploy 端点

要 deploy 端点，请执行以下步骤：

1. 在端点详情页，点击右上角的 **Deploy**。

2. 点击 **Deploy** 确认 deploy。如果端点 deploy 成功，会提示 **Endpoint has been deployed**。

    如需查看 deploy 历史，可以点击左侧 Data App 名称，再点击右侧的 **Deployments** 标签页。

### 步骤 5. 调用端点

你可以通过发送 HTTPS request 调用端点。在调用端点前，需要先为 Data App 创建 API key。

#### 1. 创建 API key

1. 在 [**Data Service**](https://tidbcloud.com/project/data-service) 页面左侧，点击你的 Data App 名称查看详情。
2. 在 **Authentication** 区域，点击 **Create API Key**。
3. 在 **Create API Key** 对话框中，执行以下操作：

    1. （可选）为 API key 输入描述。
    2. 选择 API key 的角色。

        角色用于控制 API key 是否可以对 Data App 关联的集群进行 read 或写操作。你可以选择 `ReadOnly` 或 `ReadAndWrite` 角色：

        - `ReadOnly`：只允许 API key read 数据，如 `SELECT`、`SHOW`、`USE`、`DESC` 和 `EXPLAIN` statement。
        - `ReadAndWrite`：允许 API key read 和写数据。你可以用该 API key execute 所有 SQL statement，如 DML 和 DDL statement。

    3. （可选）为 API key 设置期望的速率限制。

4. 点击 **Next**。会显示 public key 和 private key。

    请确保你已将 private key 复制并安全保存。离开此页面后，将无法再次获取完整的 private key。

5. 点击 **Done**。

关于 API key 的详细信息，参见 [Data Service 中的 API Key](/tidb-cloud/data-service-api-key.md)。

#### 2. 获取代码示例

TiDB Cloud 会生成代码示例，帮助你调用端点。要获取代码示例，请执行以下步骤：

1. 在 [**Data Service**](https://tidbcloud.com/project/data-service) 页面左侧，点击你的端点名称，然后点击右上角的 **...** > **Code Example**。会弹出 **Code Example** 对话框。

2. 在对话框中，选择你希望用于调用端点的集群和数据库，然后复制代码示例。

    curl 代码示例如下：

    <SimpleTab>
    <div label="Test Environment">

    调用端点的 draft 版本时，需要添加 `endpoint-type: draft` 头：

    ```bash
    curl --digest --user '<Public Key>:<Private Key>' \
      --request GET 'https://<region>.data.tidbcloud.com/api/v1beta/app/<App ID>/endpoint/<Endpoint Path>' \
      --header 'endpoint-type: draft'
    ```

    </div>

    <div label="Online Environment">

    你必须先 deploy 端点，才能查看线上环境下的代码示例。

    调用端点当前线上版本时，使用如下命令：

    ```bash
    curl --digest --user '<Public Key>:<Private Key>' \
      --request GET 'https://<region>.data.tidbcloud.com/api/v1beta/app/<App ID>/endpoint/<Endpoint Path>'
    ```

    </div>
    </SimpleTab>

    > **注意：**
    >
    > - 通过请求 region 域名 `<region>.data.tidbcloud.com`，你可以直接 access TiDB 集群所在 region 的端点。
    > - 你也可以不指定 region，直接请求 global 域名 `data.tidbcloud.com`。此时，TiDB Cloud 会在内部将请求重定向到目标 region，但可能会带来额外延时。如果选择这种方式，调用端点时请确保在 curl 命令中添加 `--location-trusted` 选项。

#### 3. 使用代码示例

将代码示例粘贴到你的应用中并运行，即可获得端点的 response。

- 你需要将 `<Public Key>` 和 `<Private Key>` 占位符替换为你的 API key。
- 如果端点包含 parameter，调用端点时请指定 parameter 值。

调用端点后，你可以看到 JSON 格式的 response。示例如下：

```json
{
  "type": "sql_endpoint",
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
    }
  }
}
```

关于 response 的详细信息，参见 [端点的响应](/tidb-cloud/data-service-manage-endpoint.md#response)。

## 了解更多

- [Data Service 概览](/tidb-cloud/data-service-overview.md)
- [快速开始使用 Chat2Query API](/tidb-cloud/use-chat2query-api.md)
- [管理 Data App](/tidb-cloud/data-service-manage-data-app.md)
- [管理端点](/tidb-cloud/data-service-manage-endpoint.md)
