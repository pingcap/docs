---
title: 画像検索の例
summary: テキストから画像への検索と画像から画像への検索の両方に対応するために、マルチモーダル埋め込みを使用して画像検索アプリケーションを構築します。
---

# 画像検索の例

この例では、TiDB のベクトル検索機能とマルチモーダル埋め込みモデルを組み合わせて、画像検索アプリを構築する方法を紹介します。

わずか数行のコードで、テキストと画像の両方を理解できる検索システムを作成できます。

- **テキストから画像への検索**: 「fluffy orange cat」のように、自然言語で欲しいものを説明してペットの写真を検索します
- **画像から画像への検索**: 写真をアップロードして、品種、色、ポーズなどが視覚的に似ているペットを検索します

<p align="center">
  <img width="700" alt="PyTiDB Image Search Demo" src="https://docs-download.pingcap.com/media/images/docs/ai/pet-image-search-via-multimodal-embeddings.png" />
  <p align="center"><i>マルチモーダル埋め込みによるペット画像検索</i></p>
</p>

## 前提条件 {#prerequisites}

開始する前に、以下を用意してください。

- **Python (>=3.10)**: [Python](https://www.python.org/downloads/) 3.10 以降をインストールします。
- **{{{ .starter }}} インスタンス**: [TiDB Cloud](https://tidbcloud.com/free-trial) で無料の {{{ .starter }}} インスタンスを作成できます。
- **Jina AI APIキー**: [Jina AI Embeddings](https://jina.ai/embeddings/) から無料の APIキーを取得できます。

## 実行方法 {#how-to-run}

### Step 1. `pytidb` リポジトリをクローンする {#step-1-clone-the-pytidb-repository}

[`pytidb`](https://github.com/pingcap/pytidb) は TiDB の公式 Python SDK であり、開発者が AI アプリケーションを効率的に構築できるよう設計されています。

```bash
git clone https://github.com/pingcap/pytidb.git
cd pytidb/examples/image_search/
```

### Step 2. 必要なパッケージをインストールする {#step-2-install-the-required-packages}

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r reqs.txt
```

### Step 3. 環境変数を設定する {#step-3-set-environment-variables}

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

JINA_AI_API_KEY={your-jina-ai-api-key}
EOF
```

### Step 4. データセットをダウンロードして展開する {#step-4-download-and-extract-the-dataset}

このデモでは、[Oxford Pets dataset](https://www.robots.ox.ac.uk/~vgg/data/pets/) を使用して、検索用のペット画像をデータベースに読み込みます。

*Linux/MacOS の場合:*

```bash
# Download the dataset
curl -L -o oxford_pets.tar.gz "https://thor.robots.ox.ac.uk/~vgg/data/pets/images.tar.gz"

# Extract the dataset
mkdir -p oxford_pets
tar -xzf oxford_pets.tar.gz -C oxford_pets
```

### Step 5. アプリを実行する {#step-5-run-the-app}

```bash
streamlit run app.py
```

ブラウザを開いて `http://localhost:8501` にアクセスします。

### Step 6. データを読み込む {#step-6-load-data}

サンプルアプリでは、**Load Sample Data** ボタンをクリックして、いくつかのサンプルデータをデータベースに読み込めます。

また、Oxford Pets dataset のすべてのデータを読み込みたい場合は、**Load All Data** ボタンをクリックします。

### Step 7. 検索する {#step-7-search}

1. サイドバーで **Search type** を選択します。
2. 探しているペットのテキスト説明を入力するか、犬または猫の写真をアップロードします。
3. **Search** ボタンをクリックします。

## 関連リソース {#related-resources}

- **ソースコード**: [GitHub で見る](https://github.com/pingcap/pytidb/tree/main/examples/image_search)
