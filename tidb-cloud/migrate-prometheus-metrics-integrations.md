---
title: Migrate Prometheus Integrations
summary: Learn how to migrate from the legacy project-level metrics integration to the new cluster-level Prometheus integrations.
---

# Migrate Prometheus Integrations

TiDB Cloud now manages Prometheus integrations at the cluster level, offering more granular control and configuration. The legacy project-level Prometheus integrations will be deprecated on December 31, 2025. If your organization is still using these legacy integrations, follow this guide to migrate to the new cluster-level Prometheus integrations to minimize disruptions to your metrics-related services.

## Prerequisites

- To set up third-party metrics integration for TiDB Cloud, you must have the `Organization Owner` or `Project Owner` access in TiDB Cloud.

## Migration steps

### Step 1. Delete the legacy project-level Prometheus integrations

1. In the [TiDB Cloud console](https://tidbcloud.com/), switch to the target project using the combo box in the upper-left corner.

2. In the left navigation panel, click **Project Settings** > **Integrations**.

3. On the **Integrations** page, click **Delete** next to **Integration to Prometheus**.

4. In the displayed dialog, type `Delete` to confirm the removal of the legacy integration.

### Step 2. Create the new Prometheus integration for each cluster

Repeat the following steps for each [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) cluster in the project.

1. In the [TiDB Cloud console](https://tidbcloud.com/), switch to the target cluster using the combo box in the upper-left corner.

2. In the left navigation panel, click **Settings** > **Integrations**.

3. On the **Integrations** page, create a new Prometheus integration. For more information, see [Integrate TiDB Cloud with Prometheus and Grafana](/tidb-cloud/monitor-prometheus-and-grafana-integration.md).

## Impact statement

Deleting the project-level integration immediately stops all clusters in the project from exposing metrics to the Prometheus endpoint. This results in a temporary loss of downstream data and interrupts integration-related services (such as monitoring and alerts) until you configure the new cluster-level Prometheus integrations.

## Contact support

For assistance, contact TiDB Cloud support at <a href="mailto:support@pingcap.com">support@pingcap.com</a> or reach out to your Technical Account Manager (TAM).
