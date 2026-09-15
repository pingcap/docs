---
title: SHOW CONNECTIONS
summary: 显示所有可用连接的列表。
---

# SHOW CONNECTIONS

显示所有可用连接的列表。

## 语法 {#syntax}

```sql
SHOW CONNECTIONS
```

## 示例 {#examples}

```sql
SHOW CONNECTIONS;

┌────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│   name  │ storage_type │                                         storage_params                            │
├─────────┼──────────────┼───────────────────────────────────────────────────────────────────────────────────┤
│ toronto │ s3           │ access_key_id=<your-secret-access-key> secret_access_key=<your-secret-access-key> │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```