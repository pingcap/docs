---
title: Index Insight (Beta)
summary: Learn how to use the Index Insight feature in TiDB Cloud and obtain index recommendations for your slow queries.
---

# Index Insight (Beta)

The Index Insight (beta) feature in TiDB Cloud provides powerful capabilities to optimize query performance by offering index recommendations for slow queries that are not using indexes effectively. This document walks you through the steps to enable and utilize the Index Insight feature effectively.

> **Note:**
>
> Index Insight is currently in beta and this feature is only available for [TiDB Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) clusters.

## Introduction

The Index Insight feature provides you with the following benefits:

- Enhanced query performance: By identifying and suggesting appropriate indexes for slow queries, you can significantly enhance query execution speed, resulting in quicker response times and a better user experience.
- Cost efficiency: Optimized query performance reduces the need for extra computing resources, enabling you to achieve more with existing infrastructure and potentially leading to operational cost savings.
- Simplified optimization process: Index Insight simplifies the process of identifying and implementing index improvements, eliminating the need for manual analysis and guesswork. You can get accurate recommendations using this feature, which saves time and effort.
- Improved application efficiency: By optimizing database performance, applications running on TiDB Cloud can handle larger workloads and serve more concurrent users, which enables businesses to scale operations effectively.

## Usage

This section introduces how to enable the Index Insight feature and obtain index recommendations for your slow queries.

### Before you begin

Before enabling the Index Insight feature, make sure that you have created a TiDB Dedicated cluster. If you do not have one, follow the steps in [Create a cluster](/tidb-cloud/create-tidb-cluster.md) to create one.

### Step 1: Enable Index Insight

1. In the [TiDB Cloud console](https://tidbcloud.com), navigate to the cluster overview page of your TiDB Dedicated cluster, and then click **Diagnosis** in the left navigation pane.

2. Click the **Index Insight BETA** tab. The Index Insight overview page is displayed.

3. To use the Index Insight feature, you need to create a dedicated SQL user, which is used to trigger the feature and receive index recommendations. The following SQL statements create a new SQL user with required privileges, including read privilege for `information_schema` and `mysql`. Replace `'index_insight_user'` and `'your_password'` with your values.

    ```sql
    CREATE user 'index_insight_user'@'%' IDENTIFIED by 'your_password';
    GRANT SELECT ON information_schema.* TO 'index_insight_user'@'%';
    GRANT SELECT ON mysql.* TO 'index_insight_user'@'%';
    GRANT PROCESS, REFERENCES ON *.* TO 'index_insight_user'@'%';
    FLUSH PRIVILEGES;
    ```

    > **Note:**
    >
    > To connect to your TiDB Dedicated cluster, see [Connect to a TiDB cluster](/tidb-cloud/connect-to-tidb-cluster.md).

4. Enter the username and password of the SQL user created in the preceding step. Then, click **Activate** to initiate the activation process.

### Step 2: Manually trigger Index Insight

To obtain index recommendations for your slow queries, you can manually trigger the Index Insight feature by clicking **Check Up** in the upper-right corner of the Index Insight overview page.

Then, the feature begins scanning your slow queries from the past three hours. After the scan finishes, it provides a list of index recommendations based on its analysis.

### Step 3: View index recommendations

To view the details of a specific index recommendation, click the insight from the list. The **Index Insight Detail** page is displayed.

On this page, you can find the recommended indexes, related slow queries, execution plans, and relevant metrics. This information helps you better understand the performance issues and evaluate the potential impact of implementing the recommended indexes.

### Step 4: Implement index recommendations

Before implementing the recommended indexes, you need to first review and evaluate the recommendations from the **Index Insight Detail** page.

To implement the recommended indexes, follow these steps:

1. Evaluate the impact of the proposed index on existing queries and workload.
2. Consider the storage requirements and potential trade-offs associated with the index implementation.
3. Use appropriate database management tools to create the recommended indexes on the relevant tables.
4. Monitor the performance after implementing the indexes to assess the improvements.

## Best practices

This section introduces some best practices for using the Index Insight feature.

### Regularly trigger Index Insight

To maintain optimized indexes, it is recommended to trigger the Index Insight feature periodically or whenever substantial changes occur in your queries or database schema.

### Analyze impact before implementing indexes

Before implementing the recommended indexes, analyze the potential impact on query execution plans, disk space, and any trade-offs involved. Prioritize implementing indexes that provide the most significant performance improvements.

### Monitor performance

Regularly monitor query performance after implementing the recommended indexes. This helps you confirm the improvements and make further adjustments if necessary.
