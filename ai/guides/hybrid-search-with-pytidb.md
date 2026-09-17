---
title: ハイブリッド検索の例
summary: ベクトル検索と全文検索を組み合わせて、より包括的な結果を得ます。
---

# ハイブリッド検索の例

このデモでは、ベクトル検索と全文検索を組み合わせて、ドキュメント集合に対する検索品質を向上させる方法を示します。

<p align="center">
    <img src="https://docs-download.pingcap.com/media/images/docs/ai/tidb-hybrid-search-demo.png" alt="TiDB Hybrid Search Demo" width="700"/>
    <p align="center"><i>TiDB Hybrid Search Demo</i></p>
</p>

## 前提条件 {#prerequisites}

開始する前に、以下を確認してください。

- **Python (>=3.10)**: [Python](https://www.python.org/downloads/) 3.10 以降のバージョンをインストールします。
- **{{{ .starter }}} インスタンス**: [TiDB Cloud](https://tidbcloud.com/free-trial) で無料の {{{ .starter }}} インスタンスを作成できます。
- **OpenAI APIキー**: [OpenAI](https://platform.openai.com/api-keys) から OpenAI APIキーを取得します。

> **Note**
>
> 現在、全文検索は次の製品オプションとリージョンでのみ利用できます。
>
> - TiDB Cloud Starter: Frankfurt (`eu-central-1`)、Singapore (`ap-southeast-1`)

## 実行方法 {#how-to-run}

### ステップ 1. `pytidb` リポジトリをクローンする {#step-1-clone-the-pytidb-repository}

[pytidb](https://github.com/pingcap/pytidb) は TiDB の公式 Python SDK であり、開発者が AI アプリケーションを効率的に構築できるように設計されています。

```bash
git clone https://github.com/pingcap/pytidb.git
cd pytidb/examples/hybrid_search
```

### ステップ 2. 必要なパッケージをインストールし、環境をセットアップする {#step-2-install-the-required-packages-and-set-up-the-environment}

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r reqs.txt
```

### ステップ 3. 環境変数を設定する {#step-3-set-environment-variables}

1. [TiDB Cloud console](https://tidbcloud.com/) で [**My TiDB**](https://tidbcloud.com/tidbs) ページに移動し、対象の {{{ .starter }}} インスタンス名をクリックして概要ページを開きます。
2. 右上の **Connect** をクリックします。接続ダイアログが表示され、接続パラメータが一覧表示されます。
3. 次のように、接続パラメータに従って環境変数を設定します。

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

### ステップ 4. デモを実行する {#step-4-run-the-demo}

### オプション 1. Streamlit アプリを実行する {#option-1-run-the-streamlit-app}

Web UI でデモを確認したい場合は、次のコマンドを実行します。

```bash
streamlit run app.py
```

ブラウザを開いて `http://localhost:8501` にアクセスします。

### オプション 2. デモスクリプトを実行する {#option-2-run-the-demo-script}

スクリプトでデモを確認したい場合は、次のコマンドを実行します。

```bash
python example.py
```

想定される出力:

```
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
```

## 関連リソース {#related-resources}

- **ソースコード**: [GitHub で見る](https://github.com/pingcap/pytidb/tree/main/examples/hybrid_search)
