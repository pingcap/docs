---
title: Connect to TiDB with Django
summary: Djangoを使ってTiDBに接続する方法を学びましょう。このチュートリアルでは、Djangoを使ってTiDBと連携するPythonのサンプルコードを紹介します。
aliases: ['/ja/tidb/dev/dev-guide-outdated-for-django','/ja/tidb/stable/dev-guide-sample-application-python-django/','/ja/tidb/dev/dev-guide-sample-application-python-django/','/ja/tidbcloud/dev-guide-sample-application-python-django/']
---

# DjangoでTiDBに接続する {#connect-to-tidb-with-django}

TiDBはMySQL互換のデータベースであり、[ジャンゴ](https://www.djangoproject.com)強力なオブジェクトリレーショナルマッパー（ORM）ライブラリを含む、Python向けの人気の高いWebフレームワークです。

このチュートリアルでは、TiDBとDjangoを使用して以下のタスクを実行する方法を学ぶことができます。

-   環境をセットアップしてください。
-   Djangoを使用してTiDBに接続します。
-   アプリケーションをビルドして実行します。必要に応じて、基本的なCRUD操作のサンプルコードスニペットも利用できます。

> **注記：**
>
> このチュートリアルは、 TiDB Cloud Starter、 TiDB Cloud Essential、 TiDB Cloud Premium、 TiDB Cloud Dedicated、およびTiDB Self-Managedに対応しています。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、以下が必要です。

-   [Python 3.8以降](https://www.python.org/downloads/)。
-   [Git](https://git-scm.com/downloads) 。
-   TiDBクラスタ。

**TiDBクラスタをお持ちでない場合は、以下の手順で作成できます。**

-   (推奨) [TiDB Cloud Starterインスタンスを作成する](/develop/dev-guide-build-cluster-in-cloud.md)。
-   [ローカルテスト用のTiDBセルフマネージドクラスタをデプロイ。](/quick-start-with-tidb.md#deploy-a-local-test-cluster)または[本番本番のTiDBセルフマネージドクラスタをデプロイ。](/production-deployment-using-tiup.md)

## TiDBに接続するには、サンプルアプリを実行してください。 {#run-the-sample-app-to-connect-to-tidb}

このセクションでは、サンプルアプリケーションコードを実行してTiDBに接続する方法を説明します。

### ステップ1：サンプルアプリのリポジトリをクローンする {#step-1-clone-the-sample-app-repository}

サンプルコードリポジトリをクローンするには、ターミナルウィンドウで以下のコマンドを実行してください。

```shell
git clone https://github.com/tidb-samples/tidb-python-django-quickstart.git
cd tidb-python-django-quickstart
```

### ステップ2：依存関係をインストールする {#step-2-install-dependencies}

サンプルアプリに必要なパッケージ（Django、django-tidb、mysqlclientなど）をインストールするには、以下のコマンドを実行してください。

```shell
pip install -r requirements.txt
```

mysqlclient でインストールの問題が発生した場合は、 [mysqlclient の公式ドキュメント](https://github.com/PyMySQL/mysqlclient#install)を参照してください。

#### <code>django-tidb</code>とは何ですか？ {#what-is-code-django-tidb-code}

`django-tidb`は、TiDB と Django 間の互換性の問題を解決する Django 用の TiDB 方言です。

`django-tidb`をインストールするには、お使いの Django のバージョンに合ったバージョンを選択してください。例えば、 `django==4.2.*`を使用している場合は、 `django-tidb==4.2.*`をインストールしてください。マイナーバージョンは同じである必要はありませんが、最新のマイナーバージョンを使用することをお勧めします。

詳細については、 [django-tidbリポジトリ](https://github.com/pingcap/django-tidb)を参照してください。

### ステップ3：接続情報の設定 {#step-3-configure-connection-information}

選択したTiDBのデプロイオプションに応じて、TiDBに接続してください。

<SimpleTab>
<div label="TiDB Cloud Starter or Essential">

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud StarterまたはEssentialインスタンスの名前をクリックして、概要ページに移動します。

2.  右上隅の**「接続」**をクリックしてください。接続ダイアログが表示されます。

3.  接続ダイアログの設定がご使用のオペレーティング環境と一致していることを確認してください。

    -   **接続タイプ**は`Public`に設定されています。

    -   **ブランチ**は`main`に設定されています。

    -   **Connect With は**`General`に設定されています。

    -   お使いの環境に合った**オペレーティングシステム**を選択してください。

    > **ヒント：**
    >
    > プログラムがWindows Subsystem for Linux（WSL）上で実行されている場合は、対応するLinuxディストリビューションに切り替えてください。

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
    TIDB_HOST='{host}'  # e.g. gateway01.ap-northeast-1.prod.aws.tidbcloud.com
    TIDB_PORT='4000'
    TIDB_USER='{user}'  # e.g. xxxxxx.root
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    CA_PATH='{ssl_ca}'  # e.g. /etc/ssl/certs/ca-certificates.crt (Debian / Ubuntu / Arch)
    ```

    必ずプレースホルダー`{}`を、接続ダイアログから取得した接続パラメータに置き換えてください。

    TiDB Cloud Starter は安全な接続を必要とします。mysqlclient の`ssl_mode`はデフォルトで`PREFERRED`になっているため、 `CA_PATH`手動で指定する必要はありません。空欄のままにしてください。ただし、 `CA_PATH`手動で指定する必要がある特別な理由がある場合は、 [TiDB Cloud StarterへのTLS接続](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-clusters)を参照して、さまざまなオペレーティングシステムの証明書パスを取得してください。

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

8.  対応する接続​​文字列`.env`ファイルにコピー＆ペーストしてください。例は以下のとおりです。

    ```dotenv
    TIDB_HOST='{host}'  # e.g. tidb.xxxx.clusters.tidb-cloud.com
    TIDB_PORT='4000'
    TIDB_USER='{user}'  # e.g. root
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    ```

    必ずプレースホルダー`{}`を、接続ダイアログから取得した接続パラメータに置き換えてください。

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

5.  対応する接続​​文字列`.env`ファイルにコピー＆ペーストしてください。例は以下のとおりです。

    ```dotenv
    TIDB_HOST='{host}'  # e.g. tidb.xxxx.clusters.tidb-cloud.com
    TIDB_PORT='4000'
    TIDB_USER='{user}'  # e.g. root
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    CA_PATH='{your-downloaded-ca-path}'
    ```

    必ず、プレースホルダー`{}`を接続ダイアログから取得した接続パラメータに置き換え、 `CA_PATH`前の手順でダウンロードした証明書のパスに設定してください。

6.  `.env`ファイルを保存します。

</div>
<div label="TiDB Self-Managed" value="tidb">

1.  `.env.example`をコピーして`.env`に名前を変更するには、次のコマンドを実行します。

    ```shell
    cp .env.example .env
    ```

2.  対応する接続​​文字列`.env`ファイルにコピー＆ペーストしてください。例は以下のとおりです。

    ```dotenv
    TIDB_HOST='{tidb_server_host}'
    TIDB_PORT='4000'
    TIDB_USER='root'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    ```

    プレースホルダー`{}`を接続パラメータに置き換え、 `CA_PATH`の行を削除してください。TiDB をローカルで実行している場合、デフォルトのホスト アドレスは`127.0.0.1`で、パスワードは空欄です。

3.  `.env`ファイルを保存します。

</div>
</SimpleTab>

### ステップ4：データベースを初期化する {#step-4-initialize-the-database}

プロジェクトのルートディレクトリで、以下のコマンドを実行してデータベースを初期化します。

```shell
python manage.py migrate
```

### ステップ5：サンプルアプリケーションを実行する {#step-5-run-the-sample-application}

1.  アプリケーションを開発モードで実行します。

    ```shell
    python manage.py runserver
    ```

    アプリケーションはデフォルトでポート`8000`で実行されます。別のポートを使用するには、コマンドにポート番号を追加します。以下に例を示します。

    ```shell
    python manage.py runserver 8080
    ```

2.  アプリケーションにアクセスするには、ブラウザを開いて`http://localhost:8000/`にアクセスしてください。サンプルアプリケーションでは、以下の操作が可能です。

    -   新しいプレイヤーを作成します。
    -   プレイヤーを一括作成する。
    -   全プレイヤーをビュー。
    -   プレイヤーを更新する。
    -   プレイヤーを削除する。
    -   2人のプレイヤー間で商品を取引する。

## サンプルコードスニペット {#sample-code-snippets}

以下のサンプルコードスニペットを参考に、独自のアプリケーション開発を完成させてください。

完全なサンプルコードと実行方法については、 [tidb-samples/tidb-python-django-quickstart](https://github.com/tidb-samples/tidb-python-django-quickstart)リポジトリを参照してください。

### TiDBに接続する {#connect-to-tidb}

ファイル`sample_project/settings.py`に、以下の設定を追加します。

```python
DATABASES = {
    "default": {
        "ENGINE": "django_tidb",
        "HOST": ${tidb_host},
        "PORT": ${tidb_port},
        "USER": ${tidb_user},
        "PASSWORD": ${tidb_password},
        "NAME": ${tidb_db_name},
        "OPTIONS": {
            "charset": "utf8mb4",
        },
    }
}

TIDB_CA_PATH = ${ca_path}
if TIDB_CA_PATH:
    DATABASES["default"]["OPTIONS"]["ssl_mode"] = "VERIFY_IDENTITY"
    DATABASES["default"]["OPTIONS"]["ssl"] = {
        "ca": TIDB_CA_PATH,
    }
```

`${tidb_host}` 、 `${tidb_port}` 、 `${tidb_user}` 、 `${tidb_password}` 、 `${tidb_db_name}` 、および`${ca_path}` 、TiDBの実際の値に置き換える必要があります。

### データモデルを定義する {#define-the-data-model}

```python
from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=32, blank=False, null=False)
    coins = models.IntegerField(default=100)
    goods = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

詳細については、 [Djangoモデル](https://docs.djangoproject.com/en/dev/topics/db/models/)を参照してください。

### データを挿入する {#insert-data}

```python
# insert a single object
player = Player.objects.create(name="player1", coins=100, goods=1)

# bulk insert multiple objects
Player.objects.bulk_create([
    Player(name="player1", coins=100, goods=1),
    Player(name="player2", coins=200, goods=2),
    Player(name="player3", coins=300, goods=3),
])
```

詳細については、[データを挿入する](/develop/dev-guide-insert-data.md)を参照してください。

### クエリデータ {#query-data}

```python
# get a single object
player = Player.objects.get(name="player1")

# get multiple objects
filtered_players = Player.objects.filter(name="player1")

# get all objects
all_players = Player.objects.all()
```

詳細については、 [クエリデータ](/develop/dev-guide-get-data-from-single-table.md)を参照してください。

### データの更新 {#update-data}

```python
# update a single object
player = Player.objects.get(name="player1")
player.coins = 200
player.save()

# update multiple objects
Player.objects.filter(coins=100).update(coins=200)
```

詳細については、[データの更新](/develop/dev-guide-update-data.md)を参照してください。

### データを削除する {#delete-data}

```python
# delete a single object
player = Player.objects.get(name="player1")
player.delete()

# delete multiple objects
Player.objects.filter(coins=100).delete()
```

詳細については、[データを削除する](/develop/dev-guide-delete-data.md)を参照してください。

## 次のステップ {#next-steps}

-   Django の使用法の詳細については[Djangoのドキュメント](https://www.djangoproject.com/)参照してください。
-   [開発者ガイド](https://docs.pingcap.com/developer/)[データを挿入する](/develop/dev-guide-insert-data.md)[データの更新](/develop/dev-guide-update-data.md)、[データを削除する](/develop/dev-guide-delete-data.md)、「SQL パフォーマンス最適化」などの章[単一表の読み取り](/develop/dev-guide-get-data-from-single-table.md)読んで、TiDB アプリケーション [取引](/develop/dev-guide-transaction-overview.md)[SQLパフォーマンス最適化](/develop/dev-guide-optimize-sql-overview.md)。
-   プロフェッショナルな[TiDB開発者向けコース](https://www.pingcap.com/education/)コースを通じて学習し、試験に合格すると[TiDB認定資格](https://www.pingcap.com/education/certification/)を取得します。

## お困りですか？ {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)or [スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに質問してください。
-   [TiDB Cloudのサポートチケットを送信してください](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDB Self-Managedのサポートチケットを送信してください](/support.md)
