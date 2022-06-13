---
title: Bidirectional Replication Between TiDB Clusters
summary: Learn how to perform the bidirectional replication between TiDB clusters.
---

# TiDBクラスター間の双方向レプリケーション {#bidirectional-replication-between-tidb-clusters}

> **警告：**
>
> 現在、双方向レプリケーションはまだ実験的機能です。実稼働環境での使用はお勧めし**ません**。

このドキュメントでは、2つのTiDBクラスター間の双方向レプリケーション、レプリケーションの仕組み、有効にする方法、およびDDL操作をレプリケートする方法について説明します。

## ユーザーシナリオ {#user-scenario}

2つのTiDBクラスターが相互にデータ変更を交換するようにしたい場合は、TiDBBinlogでそれを行うことができます。たとえば、クラスタAとクラスタBが相互にデータを複製するようにします。

> **ノート：**
>
> これらの2つのクラスターに書き込まれるデータは、競合がない必要があります。つまり、2つのクラスターでは、同じ主キーまたはテーブルの一意のインデックスを持つ行を変更しないでください。

ユーザーシナリオを以下に示します。

![Architect](/media/binlog/bi-repl1.jpg)

## 実装の詳細 {#implementation-details}

![Mark Table](/media/binlog/bi-repl2.png)

クラスタAとクラスタBの間で双方向レプリケーションが有効になっている場合、クラスタAに書き込まれたデータはクラスタBにレプリケートされ、次にこれらのデータ変更がクラスタAにレプリケートされます。これにより、レプリケーションの無限ループが発生します。上の図から、データレプリケーション中に、Drainerがbinlogイベントにマークを付け、マークされたイベントをフィルターで除外して、このようなレプリケーションループを回避していることがわかります。

詳細な実装は次のとおりです。

1.  2つのクラスターのそれぞれに対してTiDBBinlogレプリケーションプログラムを開始します。
2.  複製されるトランザクションがクラスタAのDrainerを通過すると、このDrainerはトランザクションに[`_drainer_repl_mark`テーブル](#mark-table)を追加し、このDMLイベント更新をマークテーブルに書き込み、このトランザクションをクラスタBに複製します。
3.  クラスターBは、 `_drainer_repl_mark`のマークテーブルを持つbinlogイベントをクラスタAに返します。クラスタBのDrainerは、binlogイベントを解析するときにDMLイベントでマークテーブルを識別し、このbinlogイベントのクラスタAへの複製をあきらめます。

クラスタBからクラスタAへのレプリケーションプロセスは上記と同じです。 2つのクラスターは、互いに上流と下流に配置できます。

> **ノート：**
>
> -   `_drainer_repl_mark`マークテーブルを更新する場合、binlogを生成するためにデータを変更する必要があります。
> -   DDL操作はトランザクションではないため、一方向の複製方法を使用してDDL操作を複製する必要があります。詳細については、 [DDL操作を複製する](#replicate-ddl-operations)を参照してください。

ドレイナーは、競合を回避するために、ダウンストリームへの接続ごとに一意のIDを使用できます。 `channel_id`は、双方向レプリケーションのチャネルを示すために使用されます。 2つのクラスターは、同じ`channel_id`の構成（同じ値）である必要があります。

アップストリームで列を追加または削除すると、ダウンストリームに複製されるデータの列が余分にあるか、欠落している可能性があります。 Drainerは、余分な列を無視するか、欠落している列にデフォルト値を挿入することにより、この状況を許容します。

## マークテーブル {#mark-table}

`_drainer_repl_mark`マークテーブルの構造は次のとおりです。

{{< copyable "" >}}

```sql
CREATE TABLE `_drainer_repl_mark` (
  `id` bigint(20) NOT NULL,
  `channel_id` bigint(20) NOT NULL DEFAULT '0',
  `val` bigint(20) DEFAULT '0',
  `channel_info` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`,`channel_id`)
);
```

Drainerは次のSQLステートメントを使用して`_drainer_repl_mark`を更新します。これにより、データの変更とbinlogの生成が保証されます。

{{< copyable "" >}}

```sql
update drainer_repl_mark set val = val + 1 where id = ? && channel_id = ?;
```

## DDL操作を複製する {#replicate-ddl-operations}

DrainerはマークテーブルをDDL操作に追加できないため、一方向の複製方法のみを使用してDDL操作を複製できます。

たとえば、クラスターAからクラスタBへのDDLレプリケーションが有効になっている場合、クラスタBからクラスタAへのレプリケーションは無効になりクラスタ。これは、すべてのDDL操作がクラスタAで実行されることを意味します。

> **ノート：**
>
> DDL操作は、2つのクラスターで同時に実行することはできません。 DDL操作が実行されるときに、DML操作が同時に実行されている場合、またはDML binlogが複製されている場合、DML複製のアップストリームテーブル構造とダウンストリームテーブル構造に一貫性がない可能性があります。

## 双方向レプリケーションを構成して有効にする {#configure-and-enable-bidirectional-replication}

クラスタAとクラスタBの間の双方向レプリケーションの場合、すべてのDDL操作がクラスタAで実行されると想定します。クラスタAからクラスタBへのレプリケーションパスで、次の構成をDrainerに追加します。

{{< copyable "" >}}

```toml
[syncer]
loopback-control = true
channel-id = 1 # Configures the same ID for both clusters to be replicated.
sync-ddl = true # Enables it if you need to perform DDL replication.

[syncer.to]
# 1 means SyncFullColumn and 2 means SyncPartialColumn.
# If set to SyncPartialColumn, Drainer allows the downstream table
# structure to have more or fewer columns than the data to be replicated
# And remove the STRICT_TRANS_TABLES of the SQL mode to allow fewer columns, and insert zero values to the downstream.
sync-mode = 2

# Ignores the checkpoint table.
[[syncer.ignore-table]]
db-name = "tidb_binlog"
tbl-name = "checkpoint"
```

クラスタBからクラスタAへのレプリケーションパスで、次の設定をDrainerに追加します。

{{< copyable "" >}}

```toml
[syncer]
loopback-control = true
channel-id = 1 # Configures the same ID for both clusters to be replicated.
sync-ddl = false  # Disables it if you do not need to perform DDL replication.

[syncer.to]
# 1 means SyncFullColumn and 2 means SyncPartialColumn.
# If set to SyncPartialColumn, Drainer allows the downstream table
# structure to have more or fewer columns than the data to be replicated
# And remove the STRICT_TRANS_TABLES of the SQL mode to allow fewer columns, and insert zero values to the downstream.
sync-mode = 2

# Ignores the checkpoint table.
[[syncer.ignore-table]]
db-name = "tidb_binlog"
tbl-name = "checkpoint"
```
