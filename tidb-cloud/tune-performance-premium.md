---
title: Analyze and Tune Performance for Premium instances
summary: Learn how to analyze and tune performance of your TiDB Cloud Premium Instance.
aliases: ['/tidbcloud/index-insight']
---

# Analyze and Tune Performance for Premium instances

<CustomContent plan="premium">

TiDB Cloud provides [Slow Query](#slow-query) and [SQL Statement](#statement-analysis) to analyze performance.

</CustomContent>

- Slow Query lets you search and view all slow queries in your Premium Instance, and explore the bottlenecks of each slow query by viewing its execution plan, SQL execution information, and other details.

- SQL Statement enables you to directly observe the SQL execution on the page, and easily locate performance problems without querying the system tables.

## View the Diagnosis page

1. On the [**TiDB Instances**](https://tidbcloud.com/tidbs) page of your Organization, click the name of your target instance to go to its overview page.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations and Premium instances.

2. In the left navigation pane, click **Monitoring**.

## Slow Query

By default, SQL queries that take more than 300 milliseconds are considered as slow queries.

To view slow queries in a TiDB Instance, perform the following steps:

1. Navigate and click the **Slow Query** page of a TiDB instance.

2. Click any slow query in the list to display its detailed execution information.

3. (Optional) You can filter slow queries based on the target time range and SQL keywords. You can also limit the number of slow queries to be displayed.

The results are displayed in the form of a table, and you can sort the results by different columns.

## SQL Statement

To use the SQL Statement, perform the following steps:

1. Navigate and click the **SQL Statement** page of a TiDB instance.

2. Click any SQL Statement in the list to display its detailed execution information.

3. Select the time period to be analyzed in the time interval box. Then you can get the execution statistics of SQL statements of all databases in this period.

4. (Optional) If you only care about certain databases, you can select the corresponding schema(s) in the next box to filter the results.

The results are displayed in the form of a table, and you can sort the results by different columns.

