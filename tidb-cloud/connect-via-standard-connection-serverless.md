---
title: Connect to TiDB Cloud Serverless via Public Endpoint
summary: パブリック エンドポイント経由でTiDB Cloud Serverless クラスターに接続する方法を学習します。
---

# パブリックエンドポイント経由でTiDB Cloud Serverlessに接続する {#connect-to-tidb-cloud-serverless-via-public-endpoint}

このドキュメントでは、コンピューターから SQL クライアントを使用してパブリック エンドポイント経由でTiDB Cloud Serverless クラスターに接続する方法と、パブリック エンドポイントを無効にする方法について説明します。

## パブリックエンドポイント経由で接続する {#connect-via-a-public-endpoint}

> **ヒント：**
>
> パブリック エンドポイント経由でTiDB Cloud Dedicated クラスターに接続する方法については、 [パブリック接続経由​​でTiDB Cloud Dedicatedに接続する](/tidb-cloud/connect-via-standard-connection.md)参照してください。

パブリック エンドポイント経由でTiDB Cloud Serverless クラスターに接続するには、次の手順を実行します。

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  ダイアログでは、接続タイプのデフォルト設定を`Public`のままにして、希望する接続方法とオペレーティング システムを選択して、対応する接続文字列を取得します。

    > **注記：**
    >
    > -   接続タイプを`Public`のままにしておくと、接続は標準の TLS 接続を介して行われることを意味します。詳細については、 [TiDB Cloud ServerlessへのTLS接続](/tidb-cloud/secure-connections-to-serverless-clusters.md)参照してください。
    > -   **「接続タイプ」**ドロップダウン リストで**「プライベート エンドポイント」**を選択した場合、接続はプライベート エンドポイント経由で行われることを意味します。詳細については、 [プライベートエンドポイント経由でTiDB Cloud Serverless に接続する](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)参照してください。

4.  TiDB Cloud Serverless を使用すると、クラスターに[枝](/tidb-cloud/branch-overview.md)作成できます。ブランチが作成されたら、**ブランチ**ドロップダウン リストからブランチに接続するように選択できます。5 `main`クラスター自体を表します。

5.  まだパスワードを設定していない場合は、 **「パスワードの生成」をクリックしてランダムなパスワード**を生成します。生成されたパスワードは再度表示されないので、パスワードは安全な場所に保存してください。

6.  接続文字列を使用してクラスターに接続します。

    > **注記：**
    >
    > TiDB Cloud Serverless クラスターに接続する場合は、ユーザー名にクラスターのプレフィックスを含め、名前を引用符で囲む必要があります。詳細については、 [ユーザー名プレフィックス](/tidb-cloud/select-cluster-tier.md#user-name-prefix)参照してください。

## パブリックエンドポイントを無効にする {#disable-a-public-endpoint}

TiDB Cloud Serverless クラスターのパブリック エンドポイントを使用する必要がない場合は、それを無効にしてインターネットからの接続を防ぐことができます。

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  左側のナビゲーション ペインで**[ネットワーク]**をクリックし、右側のペインで**[無効]**をクリックします。確認ダイアログが表示されます。

3.  確認ダイアログで**「無効にする」**をクリックします。

パブリック エンドポイントを無効にすると、接続ダイアログの**[接続タイプ]**ドロップダウン リストの`Public`番目のエントリが無効になります。ユーザーが引き続きパブリック エンドポイントからクラスターにアクセスしようとすると、エラーが発生します。

> **注記：**
>
> パブリック エンドポイントを無効にしても、既存の接続には影響しません。インターネットからの新しい接続が防止されるだけです。

パブリック エンドポイントを無効にした後、再度有効にすることができます。

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  左側のナビゲーション ペインで**[ネットワーク]**をクリックし、右側のペインで**[有効化]**をクリックします。

## 次は何か {#what-s-next}

TiDB クラスターに正常に接続されたら、 [TiDBでSQL文を調べる](/basic-sql-operations.md)実行できます。
