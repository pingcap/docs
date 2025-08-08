---
title: CLUSTER_LOAD
summary: CLUSTER_LOAD` information_schema テーブルについて学習します。
---

# クラスターロード {#cluster-load}

`CLUSTER_LOAD`クラスタ負荷テーブルは、TiDB クラスタの各インスタンスが配置されているサーバーの現在の負荷情報を提供します。

> **注記：**
>
> このテーブルは TiDB Self-Managed にのみ適用され、 [TiDB Cloud](https://docs.pingcap.com/tidbcloud/)では使用できません。

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

-   `TYPE` : 表[`information_schema.cluster_info`](/information-schema/information-schema-cluster-info.md)のフィールド`TYPE`に対応します。オプションの値は`tidb` 、 `pd` 、 `tikv`です。
-   `INSTANCE` : [`information_schema.cluster_info`](/information-schema/information-schema-cluster-info.md)クラスター情報テーブルの`INSTANCE`フィールドに対応します。
-   `DEVICE_TYPE` : ハードウェアタイプ。現在、 `cpu` 、 `memory` 、 `disk` 、 `net`タイプを照会できます。
-   `DEVICE_NAME` : ハードウェア名`DEVICE_NAME`の値は`DEVICE_TYPE`に応じて変化します。
    -   `cpu` : ハードウェア名は cpu です。
    -   `disk` : ディスク名。
    -   `net` : ネットワーク カード名。
    -   `memory` : ハードウェア名はメモリです。
-   `NAME` : 異なる負荷タイプ。例えば、CPU `load15`は`load1` `load5` 3つの負荷タイプがあり、それぞれ1分、5分、15分以内のCPUの平均負荷を意味します。
-   `VALUE` : ハードウェア負荷の値。例えば、 `1min` 、 `5min` 、 `15min`それぞれ、1分、5分、15分以内のハードウェアの平均負荷を意味します。

次の例は、 `CLUSTER_LOAD`テーブルを使用して CPU の現在の負荷情報を照会する方法を示しています。

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
