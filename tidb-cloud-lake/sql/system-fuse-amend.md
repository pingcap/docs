---
title: SYSTEM$FUSE_AMEND
summary: S3互換オブジェクトストレージからテーブルデータを復旧します。
---

# SYSTEM$FUSE_AMEND

S3互換オブジェクトストレージからテーブルデータを復旧します。

## 構文 {#syntax}

```sql
CALL SYSTEM$FUSE_AMEND('<database_name>', '<table_name>');
```

## 例 {#examples}

この関数は、Fail-Safe シナリオ向けに設計されています。詳細は [Fail-Safe ガイド](/tidb-cloud-lake/guides/fail-safe.md) を参照してください。