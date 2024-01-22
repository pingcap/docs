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

The following sections describe how to create and remove a custom domain for a Data App.

### Create a custom domain

To create a custom domain for a Data App, perform the following steps:

1. Navigate to the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project.
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
> Depending on your DNS provider, it might take up to 24 hours for the DNS record to be validated. The custom domain that have not been validated for over 24 hours will show an 'expired' status and can only be deleted.

After your custom domain status is set to **Success**, you can use it to access your endpoint. The code example provided by TiDB Cloud Data Service is automatically updated to your custom domain and path. For more information, see [Call an endpoint](/tidb-cloud/data-service-manage-endpoint.md#call-an-endpoint).

### Edit the custom domain
> **Note:**
>
> After you complete the changes, the previous custom domain and custom path will become invalid immediately. If you have changed custom domain, you need to wait for the new DNS record to be validated.

To edit the custom domain for a Data App, perform the following steps:
1. Navigate to the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project.
2. In the left pane, click the name of your target Data App to view its details.
3. In the **Manage Custom Domain** area, locate the **Action** column, and then click **Edit** in the custom domain row that you want to delete.
4. Edit custom domain or custom path
5. Preview your **Base URL** to ensure it meets your expectations. If it looks correct, click **Save**.
6. If you have changed the custom domain, it is similar to the process of creating a custom domain. Follow the instructions in the **DNS Settings** dialog to add a `CNAME` record for the default domain in your DNS provider.

### Remove a custom domain

> **Note:**
>
> Before you delete a custom domain, make sure that the custom domain is not used anymore.

To remove a custom domain for a Data App, perform the following steps:

1. Navigate to the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project.
2. In the left pane, click the name of your target Data App to view its details.
3. In the **Manage Custom Domain** area, locate the **Action** column, and then click **Delete** in the custom domain row that you want to delete.
4. In the displayed dialog box, confirm the deletion.
