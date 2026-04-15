---
title: Integrate TiDB Vector Search with peewee
summary: TiDB Vector Searchをpeeweeと統合して、埋め込みデータを保存し、セマンティック検索を実行する方法を学びましょう。
aliases: ['/ja/tidb/stable/vector-search-integrate-with-peewee/','/ja/tidb/dev/vector-search-integrate-with-peewee/','/ja/tidbcloud/vector-search-integrate-with-peewee/']
---

# TiDBベクトル検索をpeeweeと統合する {#integrate-tidb-vector-search-with-peewee}

このチュートリアルでは[ピーウィー](https://docs.peewee-orm.com/)を使用して[TiDB ベクトル検索](/ai/concepts/vector-search-overview.md)と対話し、エンベディングを保存し、ベクトル検索クエリを実行する方法を説明します。

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

以下の手順に従うことで、TiDB Vector Searchをpeeweeに統合する方法をすぐに習得できます。

### ステップ1. リポジトリをクローンする {#step-1-clone-the-repository}

[`tidb-vector-python`](https://github.com/pingcap/tidb-vector-python)リポジトリをローカルマシンにクローンしてください。

```shell
git clone https://github.com/pingcap/tidb-vector-python.git
```

### ステップ2. 仮想環境を作成する {#step-2-create-a-virtual-environment}

プロジェクト用の仮想環境を作成する：

```bash
cd tidb-vector-python/examples/orm-peewee-quickstart
python3 -m venv .venv
source .venv/bin/activate
```

### ステップ3. 必要な依存関係をインストールします {#step-3-install-required-dependencies}

デモプロジェクトに必要な依存関係をインストールします。

```bash
pip install -r requirements.txt
```

または、プロジェクトに以下のパッケージをインストールすることもできます。

```bash
pip install peewee pymysql python-dotenv tidb-vector
```

### ステップ4．環境変数を設定する {#step-4-configure-the-environment-variables}

選択したTiDBのデプロイオプションに応じて、環境変数を設定してください。

<SimpleTab>
<div label="TiDB Cloud Starter or Essential">

TiDB Cloud StarterまたはEssentialインスタンスの場合、接続文字列を取得し、環境変数を設定するには、以下の手順に従ってください。

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud StarterまたはEssentialインスタンスの名前をクリックして、概要ページに移動します。

2.  右上隅の**「接続」**をクリックしてください。接続ダイアログが表示されます。

3.  接続ダイアログの設定がご使用のオペレーティング環境と一致していることを確認してください。

    -   **接続タイプ**は`Public`に設定されています。

    -   **ブランチ**は`main`に設定されています。

    -   **「接続」は**`General`に設定されています。

    -   お使いの環境に合った**オペレーティングシステム**を選択してください。

    > **ヒント：**
    >
    > プログラムがWindows Subsystem for Linux（WSL）上で実行されている場合は、対応するLinuxディストリビューションに切り替えてください。

4.  接続ダイアログから接続パラメータをコピーしてください。

    > **ヒント：**
    >
    > まだパスワードを設定していない場合は、 **「パスワードを生成」**をクリックしてランダムなパスワードを生成してください。

5.  Python プロジェクトのルートディレクトリに`.env`ファイルを作成し、接続パラメータを対応する環境変数に貼り付けます。

    -   `TIDB_HOST` : TiDB Cloud StarterまたはEssentialインスタンスのホスト。
    -   `TIDB_PORT` : TiDB Cloud StarterまたはEssentialインスタンスのポート。
    -   `TIDB_USERNAME` : TiDBに接続するためのユーザー名。
    -   `TIDB_PASSWORD` : TiDBに接続するためのパスワード。
    -   `TIDB_DATABASE` : 接続するデータベース名。
    -   `TIDB_CA_PATH` : ルート証明書ファイルへのパス。

    以下はmacOSの例です。

    ```dotenv
    TIDB_HOST=gateway01.****.prod.aws.tidbcloud.com
    TIDB_PORT=4000
    TIDB_USERNAME=********.root
    TIDB_PASSWORD=********
    TIDB_DATABASE=test
    TIDB_CA_PATH=/etc/ssl/cert.pem
    ```

</div>
<div label="TiDB Self-Managed" value="tidb">

TiDBセルフマネージドクラスタの場合、Pythonプロジェクトのルートディレクトリに`.env`ファイルを作成します。次の内容を`.env`ファイルにコピーし、TiDBクラスタの接続パラメータに応じて環境変数の値を変更します。

```dotenv
TIDB_HOST=127.0.0.1
TIDB_PORT=4000
TIDB_USERNAME=root
TIDB_PASSWORD=
TIDB_DATABASE=test
```

TiDBをローカルマシンで実行している場合、 `TIDB_HOST`はデフォルトで`127.0.0.1`になります。初期の`TIDB_PASSWORD`は空なので、クラスターを初めて起動する場合は、このフィールドを省略できます。

各パラメータの説明は以下のとおりです。

-   `TIDB_HOST` : TiDB セルフマネージド クラスタのホスト。
-   `TIDB_PORT` : TiDB セルフマネージド クラスタのポート。
-   `TIDB_USERNAME` : TiDB セルフマネージド クラスタに接続するためのユーザー名。
-   `TIDB_PASSWORD` : TiDB セルフマネージド クラスタに接続するためのパスワード。
-   `TIDB_DATABASE` : 接続するデータベースの名前。

</div>

</SimpleTab>

### ステップ5．デモを実行する {#step-5-run-the-demo}

```bash
python peewee-quickstart.py
```

出力例：

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

アプリケーション開発にあたっては、以下のサンプルコードスニペットを参考にしてください。

### ベクターテーブルを作成する {#create-vector-tables}

#### TiDBに接続する {#connect-to-tidb}

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

`peewee_demo_documents`という名前の列を持つテーブルを作成し、その列に3次元ベクトルを格納します。

```python
class Document(Model):
    class Meta:
        database = db
        table_name = 'peewee_demo_documents'

    content = TextField()
    embedding = VectorField(3)
```

### 埋め込みを含むドキュメントを保存する {#store-documents-with-embeddings}

```python
Document.create(content='dog', embedding=[1, 2, 1])
Document.create(content='fish', embedding=[1, 2, 4])
Document.create(content='tree', embedding=[1, 0, 0])
```

### 近隣住民の文書を検索 {#search-the-nearest-neighbor-documents}

コサイン距離関数に基づいて、クエリベクトル`[1, 2, 3]`に意味的に最も近い上位 3 つのドキュメントを検索します。

```python
distance = Document.embedding.cosine_distance([1, 2, 3]).alias('distance')
results = Document.select(Document, distance).order_by(distance).limit(3)
```

### 一定距離内の文書を検索 {#search-documents-within-a-certain-distance}

クエリベクトル`[1, 2, 3]`からのコサイン距離が 0.2 未満の文書を検索します。

```python
distance_expression = Document.embedding.cosine_distance([1, 2, 3])
distance = distance_expression.alias('distance')
results = Document.select(Document, distance).where(distance_expression < 0.2).order_by(distance).limit(3)
```

## 関連項目 {#see-also}

-   [ベクトルデータ型](/ai/reference/vector-search-data-types.md)
-   [ベクトル検索インデックス](/ai/reference/vector-search-index.md)
