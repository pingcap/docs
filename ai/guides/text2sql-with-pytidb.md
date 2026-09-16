---
title: Text2SQL の例
summary: AI モデルを使用して自然言語クエリを SQL 文に変換します。
---

# Text2SQL の例

このデモでは、自然言語の質問を SQL クエリに変換し、TiDB に対して実行する AI 搭載インターフェースの構築方法を紹介します。[`pytidb`](https://github.com/pingcap/pytidb)（TiDB の公式 Python SDK）、OpenAI GPT、Streamlit を使用して構築されており、平易な英語でデータベースをクエリできます。

## 前提条件 {#prerequisites}

開始する前に、以下を確認してください。

- **Python (>=3.10)**: [Python](https://www.python.org/downloads/) 3.10 以降のバージョンをインストールします。
- **A {{{ .starter }}} instance**: [TiDB Cloud](https://tidbcloud.com/free-trial) で無料の {{{ .starter }}} インスタンスを作成できます。
- **OpenAI API key**: [OpenAI](https://platform.openai.com/api-keys) から OpenAI API key を取得します。

## 実行方法 {#how-to-run}

### Step 1. `pytidb` リポジトリをクローンする {#step-1-clone-the-pytidb-repository}

```bash
git clone https://github.com/pingcap/pytidb.git
cd pytidb/examples/text2sql/
```

### Step 2. 必要なパッケージをインストールする {#step-2-install-the-required-packages}

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r reqs.txt
```

### Step 3. Streamlit アプリを実行する {#step-3-run-the-streamlit-app}

```bash
streamlit run app.py
```

### Step 4. アプリを使用する {#step-4-use-the-app}

ブラウザを開き、`http://localhost:8501` にアクセスします。

1. 左側のサイドバーに OpenAI API key を入力します
2. 左側のサイドバーに TiDB 接続文字列を入力します。例: `mysql+pymysql://root@localhost:4000/test`

## 関連リソース {#related-resources}

- **Source Code**: [GitHub で見る](https://github.com/pingcap/pytidb/tree/main/examples/text2sql)