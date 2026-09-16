---
title: Auto Embedding の例
summary: 組み込みの埋め込みモデルを使用して、テキストデータの埋め込みを自動生成します。
---

# Auto Embedding の例

この例では、[pytidb](https://github.com/pingcap/pytidb) クライアントで [Auto Embedding](/ai/integrations/vector-search-auto-embedding-overview.md) 機能を使用する方法を示します。

1. `pytidb` クライアントを使用して TiDB に接続します。
2. 自動埋め込み用に設定された VectorField を持つテーブルを定義します。
3. プレーンテキストデータを挿入します。埋め込みはバックグラウンドで自動的に設定されます。
4. 自然言語クエリでベクトル検索を実行します。埋め込みは透過的に生成されます。

## 前提条件 {#prerequisites}

開始する前に、以下を確認してください。

- **Python (>=3.10)**: [Python](https://www.python.org/downloads/) 3.10 以降のバージョンをインストールします。
- **A {{{ .starter }}} instance**: [TiDB Cloud](https://tidbcloud.com/free-trial) で無料の {{{ .starter }}} インスタンスを作成できます。

## 実行方法 {#how-to-run}

### Step 1. `pytidb` リポジトリをクローンする {#step-1-clone-the-pytidb-repository}

```bash
git clone https://github.com/pingcap/pytidb.git
cd pytidb/examples/auto_embedding/
```

### Step 2. 必要なパッケージをインストールする {#step-2-install-the-required-packages}

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r reqs.txt
```

### Step 3. 環境変数を設定する {#step-3-set-environment-variables}

1. [TiDB Cloud コンソール](https://tidbcloud.com/) で [**My TiDB**](https://tidbcloud.com/tidbs) ページに移動し、対象の {{{ .starter }}} インスタンス名をクリックして概要ページを開きます。
2. 右上隅の **Connect** をクリックします。接続ダイアログが表示され、接続パラメータが一覧表示されます。
3. 以下のように、接続パラメータに従って環境変数を設定します。

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

### Step 4. デモを実行する {#step-4-run-the-demo}

```bash
python main.py
```

**想定される出力:**

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

- **Source Code**: [GitHub で表示](https://github.com/pingcap/pytidb/tree/main/examples/auto_embedding)