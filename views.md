---
title: Views
summary: TiDB でビューを使用する方法を学習します。
---

# ビュー {#views}

TiDB はビューをサポートしています。ビューは仮想テーブルとして機能し、そのスキーマはビューを作成する`SELECT`ステートメントによって定義されます。ビューを使用すると、次の利点があります。

-   安全なフィールドとデータのみをユーザーに公開し、基になるテーブルに保存されている機密フィールドとデータのセキュリティを確保します。
-   頻繁に表示される複雑なクエリをビューとして定義し、複雑なクエリをより簡単かつ便利にします。

## クエリビュー {#query-views}

ビューのクエリは通常のテーブルのクエリと似ています。ただし、TiDB がビューをクエリする場合、実際にはビューに関連付けられた`SELECT`ステートメントがクエリされます。

## メタデータを表示 {#show-metadata}

ビューのメタデータを取得するには、次のいずれかの方法を選択します。

### <code>SHOW CREATE TABLE view_name</code>または<code>SHOW CREATE VIEW view_name</code>ステートメントを使用します。 {#use-the-code-show-create-table-view-name-code-or-code-show-create-view-view-name-code-statement}

使用例:

```sql
show create view v;
```

このステートメントは、このビューに対応する`CREATE VIEW`ステートメントと、ビューが作成されたときの`character_set_client`と`collation_connection`のシステム変数の値を示します。

```sql
+------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------+----------------------+
| View | Create View                                                                                                                                                         | character_set_client | collation_connection |
+------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------+----------------------+
| v    | CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`127.0.0.1` SQL SECURITY DEFINER VIEW `v` (`a`) AS SELECT `s`.`a` FROM `test`.`t` LEFT JOIN `test`.`s` ON `t`.`a`=`s`.`a` | utf8                 | utf8_general_ci      |
+------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------+----------------------+
1 row in set (0.00 sec)
```

### <code>INFORMATION_SCHEMA.VIEWS</code>テーブルをクエリする {#query-the-code-information-schema-views-code-table}

使用例:

```sql
select * from information_schema.views;
```

このテーブルをクエリすることで、 `TABLE_CATALOG` 、 `TABLE_SCHEMA` 、 `TABLE_NAME` 、 `VIEW_DEFINITION` 、 `CHECK_OPTION` 、 `IS_UPDATABLE` 、 `DEFINER` 、 `SECURITY_TYPE` 、 `CHARACTER_SET_CLIENT` 、 `COLLATION_CONNECTION`などのビューの関連メタ情報を表示できます。

```sql
+---------------+--------------+------------+------------------------------------------------------------------------+--------------+--------------+----------------+---------------+----------------------+----------------------+
| TABLE_CATALOG | TABLE_SCHEMA | TABLE_NAME | VIEW_DEFINITION                                                        | CHECK_OPTION | IS_UPDATABLE | DEFINER        | SECURITY_TYPE | CHARACTER_SET_CLIENT | COLLATION_CONNECTION |
+---------------+--------------+------------+------------------------------------------------------------------------+--------------+--------------+----------------+---------------+----------------------+----------------------+
| def           | test         | v          | SELECT `s`.`a` FROM `test`.`t` LEFT JOIN `test`.`s` ON `t`.`a`=`s`.`a` | CASCADED     | NO           | root@127.0.0.1 | DEFINER       | utf8                 | utf8_general_ci      |
+---------------+--------------+------------+------------------------------------------------------------------------+--------------+--------------+----------------+---------------+----------------------+----------------------+
1 row in set (0.00 sec)
```

### HTTP APIを使用する {#use-the-http-apis}

使用例:

```sql
curl http://127.0.0.1:10080/schema/test/v
```

`http://{TiDBIP}:10080/schema/{db}/{view}`アクセスすると、ビューのすべてのメタデータを取得できます。

    {
     "id": 122,
     "name": {
      "O": "v",
      "L": "v"
     },
     "charset": "utf8",
     "collate": "utf8_general_ci",
     "cols": [
      {
       "id": 1,
       "name": {
        "O": "a",
        "L": "a"
       },
       "offset": 0,
       "origin_default": null,
       "default": null,
       "default_bit": null,
       "default_is_expr": false,
       "generated_expr_string": "",
       "generated_stored": false,
       "dependences": null,
       "type": {
        "Tp": 0,
        "Flag": 0,
        "Flen": 0,
        "Decimal": 0,
        "Charset": "",
        "Collate": "",
        "Elems": null
       },
       "state": 5,
       "comment": "",
       "hidden": false,
       "version": 0
      }
     ],
     "index_info": null,
     "fk_info": null,
     "state": 5,
     "pk_is_handle": false,
     "is_common_handle": false,
     "comment": "",
     "auto_inc_id": 0,
     "auto_id_cache": 0,
     "auto_rand_id": 0,
     "max_col_id": 1,
     "max_idx_id": 0,
     "update_timestamp": 416801600091455490,
     "ShardRowIDBits": 0,
     "max_shard_row_id_bits": 0,
     "auto_random_bits": 0,
     "pre_split_regions": 0,
     "partition": null,
     "compression": "",
     "view": {
      "view_algorithm": 0,
      "view_definer": {
       "Username": "root",
       "Hostname": "127.0.0.1",
       "CurrentUser": false,
       "AuthUsername": "root",
       "AuthHostname": "%"
      },
      "view_security": 0,
      "view_select": "SELECT `s`.`a` FROM `test`.`t` LEFT JOIN `test`.`s` ON `t`.`a`=`s`.`a`",
      "view_checkoption": 1,
      "view_cols": null
     },
     "sequence": null,
     "Lock": null,
     "version": 3,
     "tiflash_replica": null
    }

## 例 {#example}

次の例では、ビューを作成し、このビューをクエリし、このビューを削除します。

```sql
create table t(a int, b int);
```

    Query OK, 0 rows affected (0.01 sec)

```sql
insert into t values(1, 1),(2,2),(3,3);
```

    Query OK, 3 rows affected (0.00 sec)
    Records: 3  Duplicates: 0  Warnings: 0

```sql
create table s(a int);
```

    Query OK, 0 rows affected (0.01 sec)

```sql
insert into s values(2),(3);
```

    Query OK, 2 rows affected (0.01 sec)
    Records: 2  Duplicates: 0  Warnings: 0

```sql
create view v as select s.a from t left join s on t.a = s.a;
```

    Query OK, 0 rows affected (0.01 sec)

```sql
select * from v;
```

    +------+
    | a    |
    +------+
    | NULL |
    |    2 |
    |    3 |
    +------+
    3 rows in set (0.00 sec)

```sql
drop view v;
```

    Query OK, 0 rows affected (0.02 sec)

## 制限事項 {#limitations}

現在、TiDB のビューには次の制限があります。

-   マテリアライズド ビューはまだサポートされていません。
-   TiDB のビューは読み取り専用であり、 `UPDATE` 、 `INSERT` 、 `DELETE` 、 `TRUNCATE`などの書き込み操作はサポートされません。
-   作成されたビューの場合、サポートされているDDL操作は`DROP [VIEW | TABLE]`のみです。

## 参照 {#see-also}

-   [ビューを作成](/sql-statements/sql-statement-create-view.md)
-   [ドロップビュー](/sql-statements/sql-statement-drop-view.md)
