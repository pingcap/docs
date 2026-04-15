---
title: AI Agent Memory Example
summary: チャットボットや対話型AIアプリケーション向けに、会話メモリを実装する。
---

# AIエージェントのメモリ例 {#ai-agent-memory-example}

この例では、TiDBのベクトル検索機能を利用した、永続メモリを備えたAIエージェントの構築方法を示します。

ほんの数行のコードで、過去のやり取りを記憶し、時間の経過とともに文脈を構築していく対話型AIを作成できます。

-   **永続メモリ**：セッションをまたいでの会話やユーザー操作を記憶します
-   **対話型チャット**：Web UIまたはコマンドラインインターフェースのいずれかを使用します。
-   **マルチユーザーサポート**：ユーザーごとに個別のメモリコンテキストを保持します
-   **リアルタイムメモリ表示**：ウェブインターフェースに保存されているメモリを表示します

<p align="center"><img src="https://docs-download.pingcap.com/media/images/docs/ai/ai-agent-with-memory-powered-by-tidb.png" alt="TiDBを搭載したメモリ付きAIエージェント" width="700"/><p align="center"> <i>TiDBを搭載したメモリ付きAIエージェント</i></p></p>

## 前提条件 {#prerequisites}

始める前に、以下のものを用意してください。

-   **Python (&gt;=3.10)** : [Python](https://www.python.org/downloads/) 3.10以降のバージョンをインストールしてください。
-   **TiDB Cloud Starterインスタンス**: [TiDB Cloud](https://tidbcloud.com/free-trial)で無料のTiDB Cloud Starterインスタンスを作成できます。
-   **OpenAI API キー**: [OpenAI](https://platform.openai.com/api-keys)から OpenAI API キーを取得します。

## 実行方法 {#how-to-run}

### ステップ1. <code>pytidb</code>リポジトリをクローンする {#step-1-clone-the-code-pytidb-code-repository}

[`pytidb`](https://github.com/pingcap/pytidb)はTiDBの公式Python SDKであり、開発者がAIアプリケーションを効率的に構築できるよう設計されています。

```bash
git clone https://github.com/pingcap/pytidb.git
cd pytidb/examples/memory/
```

### ステップ2. 必要なパッケージをインストールします {#step-2-install-the-required-packages}

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
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

OPENAI_API_KEY={your-openai-api-key}
EOF
```

### ステップ4．アプリケーションを実行する {#step-4-run-the-application}

以下の選択肢から1つを選んでください。

### オプション1：ウェブアプリケーションを起動する {#option-1-launch-the-web-application}

```bash
streamlit run app.py
```

ブラウザを開いて`http://localhost:8501`にアクセスし、 [Webアプリケーションでメモリを操作する](https://github.com/pingcap/pytidb/tree/main/examples/memory/#interact-with-memory-in-web-application)に従ってメモリ対応 AI アシスタントの使用を開始します。

### オプション2：コマンドラインアプリケーションを実行する {#option-2-run-the-command-line-application}

```bash
python main.py
```

メモリ対応 AI アシスタントの使用を開始するには、「コマンドラインアプリケーション[コマンドラインアプリケーションでメモリを操作する](https://github.com/pingcap/pytidb/tree/main/examples/memory/#interact-with-memory-in-command-line-application)に従ってください。

## Webアプリケーションでメモリを操作する {#interact-with-memory-in-web-application}

ウェブアプリケーションでは、AIアシスタントと対話できます。UIには以下のコンポーネントが含まれています。

-   **サイドバー**：ユーザー設定とチャットリスト。
-   **メインチャットエリア**：AIアシスタントとのチャットインターフェース。
-   **メモリビューア**：保存されている情報をリアルタイムで表示するメモリビューア。

メモリの仕組みを理解するには、以下の手順に従ってください。

1.  デフォルトのチャットセッションで自己紹介をしてください。例えば、「こんにちは、ジョンです。ソフトウェアエンジニアとして働いていて、ギターが大好きです。」など。
2.  入力された情報はメモリビューアで確認できます。
3.  新しいチャットセッションを開始するには、サイドバーの**「新しいチャット」**をクリックしてください。
4.  新しいチャットセッションで「私は誰ですか？」と質問してください。AIが過去の会話からあなたの情報を記憶します。

## コマンドラインアプリケーションでメモリを操作する {#interact-with-memory-in-command-line-application}

コマンドラインアプリケーションでは、AIアシスタントとチャットしたり、自己紹介をしたりできます。

**会話例：**

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

最初の会話の後、AIアシスタントはあなたが提供した情報を記憶し、今後の質問に答える際にそれを使用します。

これで、新しいチャットセッションを開始して、AIアシスタントに「私は誰ですか？」と尋ねることができます。

**別のチャットセッションでの会話例：**

```plain
Chat with AI (type 'exit' to quit)
You: Who am I?
AI: You are Mini256, and you work at PingCAP, where you are developing pytidb, a Python SDK for TiDB to assist developers in easily connecting to TiDB.
You: exit
Goodbye!
```

ご覧のとおり、AIアシスタントはセッションをまたいであなたのことを記憶しています！

## 関連リソース {#related-resources}

-   **ソースコード**： [GitHubでビュー](https://github.com/pingcap/pytidb/tree/main/examples/memory)
