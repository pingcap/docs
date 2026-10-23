---
title: ストリーム
summary: このページでは、{{{ .lake }}} におけるストリーム操作の全体像を、参照しやすいよう機能別に整理して説明します。
---

# ストリーム

このページでは、{{{ .lake }}} におけるストリーム操作の全体像を、参照しやすいよう機能別に整理して説明します。

## ストリームの管理 {#stream-management}

| コマンド | 説明 |
|---------|-------------|
| [CREATE STREAM](/tidb-cloud-lake/sql/create-stream.md) | テーブル内の変更を追跡するための新しいストリームを作成します |
| [DROP STREAM](/tidb-cloud-lake/sql/drop-stream.md) | ストリームを削除します |

## ストリーム情報 {#stream-information}

| コマンド | 説明 |
|---------|-------------|
| [DESC STREAM](/tidb-cloud-lake/sql/desc-stream.md) | ストリームの詳細情報を表示します |
| [SHOW STREAMS](/tidb-cloud-lake/sql/show-streams.md) | 現在または指定したデータベース内のすべてのストリームを一覧表示します |

## 関連トピック {#related-topics}

- [Streams によるデータの追跡と変換](/tidb-cloud-lake/guides/track-and-transform-data-via-streams.md)

> **Note:**
>
> {{{ .lake }}} のストリームは、テーブルに対する変更を追跡および取得するために使用され、継続的なデータパイプラインとリアルタイムデータ処理を実現します。