---
title: Connect to TiDB with Visual Studio Code
summary: Visual Studio CodeまたはGitHub Codespacesを使用してTiDBに接続する方法を学びましょう。
aliases: ['/ja/tidb/stable/dev-guide-gui-vscode-sqltools/','/ja/tidb/dev/dev-guide-gui-vscode-sqltools/','/ja/tidbcloud/dev-guide-gui-vscode-sqltools/']
---

# Visual Studio Codeを使用してTiDBに接続する {#connect-to-tidb-with-visual-studio-code}

TiDB は MySQL 互換データベースであり、 [Visual Studio Code (VS Code)](https://code.visualstudio.com/)は軽量かつ強力なソース コード エディターです。このチュートリアルでは、TiDB を[公式ドライバー](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools-driver-mysql)としてサポートする[SQLツール](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools)拡張機能を使用します。

このチュートリアルでは、Visual Studio Code を使用して TiDB に接続する方法を学ぶことができます。

> **Note:**
>
> - このチュートリアルは、 TiDB Cloud Starter、 TiDB Cloud Essential、 TiDB Cloud Premium、 TiDB Cloud Dedicated、およびTiDB Self-Managedに対応しています。
> - このチュートリアルは、 [GitHub Codespaces](https://github.com/features/codespaces) 、Visual Studio [Visual Studio Code 開発コンテナ](https://code.visualstudio.com/docs/devcontainers/containers)[Visual Studio Code WSL](https://code.visualstudio.com/docs/remote/wsl) Code リモート開発環境でも動作します。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、以下が必要です。

- [Visual Studio Code](https://code.visualstudio.com/#alt-downloads) **1.72.0**以降のバージョン。
- [SQLTools MySQL/MariaDB/TiDB](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools-driver-mysql)拡張機能です。インストールするには、以下のいずれかの方法を使用できます。
    - <a href="vscode:extension/mtxr.sqltools-driver-mysql">このリンク</a>をクリックするとVS Codeが起動し、拡張機能を直接インストールできます。
    - [VS Code マーケットプレイス](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools-driver-mysql)に移動し、 **Install**をクリックします。
    - VS Code の**Extensions**タブで`mtxr.sqltools-driver-mysql`を検索して**SQLTools MySQL/MariaDB/TiDB**拡張機能を取得し、 **Install**をクリックします。
- TiDBクラスタ。

**TiDBクラスタをお持ちでない場合は、以下の手順で作成できます。**

- (推奨) [TiDB Cloud Starterインスタンスを作成する](/develop/dev-guide-build-cluster-in-cloud.md)。
- [ローカルテスト用のTiDB Self-Managedクラスタをデプロイ](/quick-start-with-tidb.md#deploy-a-local-test-cluster)または[本番のTiDB Self-Managedクラスタをデプロイ](/production-deployment-using-tiup.md)

## TiDBに接続する {#connect-to-tidb}

選択したTiDBのデプロイオプションに応じて、TiDBに接続してください。

<SimpleTab>
<div label="TiDB Cloud Starter or Essential">

1. [**My TiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud StarterまたはEssentialインスタンスの名前をクリックして、概要ページに移動します。

2. 右上隅の**Connect**をクリックしてください。接続ダイアログが表示されます。

3. 接続ダイアログの設定がご使用のオペレーティング環境と一致していることを確認してください。

    - **Connection Type**は`Public`に設定されています。

    - **Branch**は`main`に設定されています。

    - **Connect With**は`VS Code`に設定されています。

    - お使いの環境に合った**Operating System**を選択してください。

    > **Tip:**
    >
    > VS Code をリモート開発環境で実行している場合は、リストからリモートのオペレーティングシステムを選択してください。たとえば、Windows Subsystem for Linux (WSL) を使用している場合は、対応する Linux ディストリビューションに切り替えてください。GitHub Codespaces を使用している場合は、この操作は不要です。

4. **Generate Password**をクリックすると、ランダムなパスワードが生成されます。

    > **Tip:**
    >
    > 以前にパスワードを作成したことがある場合は、元のパスワードを使用するか、 **Reset Password**をクリックして新しいパスワードを生成できます。

5. VS Codeを起動し、ナビゲーションペインで**SQLTools**拡張機能を選択します。 **CONNECTIONS**セクションで**Add New Connection**をクリックし、データベースドライバとして**TiDB**を選択します。

    ![VS Code SQLTools: add new connection](/media/develop/vsc-sqltools-add-new-connection.jpg)

6. 設定画面で、以下の接続パラメータを設定します。

    - **Connection name**：この接続に分かりやすい名前を付けてください。
    - **Connection group**：（オプション）この接続グループに分かりやすい名前を付けます。同じグループ名を持つ接続はグループ化されます。
    - **Connect using**：**Server and Port**を選択してください。
    - **Server Address**： TiDB Cloud接続ダイアログから`HOST`パラメータを入力します。
    - **Port**: TiDB Cloud接続ダイアログから`PORT`パラメータを入力します。
    - **Database**：接続したいデータベースを入力してください。
    - **Username**： TiDB Cloud接続ダイアログから`USERNAME`パラメータを入力してください。
    - **Password mode**: **SQLTools Driver Credentials**を選択します。
    - **MySQL driver specific options**領域で、以下のパラメータを設定します。

        - **Authentication Protocol**：**default**を選択してください。
        - **SSL** ： **Enabled**を選択します。TiDB Cloud Starterは安全な接続を必要とします。**SSL Options (node.TLSSocket)**領域で、 TiDB Cloud接続ダイアログの`CA`パラメーターを**Certificate Authority (CA) Certificate File**フィールドに設定してください。

            > **Note:**
            >
            > Windows または GitHub Codespacesで実行している場合は、 **SSL** を空白のままにすることができます。デフォルトでは、SQLTools は Let's Encrypt によって厳選された有名な CA を信頼します。詳細については、 [TiDB Cloud Starterルート証明書管理](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-clusters#root-certificate-management)を参照してください。

    ![VS Code SQLTools: configure connection settings for TiDB Cloud Starter](/media/develop/vsc-sqltools-connection-config-serverless.jpg)

7. **TEST CONNECTION**をクリックして、対象のTiDB Cloud StarterまたはEssentialインスタンスへの接続を検証してください。

    1. ポップアップウィンドウで**Allow**をクリックします。
    2. **SQLTools Driver Credentials**ダイアログで、手順4で作成したパスワードを入力します。

        ![VS Code SQLTools: enter password to connect to TiDB Cloud Starter](/media/develop/vsc-sqltools-password.jpg)

8. 接続テストが成功すると、**Successfully connected!**というメッセージが表示されます。 **SAVE CONNECTION**をクリックして、接続設定を保存してください。

</div>
<div label="TiDB Cloud Premium">

1. [**My TiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud Premiumインスタンスの名前をクリックして概要ページに移動します。

2. 左側のナビゲーションペインで、 **Settings** &gt; **Networking**をクリックします。

3. **Networking**ページで、 **Public Endpoint**の**Enable**をクリックし、次に**Add IP Address**をクリックします。

    クライアントのIPアドレスがアクセスリストに追加されていることを確認してください。

4. 左側のナビゲーションペインで**Overview**をクリックすると、インスタンスの概要ページに戻ります。

5. 右上隅の**Connect**をクリックしてください。接続ダイアログが表示されます。

6. 接続ダイアログで、 **Connection Type**ドロップダウンリストから**Public**を選択します。

    - 公開エンドポイントがまだ有効化中であることを示すメッセージが表示された場合は、処理が完了するまでお待ちください。
    - まだパスワードを設定していない場合は、ダイアログの**Set Root Password**をクリックしてください。
    - サーバー証明書を確認する必要がある場合、または接続に失敗して認証局（CA）証明書が必要な場合は、 **CA cert**をクリックしてダウンロードしてください。
    - **Public**接続タイプに加えて、 TiDB Cloud Premium は**Private Endpoint**接続をサポートします。詳細については、 [AWS PrivateLink経由でTiDB Cloud Premiumに接続します](/tidb-cloud/premium/connect-to-premium-via-aws-private-endpoint.md)を参照してください。

7. VS Codeを起動し、ナビゲーションペインで**SQLTools**拡張機能を選択します。 **CONNECTIONS**セクションで**Add New Connection**をクリックし、データベースドライバとして**TiDB**を選択します。

8. 設定画面で、以下の接続パラメータを設定します。

    - **Connect using**：**Server and Port**を選択してください。
    - **Server Address**： TiDB Cloud接続ダイアログから`host`パラメータを入力します。
    - **Port**: TiDB Cloud接続ダイアログから`port`パラメータを入力します。
    - **Database**：接続したいデータベースを入力してください。
    - **Username**： TiDB Cloud接続ダイアログから`user`パラメータを入力してください。
    - **Password mode**: **SQLTools Driver Credentials**を選択します。
    - **MySQL driver specific options**領域で、以下のパラメータを設定します。

        - **Authentication Protocol**：**default**を選択してください。
        - **SSL** ：**Disabled**を選択してください。

9. **TEST CONNECTION**をクリックして、 TiDB Cloud Premiumインスタンスへの接続を検証してください。

10. **SQLTools Driver Credentials**ダイアログで、パスワードを入力します。

11. 接続テストが成功したら、 **SAVE CONNECTION**をクリックして接続設定を保存します。

</div>
<div label="TiDB Cloud Dedicated">

1. [**My TiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud Dedicatedクラスタの名前をクリックして概要ページに移動します。

2. 右上隅の**Connect**をクリックしてください。接続ダイアログが表示されます。

3. 接続ダイアログで、 **Connection Type**ドロップダウンリストから**Public**を選択し、 **CA cert**をクリックしてCA証明書をダウンロードします。

    IP アクセス リストを設定していない場合は、最初の接続の前に、 **Configure IP Access List**をクリックするか、[IP アクセス リストを設定する](https://docs.pingcap.com/tidbcloud/configure-ip-access-list)の手順に従って設定します。

    TiDB Cloud Dedicated は、**Public**接続タイプに加えて、**Private Endpoint**および**VPC Peering**接続タイプもサポートしています。詳細については、 [TiDB Cloud Dedicatedクラスタに接続します](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)を参照してください。

4. VS Codeを起動し、ナビゲーションペインで**SQLTools**拡張機能を選択します。 **CONNECTIONS**セクションで**Add New Connection**をクリックし、データベースドライバとして**TiDB**を選択します。

    ![VS Code SQLTools: add new connection](/media/develop/vsc-sqltools-add-new-connection.jpg)

5. 設定画面で、以下の接続パラメータを設定します。

    - **Connection name**：この接続に分かりやすい名前を付けてください。
    - **Connection group**：（オプション）この接続グループに分かりやすい名前を付けます。同じグループ名を持つ接続はグループ化されます。
    - **Connect using**：**Server and Port**を選択してください。
    - **Server Address**： TiDB Cloud接続ダイアログから`host`パラメータを入力します。
    - **Port**: TiDB Cloud接続ダイアログから`port`パラメータを入力します。
    - **Database**：接続したいデータベースを入力してください。
    - **Username**： TiDB Cloud接続ダイアログから`user`パラメータを入力してください。
    - **Password mode**: **SQLTools Driver Credentials**を選択します。
    - **MySQL driver specific options**領域で、以下のパラメータを設定します。

        - **Authentication Protocol**：**default**を選択してください。
        - **SSL** ：**Disabled**を選択してください。

    ![VS Code SQLTools: configure connection settings for TiDB Cloud Dedicated](/media/develop/vsc-sqltools-connection-config-dedicated.jpg)

6. **TEST CONNECTION**をクリックして、 TiDB Cloud Dedicatedクラスターへの接続を検証してください。

    1. ポップアップウィンドウで**Allow**をクリックします。
    2. **SQLTools Driver Credentials**ダイアログで、 TiDB Cloud Dedicatedクラスタのパスワードを入力します。

    ![VS Code SQLTools: enter password to connect to TiDB Cloud Dedicated](/media/develop/vsc-sqltools-password.jpg)

7. 接続テストが成功すると、**Successfully connected!**というメッセージが表示されます。 **SAVE CONNECTION**をクリックして、接続設定を保存してください。

</div>
<div label="TiDB Self-Managed" value="tidb">

1. VS Codeを起動し、ナビゲーションペインで**SQLTools**拡張機能を選択します。 **CONNECTIONS**セクションで**Add New Connection**をクリックし、データベースドライバとして**TiDB**を選択します。

    ![VS Code SQLTools: add new connection](/media/develop/vsc-sqltools-add-new-connection.jpg)

2. 設定画面で、以下の接続パラメータを設定します。

    - **Connection name**：この接続に分かりやすい名前を付けてください。

    - **Connection group**：（オプション）この接続グループに分かりやすい名前を付けます。同じグループ名を持つ接続はグループ化されます。

    - **Connect using**：**Server and Port**を選択してください。

    - **Server Address**：TiDB Self-ManagedクラスタのIPアドレスまたはドメイン名を入力してください。

    - **Port**：TiDB Self-Managedクラスタのポート番号を入力してください。

    - **Database**：接続したいデータベースを入力してください。

    - **Username**：TiDB Self-Managedクラスタに接続するために使用するユーザー名を入力してください。

    - **Password mode**：

        - パスワードが空欄の場合は、 **Use empty password**を選択してください。
        - それ以外の場合は、 **SQLTools Driver Credentials**を選択してください。

    - **MySQL driver specific options**領域で、以下のパラメータを設定します。

        - **Authentication Protocol**：**default**を選択してください。
        - **SSL** ：**Disabled**を選択してください。

    ![VS Code SQLTools: configure connection settings for TiDB Self-Managed](/media/develop/vsc-sqltools-connection-config-self-hosted.jpg)

3. **TEST CONNECTION**をクリックして、TiDB Self-Managedクラスタへの接続を検証してください。

    パスワードが空欄でない場合は、ポップアップウィンドウで**Allow**をクリックし、TiDB Self-Managedクラスタのパスワードを入力してください。

    ![VS Code SQLTools: enter password to connect to TiDB Self-Managed](/media/develop/vsc-sqltools-password.jpg)

4. 接続テストが成功すると、**Successfully connected!**というメッセージが表示されます。 **SAVE CONNECTION**をクリックして、接続設定を保存してください。

</div>
</SimpleTab>

## 次のステップ {#next-steps}

- Visual Studio Code の使用法の詳細については[Visual Studio Code のドキュメント](https://code.visualstudio.com/docs)を参照してください。
- VS Code SQLTools 拡張機能の使用法について詳しくは、SQLTools の[ドキュメント](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools)および[GitHubリポジトリ](https://github.com/mtxr/vscode-sqltools)ご覧ください。
- [開発者ガイド](https://docs.pingcap.com/developer/) の [データを挿入する](/develop/dev-guide-insert-data.md)、[データの更新](/develop/dev-guide-update-data.md)、[データを削除する](/develop/dev-guide-delete-data.md)、[単一表の読み取り](/develop/dev-guide-get-data-from-single-table.md)、[トランザクション](/develop/dev-guide-transaction-overview.md)、[SQLパフォーマンス最適化](/develop/dev-guide-optimize-sql-overview.md) などの章を参考に、TiDB アプリケーション開発のベストプラクティスを学びます。
- プロフェッショナルな[TiDB開発者向けコース](https://www.pingcap.com/education/)コースを通じて学習し、試験に合格すると[TiDB認定資格](https://www.pingcap.com/education/certification/)を取得します。

## お困りですか？ {#need-help}

- [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc)or [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs)コミュニティに質問してください。
- [TiDB Cloudのサポートチケットを送信してください](https://tidb.support.pingcap.com/servicedesk/customer/portals)
- [TiDB Self-Managedのサポートチケットを送信してください](/support.md)
