---
title: QUERY WATCH
summary: TiDBデータベースにおけるQUERY WATCHの使用方法の概要。
---

# クエリウォッチ {#query-watch}

`QUERY WATCH`ステートメントは、リソース グループ内の暴走クエリの監視リストを手動で管理するために使用されます。

> **注記：**
>
> この機能は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)インスタンスではご利用いただけません。

## あらすじ {#synopsis}

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

## パラメータ {#parameters}

[`QUERY WATCH`パラメータ](/tidb-resource-control-runaway-queries.md#query-watch-parameters)を参照してください。

## MySQLとの互換性 {#mysql-compatibility}

このステートメントは、MySQL構文に対するTiDBの拡張機能です。

## 関連項目 {#see-also}

-   [暴走クエリ](/tidb-resource-control-runaway-queries.md)
