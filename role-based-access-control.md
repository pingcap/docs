---
title: Role-Based Access Control
summary: This document introduces TiDB RBAC operations and implementation.
---

# ロールベースのアクセス制御 {#role-based-access-control}

TiDBの役割ベースのアクセス制御（RBAC）システムの実装は、MySQL8.0の実装と似ています。 TiDBは、MySQLのほとんどのRBAC構文と互換性があります。

このドキュメントでは、TiDB RBAC 関連の操作と実装について紹介します。

## RBAC操作 {#rbac-operations}

ロールは、一連の特権のコレクションです。次の操作を実行できます。

-   役割を作成します。
-   役割を削除します。
-   ロールに特権を付与します。
-   別のユーザーに役割を付与します。そのユーザーは、ロールを有効にした後、ロールに関連する特権を取得できます。

### 役割を作成する {#create-a-role}

たとえば、次のステートメントを使用して、ロール`app_developer` 、および`app_read`を作成でき`app_write` 。

{{< copyable "" >}}

```sql
CREATE ROLE 'app_developer', 'app_read', 'app_write';
```

ロールの命名形式とルールについては、 [TiDBユーザーアカウント管理](/user-account-management.md)を参照してください。

ロールは`mysql.user`テーブルに格納され、ロール名のホスト名部分（省略されている場合）のデフォルトは`'%'`です。作成しようとしているロールの名前は一意である必要があります。それ以外の場合は、エラーが報告されます。

役割を作成するには、 `CREATE ROLE`つまたは`CREATE USER`の特権が必要です。

### 役割に特権を付与する {#grant-a-privilege-to-a-role}

ロールに特権を付与する操作は、ユーザーに特権を付与する操作と同じです。詳細については、 [TiDB権限管理](/privilege-management.md)を参照してください。

たとえば、次のステートメントを使用して、 `app_read`のロールに`app_db`のデータベースを読み取る特権を付与できます。

{{< copyable "" >}}

```sql
GRANT SELECT ON app_db.* TO 'app_read'@'%';
```

次のステートメントを使用して、 `app_write`のロールに`app_db`のデータベースにデータを書き込む特権を付与できます。

{{< copyable "" >}}

```sql
GRANT INSERT, UPDATE, DELETE ON app_db.* TO 'app_write'@'%';;
```

次のステートメントを使用して、 `app_developer`のロールに`app_db`のデータベースに対するすべての権限を付与できます。

{{< copyable "" >}}

```sql
GRANT ALL ON app_db.* TO 'app_developer';
```

### ユーザーに役割を付与する {#grant-a-role-to-a-user}

ユーザー`dev1`が`app_db`のすべての特権を持つ開発者ロールを持っていると仮定します。 2人のユーザー`read_user1`と`read_user2`は、 `app_db`に対する読み取り専用特権を持っています。そして、ユーザ`rw_user1`は、 `app_db`に対する読み取りおよび書き込み特権を有する。

`CREATE USER`を使用してユーザーを作成します。

{{< copyable "" >}}

```sql
CREATE USER 'dev1'@'localhost' IDENTIFIED BY 'dev1pass';
CREATE USER 'read_user1'@'localhost' IDENTIFIED BY 'read_user1pass';
CREATE USER 'read_user2'@'localhost' IDENTIFIED BY 'read_user2pass';
CREATE USER 'rw_user1'@'localhost' IDENTIFIED BY 'rw_user1pass';
```

次に、 `GRANT`を使用してユーザーに役割を付与します

```sql
GRANT 'app_developer' TO 'dev1'@'localhost';
GRANT 'app_read' TO 'read_user1'@'localhost', 'read_user2'@'localhost';
GRANT 'app_read', 'app_write' TO 'rw_user1'@'localhost';
```

別のユーザーに役割を付与したり、役割を取り消したりするには、 `SUPER`の特権が必要です。

ユーザーに役割を付与することは、その役割をすぐに有効にすることを意味するわけではありません。ロールの有効化は別の操作です。

次の操作は「関係ループ」を形成する可能性があります。

```sql
CREATE USER 'u1', 'u2';
CREATE ROLE 'r1', 'r2';

GRANT 'u1' TO 'u1';
GRANT 'r1' TO 'r1';

GRANT 'r2' TO 'u2';
GRANT 'u2' TO 'r2';
```

TiDBは、このマルチレベルの承認関係をサポートしています。これを使用して、特権の継承を実装できます。

### ロールの権限を確認してください {#check-a-role-s-privileges}

`SHOW GRANTS`ステートメントを使用して、ユーザーに付与されている特権を確認できます。

別のユーザーの特権関連情報を確認するには、 `mysql`のデータベースで`SELECT`の特権が必要です。

{{< copyable "" >}}

```sql
SHOW GRANTS FOR 'dev1'@'localhost';
```

```
+-------------------------------------------------+
| Grants for dev1@localhost                       |
+-------------------------------------------------+
| GRANT USAGE ON *.* TO `dev1`@`localhost`        |
| GRANT `app_developer`@`%` TO `dev1`@`localhost` |
+-------------------------------------------------+
```

`SHOW GRANTS`のうち`USING`のオプションを使用して、役割の特権を確認できます。

{{< copyable "" >}}

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

{{< copyable "" >}}

```sql
SHOW GRANTS FOR 'rw_user1'@'localhost' USING 'app_read', 'app_write';
```

```
+------------------------------------------------------------------------------+
| Grants for rw_user1@localhost                                                |
+------------------------------------------------------------------------------+
| GRANT USAGE ON *.* TO `rw_user1`@`localhost`                                 |
| GRANT SELECT, INSERT, UPDATE, DELETE ON `app_db`.* TO `rw_user1`@`localhost` |
| GRANT `app_read`@`%`,`app_write`@`%` TO `rw_user1`@`localhost`               |
+------------------------------------------------------------------------------+
```

{{< copyable "" >}}

```sql
SHOW GRANTS FOR 'read_user1'@'localhost' USING 'app_read';
```

```
+--------------------------------------------------------+
| Grants for read_user1@localhost                        |
+--------------------------------------------------------+
| GRANT USAGE ON *.* TO `read_user1`@`localhost`         |
| GRANT SELECT ON `app_db`.* TO `read_user1`@`localhost` |
| GRANT `app_read`@`%` TO `read_user1`@`localhost`       |
+--------------------------------------------------------+
```

`SHOW GRANTS`または`SHOW GRANTS FOR CURRENT_USER()`を使用して、現在のユーザーの特権を確認できます。 `SHOW GRANTS`と`SHOW GRANTS FOR CURRENT_USER()`は、次の点で異なります。

-   `SHOW GRANTS`は、現在のユーザーに対して有効になっているロールの特権を示します。
-   `SHOW GRANTS FOR CURRENT_USER()`は、有効な役割の特権を示しません。

### デフォルトの役割を設定する {#set-the-default-role}

ロールがユーザーに付与された後、すぐには有効になりません。ユーザーがこのロールを有効にした後でのみ、ロールが所有する特権を使用できます。

ユーザーのデフォルトの役割を設定できます。ユーザーがログインすると、デフォルトの役割が自動的に有効になります。

{{< copyable "" >}}

```sql
SET DEFAULT ROLE
    {NONE | ALL | role [, role ] ...}
    TO user [, user ]
```

たとえば、次のステートメントを使用して、デフォルトの役割を`rw_user1@localhost`から`app_read`および`app_write`に設定できます。

{{< copyable "" >}}

```sql
SET DEFAULT ROLE app_read, app_write TO 'rw_user1'@'localhost';
```

次のステートメントを使用して、デフォルトの役割`dev1@localhost`をすべての役割に設定できます。

{{< copyable "" >}}

```sql
SET DEFAULT ROLE ALL TO 'dev1'@'localhost';
```

次のステートメントを使用して、 `dev1@localhost`のすべてのデフォルトの役割を無効にすることができます。

{{< copyable "" >}}

```sql
SET DEFAULT ROLE NONE TO 'dev1'@'localhost';
```

> **ノート：**
>
> デフォルトの役割をこの役割に設定する前に、ユーザーに役割を付与する必要があります。

### 現在のセッションで役割を有効にする {#enable-a-role-in-the-current-session}

現在のセッションでいくつかの役割を有効にすることができます。

```sql
SET ROLE {
    DEFAULT
  | NONE
  | ALL
  | ALL EXCEPT role [, role ] ...
  | role [, role ] ...
}
```

たとえば、 `rw_user1`がログインした後、次のステートメントを使用して、現在のセッションでのみ有効なロール`app_read`と`app_write`を有効にすることができます。

{{< copyable "" >}}

```sql
SET ROLE 'app_read', 'app_write';
```

次のステートメントを使用して、現在のユーザーのデフォルトの役割を有効にすることができます。

{{< copyable "" >}}

```sql
SET ROLE DEFAULT
```

次のステートメントを使用して、現在のユーザーに付与されているすべてのロールを有効にすることができます。

{{< copyable "" >}}

```sql
SET ROLE ALL
```

次のステートメントを使用して、すべての役割を無効にすることができます。

{{< copyable "" >}}

```sql
SET ROLE NONE
```

次のステートメントを使用して、 `app_read`以外のロールを有効にできます。

{{< copyable "" >}}

```sql
SET ROLE ALL EXCEPT 'app_read'
```

> **ノート：**
>
> `SET ROLE`を使用してロールを有効にする場合、このロールは現在のセッションでのみ有効です。

### 現在有効な役割を確認する {#check-the-current-enabled-role}

現在のユーザーは、 `CURRENT_ROLE()`関数を使用して、現在のユーザーによって有効にされている役割を確認できます。

たとえば、デフォルトの役割を`rw_user1'@'localhost`に付与できます。

{{< copyable "" >}}

```sql
SET DEFAULT ROLE ALL TO 'rw_user1'@'localhost';
```

`rw_user1@localhost`ログイン後、次のステートメントを実行できます。

{{< copyable "" >}}

```sql
SELECT CURRENT_ROLE();
```

```
+--------------------------------+
| CURRENT_ROLE()                 |
+--------------------------------+
| `app_read`@`%`,`app_write`@`%` |
+--------------------------------+
```

{{< copyable "" >}}

```sql
SET ROLE 'app_read'; SELECT CURRENT_ROLE();
```

```
+----------------+
| CURRENT_ROLE() |
+----------------+
| `app_read`@`%` |
+----------------+
```

### 役割を取り消す {#revoke-a-role}

次のステートメントを使用して、ユーザー`read_user1@localhost`および`read_user2@localhost`に付与された`app_read`の役割を取り消すことができます。

{{< copyable "" >}}

```sql
REVOKE 'app_read' FROM 'read_user1'@'localhost', 'read_user2'@'localhost';
```

次のステートメントを使用して、 `rw_user1@localhost`のユーザーに付与されたロール`app_read`および`app_write`を取り消すことができます。

{{< copyable "" >}}

```sql
REVOKE 'app_read', 'app_write' FROM 'rw_user1'@'localhost';
```

ユーザーからロールを取り消す操作はアトミックです。ロールの取り消しに失敗した場合、この操作はロールバックされます。

### 特権を取り消す {#revoke-a-privilege}

`REVOKE`ステートメントは`GRANT`と逆になります。 `REVOKE`を使用して、 `app_write`の特権を取り消すことができます。

{{< copyable "" >}}

```sql
REVOKE INSERT, UPDATE, DELETE ON app_db.* FROM 'app_write';
```

詳細については、 [TiDB権限管理](/privilege-management.md)を参照してください。

### 役割を削除する {#delete-a-role}

次のステートメントを使用して、ロール`app_read`と`app_write`を削除できます。

{{< copyable "" >}}

```sql
DROP ROLE 'app_read', 'app_write';
```

この操作により、 `mysql.user`テーブルの`app_read`と`app_write`のロールレコードと許可テーブルの関連レコードが削除され、2つのロールに関連する許可が終了します。

ロールを削除するには、 `DROP ROLE`または`DROP USER`の権限が必要です。

### 承認テーブル {#authorization-table}

4つのシステム[特権テーブル](/privilege-management.md#privilege-table)に加えて、RBACシステムは2つの新しいシステム特権テーブルを導入します。

-   `mysql.role_edges` ：ロールとユーザーの承認関係を記録します。
-   `mysql.default_roles` ：各ユーザーのデフォルトの役割を記録します。

#### <code>mysql.role_edges</code> {#code-mysql-role-edges-code}

`mysql.role_edges`には次のデータが含まれます。

{{< copyable "" >}}

```sql
SELECT * FROM mysql.role_edges;
```

```
+-----------+-----------+---------+---------+-------------------+
| FROM_HOST | FROM_USER | TO_HOST | TO_USER | WITH_ADMIN_OPTION |
+-----------+-----------+---------+---------+-------------------+
| %         | r_1       | %       | u_1     | N                 |
+-----------+-----------+---------+---------+-------------------+
1 row in set (0.00 sec)
```

-   `FROM_HOST`と`FROM_USER`は、それぞれロールのホスト名とユーザー名を示します。
-   `TO_HOST`と`TO_USER`は、ロールが付与されているユーザーのホスト名とユーザー名を示します。

#### <code>mysql.default_roles</code> {#code-mysql-default-roles-code}

`mysql.default_roles`は、各ユーザーに対してデフォルトで有効になっている役割を示します。

{{< copyable "" >}}

```sql
SELECT * FROM mysql.default_roles;
```

```
+------+------+-------------------+-------------------+
| HOST | USER | DEFAULT_ROLE_HOST | DEFAULT_ROLE_USER |
+------+------+-------------------+-------------------+
| %    | u_1  | %                 | r_1               |
| %    | u_1  | %                 | r_2               |
+------+------+-------------------+-------------------+
2 rows in set (0.00 sec)
```

-   `HOST`と`USER`は、それぞれユーザーのホスト名とユーザー名を示します。
-   `DEFAULT_ROLE_HOST`と`DEFAULT_ROLE_USER`は、それぞれデフォルトの役割のホスト名とユーザー名を示します。

### 参考文献 {#references}

RBAC、ユーザー管理、および特権管理は密接に関連しているため、次のリソースで操作の詳細を参照できます。

-   [TiDB権限管理](/privilege-management.md)
-   [TiDBユーザーアカウント管理](/user-account-management.md)
