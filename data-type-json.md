---
title: TiDB Data Type
summary: TiDB の JSON データ型について学習します。
---

# JSON データ型 {#json-data-type}

TiDB は、半構造化データを格納するのに役立つ`JSON` (JavaScript Object Notation) データ型をサポートしています。 `JSON`データ型には、文字列列に`JSON`形式の文字列を格納する場合と比べて、次の利点があります。

-   シリアル化にはバイナリ形式を使用します。内部形式により、 `JSON`ドキュメント要素への迅速な読み取りアクセスが可能になります。
-   `JSON`列に保存された JSON ドキュメントの自動検証。有効なドキュメントのみを保存できます。

`JSON`列は、他のバイナリ タイプの列と同様に直接インデックス付けされませんが、生成された列の形式で`JSON`ドキュメント内のフィールドをインデックス付けできます。

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

詳細については[JSON関数](/functions-and-operators/json-functions.md)および[生成された列](/generated-columns.md)参照してください。

## JSON 値型 {#json-value-types}

JSON ドキュメント内の値には型があります。これは[`JSON_TYPE`](/functions-and-operators/json-functions/json-functions-return.md#json_type)の出力に表示されます。

| タイプ    | 例                              |
| ------ | ------------------------------ |
| 配列     | `[]`                           |
| 少し     |                                |
| ブロブ    | `0x616263`                     |
| ブール    | `true`                         |
| 日付     | `"2025-06-14"`                 |
| 日時     | `"2025-06-14 09:05:10.000000"` |
| ダブル    | `1.14`                         |
| 整数     | `5`                            |
| NULL   | `null`                         |
| 物体     | `{}`                           |
| 不透明    |                                |
| 弦      | `"foobar"`                     |
| 時間     | `"09:10:00.000000"`            |
| 符号なし整数 | `9223372036854776000`          |

## 制限 {#restrictions}

-   現在、 TiDB はTiFlashへの限定された`JSON`関数のプッシュダウンのみをサポートしています。詳細については、 [プッシュダウン式](/tiflash/tiflash-supported-pushdown-calculations.md#push-down-expressions)参照してください。
-   TiDB バックアップ &amp; リストア (BR) は、v6.3.0 で JSON 列データのエンコード方法を変更します。したがって、 BRを使用して JSON 列を含むデータを v6.3.0 より前の TiDB クラスターにリストアすることはお勧めしません。
-   `DATE` 、 `DATETIME` 、 `TIME`などの非標準`JSON`データ型を含むデータをレプリケートする場合は、レプリケーション ツールを使用しないでください。

## MySQL 互換性 {#mysql-compatibility}

-   `BINARY`型のデータを含む JSON 列を作成すると、MySQL は現在そのデータを`STRING`型として誤ってラベル付けしますが、TiDB はそれを`BINARY`型として正しく処理します。

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

    詳細については、第[＃37443](https://github.com/pingcap/tidb/issues/37443)号を参照してください。

-   データ型を`ENUM`または`SET`から`JSON`に変換する場合、TiDB はデータ形式の正確性をチェックします。たとえば、TiDB で次の SQL ステートメントを実行すると、エラーが返されます。

    ```sql
    CREATE TABLE t(e ENUM('a'));
    INSERT INTO t VALUES ('a');
    mysql> SELECT CAST(e AS JSON) FROM t;
    ERROR 3140 (22032): Invalid JSON text: The document root must not be followed by other values.
    ```

    詳細については、第[＃9999](https://github.com/pingcap/tidb/issues/9999)号を参照してください。

-   TiDB では、 `ORDER BY`使用して JSON 配列または JSON オブジェクトをソートできます。

    MySQL では、 `ORDER BY`使用して JSON 配列または JSON オブジェクトをソートすると、MySQL から警告が返され、ソート結果が比較演算の結果と一致しなくなります。

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

    詳細については、第[＃37506](https://github.com/pingcap/tidb/issues/37506)号を参照してください。

-   JSON 列にデータを挿入すると、TiDB は暗黙的にデータの値を`JSON`型に変換します。

    ```sql
    CREATE TABLE t(col JSON);

    -- In TiDB, the following INSERT statement is executed successfully. In MySQL, executing the following INSERT statement returns the "Invalid JSON text" error.
    INSERT INTO t VALUES (3);
    ```

`JSON`データ型の詳細については、 [JSON関数](/functions-and-operators/json-functions.md)および[生成された列](/generated-columns.md)参照してください。
