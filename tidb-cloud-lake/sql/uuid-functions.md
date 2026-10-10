---
title: UUID 関数
summary: このページでは、{{{ .lake }}} の UUID 関連の関数に関するリファレンス情報を提供します。これらの関数は、Universally Unique Identifier (UUID) を生成し、操作するためのものです。
---

# UUID 関数

このページでは、{{{ .lake }}} の UUID 関連の関数に関するリファレンス情報を提供します。これらの関数は、Universally Unique Identifier (UUID) を生成し、操作するためのものです。

## UUID 生成関数 {#uuid-generation-functions}

| 関数 | 説明 | 例 |
|----------|-------------|--------|
| [GEN_RANDOM_UUID](/tidb-cloud-lake/sql/gen-random-uuid.md) | ランダムな UUID を生成します（v1.2.658 以降ではバージョン 7、それ以前ではバージョン 4） | `GEN_RANDOM_UUID()` → `'01890a5d-ac96-7cc6-8128-01d71ab8b93e'` |
| [UUID](/tidb-cloud-lake/sql/uuid-sql.md) | GEN_RANDOM_UUID のエイリアス | `UUID()` → `'01890a5d-ac96-7cc6-8128-01d71ab8b93e'` |

## 使用例 {#usage-examples}

### 主キーの生成 {#generating-primary-keys}

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

### 分散システム向けの一意識別子の作成 {#creating-unique-identifiers-for-distributed-systems}

```sql
-- Generate multiple UUIDs for distributed event tracking
SELECT
  GEN_RANDOM_UUID() AS event_id,
  'user_login' AS event_type,
  NOW() AS event_time
FROM numbers(5);
```

### UUID バージョン情報 {#uuid-version-information}

{{{ .lake }}} の UUID 実装は進化してきました。

- **Version 1.2.658 and later**: UUID バージョン 7 を使用します。これには時系列順のソートのためのタイムスタンプ情報が含まれます
- **Prior to version 1.2.658**: UUID バージョン 4 を使用しており、完全にランダムでした