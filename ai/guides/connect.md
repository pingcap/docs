---
title: Connect to TiDB
summary: pytidb` クライアントを使用して TiDB データベースに接続する方法を学習します。
---

# TiDBに接続する {#connect-to-tidb}

このガイドでは、 `pytidb`クライアントを使用して TiDB データベースに接続する方法を説明します。

## 依存関係をインストールする {#install-the-dependencies}

[`pytidb`](https://github.com/pingcap/pytidb)は[SQLアルケミー](https://sqlalchemy.org/)ベースに構築された Python クライアントです。生の SQL を書かずにベクトル埋め込みを保存および検索するための一連の高レベル API を提供します。

Python クライアントをインストールするには、次のコマンドを実行します。

```bash
pip install pytidb
```

## 接続パラメータを使用して接続する {#connect-with-connection-parameters}

TiDB の展開タイプに基づいて手順を選択します。

<SimpleTab>
<div label="TiDB Cloud Starter">

[TiDB Cloud Starterクラスターを作成する](https://tidbcloud.com/free-trial/)実行してから、次のように Web コンソールから接続パラメータを取得できます。

1.  [クラスターページ](https://tidbcloud.com/clusters)に移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。
2.  右上隅の**「接続」**をクリックします。接続パラメータがリストされた接続ダイアログが表示されます。
3.  接続パラメータをコードまたは環境変数にコピーします。

コード例:

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
> TiDB Cloud Starterでは、パブリックエンドポイントを使用する場合は[データベースへのTLS接続](https://docs.pingcap.com/tidbcloud/secure-connections-to-starter-clusters/)必要です。3クライアント`pytidb` 、TiDB Cloud StarterクラスターのTLSを**自動的に**有効化します。

</div>
<div label="TiDB Self-Managed">

テスト用に TiDB クラスターをデプロイするには、手順[TiDBセルフマネージドのクイックスタート](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb/#deploy-a-local-test-cluster)に従います。

コード例:

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
> テスト用に TiDB クラスターをデプロイするために`tiup playground`使用している場合、デフォルトのホストは`127.0.0.1`で、デフォルトのパスワードは空です。

</div>
</SimpleTab>

接続すると、 `db`オブジェクトを使用してテーブルを操作したり、データを照会したりできるようになります。

## 接続文字列で接続する {#connect-with-connection-string}

接続文字列 (データベース URL) を使用する場合は、展開タイプに応じて次の形式に従います。

<SimpleTab>
<div label="TiDB Cloud Starter">

[TiDB Cloud Starterクラスターを作成する](https://tidbcloud.com/free-trial/)実行してから、次のように Web コンソールから接続パラメータを取得できます。

1.  [クラスターページ](https://tidbcloud.com/clusters)に移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。
2.  右上隅の**「接続」**をクリックします。接続パラメータがリストされた接続ダイアログが表示されます。
3.  接続パラメータをコピーし、次の形式で接続文字列を作成します。

```python title="main.py"
from pytidb import TiDBClient

db = TiDBClient.connect(
    database_url="mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}?ssl_verify_cert=true&ssl_verify_identity=true",
)
```

> **注記：**
>
> TiDB Cloud Starter の場合、パブリック エンドポイントを使用する場合は[データベースへのTLS接続](https://docs.pingcap.com/tidbcloud/secure-connections-to-starter-clusters/)必要なので、接続文字列に`ssl_verify_cert=true&ssl_verify_identity=true`設定する必要があります。

</div>
<div label="TiDB Self-Managed">

接続文字列を構築するには、以下の形式に従います。

```python title="main.py"
from pytidb import TiDBClient

db = TiDBClient.connect(
    database_url="mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}",
)
```

> **注記：**
>
> `tiup playground`使用してテスト用の TiDB クラスターをデプロイする場合、接続文字列は次のようになります。
>
>     mysql+pymysql://root:@127.0.0.1:4000/test

</div>
</SimpleTab>

## SQLAlchemy DBエンジンに接続する {#connect-with-sqlalchemy-db-engine}

アプリケーションにすでに SQLAlchemy データベース エンジンがある場合は、 `db_engine`パラメータを使用してそれを再利用できます。

```python title="main.py"
from pytidb import TiDBClient

db = TiDBClient(db_engine=db_engine)
```

## 次のステップ {#next-steps}

TiDB データベースに接続したら、次のガイドを参照してデータの操作方法を学習できます。

-   [表の操作](/ai/guides/tables.md) : TiDB でテーブルを定義および管理する方法を学習します。
-   [ベクトル検索](/ai/guides/vector-search.md) : ベクトル埋め込みを使用してセマンティック検索を実行します。
-   [全文検索](/ai/guides/vector-search-full-text-search-python.md) : キーワードベースの検索を使用してドキュメントを取得します。
-   [ハイブリッド検索](/ai/guides/vector-search-hybrid-search.md) : ベクトル検索と全文検索を組み合わせて、より関連性の高い結果を取得します。
