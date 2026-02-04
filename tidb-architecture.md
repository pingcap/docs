---
title: TiDB Architecture
summary: TiDBプラットフォームの主要なアーキテクチャコンポーネント
---

# TiDBアーキテクチャ {#tidb-architecture}

<CustomContent platform="tidb-cloud">

TiDB には、クラシック TiDBアーキテクチャと[TiDB Xアーキテクチャ](/tidb-cloud/tidb-x-architecture.md)という 2 つのアーキテクチャがあります。このドキュメントでは、クラシック TiDBアーキテクチャについて説明します。

</CustomContent>

従来のスタンドアロン データベースと比較して、TiDB には次の利点があります。

-   柔軟で弾力的なスケーラビリティを備えた分散アーキテクチャを備えています。
-   MySQLプロトコル、共通機能、構文と完全に互換性があります。多くの場合、アプリケーションをTiDBに移行する際に、コードを1行も変更する必要はありません。
-   少数のレプリカに障害が発生した場合に自動フェイルオーバーを実行し、アプリケーションに対して透過的に高可用性をサポートします。
-   ACIDトランザクションをサポートしており、銀行振込などの強力な一貫性が求められるシナリオに適しています。

<CustomContent platform="tidb">

-   データの移行、複製、またはバックアップのための豊富なシリーズ[データ移行ツール](/migration-overview.md)を提供します。

</CustomContent>

分散データベースであるTiDBは、複数のコンポーネントで構成されるように設計されています。これらのコンポーネントは相互に通信し、完全なTiDBシステムを形成します。アーキテクチャは次のとおりです。

![TiDB Architecture](/media/tidb-architecture-v6.png)

## TiDBサーバー {#tidb-server}

[TiDBサーバー](/tidb-computing.md)はステートレスSQLレイヤーであり、MySQLプロトコルの接続エンドポイントを外部に公開します。TiDBサーバーはSQLリクエストを受け取り、SQL解析と最適化を実行し、最終的に分散実行プランを生成します。水平スケーラブルで、TiProxy、Linux Virtual Server（LVS）、HAProxy、ProxySQL、F5などの負荷分散コンポーネントを介して外部に統一されたインターフェースを提供します。データの保存は行わず、コンピューティングとSQL分析のみを行い、実際のデータ読み取りリクエストをTiKVノード（またはTiFlashノード）に送信します。

## 配置Driver（PD）サーバー {#placement-driver-pd-server}

[PDサーバー](/tidb-scheduling.md)はクラスタ全体のメタデータ管理コンポーネントです。各TiKVノードのリアルタイムデータ分布とTiDBクラスタ全体のトポロジ構造に関するメタデータを保存し、TiDBダッシュボード管理UIを提供し、分散トランザクションにトランザクションIDを割り当てます。PDサーバーは、クラスタのメタデータを保存するだけでなく、TiKVノードからリアルタイムに報告されるデータ分布状態に基づいて、特定のTiKVノードにデータスケジューリングコマンドを送信するため、TiDBクラスタ全体の「頭脳」と言えます。また、PDサーバーは少なくとも3ノードで構成され、高い可用性を備えています。奇数個のPDノードを配置することをお勧めします。

## ストレージサーバー {#storage-servers}

### TiKVサーバー {#tikv-server}

[TiKVサーバー](/tidb-storage.md)はデータの保存を担当します。TiKVは分散トランザクションキーバリューstorageエンジンです。

<CustomContent platform="tidb">

[リージョン](/glossary.md#regionpeerraft-group)はデータを格納する基本単位です。各リージョンには、StartKeyからEndKeyまでの左閉じ右開きの区間である特定のキー範囲のデータが格納されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

[リージョン](/tidb-cloud/tidb-cloud-glossary.md#region)はデータを格納する基本単位です。各リージョンには、StartKeyからEndKeyまでの左閉じ右開きの区間である特定のキー範囲のデータが格納されます。

</CustomContent>

各 TiKV ノードには複数のリージョンが存在します。TiKV API は、キーと値のペアレベルでの分散トランザクションをネイティブにサポートし、デフォルトでスナップショット分離レベルの分離をサポートします。これは、TiDB が SQL レベルで分散トランザクションをサポートする方法の中核です。TiDBサーバーはSQL 文を処理した後、SQL 実行プランを TiKV API への実際の呼び出しに変換します。そのため、データは TiKV に保存されます。TiKV 内のすべてのデータは複数のレプリカ（デフォルトでは 3 つのレプリカ）に自動的に保持されるため、TiKV はネイティブの高可用性を備え、自動フェイルオーバーをサポートします。

### TiFlashサーバー {#tiflash-server}

[TiFlashサーバー](/tiflash/tiflash-overview.md)は特殊なタイプのstorageサーバーです。通常のTiKVノードとは異なり、 TiFlashはデータを列単位で保存し、主に分析処理の高速化を目的として設計されています。
