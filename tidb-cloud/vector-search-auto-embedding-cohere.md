---
title: Cohere Embeddings
summary: TiDB Cloudで Cohere 埋め込みモデルを使用する方法を学びます。
---

# コヒーレ埋め込み {#cohere-embeddings}

このドキュメントでは、TiDB Cloudの[自動埋め込み](/tidb-cloud/vector-search-auto-embedding-overview.md)で Cohere 埋め込みモデルを使用して、テキスト クエリからセマンティック検索を実行する方法について説明します。

> **注記：**
>
> 現在、 [自動埋め込み](/tidb-cloud/vector-search-auto-embedding-overview.md)次の AWS リージョンのTiDB Cloud Starter クラスターでのみ利用可能です。
>
> -   `Frankfurt (eu-central-1)`
> -   `Oregon (us-west-2)`
> -   `N. Virginia (us-east-1)`

## 利用可能なモデル {#available-models}

TiDB Cloud は、以下の[コヒア](https://cohere.com/)埋め込みモデルをネイティブに提供します。API キーは必要ありません。

**Cohere Embed v3 モデル**

-   名前: `tidbcloud_free/cohere/embed-english-v3`
-   寸法: 1024
-   距離メトリック: コサイン、L2
-   言語: 英語
-   最大入力テキストトークン数: 512 (トークンあたり約4文字)
-   最大入力テキスト文字数: 2,048
-   価格: 無料
-   TiDB Cloudがホスト: ✅ `tidbcloud_free/cohere/embed-english-v3`
-   鍵をご持参ください: ✅ `cohere/embed-english-v3.0`

**Cohere 多言語埋め込み v3 モデル**

-   名前: `tidbcloud_free/cohere/embed-multilingual-v3`
-   寸法: 1024
-   距離メトリック: コサイン、L2
-   言語: 100以上の言語
-   最大入力テキストトークン数: 512 (トークンあたり約4文字)
-   最大入力テキスト文字数: 2,048
-   価格: 無料
-   TiDB Cloudがホスト: ✅ `tidbcloud_free/cohere/embed-multilingual-v3`
-   鍵をご持参ください: ✅ `cohere/embed-multilingual-v3.0`

または、ご自身のCohere APIキー（BYOK）をお持ちいただければ、 `cohere/`プレフィックスですべてのCohereモデルをご利用いただけます。例：

**Cohere Embed v4 モデル**

-   名前: `cohere/embed-v4.0`
-   寸法: 256、512、1024、1536 (デフォルト)
-   距離メトリック: コサイン、L2
-   最大入力テキストトークン数: 128,000
-   価格: Cohereによる請求
-   TiDB Cloudがホスト: ❌
-   鍵をご持参ください: ✅

Cohere モデルの完全なリストについては、 [Cohereドキュメント](https://docs.cohere.com/docs/cohere-embed)参照してください。

## SQL の使用例 (TiDB Cloudホスト) {#sql-usage-example-tidb-cloud-hosted}

次の例は、自動埋め込みを備えたTiDB Cloudでホストされている Cohere 埋め込みモデルを使用する方法を示しています。

```sql
CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(1024) GENERATED ALWAYS AS (EMBED_TEXT(
                "tidbcloud_free/cohere/embed-multilingual-v3",
                `content`,
                '{"input_type": "search_document", "input_type@search": "search_query"}'
              )) STORED
);
```

> **注記：**
>
> -   Cohere埋め込みモデルの場合、テーブルを定義する際に関数`EMBED_TEXT()`に`input_type`指定する必要があります。例えば、 `'{"input_type": "search_document", "input_type@search": "search_query"}'`指定すると、データ挿入時に`input_type`が`search_document`に設定され、ベクトル検索時に`search_query`自動的に適用されます。
>
> -   `@search`サフィックスは、フィールドがベクトル検索クエリ中にのみ有効になることを示します。そのため、クエリを記述するときに`input_type`再度指定する必要はありません。

データの挿入とクエリ:

```sql
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

## オプション（TiDB Cloudホスト） {#options-tidb-cloud-hosted}

**Embed v3**モデルと**Multilingual Embed v3**モデルはどちらも次のオプションをサポートしており、 `EMBED_TEXT()`関数の`additional_json_options`パラメータで指定できます。

-   `input_type` (必須): 埋め込みの目的を示す特別なトークンを先頭に付加します。同じタスクの埋め込みを生成する際は、常に同じ入力タイプを使用する必要があります。そうでない場合、埋め込みは異なる意味空間にマッピングされ、互換性がなくなります。唯一の例外はセマンティック検索で、ドキュメントは`search_document`で、クエリは`search_query`で埋め込まれます。
    -   `search_document` : ドキュメントから埋め込みを生成し、ベクター データベースに保存します。
    -   `search_query` : クエリから埋め込みを生成し、ベクトル データベースに保存されている埋め込みを検索します。
    -   `classification` : テキスト分類器の入力として使用される埋め込みを生成します。
    -   `clustering` : クラスタリングタスクの埋め込みを生成します。

-   `truncate` （オプション）: 最大トークン長を超える入力をAPIがどのように処理するかを制御します。以下のいずれかの値を指定できます。

    -   `NONE` (デフォルト): 入力が最大入力トークン長を超えた場合にエラーを返します。
    -   `START` : 入力が収まるまで先頭からのテキストを破棄します。
    -   `END` : 入力が収まるまで末尾からテキストを破棄します。

## SQL の使用例 (BYOK) {#sql-usage-example-byok}

Bring Your Own Key (BYOK) Cohere モデルを使用するには、次のように Cohere API キーを指定する必要があります。

> **注記**
>
> `'your-cohere-api-key-here'`実際のCohere APIキーに置き換えてください。APIキーは[Cohereダッシュボード](https://dashboard.cohere.com/)から取得できます。

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_COHERE_API_KEY = 'your-cohere-api-key-here';

CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(1024) GENERATED ALWAYS AS (EMBED_TEXT(
                "cohere/embed-v4.0",
                `content`,
                '{"input_type": "search_document", "input_type@search": "search_query"}'
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

## オプション（BYOK） {#options-byok}

[Cohere埋め込みオプション](https://docs.cohere.com/v2/reference/embed)すべて、 `EMBED_TEXT()`関数の`additional_json_options`パラメータを介してサポートされます。

**例: 検索操作と挿入操作に異なる`input_type`を指定する**

`@search`サフィックスを使用すると、フィールドはベクトル検索クエリ中にのみ有効になります。

```sql
CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(1024) GENERATED ALWAYS AS (EMBED_TEXT(
                "cohere/embed-v4.0",
                `content`,
                '{"input_type": "search_document", "input_type@search": "search_query"}'
              )) STORED
);
```

**例: 代替ディメンションを使用する**

```sql
CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(512) GENERATED ALWAYS AS (EMBED_TEXT(
                "cohere/embed-v4.0",
                `content`,
                '{"output_dimension": 512}'
              )) STORED
);
```

利用可能なすべてのオプションについては、 [Cohereドキュメント](https://docs.cohere.com/v2/reference/embed)参照してください。

## Pythonの使用例 {#python-usage-example}

[PyTiDB ドキュメント](https://pingcap.github.io/ai/guides/auto-embedding/)参照。

## 参照 {#see-also}

-   [自動埋め込みの概要](/tidb-cloud/vector-search-auto-embedding-overview.md)
-   [ベクトル検索](/vector-search/vector-search-overview.md)
-   [ベクトル関数と演算子](/vector-search/vector-search-functions-and-operators.md)
-   [ハイブリッド検索](/tidb-cloud/vector-search-hybrid-search.md)
