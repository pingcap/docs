---
title: VIEWS
summary: VIEWS` INFORMATION_SCHEMA テーブルについて学習します。
---

# ビュー {#views}

`VIEWS`表には[SQLビュー](/views.md)に関する情報が示されています。

```sql
USE INFORMATION_SCHEMA;
DESC VIEWS;
```

出力は次のようになります。

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

出力は次のようになります。

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

`VIEWS`テーブル内のフィールドは次のように説明されます。

-   `TABLE_CATALOG` : ビューが属するカタログの名前。この値は常に`def` 。
-   `TABLE_SCHEMA` : ビューが属するスキーマの名前。
-   `TABLE_NAME` : ビュー名。
-   `VIEW_DEFINITION` : ビューの定義。ビューが作成されるときに`SELECT`ステートメントによって作成されます。
-   `CHECK_OPTION` : `CHECK_OPTION`値。値の選択肢は`NONE` 、 `CASCADE` 、 `LOCAL`です。
-   `IS_UPDATABLE` : ビューに`UPDATE` / `INSERT` / `DELETE`が適用されるかどうか。TiDBでは、値は常に`NO`です。
-   `DEFINER` : ビューを作成したユーザーの名前。形式は`'user_name'@'host_name'`です。
-   `SECURITY_TYPE` : `SQL SECURITY`の値。値の選択肢は`DEFINER`と`INVOKER`です。
-   `CHARACTER_SET_CLIENT` : ビューが作成された時点の`character_set_client`番目のセッション変数の値。
-   `COLLATION_CONNECTION` : ビューが作成された時点の`collation_connection`番目のセッション変数の値。

## 参照 {#see-also}

-   [`CREATE VIEW`](/sql-statements/sql-statement-create-view.md)
-   [`DROP VIEW`](/sql-statements/sql-statement-drop-view.md)
