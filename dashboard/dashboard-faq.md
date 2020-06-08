---
title: TiDB Dashboard FAQ
summary: Learn about the frequently asked questions (FAQs) and answers about TiDB Dashboard.
category: how-to
---

# TiDB Dashboard FAQ

This document summarizes the frequently asked questions (FAQs) and answers about TiDB Dashboard.

## Access TiDB Dashboard

### When the firewall or reverse proxy is configured, I am redirected to an internal address other than TiDB Dashboard

When multiple PD instances are deployed in a cluster, only one of the PD instances actually runs the TiDB Dashboard service. If you access other PD instances than this Dashboard-running one, your browser redirects you to another address. If the firewall or reverse proxy is not properly configured for accessing TiDB Dashboard, after the visiting the Dashboard, you might be redirected to an internal address that is protected by the firewall or reverse proxy.

- See [TiDB Dashboard Multi-PD Instance Deployment](/dashboard/dashboard-ops-deploy.md#) to learn the working principle of TiDB Dashboard with multiple PD instances.
- See [Use TiDB Dashboard through Reverse Proxy](/dashboard/dashboard-ops-reverse-proxy.md) to learn how to correctly configure reverse proxy.
- See [Improve TiDB Dashboard Security](/dashboard/dashboard-ops-security.md) to learn how to correctly configure the firewall.

### When dual network cards are deployed, TiDB Dashboard cannot be accessed using another network card

For security reasons, TiDB Dashboard on PD only monitors the IP addresses specified during deployment (that is, it only listens on one network card), nsot on `0.0.0.0`. Therefore, when multiple network cards are installed on the host, you cannot access TiDB Dashboard using another network card.

If you have deployed TiDB using the `tiup cluster` or `tiup playground` command, currently this problem cannot be solved. It is recommended that you use a reverse proxy to safely expose TiDB Dashboard to another network card. For details, see [Use TiDB Dashboard through Reverse Proxy](/dashboard/dashboard-ops-reverse-proxy.md).

## Interface feature

### `prometheus_not_found` error is shown in **QPS** and **Latency** sections on the Overview page

Monitoring metrics in **QPS** and **Latency** sections on the **Overview** page rely on the Prometheus monitoring instance that should have been deployed properly in the cluster. Errors are shown if Prometheus is not deployed. You can address this problem by deploying new Prometheus instance in the cluster.

If the Prometheus monitoring instance has been deployed but this error persists, the possible reason is that the version of your deployment tool (TiUP, TiDB Operator or TiDB Ansible) is old, and this tool does report monitoring addresses automatically, which makes TiDB Dashboard unable to perceive and query monitoring data. You can upgrade you deployment tool to the latest version and try again.

If your deployment tool is TiUP, take the following steps to solve this problem. For other deployment tools, refer to the corresponding documents of those tools.

1. Upgrade TiUP and TiUP Cluster:

    {{< copyable "shell-regular" >}}

    ```bash
    tiup update --self
    tiup update cluster --force
    ```

2. After the upgrade, when a new cluster is deployed with monitoring nodes, the monitoring metrics can be shown normally.

3. For an existing cluster, you can restart this cluster to report the monitoring addresses. Replace `CLUSTER_NAME` with the actual cluster name:

    {{< copyable "shell-regular" >}}

    ```bash
    tiup cluster start CLUSTER_NAME
    ```

   Even if the cluster has been started, still execute this command. This command does not affect the normal application in the cluster, but refreshes and reports the monitoring addresses, so that the monitoring metrics can be shown normally in TiDB Dashboard.

### `invalid connection` error is shown in **Top SQL Statements** and **Recent Slow Queries** on the Overview page

The possible reason is that you have enabled the `prepared-plan-cache` feature of TiDB. As an experimental feature, `prepared-plan-cache` might not function properly in some TiDB versions, which might cause this problem in TiDB Dashboard (and other applications) after being enabled. Disable `prepared-plan-cache` in [TiDB Configuration file](/tidb-configuration-file.md#prepared-plan-cache).