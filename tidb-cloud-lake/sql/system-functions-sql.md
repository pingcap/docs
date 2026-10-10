---
title: システム関数
summary: このページでは、{{{ .lake }}} のシステム関連関数のリファレンス情報を提供します。これらの関数は、{{{ .lake }}} デプロイメントの内部ストレージおよびパフォーマンスに関する側面を分析および監視するのに役立ちます。
---

# システム関数

このページでは、{{{ .lake }}} のシステム関連関数のリファレンス情報を提供します。これらの関数は、{{{ .lake }}} デプロイメントの内部ストレージおよびパフォーマンスに関する側面を分析および監視するのに役立ちます。

## テーブルメタデータ関数 {#table-metadata-functions}

| 関数 | 説明 | 例 |
|----------|-------------|--------|
| [CLUSTERING_INFORMATION](/tidb-cloud-lake/sql/clustering-information.md) | テーブルのクラスタリング情報を返します | `CLUSTERING_INFORMATION('default', 'mytable')` |

## ストレージレイヤー関数 {#storage-layer-functions}

| 関数 | 説明 | 例 |
|----------|-------------|--------|
| [FUSE_SNAPSHOT](/tidb-cloud-lake/sql/fuse-snapshot.md) | テーブルのスナップショット情報を返します | `FUSE_SNAPSHOT('default', 'mytable')` |
| [FUSE_SEGMENT](/tidb-cloud-lake/sql/fuse-segment.md) | テーブルのセグメント情報を返します | `FUSE_SEGMENT('default', 'mytable')` |
| [FUSE_BLOCK](/tidb-cloud-lake/sql/fuse-block.md) | テーブルのブロック情報を返します | `FUSE_BLOCK('default', 'mytable')` |
| [FUSE_COLUMN](/tidb-cloud-lake/sql/fuse-column.md) | テーブルのカラム情報を返します | `FUSE_COLUMN('default', 'mytable')` |

## ストレージ最適化関数 {#storage-optimization-functions}

| 関数 | 説明 | 例 |
|----------|-------------|--------|
| [FUSE_STATISTIC](/tidb-cloud-lake/sql/fuse-statistic.md) | テーブルの統計情報を返します | `FUSE_STATISTIC('default', 'mytable')` |
| [FUSE_ENCODING](/tidb-cloud-lake/sql/fuse-encoding.md) | テーブルのエンコーディング情報を返します | `FUSE_ENCODING('default', 'mytable')` |
| [FUSE_VIRTUAL_COLUMN](/tidb-cloud-lake/sql/fuse-virtual-column.md) | 仮想カラム情報を返します | `FUSE_VIRTUAL_COLUMN('default', 'mytable')` |
| [FUSE_TIME_TRAVEL_SIZE](/tidb-cloud-lake/sql/fuse-time-travel-size.md) | タイムトラベルストレージ情報を返します | `FUSE_TIME_TRAVEL_SIZE('default', 'mytable')` |