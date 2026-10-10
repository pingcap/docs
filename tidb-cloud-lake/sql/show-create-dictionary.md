---
title: SHOW CREATE DICTIONARY
summary: ディクショナリの作成に使用された SQL 文を表示します。
---

# SHOW CREATE DICTIONARY

ディクショナリの作成に使用された SQL 文を表示します。

## 構文 {#syntax}

```sql
SHOW CREATE DICTIONARY [ <catalog_name>. ][ <database_name>. ]<dictionary_name>
```

## パラメータ {#parameters}

| パラメータ | 説明 |
|-----------|-------------|
| `<dictionary_name>` | ディクショナリ名です。catalog 名および database 名で修飾できます。 |

## 出力 {#output}

結果には、ディクショナリ名と再構築された `CREATE DICTIONARY` 文が含まれます。

返される SQL では、`password` などの機密性の高い source オプションはマスクされます。

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