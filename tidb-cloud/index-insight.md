---
title: Index Insight (Beta)
summary: Learn how to use the Index Insight feature in TiDB Cloud and obtain index recommendations for your slow queries.
---

# Index Insight (Beta)

The Index Insight (beta) feature in TiDB Cloud provides powerful capabilities to optimize query performance by offering index recommendations for slow queries that are not using indexes effectively. This document walks you through the steps to enable and utilize the Index Insight feature effectively.

> **Note:**
>
> Index Insight is currently in beta and only available for [TiDB Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) clusters.

## Introduction

The Index Insight feature provides you with the following benefits:

- Enhanced query performance: By identifying and suggesting appropriate indexes for slow queries, you can significantly enhance query execution speed, resulting in quicker response times and a better user experience.
- Cost efficiency: Optimized query performance reduces the need for extra computing resources, enabling you to achieve more with existing infrastructure and potentially leading to operational cost savings.
- Simplified optimization process: Index Insight simplifies the process of identifying and implementing index improvements, eliminating the need for manual analysis and guesswork. You can get accurate recommendations using this feature, which saves time and effort.
- Improved application efficiency: By optimizing database performance, applications running on TiDB Cloud can handle larger workloads and serve more users concurrently, which enables businesses to scale operations effectively.

## Usage

This section introduces how to enable the Index Insight feature and obtain recommended indexes for your slow queries.

### Before you begin

Before enabling the Index Insight feature, make sure that you have created a TiDB Dedicated cluster. If you do not have one, follow the steps in [Create a cluster](/tidb-cloud/create-tidb-cluster.md) to create one.

### Step 1: Enable Index Insight

1. In the [TiDB Cloud console](https://tidbcloud.com), navigate to the cluster overview page of your TiDB Dedicated cluster, and then click **Diagnosis** in the left navigation pane.

2. Click the **Index Insight BETA** tab. The **Index Insight overview** page is displayed.

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

To obtain index recommendations for your slow queries, you can manually trigger the Index Insight feature by clicking **Check Up** in the upper-right corner of the **Index Insight overview** page.

Then, the feature begins scanning your slow queries from the past three hours. After the scan finishes, it provides a list of index recommendations based on its analysis.

### Step 3: View index recommendations

To view the details of a specific index recommendation, click the insight from the list. The **Index Insight Detail** page is displayed.

On this page, you can find the index recommendations, related slow queries, execution plans, and relevant metrics. This information helps you better understand the performance issues and evaluate the potential impact of implementing the index recommendations.

### Step 4: Implement index recommendations

Before implementing the index recommendations, you need to first review and evaluate the recommendations from the **Index Insight Detail** page.

To implement the index recommendations, follow these steps:

1. Evaluate the impact of the proposed index on existing queries and workload.
2. Consider the storage requirements and potential trade-offs associated with the index implementation.
3. Use appropriate database management tools to create the index recommendations on the relevant tables.
4. Monitor the performance after implementing the indexes to assess the improvements.

## Best practices

This section introduces some best practices for using the Index Insight feature.

### Regularly trigger Index Insight

To maintain optimized indexes, it is recommended to trigger the Index Insight feature periodically or whenever substantial changes occur in your queries or database schema.

### Analyze impact before implementing indexes

Before implementing the index recommendations, analyze the potential impact on query execution plans, disk space, and any trade-offs involved. Prioritize implementing indexes that provide the most significant performance improvements.

### Monitor performance

Regularly monitor query performance after implementing the index recommendations. This helps you confirm the improvements and make further adjustments if necessary.

## FAQ

### How to delete user after deactivate index insight?

Once index insight is deactivated, you can proceed to delete the SQL user. You can use the DROP USER statement. For example: `DROP USER 'username'@'host';`. Replace 'username' with the name of the user you want to delete and 'host' with the specific host associated with the user. If the user is associated with multiple hosts, you may need to execute the DROP USER statement for each host separately.

### Why am I getting the 'invalid user or password' system message when I try to activate or perform a check-up on index insight?

The "invalid user or password" system message typically indicates that the credentials you provided for authentication are incorrect or not recognized by the system. This issue can occur for various reasons, such as: incorrect username or password, expired or locked account.

To troubleshoot and resolve the "invalid user or password" prompt, consider the following steps:

- Verify your credentials: Double-check that you are using the correct username and password combination. Pay attention to any case sensitivity requirements.
- Confirm account status: Ensure that your user account is active and not expired or locked. Contact the system administrator or the relevant support channel to confirm your account status.
- Create a new SQL user: If none of the above steps work, you can try creating a new SQL user.

If you have gone through the above steps and are still unable to resolve the issue, it's recommended to seek assistance from the support for further troubleshooting and guidance.

### Why am I getting the 'no sufficient privileges' system message when I try to activate or perform a check-up on index insight?

The "no sufficient privileges" system message typically indicates that the user account you are using does not have the necessary permissions or privileges to perform the requested action on Index Insight. To troubleshoot and resolve the "no sufficient privileges" issue, consider the following steps:

- Check your user privileges: Verify if your user account has been granted the necessary privileges for activating or performing check-ups on Index Insight.
- Create a new SQL user: If none of the above steps work, you can try creating a new SQL user.

If you have gone through the above steps and are still unable to resolve the issue, it's recommended to seek assistance from the support for further troubleshooting and guidance.

### Why am I getting the 'operations may be too frequent' during using index insight?

The "operations may be too frequent" message typically indicates that you have exceeded the rate limit or usage limits imposed by the Index Insight system. To troubleshoot and resolve the "operations may be too frequent" issue, consider the following steps:

- Slow down operations: If you receive this message, it's an indication that you need to reduce the frequency of your operations on Index Insight.
- Contact support: It's recommended to seek assistance from the support team. Provide them with the specific details of the error message, the actions you were performing when the error occurred, and any other relevant information. The support team will have access to system logs and can provide further troubleshooting and guidance tailored to your situation.

### Why am I getting the 'internal error' during using index insight?

The "internal error" message typically indicates that an unexpected error or issue has occurred within the Index Insight system. This error message is generic and doesn't provide specific details about the underlying cause. To troubleshoot and resolve the "internal error" issue, consider the following steps:

- Retry the action: First, try refreshing the page or performing the action again. Sometimes, the error may be temporary and can be resolved by retrying.
- Contact support: It's recommended to seek assistance from the support team. Provide them with the specific details of the error message, the actions you were performing when the error occurred, and any other relevant information. The support team will have access to system logs and can provide further troubleshooting and guidance tailored to your situation.
