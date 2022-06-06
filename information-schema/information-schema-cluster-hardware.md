---
title: CLUSTER_HARDWARE
summary: Learn the `CLUSTER_HARDWARE` information_schema table.
---

# CLUSTER_HARDWARE {#cluster-hardware}

`CLUSTER_HARDWARE`ハードウェアシステムテーブルは、クラスタの各インスタンスが配置されているサーバーのハードウェア情報を提供します。

{{< copyable "" >}}

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

フィールドの説明：

-   `TYPE` ： [`information_schema.cluster_info`](/information-schema/information-schema-cluster-info.md)テーブルの`TYPE`フィールドに対応します。オプションの値は`tidb` 、および`pd` `tikv` 。
-   `INSTANCE` ： [`information_schema.cluster_info`](/information-schema/information-schema-cluster-info.md)クラスタ情報テーブルの`INSTANCE`フィールドに対応します。
-   `DEVICE_TYPE` ：ハードウェアタイプ。現在、 `cpu` 、および`memory`タイプを`net`でき`disk` 。
-   `DEVICE_NAME` ：ハードウェア名。 `DEVICE_NAME`の値は`DEVICE_TYPE`によって異なります。
    -   `cpu` ：ハードウェア名はcpuです。
    -   `memory` ：ハードウェア名はメモリです。
    -   `disk` ：ディスク名。
    -   `net` ：ネットワークカード名。
-   `NAME` ：ハードウェアの異なる情報名。たとえば、CPUには2つの情報名があります`cpu-logical-cores`と`cpu-physical-cores`は、それぞれ論理コア番号と物理コア番号を意味します。
-   `VALUE` ：ディスクボリュームやCPUコア番号などの対応するハードウェア情報の値。

次の例は、 `CLUSTER_HARDWARE`テーブルを使用してCPU情報を照会する方法を示しています。

{{< copyable "" >}}

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
