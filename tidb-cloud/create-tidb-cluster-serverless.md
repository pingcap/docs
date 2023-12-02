---
title: Create a TiDB Serverless Cluster
summary: Learn how to create your TiDB Serverless cluster.
---

# TiDB サーバーレスクラスタの作成 {#create-a-tidb-serverless-cluster}

この[TiDB Cloudコンソール](https://tidbcloud.com/)では、TiDB サーバーレス クラスターを作成する方法について説明します。

> **ヒント：**
>
> TiDB 専用クラスターの作成方法については、 [TiDB 専用クラスタの作成](/tidb-cloud/create-tidb-cluster.md)を参照してください。

## あなたが始める前に {#before-you-begin}

TiDB Cloudアカウントをお持ちでない場合は、 [ここ](https://tidbcloud.com/signup)をクリックしてアカウントにサインアップしてください。

-   TiDB Cloud を使用してパスワードを管理できるように電子メールとパスワードでサインアップすることも、Google、GitHub、または Microsoft アカウントでサインアップすることもできます。
-   AWS Marketplace ユーザーの場合は、AWS Marketplace を通じてサインアップすることもできます。これを行うには、 `TiDB Cloud` in [AWSマーケットプレイス](https://aws.amazon.com/marketplace)を検索し、 TiDB Cloudに登録し、画面上の指示に従ってTiDB Cloudアカウントを設定します。
-   Google Cloud Marketplace ユーザーの場合は、Google Cloud Marketplace を通じてサインアップすることもできます。これを行うには、 `TiDB Cloud` in [Google Cloud マーケットプレイス](https://console.cloud.google.com/marketplace)を検索し、 TiDB Cloudに登録し、画面上の指示に従ってTiDB Cloudアカウントを設定します。

## ステップ {#steps}

`Organization Owner`または`Project Owner`ロールに属している場合は、次のように TiDB サーバーレス クラスターを作成できます。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、 [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

2.  **「クラスタの作成」**をクリックします。

3.  **「クラスタの作成」**ページでは、デフォルトで**サーバーレス**が選択されています。

4.  TiDB Serverless のクラウドプロバイダーは AWS です。クラスターをホストする AWS リージョンを選択できます。

5.  (オプション) [無料割り当て](/tidb-cloud/select-cluster-tier.md#usage-quota)よりも多くのstorageとコンピューティング リソースを使用する予定がある場合は、使用量制限を変更します。支払い方法を追加していない場合は、限度額を編集した後にクレジット カードを追加する必要があります。

    > **注記：**
    >
    > TiDB Cloudの組織ごとに、デフォルトで最大 5 つの TiDB サーバーレス クラスターを作成できます。さらに TiDB サーバーレス クラスターを作成するには、クレジット カードを追加し、使用量を[支出制限](/tidb-cloud/tidb-cloud-glossary.md#spending-limit)に設定する必要があります。

6.  必要に応じてデフォルトのクラスター名を更新し、 **「作成」**をクリックします。

    クラスター作成プロセスが開始され、 TiDB Cloudクラスターが約 30 秒で作成されます。

## 次は何ですか {#what-s-next}

クラスターが作成されたら、 [パブリックエンドポイント経由で TiDB サーバーレスに接続する](/tidb-cloud/connect-via-standard-connection-serverless.md)の手順に従ってクラスターのパスワードを作成します。

> **注記：**
>
> パスワードを設定しないと、クラスターに接続できません。
