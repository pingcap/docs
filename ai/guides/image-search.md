---
title: Image Search
summary: アプリケーションで画像検索を使用する方法を学びます。
---

# 画像検索 {#image-search}

**画像検索は**、テキストやメタデータだけでなく、視覚的なコンテンツを比較することで類似画像を見つけるのに役立ちます。この機能は、eコマース、コンテンツモデレーション、デジタルアセット管理など、画像の外観に基づいて画像を検索したり重複を除去したりする必要があるあらゆるシナリオに役立ちます。

TiDBは**ベクトル検索**による画像検索を可能にします。自動埋め込み機能により、画像URL、PIL画像、またはキーワードテキストからマルチモーダル埋め込みモデルを用いて画像埋め込みを生成できます。TiDBはその後、類似ベクトルを大規模に検索します。

> **注記：**
>
> 画像検索の完全な例については、 [画像検索の例](/ai/examples/image-search-with-pytidb.md)参照してください。

## 基本的な使い方 {#basic-usage}

### ステップ1. 埋め込み関数を定義する {#step-1-define-an-embedding-function}

画像の埋め込みを生成するには、画像入力を受け入れる埋め込みモデルが必要です。

デモンストレーションには、Jina AI のマルチモーダル埋め込みモデルを使用できます。

[ジナ・アイ](https://jina.ai/embeddings)に進み、API キーを作成し、次のように埋め込み関数を初期化します。

```python hl_lines="7"
from pytidb.embeddings import EmbeddingFunction

image_embed = EmbeddingFunction(
    # Or another provider/model that supports multimodal input
    model_name="jina_ai/jina-embedding-v4",
    api_key="{your-jina-api-key}",
    multimodal=True,
)
```

### ステップ2. テーブルとベクトルフィールドを作成する {#step-2-create-a-table-and-vector-field}

`VectorField()`画像の埋め込みを格納するためのベクトルフィールドを定義します。3 `source_field`画像のURLを格納するフィールドを指定するためのパラメータです。

```python
from pytidb.schema import TableModel, Field

class ImageItem(TableModel):
    __tablename__ = "image_items"
    id: int = Field(primary_key=True)
    image_uri: str = Field()
    image_vec: list[float] = image_embed.VectorField(
        source_field="image_uri"
    )

table = client.create_table(schema=ImageItem, if_exists="overwrite")
```

### ステップ3.画像データを挿入する {#step-3-insert-image-data}

データを挿入すると、 `image_vec`フィールドに`image_uri`から生成された埋め込みが自動的に入力されます。

```python
table.bulk_insert([
    ImageItem(image_uri="https://example.com/image1.jpg"),
    ImageItem(image_uri="https://example.com/image2.jpg"),
    ImageItem(image_uri="https://example.com/image3.jpg"),
])
```

### ステップ4. 画像検索を実行する {#step-4-perform-image-search}

画像検索はベクター検索の一種です。自動埋め込み機能では、画像URL、PIL画像、またはキーワードテキストを直接入力すると、それぞれの入力が類似マッチングのための埋め込み情報に変換されます。

#### オプション1: 画像のURLで検索 {#option-1-search-by-image-url}

画像の URL を指定して類似画像を検索します。

```python
results = table.search("https://example.com/query.jpg").limit(3).to_list()
```

クライアントは画像URLをベクトルに変換します。TiDBはベクトルを比較して最も類似した画像を返します。

#### オプション2: PIL画像で検索 {#option-2-search-by-pil-image}

画像ファイルまたはバイトを指定して類似画像を検索することもできます。

```python
from PIL import Image

image = Image.open("/path/to/query.jpg")

results = table.search(image).limit(3).to_list()
```

クライアントは、PIL イメージ オブジェクトを埋め込みモデルに送信する前に、Base64 文字列に変換します。

#### オプション3: キーワードテキストで検索 {#option-3-search-by-keyword-text}

キーワードテキストを入力して類似画像を検索することもできます。

たとえば、ペットの画像データセットを扱っている場合は、「オレンジ色のトラ猫」や「ゴールデン レトリバーの子犬」などのキーワードで検索して、類似の画像を見つけることができます。

```python
results = table.search("orange tabby cat").limit(3).to_list()
```

次に、マルチモーダル埋め込みモデルはキーワードテキストをその意味を捉える埋め込みに変換し、TiDB はベクトル検索を実行してそのキーワード埋め込みに最も類似した埋め込みを持つ画像を検索します。

## 参照 {#see-also}

-   [自動埋め込みガイド](/ai/guides/auto-embedding.md)
-   [ベクター検索ガイド](/ai/concepts/vector-search-overview.md)
-   [画像検索の例](/ai/examples/image-search-with-pytidb.md)
