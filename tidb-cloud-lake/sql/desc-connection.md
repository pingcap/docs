---
title: DESC CONNECTION
summary: 描述特定连接的详细信息，提供其类型和配置相关的信息。
---

# DESC CONNECTION

描述特定连接的详细信息，提供其类型和配置相关的信息。

## 语法 {#syntax}

```sql
DESC CONNECTION <connection_name>
```

## 示例 {#examples}

```sql
DESC CONNECTION toronto;

┌────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│   name  │ storage_type │                                         storage_params                            │
├─────────┼──────────────┼───────────────────────────────────────────────────────────────────────────────────┤
│ toronto │ s3           │ access_key_id=<your-secret-access-key> secret_access_key=<your-secret-access-key> │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```