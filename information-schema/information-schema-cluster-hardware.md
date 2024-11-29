---
title: CLUSTER_HARDWARE
summary: CLUSTER_HARDWARE` information_schema テーブルについて学習します。
---

# クラスターハードウェア {#cluster-hardware}

`CLUSTER_HARDWARE`ハードウェア システム テーブルには、クラスターの各インスタンスが配置されているサーバーのハードウェア情報が表示されます。

> **注記：**
>
> この表は TiDB Self-Managed にのみ適用され、 [TiDB Cloud](https://docs.pingcap.com/tidbcloud/)では使用できません。

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
-   `INSTANCE` : [`information_schema.cluster_info`](/information-schema/information-schema-cluster-info.md)クラスタ情報テーブルの`INSTANCE`番目のフィールドに対応します。
-   `DEVICE_TYPE` : ハードウェア タイプ。現在、 `cpu` 、 `memory` 、 `disk` 、 `net`タイプを照会できます。
-   `DEVICE_NAME` : ハードウェア名`DEVICE_NAME`の値は`DEVICE_TYPE`によって異なります。
    -   `cpu` : ハードウェア名は cpu です。
    -   `memory` : ハードウェア名はメモリです。
    -   `disk` : ディスク名。
    -   `net` : ネットワーク カード名。
-   `NAME` : ハードウェアの異なる情報名。たとえば、 cpu には`cpu-logical-cores`と`cpu-physical-cores`という 2 つの情報名があり、それぞれ論理コア番号と物理コア番号を意味します。
-   `VALUE` : ディスクボリュームや CPU コア数などの対応するハードウェア情報の値。

次の例は、 `CLUSTER_HARDWARE`テーブルを使用して CPU 情報を照会する方法を示しています。

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
