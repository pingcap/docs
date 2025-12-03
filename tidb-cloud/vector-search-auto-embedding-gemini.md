---
title: Gemini Embeddings
summary: TiDB Cloudで Google Gemini 埋め込みモデルを使用する方法を学びます。
---

# ジェミニ埋め込み {#gemini-embeddings}

このドキュメントでは、 TiDB Cloudの[自動埋め込み](/tidb-cloud/vector-search-auto-embedding-overview.md)で Gemini 埋め込みモデルを使用して、テキスト クエリからセマンティック検索を実行する方法について説明します。

> **注記：**
>
> [自動埋め込み](/tidb-cloud/vector-search-auto-embedding-overview.md)は、AWS でホストされているTiDB Cloud Starter クラスターでのみ使用できます。

## 利用可能なモデル {#available-models}

ご自身のGemini APIキー（BYOK）をお持ちいただければ、すべてのGeminiモデルを`gemini/`プレフィックスでご利用いただけます。例：

**ジェミニ埋め込み-001**

-   名前: `gemini/gemini-embedding-001`
-   寸法: 128～3072 (デフォルト: 3072)
-   距離計量：コサイン、L2
-   最大入力テキストトークン数: 2,048
-   価格: Google が請求
-   TiDB Cloudがホスト: ❌
-   鍵をご持参ください: ✅

利用可能なモデルの完全なリストについては、 [Gemini ドキュメント](https://ai.google.dev/gemini-api/docs/embeddings)参照してください。

## SQLの使用例 {#sql-usage-example}

Gemini モデルを使用するには、次のように[Gemini APIキー](https://ai.google.dev/gemini-api/docs/api-key)指定する必要があります。

> **注記：**
>
> `'your-gemini-api-key-here'`実際の Gemini API キーに置き換えます。

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_GEMINI_API_KEY = 'your-gemini-api-key-here';

CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(3072) GENERATED ALWAYS AS (EMBED_TEXT(
                "gemini/gemini-embedding-001",
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

[ジェミニオプション](https://ai.google.dev/gemini-api/docs/embeddings)すべて、 `EMBED_TEXT()`関数の`additional_json_options`パラメータを介してサポートされます。

**例: 品質を向上させるためにタスクの種類を指定する**

```sql
CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(1024) GENERATED ALWAYS AS (EMBED_TEXT(
                "gemini/gemini-embedding-001",
                `content`,
                '{"task_type": "SEMANTIC_SIMILARITY"}'
              )) STORED
);
```

**例: 代替ディメンションを使用する**

```sql
CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(768) GENERATED ALWAYS AS (EMBED_TEXT(
                "gemini/gemini-embedding-001",
                `content`,
                '{"output_dimensionality": 768}'
              )) STORED
);
```

利用可能なすべてのオプションについては、 [Gemini ドキュメント](https://ai.google.dev/gemini-api/docs/embeddings)参照してください。

## Pythonの使用例 {#python-usage-example}

[PyTiDB ドキュメント](https://pingcap.github.io/ai/guides/auto-embedding/)参照。

## 参照 {#see-also}

-   [自動埋め込みの概要](/tidb-cloud/vector-search-auto-embedding-overview.md)
-   [ベクトル検索](/vector-search/vector-search-overview.md)
-   [ベクトル関数と演算子](/vector-search/vector-search-functions-and-operators.md)
-   [ハイブリッド検索](/tidb-cloud/vector-search-hybrid-search.md)
