---
title: Basic CRUD Operations
summary: データベース接続、テーブル作成、データ操作など、pytidb`の基本的な操作を学びましょう。
---

# 基本的なCRUD操作 {#basic-crud-operations}

この例では、 [`pytidb`](https://github.com/pingcap/pytidb) （TiDBの公式Python SDK）を使用して、基本的なCRUD（作成、読み取り、更新、削除）操作を示します。

1.  `pytidb`クライアントを使用してTiDBに接続します。
2.  テキスト、ベクター、JSONの列を持つテーブルを作成します。
3.  データに対して基本的なCRUD操作を実行します。

## 前提条件 {#prerequisites}

始める前に、以下のものを用意してください。

-   **Python (&gt;=3.10)** : [Python](https://www.python.org/downloads/) 3.10以降のバージョンをインストールしてください。
-   **TiDB Cloud Starterインスタンス**: [TiDB Cloud](https://tidbcloud.com/free-trial)で無料のTiDB Cloud Starterインスタンスを作成できます。

## 実行方法 {#how-to-run}

### ステップ1. <code>pytidb</code>リポジトリをクローンする {#step-1-clone-the-code-pytidb-code-repository}

```bash
git clone https://github.com/pingcap/pytidb.git
cd pytidb/examples/basic/
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
EOF
```

### ステップ4．デモを実行する {#step-4-run-the-demo}

```bash
python main.py
```

*期待される出力:*

```plain
=== CREATE TABLE ===
Table created

=== TRUNCATE TABLE ===
Table truncated

=== CREATE ===
Created 3 items

=== READ ===
ID: 1, Content: TiDB is a distributed SQL database, Metadata: {'category': 'database'}
ID: 2, Content: GPT-4 is a large language model, Metadata: {'category': 'llm'}
ID: 3, Content: LlamaIndex is a Python library for building AI-powered applications, Metadata: {'category': 'rag'}

=== UPDATE ===
Updated item #1
After update - ID: 1, Content: TiDB Cloud Starter is a fully-managed, auto-scaling cloud database service, Metadata: {'category': 'dbass'}

=== DELETE ===
Deleted item #2

=== FINAL STATE ===
ID: 1, Content: TiDB Cloud Starter is a fully-managed, auto-scaling cloud database service, Metadata: {'category': 'dbass'}
ID: 3, Content: LlamaIndex is a Python library for building AI-powered applications, Metadata: {'category': 'rag'}

=== COUNT ROWS ===
Number of rows: 2

=== DROP TABLE ===
Table dropped

Basic CRUD operations completed!
```

## 関連リソース {#related-resources}

-   **ソースコード**： [GitHubでビュー](https://github.com/pingcap/pytidb/tree/main/examples/basic)
