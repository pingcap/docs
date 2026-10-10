---
title: 半構造化フォーマットのロード
summary: 半構造化データには、厳密なデータベース構造には従わない一方で、意味要素を分離するためのタグやマーカーが含まれます。{{{ .lake }}} は、必要に応じてその場でのデータ変換を行いながら、`COPY INTO` コマンドを使用してこれらのフォーマットを効率的にロードします。
---

# 半構造化データのロード

半構造化データには、厳密なデータベース構造には従わない一方で、意味要素を分離するためのタグやマーカーが含まれます。{{{ .lake }}} は、`COPY INTO` コマンドを使用してこれらのフォーマットを効率的にロード (load) します。必要に応じて、その場でデータ変換を行うこともできます。

## サポートされるファイル形式 {#supported-file-formats}

| ファイル形式 | 説明 | ガイド |
| ----------- | ----------- | ----- |
| **Parquet** | 効率的なカラム指向ストレージ形式 | [Parquet のロード](/tidb-cloud-lake/guides/load-parquet.md) |
| **CSV** | カンマ区切り値 | [CSV のロード](/tidb-cloud-lake/guides/load-csv.md) |
| **TSV** | タブ区切り値 | [TSV のロード](/tidb-cloud-lake/guides/load-tsv.md) |
| **NDJSON** | 改行区切り JSON | [NDJSON のロード](/tidb-cloud-lake/guides/load-ndjson.md) |
| **ORC** | 最適化された行カラム形式 | [ORC のロード](/tidb-cloud-lake/guides/load-orc.md) |
| **Avro** | スキーマ定義を持つ行ベース形式 | [Avro のロード](/tidb-cloud-lake/guides/load-avro.md) |