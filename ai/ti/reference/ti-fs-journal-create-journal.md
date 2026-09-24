---
title: ti fs-journal create-journal
summary: 追記専用の file system ジャーナルを作成します。
---

# ti fs-journal create-journal

ジャーナルを作成します。`--journal-id` を省略した場合、サービスによって自動生成されます。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェイスは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs-journal create-journal
  [--actor <string>]
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--journal-id <string>]
  [--journal-kind <string>]
  [--label <string>]
  [--title <string>]
  [--version]
```

## オプション {#options}

- `--actor <string>`: `type:id` 形式のアクターです。両方の部分はユーザー定義の空でない文字列であり、CLI は `type` を小文字に変換します。
- `--dry-run`: 変更を適用せずにリクエストを検証します。
- `--file-system-id <string>`: ファイルシステムを選択します。`TI_FS_FILE_SYSTEM_ID` を設定することもできます。
- `--fs-token <string>`: file system トークンを設定します。省略した場合、このコマンドは `TI_FS_TOKEN` 環境変数を使用します。どちらも指定されていない場合は、選択した file system 用にローカルに保存されているトークンを使用します。
- `--help`: ヘルプ情報を表示します。
- `--journal-id <string>`: ジャーナル ID です。省略した場合は生成されます。
- `--journal-kind <string>`: ユーザー定義のジャーナルカテゴリです。1〜64 文字で、小文字で始まり、小文字、数字、アンダースコア (`_`)、ピリオド (`.`)、またはハイフン (`-`) のみを使用する必要があります。\[default: agent]
- `--label <string>`: ジャーナルラベル `key=value` です。繰り返し指定できます。
- `--title <string>`: ジャーナルのタイトルです。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- agent ジャーナルを作成する:

    ```bash
    # Create an append-only journal for one agent task.
    ti fs-journal create-journal --file-system-id <file-system-id> --journal-id jrn-demo --journal-kind agent --title "demo task"
    ```

- ラベル付き deployment ジャーナルを作成する:

    ```bash
    # Attach actor and environment metadata for later searches.
    ti fs-journal create-journal --file-system-id <file-system-id> --journal-kind deployment --actor agent:ti --label env=dev
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem Journal CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem-journal.md)