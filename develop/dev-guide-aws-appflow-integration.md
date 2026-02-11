---
title: 集成 TiDB 与 Amazon AppFlow
summary: 逐步介绍如何将 TiDB 与 Amazon AppFlow 集成。
aliases: ['/tidb/stable/dev-guide-aws-appflow-integration/','/tidb/dev/dev-guide-aws-appflow-integration/','/tidbcloud/dev-guide-aws-appflow-integration/']
---

# 集成 TiDB 与 Amazon AppFlow

[Amazon AppFlow](https://aws.amazon.com/appflow/) 是一项全托管的 API 集成 service，可用于将你的 SaaS 应用程序与 AWS service 连接，并安全地传输数据。通过 Amazon AppFlow，你可以在 TiDB 与多种数据提供方之间导入和导出数据，例如 Salesforce、Amazon S3、LinkedIn 和 GitHub。更多信息请参见 AWS 文档中的 [Supported source and destination applications](https://docs.aws.amazon.com/appflow/latest/userguide/app-specific.html)。

本文档介绍如何将 TiDB 与 Amazon AppFlow 集成，并以集成 TiDB Cloud Starter cluster 为例。

如果你还没有 TiDB cluster，可以创建一个 [TiDB Cloud Starter](https://tidbcloud.com/console/clusters) cluster，该 cluster 免费且大约 30 秒即可创建完成。

## 前置条件

- [Git](https://git-scm.com/)
- [JDK](https://openjdk.org/install/) 11 或更高版本
- [Maven](https://maven.apache.org/install.html) 3.8 或更高版本
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) 版本 2
- [AWS Serverless Application Model Command Line Interface (AWS SAM CLI)](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html) 1.58.0 或更高版本
- 一个满足以下要求的 AWS [Identity and Access Management (IAM) user](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users.html)：

    - 该 user 可以通过 [access key](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html) 访问 AWS。
    - 该 user 需要具备以下权限：

        - `AWSCertificateManagerFullAccess`：用于读写 [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/)。
        - `AWSCloudFormationFullAccess`：SAM CLI 使用 [AWS CloudFormation](https://aws.amazon.com/cloudformation/) 来声明 AWS 资源。
        - `AmazonS3FullAccess`：AWS CloudFormation 使用 [Amazon S3](https://aws.amazon.com/s3/?nc2=h_ql_prod_fs_s3) 进行发布。
        - `AWSLambda_FullAccess`：目前，[AWS Lambda](https://aws.amazon.com/lambda/?nc2=h_ql_prod_fs_lbd) 是为 Amazon AppFlow 实现新 connector 的唯一方式。
        - `IAMFullAccess`：SAM CLI 需要为 connector 创建 `ConnectorFunctionRole`。

- 一个 [SalesForce](https://developer.salesforce.com) account。

## 步骤 1. 注册 TiDB connector

### 克隆代码

克隆 TiDB 与 Amazon AppFlow 的 [integration 示例代码仓库](https://github.com/pingcap-inc/tidb-appflow-integration)：

```bash
git clone https://github.com/pingcap-inc/tidb-appflow-integration
```

### 构建并上传 Lambda

1. 构建 package：

    ```bash
    cd tidb-appflow-integration
    mvn clean package
    ```

2. （可选）如果尚未配置 AWS access key ID 和 secret access key，请进行配置。

    ```bash
    aws configure
    ```

3. 将 JAR package 作为 Lambda 上传：

    ```bash
    sam deploy --guided
    ```

    > **注意：**
    >
    > - `--guided` 选项会通过提示引导你完成部署。你的输入会被存储在配置文件中，默认是 `samconfig.toml`。
    > - `stack_name` 指定你正在部署的 AWS Lambda 的名称。
    > - 此引导流程以 AWS 作为 TiDB Cloud Starter 的云服务提供商为例。如果你希望使用 Amazon S3 作为 source 或 destination，需要将 AWS Lambda 的 `region` 设置为与 Amazon S3 相同。
    > - 如果你之前已经运行过 `sam deploy --guided`，可以直接运行 `sam deploy`，SAM CLI 会使用 `samconfig.toml` 配置文件简化交互。

    如果你看到如下类似输出，说明 Lambda 已成功部署。

    ```
    Successfully created/updated stack - <stack_name> in <region>
    ```

4. 进入 [AWS Lambda 控制台](https://console.aws.amazon.com/lambda/home)，你可以看到刚刚上传的 Lambda。请注意需要在窗口右上角选择正确的 region。

    ![lambda dashboard](/media/develop/aws-appflow-step-lambda-dashboard.png)

### 使用 Lambda 注册 connector

1. 在 [AWS 管理控制台](https://console.aws.amazon.com) 中，导航到 [Amazon AppFlow > Connectors](https://console.aws.amazon.com/appflow/home#/gallery)，点击 **Register new connector**。

    ![register connector](/media/develop/aws-appflow-step-register-connector.png)

2. 在 **Register a new connector** 对话框中，选择你上传的 Lambda function，并使用 connector 名称指定 connector label。

    ![register connector dialog](/media/develop/aws-appflow-step-register-connector-dialog.png)

3. 点击 **Register**，此时 TiDB connector 注册成功。

## 步骤 2. 创建 flow

导航到 [Amazon AppFlow > Flows](https://console.aws.amazon.com/appflow/home#/list)，点击 **Create flow**。

![create flow](/media/develop/aws-appflow-step-create-flow.png)

### 设置 flow 名称

输入 flow 名称，然后点击 **Next**。

![name flow](/media/develop/aws-appflow-step-name-flow.png)

### 设置 source 和 destination 表

选择 **Source details** 和 **Destination details**。TiDB connector 可用于两者。

1. 选择 source 名称。本文以 **Salesforce** 作为示例 source。

    ![salesforce source](/media/develop/aws-appflow-step-salesforce-source.png)

    注册 Salesforce 后，Salesforce 会在你的平台中添加一些示例数据。后续步骤将以 **Account** 对象作为示例 source 对象。

    ![salesforce data](/media/develop/aws-appflow-step-salesforce-data.png)

2. 点击 **Connect**。

    1. 在 **Connect to Salesforce** 对话框中，指定此连接的名称，然后点击 **Continue**。

        ![connect to salesforce](/media/develop/aws-appflow-step-connect-to-salesforce.png)

    2. 点击 **Allow**，确认 AWS 可以读取你的 Salesforce 数据。

        ![allow salesforce](/media/develop/aws-appflow-step-allow-salesforce.png)

    > **注意：**
    >
    > 如果你的公司已经在使用 Salesforce 专业版，REST API 默认未启用。你可能需要注册新的开发者版以使用 REST API。详情请参考 [Salesforce Forum Topic](https://developer.salesforce.com/forums/?id=906F0000000D9Y2IAK)。

3. 在 **Destination details** 区域，选择 **TiDB-Connector** 作为 destination。此时会显示 **Connect** 按钮。

    ![tidb dest](/media/develop/aws-appflow-step-tidb-dest.png)

4. 在点击 **Connect** 之前，需要在 TiDB 中为 Salesforce **Account** 对象创建一个 `sf_account` 表。请注意，此表结构与 [Amazon AppFlow 教程](https://docs.aws.amazon.com/appflow/latest/userguide/flow-tutorial-set-up-source.html) 中的示例数据不同。

    ```sql
    CREATE TABLE `sf_account` (
        `id` varchar(255) NOT NULL,
        `name` varchar(150) NOT NULL DEFAULT '',
        `type` varchar(150) NOT NULL DEFAULT '',
        `billing_state` varchar(255) NOT NULL DEFAULT '',
        `rating` varchar(255) NOT NULL DEFAULT '',
        `industry` varchar(255) NOT NULL DEFAULT '',
        PRIMARY KEY (`id`)
    );
    ```

5. 创建好 `sf_account` 表后，点击 **Connect**，会弹出连接对话框。
6. 在 **Connect to TiDB-Connector** 对话框中，输入 TiDB cluster 的连接属性。如果你使用 TiDB Cloud Starter cluster，需要将 **TLS** 选项设置为 `Yes`，以便 TiDB connector 使用 TLS 连接。然后点击 **Connect**。

    ![tidb connection message](/media/develop/aws-appflow-step-tidb-connection-message.png)

7. 现在你可以获取到指定数据库下的所有表。从下拉列表中选择 **sf_account** 表。

    ![database](/media/develop/aws-appflow-step-database.png)

    下图展示了将 Salesforce **Account** 对象数据传输到 TiDB 中 `sf_account` 表的配置：

    ![complete flow](/media/develop/aws-appflow-step-complete-flow.png)

8. 在 **Error handling** 区域，选择 **Stop the current flow run**。在 **Flow trigger** 区域，选择 **Run on demand** 触发类型，表示需要手动运行 flow。然后点击 **Next**。

    ![complete step1](/media/develop/aws-appflow-step-complete-step1.png)

### 设置映射规则

将 Salesforce 中 **Account** 对象的 field 映射到 TiDB 的 `sf_account` 表，然后点击 **Next**。

- `sf_account` 表在 TiDB 中是新建的，当前为空。

    ```sql
    test> SELECT * FROM sf_account;
    +----+------+------+---------------+--------+----------+
    | id | name | type | billing_state | rating | industry |
    +----+------+------+---------------+--------+----------+
    +----+------+------+---------------+--------+----------+
    ```

- 设置映射规则时，可以在左侧选择 source field 名称，右侧选择 destination field 名称。点击 **Map fields**，即可设置一条规则。

    ![add mapping rule](/media/develop/aws-appflow-step-add-mapping-rule.png)

- 本文档需要以下映射规则（Source field name -> Destination field name）：

    - Account ID -> id
    - Account Name -> name
    - Account Type -> type
    - Billing State/Province -> billing_state
    - Account Rating -> rating
    - Industry -> industry

    ![mapping a rule](/media/develop/aws-appflow-step-mapping-a-rule.png)

    ![show all mapping rules](/media/develop/aws-appflow-step-show-all-mapping-rules.png)

### （可选）设置过滤器

如果你希望对数据 field 添加过滤器，可以在此处设置。否则跳过此步骤，点击 **Next**。

![filters](/media/develop/aws-appflow-step-filters.png)

### 确认并创建 flow

确认即将创建的 flow 信息。如果一切无误，点击 **Create flow**。

![review](/media/develop/aws-appflow-step-review.png)

## 步骤 3. 运行 flow

在新建 flow 的页面右上角，点击 **Run flow**。

![run flow](/media/develop/aws-appflow-step-run-flow.png)

下图展示了 flow 成功运行的示例：

![run success](/media/develop/aws-appflow-step-run-success.png)

查询 `sf_account` 表，可以看到 Salesforce **Account** 对象中的记录已写入该表：

```sql
test> SELECT * FROM sf_account;
+--------------------+-------------------------------------+--------------------+---------------+--------+----------------+
| id                 | name                                | type               | billing_state | rating | industry       |
+--------------------+-------------------------------------+--------------------+---------------+--------+----------------+
| 001Do000003EDTlIAO | Sample Account for Entitlements     | null               | null          | null   | null           |
| 001Do000003EDTZIA4 | Edge Communications                 | Customer - Direct  | TX            | Hot    | Electronics    |
| 001Do000003EDTaIAO | Burlington Textiles Corp of America | Customer - Direct  | NC            | Warm   | Apparel        |
| 001Do000003EDTbIAO | Pyramid Construction Inc.           | Customer - Channel | null          | null   | Construction   |
| 001Do000003EDTcIAO | Dickenson plc                       | Customer - Channel | KS            | null   | Consulting     |
| 001Do000003EDTdIAO | Grand Hotels & Resorts Ltd          | Customer - Direct  | IL            | Warm   | Hospitality    |
| 001Do000003EDTeIAO | United Oil & Gas Corp.              | Customer - Direct  | NY            | Hot    | Energy         |
| 001Do000003EDTfIAO | Express Logistics and Transport     | Customer - Channel | OR            | Cold   | Transportation |
| 001Do000003EDTgIAO | University of Arizona               | Customer - Direct  | AZ            | Warm   | Education      |
| 001Do000003EDThIAO | United Oil & Gas, UK                | Customer - Direct  | UK            | null   | Energy         |
| 001Do000003EDTiIAO | United Oil & Gas, Singapore         | Customer - Direct  | Singapore     | null   | Energy         |
| 001Do000003EDTjIAO | GenePoint                           | Customer - Channel | CA            | Cold   | Biotechnology  |
| 001Do000003EDTkIAO | sForce                              | null               | CA            | null   | null           |
+--------------------+-------------------------------------+--------------------+---------------+--------+----------------+
```

## 注意事项

- 如果遇到问题，可以在 AWS 管理控制台的 [CloudWatch](https://console.aws.amazon.com/cloudwatch/home) 页面查看日志。
- 本文档步骤基于 [Building custom connectors using the Amazon AppFlow Custom Connector SDK](https://aws.amazon.com/blogs/compute/building-custom-connectors-using-the-amazon-appflow-custom-connector-sdk/)。
- [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) **不是** 生产环境。
- 为避免篇幅过长，本文示例仅展示了 `Insert` 策略，`Update` 和 `Upsert` 策略也已测试且可用。

## 需要帮助？

- 在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问。
- [提交 TiDB Cloud 支持工单](https://tidb.support.pingcap.com/servicedesk/customer/portals)
- [提交 TiDB 自建版支持工单](/support.md)
