---
title: Subscribe via Slack
summary: Learn how to monitor your TiDB cluster by getting alert notifications via Slack.
---

# Subscribe via Slack

TiDB Cloud provides you with an easy way to subscribe to alert notifications via Slack, [email](/tidb-cloud/monitor-alert-email.md), [Zoom](/tidb-cloud/monitor-alert-zoom.md), [Flashduty](/tidb-cloud/monitor-alert-flashduty.md), and [PagerDuty](/tidb-cloud/monitor-alert-pagerduty.md). This document describes how to subscribe to alert notifications via Slack.

> **Note:**
>
> Currently, alert subscription is available for [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) instances, [TiDB Cloud Premium](/tidb-cloud/select-cluster-tier.md#premium) instances, and [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters.

## Prerequisites

- The subscribing via Slack feature is only available for organizations that subscribe to the **Enterprise** or **Premium** support plan.

<CustomContent plan="essential,dedicated">

- To subscribe to alert notifications of TiDB Cloud, you must have the `Organization Owner` access to your organization or `Project Owner` access to the target project in TiDB Cloud.

</CustomContent>

<CustomContent plan="premium">

- To subscribe to alert notifications of TiDB Cloud, you must have the `Organization Owner` access to your organization or `Instance Manager` access to the target {{{ .premium }}} instance in TiDB Cloud.

</CustomContent>

## Subscribe to alert notifications

### Step 1. Generate a Slack webhook URL

1. [Create a Slack app](https://api.slack.com/apps/new), if you do not have one already. Click **Create New App**, and choose **From scratch**. Enter a name, choose a workspace to associate your app with, and then click **Create App**.
2. Go to the settings page for your app. You can load its settings via your [app's management dashboard](https://api.slack.com/apps).
3. Click the **Incoming Webhooks** tab, and then toggle **Activate Incoming Webhooks** to **ON**.
4. Click **Add New Webhook to Workspace**.
5. Select a channel that you want to receive alert notifications in, and then select **Authorize**. If you need to add the incoming webhook to a private channel, you must first be in that channel.

You can see a new entry under the **Webhook URLs for Your Workspace** section in the following format: `https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX`.

### Step 2. Subscribe from TiDB Cloud

Alert notification subscriptions vary by [your TiDB Cloud plan](/tidb-cloud/select-cluster-tier.md).

<CustomContent plan="dedicated">

To subscribe to alert notifications of {{{ .dedicated }}} clusters, take the following steps:

> **Tip:**
>
> For {{{ .dedicated }}}, the alert subscription is for all alerts in the current project. If you have multiple {{{ .dedicated }}} clusters in the project, you just need to subscribe once.

1. In the [TiDB Cloud console](https://tidbcloud.com), navigate to the [**My TiDB**](https://tidbcloud.com/tidbs) page of your organization, and then click the **Project view** tab.
2. In the project view, locate your target project, and then click <MDSvgIcon name="icon-project-settings" /> for the project.
3. In the left navigation pane, click **Alert Subscription** under **Project Settings**.
4. On the **Alert Subscription** page, click **Add Subscriber** in the upper-right corner.
5. Select **Slack** from the **Subscriber Type** drop-down list.
6. Enter a name in the **Name** field and your Slack webhook URL in the **URL** field.
7. Click **Test Connection**.

    - If the test succeeds, the **Save** button is displayed.
    - If the test fails, an error message is displayed. Follow the message to troubleshoot the issue and retry the connection.

8. Click **Save** to complete the subscription.

Alternatively, you can also click **Subscribe** in the upper-right corner of the **Alert** page of the target {{{ .dedicated }}} cluster. You will be directed to the **Alert Subscription** page.

Alternatively, you can also click **Subscribe** in the upper-right corner of the **Alert** page of the cluster. You will be directed to the **Alert Subscription** page.

</CustomContent>

<CustomContent plan="essential">

> **Tip:**
>
> For {{{ .essential }}}, the alert subscription is for all alerts in the current instance. If you have multiple {{{ .essential }}} instances, you need to subscribe to each instance individually.

1. In the [TiDB Cloud console](https://tidbcloud.com), navigate to the [**My TiDB**](https://tidbcloud.com/tidbs) page of your organization, and then click the name of your target {{{ .essential }}} instance to go to its overview page.
2. In the left navigation pane, click **Settings** > **Alert Subscription**.
3. On the **Alert Subscription** page, click **Add Subscriber** in the upper-right corner.
4. Select **Slack** from the **Subscriber Type** drop-down list.
5. Enter a name in the **Name** field and your Slack webhook URL in the **URL** field.
6. Click **Test Connection**.

    - If the test succeeds, the **Save** button is displayed.
    - If the test fails, an error message is displayed. Follow the message to troubleshoot the issue and retry the connection.

7. Click **Save** to complete the subscription.

Alternatively, you can also click **Subscribe** in the upper-right corner of the **Alert** page of the target {{{ .essential }}} instance. You will be directed to the **Alert Subscription** page.

</CustomContent>

<CustomContent plan="premium">

> **Tip:**
>
> The alert subscription is for all alerts in the current {{{ .premium }}} instance. If you have multiple {{{ .premium }}} instances, you need to subscribe to each {{{ .premium }}} instance individually.

1. In the [TiDB Cloud console](https://tidbcloud.com), switch to your target {{{ .premium }}} instance using the combo box in the upper-left corner.
2. In the left navigation pane, click **Settings** > **Alert Subscription**.
3. On the **Alert Subscription** page, click **Add Subscriber** in the upper-right corner.
4. Select **Slack** from the **Subscriber Type** drop-down list.
5. Enter a name in the **Name** field and your Slack webhook URL in the **URL** field.
6. Click **Test Connection**.

    - If the test succeeds, the **Save** button is displayed.
    - If the test fails, an error message is displayed. Follow the message to troubleshoot the issue and retry the connection.

7. Click **Save** to complete the subscription.

Alternatively, you can also click **Subscribe** in the upper-right corner of the **Alert** page of the {{{ .premium }}} instance. You will be directed to the **Alert Subscription** page.

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

<CustomContent plan="premium">

1. In the [TiDB Cloud console](https://tidbcloud.com), switch to your target {{{ .premium }}} instance using the combo box in the upper-left corner.
2. In the left navigation pane, click **Settings** > **Alert Subscription**.
3. On the **Alert Subscription** page, locate the row of your target subscriber to be deleted, and then click **...** > **Unsubscribe**.
4. Click **Unsubscribe** to confirm the unsubscription.

</CustomContent>