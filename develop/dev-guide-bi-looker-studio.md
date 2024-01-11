---
title: Connect to TiDB Cloud with Looker Studio
summary: Learn how to connect to TiDB Cloud using Looker Studio
---

# Connect to TiDB Cloud with Looker Studio

TiDB is a MySQL-compatible database, and [Looker Studio](https://lookerstudio.google.com/) is a free web-based BI tool that can visualize data from various sources. 

In this tutorial, you can learn how to connect to your TiDB cluster using Looker Studio.

> **Note:**
>
> - For this tutorial we will use a serverless cluster. Looker Studio can also be used with dedicated clusters.

## Prerequisites

To complete this tutorial, you need:

- Google Account. 
- A TiDB cluster.

**If you don't have a TiDB cluster, you can create one as follows:**

- Follow [Creating a TiDB Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md) to create your own TiDB Serverless cluster.

## Import Dataset

You can use the S&P 500 dataset provided as an Interactive Tutorial of TiDB Serverless. 

<SimpleTab>
<div label="TiDB Serverless">

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page, and click the question mark icon in the bottom-right corner. A Help dialog is displayed. 

2. Click **Interactive Tutorials**. Then click **S&P 500 Analysis**.

3. In the **Import S&P 500 Dataset** dialog, select your Serverless cluster. Then click the **Import Dataset** button. It will start importing briefly.

4. After the status changed to **Imported**, you can close this dialog. Click the **Exit Tutorial** button in the bottom-left corner of the dialog. 

</div>
</SimpleTab>

## Connect to TiDB cluster

<SimpleTab>
<div label="TiDB Serverless">

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. Set **Operating System** to `Windows` in the connection dialog. Then Set **Connect With** to `General`. You can download [CA cert](https://letsencrypt.org/certs/isrgrootx1.pem) at the note below. 

    > **Tip:**
    >
    > As TiDB Serverless requires a secure TLS connection between the client and the cluster, you need this CA cert for connection settings on Looker Studio.

4. Click **Generate Password** to create a random password.

    > **Tip:**
    >
    > If you have created a password before, use the original password or click **Reset Password** to generate a new one.

5. Open Looker Studio and create a Blank Report. Select the' MySQL' connector in the **Add data to report** screen.

6. In the **BASIC** setting pane, configure the following connection parameters:

    - **Host Name or IP**: enter the `HOST` parameter from the TiDB Cloud connection dialog.
    - **Port(Optional)**: enter the `PORT` parameter from the TiDB Cloud connection dialog.
    - **Database**: enter the database you want to connect to. In this tutorial, set `sp500insight`.
    - **Username**: enter the `USERNAME` parameter from the TiDB Cloud connection dialog.
    - **Password**: enter the `PASSWORD` parameter from the TiDB Cloud connection dialog.
    - Check **Enable SSL**.
        - Click the icon on the right of **MySQL SSL Client Configuration Files**. Then, select the downloaded CA file in step 3. 

    ![Looker Studio: configure connection settings for TiDB cloud](/media/develop/looker-studio-configure-connection.png)

7. Click **AUTHENTICATE**. 

If the authentication succeeds, you can see tables in the database. 

</div>
<div label="TiDB Dedicated">

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **...** menu in the upper-right corner. Then, select **Security Settings**. Settings dialog shows up. 

3. Click **Generate** to generate root password and **Copy** it to the clipboard.

    > **Tip:**
    >
    > If you have created a password before, use the original password or click **Regenerate** to generate a new one.

4. Allow access from Looker Studio by adding `142.251.74.0/23` to **IP Address**, then click **Add to IP list**.

    > **Tip:**
    >
    > For more details about the connection from Looker Studio, refer to [Connect to MySQL](https://support.google.com/looker-studio/answer/7088031#zippy=%2Cin-this-article).

5. Click **Apply** to close the dialog.

6. Click **Connect** in the upper-right corner. A connection dialog is displayed.

7. You can download CA File with the link under **Step 2**. 

8. Open Looker Studio and create a Blank Report. Select the' MySQL' connector in the **Add data to report** screen.

9. In the **BASIC** setting pane, configure the following connection parameters:

    - **Host Name or IP**: enter the `HOST` parameter from the TiDB Cloud connection dialog.
    - **Port(Optional)**: enter the `PORT` parameter from the TiDB Cloud connection dialog.
    - **Database**: enter the database you want to connect to. In this tutorial, set `sp500insight`.
    - **Username**: enter the `USERNAME` parameter from the TiDB Cloud connection dialog.
    - **Password**: enter the `PASSWORD` parameter from the TiDB Cloud connection dialog.
    - Check **Enable SSL**.
        - Click the icon on the right of **MySQL SSL Client Configuration Files**. Then, select the downloaded CA file before. 

10. Click **AUTHENTICATE**. 

If the authentication succeeds, you can see tables in the database. 
</div>
</SimpleTab>

## Create a simple chart

Now, you can use TiDB cluster as a data source. Let's make a simple chart with data. 

1. In the setting pane, select **CUSTOM QUERY**. 

2. Put the SQL below, then click **Add** in the bottom-right corner. 

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
    ORDER BY 5 ASC
    ```

    If you see **You are about to add data to this report** dialog, click **ADD TO REPORT**.

3. You see a table in the report. Click **Add a chart**, then select `Combo chart` in the `Line` category.

4. In the **Chart** settings pane, configure the following parameters:

    - **Dimension**: `sector`.
    - **Metric**: `companies` and `total_market_cap`.
    - In the **STYLE** Tab:
      - Series #1 check `Line`.
      - Series #1 axis `Right`.
      - Series #2 check `Bars`.
      - Series #2 axis `Left`.
    - Leave others as defaults.

You can see a combo chart below:

![Looker Studio: A simple Combo Chart](/media/develop/looker-studio-simple-chart.png)

## Next steps

- Learn more usage of Looker Studio from [Looker Studio Help](https://support.google.com/looker-studio)
- Learn the best practices for TiDB application development with the chapters in the [Developer guide](/develop/dev-guide-overview.md), such as [Insert data](/develop/dev-guide-insert-data.md), [Update data](/develop/dev-guide-update-data.md), [Delete data](/develop/dev-guide-delete-data.md), [Single table reading](/develop/dev-guide-get-data-from-single-table.md), [Transactions](/develop/dev-guide-transaction-overview.md), and [SQL performance optimization](/develop/dev-guide-optimize-sql-overview.md).
- Learn through the professional [TiDB developer courses](https://www.pingcap.com/education/) and earn [TiDB certifications](https://www.pingcap.com/education/certification/) after passing the exam.

## Need help?

Ask questions on [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) or [create a support ticket](https://support.pingcap.com/).
