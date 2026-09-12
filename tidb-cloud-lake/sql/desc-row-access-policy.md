---
title: DESC ROW ACCESS POLICY
summary: "显示 {{{ .lake }}} 中特定行访问策略的详细信息。"
---

# DESC ROW ACCESS POLICY

显示 {{{ .lake }}} 中特定行访问策略的详细信息。

## 语法 {#syntax}

```sql
DESC ROW ACCESS POLICY <policy_name>
```

也支持 `DESCRIBE ROW ACCESS POLICY`。

## 访问控制要求 {#access-control-requirements}

| 权限 | 描述 |
|:----------|:------------|
| APPLY ROW ACCESS POLICY | 描述行访问策略时需要此权限，除非你是该策略的所有者。 |

满足以下任一条件即可：具有全局 `APPLY ROW ACCESS POLICY` 权限，或对特定行访问策略具有 APPLY/OWNERSHIP。

## 示例 {#examples}

```sql
SET enable_experimental_row_access_policy = 1;

CREATE ROW ACCESS POLICY rap_engineering
AS (dept STRING)
RETURNS BOOLEAN ->
  CASE
    WHEN current_role() = 'admin' THEN true
    WHEN dept = 'Engineering' THEN true
    ELSE false
  END
  COMMENT = 'show engineering rows';

DESC ROW ACCESS POLICY rap_engineering;

Name            | Created On                  | Signature     | Return Type | Body                                                       | Comment
----------------+-----------------------------+---------------+-------------+------------------------------------------------------------+----------------------
rap_engineering | 2026-05-15 08:42:10.949 UTC | (dept STRING) | BOOLEAN     | CASE WHEN current_role() = 'admin' THEN true WHEN...       | show engineering rows
```