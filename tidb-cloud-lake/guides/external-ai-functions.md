---
title: 外部 AI 関数
summary: "{{{ .lake }}} を独自のインフラストラクチャに接続して、強力な AI/ML 機能を構築します。外部関数を使用すると、データの安全性を保ちながら、カスタムモデルのデプロイ、GPU アクセラレーションの活用、あらゆる ML フレームワークとの統合が可能になります。"
---

# 外部 AI 関数 <!--Corresponding EN commit: 98a43e43b8d02b1c0a405d0332dadbd055612466-->

{{{ .lake }}} を独自のインフラストラクチャに接続して、強力な AI/ML 機能を構築します。外部関数を使用すると、データの安全性を保ちながら、カスタムモデルのデプロイ、GPU アクセラレーションの活用、あらゆる ML フレームワークとの統合が可能になります。

## 主な機能 {#key-capabilities}

| 機能 | 利点 |
|---------|----------|
| **カスタムモデル** | 任意のオープンソースまたは独自の AI/ML モデルを使用可能 |
| **GPU アクセラレーション** | GPU 搭載マシンにデプロイして、より高速な推論を実現 |
| **データプライバシー** | データを自社インフラストラクチャ内に保持 |
| **スケーラビリティ** | 独立したスケーリングとリソース最適化 |
| **柔軟性** | あらゆるプログラミング言語と ML フレームワークをサポート |

## 仕組み {#how-it-works}

1. **AI サーバーを作成**: Python と [`tidbcloudlake-udf`](https://pypi.org/project/tidbcloudlake-udf/) を使用して AI/ML サーバーを構築します
2. **関数を登録**: `CREATE FUNCTION` を使用してサーバーを {{{ .lake }}} に接続します
3. **SQL で使用**: カスタム AI 関数を SQL クエリ内で直接呼び出します

## ネットワーク要件 {#network-requirements}

外部関数は REST ではなく、**gRPC/HTTP2 上の Arrow Flight** を使用します。

1. 公開 TLS 証明書と gRPC/HTTP2 サポートを備えた HTTPS で UDF サーバーを公開します。
2. 右上隅の **Support** をクリックし、**Submit a request** を選択して、サーバーのホスト名をテナントの **UDF server allowlist** に追加するよう依頼します。
3. ファイアウォールが厳しく制限されている場合は、サポートリクエストを送信して {{{ .lake }}} の送信元アドレスを取得し、TCP 443 で許可します。

ホストが許可リストに追加されるまで、`CREATE FUNCTION` は `Unallowed UDF server address` で失敗します。また、リモートスキーマも検証するため、エンドポイントはオンラインである必要があります。

ローカルの `UDFServer` gRPC リスナーは非公開のままにし、gRPC ロードバランサーで TLS を終端してください。

```text
{{{ .lake }}} → HTTPS/HTTP2 :443 → UDFServer gRPC :8815
```

## 例: テキスト埋め込み関数 {#example-text-embedding-function}

```python
# Simple embedding UDF server demo
from tidbcloudlake_udf import udf, UDFServer
from sentence_transformers import SentenceTransformer

# Load pre-trained model
model = SentenceTransformer('all-mpnet-base-v2')  # 768-dimensional vectors

@udf(
    input_types=["STRING"],
    result_type="ARRAY(FLOAT)",
)
def ai_embed_768(inputs: list[str], headers) -> list[list[float]]:
    """Generate 768-dimensional embeddings for input texts"""
    try:
        # Process inputs in a single batch
        embeddings = model.encode(inputs)
        # Convert to list format
        return [embedding.tolist() for embedding in embeddings]
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        # Return empty lists in case of error
        return [[] for _ in inputs]

if __name__ == '__main__':
    print("Starting embedding UDF server on port 8815...")
    server = UDFServer("0.0.0.0:8815")
    server.add_function(ai_embed_768)
    server.serve()
```

```sql
-- Register the external function in {{{ .lake }}}
CREATE OR REPLACE FUNCTION ai_embed_768 (STRING)
    RETURNS ARRAY(FLOAT)
    LANGUAGE PYTHON
    HANDLER = 'ai_embed_768'
    ADDRESS = 'https://your-ml-server.example.com';

-- Use the custom embedding in queries
SELECT
    id,
    title,
    cosine_distance(
        ai_embed_768(content),
        ai_embed_768('machine learning techniques')
    ) AS similarity
FROM articles
ORDER BY similarity ASC
LIMIT 5;
```