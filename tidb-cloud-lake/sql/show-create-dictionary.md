---
title: SHOW CREATE DICTIONARY
summary: Shows the SQL statement used to create a dictionary.
---

# SHOW CREATE DICTIONARY

Shows the SQL statement used to create a dictionary.

## Syntax

```sql
SHOW CREATE DICTIONARY [ <catalog_name>. ][ <database_name>. ]<dictionary_name>
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| `<dictionary_name>` | The dictionary name. You can qualify it with catalog and database names. |

## Output

The result contains the dictionary name and the reconstructed `CREATE DICTIONARY` statement.

Sensitive source options such as `password` are masked in the returned SQL.

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

SHOW CREATE DICTIONARY user_info;

*************************** 1. row ***************************
       Dictionary: user_info
Create Dictionary: CREATE DICTIONARY user_info
(
  user_id BIGINT UNSIGNED NULL,
  user_name VARCHAR NULL,
  user_email VARCHAR NULL
)
PRIMARY KEY user_id
SOURCE(mysql(db='app' host='127.0.0.1' password='[HIDDEN]' port='3306' table='users' username='root'))
COMMENT 'User dictionary from MySQL'
```
