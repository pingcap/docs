---
title: system.user_functions
summary: 包含系统中用户定义函数和外部函数的信息。
---

# system.user_functions

包含系统中用户定义函数和外部函数的信息。

另请参阅：[SHOW USER FUNCTIONS](/tidb-cloud-lake/sql/show-user-functions.md)。

```sql
SELECT * FROM system.user_functions;

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│      name      │    is_aggregate   │ description │                         arguments                         │ language │                                                 definition                                                │
├────────────────┼───────────────────┼─────────────┼───────────────────────────────────────────────────────────┼──────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ binary_reverse │ NULL              │             │ {"arg_types":["Binary NULL"],"return_type":"Binary NULL"} │ python   │  (Binary NULL) RETURNS Binary NULL LANGUAGE python HANDLER = binary_reverse ADDRESS = http://0.0.0.0:8815 │
│ echo           │ NULL              │             │ {"arg_types":["String NULL"],"return_type":"String NULL"} │ python   │  (String NULL) RETURNS String NULL LANGUAGE python HANDLER = echo ADDRESS = http://0.0.0.0:8815           │
│ isnotempty     │ NULL              │             │ {"parameters":["p"]}                                      │ SQL      │  (p) -> (NOT is_null(p))                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```