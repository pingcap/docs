---
title: sys Schema
summary: sys` スキーマ内のシステム テーブルについて学習します。
---

# <code>sys</code>スキーマ {#code-sys-code-schema}

v8.0.0 以降、TiDB は`sys`スキーマを提供します。3 `sys`のビューを使用して、TiDB のシステム テーブル[`INFORMATION_SCHEMA`](/information-schema/information-schema.md)および[`PERFORMANCE SCHEMA`](/performance-schema/performance-schema.md)のデータを把握できます。

## MySQL 互換性のためのテーブル {#tables-for-mysql-compatibility}

| テーブル名                                                               | 説明                                  |
| ------------------------------------------------------------------- | ----------------------------------- |
| [`schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md) | TiDB の最後の起動以降に使用されていないインデックスを記録します。 |
