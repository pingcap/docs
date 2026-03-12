---
title: Worksheets
---

import DbSVG from '@site/static/img/icon/database.svg'
import RoleSVG from '@site/static/img/icon/role.svg'
import WarehouseSVG from '@site/static/img/icon/warehouse.svg'
import EllipsisSVG from '@site/static/img/icon/ellipsis.svg'

Worksheets in Databend Cloud are used to organize, run, and save SQL statements. They can also be shared with others in your organization.

## Creating a Worksheet

To create a new worksheet, click on **Worksheets** in the sidebar and select **New Worksheet**.

If your SQL statements are already saved in an SQL file, you can also create a worksheet directly from the file. To do so, click the ellipsis icon <EllipsisSVG/> to the right of **New Worksheet**, then select **Create from SQL File**.

## Editing and Running SQL Statements

To edit and run an SQL statement:

1. Click on the database icon <DbSVG/> above the SQL editor and select the database you want to query.
2. Click on the user icon <RoleSVG/> above the SQL editor and choose a role to use. The dropdown list will display all the roles you have been granted, along with any child roles under your roles in the hierarchy. For more information about the role hierarchy, see [Inheriting Roles & Establishing Hierarchy](/guides/security/access-control/roles#inheriting-roles--establishing-hierarchy).

3. Edit the SQL statement in the SQL editor.
4. Click on the warehouse icon <WarehouseSVG/> under the SQL editor and select a warehouse from the list.
5. Click **Run Script**.

The query result shows in the output area. You can click **Export** to save the whole result to a CSV file, or select one or multiple cells in the output area and press Command + C (on Mac) or Ctrl + C (on Windows) to copy them to your clipboard.

:::tip

- Multiple SQL statements in a single API call are not supported. Ensure that each SQL query in the worksheet ends with a single semicolon (;).
- To make it easier for you to edit SQL statements, you can select a table in the database list and click the "..." button next to it. Then, follow the menu prompts to choose to copy the table name or all column names to the SQL input area on the right in one click.

- If you enter multiple statements in the SQL input area, Databend Cloud will only execute the statement where the cursor is located. You can move the cursor to execute other statements. Additionally, you can use keyboard shortcuts: Ctrl + Enter (Windows) or Command + Enter (Mac) to execute the current statement, and Ctrl + Shift + Enter (Windows) or Command + Shift + Enter (Mac) to execute all statements.
  :::

## Sharing a Worksheet

You can share your worksheets with everyone in your organization or specific individuals. To do so, click **Share** in the worksheet you want to share, or click **Share this Folder** to share a worksheet folder.

![Alt text](@site/static/img/documents/worksheet/share.png)

In the dialog box that appears, select the sharing scope. You can copy and share the link with the intended recipients, who will also receive an email notification. Please note that if you choose the **Designated Members** scope, recipients must click the link you share for the sharing to be successful.

- To view the worksheets shared with you by others, click **Worksheets** in the sidebar, then click the **Shared with Me** tab on the right.
- When you share a worksheet with others, they can execute the SQL statements in it if they have the necessary permissions, but they won't be able to make any edits to the statements.

## Exporting Query Results

Databend Cloud provides the ability to export query results. However, this feature requires the organization Owner to grant the **EXPORT** permission to team members. For data security purposes, this feature is disabled by default.

![Alt text](@site/static/img/documents/worksheet/download.png)

If you need to use this feature, please contact your organization Owner to enable the permission(**Admin** > **Users & Roles**):

![Alt text](@site/static/img/documents/worksheet/export.png)
