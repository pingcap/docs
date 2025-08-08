---
title: Connect to TiDB Cloud Serverless with WordPress
summary: TiDB Cloud Serverlessを使ってWordPressを実行する方法を学びましょう。このチュートリアルでは、WordPress + TiDB Cloud Serverlessを数分で実行するための手順をステップバイステップで説明します。
---

# WordPressでTiDB Cloud Serverlessに接続する {#connect-to-tidb-cloud-serverless-with-wordpress}

TiDBはMySQL互換データベース、 TiDB Cloud ServerlessはフルマネージドのTiDBサービス、そして[ワードプレス](https://github.com/WordPress)ユーザーがウェブサイトを作成・管理できる無料のオープンソースコンテンツ管理システム（CMS）です。WordPressはPHPで記述されており、MySQLデータベースを使用します。

このチュートリアルでは、 TiDB Cloud Serverless を使用して WordPress を無料で実行する方法を学ぶことができます。

> **注記：**
>
> このチュートリアルは、 TiDB Cloud Serverless に加えて、 TiDB Cloud Dedicated および TiDB Self-Managed クラスターでも動作します。ただし、コスト効率の観点から、WordPress はTiDB Cloud Serverless で実行することを強くお勧めします。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、次のものが必要です。

-   TiDB Cloud Serverless クラスター。TiDB Cloud クラスターがまだない場合は、 [TiDB Cloud Serverless クラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って独自のTiDB Cloudクラスターを作成してください。

## TiDB Cloud ServerlessでWordPressを実行する {#run-wordpress-with-tidb-cloud-serverless}

このセクションでは、 TiDB Cloud Serverless を使用して WordPress を実行する方法を説明します。

### ステップ1: WordPressサンプルリポジトリをクローンする {#step-1-clone-the-wordpress-sample-repository}

サンプル コード リポジトリのクローンを作成するには、ターミナル ウィンドウで次のコマンドを実行します。

```shell
git clone https://github.com/Icemap/wordpress-tidb-docker.git
cd wordpress-tidb-docker
```

### ステップ2: 依存関係をインストールする {#step-2-install-dependencies}

1.  サンプルリポジトリでは、WordPressを起動するために[ドッカー](https://www.docker.com/)と[Dockerコンポーズ](https://docs.docker.com/compose/)必要です。すでにインストールされている場合は、この手順をスキップできます。WordPressはLinux環境（Ubuntuなど）で実行することを強くお勧めします。以下のコマンドを実行して、DockerとDocker Composeをインストールしてください。

    ```shell
    sudo sh install.sh
    ```

2.  サンプルリポジトリにはサブモジュールとして[TiDB 互換性プラグイン](https://github.com/pingcap/wordpress-tidb-plugin)含まれています。サブモジュールを更新するには、以下のコマンドを実行してください。

    ```shell
    git submodule update --init --recursive
    ```

### ステップ3: 接続情報を構成する {#step-3-configure-connection-information}

TiDB Cloud Serverless への WordPress データベース接続を構成します。

1.  [**クラスター**](https://tidbcloud.com/project/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログの構成が動作環境と一致していることを確認します。

    -   **接続タイプ**は`Public`に設定されています。
    -   **Connect With が**`WordPress`に設定されています。
    -   **オペレーティング システム**は`Debian/Ubuntu/Arch`に設定されています。
    -   **データベースは**、使用するデータベース（例： `test` ）に設定されます。

4.  ランダムなパスワードを作成するには、 **「パスワードの生成」を**クリックします。

    > **ヒント：**
    >
    > 以前にパスワードを作成したことがある場合は、元のパスワードを使用するか、 **「パスワードのリセット」を**クリックして新しいパスワードを生成することができます。

5.  次のコマンドを実行して`.env.example`コピーし、名前を`.env`に変更します。

    ```shell
    cp .env.example .env
    ```

6.  対応する接続文字列をコピーして、 `.env`ファイルに貼り付けます。結果の例は次のとおりです。

    ```dotenv
    TIDB_HOST='{HOST}'  # e.g. gateway01.ap-northeast-1.prod.aws.tidbcloud.com
    TIDB_PORT='4000'
    TIDB_USER='{USERNAME}'  # e.g. xxxxxx.root
    TIDB_PASSWORD='{PASSWORD}'
    TIDB_DB_NAME='test'
    ```

    プレースホルダー`{}`は、接続ダイアログで取得した接続パラメータに置き換えてください。デフォルトでは、 TiDB Cloud Serverlessには`test`データベースが付属しています。TiDB TiDB Cloud Serverlessクラスター内に既に別のデータベースを作成している場合は、 `test`データベース名に置き換えてください。

7.  `.env`ファイルを保存します。

### ステップ4: TiDB Cloud ServerlessでWordPressを起動する {#step-4-start-wordpress-with-tidb-cloud-serverless}

1.  WordPress を Docker コンテナとして実行するには、次のコマンドを実行します。

    ```shell
    docker compose up -d
    ```

2.  ローカル マシンでコンテナーを起動する場合は[ローカルホスト](http://localhost/)にアクセスし、WordPress がリモート マシンで実行されている場合は`http://<your_instance_ip>`アクセスして、WordPress サイトをセットアップします。

### ステップ5: データベース接続を確認する {#step-5-confirm-the-database-connection}

1.  TiDB Cloudコンソールでクラスターの接続ダイアログを閉じ、 **SQL エディター**ページを開きます。
2.  左側の**「スキーマ」**タブで、Wordpress に接続したデータベースをクリックします。
3.  そのデータベースのテーブルのリストに、Wordpress テーブル ( `wp_posts`や`wp_comments`など) が表示されていることを確認します。

## ヘルプが必要ですか? {#need-help}

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、あるいは[サポートチケットを送信する](https://tidb.support.pingcap.com/)についてコミュニティに質問してください。
