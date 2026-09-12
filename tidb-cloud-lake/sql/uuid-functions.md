---
title: UUID 函数
summary: 本页提供 {{{ .lake }}} 中与 UUID 相关函数的参考信息。这些函数用于生成和处理通用唯一标识符（UUID）。
---

# UUID 函数

本页提供 {{{ .lake }}} 中与 UUID 相关函数的参考信息。这些函数用于生成和处理通用唯一标识符（UUID）。

## UUID 生成函数 {#uuid-generation-functions}

| 函数 | 描述 | 示例 |
|----------|-------------|--------|
| [GEN_RANDOM_UUID](/tidb-cloud-lake/sql/gen-random-uuid.md) | 生成一个随机 UUID（从 v1.2.658 起为版本 7，此前为版本 4） | `GEN_RANDOM_UUID()` → `'01890a5d-ac96-7cc6-8128-01d71ab8b93e'` |
| [UUID](/tidb-cloud-lake/sql/uuid-sql.md) | GEN_RANDOM_UUID 的别名 | `UUID()` → `'01890a5d-ac96-7cc6-8128-01d71ab8b93e'` |

## 使用示例 {#usage-examples}

### 生成主键 {#generating-primary-keys}

```sql
-- Create a table with UUID primary key
CREATE TABLE users (
  id UUID DEFAULT GEN_RANDOM_UUID(),
  username VARCHAR,
  email VARCHAR,
  PRIMARY KEY(id)
);

-- Insert data without specifying UUID
INSERT INTO users (username, email)
VALUES ('johndoe', 'john@example.com');

-- Query to see the auto-generated UUID
SELECT * FROM users;
```

### 为分布式系统创建唯一标识符 {#creating-unique-identifiers-for-distributed-systems}

```sql
-- Generate multiple UUIDs for distributed event tracking
SELECT
  GEN_RANDOM_UUID() AS event_id,
  'user_login' AS event_type,
  NOW() AS event_time
FROM numbers(5);
```

### UUID 版本信息 {#uuid-version-information}

{{{ .lake }}} 的 UUID 实现已经演进：

- **Version 1.2.658 and later**: 使用 UUID 版本 7，其中包含时间戳信息，便于按时间顺序排序
- **Prior to version 1.2.658**: 使用 UUID 版本 4，它是纯随机生成的