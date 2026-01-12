---
title: TiDB Monitoring API Overview
summary: Learn the API of TiDB monitoring services.
---

# TiDB Monitoring API Overview

The TiDB monitoring framework adopts two open source projects: Prometheus and Grafana. TiDB uses [Prometheus](https://prometheus.io) to store the monitoring and performance metrics and [Grafana](https://grafana.com/grafana) to visualize these metrics. TiDB also provides a built-in [TiDB Dashboard](/dashboard/dashboard-intro.md) for monitoring and diagnosing TiDB clusters.

You can use the following types of interfaces to monitor the TiDB cluster status:

- [Status interface](/tidb-monitoring-api.md#use-the-status-interface): monitor the [running status](/tidb-monitoring-api.md#running-status) of the current TiDB server and the [storage information](/tidb-monitoring-api.md#storage-information) of a table.
- [Metrics interface](/tidb-monitoring-api.md#use-the-metrics-interface): get detailed information about various operations in components and view these metrics using Grafana.

For more information about each API, including request parameters, response examples, and usage instructions, see [TiDB Monitoring API](/tidb-monitoring-api.md).
