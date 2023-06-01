---
title: Scale Your TiDB Cluster
summary: Learn how to scale your TiDB Cloud cluster.
---

# TiDBクラスタを拡張する {#scale-your-tidb-cluster}

> **ノート：**
>
> -   [<a href="/tidb-cloud/select-cluster-tier.md#serverless-tier-beta">Serverless Tierクラスター</a>](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)をスケールすることはできません。
> -   クラスターが**MODIFYING**ステータスにある場合、クラスターに対して新しいスケーリング操作を実行することはできません。

TiDB クラスターは次の次元でスケールできます。

-   TiDB、TiKV、 TiFlashのノード番号
-   TiKV とTiFlashのノードstorage
-   TiDB、TiKV、 TiFlashのノード サイズ (vCPU とメモリを含む)

TiDB クラスターのサイズを決定する方法については、 [<a href="/tidb-cloud/size-your-cluster.md">TiDB サイズを決定する</a>](/tidb-cloud/size-your-cluster.md)を参照してください。

> **ノート：**
>
> TiDB または TiKV のノード サイズが**2 vCPU、8 GiB (ベータ版)**または**4 vCPU、16 GiB**に設定されている場合は、次の制限事項に注意してください。これらの制限を回避するには、まず[<a href="#increase-node-size">ノードサイズを増やす</a>](#increase-node-size)を実行します。
>
> -   TiDB のノード数は 1 または 2 のみに設定でき、TiKV のノード数は 3 に固定されます。
> -   2 vCPU TiDB は 2 vCPU TiKV でのみ使用でき、2 vCPU TiKV は 2 vCPU TiDB でのみ使用できます。
> -   4 vCPU TiDB は 4 vCPU TiKV でのみ使用でき、4 vCPU TiKV は 4 vCPU TiDB でのみ使用できます。
> -   TiFlashは使用できません。

## ノード番号の変更 {#change-node-number}

TiDB、TiKV、またはTiFlashノードの数を変更できます。

### ノード数を増やす {#increase-node-number}

TiDB、TiKV、またはTiFlashノードの数を増やすには、次の手順を実行します。

1.  TiDB Cloudコンソールで、プロジェクトの[<a href="https://tidbcloud.com/console/clusters">**クラスター**</a>](https://tidbcloud.com/console/clusters)ページに移動します。

2.  スケーリングするクラスターの行で、 **[...]**をクリックします。

    > **ヒント：**
    >
    > あるいは、 **「クラスター」**ページでスケーリングするクラスターの名前をクリックし、右上隅にある**「...」**をクリックすることもできます。

3.  ドロップダウン メニューで**[変更]**をクリックします。 **「クラスタの変更」**ページが表示されます。

4.  **[クラスタの変更]**ページで、TiDB、TiKV、またはTiFlashノードの数を増やします。

5.  **「確認」**をクリックします。

[<a href="https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster">Dedicated Tierクラスターを変更する</a>](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster)エンドポイントを通じてTiDB CloudAPI を使用して、TiDB、TiKV、またはTiFlashノードの数を増やすこともできます。現在、 TiDB Cloud API はまだベータ版です。詳細については、 [<a href="https://docs.pingcap.com/tidbcloud/api/v1beta">TiDB CloudAPI ドキュメント</a>](https://docs.pingcap.com/tidbcloud/api/v1beta)を参照してください。

### ノード番号を減らす {#decrease-node-number}

TiDB ノードの数を減らすには、次の手順を実行します。

1.  TiDB Cloudコンソールで、プロジェクトの[<a href="https://tidbcloud.com/console/clusters">**クラスター**</a>](https://tidbcloud.com/console/clusters)ページに移動します。

2.  スケーリングするクラスターの行で、 **[...]**をクリックします。

    > **ヒント：**
    >
    > あるいは、 **「クラスター」**ページでスケーリングするクラスターの名前をクリックし、右上隅にある**「...」**をクリックすることもできます。

3.  ドロップダウン メニューで**[変更]**をクリックします。 **「クラスタの変更」**ページが表示されます。

4.  **[クラスタの変更]**ページで、TiDB ノードの数を減らします。

5.  **「確認」**をクリックします。

TiKV またはTiFlashノードの数を減らすには、サポート チケットを送信する必要があります。 PingCAP サポート チームから連絡があり、合意された時間内にスケーリングを完了します。

> **警告：**
>
> TiKV またはTiFlashノード数を減らすことは危険を伴う可能性があり、残りのノードでstorage容量の不足、過剰な CPU 使用率、または過剰なメモリ使用率が発生する可能性があります。

サポート チケットを送信するには、 [<a href="/tidb-cloud/tidb-cloud-support.md">TiDB Cloudのサポート</a>](/tidb-cloud/tidb-cloud-support.md)の手順を実行します。スケーリングするノードごとに、 **[説明]**ボックスに次の情報を入力します。

-   クラスタ名: xxx
-   クラウドプロバイダー: GCP または AWS
-   ノードタイプ: TiKV またはTiFlash
-   現在のノード番号: xxx
-   予期されるノード番号: xxx

## ノードstorageを変更する {#change-node-storage}

TiKV またはTiFlashのノードstorageを変更できます。

### ノードstorageを増やす {#increase-node-storage}

> **ノート：**
>
> AWS にはノードstorageの変更のクールダウン期間があります。 TiDB クラスターが AWS でホストされている場合、 TiKV またはTiFlashのノードstorageまたはノード サイズを変更した後、再度変更できるようになるまで少なくとも 6 時間待つ必要があります。

TiKV またはTiFlashのノードstorageを増やすには、次の手順を実行します。

1.  TiDB Cloudコンソールで、プロジェクトの[<a href="https://tidbcloud.com/console/clusters">**クラスター**</a>](https://tidbcloud.com/console/clusters)ページに移動します。

2.  スケーリングするクラスターの行で、 **[...]**をクリックします。

    > **ヒント：**
    >
    > あるいは、 **「クラスター」**ページでスケーリングするクラスターの名前をクリックし、右上隅にある**「...」**をクリックすることもできます。

3.  ドロップダウン メニューで**[変更]**をクリックします。 **「クラスタの変更」**ページが表示されます。

4.  **[クラスタの変更]**ページで、 TiKV またはTiFlashのノードstorageを増やします。

5.  **「確認」**をクリックします。

[<a href="https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster">Dedicated Tierクラスターを変更する</a>](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster)エンドポイントを通じてTiDB CloudAPI を使用して、TiKV またはTiFlashノードのstorageを増やすこともできます。現在、 TiDB Cloud API はまだベータ版です。詳細については、 [<a href="https://docs.pingcap.com/tidbcloud/api/v1beta">TiDB CloudAPI ドキュメント</a>](https://docs.pingcap.com/tidbcloud/api/v1beta)を参照してください。

### ノードstorageを減らす {#decrease-node-storage}

実行中のクラスターの場合、AWS と Google Cloud では、インプレースのstorage容量のダウングレードが許可されません。

## ノードサイズを増やす {#increase-node-size}

> **ノート：**
>
> -   ノード サイズの増加は、AWS でホストされ、2022/12/31 以降に作成されたクラスターでのみ利用できます。
> -   AWS にはノード サイズ変更のクールダウン期間があります。 TiDB クラスターが AWS でホストされている場合、 TiKV またはTiFlashのノードstorageまたはノード サイズを変更した後、再度変更できるようになるまで少なくとも 6 時間待つ必要があります。

TiDB、TiKV、およびTiFlashのノード サイズを増やすことができます。ノード サイズの縮小はサポートされていません。

ノード サイズを増やすには、次の手順を実行します。

1.  TiDB Cloudコンソールで、プロジェクトの**「クラスター」**ページに移動します。
2.  スケーリングするクラスターの行で、 **[...]**をクリックします。
3.  ドロップダウン メニューで**[変更]**をクリックします。 **「クラスタの変更」**ページが表示されます。
4.  **[クラスタの変更]**ページで、必要に応じてノード サイズを増やします。
5.  **「確認」**をクリックします。
