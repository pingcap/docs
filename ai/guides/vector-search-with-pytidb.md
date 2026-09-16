---
title: ベクトル検索の例
summary: ベクトル埋め込みを使用したセマンティック検索を実装し、類似するコンテンツを見つけます。
---

# ベクトル検索の例

この例では、TiDB とローカル埋め込みモデルを使用してセマンティック検索アプリケーションを構築する方法を示します。ベクトル検索を使用して、意味に基づいて類似する項目を見つけます（キーワードだけではありません）。

このアプリケーションでは、ローカルでの埋め込み生成に [Ollama](https://ollama.com/download)、Web UI に [Streamlit](https://streamlit.io/)、そして RAG パイプラインの構築に [`pytidb`](https://github.com/pingcap/pytidb)（TiDB 向けの公式 Python SDK）を使用します。

<p align="center">
  <img width="700" alt="Semantic search with vector embeddings" src="https://docs-download.pingcap.com/media/images/docs/ai/semantic-search-with-vector-embeddings.png" />
  <p align="center"><i>ベクトル埋め込みを使用したセマンティック検索</i></p>
</p>

## 前提条件 {#prerequisites}

開始する前に、以下を確認してください。

- **Python (>=3.10)**: [Python](https://www.python.org/downloads/) 3.10 以降のバージョンをインストールします。
- **{{{ .starter }}} インスタンス**: [TiDB Cloud](https://tidbcloud.com/free-trial) で無料の {{{ .starter }}} インスタンスを作成できます。
- **Ollama**: [Ollama](https://ollama.com/download) からインストールします。

## 実行方法 {#how-to-run}

### ステップ 1. Ollama で埋め込みサービスを起動する {#step-1-start-the-embedding-service-with-ollama}

埋め込みモデルを取得します。

```bash
ollama pull mxbai-embed-large
```

埋め込みサービスが実行中であることを確認します。

```bash
curl http://localhost:11434/api/embed -d '{
  "model": "mxbai-embed-large",
  "input": "Llamas are members of the camelid family"
}'
```

### ステップ 2. リポジトリをクローンする {#step-2-clone-the-repository}

```bash
git clone https://github.com/pingcap/pytidb.git
cd pytidb/examples/vector_search/
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
    TIDB_DATABASE=pytidb_vector_search
    EOF
    ```

### ステップ 5. Streamlit アプリを実行する {#step-5-run-the-streamlit-app}

```bash
streamlit run app.py
```

ブラウザを開き、`http://localhost:8501` にアクセスします。

## 関連リソース {#related-resources}

- **ソースコード**: [GitHub で表示](https://github.com/pingcap/pytidb/tree/main/examples/vector_search)