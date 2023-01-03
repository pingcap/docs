---
title: Configure Cluster Security Settings
summary: Learn how to configure the root password and allowed IP addresses to connect to your cluster.
---

# Configure Cluster Security Settings

When you create a Dedicated Tier cluster, the TiDB Cloud console will automatically guide you to configure the root password and allowed IP addresses to connect to your cluster.

> **Note:**
>
> For Serverless Tier clusters, this document is inapplicable and you can refer to [Secure Connections to Serverless Tier Clusters](/tidb-cloud/secure-connections-to-serverless-tier-clusters.md) instead.

If you do not configure the root password or allowed IP addresses at that time, or if you want to modify the cluster security settings, take the following steps:

1. In the TiDB Cloud console, navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page.
2. If you have multiple projects, choose a target project in the left navigation pane. Otherwise, skip this step.
3. In the row of your target cluster, click **...** and select **Security Settings**.
4. In the **Security Settings** dialog, configure the root password and allowed IP addresses.

    To allow your cluster to be accessible by any IP addresses, click **Allow Access from Anywhere**.

5. Click **Apply**.

> **Tip:**
>
> If you are viewing the overview page of your cluster, you can click the **...** in the upper-right corner of the page, select **Security Settings**, and configure these settings, too.
