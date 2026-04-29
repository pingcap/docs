---
title: Connect to TiDB with mysql2
summary: Rubyのmysql2を使ってTiDBに接続する方法を学びましょう。このチュートリアルでは、mysql2 gemを使用してTiDBと連携するRubyのサンプルコードを紹介します。
aliases: ['/ja/tidb/stable/dev-guide-sample-application-ruby-mysql2/','/ja/tidb/dev/dev-guide-sample-application-ruby-mysql2/','/ja/tidbcloud/dev-guide-sample-application-ruby-mysql2/']
---

# mysql2を使用してTiDBに接続します。 {#connect-to-tidb-with-mysql2}

TiDBはMySQL互換のデータベースであり、 [mysql2](https://github.com/brianmario/mysql2)はRubyで最も人気のあるMySQLドライバの1つです。

このチュートリアルでは、TiDBとmysql2を使用して以下のタスクを実行する方法を学ぶことができます。

-   環境をセットアップしてください。
-   mysql2を使用してTiDBに接続します。
-   アプリケーションをビルドして実行します。オプションで、基本的な CRUD 操作用の[サンプルコードスニペット](#sample-code-snippets)を見つけることができます。

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
git clone https://github.com/tidb-samples/tidb-ruby-mysql2-quickstart.git
cd tidb-ruby-mysql2-quickstart
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

3.  接続ダイアログの設定がご使用のオペレーティング環境と一致していることを確認してください。

    -   **接続タイプ**は`Public`に設定されています。
    -   **ブランチ**は`main`に設定されています。
    -   **「接続」は**`General`に設定されています。
    -   **オペレーティングシステムは、**アプリケーションを実行するオペレーティングシステムと一致します。

4.  まだパスワードを設定していない場合は、 **「パスワードを生成」**をクリックしてランダムなパスワードを生成してください。

5.  `.env.example`をコピーして`.env`に名前を変更するには、次のコマンドを実行します。

    ```shell
    cp .env.example .env
    ```

6.  `.env`ファイルを編集し、環境変数を以下のように設定し、接続ダイアログで対応するプレースホルダー`{}`を接続パラメータに置き換えます。

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
    > [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合、パブリック エンドポイントを使用する際には`DATABASE_ENABLE_SSL`を介して TLS 接続を有効にする**必要があります**。

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

8.  `.env`ファイルを編集し、環境変数を以下のように設定し、接続ダイアログで対応するプレースホルダー`{}`を接続パラメータに置き換えます。

    ```dotenv
    DATABASE_HOST={host}
    DATABASE_PORT=4000
    DATABASE_USER={user}
    DATABASE_PASSWORD={password}
    DATABASE_NAME=test
    DATABASE_ENABLE_SSL=false
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

5.  `.env`ファイルを編集し、環境変数を以下のように設定し、接続ダイアログで対応するプレースホルダー`{}`を接続パラメータに置き換えます。

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
    > TiDB Cloud Dedicatedクラスタへの接続にパブリックエンドポイントを使用する場合は、TLS接続を有効にすることをお勧めします。
    >
    > TLS接続を有効にするには、 `DATABASE_ENABLE_SSL`を`true`に変更し、 `DATABASE_SSL_CA`を使用して、接続ダイアログからダウンロードしたCA証明書のファイルパスを指定します。

6.  `.env`ファイルを保存します。

</div>
<div label="TiDB Self-Managed" value="tidb">

1.  `.env.example`をコピーして`.env`に名前を変更するには、次のコマンドを実行します。

    ```shell
    cp .env.example .env
    ```

2.  `.env`ファイルを編集し、環境変数を以下のように設定し、対応するプレースホルダー`{}`を独自の TiDB 接続情報に置き換えてください。

    ```dotenv
    DATABASE_HOST={host}
    DATABASE_PORT=4000
    DATABASE_USER={user}
    DATABASE_PASSWORD={password}
    DATABASE_NAME=test
    ```

    TiDBをローカルで実行している場合、デフォルトのホストアドレスは`127.0.0.1`で、パスワードは空です。

3.  `.env`ファイルを保存します。

</div>
</SimpleTab>

### ステップ4：コードを実行して結果を確認する {#step-4-run-the-code-and-check-the-result}

サンプルコードを実行するには、以下のコマンドを実行してください。

```shell
ruby app.rb
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

完全なサンプルコードと実行方法については、 [tidb-samples/tidb-ruby-mysql2-quickstart](https://github.com/tidb-samples/tidb-ruby-mysql2-quickstart)リポジトリを参照してください。

### 接続オプションを使用してTiDBに接続します {#connect-to-tidb-with-connection-options}

以下のコードは、環境変数で定義されたオプションを使用してTiDBへの接続を確立します。

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
> [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合、パブリック エンドポイントを使用する際には`DATABASE_ENABLE_SSL`を介して TLS 接続を有効にする**必要があります****が**、mysql2 gem が特定の順序で既存の CA 証明書を検索してファイルが見つかるまで検索するため、 `DATABASE_SSL_CA`を介して SSL CA 証明書を指定する必要はありません。

### データを挿入する {#insert-data}

次のクエリは、2 つのフィールドを持つ単一のプレーヤーを作成し、 `last_insert_id`を返します。

```ruby
def create_player(client, coins, goods)
  result = client.query(
    "INSERT INTO players (coins, goods) VALUES (#{coins}, #{goods});"
  )
  client.last_id
end
```

詳細については、[データを挿入する](/develop/dev-guide-insert-data.md)を参照してください。

### クエリデータ {#query-data}

以下のクエリは、IDで指定された特定のプレイヤーのレコードを返します。

```ruby
def get_player_by_id(client, id)
  result = client.query(
    "SELECT id, coins, goods FROM players WHERE id = #{id};"
  )
  result.first
end
```

詳細については、 [クエリデータ](/develop/dev-guide-get-data-from-single-table.md)を参照してください。

### データの更新 {#update-data}

以下のクエリは、IDで指定された特定のプレイヤーのレコードを更新しました。

```ruby
def update_player(client, player_id, inc_coins, inc_goods)
  result = client.query(
    "UPDATE players SET coins = coins + #{inc_coins}, goods = goods + #{inc_goods} WHERE id = #{player_id};"
  )
  client.affected_rows
end
```

詳細については、[データの更新](/develop/dev-guide-update-data.md)を参照してください。

### データを削除する {#delete-data}

以下のクエリは、特定のプレイヤーのレコードを削除します。

```ruby
def delete_player_by_id(client, id)
  result = client.query(
    "DELETE FROM players WHERE id = #{id};"
  )
  client.affected_rows
end
```

詳細については、[データを削除する](/develop/dev-guide-delete-data.md)を参照してください。

## ベストプラクティス {#best-practices}

デフォルトでは、mysql2 gem は、ファイルが見つかるまで特定の順序で既存の CA 証明書を検索できます。

1.  Debian、Ubuntu、Gentoo、Arch、またはSlackwareの場合`/etc/ssl/certs/ca-certificates.crt`
2.  `/etc/pki/tls/certs/ca-bundle.crt`は RedHat、Fedora、CentOS、Mageia、Vercel、または Netlify 用です。
3.  OpenSUSE 用`/etc/ssl/ca-bundle.pem`
4.  `/etc/ssl/cert.pem` macOS または Alpine (Docker コンテナ)

CA証明書のパスを手動で指定することも可能ですが、異なるマシンや環境によってCA証明書の保存場所が異なる可能性があるため、複数の環境に展開するシナリオでは大きな不便が生じる可能性があります。そのため、柔軟性と異なる環境への展開の容易性を考慮して、 `sslca`を`nil`に設定することをお勧めします。

## 次のステップ {#next-steps}

-   mysql2 ドライバーの使用方法の詳細については[mysql2のドキュメント](https://github.com/brianmario/mysql2#readme)参照してください。
-   [開発者ガイド](https://docs.pingcap.com/developer/)[データを挿入する](/develop/dev-guide-insert-data.md)、[データの更新](/develop/dev-guide-update-data.md)[データを削除する](/develop/dev-guide-delete-data.md)SQL [取引](/develop/dev-guide-transaction-overview.md)[SQLパフォーマンス最適化](/develop/dev-guide-optimize-sql-overview.md)などの章を読ん[クエリデータ](/develop/dev-guide-get-data-from-single-table.md)、TiDB アプリケーション開発のベスト プラクティスを学びましょう。
-   プロフェッショナルな[TiDB開発者向けコース](https://www.pingcap.com/education/)コースを通じて学習し、試験に合格すると[TiDB認定資格](https://www.pingcap.com/education/certification/)を取得します。

## お困りですか？ {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)or [スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに質問してください。
-   [TiDB Cloudのサポートチケットを送信してください](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDB Self-Managedのサポートチケットを送信してください](/support.md)
