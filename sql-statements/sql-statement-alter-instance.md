---
title: ALTER INSTANCE
summary: 了解 TiDB 中 `ALTER INSTANCE` 的用法概述。
---

# ALTER INSTANCE

`ALTER INSTANCE` 语句用于对单个 TiDB 实例进行更改。目前，TiDB 仅支持 `RELOAD TLS` 子句。

> **Note:**
>
> [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 和 [Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 可以自动刷新 TLS 证书，因此该功能不适用于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 和 [Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 集群。

## RELOAD TLS

<CustomContent platform="tidb">

你可以执行 `ALTER INSTANCE RELOAD TLS` 语句，从原有的配置路径重新加载证书（[`ssl-cert`](/tidb-configuration-file.md#ssl-cert)）、密钥（[`ssl-key`](/tidb-configuration-file.md#ssl-key)）和 CA（[`ssl-ca`](/tidb-configuration-file.md#ssl-ca)）。

</CustomContent>

<CustomContent platform="tidb-cloud">

你可以执行 `ALTER INSTANCE RELOAD TLS` 语句，从原有的配置路径重新加载证书（[`ssl-cert`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#ssl-cert)）、密钥（[`ssl-key`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#ssl-key)）和 CA（[`ssl-ca`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#ssl-ca)）。

</CustomContent>

新加载的证书、密钥和 CA 会在该语句成功执行后建立的新连接中生效。在此语句执行前已建立的连接不受影响。

当在重新加载过程中发生错误时，默认会返回该错误信息，并继续使用之前的密钥和证书。但是，如果你添加了可选的 `NO ROLLBACK ON ERROR`，当重新加载过程中发生错误时，将不会返回错误，后续的请求将以禁用 TLS 安全连接的方式处理。

## 语法图

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

`ALTER INSTANCE RELOAD TLS` 语句仅支持从原有的配置路径重新加载。不支持动态修改加载路径，也不支持在 TiDB 启动时动态启用 TLS 加密连接功能。该功能在重启 TiDB 时默认处于禁用状态。

## 另请参阅

<CustomContent platform="tidb">

[启用 TiDB 客户端与服务器之间的 TLS](/enable-tls-between-clients-and-servers.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

[启用 TiDB 客户端与服务器之间的 TLS](https://docs.pingcap.com/tidb/stable/enable-tls-between-clients-and-servers)。

</CustomContent>