---
title: Integrate TiDB Vector Search with Django ORM
summary: TiDB Vector SearchをDjango ORMと統合して、埋め込みデータを保存し、セマンティック検索を実行する方法を学びましょう。
aliases: ['/ja/tidb/stable/vector-search-integrate-with-django-orm/','/ja/tidb/dev/vector-search-integrate-with-django-orm/','/ja/tidbcloud/vector-search-integrate-with-django-orm/']
---

# TiDBベクトル検索をDjango ORMと統合する {#integrate-tidb-vector-search-with-django-orm}

このチュートリアルでは[ジャンゴ](https://www.djangoproject.com/)ORM を使用して[TiDB ベクトル検索](/ai/concepts/vector-search-overview.md)と対話し、エンベディングを保存し、ベクトル検索クエリを実行する方法を説明します。

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

以下の手順に従うことで、TiDB Vector SearchをDjango ORMに統合する方法をすぐに習得できます。

### ステップ1. リポジトリをクローンする {#step-1-clone-the-repository}

`tidb-vector-python`リポジトリをローカルマシンにクローンします。

```shell
git clone https://github.com/pingcap/tidb-vector-python.git
```

### ステップ2. 仮想環境を作成する {#step-2-create-a-virtual-environment}

プロジェクト用の仮想環境を作成する：

```bash
cd tidb-vector-python/examples/orm-django-quickstart
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
pip install Django django-tidb mysqlclient numpy python-dotenv
```

mysqlclientのインストールで問題が発生した場合は、mysqlclientの公式ドキュメントを参照してください。

#### <code>django-tidb</code>とは何ですか？ {#what-is-code-django-tidb-code}

`django-tidb`は Django 用の TiDB 方言であり、Django ORM を拡張して TiDB 固有の機能 (例えば、ベクトル検索) をサポートし、TiDB と Django 間の互換性の問題を解決します。

`django-tidb`をインストールするには、お使いの Django のバージョンに合ったバージョンを選択してください。例えば、 `django==4.2.*`を使用している場合は、 `django-tidb==4.2.*`をインストールしてください。マイナーバージョンは同じである必要はありませんが、最新のマイナーバージョンを使用することをお勧めします。

詳細については、 [django-tidbリポジトリ](https://github.com/pingcap/django-tidb)を参照してください。

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

    -   **Connect With は**`General`に設定されています。

    -   お使いの環境に合った**オペレーティングシステム**を選択してください。

    > **ヒント：**
    >
    > プログラムがWindows Subsystem for Linux（WSL）上で実行されている場合は、対応するLinuxディストリビューションに切り替えてください。

4.  接続ダイアログから接続パラメータをコピーしてください。

    > **ヒント：**
    >
    > まだパスワードを設定していない場合は、 **「パスワードを生成」**をクリックしてランダムなパスワードを生成してください。

5.  Python プロジェクトのルートディレクトリに`.env`ファイルを作成し、接続パラメータを対応する環境変数に貼り付けます。

    -   `TIDB_HOST` : TiDBクラスタのホスト。
    -   `TIDB_PORT` : TiDB クラスタのポート。
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

データベーススキーマを移行する：

```bash
python manage.py migrate
```

Django開発サーバーを実行します。

```bash
python manage.py runserver
```

ブラウザを開いて`http://127.0.0.1:8000`にアクセスし、デモアプリケーションをお試しください。利用可能なAPIパスは以下のとおりです。

| APIパス                                   | 説明                        |
| --------------------------------------- | ------------------------- |
| `POST: /insert_documents`               | 埋め込みを含むドキュメントを挿入します。      |
| `GET: /get_nearest_neighbors_documents` | 最近隣の3軒の物件に関する書類を入手してください。 |
| `GET: /get_documents_within_distance`   | 一定距離内にある書類を入手する。          |

## サンプルコードスニペット {#sample-code-snippets}

以下のサンプルコードスニペットを参考に、独自のアプリケーション開発を完成させてください。

### TiDBに接続する {#connect-to-tidb}

ファイル`sample_project/settings.py`に、以下の設定を追加します。

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

プロジェクトのルート ディレクトリに`.env`ファイルを作成し、環境変数`TIDB_HOST` 、 `TIDB_PORT` 、 `TIDB_USERNAME` 、 `TIDB_PASSWORD` 、 `TIDB_DATABASE` 、および`TIDB_CA_PATH` TiDB の実際の値で設定できます。

### ベクターテーブルを作成する {#create-vector-tables}

#### ベクトル列を定義する {#define-a-vector-column}

`tidb-django`は、ベクトル埋め込みをテーブルに格納するための`VectorField`を提供します。

`embedding`という名前の列を持つテーブルを作成し、その列に3次元ベクトルを格納します。

```python
class Document(models.Model):
   content = models.TextField()
   embedding = VectorField(dimensions=3)
```

### 埋め込みを含むドキュメントを保存する {#store-documents-with-embeddings}

```python
Document.objects.create(content="dog", embedding=[1, 2, 1])
Document.objects.create(content="fish", embedding=[1, 2, 4])
Document.objects.create(content="tree", embedding=[1, 0, 0])
```

### 近隣住民の文書を検索 {#search-the-nearest-neighbor-documents}

TiDB Vectorは以下の距離関数をサポートしています。

-   `L1Distance`
-   `L2Distance`
-   `CosineDistance`
-   `NegativeInnerProduct`

コサイン距離関数に基づいて、クエリベクトル`[1, 2, 3]`に意味的に最も近い上位 3 つのドキュメントを検索します。

```python
results = Document.objects.annotate(
   distance=CosineDistance('embedding', [1, 2, 3])
).order_by('distance')[:3]
```

### 一定距離内の文書を検索 {#search-documents-within-a-certain-distance}

クエリベクトル`[1, 2, 3]`からのコサイン距離が 0.2 未満の文書を検索します。

```python
results = Document.objects.annotate(
   distance=CosineDistance('embedding', [1, 2, 3])
).filter(distance__lt=0.2).order_by('distance')[:3]
```

## 関連項目 {#see-also}

-   [ベクトルデータ型](/ai/reference/vector-search-data-types.md)
-   [ベクトル検索インデックス](/ai/reference/vector-search-index.md)
