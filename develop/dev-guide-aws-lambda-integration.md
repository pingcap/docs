---
title: Integrate TiDB Cloud Serverless with Amazon Lambda using AWS CloudFormation
summary: Introduce how to integrate TiDB with Amazon Lambda and CloudFormation step by step.
---

# Integrate TiDB Cloud Serverless with Amazon Lambda using AWS CloudFormation

## Introduction

This document provides a step-by-step guide on how to use [AWS CloudFormation](https://aws.amazon.com/cloudformation/) to integrate [TiDB Cloud Serverless](https://www.pingcap.com/tidb-cloud/), a cloud-native distributed SQL database, with Amazon Lambda, a serverless event-driven compute service. Integrating these services allows you to build serverless, event-driven microservices that enhance scalability and cost-effectiveness. AWS CloudFormation automates the creation and management of AWS resources, including Lambda functions, API Gateway, and Secrets Manager.

The document is organized into the following sections:

1. [Prerequisites](#prerequisites)
2. [Solution Overview](#solution-overview)
3. [Setting up the Demo using CloudFormation](#setting-up-the-demo-using-cloudformation)
4. [Using the Demo](#using-the-demo)
5. [Cleaning up](#cleaning-up)
6. [Conclusion](#conclusion)

## Solution Overview

This guide demonstrates how to use AWS CloudFormation to create a fully-functional online bookshop using TiDB Cloud Serverless as the database-as-a-service (DBaaS). The Secrets Manager service stores database-related details, the API Gateway handles HTTP request routes, and Lambda Functions process requests and query data from the TiDB Cloud Serverless database.

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
- Download the [latest release assets](https://github.com/pingcap/TiDB-Lambda-integration/releases/latest) to your local machine, which includes `cloudformation_template.yml` and `cloudformation_template.json` files.

<Note>
When you create the AWS resources, use `us-east-1` as your cluster region is recommended. This is because the Lambda function code in this demo hardcodes the region as `us-east-1`, and the code bundle is stored in the `us-east-1` region.

If you use a different region, you need to modify the Lambda function code, re-build and re-upload the code bundle to your own S3 bucket.
</Note>

### Modify and rebuild the Lambda Function Code if necessary

If you use a different AWS region other than `us-east-1` to create the AWS resources, you need to modify the Lambda function code, re-build and re-upload the code bundle to your own S3 bucket.

To avoid local development environment issues, we recommend you to cloudnative development environment, such as [Gitpod](https://www.gitpod.io/).

- Initialize the development environment
    - Open the [Gitpod](https://gitpod.io/#/https://github.com/pingcap/TiDB-Lambda-integration) workspace and login with your GitHub account
- Modify the Lambda function code
    - Open `aws-lambda-cloudformation/src/secretManager.ts` file in the left sidebar
    - Modify the line#22 `region` variable to your own region
- Re-build and re-upload the code bundle to your own S3 bucket
    - Install the dependencies
        - In Gitpod terminal
        - Run `cd aws-lambda-cloudformation` to change the working directory
        - Run `yarn` to install the dependencies
    - Re-build the code bundle
        - Run `yarn build` to build the code bundle
        - Check the `aws-lambda-cloudformation/dist/index.zip` file
        - Right click the `index.zip` file and select `Download`
    - Upload the code bundle to your own S3 bucket
        - Visit the [S3 service](https://console.aws.amazon.com/s3) in the AWS Management Console
        - Create a new bucket in your selected region
        - Upload the `index.zip` file to the bucket
        - Note down the S3 bucket Name and Region

## Setting up the Demo using CloudFormation

To set up the bookshop demo using CloudFormation, follow these steps:

1. Find `cloudformation_template.yml` or `cloudformation_template.json` file in previous download assets. The file contains the CloudFormation template that creates the necessary resources for the demo.
2. Navigate to the AWS Management Console and access the [CloudFormation service](https://console.aws.amazon.com/cloudformation).
3. Click **Create Stack** and upload the CloudFormation template file (either YAML or JSON).
4. Complete the stack creation process.
    - Create new stack by uploading a template file
        ![aws-lambda-cf-create-stack](/media/develop/aws-lambda-cf-create-stack.png)
    - Specify stack details
        - If you use a different AWS region other than `us-east-1`, you should follow the [Modify and rebuild the Lambda Function Code if necessary](#modify-and-rebuild-the-lambda-function-code-if-necessary) section to modify the Lambda function code, re-build and re-upload the code bundle to your own S3 bucket. Then, you need to specify the S3 bucket name and region in the `S3Bucket` and `S3Key` parameters.
        ![aws-lambda-cf-stack-details](/media/develop/aws-lambda-cf-stack-config.png)
## Using the Demo

Once the stack has been created, you can use the demo as follows:

- Visit the [API Gateway service](https://console.aws.amazon.com/apigateway) in the AWS Management Console and click on the `TiDBCloudApiGatewayV2` API
- Copy the `Invoke URL` from the Overview page, which serves as the API endpoint
    - ![api-gateway-invoke-url](/media/develop/aws-lambda-get-apigateway-invoke-url.png)
- Use API test tools like Postman or cURL to test the API
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

## Cleaning up

To avoid unnecessary charges, you can clean up the resources created by following these steps:

- Delete the CloudFormation stack in the [AWS Management Console](https://console.aws.amazon.com/cloudformation)

## Conclusion

In this document, we have provided a comprehensive guide on using AWS CloudFormation to integrate TiDB Cloud Serverless with Amazon Lambda. By following this guide, you can leverage the scalability and cost-effectiveness of serverless, event-driven microservices using TiDB Cloud Serverless and AWS Lambda.
