---
title: Integrate TiDB Vector Search with Jina AI Embeddings API
summary: TiDB Vector Search を Jina AI Embeddings API と統合して埋め込みを保存し、セマンティック検索を実行する方法を学習します。
---

# TiDBベクトル検索をJina AI Embeddings APIと統合する {#integrate-tidb-vector-search-with-jina-ai-embeddings-api}

このチュートリアルでは、 [ジナ・アイ](https://jina.ai/)使用してテキスト データの埋め込みを生成し、その埋め込みを TiDB ベクトルstorageに保存して、埋め込みに基づいて類似のテキストを検索する方法について説明します。

<CustomContent platform="tidb">

> **警告：**
>
> ベクトル検索機能は実験的です。本番環境での使用は推奨されません。この機能は予告なく変更される可能性があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)報告を行ってください。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> ベクター検索機能はベータ版です。予告なく変更される可能性があります。バグを見つけた場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)報告を行ってください。

</CustomContent>

> **注記：**
>
> ベクトル検索機能は、TiDB Self-Managed、 [TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) [TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)利用できます[TiDB Cloud専用](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated) Self-Managed およびTiDB Cloud Dedicated の場合、TiDB バージョンは v8.4.0 以降である必要があります（v8.5.0 以降を推奨）。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、次のものが必要です。

-   [Python 3.8以上](https://www.python.org/downloads/)個インストールされました。
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

[Jina AI 埋め込み API](https://jina.ai/embeddings/)ページから Jina AI API キーを取得し、選択した TiDB デプロイメント オプションに応じて環境変数を構成します。

<SimpleTab>
<div label="TiDB Cloud Starter or Essential">

TiDB Cloud Starter クラスターの場合、次の手順に従ってクラスター接続文字列を取得し、環境変数を構成します。

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

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

</div>
<div label="TiDB Self-Managed">

TiDB セルフマネージド クラスターの場合は、ターミナルで TiDB クラスターに接続するための環境変数を次のように設定します。

```shell
export JINA_API_KEY="****"
export TIDB_DATABASE_URL="mysql+pymysql://<USERNAME>:<PASSWORD>@<HOST>:<PORT>/<DATABASE>"
# For example: export TIDB_DATABASE_URL="mysql+pymysql://root@127.0.0.1:4000/test"
```

上記のコマンドのパラメータは、TiDB クラスターに応じて変更する必要があります。ローカルマシンで TiDB を実行している場合、デフォルトでは`<HOST>`が`127.0.0.1`設定されます。初期の`<PASSWORD>`空なので、クラスターを初めて起動する場合はこのフィールドを省略できます。

各パラメータの説明は次のとおりです。

-   `<USERNAME>` : TiDB クラスターに接続するためのユーザー名。
-   `<PASSWORD>` : TiDB クラスターに接続するためのパスワード。
-   `<HOST>` : TiDB クラスターのホスト。
-   `<PORT>` : TiDB クラスターのポート。
-   `<DATABASE>` : 接続するデータベースの名前。

</div>

</SimpleTab>

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

-   [ベクトルデータ型](/vector-search/vector-search-data-types.md)
-   [ベクター検索インデックス](/vector-search/vector-search-index.md)
