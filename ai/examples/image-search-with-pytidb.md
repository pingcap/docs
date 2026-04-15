---
title: Image Search Example
summary: テキストから画像への検索と画像から画像への検索の両方に対応する、マルチモーダル埋め込みを用いた画像検索アプリケーションを構築する。
---

# 画像検索の例 {#image-search-example}

この例では、TiDBのベクトル検索機能とマルチモーダル埋め込みモデルを組み合わせることで、画像検索アプリを構築する方法を示します。

ほんの数行のコードで、テキストと画像の両方を理解する検索システムを作成できます。

-   **テキストから画像への検索**：例えば「ふわふわのオレンジ色の猫」のように、自然言語でペットの写真を説明することで、ペットの写真を検索できます。
-   **画像検索**：写真をアップロードして、犬種、色、ポーズなど、視覚的に類似したペットを検索します。

<p align="center"><img width="700" alt="PyTiDB画像検索デモ" src="https://docs-download.pingcap.com/media/images/docs/ai/pet-image-search-via-multimodal-embeddings.png" /><p align="center"><i>マルチモーダル埋め込みによるペット画像検索</i></p></p>

## 前提条件 {#prerequisites}

始める前に、以下のものを用意してください。

-   **Python (&gt;=3.10)** : [Python](https://www.python.org/downloads/) 3.10以降のバージョンをインストールしてください。
-   **TiDB Cloud Starterインスタンス**: [TiDB Cloud](https://tidbcloud.com/free-trial)で無料のTiDB Cloud Starterインスタンスを作成できます。
-   **Jina AI API キー**: [Jina AI埋め込み](https://jina.ai/embeddings/)から無料の API キーを取得できます。

## 実行方法 {#how-to-run}

### ステップ1. <code>pytidb</code>リポジトリをクローンする {#step-1-clone-the-code-pytidb-code-repository}

[`pytidb`](https://github.com/pingcap/pytidb)はTiDBの公式Python SDKであり、開発者がAIアプリケーションを効率的に構築できるよう設計されています。

```bash
git clone https://github.com/pingcap/pytidb.git
cd pytidb/examples/image_search/
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

JINA_AI_API_KEY={your-jina-ai-api-key}
EOF
```

### ステップ4．データセットをダウンロードして解凍する {#step-4-download-and-extract-the-dataset}

[オックスフォード・ペットデータセット](https://www.robots.ox.ac.uk/~vgg/data/pets/)を使用して、ペット画像をデータベースに読み込んで検索するデモです。

*Linux/macOSの場合：*

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

ブラウザを開いて`http://localhost:8501`にアクセスしてください。

### ステップ6．データの読み込み {#step-6-load-data}

サンプルアプリでは、 **「サンプルデータの読み込み**」ボタンをクリックすると、サンプルデータがデータベースに読み込まれます。

または、オックスフォード・ペット・データセットのすべてのデータを読み込みたい場合は、 **「すべてのデータを読み込む」**ボタンをクリックしてください。

### ステップ7. 検索 {#step-7-search}

1.  サイドバーで**検索タイプ**を選択してください。
2.  探しているペットの説明文を入力するか、犬または猫の写真をアップロードしてください。
3.  **検索**ボタンをクリックしてください。

## 関連リソース {#related-resources}

-   **ソースコード**： [GitHubでビュー](https://github.com/pingcap/pytidb/tree/main/examples/image_search)
