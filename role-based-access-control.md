---
title: Role-Based Access Control
summary: このドキュメントでは、TiDB RBAC の操作と実装について説明します。
---

# ロールベースのアクセス制御 {#role-based-access-control}

TiDB のロールベース アクセス制御 (RBAC) システムの実装は、MySQL 8.0 の実装と似ています。TiDB は、MySQL のほとんどの RBAC 構文と互換性があります。

このドキュメントでは、TiDB RBAC 関連の操作と実装について説明します。

## RBAC 操作 {#rbac-operations}

ロールは一連の権限の集合です。次の操作を実行できます。

-   ロールを作成します。
-   ロールを削除します。
-   ロールに権限を付与します。
-   別のユーザーにロールを付与します。ロールを有効にすると、そのユーザーはロールに関連する権限を取得できます。

### ロールを作成する {#create-a-role}

たとえば、次のステートメントを使用して、ロール`app_developer` 、 `app_read` 、および`app_write`を作成できます。

```sql
CREATE ROLE 'app_developer', 'app_read', 'app_write';
```

ロールの命名形式とルールについては、 [TiDB ユーザーアカウント管理](/user-account-management.md)参照してください。

ロールは`mysql.user`テーブルに保存され、ロール名のホスト名部分 (省略されている場合) はデフォルトで`'%'`になります。作成しようとしているロールの名前は一意である必要があります。一意でない場合は、エラーが報告されます。

ロールを作成するには、権限`CREATE ROLE`または`CREATE USER`必要です。

### ロールに権限を付与する {#grant-a-privilege-to-a-role}

ロールに権限を付与する操作は、ユーザーに権限を付与する操作と同じです。詳細については、 [TiDB権限管理](/privilege-management.md)参照してください。

たとえば、次のステートメントを使用して、 `app_read`ロールに`app_db`データベースを読み取る権限を付与できます。

```sql
GRANT SELECT ON app_db.* TO 'app_read'@'%';
```

次のステートメントを使用して、 `app_write`ロールに`app_db`データベースにデータを書き込む権限を付与できます。

```sql
GRANT INSERT, UPDATE, DELETE ON app_db.* TO 'app_write'@'%';
```

次のステートメントを使用して、 `app_developer`ロールに`app_db`データベースのすべての権限を付与できます。

```sql
GRANT ALL ON app_db.* TO 'app_developer';
```

### ユーザーにロールを付与する {#grant-a-role-to-a-user}

ユーザー`dev1` `app_db`に対するすべての権限を持つ開発者ロールを持ち、ユーザー`read_user1`と`read_user2` `app_db`に対する読み取り専用権限を持ち、ユーザー`rw_user1`が`app_db`に対する読み取り権限と書き込み権限を持っているとします。

`CREATE USER`使用してユーザーを作成します。

```sql
CREATE USER 'dev1'@'localhost' IDENTIFIED BY 'dev1pass';
CREATE USER 'read_user1'@'localhost' IDENTIFIED BY 'read_user1pass';
CREATE USER 'read_user2'@'localhost' IDENTIFIED BY 'read_user2pass';
CREATE USER 'rw_user1'@'localhost' IDENTIFIED BY 'rw_user1pass';
```

次に`GRANT`使用してユーザーにロールを付与します

```sql
GRANT 'app_developer' TO 'dev1'@'localhost';
GRANT 'app_read' TO 'read_user1'@'localhost', 'read_user2'@'localhost';
GRANT 'app_read', 'app_write' TO 'rw_user1'@'localhost';
```

別のユーザーにロールを付与したり、ロールを取り消したりするには、 `SUPER`権限が必要です。

ユーザーにロールを付与することは、そのロールをすぐに有効にすることを意味するわけではありません。ロールを有効にすることは別の操作です。

次の操作は「関係ループ」を形成する可能性があります。

```sql
CREATE USER 'u1', 'u2';
CREATE ROLE 'r1', 'r2';

GRANT 'u1' TO 'u1';
GRANT 'r1' TO 'r1';

GRANT 'r2' TO 'u2';
GRANT 'u2' TO 'r2';
```

TiDB はこの複数レベルの承認関係をサポートしています。これを使用して権限の継承を実装できます。

### ロールの権限を確認する {#check-a-role-s-privileges}

`SHOW GRANTS`ステートメントを使用して、ユーザーに付与されている権限を確認できます。

他のユーザーの権限関連情報を確認するには、 `mysql`データベースに対する`SELECT`権限が必要です。

```sql
SHOW GRANTS FOR 'dev1'@'localhost';
```

    +-------------------------------------------------+
    | Grants for dev1@localhost                       |
    +-------------------------------------------------+
    | GRANT USAGE ON *.* TO `dev1`@`localhost`        |
    | GRANT `app_developer`@`%` TO `dev1`@`localhost` |
    +-------------------------------------------------+

`SHOW GRANTS`の`USING`オプションを使用して、ロールの権限を確認できます。

```sql
SHOW GRANTS FOR 'dev1'@'localhost' USING 'app_developer';
```

```sql
+----------------------------------------------------------+
| Grants for dev1@localhost                                |
+----------------------------------------------------------+
| GRANT USAGE ON *.* TO `dev1`@`localhost`                 |
| GRANT ALL PRIVILEGES ON `app_db`.* TO `dev1`@`localhost` |
| GRANT `app_developer`@`%` TO `dev1`@`localhost`          |
+----------------------------------------------------------+
```

```sql
SHOW GRANTS FOR 'rw_user1'@'localhost' USING 'app_read', 'app_write';
```

    +------------------------------------------------------------------------------+
    | Grants for rw_user1@localhost                                                |
    +------------------------------------------------------------------------------+
    | GRANT USAGE ON *.* TO `rw_user1`@`localhost`                                 |
    | GRANT SELECT, INSERT, UPDATE, DELETE ON `app_db`.* TO `rw_user1`@`localhost` |
    | GRANT `app_read`@`%`,`app_write`@`%` TO `rw_user1`@`localhost`               |
    +------------------------------------------------------------------------------+

```sql
SHOW GRANTS FOR 'read_user1'@'localhost' USING 'app_read';
```

    +--------------------------------------------------------+
    | Grants for read_user1@localhost                        |
    +--------------------------------------------------------+
    | GRANT USAGE ON *.* TO `read_user1`@`localhost`         |
    | GRANT SELECT ON `app_db`.* TO `read_user1`@`localhost` |
    | GRANT `app_read`@`%` TO `read_user1`@`localhost`       |
    +--------------------------------------------------------+

現在のユーザーの権限を確認するには、 `SHOW GRANTS`または`SHOW GRANTS FOR CURRENT_USER()`使用します。5 と`SHOW GRANTS` `SHOW GRANTS FOR CURRENT_USER()`次の点で異なります。

-   `SHOW GRANTS` 、現在のユーザーに対して有効なロールの権限を示します。
-   `SHOW GRANTS FOR CURRENT_USER()`有効なロールの権限を表示しません。

### デフォルトロールを設定する {#set-the-default-role}

ロールがユーザーに付与されても、すぐには有効になりません。ユーザーがこのロールを有効にした後にのみ、ロールが所有する権限を使用できます。

ユーザーにデフォルトのロールを設定できます。ユーザーがログインすると、デフォルトのロールが自動的に有効になります。

```sql
SET DEFAULT ROLE
    {NONE | ALL | role [, role ] ...}
    TO user [, user ]
```

たとえば、次のステートメントを使用して、デフォルトのロール`rw_user1@localhost` ～ `app_read`および`app_write`設定できます。

```sql
SET DEFAULT ROLE app_read, app_write TO 'rw_user1'@'localhost';
```

次のステートメントを使用して、すべてのロールにデフォルトのロール`dev1@localhost`を設定できます。

```sql
SET DEFAULT ROLE ALL TO 'dev1'@'localhost';
```

次のステートメントを使用して、 `dev1@localhost`のすべてのデフォルト ロールを無効にすることができます。

```sql
SET DEFAULT ROLE NONE TO 'dev1'@'localhost';
```

> **注記：**
>
> このロールにデフォルト ロールを設定する前に、ユーザーにロールを付与する必要があります。

### 現在のセッションでロールを有効にする {#enable-a-role-in-the-current-session}

現在のセッションでいくつかのロールを有効にすることができます。

```sql
SET ROLE {
    DEFAULT
  | NONE
  | ALL
  | ALL EXCEPT role [, role ] ...
  | role [, role ] ...
}
```

たとえば、 `rw_user1`ログインした後、次のステートメントを使用して、現在のセッションでのみ有効なロール`app_read`と`app_write`有効にできます。

```sql
SET ROLE 'app_read', 'app_write';
```

現在のユーザーのデフォルト ロールを有効にするには、次のステートメントを使用できます。

```sql
SET ROLE DEFAULT
```

次のステートメントを使用して、現在のユーザーに付与されているすべてのロールを有効にすることができます。

```sql
SET ROLE ALL
```

すべてのロールを無効にするには、次のステートメントを使用できます。

```sql
SET ROLE NONE
```

`app_read`以外のロールを有効にするには、次のステートメントを使用できます。

```sql
SET ROLE ALL EXCEPT 'app_read'
```

> **注記：**
>
> `SET ROLE`使用してロールを有効にすると、このロールは現在のセッションでのみ有効になります。

### 現在有効なロールを確認する {#check-the-current-enabled-role}

現在のユーザーは、 `CURRENT_ROLE()`関数を使用して、現在のユーザーによって有効になっているロールを確認できます。

たとえば、 `rw_user1'@'localhost`にデフォルトのロールを付与できます。

```sql
SET DEFAULT ROLE ALL TO 'rw_user1'@'localhost';
```

`rw_user1@localhost`ログインしたら、次のステートメントを実行できます。

```sql
SELECT CURRENT_ROLE();
```

    +--------------------------------+
    | CURRENT_ROLE()                 |
    +--------------------------------+
    | `app_read`@`%`,`app_write`@`%` |
    +--------------------------------+

```sql
SET ROLE 'app_read'; SELECT CURRENT_ROLE();
```

    +----------------+
    | CURRENT_ROLE() |
    +----------------+
    | `app_read`@`%` |
    +----------------+

### 役割を取り消す {#revoke-a-role}

次のステートメントを使用して、ユーザー`read_user1@localhost`と`read_user2@localhost`に付与された`app_read`ロールを取り消すことができます。

```sql
REVOKE 'app_read' FROM 'read_user1'@'localhost', 'read_user2'@'localhost';
```

次のステートメントを使用して、 `rw_user1@localhost`ユーザーに付与されたロール`app_read`と`app_write`取り消すことができます。

```sql
REVOKE 'app_read', 'app_write' FROM 'rw_user1'@'localhost';
```

ユーザーからロールを取り消す操作はアトミックです。ロールの取り消しに失敗した場合、この操作はロールバックされます。

### 権限を取り消す {#revoke-a-privilege}

`REVOKE`ステートメントは`GRANT`の逆です。 `REVOKE`使用して`app_write`の権限を取り消すことができます。

```sql
REVOKE INSERT, UPDATE, DELETE ON app_db.* FROM 'app_write';
```

詳細は[TiDB権限管理](/privilege-management.md)参照。

### 役割を削除する {#delete-a-role}

次のステートメントを使用して、ロール`app_read`と`app_write`削除できます。

```sql
DROP ROLE 'app_read', 'app_write';
```

この操作により、 `mysql.user`テーブルの`app_read`と`app_write`のロール レコードと承認テーブル内の関連レコードが削除され、2 つのロールに関連する承認が終了します。

ロールを削除するには、権限`DROP ROLE`または`DROP USER`必要です。

### 承認テーブル {#authorization-table}

4 つのシステム[権限テーブル](/privilege-management.md#privilege-table)に加えて、RBAC システムでは 2 つの新しいシステム権限テーブルが導入されています。

-   `mysql.role_edges` : ロールとユーザーの承認関係を記録します。
-   `mysql.default_roles` : 各ユーザーのデフォルトのロールを記録します。

#### <code>mysql.role_edges</code> {#code-mysql-role-edges-code}

`mysql.role_edges`には次のデータが含まれます。

```sql
SELECT * FROM mysql.role_edges;
```

    +-----------+-----------+---------+---------+-------------------+
    | FROM_HOST | FROM_USER | TO_HOST | TO_USER | WITH_ADMIN_OPTION |
    +-----------+-----------+---------+---------+-------------------+
    | %         | r_1       | %       | u_1     | N                 |
    +-----------+-----------+---------+---------+-------------------+
    1 row in set (0.00 sec)

-   `FROM_HOST`と`FROM_USER`それぞれロールのホスト名とユーザー名を示します。
-   `TO_HOST`と`TO_USER`ロールが付与されるユーザーのホスト名とユーザー名を示します。

#### <code>mysql.default_roles</code> {#code-mysql-default-roles-code}

`mysql.default_roles` 、各ユーザーに対してデフォルトで有効になっているロールを示します。

```sql
SELECT * FROM mysql.default_roles;
```

    +------+------+-------------------+-------------------+
    | HOST | USER | DEFAULT_ROLE_HOST | DEFAULT_ROLE_USER |
    +------+------+-------------------+-------------------+
    | %    | u_1  | %                 | r_1               |
    | %    | u_1  | %                 | r_2               |
    +------+------+-------------------+-------------------+
    2 rows in set (0.00 sec)

-   `HOST`と`USER`それぞれユーザーのホスト名とユーザー名を示します。
-   `DEFAULT_ROLE_HOST`と`DEFAULT_ROLE_USER` 、それぞれデフォルト ロールのホスト名とユーザー名を示します。

### 参考文献 {#references}

RBAC、ユーザー管理、権限管理は密接に関連しているため、操作の詳細については次のリソースを参照してください。

-   [TiDB権限管理](/privilege-management.md)
-   [TiDB ユーザーアカウント管理](/user-account-management.md)
