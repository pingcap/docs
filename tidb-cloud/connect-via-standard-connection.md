---
title: Connect to TiDB Cloud Dedicated via Public Connection
summary: パブリック接続を介してTiDB Cloudクラスターに接続する方法を学習します。
---

# パブリック接続経由​​でTiDB Cloud Dedicated に接続 {#connect-to-tidb-cloud-dedicated-via-public-connection}

このドキュメントでは、パブリック接続を介してTiDB Cloud Dedicatedクラスターに接続する方法について説明します。パブリック接続はトラフィックフィルター付きのパブリックエンドポイントを公開するため、ノートパソコンからSQLクライアントを介してTiDB Cloud Dedicatedクラスターに接続できます。

> **ヒント：**
>
> パブリック接続を介してTiDB Cloud Serverless クラスターに接続する方法については、 [パブリックエンドポイント経由でTiDB Cloud Serverless に接続する](/tidb-cloud/connect-via-standard-connection-serverless.md)参照してください。

## 前提条件: IPアクセスリストを構成する {#prerequisite-configure-ip-access-list}

パブリック接続の場合、 TiDB Cloud Dedicated は IP アクセスリストに登録されているアドレスからのクライアント接続のみを許可します。IP アクセスリストを設定していない場合は、最初の接続の前に手順[IPアクセスリストを設定する](/tidb-cloud/configure-ip-access-list.md)に従って設定してください。

## クラスターに接続する {#connect-to-the-cluster}

パブリック接続を介してTiDB Cloud Dedicated クラスターに接続するには、次の手順を実行します。

1.  ターゲット クラスターの概要ページを開きます。

    1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動します。

        > **ヒント：**
        >
        > 左上隅のコンボ ボックスを使用して、組織、プロジェクト、クラスターを切り替えることができます。

    2.  ターゲット クラスターの名前をクリックすると、概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログで、 **[接続タイプ]**ドロップダウン リストから**[パブリック]**を選択します。

    IP アクセス リストをまだ設定していない場合は、 **「IP アクセス リストの設定」を**クリックするか、手順[IPアクセスリストを設定する](/tidb-cloud/configure-ip-access-list.md)に従って、最初の接続の前に設定してください。

4.  **「CA証明書」**をクリックして、TiDBクラスタへのTLS接続用のCA証明書をダウンロードしてください。CA証明書はデフォルトでTLS 1.2バージョンをサポートしています。

5.  希望する接続方法を選択し、タブ上の接続文字列とサンプル コードを参照してクラスターに接続します。

## 次は何？ {#what-s-next}

TiDB クラスターに正常に接続すると、 [TiDBでSQL文を調べる](/basic-sql-operations.md) 。
