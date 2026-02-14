---
title: Connect to TiDB with Visual Studio Code
summary: Visual Studio Code または GitHub Codespaces を使用して TiDB に接続する方法を学習します。
aliases: ['/ja/tidb/stable/dev-guide-gui-vscode-sqltools/','/ja/tidbcloud/dev-guide-gui-vscode-sqltools/']
---

# Visual Studio Code で TiDB に接続する {#connect-to-tidb-with-visual-studio-code}

TiDBはMySQL互換のデータベースであり、 [ビジュアルスタジオコード（VSコード）](https://code.visualstudio.com/)軽量ながらも強力なソースコードエディタです。このチュートリアルでは、TiDBを[公式ドライバー](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools-driver-mysql)としてサポートする[SQLツール](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools)拡張機能を使用します。

このチュートリアルでは、Visual Studio Code を使用して TiDB クラスターに接続する方法を学習します。

> **注記：**
>
> -   このチュートリアルは、 TiDB Cloud Starter、 TiDB Cloud Essential、 TiDB Cloud Dedicated、および TiDB Self-Managed と互換性があります。
> -   このチュートリアルは、 [GitHub コードスペース](https://github.com/features/codespaces) 、 [Visual Studio Code 開発コンテナ](https://code.visualstudio.com/docs/devcontainers/containers) 、 [ビジュアルスタジオコード WSL](https://code.visualstudio.com/docs/remote/wsl)などの Visual Studio Code リモート開発環境でも機能します。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、次のものが必要です。

-   [ビジュアルスタジオコード](https://code.visualstudio.com/#alt-downloads) **1.72.0**以降のバージョン。
-   Visual Studio Code の[SQLツール MySQL/MariaDB/TiDB](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools-driver-mysql)拡張機能。インストールするには、以下のいずれかの方法があります。
    -   <a href="vscode:extension/mtxr.sqltools-driver-mysql">このリンク</a>をクリックして VS Code を起動し、拡張機能を直接インストールします。
    -   [VS Code マーケットプレイス](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools-driver-mysql)に移動して、 **「インストール」**をクリックします。
    -   VS Code の**拡張機能**タブで、 `mtxr.sqltools-driver-mysql`検索して**SQLTools MySQL/MariaDB/TiDB**拡張機能を取得し、 **「インストール」を**クリックします。
-   TiDB クラスター。

**TiDB クラスターがない場合は、次のように作成できます。**

-   (推奨) [TiDB Cloud Starter クラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って、独自のTiDB Cloudクラスターを作成します。
-   [ローカルテストTiDBクラスタをデプロイ](/quick-start-with-tidb.md#deploy-a-local-test-cluster)または[本番のTiDBクラスタをデプロイ](/production-deployment-using-tiup.md)に従ってローカル クラスターを作成します。

## TiDBに接続する {#connect-to-tidb}

選択した TiDB デプロイメント オプションに応じて、TiDB クラスターに接続します。

<SimpleTab>
<div label="TiDB Cloud Starter or Essential">

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログの構成が動作環境と一致していることを確認します。

    -   **接続タイプ**は`Public`に設定されています。

    -   **ブランチ**は`main`に設定されています。

    -   **Connect With が**`VS Code`に設定されています。

    -   **オペレーティング システムは**環境に適合します。

    > **ヒント：**
    >
    > VS Code をリモート開発環境で実行している場合は、リストからリモートオペレーティングシステムを選択してください。例えば、Windows Subsystem for Linux (WSL) を使用している場合は、対応する Linux ディストリビューションに切り替えてください。GitHub Codespaces を使用している場合は、この操作は不要です。

4.  ランダムなパスワードを作成するには、 **「パスワードの生成」を**クリックします。

    > **ヒント：**
    >
    > 以前にパスワードを作成したことがある場合は、元のパスワードを使用するか、 **「パスワードのリセット」を**クリックして新しいパスワードを生成することができます。

5.  VS Codeを起動し、ナビゲーションペインで**SQLTools**拡張機能を選択します。 **「接続」**セクションで**「新しい接続の追加」を**クリックし、データベースドライバーとして**TiDBを**選択します。

    ![VS Code SQLTools: add new connection](/media/develop/vsc-sqltools-add-new-connection.jpg)

6.  設定ペインで、次の接続パラメータを構成します。

    -   **接続名**: この接続に意味のある名前を付けます。
    -   **接続グループ**: (オプション) この接続グループに分かりやすい名前を付けます。同じグループ名の接続はグループ化されます。
    -   **接続方法**:**サーバーおよびポート**を選択します。
    -   **サーバー アドレス**: TiDB Cloud接続ダイアログから`HOST`パラメータを入力します。
    -   **ポート**: TiDB Cloud接続ダイアログから`PORT`パラメータを入力します。
    -   **データベース**: 接続するデータベースを入力します。
    -   **ユーザー名**: TiDB Cloud接続ダイアログから`USERNAME`パラメータを入力します。
    -   **パスワード モード**: **SQLToolsDriver資格情報**を選択します。
    -   **MySQL ドライバー固有のオプション**領域で、次のパラメータを設定します。

        -   **認証プロトコル**:**デフォルト**を選択します。
        -   **SSL** ：**有効を**選択します。TiDB TiDB Cloud Starterは安全な接続を必要とします。 **「SSLオプション（node.TLSSocket）」**領域で、 **「証明機関（CA）証明書ファイル」**フィールドをTiDB Cloud接続ダイアログの`CA`番目のパラメータとして設定します。

            > **注記：**
            >
            > WindowsまたはGitHub Codespacesで実行している場合は、 **SSLを**空白のままにすることができます。SQLToolsはデフォルトでLet&#39;s Encryptが管理する既知のCAを信頼します。詳細については、 [TiDB Cloud Starter ルート証明書管理](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-clusters#root-certificate-management)ご覧ください。

    ![VS Code SQLTools: configure connection settings for TiDB Cloud Starter](/media/develop/vsc-sqltools-connection-config-serverless.jpg)

7.  **[テスト接続]**をクリックして、 TiDB Cloud Starter クラスターへの接続を検証します。

    1.  ポップアップウィンドウで、 **[許可]**をクリックします。
    2.  **SQLToolsDriver資格情報**ダイアログで、手順 4 で作成したパスワードを入力します。

        ![VS Code SQLTools: enter password to connect to TiDB Cloud Starter](/media/develop/vsc-sqltools-password.jpg)

8.  接続テストが成功すると、「**正常に接続されました！」**というメッセージが表示されます。 **「接続を保存」**をクリックして接続設定を保存します。

</div>
<div label="TiDB Cloud Dedicated">

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログで、 **[接続タイプ]**ドロップダウン リストから**[パブリック]**を選択し、 **[CA 証明書]**をクリックして CA 証明書をダウンロードします。

    IP アクセス リストをまだ設定していない場合は、 **「IP アクセス リストの設定」を**クリックするか、手順[IPアクセスリストを設定する](https://docs.pingcap.com/tidbcloud/configure-ip-access-list)に従って、最初の接続の前に設定してください。

    TiDB Cloud Dedicatedは、**パブリック**接続タイプに加えて、**プライベートエンドポイント**と**VPCピアリング**接続タイプもサポートしています。詳細については、 [TiDB Cloud専用クラスタに接続する](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)ご覧ください。

4.  VS Codeを起動し、ナビゲーションペインで**SQLTools**拡張機能を選択します。 **「接続」**セクションで**「新しい接続の追加」を**クリックし、データベースドライバーとして**TiDBを**選択します。

    ![VS Code SQLTools: add new connection](/media/develop/vsc-sqltools-add-new-connection.jpg)

5.  設定ペインで、次の接続パラメータを構成します。

    -   **接続名**: この接続に意味のある名前を付けます。
    -   **接続グループ**: (オプション) この接続グループに分かりやすい名前を付けます。同じグループ名の接続はグループ化されます。
    -   **接続方法**:**サーバーおよびポート**を選択します。
    -   **サーバー アドレス**: TiDB Cloud接続ダイアログから`host`パラメータを入力します。
    -   **ポート**: TiDB Cloud接続ダイアログから`port`パラメータを入力します。
    -   **データベース**: 接続するデータベースを入力します。
    -   **ユーザー名**: TiDB Cloud接続ダイアログから`user`パラメータを入力します。
    -   **パスワード モード**: **SQLToolsDriver資格情報**を選択します。
    -   **MySQL ドライバー固有のオプション**領域で、次のパラメータを設定します。

        -   **認証プロトコル**:**デフォルト**を選択します。
        -   **SSL** : **「無効」**を選択します。

    ![VS Code SQLTools: configure connection settings for TiDB Cloud Dedicated](/media/develop/vsc-sqltools-connection-config-dedicated.jpg)

6.  **「テスト接続」**をクリックして、 TiDB Cloud Dedicated クラスターへの接続を検証します。

    1.  ポップアップウィンドウで、 **[許可]**をクリックします。
    2.  **SQLToolsDriver資格情報**ダイアログで、 TiDB Cloud Dedicated クラスターのパスワードを入力します。

    ![VS Code SQLTools: enter password to connect to TiDB Cloud Dedicated](/media/develop/vsc-sqltools-password.jpg)

7.  接続テストが成功すると、「**正常に接続されました！」**というメッセージが表示されます。 **「接続を保存」**をクリックして接続設定を保存します。

</div>
<div label="TiDB Self-Managed" value="tidb">

1.  VS Codeを起動し、ナビゲーションペインで**SQLTools**拡張機能を選択します。 **「接続」**セクションで**「新しい接続の追加」を**クリックし、データベースドライバーとして**TiDBを**選択します。

    ![VS Code SQLTools: add new connection](/media/develop/vsc-sqltools-add-new-connection.jpg)

2.  設定ペインで、次の接続パラメータを構成します。

    -   **接続名**: この接続に意味のある名前を付けます。

    -   **接続グループ**: (オプション) この接続グループに分かりやすい名前を付けます。同じグループ名の接続はグループ化されます。

    -   **接続方法**:**サーバーおよびポート**を選択します。

    -   **サーバー アドレス**: TiDB セルフマネージド クラスターの IP アドレスまたはドメイン名を入力します。

    -   **ポート**: TiDB セルフマネージド クラスターのポート番号を入力します。

    -   **データベース**: 接続するデータベースを入力します。

    -   **ユーザー名**: TiDB セルフマネージド クラスターに接続するために使用するユーザー名を入力します。

    -   **パスワードモード**:

        -   パスワードが空の場合は、 **「空のパスワードを使用する」**を選択します。
        -   それ以外の場合は、 **SQLToolsDriver資格情報**を選択します。

    -   **MySQL ドライバー固有のオプション**領域で、次のパラメータを設定します。

        -   **認証プロトコル**:**デフォルト**を選択します。
        -   **SSL** : **「無効」**を選択します。

    ![VS Code SQLTools: configure connection settings for TiDB Self-Managed](/media/develop/vsc-sqltools-connection-config-self-hosted.jpg)

3.  **[テスト接続]**をクリックして、TiDB セルフマネージド クラスターへの接続を検証します。

    パスワードが空でない場合は、ポップアップ ウィンドウで**[許可]**をクリックし、TiDB セルフマネージド クラスターのパスワードを入力します。

    ![VS Code SQLTools: enter password to connect to TiDB Self-Managed](/media/develop/vsc-sqltools-password.jpg)

4.  接続テストが成功すると、「**正常に接続されました！」という**メッセージが表示されます。 **「接続を保存」**をクリックして接続設定を保存します。

</div>
</SimpleTab>

## 次のステップ {#next-steps}

-   Visual Studio Code の使い方を[Visual Studio Codeのドキュメント](https://code.visualstudio.com/docs)から詳しく学びます。
-   SQLTools の[ドキュメント](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools)と[GitHubリポジトリ](https://github.com/mtxr/vscode-sqltools)から、VS Code SQLTools 拡張機能の詳細な使用方法を学習します。
-   [開発者ガイド](https://docs.pingcap.com/developer/)の[データを挿入する](/develop/dev-guide-insert-data.md) 、 [データを更新する](/develop/dev-guide-update-data.md) 、 [データを削除する](/develop/dev-guide-delete-data.md) 、 [単一テーブルの読み取り](/develop/dev-guide-get-data-from-single-table.md) 、 [取引](/develop/dev-guide-transaction-overview.md) 、 [SQLパフォーマンスの最適化](/develop/dev-guide-optimize-sql-overview.md)などの章で、 TiDB アプリケーション開発のベスト プラクティスを学習します。
-   プロフェッショナル[TiDB開発者コース](https://www.pingcap.com/education/)を通じて学習し、試験に合格すると[TiDB認定](https://www.pingcap.com/education/certification/)獲得します。

## ヘルプが必要ですか? {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに問い合わせてください。
-   [TiDB Cloudのサポートチケットを送信する](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDBセルフマネージドのサポートチケットを送信する](/support.md)
