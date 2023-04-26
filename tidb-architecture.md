---
title: TiDB Architecture
summary: The key architecture components of the TiDB platform
---

# TiDBアーキテクチャ {#tidb-architecture}

従来のスタンドアロン データベースと比較して、TiDB には次の利点があります。

-   柔軟で弾力性のあるスケーラビリティを備えた分散アーキテクチャを備えています。
-   MySQL 5.7プロトコル、MySQL の一般的な機能および構文と完全に互換性があります。アプリケーションを TiDB に移行するために、多くの場合、コードを 1 行も変更する必要はありません。
-   少数のレプリカに障害が発生した場合の自動フェイルオーバーで高可用性をサポートします。アプリケーションに対して透過的です。
-   ACIDトランザクションをサポートし、銀行振込などの強力な一貫性が必要なシナリオに適しています。

<CustomContent platform="tidb">

-   データの移行、複製、またはバックアップのための豊富な一連の[データ移行ツール](/migration-overview.md)を提供します。

</CustomContent>

分散データベースとして、TiDB は複数のコンポーネントで構成されるように設計されています。これらのコンポーネントは相互に通信し、完全な TiDB システムを形成します。アーキテクチャは次のとおりです。

![TiDB Architecture](/media/tidb-architecture-v6.png)

## TiDBサーバー {#tidb-server}

[TiDBサーバー](/tidb-computing.md) 、MySQL プロトコルの接続エンドポイントを外部に公開するステートレス SQLレイヤーです。 TiDBサーバーはSQL 要求を受け取り、SQL の解析と最適化を実行し、最終的に分散実行計画を生成します。水平方向にスケーラブルであり、Linux Virtual Server (LVS)、HAProxy、F5 などの負荷分散コンポーネントを介して、外部への統合インターフェイスを提供します。データを保存せず、計算と SQL 分析のみを行い、実際のデータ読み取り要求を TiKV ノード (またはTiFlashノード) に送信します。

## 配置Driver(PD)サーバー {#placement-driver-pd-server}

[PDサーバー](/tidb-scheduling.md)は、クラスター全体のメタデータ管理コンポーネントです。すべての単一の TiKV ノードのリアルタイム データ配信のメタデータと TiDB クラスター全体のトポロジ構造を格納し、TiDB ダッシュボード管理 UI を提供し、トランザクション ID を分散トランザクションに割り当てます。 PDサーバーは、TiDB クラスター全体の「頭脳」です。クラスターのメタデータを保存するだけでなく、TiKV ノードからリアルタイムで報告されるデータ配信状態に従って、特定の TiKV ノードにデータ スケジューリング コマンドを送信するからです。また、PDサーバーは少なくとも 3 つのノードで構成され、高可用性を備えています。奇数の PD ノードを展開することをお勧めします。

## ストレージサーバー {#storage-servers}

### TiKVサーバー {#tikv-server}

[TiKVサーバー](/tidb-storage.md)はデータの保存を担当します。 TiKV は、分散トランザクション キー値storageエンジンです。

<CustomContent platform="tidb">

[リージョン](/glossary.md#regionpeerraft-group)はデータを格納する基本単位です。各リージョンには、 StartKey から EndKey までの左が閉じて右が開いた間隔である特定のキー範囲のデータが格納されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

[リージョン](/tidb-cloud/tidb-cloud-glossary.md#region)はデータを格納する基本単位です。各リージョンには、 StartKey から EndKey までの左が閉じて右が開いた間隔である特定のキー範囲のデータが格納されます。

</CustomContent>

各 TiKV ノードには複数のリージョンが存在します。 TiKV API は、キーと値のペア レベルで分散トランザクションをネイティブにサポートし、デフォルトでスナップショット分離レベルの分離をサポートします。これは、TiDB が SQL レベルで分散トランザクションをサポートする方法の中核です。 SQL ステートメントを処理した後、TiDBサーバーはSQL 実行計画を TiKV API への実際の呼び出しに変換します。したがって、データはTiKVに保存されます。 TiKV のすべてのデータは、複数のレプリカ (デフォルトでは 3 つのレプリカ) で自動的に維持されるため、TiKV はネイティブの高可用性を備え、自動フェイルオーバーをサポートします。

### TiFlashサーバー {#tiflash-server}

[TiFlashサーバー](/tiflash/tiflash-overview.md)は特殊なタイプのstorageサーバーです。通常の TiKV ノードとは異なり、 TiFlash は主に分析処理を高速化するように設計された列ごとにデータを保存します。
