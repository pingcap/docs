---
title: Connect to TiDB with Rails framework and ActiveRecord ORM
summary: Railsフレームワークを使用してTiDBに接続する方法を学びます。このチュートリアルでは、RailsフレームワークとActiveRecord ORMを使用してTiDBを操作するRubyサンプルコードスニペットを紹介します。
aliases: ['/tidb/stable/dev-guide-sample-application-ruby-rails/','/tidb/dev/dev-guide-sample-application-ruby-rails/','/tidbcloud/dev-guide-sample-application-ruby-rails/']
---

# RailsフレームワークとActiveRecord ORMを使用してTiDBに接続する {#connect-to-tidb-with-rails-framework-and-activerecord-orm}

TiDB は MySQL 互換のデータベース、 [レール](https://github.com/rails/rails)は Ruby で書かれた人気の Web アプリケーション フレームワーク、 [アクティブレコードORM](https://github.com/rails/rails/tree/main/activerecord)は Rails のオブジェクト リレーショナル マッピングです。

このチュートリアルでは、TiDB と Rails を使用して次のタスクを実行する方法を学習します。

-   環境を設定します。
-   Rails を使用して TiDB クラスターに接続します。
-   アプリケーションをビルドして実行します。オプションとして、ActiveRecord ORMを使用した基本的なCRUD操作については[サンプルコードスニペット](#sample-code-snippets)参照してください。

> **注記：**
>
> このチュートリアルは、 TiDB Cloud Starter、 TiDB Cloud Essential、 TiDB Cloud Dedicated、および TiDB Self-Managed で機能します。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、次のものが必要です。

-   [ルビー](https://www.ruby-lang.org/en/) &gt;= 3.0 がマシンにインストールされている
-   [バンドラー](https://bundler.io/)マシンにインストールされています
-   [ギット](https://git-scm.com/downloads)マシンにインストールされています
-   TiDBクラスタが稼働中

**TiDB クラスターがない場合は、次のように作成できます。**

-   (推奨) [TiDB Cloud Starter クラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って、独自のTiDB Cloudクラスターを作成します。
-   [ローカルテストTiDBクラスタをデプロイ](/quick-start-with-tidb.md#deploy-a-local-test-cluster)または[本番のTiDBクラスタをデプロイ](/production-deployment-using-tiup.md)に従ってローカル クラスターを作成します。

## サンプルアプリを実行してTiDBに接続する {#run-the-sample-app-to-connect-to-tidb}

このセクションでは、サンプル アプリケーション コードを実行して TiDB に接続する方法を説明します。

### ステップ1: サンプルアプリのリポジトリをクローンする {#step-1-clone-the-sample-app-repository}

ターミナル ウィンドウで次のコマンドを実行して、サンプル コード リポジトリのクローンを作成します。

```shell
git clone https://github.com/tidb-samples/tidb-ruby-rails-quickstart.git
cd tidb-ruby-rails-quickstart
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
<div label="TiDB Cloud Starter or Essential">

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログで、 **「接続先」**ドロップダウン リストから`Rails`選択し、**接続タイプ**のデフォルト設定を`Public`のままにします。

4.  まだパスワードを設定していない場合は、 **「パスワードの生成」をクリックしてランダムなパスワード**を生成します。

5.  次のコマンドを実行して`.env.example`コピーし、名前を`.env`に変更します。

    ```shell
    cp .env.example .env
    ```

6.  `.env`ファイルを編集し、 `DATABASE_URL`環境変数を次のように設定し、接続ダイアログから接続文字列を変数値としてコピーします。

    ```dotenv
    DATABASE_URL='mysql2://{user}:{password}@{host}:{port}/{database_name}?ssl_mode=verify_identity'
    ```

    > **注記**
    >
    > [TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合、パブリックエンドポイントを使用する場合は、 `ssl_mode=verify_identity`クエリパラメータを使用して TLS 接続を有効にする**必要があります**。

7.  `.env`ファイルを保存します。

</div>
<div label="TiDB Cloud Dedicated">

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログで、 **[接続タイプ]**ドロップダウン リストから**[パブリック]**を選択し、 **[CA 証明書]**をクリックして CA 証明書をダウンロードします。

    IP アクセス リストをまだ設定していない場合は、 **「IP アクセス リストの設定」を**クリックするか、手順[IPアクセスリストを設定する](https://docs.pingcap.com/tidbcloud/configure-ip-access-list)に従って、最初の接続の前に設定してください。

    TiDB Cloud Dedicatedは、**パブリック**接続タイプに加えて、**プライベートエンドポイント**と**VPCピアリング**接続タイプもサポートしています。詳細については、 [TiDB Cloud専用クラスタに接続する](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)ご覧ください。

4.  次のコマンドを実行して`.env.example`コピーし、名前を`.env`に変更します。

    ```shell
    cp .env.example .env
    ```

5.  `.env`ファイルを編集し、 `DATABASE_URL`環境変数を次のように設定し、接続ダイアログから接続文字列を変数値としてコピーし、 `sslca`クエリ パラメータを接続ダイアログからダウンロードした CA 証明書のファイル パスに設定します。

    ```dotenv
    DATABASE_URL='mysql2://{user}:{password}@{host}:{port}/{database}?ssl_mode=verify_identity&sslca=/path/to/ca.pem'
    ```

    > **注記**
    >
    > パブリック エンドポイントを使用してTiDB Cloud Dedicated に接続する場合は、TLS 接続を有効にすることをお勧めします。
    >
    > TLS 接続を有効にするには、クエリ パラメータ`ssl_mode`の値を`verify_identity`に変更し、値`sslca`を接続ダイアログからダウンロードした CA 証明書のファイル パスに変更します。

6.  `.env`ファイルを保存します。

</div>
<div label="TiDB Self-Managed" value="tidb">

1.  次のコマンドを実行して`.env.example`コピーし、名前を`.env`に変更します。

    ```shell
    cp .env.example .env
    ```

2.  `.env`ファイル`{host}`編集し、 `DATABASE_URL`環境変数を次のように設定し、 `{user}` 、および`{port}` `{password}`独自の TiDB 接続情報に置き換え`{database}` 。

    ```dotenv
    DATABASE_URL='mysql2://{user}:{password}@{host}:{port}/{database}'
    ```

    TiDB をローカルで実行している場合、デフォルトのホスト アドレスは`127.0.0.1`で、パスワードは空になります。

3.  `.env`ファイルを保存します。

</div>
</SimpleTab>

### ステップ4: コードを実行して結果を確認する {#step-4-run-the-code-and-check-the-result}

1.  データベースとテーブルを作成します。

    ```shell
    bundle exec rails db:create
    bundle exec rails db:migrate
    ```

2.  サンプルデータをシードします。

    ```shell
    bundle exec rails db:seed
    ```

3.  サンプル コードを実行するには、次のコマンドを実行します。

    ```shell
    bundle exec rails runner ./quickstart.rb
    ```

接続が成功すると、コンソールに次のように TiDB クラスターのバージョンが出力されます。

    🔌 Connected to TiDB cluster! (TiDB version: 8.0.11-TiDB-v8.5.5)
    ⏳ Loading sample game data...
    ✅ Loaded sample game data.

    🆕 Created a new player with ID 12.
    ℹ️ Got Player 12: Player { id: 12, coins: 100, goods: 100 }
    🔢 Added 50 coins and 50 goods to player 12, updated 1 row.
    🚮 Deleted 1 player data.

## サンプルコードスニペット {#sample-code-snippets}

次のサンプル コード スニペットを参照して、独自のアプリケーション開発を完了することができます。

完全なサンプル コードとその実行方法については、 [tidb-samples/tidb-ruby-rails-クイックスタート](https://github.com/tidb-samples/tidb-ruby-rails-quickstart)リポジトリを参照してください。

### 接続オプションを使用してTiDBに接続する {#connect-to-tidb-with-connection-options}

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
> [TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)と[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)については、パブリック エンドポイントを使用する場合、 `DATABASE_URL`の`ssl_mode`クエリ パラメータを`verify_identity`に設定して TLS 接続を有効にする**必要があります**が、mysql2 gem はファイルが見つかるまで特定の順序で既存の CA 証明書を検索するため、 `DATABASE_URL`で SSL CA 証明書を指定する必要は**ありません**。

### データを挿入する {#insert-data}

次のクエリは、2 つのフィールドを持つ単一の Player を作成し、作成された`Player`オブジェクトを返します。

```ruby
new_player = Player.create!(coins: 100, goods: 100)
```

詳細については[データを挿入する](/develop/dev-guide-insert-data.md)を参照してください。

### クエリデータ {#query-data}

次のクエリは、ID によって特定のプレーヤーのレコードを返します。

```ruby
player = Player.find_by(id: new_player.id)
```

詳細については[クエリデータ](/develop/dev-guide-get-data-from-single-table.md)を参照してください。

### データを更新する {#update-data}

次のクエリは`Player`オブジェクトを更新します。

```ruby
player.update(coins: 50, goods: 50)
```

詳細については[データを更新する](/develop/dev-guide-update-data.md)を参照してください。

### データを削除する {#delete-data}

次のクエリは`Player`オブジェクトを削除します。

```ruby
player.destroy
```

詳細については[データを削除する](/develop/dev-guide-delete-data.md)を参照してください。

## ベストプラクティス {#best-practices}

デフォルトでは、mysql2 gem (ActiveRecord ORM が TiDB に接続するために使用) は、ファイルが見つかるまで特定の順序で既存の CA 証明書を検索します。

1.  /etc/ssl/certs/ca-certificates.crt # Debian / Ubuntu / Gentoo / Arch / Slackware
2.  /etc/pki/tls/certs/ca-bundle.crt # RedHat / Fedora / CentOS / Mageia / Vercel / Netlify
3.  /etc/ssl/ca-bundle.pem # OpenSUSE
4.  /etc/ssl/cert.pem # MacOS / Alpine (docker コンテナ)

CA証明書のパスを手動で指定することも可能ですが、複数の環境への導入シナリオでは、異なるマシンや環境によってCA証明書の保存場所が異なる場合があり、大きな不便が生じる可能性があります。そのため、柔軟性と容易さの観点から、異なる環境への導入を容易にするために、 `sslca` ～ `nil`設定をお勧めします。

## 次のステップ {#next-steps}

-   ActiveRecord ORM の使い方を[ActiveRecordのドキュメント](https://guides.rubyonrails.org/active_record_basics.html)から詳しく学びます。
-   [開発者ガイド](https://docs.pingcap.com/developer/)の[データを挿入する](/develop/dev-guide-insert-data.md) 、 [データを更新する](/develop/dev-guide-update-data.md) 、 [データを削除する](/develop/dev-guide-delete-data.md) 、 [クエリデータ](/develop/dev-guide-get-data-from-single-table.md) 、 [取引](/develop/dev-guide-transaction-overview.md) 、 [SQLパフォーマンスの最適化](/develop/dev-guide-optimize-sql-overview.md)などの章で、 TiDB アプリケーション開発のベスト プラクティスを学習します。
-   プロフェッショナル[TiDB開発者コース](https://www.pingcap.com/education/)を通じて学習し、試験に合格すると[TiDB認定](https://www.pingcap.com/education/certification/)獲得します。

## ヘルプが必要ですか? {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに問い合わせてください。
-   [TiDB Cloudのサポートチケットを送信する](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDBセルフマネージドのサポートチケットを送信する](/support.md)
