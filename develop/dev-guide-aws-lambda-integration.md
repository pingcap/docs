---
title: Integrate TiDB Cloud Serverless with Amazon Lambda using AWS CloudFormation
summary: Introduce how to integrate TiDB with Amazon Lambda and CloudFormation step by step.
---

# Integrate TiDB Cloud Serverless with Amazon Lambda using AWS CloudFormation

## Introduction

This document provides a step-by-step guide on how to use [AWS CloudFormation](https://aws.amazon.com/cloudformation/) to integrate [TiDB Cloud Serverless](https://www.pingcap.com/tidb-cloud/), a cloud-native distributed SQL database, with Amazon Lambda, a serverless event-driven compute service. Integrating these services allows you to build serverless, event-driven microservices that enhance scalability and cost-effectiveness. AWS CloudFormation automates the creation and management of AWS resources, including Lambda functions, API Gateway, and Secrets Manager.

The document is organized into the following sections:

1. [Solution Overview](#solution-overview)
2. [Prerequisites](#prerequisites)
3. [Setting up the Demo using CloudFormation](#set-up-the-demo-using-cloudformation)
4. [Using the Demo](#use-the-demo)
5. [Cleaning up](#clean-up)
6. [Conclusion](#conclusion)

## Solution Overview

In this guide, you will create a fully-functional online bookshop. 

The project consists of the following components:

- AWS Lambda Function: Handles requests and queries data from the TiDB Cloud Serverless database using Sequelize ORM and Fastify API framework
- AWS Secrets Manager SDK: Retrieves and manages connection configurations for the TiDB Cloud Serverless database
- AWS API Gateway: Handles HTTP request routes
- TiDB Cloud Serverless: A cloud-native distributed SQL database

CloudFormation is used to create the necessary resources for the demo, including the Secrets Manager, API Gateway, and Lambda Functions.

Finally, the following diagram shows the structure of the demo:

![aws-lambda-structure-overview](/media/develop/aws-lambda-structure-overview.png)

## Prerequisites

Before getting started, ensure you have the following:

- An AWS account
- Access to [AWS CloudFormation](https://aws.amazon.com/cloudformation/), [Secrets Manager](https://aws.amazon.com/secrets-manager/), [API Gateway](https://aws.amazon.com/api-gateway/), [Lambda services](https://aws.amazon.com/lambda/), [S3](https://aws.amazon.com/s3/), and [IAM Roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html)
- A [TiDB Cloud](https://tidbcloud.com) account and a TiDB Cloud Serverless cluster
    - Get TiDB Connection Information
        ![tidbcloud-connection-info](/media/develop/aws-lambda-tidbcloud-connection-info.png)
- API test tools like [`Postman`](https://www.postman.com/) or [`cURL`](https://curl.se/). Most of the examples in this document use `cURL`, if you are using MS Windows, `Postman` is recommended.
- Download the [latest release assets](https://github.com/pingcap/TiDB-Lambda-integration/releases/latest) of the demo project to your local machine, which includes `cloudformation_template.yml` and `cloudformation_template.json` files.

<Note>
When you create the AWS resources, use `us-east-1` as your cluster region is recommended. This is because the Lambda function code in this demo hardcodes the region as `us-east-1`, and the code bundle is stored in the `us-east-1` region.

If you use a different region, you need to modify the Lambda function code, re-build and re-upload the code bundle to your own S3 bucket.
</Note>

### Modify and rebuild the Lambda Function Code if necessary

If you use `us-east-1` as your cluster region, skip this section and go to [Set up the Demo using CloudFormation](#set-up-the-demo-using-cloudformation).

If you use a different AWS region other than `us-east-1` to create the AWS resources, you need to modify the Lambda function code, re-build and re-upload the code bundle to your own S3 bucket.

<Tip>
To avoid local development environment issues, it is recommended that you use a cloud-native development environment, such as [Gitpod](https://www.gitpod.io/).
</Tip>

1. Initialize the development environment

    - Open the [Gitpod](https://gitpod.io/#/https://github.com/pingcap/TiDB-Lambda-integration) workspace and log in with your GitHub account

2. Modify the Lambda function code

    1. Open the `aws-lambda-cloudformation/src/secretManager.ts` file in the left sidebar
    2. Modify the line#22 `region` variable to use your own region

3. Re-build the code bundle:

    1. Install the dependencies
        1. Open the Gitpod terminal.
        2. Enter the working directory:

            ```shell
            cd aws-lambda-cloudformation
            ```

        3. Install the dependencies:

            ```shell
            yarn
            ```

    2. Re-build the code bundle
        1. Build the code bundle

            ```shell
            yarn build
            ```

        2. Check the `aws-lambda-cloudformation/dist/index.zip` file.
        3. Right click the `index.zip` file and select **Download**.

4. Upload the re-built code bundle to your own S3 bucket.

    1. Visit the [S3 service](https://console.aws.amazon.com/s3) in the AWS Management Console.
    2. Create a new bucket in your selected region
    3. Upload the `index.zip` file to the bucket
    4. Note down the S3 bucket name and region

## Set up the Demo using CloudFormation

To set up the bookshop demo using CloudFormation, follow these steps:

1. Navigate to the AWS Management Console and access the [CloudFormation service](https://console.aws.amazon.com/cloudformation).
2. Click **Create Stack**.
3. In the **Create Stack** settings page, complete the stack creation process.

    1. In the **Prerequisite** panel, select **Template is ready**.
    2. Upload a template file (either YAML or JSON).

        If you do not have the file yet, download it from [GitHub](https://github.com/pingcap/TiDB-Lambda-integration/releases/latest). The file contains the CloudFormation template that creates the necessary resources for the demo. 

        ![aws-lambda-cf-create-stack](/media/develop/aws-lambda-cf-create-stack.png)
        
    3. Specify stack details
        - If you use `us-east-1` as your cluster region, fill out the fields as in the following image:
        
            ![aws-lambda-cf-stack-details](/media/develop/aws-lambda-cf-stack-config.png)

        - If you use a different AWS region other than `us-east-1`, follow [this section](#modify-and-rebuild-the-lambda-function-code-if-necessary) to modify the Lambda function code, re-build and re-upload the code bundle to your own S3 bucket. Specify the S3 bucket name and region in the `S3Bucket` and `S3Key` parameters according to your own configuration.

## Use the Demo

Once the stack has been created, you can use the demo as follows:

1. Visit the [API Gateway service](https://console.aws.amazon.com/apigateway) in the AWS Management Console and click on the `TiDBCloudApiGatewayV2` API
2. Copy the `Invoke URL` from the **Overview** page, which serves as the API endpoint.

    ![api-gateway-invoke-url](/media/develop/aws-lambda-get-apigateway-invoke-url.png)

3. Use API test tools like Postman or cURL to test the API:
    - Init mock books
        - `curl -X POST -H "Content-Type: application/json" -d '{"count":100}' https://<your-api-endpoint>/book/init`
    - Get all books
        - `curl https://<your-api-endpoint>/book`
    - Get a book by ID
        - `curl https://<your-api-endpoint>/book/<book-id>`
    - Create a book
        - `curl -X POST -H "Content-Type: application/json" -d '{ "title": "Book Title", "type": "Test", "publishAt": "2022-12-15T21:01:49.000Z", "stock": 123, "price": 12.34, "authors": "Test Test" }' https://  <your-api-endpoint>/book`
    - Update a book
        - `curl -X PUT -H "Content-Type: application/json" -d '{ "title": "Book Title(updated)" }' https://<your-api-endpoint>/book/<book-id>`
    - Delete a book
        - `curl -X DELETE https://<your-api-endpoint>/book/<book-id>`

## Clean up

To avoid unnecessary charges, you can follow these steps to clean up any resources that have been created:

- Delete the CloudFormation stack in the [AWS Management Console](https://console.aws.amazon.com/cloudformation)

## Conclusion

In this document, we have provided a comprehensive guide on using AWS CloudFormation to integrate TiDB Cloud Serverless with Amazon Lambda. By following this guide, you can leverage the scalability and cost-effectiveness of serverless, event-driven microservices using TiDB Cloud Serverless and AWS Lambda.
