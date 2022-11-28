---
title: Scale Your TiDB Cluster
summary: Learn how to scale your TiDB Cloud cluster.
aliases: ['/tidbcloud/beta/scale-tidb-cluter']
---

# TiDBクラスタをスケーリングする {#scale-your-tidb-cluster}

> **ノート：**
>
> -   [サーバーレス階層クラスター](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)をスケーリングすることはできません。
> -   クラスターが**MODIFYING**ステータスにある場合、そのクラスターに対して新しいスケーリング操作を実行することはできません。

次のディメンションで TiDB クラスターをスケーリングできます。

-   TiDB、TiKV、TiFlash のノード番号
-   TiKVとTiFlashのノードストレージ
-   TiDB、TiKV、TiFlash のノード サイズ (vCPU とメモリを含む)

TiDB クラスターのサイズを決定する方法については、 [TiDB のサイズを決定する](/tidb-cloud/size-your-cluster.md)を参照してください。

> **ノート：**
>
> TiDB または TiKV のノード サイズが**2 vCPU、8 GiB (ベータ)**または<strong>4 vCPU、16 GiB</strong>に設定されている場合は、次の制限に注意してください。これらの制限を回避するには、最初に[ノードサイズを増やす](#increase-node-size)を実行します。
>
> -   TiDB のノード数は 1 または 2 にのみ設定でき、TiKV のノード数は 3 に固定されています。
> -   2 vCPU TiDB は 2 vCPU TiKV でのみ使用でき、2 vCPU TiKV は 2 vCPU TiDB でのみ使用できます。
> -   4 vCPU TiDB は 4 vCPU TiKV でのみ使用でき、4 vCPU TiKV は 4 vCPU TiDB でのみ使用できます。
> -   TiFlash は利用できません。

## ノード番号の変更 {#change-node-number}

TiDB、TiKV、または TiFlash ノードの数を変更できます。

### ノード数を増やす {#increase-node-number}

TiDB、TiKV、または TiFlash ノードの数を増やすには、次の手順を実行します。

1.  TiDB Cloudコンソールで、プロジェクトの [**クラスター**] ページに移動します。

2.  スケーリングするクラスターを見つけて、クラスター領域の右上隅にある [ **...** ] をクリックします。

    > **ヒント：**
    >
    > または、[クラスター] ページでスケーリングする**クラスター**の名前をクリックし、右上隅にある [ <strong>...</strong> ] をクリックすることもできます。

3.  ドロップダウン メニューで [**変更**] をクリックします。 <strong>[クラスタ</strong>の変更] ページが表示されます。

4.  **[クラスタ**の変更] ページで、TiDB、TiKV、または TiFlash ノードの数を増やします。

5.  [**確認]**をクリックします。

[Dedicated Tier クラスターを変更する](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster)のエンドポイントを介してTiDB Cloud API を使用して、TiDB、TiKV、または TiFlash ノードの数を増やすこともできます。現在、 TiDB Cloud API はまだベータ版です。詳細については、 [TiDB CloudAPI ドキュメント](https://docs.pingcap.com/tidbcloud/api/v1beta)を参照してください。

### ノード番号を減らす {#decrease-node-number}

TiDB ノードの数を減らすには、次の手順を実行します。

1.  TiDB Cloudコンソールで、プロジェクトの [**クラスター**] ページに移動します。

2.  スケーリングするクラスターを見つけて、クラスター領域の右上隅にある [ **...** ] をクリックします。

    > **ヒント：**
    >
    > または、[クラスター] ページでスケーリングする**クラスター**の名前をクリックし、右上隅にある [ <strong>...</strong> ] をクリックすることもできます。

3.  ドロップダウン メニューで [**変更**] をクリックします。 <strong>[クラスタ</strong>の変更] ページが表示されます。

4.  **[クラスタ**の変更] ページで、TiDB ノードの数を減らします。

5.  [**確認]**をクリックします。

TiKV または TiFlash ノードの数を減らすには、サポート チケットを送信する必要があります。 PingCAP サポート チームがお客様に連絡し、合意された時間内にスケーリングを完了します。

> **警告：**
>
> TiKV または TiFlash ノード番号を減らすことは危険であり、ストレージ容量が不足したり、CPU 使用率が過剰になったり、残りのノードでメモリ使用率が過剰になったりする可能性があります。

サポート チケットを送信するには、 [TiDB Cloudのサポート](/tidb-cloud/tidb-cloud-support.md)の手順を実行します。スケーリングするノードごとに、[**説明**] ボックスに次の情報を入力します。

-   クラスタ名: xxx
-   クラウド プロバイダー: GCP または AWS
-   ノードタイプ: TiKV または TiFlash
-   現在のノード番号: xxx
-   予想されるノード番号: xxx

## ノード ストレージの変更 {#change-node-storage}

TiKVまたはTiFlashのノードストレージを変更できます。

### ノード ストレージを増やす {#increase-node-storage}

TiKV または TiFlash のノード ストレージを増やすには、次の手順を実行します。

1.  TiDB Cloudコンソールで、プロジェクトの [**クラスター**] ページに移動します。

2.  スケーリングするクラスターを見つけて、クラスター領域の右上隅にある [ **...** ] をクリックします。

    > **ヒント：**
    >
    > または、[クラスター] ページでスケーリングする**クラスター**の名前をクリックし、右上隅にある [ <strong>...</strong> ] をクリックすることもできます。

3.  ドロップダウン メニューで [**変更**] をクリックします。 <strong>[クラスタ</strong>の変更] ページが表示されます。

4.  **[クラスタ**の変更] ページで、TiKV または TiFlash のノード ストレージを増やします。

5.  [**確認]**をクリックします。

[Dedicated Tier クラスターを変更する](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster)エンドポイントを介してTiDB Cloud API を使用して、TiKV または TiFlash ノードのストレージを増やすこともできます。現在、 TiDB Cloud API はまだベータ版です。詳細については、 [TiDB CloudAPI ドキュメント](https://docs.pingcap.com/tidbcloud/api/v1beta)を参照してください。

> **ノート：**
>
> AWS には、ノード ストレージの変更のクールダウン期間があります。 TiDB クラスターが AWS によってホストされている場合、TiKV または TiFlash のノード ストレージを変更した後、再度変更するには、少なくとも 6 時間待つ必要があります。

### ノード ストレージを減らす {#decrease-node-storage}

実行中のクラスタの場合、AWS と Google Cloud はインプレース ストレージ容量のダウングレードを許可しません。

## ノードサイズを大きくする {#increase-node-size}

現在、クラスターの実行中は、そのノード サイズを増やすことはできません。バックアップと復元によってのみノード サイズを増やすことができます。

[クラスターの最新のバックアップを作成する](/tidb-cloud/backup-and-restore.md#manual-backup) 、そして[クラスタを削除します](/tidb-cloud/delete-tidb-cluster.md)のときにノード サイズを増やす必要があり[削除されたクラスターを復元する](/tidb-cloud/backup-and-restore.md#restore-a-deleted-cluster) 。この方法を実行する前に、次の影響が許容できることを確認してください。

-   バックアップ中またはバックアップ後のデータ損失を回避するには、バックアップを作成する前に、SQL クライアントを介したクラスターへの接続を停止する必要があります。
-   クラスターへの接続を停止すると、復元プロセスが完了するまで、このクラスターで実行されているアプリケーションは正常にサービスを提供できません。
