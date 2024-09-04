---
title: Integrate TiDB Vector Search with Django ORM
summary: TiDB Vector Search を Django ORM と統合して埋め込みを保存し、セマンティック検索を実行する方法を学習します。
---

# TiDB ベクトル検索を Django ORM と統合する {#integrate-tidb-vector-search-with-django-orm}

このチュートリアルでは、 [ジャンゴ](https://www.djangoproject.com/) ORM を使用して TiDB Vector Search と対話し、埋め込みを保存し、ベクトル検索クエリを実行する方法について説明します。

> **注記**
>
> TiDB Vector Search は現在ベータ版であり、 [TiDB サーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスターでのみ使用できます。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、次のものが必要です。

-   [Python 3.8以上](https://www.python.org/downloads/)インストールされました。
-   [ギット](https://git-scm.com/downloads)インストールされました。
-   TiDB サーバーレス クラスター。TiDB Cloud クラスターがない場合は、 [TiDB サーバーレス クラスターの作成](/tidb-cloud/create-tidb-cluster-serverless.md)に従って独自のTiDB Cloudクラスターを作成してください。

## サンプルアプリを実行する {#run-the-sample-app}

以下の手順に従って、TiDB Vector Search を Django ORM と統合する方法を簡単に学習できます。

### ステップ1. リポジトリをクローンする {#step-1-clone-the-repository}

`tidb-vector-python`リポジトリをローカル マシンにクローンします。

```shell
git clone https://github.com/pingcap/tidb-vector-python.git
```

### ステップ2. 仮想環境を作成する {#step-2-create-a-virtual-environment}

プロジェクト用の仮想環境を作成します。

```bash
cd tidb-vector-python/examples/orm-django-quickstart
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
pip install Django django-tidb mysqlclient numpy python-dotenv
```

mysqlclient のインストールで問題が発生した場合は、mysqlclient の公式ドキュメントを参照してください。

#### <code>django-tidb</code>とは何か {#what-is-code-django-tidb-code}

`django-tidb`は、Django ORM を拡張して TiDB 固有の機能 (たとえば、Vector Search) をサポートし、TiDB と Django 間の互換性の問題を解決する、Django 用の TiDB 方言です。

`django-tidb`をインストールするには、Django のバージョンと一致するバージョンを選択します。たとえば、 `django==4.2.*`を使用している場合は`django-tidb==4.2.*`をインストールします。マイナー バージョンは同じである必要はありません。最新のマイナー バージョンを使用することをお勧めします。

詳細については[django-tidb リポジトリ](https://github.com/pingcap/django-tidb)を参照してください。

### ステップ4. 環境変数を設定する {#step-4-configure-the-environment-variables}

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログの構成が動作環境と一致していることを確認します。

    -   **接続タイプは**`Public`に設定されています

    -   **ブランチ**は`main`に設定されています

    -   **接続先は**`General`に設定されています

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

データベース スキーマを移行します。

```bash
python manage.py migrate
```

Django 開発サーバーを実行します:

```bash
python manage.py runserver
```

ブラウザを開いて`http://127.0.0.1:8000`アクセスし、デモ アプリケーションを試してください。使用可能な API パスは次のとおりです。

| APIパス                                   | 説明                    |
| --------------------------------------- | --------------------- |
| `POST: /insert_documents`               | 埋め込みのあるドキュメントを挿入します。  |
| `GET: /get_nearest_neighbors_documents` | 3 つの最も近いドキュメントを取得します。 |
| `GET: /get_documents_within_distance`   | 一定の距離内の文書を取得します。      |

## サンプルコードスニペット {#sample-code-snippets}

次のサンプル コード スニペットを参照して、独自のアプリケーション開発を完了することができます。

### TiDBクラスタに接続する {#connect-to-the-tidb-cluster}

ファイル`sample_project/settings.py`に次の設定を追加します。

```python
dotenv.load_dotenv()

DATABASES = {
    "default": {
        # https://github.com/pingcap/django-tidb
        "ENGINE": "django_tidb",
        "HOST": os.environ.get("TIDB_HOST", "127.0.0.1"),
        "PORT": int(os.environ.get("TIDB_PORT", 4000)),
        "USER": os.environ.get("TIDB_USERNAME", "root"),
        "PASSWORD": os.environ.get("TIDB_PASSWORD", ""),
        "NAME": os.environ.get("TIDB_DATABASE", "test"),
        "OPTIONS": {
            "charset": "utf8mb4",
        },
    }
}

TIDB_CA_PATH = os.environ.get("TIDB_CA_PATH", "")
if TIDB_CA_PATH:
    DATABASES["default"]["OPTIONS"]["ssl_mode"] = "VERIFY_IDENTITY"
    DATABASES["default"]["OPTIONS"]["ssl"] = {
        "ca": TIDB_CA_PATH,
    }
```

プロジェクトのルート ディレクトリに`.env`ファイルを作成し、環境変数`TIDB_HOST` `TIDB_CA_PATH` `TIDB_DATABASE` `TIDB_PORT` `TIDB_USERNAME`の実際の値で設定`TIDB_PASSWORD`ます。

### ベクターテーブルを作成する {#create-vector-tables}

#### ベクトル列を定義する {#define-a-vector-column}

`tidb-django` 、ベクトル埋め込みをテーブルに格納するための`VectorField`提供します。

3 次元ベクトルを格納する`embedding`という名前の列を持つテーブルを作成します。

```python
class Document(models.Model):
   content = models.TextField()
   embedding = VectorField(dimensions=3)
```

#### インデックスで最適化されたベクトル列を定義する {#define-a-vector-column-optimized-with-index}

3 次元ベクトル列を定義し、 [ベクトル検索インデックス](/tidb-cloud/vector-search-index.md) (HNSW インデックス) で最適化します。

```python
class DocumentWithIndex(models.Model):
   content = models.TextField()
   # Note:
   #   - Using comment to add hnsw index is a temporary solution. In the future it will use `CREATE INDEX` syntax.
   #   - Currently the HNSW index cannot be changed after the table has been created.
   #   - Only Django >= 4.2 supports `db_comment`.
   embedding = VectorField(dimensions=3, db_comment="hnsw(distance=cosine)")
```

TiDB はこのインデックスを使用して、コサイン距離関数に基づくベクトル検索クエリを高速化します。

### 埋め込み付きドキュメントを保存する {#store-documents-with-embeddings}

```python
Document.objects.create(content="dog", embedding=[1, 2, 1])
Document.objects.create(content="fish", embedding=[1, 2, 4])
Document.objects.create(content="tree", embedding=[1, 0, 0])
```

### 最も近い文書を検索する {#search-the-nearest-neighbor-documents}

TiDB Vector は以下の距離関数をサポートします:

-   `L1Distance`
-   `L2Distance`
-   `CosineDistance`
-   `NegativeInnerProduct`

コサイン距離関数に基づいて、クエリ ベクトル`[1, 2, 3]`に意味的に最も近い上位 3 つのドキュメントを検索します。

```python
results = Document.objects.annotate(
   distance=CosineDistance('embedding', [1, 2, 3])
).order_by('distance')[:3]
```

### 特定の距離内の文書を検索する {#search-documents-within-a-certain-distance}

クエリベクトル`[1, 2, 3]`からのコサイン距離が 0.2 未満のドキュメントを検索します。

```python
results = Document.objects.annotate(
   distance=CosineDistance('embedding', [1, 2, 3])
).filter(distance__lt=0.2).order_by('distance')[:3]
```

## 参照 {#see-also}

-   [ベクトルデータ型](/tidb-cloud/vector-search-data-types.md)
-   [ベクター検索インデックス](/tidb-cloud/vector-search-index.md)
