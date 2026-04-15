---
title: RAG Example
summary: 文書検索と言語生成を組み合わせたRAGアプリケーションを構築する。
---

# RAGの例 {#rag-example}

この例では、 [`pytidb`](https://github.com/pingcap/pytidb) （TiDBの公式Python SDK）を使用して最小限のRAGアプリケーションを構築する方法を示します。

このアプリケーションは、ローカル埋め込み生成に[オラマ](https://ollama.com/download)、Web UI に[ストリームリット](https://streamlit.io/)リット、RAG パイプラインの構築に`pytidb`を使用します。

<p align="center"><img src="https://docs-download.pingcap.com/media/images/docs/ai/rag-application-built-with-pytidb.png" alt="PyTiDBで構築されたRAGアプリケーション" width="600" /><p align="center"> <i>PyTiDBで構築されたRAGアプリケーション</i></p></p>

## 前提条件 {#prerequisites}

始める前に、以下のものを用意してください。

-   **Python (&gt;=3.10)** : [Python](https://www.python.org/downloads/) 3.10以降のバージョンをインストールしてください。
-   **TiDB Cloud Starterインスタンス**: [TiDB Cloud](https://tidbcloud.com/free-trial)で無料のTiDB Cloud Starterインスタンスを作成できます。
-   **Ollama** :[オラマ](https://ollama.com/download)からインストールします。

## 実行方法 {#how-to-run}

### ステップ1. 推論APIを準備する {#step-1-prepare-the-inference-api}

Ollama CLIを使用して、埋め込みモデルとLLMモデルを取得します。

```bash
ollama pull mxbai-embed-large
ollama pull gemma3:4b
ollama run gemma3:4b
```

`/embed`および`/generate`エンドポイントが実行されていることを確認してください。

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

### ステップ2. リポジトリをクローンする {#step-2-clone-the-repository}

```bash
git clone https://github.com/pingcap/pytidb.git
cd pytidb/examples/rag/
```

### ステップ3．必要なパッケージをインストールし、環境をセットアップする {#step-3-install-the-required-packages-and-set-up-the-environment}

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r reqs.txt
```

### ステップ4．環境変数を設定する {#step-4-set-environment-variables}

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、ターゲットのTiDB Cloud Starterインスタンスの名前をクリックして、その概要ページに移動します。
2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示され、接続パラメータが表示されます。
3.  接続パラメータに応じて環境変数を以下のように設定してください。

```bash
cat > .env <<EOF
TIDB_HOST={gateway-region}.prod.aws.tidbcloud.com
TIDB_PORT=4000
TIDB_USERNAME={prefix}.root
TIDB_PASSWORD={password}
TIDB_DATABASE=test
EOF
```

### ステップ5. Streamlitアプリを実行します {#step-5-run-the-streamlit-app}

```bash
streamlit run main.py
```

ブラウザを開いて`http://localhost:8501`にアクセスしてください。

## トラブルシューティング {#troubleshooting}

### <code>502 Bad Gateway</code>エラー {#code-502-bad-gateway-code-error}

グローバルプロキシ設定を無効にしてみてください。

## 関連リソース {#related-resources}

-   **ソースコード**： [GitHubでビュー](https://github.com/pingcap/pytidb/tree/main/examples/rag)
