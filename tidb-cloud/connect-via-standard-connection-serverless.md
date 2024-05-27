---
title: Connect to TiDB Serverless via Public Endpoint
summary: パブリック エンドポイント経由で TiDB Serverless クラスターに接続する方法を学習します。
---

# パブリックエンドポイント経由でTiDB Serverlessに接続する {#connect-to-tidb-serverless-via-public-endpoint}

このドキュメントでは、パブリック エンドポイント経由で TiDB Serverless クラスターに接続する方法について説明します。パブリック エンドポイントを使用すると、ラップトップから SQL クライアント経由で TiDB Serverless クラスターに接続できます。

> **ヒント：**
>
> パブリック エンドポイント経由で TiDB 専用クラスターに接続する方法については、 [標準接続を介してTiDB専用に接続する](/tidb-cloud/connect-via-standard-connection.md)参照してください。

パブリック エンドポイント経由で TiDB Serverless クラスターに接続するには、次の手順を実行します。

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  ダイアログでは、エンドポイント タイプのデフォルト設定を`Public`のままにして、希望する接続方法とオペレーティング システムを選択して、対応する接続​​文字列を取得します。

    > **注記：**
    >
    > -   エンドポイント タイプを`Public`のままにしておくと、接続は標準の TLS 接続を介して行われます。詳細については、 [TiDB サーバーレスへの TLS 接続](/tidb-cloud/secure-connections-to-serverless-clusters.md)を参照してください。
    > -   **「エンドポイント タイプ」**ドロップダウン リストで**「プライベート」**を選択した場合、接続はプライベート エンドポイント経由で行われることを意味します。詳細については、 [プライベートエンドポイント経由で TiDB Serverless に接続する](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)を参照してください。

4.  TiDB Serverless を使用すると、クラスターに[枝](/tidb-cloud/branch-overview.md)作成できます。ブランチが作成されたら、**ブランチ**ドロップダウン リストからブランチに接続するように選択できます。5 `main`クラスター自体を表します。

5.  まだパスワードを設定していない場合は、 **「パスワードの生成」**をクリックしてランダムなパスワードを生成します。生成されたパスワードは再度表示されないので、パスワードは安全な場所に保存してください。

6.  接続文字列を使用してクラスターに接続します。

    > **注記：**
    >
    > TiDB Serverless クラスターに接続する場合は、ユーザー名にクラスターのプレフィックスを含め、名前を引用符で囲む必要があります。詳細については、 [ユーザー名プレフィックス](/tidb-cloud/select-cluster-tier.md#user-name-prefix)参照してください。

## 次は何ですか {#what-s-next}

TiDB クラスターに正常に接続されたら、 [TiDBでSQL文を調べる](/basic-sql-operations.md)実行できます。
