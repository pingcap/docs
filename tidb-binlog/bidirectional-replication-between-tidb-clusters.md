---
title: Bidirectional Replication Between TiDB Clusters
summary: Learn how to perform the bidirectional replication between TiDB clusters.
---

# TiDB クラスター間の双方向レプリケーション {#bidirectional-replication-between-tidb-clusters}

> **警告：**
>
> -   現在、双方向レプリケーションはまだ実験的機能です。本番環境での使用は**お**勧めしません。
> -   TiDB Binlog は、 TiDB v5.0 で導入された一部の機能と互換性がなく、一緒に使用することはできません。詳細は[ノート](/tidb-binlog/tidb-binlog-overview.md#notes)を参照してください。
> -   TiDB v7.5.0 以降、TiDB Binlogのデータ レプリケーション機能のテクニカル サポートは提供されなくなりました。データ レプリケーションの代替ソリューションとして[TiCDC](/ticdc/ticdc-overview.md)を使用することを強くお勧めします。
> -   TiDB v7.5.0 は TiDB Binlogのリアルタイム バックアップおよび復元機能を引き続きサポートしていますが、このコンポーネントは将来のバージョンでは完全に非推奨になります。データ回復の代替ソリューションとして[PITR](/br/br-pitr-guide.md)を使用することをお勧めします。

このドキュメントでは、2 つの TiDB クラスター間の双方向レプリケーション、レプリケーションの仕組み、レプリケーションを有効にする方法、DDL 操作をレプリケートする方法について説明します。

## ユーザーシナリオ {#user-scenario}

2 つの TiDB クラスターが相互にデータ変更を交換したい場合、TiDB Binlog を使用するとそれが可能になります。たとえば、クラスター A とクラスター B で相互にデータをレプリケートしたいとします。

> **注記：**
>
> これら 2 つのクラスターに書き込まれるデータには競合がない必要があります。つまり、2 つのクラスター内で、テーブルの一意のインデックスを持つ同じ主キーまたは行が変更されてはなりません。

ユーザーシナリオは以下のようになります。

![Architect](/media/binlog/bi-repl1.jpg)

## 実装の詳細 {#implementation-details}

![Mark Table](/media/binlog/bi-repl2.png)

クラスター A とクラスター B の間で双方向レプリケーションが有効になっている場合、クラスター A に書き込まれたデータはクラスター B にレプリケートされ、その後、これらのデータ変更はクラスター A にレプリケートされて戻されるため、レプリケーションの無限ループが発生します。上の図から、データ レプリケーション中に、 Drainer がbinlogイベントをマークし、マークされたイベントをフィルタリングして、そのようなレプリケーション ループを回避していることがわかります。

詳細な実装は次のように説明されます。

1.  2 つのクラスターのそれぞれに対して TiDB Binlogレプリケーション プログラムを開始します。
2.  レプリケートされるトランザクションがクラスター A のDrainerを通過すると、このDrainerはトランザクションに[`_drainer_repl_mark`テーブル](#mark-table)を追加し、この DML イベント更新をマーク テーブルに書き込み、このトランザクションをクラスター B にレプリケートします。
3.  クラスタB は、 `_drainer_repl_mark`マーク テーブルを持つbinlogイベントをクラスター A に返します。クラスター B のDrainerは、binlogイベントを解析するときに DML イベントを持つマーク テーブルを識別し、このbinlogイベントをクラスター A にレプリケートすることを断念します。

クラスター B からクラスター A へのレプリケーション プロセスは上記と同じです。 2 つのクラスターは相互に上流にも下流にもあります。

> **注記：**
>
> -   `_drainer_repl_mark`マーク テーブルを更新する場合、バイナリログを生成するにはデータ変更が必要です。
> -   DDL 操作はトランザクションではないため、DDL 操作をレプリケートするには一方向レプリケーション方法を使用する必要があります。詳細については[DDL 操作をレプリケートする](#replicate-ddl-operations)を参照してください。

Drainer は、競合を避けるために、ダウンストリームへの接続ごとに一意の ID を使用できます。 `channel_id`は、双方向レプリケーションのチャネルを示すために使用されます。 2 つのクラスターは同じ`channel_id`構成 (同じ値) である必要があります。

アップストリームで列を追加または削除すると、ダウンストリームにレプリケートされるデータの余分な列または欠落した列が存在する可能性があります。 Drainer は、余分な列を無視するか、欠落している列にデフォルト値を挿入することで、この状況を許容します。

## マークテーブル {#mark-table}

`_drainer_repl_mark`マーク テーブルは次の構造になっています。

```sql
CREATE TABLE `_drainer_repl_mark` (
  `id` bigint(20) NOT NULL,
  `channel_id` bigint(20) NOT NULL DEFAULT '0',
  `val` bigint(20) DEFAULT '0',
  `channel_info` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`,`channel_id`)
);
```

Drainer は次の SQL ステートメントを使用して`_drainer_repl_mark`更新します。これにより、データの変更とbinlogの生成が保証されます。

```sql
update drainer_repl_mark set val = val + 1 where id = ? && channel_id = ?;
```

## DDL 操作をレプリケートする {#replicate-ddl-operations}

Drainer はDDL 操作にマーク テーブルを追加できないため、DDL 操作をレプリケートするには一方向レプリケーション方法のみを使用できます。

たとえば、クラスタ A からクラスタ B への DDL レプリケーションが有効になっている場合、クラスタ B からクラスタ A へのレプリケーションは無効になります。これは、すべての DDL 操作がクラスタ A で実行されることを意味します。

> **注記：**
>
> DDL 操作は 2 つのクラスターで同時に実行できません。 DDL 操作の実行時に、DML 操作が同時に実行されているか、DMLbinlogがレプリケートされている場合、DML レプリケーションの上流と下流のテーブル構造が矛盾する可能性があります。

## 双方向レプリケーションを構成して有効にする {#configure-and-enable-bidirectional-replication}

クラスター A とクラスター B 間の双方向レプリケーションの場合、すべての DDL 操作がクラスター A で実行されると想定します。クラスター A からクラスター B へのレプリケーション パス上で、次の構成をDrainerに追加します。

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

クラスター B からクラスター A へのレプリケーション パスで、次の構成をDrainerに追加します。

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
