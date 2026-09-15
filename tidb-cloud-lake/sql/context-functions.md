---
title: 上下文函数
summary: 本页提供 {{{ .lake }}} 中与上下文相关的函数参考信息。这些函数返回当前会话、数据库或系统上下文的信息。
---

# 上下文函数

本页提供 {{{ .lake }}} 中与上下文相关的函数参考信息。这些函数返回当前会话、数据库或系统上下文的信息。

## 会话信息函数 {#session-information-functions}

| 函数 | 描述 | 示例 |
|----------|-------------|--------|
| [CONNECTION_ID](/tidb-cloud-lake/sql/connection-id.md) | 返回当前连接的连接 ID | `CONNECTION_ID()` → `42` |
| [CURRENT_USER](/tidb-cloud-lake/sql/current-user.md) | 返回当前连接的用户名和主机 | `CURRENT_USER()` → `'root'@'%'` |
| [LAST_QUERY_ID](/tidb-cloud-lake/sql/last-query-id.md) | 返回上一次执行的查询的查询 ID | `LAST_QUERY_ID()` → `'01890a5d-ac96-7cc6-8128-01d71ab8b93e'` |

## 数据库上下文函数 {#database-context-functions}

| 函数 | 描述 | 示例 |
|----------|-------------|--------|
| [CURRENT_CATALOG](/tidb-cloud-lake/sql/current-catalog.md) | 返回当前 catalog 的名称 | `CURRENT_CATALOG()` → `'default'` |
| [DATABASE](/tidb-cloud-lake/sql/database-function.md) | 返回当前数据库的名称 | `DATABASE()` → `'default'` |

## 系统信息函数 {#system-information-functions}

| 函数 | 描述 | 示例 |
|----------|-------------|--------|
| [VERSION](/tidb-cloud-lake/sql/version.md) | 返回 {{{ .lake }}} 的当前版本 | `VERSION()` → `'LakeQuery v1.2.252-nightly-193ed56304'` |