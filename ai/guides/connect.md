---
title: Connect to TiDB
summary: pytidb`クライアントを使用してTiDBデータベースに接続する方法を学びましょう。
---

# TiDBに接続する {#connect-to-tidb}

このガイドでは`pytidb`クライアントを使用して TiDB データベースに接続する方法を説明します。

## 依存関係をインストールします {#install-the-dependencies}

[`pytidb`](https://github.com/pingcap/pytidb)は[SQLAlchemy](https://sqlalchemy.org/)をベースにしたPythonクライアントです。生のSQL文を書かずにベクトル埋め込みを保存・検索できる、一連の高レベルAPIを提供します。

Pythonクライアントをインストールするには、次のコマンドを実行してください。

```bash
pip install pytidb
```

## 接続パラメータを使用して接続します。 {#connect-with-connection-parameters}

TiDBの導入タイプに基づいて手順を選択してください。

<SimpleTab>
<div label="TiDB Cloud Starter">

[TiDB Cloud Starterインスタンスを作成する](https://tidbcloud.com/free-trial/)、次のように Web コンソールから接続パラメータを取得できます。

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、次に、対象のTiDB Cloud Starterインスタンスの名前をクリックして、概要ページに移動します。
2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示され、接続パラメータが表示されます。
3.  接続パラメータをコードまたは環境変数にコピーしてください。

サンプルコード：

```python title="main.py"
from pytidb import TiDBClient

db = TiDBClient.connect(
    host="{gateway-region}.prod.aws.tidbcloud.com",
    port=4000,
    username="{prefix}.root",
    password="{password}",
    database="test",
)
```

> **注記：**
>
> TiDB Cloud Starterの場合、パブリック エンドポイントを使用する場合はデータベース[データベースへのTLS接続](https://docs.pingcap.com/tidbcloud/secure-connections-to-starter-clusters/)が必要です。 `pytidb`クライアントは、 TiDB Cloud Starterインスタンスの TLS を**自動的に**有効にします。

</div>
<div label="TiDB Self-Managed">

[TiDBセルフマネージドのクイックスタート](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb/#deploy-a-local-test-cluster)スタートに従って、テスト用にTiDBクラスターをデプロイします。

サンプルコード：

```python title="main.py"
from pytidb import TiDBClient

db = TiDBClient.connect(
    host="{tidb_server_host}",
    port=4000,
    username="root",
    password="{password}",
    database="test",
)
```

> **注記：**
>
> テスト用にTiDBクラスタをデプロイするために`tiup playground`を使用する場合、デフォルトのホストは`127.0.0.1`で、デフォルトのパスワードは空です。

</div>
</SimpleTab>

接続が完了すると、 `db`オブジェクトを使用して、テーブルの操作、データのクエリなどを行うことができます。

## 接続文字列を使用して接続します。 {#connect-with-connection-string}

接続文字列（データベースURL）を使用する場合は、デプロイメントの種類に応じて以下の形式に従ってください。

<SimpleTab>
<div label="TiDB Cloud Starter">

[TiDB Cloud Starterインスタンスを作成する](https://tidbcloud.com/free-trial/)、次のように Web コンソールから接続パラメータを取得できます。

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、次に、対象のTiDB Cloud Starterインスタンスの名前をクリックして、概要ページに移動します。
2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示され、接続パラメータが一覧表示されます。
3.  接続パラメータをコピーし、以下の形式で接続文字列を作成してください。

```python title="main.py"
from pytidb import TiDBClient

db = TiDBClient.connect(
    database_url="mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}?ssl_verify_cert=true&ssl_verify_identity=true",
)
```

> **注記：**
>
> TiDB Cloud Starterの場合、パブリック エンドポイントを使用する場合はデータベース[データベースへのTLS接続](https://docs.pingcap.com/tidbcloud/secure-connections-to-starter-clusters/)が必要となるため、接続文字列に`ssl_verify_cert=true&ssl_verify_identity=true`を設定する必要があります。

</div>
<div label="TiDB Self-Managed">

接続文字列を作成するには、以下の形式に従ってください。

```python title="main.py"
from pytidb import TiDBClient

db = TiDBClient.connect(
    database_url="mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}",
)
```

> **注記：**
>
> `tiup playground`を使用してテスト用のTiDBクラスタをデプロイする場合、接続文字列は次のとおりです。
>
>     mysql+pymysql://root:@127.0.0.1:4000/test

</div>
</SimpleTab>

## SQLAlchemy DBエンジンに接続する {#connect-with-sqlalchemy-db-engine}

アプリケーションに既に SQLAlchemy データベース エンジンが搭載されている場合は、 `db_engine`パラメータを使用してそれを再利用できます。

```python title="main.py"
from pytidb import TiDBClient

db = TiDBClient(db_engine=db_engine)
```

## 次のステップ {#next-steps}

TiDBデータベースに接続後、以下のガイドを参照してデータの操作方法を学ぶことができます。

-   [テーブルの操作](/ai/guides/tables.md): TiDB でテーブルを定義および管理する方法を学びます。
-   [ベクトル検索](/ai/guides/vector-search.md): ベクトル埋め込みを使用してセマンティック検索を実行します。
-   [全文検索](/ai/guides/vector-search-full-text-search-python.md): キーワードベースの検索を使用してドキュメントを取得します。
-   [ハイブリッド検索](/ai/guides/vector-search-hybrid-search.md): ベクトル検索と全文検索を組み合わせて、より関連性の高い結果を取得します。
