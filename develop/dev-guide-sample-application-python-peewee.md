---
title: Connect to TiDB with peewee
summary: peeweeを使ってTiDBに接続する方法を学びましょう。このチュートリアルでは、peeweeを使ってTiDBと連携するPythonのサンプルコードを紹介します。
aliases: ['/ja/tidb/stable/dev-guide-sample-application-python-peewee/','/ja/tidb/dev/dev-guide-sample-application-python-peewee/','/ja/tidbcloud/dev-guide-sample-application-python-peewee/']
---

# peeweeを使用してTiDBに接続します。 {#connect-to-tidb-with-peewee}

TiDBはMySQL互換のデータベースであり、PythonはPythonで人気の[ピーウィー](https://docs.peewee-orm.com/)リレーショナルマッパー（ORM）です。

このチュートリアルでは、TiDBとpeeweeを使用して以下のタスクを実行する方法を学ぶことができます。

-   環境をセットアップしてください。
-   peeweeを使用してTiDBに接続します。
-   アプリケーションをビルドして実行してください。必要に応じて、基本的なCRUD操作のサンプルコードスニペットも利用できます。

> **注記：**
>
> このチュートリアルは、 TiDB Cloud Starter、 TiDB Cloud Essential、 TiDB Cloud Dedicated、およびTiDB Self-Managedに対応しています。

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
git clone https://github.com/tidb-samples/tidb-python-peewee-quickstart.git
cd tidb-python-peewee-quickstart
```

### ステップ2：依存関係をインストールする {#step-2-install-dependencies}

サンプルアプリに必要なパッケージ（peeweeとPyMySQLを含む）をインストールするには、以下のコマンドを実行してください。

```shell
pip install -r requirements.txt
```

#### PyMySQLを使う理由とは？ {#why-use-pymysql}

peeweeは、複数のデータベースを扱うORMライブラリです。データベースの高レベルな抽象化を提供することで、開発者がよりオブジェクト指向的な方法でSQL文を記述できるように支援します。ただし、peeweeにはデータベースドライバは含まれていません。データベースに接続するには、データベースドライバをインストールする必要があります。このサンプルアプリケーションでは、データベースドライバとしてPyMySQLを使用しています。PyMySQLは、TiDBと互換性があり、すべてのプラットフォームにインストール可能な、純粋なPython製のMySQLクライアントライブラリです。詳細については、 [ピーウィー公式ドキュメント](https://docs.peewee-orm.com/en/latest/peewee/database.html?highlight=mysql#using-mysql)を参照してください。

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

7.  `.env`ファイルを保存します。

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

### ステップ4：コードを実行して結果を確認する {#step-4-run-the-code-and-check-the-result}

1.  サンプルコードを実行するには、以下のコマンドを実行してください。

    ```shell
    python peewee_example.py
    ```

2.  [期待される出力.txt](https://github.com/tidb-samples/tidb-python-peewee-quickstart/blob/main/Expected-Output.txt)をチェックして、出力が一致するかどうかを確認してください。

## サンプルコードスニペット {#sample-code-snippets}

以下のサンプルコードスニペットを参考に、独自のアプリケーション開発を完成させてください。

完全なサンプルコードと実行方法については、 [tidb-samples/tidb-python-peewee-quickstart](https://github.com/tidb-samples/tidb-python-peewee-quickstart)リポジトリを参照してください。

### TiDBに接続する {#connect-to-tidb}

```python
from peewee import MySQLDatabase

def get_db_engine():
    config = Config()
    connect_params = {}
    if ${ca_path}:
        connect_params = {
            "ssl_verify_cert": True,
            "ssl_verify_identity": True,
            "ssl_ca": ${ca_path},
        }
    return MySQLDatabase(
        ${tidb_db_name},
        host=${tidb_host},
        port=${tidb_port},
        user=${tidb_user},
        password=${tidb_password},
        **connect_params,
    )
```

この機能を使用する場合は、 `${tidb_host}` 、 `${tidb_port}` 、 `${tidb_user}` 、 `${tidb_password}` 、 `${tidb_db_name}` 、 `${ca_path}` TiDB の実際の値に置き換える必要があります。

### テーブルを定義する {#define-a-table}

```python
from peewee import Model, CharField, IntegerField

db = get_db_engine()

class BaseModel(Model):
    class Meta:
        database = db

class Player(BaseModel):
    name = CharField(max_length=32, unique=True)
    coins = IntegerField(default=0)
    goods = IntegerField(default=0)

    class Meta:
        table_name = "players"
```

詳細については、 [peewee ドキュメント: モデルとフィールド](https://docs.peewee-orm.com/en/latest/peewee/models.html)を参照してください。

### データを挿入する {#insert-data}

```python
# Insert a single record
Player.create(name="test", coins=100, goods=100)

# Insert multiple records
Player.insert_many(
    [
        {"name": "test1", "coins": 100, "goods": 100},
        {"name": "test2", "coins": 100, "goods": 100},
    ]
).execute()
```

詳細については、[データを挿入する](/develop/dev-guide-insert-data.md)を参照してください。

### クエリデータ {#query-data}

```python
# Query all records
players = Player.select()

# Query a single record
player = Player.get(Player.name == "test")

# Query multiple records
players = Player.select().where(Player.coins == 100)
```

詳細については、 [クエリデータ](/develop/dev-guide-get-data-from-single-table.md)を参照してください。

### データの更新 {#update-data}

```python
# Update a single record
player = Player.get(Player.name == "test")
player.coins = 200
player.save()

# Update multiple records
Player.update(coins=200).where(Player.coins == 100).execute()
```

詳細については、[データの更新](/develop/dev-guide-update-data.md)を参照してください。

### データを削除する {#delete-data}

```python
# Delete a single record
player = Player.get(Player.name == "test")
player.delete_instance()

# Delete multiple records
Player.delete().where(Player.coins == 100).execute()
```

詳細については、[データを削除する](/develop/dev-guide-delete-data.md)を参照してください。

## 次のステップ {#next-steps}

-   ピーウィーの使い方の詳細については、ピーウィー[ピーウィーのドキュメント](https://docs.peewee-orm.com/)ご覧ください。
-   [開発者ガイド](https://docs.pingcap.com/developer/)[データを挿入する](/develop/dev-guide-insert-data.md)[データの更新](/develop/dev-guide-update-data.md)、[データを削除する](/develop/dev-guide-delete-data.md)、「SQL パフォーマンス最適化」などの章[単一表の読み取り](/develop/dev-guide-get-data-from-single-table.md)読んで、TiDB アプリケーション [取引](/develop/dev-guide-transaction-overview.md)[SQLパフォーマンス最適化](/develop/dev-guide-optimize-sql-overview.md)。
-   プロフェッショナルな[TiDB開発者向けコース](https://www.pingcap.com/education/)コースを通じて学習し、試験に合格すると[TiDB認定資格](https://www.pingcap.com/education/certification/)を取得します。

## お困りですか？ {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)or [スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに質問してください。
-   [TiDB Cloudのサポートチケットを送信してください](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDB Self-Managedのサポートチケットを送信してください](/support.md)
