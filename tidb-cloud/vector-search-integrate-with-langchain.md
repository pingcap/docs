---
title: Integrate Vector Search with LangChain
summary: TiDB Cloudの Vector Search を LangChain と統合する方法を学びます。
---

# ベクトル検索をLangChainと統合する {#integrate-vector-search-with-langchain}

このチュートリアルでは、TiDB Cloudの[ベクトル検索](/tidb-cloud/vector-search-overview.md)機能を[ランチェーン](https://python.langchain.com/)と統合する方法を説明します。

> **注記**
>
> -   TiDB Vector Search は現在ベータ版であり、 [TiDB サーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスターでのみ使用できます。
> -   完全な[サンプルコード](https://github.com/langchain-ai/langchain/blob/master/docs/docs/integrations/vectorstores/tidb_vector.ipynb) Jupyter Notebook で表示したり、サンプル コードを[コラボ](https://colab.research.google.com/github/langchain-ai/langchain/blob/master/docs/docs/integrations/vectorstores/tidb_vector.ipynb)オンライン環境で直接実行したりできます。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、次のものが必要です。

-   [Python 3.8以上](https://www.python.org/downloads/)インストールされました。
-   [ジュピターノートブック](https://jupyter.org/install)インストールされました。
-   [ギット](https://git-scm.com/downloads)インストールされました。
-   TiDB サーバーレス クラスター。TiDB Cloud クラスターがない場合は、 [TiDB サーバーレス クラスターの作成](/tidb-cloud/create-tidb-cluster-serverless.md)に従って独自のTiDB Cloudクラスターを作成してください。

## 始める {#get-started}

このセクションでは、TiDB Vector Search を LangChain と統合してセマンティック検索を実行する手順を段階的に説明します。

### ステップ1. 新しいJupyter Notebookファイルを作成する {#step-1-create-a-new-jupyter-notebook-file}

任意のディレクトリに、 `integrate_with_langchain.ipynb`という名前の新しい Jupyter Notebook ファイルを作成します。

```shell
touch integrate_with_langchain.ipynb
```

### ステップ2. 必要な依存関係をインストールする {#step-2-install-required-dependencies}

プロジェクト ディレクトリで、次のコマンドを実行して必要なパッケージをインストールします。

```shell
!pip install langchain langchain-community
!pip install langchain-openai
!pip install pymysql
!pip install tidb-vector
```

Jupyter Notebook で`integrate_with_langchain.ipynb`ファイルを開き、次のコードを追加して必要なパッケージをインポートします。

```python
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import TiDBVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
```

### ステップ3. 環境を設定する {#step-3-set-up-your-environment}

#### ステップ3.1 TiDBクラスタへの接続文字列を取得する {#step-3-1-obtain-the-connection-string-to-the-tidb-cluster}

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログの構成が動作環境と一致していることを確認します。

    -   **エンドポイント タイプは**`Public`に設定されています。
    -   **ブランチ**は`main`に設定されています。
    -   **Connect With は**`SQLAlchemy`に設定されています。
    -   **オペレーティング システムは**環境に適合します。

4.  **PyMySQL**タブをクリックし、接続文字列をコピーします。

    > **ヒント：**
    >
    > まだパスワードを設定していない場合は、 **「パスワードの生成」**をクリックしてランダムなパスワードを生成します。

#### ステップ3.2 環境変数を設定する {#step-3-2-configure-environment-variables}

安全で効率的なデータベース接続を確立するには、 TiDB Cloudが提供する標準の接続方法を使用します。

このドキュメントでは、埋め込みモデル プロバイダーとして[オープンAI](https://platform.openai.com/docs/introduction)使用します。この手順では、手順 3.1 から取得した接続文字列と[OpenAI APIキー](https://platform.openai.com/docs/quickstart/step-2-set-up-your-api-key)を指定する必要があります。

環境変数を設定するには、次のコードを実行します。接続文字列と OpenAI API キーを入力するよう求められます。

```python
# Use getpass to securely prompt for environment variables in your terminal.
import getpass
import os

# Copy your connection string from the TiDB Cloud console.
# Connection string format: "mysql+pymysql://<USER>:<PASSWORD>@<HOST>:4000/<DB>?ssl_ca=/etc/ssl/cert.pem&ssl_verify_cert=true&ssl_verify_identity=true"
tidb_connection_string = getpass.getpass("TiDB Connection String:")
os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")
```

### ステップ4. サンプル文書を読み込む {#step-4-load-the-sample-document}

#### ステップ4.1 サンプルドキュメントをダウンロードする {#step-4-1-download-the-sample-document}

プロジェクト ディレクトリに`data/how_to/`という名前のディレクトリを作成し、 [langchain-ai/langchain](https://github.com/langchain-ai/langchain) GitHub リポジトリからサンプル ドキュメント[`state_of_the_union.txt`](https://github.com/langchain-ai/langchain/blob/master/docs/docs/how_to/state_of_the_union.txt)をダウンロードします。

```shell
!mkdir -p 'data/how_to/'
!wget 'https://raw.githubusercontent.com/langchain-ai/langchain/master/docs/docs/how_to/state_of_the_union.txt' -O 'data/how_to/state_of_the_union.txt'
```

#### ステップ4.2 ドキュメントを読み込み、分割する {#step-4-2-load-and-split-the-document}

サンプル ドキュメントを`data/how_to/state_of_the_union.txt`から読み込み、 `CharacterTextSplitter`を使用して約 1,000 文字のチャンクに分割します。

```python
loader = TextLoader("data/how_to/state_of_the_union.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)
```

### ステップ5. ドキュメントベクターを埋め込んで保存する {#step-5-embed-and-store-document-vectors}

TiDBベクトルストアは、ベクトル間の類似性を測定するためにコサイン距離（ `consine` ）とユークリッド距離（ `l2` ）の両方をサポートしています。デフォルトの戦略はコサイン距離です。

次のコードは、ベクトル検索に最適化された`embedded_documents`という名前のテーブルを TiDB に作成します。

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

実行が成功すると、TiDB データベース内の`embedded_documents`テーブルを直接表示してアクセスできるようになります。

### ステップ6. ベクトル検索を実行する {#step-6-perform-a-vector-search}

このステップでは、ドキュメント`state_of_the_union.txt`から「大統領は Ketanji Brown Jackson について何と言ったか」を照会する方法を示します。

```python
query = "What did the president say about Ketanji Brown Jackson"
```

#### オプション 1: <code>similarity_search_with_score()</code>を使用する {#option-1-use-code-similarity-search-with-score-code}

`similarity_search_with_score()`メソッドは、ドキュメントとクエリ間のベクトル空間距離を計算します。この距離は、選択された`distance_strategy`によって決定される類似度スコアとして機能します。このメソッドは、スコアが最も低い上位`k`ドキュメントを返します。スコアが低いほど、ドキュメントとクエリ間の類似性が高いことを示します。

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

#### オプション 2: <code>similarity_search_with_relevance_scores()</code>を使用する {#option-2-use-code-similarity-search-with-relevance-scores-code}

`similarity_search_with_relevance_scores()`メソッドは、関連性スコアが最も高い上位`k`ドキュメントを返します。スコアが高いほど、ドキュメントとクエリの類似度が高いことを示します。

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

### レトリーバーとして使用する {#use-as-a-retriever}

Langchain では、 [レトリーバー](https://python.langchain.com/v0.2/docs/concepts/#retrievers)は非構造化クエリに応答してドキュメントを取得するインターフェースであり、ベクター ストアよりも多くの機能を提供します。次のコードは、TiDB ベクター ストアを取得子として使用する方法を示しています。

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

期待される出力は次のとおりです。

    --------------------------------------------------------------------------------
    Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections.

    Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service.

    One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court.

    And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.
    --------------------------------------------------------------------------------

### ベクトルストアを削除する {#remove-the-vector-store}

既存の TiDB ベクトル ストアを削除するには、 `drop_vectorstore()`メソッドを使用します。

```python
vector_store.drop_vectorstore()
```

## メタデータフィルターで検索 {#search-with-metadata-filters}

検索を絞り込むには、メタデータ フィルターを使用して、適用したフィルターに一致する特定の最も近い結果を取得できます。

### サポートされているメタデータタイプ {#supported-metadata-types}

TiDB ベクトル ストア内の各ドキュメントは、JSON オブジェクト内のキーと値のペアとして構造化されたメタデータとペアにすることができます。キーは常に文字列ですが、値は次のいずれかの型になります。

-   弦
-   数値: 整数または浮動小数点数
-   ブール値: `true`または`false`

たとえば、有効なメタデータ ペイロードは次のとおりです。

```json
{
  "page": 12,
  "book_title": "Siddhartha"
}
```

### メタデータフィルター構文 {#metadata-filter-syntax}

利用可能なフィルターは次のとおりです。

-   `$or` : 指定された条件のいずれかに一致するベクトルを選択します。
-   `$and` : 指定されたすべての条件に一致するベクトルを選択します。
-   `$eq` : 指定された値と等しい。
-   `$ne` : 指定された値と等しくありません。
-   `$gt` : 指定された値より大きい。
-   `$gte` : 指定された値以上。
-   `$lt` : 指定された値より小さい。
-   `$lte` : 指定された値以下。
-   `$in` : 指定された値の配列内。
-   `$nin` : 指定された値の配列に存在しません。

ドキュメントのメタデータが次のとおりである場合:

```json
{
  "page": 12,
  "book_title": "Siddhartha"
}
```

次のメタデータ フィルターがこのドキュメントに一致します。

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

メタデータ フィルター内の各キーと値のペアは個別のフィルター句として扱われ、これらの句は`AND`論理演算子を使用して結合されます。

### 例 {#example}

次の例では、ドキュメント`TiDBVectorStore`に 2 つのドキュメントを追加し、各ドキュメントにメタデータとしてフィールド`title`を追加します。

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

期待される出力は次のとおりです。

```plain
[UUID('c782cb02-8eec-45be-a31f-fdb78914f0a7'),
 UUID('08dcd2ba-9f16-4f29-a9b7-18141f8edae3')]
```

メタデータ フィルターを使用して類似性検索を実行します。

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

期待される出力は次のとおりです。

```plain
--------------------------------------------------------------------------------
Score:  0.12761409169211535
TiDB Vector offers advanced, high-speed vector processing capabilities, enhancing AI workflows with efficient data handling and analytics support.
--------------------------------------------------------------------------------
```

## 高度な使用例: 旅行代理店 {#advanced-usage-example-travel-agent}

このセクションでは、旅行代理店向けにベクトル検索と Langchain を統合する高度なユースケースを紹介します。目標は、清潔なラウンジやベジタリアン向けのオプションなど、特定のアメニティを備えた空港を探している顧客向けに、パーソナライズされた旅行レポートを作成することです。

このプロセスには主に 2 つのステップが含まれます。

1.  空港レビュー全体でセマンティック検索を実行し、希望する設備に一致する空港コードを特定します。
2.  SQL クエリを実行してこれらのコードをルート情報とマージし、ユーザーの好みに一致する航空会社と目的地を強調表示します。

### データを準備する {#prepare-data}

まず、空港ルートデータを保存するテーブルを作成します。

```python
# Create table to store airplan data.
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

期待される出力は次のとおりです。

```plain
[UUID('6dab390f-acd9-4c7d-b252-616606fbc89b'),
 UUID('9e811801-0e6b-4893-8886-60f4fb67ce69'),
 UUID('f426747c-0f7b-4c62-97ed-3eeb7c8dd76e')]
```

### セマンティック検索を実行する {#perform-a-semantic-search}

次のコードは、清潔な施設とベジタリアン向けのオプションを備えた空港を検索します。

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

期待される出力は次のとおりです。

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

### 詳細な空港情報を取得する {#retrieve-detailed-airport-information}

検索結果から空港コードを抽出し、詳細なルート情報をデータベースに照会します。

```python
# Extracting airport codes from the metadata
airport_codes = [review.metadata["airport_code"] for review in reviews]

# Executing a query to get the airport details
search_query = "SELECT * FROM airplan_routes WHERE airport_code IN :codes"
params = {"codes": tuple(airport_codes)}

airport_details = vector_store.tidb_vector_client.execute(search_query, params)
airport_details.get("result")
```

期待される出力は次のとおりです。

```plain
[(1, 'JFK', 'DL', 'LAX', 'Non-stop from JFK to LAX.', datetime.timedelta(seconds=21600), 5, 'Boeing 777', Decimal('299.99'), 'None'),
 (2, 'LAX', 'AA', 'ORD', 'Direct LAX to ORD route.', datetime.timedelta(seconds=14400), 3, 'Airbus A320', Decimal('149.99'), 'None')]
```

### プロセスを合理化する {#streamline-the-process}

あるいは、単一の SQL クエリを使用してプロセス全体を合理化することもできます。

```python
search_query = f"""
    SELECT
        VEC_Cosine_Distance(se.embedding, :query_vector) as distance,
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

期待される出力は次のとおりです。

```plain
[(0.1219207353407008, 1, 'JFK', 'DL', 'LAX', 'Non-stop from JFK to LAX.', datetime.timedelta(seconds=21600), 5, 'Boeing 777', Decimal('299.99'), 'None', 'Clean lounges and excellent vegetarian dining options. Highly recommended.'),
 (0.14613754359804654, 2, 'LAX', 'AA', 'ORD', 'Direct LAX to ORD route.', datetime.timedelta(seconds=14400), 3, 'Airbus A320', Decimal('149.99'), 'None', 'Comfortable seating in lounge areas and diverse food selections, including vegetarian.'),
 (0.19840519342700513, 3, 'EFGH', 'UA', 'SEA', 'Daily flights from SFO to SEA.', datetime.timedelta(seconds=9000), 7, 'Boeing 737', Decimal('129.99'), 'None', 'Small airport with basic facilities.')]
```

### 掃除 {#clean-up}

最後に、作成したテーブルを削除してリソースをクリーンアップします。

```python
vector_store.tidb_vector_client.execute("DROP TABLE airplan_routes")
```

期待される出力は次のとおりです。

```plain
{'success': True, 'result': 0, 'error': None}
```

## 参照 {#see-also}

-   [ベクトルデータ型](/tidb-cloud/vector-search-data-types.md)
-   [ベクター検索インデックス](/tidb-cloud/vector-search-index.md)
