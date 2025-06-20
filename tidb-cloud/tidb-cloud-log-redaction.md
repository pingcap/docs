---
title: User-Controlled Log Redaction
summary: Learn how to enable or disable user-controlled log redaction for TiDB Cloud dedicated clusters to manage sensitive data visibility in execution logs.
---

# User-Controlled Log Redaction

User-controlled Log Redaction allows you to manage the visibility of sensitive data in your TiDB Cloud Dedicated cluster's logs. By toggling this redaction feature, you can protect your information, balancing operational needs with security and controlling what appears in your cluster logs.

Log redaction is enabled by default, ensuring that sensitive information in running logs and execution plans is concealed. If you need more detailed log information for cluster maintenance or SQL tuning, you can disable this feature at any time.

> **Note:**
>
> Log redaction only applies to [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters.

## Prerequisites

* You must be in the **Organization Owner** or **Project Owner** role of your organization in TiDB Cloud.
* Log redaction can not be enabled or disabled when the cluster is in the `paused` state.

## Disable log redaction

> **Warning:**
>
> Disabling log redaction might expose sensitive information and increase the risk of data leakage. Ensure that you understand and acknowledge this risk before proceeding. Remember to re-enable it as soon as your diagnostic or maintenance task is complete.

To disable log redaction, do the following:

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/).
2. Navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page, and then click the name of your target cluster to go to its overview page.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

3. In the left navigation pane, click **Settings** > **Security**.
4. In the **Execution Log Redaction** section, you can see the redaction feature is **Enabled** by default.
5. Click **Disable** to disable it.
6. A warning will appear, explaining the risks of disabling log redaction. You must confirm your action twice.

Note that after disabling log redaction:

* The change will only apply to new database connections.
* Existing connections are unaffected. You need to reconnect them for the changes to take effect.
* Logs for new sessions will no longer be redacted.

## Confirm that log redaction is disabled

To confirm that log redaction is disabled, do the following:

1. Simulate a performance issue caused by a slow-running query. For example, execute the following SQL statement:

    ```sql
    SELECT *, SLEEP(2) FROM users where email like "%useremail%";
    ```

2. Wait a few minutes for the slow query log to update.
3. Review the log to confirm that the sensitive data is not redacted.

## Enable log redaction

To maintain security, **enable log redaction** as soon as your diagnostic or maintenance task is complete as follows.

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/).
2. Navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page, and then click the name of your target cluster to go to its overview page.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

3. In the left navigation pane, click **Settings** > **Security**.
4. In the **Execution Log Redaction** section, you can see the redaction feature is **Disabled**.
5. Click **Enable** to enable it.
6. **Reconnect to the database** for the change to take effect on new sessions.
