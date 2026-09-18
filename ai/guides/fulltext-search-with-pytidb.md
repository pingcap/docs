---
title: 全文検索の例
summary: TiDB の全文検索を使用して従来型のテキスト検索を実行します。
---

# 全文検索の例

この例では、多言語サポートを備えた TiDB の全文検索を使用して、e コマースの商品検索アプリを構築する方法を示します。このアプリのユーザーは、希望する言語でキーワードを使って商品を検索できます。

<p align="center">
  <img width="700" alt="E-commerce product search with full-text search" src="https://docs-download.pingcap.com/media/images/docs/ai/e-commerce-product-search-with-full-text-search.png" />
  <p align="center"><i>全文検索を使用した e コマースの商品検索</i></p>
</p>

## 前提条件 {#prerequisites}

開始する前に、以下を確認してください。

- **Python (>=3.10)**: [Python](https://www.python.org/downloads/) 3.10 以降のバージョンをインストールします。
- **{{{ .starter }}} インスタンス**: [TiDB Cloud](https://tidbcloud.com/free-trial) で無料の {{{ .starter }}} インスタンスを作成できます。

## 実行方法 {#how-to-run}

### Step 1. `pytidb` リポジトリをクローンする {#step-1-clone-the-pytidb-repository}

[`pytidb`](https://github.com/pingcap/pytidb) は TiDB 向けの公式 Python SDK であり、開発者が AI アプリケーションを効率的に構築できるよう設計されています。

```bash
git clone https://github.com/pingcap/pytidb.git
cd pytidb/examples/fulltext_search/
```

### Step 2. 必要なパッケージをインストールし、環境をセットアップする {#step-2-install-the-required-packages-and-set-up-the-environment}

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r reqs.txt
```

### Step 3. 環境変数を設定する {#step-3-set-environment-variables}

1. [TiDB Cloud コンソール](https://tidbcloud.com/) で [**My TiDB**](https://tidbcloud.com/tidbs) ページに移動し、対象の {{{ .starter }}} インスタンス名をクリックして概要ページを開きます。
2. 右上の **Connect** をクリックします。接続ダイアログが表示され、接続パラメータが一覧表示されます。
3. 以下のように、接続パラメータに従って環境変数を設定します。

```bash
cat > .env <<EOF
TIDB_HOST={gateway-region}.prod.aws.tidbcloud.com
TIDB_PORT=4000
TIDB_USERNAME={prefix}.root
TIDB_PASSWORD={password}
TIDB_DATABASE=pytidb_fulltext_demo
EOF
```

### Step 4. Streamlit アプリを実行する {#step-4-run-the-streamlit-app}

```bash
streamlit run app.py
```

ブラウザを開き、`http://localhost:8501` にアクセスします。

## 関連リソース {#related-resources}

- **ソースコード**: [GitHub で見る](https://github.com/pingcap/pytidb/tree/main/examples/fulltext_search)
