---
title: DESC CONNECTION
summary: 特定の接続の詳細を記述し、そのタイプと設定に関する情報を提供します。
---

# DESC CONNECTION

特定の接続の詳細を記述し、そのタイプと設定に関する情報を提供します。

## 構文 {#syntax}

```sql
DESC CONNECTION <connection_name>
```

## 例 {#examples}

```sql
DESC CONNECTION toronto;

┌────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│   name  │ storage_type │                                         storage_params                            │
├─────────┼──────────────┼───────────────────────────────────────────────────────────────────────────────────┤
│ toronto │ s3           │ access_key_id=<your-secret-access-key> secret_access_key=<your-secret-access-key> │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```