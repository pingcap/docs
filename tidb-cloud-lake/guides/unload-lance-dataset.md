---
title: Lance Dataset のアンロード
summary: Lance dataset をアンロードする方法について説明します。
---

## Lance Dataset のアンロード {#unloading-lance-dataset}

Lance エクスポートは、機械学習やベクトルワークフローのような、dataset 指向の利用者を対象としています。CSV、TSV、NDJSON、Parquet のアンロードとは異なり、{{{ .lake }}} は `.lance` データファイルに加えて、`_versions/` などのメタデータを含む Lance の **dataset directory** を書き出します。

構文:

```sql
COPY INTO { internalStage | externalStage | externalLocation }
FROM { [<database_name>.]<table_name> | ( <query> ) }
FILE_FORMAT = (TYPE = LANCE)
[MAX_FILE_SIZE = <num>]
[USE_RAW_PATH = true | false]
[OVERWRITE = true | false]
[DETAILED_OUTPUT = true | false]
```

- Lance は `COPY INTO <location>` でのみサポートされます。
- `SINGLE` と `PARTITION BY` は Lance ではサポートされません。
- `USE_RAW_PATH = false`（デフォルト）の場合、{{{ .lake }}} はターゲットパスにクエリ ID を付加するため、各エクスポートはそれぞれ専用の dataset ルートを持ちます。
- Python の `lance` など、後続のリーダー向けに安定した dataset URI が必要な場合は、`USE_RAW_PATH = true` を設定します。
- 構文の詳細は [COPY INTO location](/tidb-cloud-lake/sql/copy-into-location.md) を参照してください。
- Lance の動作に関する詳細な注意事項は [Input & Output File Formats](/tidb-cloud-lake/sql/input-output-file-formats.md#lance-options) に記載されています。

## チュートリアル {#tutorial}

この例では、小規模な文書分類 dataset を作成します。生のテキストファイルは stage に保存され、`READ_FILE` によってクエリ実行時に `BINARY` 値へ変換され、{{{ .lake }}} が最終的な dataset を Python 利用者向けに Lance 形式でエクスポートします。

### 前提条件 {#prerequisites}

{{{ .lake }}} と Python 環境の両方からアクセス可能な、S3 互換のバケットを用意します。

### Step 1. 外部 stage を作成する {#step-1-create-an-external-stage}

```sql
CREATE OR REPLACE STAGE ml_assets
URL = 's3://your-bucket/lance-demo/'
CONNECTION = (
    ENDPOINT_URL = '<your-endpoint-url>',
    ACCESS_KEY_ID = '<your-access-key-id>',
    SECRET_ACCESS_KEY = '<your-secret-access-key>',
    REGION = '<your-region>'
);
```

### Step 2. サンプルソースファイルを作成する {#step-2-create-sample-source-files}

stage に 3 つの生テキストファイルを作成します。

```sql
COPY INTO @ml_assets/raw/ticket_001.txt
FROM (SELECT 'customer asked for a refund after the package arrived damaged')
FILE_FORMAT = (TYPE = CSV FIELD_DELIMITER = '|' RECORD_DELIMITER = '\n')
SINGLE = TRUE
USE_RAW_PATH = TRUE
OVERWRITE = TRUE;

COPY INTO @ml_assets/raw/ticket_002.txt
FROM (SELECT 'customer praised the fast response and confirmed the issue was resolved')
FILE_FORMAT = (TYPE = CSV FIELD_DELIMITER = '|' RECORD_DELIMITER = '\n')
SINGLE = TRUE
USE_RAW_PATH = TRUE
OVERWRITE = TRUE;

COPY INTO @ml_assets/raw/ticket_003.txt
FROM (SELECT 'customer requested escalation because the replacement order was delayed')
FILE_FORMAT = (TYPE = CSV FIELD_DELIMITER = '|' RECORD_DELIMITER = '\n')
SINGLE = TRUE
USE_RAW_PATH = TRUE
OVERWRITE = TRUE;
```

### Step 3. マニフェストテーブルを作成する {#step-3-create-a-manifest-table}

```sql
CREATE OR REPLACE TABLE support_ticket_manifest (
    ticket_id INT,
    label STRING,
    file_path STRING
);

INSERT INTO support_ticket_manifest VALUES
    (1, 'refund', 'raw/ticket_001.txt'),
    (2, 'resolved', 'raw/ticket_002.txt'),
    (3, 'escalation', 'raw/ticket_003.txt');
```

### Step 4. dataset を Lance にエクスポートする {#step-4-export-the-dataset-to-lance}

`READ_FILE` は stage 上のテキストファイルを生バイト列として読み取ります。その後、`COPY INTO` がそれらの行を Lance dataset に書き込みます。

```sql
COPY INTO @ml_assets/datasets/support-ticket-train
FROM (
    SELECT
        ticket_id,
        label,
        file_path,
        READ_FILE('@ml_assets', file_path) AS content
    FROM support_ticket_manifest
    ORDER BY ticket_id
)
FILE_FORMAT = (TYPE = LANCE)
USE_RAW_PATH = TRUE
OVERWRITE = TRUE
DETAILED_OUTPUT = TRUE;
```

結果:

```text
┌───────────────────────────────────────────────────────────────┐
│ file_name                          │ file_size │ row_count   │
├────────────────────────────────────┼───────────┼─────────────┤
│ datasets/support-ticket-train      │ ...       │ 3           │
└───────────────────────────────────────────────────────────────┘
```

### Step 5. エクスポートされた dataset レイアウトを確認する {#step-5-inspect-the-exported-dataset-layout}

```sql
LIST @ml_assets/datasets/support-ticket-train;
```

次のようなパスを含む dataset directory が表示されます。

```text
datasets/support-ticket-train/_versions/...
datasets/support-ticket-train/data/... .lance
datasets/support-ticket-train/*.manifest
```

### Step 6. Python `lance` で検証する {#step-6-verify-with-python-lance}

Python パッケージをインストールします。

```bash
pip install pylance
```

同じオブジェクトストレージの場所から、エクスポートされた dataset を読み取ります。

```python
import os
import lance

storage_options = {
    "aws_access_key_id": os.environ["AWS_ACCESS_KEY_ID"],
    "aws_secret_access_key": os.environ["AWS_SECRET_ACCESS_KEY"],
    "region": os.environ.get("AWS_REGION", "us-east-1"),
}

if endpoint := os.environ.get("AWS_ENDPOINT_URL"):
    storage_options["aws_endpoint"] = endpoint
    storage_options["aws_allow_http"] = "true" if endpoint.startswith("http://") else "false"

dataset = lance.dataset(
    "s3://your-bucket/lance-demo/datasets/support-ticket-train",
    storage_options=storage_options,
)

table = dataset.to_table()
print(table.num_rows)
print(table["label"].to_pylist())
print(table["content"].to_pylist()[0].decode("utf-8").strip())
```

想定される出力:

```text
3
['refund', 'resolved', 'escalation']
customer asked for a refund after the package arrived damaged
```

これで、ラベル、元のパス、生ファイルのバイト列をまとめて保持する完全な Lance dataset が作成され、後続の ML 処理で利用できるようになります。