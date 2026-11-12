---
title: VACUUM VIRTUAL COLUMN
summary: テーブルの古い仮想カラムファイルを削除します。
---

# VACUUM VIRTUAL COLUMN <!--Corresponding EN commit: e193d27f71bd790a28465eacb9c1b5141db672a8-->

テーブルの古い仮想カラムファイルを削除します。

## 構文 {#syntax}

```sql
VACUUM VIRTUAL COLUMN FROM [ <catalog_name>. ][ <database_name>. ]<table_name>
```

## 出力 {#output}

削除されたファイル数を返します。