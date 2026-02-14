---
title: Get Started with TiDB + AI via Python
summary: Python と TiDB Vector Search を使用してセマンティック検索を実行する AI アプリケーションを迅速に開発する方法を学びます。
aliases: ['/ja/tidb/stable/vector-search-get-started-using-python/','/ja/tidbcloud/vector-search-get-started-using-python/']
---

# PythonでTiDB + AIを使い始める {#get-started-with-tidb-ai-via-python}

このチュートリアルでは、**セマンティック検索**機能を備えたシンプルなAIアプリケーションの開発方法を説明します。従来のキーワード検索とは異なり、セマンティック検索はクエリの背後にある意味をインテリジェントに理解し、最も関連性の高い結果を返します。例えば、「犬」、「魚」、「木」というタイトルのドキュメントがあり、「泳ぐ動物」を検索すると、アプリケーションは「魚」を最も関連性の高い結果として特定します。

このチュートリアルでは、 [TiDBベクトル検索](/ai/concepts/vector-search-overview.md) 、Python、 [Python 用 TiDB ベクター SDK](https://github.com/pingcap/tidb-vector-python) 、および AI モデルを使用してこの AI アプリケーションを開発します。

> **注記：**
>
> -   ベクター検索機能はベータ版です。予告なく変更される可能性があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)報告を行ってください。
> -   ベクトル検索機能は[TiDBセルフマネージド](/overview.md) 、 [TiDB Cloudスターター](/tidb-cloud/select-cluster-tier.md#starter) 、 [TiDB Cloudエッセンシャル](/tidb-cloud/select-cluster-tier.md#essential) 、 [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)で利用可能です。TiDB Self-ManagedおよびTiDB Cloud Dedicatedの場合、TiDBバージョンはv8.4.0以降である必要があります（v8.5.0以降を推奨）。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、次のものが必要です。

-   [Python 3.8以上](https://www.python.org/downloads/)個インストールされました。
-   [ギット](https://git-scm.com/downloads)個インストールされました。
-   TiDB クラスター。

**TiDB クラスターがない場合は、次のように作成できます。**

-   (推奨) [TiDB Cloud Starter クラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って、独自のTiDB Cloudクラスターを作成します。
-   [ローカルテストTiDBクラスタをデプロイ](/quick-start-with-tidb.md#deploy-a-local-test-cluster)または[本番のTiDBクラスタをデプロイ](/production-deployment-using-tiup.md)に従ってローカル クラスターを作成します。

## 始めましょう {#get-started}

以下の手順は、アプリケーションをゼロから開発する方法を示しています。デモを直接実行するには、 [pingcap/tidb-vector-python](https://github.com/pingcap/tidb-vector-python/blob/main/examples/python-client-quickstart)リポジトリのサンプルコードをチェックアウトしてください。

### ステップ1. 新しいPythonプロジェクトを作成する {#step-1-create-a-new-python-project}

任意のディレクトリに、新しい Python プロジェクトと`example.py`という名前のファイルを作成します。

```shell
mkdir python-client-quickstart
cd python-client-quickstart
touch example.py
```

### ステップ2. 必要な依存関係をインストールする {#step-2-install-required-dependencies}

プロジェクト ディレクトリで、次のコマンドを実行して必要なパッケージをインストールします。

```shell
pip install sqlalchemy pymysql sentence-transformers tidb-vector python-dotenv
```

-   `tidb-vector` : TiDB ベクトル検索と対話するための Python クライアント。
-   [`sentence-transformers`](https://sbert.net) : テキストから[ベクトル埋め込み](/ai/concepts/vector-search-overview.md#vector-embedding)生成するための事前トレーニング済みモデルを提供する Python ライブラリ。

### ステップ3. TiDBクラスターへの接続文字列を構成する {#step-3-configure-the-connection-string-to-the-tidb-cluster}

選択した TiDB デプロイメント オプションに応じて、クラスター接続文字列を構成します。

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

    > **ヒント：**
    >
    > プログラムが Windows Subsystem for Linux (WSL) で実行されている場合は、対応する Linux ディストリビューションに切り替えます。

4.  **PyMySQL**タブをクリックし、接続文字列をコピーします。

    > **ヒント：**
    >
    > まだパスワードを設定していない場合は、 **「パスワードの生成」をクリックしてランダムなパスワード**を生成します。

5.  Python プロジェクトのルート ディレクトリに`.env`ファイルを作成し、そこに接続文字列を貼り付けます。

    以下は macOS の例です。

    ```dotenv
    TIDB_DATABASE_URL="mysql+pymysql://<prefix>.root:<password>@gateway01.<region>.prod.aws.tidbcloud.com:4000/test?ssl_ca=/etc/ssl/cert.pem&ssl_verify_cert=true&ssl_verify_identity=true"
    ```

</div>
<div label="TiDB Self-Managed" value="tidb">

TiDBセルフマネージドクラスタの場合、Pythonプロジェクトのルートディレクトリに`.env`ファイルを作成します。以下の内容を`.env`ファイルにコピーし、TiDBクラスタの接続パラメータに応じて環境変数の値を変更します。

```dotenv
TIDB_DATABASE_URL="mysql+pymysql://<USER>:<PASSWORD>@<HOST>:<PORT>/<DATABASE>"
# For example: TIDB_DATABASE_URL="mysql+pymysql://root@127.0.0.1:4000/test"
```

ローカルマシンでTiDBを実行している場合、デフォルトでは`<HOST>`が`127.0.0.1`なります。初期の`<PASSWORD>`は空なので、クラスターを初めて起動する場合はこのフィールドを省略できます。

各パラメータの説明は次のとおりです。

-   `<USER>` : TiDB クラスターに接続するためのユーザー名。
-   `<PASSWORD>` : TiDB クラスターに接続するためのパスワード。
-   `<HOST>` : TiDB クラスターのホスト。
-   `<PORT>` : TiDB クラスターのポート。
-   `<DATABASE>` : 接続するデータベースの名前。

</div>

</SimpleTab>

### ステップ4. 埋め込みモデルの初期化 {#step-4-initialize-the-embedding-model}

[埋め込みモデル](/ai/concepts/vector-search-overview.md#embedding-model)データを[ベクトル埋め込み](/ai/concepts/vector-search-overview.md#vector-embedding)に変換します。この例では、テキスト埋め込みに事前学習済みのモデル[**msmarco-MiniLM-L12-cos-v5**](https://huggingface.co/sentence-transformers/msmarco-MiniLM-L12-cos-v5)使用します。7 `sentence-transformers`が提供するこの軽量モデルは、テキストデータを 384 次元のベクトル埋め込みに変換します。

モデルをセットアップするには、次のコードを`example.py`ファイルにコピーします。このコードは`SentenceTransformer`インスタンスを初期化し、後で使用する`text_to_embedding()`関数を定義します。

```python
from sentence_transformers import SentenceTransformer

print("Downloading and loading the embedding model...")
embed_model = SentenceTransformer("sentence-transformers/msmarco-MiniLM-L12-cos-v5", trust_remote_code=True)
embed_model_dims = embed_model.get_sentence_embedding_dimension()

def text_to_embedding(text):
    """Generates vector embeddings for the given text."""
    embedding = embed_model.encode(text)
    return embedding.tolist()
```

### ステップ5. TiDBクラスターに接続する {#step-5-connect-to-the-tidb-cluster}

`TiDBVectorClient`クラスを使用して TiDB クラスターに接続し、ベクター列を持つテーブル`embedded_documents`を作成します。

> **注記**
>
> 表内のベクトル列の次元が、埋め込みモデルによって生成されるベクトルの次元と一致していることを確認してください。例えば、 **msmarco-MiniLM-L12-cos-v5**モデルは384次元のベクトルを生成するため、表`embedded_documents`のベクトル列の次元も384である必要があります。

```python
import os
from tidb_vector.integrations import TiDBVectorClient
from dotenv import load_dotenv

# Load the connection string from the .env file
load_dotenv()

vector_store = TiDBVectorClient(
   # The 'embedded_documents' table will store the vector data.
   table_name='embedded_documents',
   # The connection string to the TiDB cluster.
   connection_string=os.environ.get('TIDB_DATABASE_URL'),
   # The dimension of the vector generated by the embedding model.
   vector_dimension=embed_model_dims,
   # Recreate the table if it already exists.
   drop_existing_table=True,
)
```

### ステップ6. テキストデータを埋め込み、ベクトルを保存する {#step-6-embed-text-data-and-store-the-vectors}

このステップでは、「dog」、「fish」、「tree」といった単語を含むサンプルドキュメントを準備します。以下のコードは、 `text_to_embedding()`関数を使用してこれらのテキストドキュメントをベクトル埋め込みに変換し、ベクトルストアに挿入します。

```python
documents = [
    {
        "id": "f8e7dee2-63b6-42f1-8b60-2d46710c1971",
        "text": "dog",
        "embedding": text_to_embedding("dog"),
        "metadata": {"category": "animal"},
    },
    {
        "id": "8dde1fbc-2522-4ca2-aedf-5dcb2966d1c6",
        "text": "fish",
        "embedding": text_to_embedding("fish"),
        "metadata": {"category": "animal"},
    },
    {
        "id": "e4991349-d00b-485c-a481-f61695f2b5ae",
        "text": "tree",
        "embedding": text_to_embedding("tree"),
        "metadata": {"category": "plant"},
    },
]

vector_store.insert(
    ids=[doc["id"] for doc in documents],
    texts=[doc["text"] for doc in documents],
    embeddings=[doc["embedding"] for doc in documents],
    metadatas=[doc["metadata"] for doc in documents],
)
```

### ステップ7. セマンティック検索を実行する {#step-7-perform-semantic-search}

このステップでは、既存のドキュメント内のどの単語にも直接一致しない「a swimming animal」を検索します。

次のコードでは、 `text_to_embedding()`関数を再度使用してクエリ テキストをベクトル埋め込みに変換し、その埋め込みを使用してクエリを実行して、最も近い上位 3 つの一致を検索します。

```python
def print_result(query, result):
   print(f"Search result (\"{query}\"):")
   for r in result:
      print(f"- text: \"{r.document}\", distance: {r.distance}")

query = "a swimming animal"
query_embedding = text_to_embedding(query)
search_result = vector_store.query(query_embedding, k=3)
print_result(query, search_result)
```

`example.py`ファイルを実行すると、出力は次のようになります。

```plain
Search result ("a swimming animal"):
- text: "fish", distance: 0.4562914811223072
- text: "dog", distance: 0.6469335836410557
- text: "tree", distance: 0.798545178640937
```

検索結果の 3 つの用語は、クエリされたベクトルからのそれぞれの距離によって並べ替えられます。距離が小さいほど、対応する`document`関連性が高くなります。

したがって、出力によれば、泳いでいる動物は魚、または泳ぐ才能のある犬である可能性が最も高いです。

## 参照 {#see-also}

-   [ベクトルデータ型](/ai/reference/vector-search-data-types.md)
-   [ベクター検索インデックス](/ai/reference/vector-search-index.md)
