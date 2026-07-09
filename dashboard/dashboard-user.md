---
title: TiDB Dashboard User Management
summary: TiDB Dashboardは、TiDBと同じユーザー権限システムを採用しています。SQLユーザーがダッシュボードにアクセスするには、PROCESS、SHOW DATABASES、CONFIG、DASHBOARD_CLIENTなどの特定の権限が必要です。意図しない操作を防ぐため、必要な権限のみを持つユーザーを作成することをお勧めします。高い権限を持つユーザーもサインインできます。最小限の権限を持つSQLユーザーを作成するには、必要な権限を付与し、必要に応じてロールベースアクセス制御（RBAC）を使用してください。
---

# TiDB Dashboardのユーザー管理 {#tidb-dashboard-user-management}

TiDB Dashboardは、TiDBと同じユーザー権限システムとサインイン認証を使用します。TiDB SQLユーザーを制御・管理することで、TiDB Dashboardへのアクセスを制限できます。このドキュメントでは、TiDB SQLユーザーがTiDB Dashboardにアクセスするために必要な最小限の権限について説明し、最小限の権限を持つSQLユーザーの作成方法とRBACによる認証方法を例示します。

TiDB SQLユーザーを制御および管理する方法の詳細については、 [TiDB ユーザーアカウント管理](/user-account-management.md)参照してください。

## 必要な権限 {#required-privileges}

-   接続された TiDBサーバーで[セキュリティ強化モード（SEM）](/system-variables.md#tidb_enable_enhanced_security)が有効になっていない場合に TiDB Dashboardにアクセスするには、SQL ユーザーに次の**すべての**権限が必要です。

    -   プロセス
    -   データベースを表示
    -   設定
    -   ダッシュボードクライアント

-   接続された TiDBサーバーで[セキュリティ強化モード（SEM）](/system-variables.md#tidb_enable_enhanced_security)が有効になっているときに TiDB Dashboardにアクセスするには、SQL ユーザーに次の**すべての**権限が必要です。

    -   プロセス
    -   データベースを表示
    -   設定
    -   ダッシュボードクライアント
    -   制限付きテーブル管理者
    -   制限付きステータス管理者
    -   制限付き変数管理者

-   TiDB Dashboardにサインインした後、インターフェイス上の構成を変更するには、SQL ユーザーに次の権限も必要です。

    -   システム変数管理者

-   TiDB Dashboardにサインインした後、インターフェース上の[高速バインド実行プラン](/dashboard/dashboard-statement-details.md#fast-plan-binding)機能を使用するには、SQL ユーザーに次の権限も必要です。

    -   システム変数管理者
    -   SUPER

> **注記：**
>
> `ALL PRIVILEGES`や`SUPER`といった高い権限を持つユーザーもTiDB Dashboardにサインインできます。したがって、最小権限の原則を遵守するために、意図しない操作を防ぐために、必要な権限のみを持つユーザーを作成することを強くお勧めします。これらの権限の詳細については、 [権限管理](/privilege-management.md)参照してください。

SQL ユーザーが前述の権限要件を満たしていない場合、以下に示すように、ユーザーは TiDB Dashboardへのサインインに失敗します。

![insufficient-privileges](/media/dashboard/dashboard-user-insufficient-privileges.png)

## 例: TiDB Dashboardにアクセスするための最小権限の SQL ユーザーを作成する {#example-create-a-least-privileged-sql-user-to-access-tidb-dashboard}

-   接続された TiDBサーバーで[セキュリティ強化モード（SEM）](/system-variables.md#tidb_enable_enhanced_security)が有効になっていない場合、TiDB Dashboardにサインインできる SQL ユーザー`dashboardAdmin`を作成するには、次の SQL ステートメントを実行します。

    ```sql
    CREATE USER 'dashboardAdmin'@'%' IDENTIFIED BY '<YOUR_PASSWORD>';
    GRANT PROCESS, CONFIG ON *.* TO 'dashboardAdmin'@'%';
    GRANT SHOW DATABASES ON *.* TO 'dashboardAdmin'@'%';
    GRANT DASHBOARD_CLIENT ON *.* TO 'dashboardAdmin'@'%';

    -- To modify the configuration items on the interface after signing in to TiDB Dashboard, the user-defined SQL user must be granted with the following privilege.
    GRANT SYSTEM_VARIABLES_ADMIN ON *.* TO 'dashboardAdmin'@'%';

    -- To use the Fast Bind Executions Plan feature (https://docs.pingcap.com/tidb/dev/dashboard-statement-details#fast-plan-binding) on the interface after signing in to TiDB Dashboard, the user-defined SQL user must be granted with the following privileges.
    GRANT SYSTEM_VARIABLES_ADMIN ON *.* TO 'dashboardAdmin'@'%';
    GRANT SUPER ON *.* TO 'dashboardAdmin'@'%';
    ```

-   接続先のTiDBサーバーで[セキュリティ強化モード（SEM）](/system-variables.md#tidb_enable_enhanced_security)が有効になっている場合は、まずSEMを無効にし、以下のSQL文を実行して、TiDB DashboardにサインインできるSQLユーザー`dashboardAdmin`を作成します。ユーザーを作成したら、SEMを再度有効にします。

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

    -- To use the Fast Bind Executions Plan feature (https://docs.pingcap.com/tidb/dev/dashboard-statement-details#fast-plan-binding) on the interface after signing in to TiDB Dashboard, the user-defined SQL user must be granted with the following privileges.
    GRANT SYSTEM_VARIABLES_ADMIN ON *.* TO 'dashboardAdmin'@'%';
    GRANT SUPER ON *.* TO 'dashboardAdmin'@'%';
    ```

## 例: RBAC 経由で SQL ユーザーに TiDB Dashboardへのアクセスを許可する {#example-authorize-sql-user-to-access-tidb-dashboard-via-rbac}

次の例は、 [ロールベースのアクセス制御（RBAC）](/role-based-access-control.md)メカニズムを通じて TiDB Dashboardにアクセスするためのロールとユーザーを作成する方法を示しています。

1.  TiDB Dashboardのすべての権限要件を満たす`dashboard_access`ロールを作成します。

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

上記の手順を実行すると、 `dashboardAdmin`ユーザーを使用して TiDB Dashboardにサインインできるようになります。

## TiDB Dashboardにサインイン {#sign-in-to-tidb-dashboard}

TiDB Dashboardの権限要件を満たす SQL ユーザーを作成したら、このユーザーを使用してTiDB Dashboardに[サインイン](/dashboard/dashboard-access.md#sign-in)できます。
