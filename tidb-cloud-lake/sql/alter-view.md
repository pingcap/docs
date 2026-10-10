---
title: ALTER VIEW
summary: 別の QUERY を使用して既存のビューを変更します。
---

# ALTER VIEW

既存のビューにタグを割り当てる、または削除します。タグは事前に [CREATE TAG](/tidb-cloud-lake/sql/create-tag.md) で作成しておく必要があります。詳細は [SET TAG / UNSET TAG](/tidb-cloud-lake/sql/set-tag.md) を参照してください。

> **Note:**
>
> `ALTER VIEW ... AS ...` はサポートされていません。ビューのクエリまたは出力カラムを変更するには、代わりに [CREATE OR REPLACE VIEW](/tidb-cloud-lake/sql/create-view.md) を使用してください。

## 構文 {#syntax}

```sql
ALTER VIEW [ IF EXISTS ] [ <database_name>. ]<view_name>
    SET TAG <tag_name> = '<value>' [, <tag_name> = '<value>' ...]

ALTER VIEW [ IF EXISTS ] [ <database_name>. ]<view_name>
    UNSET TAG <tag_name> [, <tag_name> ...]
```

## 例 {#examples}

```sql
ALTER VIEW default.active_users SET TAG env = 'prod', owner = 'analytics';
ALTER VIEW default.active_users UNSET TAG env, owner;
```