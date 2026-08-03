---
title: Migrate Prometheus Integrations
summary: Learn how to migrate from the legacy project-level Prometheus integration to the new cluster-level Prometheus integrations.
---

# Migrate Prometheus Integrations

TiDB Cloud now manages [Prometheus integrations](/tidb-cloud/monitor-prometheus-and-grafana-integration.md) at the cluster level, offering more granular control and configuration. The legacy project-level Prometheus integrations (Beta) will be deprecated on January 9, 2026. If your organization is still using these legacy integrations, follow this guide to migrate them to the new cluster-level Prometheus integrations to minimize disruptions to your metrics-related services.

## Prerequisites

- To set up third-party metrics integration for TiDB Cloud, you must have the `Organization Owner` or `Project Owner` access in TiDB Cloud.

## Migration steps

Do the following to migrate the Prometheus integration.

### Step 1. Delete the legacy project-level Prometheus integrations (Beta)

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [**My TiDB**](https://tidbcloud.com/tidbs) page of your organization, and then click the **Project view** tab.

    > **Tip:**
    >
    > If you are in multiple organizations, use the combo box in the upper-left corner to switch to your target organization first.

2. In the project view, locate your target project, and then click <MDSvgIcon name="icon-project-settings" /> for the project.

3. In the left navigation panel, click **Integrations** under **Project Settings**.

4. On the **Integrations** > **Integration to Prometheus (BETA)** module, select **Scrape_config Files** and click **Delete**.

5. In the displayed dialog, type `Delete` to confirm the removal of the legacy integration.

### Step 2. Create a new cluster-level Prometheus integration for each cluster

Repeat the following steps for each [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) cluster in the project.

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [**My TiDB**](https://tidbcloud.com/tidbs) page, and then click the name of your target TiDB Cloud Dedicated cluster to go to its overview page.

2. In the left navigation panel, click **Settings** > **Integrations**.

3. On the **Integrations** page, create a new Prometheus integration. For more information, see [Integrate TiDB Cloud with Prometheus and Grafana](/tidb-cloud/monitor-prometheus-and-grafana-integration.md).

## Impact of deleting the project-level Prometheus integration (Beta)

Deleting the project-level Prometheus integration (Beta) immediately stops all clusters in the project from exposing metrics to the Prometheus endpoint. This results in a temporary loss of downstream data and interrupts integration-related services (such as monitoring and alerts) until you configure new cluster-level Prometheus integrations.

## Contact support

For assistance, contact TiDB Cloud support at <a href="mailto:support@pingcap.com">support@pingcap.com</a> or reach out to your Technical Account Manager (TAM).
