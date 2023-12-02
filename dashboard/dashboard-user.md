---
title: TiDB Dashboard User Management
summary: Learn how to create SQL users to access TiDB Dashboard.
---

# TiDB ダッシュボードのユーザー管理 {#tidb-dashboard-user-management}

TiDB ダッシュボードは、TiDB と同じユーザー権限システムとサインイン認証を使用します。 TiDB SQLユーザーを制御および管理して、TiDB ダッシュボードへのアクセスを制限できます。このドキュメントでは、 TiDB SQLユーザーが TiDB ダッシュボードにアクセスするために必要な最小限の権限について説明し、最小限の権限を持つ SQL ユーザーを作成する方法と RBAC を介して認証する方法を例示します。

TiDB SQLユーザーを制御および管理する方法の詳細については、 [TiDB ユーザーアカウント管理](/user-account-management.md)を参照してください。

## 必要な権限 {#required-privileges}

-   接続された TiDBサーバーで[Security強化モード (SEM)](/system-variables.md#tidb_enable_enhanced_security)が有効になっていない場合に TiDB ダッシュボードにアクセスするには、SQL ユーザーは次の**すべての**権限を持っている必要があります。

    -   プロセス
    -   データベースを表示する
    -   設定
    -   ダッシュボード_クライアント

-   接続された TiDBサーバーで[Security強化モード (SEM)](/system-variables.md#tidb_enable_enhanced_security)が有効になっているときに TiDB ダッシュボードにアクセスするには、SQL ユーザーは次の**すべての**権限を持っている必要があります。

    -   プロセス
    -   データベースを表示する
    -   設定
    -   ダッシュボード_クライアント
    -   RESTRICTED_TABLES_ADMIN
    -   RESTRICTED_STATUS_ADMIN
    -   RESTRICTED_VARIABLES_ADMIN

-   TiDB ダッシュボードにサインインした後にインターフェースの構成を変更するには、SQL ユーザーは次の権限も持っている必要があります。

    -   SYSTEM_VARIABLES_ADMIN

-   TiDB ダッシュボードにサインインした後、インターフェイスで[高速バインド実行計画](/dashboard/dashboard-statement-details.md#fast-plan-binding)機能を使用するには、SQL ユーザーは次の権限も持っている必要があります。

    -   SYSTEM_VARIABLES_ADMIN
    -   素晴らしい

> **注記：**
>
> `ALL PRIVILEGES`や`SUPER`などの高い権限を持つユーザーも、TiDB ダッシュボードにサインインできます。したがって、最小特権の原則に従うために、意図しない操作を防ぐためにのみ必要な権限を持つユーザーを作成することを強くお勧めします。これらの権限の詳細については、 [権限管理](/privilege-management.md)参照してください。

SQL ユーザーが前述の権限要件を満たしていない場合、以下に示すように、ユーザーは TiDB ダッシュボードへのサインインに失敗します。

![insufficient-privileges](/media/dashboard/dashboard-user-insufficient-privileges.png)

## 例: TiDB ダッシュボードにアクセスするための最小権限の SQL ユーザーを作成する {#example-create-a-least-privileged-sql-user-to-access-tidb-dashboard}

-   接続された TiDBサーバーで[Security強化モード (SEM)](/system-variables.md#tidb_enable_enhanced_security)が有効になっていない場合、TiDB ダッシュボードにサインインできる SQL ユーザー`dashboardAdmin`を作成するには、次の SQL ステートメントを実行します。

    ```sql
    CREATE USER 'dashboardAdmin'@'%' IDENTIFIED BY '<YOUR_PASSWORD>';
    GRANT PROCESS, CONFIG ON *.* TO 'dashboardAdmin'@'%';
    GRANT SHOW DATABASES ON *.* TO 'dashboardAdmin'@'%';
    GRANT DASHBOARD_CLIENT ON *.* TO 'dashboardAdmin'@'%';

    -- To modify the configuration items on the interface after signing in to TiDB Dashboard, the user-defined SQL user must be granted with the following privilege.
    GRANT SYSTEM_VARIABLES_ADMIN ON *.* TO 'dashboardAdmin'@'%';

    -- To use the Fast Bind Executions Plan feature (https://docs.pingcap.com/tidb/v7.5/dashboard-statement-details#fast-plan-binding) on the interface after signing in to TiDB Dashboard, the user-defined SQL user must be granted with the following privileges.
    GRANT SYSTEM_VARIABLES_ADMIN ON *.* TO 'dashboardAdmin'@'%';
    GRANT SUPER ON *.* TO 'dashboardAdmin'@'%';
    ```

-   接続された TiDBサーバーで[Security強化モード (SEM)](/system-variables.md#tidb_enable_enhanced_security)が有効になっている場合は、まず SEM を無効にし、次の SQL ステートメントを実行して、TiDB ダッシュボードにサインインできる SQL ユーザー`dashboardAdmin`を作成します。ユーザーを作成した後、SEM を再度有効にします。

    ```sql
    CREATE USER 'dashboardAdmin'@'%' IDENTIFIED BY '<YOUR_PASSWORD>';
    GRANT PROCESS, CONFIG ON *.* TO 'dashboardAdmin'@'%';
    GRANT SHOW DATABASES ON *.* TO 'dashboardAdmin'@'%';
    GRANT DASHBOARD_CLIENT ON *.* TO 'dashboardAdmin'@'%';
    GRANT RESTRICTED_STATUS_ADMIN ON *.* TO 'dashboardAdmin'@'%';
    GRANT RESTRICTED_TABLES_ADMIN ON *.* TO 'dashboardAdmin'@'%';
    GRANT RESTRICTED_VARIABLES_ADMIN ON *.* TO 'dashboardAdmin'@'%';

    -- To modify the configuration items on the interface after signing in to TiDB Dashboard, the user-defined SQL user must be granted with the following privilege.
    GRANT SYSTEM_VARIABLES_ADMIN ON *.* TO 'dashboardAdmin'@'%';

    -- To use the Fast Bind Executions Plan feature (https://docs.pingcap.com/tidb/v7.5/dashboard-statement-details#fast-plan-binding) on the interface after signing in to TiDB Dashboard, the user-defined SQL user must be granted with the following privileges.
    GRANT SYSTEM_VARIABLES_ADMIN ON *.* TO 'dashboardAdmin'@'%';
    GRANT SUPER ON *.* TO 'dashboardAdmin'@'%';
    ```

## 例: SQL ユーザーに RBAC 経由で TiDB ダッシュボードにアクセスする権限を与える {#example-authorize-sql-user-to-access-tidb-dashboard-via-rbac}

次の例は、 [ロールベースのアクセス制御 (RBAC)](/role-based-access-control.md)メカニズムを通じて TiDB ダッシュボードにアクセスするためのロールとユーザーを作成する方法を示しています。

1.  TiDB ダッシュボードのすべての権限要件を満たす`dashboard_access`ロールを作成します。

    ```sql
    CREATE ROLE 'dashboard_access';
    GRANT PROCESS, CONFIG ON *.* TO 'dashboard_access'@'%';
    GRANT SHOW DATABASES ON *.* TO 'dashboard_access'@'%';
    GRANT DASHBOARD_CLIENT ON *.* TO 'dashboard_access'@'%';
    GRANT SYSTEM_VARIABLES_ADMIN ON *.* TO 'dashboard_access'@'%';
    GRANT SUPER ON *.* TO 'dashboardAdmin'@'%';    
    ```

2.  `dashboard_access`ロールを他のユーザーに付与し、 `dashboard_access`デフォルトのロールとして設定します。

    ```sql
    CREATE USER 'dashboardAdmin'@'%' IDENTIFIED BY '<YOUR_PASSWORD>';
    GRANT 'dashboard_access' TO 'dashboardAdmin'@'%';
    -- You need to set dashboard_access as the default role to the user
    SET DEFAULT ROLE dashboard_access to 'dashboardAdmin'@'%';
    ```

上記の手順を完了すると、 `dashboardAdmin`ユーザーを使用して TiDB ダッシュボードにサインインできるようになります。

## TiDB ダッシュボードにサインインする {#sign-in-to-tidb-dashboard}

TiDB ダッシュボードの権限要件を満たす SQL ユーザーを作成した後、このユーザーを TiDB ダッシュ[サインイン](/dashboard/dashboard-access.md#sign-in)に使用できます。
