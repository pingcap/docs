---
title: Connect to TiDB with SQLAlchemy
summary: SQLAlchemyを使用してTiDBに接続する方法を学びましょう。このチュートリアルでは、SQLAlchemyを使用してTiDBを操作するPythonのサンプルコードを紹介します。
aliases: ['/ja/tidb/dev/dev-guide-outdated-for-sqlalchemy','/ja/tidb/stable/dev-guide-sample-application-python-sqlalchemy/','/ja/tidb/dev/dev-guide-sample-application-python-sqlalchemy/','/ja/tidbcloud/dev-guide-sample-application-python-sqlalchemy/']
---

# SQLAlchemyを使用してTiDBに接続する {#connect-to-tidb-with-sqlalchemy}

TiDBはMySQL互換のデータベースであり、 [SQLAlchemy](https://www.sqlalchemy.org/)は人気の高いPythonのSQLツールキットおよびオブジェクトリレーショナルマッパー（ORM）です。

このチュートリアルでは、TiDBとSQLAlchemyを使用して以下のタスクを実行する方法を学ぶことができます。

-   環境をセットアップしてください。
-   SQLAlchemyを使用してTiDBに接続します。
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
git clone https://github.com/tidb-samples/tidb-python-sqlalchemy-quickstart.git
cd tidb-python-sqlalchemy-quickstart
```

### ステップ2：依存関係をインストールする {#step-2-install-dependencies}

サンプルアプリに必要なパッケージ（SQLAlchemyとPyMySQLを含む）をインストールするには、以下のコマンドを実行してください。

```shell
pip install -r requirements.txt
```

#### PyMySQLを使う理由とは？ {#why-use-pymysql}

SQLAlchemyは、複数のデータベースを扱うORMライブラリです。データベースの高レベルな抽象化を提供することで、開発者がよりオブジェクト指向的な方法でSQL文を記述できるように支援します。ただし、SQLAlchemyにはデータベースドライバは含まれていません。データベースに接続するには、データベースドライバをインストールする必要があります。このサンプルアプリケーションでは、データベースドライバとしてPyMySQLを使用しています。PyMySQLは、TiDBと互換性があり、すべてのプラットフォームにインストール可能な、純粋なPython製のMySQLクライアントライブラリです。

[mysqlclient](https://github.com/PyMySQL/mysqlclient)や[mysql-connector-python](https://dev.mysql.com/doc/connector-python/en/)などの他のデータベース ドライバーを使用することもできます。ただし、これらは純粋な Python ライブラリではなく、コンパイルには対応する C/C++ コンパイラと MySQL クライアントが必要です。詳細については、 [SQLAlchemyの公式ドキュメント](https://docs.sqlalchemy.org/en/20/core/engines.html#mysql)を参照してください。

### ステップ3：接続情報の設定 {#step-3-configure-connection-information}

選択したTiDBのデプロイオプションに応じて、TiDBに接続してください。

<SimpleTab>
<div label="TiDB Cloud Starter or Essential">

> **注記：**
>
> 現在、 TiDB Cloud Starterインスタンスには制限があります。5 分間アクティブな接続がない場合、インスタンスはシャットダウンし、すべての接続が閉じられます。そのため、 TiDB Cloud Starterインスタンスで SQLAlchemy を使用する場合、プールされた接続で`OperationalError`のような`Lost connection to MySQL server during query`や`MySQL Connection not available`発生する可能性があります。このエラーを回避するには、 `pool_recycle`パラメータを`300`に設定してください。詳細については、SQLAlchemy ドキュメントの[接続切れへの対処](https://docs.sqlalchemy.org/en/20/core/pooling.html#dealing-with-disconnects)を参照してください。

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

### ステップ4：コードを実行して結果を確認する {#step-4-run-the-code-and-check-the-result}

1.  サンプルコードを実行するには、以下のコマンドを実行してください。

    ```shell
    python sqlalchemy_example.py
    ```

2.  [期待される出力.txt](https://github.com/tidb-samples/tidb-python-sqlalchemy-quickstart/blob/main/Expected-Output.txt)をチェックして、出力が一致するかどうかを確認してください。

## サンプルコードスニペット {#sample-code-snippets}

以下のサンプルコードスニペットを参考に、独自のアプリケーション開発を完成させてください。

完全なサンプルコードと実行方法については、 [tidb-samples/tidb-python-sqlalchemy-quickstart](https://github.com/tidb-samples/tidb-python-sqlalchemy-quickstart)リポジトリを参照してください。

### TiDBに接続する {#connect-to-tidb}

```python
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker

def get_db_engine():
    connect_args = {}
    if ${ca_path}:
        connect_args = {
            "ssl_verify_cert": True,
            "ssl_verify_identity": True,
            "ssl_ca": ${ca_path},
        }
    return create_engine(
        URL.create(
            drivername="mysql+pymysql",
            username=${tidb_user},
            password=${tidb_password},
            host=${tidb_host},
            port=${tidb_port},
            database=${tidb_db_name},
        ),
        connect_args=connect_args,
    )

engine = get_db_engine()
Session = sessionmaker(bind=engine)
```

この機能を使用する場合は、 `${tidb_host}` 、 `${tidb_port}` 、 `${tidb_user}` 、 `${tidb_password}` 、 `${tidb_db_name}` 、 `${ca_path}` TiDB の実際の値に置き換える必要があります。

### テーブルを定義する {#define-a-table}

```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Player(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(32), unique=True)
    coins = Column(Integer)
    goods = Column(Integer)

    __tablename__ = "players"
```

詳細については、 [SQLAlchemy ドキュメント: 宣言型によるクラスのマッピング](https://docs.sqlalchemy.org/en/20/orm/declarative_mapping.html)検討を参照してください。

### データを挿入する {#insert-data}

```python
with Session() as session:
    player = Player(name="test", coins=100, goods=100)
    session.add(player)
    session.commit()
```

詳細については、[データを挿入する](/develop/dev-guide-insert-data.md)を参照してください。

### クエリデータ {#query-data}

```python
with Session() as session:
    player = session.query(Player).filter_by(name == "test").one()
    print(player)
```

詳細については、 [クエリデータ](/develop/dev-guide-get-data-from-single-table.md)を参照してください。

### データの更新 {#update-data}

```python
with Session() as session:
    player = session.query(Player).filter_by(name == "test").one()
    player.coins = 200
    session.commit()
```

詳細については、[データの更新](/develop/dev-guide-update-data.md)を参照してください。

### データを削除する {#delete-data}

```python
with Session() as session:
    player = session.query(Player).filter_by(name == "test").one()
    session.delete(player)
    session.commit()
```

詳細については、[データを削除する](/develop/dev-guide-delete-data.md)を参照してください。

## 次のステップ {#next-steps}

-   SQLAlchemy の使用法の詳細については[SQLAlchemyのドキュメント](https://www.sqlalchemy.org/)参照してください。
-   [開発者ガイド](https://docs.pingcap.com/developer/)[データを挿入する](/develop/dev-guide-insert-data.md)[データの更新](/develop/dev-guide-update-data.md)、[データを削除する](/develop/dev-guide-delete-data.md)、「SQL パフォーマンス最適化」などの章[単一表の読み取り](/develop/dev-guide-get-data-from-single-table.md)読んで、TiDB アプリケーション [取引](/develop/dev-guide-transaction-overview.md)[SQLパフォーマンス最適化](/develop/dev-guide-optimize-sql-overview.md)。
-   プロフェッショナルな[TiDB開発者向けコース](https://www.pingcap.com/education/)コースを通じて学習し、試験に合格すると[TiDB認定資格](https://www.pingcap.com/education/certification/)を取得します。

## お困りですか？ {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)or [スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに質問してください。
-   [TiDB Cloudのサポートチケットを送信してください](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDB Self-Managedのサポートチケットを送信してください](/support.md)
