---
title: Roles
---

Roles in Databend play a pivotal role in simplifying the management of permissions. When multiple users require the same set of privileges, granting privileges individually can be cumbersome. Roles provide a solution by allowing the assignment of a set of privileges to a role, which can then be easily assigned to multiple users.

![Alt text](/img/guides/access-control-3.png)

## Inheriting Roles & Establishing Hierarchy

Role granting enables one role to inherit permissions and responsibilities from another. This contributes to the creation of a flexible hierarchy, similar to the organizational structure, where two [Built-in Roles](#built-in-roles) exist: the highest being `account-admin` and the lowest being `public`.

Consider the scenario where three roles are created: *manager*, *engineer*, and *intern*. In this example, the role of *intern* is granted to the engineer *role*. Consequently, the *engineer* not only possesses their own set of privileges but also inherits those associated with the *intern* role. Extending this hierarchy further, if the *engineer* role is granted to the *manager*, the *manager* now acquires both the inherent privileges of the *engineer* and the *intern* roles.

![Alt text](/img/guides/access-control-4.png)

## Built-in Roles

Databend comes with the following built-in roles:

| Built-in Role | Description                                                                                                                            |
|---------------|----------------------------------------------------------------------------------------------------------------------------------------|
| account-admin | Possesses all privileges, serves as the parent role for all other roles, and enables seamless switching to any role within the tenant. |
| public        | Inherits no permissions, considers all roles as its parent roles, and allows any role to switch to the public role.                    |

To assign the `account-admin` role to a user in Databend Cloud, select the role when inviting the user. You can also assign the role to a user after they join. If you're using Databend Community Edition or Enterprise Edition, configure an `account-admin` user during deployment first, and then assign the role to other users if needed. For more information about configuring admin users, see [Configuring Admin Users](../../20-self-hosted/04-references/admin-users.md).

## Setting Default Role

When a user is granted multiple roles, you can use the [CREATE USER](/sql/sql-commands/ddl/user/user-create-user) or [ALTER USER](/sql/sql-commands/ddl/user/user-alter-user) commands to set a default role for that user. The default role determines the role automatically assigned to the user at the beginning of a session:

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

- Users have the flexibility to switch to other roles within a session using the [SET ROLE](/sql/sql-commands/ddl/user/user-set-role) command.
- A user can examine their current role and view all the roles granted to them by using the [SHOW ROLES](/sql/sql-commands/ddl/user/user-show-roles) command.
- If you don't explicitly set a default role for a user, Databend will default to using the built-in role `public` as the default role.

## Active Role & Secondary Roles

A user can be granted multiple roles in Databend. These roles are categorized into an active role and secondary roles:

- The active role is the user's currently active primary role for the session, which can be set using the [SET ROLE](/sql/sql-commands/ddl/user/user-set-role) command. 

- Secondary roles are additional roles that provide extra permissions and are active by default. Users can activate or deactivate secondary roles with the [SET SECONDARY ROLES](/sql/sql-commands/ddl/user/user-set-2nd-roles) command to temporarily adjust their permission scope.

## Billing Role

In addition to the standard built-in roles, you can create a custom role named `billing` in Databend Cloud to cater specifically to the needs of finance personnel. The role `billing` provides access only to billing-related information, ensuring that finance personnel can view necessary financial data without exposure to other business-related pages.

To set up and use the role `billing`, you can create it using the following command:

```sql
CREATE ROLE billing;
```
The role name is case-insensitive, so `billing` and `Billing` are considered the same. For detailed steps on setting and assigning the role `billing`, see [Granting Access to Finance Personnel](/guides/cloud/administration/costs#granting-access-to-finance-personnel).

## Usage Examples (Basic)

This example showcases role-based permission management. Initially, a 'writer' role is created and granted privileges. Subsequently, these privileges are assigned to the user 'eric', who inherits them. Lastly, the permissions are revoked from the role, demonstrating their impact on the user's privileges.

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

## Business-Aligned Role Model

Align roles to business systems so each domain can access only its own data, and cross-domain access is granted through collaboration roles.

### Reference Architecture

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

### Role Conventions

- `<biz>_owner`: owns all objects in the domain
- `<biz>_rw`: write access for pipelines and engineers
- `<biz>_ro`: read-only access for analysts
- Databases: `<biz>_raw`, `<biz>_mart`
- Stages: `stage_<biz>_ingest`

### Ownership Behavior

Objects are owned by the role that is active when they are created. Ensure you `SET ROLE <biz>_owner` before creating objects. For details, see [Ownership](03-ownership.md).

### Usage Examples (Business Domains)

```sql title='Example:'
-- 1) Business system roles
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

-- 2) Business system resources
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

-- 3) Ownership assigned to owner roles
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

-- 4) Read/write separation inside each domain
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

-- 5) Ownership assigned at creation time
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

-- 6) Collaboration roles aligned with the architecture
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
