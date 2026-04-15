---
title: Full-Text Search Example
summary: TiDBの全文検索を使用して、従来型のテキスト検索を実行します。
---

# 全文検索の例 {#full-text-search-example}

この例では、TiDBの全文検索機能と多言語対応機能を使用して、eコマースの商品検索アプリを構築する方法を示します。このアプリのユーザーは、好みの言語でキーワードを使って商品を検索できます。

<p align="center"><img width="700" alt="全文検索機能を備えたECサイトの商品検索" src="https://docs-download.pingcap.com/media/images/docs/ai/e-commerce-product-search-with-full-text-search.png" /><p align="center"><i>全文検索機能を備えたECサイトの商品検索</i></p></p>

## 前提条件 {#prerequisites}

始める前に、以下のものを用意してください。

-   **Python (&gt;=3.10)** : [Python](https://www.python.org/downloads/) 3.10以降のバージョンをインストールしてください。
-   **TiDB Cloud Starterインスタンス**: [TiDB Cloud](https://tidbcloud.com/free-trial)で無料のTiDB Cloud Starterインスタンスを作成できます。

## 実行方法 {#how-to-run}

### ステップ1. <code>pytidb</code>リポジトリをクローンする {#step-1-clone-the-code-pytidb-code-repository}

[`pytidb`](https://github.com/pingcap/pytidb)はTiDBの公式Python SDKであり、開発者がAIアプリケーションを効率的に構築できるよう設計されています。

```bash
git clone https://github.com/pingcap/pytidb.git
cd pytidb/examples/fulltext_search/
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
TIDB_DATABASE=pytidb_fulltext_demo
EOF
```

### ステップ4. Streamlitアプリを実行します {#step-4-run-the-streamlit-app}

```bash
streamlit run app.py
```

ブラウザを開いて`http://localhost:8501`にアクセスしてください。

## 関連リソース {#related-resources}

-   **ソースコード**： [GitHubでビュー](https://github.com/pingcap/pytidb/tree/main/examples/fulltext_search)
