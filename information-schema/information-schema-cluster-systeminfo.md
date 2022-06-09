---
title: CLUSTER_SYSTEMINFO
summary: Learn the `CLUSTER_SYSTEMINFO` kernel parameter table.
---

# CLUSTER_SYSTEMINFO {#cluster-systeminfo}

`CLUSTER_SYSTEMINFO`カーネルパラメータテーブルを使用して、クラスタのすべてのインスタンスが配置されているサーバーのカーネル構成情報を照会できます。現在、 `sysctl`システムの情報を照会することができます。

{{< copyable "" >}}

```sql
USE information_schema;
DESC cluster_systeminfo;
```

```sql
+-------------+--------------+------+------+---------+-------+
| Field       | Type         | Null | Key  | Default | Extra |
+-------------+--------------+------+------+---------+-------+
| TYPE        | varchar(64)  | YES  |      | NULL    |       |
| INSTANCE    | varchar(64)  | YES  |      | NULL    |       |
| SYSTEM_TYPE | varchar(64)  | YES  |      | NULL    |       |
| SYSTEM_NAME | varchar(64)  | YES  |      | NULL    |       |
| NAME        | varchar(256) | YES  |      | NULL    |       |
| VALUE       | varchar(128) | YES  |      | NULL    |       |
+-------------+--------------+------+------+---------+-------+
6 rows in set (0.00 sec)
```

フィールドの説明：

-   `TYPE` ： [`information_schema.cluster_info`](/information-schema/information-schema-cluster-info.md)テーブルの`TYPE`フィールドに対応します。オプションの値は、 `tidb` 、および`pd` `tikv` 。
-   `INSTANCE` ： [`information_schema.cluster_info`](/information-schema/information-schema-cluster-info.md)クラスタ情報テーブルの`INSTANCE`フィールドに対応します。
-   `SYSTEM_TYPE` ：システムタイプ。現在、 `system`のシステムタイプを照会できます。
-   `SYSTEM_NAME` ：システム名。現在、 `sysctl`のシステム名を照会できます。
-   `NAME` ： `sysctl`に対応する構成名。
-   `VALUE` ： `sysctl`に対応する構成項目の値。

次の例は、 `CLUSTER_SYSTEMINFO`のシステム情報テーブルを使用して、クラスタのすべてのサーバーのカーネルバージョンを照会する方法を示しています。

```sql
SELECT * FROM cluster_systeminfo WHERE name LIKE '%kernel.osrelease%'
```

```sql
+------+-------------------+-------------+-------------+------------------+----------------------------+
| TYPE | INSTANCE          | SYSTEM_TYPE | SYSTEM_NAME | NAME             | VALUE                      |
+------+-------------------+-------------+-------------+------------------+----------------------------+
| tidb | 172.16.5.40:4008  | system      | sysctl      | kernel.osrelease | 3.10.0-862.14.4.el7.x86_64 |
| pd   | 172.16.5.40:20379 | system      | sysctl      | kernel.osrelease | 3.10.0-862.14.4.el7.x86_64 |
| tikv | 172.16.5.40:21150 | system      | sysctl      | kernel.osrelease | 3.10.0-862.14.4.el7.x86_64 |
+------+-------------------+-------------+-------------+------------------+----------------------------+
```
