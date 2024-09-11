---
title: Scale Your TiDB Cluster
summary: TiDB Cloudクラスターを拡張する方法を学びます。
---

# TiDBクラスタのスケール {#scale-your-tidb-cluster}

> **注記：**
>
> -   [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 、アプリケーションのワークロードの変化に基づいて自動的にスケーリングされます。ただし、 TiDB Cloud Serverless クラスターを手動でスケーリングすることはできません。
> -   クラスターが**MODIFYING**ステータスにある場合、そのクラスターに対して新しいスケーリング操作を実行することはできません。

TiDB クラスターは次の次元で拡張できます。

-   TiDB、TiKV、 TiFlashのノード番号
-   TiDB、TiKV、 TiFlashの vCPU と RAM
-   TiKVとTiFlashの保存

TiDB クラスターのサイズを決定する方法については、 [TiDBのサイズを決定する](/tidb-cloud/size-your-cluster.md)参照してください。

> **注記：**
>
> TiDB または TiKV の vCPU と RAM サイズが**4 vCPU、16 GiB**に設定されている場合、次の制限に注意してください。これらの制限を回避するには、まず[vCPUとRAMを増やす](#change-vcpu-and-ram)実行します。
>
> -   TiDB のノード番号は 1 または 2 にのみ設定でき、TiKV のノード番号は 3 に固定されています。
> -   4 vCPU TiDB は 4 vCPU TiKV でのみ使用でき、4 vCPU TiKV は 4 vCPU TiDB でのみ使用できます。
> -   TiFlashは利用できません。

## ノード番号を変更する {#change-node-number}

TiDB、TiKV、またはTiFlashノードの数を増減できます。

> **警告：**
>
> TiKV またはTiFlashノードの数を減らすとリスクが生じ、残りのノードでstorage容量不足、過剰な CPU 使用率、または過剰なメモリ使用率が発生する可能性があります。

TiDB、TiKV、またはTiFlashノードの数を変更するには、次の手順を実行します。

1.  TiDB Cloudコンソールで、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

2.  スケーリングするクラスターの行で、 **...**をクリックします。

    > **ヒント：**
    >
    > または、 **「クラスター」**ページでスケーリングするクラスターの名前をクリックし、右上隅の**「...」**をクリックすることもできます。

3.  ドロップダウン メニューで**[変更]**をクリックします。 **[クラスタの変更]**ページが表示されます。

4.  **[クラスタの変更]**ページで、TiDB、TiKV、またはTiFlashノードの数を変更します。

5.  右側のペインでクラスター サイズを確認し、 **[確認]**をクリックします。

[TiDB Cloud Dedicated クラスターを変更する](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster)エンドポイントを介してTiDB Cloud API を使用して、TiDB、TiKV、またはTiFlashノードの数を変更することもできます。現在、 TiDB Cloud API はまだベータ版です。詳細については、 [TiDB CloudAPI ドキュメント](https://docs.pingcap.com/tidbcloud/api/v1beta)を参照してください。

## vCPUとRAMを変更する {#change-vcpu-and-ram}

TiDB、TiKV、またはTiFlashノードの vCPU と RAM を増減できます。

> **注記：**
>
> -   vCPU と RAM の変更は、次のクラスターでのみ利用可能です。
>     -   AWS でホストされ、2022/12/31 以降に作成されました。
>     -   Google Cloud でホストされ、2023/04/26 以降に作成されました。
> -   AWS には、vCPU と RAM の変更のクールダウン期間があります。TiDB クラスターが AWS でホストされている場合、TiKV またはTiFlashのstorageまたは vCPU と RAM を変更した後、再度変更できるようになるまで少なくとも 6 時間待つ必要があります。

TiDB、TiKV、またはTiFlashノードの vCPU と RAM を変更するには、次の手順を実行します。

1.  TiDB Cloudコンソールで、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

2.  スケーリングするクラスターの行で、 **...**をクリックします。

    > **ヒント：**
    >
    > または、 **「クラスター」**ページでスケーリングするクラスターの名前をクリックし、右上隅の**「...」**をクリックすることもできます。

3.  ドロップダウン メニューで**[変更]**をクリックします。 **[クラスタの変更]**ページが表示されます。

4.  **[クラスタの変更]**ページで、TiDB、TiKV、またはTiFlashノードの vCPU と RAM を変更します。

5.  右側のペインでクラスター サイズを確認し、 **[確認]**をクリックします。

[TiDB Cloud Dedicated クラスターを変更する](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster)エンドポイントを介してTiDB Cloud API を使用して、TiDB、TiKV、またはTiFlashノードの vCPU と RAM を変更することもできます。現在、 TiDB Cloud API はまだベータ版です。詳細については、 [TiDB CloudAPI ドキュメント](https://docs.pingcap.com/tidbcloud/api/v1beta)を参照してください。

## storageの変更 {#change-storage}

TiKV またはTiFlashのstorageを増やすことができます。

> **警告：**
>
> -   実行中のクラスターの場合、AWS と Google Cloud では、インプレースstorage容量のダウングレードは許可されません。
> -   AWS には、storage変更のクールダウン期間があります。TiDB クラスターが AWS でホストされている場合、TiKV またはTiFlashのstorageまたは vCPU と RAM を変更した後、再度変更できるようになるまで少なくとも 6 時間待つ必要があります。

TiKV またはTiFlashのstorageを変更するには、次の手順を実行します。

1.  TiDB Cloudコンソールで、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

2.  スケーリングするクラスターの行で、 **...**をクリックします。

    > **ヒント：**
    >
    > または、 **「クラスター」**ページでスケーリングするクラスターの名前をクリックし、右上隅の**「...」**をクリックすることもできます。

3.  ドロップダウン メニューで**[変更]**をクリックします。 **[クラスタの変更]**ページが表示されます。

4.  **「クラスタの変更」**ページで、各 TiKV またはTiFlashノードのstorageを変更します。

5.  右側のペインでクラスター サイズを確認し、 **[確認]**をクリックします。

[TiDB Cloud Dedicated クラスターを変更する](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster)エンドポイントを介してTiDB Cloud API を使用して、TiKV ノードまたはTiFlashノードのstorageを変更することもできます。現在、 TiDB Cloud API はまだベータ版です。詳細については、 [TiDB CloudAPI ドキュメント](https://docs.pingcap.com/tidbcloud/api/v1beta)を参照してください。
