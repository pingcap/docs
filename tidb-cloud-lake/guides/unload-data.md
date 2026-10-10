---
title: TiDB Cloud Lake からデータをアンロード
summary: "`COPY INTO` コマンドを使用して、TiDB Cloud Lake からさまざまなファイル形式およびストレージ保存先にデータをアンロードする方法を学びます。"
---

# TiDB Cloud Lake からデータをアンロード

{{{ .lake }}} の `COPY INTO` コマンドを使用すると、柔軟なフォーマットオプションを指定して、さまざまなファイル形式やストレージ保存先にデータをエクスポートできます。

## サポートされるファイル形式 {#supported-file-formats}

| 形式 | 構文例 | 主なユースケース |
|--------|---------------|------------------|
| [**Parquet ファイルをアンロード**](/tidb-cloud-lake/guides/unload-parquet-file.md) | `FILE_FORMAT = (TYPE = PARQUET)` | 分析ワークロード、効率的なストレージ |
| [**CSV ファイルをアンロード**](/tidb-cloud-lake/guides/unload-csv-file.md) | `FILE_FORMAT = (TYPE = CSV)` | データ交換、幅広い互換性 |
| [**TSV ファイルをアンロード**](/tidb-cloud-lake/guides/unload-tsv-file.md) | `FILE_FORMAT = (TYPE = TSV)` | タブ区切りデータとカンマ値 |
| [**NDJSON ファイルをアンロード**](/tidb-cloud-lake/guides/unload-ndjson-file.md) | `FILE_FORMAT = (TYPE = NDJSON)` | 半構造化データ、柔軟なスキーマ |
| [**Lance データセットをアンロード**](/tidb-cloud-lake/guides/unload-lance-dataset.md) | `FILE_FORMAT = (TYPE = LANCE)` | ML およびベクトルワークロード、Arrow/Lance コンシューマー |

## ストレージ保存先 {#storage-destinations}

| 保存先 | 例 | 使用する場面 |
|-------------|---------|-------------|
| **Named Stage** | `COPY INTO my_stage FROM my_table` | 同じ場所に繰り返しエクスポートする場合 |
| **S3-Compatible Storage** | `COPY INTO 's3://bucket/path/' FROM my_table` | Amazon S3 を使用するクラウドオブジェクトストレージ |