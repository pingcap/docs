---
title: Hybrid Search
summary: 全文検索とベクトル検索を併用して、検索品質を向上させます。
aliases: ['/tidb/stable/vector-search-hybrid-search/','/tidbcloud/vector-search-hybrid-search/']
---

# ハイブリッド検索 {#hybrid-search}

全文検索を使用すると、正確なキーワードに基づいて文書を検索できます。ベクトル検索を使用すると、意味的な類似性に基づいて文書を検索できます。これら2つの検索方法を組み合わせることで、検索品質を向上させ、より多くのシナリオに対応できますか？はい、このアプローチはハイブリッド検索と呼ばれ、AIアプリケーションでよく使用されています。

TiDB でのハイブリッド検索の一般的なワークフローは次のとおりです。

1.  **全文検索**と**ベクター検索**には TiDB を使用します。
2.  **再ランク付け機能**を使用して、両方の検索の結果を結合します。

![Hybrid Search](/media/vector-search/hybrid-search-overview.svg)

このチュートリアルでは、埋め込みと再ランキングの組み込みサポートを提供する[pytidb](https://github.com/pingcap/pytidb) Python SDK を使用して、TiDB のハイブリッド検索を使用する方法を説明します。pytidb の使用は完全にオプションです。SQL を直接使用して検索を実行し、必要に応じて独自の再ランキングモデルを使用することもできます。

## 前提条件 {#prerequisites}

全文検索機能はまだ初期段階にあり、今後も継続的にお客様への展開を進めていきます。現在、全文検索機能は、以下のリージョンにおいて、 TiDB Cloud Starter およびTiDB Cloud Essential でのみご利用いただけます。

-   AWS: `Frankfurt (eu-central-1)`と`Singapore (ap-southeast-1)`

このチュートリアルを完了するには、サポートされているリージョンにTiDB Cloud Starter クラスターがあることを確認してください。クラスターがない場合は、 [TiDB Cloud Starter クラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って作成してください。

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

これらの接続パラメータは、次のようにして[TiDB Cloudコンソール](https://tidbcloud.com)から取得できます。

1.  [**クラスター**](https://tidbcloud.com/project/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

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
    db = TiDBClient.connect(
        host="gateway01.us-east-1.prod.shared.aws.tidbcloud.com",
        port=4000,
        username="4EfqPF23YKBxaQb.root",
        password="abcd1234",
        database="test",
    )
    ```

    上記の例はデモンストレーションのみを目的としていることに注意してください。パラメータにはご自身で値を入力し、安全な状態に保ってください。

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

## 融合法 {#fusion-methods}

融合手法は、ベクター（セマンティック）検索とフルテキスト（キーワード）検索の結果を単一の統合ランキングに統合します。これにより、最終結果においてセマンティックな関連性とキーワードマッチングの両方が活用されます。

`pytidb` 2 つの融合方法をサポートします。

-   `rrf` : 逆ランク融合（デフォルト）
-   `weighted` : 加重スコア融合

ハイブリッド検索結果を最適化するために、ユースケースに最適な融合方法を選択できます。

### 逆ランク融合（RRF） {#reciprocal-rank-fusion-rrf}

相互ランク融合 (RRF) は、複数の結果セット内のドキュメントのランクを活用して検索結果を評価するアルゴリズムです。

詳細については[RRF論文](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf)を参照してください。

`.fusion()`メソッドで`method`パラメータを`"rrf"`に指定して、相互ランク融合を有効にします。

```python
results = (
    table.search(
        "AI database", search_type="hybrid"
    )
    .fusion(method="rrf")
    .limit(3)
    .to_list()
)
```

パラメータ:

-   `k` : ゼロ除算を防止し、ランクの高いドキュメントの影響を制御する定数 (デフォルト: 60)。

### 加重スコア融合 {#weighted-score-fusion}

加重スコア フュージョンは、加重合計を使用してベクトル検索スコアと全文検索スコアを組み合わせます。

```python
final_score = vs_weight * vector_score + fts_weight * fulltext_score
```

`.fusion()`メソッドで`method`パラメータを`"weighted"`に指定して、加重スコア融合を有効にします。

たとえば、ベクトル検索に重点を置くには、パラメータ`vs_weight`を 0.7 に設定し、パラメータ`fts_weight`を 0.3 に設定します。

```python
results = (
    table.search(
        "AI database", search_type="hybrid"
    )
    .fusion(method="weighted", vs_weight=0.7, fts_weight=0.3)
    .limit(3)
    .to_list()
)
```

パラメータ:

-   `vs_weight` : ベクトル検索スコアの重み。
-   `fts_weight` : 全文検索スコアの重み。

## 再ランク付け法 {#rerank-method}

ハイブリッド検索では、再ランク付け固有のモデルを使用した再ランク付けもサポートされます。

`rerank()`メソッドを使用して、クエリとドキュメント間の関連性に基づいて検索結果を並べ替える再ランク付けツールを指定します。

**例: Jina AI Rerankerを使用してハイブリッド検索結果を再ランク付けする**

```python
reranker = Reranker(
    # Use the `jina-reranker-m0` model
    model_name="jina_ai/jina-reranker-m0",
    api_key="{your-jinaai-api-key}"
)

results = (
    table.search(
        "AI database", search_type="hybrid"
    )
    .fusion(method="rrf", k=60)
    .rerank(reranker, "text")
    .limit(3)
    .to_list()
)
```

他のリランカーモデルを確認するには、 [再ランキング](/ai/guides/reranking.md)参照してください。

## 参照 {#see-also}

-   [pytidb Python SDK ドキュメント](https://github.com/pingcap/pytidb)

-   [Pythonによる全文検索](/ai/guides/vector-search-full-text-search-python.md)

## フィードバックとヘルプ {#feedback-x26-help}

全文検索はまだ初期段階にあり、アクセス範囲が限られています。まだご利用いただけない地域で全文検索をお試しになりたい場合、またはフィードバックやサポートが必要な場合は、お気軽にお問い合わせください。

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに問い合わせてください。
-   [TiDB Cloudのサポートチケットを送信する](https://tidb.support.pingcap.com/servicedesk/customer/portals)
