---
title: Connect to TiDB Cloud Dedicated via Public Connection
summary: パブリック接続を使用してTiDB Cloudクラスターに接続する方法を学びましょう。
---

# パブリック接続経由​​でTiDB Cloud Dedicatedに接続します {#connect-to-tidb-cloud-dedicated-via-public-connection}

このドキュメントでは、パブリック接続を介してTiDB Cloud Dedicatedクラスターに接続する方法について説明します。パブリック接続では、トラフィックフィルタを備えたパブリックエンドポイントが公開されるため、ラップトップから SQL クライアントを使用してTiDB Cloud Dedicatedクラスターに接続できます。

> **ヒント：**
>
> パブリック接続経由​​でTiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスに接続する方法については、 [パブリックエンドポイント経由でTiDB Cloud StarterまたはEssentialに接続します](/tidb-cloud/connect-via-standard-connection-serverless.md)参照してください。

## 前提条件：IPアクセスリストの設定 {#prerequisite-configure-ip-access-list}

パブリック接続の場合、 TiDB Cloud Dedicated はIP アクセス リスト内のアドレスからのクライアント接続のみを許可します。 IP アクセス リストを設定していない場合は、最初の接続の前に[IPアクセスリストを設定する](/tidb-cloud/configure-ip-access-list.md)。

## クラスターに接続します {#connect-to-the-cluster}

パブリック接続を介してTiDB Cloud Dedicatedクラスターに接続するには、以下の手順を実行してください。

1.  対象のTiDB Cloud Dedicatedクラスタの概要ページを開きます。

    1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動します。

        > **ヒント：**
        >
        > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず目的の組織に切り替えてください。

    2.  対象のTiDB Cloud Dedicatedクラスターの名前をクリックすると、その概要ページに移動します。

2.  右上隅の**「接続」**をクリックしてください。接続ダイアログが表示されます。

3.  接続ダイアログで、 **「接続タイプ」**ドロップダウンリストから**「パブリック」**を選択します。

    IP アクセス リストを設定していない場合は、最初の接続の前に、 **[IP アクセス リストの設定] をクリックするか、「IP アクセス リストを設定する」**の手順に従って[IPアクセスリストを設定する](/tidb-cloud/configure-ip-access-list.md)。

4.  **「CA証明書」**をクリックすると、TiDBクラスターへのTLS接続に必要なCA証明書をダウンロードできます。このCA証明書は、デフォルトでTLS 1.2バージョンをサポートしています。

5.  ご希望の接続方法を選択し、タブに表示されている接続文字列とサンプルコードを参照して、 TiDB Cloud Dedicatedクラスターに接続してください。

## 次は？ {#what-s-next}

TiDB クラスターに正常に接続したら、 [TiDBを使用してSQLステートメントを探索する](/basic-sql-operations.md)ことができます。
