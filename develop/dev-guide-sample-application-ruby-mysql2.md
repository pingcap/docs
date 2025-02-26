---
title: Connect to TiDB with mysql2
summary: Ruby mysql2 を使用して TiDB に接続する方法を学びます。このチュートリアルでは、mysql2 gem を使用して TiDB で動作する Ruby サンプル コード スニペットを紹介します。
---

# mysql2でTiDBに接続する {#connect-to-tidb-with-mysql2}

TiDB は MySQL 互換のデータベースであり、Ruby 用の最も人気のある MySQL ドライバーの[マイSQL2](https://github.com/brianmario/mysql2)です。

このチュートリアルでは、TiDB と mysql2 を使用して次のタスクを実行する方法を学習します。

-   環境を設定します。
-   mysql2 を使用して TiDB クラスターに接続します。
-   アプリケーションをビルドして実行します。オプションで、基本的な CRUD 操作用の[サンプルコードスニペット](#sample-code-snippets)見つけることができます。

> **注記：**
>
> このチュートリアルは、 TiDB Cloud Serverless、 TiDB Cloud Dedicated、および TiDB Self-Managed で機能します。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、次のものが必要です。

-   [ルビー](https://www.ruby-lang.org/en/) &gt;= 3.0 がマシンにインストールされている
-   [バンドラー](https://bundler.io/)マシンにインストールされています
-   [ギット](https://git-scm.com/downloads)マシンにインストールされています
-   TiDBクラスタが稼働中

**TiDB クラスターがない場合は、次のように作成できます。**

<CustomContent platform="tidb">

-   (推奨) [TiDB Cloud Serverless クラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って、独自のTiDB Cloudクラスターを作成します。
-   [ローカルテストTiDBクラスタをデプロイ](/quick-start-with-tidb.md#deploy-a-local-test-cluster)または[本番のTiDBクラスタをデプロイ](/production-deployment-using-tiup.md)に従ってローカル クラスターを作成します。

</CustomContent>
<CustomContent platform="tidb-cloud">

-   (推奨) [TiDB Cloud Serverless クラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って、独自のTiDB Cloudクラスターを作成します。
-   [ローカルテストTiDBクラスタをデプロイ](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster)または[本番のTiDBクラスタをデプロイ](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup)に従ってローカル クラスターを作成します。

</CustomContent>

## サンプルアプリを実行してTiDBに接続する {#run-the-sample-app-to-connect-to-tidb}

このセクションでは、サンプル アプリケーション コードを実行して TiDB に接続する方法を示します。

### ステップ1: サンプルアプリのリポジトリをクローンする {#step-1-clone-the-sample-app-repository}

サンプル コード リポジトリを複製するには、ターミナル ウィンドウで次のコマンドを実行します。

```shell
git clone https://github.com/tidb-samples/tidb-ruby-mysql2-quickstart.git
cd tidb-ruby-mysql2-quickstart
```

### ステップ2: 依存関係をインストールする {#step-2-install-dependencies}

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

### ステップ3: 接続情報を構成する {#step-3-configure-connection-information}

選択した TiDB デプロイメント オプションに応じて、TiDB クラスターに接続します。

<SimpleTab>
<div label="TiDB Cloud Serverless">

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログの構成が動作環境と一致していることを確認します。

    -   **接続タイプ**は`Public`に設定されています。
    -   **ブランチ**は`main`に設定されています。
    -   **Connect With は**`General`に設定されています。
    -   **オペレーティング システムは、**アプリケーションを実行するオペレーティング システムと一致します。

4.  まだパスワードを設定していない場合は、 **「パスワードの生成」**をクリックしてランダムなパスワードを生成します。

5.  次のコマンドを実行して`.env.example`コピーし、名前を`.env`に変更します。

    ```shell
    cp .env.example .env
    ```

6.  `.env`ファイルを編集し、環境変数を次のように設定し、接続ダイアログで対応するプレースホルダー`{}`接続パラメータに置き換えます。

    ```dotenv
    DATABASE_HOST={host}
    DATABASE_PORT=4000
    DATABASE_USER={user}
    DATABASE_PASSWORD={password}
    DATABASE_NAME=test
    DATABASE_ENABLE_SSL=true
    ```

    > **注記**
    >
    > TiDB Cloud Serverless の場合、パブリック エンドポイントを使用する場合は、 `DATABASE_ENABLE_SSL`経由で TLS 接続を有効にする**必要があります**。

7.  `.env`ファイルを保存します。

</div>
<div label="TiDB Cloud Dedicated">

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログで、 **[接続タイプ]**ドロップダウン リストから**[パブリック]**を選択し、 **[CA 証明書]**をクリックして CA 証明書をダウンロードします。

    IP アクセス リストを設定していない場合は、 **「IP アクセス リストの設定」を**クリックするか、手順[IPアクセスリストを構成する](https://docs.pingcap.com/tidbcloud/configure-ip-access-list)に従って最初の接続の前に設定してください。

    TiDB Cloud Dedicated は、**パブリック**接続タイプに加えて、**プライベートエンドポイント**と**VPC ピアリング**接続タイプもサポートしています。詳細については、 [TiDB Cloud専用クラスタに接続する](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)参照してください。

4.  次のコマンドを実行して`.env.example`コピーし、名前を`.env`に変更します。

    ```shell
    cp .env.example .env
    ```

5.  `.env`ファイルを編集し、環境変数を次のように設定し、接続ダイアログで対応するプレースホルダー`{}`接続パラメータに置き換えます。

    ```dotenv
    DATABASE_HOST={host}
    DATABASE_PORT=4000
    DATABASE_USER={user}
    DATABASE_PASSWORD={password}
    DATABASE_NAME=test
    DATABASE_ENABLE_SSL=true
    DATABASE_SSL_CA={downloaded_ssl_ca_path}
    ```

    > **注記**
    >
    > パブリック エンドポイントを使用してTiDB Cloud Dedicated クラスターに接続する場合は、TLS 接続を有効にすることをお勧めします。
    >
    > TLS 接続を有効にするには、 `DATABASE_ENABLE_SSL`から`true`変更し、 `DATABASE_SSL_CA`使用して接続ダイアログからダウンロードした CA 証明書のファイル パスを指定します。

6.  `.env`ファイルを保存します。

</div>
<div label="TiDB Self-Managed">

1.  次のコマンドを実行して`.env.example`コピーし、名前を`.env`に変更します。

    ```shell
    cp .env.example .env
    ```

2.  `.env`ファイルを編集し、環境変数を次のように設定し、対応するプレースホルダー`{}`独自の TiDB 接続情報に置き換えます。

    ```dotenv
    DATABASE_HOST={host}
    DATABASE_PORT=4000
    DATABASE_USER={user}
    DATABASE_PASSWORD={password}
    DATABASE_NAME=test
    ```

    TiDB をローカルで実行している場合、デフォルトのホスト アドレスは`127.0.0.1`で、パスワードは空です。

3.  `.env`ファイルを保存します。

</div>
</SimpleTab>

### ステップ4: コードを実行して結果を確認する {#step-4-run-the-code-and-check-the-result}

サンプル コードを実行するには、次のコマンドを実行します。

```shell
ruby app.rb
```

接続が成功すると、コンソールに次のように TiDB クラスターのバージョンが出力されます。

    🔌 Connected to TiDB cluster! (TiDB version: 8.0.11-TiDB-v8.1.2)
    ⏳ Loading sample game data...
    ✅ Loaded sample game data.

    🆕 Created a new player with ID 12.
    ℹ️ Got Player 12: Player { id: 12, coins: 100, goods: 100 }
    🔢 Added 50 coins and 50 goods to player 12, updated 1 row.
    🚮 Deleted 1 player data.

## サンプルコードスニペット {#sample-code-snippets}

次のサンプル コード スニペットを参照して、独自のアプリケーション開発を完了することができます。

完全なサンプル コードとその実行方法については、 [tidb-samples/tidb-ruby-mysql2-クイックスタート](https://github.com/tidb-samples/tidb-ruby-mysql2-quickstart)リポジトリを参照してください。

### 接続オプションを使用してTiDBに接続する {#connect-to-tidb-with-connection-options}

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
> TiDB Cloud Serverless の場合、パブリック エンドポイントを使用するときは`DATABASE_ENABLE_SSL`で TLS 接続を有効にする**必要があります**が、mysql2 gem はファイルが見つかるまで特定の順序で既存の CA 証明書を検索するため、 `DATABASE_SSL_CA`で SSL CA 証明書を指定する必要は**ありません**。

### データを挿入 {#insert-data}

次のクエリは、 2 つのフィールドを持つ単一のプレーヤーを作成し、 `last_insert_id`返します。

```ruby
def create_player(client, coins, goods)
  result = client.query(
    "INSERT INTO players (coins, goods) VALUES (#{coins}, #{goods});"
  )
  client.last_id
end
```

詳細については[データを挿入](/develop/dev-guide-insert-data.md)を参照してください。

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

詳細については[クエリデータ](/develop/dev-guide-get-data-from-single-table.md)を参照してください。

### データの更新 {#update-data}

次のクエリは、ID によって特定のプレーヤーのレコードを更新しました。

```ruby
def update_player(client, player_id, inc_coins, inc_goods)
  result = client.query(
    "UPDATE players SET coins = coins + #{inc_coins}, goods = goods + #{inc_goods} WHERE id = #{player_id};"
  )
  client.affected_rows
end
```

詳細については[データの更新](/develop/dev-guide-update-data.md)を参照してください。

### データを削除する {#delete-data}

次のクエリは、特定のプレーヤーのレコードを削除します。

```ruby
def delete_player_by_id(client, id)
  result = client.query(
    "DELETE FROM players WHERE id = #{id};"
  )
  client.affected_rows
end
```

詳細については[データを削除する](/develop/dev-guide-delete-data.md)を参照してください。

## ベストプラクティス {#best-practices}

デフォルトでは、mysql2 gem は、ファイルが見つかるまで特定の順序で既存の CA 証明書を検索できます。

1.  Debian、Ubuntu、Gentoo、Arch、または Slackware の場合は`/etc/ssl/certs/ca-certificates.crt`
2.  RedHat、Fedora、CentOS、Mageia、Vercel、または Netlify の場合は`/etc/pki/tls/certs/ca-bundle.crt`
3.  OpenSUSEの場合は`/etc/ssl/ca-bundle.pem`
4.  macOS または Alpine (docker コンテナ) の場合は`/etc/ssl/cert.pem`

CA 証明書のパスを手動で指定することも可能ですが、異なるマシンや環境では CA 証明書が異なる場所に保存される可能性があるため、複数の環境を展開するシナリオでは大きな不便が生じる可能性があります。したがって、異なる環境間での展開の柔軟性と容易さのために、 `sslca`から`nil`設定することをお勧めします。

## 次のステップ {#next-steps}

-   [mysql2のドキュメント](https://github.com/brianmario/mysql2#readme)からの mysql2 ドライバーの使用法について詳しく学びます。
-   [開発者ガイド](/develop/dev-guide-overview.md)の[データを挿入](/develop/dev-guide-insert-data.md) 、 [データの更新](/develop/dev-guide-update-data.md) 、 [データを削除する](/develop/dev-guide-delete-data.md) 、 [クエリデータ](/develop/dev-guide-get-data-from-single-table.md) 、 [取引](/develop/dev-guide-transaction-overview.md) 、 [SQLパフォーマンスの最適化](/develop/dev-guide-optimize-sql-overview.md)などの章で、 TiDB アプリケーション開発のベスト プラクティスを学習します。
-   プロフェッショナル[TiDB 開発者コース](https://www.pingcap.com/education/)を通じて学び、試験に合格すると[TiDB 認定](https://www.pingcap.com/education/certification/)獲得します。

## ヘルプが必要ですか? {#need-help}

<CustomContent platform="tidb">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、または[サポートチケットを送信する](/support.md)についてコミュニティに質問してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、または[サポートチケットを送信する](https://tidb.support.pingcap.com/)についてコミュニティに質問してください。

</CustomContent>
