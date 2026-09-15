---
title: CREATE DICTIONARY
summary: 创建一个字典。
---

# CREATE DICTIONARY

创建一个字典。

## 语法 {#syntax}

```sql
CREATE [ OR REPLACE ] DICTIONARY [ IF NOT EXISTS ] [ <catalog_name>. ][ <database_name>. ]<dictionary_name>
(
    <column_name> <data_type> [ , <column_name> <data_type> , ... ]
)
PRIMARY KEY <column_name> [ , <column_name> , ... ]
SOURCE(
    <source_name>(
        <source_option> = '<value>' [ <source_option> = '<value>' ... ]
    )
)
[ COMMENT '<comment>' ]
```

## 参数 {#parameters}

| 参数 | 描述 |
|-----------|-------------|
| `OR REPLACE` | 使用相同名称替换现有字典。 |
| `IF NOT EXISTS` | 如果字典已存在，则成功返回且不做任何更改。 |
| `<dictionary_name>` | 字典名称。可以使用 catalog 和 database 名称进行限定。 |
| `(<column_name> <data_type>, ...)` | 声明字典的 schema。 |
| `PRIMARY KEY` | 定义一个或多个用于字典查找的键列。 |
| `SOURCE(...)` | 定义源连接器名称及其键值选项。 |
| `COMMENT` | 可选的字典注释。 |

> **注意：**
>
> SOURCE 仅支持 `MySQL` 和 `Redis`。

## 示例 {#examples}

MySQL 示例：

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
```

Redis 示例：

```sql
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
```