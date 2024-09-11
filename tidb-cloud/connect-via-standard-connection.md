---
title: Connect to TiDB Cloud Dedicated via Public Connection
summary: パブリック接続を介してTiDB Cloudクラスターに接続する方法を学習します。
---

# パブリック接続経由​​でTiDB Cloud Dedicatedに接続する {#connect-to-tidb-cloud-dedicated-via-public-connection}

このドキュメントでは、パブリック接続を介してTiDB Cloud Dedicated クラスターに接続する方法について説明します。パブリック接続はトラフィック フィルター付きのパブリック エンドポイントを公開するため、ラップトップから SQL クライアントを介してTiDB Cloud Dedicated クラスターに接続できます。

> **ヒント：**
>
> パブリック接続を介してTiDB Cloud Serverless クラスターに接続する方法については、 [パブリックエンドポイント経由でTiDB Cloud Serverlessに接続する](/tidb-cloud/connect-via-standard-connection-serverless.md)を参照してください。

## 前提条件: IPアクセスリストを構成する {#prerequisite-configure-ip-access-list}

パブリック接続の場合、 TiDB Cloud Dedicated は IP アクセス リスト内のアドレスからのクライアント接続のみを許可します。IP アクセス リストを設定していない場合は、最初の接続の前に[IPアクセスリストを構成する](/tidb-cloud/configure-ip-access-list.md)手順に従って設定してください。

## クラスターに接続する {#connect-to-the-cluster}

パブリック接続を介してTiDB Cloud Dedicated クラスターに接続するには、次の手順を実行します。

1.  ターゲット クラスターの概要ページを開きます。

    1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

        > **ヒント：**
        >
        > 複数のプロジェクトがある場合は、<mdsvgicon name="icon-left-projects">左下隅にある をクリックして、別のプロジェクトに切り替えます。</mdsvgicon>

    2.  ターゲット クラスターの名前をクリックすると、概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログで、 **「接続タイプ」**ドロップダウンリストから**「パブリック」**を選択します。

    IP アクセス リストを設定していない場合は、 **「IP アクセス リストの設定」**をクリックするか、手順[IPアクセスリストを構成する](/tidb-cloud/configure-ip-access-list.md)に従って最初の接続の前に設定してください。

4.  **CA 証明書**をクリックして、TiDB クラスターへの TLS 接続用の CA 証明書をダウンロードします。CA 証明書は、デフォルトで TLS 1.2 バージョンをサポートします。

5.  希望する接続方法を選択し、タブの接続文字列とサンプル コードを参照してクラスターに接続します。

## 次は何か {#what-s-next}

TiDB クラスターに正常に接続されたら、 [TiDBでSQL文を調べる](/basic-sql-operations.md)実行できます。
