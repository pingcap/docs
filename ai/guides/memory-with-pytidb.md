---
title: AI エージェントのメモリの例
summary: チャットボットや会話型 AI アプリケーション向けに会話メモリを実装します。
---

# AI エージェントのメモリの例

この例では、TiDB のベクトル検索機能を活用した永続メモリを備える AI エージェントの構築方法を紹介します。

わずか数行のコードで、過去のやり取りを記憶し、時間の経過とともにコンテキストを構築する会話型 AI を作成できます。

- **永続メモリ**: セッションやユーザー操作をまたいで会話を記憶します
- **対話型チャット**: Web UI またはコマンドラインインターフェースのいずれかを使用します
- **マルチユーザー対応**: ユーザーごとに個別のメモリコンテキストを保持します
- **リアルタイムのメモリ表示**: Web インターフェースに保存されたメモリを表示します

<p align="center">
    <img src="https://docs-download.pingcap.com/media/images/docs/ai/ai-agent-with-memory-powered-by-tidb.png" alt="AI Agent with memory powered by TiDB" width="700"/>
    <p align="center"><i>TiDB によるメモリ機能を備えた AI エージェント</i></p>
</p>

## 前提条件 {#prerequisites}

開始する前に、以下を用意してください。

- **Python (>=3.10)**: [Python](https://www.python.org/downloads/) 3.10 以降をインストールします。
- **{{{ .starter }}} インスタンス**: [TiDB Cloud](https://tidbcloud.com/free-trial) で無料の {{{ .starter }}} インスタンスを作成できます。
- **OpenAI API key**: [OpenAI](https://platform.openai.com/api-keys) から OpenAI API key を取得します。

## 実行方法 {#how-to-run}

### ステップ 1. `pytidb` リポジトリをクローンする {#step-1-clone-the-pytidb-repository}

[`pytidb`](https://github.com/pingcap/pytidb) は TiDB 向けの公式 Python SDK であり、開発者が AI アプリケーションを効率的に構築できるよう設計されています。

```bash
git clone https://github.com/pingcap/pytidb.git
cd pytidb/examples/memory/
```

### ステップ 2. 必要なパッケージをインストールする {#step-2-install-the-required-packages}

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r reqs.txt
```

### ステップ 3. 環境変数を設定する {#step-3-set-environment-variables}

1. [TiDB Cloud コンソール](https://tidbcloud.com/)で [**My TiDB**](https://tidbcloud.com/tidbs) ページに移動し、対象の {{{ .starter }}} インスタンス名をクリックして概要ページを開きます。
2. 右上の **Connect** をクリックします。接続ダイアログが表示され、接続パラメータが一覧表示されます。
3. 以下のように、接続パラメータに従って環境変数を設定します。

```bash
cat > .env <<EOF
TIDB_HOST={gateway-region}.prod.aws.tidbcloud.com
TIDB_PORT=4000
TIDB_USERNAME={prefix}.root
TIDB_PASSWORD={password}
TIDB_DATABASE=test

OPENAI_API_KEY={your-openai-api-key}
EOF
```

### ステップ 4. アプリケーションを実行する {#step-4-run-the-application}

次のいずれかの方法を選択します。

### オプション 1. Web アプリケーションを起動する {#option-1-launch-the-web-application}

```bash
streamlit run app.py
```

ブラウザで `http://localhost:8501` を開き、[Web アプリケーションでメモリを操作する](https://github.com/pingcap/pytidb/tree/main/examples/memory/#interact-with-memory-in-web-application) に従って、メモリ対応 AI アシスタントの利用を開始します。

### オプション 2. コマンドラインアプリケーションを実行する {#option-2-run-the-command-line-application}

```bash
python main.py
```

[コマンドラインアプリケーションでメモリを操作する](https://github.com/pingcap/pytidb/tree/main/examples/memory/#interact-with-memory-in-command-line-application) に従って、メモリ対応 AI アシスタントの利用を開始します。

## Web アプリケーションでメモリを操作する {#interact-with-memory-in-web-application}

Web アプリケーションでは、AI アシスタントと対話できます。UI には次のコンポーネントが含まれます。

- **Sidebar**: ユーザー設定とチャット一覧。
- **Main chat area**: AI アシスタントとのチャットインターフェース。
- **Memory viewer**: 保存された事実をリアルタイムで表示するメモリビューア。

メモリの動作を確認するには、次の手順を実行します。

1. デフォルトのチャットセッションで自己紹介します。たとえば、"Hello, I am John. I work as a software engineer and love guitar." のように入力します。
2. 入力した情報がメモリビューアに表示されます。
3. サイドバーの **New chat** をクリックして、新しいチャットセッションを開始します。
4. 新しいチャットセッションで "Who am I?" と質問します。AI は以前の会話からあなたの情報を思い出します。

## コマンドラインアプリケーションでメモリを操作する {#interact-with-memory-in-command-line-application}

コマンドラインアプリケーションでは、AI アシスタントとチャットしながら自己紹介できます。

**会話例:**

```plain
Chat with AI (type 'exit' to quit)
You: Hello, I am Mini256.
AI: Hello, Mini256! How can I assist you today?
You: I am working at PingCAP.
AI: That's great to hear, Mini256! PingCAP is known for its work on distributed databases, particularly TiDB. How's your experience been working there?
You: I am developing pytidb (A Python SDK for TiDB) which helps developers easily connect to TiDB.
AI: That sounds like a great project, Mini256! Developing a Python SDK for TiDB can make it much easier for developers to integrate with TiDB and interact with it using Python. If you need any advice on best practices, libraries to use, or specific features to implement, feel free to ask!
You: exit
Goodbye!
```

最初の会話の後、AI アシスタントはあなたが提供した情報を記憶し、今後の質問への回答に利用します。

次に、新しいチャットセッションを開始して、AI アシスタントに "Who am I?" と尋ねることができます。

**別のチャットセッションでの会話例:**

```plain
Chat with AI (type 'exit' to quit)
You: Who am I?
AI: You are Mini256, and you work at PingCAP, where you are developing pytidb, a Python SDK for TiDB to assist developers in easily connecting to TiDB.
You: exit
Goodbye!
```

このように、AI アシスタントはセッションをまたいであなたのことを記憶します。

## 関連リソース {#related-resources}

- **Source Code**: [GitHub で見る](https://github.com/pingcap/pytidb/tree/main/examples/memory)