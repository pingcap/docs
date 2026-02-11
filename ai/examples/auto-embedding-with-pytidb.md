---
title: Auto Embedding Example
summary: 組み込みの埋め込みモデルを使用して、テキスト データの埋め込みを自動的に生成します。
---

# 自動埋め込みの例 {#auto-embedding-example}

この例では、 [自動埋め込み](/ai/integrations/vector-search-auto-embedding-overview.md)機能を[pytidb](https://github.com/pingcap/pytidb)クライアントで使用する方法を示します。

1.  `pytidb`クライアントを使用して TiDB に接続します。
2.  自動埋め込み用に構成された VectorField を使用してテーブルを定義します。
3.  プレーンテキスト データを挿入します。埋め込みはバックグラウンドで自動的に入力されます。
4.  自然言語クエリを使用してベクトル検索を実行します。埋め込みは透過的に生成されます。

## 前提条件 {#prerequisites}

始める前に、次のものがあることを確認してください。

-   **Python (&gt;=3.10)** : [パイソン](https://www.python.org/downloads/) 3.10 以降のバージョンをインストールします。
-   **TiDB Cloud Starter クラスター**: [TiDB Cloud](https://tidbcloud.com/free-trial)に無料の TiDB クラスターを作成できます。

## 実行方法 {#how-to-run}

### ステップ1. <code>pytidb</code>リポジトリのクローンを作成する {#step-1-clone-the-code-pytidb-code-repository}

```bash
git clone https://github.com/pingcap/pytidb.git
cd pytidb/examples/auto_embedding/
```

### ステップ2. 必要なパッケージをインストールする {#step-2-install-the-required-packages}

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
TIDB_DATABASE=test

# Using TiDB Cloud Free embedding model by default, which does not require setting up any API key
EMBEDDING_PROVIDER=tidbcloud_free
EOF
```

### ステップ4.デモを実行する {#step-4-run-the-demo}

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

-   **ソースコード**: [GitHubでビュー](https://github.com/pingcap/pytidb/tree/main/examples/auto_embedding)
