---
title: "Monitoring Usage"
---

Databend Cloud provides monitoring functionality to help you gain a comprehensive understanding of your and your organization members' usage on the platform. To access the **Monitor** page, click **Monitor** in the sidebar menu on the homepage. The page includes the following tabs:

- [Metrics](#metrics)
- [SQL History](#sql-history)
- [Task History](#task-history)
- [Audit](#audit): Visible to `account_admin` users only.

## Metrics

The **Metrics** tab presents charts that visually illustrate usage statistics for the following metrics, covering data from the past hour, day, or week:

- Storage Size
- SQL Query Count
- Session Connections
- Data Scanned / Written
- Warehouse Status
- Rows Scanned / Written

## SQL History

The **SQL History** tab displays a list of SQL statements that have been executed by all users within your organization. By clicking **Filter** at the top of the list, you can filter records by multiple dimensions.

Clicking a record on the **SQL History** page reveals detailed information on how Databend Cloud executed the SQL statement, providing access to the following tabs:

- **Query Details**: Includes Query State (success or failure), Rows Scanned, Warehouse, Bytes Scanned, Start Time, End Time, and Handler Type.
- **Query Profile**: Illustrates how the SQL statement was executed.

## Task History

The **Task History** tab offers a comprehensive log of all executed tasks within your organization, enabling users to review task settings and monitor their status.

## Audit

The **Audit** tab records the operation logs of all organization members, including the operation type, operation time, IP address, and the account of the operator. By clicking **Filter** at the top of the list, you can filter records by multiple dimensions.