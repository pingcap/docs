---
title: SHOW USER FUNCTIONS
summary: 列出系统中现有的用户定义函数和外部函数。等价于 `SELECT name, is_aggregate, description, arguments, language FROM system.user_functions....`
---

# SHOW USER FUNCTIONS

列出系统中现有的用户定义函数和外部函数。等价于 `SELECT name, is_aggregate, description, arguments, language FROM system.user_functions ...`。

另请参阅：[system.user_functions](/tidb-cloud-lake/sql/system-user-functions.md)

## 语法 {#syntax}

```sql
SHOW USER FUNCTIONS [LIKE '<pattern>' | WHERE <expr>] | [LIMIT <limit>]
```

## 示例 {#example}

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