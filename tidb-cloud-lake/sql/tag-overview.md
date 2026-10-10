---
title: Tag
summary: TiDB Cloud Lake におけるタグ管理と割り当ての概要。
---

# Tag

タグを使用すると、データガバナンス、分類、コンプライアンス追跡のために、{{{ .lake }}} オブジェクトにキーと値のメタデータを付与できます。許可される値を任意で指定してタグを定義し、それらをオブジェクトに割り当て、`TAG_REFERENCES` テーブル関数を通じてタグの割り当てをクエリできます。

## タグ管理 {#tag-management}

| コマンド | 説明 |
|---------|-------------|
| [CREATE TAG](/tidb-cloud-lake/sql/create-tag.md) | 任意の許可値とコメントを指定して新しいタグを作成します |
| [DROP TAG](/tidb-cloud-lake/sql/drop-tag.md) | タグを削除します（アクティブな参照がない必要があります） |
| [SHOW TAGS](/tidb-cloud-lake/sql/show-tags.md) | タグ定義を一覧表示します |

## タグの割り当て {#tag-assignment}

| コマンド | 説明 |
|---------|-------------|
| [SET TAG / UNSET TAG](/tidb-cloud-lake/sql/set-tag.md) | データベースオブジェクトにタグを割り当てる、または削除します |
| [TAG_REFERENCES](/tidb-cloud-lake/sql/tag-references.md) | 特定のオブジェクトに対するタグの割り当てをクエリします |