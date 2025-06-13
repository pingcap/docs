---
title: Custom Domain in Data Service
summary: Learn how to use a custom domain to access your Data App in TiDB Cloud Data Service.
---

# Custom Domain in Data Service

TiDB Cloud Data Service provides a default domain `<region>.data.tidbcloud.com` to access each Data App's endpoints. For enhanced personalization and flexibility, you can configure a custom domain for your Data App instead of using the default domain.

This document describes how to manage custom domains in your Data App.

## Before you begin

Before configuring a custom domain for your Data App, note the following:

- Custom domain requests exclusively support HTTPS for security. Once you successfully configure a custom domain, a "Let's Encrypt" certificate is automatically applied.
- Your custom domain must be unique within the TiDB Cloud Data Service.
- You can configure only one custom domain for each default domain, which is determined by the region of your cluster.

## Manage custom domains

The following sections describe how to create, edit, and remove a custom domain for a Data App.

### Create a custom domain

To create a custom domain for a Data App, perform the following steps:

1. Navigate to the [**Data Service**](https://tidbcloud.com/project/data-service) page of your project.
2. In the left pane, click the name of your target Data App to view its details.
3. In the **Manage Custom Domain** area, click **Add Custom Domain**.
4. In the **Add Custom Domain** dialog box, do the following:
    1. Select the default domain you want to replace.
    2. Enter your desired custom domain name.
    3. Optional: configure a custom path as the prefix for your endpoints. If **Custom Path** is left empty, the default path is used.
5. Preview your **Base URL** to ensure it meets your expectations. If it looks correct, click **Save**.
6. Follow the instructions in the **DNS Settings** dialog to add a `CNAME` record for the default domain in your DNS provider.

The custom domain is in a **Pending** status initially while the system validates your DNS settings. Once the DNS validation is successful, the status of your custom domain will update to **Success**.

> **Note:**
>
> Depending on your DNS provider, it might take up to 24 hours for the DNS record to be validated. If a custom domain remains unvalidated for over 24 hours, it will be in an **Expired** status. In this case, you can only remove the custom domain and try again.

After your custom domain status is set to **Success**, you can use it to access your endpoint. The code example provided by TiDB Cloud Data Service is automatically updated to your custom domain and path. For more information, see [Call an endpoint](/tidb-cloud/data-service-manage-endpoint.md#call-an-endpoint).

### Edit a custom domain

> **Note:**
>
> After you complete the following changes, the previous custom domain and custom path will become invalid immediately. If you modify the custom domain, you need to wait for the new DNS record to be validated.

To edit a custom domain for a Data App, perform the following steps:

1. Navigate to the [**Data Service**](https://tidbcloud.com/project/data-service) page of your project.
2. In the left pane, click the name of your target Data App to view its details.
3. In the **Manage Custom Domain** area, locate the **Action** column, and then click <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" stroke-width="1.5" viewBox="0 0 24 24"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="M11 4H6.8c-1.68 0-2.52 0-3.162.327a3 3 0 0 0-1.311 1.311C2 6.28 2 7.12 2 8.8v8.4c0 1.68 0 2.52.327 3.162a3 3 0 0 0 1.311 1.311C4.28 22 5.12 22 6.8 22h8.4c1.68 0 2.52 0 3.162-.327a3 3 0 0 0 1.311-1.311C20 19.72 20 18.88 20 17.2V13M8 16h1.675c.489 0 .733 0 .963-.055.204-.05.4-.13.579-.24.201-.123.374-.296.72-.642L21.5 5.5a2.121 2.121 0 0 0-3-3l-9.563 9.563c-.346.346-.519.519-.642.72a2 2 0 0 0-.24.579c-.055.23-.055.474-.055.963V16Z" stroke-width="inherit"></path></svg> **Edit** in the custom domain row that you want to edit.
4. In the displayed dialog box, update the custom domain or custom path.
5. Preview your **Base URL** to ensure it meets your expectations. If it looks correct, click **Save**.
6. If you have changed the custom domain, follow the instructions in the **DNS Settings** dialog to add a `CNAME` record for the default domain in your DNS provider.

### Remove a custom domain

> **Note:**
>
> Before you delete a custom domain, make sure that the custom domain is not used anymore.

To remove a custom domain for a Data App, perform the following steps:

1. Navigate to the [**Data Service**](https://tidbcloud.com/project/data-service) page of your project.
2. In the left pane, click the name of your target Data App to view its details.
3. In the **Manage Custom Domain** area, locate the **Action** column, and then click <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" stroke-width="1.5" viewBox="0 0 24 24"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="M16 6v-.8c0-1.12 0-1.68-.218-2.108a2 2 0 0 0-.874-.874C14.48 2 13.92 2 12.8 2h-1.6c-1.12 0-1.68 0-2.108.218a2 2 0 0 0-.874.874C8 3.52 8 4.08 8 5.2V6m2 5.5v5m4-5v5M3 6h18m-2 0v11.2c0 1.68 0 2.52-.327 3.162a3 3 0 0 1-1.311 1.311C16.72 22 15.88 22 14.2 22H9.8c-1.68 0-2.52 0-3.162-.327a3 3 0 0 1-1.311-1.311C5 19.72 5 18.88 5 17.2V6" stroke-width="inherit"></path></svg> **Delete** in the custom domain row that you want to delete.
4. In the displayed dialog box, confirm the deletion.
