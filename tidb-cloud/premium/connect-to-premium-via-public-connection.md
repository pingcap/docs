---
title: Connect to TiDB Cloud Premium via Public Connection
summary: パブリック接続を介してTiDB Cloud Premiumに接続する方法を学びましょう。
---

# パブリック接続経由​​でTiDB Cloud Premiumに接続します {#connect-to-tidb-cloud-premium-via-public-connection}

このドキュメントでは、パブリック接続を使用してTiDB Cloud Premium インスタンスに接続する方法について説明します。パブリック接続では、トラフィックフィルタを備えたパブリックエンドポイントが公開されるため、ラップトップから SQL クライアントを介してTiDB Cloud Premium インスタンスに接続できます。

> **ヒント：**
>
> -   パブリック接続経由​​でTiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスに接続する方法については、 [パブリックエンドポイント経由でTiDB Cloud StarterまたはEssentialに接続します](/tidb-cloud/connect-via-standard-connection-serverless.md)参照してください。
> -   パブリック エンドポイント経由でTiDB Cloud Dedicatedクラスターに接続する方法については、 [パブリック接続経由​​でTiDB Cloud Dedicatedに接続します](/tidb-cloud/connect-via-standard-connection.md)を参照してください。

## 前提条件：IPアクセスリストの設定 {#prerequisite-configure-ip-access-list}

パブリック接続の場合、 TiDB Cloud Premium は IP アクセス リスト内のアドレスからのクライアント接続のみを許可します。 IP アクセス リストを設定していない場合は、最初の接続の前に[IPアクセスリストを設定する](/tidb-cloud/premium/configure-ip-access-list-premium.md)。

## インスタンスに接続します {#connect-to-the-instance}

パブリック接続を介してTiDB Cloud Premium インスタンスに接続するには、以下の手順を実行してください。

1.  対象インスタンスの概要ページを開きます。

    1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動します。

        > **ヒント：**
        >
        > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず目的の組織に切り替えてください。

    2.  対象インスタンスの名前をクリックすると、その概要ページに移動します。

2.  右上隅の**「接続」**をクリックしてください。接続ダイアログが表示されます。

3.  接続ダイアログで、 **「接続タイプ」**ドロップダウンリストから**「パブリック」**を選択します。

    IP アクセス リストを設定していない場合は、最初の接続の前に、 **[IP アクセス リストの設定] をクリックするか、「IP アクセス リストを設定する」**の手順に従って[IPアクセスリストを設定する](/tidb-cloud/premium/configure-ip-access-list-premium.md)。

4.  **「CA証明書」**をクリックすると、 TiDB Cloud PremiumインスタンスへのTLS接続に必要なCA証明書をダウンロードできます。このCA証明書はデフォルトでTLS 1.2をサポートしています。

5.  ご希望の接続方法を選択し、タブに表示されている接続文字列とサンプルコードを参照してインスタンスに接続してください。

## 次は？ {#what-s-next}

TiDB Cloud Premium インスタンスに正常に接続したら、 [TiDBを使用してSQLステートメントを探索する](/basic-sql-operations.md)ことができます。
