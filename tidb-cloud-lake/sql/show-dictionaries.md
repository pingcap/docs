---
title: SHOW DICTIONARIES
summary: 現在または指定したデータベース内のディクショナリを一覧表示します。
---

# SHOW DICTIONARIES

現在または指定したデータベース内のディクショナリを一覧表示します。

## 構文 {#syntax}

```sql
SHOW DICTIONARIES [ FROM <database_name> | IN <database_name> ]
    [ LIMIT <limit> ]
    [ LIKE '<pattern>' | WHERE <expr> ]
```

## パラメータ {#parameters}

| パラメータ | 説明 |
|-----------|-------------|
| `FROM <database_name>` / `IN <database_name>` | 任意。指定したデータベースのディクショナリを一覧表示します。 |
| `LIMIT <limit>` | 任意。返される行数を制限します。 |
| `LIKE '<pattern>'` | 任意。パターンに基づいてディクショナリ名を絞り込みます。 |
| `WHERE <expr>` | 任意。式を使用して結果セットを絞り込みます。 |

## 例 {#examples}

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