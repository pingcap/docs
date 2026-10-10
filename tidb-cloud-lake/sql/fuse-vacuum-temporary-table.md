---
title: FUSE_VACUUM_TEMPORARY_TABLE
summary: 一時テーブルは通常、セッション終了時に自動的にクリーンアップされます（詳細は CREATE TEMP TABLE を参照）。ただし、query node のクラッシュや異常なセッション終了などのイベントにより、この処理が失敗し、孤立した一時ファイルが残ることがあります。
---

# FUSE_VACUUM_TEMPORARY_TABLE

## 概要 {#overview}

一時テーブルは通常、セッション終了時に自動的にクリーンアップされます（詳細は [CREATE TEMP TABLE](/tidb-cloud-lake/sql/create-temp-table.md) を参照）。ただし、query node のクラッシュや異常なセッション終了などのイベントにより、この処理が失敗し、孤立した一時ファイルが残ることがあります。

`FUSE_VACUUM_TEMPORARY_TABLE()` は、これらの残存ファイルを手動で削除してストレージを回収します。

**この関数を使用するタイミング:**

- 既知のシステム障害や異常なセッション終了の後。
- 孤立した一時データがストレージを消費している疑いがある場合。
- このような問題が発生しやすい環境での定期的なメンテナンスタスクとして。

## 運用上の安全性 {#operational-safety}

`FUSE_VACUUM_TEMPORARY_TABLE()` 関数は、安全で信頼性の高い操作として設計されています。

- **一時データのみを対象:** 一時テーブルに属する孤立したデータファイルおよびメタデータファイルのみを特定して削除します。
- **通常テーブルへの影響なし:** この関数は、通常の永続テーブルやそのデータには影響しません。対象範囲は、参照されていない一時テーブルの残骸のクリーンアップに厳密に限定されています。

## 構文 {#syntax}

```sql
FUSE_VACUUM_TEMPORARY_TABLE();
```

## 例 {#examples}

```sql
SELECT * FROM FUSE_VACUUM_TEMPORARY_TABLE();

┌────────┐
│ result │
├────────┤
│ Ok     │
└────────┘
```