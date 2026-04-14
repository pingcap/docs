---
title: Subscribe via Zoom
summary: Learn how to monitor your TiDB cluster by getting alert notifications via Zoom.
---

# Subscribe via Zoom

TiDB Cloud provides you with an easy way to subscribe to alert notifications via Zoom, [Slack](/tidb-cloud/monitor-alert-slack.md), [email](/tidb-cloud/monitor-alert-email.md), [Flashduty](/tidb-cloud/monitor-alert-flashduty.md), and [PagerDuty](/tidb-cloud/monitor-alert-pagerduty.md). This document describes how to subscribe to alert notifications via Zoom.

> **Note:**
>
> Currently, alert subscription is available for [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) instances and [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters.

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

Alert notification subscriptions vary by [your TiDB Cloud plan](/tidb-cloud/select-cluster-tier.md).

<CustomContent plan="dedicated">

To subscribe to alert notifications of {{{ .dedicated }}} clusters, take the following steps:

> **Tip:**
>
> For {{{ .dedicated }}}, the alert subscription is for all alerts in the current project. If you have multiple {{{ .dedicated }}} clusters in the project, you just need to subscribe once.

1. In the [TiDB Cloud console](https://tidbcloud.com), navigate to the [**My TiDB**](https://tidbcloud.com/tidbs) page of your organization, and then click the **Project view** tab.
2. In the project view, locate your target project, and then click the gear icon for the project.
3. In the left navigation pane, click **Alert Subscription** under **Project Settings**.
4. On the **Alert Subscription** page, click **Add Subscriber** in the upper-right corner.
5. Select **Zoom** from the **Subscriber Type** drop-down list.
6. Enter a name in the **Name** field, your Zoom webhook URL in the **URL** field, and the verification token in the **Token** field.
7. Click **Test Connection**.

    - If the test succeeds, the **Save** button is displayed.
    - If the test fails, an error message is displayed. Follow the message for troubleshooting and retry the connection.

8. Click **Save** to complete the subscription.

Alternatively, you can also click **Subscribe** in the upper-right corner of the **Alert** page of the target {{{ .dedicated }}} cluster. You will be directed to the **Alert Subscription** page.

</CustomContent>

<CustomContent plan="essential">

To subscribe to alert notifications of a {{{ .essential }}} instance, take the following steps:

> **Tip:**
>
> For {{{ .essential }}}, the alert subscription is for all alerts in the current instance. If you have multiple {{{ .essential }}} instances, you need to subscribe to each instance individually.

1. In the [TiDB Cloud console](https://tidbcloud.com), navigate to the [**My TiDB**](https://tidbcloud.com/tidbs) page of your organization, and then click the name of your target {{{ .essential }}} instance to go to its overview page.
2. In the left navigation pane, click **Settings** > **Alert Subscription**.
3. On the **Alert Subscription** page, click **Add Subscriber** in the upper-right corner.
4. Select **Zoom** from the **Subscriber Type** drop-down list.
5. Enter a name in the **Name** field, your Zoom webhook URL in the **URL** field, and the verification token in the **Token** field.
6. Click **Test Connection**.

    - If the test succeeds, the **Save** button is displayed.
    - If the test fails, an error message is displayed. Follow the message to troubleshoot the issue and retry the connection.

7. Click **Save** to complete the subscription.

Alternatively, you can also click **Subscribe** in the upper-right corner of the **Alert** page of the target {{{ .essential }}} instance. You will be directed to the **Alert Subscription** page.

</CustomContent>

If an alert condition remains unchanged, the alert sends notifications every three hours.

## Unsubscribe from alert notifications

If you no longer want to receive alert notifications, take the following steps. The steps vary by [your TiDB Cloud plan](/tidb-cloud/select-cluster-tier.md).

<CustomContent plan="dedicated">

1. In the [TiDB Cloud console](https://tidbcloud.com), navigate to the [**My TiDB**](https://tidbcloud.com/tidbs) page of your organization, and then click the **Project view** tab.
2. In the project view, locate your target project, and then click the gear icon for the project.
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
