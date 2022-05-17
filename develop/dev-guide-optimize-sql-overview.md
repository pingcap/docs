---
title: Optimize SQL Performance Overview
summary: Provides an overview of SQL performance tuning for TiDB application developers.
---

# Optimize SQL Performance Overview

This document introduces how to optimize the performance of SQL statements in TiDB. To get good performance, you can start with the following aspects:

* SQL performance tuning
* Schema design: Based on your application workload patterns, you might need to make some changes to the table schema to avoid transaction contention or hot spots.

## SQL performance tuning

To get good SQL statement performance, you can follow these guidelines:

* Scan as few rows as possible. It is recommended to scan only the data you need and avoid scanning excess data.
* Use the right index. Ensure that there is a corresponding index for the column in the `WHERE` clause in SQL. If not, the statement entails a full table scan and thus poor performance.
* Use the right join type. It is important to choose the right join type based on the relative size of the tables involved in the query. In general, TiDB's cost-based optimizer picks the best-performing join type. However, in a few cases, it might be better if the user manually specifies the join type.
* Use the right storage engine. For hybrid OLTP and OLAP workloads, the TiFlash engine is recommended. For details, see [HTAP Query](/develop/dev-guide-hybrid-oltp-and-olap-queries.md).

## Schema design

After [tuning SQL performance](#sql-performance-tuning), if your application still cannot get good performance, you might need to check your schema design and data access patterns to avoid the following issues:

* Transaction contention. For how to diagnose and resolve transaction contention, see [Troubleshoot Lock Conflicts](/troubleshoot-lock-conflicts.md).
* Hot spots. For how to diagnose and resolve hot spots, see [Troubleshoot Hotspot Issues](/troubleshoot-hot-spot-issues.md).

### See also

* [SQL Performance Tuning](/sql-tuning-overview.md)
