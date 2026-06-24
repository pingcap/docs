---
title: Tableau
summary: Tableau is a visual analytics platform transforming the way we use data to solve problems. You can connect Tableau to TiDB Cloud Lake through Tableau's Other Databases (JDBC) interface by using the lake-jdbc driver.
---

# Tableau

[Tableau](https://www.tableau.com/) is a visual analytics platform transforming the way we use data to solve problems. You can connect Tableau to {{{ .lake }}} through Tableau's **Other Databases (JDBC)** interface by using the [lake-jdbc driver](https://github.com/tidbcloud/lake-jdbc).

For optimal compatibility, use Tableau version 2022.3 or later.

## Tutorial: Integrating with {{{ .lake }}}

This tutorial guides you through connecting Tableau Desktop to {{{ .lake }}} with `lake-jdbc`.

### Step 1. Obtain Connection Information

Obtain the connection information for your {{{ .lake }}} warehouse. For more details, see [Connecting to a Warehouse](/tidb-cloud-lake/guides/warehouse.md#connecting-to-a-warehouse).

### Step 2. Install lake-jdbc

1. Download `lake-jdbc` version `0.4.6` or later from one of the following locations:

    - [lake-jdbc GitHub repository](https://github.com/tidbcloud/lake-jdbc)
    - [lake-jdbc on Maven Central](https://repo1.maven.org/maven2/com/tidbcloud/lake-jdbc/)

2. Move the driver JAR file, for example `lake-jdbc-0.4.6.jar`, to Tableau's driver folder.

    | Operating System | Tableau's Driver Folder          |
    | ---------------- | -------------------------------- |
    | MacOS            | ~/Library/Tableau/Drivers        |
    | Windows          | C:\Program Files\Tableau\Drivers |
    | Linux            | /opt/tableau/tableau_driver/jdbc |

### Step 3. Connect to {{{ .lake }}}

1. Launch Tableau Desktop and select **Other Databases (JDBC)** in the sidebar.

    ![Other Databases (JDBC)](/media/tidb-cloud-lake/bi-tableau-1.png)

2. In the window, provide your {{{ .lake }}} connection information and click **Sign In**.

    | Parameter | Description                               | For This Tutorial                                                   |
    | --------- | ----------------------------------------- | ------------------------------------------------------------------- |
    | URL       | Format: `jdbc:lake://{user}:{password}@{host}:{port}/{database}` | `jdbc:lake://cloudapp:<your-password>@<your-host>:443/default` |
    | Dialect   | Select "MySQL" for SQL dialect.           | MySQL                                                               |
    | Username  | SQL user for connecting to {{{ .lake }}}  | cloudapp                                                            |
    | Password  | SQL user password                         | Your password                                                       |

3. When the Tableau workbook opens, select the database, schema, and tables that you want to query. For this tutorial, select _default_ for both **Database** and **Schema**.

You're all set! You can now drag tables to the work area to start your query and further analysis.
