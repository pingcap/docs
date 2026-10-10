---
title: VACUUM VIRTUAL COLUMN
summary: テーブルの古い仮想カラムファイルを削除します。
---

# VACUUM VIRTUAL COLUMN

テーブルの古い仮想カラムファイルを削除します。

> **Note:**
>
> このコマンドを使用するには、virtual column enterprise feature が必要です。

## 構文 {#syntax}

```sql
VACUUM VIRTUAL COLUMN FROM [ <catalog_name>. ][ <database_name>. ]<table_name>
```

## 出力 {#output}

削除されたファイル数を返します。