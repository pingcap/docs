---
title: SHOW CREATE DICTIONARY
summary: 显示用于创建字典的 SQL 语句。
---

# SHOW CREATE DICTIONARY

显示用于创建字典的 SQL 语句。

## 语法 {#syntax}

```sql
SHOW CREATE DICTIONARY [ <catalog_name>. ][ <database_name>. ]<dictionary_name>
```

## 参数 {#parameters}

| 参数 | 描述 |
|-----------|-------------|
| `<dictionary_name>` | 字典名称。你可以使用 catalog 名称和 database 名称对其进行限定。 |

## 输出 {#output}

结果包含字典名称以及重建后的 `CREATE DICTIONARY` 语句。

返回的 SQL 中会对敏感的源选项（例如 `password`）进行掩码处理。

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