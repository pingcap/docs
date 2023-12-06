---
title: Connect to TiDB with mysql2
summary: Learn how to connect to TiDB using Ruby mysql2. This tutorial gives Ruby sample code snippets that work with TiDB using mysql2 gem.
---

# mysql2 を使用して TiDB に接続する {#connect-to-tidb-with-mysql2}

TiDB は MySQL 互換データベースであり、Ruby 用の最も人気のある MySQL ドライバーの[mysql2](https://github.com/brianmario/mysql2)つです。

このチュートリアルでは、TiDB と mysql2 を使用して次のタスクを実行する方法を学習できます。

-   環境をセットアップします。
-   mysql2 を使用して TiDB クラスターに接続します。
-   アプリケーションをビルドして実行します。オプションで、基本的な CRUD 操作の[サンプルコードスニペット](#sample-code-snippets)を見つけることができます。

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
git clone https://github.com/tidb-samples/tidb-ruby-mysql2-quickstart.git
cd tidb-ruby-mysql2-quickstart
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

3.  接続ダイアログの設定が動作環境と一致していることを確認してください。

    -   **エンドポイント タイプは**`Public`に設定されます。
    -   **ブランチは**`main`に設定されます。
    -   **[接続先] は**`General`に設定されます。
    -   **[オペレーティング システム] は、**アプリケーションを実行するオペレーティング システムと一致します。

4.  パスワードをまだ設定していない場合は、 **「パスワードの生成」を**クリックしてランダムなパスワードを生成します。

5.  次のコマンドを実行して`.env.example`をコピーし、名前を`.env`に変更します。

    ```shell
    cp .env.example .env
    ```

6.  `.env`ファイルを編集し、次のように環境変数を設定し、接続ダイアログ内の対応するプレースホルダー`<>`接続パラメーターに置き換えます。

    ```dotenv
    DATABASE_HOST=<host>
    DATABASE_PORT=4000
    DATABASE_USER=<user>
    DATABASE_PASSWORD=<password>
    DATABASE_NAME=test
    DATABASE_ENABLE_SSL=true
    ```

    > **注記**
    >
    > TiDB サーバーレスの場合、パブリック エンドポイントを使用する場合は、TLS 接続を`DATABASE_ENABLE_SSL`経由で有効にする**必要があります**。

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

5.  `.env`ファイルを編集し、次のように環境変数を設定し、接続ダイアログ内の対応するプレースホルダー`<>`接続パラメーターに置き換えます。

    ```dotenv
    DATABASE_HOST=<host>
    DATABASE_PORT=4000
    DATABASE_USER=<user>
    DATABASE_PASSWORD=<password>
    DATABASE_NAME=test
    DATABASE_ENABLE_SSL=true
    DATABASE_SSL_CA=<downloaded_ssl_ca_path>
    ```

    > **注記**
    >
    > パブリック エンドポイントを使用して TiDB 専用クラスターに接続する場合は、TLS 接続を有効にすることをお勧めします。
    >
    > TLS 接続を有効にするには、 `DATABASE_ENABLE_SSL`を`true`に変更し、 `DATABASE_SSL_CA`使用して接続ダイアログからダウンロードした CA 証明書のファイル パスを指定します。

6.  `.env`ファイルを保存します。

</div>
<div label="TiDB Self-Hosted">

1.  次のコマンドを実行して`.env.example`をコピーし、名前を`.env`に変更します。

    ```shell
    cp .env.example .env
    ```

2.  `.env`ファイルを編集し、次のように環境変数を設定し、対応するプレースホルダー`<>`独自の TiDB 接続情報に置き換えます。

    ```dotenv
    DATABASE_HOST=<host>
    DATABASE_PORT=4000
    DATABASE_USER=<user>
    DATABASE_PASSWORD=<password>
    DATABASE_NAME=test
    ```

    TiDB をローカルで実行している場合、デフォルトのホスト アドレスは`127.0.0.1`で、パスワードは空です。

3.  `.env`ファイルを保存します。

</div>
</SimpleTab>

### ステップ 4: コードを実行して結果を確認する {#step-4-run-the-code-and-check-the-result}

次のコマンドを実行してサンプル コードを実行します。

```shell
ruby app.rb
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

完全なサンプル コードとその実行方法については、 [tidb-samples/tidb-ruby-mysql2-quickstart](https://github.com/tidb-samples/tidb-ruby-mysql2-quickstart)リポジトリを確認してください。

### 接続オプションを使用して TiDB に接続する {#connect-to-tidb-with-connection-options}

次のコードは、環境変数で定義されたオプションを使用して TiDB への接続を確立します。

```ruby
require 'dotenv/load'
require 'mysql2'
Dotenv.load # Load the environment variables from the .env file

options = {
  host: ENV['DATABASE_HOST'] || '127.0.0.1',
  port: ENV['DATABASE_PORT'] || 4000,
  username: ENV['DATABASE_USER'] || 'root',
  password: ENV['DATABASE_PASSWORD'] || '',
  database: ENV['DATABASE_NAME'] || 'test'
}
options.merge(ssl_mode: :verify_identity) unless ENV['DATABASE_ENABLE_SSL'] == 'false'
options.merge(sslca: ENV['DATABASE_SSL_CA']) if ENV['DATABASE_SSL_CA']
client = Mysql2::Client.new(options)
```

> **注記**
>
> TiDB サーバーレスの場合、パブリック エンドポイントを使用する場合は`DATABASE_ENABLE_SSL`で TLS 接続を有効にする必要が**あります**が、mysql2 gem はファイルが検出されるまで特定の順序で既存の CA 証明書を検索するため、 `DATABASE_SSL_CA`で SSL CA 証明書を指定する必要は**ありません**。

### データの挿入 {#insert-data}

次のクエリは、2 つのフィールドを持つ単一のプレーヤーを作成し、 `last_insert_id`を返します。

```ruby
def create_player(client, coins, goods)
  result = client.query(
    "INSERT INTO players (coins, goods) VALUES (#{coins}, #{goods});"
  )
  client.last_id
end
```

詳細については、 [データの挿入](/develop/dev-guide-insert-data.md)を参照してください。

### クエリデータ {#query-data}

次のクエリは、ID によって特定のプレーヤーのレコードを返します。

```ruby
def get_player_by_id(client, id)
  result = client.query(
    "SELECT id, coins, goods FROM players WHERE id = #{id};"
  )
  result.first
end
```

詳細については、 [クエリデータ](/develop/dev-guide-get-data-from-single-table.md)を参照してください。

### データを更新する {#update-data}

次のクエリは、ID によって特定のプレーヤーのレコードを更新しました。

```ruby
def update_player(client, player_id, inc_coins, inc_goods)
  result = client.query(
    "UPDATE players SET coins = coins + #{inc_coins}, goods = goods + #{inc_goods} WHERE id = #{player_id};"
  )
  client.affected_rows
end
```

詳細については、 [データを更新する](/develop/dev-guide-update-data.md)を参照してください。

### データの削除 {#delete-data}

次のクエリは、特定のプレーヤーのレコードを削除します。

```ruby
def delete_player_by_id(client, id)
  result = client.query(
    "DELETE FROM players WHERE id = #{id};"
  )
  client.affected_rows
end
```

詳細については、 [データの削除](/develop/dev-guide-delete-data.md)を参照してください。

## ベストプラクティス {#best-practices}

デフォルトでは、mysql2 gem は、ファイルが検出されるまで、特定の順序で既存の CA 証明書を検索できます。

1.  Debian、Ubuntu、Gentoo、Arch、または Slackware の場合は`/etc/ssl/certs/ca-certificates.crt`
2.  RedHat、Fedora、CentOS、Mageia、Vercel、または Netlify の場合は`/etc/pki/tls/certs/ca-bundle.crt`
3.  OpenSUSE の場合は`/etc/ssl/ca-bundle.pem`
4.  macOS または Alpine (Docker コンテナー) の場合は`/etc/ssl/cert.pem`

CA 証明書のパスを手動で指定することは可能ですが、マシンや環境が異なれば CA 証明書が異なる場所に保存される可能性があるため、複数環境の展開シナリオでは重大な不便が生じる可能性があります。したがって、さまざまな環境間での導入の柔軟性と容易さを考慮して、 `sslca` ～ `nil`を設定することをお勧めします。

## 次のステップ {#next-steps}

-   mysql2 ドライバーの使用法については[mysql2のドキュメント](https://github.com/brianmario/mysql2#readme)からご覧ください。
-   TiDB アプリケーション開発のベスト プラクティスについては、 [開発者ガイド](/develop/dev-guide-overview.md)の章 ( [データの挿入](/develop/dev-guide-insert-data.md) 、 [データを更新する](/develop/dev-guide-update-data.md) 、 [データの削除](/develop/dev-guide-delete-data.md) 、 [クエリデータ](/develop/dev-guide-get-data-from-single-table.md) 、 [取引](/develop/dev-guide-transaction-overview.md) 、 [SQLパフォーマンスの最適化](/develop/dev-guide-optimize-sql-overview.md)など) で学習してください。
-   プロフェッショナルとして[TiDB 開発者コース](https://www.pingcap.com/education/)を学び、試験合格後に[TiDB 認定](https://www.pingcap.com/education/certification/)獲得します。

## 助けが必要？ {#need-help}

質問は[不和](https://discord.gg/vYU9h56kAX)チャンネルでお願いします。
