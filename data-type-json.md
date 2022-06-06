---
title: TiDB Data Type
summary: Learn about the JSON data type in TiDB.
---

# JSONタイプ {#json-type}

> **警告：**
>
> これはまだ実験的機能です。実稼働環境で使用することはお勧めし**ません**。

TiDBは、半構造化データの保存に役立つ`JSON` （JavaScript Object Notation）データ型をサポートしています。 `JSON`データ型には、 `JSON`形式の文字列を文字列列に格納するよりも次の利点があります。

-   シリアル化にはバイナリ形式を使用します。内部形式により、 `JSON`のドキュメント要素へのクイック読み取りアクセスが可能になります。
-   `JSON`列に保存されたJSONドキュメントの自動検証。有効なドキュメントのみを保存できます。

他のバイナリタイプの列と同様に、 `JSON`列は直接インデックス付けされませんが、生成された列の形式で`JSON`ドキュメントのフィールドにインデックスを付けることができます。

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
