---
title: TiDB Data Type
summary: Learn about the JSON data type in TiDB.
---

# JSONタイプ {#json-type}

TiDB は、半構造化データの保存に役立つ`JSON` (JavaScript Object Notation) データ型をサポートしています。 `JSON`データ型には、文字列列に`JSON`形式の文字列を格納する場合に比べて次の利点があります。

-   シリアル化にはバイナリ形式を使用します。内部形式により、 `JSON`文書要素への素早い読み取りアクセスが可能になります。
-   `JSON`列に保存された JSON ドキュメントの自動検証。有効な文書のみを保管できます。

`JSON`列は、他のバイナリ型の列と同様に、直接インデックス付けされませんが、生成された列の形式で`JSON`ドキュメント内のフィールドにインデックスを付けることができます。

```sql
CREATE TABLE city (
    id INT PRIMARY KEY,
    detail JSON,
    population INT AS (JSON_EXTRACT(detail, '$.population')),
    index index_name (population)
    );
INSERT INTO city (id,detail) VALUES (1, '{"name": "Beijing", "population": 100}');
SELECT id FROM city WHERE population >= 100;
```

詳細については、 [JSON関数](/functions-and-operators/json-functions.md)および[生成された列](/generated-columns.md)を参照してください。

## 制限 {#restrictions}

-   現在、TiDB は、限られた`JSON`関数のTiFlashへのプッシュダウンのみをサポートしています。詳細については、 [プッシュダウン式](/tiflash/tiflash-supported-pushdown-calculations.md#push-down-expressions)を参照してください。
-   v6.3.0 より前の TiDB バックアップ &amp; リストア (BR) バージョンは、JSON 列を含むデータのリカバリをサポートしていません。 BRのどのバージョンも、JSON 列を含むデータを v6.3.0 より前の TiDB クラスターにリカバリすることをサポートしていません。
-   `DATE` 、 `DATETIME` 、 `TIME`などの非標準の`JSON`データ型を含むデータをレプリケートするためにレプリケーション ツールを使用しないでください。

## MySQLの互換性 {#mysql-compatibility}

-   `BINARY`タイプのデータを含む JSON カラムを作成すると、現在、MySQL はデータを`STRING`タイプとして誤ってラベル付けしますが、TiDB はデータを`BINARY`タイプとして正しく処理します。

    ```sql
    CREATE TABLE test(a json);
    INSERT INTO test SELECT json_objectagg('a', b'01010101');

    -- In TiDB, executing the following SQL statement returns `0, 0`. In MySQL, executing the following SQL statement returns `0, 1`.
    mysql> SELECT JSON_EXTRACT(JSON_OBJECT('a', b'01010101'), '$.a') = "base64:type15:VQ==" AS r1, JSON_EXTRACT(a, '$.a') = "base64:type15:VQ==" AS r2 FROM test;
    +------+------+
    | r1   | r2   |
    +------+------+
    |    0 |    0 |
    +------+------+
    1 row in set (0.01 sec)
    ```

    詳細については、問題[#37443](https://github.com/pingcap/tidb/issues/37443)を参照してください。

-   データ型を`ENUM`または`SET`から`JSON`に変換するときに、TiDB はデータ形式の正しさをチェックします。たとえば、TiDB で次の SQL ステートメントを実行すると、エラーが返されます。

    ```sql
    CREATE TABLE t(e ENUM('a'));
    INSERT INTO t VALUES ('a');
    mysql> SELECT CAST(e AS JSON) FROM t;
    ERROR 3140 (22032): Invalid JSON text: The document root must not be followed by other values.
    ```

    詳細については、問題[#9999](https://github.com/pingcap/tidb/issues/9999)を参照してください。

-   TiDB では、 `ORDER BY`を使用して JSON 配列または JSON オブジェクトを並べ替えることができます。

    MySQL では、 `ORDER BY`を使用して JSON 配列または JSON オブジェクトをソートすると、MySQL は警告を返し、ソート結果は比較演算の結果と一致しません。

    ```sql
    CREATE TABLE t(j JSON);
    INSERT INTO t VALUES ('[1,2,3,4]');
    INSERT INTO t VALUES ('[5]');

    mysql> SELECT j FROM t WHERE j < JSON_ARRAY(5);
    +--------------+
    | j            |
    +--------------+
    | [1, 2, 3, 4] |
    +--------------+
    1 row in set (0.00 sec)

    -- In TiDB, executing the following SQL statement returns the correct sorting result. In MySQL, executing the following SQL statement returns the "This version of MySQL doesn't yet support 'sorting of non-scalar JSON values'." warning and the sorting result is inconsistent with the comparison result of `<`.
    mysql> SELECT j FROM t ORDER BY j;
    +--------------+
    | j            |
    +--------------+
    | [1, 2, 3, 4] |
    | [5]          |
    +--------------+
    2 rows in set (0.00 sec)
    ```

    詳細については、問題[#37506](https://github.com/pingcap/tidb/issues/37506)を参照してください。

-   データを JSON 列に挿入すると、TiDB はデータの値を暗黙的に`JSON`型に変換します。

    ```sql
    CREATE TABLE t(col JSON);

    -- In TiDB, the following INSERT statement is executed successfully. In MySQL, executing the following INSERT statement returns the "Invalid JSON text" error.
    INSERT INTO t VALUES (3);
    ```

`JSON`データ型の詳細については、 [JSON関数](/functions-and-operators/json-functions.md)および[生成された列](/generated-columns.md)を参照してください。
