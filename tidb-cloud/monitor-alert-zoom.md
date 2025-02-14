---
title: Subscribe via Zoom
summary: Learn how to monitor your TiDB cluster by getting alert notification via Zoom.
---

# Subscribe via Zoom

TiDB Cloud provides you with an easy way to subscribe to alert notifications via Zoom, [Slack](/tidb-cloud/monitor-alert-slack.md), and [email](/tidb-cloud/monitor-alert-email.md). This document describes how to subscribe to alert notifications via Zoom.

## Prerequisites

- The Subscribing via Zoom feature is only available for organizations that subscribes to the Enterprise support plan or higher.

- To subscribe to alert notification of TiDB Cloud, you must have the `Organization Owner` access to your organization or `Project Owner` access to the target project in TiDB Cloud.

- To add and configure the Incoming Webhook Chatbot in Zoom, you need to have admin permissions on your Zoom account.

## Subscribe to alert notifications

### Step 1. Add Zoom Incoming Webhook App

1. Sign in to the [Zoom App Marketplace](https://marketplace.zoom.us/) as the account administrator.
2. Add [Incoming Webhook App](https://marketplace.zoom.us/apps/eH_dLuquRd-VYcOsNGy-hQ) from the Zoom App Marketplace, Click **Add**. If the app is not pre-approved, contact your Zoom admin to approve this app for your account. Learn more about [admin app approvals](https://support.zoom.us/hc/en-us/articles/360027829671). 
3. Confirm the permissions the app requires, then click **Authorize**. The Incoming Webhook app is now added.

### Step 2. Generate a Zoom webhook URL

1. Sign in to the Zoom desktop client.
2. Click the **Team Chat** tab.
3. Under **Apps**, find and select **Incoming Webhook**, or select a chat channel from above that you would like to receive messages in.
4. Enter the following command to make a new connection, please replace `<connectionName>` with your connection name that you want to use, for example, `tidbcloud-alerts`:

    ```shell
    /inc connect ${connectionName}
    ```

5. The command will return the following details:

   - **Endpoint**. It will provide a webhook URL in the format: `https://integrations.zoom.us/chat/webhooks/incomingwebhook/XXXXXXXXXXXXXXXXXXXXXXXX`.
   - **Verification Token**

### Step 3. Subscribe from TiDB Cloud

> **Tip:**
>
> The alert subscription is for all alerts in the current project. If you have multiple clusters in the project, you just need to subscribe once.

1. Click <MDSvgIcon name="icon-left-projects" /> in the lower-left corner, switch to the target project if you have multiple projects, and then click **Project Settings**.
2. On the **Project Settings** page of your project, click **Alert Subscription** in the left navigation pane.
3. Click **Add Subscriber**
4. Select **Zoom** from the **Subscriber Type** drop-down list.
5. Enter the **Name** field, your Zoom webhook URL into the **URL** field and the verification token into the **Token** field.
6. Click **Test Connection**.

    - If the test succeeds, the **Save** button is displayed.
    - If the test fails, an error message is displayed. Follow the message for troubleshooting and retry the connection.

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