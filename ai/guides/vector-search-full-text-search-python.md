---
title: Full-Text Search with Python
summary: 全文検索では、正確なキーワードに基づいて文書を検索できます。検索拡張生成（RAG）シナリオでは、全文検索とベクトル検索を組み合わせて使用​​することで、検索精度を向上させることができます。
aliases: ['/ja/tidb/stable/vector-search-full-text-search-python/','/ja/tidbcloud/vector-search-full-text-search-python/']
---

# Pythonによる全文検索 {#full-text-search-with-python}

意味的な類似性に焦点を当てる[ベクトル検索](/ai/concepts/vector-search-overview.md)とは異なり、全文検索では正確なキーワードに基づいて文書を取得できます。検索拡張生成（RAG）シナリオでは、全文検索とベクトル検索を組み合わせて使用​​することで、検索品質を向上させることができます。

TiDBの全文検索機能は、以下の機能を提供します。

-   **テキストデータを直接クエリする**：埋め込み処理を行わずに、任意の文字列列を直接検索できます。

-   **多言語対応**：高品質な検索のために言語を指定する必要はありません。TiDBは、同じテーブルに保存された複数の言語のドキュメントをサポートし、各ドキュメントに最適なテキストアナラ​​イザーを自動的に選択します。

-   **関連性順に並べる**: 広く採用されている[BM25ランキング](https://en.wikipedia.org/wiki/Okapi_BM25)アルゴリズムを使用して、検索結果を関連性順に並べ替えることができます。

-   **SQLとの完全な互換性**：事前フィルタリング、事後フィルタリング、グループ化、結合など、すべてのSQL機能を全文検索で使用できます。

> **ヒント：**
>
> SQL の使用法については、 [SQLによる全文検索](/ai/guides/vector-search-full-text-search-sql.md)参照してください。
>
> AI アプリで全文検索とベクトル検索を併用するには、 [ハイブリッド検索](/ai/guides/vector-search-hybrid-search.md)参照してください。

## 前提条件 {#prerequisites}

全文検索機能はまだ開発初期段階にあり、より多くのお客様に順次展開していく予定です。現在、全文検索機能は、以下のリージョンにおけるTiDB Cloud StarterおよびTiDB Cloud Essentialでのみご利用いただけます。

-   AWS: `Frankfurt (eu-central-1)`および`Singapore (ap-southeast-1)`

このチュートリアルを完了するには、サポートされているリージョンにTiDB Cloud Starterインスタンスがあることを確認してください。お持ちでない場合は、 [TiDB Cloud Starterインスタンスを作成する](/develop/dev-guide-build-cluster-in-cloud.md)。

## さあ始めましょう {#get-started}

### ステップ1. <a href="https://github.com/pingcap/pytidb">pytidb</a> Python SDKをインストールします {#step-1-install-the-a-href-https-github-com-pingcap-pytidb-pytidb-a-python-sdk}

[pytidb](https://github.com/pingcap/pytidb)はTiDBの公式Python SDKであり、開発者が効率的にAIアプリケーションを構築できるよう設計されています。ベクトル検索と全文検索の機能が組み込まれています。

SDKをインストールするには、次のコマンドを実行してください。

```shell
pip install pytidb

# (Alternative) To use the built-in embedding functions and rerankers:
# pip install "pytidb[models]"

# (Optional) To convert query results into pandas DataFrames:
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

### ステップ3．表と全文索引を作成する {#step-3-create-a-table-and-a-full-text-index}

例として、 `chunks`という名前のテーブルを作成し、以下の列を追加します。

-   `id` (int): チャンクのID。
-   `text` (テキスト): チャンクのテキストコンテンツ。
-   `user_id` (int): チャンクを作成したユーザーのID。

```python
from pytidb.schema import TableModel, Field

class Chunk(TableModel, table=True):
    __tablename__ = "chunks"

    id: int = Field(primary_key=True)
    text: str = Field()
    user_id: int = Field()

table = db.create_table(schema=Chunk)

if not table.has_fts_index("text"):
    table.create_fts_index("text")   # 👈 Create a fulltext index on the text column.
```

### ステップ4．データを挿入する {#step-4-insert-data}

```python
table.bulk_insert(
    [
        Chunk(id=2, text="the quick brown", user_id=2),
        Chunk(id=3, text="fox jumps", user_id=3),
        Chunk(id=4, text="over the lazy dog", user_id=4),
    ]
)
```

### ステップ5．全文検索を実行する {#step-5-perform-a-full-text-search}

データを挿入した後、以下のように全文検索を実行できます。

```python
df = (
  table.search("brown fox", search_type="fulltext")
    .limit(2)
    .to_pandas() # optional
)

#    id             text  user_id
# 0   3        fox jumps        3
# 1   2  the quick brown        2
```

完全な例については、 [pytidb全文検索デモ](https://github.com/pingcap/pytidb/blob/main/examples/fulltext_search)参照してください。

## 関連項目 {#see-also}

-   [pytidb Python SDK ドキュメント](https://github.com/pingcap/pytidb)

-   [ハイブリッド検索](/ai/guides/vector-search-hybrid-search.md)

## フィードバックとヘルプ {#feedback-x26-help}

全文検索はまだ開発初期段階であり、利用できる地域が限られています。まだ利用できない地域で全文検索を試してみたい場合、またはご意見やご質問がある場合は、お気軽にお問い合わせください。

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)or [スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに質問してください。
-   [TiDB Cloudのサポートチケットを送信してください](https://tidb.support.pingcap.com/servicedesk/customer/portals)
