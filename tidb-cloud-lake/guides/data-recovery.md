---
title: Data Recovery
summary: This topic explains how to back up and restore data in {{{ .lake }}}.
---

# Data Recovery

This topic explains how to back up and restore data in {{{ .lake }}}.

## Time Travel: Easy Access to Past Data

With {{{ .lake }}} Time Travel, you can revisit and retrieve data from the past, even if it's been altered or removed. It's perfect for:

- **Getting Back Deleted Data:** Helps you get back important things like tables, databases that were deleted, whether by accident or on purpose.

- **Copying and Saving Past Data:** Lets you copy and save important data from earlier times.

- **Looking at Past Data Use:** Makes it easier to see how data was used or changed at certain times.

### Main Uses of Time Travel

- **Access Past Data**: Look at data from the past, even if it has been changed or deleted.
- **Recover Lost Data**: Bring back tables and databases that were deleted using the [FLASHBACK TABLE](/tidb-cloud-lake/sql/flashback-table.md) command.

### Time Travel SQL Extensions

- **SQL Extensions for Time Travel:** Use special SQL clauses like [`AT`](/tidb-cloud-lake/sql/at.md) in SELECT statements and CREATE commands to specify the exact point in history you want to access.
- **Revive Deleted Data:** Use the `UNDROP` command for tables, databases.

### Setting the Data Retention Period

- **Personal Edition**: Choose between no retention (0 days) or the default of **1 day**.
- **Business Edition and Higher**:
    - For temporary data: Set to 0 or the default of **1 day**.
    - For permanent data: Choose any period from **0 to 90 days**.

> **Note:**
>
> Setting a retention period of 0 days means Time Travel won't be available for that data.

### Adjusting Data Retention Time

Change the data keeping time with the `DATA_RETENTION_TIME_IN_DAYS` setting, which is usually 1 day. This decides how long to keep old data.

## Fail-safe: Extra Protection for Your Data

Fail-safe in {{{ .lake }}} is an additional safety feature, different from Time Travel. It's designed to protect your data in case of system issues or security incidents.

### How Fail-safe Works

Fail-safe offers a fixed 7-day recovery window after the Time Travel period ends.

Fail-safe includes:

- **MetaData Recovery:** Uses versioning in the meta-service to recover deleted tables.
- **Data Recovery:** Uses AWS S3's versioning to save data that's been changed or deleted.

> **Note:**
>
> - Fail-safe is an emergency service, not user-configurable, provided by {{{ .lake }}}.
> - It should be used only after other recovery methods don't work.
> - Not intended for regular historical data access beyond the Time Travel period.
> - For restoring data after big problems, and you can't set it up yourself.
> - Recovery times can vary from a few hours to several days, depending on the situation.
