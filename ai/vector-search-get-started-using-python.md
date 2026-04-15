---
title: Get Started with TiDB + AI via Python
summary: PythonとTiDB Vector Searchを使用して、セマンティック検索を実行するAIアプリケーションを迅速に開発する方法を学びましょう。
aliases: ['/ja/tidb/stable/vector-search-get-started-using-python/','/ja/tidb/dev/vector-search-get-started-using-python/','/ja/tidbcloud/vector-search-get-started-using-python/']
---

# Python を使って TiDB + AI を始めよう {#get-started-with-tidb-ai-via-python}

このチュートリアルでは、**セマンティック検索**機能を提供するシンプルなAIアプリケーションの開発方法を説明します。従来のキーワード検索とは異なり、セマンティック検索はクエリの背後にある意味をインテリジェントに理解し、最も関連性の高い結果を返します。たとえば、「犬」「魚」「木」というタイトルの文書があり、「泳ぐ動物」を検索すると、アプリケーションは「魚」を最も関連性の高い結果として識別します。

このチュートリアルでは、 [TiDB ベクトル検索](/ai/concepts/vector-search-overview.md)、Python、 [TiDB Vector SDK for Python](https://github.com/pingcap/tidb-vector-python) 、および AI モデルを使用して、この AI アプリケーションを開発します。

> **注記：**
>
> -   ベクター検索機能はベータ版です。予告なく変更される場合があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)を報告してください。
> -   ベクトル検索機能は、 [TiDBセルフマネージド](/overview.md)[TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter) 、 [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) 、および[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)で利用できます。TiDB Self-ManagedおよびTiDB Cloud Dedicatedの場合、TiDBのバージョンはv8.4.0以降である必要があります（v8.5.0以降を推奨）。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、以下が必要です。

-   [Python 3.8以降](https://www.python.org/downloads/)インストールされています。
-   [Git](https://git-scm.com/downloads)がインストールされました。
-   TiDBクラスタ。

**TiDBクラスタをお持ちでない場合は、以下の手順で作成できます。**

-   (推奨) [TiDB Cloud Starterインスタンスを作成する](/develop/dev-guide-build-cluster-in-cloud.md)。
-   [ローカルテスト用のTiDBセルフマネージドクラスタをデプロイ。](/quick-start-with-tidb.md#deploy-a-local-test-cluster)または[本番本番のTiDBセルフマネージドクラスタをデプロイ。](/production-deployment-using-tiup.md)

## さあ始めましょう {#get-started}

以下の手順では、アプリケーションをゼロから開発する方法を示します。デモを直接実行するには、 [pingcap/tidb-vector-python](https://github.com/pingcap/tidb-vector-python/blob/main/examples/python-client-quickstart)リポジトリにあるサンプルコードを参照してください。

### ステップ1. 新しいPythonプロジェクトを作成する {#step-1-create-a-new-python-project}

任意のディレクトリに、新しい Python プロジェクトと`example.py`という名前のファイルを作成します。

```shell
mkdir python-client-quickstart
cd python-client-quickstart
touch example.py
```

### ステップ2. 必要な依存関係をインストールします {#step-2-install-required-dependencies}

プロジェクトディレクトリで、以下のコマンドを実行して必要なパッケージをインストールしてください。

```shell
pip install sqlalchemy pymysql sentence-transformers tidb-vector python-dotenv
```

-   `tidb-vector` : TiDBベクトル検索と対話するためのPythonクライアント。
-   [`sentence-transformers`](https://sbert.net) : テキストから[ベクトル埋め込み](/ai/concepts/vector-search-overview.md#vector-embedding)を生成するための事前トレーニング済みモデルを提供する Python ライブラリです。

### ステップ3．TiDB接続文字列を設定する {#step-3-configure-the-tidb-connection-string}

選択したTiDBのデプロイオプションに応じて、接続文字列を設定してください。

<SimpleTab>
<div label="TiDB Cloud Starter">

TiDB Cloud Starterインスタンスの場合、接続文字列を取得し、環境変数を設定するには、以下の手順を実行してください。

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、次に、対象のTiDB Cloud Starterインスタンスの名前をクリックして、概要ページに移動します。

2.  右上隅の**「接続」**をクリックしてください。接続ダイアログが表示されます。

3.  接続ダイアログの設定がご使用のオペレーティング環境と一致していることを確認してください。

    -   **接続タイプ**は`Public`に設定されています。

    -   **ブランチ**は`main`に設定されています。

    -   **「接続」は**`SQLAlchemy`に設定されています。

    -   お使いの環境に合った**オペレーティングシステム**を選択してください。

    > **ヒント：**
    >
    > プログラムがWindows Subsystem for Linux（WSL）上で実行されている場合は、対応するLinuxディストリビューションに切り替えてください。

4.  **PyMySQL**タブをクリックして、接続文字列をコピーしてください。

    > **ヒント：**
    >
    > まだパスワードを設定していない場合は、 **「パスワードを生成」**をクリックしてランダムなパスワードを生成してください。

5.  Python プロジェクトのルートディレクトリに`.env`ファイルを作成し、接続文字列を貼り付けます。

    以下はmacOSの例です。

    ```dotenv
    TIDB_DATABASE_URL="mysql+pymysql://<prefix>.root:<password>@gateway01.<region>.prod.aws.tidbcloud.com:4000/test?ssl_ca=/etc/ssl/cert.pem&ssl_verify_cert=true&ssl_verify_identity=true"
    ```

</div>
<div label="TiDB Self-Managed" value="tidb">

TiDBセルフマネージドクラスタの場合、Pythonプロジェクトのルートディレクトリに`.env`ファイルを作成します。次の内容を`.env`ファイルにコピーし、TiDBクラスタの接続パラメータに応じて環境変数の値を変更します。

```dotenv
TIDB_DATABASE_URL="mysql+pymysql://<USER>:<PASSWORD>@<HOST>:<PORT>/<DATABASE>"
# For example: TIDB_DATABASE_URL="mysql+pymysql://root@127.0.0.1:4000/test"
```

TiDBをローカルマシンで実行している場合、 `<HOST>`はデフォルトで`127.0.0.1`になります。初期の`<PASSWORD>`は空なので、クラスターを初めて起動する場合は、このフィールドを省略できます。

各パラメータの説明は以下のとおりです。

-   `<USER>` : TiDBに接続するためのユーザー名。
-   `<PASSWORD>` : TiDBに接続するためのパスワード。
-   `<HOST>` : TiDBクラスタのホスト。
-   `<PORT>` : TiDB クラスタのポート。
-   `<DATABASE>` : 接続するデータベースの名前。

</div>

</SimpleTab>

### ステップ4．埋め込みモデルを初期化する {#step-4-initialize-the-embedding-model}

[埋め込みモデル](/ai/concepts/vector-search-overview.md#embedding-model)データを[ベクトル埋め込み](/ai/concepts/vector-search-overview.md#vector-embedding)に変換します。この例では、テキスト埋め込みに事前トレーニング済みモデル[**msmarco-MiniLM-L12-cos-v5**](https://huggingface.co/sentence-transformers/msmarco-MiniLM-L12-cos-v5)を使用します。 `sentence-transformers`ライブラリによって提供されるこの軽量モデルは、テキスト データを 384 次元のベクトル埋め込みに変換します。

モデルを設定するには、次のコードを`example.py`ファイルにコピーしてください。このコードは`SentenceTransformer`インスタンスを初期化し、後で使用するために`text_to_embedding()`関数を定義します。

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

### ステップ5．TiDBに接続する {#step-5-connect-to-tidb}

`TiDBVectorClient`クラスを使用して TiDB に接続し、ベクトル列を持つテーブル`embedded_documents`を作成します。

> **注記**
>
> テーブル内のベクトル列の次元が、埋め込みモデルによって生成されるベクトルの次元と一致していることを確認してください。たとえば、 **msmarco-MiniLM-L12-cos-v5**モデルは 384 次元のベクトルを生成するため、 `embedded_documents`内のベクトル列の次元も 384 にする必要があります。

```python
import os
from tidb_vector.integrations import TiDBVectorClient
from dotenv import load_dotenv

# Load the connection string from the .env file
load_dotenv()

vector_store = TiDBVectorClient(
   # The 'embedded_documents' table will store the vector data.
   table_name='embedded_documents',
   # The TiDB connection string.
   connection_string=os.environ.get('TIDB_DATABASE_URL'),
   # The dimension of the vector generated by the embedding model.
   vector_dimension=embed_model_dims,
   # Recreate the table if it already exists.
   drop_existing_table=True,
)
```

### ステップ6．テキス​​トデータを埋め込み、ベクトルを保存する {#step-6-embed-text-data-and-store-the-vectors}

このステップでは、「dog」、「fish」、「tree」などの単語を含むサンプル文書を準備します。以下のコードは`text_to_embedding()`関数を使用してこれらのテキスト文書をベクトル埋め込みに変換し、ベクトルストアに挿入します。

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

### ステップ7．意味検索を実行する {#step-7-perform-semantic-search}

このステップでは、「泳ぐ動物」という単語を検索しますが、既存の文書にはこの単語と直接一致するものはありません。

以下のコードは`text_to_embedding()`関数を再度使用してクエリテキストをベクトル埋め込みに変換し、その埋め込みを使用してクエリを実行して、最も近い上位 3 つの一致を見つけます。

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

検索結果の 3 つの用語は、クエリされたベクトルからのそれぞれの距離によってソートされます。距離が小さいほど、対応する`document`の関連性が高くなります。

したがって、出力結果から判断すると、泳いでいる動物は魚か、泳ぎの才能に恵まれた犬である可能性が最も高い。

## 関連項目 {#see-also}

-   [ベクトルデータ型](/ai/reference/vector-search-data-types.md)
-   [ベクトル検索インデックス](/ai/reference/vector-search-index.md)
