---
title: Ngram Index
summary: このページでは、{{{ .lake }}} における Ngram index の操作について、参照しやすいよう機能別に包括的に説明します。
---

# Ngram Index

このページでは、{{{ .lake }}} における Ngram index の操作について、参照しやすいよう機能別に包括的に説明します。

## Ngram index の管理 {#ngram-index-management}

| Command                                       | 説明                                              |
|-----------------------------------------------|----------------------------------------------------------|
| [CREATE NGRAM INDEX](/tidb-cloud-lake/sql/create-ngram-index.md)   | 効率的な部分文字列検索のために新しい Ngram index を作成します |
| [REFRESH NGRAM INDEX](/tidb-cloud-lake/sql/refresh-ngram-index.md) | Ngram index を更新します                                 |
| [DROP NGRAM INDEX](/tidb-cloud-lake/sql/drop-ngram-index.md)       | Ngram index を削除します                                   |

> **Note:**
>
> {{{ .lake }}} の Ngram index を使用すると、テキストデータ内での部分文字列検索やパターンマッチ検索を効率的に実行でき、`LIKE` などの操作のパフォーマンスが向上します。