---
title: Role-Based Access Control
summary: This document introduces TiDB RBAC operations and implementation.
---

# 役割ベースのアクセス制御 {#role-based-access-control}

TiDB の役割ベースのアクセス制御 (RBAC) システムの実装は、MySQL 8.0 の実装と似ています。 TiDB は、MySQL のほとんどの RBAC 構文と互換性があります。

このドキュメントでは、TiDB RBAC 関連の操作と実装について紹介します。

## RBAC 操作 {#rbac-operations}

ロールは、一連の権限の集合です。次の操作を実行できます。

-   ロールを作成します。
-   役割を削除します。
-   ロールに権限を付与します。
-   別のユーザーに役割を付与します。そのユーザーは、ロールを有効にした後、ロールに関連する権限を取得できます。

### 役割を作成する {#create-a-role}

たとえば、次のステートメントを使用して、ロール`app_developer` 、 `app_read` 、および`app_write`を作成できます。

{{< copyable "" >}}

```sql
CREATE ROLE 'app_developer', 'app_read', 'app_write';
```

役割の命名形式と規則については、 [TiDB ユーザー アカウント管理](/user-account-management.md)を参照してください。

ロールは`mysql.user`テーブルに格納され、ロール名のホスト名部分 (省略された場合) はデフォルトで`'%'`になります。作成しようとしているロールの名前は一意である必要があります。そうでない場合、エラーが報告されます。

ロールを作成するには、 `CREATE ROLE`または`CREATE USER`権限が必要です。

### ロールに権限を付与する {#grant-a-privilege-to-a-role}

ロールに権限を付与する操作は、ユーザーに権限を付与する操作と同じです。詳細については、 [TiDB権限管理](/privilege-management.md)を参照してください。

たとえば、次のステートメントを使用して、 `app_read`ロールに`app_db`データベースを読み取る権限を付与できます。

{{< copyable "" >}}

```sql
GRANT SELECT ON app_db.* TO 'app_read'@'%';
```

次のステートメントを使用して、 `app_write`ロールに`app_db`データベースにデータを書き込む権限を付与できます。

{{< copyable "" >}}

```sql
GRANT INSERT, UPDATE, DELETE ON app_db.* TO 'app_write'@'%';
```

次のステートメントを使用して、 `app_developer`ロールに`app_db`データベースに対するすべての権限を付与できます。

{{< copyable "" >}}

```sql
GRANT ALL ON app_db.* TO 'app_developer';
```

### ユーザーにロールを付与する {#grant-a-role-to-a-user}

ユーザー`dev1`が、 `app_db`に対するすべての権限を持つ開発者ロールを持っているとします。 2 人のユーザー`read_user1`と`read_user2` `app_db`に対する読み取り専用権限を持っています。また、ユーザー`rw_user1`は`app_db`に対する読み取り権限と書き込み権限を持っています。

`CREATE USER`を使用してユーザーを作成します。

{{< copyable "" >}}

```sql
CREATE USER 'dev1'@'localhost' IDENTIFIED BY 'dev1pass';
CREATE USER 'read_user1'@'localhost' IDENTIFIED BY 'read_user1pass';
CREATE USER 'read_user2'@'localhost' IDENTIFIED BY 'read_user2pass';
CREATE USER 'rw_user1'@'localhost' IDENTIFIED BY 'rw_user1pass';
```

次に、 `GRANT`使用してユーザーにロールを付与します

```sql
GRANT 'app_developer' TO 'dev1'@'localhost';
GRANT 'app_read' TO 'read_user1'@'localhost', 'read_user2'@'localhost';
GRANT 'app_read', 'app_write' TO 'rw_user1'@'localhost';
```

別のユーザーにロールを付与したり、ロールを取り消したりするには、 `SUPER`特権が必要です。

ユーザーにロールを付与しても、そのロールがすぐに有効になるわけではありません。役割の有効化は別の操作です。

次の操作は、「リレーション ループ」を形成する可能性があります。

```sql
CREATE USER 'u1', 'u2';
CREATE ROLE 'r1', 'r2';

GRANT 'u1' TO 'u1';
GRANT 'r1' TO 'r1';

GRANT 'r2' TO 'u2';
GRANT 'u2' TO 'r2';
```

TiDB は、このマルチレベルの認証関係をサポートしています。これを使用して、特権の継承を実装できます。

### 役割の権限を確認する {#check-a-role-s-privileges}

`SHOW GRANTS`ステートメントを使用して、ユーザーに付与されている権限を確認できます。

別のユーザーの権限関連情報を確認するには、 `mysql`データベースに対する`SELECT`権限が必要です。

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

`SHOW GRANTS`の`USING`オプションを使用して、ロールの権限を確認できます。

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

`SHOW GRANTS`または`SHOW GRANTS FOR CURRENT_USER()`を使用して、現在のユーザーの権限を確認できます。 `SHOW GRANTS`と`SHOW GRANTS FOR CURRENT_USER()` 、次の点で異なります。

-   `SHOW GRANTS`現在のユーザーの有効なロールの特権を示します。
-   `SHOW GRANTS FOR CURRENT_USER()`は、有効な役割の特権を示しません。

### デフォルトの役割を設定する {#set-the-default-role}

ロールがユーザーに付与された後、すぐには有効になりません。ユーザーがこのロールを有効にした後でのみ、ロールが所有する権限を使用できます。

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

次のステートメントを使用して、デフォルトのロール`dev1@localhost`をすべてのロールに設定できます。

{{< copyable "" >}}

```sql
SET DEFAULT ROLE ALL TO 'dev1'@'localhost';
```

次のステートメントを使用して、 `dev1@localhost`のすべてのデフォルト ロールを無効にすることができます。

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

たとえば、 `rw_user1`ログインした後、次のステートメントを使用して、現在のセッションでのみ有効なロール`app_read`と`app_write`を有効にできます。

{{< copyable "" >}}

```sql
SET ROLE 'app_read', 'app_write';
```

次のステートメントを使用して、現在のユーザーのデフォルト ロールを有効にすることができます。

{{< copyable "" >}}

```sql
SET ROLE DEFAULT
```

次のステートメントを使用して、現在のユーザーに付与されたすべてのロールを有効にできます。

{{< copyable "" >}}

```sql
SET ROLE ALL
```

次のステートメントを使用して、すべてのロールを無効にすることができます。

{{< copyable "" >}}

```sql
SET ROLE NONE
```

次のステートメントを使用して、 `app_read`以外のロールを有効にすることができます。

{{< copyable "" >}}

```sql
SET ROLE ALL EXCEPT 'app_read'
```

> **ノート：**
>
> `SET ROLE`を使用してロールを有効にすると、このロールは現在のセッションでのみ有効になります。

### 現在有効になっているロールを確認する {#check-the-current-enabled-role}

現在のユーザーは、 `CURRENT_ROLE()`関数を使用して、現在のユーザーによってどのロールが有効になっているかを確認できます。

たとえば、デフォルトのロールを`rw_user1'@'localhost`に付与できます。

{{< copyable "" >}}

```sql
SET DEFAULT ROLE ALL TO 'rw_user1'@'localhost';
```

`rw_user1@localhost`がログインした後、次のステートメントを実行できます。

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

次のステートメントを使用して、ユーザー`read_user1@localhost`および`read_user2@localhost`に付与された`app_read`ロールを取り消すことができます。

{{< copyable "" >}}

```sql
REVOKE 'app_read' FROM 'read_user1'@'localhost', 'read_user2'@'localhost';
```

次のステートメントを使用して、ユーザー`rw_user1@localhost`に付与されたロール`app_read`と`app_write`を取り消すことができます。

{{< copyable "" >}}

```sql
REVOKE 'app_read', 'app_write' FROM 'rw_user1'@'localhost';
```

ユーザーからロールを取り消す操作はアトミックです。ロールの取り消しに失敗した場合、この操作はロールバックされます。

### 特権を取り消す {#revoke-a-privilege}

`REVOKE`ステートメントは`GRANT`の逆です。 `REVOKE`使用して`app_write`の権限を取り消すことができます。

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

この操作により、 `mysql.user`テーブルの`app_read`と`app_write`のロール レコードと、権限テーブルの関連レコードが削除され、2 つのロールに関連する権限が終了します。

ロールを削除するには、 `DROP ROLE`または`DROP USER`権限が必要です。

### 認可表 {#authorization-table}

4 つのシステム[特権テーブル](/privilege-management.md#privilege-table)に加えて、RBAC システムには 2 つの新しいシステム特権テーブルが導入されています。

-   `mysql.role_edges` : ロールとユーザーの認可関係を記録します。
-   `mysql.default_roles` : 各ユーザーのデフォルトの役割を記録します。

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

-   `FROM_HOST`と`FROM_USER` 、それぞれ役割のホスト名とユーザー名を示します。
-   `TO_HOST`と`TO_USER` 、ロールが付与されたユーザーのホスト名とユーザー名を示します。

#### <code>mysql.default_roles</code> {#code-mysql-default-roles-code}

`mysql.default_roles`各ユーザーに対してデフォルトで有効になっているロールを示します。

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

-   `HOST`と`USER` 、それぞれユーザーのホスト名とユーザー名を示します。
-   `DEFAULT_ROLE_HOST`と`DEFAULT_ROLE_USER` 、それぞれデフォルト ロールのホスト名とユーザー名を示します。

### 参考文献 {#references}

RBAC、ユーザー管理、および権限管理は密接に関連しているため、次のリソースで操作の詳細を参照できます。

-   [TiDB権限管理](/privilege-management.md)
-   [TiDB ユーザー アカウント管理](/user-account-management.md)
