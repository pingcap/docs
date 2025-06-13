---
title: Connect to TiDB Cloud Serverless with Looker Studio
summary: Learn how to connect to TiDB Cloud Serverless using Looker Studio.
---

# Connect to TiDB Cloud Serverless with Looker Studio

TiDB is a MySQL-compatible database, TiDB Cloud Serverless is a fully managed TiDB offering, and [Looker Studio](https://lookerstudio.google.com/) is a free web-based BI tool that can visualize data from various sources.

In this tutorial, you can learn how to connect to your TiDB Cloud Serverless cluster with Looker Studio.

> **Note:**
>
> Most steps in this tutorial work with TiDB Cloud Dedicated as well. However, for TiDB Cloud Dedicated, you need to note the following:
> 
> - Import your dataset following [Import data from files to TiDB Cloud](/tidb-cloud/tidb-cloud-migration-overview.md#import-data-from-files-to-tidb-cloud).
> - Get the connection information for your cluster following [Connect to TiDB Cloud Dedicated](/tidb-cloud/connect-via-standard-connection.md). When connecting to TiDB Cloud Dedicated, you need to allow access from `142.251.74.0/23`. For more information about connections from Looker Studio, see [Looker Studio documentation](https://support.google.com/looker-studio/answer/7088031#zippy=%2Cin-this-article).

## Prerequisites

To complete this tutorial, you need:

- A Google account
- A TiDB Cloud Serverless cluster

**If you don't have a TiDB Cloud Serverless cluster, you can create one as follows:**

- [Create a TiDB Cloud Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md#step-1-create-a-tidb-cloud-serverless-cluster)

## Step 1. Import a dataset

You can import the S&P 500 dataset provided in the interactive tutorial of TiDB Cloud Serverless.

1. Navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page, and click **?** in the lower-right corner. A **Help** dialog is displayed.

2. In the dialog, click **Interactive Tutorials**, and then click **S&P 500 Analysis**.

3. Select your TiDB Cloud Serverless cluster, and then click **Import Dataset** to import the S&P 500 dataset to your cluster.

4. After the import status changes to **IMPORTED**, click **Exit Tutorial** to close this dialog.

If you encounter any issues during import, you can cancel this import task as follows:

1. On the [**Clusters**](https://tidbcloud.com/project/clusters) page, click the name of your TiDB Cloud Serverless cluster to go to its overview page.
2. In the left navigation pane, click **Data** > **Import**.
3. Find the import task named **sp500-insight**, click **...** in the **Action** column, and then click **Cancel**.

## Step 2. Get the connection information for your cluster

1. Navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. In the connection dialog, set **Connect With** to `General`, and then click **Generate Password** to create a random password.

    > **Tip:**
    >
    > If you have created a password before, use the original password or click **Reset Password** to generate a new one.

4. Download the [CA cert](https://letsencrypt.org/certs/isrgrootx1.pem).

    > **Tip:**
    >
    > TiDB Cloud Serverless requires a secure TLS connection between the client and the cluster, so you need this CA cert for connection settings in Looker Studio.

## Step 3. Connect to your TiDB cluster with Looker Studio

1. Log into [Looker Studio](https://lookerstudio.google.com/), and then click **Create** > **Report** in the left navigation pane.

2. On the displayed page, search and select the **MySQL** connector, and then click **AUTHORIZE**.

3. In the **BASIC** setting pane, configure the connection parameters.

    - **Host Name or IP**: enter the `HOST` parameter from the TiDB Cloud Serverless connection dialog.
    - **Port(Optional)**: enter the `PORT` parameter from the TiDB Cloud Serverless connection dialog.
    - **Database**: enter the database you want to connect to. For this tutorial, enter `sp500insight`.
    - **Username**: enter the `USERNAME` parameter from the TiDB Cloud Serverless connection dialog.
    - **Password**: enter the `PASSWORD` parameter from the TiDB Cloud Serverless connection dialog.
    - **Enable SSL**: select this option, and then click the upload icon to the right of **MySQL SSL Client Configuration Files** to upload the CA file downloaded from [Step 2](#step-2-get-the-connection-information-for-your-cluster).

    ![Looker Studio: configure connection settings for TiDB Cloud Serverless](/media/tidb-cloud/looker-studio-configure-connection.png)

4. Click **AUTHENTICATE**.

If the authentication succeeds, you can see tables in the database.

## Step 4. Create a simple chart

Now, you can use the TiDB cluster as a data source and create a simple chart with data.

1. In the right pane, click **CUSTOM QUERY**.

    ![Looker Studio: custom query](/media/tidb-cloud/looker-studio-custom-query.png)

2. Copy the following code to the **Enter Custom Query** area, and then click **Add** in the lower-right corner.

    ```sql
    SELECT sector,
        COUNT(*)                                                                      AS companies,
        ROW_NUMBER() OVER (ORDER BY COUNT(*) DESC )                                   AS companies_ranking,
        SUM(market_cap)                                                               AS total_market_cap,
        ROW_NUMBER() OVER (ORDER BY SUM(market_cap) DESC )                            AS total_market_cap_ranking,
        SUM(revenue_growth * weight) / SUM(weight)                                    AS avg_revenue_growth,
        ROW_NUMBER() OVER (ORDER BY SUM(revenue_growth * weight) / SUM(weight) DESC ) AS avg_revenue_growth_ranking
    FROM companies
        LEFT JOIN index_compositions ic ON companies.stock_symbol = ic.stock_symbol
    GROUP BY sector
    ORDER BY 5 ASC;
    ```

    If you see the **You are about to add data to this report** dialog, click **ADD TO REPORT**. Then, a table is displayed in the report.

3. In the toolbar of the report, click **Add a chart**, and then select `Combo chart` in the `Line` category.

4. In the **Chart** settings pane on the right, configure the following parameters:

    - In the **SETUP** Tab:
        - **Dimension**: `sector`.
        - **Metric**: `companies` and `total_market_cap`.
    - In the **STYLE** Tab:
      - Series #1: select the `Line` option and the `Right` axis.
      - Series #2: select the `Bars` option and the `Left` axis.
    - Leave other fields as defaults.

Then, you can see a combo chart similar as follows:

![Looker Studio: A simple Combo chart](/media/tidb-cloud/looker-studio-simple-chart.png)

## Next steps

- Learn more usage of Looker Studio from [Looker Studio Help](https://support.google.com/looker-studio).
- Learn the best practices for TiDB application development with the chapters in the [Developer guide](/develop/dev-guide-overview.md), such as [Insert data](/develop/dev-guide-insert-data.md), [Update data](/develop/dev-guide-update-data.md), [Delete data](/develop/dev-guide-delete-data.md), [Single table reading](/develop/dev-guide-get-data-from-single-table.md), [Transactions](/develop/dev-guide-transaction-overview.md), and [SQL performance optimization](/develop/dev-guide-optimize-sql-overview.md).
- Learn through the professional [TiDB developer courses](https://www.pingcap.com/education/) and earn [TiDB certifications](https://www.pingcap.com/education/certification/) after passing the exam.

## Need help?

Ask the community on [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) or [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs), or [submit a support ticket](https://tidb.support.pingcap.com/).
