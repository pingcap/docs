---
title: Integrate TiDB Vector Search with Jina AI Embeddings API
summary: TiDB Vector SearchをJina AI Embeddings APIと統合して、埋め込みデータを保存し、セマンティック検索を実行する方法を学びましょう。
aliases: ['/ja/tidb/stable/vector-search-integrate-with-jinaai-embedding/','/ja/tidb/dev/vector-search-integrate-with-jinaai-embedding/','/ja/tidbcloud/vector-search-integrate-with-jinaai-embedding/']
---

# TiDBベクトル検索をJina AI埋め込みAPIと統合する {#integrate-tidb-vector-search-with-jina-ai-embeddings-api}

このチュートリアルでは[ジナAI](https://jina.ai/)を使用してテキスト埋め込みを生成し、TiDBに保存し、埋め込みに基づいて類似のテキストを検索する方法を順を追って説明します。

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

## サンプルアプリを実行します {#run-the-sample-app}

以下の手順に従うことで、TiDB Vector SearchをJina AIの埋め込み機能と統合する方法をすぐに習得できます。

### ステップ1. リポジトリをクローンする {#step-1-clone-the-repository}

`tidb-vector-python`リポジトリをローカルマシンにクローンします。

```shell
git clone https://github.com/pingcap/tidb-vector-python.git
```

### ステップ2. 仮想環境を作成する {#step-2-create-a-virtual-environment}

プロジェクト用の仮想環境を作成する：

```bash
cd tidb-vector-python/examples/jina-ai-embeddings-demo
python3 -m venv .venv
source .venv/bin/activate
```

### ステップ3. 必要な依存関係をインストールします {#step-3-install-required-dependencies}

デモプロジェクトに必要な依存関係をインストールします。

```bash
pip install -r requirements.txt
```

### ステップ4．環境変数を設定する {#step-4-configure-the-environment-variables}

Jina AIのAPIキーを[Jina AI 埋め込み API](https://jina.ai/embeddings/)ページから取得し、選択したTiDBデプロイメントオプションに応じて環境変数を設定してください。

<SimpleTab>
<div label="TiDB Cloud Starter or Essential">

TiDB Cloud StarterまたはEssentialインスタンスの場合、接続文字列を取得し、環境変数を設定するには、以下の手順に従ってください。

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud StarterまたはEssentialインスタンスの名前をクリックして、概要ページに移動します。

2.  右上隅の**「接続」**をクリックしてください。接続ダイアログが表示されます。

3.  接続ダイアログの設定がご使用のオペレーティング環境と一致していることを確認してください。

    -   **接続タイプ**は`Public`に設定されています。

    -   **ブランチ**は`main`に設定されています。

    -   **Connect With は**`SQLAlchemy`に設定されています。

    -   お使いの環境に合った**オペレーティングシステム**を選択してください。

    > **ヒント：**
    >
    > プログラムがWindows Subsystem for Linux（WSL）上で実行されている場合は、対応するLinuxディストリビューションに切り替えてください。

4.  **PyMySQL**タブに切り替えて、**コピー**アイコンをクリックして接続文字列をコピーします。

    > **ヒント：**
    >
    > まだパスワードを設定していない場合は、 **「パスワードを作成」**をクリックしてランダムなパスワードを生成してください。

5.  ターミナルで Jina AI API キーと TiDB 接続文字列を環境変数として設定するか、以下の環境変数を含む`.env`ファイルを作成してください。

    ```dotenv
    JINAAI_API_KEY="****"
    TIDB_DATABASE_URL="{tidb_connection_string}"
    ```

    以下はmacOS用の接続文字列の例です。

    ```dotenv
    TIDB_DATABASE_URL="mysql+pymysql://<prefix>.root:<password>@gateway01.<region>.prod.aws.tidbcloud.com:4000/test?ssl_ca=/etc/ssl/cert.pem&ssl_verify_cert=true&ssl_verify_identity=true"
    ```

</div>
<div label="TiDB Self-Managed" value="tidb">

TiDBセルフマネージドクラスタの場合、ターミナルで次のように環境変数を設定してTiDBクラスタに接続します。

```shell
export JINA_API_KEY="****"
export TIDB_DATABASE_URL="mysql+pymysql://<USERNAME>:<PASSWORD>@<HOST>:<PORT>/<DATABASE>"
# For example: export TIDB_DATABASE_URL="mysql+pymysql://root@127.0.0.1:4000/test"
```

ご使用の TiDB クラスタに合わせて、上記のコマンドのパラメータを置き換える必要があります。ローカル マシンで TiDB を実行している場合、 `<HOST>`はデフォルトで`127.0.0.1`になります。初期値の`<PASSWORD>`は空なので、クラスタを初めて起動する場合はこのフィールドを省略できます。

各パラメータの説明は以下のとおりです。

-   `<USERNAME>` : TiDBに接続するためのユーザー名。
-   `<PASSWORD>` : TiDBに接続するためのパスワード。
-   `<HOST>` : TiDBクラスタのホスト。
-   `<PORT>` : TiDB クラスタのポート。
-   `<DATABASE>` : 接続するデータベースの名前。

</div>

</SimpleTab>

### ステップ5．デモを実行する {#step-5-run-the-demo}

```bash
python jina-ai-embeddings-demo.py
```

出力例：

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

### Jina AIから埋め込みデータを取得する {#get-embeddings-from-jina-ai}

`generate_embeddings` AI埋め込みAPIを呼び出すためのヘルパー関数を定義します。

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

### TiDBに接続する {#connect-to-tidb}

SQLAlchemy経由でTiDBに接続する：

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

### ベクトルテーブルのスキーマを定義します {#define-the-vector-table-schema}

`jinaai_tidb_demo_documents`という名前のテーブルを作成し、テキストを格納するための`content`列と、埋め込みを格納するための`content_vec`という名前のベクトル列を作成します。

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
> -   ベクトル列の次元は、埋め込みモデルによって生成される埋め込みの次元と一致していなければなりません。
> -   この例では、 `jina-embeddings-v2-base-en`モデルによって生成される埋め込みの次元は`768`です。

### Jina AIで埋め込みを作成し、TiDBに保存します。 {#create-embeddings-with-jina-ai-and-store-in-tidb}

Jina AI Embeddings APIを使用して、各テキストの埋め込みを生成し、その埋め込みをTiDBに保存します。

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

### TiDBでJina AI埋め込みを用いたセマンティック検索を実行する {#perform-semantic-search-with-jina-ai-embeddings-in-tidb}

Jina AIの埋め込みAPIを使用してクエリテキストの埋め込みを生成し、**クエリテキストの埋め込み**と**ベクトルテーブル内の各埋め込み**との間のコサイン距離に基づいて最も関連性の高いドキュメントを検索します。

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

## 関連項目 {#see-also}

-   [ベクトルデータ型](/ai/reference/vector-search-data-types.md)
-   [ベクトル検索インデックス](/ai/reference/vector-search-index.md)
