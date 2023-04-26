---
title: Scale Your TiDB Cluster
summary: Learn how to scale your TiDB Cloud cluster.
---

# TiDBクラスタをスケーリングする {#scale-your-tidb-cluster}

> **ノート：**
>
> -   [Serverless Tierクラスター](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)をスケーリングすることはできません。
> -   クラスターが**MODIFYING**ステータスにある場合、そのクラスターに対して新しいスケーリング操作を実行することはできません。

次のディメンションで TiDB クラスターをスケーリングできます。

-   TiDB、TiKV、 TiFlashのノード番号
-   TiKVとTiFlashのノードstorage
-   TiDB、TiKV、およびTiFlashのノード サイズ (vCPU とメモリを含む)

TiDB クラスターのサイズを決定する方法については、 [TiDB のサイズを決定する](/tidb-cloud/size-your-cluster.md)を参照してください。

> **ノート：**
>
> TiDB または TiKV のノード サイズが**2 vCPU、8 GiB (ベータ)**または<strong>4 vCPU、16 GiB</strong>に設定されている場合は、次の制限に注意してください。これらの制限を回避するには、最初に[ノードサイズを増やす](#change-node-size)を実行します。
>
> -   TiDB のノード数は 1 または 2 にのみ設定でき、TiKV のノード数は 3 に固定されています。
> -   2 vCPU TiDB は 2 vCPU TiKV でのみ使用でき、2 vCPU TiKV は 2 vCPU TiDB でのみ使用できます。
> -   4 vCPU TiDB は 4 vCPU TiKV でのみ使用でき、4 vCPU TiKV は 4 vCPU TiDB でのみ使用できます。
> -   TiFlashは利用できません。

## ノード番号の変更 {#change-node-number}

TiDB、TiKV、またはTiFlashノードの数を増減できます。

> **警告：**
>
> TiKV またはTiFlashノード番号を減らすことは危険であり、storage容量が不足したり、CPU 使用率が過剰になったり、残りのノードでメモリ使用率が過剰になったりする可能性があります。

TiDB、TiKV、またはTiFlashノードの数を変更するには、次の手順を実行します。

1.  TiDB Cloudコンソールで、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

2.  スケーリングするクラスターの行で、 **[...]**をクリックします。

    > **ヒント：**
    >
    > または、 **[クラスター]**ページでスケーリングするクラスターの名前をクリックし、右上隅にある<strong>[...]</strong>をクリックすることもできます。

3.  ドロップダウン メニューで**[変更]**をクリックします。 <strong>[クラスタの変更]</strong>ページが表示されます。

4.  **[クラスタの変更]**ページで、TiDB、TiKV、またはTiFlashノードの数を変更します。

5.  **[確認]**をクリックします。

[Dedicated Tierクラスターを変更する](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster)エンドポイントを介してTiDB Cloud API を使用して、TiDB、TiKV、またはTiFlashノードの数を変更することもできます。現在、 TiDB Cloud API はまだベータ版です。詳細については、 [TiDB CloudAPI ドキュメント](https://docs.pingcap.com/tidbcloud/api/v1beta)を参照してください。

## ノードstorageの変更 {#change-node-storage}

TiKV またはTiFlashのノードstorageを増やすことができます。

> **警告：**
>
> -   実行中のクラスタの場合、AWS と Google Cloud はインプレースstorage容量のダウングレードを許可しません。
> -   AWS には、ノードstorageの変更のクールダウン期間があります。 TiDB クラスターが AWS でホストされている場合、TiKV またはTiFlashのノードstorageまたはノード サイズを変更した後、再度変更するには、少なくとも 6 時間待つ必要があります。

TiKV またはTiFlashのノードstorageを変更するには、次の手順を実行します。

1.  TiDB Cloudコンソールで、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

2.  スケーリングするクラスターの行で、 **[...]**をクリックします。

    > **ヒント：**
    >
    > または、 **[クラスター]**ページでスケーリングするクラスターの名前をクリックし、右上隅にある<strong>[...]</strong>をクリックすることもできます。

3.  ドロップダウン メニューで**[変更]**をクリックします。 <strong>[クラスタの変更]</strong>ページが表示されます。

4.  **[クラスタの変更]**ページで、TiKV またはTiFlashのノードstorageを変更します。

5.  **[確認]**をクリックします。

[Dedicated Tierクラスターを変更する](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster)エンドポイントを介してTiDB Cloud API を使用して、TiKV またはTiFlashノードのstorageを変更することもできます。現在、 TiDB Cloud API はまだベータ版です。詳細については、 [TiDB CloudAPI ドキュメント](https://docs.pingcap.com/tidbcloud/api/v1beta)を参照してください。

## ノード サイズの変更 {#change-node-size}

TiDB、TiKV、またはTiFlashノードのサイズ (vCPU とメモリを含む) を増減できます。

> **ノート：**
>
> -   ノード サイズの変更は、AWS でホストされ、2022/12/31 以降に作成されたクラスターでのみ使用できます。
> -   AWS には、ノード サイズの変更のクールダウン期間があります。 TiDB クラスターが AWS でホストされている場合、TiKV またはTiFlashのノードstorageまたはノード サイズを変更した後、再度変更するには、少なくとも 6 時間待つ必要があります。

TiDB、TiKV、またはTiFlashノードのサイズを変更するには、次の手順を実行します。

1.  TiDB Cloudコンソールで、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

2.  スケーリングするクラスターの行で、 **[...]**をクリックします。

    > **ヒント：**
    >
    > または、 **[クラスター]**ページでスケーリングするクラスターの名前をクリックし、右上隅にある<strong>[...]</strong>をクリックすることもできます。

3.  ドロップダウン メニューで**[変更]**をクリックします。 <strong>[クラスタの変更]</strong>ページが表示されます。

4.  **[クラスタの変更]**ページで、TiDB、TiKV、またはTiFlashノードのサイズを変更します。

5.  **[確認]**をクリックします。

[Dedicated Tierクラスターを変更する](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster)エンドポイントを介してTiDB Cloud API を使用して、TiDB、TiKV、またはTiFlashノードのサイズを変更することもできます。現在、 TiDB Cloud API はまだベータ版です。詳細については、 [TiDB CloudAPI ドキュメント](https://docs.pingcap.com/tidbcloud/api/v1beta)を参照してください。
