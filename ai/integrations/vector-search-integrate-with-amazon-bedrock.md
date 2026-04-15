---
title: Integrate TiDB Vector Search with Amazon Bedrock
summary: TiDB Vector SearchをAmazon Bedrockと統合して、検索拡張生成（RAG）Q&Aボットを構築する方法を学びましょう。
aliases: ['/ja/tidbcloud/vector-search-integrate-with-amazon-bedrock/']
---

# TiDB Vector SearchをAmazon Bedrockと統合する {#integrate-tidb-vector-search-with-amazon-bedrock}

> **注記：**
>
> このドキュメントはTiDB Cloudにのみ適用され、TiDB Self-Managedには適用されません。

このチュートリアルでは[TiDB ベクトル検索](/ai/concepts/vector-search-overview.md)と[アマゾンの岩盤](https://aws.amazon.com/bedrock/)統合して、検索拡張生成 (RAG) Q&amp;A ボットを構築する方法を説明します。

> **注記：**
>
> -   ベクター検索機能はベータ版です。予告なく変更される場合があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)を報告してください。
> -   ベクトル検索機能は、 [TiDBセルフマネージド](/overview.md)[TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter) 、 [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) 、および[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)で利用できます。TiDB Self-ManagedおよびTiDB Cloud Dedicatedの場合、TiDBのバージョンはv8.4.0以降である必要があります（v8.5.0以降を推奨）。

> **ヒント**
>
> 完全な[サンプルコード](https://github.com/aws-samples/aws-generativeai-partner-samples/blob/main/tidb/samples/tidb-bedrock-boto3-rag.ipynb)Notebook 形式で表示できます。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、以下が必要です。

-   [Python 3.11以降](https://www.python.org/downloads/)インストールされています

-   [ピップ](https://pypi.org/project/pip/)がインストールされました

-   [AWS CLI](https://aws.amazon.com/cli/)がインストールされました

    AWS CLI プロファイルがサポートされている[アマゾンの岩盤](https://aws.amazon.com/bedrock/)リージョンに設定されていることを確認してください。サポートされている地域のリストは[アマゾンの岩盤地帯](https://docs.aws.amazon.com/bedrock/latest/userguide/models-regions.html)でご覧いただけます。サポートされているリージョンに切り替えるには、次のコマンドを実行します。

    ```shell
    aws configure set region <your-region>
    ```

-   TiDB Cloud Starterインスタンス

    お持ちでない場合は、 [TiDB Cloud Starterインスタンスを作成する](/tidb-cloud/select-cluster-tier.md#starter)。

-   [Amazon Bedrockに必要な権限](https://docs.aws.amazon.com/bedrock/latest/userguide/security_iam_id-based-policy-examples.html)AWS アカウントと次のモデルへのアクセス:

    -   **Amazon Titan Embeddings** ( `amazon.titan-embed-text-v2:0` ) は、テキスト埋め込みを生成するために使用されます。
    -   テキスト生成に使用される**メタラマ3** （ `us.meta.llama3-2-3b-instruct-v1:0` ）

    アクセス権がない場合は、 [Amazon Bedrock基盤モデルへのアクセスをリクエストする](https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started.html#getting-started-model-access)手順に従ってください。

## さあ始めましょう {#get-started}

このセクションでは、TiDB Vector SearchをAmazon Bedrockと統合してRAGベースのQ&amp;Aボットを構築するための手順を段階的に説明します。

### ステップ1. 環境変数を設定する {#step-1-set-the-environment-variables}

[TiDB Cloudコンソール](https://tidbcloud.com/)からTiDB接続情報を取得し、開発環境の環境変数を以下のように設定してください。

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、次に、対象のTiDB Cloud Starterインスタンスの名前をクリックして、概要ページに移動します。

2.  右上隅の**「接続」**をクリックしてください。接続ダイアログが表示されます。

3.  接続ダイアログの設定がご使用のオペレーティング環境と一致していることを確認してください。

    -   **接続タイプ**は`Public`に設定されています。

    -   **ブランチ**は`main`に設定されています。

    -   **Connect With は**`General`に設定されています。

    -   お使いの環境に合った**オペレーティングシステム**を選択してください。

    > **ヒント：**
    >
    > プログラムがWindows Subsystem for Linux（WSL）上で実行されている場合は、対応するLinuxディストリビューションに切り替えてください。

4.  **「パスワードを生成」を**クリックすると、ランダムなパスワードが生成されます。

    > **ヒント：**
    >
    > 以前にパスワードを作成したことがある場合は、元のパスワードを使用するか、 **「パスワードをリセット」**をクリックして新しいパスワードを生成できます。

5.  環境変数を設定するには、ターミナルで以下のコマンドを実行してください。コマンド内のプレースホルダーは、接続ダイアログから取得した対応する接続​​パラメータに置き換える必要があります。

    ```shell
    export TIDB_HOST=<your-tidb-host>
    export TIDB_PORT=4000
    export TIDB_USER=<your-tidb-user>
    export TIDB_PASSWORD=<your-tidb-password>
    export TIDB_DB_NAME=test
    ```

### ステップ2. Python仮想環境をセットアップする {#step-2-set-up-the-python-virtual-environment}

1.  `demo.py`という名前の Python ファイルを作成します。

    ```shell
    touch demo.py
    ```

2.  依存関係を管理するための仮想環境を作成してアクティブ化する：

    ```shell
    python3 -m venv env
    source env/bin/activate  # On Windows, use env\Scripts\activate
    ```

3.  必要な依存関係をインストールします。

    ```shell
    pip install SQLAlchemy==2.0.30 PyMySQL==1.1.0 tidb-vector==0.0.9 pydantic==2.7.1 boto3
    ```

### ステップ3. 必要なライブラリをインポートする {#step-3-import-required-libraries}

必要なライブラリをインポートするには、 `demo.py`の先頭に次のコードを追加してください。

```python
import os
import json
import boto3
from sqlalchemy import Column, Integer, Text, create_engine
from sqlalchemy.orm import declarative_base, Session
from tidb_vector.sqlalchemy import VectorType
```

### ステップ4．データベース接続の設定 {#step-4-configure-the-database-connection}

`demo.py`に、データベース接続を設定するための以下のコードを追加します。

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

### ステップ5. Bedrockランタイムクライアントを使用してAmazon Titan Text Embeddings V2モデルを呼び出します。 {#step-5-invoke-the-amazon-titan-text-embeddings-v2-model-using-the-bedrock-runtime-client}

Amazon Bedrock ランタイム クライアントは、次のパラメーターを受け入れる`invoke_model` API を提供します。

-   `modelId` : Amazon Bedrock で利用可能な基盤モデルのモデル ID。
-   `accept` : 入力リクエストのタイプ。
-   `contentType` : 入力のコンテンツタイプ。
-   `body` : プロンプトと設定で構成される JSON 文字列ペイロード。

`demo.py`に次のコードを追加して、 `invoke_model` API を呼び出し、Amazon Titan Text Embeddings を使用してテキスト埋め込みを生成し、Meta Llama 3 から応答を取得します。

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

### ステップ6. ベクターテーブルを作成する {#step-6-create-a-vector-table}

`demo.py`に、テキストとベクター埋め込みを格納するベクターテーブルを作成するための以下のコードを追加します。

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

### ステップ7. ベクターデータをTiDB Cloud Starterに保存します。 {#step-7-save-the-vector-data-to-tidb-cloud-starter}

`demo.py`に、ベクトルデータをTiDB Cloud Starterインスタンスに保存するための以下のコードを追加します。

```python
# ---- Saving Vectors to TiDB ----
def save_entities_with_embedding(session, contents):
    """Save multiple entities with their embeddings to the TiDB database."""
    for content in contents:
        entity = Entity(content=content, content_vec=embedding(content))
        session.add(entity)
    session.commit()
```

### ステップ8．アプリケーションを実行する {#step-8-run-the-application}

1.  `demo.py`に、データベースセッションを確立し、埋め込みを TiDB に保存し、例となる質問 (「TiDB とは何ですか？」など) を尋ね、モデルから結果を生成するための以下のコードを追加します。

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

2.  `demo.py`へのすべての変更を保存し、スクリプトを実行します。

    ```shell
    python3 demo.py
    ```

    期待される出力は以下のようになります。

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

## 関連項目 {#see-also}

-   [ベクトルデータ型](/ai/reference/vector-search-data-types.md)
-   [ベクトル検索インデックス](/ai/reference/vector-search-index.md)
