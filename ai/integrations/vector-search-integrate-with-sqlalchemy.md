---
title: Integrate TiDB Vector Search with SQLAlchemy
summary: TiDB Vector SearchをSQLAlchemyと統合して、埋め込みデータを保存し、セマンティック検索を実行する方法を学びましょう。
aliases: ['/ja/tidb/stable/vector-search-integrate-with-sqlalchemy/','/ja/tidb/dev/vector-search-integrate-with-sqlalchemy/','/ja/tidbcloud/vector-search-integrate-with-sqlalchemy/']
---

# TiDBベクトル検索をSQLAlchemyと統合する {#integrate-tidb-vector-search-with-sqlalchemy}

このチュートリアルでは、 [SQLAlchemy](https://www.sqlalchemy.org/)を使用して[TiDB ベクトル検索](/ai/concepts/vector-search-overview.md)と対話し、埋め込みを保存し、ベクトル検索クエリを実行する方法を説明します。

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

以下の手順に従うことで、TiDB Vector SearchをSQLAlchemyと統合する方法をすぐに習得できます。

### ステップ1. リポジトリをクローンする {#step-1-clone-the-repository}

`tidb-vector-python`リポジトリをローカルマシンにクローンします。

```shell
git clone https://github.com/pingcap/tidb-vector-python.git
```

### ステップ2. 仮想環境を作成する {#step-2-create-a-virtual-environment}

プロジェクト用の仮想環境を作成する：

```bash
cd tidb-vector-python/examples/orm-sqlalchemy-quickstart
python3 -m venv .venv
source .venv/bin/activate
```

### ステップ3. 必要な依存関係をインストールします {#step-3-install-the-required-dependencies}

デモプロジェクトに必要な依存関係をインストールします。

```bash
pip install -r requirements.txt
```

または、プロジェクトに以下のパッケージをインストールすることもできます。

```bash
pip install pymysql python-dotenv sqlalchemy tidb-vector
```

### ステップ4．環境変数を設定する {#step-4-configure-the-environment-variables}

選択したTiDBのデプロイオプションに応じて、環境変数を設定してください。

<SimpleTab>
<div label="TiDB Cloud Starter or Essential">

TiDB Cloud StarterまたはEssentialインスタンスの場合、接続文字列を取得し、環境変数を設定するには、以下の手順に従ってください。

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud StarterまたはEssentialインスタンスの名前をクリックして、概要ページに移動します。

2.  右上隅の**「接続」**をクリックしてください。接続ダイアログが表示されます。

3.  接続ダイアログの設定がご使用の環境と一致していることを確認してください。

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

### ステップ5．デモを実行する {#step-5-run-the-demo}

```bash
python sqlalchemy-quickstart.py
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

from sqlalchemy import Column, Integer, create_engine, Text
from sqlalchemy.orm import declarative_base, Session
from tidb_vector.sqlalchemy import VectorType

dotenv.load_dotenv()

tidb_connection_string = os.environ['TIDB_DATABASE_URL']
engine = create_engine(tidb_connection_string)
```

#### ベクトル列を定義する {#define-a-vector-column}

`embedding`という名前の列を持つテーブルを作成し、その列に3次元ベクトルを格納します。

```python
Base = declarative_base()

class Document(Base):
    __tablename__ = 'sqlalchemy_demo_documents'
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    embedding = Column(VectorType(3))
```

### 埋め込みを含むドキュメントを保存する {#store-documents-with-embeddings}

```python
with Session(engine) as session:
   session.add(Document(content="dog", embedding=[1, 2, 1]))
   session.add(Document(content="fish", embedding=[1, 2, 4]))
   session.add(Document(content="tree", embedding=[1, 0, 0]))
   session.commit()
```

### 近隣住民の文書を検索 {#search-the-nearest-neighbor-documents}

コサイン距離関数に基づいて、クエリベクトル`[1, 2, 3]`に意味的に最も近い上位 3 つのドキュメントを検索します。

```python
with Session(engine) as session:
   distance = Document.embedding.cosine_distance([1, 2, 3]).label('distance')
   results = session.query(
      Document, distance
   ).order_by(distance).limit(3).all()
```

### 一定距離内の文書を検索 {#search-documents-within-a-certain-distance}

クエリベクトル`[1, 2, 3]`からのコサイン距離が 0.2 未満の文書を検索します。

```python
with Session(engine) as session:
    distance = Document.embedding.cosine_distance([1, 2, 3]).label('distance')
    results = session.query(
        Document, distance
    ).filter(distance < 0.2).order_by(distance).limit(3).all()
```

## 関連項目 {#see-also}

-   [ベクトルデータ型](/ai/reference/vector-search-data-types.md)
-   [ベクトル検索インデックス](/ai/reference/vector-search-index.md)
