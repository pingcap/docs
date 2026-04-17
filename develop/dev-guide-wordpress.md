---
title: Integrate WordPress with TiDB Cloud Starter
summary: TiDB Cloud Starterを使ってWordPressを実行する方法を学びましょう。このチュートリアルでは、WordPressとTiDB Cloud Starterを数分で実行するための手順をステップバイステップで解説します。
aliases: ['/ja/tidbcloud/dev-guide-wordpress/']
---

# WordPressとTiDB Cloud Starterを統合する {#integrate-wordpress-with-tidb-cloud-starter}

TiDBはMySQL互換データベースであり、 TiDB Cloud Starterはフルマネージド型のTiDBサービスです。WordPress [WordPress](https://github.com/WordPress) 、ユーザーがウェブサイトを作成・管理できる無料のオープンソースコンテンツ管理システム（CMS）です。WordPressはPHPで記述されており、MySQLデータベースを使用しています。

このチュートリアルでは、 TiDB Cloud Starterを使用してWordPressを無料で実行する方法を学ぶことができます。

> **注記：**
>
> このチュートリアルは、 TiDB Cloud Starterに加えて、 TiDB Cloud Essential、 TiDB Cloud Dedicated、および TiDB Self-Managed でも動作します。ただし、コスト効率を考慮すると、WordPress はTiDB Cloud Starterで実行することを強くお勧めします。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、以下が必要です。

-   お持ちでない場合は、 [TiDB Cloud Starterインスタンスを作成する](/develop/dev-guide-build-cluster-in-cloud.md)。

## TiDB Cloud StarterでWordPressを実行する {#run-wordpress-with-tidb-cloud-starter}

このセクションでは、TiDB Cloud Starterを使用して WordPress を実行する方法を説明します。

### ステップ1：WordPressサンプルリポジトリをクローンする {#step-1-clone-the-wordpress-sample-repository}

サンプルコードリポジトリをクローンするには、ターミナルウィンドウで以下のコマンドを実行してください。

```shell
git clone https://github.com/Icemap/wordpress-tidb-docker.git
cd wordpress-tidb-docker
```

### ステップ2：依存関係をインストールする {#step-2-install-dependencies}

1.  サンプルリポジトリでは、WordPressを起動するために[ドッカー](https://www.docker.com/)と[Docker Compose](https://docs.docker.com/compose/)必要です。既にインストール済みであれば、この手順はスキップできます。WordPressはLinux環境（Ubuntuなど）で実行することを強くお勧めします。DockerとDocker Composeをインストールするには、次のコマンドを実行してください。

    ```shell
    sudo sh install.sh
    ```

2.  サンプル リポジトリには、サブモジュールとして[TiDB互換性プラグイン](https://github.com/pingcap/wordpress-tidb-plugin)が含まれています。次のコマンドを実行してサブモジュールを更新します。

    ```shell
    git submodule update --init --recursive
    ```

### ステップ3：接続情報の設定 {#step-3-configure-connection-information}

TiDB Cloud StarterへのWordPressデータベース接続を設定します。

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、次に、対象のTiDB Cloud Starterインスタンスの名前をクリックして、概要ページに移動します。

2.  右上隅の**「接続」**をクリックしてください。接続ダイアログが表示されます。

3.  接続ダイアログの設定がご使用のオペレーティング環境と一致していることを確認してください。

    -   **接続タイプ**は`Public`に設定されています。
    -   **「接続」は**`WordPress`に設定されています。
    -   **オペレーティングシステム**は`Debian/Ubuntu/Arch`に設定されています。
    -   **データベースは**、使用したいデータベースに設定されます。たとえば、 `test` 。

4.  **「パスワードを生成」を**クリックすると、ランダムなパスワードが生成されます。

    > **ヒント：**
    >
    > 以前にパスワードを作成したことがある場合は、元のパスワードを使用するか、 **「パスワードをリセット」**をクリックして新しいパスワードを生成できます。

5.  `.env.example`をコピーして`.env`に名前を変更するには、次のコマンドを実行します。

    ```shell
    cp .env.example .env
    ```

6.  対応する接続​​文字列`.env`ファイルにコピー＆ペーストしてください。例は以下のとおりです。

    ```dotenv
    TIDB_HOST='{HOST}'  # e.g. gateway01.ap-northeast-1.prod.aws.tidbcloud.com
    TIDB_PORT='4000'
    TIDB_USER='{USERNAME}'  # e.g. xxxxxx.root
    TIDB_PASSWORD='{PASSWORD}'
    TIDB_DB_NAME='test'
    ```

    プレースホルダー`{}`を、接続ダイアログから取得した接続パラメータに置き換えてください。デフォルトでは、 TiDB Cloud Starterには`test`データベースが付属しています。TiDB Cloud Starterインスタンスで既に別のデータベースを作成している場合は、 `test`データベース名に置き換えてください。

7.  `.env`ファイルを保存します。

### ステップ4： TiDB Cloud StarterでWordPressを起動する {#step-4-start-wordpress-with-tidb-cloud-starter}

1.  WordPressをDockerコンテナとして実行するには、以下のコマンドを実行してください。

    ```shell
    docker compose up -d
    ```

2.  ローカルマシンでコンテナを起動した場合は[localhost](http://localhost/)にアクセスしてWordPressサイトをセットアップし、リモートマシンでWordPressが実行されている場合は`http://<your_instance_ip>`にアクセスしてください。

### ステップ5：データベース接続を確認する {#step-5-confirm-the-database-connection}

1.  TiDB CloudコンソールでTiDB Cloud Starterインスタンスの接続ダイアログを閉じ、 **SQLエディタ**ページを開きます。
2.  左側の**「スキーマ」**タブで、WordPressに接続したデータベースをクリックします。
3.  そのデータベースのテーブル一覧に、WordPressのテーブル（ `wp_posts`や`wp_comments`など）が表示されていることを確認してください。

## お困りですか？ {#need-help}

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)or [スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに質問するか、[サポートチケットを送信してください](https://tidb.support.pingcap.com/)。
