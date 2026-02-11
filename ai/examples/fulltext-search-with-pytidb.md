---
title: Full-Text Search Example
summary: TiDB フルテキスト検索を使用して従来のテキスト検索を実行します。
---

# 全文検索の例 {#full-text-search-example}

この例では、多言語対応のTiDB全文検索を使用して、eコマース製品検索アプリを構築する方法を示します。このアプリでは、ユーザーは好みの言語でキーワードを使用して製品を検索できます。

<p align="center"><img width="700" alt="全文検索によるEコマース製品検索" src="https://docs-download.pingcap.com/media/images/docs/ai/e-commerce-product-search-with-full-text-search.png" /><p align="center"><i>全文検索によるEコマース製品検索</i></p></p>

## 前提条件 {#prerequisites}

始める前に、次のものがあることを確認してください。

-   **Python (&gt;=3.10)** : [パイソン](https://www.python.org/downloads/) 3.10 以降のバージョンをインストールします。
-   **TiDB Cloud Starter クラスター**: [TiDB Cloud](https://tidbcloud.com/free-trial)に無料の TiDB クラスターを作成できます。

## 実行方法 {#how-to-run}

### ステップ1. <code>pytidb</code>リポジトリのクローンを作成する {#step-1-clone-the-code-pytidb-code-repository}

[`pytidb`](https://github.com/pingcap/pytidb)は、開発者が AI アプリケーションを効率的に構築できるように設計されています。

```bash
git clone https://github.com/pingcap/pytidb.git
cd pytidb/examples/fulltext_search/
```

### ステップ2. 必要なパッケージをインストールして環境を設定する {#step-2-install-the-required-packages-and-set-up-the-environment}

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r reqs.txt
```

### ステップ3. 環境変数を設定する {#step-3-set-environment-variables}

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で[**クラスター**](https://tidbcloud.com/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。
2.  右上隅の**「接続」**をクリックします。接続パラメータがリストされた接続ダイアログが表示されます。
3.  次のように接続パラメータに応じて環境変数を設定します。

```bash
cat > .env <<EOF
TIDB_HOST={gateway-region}.prod.aws.tidbcloud.com
TIDB_PORT=4000
TIDB_USERNAME={prefix}.root
TIDB_PASSWORD={password}
TIDB_DATABASE=pytidb_fulltext_demo
EOF
```

### ステップ4. Streamlitアプリを実行する {#step-4-run-the-streamlit-app}

```bash
streamlit run app.py
```

ブラウザを開いて`http://localhost:8501`アクセスします。

## 関連リソース {#related-resources}

-   **ソースコード**: [GitHubでビュー](https://github.com/pingcap/pytidb/tree/main/examples/fulltext_search)
