---
title: Scale Your TiDB Cluster
summary: Learn how to scale your TiDB Cloud cluster.
---

# TiDBクラスタをスケールする {#scale-your-tidb-cluster}

> **注記：**
>
> -   [TiDB サーバーレスクラスター](/tidb-cloud/select-cluster-tier.md#tidb-serverless)をスケールすることはできません。
> -   クラスターが**MODIFYING**ステータスにある場合、クラスターに対して新しいスケーリング操作を実行することはできません。

TiDB クラスターは次の次元でスケールできます。

-   TiDB、TiKV、 TiFlashのノード番号
-   TiDB、TiKV、 TiFlashの vCPU と RAM
-   TiKV とTiFlashのストレージ

TiDB クラスターのサイズを決定する方法については、 [TiDB サイズを決定する](/tidb-cloud/size-your-cluster.md)を参照してください。

> **注記：**
>
> TiDB または TiKV の vCPU および RAM サイズが**4 vCPU、16 GiB**に設定されている場合は、次の制限に注意してください。これらの制限を回避するには、まず[vCPU と RAM を増やす](#change-vcpu-and-ram)を実行します。
>
> -   TiDB のノード番号は 1 または 2 のみに設定でき、TiKV のノード番号は 3 に固定されます。
> -   4 vCPU TiDB は 4 vCPU TiKV でのみ使用でき、4 vCPU TiKV は 4 vCPU TiDB でのみ使用できます。
> -   TiFlashは使用できません。

## ノード番号の変更 {#change-node-number}

TiDB、TiKV、またはTiFlashノードの数を増減できます。

> **警告：**
>
> TiKV またはTiFlashノード数を減らすことは危険を伴う可能性があり、残りのノードでstorage容量の不足、過剰な CPU 使用率、または過剰なメモリ使用率が発生する可能性があります。

TiDB、TiKV、またはTiFlashノードの数を変更するには、次の手順を実行します。

1.  TiDB Cloudコンソールで、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

2.  スケーリングするクラスターの行で、 **[...]**をクリックします。

    > **ヒント：**
    >
    > あるいは、 **「クラスター」**ページでスケーリングするクラスターの名前をクリックし、右上隅にある**「...」**をクリックすることもできます。

3.  ドロップダウン メニューで**[変更]**をクリックします。 **「クラスタの変更」**ページが表示されます。

4.  **[クラスタの変更]**ページで、TiDB、TiKV、またはTiFlashノードの数を変更します。

5.  右側のペインでクラスタのサイズを確認し、 **[確認]**をクリックします。

[TiDB 専用クラスターを変更する](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster)エンドポイントを通じてTiDB Cloud API を使用して、TiDB、TiKV、またはTiFlashノードの数を変更することもできます。現在、 TiDB Cloud API はまだベータ版です。詳細については、 [TiDB CloudAPI ドキュメント](https://docs.pingcap.com/tidbcloud/api/v1beta)を参照してください。

## vCPU と RAM を変更する {#change-vcpu-and-ram}

TiDB、TiKV、またはTiFlashノードの vCPU と RAM を増減できます。

> **注記：**
>
> -   vCPU と RAM の変更は、次のクラスターでのみ使用できます。
>     -   AWS でホストされ、2022/12/31 以降に作成されました。
>     -   Google Cloud でホストされ、2023/04/26 以降に作成されました。
> -   AWS には、vCPU と RAM の変更に関するクールダウン期間があります。 TiDB クラスターが AWS でホストされている場合、 TiKV またはTiFlashのstorage、vCPU、RAM を変更した後、再度変更できるようになるまで少なくとも 6 時間待つ必要があります。

TiDB、TiKV、またはTiFlashノードの vCPU と RAM を変更するには、次の手順を実行します。

1.  TiDB Cloudコンソールで、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

2.  スケーリングするクラスターの行で、 **[...]**をクリックします。

    > **ヒント：**
    >
    > あるいは、 **「クラスター」**ページでスケーリングするクラスターの名前をクリックし、右上隅にある**「...」**をクリックすることもできます。

3.  ドロップダウン メニューで**[変更]**をクリックします。 **「クラスタの変更」**ページが表示されます。

4.  **[クラスタの変更]**ページで、TiDB、TiKV、またはTiFlashノードの vCPU と RAM を変更します。

5.  右側のペインでクラスタのサイズを確認し、 **[確認]**をクリックします。

[TiDB 専用クラスターを変更する](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster)エンドポイント経由でTiDB Cloud API を使用して、TiDB、TiKV、またはTiFlashノードの vCPU と RAM を変更することもできます。現在、 TiDB Cloud API はまだベータ版です。詳細については、 [TiDB CloudAPI ドキュメント](https://docs.pingcap.com/tidbcloud/api/v1beta)を参照してください。

## storageを変更する {#change-storage}

TiKV またはTiFlashのstorageを増やすことができます。

> **警告：**
>
> -   実行中のクラスターの場合、AWS と Google Cloud では、インプレースのstorage容量のダウングレードが許可されません。
> -   AWS にはstorage変更のクールダウン期間があります。 TiDB クラスターが AWS でホストされている場合、 TiKV またはTiFlashのstorage、vCPU、RAM を変更した後、再度変更できるようになるまで少なくとも 6 時間待つ必要があります。

TiKV またはTiFlashのstorageを変更するには、次の手順を実行します。

1.  TiDB Cloudコンソールで、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

2.  スケーリングするクラスターの行で、 **[...]**をクリックします。

    > **ヒント：**
    >
    > あるいは、 **「クラスター」**ページでスケーリングするクラスターの名前をクリックし、右上隅にある**「...」**をクリックすることもできます。

3.  ドロップダウン メニューで**[変更]**をクリックします。 **「クラスタの変更」**ページが表示されます。

4.  **[クラスタの変更]**ページで、各 TiKV ノードまたはTiFlashノードのstorageを変更します。

5.  右側のペインでクラスタのサイズを確認し、 **[確認]**をクリックします。

[TiDB 専用クラスターを変更する](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster)エンドポイント経由でTiDB Cloud API を使用して、TiKV またはTiFlashノードのstorageを変更することもできます。現在、 TiDB Cloud API はまだベータ版です。詳細については、 [TiDB CloudAPI ドキュメント](https://docs.pingcap.com/tidbcloud/api/v1beta)を参照してください。
