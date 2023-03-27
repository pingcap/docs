---
title: API Keys in Data Service
summary: Learn how to create, edit, and delete an API key for a Data App.
---

# API Keys in Data Service

The TiDB Cloud Data API uses [HTTP Digest Authentication](https://en.wikipedia.org/wiki/Digest_access_authentication). It protects your private key from being sent over the network. For more details about HTTP Digest Authentication, refer to the [IETF RFC](https://datatracker.ietf.org/doc/html/rfc7616).

> **Note:**
>
> The Data API key in Data Service is different from the key used in the [TiDB Cloud API](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication). The Data API key is used to access data in the TiDB Cloud clusters, whereas the TiDB Cloud API key is used to manage resources such as projects, clusters, backups, restores, and imports.

## API key overview

- An API key contains a public key and a private key, which act as the username and password required in the HTTP Digest Authentication. The private key is only displayed upon the key creation.
- Each API key belongs to one Data App only and is used to access the data in the TiDB Cloud clusters.
- You must provide the correct API key in every request. Otherwise, TiDB Cloud responds with a `401` error.

## Rate limiting

Each Chat2Query Data App has a rate limit of 100 requests per day. Other Data Apps have a rate limit of 100 requests per minute per API key. If you exceed the rate limit, the API returns a `429` error. For more quota, you can [submit a request](https://support.pingcap.com/hc/en-us/requests/new?ticket_form_id=7800003722519) to our support team.

## Manage API keys

The following sections describe how to create, edit, and delete an API key for a Data App.

### Create an API key

To create an API key for a Data App, perform the following steps:

1. Navigate to the [**Data Service**](https://tidbcloud.com/console/dataservice) page of your project.
2. In the left pane, click the name of your target Data App to view its details.
3. In the **API Key** area, click **Create API Key**.
4. In the **Create API Key** dialog box, enter a description for your API key, and then click **Next**. The private key and public key are displayed.

    Make sure that you have copied and saved the private key in a secure location. After leaving this page, you will not be able to get the full private key again.

5. Click **Done**.

### Edit an API key

To edit the description of an API key, perform the following steps:

1. Navigate to the [**Data Service**](https://tidbcloud.com/console/dataservice) page of your project.
2. In the left pane, click the name of your target Data App to view its details.
3. In the **API Key** area, locate the **Action** column, and then click **...** > **Edit** in the API key row that you want to change.
4. Update the description of the API key.
5. Click **Update**.

### Delete an API key

> **Note:**
>
> Before you delete an API key, make sure that the API key is not used by any Data App.

To delete an API key for a Data App, perform the following steps:

1. Navigate to the [**Data Service**](https://tidbcloud.com/console/dataservice) page of your project.
2. In the left pane, click the name of your target Data App to view its details.
3. In the **API Key** area, locate the **Action** column, and then click **...** > **Delete** in the API key row that you want to delete.
4. Click **I understand, delete** to confirm the deletion.
