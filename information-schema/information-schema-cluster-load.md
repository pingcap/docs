---
title: CLUSTER_LOAD
summary: Learn the `CLUSTER_LOAD` information_schema table.
---

# CLUSTER_LOAD {#cluster-load}

`CLUSTER_LOAD`クラスター負荷テーブルは、TiDB クラスターの各インスタンスが配置されているサーバーの現在の負荷情報を提供します。

> **注記：**
>
> このテーブルは TiDB セルフホスト型にのみ適用され、 [TiDB Cloud](https://docs.pingcap.com/tidbcloud/)では利用できません。

```sql
USE information_schema;
DESC cluster_load;
```

```sql
+-------------+--------------+------+------+---------+-------+
| Field       | Type         | Null | Key  | Default | Extra |
+-------------+--------------+------+------+---------+-------+
| TYPE        | varchar(64)  | YES  |      | NULL    |       |
| INSTANCE    | varchar(64)  | YES  |      | NULL    |       |
| DEVICE_TYPE | varchar(64)  | YES  |      | NULL    |       |
| DEVICE_NAME | varchar(64)  | YES  |      | NULL    |       |
| NAME        | varchar(256) | YES  |      | NULL    |       |
| VALUE       | varchar(128) | YES  |      | NULL    |       |
+-------------+--------------+------+------+---------+-------+
6 rows in set (0.00 sec)
```

フィールドの説明:

-   `TYPE` : [`information_schema.cluster_info`](/information-schema/information-schema-cluster-info.md)テーブルの`TYPE`フィールドに対応します。オプションの値は`tidb` 、 `pd` 、および`tikv`です。
-   `INSTANCE` : [`information_schema.cluster_info`](/information-schema/information-schema-cluster-info.md)クラスタ情報テーブルの`INSTANCE`フィールドに対応します。
-   `DEVICE_TYPE` : ハードウェアの種類。現在、 `cpu` 、 `memory` 、 `disk` 、および`net`タイプをクエリできます。
-   `DEVICE_NAME` : ハードウェア名。 `DEVICE_NAME`の値は`DEVICE_TYPE`によって変化します。
    -   `cpu` : ハードウェア名は cpu です。
    -   `disk` : ディスク名。
    -   `net` : ネットワークカード名。
    -   `memory` : ハードウェア名はメモリです。
-   `NAME` : 異なる負荷タイプ。たとえば、 cpu には`load1` 、 `load5` 、および`load15` 3 つの負荷タイプがあり、それぞれ 1 分、5 分、15 分以内の CPU の平均負荷を意味します。
-   `VALUE` : ハードウェア負荷の値。たとえば、 `1min` 、 `5min` 、および`15min` 、それぞれ 1 分、5 分、および 15 分以内のハードウェアの平均負荷を意味します。

次の例は、 `CLUSTER_LOAD`テーブルを使用して CPU の現在の負荷情報をクエリする方法を示しています。

```sql
SELECT * FROM cluster_load WHERE device_type='cpu' AND device_name='cpu';
```

```sql
+------+-----------------+-------------+-------------+--------+-------+
| TYPE | INSTANCE        | DEVICE_TYPE | DEVICE_NAME | NAME   | VALUE |
+------+-----------------+-------------+-------------+--------+-------+
| tidb | 0.0.0.0:4000    | cpu         | cpu         | load1  | 0.13  |
| tidb | 0.0.0.0:4000    | cpu         | cpu         | load5  | 0.25  |
| tidb | 0.0.0.0:4000    | cpu         | cpu         | load15 | 0.31  |
| pd   | 127.0.0.1:2379  | cpu         | cpu         | load1  | 0.13  |
| pd   | 127.0.0.1:2379  | cpu         | cpu         | load5  | 0.25  |
| pd   | 127.0.0.1:2379  | cpu         | cpu         | load15 | 0.31  |
| tikv | 127.0.0.1:20165 | cpu         | cpu         | load1  | 0.13  |
| tikv | 127.0.0.1:20165 | cpu         | cpu         | load5  | 0.25  |
| tikv | 127.0.0.1:20165 | cpu         | cpu         | load15 | 0.31  |
+------+-----------------+-------------+-------------+--------+-------+
9 rows in set (1.50 sec)
```
