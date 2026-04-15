---
title: Amazon Titan Embeddings
summary: TiDB CloudでAmazon Titanの埋め込みモデルを使用する方法を学びましょう。
aliases: ['/ja/tidbcloud/vector-search-auto-embedding-amazon-titan/']
---

# Amazon Titan 埋め込み {#amazon-titan-embeddings}

このドキュメントでは、Amazon Titanの埋め込みモデルをTiDB Cloudで[自動埋め込み](/ai/integrations/vector-search-auto-embedding-overview.md)に使用して、テキストクエリによるセマンティック検索を実行する方法について説明します。

> **注記：**
>
> [自動埋め込み](/ai/integrations/vector-search-auto-embedding-overview.md)、AWS でホストされているTiDB Cloud Starterインスタンスでのみ利用できます。

## 利用可能なモデル {#available-models}

TiDB Cloud は、次の[Amazon Titan埋め込みモデル](https://docs.aws.amazon.com/bedrock/latest/userguide/titan-embedding-models.html)ネイティブで提供します。 API キーは必要ありません。

**Amazon Titan テキスト埋め込み V2 モデル**

-   名前: `tidbcloud_free/amazon/titan-embed-text-v2`
-   寸法: 1024 (デフォルト)、512、256
-   距離指標：コサイン類似度、L2
-   対応言語：英語（プレビュー版では100以上の言語に対応）
-   典型的な使用例：RAG、文書検索、再ランキング、分類
-   入力可能なテキストトークンの最大数：8,192
-   入力可能なテキスト文字数：最大50,000文字
-   価格：無料
-   TiDB Cloudがホストしています: ✅
-   鍵をご持参ください：❌

このモデルの詳細については、 [Amazon Bedrock のドキュメント](https://docs.aws.amazon.com/bedrock/latest/userguide/titan-embedding-models.html)を参照してください。

## SQLの使用例 {#sql-usage-example}

以下の例は、Amazon Titan埋め込みモデルを自動埋め込みで使用する方法を示しています。

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

`additional_json_options` `EMBED_TEXT()` } パラメータを使用して、以下のオプションを指定できます。

-   `normalize` (オプション): 出力埋め込みを正規化するかどうか。デフォルトは`true`です。
-   `dimensions` (オプション): 出力埋め込みの次元数。サポートされている値: `1024` (デフォルト)、 `512` 、および`256` 。

**例：別の次元を使用する**

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

## 関連項目 {#see-also}

-   [自動埋め込みの概要](/ai/integrations/vector-search-auto-embedding-overview.md)
-   [ベクトル検索](/ai/concepts/vector-search-overview.md)
-   [ベクトル関数と演算子](/ai/reference/vector-search-functions-and-operators.md)
-   [ハイブリッド検索](/ai/guides/vector-search-hybrid-search.md)
