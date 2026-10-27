---
title: Ngram インデックス
summary: このページでは、{{{ .lake }}} における Ngram インデックスの操作について、参照しやすいよう機能別に包括的に説明します。
---

# Ngram インデックス

このページでは、{{{ .lake }}} における Ngram インデックスの操作について、参照しやすいよう機能別に包括的に説明します。

## Ngram インデックスの管理 {#ngram-index-management}

| コマンド                                       | 説明                                              |
|-----------------------------------------------|----------------------------------------------------------|
| [CREATE NGRAM INDEX](/tidb-cloud-lake/sql/create-ngram-index.md)   | 効率的な部分文字列検索のために新しい Ngram インデックスを作成します |
| [REFRESH NGRAM INDEX](/tidb-cloud-lake/sql/refresh-ngram-index.md) | Ngram インデックスを更新します                                 |
| [DROP NGRAM INDEX](/tidb-cloud-lake/sql/drop-ngram-index.md)       | Ngram インデックスを削除します                                   |

> **Note:**
>
> {{{ .lake }}} の Ngram インデックスを使用すると、テキストデータ内での部分文字列検索やパターンマッチ検索を効率的に実行でき、LIKE などの操作のパフォーマンスが向上します。