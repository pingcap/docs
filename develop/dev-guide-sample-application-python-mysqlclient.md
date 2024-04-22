---
title: Connect to TiDB with mysqlclient
summary: TiDBはMySQL互換データベースであり、mysqlクライアントはPython用の人気のあるオープンソースドライバーです。このチュートリアルでは、TiDBとmysqlclientを使用して環境をセットアップし、TiDBクラスターに接続し、アプリケーションをビルドして実行する方法を学習できます。また、サンプルコードスニペットを提供しています。前提条件としてPython 3.10以降、ギット、TiDBクラスターが必要です。詳細については、TiDB公式ドキュメントを参照してください。
---

# mysqlclient を使用して TiDB に接続する {#connect-to-tidb-with-mysqlclient}

TiDB は MySQL 互換データベースであり、 [mysqlクライアント](https://github.com/PyMySQL/mysqlclient)は Python 用の人気のあるオープンソース ドライバーです。

このチュートリアルでは、TiDB と mysqlclient を使用して次のタスクを実行する方法を学習できます。

-   環境をセットアップします。
-   mysqlclient を使用して TiDB クラスターに接続します。
-   アプリケーションをビルドして実行します。オプションで、基本的な CRUD 操作のサンプル コード スニペットを見つけることができます。

> **注記：**
>
> このチュートリアルは、TiDB サーバーレス、TiDB 専用、および TiDB セルフホストで動作します。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、次のものが必要です。

-   [Python **3.10**以降](https://www.python.org/downloads/) 。
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
git clone https://github.com/tidb-samples/tidb-python-mysqlclient-quickstart.git
cd tidb-python-mysqlclient-quickstart;
```

### ステップ 2: 依存関係をインストールする {#step-2-install-dependencies}

次のコマンドを実行して、サンプル アプリに必要なパッケージ ( `mysqlclient`を含む) をインストールします。

```shell
pip install -r requirements.txt
```

インストールの問題が発生した場合は、 [mysqlclientの公式ドキュメント](https://github.com/PyMySQL/mysqlclient#install)を参照してください。

### ステップ 3: 接続情報を構成する {#step-3-configure-connection-information}

選択した TiDB デプロイメント オプションに応じて、TiDB クラスターに接続します。

<SimpleTab>
<div label="TiDB Serverless">

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして、その概要ページに移動します。

2.  右上隅にある**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログの設定が動作環境と一致していることを確認してください。

    -   **エンドポイント タイプは**`Public`に設定されます

    -   **ブランチは**`main`に設定されています

    -   **[接続先] は**`General`に設定されています

    -   **オペレーティング システムが**環境に一致します。

    > **ヒント：**
    >
    > プログラムが Windows Subsystem for Linux (WSL) で実行されている場合は、対応する Linux ディストリビューションに切り替えます。

4.  **「パスワードの生成」**をクリックして、ランダムなパスワードを作成します。

    > **ヒント：**
    >
    > 以前にパスワードを作成したことがある場合は、元のパスワードを使用するか、 **「パスワードのリセット」**をクリックして新しいパスワードを生成できます。

5.  次のコマンドを実行して`.env.example`をコピーし、名前を`.env`に変更します。

    ```shell
    cp .env.example .env
    ```

6.  対応する接続​​文字列をコピーして`.env`ファイルに貼り付けます。結果の例は次のとおりです。

    ```dotenv
    TIDB_HOST='{gateway-region}.aws.tidbcloud.com'
    TIDB_PORT='4000'
    TIDB_USER='{prefix}.root'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    CA_PATH=''
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
    TIDB_HOST='{host}.clusters.tidb-cloud.com'
    TIDB_PORT='4000'
    TIDB_USER='{username}'
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

### ステップ 4: コードを実行して結果を確認する {#step-4-run-the-code-and-check-the-result}

1.  次のコマンドを実行してサンプル コードを実行します。

    ```shell
    python mysqlclient_example.py
    ```

2.  [予想される出力.txt](https://github.com/tidb-samples/tidb-python-mysqlclient-quickstart/blob/main/Expected-Output.txt)チェックして、出力が一致するかどうかを確認します。

## サンプルコードスニペット {#sample-code-snippets}

次のサンプル コード スニペットを参照して、独自のアプリケーション開発を完了できます。

完全なサンプル コードとその実行方法については、 [tidb-samples/tidb-python-mysqlclient-quickstart](https://github.com/tidb-samples/tidb-python-mysqlclient-quickstart)リポジトリを確認してください。

### TiDB に接続する {#connect-to-tidb}

```python
def get_mysqlclient_connection(autocommit:bool=True) -> MySQLdb.Connection:
    db_conf = {
        "host": ${tidb_host},
        "port": ${tidb_port},
        "user": ${tidb_user},
        "password": ${tidb_password},
        "database": ${tidb_db_name},
        "autocommit": autocommit
    }

    if ${ca_path}:
        db_conf["ssl_mode"] = "VERIFY_IDENTITY"
        db_conf["ssl"] = {"ca": ${ca_path}}

    return MySQLdb.connect(**db_conf)
```

この関数を使用する場合、 `${tidb_host}` 、 `${tidb_port}` 、 `${tidb_user}` 、 `${tidb_password}` 、 `${tidb_db_name}`および`${ca_path}`を TiDB クラスターの実際の値に置き換える必要があります。

### データの挿入 {#insert-data}

```python
with get_mysqlclient_connection(autocommit=True) as conn:
    with conn.cursor() as cur:
        player = ("1", 1, 1)
        cursor.execute("INSERT INTO players (id, coins, goods) VALUES (%s, %s, %s)", player)
```

詳細については、 [データの挿入](/develop/dev-guide-insert-data.md)を参照してください。

### クエリデータ {#query-data}

```python
with get_mysqlclient_connection(autocommit=True) as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT count(*) FROM players")
        print(cur.fetchone()[0])
```

詳細については、 [クエリデータ](/develop/dev-guide-get-data-from-single-table.md)を参照してください。

### データを更新する {#update-data}

```python
with get_mysqlclient_connection(autocommit=True) as conn:
    with conn.cursor() as cur:
        player_id, amount, price="1", 10, 500
        cursor.execute(
            "UPDATE players SET goods = goods + %s, coins = coins + %s WHERE id = %s",
            (-amount, price, player_id),
        )
```

詳細については、 [データを更新する](/develop/dev-guide-update-data.md)を参照してください。

### データの削除 {#delete-data}

```python
with get_mysqlclient_connection(autocommit=True) as conn:
    with conn.cursor() as cur:
        player_id = "1"
        cursor.execute("DELETE FROM players WHERE id = %s", (player_id,))
```

詳細については、 [データの削除](/develop/dev-guide-delete-data.md)を参照してください。

## 便利なメモ {#useful-notes}

### ドライバーまたは ORM フレームワークを使用していますか? {#using-driver-or-orm-framework}

Python ドライバーはデータベースへの低レベルのアクセスを提供しますが、開発者は次のことを行う必要があります。

-   データベース接続を手動で確立および解放します。
-   データベーストランザクションを手動で管理します。
-   データ行 ( `mysqlclient`ではタプルとして表されます) をデータ オブジェクトに手動でマップします。

複雑な SQL ステートメントを作成する必要がない限り、開発には[SQLアルケミー](/develop/dev-guide-sample-application-python-sqlalchemy.md) 、 [ピーウィー](/develop/dev-guide-sample-application-python-peewee.md) 、Django ORM などの[ORM](https://en.wikipedia.org/w/index.php?title=Object-relational_mapping)フレームワークを使用することをお勧めします。それはあなたに役立ちます:

-   接続とトランザクションの管理のために[定型コード](https://en.wikipedia.org/wiki/Boilerplate_code)を減らします。
-   多数の SQL ステートメントの代わりにデータ オブジェクトを使用してデータを操作します。

## 次のステップ {#next-steps}

-   `mysqlclient`から[mysqlclientのドキュメント](https://mysqlclient.readthedocs.io/)の使用法をさらに学習します。
-   TiDB アプリケーション開発の[SQLパフォーマンスの最適化](/develop/dev-guide-optimize-sql-overview.md)プラクティスについて[取引](/develop/dev-guide-transaction-overview.md) 、 [開発者ガイド](/develop/dev-guide-overview.md)の章 ( [データの挿入](/develop/dev-guide-insert-data.md)など) [データを更新する](/develop/dev-guide-update-data.md)参照[データの削除](/develop/dev-guide-delete-data.md) [単一テーブルの読み取り](/develop/dev-guide-get-data-from-single-table.md)ください。
-   プロフェッショナルとして[TiDB 開発者コース](https://www.pingcap.com/education/)を学び、試験合格後に[TiDB 認定](https://www.pingcap.com/education/certification/)獲得します。

## 助けが必要？ {#need-help}

<CustomContent platform="tidb">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[サポートチケットを作成する](/support.md)について質問してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[サポートチケットを作成する](https://support.pingcap.com/)について質問してください。

</CustomContent>
