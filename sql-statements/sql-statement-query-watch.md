---
title: QUERY WATCH
summary: QUERY WATCHステートメントは、リソースグループ内の暴走クエリの監視リストを手動で管理するために使用されます。この機能は実験的であり、本番環境での使用はお勧めできません。バグを見つけた場合は、GitHubで問題を報告できます。MySQLの互換性があり、TiDBの拡張機能です。QUERY WATCHパラメータを参照してください。暴走クエリの管理についても参照してください。
---

# クエリウォッチ {#query-watch}

`QUERY WATCH`ステートメントは、リソース グループ内の暴走クエリの監視リストを手動で管理するために使用されます。

> **警告：**
>
> この機能は実験的です。本番環境で使用することはお勧めできません。この機能は予告なく変更または削除される場合があります。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)を報告できます。

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

## パラメーター {#parameters}

[`QUERY WATCH`パラメータ](/tidb-resource-control.md#query-watch-parameters)を参照してください。

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張機能です。

## こちらも参照 {#see-also}

-   [暴走クエリ](/tidb-resource-control.md#manage-queries-that-consume-more-resources-than-expected-runaway-queries)
