---
title: Connect via Standard Connection
summary: Learn how to connect to your TiDB Cloud cluster via standard connection.
---

# 標準接続で接続する {#connect-via-standard-connection}

このドキュメントでは、標準接続を介してTiDB Cloudクラスターに接続する方法について説明します。標準接続では、トラフィック フィルターを備えたパブリック エンドポイントが公開されるため、ラップトップから SQL クライアント経由で TiDB クラスターに接続できます。

標準接続は、TiDB Serverlessと TiDB Dedicatedの両方で使用できます。

## TiDB Serverless {#tidb-serverless}

標準接続経由で TiDB Serverless クラスターに接続するには、次の手順を実行します。

1.  [<a href="https://tidbcloud.com/console/clusters">**クラスター**</a>](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして、その概要ページに移動します。

2.  右上隅にある**「接続」**をクリックします。接続ダイアログが表示されます。

3.  ダイアログでは、エンドポイント タイプのデフォルト設定を`Public`のままにし、優先接続方法とオペレーティング システムを選択して、対応する接続​​文字列を取得します。

    > **ノート：**
    >
    > -   エンドポイント タイプを`Public`のままにすると、接続が標準の TLS 接続を介して行われることを意味します。詳細については、 [<a href="/tidb-cloud/secure-connections-to-serverless-tier-clusters.md">TiDB Serverlessへの TLS 接続</a>](/tidb-cloud/secure-connections-to-serverless-tier-clusters.md)を参照してください。
    > -   **[エンドポイント タイプ]**ドロップダウン リストで**[プライベート]**を選択した場合、接続がプライベート エンドポイント経由であることを意味します。詳細については、 [<a href="/tidb-cloud/set-up-private-endpoint-connections.md#tidb-serverless">プライベートエンドポイント経由で接続する</a>](/tidb-cloud/set-up-private-endpoint-connections.md#tidb-serverless)を参照してください。

4.  パスワードをまだ設定していない場合は、 **「パスワードの作成」**をクリックしてランダムなパスワードを生成します。生成されたパスワードは再度表示されないため、パスワードを安全な場所に保存してください。

5.  接続文字列を使用してクラスターに接続します。

    > **ノート：**
    >
    > TiDB Serverless クラスターに接続するときは、ユーザー名にクラスターのプレフィックスを含め、名前を引用符で囲む必要があります。詳細については、 [<a href="/tidb-cloud/select-cluster-tier.md#user-name-prefix">ユーザー名のプレフィックス</a>](/tidb-cloud/select-cluster-tier.md#user-name-prefix)を参照してください。

## TiDB Dedicated {#tidb-dedicated}

標準接続経由で TiDB Dedicatedクラスターに接続するには、次の手順を実行します。

1.  ターゲットクラスターの概要ページを開きます。

    1.  [<a href="https://tidbcloud.com/">TiDB Cloudコンソール</a>](https://tidbcloud.com/)にログインし、プロジェクトの[<a href="https://tidbcloud.com/console/clusters">**クラスター**</a>](https://tidbcloud.com/console/clusters)ページに移動します。

        > **ヒント：**
        >
        > 複数のプロジェクトがある場合は、プロジェクト リストを表示し、左上隅にある ☰ ホバー メニューから別のプロジェクトに切り替えることができます。

    2.  ターゲット クラスターの名前をクリックして、その概要ページに移動します。

2.  右上隅にある**「接続」**をクリックします。接続ダイアログが表示されます。

3.  クラスターのトラフィック フィルターを作成します。トラフィック フィルターは、SQL クライアント経由でTiDB Cloudへのアクセスを許可される IP および CIDR アドレスのリストです。

    トラフィック フィルターがすでに設定されている場合は、次のサブステップをスキップしてください。トラフィック フィルターが空の場合は、次のサブ手順を実行してトラフィック フィルターを追加します。

    1.  いずれかのボタンをクリックして、ルールをすばやく追加します。

        -   **現在の IP アドレスを追加**
        -   **どこからでもアクセスを許可する**

    2.  新しく追加された IP アドレスまたは CIDR 範囲の説明をオプションで入力します。

    3.  **「フィルターの作成」**をクリックして変更を確認します。

4.  ダイアログの**「ステップ 2: TiDB クラスター CA をダウンロードする」で**、TiDB クラスターへの TLS 接続用の**TiDB クラスター CA をダウンロードするを**クリックします。 TiDB クラスター CA は、デフォルトで TLS 1.2 バージョンをサポートします。

    > **ノート：**
    >
    > -   TiDB クラスター CA は、TiDB Dedicatedクラスターでのみ使用できます。
    > -   現在、 TiDB Cloud は、MySQL、MyCLI、JDBC、Python、Go、Node.js の接続方法の接続文字列とサンプル コードのみを提供しています。

5.  ダイアログの**「ステップ 3: SQL クライアントに接続する」**で、希望する接続方法のタブをクリックし、タブ上の接続文字列とサンプル コードを参照してクラスターに接続します。

    ダウンロードした CA ファイルのパスを、接続文字列の`--ssl-ca`オプションの引数として使用する必要があることに注意してください。

## 次は何ですか {#what-s-next}

TiDB クラスターに正常に接続したら、 [<a href="/basic-sql-operations.md">TiDB で SQL ステートメントを探索する</a>](/basic-sql-operations.md)を行うことができます。
