---
title: Stream
summary: このページでは、{{{ .lake }}} における stream 操作の全体像を、参照しやすいよう機能別に整理して説明します。
---

# Stream

このページでは、{{{ .lake }}} における stream 操作の全体像を、参照しやすいよう機能別に整理して説明します。

## stream の管理 {#stream-management}

| Command | 説明 |
|---------|-------------|
| [CREATE STREAM](/tidb-cloud-lake/sql/create-stream.md) | テーブル内の変更を追跡するための新しい stream を作成します |
| [DROP STREAM](/tidb-cloud-lake/sql/drop-stream.md) | stream を削除します |

## stream 情報 {#stream-information}

| Command | 説明 |
|---------|-------------|
| [DESC STREAM](/tidb-cloud-lake/sql/desc-stream.md) | stream の詳細情報を表示します |
| [SHOW STREAMS](/tidb-cloud-lake/sql/show-streams.md) | 現在または指定したデータベース内のすべての stream を一覧表示します |

## 関連トピック {#related-topics}

- [Streams によるデータの追跡と変換](/tidb-cloud-lake/guides/track-and-transform-data-via-streams.md)

> **Note:**
>
> {{{ .lake }}} の stream は、テーブルに対する変更を追跡および取得するために使用され、継続的なデータパイプラインとリアルタイムデータ処理を実現します。