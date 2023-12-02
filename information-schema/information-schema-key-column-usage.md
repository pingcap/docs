---
title: KEY_COLUMN_USAGE
summary: Learn the `KEY_COLUMN_USAGE` information_schema table.
---

# KEY_COLUMN_USAGE {#key-column-usage}

`KEY_COLUMN_USAGE`表は、主キー制約などの列のキー制約を示します。

```sql
USE information_schema;
DESC key_column_usage;
```

    +-------------------------------+--------------+------+------+---------+-------+
    | Field                         | Type         | Null | Key  | Default | Extra |
    +-------------------------------+--------------+------+------+---------+-------+
    | CONSTRAINT_CATALOG            | varchar(512) | NO   |      | NULL    |       |
    | CONSTRAINT_SCHEMA             | varchar(64)  | NO   |      | NULL    |       |
    | CONSTRAINT_NAME               | varchar(64)  | NO   |      | NULL    |       |
    | TABLE_CATALOG                 | varchar(512) | NO   |      | NULL    |       |
    | TABLE_SCHEMA                  | varchar(64)  | NO   |      | NULL    |       |
    | TABLE_NAME                    | varchar(64)  | NO   |      | NULL    |       |
    | COLUMN_NAME                   | varchar(64)  | NO   |      | NULL    |       |
    | ORDINAL_POSITION              | bigint(10)   | NO   |      | NULL    |       |
    | POSITION_IN_UNIQUE_CONSTRAINT | bigint(10)   | YES  |      | NULL    |       |
    | REFERENCED_TABLE_SCHEMA       | varchar(64)  | YES  |      | NULL    |       |
    | REFERENCED_TABLE_NAME         | varchar(64)  | YES  |      | NULL    |       |
    | REFERENCED_COLUMN_NAME        | varchar(64)  | YES  |      | NULL    |       |
    +-------------------------------+--------------+------+------+---------+-------+
    12 rows in set (0.00 sec)

```sql
SELECT * FROM key_column_usage WHERE table_schema='mysql' and table_name='user';
```

    *************************** 1. row ***************************
               CONSTRAINT_CATALOG: def
                CONSTRAINT_SCHEMA: mysql
                  CONSTRAINT_NAME: PRIMARY
                    TABLE_CATALOG: def
                     TABLE_SCHEMA: mysql
                       TABLE_NAME: user
                      COLUMN_NAME: Host
                 ORDINAL_POSITION: 1
    POSITION_IN_UNIQUE_CONSTRAINT: NULL
          REFERENCED_TABLE_SCHEMA: NULL
            REFERENCED_TABLE_NAME: NULL
           REFERENCED_COLUMN_NAME: NULL
    *************************** 2. row ***************************
               CONSTRAINT_CATALOG: def
                CONSTRAINT_SCHEMA: mysql
                  CONSTRAINT_NAME: PRIMARY
                    TABLE_CATALOG: def
                     TABLE_SCHEMA: mysql
                       TABLE_NAME: user
                      COLUMN_NAME: User
                 ORDINAL_POSITION: 2
    POSITION_IN_UNIQUE_CONSTRAINT: NULL
          REFERENCED_TABLE_SCHEMA: NULL
            REFERENCED_TABLE_NAME: NULL
           REFERENCED_COLUMN_NAME: NULL
    2 rows in set (0.00 sec)

`KEY_COLUMN_USAGE`のテーブルの列の説明は次のとおりです。

-   `CONSTRAINT_CATALOG` : 制約が属するカタログの名前。値は常に`def`です。
-   `CONSTRAINT_SCHEMA` : 制約が属するスキーマの名前。
-   `CONSTRAINT_NAME` : 制約の名前。
-   `TABLE_CATALOG` : テーブルが属するカタログの名前。値は常に`def`です。
-   `TABLE_SCHEMA` : テーブルが属するスキーマの名前。
-   `TABLE_NAME` : 制約のあるテーブルの名前。
-   `COLUMN_NAME` : 制約のある列の名前。
-   `ORDINAL_POSITION` : テーブル内ではなく、制約内の列の位置。位置番号は`1`から始まります。
-   `POSITION_IN_UNIQUE_CONSTRAINT` : 一意制約と主キー制約が空です。外部キー制約の場合、この列は参照されるテーブルのキーの位置になります。
-   `REFERENCED_TABLE_SCHEMA` : 制約によって参照されるスキーマの名前。現在、TiDB では、外部キー制約を除くすべての制約におけるこの列の値は`nil`です。
-   `REFERENCED_TABLE_NAME` : 制約によって参照されるテーブルの名前。現在、TiDB では、外部キー制約を除くすべての制約におけるこの列の値は`nil`です。
-   `REFERENCED_COLUMN_NAME` : 制約によって参照される列の名前。現在、TiDB では、外部キー制約を除くすべての制約におけるこの列の値は`nil`です。
