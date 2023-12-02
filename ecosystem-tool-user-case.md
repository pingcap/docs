---
title: TiDB Tools Use Cases
summary: Learn the common use cases of TiDB tools and how to choose the tools.
---

# TiDB ツールの使用例 {#tidb-tools-use-cases}

このドキュメントでは、TiDB ツールの一般的な使用例と、シナリオに適したツールを選択する方法を紹介します。

## TiDB を物理マシンまたは仮想マシンにデプロイ運用する {#deploy-and-operate-tidb-on-physical-or-virtual-machines}

TiDB を物理マシンまたは仮想マシンに展開して操作する必要がある場合は、 [TiUP](/tiup/tiup-overview.md)インストールし、 TiUPを使用して TiDB、PD、TiKV などの TiDB コンポーネントを管理できます。

## TiDB を Kubernetes 上にデプロイ運用する {#deploy-and-operate-tidb-on-kubernetes}

TiDB を Kubernetes 上にデプロイして操作する必要がある場合は、Kubernetes クラスターをデプロイしてから[TiDB Operator](https://docs.pingcap.com/tidb-in-kubernetes/stable)をデプロイできます。その後、 TiDB Operator を使用して TiDB クラスターをデプロイおよび操作できるようになります。

## CSV から TiDB にデータをインポート {#import-data-from-csv-to-tidb}

他のツールによってエクスポートされた互換性のある CSV ファイルを TiDB にインポートする必要がある場合は、 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)使用します。

## MySQL/ Auroraから完全なデータをインポート {#import-full-data-from-mysql-aurora}

MySQL/ Auroraから完全なデータをインポートする必要がある場合は、まず[Dumpling](/dumpling-overview.md)を使用してデータを SQL ダンプ ファイルとしてエクスポートし、次に[TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)を使用してデータを TiDB クラスターにインポートします。

## MySQL/ Auroraからデータを移行する {#migrate-data-from-mysql-aurora}

MySQL/ Auroraから完全データと増分データの両方を移行する必要がある場合は、 [TiDB データ移行](/dm/dm-overview.md) (DM) を使用して[Amazon Auroraから TiDB へのデータの移行](/migrate-aurora-to-tidb.md)を実行します。

全データ ボリュームが大きい場合 (TB レベル)、最初に[Dumpling](/dumpling-overview.md)と[TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)を使用して完全データ移行を実行し、次に DM を使用して増分データ移行を実行できます。

## TiDB クラスターのバックアップと復元 {#back-up-and-restore-tidb-cluster}

TiDB クラスターをバックアップするか、バックアップされたデータをクラスターに復元する必要がある場合は、 [BR](/br/backup-and-restore-overview.md) (バックアップと復元) を使用します。

さらに、 BR を使用して TiDB クラスター データの[増分バックアップ](/br/br-incremental-guide.md#back-up-incremental-data)と[増分復元](/br/br-incremental-guide.md#restore-incremental-data)を実行することもできます。

## データを TiDB に移行する {#migrate-data-to-tidb}

TiDB クラスターから別の TiDB クラスターにデータを移行する必要がある場合は、 [Dumpling](/dumpling-overview.md)を使用して TiDB から完全なデータを SQL ダンプ ファイルとしてエクスポートし、次に[TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)使用してデータを別の TiDB クラスターにインポートします。

増分データも移行する必要がある場合は、 [TiCDC](/ticdc/ticdc-overview.md)を使用できます。

## TiDB 増分データ サブスクリプション {#tidb-incremental-data-subscription}

TiDB の増分変更をサブスクライブする必要がある場合は、 [TiCDC](/ticdc/ticdc-overview.md)を使用できます。
