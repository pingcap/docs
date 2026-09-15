---
title: 数据保护策略
summary: 了解掩码策略和行访问策略，它们无需修改存储值即可保护敏感信息。
---

# 数据保护策略

{{{ .lake }}} 在查询时保护敏感数据，而不会更改存储的值：

| 策略 | 它的作用 |
|--------|----------------|
| [脱敏策略](/tidb-cloud-lake/guides/masking-policy.md) | 转换列值——未授予权限的用户看到的是脱敏数据 |
| [行访问策略](/tidb-cloud-lake/guides/row-access-policy.md) | 过滤整行——未授予权限的用户永远看不到这些行 |

两者对应用程序都是透明的：无需修改代码，无需额外视图，无需复制数据。

## 选择合适的策略 {#choose-the-right-policy}

| 场景 | 用途 |
|----------|-----|
| 隐藏整行 | 行访问 |
| 保留该行，但对某一列脱敏 | 脱敏 |
| 不同角色看到同一列的不同精度 | 脱敏 |
| 多租户 / 区域隔离 | 行访问 |
| 按角色进行时间窗口控制 | 行访问 |
| 隐藏 JSON / VARIANT 中的键 | 脱敏 |
| 行隔离 + 列脱敏 | 两者都用（但不能用于同一列） |

示例：一个包含 phone、amount 和 region 的 `orders` 表。

| 要求 | 策略 |
|-------------|--------|
| 支持团队只能看到其所在 region | 基于 `region` 的行访问 |
| 分析师看到 `138****1234` | 基于 `phone` 的掩码 |
| 管理员看到所有内容 | 通过两种策略的角色 |

## 它们如何协同工作 {#how-they-work-together}

```
Query
  → Row Access Policy filters rows
  → Masking Policy transforms surviving columns
  → Result returned
```

行过滤先执行。掩码仅应用于剩余的行。

| | 掩码 | 行访问 |
|---|---|---|
| 作用域 | 列值 | 整行 |
| 返回类型 | 与列类型匹配 | BOOLEAN |
| 限制 | 每列一个 | 每表一个 |
| 影响 | `SELECT` | `SELECT`, `UPDATE`, `DELETE`, `MERGE` |
| 存储的数据 / `INSERT` | 不变 / 不过滤 | 不变 / 不过滤 |

同一张表可以同时使用两者。同一个 **column** 不能同时绑定到两者。

```sql
-- Rows: sales only see their region
CREATE ROW ACCESS POLICY rap_region
AS (r STRING) RETURNS BOOLEAN ->
CASE
  WHEN is_role_in_session('admin') THEN true
  ELSE is_role_in_session(r)
END;

ALTER TABLE customers ADD ROW ACCESS POLICY rap_region ON (region);

-- Columns: non-HR see redacted SSN
CREATE MASKING POLICY mask_ssn
AS (val STRING) RETURNS STRING ->
CASE
  WHEN is_role_in_session('hr') THEN val
  ELSE '***-**-****'
END;

ALTER TABLE customers MODIFY COLUMN ssn SET MASKING POLICY mask_ssn;
```

## 端到端：职责分离 {#end-to-end-separation-of-duties}

将 RBAC 与这两种策略结合使用，使创建者、应用者和读取者彼此分离。

| 角色 | 工作 | 可见内容 |
|------|-----|------|
| `security_admin` | 创建 / 拥有策略 | 没有表 SELECT 权限 |
| `data_engineer` | 拥有表，附加策略 | 所有行，原始 phone |
| `analyst_apac` | 分析 APAC | APAC 行，phone 已脱敏 |
| `support_global` | 全局支持 | 所有行，原始 phone |

```sql
-- account_admin: roles, users, CREATE privileges
CREATE ROLE security_admin;
CREATE ROLE data_engineer;
CREATE ROLE analyst_apac;
CREATE ROLE support_global;

CREATE USER sec_user IDENTIFIED BY 'password123';
CREATE USER eng_user IDENTIFIED BY 'password123';
CREATE USER analyst_user IDENTIFIED BY 'password123';
CREATE USER support_user IDENTIFIED BY 'password123';

GRANT ROLE security_admin TO USER sec_user;
GRANT ROLE data_engineer TO USER eng_user;
GRANT ROLE analyst_apac TO USER analyst_user;
GRANT ROLE support_global TO USER support_user;

GRANT CREATE DATABASE ON *.* TO ROLE data_engineer;
GRANT CREATE MASKING POLICY ON *.* TO ROLE security_admin;
GRANT CREATE ROW ACCESS POLICY ON *.* TO ROLE security_admin;
GRANT GRANT ON *.* TO ROLE security_admin;

-- data_engineer: table ownership
SET ROLE data_engineer;
CREATE DATABASE ecommerce;
CREATE TABLE ecommerce.orders (
  order_id INT,
  customer_name STRING,
  phone STRING,
  region STRING,
  amount DECIMAL(10,2),
  created_at TIMESTAMP
);
INSERT INTO ecommerce.orders VALUES
  (1, 'Alice',   '13812345678', 'APAC', 299.00, '2025-01-15 10:00:00'),
  (2, 'Bob',     '14987654321', 'EMEA', 150.00, '2025-01-16 11:00:00'),
  (3, 'Charlie', '13698765432', 'APAC', 520.00, '2025-01-17 09:30:00'),
  (4, 'Diana',   '15012349876', 'AMER',  89.00, '2025-01-18 14:00:00');

-- security_admin: create policies (auto OWNERSHIP)
SET ROLE security_admin;
SET enable_experimental_row_access_policy = 1;

CREATE MASKING POLICY mask_phone
AS (val STRING) RETURNS STRING ->
CASE
  WHEN is_role_in_session('data_engineer') OR is_role_in_session('support_global') THEN val
  ELSE CONCAT(SUBSTRING(val, 1, 3), '****', SUBSTRING(val, 8))
END;

CREATE ROW ACCESS POLICY rap_region
AS (r STRING) RETURNS BOOLEAN ->
CASE
  WHEN is_role_in_session('data_engineer') OR is_role_in_session('support_global') THEN true
  WHEN is_role_in_session('analyst_apac') AND r = 'APAC' THEN true
  ELSE false
END;

GRANT APPLY ON MASKING POLICY mask_phone TO ROLE data_engineer;
GRANT APPLY ON ROW ACCESS POLICY rap_region TO ROLE data_engineer;

-- data_engineer: attach (needs table ALTER + policy APPLY)
SET ROLE data_engineer;
SET enable_experimental_row_access_policy = 1;
ALTER TABLE ecommerce.orders MODIFY COLUMN phone SET MASKING POLICY mask_phone;
ALTER TABLE ecommerce.orders ADD ROW ACCESS POLICY rap_region ON (region);

-- account_admin: grant table access through roles
GRANT USAGE ON ecommerce.* TO ROLE analyst_apac;
GRANT USAGE ON ecommerce.* TO ROLE support_global;
GRANT SELECT ON ecommerce.orders TO ROLE analyst_apac;
GRANT SELECT ON ecommerce.orders TO ROLE support_global;
```

结果：

| 角色 | 行 | 电话 |
|------|------|-------|
| `analyst_apac` | 仅 APAC | 已脱敏 (`138****5678`) |
| `support_global` | 全部 | 原始值 |
| `security_admin` | — | 权限被拒绝（无 SELECT 权限） |

```sql
SET ROLE analyst_apac;
SELECT * FROM ecommerce.orders;
-- Alice / Charlie only, phones masked

SET ROLE support_global;
SELECT * FROM ecommerce.orders;
-- all 4 rows, phones visible

SET ROLE security_admin;
SELECT * FROM ecommerce.orders;
-- ERROR: Permission denied
```

回收该角色后，无需更改表授权即可移除访问权限：

```sql
REVOKE ROLE analyst_apac FROM USER analyst_user;
```

**经验法则：**

- 创建策略 ≠ 查询数据；附加策略需要同时具备策略 `APPLY` 和表 `ALTER`
- 优先将权限授予角色，而不是用户
- 创建者角色会自动获得 OWNERSHIP
- `CREATE MASKING/ROW ACCESS POLICY` 是授予给角色，而不是用户
- 使用 `SHOW GRANTS ON MASKING POLICY ...`、`SHOW GRANTS ON ROW ACCESS POLICY ...` 和 `POLICY_REFERENCES(...)` 进行审计

## 后续步骤 {#next-steps}

- [脱敏策略](/tidb-cloud-lake/guides/masking-policy.md) — 条件掩码、VARIANT 键
- [行访问策略](/tidb-cloud-lake/guides/row-access-policy.md) — 向量 / RAG 可见性、时间窗口、DML