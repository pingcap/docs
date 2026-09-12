---
title: 脱敏策略
summary: 脱敏策略通过在查询执行期间动态转换列值来保护敏感数据。它们支持基于角色访问机密信息——已授予权限的用户看到真实数据，其他用户看到脱敏后的值。
---

# 脱敏策略

脱敏策略会在查询时转换列值。已授予权限的角色可以看到真实数据；其他角色看到的是脱敏后的值。存储的数据本身不会发生变化。

如果你想隐藏整行而不是对列进行脱敏，请使用[行访问策略](/tidb-cloud-lake/guides/row-access-policy.md)。

## 何时使用 {#when-to-use}

- 客服支持 — 客服人员可以看到订单，但 ID 显示为 `3201**********1234`
- 分析场景 — email 显示为 `***@***.com`，同时不会影响聚合结果
- VARIANT 日志 — 对非管理员隐藏 `secret_key` / `token` 等 JSON 键
- 部分脱敏 — 为了验证，仅显示卡号后 4 位

## 快速开始 {#quick-start}

```sql
CREATE TABLE user_info (id INT, email STRING NOT NULL);

CREATE MASKING POLICY email_mask
AS (val STRING)
RETURNS STRING ->
CASE
  WHEN is_role_in_session('managers') THEN val
  ELSE '*********'
END;

ALTER TABLE user_info MODIFY COLUMN email SET MASKING POLICY email_mask;

INSERT INTO user_info VALUES (1, 'user@example.com');
SELECT * FROM user_info;
```

```
id | email
---|----------
 1 | *********
```

**工作原理**

- 仅在查询时生效 — `SELECT` 会被脱敏；`INSERT` / `UPDATE` / `DELETE` 使用真实值
- 列级作用域 — 每列只能绑定一个策略；同一个策略可在多张表中复用
- 优先使用 `is_role_in_session()` 而不是 `current_role()`，这样用户无法通过 `SET ROLE` 绕过限制

## 示例 {#examples}

### 条件脱敏（`USING`） {#conditional-masking-using}

基于另一列进行脱敏：

```sql
CREATE MASKING POLICY vip_mask
AS (val STRING, is_vip BOOLEAN)
RETURNS STRING ->
CASE
  WHEN is_vip = true THEN val
  ELSE '*********'
END;

ALTER TABLE user_info
MODIFY COLUMN email SET MASKING POLICY vip_mask USING (email, is_vip);

INSERT INTO user_info (id, email, is_vip) VALUES
  (1, 'vip@example.com', true),
  (2, 'normal@example.com', false);

SELECT * FROM user_info;
```

```
id | email           | is_vip
---|-----------------|-------
 1 | vip@example.com | true
 2 | *********       | false
```

仅当策略体需要这些列时，才将列添加到 `USING` 中。

### VARIANT 子字段脱敏 {#variant-sub-field-masking}

使用 `object_delete` 隐藏特定 JSON 键。所有访问路径都会遵循该脱敏规则（如下标、路径函数、类型转换、`json_object_keys`）。

```sql
CREATE TABLE events (id INT, data VARIANT);

INSERT INTO events VALUES
  (1, parse_json('{"name":"alice","content":"secret data","secret_key":"sk_123","age":30}')),
  (2, parse_json('{"name":"bob","content":"private info","secret_key":"sk_456","age":25}'));

CREATE ROLE data_admin;
CREATE ROLE data_reader;

CREATE MASKING POLICY mask_variant_sensitive
AS (val VARIANT) RETURNS VARIANT ->
CASE
  WHEN is_role_in_session('data_admin') OR is_role_in_session('account_admin') THEN val
  ELSE object_delete(val, 'content', 'secret_key')
END;

ALTER TABLE events MODIFY COLUMN data SET MASKING POLICY mask_variant_sensitive;

GRANT SELECT ON default.events TO ROLE data_admin;
GRANT SELECT ON default.events TO ROLE data_reader;
```

| 作为 `data_admin` | 作为 `data_reader` |
|-----------------|------------------|
| 完整 JSON | 移除 `content` / `secret_key` |

```sql
SET ROLE data_reader;

SELECT data FROM events;
-- {"age":30,"name":"alice"}

SELECT data['content'] FROM events;                 -- NULL
SELECT data['name'] FROM events;                    -- "alice"
SELECT json_path_query_first(data, '$.content');    -- NULL
SELECT data::STRING FROM events;                    -- {"age":30,"name":"alice"}
SELECT json_object_keys(data) FROM events;          -- ["age","name"]
SELECT * FROM events WHERE data['content'] IS NOT NULL;
-- empty
```

嵌套键：

```sql
ELSE delete_by_keypath(val, 'nested:secret')
```

## 读 / 写行为 {#read-write-behavior}

| 操作 | 影响 |
|-----------|--------|
| `SELECT` | 脱敏后的值 |
| `INSERT` / `UPDATE` / `DELETE` | 真实值（写入不会被脱敏） |

```sql
INSERT INTO user_info VALUES (2, 'admin@example.com');  -- stores real email
SELECT * FROM user_info WHERE id = 2;                   -- returns *********
```

## 管理策略 {#manage-policies}

```sql
DESCRIBE MASKING POLICY email_mask;

ALTER TABLE user_info MODIFY COLUMN email UNSET MASKING POLICY;
DROP MASKING POLICY IF EXISTS email_mask;
```

在执行 `DROP MASKING POLICY` 之前，先解除每一列上的绑定。你可以使用 `POLICY_REFERENCES(POLICY_NAME => 'email_mask')` 查找绑定关系。

## 脱敏与行访问 {#masking-vs-row-access}

| | 掩码策略 | 行访问策略 |
|---|---|---|
| 作用域 | 列值 | 整行 |
| 返回类型 | 必须与列类型匹配 | 始终为 BOOLEAN |
| 每表 | 每列一个 | 每表一个 |
| 影响 | `SELECT` | `SELECT`, `UPDATE`, `DELETE`, `MERGE` |

同一列不能同时拥有这两种策略。如果行应当保留可见但列值需要隐藏，请使用脱敏；如果整行都应消失，请使用行访问策略。

## 限制 {#limits}

- 每列只能有一个脱敏策略
- 返回类型必须与列类型匹配
- 在修改或删除列之前，必须先取消设置策略
- 仍被任何表引用的策略不能被删除
- 不支持 `CREATE OR REPLACE MASKING POLICY` — 需要先删除再重新创建
- 临时表、视图和 stream 不支持
- 脱敏策略和行访问策略的名称在全局范围内必须唯一
- 策略参数名在创建时会被转换为小写

## 最佳实践 {#best-practices}

1. 优先使用 `is_role_in_session()`，而不是 `current_role()`。
2. 保持 `USING` 最小化 —— 只包含策略体所需的列。
3. 如果应用会调用 `LENGTH` / `LIKE`，请返回与类型一致的占位值（例如 email 使用 `***@***.com`）。
4. 对于 VARIANT，优先使用 `object_delete` / `delete_by_keypath`，而不是对整个值进行脱敏。
5. 删除前先解除绑定；附加策略后，使用受限角色进行验证。

## 权限与参考 {#privileges-references}

- 在 `*.*` 上具有 `CREATE MASKING POLICY` 权限以创建策略（创建者会获得 OWNERSHIP）
- 具有全局 `APPLY MASKING POLICY` 或 `APPLY ON MASKING POLICY <name>` 权限以进行附加/分离
- 审计：`SHOW GRANTS ON MASKING POLICY <name>`

另请参阅：

- [用户与角色](/tidb-cloud-lake/sql/user-role.md)
- [CREATE MASKING POLICY](/tidb-cloud-lake/sql/create-masking-policy.md)
- [ALTER TABLE](/tidb-cloud-lake/sql/alter-table.md#column-operations)
- [脱敏策略命令](/tidb-cloud-lake/sql/masking-policy-sql.md)
- [行访问策略](/tidb-cloud-lake/guides/row-access-policy.md)