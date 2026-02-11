---
title: Text2SQL Example
summary: AI モデルを使用して自然言語クエリを SQL ステートメントに変換します。
---

# Text2SQLの例 {#text2sql-example}

このデモでは、自然言語の質問をSQLクエリに変換し、TiDBに対して実行するAI搭載インターフェースの構築方法を紹介します[`pytidb`](https://github.com/pingcap/pytidb) （TiDBの公式Python SDK）、OpenAI GPT、Streamlitを使用して構築されており、平易な英語でデータベースにクエリを実行できます。

## 前提条件 {#prerequisites}

始める前に、次のものがあることを確認してください。

-   **Python (&gt;=3.10)** : [パイソン](https://www.python.org/downloads/) 3.10 以降のバージョンをインストールします。
-   **TiDB Cloud Starter クラスター**: [TiDB Cloud](https://tidbcloud.com/free-trial)に無料の TiDB クラスターを作成できます。
-   **OpenAI API キー**: [オープンAI](https://platform.openai.com/api-keys)から OpenAI API キーを取得します。

## 実行方法 {#how-to-run}

### ステップ1. <code>pytidb</code>リポジトリのクローンを作成する {#step-1-clone-the-code-pytidb-code-repository}

```bash
git clone https://github.com/pingcap/pytidb.git
cd pytidb/examples/text2sql/
```

### ステップ2. 必要なパッケージをインストールする {#step-2-install-the-required-packages}

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r reqs.txt
```

### ステップ3. Streamlitアプリを実行する {#step-3-run-the-streamlit-app}

```bash
streamlit run app.py
```

### ステップ4. アプリを使用する {#step-4-use-the-app}

ブラウザを開いて`http://localhost:8501`アクセスします。

1.  左のサイドバーにOpenAI APIキーを入力してください
2.  左側のサイドバーにTiDB接続文字列を入力します。例: `mysql+pymysql://root@localhost:4000/test`

## 関連リソース {#related-resources}

-   **ソースコード**: [GitHubでビュー](https://github.com/pingcap/pytidb/tree/main/examples/text2sql)
