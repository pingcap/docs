---
title: DROP SEQUENCE
summary: "{{{ .lake }}} から既存のシーケンスを削除します。"
---

# DROP SEQUENCE

{{{ .lake }}} から既存のシーケンスを削除します。

## 構文 {#syntax}

```sql
DROP SEQUENCE [IF EXISTS] <sequence>
```

| パラメータ | 説明 |
|--------------|-----------------------------------------|
| `<sequence>` | 削除するシーケンスの名前です。 |

## 例 {#examples}

```sql
-- Delete a sequence named staff_id_seq
DROP SEQUENCE staff_id_seq;
```