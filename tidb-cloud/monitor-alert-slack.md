---
title: Subscribe via Slack
summary: Learn how to monitor your TiDB cluster by getting alert notification via Slack.
---

# Subscribe via Slack

TiDB Cloud provides you with an easy way to subscribe to alert notifications via multiple channels. This document describes how to subscribe to alert notifications via Slack.

## Prerequisites

- To subscribe to alert notification of TiDB Cloud, you must have the `Organization Owner` access to your organization or `Project Owner` access to the target project in TiDB Cloud.

- To receive alert notifications via Slack, you need to have an Enterprise support plan or higher.

## Subscribe to alert notifications

### Step 1. Generate a Slack webhook URL

1. [Create a Slack app](https://api.slack.com/apps/new), if you don't have one already. Click **Create New App**, and choose **From scratch**. Pick a name, choose a workspace to associate your app with, then click **Create App**.
2. Goto the settings page for your app, you can load its settings via your [app's management dashboard](https://api.slack.com/apps).
3. Select **Incoming Webhooks** tab, and toggle **Activate Incoming Webhooks** to **ON**.
4. Click **Add New Webhook to Workspace**.
5. Go ahead and pick a channel that you want to receive alert notifications in, then select **Authorize**. If you need to add the incoming webhook to a private channel, you must first be in that channel.
6. You can see a new entry under the **Webhook URLs for Your Workspace** section in the format: `https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX`.

### Step 2. Subscribe from TiDB Cloud

> **Tip:**
>
> The alert subscription is for all alerts in the current project. If you have multiple clusters in the project, you just need to subscribe once.

1. On the **Alerts** page , click **Subscribe Alerts**.
2. Select **Slack** from the **Subscriber Type** drop-down list.
3. Enter **Name** field and your Slack webhook URL into **URL** field.
4. Click **Test Connection** button.

    - If the test successes, the **Save** button is displayed.
    - If the test fails, an error message is displayed. Follow the message for troubleshooting and retry the connection.

5. Click **Save** button to complete the subscription.

Alternatively, you can also add the subscription from the **Alert Subscription** page as follows:

1. Log in to the [TiDB Cloud console](https://tidbcloud.com).
2. Click <MDSvgIcon name="icon-left-projects" /> in the lower-left corner, switch to the target project if you have multiple projects, and then click **Project Settings**.
3. On the **Project Settings** page of your project, click **Alert Subscription** in the left navigation pane.
4. Click **Add Subscriber**.
5. Select **Slack** from the **Subscriber Type** drop-down list.
6. Enter **Name** field and your Slack webhook URL into **URL** field.
7. Click **Test Connection** button.

    - If the test successes, the **Save** button is displayed.
    - If the test fails, an error message is displayed. Follow the message for troubleshooting and retry the connection.

8. Click **Save** button to complete the subscription.

If an alert condition remains unchanged, the alert sends notifications every 3 hours.

## Unsubscribe from alert notifications

If you no longer want to receive alert notifications of clusters in your project, take the following steps:

1. Log in to the [TiDB Cloud console](https://tidbcloud.com).
2. Click <MDSvgIcon name="icon-left-projects" /> in the lower-left corner, switch to the target project if you have multiple projects, and then click **Project Settings**.
3. On the **Project Settings** page of your project, click **Alert Subscription** in the left navigation pane.
4. In the row of your target subscriber to be deleted, and click **...**.
5. Click **Unsubscribe** in the drop-down menu.
5. Click **Unsubscribe** to confirm the unsubscription in the pop-up window.