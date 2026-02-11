---
title: AI Agent Memory Example
summary: チャットボットや会話型 AI アプリケーション用の会話メモリを実装します。
---

# AIエージェントのメモリ例 {#ai-agent-memory-example}

この例では、TiDB のベクトル検索機能を活用した永続メモリを備えた AI エージェントを構築する方法を示します。

わずか数行のコードで、過去のやり取りを記憶し、時間の経過とともにコンテキストを構築する会話型 AI を作成できます。

-   **永続メモリ**: セッションやユーザーインタラクションをまたいで会話を記憶します
-   **インタラクティブチャット**:Web UIまたはコマンドラインインターフェースを使用
-   **マルチユーザーサポート**: ユーザーごとに個別のメモリコンテキストを保持します
-   **リアルタイムメモリ表示**:保存されたメモリをWebインターフェースに表示します

<p align="center"><img src="https://docs-download.pingcap.com/media/images/docs/ai/ai-agent-with-memory-powered-by-tidb.png" alt="TiDB を搭載したメモリを備えた AI エージェント" width="700"/><p align="center"> <i>TiDB を搭載したメモリを備えた AI エージェント</i></p></p>

## 前提条件 {#prerequisites}

始める前に、次のものがあることを確認してください。

-   **Python (&gt;=3.10)** : [パイソン](https://www.python.org/downloads/) 3.10 以降のバージョンをインストールします。
-   **TiDB Cloud Starter クラスター**: [TiDB Cloud](https://tidbcloud.com/free-trial)に無料の TiDB クラスターを作成できます。
-   **OpenAI API キー**: [オープンAI](https://platform.openai.com/api-keys)から OpenAI API キーを取得します。

## 実行方法 {#how-to-run}

### ステップ1. <code>pytidb</code>リポジトリのクローンを作成する {#step-1-clone-the-code-pytidb-code-repository}

[`pytidb`](https://github.com/pingcap/pytidb)は、開発者が AI アプリケーションを効率的に構築できるように設計されています。

```bash
git clone https://github.com/pingcap/pytidb.git
cd pytidb/examples/memory/
```

### ステップ2. 必要なパッケージをインストールする {#step-2-install-the-required-packages}

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
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

OPENAI_API_KEY={your-openai-api-key}
EOF
```

### ステップ4. アプリケーションを実行する {#step-4-run-the-application}

次のいずれかのオプションを選択します。

### オプション1. Webアプリケーションを起動する {#option-1-launch-the-web-application}

```bash
streamlit run app.py
```

ブラウザを開き、 `http://localhost:8501`アクセスし、 [Webアプリケーションでメモリを操作する](https://github.com/pingcap/pytidb/tree/main/examples/memory/#interact-with-memory-in-web-application)に従ってメモリ対応 AI アシスタントの使用を開始します。

### オプション2. コマンドラインアプリケーションを実行する {#option-2-run-the-command-line-application}

```bash
python main.py
```

メモリ対応 AI アシスタントの使用を開始するには、 [コマンドラインアプリケーションでメモリを操作する](https://github.com/pingcap/pytidb/tree/main/examples/memory/#interact-with-memory-in-command-line-application)従ってください。

## Webアプリケーションでメモリを操作する {#interact-with-memory-in-web-application}

ウェブアプリケーションでは、AIアシスタントと対話できます。UIには以下のコンポーネントが含まれています。

-   **サイドバー**: ユーザー設定とチャット リスト。
-   **メインチャットエリア**：AI アシスタントとのチャット インターフェース。
-   **メモリ ビューアー**: 保存された事実を表示するリアルタイムメモリビューアー。

メモリがどのように機能するかを確認するには、次の手順に従ってください。

1.  デフォルトのチャットセッションで自己紹介をしましょう。例えば、「こんにちは、ジョンです。ソフトウェアエンジニアとして働いており、ギターが大好きです。」
2.  提供した情報はメモリビューアーで確認できます。
3.  新しいチャット セッションを開始するには、サイドバーの**[新しいチャット]**をクリックします。
4.  新しいチャットセッションで「私は誰？」と尋ねてください。AIが以前の会話からあなたの情報を思い出します。

## コマンドラインアプリケーションでメモリを操作する {#interact-with-memory-in-command-line-application}

コマンドライン アプリケーションでは、AI アシスタントとチャットして自己紹介することができます。

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

最初の会話の後、AI アシスタントはあなたが提供した情報を記憶し、将来の質問に答えるためにそれを使用します。

これで、新しいチャット セッションを開始し、AI アシスタントに「私は誰ですか?」と尋ねることができます。

**別のチャットセッションでの会話の例:**

```plain
Chat with AI (type 'exit' to quit)
You: Who am I?
AI: You are Mini256, and you work at PingCAP, where you are developing pytidb, a Python SDK for TiDB to assist developers in easily connecting to TiDB.
You: exit
Goodbye!
```

ご覧のとおり、AI アシスタントはセッションをまたいでユーザーを記憶します。

## 関連リソース {#related-resources}

-   **ソースコード**: [GitHubでビュー](https://github.com/pingcap/pytidb/tree/main/examples/memory)
