---
title: RAG Example
summary: ドキュメント検索と言語生成を組み合わせた RAG アプリケーションを構築します。
---

# RAGの例 {#rag-example}

この例では、 [`pytidb`](https://github.com/pingcap/pytidb) (TiDB の公式 Python SDK) を使用して最小限の RAG アプリケーションを構築する方法を示します。

アプリケーションは、ローカル埋め込み生成に[オラマ](https://ollama.com/download)使用し、Web UI に[ストリームリット](https://streamlit.io/)使用し、RAG パイプラインの構築に`pytidb`使用します。

<p align="center"><img src="https://docs-download.pingcap.com/media/images/docs/ai/rag-application-built-with-pytidb.png" alt="PyTiDB で構築された RAG アプリケーション" width="600" /><p align="center"> <i>PyTiDB で構築された RAG アプリケーション</i></p></p>

## 前提条件 {#prerequisites}

始める前に、次のものがあることを確認してください。

-   **Python (&gt;=3.10)** : [パイソン](https://www.python.org/downloads/) 3.10 以降のバージョンをインストールします。
-   **TiDB Cloud Starter クラスター**: [TiDB Cloud](https://tidbcloud.com/free-trial)に無料の TiDB クラスターを作成できます。
-   **Ollama** : [オラマ](https://ollama.com/download)からインストールします。

## 実行方法 {#how-to-run}

### ステップ1.推論APIを準備する {#step-1-prepare-the-inference-api}

Ollama CLI を使用して埋め込みモデルと LLM モデルを取得します。

```bash
ollama pull mxbai-embed-large
ollama pull gemma3:4b
ollama run gemma3:4b
```

エンドポイント`/embed`と`/generate`が実行されていることを確認します。

```bash
curl http://localhost:11434/api/embed -d '{
  "model": "mxbai-embed-large",
  "input": "Llamas are members of the camelid family"
}'
```

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "gemma3:4b",
  "prompt": "Hello, Who are you?"
}'
```

### ステップ2. リポジトリのクローンを作成する {#step-2-clone-the-repository}

```bash
git clone https://github.com/pingcap/pytidb.git
cd pytidb/examples/rag/
```

### ステップ3. 必要なパッケージをインストールして環境を設定する {#step-3-install-the-required-packages-and-set-up-the-environment}

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r reqs.txt
```

### ステップ4. 環境変数を設定する {#step-4-set-environment-variables}

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で[**クラスター**](https://tidbcloud.com/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。
2.  右上隅の**「接続」**をクリックします。接続パラメータがリストされた接続ダイアログが表示されます。
3.  次のように接続パラメータに応じて環境変数を設定します。

```bash
cat > .env <<EOF
TIDB_HOST={gateway-region}.prod.aws.tidbcloud.com
TIDB_PORT=4000
TIDB_USERNAME={prefix}.root
TIDB_PASSWORD={password}
TIDB_DATABASE=test
EOF
```

### ステップ5. Streamlitアプリを実行する {#step-5-run-the-streamlit-app}

```bash
streamlit run main.py
```

ブラウザを開いて`http://localhost:8501`アクセスします。

## トラブルシューティング {#troubleshooting}

### <code>502 Bad Gateway</code>エラー {#code-502-bad-gateway-code-error}

グローバルプロキシ設定を無効にしてみてください。

## 関連リソース {#related-resources}

-   **ソースコード**: [GitHubでビュー](https://github.com/pingcap/pytidb/tree/main/examples/rag)
