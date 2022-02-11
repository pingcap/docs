---
title: TiDB Dashboard User Management
summary: Learn how to create SQL users to access TiDB Dashboard.
---

# TiDB Dashboard User Management

TiDB Dashboard uses the same user privilege system and sign-in authentication as TiDB. You can control and manage TiDB SQL users to limit their access to TiDB Dashboard. This document describes the least privileges required for TiDB SQL users to access TiDB Dashboard and exemplifies how to create a least-privileged SQL user.

For details about how to control and manage TiDB SQL users, see [TiDB User Account Management](/user-account-management.md).

## Required privileges

- To access TiDB Dashboard when [Security Enhanced Mode (SEM)](/system-variables.md#tidb_enable_enhanced_security) is not enabled on the connected TiDB server, the SQL user should have **all** the following privileges:

    - PROCESS
    - SHOW DATABASES
    - CONFIG
    - DASHBOARD_CLIENT

- To access TiDB Dashboard when [Security Enhanced Mode (SEM)](/system-variables.md#tidb_enable_enhanced_security) is enabled on the connected TiDB server, the SQL user should have **all** the following privileges:

    - PROCESS
    - SHOW DATABASES
    - CONFIG
    - DASHBOARD_CLIENT
    - RESTRICTED_TABLES_ADMIN
    - RESTRICTED_STATUS_ADMIN
    - RESTRICTED_VARIABLES_ADMIN

- To modify the configurations on the interface after signing in with TiDB Dashboard, the SQL user must also have the following privilege:

    - SYSTEM_VARIABLES_ADMIN

> **Note:**
>
> Users with high privileges such as `ALL PRIVILEGES` or `SUPER` can sign in with TiDB Dashboard as well. Therefore, to comply with the least privilege principle, it is highly recommended that you create users with the required privileges only to prevent unintended operations. See [Privilege Management](/privilege-management.md) for more information on these privileges.

If an SQL user does not meet the preceding privilege requirements, the user fails to sign in with TiDB Dashboard, as shown below.

![insufficient-privileges](/media/dashboard/dashboard-user-insufficient-privileges.png)

## Example: Create a least-privileged SQL user to access TiDB Dashboard

- When [Security Enhanced Mode (SEM)](/system-variables.md#tidb_enable_enhanced_security) is not enabled on the connected TiDB server, to create an SQL user `dashboardAdmin` that can sign in with TiDB Dashboard, execute the following SQL statements:

    ```sql
    CREATE USER 'dashboardAdmin'@'%' IDENTIFIED BY '<YOUR_PASSWORD>';
    GRANT PROCESS, CONFIG ON *.* TO 'dashboardAdmin'@'%';
    GRANT SHOW DATABASES ON *.* TO 'dashboardAdmin'@'%';
    GRANT DASHBOARD_CLIENT ON *.* TO 'dashboardAdmin'@'%';
    ```

    -- To modify the configuration items on the interface after signing in with TiDB Dashboard, the user-defined SQL user must be granted with the following privilege:

    ```sql
    GRANT SYSTEM_VARIABLES_ADMIN ON *.* TO 'dashboardAdmin'@'%';
    ```

- When [Security Enhanced Mode (SEM)](/system-variables.md#tidb_enable_enhanced_security) is enabled on the connected TiDB server, disable SEM first and execute the following SQL statements to create an SQL user `dashboardAdmin` that can sign in with TiDB Dashboard. After creating the user, enable SEM again:

    ```sql
    CREATE USER 'dashboardAdmin'@'%' IDENTIFIED BY '<YOUR_PASSWORD>';
    GRANT PROCESS, CONFIG ON *.* TO 'dashboardAdmin'@'%';
    GRANT SHOW DATABASES ON *.* TO 'dashboardAdmin'@'%';
    GRANT DASHBOARD_CLIENT ON *.* TO 'dashboardAdmin'@'%';
    GRANT RESTRICTED_STATUS_ADMIN ON *.* TO 'dashboardAdmin'@'%';
    GRANT RESTRICTED_TABLES_ADMIN ON *.* TO 'dashboardAdmin'@'%';
    GRANT RESTRICTED_VARIABLES_ADMIN ON *.* TO 'dashboardAdmin'@'%';
    ```

    -- To modify the configuration items on the interface after signing in with TiDB Dashboard, the user-defined SQL user must be granted with the following privilege:

    ```sql
    GRANT SYSTEM_VARIABLES_ADMIN ON *.* TO 'dashboardAdmin'@'%';
    ```

## Sign in with TiDB Dashboard

After creating an SQL user that meets the privilege requirements of TiDB Dashboard, you can use this user to [Sign in](/dashboard/dashboard-access.md#Sign in) with TiDB Dashboard.