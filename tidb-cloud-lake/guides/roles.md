---
title: ロール
summary: {{{ .lake }}} のロールは、権限管理を簡素化するうえで重要な役割を果たします。複数のユーザーに同じ権限セットが必要な場合、権限を個別に付与するのは煩雑になることがあります。ロールを使用すると、権限セットをロールに割り当て、そのロールを複数のユーザーに簡単に割り当てることができます。
---

# ロール

{{{ .lake }}} のロールは、権限管理を簡素化するうえで重要な役割を果たします。複数のユーザーに同じ権限セットが必要な場合、権限を個別に付与するのは煩雑になることがあります。ロールを使用すると、権限セットをロールに割り当て、そのロールを複数のユーザーに簡単に割り当てることができます。

![Alt text](/media/tidb-cloud-lake/access-control-3.png)

## ロールの継承と階層の確立 {#inheriting-roles-establishing-hierarchy}

ロールの付与により、あるロールが別のロールから権限と責務を継承できるようになります。これにより、組織構造に似た柔軟な階層を作成できます。この階層には 2 つの [組み込みロール](#built-in-roles) があり、最上位が `account-admin`、最下位が `public` です。

たとえば、*manager*、*engineer*、*intern* の 3 つのロールを作成したとします。この例では、*intern* ロールが engineer *role* に付与されます。その結果、*engineer* は自身の権限セットを持つだけでなく、*intern* ロールに関連付けられた権限も継承します。さらにこの階層を拡張して、*engineer* ロールが *manager* に付与されると、*manager* は *engineer* と *intern* の両方のロールに本来備わっている権限を取得します。

![Alt text](/media/tidb-cloud-lake/access-control-4.png)

## 組み込みロール {#built-in-roles}

{{{ .lake }}} には、次の組み込みロールがあります。

| 組み込みロール | 説明 |
|---------------|----------------------------------------------------------------------------------------------------------------------------------------|
| account-admin | すべての権限を持ち、他のすべてのロールの親ロールとして機能し、テナント内の任意のロールへシームレスに切り替えることができます。 |
| public        | 権限を一切継承せず、すべてのロールを親ロールとして扱い、任意のロールが public ロールに切り替えることを許可します。 |

{{{ .lake }}} でユーザーに `account-admin` ロールを割り当てるには、ユーザー招待時にそのロールを選択します。ユーザー参加後にロールを割り当てることもできます。{{{ .lake }}} Community Edition または Enterprise Edition を使用している場合は、まずデプロイ時に `account-admin` ユーザーを設定し、その後必要に応じて他のユーザーにこのロールを割り当てます。

## デフォルトロールの設定 {#setting-default-role}

ユーザーに複数のロールが付与されている場合、[CREATE USER](/tidb-cloud-lake/sql/create-user.md) または [ALTER USER](/tidb-cloud-lake/sql/alter-user.md) コマンドを使用して、そのユーザーのデフォルトロールを設定できます。デフォルトロールは、セッション開始時にユーザーへ自動的に割り当てられるロールを決定します。

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

- ユーザーは、セッション内で [SET ROLE](/tidb-cloud-lake/sql/set-role.md) コマンドを使用して他のロールに柔軟に切り替えることができます。
- ユーザーは、[SHOW ROLES](/tidb-cloud-lake/sql/show-roles.md) コマンドを使用して、現在のロールを確認し、自分に付与されているすべてのロールを表示できます。
- ユーザーに対してデフォルトロールを明示的に設定しない場合、{{{ .lake }}} は組み込みロール `public` をデフォルトロールとして使用します。

## アクティブロールとセカンダリロール {#active-role-secondary-roles}

{{{ .lake }}} では、1 人のユーザーに複数のロールを付与できます。これらのロールは、アクティブロールとセカンダリロールに分類されます。

- アクティブロールは、そのセッションで現在有効なユーザーの主要ロールであり、[SET ROLE](/tidb-cloud-lake/sql/set-role.md) コマンドを使用して設定できます。

- セカンダリロールは、追加の権限を提供するロールであり、デフォルトで有効です。ユーザーは [SET SECONDARY ROLES](/tidb-cloud-lake/sql/set-secondary-roles.md) コマンドを使用してセカンダリロールを有効化または無効化し、権限範囲を一時的に調整できます。

## 請求ロール {#billing-role}

標準の組み込みロールに加えて、{{{ .lake }}} では財務担当者のニーズに特化した `billing` という名前のカスタムロールを作成できます。`billing` ロールは請求関連情報のみにアクセスを提供するため、財務担当者は他の業務関連ページに触れることなく、必要な財務データを閲覧できます。

`billing` ロールを設定して使用するには、次のコマンドで作成します。

```sql
CREATE ROLE billing;
```

ロール名では大文字と小文字は区別されないため、`billing` と `Billing` は同じものとして扱われます。`billing` ロールの設定および割り当て手順の詳細については、[財務担当者にアクセス権を付与する](/tidb-cloud-lake/guides/manage-costs.md#granting-access-to-finance-personnel) を参照してください。

## 使用例（基本） {#usage-examples-basic}

この例では、ロールベースの権限管理を示します。まず、`writer` ロールを作成して権限を付与します。次に、これらの権限をユーザー `eric` に割り当て、`eric` がそれらを継承します。最後に、ロールから権限を取り消し、それがユーザーの権限に与える影響を示します。

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

## ビジネスに整合したロールモデル {#business-aligned-role-model}

各ドメインが自分のデータのみにアクセスできるよう、ロールをビジネスシステムに合わせて設計し、ドメインをまたぐアクセスはコラボレーション用ロールを通じて付与します。

### 参照アーキテクチャ {#reference-architecture}

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

### ロール命名規則 {#role-conventions}

- `<biz>_owner`: ドメイン内のすべてのオブジェクトを所有
- `<biz>_rw`: パイプラインおよびエンジニア向けの書き込みアクセス
- `<biz>_ro`: アナリスト向けの読み取り専用アクセス
- データベース: `<biz>_raw`, `<biz>_mart`
- stage: `stage_<biz>_ingest`

### 所有権の動作 {#ownership-behavior}

オブジェクトは、作成時にアクティブだったロールによって所有されます。オブジェクトを作成する前に、必ず `SET ROLE <biz>_owner` を実行してください。詳細については、[Ownership](/tidb-cloud-lake/guides/ownership.md) を参照してください。

### 使用例（業務ドメイン） {#usage-examples-business-domains}

```sql title='例:'
-- 1) 業務システムのロール
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

-- 2) 業務システムのリソース
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

-- 3) owner ロールに割り当てられた所有権
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

-- 4) 各ドメイン内での読み取り/書き込みの分離
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

-- 5) 作成時に割り当てられる所有権
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

-- 6) アーキテクチャに合わせたコラボレーションロール
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