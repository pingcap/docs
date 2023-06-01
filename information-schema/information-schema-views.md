---
title: VIEWS
summary: Learn the `VIEWS` INFORMATION_SCHEMA table.
---

# ビュー {#views}

`VIEWS`表は、SQL ビューに関する情報を提供します。

```sql
USE INFORMATION_SCHEMA;
DESC VIEWS;
```

出力は次のとおりです。

```sql
+----------------------+--------------+------+------+---------+-------+
| Field                | Type         | Null | Key  | Default | Extra |
+----------------------+--------------+------+------+---------+-------+
| TABLE_CATALOG        | varchar(512) | NO   |      | NULL    |       |
| TABLE_SCHEMA         | varchar(64)  | NO   |      | NULL    |       |
| TABLE_NAME           | varchar(64)  | NO   |      | NULL    |       |
| VIEW_DEFINITION      | longtext     | NO   |      | NULL    |       |
| CHECK_OPTION         | varchar(8)   | NO   |      | NULL    |       |
| IS_UPDATABLE         | varchar(3)   | NO   |      | NULL    |       |
| DEFINER              | varchar(77)  | NO   |      | NULL    |       |
| SECURITY_TYPE        | varchar(7)   | NO   |      | NULL    |       |
| CHARACTER_SET_CLIENT | varchar(32)  | NO   |      | NULL    |       |
| COLLATION_CONNECTION | varchar(32)  | NO   |      | NULL    |       |
+----------------------+--------------+------+------+---------+-------+
10 rows in set (0.00 sec)
```

ビューを作成し、 `VIEWS`テーブルをクエリします。

```sql
CREATE VIEW test.v1 AS SELECT 1;
SELECT * FROM VIEWS\G
```

出力は次のとおりです。

```sql
*************************** 1. row ***************************
       TABLE_CATALOG: def
        TABLE_SCHEMA: test
          TABLE_NAME: v1
     VIEW_DEFINITION: SELECT 1
        CHECK_OPTION: CASCADED
        IS_UPDATABLE: NO
             DEFINER: root@127.0.0.1
       SECURITY_TYPE: DEFINER
CHARACTER_SET_CLIENT: utf8mb4
COLLATION_CONNECTION: utf8mb4_0900_ai_ci
1 row in set (0.00 sec)
```

`VIEWS`テーブルのフィールドは次のように説明されています。

-   `TABLE_CATALOG` : ビューが属するカタログの名前。この値は常に`def`です。
-   `TABLE_SCHEMA` : ビューが属するスキーマの名前。
-   `TABLE_NAME` : ビュー名。
-   `VIEW_DEFINITION` : ビューの定義。ビューの作成時に`SELECT`ステートメントによって作成されます。
-   `CHECK_OPTION` : `CHECK_OPTION`の値。値のオプションは`NONE` 、 `CASCADE` 、および`LOCAL`です。
-   `IS_UPDATABLE` : `UPDATE` / `INSERT` / `DELETE`がビューに適用されるかどうか。 TiDB では、値は常に`NO`です。
-   `DEFINER` : ビューを作成するユーザーの名前。形式は`'user_name'@'host_name'`です。
-   `SECURITY_TYPE` : `SQL SECURITY`の値。値のオプションは`DEFINER`および`INVOKER`です。
-   `CHARACTER_SET_CLIENT` : ビュー作成時の`character_set_client`セッション変数の値。
-   `COLLATION_CONNECTION` : ビュー作成時の`collation_connection`セッション変数の値。
