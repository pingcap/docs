---
title: 将 TiDB Cloud 集成到 Zapier
summary: 了解如何通过 Zapier 将 TiDB Cloud 连接到 5000+ 应用。
---

# 将 TiDB Cloud 集成到 Zapier

[Zapier](https://zapier.com) 是一款无代码自动化工具，可以让你轻松创建涉及数千个应用和服务的工作流。

在 Zapier 上使用 [TiDB Cloud app](https://zapier.com/apps/tidb-cloud/integrations) 可以让你：

- 使用 TiDB，这是一款兼容 MySQL 的 HTAP 数据库，无需本地搭建。
- 更便捷地管理你的 TiDB Cloud。
- 将 TiDB Cloud 连接到 5000+ 应用，实现工作流自动化。

本指南将对 Zapier 上的 TiDB Cloud app 进行高层次介绍，并提供一个使用示例。

## 使用模板快速开始

[Zap Templates](https://platform.zapier.com/partners/zap-templates) 是为公开可用的 Zapier 集成预先选定应用和核心字段的现成集成或 Zap。

本节将以 **Add new Github global events to TiDB rows** 模板为例，创建一个工作流。在该工作流中，每当你的 GitHub 账户产生新的全局事件（任何 [GitHub event](https://docs.github.com/en/developers/webhooks-and-events/events/github-event-types)，无论是你发起还是针对你的，发生在任意仓库），Zapier 都会在你的 TiDB Cloud 集群中新增一行数据。

### 前置条件

在开始之前，你需要：

- 一个 [Zapier 账户](https://zapier.com/app/login)。
- 一个 [GitHub 账户](https://github.com/login)。
- 一个 [TiDB Cloud 账户](https://tidbcloud.com/signup) 以及在 TiDB Cloud 上创建的 TiDB Cloud Serverless 集群。更多详情请参见 [TiDB Cloud 快速上手](https://docs.pingcap.com/tidbcloud/tidb-cloud-quickstart#step-1-create-a-tidb-cluster)。

### 步骤 1：获取模板

访问 [TiDB Cloud App on Zapier](https://zapier.com/apps/tidb-cloud/integrations)。选择 **Add new Github global events to TiDB rows** 模板并点击 **Try it**。随后你将进入编辑页面。

### 步骤 2：设置触发器

在编辑页面，你可以看到触发器和动作。点击触发器进行设置。

1. 选择应用和事件

    模板已默认设置好应用和事件，因此此处无需操作。点击 **Continue**。

2. 选择账户

    选择你想要与 TiDB Cloud 连接的 GitHub 账户。你可以连接新账户或选择已有账户。设置完成后，点击 **Continue**。

3. 设置触发器

    模板已默认设置好触发器。点击 **Continue**。

4. 测试触发器

    点击 **Test trigger**。如果触发器设置成功，你可以看到来自 GitHub 账户的新全局事件数据。点击 **Continue**。

### 步骤 3：设置 `Find Table in TiDB Cloud` 动作

1. 选择应用和事件

    保持模板默认设置的 `Find Table`。点击 **Continue**。

2. 选择账户

    1. 点击 **Sign in** 按钮，你将被重定向到新的登录页面。
    2. 在登录页面，填写你的公钥和私钥。获取 TiDB Cloud API key 的方法请参见 [TiDB Cloud API 文档](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-Key-Management)。
    3. 点击 **Continue**。

    ![Account](/media/tidb-cloud/zapier/zapier-tidbcloud-account.png)

3. 设置动作

    在此步骤，你需要指定 TiDB Cloud 集群中的某个表来存储事件数据。如果你还没有表，可以在此步骤创建。

    1. 在下拉列表中选择项目名称和集群名称。你的集群连接信息会自动显示。

        ![Set up project name and cluster name](/media/tidb-cloud/zapier/zapier-set-up-tidbcloud-project-and-cluster.png)

    2. 输入你的密码。

    3. 在下拉列表中选择数据库。

        ![Set up database name](/media/tidb-cloud/zapier/zapier-set-up-tidbcloud-databse.png)

        Zapier 会使用你输入的密码从 TiDB Cloud 查询数据库。如果在集群中未找到数据库，请重新输入密码并刷新页面。

    4. 在 **The table you want to search** 框中填写 `github_global_event`。如果该表不存在，模板会使用以下 DDL 创建表。点击 **Continue**。

        ![The create table DDL](/media/tidb-cloud/zapier/zapier-tidbcloud-create-table-ddl.png)

4. 测试动作

    点击 **Test action**，Zapier 会创建该表。你也可以跳过测试，首次运行该工作流时表会被自动创建。

### 步骤 4：设置 `Create Row in TiDB Cloud` 动作

1. 选择应用和事件

    保持模板默认设置。点击 **Continue**。

2. 选择账户

    选择你在设置 `Find Table in TiDB Cloud` 动作时选择的账户。点击 **Continue**。

    ![Choose account](/media/tidb-cloud/zapier/zapier-tidbcloud-choose-account.png)

3. 设置动作

    1. 按照上一步填写 **Project Name**、**Cluster Name**、**TiDB Password** 和 **Database Name**。

    2. 在 **Table Name** 处，从下拉列表选择 **github_global_event** 表。表的列会显示出来。

        ![Table columns](/media/tidb-cloud/zapier/zapier-set-up-tidbcloud-columns.png)

    3. 在 **Columns** 框中，从触发器中选择对应的数据。填写所有列后，点击 **Continue**。

        ![Fill in Columns](/media/tidb-cloud/zapier/zapier-fill-in-tidbcloud-triggers-data.png)

4. 测试动作

    点击 **Test action**，即可在表中创建新行。如果你检查 TiDB Cloud 集群，可以看到数据已成功写入。

   ```sql
   mysql> SELECT * FROM test.github_global_event;
   +-------------+-------------+------------+-----------------+----------------------------------------------+--------+---------------------+
   | id          | type        | actor      | repo_name       | repo_url                                     | public | created_at          |
   +-------------+-------------+------------+-----------------+----------------------------------------------+--------+---------------------+
   | 25324462424 | CreateEvent | shiyuhang0 | shiyuhang0/docs | https://api.github.com/repos/shiyuhang0/docs | True   | 2022-11-18 08:03:14 |
   +-------------+-------------+------------+-----------------+----------------------------------------------+--------+---------------------+
   1 row in set (0.17 sec)
   ```

### 步骤 5：发布你的 zap

点击 **Publish** 发布你的 zap。你可以在 [主页](https://zapier.com/app/zaps) 看到 zap 正在运行。

![Publish the zap](/media/tidb-cloud/zapier/zapier-tidbcloud-publish.png)

现在，该 zap 会自动将你 GitHub 账户的所有全局事件记录到 TiDB Cloud。

## 触发器与动作

[Triggers and actions](https://zapier.com/how-it-works) 是 Zapier 的核心概念。通过组合不同的触发器和动作，你可以创建各种自动化工作流。

本节介绍 TiDB Cloud App 在 Zapier 上提供的触发器和动作。

### 触发器

下表列出了 TiDB Cloud App 支持的触发器。

| Trigger                | Description                                                                 |
| ---------------------- |-----------------------------------------------------------------------------|
| New Cluster            | 当新集群被创建时触发。                                                     |
| New Table              | 当新表被创建时触发。                                                       |
| New Row                | 当新行被创建时触发。仅获取最近 10000 条新行。                               |
| New Row (Custom Query) | 当你提供的自定义查询返回新行时触发。                                       |

### 动作

下表列出了 TiDB Cloud App 支持的动作。注意部分动作需要额外资源，你需要提前准备好相应资源。

| Action | Description | Resource |
|---|---|---|
| Find Cluster | 查找已存在的 TiDB Cloud Serverless 或 TiDB Cloud Dedicated 集群。 | None |
| Create Cluster | 创建新集群。仅支持创建 TiDB Cloud Serverless 集群。 | None |
| Find Database | 查找已存在的数据库。 | 一个 TiDB Cloud Serverless 集群 |
| Create Database | 创建新数据库。 | 一个 TiDB Cloud Serverless 集群 |
| Find Table | 查找已存在的表。 | 一个 TiDB Cloud Serverless 集群和一个数据库 |
| Create Table | 创建新表。 | 一个 TiDB Cloud Serverless 集群和一个数据库 |
| Create Row | 创建新行。 | 一个 TiDB Cloud Serverless 集群、一个数据库和一个表 |
| Update Row | 更新已存在的行。 | 一个 TiDB Cloud Serverless 集群、一个数据库和一个表 |
| Find Row | 通过查找列在表中查找行。 | 一个 TiDB Cloud Serverless 集群、一个数据库和一个表 |
| Find Row (Custom Query) | 通过你提供的自定义查询在表中查找行。 | 一个 TiDB Cloud Serverless 集群、一个数据库和一个表 |

## TiDB Cloud App 模板

TiDB Cloud 提供了一些可直接在 Zapier 使用的模板。你可以在 [TiDB Cloud App](https://zapier.com/apps/tidb-cloud/integrations) 页面找到所有模板。

以下是一些示例：

- [Duplicate new TiDB Cloud rows in Google Sheets](https://zapier.com/apps/google-sheets/integrations/tidb-cloud/1134881/duplicate-new-tidb-cloud-rows-in-google-sheets)。
- [Send emails via Gmail from new custom TiDB queries](https://zapier.com/apps/gmail/integrations/tidb-cloud/1134903/send-emails-via-gmail-from-new-custom-tidb-queries)。
- [Add rows to TiDB Cloud from newly caught webhooks](https://zapier.com/apps/tidb-cloud/integrations/webhook/1134955/add-rows-to-tidb-cloud-from-newly-caught-webhooks)。
- [Store new Salesforce contacts on TiDB rows](https://zapier.com/apps/salesforce/integrations/tidb-cloud/1134923/store-new-salesforce-contacts-on-tidb-rows)。
- [Create TiDB rows for new Gmail emails with resumes and send direct Slack notifications](https://zapier.com/apps/gmail/integrations/slack/1135456/create-tidb-rows-for-new-gmail-emails-with-resumes-and-send-direct-slack-notifications)

## 常见问题

### 如何在 Zapier 中设置 TiDB Cloud 账户？

Zapier 需要你的 **TiDB Cloud API key** 来连接 TiDB Cloud 账户。Zapier 不需要你的 TiDB Cloud 登录账户。

获取 TiDB Cloud API key 的方法请参见 [TiDB Cloud API 文档](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-Key-Management)。

### TiDB Cloud 触发器如何去重？

Zapier 触发器可以通过轮询 API 调用定期检查新数据（间隔取决于你的 Zapier 计划）。

TiDB Cloud 触发器提供了一个轮询 API 调用，会返回大量结果。但大多数结果 Zapier 之前已经见过，也就是说大多数结果是重复的。

由于我们不希望当某个项目在你的 API 中出现在多次不同轮询时多次触发动作，TiDB Cloud 触发器会用 `id` 字段进行数据去重。

`New Cluster` 和 `New Table` 触发器直接使用 `cluster_id` 或 `table_id` 作为 `id` 字段进行去重。这两个触发器你无需额外操作。

**New Row Trigger**

`New Row` 触发器每次最多获取 10000 条结果。因此，如果某些新行未包含在这 10000 条结果中，则无法触发 Zapier。

避免这种情况的一种方式是在触发器中指定 `Order By` 配置。例如，一旦你按创建时间对行排序，新行总会包含在这 10000 条结果中。

`New Row` 触发器还采用灵活策略生成 `id` 字段进行去重。生成 `id` 字段的顺序如下：

1. 如果结果包含 `id` 列，则使用 `id` 列。
2. 如果你在触发器配置中指定了 `Dedupe Key`，则使用 `Dedupe Key`。
3. 如果表有主键，则使用主键。如果有多个主键，使用第一个列。
4. 如果表有唯一键，则使用唯一键。
5. 使用表的第一列。

**New Row (Custom Query) Trigger**

`New Row (Custom Query)` 触发器每次最多获取 1,000,000 条结果。1,000,000 是一个很大的数字，仅用于保护整个系统。建议你的查询包含 `ORDER BY` 和 `LIMIT`。

为了去重，你的查询结果必须有唯一的 id 字段。否则会收到 `You must return the results with id field` 错误。

确保你的自定义查询在 30 秒内执行完毕，否则会收到超时错误。

### 如何使用 `find or create` 动作？

`Find or create` 动作允许你在资源不存在时创建资源。示例如下：

1. 选择 `Find Table` 动作

2. 在 `set up action` 步骤，勾选 `Create TiDB Cloud Table if it doesn’t exist yet?` 以启用 `find and create`。

   ![Find and create](/media/tidb-cloud/zapier/zapier-tidbcloud-find-and-create.png)

该工作流会在表不存在时自动创建表。注意，如果你测试动作，表会被直接创建。