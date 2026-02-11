---
title: Reranking
summary: アプリケーションで再ランキングを使用する方法を学習します。
---

# 再ランキング {#reranking}

再ランキングは、専用の再ランキング モデルを使用して検索結果を再評価および並べ替えることで、検索結果の関連性と精度を向上させるために使用される手法です。

検索プロセスは次の 2 つの段階で行われます。

1.  **初期検索**: ベクトル検索により、コレクションから最も類似性の高い上位`k`ドキュメントが識別されます。
2.  **再ランキング**: 再ランキング モデルは、クエリとドキュメント間の関連性に基づいてこれら`k`ドキュメントを評価し、それらを並べ替えて最終的な上位`n`結果 ( `n` ≤ `k` ) を生成します。

この 2 段階の検索アプローチにより、ドキュメントの関連性と精度の両方が大幅に向上します。

## 基本的な使い方 {#basic-usage}

[`pytidb`](https://github.com/pingcap/pytidb)は、開発者が AI アプリケーションを効率的に構築できるように設計されています。

`pytidb`複数のサードパーティ プロバイダーの再ランキング モデルを使用できる`Reranker`クラスを提供します。

1.  再ランク付けインスタンスを作成します。

    ```python
    from pytidb.rerankers import Reranker

    reranker = Reranker(model_name="{provider}/{model_name}")
    ```

2.  `.rerank()`の方法を使用してリランカーを適用します。

    ```python
    table.search("{query}").rerank(reranker, "{field_to_rerank}").limit(3)
    ```

## サポートされているプロバイダー {#supported-providers}

次の例は、サードパーティ プロバイダーの再ランキング モデルを使用する方法を示しています。

### ジナ・アイ {#jina-ai}

Jina AI のリランカーを使用するには、 [Webサイト](https://jina.ai/reranker)にアクセスして API キーを作成します。

例えば：

```python
jinaai = Reranker(
    # Using the `jina-reranker-m0` model
    model_name="jina_ai/jina-reranker-m0",
    api_key="{your-jinaai-api-key}"
)
```
