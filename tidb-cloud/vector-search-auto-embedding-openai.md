---
title: OpenAI Embeddings
summary: TiDB Cloudで OpenAI 埋め込みモデルを使用する方法を学びます。
---

# OpenAI 埋め込み {#openai-embeddings}

このドキュメントでは、 TiDB Cloudの[自動埋め込み](/tidb-cloud/vector-search-auto-embedding-overview.md)で OpenAI 埋め込みモデルを使用して、テキスト クエリからセマンティック検索を実行する方法について説明します。

> **注記：**
>
> [自動埋め込み](/tidb-cloud/vector-search-auto-embedding-overview.md)は、AWS でホストされているTiDB Cloud Starter クラスターでのみ使用できます。

## 利用可能なモデル {#available-models}

ご自身のOpenAI APIキー（BYOK）をお持ちいただく場合、すべてのOpenAIモデルは`openai/`プレフィックスでご利用いただけます。例：

**テキスト埋め込み 3 小**

-   名前: `openai/text-embedding-3-small`
-   寸法: 512-1536 (デフォルト: 1536)
-   距離計量：コサイン、L2
-   価格: OpenAIによる請求
-   TiDB Cloudがホスト: ❌
-   鍵をご持参ください: ✅

**テキスト埋め込み 3 大きい**

-   名前: `openai/text-embedding-3-large`
-   寸法: 256-3072 (デフォルト: 3072)
-   距離計量：コサイン、L2
-   価格: OpenAIによる請求
-   TiDB Cloudがホスト: ❌
-   鍵をご持参ください: ✅

利用可能なモデルの完全なリストについては、 [OpenAIドキュメント](https://platform.openai.com/docs/guides/embeddings)参照してください。

## SQLの使用例 {#sql-usage-example}

OpenAI モデルを使用するには、次のように[OpenAI APIキー](https://platform.openai.com/api-keys)指定する必要があります。

> **注記：**
>
> `'your-openai-api-key-here'`実際の OpenAI API キーに置き換えます。

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_OPENAI_API_KEY = 'your-openai-api-key-here';

CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(3072) GENERATED ALWAYS AS (EMBED_TEXT(
                "openai/text-embedding-3-large",
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

## Azure OpenAI を使用する {#use-azure-openai}

AzureでOpenAI埋め込みモデルを使用するには、グローバル変数`TIDB_EXP_EMBED_OPENAI_API_BASE` AzureリソースのURLに設定します。例：

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_OPENAI_API_KEY = 'your-openai-api-key-here';
SET @@GLOBAL.TIDB_EXP_EMBED_OPENAI_API_BASE = 'https://<your-resource-name>.openai.azure.com/openai/v1';

CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(3072) GENERATED ALWAYS AS (EMBED_TEXT(
                "openai/text-embedding-3-large",
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

リソース URL が`https://<your-resource-name>.cognitiveservices.azure.com/`と表示される場合でも、OpenAI 互換のリクエストおよびレスポンス形式を確保するには、API ベースとして`https://<your-resource-name>.openai.azure.com/openai/v1`使用する必要があることに注意してください。

Azure OpenAI から OpenAI に直接切り替えるには、 `TIDB_EXP_EMBED_OPENAI_API_BASE`空の文字列に設定します。

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_OPENAI_API_BASE = '';
```

> **注記：**
>
> -   セキュリティ上の理由から、API ベースは Azure OpenAI URL または OpenAI URL のみに設定できます。任意のベース URL は許可されません。
> -   OpenAI 互換の別の埋め込みサービスを利用する場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)お問い合わせください。

## オプション {#options}

[OpenAI埋め込みオプション](https://platform.openai.com/docs/api-reference/embeddings/create)すべて、 `EMBED_TEXT()`関数の`additional_json_options`パラメータを介してサポートされます。

**例: text-embedding-3-large に代替ディメンションを使用する**

```sql
CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(1024) GENERATED ALWAYS AS (EMBED_TEXT(
                "openai/text-embedding-3-large",
                `content`,
                '{"dimensions": 1024}'
              )) STORED
);
```

利用可能なすべてのオプションについては、 [OpenAIドキュメント](https://platform.openai.com/docs/api-reference/embeddings/create)参照してください。

## Pythonの使用例 {#python-usage-example}

[PyTiDB ドキュメント](https://pingcap.github.io/ai/guides/auto-embedding/)参照。

## 参照 {#see-also}

-   [自動埋め込みの概要](/tidb-cloud/vector-search-auto-embedding-overview.md)
-   [ベクトル検索](/vector-search/vector-search-overview.md)
-   [ベクトル関数と演算子](/vector-search/vector-search-functions-and-operators.md)
-   [ハイブリッド検索](/tidb-cloud/vector-search-hybrid-search.md)
