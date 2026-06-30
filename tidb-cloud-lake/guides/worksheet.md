---
title: Worksheets
summary: Worksheets in TiDB Cloud Lake are used to organize, run, and save SQL statements. They can also be shared with others in your organization.
---

# Worksheets

Worksheets in {{{ .lake }}} are used to organize, run, and save SQL statements. They can also be shared with others in your organization.

## Creating a Worksheet

To create a new worksheet, click on **Worksheets** in the sidebar and select **New Worksheet**.

If your SQL statements are already saved in an SQL file, you can also create a worksheet directly from the file. To do so, click the ellipsis icon <svg t="1722479222306" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="2315" width="16" height="16"><path d="M213.333333 512a85.333333 85.333333 0 1 1-85.333333-85.333333 85.333333 85.333333 0 0 1 85.333333 85.333333z m298.666667-85.333333a85.333333 85.333333 0 1 0 85.333333 85.333333 85.333333 85.333333 0 0 0-85.333333-85.333333z m384 0a85.333333 85.333333 0 1 0 85.333333 85.333333 85.333333 85.333333 0 0 0-85.333333-85.333333z" fill="#1677FF" p-id="2316"></path></svg> to the right of **New Worksheet**, then select **Create from SQL File**.

## Editing and Running SQL Statements

To edit and run an SQL statement:

1. Click on the database icon <svg t="1721790323165" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="4273" width="16" height="16"><path d="M522.666667 96l8.533333 0.042667a910.08 910.08 0 0 1 91.562667 5.333333l14.549333 1.706667 15.402667 2.133333 15.125333 2.410667 7.573333 1.322666 14.890667 2.837334c125.205333 25.322667 212.928 79.488 216.256 150.677333l0.106667 4.202667v448c0 73.258667-88.704 129.066667-216.362667 154.88l-14.890667 2.837333-7.573333 1.322667-15.125333 2.389333-15.402667 2.133333c-36.266667 4.650667-74.773333 7.104-114.645333 7.104-39.872 0-78.378667-2.453333-114.645334-7.104l-15.402666-2.133333-15.125334-2.389333c-137.088-23.189333-235.264-79.488-238.72-154.901334L138.666667 714.666667v-448l0.106666-4.202667c3.328-71.189333 91.050667-125.354667 216.256-150.677333l14.890667-2.837334 7.573333-1.322666 15.125334-2.389334 15.402666-2.133333a892.202667 892.202667 0 0 1 97.642667-6.954667L522.666667 96z" fill="#1677FF" p-id="4274"></path></svg> above the SQL editor and select the database you want to query.
2. Click on the user icon <svg t="1721790740383" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="5380" width="16" height="16"><path d="M994.048 857.7024a36.4544 36.4544 0 0 0-70.6048 17.8688c5.5808 22.2208 9.4208 44.9024 11.4176 67.8912H89.1904c18.432-216.1152 199.5776-386.4064 420.096-387.7888 0.9216 0 1.7408 0.256 2.6624 0.256a256 256 0 1 0-256-256c0 84.8896 41.7792 159.5904 105.4208 206.1312C160.6144 570.0096 14.6944 758.1696 14.6944 979.8656c0 20.1216 16.3328 36.4544 36.4544 36.4544h921.6a36.4544 36.4544 0 0 0 36.4544-36.4544 494.1312 494.1312 0 0 0-15.1552-122.1632zM512 120.832c98.816 0 179.2 80.384 179.2 179.2s-80.384 179.2-179.2 179.2-179.2-80.384-179.2-179.2 80.384-179.2 179.2-179.2z" fill="#438CFF" p-id="5381"></path><path d="M579.7376 666.368a38.4 38.4 0 1 0-54.3232 54.3232l129.8432 129.792a38.2976 38.2976 0 0 0 54.272 0l274.6368-274.6368a38.4 38.4 0 1 0-54.3232-54.3232l-247.5008 247.5008-102.6048-102.656z" fill="#438CFF" p-id="5382"></path></svg> above the SQL editor and choose a role to use. The dropdown list will display all the roles you have been granted, along with any child roles under your roles in the hierarchy. For more information about the role hierarchy, see [Inheriting Roles & Establishing Hierarchy](/tidb-cloud-lake/guides/roles.md#inheriting-roles--establishing-hierarchy).

3. Edit the SQL statement in the SQL editor.
4. Click on the warehouse icon <svg stroke="#1677FF" fill="transparent" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"><path d="M9.632 17H17V3H6.316v3.684"></path><path d="M3 6.684h6.632V17H3V6.684z"></path><path d="M5.947 14.79h.737"></path><path d="M11.474 14.79h.736"></path></svg> under the SQL editor and select a warehouse from the list.
5. Click **Run Script**.

The query result shows in the output area. You can click **Export** to save the whole result to a CSV file, or select one or multiple cells in the output area and press Command + C (on Mac) or Ctrl + C (on Windows) to copy them to your clipboard.

> **Tip:**
>
> - Multiple SQL statements in a single API call are not supported. Ensure that each SQL query in the worksheet ends with a single semicolon (;).
> - To make it easier for you to edit SQL statements, you can select a table in the database list and click the "..." button next to it. Then, follow the menu prompts to choose to copy the table name or all column names to the SQL input area on the right in one click.
>
> - If you enter multiple statements in the SQL input area, {{{ .lake }}} will only execute the statement where the cursor is located. You can move the cursor to execute other statements. Additionally, you can use keyboard shortcuts: Ctrl + Enter (Windows) or Command + Enter (Mac) to execute the current statement, and Ctrl + Shift + Enter (Windows) or Command + Shift + Enter (Mac) to execute all statements.

## Query Result Defaults

{{{ .lake }}} applies the following default limits to query results displayed in the worksheet output area:

| Setting | Default | Description |
|---|---|---|
| Max display rows | 10,000 | Only the first 10,000 rows are shown in the preview. |
| Max display columns | 200 | Only the first 200 columns are shown in the preview. |
| Max cell content length | 3,000 characters | Cell values longer than this are truncated in the display. |

The row and column limits are fixed. To adjust the max cell content length, click the settings icon in the bottom-right corner of the result area and choose a value (3K–Unlimited). Note that setting a very large value or **Unlimited** may cause the browser to slow down or become unresponsive when working with large result sets.

## Sharing a Worksheet

You can share your worksheets with everyone in your organization or specific individuals. To do so, click **Share** in the worksheet you want to share, or click **Share this Folder** to share a worksheet folder.

![Alt text](/media/tidb-cloud-lake/share.png)

In the dialog box that appears, select the sharing scope. You can copy and share the link with the intended recipients, who will also receive an email notification. Please note that if you choose the **Designated Members** scope, recipients must click the link you share for the sharing to be successful.

- To view the worksheets shared with you by others, click **Worksheets** in the sidebar, then click the **Shared with Me** tab on the right.
- When you share a worksheet with others, they can execute the SQL statements in it if they have the necessary permissions, but they won't be able to make any edits to the statements.

## Exporting Query Results

{{{ .lake }}} provides the ability to export query results. However, this feature requires the organization Owner to grant the **EXPORT** permission to team members. For data security purposes, this feature is disabled by default.

If you need to use this feature, please contact your organization Owner to enable the permission(**Admin** > **Users & Roles**).
