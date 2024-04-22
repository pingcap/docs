---
title: Configure Cluster Security Settings
summary: TiDB専用クラスターでは、rootパスワードと許可されたIPアドレスを設定できます。TiDBサーバーレスクラスターの場合は、別のドキュメントを参照してください。TiDB Cloudコンソールでプロジェクトのクラスターページに移動し、ターゲットクラスターの行でSecurity設定を選択します。ダイアログでrootパスワードと許可されるIPアドレスを構成し、適用をクリックします。クラスターの概要ページからも同様の設定が可能です。
---

# クラスタのSecurity設定を構成する {#configure-cluster-security-settings}

TiDB 専用クラスターの場合、root パスワードとクラスターへの接続を許可する IP アドレスを構成できます。

> **注記：**
>
> TiDB サーバーレス クラスターの場合、このドキュメントは適用されないため、代わりに[TiDB サーバーレスへの TLS 接続](/tidb-cloud/secure-connections-to-serverless-clusters.md)を参照してください。

1.  TiDB Cloudコンソールで、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

    > **ヒント：**
    >
    > 複数のプロジェクトがある場合は、<mdsvgicon name="icon-left-projects">左下隅の をクリックして、別のプロジェクトに切り替えます。</mdsvgicon>

2.  ターゲット クラスターの行で**[...]**をクリックし、 **[Security設定]**を選択します。

3.  **「Security設定」**ダイアログで、root パスワードと許可される IP アドレスを構成します。

    クラスターに任意の IP アドレスからアクセスできるようにするには、 **「どこからでもアクセスを許可」**をクリックします。

4.  **「適用」**をクリックします。

> **ヒント：**
>
> クラスターの概要ページを表示している場合は、ページの右上隅にある [ **...]**をクリックし、 **[Security設定]**を選択して、これらの設定も構成できます。
