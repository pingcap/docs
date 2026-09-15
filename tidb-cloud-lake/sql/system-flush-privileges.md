---
title: SYSTEM FLUSH PRIVILEGES
summary: 向所有查询节点广播权限元信息刷新请求，使 GRANT 和 REVOKE 的更改立即生效。
---

# SYSTEM FLUSH PRIVILEGES

`SYSTEM FLUSH PRIVILEGES` 会向每个查询节点广播刷新请求，使每个节点立即从 Meta service 重新加载权限和角色元信息。当你需要在整个集群范围内让更改生效，而不想等待默认 15 秒的角色缓存间隔时，请在执行 `GRANT` 或 `REVOKE` 语句后运行此命令。

另请参阅：

- [GRANT](/tidb-cloud-lake/sql/grant.md)
- [REVOKE](/tidb-cloud-lake/sql/revoke.md)

## 语法 {#syntax}

```sql
SYSTEM FLUSH PRIVILEGES
```

## 使用说明 {#usage-notes}

- 需要具备允许执行系统管理命令的角色，例如 `ACCOUNT ADMIN`。
- 仅刷新已缓存的权限元信息；它本身不会修改角色或授权。
- 已经在运行的语句会继续使用其启动时解析得到的权限。刷新后，请重新运行该语句以获取这些更改。

## 示例 {#example}

以下顺序会为某个角色授予数据库访问权限，并立即刷新缓存，使新权限对每个查询节点都可见：

```sql
GRANT SELECT ON DATABASE marketing TO ROLE analyst;

SYSTEM FLUSH PRIVILEGES;
```

刷新完成后，任何在 `analyst` 角色下运行的新查询都会收到已更新的权限集，而无需等待缓存过期。