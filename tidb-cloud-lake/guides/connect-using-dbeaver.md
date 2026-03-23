---
title: DBeaver
summary: DBeaver supports connecting to {{{ .lake }}} using a built-in driver categorized under Analytical, available starting from version 24.3.1.
---

# DBeaver

[DBeaver](https://dbeaver.com/) supports connecting to {{{ .lake }}} using a built-in driver categorized under **Analytical**, available starting from **version 24.3.1**.

![Connect from DBeaver](/media/tidb-cloud-lake/dbeaver.png)

## Prerequisites

- DBeaver 24.3.1 or later version installed

## User Authentication

For connections to {{{ .lake }}}, you can use the default `cloudapp` user or an SQL user created with the [CREATE USER](/tidb-cloud-lake/sql/create-user.md) command. Please note that the user account you use to log in to the [{{{ .lake }}} console](https://app.lake.tidbcloud.com) cannot be used for connecting to {{{ .lake }}}.

## Connecting to {{{ .lake }}}

### Step 1: Obtain {{{ .lake }}} Connection Information

Log in to {{{ .lake }}} to obtain connection information. For more information, see [Connecting to a Warehouse](/tidb-cloud-lake/guides/warehouse.md#connecting).

![alt text](/media/tidb-cloud-lake/dbeaver-connect-info.png)

> **Note:**
>
> If your `user` or `password` contains special characters, you need to provide them separately in the corresponding fields (e.g., the `Username` and `Password` fields in DBeaver). In this case, {{{ .lake }}} will handle the necessary encoding for you. However, if you're providing the credentials together (e.g., as `user:password`), you must ensure that the entire string is properly encoded before use.

### Step 2: Configure {{{ .lake }}} Connection

1. In DBeaver, go to **Database** > **New Database Connection** to open the connection wizard, then select **Databend** under the **Analytical** category.

    ![alt text](/media/tidb-cloud-lake/dbeaver-analytical.png)

2. In the **Main** tab, enter the **Host**, **Port**, **Username**, and **Password** based on the connection information obtained in the previous step.

    ![alt text](/media/tidb-cloud-lake/dbeaver-main-tab.png)

3. In the **Driver properties** tab, enter the **Warehouse** name based on the connection information obtained in the previous step.

    ![alt text](/media/tidb-cloud-lake/dbeaver-driver-properties.png)

4. In the **SSL** tab, select the **Use SSL** checkbox.

    ![alt text](/media/tidb-cloud-lake/dbeaver-use-ssl.png)

5. Click **Test Connection** to verify the connection. If this is your first time connecting to {{{ .lake }}}, you will be prompted to download the driver. Click **Download** to proceed. Once the download is complete, the test connection should succeed:

    ![alt text](/media/tidb-cloud-lake/dbeaver-cloud-success.png)
