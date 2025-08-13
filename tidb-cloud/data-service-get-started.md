---
title: 快速入门 Data Service
summary: 了解如何使用 TiDB Cloud Data Service 通过 HTTPS 请求访问你的数据。
---

# 快速入门 Data Service

Data Service（测试版）使你能够通过自定义 API 端点使用 HTTPS 请求访问 TiDB Cloud 数据，并允许你无缝集成到任何兼容 HTTPS 的应用或服务中。

> **提示：**
>
> TiDB Cloud 为 TiDB 集群提供了 Chat2Query API。启用后，TiDB Cloud 会自动在 Data Service 中创建一个名为 **Chat2Query** 的系统 Data App 以及一个 Chat2Data 端点。你可以调用该端点，通过提供指令让 AI 生成并执行 SQL 语句。
>
> 更多信息，参见 [快速入门 Chat2Query API](/tidb-cloud/use-chat2query-api.md)。

本文档介绍如何通过创建 Data App、开发、测试、部署和调用端点，快速上手 TiDB Cloud Data Service（测试版）。Data App 是一组端点的集合，你可以用它来为特定应用访问数据。

## 开始之前

在创建 Data App 之前，请确保你已经创建了 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群。如果还没有，请按照 [创建 TiDB Cloud Serverless 集群](/tidb-cloud/create-tidb-cluster-serverless.md) 的步骤进行创建。

## 使用示例 Data App 快速入门

创建一个示例 Data App 是快速上手 Data Service 的最佳方式。如果你的项目还没有任何 Data App，可以按照 **Data Service** 页面上的引导创建一个示例 Data App，并通过该 App 体验 Data Service 的功能。

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 的左侧导航栏，点击 <MDSvgIcon name="icon-left-data-service" /> **Data Service**。

2. 在 **Data Service** 页面，点击 **Create Sample Data App**。会弹出一个对话框。

3. 在对话框中，如有需要可修改 App 名称，选择你希望 Data App 访问的集群，然后点击 **Create**。

    创建过程只需几秒钟。

    > **注意：**
    >
    > 如果当前项目下没有集群，可以在 **Link Data Sources** 下拉列表中点击 **Create New Cluster** 先创建一个集群。

4. 示例 Data App 自动创建完成后，你可以在左侧看到 App 名称和端点列表，在中间看到某个端点的 SQL 语句，在右侧看到关于如何使用示例 Data App 的说明。

5. 按照右侧的说明，选择一个端点并使用 curl 命令调用该端点。

## 使用自定义 Data App 快速入门

你也可以通过创建自己的 Data App，并按照以下步骤开发、测试、部署和调用端点，快速上手 Data Service。

### 步骤 1. 创建 Data App

要创建 Data App，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 的左侧导航栏，点击 <MDSvgIcon name="icon-left-data-service" /> **Data Service**。

2. 在项目的 [**Data Service**](https://tidbcloud.com/project/data-service) 页面左侧，点击 <MDSvgIcon name="icon-create-data-app" /> **Create DataApp**。

    > **提示：**
    >
    > 如果这是你项目中的第一个 Data App，请在页面中间点击 **Create Data App**。

3. 在 **Create Data App** 对话框中，输入名称、描述，并选择你希望 Data App 访问的集群。

    > **注意：**
    >
    > 默认情况下，Data App 类型为 **Standard Data App**。如果你想创建 **Chat2Query Data App**，请参考 [快速入门 Chat2Query API](/tidb-cloud/use-chat2query-api.md)，而不是本文档。

4. （可选）如需将 Data App 的端点自动部署到你指定的 GitHub 仓库和分支，请启用 **Connect to GitHub**，然后执行以下操作：

    1. 点击 **Install on GitHub**，并按照页面指引将 **TiDB Cloud Data Service** 作为应用安装到目标仓库。
    2. 返回 TiDB Cloud 控制台，点击 **Authorize** 授权 GitHub 上的应用访问权限。
    3. 指定你希望保存 Data App 配置文件的目标仓库、分支和目录。

    > **注意：**
    >
    > - 目录必须以斜杠（`/`）开头。例如，`/mydata`。如果你指定的目录在目标仓库和分支下不存在，会自动创建。
    > - 仓库、分支和目录的组合唯一标识配置文件路径，在所有 Data App 中必须唯一。如果你指定的路径已被其他 Data App 使用，需要重新指定路径。否则，在 TiDB Cloud 控制台为当前 Data App 配置的端点会覆盖你指定路径下的文件。

5. 点击 **Create Data App**。会显示 [**Data Service**](https://tidbcloud.com/project/data-service) 详情页。

6. 如果你已配置将 Data App 连接到 GitHub，请检查你指定的 GitHub 目录。你会发现 [Data App 配置文件](/tidb-cloud/data-service-app-config-files.md) 已由 `tidb-cloud-data-service` 提交到该目录，说明 Data App 已成功连接到 GitHub。

    对于新建的 Data App，**Auto Sync & Deployment** 和 **Review Draft** 默认开启，你可以方便地在 TiDB Cloud 控制台和 GitHub 之间同步 Data App 变更，并在部署前审查变更。关于 GitHub 集成的更多信息，参见 [通过 GitHub 自动部署 Data App 变更](/tidb-cloud/data-service-manage-github-connection.md)。

### 步骤 2. 开发端点

端点是你可以自定义以执行 SQL 语句的 Web API。

要创建新端点，定位到新建的 Data App，点击 App 名称右侧的 **+** **Create Endpoint**。

#### 配置属性

在右侧面板点击 **Properties** 标签页，为端点设置属性，例如：

- **Path**：用户访问端点时使用的路径。请求方法和路径的组合在同一个 Data App 内必须唯一。

- **Endpoint URL**：（只读）URL 会根据对应集群所在区域、Data App 的服务 URL 以及端点路径自动生成。例如，如果端点路径为 `/my_endpoint/get_id`，则端点 URL 为 `https://<region>.data.tidbcloud.com/api/v1beta/app/<App ID>/endpoint/my_endpoint/get_id`。

- **Request Method**：端点的 HTTP 方法。你可以使用 `GET` 获取数据，使用 `POST` 创建或插入数据，使用 `PUT` 更新或修改数据，使用 `DELETE` 删除数据。

关于端点属性的更多信息，参见 [配置属性](/tidb-cloud/data-service-manage-endpoint.md#configure-properties)。

#### 编写 SQL 语句

你可以在 **Data Service** 页中间的 SQL 编辑器自定义端点的 SQL 语句。

1. 选择集群。

    > **注意：**
    >
    > 只有已关联到 Data App 的集群会显示在下拉列表中。要管理已关联的集群，参见 [管理已关联集群](/tidb-cloud/data-service-manage-data-app.md#manage-linked-data-sources)。

    在 SQL 编辑器上方，从下拉列表中选择你希望执行 SQL 语句的集群。然后，你可以在右侧面板的 **Schema** 标签页查看该集群的所有数据库。

2. 编写 SQL 语句。

    在查询或修改数据前，需要在 SQL 语句中先指定数据库。例如，`USE database_name;`。

    在 SQL 编辑器中，你可以编写表连接查询、复杂查询、聚合函数等语句。你也可以直接输入 `--` 加上你的指令，让 AI 自动生成 SQL 语句。

    > **注意：**
    >
    > 如需体验 TiDB Cloud 的 AI 能力，你需要允许 PingCAP 和 Amazon Bedrock 使用你的代码片段进行研究和服务改进。更多信息，参见 [启用或禁用 AI 生成 SQL 查询](/tidb-cloud/explore-data-with-chat2query.md#enable-or-disable-ai-to-generate-sql-queries)。

    如需定义参数，可以在 SQL 语句中以变量占位符的形式插入，例如 `${ID}`。例如，`SELECT * FROM table_name WHERE id = ${ID}`。然后，你可以点击右侧面板的 **Params** 标签页修改参数定义和测试值。

    > **注意：**
    >
    > - 参数名区分大小写。
    > - 参数不能用作表名或列名。

    - 在 **Definition** 部分，你可以指定客户端调用端点时参数是否必填、数据类型和默认值。
    - 在 **Test Values** 部分，你可以为参数设置测试值。测试值用于运行 SQL 语句或测试端点时。如果未设置测试值，则使用默认值。
    - 更多信息，参见 [配置参数](/tidb-cloud/data-service-manage-endpoint.md#configure-parameters)。

3. 运行 SQL 语句。

    如果 SQL 语句中包含参数，请确保你已在右侧 **Params** 标签页为参数设置了测试值或默认值，否则会返回错误。

    <SimpleTab>
    <div label="macOS">

    对于 macOS：

    - 如果编辑器中只有一条语句，按 **⌘ + Enter** 或点击 <svg width="1rem" height="1rem" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.70001 20.7756C6.01949 20.3926 6.00029 19.5259 6.00034 19.0422L6.00034 12.1205L6 5.33028C6 4.75247 6.00052 3.92317 6.38613 3.44138C6.83044 2.88625 7.62614 2.98501 7.95335 3.05489C8.05144 3.07584 8.14194 3.12086 8.22438 3.17798L19.2865 10.8426C19.2955 10.8489 19.304 10.8549 19.3126 10.8617C19.4069 10.9362 20 11.4314 20 12.1205C20 12.7913 19.438 13.2784 19.3212 13.3725C19.307 13.3839 19.2983 13.3902 19.2831 13.4002C18.8096 13.7133 8.57995 20.4771 8.10002 20.7756C7.60871 21.0812 7.22013 21.0683 6.70001 20.7756Z" fill="currentColor"></path></svg>**Run** 运行。

    - 如果编辑器中有多条语句，要顺序运行其中一条或多条，将光标放在目标语句上或选中目标语句的行，然后按 **⌘ + Enter** 或点击 **Run**。

    - 要顺序运行编辑器中的所有语句，按 **⇧ + ⌘ + Enter**，或用光标选中所有语句的行后点击 **Run**。

    </div>

    <div label="Windows/Linux">

    对于 Windows 或 Linux：

    - 如果编辑器中只有一条语句，按 **Ctrl + Enter** 或点击 <svg width="1rem" height="1rem" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.70001 20.7756C6.01949 20.3926 6.00029 19.5259 6.00034 19.0422L6.00034 12.1205L6 5.33028C6 4.75247 6.00052 3.92317 6.38613 3.44138C6.83044 2.88625 7.62614 2.98501 7.95335 3.05489C8.05144 3.07584 8.14194 3.12086 8.22438 3.17798L19.2865 10.8426C19.2955 10.8489 19.304 10.8549 19.3126 10.8617C19.4069 10.9362 20 11.4314 20 12.1205C20 12.7913 19.438 13.2784 19.3212 13.3725C19.307 13.3839 19.2983 13.3902 19.2831 13.4002C18.8096 13.7133 8.57995 20.4771 8.10002 20.7756C7.60871 21.0812 7.22013 21.0683 6.70001 20.7756Z" fill="currentColor"></path></svg>**Run** 运行。

    - 如果编辑器中有多条语句，要顺序运行其中一条或多条，将光标放在目标语句上或选中目标语句的行，然后按 **Ctrl + Enter** 或点击 **Run**。

    - 要顺序运行编辑器中的所有语句，按 **Shift + Ctrl + Enter**，或用光标选中所有语句的行后点击 **Run**。

    </div>
    </SimpleTab>

    运行语句后，你可以在页面底部的 **Result** 标签页立即看到查询结果。

### 步骤 3. 测试端点（可选）

配置端点后，你可以先测试端点，验证其是否按预期工作，再进行部署。

要测试端点，点击右上角的 **Test** 或按 **F5**。

然后，你可以在页面底部的 **HTTP Response** 标签页看到响应。关于响应的更多信息，参见 [端点的响应](/tidb-cloud/data-service-manage-endpoint.md#response)。

### 步骤 4. 部署端点

要部署端点，请执行以下步骤：

1. 在端点详情页，点击右上角的 **Deploy**。

2. 点击 **Deploy** 确认部署。如果端点部署成功，会提示 **Endpoint has been deployed**。

    如需查看部署历史，可以点击左侧 Data App 名称，再点击右侧的 **Deployments** 标签页。

### 步骤 5. 调用端点

你可以通过发送 HTTPS 请求调用端点。在调用端点前，需要先为 Data App 获取 API key。

#### 1. 创建 API key

1. 在 [**Data Service**](https://tidbcloud.com/project/data-service) 页左侧，点击你的 Data App 名称查看详情。
2. 在 **Authentication** 区域，点击 **Create API Key**。
3. 在 **Create API Key** 对话框中，执行以下操作：

    1. （可选）为 API key 输入描述。
    2. 选择 API key 的角色。

        角色用于控制 API key 是否可以对 Data App 关联的集群进行读写。你可以选择 `ReadOnly` 或 `ReadAndWrite` 角色：

        - `ReadOnly`：只允许 API key 读取数据，如 `SELECT`、`SHOW`、`USE`、`DESC` 和 `EXPLAIN` 语句。
        - `ReadAndWrite`：允许 API key 读写数据。你可以用该 API key 执行所有 SQL 语句，如 DML 和 DDL 语句。

    3. （可选）为 API key 设置期望的速率限制。

4. 点击 **Next**。会显示公钥和私钥。

    请务必将私钥复制并妥善保存。离开此页面后，将无法再次获取完整私钥。

5. 点击 **Done**。

关于 API key 的更多信息，参见 [Data Service 中的 API Key](/tidb-cloud/data-service-api-key.md)。

#### 2. 获取代码示例

TiDB Cloud 会生成代码示例，帮助你调用端点。要获取代码示例，请执行以下步骤：

1. 在 [**Data Service**](https://tidbcloud.com/project/data-service) 页左侧，点击你的端点名称，然后点击右上角 **...** > **Code Example**。会弹出 **Code Example** 对话框。

2. 在对话框中，选择你希望用于调用端点的集群和数据库，然后复制代码示例。

    curl 代码示例如下：

    <SimpleTab>
    <div label="Test Environment">

    如需调用端点的草稿版本，需要添加 `endpoint-type: draft` 头：

    ```bash
    curl --digest --user '<Public Key>:<Private Key>' \
      --request GET 'https://<region>.data.tidbcloud.com/api/v1beta/app/<App ID>/endpoint/<Endpoint Path>' \
      --header 'endpoint-type: draft'
    ```

    </div>

    <div label="Online Environment">

    你必须先部署端点，才能在在线环境下查看代码示例。

    如需调用端点的当前在线版本，使用如下命令：

    ```bash
    curl --digest --user '<Public Key>:<Private Key>' \
      --request GET 'https://<region>.data.tidbcloud.com/api/v1beta/app/<App ID>/endpoint/<Endpoint Path>'
    ```

    </div>
    </SimpleTab>

    > **注意：**
    >
    > - 通过请求区域域名 `<region>.data.tidbcloud.com`，你可以直接访问 TiDB 集群所在区域的端点。
    > - 你也可以不指定区域，直接请求全局域名 `data.tidbcloud.com`。此时，TiDB Cloud 会在内部将请求重定向到目标区域，但可能会带来额外延迟。如果选择这种方式，调用端点时请确保在 curl 命令中添加 `--location-trusted` 选项。

#### 3. 使用代码示例

将代码示例粘贴到你的应用中并运行，即可获取端点响应。

- 你需要将 `<Public Key>` 和 `<Private Key>` 占位符替换为你的 API key。
- 如果端点包含参数，调用端点时请指定参数值。

调用端点后，你可以看到 JSON 格式的响应。例如：

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

关于响应的更多信息，参见 [端点的响应](/tidb-cloud/data-service-manage-endpoint.md#response)。

## 了解更多

- [Data Service 概览](/tidb-cloud/data-service-overview.md)
- [快速入门 Chat2Query API](/tidb-cloud/use-chat2query-api.md)
- [管理 Data App](/tidb-cloud/data-service-manage-data-app.md)
- [管理端点](/tidb-cloud/data-service-manage-endpoint.md)
