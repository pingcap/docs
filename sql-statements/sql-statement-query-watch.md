---
title: QUERY WATCH
summary: TiDB 数据库中 QUERY WATCH 的用法概述。
---

# QUERY WATCH

`QUERY WATCH` 语句用于手动管理资源组中失控查询的监控列表。

> **Note:**
>
> 此功能在 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 集群中不可用。

## 语法

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

ResourceGroupRunawayActionOption ::=
    DRYRUN
|   COOLDOWN
|   KILL
|   "SWITCH_GROUP" '(' ResourceGroupName ')'

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

## 参数

参见 [`QUERY WATCH` 参数](/tidb-resource-control-runaway-queries.md#query-watch-parameters)。

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [Runaway Queries](/tidb-resource-control-runaway-queries.md)