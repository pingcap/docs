---
title: Bidirectional Replication Between TiDB Clusters
summary: TiDB クラスター間の双方向レプリケーションを実行する方法を学習します。
---

# TiDB クラスター間の双方向レプリケーション {#bidirectional-replication-between-tidb-clusters}

> **警告：**
>
> -   現在、双方向レプリケーションはまだ実験的機能です。本番環境での使用は推奨され**ません**。
> -   TiDB Binlog はTiDB v5.0 で導入された一部の機能と互換性がなく、併用できません。詳細については[ノート](/tidb-binlog/tidb-binlog-overview.md#notes)を参照してください。
> -   TiDB v7.5.0 以降、TiDB Binlogのデータ レプリケーション機能のテクニカル サポートは提供されなくなりました。データ レプリケーションの代替ソリューションとして[ティCDC](/ticdc/ticdc-overview.md)を使用することを強くお勧めします。
> -   TiDB v7.5.0 では、TiDB Binlogのリアルタイム バックアップと復元機能が引き続きサポートされていますが、このコンポーネントは将来のバージョンでは完全に廃止される予定です。データ復旧の代替ソリューションとして[ピトル](/br/br-pitr-guide.md)を使用することをお勧めします。

このドキュメントでは、2 つの TiDB クラスター間の双方向レプリケーション、レプリケーションの仕組み、有効化の方法、および DDL 操作をレプリケートする方法について説明します。

## ユーザーシナリオ {#user-scenario}

2 つの TiDB クラスターが相互にデータの変更を交換する場合は、TiDB Binlog を使用するとそれが可能になります。たとえば、クラスター A とクラスター B が相互にデータを複製するとします。

> **注記：**
>
> これら 2 つのクラスターに書き込まれるデータは競合がないことが必要です。つまり、2 つのクラスターで、同じ主キーまたはテーブルの一意のインデックスを持つ行を変更してはなりません。

ユーザーシナリオは以下のようになります。

![Architect](/media/binlog/bi-repl1.jpg)

## 実装の詳細 {#implementation-details}

![Mark Table](/media/binlog/bi-repl2.png)

クラスター A とクラスター B の間で双方向レプリケーションが有効になっている場合、クラスター A に書き込まれたデータはクラスター B にレプリケートされ、その後これらのデータ変更がクラスター A にレプリケートされ、レプリケーションの無限ループが発生します。上の図から、データ レプリケーション中にDrainer がbinlogイベントをマークし、マークされたイベントをフィルターしてこのようなレプリケーション ループを回避することがわかります。

詳細な実装は次のように説明されます。

1.  2 つのクラスターそれぞれに対して TiDB Binlogレプリケーション プログラムを起動します。
2.  複製されるトランザクションがクラスター A のDrainerを通過すると、このDrainer はトランザクションに[`_drainer_repl_mark`テーブル](#mark-table)を追加し、この DML イベント更新をマーク テーブルに書き込み、このトランザクションをクラスター B に複製します。
3.  クラスタB は、マーク テーブル`_drainer_repl_mark`を含むbinlogイベントをクラスター A に返します。クラスター B のDrainer は、 binlogイベントを解析するときに DML イベントを含むマーク テーブルを識別し、このbinlogイベントをクラスター A に複製することを中止します。

クラスター B からクラスター A へのレプリケーション プロセスは上記と同じです。2 つのクラスターは、互いに上流と下流に存在できます。

> **注記：**
>
> -   `_drainer_repl_mark`マーク テーブルを更新する場合、バイナリ ログを生成するためにデータの変更が必要になります。
> -   DDL 操作はトランザクションではないため、DDL 操作をレプリケートするには一方向レプリケーション方式を使用する必要があります。詳細については[DDL操作を複製する](#replicate-ddl-operations)参照してください。

Drainerは、競合を避けるために、ダウンストリームへの接続ごとに一意の ID を使用できます。1 `channel_id`双方向レプリケーションのチャネルを示すために使用されます。2 つのクラスターは同じ`channel_id`構成 (同じ値) を持つ必要があります。

アップストリームで列を追加または削除すると、ダウンストリームに複製されるデータの列が余分に存在したり、不足したりする可能性があります。Drainerは、余分な列を無視するか、不足している列にデフォルト値を挿入することで、この状況に対応します。

## マークテーブル {#mark-table}

`_drainer_repl_mark`マーク テーブルの構造は次のとおりです。

```sql
CREATE TABLE `_drainer_repl_mark` (
  `id` bigint(20) NOT NULL,
  `channel_id` bigint(20) NOT NULL DEFAULT '0',
  `val` bigint(20) DEFAULT '0',
  `channel_info` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`,`channel_id`)
);
```

Drainer は次の SQL ステートメントを使用して`_drainer_repl_mark`更新し、データの変更とbinlogの生成を保証します。

```sql
update drainer_repl_mark set val = val + 1 where id = ? && channel_id = ?;
```

## DDL操作を複製する {#replicate-ddl-operations}

Drainer はDDL 操作にマーク テーブルを追加できないため、DDL 操作をレプリケートするには一方向のレプリケーション メソッドのみを使用できます。

たとえば、クラスター A からクラスター B への DDL レプリケーションが有効になっている場合、クラスター B からクラスター A へのレプリケーションは無効になります。つまり、すべての DDL 操作はクラスター A で実行されます。

> **注記：**
>
> DDL 操作は、2 つのクラスターで同時に実行できません。DDL 操作の実行時に、DML 操作が同時に実行されていたり、DMLbinlogがレプリケートされていたりすると、DML レプリケーションの上流と下流のテーブル構造に不整合が生じる可能性があります。

## 双方向レプリケーションを構成して有効にする {#configure-and-enable-bidirectional-replication}

クラスター A とクラスター B 間の双方向レプリケーションでは、すべての DDL 操作がクラスター A で実行されると想定します。クラスター A からクラスター B へのレプリケーション パスで、 Drainerに次の構成を追加します。

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

クラスター B からクラスター A へのレプリケーション パスで、 Drainerに次の構成を追加します。

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
