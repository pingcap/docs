---
title: 集成 TiDB Cloud 与 n8n
summary: 了解在 n8n 中使用 TiDB Cloud 节点的方法。
---

# 集成 TiDB Cloud 与 n8n

[n8n](https://n8n.io/) 是一款可扩展的工作流自动化工具。采用 [fair-code](https://faircode.io/) 分发模式，n8n 始终保持源代码可见，支持自托管，并允许你添加自定义函数、逻辑和应用。

本文介绍如何构建一个自动化工作流：创建 TiDB Cloud Starter 集群，收集 Hacker News RSS，将其存储到 TiDB，并发送简报邮件。

> **注意：**
>
> 除了 TiDB Cloud Starter 集群外，本文中的步骤同样适用于 TiDB Cloud Essential 集群。

## 前置条件：获取 TiDB Cloud API 密钥

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，使用左上角的下拉框切换到你的目标组织。
2. 在左侧导航栏，点击 **Organization Settings** > **API Keys**。
3. 在 **API Keys** 页面，点击 **Create API Key**。
4. 输入 API 密钥的描述，然后点击 **Next**。
5. 复制已创建的 API 密钥，稍后在 n8n 中使用，然后点击 **Done**。

更多信息请参见 [TiDB Cloud API Overview](https://docs.pingcap.com/api/tidb-cloud-api-overview)。

## 步骤 1：安装 n8n

有两种方式可以安装自托管的 n8n。任选其一即可。

<SimpleTab>
<div label="npm">

1. 在你的工作环境中安装 [node.js](https://nodejs.org/en/download/)。
2. 通过 `npx` 下载并启动 n8n。

    ```shell
    npx n8n
    ```

</div>
<div label="Docker">

1. 在你的工作环境中安装 [Docker](https://www.docker.com/products/docker-desktop)。
2. 通过 `docker` 下载并启动 n8n。

    ```shell
    docker run -it --rm --name n8n -p 5678:5678 -v ~/.n8n:/home/node/.n8n n8nio/n8n
    ```

</div>
</SimpleTab>

启动 n8n 后，你可以访问 [localhost:5678](http://localhost:5678) 体验 n8n。

## 步骤 2：在 n8n 中安装 TiDB Cloud 节点

TiDB Cloud 节点在 npm 仓库中名为 `n8n-nodes-tidb-cloud`。你需要手动安装该节点，以便通过 n8n 控制 TiDB Cloud。

1. 在 [localhost:5678](http://localhost:5678) 页面，为自托管的 n8n 创建 owner 账户。
2. 进入 **Settings** > **Community nodes**。
3. 点击 **Install a community node**。
4. 在 **npm Package Name** 字段中输入 `n8n-nodes-tidb-cloud`。
5. 点击 **Install**。

随后你可以在 **Workflow** > 搜索栏中搜索 **TiDB Cloud** 节点，并将其拖拽到工作区使用。

## 步骤 3：构建你的工作流

在此步骤中，你将创建一个新工作流，在点击 **Execute** 按钮时向 TiDB 插入一些数据。

本示例工作流将使用以下节点：

- [Schedule Trigger](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.scheduletrigger/)
- [RSS Read](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.rssfeedread/)
- [Code](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.code/)
- [Gmail](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.gmail/)
- [TiDB Cloud 节点](https://www.npmjs.com/package/n8n-nodes-tidb-cloud)

最终的工作流应如下图所示。

![img](/media/tidb-cloud/integration-n8n-workflow-rss.jpg)

### （可选）创建 TiDB Cloud Starter 集群

如果你还没有 TiDB Cloud Starter 集群，可以使用该节点创建一个。否则可跳过此操作。

1. 进入 **Workflows** 面板，点击 **Add workflow**。
2. 在新建工作流的工作区，点击右上角的 **+** 并选择 **All** 字段。
3. 搜索 `TiDB Cloud` 并将其拖拽到工作区。
4. 为 TiDB Cloud 节点输入凭证，即 TiDB Cloud API 密钥。
5. 在 **Project** 列表中选择你的项目。
6. 在 **Operation** 列表中选择 `Create Serverless Cluster`。
7. 在 **Cluster Name** 框中输入集群名称。
8. 在 **Region** 列表中选择一个 Region。
9. 在 **Password** 框中输入用于登录 TiDB 集群的密码。
10. 点击 **Execute Node** 运行该节点。

> **注意：**
>
> 创建新的 TiDB Cloud Starter 集群需要几秒钟时间。

### 创建工作流

#### 使用手动触发器作为工作流的起点

1. 如果你还没有工作流，进入 **Workflows** 面板，点击 **Start from scratch**。否则跳过此步。
2. 点击右上角的 **+** 并搜索 `schedule trigger`。
3. 将手动触发节点拖拽到工作区，并双击该节点。会显示 **Parameters** 对话框。
4. 按如下规则配置：

    - **Trigger Interval**: `Days`
    - **Days Between Triggers**: `1`
    - **Trigger at Hour**: `8am`
    - **Trigger at Minute**: `0`

该触发器会在每天早上 8 点执行你的工作流。

#### 创建用于插入数据的表

1. 在手动触发节点右侧点击 **+**。
2. 搜索 `TiDB Cloud` 并添加到工作区。
3. 在 **Parameters** 对话框中输入 TiDB Cloud 节点的凭证，即你的 TiDB Cloud API 密钥。
4. 在 **Project** 列表中选择你的项目。
5. 在 **Operation** 列表中选择 `Execute SQL`。
6. 选择集群。如果在列表中还未看到新集群，需要等待几分钟直到集群创建完成。
7. 在 **User** 列表中选择用户。TiDB Cloud 总会创建一个默认用户，无需手动创建。
8. 在 **Database** 框中输入 `test`。
9. 输入你的数据库密码。
10. 在 **SQL** 框中输入以下 SQL：

    ```sql
    CREATE TABLE IF NOT EXISTS hacker_news_briefing (creator VARCHAR (200), title TEXT,  link VARCHAR(200), pubdate VARCHAR(200), comments VARCHAR(200), content TEXT, guid VARCHAR (200), isodate VARCHAR(200));
    ```

11. 点击 **Execute node** 创建表。

#### 获取 Hacker News RSS

1. 在 TiDB Cloud 节点右侧点击 **+**。
2. 搜索 `RSS Read` 并添加到工作区。
3. 在 **URL** 框中输入 `https://hnrss.org/frontpage`。

#### 向 TiDB 插入数据

1. 在 RSS Read 节点右侧点击 **+**。
2. 搜索 `TiDB Cloud` 并添加到工作区。
3. 选择你在前一个 TiDB Cloud 节点中输入的凭证。
4. 在 **Project** 列表中选择你的项目。
5. 在 **Operation** 列表中选择 `Insert`。
6. 在 **Cluster**、**User**、**Database** 和 **Password** 框中输入相应的值。
7. 在 **Table** 框中输入 `hacker_news_briefing` 表。
8. 在 **Columns** 框中输入 `creator, title, link, pubdate, comments, content, guid, isodate`。

#### 构建消息

1. 在 RSS Feed Read 节点右侧点击 **+**。
2. 搜索 `code` 并添加到工作区。
3. 选择 `Run Once for All Items` 模式。
4. 在 **JavaScript** 框中复制粘贴以下代码。

    ```javascript
    let message = "";

    // Loop the input items
    for (item of items) {
      message += `
          <h3>${item.json.title}</h3>
          <br>
          ${item.json.content}
          <br>
          `
    }

    let response =
        `
          <!DOCTYPE html>
          <html>
          <head>
          <title>Hacker News Briefing</title>
        </head>
        <body>
            ${message}
        </body>
        </html>
        `
    // Return our message
    return [{json: {response}}];
    ```

#### 通过 Gmail 发送消息

1. 在 code 节点右侧点击 **+**。
2. 搜索 `gmail` 并添加到工作区。
3. 输入 Gmail 节点的凭证。详细说明请参考 [n8n 文档](https://docs.n8n.io/integrations/builtin/credentials/google/oauth-single-service/)。
4. 在 **Resource** 列表中选择 `Message`。
5. 在 **Operation** 列表中选择 `Send`。
6. 在 **To** 框中输入你的邮箱。
7. 在 **Subject** 框中输入 `Hacker News Briefing`。
8. 在 **Email Type** 框中选择 `HTML`。
9. 在 **Message** 框中点击 `Expression` 并输入 `{{ $json["response"] }}`。

    > **注意：**
    >
    > 你必须将鼠标悬停在 **Message** 框上并选择 **Expression** 模式。

## 步骤 4：运行你的工作流

构建好工作流后，你可以点击 **Execute Workflow** 进行测试运行。

如果工作流按预期运行，你将收到 Hacker News 简报邮件。这些新闻内容会被记录到你的 TiDB Cloud Starter 集群中，无需担心丢失。

现在你可以在 **Workflows** 面板激活该工作流。此工作流将帮助你每天获取 Hacker News 首页文章。

## TiDB Cloud 节点核心

### 支持的操作

TiDB Cloud 节点作为 [常规节点](https://docs.n8n.io/workflows/nodes/#regular-nodes) 使用，仅支持以下五种操作：

- **Create Serverless Cluster**：创建 TiDB Cloud Starter 集群。
- **Execute SQL**：在 TiDB 中执行 SQL 语句。
- **Delete**：删除 TiDB 中的行。
- **Insert**：向 TiDB 插入行。
- **Update**：修改 TiDB 中的行。

### 字段

使用不同操作时，你需要填写不同的必填字段。以下为各对应操作的字段说明。

<SimpleTab>
<div label="Create Serverless Cluster">

- **Credential for TiDB Cloud API**：仅支持 TiDB Cloud API 密钥。如何创建 API 密钥请参考 [获取 TiDB Cloud API 密钥](#前置条件获取-tidb-cloud-api-密钥)。
- **Project**：TiDB Cloud 项目名称。
- **Operation**：该节点的操作。所有支持的操作请参考 [支持的操作](#支持的操作)。
- **Cluster**：TiDB Cloud 集群名称。输入你的新集群名称。
- **Region**：Region 名称。选择你的集群将要部署的 Region。通常选择离你的应用部署最近的 Region。
- **Password**：root 密码。为你的新集群设置密码。

</div>
<div label="Execute SQL">

- **Credential for TiDB Cloud API**：仅支持 TiDB Cloud API 密钥。如何创建 API 密钥请参考 [获取 TiDB Cloud API 密钥](#前置条件获取-tidb-cloud-api-密钥)。
- **Project**：TiDB Cloud 项目名称。
- **Operation**：该节点的操作。所有支持的操作请参考 [支持的操作](#支持的操作)。
- **Cluster**：TiDB Cloud 集群名称。你应选择一个已有集群。
- **Password**：TiDB Cloud 集群的密码。
- **User**：TiDB Cloud 集群的用户名。
- **Database**：数据库名称。
- **SQL**：要执行的 SQL 语句。

</div>
<div label="Delete">

- **Credential for TiDB Cloud API**：仅支持 TiDB Cloud API 密钥。如何创建 API 密钥请参考 [获取 TiDB Cloud API 密钥](#前置条件获取-tidb-cloud-api-密钥)。
- **Project**：TiDB Cloud 项目名称。
- **Operation**：该节点的操作。所有支持的操作请参考 [支持的操作](#支持的操作)。
- **Cluster**：TiDB Cloud 集群名称。你应选择一个已有集群。
- **Password**：TiDB Cloud 集群的密码。
- **User**：TiDB Cloud 集群的用户名。
- **Database**：数据库名称。
- **Table**：表名。你可以使用 `From list` 模式选择，或用 `Name` 模式手动输入表名。
- **Delete Key**：决定数据库中哪些行被删除的项属性名。item 是从一个节点传递到另一个节点的数据。节点会对每个输入数据项执行操作。关于 n8n 中的 item 更多信息请参见 [n8n 文档](https://docs.n8n.io/workflows/items/)。

</div>
<div label="Insert">

- **Credential for TiDB Cloud API**：仅支持 TiDB Cloud API 密钥。如何创建 API 密钥请参考 [获取 TiDB Cloud API 密钥](#前置条件获取-tidb-cloud-api-密钥)。
- **Project**：TiDB Cloud 项目名称。
- **Operation**：该节点的操作。所有支持的操作请参考 [支持的操作](#支持的操作)。
- **Cluster**：TiDB Cloud 集群名称。你应选择一个已有集群。
- **Password**：TiDB Cloud 集群的密码。
- **User**：TiDB Cloud 集群的用户名。
- **Database**：数据库名称。
- **Table**：表名。你可以使用 `From list` 模式选择，或用 `Name` 模式手动输入表名。
- **Columns**：以逗号分隔的输入项属性列表，用作新行的列。item 是从一个节点传递到另一个节点的数据。节点会对每个输入数据项执行操作。关于 n8n 中的 item 更多信息请参见 [n8n 文档](https://docs.n8n.io/workflows/items/)。

</div>
<div label="Update">

- **Credential for TiDB Cloud API**：仅支持 TiDB Cloud API 密钥。如何创建 API 密钥请参考 [获取 TiDB Cloud API 密钥](#前置条件获取-tidb-cloud-api-密钥)。
- **Project**：TiDB Cloud 项目名称。
- **Operation**：该节点的操作。所有支持的操作请参考 [支持的操作](#支持的操作)。
- **Cluster**：TiDB Cloud 集群名称。你应选择一个已有集群。
- **Password**：TiDB Cloud 集群的密码。
- **User**：TiDB Cloud 集群的用户名。
- **Database**：数据库名称。
- **Table**：表名。你可以使用 `From list` 模式选择，或用 `Name` 模式手动输入表名。
- **Update Key**：决定数据库中哪些行被修改的项属性名。item 是从一个节点传递到另一个节点的数据。节点会对每个输入数据项执行操作。关于 n8n 中的 item 更多信息请参见 [n8n 文档](https://docs.n8n.io/workflows/items/)。
- **Columns**：以逗号分隔的输入项属性列表，用作要修改的行的列。

</div>
</SimpleTab>

### 限制

- **Execute SQL** 操作通常只允许执行一条 SQL 语句。如果你希望在一次操作中执行多条语句，需要手动开启 [`tidb_multi_statement_mode`](https://docs.pingcap.com/tidbcloud/system-variables#tidb_multi_statement_mode-new-in-v4011)。
- 对于 **Delete** 和 **Update** 操作，你需要指定一个字段作为 key。例如，`Delete Key` 设置为 `id`，等价于执行 `DELETE FROM table WHERE id = ${item.id}`。目前 **Delete** 和 **Update** 操作仅支持指定一个 key。
- 对于 **Insert** 和 **Update** 操作，你需要在 **Columns** 字段中指定以逗号分隔的列表，且字段名必须与输入项的属性名一致。