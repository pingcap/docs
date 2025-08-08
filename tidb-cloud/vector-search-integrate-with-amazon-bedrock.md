---
title: Integrate TiDB Vector Search with Amazon Bedrock
summary: TiDB Vector Search を Amazon Bedrock と統合して、検索拡張生成 (RAG) Q&A ボットを構築する方法を学びます。
---

# TiDB Vector Search を Amazon Bedrock に統合する {#integrate-tidb-vector-search-with-amazon-bedrock}

このチュートリアルでは、TiDB の[ベクトル検索](/vector-search/vector-search-overview.md)機能を[アマゾンの岩盤](https://aws.amazon.com/bedrock/)と統合して、検索拡張生成 (RAG) Q&amp;A ボットを構築する方法を説明します。

<CustomContent platform="tidb-cloud">

> **注記：**
>
> ベクター検索機能はベータ版です。予告なく変更される可能性があります。バグを見つけた場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)報告を行ってください。

</CustomContent>

> **注記**
>
> ベクトル検索機能は、TiDB Self-Managed、 [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) [TiDB Cloud専用](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated)利用できます。TiDB Self-ManagedおよびTiDB Cloud Dedicatedの場合、TiDBバージョンはv8.4.0以降である必要があります（v8.5.0以降を推奨）。

> **ヒント**
>
> [サンプルコード](https://github.com/aws-samples/aws-generativeai-partner-samples/blob/main/tidb/samples/tidb-bedrock-boto3-rag.ipynb)全体をノートブック形式で閲覧できます。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、次のものが必要です。

-   [Python 3.11以降](https://www.python.org/downloads/)インストール済み

-   [ピップ](https://pypi.org/project/pip/)インストール済み

-   [AWS CLI](https://aws.amazon.com/cli/)インストール済み

    このチュートリアルでは、AWS CLI プロファイルがサポートされている[アマゾンの岩盤](https://aws.amazon.com/bedrock/)リージョンに設定されていることを確認してください。サポートされているリージョンの一覧は[アマゾンの岩盤地域](https://docs.aws.amazon.com/bedrock/latest/userguide/models-regions.html)にあります。サポートされているリージョンに切り替えるには、次のコマンドを実行します。

    ```shell
    aws configure set region <your-region>
    ```

-   TiDB Cloudサーバーレスクラスター

    独自のTiDB Cloudクラスターがない場合は、手順[TiDB Cloud Serverless クラスターの作成](/tidb-cloud/create-tidb-cluster-serverless.md)に従って作成します。

-   [Amazon Bedrock に必要な権限](https://docs.aws.amazon.com/bedrock/latest/userguide/security_iam_id-based-policy-examples.html)と次のモデルへのアクセス権を持つ AWS アカウント:

    -   **Amazon Titan Embeddings** ( `amazon.titan-embed-text-v2:0` ) テキスト埋め込みの生成に使用される
    -   **Meta Llama 3** ( `us.meta.llama3-2-3b-instruct-v1:0` )、テキスト生成に使用される

    アクセスできない場合は、 [Amazon Bedrock 基盤モデルへのアクセスをリクエストする](https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started.html#getting-started-model-access)の手順に従ってください。

## 始めましょう {#get-started}

このセクションでは、TiDB Vector Search を Amazon Bedrock と統合して RAG ベースの Q&amp;A ボットを構築するための手順を段階的に説明します。

### ステップ1.環境変数を設定する {#step-1-set-the-environment-variables}

[TiDB Cloudコンソール](https://tidbcloud.com/)から TiDB 接続情報を取得し、開発環境で環境変数を次のように設定します。

1.  [**クラスター**](https://tidbcloud.com/project/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログの構成が動作環境と一致していることを確認します。

    -   **接続タイプ**は`Public`に設定されています

    -   **ブランチ**は`main`に設定されています

    -   **接続先が**`General`に設定されています

    -   **オペレーティング システムは**環境に適合します。

    > **ヒント：**
    >
    > プログラムが Windows Subsystem for Linux (WSL) で実行されている場合は、対応する Linux ディストリビューションに切り替えます。

4.  ランダムなパスワードを作成するには、 **「パスワードの生成」を**クリックします。

    > **ヒント：**
    >
    > 以前にパスワードを作成したことがある場合は、元のパスワードを使用するか、 **「パスワードのリセット」を**クリックして新しいパスワードを生成することができます。

5.  環境変数を設定するには、ターミナルで以下のコマンドを実行します。コマンド内のプレースホルダーは、接続ダイアログから取得した対応する接続パラメータに置き換えてください。

    ```shell
    export TIDB_HOST=<your-tidb-host>
    export TIDB_PORT=4000
    export TIDB_USER=<your-tidb-user>
    export TIDB_PASSWORD=<your-tidb-password>
    export TIDB_DB_NAME=test
    ```

### ステップ2. Python仮想環境を設定する {#step-2-set-up-the-python-virtual-environment}

1.  `demo.py`という名前の Python ファイルを作成します。

    ```shell
    touch demo.py
    ```

2.  依存関係を管理するために仮想環境を作成してアクティブ化します。

    ```shell
    python3 -m venv env
    source env/bin/activate  # On Windows, use env\Scripts\activate
    ```

3.  必要な依存関係をインストールします。

    ```shell
    pip install SQLAlchemy==2.0.30 PyMySQL==1.1.0 tidb-vector==0.0.9 pydantic==2.7.1 boto3
    ```

### ステップ3. 必要なライブラリをインポートする {#step-3-import-required-libraries}

必要なライブラリをインポートするには、 `demo.py`の先頭に次のコードを追加します。

```python
import os
import json
import boto3
from sqlalchemy import Column, Integer, Text, create_engine
from sqlalchemy.orm import declarative_base, Session
from tidb_vector.sqlalchemy import VectorType
```

### ステップ4. データベース接続を構成する {#step-4-configure-the-database-connection}

`demo.py`で、次のコードを追加してデータベース接続を構成します。

```python
# ---- Configuration Setup ----
# Set environment variables: TIDB_HOST, TIDB_PORT, TIDB_USER, TIDB_PASSWORD, TIDB_DB_NAME
TIDB_HOST = os.environ.get("TIDB_HOST")
TIDB_PORT = os.environ.get("TIDB_PORT")
TIDB_USER = os.environ.get("TIDB_USER")
TIDB_PASSWORD = os.environ.get("TIDB_PASSWORD")
TIDB_DB_NAME = os.environ.get("TIDB_DB_NAME")

# ---- Database Setup ----
def get_db_url():
    """Build the database connection URL."""
    return f"mysql+pymysql://{TIDB_USER}:{TIDB_PASSWORD}@{TIDB_HOST}:{TIDB_PORT}/{TIDB_DB_NAME}?ssl_verify_cert=True&ssl_verify_identity=True"

# Create engine
engine = create_engine(get_db_url(), pool_recycle=300)
Base = declarative_base()
```

### ステップ 5. Bedrock ランタイム クライアントを使用して Amazon Titan Text Embeddings V2 モデルを呼び出す {#step-5-invoke-the-amazon-titan-text-embeddings-v2-model-using-the-bedrock-runtime-client}

Amazon Bedrock ランタイムクライアントは、次のパラメータを受け入れる`invoke_model` API を提供します。

-   `modelId` : Amazon Bedrock で利用可能な基盤モデルのモデル ID。
-   `accept` : 入力要求のタイプ。
-   `contentType` : 入力のコンテンツ タイプ。
-   `body` : プロンプトと構成で構成される JSON 文字列ペイロード。

`demo.py`に次のコードを追加して`invoke_model` API を呼び出し、Amazon Titan Text Embeddings を使用してテキスト埋め込みを生成し、Meta Llama 3 からの応答を取得します。

```python
# Bedrock Runtime Client Setup
bedrock_runtime = boto3.client('bedrock-runtime')

# ---- Model Invocation ----
embedding_model_name = "amazon.titan-embed-text-v2:0"
dim_of_embedding_model = 512
llm_name = "us.meta.llama3-2-3b-instruct-v1:0"


def embedding(content):
    """Invoke Amazon Bedrock to get text embeddings."""
    payload = {
        "modelId": embedding_model_name,
        "contentType": "application/json",
        "accept": "*/*",
        "body": {
            "inputText": content,
            "dimensions": dim_of_embedding_model,
            "normalize": True,
        }
    }

    body_bytes = json.dumps(payload['body']).encode('utf-8')

    response = bedrock_runtime.invoke_model(
        body=body_bytes,
        contentType=payload['contentType'],
        accept=payload['accept'],
        modelId=payload['modelId']
    )

    result_body = json.loads(response.get("body").read())
    return result_body.get("embedding")


def generate_result(query: str, info_str: str):
    """Generate answer using Meta Llama 3 model."""
    prompt = f"""
    ONLY use the content below to generate an answer:
    {info_str}

    ----
    Please carefully think about the question: {query}
    """

    payload = {
        "modelId": llm_name,
        "contentType": "application/json",
        "accept": "application/json",
        "body": {
            "prompt": prompt,
            "temperature": 0
        }
    }

    body_bytes = json.dumps(payload['body']).encode('utf-8')

    response = bedrock_runtime.invoke_model(
        body=body_bytes,
        contentType=payload['contentType'],
        accept=payload['accept'],
        modelId=payload['modelId']
    )

    result_body = json.loads(response.get("body").read())
    completion = result_body["generation"]
    return completion
```

### ステップ6.ベクターテーブルを作成する {#step-6-create-a-vector-table}

`demo.py`に次のコードを追加して、テキストとベクトル埋め込みを格納するベクトル テーブルを作成します。

```python
# ---- TiDB Setup and Vector Index Creation ----
class Entity(Base):
    """Define the Entity table with a vector index."""
    __tablename__ = "entity"
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    content_vec = Column(VectorType(dim=dim_of_embedding_model), comment="hnsw(distance=l2)")

# Create the table in TiDB
Base.metadata.create_all(engine)
```

### ステップ7. ベクターデータをTiDB Cloud Serverlessに保存する {#step-7-save-the-vector-data-to-tidb-cloud-serverless}

`demo.py`で、次のコードを追加して、ベクター データをTiDB Cloud Serverless クラスターに保存します。

```python
# ---- Saving Vectors to TiDB ----
def save_entities_with_embedding(session, contents):
    """Save multiple entities with their embeddings to the TiDB Serverless database."""
    for content in contents:
        entity = Entity(content=content, content_vec=embedding(content))
        session.add(entity)
    session.commit()
```

### ステップ8. アプリケーションを実行する {#step-8-run-the-application}

1.  `demo.py`では、次のコードを追加して、データベース セッションを確立し、埋め込みを TiDB に保存し、サンプルの質問 (「TiDB とは何ですか?」など) を尋ね、モデルから結果を生成します。

    ```python
    if __name__ == "__main__":
        # Establish a database session
        with Session(engine) as session:
            # Example data
            contents = [
                "TiDB is a distributed SQL database compatible with MySQL.",
                "TiDB supports Hybrid Transactional and Analytical Processing (HTAP).",
                "TiDB can scale horizontally and provides high availability.",
                "Amazon Bedrock allows seamless integration with foundation models.",
                "Meta Llama 3 is a powerful model for text generation."
            ]

            # Save embeddings to TiDB
            save_entities_with_embedding(session, contents)

            # Example query
            query = "What is TiDB?"
            info_str = " ".join(contents)

            # Generate result from Meta Llama 3
            result = generate_result(query, info_str)
            print(f"Generated answer: {result}")
    ```

2.  すべての変更を`demo.py`に保存し、スクリプトを実行します。

    ```shell
    python3 demo.py
    ```

    期待される出力は次のようになります。

        Generated answer:  What is the main purpose of TiDB?
             What are the key features of TiDB?
             What are the key benefits of TiDB?

            ----
            Based on the provided text, here is the answer to the question:
            What is TiDB?
            TiDB is a distributed SQL database compatible with MySQL.

        ## Step 1: Understand the question
        The question asks for the definition of TiDB.

        ## Step 2: Identify the key information
        The key information provided in the text is that TiDB is a distributed SQL database compatible with MySQL.

        ## Step 3: Provide the answer
        Based on the provided text, TiDB is a distributed SQL database compatible with MySQL.

        The final answer is: TiDB is a distributed SQL database compatible with MySQL.

## 参照 {#see-also}

-   [ベクトルデータ型](/vector-search/vector-search-data-types.md)
-   [ベクター検索インデックス](/vector-search/vector-search-index.md)
