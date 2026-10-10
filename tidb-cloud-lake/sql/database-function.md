---
title: DATABASE
summary: 現在選択されているデータベースの名前を返します。データベースが選択されていない場合、この関数は default を返します。
---

# DATABASE

現在選択されているデータベースの名前を返します。データベースが選択されていない場合、この関数は `default` を返します。

## 構文 {#syntax}

```sql
DATABASE()
```

## 例 {#examples}

```sql
SELECT DATABASE();

┌────────────┐
│ database() │
├────────────┤
│ default    │
└────────────┘
```