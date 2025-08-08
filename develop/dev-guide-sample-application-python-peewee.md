---
title: Connect to TiDB with peewee
summary: peeweeを使ってTiDBに接続する方法を学びましょう。このチュートリアルでは、peeweeを使ってTiDBを操作するPythonのサンプルコードスニペットを紹介します。
---

# peeweeでTiDBに接続する {#connect-to-tidb-with-peewee}

TiDB は MySQL 互換のデータベースであり、 [ピーウィー](https://docs.peewee-orm.com/) Python 用の人気のオブジェクト リレーショナル マッパー (ORM) です。

このチュートリアルでは、TiDB と peewee を使用して次のタスクを実行する方法を学習します。

-   環境を設定します。
-   peewee を使用して TiDB クラスターに接続します。
-   アプリケーションをビルドして実行します。オプションで、基本的なCRUD操作のサンプルコードスニペットもご利用いただけます。

> **注記：**
>
> このチュートリアルは、 TiDB Cloud Serverless、 TiDB Cloud Dedicated、および TiDB Self-Managed クラスターで機能します。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、次のものが必要です。

-   [Python 3.8以上](https://www.python.org/downloads/) 。
-   [ギット](https://git-scm.com/downloads) 。
-   TiDB クラスター。

<CustomContent platform="tidb">

**TiDB クラスターがない場合は、次のように作成できます。**

-   (推奨) [TiDB Cloud Serverless クラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って、独自のTiDB Cloudクラスターを作成します。
-   [ローカルテストTiDBクラスタをデプロイ](/quick-start-with-tidb.md#deploy-a-local-test-cluster)または[本番のTiDBクラスタをデプロイ](/production-deployment-using-tiup.md)に従ってローカル クラスターを作成します。

</CustomContent>
<CustomContent platform="tidb-cloud">

**TiDB クラスターがない場合は、次のように作成できます。**

-   (推奨) [TiDB Cloud Serverless クラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って、独自のTiDB Cloudクラスターを作成します。
-   [ローカルテストTiDBクラスタをデプロイ](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster)または[本番のTiDBクラスタをデプロイ](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup)に従ってローカル クラスターを作成します。

</CustomContent>

## サンプルアプリを実行してTiDBに接続する {#run-the-sample-app-to-connect-to-tidb}

このセクションでは、サンプル アプリケーション コードを実行して TiDB に接続する方法を説明します。

### ステップ1: サンプルアプリのリポジトリをクローンする {#step-1-clone-the-sample-app-repository}

サンプル コード リポジトリのクローンを作成するには、ターミナル ウィンドウで次のコマンドを実行します。

```shell
git clone https://github.com/tidb-samples/tidb-python-peewee-quickstart.git
cd tidb-python-peewee-quickstart
```

### ステップ2: 依存関係をインストールする {#step-2-install-dependencies}

次のコマンドを実行して、サンプル アプリに必要なパッケージ (peewee および PyMySQL を含む) をインストールします。

```shell
pip install -r requirements.txt
```

#### PyMySQL を使用する理由は何ですか? {#why-use-pymysql}

peeweeは複数のデータベースに対応するORMライブラリです。データベースの高レベルな抽象化を提供し、開発者がよりオブジェクト指向的な方法でSQL文を記述するのに役立ちます。ただし、peeweeにはデータベースドライバが含まれていません。データベースに接続するには、データベースドライバをインストールする必要があります。このサンプルアプリケーションでは、データベースドライバとしてPyMySQLを使用しています。PyMySQLは、TiDBと互換性があり、すべてのプラットフォームにインストール可能なPure Python MySQLクライアントライブラリです。詳細については、 [ピーウィー公式ドキュメント](https://docs.peewee-orm.com/en/latest/peewee/database.html?highlight=mysql#using-mysql)を参照してください。

### ステップ3: 接続情報を構成する {#step-3-configure-connection-information}

選択した TiDB デプロイメント オプションに応じて、TiDB クラスターに接続します。

<SimpleTab>
<div label="TiDB Cloud Serverless">

1.  [**クラスター**](https://tidbcloud.com/project/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログの構成が動作環境と一致していることを確認します。

    -   **接続タイプ**は`Public`に設定されています

    -   **ブランチ**は`main`に設定されています

    -   **接続先が**`General`に設定されています

    -   **オペレーティング システムは**環境に適合します。

    > **ヒント：**
    >
    > プログラムが Windows Subsystem for Linux (WSL) で実行されている場合は、対応する Linux ディストリビューションに切り替えます。

4.  ランダムなパスワードを作成するには、 **「パスワードの生成」を**クリックします。

    > **ヒント：**
    >
    > 以前にパスワードを作成したことがある場合は、元のパスワードを使用するか、 **「パスワードのリセット」を**クリックして新しいパスワードを生成することができます。

5.  次のコマンドを実行して`.env.example`コピーし、名前を`.env`に変更します。

    ```shell
    cp .env.example .env
    ```

6.  対応する接続文字列をコピーして、 `.env`ファイルに貼り付けます。結果の例は次のとおりです。

    ```dotenv
    TIDB_HOST='{host}'  # e.g. gateway01.ap-northeast-1.prod.aws.tidbcloud.com
    TIDB_PORT='4000'
    TIDB_USER='{user}'  # e.g. xxxxxx.root
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    CA_PATH='{ssl_ca}'  # e.g. /etc/ssl/certs/ca-certificates.crt (Debian / Ubuntu / Arch)
    ```

    プレースホルダー`{}` 、接続ダイアログから取得した接続パラメータに置き換えてください。

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

5.  対応する接続文字列をコピーして、 `.env`ファイルに貼り付けます。結果の例は次のとおりです。

    ```dotenv
    TIDB_HOST='{host}'  # e.g. tidb.xxxx.clusters.tidb-cloud.com
    TIDB_PORT='4000'
    TIDB_USER='{user}'  # e.g. root
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    CA_PATH='{your-downloaded-ca-path}'
    ```

    プレースホルダー`{}`接続ダイアログから取得した接続パラメータに置き換え、 `CA_PATH`前の手順でダウンロードした証明書パスで構成してください。

6.  `.env`ファイルを保存します。

</div>
<div label="TiDB Self-Managed">

1.  次のコマンドを実行して`.env.example`コピーし、名前を`.env`に変更します。

    ```shell
    cp .env.example .env
    ```

2.  対応する接続文字列をコピーして、 `.env`ファイルに貼り付けます。結果の例は次のとおりです。

    ```dotenv
    TIDB_HOST='{tidb_server_host}'
    TIDB_PORT='4000'
    TIDB_USER='root'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    ```

    プレースホルダー`{}`接続パラメータに置き換え、 `CA_PATH`行を削除してください。TiDB をローカルで実行している場合、デフォルトのホストアドレスは`127.0.0.1`で、パスワードは空です。

3.  `.env`ファイルを保存します。

</div>
</SimpleTab>

### ステップ4: コードを実行して結果を確認する {#step-4-run-the-code-and-check-the-result}

1.  サンプル コードを実行するには、次のコマンドを実行します。

    ```shell
    python peewee_example.py
    ```

2.  [期待出力.txt](https://github.com/tidb-samples/tidb-python-peewee-quickstart/blob/main/Expected-Output.txt)チェックして、出力が一致するかどうかを確認します。

## サンプルコードスニペット {#sample-code-snippets}

次のサンプル コード スニペットを参照して、独自のアプリケーション開発を完了することができます。

完全なサンプル コードとその実行方法については、 [tidb-samples/tidb-python-peewee-quickstart](https://github.com/tidb-samples/tidb-python-peewee-quickstart)リポジトリを参照してください。

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

この関数を使用する場合は、 `${tidb_host}` 、 `${tidb_port}` 、 `${tidb_user}` 、 `${tidb_password}` 、 `${tidb_db_name}` 、 `${ca_path}` TiDB クラスターの実際の値に置き換える必要があります。

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

詳細については[peewee ドキュメント: モデルとフィールド](https://docs.peewee-orm.com/en/latest/peewee/models.html)を参照してください。

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

詳細については[データを挿入する](/develop/dev-guide-insert-data.md)を参照してください。

### クエリデータ {#query-data}

```python
# Query all records
players = Player.select()

# Query a single record
player = Player.get(Player.name == "test")

# Query multiple records
players = Player.select().where(Player.coins == 100)
```

詳細については[クエリデータ](/develop/dev-guide-get-data-from-single-table.md)を参照してください。

### データを更新する {#update-data}

```python
# Update a single record
player = Player.get(Player.name == "test")
player.coins = 200
player.save()

# Update multiple records
Player.update(coins=200).where(Player.coins == 100).execute()
```

詳細については[データを更新する](/develop/dev-guide-update-data.md)を参照してください。

### データを削除する {#delete-data}

```python
# Delete a single record
player = Player.get(Player.name == "test")
player.delete_instance()

# Delete multiple records
Player.delete().where(Player.coins == 100).execute()
```

詳細については[データを削除する](/develop/dev-guide-delete-data.md)を参照してください。

## 次のステップ {#next-steps}

-   peewee の使い方を[ピーウィーの記録](https://docs.peewee-orm.com/)から詳しく学びましょう。
-   [開発者ガイド](/develop/dev-guide-overview.md)の[データを挿入する](/develop/dev-guide-insert-data.md) 、 [データを更新する](/develop/dev-guide-update-data.md) 、 [データを削除する](/develop/dev-guide-delete-data.md) 、 [単一テーブルの読み取り](/develop/dev-guide-get-data-from-single-table.md) 、 [取引](/develop/dev-guide-transaction-overview.md) 、 [SQLパフォーマンスの最適化](/develop/dev-guide-optimize-sql-overview.md)などの章で、 TiDB アプリケーション開発のベスト プラクティスを学習します。
-   プロフェッショナル[TiDB開発者コース](https://www.pingcap.com/education/)を通じて学び、試験に合格すると[TiDB認定](https://www.pingcap.com/education/certification/)獲得します。

## ヘルプが必要ですか? {#need-help}

<CustomContent platform="tidb">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、あるいは[サポートチケットを送信する](/support.md)についてコミュニティに質問してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、あるいは[サポートチケットを送信する](https://tidb.support.pingcap.com/)についてコミュニティに質問してください。

</CustomContent>
