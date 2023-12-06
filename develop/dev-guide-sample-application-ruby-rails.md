---
title: Connect to TiDB with Rails framework and ActiveRecord ORM
summary: Learn how to connect to TiDB using the Rails framework. This tutorial gives Ruby sample code snippets that work with TiDB using the Rails framework and ActiveRecord ORM.
---

# Rails Framework と ActiveRecord ORM を使用して TiDB に接続する {#connect-to-tidb-with-rails-framework-and-activerecord-orm}

TiDB は MySQL 互換データベース、 [レール](https://github.com/rails/rails)は Ruby で書かれた一般的な Web アプリケーション フレームワーク、 [ActiveRecord ORM](https://github.com/rails/rails/tree/main/activerecord)は Rails のオブジェクト リレーショナル マッピングです。

このチュートリアルでは、TiDB と Rails を使用して次のタスクを実行する方法を学習できます。

-   環境をセットアップします。
-   Rails を使用して TiDB クラスターに接続します。
-   アプリケーションをビルドして実行します。オプションで、ActiveRecord ORM を使用した基本的な CRUD 操作の[サンプルコードスニペット](#sample-code-snippets)を見つけることができます。

> **注記：**
>
> このチュートリアルは、TiDB サーバーレス、TiDB 専用、および TiDB セルフホストで動作します。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、次のものが必要です。

-   [ルビー](https://www.ruby-lang.org/en/) &gt;= 3.0 がマシンにインストールされている
-   [バンドラー](https://bundler.io/)マシンにインストールされています
-   [ギット](https://git-scm.com/downloads)マシンにインストールされています
-   実行中の TiDB クラスター

**TiDB クラスターがない場合は、次のように作成できます。**

<CustomContent platform="tidb">

-   (推奨) [TiDB サーバーレスクラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って、独自のTiDB Cloudクラスターを作成します。
-   [ローカル テスト TiDB クラスターをデプロイ](/quick-start-with-tidb.md#deploy-a-local-test-cluster)または[本番TiDB クラスターをデプロイ](/production-deployment-using-tiup.md)に従ってローカル クラスターを作成します。

</CustomContent>
<CustomContent platform="tidb-cloud">

-   (推奨) [TiDB サーバーレスクラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って、独自のTiDB Cloudクラスターを作成します。
-   [ローカル テスト TiDB クラスターをデプロイ](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster)または[本番TiDB クラスターをデプロイ](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup)に従ってローカル クラスターを作成します。

</CustomContent>

## サンプル アプリを実行して TiDB に接続する {#run-the-sample-app-to-connect-to-tidb}

このセクションでは、サンプル アプリケーション コードを実行して TiDB に接続する方法を説明します。

### ステップ 1: サンプル アプリ リポジトリのクローンを作成する {#step-1-clone-the-sample-app-repository}

ターミナル ウィンドウで次のコマンドを実行して、サンプル コード リポジトリのクローンを作成します。

```shell
git clone https://github.com/tidb-samples/tidb-ruby-rails-quickstart.git
cd tidb-ruby-rails-quickstart
```

### ステップ 2: 依存関係をインストールする {#step-2-install-dependencies}

次のコマンドを実行して、サンプル アプリに必要なパッケージ ( `mysql2`と`dotenv`を含む) をインストールします。

```shell
bundle install
```

<details><summary><b>既存のプロジェクトの依存関係をインストールする</b></summary>

既存のプロジェクトの場合は、次のコマンドを実行してパッケージをインストールします。

```shell
bundle add mysql2 dotenv
```

</details>

### ステップ 3: 接続情報を構成する {#step-3-configure-connection-information}

選択した TiDB デプロイメント オプションに応じて、TiDB クラスターに接続します。

<SimpleTab>
<div label="TiDB Serverless">

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして、その概要ページに移動します。

2.  右上隅にある**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログで、 **[接続先]**ドロップダウン リストから`Rails`を選択し、**エンドポイント タイプ**のデフォルト設定を`Public`のままにします。

4.  パスワードをまだ設定していない場合は、 **「パスワードの生成」を**クリックしてランダムなパスワードを生成します。

5.  次のコマンドを実行して`.env.example`をコピーし、名前を`.env`に変更します。

    ```shell
    cp .env.example .env
    ```

6.  `.env`ファイルを編集し、 `DATABASE_URL`環境変数を次のように設定し、接続ダイアログから接続文字列を変数値としてコピーします。

    ```dotenv
    DATABASE_URL=mysql2://<user>:<password>@<host>:<port>/<database_name>?ssl_mode=verify_identity
    ```

    > **注記**
    >
    > TiDB サーバーレスの場合、パブリック エンドポイントを使用する場合は、TLS 接続を`ssl_mode=verify_identity`クエリ パラメーターで有効にする**必要があります**。

7.  `.env`ファイルを保存します。

</div>
<div label="TiDB Dedicated">

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして、その概要ページに移動します。

2.  右上隅にある**「接続」**をクリックします。接続ダイアログが表示されます。

3.  **「どこからでもアクセスを許可」**をクリックし、 **「TiDB クラスター CA のダウンロード」**をクリックして CA 証明書をダウンロードします。

    接続文字列の取得方法の詳細については、 [TiDB専用標準接続](https://docs.pingcap.com/tidbcloud/connect-via-standard-connection)を参照してください。

4.  次のコマンドを実行して`.env.example`をコピーし、名前を`.env`に変更します。

    ```shell
    cp .env.example .env
    ```

5.  `.env`ファイルを編集し、次のように`DATABASE_URL`環境変数を設定し、接続ダイアログから接続文字列を変数値としてコピーし、 `sslca`クエリ パラメータを接続ダイアログからダウンロードした CA 証明書のファイル パスに設定します。

    ```dotenv
    DATABASE_URL=mysql2://<user>:<password>@<host>:<port>/<database>?ssl_mode=verify_identity&sslca=/path/to/ca.pem
    ```

    > **注記**
    >
    > パブリック エンドポイントを使用して TiDB Dended に接続する場合は、TLS 接続を有効にすることをお勧めします。
    >
    > TLS 接続を有効にするには、 `ssl_mode`クエリ パラメータの値を`verify_identity`に変更し、 `sslca`の値を接続ダイアログからダウンロードした CA 証明書のファイル パスに変更します。

6.  `.env`ファイルを保存します。

</div>
<div label="TiDB Self-Hosted">

1.  次のコマンドを実行して`.env.example`をコピーし、名前を`.env`に変更します。

    ```shell
    cp .env.example .env
    ```

2.  `.env`ファイルを編集し、次のように`DATABASE_URL`環境変数を設定し、 `<user>` 、 `<password>` 、 `<host>` 、 `<port>` 、および`<database>`独自の TiDB 接続情報に置き換えます。

    ```dotenv
    DATABASE_URL=mysql2://<user>:<password>@<host>:<port>/<database>
    ```

    TiDB をローカルで実行している場合、デフォルトのホスト アドレスは`127.0.0.1`で、パスワードは空です。

3.  `.env`ファイルを保存します。

</div>
</SimpleTab>

### ステップ 4: コードを実行して結果を確認する {#step-4-run-the-code-and-check-the-result}

1.  データベースとテーブルを作成します。

    ```shell
    bundle exec rails db:create
    bundle exec rails db:migrate
    ```

2.  サンプル データをシードします。

    ```shell
    bundle exec rails db:seed
    ```

3.  次のコマンドを実行してサンプル コードを実行します。

    ```shell
    bundle exec rails runner ./quickstart.rb
    ```

接続が成功すると、コンソールには次のように TiDB クラスターのバージョンが出力されます。

    🔌 Connected to TiDB cluster! (TiDB version: 5.7.25-TiDB-v7.1.0)
    ⏳ Loading sample game data...
    ✅ Loaded sample game data.

    🆕 Created a new player with ID 12.
    ℹ️ Got Player 12: Player { id: 12, coins: 100, goods: 100 }
    🔢 Added 50 coins and 50 goods to player 12, updated 1 row.
    🚮 Deleted 1 player data.

## サンプルコードスニペット {#sample-code-snippets}

次のサンプル コード スニペットを参照して、独自のアプリケーション開発を完了できます。

完全なサンプル コードとその実行方法については、 [tidb-samples/tidb-ruby-rails-quickstart](https://github.com/tidb-samples/tidb-ruby-rails-quickstart)リポジトリを確認してください。

### 接続オプションを使用して TiDB に接続する {#connect-to-tidb-with-connection-options}

`config/database.yml`の次のコードは、環境変数で定義されたオプションを使用して TiDB への接続を確立します。

```yml
default: &default
  adapter: mysql2
  encoding: utf8mb4
  pool: <%= ENV.fetch("RAILS_MAX_THREADS") { 5 } %>
  url: <%= ENV["DATABASE_URL"] %>

development:
  <<: *default

test:
  <<: *default
  database: quickstart_test

production:
  <<: *default
```

> **注記**
>
> TiDB サーバーレスの場合、パブリック エンドポイントを使用するときに`ssl_mode`クエリ パラメーターを`verify_identity` in `DATABASE_URL`に設定することで TLS 接続を有効にする必要**が**ありますが、mysql2 gem は既存の CA 証明書を検索するため、 `DATABASE_URL`介して SSL CA 証明書を指定する必要は**ありません。**ファイルが検出されるまでの特定の順序。

### データの挿入 {#insert-data}

次のクエリは、2 つのフィールドを持つ単一のプレーヤーを作成し、作成された`Player`オブジェクトを返します。

```ruby
new_player = Player.create!(coins: 100, goods: 100)
```

詳細については、 [データの挿入](/develop/dev-guide-insert-data.md)を参照してください。

### クエリデータ {#query-data}

次のクエリは、ID によって特定のプレーヤーのレコードを返します。

```ruby
player = Player.find_by(id: new_player.id)
```

詳細については、 [クエリデータ](/develop/dev-guide-get-data-from-single-table.md)を参照してください。

### データを更新する {#update-data}

次のクエリは`Player`オブジェクトを更新します。

```ruby
player.update(coins: 50, goods: 50)
```

詳細については、 [データを更新する](/develop/dev-guide-update-data.md)を参照してください。

### データの削除 {#delete-data}

次のクエリは`Player`オブジェクトを削除します。

```ruby
player.destroy
```

詳細については、 [データの削除](/develop/dev-guide-delete-data.md)を参照してください。

## ベストプラクティス {#best-practices}

デフォルトでは、mysql2 gem (TiDB に接続するために ActiveRecord ORM によって使用される) は、ファイルが検出されるまで特定の順序で既存の CA 証明書を検索します。

1.  /etc/ssl/certs/ca-certificates.crt # Debian / Ubuntu / Gentoo / Arch / Slackware
2.  /etc/pki/tls/certs/ca-bundle.crt # RedHat / Fedora / CentOS / Mageia / Vercel / Netlify
3.  /etc/ssl/ca-bundle.pem # OpenSUSE
4.  /etc/ssl/cert.pem # MacOS / Alpine (Docker コンテナ)

CA 証明書のパスを手動で指定することは可能ですが、異なるマシンや環境では CA 証明書が異なる場所に保存される可能性があるため、この方法では複数環境の展開シナリオで大きな不便が生じる可能性があります。したがって、さまざまな環境間での導入の柔軟性と容易さを考慮して、 `sslca` ～ `nil`を設定することをお勧めします。

## 次のステップ {#next-steps}

-   ActiveRecord ORM の詳しい使い方を[ActiveRecord のドキュメント](https://guides.rubyonrails.org/active_record_basics.html)から学びましょう。
-   TiDB アプリケーション開発のベスト プラクティスについては、 [開発者ガイド](/develop/dev-guide-overview.md)の章 ( [データの挿入](/develop/dev-guide-insert-data.md) 、 [データを更新する](/develop/dev-guide-update-data.md) 、 [データの削除](/develop/dev-guide-delete-data.md) 、 [クエリデータ](/develop/dev-guide-get-data-from-single-table.md) 、 [取引](/develop/dev-guide-transaction-overview.md) 、 [SQLパフォーマンスの最適化](/develop/dev-guide-optimize-sql-overview.md)など) で学習してください。
-   プロフェッショナルとして[TiDB 開発者コース](https://www.pingcap.com/education/)を学び、試験合格後に[TiDB 認定](https://www.pingcap.com/education/certification/)獲得します。

## 助けが必要？ {#need-help}

質問は[不和](https://discord.gg/vYU9h56kAX)チャンネルでお願いします。
