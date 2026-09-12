---
title: DROP MASKING POLICY
summary: 从 {{{ .lake }}} 中删除现有的 masking policy。删除 masking policy 后，它会从 {{{ .lake }}} 中移除，并且与其关联的 masking 规则将不再生效。请注意，在删除 masking policy 之前，请确保该策略未与任何列关联。
---

# DROP MASKING POLICY

从 {{{ .lake }}} 中删除现有的 masking policy。删除 masking policy 后，它会从 {{{ .lake }}} 中移除，并且与其关联的 masking 规则将不再生效。请注意，在删除 masking policy 之前，请确保该策略未与任何列关联。

## 语法 {#syntax}

```sql
DROP MASKING POLICY [ IF EXISTS ] <policy_name>
```

## 访问控制要求 {#access-control-requirements}

| 权限 | 描述 |
|:----------|:------------|
| APPLY MASKING POLICY | 删除 masking policy 所需的权限，除非你拥有该策略。 |

你必须具有全局 `APPLY MASKING POLICY` 权限，或者对目标策略具有 APPLY/OWNERSHIP。删除策略后，{{{ .lake }}} 会自动从创建者角色回收 OWNERSHIP。

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

DROP MASKING POLICY email_mask;
```