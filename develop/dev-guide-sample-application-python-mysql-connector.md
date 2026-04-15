---
title: Connect to TiDB with MySQL Connector/Python
summary: MySQL Connector/Pythonを使用してTiDBに接続する方法を学びましょう。このチュートリアルでは、MySQL Connector/Pythonを使用してTiDBと連携するPythonのサンプルコードを紹介します。
aliases: ['/ja/tidb/dev/dev-guide-sample-application-python','/ja/tidb/dev/dev-guide-outdated-for-python-mysql-connector','/ja/tidb/stable/dev-guide-sample-application-python-mysql-connector/','/ja/tidb/dev/dev-guide-sample-application-python-mysql-connector/','/ja/tidbcloud/dev-guide-sample-application-python-mysql-connector/']
---

# MySQL Connector/Pythonを使用してTiDBに接続する {#connect-to-tidb-with-mysql-connector-python}

TiDB は MySQL 互換データベースであり、 [MySQLコネクタ/Python](https://dev.mysql.com/doc/connector-python/en/)は Python 用の公式 MySQL ドライバーです。

このチュートリアルでは、TiDBとMySQL Connector/Pythonを使用して以下のタスクを実行する方法を学ぶことができます。

-   環境をセットアップしてください。
-   MySQL Connector/Pythonを使用してTiDBに接続します。
-   アプリケーションをビルドして実行します。必要に応じて、基本的なCRUD操作のサンプルコードスニペットも利用できます。

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
git clone https://github.com/tidb-samples/tidb-python-mysqlconnector-quickstart.git
cd tidb-python-mysqlconnector-quickstart
```

### ステップ2：依存関係をインストールする {#step-2-install-dependencies}

サンプルアプリに必要なパッケージ（mysql-connector-pythonを含む）をインストールするには、以下のコマンドを実行してください。

```shell
pip install -r requirements.txt
```

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
    python mysql_connector_example.py
    ```

2.  [期待される出力.txt](https://github.com/tidb-samples/tidb-python-mysqlconnector-quickstart/blob/main/Expected-Output.txt)をチェックして、出力が一致するかどうかを確認してください。

## サンプルコードスニペット {#sample-code-snippets}

以下のサンプルコードスニペットを参考に、独自のアプリケーション開発を完成させてください。

完全なサンプルコードと実行方法については、 [tidb-samples/tidb-python-mysqlconnector-quickstart](https://github.com/tidb-samples/tidb-python-mysqlconnector-quickstart)リポジトリを参照してください。

### TiDBに接続する {#connect-to-tidb}

```python
def get_connection(autocommit: bool = True) -> MySQLConnection:
    config = Config()
    db_conf = {
        "host": ${tidb_host},
        "port": ${tidb_port},
        "user": ${tidb_user},
        "password": ${tidb_password},
        "database": ${tidb_db_name},
        "autocommit": autocommit,
        "use_pure": True,
    }

    if ${ca_path}:
        db_conf["ssl_verify_cert"] = True
        db_conf["ssl_verify_identity"] = True
        db_conf["ssl_ca"] = ${ca_path}
    return mysql.connector.connect(**db_conf)
```

この機能を使用する場合は、 `${tidb_host}` 、 `${tidb_port}` 、 `${tidb_user}` 、 `${tidb_password}` 、 `${tidb_db_name}` 、 `${ca_path}` TiDB の実際の値に置き換える必要があります。

### データを挿入する {#insert-data}

```python
with get_connection(autocommit=True) as conn:
    with conn.cursor() as cur:
        player = ("1", 1, 1)
        cursor.execute("INSERT INTO players (id, coins, goods) VALUES (%s, %s, %s)", player)
```

詳細については、[データを挿入する](/develop/dev-guide-insert-data.md)を参照してください。

### クエリデータ {#query-data}

```python
with get_connection(autocommit=True) as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT count(*) FROM players")
        print(cur.fetchone()[0])
```

詳細については、 [クエリデータ](/develop/dev-guide-get-data-from-single-table.md)を参照してください。

### データの更新 {#update-data}

```python
with get_connection(autocommit=True) as conn:
    with conn.cursor() as cur:
        player_id, amount, price="1", 10, 500
        cursor.execute(
            "UPDATE players SET goods = goods + %s, coins = coins + %s WHERE id = %s",
            (-amount, price, player_id),
        )
```

詳細については、[データの更新](/develop/dev-guide-update-data.md)を参照してください。

### データを削除する {#delete-data}

```python
with get_connection(autocommit=True) as conn:
    with conn.cursor() as cur:
        player_id = "1"
        cursor.execute("DELETE FROM players WHERE id = %s", (player_id,))
```

詳細については、[データを削除する](/develop/dev-guide-delete-data.md)を参照してください。

## 役立つメモ {#useful-notes}

### ドライバーまたはORMフレームワークを使用していますか？ {#using-driver-or-orm-framework}

Pythonドライバはデータベースへの低レベルアクセスを提供するが、開発者には以下のことが必要となる。

-   データベース接続を手動で確立および解放します。
-   データベースのトランザクションを手動で管理する。
-   データ行（ `mysql-connector-python`ではタプルまたは辞書として表現されます）をデータオブジェクトに手動でマッピングします。

複雑なSQL文を書く必要がない限り、 [SQLAlchemy](/develop/dev-guide-sample-application-python-sqlalchemy.md) 、 [ピーウィー](/develop/dev-guide-sample-application-python-peewee.md)、Django ORMなどの[ORM](https://en.wikipedia.org/w/index.php?title=Object-relational_mapping)フレームワークを開発に使用することをお勧めします。これにより、次のようなメリットが得られます。

-   接続とトランザクションを管理するための[定型コード](https://en.wikipedia.org/wiki/Boilerplate_code)を削減します。
-   多数のSQL文の代わりに、データオブジェクトを使用してデータを操作します。

## 次のステップ {#next-steps}

-   mysql-connector-python の使用方法の詳細については[MySQL Connector/Python のドキュメント](https://dev.mysql.com/doc/connector-python/en/)参照してください。
-   [開発者ガイド](https://docs.pingcap.com/developer/)[データを挿入する](/develop/dev-guide-insert-data.md)[データの更新](/develop/dev-guide-update-data.md)、[データを削除する](/develop/dev-guide-delete-data.md)、「SQL パフォーマンス最適化」などの章[単一表の読み取り](/develop/dev-guide-get-data-from-single-table.md)読んで、TiDB アプリケーション [取引](/develop/dev-guide-transaction-overview.md)[SQLパフォーマンス最適化](/develop/dev-guide-optimize-sql-overview.md)。
-   プロフェッショナルな[TiDB開発者向けコース](https://www.pingcap.com/education/)コースを通じて学習し、試験に合格すると[TiDB認定資格](https://www.pingcap.com/education/certification/)を取得します。

## お困りですか？ {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)or [スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに質問してください。
-   [TiDB Cloudのサポートチケットを送信してください](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDB Self-Managedのサポートチケットを送信してください](/support.md)
