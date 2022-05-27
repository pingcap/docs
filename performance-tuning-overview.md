---
title: Performance Tuning Overview
summary: This document introduces the basic concepts of performance tuning, such as user response time, throughput, and database time, and also provides a general process for performance tuning.
---

# TiDB Performance Tuning Overview

This document introduces the basic concepts of performance tuning, such as user response time, throughput, and database time, and also provides a general process for performance tuning.

## User response time and database time

### User response time

User response time indicates how long an application takes to return the results of a request to users. As you can see from the following processing timing diagram, the time of a typical user request contains the network latency between the user and the application, the processing time of the application, the network latency during the interaction between the application and the database, and the service time of the database. The user response time is affected by various subsystems on the request chain, such as network latency and bandwidth, number and request types of concurrent users, and resource usage of server CPU and I/O. To optimize the entire system effectively, you need to first locate the bottlenecks in user response time.

To get a total user response time within a specified time range (`ΔT`), you can use the following formula:

Total user response time in `ΔT` = Average TPS (Transactions Per Second) x Average user response time x `ΔT`.

! [user_response_time](/media/performance/user_response_time_cn.png)

### Database time

Database time indicates how long a database takes to provide services. The database time in `ΔT` is the sum of the time that a database takes to process all application requests concurrently.

To get the database time, you can use any of the following methods:

- Method 1: Multiply the average query latency by QPS and by ΔT, that is, `DB Time in ΔT = QPS × avg latency × ΔT`
- Method 2: Multiply the average number of active sessions by ΔT, that is, `DB Time in ΔT  = avg active connections × ΔT`
- Method 3: Calculate the time based on the TiDB internal Prometheus metric TiDB_server_handle_query_duration_seconds_sum, that is. `ΔT DB Time = rate(TiDB_server_handle_query_duration_seconds_sum) × ΔT`

## Relationship between user response time and system throughput

User response time consists of service time, queuing time, and concurrent waiting time to complete a user request.

```
User Response time = Service time + Queuing delay + Coherency delay
```

- Service Time: the time that an application consumes on certain resources when processing a request, for example, the CPU time that a database consumes to complete a SQL request.
- Queuing delay: the time that an application waits in a queue so that it can be scheduled by a service of certain resources when processing a request.
- Coherency delay: the time that an application communicates and collaborates with other concurrent tasks so that it can access shared resources when processing a request.

System throughput refers to the number of requests completed by the system per second. User response time and throughput are usually inversely inverse of each other. As throughput rises, system resource utilization rises and queuing latency for the requested service rises, and when resource utilization exceeds a certain inflection point, queuing latency rises dramatically.

For example, for database systems running OLTP loads, CPU queueing scheduling latency increases significantly after CPU utilization exceeds 65%. Because the concurrent requests of the system are not completely independent, there is collaboration and contention for shared resources between requests, e.g., different database requests may have mutually exclusive locking operations on the same data. When the resource utilization rises, the queuing and scheduling latency rises, which will result in the shared resources held not being released in time, which in turn prolongs the waiting time for shared resources by other tasks.

## performance tuning Process

The performance tuning process consists of the following 6 steps.

1. Defining the optimization objective
2. Establishing a performance baseline
3. Locating bottlenecks in user response times
4. Propose optimization options, estimating the benefits, risks and costs of each option
5. Implementation optimization
6. Evaluation of optimization results

A performance tuning project often requires multiple iterations of steps 2 through 6 to achieve the optimization goal.

### Step 1: Define the optimization objective

Optimization goals differ for different types of systems. For example, for a financial core OLTP system, the optimization goal may be to reduce the long-tail latency of transactions; for a financial settlement system, the optimization goal may be to make better use of hardware resources and reduce batch settlement task times.

A good optimization goal should be easily quantifiable, e.g.

- Good optimization goal: "The p99 latency for transfer transactions needs to be less than 200 ms during peak business hours of 9am to 10am"
- Poor optimization goal: "The system is too slow and unresponsive and needs to be optimized"

Defining a clear optimization goal helps guide subsequent performance tuning efforts.

### Step 2: Establish a performance baseline

To perform performance tuning efficiently, you need to capture current performance data to establish a performance baseline. The performance data that needs to be captured typically contains the following.

- Mean and long-tail values of user response time, application system throughput
- Database performance data such as database time, Query latency and QPS.

    TiDB has refined measurements and storage for different dimensions of performance data, such as [slow logs](/identify-slow-queries.md), [Top SQL](/dashboard/top-sql.md), [continuous performance profiling capabilities](/dashboard//continuous- profiling.md), and [traffic visualization](/dashboard/dashboard-key-visualizer.md), among others. In addition, you can perform historical backtracking and comparison of the timing metrics data stored in Prometheus.

- Resource utilization, including CPU, IO, and network resources
- Configuration information, such as application, database and operating system configuration

### Step 3: Locate bottlenecks in user response time

Locate or speculate on bottlenecks in user response times based on data from the performance baseline.

Implementations often do not have complete measurement and documentation of the links requested by the user, so you cannot effectively decompose the user response time from top to bottom through the application.

In contrast, performance metrics such as query latency and throughput are very well documented within the database. Based on database time, you can determine if the bottleneck in user response time is in the database.

- If the bottleneck is not in the database, you need to rely on the resource utilization collected outside the database or profile the application to identify the bottleneck outside the database. Common scenarios include insufficient application or proxy server resources, applications with serial points that cannot fully utilize hardware resources, etc.
- If bottlenecks exist in the database, you can perform internal database performance analysis and diagnosis through the database's comprehensive tuning tools. Common scenarios include the presence of slow SQL, applications using the database in an unreasonable manner, and the presence of read and write hotspots in the database.

For specific analysis and diagnostic methods and tools, please refer to [performance-optimization-methods](/performance-tuning-methods.md).

### Step 4: Propose optimization options, assessing the benefits, risks and costs of each option

After identifying the bottleneck points of the system through performance analysis, an optimization solution is proposed that is cost effective, low risk, and provides the maximum benefit based on the actual situation.

According to [Amdahl's Law](https://zh.wikipedia.org/wiki/%E9%98%BF%E5%A7%86%E8%BE%BE%E5%B0%94%E5%AE%9A%E5%BE%8B), the maximum gain from performance tuning depends on the percentage of the optimized part of the overall system. Therefore, you need to identify the system bottlenecks and the corresponding share based on the performance data, and predict the gains after the bottleneck is resolved or optimized.

It is important to note that even if the potential benefits of optimizing a particular solution for the largest bottleneck point are greatest, the risks and costs of that solution need to be evaluated as well. For example.

- The most straightforward optimization solution for resource-overloaded systems is to expand the capacity, but in practice the expansion solution may be too costly to be adopted.
- When a slow SQL in a business module causes a slow response time for the entire module, the solution of upgrading to a new version of the database can solve the slow SQL problem, but it may also affect modules that did not have the problem, so this solution may have a potentially high risk. A low-risk solution is to rewrite the existing slow SQL without upgrading the database version and resolve the problem in the current database version.

### Step 5: Implement optimization

Considering the benefits, risks and costs, one or more optimization options are selected for implementation, and changes to the production system are thoroughly prepared and well documented.

To mitigate risk and validate the benefits of the optimization solution, it is recommended that the changes be validated and fully regressed in a test and quasi-production environment. For example, for slow SQL for a query business, if the selected optimization solution is to create a new index to optimize the access path of the query, you need to ensure that the new index does not introduce significant write hotspots in the existing data insertion business, causing the rest of the business to slow down.

### Step 6: Evaluate optimization results

After implementing the optimization, the results need to be evaluated.

- If the optimization goal is met, the entire optimization project is successfully completed.
- If the optimization goal is not reached, you need to repeat steps 2 through 6 until the optimization goal is reached.

After reaching your optimization goals, you may need to further plan the capacity of your system in order to handle the growth of your business.