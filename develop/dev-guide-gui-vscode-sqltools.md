---
title: Connect to TiDB with Visual Studio Code
summary: Visual Studio CodeまたはGitHub Codespacesを使用してTiDBに接続する方法を学びましょう。
aliases: ['/ja/tidb/stable/dev-guide-gui-vscode-sqltools/','/ja/tidb/dev/dev-guide-gui-vscode-sqltools/','/ja/tidbcloud/dev-guide-gui-vscode-sqltools/']
---

# Visual Studio Codeを使用してTiDBに接続する {#connect-to-tidb-with-visual-studio-code}

TiDB は MySQL 互換データベースであり、 [Visual Studio Code (VS Code)](https://code.visualstudio.com/)は軽量かつ強力なソース コード エディターです。このチュートリアルでは、TiDB を[公式ドライバー](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools-driver-mysql)としてサポートする[SQLツール](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools)拡張機能を使用します。

このチュートリアルでは、Visual Studio Code を使用して TiDB に接続する方法を学ぶことができます。

> **注記：**
>
> -   このチュートリアルは、 TiDB Cloud Starter、 TiDB Cloud Essential、 TiDB Cloud Dedicated、およびTiDB Self-Managedに対応しています。
> -   このチュートリアルは、 [GitHub Codespaces](https://github.com/features/codespaces) 、Visual Studio [Visual Studio Code 開発コンテナ](https://code.visualstudio.com/docs/devcontainers/containers)[Visual Studio Code WSL](https://code.visualstudio.com/docs/remote/wsl) Code リモート開発環境でも動作します。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、以下が必要です。

-   [Visual Studio Code](https://code.visualstudio.com/#alt-downloads) **1.72.0**以降のバージョン。
-   [SQLTools MySQL/MariaDB/TiDB](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools-driver-mysql)拡張機能です。インストールするには、以下のいずれかの方法を使用できます。
    -   <a href="vscode:extension/mtxr.sqltools-driver-mysql">このリンク</a>をクリックするとVS Codeが起動し、拡張機能を直接インストールできます。
    -   [VS Code マーケットプレイス](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools-driver-mysql)に移動し、 **[インストール]**をクリックします。
    -   VS Code の**[拡張機能]**タブで`mtxr.sqltools-driver-mysql`を検索して**SQLTools MySQL/MariaDB/TiDB**拡張機能を取得し、 **[インストール] を**クリックします。
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

    -   **「接続」は**`VS Code`に設定されています。

    -   お使いの環境に合った**オペレーティングシステム**を選択してください。

    > **ヒント：**
    >
    > VS Code をリモート開発環境で実行している場合は、リストからリモートのオペレーティングシステムを選択してください。たとえば、Windows Subsystem for Linux (WSL) を使用している場合は、対応する Linux ディストリビューションに切り替えてください。GitHub Codespaces を使用している場合は、この操作は不要です。

4.  **「パスワードを生成」を**クリックすると、ランダムなパスワードが生成されます。

    > **ヒント：**
    >
    > 以前にパスワードを作成したことがある場合は、元のパスワードを使用するか、 **「パスワードをリセット」**をクリックして新しいパスワードを生成できます。

5.  VS Codeを起動し、ナビゲーションペインで**SQLTools**拡張機能を選択します。 **[接続]**セクションで**[新しい接続を追加]**をクリックし、データベースドライバとして**TiDB**を選択します。

    ![VS Code SQLTools: add new connection](/media/develop/vsc-sqltools-add-new-connection.jpg)

6.  設定画面で、以下の接続パラメータを設定します。

    -   **接続名**：この接続に分かりやすい名前を付けてください。
    -   **接続グループ**：（オプション）この接続グループに分かりやすい名前を付けます。同じグループ名を持つ接続はグループ化されます。
    -   **接続方法**：**サーバーとポート**を選択してください。
    -   **サーバーアドレス**： TiDB Cloud接続ダイアログから`HOST`パラメータを入力します。
    -   **ポート**: TiDB Cloud接続ダイアログから`PORT`パラメータを入力します。
    -   **データベース**：接続したいデータベースを入力してください。
    -   **ユーザー名**： TiDB Cloud接続ダイアログから`USERNAME`パラメータを入力してください。
    -   **パスワードモード**: **SQLToolsDriver認証情報**を選択します。
    -   **MySQLドライバ固有のオプション**領域で、以下のパラメータを設定します。

        -   **認証プロトコル**：**デフォルト**を選択してください。
        -   **SSL** ： **[有効]**を選択します。TiDB Cloud Starterは安全な接続を必要とします。SSL**オプション（node.TLSSocket）**領域で、 TiDB Cloud接続ダイアログの`CA`パラメーターを**[認証局（CA）証明書**ファイル]フィールドに設定してください。

            > **注記：**
            >
            > Windows または GitHub コードスペースで実行している場合は、 **SSL を**空白のままにすることができます。デフォルトでは、SQLTools は Let&#39;s Encrypt によって厳選された有名な CA を信頼します。詳細については、 [TiDB Cloud Starterルート証明書管理](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-clusters#root-certificate-management)参照してください。

    ![VS Code SQLTools: configure connection settings for TiDB Cloud Starter](/media/develop/vsc-sqltools-connection-config-serverless.jpg)

7.  **「接続テスト」**をクリックして、対象のTiDB Cloud StarterまたはEssentialインスタンスへの接続を検証してください。

    1.  ポップアップウィンドウで**「許可」**をクリックします。
    2.  **SQLToolsDriver認証情報**ダイアログで、手順4で作成したパスワードを入力します。

        ![VS Code SQLTools: enter password to connect to TiDB Cloud Starter](/media/develop/vsc-sqltools-password.jpg)

8.  接続テストが成功すると、「**接続に成功しました！」という**メッセージが表示されます。 **「接続を保存」**をクリックして、接続設定を保存してください。

</div>
<div label="TiDB Cloud Dedicated">

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud Dedicatedクラスタの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックしてください。接続ダイアログが表示されます。

3.  接続ダイアログで、「**接続タイプ」**ドロップダウンリストから**「パブリック」**を選択し、 **「CA証明書」**をクリックしてCA証明書をダウンロードします。

    IP アクセス リストを設定していない場合は、最初の接続の前に、 **[IP アクセス リストの設定] をクリックするか、「IP アクセス リストを設定する」**の手順に従って[IPアクセスリストを設定する](https://docs.pingcap.com/tidbcloud/configure-ip-access-list)。

    TiDB Cloud Dedicated は、**パブリック**接続タイプに加えて、**プライベート エンドポイント**および**VPC ピアリング**接続タイプもサポートしています。詳細については、 [TiDB Cloud Dedicatedクラスタに接続します](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)参照してください。

4.  VS Codeを起動し、ナビゲーションペインで**SQLTools**拡張機能を選択します。 **[接続]**セクションで**[新しい接続を追加]**をクリックし、データベースドライバとして**TiDB**を選択します。

    ![VS Code SQLTools: add new connection](/media/develop/vsc-sqltools-add-new-connection.jpg)

5.  設定画面で、以下の接続パラメータを設定します。

    -   **接続名**：この接続に分かりやすい名前を付けてください。
    -   **接続グループ**：（オプション）この接続グループに分かりやすい名前を付けます。同じグループ名を持つ接続はグループ化されます。
    -   **接続方法**：**サーバーとポート**を選択してください。
    -   **サーバーアドレス**： TiDB Cloud接続ダイアログから`host`パラメータを入力します。
    -   **ポート**: TiDB Cloud接続ダイアログから`port`パラメータを入力します。
    -   **データベース**：接続したいデータベースを入力してください。
    -   **ユーザー名**： TiDB Cloud接続ダイアログから`user`パラメータを入力してください。
    -   **パスワードモード**: **SQLToolsDriver認証情報**を選択します。
    -   **MySQLドライバ固有のオプション**領域で、以下のパラメータを設定します。

        -   **認証プロトコル**：**デフォルト**を選択してください。
        -   **SSL** ：**無効を**選択してください。

    ![VS Code SQLTools: configure connection settings for TiDB Cloud Dedicated](/media/develop/vsc-sqltools-connection-config-dedicated.jpg)

6.  **「接続テスト」**をクリックして、 TiDB Cloud Dedicatedクラスターへの接続を検証してください。

    1.  ポップアップウィンドウで**「許可」**をクリックします。
    2.  **SQLToolsDriver認証情報**ダイアログで、 TiDB Cloud Dedicatedクラスタのパスワードを入力します。

    ![VS Code SQLTools: enter password to connect to TiDB Cloud Dedicated](/media/develop/vsc-sqltools-password.jpg)

7.  接続テストが成功すると、「**接続に成功しました！」という**メッセージが表示されます。 **「接続を保存」**をクリックして、接続設定を保存してください。

</div>
<div label="TiDB Self-Managed" value="tidb">

1.  VS Codeを起動し、ナビゲーションペインで**SQLTools**拡張機能を選択します。 **[接続]**セクションで**[新しい接続を追加]**をクリックし、データベースドライバとして**TiDB**を選択します。

    ![VS Code SQLTools: add new connection](/media/develop/vsc-sqltools-add-new-connection.jpg)

2.  設定画面で、以下の接続パラメータを設定します。

    -   **接続名**：この接続に分かりやすい名前を付けてください。

    -   **接続グループ**：（オプション）この接続グループに分かりやすい名前を付けます。同じグループ名を持つ接続はグループ化されます。

    -   **接続方法**：**サーバーとポート**を選択してください。

    -   **サーバーアドレス**：TiDBセルフマネージドクラスタのIPアドレスまたはドメイン名を入力してください。

    -   **ポート**：TiDBセルフマネージドクラスタのポート番号を入力してください。

    -   **データベース**：接続したいデータベースを入力してください。

    -   **ユーザー名**：TiDBセルフマネージドクラスタに接続するために使用するユーザー名を入力してください。

    -   **パスワードモード**：

        -   パスワードが空欄の場合は、 **「空欄のパスワードを使用する」**を選択してください。
        -   それ以外の場合は、 **「SQLToolsDriver資格情報」**を選択してください。

    -   **MySQLドライバ固有のオプション**領域で、以下のパラメータを設定します。

        -   **認証プロトコル**：**デフォルト**を選択してください。
        -   **SSL** ：**無効を**選択してください。

    ![VS Code SQLTools: configure connection settings for TiDB Self-Managed](/media/develop/vsc-sqltools-connection-config-self-hosted.jpg)

3.  **「接続テスト」**をクリックして、TiDBセルフマネージドクラスタへの接続を検証してください。

    パスワードが空欄でない場合は、ポップアップウィンドウで**「許可」**をクリックし、TiDBセルフマネージドクラスタのパスワードを入力してください。

    ![VS Code SQLTools: enter password to connect to TiDB Self-Managed](/media/develop/vsc-sqltools-password.jpg)

4.  接続テストが成功すると、「**接続に成功しました！」という**メッセージが表示されます。 **「接続を保存」**をクリックして、接続設定を保存してください。

</div>
</SimpleTab>

## 次のステップ {#next-steps}

-   Visual Studio Code の使用法の詳細については[Visual Studio Code のドキュメント](https://code.visualstudio.com/docs)参照してください。
-   VS Code SQLTools 拡張機能の使用法について詳しくは、SQLTools の[ドキュメント](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools)および[GitHubリポジトリ](https://github.com/mtxr/vscode-sqltools)ご覧ください。
-   [開発者ガイド](https://docs.pingcap.com/developer/)[データを挿入する](/develop/dev-guide-insert-data.md)」、[データの更新](/develop/dev-guide-update-data.md)[データを削除する](/develop/dev-guide-delete-data.md)、「SQL パフォーマンス最適化」など[単一テーブルの読み取り](/develop/dev-guide-get-data-from-single-table.md)章を読んで、TiDB アプリケーション開発のベスト [取引](/develop/dev-guide-transaction-overview.md)[SQLパフォーマンス最適化](/develop/dev-guide-optimize-sql-overview.md)。
-   プロフェッショナルな[TiDB開発者向けコース](https://www.pingcap.com/education/)コースを通じて学習し、試験に合格すると[TiDB認定資格](https://www.pingcap.com/education/certification/)を取得します。

## お困りですか？ {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)or [スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに質問してください。
-   [TiDB Cloudのサポートチケットを送信してください](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDB Self-Managedのサポートチケットを送信してください](/support.md)
