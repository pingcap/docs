---
title: Subscribe via Flashduty
summary: Learn how to monitor your TiDB cluster by getting alert notifications via Flashduty.
---

# Subscribe via Flashduty

TiDB Cloud provides you with an easy way to subscribe to alert notifications via Flashduty, [Slack](/tidb-cloud/monitor-alert-slack.md), [email](/tidb-cloud/monitor-alert-email.md), [Zoom](/tidb-cloud/monitor-alert-zoom.md), and [PagerDuty](/tidb-cloud/monitor-alert-pagerduty.md). This document describes how to subscribe to alert notifications via Flashduty.

> **Note:**
>
> Currently, alert subscription is available for [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) and [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters.

## Prerequisites

- The subscribing via Flashduty feature is only available for organizations that subscribe to the **Enterprise** or **Premium** [support plan](/tidb-cloud/connected-care-overview.md).

- To subscribe to alert notifications of TiDB Cloud, you must have the `Organization Owner` access to your organization or `Project Owner` access to the target project in TiDB Cloud.

## Subscribe to alert notifications

To receive alert notifications of clusters, take the following steps:

### Step 1. Generate a Flashduty webhook URL

1. Generate a webhook URL by following the instructions in [Flashduty Prometheus Integration](https://docs.flashcat.cloud/en/flashduty/prometheus-integration-guide).
2. Save the generated webhook URL to use in the next step.

### Step 2. Subscribe from TiDB Cloud

Alert notification subscriptions vary by cluster plan.

<CustomContent plan="dedicated">

> **Tip:**
>
> The alert subscription is for all alerts in the current project. If you have multiple clusters in the project, you just need to subscribe once.

1. In the [TiDB Cloud console](https://tidbcloud.com), switch to your target project using the combo box in the upper-left corner.
2. In the left navigation pane, click **Project Settings** > **Alert Subscription**.
3. On the **Alert Subscription** page, click **Add Subscriber** in the upper-right corner.
4. Select **Flashduty** from the **Subscriber Type** drop-down list.
5. Enter a name in the **Name** field and your Flashduty webhook URL in the **Webhook URL** field.
6. Click **Test Connection**.

    - If the test succeeds, the **Save** button is displayed.
    - If the test fails, an error message is displayed. Follow the message to troubleshoot the issue and retry the connection.

7. Click **Save** to complete the subscription.

</CustomContent>

<CustomContent plan="essential">

> **Tip:**
>
> The alert subscription is for all alerts in the current cluster. If you have multiple clusters, you need to subscribe to each cluster individually.

1. In the [TiDB Cloud console](https://tidbcloud.com), switch to your target cluster using the combo box in the upper-left corner.
2. In the left navigation pane, click **Settings** > **Alert Subscription**.
3. On the **Alert Subscription** page, click **Add Subscriber** in the upper-right corner.
4. Select **Flashduty** from the **Subscriber Type** drop-down list.
5. Enter a name in the **Name** field and your Flashduty webhook URL in the **Webhook URL** field.
6. Click **Test Connection**.

    - If the test succeeds, the **Save** button is displayed.
    - If the test fails, an error message is displayed. Follow the message to troubleshoot the issue and retry the connection.

7. Click **Save** to complete the subscription.

</CustomContent>

Alternatively, you can also click **Subscribe** in the upper-right corner of the **Alert** page of the cluster. You will be directed to the **Alert Subscription** page.

If an alert condition remains unchanged, the alert sends notifications every three hours.

## Unsubscribe from alert notifications

If you no longer want to receive alert notifications, take the following steps. The steps vary by cluster plan.

<CustomContent plan="dedicated">

1. In the [TiDB Cloud console](https://tidbcloud.com), switch to your target project using the combo box in the upper-left corner.
2. In the left navigation pane, click **Project Settings** > **Alert Subscription**.
3. On the **Alert Subscription** page, locate the row of your target subscriber to be deleted, and then click **...** > **Unsubscribe**.
4. Click **Unsubscribe** to confirm the unsubscription.

</CustomContent>

<CustomContent plan="essential">

1. In the [TiDB Cloud console](https://tidbcloud.com), switch to your target cluster using the combo box in the upper-left corner.
2. In the left navigation pane, click **Settings** > **Alert Subscription**.
3. On the **Alert Subscription** page, locate the row of your target subscriber to be deleted, and then click **...** > **Unsubscribe**.
4. Click **Unsubscribe** to confirm the unsubscription.

</CustomContent>
