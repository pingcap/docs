---
title: SHOW DICTIONARIES
summary: Lists dictionaries in the current or specified database.
---

# SHOW DICTIONARIES

Lists dictionaries in the current or specified database.

## Syntax

```sql
SHOW DICTIONARIES [ FROM <database_name> | IN <database_name> ]
    [ LIMIT <limit> ]
    [ LIKE '<pattern>' | WHERE <expr> ]
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| `FROM <database_name>` / `IN <database_name>` | Optional. Lists dictionaries from the specified database. |
| `LIMIT <limit>` | Optional. Limits the number of returned rows. |
| `LIKE '<pattern>'` | Optional. Filters dictionary names by pattern. |
| `WHERE <expr>` | Optional. Filters the result set with an expression. |

## Examples

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
