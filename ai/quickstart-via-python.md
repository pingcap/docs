---
title: Get Started with TiDB + AI via Python
summary: Python SDK を使用して TiDB でベクトル検索を開始する方法を学びます。
aliases: ['/ja/tidb/stable/vector-search-get-started-using-python/','/ja/tidbcloud/vector-search-get-started-using-python/']
---

# PythonでTiDB + AIを使い始める {#get-started-with-tidb-ai-via-python}

このドキュメントでは、Python SDKを使用してTiDBで[ベクトル検索](/ai/concepts/vector-search-overview.md)始める方法を説明します。このドキュメントに沿って、TiDBを使った最初のAIアプリケーションを構築しましょう。

このドキュメントに従うことで、次の方法を学習できます。

-   TiDB Python SDK を使用して TiDB に接続します。
-   一般的な埋め込みモデルを使用してテキスト埋め込みを生成します。
-   ベクトルを TiDB テーブルに保存します。
-   ベクトル類似度を使用してセマンティック検索を実行します。

> **注記：**
>
> -   ベクター検索機能はベータ版であり、予告なく変更される可能性があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)報告を行ってください。
> -   ベクトル検索機能は[TiDBセルフマネージド](/overview.md) 、 [TiDB Cloudスターター](/tidb-cloud/select-cluster-tier.md#starter) 、 [TiDB Cloudエッセンシャル](/tidb-cloud/select-cluster-tier.md#essential) 、 [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)で利用可能です。TiDB Self-ManagedおよびTiDB Cloud Dedicatedの場合、TiDBバージョンはv8.4.0以降である必要があります（v8.5.0以降を推奨）。

## 前提条件 {#prerequisites}

-   [tidbcloud.com](https://tidbcloud.com/)に進み、 TiDB Cloud Starter クラスターを無料で作成するか、 [ティアップ遊び場](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb/#deploy-a-local-test-cluster)使用して、ローカル テスト用に TiDB Self-Managed クラスターをデプロイします。

## インストール {#installation}

[pytidb](https://github.com/pingcap/pytidb)は、開発者が AI アプリケーションを効率的に構築できるように設計されています。

Python SDK をインストールするには、次のコマンドを実行します。

```bash
pip install pytidb
```

組み込みの埋め込み機能を使用するには、 `models`拡張機能（代替）をインストールします。

```bash
pip install "pytidb[models]"
```

## データベースに接続する {#connect-to-database}

<SimpleTab>
<div label="TiDB Cloud Starter">

これらの接続パラメータは[TiDB Cloudコンソール](https://tidbcloud.com/clusters)から取得できます。

1.  [クラスターページ](https://tidbcloud.com/clusters)に移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。
2.  右上隅の**「接続」**をクリックします。接続パラメータがリストされた接続ダイアログが表示されます。

たとえば、接続パラメータが次のように表示される場合:

```text
HOST:     gateway01.us-east-1.prod.shared.aws.tidbcloud.com
PORT:     4000
USERNAME: 4EfqPF23YKBxaQb.root
PASSWORD: abcd1234
DATABASE: test
CA:       /etc/ssl/cert.pem
```

TiDB Cloud Starter クラスターに接続するための対応する Python コードは次のようになります。

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
> 上記の例はデモンストレーションのみを目的としています。パラメータにはご自身で値を入力し、安全な状態に保ってください。

</div>
<div label="TiDB Self-Managed">

以下は、セルフマネージド TiDB クラスターに接続するための基本的な例です。

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
> 実際の展開に応じて接続パラメータを必ず更新してください。

</div>
</SimpleTab>

接続すると、 `client`オブジェクトを使用してテーブルを操作したり、データを照会したりできるようになります。

## 埋め込み関数を作成する {#create-an-embedding-function}

[埋め込みモデル](/ai/concepts/vector-search-overview.md#embedding-model)を使用する場合、埋め込み関数を利用して、挿入段階とクエリ段階の両方でデータを自動的にベクトル化できます。OpenAI、Jina AI、Hugging Face、Sentence Transformersなどの一般的な埋め込みモデルをネイティブにサポートしています。

<SimpleTab>
<div label="OpenAI">

埋め込み用の API キーを作成するには、 [OpenAIプラットフォーム](https://platform.openai.com/api-keys)に進んでください。

```python
from pytidb.embeddings import EmbeddingFunction

text_embed = EmbeddingFunction(
    model_name="openai/text-embedding-3-small",
    api_key="<your-openai-api-key>",
)
```

</div>
<div label="Jina AI">

埋め込み用の API キーを作成するには、 [ジナ・アイ](https://jina.ai/embeddings/)に進んでください。

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

例として、次の列を持つ`chunks`という名前のテーブルを作成します。

-   `id` (int): チャンクの ID。
-   `text` (テキスト): チャンクのテキスト コンテンツ。
-   `text_vec` (ベクトル): テキストのベクトル埋め込み。
-   `user_id` (int): チャンクを作成したユーザーの ID。

```python hl_lines="6"
from pytidb.schema import TableModel, Field, VectorField

class Chunk(TableModel):
    id: int | None = Field(default=None, primary_key=True)
    text: str = Field()
    text_vec: list[float] = text_embed.VectorField(source_field="text")
    user_id: int = Field()

table = client.create_table(schema=Chunk, if_exists="overwrite")
```

作成したら、 `table`オブジェクトを使用してデータの挿入、データの検索などを行うことができます。

## データの挿入 {#insert-data}

それでは、テーブルにサンプルデータを追加してみましょう。

```python
table.bulk_insert([
    # 👇 The text will be automatically embedded and populated into the `text_vec` field.
    Chunk(text="PyTiDB is a Python library for developers to connect to TiDB.", user_id=2),
    Chunk(text="LlamaIndex is a framework for building AI applications.", user_id=2),
    Chunk(text="OpenAI is a company and platform that provides AI models service and tools.", user_id=3),
])
```

## 最も近い隣人を検索 {#search-for-nearest-neighbors}

特定のクエリに最も近い近傍を検索するには、 `table.search()`方法を使用できます。この方法はデフォルトで[ベクトル検索](/ai/guides/vector-search.md)方法を実行します。

```python
table.search(
    # 👇 Pass the query text directly, it will be embedded to a query vector automatically.
    "A library for my artificial intelligence software"
)
.limit(3).to_list()
```

この例では、ベクトル検索はクエリ ベクトルを`chunks`テーブルの`text_vec`フィールドに格納されているベクトルと比較し、類似度スコアに基づいて意味的に最も関連性の高い上位 3 つの結果を返します。

`_distance`近いほど、2 つのベクトルが類似していることを意味します。

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

テーブルから特定の行を削除するには、 `table.delete()`メソッドを使用します。

```python
table.delete({
    "id": 1
})
```

## ドロップテーブル {#drop-table}

テーブルが不要になったら、 `client.drop_table()`メソッドを使用してテーブルを削除できます。

```python
client.drop_table("chunks")
```

## 次のステップ {#next-steps}

-   TiDB の[ベクトル検索](/ai/guides/vector-search.md) [全文検索](/ai/guides/vector-search-full-text-search-python.md)詳細をご覧ください[ハイブリッド検索](/ai/guides/vector-search-hybrid-search.md)
