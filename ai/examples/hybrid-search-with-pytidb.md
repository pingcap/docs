---
title: Hybrid Search Example
summary: より包括的な結果を得るには、ベクトル検索と全文検索を組み合わせてください。
---

# ハイブリッド検索の例 {#hybrid-search-example}

このデモでは、ベクトル検索と全文検索を組み合わせて、文書セット全体の検索精度を向上させる方法を示します。

<p align="center"><img src="https://docs-download.pingcap.com/media/images/docs/ai/tidb-hybrid-search-demo.png" alt="TiDBハイブリッド検索デモ" width="700"/><p align="center"> <i>TiDBハイブリッド検索デモ</i></p></p>

## 前提条件 {#prerequisites}

始める前に、以下のものを用意してください。

-   **Python (&gt;=3.10)** : [Python](https://www.python.org/downloads/) 3.10以降のバージョンをインストールしてください。
-   **TiDB Cloud Starterインスタンス**: [TiDB Cloud](https://tidbcloud.com/free-trial)で無料のTiDB Cloud Starterインスタンスを作成できます。
-   **OpenAI API キー**: [OpenAI](https://platform.openai.com/api-keys)から OpenAI API キーを取得します。

> **注記**
>
> 現在、全文検索は以下の製品オプションおよび地域でのみご利用いただけます。
>
> -   TiDB Cloud Starter：フランクフルト（ `eu-central-1` ）、シンガポール（ `ap-southeast-1` ）

## 実行方法 {#how-to-run}

### ステップ1. <code>pytidb</code>リポジトリをクローンする {#step-1-clone-the-code-pytidb-code-repository}

[pytidb](https://github.com/pingcap/pytidb)はTiDBの公式Python SDKであり、開発者がAIアプリケーションを効率的に構築できるよう設計されています。

```bash
git clone https://github.com/pingcap/pytidb.git
cd pytidb/examples/hybrid_search
```

### ステップ2. 必要なパッケージをインストールし、環境をセットアップします。 {#step-2-install-the-required-packages-and-set-up-the-environment}

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r reqs.txt
```

### ステップ3．環境変数を設定する {#step-3-set-environment-variables}

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、ターゲットのTiDB Cloud Starterインスタンスの名前をクリックして、その概要ページに移動します。
2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示され、接続パラメータが表示されます。
3.  接続パラメータに応じて環境変数を以下のように設定してください。

```bash
cat > .env <<EOF
TIDB_HOST={gateway-region}.prod.aws.tidbcloud.com
TIDB_PORT=4000
TIDB_USERNAME={prefix}.root
TIDB_PASSWORD={password}
TIDB_DATABASE=pytidb_hybrid_demo
OPENAI_API_KEY=<your-openai-api-key>
EOF
```

### ステップ4．デモを実行する {#step-4-run-the-demo}

### オプション1：Streamlitアプリを実行する {#option-1-run-the-streamlit-app}

ウェブUIでデモを確認したい場合は、以下のコマンドを実行してください。

```bash
streamlit run app.py
```

ブラウザを開いて`http://localhost:8501`にアクセスしてください。

### オプション2：デモスクリプトを実行する {#option-2-run-the-demo-script}

スクリプトを使ってデモを確認したい場合は、以下のコマンドを実行してください。

```bash
python example.py
```

期待される出力:

    === CONNECT TO TIDB ===
    Connected to TiDB.

    === CREATE TABLE ===
    Table created.

    === INSERT SAMPLE DATA ===
    Inserted 3 rows.

    === PERFORM HYBRID SEARCH ===
    Search results:
    [
        {
            "_distance": 0.4740166257687124,
            "_match_score": 1.6804268,
            "_score": 0.03278688524590164,
            "id": 60013,
            "text": "TiDB is a distributed database that supports OLTP, OLAP, HTAP and AI workloads."
        },
        {
            "_distance": 0.6428459116216618,
            "_match_score": 0.78427225,
            "_score": 0.03200204813108039,
            "id": 60015,
            "text": "LlamaIndex is a Python library for building AI-powered applications."
        },
        {
            "_distance": 0.641581407158715,
            "_match_score": null,
            "_score": 0.016129032258064516,
            "id": 60014,
            "text": "PyTiDB is a Python library for developers to connect to TiDB."
        }
    ]

## 関連リソース {#related-resources}

-   **ソースコード**： [GitHubでビュー](https://github.com/pingcap/pytidb/tree/main/examples/hybrid_search)
