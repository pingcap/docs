---
title: TiDB Dashboard User Management
summary: TiDB ダッシュボードは、TiDB と同じユーザー権限システムを使用します。SQL ユーザーは、ダッシュボードにアクセスするために、PROCESS、SHOW DATABASES、CONFIG、DASHBOARD_CLIENT などの特定の権限が必要です。意図しない操作を防ぐために、必要な権限のみを持つユーザーを作成することをお勧めします。高い権限を持つユーザーもサインインできます。最小限の権限を持つ SQL ユーザーを作成するには、必要な権限を付与し、必要に応じてロールベースのアクセス制御 (RBAC) を使用します。
---

# TiDBダッシュボードユーザー管理 {#tidb-dashboard-user-management}

TiDB ダッシュボードは、TiDB と同じユーザー権限システムとサインイン認証を使用します。TiDB TiDB SQLユーザーを制御および管理して、TiDB ダッシュボードへのアクセスを制限できます。このドキュメントでは、 TiDB SQLユーザーが TiDB ダッシュボードにアクセスするために必要な最小限の権限について説明し、最小限の権限を持つ SQL ユーザーを作成する方法と RBAC 経由で承認する方法を例示します。

TiDB SQLユーザーを制御および管理する方法の詳細については、 [TiDB ユーザーアカウント管理](/user-account-management.md)参照してください。

## 必要な権限 {#required-privileges}

-   接続された TiDBサーバーで[Security強化モード (SEM)](/system-variables.md#tidb_enable_enhanced_security)が有効になっていない場合に TiDB ダッシュボードにアクセスするには、SQL ユーザーに次の**すべて**の権限が必要です。

    -   プロセス
    -   データベースを表示
    -   構成
    -   ダッシュボードクライアント

-   接続された TiDBサーバーで[Security強化モード (SEM)](/system-variables.md#tidb_enable_enhanced_security)が有効になっているときに TiDB ダッシュボードにアクセスするには、SQL ユーザーに次の**すべて**の権限が必要です。

    -   プロセス
    -   データベースを表示
    -   構成
    -   ダッシュボードクライアント
    -   制限付きテーブル管理者
    -   制限付きステータス管理者
    -   制限付き変数管理者

-   TiDB ダッシュボードにサインインした後、インターフェイスの設定を変更するには、SQL ユーザーに次の権限も必要です。

    -   システム変数管理者

-   TiDB ダッシュボードにサインインした後、インターフェイスの[高速バインド実行プラン](/dashboard/dashboard-statement-details.md#fast-plan-binding)機能を使用するには、SQL ユーザーに次の権限も必要です。

    -   システム変数管理者
    -   素晴らしい

> **注記：**
>
> `ALL PRIVILEGES`や`SUPER`などの高い権限を持つユーザーも TiDB ダッシュボードにサインインできます。したがって、最小権限の原則に準拠するには、意図しない操作を防ぐために必要な権限のみを持つユーザーを作成することを強くお勧めします。これらの権限の詳細については、 [権限管理](/privilege-management.md)参照してください。

SQL ユーザーが前述の権限要件を満たしていない場合、以下に示すように、そのユーザーは TiDB ダッシュボードへのサインインに失敗します。

![insufficient-privileges](/media/dashboard/dashboard-user-insufficient-privileges.png)

## 例: TiDB ダッシュボードにアクセスするための最小権限の SQL ユーザーを作成する {#example-create-a-least-privileged-sql-user-to-access-tidb-dashboard}

-   接続された TiDBサーバーで[Security強化モード (SEM)](/system-variables.md#tidb_enable_enhanced_security)有効になっていない場合、TiDB ダッシュボードにサインインできる SQL ユーザー`dashboardAdmin`を作成するには、次の SQL ステートメントを実行します。

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

-   接続された TiDBサーバーで[Security強化モード (SEM)](/system-variables.md#tidb_enable_enhanced_security)が有効になっている場合は、まず SEM を無効にし、次の SQL ステートメントを実行して、TiDB ダッシュボードにサインインできる SQL ユーザー`dashboardAdmin`を作成します。ユーザーを作成したら、SEM を再度有効にします。

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

## 例: RBAC 経由で SQL ユーザーに TiDB ダッシュボードへのアクセスを許可する {#example-authorize-sql-user-to-access-tidb-dashboard-via-rbac}

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

上記の手順を実行すると、 `dashboardAdmin`ユーザーを使用して TiDB ダッシュボードにサインインできるようになります。

## TiDBダッシュボードにサインイン {#sign-in-to-tidb-dashboard}

TiDB ダッシュボードの権限要件を満たす SQL ユーザーを作成したら、このユーザーを TiDB ダッシュ[サインイン](/dashboard/dashboard-access.md#sign-in)に使用できます。
