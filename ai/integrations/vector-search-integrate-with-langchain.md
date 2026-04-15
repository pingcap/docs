---
title: Integrate Vector Search with LangChain
summary: TiDB Vector SearchをLangChainと統合する方法を学びましょう。
aliases: ['/ja/tidb/stable/vector-search-integrate-with-langchain/','/ja/tidb/dev/vector-search-integrate-with-langchain/','/ja/tidbcloud/vector-search-integrate-with-langchain/']
---

# ベクトル検索をLangChainと統合する {#integrate-vector-search-with-langchain}

このチュートリアルでは[TiDB ベクトル検索](/ai/concepts/vector-search-overview.md)[ラングチェーン](https://python.langchain.com/)する方法を説明します。

> **注記：**
>
> -   ベクター検索機能はベータ版です。予告なく変更される場合があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)を報告してください。
> -   ベクトル検索機能は、 [TiDBセルフマネージド](/overview.md)[TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter) 、 [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) 、および[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)で利用できます。TiDB Self-ManagedおよびTiDB Cloud Dedicatedの場合、TiDBのバージョンはv8.4.0以降である必要があります（v8.5.0以降を推奨）。

> **ヒント**
>
> 完全な[サンプルコード](https://github.com/langchain-ai/langchain/blob/master/docs/docs/integrations/vectorstores/tidb_vector.ipynb)Jupyter Notebook で表示することも、 [コラボレーション](https://colab.research.google.com/github/langchain-ai/langchain/blob/master/docs/docs/integrations/vectorstores/tidb_vector.ipynb)オンライン環境で直接実行することもできます。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、以下が必要です。

-   [Python 3.8以降](https://www.python.org/downloads/)インストールされています。
-   [ジュピターノートブック](https://jupyter.org/install)がインストールされました。
-   [Git](https://git-scm.com/downloads)がインストールされました。
-   TiDBクラスタ。

**TiDBクラスタをお持ちでない場合は、以下の手順で作成できます。**

-   (推奨) [TiDB Cloud Starterインスタンスを作成する](/develop/dev-guide-build-cluster-in-cloud.md)。
-   [ローカルテスト用のTiDBセルフマネージドクラスタをデプロイ。](/quick-start-with-tidb.md#deploy-a-local-test-cluster)または[本番本番のTiDBセルフマネージドクラスタをデプロイ。](/production-deployment-using-tiup.md)

## さあ始めましょう {#get-started}

このセクションでは、TiDB Vector SearchをLangChainと統合して意味検索を実行するための手順を段階的に説明します。

### ステップ1. 新しいJupyter Notebookファイルを作成する {#step-1-create-a-new-jupyter-notebook-file}

任意のディレクトリに、 `integrate_with_langchain.ipynb`という名前の新しい Jupyter Notebook ファイルを作成します。

```shell
touch integrate_with_langchain.ipynb
```

### ステップ2. 必要な依存関係をインストールします {#step-2-install-required-dependencies}

プロジェクトディレクトリで、以下のコマンドを実行して必要なパッケージをインストールしてください。

```shell
!pip install langchain langchain-community
!pip install langchain-openai
!pip install pymysql
!pip install tidb-vector
```

Jupyter Notebookで`integrate_with_langchain.ipynb`ファイルを開き、必要なパッケージをインポートするために以下のコードを追加します。

```python
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import TiDBVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
```

### ステップ3．環境をセットアップする {#step-3-set-up-your-environment}

選択したTiDBのデプロイオプションに応じて、環境変数を設定してください。

<SimpleTab>
<div label="TiDB Cloud Starter or Essential">

TiDB Cloud StarterまたはEssentialインスタンスの場合、接続文字列を取得し、環境変数を設定するには、以下の手順に従ってください。

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud StarterまたはEssentialインスタンスの名前をクリックして、概要ページに移動します。

2.  右上隅の**「接続」**をクリックしてください。接続ダイアログが表示されます。

3.  接続ダイアログの設定がご使用のオペレーティング環境と一致していることを確認してください。

    -   **接続タイプ**は`Public`に設定されています。
    -   **ブランチ**は`main`に設定されています。
    -   **「接続」は**`SQLAlchemy`に設定されています。
    -   お使いの環境に合った**オペレーティングシステム**を選択してください。

4.  **PyMySQL**タブをクリックして、接続文字列をコピーしてください。

    > **ヒント：**
    >
    > まだパスワードを設定していない場合は、 **「パスワードを生成」**をクリックしてランダムなパスワードを生成してください。

5.  環境変数を設定します。

    このドキュメントでは、埋め込みモデルプロバイダーとして[OpenAI](https://platform.openai.com/docs/introduction)を使用します。この手順では、前の手順で取得した接続文字列と[OpenAI APIキー](https://platform.openai.com/docs/quickstart/step-2-set-up-your-api-key)指定する必要があります。

    環境変数を設定するには、次のコードを実行してください。接続文字列とOpenAI APIキーの入力を求められます。

    ```python
    # Use getpass to securely prompt for environment variables in your terminal.
    import getpass
    import os

    # Copy your connection string from the TiDB Cloud console.
    # Connection string format: "mysql+pymysql://<USER>:<PASSWORD>@<HOST>:4000/<DB>?ssl_ca=/etc/ssl/cert.pem&ssl_verify_cert=true&ssl_verify_identity=true"
    tidb_connection_string = getpass.getpass("TiDB Connection String:")
    os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")
    ```

</div>
<div label="TiDB Self-Managed" value="tidb">

このドキュメントでは、埋め込みモデルプロバイダーとして[OpenAI](https://platform.openai.com/docs/introduction)を使用します。この手順では、前の手順で取得した接続文字列と[OpenAI APIキー](https://platform.openai.com/docs/quickstart/step-2-set-up-your-api-key)指定する必要があります。

環境変数を設定するには、次のコードを実行してください。接続文字列とOpenAI APIキーの入力を求められます。

```python
# Use getpass to securely prompt for environment variables in your terminal.
import getpass
import os

# Connection string format: "mysql+pymysql://<USER>:<PASSWORD>@<HOST>:4000/<DB>?ssl_ca=/etc/ssl/cert.pem&ssl_verify_cert=true&ssl_verify_identity=true"
tidb_connection_string = getpass.getpass("TiDB Connection String:")
os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")
```

macOSを例にとると、クラスタ接続文字列は次のようになります。

```dotenv
TIDB_DATABASE_URL="mysql+pymysql://<USERNAME>:<PASSWORD>@<HOST>:<PORT>/<DATABASE_NAME>"
# For example: TIDB_DATABASE_URL="mysql+pymysql://root@127.0.0.1:4000/test"
```

TiDBクラスタに合わせて接続パラメータの値を変更する必要があります。ローカルマシンでTiDBを実行している場合、 `<HOST>`はデフォルトで`127.0.0.1`になります。初期値の`<PASSWORD>`は空なので、クラスタを初めて起動する場合はこのフィールドを省略できます。

各パラメータの説明は以下のとおりです。

-   `<USERNAME>` : TiDBに接続するためのユーザー名。
-   `<PASSWORD>` : TiDBに接続するためのパスワード。
-   `<HOST>` : TiDBクラスタのホスト。
-   `<PORT>` : TiDB クラスタのポート。
-   `<DATABASE>` : 接続するデータベースの名前。

</div>

</SimpleTab>

### ステップ4. サンプルドキュメントを読み込む {#step-4-load-the-sample-document}

#### ステップ4.1 サンプル文書をダウンロードする {#step-4-1-download-the-sample-document}

プロジェクトディレクトリ内に、 `data/how_to/`という名前のディレクトリを作成し、 [langchain-ai/langchain](https://github.com/langchain-ai/langchain) GitHubリポジトリからサンプルドキュメント[`state_of_the_union.txt`](https://github.com/langchain-ai/langchain/blob/master/docs/docs/how_to/state_of_the_union.txt)をダウンロードしてください。

```shell
!mkdir -p 'data/how_to/'
!wget 'https://raw.githubusercontent.com/langchain-ai/langchain/master/docs/docs/how_to/state_of_the_union.txt' -O 'data/how_to/state_of_the_union.txt'
```

#### ステップ4.2 ドキュメントを読み込んで分割する {#step-4-2-load-and-split-the-document}

`data/how_to/state_of_the_union.txt`からサンプル文書を読み込み、 `CharacterTextSplitter`を使用してそれぞれ約 1,000 文字のチャンクに分割します。

```python
loader = TextLoader("data/how_to/state_of_the_union.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)
```

### ステップ5．ドキュメントベクターを埋め込んで保存する {#step-5-embed-and-store-document-vectors}

TiDB ベクター ストアは、ベクター間の類似性を測定するために、コサイン距離 ( `cosine` ) とユークリッド距離 ( `l2` ) の両方をサポートしています。デフォルトの戦略はコサイン距離です。

以下のコードは、ベクトル検索に最適化されたTiDBに`embedded_documents`という名前のテーブルを作成します。

```python
embeddings = OpenAIEmbeddings()
vector_store = TiDBVectorStore.from_documents(
    documents=docs,
    embedding=embeddings,
    table_name="embedded_documents",
    connection_string=tidb_connection_string,
    distance_strategy="cosine",  # default, another option is "l2"
)
```

正常に実行されると、TiDB データベース内の`embedded_documents`テーブルを直接表示およびアクセスできるようになります。

### ステップ6. ベクトル検索を実行する {#step-6-perform-a-vector-search}

この手順では、ドキュメント`state_of_the_union.txt`から「大統領はケタンジ・ブラウン・ジャクソンについて何と言ったか」をクエリする方法を示します。

```python
query = "What did the president say about Ketanji Brown Jackson"
```

#### オプション1： <code>similarity_search_with_score()</code>を使用する {#option-1-use-code-similarity-search-with-score-code}

`similarity_search_with_score()`メソッドは、文書とクエリ間のベクトル空間距離を計算します。この距離は類似度スコアとして機能し、選択された`distance_strategy`によって決定されます。このメソッドは、スコアが最も低い上位`k`文書を返します。スコアが低いほど、文書とクエリ間の類似度が高いことを示します。

```python
docs_with_score = vector_store.similarity_search_with_score(query, k=3)
for doc, score in docs_with_score:
   print("-" * 80)
   print("Score: ", score)
   print(doc.page_content)
   print("-" * 80)
```

<details><summary><b>期待される出力</b></summary>

```plain
--------------------------------------------------------------------------------
Score:  0.18472413652518527
Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections.

Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service.

One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court.

And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
Score:  0.21757513022785557
A former top litigator in private practice. A former federal public defender. And from a family of public school educators and police officers. A consensus builder. Since she’s been nominated, she’s received a broad range of support—from the Fraternal Order of Police to former judges appointed by Democrats and Republicans.

And if we are to advance liberty and justice, we need to secure the Border and fix the immigration system.

We can do both. At our border, we’ve installed new technology like cutting-edge scanners to better detect drug smuggling.

We’ve set up joint patrols with Mexico and Guatemala to catch more human traffickers.

We’re putting in place dedicated immigration judges so families fleeing persecution and violence can have their cases heard faster.

We’re securing commitments and supporting partners in South and Central America to host more refugees and secure their own borders.
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
Score:  0.22676987253721725
And for our LGBTQ+ Americans, let’s finally get the bipartisan Equality Act to my desk. The onslaught of state laws targeting transgender Americans and their families is wrong.

As I said last year, especially to our younger transgender Americans, I will always have your back as your President, so you can be yourself and reach your God-given potential.

While it often appears that we never agree, that isn’t true. I signed 80 bipartisan bills into law last year. From preventing government shutdowns to protecting Asian-Americans from still-too-common hate crimes to reforming military justice.

And soon, we’ll strengthen the Violence Against Women Act that I first wrote three decades ago. It is important for us to show the nation that we can come together and do big things.

So tonight I’m offering a Unity Agenda for the Nation. Four big things we can do together.

First, beat the opioid epidemic.
--------------------------------------------------------------------------------
```

</details>

#### オプション2： <code>similarity_search_with_relevance_scores()</code>を使用する {#option-2-use-code-similarity-search-with-relevance-scores-code}

`similarity_search_with_relevance_scores()`メソッドは、関連性スコアが最も高い上位`k`ドキュメントを返します。スコアが高いほど、ドキュメントとクエリの類似性が高いことを示します。

```python
docs_with_relevance_score = vector_store.similarity_search_with_relevance_scores(query, k=2)
for doc, score in docs_with_relevance_score:
    print("-" * 80)
    print("Score: ", score)
    print(doc.page_content)
    print("-" * 80)
```

<details><summary><b>期待される出力</b></summary>

```plain
--------------------------------------------------------------------------------
Score:  0.8152758634748147
Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections.

Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service.

One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court.

And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
Score:  0.7824248697721444
A former top litigator in private practice. A former federal public defender. And from a family of public school educators and police officers. A consensus builder. Since she’s been nominated, she’s received a broad range of support—from the Fraternal Order of Police to former judges appointed by Democrats and Republicans.

And if we are to advance liberty and justice, we need to secure the Border and fix the immigration system.

We can do both. At our border, we’ve installed new technology like cutting-edge scanners to better detect drug smuggling.

We’ve set up joint patrols with Mexico and Guatemala to catch more human traffickers.

We’re putting in place dedicated immigration judges so families fleeing persecution and violence can have their cases heard faster.

We’re securing commitments and supporting partners in South and Central America to host more refugees and secure their own borders.
--------------------------------------------------------------------------------
```

</details>

### 回収犬として使用する {#use-as-a-retriever}

LangChainでは、 [レトリバー](https://python.langchain.com/v0.2/docs/concepts/#retrievers)は非構造化クエリのドキュメントを取得するインターフェースであり、ベクターストアよりも多くの機能を提供します。以下のコードは、TiDBベクターストアをレトリバーとして使用する方法を示しています。

```python
retriever = vector_store.as_retriever(
   search_type="similarity_score_threshold",
   search_kwargs={"k": 3, "score_threshold": 0.8},
)
docs_retrieved = retriever.invoke(query)
for doc in docs_retrieved:
   print("-" * 80)
   print(doc.page_content)
   print("-" * 80)
```

期待される出力は以下のとおりです。

    --------------------------------------------------------------------------------
    Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections.

    Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service.

    One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court.

    And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.
    --------------------------------------------------------------------------------

### ベクターストアを削除する {#remove-the-vector-store}

既存のTiDBベクターストアを削除するには、 `drop_vectorstore()`メソッドを使用します。

```python
vector_store.drop_vectorstore()
```

## メタデータフィルターを使用して検索する {#search-with-metadata-filters}

検索結果を絞り込むには、メタデータフィルターを使用して、適用したフィルターに一致する特定の近隣検索結果を取得できます。

### サポートされているメタデータタイプ {#supported-metadata-types}

TiDBベクターストア内の各ドキュメントには、JSONオブジェクト内のキーと値のペアとして構造化されたメタデータを関連付けることができます。キーは常に文字列であり、値は以下のいずれかの型になります。

-   弦
-   数値：整数または浮動小数点
-   ブール値: `true`または`false`

例えば、以下は有効なメタデータペイロードの例です。

```json
{
  "page": 12,
  "book_title": "Siddhartha"
}
```

### メタデータフィルタ構文 {#metadata-filter-syntax}

利用可能なフィルターは以下のとおりです。

-   `$or` : 指定された条件のいずれかに一致するベクトルを選択します。
-   `$and` : 指定されたすべての条件に一致するベクトルを選択します。
-   `$eq` : 指定された値と等しい。
-   `$ne` : 指定された値と等しくありません。
-   `$gt` : 指定された値より大きい。
-   `$gte` : 指定された値以上。
-   `$lt` : 指定された値より小さい。
-   `$lte` : 指定された値以下。
-   `$in` : 指定された値の配列内。
-   `$nin` : 指定された値の配列に含まれていません。

文書のメタデータが以下のようになっている場合：

```json
{
  "page": 12,
  "book_title": "Siddhartha"
}
```

このドキュメントに一致するメタデータフィルタは以下のとおりです。

```json
{ "page": 12 }
```

```json
{ "page": { "$eq": 12 } }
```

```json
{
  "page": {
    "$in": [11, 12, 13]
  }
}
```

```json
{ "page": { "$nin": [13] } }
```

```json
{ "page": { "$lt": 11 } }
```

```json
{
  "$or": [{ "page": 11 }, { "page": 12 }],
  "$and": [{ "page": 12 }, { "page": 13 }]
}
```

メタデータフィルタでは、TiDB は各キーと値のペアを個別のフィルタ句として扱い、これらの句を`AND`論理演算子を使用して結合します。

### 例 {#example}

次の例では、2 つのドキュメントを`TiDBVectorStore`に追加し、各ドキュメントにメタデータとして`title`フィールドを追加します。

```python
vector_store.add_texts(
    texts=[
        "TiDB Vector offers advanced, high-speed vector processing capabilities, enhancing AI workflows with efficient data handling and analytics support.",
        "TiDB Vector, starting as low as $10 per month for basic usage",
    ],
    metadatas=[
        {"title": "TiDB Vector functionality"},
        {"title": "TiDB Vector Pricing"},
    ],
)
```

期待される出力は以下のとおりです。

```plain
[UUID('c782cb02-8eec-45be-a31f-fdb78914f0a7'),
 UUID('08dcd2ba-9f16-4f29-a9b7-18141f8edae3')]
```

メタデータフィルターを使用して類似性検索を実行します。

```python
docs_with_score = vector_store.similarity_search_with_score(
    "Introduction to TiDB Vector", filter={"title": "TiDB Vector functionality"}, k=4
)
for doc, score in docs_with_score:
    print("-" * 80)
    print("Score: ", score)
    print(doc.page_content)
    print("-" * 80)
```

期待される出力は以下のとおりです。

```plain
--------------------------------------------------------------------------------
Score:  0.12761409169211535
TiDB Vector offers advanced, high-speed vector processing capabilities, enhancing AI workflows with efficient data handling and analytics support.
--------------------------------------------------------------------------------
```

## 高度な使用例：旅行代理店 {#advanced-usage-example-travel-agent}

このセクションでは、旅行代理店向けにベクトル検索とLangchainを統合するユースケースを紹介します。目的は、顧客一人ひとりに合わせた旅行レポートを作成し、清潔なラウンジやベジタリアン向けの食事など、特定の設備を備えた空港を見つける手助けをすることです。

このプロセスは主に2つのステップから構成されます。

1.  空港レビュー全体を対象に意味検索を行い、希望する設備に一致する空港コードを特定します。
2.  SQLクエリを実行してこれらのコードをルート情報と統合し、ユーザーの好みに合致する航空会社と目的地を強調表示します。

### データの準備 {#prepare-data}

まず、空港ルートデータを格納するためのテーブルを作成します。

```python
# Create a table to store flight plan data.
vector_store.tidb_vector_client.execute(
    """CREATE TABLE airplan_routes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        airport_code VARCHAR(10),
        airline_code VARCHAR(10),
        destination_code VARCHAR(10),
        route_details TEXT,
        duration TIME,
        frequency INT,
        airplane_type VARCHAR(50),
        price DECIMAL(10, 2),
        layover TEXT
    );"""
)

# Insert some sample data into airplan_routes and the vector table.
vector_store.tidb_vector_client.execute(
    """INSERT INTO airplan_routes (
        airport_code,
        airline_code,
        destination_code,
        route_details,
        duration,
        frequency,
        airplane_type,
        price,
        layover
    ) VALUES
    ('JFK', 'DL', 'LAX', 'Non-stop from JFK to LAX.', '06:00:00', 5, 'Boeing 777', 299.99, 'None'),
    ('LAX', 'AA', 'ORD', 'Direct LAX to ORD route.', '04:00:00', 3, 'Airbus A320', 149.99, 'None'),
    ('EFGH', 'UA', 'SEA', 'Daily flights from SFO to SEA.', '02:30:00', 7, 'Boeing 737', 129.99, 'None');
    """
)
vector_store.add_texts(
    texts=[
        "Clean lounges and excellent vegetarian dining options. Highly recommended.",
        "Comfortable seating in lounge areas and diverse food selections, including vegetarian.",
        "Small airport with basic facilities.",
    ],
    metadatas=[
        {"airport_code": "JFK"},
        {"airport_code": "LAX"},
        {"airport_code": "EFGH"},
    ],
)
```

期待される出力は以下のとおりです。

```plain
[UUID('6dab390f-acd9-4c7d-b252-616606fbc89b'),
 UUID('9e811801-0e6b-4893-8886-60f4fb67ce69'),
 UUID('f426747c-0f7b-4c62-97ed-3eeb7c8dd76e')]
```

### セマンティック検索を実行する {#perform-a-semantic-search}

以下のコードは、清潔な設備とベジタリアン向けのメニューを備えた空港を検索します。

```python
retriever = vector_store.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"k": 3, "score_threshold": 0.85},
)
semantic_query = "Could you recommend a US airport with clean lounges and good vegetarian dining options?"
reviews = retriever.invoke(semantic_query)
for r in reviews:
    print("-" * 80)
    print(r.page_content)
    print(r.metadata)
    print("-" * 80)
```

期待される出力は以下のとおりです。

```plain
--------------------------------------------------------------------------------
Clean lounges and excellent vegetarian dining options. Highly recommended.
{'airport_code': 'JFK'}
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
Comfortable seating in lounge areas and diverse food selections, including vegetarian.
{'airport_code': 'LAX'}
--------------------------------------------------------------------------------
```

### 空港の詳細情報を取得する {#retrieve-detailed-airport-information}

検索結果から空港コードを抽出し、データベースに詳細なルート情報を照会します。

```python
# Extracting airport codes from the metadata
airport_codes = [review.metadata["airport_code"] for review in reviews]

# Executing a query to get the airport details
search_query = "SELECT * FROM airplan_routes WHERE airport_code IN :codes"
params = {"codes": tuple(airport_codes)}

airport_details = vector_store.tidb_vector_client.execute(search_query, params)
airport_details.get("result")
```

期待される出力は以下のとおりです。

```plain
[(1, 'JFK', 'DL', 'LAX', 'Non-stop from JFK to LAX.', datetime.timedelta(seconds=21600), 5, 'Boeing 777', Decimal('299.99'), 'None'),
 (2, 'LAX', 'AA', 'ORD', 'Direct LAX to ORD route.', datetime.timedelta(seconds=14400), 3, 'Airbus A320', Decimal('149.99'), 'None')]
```

### プロセスを効率化する {#streamline-the-process}

あるいは、単一のSQLクエリを使用してプロセス全体を効率化することもできます。

```python
search_query = f"""
    SELECT
        VEC_COSINE_DISTANCE(se.embedding, :query_vector) as distance,
        ar.*,
        se.document as airport_review
    FROM
        airplan_routes ar
    JOIN
        {TABLE_NAME} se ON ar.airport_code = JSON_UNQUOTE(JSON_EXTRACT(se.meta, '$.airport_code'))
    ORDER BY distance ASC
    LIMIT 5;
"""
query_vector = embeddings.embed_query(semantic_query)
params = {"query_vector": str(query_vector)}
airport_details = vector_store.tidb_vector_client.execute(search_query, params)
airport_details.get("result")
```

期待される出力は以下のとおりです。

```plain
[(0.1219207353407008, 1, 'JFK', 'DL', 'LAX', 'Non-stop from JFK to LAX.', datetime.timedelta(seconds=21600), 5, 'Boeing 777', Decimal('299.99'), 'None', 'Clean lounges and excellent vegetarian dining options. Highly recommended.'),
 (0.14613754359804654, 2, 'LAX', 'AA', 'ORD', 'Direct LAX to ORD route.', datetime.timedelta(seconds=14400), 3, 'Airbus A320', Decimal('149.99'), 'None', 'Comfortable seating in lounge areas and diverse food selections, including vegetarian.'),
 (0.19840519342700513, 3, 'EFGH', 'UA', 'SEA', 'Daily flights from SFO to SEA.', datetime.timedelta(seconds=9000), 7, 'Boeing 737', Decimal('129.99'), 'None', 'Small airport with basic facilities.')]
```

### データのクリーンアップ {#clean-up-data}

最後に、作成したテーブルを削除してリソースをクリーンアップします。

```python
vector_store.tidb_vector_client.execute("DROP TABLE airplan_routes")
```

期待される出力は以下のとおりです。

```plain
{'success': True, 'result': 0, 'error': None}
```

## 関連項目 {#see-also}

-   [ベクトルデータ型](/ai/reference/vector-search-data-types.md)
-   [ベクトル検索インデックス](/ai/reference/vector-search-index.md)
