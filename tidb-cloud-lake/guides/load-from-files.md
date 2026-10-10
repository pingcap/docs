---
title: ファイルからのロード
summary: TiDB Cloud Lake は、データファイルをテーブルにロードするためのシンプルで強力なコマンドを提供します。ほとんどの操作は、1 つのコマンドだけで実行できます。
---

# ファイルからのロード

{{{ .lake }}} は、データファイルをテーブルにロードするためのシンプルで強力なコマンドを提供します。ほとんどの操作は、1 つのコマンドだけで実行できます。データは[サポートされている形式](/tidb-cloud-lake/sql/input-output-file-formats.md)である必要があります。

![データのロードとアンロードの概要](/media/tidb-cloud-lake/load-unload.png)

## サポートされているファイル形式 {#supported-file-formats}

| 形式 | 種類 | 説明 |
|--------|------|-------------|
| [**CSV**](/tidb-cloud-lake/guides/load-csv.md), [**TSV**](/tidb-cloud-lake/guides/load-tsv.md) | 区切り形式 | 区切り文字をカスタマイズできるテキストファイル |
| [**NDJSON**](/tidb-cloud-lake/guides/load-ndjson.md) | 半構造化 | 1 行に 1 つの JSON オブジェクトを含む形式 |
| [**Parquet**](/tidb-cloud-lake/guides/load-parquet.md) | 半構造化 | 効率的なカラム指向ストレージ形式 |
| [**ORC**](/tidb-cloud-lake/guides/load-orc.md) | 半構造化 | 高性能なカラム指向形式 |
| [**Avro**](/tidb-cloud-lake/guides/load-avro.md) | 半構造化 | スキーマを持つコンパクトなバイナリ形式 |

## ファイルの場所によるロード方法 {#loading-by-file-location}

推奨されるロード方法を確認するには、ファイルの保存場所を選択してください。

| データソース | 推奨ツール | 説明 | ドキュメント |
|-------------|-----------------|-------------|---------------|
| **stage 済みデータファイル** | **COPY INTO** | 内部 / 外部 stage または user stage から高速かつ効率的にロードします | [stage からのロード](/tidb-cloud-lake/guides/load-from-stage.md) |
| **クラウドストレージ** | **COPY INTO** | Amazon S3、Google Cloud Storage、Microsoft Azure からロードします | [バケットからのロード](/tidb-cloud-lake/guides/load-from-bucket.md) |
| **ローカルファイル** | [**LakeSQL**](https://github.com/tidbcloud/lakesql) | ローカルファイルのロード向けに設計された {{{ .lake }}} ネイティブの CLI ツール | [ローカルファイルからのロード](/tidb-cloud-lake/guides/load-from-local-file.md) |
| **リモートファイル** | **COPY INTO** | リモートの HTTP/HTTPS ロケーションからデータをロードします | [リモートファイルからのロード](/tidb-cloud-lake/guides/load-from-remote-file.md) |