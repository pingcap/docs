---
title: RAG の例
summary: ドキュメント検索と言語生成を組み合わせた RAG アプリケーションを構築します。
---

# RAG の例

この例では、[`pytidb`](https://github.com/pingcap/pytidb)（TiDB 向け公式 Python SDK）を使用して、最小限の RAG アプリケーションを構築する方法を示します。

このアプリケーションでは、ローカルでの埋め込み生成に [Ollama](https://ollama.com/download)、Web UI に [Streamlit](https://streamlit.io/)、そして RAG パイプラインの構築に `pytidb` を使用します。

<p align="center">
  <img src="https://docs-download.pingcap.com/media/images/docs/ai/rag-application-built-with-pytidb.png" alt="RAG application built with PyTiDB" width="600" />
  <p align="center"><i>PyTiDB で構築した RAG アプリケーション</i></p>
</p>

## 前提条件 {#prerequisites}

開始する前に、以下を確認してください。

- **Python (>=3.10)**: [Python](https://www.python.org/downloads/) 3.10 以降をインストールします。
- **A {{{ .starter }}} instance**: [TiDB Cloud](https://tidbcloud.com/free-trial) で無料の {{{ .starter }}} インスタンスを作成できます。
- **Ollama**: [Ollama](https://ollama.com/download) からインストールします。

## 実行方法 {#how-to-run}

### ステップ 1. 推論 API を準備する {#step-1-prepare-the-inference-api}

Ollama CLI を使用して埋め込みモデルと LLM モデルを pull します。

```bash
ollama pull mxbai-embed-large
ollama pull gemma3:4b
ollama run gemma3:4b
```

`/embed` エンドポイントと `/generate` エンドポイントが実行中であることを確認します。

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

### ステップ 2. リポジトリをクローンする {#step-2-clone-the-repository}

```bash
git clone https://github.com/pingcap/pytidb.git
cd pytidb/examples/rag/
```

### ステップ 3. 必要なパッケージをインストールし、環境をセットアップする {#step-3-install-the-required-packages-and-set-up-the-environment}

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r reqs.txt
```

### ステップ 4. 環境変数を設定する {#step-4-set-environment-variables}

1. [TiDB Cloud コンソール](https://tidbcloud.com/) で [**My TiDB**](https://tidbcloud.com/tidbs) ページに移動し、対象の {{{ .starter }}} インスタンス名をクリックして概要ページを開きます。
2. 右上の **Connect** をクリックします。接続ダイアログが表示され、接続パラメータが一覧表示されます。
3. 以下のように、接続パラメータに従って環境変数を設定します。

```bash
cat > .env <<EOF
TIDB_HOST={gateway-region}.prod.aws.tidbcloud.com
TIDB_PORT=4000
TIDB_USERNAME={prefix}.root
TIDB_PASSWORD={password}
TIDB_DATABASE=test
EOF
```

### ステップ 5. Streamlit アプリを実行する {#step-5-run-the-streamlit-app}

```bash
streamlit run main.py
```

ブラウザを開き、`http://localhost:8501` にアクセスします。

## トラブルシューティング {#troubleshooting}

### `502 Bad Gateway` エラー {#502-bad-gateway-error}

グローバルプロキシ設定を無効にしてみてください。

## 関連リソース {#related-resources}

- **ソースコード**: [GitHub で表示](https://github.com/pingcap/pytidb/tree/main/examples/rag)