---
title: QuickSight Integration Guide
summary: Learn how to integrate TiDB Cloud Dedicated Tier with Amazon QuickSight.
---

# Integrate TiDB with Amazon QuickSight

This document provides a general introduction to Amazon QuickSight and describes how to integrate Amazon QuickSight with TiDB.

If you are interested in learning more about TiDB and Amazon QuickSight, you can find some useful links as follows:

- [TiDB Cloud](https://docs.pingcap.com/tidbcloud)
- [TiDB Developer Guide](/develop/dev-guide-overview.md)
- [Amazon QuickSight Documentation](https://docs.aws.amazon.com/quicksight/latest/user/welcome.html)

## What is Amazon QuickSight?

[Amazon QuickSight](https://aws.amazon.com/quicksight/) is a cloud-scale business intelligence (BI) service that you can use to deliver easy-to-understand insights to the people who you work with, wherever they are. Amazon QuickSight connects to your data in the cloud and combines data from many different sources. In a single data dashboard, QuickSight can include AWS data, third-party data, big data, spreadsheet data, SaaS data, B2B data, and more. As a fully managed cloud-based service, Amazon QuickSight provides enterprise-grade security, global availability, and built-in redundancy. It also provides the user-management tools that you need to scale from 10 users to 10,000, all with no infrastructure to deploy or manage.

## Why Amazon QuickSight integration?

Every day, the people in your organization make decisions that affect your business. When they have the right information at the right time, they can make the choices that move your company in the right direction.

Here are some of the benefits of using Amazon QuickSight for analytics, data visualization, and reporting:

- The in-memory engine, called SPICE, responds with blazing speed.
- No upfront costs for licenses and a low total cost of ownership (TCO).
- Collaborative analytics with no need to install an application.
- Combine a variety of data into one analysis.
- Publish and share your analysis as a dashboard.
- Control features available in a dashboard.
- No need to manage granular database permissions—dashboard viewers can see only what you share.

## Prerequisites

- [TiDB Cluster](#create-tidb-cluster)
- [Amazon QuickSight Account](https://portal.aws.amazon.com/billing/signup?client=quicksight&fid=441BE2A63D1F1F56-313F2AF2462BDF3C&redirect_url=https%3A%2F%2Fquicksight.aws.amazon.com%2Fsn%2Fconsole%2Fsignup#/start&refid=ha_awssm-evergreen-free_tier)

## Create TiDB Cluster

TiDB (/’taɪdiːbi:/, "Ti" stands for Titanium) is an open-source NewSQL database that supports Hybrid Transactional and Analytical Processing (HTAP) workloads. It is MySQL compatible and features horizontal scalability, strong consistency, and high availability.

<CustomContent platform="tidb">

If you don't have a TiDB cluster, you can follow the [Quick Start Guide for the TiDB Database Platform](/quick-start-with-tidb.md) to create a TiDB cluster.

</CustomContent>

Here is the way to create a playground TiDB cluster. In this section, create a TiDB cluster using [TiDB Cloud Dedicated Tier](https://docs.pingcap.com/tidbcloud/select-cluster-tier#dedicated-tier). But you can create your TiDB cluster anywhere. Just ensure that Amazon QuickSight can connect to your TiDB cluster.

You can follow the document to [Create a TiDB Cluster](https://docs.pingcap.com/tidbcloud/create-tidb-cluster), to create a TiDB Cloud Dedicated Tier cluster.

## Integrate Amazon QuickSight and TiDB

1. You need to [get an account](https://portal.aws.amazon.com/billing/signup?client=quicksight&fid=441BE2A63D1F1F56-313F2AF2462BDF3C&redirect_url=https%3A%2F%2Fquicksight.aws.amazon.com%2Fsn%2Fconsole%2Fsignup#/start&refid=ha_awssm-evergreen-free_tier) for [Amazon QuickSight](https://aws.amazon.com/quicksight). If you register successfully, you can see a page like this.

    ![aws quicksight register](/media/develop/aws-quicksight-register.png)

2. Click **Go to Amazon QuickSight**. It will jump to the [home page of Amazon QuickSight](https://quicksight.aws.amazon.com/sn/start/analyses).

    ![aws quicksight home page](/media/develop/aws-quicksight-home.png)

3. In the **Datasets** tab, click **New dataset**.

    ![aws quicksight new dataset](/media/develop/aws-quicksight-new-dataset.png)

4. And you can select the **MySQL** card. Because TiDB is highly compatible with the MySQL protocol and supports [most MySQL syntax and features](/mysql-compatibility.md), most MySQL connection libraries are compatible with TiDB.

    ![aws quicksight new dataset mysql type](/media/develop/aws-quicksight-mysql-card.png)

5. In the dialog, input your TiDB cluster message. And click **Validate connection**. Amazon QuickSight will use the TiDB cluster properties you just input, try to connect the TiDB cluster.

    ![aws quicksight tidb properties](/media/develop/aws-quicksight-tidb-props.png)

6. It shows validated, then clicks **Create data source** (If some errors occur, please check your TiDB cluster is available, and reachable to Amazon QuickSight).

    ![aws quicksight tidb checked](/media/develop//aws-quicksight-tidb-checked.png)

7. Then you can see the tables in the database you specify. In this section, just click **Select** for demonstration. You can edit/preview it, or use SQL to retrieve a result set. For example, you can choose Commercial Open Source Software (COSS) [publicly announced global VC Funding Investments dataset](https://docs.google.com/spreadsheets/d/1Bz0lxWzwW8q9AUSO5HgRrUyfR47em6YQW4h8PF_vRmE/edit#gid=666389338) that stored in `coss_invest` table within TiDB Cluster (PingCAP don't offer this data, just for a demonstrate).

    ![aws quicksight table](/media/develop/aws-quicksight-table.png)

8. In this case, select **Directly query your data** and click **Visualize**.

    ![aws quicksight dataset creation finish](/media/develop/aws-quicksight-dataset-finish.png)

9. Data is successfully imported. And you can just click these buttons. You can see a pie chart for **Total percentage of investment in commercial open source softwares by Venture Capitalists**.

    ![aws quicksight pie chart](/media/develop/aws-quicksight-pie-chart.png)

For more Amazon QuickSight usage, refer to [Amazon QuickSight User Guide](https://docs.aws.amazon.com/quicksight/latest/user/welcome.html).