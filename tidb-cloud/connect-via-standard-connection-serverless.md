---
title: Connect to TiDB Cloud Starter or Essential via Public Endpoint
summary: パブリックエンドポイントを介して、 TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスに接続する方法を学びましょう。
---

# パブリックエンドポイント経由でTiDB Cloud StarterまたはEssentialに接続します {#connect-to-tidb-cloud-starter-or-essential-via-public-endpoint}

このドキュメントでは、コンピュータ上のSQLクライアントを使用してパブリックエンドポイント経由でTiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスに接続する方法、およびパブリックエンドポイントを無効にする方法について説明します。

## 公開エンドポイント経由で接続します {#connect-via-a-public-endpoint}

> **ヒント：**
>
> パブリック エンドポイント経由でTiDB Cloud Dedicatedクラスターに接続する方法については、 [パブリック接続経由​​でTiDB Cloud Dedicatedに接続します](/tidb-cloud/connect-via-standard-connection.md)を参照してください。

パブリックエンドポイント経由でTiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスに接続するには、以下の手順を実行してください。

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud StarterまたはEssentialインスタンスの名前をクリックして、概要ページに移動します。

2.  右上隅の**「接続」**をクリックしてください。接続ダイアログが表示されます。

3.  ダイアログでは、接続タイプのデフォルト設定を`Public`のままにして、希望する接続方法とオペレーティングシステムを選択して、対応する接続​​文字列を取得します。

    <CustomContent language="en,zh">

    > **注記：**
    >
    > -   接続タイプを`Public`のままにすると、接続が標準の TLS 接続を介して行われることを意味します。詳細については、 [TiDB Cloud StarterまたはEssentialへのTLS接続](/tidb-cloud/secure-connections-to-serverless-clusters.md)を参照してください。
    > -   **接続タイプの**ドロップダウンリストで**「プライベートエンドポイント」**を選択した場合、接続はプライベートエンドポイント経由で行われます。詳細については、以下のドキュメントを参照してください。
    >
    >     -   [AWS PrivateLink経由でTiDB Cloud StarterまたはEssentialに接続します。](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)
    >     -   [Alibaba Cloudプライベートエンドポイント経由でTiDB Cloud StarterまたはEssentialに接続します。](/tidb-cloud/set-up-private-endpoint-connections-on-alibaba-cloud.md)

    </CustomContent>

    <CustomContent language="ja">

    > **注記：**
    >
    > -   接続タイプを`Public`のままにすると、接続が標準の TLS 接続を介して行われることを意味します。詳細については、 [TiDB Cloud StarterまたはEssentialへのTLS接続](/tidb-cloud/secure-connections-to-serverless-clusters.md)を参照してください。
    > -   **[接続タイプ]**ドロップダウン リストで**[プライベート エンドポイント]**を選択した場合、接続がプライベート エンドポイント経由であることを意味します。詳細については、 [AWS PrivateLink経由でTiDB Cloud StarterまたはEssentialに接続します。](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)参照してください。

    </CustomContent>

4.  TiDB Cloud、 TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンス用に[支店](/tidb-cloud/branch-overview.md)を作成できます。ブランチが作成されると、**ブランチの**ドロップダウン リストからブランチに接続できます。 `main` TiDB Cloud StarterまたはEssentialインスタンス自体を表します。

5.  まだパスワードを設定していない場合は、 **「パスワードを生成」をクリックしてランダムなパスワード**を生成してください。生成されたパスワードは二度と表示されませんので、安全な場所に保存してください。

6.  接続文字列を使用して、 TiDB Cloud StarterまたはEssentialインスタンスに接続します。

    > **注記：**
    >
    > TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスに接続するときは、ユーザー名にTiDB Cloud Starterまたは TiDB Cloud Essentialインスタンスのプレフィックスを含め、名前を引用符で囲む必要があります。詳細については、 [ユーザー名の接頭辞](/tidb-cloud/select-cluster-tier.md#user-name-prefix)参照してください。クライアント IP は、TiDB Cloud StarterまたはEssentialインスタンスのパブリック エンドポイントの許可された IP ルールに含まれている必要があります。詳細については、 [パブリックエンドポイント向けにTiDB Cloud StarterまたはEssential Firewallルールを設定する](/tidb-cloud/configure-serverless-firewall-rules-for-public-endpoints.md)参照してください。

## 公開エンドポイントを無効にする {#disable-a-public-endpoint}

TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスのパブリックエンドポイントを使用する必要がない場合は、インターネットからの接続を防止するために、そのエンドポイントを無効にすることができます。

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud StarterまたはEssentialインスタンスの名前をクリックして、概要ページに移動します。

2.  左側のナビゲーションペインで、 **[設定]** &gt; **[ネットワーク]**をクリックします。

3.  **ネットワーク設定**ページで、 **「無効にする」**をクリックします。確認ダイアログが表示されます。

4.  確認ダイアログで**「無効にする」**をクリックしてください。

パブリックエンドポイントを無効にすると、接続ダイアログの**「接続タイプ」**ドロップダウンリストにある`Public`エントリが無効になります。ユーザーがパブリックエンドポイントからTiDB Cloud StarterまたはEssentialインスタンスにアクセスしようとすると、エラーが発生します。

> **注記：**
>
> パブリックエンドポイントを無効にしても、既存の接続には影響しません。インターネットからの新規接続のみを防止します。

パブリックエンドポイントを無効化した後、再度有効化することができます。

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud StarterまたはEssentialインスタンスの名前をクリックして、概要ページに移動します。

2.  左側のナビゲーションペインで、 **[設定]** &gt; **[ネットワーク]**をクリックします。

3.  **ネットワークの**ページで、 **[有効にする]**をクリックします。

## 次は？ {#what-s-next}

TiDB Cloud StarterまたはEssentialインスタンスに正常に接続したら、 [TiDBを使用してSQLステートメントを探索する](/basic-sql-operations.md)ことができます。
