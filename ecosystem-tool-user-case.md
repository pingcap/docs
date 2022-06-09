---
title: TiDB Tools Use Cases
summary: Learn the common use cases of TiDB tools and how to choose the tools.
---

# TiDBツールのユースケース {#tidb-tools-use-cases}

このドキュメントでは、TiDBツールの一般的な使用例と、シナリオに適したツールを選択する方法を紹介します。

## 物理マシンまたは仮想マシンにデプロイを導入して運用する {#deploy-and-operate-tidb-on-physical-or-virtual-machines}

物理マシンまたは仮想マシンにTiDBを展開して操作する必要がある場合は、 [TiUP](/tiup/tiup-overview.md)をインストールしてから、TiUPを使用してTiDB、PD、TiKVなどのTiDBコンポーネントを管理できます。

## KubernetesでTiDBをデプロイして運用する {#deploy-and-operate-tidb-in-kubernetes}

KubernetesでTiDBをデプロイして運用する必要がある場合は、Kubernetesクラスタをデプロイしてから、 [TiDB Operator](https://docs.pingcap.com/tidb-in-kubernetes/stable)をデプロイできます。その後、 TiDB Operatorを使用して、TiDBクラスタをデプロイおよび操作できます。

## CSVからTiDBにデータをインポートする {#import-data-from-csv-to-tidb}

他のツールによってエクスポートされた互換性のあるCSVファイルをTiDBにインポートする必要がある場合は、 [TiDB Lightning](/tidb-lightning/migrate-from-csv-using-tidb-lightning.md)を使用します。

## MySQL/ Auroraから完全なデータをインポートする {#import-full-data-from-mysql-aurora}

MySQL / Auroraから完全なデータをインポートする必要がある場合は、最初に[Dumpling](/dumpling-overview.md)を使用してデータをSQLダンプファイルとしてエクスポートし、次に[TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)を使用してデータをTiDBクラスタにインポートします。

## MySQL/ Auroraからデータを移行する {#migrate-data-from-mysql-aurora}

MySQL / Auroraからフルデータとインクリメンタルデータの両方を移行する必要がある場合は、 [TiDBデータ移行](/dm/dm-overview.md) （DM）を使用して[AuroraからTiDBへのデータの移行](/migrate-aurora-to-tidb.md)を実行します。

フルデータボリュームが（TBレベルで）大きい場合は、最初に[Dumpling](/dumpling-overview.md)と[TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)を使用してフルデータ移行を実行し、次にDMを使用してインクリメンタルデータ移行を実行できます。

## TiDBクラスタのバックアップと復元 {#back-up-and-restore-tidb-cluster}

TiDBクラスタをバックアップするか、バックアップしたデータをクラスタに復元する必要がある場合は、 [BR](/br/backup-and-restore-tool.md) （バックアップと復元）を使用します。

さらに、BRを使用して[増分バックアップ](/br/use-br-command-line-tool.md#back-up-incremental-data)および[インクリメンタルリストア](/br/use-br-command-line-tool.md#restore-incremental-data)のTiDBクラスタデータを実行することもできます。

## データをTiDBに移行する {#migrate-data-to-tidb}

TiDBクラスタから別のTiDBクラスタにデータを移行する必要がある場合は、 [Dumpling](/dumpling-overview.md)を使用してTiDBからSQLダンプファイルとして完全なデータをエクスポートし、次に[TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)を使用して別のTiDBクラスタにデータをインポートします。

インクリメンタルデータも移行する必要がある場合は、 [TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md)を使用します。

## TiDBインクリメンタルデータサブスクリプション {#tidb-incremental-data-subscription}

TiDBの増分変更をサブスクライブする必要がある場合は、 [TiDB Binlog](/tidb-binlog/binlog-consumer-client.md)を使用します。
