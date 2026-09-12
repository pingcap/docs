---
title: 角色
summary: {{{ .lake }}} 中的角色在简化权限管理方面发挥着关键作用。当多个用户需要相同的一组权限时，逐个授予权限会很繁琐。角色通过将一组权限分配给某个角色来提供解决方案，然后可以轻松地将该角色分配给多个用户。
---

# 角色

{{{ .lake }}} 中的角色在简化权限管理方面发挥着关键作用。当多个用户需要相同的一组权限时，逐个授予权限会很繁琐。角色通过将一组权限分配给某个角色来提供解决方案，然后可以轻松地将该角色分配给多个用户。

![Alt text](/media/tidb-cloud-lake/access-control-3.png)

## 继承角色并建立层级关系 {#inheriting-roles-establishing-hierarchy}

角色授予允许一个角色继承另一个角色的权限和职责。这有助于创建一种灵活的层级结构，类似于组织架构，其中存在两个[内置角色](#built-in-roles)：最高的是 `account-admin`，最低的是 `public`。

假设创建了三个角色：*manager*、*engineer* 和 *intern*。在这个示例中，*intern* 角色被授予给 *engineer* 角色。因此，*engineer* 不仅拥有自身的一组权限，还会继承与 *intern* 角色相关的权限。进一步扩展这一层级关系，如果将 *engineer* 角色授予给 *manager*，那么 *manager* 现在将同时获得 *engineer* 和 *intern* 角色所固有的权限。

![Alt text](/media/tidb-cloud-lake/access-control-4.png)

## 内置角色 {#built-in-roles}

{{{ .lake }}} 提供以下内置角色：

| 内置角色 | 描述                                                                                                                            |
|---------------|----------------------------------------------------------------------------------------------------------------------------------------|
| account-admin | 拥有所有权限，作为所有其他角色的父角色，并支持在租户内无缝切换到任意角色。 |
| public        | 不继承任何权限，将所有角色视为其父角色，并允许任何角色切换到 public 角色。                    |

要在 {{{ .lake }}} 中将 `account-admin` 角色分配给用户，请在邀请用户时选择该角色。你也可以在用户加入后再将该角色分配给他们。如果你使用的是 {{{ .lake }}} Community Edition 或 Enterprise Edition，请先在部署期间配置一个 `account-admin` 用户，然后根据需要将该角色分配给其他用户。

## 设置默认角色 {#setting-default-role}

当一个用户被授予多个角色时，你可以使用 [CREATE USER](/tidb-cloud-lake/sql/create-user.md) 或 [ALTER USER](/tidb-cloud-lake/sql/alter-user.md) 命令为该用户设置默认角色。默认角色决定了在会话开始时自动分配给用户的角色：

```sql title='Example:'
-- Show existing roles in the system
SHOW ROLES;

┌───────────────────────────────────────────────────────────┐
│      name     │ inherited_roles │ is_current │ is_default │
├───────────────┼─────────────────┼────────────┼────────────┤
│ account_admin │               0 │ true       │ true       │
│ public        │               0 │ false      │ false      │
│ writer        │               0 │ false      │ false      │
└───────────────────────────────────────────────────────────┘

-- Create a user 'eric' with the password 'abc123' and set 'writer' as the default role
CREATE USER eric IDENTIFIED BY 'abc123' WITH DEFAULT_ROLE = 'writer';

-- Grant the 'account_admin' role to the user 'eric'
GRANT ROLE account_admin TO eric;

-- Set 'account_admin' as the default role for user 'eric'
ALTER USER eric WITH DEFAULT_ROLE = 'account_admin';
```

- 用户可以在会话中使用 [SET ROLE](/tidb-cloud-lake/sql/set-role.md) 命令灵活切换到其他角色。
- 用户可以使用 [SHOW ROLES](/tidb-cloud-lake/sql/show-roles.md) 命令查看当前角色以及授予给自己的所有角色。
- 如果你没有为用户显式设置默认角色，{{{ .lake }}} 会默认使用内置角色 `public` 作为默认角色。

## 活动角色和次要角色 {#active-role-secondary-roles}

在 {{{ .lake }}} 中，一个用户可以被授予多个角色。这些角色分为活动角色和次要角色：

- 活动角色是用户在当前会话中处于活动状态的主要角色，可以使用 [SET ROLE](/tidb-cloud-lake/sql/set-role.md) 命令进行设置。

- 次要角色是提供额外权限的附加角色，默认处于激活状态。用户可以使用 [SET SECONDARY ROLES](/tidb-cloud-lake/sql/set-secondary-roles.md) 命令启用或停用次要角色，以临时调整其权限作用域。

## 计费角色 {#billing-role}

除了标准内置角色之外，你还可以在 {{{ .lake }}} 中创建一个名为 `billing` 的自定义角色，以专门满足财务人员的需求。`billing` 角色仅提供对计费相关信息的访问，确保财务人员能够查看必要的财务数据，而不会接触到其他业务相关页面。

要设置并使用 `billing` 角色，可以使用以下命令创建它：

```sql
CREATE ROLE billing;
```

角色名称不区分大小写，因此 `billing` 和 `Billing` 被视为相同。有关设置和分配 `billing` 角色的详细步骤，请参见[向财务人员授予访问权限](/tidb-cloud-lake/guides/manage-costs.md#granting-access-to-finance-personnel)。

## 使用示例（基础） {#usage-examples-basic}

本示例展示了基于角色的权限管理。首先，创建一个 `writer` 角色并授予其权限。随后，将这些权限分配给用户 `eric`，使其继承这些权限。最后，从该角色回收这些权限，以展示其对用户权限的影响。

```sql title='Example:'
-- Create a new role named 'writer'
CREATE ROLE writer;

-- Grant all privileges on all objects in the 'default' schema to the role 'writer'
GRANT ALL ON default.* TO ROLE writer;

-- Create a new user named 'eric' with the password 'abc123' and set the default role
CREATE USER eric IDENTIFIED BY 'abc123' WITH DEFAULT_ROLE = 'writer';

-- Grant the role 'writer' to the user 'eric'
GRANT ROLE writer TO eric;

-- Show the granted privileges for the role 'writer'
SHOW GRANTS FOR ROLE writer;

┌───────────────────────────────────────────────────────┐
│                      Grants                           │
├───────────────────────────────────────────────────────┤
│ GRANT ALL ON 'default'.'default'.* TO ROLE 'writer'   │
└───────────────────────────────────────────────────────┘

-- Revoke all privileges on all objects in the 'default' schema from role 'writer'
REVOKE ALL ON default.* FROM ROLE writer;

-- Show the granted privileges for the role 'writer'
-- No privileges are displayed as they have been revoked from the role
SHOW GRANTS FOR ROLE writer;
```

## 与业务对齐的角色模型 {#business-aligned-role-model}

将角色与业务系统对齐，使每个领域只能访问自己的数据，而跨领域访问则通过协作角色来授予。

### 参考架构 {#reference-architecture}

```text
                         ┌──────────────┐
                         │  identity    │
                         │  account     │
                         └──────┬───────┘
                                │ users/permissions
                                v
┌──────────────┐   products   ┌──────────────┐   settlement ┌──────────────┐
│  marketing   │─────────────>│  commerce    │─────────────>│   payment    │
│  growth      │              │  orders      │              │  settlement  │
└──────┬───────┘              └──────┬───────┘              └──────┬───────┘
       │                            │ fulfillment                    │ accounting
       │                            v                               v
       │                      ┌──────────────┐               ┌──────────────┐
       │                      │ fulfillment  │               │   finance    │
       │                      │ logistics    │               │ accounting   │
       │                      └──────────────┘               └──────────────┘
       │
       │ support/feedback
       v
┌──────────────┐
│   support    │
│ tickets      │
└──────────────┘

       ^  risk monitoring/policies
       │
┌──────────────┐
│    risk      │
│  fraud       │
└──────────────┘
```

### 角色命名约定 {#role-conventions}

- `<biz>_owner`：拥有该领域中的所有对象
- `<biz>_rw`：供 pipeline 和工程师使用的写访问权限
- `<biz>_ro`：供分析师使用的只读访问权限
- Databases：`<biz>_raw`、`<biz>_mart`
- Stages：`stage_<biz>_ingest`

### 所有权行为 {#ownership-behavior}

对象归创建它们时处于活动状态的角色所有。请确保在创建对象之前执行 `SET ROLE <biz>_owner`。详情请参见 [所有权](/tidb-cloud-lake/guides/ownership.md)。

### 使用示例（业务领域） {#usage-examples-business-domains}

```sql title='示例：'
-- 1) 业务系统角色
CREATE ROLE identity_owner;
CREATE ROLE identity_rw;
CREATE ROLE identity_ro;

CREATE ROLE commerce_owner;
CREATE ROLE commerce_rw;
CREATE ROLE commerce_ro;

CREATE ROLE payment_owner;
CREATE ROLE payment_rw;
CREATE ROLE payment_ro;

CREATE ROLE fulfillment_owner;
CREATE ROLE fulfillment_rw;
CREATE ROLE fulfillment_ro;

CREATE ROLE marketing_owner;
CREATE ROLE marketing_rw;
CREATE ROLE marketing_ro;

CREATE ROLE finance_owner;
CREATE ROLE finance_rw;
CREATE ROLE finance_ro;

CREATE ROLE support_owner;
CREATE ROLE support_rw;
CREATE ROLE support_ro;

CREATE ROLE risk_owner;
CREATE ROLE risk_rw;
CREATE ROLE risk_ro;

-- 2) 业务系统资源
CREATE DATABASE identity_raw;
CREATE DATABASE identity_mart;
CREATE STAGE stage_identity_ingest;

CREATE DATABASE commerce_raw;
CREATE DATABASE commerce_mart;
CREATE STAGE stage_commerce_ingest;

CREATE DATABASE payment_raw;
CREATE DATABASE payment_mart;
CREATE STAGE stage_payment_ingest;

CREATE DATABASE fulfillment_raw;
CREATE DATABASE fulfillment_mart;
CREATE STAGE stage_fulfillment_ingest;

CREATE DATABASE marketing_raw;
CREATE DATABASE marketing_mart;
CREATE STAGE stage_marketing_ingest;

CREATE DATABASE finance_raw;
CREATE DATABASE finance_mart;
CREATE STAGE stage_finance_ingest;

CREATE DATABASE support_raw;
CREATE DATABASE support_mart;
CREATE STAGE stage_support_ingest;

CREATE DATABASE risk_raw;
CREATE DATABASE risk_mart;
CREATE STAGE stage_risk_ingest;

-- 3) 将所有权分配给 owner 角色
GRANT OWNERSHIP ON identity_raw.* TO ROLE identity_owner;
GRANT OWNERSHIP ON identity_mart.* TO ROLE identity_owner;
GRANT OWNERSHIP ON STAGE stage_identity_ingest TO ROLE identity_owner;

GRANT OWNERSHIP ON commerce_raw.* TO ROLE commerce_owner;
GRANT OWNERSHIP ON commerce_mart.* TO ROLE commerce_owner;
GRANT OWNERSHIP ON STAGE stage_commerce_ingest TO ROLE commerce_owner;

GRANT OWNERSHIP ON payment_raw.* TO ROLE payment_owner;
GRANT OWNERSHIP ON payment_mart.* TO ROLE payment_owner;
GRANT OWNERSHIP ON STAGE stage_payment_ingest TO ROLE payment_owner;

GRANT OWNERSHIP ON fulfillment_raw.* TO ROLE fulfillment_owner;
GRANT OWNERSHIP ON fulfillment_mart.* TO ROLE fulfillment_owner;
GRANT OWNERSHIP ON STAGE stage_fulfillment_ingest TO ROLE fulfillment_owner;

GRANT OWNERSHIP ON marketing_raw.* TO ROLE marketing_owner;
GRANT OWNERSHIP ON marketing_mart.* TO ROLE marketing_owner;
GRANT OWNERSHIP ON STAGE stage_marketing_ingest TO ROLE marketing_owner;

GRANT OWNERSHIP ON finance_raw.* TO ROLE finance_owner;
GRANT OWNERSHIP ON finance_mart.* TO ROLE finance_owner;
GRANT OWNERSHIP ON STAGE stage_finance_ingest TO ROLE finance_owner;

GRANT OWNERSHIP ON support_raw.* TO ROLE support_owner;
GRANT OWNERSHIP ON support_mart.* TO ROLE support_owner;
GRANT OWNERSHIP ON STAGE stage_support_ingest TO ROLE support_owner;

GRANT OWNERSHIP ON risk_raw.* TO ROLE risk_owner;
GRANT OWNERSHIP ON risk_mart.* TO ROLE risk_owner;
GRANT OWNERSHIP ON STAGE stage_risk_ingest TO ROLE risk_owner;

-- 4) 每个域内的读写分离
GRANT USAGE ON identity_raw.* TO ROLE identity_rw;
GRANT SELECT ON identity_raw.* TO ROLE identity_rw;
GRANT CREATE, INSERT, UPDATE, DELETE, ALTER, DROP ON identity_mart.* TO ROLE identity_rw;
GRANT USAGE ON identity_mart.* TO ROLE identity_ro;
GRANT SELECT ON identity_mart.* TO ROLE identity_ro;
GRANT READ, WRITE ON STAGE stage_identity_ingest TO ROLE identity_rw;

GRANT USAGE ON commerce_raw.* TO ROLE commerce_rw;
GRANT SELECT ON commerce_raw.* TO ROLE commerce_rw;
GRANT CREATE, INSERT, UPDATE, DELETE, ALTER, DROP ON commerce_mart.* TO ROLE commerce_rw;
GRANT USAGE ON commerce_mart.* TO ROLE commerce_ro;
GRANT SELECT ON commerce_mart.* TO ROLE commerce_ro;
GRANT READ, WRITE ON STAGE stage_commerce_ingest TO ROLE commerce_rw;

GRANT USAGE ON payment_raw.* TO ROLE payment_rw;
GRANT SELECT ON payment_raw.* TO ROLE payment_rw;
GRANT CREATE, INSERT, UPDATE, DELETE, ALTER, DROP ON payment_mart.* TO ROLE payment_rw;
GRANT USAGE ON payment_mart.* TO ROLE payment_ro;
GRANT SELECT ON payment_mart.* TO ROLE payment_ro;
GRANT READ, WRITE ON STAGE stage_payment_ingest TO ROLE payment_rw;

GRANT USAGE ON fulfillment_raw.* TO ROLE fulfillment_rw;
GRANT SELECT ON fulfillment_raw.* TO ROLE fulfillment_rw;
GRANT CREATE, INSERT, UPDATE, DELETE, ALTER, DROP ON fulfillment_mart.* TO ROLE fulfillment_rw;
GRANT USAGE ON fulfillment_mart.* TO ROLE fulfillment_ro;
GRANT SELECT ON fulfillment_mart.* TO ROLE fulfillment_ro;
GRANT READ, WRITE ON STAGE stage_fulfillment_ingest TO ROLE fulfillment_rw;

GRANT USAGE ON marketing_raw.* TO ROLE marketing_rw;
GRANT SELECT ON marketing_raw.* TO ROLE marketing_rw;
GRANT CREATE, INSERT, UPDATE, DELETE, ALTER, DROP ON marketing_mart.* TO ROLE marketing_rw;
GRANT USAGE ON marketing_mart.* TO ROLE marketing_ro;
GRANT SELECT ON marketing_mart.* TO ROLE marketing_ro;
GRANT READ, WRITE ON STAGE stage_marketing_ingest TO ROLE marketing_rw;

GRANT USAGE ON finance_raw.* TO ROLE finance_rw;
GRANT SELECT ON finance_raw.* TO ROLE finance_rw;
GRANT CREATE, INSERT, UPDATE, DELETE, ALTER, DROP ON finance_mart.* TO ROLE finance_rw;
GRANT USAGE ON finance_mart.* TO ROLE finance_ro;
GRANT SELECT ON finance_mart.* TO ROLE finance_ro;
GRANT READ, WRITE ON STAGE stage_finance_ingest TO ROLE finance_rw;

GRANT USAGE ON support_raw.* TO ROLE support_rw;
GRANT SELECT ON support_raw.* TO ROLE support_rw;
GRANT CREATE, INSERT, UPDATE, DELETE, ALTER, DROP ON support_mart.* TO ROLE support_rw;
GRANT USAGE ON support_mart.* TO ROLE support_ro;
GRANT SELECT ON support_mart.* TO ROLE support_ro;
GRANT READ, WRITE ON STAGE stage_support_ingest TO ROLE support_rw;

GRANT USAGE ON risk_raw.* TO ROLE risk_rw;
GRANT SELECT ON risk_raw.* TO ROLE risk_rw;
GRANT CREATE, INSERT, UPDATE, DELETE, ALTER, DROP ON risk_mart.* TO ROLE risk_rw;
GRANT USAGE ON risk_mart.* TO ROLE risk_ro;
GRANT SELECT ON risk_mart.* TO ROLE risk_ro;
GRANT READ, WRITE ON STAGE stage_risk_ingest TO ROLE risk_rw;

-- 5) 在创建时分配所有权
SET ROLE commerce_owner;
CREATE TABLE commerce_mart.orders (
  order_id STRING,
  user_id STRING,
  order_ts TIMESTAMP,
  amount DECIMAL(18, 2)
);

SET ROLE payment_owner;
CREATE TABLE payment_mart.transactions (
  transaction_id STRING,
  order_id STRING,
  user_id STRING,
  transaction_ts TIMESTAMP,
  amount DECIMAL(18, 2)
);

SET ROLE identity_owner;
CREATE TABLE identity_mart.users (
  user_id STRING,
  email STRING,
  created_at TIMESTAMP
);

-- 6) 与架构对齐的协作角色
CREATE ROLE collab_marketing_commerce;
GRANT SELECT ON commerce_mart.orders TO ROLE collab_marketing_commerce;
GRANT ROLE collab_marketing_commerce TO ROLE marketing_ro;

CREATE ROLE collab_fulfillment_commerce;
GRANT SELECT ON commerce_mart.orders TO ROLE collab_fulfillment_commerce;
GRANT ROLE collab_fulfillment_commerce TO ROLE fulfillment_ro;

CREATE ROLE collab_payment_commerce;
GRANT SELECT ON commerce_mart.orders TO ROLE collab_payment_commerce;
GRANT ROLE collab_payment_commerce TO ROLE payment_ro;

CREATE ROLE collab_finance_payment;
GRANT SELECT ON payment_mart.transactions TO ROLE collab_finance_payment;
GRANT ROLE collab_finance_payment TO ROLE finance_ro;

CREATE ROLE collab_support_core;
GRANT SELECT ON commerce_mart.orders TO ROLE collab_support_core;
GRANT SELECT ON payment_mart.transactions TO ROLE collab_support_core;
GRANT ROLE collab_support_core TO ROLE support_ro;

CREATE ROLE collab_risk_core;
GRANT SELECT ON identity_mart.users TO ROLE collab_risk_core;
GRANT SELECT ON commerce_mart.orders TO ROLE collab_risk_core;
GRANT SELECT ON payment_mart.transactions TO ROLE collab_risk_core;
GRANT ROLE collab_risk_core TO ROLE risk_ro;
```