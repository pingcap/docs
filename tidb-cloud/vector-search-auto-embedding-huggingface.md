---
title: HuggingFace Embeddings
summary: TiDB Cloudで HuggingFace 埋め込みモデルを使用する方法を学びます。
---

# ハギングフェイス埋め込み {#huggingface-embeddings}

このドキュメントでは、TiDB Cloudの[自動埋め込み](/tidb-cloud/vector-search-auto-embedding-overview.md)で HuggingFace 埋め込みモデルを使用して、テキスト クエリからセマンティック検索を実行する方法について説明します。

> **注記：**
>
> [自動埋め込み](/tidb-cloud/vector-search-auto-embedding-overview.md)は、AWS でホストされているTiDB Cloud Starter クラスターでのみ使用できます。

## 利用可能なモデル {#available-models}

独自の[HuggingFace推論API](https://huggingface.co/docs/inference-providers/index)キー (BYOK) をお持ちの場合は、HuggingFace モデルを`huggingface/`プレフィックスで使用できます。

以下のセクションでは、便宜上、いくつかの一般的なモデルを例として取り上げ、それらを自動埋め込みでどのように使用するかを説明します。利用可能なモデルの完全なリストについては、 [ハギングフェイスモデル](https://huggingface.co/models?library=sentence-transformers&#x26;inference_provider=hf-inference&#x26;sort=trending)参照してください。すべてのモデルがHuggingFace推論APIで提供されているわけではなく、常に動作するわけでもないことに注意してください。

## 多言語-e5-ラージ {#multilingual-e5-large}

-   名前: `huggingface/intfloat/multilingual-e5-large`
-   寸法: 1024
-   距離計量：コサイン、L2
-   価格: HuggingFaceによる請求
-   TiDB Cloudがホスト: ❌
-   鍵をご持参ください: ✅
-   プロジェクトホーム: [https://huggingface.co/intfloat/multilingual-e5-large](https://huggingface.co/intfloat/multilingual-e5-large)

例：

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_HUGGINGFACE_API_KEY = 'your-huggingface-api-key-here';

CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(1024) GENERATED ALWAYS AS (EMBED_TEXT(
                "huggingface/intfloat/multilingual-e5-large",
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

## bge-m3 {#bge-m3}

-   名前: `huggingface/BAAI/bge-m3`
-   寸法: 1024
-   距離計量：コサイン、L2
-   価格: HuggingFaceによる請求
-   TiDB Cloudがホスト: ❌
-   鍵をご持参ください: ✅
-   プロジェクトホーム: [https://huggingface.co/BAAI/bge-m3](https://huggingface.co/BAAI/bge-m3)

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_HUGGINGFACE_API_KEY = 'your-huggingface-api-key-here';

CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(1024) GENERATED ALWAYS AS (EMBED_TEXT(
                "huggingface/BAAI/bge-m3",
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

## オールミニLM-L6-v2 {#all-minilm-l6-v2}

-   名前: `huggingface/sentence-transformers/all-MiniLM-L6-v2`
-   寸法: 384
-   距離計量：コサイン、L2
-   価格: HuggingFaceによる請求
-   TiDB Cloudがホスト: ❌
-   鍵をご持参ください: ✅
-   プロジェクトホーム: [https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)

例：

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_HUGGINGFACE_API_KEY = 'your-huggingface-api-key-here';

CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(384) GENERATED ALWAYS AS (EMBED_TEXT(
                "huggingface/sentence-transformers/all-MiniLM-L6-v2",
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

## all-mpnet-base-v2 {#all-mpnet-base-v2}

-   名前: `huggingface/sentence-transformers/all-mpnet-base-v2`
-   寸法: 768
-   距離計量：コサイン、L2
-   価格: HuggingFaceによる請求
-   TiDB Cloudがホスト: ❌
-   鍵をご持参ください: ✅
-   プロジェクトホーム: [https://huggingface.co/sentence-transformers/all-mpnet-base-v2](https://huggingface.co/sentence-transformers/all-mpnet-base-v2)

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_HUGGINGFACE_API_KEY = 'your-huggingface-api-key-here';

CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(768) GENERATED ALWAYS AS (EMBED_TEXT(
                "huggingface/sentence-transformers/all-mpnet-base-v2",
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

## Qwen3-埋め込み-0.6B {#qwen3-embedding-0-6b}

> **注記：**
>
> HuggingFace Inference API はこのモデルでは安定していない可能性があります。

-   名前: `huggingface/Qwen/Qwen3-Embedding-0.6B`
-   寸法: 1024
-   距離計量：コサイン、L2
-   最大入力テキストトークン数: 512
-   価格: HuggingFaceによる請求
-   TiDB Cloudがホスト: ❌
-   鍵をご持参ください: ✅
-   プロジェクトホーム: [https://huggingface.co/Qwen/Qwen3-Embedding-0.6B](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B)

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_HUGGINGFACE_API_KEY = 'your-huggingface-api-key-here';

CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(1024) GENERATED ALWAYS AS (EMBED_TEXT(
                "huggingface/Qwen/Qwen3-Embedding-0.6B",
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

## Pythonの使用例 {#python-usage-example}

[PyTiDB ドキュメント](https://pingcap.github.io/ai/guides/auto-embedding/)参照。

## 参照 {#see-also}

-   [自動埋め込みの概要](/tidb-cloud/vector-search-auto-embedding-overview.md)
-   [ベクトル検索](/vector-search/vector-search-overview.md)
-   [ベクトル関数と演算子](/vector-search/vector-search-functions-and-operators.md)
-   [ハイブリッド検索](/tidb-cloud/vector-search-hybrid-search.md)
