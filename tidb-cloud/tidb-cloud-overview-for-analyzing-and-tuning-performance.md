---
title: Overview for Analyzing and Tuning Performance
summary: Learn about how to analyze and tune SQL performance in TiDB Cloud.
---

# Overview for Analyzing and Tuning Performance

This document describes steps to help you analyze and tune SQL performance in TiDB Cloud.

## User response time

User response time indicates how long an application takes to return the results of a request to users. As you can see from the following sequential timing diagram, the time of a typical user request contains the following:

- The network latency between the user and the application
- The processing time of the application
- The network latency during the interaction between the application and the database
- The service time of the database

The user response time is affected by various subsystems on the request chain, such as network latency and bandwidth, number and request types of concurrent users, and resource usage of server CPU and I/O. To optimize the entire system effectively, you need to first identify the bottlenecks in user response time.

To get a total user response time within a specified time range (`ΔT`), you can use the following formula:

Total user response time in `ΔT` = Average TPS (Transactions Per Second) x Average user response time x `ΔT`.

![user_response_time](/media/performance/user_response_time_en.png)

## Relationship between user response time and system throughput

User response time consists of service time, queuing time, and concurrent waiting time to complete a user request.

```
User Response time = Service time + Queuing delay + Coherency delay
```

- Service time: the time a system consumes on certain resources when processing a request, for example, the CPU time that a database consumes to complete a SQL request.
- Queuing delay: the time a system waits in a queue for service of certain resources when processing a request.
- Coherency delay: the time a system communicates and collaborates with other concurrent tasks, so that it can access shared resources when processing a request.

System throughput indicates the number of requests that can be completed by a system per second. User response time and throughput are usually inverse of each other. When the throughput increases, the system resource utilization and the queuing latency for a requested service increase accordingly. Once resource utilization exceeds a certain inflection point, the queuing latency will increase dramatically.

For example, for a database system running OLTP loads, after its CPU utilization exceeds 65%, the CPU queueing scheduling latency increases significantly. This is because concurrent requests of a system are not completely independent, which means that these requests can collaborate and compete for shared resources. For example, requests from different users might perform mutually exclusive locking operations on the same data. When the resource utilization increases, the queuing and scheduling latency increases too, which causes that the shared resources cannot be released in time and in turn prolongs the waiting time for shared resources by other tasks.

## Troubleshooting Steps

There are several pages on the TiDB Cloud console that help you troubleshoot user response time.

- **Overview**: on this tab, you can view TiDB metrics. Currently, the metrics include Total QPS, Latency, Connections, TiFlashbeta Request QPS, TiFlashbeta Request Duration, TiFlashbeta Storage Size, TiKV Storage Size, TiDB CPU, TiKV CPU, TiKV IO Read, and TiKV IO Write.
- **Diagnosis**:
    - **Statement** enables you to directly observe the SQL execution on the page, and easily locate performance problems without querying the system tables. You can click on a SQL statement to further view the execution plan of the query for troubleshooting and analysis. For more information about SQL performance tuning, see [SQL Tuning Overview](/tidb-cloud/tidb-cloud-sql-tuning-overview.md).
    - **Key Visualizer** helps you observe TiDB's data access patterns and data hotspots.

If you require additional metrics, you can contact the PingCAP support team.

If you experience latency and performance issues that are not as expected, consider steps in the following sections for analysis and troubleshooting.
