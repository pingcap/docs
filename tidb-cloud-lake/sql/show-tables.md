---
title: SHOW TABLES
summary: 列出当前数据库或指定数据库中的表。
---

# SHOW TABLES

列出当前数据库或指定数据库中的表。

> **Note:**
>
> 从 1.2.415 版本开始，SHOW TABLES 命令的结果中不再包含视图。要显示视图，请改用 [SHOW VIEWS](/tidb-cloud-lake/sql/show-views.md)。

另请参阅：[system.tables](/tidb-cloud-lake/sql/system-tables.md)

## 语法 {#syntax}

```sql
SHOW [ FULL ] TABLES
     [ {FROM | IN} <database_name> ]
     [ HISTORY ]
     [ LIKE '<pattern>' | WHERE <expr> ]
```

| 参数 | 描述 |
|-----------|-----------------------------------------------------------------------------------------------------------------------------|
| FULL      | 列出结果并附带额外信息。更多详情请参见[示例](#examples)。                                  |
| FROM / IN | 指定数据库。如果省略，该命令返回当前数据库中的结果。                                |
| HISTORY   | 显示保留时间内（默认 24 小时）被删除表的时间戳。如果某个表尚未被删除，则 `drop_time` 的值为 NULL。 |
| LIKE      | 使用大小写敏感的模式匹配按名称过滤结果。                                                   |
| WHERE     | 使用 WHERE 子句中的表达式过滤结果。                                                                |

## 示例 {#examples}

以下示例列出当前数据库（默认）的所有表名：

```sql
SHOW TABLES;

┌───────────────────┐
│ Tables_in_default │
├───────────────────┤
│ books             │
│ mytable           │
│ ontime            │
│ products          │
└───────────────────┘
```

以下示例列出所有表及其附加信息：

```sql
SHOW FULL TABLES;

┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  tables  │ table_type │ database │ catalog │       owner      │ engine │ cluster_by │         create_time        │     num_rows     │     data_size    │ data_compressed_size │    index_size    │
├──────────┼────────────┼──────────┼─────────┼──────────────────┼────────┼────────────┼────────────────────────────┼──────────────────┼──────────────────┼──────────────────────┼──────────────────┤
│ books    │ BASE TABLE │ default  │ default │ account_admin    │ FUSE   │            │ 2024-01-16 03:53:15.354132 │                0 │                0 │                    0 │                0 │
│ mytable  │ BASE TABLE │ default  │ default │ account_admin    │ FUSE   │            │ 2024-01-16 03:53:27.968505 │                0 │                0 │                    0 │                0 │
│ ontime   │ BASE TABLE │ default  │ default │ account_admin    │ FUSE   │            │ 2024-01-16 03:53:42.052399 │                0 │                0 │                    0 │                0 │
│ products │ BASE TABLE │ default  │ default │ account_admin    │ FUSE   │            │ 2024-01-16 03:54:00.883985 │                0 │                0 │                    0 │                0 │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

以下示例演示了当存在可选参数 HISTORY 时，结果将包含已删除的表：

```sql
DROP TABLE products;

SHOW TABLES;

┌───────────────────┐
│ Tables_in_default │
├───────────────────┤
│ books             │
│ mytable           │
│ ontime            │
└───────────────────┘

SHOW TABLES HISTORY;

┌────────────────────────────────────────────────┐
│ Tables_in_default │          drop_time         │
├───────────────────┼────────────────────────────┤
│ books             │ NULL                       │
│ mytable           │ NULL                       │
│ ontime            │ NULL                       │
│ products          │ 2024-01-16 03:55:47.900362 │
└────────────────────────────────────────────────┘
```

以下示例列出名称以字符串 "time" 结尾的表：

```sql
SHOW TABLES LIKE '%time';

┌───────────────────┐
│ Tables_in_default │
├───────────────────┤
│ ontime            │
└───────────────────┘

-- CASE-SENSITIVE pattern matching.
-- No results will be returned if you code the previous statement like this:
SHOW TABLES LIKE '%TIME';
```

以下示例列出数据大小大于 1,000 字节的表：

```sql
SHOW TABLES WHERE data_size > 1000 ;

┌───────────────────┐
│ Tables_in_default │
├───────────────────┤
│ ontime            │
└───────────────────┘
```