---
title: Hybrid Search
summary: 全文検索とベクトル検索を併用して、検索品質を向上させます。
---

# ハイブリッド検索 {#hybrid-search}

全文検索を使用すると、正確なキーワードに基づいて文書を検索できます。ベクトル検索を使用すると、意味的な類似性に基づいて文書を検索できます。これら2つの検索方法を組み合わせることで、検索品質を向上させ、より多くのシナリオに対応できますか？はい、このアプローチはハイブリッド検索と呼ばれ、AIアプリケーションでよく使用されています。

TiDB でのハイブリッド検索の一般的なワークフローは次のとおりです。

1.  **全文検索**や**ベクター検索**には TiDB を使用します。
2.  **再ランク付け機能**を使用して、両方の検索の結果を結合します。

![Hybrid Search](/media/vector-search/hybrid-search-overview.svg)

このチュートリアルでは、埋め込みと再ランキングの組み込みサポートを提供する[pytidb](https://github.com/pingcap/pytidb) Python SDKを使用して、TiDBのハイブリッド検索を使用する方法を説明します。pytidbの使用は完全にオプションです。SQLを使用して直接検索を実行し、必要に応じて独自の再ランキングモデルを使用することもできます。

## 前提条件 {#prerequisites}

ハイブリッド検索は、 [全文検索](/tidb-cloud/vector-search-full-text-search-python.md)検索とベクトル検索の両方を利用します。全文検索はまだ初期段階であり、より多くのお客様に継続的に展開しています。現在、全文検索は以下の製品オプションとリージョンでのみご利用いただけます。

-   TiDB Cloudサーバーレス: `Frankfurt (eu-central-1)`と`Singapore (ap-southeast-1)`

このチュートリアルを完了するには、サポート対象リージョンにTiDB Cloud Serverlessクラスターがインストールされている必要があります。まだインストールされていない場合は、手順[TiDB Cloud Serverless クラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って作成してください。

## 始めましょう {#get-started}

### ステップ1. <a href="https://github.com/pingcap/pytidb">pytidb</a> Python SDKをインストールする {#step-1-install-the-a-href-https-github-com-pingcap-pytidb-pytidb-a-python-sdk}

```shell
pip install "pytidb[models]"

# (Alternative) If you don't want to use built-in embedding functions and rerankers:
# pip install pytidb

# (Optional) To convert query results to pandas DataFrame:
# pip install pandas
```

### ステップ2. TiDBに接続する {#step-2-connect-to-tidb}

```python
from pytidb import TiDBClient

db = TiDBClient.connect(
    host="HOST_HERE",
    port=4000,
    username="USERNAME_HERE",
    password="PASSWORD_HERE",
    database="DATABASE_HERE",
)
```

これらの接続パラメータは[TiDB Cloudコンソール](https://tidbcloud.com)から取得できます:

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

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

    TiDB Cloud Serverless クラスターに接続するための対応する Python コードは次のようになります。

    ```python
    db = TiDBClient.connect(
        host="gateway01.us-east-1.prod.shared.aws.tidbcloud.com",
        port=4000,
        username="4EfqPF23YKBxaQb.root",
        password="abcd1234",
        database="test",
    )
    ```

    上記の例はデモンストレーションのみを目的としていることに注意してください。パラメータには独自の値を入力し、安全な状態に保ってください。

### ステップ3. テーブルを作成する {#step-3-create-a-table}

例として、次の列を持つ`chunks`という名前のテーブルを作成します。

-   `id` (int): チャンクの ID。
-   `text` (テキスト): チャンクのテキスト コンテンツ。
-   `text_vec` (ベクトル): pytidb の埋め込みモデルによって自動的に生成されたテキストのベクトル表現。
-   `user_id` (int): チャンクを作成したユーザーの ID。

```python
from pytidb.schema import TableModel, Field
from pytidb.embeddings import EmbeddingFunction

text_embed = EmbeddingFunction("openai/text-embedding-3-small")

class Chunk(TableModel, table=True):
    __tablename__ = "chunks"

    id: int = Field(primary_key=True)
    text: str = Field()
    text_vec: list[float] = text_embed.VectorField(
        source_field="text"
    )  # 👈 Define the vector field.
    user_id: int = Field()

table = db.create_table(schema=Chunk)
```

### ステップ4. データを挿入する {#step-4-insert-data}

```python
table.bulk_insert(
    [
        Chunk(id=2, text="bar", user_id=2),   # 👈 The text field will be embedded to a
        Chunk(id=3, text="baz", user_id=3),   # vector and stored in the "text_vec" field
        Chunk(id=4, text="qux", user_id=4),   # automatically.
    ]
)
```

### ステップ5.ハイブリッド検索を実行する {#step-5-perform-a-hybrid-search}

この例では、 [jina-reranker](https://huggingface.co/jinaai/jina-reranker-m0)モデルを使用して検索結果を再ランク付けします。

```python
from pytidb.rerankers import Reranker

jinaai = Reranker(model_name="jina_ai/jina-reranker-m0")

df = (
  table.search("<query>", search_type="hybrid")
    .rerank(jinaai, "text")  # 👈 Rerank the query result using the jinaai model.
    .limit(2)
    .to_pandas()
)
```

完全な例については、 [pytidb ハイブリッド検索デモ](https://github.com/pingcap/pytidb/tree/main/examples/hybrid_search)参照してください。

## 参照 {#see-also}

-   [pytidb Python SDK ドキュメント](https://github.com/pingcap/pytidb)

-   [Pythonによる全文検索](/tidb-cloud/vector-search-full-text-search-python.md)

## フィードバックとヘルプ {#feedback-x26-help}

全文検索はまだ初期段階にあり、アクセス範囲が限られています。まだご利用いただけない地域で全文検索をお試しになりたい場合、またはフィードバックやサポートが必要な場合は、お気軽にお問い合わせください。

<CustomContent platform="tidb">

-   [Discordに参加する](https://discord.gg/zcqexutz2R)

</CustomContent>

<CustomContent platform="tidb-cloud">

-   [Discordに参加する](https://discord.gg/zcqexutz2R)
-   [サポートポータルをご覧ください](https://tidb.support.pingcap.com/)

</CustomContent>
