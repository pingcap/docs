---
title: Migrate MySQL with Addax (Batch)
sidebar_label: 'MySQL → Databend: Addax (Batch)'
---

> **Capabilities**: Full Load, Incremental

In this tutorial, you will load data from MySQL to Databend with Addax. Before you start, make sure you have successfully set up Databend, MySQL, and Addax in your environment.

1. In MySQL, create a SQL user that you will use for data loading and then create a table and populate it with sample data.

```sql title='In MySQL:'
mysql> create user 'mysqlu1'@'%' identified by '123';
mysql> grant all on *.* to 'mysqlu1'@'%';
mysql> create database db;
mysql> create table db.tb01(id int, col1 varchar(10));
mysql> insert into db.tb01 values(1, 'test1'), (2, 'test2'), (3, 'test3');
```

2. In Databend, create a corresponding target table.

```sql title='In Databend:'
databend> create database migrated_db;
databend> create table migrated_db.tb01(id int null, col1 String null);
```

3. Copy and paste the following code to a file, and name the file as _mysql_demo.json_:

:::note
For the available parameters and their descriptions, refer to the documentation provided at the following link: https://wgzhao.github.io/Addax/develop/writer/databendwriter/#_2
:::

```json title='mysql_demo.json'
{
  "job": {
    "setting": {
      "speed": {
        "channel": 4
      }
    },
    "content": {
      "writer": {
        "name": "databendwriter",
        "parameter": {
          "preSql": ["truncate table @table"],
          "postSql": [],
          "username": "u1",
          "password": "123",
          "database": "migrate_db",
          "table": "tb01",
          "jdbcUrl": "jdbc:mysql://127.0.0.1:3307/migrated_db",
          "loadUrl": ["127.0.0.1:8000", "127.0.0.1:8000"],
          "fieldDelimiter": "\\x01",
          "lineDelimiter": "\\x02",
          "column": ["*"],
          "format": "csv"
        }
      },
      "reader": {
        "name": "mysqlreader",
        "parameter": {
          "username": "mysqlu1",
          "password": "123",
          "column": ["*"],
          "connection": [
            {
              "jdbcUrl": ["jdbc:mysql://127.0.0.1:3306/db"],
              "driver": "com.mysql.jdbc.Driver",
              "table": ["tb01"]
            }
          ]
        }
      }
    }
  }
}
```

4. Run Addax:

```shell
cd {YOUR_ADDAX_DIR_BIN}
./addax.sh -L debug ./mysql_demo.json
```

You are all set! To verify the data loading, execute the query in Databend:

```sql
databend> select * from migrated_db.tb01;
+------+-------+
| id   | col1  |
+------+-------+
|    1 | test1 |
|    2 | test2 |
|    3 | test3 |
+------+-------+
```
