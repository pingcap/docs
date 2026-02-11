---
title: Image Search Example
summary: テキストから画像への検索と画像から画像への検索の両方にマルチモーダル埋め込みを使用して画像検索アプリケーションを構築します。
---

# 画像検索の例 {#image-search-example}

この例では、TiDB ベクトル検索機能とマルチモーダル埋め込みモデルを組み合わせて画像検索アプリを構築する方法を示します。

わずか数行のコードで、テキストと画像の両方を理解する検索システムを作成できます。

-   **テキストから画像への検索**: 「ふわふわのオレンジ色の猫」など、自然言語で欲しいものを説明してペットの写真を検索します
-   **画像間検索**: 写真をアップロードして、品種、色、ポーズなどで視覚的に似ているペットを検索します

<p align="center"><img width="700" alt="PyTiDB 画像検索デモ" src="https://docs-download.pingcap.com/media/images/docs/ai/pet-image-search-via-multimodal-embeddings.png" /><p align="center"><i>マルチモーダル埋め込みによるペット画像検索</i></p></p>

## 前提条件 {#prerequisites}

始める前に、次のものがあることを確認してください。

-   **Python (&gt;=3.10)** : [パイソン](https://www.python.org/downloads/) 3.10 以降のバージョンをインストールします。
-   **TiDB Cloud Starter クラスター**: [TiDB Cloud](https://tidbcloud.com/free-trial)に無料の TiDB クラスターを作成できます。
-   **Jina AI APIキー**： [Jina AI 埋め込み](https://jina.ai/embeddings/)から無料のAPIキーを取得できます。

## 実行方法 {#how-to-run}

### ステップ1. <code>pytidb</code>リポジトリのクローンを作成する {#step-1-clone-the-code-pytidb-code-repository}

[`pytidb`](https://github.com/pingcap/pytidb)は、開発者が AI アプリケーションを効率的に構築できるように設計されています。

```bash
git clone https://github.com/pingcap/pytidb.git
cd pytidb/examples/image_search/
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

JINA_AI_API_KEY={your-jina-ai-api-key}
EOF
```

### ステップ4.データセットをダウンロードして抽出する {#step-4-download-and-extract-the-dataset}

このデモでは、 [オックスフォードペットデータセット](https://www.robots.ox.ac.uk/~vgg/data/pets/)を使用してペットの画像を検索用にデータベースに読み込みます。

*Linux/MacOSの場合:*

```bash
# Download the dataset
curl -L -o oxford_pets.tar.gz "https://thor.robots.ox.ac.uk/~vgg/data/pets/images.tar.gz"

# Extract the dataset
mkdir -p oxford_pets
tar -xzf oxford_pets.tar.gz -C oxford_pets
```

### ステップ5. アプリを実行する {#step-5-run-the-app}

```bash
streamlit run app.py
```

ブラウザを開いて`http://localhost:8501`アクセスします。

### ステップ6. データをロードする {#step-6-load-data}

サンプル アプリでは、 **[サンプル データの読み込み]**ボタンをクリックして、サンプル データをデータベースに読み込むことができます。

または、Oxford Pets データセット内のすべてのデータをロードする場合は、 **[すべてのデータのロード]**ボタンをクリックします。

### ステップ7. 検索 {#step-7-search}

1.  サイドバーで**検索タイプ**を選択します。
2.  探しているペットの説明文を入力するか、犬または猫の写真をアップロードします。
3.  **[検索]**ボタンをクリックします。

## 関連リソース {#related-resources}

-   **ソースコード**: [GitHubでビュー](https://github.com/pingcap/pytidb/tree/main/examples/image_search)
