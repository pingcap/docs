---
title: Optimize SQL Performance Overview
summary: Provides an overview of SQL performance tuning for TiDB.
---

# Optimize SQL Performance Overview

This section introduce how to optimize the performance of SQL in TiDB. To get good performance, you can start with the following:

* SQL Performance Tuning
* Schema design: Depending on your SQL schema and the data access patterns of your workload, you may need to make some changes to the table's schema in order to avoid transaction contention or hot spots.

## SQL Performance Tuning

To get good SQL statement performance, you can follow these guidelines:

* Scan as few rows as possible. It's best to scan only the data you need and avoid scanning excess data.
* Use right index, you need to ensure that there is a corresponding index for the column in the `WHERE` clause in SQL, otherwise it will be a full table scan, and the performance will be poor.
* Use the right join type. Depending on the relative size of the tables in the query, it is also important to choose the right join type. In general, TiDB's cost-base optimizer should pick the best-performing join type. However, in a few cases it may be better for the user to specify the join type manually.
* Use the right storage engine. For mixed OLTP and OLAP workloads, the TiFlash engine is recommended. For details, see [HTAP Query](/develop/hybrid-oltp-and-olap-queries.md).

## Schema Design

If you still not get good performance after tuning according to [SQL Performance Tuning](#sql-performance-tuning), you may need to check your schema design and data access patterns to make sure you avoid the following issues:

* Transaction contention. For how to diagnose and resolve transaction contention, see [Troubleshoot Lock Conflicts](/troubleshoot-lock-conflicts.md).
* Hot spots. For how to diagnose and resolve hot spots, see [Troubleshoot Hotspot Issues](/troubleshoot-hot-spot-issues.md).

### See Also

* [SQL Performance Tuning](/sql-tuning-overview.md)
