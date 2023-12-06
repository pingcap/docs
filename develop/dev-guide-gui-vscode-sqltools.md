---
title: Connect to TiDB with Visual Studio Code
summary: Learn how to connect to TiDB using Visual Studio Code or GitHub Codespaces.
---

# Visual Studio Code を使用して TiDB に接続する {#connect-to-tidb-with-visual-studio-code}

TiDB は MySQL と互換性のあるデータベースであり、 [Visual Studio コード (VS コード)](https://code.visualstudio.com/)かつ強力なソース コード エディターです。このチュートリアルでは、TiDB を[公式ドライバー](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools-driver-mysql)としてサポートする[SQLツール](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools)拡張機能を使用します。

このチュートリアルでは、Visual Studio Code を使用して TiDB クラスターに接続する方法を学習できます。

> **注記：**
>
> -   このチュートリアルは、TiDB サーバーレス、TiDB 専用、および TiDB セルフホストと互換性があります。
> -   このチュートリアルは、 [GitHub コードスペース](https://github.com/features/codespaces) 、 [Visual Studio コード開発コンテナ](https://code.visualstudio.com/docs/devcontainers/containers) 、 [Visual Studio コード WSL](https://code.visualstudio.com/docs/remote/wsl)などの Visual Studio Code リモート開発環境でも動作します。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、次のものが必要です。

-   [Visual Studio コード](https://code.visualstudio.com/#alt-downloads) **1.72.0**以降のバージョン。
-   Visual Studio Code の[SQLツールMySQL/MariaDB/TiDB](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools-driver-mysql)拡張機能。インストールするには、次のいずれかの方法を使用できます。
    -   <a href="vscode:extension/mtxr.sqltools-driver-mysql">このリンク</a>をクリックして VS Code を起動し、拡張機能を直接インストールします。
    -   [VS コード マーケットプレイス](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools-driver-mysql)に移動し、 **「インストール」を**クリックします。
-   TiDB クラスター。

<CustomContent platform="tidb">

**TiDB クラスターがない場合は、次のように作成できます。**

-   (推奨) [TiDB サーバーレスクラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って、独自のTiDB Cloudクラスターを作成します。
-   [ローカル テスト TiDB クラスターをデプロイ](/quick-start-with-tidb.md#deploy-a-local-test-cluster)または[本番TiDB クラスターをデプロイ](/production-deployment-using-tiup.md)に従ってローカル クラスターを作成します。

</CustomContent>
<CustomContent platform="tidb-cloud">

**TiDB クラスターがない場合は、次のように作成できます。**

-   (推奨) [TiDB サーバーレスクラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って、独自のTiDB Cloudクラスターを作成します。
-   [ローカル テスト TiDB クラスターをデプロイ](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster)または[本番TiDB クラスターをデプロイ](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup)に従ってローカル クラスターを作成します。

</CustomContent>

## TiDB に接続する {#connect-to-tidb}

選択した TiDB デプロイメント オプションに応じて、TiDB クラスターに接続します。

<SimpleTab>
<div label="TiDB Serverless">

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして、その概要ページに移動します。

2.  右上隅にある**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログの設定が動作環境と一致していることを確認してください。

    -   **エンドポイント タイプは**`Public`に設定されます。

    -   **ブランチは**`main`に設定されます。

    -   **[接続先] は**`VS Code`に設定されます。

    -   **オペレーティング システムが**環境に一致します。

    > **ヒント：**
    >
    > VS Code がリモート開発環境で実行されている場合は、リストからリモート オペレーティング システムを選択します。たとえば、Windows Subsystem for Linux (WSL) を使用している場合は、対応する Linux ディストリビューションに切り替えます。 GitHub コードスペースを使用している場合、これは必要ありません。

4.  **「パスワードの生成」**をクリックして、ランダムなパスワードを作成します。

    > **ヒント：**
    >
    > 以前にパスワードを作成したことがある場合は、元のパスワードを使用するか、 **「パスワードのリセット」**をクリックして新しいパスワードを生成できます。

5.  VS Code を起動し、ナビゲーション ペインで**SQLTools**拡張機能を選択します。 **[接続]**セクションで、 **[新しい接続の追加]**をクリックし、データベース ドライバーとして**TiDB**を選択します。

    ![VS Code SQLTools: add new connection](/media/develop/vsc-sqltools-add-new-connection.jpg)

6.  設定ペインで、次の接続パラメータを構成します。

    -   **接続名**: この接続に意味のある名前を付けます。
    -   **接続グループ**: (オプション) この接続グループに意味のある名前を付けます。同じグループ名の接続はグループ化されます。
    -   **次の方法で接続します**。**サーバーとポート**を選択します。
    -   **サーバーアドレス**: TiDB Cloud接続ダイアログから`HOST`パラメータを入力します。
    -   **ポート**: TiDB Cloud接続ダイアログから`PORT`パラメータを入力します。
    -   **データベース**: 接続するデータベースを入力します。
    -   **ユーザー名**: TiDB Cloud接続ダイアログから`USERNAME`パラメータを入力します。
    -   **パスワード モード**: **[SQLTools Driver Credentials]**を選択します。
    -   **MySQL ドライバー固有のオプション**領域で、次のパラメーターを構成します。

        -   **認証プロトコル**:**デフォルト**を選択します。
        -   **SSL** : **「有効」**を選択します。 TiDB サーバーレスには安全な接続が必要です。 **「SSL オプション (node.TLSSocket)」**領域で、 **「認証局 (CA) 証明書ファイル」**フィールドをTiDB Cloud接続ダイアログの`CA`パラメーターとして構成します。

            > **注記：**
            >
            > Windows または GitHub コードスペースで実行している場合は、 **SSL を**空白のままにすることができます。デフォルトでは、SQLTools は Let&#39;s Encrypt によって厳選された有名な CA を信頼します。詳細については、 [TiDB サーバーレスのルート証明書管理](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-clusters#root-certificate-management)を参照してください。

    ![VS Code SQLTools: configure connection settings for TiDB Serverless](/media/develop/vsc-sqltools-connection-config-serverless.jpg)

7.  **「接続のテスト」**をクリックして、TiDB サーバーレスクラスターへの接続を検証します。

    1.  ポップアップ ウィンドウで、 **[許可]**をクリックします。
    2.  **[SQLTools Driver Credentials]**ダイアログで、手順 4 で作成したパスワードを入力します。

        ![VS Code SQLTools: enter password to connect to TiDB Serverless](/media/develop/vsc-sqltools-password.jpg)

8.  接続テストが成功すると、「**接続に成功しました!」**と表示されます。メッセージ。 「接続**を保存」**をクリックして接続構成を保存します。

</div>
<div label="TiDB Dedicated">

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして、その概要ページに移動します。

2.  右上隅にある**「接続」**をクリックします。接続ダイアログが表示されます。

3.  **[どこからでもアクセスを許可する]**をクリックします。

    接続文字列の取得方法の詳細については、 [TiDB専用標準接続](https://docs.pingcap.com/tidbcloud/connect-via-standard-connection)を参照してください。

4.  VS Code を起動し、ナビゲーション ペインで**SQLTools**拡張機能を選択します。 **[接続]**セクションで、 **[新しい接続の追加]**をクリックし、データベース ドライバーとして**TiDB**を選択します。

    ![VS Code SQLTools: add new connection](/media/develop/vsc-sqltools-add-new-connection.jpg)

5.  設定ペインで、次の接続パラメータを構成します。

    -   **接続名**: この接続に意味のある名前を付けます。
    -   **接続グループ**: (オプション) この接続グループに意味のある名前を付けます。同じグループ名の接続はグループ化されます。
    -   **次の方法で接続します**。**サーバーとポート**を選択します。
    -   **サーバーアドレス**: TiDB Cloud接続ダイアログから`host`パラメータを入力します。
    -   **ポート**: TiDB Cloud接続ダイアログから`port`パラメータを入力します。
    -   **データベース**: 接続するデータベースを入力します。
    -   **ユーザー名**: TiDB Cloud接続ダイアログから`user`パラメータを入力します。
    -   **パスワード モード**: **[SQLTools Driver Credentials]**を選択します。
    -   **MySQL ドライバー固有のオプション**領域で、次のパラメーターを構成します。

        -   **認証プロトコル**:**デフォルト**を選択します。
        -   **SSL** : **「無効」**を選択します。

    ![VS Code SQLTools: configure connection settings for TiDB Dedicated](/media/develop/vsc-sqltools-connection-config-dedicated.jpg)

6.  **「接続のテスト」**をクリックして、TiDB 専用クラスターへの接続を検証します。

    1.  ポップアップ ウィンドウで、 **[許可]**をクリックします。
    2.  **[SQLTools Driver Credentials]**ダイアログで、TiDB 専用クラスターのパスワードを入力します。

    ![VS Code SQLTools: enter password to connect to TiDB Dedicated](/media/develop/vsc-sqltools-password.jpg)

7.  接続テストが成功すると、「**接続に成功しました!」**と表示されます。メッセージ。 「接続**を保存」**をクリックして接続構成を保存します。

</div>
<div label="TiDB Self-Hosted">

1.  VS Code を起動し、ナビゲーション ペインで**SQLTools**拡張機能を選択します。 **[接続]**セクションで、 **[新しい接続の追加]**をクリックし、データベース ドライバーとして**TiDB**を選択します。

    ![VS Code SQLTools: add new connection](/media/develop/vsc-sqltools-add-new-connection.jpg)

2.  設定ペインで、次の接続パラメータを構成します。

    -   **接続名**: この接続に意味のある名前を付けます。

    -   **接続グループ**: (オプション) この接続グループに意味のある名前を付けます。同じグループ名の接続はグループ化されます。

    -   **次の方法で接続します**。**サーバーとポート**を選択します。

    -   **サーバーアドレス**: TiDB セルフホストクラスターの IP アドレスまたはドメイン名を入力します。

    -   **ポート**: TiDB セルフホスト クラスターのポート番号を入力します。

    -   **データベース**: 接続するデータベースを入力します。

    -   **ユーザー名**: TiDB セルフホスト クラスターへの接続に使用するユーザー名を入力します。

    -   **パスワードモード**:

        -   パスワードが空の場合は、 **「空のパスワードを使用する」**を選択します。
        -   それ以外の場合は、 **SQLTools Driver Credentials**を選択します。

    -   **MySQL ドライバー固有のオプション**領域で、次のパラメーターを構成します。

        -   **認証プロトコル**:**デフォルト**を選択します。
        -   **SSL** : **「無効」**を選択します。

    ![VS Code SQLTools: configure connection settings for TiDB Self-Hosted](/media/develop/vsc-sqltools-connection-config-self-hosted.jpg)

3.  **「接続のテスト」**をクリックして、TiDB セルフホストクラスターへの接続を検証します。

    パスワードが空でない場合は、ポップアップ ウィンドウで**[許可]**をクリックし、TiDB セルフホスト クラスターのパスワードを入力します。

    ![VS Code SQLTools: enter password to connect to TiDB Self-Hosted](/media/develop/vsc-sqltools-password.jpg)

4.  接続テストが成功すると、「**接続に成功しました!」**と表示されます。メッセージ。 「接続**を保存」**をクリックして接続構成を保存します。

</div>
</SimpleTab>

## 次のステップ {#next-steps}

-   Visual Studio Code の詳しい使い方を[Visual Studio Code のドキュメント](https://code.visualstudio.com/docs)から学びましょう。
-   VS Code SQLTools 拡張機能の使用法については、SQLTools の[文書](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools)と[GitHub リポジトリ](https://github.com/mtxr/vscode-sqltools)から学びましょう。
-   TiDB アプリケーション開発[単一テーブルの読み取り](/develop/dev-guide-get-data-from-single-table.md)ベスト プラクティスについて[取引](/develop/dev-guide-transaction-overview.md) 、 [開発者ガイド](/develop/dev-guide-overview.md)の章 ( [データの挿入](/develop/dev-guide-insert-data.md)など) [データを更新する](/develop/dev-guide-update-data.md)参照[データの削除](/develop/dev-guide-delete-data.md) [SQLパフォーマンスの最適化](/develop/dev-guide-optimize-sql-overview.md)ください。
-   プロフェッショナルとして[TiDB 開発者コース](https://www.pingcap.com/education/)を学び、試験合格後に[TiDB 認定](https://www.pingcap.com/education/certification/)獲得します。

## 助けが必要？ {#need-help}

[不和](https://discord.gg/vYU9h56kAX)または[サポートチケットを作成する](https://support.pingcap.com/)について質問してください。
