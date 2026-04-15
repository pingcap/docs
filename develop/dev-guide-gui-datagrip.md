---
title: Connect to TiDB with JetBrains DataGrip
summary: JetBrains DataGripを使用してTiDBに接続する方法を学びましょう。このチュートリアルは、IntelliJ、PhpStorm、PyCharmなどの他のJetBrains IDEで利用可能なデータベースツールおよびSQLプラグインにも適用できます。
aliases: ['/ja/tidb/stable/dev-guide-gui-datagrip/','/ja/tidb/dev/dev-guide-gui-datagrip/','/ja/tidbcloud/dev-guide-gui-datagrip/']
---

# JetBrains DataGripを使用してTiDBに接続する {#connect-to-tidb-with-jetbrains-datagrip}

TiDBはMySQL互換のデータベースであり、 [JetBrains DataGrip](https://www.jetbrains.com/help/datagrip/getting-started.html)データベースとSQLのための強力な統合開発環境（IDE）です。このチュートリアルでは、DataGripを使用してTiDBクラスタに接続する手順を説明します。

> **注記：**
>
> このチュートリアルは、 TiDB Cloud Starter、 TiDB Cloud Essential、 TiDB Cloud Dedicated、およびTiDB Self-Managedに対応しています。

DataGripは2つの方法で使用できます。

-   [DataGrip IDE](https://www.jetbrains.com/datagrip/download)スタンドアロンツールとして。
-   IntelliJ、PhpStorm、PyCharm などの JetBrains IDE のデータベース[データベースツールとSQLプラグイン](https://www.jetbrains.com/help/idea/relational-databases.html)として。

このチュートリアルは主にスタンドアロン版のDataGrip IDEに焦点を当てています。JetBrains IDEのJetBrains Database ToolsおよびSQLプラグインを使用してTiDBに接続する手順も同様です。また、どのJetBrains IDEからTiDBに接続する場合でも、このドキュメントの手順を参考にすることができます。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、以下が必要です。

-   [DataGrip **2023.2.1**以降](https://www.jetbrains.com/datagrip/download/)、または非コミュニティ エディションの[ジェットブレインズ](https://www.jetbrains.com/)IDE。
-   TiDBクラスタ。

**TiDBクラスタをお持ちでない場合は、以下の手順で作成できます。**

-   (推奨) [TiDB Cloud Starterインスタンスを作成する](/develop/dev-guide-build-cluster-in-cloud.md)。
-   [ローカルテスト用のTiDBセルフマネージドクラスタをデプロイ。](/quick-start-with-tidb.md#deploy-a-local-test-cluster)または[本番本番のTiDBセルフマネージドクラスタをデプロイ。](/production-deployment-using-tiup.md)

## TiDBに接続する {#connect-to-tidb}

選択したTiDBのデプロイオプションに応じて、TiDBに接続してください。

<SimpleTab>
<div label="TiDB Cloud Starter or Essential">

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud StarterまたはEssentialインスタンスの名前をクリックして、概要ページに移動します。

2.  右上隅の**「接続」**をクリックしてください。接続ダイアログが表示されます。

3.  接続ダイアログの設定がご使用のオペレーティング環境と一致していることを確認してください。

    -   **接続タイプ**は`Public`に設定されています。
    -   **ブランチ**は`main`に設定されています。
    -   **Connect With は**`DataGrip`に設定されています。
    -   お使いの環境に合った**オペレーティングシステム**を選択してください。

4.  **「パスワードを生成」を**クリックすると、ランダムなパスワードが生成されます。

    > **ヒント：**
    >
    > 以前にパスワードを作成したことがある場合は、元のパスワードを使用するか、 **「パスワードをリセット」**をクリックして新しいパスワードを生成できます。

5.  DataGripを起動し、接続を管理するためのプロジェクトを作成します。

    ![Create a project in DataGrip](/media/develop/datagrip-create-project.jpg)

6.  新しく作成したプロジェクトで、**データベースエクスプローラー**パネルの左上隅にある**「+」**をクリックし、 **「データソース」** &gt; **「その他」** &gt; **「TiDB」**を選択します。

    ![Select a data source in DataGrip](/media/develop/datagrip-data-source-select.jpg)

7.  TiDB Cloud接続ダイアログから接続文字列をコピーします。次に、それを**URL**フィールドに貼り付けると、残りのパラメータは自動的に入力されます。結果の例は次のとおりです。

    ![Configure the URL field for TiDB Cloud Starter](/media/develop/datagrip-url-paste.jpg)

    **「不足しているドライバファイルをダウンロードしてください」**という警告が表示された場合は、 **「ダウンロード」**をクリックしてドライバファイルを入手してください。

8.  **「接続テスト」**をクリックして、対象のTiDB Cloud StarterまたはEssentialインスタンスへの接続を検証してください。

    ![Test the connection to a TiDB Cloud Starter instance](/media/develop/datagrip-test-connection.jpg)

9.  接続設定を保存するには、 **「OK」**をクリックしてください。

</div>
<div label="TiDB Cloud Dedicated">

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud Dedicatedクラスタの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックしてください。接続ダイアログが表示されます。

3.  接続ダイアログで、「**接続タイプ」**ドロップダウンリストから**「パブリック」**を選択し、 **「CA証明書」**をクリックしてCA証明書をダウンロードします。

    IP アクセス リストを設定していない場合は、最初の接続の前に、 **[IP アクセス リストの設定] をクリックするか、「IP アクセス リストを設定する」**の手順に従って[IPアクセスリストを設定する](https://docs.pingcap.com/tidbcloud/configure-ip-access-list)。

    TiDB Cloud Dedicated は、**パブリック**接続タイプに加えて、**プライベート エンドポイント**および**VPC ピアリング**接続タイプもサポートしています。詳細については、 [TiDB Cloud Dedicatedクラスタに接続します](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)参照してください。

4.  DataGripを起動し、接続を管理するためのプロジェクトを作成します。

    ![Create a project in DataGrip](/media/develop/datagrip-create-project.jpg)

5.  新しく作成したプロジェクトで、**データベースエクスプローラー**パネルの左上隅にある**「+」**をクリックし、 **「データソース」** &gt; **「その他」** &gt; **「TiDB」**を選択します。

    ![Select a data source in DataGrip](/media/develop/datagrip-data-source-select.jpg)

6.  適切な接続文字列をコピーして、DataGrip の [**データ ソースとドライバ]**ウィンドウに貼り付けてください。DataGrip フィールドとTiDB Cloud Dedicated接続文字列のマッピングは以下のとおりです。

    | データグリップフィールド | TiDB Cloud Dedicated接続文字列 |
    | ------------ | ------------------------- |
    | ホスト          | `{host}`                  |
    | ポート          | `{port}`                  |
    | ユーザー         | `{user}`                  |
    | パスワード        | `{password}`              |

    例えば、以下のような例があります。

    ![Configure the connection parameters for TiDB Cloud Dedicated](/media/develop/datagrip-dedicated-connect.jpg)

7.  **SSH/SSL**タブをクリックし、 **「SSLを使用する」**チェックボックスを選択して、CA証明書のパスを**CAファイル**フィールドに入力します。

    ![Configure the CA for TiDB Cloud Dedicated](/media/develop/datagrip-dedicated-ssl.jpg)

    **「不足しているドライバファイルをダウンロードしてください」**という警告が表示された場合は、 **「ダウンロード」**をクリックしてドライバファイルを入手してください。

8.  **[詳細設定]**タブをクリックし、スクロールして**enabledTLSProtocols**パラメーターを見つけ、その値を`TLSv1.2,TLSv1.3`に設定します。

    ![Configure the TLS for TiDB Cloud Dedicated](/media/develop/datagrip-dedicated-advanced.jpg)

9.  **「接続テスト」**をクリックして、 TiDB Cloud Dedicatedクラスターへの接続を検証してください。

    ![Test the connection to a TiDB Cloud Dedicated cluster](/media/develop/datagrip-dedicated-test-connection.jpg)

10. 接続設定を保存するには、 **「OK」**をクリックしてください。

</div>
<div label="TiDB Self-Managed" value="tidb">

1.  DataGripを起動し、接続を管理するためのプロジェクトを作成します。

    ![Create a project in DataGrip](/media/develop/datagrip-create-project.jpg)

2.  新しく作成したプロジェクトで、**データベースエクスプローラー**パネルの左上隅にある**「+」**をクリックし、 **「データソース」** &gt; **「その他」** &gt; **「TiDB」**を選択します。

    ![Select a data source in DataGrip](/media/develop/datagrip-data-source-select.jpg)

3.  以下の接続パラメータを設定してください。

    -   **ホスト**：TiDBセルフマネージドクラスタのIPアドレスまたはドメイン名。
    -   **ポート**：TiDBセルフマネージドクラスタのポート番号。
    -   **ユーザー**：TiDBセルフマネージドクラスタに接続するために使用するユーザー名。
    -   **パスワード**：ユーザー名のパスワード。

    例えば、以下のような例があります。

    ![Configure the connection parameters for TiDB Self-Managed](/media/develop/datagrip-self-hosted-connect.jpg)

    **「不足しているドライバファイルをダウンロードしてください」**という警告が表示された場合は、 **「ダウンロード」**をクリックしてドライバファイルを入手してください。

4.  **「接続テスト」**をクリックして、TiDBセルフマネージドクラスタへの接続を検証してください。

    ![Test the connection to a TiDB Self-Managed cluster](/media/develop/datagrip-self-hosted-test-connection.jpg)

5.  接続設定を保存するには、 **「OK」**をクリックしてください。

</div>
</SimpleTab>

## 次のステップ {#next-steps}

-   DataGrip の使用法の詳細については[DataGripのドキュメント](https://www.jetbrains.com/help/datagrip/getting-started.html)ご覧ください。
-   [開発者ガイド](https://docs.pingcap.com/developer/)[データを挿入する](/develop/dev-guide-insert-data.md)[データの更新](/develop/dev-guide-update-data.md)、[データを削除する](/develop/dev-guide-delete-data.md)、「SQL パフォーマンス最適化」などの章[単一表の読み取り](/develop/dev-guide-get-data-from-single-table.md)読んで、TiDB アプリケーション [取引](/develop/dev-guide-transaction-overview.md)[SQLパフォーマンス最適化](/develop/dev-guide-optimize-sql-overview.md)。
-   プロフェッショナルな[TiDB開発者向けコース](https://www.pingcap.com/education/)コースを通じて学習し、試験に合格すると[TiDB認定資格](https://www.pingcap.com/education/certification/)を取得します。

## お困りですか？ {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)or [スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに質問してください。
-   [TiDB Cloudのサポートチケットを送信してください](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDB Self-Managedのサポートチケットを送信してください](/support.md)
