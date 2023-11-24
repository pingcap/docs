---
title: CLUSTER_HARDWARE
summary: Learn the `CLUSTER_HARDWARE` information_schema table.
---

# クラスター_ハードウェア {#cluster-hardware}

`CLUSTER_HARDWARE`ハードウェア システム テーブルは、クラスターの各インスタンスが配置されているサーバーのハードウェア情報を提供します。

> **注記：**
>
> このテーブルは TiDB セルフホスト型にのみ適用され、 [TiDB Cloud](https://docs.pingcap.com/tidbcloud/)では利用できません。

```sql
USE information_schema;
DESC cluster_hardware;
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
    -   `memory` : ハードウェア名はメモリです。
    -   `disk` : ディスク名。
    -   `net` : ネットワークカード名。
-   `NAME` : ハードウェアの各種情報名。たとえば、cpu には`cpu-logical-cores`と`cpu-physical-cores`という 2 つの情報名があり、それぞれ論理コア番号と物理コア番号を意味します。
-   `VALUE` : ディスクボリュームやCPUコア番号など、対応するハードウェア情報の値。

次の例は、 `CLUSTER_HARDWARE`テーブルを使用して CPU 情報をクエリする方法を示しています。

```sql
SELECT * FROM cluster_hardware WHERE device_type='cpu' AND device_name='cpu' AND name LIKE '%cores';
```

```sql
+------+-----------------+-------------+-------------+--------------------+-------+
| TYPE | INSTANCE        | DEVICE_TYPE | DEVICE_NAME | NAME               | VALUE |
+------+-----------------+-------------+-------------+--------------------+-------+
| tidb | 0.0.0.0:4000    | cpu         | cpu         | cpu-logical-cores  | 16    |
| tidb | 0.0.0.0:4000    | cpu         | cpu         | cpu-physical-cores | 8     |
| pd   | 127.0.0.1:2379  | cpu         | cpu         | cpu-logical-cores  | 16    |
| pd   | 127.0.0.1:2379  | cpu         | cpu         | cpu-physical-cores | 8     |
| tikv | 127.0.0.1:20165 | cpu         | cpu         | cpu-logical-cores  | 16    |
| tikv | 127.0.0.1:20165 | cpu         | cpu         | cpu-physical-cores | 8     |
+------+-----------------+-------------+-------------+--------------------+-------+
6 rows in set (0.03 sec)
```
