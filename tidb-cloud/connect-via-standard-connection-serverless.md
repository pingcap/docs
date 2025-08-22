---
title: Connect to {{{ .starter }}} or Essential via Public Endpoint
summary: パブリック エンドポイント経由で {{{ .starter }}} または {{{ .essential }}} クラスターに接続する方法について説明します。
---

# パブリックエンドポイント経由で {{{ .starter }}} または Essential に接続する {#connect-to-starter-or-essential-via-public-endpoint}

このドキュメントでは、コンピューターから SQL クライアントを使用してパブリック エンドポイント経由で {{{ .starter }}} または {{{ .essential }}} クラスターに接続する方法と、パブリック エンドポイントを無効にする方法について説明します。

## パブリックエンドポイント経由で接続する {#connect-via-a-public-endpoint}

> **ヒント：**
>
> パブリック エンドポイント経由でTiDB Cloud Dedicated クラスターに接続する方法については、 [パブリック接続経由​​でTiDB Cloud Dedicated に接続](/tidb-cloud/connect-via-standard-connection.md)参照してください。

パブリックエンドポイント経由で {{{ .starter }}} または {{{ .essential }}} クラスターに接続するには、次の手順を実行します。

1.  [**クラスター**](https://tidbcloud.com/project/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  ダイアログでは、接続タイプのデフォルト設定を`Public`のままにして、希望する接続方法とオペレーティング システムを選択して、対応する接続文字列を取得します。

    <CustomContent language="en,zh">

    > **注記：**
    >
    > -   接続タイプを`Public`ままにしておくと、標準のTLS接続が使用されます。詳細については、 [{{{ .starter }}} または Essential への TLS 接続](/tidb-cloud/secure-connections-to-serverless-clusters.md)参照してください。
    > -   **「接続タイプ」**ドロップダウンリストで**「プライベートエンドポイント」**を選択した場合、接続はプライベートエンドポイント経由となります。詳細については、以下のドキュメントをご覧ください。
    >
    >     -   [AWS PrivateLink 経由で {{{ .starter }}} に接続する](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)
    >     -   [Alibaba Cloud プライベートエンドポイント経由で {{{ .starter }}} または Essential に接続する](/tidb-cloud/set-up-private-endpoint-connections-on-alibaba-cloud.md)

    </CustomContent>

    <CustomContent language="ja">

    > **注記：**
    >
    > -   接続タイプを`Public`ままにしておくと、標準のTLS接続が使用されます。詳細については、 [{{{ .starter }}} または Essential への TLS 接続](/tidb-cloud/secure-connections-to-serverless-clusters.md)参照してください。
    > -   **「接続タイプ」**ドロップダウンリストで**「プライベートエンドポイント」**を選択した場合、接続はプライベートエンドポイント経由となります。詳細については、 [AWS PrivateLink 経由で {{{ .starter }}} に接続する](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)参照してください。

    </CustomContent>

4.  TiDB Cloud、{{{ .starter }}} または {{{ .essential }}} クラスター用に[枝](/tidb-cloud/branch-overview.md)作成できます。ブランチを作成したら、 **「ブランチ」**ドロップダウンリストからそのブランチに接続できます。5 `main`クラスター自体を表します。

5.  まだパスワードを設定していない場合は、 **「パスワードを生成」**をクリックしてランダムなパスワードを生成します。生成されたパスワードは再度表示されないため、安全な場所に保存してください。

6.  接続文字列を使用してクラスターに接続します。

    > **注記：**
    >
    > {{{ .starter }}} または {{{ .essential }}} クラスターに接続する場合は、ユーザー名にクラスターのプレフィックスを含め、名前を引用符で囲む必要があります。詳細については、 [ユーザー名のプレフィックス](/tidb-cloud/select-cluster-tier.md#user-name-prefix)参照してください。クライアント IP は、クラスターのパブリックエンドポイントの許可 IP ルールに含まれている必要があります。詳細については、 [パブリックエンドポイントの {{{ .starter }}} または必須のファイアウォールルールを構成する](/tidb-cloud/configure-serverless-firewall-rules-for-public-endpoints.md)参照してください。

## パブリックエンドポイントを無効にする {#disable-a-public-endpoint}

{{{ .starter }}} または {{{ .essential }}} クラスターのパブリックエンドポイントを使用する必要がない場合は、それを無効にしてインターネットからの接続を防ぐことができます。

1.  [**クラスター**](https://tidbcloud.com/project/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  左側のナビゲーション ペインで、 **[設定]** &gt; **[ネットワーク] を**クリックします。

3.  **「ネットワーク」**ページで、 **「無効にする」**をクリックします。確認ダイアログが表示されます。

4.  確認ダイアログで**「無効にする」を**クリックします。

パブリックエンドポイントを無効化すると、接続ダイアログの「**接続タイプ」**ドロップダウンリストの`Public`番目のエントリが無効化されます。ユーザーが引き続きパブリックエンドポイントからクラスターにアクセスしようとすると、エラーが発生します。

> **注記：**
>
> パブリックエンドポイントを無効にしても、既存の接続には影響しません。インターネットからの新規接続のみがブロックされます。

パブリック エンドポイントを無効にした後、再度有効にすることができます。

1.  [**クラスター**](https://tidbcloud.com/project/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  左側のナビゲーション ペインで、 **[設定]** &gt; **[ネットワーク] を**クリックします。

3.  **[ネットワーク]**ページで、 **[有効化]**をクリックします。

## 次は何？ {#what-s-next}

TiDB クラスターに正常に接続すると、 [TiDBでSQL文を調べる](/basic-sql-operations.md) 。
