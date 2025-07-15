---
title: User-Controlled Log Redaction
summary: Learn how to enable or disable user-controlled log redaction for TiDB Cloud Dedicated clusters to manage sensitive data visibility in execution logs.
---

# User-Controlled Log Redaction

User-controlled log redaction lets you manage the visibility of sensitive data in your [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) cluster logs. By toggling this redaction feature, you can protect your information, balance operational needs with security, and control what appears in your cluster logs.

Log redaction is enabled by default, ensuring that sensitive information in running logs and execution plans is concealed. If you need more detailed log information for cluster maintenance or SQL tuning, you can disable this feature at any time.

> **Note:**
>
> The log redaction feature is only supported for TiDB Cloud Dedicated clusters.

## Prerequisites

* You must be in the **Organization Owner** or **Project Owner** role of your organization in TiDB Cloud.
* Log redaction cannot be enabled or disabled when the cluster is in the `paused` state.

## Disable log redaction

> **Warning:**
>
> Disabling log redaction might expose sensitive information and increase the risk of data leakage. Ensure that you understand and acknowledge this risk before proceeding. Remember to re-enable it as soon as you complete your diagnostic or maintenance task.

To disable log redaction, do the following:

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/).
2. Navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page, and then click the name of your target cluster to go to its overview page.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

3. In the left navigation pane, click **Settings** > **Security**.
4. In the **Execution Log Redaction** section, you can see that the redaction feature is **Enabled** by default.
5. Click **Disable**. A warning appears, explaining the risks of disabling log redaction. 
6. Confirm the disabling.

After disabling log redaction, note the following:

* The change only applies to new database connections.
* Existing connections are unaffected. You need to reconnect them for the changes to take effect.
* Logs for new sessions will no longer be redacted.

## Check the updated logs

To check the updated logs after log redaction is disabled, do the following:

1. Simulate a performance issue caused by a slow query. For example, execute the following SQL statement:

    ```sql
    SELECT *, SLEEP(2) FROM users WHERE email LIKE "%useremail%";
    ```

2. Wait a few minutes for the slow query log to update.
3. Review the log to confirm that the sensitive data is not redacted.

## Enable log redaction

To maintain data security, **enable log redaction** as soon as you complete your diagnostic or maintenance task as follows.

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/).
2. Navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page, and then click the name of your target cluster to go to its overview page.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

3. In the left navigation pane, click **Settings** > **Security**.
4. In the **Execution Log Redaction** section, you can see that the redaction feature is **Disabled**.
5. Click **Enable** to enable it.
6. Reconnect to the database for the change to take effect on new sessions.
