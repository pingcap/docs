---
title: Monitor the TiProxy Cluster
summary: Learn the monitoring items of TiProxy.
aliases: ['/docs/dev/tiproxy/monitor-tiproxy/','/docs/dev/reference/tiproxy/monitor/']
---

# TiProxy Monitoring Metrics

This document describes the monitoring items of TiProxy.

If you use TiUP to deploy the TiDB cluster, the monitoring system (Prometheus & Grafana) is deployed at the same time. For more information, see [Overview of the Monitoring Framework](/tidb-monitoring-framework.md).

The Grafana dashboard is divided into a series of sub dashboards which include Overview, PD, TiDB, TiKV, TiProxy, and Node\_exporter. A lot of metrics are there to help you diagnose. Each dashboard contains panel groups and their panels.

TiProxy has four panel groups. The metrics on these panels indicate the current status of TiProxy.

- **TiProxy-Server**: instance information.
- **TiProxy-Query-Summary**: SQL query metrics like CPS. 
- **TiProxy-Backend**: information on TiDB nodes that TiProxy might connect to.
- **TiProxy-Balance**: loadbalance mertrics.

## Server

- CPU Usage: The CPU utilization per TiProxy instance.
- Memory Usage: The memory usage per TiProxy instance.
- Uptime: The runtime of TiProxy since last restart.
- Goroutine Count: Running goroutine count of TiProxy instance.
- Connection Count: SQL connections that TiProxy instance serve.

## Query-Summary

- Duration: average, p95, p99 SQL statement execution duration.
- CPS by Instance: command per second of all TiProxy instances.
- CPS by Backend: command per second of all TiDB instances.
- CPS by CMD: command per second grouped by SQL command type.

## Balance

- Backend Connections: connection counts between each TiDB instance and each TiProxy instance. 
- Session Migrations: session migrations happened on all TiProxy instances, recording sessions on which TiDB instance migrated to the other.
- Session Migration Duration: average, p95, p99 session migration duration.

## Backend

- Get Backend Count: how many times did TiProxy instances try to connect the backend.
- Get Backend Duration: average, p95, p99 duration of connecting backend, useful for debugging why TiProxy cant establish healthy connections.
- Ping Backend Duration: latencies between each TiDB instance and each TiProxy instance.
