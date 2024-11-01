---
title: TiProxy Monitoring Metrics
summary: Learn the monitoring items of TiProxy.
---

# TiProxy Monitoring Metrics

This document describes the monitoring items of TiProxy.

If you use TiUP to deploy the TiDB cluster, the monitoring system (Prometheus & Grafana) is deployed at the same time. For more information, see [Overview of the Monitoring Framework](/tidb-monitoring-framework.md).

The Grafana dashboard is divided into a series of sub dashboards which include Overview, PD, TiDB, TiKV, TiProxy, and Node\_exporter. A lot of metrics are there to help you diagnose. Each dashboard contains panel groups and their panels.

TiProxy has four panel groups. The metrics on these panels indicate the current status of TiProxy.

- **TiProxy-Server**: instance information.
- **TiProxy-Query-Summary**: SQL query metrics like CPS. 
- **TiProxy-Backend**: information on TiDB nodes that TiProxy might connect to.
- **TiProxy-Balance**: load balancing metrics.

## Server

- CPU Usage: the CPU utilization of each TiProxy instance
- Memory Usage: the memory usage of each TiProxy instance
- Uptime: the runtime of each TiProxy instance since last restart
- Connection Count: the number of clients connected to each TiProxy instance
- Create Connection OPM: the number of connections created on each TiProxy instance every minute
- Disconnection OPM: the number of disconnections for each reason every minute. Reasons include:
    - success: the client disconnects normally
    - client network break: the client does not send a `QUIT` command before it disconnects. It may also be caused by a network problem or the client shutting down
    - client handshake fail: the client fails to handshake with TiProxy
    - auth fail: the access is denied by TiDB
    - SQL error: TiDB returns other SQL errors
    - proxy shutdown: TiProxy is shutting down
    - malformed packet: TiProxy fails to parse the MySQL packet
    - get backend fail: TiProxy fails to find an available backend for the connection
    - proxy error: other TiProxy errors
    - backend network break: fails to read from or write to the TiDB. This may be caused by a network problem or the TiDB server shutting down
    - backend handshake fail: TiProxy fails to handshake with the TiDB server
- Goroutine Count: the number of Goroutines on each TiProxy instance

## Query-Summary

- Duration: average, P95, P99 SQL statement execution duration. It includes the duration of SQL statement execution on TiDB servers, so it is higher than the duration on the TiDB Grafana panel
- P99 Duration By Instance: P99 statement execution duration of each TiProxy instance
- P99 Duration By Backend: P99 statement execution duration of the statements that are executed on each TiDB instance
- CPS by Instance: command per second of each TiProxy instance
- CPS by Backend: command per second of each TiDB instance
- CPS by CMD: command per second grouped by SQL command type
- Handshake Duration: average, P95, and P99 duration of the handshake phase between the client and TiProxy

## Balance

- Backend Connections: connection counts between each TiDB instance and each TiProxy instance. For example, `10.24.31.1:6000 | 10.24.31.2:4000` indicates the connections between TiProxy instance `10.24.31.1:6000` and TiDB instance `10.24.31.2:4000`
- Session Migration OPM: the number of session migrations that happened every minute, recording sessions on which TiDB instance migrated to the other. For example, `succeed: 10.24.31.2:4000 => 10.24.31.3:4000` indicates the number of sessions that are successfully migrated from TiDB instance `10.24.31.2:4000` to TiDB instance `10.24.31.3:4000`
- Session Migration Duration: average, P95, P99 session migration duration.
- Session Migration Reasons: the number of session migrations that happened every minute and the reason for them. The reasons include the following:
    - `status`: TiProxy performed [status-based load balancing](/tiproxy/tiproxy-load-balance.md#status-based-load-balancing).
    - `label`: TiProxy performed [label-based load balancing](/tiproxy/tiproxy-load-balance.md#label-based-load-balancing).
    - `health`: TiProxy performed [health-based load balancing](/tiproxy/tiproxy-load-balance.md#health-based-load-balancing).
    - `memory`: TiProxy performed [memory-based load balancing](/tiproxy/tiproxy-load-balance.md#memory-based-load-balancing).
    - `cpu`: TiProxy performed [CPU-based load balancing](/tiproxy/tiproxy-load-balance.md#cpu-based-load-balancing).
    - `location`: TiProxy performed [location-based load balancing](/tiproxy/tiproxy-load-balance.md#location-based-load-balancing).
    - `conn`: TiProxy performed [connection count-based load balancing](/tiproxy/tiproxy-load-balance.md#connection-count-based-load-balancing).

## Backend

- Get Backend Duration: the average, p95, p99 duration of TiProxy connecting to a TiDB instance
- Ping Backend Duration: the network latency between each TiProxy instance and each TiProxy instance. For example, `10.24.31.1:6000 | 10.24.31.2:4000` indicates the network latency between TiProxy instance `10.24.31.1:6000` and TiDB instance `10.24.31.2:4000`
- Health Check Cycle: the duration of a cycle of the health check between a TiProxy instance and all TiDB instances. For example, `10.24.31.1:6000` indicates the duration of the latest health check that TiProxy instance `10.24.31.1:6000` executes on all the TiDB instances. If this duration is higher than 3 seconds, TiProxy may not be timely to refresh the backend TiDB list

## Traffic

- Bytes/Second from Backends: the amount of data, in bytes, sent from each TiDB instance to each TiProxy instance per second.
- Packets/Second from Backends: the number of MySQL packets sent from each TiDB instance to each TiProxy instance per second.
- Bytes/Second to Backends: the amount of data, in bytes, sent from each TiProxy instance to each TiDB instance per second.
- Packets/Second to Backends: the number of MySQL packets sent from each TiProxy instance to each TiDB instance per second.
- Cross Location Bytes/Second: the amount of data, in bytes, sent from each TiProxy instance to TiDB instances in different locations per second.
