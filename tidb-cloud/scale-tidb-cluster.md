---
title: Scale Your TiDB Cluster
summary: Learn how to scale your TiDB Cloud cluster.
---

# TiDBクラスタを拡張する {#scale-your-tidb-cluster}

> **ノート：**
>
> -   [<a href="/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta">TiDB サーバーレスクラスター</a>](/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta)をスケールすることはできません。
> -   クラスターが**MODIFYING**ステータスにある場合、クラスターに対して新しいスケーリング操作を実行することはできません。

TiDB クラスターは次の次元でスケールできます。

-   TiDB、TiKV、 TiFlashのノード番号
-   TiKV とTiFlashのノードstorage
-   TiDB、TiKV、 TiFlashのノード サイズ (vCPU とメモリを含む)

TiDB クラスターのサイズを決定する方法については、 [<a href="/tidb-cloud/size-your-cluster.md">TiDB サイズを決定する</a>](/tidb-cloud/size-your-cluster.md)を参照してください。

> **ノート：**
>
> TiDB または TiKV のノード サイズが**2 vCPU、8 GiB (ベータ版)**または**4 vCPU、16 GiB**に設定されている場合は、次の制限事項に注意してください。これらの制限を回避するには、まず[<a href="#change-node-size">ノードサイズを増やす</a>](#change-node-size)を実行します。
>
> -   TiDB のノード数は 1 または 2 のみに設定でき、TiKV のノード数は 3 に固定されます。
> -   2 vCPU TiDB は 2 vCPU TiKV でのみ使用でき、2 vCPU TiKV は 2 vCPU TiDB でのみ使用できます。
> -   4 vCPU TiDB は 4 vCPU TiKV でのみ使用でき、4 vCPU TiKV は 4 vCPU TiDB でのみ使用できます。
> -   TiFlashは使用できません。

## ノード番号の変更 {#change-node-number}

TiDB、TiKV、またはTiFlashノードの数を増減できます。

> **警告：**
>
> TiKV またはTiFlashノード数を減らすことは危険を伴う可能性があり、残りのノードでstorage容量の不足、過剰な CPU 使用率、または過剰なメモリ使用率が発生する可能性があります。

TiDB、TiKV、またはTiFlashノードの数を変更するには、次の手順を実行します。

1.  TiDB Cloudコンソールで、プロジェクトの[<a href="https://tidbcloud.com/console/clusters">**クラスター**</a>](https://tidbcloud.com/console/clusters)ページに移動します。

2.  スケーリングするクラスターの行で、 **[...]**をクリックします。

    > **ヒント：**
    >
    > あるいは、 **「クラスター」**ページでスケーリングするクラスターの名前をクリックし、右上隅にある**「...」**をクリックすることもできます。

3.  ドロップダウン メニューで**[変更]**をクリックします。 **「クラスタの変更」**ページが表示されます。

4.  **[クラスタの変更]**ページで、TiDB、TiKV、またはTiFlashノードの数を変更します。

5.  **「確認」**をクリックします。

[<a href="https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster">TiDB 専用クラスターを変更する</a>](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster)エンドポイントを通じてTiDB Cloud API を使用して、TiDB、TiKV、またはTiFlashノードの数を変更することもできます。現在、 TiDB Cloud API はまだベータ版です。詳細については、 [<a href="https://docs.pingcap.com/tidbcloud/api/v1beta">TiDB CloudAPI ドキュメント</a>](https://docs.pingcap.com/tidbcloud/api/v1beta)を参照してください。

## ノードstorageを変更する {#change-node-storage}

TiKV またはTiFlashのノードstorageを増やすことができます。

> **警告：**
>
> -   実行中のクラスターの場合、AWS と Google Cloud では、インプレースのstorage容量のダウングレードが許可されません。
> -   AWS にはノードstorageの変更のクールダウン期間があります。 TiDB クラスターが AWS でホストされている場合、 TiKV またはTiFlashのノードstorageまたはノード サイズを変更した後、再度変更できるようになるまで少なくとも 6 時間待つ必要があります。

TiKV またはTiFlashのノードstorageを変更するには、次の手順を実行します。

1.  TiDB Cloudコンソールで、プロジェクトの[<a href="https://tidbcloud.com/console/clusters">**クラスター**</a>](https://tidbcloud.com/console/clusters)ページに移動します。

2.  スケーリングするクラスターの行で、 **[...]**をクリックします。

    > **ヒント：**
    >
    > あるいは、 **「クラスター」**ページでスケーリングするクラスターの名前をクリックし、右上隅にある**「...」**をクリックすることもできます。

3.  ドロップダウン メニューで**[変更]**をクリックします。 **「クラスタの変更」**ページが表示されます。

4.  **[クラスタの変更]**ページで、TiKV またはTiFlashのノードstorageを変更します。

5.  **「確認」**をクリックします。

[<a href="https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster">TiDB 専用クラスターを変更する</a>](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster)エンドポイント経由でTiDB Cloud API を使用して、TiKV またはTiFlashノードのstorageを変更することもできます。現在、 TiDB Cloud API はまだベータ版です。詳細については、 [<a href="https://docs.pingcap.com/tidbcloud/api/v1beta">TiDB CloudAPI ドキュメント</a>](https://docs.pingcap.com/tidbcloud/api/v1beta)を参照してください。

## ノードサイズの変更 {#change-node-size}

TiDB、TiKV、またはTiFlashノードのサイズ (vCPU とメモリを含む) を増減できます。

> **ノート：**
>
> -   ノード サイズの変更は、次のクラスターでのみ使用できます。
>     -   AWS でホストされ、2022/12/31 以降に作成されました。
>     -   GCP でホストされ、2023/04/26 以降に作成されました。
> -   AWS にはノード サイズ変更のクールダウン期間があります。 TiDB クラスターが AWS でホストされている場合、 TiKV またはTiFlashのノードstorageまたはノード サイズを変更した後、再度変更できるようになるまで少なくとも 6 時間待つ必要があります。

TiDB、TiKV、またはTiFlashノードのサイズを変更するには、次の手順を実行します。

1.  TiDB Cloudコンソールで、プロジェクトの[<a href="https://tidbcloud.com/console/clusters">**クラスター**</a>](https://tidbcloud.com/console/clusters)ページに移動します。

2.  スケーリングするクラスターの行で、 **[...]**をクリックします。

    > **ヒント：**
    >
    > あるいは、 **「クラスター」**ページでスケーリングするクラスターの名前をクリックし、右上隅にある**「...」**をクリックすることもできます。

3.  ドロップダウン メニューで**[変更]**をクリックします。 **「クラスタの変更」**ページが表示されます。

4.  **[クラスタの変更]**ページで、TiDB、TiKV、またはTiFlashノードのサイズを変更します。

5.  **「確認」**をクリックします。

[<a href="https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster">TiDB 専用クラスターを変更する</a>](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster)エンドポイント経由でTiDB Cloud API を使用して、TiDB、TiKV、またはTiFlashノードのサイズを変更することもできます。現在、 TiDB Cloud API はまだベータ版です。詳細については、 [<a href="https://docs.pingcap.com/tidbcloud/api/v1beta">TiDB CloudAPI ドキュメント</a>](https://docs.pingcap.com/tidbcloud/api/v1beta)を参照してください。
