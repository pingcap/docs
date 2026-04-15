---
title: Subscribe via PagerDuty
summary: Learn how to monitor TiDB by getting alert notifications via PagerDuty.
---

# Subscribe via PagerDuty

TiDB Cloud provides you with an easy way to subscribe to alert notifications via PagerDuty, [Slack](/tidb-cloud/monitor-alert-slack.md), [email](/tidb-cloud/monitor-alert-email.md), [Zoom](/tidb-cloud/monitor-alert-zoom.md), and [Flashduty](/tidb-cloud/monitor-alert-flashduty.md). This document describes how to subscribe to alert notifications via PagerDuty.

> **Note:**
>
> Currently, alert subscription is available for [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) instances and [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters.

## Prerequisites

- The subscribing via PagerDuty feature is only available for organizations that subscribe to the **Enterprise** or **Premium** [support plan](/tidb-cloud/connected-care-overview.md).

- To subscribe to alert notifications of TiDB Cloud, you must have the `Organization Owner` access to your organization or `Project Owner` access to the target project in TiDB Cloud.

## Subscribe to alert notifications

To receive alert notifications, take the following steps:

### Step 1. Generate a PagerDuty integration key

1. Generate an integration key of type **Events API v2** by following the instructions in the [PagerDuty Events API v2 Overview](https://developer.pagerduty.com/docs/events-api-v2-overview#getting-started).
2. Save the generated integration key to use in the next step.

### Step 2. Subscribe from TiDB Cloud

Alert notification subscriptions vary by [your TiDB Cloud plan](/tidb-cloud/select-cluster-tier.md).

<CustomContent plan="dedicated">

> **Tip:**
>
> For {{{ .dedicated }}}, the alert subscription is for all alerts in the current project. If you have multiple {{{ .dedicated }}} clusters in the project, you just need to subscribe once.

1. In the [TiDB Cloud console](https://tidbcloud.com), navigate to the [**My TiDB**](https://tidbcloud.com/tidbs) page of your organization, and then click the **Project view** tab.
2. In the project view, locate your target project, and then click <MDSvgIcon name="icon-project-settings" /> for the project.
3. In the left navigation pane, click **Alert Subscription** under **Project Settings**.
4. On the **Alert Subscription** page, click **Add Subscriber** in the upper-right corner.
5. Select **PagerDuty** from the **Subscriber Type** drop-down list.
6. Enter a name in the **Name** field and your PagerDuty integration key in the **Integration Key** field.
7. Click **Test Connection**.

    - If the test succeeds, the **Save** button is displayed.
    - If the test fails, an error message is displayed. Follow the message to troubleshoot the issue and retry the connection.

8. Click **Save** to complete the subscription.

Alternatively, you can also click **Subscribe** in the upper-right corner of the **Alert** page of the {{{ .dedicated }}} cluster. You will be directed to the **Alert Subscription** page.

</CustomContent>

<CustomContent plan="essential">

> **Tip:**
>
> For {{{ .essential }}}, the alert subscription is for all alerts in the current instance. If you have multiple instances, you need to subscribe to each instance individually.

1. In the [TiDB Cloud console](https://tidbcloud.com), navigate to the [**My TiDB**](https://tidbcloud.com/tidbs) page of your organization, and then click the name of your target {{{ .essential }}} instance to go to its overview page.
2. In the left navigation pane, click **Settings** > **Alert Subscription**.
3. On the **Alert Subscription** page, click **Add Subscriber** in the upper-right corner.
4. Select **PagerDuty** from the **Subscriber Type** drop-down list.
5. Enter a name in the **Name** field and your PagerDuty integration key in the **Integration Key** field.
6. Click **Test Connection**.

    - If the test succeeds, the **Save** button is displayed.
    - If the test fails, an error message is displayed. Follow the message to troubleshoot the issue and retry the connection.

7. Click **Save** to complete the subscription.

Alternatively, you can also click **Subscribe** in the upper-right corner of the **Alert** page of the {{{ .essential }}} instance. You will be directed to the **Alert Subscription** page.

</CustomContent>

If an alert condition remains unchanged, the alert sends notifications every three hours.

## Unsubscribe from alert notifications

If you no longer want to receive alert notifications, take the following steps. The steps vary by [your TiDB Cloud plan](/tidb-cloud/select-cluster-tier.md).

<CustomContent plan="dedicated">
    
1. In the [TiDB Cloud console](https://tidbcloud.com), navigate to the [**My TiDB**](https://tidbcloud.com/tidbs) page of your organization, and then click the **Project view** tab.
2. In the project view, locate your target project, and then click <MDSvgIcon name="icon-project-settings" /> for the project.
3. In the left navigation pane, click **Alert Subscription** under **Project Settings**.
4. On the **Alert Subscription** page, locate the row of your target subscriber to be deleted, and then click **...** > **Unsubscribe**.
5. Click **Unsubscribe** to confirm the unsubscription.

</CustomContent>

<CustomContent plan="essential">

1. In the [TiDB Cloud console](https://tidbcloud.com), navigate to the [**My TiDB**](https://tidbcloud.com/tidbs) page of your organization, and then click the name of your target {{{ .essential }}} instance to go to its overview page.
2. In the left navigation pane, click **Settings** > **Alert Subscription**.
3. On the **Alert Subscription** page, locate the row of your target subscriber to be deleted, and then click **...** > **Unsubscribe**.
4. Click **Unsubscribe** to confirm the unsubscription.

</CustomContent>
