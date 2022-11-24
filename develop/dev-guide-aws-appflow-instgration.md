---
title: Integrate TiDB with Amazon AppFlow
summary: Introduce how to integrate TiDB with Amazon AppFlow step by step.
---

# Integrate TiDB with Amazon AppFlow

This document describes how to integrate TiDB with Amazon AppFlow and takes a TiDB Cloud Serverless Tier cluster as an example.

## Prerequisites

- [Git](https://git-scm.com/)
- [JDK](https://openjdk.org/install/) 11 or above
- [Maven](https://maven.apache.org/install.html) 3.8 or above
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) Version 2
- [AWS Serverless Application Model Command Line Interface (AWS SAM CLI)](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html) 1.58.0 or above
- An AWS [Identity and Access Management (IAM) user](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users.html) with the following requirements:

    - The user can access AWS using an [access key](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html).
    - The user has the following permissions:

        - `AWSCertificateManagerFullAccess`: used for reading and writing the [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/).
        - `AWSCloudFormationFullAccess`: SAM CLI uses [AWS CloudFormation](https://aws.amazon.com/cloudformation/) to proclaim the AWS resources.
        - `AmazonS3FullAccess`: AWS CloudFormation uses [AWS S3](https://aws.amazon.com/s3/?nc2=h_ql_prod_fs_s3) to publish.
        - `AWSLambda_FullAccess`: currently, [AWS Lambda](https://aws.amazon.com/lambda/?nc2=h_ql_prod_fs_lbd) is the only way to implement a new connector for Amazon AppFlow.
        - `IAMFullAccess`: SAM CLI needs to create a `ConnectorFunctionRole` to the connector.

    - Permissions Preview:

        ![aws auth](/media/develop/aws-appflow-step-auth.png)

- A [SalesForce](https://developer.salesforce.com) account.

## Step 1. Register a TiDB connector

### Clone the code
```bash
git clone https://github.com/pingcap-inc/tidb-appflow-integration
```

### Build and upload a Lambda

1. Build:

    ```bash
    cd tidb-appflow-integration
    mvn clean package
    ```

2. (Optional) You need to configure your AWS access key ID and secret access key if you haven't.

    ```bash
    aws configure
    ```

3. Upload your JAR package as a Lambda:

    ```bash
    sam deploy --guided
    ```

    > **Note:**
    >
    > - `--guided` option will ask you some questions at the terminal. The answer will be stored in a file. The default name is `samconfig.toml`.
    > - `stack_name` refers to the name of AWS Lambda. You can type what you want to call this service.
    > - If you want to use AWS S3 as the source or destination, you need to set the `region` of AWS Lambda as the same as AWS S3.
    > - If you already run the `sam deploy --guided`. Next time, you can just run `sam deploy` instead, SAM CLI will use the config file `samconfig.toml` to simplify the interaction.

    If you see a similar output as follows, this Lambda is successfully deployed.
    
    ```
    Successfully created/updated stack - <stack_name> in <region>
    ```
    Then you can see the [Lambda Dashboard](https://us-west-2.console.aws.amazon.com/lambda/home). It will appear you uploaded Lambda just now (Don't forget to select the correct region).
    
    ![lambda dashboard](/media/develop/aws-appflow-step-lambda-dashboard.png)

### Using Lambda to register a connector

> **Note:**
> 
> The following operations are on [AWS Console](https://console.aws.amazon.com), which is super handy.

Navigate to [Amazon AppFlow > Connectors](https://console.aws.amazon.com/appflow/home#/gallery) and click **Register new connector**.

![register connector](/media/develop/aws-appflow-step-register-connector.png)

In the **Register a new connector** dialog, choose the Lambda function you uploaded and specify the connector label, which is the name of the connector.

![register connector dialog](/media/develop/aws-appflow-step-register-connector-dialog.png)

Click **Register** and then a TiDB connector is registered successfully.

## Step 2. Using the TiDB connector to create a flow

Navigate to [Amazon AppFlow > Flows](https://console.aws.amazon.com/appflow/home#/list) and click **Create flow**.

![create flow](/media/develop/aws-appflow-step-create-flow.png)

### Set the flow name

In **Step 1**, you need to enter the flow name and then click **Next**.

![name flow](/media/develop/aws-appflow-step-name-flow.png)

### Set the source and destination tables

In **Step 2**, you need to choose the **Source details** and **Destination details**. TiDB connector can be used in both of them.

- The following uses **Salesforce** as the source.

    ![salesforce source](/media/develop/aws-appflow-step-salesforce-source.png)

- If you register to Salesforce, Salesforce will add some example data to your platform. The **Account** objects can be used in the following examples.

    ![salesforce data](/media/develop/aws-appflow-step-salesforce-data.png)

- Click **Connect**. In the **Connect to Salesforce** dialog, specify the name of this connection and then click **Continue**.

    ![connect to salesforce](/media/develop/aws-appflow-step-connect-to-salesforce.png)

- Click **Allow** to confirm that AWS can read your Salesforce data.

    ![allow salesforce](/media/develop/aws-appflow-step-allow-salesforce.png)

> **Note:**
>
> If your company already used the Professional Edition of Salesforce, the REST API is not enabled by default. You might need to register a new Developer Edition to use the REST API. For more information, refer to [Salesforce Forum Topic](https://developer.salesforce.com/forums/?id=906F0000000D9Y2IAK).

- In the **Destination details** tab, choose the TiDB-Connector as the destination and the **Connect** will appear.

    ![tidb dest](/media/develop/aws-appflow-step-tidb-dest.png)

> **Note:**
>
> If you do not have a TiDB cluster, you can create a [Serverless Tier](https://tidbcloud.com/console/clusters) cluster, which is free and can be created in approximately 30 seconds. This guide uses AWS as the cloud provider of TiDB Cloud Serverless Tier. To speed up the connection, you can choose the same region as Lambda.

- Before connecting, you need to create a table at TiDB. Let’s run a SQL at TiDB Serverless Tier (This table schema from the sample data in [Tutorial of Amazon AppFlow](https://docs.aws.amazon.com/appflow/latest/userguide/flow-tutorial-set-up-source.html)).

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

- After executing the preceding statement and creating the `sf_account` table, you can click **Connect**.
- In this dialog, you need to enter the connection properties of the TiDB cluster. If you use a TiDB Cloud Serverless Tier cluster, you need to enable the **TLS** option and set it to `Yes`, which lets the TiDB connector use the TLS connection. Then, click **Connect**.

    ![tidb connection message](/media/develop/aws-appflow-step-tidb-connection-message.png)

- Then, you can get all tables in the database that you specified in the last step.

    ![database](/media/develop/aws-appflow-step-database.png)

- The following configuration shows transferring data from the Salesforce **Account** objects to the `sf_account` table in TiDB:

    ![complete flow](/media/develop/aws-appflow-step-complete-flow.png)

- In the **Error handling** tab, choose **Stop the current flow run**. In the **Flow trigger** tab, choose the **Run on demand** trigger type, which means you need to run the flow manually.

    ![complete step1](/media/develop/aws-appflow-step-complete-step1.png)

### Set mapping rules

In **Step 3**, you need to map the fields.

- The `sf_account` table is newly created and it is empty.

    ```sql
    test> SELECT * FROM sf_account;
    +----+------+------+---------------+--------+----------+
    | id | name | type | billing_state | rating | industry |
    +----+------+------+---------------+--------+----------+
    +----+------+------+---------------+--------+----------+
    ```

- To set a mapping rule, you can select a source field name on the left, and select a destination field name on the right. Then click **Map fields** and a rule is set.

    ![add mapping rule](/media/develop/aws-appflow-step-add-mapping-rule.png)

- The following rules (Source field name -> Destination field name) are needed in this documentation:

    - Account ID -> id
    - Account Name -> name
    - Account Type -> type
    - Billing State/Province -> billing_state
    - Account Rating -> rating
    - Industry -> industry

    ![mapping a rule](/media/develop/aws-appflow-step-mapping-a-rule.png)

    ![show all mapping rules](/media/develop/aws-appflow-step-show-all-mapping-rules.png)

### (Optional) Set filters

In **Step 4**, there is no filter needed in this documentation. But if you want, you can add some filters here.

![filters](/media/develop/aws-appflow-step-filters.png)

### Review and Create the Flow

This step is to confirm the information of the flow to be created. After confirming, click **Create flow**.

![review](/media/develop/aws-appflow-step-review.png)

## Step 3. Run the flow

Click **Run flow** in the upper-right corner of the newly created flow page.

![run flow](/media/develop/aws-appflow-step-run-flow.png)

The following diagram shows an example when the flow runs successfully:

![run success](/media/develop/aws-appflow-step-run-success.png)

Query the `sf_account` table and you can see that the records have been written to it.


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
## Noteworthy Things

- If something goes wrong, you can navigate to [CloudWatch](https://console.aws.amazon.com/cloudwatch/home) page on the AWS Management console to get logs.
- These steps are based on [Building custom connectors using the Amazon AppFlow Custom Connector SDK](https://aws.amazon.com/blogs/compute/building-custom-connectors-using-the-amazon-appflow-custom-connector-sdk/).
- [TiDB Cloud Serverless Tier](https://docs.pingcap.com/tidbcloud/select-cluster-tier#serverless-tier-beta) is **NOT** a production environment.
- To prevent excessive length, the preceding examples only show the `Insert` strategy, but `Update` and `Upsert` strategies are also tested.