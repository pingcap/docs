---
title: ビュー
summary: このページでは、{{{ .lake }}} におけるビュー操作の包括的な概要を、参照しやすいよう機能別に整理して紹介します。
---

# ビュー

このページでは、{{{ .lake }}} におけるビュー操作の包括的な概要を、参照しやすいよう機能別に整理して紹介します。

## ビューの管理 {#view-management}

| コマンド | 説明 |
|---------|-------------|
| [CREATE VIEW](/tidb-cloud-lake/sql/create-view.md) | クエリに基づいて新しいビューを作成します |
| [ALTER VIEW](/tidb-cloud-lake/sql/alter-view.md) | 既存のビューにタグを割り当てる、または削除します |
| [DROP VIEW](/tidb-cloud-lake/sql/drop-view.md) | ビューを削除します |
| [マテリアライズドビュー](/tidb-cloud-lake/sql/materialized-view.md) | 物理ストレージを基盤とするマテリアライズドビューを作成および管理します |
| [REFRESH LINEAGE](/tidb-cloud-lake/sql/refresh-lineage.md) | 既存のビューのリネージをバックフィルまたは整合させます |

## ビュー情報 {#view-information}

| コマンド | 説明 |
|---------|-------------|
| [DESC VIEW](/tidb-cloud-lake/sql/desc-view.md) | ビューの詳細情報を表示します |
| [SHOW VIEWS](/tidb-cloud-lake/sql/show-views.md) | 現在のデータベースまたは指定したデータベース内のすべてのビューを一覧表示します |

> **Note:**
>
> {{{ .lake }}} のビューは、データベースに保存された名前付きクエリであり、テーブルのように参照できます。これにより、複雑なクエリを簡素化し、基盤となるデータへのアクセスを制御できます。