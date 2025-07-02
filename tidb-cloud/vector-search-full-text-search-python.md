---
title: Full-Text Search with Python
summary: 全文検索を使用すると、キーワードに完全一致するドキュメントを取得できます。検索拡張生成（RAG）シナリオでは、全文検索とベクター検索を併用することで、検索品質を向上させることができます。
aliases: ['/tidb/stable/vector-search-full-text-search-python']
---

# Pythonによる全文検索 {#full-text-search-with-python}

意味的類似性に重点を置く[ベクトル検索](/tidb-cloud/vector-search-overview.md)とは異なり、全文検索では正確なキーワードで文書を検索できます。検索拡張生成（RAG）シナリオでは、全文検索とベクトル検索を併用することで検索品質を向上させることができます。

TiDB の全文検索機能は、次の機能を提供します。

-   **テキスト データを直接クエリします**。埋め込みプロセスなしで任意の文字列列を直接検索できます。

-   **複数言語のサポート**：高品質な検索のために言語を指定する必要はありません。TiDBは、同一テーブルに格納された複数言語の文書をサポートし、各文書に最適なテキストアナライザーを自動的に選択します。

-   **関連性による並べ替え**: 広く採用されている[BM25ランキング](https://en.wikipedia.org/wiki/Okapi_BM25)アルゴリズムを使用して、検索結果を関連性によって並べ替えることができます。

-   **SQL と完全に互換性があります**。事前フィルタリング、事後フィルタリング、グループ化、結合などのすべての SQL 機能をフルテキスト検索で使用できます。

> **ヒント：**
>
> SQL の使用法については、 [SQLによる全文検索](/tidb-cloud/vector-search-full-text-search-sql.md)参照してください。
>
> AI アプリで全文検索とベクトル検索を併用するには、 [ハイブリッド検索](/tidb-cloud/vector-search-hybrid-search.md)参照してください。

## 前提条件 {#prerequisites}

全文検索機能はまだ初期段階にあり、今後も継続的に多くのお客様にご利用いただけるよう展開していきます。現在、全文検索機能は下記の製品オプションとリージョンでのみご利用いただけます。

-   TiDB Cloudサーバーレス: `Frankfurt (eu-central-1)`と`Singapore (ap-southeast-1)`

このチュートリアルを完了するには、サポート対象リージョンにTiDB Cloud Serverlessクラスターがインストールされている必要があります。まだインストールされていない場合は、手順[TiDB Cloud Serverless クラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って作成してください。

## 始めましょう {#get-started}

### ステップ1. <a href="https://github.com/pingcap/pytidb">pytidb</a> Python SDKをインストールする {#step-1-install-the-a-href-https-github-com-pingcap-pytidb-pytidb-a-python-sdk}

[pytidb](https://github.com/pingcap/pytidb)はTiDBの公式Python SDKで、開発者がAIアプリケーションを効率的に構築できるように設計されています。ベクトル検索と全文検索のサポートが組み込まれています。

SDK をインストールするには、次のコマンドを実行します。

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

これらの接続パラメータは[TiDB Cloudコンソール](https://tidbcloud.com)から取得できます:

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

### ステップ3. テーブルとフルテキストインデックスを作成する {#step-3-create-a-table-and-a-full-text-index}

例として、次の列を持つ`chunks`という名前のテーブルを作成します。

-   `id` (int): チャンクの ID。
-   `text` (テキスト): チャンクのテキスト コンテンツ。
-   `user_id` (int): チャンクを作成したユーザーの ID。

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

### ステップ4. データを挿入する {#step-4-insert-data}

```python
table.bulk_insert(
    [
        Chunk(id=2, text="the quick brown", user_id=2),
        Chunk(id=3, text="fox jumps", user_id=3),
        Chunk(id=4, text="over the lazy dog", user_id=4),
    ]
)
```

### ステップ5. 全文検索を実行する {#step-5-perform-a-full-text-search}

データを挿入した後、次のように全文検索を実行できます。

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

## 参照 {#see-also}

-   [pytidb Python SDK ドキュメント](https://github.com/pingcap/pytidb)

-   [ハイブリッド検索](/tidb-cloud/vector-search-hybrid-search.md)

## フィードバックとヘルプ {#feedback-x26-help}

全文検索はまだ初期段階にあり、アクセス範囲が限られています。まだご利用いただけない地域で全文検索をお試しになりたい場合、またはフィードバックやサポートが必要な場合は、お気軽にお問い合わせください。

<CustomContent platform="tidb">

-   [Discordに参加する](https://discord.gg/zcqexutz2R)

</CustomContent>

<CustomContent platform="tidb-cloud">

-   [Discordに参加する](https://discord.gg/zcqexutz2R)
-   [サポートポータルをご覧ください](https://tidb.support.pingcap.com/)

</CustomContent>
