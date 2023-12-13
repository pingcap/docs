---
title: Connect to TiDB Serverless with WordPress
summary: Learn how to use TiDB Serverless to run WordPress. This tutorial gives step-by-step guidance to run WordPress + TiDB Serverless in a few minutes.
---

# WordPress を使用して TiDB サーバーレスに接続する {#connect-to-tidb-serverless-with-wordpress}

TiDB は MySQL 互換データベースであり、TiDB Serverless はフルマネージド TiDB 製品であり、 [ワードプレス](https://github.com/WordPress)はユーザーが Web サイトを作成および管理できる無料のオープンソース コンテンツ管理システム (CMS) です。 WordPress は PHP で書かれており、MySQL データベースを使用します。

このチュートリアルでは、TiDB Serverless を使用して WordPress を無料で実行する方法を学ぶことができます。

> **注記：**
>
> TiDB サーバーレスに加えて、このチュートリアルは TiDB 専用クラスターおよび TiDB セルフホストクラスターでも動作します。ただし、コスト効率を高めるために、TiDB サーバーレスで WordPress を実行することを強くお勧めします。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、次のものが必要です。

-   TiDB サーバーレス クラスター。独自のTiDB Cloudクラスターがない場合は、 [TiDB サーバーレスクラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って作成します。

## TiDB サーバーレスで WordPress を実行する {#run-wordpress-with-tidb-serverless}

このセクションでは、TiDB サーバーレスで WordPress を実行する方法を説明します。

### ステップ 1: WordPress サンプル リポジトリのクローンを作成する {#step-1-clone-the-wordpress-sample-repository}

ターミナル ウィンドウで次のコマンドを実行して、サンプル コード リポジトリのクローンを作成します。

```shell
git clone https://github.com/Icemap/wordpress-tidb-docker.git
cd wordpress-tidb-docker
```

### ステップ 2: 依存関係をインストールする {#step-2-install-dependencies}

1.  サンプル リポジトリでは、WordPress を起動するために[ドッカー](https://www.docker.com/)と[Docker Compose](https://docs.docker.com/compose/)が必要です。インストールされている場合は、この手順をスキップできます。 WordPress を Linux 環境 (Ubuntu など) で実行することを強くお勧めします。次のコマンドを実行してインストールします。

    ```shell
    sudo sh install.sh
    ```

2.  サンプル リポジトリには、サブモジュールとして[TiDB 互換性プラグイン](https://github.com/pingcap/wordpress-tidb-plugin)が含まれています。次のコマンドを実行してサブモジュールを更新します。

    ```shell
    git submodule update --init --recursive
    ```

### ステップ 3: 接続情報を構成する {#step-3-configure-connection-information}

TiDB サーバーレスへの WordPress データベース接続を構成します。

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして、その概要ページに移動します。

2.  右上隅にある**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログの設定が動作環境と一致していることを確認してください。

    -   **エンドポイント タイプは**`Public`に設定されます。
    -   **[接続先] は**`WordPress`に設定されます。
    -   **オペレーティング システムは**`Debian/Ubuntu/Arch`に設定されています。

4.  **「パスワードの生成」**をクリックして、ランダムなパスワードを作成します。

    > **ヒント：**
    >
    > 以前にパスワードを作成したことがある場合は、元のパスワードを使用するか、 **「パスワードのリセット」**をクリックして新しいパスワードを生成できます。

5.  次のコマンドを実行して`.env.example`をコピーし、名前を`.env`に変更します。

    ```shell
    cp .env.example .env
    ```

6.  対応する接続​​文字列をコピーして`.env`ファイルに貼り付けます。結果の例は次のとおりです。

    ```dotenv
    TIDB_HOST='{HOST}'  # e.g. gateway01.ap-northeast-1.prod.aws.tidbcloud.com
    TIDB_PORT='4000'
    TIDB_USER='{USERNAME}'  # e.g. xxxxxx.root
    TIDB_PASSWORD='{PASSWORD}'
    TIDB_DB_NAME='test'
    ```

    プレースホルダー`{}` 、接続ダイアログから取得した接続パラメーターに必ず置き換えてください。デフォルトでは、TiDB サーバーレスには`test`データベースが付属しています。 TiDB サーバーレス クラスターに別のデータベースをすでに作成している場合は、 `test`データベース名に置き換えることができます。

7.  `.env`ファイルを保存します。

### ステップ 4: TiDB サーバーレスで WordPress を開始する {#step-4-start-wordpress-with-tidb-serverless}

1.  次のコマンドを実行して、WordPress を Docker コンテナとして実行します。

    ```shell
    docker compose up -d
    ```

2.  ローカルマシンでコンテナを起動する場合は[ローカルホスト](http://localhost/)にアクセスし、WordPress がリモートマシンで実行されている場合は`http://<your_instance_ip>`アクセスして、WordPress サイトをセットアップします。

## 助けが必要？ {#need-help}

[不和](https://discord.gg/vYU9h56kAX)または[サポートチケットを作成する](/tidb-cloud/tidb-cloud-support.md)について質問してください。
