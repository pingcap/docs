---
title: Integrate a Data App with third party component
summary: Learn how to integrate a Data App with third party component in the TiDB Cloud console.
---

# Integrate a Data App with third party component

The integration of third-party components with your Data App allows you to enhance your applications with intelligent capabilities. This integration enables your applications to leverage advanced natural language processing and AI capabilities provided by third-party components, empowering your applications to perform sophisticated tasks and deliver smarter solutions.

This document describes how to integrate a Data App with third party component in the TiDB Cloud console.

## Integrate your Data App with GPTs

You can integrate your Data App with [GPTs](https://openai.com/blog/introducing-gpts) to enhance your applications with intelligent capabilities.

To integrate your Data App with GPTs, perform the following steps:

1. Navigate to the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project.
2. In the left pane, locate your target Data App and click the name of your target Data App to view its details.
3. In the **Integration with GPTs** area, click **Get Configuration**.

   ![Get Configuration](/media/tidb-cloud/data-service/GPTs1.png)

4. In the displayed dialog box, you can see the following fields:

   a. **API Specification URL**: copy the URL of the OpenAPI Specification of your Data App. For more information, see [Use the OpenAPI Specification](#use-the-openapi-specification).

   b. **API Key**: enter the API key of your Data App. If you do not have an API key yet, click **Create API Key** to create one. For more information, see [Create an API key](/tidb-cloud/data-service-api-key.md#create-an-api-key).

   c. **API Key Encoded**: copy the base64 encoded string equivalent to the API key you have provided.

   ![GPTs Dialog Box](/media/tidb-cloud/data-service/GPTs2.png)

5. Use the copied API Specification URL and the encoded API key in your GPT configuration.

## Integrate your Data App with Dify

You can integrate your Data App with [dify.ai](https://docs.dify.ai/guides/tools) to enhance your applications with intelligent capabilities.

Integrate dify.ai with ease to leverage vector distance calculations. Find essential configuration details for seamless setup, enabling your applications to perform advanced similarity searches and enhance functionality with powerful vector analysis.

To integrate your Data App with Dify, perform steps are same as GPTs.
