---
title: TiDB Data Type
summary: Learn about the JSON data type in TiDB.
---

# JSON タイプ {#json-type}

> **警告：**
>
> これはまだ実験的機能です。本番環境で使用することはお勧めし**ません**。

TiDB は、半構造化データの格納に役立つ`JSON` (JavaScript Object Notation) データ型をサポートしています。 `JSON`データ型には、文字列列に`JSON`形式の文字列を格納する場合と比較して、次の利点があります。

-   シリアル化には Binary 形式を使用します。内部フォーマットにより、 `JSON`のドキュメント要素への迅速な読み取りアクセスが可能になります。
-   `JSON`列に格納された JSON ドキュメントの自動検証。有効なドキュメントのみを保存できます。

`JSON`列は、他のバイナリ型の列と同様に直接インデックス付けされませんが、生成された列の形式で`JSON`ドキュメントのフィールドにインデックスを付けることができます。

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

詳細については、 [JSON 関数](/functions-and-operators/json-functions.md)および[生成された列](/generated-columns.md)を参照してください。
