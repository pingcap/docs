---
title: SHOW DICTIONARIES
summary: 列出当前或指定数据库中的字典。
---

# SHOW DICTIONARIES

列出当前或指定数据库中的字典。

## 语法 {#syntax}

```sql
SHOW DICTIONARIES [ FROM <database_name> | IN <database_name> ]
    [ LIMIT <limit> ]
    [ LIKE '<pattern>' | WHERE <expr> ]
```

## 参数 {#parameters}

| 参数 | 描述 |
|-----------|-------------|
| `FROM <database_name>` / `IN <database_name>` | 可选。列出指定数据库中的字典。 |
| `LIMIT <limit>` | 可选。限制返回的行数。 |
| `LIKE '<pattern>'` | 可选。按模式过滤字典名称。 |
| `WHERE <expr>` | 可选。使用表达式过滤结果集。 |

## 示例 {#examples}

```sql
CREATE DICTIONARY user_info
(
    user_id UInt64,
    user_name String,
    user_email String
)
PRIMARY KEY user_id
SOURCE(
    mysql(
        host = '127.0.0.1'
        port = '3306'
        username = 'root'
        password = 'root'
        db = 'app'
        table = 'users'
    )
)
COMMENT 'User dictionary from MySQL';

CREATE DICTIONARY cache
(
    key String,
    value String
)
PRIMARY KEY key
SOURCE(
    redis(
        host = '127.0.0.1'
        port = '6379'
    )
)
COMMENT 'cache dictionary from Redis';

SHOW DICTIONARIES;
╭─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ database │ dictionary │   key_names   │         key_types        │       attribute_names      │         attribute_types         │                                          source                                         │           comment           │
│  String  │   String   │ Array(String) │       Array(String)      │        Array(String)       │          Array(String)          │                                          String                                         │            String           │
├──────────┼────────────┼───────────────┼──────────────────────────┼────────────────────────────┼─────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────┼─────────────────────────────┤
│ default  │ cache      │ ["key"]       │ ["VARCHAR NULL"]         │ ["value"]                  │ ["VARCHAR NULL"]                │ redis(host=127.0.0.1 port=6379)                                                         │ cache dictionary from Redis │
│ default  │ user_info  │ ["user_id"]   │ ["BIGINT UNSIGNED NULL"] │ ["user_name","user_email"] │ ["VARCHAR NULL","VARCHAR NULL"] │ mysql(db=app host=127.0.0.1 password=[hidden] port=3306 table=users username=root)      │ User dictionary from MySQL  │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```