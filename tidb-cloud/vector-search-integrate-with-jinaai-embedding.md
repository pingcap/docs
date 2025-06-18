---
title: Integrate TiDB Vector Search with Jina AI Embeddings API
summary: TiDB Vector Search を Jina AI Embeddings API と統合して埋め込みを保存し、セマンティック検索を実行する方法を学習します。
---

# TiDBベクトル検索をJina AI Embeddings APIと統合する {#integrate-tidb-vector-search-with-jina-ai-embeddings-api}

このチュートリアルでは、 [ジナ・アイ](https://jina.ai/)使用してテキスト データの埋め込みを生成し、その埋め込みを TiDB ベクトルstorageに保存して、埋め込みに基づいて類似のテキストを検索する方法について説明します。

> **注記**
>
> TiDB Vector Searchは、TiDB Self-Managed (TiDB &gt;= v8.4)および[TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)のみ利用できます。 [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)では利用できません。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、次のものが必要です。

-   [Python 3.8以上](https://www.python.org/downloads/)個インストールされました。
-   [ギット](https://git-scm.com/downloads)個インストールされました。
-   TiDB Cloud Serverless クラスター。TiDB Cloud クラスターがまだない場合は、 [TiDB Cloud Serverless クラスターの作成](/tidb-cloud/create-tidb-cluster-serverless.md)に従って独自のTiDB Cloudクラスターを作成してください。

## サンプルアプリを実行する {#run-the-sample-app}

以下の手順に従って、TiDB Vector Search を JinaAI Embedding と統合する方法を簡単に学習できます。

### ステップ1. リポジトリのクローンを作成する {#step-1-clone-the-repository}

`tidb-vector-python`リポジトリをローカル マシンにクローンします。

```shell
git clone https://github.com/pingcap/tidb-vector-python.git
```

### ステップ2. 仮想環境を作成する {#step-2-create-a-virtual-environment}

プロジェクト用の仮想環境を作成します。

```bash
cd tidb-vector-python/examples/jina-ai-embeddings-demo
python3 -m venv .venv
source .venv/bin/activate
```

### ステップ3. 必要な依存関係をインストールする {#step-3-install-required-dependencies}

デモ プロジェクトに必要な依存関係をインストールします。

```bash
pip install -r requirements.txt
```

### ステップ4.環境変数を設定する {#step-4-configure-the-environment-variables}

[Jina AI 埋め込み API](https://jina.ai/embeddings/)ページ目からJina AI APIキーを取得します。次に、クラスター接続文字列を取得し、環境変数を以下のように設定します。

1.  [**クラスター**](https://tidbcloud.com/project/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログの構成が動作環境と一致していることを確認します。

    -   **接続タイプ**は`Public`に設定されています

    -   **ブランチ**は`main`に設定されています

    -   **接続先が**`SQLAlchemy`に設定されています

    -   **オペレーティング システムは**環境に適合します。

    > **ヒント：**
    >
    > プログラムが Windows Subsystem for Linux (WSL) で実行されている場合は、対応する Linux ディストリビューションに切り替えます。

4.  **PyMySQL**タブに切り替えて、**コピー**アイコンをクリックして接続文字列をコピーします。

    > **ヒント：**
    >
    > まだパスワードを設定していない場合は、 **「パスワードの作成」**をクリックしてランダムなパスワードを生成します。

5.  ターミナルで Jina AI API キーと TiDB 接続文字列を環境変数として設定するか、次の環境変数を含む`.env`ファイルを作成します。

    ```dotenv
    JINAAI_API_KEY="****"
    TIDB_DATABASE_URL="{tidb_connection_string}"
    ```

    以下は macOS の接続文字列の例です。

    ```dotenv
    TIDB_DATABASE_URL="mysql+pymysql://<prefix>.root:<password>@gateway01.<region>.prod.aws.tidbcloud.com:4000/test?ssl_ca=/etc/ssl/cert.pem&ssl_verify_cert=true&ssl_verify_identity=true"
    ```

### ステップ5.デモを実行する {#step-5-run-the-demo}

```bash
python jina-ai-embeddings-demo.py
```

出力例:

```text
- Inserting Data to TiDB...
  - Inserting: Jina AI offers best-in-class embeddings, reranker and prompt optimizer, enabling advanced multimodal AI.
  - Inserting: TiDB is an open-source MySQL-compatible database that supports Hybrid Transactional and Analytical Processing (HTAP) workloads.
- List All Documents and Their Distances to the Query:
  - distance: 0.3585317326132522
    content: Jina AI offers best-in-class embeddings, reranker and prompt optimizer, enabling advanced multimodal AI.
  - distance: 0.10858102967720984
    content: TiDB is an open-source MySQL-compatible database that supports Hybrid Transactional and Analytical Processing (HTAP) workloads.
- The Most Relevant Document and Its Distance to the Query:
  - distance: 0.10858102967720984
    content: TiDB is an open-source MySQL-compatible database that supports Hybrid Transactional and Analytical Processing (HTAP) workloads.
```

## サンプルコードスニペット {#sample-code-snippets}

### Jina AIから埋め込みを取得する {#get-embeddings-from-jina-ai}

Jina AI 埋め込み API を呼び出す`generate_embeddings`ヘルパー関数を定義します。

```python
import os
import requests
import dotenv

dotenv.load_dotenv()

JINAAI_API_KEY = os.getenv('JINAAI_API_KEY')

def generate_embeddings(text: str):
    JINAAI_API_URL = 'https://api.jina.ai/v1/embeddings'
    JINAAI_HEADERS = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {JINAAI_API_KEY}'
    }
    JINAAI_REQUEST_DATA = {
        'input': [text],
        'model': 'jina-embeddings-v2-base-en'  # with dimension 768.
    }
    response = requests.post(JINAAI_API_URL, headers=JINAAI_HEADERS, json=JINAAI_REQUEST_DATA)
    return response.json()['data'][0]['embedding']
```

### TiDBクラスタに接続する {#connect-to-the-tidb-cluster}

SQLAlchemy を介して TiDB クラスターに接続します。

```python
import os
import dotenv

from tidb_vector.sqlalchemy import VectorType
from sqlalchemy.orm import Session, declarative_base

dotenv.load_dotenv()

TIDB_DATABASE_URL = os.getenv('TIDB_DATABASE_URL')
assert TIDB_DATABASE_URL is not None
engine = create_engine(url=TIDB_DATABASE_URL, pool_recycle=300)
```

### ベクターテーブルスキーマを定義する {#define-the-vector-table-schema}

テキストを格納するための`content`列と、埋め込みを格納するための`content_vec`名前のベクトル列を持つ`jinaai_tidb_demo_documents`という名前のテーブルを作成します。

```python
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Document(Base):
    __tablename__ = "jinaai_tidb_demo_documents"

    id = Column(Integer, primary_key=True)
    content = Column(String(255), nullable=False)
    content_vec = Column(
        # DIMENSIONS is determined by the embedding model,
        # for Jina AI's jina-embeddings-v2-base-en model it's 768.
        VectorType(dim=768),
        comment="hnsw(distance=cosine)"
```

> **注記：**
>
> -   ベクトル列の次元は、埋め込みモデルによって生成された埋め込みの次元と一致する必要があります。
> -   この例では、 `jina-embeddings-v2-base-en`モデルによって生成される埋め込みの次元は`768`です。

### Jina AIで埋め込みを作成し、TiDBに保存する {#create-embeddings-with-jina-ai-and-store-in-tidb}

Jina AI Embeddings API を使用して、各テキストの埋め込みを生成し、TiDB に保存します。

```python
TEXTS = [
   'Jina AI offers best-in-class embeddings, reranker and prompt optimizer, enabling advanced multimodal AI.',
   'TiDB is an open-source MySQL-compatible database that supports Hybrid Transactional and Analytical Processing (HTAP) workloads.',
]
data = []

for text in TEXTS:
    # Generate embeddings for the texts via Jina AI API.
    embedding = generate_embeddings(text)
    data.append({
        'text': text,
        'embedding': embedding
    })

with Session(engine) as session:
   print('- Inserting Data to TiDB...')
   for item in data:
      print(f'  - Inserting: {item["text"]}')
      session.add(Document(
         content=item['text'],
         content_vec=item['embedding']
      ))
   session.commit()
```

### TiDB で Jina AI 埋め込みを使用してセマンティック検索を実行する {#perform-semantic-search-with-jina-ai-embeddings-in-tidb}

Jina AI 埋め込み API を使用してクエリ テキストの埋め込みを生成し、**クエリ テキストの埋め込み**と**ベクトル テーブル内の各埋め込み**間のコサイン距離に基づいて最も関連性の高いドキュメントを検索します。

```python
query = 'What is TiDB?'
# Generate the embedding for the query via Jina AI API.
query_embedding = generate_embeddings(query)

with Session(engine) as session:
    print('- The Most Relevant Document and Its Distance to the Query:')
    doc, distance = session.query(
        Document,
        Document.content_vec.cosine_distance(query_embedding).label('distance')
    ).order_by(
        'distance'
    ).limit(1).first()
    print(f'  - distance: {distance}\n'
          f'    content: {doc.content}')
```

## 参照 {#see-also}

-   [ベクトルデータ型](/tidb-cloud/vector-search-data-types.md)
-   [ベクター検索インデックス](/tidb-cloud/vector-search-index.md)
