---
title: Configure Cluster Security Settings
summary: Learn how to configure the root password and allowed IP addresses to connect to your cluster.
---

# クラスタのSecurity設定を構成する {#configure-cluster-security-settings}

Dedicated Tierクラスターの場合、root パスワードとクラスターへの接続を許可する IP アドレスを構成できます。

> **ノート：**
>
> Serverless Tierクラスターの場合、このドキュメントは適用されないため、代わりに[<a href="/tidb-cloud/secure-connections-to-serverless-tier-clusters.md">Serverless Tierクラスターへのセキュリティ接続</a>](/tidb-cloud/secure-connections-to-serverless-tier-clusters.md)を参照してください。

1.  TiDB Cloudコンソールで、プロジェクトの[<a href="https://tidbcloud.com/console/clusters">**クラスター**</a>](https://tidbcloud.com/console/clusters)ページに移動します。

    > **ヒント：**
    >
    > 複数のプロジェクトがある場合は、 **「クラスター」**ページの左側のナビゲーション・ペインでターゲット・プロジェクトに切り替えることができます。

2.  ターゲット クラスターの行で**[...]**をクリックし、 **[Security設定]**を選択します。

3.  **「Security設定」**ダイアログで、root パスワードと許可される IP アドレスを構成します。

    クラスターに任意の IP アドレスからアクセスできるようにするには、 **「どこからでもアクセスを許可」**をクリックします。

4.  **「適用」**をクリックします。

> **ヒント：**
>
> クラスターの概要ページを表示している場合は、ページの右上隅にある [ **...]**をクリックし、 **[Security設定]**を選択して、これらの設定も構成できます。
