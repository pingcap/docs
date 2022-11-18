---
title: Integrate TiDB with AWS AppFlow
summary: Introduce how to integrate TiDB with AWS AppFlow step by step.
---

# Integrate TiDB with AWS AppFlow

This document describes how to integrate **TiDB Serverless Tier**  with **AWS AppFlow**.

## Prerequisites

- [Git](https://git-scm.com/)
- [JDK](https://openjdk.org/install/) (version `11` and above)
- [Maven](https://maven.apache.org/install.html) (version `3.8` and above)
- [AWS CLI](https://docs.aws.amazon.com/zh_cn/cli/latest/userguide/getting-started-install.html) (version `2.x`)
- [SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html) (version `1.58.0` and above)
- An AWS [IAM users](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users.html)

    - User credentials have [access keys](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html) way
    - Permissions

        - AWSCertificateManagerFullAccess: For writing and reading the[AWS Secrets Manager](https://aws.amazon.com/secrets-manager/).
        - AWSCloudFormationFullAccess: `SAM CLI` using[AWS CloudFormation](https://aws.amazon.com/cloudformation/) to proclaim the AWS resources.
        - AmazonS3FullAccess: `AWS CloudFormation` uses[AWS S3](https://aws.amazon.com/s3/?nc2=h_ql_prod_fs_s3) to publish. So we need to grant `AWS S3` permissions too.
        - AWSLambda_FullAccess: Currently,[AWS Lambda](https://aws.amazon.com/lambda/?nc2=h_ql_prod_fs_lbd) is the only way to implement a new connector for[AWS AppFlow](https://aws.amazon.com/appflow/).
        - IAMFullAccess: `SAM CLI` needs to create a `ConnectorFunctionRole` to this connector.

    - Permissions Preview:

        ![aws auth](/media/develop/aws-appflow-step-auth.png)

- [SalesForce](https://www.google.com/url?q=https://developer.salesforce.com/signup&sa=D&source=editors&ust=1668768302206671&usg=AOvVaw0sf63USux4lVz5_f88q5M5) account

## Register a TiDB Connector

### Clone the Code

This is the code repository. I adapted TLS connection for TiDB Serverless Tier.

```bash
git clone https://github.com/pingcap-inc/tidb-appflow-integration
```

### Build and Upload a Lambda

Build:

```bash
cd tidb-appflow-integration
mvn clean package
```

(Optional) If it is the first time to use AWS CLI, you need to configure it with your AWS Access key ID and Secret access key.

```bash
aws configure
```

Upload your JAR package as a Lambda:

```bash
sam deploy --guided
```

> **Note:**
>
> - `--guided` option will ask you some questions at the terminal. The answer will be stored in a file. The default name is `samconfig.toml`.
> - `stack_name` refers to the name of `AWS Lambda`. You can type what you want to call this service.
> - If you want to use `AWS S3` as the source or destination, you need to set the `region` of `AWS Lambda` as the same as `AWS S3`.
> - If you already run the `sam deploy --guided`. Next time, you can just run `sam deploy` instead, `SAM CLI` will use the config file `samconfig.toml` to simplify the interaction.

If you can see the output log below. You successfully deployed this Lambda.

```
Successfully created/updated stack - <stack_name> in <region>
```

![sam output](/media/develop/aws-appflow-step-sam-putput.png)

And you can see the [Lambda Dashboard](https://us-west-2.console.aws.amazon.com/lambda/home). It will appear you uploaded Lambda just now (Don't forget to select the correct region).

![lambda dashboard](/media/develop/aws-appflow-step-lambda-dashboard.png)

### Using Lambda to Register a Connector

> **Note:**
> 
> From here, we can just use the [AWS Console](https://console.aws.amazon.com). It's super handy.

Open your [AWS AppFlow Connectors](https://console.aws.amazon.com/appflow/home#/gallery) website, and click the "**Register new connector**" button.

![register connector](/media/develop/aws-appflow-step-register-connector.png)

You need to choose the Lambda you uploaded. And give your connector an epic name ("**Connector label**" just refers to the name of connector).

![register connector dialog](/media/develop/aws-appflow-step-register-connector-dialog.png)

Click "**Register**". Then you register a TiDB connector successfully.

## Using the TiDB Connector to Create a Flow

Open your [AWS AppFlow Flows](https://console.aws.amazon.com/appflow/home#/list) website, and click the "**Create flow**" button.

![create flow](/media/develop/aws-appflow-step-create-flow.png)

### Set the Name of Flow

In step 1, you need to name this flow, and click the "**Next**" button.

![name flow](/media/develop/aws-appflow-step-name-flow.png)

### Set the Source and Destination tables

In step 2, you need to choose the **Source Details** and **Destination details**. TiDB Connector can be used in both of them.

- Let’s select Salesforce as the data source.

    ![salesforce source](/media/develop/aws-appflow-step-salesforce-source.png)

- If you register to Salesforce, they will add some example data in your platform. We can use the "**Account**" objects.

    ![salesforce data](/media/develop/aws-appflow-step-salesforce-data.png)

- Give this connection a name and click the "**Continue**" button.

    ![connect to salesforce](/media/develop/aws-appflow-step-connect-to-salesforce.png)

- And then, you need to click the "**Allow**" button, to confirm that AWS reads your Salesforce data.

    ![allow salesforce](/media/develop/aws-appflow-step-allow-salesforce.png)

> **Note:**
>
> If your company already used the Professional Edition of Salesforce, the REST API is not enabled for defaultly. You might need to register a new Developer Edition to use the REST API. You can get more information at this [Salesforce Forum Topic](https://developer.salesforce.com/forums/?id=906F0000000D9Y2IAK).

- Choose the TiDB Connector at Destination details. A button will appear, named "**Connect**".

    ![tidb dest](/media/develop/aws-appflow-step-tidb-dest.png)

> **Note:**
>
> If you don't have a TiDB Cluster, get a [Serverless Tier](https://tidbcloud.com/console/clusters) here. It's free. And just need 3 minutes to create. We used AWS to provide TiDB Cloud Serverless Tier. You can choose the same region as Lambda to speed up the connections.

- Before connecting, you need to create a table at TiDB. Let’s run a SQL at TiDB Serverless Tier (This table schema from the sample data in [Tutorial of AWS AppFlow](https://docs.aws.amazon.com/appflow/latest/userguide/flow-tutorial-set-up-source.html)).

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

- When the SQL runs successfully, you can click the "**Connect**" button.
- In this dialog, you need to input the connection properties of the TiDB Cluster. If you are using [TiDB Cloud Serverless Tier](https://tidbcloud.com/console/clusters). You need to select the "**TLS**" option to Yes.  It can let the TiDB Connector use TLS connections. And click "**Connect**".

    ![tidb connection message](/media/develop/aws-appflow-step-tidb-connection-message.png)

- Then, you'll get all the tables in the database that you specified in the last step.

    ![database](/media/develop/aws-appflow-step-database.png)

- I'll transfer data from the Salesforce Account Objects to the TiDB Serverless Tier table "sf_account". So the configurations are like this.

    ![complete flow](/media/develop/aws-appflow-step-complete-flow.png)

- We select "**Stop the current flow run**" when errors occur. And the "**Run on demand**" trigger type, means you need to click a button to run it.

    ![complete step1](/media/develop/aws-appflow-step-complete-step1.png)

### Set the Mapping Rules

In step 3, you need to map the fields.

- We just created the sf_account table. So, it’s empty.

    ```sql
    test> select * from sf_account;
    +----+------+------+---------------+--------+----------+
    | id | name | type | billing_state | rating | industry |
    +----+------+------+---------------+--------+----------+
    +----+------+------+---------------+--------+----------+
    ```

- We need to build a bunch of mapping rules. You can select a source field name option on the left, and select a destination field name on the right. Then, click the "**Map fields**" button. In that way, you can get a mapping rule.

    ![add mapping rule](/media/develop/aws-appflow-step-add-mapping-rule.png)

- We need add these rules:

    - Account ID -> id
    - Account Name -> name
    - Account Type -> type
    - Billing State/Province -> billing_state
    - Account Rating -> rating
    - Industry -> industry

    ![mapping a rule](/media/develop/aws-appflow-step-mapping-a-rule.png)

    ![show all mapping rules](/media/develop/aws-appflow-step-show-all-mapping-rules.png)

### (Optional) Set Filters

In step 4, we don't need any filter. But if you want, you can add some filters here.

![filters](/media/develop/aws-appflow-step-filters.png)

### Review and Create the Flow

This step is for review. You can check it, and click the "**Create flow**" button.

![review](/media/develop/aws-appflow-step-review.png)

## Run the Flow

Click the "**Run flow**" button.

![run flow](/media/develop/aws-appflow-step-run-flow.png)

Run successfully.

![run success](/media/develop/aws-appflow-step-run-success.png)

Let's query the `sf_account` table.

```sql
test> select * from sf_account;
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

Records are written on it.

## Noteworthy Things

- If something goes wrong, you can see the [AWS CloudWatch](https://console.aws.amazon.com/cloudwatch/home) to get some logs.
- These steps are based on this [AWS Blog](https://aws.amazon.com/blogs/compute/building-custom-connectors-using-the-amazon-appflow-custom-connector-sdk/).
- [TiDB Cloud Serverless Tier](https://docs.pingcap.com/tidbcloud/select-cluster-tier#serverless-tier-beta) is **NOT** a production environment.
- Just show the `Insert` strategy above, preventing excessive length. But `Update` and `Upsert` strategies were also tested.