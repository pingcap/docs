---
title: External AI Functions
---

# External AI Functions

Build powerful AI/ML capabilities by connecting Databend with your own infrastructure. External functions let you deploy custom models, leverage GPU acceleration, and integrate with any ML framework while keeping your data secure.

## Key Capabilities

| Feature | Benefits |
|---------|----------|
| **Custom Models** | Use any open-source or proprietary AI/ML models |
| **GPU Acceleration** | Deploy on GPU-equipped machines for faster inference |
| **Data Privacy** | Keep your data within your infrastructure |
| **Scalability** | Independent scaling and resource optimization |
| **Flexibility** | Support for any programming language and ML framework |

## How It Works

1. **Create AI Server**: Build your AI/ML server using Python and [databend-udf](https://pypi.org/project/databend-udf)
2. **Register Function**: Connect your server to Databend with `CREATE FUNCTION`
3. **Use in SQL**: Call your custom AI functions directly in SQL queries

## Example: Text Embedding Function

```python
# Simple embedding UDF server demo
from databend_udf import udf, UDFServer
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
-- Register the external function in Databend
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

## Learn More

- **[External Functions Guide](/guides/ai-functions/external-functions)** - Complete setup and deployment instructions
- **[Databend Cloud](https://databend.com)** - Try external functions with a free account
