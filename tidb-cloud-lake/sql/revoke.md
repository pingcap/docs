---
title: REVOKE
summary: 特定のデータベースオブジェクトに対する権限、ロール、および所有権を取り消します。これには以下が含まれます。
---

# REVOKE

特定のデータベースオブジェクトに対する権限、ロール、および所有権を取り消します。これには以下が含まれます。

- ロールから権限を取り消す。
- ユーザーまたは他のロールからロールを削除する。

関連情報:

- [GRANT](/tidb-cloud-lake/sql/grant.md)
- [SHOW GRANTS](/tidb-cloud-lake/sql/show-grants.md)

> **Note:**
>
> `REVOKE` で権限またはロールを変更した後は、更新内容をすべてのクエリノードに即座に反映させるために、[SYSTEM FLUSH PRIVILEGES](/tidb-cloud-lake/sql/system-flush-privileges.md) を実行してください。

## 構文 {#syntax}

### 権限の取り消し {#revoking-privileges}

```sql
REVOKE {
        schemaObjectPrivileges | ALL [ PRIVILEGES ] ON <privileges_level>
       }
FROM ROLE <role_name>
```

以下のとおりです。

```sql
schemaObjectPrivileges ::=
-- For TABLE
  { SELECT | INSERT }

-- For SCHEMA
  { CREATE | DROP | ALTER }

-- For USER
  { CREATE USER }

-- For ROLE
  { CREATE ROLE}

-- For STAGE
  { READ, WRITE }

-- For UDF
  { USAGE }

-- For MASKING POLICY (account-level privileges)
  { CREATE MASKING POLICY | APPLY MASKING POLICY }

-- For ROW ACCESS POLICY (account-level privileges)
  { CREATE ROW ACCESS POLICY | APPLY ROW ACCESS POLICY }
```

```sql
privileges_level ::=
    *.*
  | db_name.*
  | db_name.tbl_name
  | STAGE <stage_name>
  | UDF <udf_name>
  | MASKING POLICY <policy_name>
  | ROW ACCESS POLICY <policy_name>
```

### Masking Policy 権限の取り消し {#revoking-masking-policy-privileges}

```sql
REVOKE APPLY ON MASKING POLICY <policy_name> FROM ROLE <role_name>
REVOKE ALL [ PRIVILEGES ] ON MASKING POLICY <policy_name> FROM ROLE <role_name>
REVOKE OWNERSHIP ON MASKING POLICY <policy_name> FROM ROLE '<role_name>'
```

これらの形式を使用すると、個別の masking policy へのアクセスを削除できます。グローバルな `CREATE MASKING POLICY` および `APPLY MASKING POLICY` 権限は、`ON *.*` を使用した標準構文で取り消します。

### Row Access Policy 権限の取り消し {#revoking-row-access-policy-privileges}

```sql
REVOKE APPLY ON ROW ACCESS POLICY <policy_name> FROM ROLE <role_name>
REVOKE ALL [ PRIVILEGES ] ON ROW ACCESS POLICY <policy_name> FROM ROLE <role_name>
REVOKE OWNERSHIP ON ROW ACCESS POLICY <policy_name> FROM ROLE '<role_name>'
```

これらの形式を使用すると、特定の row access policy へのアクセスを取り消せます。グローバルな `CREATE ROW ACCESS POLICY` および `APPLY ROW ACCESS POLICY` 権限は、`ON *.*` に対する標準構文で取り消します。

### ロールの取り消し {#revoking-role}

```sql
-- Revoke a role from a user
REVOKE ROLE <role_name> FROM <user_name>

-- Revoke a role from a role
REVOKE ROLE <role_name> FROM ROLE <role_name>
```

## 例 {#examples}

### 例 1: ロールから権限を取り消す {#example-1-revoking-privileges-from-a-role}

ロールを作成します。

```sql
CREATE ROLE user1_role;
```

`default` データベース内の既存のすべてのテーブルに対する `SELECT,INSERT` 権限を、ロール `user1_role` に付与します。

```sql
GRANT SELECT,INSERT ON default.* TO ROLE user1_role;
```

```sql
SHOW GRANTS FOR ROLE user1_role;
+---------------------------------------------------------+
| Grants                                                  |
+---------------------------------------------------------+
| GRANT SELECT,INSERT ON 'default'.* TO ROLE 'user1_role' |
+---------------------------------------------------------+
```

ロール `user1_role` から `INSERT` 権限を取り消します。

```sql
REVOKE INSERT ON default.* FROM ROLE user1_role;
```

```sql
SHOW GRANTS FOR ROLE user1_role;
+---------------------------------------------------+
| Grants                                            |
+---------------------------------------------------+
| GRANT SELECT ON 'default'.* TO 'user1_role'       |
+---------------------------------------------------+
```

### 例 2: 別のロールから権限を取り消す {#example-2-revoking-privileges-from-another-role}

`mydb` データベース内の既存のすべてのテーブルに対する `SELECT,INSERT` 権限を、ロール `role1` に付与します。

ロールを作成します。

```sql
CREATE ROLE role1;
```

ロールに権限を付与します。

```sql
GRANT SELECT,INSERT ON mydb.* TO ROLE role1;
```

ロールの付与内容を表示します。

```sql
SHOW GRANTS FOR ROLE role1;
+--------------------------------------------+
| Grants                                     |
+--------------------------------------------+
| GRANT SELECT,INSERT ON 'mydb'.* TO 'role1' |
+--------------------------------------------+
```

ロール `role1` から `INSERT` 権限を取り消します。

```sql
REVOKE INSERT ON mydb.* FROM ROLE role1;
```

```sql
SHOW GRANTS FOR ROLE role1;
+-------------------------------------+
| Grants                              |
+-------------------------------------+
| GRANT SELECT ON 'mydb'.* TO 'role1' |
+-------------------------------------+
```

### 例 3: ユーザーからロールを取り消す {#example-3-revoking-a-role-from-a-user}

```sql
REVOKE ROLE role1 FROM USER user1;
```

```sql
SHOW GRANTS FOR user1;
```

> **Tip:**
>
> revoke の後でも、なぜ `default_role` は引き続き表示されるのでしょうか？
>
> `default_role` は grant ではなく、ユーザーのプロパティです。`REVOKE` はロールのメンバーシップを削除しますが、`default_role` はリセットしません。以下はその例です。
>
> ```sql
> CREATE ROLE analyst;
> CREATE USER bob IDENTIFIED BY 'password123' WITH DEFAULT_ROLE = 'analyst';
> GRANT ROLE analyst TO bob;
>
> DESC USER bob;
> +------+----------+----------------------+--------------+---------+
> | name | hostname | auth_type            | default_role | roles   |
> +------+----------+----------------------+--------------+---------+
> | bob  | %        | double_sha1_password | analyst      | analyst |
> +------+----------+----------------------+--------------+---------+
>
> REVOKE ROLE analyst FROM bob;
>
> DESC USER bob;
> +------+----------+----------------------+--------------+-------+
> | name | hostname | auth_type            | default_role | roles |
> +------+----------+----------------------+--------------+-------+
> | bob  | %        | double_sha1_password | analyst      |       |
> +------+----------+----------------------+--------------+-------+
> ```
>
> `roles` は空になっていますが、`default_role` はそのまま残っていることに注目してください。ユーザーはもはや `analyst` の権限を持っていません。これを整理するには、`ALTER USER bob WITH DEFAULT_ROLE = 'public'` を実行します。

### 例 4: Masking Policy 権限を取り消す {#example-4-revoking-masking-policy-privileges}

```sql
-- Remove per-policy access from a role
REVOKE APPLY ON MASKING POLICY email_mask FROM ROLE pii_readers;

-- Revoke the ability to create masking policies at the account level
REVOKE CREATE MASKING POLICY ON *.* FROM ROLE security_admin;
```

### 例 5: Row Access Policy 権限を取り消す {#example-5-revoking-row-access-policy-privileges}

```sql
-- Remove per-policy access from a role
REVOKE APPLY ON ROW ACCESS POLICY rap_region FROM ROLE apac_only;

-- Revoke the ability to create row access policies globally
REVOKE CREATE ROW ACCESS POLICY ON *.* FROM ROLE row_policy_admin;
```