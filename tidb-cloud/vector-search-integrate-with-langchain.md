---
title: Integrate Vector Search with LangChain
summary: 
---

# Integrate Vector Search with LangChain

This tutorial will walk you through how to integrate the TiDB vector search feature with [LangChain](https://python.langchain.com/).

> **Note**
>
> TiDB Vector Search is only available for TiDB Serverless at this moment.

> **Tips**
>
> You can check the complete [sample code](https://github.com/langchain-ai/langchain/blob/master/docs/docs/integrations/vectorstores/tidb_vector.ipynb) on Jupyter Notebook, or run the sample code directly in the [colab](https://colab.research.google.com/github/langchain-ai/langchain/blob/master/docs/docs/integrations/vectorstores/tidb_vector.ipynb) online environment.

## Prerequisites

To complete this tutorial, you need:

- [Python 3.8 or higher](https://www.python.org/downloads/) installed.
- [Jupyter Notebook](https://jupyter.org/install) installed.
- [Git](https://git-scm.com/downloads) installed.
- A TiDB Serverless cluster running.

<CustomContent platform="tidb-cloud">

**If you don't have a TiDB cluster, you can create one as follows:**

- Follow [Creating a TiDB Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md) to create your own TiDB Cloud cluster.

</CustomContent>

## Get Started

In this section, you can learn step-by-step how to use LangChain to integrate with TiDB vector search and perform semantic search.

### Step 1. Create a new Jupyter Notebook file

Create a new Jupyter Notebook file in your preferred directory.

```shell
touch integrate_with_langchain.ipynb
```

### Step 2. Install required dependencies

Run the following command on your project directory to install the required packages:

```shell
!pip install langchain langchain-community
!pip install langchain-openai
!pip install pymysql
!pip install tidb-vector
```

Import the required packages in your code:

```python
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import TiDBVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
```

### Step 3. Set up environments

#### Step 3.1 Obtains the connection string to the TiDB cluster

<SimpleTab>
<div label="TiDB Serverless">

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. Ensure the configurations in the connection dialog match your operating environment.

    - **Endpoint Type** is set to `Public`
    - **Branch** is set to `main`
    - **Connect With** is set to `SQLAlchemy`
    - **Operating System** matches your environment.

4. Switch to the **PyMySQL** tab and click the **Copy** icon to copy the connection string.

</div>

</SimpleTab>

#### Step 3.2 Configure the environment variables

Configure both the OpenAI and TiDB connection string settings that you will need.

In this notebook, we will follow the standard connection method provided by TiDB Cloud to establish a secure and efficient database connection.

```python
# Here we useimport getpass
import getpass
import os

os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")
# Copy from TiDB Cloud Console
# The format of connection string: "mysql+pymysql://<USER>:<PASSWORD>@<HOST>:4000/<DB>?ssl_ca=/etc/ssl/cert.pem&ssl_verify_cert=true&ssl_verify_identity=true"
tidb_connection_string = getpass.getpass("TiDB Connection String:")
```

### Step 4. Load the sample document

#### Step 4.1 Download the sample document

Download the sample document `state_of_the_union.txt` from the GitHub repository.

```shell
!mkdir -p 'data/how_to/'
!wget 'https://raw.githubusercontent.com/langchain-ai/langchain/master/docs/docs/how_to/state_of_the_union.txt' -O 'data/how_to/state_of_the_union.txt'
```

#### Step 4.2 Load documents

Load the sample document from the directory with the `SimpleDirectoryReader` class.

```python
loader = TextLoader("data/how_to/state_of_the_union.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)
```

### Step 5. Build index

TiDB Vector Store supports both cosine distance (`consine`) and Euclidean distance (`l2`), and the default distance strategy is cosine distance.

The code snippet below creates a table named `embedded_documents` in TiDB, which is optimized for vector searching.

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

Upon successful execution of this code, you will be able to view and access the `embedded_documents` table directly within your TiDB database.

### Step 6. Semantic similarity search

For example, we will query "What did the president say about Ketanji Brown Jackson" from the document `state_of_the_union.txt`.

```python
query = "What did the president say about Ketanji Brown Jackson"
```

#### Step 6.1 Execute `similarity_search_with_score` method

The `similarity_search_with_score` method calculates the vector space distance between the documents and the query as the `score` based on the `distance_strategy` strategy, and then returns the top `k` documents with the lowest score. The lower the score, the higher the similarity.

```python
docs_with_score = vector_store.similarity_search_with_score(query, k=3)
for doc, score in docs_with_score:
   print("-" * 80)
   print("Score: ", score)
   print(doc.page_content)
   print("-" * 80)
```

<details>
   <summary><b>Excepted output</b></summary>

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


#### Step 6.2 Execute `similarity_search_with_relevance_scores` method

Additionally, the `similarity_search_with_relevance_scores` method returns the top `k` documents with the highest relevance score. The higher the score, the higher the similarity between the documents and the query.

```python
docs_with_relevance_score = vector_store.similarity_search_with_relevance_scores(query, k=2)
for doc, score in docs_with_relevance_score:
    print("-" * 80)
    print("Score: ", score)
    print(doc.page_content)
    print("-" * 80)
```

<details>
   <summary><b>Excepted output</b></summary>

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


### Using as a Retriever

In Langchain, a retriever is an interface that retrieves documents in response to an unstructured query, offering a broader functionality than a vector store. The code below demonstrates how to utilize TiDB Vector as a retriever.

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

Excepted output:

```
--------------------------------------------------------------------------------
Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. 

Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. 

One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. 

And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.
--------------------------------------------------------------------------------
```

### Drop the vector store

You can remove the TiDB Vector Store by using the `.drop_vectorstore()` method.

```python
vector_store.drop_vectorstore()
```

## Metadata Filter 

Perform searches using metadata filters to retrieve a specific number of nearest-neighbor results that align with the applied filters.

### Supported metadata types

Each document in the TiDB Vector Store can be paired with metadata, structured as key-value pairs within a JSON object.

The keys are strings, and the values can be of the following types:

- String
- Number (integer or floating point)
- Booleans (true, false)

For instance, consider the following valid metadata payloads:

```json
{
    "page": 12,
    "book_title": "Siddhartha"
}
```

### Metadata filter syntax

The available filters include:

- `$or` - Selects vectors that meet any one of the given conditions.
- `$and` - Selects vectors that meet all the given conditions.
- `$eq` - Equal to
- `$ne` - Not equal to
- `$gt` - Greater than
- `$gte` - Greater than or equal to
- `$lt` - Less than
- `$lte` - Less than or equal to
- `$in` - In array
- `$nin` - Not in array

For example, assuming there is a document with the following metadata:

```json
{
   "page": 12,
   "book_title": "Siddhartha"
}
```

The following metadata filters are able to match the above document:

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

Please note that each key-value pair in the metadata filters is treated as a separate filter clause, and these clauses are combined using the AND logical operator.

### Metadata filter Example

For example, we add two documents to `TiDBVectorStore`, and add a `title` field to each document as the metadata.

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

Excepted output:

```plain
[UUID('c782cb02-8eec-45be-a31f-fdb78914f0a7'),
 UUID('08dcd2ba-9f16-4f29-a9b7-18141f8edae3')]
```

Perform similarity search with metadata filters:

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

Excepted output:

```plain
--------------------------------------------------------------------------------
Score:  0.12761409169211535
TiDB Vector offers advanced, high-speed vector processing capabilities, enhancing AI workflows with efficient data handling and analytics support.
--------------------------------------------------------------------------------
```

## Advanced Examples

### Travel Agent

Let's look at an advanced use case — a travel agent is crafting a custom travel report for clients who desire airports with specific amenities such as clean lounges and vegetarian options.

The process involves:

- A semantic search within airport reviews to extract airport codes meeting these amenities.

- A later SQL query that joins these codes with route information, detailing airlines and destinations aligned with the clients' preferences.

First, let's prepare some airport related data.

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

Excepted output:

```plain
[UUID('6dab390f-acd9-4c7d-b252-616606fbc89b'),
 UUID('9e811801-0e6b-4893-8886-60f4fb67ce69'),
 UUID('f426747c-0f7b-4c62-97ed-3eeb7c8dd76e')]
```

Finding Airports with Clean Facilities and Vegetarian Options via Vector Search.

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

Excepted output:

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

```python
# Extracting airport codes from the metadata
airport_codes = [review.metadata["airport_code"] for review in reviews]

# Executing a query to get the airport details
search_query = "SELECT * FROM airplan_routes WHERE airport_code IN :codes"
params = {"codes": tuple(airport_codes)}

airport_details = vector_store.tidb_vector_client.execute(search_query, params)
airport_details.get("result")
```

Excepted output:

```plain
[(1, 'JFK', 'DL', 'LAX', 'Non-stop from JFK to LAX.', datetime.timedelta(seconds=21600), 5, 'Boeing 777', Decimal('299.99'), 'None'),
 (2, 'LAX', 'AA', 'ORD', 'Direct LAX to ORD route.', datetime.timedelta(seconds=14400), 3, 'Airbus A320', Decimal('149.99'), 'None')]
```

Alternatively, we can streamline the process by using a single SQL query to achieve the search in one step.

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

Excepted output:

```plain
[(0.1219207353407008, 1, 'JFK', 'DL', 'LAX', 'Non-stop from JFK to LAX.', datetime.timedelta(seconds=21600), 5, 'Boeing 777', Decimal('299.99'), 'None', 'Clean lounges and excellent vegetarian dining options. Highly recommended.'),
 (0.14613754359804654, 2, 'LAX', 'AA', 'ORD', 'Direct LAX to ORD route.', datetime.timedelta(seconds=14400), 3, 'Airbus A320', Decimal('149.99'), 'None', 'Comfortable seating in lounge areas and diverse food selections, including vegetarian.'),
 (0.19840519342700513, 3, 'EFGH', 'UA', 'SEA', 'Daily flights from SFO to SEA.', datetime.timedelta(seconds=9000), 7, 'Boeing 737', Decimal('129.99'), 'None', 'Small airport with basic facilities.')]
```

Clean up the table.

```python
vector_store.tidb_vector_client.execute("DROP TABLE airplan_routes")
```

Excepted output:

```plain
{'success': True, 'result': 0, 'error': None}
```
