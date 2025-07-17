---
title: SHOW PROFILES
summary: 关于 TiDB 数据库中使用 SHOW PROFILES 的概述。
---

# SHOW PROFILES

`SHOW PROFILES` 语句目前只返回空结果。

## 概述

```ebnf+diagram
ShowProfilesStmt ::=
    "SHOW" "PROFILES" ShowLikeOrWhere?

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## 示例

```sql
SHOW PROFILES;
```

```
Empty set (0.00 sec)
```

## MySQL 兼容性

此语句仅为兼容 MySQL 而包含。执行 `SHOW PROFILES` 始终返回空结果。

作为替代方案，TiDB 提供 [statement summary tables](/statement-summary-tables.md) 来帮助理解 SQL 性能问题。