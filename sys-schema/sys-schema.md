---
title: sys Schema
summary: sys` スキーマ内のシステム テーブルについて学習します。
---

# <code>sys</code>スキーマ {#code-sys-code-schema}

TiDBはv8.0.0以降、 `sys`スキーマを提供します。3 `sys`のビューを使用して、TiDBのシステムテーブル[`INFORMATION_SCHEMA`](/information-schema/information-schema.md) [`PERFORMANCE SCHEMA`](/performance-schema/performance-schema.md)データを把握できます。

## MySQL互換性のためのテーブル {#tables-for-mysql-compatibility}

| テーブル名                                                               | 説明                                  |
| ------------------------------------------------------------------- | ----------------------------------- |
| [`schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md) | TiDB の最後の起動以降に使用されていないインデックスを記録します。 |
