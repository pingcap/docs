---
title: Connect to TiDB Serverless via Public Endpoint
summary: Learn how to connect to your TiDB Serverless cluster via public endpoint.
---

# パブリックエンドポイント経由で TiDB サーバーレスに接続する {#connect-to-tidb-serverless-via-public-endpoint}

このドキュメントでは、パブリック エンドポイント経由で TiDB サーバーレス クラスターに接続する方法について説明します。パブリック エンドポイントを使用すると、ラップトップから SQL クライアント経由で TiDB サーバーレス クラスターに接続できます。

> **ヒント：**
>
> パブリック エンドポイント経由で TiDB 専用クラスターに接続する方法については、 [標準接続経由で TiDB 専用に接続する](/tidb-cloud/connect-via-standard-connection.md)を参照してください。

パブリック エンドポイント経由で TiDB サーバーレス クラスターに接続するには、次の手順を実行します。

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして、その概要ページに移動します。

2.  右上隅にある**「接続」**をクリックします。接続ダイアログが表示されます。

3.  ダイアログでは、エンドポイント タイプのデフォルト設定を`Public`のままにし、優先接続方法とオペレーティング システムを選択して、対応する接続​​文字列を取得します。

    > **注記：**
    >
    > -   エンドポイント タイプを`Public`のままにすると、接続が標準の TLS 接続を介して行われることを意味します。詳細については、 [TiDB サーバーレスへの TLS 接続](/tidb-cloud/secure-connections-to-serverless-clusters.md)を参照してください。
    > -   **[エンドポイント タイプ]**ドロップダウン リストで**[プライベート]**を選択した場合、接続がプライベート エンドポイント経由であることを意味します。詳細については、 [プライベートエンドポイント経由で TiDB サーバーレスに接続する](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)を参照してください。

4.  TiDB サーバーレスでは、クラスターに[枝](/tidb-cloud/branch-overview.md)を作成できます。ブランチを作成した後、 **[ブランチ]**ドロップダウン リストからブランチへの接続を選択できます。 `main`クラスター自体を表します。

5.  パスワードをまだ設定していない場合は、 **「パスワードの生成」を**クリックしてランダムなパスワードを生成します。生成されたパスワードは再度表示されないため、パスワードを安全な場所に保存してください。

6.  接続文字列を使用してクラスターに接続します。

    > **注記：**
    >
    > TiDB サーバーレス クラスターに接続するときは、ユーザー名にクラスターのプレフィックスを含め、名前を引用符で囲む必要があります。詳細については、 [ユーザー名のプレフィックス](/tidb-cloud/select-cluster-tier.md#user-name-prefix)を参照してください。

## 次は何ですか {#what-s-next}

TiDB クラスターに正常に接続したら、 [TiDB で SQL ステートメントを探索する](/basic-sql-operations.md)を行うことができます。
