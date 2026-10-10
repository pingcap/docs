---
title: シーケンス
summary: このページでは、{{{ .lake }}} におけるシーケンス操作の包括的な概要を、参照しやすいよう機能別に整理して説明します。
---

# シーケンス

このページでは、{{{ .lake }}} におけるシーケンス操作の包括的な概要を、参照しやすいよう機能別に整理して説明します。

## シーケンス管理 {#sequence-management}

| コマンド | 説明 |
|---------|-------------|
| [CREATE SEQUENCE](/tidb-cloud-lake/sql/create-sequence.md) | 新しいシーケンスジェネレーターを作成します |
| [DROP SEQUENCE](/tidb-cloud-lake/sql/drop-sequence.md) | シーケンスジェネレーターを削除します |

## シーケンス情報 {#sequence-information}

| コマンド | 説明 |
|---------|-------------|
| [DESC SEQUENCE](/tidb-cloud-lake/sql/desc-sequence.md) | シーケンスの詳細情報を表示します |
| [SHOW SEQUENCES](/tidb-cloud-lake/sql/show-sequences.md) | 現在のデータベースまたは指定したデータベース内のすべてのシーケンスを一覧表示します |

> **Note:**
>
> {{{ .lake }}} のシーケンスは、一意の数値を順番に生成するために使用され、主キーやその他の一意識別子によく利用されます。