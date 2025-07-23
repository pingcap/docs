---
title: ALTER INSTANCE
summary: 了解 TiDB 中 `ALTER INSTANCE` 的用法概述。
---

# ALTER INSTANCE

`ALTER INSTANCE` 语句用于对单个 TiDB 实例进行更改。目前，TiDB 仅支持 `RELOAD TLS` 子句。

> **Note:**
>
> [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 可以自动刷新 TLS 证书，因此此功能不适用于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群。

## RELOAD TLS

<CustomContent platform="tidb">

你可以执行 `ALTER INSTANCE RELOAD TLS` 语句，从原始配置路径重新加载证书 ([`ssl-cert`](/tidb-configuration-file.md#ssl-cert))、密钥 ([`ssl-key`](/tidb-configuration-file.md#ssl-key)) 和 CA ([`ssl-ca`](/tidb-configuration-file.md#ssl-ca))。

</CustomContent>

<CustomContent platform="tidb-cloud">

你可以执行 `ALTER INSTANCE RELOAD TLS` 语句，从原始配置路径重新加载证书 ([`ssl-cert`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#ssl-cert))、密钥 ([`ssl-key`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#ssl-key)) 和 CA ([`ssl-ca`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#ssl-ca))。

</CustomContent>

新加载的证书、密钥和 CA 在成功执行该语句后建立的连接中生效。执行该语句之前建立的连接不受影响。

当重新加载过程中发生错误时，默认会返回该错误信息，之前的密钥和证书仍然继续使用。但是，如果你添加了可选的 `NO ROLLBACK ON ERROR`，在重新加载过程中发生错误时，错误不会被返回，后续请求将以禁用 TLS 安全连接的方式处理。

## 语法示意图

**AlterInstanceStmt:**

```ebnf+diagram
AlterInstanceStmt ::=
    'ALTER' 'INSTANCE' InstanceOption

InstanceOption ::=
    'RELOAD' 'TLS' ('NO' 'ROLLBACK' 'ON' 'ERROR')?
```

## 示例

```sql
ALTER INSTANCE RELOAD TLS;
```

## MySQL 兼容性

`ALTER INSTANCE RELOAD TLS` 语句仅支持从原始配置路径重新加载。它不支持在 TiDB 启动时动态修改加载路径或动态启用 TLS 加密连接功能。此功能在重启 TiDB 时默认是禁用的。

## 相关链接

<CustomContent platform="tidb">

[Enable TLS Between TiDB Clients and Servers](/enable-tls-between-clients-and-servers.md).

</CustomContent>

<CustomContent platform="tidb-cloud">

[Enable TLS Between TiDB Clients and Servers](https://docs.pingcap.com/tidb/stable/enable-tls-between-clients-and-servers).

</CustomContent>