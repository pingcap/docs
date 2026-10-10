---
title: SHOW USER FUNCTIONS
summary: システム内に存在するユーザー定義関数および外部関数を一覧表示します。`SELECT name, is_aggregate, description, arguments, language FROM system.user_functions....` と同等です。
---

# SHOW USER FUNCTIONS

システム内に存在するユーザー定義関数および外部関数を一覧表示します。`SELECT name, is_aggregate, description, arguments, language FROM system.user_functions ...` と同等です。

関連情報: [system.user_functions](/tidb-cloud-lake/sql/system-user-functions.md)

## 構文 {#syntax}

```sql
SHOW USER FUNCTIONS [LIKE '<pattern>' | WHERE <expr>] | [LIMIT <limit>]
```

## 例 {#example}

```sql
SHOW USER FUNCTIONS;

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│      name      │    is_aggregate   │ description │                         arguments                         │ language │
├────────────────┼───────────────────┼─────────────┼───────────────────────────────────────────────────────────┼──────────┤
│ binary_reverse │ NULL              │             │ {"arg_types":["Binary NULL"],"return_type":"Binary NULL"} │ python   │
│ echo           │ NULL              │             │ {"arg_types":["String NULL"],"return_type":"String NULL"} │ python   │
│ isnotempty     │ NULL              │             │ {"parameters":["p"]}                                      │ SQL      │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```