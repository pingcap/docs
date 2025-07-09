---
title: QUERY WATCH
summary: 关于在 TiDB 数据库中使用 QUERY WATCH 的概述。
---

# QUERY WATCH

`QUERY WATCH` 语句用于手动管理资源组中失控查询的监控列表。

> **Note:**
>
> 该功能在 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群上不可用。

## Synopsis

```ebnf+diagram
AddQueryWatchStmt ::=
    "QUERY" "WATCH" "ADD" QueryWatchOptionList
QueryWatchOptionList ::=
    QueryWatchOption
|   QueryWatchOptionList QueryWatchOption
|   QueryWatchOptionList ',' QueryWatchOption
QueryWatchOption ::=
    "RESOURCE" "GROUP" ResourceGroupName
|   "RESOURCE" "GROUP" UserVariable
|   "ACTION" EqOpt ResourceGroupRunawayActionOption
|   QueryWatchTextOption
ResourceGroupName ::=
    Identifier
|   "DEFAULT"
QueryWatchTextOption ::=
    "SQL" "DIGEST" SimpleExpr
|   "PLAN" "DIGEST" SimpleExpr
|   "SQL" "TEXT" ResourceGroupRunawayWatchOption "TO" SimpleExpr

ResourceGroupRunawayWatchOption ::=
    "EXACT"
|   "SIMILAR"
|   "PLAN"

DropQueryWatchStmt ::=
    "QUERY" "WATCH" "REMOVE" NUM
```

## Parameters

请参见 [`QUERY WATCH` parameters](/tidb-resource-control.md#query-watch-parameters)。

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 相关链接

* [Runaway Queries](/tidb-resource-control.md#manage-queries-that-consume-more-resources-than-expected-runaway-queries)