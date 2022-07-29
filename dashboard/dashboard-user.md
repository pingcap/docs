---
title: TiDB Dashboard User Management
summary: Learn how to create SQL users to access TiDB Dashboard.
---

# TiDBダッシュボードユーザー管理 {#tidb-dashboard-user-management}

TiDBダッシュボードは、TiDBと同じユーザー特権システムとサインイン認証を使用します。 TiDB SQLユーザーを制御および管理して、TiDBダッシュボードへのアクセスを制限できます。このドキュメントでは、 TiDB SQLユーザーがTiDBダッシュボードにアクセスするために必要な最小特権について説明し、最小特権のSQLユーザーを作成する方法とRBACを介して認証する方法を例示します。

TiDB SQLユーザーを制御および管理する方法の詳細については、 [TiDBユーザーアカウント管理](/user-account-management.md)を参照してください。

## 必要な特権 {#required-privileges}

-   接続されたTiDBサーバーで[セキュリティ強化モード（SEM）](/system-variables.md#tidb_enable_enhanced_security)が有効になっていないときにTiDBダッシュボードにアクセスするには、SQLユーザーに次の**すべて**の権限が必要です。

    -   処理する
    -   データベースを表示する
    -   CONFIG
    -   DASHBOARD_CLIENT

-   接続されたTiDBサーバーで[セキュリティ強化モード（SEM）](/system-variables.md#tidb_enable_enhanced_security)が有効になっているときにTiDBダッシュボードにアクセスするには、SQLユーザーに次の**すべて**の権限が必要です。

    -   処理する
    -   データベースを表示する
    -   CONFIG
    -   DASHBOARD_CLIENT
    -   RESTRICTED_TABLES_ADMIN
    -   RESTRICTED_STATUS_ADMIN
    -   RESTRICTED_VARIABLES_ADMIN

-   TiDBダッシュボードにサインインした後にインターフェイスの構成を変更するには、SQLユーザーに次の権限も必要です。

    -   SYSTEM_VARIABLES_ADMIN

> **ノート：**
>
> `ALL PRIVILEGES`や`SUPER`などの高い権限を持つユーザーは、TiDBダッシュボードにもサインインできます。したがって、最小特権の原則に準拠するために、意図しない操作を防ぐためにのみ、必要な特権を持つユーザーを作成することを強くお勧めします。これらの特権の詳細については、 [権限管理](/privilege-management.md)を参照してください。

SQLユーザーが前述の特権要件を満たしていない場合、以下に示すように、ユーザーはTiDBダッシュボードへのサインインに失敗します。

![insufficient-privileges](/media/dashboard/dashboard-user-insufficient-privileges.png)

## 例：TiDBダッシュボードにアクセスするための最小特権SQLユーザーを作成します {#example-create-a-least-privileged-sql-user-to-access-tidb-dashboard}

-   接続されたTiDBサーバーで[セキュリティ強化モード（SEM）](/system-variables.md#tidb_enable_enhanced_security)が有効になっていない場合、TiDBダッシュボードにサインインできるSQLユーザー`dashboardAdmin`を作成するには、次のSQLステートメントを実行します。

    ```sql
    CREATE USER 'dashboardAdmin'@'%' IDENTIFIED BY '<YOUR_PASSWORD>';
    GRANT PROCESS, CONFIG ON *.* TO 'dashboardAdmin'@'%';
    GRANT SHOW DATABASES ON *.* TO 'dashboardAdmin'@'%';
    GRANT DASHBOARD_CLIENT ON *.* TO 'dashboardAdmin'@'%';

    -- To modify the configuration items on the interface after signing in to TiDB Dashboard, the user-defined SQL user must be granted with the following privilege.
    GRANT SYSTEM_VARIABLES_ADMIN ON *.* TO 'dashboardAdmin'@'%';
    ```

-   接続されたTiDBサーバーで[セキュリティ強化モード（SEM）](/system-variables.md#tidb_enable_enhanced_security)が有効になっている場合は、最初にSEMを無効にし、次のSQLステートメントを実行して、TiDBダッシュボードにサインインできるSQLユーザー`dashboardAdmin`を作成します。ユーザーを作成したら、SEMを再度有効にします。

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
    ```

## 例：SQLユーザーにRBAC経由でTiDBダッシュボードにアクセスすることを許可します {#example-authorize-sql-user-to-access-tidb-dashboard-via-rbac}

次の例は、 [役割ベースのアクセス制御（RBAC）](/role-based-access-control.md)メカニズムを介してTiDBダッシュボードにアクセスするためのロールとユーザーを作成する方法を示しています。

1.  TiDBダッシュボードの特権要件を満たす`dashboard_access`の役割を作成します。

    ```sql
    CREATE ROLE 'dashboard_access';
    GRANT PROCESS, CONFIG ON *.* TO 'dashboard_access'@'%';
    GRANT SHOW DATABASES ON *.* TO 'dashboard_access'@'%';
    GRANT DASHBOARD_CLIENT ON *.* TO 'dashboard_access'@'%';
    GRANT SYSTEM_VARIABLES_ADMIN ON *.* TO 'dashboard_access'@'%';
    ```

2.  他のユーザーに`dashboard_access`の役割を付与し、デフォルトの役割として`dashboard_access`を設定します。

    ```sql
    CREATE USER 'dashboardAdmin'@'%' IDENTIFIED BY '<YOUR_PASSWORD>';
    GRANT 'dashboard_access' TO 'dashboardAdmin'@'%';
    -- You need to set dashboard_access as the default role to the user
    SET DEFAULT ROLE dashboard_access to 'dashboardAdmin'@'%';
    ```

上記の手順の後、 `dashboardAdmin`人のユーザーを使用してTiDBダッシュボードにサインインできます。

## TiDBダッシュボードにサインインする {#sign-in-to-tidb-dashboard}

TiDBダッシュボードの特権要件を満たすSQLユーザーを作成した後、このユーザーをTiDBダッシュボードに[ログイン](/dashboard/dashboard-access.md#sign-in)対1で使用できます。
