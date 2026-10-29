---
title: Subscribe via Webhook
summary: Learn how to monitor your TiDB cluster by getting alert notifications via a generic webhook.
---

# Subscribe via Webhook

TiDB Cloud provides you with an easy way to subscribe to alert notifications via a [Generic Webhook](/tidb-cloud/monitor-alert-webhook.md), [email](/tidb-cloud/monitor-alert-email.md), [Slack](/tidb-cloud/monitor-alert-slack.md), [Zoom](/tidb-cloud/monitor-alert-zoom.md), [Flashduty](/tidb-cloud/monitor-alert-flashduty.md), and [PagerDuty](/tidb-cloud/monitor-alert-pagerduty.md). This document describes how to subscribe to alert notifications via a generic webhook.

> **Note:**
>
> Currently, alert subscription is available for [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) instances, [TiDB Cloud Premium](/tidb-cloud/select-cluster-tier.md#premium) instances, and [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters.

## Prerequisites

- The subscribing via webhook feature is only available for organizations that subscribe to the **Enterprise** or **Premium** support plan.

- You need a webhook URL from the platform where you want to receive alert notifications on (for example, Telegram, Microsoft Teams, or your own on-call system that accepts HTTP POST requests with a JSON payload). Currently, TiDB Cloud does not support customizing the request headers or the payload format. For the payload format, see [Webhook payload](#webhook-payload).

<CustomContent plan="dedicated">

- To subscribe to alert notifications of TiDB Cloud, you must have the `Organization Owner` access to your organization or `Project Owner` access to the target project in TiDB Cloud.

</CustomContent>

<CustomContent plan="essential,premium">

- To subscribe to alert notifications of TiDB Cloud, you must have the `Organization Owner` access to your organization or `Project Owner` or `Instance Manager` access to the target instance in TiDB Cloud.

</CustomContent>

## Subscribe to alert notifications

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
5. Select **Webhook** from the **Subscriber Type** drop-down list.
6. Enter a name in the **Name** field and your webhook URL in the **Webhook URL** field.
7. Click **Save**. The backend will test connection and save for you.

    If the test fails, an error message is displayed. Follow the message to troubleshoot the issue and retry the connection.

Alternatively, you can also click **Subscribe** in the upper-right corner of the **Alert** page of the target {{{ .dedicated }}} cluster. You will be directed to the **Alert Subscription** page.

</CustomContent>

<CustomContent plan="essential">

> **Tip:**
>
> For {{{ .essential }}}, the alert subscription is for all alerts in the current instance. If you have multiple {{{ .essential }}} instances, you need to subscribe to each instance individually.

1. In the [TiDB Cloud console](https://tidbcloud.com), navigate to the [**My TiDB**](https://tidbcloud.com/tidbs) page of your organization, and then click the name of your target {{{ .essential }}} instance to go to its overview page.
2. In the left navigation pane, click **Settings** > **Alert Subscription**.
3. On the **Alert Subscription** page, click **Add Subscriber** in the upper-right corner.
4. Select **Webhook** from the **Subscriber Type** drop-down list.
5. Enter a name in the **Name** field and your webhook URL in the **Webhook URL** field.
6. Click **Save**. The backend will test connection and save for you.

    If the test fails, an error message is displayed. Follow the message to troubleshoot the issue and retry the connection.

Alternatively, you can also click **Subscribe** in the upper-right corner of the **Alert** page of the target {{{ .essential }}} instance. You will be directed to the **Alert Subscription** page.

</CustomContent>

<CustomContent plan="premium">

> **Tip:**
>
> For {{{ .premium }}}, the alert subscription is for all alerts in the current instance. If you have multiple {{{ .premium }}} instances, you need to subscribe to each instance individually.

1. In the [TiDB Cloud console](https://tidbcloud.com), navigate to the [**My TiDB**](https://tidbcloud.com/tidbs) page of your organization, and then click the name of your target {{{ .premium }}} instance to go to its overview page.
2. In the left navigation pane, click **Settings** > **Alert Subscription**.
3. On the **Alert Subscription** page, click **Add Subscriber** in the upper-right corner.
4. Select **Webhook** from the **Subscriber Type** drop-down list.
5. Enter a name in the **Name** field and your webhook URL in the **Webhook URL** field.
6. Click **Save**. The backend will test connection and save for you.

    If the test fails, an error message is displayed. Follow the message to troubleshoot the issue and retry the connection.

Alternatively, you can also click **Subscribe** in the upper-right corner of the **Alert** page of the target {{{ .premium }}} instance. You will be directed to the **Alert Subscription** page.

</CustomContent>

If an alert condition remains unchanged, the alert sends notifications every three hours.

## Webhook payload

TiDB Cloud sends each alert notification to your webhook URL as an HTTP `POST` request with a JSON body. The payload is compatible with the [Alertmanager webhook format](https://prometheus.io/docs/alerting/latest/configuration/#webhook_config).

### Endpoint requirements

- The webhook URL must use `http` or `https`, be accessible from the public internet, and contain no more than 255 characters.
- The webhook URL cannot contain a username or password.
- The endpoint must return a `2xx` status code within 15 seconds. Redirects are not followed.

### Payload fields

| Field | Type | Description |
|:---|:---|:---|
| `receiver` | String | The receiver name. The value is always `webhook`. |
| `status` | String | The alert status. Valid values are `firing` and `resolved`. |
| `alerts` | Array | The alert list. Each request contains exactly one alert. |
| `alerts[].status` | String | The alert status. Same as `status`. |
| `alerts[].labels.cluster` | String | The name of the cluster or instance. |
| `alerts[].labels.severity` | String | The alert severity, such as `critical`, `warning`, or `info`. |
| `alerts[].labels.project` | String | The name of the project. Only available for TiDB Cloud Dedicated clusters. |
| `alerts[].annotations.alertname` | String | The alert title. |
| `alerts[].annotations.message` | String | The alert details. The value might contain HTML tags. |
| `alerts[].startsAt` | String | The time when the alert is triggered, in RFC 3339 format. |
| `alerts[].endsAt` | String | The time when the alert is resolved, in RFC 3339 format. Only available when `status` is `resolved`. |
| `groupKey` | String | The identifier of the alert. Notifications of the same alert share the same value. Optional. |
| `groupLabels` | Object | The same as `alerts[].labels`, without `project`. |
| `commonLabels` | Object | The same as `alerts[].labels`, without `project`. |
| `commonAnnotations` | Object | The same as `alerts[].annotations`, without `message`. |
| `dryRun` | Boolean | Whether the request is a connection test. Only available in test notifications, with the value `true`. |

### Payload example

```json
{
  "receiver": "webhook",
  "status": "firing",
  "alerts": [
    {
      "status": "firing",
      "labels": {
        "cluster": "Cluster0",
        "severity": "warning",
        "project": "default project"
      },
      "annotations": {
        "alertname": "Total TiKV CPU usage is too high",
        "message": "The total CPU usage of TiKV nodes in cluster Cluster0 has exceeded 80% for 10 minutes."
      },
      "startsAt": "2026-10-10T08:00:00Z"
    }
  ],
  "groupKey": "a1b2c3d4e5f60718",
  "groupLabels": {
    "cluster": "Cluster0",
    "severity": "warning"
  },
  "commonLabels": {
    "cluster": "Cluster0",
    "severity": "warning"
  },
  "commonAnnotations": {
    "alertname": "Total TiKV CPU usage is too high"
  }
}
```

### Notification behavior

- When an alert is triggered, TiDB Cloud sends a notification with `status` set to `firing`. If the alert condition remains unchanged, the notification is sent again every three hours.
- When an alert is resolved, TiDB Cloud sends a notification with `status` set to `resolved`.
- If a request fails due to a network error, or the endpoint returns `429` or `5xx`, TiDB Cloud retries the request up to two times. Your endpoint might receive the same notification more than once.
- When you save a webhook subscriber, TiDB Cloud sends a test notification with `dryRun` set to `true`. The subscriber is saved only if the test succeeds.

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

1. In the [TiDB Cloud console](https://tidbcloud.com), navigate to the [**My TiDB**](https://tidbcloud.com/tidbs) page of your organization, and then click the name of your target {{{ .premium }}} instance to go to its overview page.
2. In the left navigation pane, click **Settings** > **Alert Subscription**.
3. On the **Alert Subscription** page, locate the row of your target subscriber to be deleted, and then click **...** > **Unsubscribe**.
4. Click **Unsubscribe** to confirm the unsubscription.

</CustomContent>
