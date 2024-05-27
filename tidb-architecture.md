---
title: TiDB Architecture
summary: TiDBプラットフォームの主要なアーキテクチャコンポーネント
---

# TiDBアーキテクチャ {#tidb-architecture}

従来のスタンドアロン データベースと比較して、TiDB には次の利点があります。

-   柔軟で弾力的なスケーラビリティを備えた分散アーキテクチャを備えています。
-   MySQL プロトコル、MySQL の共通機能および構文と完全に互換性があります。多くの場合、アプリケーションを TiDB に移行するには、コードを 1 行も変更する必要はありません。
-   少数のレプリカに障害が発生した場合に自動フェイルオーバーを実行し、アプリケーションに対して透過的に高可用性をサポートします。
-   ACIDトランザクションをサポートしており、銀行振込などの強力な一貫性が求められるシナリオに適しています。

<CustomContent platform="tidb">

-   データの移行、複製、またはバックアップのための豊富なシリーズ[データ移行ツール](/migration-overview.md)を提供します。

</CustomContent>

分散データベースである TiDB は、複数のコンポーネントで構成されるように設計されています。これらのコンポーネントは相互に通信し、完全な TiDB システムを形成します。アーキテクチャは次のとおりです。

![TiDB Architecture](/media/tidb-architecture-v6.png)

## TiDBサーバー {#tidb-server}

[TiDBサーバー](/tidb-computing.md) 、MySQL プロトコルの接続エンドポイントを外部に公開するステートレス SQLレイヤーです。TiDBサーバーはSQL 要求を受け取り、SQL 解析と最適化を実行し、最終的に分散実行プランを生成します。水平方向に拡張可能で、TiProxy、Linux Virtual Server (LVS)、HAProxy、ProxySQL、F5 などの負荷分散コンポーネントを通じて外部に統一されたインターフェイスを提供します。データを保存せず、コンピューティングと SQL 分析のみを目的としており、実際のデータ読み取り要求を TiKV ノード (またはTiFlashノード) に送信します。

## 配置Driver(PD)サーバー {#placement-driver-pd-server}

[PDサーバー](/tidb-scheduling.md) 、クラスタ全体のメタデータ管理コンポーネントです。各 TiKV ノードのリアルタイムデータ分布と TiDB クラスタ全体のトポロジ構造のメタデータを保存し、TiDB ダッシュボード管理 UI を提供し、分散トランザクションにトランザクション ID を割り当てます。PDサーバーは、クラスタのメタデータを保存するだけでなく、TiKV ノードからリアルタイムに報告されたデータ分布状態に応じて、特定の TiKV ノードにデータスケジュールコマンドを送信するため、TiDB クラスタ全体の「頭脳」です。また、PDサーバーは少なくとも 3 つのノードで構成され、高可用性を備えています。奇数の PD ノードを展開することをお勧めします。

## ストレージサーバー {#storage-servers}

### TiKVサーバー {#tikv-server}

[TiKVサーバー](/tidb-storage.md)データの保存を担当します。TiKV は分散トランザクション キー値storageエンジンです。

<CustomContent platform="tidb">

[リージョン](/glossary.md#regionpeerraft-group)はデータを格納する基本単位です。各リージョンには、 StartKey から EndKey までの左閉じ右開きの間隔である特定のキー範囲のデータが格納されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

[リージョン](/tidb-cloud/tidb-cloud-glossary.md#region)はデータを格納する基本単位です。各リージョンには、 StartKey から EndKey までの左閉じ右開きの間隔である特定のキー範囲のデータが格納されます。

</CustomContent>

各 TiKV ノードには複数のリージョンが存在します。TiKV API は、キーと値のペア レベルでの分散トランザクションをネイティブにサポートし、デフォルトでスナップショット分離レベルの分離をサポートします。これが、TiDB が SQL レベルで分散トランザクションをサポートする方法の中核です。SQL ステートメントを処理した後、TiDBサーバーはSQL 実行プランを TiKV API への実際の呼び出しに変換します。そのため、データは TiKV に保存されます。TiKV のすべてのデータは複数のレプリカ (デフォルトでは 3 つのレプリカ) に自動的に保持されるため、TiKV はネイティブの高可用性を備え、自動フェイルオーバーをサポートします。

### TiFlashサーバー {#tiflash-server}

[TiFlashサーバー](/tiflash/tiflash-overview.md)特殊なタイプのstorageサーバーです。通常のTiKVノードとは異なり、 TiFlashは列ごとにデータを保存し、主に分析処理を高速化するように設計されています。
