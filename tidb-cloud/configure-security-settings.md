---
title: Configure Cluster Security Settings
summary: Learn how to configure the root password and allowed IP addresses to connect to your cluster.
---

# クラスタSecurity設定の構成 {#configure-cluster-security-settings}

Dedicated Tierクラスターの場合、root パスワードと許可された IP アドレスを構成して、クラスターに接続できます。

> **ノート：**
>
> Serverless Tierクラスターの場合、このドキュメントは適用されず、代わりに[Serverless Tierへの TLS 接続](/tidb-cloud/secure-connections-to-serverless-tier-clusters.md)を参照できます。

1.  TiDB Cloudコンソールで、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

    > **ヒント：**
    >
    > 複数のプロジェクトがある場合は、プロジェクト リストを表示し、左上隅の ☰ ホバー メニューから別のプロジェクトに切り替えることができます。

2.  ターゲット クラスタの行で、 **[...]**をクリックして<strong>[Security Settings]</strong>を選択します。

3.  **[Security設定]**ダイアログで、ルート パスワードと許可された IP アドレスを構成します。

    任意の IP アドレスからクラスターにアクセスできるようにするには、 **[どこからでもアクセスを許可する]**をクリックします。

4.  **[適用]**をクリックします。

> **ヒント：**
>
> クラスターの概要ページを表示している場合は、ページの右上隅にある [ **...]**をクリックし、 <strong>[Security設定]</strong>を選択して、これらの設定を構成することもできます。
