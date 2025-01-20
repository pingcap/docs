---
title: Integrate TiDB Cloud Serverless with Amazon Lambda Using AWS CloudFormation
summary: Introduce how to integrate TiDB with Amazon Lambda and CloudFormation step by step.
---

# Integrate TiDB Cloud Serverless with Amazon Lambda Using AWS CloudFormation

This document provides a step-by-step guide on how to use [AWS CloudFormation](https://aws.amazon.com/cloudformation/) to integrate [TiDB Cloud Serverless](https://www.pingcap.com/tidb-cloud/), a cloud-native distributed SQL database, with [Amazon Lambda](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html), a serverless amd event-driven compute service. By integrating TiDB Cloud Serverless with Amazon Lambda, you can leverage the scalability and cost-efficiency of microservices through TiDB Cloud Serverless and AWS Lambda.

Integrating these services allows you to build serverless and event-driven microservices that enhance scalability and cost-effectiveness. AWS CloudFormation automates the creation and management of AWS resources, including Lambda functions, API Gateway, and Secrets Manager.

## Solution overview

In this guide, you will create a fully functional online bookshop.

The project consists of the following components:

- AWS Lambda Function: handles requests and queries data from a TiDB Cloud Serverless cluster using Sequelize ORM and Fastify API framework.
- AWS Secrets Manager SDK: retrieves and manages connection configurations for the TiDB Cloud Serverless cluster.
- AWS API Gateway: handles HTTP request routes.
- TiDB Cloud Serverless: a cloud-native distributed SQL database.

AWS CloudFormation is used to create the necessary resources for the project, including the Secrets Manager, API Gateway, and Lambda Functions.

The structure of the project is as follows:

![aws-lambda-structure-overview](/media/develop/aws-lambda-structure-overview.png)

## Prerequisites

Before getting started, ensure that you have the following:

- An AWS account
- Access to the following AWS services:
    - [AWS CloudFormation](https://aws.amazon.com/cloudformation/)
    - [Secrets Manager](https://aws.amazon.com/secrets-manager/)
    - [API Gateway](https://aws.amazon.com/api-gateway/)
    - [Lambda services](https://aws.amazon.com/lambda/)
    - [S3](https://aws.amazon.com/s3/)
    - [IAM Roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html)
- A [TiDB Cloud](https://tidbcloud.com) account and a TiDB Cloud Serverless cluster. Get the connection information for your TiDB Cloud Serverless:

    ![TiDB Cloud connection information](/media/develop/aws-lambda-tidbcloud-connection-info.png)

- API test tools such as [Postman](https://www.postman.com/) and [cURL](https://curl.se/). Most examples in this document use cURL. For Windows users, Postman is recommended.
- Download the [latest release assets](https://github.com/pingcap/TiDB-Lambda-integration/releases/latest) of the project to your local machine, which includes `cloudformation_template.yml` and `cloudformation_template.json` files.

> **Note:**
>
> - When you create the AWS resources, it is recommended to use `us-east-1` as your cluster region . This is because the Lambda function code in this demo hardcodes the region as `us-east-1`, and the code bundle is stored in the `us-east-1` region. 
> - If you use a different region, you need to modify the Lambda function code, rebuild and upload the code bundle to your own S3 bucket.

### Modify and rebuild the Lambda function code if necessary

If you use `us-east-1` as your cluster region, skip this section and go to [Step 1: Set up the project using AWS CloudFormation](#step-1-set-up-the-project-using-aws-cloudformation).

If you use a different AWS region other than `us-east-1` to create the AWS resources, you need to modify the Lambda function code, rebuild and upload the code bundle to your own S3 bucket.

To avoid local development environment issues, it is recommended that you use a cloud-native development environment, such as [Gitpod](https://www.gitpod.io/).

To rebuild and upload the code bundle to your own S3 bucket, do the following:

1. Initialize the development environment.

    - Open the [Gitpod](https://gitpod.io/#/https://github.com/pingcap/TiDB-Lambda-integration) workspace and log in with your GitHub account.

2. Modify the Lambda function code.

    1. Open the `aws-lambda-cloudformation/src/secretManager.ts` file in the left sidebar.
    2. Locate the line 22 and then modify the `region` variable to use your own region.

3. Rebuild the code bundle.

    1. Install the dependencies.

        1. Open the Gitpod terminal.
        2. Enter the working directory:

            ```shell
            cd aws-lambda-cloudformation
            ```

        3. Install the dependencies:

            ```shell
            yarn
            ```

    2. Rebuild the code bundle.

        1. Build the code bundle.

            ```shell
            yarn build
            ```

        2. Check the `aws-lambda-cloudformation/dist/index.zip` file.
        3. Right-click the `index.zip` file and select **Download**.

4. Upload the rebuilt code bundle to your own S3 bucket.

    1. Visit the [S3 service](https://console.aws.amazon.com/s3) in the AWS Management Console.
    2. Create a new bucket in your selected region.
    3. Upload the `index.zip` file to the bucket.
    4. Note down the S3 bucket name and region for later use.

## Step 1: Set up the project using AWS CloudFormation

To set up the bookshop project using AWS CloudFormation, do the following:

1. Navigate to the AWS Management Console and access the [AWS CloudFormation service](https://console.aws.amazon.com/cloudformation).
2. Click **Create Stack** > **With new resources (standard)**.
3. On the **Create Stack** settings page, complete the stack creation process.

    1. In the **Prerequisite** panel, select **Template is ready**.
    2. Upload the template file (either YAML or JSON), and click **Next**.

        If you do not have the file yet, download it from [GitHub](https://github.com/pingcap/TiDB-Lambda-integration/releases/latest). The file contains the AWS CloudFormation template that creates the necessary resources for the project.

        ![aws-lambda-cf-create-stack](/media/develop/aws-lambda-cf-create-stack.png)

    3. Specify stack details.

        - If you use `us-east-1` as your cluster region, fill in the fields as in the following screenshot:

            ![aws-lambda-cf-stack-details](/media/develop/aws-lambda-cf-stack-config.png)

            - **Stack name**: enter the stack name.
            - **S3Bucket**: enter the S3 bucket where you store the zip file.
            - **S3Key**: enter the S3 key.
            - **TiDBDatabase**: enter the TiDB Cloud cluster name.
            - **TiDBHost**: enter the host URL for TiDB Cloud database access. Enter `localhost`.
            - **TiDBPassword**: enter the password for TiDB Cloud database access.
            - **TiDBPort**: enter the port for TiDB Cloud database access.
            - **TiDBUser**: enter the user name for TiDB Cloud database access.

        - If you use a different AWS region other than `us-east-1`, follow these steps:

            1. Refer to [Modify and rebuild the Lambda function code if necessary](#modify-and-rebuild-the-lambda-function-code-if-necessary) to modify the Lambda function code, rebuild and upload the code bundle to your own S3 bucket.
            2. In the stack details fields, specify the S3 bucket name and region in the `S3Bucket` and `S3Key` parameters according to your own configuration.
            3. Fill in other fields as in the preceding screenshot.

## Step 2: Use the project

After the stack has been created, you can use the project as follows:

1. Visit the [API Gateway service](https://console.aws.amazon.com/apigateway) in the AWS Management Console and click the `TiDBCloudApiGatewayV2` API.

2. Copy the `Invoke URL` from the **Overview** page. This URL serves as the API endpoint.

    ![api-gateway-invoke-url](/media/develop/aws-lambda-get-apigateway-invoke-url.png)

3. Use API test tools such as Postman and cURL to test the API:

    - Init mock books:

        ```shell
        curl -X POST -H "Content-Type: application/json" -d '{"count":100}' https://<your-api-endpoint>/book/init
        ```

    - Get all books:

        ```shell
        curl https://<your-api-endpoint>/book
        ```

    - Get a book by ID:

        ```shell
        curl https://<your-api-endpoint>/book/<book-id>
        ```

    - Create a book:

        ```shell
        curl -X POST -H "Content-Type: application/json" -d '{ "title": "Book Title", "type": "Test", "publishAt": "2022-12-15T21:01:49.000Z", "stock": 123, "price": 12.34, "authors": "Test Test" }' https://  <your-api-endpoint>/book
        ```

    - Update a book:

        ```shell
        curl -X PUT -H "Content-Type: application/json" -d '{ "title": "Book Title(updated)" }' https://<your-api-endpoint>/book/<book-id>
        ```

    - Delete a book:

        ```shell
        curl -X DELETE https://<your-api-endpoint>/book/<book-id>
        ```

## Step 3: Clean up resources

To avoid unnecessary charges, you can clean up any resources that have been created.

To do so, access the [AWS Management Console](https://console.aws.amazon.com/cloudformation) and delete the AWS CloudFormation stack.
