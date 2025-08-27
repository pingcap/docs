---
title: Jina AI Embeddings
summary: TiDB Cloudで Jina AI 埋め込みモデルを使用する方法を学びます。
---

# Jina AI 埋め込み {#jina-ai-embeddings}

このドキュメントでは、 TiDB Cloudの[自動埋め込み](/tidb-cloud/vector-search-auto-embedding-overview.md)使用した Jina AI 埋め込みモデルを使用して、テキスト クエリからセマンティック検索を実行する方法について説明します。

> **注記：**
>
> 現在、 [自動埋め込み](/tidb-cloud/vector-search-auto-embedding-overview.md)次の AWS リージョンのTiDB Cloud Starter クラスターでのみ利用可能です。
>
> -   `Frankfurt (eu-central-1)`
> -   `Oregon (us-west-2)`
> -   `N. Virginia (us-east-1)`

## 利用可能なモデル {#available-models}

ご自身のJina AI APIキー（BYOK）をお持ちいただければ、すべてのJina AIモデルを`jina_ai/`プレフィックスでご利用いただけます。例：

**jina-embeddings-v4**

-   名前: `jina_ai/jina-embeddings-v4`
-   寸法: 2048
-   距離メトリック: コサイン、L2
-   最大入力テキストトークン数: 32,768
-   価格：Jina AIによる請求
-   TiDB Cloudがホスト: ❌
-   鍵をご持参ください: ✅

**jina-embeddings-v3**

-   名前: `jina_ai/jina-embeddings-v3`
-   寸法: 1024
-   距離メトリック: コサイン、L2
-   最大入力テキストトークン数: 8,192
-   価格：Jina AIによる請求
-   TiDB Cloudがホスト: ❌
-   鍵をご持参ください: ✅

利用可能なモデルの完全なリストについては、 [Jina AI ドキュメント](https://jina.ai/embeddings/)参照してください。

## SQLの使用例 {#sql-usage-example}

Jina AI モデルを使用するには、次のように[Jina AI APIキー](https://jina.ai/)指定する必要があります。

> **注記：**
>
> `'your-jina-ai-api-key-here'`実際の Jina AI API キーに置き換えます。

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_JINA_AI_API_KEY = 'your-jina-ai-api-key-here';

CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(1024) GENERATED ALWAYS AS (EMBED_TEXT(
                "jina_ai/jina-embeddings-v4",
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

[Jina AIオプション](https://jina.ai/embeddings/)すべて、 `EMBED_TEXT()`関数の`additional_json_options`パラメータを介してサポートされます。

**例: パフォーマンス向上のため「下流タスク」を指定する**

```sql
CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(2048) GENERATED ALWAYS AS (EMBED_TEXT(
                "jina_ai/jina-embeddings-v4",
                `content`,
                '{"task": "retrieval.passage", "task@search": "retrieval.query"}'
              )) STORED
);
```

**例: 代替ディメンションを使用する**

```sql
CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(768) GENERATED ALWAYS AS (EMBED_TEXT(
                "jina_ai/jina-embeddings-v3",
                `content`,
                '{"dimensions":768}'
              )) STORED
);
```

利用可能なすべてのオプションについては、 [Jina AI ドキュメント](https://jina.ai/embeddings/)参照してください。

## Pythonの使用例 {#python-usage-example}

[PyTiDB ドキュメント](https://pingcap.github.io/ai/integrations/embedding-jinaai/)参照。

## 参照 {#see-also}

-   [自動埋め込みの概要](/tidb-cloud/vector-search-auto-embedding-overview.md)
-   [ベクトル検索](/vector-search/vector-search-overview.md)
-   [ベクトル関数と演算子](/vector-search/vector-search-functions-and-operators.md)
-   [ハイブリッド検索](/tidb-cloud/vector-search-hybrid-search.md)
