---
title: Connect to TiDB with MySQL Workbench
summary: MySQL Workbenchを使用してTiDBに接続する方法を学びましょう。
aliases: ['/ja/tidb/stable/dev-guide-gui-mysql-workbench/','/ja/tidb/dev/dev-guide-gui-mysql-workbench/','/ja/tidbcloud/dev-guide-gui-mysql-workbench/']
---

# MySQL Workbenchを使用してTiDBに接続する {#connect-to-tidb-with-mysql-workbench}

TiDBはMySQL互換データベースであり、 [MySQL Workchen](https://www.mysql.com/products/workbench/)はMySQLデータベースユーザー向けのGUIツールセットです。

> **警告：**
>
> -   MySQL WorkbenchはMySQLとの互換性があるため、TiDBに接続できますが、MySQL WorkbenchはTiDBを完全にサポートしているわけではありません。TiDBをMySQLとして扱うため、使用中に問題が発生する可能性があります。
> -   [データグリップ](/develop/dev-guide-gui-datagrip.md)、 [DBeaver](/develop/dev-guide-gui-dbeaver.md) 、 [VS Code SQLTools](/develop/dev-guide-gui-vscode-sqltools.md)など、TiDB を正式にサポートする他の GUI ツールを使用することをお勧めします。 TiDB で完全にサポートされている GUI ツールの完全なリストについては、 [TiDBがサポートするサードパーティツール](/develop/dev-guide-third-party-support.md#gui)を参照してください。

このチュートリアルでは、MySQL Workbenchを使用してTiDBに接続する方法を学ぶことができます。

> **注記：**
>
> このチュートリアルは、 TiDB Cloud Starter、 TiDB Cloud Essential、 TiDB Cloud Premium、 TiDB Cloud Dedicated、およびTiDB Self-Managedに対応しています。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、以下が必要です。

-   [MySQL Workchen](https://dev.mysql.com/downloads/workbench/) **8.0.31**以降のバージョン。
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
    -   **「接続」は**`MySQL Workbench`に設定されています。
    -   お使いの環境に合った**オペレーティングシステム**を選択してください。

4.  **「パスワードを生成」を**クリックすると、ランダムなパスワードが生成されます。

    > **ヒント：**
    >
    > 以前にパスワードを作成したことがある場合は、元のパスワードを使用するか、 **「パスワードをリセット」**をクリックして新しいパスワードを生成できます。

5.  MySQL Workbenchを起動し、 **「MySQL Connections」**タイトルの横にある**「+」**をクリックします。

    ![MySQL Workbench: add new connection](/media/develop/mysql-workbench-add-new-connection.png)

6.  **「新しい接続の設定**」ダイアログで、以下の接続パラメータを設定します。

    -   **接続名**：この接続に分かりやすい名前を付けてください。
    -   **ホスト名**： TiDB Cloud接続ダイアログから`HOST`パラメータを入力します。
    -   **ポート**: TiDB Cloud接続ダイアログから`PORT`パラメータを入力します。
    -   **ユーザー名**： TiDB Cloud接続ダイアログから`USERNAME`パラメータを入力してください。
    -   **パスワード**： **[キーチェーンに保存...]**または**[Vaultに保存]**をクリックし、手順4で作成したパスワードを入力して、 **[OK]**をクリックしてパスワードを保存します。

        ![MySQL Workbench: store the password of TiDB Cloud Starter in keychain](/media/develop/mysql-workbench-store-password-in-keychain.png)

    次の図は、接続パラメータの例を示しています。

    ![MySQL Workbench: configure connection settings for TiDB Cloud Starter](/media/develop/mysql-workbench-connection-config-serverless-parameters.png)

7.  **「接続テスト」**をクリックして、対象のTiDB Cloud StarterまたはEssentialインスタンスへの接続を検証してください。

8.  接続テストが成功すると、 **「MySQL接続が正常に確立されました」という**メッセージが表示されます。 **「OK」**をクリックして接続設定を保存してください。

</div>
<div label="TiDB Cloud Premium">

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud Premiumインスタンスの名前をクリックして概要ページに移動します。

2.  左側のナビゲーションペインで、 **[設定]** &gt; **[ネットワーク]**をクリックします。

3.  **ネットワークの**ページで、 **[パブリックエンドポイント****を有効にする]**をクリックし、次に**[IP アドレスの追加]**をクリックします。

    クライアントのIPアドレスがアクセスリストに追加されていることを確認してください。

4.  左側のナビゲーションペインで**「概要」**をクリックすると、インスタンスの概要ページに戻ります。

5.  右上隅の**「接続」**をクリックしてください。接続ダイアログが表示されます。

6.  接続ダイアログで、 **「接続タイプ」**ドロップダウンリストから**「パブリック」**を選択します。

    -   公開エンドポイントがまだ有効化中であることを示すメッセージが表示された場合は、処理が完了するまでお待ちください。
    -   まだパスワードを設定していない場合は、ダイアログの**「ルートパスワードを設定」**をクリックしてください。
    -   サーバー証明書を確認する必要がある場合、または接続に失敗して認証局（CA）証明書が必要な場合は、 **「CA証明書」**をクリックしてダウンロードしてください。
    -   **パブリック**接続タイプに加えて、 TiDB Cloud Premium は**プライベート エンドポイント**接続をサポートします。詳細については、 [AWS PrivateLink経由でTiDB Cloud Premiumに接続します。](/tidb-cloud/premium/connect-to-premium-via-aws-private-endpoint.md)を参照してください。

7.  MySQL Workbenchを起動し、 **「MySQL接続」**タイトルの横にある**「+」**をクリックします。

8.  **「新しい接続の設定**」ダイアログで、以下の接続パラメータを設定します。

    -   **接続名**：この接続に分かりやすい名前を付けてください。
    -   **ホスト名**： TiDB Cloud接続ダイアログから`HOST`パラメータを入力します。
    -   **ポート**: TiDB Cloud接続ダイアログから`PORT`パラメータを入力します。
    -   **ユーザー名**： TiDB Cloud接続ダイアログから`USERNAME`パラメータを入力してください。
    -   **パスワード**： **[キーチェーンに保存...]**または**[Vaultに保存]**をクリックし、 TiDB Cloud Premiumインスタンスのパスワードを入力して、 **[OK]**をクリックするとパスワードが保存されます。

9.  **「接続テスト」**をクリックして、 TiDB Cloud Premiumインスタンスへの接続を検証してください。

10. 接続テストが成功すると、 **「MySQL接続が正常に確立されました」という**メッセージが表示されます。 **「OK」**をクリックして接続設定を保存してください。

</div>
<div label="TiDB Cloud Dedicated">

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud Dedicatedクラスタの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックしてください。接続ダイアログが表示されます。

3.  接続ダイアログで、「**接続タイプ」**ドロップダウンリストから**「パブリック」**を選択し、 **「CA証明書」**をクリックしてCA証明書をダウンロードします。

    IP アクセス リストを設定していない場合は、最初の接続の前に、 **[IP アクセス リストの設定] をクリックするか、「IP アクセス リストを設定する」**の手順に従って[IPアクセスリストを設定する](https://docs.pingcap.com/tidbcloud/configure-ip-access-list)。

    TiDB Cloud Dedicated は、**パブリック**接続タイプに加えて、**プライベート エンドポイント**および**VPC ピアリング**接続タイプもサポートしています。詳細については、 [TiDB Cloud Dedicatedクラスタに接続します](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)参照してください。

4.  MySQL Workbenchを起動し、 **「MySQL Connections」**タイトルの横にある**「+」**をクリックします。

    ![MySQL Workbench: add new connection](/media/develop/mysql-workbench-add-new-connection.png)

5.  **「新しい接続の設定**」ダイアログで、以下の接続パラメータを設定します。

    -   **接続名**：この接続に分かりやすい名前を付けてください。
    -   **ホスト名**： TiDB Cloud接続ダイアログから`HOST`パラメータを入力します。
    -   **ポート**: TiDB Cloud接続ダイアログから`PORT`パラメータを入力します。
    -   **ユーザー名**： TiDB Cloud接続ダイアログから`USERNAME`パラメータを入力してください。
    -   **パスワード**： **[キーチェーンに保存...]**をクリックし、 TiDB Cloud Dedicatedクラスタのパスワードを入力して、 **[OK]**をクリックするとパスワードが保存されます。

        ![MySQL Workbench: store the password of TiDB Cloud Dedicated in keychain](/media/develop/mysql-workbench-store-dedicated-password-in-keychain.png)

    次の図は、接続パラメータの例を示しています。

    ![MySQL Workbench: configure connection settings for TiDB Cloud Dedicated](/media/develop/mysql-workbench-connection-config-dedicated-parameters.png)

6.  **「接続テスト」**をクリックして、 TiDB Cloud Dedicatedクラスターへの接続を検証してください。

7.  接続テストが成功すると、 **「MySQL接続が正常に確立されました」という**メッセージが表示されます。 **「OK」**をクリックして接続設定を保存してください。

</div>
<div label="TiDB Self-Managed" value="tidb">

1.  MySQL Workbenchを起動し、 **「MySQL Connections」**タイトルの横にある**「+」**をクリックします。

    ![MySQL Workbench: add new connection](/media/develop/mysql-workbench-add-new-connection.png)

2.  **「新しい接続の設定**」ダイアログで、以下の接続パラメータを設定します。

    -   **接続名**：この接続に分かりやすい名前を付けてください。
    -   **ホスト名**：TiDBセルフマネージドクラスタのIPアドレスまたはドメイン名を入力してください。
    -   **ポート**：TiDBセルフマネージドクラスタのポート番号を入力してください。
    -   **ユーザー名**：TiDBに接続するために使用するユーザー名を入力してください。
    -   **パスワード**： **[キーチェーンに保存...]**をクリックし、TiDBセルフマネージドクラスタへの接続に使用するパスワードを入力して、 **[OK]**をクリックしてパスワードを保存します。

        ![MySQL Workbench: store the password of TiDB Self-Managed in keychain](/media/develop/mysql-workbench-store-self-hosted-password-in-keychain.png)

    次の図は、接続パラメータの例を示しています。

    ![MySQL Workbench: configure connection settings for TiDB Self-Managed](/media/develop/mysql-workbench-connection-config-self-hosted-parameters.png)

3.  **「接続テスト」**をクリックして、TiDBセルフマネージドクラスタへの接続を検証してください。

4.  接続テストが成功すると、 **「MySQL接続が正常に確立されました」という**メッセージが表示されます。 **「OK」**をクリックして接続設定を保存してください。

</div>
</SimpleTab>

## よくある質問 {#faqs}

### 接続タイムアウトエラー「エラーコード：2013。クエリ実行中にMySQLサーバーへの接続が失われました」への対処方法を教えてください。 {#how-to-handle-the-connection-timeout-error-error-code-2013-lost-connection-to-mysql-server-during-query}

このエラーは、クエリの実行時間がタイムアウト制限を超えたことを示しています。この問題を解決するには、以下の手順でタイムアウト設定を調整してください。

1.  MySQL Workbenchを起動し、 **Workbenchの設定**ページに移動します。
2.  **SQLエディタの****「MySQLセッション」**セクションで、 **「DBMS接続読み取りタイムアウト間隔（秒）」**オプションを設定します。これは、MySQL Workbenchがサーバーから切断されるまでにクエリが実行できる最大時間（秒単位）を設定します。

    ![MySQL Workbench: adjust timeout option in SQL Editor settings](/media/develop/mysql-workbench-adjust-sqleditor-read-timeout.jpg)

詳細については、 [MySQL Workbenchに関するよくある質問](https://dev.mysql.com/doc/workbench/en/workbench-faq.html)を参照してください。

## 次のステップ {#next-steps}

-   MySQL Workbench の使用法の詳細については[MySQL Workbenchのドキュメント](https://dev.mysql.com/doc/workbench/en/)参照してください。
-   [開発者ガイド](https://docs.pingcap.com/developer/)[データを挿入する](/develop/dev-guide-insert-data.md)[データの更新](/develop/dev-guide-update-data.md)、[データを削除する](/develop/dev-guide-delete-data.md)、「SQL パフォーマンス最適化」などの章[単一表の読み取り](/develop/dev-guide-get-data-from-single-table.md)読んで、TiDB アプリケーション [取引](/develop/dev-guide-transaction-overview.md)[SQLパフォーマンス最適化](/develop/dev-guide-optimize-sql-overview.md)。
-   プロフェッショナルな[TiDB開発者向けコース](https://www.pingcap.com/education/)コースを通じて学習し、試験に合格すると[TiDB認定資格](https://www.pingcap.com/education/certification/)を取得します。

## お困りですか？ {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)or [スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに質問してください。
-   [TiDB Cloudのサポートチケットを送信してください](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDB Self-Managedのサポートチケットを送信してください](/support.md)
