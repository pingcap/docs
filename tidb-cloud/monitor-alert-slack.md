---
title: Subscribe via Slack
summary: Learn how to monitor your TiDB cluster by getting alert notification via Slack.
---

# Subscribe via Slack

TiDB Cloud provides you with an easy way to subscribe to alert notifications via Slack, [email](/tidb-cloud/monitor-alert-email.md), and [Zoom](/tidb-cloud/monitor-alert-zoom.md). This document describes how to subscribe to alert notifications via Slack.

## Prerequisites

- The Subscribing via Slack feature is only available for organizations that subscribes to the Enterprise support plan or higher.

- To subscribe to alert notification of TiDB Cloud, you must have the `Organization Owner` access to your organization or `Project Owner` access to the target project in TiDB Cloud.

## Subscribe to alert notifications

### Step 1. Generate a Slack webhook URL

1. [Create a Slack app](https://api.slack.com/apps/new), if you do not have one already. Click **Create New App**, and choose **From scratch**. Enter a name, choose a workspace to associate your app with, and then click **Create App**.
2. Go to the settings page for your app. You can load its settings via your [app's management dashboard](https://api.slack.com/apps).
3. Click the **Incoming Webhooks** tab, and then toggle **Activate Incoming Webhooks** to **ON**.
4. Click **Add New Webhook to Workspace**.
5. Select a channel that you want to receive alert notifications in, and then select **Authorize**. If you need to add the incoming webhook to a private channel, you must first be in that channel.
6. You can see a new entry under the **Webhook URLs for Your Workspace** section in the format: `https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX`.

### Step 2. Subscribe from TiDB Cloud

> **Tip:**
>
> The alert subscription is for all alerts in the current project. If you have multiple clusters in the project, you just need to subscribe once.

1. Click <MDSvgIcon name="icon-left-projects" /> in the lower-left corner, switch to the target project if you have multiple projects, and then click **Project Settings**.
2. On the **Project Settings** page of your project, click **Alert Subscription** in the left navigation pane.
3. Click **Add Subscriber**.
4. Select **Slack** from the **Subscriber Type** drop-down list.
5. In the **Name** field, enter a name and your Slack webhook URL into **URL** field.
6. Click **Test Connection**.

    - If the test succeeds, the **Save** button is displayed.
    - If the test fails, an error message is displayed. Follow the message to troubleshoot the issue and retry the connection.

7. Click **Save** to complete the subscription.

Alternatively, you can also click **Subscribe** in the top right corner of the **Alert** page of the cluster. You will be directed to the **Alert Subscriber** page.

If an alert condition remains unchanged, the alert sends notifications every three hours.

## Unsubscribe from alert notifications

If you no longer want to receive alert notifications of clusters in your project, take the following steps:

1. Log in to the [TiDB Cloud console](https://tidbcloud.com).
2. Click <MDSvgIcon name="icon-left-projects" /> in the lower-left corner, switch to the target project if you have multiple projects, and then click **Project Settings**.
3. On the **Project Settings** page of your project, click **Alert Subscription** in the left navigation pane.
4. In the row of your target subscriber to be deleted, and click **...**.
5. Click **Unsubscribe** to confirm the unsubscription in the pop-up window.