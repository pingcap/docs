---
title: Integrate TiDB Vector Search with peewee
summary: TiDB Vector Search を peewee と統合して埋め込みを保存し、セマンティック検索を実行する方法を学習します。
---

# TiDB Vector Search を peewee と統合する {#integrate-tidb-vector-search-with-peewee}

このチュートリアルでは、 [ピーウィー](https://docs.peewee-orm.com/)使用して[TiDB ベクトル検索](/tidb-cloud/vector-search-overview.md)と対話し、埋め込みを保存し、ベクトル検索クエリを実行する方法について説明します。

> **注記**
>
> TiDB Vector Search は現在ベータ版であり、 [TiDB サーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスターでのみ使用できます。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、次のものが必要です。

-   [Python 3.8以上](https://www.python.org/downloads/)インストールされました。
-   [ギット](https://git-scm.com/downloads)インストールされました。
-   TiDB サーバーレス クラスター。TiDB クラウド クラスターがない場合は、 [TiDB サーバーレス クラスターの作成](/tidb-cloud/create-tidb-cluster-serverless.md)に従って独自のTiDB Cloudクラスターを作成します。

## サンプルアプリを実行する {#run-the-sample-app}

以下の手順に従って、TiDB Vector Search を peewee と統合する方法を簡単に学習できます。

### ステップ1. リポジトリをクローンする {#step-1-clone-the-repository}

[`tidb-vector-python`](https://github.com/pingcap/tidb-vector-python)リポジトリをローカル マシンにクローンします。

```shell
git clone https://github.com/pingcap/tidb-vector-python.git
```

### ステップ2. 仮想環境を作成する {#step-2-create-a-virtual-environment}

プロジェクト用の仮想環境を作成します。

```bash
cd tidb-vector-python/examples/orm-peewee-quickstart
python3 -m venv .venv
source .venv/bin/activate
```

### ステップ3. 必要な依存関係をインストールする {#step-3-install-required-dependencies}

デモ プロジェクトに必要な依存関係をインストールします。

```bash
pip install -r requirements.txt
```

既存のプロジェクトの場合は、次のパッケージをインストールできます。

```bash
pip install peewee pymysql python-dotenv tidb-vector
```

### ステップ4. 環境変数を設定する {#step-4-configure-the-environment-variables}

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログの構成が動作環境と一致していることを確認します。

    -   **エンドポイント タイプは**`Public`に設定されています。

    -   **ブランチ**は`main`に設定されています。

    -   **Connect With は**`General`に設定されています。

    -   **オペレーティング システムは**環境に適合します。

    > **ヒント：**
    >
    > プログラムが Windows Subsystem for Linux (WSL) で実行されている場合は、対応する Linux ディストリビューションに切り替えます。

4.  接続ダイアログから接続パラメータをコピーします。

    > **ヒント：**
    >
    > まだパスワードを設定していない場合は、 **「パスワードの生成」**をクリックしてランダムなパスワードを生成します。

5.  Python プロジェクトのルート ディレクトリに`.env`ファイルを作成し、接続パラメータを対応する環境変数に貼り付けます。

    -   `TIDB_HOST` : TiDB クラスターのホスト。
    -   `TIDB_PORT` : TiDB クラスターのポート。
    -   `TIDB_USERNAME` : TiDB クラスターに接続するためのユーザー名。
    -   `TIDB_PASSWORD` : TiDB クラスターに接続するためのパスワード。
    -   `TIDB_DATABASE` : 接続するデータベース名。
    -   `TIDB_CA_PATH` : ルート証明書ファイルへのパス。

    以下は macOS の例です。

    ```dotenv
    TIDB_HOST=gateway01.****.prod.aws.tidbcloud.com
    TIDB_PORT=4000
    TIDB_USERNAME=********.root
    TIDB_PASSWORD=********
    TIDB_DATABASE=test
    TIDB_CA_PATH=/etc/ssl/cert.pem
    ```

### ステップ5.デモを実行する {#step-5-run-the-demo}

```bash
python peewee-quickstart.py
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

from peewee import Model, MySQLDatabase, SQL, TextField
from tidb_vector.peewee import VectorField

dotenv.load_dotenv()

# Using `pymysql` as the driver.
connect_kwargs = {
    'ssl_verify_cert': True,
    'ssl_verify_identity': True,
}

# Using `mysqlclient` as the driver.
# connect_kwargs = {
#     'ssl_mode': 'VERIFY_IDENTITY',
#     'ssl': {
#         # Root certificate default path
#         # https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-clusters/#root-certificate-default-path
#         'ca': os.environ.get('TIDB_CA_PATH', '/path/to/ca.pem'),
#     },
# }

db = MySQLDatabase(
    database=os.environ.get('TIDB_DATABASE', 'test'),
    user=os.environ.get('TIDB_USERNAME', 'root'),
    password=os.environ.get('TIDB_PASSWORD', ''),
    host=os.environ.get('TIDB_HOST', 'localhost'),
    port=int(os.environ.get('TIDB_PORT', '4000')),
    **connect_kwargs,
)
```

#### ベクトル列を定義する {#define-a-vector-column}

3 次元ベクトルを格納する`peewee_demo_documents`という名前の列を持つテーブルを作成します。

```python
class Document(Model):
    class Meta:
        database = db
        table_name = 'peewee_demo_documents'

    content = TextField()
    embedding = VectorField(3)
```

#### インデックスで最適化されたベクトル列を定義する {#define-a-vector-column-optimized-with-index}

3 次元ベクトル列を定義し、 [ベクトル検索インデックス](/tidb-cloud/vector-search-index.md) (HNSW インデックス) で最適化します。

```python
class DocumentWithIndex(Model):
    class Meta:
        database = db
        table_name = 'peewee_demo_documents_with_index'

    content = TextField()
    embedding = VectorField(3, constraints=[SQL("COMMENT 'hnsw(distance=cosine)'")])
```

TiDB はこのインデックスを使用して、コサイン距離関数に基づくベクトル検索クエリを高速化します。

### 埋め込み付きドキュメントを保存する {#store-documents-with-embeddings}

```python
Document.create(content='dog', embedding=[1, 2, 1])
Document.create(content='fish', embedding=[1, 2, 4])
Document.create(content='tree', embedding=[1, 0, 0])
```

### 最も近い文書を検索する {#search-the-nearest-neighbor-documents}

コサイン距離関数に基づいて、クエリ ベクトル`[1, 2, 3]`に意味的に最も近い上位 3 つのドキュメントを検索します。

```python
distance = Document.embedding.cosine_distance([1, 2, 3]).alias('distance')
results = Document.select(Document, distance).order_by(distance).limit(3)
```

### 特定の距離内の文書を検索する {#search-documents-within-a-certain-distance}

クエリベクトル`[1, 2, 3]`からのコサイン距離が 0.2 未満のドキュメントを検索します。

```python
distance_expression = Document.embedding.cosine_distance([1, 2, 3])
distance = distance_expression.alias('distance')
results = Document.select(Document, distance).where(distance_expression < 0.2).order_by(distance).limit(3)
```

## 参照 {#see-also}

-   [ベクトルデータ型](/tidb-cloud/vector-search-data-types.md)
-   [ベクター検索インデックス](/tidb-cloud/vector-search-index.md)
