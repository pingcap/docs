---
title: CREATE DICTIONARY
summary: ディクショナリを作成します。
---

# CREATE DICTIONARY

ディクショナリを作成します。

## 構文 {#syntax}

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

## パラメータ {#parameters}

| パラメータ | 説明 |
|-----------|-------------|
| `OR REPLACE` | 同じ名前の既存のディクショナリを置き換えます。 |
| `IF NOT EXISTS` | ディクショナリがすでに存在する場合、変更を加えずに成功します。 |
| `<dictionary_name>` | ディクショナリ名です。catalog 名および database 名で修飾できます。 |
| `(<column_name> <data_type>, ...)` | ディクショナリのスキーマを宣言します。 |
| `PRIMARY KEY` | ディクショナリのルックアップに使用する 1 つ以上のキーカラムを定義します。 |
| `SOURCE(...)` | ソースコネクタ名と、そのキーと値のオプションを定義します。 |
| `COMMENT` | 任意のディクショナリコメントです。 |

> **Note:**
>
> SOURCE は `MySQL` と `Redis` のみをサポートします。

## 例 {#examples}

MySQL の例:

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

Redis の例:

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