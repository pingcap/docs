---
title: TiDB Tools Use Cases
summary: TiDB ツールの一般的な使用例とツールの選択方法について学習します。
---

# TiDB ツールの使用例 {#tidb-tools-use-cases}

このドキュメントでは、TiDB ツールの一般的な使用例と、シナリオに適したツールを選択する方法について説明します。

## 物理マシンまたは仮想マシンにTiDBをデプロイて運用する {#deploy-and-operate-tidb-on-physical-or-virtual-machines}

物理マシンまたは仮想マシンに TiDB を展開して操作する必要がある場合は、 [TiUP](/tiup/tiup-overview.md)インストールし、 TiUP を使用して TiDB、PD、TiKV などの TiDB コンポーネントを管理できます。

## Kubernetes 上で TiDB をデプロイて運用する {#deploy-and-operate-tidb-on-kubernetes}

Kubernetes 上で TiDB をデプロイして運用する必要がある場合は、まず Kubernetes クラスターをデプロイし、次に[TiDB Operator](https://docs.pingcap.com/tidb-in-kubernetes/stable)デプロイします。その後、 TiDB Operator を使用して TiDB クラスターをデプロイして運用します。

## CSVからTiDBにデータをインポートする {#import-data-from-csv-to-tidb}

他のツールによってエクスポートされた互換性のある CSV ファイルを TiDB にインポートする必要がある場合は、 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)使用します。

## MySQL/ Auroraから完全なデータをインポート {#import-full-data-from-mysql-aurora}

MySQL/ Auroraから完全なデータをインポートする必要がある場合は、まず[Dumpling](/dumpling-overview.md)使用してデータを SQL ダンプ ファイルとしてエクスポートし、次に[TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)使用してデータを TiDB クラスターにインポートします。

## MySQL/ Auroraからデータを移行する {#migrate-data-from-mysql-aurora}

MySQL/ Auroraから全データと増分データの両方を移行する必要がある場合は、 [TiDB データ移行](/dm/dm-overview.md) (DM) を使用して[Amazon Auroraから TiDB へのデータ移行](/migrate-aurora-to-tidb.md)実行します。

全データ量が大きい場合 (TB レベル)、最初に[Dumpling](/dumpling-overview.md)と[TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)使用して全データ移行を実行し、次に DM を使用して増分データ移行を実行できます。

## TiDB クラスターのバックアップと復元 {#back-up-and-restore-tidb-cluster}

TiDB クラスターをバックアップする必要がある場合、またはバックアップしたデータをクラスターに復元する必要がある場合は、 [BR](/br/backup-and-restore-overview.md) (バックアップと復元) を使用します。

また、 BR はTiDB クラスター データの[増分バックアップ](/br/br-incremental-guide.md#back-up-incremental-data)と[増分復元](/br/br-incremental-guide.md#restore-incremental-data)実行するためにも使用できます。

## データをTiDBに移行する {#migrate-data-to-tidb}

TiDB クラスターから別の TiDB クラスターにデータを移行する必要がある場合は、 [Dumpling](/dumpling-overview.md)使用して TiDB から完全なデータを SQL ダンプ ファイルとしてエクスポートし、 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)使用してデータを別の TiDB クラスターにインポートします。

増分データも移行する必要がある場合は、 [ティCDC](/ticdc/ticdc-overview.md)使用できます。

## TiDB 増分データサブスクリプション {#tidb-incremental-data-subscription}

TiDB の増分変更をサブスクライブする必要がある場合は、 [ティCDC](/ticdc/ticdc-overview.md)使用できます。
