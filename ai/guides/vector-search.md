---
title: Vector Search
summary: アプリケーションでベクター検索を使用する方法を学習します。
---

# ベクトル検索 {#vector-search}

ベクトル検索では、意味的類似性を使用して、クエリにすべてのキーワードが明示的に含まれていない場合でも、最も関連性の高いレコードを見つけやすくします。

> **注記：**
>
> ベクトル検索の完全な例については、 [ベクトル検索の例](/ai/examples/vector-search-with-pytidb.md)参照してください。

## 基本的な使い方 {#basic-usage}

このセクションでは、アプリケーションでベクトル検索を使用する方法を数ステップで説明します。始める前に、 [データベースに接続する](/ai/guides/connect.md) .

### ステップ1. ベクトルフィールドを持つテーブルを作成する {#step-1-create-a-table-with-a-vector-field}

<SimpleTab groupId="language">
<div label="Python" value="python">

`client.create_table()`使用してテーブルを作成し、 `VectorField`使用してベクトル フィールドを定義できます。

次の例では、4 つの列を持つ`documents`テーブルを作成します。

-   `id` : テーブルの主キー。
-   `text` : ドキュメントのテキストコンテンツ。
-   `text_vec` : テキスト コンテンツのベクトル埋め込み。
-   `meta` : ドキュメントのメタデータ (JSON オブジェクト)。

```python hl_lines="9"
from pytidb.schema import TableModel, Field, VectorField
from pytidb.datatype import TEXT, JSON

class Document(TableModel):
    __tablename__ = "documents"

    id: int = Field(primary_key=True)
    text: str = Field(sa_type=TEXT)
    text_vec: list[float] = VectorField(dimensions=3)
    meta: dict = Field(sa_type=JSON, default_factory=dict)

table = client.create_table(schema=Document, if_exists="overwrite")
```

`VectorField`クラスは次のパラメータを受け入れます。

-   `dimensions` : ベクトルの次元。指定すると、このフィールドには指定した次元のベクトルのみが格納されます。
-   `index` : ベクトルフィールドに[ベクトルインデックス](https://docs.pingcap.com/tidbcloud/vector-search-index/)を作成するかどうか。デフォルトは`True`です。
-   `distance_metric` : ベクトルインデックスに使用する距離メトリック。サポートされる値:
    -   `DistanceMetric.COSINE` （デフォルト）: コサイン距離メトリック。テキストの類似性を測定するのに適しています。
    -   `DistanceMetric.L2` : L2距離メトリック、全体的な差異を捉えるのに適しています

</div>
<div label="SQL" value="sql">

`CREATE TABLE`ステートメントを使用してテーブルを作成し、 `VECTOR`型を使用してベクトル列を定義します。

```sql hl_lines="4 5"
CREATE TABLE documents (
    id INT PRIMARY KEY,
    text TEXT,
    text_vec VECTOR(3),
    VECTOR INDEX `vec_idx_text_vec`((VEC_COSINE_DISTANCE(`text_vec`)))
);
```

この例では、

-   `text_vec`列目は`VECTOR(3)`として定義されているため、この列に格納されるベクトルは 3 次元である必要があります。
-   ベクトル検索のパフォーマンスを最適化するために、 `VEC_COSINE_DISTANCE`関数を使用してベクトル インデックスが作成されます。

TiDB はベクトル インデックスに対して 2 つの距離関数をサポートしています。

-   `VEC_COSINE_DISTANCE` : 2つのベクトル間のコサイン距離を計算する
-   `VEC_L2_DISTANCE` : 2つのベクトル間のL2距離（ユークリッド距離）を計算する

</div>
</SimpleTab>

### ステップ2. テーブルにベクターデータを挿入する {#step-2-insert-vector-data-into-the-table}

デモンストレーションとして、いくつかのテキストとそれに対応する埋め込みをテーブルに挿入します。

次の例では、それぞれ単純な 3 次元ベクトル埋め込みを持つ 3 つのドキュメントを挿入します。

-   `dog`ベクトル埋め込み`[1, 2, 1]`
-   `fish`ベクトル埋め込み`[1, 2, 4]`
-   `tree`ベクトル埋め込み`[1, 0, 0]`

<SimpleTab groupId="language">
<div label="Python" value="python">

```python
table.bulk_insert([
    Document(text="dog", text_vec=[1,2,1], meta={"category": "animal"}),
    Document(text="fish", text_vec=[1,2,4], meta={"category": "animal"}),
    Document(text="tree", text_vec=[1,0,0], meta={"category": "plant"}),
])
```

</div>
<div label="SQL" value="sql">

```sql
INSERT INTO documents (id, text, text_vec, meta)
VALUES
    (1, 'dog', '[1,2,1]', '{"category": "animal"}'),
    (2, 'fish', '[1,2,4]', '{"category": "animal"}'),
    (3, 'tree', '[1,0,0]', '{"category": "plant"}');
```

> **注記：**
>
> 実際のアプリケーションでは、埋め込みは通常[埋め込みモデル](/ai/concepts/vector-search-overview.md#embedding-model)によって生成されます。

利便性のため、pytidb は、挿入、更新、または検索時にテキスト フィールドのベクトル埋め込みを自動的に生成できる自動埋め込み機能を提供します。手動処理は必要ありません。

詳細は[自動埋め込み](/ai/guides/auto-embedding.md)ガイドをご覧ください。

</div>
</SimpleTab>

### ステップ3. ベクトル検索を実行する {#step-3-perform-vector-search}

ベクトル検索では、ベクトル距離指標を用いてベクトル間の類似性と関連性を測定します。距離が近いほど、レコードの関連性が高くなります。テーブル内で最も関連性の高いドキュメントを見つけるには、クエリベクトルを指定する必要があります。

次の例では、クエリが`A swimming animal`で、そのベクトル埋め込みが`[1, 2, 3]`あると想定しています。

<SimpleTab groupId="language">
<div label="Python" value="python">

ベクトル検索を実行するには`table.search()`メソッドを使用します。デフォルトでは`search_mode="vector"`が使用されます。

```python
table.search([1, 2, 3]).limit(3).to_list()
```

```python title="Execution result"
[
    {"id": 2, "text": "fish", "text_vec": [1,2,4], "_distance": 0.00853986601633272},
    {"id": 1, "text": "dog", "text_vec": [1,2,1], "_distance": 0.12712843905603044},
    {"id": 3, "text": "tree", "text_vec": [1,0,0], "_distance": 0.7327387580875756},
]
```

結果によると、最も関連性の高いドキュメントは距離が`0.00853986601633272`の`fish`です。

</div>
<div label="SQL" value="sql">

クエリ ベクトルの`n`最も近い近傍を取得するには、 `SELECT`ステートメントの`ORDER BY <distance_function>(<column_name>, <query_vector>) LIMIT <n>`句を使用します。

次の例では、 `vec_cosine_distance`関数を使用して、 `text_vec`列に格納されているベクトルと指定されたクエリ ベクトル`[1, 2, 3]`間のコサイン距離を計算します。

```sql
SELECT id, text, vec_cosine_distance(text_vec, '[1,2,3]') AS distance
FROM documents
ORDER BY distance
LIMIT 3;
```

```plain title="Execution result"
+----+----------+---------------------+
| id | text     | distance            |
+----+----------+---------------------+
|  2 | fish     | 0.00853986601633272 |
|  1 | dog      | 0.12712843905603044 |
|  3 | tree     |  0.7327387580875756 |
+----+----------+---------------------+
3 rows in set (0.15 sec)
```

結果によると、最も関連性の高いドキュメントは距離が`0.00853986601633272`の`fish`です。

</div>
</SimpleTab>

## 距離測定 {#distance-metrics}

距離メトリクスは、ベクトルのペア間の類似度を測る尺度です。現在、TiDBは以下の距離メトリクスをサポートしています。

<SimpleTab groupId="language">
<div label="Python" value="python">

`table.search()` API は次の距離メトリックをサポートしています。

| メトリック名                  | 説明                                           | 最適な用途              |
| ----------------------- | -------------------------------------------- | ------------------ |
| `DistanceMetric.COSINE` | 2つのベクトル間のコサイン距離を計算します（デフォルト）。ベクトル間の角度を測定します。 | テキスト埋め込み、セマンティック検索 |
| `DistanceMetric.L2`     | 2つのベクトル間のL2距離（ユークリッド距離）を計算します。直線距離を測定します。    | 画像の特徴              |

ベクトル検索に使用する距離メトリックを変更するには、 `.distance_metric()`メソッドを使用します。

**例: L2距離メトリックを使用する**

```python
from pytidb.schema import DistanceMetric

results = (
    table.search([1, 2, 3])
        .distance_metric(DistanceMetric.L2)
        .limit(10)
        .to_list()
)
```

</div>
<div label="SQL" value="sql">

SQL では、次の組み込み関数を使用して、クエリ内でベクトル距離を直接計算できます。

| 関数名                                                                                                                                  | 説明                            |
| ------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------- |
| [`VEC_L2_DISTANCE`](https://docs.pingcap.com/tidbcloud/vector-search-functions-and-operators/#vec_l2_distance)                       | 2つのベクトル間のL2距離（ユークリッド距離）を計算します |
| [`VEC_COSINE_DISTANCE`](https://docs.pingcap.com/tidbcloud/vector-search-functions-and-operators/#vec_cosine_distance)               | 2つのベクトル間のコサイン距離を計算します         |
| [`VEC_NEGATIVE_INNER_PRODUCT`](https://docs.pingcap.com/tidbcloud/vector-search-functions-and-operators/#vec_negative_inner_product) | 2つのベクトルの内積の負数を計算します           |
| [`VEC_L1_DISTANCE`](https://docs.pingcap.com/tidbcloud/vector-search-functions-and-operators/#vec_l1_distance)                       | 2つのベクトル間のL1距離（マンハッタン距離）を計算します |

</div>
</SimpleTab>

## 距離閾値 {#distance-threshold}

`table.search()` APIでは、距離の閾値を設定して、返される結果の類似度を制御できます。この閾値を指定することで、類似度の低いベクトルを除外し、関連性基準を満たすベクトルのみを返すことができます。

<SimpleTab groupId="language">
<div label="Python" value="python">

`.distance_threshold()`メソッドを使用して、検索結果の最大距離を設定します。しきい値未満の距離を持つレコードのみが返されます。

**例: 距離が 0.5 未満のドキュメントのみを返す**

```python
results = table.search([1, 2, 3]).distance_threshold(0.5).limit(10).to_list()
```

</div>
<div label="SQL" value="sql">

SQL では、距離関数を含む`HAVING`句を使用して、距離で結果をフィルタリングします。

**例: 距離が 0.1 未満のドキュメントのみを返す**

```sql
SELECT id, text, vec_cosine_distance(text_vec, '[1,2,3]') AS distance
FROM documents
HAVING distance < 0.1
ORDER BY distance
LIMIT 10;
```

</div>
</SimpleTab>

## 距離範囲 {#distance-range}

`table.search()` API では、結果をさらに絞り込むために距離範囲を指定することもサポートされています。

<SimpleTab groupId="language">
<div label="Python" value="python">

最小距離と最大距離の両方を設定するには、 `.distance_range()`メソッドを使用します。この範囲内の距離を持つレコードのみが返されます。

**例: 距離が 0.01 から 0.05 までのドキュメントのみを返す**

```python
results = table.search([1, 2, 3]).distance_range(0.01, 0.05).limit(10).to_list()
```

</div>
<div label="SQL" value="sql">

SQL で距離の範囲を指定するには、 `HAVING`句で`BETWEEN`またはその他の比較演算子を使用します。

**例: 距離が 0.01 から 0.05 までのドキュメントのみを返す**

```sql
SELECT id, text, vec_l2_distance(text_vec, '[1,2,3]') AS distance
FROM documents
HAVING distance BETWEEN 0.01 AND 0.05
ORDER BY distance
LIMIT 10;
```

</div>
</SimpleTab>

## メタデータフィルタリング {#metadata-filtering}

リレーショナル データベースである TiDB は、豊富なセット[SQL演算子](https://docs.pingcap.com/tidbcloud/operators/)をサポートし、フィルタリング条件の柔軟な組み合わせを可能にします。

TiDB でのベクトル検索では、スカラー フィールド (整数や文字列など) または JSON フィールドにメタデータ フィルタリングを適用できます。

通常、メタデータ フィルタリングと組み合わせたベクター検索には、次の 2 つのモードがあります。

-   **後フィルタリング**：TiDBはまずベクトル検索を実行し、ベクトル空間全体から上位k個の候補を取得し、その候補セットにフィルターを適用します。ベクトル検索段階では、効率性を高めるため、通常、ベクトルインデックスが使用されます。
-   **事前フィルタリング**：TiDBはベクター検索の前にフィルタを適用します。フィルタの選択性が高く、フィルタリング対象フィールドにスカラーインデックスがある場合、このモードにより検索空間が縮小され、パフォーマンスが向上します。

### 後フィルタリング {#post-filtering}

<SimpleTab groupId="language">
<div label="Python" value="python">

フィルター辞書を持つ`.filter()`メソッドを使用して、ベクトル検索にフィルターを適用します。

デフォルトでは、 `table.search()` API はポストフィルタリング モードを使用して、ベクター インデックスによる検索パフォーマンスを最大化します。

**例: ポストフィルタリングによるベクトル検索**

```python
results = (
    table.search([1, 2, 3])
        # The `meta` is a JSON field, and its value is a JSON object
        # like {"category": "animal"}
        .filter({"meta.category": "animal"})
        .num_candidate(50)
        .limit(10)
        .to_list()
)
```

> **注記：**
>
> ベクトルインデックスを使用する場合、最後の`limit`が非常に小さいと結果の精度が低下する可能性があります。3 `.num_candidate()`の方法を使用すると、ベクトル検索フェーズでベクトルインデックスから取得する候補の数を、 `limit`番目のパラメータを変更せずに制御できます。

> `num_candidate`値を大きくすると、一般的に再現率は向上しますが、クエリのパフォーマンスが低下する可能性があります。データセットと精度要件に応じてこの値を調整してください。

</div>
<div label="SQL" value="sql">

現在、ベクトル インデックスは、次のような厳密な ANN (近似最近傍) クエリでのみ有効です。

```sql
SELECT * FROM <table> ORDER BY <distance_func>(<column>) LIMIT <n>
```

つまり、同じクエリ内で`WHERE`句とベクトル インデックスを一緒に使用することはできません。

ベクトル検索と追加のフィルタリング条件を組み合わせる必要がある場合は、ポストフィルタリングパターンを使用できます。このアプローチでは、ANNクエリは2つの部分に分割されます。

-   内部クエリは、ベクトル インデックスを使用してベクトル検索を実行します。
-   外側のクエリは`WHERE`条件を適用して結果をフィルタリングします。

```sql hl_lines="8"
SELECT *
FROM (
    SELECT id, text, meta, vec_cosine_distance(text_vec, '[1,2,3]') AS distance
    FROM documents
    ORDER BY distance
    LIMIT 50
) candidates
WHERE meta->>'$.category' = 'animal'
ORDER BY distance
LIMIT 10;
```

> **注記：**
>
> 後続フィルタリングパターンにより、結果が空になる場合があります。例えば、内部クエリで最も類似度の高い上位50件のレコードが取得されるものの、条件`WHERE`に一致するレコードが1件も存在しない場合などです。
>
> これを軽減するには、**内部クエリ**の`LIMIT`値 (例: 50) を増やして、より多くの候補を取得し、フィルタリング後に十分な有効な結果が返される可能性を高めることができます。

サポートされている SQL 演算子については、 TiDB Cloudドキュメントの[オペレーター](https://docs.pingcap.com/tidbcloud/operators/)参照してください。

</div>
</SimpleTab>

### プレフィルタリング {#pre-filtering}

<SimpleTab groupId="language">
<div label="Python" value="python">

事前フィルタリングを有効にするには、 `.filter()`方法で`prefilter=True`設定します。

**例: 事前フィルタリングによるベクトル検索**

```python
results = (
    table.search([1, 2, 3])
        .filter({"meta.category": "animal"}, prefilter=True)
        .limit(10)
        .to_list()
)
```

サポートされているフィルター演算子については、 [フィルタリング](/ai/guides/filtering.md)参照してください。

</div>
<div label="SQL" value="sql">

SQL では、 `->>`演算子または`JSON_EXTRACT`を使用して、 `WHERE`句の JSON フィールドにアクセスします。

```sql
SELECT id, text, meta, vec_cosine_distance(text_vec, '[1,2,3]') AS distance
FROM documents
WHERE meta->>'$.category' = 'animal'
ORDER BY distance
LIMIT 10;
```

サポートされている SQL 演算子については、 TiDB Cloudドキュメントの[オペレーター](https://docs.pingcap.com/tidbcloud/operators/)参照してください。

</div>
</SimpleTab>

## 複数のベクトル場 {#multiple-vector-fields}

TiDB は、単一のテーブルに複数のベクトル列を定義することをサポートしており、さまざまな種類のベクトル埋め込みを保存および検索できます。

たとえば、テキスト埋め込みと画像埋め込みの両方を同じテーブルに保存できるため、マルチモーダル データの管理に便利です。

<SimpleTab groupId="language">
<div label="Python" value="python">

スキーマ内に複数のベクトル フィールドを定義し、 `.vector_column()`メソッドを使用して指定されたベクトル フィールドに対してベクトル検索を実行できます。

**例: 検索するベクトル場を指定する**

```python hl_lines="6 8 17"
# Create a table with multiple vector fields
class RichTextDocument(TableModel):
    __tablename__ = "rich_text_documents"
    id: int = Field(primary_key=True)
    text: str = Field(sa_type=TEXT)
    text_vec: list[float] = VectorField(dimensions=3)
    image_url: str
    image_vec: list[float] = VectorField(dimensions=3)

table = client.create_table(schema=RichTextDocument, if_exists="overwrite")

# Insert sample data ...

# Search using image vector field
results = (
    table.search([1, 2, 3])
        .vector_column("image_vec")
        .distance_metric(DistanceMetric.COSINE)
        .limit(10)
        .to_list()
)
```

</div>
<div label="SQL" value="sql">

テーブル内に複数のベクトル列を作成し、適切な距離関数を使用してそれらを検索することができます。

```sql
-- Create a table with multiple vector fields
CREATE TABLE rich_text_documents (
    id BIGINT PRIMARY KEY,
    text TEXT,
    text_vec VECTOR(3),
    image_url VARCHAR(255),
    image_vec VECTOR(3)
);

-- Insert sample data ...

-- Search using text vector
SELECT id, image_url, vec_l2_distance(image_vec, '[4,5,6]') AS image_distance
FROM rich_text_documents
ORDER BY image_distance
LIMIT 10;
```

</div>
</SimpleTab>

## 検索結果を出力する {#output-search-results}

`table.search()` API を使用すると、検索結果をいくつかの一般的なデータ処理形式に変換できます。

### SQLAlchemyの結果行として {#as-sqlalchemy-result-rows}

生の SQLAlchemy 結果行を操作するには、次を使用します。

```python
table.search([1, 2, 3]).limit(10).to_rows()
```

### Python辞書のリストとして {#as-a-list-of-python-dictionaries}

Python での操作を容易にするために、結果を辞書のリストに変換します。

```python
table.search([1, 2, 3]).limit(10).to_list()
```

### pandas DataFrameとして {#as-a-pandas-dataframe}

結果をユーザーフレンドリーな表で表示するには (特に Jupyter ノートブックで便利です)、結果を pandas DataFrame に変換します。

```python
table.search([1, 2, 3]).limit(10).to_pandas()
```

### Pydanticモデルインスタンスのリストとして {#as-a-list-of-pydantic-model-instances}

`TableModel`クラスは、データエンティティを表す Pydantic モデルとしても使用できます。結果を Pydantic モデルインスタンスとして操作するには、以下を使用します。

```python
table.search([1, 2, 3]).limit(10).to_pydantic()
```
