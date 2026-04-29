---
title: Connect to TiDB with Rails framework and ActiveRecord ORM
summary: Railsフレームワークを使用してTiDBに接続する方法を学びましょう。このチュートリアルでは、RailsフレームワークとActiveRecord ORMを使用してTiDBと連携するRubyのサンプルコードを紹介します。
aliases: ['/ja/tidb/stable/dev-guide-sample-application-ruby-rails/','/ja/tidb/dev/dev-guide-sample-application-ruby-rails/','/ja/tidbcloud/dev-guide-sample-application-ruby-rails/']
---

# RailsフレームワークとActiveRecord ORMを使用してTiDBに接続する {#connect-to-tidb-with-rails-framework-and-activerecord-orm}

TiDBはMySQL互換のデータベースであり、 [Rails](https://github.com/rails/rails) Rubyで書かれた人気のWebアプリケーションフレームワークであり、 [ActiveRecord ORM](https://github.com/rails/rails/tree/main/activerecord)はRailsにおけるオブジェクトリレーショナルマッピングです。

このチュートリアルでは、TiDBとRailsを使用して以下のタスクを実行する方法を学ぶことができます。

-   環境をセットアップしてください。
-   Railsを使用してTiDBに接続します。
-   アプリケーションをビルドして実行します。オプションで、ActiveRecord ORM を使用した基本的な CRUD 操作用の[サンプルコードスニペット](#sample-code-snippets)を見つけることができます。

> **注記：**
>
> このチュートリアルは、 TiDB Cloud Starter、 TiDB Cloud Essential、 TiDB Cloud Premium、 TiDB Cloud Dedicated、およびTiDB Self-Managedに対応しています。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、以下が必要です。

-   [ルビー](https://www.ruby-lang.org/en/)&gt;= 3.0 がマシンにインストールされている
-   あなたのマシンにインストールされている[バンドラー](https://bundler.io/)
-   お使いのマシンに[Git](https://git-scm.com/downloads)がインストールされています
-   TiDBクラスタが稼働中

**TiDBクラスタをお持ちでない場合は、以下の手順で作成できます。**

-   (推奨) [TiDB Cloud Starterインスタンスを作成する](/develop/dev-guide-build-cluster-in-cloud.md)。
-   [ローカルテスト用のTiDBセルフマネージドクラスタをデプロイ。](/quick-start-with-tidb.md#deploy-a-local-test-cluster)または[本番本番のTiDBセルフマネージドクラスタをデプロイ。](/production-deployment-using-tiup.md)

## TiDBに接続するには、サンプルアプリを実行してください。 {#run-the-sample-app-to-connect-to-tidb}

このセクションでは、サンプルアプリケーションコードを実行してTiDBに接続する方法を説明します。

### ステップ1：サンプルアプリのリポジトリをクローンする {#step-1-clone-the-sample-app-repository}

サンプルコードリポジトリをクローンするには、ターミナルウィンドウで以下のコマンドを実行してください。

```shell
git clone https://github.com/tidb-samples/tidb-ruby-rails-quickstart.git
cd tidb-ruby-rails-quickstart
```

### ステップ2：依存関係をインストールする {#step-2-install-dependencies}

サンプルアプリに必要なパッケージ（ `mysql2`および`dotenv`を含む）をインストールするには、次のコマンドを実行します。

```shell
bundle install
```

<details><summary><b>既存プロジェクトの依存関係をインストールする</b></summary>

既存のプロジェクトの場合、以下のコマンドを実行してパッケージをインストールしてください。

```shell
bundle add mysql2 dotenv
```

</details>

### ステップ3：接続情報の設定 {#step-3-configure-connection-information}

選択したTiDBのデプロイオプションに応じて、TiDBに接続してください。

<SimpleTab>
<div label="TiDB Cloud Starter or Essential">

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud StarterまたはEssentialインスタンスの名前をクリックして、概要ページに移動します。

2.  右上隅の**「接続」**をクリックしてください。接続ダイアログが表示されます。

3.  接続ダイアログで、[**接続先]**ドロップダウンリストから`Rails`を選択し、 **[接続タイプ]**のデフォルト設定を`Public`のままにします。

4.  まだパスワードを設定していない場合は、 **「パスワードを生成」**をクリックしてランダムなパスワードを生成してください。

5.  `.env.example`をコピーして`.env`に名前を変更するには、次のコマンドを実行します。

    ```shell
    cp .env.example .env
    ```

6.  `.env`ファイルを編集し、 `DATABASE_URL`環境変数を次のように設定し、接続ダイアログから接続文字列をコピーして変数の値として使用します。

    ```dotenv
    DATABASE_URL='mysql2://{user}:{password}@{host}:{port}/{database_name}?ssl_mode=verify_identity'
    ```

    > **注記**
    >
    > [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合、パブリックエンドポイントを使用する際には、 `ssl_mode=verify_identity`クエリパラメータを使用して TLS 接続を有効にする**必要があります**。

7.  `.env`ファイルを保存します。

</div>
<div label="TiDB Cloud Premium">

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud Premiumインスタンスの名前をクリックして概要ページに移動します。

2.  左側のナビゲーションペインで、 **[設定]** &gt; **[ネットワーク]**をクリックします。

3.  **ネットワークの**ページで、 **[パブリックエンドポイント****を有効にする]**をクリックし、次に**[IP アドレスの追加]**をクリックします。

    クライアントのIPアドレスがアクセスリストに追加されていることを確認してください。

4.  左側のナビゲーションペインで**「概要」**をクリックすると、インスタンスの概要ページに戻ります。

5.  右上隅の**「接続」**をクリックしてください。接続ダイアログが表示されます。

6.  接続ダイアログで、 **「接続タイプ」**ドロップダウンリストから**「パブリック」**を選択します。

    -   公開エンドポイントがまだ有効化中であることを示すメッセージが表示された場合は、処理が完了するまでお待ちください。
    -   まだパスワードを設定していない場合は、ダイアログの**「ルートパスワードを設定」**をクリックしてください。
    -   サーバー証明書を確認する必要がある場合、または接続に失敗して認証局（CA）証明書が必要な場合は、 **「CA証明書」**をクリックしてダウンロードしてください。
    -   **パブリック**接続タイプに加えて、 TiDB Cloud Premium は**プライベート エンドポイント**接続をサポートします。詳細については、 [AWS PrivateLink経由でTiDB Cloud Premiumに接続します。](/tidb-cloud/premium/connect-to-premium-via-aws-private-endpoint.md)を参照してください。

7.  `.env.example`をコピーして`.env`に名前を変更するには、次のコマンドを実行します。

    ```shell
    cp .env.example .env
    ```

8.  `.env`ファイルを編集し、 `DATABASE_URL`環境変数を以下のように設定し、接続ダイアログで対応するプレースホルダー`{}`接続パラメータに置き換えます。

    ```dotenv
    DATABASE_URL='mysql2://{user}:{password}@{host}:{port}/{database_name}'
    ```

9.  `.env`ファイルを保存します。

</div>
<div label="TiDB Cloud Dedicated">

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud Dedicatedクラスタの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックしてください。接続ダイアログが表示されます。

3.  接続ダイアログで、「**接続タイプ」**ドロップダウンリストから**「パブリック」**を選択し、 **「CA証明書」**をクリックしてCA証明書をダウンロードします。

    IP アクセス リストを設定していない場合は、最初の接続の前に、 **[IP アクセス リストの設定] をクリックするか、「IP アクセス リストを設定する」**の手順に従って[IPアクセスリストを設定する](https://docs.pingcap.com/tidbcloud/configure-ip-access-list)。

    TiDB Cloud Dedicated は、**パブリック**接続タイプに加えて、**プライベート エンドポイント**および**VPC ピアリング**接続タイプもサポートしています。詳細については、 [TiDB Cloud Dedicatedクラスタに接続します](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)参照してください。

4.  `.env.example`をコピーして`.env`に名前を変更するには、次のコマンドを実行します。

    ```shell
    cp .env.example .env
    ```

5.  `.env`ファイルを編集し、 `DATABASE_URL`環境変数を次のように設定し、接続ダイアログから接続文字列をコピーして変数の値として設定し、 `sslca`クエリパラメータを接続ダイアログからダウンロードした CA 証明書のファイルパスに設定します。

    ```dotenv
    DATABASE_URL='mysql2://{user}:{password}@{host}:{port}/{database}?ssl_mode=verify_identity&sslca=/path/to/ca.pem'
    ```

    > **注記**
    >
    > TiDB Cloud Dedicatedへの接続にパブリックエンドポイントを使用する場合は、TLS接続を有効にすることをお勧めします。
    >
    > TLS接続を有効にするには、 `ssl_mode`クエリパラメータの値を`verify_identity`に変更し、 `sslca`の値を接続ダイアログからダウンロードしたCA証明書のファイルパスに変更してください。

6.  `.env`ファイルを保存します。

</div>
<div label="TiDB Self-Managed" value="tidb">

1.  `.env.example`をコピーして`.env`に名前を変更するには、次のコマンドを実行します。

    ```shell
    cp .env.example .env
    ```

2.  `.env`ファイルを編集し、 `DATABASE_URL`環境変数を次のように設定し、 `{user}` 、 `{password}` 、 `{host}` 、 `{port}` 、および`{database}`独自の TiDB 接続情報に置き換えてください。

    ```dotenv
    DATABASE_URL='mysql2://{user}:{password}@{host}:{port}/{database}'
    ```

    TiDBをローカルで実行している場合、デフォルトのホストアドレスは`127.0.0.1`で、パスワードは空です。

3.  `.env`ファイルを保存します。

</div>
</SimpleTab>

### ステップ4：コードを実行して結果を確認する {#step-4-run-the-code-and-check-the-result}

1.  データベースとテーブルを作成します。

    ```shell
    bundle exec rails db:create
    bundle exec rails db:migrate
    ```

2.  サンプルデータにシード値を設定します。

    ```shell
    bundle exec rails db:seed
    ```

3.  サンプルコードを実行するには、以下のコマンドを実行してください。

    ```shell
    bundle exec rails runner ./quickstart.rb
    ```

接続が成功すると、コンソールには次のようにTiDBのバージョンが出力されます。

    🔌 Connected to TiDB cluster! (TiDB version: 8.0.11-TiDB-v8.5.4)
    ⏳ Loading sample game data...
    ✅ Loaded sample game data.

    🆕 Created a new player with ID 12.
    ℹ️ Got Player 12: Player { id: 12, coins: 100, goods: 100 }
    🔢 Added 50 coins and 50 goods to player 12, updated 1 row.
    🚮 Deleted 1 player data.

## サンプルコードスニペット {#sample-code-snippets}

以下のサンプルコードスニペットを参考に、独自のアプリケーション開発を完成させてください。

完全なサンプルコードと実行方法については、 [tidb-samples/tidb-ruby-rails-quickstart](https://github.com/tidb-samples/tidb-ruby-rails-quickstart)リポジトリを参照してください。

### 接続オプションを使用してTiDBに接続します {#connect-to-tidb-with-connection-options}

`config/database.yml`内の以下のコードは、環境変数で定義されたオプションを使用して TiDB への接続を確立します。

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
> [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合、パブリック エンドポイントを使用する際には**、** `ssl_mode`の`verify_identity`クエリ パラメータを`DATABASE_URL`に設定して TLS 接続を有効にする必要がありますが、mysql2 gem が特定の順序で既存の CA 証明書を検索してファイルが見つかるまで検索するため、 `DATABASE_URL`を介して SSL CA 証明書を指定する必要**はあり**ません。

### データを挿入する {#insert-data}

次のクエリは、2 つのフィールドを持つ単一の Player オブジェクトを作成し、作成された`Player`オブジェクトを返します。

```ruby
new_player = Player.create!(coins: 100, goods: 100)
```

詳細については、[データを挿入する](/develop/dev-guide-insert-data.md)を参照してください。

### クエリデータ {#query-data}

以下のクエリは、IDで指定された特定のプレイヤーのレコードを返します。

```ruby
player = Player.find_by(id: new_player.id)
```

詳細については、 [クエリデータ](/develop/dev-guide-get-data-from-single-table.md)を参照してください。

### データの更新 {#update-data}

次のクエリは`Player`オブジェクトを更新します。

```ruby
player.update(coins: 50, goods: 50)
```

詳細については、[データの更新](/develop/dev-guide-update-data.md)を参照してください。

### データを削除する {#delete-data}

次のクエリは`Player`オブジェクトを削除します。

```ruby
player.destroy
```

詳細については、[データを削除する](/develop/dev-guide-delete-data.md)を参照してください。

## ベストプラクティス {#best-practices}

デフォルトでは、mysql2 gem（ActiveRecord ORMがTiDBに接続するために使用）は、ファイルが見つかるまで特定の順序で既存のCA証明書を検索します。

1.  /etc/ssl/certs/ca-certificates.crt # Debian / Ubuntu / Gentoo / Arch / Slackware
2.  /etc/pki/tls/certs/ca-bundle.crt # RedHat / Fedora / CentOS / Mageia / Vercel / Netlify
3.  /etc/ssl/ca-bundle.pem # OpenSUSE
4.  /etc/ssl/cert.pem # MacOS / Alpine (Dockerコンテナ)

CA証明書のパスを手動で指定することも可能ですが、異なるマシンや環境によってCA証明書の保存場所が異なる場合があるため、複数の環境に展開するシナリオでは、この方法は大きな不便をもたらす可能性があります。そのため、 `sslca`を`nil`に設定することで、柔軟性と異なる環境への展開の容易性を確保できます。

## 次のステップ {#next-steps}

-   ActiveRecord ORM の使用法について詳しくは[ActiveRecordのドキュメント](https://guides.rubyonrails.org/active_record_basics.html)ご覧ください。
-   [開発者ガイド](https://docs.pingcap.com/developer/)[データを挿入する](/develop/dev-guide-insert-data.md)、[データの更新](/develop/dev-guide-update-data.md)[データを削除する](/develop/dev-guide-delete-data.md)SQL [取引](/develop/dev-guide-transaction-overview.md)[SQLパフォーマンス最適化](/develop/dev-guide-optimize-sql-overview.md)などの章を読ん[クエリデータ](/develop/dev-guide-get-data-from-single-table.md)、TiDB アプリケーション開発のベスト プラクティスを学びましょう。
-   プロフェッショナルな[TiDB開発者向けコース](https://www.pingcap.com/education/)コースを通じて学習し、試験に合格すると[TiDB認定資格](https://www.pingcap.com/education/certification/)を取得します。

## お困りですか？ {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)or [スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに質問してください。
-   [TiDB Cloudのサポートチケットを送信してください](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDB Self-Managedのサポートチケットを送信してください](/support.md)
