---
title: DESC MASKING POLICY
summary: 显示 {{{ .lake }}} 中特定 masking policy 的详细信息。
---

# DESC MASKING POLICY

显示 {{{ .lake }}} 中特定 masking policy 的详细信息。

## 语法 {#syntax}

```sql
DESC MASKING POLICY <policy_name>
```

## 访问控制要求 {#access-control-requirements}

| 权限 | 描述 |
|:----------|:------------|
| APPLY MASKING POLICY | 描述 masking policy 所必需的权限，除非你是该 policy 的所有者。 |

满足此要求的条件包括：拥有全局 `APPLY MASKING POLICY` 权限，或者对特定 masking policy 拥有 APPLY/OWNERSHIP。

## 示例 {#examples}

```sql
CREATE MASKING POLICY email_mask
AS
  (val string)
  RETURNS string ->
  CASE
  WHEN current_role() IN ('MANAGERS') THEN
    val
  ELSE
    '*********'
  END
  COMMENT = 'hide_email';

DESC MASKING POLICY email_mask;

Name       |Value                                                                |
-----------+---------------------------------------------------------------------+
Name       |email_mask                                                           |
Created On |2023-08-09 02:29:16.177898 UTC                                       |
Signature  |(val STRING)                                                         |
Return Type|STRING                                                               |
Body       |CASE WHEN current_role() IN('MANAGERS') THEN VAL ELSE '*********' END|
Comment    |hide_email                                                           |
```