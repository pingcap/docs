---
title: Integrate TiDB Vector Search with SQLAlchemy
summary: TiDB Vector Search を SQLAlchemy と統合して埋め込みを保存し、セマンティック検索を実行する方法を学習します。
---

# TiDB ベクトル検索を SQLAlchemy と統合する {#integrate-tidb-vector-search-with-sqlalchemy}

このチュートリアルでは、 [SQLアルケミー](https://www.sqlalchemy.org/)使用して[TiDB ベクトル検索](/tidb-cloud/vector-search-overview.md)と対話し、埋め込みを保存し、ベクトル検索クエリを実行する方法について説明します。

> **注記**
>
> TiDB Vector Search は現在ベータ版であり、 [TiDB サーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスターでのみ使用できます。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、次のものが必要です。

-   [Python 3.8以上](https://www.python.org/downloads/)インストールされました。
-   [ギット](https://git-scm.com/downloads)インストールされました。
-   TiDB サーバーレス クラスター。TiDB Cloud クラスターがない場合は、 [TiDB サーバーレス クラスターの作成](/tidb-cloud/create-tidb-cluster-serverless.md)に従って独自のTiDB Cloudクラスターを作成してください。

## サンプルアプリを実行する {#run-the-sample-app}

以下の手順に従って、TiDB Vector Search を SQLAlchemy と統合する方法を簡単に学習できます。

### ステップ1. リポジトリをクローンする {#step-1-clone-the-repository}

`tidb-vector-python`リポジトリをローカル マシンにクローンします。

```shell
git clone https://github.com/pingcap/tidb-vector-python.git
```

### ステップ2. 仮想環境を作成する {#step-2-create-a-virtual-environment}

プロジェクト用の仮想環境を作成します。

```bash
cd tidb-vector-python/examples/orm-sqlalchemy-quickstart
python3 -m venv .venv
source .venv/bin/activate
```

### ステップ3. 必要な依存関係をインストールする {#step-3-install-the-required-dependencies}

デモ プロジェクトに必要な依存関係をインストールします。

```bash
pip install -r requirements.txt
```

既存のプロジェクトの場合は、次のパッケージをインストールできます。

```bash
pip install pymysql python-dotenv sqlalchemy tidb-vector
```

### ステップ4. 環境変数を設定する {#step-4-configure-the-environment-variables}

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログの構成が環境と一致していることを確認します。

    -   **接続タイプ**は`Public`に設定されています。

    -   **ブランチ**は`main`に設定されています。

    -   **Connect With は**`SQLAlchemy`に設定されています。

    -   **オペレーティング システムは**環境に適合します。

    > **ヒント：**
    >
    > プログラムが Windows Subsystem for Linux (WSL) で実行されている場合は、対応する Linux ディストリビューションに切り替えます。

4.  **PyMySQL**タブをクリックし、接続文字列をコピーします。

    > **ヒント：**
    >
    > まだパスワードを設定していない場合は、 **「パスワードの生成」**をクリックしてランダムなパスワードを生成します。

5.  Python プロジェクトのルート ディレクトリに`.env`ファイルを作成し、その中に接続文字列を貼り付けます。

    以下は macOS の例です。

    ```dotenv
    TIDB_DATABASE_URL="mysql+pymysql://<prefix>.root:<password>@gateway01.<region>.prod.aws.tidbcloud.com:4000/test?ssl_ca=/etc/ssl/cert.pem&ssl_verify_cert=true&ssl_verify_identity=true"
    ```

### ステップ5.デモを実行する {#step-5-run-the-demo}

```bash
python sqlalchemy-quickstart.py
```

出力例:

```text
Get 3-nearest neighbor documents:
  - distance: 0.00853986601633272
    document: fish
  - distance: 0.12712843905603044
    document: dog
  - distance: 0.7327387580875756
    document: tree
Get documents within a certain distance:
  - distance: 0.00853986601633272
    document: fish
  - distance: 0.12712843905603044
    document: dog
```

## サンプルコードスニペット {#sample-code-snippets}

アプリケーションを開発するには、次のサンプル コード スニペットを参照してください。

### ベクターテーブルを作成する {#create-vector-tables}

#### TiDBクラスタに接続する {#connect-to-tidb-cluster}

```python
import os
import dotenv

from sqlalchemy import Column, Integer, create_engine, Text
from sqlalchemy.orm import declarative_base, Session
from tidb_vector.sqlalchemy import VectorType

dotenv.load_dotenv()

tidb_connection_string = os.environ['TIDB_DATABASE_URL']
engine = create_engine(tidb_connection_string)
```

#### ベクトル列を定義する {#define-a-vector-column}

3 次元ベクトルを格納する`embedding`という名前の列を持つテーブルを作成します。

```python
Base = declarative_base()

class Document(Base):
    __tablename__ = 'sqlalchemy_demo_documents'
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    embedding = Column(VectorType(3))
```

#### インデックスで最適化されたベクトル列を定義する {#define-a-vector-column-optimized-with-index}

3 次元ベクトル列を定義し、 [ベクトル検索インデックス](/tidb-cloud/vector-search-index.md) (HNSW インデックス) で最適化します。

```python
class DocumentWithIndex(Base):
    __tablename__ = 'sqlalchemy_demo_documents_with_index'
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    embedding = Column(VectorType(3), comment="hnsw(distance=cosine)")
```

TiDB はこのインデックスを使用して、コサイン距離関数に基づくベクトル検索クエリを高速化します。

### 埋め込み付きドキュメントを保存する {#store-documents-with-embeddings}

```python
with Session(engine) as session:
   session.add(Document(content="dog", embedding=[1, 2, 1]))
   session.add(Document(content="fish", embedding=[1, 2, 4]))
   session.add(Document(content="tree", embedding=[1, 0, 0]))
   session.commit()
```

### 最も近い文書を検索する {#search-the-nearest-neighbor-documents}

コサイン距離関数に基づいて、クエリ ベクトル`[1, 2, 3]`に意味的に最も近い上位 3 つのドキュメントを検索します。

```python
with Session(engine) as session:
   distance = Document.embedding.cosine_distance([1, 2, 3]).label('distance')
   results = session.query(
      Document, distance
   ).order_by(distance).limit(3).all()
```

### 特定の距離内の文書を検索する {#search-documents-within-a-certain-distance}

クエリベクトル`[1, 2, 3]`からのコサイン距離が 0.2 未満のドキュメントを検索します。

```python
with Session(engine) as session:
    distance = Document.embedding.cosine_distance([1, 2, 3]).label('distance')
    results = session.query(
        Document, distance
    ).filter(distance < 0.2).order_by(distance).limit(3).all()
```

## 参照 {#see-also}

-   [ベクトルデータ型](/tidb-cloud/vector-search-data-types.md)
-   [ベクター検索インデックス](/tidb-cloud/vector-search-index.md)
