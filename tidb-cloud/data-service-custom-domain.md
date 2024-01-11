---
title: Custom Domain in Data Service
summary: Learn how to add and delete a custom domain for a Data App.
---

# Custom Domain in Data Service

Custom Domain enables you to replace the TiDB Cloud Data Serivce provided default domain with your own one. 
Additionally, you have the flexibility to customize the default URL path according to your preferences. 

This document describes how to manage custom domains in your Data App.


## Custom domain overview

- Custom domain requests exclusively support HTTPS. Once you successfully configure your custom domain, a Let's Encrypt certificate will be automatically applied for enhanced security.
- Custom domains need to be unique within TiDB Cloud Data Service.
- You can configure a custom domain for each default domain. The default domain is determined by the region of your cluster.

## Manage custom domains

The following sections describe how to add and delete a custom domain for a Data App.

### Add a custom domain

To create a custom domain for a Data App, perform the following steps:

1. Navigate to the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project.
2. In the left pane, click the name of your target Data App to view its details.
3. In the **Manage Custom Domain** area, click **Add Custom Domain**.
4. In the **Add Custom Domain** dialog box, do the following:
    1. Select the default domain you wish to replace.
    2. Enter your desired custom domain name.
    3. (Optional) Configure custom path. This will be the prefix for your endpoints. If left empty, the default path is used.
5. Preview your Base URL to ensure it meets your expectations. If everything looks correct, click **Save**.
6. The **DNS Settings** dialog box is displayed. Then you need to add the default domain as a `CNAME` record to your DNS.

After setting up your custom domain, it will initially be in a **Pending** status as the system validates your DNS settings.
Once the DNS validation is successful, the status of your custom domain will change to **Success**.

> **Note:**
>
> Depending on your DNS provider, it might take up to 24 hours for the DNS record to be validated.

Once your custom domain status changes to **Success**, you will be able to access your endpoint using the new custom domain and path. 
You can refer to [Call an endpoint](/tidb-cloud/data-service-manage-endpoint.md#call-an-endpoint) to see how to find the code example. 
The domain name and path in the code example will be automatically updated to the custom domain when it's status reaches **Success**.

### Delete a custom domain

> **Note:**
>
> Before you delete a custom domain, make sure the custom domain is not used anymore.

To delete a custom domain for a Data App, perform the following steps:
1. Navigate to the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project.
2. In the left pane, click the name of your target Data App to view its details.
3. In the **Manage Custom Domain** area, locate the Action column, and then click **Delete** in the custom domain row that you want to delete.
4. In the displayed dialog box, confirm the deletion.
