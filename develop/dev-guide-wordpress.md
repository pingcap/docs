---
title: Integrate WordPress with {{{ .starter }}}
summary: "{{{ .starter }}}を使ってWordPressを実行する方法を学びましょう。このチュートリアルでは、WordPressと{{{ .starter }}}を数分で実行するための手順をステップバイステップで解説します。"
aliases: ['/ja/tidbcloud/dev-guide-wordpress/']
---

# WordPressと{{{ .starter }}}を統合する {#integrate-wordpress-with-tidb-cloud-starter}

TiDBはMySQL互換データベースであり、 {{{ .starter }}}はフルマネージド型のTiDBサービスです。[WordPress](https://github.com/WordPress)は、ユーザーがウェブサイトを作成・管理できる無料のオープンソースコンテンツ管理システム（CMS）です。WordPressはPHPで記述されており、MySQLデータベースを使用しています。

このチュートリアルでは、 {{{ .starter }}}を使用してWordPressを無料で実行する方法を学べます。

> **Note:**
>
> このチュートリアルは、 {{{ .starter }}}に加えて、 {{{ .essential }}}、 TiDB Cloud Dedicated、および TiDB Self-Managed でも動作します。ただし、コスト効率を考慮すると、WordPress は{{{ .starter }}}で実行することを強くお勧めします。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、以下が必要です。

- お持ちでない場合は、 [{{{ .starter }}}インスタンスを作成する](/develop/dev-guide-build-cluster-in-cloud.md)。

## {{{ .starter }}}でWordPressを実行する {#run-wordpress-with-tidb-cloud-starter}

このセクションでは、{{{ .starter }}}を使用して WordPress を実行する方法を説明します。

### ステップ1：WordPressサンプルリポジトリをクローンする {#step-1-clone-the-wordpress-sample-repository}

サンプルコードリポジトリをクローンするには、ターミナルウィンドウで以下のコマンドを実行してください。

```shell
git clone https://github.com/Icemap/wordpress-tidb-docker.git
cd wordpress-tidb-docker
```

### ステップ2：依存関係をインストールする {#step-2-install-dependencies}

1. サンプルリポジトリでは、WordPressを起動するために[Docker](https://www.docker.com/)と[Docker Compose](https://docs.docker.com/compose/)が必要です。既にインストール済みであれば、この手順はスキップできます。WordPressはLinux環境（Ubuntuなど）で実行することを強くお勧めします。DockerとDocker Composeをインストールするには、次のコマンドを実行してください。

    ```shell
    sudo sh install.sh
    ```

2. サンプルリポジトリには、サブモジュールとして[TiDB互換性プラグイン](https://github.com/pingcap/wordpress-tidb-plugin)が含まれています。次のコマンドを実行してサブモジュールを更新します。

    ```shell
    git submodule update --init --recursive
    ```

### ステップ3：接続情報の設定 {#step-3-configure-connection-information}

{{{ .starter }}}へのWordPressデータベース接続を設定します。

1. [**My TiDB**](https://tidbcloud.com/tidbs)ページに移動し、次に、対象の{{{ .starter }}}インスタンスの名前をクリックして、概要ページに移動します。

2. 右上隅の**Connect**をクリックしてください。接続ダイアログが表示されます。

3. 接続ダイアログの設定がご使用のオペレーティング環境と一致していることを確認してください。

    - **Connection Type**は`Public`に設定されています。
    - **Connect With**は`WordPress`に設定されています。
    - **Operating System**は`Debian/Ubuntu/Arch`に設定されています。
    - **Database**は、使用したいデータベースに設定されます。たとえば、 `test` 。

4. **Generate Password**をクリックすると、ランダムなパスワードが生成されます。

    > **Tip:**
    >
    > 以前にパスワードを作成したことがある場合は、元のパスワードを使用するか、 **Reset Password**をクリックして新しいパスワードを生成できます。

5. `.env.example`をコピーして`.env`に名前を変更するには、次のコマンドを実行します。

    ```shell
    cp .env.example .env
    ```

6. 対応する接続文字列を`.env`ファイルにコピー＆ペーストしてください。例は以下のとおりです。

    ```dotenv
    TIDB_HOST='{HOST}'  # e.g. gateway01.ap-northeast-1.prod.aws.tidbcloud.com
    TIDB_PORT='4000'
    TIDB_USER='{USERNAME}'  # e.g. xxxxxx.root
    TIDB_PASSWORD='{PASSWORD}'
    TIDB_DB_NAME='test'
    ```

    プレースホルダー`{}`を、接続ダイアログから取得した接続パラメーターに置き換えてください。デフォルトでは、 {{{ .starter }}}には`test`データベースが付属しています。{{{ .starter }}}インスタンスで既に別のデータベースを作成している場合は、 `test`をデータベース名に置き換えてください。

7. `.env`ファイルを保存します。

### ステップ4： {{{ .starter }}}でWordPressを起動する {#step-4-start-wordpress-with-tidb-cloud-starter}

1. WordPressをDockerコンテナーとして実行するには、以下のコマンドを実行してください。

    ```shell
    docker compose up -d
    ```

2. ローカルマシンでコンテナーを起動した場合は[localhost](http://localhost/)にアクセスしてWordPressサイトをセットアップし、リモートマシンでWordPressが実行されている場合は`http://<your_instance_ip>`にアクセスしてください。

### ステップ5：データベース接続を確認する {#step-5-confirm-the-database-connection}

1. TiDB Cloudコンソールで{{{ .starter }}}インスタンスの接続ダイアログを閉じ、 **SQL Editor**ページを開きます。
2. 左側の**Schemas**タブで、WordPressに接続したデータベースをクリックします。
3. そのデータベースのテーブル一覧に、WordPressのテーブル（ `wp_posts`や`wp_comments`など）が表示されていることを確認してください。

## お困りですか？ {#need-help}

[Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs)コミュニティに質問するか、[サポートチケットを送信してください](https://tidb.support.pingcap.com/)。
