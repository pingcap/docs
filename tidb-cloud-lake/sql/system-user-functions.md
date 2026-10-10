---
title: system.user_functions
summary: システム内のユーザー定義関数および外部関数に関する情報を含みます。
---

# system.user_functions

システム内のユーザー定義関数および外部関数に関する情報を含みます。

関連情報: [SHOW USER FUNCTIONS](/tidb-cloud-lake/sql/show-user-functions.md)。

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