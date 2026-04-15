---
title: Hybrid Search
summary: 全文検索とベクトル検索を併用することで、検索結果の質を向上させることができます。
aliases: ['/ja/tidb/stable/vector-search-hybrid-search/','/ja/tidbcloud/vector-search-hybrid-search/']
---

# ハイブリッド検索 {#hybrid-search}

全文検索では、正確なキーワードに基づいて文書を検索できます。ベクトル検索では、意味的な類似性に基づいて文書を検索できます。これらの2つの検索方法を組み合わせることで、検索精度を向上させ、より多くのシナリオに対応できるでしょうか？はい、このアプローチはハイブリッド検索と呼ばれ、AIアプリケーションで一般的に使用されています。

TiDBにおけるハイブリッド検索の一般的なワークフローは以下のとおりです。

1.  **全文検索**と**ベクトル検索**にはTiDBを使用してください。
2.  **リランカー**を使用して、両方の検索結果を統合します。

![Hybrid Search](/media/vector-search/hybrid-search-overview.svg)

このチュートリアルでは、埋め込みと再ランキングを標準でサポートする[pytidb](https://github.com/pingcap/pytidb) Python SDKを使用して、TiDBでハイブリッド検索を行う方法を説明します。pytidbの使用は完全に任意です。SQLを直接使用して検索を実行し、独自の再ランキングモデルを自由に利用することもできます。

## 前提条件 {#prerequisites}

全文検索機能はまだ開発初期段階にあり、より多くのお客様に順次展開していく予定です。現在、全文検索機能は、以下のリージョンにおけるTiDB Cloud StarterおよびTiDB Cloud Essentialでのみご利用いただけます。

-   AWS: `Frankfurt (eu-central-1)`および`Singapore (ap-southeast-1)`

このチュートリアルを完了するには、サポートされているリージョンにTiDB Cloud Starterインスタンスがあることを確認してください。お持ちでない場合は、 [TiDB Cloud Starterインスタンスを作成する](/develop/dev-guide-build-cluster-in-cloud.md)。

## さあ始めましょう {#get-started}

### ステップ1. <a href="https://github.com/pingcap/pytidb">pytidb</a> Python SDKをインストールします {#step-1-install-the-a-href-https-github-com-pingcap-pytidb-pytidb-a-python-sdk}

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

これらの接続パラメータは、次のように[TiDB Cloudコンソール](https://tidbcloud.com)から取得できます。

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud StarterまたはEssentialインスタンスの名前をクリックして、概要ページに移動します。

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
    db = TiDBClient.connect(
        host="gateway01.us-east-1.prod.shared.aws.tidbcloud.com",
        port=4000,
        username="4EfqPF23YKBxaQb.root",
        password="abcd1234",
        database="test",
    )
    ```

    上記の例はあくまでも説明のためのものです。パラメータにはご自身の値を入力し、安全に保管してください。

### ステップ3. テーブルを作成する {#step-3-create-a-table}

例として、 `chunks`という名前のテーブルを作成し、以下の列を追加します。

-   `id` (int): チャンクのID。
-   `text` (テキスト): チャンクのテキストコンテンツ。
-   `text_vec` (ベクトル): テキストのベクトル表現。pytidb の埋め込みモデルによって自動的に生成されます。
-   `user_id` (int): チャンクを作成したユーザーのID。

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

### ステップ4．データを挿入する {#step-4-insert-data}

```python
table.bulk_insert(
    [
        Chunk(id=2, text="bar", user_id=2),   # 👈 The text field will be embedded to a
        Chunk(id=3, text="baz", user_id=3),   # vector and stored in the "text_vec" field
        Chunk(id=4, text="qux", user_id=4),   # automatically.
    ]
)
```

### ステップ5．ハイブリッド検索を実行する {#step-5-perform-a-hybrid-search}

この例では、 [ジナ・リランカー](https://huggingface.co/jinaai/jina-reranker-m0)モデルを使用して検索結果を再ランク付けします。

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

完全な例については、 [pytidb ハイブリッド検索デモ](https://github.com/pingcap/pytidb/tree/main/examples/hybrid_search)を参照してください。

## 融合方法 {#fusion-methods}

融合手法は、ベクトル（意味）検索と全文（キーワード）検索の結果を統合し、単一の統一されたランキングを作成します。これにより、最終結果が意味的な関連性とキーワードの一致の両方を活用できるようになります。

`pytidb` 2 つの融合方法をサポートしています。

-   `rrf` : 相互ランク融合 (デフォルト)
-   `weighted` : 加重スコア融合

ハイブリッド検索結果を最適化するために、ご自身のユースケースに最適な融合方法を選択できます。

### 相互ランク融合（RRF） {#reciprocal-rank-fusion-rrf}

相互ランク融合（RRF）は、複数の検索結果セットにおける文書のランクを活用して検索結果を評価するアルゴリズムです。

詳細については、 [RRF論文](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf)参照してください。

`method`メソッドで`"rrf"`パラメーター`.fusion()`有効にします。

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

-   `k` : ゼロ除算を防ぎ、高ランクのドキュメントの影響を制御するための定数 (デフォルト: 60)。

### 加重スコア融合 {#weighted-score-fusion}

加重スコア融合は、ベクトル検索と全文検索のスコアを加重和を用いて組み合わせます。

```python
final_score = vs_weight * vector_score + fts_weight * fulltext_score
```

`method`メソッドで`"weighted"`パラメーター`.fusion()`有効にします。

例えば、ベクトル検索の重みを大きくするには、 `vs_weight`パラメータを 0.7 に、 `fts_weight`パラメータを 0.3 に設定します。

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

## 再ランク法 {#rerank-method}

ハイブリッド検索は、リランカー専用モデルを使用したリランキングもサポートしています。

`rerank()`メソッドを使用して、クエリとドキュメント間の関連性に基づいて検索結果を並べ替えるリランカーを指定します。

**例：Jina AI Rerankerを使用してハイブリッド検索結果の順位を再設定する**

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

他のリランカーモデルを確認するには、[ランキング変更](/ai/guides/reranking.md)ご覧ください。

## 関連項目 {#see-also}

-   [pytidb Python SDK ドキュメント](https://github.com/pingcap/pytidb)

-   [Pythonによる全文検索](/ai/guides/vector-search-full-text-search-python.md)

## フィードバックとヘルプ {#feedback-x26-help}

全文検索はまだ開発初期段階であり、利用できる地域が限られています。まだ利用できない地域で全文検索を試してみたい場合、またはご意見やご質問がある場合は、お気軽にお問い合わせください。

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)or [スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに質問してください。
-   [TiDB Cloudのサポートチケットを送信してください](https://tidb.support.pingcap.com/servicedesk/customer/portals)
