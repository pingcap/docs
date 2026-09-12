---
title: SHOW VIEWS
summary: 返回指定数据库中的视图名称列表；如果未提供数据库名称，则返回当前数据库中的视图名称列表。
---

# SHOW VIEWS

返回指定数据库中的视图名称列表；如果未提供数据库名称，则返回当前数据库中的视图名称列表。

## 语法 {#syntax}

```sql
SHOW [ FULL ] VIEWS
     [ { FROM | IN } <database_name> ]
     [ HISTORY ]
     [ LIKE '<pattern>' | WHERE <expr> ]
```

| 参数 | 描述 |
|-----------|----------------------------------------------------------------------------------------------|
| FULL      | 返回包含附加信息的结果。更多详情请参见[示例](#examples)。   |
| FROM / IN | 指定一个数据库。如果省略，则该命令返回当前数据库中的结果。 |
| HISTORY   | 显示保留时间内（默认 24 小时）被删除视图的时间戳。如果某个视图尚未被删除，则 `drop_time` 的值为 NULL。 |
| LIKE      | 使用带有 `%` 通配符的大小写敏感模式匹配来过滤视图名称。          |
| WHERE     | 使用 WHERE 子句中的表达式来过滤视图名称。                              |

## 示例 {#examples}

```sql
SHOW VIEWS;

┌───────────────────────────────────────────────────────────────────┐
│ Views_in_default │                   view_query                   │
├──────────────────┼────────────────────────────────────────────────┤
│ books_view       │ SELECT id, title, genre FROM default.books     │
│ users_view       │ SELECT username, email, age FROM default.users │
└───────────────────────────────────────────────────────────────────┘

SHOW FULL VIEWS;

┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│    views   │ database │ catalog │       owner      │ engine │         create_time        │                   view_query                   │
├────────────┼──────────┼─────────┼──────────────────┼────────┼────────────────────────────┼────────────────────────────────────────────────┤
│ books_view │ default  │ default │ NULL             │ VIEW   │ 2024-04-14 23:29:52.916989 │ SELECT id, title, genre FROM default.books     │
│ users_view │ default  │ default │ NULL             │ VIEW   │ 2024-04-14 23:31:02.918994 │ SELECT username, email, age FROM default.users │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

-- Delete the view 'books_view'
DROP VIEW books_view;

SHOW VIEWS HISTORY;

┌────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Views_in_default │                   view_query                   │          drop_time         │
├──────────────────┼────────────────────────────────────────────────┼────────────────────────────┤
│ books_view       │ SELECT id, title, genre FROM default.books     │ 2024-04-15 02:29:56.051081 │
│ users_view       │ SELECT username, email, age FROM default.users │ NULL                       │
└────────────────────────────────────────────────────────────────────────────────────────────────┘
```