---
title: テーブルエンジン
summary: "{{{ .lake }}} は、データを移動することなくパフォーマンスと相互運用性の要件のバランスを取れるように、複数のテーブルエンジンを提供します。各エンジンは、{{{ .lake }}} のネイティブな Fuse ストレージから外部データレイク形式まで、特定のシナリオ向けに最適化されています。"
---

# テーブルエンジン

{{{ .lake }}} は、データを移動することなくパフォーマンスと相互運用性の要件のバランスを取れるように、複数のテーブルエンジンを提供します。各エンジンは、{{{ .lake }}} のネイティブな Fuse ストレージから外部データレイク形式まで、特定のシナリオ向けに最適化されています。

## 利用可能なエンジン {#available-engines}

| エンジン | 最適な用途 | 特長 |
| ------ | -------- | ---------- |
| [Fuse Engine Tables](/tidb-cloud-lake/sql/fuse-engine-tables.md) | ネイティブな {{{ .lake }}} テーブル | スナップショットベースのストレージ、自動クラスタリング、変更追跡 |
| [Apache Iceberg™ Tables](/tidb-cloud-lake/sql/apache-icebergtm-tables.md) | lakehouse カタログ | タイムトラベル、Schema Evolution、REST/Hive/Storage カタログ |
| [Apache Hive Tables](/tidb-cloud-lake/sql/apache-hive-tables.md) | Hive metastore データ | 外部テーブルを通じて Hive 管理のデータストアをクエリ |
| [Delta Lake Engine](/tidb-cloud-lake/sql/delta-lake-engine.md) | Delta Lake データセット | オブジェクトストレージ内の Delta テーブルを ACID 保証付きで読み取る |

## エンジンの選択 {#choosing-an-engine}

- データを {{{ .lake }}} 内で直接管理し、最高のストレージ性能とクエリ性能を求める場合は、**Fuse** を使用します。
- すでに Iceberg カタログを通じてデータセットを管理しており、lakehouse との緊密な統合が必要な場合は、**Iceberg** を選択します。
- 既存の Hive Metastore に依存しているが、{{{ .lake }}} のクエリエンジンを利用したい場合は、**Hive** を設定します。
- Delta Lake テーブルを Fuse に取り込まず、その場で分析したい場合は、**Delta** を選択します。