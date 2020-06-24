# view

TiDB supports views, A view acts as a virtual table, It can be created from SELECT statements. On the one hand, Using the view can only expose safe columns and data to the user, to ensure the security of sensitive columns and data in the underlying table. On the other hand, defining complex queries that frequently appear as views can make complex queries simpler and more convenient.

## query views

You can query a view in a similar way as you query an actual table. When the query is actually executed, the view is expanded into the SELECT statement defined when the view was created, and then the expanded query statment is executed.

## view metadata

To obtain metadata about views:

### use the `SHOW CREATE TABLE view_name` or `SHOW CREATE VIEW view_name` statement 

example：

```sql
show create view v;
```

This statement shows the `CREATE VIEW` statement that creates the named view. And show the value of the `character_set_client` and `collation_connection` system variable when the view was created. 

```sql
+------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------+----------------------+
| View | Create View                                                                                                                                                         | character_set_client | collation_connection |
+------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------+----------------------+
| v    | CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`127.0.0.1` SQL SECURITY DEFINER VIEW `v` (`a`) AS SELECT `s`.`a` FROM `test`.`t` LEFT JOIN `test`.`s` ON `t`.`a`=`s`.`a` | utf8                 | utf8_general_ci      |
+------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------+----------------------+
1 row in set (0.00 sec)
```

### query the `INFORMATION_SCHEMA.VIEWS` table

example:

```sql
select * from information_schema.views;
```

You can view the relevant meta information of the view by querying the table, Including `TABLE_CATALOG`, `TABLE_SCHEMA`, `TABLE_NAME`, `VIEW_DEFINITION`, `CHECK_OPTION`, `IS_UPDATABLE`, `DEFINER`, `SECURITY_TYPE`, `CHARACTER_SET_CLIENT`, `COLLATION_CONNECTION`

```sql
+---------------+--------------+------------+------------------------------------------------------------------------+--------------+--------------+----------------+---------------+----------------------+----------------------+
| TABLE_CATALOG | TABLE_SCHEMA | TABLE_NAME | VIEW_DEFINITION                                                        | CHECK_OPTION | IS_UPDATABLE | DEFINER        | SECURITY_TYPE | CHARACTER_SET_CLIENT | COLLATION_CONNECTION |
+---------------+--------------+------------+------------------------------------------------------------------------+--------------+--------------+----------------+---------------+----------------------+----------------------+
| def           | test         | v          | SELECT `s`.`a` FROM `test`.`t` LEFT JOIN `test`.`s` ON `t`.`a`=`s`.`a` | CASCADED     | NO           | root@127.0.0.1 | DEFINER       | utf8                 | utf8_general_ci      |
+---------------+--------------+------------+------------------------------------------------------------------------+--------------+--------------+----------------+---------------+----------------------+----------------------+
1 row in set (0.00 sec)
```

### use the HTTP API

example:

```shell
curl http://127.0.0.1:10080/schema/test/v
```

By visiting `http://{TiDBIP}:10080/schema/{db}/{view}`, you can  get all the meta-information for the view.

```shell
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
```

## Example

The following example will create a view, query the view, and finally delete the view.

```sql
create table t(a int, b int);
Query OK, 0 rows affected (0.01 sec)
```

```sql
insert into t values(1, 1),(2,2),(3,3);
Query OK, 3 rows affected (0.00 sec)
Records: 3  Duplicates: 0  Warnings: 0
```

```sql
create table s(a int);
Query OK, 0 rows affected (0.01 sec)
```

```sql
insert into s values(2),(3);
Query OK, 2 rows affected (0.01 sec)
Records: 2  Duplicates: 0  Warnings: 0
```

```sql
create view v as select s.a from t left join s on t.a = s.a;
Query OK, 0 rows affected (0.01 sec)
```

```sql
select * from v;
+------+
| a    |
+------+
| NULL |
|    2 |
|    3 |
+------+
3 rows in set (0.00 sec)
```

```sql
drop view v;
Query OK, 0 rows affected (0.02 sec)
```

## View limitations

 Now views in TiDB are subject to the following limitations:

* Materialized views are not supported yet.
* Views in TiDB are read-only, does not support write DML such as `UPDATE`, `INSERT`, `DELETE`, `TRUNCATE`.
* For created views,  the only supported DDL is `DROP`, i.e., `DROP [VIEW | TABLE]`.
