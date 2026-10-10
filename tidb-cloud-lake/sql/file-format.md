---
title: ファイル形式
summary: このページでは、{{{ .lake }}} における File Format 操作の包括的な概要を、参照しやすいよう機能別に整理して説明します。
---

# ファイル形式

このページでは、{{{ .lake }}} における File Format 操作の包括的な概要を、参照しやすいよう機能別に整理して説明します。

## ファイル形式の管理 {#file-format-management}

| コマンド | 説明 |
|---------|-------------|
| [CREATE FILE FORMAT](/tidb-cloud-lake/sql/create-file-format.md) | データのロード (load) およびアンロード (unload) で使用する名前付きのファイル形式オブジェクトを作成します |
| [DROP FILE FORMAT](/tidb-cloud-lake/sql/drop-file-format.md) | ファイル形式オブジェクトを削除します |

## ファイル形式の情報 {#file-format-information}

| コマンド | 説明 |
|---------|-------------|
| [SHOW FILE FORMATS](/tidb-cloud-lake/sql/show-file-formats.md) | 現在のデータベース内のすべてのファイル形式を一覧表示します |

> **Note:**
>
> {{{ .lake }}} のファイル形式は、データのロード操作時にデータファイルをどのように解析するか、またはデータのアンロード操作時にどのように整形するかを定義します。これにより、ファイルタイプ、フィールド区切り文字、圧縮、その他の書式オプションを再利用可能な形で指定できます。