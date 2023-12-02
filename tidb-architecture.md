---
title: TiDB Architecture
summary: The key architecture components of the TiDB platform
---

# TiDBアーキテクチャ {#tidb-architecture}

従来のスタンドアロン データベースと比較して、TiDB には次の利点があります。

-   柔軟かつ柔軟な拡張性を備えた分散アーキテクチャを備えています。
-   MySQL 5.7プロトコル、MySQL の共通機能および構文と完全な互換性があります。アプリケーションを TiDB に移行するために、多くの場合、コードを 1 行も変更する必要はありません。
-   少数のレプリカに障害が発生した場合の自動フェイルオーバーにより高可用性をサポートします。アプリケーションに対して透過的です。
-   ACIDトランザクションをサポートし、銀行振込などの強力な一貫性が必要なシナリオに適しています。

<CustomContent platform="tidb">

-   データの移行、複製、またはバックアップのための豊富な[データ移行ツール](/migration-overview.md)シリーズを提供します。

</CustomContent>

分散データベースとして、TiDB は複数のコンポーネントで構成されるように設計されています。これらのコンポーネントは相互に通信し、完全な TiDB システムを形成します。アーキテクチャは次のとおりです。

![TiDB Architecture](/media/tidb-architecture-v6.png)

## TiDBサーバー {#tidb-server}

[TiDBサーバー](/tidb-computing.md) 、MySQL プロトコルの接続エンドポイントを外部に公開するステートレス SQLレイヤーです。 TiDBサーバーはSQL リクエストを受信し、SQL 解析と最適化を実行し、最終的に分散実行プランを生成します。水平方向に拡張可能で、Linux Virtual Server (LVS)、HAProxy、F5 などの負荷分散コンポーネントを通じて外部に統合インターフェイスを提供します。データは保存されず、コンピューティングと SQL 分析のみを目的としており、実際のデータ読み取りリクエストを TiKV ノード (またはTiFlashノード) に送信します。

## 配置Driver(PD)サーバー {#placement-driver-pd-server}

[PDサーバー](/tidb-scheduling.md)は、クラスター全体のメタデータ管理コンポーネントです。すべての単一 TiKV ノードのリアルタイム データ分散のメタデータと TiDB クラスター全体のトポロジ構造を保存し、TiDB ダッシュボード管理 UI を提供し、分散トランザクションにトランザクション ID を割り当てます。 PDサーバーは、クラスターのメタデータを保存するだけでなく、TiKV ノードからリアルタイムで報告されるデータ分散状態に従って、特定の TiKV ノードにデータ スケジューリング コマンドを送信するため、TiDB クラスター全体の「頭脳」です。また、PDサーバーは少なくとも 3 つのノードで構成され、高可用性を備えています。奇数の PD ノードを展開することをお勧めします。

## ストレージサーバー {#storage-servers}

### TiKVサーバー {#tikv-server}

[TiKVサーバー](/tidb-storage.md)はデータの保存を担当します。 TiKV は、分散トランザクションのキーと値のstorageエンジンです。

<CustomContent platform="tidb">

[リージョン](/glossary.md#regionpeerraft-group)はデータを格納する基本単位です。各リージョンには、 StartKey から EndKey までの左が閉じて右が開いた間隔である特定のキー範囲のデータが格納されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

[リージョン](/tidb-cloud/tidb-cloud-glossary.md#region)はデータを格納する基本単位です。各リージョンには、 StartKey から EndKey までの左が閉じて右が開いた間隔である特定のキー範囲のデータが格納されます。

</CustomContent>

各 TiKV ノードには複数のリージョンが存在します。 TiKV API は、キーと値のペア レベルで分散トランザクションにネイティブ サポートを提供し、デフォルトでスナップショット分離レベルの分離をサポートします。これは、TiDB が SQL レベルで分散トランザクションをサポートする方法の中核です。 SQL ステートメントを処理した後、TiDBサーバーはSQL 実行プランを TiKV API への実際の呼び出しに変換します。したがって、データは TiKV に保存されます。 TiKV 内のすべてのデータは複数のレプリカ (デフォルトでは 3 つのレプリカ) で自動的に維持されるため、TiKV はネイティブの高可用性を備え、自動フェイルオーバーをサポートします。

### TiFlashサーバー {#tiflash-server}

[TiFlashサーバー](/tiflash/tiflash-overview.md)は特殊なタイプのstorageサーバーです。通常の TiKV ノードとは異なり、 TiFlash はデータを列ごとに保存し、主に分析処理を高速化するように設計されています。
