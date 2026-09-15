---
title: 所有权
summary: 所有权是一种特殊的权限，表示某个角色在 {{{ .lake }}} 中对特定数据对象（当前包括数据库、表、UDF 和 stage）所拥有的专属权利和责任。
---

# 所有权

所有权是一种特殊的权限，表示某个角色在 {{{ .lake }}} 中对特定数据对象（当前包括数据库、表、UDF 和 stage）所拥有的专属权利和责任。

## 授予所有权 {#granting-ownership}

对象的所有权会自动授予创建该对象的用户所属角色，并且可以使用 [GRANT](/tidb-cloud-lake/sql/grant.md) 命令在角色之间转移：

- 将对象的所有权授予新角色时，会把完整所有权转移给新角色，并从原角色中移除该所有权。例如，如果角色 A 最初拥有某个表，而你将所有权授予角色 B，则角色 B 会成为新的所有者，角色 A 将不再拥有该表的所有权。
- 出于安全原因，不建议将所有权授予内置角色 `public`。如果用户在创建对象时属于 `public` 角色，那么所有用户都将拥有该对象的所有权，因为每个用户默认都具有 `public` 角色。{{{ .lake }}} 建议创建并为用户分配自定义角色，而不是使用 `public` 角色，以便更清晰地管理所有权。有关内置角色的信息，请参见[内置角色](/tidb-cloud-lake/guides/roles.md)。
- `default` 数据库中的表不能授予所有权，因为它由内置角色 `account_admin` 拥有。

## 不允许撤销所有权 {#revoking-ownership-not-allowed}

不支持撤销所有权，因为每个对象都必须有一个所有者。

- 如果对象被删除，它不会保留原角色的所有权。如果该对象被恢复（如果可能），所有权也不会自动重新分配，此时需要由 `account_admin` 手动将所有权重新分配给某个角色。
- 如果拥有某个对象的角色被删除，`account_admin` 可以将该对象的所有权转移给另一个角色。

## 示例 {#examples}

要将所有权授予某个角色，请使用 [GRANT](/tidb-cloud-lake/sql/grant.md) 命令。以下示例演示了如何将不同数据库对象的所有权授予角色 'data_owner'：

```sql
-- Grant ownership of all tables in the 'finance_data' database to the role 'data_owner'
GRANT OWNERSHIP ON finance_data.* TO ROLE 'data_owner';

-- Grant ownership of the table 'transactions' in the 'finance_data' schema to the role 'data_owner'
GRANT OWNERSHIP ON finance_data.transactions TO ROLE 'data_owner';

-- Grant ownership of the stage 'ingestion_stage' to the role 'data_owner'
GRANT OWNERSHIP ON STAGE ingestion_stage TO ROLE 'data_owner';

-- Grant ownership of the user-defined function 'calculate_profit' to the role 'data_owner'
GRANT OWNERSHIP ON UDF calculate_profit TO ROLE 'data_owner';
```

以下示例演示了如何在 {{{ .lake }}} 中建立基于角色的所有权。管理员创建角色 'role1' 并将其分配给用户 'u1'。随后，将在 'db' schema 中创建表的权限授予 'role1'。因此，当 'u1' 登录后，他们将拥有 'role1' 的权限，从而可以在 'db' 下创建并拥有表。但是，对不属于 'role1' 所有的表的访问会受到限制，这一点可以从对 'db.t_old_exists' 的查询失败中看出。

```sql
-- Admin creates roles and assigns roles to corresponding users
CREATE ROLE role1;
CREATE USER u1 IDENTIFIED BY '123' WITH DEFAULT ROLE 'role1';
GRANT CREATE ON db.* TO ROLE role1;
GRANT ROLE role1 TO u1;

-- After u1 logs into {{{ .lake }}}, role1 has been granted to u1, so u1 can create and own tables under db:
u1> CREATE TABLE db.t(id INT);
u1> INSERT INTO db.t VALUES(1);
u1> SELECT * FROM db.t;
u1> SELECT * FROM db.t_old_exists; -- Failed because the owner of this table is not role1
```

以下示例展示了如何让用户创建仅由其角色拥有的数据库，这样其他用户除非被显式授予访问权限，否则无法看到这些数据库：

```sql
CREATE ROLE part1_role;
GRANT CREATE DATABASE ON *.* TO ROLE part1_role;
CREATE USER user1 IDENTIFIED BY 'abc123' WITH DEFAULT ROLE 'part1_role';
GRANT ROLE part1_role TO user1;

-- When user1 creates a database, ownership is assigned to part1_role.
-- Other users will not be able to see or access that database unless
-- privileges or ownership are granted to their roles.
```