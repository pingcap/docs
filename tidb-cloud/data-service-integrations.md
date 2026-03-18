---
title: Integrate a Data App with Third-Party Tools
summary: Learn how to integrate a TiDB Cloud Data App with third-party tools, such as GPTs and Dify, in the TiDB Cloud console.
---

# Integrate a Data App with Third-Party Tools

Integrating third-party tools with your Data App enhances your applications with advanced natural language processing and artificial intelligence (AI) capabilities provided by third-party tools. This integration enables your applications to perform more complex tasks and deliver intelligent solutions.

This document describes how to integrate a Data App with third-party tools, such as GPTs and Dify, in the TiDB Cloud console.

## Integrate your Data App with GPTs

You can integrate your Data App with [GPTs](https://openai.com/blog/introducing-gpts) to enhance your applications with intelligent capabilities.

To integrate your Data App with GPTs, perform the following steps:

1. Navigate to the [**Data Service**](https://tidbcloud.com/project/data-service) page of your project.
2. In the left pane, locate your target Data App, click the name of your target Data App, and then click the **Integrations** tab.
3. In the **Integrate with GPTs** area, click **Get Configuration**.

    ![Get Configuration](/media/tidb-cloud/data-service/GPTs1.png)

4. In the displayed dialog box, you can see the following fields:

    a. **API Specification URL**: copy the URL of the OpenAPI Specification of your Data App. For more information, see [Use the OpenAPI Specification](/tidb-cloud/data-service-manage-data-app.md#use-the-openapi-specification).

    b. **API Key**: enter the API key of your Data App. If you do not have an API key yet, click **Create API Key** to create one. For more information, see [Create an API key](/tidb-cloud/data-service-api-key.md#create-an-api-key).

    c. **API Key Encoded**: copy the base64 encoded string equivalent to the API key you have provided.

    ![GPTs Dialog Box](/media/tidb-cloud/data-service/GPTs2.png)

5. Use the copied API Specification URL and the encoded API key in your GPT configuration.

## Integrate your Data App with Dify

You can integrate your Data App with [Dify](https://docs.dify.ai/guides/tools) to enhance your applications with intelligent capabilities, such as vector distance calculations, advanced similarity searches, and vector analysis.

To integrate your Data App with Dify, follow the same steps as for [GPTs integration](#integrate-your-data-app-with-gpts). The only difference is that on the **Integrations** tab, you need to click **Get Configuration** in the **Integrate with Dify** area.
