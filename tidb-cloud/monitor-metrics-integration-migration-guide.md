---
title: Migrate Datadog and New Relic Integrations
summary: Learn how to migrate from the legacy to the new metrics integration for Datadog and New Relic.
---

# Metrics Integration Migration Guide

New metrics integration is now managed at the individual cluster level, providing more granular control and configuration. The legacy project-level metrics integration for Datadog and New Relic will be deprecated. This guide provides detailed instructions for migrating from the legacy project-level integration to the new cluster-level integration, for Datadog and New Relic.

## Prerequisites

- To set up third-party metrics integration for TiDB Cloud, you must have the `Organization Owner` or `Project Owner` access in TiDB Cloud.

## Migration Steps

### Step 1. Disable the Legacy Project-Level Integration

1. In the [TiDB Cloud console](https://tidbcloud.com/), switch to the target project using the combo box in the upper-left corner.

2. In the left navigation panel, click **Project Settings** > **Integrations**.

3. On the **Integrations** page, click the `Delete` button to the right of the **Integration to Datadog** row or the **Integration to New Relic** row.

4. Type "**Delete**" in the pop-up window to confirm deletion of the legacy integration.

### Step 2. Enable the new integration for each cluster

Repeat the following steps for each dedicated cluster under the project to create a new integration.

1. In the [TiDB Cloud console](https://tidbcloud.com/), switch to the target cluster using the combo box in the upper-left corner.

2. In the left navigation panel, click **Settings** > **Integrations**.

3. On the **Integrations** page, create new integrations on demand. For more details on how to create integrations, see [Integrate TiDB Cloud with Datadog](/tidb-cloud/monitor-datadog-integration.md) and [Integrate TiDB Cloud with New Relic](/tidb-cloud/monitor-new-relic-integration.md).

## Impact Statement

Deleting the project-level integration immediately stops all clusters under the project from sending metrics downstream. This causes a temporary loss of downstream data and interrupts integration-related services (such as monitoring and alerts) until you create the new integration.

## Contact support

For help or questions, please contact TiDB Cloud support at <a href="mailto:support@pingcap.com">support@pingcap.com</a> or reach out to your Technical Account Manager (TAM).
