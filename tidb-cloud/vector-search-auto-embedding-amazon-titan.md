---
title: Amazon Titan Embeddings
summary: TiDB Cloudで Amazon Titan 埋め込みモデルを使用する方法を学びます。
---

# Amazon Titan 埋め込み {#amazon-titan-embeddings}

このドキュメントでは、TiDB Cloudの[自動埋め込み](/tidb-cloud/vector-search-auto-embedding-overview.md)で Amazon Titan 埋め込みモデルを使用して、テキストクエリからセマンティック検索を実行する方法について説明します。

> **注記：**
>
> 現在、 [自動埋め込み](/tidb-cloud/vector-search-auto-embedding-overview.md)次の AWS リージョンのTiDB Cloud Starter クラスターでのみ利用可能です。
>
> -   `Frankfurt (eu-central-1)`
> -   `Oregon (us-west-2)`
> -   `N. Virginia (us-east-1)`

## 利用可能なモデル {#available-models}

TiDB Cloud は以下の[Amazon Titan 埋め込みモデル](https://docs.aws.amazon.com/bedrock/latest/userguide/titan-embedding-models.html)をネイティブに提供します。API キーは必要ありません。

**Amazon Titan テキスト埋め込み V2 モデル**

-   名前: `tidbcloud_free/amazon/titan-embed-text-v2`
-   寸法: 1024 (デフォルト)、512、256
-   距離メトリック: コサイン、L2
-   言語: 英語 (プレビューでは 100 以上の言語に対応)
-   一般的な使用例: RAG、ドキュメント検索、再ランク付け、分類
-   最大入力テキストトークン数: 8,192
-   最大入力テキスト文字数: 50,000
-   価格: 無料
-   TiDB Cloudがホスト: ✅
-   自分の鍵を持参: ❌

このモデルの詳細については、 [Amazon Bedrock ドキュメント](https://docs.aws.amazon.com/bedrock/latest/userguide/titan-embedding-models.html)参照してください。

## SQLの使用例 {#sql-usage-example}

次の例は、Auto Embedding で Amazon Titan 埋め込みモデルを使用する方法を示しています。

```sql
CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(1024) GENERATED ALWAYS AS (EMBED_TEXT(
                "tidbcloud_free/amazon/titan-embed-text-v2",
                `content`
              )) STORED
);


INSERT INTO sample
    (`id`, `content`)
VALUES
    (1, "Java: Object-oriented language for cross-platform development."),
    (2, "Java coffee: Bold Indonesian beans with low acidity."),
    (3, "Java island: Densely populated, home to Jakarta."),
    (4, "Java's syntax is used in Android apps."),
    (5, "Dark roast Java beans enhance espresso blends.");


SELECT `id`, `content` FROM sample
ORDER BY
  VEC_EMBED_COSINE_DISTANCE(
    embedding,
    "How to start learning Java programming?"
  )
LIMIT 2;
```

結果：

    +------+----------------------------------------------------------------+
    | id   | content                                                        |
    +------+----------------------------------------------------------------+
    |    1 | Java: Object-oriented language for cross-platform development. |
    |    4 | Java's syntax is used in Android apps.                         |
    +------+----------------------------------------------------------------+

## オプション {#options}

`EMBED_TEXT()`関数の`additional_json_options`パラメータを介して次のオプションを指定できます。

-   `normalize` (オプション): 出力埋め込みを正規化するかどうか。デフォルトは`true`です。
-   `dimensions` （オプション）：出力埋め込みの次元数。サポートされる値： `1024` （デフォルト）、 `512` 、 `256` 。

**例: 代替ディメンションを使用する**

```sql
CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(512) GENERATED ALWAYS AS (EMBED_TEXT(
                "tidbcloud_free/amazon/titan-embed-text-v2",
                `content`,
                '{"dimensions": 512}'
              )) STORED
);


INSERT INTO sample
    (`id`, `content`)
VALUES
    (1, "Java: Object-oriented language for cross-platform development."),
    (2, "Java coffee: Bold Indonesian beans with low acidity."),
    (3, "Java island: Densely populated, home to Jakarta."),
    (4, "Java's syntax is used in Android apps."),
    (5, "Dark roast Java beans enhance espresso blends.");


SELECT `id`, `content` FROM sample
ORDER BY
  VEC_EMBED_COSINE_DISTANCE(
    embedding,
    "How to start learning Java programming?"
  )
LIMIT 2;
```

結果：

    +------+----------------------------------------------------------------+
    | id   | content                                                        |
    +------+----------------------------------------------------------------+
    |    1 | Java: Object-oriented language for cross-platform development. |
    |    4 | Java's syntax is used in Android apps.                         |
    +------+----------------------------------------------------------------+

## Pythonの使用例 {#python-usage-example}

[PyTiDB ドキュメント](https://pingcap.github.io/ai/guides/auto-embedding/)参照。

## 参照 {#see-also}

-   [自動埋め込みの概要](/tidb-cloud/vector-search-auto-embedding-overview.md)
-   [ベクトル検索](/vector-search/vector-search-overview.md)
-   [ベクトル関数と演算子](/vector-search/vector-search-functions-and-operators.md)
-   [ハイブリッド検索](/tidb-cloud/vector-search-hybrid-search.md)
