---
title: Connect to TiDB with mysqlclient
summary: mysqlclient を使用して TiDB に接続する方法を学びます。このチュートリアルでは、mysqlclient を使用して TiDB を操作する Python サンプル コード スニペットを示します。
---

# mysqlclientでTiDBに接続する {#connect-to-tidb-with-mysqlclient}

TiDB は MySQL 互換のデータベースであり、 [mysqlクライアント](https://github.com/PyMySQL/mysqlclient) Python 用の人気のあるオープンソース ドライバーです。

このチュートリアルでは、TiDB と mysqlclient を使用して次のタスクを実行する方法を学習します。

-   環境を設定します。
-   mysqlclient を使用して TiDB クラスターに接続します。
-   アプリケーションをビルドして実行します。オプションで、基本的な CRUD 操作のサンプル コード スニペットを見つけることができます。

> **注記：**
>
> このチュートリアルは、 TiDB Cloud Serverless、 TiDB Cloud Dedicated、および TiDB Self-Managed で機能します。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、次のものが必要です。

-   [Python **3.10**以上](https://www.python.org/downloads/) 。
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

このセクションでは、サンプル アプリケーション コードを実行して TiDB に接続する方法を示します。

### ステップ1: サンプルアプリのリポジトリをクローンする {#step-1-clone-the-sample-app-repository}

サンプル コード リポジトリを複製するには、ターミナル ウィンドウで次のコマンドを実行します。

```shell
git clone https://github.com/tidb-samples/tidb-python-mysqlclient-quickstart.git
cd tidb-python-mysqlclient-quickstart;
```

### ステップ2: 依存関係をインストールする {#step-2-install-dependencies}

次のコマンドを実行して、サンプル アプリに必要なパッケージ ( `mysqlclient`を含む) をインストールします。

```shell
pip install -r requirements.txt
```

インストールで問題が発生した場合は、 [mysqlclient 公式ドキュメント](https://github.com/PyMySQL/mysqlclient#install)を参照してください。

### ステップ3: 接続情報を構成する {#step-3-configure-connection-information}

選択した TiDB デプロイメント オプションに応じて、TiDB クラスターに接続します。

<SimpleTab>
<div label="TiDB Cloud Serverless">

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログの構成が動作環境と一致していることを確認します。

    -   **接続タイプ**は`Public`に設定されています

    -   **ブランチは**`main`に設定されています

    -   **接続先は**`General`に設定されています

    -   **オペレーティング システムは**環境に適合します。

    > **ヒント：**
    >
    > プログラムが Windows Subsystem for Linux (WSL) で実行されている場合は、対応する Linux ディストリビューションに切り替えます。

4.  ランダムなパスワードを作成するには、 **「パスワードの生成」**をクリックします。

    > **ヒント：**
    >
    > 以前にパスワードを作成したことがある場合は、元のパスワードを使用するか、 **「パスワードのリセット」**をクリックして新しいパスワードを生成することができます。

5.  次のコマンドを実行して`.env.example`コピーし、名前を`.env`に変更します。

    ```shell
    cp .env.example .env
    ```

6.  対応する接続文字列をコピーして`.env`ファイルに貼り付けます。例の結果は次のようになります。

    ```dotenv
    TIDB_HOST='{gateway-region}.aws.tidbcloud.com'
    TIDB_PORT='4000'
    TIDB_USER='{prefix}.root'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    CA_PATH=''
    ```

    プレースホルダー`{}` 、接続ダイアログから取得した接続パラメータに必ず置き換えてください。

    TiDB Cloud Serverless には安全な接続が必要です。 mysqlclient の`ssl_mode`はデフォルトで`PREFERRED`になっているため、 `CA_PATH`手動で指定する必要はありません。空のままにしておきます。ただし、特別な理由により`CA_PATH`手動で指定する必要がある場合は、 [TiDB Cloud ServerlessへのTLS接続](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-clusters)を参照して、さまざまなオペレーティング システムの証明書パスを取得できます。

7.  `.env`ファイルを保存します。

</div>
<div label="TiDB Cloud Dedicated">

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログで、 **[接続タイプ]**ドロップダウン リストから**[パブリック]**を選択し、 **[CA 証明書]**をクリックして CA 証明書をダウンロードします。

    IP アクセス リストを設定していない場合は、 **「IP アクセス リストの設定」**をクリックするか、手順[IPアクセスリストを構成する](https://docs.pingcap.com/tidbcloud/configure-ip-access-list)に従って最初の接続の前に設定してください。

    **パブリック**接続タイプに加えて、TiDB Dedicated は**プライベートエンドポイント**と**VPC ピアリング**接続タイプもサポートしています。詳細については、 [TiDB専用クラスタに接続する](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)参照してください。

4.  次のコマンドを実行して`.env.example`コピーし、名前を`.env`に変更します。

    ```shell
    cp .env.example .env
    ```

5.  対応する接続文字列をコピーして`.env`ファイルに貼り付けます。例の結果は次のようになります。

    ```dotenv
    TIDB_HOST='{host}.clusters.tidb-cloud.com'
    TIDB_PORT='4000'
    TIDB_USER='{username}'
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

2.  対応する接続文字列をコピーして`.env`ファイルに貼り付けます。例の結果は次のようになります。

    ```dotenv
    TIDB_HOST='{tidb_server_host}'
    TIDB_PORT='4000'
    TIDB_USER='root'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    ```

    プレースホルダー`{}`接続パラメータに置き換え、 `CA_PATH`行を削除してください。TiDB をローカルで実行している場合、デフォルトのホスト アドレスは`127.0.0.1`で、パスワードは空です。

3.  `.env`ファイルを保存します。

</div>
</SimpleTab>

### ステップ4: コードを実行して結果を確認する {#step-4-run-the-code-and-check-the-result}

1.  サンプル コードを実行するには、次のコマンドを実行します。

    ```shell
    python mysqlclient_example.py
    ```

2.  [予想される出力.txt](https://github.com/tidb-samples/tidb-python-mysqlclient-quickstart/blob/main/Expected-Output.txt)をチェックして、出力が一致するかどうかを確認します。

## サンプルコードスニペット {#sample-code-snippets}

次のサンプル コード スニペットを参照して、独自のアプリケーション開発を完了することができます。

完全なサンプル コードとその実行方法については、 [tidb-samples/tidb-python-mysqlclient-クイックスタート](https://github.com/tidb-samples/tidb-python-mysqlclient-quickstart)リポジトリを参照してください。

### TiDBに接続する {#connect-to-tidb}

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

この関数を使用する場合は、 `${tidb_host}` 、 `${tidb_port}` 、 `${tidb_user}` 、 `${tidb_password}` 、 `${tidb_db_name}` 、 `${ca_path}`を TiDB クラスターの実際の値に置き換える必要があります。

### データを挿入 {#insert-data}

```python
with get_mysqlclient_connection(autocommit=True) as conn:
    with conn.cursor() as cur:
        player = ("1", 1, 1)
        cursor.execute("INSERT INTO players (id, coins, goods) VALUES (%s, %s, %s)", player)
```

詳細については[データを挿入](/develop/dev-guide-insert-data.md)を参照してください。

### クエリデータ {#query-data}

```python
with get_mysqlclient_connection(autocommit=True) as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT count(*) FROM players")
        print(cur.fetchone()[0])
```

詳細については[クエリデータ](/develop/dev-guide-get-data-from-single-table.md)を参照してください。

### データの更新 {#update-data}

```python
with get_mysqlclient_connection(autocommit=True) as conn:
    with conn.cursor() as cur:
        player_id, amount, price="1", 10, 500
        cursor.execute(
            "UPDATE players SET goods = goods + %s, coins = coins + %s WHERE id = %s",
            (-amount, price, player_id),
        )
```

詳細については[データの更新](/develop/dev-guide-update-data.md)を参照してください。

### データを削除する {#delete-data}

```python
with get_mysqlclient_connection(autocommit=True) as conn:
    with conn.cursor() as cur:
        player_id = "1"
        cursor.execute("DELETE FROM players WHERE id = %s", (player_id,))
```

詳細については[データを削除する](/develop/dev-guide-delete-data.md)を参照してください。

## 役に立つメモ {#useful-notes}

### ドライバーまたは ORM フレームワークを使用していますか? {#using-driver-or-orm-framework}

Python ドライバーはデータベースへの低レベル アクセスを提供しますが、開発者は次の作業を行う必要があります。

-   データベース接続を手動で確立および解放します。
-   データベース トランザクションを手動で管理します。
-   データ行 ( `mysqlclient`ではタプルとして表される) をデータ オブジェクトに手動でマップします。

複雑な SQL 文を書く必要がない限り、開発には[SQLアルケミー](/develop/dev-guide-sample-application-python-sqlalchemy.md) 、 [ピーウィー](/develop/dev-guide-sample-application-python-peewee.md) 、 Django ORM などの[ORM](https://en.wikipedia.org/w/index.php?title=Object-relational_mapping)フレームワークを使用することをお勧めします。次のことに役立ちます。

-   接続とトランザクションを管理するために[定型コード](https://en.wikipedia.org/wiki/Boilerplate_code)減らします。
-   多数の SQL ステートメントの代わりにデータ オブジェクトを使用してデータを操作します。

## 次のステップ {#next-steps}

-   [mysqlclientのドキュメント](https://mysqlclient.readthedocs.io/)から`mysqlclient`の使用法について詳しく学びます。
-   [開発者ガイド](/develop/dev-guide-overview.md)の[データを挿入](/develop/dev-guide-insert-data.md) 、 [データの更新](/develop/dev-guide-update-data.md) 、 [データを削除する](/develop/dev-guide-delete-data.md) 、 [単一テーブル読み取り](/develop/dev-guide-get-data-from-single-table.md) 、 [取引](/develop/dev-guide-transaction-overview.md) 、 [SQLパフォーマンスの最適化](/develop/dev-guide-optimize-sql-overview.md)などの章で、 TiDB アプリケーション開発のベスト プラクティスを学習します。
-   プロフェッショナル[TiDB 開発者コース](https://www.pingcap.com/education/)を通じて学び、試験に合格すると[TiDB 認定](https://www.pingcap.com/education/certification/)獲得します。

## ヘルプが必要ですか? {#need-help}

<CustomContent platform="tidb">

[TiDB コミュニティ](https://ask.pingcap.com/) 、または[サポートチケットを作成する](/support.md)について質問します。

</CustomContent>

<CustomContent platform="tidb-cloud">

[TiDB コミュニティ](https://ask.pingcap.com/) 、または[サポートチケットを作成する](https://support.pingcap.com/)について質問します。

</CustomContent>
