---
title: Migrate MySQL with DataX (Batch)
sidebar_label: 'MySQL → Databend: DataX (Batch)'
---

> **Capabilities**: Full Load, Incremental

In this tutorial, you will load data from MySQL to Databend with DataX. Before you start, make sure you have successfully set up Databend, MySQL, and DataX in your environment.

1. In MySQL, create a SQL user that you will use for data loading and then create a table and populate it with sample data.

```sql title='In MySQL:'
mysql> create user 'mysqlu1'@'%' identified by 'databend';
mysql> grant all on *.* to 'mysqlu1'@'%';
mysql> create database db;
mysql> create table db.tb01(id int, d double, t TIMESTAMP,  col1 varchar(10));
mysql> insert into db.tb01 values(1, 3.1,now(), 'test1'), (1, 4.1,now(), 'test2'), (1, 4.1,now(), 'test2');
```

2. In Databend, create a corresponding target table.

:::note
DataX data types can be converted to Databend's data types when loaded into Databend. For the specific correspondences between DataX data types and Databend's data types, refer to the documentation provided at the following link: https://github.com/alibaba/DataX/blob/master/databendwriter/doc/databendwriter.md#33-type-convert
:::

```sql title='In Databend:'
databend> create database migrated_db;
databend> create table migrated_db.tb01(id int null, d double null, t TIMESTAMP null,  col1 varchar(10) null);
```

3. Copy and paste the following code to a file, and name the file as *mysql_demo.json*. For the available parameters and their descriptions, refer to the documentation provided at the following link: https://github.com/alibaba/DataX/blob/master/databendwriter/doc/databendwriter.md#32-configuration-description

```json title='mysql_demo.json'
{
  "job": {
    "content": [
      {
        "reader": {
          "name": "mysqlreader",
          "parameter": {
            "username": "mysqlu1",
            "password": "databend",
            "column": [
              "id", "d", "t", "col1"
            ],
            "connection": [
              {
                "jdbcUrl": [
                  "jdbc:mysql://127.0.0.1:3307/db"
                ],
                "driver": "com.mysql.jdbc.Driver",
                "table": [
                  "tb01"
                ]
              }
            ]
          }
        },
        "writer": {
          "name": "databendwriter",
          "parameter": {
            "username": "databend",
            "password": "databend",
            "column": [
              "id", "d", "t", "col1"
            ],
            "preSql": [
            ],
            "postSql": [
            ],
            "connection": [
              {
                "jdbcUrl": "jdbc:databend://localhost:8000/migrated_db",
                "table": [
                  "tb01"
                ]
              }
            ]
          }
        }
      }
    ],
    "setting": {
      "speed": {
        "channel": 1
       }
    }
  }
}
```

:::tip
The provided code above configures DatabendWriter to operate in the INSERT mode. To switch to the REPLACE mode, you must include the writeMode and onConflictColumn parameters. For example:

```json title='mysql_demo.json'
...
"writer": {
          "name": "databendwriter",
          "parameter": {
            "writeMode": "replace",
            "onConflictColumn":["id"],
            "username": ...
```
:::

4. Run DataX:

```shell
cd {YOUR_DATAX_DIR_BIN}
python datax.py ./mysql_demo.json 
```

You're all set! To verify the data loading, execute the query in Databend:

```sql
databend> select * from migrated_db.tb01;
+------+------+----------------------------+-------+
| id   | d    | t                          | col1  |
+------+------+----------------------------+-------+
|    1 |  3.1 | 2023-02-01 07:11:08.500000 | test1 |
|    1 |  4.1 | 2023-02-01 07:11:08.501000 | test2 |
|    1 |  4.1 | 2023-02-01 07:11:08.501000 | test2 |
+------+------+----------------------------+-------+
```
