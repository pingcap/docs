---
title: Vector Search Example
summary: 類似コンテンツを見つけるために、ベクトル埋め込みを使用してセマンティック検索を実装します。
---

# ベクトル検索の例 {#vector-search-example}

この例では、TiDBとローカル埋め込みモデルを用いたセマンティック検索アプリケーションの構築方法を示します。ベクトル検索を用いて、キーワードだけでなく意味に基づいて類似アイテムを検索します。

アプリケーションは、ローカル埋め込み生成に[オラマ](https://ollama.com/download) 、Web UI に[ストリームリット](https://streamlit.io/) 、RAG パイプラインの構築に[`pytidb`](https://github.com/pingcap/pytidb) (TiDB 用の公式 Python SDK) を使用します。

<p align="center"><img width="700" alt="ベクトル埋め込みによるセマンティック検索" src="https://docs-download.pingcap.com/media/images/docs/ai/semantic-search-with-vector-embeddings.png" /><p align="center"><i>ベクトル埋め込みによるセマンティック検索</i></p></p>

## 前提条件 {#prerequisites}

始める前に、次のものがあることを確認してください。

-   **Python (&gt;=3.10)** : [パイソン](https://www.python.org/downloads/) 3.10 以降のバージョンをインストールします。
-   **TiDB Cloud Starter クラスター**: [TiDB Cloud](https://tidbcloud.com/free-trial)に無料の TiDB クラスターを作成できます。
-   **Ollama** : [オラマ](https://ollama.com/download)からインストールします。

## 実行方法 {#how-to-run}

### ステップ1. Ollamaで埋め込みサービスを開始する {#step-1-start-the-embedding-service-with-ollama}

埋め込みモデルを取得します。

```bash
ollama pull mxbai-embed-large
```

埋め込みサービスが実行されていることを確認します。

```bash
curl http://localhost:11434/api/embed -d '{
  "model": "mxbai-embed-large",
  "input": "Llamas are members of the camelid family"
}'
```

### ステップ2. リポジトリのクローンを作成する {#step-2-clone-the-repository}

```bash
git clone https://github.com/pingcap/pytidb.git
cd pytidb/examples/vector_search/
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
    TIDB_DATABASE=pytidb_vector_search
    EOF
    ```

### ステップ5. Streamlitアプリを実行する {#step-5-run-the-streamlit-app}

```bash
streamlit run app.py
```

ブラウザを開いて`http://localhost:8501`アクセスします。

## 関連リソース {#related-resources}

-   **ソースコード**: [GitHubでビュー](https://github.com/pingcap/pytidb/tree/main/examples/vector_search)
