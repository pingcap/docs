---
title: Connect via Standard Connection
summary:
---

# Connect via Standard Connection

## Connect via standard connection

<SimpleTab>
<div label="Serverless Tier">

To connect to a Serverless Tier cluster via standard connection, perform the following steps:

1. Navigate to the **Clusters** page.

2. Locate your cluster, and click **Connect** in the upper-right corner of the cluster area. A connection dialog box is displayed.

3. Under **Connect with a SQL client** in the dialog, click the tab of your preferred connection method, and then connect to your cluster with the connection string.

    > **Note:**
    >
    > - When you connect to a Serverless Tier cluster, you must include the prefix for your cluster in the user name and wrap the name with quotation marks. For more information, see [User name prefix](/tidb-cloud/select-cluster-tier.md#user-name-prefix).
    > - Serverless Tier clusters only support TLS connection. For more information, see [Secure Connections to Serverless Tier Clusters](/tidb-cloud/secure-connections-to-serverless-tier-clusters.md).

</div>

<div label="Dedicated Tier">

To connect to a Dedicated Tier cluster via standard connection, perform the following steps:

1. Navigate to the **Clusters** page.

2. Locate your cluster, and click **Connect** in the upper-right corner of the cluster area. A connection dialog box is displayed.

3. Create a traffic filter for the cluster. Traffic filter is a list of IPs and CIDR addresses that are allowed to access TiDB Cloud via a SQL client.

    If the traffic filter is already set, skip the following sub-steps. If the traffic filter is empty, take the following sub-steps to add one.

    1. Click one of the buttons to add some rules quickly.

        - **Add My Current IP Address**
        - **Allow Access from Anywhere**

    2. Provide an optional description for the newly added IP address or CIDR range.

    3. Click **Create Filter** to confirm the changes.

4. Under **Step 2: Download TiDB cluster CA** in the dialog, click **Download TiDB cluster CA** for TLS connection to TiDB clusters. The TiDB cluster CA supports TLS 1.2 version by default.

    > **Note:**
    >
    > - The TiDB cluster CA is only available for Dedicated Tier clusters.
    > - Currently, TiDB Cloud only provides the connection strings and sample code for these connection methods: MySQL, MyCLI, JDBC, Python, Go, and Node.js.

5. Under **Step 3: Connect with a SQL client** in the dialog, click the tab of your preferred connection method, and then refer to the connection string and sample code on the tab to connect to your cluster.

    Note that you need to use the path of the downloaded CA file as the argument of the `--ssl-ca` option in the connection string.

</div>
</SimpleTab>
