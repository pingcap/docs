---
title: Connected: IM Subscription for TiDB Cloud Alerts
summary: Introduces detailed information about the IM subscription for TiDB Cloud alerts
---

# Connected: IM Subscription for TiDB Cloud Alerts

For customers subscribed to the **Enterprise** or **Premium** support plan, in addition to subscribing to alert notifications via email, TiDB Cloud also provides you with an easy way to subscribe to alert notifications via instant message (IM) tools such as Slack and Zoom.

## Subscribe via Slack

This section describes how to subscribe to alert notifications via Slack.

### Prerequisites

The Subscribing via Slack feature is only available for organizations that subscribe to the **Enterprise** or **Premium** support plan.

To subscribe to alert notifications of TiDB Cloud, you must have the `Organization Owner` access to your organization or `Project Owner` access to the target project in TiDB Cloud.

### Subscribe to alert notifications

#### Step 1. Generate a Slack webhook URL

1. [Create a Slack app](https://api.slack.com/apps/new), if you do not have one already. Click **Create New App**, and choose **From scratch**. Enter a name, choose a workspace to associate your app with, and then click **Create App**.

2. Go to the settings page for your app. You can load its settings via your [app's management dashboard](https://api.slack.com/apps).

3. Click the **Incoming Webhooks** tab, and then toggle **Activate Incoming Webhooks** to `ON`.

4. Click **Add New Webhook to Workspace**.

5. Select a channel that you want to receive alert notifications in, and then select **Authorize**. If you need to add the incoming webhook to a private channel, you must first be in that channel.

You can see a new entry under the **Webhook URLs** for Your Workspace section in the following format: `https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX`.

#### Step 2. Subscribe from TiDB Cloud

> **Tip:**
>
> The alert subscription is for all alerts in the current project. If you have multiple clusters in the project, you just need to subscribe once.

To get alert notifications of clusters in your project, take the following steps:

1. Click <MDSvgIcon name="icon-left-projects" /> in the lower-left corner, switch to the target project if you have multiple projects, and then click **Project Settings**.

2. On the **Project Settings** page of your project, click **Alert Subscription** in the left navigation pane.

3. Click **Add Subscriber**.

4. Select **Slack** from the **Subscriber Type** drop-down list.

5. In the **Name** field, enter a name and your Slack webhook URL in the **URL** field.

6. Click Test Connection.

    * If the test succeeds, the Save button is displayed.
    
    * If the test fails, an error message is displayed. Follow the message to troubleshoot the issue and retry the connection.

7. Click **Save** to complete the subscription.

Alternatively, you can also click **Subscribe** in the upper-right corner of the **Alert** page of the cluster. You will be directed to the **Alert Subscriber** page.

If an alert condition remains unchanged, the alert sends notifications every three hours.

### Unsubscribe from alert notifications

If you no longer want to receive alert notifications of clusters in your project, take the following steps:

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/).

2. Click <MDSvgIcon name="icon-left-projects" /> in the lower-left corner, switch to the target project if you have multiple projects, and then click **Project Settings**.

3. On the **Project Settings** page of your project, click **Alert Subscription** in the left navigation pane.

4. In the row of your target subscriber to be deleted, click ....

5. Click **Unsubscribe** to confirm the unsubscription in the pop-up window.

## Subscribe via Zoom

This section describes how to subscribe to alert notifications via Zoom.

### Prerequisites

* The Subscribing via Zoom feature is only available for organizations that subscribe to the **Enterprise** or **Premium** support plan.

* To subscribe to alert notifications of TiDB Cloud, you must have the `Organization Owner` access to your organization or `Project Owner` access to the target project in TiDB Cloud.

* To add and configure the **Incoming Webhook Chatbot** in Zoom, you need to have admin permissions on your Zoom account.

### Subscribe to alert notifications

#### Step 1. Add Zoom Incoming Webhook App

1. Sign in to the [Zoom App Marketplace](https://marketplace.zoom.us/) as the account administrator.

2. Add [Incoming Webhook App](https://marketplace.zoom.us/apps/eH_dLuquRd-VYcOsNGy-hQ) from the Zoom App Marketplace, and then click **Add**. If the app is not pre-approved, contact your Zoom administrator to approve this app for your account. For more information, see admin app approvals.

3. Confirm the permissions the app requires, then click **Authorize** to add the Incoming Webhook app.

#### Step 2. Generate a Zoom webhook URL

1. Sign in to the Zoom desktop client.

2. Click the **Team Chat** tab.

3. Under Apps, find and select **Incoming Webhook**, or select a chat channel from above that you would like to receive messages in.

4. Enter the following command to make a new connection. You need to replace {connectionName} with your desired connection name, for example, tidbcloud-alerts:

    ```shell
    /inc connect ${connectionName}
    ```

5. The command will return the following details:

   * Endpoint. It will provide a webhook URL in the following format: `https://integrations.zoom.us/chat/webhooks/incomingwebhook/XXXXXXXXXXXXXXXXXXXXXXXX`.

   * Verification Token

#### Step 3. Subscribe from TiDB Cloud

> **Tip**
>
> The alert subscription is for all alerts in the current project. If you have multiple clusters in the project, you just need to subscribe once.

To get alert notifications of clusters in your project, take the following steps:

1. Click <MDSvgIcon name="icon-left-projects" /> in the lower-left corner, switch to the target project if you have multiple projects, and then click Project Settings.

2. On the **Project Settings** page of your project, click **Alert Subscription** in the left navigation pane.

3. Click **Add Subscriber**.

4. Select **Zoom** from the **Subscriber Type** drop-down list.

5. Enter the **Name** field, enter your Zoom webhook URL in the **URL** field, and enter the verification token in the **Token** field.

6. Click **Test Connection**.

    * If the test succeeds, the `Save` button is displayed.
    
    * If the test fails, an error message is displayed. Follow the message for troubleshooting and retry the connection.

7. Click **Save** to complete the subscription.

Alternatively, you can also click **Subscribe** in the upper-right corner of the **Alert** page of the cluster. You will be directed to the **Alert Subscriber** page.

If an alert condition remains unchanged, the alert sends notifications every three hours.

### Unsubscribe from alert notifications

If you no longer want to receive alert notifications of clusters in your project, take the following steps:

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/).

2. Click <MDSvgIcon name="icon-left-projects" /> in the lower-left corner, switch to the target project if you have multiple projects, and then click Project Settings.

3. On the **Project Settings** page of your project, click **Alert Subscription** in the left navigation pane.

4. In the row of your target subscriber to be deleted, click ....

5. Click **Unsubscribe** to confirm the unsubscription in the pop-up window.

