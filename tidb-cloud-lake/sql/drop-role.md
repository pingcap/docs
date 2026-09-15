---
title: DROP ROLE
summary: 从系统中移除指定的角色。
---

# DROP ROLE

从系统中移除指定的角色。

## 语法 {#syntax}

```sql
DROP ROLE [ IF EXISTS ] <role_name>
```

## 使用说明 {#usage-notes}

* 如果某个角色已授予给用户，{{{ .lake }}} 无法自动删除该角色上的授权。

## 示例 {#examples}

```sql
DROP ROLE role1;
```