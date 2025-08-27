---
title: NVIDIA NIM Embeddings
summary: TiDB Cloudで NVIDIA NIM 埋め込みモデルを使用する方法を学びます。
---

# NVIDIA NIM 埋め込み {#nvidia-nim-embeddings}

このドキュメントでは、TiDB Cloudの[自動埋め込み](/tidb-cloud/vector-search-auto-embedding-overview.md)で NVIDIA NIM 埋め込みモデルを使用して、テキスト クエリからセマンティック検索を実行する方法について説明します。

> **注記：**
>
> 現在、 [自動埋め込み](/tidb-cloud/vector-search-auto-embedding-overview.md)次の AWS リージョンのTiDB Cloud Starter クラスターでのみ利用可能です。
>
> -   `Frankfurt (eu-central-1)`
> -   `Oregon (us-west-2)`
> -   `N. Virginia (us-east-1)`

## 利用可能なモデル {#available-models}

NVIDIA NIM でホストされている埋め込みモデルは、独自の[NVIDIA NIM APIキー](https://build.nvidia.com/settings/api-keys) (BYOK) を持ち込む場合、プレフィックス`nvidia_nim/`で使用できます。

以下のセクションでは、便宜上、一般的なモデルを例に挙げ、自動埋め込みでの使用方法を説明します。利用可能なモデルの完全なリストについては、 [NVIDIA NIM テキスト埋め込みモデル](https://build.nvidia.com/models?filters=usecase%3Ausecase_text_to_embedding)参照してください。

## bge-m3 {#bge-m3}

-   名前: `nvidia_nim/baai/bge-m3`
-   寸法: 1024
-   距離メトリック: コサイン、L2
-   最大入力テキストトークン数: 8,192
-   価格: NVIDIA が請求
-   TiDB Cloudがホスト: ❌
-   鍵をご持参ください: ✅
-   ドキュメント: [https://docs.api.nvidia.com/nim/reference/baai-bge-m3](https://docs.api.nvidia.com/nim/reference/baai-bge-m3)

例：

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_NVIDIA_NIM_API_KEY = 'your-nvidia-nim-api-key-here';

CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(1024) GENERATED ALWAYS AS (EMBED_TEXT(
                "nvidia_nim/baai/bge-m3",
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

## Pythonの使用例 {#python-usage-example}

[PyTiDB ドキュメント](https://pingcap.github.io/ai/guides/auto-embedding/)参照。

## 参照 {#see-also}

-   [自動埋め込みの概要](/tidb-cloud/vector-search-auto-embedding-overview.md)
-   [ベクトル検索](/vector-search/vector-search-overview.md)
-   [ベクトル関数と演算子](/vector-search/vector-search-functions-and-operators.md)
-   [ハイブリッド検索](/tidb-cloud/vector-search-hybrid-search.md)
