---
title: Integrate Vector Search with LlamaIndex
summary: TiDB Vector SearchとLlamaIndexを統合する方法を学びましょう。
aliases: ['/ja/tidb/stable/vector-search-integrate-with-llamaindex/','/ja/tidb/dev/vector-search-integrate-with-llamaindex/','/ja/tidbcloud/vector-search-integrate-with-llamaindex/']
---

# ベクトル検索をLlamaIndexと統合する {#integrate-vector-search-with-llamaindex}

このチュートリアルでは[TiDB ベクトル検索](/ai/concepts/vector-search-overview.md)[ラマインデックス](https://www.llamaindex.ai)統合する方法を説明します。

> **注記：**
>
> -   ベクター検索機能はベータ版です。予告なく変更される場合があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)を報告してください。
> -   ベクトル検索機能は、 [TiDBセルフマネージド](/overview.md)[TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter) 、 [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) 、および[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)で利用できます。TiDB Self-ManagedおよびTiDB Cloud Dedicatedの場合、TiDBのバージョンはv8.4.0以降である必要があります（v8.5.0以降を推奨）。

> **ヒント**
>
> 完全な[サンプルコード](https://github.com/run-llama/llama_index/blob/main/docs/docs/examples/vector_stores/TiDBVector.ipynb)Jupyter Notebook で表示することも、 [コラボレーション](https://colab.research.google.com/github/run-llama/llama_index/blob/main/docs/docs/examples/vector_stores/TiDBVector.ipynb)オンライン環境で直接実行することもできます。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、以下が必要です。

-   [Python 3.8以降](https://www.python.org/downloads/)インストールされています。
-   [ジュピターノートブック](https://jupyter.org/install)がインストールされました。
-   [Git](https://git-scm.com/downloads)がインストールされました。
-   TiDBクラスタ。

**TiDBクラスタをお持ちでない場合は、以下の手順で作成できます。**

-   (推奨) [TiDB Cloud Starterインスタンスを作成する](/develop/dev-guide-build-cluster-in-cloud.md)。
-   [ローカルテスト用のTiDBセルフマネージドクラスタをデプロイ。](/quick-start-with-tidb.md#deploy-a-local-test-cluster)または[本番本番のTiDBセルフマネージドクラスタをデプロイ。](/production-deployment-using-tiup.md)

## さあ始めましょう {#get-started}

このセクションでは、TiDB Vector SearchをLlamaIndexと統合してセマンティック検索を実行するための手順を段階的に説明します。

### ステップ1. 新しいJupyter Notebookファイルを作成する {#step-1-create-a-new-jupyter-notebook-file}

ルートディレクトリに、 `integrate_with_llamaindex.ipynb`という名前の新しい Jupyter Notebook ファイルを作成します。

```shell
touch integrate_with_llamaindex.ipynb
```

### ステップ2. 必要な依存関係をインストールします {#step-2-install-required-dependencies}

プロジェクトディレクトリで、以下のコマンドを実行して必要なパッケージをインストールしてください。

```shell
pip install llama-index-vector-stores-tidbvector
pip install llama-index
```

Jupyter Notebookで`integrate_with_llamaindex.ipynb`ファイルを開き、必要なパッケージをインポートするために以下のコードを追加します。

```python
import textwrap

from llama_index.core import SimpleDirectoryReader, StorageContext
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.tidbvector import TiDBVectorStore
```

### ステップ3．環境変数を設定する {#step-3-configure-environment-variables}

選択したTiDBのデプロイオプションに応じて、環境変数を設定してください。

<SimpleTab>
<div label="TiDB Cloud Starter or Essential">

TiDB Cloud StarterまたはEssentialインスタンスの場合、接続文字列を取得し、環境変数を設定するには、以下の手順に従ってください。

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud StarterまたはEssentialインスタンスの名前をクリックして、概要ページに移動します。

2.  右上隅の**「接続」**をクリックしてください。接続ダイアログが表示されます。

3.  接続ダイアログの設定がご使用のオペレーティング環境と一致していることを確認してください。

    -   **接続タイプ**は`Public`に設定されています。
    -   **ブランチ**は`main`に設定されています。
    -   **「接続」は**`SQLAlchemy`に設定されています。
    -   お使いの環境に合った**オペレーティングシステム**を選択してください。

4.  **PyMySQL**タブをクリックして、接続文字列をコピーしてください。

    > **ヒント：**
    >
    > まだパスワードを設定していない場合は、 **「パスワードを生成」**をクリックしてランダムなパスワードを生成してください。

5.  環境変数を設定します。

    このドキュメントでは、埋め込みモデルプロバイダーとして[OpenAI](https://platform.openai.com/docs/introduction)を使用します。この手順では、前の手順で取得した接続文字列と[OpenAI APIキー](https://platform.openai.com/docs/quickstart/step-2-set-up-your-api-key)指定する必要があります。

    環境変数を設定するには、次のコードを実行してください。接続文字列とOpenAI APIキーの入力を求められます。

    ```python
    # Use getpass to securely prompt for environment variables in your terminal.
    import getpass
    import os

    # Copy your connection string from the TiDB Cloud console.
    # Connection string format: "mysql+pymysql://<USER>:<PASSWORD>@<HOST>:4000/<DB>?ssl_ca=/etc/ssl/cert.pem&ssl_verify_cert=true&ssl_verify_identity=true"
    tidb_connection_string = getpass.getpass("TiDB Connection String:")
    os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")
    ```

</div>
<div label="TiDB Self-Managed" value="tidb">

このドキュメントでは、埋め込みモデルプロバイダーとして[OpenAI](https://platform.openai.com/docs/introduction)を使用します。この手順では、TiDBクラスターの接続文字列と[OpenAI APIキー](https://platform.openai.com/docs/quickstart/step-2-set-up-your-api-key)指定する必要があります。

環境変数を設定するには、次のコードを実行してください。接続文字列とOpenAI APIキーの入力を求められます。

```python
# Use getpass to securely prompt for environment variables in your terminal.
import getpass
import os

# Connection string format: "mysql+pymysql://<USER>:<PASSWORD>@<HOST>:4000/<DB>?ssl_ca=/etc/ssl/cert.pem&ssl_verify_cert=true&ssl_verify_identity=true"
tidb_connection_string = getpass.getpass("TiDB Connection String:")
os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")
```

macOSを例にとると、クラスタ接続文字列は次のようになります。

```dotenv
TIDB_DATABASE_URL="mysql+pymysql://<USERNAME>:<PASSWORD>@<HOST>:<PORT>/<DATABASE_NAME>"
# For example: TIDB_DATABASE_URL="mysql+pymysql://root@127.0.0.1:4000/test"
```

TiDBクラスタに合わせて、接続文字列のパラメータを変更する必要があります。ローカルマシンでTiDBを実行している場合、 `<HOST>`はデフォルトで`127.0.0.1`になります。初期値の`<PASSWORD>`は空なので、クラスタを初めて起動する場合は、このフィールドを省略できます。

各パラメータの説明は以下のとおりです。

-   `<USERNAME>` : TiDBに接続するためのユーザー名。
-   `<PASSWORD>` : TiDBに接続するためのパスワード。
-   `<HOST>` : TiDBクラスタのホスト。
-   `<PORT>` : TiDB クラスタのポート。
-   `<DATABASE>` : 接続するデータベースの名前。

</div>

</SimpleTab>

### ステップ4. サンプルドキュメントを読み込む {#step-4-load-the-sample-document}

#### ステップ4.1 サンプル文書をダウンロードする {#step-4-1-download-the-sample-document}

プロジェクトディレクトリ内に、 `data/paul_graham/`という名前のディレクトリを作成し、 [run-llama/llama_index](https://github.com/run-llama/llama_index) GitHubリポジトリからサンプルドキュメント[`paul_graham_essay.txt`](https://github.com/run-llama/llama_index/blob/main/docs/docs/examples/data/paul_graham/paul_graham_essay.txt)をダウンロードしてください。

```shell
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

#### ステップ4.2 ドキュメントを読み込む {#step-4-2-load-the-document}

`data/paul_graham/paul_graham_essay.txt`クラスを使用して、 `SimpleDirectoryReader` } からサンプル ドキュメントを読み込みます。

```python
documents = SimpleDirectoryReader("./data/paul_graham").load_data()
print("Document ID:", documents[0].doc_id)

for index, document in enumerate(documents):
   document.metadata = {"book": "paul_graham"}
```

### ステップ5．ドキュメントベクターを埋め込んで保存する {#step-5-embed-and-store-document-vectors}

#### ステップ5.1 TiDBベクターストアの初期化 {#step-5-1-initialize-the-tidb-vector-store}

以下のコードは、ベクトル検索に最適化されたTiDBに`paul_graham_test`という名前のテーブルを作成します。

```python
tidbvec = TiDBVectorStore(
   connection_string=tidb_connection_string,
   table_name="paul_graham_test",
   distance_strategy="cosine",
   vector_dimension=1536,
   drop_existing_table=False,
)
```

正常に実行されると、TiDB データベース内の`paul_graham_test`テーブルを直接表示およびアクセスできるようになります。

#### ステップ5.2 埋め込みを生成して保存する {#step-5-2-generate-and-store-embeddings}

以下のコードは、ドキュメントを解析し、埋め込みを生成し、それらをTiDBベクトルストアに保存します。

```python
storage_context = StorageContext.from_defaults(vector_store=tidbvec)
index = VectorStoreIndex.from_documents(
   documents, storage_context=storage_context, show_progress=True
)
```

期待される出力は以下のとおりです。

```plain
Parsing nodes: 100%|██████████| 1/1 [00:00<00:00,  8.76it/s]
Generating embeddings: 100%|██████████| 21/21 [00:02<00:00,  8.22it/s]
```

### ステップ6. ベクトル検索を実行する {#step-6-perform-a-vector-search}

以下では、TiDBベクトルストアに基づいてクエリエンジンを作成し、意味的類似性検索を実行します。

```python
query_engine = index.as_query_engine()
response = query_engine.query("What did the author do?")
print(textwrap.fill(str(response), 100))
```

> **注記**
>
> `TiDBVectorStore` [`default`](https://docs.llamaindex.ai/en/stable/api_reference/storage/vector_store/?h=vectorstorequerymode#llama_index.core.vector_stores.types.VectorStoreQueryMode)クエリ モードのみをサポートしています。

期待される出力は以下のとおりです。

```plain
The author worked on writing, programming, building microcomputers, giving talks at conferences,
publishing essays online, developing spam filters, painting, hosting dinner parties, and purchasing
a building for office use.
```

### ステップ7．メタデータフィルターを使用して検索する {#step-7-search-with-metadata-filters}

検索結果を絞り込むには、メタデータフィルターを使用して、適用したフィルターに一致する特定の近隣検索結果を取得できます。

#### <code>book != &quot;paul_graham&quot;</code>フィルターと異なるクエリ {#query-with-code-book-paul-graham-code-filter}

次の例では`book`メタデータ フィールドが`"paul_graham"`である結果を除外しています。

```python
from llama_index.core.vector_stores.types import (
   MetadataFilter,
   MetadataFilters,
)

query_engine = index.as_query_engine(
   filters=MetadataFilters(
      filters=[
         MetadataFilter(key="book", value="paul_graham", operator="!="),
      ]
   ),
   similarity_top_k=2,
)
response = query_engine.query("What did the author learn?")
print(textwrap.fill(str(response), 100))
```

期待される出力は以下のとおりです。

```plain
Empty Response
```

#### <code>book == &quot;paul_graham&quot;</code>フィルターを含むクエリ {#query-with-code-book-paul-graham-code-filter}

次の例では`book`メタデータ フィールドが`"paul_graham"`であるドキュメントのみを結果に含めるようにフィルタリングしています。

```python
from llama_index.core.vector_stores.types import (
   MetadataFilter,
   MetadataFilters,
)

query_engine = index.as_query_engine(
   filters=MetadataFilters(
      filters=[
         MetadataFilter(key="book", value="paul_graham", operator="=="),
      ]
   ),
   similarity_top_k=2,
)
response = query_engine.query("What did the author learn?")
print(textwrap.fill(str(response), 100))
```

期待される出力は以下のとおりです。

```plain
The author learned programming on an IBM 1401 using an early version of Fortran in 9th grade, then
later transitioned to working with microcomputers like the TRS-80 and Apple II. Additionally, the
author studied philosophy in college but found it unfulfilling, leading to a switch to studying AI.
Later on, the author attended art school in both the US and Italy, where they observed a lack of
substantial teaching in the painting department.
```

### ステップ8．文書を削除する {#step-8-delete-documents}

インデックスから最初のドキュメントを削除します。

```python
tidbvec.delete(documents[0].doc_id)
```

文書が削除されているかどうかを確認してください。

```python
query_engine = index.as_query_engine()
response = query_engine.query("What did the author learn?")
print(textwrap.fill(str(response), 100))
```

期待される出力は以下のとおりです。

```plain
Empty Response
```

## 関連項目 {#see-also}

-   [ベクトルデータ型](/ai/reference/vector-search-data-types.md)
-   [ベクトル検索インデックス](/ai/reference/vector-search-index.md)
