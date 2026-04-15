---
title: Vector Search Example
summary: ベクトル埋め込みを用いたセマンティック検索を実装し、類似コンテンツを検索する。
---

# ベクトル検索の例 {#vector-search-example}

この例では、TiDBとローカル埋め込みモデルを使用してセマンティック検索アプリケーションを構築する方法を示します。ベクトル検索を使用して、キーワードだけでなく意味に基づいて類似アイテムを検索します。

このアプリケーションは、ローカル エンベディング生成に[オラマ](https://ollama.com/download)、Web UI に[ストリームリット](https://streamlit.io/)、および RAG パイプラインを構築するために[`pytidb`](https://github.com/pingcap/pytidb) (TiDB 用の公式 Python SDK) を使用します。

<p align="center"><img width="700" alt="ベクトル埋め込みを用いた意味検索" src="https://docs-download.pingcap.com/media/images/docs/ai/semantic-search-with-vector-embeddings.png" /><p align="center"><i>ベクトル埋め込みを用いた意味検索</i></p></p>

## 前提条件 {#prerequisites}

始める前に、以下のものを用意してください。

-   **Python (&gt;=3.10)** : [Python](https://www.python.org/downloads/) 3.10以降のバージョンをインストールしてください。
-   **TiDB Cloud Starterインスタンス**: [TiDB Cloud](https://tidbcloud.com/free-trial)で無料のTiDB Cloud Starterインスタンスを作成できます。
-   **Ollama** :[オラマ](https://ollama.com/download)からインストールします。

## 実行方法 {#how-to-run}

### ステップ1. Ollamaで埋め込みサービスを開始する {#step-1-start-the-embedding-service-with-ollama}

埋め込みモデルを取得します。

```bash
ollama pull mxbai-embed-large
```

埋め込みサービスが実行されていることを確認してください。

```bash
curl http://localhost:11434/api/embed -d '{
  "model": "mxbai-embed-large",
  "input": "Llamas are members of the camelid family"
}'
```

### ステップ2. リポジトリをクローンする {#step-2-clone-the-repository}

```bash
git clone https://github.com/pingcap/pytidb.git
cd pytidb/examples/vector_search/
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
    TIDB_DATABASE=pytidb_vector_search
    EOF
    ```

### ステップ5. Streamlitアプリを実行します {#step-5-run-the-streamlit-app}

```bash
streamlit run app.py
```

ブラウザを開いて`http://localhost:8501`にアクセスしてください。

## 関連リソース {#related-resources}

-   **ソースコード**： [GitHubでビュー](https://github.com/pingcap/pytidb/tree/main/examples/vector_search)
