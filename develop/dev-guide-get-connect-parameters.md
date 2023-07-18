---
title: Get TiDB Cloud Connection Parameters
summary: This document provides instructions on obtaining the connection parameters for TiDB Cloud.
---

<!-- markdownlint-disable MD029 -->

# Get TiDB Cloud Connection Parameters

<CustomContent platform="tidb-cloud">

This document outlines the steps to obtain the connection parameters for TiDB Cloud in the TiDB Cloud console.

If you do not have a TiDB Cloud cluster yet, you can create one using the [Create Cluster](https://tidbcloud.com/console/clusters/create-cluster) page.

![Create TiDB Cloud Cluster](/media/develop/tidb-cloud-create-cluster.jpg)

</CustomContent>

## TiDB Cloud Serverless Tier Cluster

<CustomContent platform="tidb-cloud">

1. Go to the [Clusters](https://tidbcloud.com/console/clusters) page and click on the name of your TiDB Cloud Serverless Tier cluster.

    ![TiDB Cloud Cluster Page](/media/develop/tidb-cloud-cluster-page.jpg)

2. Click on **Connect**.

    ![Click Connect](/media/develop/tidb-cloud-click-connect.jpeg)

3. Select the **General** tab in the dialog box.

    ![Connect Panel Selector](/media/develop/tidb-cloud-connect-panel-selector.jpeg)

4. Depending on whether you have set a password before:

    1. If you have not set a password before, the panel will look like this. Click on **Create Password** to initialize your password.

        ![Connect Panel Initial](/media/develop/tidb-cloud-connect-panel-initial.jpg)

    2. Otherwise, it will look like this. If you have forgotten the password for the cluster, you can click on **Reset Password** to reset it.

        ![Connect Panel](/media/develop/tidb-cloud-connect-panel.jpeg)

5. Select the **Operating System** according to your preference, as the CA path is related to the operating system.

    ![Connect Panel OS](/media/develop/tidb-cloud-connect-panel-os.jpg)

6. If you encounter any issues obtaining these parameters, refer to the [Connect to Your TiDB Serverless Tier Cluster](/tidb-cloud/connect-to-tidb-cluster.md#serverless-tier) and [Secure Connections to Serverless Tier Clusters](/tidb-cloud/secure-connections-to-serverless-tier-clusters.md) documents.

</CustomContent>

## TiDB Cloud Dedicated Tier Cluster

<CustomContent platform="tidb-cloud">

1. Go to the [Clusters](https://tidbcloud.com/console/clusters) page and click on the name of your TiDB Cloud Dedicated Tier cluster.

    ![TiDB Cloud Cluster Page - Dedicated](/media/develop/tidb-cloud-cluster-page-dedicated.jpeg)

2. Click on **Connect**.

    ![Click Connect - Dedicated](/media/develop/tidb-cloud-click-connect-dedicated.jpeg)

3. Click on **Allow Access from Anywhere**, and then click on **Update Filter**. This will open the database to the public network. If you want to set specific IP restrictions, please refer to the [Connect via Standard Connection](/tidb-cloud/connect-via-standard-connection.md#connect-via-standard-connection) document.

    ![Allow All Connections](/media/develop/tidb-cloud-connect-allow-all.jpeg)
    ![Update Allow All](/media/develop/tidb-cloud-connect-allow-all-update.jpeg)

4. You do not need to use the CA. You can find the `host`, `port`, and `user` information here.

    - `host`

        ![Dedicated Host](/media/develop/tidb-cloud-connect-dedicated-host.jpg)

    - `port`

        ![Dedicated Port](/media/develop/tidb-cloud-connect-dedicated-port.jpg)

    - `user`

        ![Dedicated User](/media/develop/tidb-cloud-connect-dedicated-user.jpg)

5. If you have not set a password before, click on **···**, then **Security Settings**. Set the `password` in the dialog and click **Apply**.

    ![Dedicated More Security](/media/develop/tidb-cloud-dedicated-more-security.jpeg)
    ![Dedicated Security](/media/develop/tidb-cloud-dedicated-security.jpeg)

6. If you encounter any issues obtaining these parameters, refer to the [Connect to Your TiDB Dedicated Tier Cluster](/tidb-cloud/connect-to-tidb-cluster.md#dedicated-tier) document.

</CustomContent>