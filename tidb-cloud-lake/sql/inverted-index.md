---
title: 転置インデックス
summary: このページでは、{{{ .lake }}} における転置インデックス操作の包括的な概要を、参照しやすいよう機能別に整理して説明します。
---

# 転置インデックス

このページでは、{{{ .lake }}} における転置インデックス操作の包括的な概要を、参照しやすいよう機能別に整理して説明します。

## 転置インデックスの管理 {#inverted-index-management}

| コマンド | 説明 |
|---------|-------------|
| [CREATE INVERTED INDEX](/tidb-cloud-lake/sql/create-inverted-index.md) | 全文検索用の新しい転置インデックスを作成します |
| [DROP INVERTED INDEX](/tidb-cloud-lake/sql/drop-inverted-index.md) | 転置インデックスを削除します |
| [REFRESH INVERTED INDEX](/tidb-cloud-lake/sql/refresh-inverted-index.md) | 最新のデータで転置インデックスを更新します |

## 関連トピック {#related-topics}

- [Full-Text Index](/tidb-cloud-lake/guides/full-text-index.md)

> **Note:**
>
> {{{ .lake }}} の転置インデックスにより、テキストデータに対する効率的な全文検索機能が実現され、大規模なテキストカラム全体に対して高速なキーワード検索を実行できます。