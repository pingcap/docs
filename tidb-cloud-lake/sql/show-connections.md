---
title: SHOW CONNECTIONS
summary: 利用可能なすべての接続の一覧を表示します。
---

# SHOW CONNECTIONS

利用可能なすべての接続の一覧を表示します。

## 構文 {#syntax}

```sql
SHOW CONNECTIONS
```

## 例 {#examples}

```sql
SHOW CONNECTIONS;

┌────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│   name  │ storage_type │                                         storage_params                            │
├─────────┼──────────────┼───────────────────────────────────────────────────────────────────────────────────┤
│ toronto │ s3           │ access_key_id=<your-secret-access-key> secret_access_key=<your-secret-access-key> │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```