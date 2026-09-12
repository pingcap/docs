---
title: 行访问策略
summary: 行访问策略通过在查询时过滤表中的行来保护数据。你可以集中定义一次行级谓词，将其附加到表上，并确保用户只能看到满足策略的行。
---

# 行访问策略

行访问策略会在查询时过滤表中的行。只需定义一次布尔谓词并将其附加到表上，用户就只能看到通过该策略的行。

如果你希望进行列级脱敏，而不是隐藏整行，请使用[脱敏策略](/tidb-cloud-lake/guides/masking-policy.md)。

> **Note:**
>
> 这是一个**实验性**功能。可通过 `SET enable_experimental_row_access_policy = 1`（会话）或 `SET GLOBAL enable_experimental_row_access_policy = 1`（账户）启用。

## 何时使用 {#when-to-use}

- 多租户隔离 —— 每个租户只能看到自己的行
- 区域 / 部门隔离 —— 销售只能看到其所属区域的数据
- 时间窗口控制 —— 告警可扫描 1 天数据；离线分析可扫描 7 天数据
- 向量 / RAG 搜索 —— 共享知识库，基于角色控制文档可见性
- 合规 —— 审计人员只能看到已批准的时间范围或子集

## 快速开始 {#quick-start}

```sql
SET enable_experimental_row_access_policy = 1;

CREATE TABLE employees (
  id INT,
  name STRING,
  department STRING
);

INSERT INTO employees VALUES
  (1, 'Alice', 'Engineering'),
  (2, 'Bob', 'Sales'),
  (3, 'Charlie', 'Engineering');

CREATE ROW ACCESS POLICY rap_engineering
AS (dept STRING)
RETURNS BOOLEAN ->
CASE
  WHEN IS_ROLE_IN_SESSION('admin') THEN true
  WHEN dept = 'Engineering' THEN true
  ELSE false
END;

-- ON (column) maps to the policy argument by position
ALTER TABLE employees ADD ROW ACCESS POLICY rap_engineering ON (department);

SELECT id, name, department FROM employees ORDER BY id;
```

```
id | name    | department
---|---------|-------------
 1 | Alice   | Engineering
 3 | Charlie | Engineering
```

**工作原理**

- 仅在查询时生效 —— 存储的数据不会改变
- 每张表只能有一个策略；参数会按位置映射到 `ON (...)` 中的列
- 优先使用 `IS_ROLE_IN_SESSION()` 而不是 `current_role()`，这样用户无法通过 `SET ROLE` 绕过策略

多列策略：

```sql
CREATE ROW ACCESS POLICY rap_region_dept
AS (region STRING, dept STRING)
RETURNS BOOLEAN ->
  region = 'APAC' AND dept = 'Engineering';

ALTER TABLE employees
ADD ROW ACCESS POLICY rap_region_dept ON (office_region, department);
```

## 示例 {#examples}

### 向量 / RAG 文档可见性 {#vector-rag-document-visibility}

共享知识库表 + 向量搜索。只需配置一次可见性；搜索 SQL 无需携带文档 ID 过滤条件。参见[向量搜索](/tidb-cloud-lake/guides/vector-search-guide.md)。

| 角色 | 可见内容 |
|------|------|
| `admin` | 所有行 |
| `sales` | `dept = 'sales'` + 公开 |
| `finance` | `dept = 'finance'` + 公开 |

```sql
SET enable_experimental_row_access_policy = 1;

CREATE ROLE IF NOT EXISTS admin;
CREATE ROLE IF NOT EXISTS sales;
CREATE ROLE IF NOT EXISTS finance;

CREATE TABLE knowledge_docs (
  doc_id    BIGINT,
  title     STRING,
  dept      STRING,
  is_public BOOLEAN,
  embedding VECTOR(4),
  VECTOR INDEX idx_emb(embedding) distance='cosine'
);

INSERT INTO knowledge_docs VALUES
  (1, 'Sales contract template',  'sales',   false, [0.90, 0.10, 0.05, 0.05]),
  (2, 'Q2 financial draft',       'finance', false, [0.10, 0.90, 0.05, 0.05]),
  (3, 'Public company handbook',  'hr',      true,  [0.20, 0.20, 0.90, 0.10]),
  (4, 'Competitor pricing notes', 'sales',   false, [0.85, 0.15, 0.10, 0.05]),
  (5, 'Internal audit checklist', 'finance', false, [0.15, 0.85, 0.10, 0.05]);

CREATE ROW ACCESS POLICY rap_knowledge_docs
AS (dept STRING, is_public BOOLEAN)
RETURNS BOOLEAN ->
CASE
  WHEN IS_ROLE_IN_SESSION('admin') THEN true
  WHEN is_public THEN true
  WHEN IS_ROLE_IN_SESSION('sales') AND dept = 'sales' THEN true
  WHEN IS_ROLE_IN_SESSION('finance') AND dept = 'finance' THEN true
  ELSE false
END;

ALTER TABLE knowledge_docs
ADD ROW ACCESS POLICY rap_knowledge_docs ON (dept, is_public);

GRANT SELECT ON knowledge_docs TO ROLE sales;
GRANT SELECT ON knowledge_docs TO ROLE finance;

-- Activate one role for the session, then run the same search SQL
SET ROLE sales;
SET SECONDARY ROLES NONE;

SELECT doc_id, title,
       round(cosine_distance(embedding, [0.88, 0.12, 0.08, 0.05]::VECTOR(4)), 4) AS dist
FROM knowledge_docs
ORDER BY dist
LIMIT 10;
```

| 作为 `sales` | 作为 `finance` (`SET ROLE finance`) |
|------------|-------------------------------------|
| 1 销售合同模板 `0.0009` | 3 上市公司手册 `0.6731` |
| 4 竞争对手定价说明 `0.0011` | 5 内部审计检查清单 `0.6855` |
| 3 上市公司手册 `0.6731` | 2 Q2 财务草案 `0.7504` |

### 按角色进行时间范围访问 {#time-range-access-by-role}

不同的服务账户可能只能扫描不同的历史时间窗口。

| 账户 | 角色 | 窗口 |
|---------|-------|--------|
| `svc_realtime_alert` | `rap_role_1_day` | 最近 1 天 |
| `svc_offline_analysis` | `rap_role_1_day`, `rap_role_7_day` | 最多 7 天 |

```sql
SET enable_experimental_row_access_policy = 1;

CREATE ROLE rap_role_7_day;
CREATE ROLE rap_role_1_day;

-- CASE is top-down: put the wider window first
CREATE ROW ACCESS POLICY rap_time_range
AS (start_time TIMESTAMP)
RETURNS BOOLEAN ->
CASE
  WHEN IS_ROLE_IN_SESSION('rap_role_7_day') THEN
    start_time >= now() - INTERVAL 7 DAY
  WHEN IS_ROLE_IN_SESSION('rap_role_1_day') THEN
    start_time >= now() - INTERVAL 1 DAY
  ELSE false
END;

CREATE TABLE metrics(id INT, start_time TIMESTAMP);
INSERT INTO metrics VALUES
  (1, now() - INTERVAL 15 DAY),
  (2, now() - INTERVAL 5 DAY),
  (3, now() - INTERVAL 12 HOUR),
  (4, now() - INTERVAL 1 HOUR),
  (5, now() - INTERVAL 8 DAY);

ALTER TABLE metrics ADD ROW ACCESS POLICY rap_time_range ON (start_time);

GRANT ROLE rap_role_1_day TO USER svc_realtime_alert;
GRANT ROLE rap_role_1_day TO USER svc_offline_analysis;
GRANT ROLE rap_role_7_day TO USER svc_offline_analysis;

SELECT id, start_time FROM metrics ORDER BY id;
```

登录后，{{{ .lake }}} 会激活所有已授予的角色（`SECONDARY ROLES ALL`）。

| 会话 | 可见行 |
|---------|--------------|
| `svc_realtime_alert`（仅 1 天） | 最近 1 天 |
| `svc_offline_analysis`（两个角色） | 默认最近 7 天 |

将离线账户收窄为 1 天：

```sql
SET ROLE rap_role_1_day;
SET SECONDARY ROLES NONE;
SELECT id, start_time FROM metrics ORDER BY id;
```

再次放宽：

```sql
SET ROLE rap_role_7_day;
SELECT id, start_time FROM metrics ORDER BY id;
```

一个账户只能激活已授予给它的角色。`svc_realtime_alert` 不能执行 `SET ROLE rap_role_7_day`。

## 读写行为 {#read-and-write-behavior}

| 操作 | 影响 |
|-----------|--------|
| `SELECT` | 仅返回策略可见的行 |
| `UPDATE` / `DELETE` / `MERGE` | 仅匹配/修改可见的目标行 |
| `INSERT` | 不会被过滤——即使当前不可见，行也会被存储 |

要检查所有已存储的行，请使用一个能够通过该策略的角色，或临时将策略解绑。

```sql
SET enable_experimental_row_access_policy = 1;

CREATE ROW ACCESS POLICY rap_sales_only
AS (dept STRING) RETURNS BOOLEAN -> dept = 'sales';

CREATE TABLE orders(id INT, dept STRING, amount INT);
ALTER TABLE orders ADD ROW ACCESS POLICY rap_sales_only ON (dept);

INSERT INTO orders VALUES (1, 'sales', 100), (2, 'eng', 200), (3, 'sales', 300);

SELECT * FROM orders ORDER BY id;
-- 1 sales 100
-- 3 sales 300

UPDATE orders SET amount = amount + 10;
DELETE FROM orders WHERE dept = 'eng';   -- no-op: eng rows are invisible
DELETE FROM orders WHERE id = 1;         -- deletes visible row 1

-- MERGE only matches visible targets
CREATE TABLE src(id INT, new_amount INT);
INSERT INTO src VALUES (2, 777), (3, 888);

MERGE INTO orders AS t
USING src AS s
ON t.id = s.id
WHEN MATCHED THEN UPDATE SET t.amount = s.new_amount;

-- Detach to inspect storage
ALTER TABLE orders DROP ROW ACCESS POLICY rap_sales_only;
SELECT * FROM orders ORDER BY id;
-- 2 eng 200   (never updated)
-- 3 sales 888 (merged)
```

## 管理策略 {#manage-policies}

```sql
DESC ROW ACCESS POLICY rap_engineering;

ALTER TABLE employees DROP ROW ACCESS POLICY rap_engineering;
DROP ROW ACCESS POLICY rap_engineering;

ALTER TABLE employees DROP ALL ROW ACCESS POLICIES;
```

在执行 `DROP ROW ACCESS POLICY` 之前，请先解绑。修改受保护列之前，也需要先删除或解绑策略。

## 限制 {#limits}

- 每个表只能有一个行访问策略
- 仅支持普通表——不支持视图、流、临时表或 ICE 数据库
- 每列只能有一个安全策略（脱敏 **or** 行访问，不能同时使用）
- 不支持 `CREATE OR REPLACE` / `ALTER` policy——需要删除后重建
- 策略名称在脱敏策略和行访问策略之间是全局唯一的
- 创建时，策略参数名称会被转换为小写

## 最佳实践 {#best-practices}

1. 优先使用 `IS_ROLE_IN_SESSION()`，而不是 `current_role()`。
2. 按“最宽 → 最窄”的顺序排列 `CASE` 分支（管理员优先）。
3. 如果策略引用了查找表，请将其与受保护表放在同一个数据库中。
4. 在绑定后使用多个角色进行验证——管理员、受限角色和无匹配角色都要验证。
5. 对于全量数据检查，优先使用有权限的角色，而不是反复解绑/绑定。

## 权限与参考 {#privileges-references}

- 在 `*.*` 上具有 `CREATE ROW ACCESS POLICY` 权限以创建策略（创建者获得 OWNERSHIP）
- 具有表上的 `ALTER` 权限，以及 `APPLY ROW ACCESS POLICY`（全局）或 `APPLY ON ROW ACCESS POLICY <name>` 权限以进行绑定/解绑
- 审计：`SHOW GRANTS ON ROW ACCESS POLICY <name>`
- 用法：[`POLICY_REFERENCES`](/tidb-cloud-lake/sql/policy-references.md)

另请参阅：

- [用户与角色](/tidb-cloud-lake/sql/user-role.md)
- [CREATE ROW ACCESS POLICY](/tidb-cloud-lake/sql/create-row-access-policy.md)
- [ALTER TABLE](/tidb-cloud-lake/sql/alter-table.md#row-access-policy-operations)
- [行访问策略命令](/tidb-cloud-lake/sql/row-access-policy-overview.md)