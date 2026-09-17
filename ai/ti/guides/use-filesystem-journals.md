---
title: TiDB Cloud Filesystem Journals を使う
summary: Filesystem 内のエージェントおよび自動化イベント向けの追記専用ジャーナルを作成、追記、読み取り、検索、検証する方法を学びます。
---

# TiDB Cloud Filesystem Journals を使う

ジャーナルは、TiDB Cloud Filesystem 上で実行されるエージェントワークフローおよび自動化パイプライン向けに、追記専用かつハッシュチェーン化されたイベントログを提供します。[`ti fs-journal` コマンド](/ai/ti/reference/ti-filesystem-journal.md)を使用して、ジャーナルの作成、順序付きイベントの追記、それらの検索または読み取り、ハッシュチェーンの検証を行います。

## 前提条件 {#prerequisites}

- [TiDB Cloud CLI をインストールして設定する](/ai/ti/reference/ti-install-configure-update.md)。
- `--file-system-id` を渡す、`TI_FS_FILE_SYSTEM_ID` を設定する、または Filesystem を識別する FS トークンを指定して、Filesystem を選択します。
- `--fs-token`、`TI_FS_TOKEN`、または選択した Filesystem 用に保存されているローカル認証情報を通じて、ジャーナル権限を持つ FS トークンを指定します。

## ジャーナルを作成する {#create-a-journal}

```shell
ti fs-journal create-journal \
  --journal-kind agent \
  --title "review task" \
  --actor agent:reviewer
```

返されたジャーナル ID を保存します。

## エントリを追記する {#append-entries}

```shell
ti fs-journal append-journal-entries \
  --journal-id "<journal-id>" \
  --entry-json '{"type":"review_started"}'
```

サポートされる入力形式とエントリフィールドについては、[`append-journal-entries` リファレンス](/ai/ti/reference/ti-fs-journal-append-journal-entries.md)を参照してください。

## エントリを読み取りおよび検索する {#read-and-search-entries}

シーケンス順にエントリを読み取ります。

```shell
ti fs-journal read-journal-entries --journal-id "<journal-id>"
```

ジャーナルとエントリをまたいで検索します。

```shell
ti fs-journal search-journal-entries \
  --entry-type review_started \
  --include-entries
```

## ジャーナルを検証する {#verify-a-journal}

ジャーナルのハッシュチェーンが完全であることを検証します。

```shell
ti fs-journal verify-journal --journal-id "<journal-id>"
```

## 次のステップ {#what-s-next}

- [TiDB Cloud Filesystem Journal に Agent Workflow を記録する](/ai/ti/guides/ti-journal-agent-workflow-example.md)
- [TiDB Cloud Filesystem Journal CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem-journal.md)
