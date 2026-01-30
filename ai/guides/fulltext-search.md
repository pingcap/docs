# Full-text Search

**Full-text search** enables you to find documents or data by matching keywords or phrases within the entire text content. It is widely used in search engines, document management, e-commerce, and any scenario where users need to search large volumes of unstructured or semi-structured text.

TiDB provides full-text search capabilities for **massive datasets** with high performance and built-in **multilingual support**.

!!! note

    Full-text search is currently in the early stages with limited accessibility. It is only available for **TiDB Cloud Starter** in the following regions:
    
    - **Frankfurt (eu-central-1)**
    - **Singapore (ap-southeast-1)**
  
    If you have feedback or need help, feel free to reach out to us on [Discord](https://discord.gg/zcqexutz2R).

!!! tip

    For a complete example of full-text search, see the [E-commerce product search demo](../examples/fulltext-search-with-pytidb.md).

## Basic Usage

### Step 1. Create Table and Full-text Index

=== "Python"

    You can use `FullTextField` to define a text field with full-text search enabled. The `fts_parser` parameter in Python corresponds to the `WITH PARSER` clause in SQL.

    For example, the following code creates a table with a full-text index on the `title` column:

    ```python hl_lines="6"
    from pytidb.schema import TableModel, Field, FullTextField

    class Item(TableModel):
        __tablename__ = "items"
        id: int = Field(primary_key=True)
        title: str = FullTextField(fts_parser="MULTILINGUAL")

    table = client.create_table(schema=Item, if_exists="overwrite")
    ```

    The `fts_parser` parameter specifies the parser for the full-text index. Supported values:
    
    - `STANDARD`: Fast, works for English content, splits words by spaces and punctuation.
    - `MULTILINGUAL` (default): Supports multiple languages, including English, Chinese, Japanese, and Korean.

=== "SQL"

    Create a table with a full-text index:

    ```sql hl_lines="4"
    CREATE TABLE items(
        id INT PRIMARY KEY,
        title TEXT,
        FULLTEXT INDEX (title) WITH PARSER MULTILINGUAL
    );
    ```

    You can also add a full-text index to an existing table with a separate statement:

    ```sql
    CREATE TABLE items(
        id INT PRIMARY KEY,
        title TEXT
    );

    ALTER TABLE items ADD FULLTEXT INDEX (title)
    WITH PARSER MULTILINGUAL ADD_COLUMNAR_REPLICA_ON_DEMAND;
    ```

    The following parsers are supported in the `WITH PARSER <PARSER_NAME>` clause:

    - `STANDARD`: Fast, works for English content, splits words by spaces and punctuation.
    - `MULTILINGUAL`: Supports multiple languages, including English, Chinese, Japanese, and Korean.

### Step 2. Insert Sample Data

For demonstration purposes, the following sample data covers English, Japanese, and Chinese text.

=== "Python"

    You can use the `bulk_insert` method to insert sample data into the table.

    ```python
    table.bulk_insert([
        Item(id=1, title="Bluetooth Earphones, HiFi sound, 48h battery, Fast charge, Low latency"),
        Item(id=2, title="Bluetooth 5.3 Headphones, Noise Cancelling, Immersive sound, Comfortable"),
        Item(id=3, title="IPX7 Waterproof Earbuds, Sport ready, Touch control, High-quality music"),
        Item(id=4, title="Sports Earbuds, Secure fit, Sweatproof, Long battery, Workout support"),
        Item(id=5, title="Wired Headphones, Studio-grade, HD sound, Comfortable, Pro music experience"),
        Item(id=6, title="Bluetoothイヤホン HiFi音質 48hバッテリー 急速充電 低遅延"),
        Item(id=7, title="Bluetooth5.3ヘッドホン ノイズキャンセリング 没入サウンド 快適装着"),
        Item(id=8, title="IPX7防水イヤホン スポーツ対応 タッチ操作 高音質音楽"),
        Item(id=9, title="スポーツイヤホン 安定装着 防汗 長持ちバッテリー ワークアウト対応"),
        Item(id=10, title="有線ヘッドホン スタジオ級 HDサウンド 快適装着 プロ音楽体験"),
        Item(id=11, title="无线蓝牙耳机 HiFi音质 48小时超长续航 快速充电 低延迟"),
        Item(id=12, title="蓝牙5.3降噪头戴式耳机 杜比全景声 沉浸音效 舒适佩戴 畅享静谧音乐时光"),
        Item(id=13, title="IPX7防水真无线耳机 运动无忧 智能触控 随时畅听高品质音乐"),
        Item(id=14, title="运动专用耳机 稳固佩戴 防汗设计 超长续航 低延迟音频 高清通话"),
        Item(id=15, title="录音室级有线耳机 高清音质 舒适佩戴 可拆卸线材 多设备兼容 降噪麦克风"),
    ])
    ```

=== "SQL"

    You can use the `INSERT INTO` statement to insert the sample data into the table.

    ```sql
    INSERT INTO items (id, title) VALUES
        (1, 'Bluetooth Earphones, HiFi sound, 48h battery, Fast charge, Low latency'),
        (2, 'Bluetooth 5.3 Headphones, Noise Cancelling, Immersive sound, Comfortable'),
        (3, 'IPX7 Waterproof Earbuds, Sport ready, Touch control, High-quality music'),
        (4, 'Sports Earbuds, Secure fit, Sweatproof, Long battery, Workout support'),
        (5, 'Wired Headphones, Studio-grade, HD sound, Comfortable, Pro music experience'),
        (6, 'Bluetoothイヤホン HiFi音質 48hバッテリー 急速充電 低遅延'),
        (7, 'Bluetooth5.3ヘッドホン ノイズキャンセリング 没入サウンド 快適装着'),
        (8, 'IPX7防水イヤホン スポーツ対応 タッチ操作 高音質音楽'),
        (9, 'スポーツイヤホン 安定装着 防汗 長持ちバッテリー ワークアウト対応'),
        (10, '有线ヘッドホン スタジオ级 HDサウンド 快适装着 プロ音楽体験'),
        (11, '无线蓝牙耳机 HiFi音质 48小时超长续航 快速充电 低延迟'),
        (12, '蓝牙5.3降噪头戴式耳机 杜比全景声 沉浸音效 舒适佩戴 畅享静谧音乐时光'),
        (13, 'IPX7防水真无线耳机 运动无忧 智能触控 随时畅听高品质音乐'),
        (14, '运动专用耳机 稳固佩戴 防汗设计 超长续航 低延迟音频 高清通话'),
        (15, '录音室级有线耳机 高清音质 舒适佩戴 可拆卸线材 多设备兼容 降噪麦克风');
    ```

### Step 3. Perform a Full-text Search

=== "Python"

    To perform a full-text search with pytidb, use the `search` method and set the `search_type` parameter to `"fulltext"`.

    **Example: Search for the 3 most relevant documents**

    ```python
    results = table.search("Bluetooth Headphones", search_type="fulltext").limit(3).to_list()
    print(json.dumps(results, indent=2, ensure_ascii=False))
    ```

    ```python title="Execution result"
    [
        {
            "id": 2,
            "title": "Bluetooth 5.3 Headphones, Noise Cancelling, Immersive sound, Comfortable",
            "_match_score": 3.7390857,
            "_score": 3.7390857
        },
        {
            "id": 5,
            "title": "Wired Headphones, Studio-grade, HD sound, Comfortable, Pro music experience",
            "_match_score": 1.9798478,
            "_score": 1.9798478
        },
        {
            "id": 1,
            "title": "Bluetooth Earphones, HiFi sound, 48h battery, Fast charge, Low latency",
            "_match_score": 1.620981,
            "_score": 1.620981
        }
    ]
    ```

    The results are sorted by relevance, with the most relevant documents listed first.

    The `_match_score` (or `_score`) field indicates the relevance score of each document, calculated using the [BM25](https://en.wikipedia.org/wiki/Okapi_BM25) algorithm—a widely used ranking function in information retrieval.

    **Example: Search for the 3 most relevant documents in another language**

    ```python
    results = table.search("蓝牙耳机", search_type="fulltext").limit(3).to_list()
    print(json.dumps(results, indent=2, ensure_ascii=False))
    ```

    ```python title="Execution result"
    [
        {
            "id": 11,
            "title": "无线蓝牙耳机 HiFi音质 48小时超长续航 快速充电 低延迟",
            "_match_score": 3.000002,
            "_score": 3.000002
        },
        {
            "id": 12,
            "title": "蓝牙5.3降噪头戴式耳机 杜比全景声 沉浸音效 舒适佩戴 畅享静谧音乐时光",
            "_match_score": 2.5719738,
            "_score": 2.5719738
        },
        {
            "id": 14,
            "title": "运动专用耳机 稳固佩戴 防汗设计 超长续航 低延迟音频 高清通话",
            "_match_score": 1.1418362,
            "_score": 1.1418362
        }
    ]
    ```

=== "SQL"

    To perform a full-text search, use the `fts_match_word()` function.

    **Example: Search for the 3 most relevant documents**

    ```sql
    SELECT *, fts_match_word("Bluetooth Headphones", title) AS score
    FROM items
    WHERE fts_match_word("Bluetooth Headphones", title)
    ORDER BY score DESC
    LIMIT 3;
    ```

    ```plain title="Execution result"
    +----+-----------------------------------------------------------------------------+-----------+
    | id | title                                                                       | score     |
    +----+-----------------------------------------------------------------------------+-----------+
    |  2 | Bluetooth 5.3 Headphones, Noise Cancelling, Immersive sound, Comfortable    | 3.7390857 |
    |  5 | Wired Headphones, Studio-grade, HD sound, Comfortable, Pro music experience | 1.9798478 |
    |  1 | Bluetooth Earphones, HiFi sound, 48h battery, Fast charge, Low latency      |  1.620981 |
    +----+-----------------------------------------------------------------------------+-----------+
    ```

    The results are ordered by relevance, with the most relevant documents first.

    **Example: Search for the 3 most relevant documents in another language**

    ```sql
    SELECT *, fts_match_word("蓝牙耳机", title) AS score
    FROM items
    WHERE fts_match_word("蓝牙耳机", title)
    ORDER BY score DESC
    LIMIT 3;
    ```

    ```plain title="Execution result"
    +----+------------------------------------------------------------------+-----------+
    | id | title                                                            | score     |
    +----+------------------------------------------------------------------+-----------+
    | 11 | 无线蓝牙耳机 HiFi音质 48小时超长续航 快速充电 低延迟                    |  3.000002 |
    | 12 | 蓝牙5.3降噪头戴式耳机 杜比全景声 沉浸音效 舒适佩戴 畅享静谧音乐时光        | 2.5719738 |
    | 14 | 运动专用耳机 稳固佩戴 防汗设计 超长续航 低延迟音频 高清通话               | 1.1418362 |
    +----+------------------------------------------------------------------+-----------+
    ```

## See Also

In Retrieval-Augmented Generation (RAG) scenarios, it is often beneficial to utilize both full-text search and vector search for optimal results.

- Learn how to combine these approaches in the [hybrid search guide](./hybrid-search.md).
- For more on vector search, see the [vector search guide](../concepts/vector-search.md).