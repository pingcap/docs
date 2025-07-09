---
title: Subscribe via Email
summary: Learn how to monitor your TiDB cluster by getting alert notifications via Email.
---

# Subscribe via Email

TiDB Cloud provides you with an easy way to subscribe to alert notifications via email, [Slack](/tidb-cloud/monitor-alert-slack.md), and [Zoom](/tidb-cloud/monitor-alert-zoom.md). This document describes how to subscribe to alert notifications via email.

> **Note:**
>
> Currently, alert subscription is only available for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters.

## Prerequisites

- To subscribe to alert notifications of TiDB Cloud, you must have the `Organization Owner` access to your organization or `Project Owner` access to the target project in TiDB Cloud.

## Subscribe to alert notifications

> **Tip:**
>
> The alert subscription is for all alerts in the current project. If you have multiple clusters in the project, you just need to subscribe once.

To get alert notifications of clusters in your project, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com), switch to your target project using the combo box in the upper-left corner.
2. In the left navigation pane, click **Project Settings** > **Alert Subscription**.
3. On the **Alert Subscription** page, click **Add Subscriber** in the upper-right corner.
4. Select **Email** from the **Subscriber Type** drop-down list.
5. Enter your email address.
6. Click **Test Connection**.

    - If the test succeeds, the **Save** button is displayed.
    - If the test fails, an error message is displayed. Follow the message to troubleshoot the issue and then retry the connection.

7. Click **Save** to complete the subscription.

Alternatively, you can also click **Subscribe** in the upper-right corner of the [**Alert**](/tidb-cloud/monitor-built-in-alerting.md#view-alerts) page of the cluster. You will be directed to the **Alert Subscriber** page.

If an alert condition remains unchanged, the alert sends email notifications every three hours.

## Unsubscribe from alert notifications

If you no longer want to receive alert notifications of clusters in your project, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com), switch to your target project using the combo box in the upper-left corner.
2. In the left navigation pane, click **Project Settings** > **Alert Subscription**.
3. On the **Alert Subscription** page, locate the row of your target subscriber to be deleted, and then click **...** > **Unsubscribe**.
4. Click **Unsubscribe** to confirm the unsubscription.