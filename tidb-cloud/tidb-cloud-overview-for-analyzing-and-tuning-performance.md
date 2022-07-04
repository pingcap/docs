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