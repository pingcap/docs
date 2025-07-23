---
title: 将 TiDB 集成到 Amazon AppFlow
summary: 逐步介绍如何将 TiDB 与 Amazon AppFlow 集成。
---

# 将 TiDB 集成到 Amazon AppFlow

[Amazon AppFlow](https://aws.amazon.com/appflow/) 是一项完全托管的 API 集成服务，您可以使用它将您的软件即服务（SaaS）应用程序连接到 AWS 服务，并安全地传输数据。通过 Amazon AppFlow，您可以将数据从 TiDB 导入或导出到多种数据提供商，例如 Salesforce、Amazon S3、LinkedIn 和 GitHub。更多信息，请参见 AWS 文档中的 [Supported source and destination applications](https://docs.aws.amazon.com/appflow/latest/userguide/app-specific.html)。

本文档描述了如何将 TiDB 与 Amazon AppFlow 集成，并以集成 {{{ .starter }}} 集群为例。

如果你没有 TiDB 集群，可以创建一个 [{{{ .starter }}}](https://tidbcloud.com/console/clusters) 集群，该集群免费且大约在 30 秒内即可创建完成。

## 前提条件

- [Git](https://git-scm.com/)
- [JDK](https://openjdk.org/install/) 11 或以上
- [Maven](https://maven.apache.org/install.html) 3.8 或以上
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) 版本 2
- [AWS Serverless Application Model Command Line Interface (AWS SAM CLI)](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html) 1.58.0 或以上
- 一个具有以下权限的 AWS [身份与访问管理（IAM）用户](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users.html)：

    - 用户可以使用 [访问密钥](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html) 访问 AWS。
    - 用户拥有以下权限：

        - `AWSCertificateManagerFullAccess`：用于读取和写入 [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/)。
        - `AWSCloudFormationFullAccess`：SAM CLI 使用 [AWS CloudFormation](https://aws.amazon.com/cloudformation/) 来声明 AWS 资源。
        - `AmazonS3FullAccess`：AWS CloudFormation 使用 [Amazon S3](https://aws.amazon.com/s3/?nc2=h_ql_prod_fs_s3) 进行发布。
        - `AWSLambda_FullAccess`：目前，[AWS Lambda](https://aws.amazon.com/lambda/?nc2=h_ql_prod_fs_lbd) 是实现 Amazon AppFlow 新连接器的唯一方式。
        - `IAMFullAccess`：SAM CLI 需要创建一个 `ConnectorFunctionRole` 以供连接器使用。

- 一个 [SalesForce](https://developer.salesforce.com) 账户。

## 第 1 步：注册 TiDB 连接器

### 克隆代码

克隆 [集成示例代码仓库](https://github.com/pingcap-inc/tidb-appflow-integration)，用于 TiDB 和 Amazon AppFlow：

```bash
git clone https://github.com/pingcap-inc/tidb-appflow-integration
```

### 构建并上传 Lambda

1. 构建包：

    ```bash
    cd tidb-appflow-integration
    mvn clean package
    ```

2. （可选）如果尚未配置 AWS 访问密钥 ID 和密钥，请进行配置。

    ```bash
    aws configure
    ```

3. 将 JAR 包作为 Lambda 上传：

    ```bash
    sam deploy --guided
    ```

    > **注意：**
    >
    > - `--guided` 选项会使用提示引导你完成部署。你的输入会被存储在配置文件中，默认为 `samconfig.toml`。
    > - `stack_name` 指定你要部署的 AWS Lambda 的名称。
    > - 该引导流程假设使用 AWS 作为 {{{ .starter }}} 的云提供商。若要使用 Amazon S3 作为源或目标，你需要将 AWS Lambda 的 `region` 设置为与 Amazon S3 相同。
    > - 如果你之前已运行过 `sam deploy --guided`，可以直接运行 `sam deploy`，SAM CLI 会使用 `samconfig.toml` 配置文件简化操作。

    如果看到类似如下的输出，说明 Lambda 已成功部署。

    ```
    Successfully created/updated stack - <stack_name> in <region>
    ```

4. 进入 [AWS Lambda 控制台](https://console.aws.amazon.com/lambda/home)，可以看到你刚刚上传的 Lambda。注意需要在右上角选择正确的区域。

    ![lambda dashboard](/media/develop/aws-appflow-step-lambda-dashboard.png)

### 使用 Lambda 注册连接器

1. 在 [AWS 管理控制台](https://console.aws.amazon.com)，导航到 [Amazon AppFlow > Connectors](https://console.aws.amazon.com/appflow/home#/gallery)，点击 **Register new connector**。

    ![register connector](/media/develop/aws-appflow-step-register-connector.png)

2. 在 **Register a new connector** 对话框中，选择你上传的 Lambda 函数，并用连接器名称指定连接器标签。

    ![register connector dialog](/media/develop/aws-appflow-step-register-connector-dialog.png)

3. 点击 **Register**。此时，TiDB 连接器注册成功。

## 第 2 步：创建数据流

导航到 [Amazon AppFlow > Flows](https://console.aws.amazon.com/appflow/home#/list)，点击 **Create flow**。

![create flow](/media/develop/aws-appflow-step-create-flow.png)

### 设置数据流名称

输入数据流名称，然后点击 **Next**。

![name flow](/media/develop/aws-appflow-step-name-flow.png)

### 设置源表和目标表

选择 **Source details** 和 **Destination details**。TiDB 连接器可以在两者中使用。

1. 选择源名称。本文以 **Salesforce** 作为示例源。

    ![salesforce source](/media/develop/aws-appflow-step-salesforce-source.png)

    注册到 Salesforce 后，Salesforce 会向你的平台添加一些示例数据。以下步骤将以 **Account** 对象作为示例源对象。

    ![salesforce data](/media/develop/aws-appflow-step-salesforce-data.png)

2. 点击 **Connect**。

    1. 在 **Connect to Salesforce** 对话框中，指定此连接的名称，然后点击 **Continue**。

        ![connect to salesforce](/media/develop/aws-appflow-step-connect-to-salesforce.png)

    2. 点击 **Allow**，确认 AWS 可以读取你的 Salesforce 数据。

        ![allow salesforce](/media/develop/aws-appflow-step-allow-salesforce.png)

    > **注意：**
    >
    > 如果你的公司已使用 Salesforce 的专业版，REST API 默认未启用。你可能需要注册一个新的开发者版以使用 REST API。更多信息，请参见 [Salesforce Forum Topic](https://developer.salesforce.com/forums/?id=906F0000000D9Y2IAK)。

3. 在 **Destination details** 区域，选择 **TiDB-Connector** 作为目标。此时会显示 **Connect** 按钮。

    ![tidb dest](/media/develop/aws-appflow-step-tidb-dest.png)

4. 在点击 **Connect** 之前，你需要在 TiDB 中创建一个 `sf_account` 表，用于存储 Salesforce 的 **Account** 对象。注意，此表结构与 [Amazon AppFlow 教程](https://docs.aws.amazon.com/appflow/latest/userguide/flow-tutorial-set-up-source.html) 中的示例数据不同。

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

5. `sf_account` 表创建完成后，点击 **Connect**。会显示连接对话框。

6. 在 **Connect to TiDB-Connector** 对话框中，输入 TiDB 集群的连接属性。如果使用 {{{ .starter }}} 集群，需要将 **TLS** 选项设置为 `Yes`，以启用 TLS 连接。然后点击 **Connect**。

    ![tidb connection message](/media/develop/aws-appflow-step-tidb-connection-message.png)

7. 现在可以获取你指定连接的数据库中的所有表。从下拉列表中选择 **sf_account** 表。

    ![database](/media/develop/aws-appflow-step-database.png)

    下图显示了将 Salesforce **Account** 对象中的数据传输到 TiDB 中 `sf_account` 表的配置示例：

    ![complete flow](/media/develop/aws-appflow-step-complete-flow.png)

8. 在 **Error handling** 区域，选择 **Stop the current flow run**。在 **Flow trigger** 区域，选择 **Run on demand** 触发类型，即需要手动运行数据流。然后点击 **Next**。

    ![complete step1](/media/develop/aws-appflow-step-complete-step1.png)

### 设置映射规则

将 Salesforce 中 **Account** 对象的字段映射到 TiDB 中的 `sf_account` 表，然后点击 **Next**。

- `sf_account` 表在 TiDB 中是新建且为空的。

    ```sql
    test> SELECT * FROM sf_account;
    +----+------+------+---------------+--------+----------+
    | id | name | type | billing_state | rating | industry |
    +----+------+------+---------------+--------+----------+
    +----+------+------+---------------+--------+----------+
    ```

- 设置映射规则时，可以在左侧选择源字段名，在右侧选择目标字段名，然后点击 **Map fields**，规则即被设置。

    ![add mapping rule](/media/develop/aws-appflow-step-add-mapping-rule.png)

- 本文档中需要的映射规则（源字段名 -> 目标字段名）包括：

    - Account ID -> id
    - Account Name -> name
    - Account Type -> type
    - Billing State/Province -> billing_state
    - Account Rating -> rating
    - Industry -> industry

    ![mapping a rule](/media/develop/aws-appflow-step-mapping-a-rule.png)

    ![show all mapping rules](/media/develop/aws-appflow-step-show-all-mapping-rules.png)

### （可选）设置过滤器

如果你想为数据字段添加过滤条件，可以在此设置。否则跳过此步骤，点击 **Next**。

![filters](/media/develop/aws-appflow-step-filters.png)

### 确认并创建数据流

确认即将创建的数据流信息。如果一切正常，点击 **Create flow**。

![review](/media/develop/aws-appflow-step-review.png)

## 第 3 步：运行数据流

在新建数据流的页面，点击右上角的 **Run flow**。

![run flow](/media/develop/aws-appflow-step-run-flow.png)

下图显示了数据流成功运行的示例：

![run success](/media/develop/aws-appflow-step-run-success.png)

查询 `sf_account` 表，即可看到 Salesforce **Account** 对象中的记录已写入其中：

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

## 重要事项

- 如果出现问题，可以在 [CloudWatch](https://console.aws.amazon.com/cloudwatch/home) 页面查看日志。
- 本文档中的步骤基于 [Building custom connectors using the Amazon AppFlow Custom Connector SDK](https://aws.amazon.com/blogs/compute/building-custom-connectors-using-the-amazon-appflow-custom-connector-sdk/)。
- [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) **不是** 生产环境。
- 为了避免篇幅过长，本文中的示例仅展示了 `Insert` 策略，但 `Update` 和 `Upsert` 策略也已测试，可以使用。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>