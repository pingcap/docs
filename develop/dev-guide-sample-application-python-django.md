---
title: Connect to TiDB with Django
summary: Learn how to connect to TiDB using Django. This tutorial gives Python sample code snippets that work with TiDB using Django.
---

# Django を使用して TiDB に接続する {#connect-to-tidb-with-django}

TiDB は MySQL 互換データベースであり、 [ジャンゴ](https://www.djangoproject.com)は Python の人気のある Web フレームワークであり、強力なオブジェクト リレーショナル マッパー (ORM) ライブラリが含まれています。

このチュートリアルでは、TiDB と Django を使用して次のタスクを実行する方法を学習できます。

-   環境をセットアップします。
-   Django を使用して TiDB クラスターに接続します。
-   アプリケーションをビルドして実行します。オプションで、基本的な CRUD 操作のサンプル コード スニペットを見つけることができます。

> **注記：**
>
> このチュートリアルは、TiDB サーバーレス、TiDB 専用、および TiDB セルフホスト クラスターで動作します。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、次のものが必要です。

-   [Python 3.8以降](https://www.python.org/downloads/) 。
-   [ギット](https://git-scm.com/downloads) 。
-   TiDB クラスター。

<CustomContent platform="tidb">

**TiDB クラスターがない場合は、次のように作成できます。**

-   (推奨) [TiDB サーバーレスクラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って、独自のTiDB Cloudクラスターを作成します。
-   [ローカル テスト TiDB クラスターをデプロイ](/quick-start-with-tidb.md#deploy-a-local-test-cluster)または[本番TiDB クラスターをデプロイ](/production-deployment-using-tiup.md)に従ってローカル クラスターを作成します。

</CustomContent>
<CustomContent platform="tidb-cloud">

**TiDB クラスターがない場合は、次のように作成できます。**

-   (推奨) [TiDB サーバーレスクラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って、独自のTiDB Cloudクラスターを作成します。
-   [ローカル テスト TiDB クラスターをデプロイ](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster)または[本番TiDB クラスターをデプロイ](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup)に従ってローカル クラスターを作成します。

</CustomContent>

## サンプル アプリを実行して TiDB に接続する {#run-the-sample-app-to-connect-to-tidb}

このセクションでは、サンプル アプリケーション コードを実行して TiDB に接続する方法を説明します。

### ステップ 1: サンプル アプリ リポジトリのクローンを作成する {#step-1-clone-the-sample-app-repository}

ターミナル ウィンドウで次のコマンドを実行して、サンプル コード リポジトリのクローンを作成します。

```shell
git clone https://github.com/tidb-samples/tidb-python-django-quickstart.git
cd tidb-python-django-quickstart
```

### ステップ 2: 依存関係をインストールする {#step-2-install-dependencies}

次のコマンドを実行して、サンプル アプリに必要なパッケージ (Django、django-tidb、mysqlclient など) をインストールします。

```shell
pip install -r requirements.txt
```

mysqlclient でインストールの問題が発生した場合は、 [mysqlclientの公式ドキュメント](https://github.com/PyMySQL/mysqlclient#install)を参照してください。

#### <code>django-tidb</code>とは何ですか? {#what-is-code-django-tidb-code}

`django-tidb`は、TiDB と Django の間の互換性の問題を解決する Django 用の TiDB 方言です。

`django-tidb`をインストールするには、Django のバージョンと一致するバージョンを選択します。たとえば、 `django==4.2.*`使用している場合は、 `django-tidb==4.2.*`をインストールします。マイナー バージョンは同じである必要はありません。最新のマイナー バージョンを使用することをお勧めします。

詳細については、 [django-tidb リポジトリ](https://github.com/pingcap/django-tidb)を参照してください。

### ステップ 3: 接続情報を構成する {#step-3-configure-connection-information}

選択した TiDB デプロイメント オプションに応じて、TiDB クラスターに接続します。

<SimpleTab>
<div label="TiDB Serverless">

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして、その概要ページに移動します。

2.  右上隅にある**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログの設定が動作環境と一致していることを確認してください。

    -   **エンドポイント タイプは**`Public`に設定されます

    -   **[接続先] は**`General`に設定されています

    -   **オペレーティング システムが**環境に一致します。

    > **ヒント：**
    >
    > プログラムが Windows Subsystem for Linux (WSL) で実行されている場合は、対応する Linux ディストリビューションに切り替えます。

4.  **「パスワードの作成」**をクリックしてランダムなパスワードを作成します。

    > **ヒント：**
    >
    > 以前にパスワードを作成したことがある場合は、元のパスワードを使用するか、 **「パスワードのリセット」**をクリックして新しいパスワードを生成できます。

5.  次のコマンドを実行して`.env.example`をコピーし、名前を`.env`に変更します。

    ```shell
    cp .env.example .env
    ```

6.  対応する接続​​文字列をコピーして`.env`ファイルに貼り付けます。結果の例は次のとおりです。

    ```dotenv
    TIDB_HOST='{host}'  # e.g. gateway01.ap-northeast-1.prod.aws.tidbcloud.com
    TIDB_PORT='4000'
    TIDB_USER='{user}'  # e.g. xxxxxx.root
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    CA_PATH='{ssl_ca}'  # e.g. /etc/ssl/certs/ca-certificates.crt (Debian / Ubuntu / Arch)
    ```

    プレースホルダー`{}` 、接続ダイアログから取得した接続パラメーターに必ず置き換えてください。

    TiDB サーバーレスには安全な接続が必要です。 mysqlclient の`ssl_mode`デフォルトで`PREFERRED`であるため、手動で`CA_PATH`を指定する必要はありません。空のままにしておいてください。ただし、 `CA_PATH`手動で指定する特別な理由がある場合は、 [TiDB サーバーレスへの TLS 接続](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-clusters)を参照して、さまざまなオペレーティング システムの証明書パスを取得できます。

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

5.  対応する接続​​文字列をコピーして`.env`ファイルに貼り付けます。結果の例は次のとおりです。

    ```dotenv
    TIDB_HOST='{host}'  # e.g. tidb.xxxx.clusters.tidb-cloud.com
    TIDB_PORT='4000'
    TIDB_USER='{user}'  # e.g. root
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    CA_PATH='{your-downloaded-ca-path}'
    ```

    必ずプレースホルダー`{}`接続ダイアログから取得した接続パラメーターに置き換え、 `CA_PATH`前の手順でダウンロードした証明書パスで構成してください。

6.  `.env`ファイルを保存します。

</div>
<div label="TiDB Self-Hosted">

1.  次のコマンドを実行して`.env.example`をコピーし、名前を`.env`に変更します。

    ```shell
    cp .env.example .env
    ```

2.  対応する接続​​文字列をコピーして`.env`ファイルに貼り付けます。結果の例は次のとおりです。

    ```dotenv
    TIDB_HOST='{tidb_server_host}'
    TIDB_PORT='4000'
    TIDB_USER='root'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    ```

    必ずプレースホルダー`{}`接続パラメーターに置き換えて、 `CA_PATH`行を削除してください。 TiDB をローカルで実行している場合、デフォルトのホスト アドレスは`127.0.0.1`で、パスワードは空です。

3.  `.env`ファイルを保存します。

</div>
</SimpleTab>

### ステップ 4: データベースを初期化する {#step-4-initialize-the-database}

プロジェクトのルート ディレクトリで次のコマンドを実行してデータベースを初期化します。

```shell
python manage.py migrate
```

### ステップ 5: サンプル アプリケーションを実行する {#step-5-run-the-sample-application}

1.  アプリケーションを開発モードで実行します。

    ```shell
    python manage.py runserver
    ```

    アプリケーションはデフォルトでポート`8000`で実行されます。別のポートを使用するには、コマンドにポート番号を追加します。以下は例です。

    ```shell
    python manage.py runserver 8080
    ```

2.  アプリケーションにアクセスするには、ブラウザを開いて`http://localhost:8000/`に進みます。サンプル アプリケーションでは、次のことができます。

    -   新しいプレーヤーを作成します。
    -   プレーヤーを一括作成します。
    -   すべてのプレーヤーをビュー。
    -   プレーヤーを更新します。
    -   プレーヤーを削除します。
    -   2 人のプレイヤー間で商品を交換します。

## サンプルコードスニペット {#sample-code-snippets}

次のサンプル コード スニペットを参照して、独自のアプリケーション開発を完了できます。

完全なサンプル コードとその実行方法については、 [tidb-samples/tidb-python-django-quickstart](https://github.com/tidb-samples/tidb-python-django-quickstart)リポジトリを確認してください。

### TiDB に接続する {#connect-to-tidb}

ファイル`sample_project/settings.py`に、次の構成を追加します。

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

`${tidb_host}` 、 `${tidb_port}` 、 `${tidb_user}` 、 `${tidb_password}` 、 `${tidb_db_name}` 、および`${ca_path}`を TiDB クラスターの実際の値に置き換える必要があります。

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

詳細については、 [ジャンゴモデル](https://docs.djangoproject.com/en/dev/topics/db/models/)を参照してください。

### データの挿入 {#insert-data}

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

詳細については、 [データの挿入](/develop/dev-guide-insert-data.md)を参照してください。

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

### データを更新する {#update-data}

```python
# update a single object
player = Player.objects.get(name="player1")
player.coins = 200
player.save()

# update multiple objects
Player.objects.filter(coins=100).update(coins=200)
```

詳細については、 [データを更新する](/develop/dev-guide-update-data.md)を参照してください。

### データの削除 {#delete-data}

```python
# delete a single object
player = Player.objects.get(name="player1")
player.delete()

# delete multiple objects
Player.objects.filter(coins=100).delete()
```

詳細については、 [データの削除](/develop/dev-guide-delete-data.md)を参照してください。

## 次のステップ {#next-steps}

-   Django の詳しい使い方を[Django のドキュメント](https://www.djangoproject.com/)から学びましょう。
-   TiDB アプリケーション開発[単一テーブルの読み取り](/develop/dev-guide-get-data-from-single-table.md)ベスト プラクティスについて[取引](/develop/dev-guide-transaction-overview.md) 、 [開発者ガイド](/develop/dev-guide-overview.md)の章 ( [データの挿入](/develop/dev-guide-insert-data.md)など) [データを更新する](/develop/dev-guide-update-data.md)参照[データの削除](/develop/dev-guide-delete-data.md) [SQLパフォーマンスの最適化](/develop/dev-guide-optimize-sql-overview.md)ください。
-   プロフェッショナルとして[TiDB 開発者コース](https://www.pingcap.com/education/)を学び、試験合格後に[TiDB 認定](https://www.pingcap.com/education/certification/)獲得します。

## 助けが必要？ {#need-help}

<CustomContent platform="tidb">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[サポートチケットを作成する](/support.md)について質問してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[サポートチケットを作成する](https://support.pingcap.com/)について質問してください。

</CustomContent>
