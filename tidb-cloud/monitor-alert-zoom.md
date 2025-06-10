---
title: Subscribe via Zoom
summary: Learn how to monitor your TiDB cluster by getting alert notifications via Zoom.
---

# Subscribe via Zoom

TiDB Cloud provides you with an easy way to subscribe to alert notifications via [Zoom](https://www.zoom.com/), [Slack](/tidb-cloud/monitor-alert-slack.md), and [email](/tidb-cloud/monitor-alert-email.md). This document describes how to subscribe to alert notifications via Zoom.

> **Note:**
>
> Currently, alert subscription is only available for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters.

## Prerequisites

- The subscribing via Zoom feature is only available for organizations that subscribe to the **Enterprise** or **Premium** support plan.

- To subscribe to alert notifications of TiDB Cloud, you must have the `Organization Owner` access to your organization or `Project Owner` access to the target project in TiDB Cloud.

- To add and configure the Incoming Webhook Chatbot in Zoom, you need to have admin permissions on your Zoom account.

## Subscribe to alert notifications

### Step 1. Add the Zoom Incoming Webhook app

1. Sign in to the [Zoom App Marketplace](https://marketplace.zoom.us/) as the account administrator.
2. Go to the [Incoming Webhook App](https://marketplace.zoom.us/apps/eH_dLuquRd-VYcOsNGy-hQ) page in the Zoom App Marketplace, and then click **Add** to add this app. If the app is not pre-approved, contact your Zoom admin to approve this app for your account. For more information, see [Approving apps and managing app requests](https://support.zoom.us/hc/en-us/articles/360027829671). 
3. Confirm the permissions the app requires, then click **Authorize** to add the Incoming Webhook app.

### Step 2. Generate a Zoom webhook URL

1. Sign in to the Zoom desktop client.
2. Click the **Team Chat** tab.
3. Under **Apps**, find and select **Incoming Webhook**, or select a chat channel from above that you would like to receive messages in.
4. Enter the following command to make a new connection. You need to replace `${connectionName}` with your desired connection name, for example, `tidbcloud-alerts`:

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

1. In the [TiDB Cloud console](https://tidbcloud.com), switch to your target project using the combo box in the upper-left corner.
2. In the left navigation pane, click **Project Settings** > **Alert Subscription**.
3. On the **Alert Subscription** page, click **Add Subscriber**.
4. Select **Zoom** from the **Subscriber Type** drop-down list.
5. Enter a name in the **Name** field, your Zoom webhook URL in the **URL** field, and the verification token in the **Token** field.
6. Click **Test Connection**.

    - If the test succeeds, the **Save** button is displayed.
    - If the test fails, an error message is displayed. Follow the message for troubleshooting and retry the connection.

7. Click **Save** to complete the subscription.

Alternatively, you can also click **Subscribe** in the upper-right corner of the **Alert** page of the cluster. You will be directed to the **Alert Subscriber** page.

If an alert condition remains unchanged, the alert sends notifications every three hours.

## Unsubscribe from alert notifications

If you no longer want to receive alert notifications of clusters in your project, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com), switch to your target project using the combo box in the upper-left corner.
2. In the left navigation pane, click **Project Settings** > **Alert Subscription**.
3. On the **Alert Subscription** page, locate the row of your target subscriber to be deleted, and then click **...** > **Unsubscribe**.
4. Click **Unsubscribe** to confirm the unsubscription.
