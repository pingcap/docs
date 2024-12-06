---
title: Subscribe via Email
summary: Learn how to monitor your TiDB cluster by getting alert notification via Email.
---

# Subscribe via Email

TiDB Cloud provides you with an easy way to subscribe to alert notifications via multiple channels. This document describes how to subscribe to alert notifications via Email.

## Prerequisites

- To subscribe to alert notification of TiDB Cloud, you must have the `Organization Owner` access to your organization or `Project Owner` access to the target project in TiDB Cloud.

## Subscribe to alert notifications

> **Tip:**
>
> The alert subscription is for all alerts in the current project. If you have multiple clusters in the project, you just need to subscribe once.

To get alert notifications of clusters in your project, take the following steps:

1. On the **Alerts** page , click **Subscribe Alerts**.
2. Select **Email** from the **Subscriber Type** drop-down list.
3. Enter your email address.
4. Click **Test Connection** button.

    - If the test successes, the **Save** button is displayed.
    - If the test fails, an error message is displayed. Follow the message for troubleshooting and retry the connection.

5. Click **Save** button to complete the subscription.

Alternatively, you can also add the subscription from the **Alert Subscription** page as follows:

1. Log in to the [TiDB Cloud console](https://tidbcloud.com).
2. Click <MDSvgIcon name="icon-left-projects" /> in the lower-left corner, switch to the target project if you have multiple projects, and then click **Project Settings**.
3. On the **Project Settings** page of your project, click **Alert Subscription** in the left navigation pane.
4. Click **Add Subscriber**.
5. Select **Email** from the **Subscriber Type** drop-down list.
6. Enter your email address.
7. Click **Test Connection** button.

    - If the test successes, the **Save** button is displayed.
    - If the test fails, an error message is displayed. Follow the message for troubleshooting and retry the connection.

8. Click **Save** button to complete the subscription.

If an alert condition remains unchanged, the alert sends email notifications every 3 hours.

## Unsubscribe from alert notifications

If you no longer want to receive alert notifications of clusters in your project, take the following steps:

1. Log in to the [TiDB Cloud console](https://tidbcloud.com).
2. Click <MDSvgIcon name="icon-left-projects" /> in the lower-left corner, switch to the target project if you have multiple projects, and then click **Project Settings**.
3. On the **Project Settings** page of your project, click **Alert Subscription** in the left navigation pane.
4. In the row of your target subscriber to be deleted, and click **...**.
5. Click **Unsubscribe** in the drop-down menu.
5. Click **Unsubscribe** to confirm the unsubscription in the pop-up window.