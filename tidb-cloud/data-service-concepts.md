---
title: Data Service (Beta)
summary: Learn about Data Service concepts for TiDB Cloud.
---

# Data Service (Beta)

TiDB Cloud [Data Service (beta)](https://tidbcloud.com/project/data-service) is a fully managed low-code backend-as-a-service solution that simplifies backend application development, empowering developers to rapidly build highly scalable, secure, data-driven applications.

Data Service enables you to access TiDB Cloud data via an HTTPS request using a custom API endpoint. This feature uses a serverless architecture to handle computing resources and elastic scaling, so you can focus on the query logic in endpoints without worrying about infrastructure or maintenance costs.

For more information, see [TiDB Cloud Data Service (Beta) Overview](/tidb-cloud/data-service-overview.md).

## Data App

A Data App in [Data Service (beta)](https://tidbcloud.com/project/data-service) is a collection of endpoints that you can use to access data for a specific application. By creating a Data App, you can group your endpoints and configure authorization settings using API keys to restrict access to endpoints. In this way, you can ensure that only authorized users can access and manipulate your data, making your application more secure.

For more information, see [Manage a Data App](/tidb-cloud/data-service-manage-data-app.md).

## Data App endpoints

An endpoint in [Data Service (beta)](https://tidbcloud.com/project/data-service) is a web API that you can customize to execute SQL statements. You can specify parameters for your SQL statements, such as the value used in the `WHERE` clause. When a client calls an endpoint and provides values for the parameters in a request URL, the endpoint executes the corresponding SQL statement with the provided parameters and returns the results as part of the HTTP response.

For more information, see [Manage an Endpoint](/tidb-cloud/data-service-manage-endpoint.md).

## Chat2Query API

In TiDB Cloud, Chat2Query API is a RESTful interface that enables you to generate and execute SQL statements using AI by providing instructions. Then, the API returns the query results for you.

For more information, see [Get Started with Chat2Query API](/tidb-cloud/use-chat2query-api.md).

## AI integrations

Integrating third-party tools with your Data App enhances your applications with advanced natural language processing and artificial intelligence (AI) capabilities provided by third-party tools. This integration enables your applications to perform more complex tasks and deliver intelligent solutions.

Currently, you can integrate third-party tools, such as GPTs and Dify, in the TiDB Cloud console.

For more information, see [Integrate a Data App with Third-Party Tools](/tidb-cloud/data-service-integrations.md).

## Configuration as Code

TiDB Cloud provides a Configuration as Code (CaC) approach to represent your entire Data App configurations as code using the JSON syntax.

By connecting your Data App to GitHub, TiDB Cloud can use the CaC approach and push your Data App configurations as [configuration files](/tidb-cloud/data-service-app-config-files.md) to your preferred GitHub repository and branch.

If Auto Sync & Deployment is enabled for your GitHub connection, you can also modify your Data App by updating its configuration files on GitHub. After you push the configuration file changes to GitHub, the new configurations will be deployed in TiDB Cloud automatically.

For more information, see [Deploy Data App Automatically with GitHub](/tidb-cloud/data-service-manage-github-connection.md).