---
title: Get Started with TiDB + AI via Python
summary: Python SDKを使用してTiDBでベクトル検索を開始する方法を学びましょう。
aliases: ['/ja/tidb/stable/vector-search-get-started-using-python/','/ja/tidb/dev/vector-search-get-started-using-python/','/ja/tidbcloud/vector-search-get-started-using-python/']
---

# Python を使って TiDB + AI を始めよう {#get-started-with-tidb-ai-via-python}

このドキュメントでは、Python SDK を使用して TiDB で[ベクトル検索](/ai/concepts/vector-search-overview.md)開始する方法を説明します。手順に従って、TiDB で動作する最初の AI アプリケーションを構築します。

このドキュメントに従うことで、以下のことを学ぶことができます。

-   TiDB Python SDKを使用してTiDBに接続します。
-   一般的な埋め込みモデルを使用してテキスト埋め込みを生成します。
-   ベクトルをTiDBテーブルに格納します。
-   ベクトル類似度を用いて意味検索を実行する。

> **注記：**
>
> -   ベクトル検索機能はベータ版であり、予告なく変更される場合があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)報告してください。
> -   ベクトル検索機能は、 [TiDBセルフマネージド](/overview.md)[TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter) 、 [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) 、および[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)で利用できます。TiDB Self-ManagedおよびTiDB Cloud Dedicatedの場合、TiDBのバージョンはv8.4.0以降である必要があります（v8.5.0以降を推奨）。

## 前提条件 {#prerequisites}

-   [tidbcloud.com](https://tidbcloud.com/)にアクセスしてTiDB Cloud Starterインスタンスを無料で作成するか、 [ティアップ遊び場](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb/#deploy-a-local-test-cluster)を使用してローカル テスト用の TiDB 自己管理クラスターをデプロイします。

## インストール {#installation}

[pytidb](https://github.com/pingcap/pytidb)はTiDBの公式Python SDKであり、開発者がAIアプリケーションを効率的に構築できるよう設計されています。

Python SDKをインストールするには、次のコマンドを実行してください。

```bash
pip install pytidb
```

組み込みの埋め込み機能を使用するには、 `models`拡張機能をインストールしてください（代替案）：

```bash
pip install "pytidb[models]"
```

## データベースに接続します {#connect-to-database}

<SimpleTab>
<div label="TiDB Cloud Starter">

これらの接続パラメータは[TiDB Cloudコンソール](https://tidbcloud.com/tidbs)から取得できます。

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、次に、対象のTiDB Cloud Starterインスタンスの名前をクリックして、概要ページに移動します。
2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示され、接続パラメータが表示されます。

例えば、接続パラメータが以下のように表示される場合：

```text
HOST:     gateway01.us-east-1.prod.shared.aws.tidbcloud.com
PORT:     4000
USERNAME: 4EfqPF23YKBxaQb.root
PASSWORD: abcd1234
DATABASE: test
CA:       /etc/ssl/cert.pem
```

TiDB Cloud Starterインスタンスに接続するための対応するPythonコードは以下のとおりです。

```python
from pytidb import TiDBClient

client = TiDBClient.connect(
    host="gateway01.us-east-1.prod.shared.aws.tidbcloud.com",
    port=4000,
    username="4EfqPF23YKBxaQb.root",
    password="abcd1234",
    database="test",
)
```

> **注記：**
>
> 上記の例はあくまでも説明のためのものです。パラメータにはご自身の値を入力し、安全に保管してください。

</div>
<div label="TiDB Self-Managed">

TiDBセルフマネージドクラスタに接続するための基本的な例を以下に示します。

```python
from pytidb import TiDBClient

client = TiDBClient.connect(
    host="localhost",
    port=4000,
    username="root",
    password="",
    database="test",
    ensure_db=True,
)
```

> **注記：**
>
> 実際の導入環境に合わせて、接続パラメータを必ず更新してください。

</div>
</SimpleTab>

接続が完了すると、 `client`オブジェクトを使用して、テーブルの操作、データのクエリなどを行うことができます。

## 埋め込み関数を作成する {#create-an-embedding-function}

[埋め込みモデル](/ai/concepts/vector-search-overview.md#embedding-model)扱う場合、埋め込み機能を利用することで、挿入時とクエリ時の両方でデータを自動的にベクトル化できます。OpenAI、Jina AI、Hugging Face、Sentence Transformersなど、人気の埋め込みモデルをネイティブでサポートしています。

<SimpleTab>
<div label="OpenAI">

[OpenAIプラットフォーム](https://platform.openai.com/api-keys)に移動して、埋め込み用の API キーを作成します。

```python
from pytidb.embeddings import EmbeddingFunction

text_embed = EmbeddingFunction(
    model_name="openai/text-embedding-3-small",
    api_key="<your-openai-api-key>",
)
```

</div>
<div label="Jina AI">

埋め込み用のAPIキーを作成するには、[ジナAI](https://jina.ai/embeddings/)にアクセスしてください。

```python
from pytidb.embeddings import EmbeddingFunction

text_embed = EmbeddingFunction(
    model_name="jina/jina-embeddings-v3",
    api_key="<your-jina-api-key>",
)
```

</div>
</SimpleTab>

## テーブルを作成する {#create-a-table}

例として、 `chunks`という名前のテーブルを作成し、以下の列を追加します。

-   `id` (int): チャンクのID。
-   `text` (テキスト): チャンクのテキストコンテンツ。
-   `text_vec` (ベクトル): テキストのベクトル埋め込み。
-   `user_id` (int): チャンクを作成したユーザーのID。

```python hl_lines="6"
from pytidb.schema import TableModel, Field, VectorField

class Chunk(TableModel):
    id: int | None = Field(default=None, primary_key=True)
    text: str = Field()
    text_vec: list[float] = text_embed.VectorField(source_field="text")
    user_id: int = Field()

table = client.create_table(schema=Chunk, if_exists="overwrite")
```

作成後は、 `table`オブジェクトを使用して、データの挿入、データの検索などを行うことができます。

## データを挿入する {#insert-data}

それでは、サンプルデータをテーブルに追加してみましょう。

```python
table.bulk_insert([
    # 👇 The text will be automatically embedded and populated into the `text_vec` field.
    Chunk(text="PyTiDB is a Python library for developers to connect to TiDB.", user_id=2),
    Chunk(text="LlamaIndex is a framework for building AI applications.", user_id=2),
    Chunk(text="OpenAI is a company and platform that provides AI models service and tools.", user_id=3),
])
```

## 近隣住民を検索 {#search-for-nearest-neighbors}

指定されたクエリの最近傍を検索するには、 `table.search()`メソッドを使用できます。このメソッドは、 デフォルトで[ベクトル検索](/ai/guides/vector-search.md)実行します。

```python
table.search(
    # 👇 Pass the query text directly, it will be embedded to a query vector automatically.
    "A library for my artificial intelligence software"
)
.limit(3).to_list()
```

この例では、ベクトル検索はクエリベクトル`text_vec`テーブルの`chunks`フィールドに格納されているベクトルと比較し、類似度スコアに基づいて意味的に最も関連性の高い上位3つの結果を返します。

`_distance`が近いほど、2 つのベクトルはより類似していることを意味します。

```json title="Expected output"
[
    {
        'id': 2,
        'text': 'LlamaIndex is a framework for building AI applications.',
        'text_vec': [...],
        'user_id': 2,
        '_distance': 0.5719928358786761,
        '_score': 0.4280071641213239
    },
    {
        'id': 3,
        'text': 'OpenAI is a company and platform that provides AI models service and tools.',
        'text_vec': [...],
        'user_id': 3,
        '_distance': 0.603133726213383,
        '_score': 0.396866273786617
    },
    {
        'id': 1,
        'text': 'PyTiDB is a Python library for developers to connect to TiDB.',
        'text_vec': [...],
        'user_id': 2,
        '_distance': 0.6202191842385758,
        '_score': 0.3797808157614242
    }
]
```

## データを削除する {#delete-data}

テーブルから特定の行を削除するには、 `table.delete()`メソッドを使用できます。

```python
table.delete({
    "id": 1
})
```

## ドロップテーブル {#drop-table}

テーブルが不要になった場合は、 `client.drop_table()`メソッドを使用して削除できます。

```python
client.drop_table("chunks")
```

## 次のステップ {#next-steps}

-   TiDB の[ベクトル検索](/ai/guides/vector-search.md)、 [全文検索](/ai/guides/vector-search-full-text-search-python.md)、 [ハイブリッド検索](/ai/guides/vector-search-hybrid-search.md)の詳細については、こちらをご覧ください。
