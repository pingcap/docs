---
title: User-Controlled Log Redaction
summary: Learn how to enable or disable user-controlled log redaction for TiDB Cloud dedicated clusters to manage sensitive data visibility in execution logs.
---

# User-Controlled Log Redaction
User-controlled Log Redaction allows you to manage the visibility of sensitive data in your TiDB Cloud Dedicated cluster's logs by toggling a redaction feature that protects your information. This feature is designed to balance operational needs with security, giving you control over what is visible in your cluster logs.
The Log Redaction is enabled by default, ensuring that sensitive information in running logs and execution plans is concealed to protect your data. If you need more detailed log information for cluster maintenance or SQL tuning, you can disable this feature at any time. 

> **Note:**
>
> Disabling log redaction may expose sensitive information and increase the risk of data leakage. Please remember to enable as soon as your diagnostic or maintenance task is complete.
>

# Prerequisites
* You must be in the **Organization Owner** or **Project Owner** role of your organization in TiDB Cloud.
* You can only enable or disable log redaction for **dedicated clusters** in your cluster.
* Log redaction cannot be enabled or disabled when the cluster is in a paused state.
* After disabling log redaction, sensitive information may appear in TiDB logs, and there is a risk of data leakage. Make sure to inform and acknowledge this risk before proceeding.

# Disable Log Redaction
1. Navigate to your **dedicated cluster** in the TiDB Cloud Console.
2. From the left navigation bar, go to: **Settings > Security**
3. In the **Execution Log Redaction** section:
    * You will see the redaction feature is enabled by default.
4. Click the **Disable** button.
    * A warning will appear, explaining the risks of disabling log redaction.
    * You must confirm your action twice.
5. After disabling:
    * The change will apply to new database connections only.
    * Existing connections are unaffected; reconnect to apply changes.
    * Logs for new sessions will no longer be redacted.

> **Note:**
>
> Disabling log redaction may expose sensitive information and increase the risk of data leakage. Please remember to enable as soon as your diagnostic or maintenance task is complete.
>

# Confirm Log Redaction is Disabled
1. Generate a **slow query**
2. Wait a few minutes for the slow query log to update.
3. Review the log to confirm sensitive data appears unredacted.

# Enable Log Redaction
To maintain security, **enable log redaction** as soon as your diagnostic or maintenance task is complete.
1. Go to: **Settings** > **Security**
2. Click the **Enable** button.
3. **Reconnect to the database** for the change to take effect on new sessions.



