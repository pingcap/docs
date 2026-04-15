---
title: Auto Embedding Example
summary: 組み込みの埋め込みモデルを使用して、テキストデータの埋め込みを自動的に生成します。
---

# 自動埋め込みの例 {#auto-embedding-example}

この例では、 [pytidb](https://github.com/pingcap/pytidb)クライアントで[自動埋め込み](/ai/integrations/vector-search-auto-embedding-overview.md)機能を使用する方法を示します。

1.  `pytidb`クライアントを使用してTiDBに接続します。
2.  自動埋め込み用に構成されたVectorFieldを持つテーブルを定義します。
3.  プレーンテキストデータを挿入してください。埋め込みデータはバックグラウンドで自動的に生成されます。
4.  自然言語クエリを使用してベクトル検索を実行します。埋め込みベクトルは透過的に生成されます。

## 前提条件 {#prerequisites}

始める前に、以下のものを用意してください。

-   **Python (&gt;=3.10)** : [Python](https://www.python.org/downloads/) 3.10以降のバージョンをインストールしてください。
-   **TiDB Cloud Starterインスタンス**: [TiDB Cloud](https://tidbcloud.com/free-trial)で無料のTiDB Cloud Starterインスタンスを作成できます。

## 実行方法 {#how-to-run}

### ステップ1. <code>pytidb</code>リポジトリをクローンする {#step-1-clone-the-code-pytidb-code-repository}

```bash
git clone https://github.com/pingcap/pytidb.git
cd pytidb/examples/auto_embedding/
```

### ステップ2. 必要なパッケージをインストールします {#step-2-install-the-required-packages}

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
TIDB_DATABASE=test

# Using TiDB Cloud Free embedding model by default, which does not require setting up any API key
EMBEDDING_PROVIDER=tidbcloud_free
EOF
```

### ステップ4．デモを実行する {#step-4-run-the-demo}

```bash
python main.py
```

**期待される出力:**

```plain
=== Define embedding function ===
Embedding function (model id: tidbcloud_free/amazon/titan-embed-text-v2) defined

=== Define table schema ===
Table created

=== Truncate table ===
Table truncated

=== Insert sample data ===
Inserted 3 chunks

=== Perform vector search ===
id: 1, text: TiDB is a distributed database that supports OLTP, OLAP, HTAP and AI workloads., distance: 0.30373281240458805
id: 2, text: PyTiDB is a Python library for developers to connect to TiDB., distance: 0.422506501973434
id: 3, text: LlamaIndex is a Python library for building AI-powered applications., distance: 0.5267239638442787
```

## 関連リソース {#related-resources}

-   **ソースコード**： [GitHubでビュー](https://github.com/pingcap/pytidb/tree/main/examples/auto_embedding)
