---
title: Connect to Your TiDB Cluster
summary: Connect to your TiDB cluster via a SQL client or SQL shell.
---

# TiDBクラスターに接続する {#connect-to-your-tidb-cluster}

TiDBクラスタがTiDB Cloud上に作成された後、次の3つの方法のいずれかを使用してTiDBクラスタに接続できます。 SQLクライアントを介して、またはTiDB CloudコンソールのSQLシェルを介してクラスタにすばやくアクセスできます。

-   SQLクライアントを介して接続する

    -   [標準接続で接続する](#connect-via-standard-connection) ：標準接続では、トラフィックフィルターを使用してパブリックエンドポイントが公開されるため、ラップトップからTiDBクラスタに接続できます。
    -   [VPCピアリングを介して接続する](#connect-via-vpc-peering) ：レイテンシーを下げてセキュリティを強化したい場合は、VPCピアリングを設定し、クラウドアカウントの対応するクラウドプロバイダーのVMインスタンスを使用してプライベートエンドポイント経由で接続します。 VPCピアリングを使用して[開発者層クラスター](/tidb-cloud/select-cluster-tier.md#developer-tier)に接続することはできないことに注意してください。

<!---->

-   [SQLシェルを介して接続する](#connect-via-sql-shell) ： TiDB SQLを試して、TiDBとMySQLの互換性をすばやくテストするか、ユーザー権限を管理します

## 標準接続で接続する {#connect-via-standard-connection}

標準接続を介してTiDBクラスタに接続するには、次の手順を実行します。

1.  [**アクティブクラスター**]ページに移動し、新しく作成したクラスタの名前をクリックします。

2.  [**接続]**をクリックします。 [ <strong>TiDBに接続</strong>]ダイアログボックスが表示されます。

3.  クラスタのトラフィックフィルターを作成します。トラフィックフィルターは、SQLクライアントを介してTiDB Cloudにアクセスすることを許可されているIPとCIDRアドレスのリストです。

    トラフィックフィルタがすでに設定されている場合は、次のサブステップをスキップします。トラフィックフィルターが空の場合は、次のサブステップを実行して追加します。

    1.  ボタンの1つをクリックして、いくつかのルールをすばやく追加します。

        -   **現在のIPアドレスを追加する**
        -   **どこからでもアクセスを許可する**

    2.  新しく追加されたIPアドレスまたはCIDR範囲のオプションの説明を提供します。

    3.  [**フィルターの作成]**をクリックして、変更を確認します。

4.  [**手順2：ダイアログボックスのSQLクライアントに接続**する]で、希望する接続方法のタブをクリックし、接続文字列を使用してクラスタに接続します。

> **ノート：**
>
> [開発者層クラスター](/tidb-cloud/select-cluster-tier.md#developer-tier)の場合、クラスタに接続するときは、クラスタのプレフィックスをユーザー名に含め、名前を引用符で囲む必要があります。詳細については、 [ユーザー名のプレフィックス](/tidb-cloud/select-cluster-tier.md#user-name-prefix)を参照してください。

## VPCピアリングを介して接続する {#connect-via-vpc-peering}

> **ノート：**
>
> VPCピアリングを使用して[開発者層クラスター](/tidb-cloud/select-cluster-tier.md#developer-tier)に接続できないため、この方法は開発者層クラスターでは機能しません。

VPCピアリングを介してTiDBクラスタに接続するには、次の手順を実行します。

1.  [**アクティブクラスター**]ページに移動し、新しく作成したクラスタの名前をクリックします。

2.  [**接続**]をクリックし、[ <strong>TiDBに接続</strong>]ダイアログで[ <strong>VPCピアリング</strong>]タブを選択します。

3.  VPCピアリングを設定します。詳細については、 [VPCピアリングを設定する](/tidb-cloud/set-up-vpc-peering-connections.md)を参照してください。

4.  [**エンドポイントの取得]**をクリックして、数分待ちます。次に、接続コマンドがダイアログに表示されます。

5.  SQLクライアントを使用して、 TiDB CloudとのVPCピアリングをセットアップしたサーバーからTiDBに接続します。

    {{< copyable "" >}}

    ```shell
    mysql -u root -h <endpoint> -P <port number> -p
    ```

## SQLシェル経由で接続 {#connect-via-sql-shell}

SQLシェルを使用してTiDBクラスタに接続するには、次の手順を実行します。

1.  [**アクティブクラスター**]ページに移動し、新しく作成したクラスタの名前をクリックします。

2.  [**接続**]をクリックし、[TiDBに<strong>接続]ダイアログで[WebSQL</strong><strong>シェル</strong>]タブを選択します。

3.  [ **SQLシェルを開く]**をクリックします。

4.  プロンプトが表示された**TiDBパスワード**行で、現在のクラスタのルートパスワードを入力します。次に、アプリケーションはTiDBクラスタに接続されます。

## 次は何ですか {#what-s-next}

TiDBクラスタに正常に接続した後、次のことができます[TiDBでSQLステートメントを調べる](https://docs.pingcap.com/tidb/stable/basic-sql-operations) 。
