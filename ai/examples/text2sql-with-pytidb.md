---
title: Text2SQL Example
summary: AIモデルを使用して、自然言語によるクエリをSQL文に変換する。
---

# Text2SQLの例 {#text2sql-example}

このデモでは、自然言語による質問をSQLクエリに変換し、TiDBに対して実行するAI搭載インターフェースの構築方法を紹介します。pytidb（TiDBの公式Python SDK）、OpenAI GPT、およびStreamlitを使用して構築されており、平易な英語でデータベース[`pytidb`](https://github.com/pingcap/pytidb)クエリを実行できます。

## 前提条件 {#prerequisites}

始める前に、以下のものを用意してください。

-   **Python (&gt;=3.10)** : [Python](https://www.python.org/downloads/) 3.10以降のバージョンをインストールしてください。
-   **TiDB Cloud Starterインスタンス**: [TiDB Cloud](https://tidbcloud.com/free-trial)で無料のTiDB Cloud Starterインスタンスを作成できます。
-   **OpenAI API キー**: [OpenAI](https://platform.openai.com/api-keys)から OpenAI API キーを取得します。

## 実行方法 {#how-to-run}

### ステップ1. <code>pytidb</code>リポジトリをクローンする {#step-1-clone-the-code-pytidb-code-repository}

```bash
git clone https://github.com/pingcap/pytidb.git
cd pytidb/examples/text2sql/
```

### ステップ2. 必要なパッケージをインストールします {#step-2-install-the-required-packages}

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r reqs.txt
```

### ステップ3. Streamlitアプリを実行します {#step-3-run-the-streamlit-app}

```bash
streamlit run app.py
```

### ステップ4．アプリを使用する {#step-4-use-the-app}

ブラウザを開いて`http://localhost:8501`にアクセスしてください。

1.  左側のサイドバーにOpenAI APIキーを入力してください。
2.  左側のサイドバーにTiDB接続文字列を入力してください。例： `mysql+pymysql://root@localhost:4000/test`

## 関連リソース {#related-resources}

-   **ソースコード**： [GitHubでビュー](https://github.com/pingcap/pytidb/tree/main/examples/text2sql)
