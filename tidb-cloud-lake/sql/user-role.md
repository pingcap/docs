---
title: 用户与角色
summary: 本页按功能分类，全面概述了 {{{ .lake }}} 中的用户和角色操作，便于快速查阅。
---

# 用户与角色

本页按功能分类，全面概述了 {{{ .lake }}} 中的用户和角色操作，便于快速查阅。

## 用户管理 {#user-management}

| Command | 描述 |
|---------|-------------|
| [CREATE USER](/tidb-cloud-lake/sql/create-user.md) | 创建新的用户账户 |
| [ALTER USER](/tidb-cloud-lake/sql/alter-user.md) | 修改现有用户账户 |
| [DROP USER](/tidb-cloud-lake/sql/drop-user.md) | 删除用户账户 |
| [DESC USER](/tidb-cloud-lake/sql/desc-user.md) | 显示用户的详细信息 |
| [SHOW USERS](/tidb-cloud-lake/sql/show-users.md) | 列出系统中的所有用户 |

## 角色管理 {#role-management}

| Command | 描述 |
|---------|-------------|
| [CREATE ROLE](/tidb-cloud-lake/sql/create-role.md) | 创建新角色 |
| [DROP ROLE](/tidb-cloud-lake/sql/drop-role.md) | 删除角色 |
| [SET ROLE](/tidb-cloud-lake/sql/set-role.md) | 为当前会话设置活动角色 |
| [SET SECONDARY ROLES](/tidb-cloud-lake/sql/set-secondary-roles.md) | 为会话设置次要角色 |
| [SHOW ROLES](/tidb-cloud-lake/sql/show-roles.md) | 列出系统中的所有角色 |

## 权限管理 {#privilege-management}

| Command | 描述 |
|---------|-------------|
| [GRANT](/tidb-cloud-lake/sql/grant.md) | 向角色授予权限 |
| [REVOKE](/tidb-cloud-lake/sql/revoke.md) | 从角色中移除权限 |
| [SHOW GRANTS](/tidb-cloud-lake/sql/show-grants.md) | 显示角色授权和角色分配信息 |

> **注意：**
>
> 正确管理用户和角色对于数据库安全至关重要。授予权限时，请始终遵循最小权限原则。