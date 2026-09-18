---
title: TiDB Cloud Filesystem Journal CLI コマンドリファレンス
summary: ジャーナルの作成、追記、読み取り、検索、検証を行うすべての `ti fs-journal` コマンドのリファレンスです。
---

# TiDB Cloud Filesystem Journal CLI コマンドリファレンス

`ti fs-journal` は、エージェントおよびワークフローのイベントに対して、追記専用で検証可能な台帳を提供します。

## コマンド {#commands}

| コマンド | 説明 |
|---|---|
| [`create-journal`](/ai/ti/reference/ti-fs-journal-create-journal.md) | ジャーナルを作成します。 |
| [`append-journal-entries`](/ai/ti/reference/ti-fs-journal-append-journal-entries.md) | ジャーナルにイベントを追記します。 |
| [`read-journal-entries`](/ai/ti/reference/ti-fs-journal-read-journal-entries.md) | シーケンス順でジャーナルエントリを読み取ります。 |
| [`search-journal-entries`](/ai/ti/reference/ti-fs-journal-search-journal-entries.md) | ジャーナルとエントリを検索します。 |
| [`verify-journal`](/ai/ti/reference/ti-fs-journal-verify-journal.md) | ジャーナルのハッシュチェーンを検証します。 |

## 関連情報 {#see-also}

- [TiDB Cloud Filesystem Journal を使用する](/ai/ti/guides/use-filesystem-journals.md)
- [TiDB Cloud Filesystem Journal にエージェントワークフローを記録する](/ai/ti/guides/ti-journal-agent-workflow-example.md)