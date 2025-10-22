---
title: Integrate Vector Search with LlamaIndex
summary: TiDB Vector Search を LlamaIndex と統合する方法を学びます。
---

# ベクトル検索とLlamaIndexの統合 {#integrate-vector-search-with-llamaindex}

このチュートリアルでは、TiDB の[ベクトル検索](/vector-search/vector-search-overview.md)機能を[ラマインデックス](https://www.llamaindex.ai)と統合する方法を説明します。

<CustomContent platform="tidb">

> **警告：**
>
> ベクトル検索機能は実験的です。本番環境での使用は推奨されません。この機能は予告なく変更される可能性があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)報告を行ってください。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> ベクター検索機能はベータ版です。予告なく変更される可能性があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)報告を行ってください。

</CustomContent>

> **注記：**
>
> ベクトル検索機能は、TiDB Self-Managed、 [TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) [TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)利用できます[TiDB Cloud専用](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated) Self-ManagedおよびTiDB Cloud Dedicatedの場合、TiDBバージョンはv8.4.0以降である必要があります（v8.5.0以降を推奨）。

> **ヒント**
>
> 完全な[サンプルコード](https://github.com/run-llama/llama_index/blob/main/docs/docs/examples/vector_stores/TiDBVector.ipynb) Jupyter Notebook で表示することも、サンプル コードを[コラボ](https://colab.research.google.com/github/run-llama/llama_index/blob/main/docs/docs/examples/vector_stores/TiDBVector.ipynb)オンライン環境で直接実行することもできます。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、次のものが必要です。

-   [Python 3.8以上](https://www.python.org/downloads/)個インストールされました。
-   [ジュピターノートブック](https://jupyter.org/install)個インストールされました。
-   [ギット](https://git-scm.com/downloads)個インストールされました。
-   TiDB クラスター。

<CustomContent platform="tidb">

**TiDB クラスターがない場合は、次のように作成できます。**

-   [ローカルテストTiDBクラスタをデプロイ](/quick-start-with-tidb.md#deploy-a-local-test-cluster)または[本番のTiDBクラスタをデプロイ](/production-deployment-using-tiup.md)に従ってローカル クラスターを作成します。
-   [TiDB Cloud Starter クラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って、独自のTiDB Cloudクラスターを作成します。

</CustomContent>
<CustomContent platform="tidb-cloud">

**TiDB クラスターがない場合は、次のように作成できます。**

-   (推奨) [TiDB Cloud Starter クラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って、独自のTiDB Cloudクラスターを作成します。
-   [ローカルテストTiDBクラスタをデプロイ](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster)または[本番のTiDBクラスタをデプロイ](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup)に従って、v8.4.0 以降のバージョンのローカル クラスターを作成します。

</CustomContent>

## 始めましょう {#get-started}

このセクションでは、TiDB Vector Search を LlamaIndex と統合してセマンティック検索を実行する手順を段階的に説明します。

### ステップ1. 新しいJupyter Notebookファイルを作成する {#step-1-create-a-new-jupyter-notebook-file}

ルート ディレクトリに、 `integrate_with_llamaindex.ipynb`名前の新しい Jupyter Notebook ファイルを作成します。

```shell
touch integrate_with_llamaindex.ipynb
```

### ステップ2. 必要な依存関係をインストールする {#step-2-install-required-dependencies}

プロジェクト ディレクトリで、次のコマンドを実行して必要なパッケージをインストールします。

```shell
pip install llama-index-vector-stores-tidbvector
pip install llama-index
```

Jupyter Notebook で`integrate_with_llamaindex.ipynb`ファイルを開き、次のコードを追加して必要なパッケージをインポートします。

```python
import textwrap

from llama_index.core import SimpleDirectoryReader, StorageContext
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.tidbvector import TiDBVectorStore
```

### ステップ3.環境変数を設定する {#step-3-configure-environment-variables}

選択した TiDB デプロイメント オプションに応じて環境変数を構成します。

<SimpleTab>
<div label="TiDB Cloud Starter or Essential">

TiDB Cloud Starter クラスターの場合、クラスター接続文字列を取得し、環境変数を構成するには、次の手順を実行します。

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログの構成が動作環境と一致していることを確認します。

    -   **接続タイプ**は`Public`に設定されています。
    -   **ブランチ**は`main`に設定されています。
    -   **Connect With が**`SQLAlchemy`に設定されています。
    -   **オペレーティング システムは**環境に適合します。

4.  **PyMySQL**タブをクリックし、接続文字列をコピーします。

    > **ヒント：**
    >
    > まだパスワードを設定していない場合は、 **「パスワードの生成」**をクリックしてランダムなパスワードを生成します。

5.  環境変数を設定します。

    このドキュメントでは、埋め込みモデルプロバイダーとして[オープンAI](https://platform.openai.com/docs/introduction)使用します。この手順では、前の手順で取得した接続文字列と[OpenAI APIキー](https://platform.openai.com/docs/quickstart/step-2-set-up-your-api-key)指定する必要があります。

    環境変数を設定するには、以下のコードを実行します。接続文字列とOpenAI APIキーの入力を求められます。

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
<div label="TiDB Self-Managed">

このドキュメントでは、埋め込みモデルプロバイダーとして[オープンAI](https://platform.openai.com/docs/introduction)使用します。このステップでは、TiDB クラスターの接続文字列と[OpenAI APIキー](https://platform.openai.com/docs/quickstart/step-2-set-up-your-api-key)指定する必要があります。

環境変数を設定するには、以下のコードを実行します。接続文字列とOpenAI APIキーの入力を求められます。

```python
# Use getpass to securely prompt for environment variables in your terminal.
import getpass
import os

# Connection string format: "mysql+pymysql://<USER>:<PASSWORD>@<HOST>:4000/<DB>?ssl_ca=/etc/ssl/cert.pem&ssl_verify_cert=true&ssl_verify_identity=true"
tidb_connection_string = getpass.getpass("TiDB Connection String:")
os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")
```

macOS を例にとると、クラスター接続文字列は次のようになります。

```dotenv
TIDB_DATABASE_URL="mysql+pymysql://<USERNAME>:<PASSWORD>@<HOST>:<PORT>/<DATABASE_NAME>"
# For example: TIDB_DATABASE_URL="mysql+pymysql://root@127.0.0.1:4000/test"
```

接続文字列のパラメータは、TiDB クラスターに合わせて変更する必要があります。ローカルマシンで TiDB を実行している場合、デフォルトでは`<HOST>`が`127.0.0.1`設定されます。初期の`<PASSWORD>`空なので、クラスターを初めて起動する場合はこのフィールドを省略できます。

各パラメータの説明は次のとおりです。

-   `<USERNAME>` : TiDB クラスターに接続するためのユーザー名。
-   `<PASSWORD>` : TiDB クラスターに接続するためのパスワード。
-   `<HOST>` : TiDB クラスターのホスト。
-   `<PORT>` : TiDB クラスターのポート。
-   `<DATABASE>` : 接続するデータベースの名前。

</div>

</SimpleTab>

### ステップ4. サンプルドキュメントを読み込む {#step-4-load-the-sample-document}

#### ステップ4.1 サンプルドキュメントをダウンロードする {#step-4-1-download-the-sample-document}

プロジェクト ディレクトリに`data/paul_graham/`という名前のディレクトリを作成し、 [ランラマ/llama_index](https://github.com/run-llama/llama_index) GitHub リポジトリからサンプル ドキュメント[`paul_graham_essay.txt`](https://github.com/run-llama/llama_index/blob/main/docs/docs/examples/data/paul_graham/paul_graham_essay.txt)ダウンロードします。

```shell
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

#### ステップ4.2 ドキュメントを読み込む {#step-4-2-load-the-document}

`SimpleDirectoryReader`クラスを使用して`data/paul_graham/paul_graham_essay.txt`からサンプル ドキュメントを読み込みます。

```python
documents = SimpleDirectoryReader("./data/paul_graham").load_data()
print("Document ID:", documents[0].doc_id)

for index, document in enumerate(documents):
   document.metadata = {"book": "paul_graham"}
```

### ステップ5. ドキュメントベクターを埋め込んで保存する {#step-5-embed-and-store-document-vectors}

#### ステップ5.1 TiDBベクトルストアを初期化する {#step-5-1-initialize-the-tidb-vector-store}

次のコードは、ベクトル検索に最適化された`paul_graham_test`名前のテーブルを TiDB に作成します。

```python
tidbvec = TiDBVectorStore(
   connection_string=tidb_connection_url,
   table_name="paul_graham_test",
   distance_strategy="cosine",
   vector_dimension=1536,
   drop_existing_table=False,
)
```

実行が成功すると、TiDB データベース内の`paul_graham_test`テーブルを直接表示してアクセスできるようになります。

#### ステップ5.2 埋め込みを生成して保存する {#step-5-2-generate-and-store-embeddings}

次のコードは、ドキュメントを解析し、埋め込みを生成し、TiDB ベクトル ストアに保存します。

```python
storage_context = StorageContext.from_defaults(vector_store=tidbvec)
index = VectorStoreIndex.from_documents(
   documents, storage_context=storage_context, show_progress=True
)
```

期待される出力は次のとおりです。

```plain
Parsing nodes: 100%|██████████| 1/1 [00:00<00:00,  8.76it/s]
Generating embeddings: 100%|██████████| 21/21 [00:02<00:00,  8.22it/s]
```

### ステップ6. ベクトル検索を実行する {#step-6-perform-a-vector-search}

以下は、TiDB ベクトル ストアに基づいてクエリ エンジンを作成し、セマンティック類似性検索を実行します。

```python
query_engine = index.as_query_engine()
response = query_engine.query("What did the author do?")
print(textwrap.fill(str(response), 100))
```

> **注記**
>
> `TiDBVectorStore` [`default`](https://docs.llamaindex.ai/en/stable/api_reference/storage/vector_store/?h=vectorstorequerymode#llama_index.core.vector_stores.types.VectorStoreQueryMode)クエリ モードのみをサポートします。

期待される出力は次のとおりです。

```plain
The author worked on writing, programming, building microcomputers, giving talks at conferences,
publishing essays online, developing spam filters, painting, hosting dinner parties, and purchasing
a building for office use.
```

### ステップ7.メタデータフィルターを使って検索する {#step-7-search-with-metadata-filters}

検索を絞り込むには、メタデータ フィルターを使用して、適用したフィルターに一致する特定の最も近い結果を取得できます。

#### <code>book != &quot;paul_graham&quot;</code>フィルターを使用したクエリ {#query-with-code-book-paul-graham-code-filter}

次の例では、 `book`メタデータ フィールドが`"paul_graham"`ある結果を除外します。

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

期待される出力は次のとおりです。

```plain
Empty Response
```

#### <code>book == &quot;paul_graham&quot;</code>フィルターを使用したクエリ {#query-with-code-book-paul-graham-code-filter}

次の例では、 `book`データ フィールドが`"paul_graham"`あるドキュメントのみを含むように結果をフィルタリングします。

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

期待される出力は次のとおりです。

```plain
The author learned programming on an IBM 1401 using an early version of Fortran in 9th grade, then
later transitioned to working with microcomputers like the TRS-80 and Apple II. Additionally, the
author studied philosophy in college but found it unfulfilling, leading to a switch to studying AI.
Later on, the author attended art school in both the US and Italy, where they observed a lack of
substantial teaching in the painting department.
```

### ステップ8. ドキュメントを削除する {#step-8-delete-documents}

インデックスから最初のドキュメントを削除します。

```python
tidbvec.delete(documents[0].doc_id)
```

ドキュメントが削除されたかどうかを確認します。

```python
query_engine = index.as_query_engine()
response = query_engine.query("What did the author learn?")
print(textwrap.fill(str(response), 100))
```

期待される出力は次のとおりです。

```plain
Empty Response
```

## 参照 {#see-also}

-   [ベクトルデータ型](/vector-search/vector-search-data-types.md)
-   [ベクター検索インデックス](/vector-search/vector-search-index.md)
